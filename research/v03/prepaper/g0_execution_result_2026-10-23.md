# G0 executed verification checkpoint — 2026-10-23 UTC

**Scope:** executable reproduction of the *finite baseline* only. Source/research benchmark code identical to research head `7595130fecb1a21dc8ca8823d9ee8d5d136af97a`. Read this record together with `baseline_audit.md` and `evidence_register.md`. This is the later G0 evidence checkpoint; earlier PENDING statements in those snapshot files reflect their time of authorship.

## Verified fresh GitHub Actions run (connector job steps and logs read)

PR [#4](https://github.com/SaridakisStamatisChristos/MOCOSO/pull/4), evidence-only commit [`a2875732e53ae83045e47f44a0f4e725b3cbc86e`](https://github.com/SaridakisStamatisChristos/MOCOSO/commit/a2875732e53ae83045e47f44a0f4e725b3cbc86e), executed the following complete workflows:

| Run (at exact commit) | Result | Directly checked evidence |
|---|---|---|
| [40013433164 G0](https://github.com/SaridakisStamatisChristos/MOCOSO/actions/runs/40013433164) | SUCCESS, 2/2 jobs | Fresh unit+legacy tests, original 13-case benchmark, 104-case M1 protocol, generated summary and archive |
| [40013433151 v0.2](https://github.com/SaridakisStamatisChristos/MOCOSO/actions/runs/40013433151) | SUCCESS, 5/5 jobs | Four Python versions + comparison |
| [40013433034 v0.3](https://github.com/SaridakisStamatisChristos/MOCOSO/actions/runs/40013433034) | SUCCESS, 6/6 jobs | Four Python versions, two OS runners and original comparison grid |

G0 `g0-unit-and-legacy` job 120619328448: the checked log states `Ran 36 tests in 15.258s`, `OK`, and successful `research_tests.py`, `edge_trials.py`, and `extra_trials.py` steps. The frozen-code `git diff --exit-code` step succeeded. The environment/source-hash text was uploaded.

G0 `g0-benchmark-reproduction` job 120619328746: all original 13-case, plan-only, 104-case and summary-regeneration steps passed. The checked **executed job log** states exactly `{"OK": 1164, "SKIPPED": 292}` for the newly rerun M1 CI profile (two blocks, three timing repetitions, seed protocol as versioned). The number matches earlier reported M1 counts, but fresh timings need not be numerically identical. Job output includes new `g0_original13_raw.json`, `g0_m1_plan.json`, `g0_m1_raw.json`, `g0_m1_summary.json`.

## Immutable new CI artifact metadata (GitHub API)

| Artifact | ID | GitHub-reported SHA256 ZIP digest | Expires UTC |
|---|---:|---|---|
| [G0 environment and source hash](https://github.com/SaridakisStamatisChristos/MOCOSO/actions/runs/40013433164/artifacts/12527985212) | 12527985212 | `0a1e2b6b1d722e1de6830139a4bb0583b959bc6a38e98f05a33b0fe18e7b28b5` | 2027-01-21 19:41:48 |
| [G0 original13 + M1 plan/raw/summary](https://github.com/SaridakisStamatisChristos/MOCOSO/actions/runs/40013433164/artifacts/12527546423) | 12527546423 | `c2c8665ea1d3a15d2e9bbc0168d822883e12399bea5b5573205a4ff2a01e411e` | 2027-01-21 19:41:48 |

The archive digests are **metadata returned by GitHub**, not independent file re-hashes. These artifacts also expire and must be archived with G5's durable supplementary evidence pack. Historic final PR #3 M1 Ubuntu/Windows artifacts still expire 2026-11-22 and must be copied before then.

## Claims and gate disposition

- **PASS — G0 versioned source/branch provenance:** live heads and stacking verified, original solvers unchanged, Git tree/blob map pinned.
- **PASS — fresh finite test reproduction:** 36 unit tests and legacy scripts, plus full v0.2/v0.3 CI matrix reported passing at the pinned G0 source commit.
- **PASS — fresh benchmark *execution* reproduction:** 13-case harness and 104-case CI profile completed; 1164 OK + 292 planned skips; raw artifacts captured. This does not mean every benchmark summary datum has been independently recomputed by a separately authored analyzer.
- **PARTIAL — independent raw numeric/data forensics:** own independent extractor, rehash of ZIP payloads, external hardware reproduction, unverified 26 larger cross-algorithm cases, and distributions with many empty optima belong to G4/G5.
- **PENDING — G1 closest-work originality tribunal and G2 independent theorem proof.** No other plugin review has been executed or claimed here.
- **NOT TRIGGERED — G3**, conditional on G1/G2.
- **BLOCKED — G4/G5/G6**, until suitable mathematical and empirical gate evidence exists.

**Operational G0 finite-reproduction gate: PASS with explicit provenance/reanalysis limitations.** This is not a pre-publication GO or a novel-theorem verdict. No production algorithm change, PR merge, manuscript writing, first-in-literature statement or universal-performance claim.
