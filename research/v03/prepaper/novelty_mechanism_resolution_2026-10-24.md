# MOCOSO v0.3 — G6 follow-on theoretical originality resolution

**2026-10-24 · Knowledge Nexus (mechanism/source graph) + SOTA Research Auditor (claim-level adversarial adjudication).**

**Scope:** The exactness and novelty of the **high-modulus MOCOSO polynomial-deficit algorithm**, not an overall claim of uniqueness of the mathematical problem. Frozen G3 source `53b2276c7ed450ba8c27adc0e1e02c1493b4e592`; G6 independent audit at `00d7f1870bbb3d35e1e62da1057c76ff4dde712d`. This additive review is stacked on G6 and preserves main, existing pull requests and research solvers. A newly written reference implementation is marked a **prior-art reconstruction**, not a new-literature discovery.

## Verdict, with quantifiers

1. **Strong G3 mechanism novelty: NOT DEFENSIBLE.** We construct a direct, explicit resource-budget lift of the **2013 sorted-convex-edge algorithm** using classical one-resource dynamic programming; it attains the same high-modulus `O(n+h^3)` bound **for optimum length**, with **better `O(h²)` auxiliary space**. Exact *global lexicographic witness* reconstruction using generic greedy self-reduction achieves `O(n+h^4)` time and `O(h²)` auxiliary space. This construction shows that no new primitive is needed to obtain the polynomial dependence on h, and creates an explicit nontrivial Pareto comparator not previously in MOCOSO. **We do NOT claim the exact combined statement appeared verbatim in 2013** or that it is legally anticipated as a patent claim; we establish algorithmic *compositional derivability* rather than prove global historical identity.
2. **Problem formulation / specific high-modulus local boundary: likely distinct within searched sources**, but no evidence it is a genuinely new computational *complexity class* or an original general theory. The exact q+2 crossing-triple boundary is a correct and useful application-specific lemma, obtainable by straightforward fixed-index logic. Its priority remains unknown, and the scientific-significance threshold for a high-selectivity theory paper is not crossed by that lemma alone.
3. **T1 reachable-sum-guided omission DFS: historically established mechanism.** Dutta–Rajasree's extended 2021/22 subset-sum exact-target enumeration and classic DP/DFS pruning supply it; stream-one-best storage and immutable-suffix checking are adaptations, not new enumeration machinery.
4. **Abstract algorithm correctness remains positive within its model**; this audit does not falsify G3's proof or the G4/G5 reproducibility record. But **theorem priority and performance superiority over optimized literature baselines are not established**.
5. **Decision:** RESEARCH NOVELTY BLOCKER RESOLVED NEGATIVELY FOR THE EXISTING STANDALONE G3 MECHANISM. **NO-GO for presenting current G3 as a fundamentally new algorithm or SOTA theorem.** Literature-level originality of the *particular application and theorem wording* remains **UNRESOLVED**, not disproven. A new, noncompositional result or honest methods/technical-report framing is needed.

## Primary evidence (sources are not interchangeable)

| ID | Independently consulted original | Exact supported component | Exact limitation |
|---|---|---|---|
| K13 | Evgeny Kluev (Dec 18, 2013), original answer, https://stackoverflow.com/questions/20664920/longest-convex-subsequence-in-an-array | Sort all ordered index pairs by difference `a_j-a_i`; second endpoint **descending on ties**; update DP best tail/endpoint for strictly increasing successive differences. Also gives explicit pair-vertex DAG. Claimed unconstrained O(n² log n) time | No selected-index modular sum, omission budget, or exact-full-lex constraint in that original answer |
| AT19 | Kyriakos Axiotis & Christos Tzamos (ICALP 2019), DOI https://doi.org/10.4230/LIPIcs.ICALP.2019.19 | Established capacitated DP on DAGs and generic capacity-expanded states. The article studies length-k resource/hop constraints and structured graph acceleration | **Not a proof AT19 has an explicit arbitrary omission-weight MOCOSO recurrence**; direct omission budget uses the standard *generic* additive-resource augmentation, not a claimed verbatim corollary of AT19's special theorems |
| CS10 | Camponogara & Shima (2010), https://doi.org/10.3217/jucs-016-03-0372 | Resource-constrained longest paths on DAGs and pseudopolynomial DP | Different graph and application; mechanism lineage, not an exact previous MOCOSO solution |
| DR21 | Dutta & Rajasree (expanded arXiv 2112.11020, 2021/22), https://arxiv.org/abs/2112.11020 | Exact-target reachable sum DP and predecessor-pruned DFS enumeration | Extended-paper Appendix B.1; not necessarily in shorter refereed proceedings; different all-output memory accounting |
| M19 | Axiotis–Tzamos original PDF and primary 2013 algorithm | A generic capacity dimension can multiply the transitions of an acyclic/ordered-event DP, and sorted-difference events already encode convexity | This composition is **proved below as our derivation**, not attributed as an explicit written theorem to either author |

