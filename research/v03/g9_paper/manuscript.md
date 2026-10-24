---
title: Canonical witnesses for modular convex subsequences with a small index deficit
author: Stamatis-Christos Saridakis
date: 24 October 2026
lang: en-US
fontsize: 11pt
geometry: margin=1in
papersize: letter
colorlinks: false
---

**Research draft.** Revised after the source-specific priority investigation. The contribution is an incremental specialization of established methods; worldwide priority and suitability for a publication venue remain unresolved.

# Abstract

Consider a maximum-cardinality subsequence of an integer array whose original indices sum to zero modulo a prescribed integer and whose consecutive selected values have strictly increasing differences. We study the regime where the modulus is close to the sum of all indices. Writing $h=n(n+1)/2-m<n$ and $H=h+1$, we prove that the globally lexicographically least entire optimal index tuple can be computed in $O(n+H^{5/2}\log^2(h+2))$ wide-word operations using $O(H^2)$ auxiliary words, excluding the input and one returned output. The proof specializes established difference-sorted dynamic programming, exact-resource lifting, and sparse oracle reconstruction. An exact omission deficit yields a core of at most $h+2$ indices, $O(H\log(h+2))$ eligible transitions, and $O(\sqrt H)$ omissions. We prove both the constrained scalar invariant and the complete lexicographic reconstruction guarantee, with every feasibility call charged. An inclusion-only formulation clarifies the relationship to earlier arbitrary-witness extraction. The preserved implementation audit contains 80,283 complete-witness comparisons and identifies an output-validation allocation repaired in a separate derivative. Additional reduction checks are reported separately. The contribution is an incremental specialized theorem and reproducible implementation analysis; it does not establish a new general extraction principle, worldwide priority, or asymptotic optimality.

# 1 Introduction

An optimal score and a canonical optimal witness impose different obligations on an exact algorithm. For a convex subsequence, a scalar score can be propagated in sorted order of value differences. Retaining one locally preferred predecessor does not by itself show that the resulting entire index tuple is globally lexicographically least. A second difficulty appears in space analysis: even when the optimization state is small, copying a large returned witness during validation can invalidate an auxiliary-space bound.

This note addresses both obligations for a modular index constraint in a restricted parameter regime. The input is an integer array $A[1..n]$. Selected values must be strictly convex in their selected order, and the sum of the selected original indices must be divisible by $m$. The objective first maximizes the number of selected indices and then minimizes their complete increasing tuple lexicographically. If $m$ is sufficiently large, the modular condition becomes an exact omitted-weight condition. When its deficit $h$ is smaller than $n$, all choices occur near the start of the array.

The main result is a complete algorithm and proof with quadratic auxiliary space in $h+1$. Its reconstruction operates on omissions: an optimal omitted set has only $O(\sqrt{h+1})$ elements, and each next omission is found by binary search on a threshold feasibility predicate. Sparse extraction with $O(k\log N)$ oracle queries was already established by Björklund, Kaski, and Kowalik [@bjorklund2014]. Our analysis supplies the particular constrained oracle, preserves the entire original-index order, and accounts for the compulsory suffix, event sorting, repeated queries, and output construction.

The mathematical mechanisms have clear antecedents. The full upper bound can be derived by combining them with elementary deficit structure, so its significance rests on the precise specialized guarantee and reproducible correction. The manuscript does not claim a general advance in canonical traceback, a lower-bound-optimal algorithm, or a demonstrated practical speedup. The corrected artifact and original implementation are preserved separately [@mocoso2026]. A subsequent source-specific investigation supplies the revised literature assessment and additional reduction checks [@mocosopriority2026].

# 2 Problem and computational model

Let $n\geq2$, let $A[1..n]$ contain arbitrary signed integers, and let $m\geq2$ be an integer. Define

$$U=\frac{n(n+1)}2,\qquad h=U-m,\qquad H=h+1.$$

Assume $U/2<m\leq U$ and $0\leq h<n$. A feasible witness is a nonempty tuple $S=(s_1,\ldots,s_k)$ with strictly increasing entries in $[n]=\{1,\ldots,n\}$ satisfying

$$\sum_{r=1}^k s_r\equiv0\pmod m,$$

and, for each $1\leq r\leq k-2$,

