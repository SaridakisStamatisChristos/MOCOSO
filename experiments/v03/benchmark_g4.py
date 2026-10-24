"""G4 predeclared comparison using the unchanged M1 benchmark's measurement protocol.

Retains fresh subprocess per cell/block, warmup and traced measurement,
per-case full witness verification, timeout/skip records and input hashes.
This adapter does not modify the M1 harness, T1, G3 or production solver.

Compare T1, G3 polynomial DP, independent generic RC-DAG and public v0.2.
Outputs have the exact same modular-index/strict-convex/lex semantics.
"""
import json
import math
from pathlib import Path
import subprocess
import sys
import statistics

from experiments.v03 import benchmark_expanded as m1
from experiments.v03.generic_rc_dag import solve_generic_rc_dag
from experiments.v03.poly_deficit import solve_poly_deficit
from modconvex import dense_dp_payload_bytes

ROOT=Path(__file__).resolve().parents[2]
m1.VERSION = "G4-targeted-registered-v1"
m1.ALGORITHMS = ("deficit","g3_poly","rc_dag","v02_default")
m1.SOURCES = tuple(dict.fromkeys(tuple(m1.SOURCES)+(
    "experiments/v03/generic_rc_dag.py",
    "experiments/v03/poly_deficit.py",
    "experiments/v03/benchmark_g4.py",
    "tests/test_v03_g4.py",
)))
OLD_CALL=m1.call_algorithm
def g4_call(name, a, m):
    if name=="g3_poly":
        z=solve_poly_deficit(a,m)
        return z.status,z.indices,dict(states=z.state_cells,relaxations=z.relaxations)
    if name=="rc_dag":
        return "OPTIMAL",solve_generic_rc_dag(a,m,max_states=60000),{}
    return OLD_CALL(name,a,m)
m1.call_algorithm=g4_call

def skip(case,name):
    n,h,m=case["n"],case["h"],case["m"]
    q=min(n,h)
    p=min(n,q+2)
    cells=p*(p-1)//2*(h+1)
    if name=="rc_dag" and cells>60000:
        return "preregistered generic DAG state cap 60000; not an infeasible answer"
    if name=="g3_poly" and cells>1000000:
        return "preregistered G3 state cap 1000000"
    if name=="v02_default" and (
            n>25 or dense_dp_payload_bytes(n,m)>8*1024*1024):
        return "registered public v0.2 cap n>25 or payload>8MiB"
    return None
m1.skip_reason=skip

REGISTERED=(
    (12,4),(12,8),(20,12),(25,15),(30,20),
    (40,25),(60,40),(75,50),(90,60),(1000,4)
)
FAMILIES=("superconvex","prefix_spike","suffix_defect","alternating")

def registered_cases(profile,seed):
    if seed!=20261024:
        raise ValueError("G4 comparison workload seed pinned to 20261024")
    base=REGISTERED[:3] if profile=="smoke" else REGISTERED
    cases=[]
    for n,h in base:
        m=n*(n+1)//2-h
        assert 2*m>n*(n+1)//2 and m>=2
        for family in FAMILIES:
            if family=="superconvex":
                a=[3**i for i in range(n)]
            elif family=="prefix_spike":
                a=[3**i for i in range(n)]
                a[0]=3**(n+1)
            elif family=="suffix_defect":
                a=[3**i for i in range(n)]
                a[-1]=-a[-1]
            else:
                a=[(-1)**i*(i%7) for i in range(n)]
            cases.append(dict(
                case_id="g4-%s-n%d-h%d"%(family,n,h),
                family=family,cohort="g4_registered",
                n=n,m=m,h=h,a=a,seed=seed,
                content_hash=m1.canonical_hash(dict(a=a,m=m)),
            ))
    return cases
m1.build_cases=registered_cases

def independent_superconvex_oracle(a,m):
    """Separate selected-index optimization via min-cardinality omitted-set DP.

    For a_i=3^i every selected tuple is strictly convex; at fixed omission
    count, lexicographically largest omission tuple preserves the earliest
    selected indices, giving lexicographically smallest chosen complement.
    """
    n=len(a)
    if a!=[3**i for i in range(n)]:
        raise ValueError("not superconvex reference class")
    U=n*(n+1)//2
    h=U-m
    if not (0<=h and U<2*m):
        raise ValueError("not high modulus")
    states={0:()}
    for x in range(1,min(n,h)+1):
        nextstates=states.copy()
        for total,omissions in states.items():
            newtotal=total+x
            if newtotal>h:
                continue
            alt=omissions+(x,)
            old=nextstates.get(newtotal)
            if old is None or len(alt)<len(old) or (
                    len(alt)==len(old) and alt>old):
                nextstates[newtotal]=alt
        states=nextstates
    omit=states.get(h)
    return () if omit is None else tuple(
        i for i in range(1,n+1) if i not in set(omit))
m1.superconvex_oracle=independent_superconvex_oracle

def subprocess_cell(cfg,timeout):
    """M1 run_cell with this adapter as worker entrypoint, not old harness."""
    try:
        proc=subprocess.run(
            [sys.executable,str(Path(__file__).resolve()),"--worker"],
            input=json.dumps(cfg),capture_output=True,text=True,
            encoding="utf-8",cwd=ROOT,timeout=timeout)
    except subprocess.TimeoutExpired:
        return dict(status="TIMEOUT",timeout_seconds=timeout,
                    reason="entire fresh worker timed out")
    if proc.returncode:
        # A deliberately registered comparator cap counts as SKIPPED, never
        # as TIMEOUT, ERROR, RESOURCE_LIMIT=NO or a timing sample.
        if "MemoryError: generic comparator registered state cap" in proc.stderr:
            return dict(status="SKIPPED",reason="generic comparator cap")
        return dict(status="ERROR",returncode=proc.returncode,
                    stderr=proc.stderr[-3000:])
    try:
        out=json.loads(proc.stdout)
        if out["status"]=="OK":
            times=out["runtime_ns"]
            if (len(times)!=cfg["repetitions"]
                or any(type(t) is not int or t<=0 for t in times)
                or out["median_ns"]!=statistics.median(times)
                or not m1.valid_witness(cfg["a"],cfg["m"],out["witness"])):
                raise ValueError("worker measurement invalid")
        elif out["status"] not in ("RESOURCE_LIMIT","SKIPPED"):
            raise ValueError("unknown status")
        return out
    except (ValueError,KeyError,TypeError):
        return dict(status="ERROR",reason="malformed worker result",
                    stdout=proc.stdout[-3000:])
m1.run_cell=subprocess_cell

if __name__=="__main__":
    # The original robust M1 main remains unchanged; only the controlled
    # G4 algorithms, cases, skip policy, reference and worker are injected.
    raise SystemExit(m1.main())
