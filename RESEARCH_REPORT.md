# SQI v2.1 — Modular Convex Subsequence Optimization: evidence-led research report

**Date:** 2026-10-23. **Status:** mathematical proofs are self-audited, not formally machine-checked; finite tests executed. **Source SHA-256:** see `run.log`, `report.json`, and `sha256sum` of files. This is a research deliverable, not a claim of external peer review or publication priority.

## 1. Semantics and objective

Input: arbitrary signed integers `a[1..n]` (including empty arrays), integer modulus `m >= 2`, optionally integer target `K`. Find an index sequence `I=(i_1,...,i_k)` strictly increasing with `1 <= i_t <= n`, satisfying every consecutive triple `a[i_(t+2)] - a[i_(t+1)] > a[i_(t+1)] - a[i_t]` and `sum(I) % m == 0`. Maximize `k`, then minimize `I` lexicographically. Empty sequence is feasible. Threshold decision asks whether optimum length `>=K`. The odd printed comparison symbol in the user's prompt is interpreted as `>` because the prose explicitly says differences strictly increase.

Let `U=n(n+1)/2`, `B=max(1, max_i(abs(a_i).bit_length()+1))`, `L=ceil(log2(m+1))`, `d=#distinct(a)`. `N=n(n-1)/2` is the number of unordered index pairs.

## 2. Foundational lemmas — PROVED

**Large modulus.** Any nonempty sum of selected distinct 1-based indices lies in `[1,U]`. If `m>U`, no nonempty sum is divisible by `m`, so the only feasible answer is empty. Otherwise `m<=U=O(n^2)`, making the full problem polynomial in the ordinary binary input size.

**Index-sum upper bound.** For a subsequence of length `t`, its index sum lies between `L_t=t(t+1)/2` and `H_t=t(2n-t+1)/2`. If `[L_t,H_t]` contains no multiple of `m`, no feasible length-`t` subsequence exists. Therefore `UB_index=max({0} union {t in [1,n]: ceil(L_t/m)<=floor(H_t/m)})` is an upper bound on the optimum. This is a *necessary* arithmetic test, not a sufficient convexity test. In fact every integer in the interval is attainable by some t-subset, but that stronger property is not needed for soundness.

**Distinct-value upper bound.** With `d` distinct values, possible differences between two values are contained in `V-V`, which has at most `d(d-1)+1` distinct elements (at most one zero, and at most `d(d-1)` ordered nonidentical differences). Consecutive differences of a strictly convex length-`k` sequence are strictly increasing and hence pairwise distinct, so `k-1<=d(d-1)+1`, or `k<=d(d-1)+2`. Thus `UB=min(UB_index,d(d-1)+2)` is sound (and is <=n). Constant-value arrays have optimum <=2.

## 3. Exact two-index/residue backward DP — PROVED

For fixed `1<=i<j<=n`, define `F(i,j,r)` as the maximal number of *additional* elements after the fixed first pair `(i,j)` such that their selected **additional** indices sum to `r mod m` and the complete sequence starting with `(i,j)` has strictly increasing consecutive value differences. Unreachable states have `-infinity`; the empty continuation has length 0 and residue 0.

For `k>j`, the first triple is admissible exactly when `a[k]>2*a[j]-a[i]`. The exact recurrence is:

`F(i,j,r) = max(0 if r==0 else -infinity, 1+F(j,k,(r-k)%m) for k>j with a[k]>2*a[j]-a[i])`.

A state additionally stores the smallest next index `k` among all maximum-length extensions, with suffix recursively chosen lexicographically. For each `j`, all required `F(j,k,*)` have been determined when second indices greater than `j` were processed. Base `j=n`: no successor exists, so only residue 0 has length 0. Induction descending in `j` proves every state correct.

**Geometric sweep.** Fix `j`, arrange `k>j` by decreasing `a[k]` and `i<j` by increasing `a[i]`. Threshold `theta(i)=2*a[j]-a[i]` is nonincreasing in the predecessor sweep. Before processing `i`, insert all previously unseen `k` with `a[k]>theta(i)` into residue-indexed table `Best[r]`, using each state `F(j,k,s)` to offer value `1+F(j,k,s)` into residue `(k+s) mod m`; break ties by smaller k. The table contains exactly the admissible successors for the current i. Copy the table into `F(i,j,*)`, adding the empty continuation only at residue 0. Ties among the same k are settled recursively by the canonical state at `(j,k,s)`. Consequently `F(i,j,*)` and its lexicographically least maximizing continuation are exact.

