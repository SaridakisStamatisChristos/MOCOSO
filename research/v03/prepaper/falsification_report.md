# G2 — Independent falsification report (executed evidence, not a machine proof)

**Date:** 2026-10-23 UTC. Author: separately invoked Theorem Foundry.
**Underlying frozen research algorithm:** `7595130fecb1a21dc8ca8823d9ee8d5d136af97a`; **G2 PR:** https://github.com/SaridakisStamatisChristos/MOCOSO/pull/6 (standalone branch from G0, not G1's PR #5).
**Status:** No counterexample found to canonical T1 abstract correctness, lex minimality, crossing-triple locality or *returned* certificate invariants in the domains tested. These are finite checks and **not proof of arbitrary size**. Human mathematical proof separately in `independent_proof_audit.md`.

## Direct executed source and command

- New code: `research/v03/prepaper/g2_independent_checks.py`, independently authored after inspecting the algorithm and problem contract; uses full selected-index subset enumeration with **independent algebraic predicate** `a[i]+a[k]>2a[j]`, not omission enumeration, not original `modconvex.verify`, not the supplied T1 proof.
- For 3^i inputs, a separate exact *sum-residue and lex-tuple* DP computes the optimum independently of the high-modulus omission construction.
- Also checks complement index-sum identity on finite subsets, immutable-suffix/local-prefix triple equivalence, global optimal witnesses, threshold FEASIBLE/INFEASIBLE/OPTIMAL, RESOURCE_LIMIT validity and 0<=LB<=OPT<=UB<=n, plus zero/boundary cases.
- Declared deterministic random seed: `2601023`; five deterministic input families used for local triple checks; signed 170-digit-scale values, constants, alternating signs, zeros and negative values included.
- CI command `python research/v03/prepaper/g2_independent_checks.py` with `PYTHONHASHSEED=0`, `PYTHONPATH=.`, and `core.autocrlf=false`. Compilation/interpreter checked by GitHub Actions. Script SHA256 **`6a8c90d74b32c0b7ea5dec2dcaf1f2fb6181d0f13b115ef0a505f29ee96ac262`** (logged in all four initial jobs).
- Workflow: `.github/workflows/v03-g2-proof-audit.yml`. No tests are represented as a formal proof checker; Lean/Coq/Isabelle were not run.

## Primary independently inspected GitHub Actions evidence

