# G14: anchored three-omission linear-time exact certificates

**RFP deep + OmO native fallback, 2026-10-27.** Research-only extension stacked on PR #26, preserves G8–G13 historical code and prior manuscript. No outside referee, world novelty certificate, universal practical SOTA or production dispatch is asserted.

## Domain

Given n>=2 arbitrary signed integer values a[1..n], integer m>=2, U=n(n+1)/2, U/2<m<=U, and h=U-m<n, maximize the number of selected indices with selected index sum divisible by m and strictly increasing differences of **consecutive selected values**, breaking ties by the lexicographically **least complete selected-index tuple**.

`certify_g14(a,m)` returns either the exact canonical optimum tuple, an empty tuple if globally infeasible, or `None` if unable to certify. `solve_g14` delegates `None` to unchanged G11; public `modconvex.solve` is not modified.

## Theorem G14-1: linear-time anchored canonical witness

For every valid high-modulus input, `certify_g14` performs **O(n+h)=O(n)** charged wide-word operations and uses **O(h+1)** auxiliary wide words, excluding input and one emitted output tuple. Its non-`None` result is the correct **global canonical optimum**, and any `None` case may have an optimum omitting 4 or more indices, or 3 omitted indices with no originally invalid consecutive triple.

Its coverage includes:

1. All cases with h<=9 (full exact solution or proof of infeasibility, no abstention).
2. All cases whose true optimum omits at most two positions (G13).
3. All cases with a length-(n-3) optimum and **at least one originally bad consecutive triple**. A three-omission witness is discovered in exact lexicographic order.
4. Additional impossible cases proved by G13's linear weighted-hitting/suffix certificates.

This is a **strictly stronger certified subclass**, not an improvement in the unrestricted worst-case complexity of G10/G11. When the certificate returns n-O(1) selected indices, its linear time is output-size optimal.

### Proof 1: exact deficit, failed triple hitting and three-omission anchor

Because 0<sum(selected)<=U<2m, any nonempty feasible selected index sum must equal m. The omitted distinct index set Q is a subset of [1,h] with exact sum(Q)=h; all indices >h compulsory.

If an original consecutive triple (k-2,k-1,k) violates convexity and all three indices are selected, the same triple occurs consecutively in the selected tuple and invalidates it. **Hence every feasible Q must intersect each originally bad triple.** This is an exact necessary condition, not a sufficient convexity guarantee.

Suppose Q contains exactly 3 positions and at least one bad original triple exists. Choose the first such triple, with endpoints [k-2,k]. Some r in {k-2,k-1,k} must belong to Q. Given that fixed r, the other two omitted indices i<j must have distinct positive indices, differ from r and satisfy i+j=h-r. There are at most O(h) such pairs. There are only **three possible anchors**, so at most O(h) candidate three-element sets Q, including duplicates. Every valid three-omission Q is among them.

If there are more than 9 originally bad triples, 3 omissions cannot cover them because each omitted index belongs to at most 3 adjacent original triples, so no 3-omission Q can work.

### Proof 2: candidate enumeration in lexicographically descending O(h) time

For a fixed anchor r, enumerate the smaller other omitted index i from floor((h-r-1)/2) downward to 1, with j=h-r-i, skipping any i or j equal to r. The sorted triple Q=sort(r,i,j) is lexicographically **nonincreasing** as i decreases; this holds independently whether r is the smallest, middle or largest element. This monotonicity was exhaustively checked for h=6..189 and all applicable anchors r<=20 before integration.

Each of the at most 3 generated streams is already sorted in descending lexicographic order. A 3-way heap merge requires O(h log 3)=O(h) time, **O(1)** heap/state words; deduplicate adjacent identical triples. Process candidates in descending Q. For fixed omission cardinality 3, the lexicographically largest omitted tuple gives the lexicographically smallest entire **selected** tuple. Consequently the first valid candidate is the canonical length-(n-3) witness. G13 has already excluded every better n, n-1 or n-2 witness.

### Proof 3: constant-time strict-convexity test for each triple

