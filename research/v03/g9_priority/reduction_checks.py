"""Independent experiments for the prior-art implication audit.

No imports from any MOCOSO solver. This is research evidence, not production code.
The batch sweep deliberately uses simultaneous equal-difference updates instead
of G9's descending-destination scheduling. Tests do not establish priority.
Run: python research/v03/g9_priority/reduction_checks.py
"""
from collections import deque
from itertools import combinations, groupby, product
import hashlib
import json
from pathlib import Path
import random


def canonical_inclusion(n, k, includes):
    """Lexicographically greatest increasing k-tuple in a uniform family.

    Assumes the family is nonempty. Does not ask a forced-inclusion query.
    """
    chosen = []
    previous = 0
    queries = 0
    for _ in range(k):
        lo, hi = previous + 1, n + 1
        while hi - lo > 1:
            mid = (lo + hi) // 2
            queries += 1
            if includes(set(chosen) | set(range(mid, n + 1))):
                lo = mid
            else:
                hi = mid
        chosen.append(lo)
        previous = lo
    return tuple(chosen), queries


def bkk_fifo(order, family):
    """Independent transcription of deterministic Algorithm 1, BKK v1.

    List order specifies one allowed choice of balanced partitions. The paper
    permits arbitrary balanced partitions and promises a witness, not this lex
    objective. This implementation is used only to test that distinction.
    """
    universe = set(order)
    queue = deque([list(order)])
    witness = set()
    while queue:
        part = queue.popleft()
        if len(part) == 1:
            witness.update(part)
            continue
        cut = len(part) // 2
        left, right = part[:cut], part[cut:]
        if any(set(w) <= universe - set(left) for w in family):
            universe.difference_update(left)
            queue.append(right)
        elif any(set(w) <= universe - set(right) for w in family):
            universe.difference_update(right)
            queue.append(left)
        else:
            queue.extend((left, right))
    return tuple(sorted(witness))


def make_score(a, h):
    """Exact score with arbitrary forced-selected indices, via batched events.

    Constructs the small core once. This intentionally simple experiment
    enumerates all core pairs; it does not claim optimal event construction time.
    """
    n = len(a)
    p = min(n, h + 2)
    if any(a[j] - a[j-1] <= a[j-1] - a[j-2]
           for j in range(h + 2, n)):
        return lambda required: 0
    events = []
    for i in range(1, p + 1):
        for j in range(i + 1, p + 1):
            if any(v > h for v in range(i + 1, j)):
                continue
            gap = sum(range(i + 1, j))
            if gap <= h:
                events.append((a[j-1] - a[i-1], i, j, gap))
    events.sort()
    groups = [list(g) for _, g in groupby(events, key=lambda e: e[0])]

    def score(required):
        counts = [0]
        for j in range(1, p + 1):
            counts.append(counts[-1] + (j in required))
        table = [[-1] * (h + 1) for _ in range(p + 1)]
        for i in range(1, p + 1):
            initial = i * (i - 1) // 2
            if initial <= h and counts[i-1] == 0:
                table[i][initial] = 1
        for group in groups:
            # A single p-by-H scratch array per group, not an event history.
            pending = [[-1] * (h + 1) for _ in range(p + 1)]
            for _, i, j, gap in group:
                if counts[j-1] != counts[i]:
                    continue
                for r in range(h - gap + 1):
                    if table[i][r] >= 1:
                        pending[j][r+gap] = max(pending[j][r+gap],
                                                table[i][r] + 1)
            for j in range(1, p + 1):
                for r in range(h + 1):
                    table[j][r] = max(table[j][r], pending[j][r])
        return table[p][h] + n - p if table[p][h] >= 1 else 0
    return score


def all_feasible(a, h):
    """Direct enumeration of selected tuples and modular feasibility."""
    n = len(a)
    m = n * (n + 1) // 2 - h
    result = []
    for bits in range(1, 1 << n):
        s = tuple(i + 1 for i in range(n) if bits >> i & 1)
        if sum(s) % m:
            continue
        if all(a[z-1] - a[y-1] > a[y-1] - a[x-1]
               for x, y, z in zip(s, s[1:], s[2:])):
            result.append(s)
    return result


