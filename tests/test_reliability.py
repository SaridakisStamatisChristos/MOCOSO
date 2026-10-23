"""Independent reliability tests for v0.2; do not mutate archived research reports."""
import itertools
import random
import unittest
from array import array
from unittest.mock import patch

from modconvex import dense_dp_payload_bytes, oracle, solve, verify, index_only_upper
from edge_dp import solve_edge


class Exactness(unittest.TestCase):
    def test_exhaustive_small_alphabet_and_lex_order(self):
        for n in range(5):
            for a in itertools.product((-2, 0, 2), repeat=n):
                for m in range(2, n * (n + 1) // 2 + 3):
                    expected = oracle(a, m)
                    result = solve(a, m)
                    self.assertEqual((result.status, result.indices),
                                     ('OPTIMAL', expected), (a, m))
                    self.assertEqual(result.length, len(expected))
                    self.assertTrue(result.lower_bound <= len(expected) <= result.upper_bound)

    def test_large_signed_integer_and_modulus(self):
        big = 10**300
        cases = [
            ([], 2), ([big], 2), ([-big, -big, -big], 3),
            ([-big, 0, big, big + 1], 6), ([0, 1, 2], 6),
            ([0, 1, 3], 6), ([3, 3, 3, 3], 5),
            ([big, -big, big, -big, big], 10**200),
            ([0, 4, 9, 16], 10),
            ([0, 4, 9, 16], 10**200),
        ]
        for a, m in cases:
            with self.subTest(a=a, m=m):
                exp = oracle(a, m)
                got = solve(a, m)
                self.assertEqual(got.indices, exp)
                self.assertEqual(solve_edge(a, m), exp)

    def test_seeded_random_and_decisions(self):
        rng = random.Random(204002)
        for _ in range(220):
            n = rng.randrange(0, 10)
            a = tuple(rng.choice([-10**100, -3, 0, 0, 7, 10**100])
                      for _ in range(n))
            m = rng.randrange(2, n * (n + 1) // 2 + 6)
            optimum = oracle(a, m)
            result = solve(a, m)
            self.assertEqual(result.indices, optimum)
            self.assertEqual(solve_edge(a, m), optimum)
            for K in (-1, 0, 1, len(optimum), len(optimum)+1, n+1):
                got = solve(a, m, K=K)
                self.assertEqual(got.status, 'FEASIBLE' if len(optimum) >= K else 'INFEASIBLE')
                self.assertTrue(verify(a, m, got.indices))
                if got.status == 'FEASIBLE':
                    self.assertGreaterEqual(len(got.indices), K)

    def test_pure_index_bounds(self):
        for n in range(16):
            for m in range(2, n * (n + 1) // 2 + 5):
                ub = index_only_upper(n, m)
                self.assertGreaterEqual(ub, 0)
                self.assertLessEqual(ub, n)
                for values in ((0,) * n, tuple(i*i for i in range(n))):
                    self.assertLessEqual(len(oracle(values, m)) if n <= 9 else 0, ub)


class ResourceReliability(unittest.TestCase):
    def test_adaptive_dense_payload_bytes(self):
        for n, m in [(0, 2), (1, 200), (12, 7), (150, 25),
                     (32767, 2), (32768, 2), (65535, 2), (65536, 2)]:
            pairs = n * (n-1) // 2
            length_width = (array('h').itemsize if n <= 32767
                            else array('i').itemsize)
            successor_width = (array('H').itemsize if n <= 65535
                               else array('I').itemsize)
            self.assertEqual(dense_dp_payload_bytes(n, m),
                             pairs * m * (length_width + successor_width))
        with self.assertRaises(ValueError):
            dense_dp_payload_bytes(-1, 2)

    def test_zero_time_budget_before_sort(self):
        a = [i*i for i in range(15)]
        with patch('modconvex.time.monotonic', side_effect=[0.0, 1.0]):
            result = solve(a, 3, max_seconds=0.1)
        self.assertEqual(result.status, 'RESOURCE_LIMIT')
        self.assertEqual(result.reason, 'soft time budget')
        self.assertTrue(verify(a, 3, result.indices))
        self.assertEqual(result.upper_bound, len(a))

    def test_time_budget_after_sort(self):
        a = [i*i for i in range(15)]
        with patch('modconvex.time.monotonic', side_effect=[0.0, 0.0, 1.0]):
            result = solve(a, 3, max_seconds=0.1)
        self.assertEqual(result.status, 'RESOURCE_LIMIT')
        self.assertTrue(verify(a, 3, result.indices))

    def test_memory_preflight_no_false_infeasible(self):
        a = [i*i for i in range(14)]
        self.assertGreater(dense_dp_payload_bytes(len(a), 5), 250)
        with patch('modconvex.tracemalloc.get_traced_memory', return_value=(0, 0)):
            out = solve(a, 5, K=13, max_heap_bytes=250)
        self.assertEqual(out.status, 'RESOURCE_LIMIT')
        self.assertIn('preflight', out.reason)
        self.assertTrue(verify(a, 5, out.indices))
        self.assertLessEqual(out.lower_bound, len(oracle(a, 5)))
        self.assertLessEqual(len(oracle(a, 5)), out.upper_bound)

    def test_bounded_interruption_cannot_imply_no(self):
        a = [i*i for i in range(9)]
        optimum = oracle(a, 2)
        for limit in (0, 1, 3):
            result = solve(a, 2, K=len(optimum), max_operations=limit)
            self.assertIn(result.status, ('RESOURCE_LIMIT', 'FEASIBLE'))
            self.assertTrue(verify(a, 2, result.indices))
            self.assertLessEqual(result.lower_bound, len(optimum))
            self.assertGreaterEqual(result.upper_bound, len(optimum))
            if result.status == 'FEASIBLE':
                self.assertGreaterEqual(len(result.indices), len(optimum))

    def test_proved_shortcuts_with_limits(self):
        a = [0, 1, 3]
        self.assertEqual(solve(a, 6, K=4, max_operations=0).status, 'INFEASIBLE')
        self.assertEqual(solve(a, 1000, K=1, max_operations=0).status, 'INFEASIBLE')
        self.assertEqual(solve(a, 6, K=0, max_operations=0).status, 'FEASIBLE')


if __name__ == '__main__':
    unittest.main()
