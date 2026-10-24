"""Versioned benchmark inputs only; no solver or production dispatch changes."""
import hashlib
import json
import random

VERSION = 'v03-benchmark-m1'
FAMILIES = (
    'uniform', 'sorted_uniform', 'permutation', 'random_walk', 'few_values',
    'sparse_outliers', 'piecewise_quadratic', 'arithmetic', 'convex', 'equal',
    'alternating', 'huge', 'superconvex', 'prefix_defect', 'suffix_defect',
)
LEGACY = (
    (12, 3, 'convex'), (12, 8, 'alternating'), (20, 7, 'convex'),
    (20, 12, 'alternating'), (20, 8, 'equal'), (20, 10, 'huge'),
    (35, 5, 'convex'), (35, 12, 'alternating'),
    (12, 8, 'superconvex'), (20, 12, 'superconvex'),
    (35, 12, 'superconvex'), (20, 24, 'superconvex'), (35, 40, 'superconvex'),
)


def canonical_hash(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True,
                                    separators=(',', ':')).encode()).hexdigest()


def values(n, family, seed):
    # Local content-derived RNG: changing case order never changes any input.
    rng = random.Random(int(canonical_hash([VERSION, n, family, seed]), 16))
    if family == 'uniform':
        return [rng.randrange(-n*n, n*n+1) for _ in range(n)]
    if family == 'sorted_uniform':
        return sorted(values(n, 'uniform', seed))
    if family == 'permutation':
        a = list(range(n))
        rng.shuffle(a)
        return a
    if family == 'random_walk':
        a, current = [], 0
        for _ in range(n):
            current += rng.randrange(-5, 6)
            a.append(current)
        return a
    if family == 'few_values':
        return [rng.choice((-2, 0, 2)) for _ in range(n)]
    if family == 'sparse_outliers':
        return [rng.choice((-1, 1))*10**6 if rng.randrange(5) == 0 else 0
                for _ in range(n)]
    if family == 'piecewise_quadratic':
        return [i*i if i < n//2 else -(i-n//2)**2 for i in range(n)]
    if family == 'arithmetic':
        return [3*i-7 for i in range(n)]
    if family == 'convex':
        return [i*i for i in range(n)]
    if family == 'equal':
        return [7]*n
    if family == 'alternating':
        return [(-1)**i*(i*i+1) for i in range(n)]
    if family == 'huge':
        return [(-1)**i*(10**120+i*i) for i in range(n)]
    if family in ('superconvex', 'prefix_defect', 'suffix_defect'):
        a = [3**i for i in range(n)]
        if family == 'prefix_defect':
            a[2] = -a[2]
        if family == 'suffix_defect':
            a[-2] = a[-1]
        return a
    raise ValueError(family)


def build_cases(profile='ci', seed=20261023):
    if profile not in ('smoke', 'ci', 'paper'):
        raise ValueError(profile)
    cases = []

    def add(n, m, family, sample, cohort):
        a = values(n, family, sample)
        identity = [cohort, n, m, family, sample]
        cases.append(dict(case_id=canonical_hash(identity)[:20], cohort=cohort,
                          n=n, m=m, h=n*(n+1)//2-m, family=family,
                          sample_seed=sample, a=a, input_sha256=canonical_hash([a, m])))

    if profile != 'smoke':
        for i, (n, h, family) in enumerate(LEGACY):
            add(n, n*(n+1)//2-h, family, seed,
                'legacy_original' if i < 8 else 'legacy_posthoc')
    # Same workload sample seeds on every runner; timing order uses a separate seed.
    samples = 1 if profile == 'smoke' else (2 if profile == 'ci' else 5)
    sizes = (8,) if profile == 'smoke' else (12, 24)
    for sample in range(seed, seed+samples):
        for n in sizes:
            for family in FAMILIES:
                if sample != seed and family not in FAMILIES[:6]:
                    continue  # deterministic controls are not independent samples
                add(n, n*(n+1)//2-min(12, n-1), family, sample, 'distribution')
    # Both sides of U/2 and m=U; T1 inapplicability is an explicit planned cell.
    for n in ((8,) if profile == 'smoke' else (8, 12)):
        U = n*(n+1)//2
        moduli = sorted({2, U//2, U//2+1, U-n-1, U-n, U-1, U, U+1})
        for m in moduli:
            for family in ('arithmetic', 'superconvex'):
                add(n, m, family, seed, 'modulus_boundary')
    if profile != 'smoke':
        for n in ((12, 24, 48) if profile == 'ci' else (12, 24, 48, 96)):
            U = n*(n+1)//2
            for h in (0, 1, 5, 12, 24, 40):
                if 2*(U-h) > U:
                    add(n, U-h, 'superconvex', seed, 'deficit_scaling')
    if len({c['case_id'] for c in cases}) != len(cases):
        raise AssertionError('duplicate case identity')
    return cases
