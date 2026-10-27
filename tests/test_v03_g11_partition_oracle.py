"""Independent distinct-partition oracle for G11's non-direct branches.

Unlike G8/G10 event-DP this oracle enumerates *all omitted index sets* with
exact sum h and validates full selected triples directly (not core pruning).
The finite h<=65 boundary tests are small enough to enumerate exactly.
"""
from random import Random
import unittest

from experiments.v03.g11_hybrid import solve_g11


def omitted_partition_oracle(a,m):
    n=len(a)
    h=n*(n+1)//2-m
    best=None

    def search(remainder,minimum,omissions):
        nonlocal best
        if remainder==0:
            Q=tuple(omissions)
            if best is not None and (len(Q)>len(best) or
                    (len(Q)==len(best) and Q<=best)):
                return
            dropped=set(Q)
            prev2=prev1=None
            for i in range(1,n+1):
                if i in dropped:
                    continue
                if (prev2 is not None and
                        a[prev2-1]+a[i-1]<=2*a[prev1-1]):
                    return
                prev2,prev1=prev1,i
            best=Q
            return
        for i in range(minimum,remainder+1):
            omissions.append(i)
            search(remainder-i,i+1,omissions)
            omissions.pop()

    search(h,1,[])
    if best is None:
        return ()
    dropped=set(best)
    return tuple(i for i in range(1,n+1) if i not in dropped)


class G11NonDirectIndependent(unittest.TestCase):
    def test_56_exact_distinct_partition_cases_across_modes(self):
        count=0
        for h in (19,24,32,48,60,64,65):
            for n in (h+2,h+7):
                rng=Random(20261027+h+n)
                for family in ("powers","square","flat","random_jitter"):
                    a=(tuple(4**i for i in range(n)) if family=="powers" else
                       tuple(i*i for i in range(n)) if family=="square" else
                       (0,)*n if family=="flat" else
                       tuple(i*i+rng.randint(-i,i) for i in range(n)))
                    m=n*(n+1)//2-h
                    self.assertEqual(solve_g11(a,m),
                                     omitted_partition_oracle(a,m),
                                     (h,n,family))
                    count+=1
        self.assertEqual(count,56)


if __name__=="__main__":
    unittest.main()
