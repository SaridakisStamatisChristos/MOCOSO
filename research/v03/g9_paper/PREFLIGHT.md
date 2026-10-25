# Contribution preflight

Date: 2026-10-24. Revised after priority snapshot b23ca44be7f5a0932c209b2b4f80a221830ed8b2; original implementation audit 43353e2b9a659d736b627788ec0c46554a090c75.
Paper type: theoretical algorithms technical note with computational audit.
Scope: corrected research-only solver, arbitrary signed integer values, high-modulus deficit regime. No venue or acceptance claim.

| Candidate claim | Assessment | Required framing |
|---|---|---|
| Inventing the sorted-difference sweep or its equal-difference order | OVERLAP | Attribute Kluev (2013); independently prove the lifted invariant |
| Inventing resource DP or canonical self-reduction | OVERLAP | Attribute prior methods; no general-method novelty |
| Inventing sparse O(k log N) oracle extraction | OVERLAP | Attribute Björklund–Kaski–Kowalik, ESA 2014 / full version 2015 |
| Published arbitrary-witness extraction is automatically canonical | REFUTED | Explicit set-family counterexample; prove ordered extraction separately |
| Inclusion-only ordered reconstruction is a new general principle | WEAK / unsupported | Proposition 9 is an elementary explanatory specialization, without a novelty claim |
| Specialized complete canonical-witness bound | SURVIVES as a proved upper bound | State regime, query accounting, wide-word and output model |
| First published theorem with these exact bounds | UNRESOLVED | Do not claim priority; bounded search only |
| Improving both time and memory over G8 | WEAK / misleading | Describe a space-time tradeoff against repository-stated G8 bounds |
| Original pinned Python solver meets quadratic auxiliary space | REFUTED | Counterfamily h=0; use corrected derivative |
| Practical speedup or broad application value | EVIDENCE-DEPENDENT | No performance/application claim from correctness tests |

Closest overlaps: Kluev supplies the sweep and tie order; Turner supplies exact-resource DP; Björklund–Kaski–Kowalik supply sparse inclusion-oracle extraction; Meeks distinguishes inclusion from arbitrary extension; Große et al. and Creignou et al. document canonical prefix construction; Wu et al. supply a temporal path representation. The surviving content is an incremental specialized composition: complement deficit, compulsory anchors, harmonic event count, constrained score invariant, complete order guarantee, and output accounting.

Collapse risks: an earlier equivalent specialized theorem; a tighter black-box transfer with the same canonical guarantee; absence of sufficient significance for a chosen venue. None is resolved by passing tests. The paper will be a draft technical note without firstness, optimality, SOTA, or submission-readiness claims.

The thirty-query source-specific investigation is preserved in ../g9_priority/SEARCH_LOG.md and PRIOR_ART_REPORT.md. This revision uses its inspected sources rather than presenting a new search as if it had been conducted during typesetting. No exact full theorem was identified within that scope. Strong mechanism overlap is established; worldwide priority is unresolved. The complete bound is independently derivable by the elementary composition in the report.