**Global optimum.** Enumerate empty, all singletons with index divisible by m, all pairs with index sum divisible by m, and for every pair `(i,j)` the candidate of length `2+F(i,j,(-i-j)%m)` if reachable. Any feasible length>=2 subsequence has one such first pair; optimal substructure gives no smaller length, and constructed candidates are feasible. Comparing lengths and first pairs chooses the globally lexicographically smallest maximizing solution. The per-pair successor pointers recover the rest. Equal-length distinct candidates with differing first pairs can be compared solely by `(i,j)`; with identical first pair the DP already chose the lexicographically smallest continuation. One final traceback costs O(n).

**Strictness / sign / duplicates / boundaries.** Comparisons use `>` on exact signed integers, not division or floating-point arithmetic. Equal values and equal differences never pass a strict inequality. Empty, singleton, and pair sequences are handled explicitly (the triple condition is vacuous). When a required residue has no extension, only residue 0 receives the empty continuation. The index order is always strictly increasing. No value monotonicity is assumed.

### Operation and memory counts

For each `j=2..n`, at most `n-j` candidates are inserted and exactly `j-1` predecessors are scanned. Each insertion and each predecessor copies at most `m` residues. Hence **at most exactly** `(n-1)^2*m` residue-slot iterations in the full sweep, in addition to O(n^2) threshold/filter/pair operations and O(n log n) comparisons to sort once by value. Flat arrays store lengths and successors for each pair and each residue: exactly `2*N*m` stored integers (`8*N*m` payload bytes in the tested CPython with 4-byte `array('i')`). Additional sorting/sweep arrays require O(n+m) machine words. The implementation does not repeatedly reconstruct candidate witnesses; reconstruction occurs once at the end or resource-limit return.

## 4. Mandatory feasibility theorem — PROVED (abstract algorithm)

**Theorem.** For every finite signed-integer array, `m>=2`, and integer `K`, the unrestricted backward-sweep algorithm returns a correct YES/NO decision for the predicate `OPT>=K`, and its optimization form returns the exact optimum and lexicographically smallest optimal index sequence. On a unit-cost word-RAM with word width enough to hold input values, thresholds `2*a[j]-a[i]`, residues, sums up to `U`, and table addresses, it performs `O(n log(n+1)+n^2+n^2*m)` operations and requires `O(n^2*m+n+m)` auxiliary words. For `m>U`, its answer is immediate after reading the input and comparing m with U. Consequently, across all inputs, there is an unconditional `O(n^4)` worst-case arithmetic-operation algorithm and `O(n^4)`-word worst-case auxiliary space bound, with no dependence on m beyond its binary input representation when `m>U`.

**Proof.** The exact recurrence, induction and sweep invariants from section 3 establish all DP values and lexical choices. Any nonempty feasible subsequence has index sum <=U, so `m>U` is trivial. In the remaining case, `m<=U=O(n^2)`, and the residue work and memory bounds follow by counting all candidate insertions and predecessor copies. The exhaustive cases empty/single/pair and first-pair decomposition cover every feasible solution. Testing `OPT>=K` is correct by definition. All loops and arrays are finite. QED.

**Constant-value specialization.** For d=1 no feasible triple exists. The minimum modular singleton is `(m)` if m<=n. For each i=1,...,n-1 in order, the smallest j>i with `i+j ≡ 0 (mod m)` is `j=i+1+((-2*i-1) mod m)`; the first candidate in range gives the lexicographically first feasible pair. This is exact in O(n) index-level arithmetic after the preprocessing sort used to establish d.

**Explicit useful resource bounds.** Let `q=m` when `m<=U`, else `q=0`; `w=ceil(log2(n+m+3))+B+3`. In an abstract schoolbook bit model with additions/comparisons of b-bit integers costing O(b) and division/modulo of b-bit integers costing O(b²), a conservative bound for the sweep algorithm, including sorting and lex reconstruction, is

