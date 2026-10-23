# G2 — Acyclic proof dependency graph and evidence states

**Research target:** MOCOSO T1 at `7595130fecb1a21dc8ca8823d9ee8d5d136af97a`. **Date:** 2026-10-23 UTC. Reviewer: separately invoked Theorem Foundry. This record certifies human-readable deductions only; no proof assistant was run. The exact derivations are in `independent_proof_audit.md`.

## DAG (arrows are logical dependencies, NOT chronological implementation order)

```mermaid
flowchart TD
  D[Definitions: index sum, strict convexity, lex order] --> L1[L1: single multiple & complement]
  D --> L2[L2: fixed suffix triple locality]
  L1 --> L2
  S[Finite subset dichotomy: include / exclude t] --> L3[L3: R recurrence is exact]
  L3 --> L4[L4: unique pruned reachable DFS]
  L1 --> L4
  L1 --> L5[L5: complete candidate domain]
  L2 --> L5
  L4 --> L5
  L5 --> L6[L6: OPT + full lex; sound returned certificates]
  L2 --> L7[L7: per candidate O(q) locality]
  L3 --> L7
  L4 --> L7
  E[Classical Euler distinct-parts generating function] --> P[Bound Pd(h) <= exp(2 sqrt h)]
  L7 --> T[T1 time and auxiliary-space in wide-word model]
  P --> T
  A[Exact arithmetic and valid word width] --> T
  V[v0.2 two-index residue recurrence] --> V2[v0.2 descending j sweep and lex pointers]
  D --> V
  V2 --> VB[v0.2 exact optimization for successful runs]
  CI[Independent finite G2 execution] -. Falsification evidence, not proof .-> L5
  CI -. Falsification evidence, not proof .-> L6
```

The threshold/certificate branch requires L5 completeness for exhaustive infeasibility and feasible-witness validity for partial returns. **Do not use the G1 novelty analysis as a mathematical premise.** Distinct parts P_d is a known combinatorial object, not a new lemma.

## Node ledger

| Node | Dependencies | Status | Proof/observation | Important limitation |
|---|---|---|---|---|
| D | Definitions and integer arithmetic | PROVED / definition | Exact problem statement | n>=2 in specialized domain; empty allowed |
| L1 | D, U<n*m relation | PROVED human | Bound 0<s<=U<2m | Only *nonempty* modular candidates |
| L2 | D, L1 | PROVED human | Partition triples by last selected index <=q+2 vs >=q+3 | q=0 and q=n explicitly accounted |
| L3 | include/exclude identity | PROVED human | Induction in t | R is exact only for nonnegative targets <=h |
| L4 | L1, L3 | PROVED human | DFS bijection and charging to leaves | q=0 singleton and D=0 no-leaf case |
| L5 | L1,L2,L4 | PROVED human | Feasible candidate enumeration; fixed-suffix full-lex equivalence | Requires *complete* enumeration for OPT |
| L6 | L5 | PROVED conditional | Return status logic | No unconditional OOM-return guarantee |
| E/P | classical generating function | PROVED human / classical | \(\log(1+z)\le z\), optimize x=1/sqrt(h) | Requires h>0; h=0 handled separately |
| L7/T | L2,L3,L4,P, model assumptions | PROVED conditional | Count qh, qD, n; bound auxiliary bytes/words | Big-int bit cost and Python RSS not unit word count |
| V/V2/VB | strict triple recurrence; sweep order; pointer ties | PROVED abstract | Descending second index and monotone k eligibility | Finite CI not a machine proof of code |
| CI | separately-authored script + GitHub Actions | FINITE TEST PASSED | Run 40025669353 all 4 matrix jobs passed | NOT FORMALLY VERIFIED; sampled finite inputs |
| G1 priority | outside G2 mathematical DAG | NOT CLEARED (G1) | Classical enumeration overlaps | G2 mathematical PASS cannot override novelty gate |

## Rejected/invalid dependency patterns

- `finite oracle tests => universal theorem`: INVALID. Tests can falsify, not prove infinite signed-input claim.
- `P_d(h) partition bound => novel new algorithm`: INVALID. A classical count bound does not establish research originality.
- `DP stores O(qh) byte cells => process RSS <= Cqh`: INVALID; Python objects, runtime, memory allocator, tracing overhead and output are outside that accounting.
- `RESOURCE_LIMIT always returns a witness even if OOM kills process`: INVALID; partial certificate guarantee applies to *returned results*.
- `G0 CI status => independent proof`: INVALID. G2's proof is separately documented; G0 tests are historical supporting observations.
- `C5 reachability/DFS was invented by this research`: INVALID. G1 identifies earlier general mechanisms; not a premise for L4's mathematical correctness.

## Handoff

Mathematical T1 passes under narrow conditions. G3 should compare new candidates against the *generic subset-sum DP+DFS* baseline while seeking a genuinely stronger theorem; G1 novelty limitations remain binding. G4 must not treat `RESOURCE_LIMIT` as negative feasibility. G6 independent auditor still owns publication GO/NO-GO.
