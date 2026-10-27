#!/usr/bin/env python3
"""RFP 240-case independent-distribution holdout, G8 vs G10 vs G11.

This distribution differs from G11's 171-case benchmark. It contains
60 feasible constructed witnesses plus 180 adversarial mixed witnesses/
failures. The fixed random seed is 734120; all losing cells are retained.
It is an *exploratory* single-host comparison, not world SOTA evidence.
"""
import argparse
import hashlib
import json
import platform
from pathlib import Path
from random import Random
from statistics import median
import subprocess
import sys
from time import perf_counter_ns

from experiments.v03.g11_hybrid import solve_g11
from experiments.v03.g11_bounded_g8 import solve_g8
from experiments.v03.g10_direct_next import solve_g10

SEED=734120
SOLVERS={"g8":solve_g8,"g10":solve_g10,"g11":solve_g11}


def cases():
    rng=Random(SEED)
    for h in (19,24,32,48,60,64,65,75,90,110):
        for n in (h+2,h+15,h+160):
            m=n*(n+1)//2-h
            for family in ("strict_random","nearconvex","quadratic_jitter",
                           "flat","random_signed","broken_end",
                           "feasible_one","feasible_many"):
                if family=="strict_random":
                    v=diff=0
                    a=[]
                    for i in range(n):
                        diff+=rng.randint(1,10)
                        v+=diff
                        a.append(v)
                elif family=="nearconvex":
                    a=[3*i*i for i in range(n)]
                    a[max(1,n//2)]+=rng.randrange(0,120)
                elif family=="quadratic_jitter":
                    a=[i*i+rng.randint(-max(0,i//5),max(0,i//5))
                       for i in range(n)]
                elif family=="flat":
                    a=[0]*n
                elif family=="random_signed":
                    a=[rng.randint(-100000,100000) for _ in range(n)]
                elif family=="broken_end":
                    a=[i*i for i in range(n)]
                    a[-1]=-a[-1]
                else:
                    if family=="feasible_one":
                        Q={h}
                    else:
                        k=1
                        while (k+1)*(k+2)//2<=h:
                            k+=1
                        Q=set(range(1,k))
                        Q.add(h-k*(k-1)//2)
                    a=[]
                    diff=value=0
                    for i in range(1,n+1):
                        if i in Q:
                            a.append(-10**9)
                        else:
                            diff+=rng.randint(1,8)
                            value+=diff
                            a.append(value)
                a=tuple(a)
                yield {"id":f"h{h}-n{n}-{family}","h":h,"n":n,
                       "m":m,"family":family,"a":a,
                       "sha256":hashlib.sha256(json.dumps([a,m]).encode()).hexdigest()}


def summarize(rows,filterfn):
    subset=[x for x in rows if filterfn(x)]
    ratio=[x["times_ns"]["g8"]/x["times_ns"]["g10"] for x in subset]
    other=[x["times_ns"]["g8"]/x["times_ns"]["g11"] for x in subset]
    return {"count":len(subset),"g8_faster_g10":sum(v<1 for v in ratio),
            "g10_faster_g8":sum(v>1 for v in ratio),
            "median_g8_over_g10":median(ratio) if ratio else None,
            "g11_faster_g8":sum(v>1 for v in other),
            "median_g8_over_g11":median(other) if other else None}


def run(repeats):
    collection=list(cases())
    rows=[]
    for c in collection:
        times={}
        answers={}
        for name,solver in SOLVERS.items():
            samples=[]
            solver(c["a"],c["m"])
            for _ in range(repeats):
                t=perf_counter_ns()
                value=solver(c["a"],c["m"])
                samples.append(perf_counter_ns()-t)
                if answers and value!=next(iter(answers.values())):
                    raise AssertionError("canonical full witness mismatch "+c["id"])
                answers[name]=value
            times[name]=median(samples)
        rows.append({k:v for k,v in c.items() if k!="a"} |
                    {"feasible":bool(answers["g10"]),"times_ns":times})
    groups={"all":lambda x:True,"h_19_64":lambda x:x["h"]<=64,
            "h_ge_65":lambda x:x["h"]>=65,
            "feasible":lambda x:x["feasible"],
            "mid_feasible":lambda x:x["feasible"] and x["h"]<=64,
            "infeasible":lambda x:not x["feasible"]}
    root=Path(__file__).resolve().parents[1]
    source_paths=("benchmarks/g11_rfp_holdout.py",
                  "experiments/v03/g11_hybrid.py",
                  "experiments/v03/g11_bounded_g8.py",
                  "experiments/v03/g10_direct_next.py")
    hashes={p:hashlib.sha256((root/p).read_bytes()).hexdigest()
            for p in source_paths}
    git=subprocess.run(["git","rev-parse","HEAD"],cwd=root,
                       capture_output=True,text=True)
    return {"meta":{"seed":SEED,"repeats":repeats,"case_count":len(rows),
                    "head":git.stdout.strip(),"python":sys.version,
                    "platform":platform.platform(),"sha256":hashes,
                    "limits":"single hosted runner, exploratory paired medians; "
                    "not an external SOTA or significance claim"},
            "summary":{name:summarize(rows,fn) for name,fn in groups.items()},
            "rows":rows}


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--repeats",type=int,default=5)
    p.add_argument("--output",default="g11_rfp_holdout.json")
    args=p.parse_args()
    if args.repeats<1 or args.repeats>30:
        p.error("repeats must be in 1..30")
    result=run(args.repeats)
    Path(args.output).write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",
                                 encoding="utf-8")
    print(json.dumps({"cases":result["meta"]["case_count"],
          "summary":result["summary"],"output":args.output},indent=2))
