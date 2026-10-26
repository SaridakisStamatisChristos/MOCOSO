# G11 engineering frontier: exact bounded-deficit routing

**Execution date:** 2026-10-27. **Parent:** RFP G10 PR #23, immutable head `55193723d6cb0144cb1485cd79155bd3b2fd1261`. This checkpoint documents a *new tested engineering composition*, not a new mathematical primitive, independent referee opinion, published theorem, or universal SOTA.

## Contract and algorithm

Input integer array `a[1..n]`, `n>=2`, integer `m>=2`, `U=n(n+1)/2`, `U/2<m<=U`, `h=U-m<n`. The result must maximize selected-index cardinality under exact sum `m` and strictly increasing differences of *consecutive selected values*, then minimize the **entire selected index tuple** lexicographically. Return empty if no feasible nonempty witness.

Research-only entry point `experiments/v03/g11_hybrid.py:solve_g11` uses **fixed, public thresholds**:

| h | Subsolver | Why |
|---|---|---|
| 0..18 | `solve_direct`: enumerates distinct positive omitted parts summing to h | Low combinatorial cost, no event DP |
| 19..64 | copied and output-slice-corrected G8 interval DP | Avoid repeated reconstruction score calls on bounded deficits |
| >=65 | original G10 direct-next DP | Preserve the proposed quadratic auxiliary-space bound for unbounded H |

These thresholds are engineering decisions, not proven globally optimal, trained adaptively or silently selected after reviewing each test output. No production dispatch is altered.

## Proof of composition (conditional on cited G8/G10 correctness)

In the high-modulus regime any nonempty selected sum divisible by `m` equals `m`, because it is positive and at most `U<2m`. Its omitted indices have **exact distinct-positive sum** `h`, lie among `[1,h]` and leave all `h+1,...,n` compulsory. The suffix strict-convexity test of consecutive compulsory triples ending at `k>=h+3` is necessary, and together with the convexity of the selected prefix through `p=min(n,h+2)` is sufficient. The two compulsory anchors connect the prefix to the suffix with no missing triple. This includes h=0 and boundary p=n, where no suffix remains.

Distinct-part recursion visits every increasing omitted tuple `Q=(q_1<...<q_t)` with sum h exactly once. The direct candidate's selected prefix is the complement in `[1,p]`. The algorithm keeps **minimum t** (maximum selected cardinality) and, among equal t, lexicographically **maximum Q**, which corresponds exactly to lexicographically **minimum entire selected tuple**. No candidate outside this omission enumeration exists. Only once, for the winning omission tuple, materialize one returned output tuple. The direct mode has O(n+C_18) operations (C_18 is an absolute finite enumeration constant) and O(C_18) auxiliary words; these are worst-case constant in h<=18 aside from the charged read-only input and emitted output.

For h=19..64 the independent G8 implementation is copied verbatim except its last assertion changes from `zip(selected,selected[1:],selected[2:])` to index-based reads. Output-sized tuple slices in that last assertion would violate input/output-excluded auxiliary-space accounting when n is unbounded; the new indexed form does not. Since h<=64 is a **fixed constant** in this mode, G8's finite core DP and persistent path nodes consume O(1) wide words *as n tends to infinity*. Their worst bounded size is a constant depending on the fixed threshold (not a practical small-memory guarantee).

For h>=65 the unchanged G10 wide-word theorem candidate supplies its correctness and `O(n+H^(5/2)log(h+2))` time / `O(H²)` auxiliary words. The composition therefore has the same asymptotic upper bound **if the G10 proof is correct**, with the h<=64 constant absorbed into big-O constants. This is a trivial bounded-domain dispatch closure property—not a stricter asymptotic upper bound, nor a globally novel algorithmic result.

## Independent verification, local

- 73,809 complete witness comparisons for n=2..8, ternary signed alphabet {-3,0,2}, with **selected-subset brute enumeration independent of omission partitions and DP**: zero mismatches.
- 1,200 high-bit signed-seed comparisons n up to 124 against the unchanged G10 implementation: zero mismatches.
- Boundary 18/19 and 64/65, h=0 large output and forced omission cases: zero mismatches in the initial 2026-10-27 local source-subset run.
- Original historical G8 and G10 are never modified.

**Local exploratory performance screen (not yet independent CI):** 171 fixed instances, 19 h values, 3 sizes and 3 families (strictly convex squares, powers of four, and terminal broken suffix). Five matched complete-answer repetitions, same process and host. G11 beat the corrected G8 on **102/171** cases; median corrected-G8/G11 median-ratio across all cases **1.127×**. It won **56/81** for h<=18 and **29/36** for h>=65; it *lost the majority* for h in 19..64 due additional routing overhead. Broken-suffix workloads had median G8/G11 ratio **0.795×**, a negative result not to be suppressed. These numbers are preliminary and must not be described as verified GitHub CI, external SOTA or statistical significance.

## Prospective GitHub evidence gate

