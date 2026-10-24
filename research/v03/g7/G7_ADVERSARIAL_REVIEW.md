# G7.3 independent falsification and review ledger

Date: 2026-10-24. Reviewer roles: Theorem Foundry (logical DAG), Algorithm Foundry (independent selected-subset oracle), SOTA Research Auditor (prior-method and complexity overclaim attack).

## Validated scope and independent oracle

The research-only G7 compact-lex implementation does **not** import G3 or PR #11. A direct index-*subset* enumerator checks each mask in [0,2^n), verifies selected-index sum %m, checks every selected strict triple, then maximizes (cardinality,-lex tuple) exactly. It does not reuse the omission DP. The standalone independent prototype and tests ran locally on Linux CPython 3.13.5 (kernel 6.18.55), with:

- A∈{-1,0,1}^n for n=2..7, all legal U/2<m<=U with h<n: **21,321** entire tuple comparisons.
- A∈{-2,-1,0,1}^n over the same n/m domain: **145,632** entire tuple comparisons.
- **1,000** pseudorandom cases with seed 20261024, n=2..10, h chosen uniformly in allowed range, elements in {±10^160,±10^90,-1,0,1}; complete oracle comparisons.
- Deterministic h=0, n=2 singleton, repeated/equal difference, n=1000,h=4 superconvex and broken mandatory-suffix cases. Additional focused true lex tie from n=6,m=16,a=(-3,-3,-3,-3,-2,0).

Observed outcomes on the local standalone prototype: **all passed**. These counts describe corpus comparisons, not distinct independent OS samples, not proof of the general theorem, and not GitHub Actions outcomes. Local prototype SHA256: \`787efbf38f321051bf644d46339d242956f5923c5981822e5989de16a44849d3\` (filename \`compact_omission_lex.py\`); committed GitHub source is a separate transcription and must use its own Git blob SHA/CI fingerprint. Exact local test script \`test_compact.py\` SHA256 \`f93648d2c9c27720feb30df06e14315b7d94a4bbce08c39f69fa8c2a20cce226\`; the four-valued second exhaustive corpus was executed as an explicit one-off local script and then made a committed test method.

## Serious adversarial objections

1. **Omissions bound incorrectly applies to arbitrary prefix length?** Discharged: omission indices are distinct, positive, and sum r<=h in every state; count <=floor((sqrt(8h+1)-1)/2), independent of n and prefix endpoint.
2. **Lex reversal valid for different cardinalities?** Discharged conditionally: first compare selected cardinality; only compare omitted tuples on a tie. For equal selected cardinality *at the same endpoint* the omitted tuple cardinality is also equal, so lex reversal applies.
3. **Same-difference chaining?** Discharged by descending destination ordering; independent counterexample a=(0,1,2), n=3, m=6 explicitly attacks the incorrect alternative.
4. **Mandatory suffix or crossing triple silently skipped?** Discharged by suffix scan ending >=q+3 plus event DP through p=q+2 where possible. Test n=7,m=26,a=(0,1,2,3,7,15,31) must yield empty because crossing triple fails.
5. **Cheating with Python tuple/object word accounting?** The abstract theorem charges every omitted list member explicitly, O(sqrt h) time per copy/compare and space per live state; Python allocations and arbitrary-precision bit arithmetic are not bounded by the word theorem.
6. **Theorem strictly improves G3?** **No dominating result**: time exponent is worse, space exponent is better. Calling it a universal stronger complexity theorem would overstate the evidence.
7. **The new result is fundamentally original?** **No originality demonstration**: sorted-edge DP and resource lifting predate this branch; bounded distinct-part representations are elementary. A compositional space/time Pareto result is defensible; theory novelty remains open.
8. **A fifth superconvex optimal tuple spoils a lex tie test?** **Yes: rejected fixture!** For n=6,h=5 superconvex a=3^i, omitting {5} yields a length-5 witness, so pairs {1,4}/{2,3} do not determine global optimal tie. Replaced with signed tuple (-3,-3,-3,-3,-2,0) where singleton-{5} candidate is invalid and the true lex tie holds.

## Execution vs CI

A native Linux/Windows × Python 3.11/3.13 GitHub Actions test matrix is committed at \`.github/workflows/v03-g7-compact-lex.yml\`. The workflow enforces source-preservation diff, runs the committed independent direct-subset oracle plus G3 comparator, records commit/runtime/file hash and uploads logs. **At original G7 head `e8ff4846968699488a3cba6f995dbbb19a038be3`, GitHub Actions run [40083406635](https://github.com/SaridakisStamatisChristos/MOCOSO/actions/runs/40083406635) completed successfully; its 4/4 Linux/Windows x Python 3.11/3.13 jobs succeeded. This verifies that frozen G7 head only; subsequent G8-head tests need independent run results.** No formal verifier/Lean run was done. No performance benchmarking or Python RSS guarantee is claimed; the asymptotic bound is established by the proof, not empirical timing.

## Outstanding independent proof obligations

Primary target O(n+h^3) time/O(h²) space with globally least entire witness: **OPEN**. Specifically the safe dynamic history/rank reconstruction without cubic persistent state or an extra p recomputation factor is unproved. Generic bounded-frontier traceback has not been reduced parameter-preservingly to this sorted-event DP.


## G8 handoff: independent G7 audit corrections (2026-10-24)

The additional omission-partition oracle reported in the PR #13 SOTA Auditor review is now reproducibly encoded in \`tests/test_v03_g7_independent_partition.py\`, **independent of both the G7 edge sweep and G3 pair-state DP**. The test enumerates strictly increasing omitted index partitions with exact sum h, forms each full complement and independently checks strict triples and entire-tuple lex order. It tests the actual \`experiments/v03/g7_compact_lex.py\` function, not a local transcription.

Reproduction: \`python -m unittest -v tests.test_v03_g7_independent_partition\`. Defined deterministic corpus: exhaustive A in {-1,0,1}^n for n=2..7 over h<n and high-modulus, 21,321 cases; plus 1,500 seeded cases (seed 22102407, 2<=n<=100, h<=16, giant signed elements) and the true lex tie fixture. This description is a **test specification**, not an assertion that a newly committed head's CI is green. The separately executed Linux CPython 3.13.5 local prototype matched all 21,321 + 1,500 cases. Retain explicit distinction between independently audited prototype and independently CI-tested repository code.

All G3-G7 antecedents remain immutable. Proof details, bit-cost qualifications, and G8's subsequent verdict are separate from the G7-P originally established claim.
