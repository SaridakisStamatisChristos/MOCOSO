# G2 — Independent mathematical proof audit (Theorem Foundry)

**Date:** 2026-10-23 UTC. **Reviewer:** separately invoked `@Theorem Foundry` skill. **Independent of G0 developer proof assertions and G1 novelty verdict**, although supplied source and handoff were read as *targets*. Frozen original algorithm/code target: [`7595130fecb1a21dc8ca8823d9ee8d5d136af97a`](https://github.com/SaridakisStamatisChristos/MOCOSO/commit/7595130fecb1a21dc8ca8823d9ee8d5d136af97a). G2 review branch: `research/v03-g2-theorem-foundry`, based on G0 head `567c5bfca0eda13c8ff98045423f16038f37e609`, **not on G1 PR #5**. The G2 CI uses GitHub's generated PR test merge commit (reported `fbd022c47474d940bc05fba56b51ae14c59b7792` on the initial run), with a successful guard ensuring solver/proof source bytes match the original T1 head. No production solver was edited.

## 1. Canonical mathematical contract (no implicit assumptions)

For every integer `n>=2`, finite arbitrary signed-integer sequence `a=(a_1,...,a_n)`, integer `m>=2` with `U/2<m<=U`, where `U=n(n+1)/2`, set `h=U-m` and `q=min(n,h)`. (There is no valid such `m` for `n<2`.) A solution is a sequence of distinct, strictly increasing 1-based indices `I=(i_1,...,i_k)`, possibly empty, with index-sum congruent to zero mod `m`, and satisfying `a_{i_{t+2}}-a_{i_{t+1}}>a_{i_{t+1}}-a_{i_t}` for every consecutive triple. Optimize by maximum `k`, then minimum *full index tuple* lexicographically. For integer threshold `K`, decide `OPT>=K`; a feasible witness may certify YES before optimum is known.

Let `D_q(h)` count subsets of `{1,...,q}` with sum `h`, with `D_0(0)=1`; let `P_d(h)` count unrestricted partitions of `h` into distinct positive integers, `P_d(0)=1`.

**Computational model for the conditional theorem:** uniform-cost RAM whose *word* holds input integers and intermediate signed differences (up to `B+O(1)` bits for `B=max_i bitlength(|a_i|)+1`), indices up to `n`, sums up to `U`, the DP addressing range `(q+1)(h+1)`, and counters; it charges O(1) for integer add/subtract/compare, indexing, word writes and one word of storage. This is a **wide-word** model when `B` is very large; it is **not** the conventional `Theta(log input_length)`-word RAM for unbounded-precision input values. The complexity claim applies to **successful, unrestricted mathematical algorithm execution**; it excludes input storage, returned `O(n)` witness, Python interpreter/tracemalloc/environment overhead and hard memory faults. Bounds do not guarantee real clock time or RSS.

## 2. Independent complete derivations

### L1. High-modulus complement equivalence — **PROVED, human proof**

A nonempty subset of distinct indices `[1..n]` has positive sum `s<=U`. If `m>U/2` and `m|s`, then `s=tm` for some positive integer t, but `2m>U>=s`, so `t=1` and `s=m`. Its complement `O=[1..n]\\I` therefore has sum `U-m=h`. Every element of O is positive and <=h, hence O subset of `[1..q]`. Conversely a subset of `[1..q]` summing to h has complement of sum `U-h=m`. Convexity is an **additional** constraint, and the empty subsequence is always allowed. This proves a bijection between *nonempty modular candidates* and omission subsets with sum h; no claim that every candidate is convex.

Special cases: h=0 gives O=empty and the unique nonempty modular candidate is the full sequence; q=0 automatically. q=n means the suffix below is empty. A missing exact-sum omission partition means there is no nonempty modular candidate, not an unsupported assumption of all-subsequence infeasibility.

### L2. Fixed-suffix triple locality — **PROVED, human proof**

Since O subset `[1..q]`, every candidate contains all indices `q+1,...,n`. Partition its consecutive selected triples by the final selected index k. If `k>=q+3`, the preceding two selected indices must be `k-2,k-1`: all three are in the **uninterrupted present suffix**; the necessary-and-sufficient inequality is precisely `a_k-a_{k-1}>a_{k-1}-a_{k-2}`. These fixed suffix tests can be performed once for all candidates. If `k<=q+2`, all three selected indices lie within `[1,min(n,q+2)]`, and the triple occurs, in the same adjacency order, in the selected restriction to that prefix. Therefore the conjunction of (a) all ordinary triples for k=q+3..n and (b) all consecutive selected triples in that restricted prefix is **equivalent to the full convexity predicate**. The boundary at q+2 is essential: a crossing triple ending at q+1 or q+2 can contain an omitted-prefix gap. When `q>=n`, the first class is empty; when `q=0`, the prefix contains at most two indices and all triples are fixed suffix triples.

Thus suffix test costs O(n) once; an individual candidate is checked with at most `q+2` prefix indices, O(q+1) comparisons. It is an **application-specific locality lemma**, not evidence of global research priority.

### L3. Reachability table — **PROVED, human proof**

Define R[t,s] iff there exists `O subseteq [1..t]` with sum(O)=s, for `0<=t<=q`, `0<=s<=h`. The base R[0,0]=true and R[0,s>0]=false holds because the empty subset is unique. For t>=1, every subset either excludes t, yielding R[t-1,s], or includes t, yielding R[t-1,s-t] if s>=t. Conversely either predecessor yields a valid witness in [1..t]. Induction on t proves the recurrence exactly. `q+1` bytearray rows of length `h+1` require O(qh+q+h+1) bytes in general; **for q>=1, h>=1**, O(qh) because h<=qh. For q=0, h=0, O(1). Hence for the canonical valid regime the bound is O(qh+1) bytes plus O(q) row objects, and O(qh+1) writes/reads.

### L4. Complete, unique, reachable DFS with output charge — **PROVED, human proof**

From state (q,h), recurse on (t-1,s) only if R[t-1,s] is true and on (t-1,s-t) only if s>=t and R[t-1,s-t] is true; the latter sets omitted[t]=true, later undone. The table invariant ensures every descended state has a completion, and every exact-sum subset yields a unique length-q sequence of include/exclude decisions. No duplicate leaf is generated, and each reachable completion must follow one of the two branches at every t, so none are missed. At a leaf (0,0), exactly one omission subset has been constructed.

If D=D_q(h)>0, assign every visited **entry** node to any complete descendant. Each leaf can be charged at most q+1 ancestors, hence at most `(q+1)D` entry nodes. The implementation's constant number of phase/undo frames per entry preserves O(qD) total stack events. Each leaf computes its selected local prefix, omitted count, comparison and possibly best-descriptor copy in O(q+1) word operations. Maximum stack depth is O(q) even with explicit phase frames; best omission and prefix descriptors use O(q). If D=0, R[q,h] is false and DFS is not entered. This proves the complete enumeration cost O(qD+1).

**Prior-art caution:** Generic reachability-DP-guided subset enumeration and this kind of output charging predate MOCOSO; G2 validates the *proof*, not its novelty.

### L5. Exact optimum and global lex tuple — **PROVED, human proof**

By L1 every nonempty modular candidate corresponds to exactly one leaf; by L2 the suffix+local test accepts **precisely** its convex candidates. The winner is the candidate with maximal `n-|O|`, ties broken by lexicographically least selected local prefix. Every feasible candidate has the identical fixed suffix of selected indices `[q+1,...,n]`; any two equal-total-length candidates therefore have equal-length local selected prefixes (after intersecting with `[1,min(n,q+2)]`). If their prefixes differ, the first differing index occurs there and decides the full tuple's lex order; if prefixes agree, both omissions are identical, hence the complete tuples agree. Thus prefix comparison is exact full-tuple lex comparison. If no nonempty modular candidate passes L2, the empty tuple is the unique length-zero optimum. Every leaf is considered; the procedure returns the exact optimal length and lex-smallest complete witness.

### L6. Threshold and partial certificates — **PROVED for returned values under stated execution assumptions**

Let true OPT be maximum length. Any *returned* candidate witness is checked by L2 (or is empty), so `lower_bound=len(indices)<=OPT`. During incomplete enumeration, setting `upper_bound=n` is trivially sound. If a suffix fixed triple fails, L2 proves there is no nonempty candidate, hence `upper_bound=0` is sound. If R[q,h] is false, L3 proves there is no nonempty modular candidate, also upper 0. After complete enumeration, L4–L5 prove `upper_bound=best_len=OPT`. `FEASIBLE` is returned only with a witness length>=K; `INFEASIBLE` for K>n, for a suffix/reachability impossibility, or after exhaustive search with OPT<K. `K<=0` is satisfied by the empty solution. Thus no `INFEASIBLE` is inferred from a resource budget.

**Qualified software guarantee:** This is an invariant for *successfully returned* result objects. A real `MemoryError`/overflow or abrupt external termination can occur **inside result reconstruction**; the catch handler calls result reconstruction again, which may fail under exhausted memory. Consequently the implementation **does not guarantee that every actual OOM event yields a result object**. `max_seconds` and `max_heap_bytes` are cooperative checks, not preemptive time/RSS ceilings; `max_operations` measures only selected loop events. Do not claim unconditional crash-free certificate delivery or hard resource enforcement.

### L7. Asymptotic counts — **PROVED under explicit model, NOT an unconditional Python bound**

Work is (1) O(n) fixed suffix scan, (2) O(qh+1) reachable table construction including bytearray copying, (3) O(qD+1) DFS+candidate-local evaluation, (4) O(n) final reconstruction. Total
`O(n+qh+q D_q(h)) <= O(n+qh+q P_d(h))`
unit-cost **wide-word** operations. Auxiliary storage: O(qh+q+1) word-equivalent units/byte cells for table, phase stack and descriptors, excluding existing input and final returned sequence; because `n>=2` the additive constant is absorbed. If `h>=1`, `q<=h`, so O(n+h²+hP_d(h)).

For the classical `P_d(h)` upper bound, let `F(z)=prod_{j>=1}(1+z^j)=sum_{t>=0} P_d(t) z^t`. For `x>0`, nonnegative coefficients give `P_d(h)e^{-xh} <= F(e^{-x})`. Taking logarithms: `log F(e^{-x}) <= sum_{j>=1}e^{-xj} = 1/(e^x-1) <=1/x`. Consequently `P_d(h) <= e^{xh+1/x}`; optimizing with `x=h^{-1/2}` for `h>0` yields `P_d(h)<=e^{2 sqrt h}`. This **does not** prove a new generating function or new partition inequality.

**Necessary word-size caveat:** The problem allows arbitrary input integer bit-length B. The displayed unit-cost bound requires words wide enough for those integers and for indices/addresses. It is not valid as a uniform standard log-word RAM assertion without extra bit-operation factors. A safe generic conservative schoolbook-bit upper bound, with `W=max(2,B,ceil(log2((q+1)(h+1)+U+3)))`, is
`O((n + qh + qD_q(h) + 1) W²)` bit operations,
excluding input parsing and external interpreter overhead; all integer operations used are additions, comparisons, subtraction, bit/index accounting and array access on at most O(W)-bit quantities. The bound is deliberately conservative (many comparisons are O(W)). Auxiliary *bit* storage for the DP itself is O(qh) bits plus O(qW) for row/frame/descriptor/index metadata, **excluding** the read-only input, final witness and interpreter object overhead. This is a mathematical implementation model, not a measured CPython bit-time upper bound. In particular an O(qh)-byte table cannot be called O(qh)-bit **Python resident memory** without clarifying byte/bit factors and objects.

### L8. Unrestricted v0.2 baseline DP recurrence — **PROVED mathematically; software verification finite**

Define `F(i,j,r)` as maximum number of additional selected indices following the fixed pair i<j, additional **index** sum r mod m, with the strictly convex inequality for every adjacent triple; `F(i,j,0)>=0` due empty continuation, all other no-extension residues start unreachable. For each k>j with `a_k>2a_j-a_i`, append k to any optimal continuation from F(j,k,s) with `s=(r-k) mod m`. Every feasible nonempty continuation starts with precisely one such k; conversely any such child yields a valid continuation. By decreasing j, the child states are complete before their parents. For fixed j, sorting candidate successor k by decreasing a_k and predecessor i by increasing a_i makes the strict threshold `2a_j-a_i` nonincreasing; admissible successors only accumulate. Per-residue winner by maximum length then smallest first successor k is lex-canonical because the child state already chooses its own canonical suffix. Equal lengths with the same first pair thus inherit canonical children. Compare complete singleton/pair and first-pair derived solutions by maximum length, then lexicographically smallest full tuple. A candidate whose first two indices differ is ordered lex by that first pair; for identical first pair the child pointer was canonical. Hence abstract recurrence and sweep are exact under exact arithmetic and a fully evaluated state. **Important:** v0.2's soft limits/exception safety are separate software semantics; `edge_dp.py` is another finite-tested exact reference, not a formal proof assistant.

Resource counts for v0.2: O(n²m+n log n) word operations, O(n²m) table words plus O(n+m) scan state, conditional on full-word input arithmetic. When m>U, no nonempty solution; otherwise m<=U=O(n²), so polynomial-time in n, assuming uniform-word arithmetic. Python big-int bit costs and OS memory pressure require separate qualifications.

## 3. Adversarial execution and status

New *separately authored* `g2_independent_checks.py` uses complete selected-index subset enumeration and its **own** convexity predicate `a[i]+a[k]>2*a[j]` rather than T1's omission DFS or existing `modconvex.verify`. It checks sound threshold/certificate bounds, crossing triples and empty/boundary regimes. It adds a separate exact residue-index DP oracle for `a_i=3^{i-1}`. No current formal proof assistant (Lean/Coq/Isabelle) was run.

[GitHub Actions G2 run #40025669353](https://github.com/SaridakisStamatisChristos/MOCOSO/actions/runs/40025669353), **4/4 successful jobs**: Python 3.11 and 3.13 on both Ubuntu and native Windows. Per execution: 11,567 complete-subset oracle comparisons, 2,485 fixed-suffix locality predicate comparisons, 14,511 certificate checks, 25 analytic-family independent DP comparisons and 55 independently rechecked v0.2 cases. The script prints `G2_INDEPENDENT_SUMMARY` including git checkout ID and SHA256, and logs are uploaded by CI; counts are **per execution** (do not multiply as if unique independently sampled inputs). Script SHA256 `6a8c90d74b32c0b7ea5dec2dcaf1f2fb6181d0f13b115ef0a505f29ee96ac262`. Git checkout in the initial PR-run log is `fbd022c47474d940bc05fba56b51ae14c59b7792` (CI-generated PR test merge ref), while source-proof-byte freeze guards tie the code to the immutable original T1 head. Executed `unittest` 4 tests per matrix cell. No counterexample emerged **within these finite domains**. Logs are independent tests, not formal machine-checked general proofs.

## 4. Claim status — separate mathematics, software, and novelty

| Obligation | Mathematical abstract algorithm | Executable-source confidence | Formal verification | Priority |
|---|---|---|---|---|
| High-modulus complement & q-support | **PROVED** (L1) | Tested | NOT VERIFIED | elementary known |
| Immutable-suffix exact boundary | **PROVED** (L2) | Tested | NOT VERIFIED | G1 unresolved |
| Reachability & pruned enumeration | **PROVED** (L3–L4) | Tested | NOT VERIFIED | generic prior art |
| Max length + full lex tuple | **PROVED** (L5) | Finite independent oracle PASS | NOT VERIFIED | distinctiveness unresolved |
| YES/NO and interrupted-result bounds | **PROVED conditional on return** (L6) | Finite test PASS; catastrophic OOM recovery **NOT GUARANTEED** | NOT VERIFIED | not assessed here |
| Time/aux memory | **PROVED only in wide-word abstract model** (L7) | Concrete Python big integers, wall time and RSS **not** established by word count | NOT VERIFIED | G1 undermines novelty |
| v0.2 backward exact recurrence | **PROVED abstractly** (L8) | historical CI + partial independent G2 checks; **not** end-to-end formal equivalence | NOT VERIFIED | prior-method overlap |
| Research readiness / first / best | **NOT G2** | NOT G2 | NOT G2 | G1 REVISE, G6 pending |

**Gate verdict:** G2 mathematical T1 **PASS with mandatory scope qualifications**, assuming correct unit-cost wide-word model and successful execution; source-level finite falsification tests **PASS** but software is **not formally verified**; hard resource-cap or unconditional OOM-certificate guarantees are **NOT VERIFIED/NOT PROMISED**. Do **not** permit a broader claim in a paper. G1 found prior-art overlap; thus passing G2 alone does **not** qualify MOCOSO for publication. G3 is justified as conditional contribution-strengthening work and G4–G6 remain gated.

## 5. Exact permitted statement for future internal research

> In the regime U/2 < m <= U, letting h=U-m and q=min(n,h), the deficit-based algorithm exhaustively evaluates the feasible omission sets using a standard subset-sum reachability DP, checks the strict convexity condition by a fixed-suffix/local-prefix decomposition, and returns a maximum-length, globally lexicographically least feasible selected-index tuple. On a RAM with constant-time arithmetic for all involved integers and enough word width to address the DP, its unrestricted successful computation uses O(n+qh+qD_q(h)) operations and O(qh+q) auxiliary words excluding input and final output. For h>0, D_q(h)<=P_d(h)<=exp(2 sqrt h). Arbitrary-precision integer bit costs, actual Python resident memory, interrupted execution and research novelty are separate questions.

This is internal proof-audit wording, **not formal manuscript text** and not a first-in-literature or peer-review assertion.
