# v0.3 research milestone M1: expanded benchmark evidence

Status: prospective experiment specification, 2026-10-23. This is a separate
milestone stacked on research PR #2, frozen research reference
`65030469c65545a0877740fed9c53ef2035766f2`. It changes no production solver,
research solver, baseline implementation, previous benchmark, theorem, manuscript,
or archived result. Acceptance of this harness is separate from acceptance of T1.

## Questions and falsifiers

1. Does T1's observed advantage over the public solver persist across input
   distributions and default API dispatch? A baseline/T1 ratio below 1 is a
   measured loss, retained at case level, never excluded from reporting.
2. How do costs vary with n and h, especially h=0, h>n and the U/2 boundary?
   Finite timings and T1 node/partition counters characterize these cases;
   they do not prove asymptotic bounds. Algorithm counters count different work.
3. Do all exact methods return the same **full lexicographic witness**, including
   empty optima? Any disagreement fails the milestone. A timeout, resource limit,
   unverified single-method result, or exception is retained, never infeasibility.
4. Do within-runner directions reproduce on Ubuntu and Windows? Both run the
   identical versioned inputs, policies and seeds. Runner differences confound
   absolute time; these are algorithm comparisons within each runner.

These hypotheses were written after observing the earlier 13-case study and
before timing this new suite. This is a prospective follow-up to exploratory
work, **not** an independent external preregistration or a new novelty claim.
Plans and inputs are persisted before timing; commit the specification before
collecting final evidence. Amendments require a new version and disclosure.

## Workloads and cohorts

| Profile | Cases | Measured cells per process block | Planned skips per block | Purpose |
| --- | ---: | ---: | ---: | --- |
| smoke | 31 | 205 | 12 | End-to-end harness check, tiny independently checked cases |
| ci | 104 | 582 | 146 | Reproducible expanded runner evidence |
| paper | 146 | 808 | 214 | Larger seed sample and n=96 scaling, opt-in local run |

A cell is one case/algorithm/process block, with one warmup, several untraced
timing calls, then a separate traced-allocation call. The default two blocks
therefore plan 1,456 CI cells: 1,164 measured and 292 explicit skips.

- All eight original and five historically post-hoc cases are reproduced
  byte-for-byte, with their old cohort labels. The old script and results remain
  available for historical reproduction.
- New distribution cohort: uniform signed integers, sorted uniform integers,
  random permutations, random walks, three-valued data, sparse large outliers,
  piecewise quadratic data, arithmetic progressions, quadratics, constants,
  alternating signs, signed 120-digit integers, powers of three, and powers of
  three with a defect in the mutable prefix or far suffix. CI uses n=12 and 24,
  h=12; six stochastic families use two seeds, deterministic controls one each.
  Paper profile uses five stochastic seeds. Empty answers remain visible.
- Modulus boundaries at n=8 and 12: m=2, floor(U/2), floor(U/2)+1,
  U-n-1, U-n, U-1, U, U+1, for arithmetic and superconvex arrays. Every
  non-applicable T1/mask cell is recorded as a planned domain skip.
- Scaling: n=12,24,48 (plus 96 for paper), h=0,1,5,12,24,40 when 2m>U.
  Large cases use the independent superconvex oracle even where slower
  comparison methods hit the registered size cap. Such cells cannot establish
  a comparative timing ratio without a completed baseline.

Every case records its full input, modulus, n, h, seed, cohort, content hash and
stable identity. Workload RNGs derive from case content, independently of timing
order. Default workload seed 20261023, execution-order seed 713. Distinct seeds
do not imply distinct inputs for discrete random families; input hashes expose
duplicates. Technical repetitions and process blocks are not new input samples.

## Comparators and registered omissions

All seven methods solve the same signed-integer, strict-convexity, index-sum
modulo m, maximum-length, globally lexicographically least witness objective.
The existing implementations are imported without edits.

| Name | Configuration | Registered restriction |
| --- | --- | --- |
| deficit | Research T1 implementation | U/2 < m <= U |
| v02 | Public API, complement_cutoff=20, historical protocol | n<=35; dense payload<=8 MiB |
| v02_default | Public API, default cutoff=15 | Same caps |
| mask_isolated | Full 2^q mask enumeration, no API preprocessing | High modulus; q<=12 |
| edge_bitmask | Existing sorted-edge DP | n<=35 |
| edge_tuple | Existing modular/lex tuple adapter | n<=24 |
| cubic | Existing cubic DP correctness/performance control | n<=8 |

