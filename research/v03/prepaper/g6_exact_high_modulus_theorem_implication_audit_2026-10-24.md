# Focused G6-N audit: does published work ALREADY IMPLY the exact MOCOSO high-modulus theorem?

**Date:** 2026-10-24. **Auditor:** @SOTA Research Auditor. **Scope:** published-theorem entailment and priority of the exact high-modulus *full index-lexicographic* O(n+p²(h+1)) result only. Source G3 at 53b2276c7ed450ba8c27adc0e1e02c1493b4e592; G6 at 00d7f1870bbb3d35e1e62da1057c76ff4dde712d; joint originality review draft PR #11. No production or source-theorem changes.

## Executive decision: direct prior theorem NOT ESTABLISHED; constructive derivation YES; global priority UNRESOLVED

The scoped MOCOSO theorem states: for arbitrary signed a[1..n], integer m with U/2<m<=U, U=n(n+1)/2, h=U-m, q=min(n,h), p=min(n,q+2), find the maximum-length selected indices under strict increasing consecutive value differences and index-sum divisible by m; return the **lexicographically least entire optimal index tuple**, permitting empty, in O(n+p²(h+1)) wide-word work and O(p²(h+1)) auxiliary words. For h<n this gives O(n+h³) work/space. Input and final witness excluded from auxiliary space, arbitrary-precision bit-time and Python RSS not claimed.

**Question:** Does an identified preexisting published mathematical result, by applying its stated hypotheses *without proving additional MOCOSO-specific lemmas*, yield this whole statement?

**Result: NO SUCH DIRECT IMPLICATION HAS BEEN ESTABLISHED BY THE SOURCES INSPECTED.** No original paper was found stating the same complete high-modulus theorem. An explicit **new derivation from previously known algorithmic methods** can prove it, but this is different from an already-published *full theorem*. Thus the earlier G6 claim that the precise theorem's originality was “resolved negatively” went beyond the evidence.

This finding does NOT establish firstness or theoretical significance. An elementary synthesis can be original in formulation yet insufficiently innovative for a theory venue. The strong claim “G3 invents a new general dynamic-programming primitive” is unsupported, because convex-edge ordering, exact integer-resource DP, and lex-path DP techniques predate MOCOSO.

## Exact original-source transfer matrix

| Work and public source | Result actually demonstrated/disclosed | Why it does NOT directly yield the complete MOCOSO theorem |
|---|---|---|
| Kluev (Dec. 18 2013), Longest convex subsequence, original public answer (NOT peer-reviewed), https://stackoverflow.com/questions/20664920/longest-convex-subsequence-in-an-array | O(N² log N) unweighted convex-subsequence length via pairs ordered by difference; decreasing second endpoint on ties. Provides some-witness backpointers and explicit O(N³)-edge pair-DAG | No selected-index modular/omitted-sum resource, no high-modulus suffix, no lex-least full index tuple under exact resource |
| Turner (2012), Variants of Shortest Path Problems, https://journals.lib.unb.ca/index.php/AOR/article/view/18312 | Publisher abstract explicitly notes equality-constrained resource path problems on acyclic graphs are pseudopolynomially solvable for fixed resource dimensions | No MOCOSO convex-edge sweep, no p/h definition and no O(p²h) bound or specified lex return |
| Camponogara & Shima (2010), resource-constrained longest paths on acyclic graphs, https://jucs.org/jucs_16_3/mobile_agent_routing_with.html | Original abstract records exact DP for a longest-resource-constrained path in a DAG | Not a sorted-convex-edge algorithm; no deficit/suffix full lex result |
| Axiotis & Tzamos (ICALP 2019), Capacitated Dynamic Programming: Faster Knapsack and Graph Algorithms, https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ICALP.2019.19 | Published graph-capacity setting explicitly constrains **number of edges/path length k**; generic O(k times graph-edge-count) DP; special graph results require concavity/Monge-style structure | MOCOSO h is **sum of omitted original positions**, NOT path hop count. No relevant required concavity/Monge hypothesis has been established; its graph theorem cannot be substituted verbatim for arbitrary omission weights or full lex tie |
| Bannai et al., Computing Longest Lyndon Subsequences and Longest Common Lyndon Subsequences (2023 online, Algorithmica vol. 2024), https://doi.org/10.1007/s00453-023-01125-z | Publisher full HTML derives algorithms for lexicographically minimal fixed-length subsequences in a different string setting, including compressed witness techniques | No strictly convex triple constraint, exact index-weight residue/deficit, or guaranteed corresponding work |
| Original MOCOSO edge_dp.py at 7595130fecb1a21dc8ca8823d9ee8d5d136af97a | Already implements sorted edge-difference + per-vertex/modulus-residue exact full-lex witness with bitmask tuples | Internal prior implementation, **NOT third-party published prior art**, no h-specific O(n+h³) statement; masks are n-bit and cannot silently be treated as constant log-sized words |