### Independent source graph / causal chain

`K13 sorted differences + tie order` → *strict local convexity represented as an increasing-difference path without pair-state storage*.

`Classical exact resource DP` → *append a cost coordinate to every edge transition*.

`High-modulus complement identity` → *omission target h instead of selected-index target m; mandatory suffix and p-sized local core*.

These **three** edges together yield the exact alternative algorithm below. It is therefore unwarranted to assign G3's *resource lifting + convex edge sweep* an independent algorithm-priority claim merely because an earlier paper has not named this precise combined application.

**Independence caution:** G2/G3/G4/G5/G6 numerical proof/test reports all share MOCOSO's underlying cases. They do not establish independent historical novelty. K13, AT19, CS10 and DR21 are independent *algorithm-literature lineages*, and none alone proves the whole MOCOSO theorem predated it. This audit's alternative code is separately derived but authored in the same research session; it is not an outside peer review.

## Mathematical certificate: direct lifted sorted-edge algorithm

### Scope

For n≥2, signed `a[1..n]`, m≥2, and `U/2<m≤U`, define `h=U-m`, `q=min(n,h)`, `p=min(n,q+2)` and `W(t)=t(t+1)/2`. A **nonempty** modular selection must have index sum exactly m, so omitted indices sum h. Since no omitted index may exceed h, all `q+1..n` are mandatory.

If any ordinary triple ending at `k≥q+3` fails the strict convexity inequality `a_k+a_{k-2}>2a_{k-1}`, there is no nonempty feasible witness. Otherwise the only variable triples end inside the local prefix `1..p`; all later indices `p+1..n` are in the fixed suffix and can be appended.

### Omissions as additive *edge* weights

For two successive selected local indices `i<j`, let
\[
g(i,j)=W(\min(j-1,q))-W(\min(i,q)).
\]
This equals the sum of **omitted** indices strictly between the endpoints. Any edge skipping a compulsory index `>q` is forbidden. A first chosen index `i` pays source weight
\[
b(i)=W(\min(i-1,q)),
\]
and must satisfy `i≤q+1`. Termination after last local index `j` either requires `j=p` if `p>q`, or pays trailing omission cost `W(q)-W(j)` if `p=q=n`. Each omitted index is thus charged exactly once; all nonempty feasible selections of index sum m correspond to exactly-cost-h paths.

### Globally ordered edge-difference events

Make one event `e=(i,j)` for every `1≤i<j≤p`, with `d_e=a_j-a_i`; **sort in ascending `d_e`, and on equality in *descending* j**. Maintain `L[j,r]` = best number of selected core indices in an admissible prefix path ending at j with exact paid omission cost r, whose last edge belongs to the strictly earlier processed difference class (or is a singleton).

Initialize `L[i,b(i)]=1` for allowed singleton starts, all other cells unreachable. At event `(i,j)`, if the edge skips no compulsory index, scan each possible paid cost r, and relax
\[
L[j,r+g(i,j)]\gets\max\{L[j,r+g(i,j)],\,L[i,r]+1\},
\qquad r+g(i,j)\le h.
\]

**Strictness invariant:** Any predecessor edge into i on a chosen convex chain must have smaller difference than the current `d(i,j)`. Because the events are processed in ascending difference and a chained predecessor edge ending at i has smaller *second index* i than the current edge ending at j>i, **same-difference predecessor edges are processed later**, due to descending-second-index tie order. Hence no illegal equal-difference extension can occur. Conversely every chain of strictly increasing consecutive differences is visited in increasing event order, so the standard DP induction is complete. This is precisely the tie-order rationale visible in K13, now with a scalar nonnegative resource coordinate.

Among all valid terminals, add the constant selected suffix size `n-p`, demand exactly h paid omissions, and maximize selected length. If none exists, the empty tuple gives length 0. This returns the **exact optimal LENGTH**, not the lexicographically canonical tuple.

### Complexity and independently constructed space improvement

- O(n) fixed suffix comparison and output bookkeeping.
- `p(p-1)/2=O(p²)` edge events stored/sorted, O(p² log(p+1)) comparisons (wide-word assumption).
- Each event scans ≤h+1 resource values, total O(p²(h+1)).
- The only mutable DP is `p(h+1)` integer length cells; events store O(p²) records, plus O(p) constraints/workspace.

Therefore **optimum length** uses
\[
T_{\mathrm{len}}=O(n+p^2\log(p+1)+p^2(h+1)),\quad
S_{\mathrm{len}}=O(p^2+p(h+1))\ \text{auxiliary wide words}.
\]
When `h<n`, `p≤h+2`, so **`T_len=O(n+(h+1)^3)` and `S_len=O((h+1)^2)`**.

