# G15: single-pass canonical optimization by ranked omissions

Research contribution, 29 October 2026. Complete human-checkable derivation
below; not formally verified, independently refereed, or globally SOTA.
The generic ranking technique is Cover's enumerative encoding, not new.
The candidate contribution is its telescoped exact-deficit integration into
the convex-subsequence sweep, full canonical reconstruction in one sweep,
and extension to all high moduli, including h >= n.

## Contract and result

Let n >= 2, A[1..n] be arbitrary signed integers, U=n(n+1)/2,
m >= 2, U/2 < m <= U, h=U-m, H=h+1. Maximize the cardinality of a
nonempty increasing selected-index tuple S with sum(S) divisible by m and
A[S[t]] + A[S[t+2]] > 2 A[S[t+1]] for every consecutive selected triple.
Among equal-cardinality solutions minimize the entire tuple lexicographically.
Return () for infeasibility. Convexity uses selected-value differences, not
slopes divided by original index gaps.

**Theorem.** `solve_ranked` returns exactly this answer for every input in
the contract. No bound on omission count and no h<n assumption is needed.
It uses one sorted-event optimization sweep followed by one unranking.

Let K=min(n,h), p=min(n,h+2), and M be the eligible-event count. In a RAM
whose w-bit words hold input differences, sums and addresses, let
L=1+ceil(sqrt(H)/w). With standard multiword addition/subtraction/comparison,
the deterministic bounds are

    time  O(n + M log(M+1) + ((K+p)H + MH)L)
    space O((K+p)H L + M) auxiliary w-bit words.

Since p=O(H), K=O(H), and M=O(H log(H+1)), this simplifies to

    time  O(n + H² log(H+1) (1 + sqrt(H)/w))
    space O(H² (1 + sqrt(H)/w)).

Input and one returned output tuple are excluded. If w=Omega(sqrt(H)),
the bounds become O(n+H² log(H+1)) time and O(H²) auxiliary words.
This width condition must accompany that simplified statement.

In the common h<n domain, the general time bound improves on the repository's
G10 O(n+H^(5/2)log(H+1)) bound, while potentially using more than its O(H²)
auxiliary words. This is a time/space tradeoff, not unconditional domination.
Python integers are arbitrary precision; neither fixed-64-bit constant-time
arithmetic nor Python RSS follows from the theorem.

## 1. Exact complement and compulsory suffix

A nonempty selected sum is positive and at most U<2m, so the only feasible
multiple of m is m. Thus its omitted set D has exact sum h. Conversely,
any complement with omitted sum h has selected sum m>0. Every omitted
index is at most K, and |D|(|D|+1)/2 <= h.

If p<n, indices h+1 and h+2 are compulsory. Checking each original triple
ending at h+3,...,n suffices to validate the fixed appended suffix. A failed
such triple proves infeasibility. Otherwise the core [p] with those two
anchors is sufficient. If p=n there is no appended suffix and the algorithm
allows every possible final selected endpoint; this handles h>=n.

## 2. Exact-sum ranks and their width

Define C(i,s) as the number of subsets of {i,...,K} of sum s, with
C(K+1,0)=1 and C(K+1,s)=0 for s>0. Negative residuals have count zero.
The standard include/exclude recurrence is

    C(i,s) = C(i+1,s) + [s>=i] C(i+1,s-i).

All omission incidence strings are ordered lexicographically using
keep=0, omit=1. For a prefix ending at index i, let r be its omitted sum.
Its compatible exact-sum completions form a contiguous rank interval of
length C(i+1,h-r). Its lower endpoint R is the sum, at every omitted
position q, of the count of the sibling branch which keeps q:

    R = sum over omitted q<=i of C(q+1, h - sum(omitted positions < q)).

This is Cover's enumerative rank formula specialized to exact positive
weights. Keeping an index leaves R unchanged. Omitting q adds the displayed
count and decreases the remaining resource by q. These statements follow
by partitioning the completion set into its zero and one branches in order.
They prove both the interval invariant and injectivity at a complete leaf.

For width, let q(s) count partitions of s into distinct positive parts.
For any t>0,

    q(s) exp(-ts) <= product_{j>=1}(1+exp(-tj))
                 <= exp(sum_{j>=1}exp(-tj)) <= exp(1/t).

Taking t=1/sqrt(s) for s>=1 gives q(s)<=exp(2sqrt(s)); s=0 is trivial.
Every C(i,s), s<=h, has O(sqrt(H)) bits. Rank offsets of nonempty intervals
are less than C(1,h), so they have the same bound. Intermediate differences
and sums have at most a constant number of extra bits. Counts are never
approximated, hashed, truncated, or treated as constant-width without this
explicit word accounting.

## 3. Constant-number-of-arithmetic-operations gap update

