# Search log

Date: 2026-10-24. Thirty executed queries across two search engines, plus direct
primary-source opens, in-document searches, and citation follow-up. This records
this follow-up investigation; it does not count the earlier PR16 searches as new.
Searches are reproducible strings, not a claim that search rankings are stable.
Each batch's outcome summarizes the combined returned results.

## Batch 1 — system2

- `"convex subsequence" "modular"`
- `"convex subsequence" "lexicographic"`
- `"longest convex subsequence" algorithm difference`
- `"increasing paths" "resource constrained" algorithm`

Direct terminology and event-path reformulations; did not identify an exact full theorem.

## Batch 2 — system1

- `"longest convex subsequence" algorithm paper`
- `"temporal paths" "resource" constrained`
- `"lexicographic" "witness" "self-reduction" binary search`

Verified base-problem leads and expanded into temporal paths and lexicographic self-reduction.

## Batch 3 — system2

- `temporal graphs optimal paths edge stream Wu 2014 time complexity`
- `"resource constrained" "temporal" shortest path algorithm`
- `"A complexity theory for hard enumeration problems" pdf`
- `"Hirschberg" "lexicographically" shortest path`

Located Wu's primary PDF and an accessible full preprint of Creignou et al.; screened Hirschberg-related results.

## Batch 4 — system1

- `lexicographically smallest optimal path linear space dynamic programming Hirschberg`
- `finding witnesses decision oracle k log n self reduction sparse`
- `"convex subsequence" "sum" "indices"`
- `"Path problems in temporal graphs" pdf`

Located Björklund–Kaski–Kowalik's sparse witness extraction and Meeks's citing work; this was the principal new overlap.

## Batch 5 — system2

- `"Fast Witness Extraction" "lexicographic"`
- `"convex subsequence" "modulo"`
- `"convex subsequence" "deficit"`
- `site:pixel-druid.com "Longest Convex Subsequence"`

Checked whether sparse extraction was explicitly canonical; screened Pixel Druid's cubic recurrence and unrelated modulo/counting hits.

## Batch 6 — system1

- `"convex subsequence" "index sum"`
- `"convex subsequence" "modular" algorithm`
- `"witness extraction" "lexicographically"`
- `"increasing paths" "resource" dynamic programming`

Second-engine verification of exact index-sum/modular terminology; results largely base exercises or different problems.

## Batch 7 — system2

- `"lexicographically" "inclusion oracle"`
- `"lexicographically" "group testing" witness`
- `"temporal" "exact" "resource constrained" path`

Inclusion-oracle/group-testing terminology cross-check; temporal-resource query returned mostly project scheduling, not this path theorem.

## Batch 8 — system1

- `"convex subsequence" algorithm deficit lexicographic`
- `"modular convex subsequence"`
- `"longest convex subsequence" "resource"`
- `"Fast Witness Extraction Using a Decision Oracle" ESA 2014 DOI`

Closing exact-phrase search and independent verification of ESA 2014 metadata through Springer and the author's institution.

## Direct source follow-up

The version-specific URLs and inspected theorem locations are in [SOURCES.md](SOURCES.md).
The decisive positive links are Kluev's actual numbered algorithm, Turner's
journal recurrence/Theorem 2, BKK's full-version Theorem 1/Algorithm 1, Meeks's
oracle definitions, Creignou v2 Proposition 5, and Wu's temporal expansion.
BKK's 2014 conference date was cross-checked against its full-version opening
note, Springer DOI record, and Aalto's publication record; the full theorem was
read in the 2015 version. The target commit's author and committer timestamps
are 24 October 2026. A Git timestamp alone is not an authenticated first-public-
disclosure certificate.

The forward citation from BKK to Meeks was followed. Backward group-testing,
Fellows–Langston, and Lawler references were recorded as leads; their original
proofs were not retrieved and are not treated as independently verified theorem
sources. This explicitly limits citation-graph coverage.

## Screening and limits

- No result identified the exact full modular/deficit/canonical theorem.
- Geometric convexity, convex hulls, extremal existence theorems, counting modulo
  a number, project scheduling, and cryptographic witness extraction were excluded
  when their definitions or oracle models differed.
- The previous journal-access limitation for Creignou's proof was resolved by
  reading the author preprint. Journal/preprint proposition numbers are not
  silently interchanged.
- No subscription bibliographic database, exhaustive citing-paper export,
  non-English corpus review, author correspondence, or external referee report
  was obtained. Google Scholar, MathSciNet, and zbMATH were not directly searched
  through their own interfaces in this investigation.
- S7, S9, and the textbook portion of S10 are explicitly carried-forward source
  checks from the earlier audit; they are not presented as newly discovered papers.

The stopping point is evidential: the strongest retrieved overlaps were read,
the proposed full implication was written out, and the main black-box shortcuts
were either justified or falsified. Absolute absence from all literature cannot
be inferred from this search.
