"""Reproducible old-vs-new comparative timings and traced-heap measurements.

Run: python benchmarks/compare_v02.py baseline_original/modconvex.py modconvex.py
Timings are descriptive, not asymptotic proofs or controlled speed claims.
"""
import gc
import importlib.util
import json
from pathlib import Path
import statistics
import sys
import time
import tracemalloc


def import_source(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def sample(solver, a, m):
    times = []
    peaks = []
    sol = None
    for _ in range(3):
        gc.collect()
        tracemalloc.start()
        started = time.perf_counter()
        result = solver(a, m)
        duration = time.perf_counter() - started
        peak = tracemalloc.get_traced_memory()[1]
        tracemalloc.stop()
        assert result.status == 'OPTIMAL'
        times.append(duration)
        peaks.append(peak)
        if sol is not None:
            assert result.indices == sol
        sol = result.indices
    return {'median_instrumented_s': statistics.median(times),
            'median_traced_peak_bytes': statistics.median(peaks),
            'times_s': times, 'peaks_bytes': peaks, 'indices': sol}


def main():
    if len(sys.argv) != 3:
        raise SystemExit('usage: python benchmarks/compare_v02.py OLD.py NEW.py')
    old = import_source('mocoso_pre_v02', Path(sys.argv[1]).resolve())
    new = import_source('mocoso_current_v02', Path(sys.argv[2]).resolve())
    cases = [(50, 20, 'convex'), (100, 30, 'convex'),
             (100, 2, 'convex'), (80, 30, 'alternating'),
             (50, 1265, 'complement')]
    data = []
    for n, m, kind in cases:
        a = ([i*i for i in range(n)] if kind != 'alternating'
             else [(-1)**i * (i*i+1) for i in range(n)])
        if kind == 'complement':
            # Valid modulus for n=50, with deficit h=10.
            m = n*(n+1)//2 - 10
        left = sample(old.solve, a, m)
        right = sample(new.solve, a, m)
        assert left.pop('indices') == right.pop('indices')
        slots = n*(n-1)//2*m
        row = {'n': n, 'm': m, 'family': kind,
               'old_dense_array_payload_bytes': 8*slots,
               'new_dense_array_payload_bytes': new.dense_dp_payload_bytes(n,m),
               'baseline': left, 'candidate': right}
        data.append(row)
        print(json.dumps(row, sort_keys=True), flush=True)
    output = {'baseline_file': sys.argv[1], 'candidate_file': sys.argv[2],
              'cases': data, 'python': sys.version}
    target = Path('v02_comparison.json')
    target.write_text(json.dumps(output, indent=2) + '\n', encoding='utf-8')
    print('COMPARISON PASS:', str(target), flush=True)


if __name__ == '__main__':
    main()
