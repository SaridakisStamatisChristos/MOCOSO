# G9 falsification and execution ledger — 2026-10-24

## Independently executed local research prototypes

Linux CPython isolated workspace: candidate uses only scalar constrained DP and binary-search omitted-index reconstruction. Two independent reference methods: (1) direct selected-subset enumeration over 2^n masks, testing original modular sum and strict convexity of every selected triple; (2) recursive distinct omitted-index partition enumeration, forming whole selected complements and comparing exact full tuples. Neither oracle uses the G9 event DP.

- **21,321** exhaustive ternary signed grid cases n=2..7 and all legal h<n; compared exact full output against selected-subset oracle; PASS.
- **145,632** exhaustive signed four-valued grid cases n=2..7, same legal regime; compared exact full output against selected-subset oracle; PASS.
- **1,500** seed 22102407 giant signed cases, n=2..100 and h<=16, independently compared against omission-partition oracle; PASS.
- **4,000** additional seed 20261024 signed giant cases, n=2..110 and h<=17, independent omission-partition oracle; PASS.
- Strict/equal-difference counterexamples, true lex tie, large superconvex n=10000,h=4 and broken mandatory-suffix cases; PASS. Instrumented query counts conformed to the derived safe envelope. Large exponentials were NOT constant-bit-cost benchmark inputs.
- These counts were executed on *local prototype code*. The committed test suite explicitly recreates 21,321+145,632 selected-subset and 1,500 omission-partition cases, plus other checks; committed-source CI must be fetched independently before a CI verified label is awarded.

## Adversarial hypotheses

| Candidate hypothesis | Status |
|---|---|
| G8's persistent O(H² log H) allocations can simply be described as quadratic | **REFUTED as an implication**; no such stronger node count proved |
| Recompute dense O(H³) length oracle O(sqrt H log H) times | **INVALID target time**; must use G8 sparse-gap per-query O(H² log H) bound |
| Canonical paths must be retained in each DP state | **UNNECESSARY**, since scalar forced-score plus omitted decision self-reduction recovers them |
| Scanning all h inclusion/omission decisions one by one | **KNOWN baseline** in PR #11; adds O(h) queries and loses the stronger G9 time |
| Binary-search exact next omitted index based on equality x | **UNJUSTIFIED monotonicity**; use threshold >=x instead |
| Lex-smaller omitted tuples correspond to lex-smaller selected tuples | **REFUTED** by A=(-3,-3,-3,-3,-2,0), m=16: omitted (2,3) is lex-greater than omitted (1,4), but selected (1,4,5,6) is lex-smaller |
| Equal differences can safely feed one another | **REFUTED**: A=(0,1,2), m=6 returns empty |
| Endpoints only suffice for forced-select enforcement | **REJECTED**: forced selections in skipped intervals must be checked |
| Recheck O(n) fixed suffix each oracle call | **UNNECESSARY/WRONG complexity**: fixed suffix scanned once in O(n) |
| Full bitset or bigint exact rank stored in one fixed word | **REJECTED**: G9 stores only scalar counters and masks |
| Finite tests prove arbitrary n or scholarly originality | **FALSE**: separate proof and current priority audit gates |

## Preservation and rerun

Only new research, tests, and CI files are permitted under PR #14. Run committed test with: python -m unittest -v tests.test_v03_g9_quadratic_lex. The G9 workflow also compares pre-existing solver files to frozen PR #14 head and fingerprints runtime/source. No merge, production rewrite or paper draft.
