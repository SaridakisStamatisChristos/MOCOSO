# MOCOSO v0.3 closest-mechanism matrix

Dated initial pass: 2026-10-23. Not a systematic bibliographic review; confirm forward/backward citations and scholarly indices before asserting priority.

| Family or disclosed work | Closest mechanism | Shared with MOCOSO | What it does NOT establish here | Disposition |
|---|---|---|---|---|
| Evgeny Kluev, Stack Overflow answer, Dec 18 2013 | O(n^2 log n) longest convex subsequence from edges in increasing difference order | Strictly increasing differences, sorted directed edges, dynamic programming | Does not formulate index-sum residue or lex-optimal modular witness | Established unconstrained predecessor; do not claim edge ordering is new |
| Illinois CS374, lab 07b 2020 / DP tips 2024 | Cubic adjacent-pair state for longest convex subsequences | Pair-state structural recurrence | Does not settle MOCOSO residue, lex, or deficit | Established classical DP |
| Barrett, Jacob, Marathe, SIAM J. Computing 30(3) (2000), DOI 10.1137/S0097539798337716 | Formal-language-constrained paths with automata | Finite-state / path product methodology | Not a direct proof of the present convex/position-residue problem | General automata constraint prior art |
| Labeled direct product for string problems on graphs (2022) | Graph product for path-string constraints | Constraint composition in graph algorithms | Not a direct MOCOSO solver | General methodological background; screen full article |
| Euler distinct-part partitions; OEIS A000009; Andrews, Theory of Partitions | Product prod(1+x^i), distinct-part counting | Counts T1 omission choices | Classical counting, not new by itself | Requires explicit acknowledgment |
| v0.2 backward sweep, merged main 9cedac0 | O(n^2m+n log n) word time, O(n^2m) words, exact lex witness | Same full MOCOSO objective | Dense representation is a constant-factor space improvement, not new asymptotic complexity | Exact production baseline |
| v0.2 edge_dp.py | O(n^2 log n+n^2m) word-step description, O(n^2+nm) abstract states, n-bit lex masks | Same full MOCOSO objective | Does not solve T2 bit-efficient persistent lex representation | Exact independent baseline |
| v0.3 T1 prototype | Reachability-pruned distinct omissions, immutable suffix locality | Same exact objective **when U/2<m<=U** | Does not claim unconditional improvement or novelty outside that regime | Proof draft; independent math review pending |
| v0.3 tuple edge adapter | Kluev edge sweep augmented with residue/lex, equal-weight staging | Same exact objective | Tuple copies can take O(n) time and space per candidate; not asymptotic performance win | Correctness control, not novelty |

Source URLs:
- https://stackoverflow.com/questions/20664920/longest-convex-subsequence-in-an-array
- https://courses.physics.illinois.edu/cs374/fa2020/labs/sol/lab_07_b_sol.pdf
- https://courses.grainger.illinois.edu/cs374al1/sp2024/hw/DP_tips.pdf
- https://doi.org/10.1137/S0097539798337716
- https://link.springer.com/article/10.1007/s00453-022-00989-x
- https://oeis.org/A000009

Scope: links checked via indexed search and original disclosures where available. Scholarly references require bibliographic backward/forward-screening; absence of a direct hit is never proof of priority.
