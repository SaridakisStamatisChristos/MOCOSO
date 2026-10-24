# Claim and evidence map

| Claim | Manuscript locus | Evidence | Limitation |
|---|---|---|---|
| O(n+H^(5/2) log²(h+2)) time | Theorem 1; Lemmas 4, 6, 7 | Explicit transition count and all-query bound | Wide-word model; h<n |
| O(H²) auxiliary words | Theorem 1; Section 7 | Matrix/event accounting; corrected output cursor | Excludes input and one output, not temporary copies; not RSS |
| Globally least whole optimal tuple | Lemmas 5, 7, 8 | Constrained-oracle correctness and complement order reversal | Requires fixed optimal cardinality |
| Inclusion-only extraction preserves complete order | Proposition 9 | Essential-prefix invariant and monotone permitted sets | Uniform cardinality and known existence; no arbitrary extension oracle |
| O(k log N) extraction is established | Section 3 | Björklund–Kaski–Kowalik, full-version Theorem 1 | Arbitrary witness; does not prescribe our canonical order |
| Generic extraction is not automatically canonical | Section 6 | Explicit weight-five family and allowed partition | Abstract oracle family, not asserted to be realized by an array |
| Additional reduction experiments | Section 8 subsection | Priority results.json: 2,228 exhaustive families, 3,000 random families, 7,612 instances, 30,448 scores | Separate corpus; no unique-case total across audits; no timing inference |
| Original implementation violates space | Section 7 | h=0, A[i]=i², two Python output slices | Functional correctness remains separate |
| 80,283 complete comparisons | Section 8 | Preserved results.json histogram and audit.py category loops | 75,621 infeasible; finite corpus |
| 13,767 forced queries | Section 8 | Preserved counts.forced_scalar_queries | Not additional full-witness instances |
| Mutation counterexamples | Section 8 | results.json findings plus audit.py | Intentionally broken algorithms, not defects in corrected solver |
| General mechanisms precede G9 | Section 3 | Source registry, primary disclosures | Does not settle exact-theorem priority |
| G8 space-time comparison | Section 9 | research/v03/g8/G8_THEOREM_LAB.md at pinned snapshot | Comparison of stated theoretical bounds only |

The original audit evidence is pinned to 43353e2b9a659d736b627788ec0c46554a090c75. Priority investigation and reduction evidence are pinned to b23ca44be7f5a0932c209b2b4f80a221830ed8b2. The new revision rerun verifies the priority checks only; the original audit rerun remains historical metadata. Neither preserved corpus is overwritten. The manuscript is the canonical source for PDF, DOCX, and LaTeX; references.bib is the bibliographic source.
