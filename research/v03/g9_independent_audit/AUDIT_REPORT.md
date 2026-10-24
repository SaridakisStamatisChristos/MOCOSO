# Independent G9 mathematical and scientific audit

Audit date: 2026-10-24. Target: draft PR #15, **96ac7e2df040ed964bc36f0ad4e00d541b3f1f2d**.
Audited source: `experiments/v03/g9_quadratic_lex.py`, Git blob
`bcdbabc1cde45d357baa64fd78a693889258855b`.

**Finding: the abstract exact canonical-witness algorithm is supported by an independent
human proof, but the pinned executable does not satisfy its stated auxiliary-space
bound with assertions enabled.** Its final validation creates two output-sized tuple
slices. A separate research-only derivative repairs this defect without changing the
DP or reconstruction decisions. Neither the original G3–G9 files nor production code
are edited. This is an audit, not a manuscript or a formal proof-assistant certificate.

## Five separate verdicts

| Gate | Verdict | Precisely supported conclusion |
|---|---|---|
| Mathematical correctness | **SUPPORTED, abstract algorithm** | The deficit reduction, constrained scalar sweep, monotone threshold reconstruction, and whole-tuple lexicographic order are correct under the stated domain. The proof below independently derives them. The stronger claim that the pinned executable realizes all resource bounds is false. |
| Implementation correctness | **PARTIAL** | No wrong witness found; new independent oracles and the upstream suite pass. **Auxiliary-space compliance is CONTRADICTED** at pinned lines 108–109. The included corrected derivative passes the same independent corpus and memory regression. |
| Asymptotic improvement | **SUPPORTED after correction, as a tradeoff** | The abstract/corrected algorithm has time `O(n+H^(5/2) log²(h+2))` and auxiliary space `O(H²)` wide words. Relative to G8's stated core bounds it saves a log factor in space and spends a log factor in time; it is not a simultaneous time improvement over G8. No optimality lower bound is established. |
| Literature priority | **UNRESOLVED; mechanisms substantially overlapping** | Primary sources already disclose the sweep and equal-difference order, exact-resource DP, and canonical extension search. No inspected source states the complete specialized theorem. Its combination is elementary and does not establish a new general primitive or worldwide priority. |
| Scientific significance | **MODEST / INCREMENTAL on present evidence** | A useful, rigorously explainable, specialized time–space tradeoff and a repaired research artifact. Independent practical importance, external algorithmic superiority, and standalone theory-paper significance are not established. |

Here and below `H=h+1`. All space bounds exclude read-only input and the one returned
output buffer, but **do not exclude other objects merely because they copy output**.

## Independence and scope

The repository and its claimed proof were inspected to identify the exact object being
audited; no prior proof or test outcome was accepted as evidence of correctness.
The proofs below were reconstructed from the source operations and the original
optimization definition. `audit.py` contains newly written selected-subset enumeration,
a full-input last-two-indices/selected-sum DP, and distinct-part enumeration. It imports
no upstream oracle. A separate instrument exposes the actual nested G9 scalar oracle
by changing only the return boundary, allowing its intermediate answers to be checked.

This is methodological independence within one audit session, not a claim of blinded
authorship, an independent human reviewer, or a separate-model replication. The
corrected solver is explicitly an attributed derivative, not a clean-room algorithm.

## A. Reconstructed model and independently derived proof

Assume `n>=2`, integer array entries of either sign, integer `m>=2`,
`U=n(n+1)/2`, `U/2<m<=U`, and `0<=h=U-m<n`. A witness is a nonempty increasing
tuple `S=(s1,...,sL)` of original indices, with `sum(S)` divisible by `m` and

`a[s(k+2)] - a[s(k+1)] > a[s(k+1)] - a[sk]`

for every consecutive selected triple (mathematical indices are 1-based). Maximize
`L`, then minimize the entire `S` lexicographically. Return `()` if no nonempty
witness exists. This is value-difference convexity, **not** divided-difference
convexity using the original index distances, and the resource is the sum of indices,
not the sum of values.