Precompute B[t], the prefix number of originally bad consecutive triples ending by t, for t<=p=min(n,h+2). The compulsory suffix check from G13 has already verified endpoints k>=h+3. An original bad triple disappears only if some index q in Q falls within its span, so its endpoint belongs to [q,q+2]. Since Q has exactly 3 indices, the union of these at most 3 short intervals can be counted with O(1) prefix-sum operations (merge already sorted intervals in order). If any original bad triple remains outside their union, Q is invalid.

For any newly adjacent triple among the selected indices, its span contains at least one deleted index q. With at most 3 deletions, its last endpoint lies at most 5 original index steps after q. Enumerating k in (q,q+5] for each q, and ignoring deleted endpoints, covers every changed selected triple in **O(1)** checks; finding its two predecessors skips at most 3 deleted positions. Since a 3-omission Q has largest element <=h-3, every changed triple endpoint is <=h+2=p. Check exact signed inequality a[first]+a[last]>2a[middle] for each such triple.

This test is both **necessary and sufficient** for the whole retained tuple to be strictly value-convex: every consecutive selected triple is either unchanged (and included in the prefix/suffix original-bad checks) or newly adjacent (and checked directly).

### Proof 4: exactness when h<=9

The smallest sum of **four distinct positive indices** is 1+2+3+4=10. Thus h<=9 permits at most three omissions. G13 already proves all 0/1/2-omission cases or soundly abstains. If some original bad triple exists, G14 enumerates every admissible 3-omission set by its required anchor. If **none** exists, h<=9 is an absolute constant and G14 enumerates all possible distinct 3-part partitions directly in O(1) work relative to unbounded n. If no valid Q is found, the instance is globally infeasible. For h<=9, B[p]<=p-2<=h<=9, so the early >9-bad-triple exclusion cannot obstruct completeness.

### Proof 5: complexity and scope

G13 runs in O(n), O(h) auxiliary. The G14 extension creates B[0..p] in O(h), scans up to 3 candidate streams each with at most h/2 members, performs O(1) exact-triple work per candidate, and constructs at most one returned n-O(1) tuple. A three-stream merge has constant heap width. Hence O(n+h)=O(n) time, O(h+1) auxiliary wide words. The fallback to general G11 is **outside** this partial theorem and retains the prior conditional G10 bound.

## Executed adversarial evidence, prior to GitHub

- 73,809 exhaustive signed ternary cases n=2..8: G14 returned a **complete globally canonical witness or exact empty result for every case**. Every tuple matched an independent selected-subset bitmask oracle. Zero mismatches, zero abstentions (all those inputs have h<=7).
- 5,000 seeded independent random signed cases n=2..11: every completed certificate exactly matched the independent oracle; every abstention corresponded to an optimum omitting at least 4 elements. Zero errors.
- Checked that each fixed-anchor descending stream is correctly sorted for h=6..189 and r<=20. Zero ordering violations.
- Constructed exact three-omission instances h=6,7,8,9,10,12,19,32,65,100 with omitted Q={1,2,h-3}, verified full canonical witness; no incorrect early one/two-omission certification.
- Safe abstention test: squared values `a[i]=i²`, h>9, with no originally bad triple but no 0/1/2-omission witness. No invented infeasibility result.

Tests support the reasoning but are **not a machine-checkable formal proof**. The cross-platform GitHub workflow independently reruns oracle suites; status remains provisional until its exact run completes.

## Benchmark plan and controls

`benchmarks/g14_rfp_three_omission_screen.py` performs matched G14/G13/G12/G11/corrected-G8/G10 whole-tuple comparisons on **677 previously registered cases plus a newly fixed 140-case three-omission-centered holdout** (10 h values x 2 sizes x 7 value families; independent seed 27102714). It preserves feasible, infeasible, certified, abstained and losing regimes with raw samples, environment, source checksums. All cases must match on the complete canonical selected-index tuple; a single mismatch fails the workflow.

Neither the generic interval hitting and lexicographic generation patterns nor existing resource-constrained convex subsequence primitives are asserted to be novel. The narrow G10 high-modulus *joint* bound and its literature priority still need external theorem-level refereeing. An efficiency gain over an internal baseline, even if reproduced, does not certify worldwide practical SOTA.

**Statuses:** partial G14 theorem PROOF_SKETCH with human-checkable full argument; implementation TESTED; external/formal verification OPEN; world novelty UNRESOLVED; production integration withheld.
