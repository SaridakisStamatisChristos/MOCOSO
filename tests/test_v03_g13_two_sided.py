"""Independent RFP tests for G13's O(n) *two-sided* exact certificates.

Brute oracle enumerates selected subsets, not omission pairs or interval DP.
A None return is safe abstention, not an infeasibility claim.
"""
from itertools import product
from random import Random
import unittest

from experiments.v03.g13_two_sided_certificate import certify_g13
from experiments.v03.g13_certified_hybrid import solve_g13
from experiments.v03.g12_linear_certificate import certify_up_to_two_omissions
from experiments.v03.g11_hybrid import solve_g11
from tests.test_v03_g12_linear_certificate import independent_selected_mask_oracle


class G13Certified(unittest.TestCase):
    def test_73809_independent_bruteforce_certificates(self):
        cases=resolved=weighted=0
        for n in range(2,9):
            U=n*(n+1)//2
            for a in product((-3,0,2),repeat=n):
                for h in range(n):
                    m=U-h
                    if m<2 or U>=2*m:
                        continue
                    oracle=independent_selected_mask_oracle(a,m)
                    counters={}
                    got=certify_g13(a,m,counters=counters)
                    if got is None:
                        self.assertLessEqual(len(oracle),n-3,(n,a,m))
                    else:
                        self.assertEqual(got,oracle,(n,a,m,counters))
                        resolved+=1
                    if counters["status"]=="weighted_hitting_infeasible":
                        weighted+=1
                    cases+=1
        self.assertEqual(cases,73809)
        self.assertGreater(resolved,65000)
        self.assertGreater(weighted,9000)

    def test_hitting_succeeds_even_when_suffix_has_no_triple(self):
        # n=h+2 makes the compulsory suffix just two indices. This is
        # nontrivial infeasibility from the 4-state *weighted* hitting DP.
        for h in (6,8,10,12,19,32,64,110):
            n=h+2
            m=n*(n+1)//2-h
            counters={}
            self.assertEqual(certify_g13((0,)*n,m,counters=counters),())
            self.assertEqual(counters["status"],"weighted_hitting_infeasible")

    def test_g13_never_retracts_g12_certificate(self):
        rng=Random(20261027)
        for case in range(1400):
            n=rng.randint(2,135)
            h=rng.randrange(n)
            U=n*(n+1)//2
            if case%3==0:
                a=tuple(i*i+rng.randint(-i,i) for i in range(n))
            elif case%3==1:
                a=tuple(rng.choice((-10**130,-5,0,1,9,10**130))
                        for _ in range(n))
            else:
                a=tuple(4**i for i in range(n))
            c12=certify_up_to_two_omissions(a,U-h)
            c13=certify_g13(a,U-h)
            if c12 is not None:
                self.assertEqual(c13,c12,(case,n,h))
            self.assertEqual(solve_g13(a,U-h),solve_g11(a,U-h),
                             (case,n,h))

    def test_bridged_triples_distinguish_bad_and_good_deletions(self):
        # Squares are strictly convex as a full array, but deleting index 3
        # creates a descending consecutive difference at selected endpoints.
        self.assertEqual(certify_g13((1,4,9,16,25),12),(3,4,5))
        self.assertEqual(solve_g13((1,4,9,16,25),12),(3,4,5))

    def test_large_linear_certified_output_and_domain(self):
        n=3000
        a=tuple(4**i for i in range(n))
        h=n-1
        record={}
        witness=solve_g13(a,n*(n+1)//2-h,counters=record)
        self.assertEqual(len(witness),n-1)
        self.assertNotIn(h,witness)
        self.assertEqual(record["mode"],"G13_certificate")
        for a,m in (((0,True,3),6),((0,1,3),True),
                    ((0,1,3,5,10,20,40,80),24)):
            with self.assertRaises(ValueError):
                certify_g13(a,m)
            with self.assertRaises(ValueError):
                solve_g13(a,m)


if __name__=='__main__':
    unittest.main()
