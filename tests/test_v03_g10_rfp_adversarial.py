"""RFP adversarial G10 audit: inner oracle, mutation, and sparse variant.

Complete small-subset enumeration is independent of any DP implementation.
The instrumented inner routine is still the real G10 routine; it is inspected
at source level and no implementation or historical artifact is modified.
"""
from itertools import product
from random import Random
import inspect
import unittest

from experiments.v03.g10_direct_next import solve_g10
from experiments.v03.g10_sparse_experimental import solve_g10_sparse


def brute_full(a, m, Q=(), first_allowed=1):
    n = len(a)
    p = min(n, n * (n + 1) // 2 - m + 2)
    forbidden = set(Q)
    winner = (0, p + 1)
    for mask in range(1, 1 << n):
        S = tuple(i+1 for i in range(n) if mask >> i & 1)
        if sum(S) % m:
            continue
        selected = set(S)
        if forbidden & selected:
            continue
        if any(i not in selected for i in range(1, first_allowed)
               if i not in forbidden):
            continue
        if any(a[i-1] + a[k-1] <= 2*a[j-1]
               for i, j, k in zip(S, S[1:], S[2:])):
            continue
        remaining = set(range(1, n+1)) - selected - forbidden
        z = min(remaining, default=p+1)
        winner = max(winner, (len(S), z))
    return winner


def inner_g10(change_tie=False):
    source = inspect.getsource(solve_g10)
    anchor = "    optimum,first=best_next((),1)\n"
    if source.count(anchor) != 1:
        raise AssertionError("G10 instrumentation anchor changed")
    if change_tie:
        tie = "nxt>dst_next[r+g]"
        if source.count(tie) != 1:
            raise AssertionError("G10 tie guard changed")
        source = source.replace(tie, "nxt<dst_next[r+g]", 1)
    source = source.replace(anchor, "    return best_next\n", 1)
    namespace = dict(solve_g10.__globals__)
    exec(compile(source, "<auditor-instrumented-G10>", "exec"), namespace)
    return namespace["solve_g10"]


class G10Adversarial(unittest.TestCase):
    def test_internal_constrained_oracle_4500(self):
        rng = Random(261026)
        actual_probe = inner_g10()
        active, feasible = 0, 0
        for case in range(4500):
            n = rng.randint(2, 10)
            U = n * (n + 1) // 2
            h = rng.randrange(n)
            m = U - h
            selector = case % 4
            if selector == 0:
                a = tuple(1000*i*i + rng.randint(-i, i)
                          for i in range(n))
            elif selector == 1:
                a = tuple(4**i for i in range(n))
            elif selector == 2:
                alphabet = (-10**36, -2, 0, 1, 3, 10**36)
                a = tuple(rng.choice(alphabet) for _ in range(n))
            else:
                prefix = [rng.choice((-10**36, -2, 0, 1, 3, 10**36))
                          for _ in range(n)]
                for i in range(h+2, n):
                    prefix[i] = (2*prefix[i-1] - prefix[i-2]
                                 + abs(prefix[i-1] - prefix[i-2]) + 1)
                a = tuple(prefix)
            k = rng.randrange(min(h, 3) + 1)
            Q = tuple(sorted(rng.sample(range(1, h+1), k))) if k else ()
            threshold = rng.randint(Q[-1]+1 if Q else 1, h+1)
            oracle = brute_full(a, m, Q, threshold)
            instrument = actual_probe(a, m)
            if callable(instrument):
                active += 1
                observed = instrument(Q, threshold)
            else:
                observed = (0, min(n, h+2)+1)
            if observed[0]:
                feasible += 1
            self.assertEqual(oracle, observed,
                             (case, n, h, Q, threshold, a))
        self.assertGreaterEqual(active, 3500)
        self.assertGreaterEqual(feasible, 1200)

    def test_mutation_is_caught_by_complete_lex_witness(self):
        # Concrete falsifier: flipping only the equal-cardinality tie direction
        # leaves a valid max-cardinality witness but loses canonical order.
        a = (0, 0, -2, -2, -2, 0)
        m = 16
        self.assertEqual(solve_g10(a, m), (1, 4, 5, 6))
        source = inspect.getsource(solve_g10)
        assert source.count("nxt>dst_next[r+g]") == 1
        scope = dict(solve_g10.__globals__)
        exec(compile(source.replace("nxt>dst_next[r+g]",
                                    "nxt<dst_next[r+g]", 1),
                     "<tie-mutation>", "exec"), scope)
        mutant = scope["solve_g10"]
        self.assertNotEqual(mutant(a, m), solve_g10(a, m))
        self.assertEqual(mutant(a, m), (2, 3, 5, 6))

    def test_sparse_against_independent_selected_subset_oracle(self):
        count = 0
        for n in range(2, 8):
            U = n * (n + 1) // 2
            for a in product((-2, 0, 3), repeat=n):
                for h in range(n):
                    m = U - h
                    if m < 2 or 2*m <= U:
                        continue
                    expected = brute_full(a, m)[0]
                    actual = solve_g10_sparse(a, m)
                    exact = solve_g10(a, m)
                    self.assertEqual(actual, exact, (n, h, a))
                    self.assertEqual(len(actual), expected, (n, h, a))
                    count += 1
        self.assertEqual(count, 21321)

    def test_sparse_signed_and_max_omissions(self):
        rng = Random(20261026)
        for trial in range(2500):
            n = rng.randint(2, 15)
            U = n * (n+1)//2
            h = rng.randrange(n)
            a = tuple(rng.choice((-10**80, -7, -2, 0, 1, 3, 10**80))
                      for _ in range(n))
            self.assertEqual(solve_g10_sparse(a, U-h), solve_g10(a, U-h),
                             (trial, n, h))
        for k in (1, 2, 3, 5, 7, 9, 11):
            h = k*(k+1)//2
            n = h + 15
            a = tuple([-10**200]*k + [4**i for i in range(k, n)])
            counters = {}
            result = solve_g10_sparse(a, n*(n+1)//2-h, counters=counters)
            self.assertEqual(result, tuple(range(k+1, n+1)))
            self.assertEqual(counters["omissions"], k)
            self.assertEqual(counters["queries"], k)

    def test_input_edges(self):
        self.assertEqual(solve_g10_sparse((0, 1, 2), 6), ())
        self.assertEqual(solve_g10_sparse((-3,-3,-3,-3,-2,0),16),
                         (1,4,5,6))
        for n in (2, 3, 10000):
            a = tuple(i*i for i in range(n))
            self.assertEqual(solve_g10_sparse(a, n*(n+1)//2),
                             tuple(range(1,n+1)))
        for a,m in (((0,True,3),6), ((0,1,3),True),
                    ((0,1,3,5,10,20,40,80),24)):
            with self.assertRaises(ValueError):
                solve_g10_sparse(a,m)


if __name__ == "__main__":
    unittest.main()
