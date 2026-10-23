# Prior-art search log — preliminary / bounded

Date: 2026-10-23. Research goal: distinguish truly new algorithmic bounds from known convex subsequence, automaton-product, and partition-enumeration methods. This initial log records publicly indexed web retrieval, NOT comprehensive searches of all scholarly indexes.

| Query family | Initial retrieval | Interpretation |
|---|---|---|
| longest convex subsequence Evgeny Kluev 2013 algorithm edges | https://stackoverflow.com/questions/20664920/longest-convex-subsequence-in-an-array | Earlier O(n^2 log n) unconstrained edge-order method located |
| longest convex subsequence classical cubic DP Illinois | https://courses.physics.illinois.edu/cs374/fa2020/labs/sol/lab_07_b_sol.pdf ; https://courses.grainger.illinois.edu/cs374al1/sp2024/hw/DP_tips.pdf | Classical pair-state method documented |
| formal language constrained paths Barrett Jacob Marathe | https://doi.org/10.1137/S0097539798337716 | Established regular-language constrained path methodology |
| distinct partitions generating function enumerating | https://oeis.org/A000009 ; https://mathworld.wolfram.com/EulerIdentity.html | Euler distinct-part generating function is established |
| subset-sum reachable backtracking, graph path lex comparison | Indexed search attempted; no decisive equivalent result established by this pass | **OPEN**: needs primary-paper screening, citations, and comparable algorithms |

Still required before M0:
1. Search DBLP, Semantic Scholar, OpenAlex, arXiv, Crossref and Google Scholar using exact/synonym queries: strictly convex subsequence, increasing adjacent differences, ordered-edge path, selected-position residues, constrained DAG longest paths, small-deficit complement, output-sensitive partition enumeration, exact lexicographic path with persistent reconstruction.
2. Download/read closest primary papers, compare problem definition and bounds at mechanism level, and follow citation chains in both directions.
3. Screen citations to the 2013 algorithm and the 2000 constrained-path work; search known partition enumeration algorithms for equivalent O(h^2+hP_d(h)) complexity.
4. Record all candidates, search date, hit counts, exclusion reasons, and exact paper versions.

Do not interpret this bounded web pass as proof that T1 or T2 is first or publishable.
