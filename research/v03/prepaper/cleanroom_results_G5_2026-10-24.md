# MOCOSO G5 — Independent clean-room reproducibility and durable evidence disposition

**Execution date:** 2026-10-24 UTC. **Owner:** separately invoked Trillion Developer++ / Conductor–ACO with evidence-assurance gates. **Scope:** numerical/computational reproduction and artifact provenance of frozen MOCOSO G4; **not** independent mathematical peer review, novelty priority, a formal proof assistant result, a claim of universal performance, or paper authorization.

## Immutable lineage and source contracts

| Role | Git SHA or ref |
|---|---|
| v0.2 production | `9cedac0d0f860564d5ee1a9064b01ef56ac2a764` |
| original T1/M1 research | `7595130fecb1a21dc8ca8823d9ee8d5d136af97a` |
| G3 research source | `53b2276c7ed450ba8c27adc0e1e02c1493b4e592` |
| **G4 source replayed from clean checkouts** | **`a6abd7459f9150a1342e35408d1cc735470c35bc`** |
| G4 original raw evidence run | [40058471851](https://github.com/SaridakisStamatisChristos/MOCOSO/actions/runs/40058471851) |
| G5 first run (three verified jobs, failed packaging path) | [40060372352](https://github.com/SaridakisStamatisChristos/MOCOSO/actions/runs/40060372352) |
| **G5 final successful run** | [40060653058](https://github.com/SaridakisStamatisChristos/MOCOSO/actions/runs/40060653058) |
| G5 verifier/workflow inspected in draft | [PR #9](https://github.com/SaridakisStamatisChristos/MOCOSO/pull/9), based on unmerged G4 PR #8 |
| Git-backed archive (separate unmerged branch) | [research/v03-g5-evidence-archive](https://github.com/SaridakisStamatisChristos/MOCOSO/tree/research/v03-g5-evidence-archive/research/v03/prepaper/archive) |

**Authority:** No upstream PR was merged; no production solver or existing T1/G3 algorithms were changed. G5 verifier and workflow are additive; archive is a separate branch, one commit ahead of G5's tested implementation head, containing only the original ZIPs and reproduced outputs (9 added files, no changes/deletions).

## Executed reproduction and genuine independence boundaries

The G5 workflow used fresh checkout directories in new native Ubuntu and Windows Actions workers. In both replay workers, the algorithm being reproduced was checked out at exactly G4 SHA `a6abd7459...`; checkout and original-file preservation checks passed. The verifier itself runs from a **separate G5 code checkout** and does not import the MOCOSO solvers, G4 benchmark summary calculation, or the G4 recomputation script.

G5 historical archive job re-fetched all four original GitHub artifact IDs as ZIP bytes, checked **exact byte SHA-256**, ZIP validity, all planned report cells, independent arithmetic feasibility of every returned witness, full-method lex-witness parity, timestamp arrays/medians/min/max/MAD, case/plan fingerprints and independently enumerated all selected subsets for the specified small-input subset of cases. Re-use of original expected-witness values was prohibited where the direct selected-subset oracle applies; larger non-superconvex cases retain agreement-only status, and analytical family witnesses have distinct finite controls from previous G4/G3 tests.

G5 new replay used **the same 146 M1-paper inputs and the same 40 targeted G4 inputs** with order-seed 9917 (different from G4's original order-seed 713), one fresh process block and two untraced repetitions per method/case cell. This exactly replays semantic outputs and sample sets, but does **not** claim identical timings or reproduce the paper proposal's more intensive 3-block/5-repetition configuration.

## Fresh reproduction results (from G5 CI and independent report)

| Runner | Cohort | Cases | Planned cells | Completed/OK | Registered skipped | MISMATCH, ERROR, TIMEOUT, UNVERIFIED |
|---|---|---:|---:|---:|---:|---:|
| Ubuntu | original M1 paper profile | 146 | 1,022 | 808 | 214 | **0** |
| Windows | original M1 paper profile | 146 | 1,022 | 808 | 214 | **0** |
| Ubuntu | G4 targeted four-way | 40 | 160 | 128 | 32 | **0** |
| Windows | G4 targeted four-way | 40 | 160 | 128 | 32 | **0** |
| **Total** | | same registered inputs on 2 OS | **2,364** | **1,872** | **492** | **0** |

The independent cross-validation job verified the entire replay against the original G4 per-input, per-algorithm **full optimal index tuples**, not merely lengths; original source file SHA hashes and workload hashes matched. Independent local inspection of both raw downloaded replay archives independently reproduced the same zero-drift result. These repeated samples are not independent new benchmark instances; they are different executions of the same registered cases.

## Original raw G4 evidence byte preservation

| Artifact / contents | Original GitHub ID | Verifier expected ZIP SHA256 |
|---|---:|---|
| 146-case Ubuntu | 12546253781 | `2c8f962abedcb59c630b145ff6d3f981069accf706fcc204e310b442c73dd175` |
| 146-case Windows | 12546566643 | `432d9533b0db6a49158bfb3d3d35564f63e8d709957109229fbcd89d1e8d6b61` |
| 40-case Ubuntu | 12546576206 | `5051ac65321107385ceb8b5c7d2eaba25690e90cd8b73594b13895098634f3cb` |
| 40-case Windows | 12546317881 | `e37b09670bb518863d3310c7350c5521aa251df18f5313e47848924841e29a18` |

All four ZIPs passed the G5 CI byte-level verifier. The G5 archived repository branch now stores **those original binary ZIPs**, plus all four fresh replay JSON reports and [`manifest_verified.json`](https://github.com/SaridakisStamatisChristos/MOCOSO/blob/research/v03-g5-evidence-archive/research/v03/prepaper/archive/G5/manifest_verified.json), which records exact source revisions, per-report hashes and all evidence statuses. This preserves raw data in Git history while that ref is retained, rather than solely in expiring Actions temporary artifacts. No assertion that GitHub cannot delete or alter a branch is made.

## Preserved failed-first-attempt / causal repair

The initial G5 run [40060372352](https://github.com/SaridakisStamatisChristos/MOCOSO/actions/runs/40060372352) had **three successful upstream jobs** — original-G4 artifact verification, fresh Ubuntu replay and fresh Windows replay — but its final cross-validation/archive job failed **before comparison** because the Actions downloader nested the original report `replay/` directory within another `replay/` directory. The failure explicitly reported `missing replay report collected/replay/g5_paper_ubuntu.json`. This was a path-of-extraction bug, not an algorithm or source mismatch. Repair commit `2b15620f63d853add2efe1a563790a204c3b0989` altered only the two downloader destinations to `collected`, leaving the downloaded `replay/` prefix unchanged.

The completely fresh follow-up run [40060653058](https://github.com/SaridakisStamatisChristos/MOCOSO/actions/runs/40060653058) passed **all four G5 jobs**, including independent cross-validation and successful write to the separate unmerged archive branch. Preserve the failed attempt as causal evidence; don't erase it from the report.

## Independent assurance judgment

| Obligation | Disposition |
|---|---|
| Verify original G4 ZIP hashes and report integrity | **PASS** |
| Reproduce all original 146 paper cases on a pinned fresh native Linux and Windows checkout | **PASS**, 1 block x2 repetitions |
| Reproduce all G4 targeted 40 cases including independent generic forward DAG control | **PASS**, 1 block x2 repetitions |
| Verify complete optimal tuple equality, original source hashes, and input/plan fingerprints | **PASS**, within finite declared domains |
| Preserve both original and replay raw evidence beyond Actions ZIP expiry | **PASS** while unmerged archive Git ref remains, raw files committed and branch directly confirmed |
| Reproduce original M1 proposal's intensive paper configuration (3 blocks x5 reps) | **NOT DONE**; current G4 used 2x3 and G5 replay 1x2 |
| Fully independent theorem proof, external independent physical lab, or external paper referee | **NOT CLAIMED**; prior G2/G3 proof scope and limits remain |
| Prove algorithm originality / global SOTA performance / hard memory limits | **NOT CLEARED** by G1/G2/G3/G4/G5 |
| Final publication manuscript GO | **RESERVED for independently invoked G6 SOTA Research Auditor** |

**G5 disposition: PASS — bounded source, numerical and artifact reproducibility with explicit limitations.** This certifies the finite source revision and experiment family, not mathematical originality, new-complexity priority or publication readiness. The independent G6 reviewer should inspect this result and G1's substantive prior-art warning, and treat the missing intensive 3x5 comparison and optimized constrained-path prior-art baseline as still open.

## Reuse instructions

- Browse [Git-backed archived binary ZIPs](https://github.com/SaridakisStamatisChristos/MOCOSO/tree/research/v03-g5-evidence-archive/research/v03/prepaper/archive/G4), [fresh native replay reports](https://github.com/SaridakisStamatisChristos/MOCOSO/tree/research/v03-g5-evidence-archive/research/v03/prepaper/archive/G5) and their machine-readable verification manifest.
- Run G5 independent audit from PR #9 as `python research/v03/prepaper/g5_independent_audit.py --archives originals --replica replay --output g5_independent_final.json`, where `originals/` contains the four original ZIP file names defined in the script and `replay/` contains the four original G5 replay JSON file names.
- For a new full checkout run, follow the pinned workflow [v03-g5-cleanroom.yml](https://github.com/SaridakisStamatisChristos/MOCOSO/blob/research/v03-g5-cleanroom-repro/.github/workflows/v03-g5-cleanroom.yml). Do not expect equal wall times across environments.
