"""Independent G9 audit; standard library only. Run from any directory.

Original source is hash-checked. No existing test/oracle implementation is used.
Clean-room means separately written implementations after inspecting the target,
not blinded authorship or independent human replication.
"""
from __future__ import annotations
import ast
from collections import Counter
from functools import lru_cache
import hashlib
import importlib.util
from itertools import combinations, product
import json
from math import isqrt
from pathlib import Path
import platform
import random
import sys
import time
import tracemalloc

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE = ROOT / 'experiments/v03/g9_quadratic_lex.py'
PIN = '96ac7e2df040ed964bc36f0ad4e00d541b3f1f2d'
EXPECTED_BLOB = 'bcdbabc1cde45d357baa64fd78a693889258855b'


def load(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.solve_g9


def convex(a, s):
    # Direct second differences, indexed access, no target helpers.
    return all(a[s[k+2]-1] - 2*a[s[k+1]-1] + a[s[k]-1] > 0
               for k in range(len(s)-2))


@lru_cache(None)
def selected_candidates(n, m):
    # Enumerates ALL selected subsets; does not use deficit/complement rules.
    return tuple(s for k in range(1, n+1)
                 for s in combinations(range(1, n+1), k) if sum(s) % m == 0)


def feasible_selected(a, m):
    return [s for s in selected_candidates(len(a), m) if convex(a, s)]


def best(witnesses):
    return min(witnesses, key=lambda s: (-len(s), s), default=())


def constrained_brute(witnesses, q, x):
    omitted = set(q)
    required = set(range(1, x)) - omitted
    return max((len(s) for s in witnesses
                if not omitted.intersection(s) and required.issubset(s)), default=0)


def pair_sum_dp(a, m, q=(), x=1):
    """Clean-room DP: last TWO indices + exact SELECTED sum, full n.

    No edge sorting, deficit truncation, harmonic sparsity, or scalar sweep.
    Topological scan over the second endpoint; retain explicit best tuples.
    Deliberately slow test oracle, not part of the claimed resource bounds.
    """
    n = len(a)
    omit = set(q)
    required = set(range(1, x)) - omit
    table = {}
    candidates = []
    for j in range(1, n+1):
        if j in omit:
            continue
        singleton = (j,)
        if j % m == 0 and required.issubset(singleton):
            candidates.append(singleton)
        for i in range(1, j):
            if i in omit or any(t < j and t != i for t in required):
                continue
            table[(i, j, i+j)] = (i, j)
        # Newly created pairs ending at j and extensions from earlier endpoints.
        ending = [(key, s) for key, s in table.items() if key[1] == j]
        for (i, _, total), s in ending:
            if total % m == 0 and required.issubset(s):
                candidates.append(s)
            for k in range(j+1, n+1):
                if k in omit or any(j < t < k for t in required):
                    continue
                if a[k-1] - a[j-1] <= a[j-1] - a[i-1]:
                    continue
                key = (j, k, total+k)
                candidate = s + (k,)
                old = table.get(key)
                if old is None or (-len(candidate), candidate) < (-len(old), old):
                    table[key] = candidate
    return best(candidates)


@lru_cache(None)
def distinct_parts(total, lower=1):
    """Independent omission enumeration for larger planted instances."""
    if total == 0:
        return ((),)
    return tuple((i,) + rest for i in range(lower, total+1)
                 for rest in distinct_parts(total-i, i+1))


def partition_best(a, h):
    candidates = []
    for omission in distinct_parts(h):
        d = set(omission)
        s = tuple(i for i in range(1, len(a)+1) if i not in d)
        if convex(a, s):
            candidates.append(s)
    return best(candidates)


def exposed_oracle(source):
    """Instrument ONLY the return boundary, exposing the actual nested oracle.

    No mutation of oracle initialization/transitions/events. Returns zero on
    suffix rejection, exactly as the target's precheck requires.
    """
    tree = ast.parse(source)
    fn = next(node for node in tree.body if isinstance(node, ast.FunctionDef))
    for index, node in enumerate(fn.body):
        if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == 'optimum' for t in node.targets):
            fn.body[index:] = [ast.Return(value=ast.Name(id='max_length', ctx=ast.Load()))]
            break
    namespace = {}
    exec(compile(ast.fix_missing_locations(tree), '<exposed-g9>', 'exec'), namespace)
    def factory(a, m):
        result = namespace['solve_g9'](a, m)
        return result if callable(result) else lambda q, x: 0
    return factory


