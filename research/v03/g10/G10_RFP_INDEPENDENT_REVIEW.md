# G10 RFP adversarial audit and performance continuation

Date: 2026-10-26. Base: PR #22 commit `8b784e60c696a2c531bcfe306d9dfaab6b78ebaf`. This is a **self-contained adversarial examination and prototype comparison, not an outside referee report**.

## Locked mathematical claim

Signed integer values `a[1..n]`, n>=2, m>=2, U=n(n+1)/2, U/2<m<=U, h=U-m<n, H=h+1. Return the maximum-cardinality strictly value-convex selected indices, with entire tuple lexicographically least, and sum of selected indices exactly m, or empty when infeasible.

G10-N's proposed time O(n+H^(5/2) log(h+2)) and O(H²) auxiliary wide words are conditional on the paper's charged wide-word model, excluding input and one output. No priority, Python-RSS, fixed-word, or universal runtime claim.

## An adversarial second route: dynamic max-min pair semantics

At the start of processing an event with slope d, a state at endpoint i only includes paths whose final slope is strictly less than d: ties order endpoints descending. Two such histories at the same (i,r), with the same permitted forced omission Q, can be compared by

  (selected-prefix length, earliest omitted position outside Q),

ordered lexicographically with both coordinates maximized. If the same continuation is appended, selected length increases by an equal amount and the new earliest omission becomes `min(old_earliest, earliest_omission_in_extension)`; the map `z -> min(z,c)` is monotone nondecreasing. Hence the dominated pair cannot become preferable under any common continuation. Exact resource and endpoint make available suffix transitions identical.

This is a **different mathematical formulation** of the G10 proof, as a monotone pair extension over an event-ordered resource path. Its essential vulnerability is the tie order: without descending destination at equal slope the source can already have a last event with slope d. The previous candidate's monotonicity lemma thus survives this re-expression. External mathematical review is still missing, so status remains PROOF_SKETCH, not machine-verified.

## Independently enumerated arbitrary constrained oracle

The G10 inner oracle is instrumented from the actual source function (one source-level return substitution, no alternative DP). An **independent selected-subset enumeration** for n<=10 computes the exact pair `(max length, max earliest remaining omission)` under arbitrary Q and arbitrary first-allowed thresholds. Unlike whole-witness checks, this isolates the load-bearing dynamic-programming dominance claim.

2026-10-26 local run: **4,500** seeded cases, of which **3,970** exercised the inner oracle and **1,942** had nonempty feasible witnesses. The generated families include quadratic convex, powers-of-four, arbitrary signed up to 10^36, and arbitrary signed prefixes with explicitly convex suffixes. Zero mismatches in this bounded domain. This is finite **TESTED** evidence; it does not prove the general theorem.

### Mutation falsifier: lex direction matters

With `a=(0,0,-2,-2,-2,0)`, n=6, U=21, m=16, h=5, G10 returns `(1,4,5,6)`. If **only** the equal-cardinality DP tie comparator is reversed, the mutated solver returns `(2,3,5,6)`. Both are cardinality-4 convex witnesses with selected-index sum 16, but the latter is lexicographically worse. The new CI test executes this mutation and requires detection. Thus the oracle can detect a valid-but-noncanonical error; it is not merely checking feasibility.

## A distinct experimental implementation, G10-S

File `experiments/v03/g10_sparse_experimental.py` uses sparse dictionaries indexed by attained omitted-resource states, instead of G10's full (endpoint,resource) dense matrices. Its exact output is checked against the untouched G10 and independently enumerated subsets; the event-order and max-min logic are unchanged.

The **state count** remains O(H²) in the worst case, but Python dictionary operations admit average/amortized rather than a deterministic worst-case time guarantee. We do not transfer G10's deterministic asymptotic time claim to G10-S. Its Python overhead and real heap may be greater in dense regimes.

Local 2026-10-26 CPython exploratory comparison (184 matched cases, 3 warmup-free timed repetitions per method, generator seed 20261026, h up to 80): sparse G10 won **138/184** over dense G10 with median dense/sparse ratio **1.029**. Within the **75 feasible** cases it won **46/75**, median ratio **1.024**. Against G8, sparse G10 won only **23/75 feasible cases** with median G8/sparse ratio **0.834**. This is **not** SOTA; in particular powers-of-four and high-density states often regress, and some quadratic instances benefit considerably. One machine, no confidence intervals.

