# G9 prior-art and implication investigation

Date: **2026-10-24**. Target: `SaridakisStamatisChristos/MOCOSO`, draft PR #15,
commit `96ac7e2df040ed964bc36f0ad4e00d541b3f1f2d`.
Research-only follow-up to [PR #16](https://github.com/SaridakisStamatisChristos/MOCOSO/pull/16)
and [manuscript PR #17](https://github.com/SaridakisStamatisChristos/MOCOSO/pull/17).
This report records an AI-assisted source investigation and independent deductions;
it is not an external referee endorsement or a certificate of worldwide priority.

## Finding

**The defensible novelty classification is INCREMENTAL / COMBINATIONAL.**
The general sweep, exact-resource lifting, and sparse decision-to-search ideas
have substantial prior art. A particularly relevant predecessor omitted from the
earlier bibliography is **Björklund–Kaski–Kowalik, ESA 2014**: sparse witness
extraction already has an O(k log N) inclusion-oracle query bound.

No inspected source was found to state the entire MOCOSO theorem with this exact
modular index constraint, deficit regime, complete index-tuple order, and both
resource bounds. However, **the complete bound can be derived by an elementary
composition of established mechanisms and the problem's deficit structure**;
the derivation is given below. Lack of an identical published statement therefore
does not support a claim to a new general reconstruction principle.

These are different conclusions:

- **Earlier explicit statement of the entire theorem:** not identified within
  the documented search scope; absolute priority remains unresolved.
- **Derivability using earlier techniques:** supported by the reduction below.
- **Novelty of the central general algorithmic mechanisms:** substantially
  overlapping prior art; a broad originality claim is not supported.
- **Residual contribution:** the specialized deficit reduction, precise combined
  accounting, full-order proof, and verified implementation constitute a bounded
  technical contribution. No major standalone theoretical advance is established.

## Exact object being compared

Let U=n(n+1)/2, m>=2, U/2<m<=U, 0<=h=U-m<n, and H=h+1. Input values A[1..n]
are arbitrary signed integers. A feasible nonempty increasing tuple S has
sum(S) divisible by m and, for each consecutive selected triple x<y<z,
A[z]-A[y] > A[y]-A[x]. Maximize |S|, then minimize the **entire tuple S**
lexicographically. Return empty only if infeasible.

The target is time O(n+H^(5/2) log²(h+2)) and auxiliary space O(H²) wide words,
excluding the read-only input and one output tuple. A wide word must hold input
values, differences, indices, and sums: O(B+log n) bits for B-bit values. This is
not a fixed-machine-word bound for unrestricted Python integers.

Geometric convex chains compare slopes divided by index gaps. That is a different
condition. Counting subsequences modulo a prime also differs from constraining the
sum of their original indices. Those apparent matches were screened out.

## Closest-source matrix

The source identifiers refer to the linked, version-specific registry in
[SOURCES.md](SOURCES.md). Dates below precede the pinned target's 24 October 2026
commit; they do not establish when the repository's ideas were first conceived.

| Source / locus | Established overlap | Missing for the exact target |
|---|---|---|
| S1 Kluev, public answer, 2013, steps 1–6 | Same convexity, sorted differences, descending destination on ties, scalar endpoint updates; reconstruction discussion | Omission resource, deficit counts, complete lex objective |
| S2 Turner, 2011 volume / 2012 online, p.96, (23), Theorem 2 | Exact-resource shortest-path DP on a DAG | Problem-specific event representation and canonical reconstruction |
| S3 Björklund–Kaski–Kowalik, ESA 2014; full version 2015, Theorem 1, Algorithm 1 | Deterministic sparse extraction using at most 2k(log₂(N/k)+2) inclusion queries | Prescribed lex order and construction of MOCOSO's oracle |
| S4 Meeks, 2015 preprint / inspected v4 2018, §1 and §3 | Inclusion/extension oracle distinction and sparse-extraction ancestry | This constrained DP and target bounds |
| S5 Creignou et al., inspected v2 2017, §3.2, Proposition 5 and proof | Lexicographic construction through extension queries | Sparse numerical-coordinate query accounting and this oracle |
| S6 Wu et al., PVLDB 2014, §5 | Temporal-to-static path expansion | Exact omission resource, maximum cardinality, quadratic-space compression |
| S7 Große–Rothe–Wechsung, 2001 / v2 2006, §3 | Lexicographic prefix search for self-reducible problems | The specialized constraints and exponent |
| S8 Nye, preprint 2025, Theorem 1 | Claimed general frontier-based traceback with fixed local ties | Target time bound and proof that ties mean whole-tuple lex order |
| S9 Jin–Vyas–Williams, 2020 / SODA 2021 | Low-space exact Subset Sum | Convexity of the complement and canonical optimum |
| S10 Erickson, textbook 2019, convex-subsequence exercise | Established base optimization problem | Modular index constraint and deficit parameter |

S1 is a primary public disclosure, not a peer-reviewed paper. Its zero-initialized
length array naturally counts edges; vertex length needs a +1 convention. This
minor presentation issue does not erase the disclosed sweep and tie ordering.
S8's theorem was not independently certified here; no positive implication relies
on it. S9 was screened at its problem statement and headline theorem, not through
a full verification of its randomized algorithms.

## Independent implication derivation

The following is **our reconstruction**, not a claim that any cited author wrote
this specialized theorem. It also identifies exactly what must be supplied beyond
the published statements.

### A. Reduce the modulus to a sparse omitted set

A nonempty selected sum is positive and at most U<2m, so it must equal m.
Consequently its complement D has sum h. Every omitted index is <=h, and if
t=|D|, then t(t+1)/2<=h. Thus t=O(sqrt(H)). Maximizing selected length is
minimizing the number of omissions.

All indices greater than h are compulsory. Keep the core through
p=min(n,h+2), and check triples ending at h+3,...,n once. The first two compulsory
indices, when they exist, connect the core to the suffix. This preserves the
boundary triple. When p=n there is no discarded suffix. The case h=0 is a direct
convexity check and output scan.

For an eligible transition i->j in the core, omit the gap between i and j;
reject any gap containing a compulsory index. Its resource is
g(i,j)=sum_{v=i+1}^{j-1}v. For a positive gap length u=j-i-1,
g=ui+u(u+1)/2. A gap costing <=h permits at most floor(h/u) choices of i,
and u<=sqrt(2h). Adding adjacent edges gives

    M <= (p-1) + sum_{u=1}^{floor(sqrt(2h))} floor(h/u)
      = O(H log(h+2)).

This is an upper bound; compulsory-index restrictions can only remove edges.
For each i, stop enumerating j at the first excess-cost or compulsory-gap
violation. Both violations persist as j increases, giving O(p+M) enumeration
work. Sort once in O(M log(M+1)) time and retain the list across oracle calls.

### B. Lift the old event sweep to a constrained score oracle

Given an arbitrary set R of required-selected core indices, let V[i,r] be the
greatest selected-prefix length ending at i with exactly r omitted weight,
relative to the event frontier. Initialize a singleton i with r=i(i-1)/2 if
r<=h and no required index precedes i. Process eligible events in increasing
A[j]-A[i], with decreasing destination j within each equal-difference group.
Skip an edge whose open gap meets R; prefix counts test this in constant time.
Update V[j,r+g] from V[i,r]+1 for all valid r. Read V[p,h]. Add n-p if feasible.

Why scalar dominance is safe: immediately before processing i->j with difference
d, all incoming events to i of difference below d have been processed. Incoming
events to i of difference d have smaller destination than j and occur later.
Therefore V[i,r] contains only prefixes whose last difference is strictly below
d (or a singleton). They are all eligible for this event; among them only the
largest length matters. Every convex extension appears when its last edge is
processed. Requiring selected vertices merely removes starts or gaps; it does
not invalidate this argument. Reaching compulsory endpoint p ensures that all
requirements have been accounted for.

This proves an arbitrary-required-selection oracle in O(pH+MH)=O(H² log(h+2))
time per call and O(pH+M)=O(H²) space. It is an exact-resource lift of an already
disclosed sweep. A forced-omission variant additionally excludes endpoints;
the alternative reconstruction below does not need that stronger interface.

### C. Canonical sparse extraction needs only inclusion queries here

Let F be any nonempty family of k-element subsets of [N], and suppose
I(Y) decides whether some W in F is contained in Y. There is a simple
ordered-deletion procedure for the lexicographically greatest increasing tuple:

1. Maintain chosen prefix Q and its last element b (initially empty and 0).
2. Binary-search the greatest x in [b+1,N] with I(Q union [x,N]) true.
3. Append x to Q and repeat k times.

**Proof.** The invariant is that every witness contained in Q union [b+1,N]
contains Q, and at least one such witness exists. Initially it is immediate.
The predicate is monotone because its query sets shrink as x increases. The
lower endpoint is true. The sentinel x=N+1 is false while |Q|<k because no
k-element witness fits in Q alone. At the greatest true x=q, every remaining
witness contains q: one avoiding q would also fit in Q union [q+1,N], contradicting
maximality. Earlier chosen elements remain essential under further restriction.
Thus q is the largest attainable next coordinate. Induction proves both the
invariant and whole-tuple lexicographic maximality. After k stages Q is a witness.
There are at most k ceil(log₂(N+1)) threshold calls, apart from the initial
existence/optimum computation. Query sets can be generated in O(N) space/time
per call, which is dominated by the oracle in this application.

This is an elementary ordered self-reduction. We make **no novelty claim** for
this lemma and do not misattribute this exact canonical formulation to S3.
It explains why S4's warning about arbitrary extension queries is not an obstacle:
along this particular greedy path, the fixed elements are already essential.
It does not provide an extension oracle for an arbitrary requested prefix.

Apply the lemma to F = all minimum-cardinality omission sets, N=h, k=t=n-L,
where L is the unconstrained optimum length. Realize I(Y) by requiring selected
every index in [h] outside Y and testing whether the score remains L. This is
the oracle of B. Since two optima have equal cardinality, the first index on
which their omission sets differ reverses the order of their selected tuples.
Lexicographically greatest D therefore gives lexicographically least entire S.

### D. Combine all costs

There are O(1+sqrt(H) log(h+2)) score calls. Multiplying by the per-call bound,
then charging the one-time suffix scan, sorting, and streamed complement output,
gives O(n+H^(5/2) log²(h+2)) time. Sequential reuse of the matrix gives O(H²)
auxiliary wide words. Store only the O(sqrt(H)) omissions; write one output tuple
and validate it with indexed reads, without output-sized temporary slices.

Thus the **complete target bound follows from this composition**. The remaining
specialized work is the deficit reduction, harmonic count, legal-mask argument,
and careful input/output accounting. The sparse-reconstruction multiplier is
not persuasive evidence of an independently new general algorithm.

## Strongest attempted black-box implications and why they stop

| Hypothesis tested | Result / rigorous correction |
|---|---|
| S3 Algorithm 1 already returns our canonical witness | **False.** For F={{1,4},{2,3}} on [5], an allowed first partition {2,3} / {1,4,5} deletes the former and returns {1,4}; lex greatest is {2,3}. Both witnesses have size 2 and weight 5. This is a set-oracle counterexample, not a claim that this exact family is realized by some A. Use the ordered procedure in C. |
| Sorting the universe before S3's FIFO procedure fixes lex order | **False.** With F={{1,2},{1,3}} on [4], contiguous first halves {1,2}/{3,4} allow deletion of the second half, yielding {1,2}. Order alone does not repair its deletion priority. |
| S3's stronger total-runtime bound removes a log from G9 | **Unproved.** Its runtime transfer assumes an oracle scaling with the shrinking universe in a specified superadditive way. The G9 resource dimension and original index weights remain h after deletions. Renumbering changes the problem. Charge each call at its full proved cost. |
| S6 temporal expansion plus S2 directly proves quadratic space | **Insufficient as a black box.** Give each eligible edge departure time equal to its difference rank and duration 1. Then successive temporal edges correspond exactly to strictly increasing differences. Expand arrival/departure copies and waiting arcs. Assign gap resource and cost -1 to travel arcs, 0 to waiting arcs, plus start resource/length. This produces O(M+p) vertices/arcs; an explicit resource table uses O(MH)=O(H² log H) words. The rolling endpoint compression in B is still required to reach H². |
| S6's shortest temporal path objective is already ours | **False.** Maximum selected cardinality is not minimum duration/hops. The above negative-cost DAG reduction repairs the objective; it is our construction, not a claim about S6's stated objective. |
| General Hirschberg-style traceback automatically gives the exact theorem | **Not established.** A local predecessor tie rule does not automatically encode lex order on entire original-index tuples; the inspected general theorem also promises polynomial time rather than this exponent. |
| Exact Subset Sum alone solves the omitted-set problem | **False.** Equal omitted weight does not ensure convexity of the selected complement or optimum cardinality. Discarding those constraints is not a valid reduction. |

## Executed independent checks

[reduction_checks.py](reduction_checks.py) imports no repository solver.
[results.json](results.json) records seed 20261024, script hash, and results:

- All **2,228** nonempty uniform set families on universes of size 1 through 5
  verified the ordered inclusion-only extraction against the true lex maximum.
- **3,000** further random uniform families on universes of size 6 through 15 passed.
- **7,612** MOCOSO instances compared the independently built score/reconstruction
  composition with direct enumeration of nonempty selected tuples and the modulus.
  There were **1,397** feasible instances and **29** with multiple optimal tuples.
- **30,448** arbitrary-required-selection score comparisons passed.
- Both failed canonical-transfer hypotheses above have executable counterexamples.

The test sweep batches equal differences simultaneously instead of reusing G9's
tie scheduler. It deliberately uses slower all-pairs generation and dense scratch
merges; **its elapsed time is not evidence for the optimized asymptotic bound**.
The mathematical analysis above concerns the sparse enumeration and descending-
destination implementation. Finite tests establish neither priority nor a proof
of asymptotics. Earlier PR16's test totals are not counted as new evidence here.

Reproduce from the repository root:

```sh
python research/v03/g9_priority/reduction_checks.py
```

## Five separate verdicts

| Axis | Verdict |
|---|---|
| Mathematical correctness | **Supported under the explicit model.** The independent derivation recovers both bounds and full lex order. No mathematical counterexample was found in this investigation. |
| Implementation correctness | **Original pinned implementation still fails its claimed auxiliary-space bound** because validation slices copy the output. The research correction in PR16 addresses that defect. This pass tests an independent reduction, not a new full re-audit of every historical implementation. |
| Asymptotic improvement | **Qualified tradeoff.** Relative to the repository's G8 stated bounds, quadratic auxiliary space saves a log while the stated time pays an extra log. An external state-of-the-art dominance claim is not established. |
| Literature priority | **General mechanism priority belongs to prior work; exact specialized-statement priority remains unresolved.** No identical full theorem was identified, but the full upper bound is derivable by the elementary composition above. |
| Scientific significance | **Modest specialized contribution; incremental/combinational.** Suitable framing is a carefully attributed technical note. The evidence does not support a breakthrough or a new generic canonical-witness method. |

## Effect on the existing manuscript

PR17 already avoids worldwide-firstness language, but its bibliography and
discussion are incomplete without S3 and the inclusion/extension distinction in
S4. S6 is relevant to the path-reduction comparison. The preprint locus for S5
is now verified directly: **v2 Proposition 5**, rather than assuming journal and
preprint proposition numbers coincide.

[MANUSCRIPT_AMENDMENT.md](MANUSCRIPT_AMENDMENT.md) supplies concrete replacement
wording and [additions.bib](additions.bib) supplies the missing references.
This PR preserves the existing manuscript exports and every G3–G9 implementation;
the amendment is explicitly pending integration, so those exports should not be
treated as incorporating this investigation. No merge or external submission is
performed. A writing plugin cannot change the literature-priority verdict.

Search scope and unresolved leads are documented in [SEARCH_LOG.md](SEARCH_LOG.md).
No expert was contacted; no claim of exhaustive coverage, independent human
review, or peer-review acceptance is made.