### A1. Exact complement and the two compulsory anchors

A nonempty index sum is positive and at most `U<2m`, so the only permitted multiple
is exactly `m`. Thus its complement `D=[1,n]\S` consists of distinct positive
indices whose sum is exactly `h`. In particular each omitted index is at most `h`.
All indices `h+1,...,n` are compulsory.

Let `p=min(n,h+2)`. If `p<n`, both `h+1` and `h+2` are selected. Every selected
triple ending at `k>=h+3` is therefore precisely `(k-2,k-1,k)`. These triples
can be checked once. The triple crossing from a mutable predecessor into the first
two compulsory positions ends at `h+2`, and **must remain inside the core DP**.
If `p=n`, there is no detached suffix. Hence a feasible core ending at `p` extends
to the full witness by appending `p+1,...,n`, if and only if the one-time suffix
test passed. Using just one compulsory anchor would miss a boundary constraint.

For `t=|D|`, distinctness gives `t(t+1)/2<=h`; thus
`t<=floor((sqrt(8h+1)-1)/2)`. In particular `t=O(sqrt(H))` and every length-optimal
witness has the same omission cardinality `t=n-L`. The empty fallback must be
handled before applying that argument.

### A2. Legal edges and independent sparsity count

If consecutive selected indices are `i<j`, their gap omits exactly the indices
`i+1,...,j-1`. Any compulsory index in that gap invalidates the edge. Otherwise its
cost is

`g(i,j)=sum(i+1,...,j-1)=u*i+u(u+1)/2`, where `u=j-i-1`.

All costs are nonnegative, so `g>h` cannot be used by a feasible path. For `u>=1`,
`u(u+3)/2<=h` is necessary because `i>=1`; also `i<=h/u`. Consequently the count
of eligible edges is at most

`M <= p-1 + sum_{u=1}^{floor(sqrt(2h))} floor(h/u) = O(H log(h+2))`.

This bound counts even some infeasible initial-prefix combinations, which only
makes it an upper bound. Adjacent edges account for `p-1`. For each fixed source
`i`, both gap cost and the event of skipping a compulsory index are monotone in
`j`; the two early `break`s in the source cannot lose a legal edge. Enumeration
therefore uses `O(M+p)` iterations, not `Theta(p²)` on these inputs. The clipped
triangular formula in the source equals the ordinary gap sum on all admitted
edges. Sorting once costs `O(M log(M+1))` operations and `O(M)` temporary words.

### A3. Constrained scalar oracle without witness histories

For a fixed omitted set `Q` and threshold `x`, force every member of `Q` to be
omitted and every index below `x` outside `Q` to be selected. Define `F(Q,x)` to be
the maximum full witness length under these constraints, or zero when impossible.
The reconstruction uses increasing `Q` with all its members below `x`; the oracle's
constraint semantics also make sense for the additional arbitrary sets used in testing.

Initialize a singleton core at each allowed first endpoint `i` with omission cost
`W(i-1)=i(i-1)/2<=h`, provided it skips no required index. Starting beyond `h+1`
would skip a compulsory index, so the initialization range is correct. A pair
transition `i->j` is admitted only if neither endpoint is forbidden and its open
gap contains no required selected index. The prefix-count test is exactly this
condition: `required[j-1]-required[i]=0`.

Induct on the sorted event order `(a[j]-a[i], -j, i, j, g)` and regard singletons
as paths with last difference minus infinity. Immediately before event `(i,j)`
with difference `d`, every available non-singleton path ending at its source `i`
has last difference strictly below `d`: smaller-difference events have all been
processed, while already processed equal-difference edges have destination at
least `j`, hence cannot enter `i<j`. Equal destination ties do not matter.

