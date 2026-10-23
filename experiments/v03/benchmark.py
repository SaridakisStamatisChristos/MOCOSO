"""Run: python experiments/v03/benchmark.py --output v03_raw.json

Optional: --repetitions 5 --seed 20261023. Subprocess isolation prevents
cumulative peak RSS contamination. Not automatically part of smoke CI.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import random
import resource
import statistics
import subprocess
import sys
import time
import tracemalloc

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from experiments.v03.baselines import solve_mask, solve_edge_tuple
from experiments.v03.deficit import solve_deficit
from modconvex import solve, oracle
from edge_dp import solve_edge


def case_data(n, kind):
    if kind == 'convex':
        return [i*i for i in range(n)]
    if kind == 'alternating':
        return [(-1)**i * (i*i + 1) for i in range(n)]
    if kind == 'equal':
        return [7]*n
    if kind == 'huge':
        return [(-1)**i * (10**120 + i*i) for i in range(n)]
    raise ValueError(kind)


def call_algorithm(name, a, m):
    if name == 'deficit':
        out = solve_deficit(a, m)
        if out.status != 'OPTIMAL':
            raise AssertionError(out)
        return out.indices, {'operations': out.operations,
                             'nodes': out.nodes, 'partitions': out.candidates}
    if name == 'v02':
        out = solve(a, m, complement_cutoff=20)
        if out.status != 'OPTIMAL':
            raise AssertionError(out)
        return out.indices, {'operations': out.operations}
    if name == 'mask_isolated':
        return solve_mask(a, m), {}
    if name == 'edge_tuple':
        return solve_edge_tuple(a, m), {}
    if name == 'edge_bitmask':
        return solve_edge(a, m), {}
    raise ValueError(name)


def worker():
    cfg = json.load(sys.stdin)
    name, a, m, repetitions = (cfg[k] for k in ('algorithm', 'a', 'm', 'repetitions'))
    # Warmup separately; no tracemalloc during timing.
    expected, counters = call_algorithm(name, a, m)
    timings = []
    for _ in range(repetitions):
        begin = time.perf_counter_ns()
        witness, _ = call_algorithm(name, a, m)
        timings.append(time.perf_counter_ns() - begin)
        if witness != expected:
            raise AssertionError('nondeterministic witness')
    tracemalloc.start()
    result, _ = call_algorithm(name, a, m)
    traced_peak = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    if result != expected:
        raise AssertionError('instrumented witness drift')
    print(json.dumps({'algorithm': name, 'witness': expected,
                      'runtime_ns': timings, 'traced_peak_bytes': traced_peak,
                      'peak_rss_kib_linux': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
                          if sys.platform.startswith('linux') else None,
                      'counters': counters}))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='v03_raw.json')
    parser.add_argument('--repetitions', type=int, default=5)
    parser.add_argument('--seed', type=int, default=20261023)
    parser.add_argument('--worker', action='store_true')
    args = parser.parse_args()
    if args.worker:
        worker()
        return
    if args.repetitions < 1:
        parser.error('repetitions must be >= 1')
    rng = random.Random(args.seed)
    # Pre-registered cases. Mask sweep is restricted to h<=12 so tests are
    # bounded; edge tuple is bounded to n<=20 to control nm tuple-state cost.
    cases = [(12, 3, 'convex'), (12, 8, 'alternating'),
             (20, 7, 'convex'), (20, 12, 'alternating'),
             (20, 8, 'equal'), (20, 10, 'huge'),
             (35, 5, 'convex'), (35, 12, 'alternating')]
    jobs = []
    for n, h, family in cases:
        U = n*(n+1)//2
        m = U - h
        algorithms = ['deficit', 'v02', 'mask_isolated', 'edge_bitmask']
        if n <= 20:
            algorithms.append('edge_tuple')
        for name in algorithms:
            jobs.append((n, h, family, m, name))
    rng.shuffle(jobs)
    by_case = {}
    rows = []
    for n, h, family, m, name in jobs:
        a = case_data(n, family)
        msg = {'algorithm':name,'a':a,'m':m,'repetitions':args.repetitions}
        child = subprocess.run([sys.executable, str(Path(__file__).resolve()), '--worker'],
                               input=json.dumps(msg), text=True, capture_output=True,
                               timeout=120, check=True, cwd=ROOT)
        out = json.loads(child.stdout)
        key = (n, h, family)
        if key not in by_case:
            by_case[key] = tuple(oracle(a, m)) if n <= 12 else None
        if by_case[key] is None:
            by_case[key] = tuple(out['witness'])
        assert tuple(out['witness']) == by_case[key], (key, name, out['witness'])
        out.update(n=n, h=h, m=m, family=family,
                   median_ns=statistics.median(out['runtime_ns']),
                   min_ns=min(out['runtime_ns']), max_ns=max(out['runtime_ns']))
        rows.append(out)
        print(f'{n=} {h=} {family=} {name=}: median={out["median_ns"]} ns', flush=True)
    modules = ['modconvex.py','edge_dp.py','experiments/v03/deficit.py',
               'experiments/v03/baselines.py','experiments/v03/benchmark.py']
    hashes = {p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in modules}
    try:
        commit = subprocess.check_output(['git','rev-parse','HEAD'], cwd=ROOT,
                                         text=True, stderr=subprocess.DEVNULL).strip()
    except (OSError, subprocess.CalledProcessError):
        commit = None
    report = {'baseline_main_sha': '9cedac0d0f860564d5ee1a9064b01ef56ac2a764',
              'working_commit':commit,'file_sha256':hashes,'seed':args.seed,
              'repetitions':args.repetitions, 'python':sys.version,
              'platform':platform.platform(), 'processor':platform.processor(),
              'cpu_count':os.cpu_count(), 'rows':rows,
              'notes':['peak_rss_kib_linux is process peak including imports and warmup',
                       'tracemalloc bytes are Python tracked peak, not total RSS',
                       'counted operations differ by algorithm and cannot be compared directly',
                       'timing includes witness reconstruction, excludes subprocess startup',
                       'no hard memory limit or external timeout semantics claimed']}
    Path(args.output).write_text(json.dumps(report, indent=2)+'\n')
    print('comparison cases verified; raw report:', args.output)


if __name__ == '__main__':
    main()