$$A[s_{r+2}]-A[s_{r+1}]>A[s_{r+1}]-A[s_r].$$

Tuples of length one or two satisfy the convexity condition vacuously. This is convexity of selected values in selected order. It is not a condition on divided differences using the original index gaps. Among all feasible witnesses, the requested output has maximum length and, among witnesses of that length, is lexicographically least. An empty tuple denotes infeasibility and is not a feasible candidate of score zero.

We count operations on wide words large enough to contain input values, differences, triangular sums, addresses, and polynomially bounded counters. If signed input values require at most $B$ bits, $b=\Theta(B+\log(n+2))$ bits per word suffice, with an adequate constant factor. Arithmetic and comparisons on such words have unit cost in the primary theorem. This is not a fixed 64-bit RAM assumption. The auxiliary-space measure excludes a read-only random-access input and one final output array; all intermediate arrays, event records, sorting storage, and temporary output copies are charged.

**Theorem 1.** Under these assumptions, the globally lexicographically least entire maximum-cardinality feasible witness, or an infeasibility report, is computable deterministically in $O(n+H^{5/2}\log^2(h+2))$ wide-word operations and $O(H^2)$ auxiliary wide words.

The theorem concerns the algorithm below and the corrected research derivative described in Section 7. The original pinned implementation has a separate auxiliary-space defect. With elementary bit arithmetic, a conservative translation of the theorem gives time $O((n+H^{5/2}\log^2(h+2))b^2)$ and auxiliary storage $O(H^2b)$ bits. The excluded input and output require $O(nB)$ and $O(n\log(n+2))$ bits, respectively. These bounds do not predict Python process RSS or allocator behavior.

# 3 Established ingredients and scope of contribution

The unweighted value-convex subsequence problem appears in Erickson's algorithms textbook [@erickson2019, p. 126, exercise (f)]. Kluev's 2013 public technical answer gives the closely related sorted-difference sweep, including decreasing destination indices for equal differences, scalar endpoint scores, and witness reconstruction suggestions [@kluev2013, steps 1--6]. That answer is a primary public disclosure, not a peer-reviewed paper. The sweep and its equal-difference ordering are therefore established ingredients, not claimed contributions of this note.

Exact resource coordinates in dynamic programming are also standard. Turner describes equality-constrained resource shortest paths on acyclic digraphs [@turner2011, equation (23), Theorem 2]. Wu et al. describe temporal-to-static path expansion [@wu2014, Section 5]. For comparison, assign each eligible transition its difference rank as departure time and duration one. Temporal compatibility then enforces strictly increasing differences. Arrival/departure copies and waiting arcs give a graph with $O(M+p)$ vertices and arcs. Our adaptation assigns gap resource and cost minus one to travel arcs, zero to waiting arcs, and the appropriate initial resource and length to source arcs. Minimizing cost now maximizes selected length. An explicit exact-resource table on this graph uses $O(MH)=O(H^2\log(h+2))$ words. This reduction is our inference from the path representation, not a theorem stated by Wu et al.; the rolling endpoint compression proved below is still needed for quadratic space.

Canonical witness search by constrained extension queries belongs to established self-reduction methods [@grosse2006, Section 3]. Creignou et al. describe lexicographic enumeration using extension queries; the directly inspected preprint locus is version 2, Section 3.2, Proposition 5 [@creignou2017]. Our use of such queries requires proof that the particular constrained optimization oracle remains efficient.

Björklund, Kaski, and Kowalik give deterministic extraction of a witness of size at most $k$ from an $N$-element universe using at most $2k(\log_2(N/k)+2)$ inclusion-oracle queries [@bjorklund2014, full version, Theorem 1]. The conference publication is from 2014; the numbered theorem and algorithm inspected here are in the 2015 full version. An inclusion query asks whether some witness is contained in a permitted set. Their Algorithm 1 permits arbitrary balanced partitions and does not prescribe our lexicographic optimum. Section 6 gives a counterexample to that automatic transfer and an elementary ordered adaptation. We do not claim novelty for sparse extraction or that adaptation. The paper's stronger total-runtime transfer also assumes that oracle cost scales appropriately with the shrinking universe. Our original index weights and resource limit remain fixed after restrictions, so we charge each query at its full proved cost.

