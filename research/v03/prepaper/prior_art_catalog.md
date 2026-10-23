# G1 prior-art catalog — independent Knowledge Nexus review

**Review date:** 2026-10-23 (UTC); **reviewer:** Knowledge Nexus plugin, separately invoked after engineering G0. This is a literature/novelty assessment, **not** an external human review and **not** G2 proof certification.
**Frozen MOCOSO mathematical/code target:** `7595130fecb1a21dc8ca8823d9ee8d5d136af97a` (stacked PR #3, downstream of draft PR #2). **G0 handoff reference:** `567c5bfca0eda13c8ff98045423f16038f37e609`. No solver edits or PR merges.

## Research scope and provenance method

Question: have the MOCOSO objective and proposed T1 high-modulus complement, immutable-suffix filtering, reachable-partition enumeration, or `O(n+qh+q P_d(h))` word bound already appeared, or are these direct applications of known results? Map separately C1 formulation, C2 unrestricted DP, C3 complement, C4 suffix locality, C5 exact-target reachable-sum DFS, C6 combined theorem, C7 unproved T2/T3.

**Evidence grades:** P = primary author's own full text inspected; A = publisher abstract/metadata or partial original accessible; S = survey/expository secondary; M = database/sequence metadata. A reviewed arXiv full text can be a primary document without implying peer review. Search snippets are not treated as full-paper inspection. All source URLs are public; URL access can change.

## Closest sources (date, type, inspected extent and direct mechanism)

### P01 — Dutta & Rajasree — *Efficient Reductions and Algorithms for Variants of Subset Sum* (2021 preprint; CALDAM 2022 related proceedings)
- **Primary full text inspected:** https://arxiv.org/abs/2112.11020, particularly Appendix B.1, lines corresponding to the subsection *Trivial solution for k-SSSUM*. The corresponding **peer-reviewed conference publication** is titled *Algebraic Algorithms for Variants of Subset Sum*, Pranjal Dutta and Mahesh Sreekumar Rajasree, LNCS 13179, 237–251, first online 2022-01-24, DOI https://doi.org/10.1007/978-3-030-95018-7_19 . Publisher page/abstract inspected: https://link.springer.com/chapter/10.1007/978-3-030-95018-7_19 . **Do not assume Appendix B.1 appears in the paywalled conference chapter:** it is directly verified in the longer arXiv version, not the inaccessible proceedings full text.
- **Exact relevant mechanism:** Bellman reachability `S((a_1..a_j),t)` table; add predecessor include/exclude pointers to attainable states; enumerate all exact-target subsets by DFS through its directed acyclic graph. Authors explicitly derive `O(n(t+k))` total time **and space** for their all-solutions implementation where `k` denotes solutions. This establishes the core *reachable exact-sum DP + DFS solution enumeration* architecture before MOCOSO.
- **Scope difference:** arbitrary positive item weights and exact target, not strictly convex subsequences or maximal length/full lex tie under index-sum modulo. Their stated space includes all discovered solutions; MOCOSO streams candidates and keeps one witness, so do not assert the space bounds are identical. **Lineage group:** SSUM-enumeration independent research.
- **Impacts:** C5 strongly; C6 strongly weakens mechanism novelty. **Originality of combination not settled.**

### P02 — Allcock, Hamoudi, Joux, Klingelhöfer, Santha — *Classical and Quantum Algorithms for Variants of Subset-Sum via Dynamic Programming*
- **Primary full text inspected:** https://arxiv.org/abs/2111.07059 and versioned author PDF https://arxiv.org/pdf/2111.07059 (PDF page 14 visually inspected). First arXiv posting 2021-11-13, inspected PDF v2 dated July 2022; later arXiv HTML version date differs, so pin version when citing a theorem.
- **Exact relevant mechanism:** Section 3.1, Theorem 3.5 and Corollary 3.6: preprocessing for a count DP indexed by selected-item sum **modulo p**, then recovering/enumerating subsets in a specified modular sum class. Corollary reports \(\widetilde O(p+c)\) in its stated regime; the original proof explicitly contains \(O(n^2p)\) preprocessing and \(O(n^2)\) per selected subset, so do **not** transfer its softened notation uncritically to arbitrary MOCOSO `n,m`. Explicit notion of modular subset enumeration is **old**.
- **Scope difference:** cardinalities modulo p and ordered subset access; no convex selected-value triple constraint, no high-deficit small-h observation, no MOCOSO objective. **Lineage group:** independent modular-sum enumeration; not independent support for MOCOSO proof.
- **Impacts:** C1/C3 context, C5 overlap, T2 exact witness/rank related conceptual prior art.

### P03 — Wu et al. — *The Subset Sum Matching Problem*
- **Primary full text inspected:** https://arxiv.org/abs/2508.19218 , originally dated 2025-08-26, Section 6.2.2–6.2.3 and Theorem 6.4. Journal version (2026): https://journals.sagepub.com/doi/10.3233/FAIA250892 ; publisher rendering was intermittently unavailable, arXiv body was inspected.
- **Relevant mechanism:** two reachability tables for subset sums, then backtrack through true-valued include/exclude DP predecessors; prune branches with false states; use the paths to recover compatible subsets. **This is another independent published exposition of the precise pruning pattern.**
- **Scope difference:** two-sided subset matching; not MOCOSO or the high-modulus deficit bound. Theorem 6.4's bound concerns an exact *matching* subproblem; do not equate it with enumeration of all MOCOSO candidates. **Lineage group:** SSMP paper, independent problem application.
- **Impacts:** C5 overlap/strong corroboration of standard mechanism.

### P04 — Conte, Kurita, Marino, Punzi, Uno, Wasa — *Designing Output Sensitive Algorithms for Subgraph Enumeration*
- **Survey full text inspected:** https://drops.dagstuhl.de/storage/01oasics/oasics-vol132-grossis-festschrift/html/OASIcs.Grossi.19/OASIcs.Grossi.19.html ; DOI https://doi.org/10.4230/OASIcs.Grossi.19 . 2025 OASIcs.
- **Relevant mechanism:** §4.3 'flashlight search' formalizes extension-oracle-guided include/exclude partition search: recur only if a branch has solutions, charge explored nodes to output leaves, bound unary paths by depth. This is the general *prune unreachable search branches before DFS* technique, rather than a direct MOCOSO predecessor. §4.1.1 additionally covers subsets of bounded sum (inequality rather than exact-target).
- **Classification:** S/survey. **Do not count cited predecessor techniques as independent mathematical discoveries from the review itself.**
- **Impacts:** explains why C5's output-sensitive charging argument is a generic known enumeration method.

### P05 — Kluev — *Longest convex subsequence in an array*, direct algorithm disclosure (2013)
- **Original firsthand answer inspected:** https://stackoverflow.com/questions/20664920/longest-convex-subsequence-in-an-array ; answer dated 2013-12-18. Directly converts convexity to strictly increasing edge differences, sorts \(O(n^2)\) candidate edges and sweeps to attain \(O(n^2\log n)\) unconstrained longest convex subsequence. Also sketches predecessor-node reconstruction and an approach to reduce witness-chain storage.
- **Status:** primary public algorithm disclosure, **not peer-reviewed journal work**. Important historical priority even without journal publication.
- **Scope difference:** no index-sum modulo, globally lex-smallest full-index witness requirement. The codebase's residue DP cannot claim that sorted-edge convexity itself is new. C2 overlaps; any T2 path-storage proposal must screen the answer's described space-saving reconstruction trick.

### P06 — Barrett, Jacob & Marathe — *Formal-Language-Constrained Path Problems* (2000)
- **Publisher-authored abstract inspected (full journal article not obtained):** https://epubs.siam.org/doi/10.1137/S0097539798337716 ; SIAM J. Comput. 30(3):809–837 (2000).
- **Relevant mechanism:** formal-language/regular-automaton constraints on graph paths with known polynomial algorithms. General state-product/path constraint baseline, **not** proof of the specific MOCOSO recurrence or modular objective.
- **Status:** A/abstract. Do not claim full-text structural equivalence or exact complexity bound not checked in article body. **Impacts:** C2 conceptual predecessor; citation chain still incomplete.

### P07 — Euler distinct-part partition numbers / OEIS A000009
- **Mathematical reference inspected:** https://oeis.org/A000009 : \(P_d(h)\) is coefficient of \(\prod_{i\ge 1}(1+x^i)\); Euler's distinct-part vs odd-part identity is classical. Bibliographic refs include Andrews, *The Theory of Partitions*.
- **Status:** M/authoritative sequence metadata, not an original paper/modern complexity theorem. The generating-function bound in T1 must not be sold as a new combinatorial object or novel generating function. **Impacts:** C3/C6 classical combinatorial backdrop.

### P08 — Zoghbi & Stojmenović — *Fast Algorithms for Generating Integer Partitions* (received 1998; journal Vol.70)
- **Publisher abstract only inspected:** DOI https://doi.org/10.1080/00207169808804755 ; abstract describes generation of unrestricted integer partitions in lexicographic and anti-lexicographic order with constant average delay, output cost excluded. Journal bibliographic dates/online-digital dates differ; use original-received 1998 for historical comparison and verify print year in definitive PDF.
- **Scope difference:** unrestricted partitions, not exact target sums over distinct labels in \([1,q]\) and not MOCOSO. Supports the broad maturity of partition enumeration only. **Status:** A, relevant but indirect.

### P09 — Büchel, Gilleßen & Witt — *An Output-Sensitive Algorithm to Partition a Sequence of Integers into Subsets with Equal Sums* (2019)
- **Original publisher abstract/metadata inspected:** DOI https://doi.org/10.23638/DMTCS-20-2-18 , https://dmtcs.episciences.org/en/articles/4994 ; 2019-01-24. Specific partition of \(\{1,\ldots,n\}\) into \(k\) disjoint equal-sum blocks; differs from selecting one complement of sum \(h\) and convexity filter.
- **Status:** A/abstract, not full-paper equation-level inspection. Interesting nearby restricted-integer structure but **not** a direct algorithm equivalence.

### P10 — Koiliaris & Xu, *A Faster Pseudopolynomial Time Algorithm for Subset Sum* (2017); Bringmann, *A Near-Linear Pseudopolynomial Time Algorithm for Subset Sum* (2017)
- **Original conference abstract inspected:** https://doi.org/10.1137/1.9781611974782.68 and https://doi.org/10.1137/1.9781611974782.69 . These improve decision/reachable-sums complexity relative to Bellman for general weights. They do **not** directly provide a streaming exhaustive candidate filter for MOCOSO.
- **Status:** A, contextual alternative `qh` precomputation; a claimed optimal or best-possible subset-sum DP preprocessing bound would require comparing these regimes. **Lineage:** algorithms for reachable sums.

### P11 — Jin, Vyas & Williams — *Fast Low-Space Algorithms for Subset Sum* (2020 arXiv / SODA 2021)
- **Original abstract inspected:** https://arxiv.org/abs/2011.03819 ; DOI https://doi.org/10.1137/1.9781611976465.106 . Shows substantially lower-space variants of subset-sum decision/reconstruction. **Not** a direct low-memory theorem for the MOCOSO lex-convex residue problem. T2-related caution.
- **Status:** A.

### P12 — 1995 *Fast Parallel Algorithms for All-Sources Lexicographic Search and Path-Algebra Problems*
- **Publisher abstract located but full text unavailable:** https://doi.org/10.1006/jagm.1995.1025 . The abstract includes lexmin paths on DAGs and lexmax longest paths on weighted DAGs in a general path-algebra framework. It is **not proof of a drop-in exact lex witness for MOCOSO**. **Status:** A, unresolved G1/T2 comparison.

### P13 — Chan, *Derandomizing Pseudopolynomial Algorithms for Subset Sum*, SODA 2026
- **Publisher abstract inspected:** https://doi.org/10.1137/1.9781611978971.131 ; improved reachable-subset-sum algorithm, with citations to output-sensitive target-sum results. **Decision not enumeration of all distinct solutions.** Screen if T1+ claims improved reachability, not as direct invalidation of current T1 composite time.
- **Status:** A, broad 2026 state of field.

## Search coverage / negative findings, 2026-10-23

Searches were performed on general web indexes with site filters and direct publisher/arXiv pages, including variants of *longest convex subsequence*, *increasing adjacent differences*, *modular selected-position sum*, *longest path under residue and lex constraints*, *subset-sum reachable-state backtracking all solutions*, *distinct-part output-sensitive partitions*, *complement parameterization*, and *lexicographic DAG witnesses*. Accessible first-party surfaces inspected: publisher pages (Springer, SIAM, OASIcs, arXiv, OEIS), DBLP CALDAM 2022 listing, arXiv full-text sections, and firsthand 2013 algorithm post. Site-restricted exploratory queries for OpenAlex, Semantic Scholar, Crossref and Google Scholar **did not produce an exhaustively inspectable result set**; those databases were **not systematically traversed by their native search APIs**. No reliable hit counts, exhaustive backward/forward citation network, or worldwide negative-proof claim are available.

**Negative finding with strictly bounded scope:** Within the documents actually examined, no source was identified that explicitly states **the entire** MOCOSO optimization problem with arbitrary signed input values, strict convex triples, modular **index** sum, maximal length and global lex-smallest witness, together with the specific high-modulus T1 bound. This is **not** proof of originality, nor an endorsement of MOCOSO theorem correctness.

**Important positive finding:** Exact-target subset enumeration via reachable-state DP and DFS predates MOCOSO by years (P01); modular subset enumeration predates it (P02); enumeration pruning is a general established technique (P04). A claim that C5 is new is contradicted by accessible primary text.

## Citation independence

P01 and its Springer chapter are the **same author/work lineage** (do not double count); P02 is a separate research team, P03 independent modern application, and P04 a survey tracing generic mechanisms (not an independent original discovery). Bellman 1957 as discussed by P01/P10/P11 is shared underlying classical work. OEIS and Euler/Andrews are one classic distinct-part combinatorics lineage, not multiple independent confirmations of novelty.

## Outstanding exact screening needs

Full-text access to P06, P08, P09, P12; direct bibliometric query/citation traversal for closest paper families; careful release/version reconciliation of P02 and P01, plus adjacent indexed-only work. Formal novelty clearance is **NOT GRANTED** on this incomplete, strongly overlapping record. See `closest_work_matrix.md` and `novelty_assessment.md`.
