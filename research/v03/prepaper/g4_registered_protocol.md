# G4 comparative study registration — before fresh CI measurements

**Registered:** 2026-10-24 UTC. **Coordinator:** Trillion Developer++ / evidence-gated G4. This is a prospective *within-project* protocol version 1, not an external preregistration. Target stack: v0.2 `9cedac0d0f860564d5ee1a9064b01ef56ac2a764`; T1 + M1 `7595130fecb1a21dc8ca8823d9ee8d5d136af97a`; G3 `53b2276c7ed450ba8c27adc0e1e02c1493b4e592`. All PRs unmerged, research branch derived from G3. Do not combine results across distinct code revisions without labeling them.

## Primary objective / non-goals

Measure exact full-witness equivalence, runtime distributions, resource peaks and cap/timeouts for T1 `solve_deficit`, G3 `solve_poly_deficit`, a **structurally distinct generic resource-constrained DAG DP** and public v0.2. Include both hard positive-optimum and trivial negative-optimum cases. Report every loss, skip and failure, no pooled SOTA claim. This is not a novelty tribunal, external peer review or paper manuscript.

## Cohort A: registered original M1 paper-profile workload (frozen)

Use unchanged `experiments/v03/benchmark_expanded.py` and `workloads_expanded.py`; `--profile paper --seed 20261023 --order-seed 713` specifies 146 cases and 7 algorithms, with per-block 808 executable comparisons and 214 registered skips. Perform **2 fresh-process blocks x 3 untraced repetitions** on Ubuntu and Windows (same within-runner methodology as historical M1 CI profile but with *146-case paper workload*). This is **a reduced-replication paper-profile audit**, NOT the original suggested intensive command `--blocks 3 --repetitions 5`. Preserve original 3x5 requirement as pending rather than mislabel this as full-intensity paper evidence. Each block cell has separate warmup and separate tracemalloc run. `--timeout 45` bounds the **entire child**. Retain ordered plan, every raw row, full verification labels, summary and metadata. An incomplete run is PARTIAL, not success.

If full paper profile proves too heavy for CI, retain checkpointed raw partial artifacts; disclose whether suite completed. Do not silently drop failed samples. Native Windows reports no Linux RSS measurement; tracemalloc is not RSS.

## Cohort B: G4 new comparative 4-algorithm 40-case matrix

`experiments/v03/benchmark_g4.py` injects new case generator, independent generic resource-DAG comparator and G3 solver *without editing* M1 benchmark source. Pin `--profile ci --seed 20261024 --order-seed 713 --blocks 2 --repetitions 3 --timeout 45` on Ubuntu and Windows. 10 fixed (n,h) pairs = (12,4),(12,8),(20,12),(25,15),(30,20),(40,25),(60,40),(75,50),(90,60),(1000,4); four input families per pair, total **40 cases** and **160 planned cells per block** = 320 per OS before registered skips.

Families: `superconvex` a_i=3^(i-1), strongly positive and all subsets convex; `prefix_spike` same but first value replaced by 3^(n+1), preserving suffix but invalidating some candidate crossings; `suffix_defect` same with last value negated, forcing empty answer after immutable-suffix contradiction; `alternating` signed periodic values, typically empty. Zero/empty results are never dropped.

Control types:
- `deficit`: frozen T1 exact DP + reachable enumeration;
- `g3_poly`: frozen G3 polynomial-deficit weighted-pair sweep;
- `rc_dag`: newly independent **generic forward pair-DAG DP** with explicit omitted-index cost and full tuple witnesses; no decreasing-threshold optimization and expensive tuple copies (not claimed fastest generic literature implementation). Registered skip if state cells >60,000, non-feasibility semantics unchanged;
- `v02_default`: frozen public production API with default complement cutoff, cap n<=25 and dense payload <=8MiB.

All algorithms must return identical **full lexicographic optimum index sequences** on completed comparable inputs; a disagreement is `MISMATCH`, not a performance sample. Every returned witness is independently validated using the M1 algebraic second-difference predicate. For n<=12 M1 uses full selected-subset enumeration; for exact powers-of-three superconvex family all n use a **separate minimal-cardinality omitted-sum DP oracle** with lex tie logic. Large non-superconvex cases have cross-algorithm agreement only, not an independent full oracle.

The resulting comparisons isolate benefits:
- T1 vs generic DP assesses an output enumerator vs general resource DP;
- G3 vs generic assesses impact of monotone sweep **but also tuple versus pointer representation**; therefore it is *not a controlled experiment isolating sweep alone*. Do NOT attribute entire ratio to the sweep.
- T1 vs G3 tests real practical crossover; a fixed asymptotic algorithm separation does not imply G3 wins for every n,h.

## Measurement and verification

Use full M1 protocol in a fresh interpreter per timed cell/block: one warmup, 3 untraced timings, separate traced heap run, min/median/max/MAD, Linux ru_maxrss (whole child, not solver-only) and null Windows RSS. Preserve OS-specific rows, exact source SHA256, checkout commit, runner image, input/plan hashes and all planned skips. Timeouts, errors, drift, mismatches and RESOURCE_LIMIT are distinct; **only complete comparable OK pairs are summarized**, and every missing denominator remains reported. Physical runner CPU is not controlled; medians on two blocks cannot yield statistical-significance claims.

## G4 pass criteria and further gates

- G4 checks: 4 native platform/version CI jobs for independent generic comparator and raw source freeze; targeted and M1-paper both native runners; no validity mismatch/errors; planned caps explicitly retained.
- A source hash check must ensure `modconvex.py`, `edge_dp.py`, original `deficit.py`, old M1 harness/workloads and G3 `poly_deficit.py` are identical to pinned ancestors.
- If a benchmark ends with resource or timeout, retain as partial and do not call its comparison PASS.
- Strong speedups over `rc_dag` **cannot** imply globally SOTA; code is a self-implemented semantic comparator, not a historically validated reference optimized baseline.
- G4 evaluated separately from G1 scientific priority, G2/G3 theorem correctness and G5 clean-room source/artifact rehash. Manuscript drafting is prohibited; G6 final independent GO/NO-GO remains withheld.

Raw artifact ZIPs may expire and must be preserved non-ephemerally during G5.
