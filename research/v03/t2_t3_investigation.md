# T2 / T3 design record — open, not a proved algorithm

Date: 2026-10-23. Baseline edge_dp.py uses 1 bit per selected index in integer lex witnesses at each row/residue state. The table has O(nm) states, but each stored bitmask may need n bits; abstract state count is not a complete bit-space bound.

## T2 candidates (not yet verified)

(1) Immutable/persistent predecessor chains: store a path-node for every accepted improvement, never a pointer into an evolving mutable row; such a mutable pointer may retroactively change the represented old prefix and invalidate increasing-edge order. Naively materializing a persistent node at every improvement could consume O(n^2m) nodes, which defeats the intended memory advantage. Need a proof of update counts, garbage collection/reachability or recomputation tradeoff.

(2) Lexicographic path comparison without full masks: canonical persistent paths with exact LCP/first-divergence queries, or rank identifiers scoped to equal-length sequences, potentially support fast lex comparisons. Hash-only fingerprints without collision proof are unacceptable for exactness. Rank maintenance must be well-defined across differential edge groups and node revisions.

(3) Equal-edge-weight staging must be retained: a strictly increasing-difference path cannot extend on an edge of *equal* difference. On-the-fly in-place state updates within a weight batch risk illegal sequences. Existing edge_dp.py stages each batch.

(4) Pure no-path-storage, trace-back with recomputation might trade time for space, but only a fully specified exact algorithm with a real improved bound counts as T2. O(nm) mutable state alone does not guarantee valid lex witness reconstruction.

Unresolved proof obligations: path identity and durability, exact lex comparison, update bound, memory reclamation/reconstruction, index-sum residues, equal-weight groups, arbitrary signed integer sorting cost, and failure/resource semantics. The tuple adapter in baselines.py is an exact correctness reference, NOT a solved asymptotic T2 improvement. No T2 theorem is claimed.

## T3 search targets

Restricted input value classes; bounded number d of distinct values; feasible-length structural bounds; modular accessibility; lower-bound/counterexample statements. The constant-value shortcut is already present in v0.2 and is not publishable novelty. Since the unrestricted optimization problem is polynomial, 'FPT in K' without stronger algorithmic information is not a contribution.

Disposition: continue exploratory tests only after T1 verification and prior-art scan. If no genuine new bound survives, release a reproducible technical report, not an algorithmic-priority claim.
