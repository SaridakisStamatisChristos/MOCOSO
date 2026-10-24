# G7 theorem lab: compact omission witness Pareto point

**Status:** Human-checkable proof under the declared wide-word model; independent finite testing passed locally. NOT formally machine-checked. NOT a proof of world novelty or of the primary O(h^3)-time/O(h^2)-space conjecture.

## Theorem G7-P (restricted h<n)

For n>=2, integer values a[1..n], integer m>=2 satisfying U/2<m<=U and h=U-m<n, the globally lexicographically smallest maximum-cardinality feasible selected tuple (empty if none nonempty exists) is computable in

\[
T=O\big(n+p^2(h+1)(1+\sqrt{h+1})\big),\qquad
S=O\big(p^2+p(h+1)(1+\sqrt{h+1})\big)
\]

auxiliary *wide words*, with p=min(n,h+2). In particular T=O(n+(h+1)^{7/2}) and S=O((h+1)^{5/2}). The algorithm emits the entire selected-index tuple with no external lex reconstruction pass. Input and output storage are not auxiliary.

### 1. Distinct-part omission bound (proved)

Any partial selected path ending at j has a finite omission set D drawn from distinct positive indices no greater than q=h, with exact weight r=sum(D)<=h. Writing s=|D|, distinct positive integers have sum >=1+...+s=s(s+1)/2; therefore

\[
s\le t(h):=\lfloor(\sqrt{8h+1}-1)/2\rfloor=O(\sqrt{h+1}).
\]

Every stored omitted-index tuple is an explicit list of <=t(h) **individual word-sized integers**. No variable-width integer is assumed O(1).

### 2. Exact prefix representation and admissible edge events

Let W(t)=t(t+1)/2. A prefix of selected indices ending at j has omission weight r equal to sum of omitted original positions in [1,j]. Base paths containing solely selected i have omitted set (1,...,i-1) with cost W(i-1), allowed only if i<=q+1 and cost<=h. For consecutive selected indices i<j, its gap weight is

\[
g(i,j)=W(\min(j-1,q))-W(\min(i,q)).
\]

Reject edges skipping an obligatory index >q: (i<=q and j>=q+2) or (i>=q+1 and j>i+1). The allowed gap tuple lists exactly indices (i+1,...,min(j-1,q)). Appending this tuple to the predecessor omission tuple gives the exact new omission tuple for the prefix ending at j, with resource r+g(i,j). All omissions are disjoint and in increasing order.

Sort every candidate edge (i,j) with i<j<=p by (a[j]-a[i], -j, i). DP[j][r] stores an optimal selected prefix ending at j among paths whose last edge difference is strictly below the *next* event's difference, represented by (selected-count, omitted-tuple).

### 3. Strict-convexity sweep invariant (proved)

Induct over ordered edge events. When processing edge (i,j) of difference d, every prefix currently in DP[i][r] has last difference <d. For different differences this follows from ascending event ordering. For equal differences, any earlier event ending at i has destination i<j and hence is processed **after** (i,j) because destinations are ordered descending. Thus no same-difference last edge can feed the current event. Appending j yields a strict increase and preserves all earlier strict triples. Conversely, the last edge of every feasible selected prefix is eventually processed and all its predecessor prefixes with smaller last differences have already been considered. Discarded infeasible mandatory-skipping edges can never belong to a valid solution. Resource accounting from Section 2 is exact.

### 4. Local lex dominance (proved)

For any two selected prefixes ending at the same j with the same omitted sum r and selected count L, both omit exactly j-L indices from [1,j]. At the first position where their omission sets differ, **including** that position produces the lexicographically smaller equal-cardinality selected prefix. Among equal-length prefixes, lexicographically **larger omission tuples** (usual ascending tuples) therefore correspond to lexicographically **smaller selected tuples**. At DP[j][r], maximize the ordinary Python ordered pair (selected count, omission tuple). This retains the lex-min optimal prefix among paths admissible under the current difference threshold.