These sources demonstrate **prior methods**, not a verbatim prior MOCOSO theorem. Historical public algorithm disclosure (K13) counts for idea priority but must not be falsely called a peer-reviewed published paper.

## Formal implication stress test A: generic constrained pair-DAG is TOO SLOW

Construct pair vertices (i,j) for i<j<=p and arcs (i,j)->(j,k) when i<j<k and a[k]>2a[j]-a[i]. There are O(p²) vertices and up to Theta(p³) arcs (strictly superconvex values). Assign an omitted-index additive cost to each arc, plus initial/terminal charges, and require the total resource EXACTLY h.

A conventional exact-resource DAG DP over all arc/resource pairs needs **O(p³(h+1)) time**, O(p²(h+1)) state words. Existing generic resource-constrained path papers therefore do **not** furnish the missing factor p in G3's O(p²(h+1)) time merely by a black-box reduction. AT19 additionally uses a path-**length** capacity in the graph problem, not an exact arbitrary weighted-cost budget. Claiming AT19 alone directly subsumes G3 is an invalid theorem transfer.

## Formal implication stress test B: Kluev's sorted-edge algorithm supplies O(p²h) for LENGTH only after a resource lift

Elementary complement: every nonempty modular subsequence has selected-index sum exactly m because 0<sum<=U<2m. Its omitted positions sum h, so every omitted index <=q=min(n,h), and q+1..n are compulsory. All selected triples ending k>=q+3 are immutable suffix tests (one O(n) scan); remaining variable/crossing triples lie inside the prefix 1..p, p=min(n,q+2).

Define W(t)=t(t+1)/2, omission gap g(j,k)=W(min(k-1,q))-W(min(j,q)) between consecutive selected core endpoints j<k. Ban any pair edge skipping an index >q; charge omissions before first selected and after the last selected; exact cost h represents exactly the nonempty modular condition.

K13's sorted-difference events can now each scan h+1 possible exact omitted costs. Equal differences are sorted by decreasing destination to forbid chaining equal differences. Thus a **new explicit DP construction from older ideas** yields **exact optimal LENGTH** within O(n+p² log(p+1)+p²(h+1)) word time and O(p²+p(h+1)) auxiliary words. Because p<=h+2, sorting is absorbed by O(p²(h+1)); for h<n this is O(n+h³) time and O(h²) space.

**Crucial distinction:** this is ONLY an optimum-length recurrence. Greedy lex reconstruction by p separately forced-inclusion/exclusion length queries uses O(n+p³(h+1)+p³ log(p+1)) time, O(p²+p(h+1)) working words, namely O(n+h⁴)/O(h²) for h<n. The published K13 answer does NOT yield *global exact lex witness* in O(n+h³) by its stated theorem; its generic “a longest witness” pointers are not equivalent to canonical lex order.

This exposes an exact gap in any argument that a direct citation of K13 already implies our entire theorem.

## Formal implication stress test C: reverse DP achieves full lex in O(p²h), but with added derivation

The actual G3-style reverse state F(i,j,r) stores best further selected-core length after last chosen pair i<j, under EXACT omitted-sum remainder r, plus one canonical successor pointer. A legal extension has successor k>j, satisfies a[k]>2a[j]-a[i], pays gap g(j,k), and returns 1+F(j,k,r-g(j,k)). A zero extension is allowed only at the correct terminal/mandatory-suffix completion.

