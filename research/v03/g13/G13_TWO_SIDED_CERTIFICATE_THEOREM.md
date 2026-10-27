# G13: two-sided linear-time exact certificates

**2026-10-27, RFP deep/OmO native fallback.** G13 is a research-only addition **stacked on G12 PR #25**. Prior G8–G12 sources, the G9 paper, and the G10 candidate theorem are immutable. `modconvex.solve` is not changed. A certificate is an **exact answer** (tuple or empty); `None` means **abstention, never infeasibility**.

## Locked domain

n>=2, signed integers a[1..n], m>=2, U=n(n+1)/2, U/2<m<=U, 0<=h=U-m<n. A nonempty selected index tuple must have index sum m, strictly increasing **consecutive selected value differences**, maximal length and entire-tuple lexicographically minimum among maxima.

## Theorem G13-1 (certified soundness and resource bound)

`experiments/v03/g13_two_sided_certificate.py:certify_g13(a,m)` runs in worst-case **O(n+h)=O(n)** wide-word operations and O(h+1) auxiliary wide words, excluding read-only input and one returned tuple, and satisfies:

- If it returns a nonempty tuple, this is the global canonical optimum, and the optimum omits at most two indices.
- If it returns `()`, no nonempty feasible witness exists.
- If it returns `None`, no optimum with <=2 omitted indices exists, but a feasible optimum omitting >=3 indices may exist.
- In particular, for h<=5 the certificate is *complete*: no three distinct positive indices can sum below 6.
- The solver `solve_g13` passes only `None` cases to the unchanged `solve_g11`. Consequently its unrestricted correctness and worst-case upper bound depend on separately audited G11/G10.

This **does not** improve the general worst-case H-dependent G10 upper bound or establish worldwide SOTA. The specialized O(n) positive cases are output-time-optimal, since printing n-O(1) indices costs Omega(n).

### Proof 1: exact omission sum, suffix and small canonical witnesses

Since 0<sum(selected)<=U<2m, a nonempty selected index sum divisible by m must equal m. The omitted distinct indices Q have exact sum h; therefore Q subset of [1,h] and every index >h is compulsory. Failed original consecutive triples ending at k>=h+3 cannot be repaired by any omission. Check them in O(n) time; any violation means globally infeasible.

For Q empty h must be 0. For one omission Q={h}. For two Q={u,h-u}, 1<=u<h-u. The G12 candidate's prefix sum of original bad triples ending up to p=min(n,h+2) allows constant-time testing of all *unaffected* triples: an original triple ending at k vanishes iff some deleted index q lies in [k-2,k], equivalently k in [q,q+2]. Each deleted position affects at most three original adjacent triples.

Every new consecutive selected triple crossing an omission spans at most 4 original index steps for |Q|<=2 and ends no later than p. Enumerate at most 4 endpoints per omitted index and inspect their two preceding selected indices in constant time. This verifies every changed triple exactly. Thus each one-/two-omission candidate is certified in O(1) beyond O(n) prefix/suffix preprocessing. Test Q={h} first; enumerate pairs with descending first omitted index to return the lex-least **selected** tuple (equivalent to lex-greatest omitted pair among equal sizes).

### Proof 2: only 0–3 pairs need testing if any original triple fails

Suppose an original consecutive triple [k-2,k] violates strict convexity and some candidate omits exactly two indices. At least one of k-2,k-1,k *must be omitted*, otherwise all three remain consecutive selected positions and violate convexity. As the omitted exact sum is h, specifying either omitted index determines its partner uniquely as h-r. Hence **at most three** candidate two-index omitted sets survive this necessary condition. When the number of bad original triples exceeds six, no two omitted positions can hit them all, and no pair enumeration is needed. When no bad original triple exists, at most floor((h-1)/2) pairs are tested. In both cases total time is O(h).

### Proof 3: weighted hitting lower bound for impossibility

For any valid omitted set Q, every originally bad consecutive triple must contain an index of Q. Define the hitting relaxation: find an omitted set R subset [1,h] of **minimum total index weight** sum(R) that intersects each bad original triple ending at <=p. No convexity of bridged triples is imposed, so the minimum `L` is a *lower bound* on the omitted weight of every feasible convex witness.

