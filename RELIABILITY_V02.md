# MOCOSO v0.2 reliability and memory engineering

This document records engineering decisions; the original research artifacts,
proofs, JSON benchmark records, logs and checksum manifest are preserved
unchanged. In particular, the old measurements describe the original code,
not v0.2. No asymptotic improvement is claimed.

## Hard invariants

- Same exact recurrence and strict inequality as `RESEARCH_REPORT.md`.
- Lexicographic optimum for `K=None`, valid early witness for threshold YES.
- Never return `INFEASIBLE` because of resource exhaustion.
- On `RESOURCE_LIMIT`, `indices` is a valid certified lower-bound witness,
  while `upper_bound` is a sound proved upper bound.
- No arbitrary maximum n or m in the unrestricted exact API.

## Table packing

Let `N=n(n-1)/2` and `Q=N*m`. The original main algorithm allocated
two signed `array('i')` tables with payload `8Q` bytes on common platforms.
The revised implementation chooses the smallest standard-library C integer
array whose representable range safely contains each table's values:

| n | Continuation lengths | Successor index | Common payload |
|---|---|---|---|
| 0 ... 32767 | signed `h` | unsigned `H` | `4Q` bytes |
| 32768 ... 65535 | signed `i` | unsigned `H` | `6Q` bytes |
| 65536 ... 2147483647 | signed `i` | unsigned `I` | `8Q` bytes |
| larger n | signed `q` when needed | unsigned `I` or `Q` | platform dependent |

For a pair `(i,j)`, the continuation length lies in `{-1,0,...,n-2}`;
an unsigned successor index lies in `[0,n]`. Thus each selected array
contains every possible value without overflow under the stated thresholds.
The `-1` unreachable sentinel and `0` no-successor sentinel are unchanged.
The recurrence, choice comparison, offset calculation and pointer reconstruction
are untouched. Packing changes no operation count or asymptotic bound.

`dense_dp_payload_bytes(n,m)` computes the two-table payload on the running
Python platform. It is a *necessary* memory allocation budget, not a
process-RSS prediction or an upper bound on peak memory. Arrays, sorting,
Python lists, objects, temporary allocations and allocator fragmentation
add overhead. `max_heap_bytes` remains cooperative *tracemalloc-traced*
memory, not a hard memory cap.

## Budget handling

Preprocessing (validation, sort, distinct-value computation, index-only upper
bound, singleton/pair scans) previously could finish substantial work without
time/heap checks. The revised solver checks budgets before and after sorting,
after bound computation, and periodically through constant-value, singleton
and pair scans. Returns during partially completed preprocessing use the valid
coarse upper bound `n`, then the tighter bound only after its proof computation
finishes. Feasible certificates are formed only from complete, validated states.

`max_operations` continues to count residue-slot transitions and
complement-enumeration masks as in v0.1; it is **not** an instruction,
sort-comparison, pair-preprocessing or wall-clock budget. `max_seconds` and
`max_heap_bytes` are *soft cooperative limits*. Python's built-in sort, a
single very-large-integer arithmetic operation, input validation and array
initialization cannot be preempted safely in-process. Hard limits require
an external process/OS supervisor and may terminate the process without a
recoverable `Result`.

Budget validation rejects NaN, infinities, booleans and nonnumeric inputs.
Operation and heap byte budgets must be nonnegative integers; the soft time
budget accepts finite nonnegative integers or floats (including fractions).
An omitted budget (`None`) remains unbounded.

`K>n`, `m>U` and `K<=0` remain logically proved shortcuts and need not
be rejected just because the requested budget is zero. Resource checks can
return `RESOURCE_LIMIT` instead of a proven result when the soft budget is
already exceeded; this does not assert nonexistence.

## Alternatives investigated and rejected

1. **Sparse dict residue states**: many valid families saturate most residues,
   and Python dictionary entries substantially increase per-state memory.
   No worst-case or measured crossover advantage has been shown here. It
   would change the recurrence implementation and needs its own differential
   campaign. Therefore do not route production calls to it.
2. **Automatic edge-DP selection**: `edge_dp.py` uses only `O(nm)` state
   entries but materializes and sorts `Theta(n^2)` arbitrary-precision
   edge differences and stores n-bit lex masks. Benchmark results are mixed.
   Its API also lacks interrupted-result / resource-budget semantics.
   Making it an unverified drop-in would weaken the API guarantee. Preserve
   it as an independent oracle, not a production switch.
3. **Length-only residue dominance**: mathematically false; see explicit
   counterexample in section 10 of the research report.
4. **Artificial input caps**: inconsistent with the unbounded exact API.
5. **Claims of lower asymptotic complexity**: not justified by packing.
   Word operations remain `O(n log n+n^2 m)` and memory remains `O(n^2 m)`.
   The original polynomial and parameterized feasibility proofs still apply.

## Verification and measurements

The CI matrix runs Python 3.10–3.13, compiles the modules, executes
`research_tests.py`, `edge_trials.py`, `extra_trials.py`, and the
independent `unittest` adversarial regression suite. These test scripts
exercise signed/huge integers, duplicates, lex ties, large moduli, shortcuts,
witness validity, memory estimates, bounded interruptions, and original
oracle comparisons.

`benchmarks/compare_v02.py` loads original main-branch and candidate solver
as distinct modules and runs paired, deterministic cases. CI pins its original
main-branch comparison checkout to the PR's immutable base commit
`e8c5f0461beaf975ab7acaa1e35ced9f2d09a276`. The artifact records SHA-256 checksums
and resolved Git revisions for both solver sources, and rejects baseline drift
when `MOCOSO_BASELINE_SHA` supplies the expected commit. CI uploads the
`v02_comparison.json` measurements. Results are traced-heap peaks and
*instrumented* times; `tracemalloc` overhead is included and this is not a
controlled hardware performance superiority claim. Complement shortcut rows
may not allocate a dense table, so their notional payload is *not* observed
memory.

For independent reproduction:

```bash
python -m unittest discover -s tests -p 'test_*.py' -v
python research_tests.py
python edge_trials.py
python extra_trials.py
# from the branch root with the main branch checked out at baseline_original:
python benchmarks/compare_v02.py baseline_original/modconvex.py modconvex.py
```

The old benchmark JSON and manifest belong to the original snapshot and
must not be rewritten by the feature PR. Existing scripts overwrite their
report outputs *locally*, so CI runs them in ephemeral checkouts only.

## Residual risks

- `tracemalloc` does not measure all process memory, and soft limits can overshoot.
- The original backward recurrence remains bounded by `Theta(n^2m)` states.
- Large Python integers can dominate sorting and arithmetic time.
- CI compares finite cases and does not constitute a machine-checked proof.
- No production use of the edge solver has been enabled.
