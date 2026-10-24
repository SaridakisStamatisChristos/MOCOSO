"""Independent witness/oracle checks for the G8 research-only implementation."""
from itertools import product
from math import isqrt
from random import Random
import unittest
from experiments.v03.g8_persistent_intervals import solve_g8
from experiments.v03.g7_compact_lex import solve_compact_lex
from tests.test_v03_g7_independent_partition import partition_oracle


def counted_by_gap(h):
    count = h+1  # adjacent edges with p=h+2
    for t in range(1, isqrt(2*h)+1):
        for i in range(1, h+2-t):
            if t*i + t*(t+1)//2 <= h:
                count += 1
    return count


def counted_by_brute(h):
    p = h+2
    return sum(1 for i in range(1, p)
               for j in range(i+1, p+1)
               if sum(range(i+1, j)) <= h)


class G8Independent(unittest.TestCase):
    def test_edge_count_two_independent_methods(self):
        for h in range(160):
            a = counted_by_gap(h)
            self.assertEqual(a, counted_by_brute(h))
            self.assertLessEqual(a, (h+2)*(3+(h+2).bit_length()))

    def test_exhaustive_ternary_full_witness(self):
        count = 0
        for n in range(2, 8):
            U = n*(n+1)//2
            for a in product((-1, 0, 1), repeat=n):
                for h in range(min(n, U-U//2)):
                    m = U-h
                    expected = partition_oracle(a, m)
                    self.assertEqual(solve_g8(a, m), expected, (n, a, m))
                    self.assertEqual(solve_compact_lex(a, m), expected)
                    count += 1
        self.assertEqual(count, 21321)

    def test_large_signed_seeded_full_witness(self):
        rng = Random(22102407)
        alphabet = (-10**90, -17, -2, 0, 1, 9, 10**90)
        for k in range(1500):
            n = rng.randint(2, 100)
            U = n*(n+1)//2
            h = rng.randint(0, min(n-1, U-U//2-1, 16))
            a = tuple(rng.choice(alphabet) for _ in range(n))
            self.assertEqual(
                solve_g8(a, U-h), partition_oracle(a, U-h),
                (k, n, h))

    def test_equal_differences_and_global_lex(self):
        self.assertEqual(solve_g8((-3, -3, -3, -3, -2, 0), 16),
                         (1, 4, 5, 6))
        self.assertEqual(solve_g8((0, 1, 2), 6), ())
        self.assertEqual(solve_g8((0, 1, 3), 6), (1, 2, 3))
        self.assertEqual(solve_g8((0, 0, 0, 0), 10), ())
        self.assertEqual(solve_g8((0, 1, 2, 3, 7, 15, 31), 26), ())

    def test_fixed_suffix_and_domain(self):
        for n, h in ((2, 0), (2, 1), (12, 4), (25, 15), (70, 50), (1000, 4)):
            a = [3**i for i in range(n)]
            m = n*(n+1)//2-h
            self.assertEqual(solve_g8(a, m), solve_compact_lex(a, m))
            if n >= 12:
                a[-1] = -a[-1]
                self.assertEqual(solve_g8(a, m), ())
        with self.assertRaises(ValueError):
            solve_g8((0, True, 3), 6)


if __name__ == "__main__":
    unittest.main()
