"""G4 independent comparator correctness tests. No G3/T1 feasibility helper."""
import itertools
import random
import unittest

from experiments.v03.generic_rc_dag import solve_generic_rc_dag
from experiments.v03.deficit import solve_deficit
from experiments.v03.poly_deficit import solve_poly_deficit

def direct_oracle(a, m):
    best=()
    for bits in range(1<<len(a)):
        s=tuple(i+1 for i in range(len(a)) if (bits>>i)&1)
        if sum(s)%m:
            continue
        if any(a[x-1]+a[z-1] <= 2*a[y-1]
               for x,y,z in zip(s,s[1:],s[2:])):
            continue
        if len(s)>len(best) or (len(s)==len(best) and s<best):
            best=s
    return best


class GenericResourceControl(unittest.TestCase):
    def test_small_exhaustive(self):
        count=0
        for n in range(2,7):
            U=n*(n+1)//2
            for a in itertools.product((-1,0,1),repeat=n):
                for m in range(U//2+1,U+1):
                    expected=direct_oracle(a,m)
                    generic=solve_generic_rc_dag(a,m)
                    self.assertEqual(generic,expected,(a,m))
                    count+=1
        self.assertEqual(count,10467)

    def test_random_signed_and_lex(self):
        rng=random.Random(20261024)
        for i in range(370):
            n=rng.randrange(2,12)
            a=[rng.choice((0,0,-10**120,-1,1,10**120))
               for _ in range(n)]
            U=n*(n+1)//2
            m=rng.randrange(U//2+1,U+1)
            expected=direct_oracle(a,m)
            actual=solve_generic_rc_dag(a,m)
            self.assertEqual(actual,expected,(a,m))
            if i%5==0:
                self.assertEqual(solve_deficit(a,m).indices,expected)
                self.assertEqual(solve_poly_deficit(a,m).indices,expected)

    def test_superconvex_positive_and_empty(self):
        for n,h in ((12,0),(12,8),(20,12),(30,20),(40,25),(55,35)):
            a=[3**i for i in range(n)]
            m=n*(n+1)//2-h
            actual=solve_generic_rc_dag(a,m)
            prior=solve_poly_deficit(a,m)
            self.assertEqual(actual,prior.indices)
            self.assertGreater(len(actual),0)
        for n,h in ((20,8),(30,20)):
            a=[0]*n
            m=n*(n+1)//2-h
            self.assertEqual(solve_generic_rc_dag(a,m),
                             solve_deficit(a,m).indices)

    def test_caps_and_domains(self):
        n,h=85,60
        a=[i*i for i in range(n)]
        m=n*(n+1)//2-h
        with self.assertRaises(MemoryError):
            solve_generic_rc_dag(a,m,max_states=10)
        for m in (1,2,n*(n+1)//2+1,True):
            with self.assertRaises(ValueError):
                solve_generic_rc_dag(a,m)
