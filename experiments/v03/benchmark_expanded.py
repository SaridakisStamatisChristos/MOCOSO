"""M1 research benchmark. See research/v03/benchmark_m1.md for the protocol.

Each timed block is a fresh process; heap instrumentation is a separate call.
Every planned case/algorithm/block is retained, including skips and failures.
"""
import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import random
import statistics
import subprocess
import sys
import time
import tracemalloc

try:
    import resource
except ImportError:
    resource = None

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from experiments.v03.workloads_expanded import VERSION, build_cases, canonical_hash
from experiments.v03.baselines import solve_mask, solve_edge_tuple
from experiments.v03.deficit import solve_deficit
from modconvex import solve, cubic_dp, dense_dp_payload_bytes
from edge_dp import solve_edge

BASE_RESEARCH = '65030469c65545a0877740fed9c53ef2035766f2'
ALGORITHMS = ('deficit', 'v02', 'v02_default', 'mask_isolated',
              'edge_bitmask', 'edge_tuple', 'cubic')
SOURCES = ('modconvex.py', 'edge_dp.py', 'experiments/v03/deficit.py',
           'experiments/v03/baselines.py', 'experiments/v03/workloads_expanded.py',
           'experiments/v03/benchmark_expanded.py')
FROZEN = SOURCES[:4] + ('experiments/v03/benchmark.py',)


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT,
                                   stderr=subprocess.DEVNULL).decode().strip()


def provenance():
    hashes = {p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in SOURCES}
    # Mandatory preservation gate; an unchanged HEAD cannot conceal a dirty solver.
    for p in FROZEN:
        expected = subprocess.check_output(['git', 'show', f'{BASE_RESEARCH}:{p}'],
                                           cwd=ROOT, stderr=subprocess.DEVNULL)
        if (ROOT/p).read_bytes() != expected:
            raise ValueError(f'frozen source changed: {p}')
    return dict(working_commit=git('rev-parse', 'HEAD'),
                git_status=git('status', '--porcelain', '--untracked-files=normal'),
                file_sha256=hashes, frozen_source_gate='PASS',
                frozen_reference=BASE_RESEARCH)


def valid_witness(a, m, witness):
    """Separate predicate, using second differences rather than solver verify()."""
    return (isinstance(witness, (tuple, list)) and
            all(type(i) is int and 1 <= i <= len(a) for i in witness) and
            all(i < j for i, j in zip(witness, witness[1:])) and
            sum(witness) % m == 0 and
            all(a[i-1]+a[k-1] > 2*a[j-1]
                for i, j, k in zip(witness, witness[1:], witness[2:])))


def exhaustive_oracle(a, m):
    """All selected subsets, independent of complement/edge DP mechanisms."""
    answer = ()
    for bits in range(1 << len(a)):
        candidate = tuple(i+1 for i in range(len(a)) if bits & (1 << i))
        if valid_witness(a, m, candidate) and (
                len(candidate) > len(answer) or
                (len(candidate) == len(answer) and candidate < answer)):
            answer = candidate
    return answer


def superconvex_oracle(a, m):
    """Independent cardinality/lex index-sum DP for exactly A[i]=3**i.

    Every subsequence is convex: 3**k-3**j >= 2*3**j > 3**j-3**i.
    Iterate selected indices, no omission partitions or edge-difference states.
    """
    if a != [3**i for i in range(len(a))]:
        raise ValueError('analytic oracle domain mismatch')
    states = {0: ()}
    for i in range(1, len(a)+1):
        for total, prior in list(states.items()):
            candidate = prior+(i,)
            old = states.get(total+i)
            if old is None or len(candidate) > len(old) or (
                    len(candidate) == len(old) and candidate < old):
                states[total+i] = candidate
    candidates = [w for total, w in states.items() if total % m == 0]
    return min(candidates, key=lambda w: (-len(w), w))