`T_bit(n,m,K,B) = O((n²*(q+1)+n*ceil(log2(n+2))+1)*w²)` bit operations,

`S_bit(n,m,K,B) = O((N*q+n+q+1)*ceil(log2(n+2))+B+ceil(log2(m+2)))` auxiliary bits, excluding the read-only input. These are deliberately conservative upper bounds; small K does not worsen them. The underlying tighter word-operation work bound is `O(n log n+n²+(n-1)²*q)` and the memory bound is `O(N*q+n+q)` words. In the `q=0` branch, no DP allocation is needed. Reading the input requires O(nB+log m) input bits; Python implementation memory, interpreter overhead, and allocation limits are platform-dependent.

The constants hidden in O refer to a specified implementation of elementary bit operations, not a guarantee of wall-clock time on arbitrary hardware. An explicit computable **transition count** is the stronger practical guarantee: <= `(n-1)^2*m` for the full DP. An input-size-polynomial upper bound follows since `q<=n(n+1)/2`. One can take `T(n,m,K,B)` and `S(n,m,K,B)` to be the right-hand-side expressions above times fixed model-specific constants.

## 5. Parameterized complexity and thresholds — PROVED

For parameter p, an algorithm is **FPT** if it runs in `f(p)*|input|^c` for a computable f and a constant c independent of p. It is **XP** if it runs in `|input|^{g(p)}` (or equivalent parameter-dependent polynomial exponent). Since the *unparameterized* problem is in P by the above theorem, it is FPT (and XP) under **every computable parameterization**, including `n`, `m`, `K`, `B`, `d`, `(K,m)`, etc., by taking `f(p)=1`. This is a correct classification but mostly uninformative: no new structural dependence on small K has been established. A more informative explicit `m`-dependence is `O(n² m+n log n)` word operations with `O(n²m)` memory, and `m` never exceeds O(n²) in a nontrivial instance. Brute force `O(n*2^n)` gives another, sometimes preferable, FPT-by-n baseline with small memory.

Because the decision problem is in P, a **formal constant-size kernel** exists by fully solving the input and outputting fixed YES instance `(A=[],m=2,K=0)` or fixed NO instance `(A=[],m=2,K=1)`. This is a vacuous kernelization that *already solves* the instance; it is **not** a useful structural kernel in K or m. Whether more useful reductions exist is not established here.

**Decision and optimization.** `OPT>=K` is monotone nonincreasing in K: if true at K it is true at every smaller threshold. Binary search is therefore logically valid, but rerunning a full exact decision algorithm O(log n) times is generally unnecessary. A single optimization DP computes the optimum and lex minimum with the same worst-case bounds. Early YES may return an arbitrary valid witness of length >=K; it does not claim globally lexicographic optimality. A NO is issued only from a proven arithmetic/value upper bound or completed exact search.

`K<=0` is always YES (empty witness); `K>n` is always NO and is handled before sorting by the shipped implementation. Notably, small positive K alone does **not** permit restricting the search to subsequences of length exactly K or to singleton/pair witnesses. Example `a=(0,1,3), n=3, m=6, K=1`: only the complete triple has index sum divisible by 6, and it is strictly convex; no singleton or pair satisfies the modulus.

## 6. Specialized high-modulus algorithm — PROVED

When `U/2<m<=U`, a nonempty index sum divisible by m must equal m itself. Thus the omitted indices have sum `h=U-m`. Every omitted index is at most h. Enumerate all subsets of `{1,...,min(h,n)}` with sum h, take their complements within `[1,n]`, directly verify strict convexity, and choose the lexicographically least longest feasible complement. This is complete because omitted indices cannot exceed h. A simple direct implementation uses at most `2^{min(h,n)}` masks and `O((h+n)*2^{min(h,n)})` arithmetic steps plus `O(n log n)` preprocessing, `O(n+h)` auxiliary words, and additional O(B) bit costs for each triple comparison. This gives a useful gap-parameter FPT bound in `h` independently of the general polynomial-time result. The shipped hybrid invokes this branch for `h<=15`, otherwise it uses the dense sweep. For `h=0`, only the full index set is possible; this can be tested in linear time without any DP.

## 7. Competing exact algorithms

