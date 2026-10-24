# G9 canonical witness manuscript draft

Canonical source: [manuscript.md](manuscript.md). Bibliography: [references.bib](references.bib).

The manuscript is based on the immutable audit snapshot `43353e2b9a659d736b627788ec0c46554a090c75` and designates its corrected research-only solver as the implementation of the quadratic-space theorem. It does not alter original G3–G9 source, merge any research branch, or certify literature priority or publication readiness.

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

## Rebuild

Install Pandoc with citeproc, XeLaTeX, and Python with python-docx, then run:

```bash
python research/v03/g9_paper/build.py
```

The script checks that every citation has a bibliography entry and that no entry is unused. It regenerates all three exports from the same Markdown and BibTeX. The DOCX uses Pandoc's native OMML equation conversion with python-docx styling. Compile the standalone LaTeX separately with XeLaTeX if desired. Binary file hashes may vary across rebuilds because document timestamps and archive metadata can change.

To rerun the audit, use a disposable checkout of the pinned evidence commit and follow `../g9_independent_audit/REPRODUCE.md`. The audit regenerates its JSON; do not overwrite the preserved historical run. No new experiment is inferred merely from rebuilding the manuscript.

## Readiness

Draft complete, contribution assessment conditional. Remaining questions are external priority coverage, author/expert review, and a venue-specific significance case. No submission, public preprint deposit, or repository merge is implied by this draft.
