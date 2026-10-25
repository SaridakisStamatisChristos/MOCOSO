# T1: High-modulus deficit partition algorithm — candidate theorem

Status: complete in-repository derivation; finite falsification evidence exists; **independent mathematical review and literature-priority review pending**. This file is not a claim of a new published theorem. Date: 2026-10-23. Baseline main: 9cedac0d0f860564d5ee1a9064b01ef56ac2a764.

## Definitions

Given signed A[1..n], m>=2, select strictly increasing indices i_1<...<i_k, strictly increasing consecutive *value* differences, sum(i_t) congruent to 0 modulo m. Empty is valid. Maximize k and choose lexicographically least full index tuple among maximizers. Define U=n(n+1)/2, U/2<m<=U, h=U-m, q=min(n,h). Let D_q(h) be number of distinct subsets of {1,..,q} with sum h, and P_d(h) be unrestricted number of partitions of h into distinct positive parts (including P_d(0)=1). Necessarily n>=2 in this regime for m>=2.

## Proposition 1: Complement equivalence

Any nonempty selected index sum s lies in [1,U]. As m>U/2, the only positive multiple of m no greater than U is m (because 2m>U). Hence omitted indices form a subset O of [1,n] summing to U-m=h. No omitted index can exceed h, so O is contained in [1,q]. Conversely, every distinct-index O contained in [1,q] summing to h has complement S with sum U-h=m and thus satisfies the modular constraint. Convexity is the only remaining feasibility question.

## Proposition 2: Exact immutable-suffix locality

For every candidate, all indices q+1,...,n are present. A selected triple ending at k>=q+3 has previous selected indices exactly k-2 and k-1 (both belong to the present suffix), so its convexity is exactly A[k]-A[k-1] > A[k-1]-A[k-2]. Conversely, any selected triple not of this form ends at index <=q+2 and appears in the selected restriction S intersect [1,min(n,q+2)]. Therefore *all* convexity triples pass iff (a) every ordinary suffix triple for k=q+3,...,n passes, AND (b) every adjacent selected triple in the local restriction passes. This equivalence includes q=n, h=0, no local prefix, and candidates with fewer than three selected elements. The suffix can be rejected once; each candidate uses O(q) local work, not O(n) work.

## Proposition 3: Enumerate all and only reachable omissions

Let R[t,s]=1 iff a subset of distinct indices {1,...,t} sums to s. Base: R[0,0]=1 and R[0,s>0]=0. Recurrence R[t,s]=R[t-1,s] OR (s>=t AND R[t-1,s-t]), by the unique exclude/include dichotomy for t. Construct rows t=1..q for s<=h. Cost O(qh) time and O(qh) bytes in the concrete bytearray implementation; this is O(qh) machine words as a conservative bound.

Backtracking starts at (q,h) and follows only exclusion or inclusion choices certified by the R row below. By induction, each traversed state extends to at least one complete distinct-part partition and every partition occurs exactly once. If L=D_q(h)>=1, each visited entry state has a complete descendant. Charge each entry state to an arbitrary descendant leaf. Each leaf can have at most q+1 ancestors (one per t), so entries <=(q+1)L. Local checking, comparison and copying the best q-bit omission decision as a Boolean tuple cost O(q) per leaf. Save the best omission descriptor; reconstruct its full selected tuple only once upon returning a result, in O(n) time.

All selected candidates share the identical suffix beyond q. For equal-length candidates their selected local lists have equal length, so their lexicographic order equals that of their complete selected index tuples. Maximize length first, then compare local lists. If none passes, the empty tuple is optimal since there are no other positive modular sums. For threshold K, a verified candidate of length>=K certifies YES. NO is returned only after complete enumeration (or a bound such as K>n). The partial RESOURCE_LIMIT status carries a verified feasible witness and the sound bound n; it never certifies NO.

## Theorem candidate and proof summary

For U/2<m<=U, the above procedure produces the exact length and globally lexicographically least optimal witness using

  O(n + qh + q P_d(h)) unit-cost word operations

and O(qh+q) auxiliary words, apart from input and final output. This includes initial suffix check O(n), reachability O(qh), at most O(qD_q(h)) backtracking/local candidate work, and final O(n) reconstruction. Because D_q(h)<=P_d(h), the stated bound follows. For q=0 the singleton h=0 case is O(n). For positive h, q<=h and the bound is O(n+h^2+h P_d(h)).

For x>0, the generating function F(z)=product_{i>=1}(1+z^i)=sum_{j>=0} P_d(j) z^j has nonnegative coefficients. Therefore P_d(h)e^{-xh} <= F(e^{-x}). Using log(1+z)<=z and sum_{i>=1}e^{-xi}=1/(e^x-1) <= 1/x,

  P_d(h) <= exp(xh + 1/x).

Take x=1/sqrt(h) to obtain P_d(h)<=exp(2 sqrt(h)). Thus the high-modulus parameter bound is O(n+h^2+h exp(2 sqrt(h))) for h>=1 (unit-cost word model).

## Exactness and computational model qualifications

- Python arbitrary-precision integer subtraction/comparison costs depend on bitlength B of A values. The displayed bound is an *arithmetic word-operation count*, not a RAM bit-complexity or Python wall-clock claim. The input itself can require Omega(nB) bits.
- Machine-word indexing/modulus arithmetic assumes O(log(n+m+h)) bits fit into a word; outside that model, include big-integer costs.
- The implementation's signed difference comparisons remain exact. No floats, convexity approximation, or division enter the predicate.
- The Boolean reachability table allocates (q+1)*(h+1) bytes plus Python allocation overhead, not a hard process memory maximum. Stack and omitted descriptors consume O(q) words. A soft tracemalloc cap cannot enforce hard RSS, and each budget checks only at specified safe points.
- The auxiliary-space statement excludes the input, final O(n) output tuple and runtime/import/interpreter overhead.
- The counted operations metric covers selected loops, **not** all instructions, sorting, or allocation. An operation budget stopping at any supported point yields RESOURCE_LIMIT, not an infeasibility claim.
- This specialization can have enormous qh memory even when the general solver uses another strategy. It is experimental and not a default solver dispatch.

## Verification status and falsification

Independent complement-unaware brute-force oracle checks all 2^n index subsets for 41,085 instances: n=2..7, A in {-1,0,1}^n and all high moduli. There are 250 additional seeded large-signed cases. Small complete cases compare threshold statuses and full lex-optimal witnesses; resource interruptions assert sound bounds. These are finite executable tests in tests/test_v03_deficit.py, not a mathematical peer review. The branch must pass CI before recording a release gate as met.

## Priority warning

Distinct-part partitions, reachability pruning and locality checks are not inherently new. P_d is the classical distinct-parts partition function (OEIS A000009). This proof may show a valid project-specific parameter bound without meeting peer-reviewed novelty standards. See novelty_matrix.md and claim_ledger.md.

Source pointers: https://oeis.org/A000009 ; https://stackoverflow.com/questions/20664920/longest-convex-subsequence-in-an-array .