**Independent edge-difference algorithm (`edge_dp.py`).** Construct all edges `(i,j)` with `i<j` and weight `a[j]-a[i]`. Sort by weight ascending and process equal-weight edges *as one batch*. For each vertex v and residue r, retain the best length (and tie-breaking bitmask) of any path ending at v whose index sum is r, using only previously completed weight groups. For edge i->j, extend a best state at i into j with residue `(r+j)%m`. Apply all same-weight updates only after the group completes, preventing equal consecutive differences. Initial states are each singleton. On a fixed-length tie, representing index i by bit n-i ensures the numerically **larger** n-bit membership mask encodes the lexicographically **smaller** index tuple. Take the best residue-0 state, or empty. Correctness follows by induction on difference groups: every strictly increasing-difference path's preceding edge appears in an earlier group, and equal-group staging cannot introduce an invalid extension. This is a complete, structurally distinct exact algorithm.

Word operations with constant-time n-bit masks: O(n² log n+n²m), space O(n²+nm) words. **Actual bit-model** upper bounds are O(n² log n*B+n³m+n²m*log n) time and O(n²*B+n²m) bits, because difference keys have B bits and masks have n bits. Large high-width inputs can make materializing O(n²) differences undesirable. Tested implementation uses Python arbitrary-size bitmasks and lists/dictionaries, so these bounds do not assert its precise heap size.

**Naive forward DP (`cubic_dp` in `modconvex.py`).** Maintain best lexicographically minimal prefix for each last pair `(i,j)` and residue. Enumerate all triples i<j<k and all residues. Strict inequality gates each transition. Correct by induction on the second-to-last index, but storing/copying complete tuples can cost O(n^4*m) time and O(n³*m) bits/words depending on representation. A pointer-based implementation improves memory to O(n²m) words while leaving potentially O(n) lex tie checks. This is an independent structural control (prefix DP vs suffix sweep).

**Brute-force oracle.** Enumerate all 2^n index subsets, verify increasing indices (automatic by construction), sum % m, and each consecutive triple directly; update by length then literal Python tuple order. Runs in O(n*2^n) arithmetic-level checking time and O(n) auxiliary words. The oracle does **not** use the DP recurrence.

## 8. Parameter-regime table

| Regime | Justified exact method | Proven bound (word operations; input values fit words) | Caveat |
| --- | --- | --- | --- |
| Small n, arbitrary m | Brute force or sweep | O(n*2^n), O(n) words; or sweep O(n²m+n log n) when m<=U | Choose by concrete resource budget |
| Small fixed m, large n | Backward geometric sweep | O(n²m+n log n), O(n²m) words | Quadratic for fixed m |
| Large m, small n | `m>U` shortcut, else brute force | O(n) or O(n*2^n) | No dense modulus table needed for oracle |
| `m>U` | Empty subsequence | O(n) to validate/read, O(1) extra words | Exact, all B and K |
| `m=U` | Full-index-sequence check | O(n) arithmetic comparisons | If full sequence fails, empty is optimal |
| `m>U/2`, small `h=U-m` | Omitted-index enumeration | O(n log n + (n+h)*2^min(h,n)), O(n+h) words | Exponential in h, not in n |
| Small positive K | Full solver; optional early feasible witness | O(n²m+n log n) worst case | No general K-only speed theorem beyond P |
| K>n | Immediate infeasible | O(1) following input-length knowledge | Pure logical shortcut |
| d=1 | Modular-compatible singleton/pair arithmetic shortcut | O(n) index operations after O(n log n) initial sorting; O(n) without sorting in dedicated implementation | Convex length >=3 impossible |
| Very large signed values | Exact-int sweep | Same word operations if B fits word; bit costs include B | Never use floating comparisons |
| No helpful structure | Sweep, with m<=U | O(n⁴), O(n⁴) words globally | This is upper bound, not lower bound |

## 9. Resource budgets and certificates

`solve(a,m,K=...)` returns `FEASIBLE`, `INFEASIBLE`, or `RESOURCE_LIMIT`; `solve(a,m)` returns `OPTIMAL` or `RESOURCE_LIMIT`. `Result.indices` is a concrete valid certificate whenever nonempty and `verify(a,m,indices)` checks it independently. `lower_bound = len(indices)` is always certified, even after interruption; `upper_bound` is a proved bound: normally `min(UB_index,d(d-1)+2)`; the immediate `K>n` exit uses the coarser valid bound `n`. Full `INFEASIBLE` results are justified by the upper-bound tests or exhaustive completion of one of the exact algorithms. The only time a result contains `length` is exact optimization completion.

