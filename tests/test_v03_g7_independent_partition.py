"""Independent exact omitted-index partition oracle for G7, not a DP variant."""
from itertools import product
from random import Random
import unittest

from experiments.v03.g7_compact_lex import solve_compact_lex


def partition_oracle(values, modulus):
    """Enumerate each distinct increasing omitted-index partition of h once.

    This uses neither the event ordering nor the G3 reverse DP. It compares
    the entire selected tuple, including its mandatory suffix.
    """
    n = len(values)
    h = n * (n + 1) // 2 - modulus
    best = ()

    def visit(start, remaining, omitted):
        nonlocal best
        if remaining == 0:
            omitted_set = set(omitted)
            selected = tuple(i for i in range(1, n + 1)
                             if i not in omitted_set)
            if selected and all(
                values[x - 1] + values[z - 1] > 2 * values[y - 1]
                for x, y, z in zip(selected, selected[1:], selected[2:])
            ):
                if len(selected) > len(best) or (
                    len(selected) == len(best) and selected < best
                ):
                    best = selected
            return
        for i in range(start, min(n, remaining) + 1):
            visit(i + 1, remaining - i, omitted + (i,))

    visit(1, h, ())
    return best


class IndependentG7Audit(unittest.TestCase):
    def test_exhaustive_ternary_full_witness(self):
        count = 0
        for n in range(2, 8):
            U = n * (n + 1) // 2
            for values in product((-1, 0, 1), repeat=n):
                for h in range(min(n, U - U // 2)):
                    modulus = U - h
                    self.assertEqual(
                        solve_compact_lex(values, modulus),
                        partition_oracle(values, modulus),
                        (n, values, modulus))
                    count += 1
        self.assertEqual(count, 21321)

    def test_signed_seeded_full_witness(self):
        rng = Random(22102407)
        alphabet = (-10**90, -17, -2, 0, 1, 9, 10**90)
        for k in range(1500):
            n = rng.randint(2, 100)
            U = n * (n + 1) // 2
            h = rng.randint(0, min(n - 1, U - U // 2 - 1, 16))
            values = tuple(rng.choice(alphabet) for _ in range(n))
            self.assertEqual(
                solve_compact_lex(values, U - h),
                partition_oracle(values, U - h),
                (k, n, h))

    def test_global_lex_tie(self):
        values = (-3, -3, -3, -3, -2, 0)
        self.assertEqual(partition_oracle(values, 16), (1, 4, 5, 6))
        self.assertEqual(solve_compact_lex(values, 16), (1, 4, 5, 6))


if __name__ == "__main__":
    unittest.main()
