# Source-specific originality and implication audit

Date: 2026-10-24. Bounded live search and direct primary-source inspection. This
file distinguishes prior technique, an already stated exact theorem, and a theorem
we can now derive by combining prior techniques with elementary problem structure.

## Sources actually checked

| Source and precise locus | Verified overlap | Does it directly supply the entire G9 theorem? |
|---|---|---|
| [Evgeny Kluev, 18 Dec 2013, answer to Longest convex subsequence in an array](https://stackoverflow.com/questions/20664920/longest-convex-subsequence-in-an-array), numbered steps 1–6 and discussion | Same value-difference convexity; sorted pair differences; **descending second index on equal differences**; scalar endpoint sweep; immutable witness nodes and a midpoint-recomputation suggestion | No modulus/omission resource, deficit-dependent event count, or global full-index lex guarantee is given. It directly anticipates the sweep and event-order mechanism. This is an original public technical disclosure, not a peer-reviewed article. |
| [Lara Turner, Variants of the Shortest Path Problem, AOR 6, 91–104](https://journals.lib.unb.ca/index.php/AOR/article/download/18312/20525/24773), printed p.96, recurrence (23), Theorem 2 | Exact-resource DP on an acyclic digraph; O(T+M K R1...RK) time; ordinary predecessor reconstruction | With one resource R=h and unit negative edge costs, it supplies a standard resource optimization template. It does not itself identify MOCOSO's legal event graph, harmonic edge count, or canonical omission self-reduction. A naive last-two-indices DAG has many more transitions. |
| [Große, Rothe, Wechsung, A Note on the Complexity of Computing the Smallest Four-Coloring of Planar Graphs](https://arxiv.org/pdf/cs/0106045), v2 7 Feb 2006, §3, printed p.5 after Definition 3.2 | Explicit statement that self-reducible problems admit lexicographically first solutions through prefix oracle search | Establishes ancestry of canonical decision-to-search reconstruction, not this constraint oracle or the specific deficit cost. Its warning that efficient decision alone does not automatically yield canonical search reinforces the need to prove G9's constrained oracle. |
| [Creignou et al., A complexity theory for hard enumeration problems](https://doi.org/10.1016/j.dam.2019.02.025), DAM 268 (2019), §3.2, Proposition 6 | Extension queries construct solutions in lexicographic order | Supports standard extension-oracle ancestry. Does not state the specialized polynomial exponent or omission count. Proposition text was retrieved through indexed publisher content; direct publisher open returned HTTP 403, so deeper full-text examination of that article remains limited. |
| [Logan Nye, Universal Hirschberg for Width Bounded Dynamic Programs](https://arxiv.org/html/2512.10132v1), 10 Dec 2025, Theorem 1, §2.3, §5.5 | Claims general traceback under a frontier-width model, polynomial time, and a predetermined local tie rule | Does not give the G9 time exponent; deterministic local canonical choice is not automatically lexicographic order on the whole selected tuple. A representation/frontier and tie-preservation reduction would still be needed. This audit does not certify the preprint's theorem; no G9 proof relies on it. |
| [Jin, Vyas, Williams, Fast Low-Space Algorithms for Subset Sum](https://arxiv.org/abs/2011.03819), 2020 preprint / [SODA 2021](https://epubs.siam.org/doi/10.1137/1.9781611976465.106) | Exact subset-sum time–space tradeoffs; demonstrates that resource equality and low space are established research topics | Its problem lacks selected-order convexity and this full canonical objective. The problem statement and headline results do not supply an implication to G9. No generic black-box transfer is claimed. |
| [Jeff Erickson, Algorithms, Dynamic Programming chapter](https://jeffe.cs.illinois.edu/teaching/algorithms/book/03-dynprog.pdf), printed p.126, subsequence exercise (f) | The identical unweighted value-convex subsequence problem is a standard exercise | Establishes that the base problem is established, not a new MOCOSO invention. It does not add the modular index resource or claim the target theorem. |

Turner's PDF is labeled **2011**, with received/revised/accepted dates in 2011.
The [journal landing page](https://journals.lib.unb.ca/index.php/AOR/article/view/18312)
lists online publication on **2012-01-03**. These are compatible bibliographic dates;
the distinction should be preserved. The university report PDF is a different
28-page version; equation/theorem references above refer to the 14-page journal PDF.

An additional check, [Bogdanov and Trevisan, Average-Case Complexity, ECCC TR06-073](https://eccc.weizmann.ac.il/report/2006/073/download/),
§3.2, printed pp.18–19, explicitly presents binary search using a witness-order
threshold query. This is a survey confirmation of familiar ancestry, not the
primary novelty basis and not a specialized MOCOSO result.

## What the exact composition does and does not establish

An independently reconstructed derivation is short:

1. Convert nonempty modular feasibility to exact omitted weight h using U<2m.
2. Retain only the first h+2 indices, validate the compulsory suffix once, and
   count legal gaps by sum over omitted gap length u: at most h/u each.
3. Lift the previously disclosed sorted-difference sweep by an exact resource
   coordinate and forced-choice masks; this gives the constrained score oracle.
4. Encode the optimum's omitted set as at most sqrt(2h) increasing integers.
   For each integer, binary-search a monotone extension threshold. This is
   ordinary canonical self-reduction on a sparse witness representation.
5. Multiply the proved oracle cost by the proved query count and charge output.

This is enough to **derive** the corrected upper bounds from classical mechanisms
plus elementary MOCOSO-specific structural arguments. It is not enough to say that
a cited paper **previously stated or proved the exact theorem**. Conversely, absence
of a matching theorem statement does not turn this combination into a new general
algorithmic principle. A specialized theorem can be correct and useful while having
limited standalone novelty.

Within the repository, `experiments/v03/edge_budget_lift.py` already implements a
forced-selected/forced-omitted score oracle and index-by-index lex reconstruction;
G8 already uses sparse gaps. These files were read directly at the pinned commit.
G9's substantive incremental distinction is replacing per-mutable-index feasibility
decisions or stored witness histories with O(sqrt(H) log(H+1)) threshold queries.
That distinction deserves attribution and analysis, not a claim to invent
self-reduction, binary search, or witness-free score DP.

## Search coverage and limitations

Both available search engines were used, with primary-source follow-up. Query
families included:

- `longest convex subsequence increasing differences algorithm dynamic programming`
- `"longest convex subsequence" algorithm`
- `"longest convex subsequence" algorithm lexicographic`
- `"convex subsequence" "modular" algorithm`
- `"convex subsequence" modular deficit index sum`
- `"longest convex subsequence" "sum" indices`
- `lexicographically smallest witness self reducibility optimization binary search sparse solutions`
- `"sparse" "witness" "self-reduction" binary search`
- `"lexicographic" "self-reduction" "binary search" witness`
- `"resource constrained" "increasing paths" algorithm`
- Exact titles for Turner, canonical four-coloring self-reducibility, hard
  enumeration, and low-space Subset Sum; original source URLs for Kluev and Nye.

Some broad searches returned unrelated LIS material or functional-analysis
"convex subsequences"; these were excluded after distinguishing definitions.
An initial Turner download path and the university PDF follow-up failed; the
actual journal PDF was subsequently located and its recurrence and theorem read.
Publisher access to the hard-enumeration article was partial as stated above.
Search rankings, paywalls, terminology differences, unpublished work, and omitted
citation descendants prevent an exhaustive priority claim. Search-result crawl
dates were not treated as publication dates.

## Defensible contribution language

"For the specified high-modulus deficit regime, we give a specialized composition
of sorted-difference DP, exact-resource lifting, and canonical self-reduction,
with O(n+H^(5/2) log²(h+2)) time and O(H²) auxiliary wide-word space under the
explicit input/output model. We did not identify the same complete theorem in the
sources inspected on 2026-10-24. Its general mechanisms are established prior art."

Do not claim worldwide firstness, a new convex-subsequence DP primitive, generic
canonical traceback novelty, a lower-bound-optimal result, or SOTA without a
defined and comparable external baseline set. No paper-readiness GO follows.
