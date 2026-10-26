#!/usr/bin/env python3
"""Prospectively registered G10 sparse/dense/G8 crossover, not a SOTA claim.

Raw observations include all losing cells, feasible/infeasible partitions, and
skips (none in these three comparison arms). Does not select best-of-both
adaptively or mix different Python hosts. Time measurements are observational.
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

from benchmarks.g10_rfp_comparative import expanded_cases
from experiments.v03.g10_direct_next import solve_g10
from experiments.v03.g10_sparse_experimental import solve_g10_sparse
from experiments.v03.g8_persistent_intervals import solve_g8

SEED = 20261026
SOLVERS = {"g8": solve_g8, "g10_dense": solve_g10,
           "g10_sparse": solve_g10_sparse}


def stats(pairs):
    ratios = [p["baseline_over_sparse"] for p in pairs]
    return {"n": len(ratios), "sparse_wins": sum(x > 1 for x in ratios),
            "sparse_losses": sum(x < 1 for x in ratios),
            "median_ratio": statistics.median(ratios) if ratios else None}


def measure(profile, repetitions):
    cases = list(expanded_cases(profile))
    schedule = [(idx, name) for idx in range(len(cases)) for name in SOLVERS]
    random.Random(SEED + 401).shuffle(schedule)
    values = {}
    rows = []
    for idx, name in schedule:
        c = cases[idx]
        a, m = c["a"], c["m"]
        run = SOLVERS[name]
        item = {"case_id": c["case_id"], "family": c["family"],
                "n": c["n"], "h": c["h"], "solver": name,
                "status": "PENDING", "samples_ns": []}
        try:
            run(a, m)
            for _ in range(repetitions):
                start = time.perf_counter_ns()
                answer = run(a, m)
                item["samples_ns"].append(time.perf_counter_ns() - start)
                if idx in values and answer != values[idx]:
                    raise AssertionError("whole canonical witness mismatch")
                values[idx] = answer
            item.update(status="PASS", feasible=bool(answer),
                        median_ns=statistics.median(item["samples_ns"]))
        except Exception as e:
            item.update(status="ERROR", reason=repr(e))
        rows.append(item)
    timings = {(r["case_id"], r["solver"]): r["median_ns"]
               for r in rows if r["status"] == "PASS"}
    feasible = {r["case_id"]: r["feasible"]
                for r in rows if r["solver"] == "g10_dense"
                and r["status"] == "PASS"}
    comparisons = {}
    for baseline in ("g8", "g10_dense"):
        pairs = []
        for c in cases:
            key = c["case_id"]
            b = timings.get((key, baseline))
            s = timings.get((key, "g10_sparse"))
            if b and s:
                pairs.append({"case_id": key, "family": c["family"],
                              "h": c["h"], "n": c["n"],
                              "feasible": feasible.get(key),
                              "baseline_over_sparse": b/s})
        comparisons[baseline] = {
            "all": stats(pairs),
            "feasible": stats([p for p in pairs if p["feasible"]]),
            "infeasible": stats([p for p in pairs if not p["feasible"]]),
            "pairs": pairs}
    root = Path(__file__).resolve().parents[1]
    source_paths = ("experiments/v03/g10_sparse_experimental.py",
                    "experiments/v03/g10_direct_next.py",
                    "experiments/v03/g8_persistent_intervals.py",
                    "benchmarks/g10_rfp_sparse_screen.py")
    hashes = {p: hashlib.sha256((root/p).read_bytes()).hexdigest()
              for p in source_paths}
    rev = subprocess.run(["git","rev-parse","HEAD"],cwd=root,
                         text=True,capture_output=True,check=False)
    return {"metadata": {"head": rev.stdout.strip(), "python": sys.version,
                         "platform": platform.platform(), "seed": SEED,
                         "profile": profile, "repetitions": repetitions,
                         "source_sha256": hashes, "case_count": len(cases),
                         "limitations": "same-process medians, no cross-host "
                         "replication or statistical intervals; no SOTA claim"},
            "rows": rows, "comparisons": comparisons,
            "errors": sum(row["status"] == "ERROR" for row in rows)}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--profile",choices=("smoke","ci","paper"),
                   default="smoke")
    p.add_argument("--repetitions",type=int,default=5)
    p.add_argument("--output",default="g10_rfp_sparse.json")
    args = p.parse_args()
    if args.repetitions < 1 or args.repetitions > 30:
        p.error("repetitions must be 1..30")
    report = measure(args.profile,args.repetitions)
    dest = Path(args.output)
    dest.write_text(json.dumps(report,indent=2,sort_keys=True) + "\n")
    compact = {k: {label: value for label,value in x.items() if label != "pairs"}
               for k,x in report["comparisons"].items()}
    print(json.dumps({"output":str(dest),"case_count":
                      report["metadata"]["case_count"],"errors":
                      report["errors"],"comparisons":compact},indent=2))
    return int(report["errors"] > 0)


if __name__ == "__main__":
    raise SystemExit(main())
