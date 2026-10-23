# MOCOSO

**Modular Convex Subsequence Optimization — exact algorithms and reproducible research.**

Given a sequence of arbitrary signed integers and a modulus `m >= 2`, find a longest subsequence whose consecutive value differences are strictly increasing and whose 1-based selected-index sum is divisible by `m`. Ties are broken lexicographically by selected indices. The empty subsequence is valid.

## Code and evidence

- [modconvex.py](modconvex.py) — exact optimizer and threshold decision solver, certificate checking, and brute-force oracle.
- [edge_dp.py](edge_dp.py) — structurally different exact dynamic program used in verification.
- [research_tests.py](research_tests.py), [edge_trials.py](edge_trials.py), [extra_trials.py](extra_trials.py) — differential, adversarial, and parameter-regime tests.
- [RESEARCH_REPORT.md](RESEARCH_REPORT.md) — mathematical formulations, proofs, complexity, guarantees, and open questions.
- [report.json](report.json), [edge_report.json](edge_report.json), [extra_report.json](extra_report.json), and corresponding `*.log` — recorded results and experimental provenance.
- [manifest_sha256.json](manifest_sha256.json) — SHA-256 hashes of the original research artifacts.

## Quick start

Python 3.10+ with no third-party runtime packages required:

```python
from modconvex import solve, verify
out = solve([0, 1, 3], 6)
assert out.status == "OPTIMAL"
assert out.indices == (1, 2, 3)
assert verify([0, 1, 3], 6, out.indices)
print(out)
```

Run the reproducible tests:

```bash
python research_tests.py
python edge_trials.py
python extra_trials.py
```

**Evidence caution:** Computational verification covers finite test sets only. Mathematical results are identified as proved arguments in the report, not formally machine-checked. Timing data depend on the stated platform and must not be interpreted as universally optimal performance. Resource-limit responses do not establish infeasibility.

**Repository status:** Research prototype. No license has been granted in this repository; consult the owner before reusing or redistributing code.
