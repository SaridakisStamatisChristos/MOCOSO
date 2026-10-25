# G3 — Execution evidence, measured comparisons, and conditional gate decision

**Owner:** Algorithm Foundry, user-invoked 2026-10-24. **Original research SHA:** 7595130fecb1a21dc8ca8823d9ee8d5d136af97a. **Review branch:** research/v03-g3-polynomial-deficit; initial tested change-set head 355c30c3384b0edbb5debae96c53811d93a96234; later proof-only commits MUST be distinguished when checking latest CI. PR #7: https://github.com/SaridakisStamatisChristos/MOCOSO/pull/7, draft/unmerged.

## 1. Direct executed gate (initial code/test/benchmark head)

GitHub Actions run https://github.com/SaridakisStamatisChristos/MOCOSO/actions/runs/40057400536 : **5/5 successful jobs**.

- ubuntu-latest Python 3.11: job 120763304800, 4 unittest methods executed, 6.882 seconds, OK.
- ubuntu-latest Python 3.13: job 120763304777, success.
- windows-latest Python 3.11: job 120763304807, success.
- windows-latest Python 3.13: job 120763304767, 4 unittest methods executed, 7.457 seconds, OK.
- benchmark Ubuntu Python 3.11: job 120763304679, success. All two-algorithm runs returned OPTIMAL and produced **identical full witness tuples** for every case.

The independent full selected-subset oracle, rather than the G3 edge DP itself, verifies the 41,085 full Cartesian (n=2..7, A in {-1,0,1}^n and every high modulus) tests **per execution**, plus 850 seeded signed ~150-digit integer inputs. Seed: 20261024. Additional tests cover arbitrary thresholds K, sound RESOURCE_LIMIT with conservative bounds, n up to 1000 with positive superconvex values a_i=3^(i-1), and a separate index-residue tuple DP oracle for the smaller superconvex instances. Do **not** multiply same deterministic coverage by four and pretend it is four independent samples.

### Artifact provenance

These are **GitHub-reported** artifact ZIP SHA256 digests, not bytes independently downloaded/rehashed by this reviewer; all initial runs report expiry 2027-01-22 03:13:11 UTC:

| Asset | Artifact ID | GitHub-reported ZIP sha256 |
|---|---:|---|
| preregistered Ubuntu Py3.11 benchmark | 12546380258 | 47ca1ed938493acd0e4d68516f231ac1028d42236d8674c785dae3e15a613755 |
| Ubuntu Py3.11 exactness | 12546355456 | 4e93ddcd0a9c8f75c442e2e81ab8f0079bcab0a81c11a82b4384fb6e488e6c67 |
| Ubuntu Py3.13 exactness | 12545947615 | a2b527a6f9490b32b1b7e93cc12449f96aa447f4a564517558cbe8bc9361835a |
| Windows Py3.11 exactness | 12545682143 | e13d5b3d74ad4cf971f9f84796c248a57f9122a06c209bf860218e414917a4cf |
| Windows Py3.13 exactness | 12545658459 | b581b97301ac10a105e7ac22d010de57e2fc97a267b4369e01fb0ced7856c2b9 |

Full raw JSONL timings are in artifact 12546380258, emitted by command:

~~~
python experiments/v03/benchmark_poly_deficit.py --profile ci --repetitions 2
~~~

Comparison design: predetermined 7 (n,h) pairs x 2 input families (superconvex a_i=3^(i-1), and alternating signed repeated a_i=(-1)^i (i mod 7)), two medians from **two samples each**, pinned Ubuntu Python 3.11.17, seed label 20261024, one Actions runner. This is an exploratory smoke benchmark, **not** a statistical multi-machine performance claim. Times are nanosecond wall readings and depend on hardware/load/bit widths. Both full tuple outputs are checked for exact equality on each case; non-OPTIMAL status fails the benchmark.

## 2. Exact observed medians — positive optimum family

