# Adversarial manuscript review and contribution stress test

Date: 2026-10-24. Reviewer scope: separate adversarial pass by the same AI assistant, with source and evidence checks. This is not an independent human reviewer, a separate model, or external peer review. No fictional reviewer identity or acceptance recommendation is provided.

## Reviewer 2 findings

| Severity | Location and challenge | Resolution or remaining risk |
|---|---|---|
| Major | Theorem 1: original implementation contradicts quadratic auxiliary space at h=0 | Resolved in scope: theorem names corrected algorithm; Section 7 preserves the explicit original counterfamily |
| Major | Lemma 5: endpoint and resource alone appear to forget the last difference | Resolved by an event-relative source invariant; equal-difference incoming edges to the source occur later |
| Major | Lemma 7: feasibility of a next omission need not be monotone | Resolved by distinguishing threshold from equality; explicit equality counterexample included |
| Major | Theorem 1: repeated feasibility queries could hide an extra n or H factor | Resolved: one suffix check; explicit 1+t(1+ceil(log2 H)) query bound; one matrix at a time |
| Major | Novelty: all general mechanisms are established | Unresolved as a publication-strength concern; title and all contribution prose narrowed to a specialized composition |
| Major | Earlier draft omitted the directly relevant ESA 2014 sparse-extraction result | Repaired: added full-version theorem, conference date, arbitrary-witness scope, and runtime-transfer assumptions |
| Major | Inclusion-only oracle might be mistaken for an arbitrary forced-prefix oracle | Repaired: Proposition 9 proves essentiality only along the greedy path; Meeks's distinction is explicit |
| Major | New Proposition 9 could merely rebrand standard self-reduction | Repaired: expressly elementary explanatory specialization, without a novelty claim |
| Moderate | Temporal path reduction could silently change maximum cardinality to minimum duration | Repaired: specify negative travel cost and exact gap resource; attribute adaptation as our inference |
| Moderate | Reduction checks might be confused with the optimized G9 implementation or merged into old counts | Repaired: separate subsection, snapshots, seed, corpus totals, batch scheduler, and explicit non-performance scope |
| Moderate | Section 8: test counts could double-count pair-DP checks or hide infeasible domination | Resolved: disjoint 80,283-instance table; 1,800 subset and 75,621 infeasible instances disclosed |
| Moderate | Section 8: independent could imply external/blinded verification | Resolved: same-session separately written methods explicitly stated |
| Moderate | Section 9: G8 comparison could imply both time and space improve | Resolved: extra time logarithm stated; G8 comparison labeled repository-stated theoretical bound |
| Moderate | Section 8: allocation probe could be mistaken for total memory | Resolved: reset point and validation-only scope stated, no RSS claim |
| Moderate | References: broad search cannot certify priority | Unresolved; explicit bounded-search and priority limitations, no firstness claim |
| Minor | Bibliography: Turner issue and online dates differ | Resolved: 2011 issue citation with 2012 online note |
| Minor | Reproduction mutates historical results.json | Resolved: disposable-checkout instruction and fresh rerun performed outside manuscript checkout |

## Contribution stress test

Strongest overlap case: credit Kluev's sweep and tie ordering, Turner's exact-resource template, Björklund–Kaski–Kowalik's sparse extraction, existing ordered self-reduction, and Wu's temporal expansion. Also credit the repository's preceding resource-lift and sparse-gap experiments. Remove all claims to invent these mechanisms, including Proposition 9's elementary ordered adaptation.

What remains: the specialized theorem for high-modulus value-convex subsequences, the core and harmonic gap count, an explicit constrained score invariant and complete-order proof, and the correction showing why output validation must be charged. The entire upper bound is derivable by an elementary combination of known methods with this structure. Its general-method novelty is therefore substantially overlapping, and its residual scientific contribution is modest and incremental.

Classification: **BOUNDED** mathematical contribution, **CONDITIONAL** publication significance.
Publication contribution gate: **REFRAME completed as a specialized technical note; submission readiness not established.** Draft compilation is allowed. Conditions remaining are author/expert review, a venue-appropriate significance case, and unresolved exact-theorem priority beyond the completed search scope. No unresolved mathematical defect was found in this manuscript review; this is not a machine-checked proof or external certification.

Propagation check: title, abstract, introduction, related work, theorem model, discussion, conclusion, artifact disclosure, and draft PR metadata all use the specialized-composition framing. No SOTA, optimality, world-first, blanket original-implementation compliance, or publication-ready claim remains.

## Five verdicts carried into the paper

1. Mathematical correctness: the corrected theorem is supported by the independent derivation; no counterexample found.
2. Implementation correctness: exact witnesses pass the preserved comparisons; original auxiliary-space claim is refuted; derivative repairs the identified allocation.
3. Asymptotic improvement: specialized quadratic-space tradeoff; no simultaneous time/space improvement over stated G8 bounds.
4. Literature priority: prior general mechanisms established; exact specialized-statement priority unresolved; full bound derivable by the documented composition.
5. Scientific significance: modest incremental technical-note contribution; no broad impact, practical superiority, or submission acceptance established.

The paper is an authored draft with evidence, not a decision to merge research code or submit a manuscript.
