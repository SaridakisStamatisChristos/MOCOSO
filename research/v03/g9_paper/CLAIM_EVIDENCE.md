# Claim and evidence map

| Claim | Manuscript locus | Evidence | Limitation |
|---|---|---|---|
| O(n+H^(5/2) log²(h+2)) time | Theorem 1; Lemmas 4, 6, 7 | Explicit transition count and all-query bound | Wide-word model; h<n |
| O(H²) auxiliary words | Theorem 1; Section 7 | Matrix/event accounting; corrected output cursor | Excludes input and one output, not temporary copies; not RSS |
| Globally least whole optimal tuple | Lemmas 5, 7, 8 | Constrained-oracle correctness and complement order reversal | Requires fixed optimal cardinality |
| Original implementation violates space | Section 7 | h=0, A[i]=i², two Python output slices | Functional correctness remains separate |
| 80,283 complete comparisons | Section 8 | Preserved results.json histogram and audit.py category loops | 75,621 infeasible; finite corpus |
| 13,767 forced queries | Section 8 | Preserved counts.forced_scalar_queries | Not additional full-witness instances |
| Mutation counterexamples | Section 8 | results.json findings plus audit.py | Intentionally broken algorithms, not defects in corrected solver |
| General mechanisms precede G9 | Section 3 | Source registry, primary disclosures | Does not settle exact-theorem priority |
| G8 space-time comparison | Section 9 | research/v03/g8/G8_THEOREM_LAB.md at pinned snapshot | Comparison of stated theoretical bounds only |

All repository evidence is pinned to 43353e2b9a659d736b627788ec0c46554a090c75. New rerun metadata is separate from historical evidence. The manuscript is the canonical content source for PDF, DOCX, and LaTeX exports; references.bib is the bibliographic source.
