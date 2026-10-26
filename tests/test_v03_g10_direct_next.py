"""Adversarial executable checks of G10. These tests do not establish novelty."""
from itertools import product
from random import Random
import unittest

from experiments.v03.g10_direct_next import solve_g10
from research.v03.g9_independent_audit.solver_corrected import solve_g9


def independent_reference(a,m):
    best=()
    for mask in range(1<<len(a)):
        selected=tuple(i+1 for i in range(len(a)) if mask>>i&1)
        if sum(selected)%m:
            continue
        if any(a[x-1]+a[z-1]<=2*a[y-1]
               for x,y,z in zip(selected,selected[1:],selected[2:])):
            continue
        if len(selected)>len(best) or (len(selected)==len(best) and selected<best):
            best=selected
    return best


class G10DirectNext(unittest.TestCase):
    def test_ternary_exhaustive(self):
        count=0
        for n in range(2,9):
            U=n*(n+1)//2
            for a in product((-3,0,5),repeat=n):
                for h in range(n):
                    m=U-h
                    if m<2 or 2*m<=U:
                        continue
                    self.assertEqual(solve_g10(a,m),independent_reference(a,m),(n,h,a))
                    count+=1
        self.assertEqual(count,73809)

    def test_four_value_exhaustive(self):
        count=0
        for n in range(2,8):
            U=n*(n+1)//2
            for a in product((-2,-1,0,1),repeat=n):
                for h in range(n):
                    m=U-h
                    if m<2 or 2*m<=U:
                        continue
                    self.assertEqual(solve_g10(a,m),independent_reference(a,m),(n,h,a))
                    count+=1
        self.assertEqual(count,145632)

    def test_seeded_signed_g9_equivalence(self):
        rng=Random(20261026)
        alphabet=(-10**160,-10**100,-5,0,1,3,10**100,10**160)
        for j in range(1200):
            n=rng.randint(2,119)
            h=rng.randrange(n)
            U=n*(n+1)//2
            a=tuple(rng.choice(alphabet) for _ in range(n))
            self.assertEqual(solve_g10(a,U-h),solve_g9(a,U-h),(j,n,h))

    def test_maximal_omission_instances(self):
        for k in (1,2,3,4,5,7,9,11):
            h=k*(k+1)//2
            n=h+15
            a=tuple([-10**200]*k+[4**i for i in range(k,n)])
            counters={}
            answer=solve_g10(a,n*(n+1)//2-h,counters=counters)
            self.assertEqual(answer,tuple(range(k+1,n+1)))
            self.assertEqual(counters['omissions'],k)
            self.assertEqual(counters['queries'],k)
            self.assertEqual(answer,solve_g9(a,n*(n+1)//2-h))

    def test_boundaries_and_large_output(self):
        self.assertEqual(solve_g10((0,1,2),6),())
        self.assertEqual(solve_g10((-3,-3,-3,-3,-2,0),16),(1,4,5,6))
        for n in (2,3,10000):
            a=tuple(i*i for i in range(n))
            self.assertEqual(solve_g10(a,n*(n+1)//2),tuple(range(1,n+1)))
        for a,m in (((0,True,3),6),((0,1,3),True),
                    ((0,1,3,5,10,20,40,80),24)):
            with self.assertRaises(ValueError):
                solve_g10(a,m)


if __name__=='__main__':
    unittest.main()