Meeks distinguishes inclusion queries from extension queries that additionally require specified elements [@meeks2018, Sections 1 and 3]. This distinction matters: an efficient existence procedure does not generally answer arbitrary forced-prefix questions. We prove the constrained sweep directly. An alternative inclusion-only reconstruction maintains that its previously chosen elements are essential to every remaining optimum; it does not solve the arbitrary extension problem. Low-space Subset Sum algorithms [@jin2020] likewise cannot be transferred without retaining the selected complement's convexity constraint.

The surviving contribution is the joint specialized analysis: an exact omission deficit, a two-anchor core, a harmonic eligible-event bound, a constrained scalar sweep, and complete lexicographic reconstruction with all queries charged. This is an incremental composition of established mechanisms and elementary problem structure. The documented investigation used thirty queries across two search engines, primary-source follow-up, and limited citation chaining [@mocosopriority2026]. It found no source stating the same complete theorem, but did not exhaust the literature. Earlier explicit statement, present-day derivability from known methods, and scientific significance are separate questions; only the second is established by the derivation here.

# 4 Deficit structure and eligible transitions

**Lemma 2 (exact complement).** For any feasible witness, its omitted set $D$, consisting of the indices outside $S$, satisfies $\sum_{d\in D}d=h$. Conversely, any complement with that omitted sum satisfies the modular index condition. Every omission is at most $h$, and the omission count $t$ satisfies $t(t+1)/2\leq h$.

*Proof.* A nonempty selected sum is positive and at most $U<2m$. Its only possible positive multiple of $m$ is $m$. Taking complements gives omitted sum $U-m=h$, and the converse follows immediately. An omitted index greater than $h$ would already exceed the nonnegative total. Distinct positive omitted indices have sum at least $1+\cdots+t=t(t+1)/2$. Thus $t=O(\sqrt H)$. In particular, every index from $h+1$ through $n$ is compulsory. $\square$

Set $p=\min(n,h+2)$ and let $W(q)=q(q+1)/2$ for $q\geq0$.

**Lemma 3 (two-anchor core).** Test the original consecutive triples ending at indices $k=h+3,\ldots,n$. If any fails strict convexity, the instance is infeasible. Otherwise, feasible core witnesses on $[p]$ that include its compulsory indices correspond exactly to full feasible witnesses by appending $p+1,\ldots,n$. Scores increase by $n-p$.

*Proof.* Each tested triple consists entirely of compulsory indices and hence occurs consecutively in every witness. When $p<n$, the core contains the two compulsory indices $h+1,h+2$. Consequently, the first triple crossing into the appended suffix ends at $h+3$ and is among those tested. Every later suffix triple is tested as well. Any triple involving a mutable index and ending at either compulsory anchor remains in the core. If $p=n$, there is no suffix to append. Restriction and extension therefore preserve feasibility in both directions. $\square$

The suffix check costs $O(n)$ once. Including only $h+1$ as an anchor would leave a triple involving the last mutable selected index unchecked; the second anchor is essential to this reduction.

A core event is a possible pair of consecutive selected indices $(i,j)$ with $1\leq i<j\leq p$. Retain the pair only if its open gap contains no compulsory index and its omitted weight

$$g(i,j)=W(j-1)-W(i)$$

is at most $h$. Adjacent indices have gap weight zero. Every consecutive selected pair of a feasible core witness is eligible. For each retained event, store its difference $d(i,j)=A[j]-A[i]$ and its gap weight.

**Lemma 4 (harmonic event count).** The number $M$ of eligible events is $O(H\log(h+2))$. They can be enumerated in $O(M+p)$ time and sorted in $O(M\log(M+1))$ time.

*Proof.* There are at most $p-1$ adjacent events. For a nonempty gap containing $u=j-i-1$ indices, its weight is

$$g(i,j)=ui+\frac{u(u+1)}2.$$

Eligibility implies $u\leq\operatorname{floor}(\sqrt{2h})$ and $i\leq\operatorname{floor}(h/u)$. Hence

$$M\leq p-1+\sum_{u=1}^{\operatorname{floor}(\sqrt{2h})}\operatorname{floor}(h/u)
=O(H\log(h+2)).$$

