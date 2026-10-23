"""Independent exhaustive oracle, baseline and resource falsification for v0.3."""
import importlib.util
import itertools
import random
import sys
import unittest
from pathlib import Path

from modconvex import solve as v02_solve, oracle as v02_oracle, cubic_dp, verify
from edge_dp import solve_edge
from experiments.v03.baselines import solve_mask, solve_edge_tuple

BASE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('v03_deficit', BASE/'experiments/v03/deficit.py')
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
solve_deficit = module.solve_deficit


def independent_oracle(a, m):
    """Enumerate every index subset, not omissions or distinct partitions."""
    n = len(a)
    answer = ()
    for mask in range(1 << n):
        witness = tuple(j+1 for j in range(n) if (mask >> j) & 1)
        if sum(witness) % m:
            continue
        if any(2*a[j-1] >= a[i-1]+a[k-1]
               for i, j, k in zip(witness, witness[1:], witness[2:])):
            continue
        if len(witness) > len(answer) or (len(witness) == len(answer)
                and witness < answer):
            answer = witness
    return answer


class DeficitFalsification(unittest.TestCase):
    def test_all_small_signed_values_and_high_moduli(self):
        count = 0
        for n in range(2, 8):
            U = n*(n+1)//2
            for a in itertools.product((-1, 0, 1), repeat=n):
                for m in range(max(2, U//2+1), U+1):
                    expected = independent_oracle(a, m)
                    out = solve_deficit(a, m)
                    self.assertEqual((out.status, out.indices, out.length),
                                     ('OPTIMAL', expected, len(expected)), (a, m))
                    self.assertTrue(verify(a, m, out.indices))
                    for K in (-1, 0, 1, len(expected), len(expected)+1, n+1):
                        got = solve_deficit(a, m, K=K)
                        self.assertEqual(got.status, 'FEASIBLE' if K <= len(expected)
                                         else 'INFEASIBLE', (a, m, K))
                        self.assertTrue(verify(a, m, got.indices))
                        if got.status == 'FEASIBLE':
                            self.assertGreaterEqual(len(got.indices), K)
                    if count % 83 == 0:
                        self.assertEqual(v02_solve(a, m).indices, expected)
                        self.assertEqual(solve_edge(a, m), expected)
                        self.assertEqual(v02_oracle(a, m), expected)
                        if n <= 5:
                            self.assertEqual(cubic_dp(a, m), expected)
                    count += 1
        self.assertEqual(count, 41085)

    def test_exact_comparator_equivalence_small(self):
        count = 0
        for n in range(2, 7):
            U = n*(n+1)//2
            for a in itertools.product((-1,0,1), repeat=n):
                for m in range(max(2, U//2+1), U+1):
                    expected = independent_oracle(a, m)
                    self.assertEqual(solve_mask(a, m), expected)
                    self.assertEqual(solve_edge_tuple(a, m), expected)
                    count += 1
        self.assertEqual(count, 10467)

    def test_fuzz_large_signed_boundary(self):
        rng = random.Random(20261023)
        for _ in range(250):
            n = rng.randrange(2, 12)
            a = [rng.choice((-10**120, -10**5, -1, 0, 1, 10**5, 10**120))
                 for _ in range(n)]
            U = n*(n+1)//2
            m = rng.randrange(max(2,U//2+1), U+1)
            expected = independent_oracle(a, m)
            self.assertEqual(solve_deficit(a, m).indices, expected)
            self.assertEqual(solve_edge_tuple(a, m), expected)

    def test_budget_and_domain(self):
        a = [i*i for i in range(12)]
        U = 78
        expected = independent_oracle(a, U-7)
        for budget in (0, 1, 3, 10, 20):
            for K in (None, 1, len(expected), len(expected)+1):
                got = solve_deficit(a, U-7, K=K, max_operations=budget)
                self.assertIn(got.status, ('RESOURCE_LIMIT', 'FEASIBLE', 'INFEASIBLE', 'OPTIMAL'))
                self.assertTrue(verify(a, U-7, got.indices))
                self.assertLessEqual(got.lower_bound, len(expected))
                self.assertGreaterEqual(got.upper_bound, len(expected))
                if got.status == 'FEASIBLE':
                    self.assertGreaterEqual(len(got.indices), K)
                if got.status == 'INFEASIBLE':
                    self.assertGreater(K, len(expected))
        for bad in (-1, 1.0, True, float('inf')):
            with self.assertRaises(ValueError):
                solve_deficit(a, U-7, max_operations=bad)
        for m in (2, U+1):
            with self.assertRaises(ValueError):
                solve_deficit(a, m)

    def test_long_prefix_does_not_recurse(self):
        # q=1100 is above the default CPython recursion limit.
        n = 1100
        a = [i*i for i in range(n)]
        U = n*(n+1)//2
        out = solve_deficit(a, U-1100, max_operations=1250000)
        self.assertIn(out.status, ('RESOURCE_LIMIT', 'OPTIMAL'))
        self.assertTrue(verify(a, U-1100, out.indices))


if __name__ == '__main__':
    unittest.main()