The prospective GitHub harness freezes the inherited smoke/CI/paper test families, adds fixed forced-omission tests, includes raw per-case repetitions and hash-provenance, and reports every win/loss stratified by feasible vs infeasible. The CI workflow uses Linux/Windows, Python 3.11/3.13. Read actual CI status before treating it as verified. No adaptive selector or production dispatch is added.

## More relevant prior art found in the follow-up

Existing general-purpose lexicographic path / bottleneck machinery means the DP pair's abstract mechanism must **not** be advertised as invented here.

- R. E. Burkard and F. Rendl, *Lexicographic bottleneck problems*, Operations Research Letters 10(5), 303–308 (1991), DOI [10.1016/0167-6377(91)90018-K](https://doi.org/10.1016/0167-6377(91)90018-K). Generic iterative lex-bottleneck solution.
- F. Della Croce, V. T. Paschos, A. Tsoukias, *An improved general procedure for lexicographic bottleneck problems*, Operations Research Letters 24(4), 187–194 (1999), DOI [10.1016/S0167-6377(99)00013-9](https://doi.org/10.1016/S0167-6377(99)00013-9). General vector-lifting procedure.
- N. E. H. Tellache, F. Meunier, A. Parmentier, *Linear Lexicographic Optimization and Preferential Bidding System*, 2022 preprint [arXiv:2201.08907](https://arxiv.org/abs/2201.08907) and published DOI [10.1287/trsc.2022.0372](https://doi.org/10.1287/trsc.2022.0372). **Especially close in methodology:** explicitly extends resource-constrained longest-path DP with lexicographic costs and dominance. Its problem model and results differ from the high-modulus convex subsequence problem, but general resource-constrained lexicographic path DP is preexisting.
- A. Björklund, P. Kaski, Ł. Kowalik, *Fast Witness Extraction Using a Decision Oracle*, ESA 2014, DOI [10.1007/978-3-662-44777-2_13](https://doi.org/10.1007/978-3-662-44777-2_13). Generic sparse witness extraction with O(k log n) inclusion-oracle queries. G10's direct next-coordinate is structurally different from that generic oracle count but not an unqualified witness-extraction invention.

These primary-source abstracts and exposed introductory discussion support **PRIOR_ART_FOUND for generic mechanisms**. They **do not establish** that a published theorem already states or implies the identical high-modulus lex-witness joint bound. For that narrow theorem: **POSSIBLY_NOVEL / priority unresolved**, pending fuller reading of technical appendices and an independent expert referee. An absence-of-identical-title search is not a rigorous implication analysis.

## Evidence ledger and admission controls

| Claim | State | Executed evidence | Blocker |
|---|---|---|---|
| G10 whole witnesses exact in bounded domain | TESTED | 219,441 past exhaustive comparisons plus 1,200 signed cases on pinned PR #22 | Not a proof |
| G10 inner constrained oracle | TESTED | 4,500 fresh selected-subset enumerations, >1,900 feasible | Unbounded case remains mathematical |
| Pair monotonicity with ordered events | PROOF_SKETCH | Monotone min extension and source event slope separation; mutation counterexample for wrong tie | External proof audit |
| G10-S sparse correctness | TESTED | 21,321 local ternary small cases and 2,500 signed differential cases, fixed omission instances | General proof by same DP invariant |
| G10-S uniform practical speedup | REFUTED | Local paired losses, especially against G8 on feasible | No production dispatch |
| Universal global SOTA | UNCHECKED | No exhaustive external comparison | Strongest comparator, venue, independent reviewer |
| Generic lex resource-constrained DP is new | REFUTED | 1991/1999/2022 research | Attribute predecessors |
| Exactly matching specialized high-modulus G10 bound appears in prior art | UNRESOLVED | Bounded directed literature review | Full theorem-level implication analysis |

**Next gate:** obtain a genuinely independent mathematical referee and compare the *specialized* H-dependent complexity against the strongest published results with exact input assumptions. Merge/release only what test evidence supports. This exercise does not silently rewrite PR #22, its proof, G9, or production.
