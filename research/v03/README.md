# G9 research and manuscript

The current result is the exact canonical-witness theorem for the high-modulus
regime `U/2 < m <= U`, `h = U - m < n`, where `U = n(n+1)/2`.
The corrected algorithm returns the globally lexicographically least entire
maximum-cardinality witness in `O(n + (h+1)^(5/2) log²(h+2))` wide-word operations
using `O((h+1)²)` auxiliary wide words, excluding the input and one returned output.
The paper specifies the arithmetic model and boundary cases.

## Start here

- [Revised manuscript](g9_paper/manuscript.md), [PDF](g9_paper/exports/manuscript.pdf),
  [Word](g9_paper/exports/manuscript.docx), and [LaTeX](g9_paper/exports/manuscript.tex).
- [Corrected G9 implementation](g9_independent_audit/solver_corrected.py).
- [Independent audit and five separate verdicts](g9_independent_audit/AUDIT_REPORT.md).
- [Prior-art investigation](g9_priority/PRIOR_ART_REPORT.md) and
  [documented search log](g9_priority/SEARCH_LOG.md).
- [Original G9 implementation](../../experiments/v03/g9_quadratic_lex.py) and
  [original theorem development](g9/G9_THEOREM_LAB.md), preserved as historical artifacts.

The original implementation allocates output-sized tuple slices in its final
validation. Use the corrected derivative for the claimed auxiliary-space bound.
The production solver and its dispatch remain unchanged.

## Contribution and evidence

No earlier statement of the same complete specialized theorem was identified in
the documented source-specific search. Its general techniques have established
precedents. The supported contribution is an incremental specialized theorem,
with complete canonical reconstruction and explicit resource accounting; an
unqualified worldwide-first claim is not established.

Historical G0–G9 reports retain their original dates, verdicts, and failed
hypotheses. Earlier instructions to hold merging or paper drafting record the
state at those stages; the later audit, prior-art report, and revised manuscript
provide the current research assessment. Repository integration is separate from
journal acceptance or submission.

## Integration verification

The integration preserves the full research commit ancestry and all original
G3–G9 implementations. Three workflow corrections address observed failures:

- The G6 preservation check compares every file present in its frozen baseline,
  allowing later additions while still rejecting modification or deletion of
  historical files.
- Each G5 replay archives to a run-and-attempt-specific branch, avoiding the
  observed non-fast-forward rejection and preserving the original evidence ref.
- The G9 audit preservation check protects the frozen solvers, tests, and
  research evidence while permitting root navigation and CI maintenance.

Reproduce the solver tests with `python -m unittest discover -s tests -p 'test_*.py' -v`.
See [audit reproduction](g9_independent_audit/REPRODUCE.md) and
[manuscript build QA](g9_paper/BUILD_QA.md) for the separate evidence scopes.
