# Build and verification record

Date: 2026-10-24.

- One canonical manuscript and bibliography generated standalone LaTeX, a 10-page PDF, and an editable DOCX with native OMML equations. The Word rendering is also 10 pages; line wrapping and page breaks differ between formats.
- Bibliography reconciliation passed: all six entries are cited; all citation keys resolve. Inspected primary sources and loci are recorded in SOURCE_REGISTRY.md.
- Canonical math-node count and DOCX native equation count match exactly. No equation was intentionally rasterized.
- All Word pages were rendered and visually inspected. The PDF was rendered and inspected, with a final full-page overview and targeted reinspection after repairs. No clipped text or unresolved equation glyph markers remain; automated text bounds also found no words outside a 35-point page inset in either PDF render.
- Initial Word conversion mishandled set-difference and auto-sized floor delimiters. The canonical manuscript now defines the complement in prose and uses equivalent floor/ceil function notation consistently across every format. A long inline commit identifier also caused PDF overflow; prose uses short identifiers while the reference and evidence manifest retain complete immutable hashes. These are presentation repairs, not mathematical changes.
- A fresh audit ran in a disposable detached checkout of 43353e2b9a659d736b627788ec0c46554a090c75. All 80,283 complete-witness cases, all 13,767 forced scalar queries, event checks, mutation examples, and semantic result fields matched the preserved evidence. Runtime-dependent timing and allocation-byte data were not required to match.
- The six existing G9 unit tests passed again with assertions enabled.
- Historical source and evidence files were not edited. All added manuscript files are under research/v03/g9_paper/.
- PREFLIGHT.md, CLAIM_EVIDENCE.md, SOURCE_REGISTRY.md, and REVIEW.md document the contribution screen, claim mapping, citations, adversarial critique, and final stress test. Draft gate is conditional; this build does not certify priority, external review, or submission readiness.

Build tools: Pandoc with citeproc, XeLaTeX, Python 3.12 and python-docx. Final source/export SHA-256 values are in artifact_hashes.json; reproducible evidence input hashes are in evidence_manifest.json. Rebuilding can change binary hashes due to timestamps.