`max_operations` **strictly caps the counted residue-slot iterations / complement masks**, not instruction count, sorting/preprocessing or wall time. `max_seconds` is a cooperative **soft** wall-clock budget checked at bounded algorithm checkpoints, and may overshoot. `max_heap_bytes` uses `tracemalloc` with a mandatory-array preflight and cooperative **soft** measurements; it is not a hard RSS cap and may overshoot between checks. `MemoryError` and `OverflowError` are converted to `RESOURCE_LIMIT`. Full process hard memory ceilings require external operating-system/container limits; platform-dependent OS termination is not guaranteed to be intercepted and reported from within the same Python process. No claimed completion guarantee within user-specified T_max / M_max is made unless actual worst-case bounds fit the specified computing model and physical resource constraints.

Even without early stopping, the abstract algorithm terminates for every finite input with unbounded resources. The concrete Python process may hit OS memory/address limits; such failure must not be interpreted as mathematical infeasibility. `array('i')` assumes its index and length fields fit the platform signed integer representation (4 bytes in the tested runtime); theoretical algorithms use enough bits to represent n.

## 10. Adversarial counterexamples — PROVED where indicated

**Earliest admissible extension is not optimal.** Choose a1=0,a2=0,a3=0,a4=1 and m=2. The heuristic that begins with indices (1,2), then greedily appends the earliest admissible next index, obtains (1,2,4), sum 7 odd, and has no modular-valid nonempty prefix. However (1,3,4) is convex (differences 0 then 1), index sum 8 even, and length 3. In the version of this greedy heuristic that fixes start (1,2), this is minimal n for a failure with optimum length >=3: at n<=3, a feasible triple necessarily equals (1,2,3), which the greedy accepts. The more trivial n=2,m=2 example `a=(0,0)` gives valid singleton (2), whereas earliest full prefix (1,2) is invalid modulo 2.

**Dropping the residue dimension is unsound.** For `a=(0,0,0,1)`, `m=3`, optimum is (2,3,4), length3, sum9 divisible by3. A prefix-only DP keeping a single best subsequence for each last pair, regardless of residue, instead retains (1,3,4) for last pair (3,4) (also length3 but residue 8 mod3), and may report only (1,2), length2. Thus the residue state cannot be dominated solely by length and lex order. This concrete failure was found by enumeration of arrays in `{0,1,2}^4` and m values increasing; it is not a universal minimality claim beyond the stated n ordering.

**Strictness.** Constant arrays cannot yield triples: adjacent differences both zero. The edge-based algorithm must batch equal-difference edges. Without batching, it may chain two equal-difference edges and output an invalid subsequence. With `a=(0,1,2), m=6`, all three indices sum to6 but their value differences are equal, so the correct answer is empty (no singleton or pair has sum divisible by6).

## 11. Executed tests and benchmark evidence — VERIFIED-COMPUTATIONAL

`research_tests.py` ran **13,311 unique inputs**, including full domains `n=0..4`, values in `{-2,-1,0,1,2}`, each tested at all `2<=m<=U+3` (the n=0 case uses m=2..3), plus `n=5` on `{-1,0,1}^5` with m=2..19 and 295 uniquely generated seeded cases. **9,828 decision invocations** covered threshold extremes. Every optimizer result was checked against the independently enumerating brute-force oracle; a sample also checked the naive forward DP. **0 mismatches**. Seed=20261023. Independent `edge_trials.py` checked 5,775 further instances against oracle, seed=7919; **0 mismatches**. Some cases may overlap across the two suites; therefore do not add their unique counts as if globally deduplicated.

Measured on Linux 6.18.55 x86_64, Python 3.13.5. Wall times exclude process startup, with three repetitions per benchmarking case; no claims of statistically stable crossover thresholds. Selected medians from `report.json` (the latest final run):

