"""G9 independently enumerated selected-subset and omitted-partition checks."""
from itertools import product
from random import Random
import unittest

from experiments.v03.g9_quadratic_lex import solve_g9
from experiments.v03.g8_persistent_intervals import solve_g8
from tests.test_v03_g7_independent_partition import partition_oracle


def selected_subset_oracle(a, m):
    """Independent unconstrained selected-subset enumeration, no complement DP."""
    n = len(a)
    best = ()
    for mask in range(1 << n):
        chosen = tuple(i+1 for i in range(n) if mask >> i & 1)
        if sum(chosen) % m:
            continue
        if any(a[x-1]+a[z-1] <= 2*a[y-1]
               for x,y,z in zip(chosen, chosen[1:], chosen[2:])):
            continue
        if len(chosen)>len(best) or (len(chosen)==len(best) and chosen<best):
            best = chosen
    return best


class G9QuadraticSpaceIndependent(unittest.TestCase):
    def test_exhaustive_ternary_full_selected_subset(self):
        count=0
        for n in range(2, 8):
            U=n*(n+1)//2
            for a in product((-1,0,1), repeat=n):
                for h in range(min(n, U-U//2)):
                    m=U-h
                    self.assertEqual(solve_g9(a,m),
                                     selected_subset_oracle(a,m), (n,a,m))
                    count+=1
        self.assertEqual(count, 21321)

    def test_exhaustive_four_valued_full_selected_subset(self):
        count=0
        for n in range(2, 8):
            U=n*(n+1)//2
            for a in product((-2,-1,0,1),repeat=n):
                for h in range(min(n,U-U//2)):
                    m=U-h
                    self.assertEqual(solve_g9(a,m),
                                     selected_subset_oracle(a,m), (n,a,m))
                    count+=1
        self.assertEqual(count,145632)

    def test_independent_partition_large_signed_seed(self):
        rng=Random(22102407)
        choices=(-10**90,-17,-2,0,1,9,10**90)
        for k in range(1500):
            n=rng.randint(2,100)
            U=n*(n+1)//2
            h=rng.randint(0,min(n-1,U-U//2-1,16))
            a=tuple(rng.choice(choices) for _ in range(n))
            self.assertEqual(solve_g9(a,U-h),partition_oracle(a,U-h),
                             (k,n,h))

    def test_lex_tie_equal_differences_fixed_suffix_and_zero(self):
        self.assertEqual(solve_g9((-3,-3,-3,-3,-2,0),16),(1,4,5,6))
        self.assertEqual(solve_g9((0,1,2),6),())
        self.assertEqual(solve_g9((0,1,3),6),(1,2,3))
        self.assertEqual(solve_g9((0,0,0,0),10),())
        self.assertEqual(solve_g9((0,1,2,3,7,15,31),26),())
        for n,h in ((2,0),(2,1),(12,4),(25,15),(40,25),(70,50),(1000,4)):
            a=[3**i for i in range(n)]
            m=n*(n+1)//2-h
            self.assertEqual(solve_g9(a,m),solve_g8(a,m))
            if n>=12:
                a[-1]=-a[-1]
                self.assertEqual(solve_g9(a,m),())

    def test_query_bound_and_domain(self):
        for n,h in ((6,5),(12,11),(26,25),(60,59)):
            a=[3**i for i in range(n)]
            counters={}
            out=solve_g9(a,n*(n+1)//2-h,counters=counters)
            self.assertEqual(len(out),n-counters["omissions"])
            # A safe numerical envelope for <=1+s(1+ceil(log2(h+1))) queries.
            self.assertLessEqual(counters["queries"],
                                 1+counters["omissions"]*(2+(h+1).bit_length()))
        for a,m in (((0,True,3),6),((0,1,3),True),
                    ((0,1,3,5,10,20,40,80),24)):
            with self.assertRaises(ValueError):
                solve_g9(a,m)


if __name__=="__main__":
    unittest.main()
