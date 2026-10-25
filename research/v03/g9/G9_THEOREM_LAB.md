# G9 mathematical certificate — quadratic-space full lex

Date 2026-10-24. Research-only based on unmerged PR #14 head af67856d17d87399b13c61006363a8448fd360bd. Complete human proof, NOT a machine-checked or peer-reviewed result.

## Canonical statement

Let n>=2, arbitrary signed integers A[1..n], m>=2, U=n(n+1)/2, U/2<m<=U and deficit h=U-m<n. Put H=h+1. Among all increasing selected-index tuples whose sum is divisible by m and whose consecutive selected *value* differences strictly increase, find the maximum length, then the lexicographically least **entire** selected tuple. Return empty only when no nonempty feasible witness exists.

**G9-T:** The research implementation experiments/v03/g9_quadratic_lex.py solves this exact objective with

\[
T=O(n+H^{5/2}\log^2(h+2)),\qquad S=O(H^2)
\]

time and auxiliary space, in **wide-word operations and wide words**, with input and returned tuple excluded. This also gives the originally requested simultaneous O(n+H^3) time and O(H^2) memory, since log²(H+1)=O(sqrt(H)). Each word must accommodate signed values and intermediate differences, indices, addresses, and counters; this is NOT a bounded-64-bit or Python-RSS theorem.

## Complete proof dependencies

**L1 (complement, compulsory suffix, sparse omissions).** Any positive modular selected sum s satisfies 0<s<=U<2m, so s=m, and omitted original indices D have sum h. They are distinct positive indices <=h, so all h+1..n are compulsory. Put p=min(n,h+2); every nonempty witness contains p and all selected triples ending >=h+3 are fixed adjacent suffix triples. Check those once in O(n); all remaining triples lie in 1..p. For t=|D|, 1+...+t<=h, hence t<=floor((sqrt(8h+1)-1)/2)=O(sqrt H). If optimum full selected length is L>0, every optimum has **exactly t=n-L omitted indices**.

**L2 (sparse legal convex-edge events, inherited from G8).** For consecutive selected positions i<j with skipped-count u=j-i-1>0, the exact omitted resource cost is g(i,j)=ui+u(u+1)/2. Feasible edges need g<=h, forcing u=O(sqrt H), i<=h/u; summing over all u gives at most O(H log(h+2)) positive-gap edges plus O(H) adjacent edges. Skipping a compulsory suffix index also invalidates an edge. For a fixed i, overbudget or compulsory-skip illegality is monotone in j; enumerating only eligible edges takes O(H log(h+2)) effort. Sort all eligible M=O(H log(h+2)) edges *once* by increasing (A[j]-A[i],-j,i), costing O(M log(M+1)) time and O(M) storage. Neither h nor A changes between queries.

**L3 (exact forced-prefix scalar length oracle).** Given a fixed omitted prefix Q and integer threshold x, let F(Q,x) be the maximum full selected length among nonempty feasible witnesses omitting every index in Q and selecting every position <x not in Q (zero if none). Construct forbidden-endpoint flags for Q and a prefix-count of required selected positions [1,x) minus Q, both O(H) words. Initialize one-element chosen core paths at endpoint i<=h+1 when initial omission cost W(i-1)<=h and no required index is skipped. For each sorted event i->j, discard if either endpoint is forbidden or a required selected index lies strictly between endpoints. Otherwise, for each r with r+g(i,j)<=h, update only scalar best chosen prefix count dp[j][r+g] from dp[i][r]+1.

Correctness induction: a path entering event (i,j) with difference d has last difference <d. For equal d, already processed incoming edges have larger destination than j, whereas a prefix ending at i<j can only have final destination i. Thus no equal-difference path is incorrectly chained. Every smaller-difference feasible predecessor has been seen. At the same endpoint and exact resource, a longer prefix dominates a shorter prefix for all future, larger-difference continuations regardless of its internal history. Every feasible core path is enumerated by its initial chosen index and successive final edges; forbidden endpoints, required skipped positions and budget rule make every constructed path legal. Since p is compulsory and resource h exact, F(Q,x) is dp[p][h]+(n-p) if reachable, else 0.

Each F query uses one (p+1)(h+1)=O(H²) DP matrix, O(H) masks, and the reusable O(H log H) event list. Computing the whole matrix costs O(H² log(h+2)) time, O(H²) auxiliary wide words. The suffix is checked only once, not rescanned by F.

**L4 (monotone next-omission reconstruction).** Compute L=F(empty,1). If L=0 return empty. Otherwise t=n-L=O(sqrt H). Construct lexicographically **largest** increasing omitted tuple Q=(d1,...,dt). Assume d1..d(k-1) already fixed as the prefix of at least one optimum, and all earlier non-Q positions selected; set d0=0. For any candidate x in [d(k-1)+1,h+1], F(Q,x)=L iff there exists an optimum completion of Q whose next omitted index d_k >= x: the oracle forbids omissions below x outside Q, and optimum omissions remaining number t-(k-1)>0, all <=h. Hence the threshold predicate is monotone nonincreasing in x. It is true at x=d(k-1)+1 by induction and false at x=h+1 (no omitted position remains <=h if all positions through h except Q are selected). Binary search locates its **maximum true x** in O(log(h+2)) oracle invocations. This x is precisely the greatest feasible next omitted index; if a completion skipped x, it would make x+1 true, contradiction. Append x to Q. Repeating t times yields the lexicographically greatest optimum omitted tuple by induction.

**L5 (global lex tie and complexity).** All optimum omitted tuples have same length t; at the first index where two omitted sets differ, the one omitting the larger index instead retains the smaller original index, hence its selected tuple is lexicographically smaller. Therefore the lexicographically greatest increasing omission tuple corresponds exactly to the lexicographically least **complete** selected-index tuple. The compulsory suffix is common to all and cannot change the comparison. Emit the complement of Q in O(n) work.

The algorithm issues at most 1+t(1+ceil(log2(h+1)))=O(1+sqrt H log(h+2)) scalar oracle calls. Each oracle costs O(H² log(h+2)), giving O(n+H^(5/2)log²(h+2)) total wide-word operations; memory is one scalar DP O(H²), event list O(H log H), constraint masks O(H), omission prefix O(sqrt H), excluding read-only input/output. No persistent witness histories, hash ranks or uncharged giant bitmasks exist.

## Signed-input bit and machine-model qualification

Let B bound input signed bit length and b=B+O(log(n+h+2)). Under schoolbook bit arithmetic, a conservative upper bound is O((n+H^(5/2)log²(h+2)) b²) bit operations and O(H² b) auxiliary bits, excluding input/output, with output bits O(n log(n+2)) and input reading Omega(nB) if I/O charged. CPython object headers and high-bit integer costs do not satisfy constant-cost ordinary machine-word arithmetic. No hard RSS limit follows.

## Proof gates and counterexample concerns

The exact *next omitted index equals x* feasibility predicate need not be monotone; G9 uses the nested next-index >=x predicate. Forced omitted Q must forbid endpoints; forced selected indices between endpoints must never be skipped. In-place equal-difference transitions require descending destination. A zero optimum is distinguished before using t=n-L. These are enforced by executable code and falsification tests. The proof is **human-checkable**, not formal proof assistant output. Novelty of constituent techniques is specifically denied; see priority matrix.
