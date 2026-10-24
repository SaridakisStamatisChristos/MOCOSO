"""G3 preregistered exploratory benchmark: polynomial DP vs frozen T1 DFS.

Times are *observations*, not guarantees. Cases include both positive-optimum
and typically empty-optimum families, fixed before CI run. No post-hoc filtering.
Comparisons require identical inputs, exact optimal tuples, and full completion.
"""
import argparse
import json
import platform
import statistics
import sys
import time

from experiments.v03.deficit import solve_deficit
from experiments.v03.poly_deficit import solve_poly_deficit

SEED = 20261024
CASES = (
    (12, 4),
    (25, 15),
    (40, 25),
    (60, 40),
    (75, 50),
    (90, 60),
    (1000, 4),
)
FAMILIES = ("superconvex", "alternating")


def make_values(n, family):
    if family == "superconvex":
        return [3**i for i in range(n)]
    if family == "alternating":
        return [(-1)**i * (i % 7) for i in range(n)]
    raise AssertionError(family)


def run(profile, repetitions):
    if repetitions < 1:
        raise ValueError("repetitions must be positive")
    cases = CASES if profile == "ci" else CASES + ((110, 75),)
    output = []
    for n, h in cases:
        U = n * (n + 1) // 2
        m = U - h
        for family in FAMILIES:
            a = make_values(n, family)
            rec = {
                "n": n, "h": h, "m": m, "family": family,
                "repetitions": repetitions, "bits_max": max(abs(x).bit_length() for x in a),
                "results": {},
            }
            witness = None
            for name, solver in (("T1-dfs", solve_deficit),
                                 ("G3-poly", solve_poly_deficit)):
                trials = []
                for rep in range(repetitions):
                    before = time.perf_counter_ns()
                    result = solver(a, m)
                    elapsed = time.perf_counter_ns() - before
                    if result.status != "OPTIMAL":
                        raise AssertionError((n, h, family, name, result.status))
                    if witness is not None and result.indices != witness:
                        raise AssertionError((n, h, family, name,
                                              "different witness", witness, result.indices))
                    witness = result.indices
                    trials.append(elapsed)
                rec["results"][name] = {
                    "elapsed_ns": trials, "median_ns": int(statistics.median(trials)),
                    "minimum_ns": min(trials), "maximum_ns": max(trials),
                }
            rec["optimal_length"] = len(witness)
            a_ns = rec["results"]["T1-dfs"]["median_ns"]
            b_ns = rec["results"]["G3-poly"]["median_ns"]
            rec["T1_over_G3_median_ratio"] = a_ns / b_ns if b_ns else None
            output.append(rec)
            print(json.dumps({"case":rec}, sort_keys=True), flush=True)
    print(json.dumps({"summary": {
        "profile": profile, "seed": SEED, "case_count": len(output),
        "repetitions": repetitions, "python": sys.version,
        "platform": platform.platform(),
        "results": output
    }}, sort_keys=True), flush=True)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--profile", choices=("ci", "extended"), default="ci")
    p.add_argument("--repetitions", type=int, default=2)
    args = p.parse_args()
    run(args.profile, args.repetitions)