def skip_reason(case, name):
    n, m, h = (case[k] for k in ('n', 'm', 'h'))
    U = n*(n+1)//2
    high = 2*m > U and m <= U
    if name in ('deficit', 'mask_isolated') and not high:
        return 'outside high-modulus domain'
    if name == 'mask_isolated' and min(n, h) > 12:
        return 'registered mask cap q>12'
    if name == 'cubic' and n > 8:
        return 'registered cubic cap n>8'
    if name == 'edge_tuple' and n > 24:
        return 'registered tuple cap n>24'
    if name == 'edge_bitmask' and n > 35:
        return 'registered edge cap n>35'
    if name in ('v02', 'v02_default') and (n > 35 or
            dense_dp_payload_bytes(n, m) > 8*1024*1024):
        return 'registered public-API cap n>35 or dense payload>8 MiB'
    return None


def call_algorithm(name, a, m):
    if name == 'deficit':
        out = solve_deficit(a, m)
        return out.status, out.indices, dict(operations=out.operations,
                                            nodes=out.nodes, partitions=out.candidates)
    if name in ('v02', 'v02_default'):
        out = solve(a, m, **({'complement_cutoff': 20} if name == 'v02' else {}))
        return out.status, out.indices, dict(operations=out.operations, reason=out.reason)
    functions = dict(mask_isolated=solve_mask, edge_bitmask=solve_edge,
                     edge_tuple=solve_edge_tuple, cubic=cubic_dp)
    return 'OPTIMAL', functions[name](a, m), {}


def worker(cfg):
    name, a, m = (cfg[k] for k in ('algorithm', 'a', 'm'))
    status, expected, counters = call_algorithm(name, a, m)
    if status != 'OPTIMAL':
        return dict(status='RESOURCE_LIMIT', solver_status=status, witness=expected)
    if not valid_witness(a, m, expected):
        raise ValueError('invalid warmup witness')
    timings = []
    for _ in range(cfg['repetitions']):
        begin = time.perf_counter_ns()
        status, witness, _ = call_algorithm(name, a, m)
        elapsed = time.perf_counter_ns()-begin
        if status != 'OPTIMAL' or witness != expected:
            raise ValueError('timed output drift')
        timings.append(elapsed)
    tracemalloc.start()
    try:
        status, witness, _ = call_algorithm(name, a, m)
        peak = tracemalloc.get_traced_memory()[1]
    finally:
        tracemalloc.stop()
    if status != 'OPTIMAL' or witness != expected:
        raise ValueError('instrumented output drift')
    median = statistics.median(timings)
    return dict(status='OK', witness=expected, runtime_ns=timings,
                median_ns=median, min_ns=min(timings), max_ns=max(timings),
                mad_ns=statistics.median(abs(t-median) for t in timings),
                traced_peak_bytes=peak, counters=counters,
                peak_rss_kib_linux=(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
                                    if resource is not None and sys.platform.startswith('linux')
                                    else None))


def run_cell(cfg, timeout):
    try:
        proc = subprocess.run([sys.executable, str(Path(__file__).resolve()), '--worker'],
                              input=json.dumps(cfg), capture_output=True, text=True,
                              encoding='utf-8', cwd=ROOT, timeout=timeout)
    except subprocess.TimeoutExpired:
        return dict(status='TIMEOUT', timeout_seconds=timeout,
                    reason='whole worker deadline: startup, warmup, timing and traced call')
    if proc.returncode:
        return dict(status='ERROR', returncode=proc.returncode, stderr=proc.stderr[-4000:])
    try:
        result = json.loads(proc.stdout)
        if result['status'] == 'OK':
            times = result['runtime_ns']
            if (len(times) != cfg['repetitions'] or not times or
                    any(type(t) is not int or t <= 0 for t in times) or
                    result['median_ns'] != statistics.median(times) or
                    not valid_witness(cfg['a'], cfg['m'], result['witness'])):
                raise ValueError('invalid worker measurement')
        elif result['status'] != 'RESOURCE_LIMIT':
            raise ValueError('unknown worker status')
        return result
    except (ValueError, KeyError, TypeError):
        return dict(status='ERROR', reason='malformed worker JSON', stdout=proc.stdout[-4000:])


