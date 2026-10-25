# G8 theorem laboratory — sparse-gap full-lex witness compression

Date: 2026-10-24. Base: unmerged G7 PR #13 at e8ff4846968699488a3cba6f995dbbb19a038be3. Not a paper draft, a machine-checked proof, or a priority claim.

## Canonical problem

Given n>=2, arbitrary signed integers a[1..n], m>=2, U=n(n+1)/2, and U/2<m<=U, put h=U-m<n and H=h+1. Return the maximum-cardinality nonempty increasing selected-index tuple satisfying both divisibility of its index sum by m and strictly increasing consecutive selected value differences. Break cardinality ties by the **lexicographically least entire selected tuple**. Return empty only if no nonempty feasible tuple exists.

### G8-T (complete human-checkable proof, not formal checker)

The research solver in experiments/v03/g8_persistent_intervals.py computes the stated tuple using

\[
\boxed{T=O(n+H^{5/2}\log(h+2)), \quad S=O(H^2\log(h+2))}
\]

unit **wide-word** operations and auxiliary wide words, respectively, excluding input and returned output. The abstraction requires signed input values and intermediate differences, indices, counters, pointers and addresses each to fit one charged wide word. It is not an assertion of bounded fixed-word costs or Python RSS bounds. This is a strictly subcubic deficit-time upper bound and strictly better within the project's prior full-lex bounds for h<n, but **not the originally requested O(n+H^3)-time/O(H^2)-space pair**, because logarithmic excess memory remains.

## Proof dependency graph: L1 -> L2 -> L3 -> L4 -> L5

**L1. Exact high-modulus complement and compulsory suffix (inherited, proved).**
Any nonempty selected-index sum s is between 1 and U<2m and divisible by m; hence s=m and the omitted distinct original indices sum exactly h. Therefore omitted indices cannot exceed h, and every position h+1..n is compulsory. Set p=min(n,h+2), so h<n implies p>h and p belongs to every nonempty feasible tuple. Any triple whose last selected position is >=h+3 is a fixed adjacent suffix triple, checked once in O(n) time; remaining triples occur within indices <=p. For a starting index i, omitted initial indices are 1..i-1 at cost W(i-1), W(t)=t(t+1)/2. A legal edge i<j skips exactly i+1..j-1, disallowing any skip of compulsory indices.

**L2. Sparse eligible weighted gaps (new tightened bound, proved).**
For a nonadjacent edge j=i+t+1 with t>=1 skipped indices, the omitted-index sum is exactly

\[
g(i,j)=\sum_{k=i+1}^{j-1}k=ti+t(t+1)/2.
\]

A feasible partial witness cannot use g(i,j)>h. Since i>=1, feasibility implies t(t+3)/2<=h and thus t=O(sqrt(H)). For fixed t, feasibility also implies ti<=h, giving at most floor(h/t) possible sources i. There are at most p-1=O(H) adjacent edges. Consequently, with M the number of eligible edges,

\[
M\le p-1+\sum_{t=1}^{\lfloor\sqrt{2h}\rfloor}
\lfloor h/t\rfloor
=O(H\log(h+2)).
\]

The bound also holds when p=n<h+2. For a fixed i, g(i,j) is nondecreasing with j, and once an edge skips a compulsory index, every later destination also does. Thus the sparse generation loop can break safely after at most one rejected destination per source: its work is O(M+p), and sorting costs O(M log(M+1)). An overbudget edge cannot occur in any feasible prefix; deleting it cannot alter exactness. This crucially bounds resource relaxations by M(h+1), **not** the loose p^2(h+1).

