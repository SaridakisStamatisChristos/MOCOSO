# G0 evidence and decision register (append-only research ledger)

As of 2026-10-23, source head `7595130fecb1a21dc8ca8823d9ee8d5d136af97a`. Coordinator-prepared; **not** independent external review. Never rewrite historical artifacts; append future independently obtained findings with reviewer identity, date, exact commit and executed command.

## Evidence classes
- `VERIFIED_GIT`: directly retrieved immutable Git refs/comparisons/tree/source.
- `VERIFIED_CI_METADATA`: checked GitHub workflow/job or artifact metadata; does not assert raw results were independently inspected.
- `REPO_REPORTED`: assertion in committed prose/report, not reproduced in this gate.
- `FINITE_TEST`: historical executed test, not theorem proof.
- `HYPOTHESIS`: unreviewed theorem/originality statement.
- `NOT_VERIFIABLE`: requested verification has not been executed or material is inaccessible.
- `PENDING`: planned future result; do not imply PASS.

| ID | Claim or question | Source / lineage | Evidence class | Counterevidence or scope | Current disposition | Required gate/action |
|---|---|---|---|---|---|---|
| GIT-01 | Main v0.2 frozen at `9cedac0`; #2 and #3 open unmerged, stack 20+2 commits | GitHub refs, PR API, compare main..#2..#3, 2026-10-23 | VERIFIED_GIT | Can advance later; reconfirm before future write | SUPPORTED at snapshot | G5 pin/recheck |
| GIT-02 | PR2/#3 do not change `modconvex.py`, `edge_dp.py` or historical main files | Comparison file lists and Git blobs at `9cedac0`/`7595130` | VERIFIED_GIT | Diff audit covers these ref snapshots only | SUPPORTED | Maintain branch-only edits |
| ALG-C1 | Full modular index-sum strict convexity, global lex objective implemented by v0.2 | `modconvex.py`, `edge_dp.py`, `RESEARCH_REPORT.md`, historical exactness run 39991432942 | VERIFIED_GIT + FINITE_TEST + REPO_REPORTED | Finite tests are not universal proof or novelty | PARTIAL | Independent G2 reconstruction; G1 prior art |
| ALG-C2 | Correct backward sweep lex-optimal unrestricted solver and resource semantics | `modconvex.py`, `RELIABILITY_V02.md`, `tests/test_reliability.py`, CI exactness | REPO_REPORTED + FINITE_TEST | Check tie handling, correctness in mathematical/bit model, soft limits | PARTIAL | G2 |
| T1-C3 | High modulus complement correspondence | `research/v03/t1_deficit_proof.md`, `deficit.py` | HYPOTHESIS + FINITE_TEST | Could be classical reduction; zero/empty edge cases | UNRESOLVED as independently proved | G1 + G2 |
| T1-C4 | Immutable suffix locality for all crossing triples | Same theorem file, tests/test_v03_deficit.py | HYPOTHESIS + FINITE_TEST | Need independent proof of boundary triples for all q,n | UNRESOLVED | G2 |
| T1-C5 | Reachability-pruned distinct-part enumerator is sound, complete, nonduplicating | `deficit.py`, candidate theorem, finite falsification | HYPOTHESIS + FINITE_TEST | Charging argument/temporary memory; known subset-sum prior art | UNRESOLVED | G1 + G2 |
| T1-C6 | `O(n+qh+q P_d(h))` unit-word and `O(qh+q)` auxiliary words | Candidate theorem proof | HYPOTHESIS | Bit complexity, count all interpreter and allocation costs, output exclusion | UNRESOLVED | G2 |
| SEM-01 | Optimal complete lex tuple and threshold/resource certificates exact | `modconvex.py`, `deficit.py`, finite oracle tests | FINITE_TEST + REPO_REPORTED | `RESOURCE_LIMIT` cannot imply NO; budgets soft | PARTIAL | G2 |
| TEST-01 | Frozen-head v0.2 CI passes 5/5 jobs | https://github.com/SaridakisStamatisChristos/MOCOSO/actions/runs/39991432942 | VERIFIED_CI_METADATA | No new independent rerun at G0 write | SUPPORTED historical only | G0 rerun |
| TEST-02 | Frozen-head T1 CI passes 6/6 jobs | https://github.com/SaridakisStamatisChristos/MOCOSO/actions/runs/39991432594 | VERIFIED_CI_METADATA | Historical finite coverage | SUPPORTED historical only | G0 rerun |
| EXP-01 | Frozen-head M1 two native OS jobs successful | https://github.com/SaridakisStamatisChristos/MOCOSO/actions/runs/39991432958 | VERIFIED_CI_METADATA | Runtime arrays not independently analyzed | SUPPORTED as job result only | G0/G5 regeneration |
| EXP-02 | 104 cases, 1,164 measured, 292 explicit skips; independent oracles 78 cases | `benchmark_m1_execution.md`, `benchmark_m1.md`, local raw gzip, CI artifacts | REPO_REPORTED | 26 agreement-only cases, distribution mostly empty; can be skewed | PARTIAL | Recalculate raw JSON in G0/G4/G5 |
| EXP-03 | T1 generally faster | Same historical report | REPO_REPORTED | **Counterevidence: measured T1 losses; skips; empty-optimum-heavy distribution** | CONTRADICTED as universal statement | Never assert generalized dominance |
| EXP-04 | Paper-profile 146-case evidence collected | `benchmark_m1.md` documents profile only | NOT_VERIFIABLE | No verified completed 146-case run | UNRESOLVED | G4 |
| NOV-01 | T1 theorem is genuinely novel / strongest known | `novelty_matrix.md`, `search_log.md` | HYPOTHESIS | Classical distinct partitions/DP and predecessor convex-subsequence work; narrow search | UNRESOLVED | Independent G1 |
| PUB-01 | Publication-ready claim and GO decision | G0–G6 plan | NOT_VERIFIABLE | G1–G6 not passed | **NO GO at current gate, provisional not final adjudication** | Independent G6 only |
| ART-01 | Native final M1 ZIP artifacts intact and indefinitely reproducible | GitHub artifact IDs 12517743190 / 12518805490, server digests | VERIFIED_CI_METADATA | Both expire 2026-11-22; archive bytes not independently hashed | PARTIAL | Archive/rehash G5 |
| REPRO-01 | Clean checkout by coordinator reproduces source/tests/benchmarks | No local external Git DNS; GitHub Actions historical only | NOT_VERIFIABLE | New G0 CI run pending | PENDING | G0 CI new run |

## Gate lifecycle
| Gate | Owner | Status | Strict transition rule |
|---|---|---|---|
| G0 | Trillion Developer++ | PARTIAL | Pin hashes, directly reproduce where available; no false PASS |
| G1 | Knowledge Nexus | PENDING | Closest primary papers; C1–C7 equivalence, limitations |
| G2 | Theorem Foundry | PENDING | Adversarial independent proof and counterexamples |
| G3 | Algorithm Foundry | NOT TRIGGERED | Only if G1/G2 motivates distinct stronger contribution |
| G4 | Trillion Developer++ | BLOCKED by G1/G2 | Registered paper profile + positive-optimum hard cases |
| G5 | Separate clean-room reproduction | BLOCKED by preceding evidence | Artifact integrity, direct recomputation, version coherence |
| G6 | SOTA Research Auditor | BLOCKED by G1–G5 | Claim-level independent GO/CONDITIONAL GO/NO-GO |

The final verdict is reserved for G6. Do not launder these coordinator judgments into independent approvals.