This is an upper bound, not an assertion that every counted pair is eligible. For each fixed $i$, increasing $j$ increases the gap weight and cannot remove a compulsory-index violation. Thus a direct scan stops at its first failure, charging eligible events and at most one failed candidate per $i$. Comparison sorting gives the claimed preprocessing cost. When $h=0$, the sum is empty and the bounds remain valid. $\square$

# 5 A forced-prefix scalar optimization oracle

Fix a set $Q\subseteq[h]$ of forced omissions and a threshold $x\in[1,h+1]$. The oracle $F(Q,x)$ returns the maximum full-witness length subject to the original constraints, omission of every member of $Q$, and selection of every index less than $x$ outside $Q$. It returns zero if no such witness exists. The suffix check from Lemma 3 is performed before any oracle calls.

Let a Boolean array mark forbidden endpoints in $Q$, and define a prefix count

$$R(v)=|\{r\leq v:r<x,\ r\notin Q\}|,\qquad R(0)=0.$$

An event $(i,j)$ is allowed for this query precisely when neither endpoint is forbidden and $R(j-1)=R(i)$, so its gap contains no required index. These checks take constant time per event. A singleton start at $i$ is allowed when $i\leq\min(p,h+1)$, $i\notin Q$, $W(i-1)\leq h$, and $R(i-1)=0$.

Create a matrix $V[i,r]$ for $1\leq i\leq p$ and $0\leq r\leq h$, initially unreachable. For each allowed singleton start, set $V[i,W(i-1)]=1$. Sort all eligible events once, outside the oracle, by increasing difference and then decreasing destination. Remaining ties may be broken arbitrarily. For each allowed event $(i,j)$, and for each $0\leq r\leq h-g(i,j)$ with reachable $V[i,r]$, perform

$$V[j,r+g(i,j)]\gets\max\{V[j,r+g(i,j)],V[i,r]+1\}.$$

The result is $V[p,h]+n-p$ if $V[p,h]$ is reachable, and zero otherwise. The matrix stores only lengths. No predecessor tuple or persistent witness tree is retained.

**Lemma 5 (event-relative dominance).** Immediately before an event $(i,j)$ of difference $d$ is processed, the source values $V[i,r]$ represent optimal lengths among admissible paths ending at $i$, of omitted weight $r$ through $i$, whose last difference is less than $d$, together with admissible singleton starts. The update therefore enforces strict convexity, and the final oracle value is correct.

*Proof.* All events with difference less than $d$ have been processed. Any event of difference exactly $d$ entering $i$ has destination $i<j$, and decreasing destination order places it after the current event. Thus no equal-difference incoming event can yet have contributed to $V[i,r]$. Events with larger difference also have not been processed. Singleton starts have no last difference and may precede any first edge.

Inductively, every reachable state arises from a strictly convex selected path satisfying the endpoint and required-gap checks. Conversely, the previous edge of any admissible path that can use $(i,j)$ has smaller difference and has already been processed, so that path's predecessor score is represented or dominated. At this event, a larger score with the same endpoint and exact resource can use every continuation available to the smaller score: the source paths all satisfy the current difference threshold. Retaining only the maximum score therefore loses no optimal extension. This reasoning is relative to the event order; it does not claim that arbitrary endpoint-equal paths with different last differences are interchangeable at all times.

Singleton omission weights and the disjoint open gaps count exactly the indices omitted through the current endpoint. Forbidden endpoints ensure that members of $Q$ are absent, and required-prefix checks ensure that every required index is present. Eligibility prevents compulsory indices from being skipped, including by an initial start. Since $p$ is compulsory, an admissible core path must end at $p$ and have total omitted weight $h$. Lemma 3 then supplies exactly the appended suffix length. This proves both soundness and completeness. $\square$

**Lemma 6 (oracle resources).** A query costs $O(H^2\log(h+2))$ operations and $O(H^2)$ auxiliary words.

*Proof.* The matrix has $O(pH)=O(H^2)$ entries. Its initialization, flags, and prefix counts take $O(H^2)$ time. Each of $M$ events scans at most $H$ resource entries, for $O(MH)$ time. The event list occupies $O(M)$ words and is reused. The matrix is released between calls. Lemma 4 gives the bounds. There is no suffix or output scan inside a query. $\square$

# 6 Canonical reconstruction and total complexity