| n | m | family | Python sweep median (seconds) |
| ---: | ---: | --- | ---: |
| 25 | 2 | convex quadratic values | see report.json |
| 50 | 2 | convex quadratic values | see report.json |
| 100 | 2 | convex quadratic values | see report.json |
| 180 | 2 | convex quadratic values | see report.json |
| 100 | 20 | constant values | see report.json |
| 100 | 20 | alternating values | see report.json |
| 100 | 20 | seeded random | see report.json |

Selected independently logged complement-comparison result (`extra_report.json`): n=25, m=317, h=8; sweeping with complement disabled took about 0.037 seconds, while complement enumeration took about 0.00076 seconds in that measured run. This is a measured speed difference on a single family, not a universal dominance claim. The `edge_report.json` includes medians for sweep-versus-edge with n=30,50,100 and m=2,10,20; results are mixed, as expected. Heap traces (`tracemalloc`) were taken separately for n<=50 to avoid perturbing time observations; larger rows have null heap measurement, not zero. `ru_maxrss` samples are process high-water marks contaminated by earlier work in the same Python process, **not** standalone incremental solver RSS figures. Resource interruption tests exercised zero operation budget, zero time budget, and a 1000-byte soft heap budget, with correct `RESOURCE_LIMIT` statuses and certified bounds/witnesses.

The first larger exhaustive campaign timed out and produced no result log; it was superseded by the declared reduced complete domains. No tests are described as passed from that timed-out campaign. Final logs, raw measured repetitions, seed, case breakdown, SHA-256, and code versions are packaged alongside this report.

Run: `python research_tests.py && python edge_trials.py && python extra_trials.py` from this directory. Python standard library only.

## 12. Prior art and frontier — SUPPORTED / UNKNOWN

The underlying *unconstrained* convex-subsequence recurrence is taught in University of Illinois CS/ECE 374 Fall 2020 discussion solutions, page 4: https://courses.grainger.illinois.edu/cs374/fa2020/labs/sol/lab_07_a_sol.pdf . A 2013 Stack Overflow answer by Evgeny Kluev describes a difference-sorted O(n² log n) algorithm and a cubic pair-DAG algorithm for ordinary longest convex subsequence: https://stackoverflow.com/questions/20664920/longest-convex-subsequence-in-an-array . A 2014 algorithms note discusses dynamic programming via endpoint and last difference: https://algnotes.wordpress.com/2014/02/01/longest-convex-subsequence/ . These establish **prior art for the non-modular convex problem and the ordered-edge principle**, not a published bound for the full modular/lexicographic problem. No exhaustive systematic literature review of the full modular variant was completed, so novelty of the geometric-sweep residue extension is **UNKNOWN**.

Unresolved: whether the combined modular, lex-minimum problem has a better worst-case bit-complexity and/or memory bound, whether the memory table can be reduced without repeated DP computation, structural kernelizations better than the trivial P-kernel, and fine-grained lower bounds. No W-hardness, ETH/SETH hardness, optimality, or new SOTA claim is asserted. Experimental single-machine runtimes cannot prove asymptotic optimality. Reproducing larger scaled tests with strict external OS memory ceilings and C++/Rust fixed-word vs bignum implementations would be the next practical engineering task.

## 13. Final assessment

**PROVED:** polynomial-time decidability; U-cutoff; dense suffix DP recurrence and sweep; tie-breaking; upper bounds; high-modulus complement method; distinct-value length bound; FPT-by-membership-in-P classification; batch edge-weight DP correctness.

**VERIFIED-COMPUTATIONAL:** 13,311 main unique inputs, 9,828 decision calls, 5,775 independently coded edge algorithm oracle cases, reported benchmark cases and resource-interruption samples. No mismatch in executed suites; they are finite.

**SUPPORTED:** historical unconstrained convex-subsequence algorithms from the linked sources.

**HYPOTHESIS:** a sparse residue representation could outperform the dense sweep in selected high-m regimes, but deterministic worst-case benefit is not shown here.

**UNKNOWN:** best possible worst-case complexity, sharper memory trade-offs, strong parameter-dependent K improvements, and originality of the precise modular sweep formulation.

**Practical conclusion:** the hybrid backward sweep / small-deficit complement enumeration is a correct, reproducibly tested exact baseline with an explicit polynomial worst-case upper bound and sound resource-limit distinctions. It is not claimed to be asymptotically optimal or state of the art.