An edge i->j omits the consecutive gap {i+1,...,j-1}, of weight
g=W(j-1)-W(i), where W(x)=x(x+1)/2. Given source residual s=h-r,
the sum of all one-branch rank increments telescopes by the recurrence:

    delta(i,j,r) = C(i+1,s) - C(j,s-g).

Proof: at position q the increment C(q+1,s_q) equals
C(q,s_q)-C(q+1,s_q-q). The second term is the next position's first term.
Only the first and last terms survive. The adjacent-edge case has g=0
and delta=0. Selecting j changes no rank offset. Reject an edge state
when g>h-r or C(j+1,h-r-g)=0: it cannot complete to exact omitted sum h,
even before imposing convexity. This pruning loses no solution.

Initial singleton i omits [1,i-1]. Its resource is W(i-1), length one,
and offset C(1,h)-C(i,h-W(i-1)), again by telescoping. A positive
C(i+1,h-W(i-1)) is necessary for a completion after selecting i.

## 4. Single-pass dominance and strict convexity

At each endpoint i and exact prefix omitted sum r retain the pair
(maximum selected length, minimum rank offset among that length).
An edge adds one to length, g to resource, and delta(i,j,r) to rank.
For any two histories sharing i,r, all these increments are identical.
Therefore larger length dominates; at equal length, smaller rank dominates.
Any common future continuation adds the same offset to each. This proves
order preservation, including histories with different earlier omissions.

Sort eligible edges by (A[j]-A[i], -j), with arbitrary remaining ties.
Immediately before i->j of difference d, edges of smaller difference
have been processed, whereas every difference-d edge entering i has
destination i<j and is processed later. Larger differences have not run.
Thus all nonsingleton source histories have final difference <d.
Dominance is applied at this event, not retrospectively at an arbitrary
earlier slope threshold. Induction over events proves that every represented
history is valid and every valid extension is represented or dominated.
No predecessor chain or repeated reconstruction query is required.

## 5. Terminal selection and global canonical witness

When p<n, the only core terminal is compulsory p with resource h; append
the checked suffix and add n-p to its length. When p=n, each possible
terminal j has omitted tail weight T=W(n)-W(j). Accept only the state
r=h-T. Its residual T is the maximum sum of the remaining indices, so
its sole possible completion omits every tail index. That completion has
additional offset zero. Thus the retained prefix rank is the full rank.
Compare these terminal states by maximum length and then minimum rank.

Unrank the winning R: at q, count the keep branch C(q+1,remaining).
If R is below that count, keep q. Otherwise subtract the count, omit q,
and subtract q from the remaining sum. The interval invariant proves that
the process terminates at residual zero and rank zero and recovers exactly
the chosen omission set. The returned complement is nonempty because m>0.

For two selected tuples of equal length, at their first differing incidence
position the tuple retaining that smaller index is lexicographically smaller.
Hence minimizing omitted incidence (keep=0 first) is exactly minimizing the
entire selected tuple, after cardinality optimization. This completes the
correctness and canonicality proof.

## 6. Resources, including allocations

Enumerate only edges with g<=h that skip no compulsory index. For a positive
gap of q indices, g=qi+q(q+1)/2, so q<=sqrt(2h), i<=h/q.
Summing over q gives O(H log(H+1)) events, plus O(p) adjacent events.
Increasing j makes both exclusion predicates monotone, permitting early
breaks. Sort once; costs are O(M log(M+1)) operations and O(M) words.

The count table uses O(KH) rank-size integers and O(KH) additions.
Two dense DP tables and active-resource lists occupy O(pH L) words;
active lists contain each reachable cell once. All active-source scans are
bounded by MH. Each relaxation uses a constant number of rank operations
costing O(L) words/time. No hash-table expected-time assumption is needed.
Terminal processing costs O(p); unranking O(KL). The omission list has
O(sqrt(H)) indices; its exact-size iterator emits the sole output tuple in
O(n) time. Validation uses indexed triples, without output-sized slices.
Counts, active lists, rank tables, event records, sorting and all temporaries
are included in the stated auxiliary bound.

## 7. Evidence and boundaries

The committed tests independently enumerate selected subsets for every
signed ternary input of length 2..8 and every high modulus: 159,183 cases,
including 85,374 with h>=n. They also test the rank bijection by enumerating
binary strings, the telescoping identity against explicit sums, 500 high-bit
random oracle cases and affine invariance, forced 4..15 omissions, ties,
terminal endpoints, infeasibility, validation and zero deficit.
Results and commands belong in EXECUTION.md after they actually run.

`solve_g15` additionally preserves G14's fast certificates for h<n, using
the complete ranked solver only on abstention. Its inherited certificate
implementation and evidence remain attributable to the pinned G14 head;
the theorem above concerns the new standalone `solve_ranked` kernel.

The bound is specific to the high-modulus domain. It is neither an O(n)
general solver nor a proof of global optimality. The bit-width/space tradeoff,
synthetic workload limitations, existing ranking/sweep prior art, and lack
of independent mathematical review remain material.
