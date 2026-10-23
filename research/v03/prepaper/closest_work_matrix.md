# G1 closest-work equivalence matrix — Knowledge Nexus independent review

**Date:** 2026-10-23 UTC. **Comparison target:** immutable `7595130fecb1a21dc8ca8823d9ee8d5d136af97a` of MOCOSO. Theorem `research/v03/t1_deficit_proof.md` is **candidate**, not accepted by this literature review. Sources P01–P13 are cataloged with original URLs and access limitations in `prior_art_catalog.md`.

## Formal MOCOSO target to prevent false equivalence

Given signed \(A=(a_1,\ldots,a_n)\), \(m\ge2\), select \(1\le i_1<\cdots<i_k\le n\), maximize \(k\) then minimize the **complete index tuple** lexicographically, subject to \(a_{i_{t+2}}-a_{i_{t+1}}>a_{i_{t+1}}-a_{i_t}\) and \(\sum_t i_t\equiv0\pmod m\). Empty admissible. T1 restricts \(U/2<m\le U\), \(U=n(n+1)/2\), \(h=U-m\), \(q=\min(n,h)\), and claims \(O(n+qh+qP_d(h))\) word time, \(O(qh+q)\) auxiliary words excluding input and final output. **These bounds are the codebase's proposed claim only.**

Define \(D_q(h)=|\{O\subseteq\{1,\ldots,q\}:\sum_{j\in O}j=h\}|\), thus \(D_q(h)\le P_d(h)\). Comparison must not substitute \(k\) from P01 (number of target subsets) with \(k\) from MOCOSO (witness length).

