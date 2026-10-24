# MOCOSO

**Modular Convex Subsequence Optimization — exact algorithms and reproducible research.**

Given a sequence of arbitrary signed integers and a modulus `m >= 2`, find a longest subsequence whose consecutive value differences are strictly increasing and whose 1-based selected-index sum is divisible by `m`. Ties are broken lexicographically by selected indices. The empty subsequence is valid.

## Code and evidence

- [G9 research guide](research/v03/README.md) — corrected quadratic-space canonical-witness algorithm, theorem, independent audit, prior-art investigation, and revised paper ([PDF](research/v03/g9_paper/exports/manuscript.pdf), [Word](research/v03/g9_paper/exports/manuscript.docx)).
- [modconvex.py](modconvex.py) — exact optimizer and threshold decision solver, certificate checking, and brute-force oracle.
- [edge_dp.py](edge_dp.py) — structurally different exact dynamic program used in verification.
- [research_tests.py](research_tests.py), [edge_trials.py](edge_trials.py), [extra_trials.py](extra_trials.py) — differential, adversarial, and parameter-regime tests.
- [RESEARCH_REPORT.md](RESEARCH_REPORT.md) — mathematical formulations, proofs, complexity, guarantees, and open questions.
- [RELIABILITY_V02.md](RELIABILITY_V02.md) — v0.2 memory packing, cooperative budget semantics, rejected alternatives and reproduction instructions.
- [benchmarks/compare_v02.py](benchmarks/compare_v02.py) — paired measurements against the preserved original implementation.
- [report.json](report.json), [edge_report.json](edge_report.json), [extra_report.json](extra_report.json), and corresponding `*.log` — recorded results and experimental provenance.
- [manifest_sha256.json](manifest_sha256.json) — SHA-256 hashes of the original research artifacts.

## Quick start

Python 3.10+ with no third-party runtime packages required:

```python
from modconvex import solve, verify, dense_dp_payload_bytes
out = solve([0, 1, 3], 6)
assert out.status == "OPTIMAL"
assert out.indices == (1, 2, 3)
assert verify([0, 1, 3], 6, out.indices)
print(out)
print('Minimum dense-table payload:', dense_dp_payload_bytes(100, 20), 'bytes')
```

Run the reproducible tests:

```bash
python research_tests.py
python edge_trials.py
python extra_trials.py
python -m unittest discover -s tests -p 'test_*.py' -v
```

**v0.2 memory:** For n <= 32,767, the two dense tables use 4 payload bytes per (pair, residue) state on typical platforms instead of the original 8. This is a storage-constant improvement, not a new asymptotic complexity bound. `max_seconds` and `max_heap_bytes` remain cooperative, not hard system-enforced limits. CI runs on Python 3.10–3.13.

**Evidence caution:** Computational verification covers finite test sets only. Mathematical results are identified as proved arguments in the report, not formally machine-checked. Timing data depend on the stated platform and must not be interpreted as universally optimal performance. Resource-limit responses do not establish infeasibility.

**Repository status:** Research prototype. No license has been granted in this repository; consult the owner before reusing or redistributing code.