For a fixed second endpoint j, sort predecessors i in ascending a[i]; admissibility threshold 2a[j]-a[i] decreases. Sort candidate successors k by decreasing a[k]. Each successor becomes admissible at most once for this j; insert its h+1 child resource states into a best-by-budget array only once. Every predecessor row is a copy of this array. Summed over all j, at most O(p²) successor insertions and O(p²) row copies each cost O(h+1), yielding O(p²(h+1)) word work and O(p²(h+1)) saved table/pointer words, plus O(n) immutable suffix scanning and output reconstruction.

**Exact lex at no extra asymptotic work:** within a fixed state (i,j,r), when extension length ties, prefer the **smallest FIRST successor index k**. Two tied tails with the same k use an identical child state, whose suffix pointer is already canonical by descending-j induction. Global root compares first pairs in lex order, and appends the identical compulsory suffix. Singleton and empty cases are separate. Thus complete lex optimality is proved using one constant-sized successor pointer per DP entry; no O(p)-length witness comparison and no p-bit witness-as-word assumption are needed.

This is a correct human-checkable conditional derivation in G3, but **no inspected earlier publication states this integrated high-modulus reduction, transition compression and lex-pointer guarantee as its own theorem**. Such a derivation may still be considered mathematically routine by expert reviewers; “extra lemmas needed” is not itself evidence of publication-level novelty.

## Claim-by-claim dispositions (not a global novelty score)

| Question | Auditor determination |
|---|---|
| Published convex-subsequence sorted-edge primitive exists? | **YES**, public algorithm disclosure K13 (not peer-reviewed) |
| Published exact integer-resource-constrained DAG DP exists? | **YES**, general setting in CS10/T12 |
| AT19 theorem literally implies exact weighted omitted-index h and O(p²h)? | **NO DIRECT TRANSFER SHOWN**, capacity is path length, missing graph hypotheses |
| Literature theorem found explicitly covering strict triples + modular selected INDEX sum + full lex + this h/p bound? | **NO SUCH SOURCE IDENTIFIED** (NOT “proved none exists”) |
| Can the exact theorem be derived with *additional* application-specific lemmas using known DP ideas? | **YES**, proof reconstruction above; finite oracle verification was separately completed in draft PR #11 |
| Does the existence of prior building blocks disprove novelty of the precise combined theorem? | **NO** |
| Is the entire theorem historically first or significant enough for publication? | **UNRESOLVED**, requires targeted scholarly priority/significance assessment |

**NARROW G6-N VERDICT:** the allegation that this **particular high-modulus, full-index-lex complexity theorem** was already proved or is directly implied by a cited earlier theorem is **not supported by our inspected literature**. The converse claim of firstness is also unsupported. Keep direct-publication-duplication status **UNRESOLVED / NO MATCH IDENTIFIED**, while classify the general algorithmic primitives as **ESTABLISHED PRIOR ART**.

## Search scope and limitations

Public literature searches through 2026-10-24 used exact/coined names AND non-coined formulations: convex subsequence + modular, index sum, resource, budget, lex; sorted-edge difference sequences; acyclic longest paths with exact equality resource; path lex-tie DP. Searched primary source lines/abstracts. Original K13 complete answer inspected; ICALP 2019 original publisher and paper PDF text inspected, with rendered PDF screenshots attempted unsuccessfully (cache miss); T12 and CS10 primary publisher *abstracts* (NOT their complete mathematical bodies); Bannai et al full publisher HTML lex DP text. Other publications and unindexed literature could exist. This is **not an exhaustive bibliometric search or external human theorem review**.

The dispositive falsifier would be an earlier theorem plus an exact parameter-preserving reduction certifying: signed arbitrary values, strict selected triples, equal omitted-index sum h, compulsory boundary/crossing triples, complete full lex witness without p-bit word cheats, and O(n+p²(h+1)) word time/O(p²(h+1)) words. No such citation/reduction was produced.

**Scientific direction:** do not reject the theorem merely because standard ideas are used. Do not assert it is first. Preserve the precise new scoped corollary as a candidate research result and submit it to an outside algorithmist with this matrix; separately investigate whether improved lex time-space bounds yield a stronger theory contribution. This file makes no publication readiness claim and does not change the G6 non-novelty-independent blockers.
