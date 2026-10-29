"""Selected-subset oracle, independent rank enumeration and metamorphic checks."""
from itertools import product
from random import Random
import unittest

from experiments.v03.g15_ranked_omissions import (
    _counts, _unrank, solve_ranked, solve_g15,
)
from experiments.v03.g10_direct_next import solve_g10
from tests.test_v03_g12_linear_certificate import independent_selected_mask_oracle


class G15Ranked(unittest.TestCase):
    def test_exhaustive_all_high_moduli(self):
        count = extended = 0
        for n in range(2, 9):
            u = n * (n + 1) // 2
            # Enumerate selected masks once per array; independent of ranks,
            # omission partitions, sorted events, and the candidate DP.
            selected = [(tuple(i+1 for i in range(n) if mask >> i & 1))
                        for mask in range(1, 1 << n)]
            for a in product((-3, 0, 2), repeat=n):
                expected = {}
                for s in selected:
                    m = sum(s)
                    if m < 2 or 2*m <= u:
                        continue
                    if any(a[x-1]+a[z-1] <= 2*a[y-1]
                           for x,y,z in zip(s,s[1:],s[2:])):
                        continue
                    old = expected.get(m, ())
                    if len(s)>len(old) or (len(s)==len(old) and s<old):
                        expected[m] = s
                for m in range(max(2,u//2+1),u+1):
                    answer = expected.get(m, ())
                    self.assertEqual(solve_ranked(a,m),answer,(n,a,m))
                    self.assertEqual(solve_g15(a,m),answer,(n,a,m))
                    count += 1
                    extended += u-m >= n
        self.assertEqual(count, 159183)
        self.assertEqual(extended, 85374)

    def test_rank_bijection_and_gap_telescope(self):
        for k in range(0, 13):
            by_sum = {}
            for bits in product((0,1), repeat=k):
                q = tuple(i+1 for i,b in enumerate(bits) if b)
                by_sum.setdefault(sum(q), []).append(q)
            for h, family in by_sum.items():
                c = _counts(k,h)
                self.assertEqual(c[1][h],len(family))
                for rank,q in enumerate(family):
                    self.assertEqual(tuple(_unrank(c,k,h,rank)),q)
        c = _counts(40,80)
        for lo in range(1,35):
            for hi in range(lo,40):
                gap = sum(range(lo,hi+1))
                for s in range(gap,81):
                    remaining, direct = s, 0
                    for q in range(lo,hi+1):
                        direct += c[q+1][remaining]
                        remaining -= q
                    self.assertEqual(direct,c[lo][s]-c[hi+1][s-gap])

    def test_random_general_regime_and_affine_invariance(self):
        rng=Random(29102615)
        for _ in range(500):
            n=rng.randrange(2,13)
            u=n*(n+1)//2
            m=rng.randrange(max(2,u//2+1),u+1)
            a=tuple(rng.choice((-10**100,-9,-1,0,2,7,10**100))
                    for _ in range(n))
            expected=independent_selected_mask_oracle(a,m)
            self.assertEqual(solve_ranked(a,m),expected)
            self.assertEqual(solve_g15(a,m),expected)
            self.assertEqual(solve_ranked(tuple(7*x+31 for x in a),m),expected)

    def test_many_omissions_and_single_sweep(self):
        for t in (4,5,7,9,11,15):
            omitted=set(range(1,t+1))
            h=sum(omitted)
            n=h+3
            a=tuple(-10**200 if i in omitted else 4**i
                    for i in range(1,n+1))
            m=n*(n+1)//2-h
            details={}
            answer=solve_ranked(a,m,counters=details)
            self.assertEqual(answer,tuple(range(t+1,n+1)))
            self.assertEqual(answer,solve_g10(a,m))
            self.assertEqual(details['sweeps'],1)

    def test_last_endpoint_and_infeasibility(self):
        # h>=n: optimal answers need not include the last input position.
        for n in range(4,11):
            for a in ((0,)*n,tuple(i*i for i in range(n)),
                      tuple(4**i for i in range(n))):
                u=n*(n+1)//2
                for h in range(n,(u-1)//2+1):
                    self.assertEqual(solve_ranked(a,u-h),
                                     independent_selected_mask_oracle(a,u-h))

    def test_invalid_and_zero_deficit(self):
        for a,m in (((),2),((1,),2),((0,True,3),6),
                    ((0,1,3),True),((0,1,3),3),((0,1,3),7)):
            for fun in (solve_ranked,solve_g15):
                with self.assertRaises(ValueError): fun(a,m)
        self.assertEqual(solve_ranked((0,1,2),6),())
        self.assertEqual(solve_ranked((0,1,3),6),(1,2,3))


if __name__=='__main__':
    unittest.main()