Caps are conservative benchmark selection policies, not measured memory limits
or solver impossibility claims. The public-API payload gate is conservative even
when a shortcut might avoid dense allocation. The isolated mask scan exposes a
mechanism cost; it has less preprocessing than a public API call. The edge tuple
adapter is a modular augmentation, not an unmodified literature implementation.
This milestone adds distributional coverage and a default-API control; it adds
no claim that the comparator set exhausts prior art.

## Correctness evidence

Every output undergoes a separately coded feasibility predicate. Every n<=12
case additionally uses a selected-subset exhaustive oracle. For larger powers
of three, any subsequence is strictly convex: for i<j<k,
3^k-3^j >= 2*3^j > 3^j-3^i. An independent index-sum DP over selected indices
therefore obtains the exact maximum-cardinality, lex-smallest answer. Its tiny
instances are exhaustively cross-checked, including non-high moduli.

Other larger inputs require agreement from at least two distinct algorithm
names and are labeled `cross_algorithm_agreement`, not independent proof.
These implementations have shared provenance; even cross-algorithm agreement
is weaker than an independent oracle. Any mismatch marks every measured cell
for that case MISMATCH. A lone unreferenced result becomes UNVERIFIED.

## Measurement and failure protocol

Each block/case/algorithm runs in a fresh child process. Seeded random ordering
mixes algorithms, cases and blocks. A warmup precedes all timings; reconstruction
is included, subprocess startup excluded. `runtime_ns` retains every repetition;
median, min, max and median absolute deviation are descriptive only. Tracemalloc
runs separately. Linux process peak RSS includes imports, warmup and all calls;
it is not solver-only payload. Windows RSS is null. Traced peak bytes and RSS
have different scopes. No hard memory cap is enforced.

The 60-second parent deadline covers **the entire child**, including startup,
warmup, every timing and the traced call. It is not a per-solve timing observation
or a censored solve-time estimate. A timeout produces TIMEOUT with no fabricated
runtime. Nonzero exits and malformed worker output produce ERROR. Prior cells
are checkpointed atomically after every job, with the original full execution
plan retained. The command exits 1 on mismatch/error, 2 on incomplete resource or
verification results, and 0 only on completed comparisons plus planned skips.

Source SHA256s, HEAD, working-tree state, platform, Python version, runner image,
CPU details and UTC collection time accompany every report. A mandatory byte
comparison to the pinned research commit rejects modification of both solvers,
both existing baseline modules and the historical benchmark, including dirty
files with an unchanged HEAD. Git checkout uses LF on both CI platforms.

## Analysis and reproduction

```bash
python -m unittest discover -s tests -p 'test_*.py' -v
python experiments/v03/benchmark_expanded.py --profile ci --plan-only --output m1_plan.json
python experiments/v03/benchmark_expanded.py --profile ci --blocks 2 --repetitions 3 --output m1_raw.json
python experiments/v03/benchmark_expanded.py --summarize m1_raw.json --output m1_summary.json
# Larger follow-up, same registered policy; do not merge it into the CI cohort:
python experiments/v03/benchmark_expanded.py --profile paper --blocks 3 --repetitions 5 --output m1_paper.json
```

The summary pairs baseline median/T1 median **within each process-block index**
on one runner, then takes the median ratio across completed blocks. These are
matched input/environment blocks, not simultaneous measurements. Summaries
preserve every case and baseline, missing pairs, and faster/slower/equal counts
by cohort, distribution and baseline. Partial blocks are visible but excluded
from complete-pair aggregates. An incomplete/interrupted report never yields
certified ratios. There is no pooled grand speedup, significance test, bootstrap
confidence claim, OS-versus-OS speed claim, or reclassification of old post-hoc
cases. The case table supplies the denominator even when comparisons fail.

Workflow `v03-benchmark-m1.yml` independently collects native Ubuntu and Windows
evidence with Python 3.13, two fresh-process blocks and three timings each.
Artifacts contain the pre-execution plan, raw JSON, descriptive summary and
hardware text, retained for 30 days. Archive artifacts for paper reproducibility
before expiration. The larger paper profile, repeated physical hosts, theorem
review and systematic prior-art coverage remain separate research gates.

## Acceptance

- PASS only after all new harness tests and existing exactness tests pass.
- PASS source-preservation gate; diff contains research additions only.
- PASS full CI-profile run with explicit skips, exact output verification and
  recoverable raw observations. Keep each native runner's evidence separate.
- Report observed finite results and limitations. This milestone does not
  certify T1 novelty, mathematical peer review, publishability or SOTA status.