Compute $L=F(\varnothing,1)$. If $L=0$, report infeasibility. Otherwise all optimal witnesses omit exactly $t=n-L$ indices. Maintain an increasing omission prefix $Q=(q_1,\ldots,q_r)$ that is the beginning of the omitted tuple of at least one optimum. Initially $Q$ is empty and its previous index $b$ is zero. Until $r=t$, binary-search thresholds $x\in[b+1,h+1]$ for the greatest value satisfying

$$F(Q,x)=L.$$

Append that value to $Q$ and update $b$. Return the increasing complement of the completed $Q$.

**Lemma 7 (threshold monotonicity and extension).** With the stated prefix invariant and $r<t$, the predicate $F(Q,x)=L$ is true exactly when some optimal omitted tuple extending $Q$ has its next element at least $x$. It is true at $b+1$, false at $h+1$, and monotone from true to false. Its greatest true threshold is the greatest possible next omission among those optima.

*Proof.* Every index below $x$ outside $Q$ must be selected. Since $x>b$ and all members of $Q$ are forbidden, this fixes the omission prefix through $x-1$ to exactly $Q$. There remains at least one omission because $r<t$. It must lie at or beyond $x$. Conversely, an optimum with that omission prefix and next omission at least $x$ satisfies all query constraints. Constrained scores cannot exceed the unconstrained optimum $L$, so equality is exactly the claimed existence test.

Increasing $x$ adds required selections and cannot create an optimum. The prefix invariant gives truth at $b+1$. At $h+1$, every mutable index outside $Q$ would be required, leaving no location for the remaining omission. Thus the upper endpoint is false. At a greatest true threshold $x^*$, a witnessing optimum cannot have its next omission greater than $x^*$, because it would then satisfy threshold $x^*+1$ as well. Its next omission is therefore exactly $x^*$. Appending it preserves the prefix invariant and makes the next omission as large as possible. $\square$

This predicate concerns a lower bound on the next omission, not equality to a proposed omission. Equality feasibility need not be monotone. For example, with $A=(1,3,9,27,81,243,729)$, $n=7$, and $m=22$, the maximum length is six and the only optimal omission is index six. The equality predicate is false at one through five, true at six, and false at seven. The threshold predicate is true at one through six and false at seven.

**Lemma 8 (entire-witness order).** Lexicographically maximizing the increasing omitted tuple among optimal witnesses lexicographically minimizes the entire selected tuple.

*Proof.* Compare distinct omitted sets of equal cardinality, and let $z$ be the smallest index in their symmetric difference. Their increasing omitted tuples first differ in favor of the set that contains $z$: that tuple is lexicographically smaller. The selected complements first differ in the reverse direction, since exactly the other complement contains $z$. Thus complementation reverses the order. Lemma 7 successively maximizes every omission coordinate among surviving optima, so the completed omitted tuple is globally greatest. Its complement is globally least. $\square$

*Proof of Theorem 1.* Correctness follows from Lemmas 2--8. For an explicit query bound, count the initial optimization, one lower-endpoint assertion query per omission, and at most $\operatorname{ceil}(\log_2 H)$ binary-search queries per omission. This yields

$$q\leq1+t\bigl(1+\operatorname{ceil}(\log_2 H)\bigr).$$

For $h=0$, $t=0$, so only the initial query is needed. In all cases, Lemma 2 gives $q=O(1+\sqrt H\log(h+2))$. Multiplying by Lemma 6 gives the claimed parameter-dependent time. Sorting the single event list costs $O(H\log^2(h+2))$, which is absorbed. The initial input and suffix checks and final output construction cost $O(n)$ in total; they are not repeated by the oracle.

At any instant there is one $O(H^2)$ matrix, an $O(H\log(h+2))$ event list with sorting workspace of the same order, $O(H)$ flags and prefix counters, and $O(\sqrt H)$ chosen omissions. These occupy $O(H^2)$ auxiliary words. Allocate the known-length output once and fill it by scanning $[n]$ against a monotone cursor in the sorted omission list. Validate it by indexed reads with a constant number of temporary words. No additional output-sized tuple or list is necessary. This establishes the stated auxiliary-space bound. $\square$

## Inclusion only reconstruction and its relationship to prior extraction