Compare to G3 exact full-lex pointer DP: **O(n+(h+1)^3) time, O((h+1)^3) auxiliary words** in this same restricted regime. The new independently-derived *length-only* algorithm matches G3's worst-case time order, with quadratically-bounded rather than cubically-bounded auxiliary space. This tradeoff is not evidence of original literature priority: it is an explicit standard lift of an earlier sorted-edge DP.

### Lexicographically smallest *complete* witness via self-reduction

First compute optimum nonempty length `L=best_length`. If L=0, return empty. Maintain sets of indices `S` explicitly forced selected and `E` explicitly forced omitted. For indices i=1..p, in increasing order:
- if i>q (compulsory), include it;
- otherwise evaluate `best_length` with `S∪{i}` forced included and E forced omitted, where forcing S forbids source/edge/terminal paths that skip an S-index, and omitting E forbids every selected endpoint in E;
- **include i** iff a feasible completion of length L remains; otherwise **omit i**.

Greedy proof: all completions considered have length L; among two different equal-cardinality sorted index tuples, their lex order is decided by their *first differing included index*. Thus a completion including the earliest undecided index, whenever one exists, is lexicographically smaller than every completion excluding it. Inductively greedy preserves at least one global optimum and yields the lexicographically smallest **complete** selected tuple. Append the obligatory suffix `p+1..n`.