The new workflow first runs all 6 `test_v03_g11_rfp_hybrid` independent tests on Linux/Windows and Python 3.11/3.13, checks historical source immutability, and **only then** executes the fixed smoke and full matched benchmarks. Results retain all cases, feasibility strata, every median and raw timing sample, environmental metadata and source SHA-256 hashes. The benchmark includes both the *unchanged original G8* and *output-validation-corrected G8*, to avoid winning merely because the baseline allocated prohibited output-sized temporary slices.

No CI outcome is claimed until checking the actual GitHub job and artifact. Do not merge automatically. Historical G9/G10 proof, manuscript and production remain unchanged.

## Deep theoretical priority and referee obligations

A narrowed source search finds substantial prior art for generic lexicographic resource-constrained path DP. In particular:

- Tellache, Meunier, Parmentier, *Linear Lexicographic Optimization and Preferential Bidding System*, *Transportation Science* 58(3) (2024), 597–613, DOI https://doi.org/10.1287/trsc.2022.0372, arXiv https://arxiv.org/abs/2201.08907 (2022). The authors explicitly extend resource-constrained longest-path tools to lexicographic path objectives. This is **positive prior art for the generic approach**.
- Irnich, Desaulniers, *Shortest Path Problems with Resource Constraints*, in *Column Generation* (2005), DOI https://doi.org/10.1007/0-387-25486-2_2. Classical extension and dominance framework.
- Björklund, Kaski, Kowalik, *Fast Witness Extraction Using a Decision Oracle*, ESA 2014, DOI https://doi.org/10.1007/978-3-662-44777-2_13. Sparse witness extraction is established machinery.

None of those abstract-level matches by itself proves the **exact G10 high-modulus, strict-convexity, globally canonical witness and joint H-bound theorem** is preexisting; neither does this search prove world novelty. A mathematical referee must inspect the resource-augmented, sorted-difference event proof and determine whether the specialized bound is a straightforward corollary of published generic results. G11 does not change that question, since it is only a constant-regime engineering selection.

## RFP status ledger

| Node | Status | Evidence | Remaining gate |
|---|---|---|---|
| G11 finite exactness | TESTED | 73,809 independent local exhaustive cases, 1,200 signed G10 comparisons | CI cross-platform recheck |
| G11 direct-regime proof | PROVED (conditional on elementary compulsory-suffix lemma) | Exhaustive distinct-part enumeration + tie complement equivalence | External reader may audit |
| G8 last validation auxiliary O(n) artifact | REFUTED | Selected tuple slices; repaired in new research derivative | CPython heap is not abstract word space |
| G11 worst-case bound | PROOF_SKETCH conditional on G10 | Fixed bounded dispatch + original G10 theorem | Independent G10 theorem review |
| G11 universally faster than G8 | REFUTED by benchmark losses | Broken suffix and bounded middle regime | No unconditional production routing |
| Novel generic lex path DP | PRIOR_ART_FOUND | Above published work | Attribution required |
| Exact high-modulus G10 global priority | POSSIBLY_NOVEL (unresolved) | Bounded targeted search | External theorem-level implication audit |

**RFP checkpoint:** PR #24 should remain a draft. The most valuable next action is external mathematical review of G10 or a separately validated implementation improvement on representative feasible workload distributions—not additional ungrounded SOTA claims.

## Execution continuation and CI defect, 2026-10-27

The first PR #24 workflow [40413443061](https://github.com/SaridakisStamatisChristos/MOCOSO/actions/runs/40413443061) **failed before executing any oracle tests**. Reproduced reason: the initial copied G8 derivative inserted a second module docstring before `from __future__ import annotations`, which Python forbids. Corrected by moving provenance to comments **ahead of the original docstring** in commit `0fb8a13ba98a2eba5690c449c0b8b45a61912ed2`. This was a packaging SyntaxError, not a semantic counterexample. The failure is retained in GitHub Actions and should not be represented as a passing run.

Second performance-specific correction: the top-level router originally scanned all values for type errors before delegating to subsolvers that scan the same array again. The revised router validates only modulus/range before dispatch, and delegates integer-value validation to the selected exact solver, in commit `8acd2b6ff58c3f33424612c4142db0c6ca042a48`. This preserves errors for noninteger inputs and eliminates a redundant O(n) scan. A local repeat of the same 171-case benchmark showed **117/171 wins** versus the corrected G8, median corrected-G8/G11 ratio **1.141x**. The terminal-fault family remained approximately at parity (median 0.990x), so uniform superiority is still false. These are repeated local observations and replace neither the earlier data nor prospective CI results.

A **second independent oracle**, separate from the G11 and G8/G10 implementations, was then executed locally: brute enumeration of distinct omitted index subsets of exact sum h and *full* selected-triple verification, not core truncation. It matched G11 on **56 high-deficit cases**, covering h=19,24,32,48,60,64,65; two n sizes; four value families. This targets both the G8-bounded and G10-unbounded branches, which small n<=8 oracle tests do not reach. The cross-platform CI suite now includes `tests/test_v03_g11_partition_oracle.py`.

**No performance result is VERIFIED_CI until the subsequent GitHub run passes and raw artifact checks.** No code or manuscript is merged, nor has any world-priority or universal SOTA claim been established.
