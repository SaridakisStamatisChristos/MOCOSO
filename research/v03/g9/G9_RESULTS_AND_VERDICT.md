# G9 independent-gate verdict (2026-10-24)

**Original high-modulus cubic-time / quadratic-memory full-lex challenge MET in the mathematical wide-word model by a sharper subcubic-time bound.** H=h+1, 0<=h<n:

\[
T=O(n+H^{5/2}\log^2(h+2))\subseteq O(n+H^3),
\qquad S=O(H^2).
\]

The proof (G9_THEOREM_LAB.md) derives sparse eligible edges, an exact forced-prefix scalar length oracle, logarithmic monotone next-omission search, global lex reversal and full bit-model caveats. Exact code and independent oracle tests are under experiments/v03/g9_quadratic_lex.py and tests/test_v03_g9_quadratic_lex.py.

| Independent gate | Disposition |
|---|---|
| Theorem correctness | COMPLETE HUMAN-CHECKABLE PROOF in stated model; no formal checker or external referee |
| Implementation exactness | Local candidate survived 21,321+145,632 exhaustive selected-subset cases and 5,500 seeded independent partition cases; committed CI must be checked separately |
| Original simultaneous O(n+H³)/O(H²) objective | **ACHIEVED in wide words**; even O(n+H^(5/2)log² H) time |
| Standard fixed-word / bit RSS guarantee | NOT CLAIMED. Input word-size B and Python object overhead matter |
| Algorithmic novelty | CLASSICAL SELF-REDUCTION and sorted-resource DP plus specialized bounds; likely compositional |
| Global literature priority | UNRESOLVED, bounded source-specific audit only |
| Scientific significance | Stronger internal mathematical guarantee, independently new general primitive not demonstrated |
| Paper readiness | HOLD, explicitly prohibited |
| Preservation | G3–G8 evidence and executables preserved, production unmodified, separate stacked draft PR, no merge |
