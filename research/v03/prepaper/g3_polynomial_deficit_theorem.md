# G3 — Polynomial-deficit exact algorithm: proof and novelty quarantine

**Research date:** 2026-10-24 UTC. **Reviewer:** separately invoked Algorithm Foundry. **Frozen subject:** MOCOSO research head 7595130fecb1a21dc8ca8823d9ee8d5d136af97a, G0 base 567c5bfca0eda13c8ff98045423f16038f37e609. **G3 branch:** research/v03-g3-polynomial-deficit, draft PR #7. G1 and G2 are separate, unmerged sibling reviews.

This document records a **human-checkable mathematical proof**, not a machine-checked theorem, a claim of publication originality or manuscript prose. Existing v0.2 source and original T1 solver remain byte-for-byte untouched.

## 1. Exact problem and computational model

Let n>=2, a[1..n] arbitrary signed integers, m>=2 and U/2<m<=U with U=n(n+1)/2. Write h=U-m, q=min(n,h), p=min(n,q+2). Find a selected strictly increasing index tuple I (possibly empty) whose index sum is divisible by m and whose consecutive selected value differences are strictly increasing; maximize length and then choose the **lexicographically least complete tuple**. Optionally decide whether OPT>=K.

The algorithmic bound counts **unit wide-word arithmetic operations**, where a word can represent a signed input value, its required intermediate differences, array indices, DP state counts and table addresses. This model does not promise constant-time operations for unbounded Python integers on standard hardware. Input, final output tuple and runtime allocator/interpreter overhead are excluded from auxiliary space.

## 2. Main result G3-T1+

**Claim (human-proof level).** There exists a deterministic exact algorithm for the scoped problem, returning the maximum length and lexicographically least complete witness, using:

~~~
Time:  O(n + p^2 (h+1)) wide-word operations
Space: O(p^2 (h+1)) auxiliary words
p = min(n, min(n,h)+2).
~~~

If h<n, p<=h+2 and these specialize to O(n+h^3) time and O(h^3) auxiliary words (for h=0 handle additive constants). If h>=n, p=n and the result becomes O(n^2(h+1)) time/auxiliary words.

This is **strictly polynomial in h** versus the earlier T1 candidate-enumeration expression O(n+qh+qD_q(h)), where D_q(h) may be superpolynomial in h when q=h. But it can use substantially more space than T1's O(qh+q) and can be slower for small h; no universal practical dominance is claimed. An output-sensitive enumerator and a polynomial DP are different Pareto choices.

## 3. Lemma proofs

### A — Complement and mandatory suffix

A nonempty selected-index sum s is positive and at most U. Since it is a multiple of m and 2m>U, s=m. Thus omitted index sum is h. Every omitted index is at most h and at most n; omissions are contained in [1..q] and every index in [q+1..n] is mandatory. Conversely omissions totaling h give selected-index sum m, leaving only convexity to test. This is a standard elementary reduction, not proposed novelty.

### B — Exact locality boundary

Every consecutive selected triple ending at k>=q+3 is the ordinary triple k-2,k-1,k of the permanently selected suffix. Its strict convexity test is therefore fixed across all candidates and can be performed once in O(n) time. Every other selected triple ends at <=q+2 and appears exactly as a consecutive triple within the chosen local prefix [1..p]. Rejecting on any failed fixed suffix test is sound. Processing all selected triples in the local prefix is also necessary and sufficient; in particular crossing triples ending at q+1 or q+2 cannot be dropped. Once the fixed tests pass, the selected tail [p+1..n] is compulsory and identical for every candidate.

### C — Gap weights and mandatory-index exclusion

Let W(t)=t(t+1)/2. For consecutive selected core indices j<k, the omitted-index cost is exactly

~~~
g(j,k) = W(min(k-1,q)) - W(min(j,q)).
~~~

An edge is forbidden if it skips an index >q. It is therefore forbidden when j<=q and k>=q+2, or when j>=q+1 and k>j+1; the implementation tests these cases explicitly. The sum of omitted indices strictly before the first chosen index i is W(min(i-1,q)), provided i<=q+1 (otherwise q+1 would be skipped). If no core index is chosen after j, then either (i) q=p=n, so all remaining indices can be omitted at cost W(q)-W(j), or (ii) p>q and termination is legal only at the compulsory last core index j=p, with cost zero. These intervals partition all omitted core positions with no double counting.

### D — Exact pair and omitted-sum recurrence

Define F(i,j,r) for i<j<=p, 0<=r<=h, as the maximum **number of additional chosen core indices after j** under all of: the selected prefix starts with fixed last two indices i,j; all new selected triples are strictly convex; omitted-index weight after j is exactly r; every compulsory core index >q is included. Unreachable value is -1.

There is an empty-extension option with value zero exactly when Lemma C permits termination and the remaining omitted weight is the exact tail cost. Otherwise, any nonempty continuation has a unique first chosen successor k>j, satisfying the mandatory-gap rule and strict difference inequality

~~~
a[k] > 2*a[j] - a[i].
~~~

It contributes 1+F(j,k,r-g(j,k)), provided r>=g(j,k) and the child state is reachable. Choosing the maximum of all valid contributions and the legal terminal option is exact: every legal continuation decomposes through precisely one first successor, and every such child concatenation is feasible. Processing second indices j in descending order makes every needed child F(j,k,*) available (k>j). Induction proves exact state lengths.

