# G12: linear-time certificates for the two largest feasible witness lengths

**Date:** 2026-10-27. Research-only, stacked after PR #24. **Do not confuse a certified subclass with unrestricted global SOTA.** The general high-modulus research problem remains constrained by the separate G10/G11 assumptions and prior-art questions.

## Domain and contract

Let n>=2, signed integers `a_1..a_n`, integer m>=2, and U=n(n+1)/2 with U/2<m<=U and h=U-m<n. Maximize the number of nonempty selected original indices, subject to selected index sum divisible by m and strict increase of differences between consecutive *selected values*. Resolve ties by lexicographically least **entire selected index tuple**.

Return type of the **certificate**, `certify_up_to_two_omissions(a,m)`: an exact optimal tuple, including `()` when provably infeasible, or `None` if the optimum might require at least three omissions. `None` is abstention and **never** a no-solution claim.

The wrapper `solve_g12(a,m)` invokes the unchanged exact `solve_g11` only after `None`, preserving full exactness. `modconvex.solve` is untouched.

## Proposition G12-1: certified O(n)-time near-complete optimum

The certificate always returns the global canonical optimum if the optimum has at least n-2 selected positions. It may also prove infeasibility when the compulsory suffix itself violates strict convexity, or when h<=5 has no legal omission partition after all 0/1/2 cases have been exhausted. Otherwise it returns `None`, never a false certificate.

The certificate uses **O(n+h)=O(n)** charged wide-word time and **O(h+1)** auxiliary wide words beyond its input and single returned output tuple. This time bound is worst-case for any instance *including abstention*. The result is output-time optimal on nonempty certified instances because emitting n, n-1 or n-2 indices takes Omega(n) time. This does not imply a faster general exact algorithm.

### Proof

1. **Exact omission sum:** every nonempty selected index sum is positive and at most U<2m, hence divisible by m iff equal to m. The omitted set D has *distinct positive index sum* exactly h. Thus every omitted index <=h, all indices h+1..n compulsory. If the originally consecutive triple ending at k>=h+3 fails strict convexity, those compulsory elements persist consecutively in any selected witness; therefore **no nonempty feasible solution** exists.

2. **Only candidate lengths:** If |D|=0 then h=0, and the only candidate is the full index tuple. If |D|=1, D must be {h}. If |D|=2, D={u,v} with 1<=u<v and u+v=h; there are at most floor((h-1)/2) pairs. No h-dependent event sorting or score DP is necessary.

3. **Constant-time validity for a fixed one-/two-omission set Q:** Set p=min(n,h+2) and store the prefix count B[k] of failures of original consecutive triples (k-2,k-1,k), k<=p. All original triples ending at k>p are compulsory and have already been checked. Removing q from the selected tuple destroys an original adjacent triple iff its ending index k is in [q,q+2]; for two omissions, the union of the two ranges is computed via O(1) prefix-sum arithmetic with one overlap subtraction. Thus if an original failed triple outside these ranges exists, the candidate is invalid.

   Every remaining selected triple not equal to an original consecutive triple **spans at least one omitted index**. With at most two omissions, its original span has width <=4, so the triple's *last* index is at most q+4 for some omitted q. Inspect at most 4 possible triple endpoints per omission, and find their two preceding selected indices by scanning backwards over at most two omitted positions. This is O(1) work for |Q|<=2, detects every newly created selected triple, and checks each with exact signed arithmetic. Together with the unaffected-triple count, this condition is **necessary and sufficient** for strict convexity of the entire remaining sequence. A full rescan per candidate is unnecessary.

4. **Optimality and tie-breaking:** Test the length n candidate when h=0 and the unique n-1 candidate {h} for h>0. Only if n-1 fails, test every legal pair for n-2. Examine pair candidates in descending u. For fixed sum h, the first differing omitted index determines the order: the lexicographically greatest omission tuple yields the lexicographically **smallest selected tuple** among equal-size omitted sets. Hence the first feasible pair is the entire canonical optimum for n-2. If no pair exists and h<=5, no larger omission set can sum to h (smallest three distinct indices sum to 6), so no solution. If h>=6, report `None` unless a fixed-suffix contradiction already proves infeasibility.