def measure_validation(fn, n):
    """Reset peak AFTER output exists: isolate assertion temporary storage."""
    a = [i*i for i in range(1, n+1)]
    samples = {}
    filename = fn.__code__.co_filename
    def trace(frame, event, arg):
        if frame.f_code is fn.__code__ and event == 'line':
            if 'selected' in frame.f_locals and 'baseline' not in samples:
                samples['baseline'] = tracemalloc.get_traced_memory()[0]
                tracemalloc.reset_peak()
        if frame.f_code is fn.__code__ and event == 'return' and 'baseline' in samples:
            samples['validation_peak_extra_bytes'] = (
                tracemalloc.get_traced_memory()[1] - samples['baseline'])
        return trace if frame.f_code.co_filename == filename else None
    tracemalloc.start()
    sys.settrace(trace)
    try:
        s = fn(a, n*(n+1)//2)
    finally:
        sys.settrace(None)
        tracemalloc.stop()
    assert len(s) == n
    return samples['validation_peak_extra_bytes']


def main():
    started = time.perf_counter()
    source = SOURCE.read_text()
    data = SOURCE.read_bytes()
    blob = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    assert blob == EXPECTED_BLOB, (blob, EXPECTED_BLOB)
    original = load(SOURCE)
    corrected = load(HERE / 'solver_corrected.py')
    factory = exposed_oracle(source)
    mutation_sources = {
        'forbidden_endpoints_removed': source.replace('not forbidden[i] and ', '').replace(
            'forbidden[i] or forbidden[j] or\n                    ', ''),
        'required_gap_check_removed': source.replace(
            'required[j-1] != required[i]', 'False'),
        'required_start_check_removed': source.replace(
            ' and required[i-1] == 0', ''),
        'one_compulsory_anchor_only': source.replace('p = min(n, h+2)', 'p = min(n, h+1)'),
    }
    mutation_factories = {name: exposed_oracle(s) for name, s in mutation_sources.items()}
    mutation_counterexamples = {}
    report = dict(pin=PIN, source_git_blob=blob, seed=2026102415,
                  python=sys.version, platform=platform.platform(),
                  counts={}, findings={}, stages=[])
    counts = Counter()
    histogram = Counter()
    def stage(name):
        report['stages'].append(dict(name=name, elapsed_seconds=time.perf_counter()-started))
        print(name, dict(counts), flush=True)
    def check(a, h, expected, pair=False):
        m = len(a)*(len(a)+1)//2-h
        counters = {}
        got = original(a, m, counters=counters)
        assert got == expected, ('original', a, m, got, expected)
        assert corrected(a, m) == expected, ('corrected', a, m, expected)
        if pair:
            assert pair_sum_dp(a, m) == expected, ('pair', a, m, expected)
            counts['pair_full_witness'] += 1
        histogram[len(a)-len(expected) if expected else 'infeasible'] += 1
        if counters:
            t = len(a)-len(expected)
            assert t*(t+1)//2 <= h
            # ceil(log2(h+1)) == h.bit_length().
            assert counters['queries'] <= 1+t*(1+h.bit_length())
            assert counters['relaxations'] <= counters['queries']*counters['events']*(h+1)
            counts['counter_bound_checks'] += 1
    # New alphabet, all valid high-modulus deficits, both implementations.
    for n in range(2, 9):
        for a in product((-3, 0, 5), repeat=n):
            for h in range(n):
                m = n*(n+1)//2-h
                if m < 2 or 2*m <= n*(n+1)//2:
                    continue
                check(a, h, best(feasible_selected(a, m)))
                counts['exhaustive_selected_subset'] += 1
    stage('exhaustive selected subsets complete')
    rng = random.Random(report['seed'])
    first_tie = None
    for trial in range(6000):
        n = rng.randrange(3, 13)
        h = rng.randrange(n)
        mode = trial % 6
        if mode == 0:
            a = [rng.randrange(-20, 21) for _ in range(n)]
        elif mode == 1:
            a = [i*i+rng.randrange(-6, 7) for i in range(n)]
        elif mode == 2:
            a = [rng.choice((-1, 0, 1))*10**120+rng.randrange(-3, 4) for _ in range(n)]
        elif mode == 3:
            a = [0]*n
            for i in range(1, n):
                a[i] = a[i-1] + rng.randrange(-5, 6)
        elif mode == 4:
            d = rng.choice(distinct_parts(h))
            a = [0]*n
            rank = 0
            for i in range(1, n+1):
                if i in d:
                    a[i-1] = rng.randrange(-100, 101)
                else:
                    a[i-1] = rank*rank*17 - rank*10**60
                    rank += 1
        else:
            a = [i*10**120+i*i for i in range(n)]
        m = n*(n+1)//2-h
        witnesses = feasible_selected(a, m)
        expected = best(witnesses)
        check(a, h, expected, pair=trial < 1800)
        counts['random_selected_subset'] += 1
        if expected:
            tied = sorted(s for s in witnesses if len(s) == len(expected))
            if len(tied) > 1:
                counts['nontrivial_optimal_ties'] += 1
                if first_tie is None:
                    first_tie = dict(a=a, m=m, witnesses=tied)
        # Query arbitrary omission sets and every threshold, not only successful
        # search prefixes. Independently compare the nested scalar oracle.
        if trial < 1500:
            oracle = factory(a, m)
            mutant_oracles = {name: f(a, m) for name, f in mutation_factories.items()
                              if name not in mutation_counterexamples}
            qs = [(), tuple(i for i in range(1, h+1) if rng.randrange(3) == 0)]
            if expected:
                omissions = tuple(i for i in range(1, n+1) if i not in expected)
                qs.extend(omissions[:k] for k in range(len(omissions)+1))
            for q in set(qs):
                previous_score = n+1
                for x in range(1, h+2):
                    want = constrained_brute(witnesses, q, x)
                    got = oracle(q, x)
                    assert got == want, ('forced oracle', a, m, q, x, got, want)
                    assert got <= previous_score, ('monotonicity', a, m, q, x)
                    previous_score = got
                    counts['forced_scalar_queries'] += 1
                    for name, mo in mutant_oracles.items():
                        if name not in mutation_counterexamples:
                            wrong = mo(q, x)
                            if wrong != want:
                                mutation_counterexamples[name] = dict(
                                    a=a, m=m, q=q, x=x, expected=want, mutant=wrong)
                    if trial < 180:
                        assert len(pair_sum_dp(a, m, q, x)) == want
                        counts['forced_pair_queries'] += 1
    report['findings']['first_nontrivial_tie'] = first_tie
    report['findings']['mutation_counterexamples'] = mutation_counterexamples
    assert len(mutation_counterexamples) == len(mutation_factories), mutation_counterexamples
    # Edge list compared with direct gap sums and mandatory-index membership.
    for h in range(201):
        n = h+3
        a = [i*i for i in range(n)]
        oracle = factory(a, n*(n+1)//2-h)
        closure = dict(zip(oracle.__code__.co_freevars,
                           (c.cell_contents for c in oracle.__closure__)))
        events = closure['events']
        p = min(n, h+2)
        expected_edges = set()
        for i in range(1, p):
            for j in range(i+1, p+1):
                gap = tuple(range(i+1, j))
                if sum(gap) <= h and all(k <= h for k in gap):
                    expected_edges.add((i, j, sum(gap)))
        assert {(e[2],e[3],e[4]) for e in events} == expected_edges
        assert len(events) <= p-1+sum(h//u for u in range(1,isqrt(2*h)+1))
        counts['event_set_and_harmonic_checks'] += 1
    stage('random, pair-state and constrained-oracle checks complete')
    for trial in range(450):
        h = rng.randrange(0, 35)
        n = rng.randrange(max(h+1, 3), max(h+1, 3)+60)
        d = rng.choice(distinct_parts(h))
        a = []
        rank = 0
        for i in range(1, n+1):
            if i in d:
                a.append(rng.randrange(-10000, 10001))
            else:
                a.append(rank*rank + rank*10**80)
                rank += 1
        check(a, h, partition_best(a, h))
        counts['planted_partition_witnesses'] += 1
    # Force all first t entries omitted: the last such entry, if selected,
    # would jump by >n^2 into a nonnegative suffix, whose next jump is <n^2.
    stress = []
    for t in (1, 2, 4, 8, 12, 16):
        h = t*(t+1)//2
        n = h+3
        a = [-10*n*n]*t + [i*i for i in range(t+1, n+1)]
        expected = tuple(range(t+1, n+1))
        check(a, h, expected)
        counters = {}
        original(a, n*(n+1)//2-h, counters=counters)
        stress.append(dict(n=n, h=h, **counters))
    report['stress_counters'] = stress
    # Three-way optimum ties after k forced initial omissions, exercising ties
    # beyond the first omission and large signed affine value transformations.
    tie_families = []
    for k in range(6):
        w = k*(k+1)//2
        h = w+2*(k+3)+2
        n = h+2
        a = [-3**(n+3)]*k + [0]*3 + [3**i for i in range(k+4,n+1)]
        d = tuple(range(1,k+1)) + (k+3, h-w-k-3)
        expected = tuple(i for i in range(1,n+1) if i not in d)
        assert partition_best(a, h) == expected
        for scale, offset in ((1,0),(7,-10**120),(10**100,10**130)):
            transformed = [scale*v+offset for v in a]
            check(transformed, h, expected)
            counts['constructed_deep_lex_ties'] += 1
        tie_families.append(dict(n=n, h=h, shared_omission_prefix=list(range(1,k+1)),
                                 canonical_omissions=d))
    report['constructed_tie_families'] = tie_families
    stage('planted and maximal-omission families complete')
    # Actual source mutation: reverse equal-difference order, remove final
    # assertions so a wrong witness is observable rather than an assert error.
    mutant_src = source.replace('(a[j-1]-a[i-1], -j, i, j, gap)',
                                '(a[j-1]-a[i-1], j, i, j, gap)')
    namespace = {}
    exec(compile(mutant_src, '<ascending-destination-mutant>', 'exec', optimize=1), namespace)
    mutant = namespace['solve_g9']
    a = [0, 0, 0, 0]
    assert original(a, 8) == () and mutant(a, 8) == (1, 3, 4)
    report['findings']['equal_difference_mutant'] = dict(a=a, m=8, correct=[], mutant=[1,3,4])
    # Searching equality is not monotone: synthetic fixed-cardinality family.
    # Also seek an ACTUAL feasible MOCOSO family with a hole in next omissions.
    gap_example = None
    for trial in range(10000):
        n, h = 10, 9
        a = [i*i+rng.randrange(-20, 21) for i in range(n)]
        w = feasible_selected(a, 55-h)
        target = best(w)
        if not target:
            continue
        opts = [s for s in w if len(s) == len(target)]
        ds = [tuple(i for i in range(1,n+1) if i not in s) for s in opts]
        if not ds or not ds[0]:
            continue
        positions = sorted(set(d[0] for d in ds))
        if len(positions)>1 and positions != list(range(positions[0], positions[-1]+1)):
            gap_example = dict(a=a, m=46, optimum=len(target),
                               first_omissions=positions, omissions=ds)
            break
    report['findings']['noncontiguous_first_omission_search'] = dict(
        trials=trial+1, found=gap_example)
    a = [3**i for i in range(7)]
    opts = feasible_selected(a, 22)
    target = best(opts)
    omissions = [tuple(i for i in range(1,8) if i not in s)
                 for s in opts if len(s) == len(target)]
    equality = [any(d[0] == x for d in omissions) for x in range(1,8)]
    threshold = [any(d[0] >= x for d in omissions) for x in range(1,8)]
    assert equality == [False]*5+[True,False]
    assert threshold == [True]*6+[False]
    report['findings']['nonmonotone_equality_example'] = dict(
        a=a, m=22, omissions=omissions, equality=equality, threshold=threshold)
    report['memory_validation'] = [dict(n=n, h=0,
        original_extra_bytes=measure_validation(original, n),
        corrected_extra_bytes=measure_validation(corrected, n))
        for n in (1000, 10000, 100000)]
    for row in report['memory_validation']:
        assert row['original_extra_bytes'] > 8*row['n']
        assert row['corrected_extra_bytes'] < 16384
    stage('mutants and fixed-deficit memory regression complete')
    report['counts'] = dict(counts)
    report['omission_histogram'] = {str(k):v for k,v in histogram.items()}
    report['elapsed_seconds'] = time.perf_counter()-started
    report['status'] = 'PASS: exactness checks; pinned auxiliary-space claim REFUTED'
    report['files_sha256'] = {p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                              for p in (SOURCE, Path(__file__), HERE/'solver_corrected.py')}
    (HERE/'results.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2), flush=True)


if __name__ == '__main__':
    main()
