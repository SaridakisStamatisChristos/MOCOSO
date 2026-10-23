"""Independent finite adversarial oracle for Theorem Foundry G2.

No import/use of repository feasibility predicate, enumeration DP, or theorem proof.
Checks the frozen research solver against a direct 2^n subset oracle, and
locality using a separately specified full vs restricted triple predicate.

This is finite falsification only, not formal proof.
"""
from __future__ import annotations
import hashlib
import itertools
import json
import os
from pathlib import Path
import platform
import random
import subprocess
import sys
import unittest

from experiments.v03.deficit import solve_deficit
from modconvex import solve as v02_solve
from edge_dp import solve_edge

ROOT = Path(__file__).resolve().parents[3]
SEED = 2601023
COUNTS = {"full_oracle": 0, "triple_locality": 0, "certificate": 0,
          "superconvex_dp": 0, "v02_reference": 0}

def feasible(a, m, ind):
    return (sum(ind) % m == 0 and
            all(a[ind[t-2]-1] + a[ind[t]-1] > 2*a[ind[t-1]-1]
                for t in range(2, len(ind))))

def objective_best(first, second):
    return (len(second) > len(first) or
            (len(second) == len(first) and second < first))

def full_oracle(a, m):
    result = ()
    n = len(a)
    for mask in range(1 << n):
        ind = tuple(j + 1 for j in range(n) if mask & (1 << j))
        if feasible(a, m, ind) and objective_best(result, ind):
            result = ind
    return result

def check_certificate(test, a, m, ans, opt, K=None):
    COUNTS["certificate"] += 1
    test.assertTrue(feasible(a, m, ans.indices), (a, m, ans))
    test.assertEqual(len(ans.indices), ans.lower_bound)
    test.assertLessEqual(ans.lower_bound, len(opt))
    test.assertGreaterEqual(ans.upper_bound, len(opt))
    test.assertLessEqual(ans.upper_bound, len(a))
    if ans.status == "OPTIMAL":
        test.assertIsNone(K)
        test.assertEqual((ans.indices, ans.length, ans.upper_bound),
                         (opt, len(opt), len(opt)))
    elif ans.status == "FEASIBLE":
        test.assertIsNotNone(K)
        test.assertGreaterEqual(len(ans.indices), K)
    elif ans.status == "INFEASIBLE":
        test.assertIsNotNone(K)
        test.assertGreater(K, len(opt))
    else:
        test.assertEqual(ans.status, "RESOURCE_LIMIT")

def superconvex_index_oracle(n, m):
    # O(n*m) states storing EXACT lex-best tuples for each sum residue;
    # independent of omission enumeration and the strict-convex solver.
    states = {0: ()}
    for idx in range(1, n + 1):
        nxt = states.copy()
        for rem, seq in states.items():
            key = (rem + idx) % m
            candidate = seq + (idx,)
            if key not in nxt or objective_best(nxt[key], candidate):
                nxt[key] = candidate
        states = nxt
    return states.get(0, ())

