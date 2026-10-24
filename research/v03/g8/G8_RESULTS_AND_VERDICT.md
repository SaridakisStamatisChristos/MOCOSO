# G8 evidence-gated verdict — 2026-10-24

**Main result:** full-lex high-modulus h<n exact solution with O(n+(h+1)^(5/2) log(h+2)) wide-word time and O((h+1)^2 log(h+2)) auxiliary wide words, from harmonic eligible-gap counting plus immutable interval witness chains. Proof in G8_THEOREM_LAB.md; reproduction in experiments/v03/g8_persistent_intervals.py and tests/test_v03_g8_persistent_intervals.py.

| Independent gate | Verdict |
|---|---|
| Theorem correctness | COMPLETE HUMAN-CHECKABLE PROOF, not machine verified |
| Algorithm implementation | LOCAL PROTOTYPE VALIDATION: 21,321 exhaustive + 1,500 seeded full-tuple oracle comparisons and 160 edge-count cases. Verify committed CI separately before upgrading |
| Strength over project's G3 and G7 full-lex results | YES in high-deficit asymptotic time and auxiliary word-space upper bounds; a tightened analysis plus a research-only prototype |
| Original required O(n+h³) time and O(h²) auxiliary words | **OPEN**: G8 has log h extra auxiliary storage; do not drop it |
| Algorithmic novelty | COMPOSITION OF KNOWN DP AND BACKPOINTER PRIMITIVES; a specialized sharpened bound, not an independently established general algorithm breakthrough |
| Literature priority | UNRESOLVED after source-specific bounded search |
| Scientific significance | UNESTABLISHED beyond meaningful within-repo upper-bound improvement |
| Paper readiness | HOLD, and paper drafting explicitly prohibited by user |

G7 audit corrections are on this branch's *first* new commit. No production or G3–G7 executable solver modified. G8 is a separate unmerged research draft; all failed claims and counterexamples are preserved in G8_ADVERSARIAL_EVIDENCE.md. Do not merge.
