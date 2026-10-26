# RFP execution checkpoint — MOCOSO G9

Date: 2026-10-26. Frozen base: main merge commit bd22ddc05954af19aa2f57c6199c92817c232f54.

This change adds research files only; it does not rewrite production code, historical evidence, audited originals, or the existing paper. **No claim of SOTA, formal verification, human peer review, or world priority is made.**

## Gate 1 — Canonical corrected research implementation

- New entrypoint: experiments/v03/g9_corrected.py, an exact byte-for-byte copy of the audited research derivative research/v03/g9_independent_audit/solver_corrected.py at original Git blob 86a35229cb915427364a8d9820f5d54901482570. This is an **attributed correction**, not a new algorithm.
- Historical original: experiments/v03/g9_quadratic_lex.py, unchanged. It contains output-sized validation slices selected[1:] and selected[2:]; for h=0, H=h+1=1 and n arbitrarily large, these extra arrays cost Theta(n) references, refuting the original executable's advertised O(H²) *auxiliary* bound. Its mathematical DP and functional output are not refuted.
- Corrected emission: monotone omission cursor, indexed validation, no temporary output-sized tuple slices. Abstract space accounting remains conditional on the charged wide-word model, not ordinary Python process RSS.
- Public solve() dispatch: **not changed**. Comparative evidence is required before automatic routing.

## Gate 2 — Independent regression and reproducibility

The new tests/test_v03_g9_corrected_rfp.py exercises:

1. Small signed ternary-grid selected-subset oracle, independently enumerated, with full-tuple equality.
2. 300 seeded high-bit signed arrays against the pinned historical original.
3. Empty result, lexicographic tie, strict-equality, and suffix-boundary counterexamples.
4. Full output with 25,000 indices at h=0.
5. Static AST check prohibiting selected-output slices.
6. CPython tracemalloc original-versus-corrected h=0 allocation regression at n=12,000.

Executed in a CPython 3.13 source-subset workspace on 2026-10-26:

    PYTHONPATH=. python -m unittest discover -s tests -p 'test_v03_g9_corrected_rfp.py' -v

Result: **6 tests passed**. Execution classification: EXECUTED_LOCAL. These finite tests do not prove the general theorem, and the source-subset run is **not** full-repository CI. The new GitHub workflow runs the same six tests on Ubuntu and Windows, Python 3.11 and 3.13. Its status must be read from the *actual* commit; its mere existence is not VERIFIED_CI.

## Gate 3 — Registered crossover measurement

Run from the repository root:

    python benchmarks/g9_rfp_comparative.py --profile smoke --plan-only --output g9_rfp_plan.json
    python benchmarks/g9_rfp_comparative.py --profile smoke --repeats 3 --output g9_rfp_results.json
    python benchmarks/g9_rfp_comparative.py --profile ci --repeats 5 --output g9_rfp_ci_results.json
    python benchmarks/g9_rfp_comparative.py --profile paper --repeats 7 --output g9_rfp_paper_results.json

Four exact solvers: corrected G9, G8 persistent intervals, T1 deficit, and public default. Five input families: powers of four, quadratic, signed jitter, flat, and terminal broken suffix. Seed 20261026; small exhaustive oracle for n<=12; larger cases compare full canonical witnesses across solvers. End-to-end timing includes reconstruction; one warmup and individual nanosecond samples per method. Planned skips for public n>16 or h>12, and T1 h>19, are retained in raw JSON; speedup is always **matched baseline median / G9 median**, with case-level losses visible.

**Limitations:** the runner shares a process and host across methods; no hard deadline, RSS limit, distributional representativeness, independent external comparator, statistical significance, or causal algorithm superiority is established. Early infeasibility/constant-value workloads must remain in the output, not be removed opportunistically. GitHub's smoke workflow is designed to generate raw evidence, not certify practical SOTA. Production dispatch is postponed until paired results and an appropriate replication pass establish an actual advantage.

## Gate 4 — Stronger-theorem research hypotheses

These are questions, **not established G10 theorems**.

- **H1 (remove a logarithm).** Can the G9 quadratic-space score-extraction approach be reorganized to match G8's O(n+H^(5/2) log(h+2)) *time*, while retaining O(H²) *auxiliary wide words*? Possible independent routes: batching ordered prefix queries; sharing safe immutable event structures; alternative lex tracebacks. Each must account for event ordering, exact-resource masks, full lexicographic order, and output storage. No improvement has been proved or implemented.
- **H2 (extend the regime).** For h>=n the currently compulsory two-anchor suffix no longer follows. For m<=U/2 even the exact omitted-sum reduction may have multiple valid selected sums. The existing G9 argument must not be reused without a new reduction and proof.
- **H3 (lower bounds).** In the h=0 subcase, the all-selected witness is mandatory, so checking strict convexity of every consecutive triple takes Omega(n) input accesses in the worst case: starting with strictly convex values, altering an unobserved position can invalidate a neighboring triple without changing observed entries. This proves *only* a linear input-inspection lower bound, not Omega(H²) auxiliary space or general optimality.

Work on H1/H2/H3 is **PROPOSED/OPEN** and is not inserted into the paper as a discovery. A published identical specialized theorem was not found in the earlier bounded search; this is not worldwide novelty certification.

## Gate 5 — Prepared independent review request (not submitted)

Supply an algorithms referee with manuscript.md, the 2026-10-24 audit report, the priority source matrix, this checkpoint, and the complete benchmark JSON. Ask for a direct audit of (i) event-relative dominance with equal-difference ties, (ii) compulsory two-anchor suffix, (iii) monotone threshold oracle and entire-tuple order, (iv) output/temporary memory accounting, (v) prior art attributed to Kluev's 2013 answer and Björklund–Kaski–Kowalik's ESA 2014 witness extraction, and (vi) venue significance. No expert has been contacted and no paper submitted in this execution.

## RFP evidence ledger

| Claim | Status | Execution | Remaining action |
|---|---|---|---|
| Corrected source matches audited derivative | TESTED | Git blob equality and local copy | Check branch blob |
| Small-input canonical outputs | TESTED | EXECUTED_LOCAL, six-test suite | Confirm branch CI |
| Original G9 auxiliary O(H²) claim | REFUTED | h=0 counterfamily and regression | No remaining defect-discovery obligation |
| Corrected output avoids known linear slice | TESTED | EXECUTED_LOCAL, AST/tracemalloc | Abstract model is not an RSS guarantee |
| Four-way runtime ranking | SPECIFIED | NOT_EXECUTED until raw report exists | Run CI smoke and independently interpret |
| Improved asymptotic Pareto frontier | PROPOSED | NOT_EXECUTED | New algorithm and human-checkable proof |
| Exact literature priority and significance | PROPOSED | NOT_EXECUTED | Human referee and literature follow-up |

Preserve the historical original, its audit, and the existing paper. This checkpoint can be updated only with verified new evidence, not inferred future results.
