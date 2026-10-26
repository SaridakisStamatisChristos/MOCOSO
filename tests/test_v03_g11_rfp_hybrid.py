"""Independent full-witness oracle and boundary gates for G11 hybrid.

No source import from the candidate is used by the selected-subset oracle.
Historical G8/G10 originals are not edited.
"""
import ast
from itertools import product
from pathlib import Path
from random import Random
import unittest

from experiments.v03.g11_hybrid import solve_direct, solve_g11
from experiments.v03.g11_bounded_g8 import solve_g8 as bounded_g8
from experiments.v03.g8_persistent_intervals import solve_g8 as historical_g8
from experiments.v03.g10_direct_next import solve_g10


def independent_reference(a,m):
    """Independently enumerate all selected bitmasks, not omission paths."""
    n=len(a)
    best=()
    for mask in range(1,1<<n):
        selected=tuple(i+1 for i in range(n) if mask >> i & 1)
        if sum(selected)%m:
            continue
        if any(a[selected[k]-1]+a[selected[k+2]-1]<=
               2*a[selected[k+1]-1]
               for k in range(len(selected)-2)):
            continue
        if len(selected)>len(best) or (
                len(selected)==len(best) and selected<best):
            best=selected
    return best


class G11HybridGates(unittest.TestCase):
    def test_73809_exhaustive_subset_oracle(self):
        count=0
        for n in range(2,9):
            U=n*(n+1)//2
            for a in product((-3,0,2),repeat=n):
                for h in range(n):
                    m=U-h
                    if m<2 or 2*m<=U:
                        continue
                    self.assertEqual(solve_g11(a,m),independent_reference(a,m),
                                     (n,h,a))
                    count+=1
        self.assertEqual(count,73809)

    def test_1500_signed_differential(self):
        rng=Random(221009)
        alphabet=(-10**110,-100,-5,0,1,3,10,10**110)
        for trial in range(1500):
            n=rng.randrange(2,126)
            h=rng.randrange(n)
            U=n*(n+1)//2
            a=tuple(rng.choice(alphabet) for _ in range(n))
            self.assertEqual(solve_g11(a,U-h),solve_g10(a,U-h),
                             (trial,n,h))

    def test_dispatch_boundaries_and_forced_omissions(self):
        for h in (0,1,18,19,63,64,65,66,90,110):
            n=max(h+20,24)
            U=n*(n+1)//2
            for kind in ("square","powers","infeasible"):
                a=tuple((i*i if kind=="square" else 4**i
                         if kind=="powers" else 0) for i in range(n))
                counters={}
                got=solve_g11(a,U-h,counters=counters)
                want=solve_g10(a,U-h)
                self.assertEqual(got,want,(n,h,kind))
                expected=("direct" if h<=18 else
                          "g8_bounded" if h<=64 else "g10")
                self.assertEqual(counters["mode"],expected)
        for omissions in (1,2,3,5,7,9,11):
            h=omissions*(omissions+1)//2
            n=h+15
            a=tuple([-10**200]*omissions+[4**i for i in range(omissions,n)])
            U=n*(n+1)//2
            self.assertEqual(solve_g11(a,U-h),
                             tuple(range(omissions+1,n+1)))

    def test_bounded_g8_original_equivalence(self):
        rng=Random(20261027)
        for j in range(700):
            h=rng.randint(19,64)
            n=h+rng.randint(1,35)
            U=n*(n+1)//2
            kind=j%3
            a=(tuple(4**i for i in range(n)) if kind==0 else
               tuple(i*i for i in range(n)) if kind==1 else
               tuple(rng.randint(-1000,1000) for _ in range(n)))
            self.assertEqual(bounded_g8(a,U-h),
                             historical_g8(a,U-h),(j,n,h))

    def test_zero_deficit_large_return_without_linear_slices(self):
        n=40000
        a=tuple(i*i for i in range(n))
        self.assertEqual(solve_g11(a,n*(n+1)//2),
                         tuple(range(1,n+1)))
        path=Path(__file__).resolve().parents[1]/"experiments/v03/g11_bounded_g8.py"
        syntax=ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(syntax):
            if isinstance(node,ast.Subscript) and isinstance(node.value,ast.Name):
                self.assertFalse(node.value.id=="selected" and
                                 isinstance(node.slice,ast.Slice))

    def test_domain(self):
        for a,m in (((0,True,3),6),((0,1,3),True),
                    ((0,1,3,5,10,20,40,80),24)):
            with self.assertRaises(ValueError):
                solve_g11(a,m)
        with self.assertRaises(ValueError):
            solve_direct(tuple(range(100)),5050-19)


if __name__=="__main__":
    unittest.main()
