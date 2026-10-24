# G8 adversarial evidence and failed hypotheses

Date: 2026-10-24. Independent proof/refutation roles: Theorem Foundry, Algorithm Foundry and SOTA Research Auditor. This ledger separates local executed prototypes from subsequently committed CI.

## Executed prototype evidence

A Linux CPython 3.13.5 local experiment compared the sparse-gap immutable-interval prototype against an independently programmed distinct-index omission-partition enumerator (not G3 or a sorted-event DP), checking the **entire selected tuple**. All 21,321 cases from the n=2..7 ternary input grid and admissible h<n passed. Another 1,500 seeded giant-signed cases passed (seed 22102407, 2<=n<=100, h<=16, input alphabet {-10^90,-17,-2,0,1,9,10^90}). The original G7 transcription matched the same oracle. All 160 edge-count comparisons h=0..159 using gap-length counting versus direct pair enumeration passed. The focused lex tie (-3,-3,-3,-3,-2,0), m=16 yielded selected (1,4,5,6). Equal-difference control (0,1,2), m=6 correctly yielded empty.

**Important:** Those executions ran on ephemeral local transcriptions. For independently rerunnable *committed source* evidence see tests/test_v03_g7_independent_partition.py and tests/test_v03_g8_persistent_intervals.py plus .github/workflows/v03-g8-sparse-gap.yml. GitHub CI status must be retrieved at the new final head before claiming a verified commit.

## Claims attacked

| Claim or shortcut | Result |
|---|---|
| Every one of p^2 candidate edges requires h resource scans | REFUTED as tight analysis: nonadjacent overbudget gaps are impossible; proved O(H log(h+2)) eligible edge bound. Older G7 loose bound remains mathematically valid |
| Break inner loop after weight exceeds h | PROVED: nondecreasing gap weight in destination; compulsory-skipping illegality also monotone |
| Same-difference edges can update from same-difference prefixes | REFUTED by (0,1,2), m=6; descending destination order is mandatory |
| Lex smallest omitted tuple means lex smallest selected tuple | REFUTED by (-3,-3,-3,-3,-2,0), m=16; select (1,4,5,6) by omitting (2,3), lex larger than (1,4) |
| Unversioned mutable predecessor pointers reconstruct history | REJECTED as unjustified because predecessor states may change after an outgoing event. No claim of a minimized MOCOSO mutable-pointer counterexample |
| Each skipped index must be allocated in a separate persistent node | REFUTED: one interval node encodes all skipped indices of a positive gap |
| O(H^2 log H) allocated nodes imply O(H^2) auxiliary words | REFUTED mathematically: the log factor is unbounded. Primary full-lex cubic/quadratic target remains OPEN |
| One arbitrarily large bitmask or exact rank is a fixed-cost word | REFUTED as model error. G8 uses explicit O(1)-word interval nodes and honest enumeration on ties |
| Universal Hirschberg automatically gives cubic/quadratic | UNPROVED: event-DAG locality, canonical semiring and precise cubic-time mapping still missing |
| Passing finite oracle tests proves asymptotic or global novelty | REJECTED. Tests falsify examples; the independent human proof supplies asymptotics and bounded source review cannot prove worldwide firstness |

## Gate separation

- Mathematical correctness: human proof available, external referee or formal checker absent.
- Algorithmic implementation exactness: local prototype comparisons successful; verify new GitHub CI for committed source.
- Algorithmic novelty: improved *repository-specific* complexity pair, but apparently composed of known primitives.
- Literature priority: no exhaustive forward/backward search; unresolved.
- Scientific significance: independent general breakthrough not demonstrated; paper drafting HOLD.