def verify_rows(cases, rows, references):
    """Cross-check full witnesses, never merely lengths or first-result acceptance."""
    by_case = defaultdict(list)
    for row in rows:
        if row['status'] == 'OK':
            by_case[row['case_id']].append(row)
    for case in cases:
        cid = case['case_id']
        group = by_case[cid]
        ref = references[cid]
        witnesses = {tuple(r['witness']) for r in group}
        mismatch = len(witnesses) > 1 or (ref['witness'] is not None and
                   any(tuple(r['witness']) != tuple(ref['witness']) for r in group))
        independent = ref['kind'] != 'cross_algorithm_only'
        algorithms = {r['algorithm'] for r in group}
        level = ('independent_oracle' if independent else
                 'cross_algorithm_agreement' if len(algorithms) >= 2 else 'unverified')
        for row in group:
            row['verification'] = level
            if mismatch:
                row['status'] = 'MISMATCH'
            elif level == 'unverified':
                row['status'] = 'UNVERIFIED'


def summary(report):
    """Within-runner ratios only. Retain per-case losses and incomplete pairs."""
    cases = {c['case_id']: c for c in report['cases']}
    rows = report['rows']
    lookup = {(r['case_id'], r['algorithm'], r['block']): r for r in rows}
    pairs = []
    for cid, case in cases.items():
        for baseline in ALGORITHMS[1:]:
            ratios = []
            for block in range(report['blocks']):
                t1 = lookup.get((cid, 'deficit', block), {})
                other = lookup.get((cid, baseline, block), {})
                if (report.get('complete', False) and
                        t1.get('verification') in ('independent_oracle', 'cross_algorithm_agreement') and
                        other.get('verification') in ('independent_oracle', 'cross_algorithm_agreement') and
                        t1.get('status') == other.get('status') == 'OK'):
                    ratios.append(other['median_ns']/t1['median_ns'])
            pairs.append(dict(case_id=cid, cohort=case['cohort'], family=case['family'],
                              baseline=baseline, n=case['n'], h=case['h'],
                              paired_blocks=len(ratios), block_ratios=ratios,
                              median_ratio=statistics.median(ratios) if ratios else None,
                              complete=len(ratios) == report['blocks']))
    strata = defaultdict(list)
    for pair in pairs:
        strata[(pair['cohort'], pair['family'], pair['baseline'])].append(pair)
    groups = []
    for (cohort, family, baseline), group in sorted(strata.items()):
        ratios = [p['median_ratio'] for p in group if p['complete']]
        groups.append(dict(cohort=cohort, family=family, baseline=baseline,
                           planned_cases=len(group), complete_pairs=len(ratios),
                           faster=sum(r > 1 for r in ratios), slower=sum(r < 1 for r in ratios),
                           equal=sum(r == 1 for r in ratios),
                           median_ratio=statistics.median(ratios) if ratios else None,
                           min_ratio=min(ratios) if ratios else None,
                           max_ratio=max(ratios) if ratios else None))
    return dict(report_complete=report.get('complete', False),
                status_counts=dict(Counter(r['status'] for r in rows)),
                verification_counts=dict(Counter(r.get('verification') for r in rows
                                                if r['status'] == 'OK')),
                pairs=pairs, strata=groups)


