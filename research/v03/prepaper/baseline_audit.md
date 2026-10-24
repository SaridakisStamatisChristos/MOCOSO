# G0 baseline reconstruction — MOCOSO v0.3 pre-paper (2026-10-23)

**Status: PARTIAL — GitHub provenance/CI inspected; fresh reproduction pending.** Do not call this an independent proof, originality determination, paper-ready benchmark, or complete G0 PASS. This file was produced by the research coordinator and is **not** an independent mathematical or literature review.

## Exact Git state (GitHub connector read, 2026-10-23 UTC)
- Repository: https://github.com/SaridakisStamatisChristos/MOCOSO
- Production `main`: [`9cedac0d0f860564d5ee1a9064b01ef56ac2a764`](https://github.com/SaridakisStamatisChristos/MOCOSO/commit/9cedac0d0f860564d5ee1a9064b01ef56ac2a764)
- Draft [PR #2](https://github.com/SaridakisStamatisChristos/MOCOSO/pull/2): `mocoso-v0.3-research-t1` at [`65030469c65545a0877740fed9c53ef2035766f2`](https://github.com/SaridakisStamatisChristos/MOCOSO/commit/65030469c65545a0877740fed9c53ef2035766f2). Targets main. Comparison: 20 commits ahead, 0 behind; 13 added files, no edits of existing solver.
- Draft [PR #3](https://github.com/SaridakisStamatisChristos/MOCOSO/pull/3): `research/v03-benchmark-expansion` at [`7595130fecb1a21dc8ca8823d9ee8d5d136af97a`](https://github.com/SaridakisStamatisChristos/MOCOSO/commit/7595130fecb1a21dc8ca8823d9ee8d5d136af97a). Targets PR #2 branch. Comparison: 2 ahead, 0 behind; seven added files, no edits of existing solver.
- New research branch: `research/v03-prepaper-g0-evidence`, created from the exact PR #3 commit; document/verification-only changes; PR #2 and #3 remain unmerged.
- Commit lineage verified by comparison merge bases and ahead/behind counts, not inferred solely from PR descriptions.

## Source/proof/evidence map (Git blob SHA-1 at frozen PR #3 tree)
| Role | Path | Git blob | Trust boundary |
|---|---|---|---|
| Production exact solver | `modconvex.py` | `3e412a9dcc4f95ad9bbbe6b87e1e1309b7382d1d` | Production v0.2; unchanged |
| Independent edge baseline | `edge_dp.py` | `042261b2cac98a1acab9f81d3baed12198c1db42` | Comparison code; shared project provenance |
| T1 research solver | `experiments/v03/deficit.py` | `847ff91e12b88997a004c68e530e6f483840d206` | Experimental only; no dispatch |
| Comparator adapters | `experiments/v03/baselines.py` | `52676a03787dd358d5cc6a80eb679764dd5a267a` | Mask and tuple edge controls |
| T1 proof draft | `research/v03/t1_deficit_proof.md` | `e51bd340f18cb6826ad1a6a6ff2cfe47749298d3` | Candidate proof, not independently certified |
| Novelty matrix | `research/v03/novelty_matrix.md` | `5336db9c5a6af483c3904f9836883719f897c781` | Bounded prior-art screening only |
| T1 falsification | `tests/test_v03_deficit.py` | `2549545a216b82fe2d5207c4a621b1878b0ad9f0` | Finite exhaustive/differential tests |
| Original T1 harness | `experiments/v03/benchmark.py` | `f8e5171eebd17f0a4492f3d9a6967003c2f8d066` | Historical 13-case evidence |
| M1 harness | `experiments/v03/benchmark_expanded.py` | `6e16de7faf6f4767f74765ddda18071d9fccf293` | 104 CI / 146 paper profiles |
| M1 workload generator | `experiments/v03/workloads_expanded.py` | `7f6ab2a495c88a73f1118ace27686f010b026f7d` | Seeded/registered families |
| M1 harness tests | `tests/test_v03_benchmark_m1.py` | `14d7239795fd4d837a83231b03496fe788f84054` | Finite protocol checks |
| Committed M1 local raw | `research/v03/evidence/benchmark_m1_local_raw.json.gz` | `36bf6f41b9503d47e6ac6bb39256c17363afcfa6` | Git-retained gzip; gzip bytes not independently decompressed in this audit |

The main production and edge code blobs are identical between `main`, #2, #3. Git *blob* digests above use Git's SHA-1 object namespace; do **not** relabel these as SHA-256.

## Problem and invariant contract
Input: arbitrary signed integers `a[1..n]`, `m>=2`. Choose increasing indices maximizing full subsequence length, with consecutive selected value differences *strictly increasing*, sum of 1-based indices congruent to 0 modulo `m`, and globally lexicographically smallest **complete index tuple** among maximizers. Empty subsequence is admissible. Threshold asks `OPT >= K`; soft `max_seconds`/`max_heap_bytes` checks are not hard caps; `RESOURCE_LIMIT` cannot certify infeasibility.

Research T1 restricted to `U/2<m<=U`, `U=n(n+1)/2`, `h=U-m`, `q=min(n,h)`. A nonempty feasible solution omits distinct indices of sum `h`, hence omissions lie in `1..q`. The suffix `q+1..n` is present for all candidates, and only local selected triples through `q+2` depend on the omissions. Reachability DP + recursive enumeration is claimed to give `O(n+qh+q P_d(h))` unit-word operations and `O(qh+q)` auxiliary words (excludes input and final output). The proof is in the above candidate file, and **G2 must challenge** its count, word/bit model, lex ties, memory accounting and partial certificates. This reconstruction does NOT certify the theorem.

## Independently read GitHub Actions run metadata (historical, not a newly rerun test)
At commit `7595130fecb1a21dc8ca8823d9ee8d5d136af97a`:
- [v0.2 exactness](https://github.com/SaridakisStamatisChristos/MOCOSO/actions/runs/39991432942): 5/5 successful jobs, Python 3.10–3.13; scripts `research_tests.py`, `edge_trials.py`, `extra_trials.py`, and unittest suite.
- [v0.3 research](https://github.com/SaridakisStamatisChristos/MOCOSO/actions/runs/39991432594): 6/6 successful jobs, four Python versions, Ubuntu and native Windows benchmarks/tests.
- [M1 expanded](https://github.com/SaridakisStamatisChristos/MOCOSO/actions/runs/39991432958): 2/2 successful jobs, native Ubuntu and Windows; `--profile ci --blocks 2 --repetitions 3`. CI step conclusions and existence/digests of artifacts checked through GitHub API; new raw re-analysis not yet performed.

Historical execution note `research/v03/evidence/benchmark_m1_execution.md` reports 104 cases, 1,164 completed measured cells and 292 planned skips per environment; separately reports a local Linux 3.12.14 run with 36 tests and 61 selected-subset oracle + 17 superconvex oracle + 26 cross-algorithm-only cases. These *numeric case classifications and timings are report-authored statements*, not re-derived from compressed bytes by G0. It reports T1 losses and a distribution cohort of 36 empty optima out of 42; no universal performance inference is licensed. The 146-case paper profile has **not** been newly executed.

### CI artifact preservation register (GitHub API metadata, 2026-10-23)
| Run/artifact | Artifact ID | Server SHA256 digest | Expires UTC |
|---|---:|---|---|
| final M1 Ubuntu | [12517743190](https://github.com/SaridakisStamatisChristos/MOCOSO/actions/runs/39991432958) | `0dbfa511c2443b0a3710d507378d1047eff6325dbfed8a3036c5e6ef0fc9d46b` | 2026-11-22 17:03:24 |
| final M1 Windows | [12518805490](https://github.com/SaridakisStamatisChristos/MOCOSO/actions/runs/39991432958) | `ce3aa87d766aa1ec1e8e53bf53fdde6b1add11d8ddb33d96d04d174ee16239fd` | 2026-11-22 17:04:14 |
| v0.3 raw Ubuntu | 12516779765 | `e126dff2e258dc8c9a1c39d3a05f53cf0f6a4be7f7a3b958ba51e96965ba03b7` | 2027-01-21 |
| v0.3 raw Windows | 12517318909 | `a52432f16ec3228e79c92b5d16685707886a9df9147389fa5753ad200d999692` | 2027-01-21 |

The M1 workflow explicitly sets 30-day retention; materialize unexpired ZIP bytes with independent SHA checks and commit/export durable archival copies during G5. The server-reported archive digest is evidence of server metadata, **not** a locally rehashed ZIP.

## Reproduction protocol and unresolved actions
1. Clean checkout `7595130fecb1a21dc8ca8823d9ee8d5d136af97a`, verify Git tree and SHA256 checksums.
2. `python -m unittest discover -s tests -p 'test_*.py' -v`; `python research_tests.py`; `python edge_trials.py`; `python extra_trials.py`.
3. `python experiments/v03/benchmark.py --output v03_raw.json --repetitions 3 --seed 20261023`.
4. `python experiments/v03/benchmark_expanded.py --profile ci --blocks 2 --repetitions 3 --plan-only --output m1_plan.json`; rerun without `--plan-only` to `m1_raw.json`; `--summarize m1_raw.json --output m1_summary.json`. Do **not** overwrite committed historical results.
5. Check source digests, case/input/plan hashes, full witness semantics, exclusions, skips, raw timings, and independently recompute summary.
6. Archive M1 hosted artifacts before expiry. Identify runner differences and treatment of non-independent oracle cells.
7. G1 and G2 are independent plugin reviews, not an endorsement by this coordinator.

**G0 checkpoint:** git/CI metadata verification PASS; source preservation PASS; local clean-checkout fresh execution NOT_VERIFIABLE (this execution environment has no direct network clone); fresh GitHub Actions reproduction PENDING; archive bytes independent digest NOT_VERIFIABLE; baseline research-claim acceptance PENDING. No formal manuscript drafting; no merge.
