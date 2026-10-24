# MOCOSO v0.3 — GitHub CI and raw benchmark evidence (2026-10-23)

Research only. Main baseline: 9cedac0d0f860564d5ee1a9064b01ef56ac2a764. **No scholarly priority, generalized speed superiority, or publication-readiness claim.**

## Independent execution evidence

- V0.3 research workflow: https://github.com/SaridakisStamatisChristos/MOCOSO/actions/runs/39953542302 — **SUCCESS** for Python 3.10, 3.11, 3.12, 3.13 and paired raw benchmark job.
- Workflow HEAD branch commit: 33e52bb60b23aa82644b0be30ac302298329eb3e. Checkout internally recorded GitHub PR merge-testing commit 5e72bf999601d6f3a671ff3ac87fb647cd329333; do NOT mistake this synthetic checkout SHA for the branch HEAD.
- Download the original GitHub Actions artifact `v03-raw-benchmark` from the workflow (artifact id 12501142148, ZIP SHA256 `3de497800139f18aefde03273e45711f109dc4fd899a332ce2eaa76666f0c03e`). It contains `v03_raw.json` and `v03_hardware.txt`.
- Previous complete v0.2 exactness workflow at code-containing commit 071508acd13953f9d8bc695381dd9098429d8c1a: https://github.com/SaridakisStamatisChristos/MOCOSO/actions/runs/39953125613 — **SUCCESS**.
- Standalone v0.3 unittest checks use a separately authored exhaustive all-subsets oracle; 41,085 small exhaustive instances (n=2..7, values in {-1,0,1}, each high modulus) and 250 signed large-integer seeded cases. The mask and tuple edge comparators are also checked against the exhaustive oracle over 10,467 small cases. CI SUCCESS confirms the runnable test suite, not that untested inputs or theorems are universally correct.

## Measured benchmark (one GitHub runner, descriptive)

GitHub-hosted Ubuntu Linux, Python 3.13.16, reported 4 CPUs; 3 repetitions per algorithm after warmup, each comparator in an isolated process. End-to-end algorithm call timing includes reconstruction but excludes Python interpreter process startup. The original eight-case benchmark disproportionately produced empty optimum witnesses. Therefore **the five superconvex rows below are a disclosed post-hoc coverage repair, not preregistered results**. All were compared on identical full modular/lex/strict-convex semantics; algorithms returned identical index witnesses.

| Family | n | h | optimum length | T1 median milliseconds | v0.2 median milliseconds | v0.2 / T1 observed ratio |
|---|---:|---:|---:|---:|---:|---:|
| superconvex | 12 | 8 | 11 | 0.049 | 0.213 | 4.35 |
| superconvex | 20 | 12 | 19 | 0.105 | 3.819 | 36.28 |
| superconvex | 35 | 12 | 34 | 0.117 | 4.071 | 34.91 |
| superconvex | 20 | 24 | 18 | 0.801 | 9.404 | 11.74 |
| superconvex | 35 | 40 | 33 | 9.907 | 98.575 | 9.95 |

The last two rows have h>n. The n=35,h=40 T1 row recorded 1,106 completed distinct omission partitions, 7,464 visited entry states, 8,270 counted operations. The v0.2 run counted 682,040 operations, **but operation counters are not defined identically** and must not be equated directly. Its independent edge-bitmask comparator took 30.993 ms on that case (three-run median).

The original case grid is *also* included in raw JSON, including empty-answer fast-rejection cases and a case where the isolated mask loop beat the T1 implementation. The published table above is deliberately labeled as a coverage-repair subset; it is NOT the full distribution and cannot be used to claim general performance leadership. Source-file SHA256 hashes, raw runs, platform/CPU information, tracemalloc peak allocations and Linux maximum process RSS are in the ZIP. Maximum RSS includes import and warmup baselines, and traced peak is not total RSS. No external hard RSS cap was applied.

## Gate status after these runs

- T1 finite exactness and lex/decision regression tests: **PASS on stated finite suite / four Python versions**.
- Original v0.2 regression workflow: **PASS at stated code commit**; later documentation-only commits do not alter solver.
- Raw paired benchmark reproducibility on one CI environment: **PASS** with primary artifact.
- Meaningful cross-environment performance superiority: **UNVERIFIED**. Replicate on different machine and report full raw distribution, including unfavorable cases.
- Independent mathematical proof review, systematic bibliographic priority assessment, T2 space-time theorem and scholarly publishability: **UNVERIFIED / OPEN**.

Disposition: **conditional research progress**, preserve draft PR and v0.2 main, no merge by default and no unconditional novelty claim.