def save(path, report):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix+'.tmp')
    temp.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    temp.replace(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--profile', choices=('smoke', 'ci', 'paper'), default='ci')
    parser.add_argument('--seed', type=int, default=20261023)
    parser.add_argument('--order-seed', type=int, default=713)
    parser.add_argument('--blocks', type=int, default=2)
    parser.add_argument('--repetitions', type=int, default=3)
    parser.add_argument('--timeout', type=float, default=60)
    parser.add_argument('--output', default='benchmark_m1_raw.json')
    parser.add_argument('--plan-only', action='store_true')
    parser.add_argument('--summarize', metavar='REPORT')
    parser.add_argument('--worker', action='store_true', help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.worker:
        print(json.dumps(worker(json.load(sys.stdin))))
        return 0
    if args.summarize:
        save(args.output, summary(json.loads(Path(args.summarize).read_text(encoding='utf-8'))))
        return 0
    if args.blocks < 1 or args.repetitions < 1 or not math.isfinite(args.timeout) or args.timeout <= 0:
        parser.error('blocks/repetitions must be positive integers; timeout must be positive and finite')
    cases = build_cases(args.profile, args.seed)
    plan = [dict(case_id=c['case_id'], algorithm=name, block=block,
                 skip_reason=skip_reason(c, name))
            for block in range(args.blocks) for c in cases for name in ALGORITHMS]
    random.Random(args.order_seed).shuffle(plan)
    report = dict(schema_version=1, milestone=VERSION, profile=args.profile,
                  seed=args.seed, order_seed=args.order_seed, blocks=args.blocks,
                  repetitions=args.repetitions, timeout_seconds=args.timeout,
                  created_utc=datetime.now(timezone.utc).isoformat(),
                  python=sys.version, platform=platform.platform(),
                  processor=platform.processor(), cpu_count=os.cpu_count(),
                  runner={k: os.environ.get(k) for k in
                          ('RUNNER_OS', 'RUNNER_ARCH', 'ImageOS', 'ImageVersion', 'GITHUB_RUN_ID')},
                  provenance=provenance(), cases=cases, plan=plan,
                  workload_sha256=canonical_hash(cases), plan_sha256=canonical_hash(plan),
                  references={}, rows=[], complete=False,
                  notes=['runtime includes reconstruction, excludes process startup; one warmup per block',
                         'tracemalloc is a separate call; process peak RSS includes imports and warmup',
                         'null RSS is unavailable; no hard RSS cap or infeasibility from timeout',
                         'ratios compare algorithms within one runner, not operating-system speed',
                         'blocks/repetitions are not independent workload samples; no significance claim',
                         'v02 uses cutoff 20 for historical parity; v02_default uses the public default 15',
                         'legacy_original and legacy_posthoc retain their historical evidence labels'])
    save(args.output, report)  # Freeze all inputs/omissions before any measurements.
    if args.plan_only:
        print(f'planned {len(cases)} cases, {len(plan)} cells: {args.output}')
        return 0
    for c in cases:
        if c['n'] <= 12:
            kind, witness = 'all_selected_subsets', exhaustive_oracle(c['a'], c['m'])
        elif c['family'] == 'superconvex':
            kind, witness = 'superconvex_index_sum_dp', superconvex_oracle(c['a'], c['m'])
        else:
            kind, witness = 'cross_algorithm_only', None
        report['references'][c['case_id']] = dict(kind=kind, witness=witness)
    by_id = {c['case_id']: c for c in cases}
    for i, job in enumerate(plan):
        c = by_id[job['case_id']]
        if job['skip_reason']:
            out = dict(status='SKIPPED', reason=job['skip_reason'])
        else:
            out = run_cell(dict(algorithm=job['algorithm'], a=c['a'], m=c['m'],
                                repetitions=args.repetitions), args.timeout)
        report['rows'].append(dict(out, case_id=c['case_id'], algorithm=job['algorithm'],
                                   block=job['block'], execution_index=i))
        # A failed/timed-out child cannot erase earlier measurements.
        save(args.output, report)
        if (i+1) % 50 == 0:
            print(f'{i+1}/{len(plan)} cells retained', flush=True)
    verify_rows(cases, report['rows'], report['references'])
    report['complete'] = True
    report['summary'] = summary(report)
    save(args.output, report)
    print(json.dumps(report['summary']['status_counts']), flush=True)
    statuses = {r['status'] for r in report['rows']}
    return 1 if statuses & {'ERROR', 'MISMATCH'} else (
        2 if statuses & {'TIMEOUT', 'RESOURCE_LIMIT', 'UNVERIFIED'} else 0)


if __name__ == '__main__':
    raise SystemExit(main())
