# Revised manuscript build and verification record

Date: 2026-10-24. Revision follows priority snapshot
b23ca44be7f5a0932c209b2b4f80a221830ed8b2.

## Current revision

- One canonical manuscript and bibliography generated standalone LaTeX, a
  **13-page PDF**, and an editable DOCX whose LibreOffice rendering has **12 pages**.
  Page breaks differ between formats; the scientific content is shared.
- Citation reconciliation passed for **eleven** entries: every key resolves,
  every entry is cited, and there are no duplicate keys. Conference/full-version
  and journal/preprint distinctions are recorded in SOURCE_REGISTRY.md.
- The canonical Pandoc AST contains **255 math nodes**; the DOCX contains exactly
  **255 native OMML equations**. No equations were intentionally rasterized.
- All thirteen PDF page images and all twelve Word page images were opened and
  visually inspected, including Proposition 9, both evidence tables, and the
  expanded references. No clipping, overlapping text, or missing equation
  glyphs was observed. Text-bound checks found no words beyond the configured
  35-point left/right/top and 25-point bottom safety insets in either PDF render;
  extracted text contains no Unicode replacement characters.
- The priority reduction checks were executed again with seed 20261024. Their
  complete JSON output exactly matches the preserved result: 2,228 exhaustive
  uniform families, 3,000 random families, 7,612 MOCOSO instances, and 30,448
  constrained scores. The original result file was not overwritten.
- Every pinned original-audit input hash and every priority-folder hash was
  checked against evidence_manifest.json. All were unchanged.
- The corrected G9 solver and original 80,283-instance audit were not modified
  or rerun in this manuscript-only revision. Their prior verification is retained
  as historical evidence rather than presented as new work.
- PREFLIGHT.md and REVIEW.md record the updated overlap analysis, repaired major
  objections, explicit contribution stress test, and propagation through the
  manuscript. Classification: **INCREMENTAL / COMBINATIONAL**. Publication gate:
  **REFRAME completed as a technical note; submission readiness not established**.

## Preserved earlier verification

The previous manuscript build reran the original audit in a disposable checkout
of 43353e2b9a659d736b627788ec0c46554a090c75. Its 80,283 complete-witness cases,
13,767 forced scalar queries, event checks, mutation examples, and semantic
fields reproduced the preserved evidence; all six existing G9 unit tests passed.
Those details remain in evidence_manifest.json and the previous Git revision.

The original build also repaired Word conversion of set-difference and auto-sized
floor delimiters by using equivalent prose/function notation. This revision
retains those repairs. Compilation uses Pandoc with citeproc, XeLaTeX, and the
bundled Python runtime with python-docx; Word rendering uses the document skill's
renderer. Build success and visual QA do not certify mathematical priority,
external review, venue suitability, or submission acceptance.

Final source/export hashes are recorded in artifact_hashes.json. Binary hashes
can vary after rebuilding because timestamps and archive metadata can change.
