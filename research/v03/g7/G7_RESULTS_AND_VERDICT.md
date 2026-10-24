# G7.4 result and paper-readiness decision

**G7 research verdict: VALIDATED BUT COMPOSITIONAL SPECIALIZATION.**
This refers to the explicit-omission witness Pareto theorem below, not to a claimed world-original algorithm primitive. **The primary cubic-time/quadratic-space full-lex target remains UNSOLVED.**

## Claim–evidence gates

| Claim | State | Evidence and caveat |
|---|---|---|
| Original G3 full-lex high-modulus cubic/cubic wide-word bound | Prior human proof; frozen | \`research/v03/prepaper/g3_polynomial_deficit_theorem.md\` @ \`53b2276c7ed450ba8c27adc0e1e02c1493b4e592\` |
| G7-P exact full-lex O(n+h^(7/2)) time/O(h^(5/2)) auxiliary wide words for h<n | **Human proof + local adversarial validation** | \`G7_THEOREM_LAB.md\`; \`experiments/v03/g7_compact_lex.py\`; \`tests/test_v03_g7_compact_lex.py\`. Polynomial exponents formally use h+1. |
| Exact original G7 objective, including global lex, empty fallback, compulsory suffix | **Supported** | Invariant induction, selected subset brute force, signed random and fixed crossing adversaries |
| Primary stronger target O(n+h^3) time/O(h²) words full lex | **OPEN / NOT CLAIMED** | No safe canonical-pointer versioning/compact reconstruction proof, R1–R3 |
| Literature nonduplication for exact specialized theorem | **UNRESOLVED** | Original-publication implication matrix; no inspected verbatim predecessor but mechanisms known |
| Independent scientific importance / competitive SOTA performance | **UNRESOLVED** | No optimised equivalent-semantics full benchmark / no rigorous uniqueness in prior literature |
| Local standalone repeatability | **Supported within recorded corpus** | 21,321 +145,632 exhaustive signed-grid cases, 1,000 seeded giant signed cases and focused adversaries; Linux CPython 3.13.5. GitHub matrix to be checked separately |
| Formal mechanized proof | **NOT DONE** | No proof assistant invoked |
| Theory manuscript readiness | **HOLD / NO-GO for originality-driven theory submission** | Results are compositional; distinct theoretical significance unresolved; user explicitly forbids writing paper |

## Why the result is useful but not an automatic paper

G7 improves the previous *known tradeoff frontier* within MOCOSO's investigated research implementations: G3 cubic-time/cubic-space full lex and PR #11 quartic-time/quadratic-space full lex admit a middle time O(h^3.5) / space O(h^2.5) full-lex point. The proof depends on the structure of a distinct-index omission sum and charges each omission entry. It is a constructive exact algorithm and directly falsifiable, but an interpolation of known techniques, **not a fundamentally novel paradigm or a complexity-class lower bound**. No superiority over every published approach is asserted.

## Next mathematically meaningful bottleneck

Seek O(n+(h+1)^3) time / O((h+1)^2) wide-word auxiliary memory with exact full lex, ideally by a proved canonical ranking/traceback mechanism that fits the O(p(h+1)) sorted-event frontier. Audit the 2025 width-bounded Hirschberg work against the actual event graph's frontier size and tie semantics before claiming transfer. Preserve exact omission resource, q+2 crossing triples, and original G3 proof. For any failed avenue record a minimized counterexample instead of repairing claims silently.

**Git policy:** standalone research-only G7 branch stacked on unmerged PR #12. No production rewrite, no merge, no manuscript preparation or submission. Existing G6 judgments are not erased; the only change is an additional verified compositional Pareto bound.


## Post-PR13 independent audit handoff, 2026-10-24

Run [40083406635](https://github.com/SaridakisStamatisChristos/MOCOSO/actions/runs/40083406635), at original PR #13 SHA \`e8ff4846968699488a3cba6f995dbbb19a038be3\`, has completed **4/4 SUCCESS**. The original table's sentence "GitHub matrix to be checked separately" concerns the historical at-authoring-time status, not the now-verified frozen run. This is not evidence for G8 commits until their own CI passes.

The G7 review's independently constructed *omission partition* oracle is now test code under \`tests/test_v03_g7_independent_partition.py\` with seed, finite scope and intended test command recorded in the adversarial ledger. Theorem proof event-threshold quantifier and a conservative bit-cost overlay are appended to \`G7_THEOREM_LAB.md\`. These are research-only documentary and test/CI changes; no production algorithm is changed.

The G7 bound itself remains a valid conservative upper bound, pending any strictly stronger G8 derivation. Priority/significance remain separate, unresolved publication gates.