The forced-prefix formulation above matches the corrected G9 implementation. A second formulation makes the connection to inclusion-oracle extraction explicit.

**Proposition 9.** Let $\mathcal F$ be a nonempty family of $k$-element subsets of $[N]$. Given an oracle $I(Y)$ deciding whether some $D\in\mathcal F$ is contained in $Y$, the lexicographically greatest increasing witness tuple can be extracted with at most $k\operatorname{ceil}(\log_2(N+1))$ threshold queries, assuming existence and $k$ are known. For $k=0$, return the empty tuple without queries.

*Proof.* Maintain a chosen tuple $Q$ with last element $b$, initially empty with $b=0$. The invariant is that at least one witness is contained in $Q\cup\{b+1,\ldots,N\}$ and every such witness contains $Q$. While $|Q|<k$, binary-search the greatest $x\in[b+1,N]$ such that

$$I\bigl(Q\cup\{x,\ldots,N\}\bigr)=\mathrm{true}.$$

The predicate is monotone because the permitted sets shrink. The lower endpoint is true by the invariant, and the sentinel $x=N+1$ is false because $Q$ alone has fewer than $k$ elements. At the greatest true threshold $q$, every remaining witness contains $q$: otherwise it would also fit in $Q\cup\{q+1,\ldots,N\}$. Earlier chosen elements remain essential under restriction. Appending $q$ therefore preserves the invariant and maximizes the next coordinate. After $k$ stages the chosen tuple is the lexicographic maximum. Binary search gives the query bound. Explicit query-set construction costs $O(N)$ per call and $O(N)$ storage. $\square$

For this problem, compute $L$ once and take $N=h$, $k=n-L$, and $\mathcal F$ to be all optimal omission sets. Realize $I(Y)$ by requiring selected every mutable index outside $Y$ and checking whether the score is still $L$. Lemma 5 extends directly to an arbitrary required-selected mask: its prefix counts reject starts and gaps that skip required indices, and the event order is unchanged. The cost remains that of Lemma 6. Proposition 9 and Lemma 8 therefore recover Theorem 1 using only inclusion queries. The fixed prefix is essential along this greedy path; the argument does not produce a general extension oracle. This elementary specialization is included for attribution and clarity, without a priority claim.

The arbitrary-witness algorithm cannot simply be declared canonical. For $\mathcal F=\{\{1,4\},\{2,3\}\}$ on $[5]$, an allowed first partition in Algorithm 1 of Björklund et al. is $\{2,3\}$ and $\{1,4,5\}$. Deleting the former leaves the witness $(1,4)$, although $(2,3)$ is lexicographically greater. Both have cardinality two and weight five. This is an abstract oracle-family example, not a claim that this exact family occurs for some input array. It respects that algorithm's arbitrary-witness guarantee and refutes only the proposed automatic canonical transfer. Ordered deletion repairs the transfer without introducing a new general extraction principle.

# 7 Implementation defect and correction

The original G9 source is pinned to repository commit `96ac7e2` (full identifiers are in the evidence manifest). Its final convexity assertion iterates over `zip(selected, selected[1:], selected[2:])`. Python evaluates both slices before the iteration, creating two additional tuples of length proportional to the output. These tuples are auxiliary storage even though the original returned tuple is excluded.

The counterfamily is $h=0$, $m=U$, and $A[i]=i^2$. Every index must be selected and the complete array is strictly convex. Therefore $H=1$ while the two slices use $\Theta(n)$ auxiliary reference slots. The original code's asserted $O(H^2)$ auxiliary-space bound is false on this family. Passing functional tests cannot detect that asymptotic defect without a space-specific check.

The corrected derivative replaces the sliced assertion with indexed comparisons and constructs the output through an omission cursor. The cursor also removes reliance on average-case hash membership for a deterministic output-time claim. Its iterator exposes the known remaining output length to CPython; interpreter allocation details remain outside the abstract storage theorem. The scalar DP, event order, and reconstruction loop are unchanged. The derivative is an attributed correction, not a clean-room reimplementation of G9.

Both versions and all prior research implementations are retained in snapshot `43353e2` [@mocoso2026]. The corrected file is `research/v03/g9_independent_audit/solver_corrected.py`. Its complete SHA-256 and the audit harness hash appear in the companion evidence manifest, avoiding ambiguity about which implementation supports the theorem.

