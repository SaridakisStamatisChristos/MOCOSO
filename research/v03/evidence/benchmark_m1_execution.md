# M1 execution evidence — 2026-10-23

Outcome: expanded CI-profile experiment completed locally and on native Ubuntu and Windows. No solver changes. No novelty or general superiority claim.

## Frozen source and verification

- Remote protocol/harness commit: `9f42ae129bd18dff26101d0c265556cd7df76093`. Local pre-run commit recorded in the raw report: `6d7f778b5cdc57815cb9f54b8dc0e2a51055740f`. Both commits have the identical complete Git tree `6332aae527a7a8b346ba68e0daf68bba1250659d`; they differ only in commit metadata. Reproduce from the remote protocol commit. The raw report preserves the actual local HEAD and dirty-tree observation rather than substituting another commit identity.
- Production/research solvers, existing baselines and previous benchmark passed the mandatory byte-preservation gate against `65030469c65545a0877740fed9c53ef2035766f2`.
- All 36 unit tests passed locally and on each native runner. Twelve tests specifically challenge the new harness, including tampered sources, exact-oracle comparisons, missing RSS support, deadlines, bad worker output, output disagreements and incomplete summaries.
- Local command: `PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 python experiments/v03/benchmark_expanded.py --profile ci --blocks 2 --repetitions 3 --output research/v03/evidence/benchmark_m1_local_raw.json`.

## Completed runs

| Environment | Tests | Successful measured cells | Planned skips | Errors / timeouts / mismatches |
| --- | ---: | ---: | ---: | ---: |
| Local 3.12.14 / Linux | 36 passed | 1,164 | 292 | 0 |
| GitHub Ubuntu / Python 3.13.16 | 36 passed | 1,164 | 292 | 0 |
| GitHub Windows / Python 3.13.16 | 36 passed | 1,164 | 292 | 0 |

CI source-head [run 39990732931](https://github.com/SaridakisStamatisChristos/MOCOSO/actions/runs/39990732931) passed both jobs. The existing [v0.2 exactness run](https://github.com/SaridakisStamatisChristos/MOCOSO/actions/runs/39990732710) and [v0.3 research run](https://github.com/SaridakisStamatisChristos/MOCOSO/actions/runs/39990733035) also passed. Native job logs explicitly report `{"OK": 1164, "SKIPPED": 292}`; artifact existence and digest metadata were verified. Native timing arrays have not been independently downloaded/analyzed for this note, so the timing observations below refer **only to the local run**.

Native artifacts (plan, raw report, summary, hardware):

- [Ubuntu artifact 12518150514](https://github.com/SaridakisStamatisChristos/MOCOSO/actions/runs/39990732931/artifacts/12518150514), archive SHA256 `03d4395b222a26f88f66ae8881869f9c4732f727884bc1df064604cf25334279`.
- [Windows artifact 12517851709](https://github.com/SaridakisStamatisChristos/MOCOSO/actions/runs/39990732931/artifacts/12517851709), archive SHA256 `d8043579274d59728732dc5218c6a556161a7a8cb1e881d44ea6cc34807fe59a`.
- GitHub reports expiration on 2026-11-22. Archive these before using them as permanent paper supplements. The committed local raw report is independent of that expiration.

## Local outcome balance

| Cohort | Cases | Empty optimum | Positive optimum |
| --- | ---: | ---: | ---: |
| legacy_original | 8 | 7 | 1 |
| legacy_posthoc | 5 | 0 | 5 |
| distribution | 42 | 36 | 6 |
| modulus_boundary | 32 | 14 | 18 |
| deficit_scaling | 17 | 0 | 17 |

Of 104 cases, 61 have selected-subset oracle support, 17 have independent superconvex index-sum oracle support, and 26 larger cases use cross-algorithm agreement only. Across measured cells this is 856 independent-oracle checks and 308 agreement-only checks. The distribution cohort remains dominated by empty answers in the high-modulus regime; do not generalize it to typical feasible production instances.

## Local within-runner comparison observations

Counts below use complete pairs of both process blocks. A win/loss compares the median of baseline/T1 ratios with 1; it does not establish statistical significance. Sub-microsecond costs and hosted CPU noise can change small effects. Every per-case ratio, raw time and missing pair remains in the compressed JSON.

| Cohort | Baseline configuration | Complete cases | T1 faster | T1 slower | Equal |
| --- | --- | ---: | ---: | ---: | ---: |
| legacy_original | v02 | 8 | 8 | 0 | 0 |
| legacy_original | v02_default | 8 | 8 | 0 | 0 |
| legacy_posthoc | v02 | 5 | 5 | 0 | 0 |
| legacy_posthoc | v02_default | 5 | 5 | 0 | 0 |
| distribution | v02 | 42 | 41 | 1 | 0 |
| distribution | v02_default | 42 | 41 | 1 | 0 |
| modulus_boundary | v02 | 20 | 18 | 2 | 0 |
| modulus_boundary | v02_default | 20 | 19 | 1 | 0 |
| deficit_scaling | v02 | 11 | 10 | 1 | 0 |
| deficit_scaling | v02_default | 11 | 10 | 1 | 0 |

This wider suite does not support a universal T1 speed advantage. Comparison cells outside the high-modulus domain are deliberately inapplicable. Scaling cells without a completed baseline do not enter comparative counts. All old post-hoc cases retain their original label. Paper-profile execution, independent physical-host replication, native timing analysis, theorem review and prior-art review remain open research work.

## Permanent local raw evidence

`benchmark_m1_local_raw.json.gz` is a gzip-compressed, unmodified raw report, containing all cases, input values, references, original plan, 1,456 cell records, raw timing arrays, memory observations, counters, source hashes and descriptive summaries.

- Compressed SHA256: `346866aedd2ff2edf6aa2067497b5f051b2417cd6aa14b399d889bec8478a722`.
- Uncompressed SHA256: `3afc887d038dcd23b115add4fef7c394cd00a38603ed9ae2c5fe074980eb8b1f`.
- Workload SHA256: `63e02910b47f95705192abf2ef3c0c5b7c3cbf57a08e5d18559fda5e0c52f51f`.
- Plan SHA256: `1d1715526cee4d65243ae51f92d3fa5d64e06f51fbb42a068c188707300b35b6`.

```bash
python -c "import gzip, pathlib; p=pathlib.Path('research/v03/evidence/benchmark_m1_local_raw.json.gz'); p.with_suffix('').write_bytes(gzip.decompress(p.read_bytes()))"
python experiments/v03/benchmark_expanded.py --summarize research/v03/evidence/benchmark_m1_local_raw.json --output m1_local_summary.json
```