5. **Bounds:** Validated input scan and compulsory suffix check are O(n). Build B[0..p] in O(h+1) words and time. Each of O(h) pairs takes O(1) time and O(1) temporary space; final output takes O(n) and one tuple. Because h<n, O(n+h)=O(n). The only surviving auxiliary structures are B of size O(h), and a constant-size endpoint set/list.

No call to G8, G10 or an unproven lemma is required for this **partial exact certification** theorem. The completeness of the fallback full G12 remains conditional on G11/G10 as separately documented.

## Independent execution and falsifiers

Actually executed *before upload* on a standalone copy of the certificate and an independent selected-mask exhaustive oracle:

- **73,809** signed ternary-array cases for n=2..8. On every non-`None` certificate, the whole tuple exactly equals the independent global optimum. On every `None` case, the independent optimum has at most n-3 indices. **Zero discrepancies**.
- **10,000** additional fixed-seed random signed arrays for n=2..11, checked against the same independent exhaustive oracle: **zero discrepancies**.
- Enumerated explicit one- and two-omission optimum families, equalities, empty output and domain boundaries.

These are **EXECUTED_LOCAL** and support the formal argument but do not imply machine-checked unbounded theorem. The new repository CI repeats the 73,809 independent cases across Windows/Ubuntu Python 3.11/3.13 and adds full G11 differential tests, regression boundary cases and a strong two-omission fixture.

### Mutation and counterexample obligation

A common incorrect optimization is to check only original consecutive triples outside the removed neighborhoods. That would miss **new triples bridged over a deletion**. For example, `a=(1,4,9,16,25)` has strictly increasing original consecutive differences. Deleting index 3 creates selected values `(1,4,16,25)`, whose final two differences are 12 and 9, so this one-omission candidate is **invalid**. For `m=12` (h=3), the correct best witness is the two-omission complement `(3,4,5)`. The regression suite asserts this explicitly. The G12 verifier *explicitly tests the changed triples*, rather than inferring convexity from original local failures alone. An independent mutation gate should verify this property on a concrete invalid case.

## Prospective benchmark

`benchmarks/g12_rfp_matched.py` compares **G12, G11, corrected G8, and G10** on exactly the previous 171-case synthetic cohort, the independent 240-case holdout, and 14 newly named guaranteed-feasible two-omission cases. Seed 271026; randomize matched run order, warmup, repeat exact whole-witness timings and retain **all** per-case losses, certificate categories, source SHA256 and platform metadata. No advantage is claimed before actual GitHub execution; no learner is trained on the holdout.

A certificate that abstains can impose overhead versus G8 or G11. The project must report that loss and should not promote G12 to production solely because it wins on handcrafted near-optimum examples.

## Literature and scope

This is a deliberately narrow and elementary near-complete-witness optimization, not an assertion that local post-deletion triple checking, distinct-sum enumeration or fixed-parameter enumeration was invented here. Generic lexicographic resource-constrained longest-path dominance already appears in Tellache–Meunier–Parmentier (2024), *Transportation Science* 58(3), DOI https://doi.org/10.1287/trsc.2022.0372. The exact G10 joint asymptotic bound still needs external mathematical review, and an incremental G12 certificate does not settle publication priority.

## Status

- **G12 partial exact certificate:** PROOF_SKETCH with complete human-checkable argument, TESTED 83,809 independent local cases; no formal checker.
- **G12 unrestricted exactness:** CONDITIONAL on unchanged G11/G10, TESTED where benchmark comparisons agree.
- **Linear-time subclass:** proved by the elementary argument above *subject to the same wide-word model*; no universal algorithmic SOTA claim.
- **Performance advantage:** UNCHECKED until new GitHub CI and held-out comparisons; do not infer success from complexity alone.
- **Publication novelty and human peer review:** UNRESOLVED.