Run [40025669353](https://github.com/SaridakisStamatisChristos/MOCOSO/actions/runs/40025669353) ran against the **GitHub Actions pull_request test-merge checkout** `fbd022c47474d940bc05fba56b51ae14c59b7792` as printed in raw logs (not the pushed head of PR #6). Every job ran `git diff --exit-code 7595130fec... -- modconvex.py edge_dp.py experiments/v03/deficit.py experiments/v03/baselines.py research/v03/t1_deficit_proof.md`, and the check succeeded. This protects the claim that the tested algorithm/proof sources match the pinned original research head.

| OS / interpreter | Job ID | Outcome | Runtime evidence |
|---|---:|---|---|
| Ubuntu Python 3.11.17 | 120661105925 | SUCCESS | 4 unit tests, 1.354 sec |
| Ubuntu Python 3.13.16 | 120661106293 | SUCCESS | 4 unit tests, 1.869 sec |
| Windows Python 3.11.9 | 120661107258 | SUCCESS | 4 unit tests, 1.931 sec |
| Windows Python 3.13.16 | 120661106217 | SUCCESS | 4 unit tests, 2.129 sec |

**Per matrix job**, raw `G2_INDEPENDENT_SUMMARY` printed:

```json
{
  "success": true,
  "counts": {
    "full_oracle": 11567,
    "triple_locality": 2485,
    "certificate": 14511,
    "superconvex_dp": 25,
    "v02_reference": 55
  },
  "code_sha256": "6a8c90d74b32c0b7ea5dec2dcaf1f2fb6181d0f13b115ef0a505f29ee96ac262"
}
```

**Counting discipline:** These are counts from the same deterministic suite run independently on four interpreter/OS combinations. They are not four independent sets of 11,567 input samples; certificate counts include multiple thresholds and budgets per input, and locality checks loop over omission choices and families.

### CI artifacts / expiration

Each four-job log bundle contains `g2_test_results.txt` and `g2_environment.txt`, according to workflow and upload API. ZIP digests below are **GitHub-reported**, not independently SHA256-rehashed by this reviewer.

| Artifact | GitHub ID | ZIP SHA256 |
|---|---:|---|
| Ubuntu 3.11 | 12531714631 | `9affd8d9f8dce878579591f322e06551cb824fdd22436ad2374979ec5e643929` |
| Ubuntu 3.13 | 12532880912 | `6c1656baf40db1ec18edbbec378e7fc5e1ac72741ce1737883735315d00ed4cf` |
| Windows 3.11 | 12532701371 | `b7f1f82a55bd46ea26e1c9b059fb936597d4949be38027f37054657c3bc04aed` |
| Windows 3.13 | 12532143776 | `aca774b8a6a467e908e4143932b75ef92d1afb466869e5d4337c1e27500ff66e` |

At review, all four report an expiry of **2027-01-21 21:17:27 UTC**; archive for G5 non-expiring supplement. Historical CI from earlier gates belongs to different source/checkpoint ancestry and is not independent G2 verification.

## Attacks and counterexample results

| Attack | Method | Outcome |
|---|---|---|
| L1 complement and domain | All actual O with sum h, direct complement sum verification; n=2..9 | No falsifier |
| L2 crossing triples | Full selected triple predicate vs O(q) local prefix and fixed suffix, including q=0/q=n, five array families | No falsifier in 2485 comparisons |
| T1 exact global lex optimum | Direct 2^n selected-subset exhaustive oracle on full small Cartesian grid and 1100 seeded huge-signed instances | No falsifier in 11567 complete-oracle comparisons |
| Resource/certificate semantics | Direct oracle OPT + 14511 result checks including K<0, K=0, K>OPT, 0/1/bounded operation budgets, time=0, traced-heap=0/1 | No falsifier among successfully returned outputs |
| Large positive-optimum cases | Index-sum-residue DP for superconvex inputs n up to 35 | No falsifier in 25 comparisons |
| Imported v0.2 baseline | Compare existing API against independent subset oracle on 55 random high-modulus instances, plus existing historical CI | No falsifier in this bounded subcampaign |
| Potential full-machine verification | Checked local available Lean/Coq/Isabelle executable availability; absent | NOT RUN / NOT FORMALLY VERIFIED |
| Catastrophic OS memory failure | Not intentionally triggered; no hard RSS supervisor. Reentrant allocation in result/exception handler can fail | Unconditional successful return on every OOM **NOT GUARANTEED**, not a tested counterexample to conditional returned-value soundness |

No minimized concrete T1 witness exists because no case failed. If future G3/G4 finds one, preserve its (n,m,A,K,limits), source SHA, exact erroneous output, independent oracle answer, and minimized size in an append-only record.

## Residual formal/software limitations

1. Mathematical proof covers the intended abstract T1 algorithm and a conditional word model; **not** full line-by-line formal semantics of CPython allocations, exceptions, OS process termination, or counters.
2. G2 suite verifies finite sources and full witnesses on selected signed families; cannot establish that no integer/biginput counterexample exists outside tested bounds.
3. `max_seconds`, `max_heap_bytes` are soft; hard time or RSS cap and crash-safe certificate delivery should not be asserted.
4. No independent large-instance brute force oracle for arbitrary `a`; superconvex family is separately solvable by residue DP, but special.
5. Bit-complexity and measured peak memory are different from `O(n+qh+q P_d(h))` word time and O(qh+q) auxiliary words. The correct caveats are mandatory before G6.
6. Prior-art review G1 reports direct overlap in known subset-sum enumeration. This is **not** a correctness counterexample but materially affects publication prospects.

**G2 final status:** independent *human-checkable abstract proof* PROVED conditional; *finite code falsification* PASS; formal machine verification NOT DONE; unconditional hard budget/OOM result guarantee NOT SUPPORTED; originality reserved for G1/G3 and final publication decision for G6. No merge or manuscript writing.
