"""Novelty/collision falsification of independently lifted 2013 edge algorithm.

Primary oracle enumerates selected tuples directly (not omissions or G3);
compares full index tuple, not only optimum length. This intentionally probes
whether existing algorithm ingredients obtain G3's time bound plus a smaller
working-space / slower reconstruction Pareto point.
"""
from itertools import product
import random
import unittest

from experiments.v03.edge_budget_lift import (best_length, solve_lex_by_recomputation,
    best_length_modular, solve_lex_modular_by_recomputation)
from experiments.v03.poly_deficit import solve_poly_deficit


def selected_subset_oracle(a,m):
    best = ()
    for mask in range(1 << len(a)):
        w=tuple(i+1 for i in range(len(a)) if mask & (1 << i))
        if sum(w) % m:
            continue
        if any(a[x-1]+a[z-1] <= 2*a[y-1]
               for x,y,z in zip(w,w[1:],w[2:])):
            continue
        if len(w)>len(best) or (len(w)==len(best) and w<best):
            best=w
    return best


class PriorEdgeResourceLift(unittest.TestCase):
    def test_full_cartesian_small_signed(self):
        count=0
        for n in range(2,8):
            U=n*(n+1)//2
            for a in product((-1,0,1),repeat=n):
                for m in range(U//2+1,U+1):
                    ref=selected_subset_oracle(a,m)
                    self.assertEqual(best_length(a,m),len(ref),(n,a,m))
                    self.assertEqual(solve_lex_by_recomputation(a,m),ref,
                                     (n,a,m))
                    count+=1
        self.assertEqual(count,41085)

    def test_big_signed_random_full_tuple(self):
        rng=random.Random(20261024)
        for _ in range(650):
            n=rng.randrange(2,11)
            a=[rng.choice((-10**160,-10**90,-1,0,0,1,
                           10**90,10**160)) for _ in range(n)]
            U=n*(n+1)//2
            m=rng.randrange(U//2+1,U+1)
            ref=selected_subset_oracle(a,m)
            self.assertEqual(solve_lex_by_recomputation(a,m),ref)
            self.assertEqual(best_length(a,m),len(ref))
            self.assertEqual(solve_poly_deficit(a,m).indices,ref)

    def test_g3_positive_large_and_suffix_no(self):
        for n,h in ((2,0),(2,1),(12,4),(25,15),(40,25),
                    (60,40),(75,50),(90,60),(1000,4)):
            a=[3**i for i in range(n)]
            m=n*(n+1)//2-h
            got=solve_lex_by_recomputation(a,m)
            self.assertEqual(got,solve_poly_deficit(a,m).indices,(n,h))
            self.assertEqual(len(got),best_length(a,m))
            if n>=10:
                a[-1]=-a[-1]
                self.assertEqual(solve_lex_by_recomputation(a,m),())
                self.assertEqual(best_length(a,m),0)

    def test_forced_selection_and_gap(self):
        for n in range(2,8):
            a=[(i-4)**2 for i in range(1,n+1)]
            U=n*(n+1)//2
            for m in range(U//2+1,U+1):
                ref=selected_subset_oracle(a,m)
                self.assertEqual(solve_lex_by_recomputation(a,m),ref)
                for i in range(1,n+1):
                    for include in (False,True):
                        allowable=[]
                        for mask in range(1<<n):
                            w=tuple(j+1 for j in range(n) if mask>>j & 1)
                            if (i in w) != include or sum(w)%m:
                                continue
                            if any(a[x-1]+a[z-1]<=2*a[y-1]
                                   for x,y,z in zip(w,w[1:],w[2:])):
                                continue
                            allowable.append(w)
                        expect=max(map(len,allowable),default=-1)
                        if not include and expect==-1:
                            # Empty selected tuple always permitted and omits i.
                            expect=0
                        actual=best_length(
                            a,m,must_select=(i,) if include else (),
                            must_omit=(i,) if not include else ())
                        self.assertEqual(actual,expect,(n,m,i,include))

    def test_domains(self):
        for m in (1,2,11,True):
            with self.assertRaises(ValueError):
                solve_lex_by_recomputation([1,3,9,27],m)
        for bad in (0,True,1.4):
            with self.assertRaises(ValueError):
                best_length([1,3,9,27],10,must_select=(bad,))


    def test_unrestricted_modulus_length_classical_lift(self):
        # Independent direct selected-index subset enumeration; includes
        # m near 2, m>U, tie cases, signed values and empty solutions.
        count=0
        for n in range(2,8):
            U=n*(n+1)//2
            for a in product((-1,0,1),repeat=n):
                for m in range(2,U+3):
                    ref=selected_subset_oracle(a,m)
                    self.assertEqual(best_length_modular(a,m),len(ref),(n,a,m))
                    count+=1
        self.assertEqual(count,84465)

    def test_unrestricted_modulus_full_lex_selfreduction(self):
        count=0
        for n in range(2,7):
            U=n*(n+1)//2
            for a in product((-1,0,1),repeat=n):
                for m in range(2,U+3):
                    ref=selected_subset_oracle(a,m)
                    self.assertEqual(
                        solve_lex_modular_by_recomputation(a,m),
                        ref,(n,a,m))
                    count+=1
        self.assertEqual(count,21042)


if __name__=="__main__":
    unittest.main()
