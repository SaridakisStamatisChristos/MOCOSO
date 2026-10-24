"""G5 independent artifact validator. Does not import MOCOSO solvers, G4 harness,
benchmark summaries, or G4 recomputation script.

Accepts four ORIGINAL artifact ZIPs fetched by artifact ID, compares GitHub
ZIP SHA-256, independently validates plan/row bijection, checks complete
witnesses and finite complete selected-subset oracles, recomputes basic summary,
and compares each native OS's input and exact output ledger. Optionally
compares a fresh single-block replay against the same original raw reports.

Finite verification, not a mathematical proof or independent performance oracle.
"""
from __future__ import annotations
import argparse, collections, hashlib, io, json, pathlib, statistics, zipfile

EXPECTED = {
    "paper_ubuntu.zip": ("2c8f962abedcb59c630b145ff6d3f981069accf706fcc204e310b442c73dd175", 146, 2044, 1616, 428),
    "paper_windows.zip": ("432d9533b0db6a49158bfb3d3d35564f63e8d709957109229fbcd89d1e8d6b61", 146, 2044, 1616, 428),
    "targeted_ubuntu.zip": ("5051ac65321107385ceb8b5c7d2eaba25690e90cd8b73594b13895098634f3cb", 40, 320, 256, 64),
    "targeted_windows.zip": ("e37b09670bb518863d3310c7350c5521aa251df18f5313e47848924841e29a18", 40, 320, 256, 64),
}
def canon(x):
    return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def feasible(a,m,w):
    return (all(type(i) is int and 1<=i<=len(a) for i in w)
            and all(i<j for i,j in zip(w,w[1:])) and
            sum(w)%m==0 and
            all(a[i-1]+a[k-1]>2*a[j-1] for i,j,k in zip(w,w[1:],w[2:])))
def oracle(a,m):
    best=()
    for mask in range(1<<len(a)):
        w=tuple(i+1 for i in range(len(a)) if mask>>i&1)
        if feasible(a,m,w) and (len(w)>len(best) or
                (len(w)==len(best) and w<best)):
            best=w
    return best

def extract(zpath,name):
    with zipfile.ZipFile(zpath) as z:
        assert z.testzip() is None, ("damaged_zip",str(zpath))
        # Strict no member path traversal, duplicate paths or nested dirs.
        members=z.namelist()
        assert len(members)==len(set(members)) and all("/" not in p and
                "\\" not in p and p.endswith((".json",".txt",".log")) for p in members)
        raw=json.loads(z.read("g4_%s_raw.json"%name))
        plan=json.loads(z.read("g4_%s_plan.json"%name))
        summ=json.loads(z.read("g4_%s_summary.json"%name))
        return raw,plan,summ

