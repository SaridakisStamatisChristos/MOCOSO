"""G7 direct-selected-subset oracle and frozen G3 differential checks."""
from itertools import product
from random import Random
import unittest
from experiments.v03.g7_compact_lex import solve_compact_lex
from experiments.v03.poly_deficit import solve_poly_deficit


def direct_selected_subset_oracle(a, m):
    best = ()
    for mask in range(1 << len(a)):
        indices = tuple(i+1 for i in range(len(a)) if mask >> i & 1)
        if sum(indices) % m:
            continue
        if any(a[x-1]+a[z-1] <= 2*a[y-1]
               for x,y,z in zip(indices, indices[1:], indices[2:])):
            continue
        if len(indices) > len(best) or (
                len(indices) == len(best) and indices < best):
            best = indices
    return best


class G7CompactLex(unittest.TestCase):
    def test_exhaustive_signed_three_values_full_lex(self):
        count = 0
        for n in range(2,8):
            U=n*(n+1)//2
            for a in product((-1,0,1),repeat=n):
                for m in range(U//2+1,U+1):
                    if U-m>=n:
                        continue
                    expected=direct_selected_subset_oracle(a,m)
                    self.assertEqual(solve_compact_lex(a,m),expected,(n,a,m))
                    count+=1
        self.assertEqual(count,21321)

    def test_exhaustive_signed_four_values_full_lex(self):
        count = 0
        for n in range(2,8):
            U=n*(n+1)//2
            for a in product((-2,-1,0,1),repeat=n):
                for m in range(U//2+1,U+1):
                    if U-m>=n:
                        continue
                    self.assertEqual(solve_compact_lex(a,m),
                                     direct_selected_subset_oracle(a,m),
                                     (n,a,m))
                    count+=1
        self.assertEqual(count,145632)

    def test_big_signed_full_lex_against_both_oracles(self):
        rng=Random(20261024)
        for _ in range(1000):
            n=rng.randrange(2,11)
            U=n*(n+1)//2
            h=rng.randrange(min(n,U-U//2))
            a=[rng.choice((-10**160,-10**90,-1,0,0,1,10**90,10**160))
               for _ in range(n)]
            m=U-h
            expected=direct_selected_subset_oracle(a,m)
            self.assertEqual(solve_compact_lex(a,m),expected,(n,a,m))
            self.assertEqual(solve_poly_deficit(a,m).indices,expected,(n,a,m))

    def test_superconvex_suffix_and_lex_tie(self):
        for n,h in ((2,0),(2,1),(12,4),(25,15),(40,25),
                    (70,50),(1000,4)):
            a=[3**i for i in range(n)]
            m=n*(n+1)//2-h
            result=solve_compact_lex(a,m)
            self.assertEqual(sum(result),m)
            self.assertEqual(result,solve_poly_deficit(a,m).indices)
            if n>=12:
                a[-1]=-a[-1]
                self.assertEqual(solve_compact_lex(a,m),())
        # Distinct equal-cardinality omission sets summing 5:
        # omit (2,3) is lex-better selected tuple than omit (1,4).
        a=(-3,-3,-3,-3,-2,0)
        self.assertEqual(solve_compact_lex(a,16),(1,4,5,6))

    def test_threshold_tie_and_crossing(self):
        self.assertEqual(solve_compact_lex((0,1,2),6),())
        self.assertEqual(solve_compact_lex((0,1,3),6),(1,2,3))
        self.assertEqual(solve_compact_lex((0,0,0,0),10),())
        # Omit index 2; crossing triple (1,3,4) fails even while
        # fully fixed triples ending >= q+3 are strictly convex.
        self.assertEqual(
            solve_compact_lex((0,1,2,3,7,15,31),26),())

    def test_domain_and_non_applicability(self):
        for bad_m in (1,True,0,4.5):
            with self.assertRaises(ValueError):
                solve_compact_lex((0,1,3),bad_m)
        with self.assertRaises(ValueError):
            solve_compact_lex((0,True,3),6)
        # High modulus alone is insufficient; requires h<n.
        with self.assertRaises(ValueError):
            solve_compact_lex((0,1,3,10,25,51,100,201),24)


if __name__=="__main__":
    unittest.main()
