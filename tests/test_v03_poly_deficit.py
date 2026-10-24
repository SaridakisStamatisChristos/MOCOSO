"""G3 independent adversarial check of the polynomial-deficit research solver.

Exact reference uses all 2**n SELECTED subsets, never a gap-weight DP.
The original T1 enumerator is a secondary differential control only.
"""
import itertools
import random
import unittest

from experiments.v03.poly_deficit import solve_poly_deficit
from experiments.v03.deficit import solve_deficit
from modconvex import solve as v02_solve


def direct_oracle(a, m):
    n = len(a)
    best = ()
    for mask in range(1 << n):
        seq = tuple(j + 1 for j in range(n) if (mask >> j) & 1)
        if sum(seq) % m != 0:
            continue
        if any(a[i - 1] + a[k - 1] <= 2 * a[j - 1]
               for i, j, k in zip(seq, seq[1:], seq[2:])):
            continue
        if len(seq) > len(best) or (len(seq) == len(best) and seq < best):
            best = seq
    return best


def valid(a, m, witness):
    return (sum(witness) % m == 0 and all(
        a[k-1] + a[i-1] > 2*a[j-1]
        for i, j, k in zip(witness, witness[1:], witness[2:])
    ))


def superconvex_residue_dp(n, m):
    # Independent exact tuple DP for any subsequence of powers 3**i,
    # which is strictly convex for EVERY selected triple.
    rows = {0: ()}
    for i in range(1, n + 1):
        nxt = rows.copy()
        for r, old in rows.items():
            key = (r + i) % m
            alt = old + (i,)
            current = nxt.get(key)
            if (current is None or len(alt) > len(current)
                    or (len(alt) == len(current) and alt < current)):
                nxt[key] = alt
        rows = nxt
    return rows.get(0, ())


class PolyG3(unittest.TestCase):
    def test_exhaustive_cartesian_values_moduli(self):
        count = 0
        for n in range(2, 8):
            U = n * (n + 1) // 2
            for a in itertools.product((-1, 0, 1), repeat=n):
                for m in range(U // 2 + 1, U + 1):
                    expected = direct_oracle(a, m)
                    got = solve_poly_deficit(a, m)
                    self.assertEqual(
                        (got.status, got.indices, got.length, got.upper_bound),
                        ("OPTIMAL", expected, len(expected), len(expected)),
                        (n, a, m),
                    )
                    count += 1
                    if count % 151 == 0:
                        self.assertEqual(solve_deficit(a, m).indices, expected)
                        self.assertEqual(v02_solve(a, m).indices, expected)
                        for K in (-1, 0, 1, len(expected), len(expected) + 1, n + 1):
                            r = solve_poly_deficit(a, m, K=K)
                            self.assertEqual(
                                r.status,
                                "FEASIBLE" if K <= len(expected) else "INFEASIBLE",
                                (a, m, K),
                            )
                            self.assertEqual(r.indices, expected if K > 0 and K <= n
                                             else (), (a, m, K))
                            self.assertTrue(valid(a, m, r.indices))
        self.assertEqual(count, 41085)

    def test_seeded_huge_signed_and_budget(self):
        rng = random.Random(20261024)
        for trial in range(850):
            n = rng.randrange(2, 12)
            a = [rng.choice((-10**150, -100000, -1, 0, 0, 1,
                             10**5, 10**150)) for _ in range(n)]
            U = n * (n + 1) // 2
            m = rng.randrange(U // 2 + 1, U + 1)
            expected = direct_oracle(a, m)
            r = solve_poly_deficit(a, m)
            self.assertEqual(r.indices, expected, (n, a, m))
            self.assertTrue(valid(a, m, r.indices))
            if trial % 10 == 0:
                self.assertEqual(solve_deficit(a, m).indices, expected)
                for K in (0, 1, 2, len(expected), len(expected)+1):
                    t = solve_poly_deficit(a, m, K=K)
                    self.assertEqual(t.status,
                                     "FEASIBLE" if K <= len(expected) else
                                     "INFEASIBLE")
                    self.assertGreaterEqual(t.upper_bound, len(expected))
                    self.assertLessEqual(t.lower_bound, len(expected))
                for cap in (0, 1, 10):
                    t = solve_poly_deficit(a, m, max_state_cells=cap)
                    self.assertTrue(valid(a, m, t.indices))
                    self.assertGreaterEqual(t.upper_bound, len(expected))
                    self.assertLessEqual(t.lower_bound, len(expected))
                    self.assertNotEqual(t.status, "INFEASIBLE")

    def test_positive_large_n_independent_residue_dp(self):
        # The fastest experimental cases must not all have empty optimum.
        cases = [(2, 0), (2, 1), (12, 0), (20, 4), (25, 16),
                 (35, 25), (50, 38), (65, 45), (90, 60),
                 (500, 3), (1000, 4)]
        for n, h in cases:
            U = n * (n + 1) // 2
            m = U - h
            a = [3**i for i in range(n)]
            reference = superconvex_residue_dp(n, m) if n <= 90 else (
                tuple(i for i in range(1, n + 1) if i != h)
            )
            got = solve_poly_deficit(a, m)
            self.assertEqual(got.status, "OPTIMAL")
            self.assertEqual(got.indices, reference, (n, h))
            self.assertTrue(valid(a, m, got.indices))

    def test_boundaries_no_overclaims(self):
        for n in (2, 3, 6, 9, 30, 85):
            U = n * (n + 1) // 2
            m = U
            a = [0] * n
            got = solve_poly_deficit(a, m)
            self.assertEqual(got.indices, () if n >= 3 else (1, 2))
            self.assertEqual(got.status, "OPTIMAL")
            self.assertEqual(got.upper_bound, len(got.indices))
        a = [0, 0, 0, 0]
        for bad_m in (1, 2, 11, True, 3.2):
            with self.assertRaises(ValueError):
                solve_poly_deficit(a, bad_m)
        for bad_cap in (True, -1, 1.2):
            with self.assertRaises(ValueError):
                solve_poly_deficit(a, 10, max_state_cells=bad_cap)
        for bad_k in (True, 1.2):
            with self.assertRaises(ValueError):
                solve_poly_deficit(a, 10, K=bad_k)
        for n, h in ((80, 45), (100, 60), (150, 90)):
            a = [3**i for i in range(n)]
            U = n * (n + 1) // 2
            r = solve_poly_deficit(a, U - h, max_state_cells=25)
            self.assertEqual(r.status, "RESOURCE_LIMIT")
            self.assertEqual(r.indices, ())
            self.assertEqual((r.lower_bound, r.upper_bound), (0, n))


if __name__ == "__main__":
    unittest.main()