At most p+1 independent length-oracle calls yield
\[
T_{\mathrm{fulllex}}=O(n+p^3\log(p+1)+p^3(h+1)),\quad
S_{\mathrm{fulllex}}=O(p^2+p(h+1))
\]
excluding existing input/final returned O(n) tuple. For h<n, this is **O(n+(h+1)^4) time and O((h+1)^2) auxiliary words** (vs G3's cubic/cubic). More execution time buys less auxiliary memory, preserving exactness and global lex optimization. **This is a technical Pareto statement between these specific algorithms, not a claimed first-known space bound.**

### Independently executable reconstruction evidence

Added `experiments/v03/edge_budget_lift.py` with `best_length` and `solve_lex_by_recomputation`. It does **not** import the G3 or G4 solvers. Added `tests/test_v03_edge_budget_lift.py` with direct selected-subset enumeration n=2..7, A∈{-1,0,1}^n, all high moduli: exactly **41,085** cases; 650 deterministic arbitrary huge signed cases; specified large-n powers-of-3 positive instances and forced-choice exactness tests. Initial standalone local prototype reproduced all 41,085 full optimal index tuples; independent GitHub CI results must be stated **only after actually observed**, not inferred from the file's presence.

The cost of pathological huge signed integers in Python is not constant per operation. No hard resident-memory ceiling/guaranteed forced-OOM certificate is claimed. Lex self-reduction is standard, not a new proof technique.

## Novelty matrix — exact classifications

| Claim | Mechanism-level evidence | Knowledge Nexus state | SOTA Research Auditor resolution |
|---|---|---|---|
| Target problem combination strictly convex selected triples + modular index sum + full lex | No reviewed source states the complete combination | **Tentative likely distinct** in scoped search | **UNRESOLVED historical priority**, can present as precise researched formulation |
| High-modulus omitted-sum equivalence and q+2 kernel boundary | Elementary h-sum bound and consecutive triples | **Established as mathematics, novelty weak** | **Incremental/application-specific** |
| T1 exact-target DP/DFS enumerator | DR21 direct structural predecessor enumeration | **Established prior mechanism** | **SUBSTANTIALLY OVERLAPPING** |
| G3 resource pair DP in O(n+h³) | Classical capacitated DAG DP + 2013 convex sorted-edge sweep; explicit independent budget lift above | **Strongly supported composition** | **NOT DEFENSIBLE AS NEW DP PRIMITIVE;** new exact formalization may be independently useful |
| Lex pointer tie optimality | Standard canonical DP tie & standard greedy self-reduction | **Established general patterns** | **NOT intrinsically original** |
| G3 faster than previous repository enumerator on a superconvex family | Formal separation and original G4 native measurements | **Supported only relative to particular T1 algorithm** | **Not a global complexity lower bound / literature superiority** |
| Independently reconstructed O(n+h³), O(h²) length-only bound | New explicit algorithm + proof here, rooted in K13/resource DP | **Mathematically supported conditional proof** | **No established historical priority**, not license for SOTA title |
| Independently reconstructed O(n+h⁴), O(h²) full-lex witness | Standard constrained feasibility self-reduction and separate exact recurrence | **Mathematically supported conditional proof** | **Potential application-specific Pareto point; global originality unresolved** |

## Adversarial checks and falsifiers

**A — False equivalence to AT19 must be rejected.** AT19's advertised graph capacity is a path length/hop-budget formulation, while the MOCOSO reduction has a *sum of omitted original position labels* as an edge resource. The shared mechanism is the generic capacity-expanded DP, not a literal theorem that the whole problem appeared in that paper.

**B — Equal edge differences must not be accidentally chained.** Sorting by increasing `d=a_j-a_i` and descending j on ties is necessary to prevent chains with equal d. Omitting the tie rule can silently break strict convexity on arithmetic-progression inputs. Our independently added tests include exact equality, ties, arbitrary signed data and forced-choice paths.

**C — Mandatory suffix must not be omitted.** A core edge skipping an index >q is forbidden, source starts after q+1 are forbidden, and terminal state includes required p; otherwise the weighted budget fails to represent a valid modular solution. The p=q=n case has different terminal trailing omission cost.

**D — Do not silently call length-only an exact full-witness solver.** The O(h²)-space bound is proved for optimum LENGTH directly; exact full lex uses p-times self-reduction with O(h⁴) work. Publishing O(h³)-time **full lex** and O(h²)-space from this reconstruction would be incorrect absent a different witness algorithm.

**E — Sorted-edge DP and omission-cost DP do not prove distinct algorithm priority simply because their composition was not found spelled out.** Conversely, no literature source was found giving a *verbatim* MOCOSO solution. Both claims require qualified wording.

**F — Source independence.** Evidence from repeated GitHub CI with same tests is correlated. K13 original answer + AT19/CS10 original publications are independent prior-work lineages, not multiple validations of MOCOSO's own theorem. The independent reconstruction is a conceptual comparator, not external peer-review.

## Decision and next exact scientific objective

**G6 NO-GO preserved for a new algorithm-theory contribution claiming G3 itself as a new mechanism.** Further generic benchmark polishing will not remove that originality defect.

To reopen theory novelty: formulate a mathematically *irreducible* theorem that beats the explicit lifted sorted-edge reference in the same full-lex complexity model (for example **O(n+h³) time with O(h²) auxiliary wide-word memory for exact full-lex witnesses**, or provably faster than cubic deficit time), with proof and counterexample testing; then search the literature specifically for such refined witness/lower-bound methods. **Those targets are open research objectives, not already obtained results.** An alternative is an application-/methods-focused note clearly treating the mechanism as inherited.

No full manuscript, paper release, merges, production rewrites, formal checker execution or global novelty guarantee authorized by this review.


## Unrestricted-modulus corollary — even broader novelty collision

The same historical edge-event method is not confined to high modulus. For arbitrary m>=2, use the sum of **selected original indices modulo m** as resource rather than the omitted-index sum. Let `L[j,r]` be best selected length ending at j with residue r, with singleton base `L[j,j mod m]=1`. Process all i<j in K13's ascending `a_j-a_i` / descending-j-on-tie event order and perform
\[
L[j,(r+j)\bmod m]\gets \max\{L[j,(r+j)\bmod m],1+L[i,r]\}.
\]
Final optimum is `max(0,max_j L[j,0])`. The preceding strict-event invariant proves correctness without tracking the last *pair* in the DP table: edge-difference event order already encodes the required previous-difference threshold. This is a standard **resource-coordinate lift of an existing DP**, not a claim that K13 published this modular extension.

The event list occupies O(n²) wide words, and the table contains only n*m entries. Time is **O(n²m+n²log(n+1))**, auxiliary **O(nm+n²)** wide words for **exact optimum LENGTH** over the **entire arbitrary-modulus problem**. The original MOCOSO v0.2 pair-state residue DP uses O(n²m) time and O(n²m) auxiliary words (both in its documented computational model). Thus the lifted edge method recovers the same leading time order with fewer auxiliary words for length-only. It also strengthens the conclusion that the basic convexity+resource-DP *mechanism* cannot be advertised as intrinsically new.

For the **full lexicographically least optimal tuple**, force inclusion/exclusion of each index and recompute the length oracle at most n times: **O(n³m+n³log(n+1)) time and O(nm+n²) auxiliary words**, excluding read-only input/final output. The first differing selected index resolves lex among equal-cardinality tuples, as proved for the deficit specialization. This is a standard time–space exchange, **not** the v0.2/G3 time guarantee for full lex.

An independent prototype was compared against 84,465 direct selected-subset exhaustive signed instances n=2..7 across *all* m=2..U+2, with no length mismatches. The added repository tests separately check the full lex tuple for 21,042 direct-oracle cases n=2..6, plus the original 41,085 high-modulus full-lex corpus. These test counts are not to be presented as newly observed repository CI success until the exact associated CI run is inspected.

**Originality implications:** this corollary is a useful *in-project* improvement in space-accounting and a publishable research question only if stronger independent priority/significance evidence is found. It is not yet an externally novel theorem; it instead demonstrates the reach of the classical K13 sorted-event/resource-state combination.
