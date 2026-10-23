# MOCOSO v0.3 evidence/claim ledger

Baseline: v0.2 main 9cedac0d0f860564d5ee1a9064b01ef56ac2a764. Status date 2026-10-23. Gate evidence must be updated when CI or independent review completes.

| Claim | Status | Evidence | Required next gate |
|---|---|---|---|
| v0.2 baseline preserved on separate research branch | SUPPORTED | GitHub branch created from exact merged main SHA; additions only | Confirm GitHub PR diff |
| Index-sum complement when m>U/2 | SUPPORTED derivation | Proposition 1 in t1_deficit_proof.md | Independent proof reader |
| Immutable suffix locality | SUPPORTED derivation | Proposition 2 and exhaustive test code | Independent proof reader |
| O(n+qh+qP_d(h)) arithmetic-word time, O(qh+q) auxiliary words | PARTIAL | Proof draft and prototype; modeling caveats explicit | Independent complexity review; memory measurement |
| P_d(h)<=exp(2 sqrt h) | SUPPORTED derivation | Classical generating-function inequality | Independent proof reader; credit classical literature |
| Exact lex optimum and threshold decisions | PARTIAL | Brute-force differential code; local run: 41,085 exhaustive instances and 250 seeded cases | GitHub CI and independent auditor |
| Best v0.3 runtime or memory vs v0.2 | UNRESOLVED | Reproducible benchmark harness, no trusted cross-environment data yet | Raw comparative runs and second environment |
| T1 is genuinely novel in literature | UNRESOLVED | Bounded search, no comprehensive citation traversal | Finish M0 |
| T2 lower-bit-memory exact edge DP | UNRESOLVED | Only investigation outline; tuple comparator is **not** the solution | Derive algorithm/proof or document failure |
| T3 nontrivial structural result | UNRESOLVED | Not yet proved | Rigorous statement with counterexample search |
| Publishability / SOTA / priority | UNRESOLVED | No independent prior-art plus proof review | M0-M6 |

Strict reading: local finite testing does not establish a theorem's novelty, CI green does not establish proof, and smaller prototype code does not establish asymptotic space. Current campaign disposition: **research in progress; no GO for a scholarly originality claim**.