Thus any retained source path can be extended legally. Conversely, the final
edge of every feasible path is processed after its preceding edge. At that time
the scalar table contains a path of at least the same length at that predecessor
endpoint and the same exact resource. Replacing the predecessor with this longer
path is safe because it too has last difference below the current `d`, meets the
same constraints, and uses the same omitted weight. This proves completeness of
the length optimization as well as soundness of every transition.

The important qualification is **event-relative dominance**: the final table is
not a universal endpoint/resource summary valid for arbitrary earlier slope
thresholds. Recomputing a fresh sweep for each oracle call is what makes a
single scalar per cell valid. A claim of timeless endpoint-only dominance would
be false; the actual algorithm does not need it.

Initial cost plus successive gap costs is exactly the omitted weight before
the terminal core endpoint. Since `p` and every later index are compulsory,
`dp[p][h]` enforces all omissions, including every forbidden `Q` index. The
returned score `dp[p][h]+n-p` is therefore exactly `F(Q,x)`, when reachable.

### A4. Monotone search and preservation of an optimal completion

Let `L=F((),1)>0` and `t=n-L`. Maintain an increasing prefix `Q` of the omitted
tuple of at least one global optimum, and let `b` be its last index, or zero.
While `|Q|<t`, for every integer `x` in `[b+1,h+1]`,

`F(Q,x)=L` iff an optimum has omission prefix `Q` and next omission at least `x`.

Indeed, all non-Q indices below `x` are forced selected; all Q indices are
forced omitted; an optimum still has `t-|Q|>0` omissions left. Conversely any
such completion obeys precisely these constraints. Its value cannot exceed
the unconstrained maximum `L`.

The feasible sets shrink as `x` increases, so equality with `L` is a true-then-false
predicate. The low endpoint `b+1` is feasible by the maintained invariant. The
sentinel `h+1` is infeasible: it allows no further omitted index at most `h`.
Binary search therefore finds the largest true integer `x*`. Some optimum has
its next omission at least `x*`. If that next omission were strictly larger,
`x*+1` would be feasible too, contradicting maximality (including the sentinel
case). Hence an optimum exists with next omission exactly `x*`; appending it
preserves the invariant. Induction over all `t` positions constructs the
lexicographically greatest optimal omission tuple.

The predicate "next omission equals x" is a different, nonmonotone predicate.
For `a=(1,3,9,27,81,243,729)` and `m=22`, the only optimum omits index 6:
its equality predicate on `x=1,...,7` is `F,F,F,F,F,T,F`, whereas G9's threshold
predicate is `T,T,T,T,T,T,F`.

### A5. Whole-witness lexicographic optimality

For two distinct optimal omission sets of the same cardinality, consider the
smallest index in their symmetric difference. The complement that retains that
index has the smaller next selected element after their common selected prefix.
The omission tuple that retains this index in its complement instead omits a
larger index at its first differing omission position. Thus omission lex order
is reversed by complementation for these equal-cardinality tuples. This proves
the least **entire** selected tuple, not just the least last index or a local
tie choice. The identical compulsory suffix cannot change that comparison.

## B. Time, space, and bit complexity

The cost of one scalar query is `O(pH+MH)=O(H² log(h+2))`: it includes a fresh
matrix, flags, required-index counts, and all resource attempts. It contains
no scan of the length-n suffix. The source's extra assertion query at the
beginning of each omission step **is included**. Total queries are at most

`1+t(1+ceil(log2(H))) = O(1+sqrt(H) log(h+2))`.

Repeated feasible and infeasible searches, including final-step searches, are
all covered. One-time preprocessing and suffix validation, this query product,
and deterministic complement emission give

`T=O(n+H^(5/2) log²(h+2))`.

Only one matrix exists at a time; completed calls retain no DP histories.
Matrix `O(H²)`, reusable sorted events and sort workspace `O(H log(h+2))`, flags
`O(H)`, omitted tuple `O(sqrt(H))`, and constant-size output cursor/validation
state yield **O(H²) auxiliary wide words for the corrected algorithm**.
Since `log²(H+1)=O(sqrt(H))`, this also meets `O(n+H³)` time. This is an
asymptotic upper bound, not a claim that logarithms are numerically small.