A future outgoing edge depends only on endpoint j, its difference relative to the sweep threshold, and omission cost r; it does not depend on the earlier prefix path. Hence neither a shorter prefix nor an equally long lex-larger prefix can lead to a better completed path via a future edge. Canonical tie dominance is preserved by continuation.

### 5. Mandatory suffix and global optimality (proved)

Because h<n, q=h and p=min(n,h+2)>q. All indices >q are compulsory. In particular **p belongs to every nonempty feasible tuple**, and every index >p is common to them. Every selected triple ending at k>=q+3 is an immutable ordinary suffix triple. Reject all nonempty candidates if any such triple fails; otherwise every variable triple appears in the processed prefix ending <=p. Therefore after completing the sweep, DP[p][h] is the single exact best state for **all** nonempty global solutions (including valid singleton solutions). Append the fixed p+1..n suffix to its selected prefix, or equivalently output all indices except its omitted tuple. If DP[p][h] is unreachable, return empty.

Equal core selected counts mean equal complete counts since suffix is common. Core lex order and complete lex order also agree. Thus optimizing the state pair yields the globally lexicographically least entire optimal tuple, not merely a prefix-local tie.

### 6. Complexity proof (proved)

There are O(p^2) ordered edges (sort O(p^2 log(p+1))), O(p(h+1)) DP cells, and at most O(p^2(h+1)) relaxations. Each relaxation concatenates and compares two length-at-most-t(h) omitted tuples, costing O(1+t(h)) individual wide-word operations. Each live cell holds one integer and at most t(h) omission indices: O(p(h+1)(1+t(h))) words. The event list contains O(p^2) entries of O(1) words; each temporary gap list has at most t(h) indices. Immutable suffix checking plus output is O(n). Since p<=h+2, the sort is absorbed by the stated time upper bound. Space counts the returned tuple separately and charges every omitted index as a word. Real CPython allocation/bit cost for large values is outside the word-model theorem.

## Research attacks and unsuccessful routes

- **R1: desired cubic/quadratic full lex using only lengths per sorted-edge state. OPEN.** Endpoint/resource length cells do not by themselves retain which lex-min prefix attained that length. Canonical predecessor pointers can be overwritten as later thresholds improve states; keeping all historical versions may cost O(p^2(h+1)) words. No O(p(h+1)) persistent-witness proof obtained.
- **R2: treating a bitmask over 1..h as one O(1) machine word. REJECTED FOR MODEL ERROR.** Its h-bit width needs explicit bit/word cost; it is not valid evidence for quadratic standard-word memory.
- **R3: ordinary Hirschberg split of pair/event states. OPEN.** A split must also retain both boundary last-difference compatibility and exact weighted omission equality; no proved O(h^3)/O(h^2) factorization here. Investigate general width-bounded DP traceback results only after verifying frontier and lex assumptions.
- **R4: unsafely allowing equal edge differences to chain. REFUTED.** Input a=(0,1,2), n=3, m=6, h=0. The only nonempty feasible modular witness would be (1,2,3), but its consecutive differences are equal, so the correct answer is empty; naive same-difference propagation can incorrectly construct length 3.
- **R5: selecting lex-smallest omissions, rather than lex-largest for fixed selected length. REFUTED.** Input a=(-3,-3,-3,-3,-2,0), n=6, U=21,m=16,h=5. The feasible optimal 4-tuples (1,4,5,6) and (2,3,5,6) correspond to omitted (2,3) and (1,4). The former selected tuple is lex-smallest, and its omitted tuple is lex-**largest**. A one-element omission (5) creates an invalid five-index tuple on this input.

**Priority statement:** The established bound is a resource-lift of Kluev-style sorted convex edges with elementary distinct-positive-part compression and ordinary explicit tuple comparisons. It is a reproducible specialized Pareto bound; no claim of a new general DP primitive, lower bound, or first-in-literature theorem follows.
