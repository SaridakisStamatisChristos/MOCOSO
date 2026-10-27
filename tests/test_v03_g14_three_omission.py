"""Independent selected-mask and anchored-triple falsification for G14."""
from itertools import product
from random import Random
import unittest

from experiments.v03.g14_three_omission_certificate import certify_g14
from experiments.v03.g14_certified_hybrid import solve_g14
from experiments.v03.g13_two_sided_certificate import certify_g13
from experiments.v03.g11_hybrid import solve_g11
from tests.test_v03_g12_linear_certificate import independent_selected_mask_oracle


class G14ThreeOmission(unittest.TestCase):
    def test_exhaustive_73809_whole_witnesses_and_completeness(self):
        count=0
        for n in range(2,9):
            U=n*(n+1)//2
            for a in product((-3,0,2),repeat=n):
                for h in range(n):
                    m=U-h
                    if m<2 or U>=2*m:
                        continue
                    result=certify_g14(a,m)
                    oracle=independent_selected_mask_oracle(a,m)
                    self.assertEqual(result,oracle,(n,h,a))
                    count+=1
        self.assertEqual(count,73809)

    def test_constructed_maximal_three_omissions(self):
        for h in (6,7,8,9,10,12,19,32,48,65,100,150):
            n=h+10
            omitted={1,2,h-3}
            a=tuple((-10**110 if i in omitted else 4**i)
                    for i in range(1,n+1))
            m=n*(n+1)//2-h
            counters={}
            result=certify_g14(a,m,counters=counters)
            self.assertEqual(result,tuple(i for i in range(1,n+1)
                                         if i not in omitted),(h,counters))
            self.assertEqual(counters['status'],'three_omissions')
            self.assertEqual(solve_g14(a,m),solve_g11(a,m))

    def test_independent_oracle_beyond_h_nine(self):
        # Brute selected masks, NOT a resource/event oracle; here h=10,11,12.
        rng=Random(27102714)
        for h in (10,11,12):
            n=h+2
            m=n*(n+1)//2-h
            for case in range(16):
                if case%3==0:
                    q={1,2,h-3}
                    a=tuple(-10**60 if i in q else 4**i
                            for i in range(1,n+1))
                elif case%3==1:
                    a=tuple(i*i+rng.randrange(-i,i+1) for i in range(n))
                else:
                    a=tuple(rng.choice((-100,-2,0,1,10,100))
                            for _ in range(n))
                cert=certify_g14(a,m)
                oracle=independent_selected_mask_oracle(a,m)
                if cert is None:
                    self.assertLessEqual(len(oracle),n-4)
                else:
                    self.assertEqual(cert,oracle,(h,case,a))

    def test_signed_large_random_against_g11(self):
        rng=Random(20261027)
        alph=(-10**110,-11,-3,0,1,6,10**110)
        for case in range(900):
            n=rng.randrange(2,145)
            U=n*(n+1)//2
            h=rng.randrange(n)
            a=tuple(rng.choice(alph) for _ in range(n))
            self.assertEqual(solve_g14(a,U-h),solve_g11(a,U-h),
                             (case,n,h))
            prior=certify_g13(a,U-h)
            now=certify_g14(a,U-h)
            if prior is not None:
                self.assertEqual(now,prior)

    def test_safe_abstention_no_bad_triple_anchor(self):
        for h in (10,15,19,32,64):
            n=h+4
            a=tuple(i*i for i in range(n))
            m=n*(n+1)//2-h
            counters={}
            self.assertIsNone(certify_g14(a,m,counters=counters))
            self.assertEqual(counters['status'],'unresolved_no_bad_anchor')

    def test_input_validation(self):
        for a,m in (((0,True,3),6),((0,1,3),True),
                    ((0,1,3,5,10,20,40,80),24)):
            with self.assertRaises(ValueError):
                certify_g14(a,m)
            with self.assertRaises(ValueError):
                solve_g14(a,m)


if __name__=='__main__':
    unittest.main()
