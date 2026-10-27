# G14 RFP/OmO final executable research checkpoint

**2026-10-27. PR #27 exact head `9e85cccd83c3d25d5f242639add8c0af2f156069`.**

## Verified GitHub CI

[GitHub Actions run 40458610905](https://github.com/SaridakisStamatisChristos/MOCOSO/actions/runs/40458610905) completed **SUCCESS**:

- Ubuntu and Windows, Python 3.11 and 3.13: four exhaustive/independent-oracle test jobs passed.
- Six-way benchmark job passed, 817 original-plus-new cases, **zero full-canonical-witness disagreements** and no runtime exceptions.
- Historical G8/G10/G11/G12/G13 sources, revised G9 manuscript and G10 proof were checked for immutability.
- [Raw artifact (two JSON reports)](https://github.com/SaridakisStamatisChristos/MOCOSO/actions/runs/40458610905/artifacts/12713910178): individual repetitions, each case's provenance and digest, certified/abstained status, all loss cells, environment and source SHA-256 checks.

The executed profile contains the earlier 677 cases plus **140 newly registered** cases with seed 27102714. No benchmark thresholds or acceptance requirements were altered after seeing the results.

## Two distinct performance questions, explicitly separated

Performance ratio = baseline median complete-answer runtime / G14 median complete-answer runtime. A ratio above 1 favors G14. **The median of ratios and the ratio of sums are different statistics**; neither should silently replace the other.

| Baseline | Number of matched cases | G14 pairwise wins | Median of per-case ratios | Sum(baseline per-case medians) / Sum(G14 per-case medians) |
|---|---:|---:|---:|---:|
| G13 | 817 | 232 | **0.965x (regression)** | **1.430x** |
| G12 | 817 | 266 | **0.944x (regression)** | **1.603x** |
| G11 | 817 | 449 | 1.041x | 2.437x |
| corrected G8 | 817 | 488 | 1.647x | 4.055x |
| G10 | 817 | see raw JSON | see raw JSON | 2.103x |

On the **56 cases** certified specifically as `three_omissions`, G14 won **56/56 against G13**, with median paired speedup 13.283x and ratio of sums 16.834x. It won 49/56 against corrected G8, with ratio of sums 29.006x.

**Negative results are not hidden:** On the **207 abstained** cases, G14 has total-time ratio 0.973x versus G13 (worse), and 0.723x versus G8. On **501 infeasible** cases G14's total-time ratio is 0.948x versus G13 (worse). On the **median individual case** G14 is 3.5% slower than G13. A universal per-instance speed superiority claim is false.

The prior 677 cases alone have sum-ratio G13/G14 1.315x; the fresh 140 cases have sum-ratio 1.813x. This supports a repeatable *workload-total* improvement within the registered synthetic generators, not a statistically certified result for arbitrary real data. A large benefit concentrated on the near-complete subset can dominate sums while most individual cases lose. Do **not** report only the aggregate value.

## Research contribution and frontier

The strongest mathematical advance in this series is a **true partial exact O(n)-time certificate** (G12 one/two omitted, G13 weighted-hitting infeasibility, G14 anchored three omitted). It is **not** an unrestricted O(n) solver for the full convex, modular-index-sum subsequence problem. The unrestricted G14 wrapper still uses G11/G10 fallback, preserving G10's conditional `O(n+H^(5/2)log(H+1))` time and `O(H²)` wide-word auxiliary claims.

Generic interval hitting, lexicographic resource path extension, and sorted-difference convex-subsequence algorithms have prior art. G14's specific linear certification composition has not undergone an independent prior-art theorem implication audit. No globally SOTA/first/published claim is made.

The standalone real OmO binary/runtime bridge was not exposed; this campaign used the **ChatGPT-native recursive OmO controller** and real GitHub/CI/executable Python tools. No independent workers or human referees were fabricated.

## Evidence ledger

| Claim | RFP status | Supporting evidence | Residual |
|---|---|---|---|
| G14 exact canonical witness for n<=8 signed alphabet | TESTED, VERIFIED_CI | four-platform 73,809 independent selected-mask comparisons | finite domain |
| G14 larger three-omission certificates | TESTED, VERIFIED_CI | cross-checked constructed cases h up to150, independent n12–14 oracle | arbitrary n theorem human-checkable, not formal |
| G14 partial linear time/space | PROOF_SKETCH | anchored candidate bound, constant-size local checks, 3-stream merge, O(h) prefix | outside math referee |
| G14 full solver exactness | TESTED, VERIFIED_CI on registered cases; conditional general proof | 817 six-way full-tuple equalities and unchanged G11/G10 | full theorem not formally verified |
| G14 per-instance superiority to G13 | REFUTED | 585/817 ties/losses by median, median ratio 0.965x | do not claim it |
| G14 workload-aggregate improvement | TESTED, VERIFIED_CI | source-pinned 817-case sums and raw samples | host/distribution bias, no confidence interval |
| World theoretical/practical SOTA | UNRESOLVED | no global external comparator or refereeing | independent sources & benchmarks |
| Exact high-modulus joint bound originality | POSSIBLY_NOVEL, unresolved | bounded directed prior art | external theorem-level audit |

## Decision

**Keep PR #27 and parent PRs #21–#26 as research drafts** until an independently verified integration decision. Do not automatically route public `modconvex.solve` through G14: the population of workloads is unknown, and fallback overhead can defeat gains on cases outside the certificate subclasses. Publish no universal SOTA or worldwide-priority assertion.

The next highest-information-value work is (a) a truly external mathematical referee checking the exact G10/G14 statements against existing literature, and (b) a representative external benchmark for the precise modular convex-subsequence problem, or a clearly specified target workload distribution. Additional same-distribution heuristic tuning is not adequate evidence of worldwide SOTA.