| Claim | Exact MOCOSO component | Closest original prior art | Equivalent part | Necessary difference | G1 classification |
|---|---|---|---|---|---|
| **C1** problem formulation | Signed value array, strict convex triples + **index** modular sum, length optimum and global lex tie | P05 convex subsequences; P06 constrained paths; P02 modular sums | Each constraint studied separately | No inspected source explicitly combines **all** MOCOSO requirements | **PARTIAL / problem-specific formulation not located**, priority unproven |
| **C2** general DP | Pair-/edge-state convex subsequence DP augmented with index-sum residue and lex witnesses | P05 explicit 2013 edge-difference ordering and DAG; P06 path constraints; P12 lex paths | Edge ordering, graph DP, constrained-path and lex objectives precede MOCOSO | An exact faithful MOCOSO-specific witness/certificate state may be an original implementation, but method building blocks are old | **OVERLAP in foundations**; specific packaging unresolved |
| **C3** complement | For \(m>U/2\), nonempty index sum equals \(m\), hence omitted indices total \(h=U-m\) | Elementary subset-sum complement of fixed universe; P02 modular subset classes; P07 distinct parts | Single possible positive multiple and complementary target sum are immediate from \(s\le U<2m\) | None of inspected P01/P02 explicitly states this exact MOCOSO parameter transformation | **OVERLAP in elementary technique**, application-specific statement possible but weak novelty |
| **C4** immutable-suffix locality | Omissions \(\subseteq[1,q]\); suffix \(q+1,\ldots,n\) fixed; check unaffected suffix triples once, only mutable-prefix and crossing triples per candidate | General fixed-variable/local-constraint reasoning; P04 extension-oracle pruning; P05 local triple predicate | When omissions are bounded, a local predicate can often be checked only where changes occur | No inspected source states **the exact q+2/q+3 triple boundary for this MOCOSO constraint** | **PARTIAL, application-specific lemma potentially distinctive**, scientific significance still unproved |
| **C5** enumerate omissions | Build reachable exact sums \(R[t,s]\), DFS only positive predecessors; generate distinct omission subsets without duplicates | **P01 Appendix B.1** exact-sum reachable DP + DFS; **P03 §6.2.3** same true-state pruning; P04 general flashlight search | **Direct structural equivalence of the reachability-plus-pruned DFS mechanism**; \(w_i=i\) is a simple special case | MOCOSO emits only exact-target omissions and optimizes convexity/lex instead of outputting all solutions; uses one best descriptor instead of P01's all-solutions storage | **OVERLAP / NOT A NOVEL ENUMERATION TECHNIQUE** |
| **C6** combined specialized bound | \(O(n+qh+qD_q(h))\), upper bounded by \(O(n+qh+qP_d(h))\), once-per-instance fixed suffix + per-partition local convexity | P01 \(O(q(h+D_q(h)))\) direct specialization of their \(O(n(t+k))\) all-solutions derivation (their implementation's **space** bound differs); P04 generic output-size charging; P07 count \(P_d\) | Reachability construction \(O(qh)\) and \(O(qD_q(h))\) candidate enumeration follow established work. Classical partition number upper bound comes from Euler product | MOCOSO can avoid scanning all \(n\) positions per candidate via the q+2 boundary, retaining only one optimal descriptor. **This combination may be a new explicit statement, not verified as novel asymptotic method.** | **PARTIAL / natural composition with application-specific locality**, priority and exact model unresolved |
| **C7** T2 persistent exact-lex / T3 structure | Unproved future space-time tradeoff, new restricted cases | P05 explicitly discusses witness back-pointer memory and reconstruction; P12 lex DAG paths; P11 low-space subset sum | Generic witness path storage/lex path techniques exist | No fully specified MOCOSO T2 or T3 theorem to compare at all | **UNRESOLVED / no contribution yet** |

## Direct mechanism reduction / adversarial collision test for C5–C6

Suppose we ignore the value-convexity test and take the ordered positive item multiset \(w_t=t\) for \(1\le t\le q\). Choosing an omission set in T1 is exactly the standard *all solutions to subset sum of target h* problem. Feed \(w_t=t\) and \(t=h\) into P01's Bellman table plus pointer-guided DFS. Every reachable branch represents the **same inclusion/exclusion choice tree** as MOCOSO's \(R[t,s]\)-guided backtracking. Structural difference: P01 may retain all output solution paths (and charges them to space), while T1's `deficit.py` evaluates each candidate and keeps a best omission tuple.

From the known DP/DFS schema, using `q` items and target `h`, the straightforward work decomposition is \(O(qh)\) for reachability plus \(O(qD_q(h))\) to visit candidate paths of length \(q\). Thus **the enumeration-only portion is not an independent new algorithmic advance**. To obtain the full T1 bound, one must separately argue that convexity checking of each candidate takes only \(O(q)\) instead of \(O(n)\), through MOCOSO's specific fixed-suffix lemma. The combination's correctness and detailed accounting belong to independent **G2**, while whether it is *research-novel* belongs to closest-work and significance judgment. A natural corollary can be useful without being a new general technique.

**Non-equivalences that MUST remain explicit:**
1. P01's all-solutions *storage* is not the same as streaming+single-optimum memory. In particular do not treat its \(O(n(t+k))\) **space** as direct prior for T1 \(O(qh+q)\) auxiliary space.
2. P02's modulo-p subset oracle is a different preprocessing model; its \(\widetilde O(p+c)\) notation is accompanied by a proof with \(O(n^2p)\) preprocessing and \(O(n^2)\) per query, and is **not** MOCOSO's candidate complexity for \(m=\Theta(n^2)\).
3. P03's subset-sum matching outputs valid cross-table matches, not a globally lex-smallest convex subsequence.
4. P04 is a survey of known enumeration techniques, not the original source of every constituent algorithm.
5. P05 solves the unconstrained convex subsequence problem; its \(O(n^2\log n)\) is **not** an \(m\)-residue-constrained MOCOSO bound.
6. \(P_d(h)\) counts distinct positive integer partitions; T1's valid omissions number \(D_q(h)\le P_d(h)\), not \(P_d(h)\) exactly in all instances.
7. Word-operation bounds and Python arbitrary-precision bit costs are different scientific claims.
8. None of the preceding demonstrates a published **full MOCOSO equivalence**; absence of a match in inspected texts is not global priority evidence.

## Cross-source evidence graph

- **E-01:** P05 → supports old unconstrained sorted-edge longest convex subsequence → qualifies C1 and undermines originality of C2.
- **E-02:** P01 → supports exact-target DP+DFS enumeration → directly overlaps C5, supplies major component of C6.
- **E-03:** P02 → supports modular subset-sum solution enumeration → overlaps residue-class enumeration, but *not* convex optimization.
- **E-04:** P03 → independently confirms DP predecessor pruning in another problem → supports known C5 mechanism (not mathematical verification of MOCOSO).
- **E-05:** P04 → contextualizes source-independent flashlight-search framework → C5 generic, survey evidence dependent on underlying antecedents.
- **E-06:** P07 → establishes distinct-parts generating function and counting terminology → C6 classical counting.
- **E-07:** MOCOSO candidate lemma → may distinguish C4; **unverified by G2**, no external independent primary equivalent located.
- **E-08:** G0 finite CI results → say nothing directly about novelty or mathematical proof; should not be used as C1/C6 originality evidence.

## Sources and reproducibility

Use the link/extent catalog in `prior_art_catalog.md`. This matrix is a mechanism-level comparison, not a formal reduction establishing theorem equivalence between **entire** scholarly problems. It was authored independently of the engineer's earlier summary, but the reviewer is still an AI-assisted research system rather than a formal external referee. **G1 result:** strongest potential distinctive element is the *problem-specific immutable-suffix locality and complete exact-lex T1 synthesis*, with no verified priority or demonstrated nontrivial theoretical separation. See `novelty_assessment.md` for gate disposition.