The pinned source also uses hash-set membership for output emission. A general
deterministic O(1)-dictionary assumption is not specified in its wide-word model.
The corrected derivative uses an increasing omission cursor instead, establishing
O(n+t) output work without relying on hash-table behavior. This is removal of
an accounting assumption; no concrete hash-related wrong output is alleged.

Let `B>=1` bound signed input bit length, and take word width
`b=Theta(B+log(n+2))` with adequate constant factors. It covers signed differences,
`U=Theta(n²)`, scores, indices, addresses, and polynomially many relaxation counts.
Using schoolbook integer arithmetic, the safe coarse overlay is

`O((n+H^(5/2) log²(h+2)) b²)` bit operations,
`O(H² b)` auxiliary bits for the corrected algorithm.

Input storage can be O(nB), output O(n log(n+2)) bits. Arbitrary-size integers
are not constant-cost 64-bit values. These are logical word/bit-space bounds,
not a hard bound on CPython RSS, garbage collectors, or allocator bookkeeping.

### B1. Verified counterexample to the pinned space claim

Choose **any n>=3**, `h=0`, `m=U`, and `a_i=i²`. The unique feasible optimal
witness is `(1,...,n)`, and all convexity checks pass. The core has constant
size. At pinned lines 108–109:

```python
zip(selected, selected[1:], selected[2:])
```

materializes two separate tuples of sizes `n-1` and `n-2`, retained together
by the zip iterator. They are temporary auxiliary arrays of references, distinct
from the returned tuple. Even a logical wide-word model charges Theta(n) words
for them; excluding output or disavowing RSS does not remove those arrays.
Since H=1 while n is unbounded, O(H²) is contradicted. An appropriate general
upper bound for the pinned code's logical auxiliary storage is O(n+H²).

The traced experiment resets its peak only **after the returned tuple exists**,
isolating validation allocations from output materialization. Exact local numbers
are in `results.json`; at n=100000 the original needs approximately 1.60 MB
additional validation storage, versus under 2 KB in the corrected derivative.
The analytical counterexample proves the violation; the measurements corroborate it.

`solver_corrected.py` replaces tuple-slice validation with indexed reads. It also
emits the complement through a deterministic cursor with an exact remaining-length
hint. It does not change event preparation, oracle recurrence, query thresholds,
or tie-breaking. Assertions remain enabled. Running the original with `python -O`
would also remove the offending assertion, but is not the correction adopted here
and was not a condition of the original theorem.

## C. Executed falsification and reproducibility

See `audit.py`, `results.json`, `run.log`, and `REPRODUCE.md`. New audit corpus:

| Check | Executed scope |
|---|---:|
| Exhaustive selected-subset comparisons, alphabet {-3,0,5}, n=2..8, every valid deficit | 73,809 inputs |
| Seeded direct selected-subset comparisons, n=3..12, six input families including 120-digit signed values | 6,000 inputs |
| Independent pair-state/selected-sum DP, full witness comparison | 1,800 of those inputs |
| Direct scalar-oracle comparisons at arbitrary forced sets and all thresholds | 13,767 queries |
| Pair-state constrained-score comparisons | 1,565 of those queries |
| Eligible-event set equality versus direct gap enumeration, plus harmonic envelope | 201 deficits, h=0..200 |
| Planted feasible witnesses against independent distinct-part enumeration | 450 inputs, h<=34, n<=94 |
| Proven maximal-omission stress family | 6 inputs, t=1,2,4,8,12,16 |
| Constructed three-way ties after 0..5 shared omissions, including signed affine transformations | 18 inputs |
| Fixed-h=0 validation-memory regression | n=1000,10000,100000, both implementations |

