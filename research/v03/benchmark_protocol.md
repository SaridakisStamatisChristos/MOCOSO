# v0.3 comparator, execution and evidence protocol

Initial registration: 2026-10-23, before any GitHub CI comparative result. Baseline SHA is 9cedac0d0f860564d5ee1a9064b01ef56ac2a764.

## Comparable semantics

All tested methods must use: signed unbounded integer A[1..n], 1-based *index* sum modulo m, strict convexity A[k]-A[j] > A[j]-A[i], maximum length, and globally lex-smallest index tuple among length maximizers. No approximate/relaxed answers are comparable. Full v0.2 solve() returns OPTIMAL; research adapters return tuples; the harness normalizes to tuples.

Competitors:
- modconvex.solve with complement_cutoff=20: original v0.2 public API. Has preprocessing, shortcuts, optional dense fallback.
- experiments/v03/baselines.py solve_mask: isolated faithful scan of all 2^q masks from the v0.2 complement method. Does NOT include v0.2's preprocessing; mechanism-only cost comparison.
- experiments/v03/deficit.py solve_deficit: proposed partition enumerator plus immutable-suffix filtering.
- edge_dp.solve_edge: independent existing exact sorted-edge/bitmask witness baseline.
- solve_edge_tuple: independently written modular/lex augmented Kluev edge sweep; not the original unconstrained Kluev algorithm. This adapter stages equal-weight edges and retains O(nm) states of potentially O(n)-length tuples.
- modconvex.cubic_dp and an independently coded brute-force all-subsets oracle in tests for small inputs. Cubic and exhaustive implementations are correctness controls, not large-scale speed comparators.

## Registered benchmark grid and scope

**Original preregistered grid:** n,h,family: (12,3,convex), (12,8,alternating), (20,7,convex), (20,12,alternating), (20,8,equal), (20,10,huge-signed), (35,5,convex), (35,12,alternating). **Post-hoc coverage repair (added after seeing initial raw CI output):** (12,8,superconvex), (20,12,superconvex), (35,12,superconvex), (20,24,superconvex), (35,40,superconvex). Here superconvex means A[i]=3**i (0-based Python indexing), guaranteeing every subsequence is strictly convex. This repairs the initial workload's overrepresentation of empty optima and deliberately includes h>n. Report the two sets separately; do NOT mislabel the added cases preregistered. For each, m=U-h and U/2<m<=U. Tuple edge comparator is restricted to n<=20, and the 2^q isolated mask comparator to q<=12, for bounded cost. Report omitted cells explicitly.

Command from repository root:

    python experiments/v03/benchmark.py --output v03_raw.json --repetitions 5 --seed 20261023

Benchmark executes each algorithm in a new Python subprocess with one warmup, five timed runs, and one separately tracemalloc-instrumented run. Algorithm order is seeded/randomized. Timing uses perf_counter_ns, excludes interpreter/subprocess startup but includes reconstruction. Per-child peak Linux RSS (KiB) includes module imports and warmup and should not be described as precise DP payload. The `resource` module is optional: on Windows (or whenever it cannot be imported), `peak_rss_kib_linux` is `null`. Runtime and traced-heap measurements remain available; a null RSS observation is not zero consumption. The missing-module path is tested with a simulated import failure, not with a native Windows CI runner. Traced Python heap peak (bytes) is distinct from RSS; neither implements a hard external memory limit. Algorithm-specific counters are different metrics; they must not be directly compared as 'same operations'.

Stored JSON must include every raw timing repetition, minimum, maximum, median, peak RSS, traced peak, n,m,h,family, witness, operation counts where defined, seed, interpreter, OS, processor, CPU count, branch commit (if available), baseline commit and SHA256 of imported source files. Runtime spread is observable from raw runs. The harness checks exact witness agreement and uses all-subset oracle on n<=12. For n>12 it checks all algorithms against the first computed output, but independent tests separately use all-subset oracle on small instances. Always report which results had independent oracle support.

## Gates and limits

Re-run on a second machine/software configuration before any cross-environment performance or 'fastest' claim. Randomized ordering is across algorithms/cases; Python allocator and CPU noise still remain. Timings do not prove an asymptotic theorem. Omitted work not included in comparator cost must be explicitly disclosed. Research prototypes should not auto-route production users, nor circumvent resource-limit contracts. A sample report is not committed until it is actually generated and source hashes are checked.

## Cross-environment reproduction (Windows and Ubuntu)

The GitHub research workflow runs the **same existing 13 cases, algorithms, seed
20261023, and three timed repetitions** on `ubuntu-latest` and `windows-latest`
with Python 3.13. The new Windows job executes the exhaustive research tests
natively before running the full subprocess-isolated benchmark. Its artifact
`v03-raw-benchmark-windows` contains `v03_windows_raw.json` and
`v03_hardware_windows.txt`; the Ubuntu artifact remains `v03-raw-benchmark`.
The source hashes and runtime/OS fields are embedded in each raw JSON.
`peak_rss_kib_linux` is intentionally null on Windows; compare traced Python
allocations separately and never interpret null as zero memory usage.

For performance comparisons, pair the **same (n, h, family, algorithm)** on each
runner and calculate an **intra-runner** baseline/T1 timing ratio. Then compare
the directions and distributions of those ratios across OS/runner environments.
Absolute milliseconds from different CPUs/hosts must not be used to assert
an OS-dependent algorithmic speedup. GitHub-hosted runners can vary in hardware
and background load; this adds a second environment, not controlled replication
on identical hardware. The five disclosed post-hoc superconvex workloads remain
post-hoc, not reclassified as preregistered.
