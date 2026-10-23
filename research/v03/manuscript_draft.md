# A high-modulus specialization for modular convex subsequences — PREPRINT WORKING DRAFT

**DO NOT CITE AS A PUBLISHED OR NOVEL RESULT.** This is a candidate mathematical derivation awaiting independent peer review, systematic prior-art screening, raw comparative runs, and release gates M0–M6. Prepared 2026-10-23.

## Abstract (provisional)

For a finite signed integer sequence, find the longest index subsequence with strictly increasing consecutive value differences and a selected-index sum divisible by m, breaking ties by the lexicographically least witness. We examine the regime U/2<m<=U with U=n(n+1)/2. Complementing selected indices yields an omitted-index distinct-part partition of h=U-m. A bounded subset-sum reachability table generates only complete partitions, and suffix-local convexity limits each candidate test to O(q) indices with q=min(n,h). We derive an arithmetic word-operation bound O(n+qh+qP_d(h)) and O(qh+q) auxiliary words, and observe P_d(h)<=exp(2 sqrt h). The method remains experimental; novelty relative to prior partition enumeration and constrained-path literature is unresolved.

## Scope and relation to predecessors

Kluev's 2013 unconstrained longest-convex-subsequence edge ordering and classical cubic pair-index recurrence are acknowledged antecedents. Barrett–Jacob–Marathe's language-constrained paths and classical Euler distinct-part counting establish broad methodological context. The present special case does not claim that ordered edges, automaton products, subset-sum pruning or partition functions themselves are new.

## Candidate formal result

See t1_deficit_proof.md for the full definitions, complement proof, suffix-locality equivalence, reachability recurrence, enumeration charging argument, lex witness proof, upper bound and arithmetic/bit-model qualifications. The method is only promised to operate in U/2<m<=U and does not replace the general m solver.

## Experimental protocol

Use tests/test_v03_deficit.py and experiments/v03/benchmark.py. Tiny cases use an independently constructed all-subsets oracle. The benchmark includes original v0.2 solve, a mask-specific baseline, independent bitmask edge DP and modular/lex tuple edge adaptation. All raw measurements, failure statuses and SHA256 provenance must be retained. Local finite testing to date is not a claim of cross-environment superiority.

## Limitations and open problems

O(qh) reachability memory can be prohibitive when h is large. Python arbitrary-precision value comparisons and process memory are not covered by a unit-cost word bound. A proposed reduction in candidate enumeration might already follow from standard partition output-sensitive generation. Open: complete novelty audit; independently reviewed proof; actual paired performance on two environments; genuinely improved persistent exact-lex edge DP without mask-size costs.

## References (initial; expand after bibliographic screening)

1. Evgeny Kluev (2013), Longest convex subsequence in an array, Stack Overflow: https://stackoverflow.com/questions/20664920/longest-convex-subsequence-in-an-array
2. Illinois CS374, discussion 07b, longest convex subsequence: https://courses.physics.illinois.edu/cs374/fa2020/labs/sol/lab_07_b_sol.pdf
3. Chris Barrett, Riko Jacob, Madhav Marathe (2000), Formal-Language-Constrained Path Problems, SIAM Journal on Computing 30(3), 809–837. DOI: 10.1137/S0097539798337716
4. OEIS A000009, partitions into distinct parts; cites George E. Andrews, The Theory of Partitions: https://oeis.org/A000009
5. Solving String Problems on Graphs Using the Labeled Direct Product (2022): https://link.springer.com/article/10.1007/s00453-022-00989-x

## Release decision

No 'first', SOTA, superiority or publication-ready claim permitted until M0 through M6 satisfy the original handoff's acceptance criteria. A successful isolated research PR is not a production algorithm release.
