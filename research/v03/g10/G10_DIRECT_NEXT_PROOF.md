# G10-N: direct next-omission coordinate — candidate mathematical certificate

Date 2026-10-26. Independent RFP theorem-strengthening experiment, based on the exact G9 contract. **Not formally checked, externally refereed, or priority-certified.** This document presents a complete candidate proof for adversarial review. Nothing here replaces the revised G9 paper.

## Target and candidate bound

Let n>=2 and integer values A[1..n] of either sign, m>=2, U=n(n+1)/2, U/2<m<=U, 0<=h=U-m<n, H=h+1. Feasible nonempty selected-index tuples S have sum(S) divisible by m and strictly increasing *consecutive selected value differences*. Maximize |S|, then lexicographically minimize the **entire** S. Return empty only if no nonempty witness exists.

**Candidate G10-N.** The algorithm experiments/v03/g10_direct_next.py computes the exact canonical witness with

    O(n + H^(5/2) log(h+2)) wide-word operations
    O(H²) auxiliary wide words,

excluding read-only input and the single emitted output tuple. Words accommodate the signed input and derived differences, indices, sums, and counters. Neither fixed-64-bit complexity nor Python RSS is claimed.

This is a possible *simultaneous theoretical strengthening* of the repository's stated G8 and G9 tradeoffs, **not** a claim of global firstness or significance. Equal-cardinality lex-score lifting and ordered self-reduction may have prior-art precedents; no new comprehensive search or human referee is claimed.

## Proof obligation 1: exact deficit, core and edge count

A nonempty selected index sum lies between 1 and U<2m, so its only admissible positive multiple is m. Its omitted set D has exact distinct-positive weight sum(D)=h. Thus every omitted index lies in [h], all indices h+1..n are compulsory, and if t=|D| then t(t+1)/2<=h.

As in the audited G9 theorem, set p=min(n,h+2), check each fixed suffix triple ending at k>=h+3 once, then use a core selected path ending at compulsory p. Every relevant transition i<j has omitted-gap weight g(i,j)=sum_{u=i+1}^{j-1}u<=h and cannot skip a compulsory index. For a positive gap of q skipped indices, g=q*i+q(q+1)/2; summing eligible sources by gap length bounds their number by M=O(H log(h+2)). Enumerate in O(M+p) and sort once by (A[j]-A[i], -j, i). For equal differences, larger destination comes first, preventing an equal-difference edge from entering an already-processed source.

## Proof obligation 2: two-coordinate constrained event oracle

Assume a previously fixed increasing omitted prefix Q, all its indices <=h. Let b=last(Q) or 0, and require every index <=b outside Q to be selected. All Q members must be omitted. Define, for any permitted *core prefix* path P ending at i, with omitted positions D(P) among [i],

    z_Q(P) = min(D(P) \ Q), or INF if the set is empty.

Retain, at each endpoint i and exact omitted resource r, the **lexicographically largest pair**

    (ell(P), z_Q(P)),

where ell is the selected prefix cardinality; hence cardinality is primary, maximum earliest *new* omission is secondary. This pair uses two scalar words per DP cell, not a stored history. Prefix-required flags and forbidden endpoints are the same as G9's forced-score oracle.

Initialization: for any allowed first selected i, resource W(i-1)=i(i-1)/2, ell=1, and z is the first member of [i-1]\Q, or INF. The required-selected prefix must contain no skipped index.

For eligible event i -> j, with gap G={i+1,...,j-1}, let e=min(G\Q) or INF; this value is found in O(1) using a reverse precomputed "next index not in Q" array. An admissible extension maps

    (ell,z) -> (ell+1, min(z,e))

at the same endpoint j and incremented omitted resource r+g(i,j). Endpoints in Q or gaps containing required indices are prohibited.

**Dominance lemma.** Suppose two permitted prefix histories share endpoint i, exact resource r, and both have last difference strictly below the current event difference d. If (ell1,z1)>=(ell2,z2) lexicographically, then for any common compatible future continuation C, their eventual pairs have the same ordering or the first has larger cardinality. The number of added selected positions is identical; the extra omitted set from C is identical. If ell1>ell2, the first still wins in cardinality. If ell1=ell2 and z1>=z2, then min(z1,e_C)>=min(z2,e_C). Therefore the dominated history can be discarded without losing a cardinality-optimal or maximal-next-omission completion.

