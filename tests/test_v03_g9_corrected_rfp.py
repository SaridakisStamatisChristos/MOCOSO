"""RFP regression for audited G9; historical solver and corpus stay frozen.

The independent selected-subset oracle below imports no solver or DP reference.
Tracemalloc evidence is CPython-specific and is not an asymptotic proof.
"""
from itertools import product
from random import Random
import ast
import gc
import platform
import tracemalloc
import unittest
from pathlib import Path

from experiments.v03.g9_corrected import solve_g9 as corrected
from experiments.v03.g9_quadratic_lex import solve_g9 as historical


def subset_reference(a, m):
    best = ()
    for mask in range(1 << len(a)):
        indices = tuple(i + 1 for i in range(len(a)) if mask & (1 << i))
        if sum(indices) % m:
            continue
        if any(a[i - 1] + a[k - 1] <= 2*a[j - 1]
               for i, j, k in zip(indices, indices[1:], indices[2:])):
            continue
        if len(indices) > len(best) or (len(indices) == len(best) and indices < best):
            best = indices
    return best


def traced_peak(solver, a, m):
    gc.collect()
    tracemalloc.start()
    try:
        result = solver(a, m)
        _, peak = tracemalloc.get_traced_memory()
        return result, peak
    finally:
        tracemalloc.stop()


class G9RFPRegression(unittest.TestCase):
    def test_exact_small_ternary(self):
        cases = 0
        for n in range(2, 7):
            U = n * (n + 1) // 2
            for a in product((-2, 0, 3), repeat=n):
                for h in range(n):
                    m = U - h
                    if m < 2 or 2*m <= U:
                        continue
                    self.assertEqual(corrected(a, m), subset_reference(a, m),
                                     (n, a, m))
                    cases += 1
        self.assertGreater(cases, 1000)

    def test_seeded_large_signed_and_old_equivalence(self):
        rng = Random(20261026)
        alphabet = (-10**140, -10**50, -9, 0, 1, 17, 10**50, 10**140)
        for case in range(300):
            n = rng.randint(2, 45)
            h = rng.randrange(n)
            U = n*(n+1)//2
            a = tuple(rng.choice(alphabet) for _ in range(n))
            self.assertEqual(corrected(a, U-h), historical(a, U-h), (case, n, h))

    def test_lexicographic_and_suffix_edges(self):
        cases = [((-3,-3,-3,-3,-2,0),16,(1,4,5,6)),
                 ((0,1,2),6,()),
                 ((0,1,3),6,(1,2,3)),
                 ((0,0,0,0),10,())]
        for a, m, expected in cases:
            self.assertEqual(corrected(a, m), expected)

    def test_h_zero_streaming_large_output(self):
        n = 25000
        a = tuple(i*i for i in range(n))
        result = corrected(a, n*(n+1)//2)
        self.assertEqual(len(result), n)
        self.assertEqual(result[:3], (1,2,3))
        self.assertEqual(result[-3:], (n-2,n-1,n))

    def test_no_selected_output_slice(self):
        source = Path(__file__).resolve().parents[1] / 'experiments/v03/g9_corrected.py'
        tree = ast.parse(source.read_text(encoding='utf-8'))
        for node in ast.walk(tree):
            if isinstance(node, ast.Subscript) and isinstance(node.value, ast.Name):
                self.assertFalse(node.value.id == 'selected' and
                                 isinstance(node.slice, ast.Slice),
                                 'Output-sized selected slice violates auxiliary accounting')

    @unittest.skipUnless(platform.python_implementation() == 'CPython',
                         'CPython tracemalloc regression only')
    def test_h_zero_no_linear_validation_copy(self):
        n = 12000
        a = tuple(i*i for i in range(n))
        m = n*(n+1)//2
        old_result, original = traced_peak(historical, a, m)
        new_result, fixed = traced_peak(corrected, a, m)
        self.assertEqual(old_result, new_result)
        self.assertGreater(original - fixed, 4*n, (original, fixed, n))


if __name__ == '__main__':
    unittest.main()