### E — Quadratic-times-budget sweep

For fixed j, sort predecessors i<j by increasing a[i] and prospective legal successors k>j by decreasing a[k]. For the current i the strict admissibility threshold theta(i)=2*a[j]-a[i] is nonincreasing. Maintain a Best array indexed by exact omitted weight. Whenever a successor k becomes admissible for the first time, for each possible child omitted cost r, offer the extension 1+F(j,k,r) at new omitted cost r+g(j,k). The best known extension never becomes invalid for later predecessors because theta only decreases.

Each successor k is processed at most once per j; each insertion scans at most h+1 costs. Each predecessor row F(i,j,*) is a copy of Best and is adjusted only by a possible terminal option, costing at most O(h+1). There are O(p^2) total successor insertions and O(p^2) predecessor rows, giving O(p^2(h+1)). Sorting the p local indices once costs O(p log p), absorbed by that bound for p>=2. Ties of a[i] or a[k] do not violate strictness because admission tests use > rather than >=.

### F — Complete global optimum and lex order

In a state with a fixed first pair (i,j) and omitted weight r, among equally long nonempty extensions, choose the smallest **first successor k**; if k ties, the child's saved lex-optimal continuation resolves the remaining order recursively. This establishes canonical state witnesses by induction. A terminal (length 0) option cannot tie a positive extension.

For each legal first pair i,j, subtract the omitted-before-first and omitted-between-pair weights from h, and consult F(i,j,remaining). Its total selected length is 2+F+(n-p), including the fixed remaining suffix. Every feasible solution with at least two selected indices has a unique first pair and is considered. Among equal-length candidates with different first pairs, the lex smaller first pair gives the lex smaller full index tuple; within a fixed pair the recurrence already yields the lex least tail. Singleton candidates are checked separately (possible when m<=n, notably n=2,m=2). The empty tuple remains an admissible fallback. Thus the reconstructed result is the length-optimal, globally lexicographically least **complete** tuple.

### G — Complexity, decision and interruption contract

The fixed-suffix scan costs O(n). There are p(p-1)/2 DP pair states and h+1 weight entries each; length and successor pointers occupy O(p²(h+1)) abstract words. Temporary sorted indices and best rows cost O(p+h); output reconstruction costs O(n). Lemma E bounds all relaxations and row copies by O(p²(h+1)). Therefore time O(n+p²(h+1)) and auxiliary memory O(p²(h+1)) as claimed. On a schoolbook bit model with W representing an upper bound on all numbers' bitwidth and DP addressing, a safe, deliberately loose adaptation is O((n+p²(h+1))W²) bit operations; Python performance must still be measured.

For completed execution the exact OPT gives sound FEASIBLE/INFEASIBLE threshold decisions. For K<=0, empty is a verified YES witness; K>n is an immediate NO. When a compulsory suffix triple fails, empty is provably optimal, so upper bound zero is sound. If the **preflight state-cell ceiling** is exceeded, return RESOURCE_LIMIT with valid empty lower-bound witness and sound coarse upper bound n, not INFEASIBLE. This is a cooperative guard, not a hard RSS ceiling; catastrophic memory faults or process termination may prevent a result object from being returned.

**This completes a human-checkable proof of the abstract claim under its explicit model. No Lean/Coq/Isabelle proof run is claimed.**

## 4. Adversarial surface and no-overclaim ledger

Tests compare the candidate to an independently coded exhaustive **selected-subset** oracle over all A in {-1,0,1}^n for n=2..7 and all legal moduli, plus 850 seeded arbitrary large signed inputs. Additional independent index-sum DP checks cover large superconvex 3^i inputs where every subsequence automatically has increasing consecutive differences; resource and threshold statuses are checked separately. Sources and actual jobs are recorded in g3_execution_evidence.md.

Source-level policy: this is a **research-only** algorithm; no production solver changes, no PR merges, no paper writing, no unsupported hard-memory guarantees.

## 5. Prior-art and meaning of “stronger”

The new O(n+h^3) special-case guarantee (h<n) avoids the **distinct-part enumeration dependency** in the earlier in-repository T1 analysis. That is a real asymptotic improvement *over that algorithm's worst-case dependence on h*, but it is based on known building blocks:

- Ordered-edge convex subsequences: Evgeny Kluev (2013), https://stackoverflow.com/questions/20664920/longest-convex-subsequence-in-an-array .
- Standard exact-target subset-sum enumeration (different from G3 DP): Dutta and Rajasree (2021/2022), https://arxiv.org/abs/2112.11020 .
- Resource-constrained longest paths in acyclic graphs and dynamic programming: Camponogara and Shima (2010), https://doi.org/10.3217/jucs-016-03-0372 .
- Resource-constrained shortest paths as a general classical problem, with exact resource tracking: https://www.boost.org/doc/libs/latest/libs/graph/doc/html/graph/algorithms/shortest_paths/r_c_shortest_paths.html .

**Research novelty: UNRESOLVED / probably compositional.** This record does not claim a fundamentally new DP paradigm, or that a similar parametric bound could not be derived from preexisting general constrained-path results. An independent G1 follow-on should examine exact reductions and original proofs before any originality claim. G4 benchmarks should include a faithful resource-constrained DAG baseline and more than one runner/environment. G6 owns final paper GO/NO-GO.