Both original and corrected solvers agree with the independent expected full tuple
on **80,283** new witness cases. Nested checks are not additional distinct inputs.
Most random/exhaustive inputs are infeasible; the recorded histogram makes that
imbalance explicit. Planted, maximal-omission, and deep-tie families address it.
Finite agreement is not the proof of universal correctness or asymptotic complexity.

The original six-test G9 suite was also rerun independently and passed; its log is
`upstream_tests.log`. It is supporting reproduction, **not** counted as clean-room
evidence. No reliance is placed on the old CI status or PR review verdict.

### C1. Counterexamples to deliberately broken hypotheses

All are preserved with exact arrays and constraints in `results.json`:

- Ascending equal-difference destination order admits `(1,3,4)` for all-zero
  length-four input with m=8, whereas strict convexity makes the instance infeasible.
- Removing forbidden-endpoint checks makes an impossible forced-omission query
  appear feasible (n=5, m=11, Q=(2,3), x=1).
- Removing required-index gap checks lets a query requiring every mutable index
  return a positive score at nonzero deficit (same n=5 input, Q=(), x=5).
- Removing the required-prefix initialization check admits a singleton start
  after an index that was required selected.
- Replacing p=h+2 with p=h+1 returns an overestimated score by ignoring the
  crossing triple into the compulsory suffix.

These are mutation counterexamples, **not defects present in the pinned recurrence**.
Their purpose is to show the independent tests exercise each essential condition.

### C2. Failed searches and audit-development limitations

- Attempts to disprove event-relative scalar dominance, threshold monotonicity,
  complement lex order, event sparsity, or the charged query count found no
  counterexample in the recorded scopes. Sections A–B provide proofs, not an
  inference from those failed searches.
- A 10,000-instance search for a hole between feasible first-omission values
  found none. It establishes no interval theorem. The simpler equality-predicate
  example above already suffices to refute monotonicity of equality search.
- An initial mutation fixture used all-zero n=3, h=0; the suffix precheck rejected
  it before the mutated core ran. The audit runner stopped at that test assertion,
  after its then-current exactness phases passed. Replacing the fixture by n=4,
  h=2 reached the intended event-order defect. This was an audit-test fixture
  error, not a target-solver failure. The final full rerun is the committed log.
- No machine-checked formal proof, external human referee, or complete global
  priority proof is provided. Cross-version CI is separate from the local results.

## D. Claim–evidence contract and repair priority

| Claim | Status | Evidence / needed action |
|---|---|---|
| Exact objective and full lex tie | SUPPORTED | A1–A5; independent full-tuple and constrained-oracle checks |
| Sparse eligible events and total query bound | SUPPORTED | A2, B; direct event enumeration and charged counters |
| Pinned source has O(H²) auxiliary words | CONTRADICTED | B1 family; explicit tuple slices; memory regression |
| Corrected research algorithm realizes the advertised pair of upper bounds | SUPPORTED in stated model | B; corrected derivative, independent tests; no fixed-RSS claim |
| Better than G8 in both time and memory | CONTRADICTED as an inference from stated bounds | G8 time has one log, G9 two; G9 improves memory |
| Exact theorem already stated in inspected literature | NOT IDENTIFIED | Source-specific comparison in LITERATURE.md; absence is not priority |
| New general reconstruction or convex-sweep primitive | CONTRADICTED | Kluev and extension-search prior sources |
| Standalone major scientific contribution / paper readiness | UNRESOLVED | No lower bound, external superiority, or validated application |

**Major repair:** retain the pinned file as historical evidence and review the new
corrected derivative and explicit implementation qualification before describing G9
as an executable quadratic-auxiliary-space result. Its abstract theorem survives.

**Next research decision:** credit the classical constituents precisely and decide
whether the narrow deficit-parameterized tradeoff merits a technical note or forms
one part of a broader contribution. A stronger bound, lower bound, or independently
motivated application would change the significance assessment; none is assumed.
Keep this research correction draft and unmerged. No paper has been started here.