Scan indices k=1..p with a four-state DP indexed by the two omission bits at positions k-2,k-1. At k, choose `omit=0` (mandatory when k>h), or `omit=1` if k<=h, adding weight k. If the original triple ending at k is bad, reject the transition when the previous two bits and the new bit are all zero. The new mask is `((mask & 1)<<1)|omit`. Initialize mask 00 with cost0; keep the minimum total omitted-index weight per mask. This is an exact weighted hitting-set DP on a width-3 interval hypergraph, with **four states and O(p) operations**, and O(1) auxiliary DP words beyond the already computed bad-triple prefix.

If the minimum L>h, every feasible convex omitted set would need weight >h, contradicting exact omitted weight h. Thus `()` is an **exact infeasibility certificate**. When L<=h the relaxation is merely necessary, not sufficient; G13 correctly abstains if no 0/1/2 omitted witness was already found. This precludes confusing a relaxed hitting solution with a valid convex subsequence.

### Proof 4: resource bound and completeness

Reading/validating signed inputs O(n), compulsory suffix check O(n), bad-prefix O(p)=O(h+1). Check one omitted index O(1), plus <=3 pair candidates when some bad triple exists or O(h) candidates otherwise. Weighted four-state DP O(p)=O(h), O(1) additional DP state, at most one invocation. Build at most one returned output tuple in O(n) time. Since h<n, overall O(n) time, O(h+1) auxiliary charged wide words.

No claim of O(n) unrestricted exact solving is made: `None` calls the existing G11/G10 research algorithms.

## Executed falsification

Fresh standalone local implementation checked **73,809 exhaustive ternary signed instances n=2..8**, each against a simple independent selected-bitmask enumeration. **68,148** had complete correct certificates; **9,648** returned `()` specifically because the weighted-hitting minimum exceeded h. On every abstention, the independent optimum required at least 3 omissions. **Zero mismatches**. Another **10,000** fixed-seed random signed instances n<=11 agreed or safely abstained, zero mismatches.

As a concrete weighted-hitting witness, take n=h+2 and all a[i]=0 for h in {6,8,10,12,19,32,64}. The immutable suffix contains only two positions, so the trivial fixed-suffix check does not apply. Nevertheless, covering every bad original triple by omitted indices has total weight exceeding h; the weighted DP certifies **global infeasibility**.

Cross-platform CI exercises those proof obligations and a seeded differential suite against G11; it should be described as VERIFIED_CI only after actual GitHub Actions results. Tests do not machine-prove the unbounded theorem. No external human referee is represented by RFP/OmO self-audit.

## Prospective benchmark and SOTA claim boundary

`benchmarks/g13_rfp_three_cohorts.py`: exactly 425 cases from the earlier original-plus-holdout G12 benchmark and **252 newly generated holdout cases** (independent seed 26102713), 12 deficit levels x 3 sizes x 7 input families, including flat, signed core, near-convex, plateau, and constructed feasible one/two/three omission families. Five complete exact solvers compared on the same instances: G13, G12, G11, corrected G8, G10; deterministic randomized execution ordering and all losing cells retained. All raw per-case nanosecond repetitions, correctness mismatches, source hashes, and platform details are archived.

This is a within-repository *research* benchmark. It cannot establish universal practical SOTA or worldwide theoretical novelty. The new 252-case cohort is intentionally not used to choose an adaptive threshold after observing its outcomes.

## Prior-art scope

Greedy/local interval stabbing and four-state DP on bounded-width constraints are standard algorithmic techniques. Generic lexicographic resource-constrained path machinery is earlier, including Tellache–Meunier–Parmentier, *Transportation Science* (2024), DOI https://doi.org/10.1287/trsc.2022.0372. G13's narrow exact linear-time certificate combination does **not** assert independent worldwide novelty. G10's joint specialized resource bound and publication-significance questions remain open to an **outside** algorithms referee.

**RFP state:** partial certificates PROOF_SKETCH with human-checkable derivation + TESTED; benchmark provisional until exact CI; global theoretical/practical SOTA UNRESOLVED.
