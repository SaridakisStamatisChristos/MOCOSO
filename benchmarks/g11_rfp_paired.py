#!/usr/bin/env python3
"""Paired end-to-end G11 vs corrected G8/G8 historical/G10 benchmark.

All cases and losses preserved. Intended as within-repository evidence, not
external SOTA or a statistically controlled multicore/host comparison.
"""
import argparse
import hashlib
import json
import platform
import random
import statistics
import subprocess
import sys
import time
from pathlib import Path

from experiments.v03.g11_hybrid import solve_g11
from experiments.v03.g11_bounded_g8 import solve_g8 as bounded_g8
from experiments.v03.g8_persistent_intervals import solve_g8 as original_g8
from experiments.v03.g10_direct_next import solve_g10

SEED=20261027
METHODS={"g11":solve_g11,"g8_corrected":bounded_g8,
         "g8_original":original_g8,"g10":solve_g10}
H_VALUES=(0,1,2,3,5,8,12,15,18,19,24,32,48,60,64,65,75,90,110)


def cases(profile):
    hs=(0,1,8,18,19,64,65,90) if profile=="smoke" else H_VALUES
    ns=(2,25) if profile=="smoke" else (2,25,300)
    for h in hs:
        for extra in ns:
            n=max(3,h+extra)
            U=n*(n+1)//2
            m=U-h
            for family in ("square","powers","suffix_fault"):
                if family=="square":
                    a=tuple(i*i for i in range(1,n+1))
                elif family=="powers":
                    a=tuple(4**i for i in range(n))
                else:
                    a=tuple(list(i*i for i in range(1,n))+[-1])
                label=f"h{h}_n{n}_{family}"
                yield {"id":label,"n":n,"h":h,"m":m,"a":a,
                       "family":family,"digest":hashlib.sha256(
                           json.dumps([a,m]).encode()).hexdigest()}


def aggregate(pairs):
    vals=[p["baseline_over_g11"] for p in pairs]
    return {"paired":len(vals),"g11_wins":sum(x>1 for x in vals),
            "g11_losses":sum(x<1 for x in vals),
            "median_paired_ratio":statistics.median(vals) if vals else None}


def bench(profile,reps):
    inputs=list(cases(profile))
    schedule=[(i,key) for i in range(len(inputs)) for key in METHODS]
    random.Random(SEED+61).shuffle(schedule)
    rows=[]
    outputs={}
    for ix,key in schedule:
        case=inputs[ix]
        a,m=case["a"],case["m"]
        solver=METHODS[key]
        item={"case_id":case["id"],"method":key,"samples_ns":[],
              "status":"PENDING"}
        try:
            solver(a,m)
            for _ in range(reps):
                t=time.perf_counter_ns()
                result=solver(a,m)
                item["samples_ns"].append(time.perf_counter_ns()-t)
                if ix in outputs and result!=outputs[ix]:
                    raise AssertionError("whole canonical witness mismatch")
                outputs[ix]=result
            item.update(status="PASS",
                        median_ns=statistics.median(item["samples_ns"]),
                        feasible=bool(result))
        except Exception as exc:
            item.update(status="ERROR",reason=repr(exc))
        rows.append(item)
    lookup={(r["case_id"],r["method"]):r for r in rows
            if r["status"]=="PASS"}
    comparisons={}
    for other in ("g8_corrected","g8_original","g10"):
        pairs=[]
        for c in inputs:
            key=c["id"]
            first=lookup.get((key,"g11"))
            alt=lookup.get((key,other))
            if first is None or alt is None:
                continue
            pairs.append({"case_id":key,"h":c["h"],
                          "family":c["family"],"feasible":first["feasible"],
                          "baseline_over_g11":
                          alt["median_ns"]/first["median_ns"]})
        comparisons[other]={"overall":aggregate(pairs),
            "feasible":aggregate([p for p in pairs if p["feasible"]]),
            "infeasible":aggregate([p for p in pairs if not p["feasible"]]),
            "h_le_18":aggregate([p for p in pairs if p["h"]<=18]),
            "h_19_to_64":aggregate([p for p in pairs if 19<=p["h"]<=64]),
            "h_ge_65":aggregate([p for p in pairs if p["h"]>=65]),
            "pairs":pairs}
    root=Path(__file__).resolve().parents[1]
    files=("experiments/v03/g11_hybrid.py",
           "experiments/v03/g11_bounded_g8.py",
           "experiments/v03/g8_persistent_intervals.py",
           "experiments/v03/g10_direct_next.py",
           "benchmarks/g11_rfp_paired.py")
    sources={f:hashlib.sha256((root/f).read_bytes()).hexdigest() for f in files}
    revision=subprocess.run(["git","rev-parse","HEAD"],cwd=root,
                            capture_output=True,text=True)
    return {"metadata":{"seed":SEED,"head":revision.stdout.strip(),
            "profile":profile,"repeats":reps,"case_count":len(inputs),
            "python":sys.version,"platform":platform.platform(),
            "source_sha256":sources,
            "limits":"single-runner exploratory end-to-end medians, no "
            "significance or external SOTA claim"},
            "rows":rows,"comparisons":comparisons,
            "cases":[{k:(list(v) if k=="a" else v)
                     for k,v in c.items()} for c in inputs],
            "errors":sum(r["status"]=="ERROR" for r in rows)}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--profile",choices=("smoke","paper"),default="smoke")
    parser.add_argument("--repeats",type=int,default=5)
    parser.add_argument("--output",default="g11_rfp_results.json")
    args=parser.parse_args()
    if not 1<=args.repeats<=30:
        parser.error("repeats must be 1..30")
    out=bench(args.profile,args.repeats)
    Path(args.output).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",
                                 encoding="utf-8")
    print(json.dumps({"path":args.output,"errors":out["errors"],
          "cases":out["metadata"]["case_count"],
          "comparisons":{k:{w:v for w,v in d.items() if w!="pairs"}
                         for k,d in out["comparisons"].items()}},indent=2))
    return int(out["errors"]!=0)


if __name__=="__main__":
    raise SystemExit(main())