# 8 Computational audit

The computational evidence supplements the proof. The preserved audit uses seed 2026102415 and CPython 3.12.14 on Linux x86-64. Three separately written reference approaches were used: direct selected-subset enumeration, full-array dynamic programming indexed by the last two selected indices and exact selected sum, and distinct-part omission enumeration for planted instances. The reference methods do not import upstream reference solvers. Independence here means separately written methods within the same assisted audit session, not blinded external replication or formal verification.

The full-witness corpus contains 80,283 instances. The following categories are disjoint; the additional pair-DP checks are a subset of the random category.

| Full-witness category | Instances | Scope |
|:--|--:|:--|
| Exhaustive selected-subset comparisons | 73,809 | Three values, lengths 2 through 8, valid deficits |
| Seeded random comparisons | 6,000 | Lengths 3 through 12, six input families |
| Planted omission instances | 450 | Deficits 0 through 34 |
| Maximum-omission stress cases | 6 | Up to 16 omissions |
| Constructed deep lexicographic ties | 18 | Shared omission prefixes of lengths 0 through 5 |
| Total | 80,283 | Complete returned tuples compared |

The exhaustive alphabet is $\{-3,0,5\}$. Random families include small signed values, perturbed quadratics, random walks, and very large integers, including 120-digit magnitudes. Of the 6,000 random instances, 1,800 also receive the independent last-two-indices DP check. Across the full corpus, 75,621 instances are infeasible and 4,662 feasible. This imbalance limits any interpretation as a representative workload; the suite is designed for correctness falsification, not performance estimation.

The constrained oracle is tested separately on 13,767 forced-omission/threshold queries against direct enumeration; 1,565 of those also receive the independent pair-DP check. Event enumeration and its harmonic bound are checked for all deficits from zero through 200. These counts are additional checks, not additional full-witness instances. No mismatch is recorded for the original or corrected exact returned witnesses in the preserved run.

Mutation tests deliberately reverse the equal-difference destination order, remove forbidden-endpoint or required-prefix checks, and shorten the core to one anchor. Concrete counterexamples in the audit artifact show that these changes break the relevant invariants. For instance, with all four values zero and $m=8$, ascending equal-difference order can return $(1,3,4)$ even though no feasible witness exists. The mutant's assertions are disabled only to observe that invalid result; assertions remain enabled for the normal audit.

An additional search over 10,000 random inputs found no hole in the feasible interval of first omissions under the investigated hypothesis. That failed falsification attempt establishes no interval theorem and is not used in the proof. The proof uses the nested threshold constraints directly. All explicit mutation examples and the failed-search scope are preserved in the audit report.

The validation-phase allocation probe isolates the discovered slice defect. After the returned tuple is constructed, it resets the tracing peak and measures extra allocations during validation and return. It does not measure total solver memory or RSS.

| Input length | Original extra bytes | Corrected extra bytes |
|--:|--:|--:|
| 1,000 | 17,160 | 1,022 |
| 10,000 | 160,992 | 832 |
| 100,000 | 1,601,000 | 840 |

These observations are consistent with the explicit allocation argument in Section 7. Their precise byte counts depend on the runtime and do not establish a machine-independent empirical complexity law. The auxiliary bound for the corrected algorithm follows from object accounting in Theorem 1.

## Separate verification of the prior art reduction

The later priority investigation has its own immutable evidence snapshot and seed 20261024 [@mocosopriority2026]. It checks Proposition 9 on all 2,228 nonempty uniform families over universes of sizes one through five, and on 3,000 random uniform families over universes of sizes six through fifteen. It also compares the inclusion-only composition with direct selected-tuple enumeration on 7,612 MOCOSO instances: 1,397 are feasible, and 29 have multiple optimal tuples. A further 30,448 arbitrary-required-selection score comparisons all agree. These experiments are separate from the earlier 80,283-instance corpus; no combined unique-instance total is claimed.

The reduction-check program imports no repository solver and batches equal-difference events simultaneously, providing a different implementation of strictness from the production-style scheduler. Its all-pairs event construction and dense scratch merges deliberately favor clarity over speed. Its runtime is not evidence for the optimized asymptotic theorem. The recorded counterexamples distinguish arbitrary extraction from canonical extraction; they are not defects in the published arbitrary-witness guarantee. These finite checks support the mathematical reduction and do not establish literature priority or independent external replication.

