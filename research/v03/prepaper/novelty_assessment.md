# G1 independent novelty assessment and gate verdict

**Date (UTC):** 2026-10-23
**Reviewer:** Knowledge Nexus plugin, independently invoked for literature mapping after G0. This is a **new source-based assessment**, NOT a human referee, NOT mathematical G2, and NOT a pre-paper G6 verdict.
**Frozen evaluated target:** `7595130fecb1a21dc8ca8823d9ee8d5d136af97a` (research PR #3 stacked on T1 PR #2); G1 work in separate research branch `research/v03-g1-knowledge-nexus`.
**Evidence:** `prior_art_catalog.md` and `closest_work_matrix.md` cite original accessible literature; G0 `evidence_register.md` used only for problem framing, **not** adopted as independent verification.

## Executive decision

**G1: REVISE / NOT CLEARED for strong algorithmic novelty.** The current T1 presentation has substantial **identified prior-art overlap**, especially:
1. **Dutta–Rajasree (preprint 2021, CALDAM 2022 lineage), Appendix B.1** directly gives a standard reachability-DP + predecessor DFS scheme for listing exact-target subset-sum solutions, with an output-sensitive \(O(n(t+k))\) time accounting. Source: https://arxiv.org/abs/2112.11020 .
2. **Allcock et al. (2021/2022), §3, Theorem 3.5 / Corollary 3.6** explicitly supports enumeration of subsets by sum *modulo p*. Source: https://arxiv.org/abs/2111.07059 .
3. **Kluev (2013)** describes the underlying convex subsequence edge sorting and discusses storing/reconstructing path witnesses. Source: https://stackoverflow.com/questions/20664920/longest-convex-subsequence-in-an-array .
4. **Conte et al. (2025), §4.3**, explains general extension-oracle/flashlight enumeration and output-based branch charging. This is a contextual **survey**, not another separate original proof: https://doi.org/10.4230/OASIcs.Grossi.19 .

**What survives:** The complete strict-convexity + modular **index** sum + global lexicographic optimization *formulation*, and the exact **q+2/q+3 immutable-suffix boundary** appear application-specific among the sources checked. No inspected original source was found with the entire T1 theorem **verbatim**. However, the C6 running-time expression looks like a **natural combination** of preexisting target-sum enumeration with a straightforward local predicate decomposition, not evidence of a fundamentally new enumeration algorithm. This is an epistemic distinction: **not located** is not **proved novel**, and **incremental combination** is not automatically publishable.

## Claim-level novelty dispositions

| Claim | Novelty disposition | Epistemic state | Evidence/counterevidence | Permitted claim language |
|---|---|---|---|---|
| **C1** Full MOCOSO optimization formulation | **UNRESOLVED (possible formulation-level distinctiveness)** | Unknown / insufficient evidence | P05 studies convex subsequences alone; P02 residue subsets alone; P06 path languages. No exact complete problem match in inspected set; search not exhaustive. | "We study the combined problem of ..." with no first/previously unknown claim |
| **C2** Backward/ordered-edge exact DP | **OVERLAP in foundational methods** | Strongly supported | P05 ordered edge convex DP (2013), P06 constrained paths (2000), P12 lex path-algebra concept | "We implement/adapt known DP principles to the additional index-residue and lex objective" |
| **C3** High-modulus complement | **OVERLAP / elementary reduction** | Strongly supported as a structural consequence; historical exact usage not fully scoped | \(s\le U<2m\Rightarrow s=m\) for any nonempty modular-selected sum; subset-complement duality. P07 distinct integer parts classical. | "In the high-modulus regime, a simple complement observation gives ..." |
| **C4** Immutable suffix locality | **PARTIAL / potentially application-specific** | Tentative | Consequence of omissions confined to \([1,q]\) plus convexity's triple locality; no exact predecessor with q+2 boundary observed. G2 mathematical proof pending. | "We derive an application-specific fixed-suffix screening lemma" **only after G2 validates** |
| **C5** Reachability-pruned distinct-part enumeration | **OVERLAP — new-enumerator claim is unsustainable** | Established for the generic mechanism, not MOCOSO correctness | P01 exact-target reachable DP + DFS; P03 equivalent true-state predecessor pruning; P04 generic flashlight search. Item weights \(1,2,\ldots,q\) are a restriction of P01's positive inputs. | "We apply known subset-sum reachability-guided backtracking to distinct omitted indices" |
| **C6** Combined \(O(n+qh+qP_d(h))\), \(O(qh+q)\) auxiliary | **PARTIAL / potentially new special-case bound statement, weak originality** | Tentative for significance; mathematical proof requires G2 | P01 has \(O(q(h+D_q(h)))\) analogous enumeration time; P07 counts \(P_d(h)\); C4 supplies \(O(q)\) per convexity test. Space comparison requires explicit streaming vs materialization distinction. | "We analyze a high-modulus exact specialization obtained by combining subset-sum DP/DFS with a local convexity filter" after G2; no first/best/new paradigm |
| **C7** T2 persistent lex / T3 structural research | **UNRESOLVED / no finished result** | Unknown | Only outline in MOCOSO research file; P05/P11/P12 show adjacent known space/lex techniques | Do not include theorem or novelty claims until an implementation-independent rigorous result exists |

## Material contradiction and resolution

**Hypothesis A (strong originality):** T1 is a newly invented output-sensitive algorithm for exact modular convex subsequences.

**Observed counterevidence:** The search/enumeration skeleton is already explicit in P01; modular subset-class enumeration is explicit in P02. Therefore A cannot be defended insofar as it attributes novelty to reachable-state backtracking or generic modular-subset enumeration.

**Narrowed hypothesis B:** T1 may provide a previously unstated **application-specific exact theorem**: a fixed-suffix locality lemma plus full lex-optimal witness for strict convex subsequences under a high-modulus selected-index residue, with a bounded deficit parameter.

**Disposition:** B is **not refuted** by inspected sources, but currently has only bounded negative-search evidence, and the compositional nature of its time bound undermines broad originality. A venue requiring a nontrivial new algorithmic mechanism may find B insufficient even if G2 confirms the proof.

**Not an apparent proof contradiction:** General exact-target enumeration results do not solve MOCOSO's arbitrary signed **value convexity** / global lex optimality automatically. Their overlapping selection subroutine is not a theorem refuting overall correctness or proving full equivalence. Literature novelty and mathematical exactness are independent gates.

## Source-dependence / confidence calibration

- P01 arXiv and related Springer chapter = **one research lineage**, not two independent demonstrations.
- P02 a different team's modular-subset enumeration = separate primary work, though both rely on the classical Bellman DP tradition.
- P03 independently reuses the same known structure in a different combinatorial problem, so corroborates **knownness** of the mechanism, not MOCOSO theorem correctness.
- P04 is a survey and cannot be counted as original novelty or independent discovery of each algorithm it discusses.
- P05 is an original public algorithm disclosure but not a peer-reviewed journal proof.
- P07 OEIS/Euler are a classical partition-combinatorics lineage.
- One exhaustive negative result across DBLP, OpenAlex, Semantic Scholar, Crossref, arXiv and Google Scholar has **not** been established. Site-filtered exploratory queries and selected primary-text reading do not supply comprehensive bibliometric coverage.
- Do **not** express novelty confidence as made-up numerical percentages.

## Decision-value-ranked remaining gaps

**G1-D1 — Prove or refute genuine theoretical separation (highest):** Translate P01's generic \(O(q(h+D_q(h)))\) exact-target DFS to T1 in full detail, then isolate which additional MOCOSO theorem is not merely a per-leaf \(O(q)\) predicate check. Compare every competing work/time/space model fairly; include the streaming single-best-space distinction. A critical reviewer will immediately try this reduction.

**G1-D2 — Originality search depth:** Perform API-level/exhaustive-ish thematic retrieval + citation-chaining around P01, P02, P05, related all-solutions subset-sum/partition enumeration, modular constrained longest paths, and strict convex subsequences; inspect closest originals, negative results with timestamps, exclusions and query logs. Full publisher P06/P08/P09/P12 texts or independent library access where available.

**G1-D3 — Mathematics (delegate independently to G2):** Prove q+2/q+3 boundary, no lost crossing triple, candidate accounting, lex tie semantics, h=0/q=n, and word/bit-space bounds; tests alone do not settle this. If false, novelty question becomes secondary to correctness repair.

**G1-D4 — Distinct research contribution (conditional G3 trigger):** Search T1+ for a genuinely stronger pruning or output-sensitive bound not reducible to basic subset-sum enumeration; or T2 for an exact persistent lex witness representation with strictly improved, fully counted memory/time; or T3 for a nontrivial structural theorem. A meaningful negative result with accurate limitations is acceptable. An extra proof of textbook reachability or a better Python runtime alone is not sufficient.

**G1-D5 — Empirical isolation (future G4):** Compare the exact same \((n,h,A,m)\) inputs against *generic P01-style DP+DFS* with convexity naive scan vs q-local scan, in addition to v0.2, to attribute any performance differences to the actual application-specific optimization. Favor feasible positive optima and report all losses and caps.

## Recommendation, handoff and release guard

1. **Immediate reviewer-facing language:** "MOCOSO combines a strict-convexity subsequence objective with a selected-index modular constraint and globally lexicographic optimization. For high moduli, we analyze an exact deficit-parameterized specialization based on classical subset-sum enumeration and a problem-specific locality observation." This is careful *descriptive* wording, not a priority/proof claim.
2. **Do not claim:** first modular-convex subsequence solver; first subset-sum enumeration with DP/backtracking; novel distinct partition generator; fastest/SOTA/universally superior; publication readiness. No evidence here supports those declarations.
3. **Gate transition:** G1 is **REVISE / NOT CLEARED** for a strong algorithmic-originality paper. G2 proceeds independently. **Recommend triggering G3 Algorithm Foundry once G2 shows what remains valid**, targeting a mathematically nontrivial improvement or justified narrower/technical-report result. Do not turn the draft manuscript into formal paper prose or merge PRs.
4. **Future G6 status:** still **PENDING**; G1 cannot issue final pre-publication GO/NO-GO in place of the independent SOTA Research Auditor.

### Reference provenance
See source IDs P01–P13, inspect-level indicators, dates, original URLs and unavailable sources in `prior_art_catalog.md`; see C1–C7 equation/mechanism comparison in `closest_work_matrix.md`. The reviewer made no production solver edits, ran no fresh code correctness tests, and did not represent its conclusions as external peer review.