def main():
    rng = random.Random(20261024)
    counts = dict(exhaustive_uniform_families=0, random_uniform_families=0,
                  mocoso_instances=0, constrained_scores=0,
                  feasible_instances=0, tied_optimum_instances=0,
                  canonical_queries=0)
    first_fifo_failure = None
    for n in range(1, 6):
        for k in range(n + 1):
            candidates = list(combinations(range(1, n + 1), k))
            for mask in range(1, 1 << len(candidates)):
                family = [s for j, s in enumerate(candidates) if mask >> j & 1]
                includes = lambda y: any(set(w) <= y for w in family)
                got, queries = canonical_inclusion(n, k, includes)
                assert got == max(family), (n, family, got)
                assert queries <= k * n.bit_length()
                if k:
                    arbitrary = bkk_fifo(list(range(1, n + 1)), family)
                    assert arbitrary in family
                    if arbitrary != max(family) and first_fifo_failure is None:
                        first_fifo_failure = dict(n=n, family=family,
                                                  returned=arbitrary,
                                                  canonical=max(family))
                counts['exhaustive_uniform_families'] += 1
    for _ in range(3000):
        n = rng.randrange(6, 16)
        k = rng.randrange(n + 1)
        family = list({tuple(sorted(rng.sample(range(1, n + 1), k)))
                       for _ in range(rng.randrange(1, 40))})
        got, queries = canonical_inclusion(n, k,
                            lambda y: any(set(w) <= y for w in family))
        assert got == max(family)
        assert queries <= k * n.bit_length()
        counts['random_uniform_families'] += 1

    cases = []
    for n in range(2, 7):
        for a in product((-2, 0, 3), repeat=n):
            for h in range(n):
                if n * (n + 1) // 2 - h >= 2:
                    cases.append((a, h))
    for _ in range(1600):
        n = rng.randrange(3, 12)
        h = rng.randrange(n)
        mode = rng.randrange(3)
        if mode == 0:
            a = tuple(rng.randrange(-20, 21) for _ in range(n))
        elif mode == 1:
            a = tuple(i*i + rng.randrange(-3, 4) for i in range(n))
        else:
            a = tuple(i*i if rng.random() < .8 else rng.randrange(-10, 11)
                      for i in range(n))
        cases.append((a, h))
    for a, h in cases:
        n = len(a)
        feasible = all_feasible(a, h)
        expected = min(feasible, key=lambda s: (-len(s), s)) if feasible else ()
        score = make_score(a, h)
        optimum = score(set())
        assert optimum == len(expected), (a, h, optimum, expected)
        for _ in range(4):
            required = {i for i in range(1, h+1) if rng.randrange(2)}
            want = max((len(s) for s in feasible if required <= set(s)), default=0)
            assert score(required) == want, (a, h, required, want)
            counts['constrained_scores'] += 1
        if optimum:
            omissions, queries = canonical_inclusion(h, n-optimum,
                lambda y: score(set(range(1, h+1)) - y) == optimum)
            got = tuple(i for i in range(1, n+1) if i not in omissions)
            assert got == expected, (a, h, got, expected)
            counts['feasible_instances'] += 1
            counts['canonical_queries'] += queries
            counts['tied_optimum_instances'] += sum(len(s) == optimum for s in feasible) > 1
        counts['mocoso_instances'] += 1

    family = [(1, 4), (2, 3)]
    noncanonical = bkk_fifo([2, 3, 1, 4, 5], family)
    assert noncanonical == (1, 4) and max(family) == (2, 3)
    result = dict(status='PASS', seed=20261024, counts=counts,
        same_weight_bkk_counterexample=dict(universe=list(range(1, 6)),
            family=family, partition_order=[2, 3, 1, 4, 5],
            returned=noncanonical, lexicographic_maximum=max(family)),
        contiguous_fifo_counterexample=first_fifo_failure,
        script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        limitation='Finite checks support the reduction; they prove neither priority nor asymptotics.')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