# 9 Discussion and limitations

The omission representation is useful because it changes the number of reconstruction decisions. A direct feasibility decision for each mutable index makes $O(H)$ oracle calls. This reconstruction uses $O(\sqrt H\log(h+2))$ calls while retaining scalar states. Its cost includes an additional logarithm relative to the repository's stated G8 sparse-witness time bound. In that comparison, the G8 analysis states time $O(n+H^{5/2}\log(h+2))$ and auxiliary space $O(H^2\log(h+2))$, whereas the present theorem removes the logarithm from auxiliary space at the cost of another logarithm in time [@mocoso2026, G8 theorem laboratory]. This is a comparison with a repository-stated theoretical bound, not independent certification of every allocation in the G8 implementation, and not an external state-of-the-art ranking.

Five conclusions must be kept separate. Mathematical correctness is supported by the explicit derivation. Implementation correctness includes a verified space defect in the original and a corresponding correction. The asymptotic contribution is a specialized space-time tradeoff. Priority for the general mechanisms belongs to earlier work; priority for an explicit statement of this complete specialized theorem remains unresolved. Scientific significance is modest and incremental, limited by the narrow regime, established ingredients, and absence of demonstrated applications or lower bounds. None of these conclusions follows automatically from any of the others.

The strongest overlap case grants all the difference-sorted sweep, exact-resource DP, sparse extraction, and ordered self-reduction to prior methods. What remains is the deficit-specific reduction, legal-event count, combined canonical guarantee, and reproducible storage correction. Because their composition is elementary once these observations are available, the result should be evaluated as a specialized technical note. The absence of a matching search result cannot turn it into a new general algorithmic principle.

Several limitations remain. The algorithm assumes $h<n$ and does not solve all modulus regimes within these bounds. Arithmetic on arbitrary-size values is charged through a wide-word model. The experiments are finite, predominantly small, and not an industrial benchmark. The independent reference programs and the proof were prepared in an AI-assisted workflow within the same session; external expert replication remains valuable. The literature search is source-specific but not exhaustive. The correctness theorem can survive a priority discovery even if the paper's novelty case does not.

Useful subsequent work would identify a substantive application or a broader parameter regime, prove stronger tradeoffs, or establish a meaningful lower bound. Such possibilities are research questions, not results of this note. A venue decision should depend on the surviving specialized theorem and the reproducible correction, not on the availability of polished manuscript files.

# 10 Conclusion

In the high-modulus small-deficit regime, exact modular feasibility confines all omissions to a short prefix and bounds their number by a square root of the deficit. A resource-lifted sorted-difference sweep supports ordered searches for the lexicographically greatest omitted tuple, whose complement is the globally least complete optimal witness. Charging all queries and output operations gives quadratic auxiliary wide-word space and $O(n+(h+1)^{5/2}\log^2(h+2))$ time for the corrected algorithm. Earlier work supplies the general sweep and sparse-extraction mechanisms; this note contributes their explicit specialization and implementation accounting. Its bounded novelty is compatible with a correct theorem, while worldwide priority and venue-level significance remain unresolved.

# Artifact availability and disclosure

The original reproducible audit snapshot is linked in the references [@mocoso2026]. From that commit, run `python research/v03/g9_independent_audit/audit.py` and `python -m unittest tests.test_v03_g9_quadratic_lex -v` with assertions enabled. The first command regenerates `results.json`; use a disposable checkout to preserve the committed evidence. The later priority snapshot [@mocosopriority2026] contains `research/v03/g9_priority/reduction_checks.py`, which prints its separate deterministic results without rewriting the preserved JSON. The companion manuscript folder includes claim mapping, source registry, review, contribution stress test, evidence hashes, revision record, and build instructions. Both evidence snapshots and original G3--G9 research files are preserved.

This manuscript was drafted with AI assistance, including source inspection, mathematical reconstruction, code execution, literature searches, and adversarial review. That review is an internal assisted critique, not external peer review. The named author's review and responsibility for any eventual submission are required; no affiliation, funding award, external endorsement, or venue acceptance is asserted.

# References
