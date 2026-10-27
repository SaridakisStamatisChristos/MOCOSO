"""Independent RFP verification for the exact G12 linear fast path.

The oracle enumerates selected bitmasks directly (no omission partitions, no
sorted-gap or score DP). A None certificate is a valid abstention, never a
claim of infeasibility. Results are compared as complete canonical tuples.
"""
from itertools import product
from random import Random
import unittest

from experiments.v03.g12_linear_certificate import certify_up_to_two_omissions
from experiments.v03.g12_certified_hybrid import solve_g12
from experiments.v03.g11_hybrid import solve_g11


def independent_selected_mask_oracle(a,m):
    n=len(a)
    best=()
    for mask in range(1,1<<n):
        selected=tuple(k+1 for k in range(n) if mask & (1<<k))
        if sum(selected)%m:
            continue
        if any(a[x-1]+a[z-1]<=2*a[y-1]
               for x,y,z in zip(selected,selected[1:],selected[2:])):
            continue
        if len(selected)>len(best) or (
                len(selected)==len(best) and selected<best):
            best=selected
    return best


class G12LinearCertificate(unittest.TestCase):
    def test_73809_exact_or_abstain_small_selected_mask_cases(self):
        checked=0
        certified=0
        for n in range(2,9):
            U=n*(n+1)//2
            for a in product((-3,0,2),repeat=n):
                for h in range(n):
                    m=U-h
                    if m<2 or U>=2*m:
                        continue
                    expected=independent_selected_mask_oracle(a,m)
                    certificate=certify_up_to_two_omissions(a,m)
                    if certificate is None:
                        self.assertLessEqual(len(expected),n-3,(n,a,h))
                    else:
                        self.assertEqual(certificate,expected,(n,a,h))
                        certified+=1
                    checked+=1
        self.assertEqual(checked,73809)
        self.assertGreater(certified,40000)

    def test_explicit_one_and_two_omission_extraction(self):
        for h in (3,7,18,19,64,65,110,301):
            n=h+9
            U=n*(n+1)//2
            a=tuple(4**i for i in range(n))
            details={}
            out=certify_up_to_two_omissions(a,U-h,counters=details)
            self.assertEqual(out,tuple(i for i in range(1,n+1) if i!=h))
            self.assertEqual(details['status'],'one_omission')
        for h in (3,19,32,64,65,110):
            n=h+7
            u=(h-1)//2
            v=h-u
            bad={u,v}
            a=tuple((-10**140 if i in bad else 4**i)
                    for i in range(1,n+1))
            details={}
            out=certify_up_to_two_omissions(a,n*(n+1)//2-h,counters=details)
            self.assertEqual(out,tuple(i for i in range(1,n+1)
                                       if i not in bad))
            self.assertEqual(details['status'],'two_omissions')

    def test_unresolved_not_falsely_infeasible(self):
        for h in (6,12,24,32,66):
            n=h+10
            excluded={1,2,h-3}
            self.assertEqual(sum(excluded),h)
            a=tuple(-10**100 if i in excluded else 4**i
                    for i in range(1,n+1))
            self.assertIsNone(certify_up_to_two_omissions(
                a,n*(n+1)//2-h))
            self.assertEqual(solve_g12(a,n*(n+1)//2-h),
                             solve_g11(a,n*(n+1)//2-h))

    def test_arbitrary_signed_differential(self):
        rng=Random(20261027)
        alph=(-10**70,-9,-2,0,1,3,10**70)
        for case in range(800):
            n=rng.randint(2,130)
            h=rng.randrange(n)
            U=n*(n+1)//2
            a=tuple(rng.choice(alph) for _ in range(n))
            direct=certify_up_to_two_omissions(a,U-h)
            g11=solve_g11(a,U-h)
            if direct is not None:
                self.assertEqual(direct,g11,(case,n,h))
            self.assertEqual(solve_g12(a,U-h),g11,(case,n,h))

    def test_boundaries_empty_and_large_streamed_witness(self):
        self.assertEqual(certify_up_to_two_omissions((0,1,2),6),())
        self.assertEqual(solve_g12((0,1,2),6),())
        self.assertEqual(solve_g12((0,1,3),6),(1,2,3))
        n=3500
        a=tuple(4**i for i in range(n))
        h=n-1
        counters={}
        chosen=solve_g12(a,n*(n+1)//2-h,counters=counters)
        self.assertEqual(len(chosen),n-1)
        self.assertNotIn(h,chosen)
        self.assertEqual(counters['mode'],'linear_certificate')

    def test_input_validation(self):
        for a,m in (((0,True,3),6),((0,1,3),True),
                    ((0,1,3,5,10,20,40,80),24)):
            with self.assertRaises(ValueError):
                certify_up_to_two_omissions(a,m)
            with self.assertRaises(ValueError):
                solve_g12(a,m)


if __name__=='__main__':
    unittest.main()