**L3. Global event-threshold invariant and canonical state dominance (inherited, proved).**
Sort remaining events (i,j) by increasing d=a[j]-a[i], breaking equal d by **decreasing j**, then increasing i. Before an event (i,j) of difference d, every prefix stored at dp[i][r] has last difference <d: an earlier edge with the same d has destination greater than j, whereas a path ending at i<j must have destination i. Every smaller-difference predecessor was processed earlier. Thus combining a prefix ending at i with edge i->j creates a strictly convex selected prefix; all strictly convex prefixes arise through their final event. At fixed endpoint j and exact omitted weight r, maximize selected prefix length; among equal lengths retain the **lexicographically greatest increasing omission tuple**. At equal selected length, the first disagreement in omitted membership reverses the lex order of selected membership. Future larger-difference continuations depend only on endpoint, resource and length (not predecessor history), so the current state dominates all discarded states for all subsequent admissible events. After all events, dp[p][h] is the globally optimal core with its lexicographically least whole selected tuple; append the fixed mandatory suffix. If that state is absent, no nonempty solution exists.

**L4. Immutable interval witnesses and exact tie comparisons (new representation, proved).**
Store each dp cell as two words: (selected-count, omitted-history-node-id). Node zero denotes empty omission history. Every other immutable node stores exactly (previous-id, lo, hi), denoting the contiguous increasing omitted interval [lo,hi] appended to the predecessor history. Initial singleton paths use at most one node for [1,i-1]; an accepted positive-cost gap transition allocates **one** node storing [i+1,j-1], regardless of how many indices it contains; an adjacent transition with no omission allocates no node and reuses the predecessor's immutable pointer. No historical node is ever mutated or reclaimed while possibly referenced. Consequently later DP overwrites cannot corrupt earlier accepted histories.

For any omission sum r<=h, s distinct positive omitted indices satisfy s(s+1)/2<=h, giving s<=floor((sqrt(8h+1)-1)/2)=O(sqrt(H)). The chain represents nonoverlapping increasing intervals, so both any stored chain and the candidate predecessor chain plus tested gap can be expanded into ordinary increasing omission tuples in O(sqrt(H)) individual wide-word operations (including comparison). An improvement either wins on cardinality in O(1), or wins an exact **collision-free** lex comparison at that cost. This does not assume an h-bit mask or arbitrary-precision hash is one ordinary fixed word.

**L5. Operation count, storage and emission (proved).**
The DP has (p+1)(h+1)=O(H^2) cells. By L2, it considers M=O(H log(h+2)) sorted feasible events. Each scans at most h+1=O(H) resources, for O(H^2 log(h+2)) attempts. By L4, each attempt costs at most O(sqrt(H)) word operations, so total is O(H^(5/2) log(h+2)), including all attempted ties. Sorting, dense DP initialization and event generation are asymptotically absorbed. Fixed-suffix scanning and final emission take O(n).

Each accepted positive-gap improvement creates one immutable O(1)-word node; the number of accepted improvements cannot exceed the number of resource attempts. Thus nodes occupy O(H^2 log(h+2)) words, dp O(H^2), events O(H log(h+2)), and temporary reconstructed omitted tuples O(sqrt(H)). No stored pointer into an evolving state is used. The global full tuple is reconstructed once in O(n) by omitting exactly the immutable terminal chain indices. This proves G8-T.

## Conservative bit-cost overlay

Let B>=1 bound signed input bit length and L=B+1+ceil(log2(n+h+2)). Event differences, counters, indexes and (polynomially bounded) node IDs take O(L) bits. A deliberately loose schoolbook upper bound is O((n+H^(5/2)log(h+2))L^2) bit operations, and O(H^2 log(h+2) L) auxiliary bits, excluding input/output. Writing the output can cost O(n log(n+2)) bits; reading arbitrary signed values costs Omega(nB) when input I/O is charged. These overlays are not tight conventional word-RAM or Python allocation claims.

## Non-results and verification gates

- The primary O(n+H^3)-time/O(H^2)-space **entire-witness** target is OPEN. A logarithmic factor in G8 memory must not be silently dropped.
- No proof of an O(H^2) bound on accepted persistent nodes, rank-maintenance space, garbage-collected reachable histories, or canonical Hirschberg reduction is available.
- The proof above is human-checkable, **not formally machine checked**. Committed tests perform finite independent full-selected-tuple comparisons, not a proof of complexity.
- The structural count is elementary harmonic-series arithmetic. The algorithm combines the existing Kluev-style sorted-edge sweep, exact-resource DP and immutable backpointers, not a demonstrated new general primitive.
