# Independent G9 prior-art investigation

Start with [PRIOR_ART_REPORT.md](PRIOR_ART_REPORT.md).

Finding: **incremental/combinational**, with substantial prior art for the
general mechanisms. No identical complete theorem was identified in the inspected
sources. The report independently derives the full bound from established ideas
and elementary deficit structure, and distinguishes that implication from an
earlier explicit statement or a worldwide-priority claim.

- [SOURCES.md](SOURCES.md): primary sources, dates, exact theorem locations, access scope.
- [SEARCH_LOG.md](SEARCH_LOG.md): thirty executed queries and citation-chain coverage.
- [reduction_checks.py](reduction_checks.py), [results.json](results.json): independent
  set-oracle experiments, MOCOSO brute-force comparisons, and canonical-transfer counterexamples.
- [MANUSCRIPT_AMENDMENT.md](MANUSCRIPT_AMENDMENT.md), [additions.bib](additions.bib):
  concrete proposed corrections to PR17's related work; existing exports preserved.
- [manifest.json](manifest.json): pinned snapshots and hashes of these artifacts.

Run from the repository root with Python 3:

```sh
python research/v03/g9_priority/reduction_checks.py
```

This folder is research evidence. It neither replaces nor edits the G3–G9 solvers.
The slower independent implementation is for reduction verification, not a new
performance claim. The proof, rather than benchmark timing, supplies asymptotics.