| n | h | optimal length | T1 median ms | G3 median ms | T1/G3 median ratio |
|---:|---:|---:|---:|---:|---:|
| 12 | 4 | 11 | 0.04 | 0.06 | 0.67 |
| 25 | 15 | 24 | 0.23 | 0.29 | 0.77 |
| 40 | 25 | 39 | 1.07 | 0.68 | 1.57 |
| 60 | 40 | 59 | 9.81 | 1.98 | 4.95 |
| 75 | 50 | 74 | 36.97 | 3.62 | 10.22 |
| 90 | 60 | 89 | 125.07 | 5.32 | 23.49 |
| 1000 | 4 | 999 | 0.34 | 0.45 | 0.77 |

The measured ratios on large h for this family are consistent with the asymptotic enumeration-vs-DP distinction, **not a proof of the O-bound**. At h=4 and h=15 T1 is measured faster, an important non-dominance result. The seven alternating-value cases all produced empty optima; both algorithms often finished with a fixed-suffix rejection in ~0.01ms, and such tiny timings must not be interpreted as meaningful superiority in either direction. No cases were removed because G3 lost.

**The separate asymptotic separation proof** in g3_asymptotic_separation.md exhibits a complete input family on which T1 enumerates P_d(h) candidate omission sets while G3 performs polynomial work. This is a fixed-algorithm comparison only, NOT a lower bound on all solutions or a claim of new theoretical research priority.

## 3. Reproducibility/verification qualification

- Local independent prototype preceding GitHub push passed 41,085 direct-subset exhaustive comparisons and 1,000 seeded signed-bigint instances; these are **development probes**, distinct from the GitHub-committed tests' 850 random instances. The local prototype's SHA is not the committed SHA: GitHub CI is authoritative for source verification.
- The committed code and tests are in experiments/v03/poly_deficit.py, tests/test_v03_poly_deficit.py; CI freeze guard compares v0.2 and original T1 source/proof against SHA 7595130f... and must succeed.
- Bench comparisons are T1 vs G3; a separate faithful generic constrained-DAG DP and G4's pre-registered paper profile are not yet measured. Thus this is **not** a comprehensive SOTA comparison.
- Python allocation overhead and arbitrary-precision integer costs are not certified by theoretical wide-word asymptotics.
- The preflight cell cap (default 1,000,000) is cooperative: it may return RESOURCE_LIMIT with a verified empty lower-bound witness and safe n upper bound. It does not enforce an OS process RSS ceiling; catastrophic OOM return is not guaranteed.
- No proof assistant checker was executed; human mathematical proof is in g3_polynomial_deficit_theorem.md. No external human mathematical referee has validated it yet.
- Previous G1 novelty audit found generic enumerative and graph-DP building blocks; resource-constrained path DPs are independently established in the literature. The priority of this particular bound is **unresolved**.
- Original experimental T1, v0.2 production solver, paper proof and their Git histories remain unchanged; all G1/G2/G3 branches and PRs remain separate and unmerged.

## 4. Gate decision and onward constraints

**G3 ALGORITHMIC STRENGTHENING: CONDITIONAL PASS.** The current research implementation and its direct tests passed, and the stated abstract polynomial-deficit bound has a complete human-checkable proof. An explicit input family separates its worst-case candidate count from original T1 enumeration, but this does **not** certify novelty over resource-constrained DAG DP literature or publication readiness.

**G3 scientific originality: NOT CLEARED.** Strong priority claims require independent updated G1 screening of the constrained-path variant and a mathematical external challenge to this new G3-T1+ proof. To proceed through G4, register harder cases and a faithful generic resource-constrained-DAG comparator, repeat on multiple environments, report memory peaks, cap and failure cases and complete 146-case profile; G5 must independently rehash preserved artifacts and reconstruct a clean checkout. G6 SOTA Research Auditor alone issues final paper GO/NO-GO. No merging and no manuscript writing within G3.