def audit(report,planfile,summaryfile,expect=None):
    cases=report["cases"]
    plan=report["plan"]
    rows=report["rows"]
    bycase={c["case_id"]:c for c in cases}
    assert len(bycase)==len(cases)
    assert report["complete"] and report["workload_sha256"]==canon(cases)
    assert report["plan_sha256"]==canon(plan)
    assert planfile["plan_sha256"]==report["plan_sha256"]
    assert planfile["workload_sha256"]==report["workload_sha256"]
    assert len(planfile["plan"])==len(plan)
    assert len(rows)==len(plan)
    assert [x["execution_index"] for x in rows]==list(range(len(rows)))
    assert len({(x["case_id"],x["algorithm"],x["block"]) for x in rows})==len(rows)
    for job,row in zip(plan,rows):
        assert all(job[k]==row[k] for k in ("case_id","algorithm","block"))
        assert job["case_id"] in bycase
        if job.get("skip_reason"):
            assert row["status"]=="SKIPPED"
            assert row.get("reason")
        else:
            assert row["status"] in ("OK","TIMEOUT","RESOURCE_LIMIT","ERROR","MISMATCH","UNVERIFIED","SKIPPED")
    counts=collections.Counter(r["status"] for r in rows)
    if expect is not None:
        _,nc,nrows,ok,sk=expect
        assert len(cases)==nc and len(rows)==nrows
        assert counts=={"OK":ok,"SKIPPED":sk},counts
    assert report["summary"]["status_counts"]==dict(counts)
    # Recompute entire witness and timer integrity from raw entries, not copied
    # from producer's summary or own algorithm.
    completed_witness={}
    for row in rows:
        if row["status"]!="OK":
            continue
        c=bycase[row["case_id"]]
        w=tuple(row["witness"])
        assert feasible(c["a"],c["m"],w),(c["case_id"],row["algorithm"])
        times=row["runtime_ns"]
        assert len(times)==report["repetitions"] and all(type(t) is int and t>0 for t in times)
        assert row["median_ns"]==statistics.median(times)
        assert row["min_ns"]==min(times) and row["max_ns"]==max(times)
        assert row["mad_ns"]==statistics.median(abs(t-row["median_ns"]) for t in times)
        key=c["case_id"]
        if key in completed_witness:
            assert completed_witness[key]==w,("different complete optimal witnesses",key)
        else:
            completed_witness[key]=w
    verified={}
    for cid,c in bycase.items():
        ref=report["references"].get(cid)
        assert ref is not None
        witness=tuple(ref["witness"]) if ref.get("witness") is not None else None
        if ref["kind"]=="all_selected_subsets":
            assert c["n"]<=12
            independently=oracle(c["a"],c["m"])
            assert independently==witness,("bad producer oracle",cid)
            verified[cid]="direct_selected_subset"
        elif ref["kind"]=="superconvex_index_sum_dp":
            # The claimed analytical class must actually be powers of three.
            assert c["a"]==[3**i for i in range(c["n"])],cid
            assert witness is not None and feasible(c["a"],c["m"],witness)
            # Full optimality against a distinct residue DP is covered by
            # the fresh cleanroom run, NOT pretended here.
            verified[cid]="analytical_class_reference_unreproved"
        else:
            assert ref["kind"]=="cross_algorithm_only" and witness is None
            verified[cid]="agreement_only"
        if witness is not None and cid in completed_witness:
            assert completed_witness[cid]==witness,("oracle_vs_solver",cid)
    # Validate input identities (stable across process blocks and OS).
    for c in cases:
        assert len(c["a"])==c["n"],c["case_id"]
        if "input_sha256" in c:
            assert c["input_sha256"]==canon([c["a"],c["m"]])
        if "content_hash" in c:
            assert c["content_hash"]==canon({"a":c["a"],"m":c["m"]})
    return dict(cases=len(cases),rows=len(rows),status_counts=dict(counts),
                independently_checked_cases=sum(x=="direct_selected_subset" for x in verified.values()),
                analytical_class_cases=sum(x=="analytical_class_reference_unreproved" for x in verified.values()),
                agreement_only_cases=sum(x=="agreement_only" for x in verified.values()),
                bycase_witness={k:list(v) for k,v in completed_witness.items()},
                plan_sha256=report["plan_sha256"],workload_sha256=report["workload_sha256"],
                source_hashes=report["provenance"]["file_sha256"],
                original_checkout=report["provenance"]["working_commit"])

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--archives",required=True)
    p.add_argument("--replica",default=None)
    p.add_argument("--output",required=True)
    args=p.parse_args()
    root=pathlib.Path(args.archives)
    records={}
    reports={}
    for name,expect in EXPECTED.items():
        path=root/name
        assert path.is_file(),("missing artifact",str(path))
        raw_bytes=path.read_bytes()
        digest=hashlib.sha256(raw_bytes).hexdigest()
        assert digest==expect[0],("zip digest mismatch",name,digest)
        cohort="paper" if name.startswith("paper") else "targeted"
        raw,plan,summ=extract(path,cohort)
        records[name]=audit(raw,plan,summ,expect)
        records[name]["zip_sha256"]=digest
        records[name]["artifact_size_bytes"]=len(raw_bytes)
        reports[name]=raw
    for label in ("paper","targeted"):
        u,w=(records[f"{label}_{os}.zip"] for os in ("ubuntu","windows"))
        assert (u["plan_sha256"],u["workload_sha256"],u["source_hashes"],u["bycase_witness"])==(
                w["plan_sha256"],w["workload_sha256"],w["source_hashes"],w["bycase_witness"]),label
    replicas={}
    if args.replica:
        d=pathlib.Path(args.replica)
        for label in ("paper","targeted"):
            for os in ("ubuntu","windows"):
                path=d/f"g5_{label}_{os}.json"
                assert path.is_file(),("missing replay report",str(path))
                rep=json.loads(path.read_text())
                # The G5 fresh run MUST have a separate checkout, fresh
                # process blocks and timings, but identical registered inputs.
                hist=reports[f"{label}_{os}.zip"]
                assert rep["workload_sha256"]==hist["workload_sha256"]
                assert rep["profile"]==hist["profile"]
                assert len(rep["cases"])==len(hist["cases"])
                assert rep["provenance"]["file_sha256"]==hist["provenance"]["file_sha256"]
                assert rep["provenance"]["working_commit"]=="a6abd7459f9150a1342e35408d1cc735470c35bc", ("not exact pinned G4 commit",rep["provenance"]["working_commit"])
                assert rep["complete"] and len(rep["rows"])==len(rep["plan"])
                assert rep["repetitions"]==2 and rep["blocks"]==1
                bycid={c["case_id"]:c for c in rep["cases"]}
                old_wit=records[f"{label}_{os}.zip"]["bycase_witness"]
                cnt=collections.Counter(r["status"] for r in rep["rows"])
                assert not any(cnt[x] for x in ("MISMATCH","ERROR","UNVERIFIED","TIMEOUT","RESOURCE_LIMIT"))
                for row in rep["rows"]:
                    if row["status"]=="OK":
                        witness=tuple(row["witness"])
                        case=bycid[row["case_id"]]
                        assert feasible(case["a"],case["m"],witness)
                        assert witness==tuple(old_wit[row["case_id"]]),("replay full witness drift",label,os,row["case_id"])
                replicas[f"{label}_{os}"]=dict(counts=dict(cnt),cases=len(rep["cases"]),
                            sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                            checkout=rep["provenance"]["working_commit"])
    out={"result":"PASS","historical":records,"fresh_replica":replicas,
         "limitations":["finite case verification","analytical-class independent optimality not fully re-proved here",
          "cross-algorithm agreement is not an independent oracle",
          "GitHub Actions clone is fresh runner not an external independent physical laboratory",
          "timing equality is not expected; output/plan equality is asserted",
          "unmerged research branches and no paper GO"]}
    pathlib.Path(args.output).write_text(json.dumps(out,sort_keys=True,indent=2)+"\n")
    print(json.dumps({"result":"PASS","historical":{
         n:{k:v for k,v in r.items() if k not in ("bycase_witness","source_hashes")}
         for n,r in records.items()},"replica":replicas},sort_keys=True))
if __name__=="__main__":
    main()
