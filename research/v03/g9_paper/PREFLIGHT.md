# Contribution preflight

Date: 2026-10-24. Snapshot: 43353e2b9a659d736b627788ec0c46554a090c75.
Paper type: theoretical algorithms technical note with computational audit.
Scope: corrected research-only solver, arbitrary signed integer values, high-modulus deficit regime. No venue or acceptance claim.

| Candidate claim | Assessment | Required framing |
|---|---|---|
| Inventing the sorted-difference sweep or its equal-difference order | OVERLAP | Attribute Kluev (2013); independently prove the lifted invariant |
| Inventing resource DP or canonical self-reduction | OVERLAP | Attribute prior methods; no general-method novelty |
| Specialized complete canonical-witness bound | SURVIVES as a proved upper bound | State regime, query accounting, wide-word and output model |
| First published theorem with these exact bounds | UNRESOLVED | Do not claim priority; bounded search only |
| Improving both time and memory over G8 | WEAK / misleading | Describe a space-time tradeoff against repository-stated G8 bounds |
| Original pinned Python solver meets quadratic auxiliary space | REFUTED | Counterfamily h=0; use corrected derivative |
| Practical speedup or broad application value | EVIDENCE-DEPENDENT | No performance/application claim from correctness tests |

Closest overlaps: Kluev's public technical disclosure supplies the sweep and tie order; Turner's journal paper supplies an exact-resource DP template; Große, Rothe and Wechsung discuss lexicographic self-reduction. The surviving mathematical content is a problem-specific composition: complement deficit, two compulsory anchors, harmonic event count, constrained score oracle, sparse omission threshold reconstruction, and explicit output accounting.

Collapse risks: an earlier equivalent specialized theorem; a tighter black-box transfer with the same canonical guarantee; absence of sufficient significance for a chosen venue. None is resolved by passing tests. The paper will be a draft technical note without firstness, optimality, SOTA, or submission-readiness claims.

New search on this date repeated convex-subsequence/modular/index/lexicographic and sparse-witness/self-reduction queries; no exact theorem was identified in the inspected sources. Search coverage is incomplete. The broader source-by-source audit remains in ../g9_independent_audit/LITERATURE.md.