**Strict event-order invariant.** Before processing event (i,j) of difference d, incoming edges to i of difference <d have been processed. Edges of difference =d entering i have destination i<j and are processed later because ties use decreasing destination. Hence each currently represented non-singleton path ending at i has its last difference <d. The dominance lemma applies at *each event*, not to the final table under an arbitrary earlier slope threshold. By induction over events, every propagated pair represents a legal strictly convex path, and every admissible path is represented or dominated at the point of its final edge. At compulsory endpoint p and resource h, the pair gives (optimal full length L, maximum earliest omitted index outside Q among length-L completions). Appending the checked suffix adds n-p to the score and no omissions.

The oracle's work is O(pH+MH)=O(H² log(h+2)), including fresh pair matrices, required mask, next-not-Q array, and every transition. Space is O(H²) words. Previous queries' matrices are released before the next query.

## Proof obligation 3: direct greedy extraction

Call the pair oracle first with Q=empty and b=0. If L=0, report empty. Otherwise let t=n-L, and by the deficit lemma t=O(sqrt H). If t=0, all positions are selected.

For k=1..t, assume Q is the lexicographically greatest feasible first k-1 omissions among global length-L optima. Require all indices <=last(Q) outside Q to be selected, and all Q indices omitted; there exists at least one optimum completion by induction. The pair oracle's returned second component z is precisely the **largest possible k-th omitted index** among optimum completions: all remaining omissions must exceed last(Q), and the first omitted outside Q is the next one in increasing order. Append z. This is admissible and preserves the invariant. After t selections Q is the lexicographically greatest entire optimum omitted tuple.

All optimum omitted tuples have identical cardinality t. At their first differing omitted index, the complement that *retains* the smaller index has the lexicographically smaller selected index tuple. Therefore lex-max Q corresponds exactly to lex-min complete S. Emit S with one output tuple and an O(1)-workspace monotone omission cursor.

Unlike G9, **no binary search over the next omitted index is required**: the maximizing candidate emerges from the augmented event DP itself. Exactly max(1,t) oracle sweeps are needed; no hidden t log H factor remains.

## Complexity accounting

Preprocessing tests the suffix in O(n), constructs O(M) eligible events and sorts them in O(M log M). Each oracle evaluates O(MH+pH)=O(H² log(h+2)) scalar updates, uses two O(pH) matrices and O(H) masks. There are max(1,t)=O(sqrt H) oracle calls. The final streamed complement takes O(n) time and O(1) additional work beyond the O(sqrt H) omission list and one returned output. Consequently

    time = O(n + H^(5/2) log(h+2))
    auxiliary wide words = O(H²).

The one-time sorting O(H log²(H+2)) fits the stated bound. With B-bit signed values, a safe coarse bit overlay charges b=Theta(B+log(n+2)) bits/word and schoolbook arithmetic; it does not imply fixed-word-RAM or Python RSS guarantees.

## Executed falsification

- 73,809 exhaustive signed ternary-grid cases n=2..8: whole witness equals independently enumerated selected subsets.
- 145,632 exhaustive four-value cases n=2..7: independent whole-witness oracle.
- 1,200 deterministic high-bit signed cases, n up to 119: complete output equals attributed corrected G9.
- Eight targeted examples forcing 1,2,3,4,5,7,9,11 omissions; G10 uses exactly t oracle sweeps, agrees with G9, returns the asserted full complement.
- Zero-deficit large-output cases, strict-equality/lex ties, and invalid-domain exceptions.

**Local execution:** 5 new unit tests passed under Python 3.13 in a source-subset workspace (23.5 s). GitHub CI and independent mathematical review must be checked separately before any status upgrade.

## Remaining falsification/priority questions

1. Have we charged every temporary allocation in the abstract word model? The output cursor avoids the original G9 slice defect, but external review should inspect Python allocator behavior separately from word-space proof.
2. Is the pair dominance invariant valid in every event-relative state, including equal slopes, arbitrary fixed Q, and exact h? The above inductive argument is offered for adversarial review.
3. Does prior work already describe the same endpoint/resource/earliest-new-omission lex-score semiring and yield this exact combined bound? **Novelty UNCHECKED** for this specific stronger candidate. Do not submit a priority claim.
4. Does the apparent query-count improvement survive matched feasible-workload benchmarking against G8 and T1 on real hardware? **Not established by correctness tests.**
5. Extend beyond h<n or derive a meaningful superlinear lower bound? **OPEN**.

Status: **PROOF_SKETCH + TESTED** (candidate), not FORMALLY_VERIFIED or external peer review. No manuscript modification is authorized by this experiment alone.