class IndependentG2(unittest.TestCase):
    def test_complement_and_crossing_triples(self):
        for n in range(2, 10):
            U = n*(n+1)//2
            for m in range(max(2, U//2+1), U+1):
                h, q = U-m, min(n,U-m)
                for omask in range(1 << n):
                    omit = tuple(i for i in range(1,n+1) if omask & (1 << (i-1)))
                    if sum(omit) != h:
                        continue
                    self.assertTrue(all(i <= q for i in omit))
                    selected = tuple(i for i in range(1,n+1) if i not in omit)
                    self.assertEqual(sum(selected),m)
                    self.assertEqual(selected[q-len(omit):] if False else
                                     tuple(i for i in selected if i>q),
                                     tuple(range(q+1,n+1)))
                    # Vary signed, duplicate, huge and alternating arrays.
                    for mode in range(5):
                        a = {
                            0: [(-1)**i * i for i in range(1,n+1)],
                            1: [0]*n,
                            2: [i*i for i in range(n)],
                            3: [10**120 * (-1)**i for i in range(n)],
                            4: [3**i for i in range(n)],
                        }[mode]
                        global_ok = all(a[selected[t-2]-1]+a[selected[t]-1] >
                                        2*a[selected[t-1]-1]
                                        for t in range(2,len(selected)))
                        local = tuple(i for i in selected if i <= min(n,q+2))
                        prefix_ok = all(a[local[t-2]-1]+a[local[t]-1] >
                                        2*a[local[t-1]-1]
                                        for t in range(2,len(local)))
                        suffix_ok = all(a[k-3] + a[k-1] > 2*a[k-2]
                                        for k in range(q+3,n+1))
                        self.assertEqual(global_ok, prefix_ok and suffix_ok,
                                         (n,m,omask,mode))
                        COUNTS["triple_locality"] += 1

    def test_independent_exhaustive_and_randomized(self):
        rng=random.Random(SEED)
        for n in range(2, 7):
            U=n*(n+1)//2
            for a in itertools.product((-2,0,3),repeat=n):
                for m in range(max(2,U//2+1),U+1):
                    opt=full_oracle(a,m)
                    ans=solve_deficit(a,m)
                    check_certificate(self,a,m,ans,opt)
                    COUNTS["full_oracle"]+=1
                    if COUNTS["full_oracle"]%101==0:
                        for K in (-1,0,1,len(opt),len(opt)+1,n+1):
                            check_certificate(self,a,m,solve_deficit(a,m,K=K),opt,K)
        for i in range(1100):
            n=rng.randrange(2,12)
            a=[rng.choice((-10**170,-9,-2,-1,0,0,0,3,8,10**170))
               +rng.randrange(-3,4) for _ in range(n)]
            U=n*(n+1)//2
            m=rng.randrange(max(2,U//2+1),U+1)
            opt=full_oracle(a,m)
            check_certificate(self,a,m,solve_deficit(a,m),opt)
            COUNTS["full_oracle"]+=1
            if i%20==0:
                v02=v02_solve(a,m).indices
                self.assertEqual(v02,opt,(n,a,m))
                COUNTS["v02_reference"]+=1
            if i%30==0:
                self.assertEqual(solve_edge(a,m),opt)
            if i%10==0:
                for K in (0,1,2,len(opt),len(opt)+1,n+1):
                    check_certificate(self,a,m,solve_deficit(a,m,K=K),opt,K)
                for budget in (0,1,2,5,12,24,100):
                    check_certificate(self,a,m,
                                      solve_deficit(a,m,max_operations=budget),opt)
                    check_certificate(self,a,m,
                                      solve_deficit(a,m,K=2,max_operations=budget),opt,2)

    def test_independent_superconvex_index_dp_and_limits(self):
        for n in (2,3,12,20,35):
            U=n*(n+1)//2
            for h in (0,1,2,5,12,24,40):
                m=U-h
                if m<2 or 2*m<=U: continue
                a=[3**i for i in range(n)]
                opt=superconvex_index_oracle(n,m)
                # all subsequences of 3**i are strictly convex:
                # 3^k-3^j > 3^j-3^i, k>j>i, by k>=j+1.
                ans=solve_deficit(a,m)
                check_certificate(self,a,m,ans,opt)
                COUNTS["superconvex_dp"]+=1
                for K in (1,len(opt),len(opt)+1):
                    check_certificate(self,a,m,solve_deficit(a,m,K=K),opt,K)

    def test_h0_zero_budget_and_non_domain(self):
        for n in (2,3,4,9,35):
            U=n*(n+1)//2
            a=[i*i for i in range(n)]
            ans=solve_deficit(a,U)
            opt=tuple(range(1,n+1)) if feasible(a,U,tuple(range(1,n+1))) else ()
            self.assertEqual(ans.indices,opt)
            self.assertEqual(ans.status,"OPTIMAL")
            for bud in (0,1):
                check_certificate(self,a,U,
                                  solve_deficit(a,U,max_operations=bud),opt)
        for n in (3,10):
            U=n*(n+1)//2
            a=[0]*n
            for m in (2,U+1):
                with self.assertRaises(ValueError):
                    solve_deficit(a,m)
        # Soft checks: failure only limits knowledge, never proves infeasibility.
        for n in (4,12):
            U=n*(n+1)//2; m=U-2
            a=[(-1)**i*(10**100) for i in range(n)]
            opt=full_oracle(a,m)
            for K in (None,1):
                for cap in (0,1):
                    check_certificate(self,a,m,
                         solve_deficit(a,m,K=K,max_heap_bytes=cap),opt,K)
                    check_certificate(self,a,m,
                         solve_deficit(a,m,K=K,max_seconds=0.0),opt,K)

if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(IndependentG2)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print("G2_INDEPENDENT_SUMMARY="+json.dumps({
        "counts":COUNTS,
        "python":sys.version,
        "platform":platform.platform(),
        "code_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "git_head":subprocess.run(["git","rev-parse","HEAD"],capture_output=True,
                                  text=True).stdout.strip(),
        "success":result.wasSuccessful()
    },sort_keys=True))
    raise SystemExit(0 if result.wasSuccessful() else 1)
