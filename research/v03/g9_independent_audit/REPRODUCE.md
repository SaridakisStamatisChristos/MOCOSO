# Reproduce the independent G9 audit

Use CPython 3.12 with assertions enabled; standard library only. Other Python
versions may work, but the committed local run used 3.12.14 on Linux x86_64.
No dependency installation or network is required for execution.

From the repository root:

```bash
python research/v03/g9_independent_audit/audit.py
python -m unittest tests.test_v03_g9_quadratic_lex -v
```

The first command regenerates `results.json`; redirect stdout to a new log if
you want to retain the original `run.log`. Timings, platform strings, and exact
allocation byte counts are environment-dependent. Case counts, expected tuples,
source blob identity, and mutation witnesses for the fixed seed are reproducible.
The script checks the pinned solver's Git blob before running and records SHA-256
hashes of itself, the original solver, and the corrected derivative in its output.

## Artifact map

- `AUDIT_REPORT.md`: five verdicts, independent proof, complexity accounting,
  defect family, experiment scopes, failed hypotheses, and repair qualification.
- `LITERATURE.md`: checked sources, exact loci, overlap/implication matrix,
  bounded search log, and originality limitations.
- `audit.py`: independent test harness and three separately written reference
  methods; no imports of upstream reference solvers.
- `solver_corrected.py`: attributed research-only G9 derivative. Core algorithm
  unchanged; streaming/indexed validation and deterministic output cursor.
- `results.json`: final executed audit data, counters, complete mutation
  examples, omission histogram, environment, and source hashes.
- `run.log`: full successful local audit stdout.
- `upstream_tests.log`: independent rerun of the existing six-test G9 suite.

## What is being measured

The memory experiment creates the input before tracing, waits until the solver
has constructed its returned tuple, then resets tracemalloc's peak. It measures
additional allocations made by the validation/return phase, **not** total solver
memory, RSS, or the output tuple. The original creates two O(n) slices; the
corrected derivative uses constant-many indices and arithmetic temporaries.

The regression thresholds deliberately distinguish linear extra tuple-reference
storage from a small constant overhead. They are not a proof of the corrected
total bound: that proof is the explicit object accounting in AUDIT_REPORT.md.
The iterator exposes its exact remaining output length to avoid needless tuple
growth; allocator internals are outside the abstract wide-word claim.

The `assert` statements in the harness are test checks. Do not run this audit
under `python -O`, which disables them. A single deliberately mutated solver is
compiled with optimized mode only to observe its invalid return value after
reversing the equal-difference order; this does not alter the original or corrected
solver execution modes.

The target is permanently the pinned commit, not a moving PR head. This branch
adds evidence and a corrected derivative; it does not replace historical files.
