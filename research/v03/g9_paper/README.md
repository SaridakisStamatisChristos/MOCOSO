# G9 canonical witness manuscript draft

Canonical source: [manuscript.md](manuscript.md). Bibliography: [references.bib](references.bib).

The manuscript is based on the immutable audit snapshot `43353e2b9a659d736b627788ec0c46554a090c75` and incorporates the priority findings at `b23ca44be7f5a0932c209b2b4f80a221830ed8b2`. The corrected research-only solver implements the quadratic-space theorem. The revision adds the missing sparse-extraction attribution, an explanatory inclusion-only proof, and separate reduction evidence. It is an incremental specialized technical note; it does not certify worldwide priority or publication readiness.

## Contents

- `exports/manuscript.pdf`: typeset reading copy.
- `exports/manuscript.docx`: editable Word copy with native equations.
- `exports/manuscript.tex`: standalone LaTeX generated from the canonical manuscript; rendered bibliography included.
- `references.bib`: editable verified bibliography used by Pandoc's citation processor.
- `PREFLIGHT.md`: early overlap and contribution screen.
- `REVIEW.md`: adversarial critique, five verdicts, final contribution stress test.
- `CLAIM_EVIDENCE.md`: proof and experimental claim mapping.
- `SOURCE_REGISTRY.md`: inspected primary sources and exact loci.
- `evidence_manifest.json`: pinned inputs, hashes, case counts, and separate rerun verification.
- `BUILD_QA.md`: artifact compilation and inspection results.
- `REVISION.md`: changes made after PR18 and readiness status.

## Rebuild

Install Pandoc with citeproc, XeLaTeX, and Python with python-docx, then run:

```bash
python research/v03/g9_paper/build.py
```

The script checks that every citation has a bibliography entry and that no entry is unused. It regenerates all three exports from the same Markdown and BibTeX. The DOCX uses Pandoc's native OMML equation conversion with python-docx styling. Compile the standalone LaTeX separately with XeLaTeX if desired. Binary file hashes may vary across rebuilds because document timestamps and archive metadata can change.

To rerun the audit, use a disposable checkout of the pinned evidence commit and follow `../g9_independent_audit/REPRODUCE.md`. The audit regenerates its JSON; do not overwrite the preserved historical run. No new experiment is inferred merely from rebuilding the manuscript.

## Readiness

Draft revised following PR18. The proposed amendment in the historical priority folder is now integrated into this manuscript and all regenerated exports; that earlier evidence snapshot remains preserved. The contribution is incremental/combinational. Remaining questions are exact-theorem priority beyond the inspected scope, author/expert review, and venue-specific significance. No submission, public preprint deposit, or repository merge is implied.
