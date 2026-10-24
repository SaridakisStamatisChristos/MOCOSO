"""G6 independent finite-evidence adjudicator, independent of G4/G5 auditor code.

Reads exactly archived bytes on the independent G5 evidence-archive branch,
rechecks SHA256, count/plan provenance, per-cell times, full signed-convex
witness semantics, small-instance optimality, frozen-source fingerprints and
cross-run replay equality. It does NOT derive new theorem proofs or priority.

Exit nonzero on any material contradiction. No MOCOSO solver imports.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import io
import json
from pathlib import Path
import statistics
import zipfile

ORIGINAL_HEAD = "a6abd7459f9150a1342e35408d1cc735470c35bc"
SOURCES = {
    "paper_ubuntu": ("2c8f962abedcb59c630b145ff6d3f981069accf706fcc204e310b442c73dd175",146,2044,1616,428),
    "paper_windows": ("432d9533b0db6a49158bfb3d3d35564f63e8d709957109229fbcd89d1e8d6b61",146,2044,1616,428),
    "targeted_ubuntu": ("5051ac65321107385ceb8b5c7d2eaba25690e90cd8b73594b13895098634f3cb",40,320,256,64),
    "targeted_windows": ("e37b09670bb518863d3310c7350c5521aa251df18f5313e47848924841e29a18",40,320,256,64),
}
def sha(raw): return hashlib.sha256(raw).hexdigest()
def canonical(value):
    return sha(json.dumps(value, sort_keys=True, separators=(",",":")).encode())
def admissible(a,m,w):
    return (all(type(x) is int and 1<=x<=len(a) for x in w)
            and all(x<y for x,y in zip(w,w[1:]))
            and sum(w)%m==0
            and all(a[x-1]+a[z-1]>2*a[y-1]
                    for x,y,z in zip(w,w[1:],w[2:])))

def complete_oracle(a,m):
    best=()
    for mask in range(1<<len(a)):
        candidate=tuple(j+1 for j in range(len(a)) if mask & (1<<j))
        if admissible(a,m,candidate) and (len(candidate)>len(best) or
           (len(candidate)==len(best) and candidate<best)):
            best=candidate
    return best

def max_witness_in_superconvex(a,m):
    """Independent min-omission cardinality DP for high moduli only."""
    n=len(a); U=n*(n+1)//2; h=U-m
    if not (U<2*m<=2*U and a==[3**i for i in range(n)]):
        return None
    dp={0:()}
    for j in range(1,min(n,h)+1):
        nxt=dict(dp)
        for total,omit in dp.items():
            s=total+j
            if s>h: continue
            cand=omit+(j,)
            old=nxt.get(s)
            if old is None or len(cand)<len(old) or (len(cand)==len(old) and cand>old):
                nxt[s]=cand
        dp=nxt
    best_omit=dp.get(h)
    if best_omit is None: return ()
    skipped=set(best_omit)
    return tuple(j for j in range(1,n+1) if j not in skipped)

def read_original(raw_archive, group):
    with zipfile.ZipFile(io.BytesIO(raw_archive)) as z:
        assert z.testzip() is None
        assert len(z.namelist())==len(set(z.namelist()))
        original=json.loads(z.read("g4_"+group+"_raw.json"))
        plan=json.loads(z.read("g4_"+group+"_plan.json"))
    return original,plan

def inspect_report(report, *, expected, old=None, check_plan=True):
    cases=report["cases"]; case_map={c["case_id"]:c for c in cases}
    plan=report["plan"]; rows=report["rows"]
    assert report["complete"] and len(case_map)==len(cases)
    assert len(rows)==len(plan)
    assert report["workload_sha256"]==canonical(cases)
    assert report["plan_sha256"]==canonical(plan)
    assert len({(j["case_id"],j["algorithm"],j["block"]) for j in plan})==len(plan)
    assert report["provenance"]["frozen_source_gate"]=="PASS"
    status=Counter(x["status"] for x in rows)
    if expected:
        n,entries,ok,skips=expected
        assert (len(cases),len(rows),status["OK"],status["SKIPPED"])==(n,entries,ok,skips)
    assert sum(status.values())==len(plan) and not any(
        status[x] for x in ("ERROR","MISMATCH","UNVERIFIED","TIMEOUT","RESOURCE_LIMIT"))
    assert dict(status)==report["summary"]["status_counts"]
    obtained={}
    for cell,row in zip(plan,rows):
        assert (cell["case_id"],cell["algorithm"],cell["block"])==(
            row["case_id"],row["algorithm"],row["block"])
        case=case_map[row["case_id"]]
        if row["status"]=="SKIPPED":
            assert cell["skip_reason"] is not None
            continue
        assert row["status"]=="OK" and cell["skip_reason"] is None
        w=tuple(row["witness"]); assert admissible(case["a"],case["m"],w)
        samples=row["runtime_ns"]
        assert len(samples)==report["repetitions"] and all(type(s) is int and s>0 for s in samples)
        assert row["median_ns"]==statistics.median(samples)
        assert row["min_ns"]==min(samples) and row["max_ns"]==max(samples)
        assert row["mad_ns"]==statistics.median(abs(s-row["median_ns"]) for s in samples)
        k=cell["case_id"]
        if k in obtained: assert obtained[k]==w,("within-report disagreement",k)
        obtained[k]=w
    # Separate from producer's recorded expected witnesses, recompute all
    # small exact cases and high-modulus powers-of-3 class where applicable.
    oracles=0; analytic=0
    for c in cases:
        k=c["case_id"]; a=c["a"];m=c["m"]
        assert len(a)==c["n"] and type(m) is int and m>=2
        if "input_sha256" in c: assert c["input_sha256"]==canonical([a,m])
        if "content_hash" in c: assert c["content_hash"]==canonical({"a":a,"m":m})
        expect=None
        if len(a)<=12:
            expect=complete_oracle(a,m);oracles+=1
        elif a==[3**i for i in range(len(a))] and 2*m>len(a)*(len(a)+1):
            expect=max_witness_in_superconvex(a,m);analytic+=1
        if expect is not None and k in obtained:
            assert obtained[k]==expect,("fresh independent optimality disagreement",k)
    if old is not None:
        assert report["workload_sha256"]==old["workload_sha256"]
        assert report["provenance"]["file_sha256"]==old["provenance"]["file_sha256"]
        assert report["provenance"]["working_commit"]==ORIGINAL_HEAD
        assert report["blocks"]==1 and report["repetitions"]==2
    return {"cases":len(cases),"planned":len(rows),"statuses":dict(status),
            "direct_oracle_cases":oracles,"high_mod_superconvex_oracle_cases":analytic,
            "full_optima":{k:list(v) for k,v in obtained.items()},
            "inputs_sha256":report["workload_sha256"],
            "source_sha256":report["provenance"]["file_sha256"]}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--archive-dir",required=True)
    p.add_argument("--output",required=True)
    args=p.parse_args()
    base=Path(args.archive_dir)
    saved=json.loads((base/"G5/manifest_verified.json").read_text(encoding="utf8"))
    assert saved["result"]=="PASS"
    records={}
    original={}
    for name,(digest,n,total,ok,sk) in SOURCES.items():
        file=base/"G4"/(name+".zip")
        data=file.read_bytes()
        assert sha(data)==digest,("binary ZIP hash drift",name)
        group="paper" if name.startswith("paper") else "targeted"
        report,plan=read_original(data,group)
        assert plan["plan_sha256"]==report["plan_sha256"]
        assert plan["workload_sha256"]==report["workload_sha256"]
        a=inspect_report(report,expected=(n,total,ok,sk))
        a["archive_zip_sha256"]=digest
        records[name]=a
        original[name]=report
    replay={}
    for name in SOURCES:
        part=name.split("_"); kind,platform=part
        file=base/"G5"/("g5_"+kind+"_"+platform+".json")
        b=file.read_bytes()
        manifest=saved["fresh_replica"][kind+"_"+platform]
        assert sha(b)==manifest["sha256"],("manifest mismatch",name)
        report=json.loads(b)
        assert report["order_seed"]!=original[name]["order_seed"]
        a=inspect_report(report,expected=None,old=original[name])
        assert (a["cases"],a["planned"])==(
            len(original[name]["cases"]),len(original[name]["plan"])//2)
        assert a["full_optima"]==records[name]["full_optima"],("original vs replay witness",name)
        assert a["source_sha256"]==records[name]["source_sha256"]
        a["json_sha256"]=sha(b)
        replay[name]=a
    for prefix in ("paper","targeted"):
        u,w=(records[f"{prefix}_{os}"] for os in ("ubuntu","windows"))
        assert (u["inputs_sha256"],u["source_sha256"],u["full_optima"])==(
            w["inputs_sha256"],w["source_sha256"],w["full_optima"])
        u,w=(replay[f"{prefix}_{os}"] for os in ("ubuntu","windows"))
        assert (u["inputs_sha256"],u["source_sha256"],u["full_optima"])==(
            w["inputs_sha256"],w["source_sha256"],w["full_optima"])
    out={"verdict":"FINITE_REPLICATION_PASS","source":ORIGINAL_HEAD,
         "originals":{k:{x:y for x,y in a.items() if x not in ("full_optima","source_sha256")}
                      for k,a in records.items()},
         "replicas":{k:{x:y for x,y in a.items() if x not in ("full_optima","source_sha256")}
                     for k,a in replay.items()},
         "limitations":["Only finite cases; no formal proof",
          "Same GitHub-hosted service, not independently staffed external lab",
          "Prior art and scientific novelty cannot be established by tests",
          "No claim of speed dominance from clipped case selection",
          "Does not satisfy previously proposed 3x5 intensive measurements"]}
    Path(args.output).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"verdict":out["verdict"],
                      "original_statuses":{k:v["statuses"] for k,v in records.items()},
                      "replay_statuses":{k:v["statuses"] for k,v in replay.items()}},
                     sort_keys=True))
if __name__=="__main__":
    main()
