# G4 comparative evidence — executed native-runner audit and disposition

**Date:** 2026-10-24 UTC. **Owner:** Trillion Developer++ G4 (Conductor/ACO + evidence audit). **Research PR:** [#8](https://github.com/SaridakisStamatisChristos/MOCOSO/pull/8), draft, stacked on unmerged G3 PR #7. **Immutable executed source head:** `35b7c6f958141664f03be0913dff9bf47f946350` (the CI tests the GitHub-generated synthetic pull-request merge `c64c6510692e2e444f3c744322b4e1567d6e8faa`, not an independently merged product). Parent G3 head `53b2276c7ed450ba8c27adc0e1e02c1493b4e592`. Frozen original T1/M1 source `7595130fecb1a21dc8ca8823d9ee8d5d136af97a`. v0.2 main `9cedac0d0f860564d5ee1a9064b01ef56ac2a764`.

## Gate conclusion

**G4 FINITE COMPARATIVE EVIDENCE: PASS WITH CAVEATS. Strongest paper-protocol / research-priority claims: NOT CLEARED.** The corrected Actions workflow completed **8/8 successful jobs** on [run 40058471851](https://github.com/SaridakisStamatisChristos/MOCOSO/actions/runs/40058471851): four direct independent generic-DAG oracle jobs (Ubuntu/Windows x Python 3.11/3.13), two registered G4 targeted benchmark jobs (both native OS) and two original M1 146-case paper-profile benchmark jobs (both native OS, Python 3.13).

This is the first G4 research evidence round, NOT the independent G5 clean-room audit, NOT external literature priority certification, and NOT a G6 manuscript GO. **No merge, solver rewrite, hidden case exclusion or paper authoring.**

## Claim/evidence table — all status counts independently recomputed from full raw artifact ZIPs

| Native OS | Workload cohort | Cases | Process blocks | Timings per block | Planned cells | OK measured | Registered SKIPPED | TIMEOUT / ERROR / MISMATCH / UNVERIFIED |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Ubuntu | M1 paper-profile (original 7 methods) | 146 | 2 | 3 | 2,044 | **1,616** | **428** | **0** |
| Windows | M1 paper-profile (original 7 methods) | 146 | 2 | 3 | 2,044 | **1,616** | **428** | **0** |
| Ubuntu | New G4 targeted four-way | 40 | 2 | 3 | 320 | **256** | **64** | **0** |
| Windows | New G4 targeted four-way | 40 | 2 | 3 | 320 | **256** | **64** | **0** |

Each paper-profile OS run had **1,092 independently-oracle-verified measured cells** and **524 cross-algorithm-agreement-only measured cells**. The 146-case paper cohort had **79 small all-selected-subset-oracle cases, 23 power-of-three superconvex index-sum-oracle cases and 44 large comparison-only cases**. Of the independently checked cases, 52 have positive optimum and 50 empty optimum. These are **cases**, whereas 1,092/524 are **method/block cells**.

Each targeted OS run had **112 independently-oracle-verified measured cells and 144 cross-algorithm-agreement-only cells**. There are 8 small direct-oracle cases and 8 additional independently solvable superconvex cases; other 24 targeted cases have exact cross-algorithm agreement (not independent proof). New generic comparator passed its own full selected-subset Cartesian oracle (10,467 combinations of n, signed sequences and high moduli) plus 370 seeded large-signed instances per deterministic test execution; the same test inputs run four times on different OS/Python versions **must not be counted as four independent input samples**.

Raw ZIP bytes of all four benchmark artifacts were downloaded using the GitHub connector and independently SHA256 hashed in the working runtime. The hashes agreed exactly with GitHub's artifact service digests. The plans, input hashes, frozen source hash dictionaries and complete-witness optimal lengths agree **across Ubuntu and Windows** in both cohorts. All reported `complete` flags are true; all rows in the registered plans were present. The four G4 test jobs passed. The original `benchmark_expanded.py`, production v0.2, original T1 and G3 source blobs remained untouched, with the CI freeze gate passing on both platforms.

## Registered source/provenance hashes

- G4 targeted plan hash (both OS): `0a2a77fc6a945c96782cd9df33bd1c34288589be5ffe329dbc848705609d1162`.
- G4 targeted input hash (both OS): `474da658f6abbc2a379f625f8590bc06c84a65d41657bb2cc3f8028bea89a525`.
- Paper M1 plan hash (both OS): `c59cb25626d0debb3f6bd1aad69052cc11aaed1a7a861854875ab5b114179e11`.
- Paper M1 input hash (both OS): `40fbcbf2c1292b15d9a124c25c6ab877339c3acfb907b660b0f008db1fff3314`.
- G3 `experiments/v03/poly_deficit.py` source SHA256 in both targeted reports: `65773bc7840738a430f809096fbdefa48e4cd7275f10bb1c50fd4fcb572dc2a9`.

## Downloaded archive IDs, independent byte digests and archival deadline

| Workload/OS | Artifact ID | Verified ZIP SHA256 |
|---|---:|---|
| 146-case Ubuntu | [12546253781](https://github.com/SaridakisStamatisChristos/MOCOSO/actions/runs/40058471851/artifacts/12546253781) | `2c8f962abedcb59c630b145ff6d3f981069accf706fcc204e310b442c73dd175` |
| 146-case Windows | [12546566643](https://github.com/SaridakisStamatisChristos/MOCOSO/actions/runs/40058471851/artifacts/12546566643) | `432d9533b0db6a49158bfb3d3d35564f63e8d709957109229fbcd89d1e8d6b61` |
| 40-case Ubuntu | [12546576206](https://github.com/SaridakisStamatisChristos/MOCOSO/actions/runs/40058471851/artifacts/12546576206) | `5051ac65321107385ceb8b5c7d2eaba25690e90cd8b73594b13895098634f3cb` |
| 40-case Windows | [12546317881](https://github.com/SaridakisStamatisChristos/MOCOSO/actions/runs/40058471851/artifacts/12546317881) | `e37b09670bb518863d3310c7350c5521aa251df18f5313e47848924841e29a18` |

GitHub reports ZIP expiration **2027-01-22 03:28:58 UTC** for these artifacts. They are verified downloads in G4, **not yet guaranteed durable third-party archival**; G5 should copy and hash independently in its own clean environment. Older M1 original native artifacts expire **2026-11-22** and have higher archival urgency. ZIP hashes are of archive bytes; inner raw JSON content can be individually content-hashed later for immutable supplement.

## Empirical findings, including counterevidence

### Paper cohort, T1 versus baseline v0.2

Of 122 complete paired T1–v0.2 case comparisons (the other 24 lack complete pairing due registered skips), T1 was faster on **121 / 122 on Ubuntu** and **120 / 122 on Windows**; losses **1** and **2** respectively. Observed per-case median baseline/T1 ratios across complete pairs were **25.46 Ubuntu** and **27.18 Windows**. These distributions are conditional on the registered case mixture, the old public implementation choices/caps, and one ephemeral runner per OS. They do not establish an overall constant-factor guarantee, globally fastest exact solver, independent review, or state-of-the-art priority. The original M1 study includes both historical and post-hoc cohorts; their provenance labels remain unaltered.

The independent reference states are uneven: 102 of 146 cases have independent oracles (52 positive, 50 empty), but 44 cases rely on agreement by algorithms with some shared lineage. Large positive-optimum cases get independent superconvex controls, while generic random difficult cases still require stronger independent proof/oracles.

### Targeted cohort, G3 versus T1, positive optimum

| n | h | G3 speedup T1/G3, Ubuntu | G3 speedup T1/G3, Windows |
|---:|---:|---:|---:|
| 12 | 4 | 0.61x | 0.54x |
| 12 | 8 | 0.62x | 0.69x |
| 20 | 12 | 0.73x | 0.70x |
| 25 | 15 | 0.96x | 0.98x |
| 30 | 20 | 1.49x | 1.45x |
| 40 | 25 | 2.16x | 2.26x |
| 60 | 40 | 8.69x | 8.75x |
| 75 | 50 | 17.1x | 19.1x |
| 90 | 60 | **37.21x** | **44.77x** |
| 1000 | 4 | 0.67x | 0.79x |

Ratios are medians across the two complete block ratios on **a single native runner per OS**, with three untraced repetitions per block; they are descriptive, not significance tests or cross-OS speed measurements. G3's wins on larger h coexist with real losses at small h. The alternating and immutable-suffix-defect negative-optimum cases are retained rather than hidden.

### T1/G3 theoretical bound versus observed memory

On the Ubuntu n=90,h=60 superconvex case, traced peak Python allocations were approximately **12.9 KiB for T1** versus **2,256.7 KiB for G3**. This illustrates the predicted *direction* of the time–space tradeoff but does not prove asymptotic memory complexity. Whole-child Linux peak RSS stayed around the Python interpreter/runtime background (roughly 25–27 MiB) and is **not the solver-only payload**. Windows RSS is unavailable in this protocol. Traced memory is a separate instrumented call from timing repetitions, and unbounded input integer bit costs are not charged in the G2/G3 unit wide-word theorem.

### Why generic DAG comparison is NOT SOTA proof

`experiments/v03/generic_rc_dag.py` is a genuinely **different forward selected-pair/resource-cost DP** and independently exhaustively validated small oracle. However it retains full tuple witnesses per state and does not use G3's monotone difference sweep. G3 can be faster for n=60,h=40 (around 11.9x Ubuntu and 12.5x Windows versus this control), but the difference bundles **sweep optimization plus witness storage representation**, not an isolated causal treatment. The control is **not** a reproduction of a uniquely identified optimized literature implementation or proof that no superior generic resource-constrained longest-path method exists. Register state cap 60,000 is a benchmark policy, not a resource-theoretic impossibility; 16 comparator cells per OS skipped under this cap. v0.2 skip policy similarly produces 48 skipped cells per targeted OS.

## Preserved failed-first-attempt and fix

Initial [G4 run 40058407831](https://github.com/SaridakisStamatisChristos/MOCOSO/actions/runs/40058407831): both initial Windows benchmark jobs **FAILED before measuring** because Git native checkout transformed LF Python sources to CRLF. The existing M1 byte-level `frozen source changed: modconvex.py` check was correctly strict; treating this failure as a mathematical mismatch would have been incorrect, and suppressing the gate would have been unsafe. Commit `35b7c6f958141664f03be0913dff9bf47f946350` added only job-level `GIT_CONFIG_COUNT=1`, `GIT_CONFIG_KEY_0=core.autocrlf`, `GIT_CONFIG_VALUE_0=false`; no solver file was touched. Corrected [run 40058471851](https://github.com/SaridakisStamatisChristos/MOCOSO/actions/runs/40058471851) then passed **all 8 G4 jobs**, including both native Windows paper/targeted source-preservation gates.

## Gate outstanding after executed G4

1. **Intensive 3 blocks ×5 reps paper benchmark was not run.** G4 executed 146 complete cases using **2 blocks x3 reps** on each OS. This is quantitatively full-case coverage but lower repetition intensity than the originally documented paper command; any claim of satisfying that *specific* 3x5 protocol would be false. Additional physical-machine / rerun replication and uncertainty intervals remain outstanding.
2. **Scientific originality and closest optimized literature baseline remain NOT CLEARED** after G1. A generic semantic comparator is not enough to establish new-algorithm precedence.
3. **Memory/time hard ceilings and catastrophic OOM certificate delivery remain UNVERIFIED**. No kernel-enforced hard RSS cap was used; tracemalloc and Linux ru_maxrss have different meanings.
4. **G5** requires clean-room reproduction, rehashing exact artifact bytes in an independent environment, environment pinning and retention beyond artifact expiry (especially historical expiring November 2026 data).
5. **G6** independent SOTA Research Auditor exclusively decides GO / CONDITIONAL GO / NO-GO for manuscript, based on resolved novelty and evidence.

**G4 decision:** **PASS (registered finite comparison and new controls, qualified)**, **NOT a publication-readiness GO**. Preserve draft PR #8 and all upstream drafts unmerged. No manuscript has been started.
