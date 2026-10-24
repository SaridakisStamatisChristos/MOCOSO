# Version-specific source registry

Inspected on 2026-10-24. Publication dates below come from the documents or
publisher/author records, not search-engine crawl timestamps. The compact
descriptions distinguish source statements from our implications in the report.

| ID | Primary source and date | Precisely inspected locus / access |
|---|---|---|
| S1 | Evgeny Kluev, [answer to Longest convex subsequence in an array](https://stackoverflow.com/questions/20664920/longest-convex-subsequence-in-an-array), posted 18 Dec 2013, edited 20 Dec 2013 | Full answer; numbered sweep steps, equal-difference ordering, back-pointer discussion. Public technical disclosure. |
| S2 | Lara Turner, [Variants of the Shortest Path Problem](https://journals.lib.unb.ca/index.php/AOR/article/download/18312/20525/24773), Algorithmic Operations Research 6 (2011), 91–104; [online record](https://journals.lib.unb.ca/index.php/AOR/article/view/18312) 3 Jan 2012 | Journal PDF, p.96, recurrence (23), Theorem 2. Arbitrary real edge costs and acyclic graph setting; equality resource bounds. |
| S3 | Andreas Björklund, Petteri Kaski, Łukasz Kowalik, [Fast Witness Extraction Using a Decision Oracle](https://doi.org/10.1007/978-3-662-44777-2_13), ESA 2014, LNCS 8737, 149–160; [full arXiv v1](https://arxiv.org/html/1508.03572v1), 14 Aug 2015 | Full-version §1, Theorem 1, §2 Algorithm 1 and query analysis; related-work references. [Author institution record](https://research.aalto.fi/en/publications/fast-witness-extraction-using-a-decision-oracle/) corroborates 2014 publication. The exact numbered theorem was read in the 2015 full version, not assumed to have identical numbering in the conference chapter. |
| S4 | Kitty Meeks, [Randomised enumeration of small witnesses using a decision oracle](https://arxiv.org/html/1509.05572v4), inspected v4, 4 Jan 2018; arXiv initial submission 2015 | §1 oracle definitions, sparse-extraction discussion, §3 distinction between general inclusion and extension, references. A forward citation of S3. |
| S5 | Nadia Creignou, Markus Kröll, Reinhard Pichler, Sebastian Skritek, Heribert Vollmer, [A Complexity Theory for Hard Enumeration Problems, arXiv v2](https://arxiv.org/pdf/1610.05493v2), 24 Oct 2017; [journal version](https://doi.org/10.1016/j.dam.2019.02.025), Discrete Applied Mathematics 268 (2019), 191–209 | Directly accessible preprint §3.2, printed p.8 Proposition 5 and proof; p.9 Definition 3 and Proposition 6. This closes the earlier journal-access gap for the standard prefix argument. Version-specific numbering is retained. |
| S6 | Huanhuan Wu, James Cheng, Silu Huang, Yiping Ke, Yi Lu, Yanyan Xu, [Path Problems in Temporal Graphs](https://www.vldb.org/pvldb/vol7/p721-wu.pdf), PVLDB 7(9), 721–732 (2014), DOI 10.14778/2732939.2732945 | §4 temporal objectives and §5, printed pp.728–729, arrival/departure vertex copies and waiting/travel edges. The exact-resource/negative-cost adaptation in our report is our deduction. |
| S7 | André Große, Jörg Rothe, Gerd Wechsung, [A Note on the Complexity of Computing the Smallest Four-Coloring of Planar Graphs](https://arxiv.org/pdf/cs/0106045), initial 2001, inspected v2 7 Feb 2006 | §3, printed p.5, discussion after Definition 3.2. Previously inspected in PR16; retained as supporting ancestry rather than newly discovered evidence. |
| S8 | Logan Nye, [Universal Hirschberg for Width Bounded Dynamic Programs](https://arxiv.org/html/2512.10132v1), 10 Dec 2025 | Theorem 1, model and tie convention. It concerns a fixed local tie rule and polynomial total time. Not independently certified, and not required by our positive proof. |
| S9 | Ce Jin, Nikhil Vyas, Ryan Williams, [Fast Low-Space Algorithms for Subset Sum](https://arxiv.org/abs/2011.03819), 2020 preprint / [SODA 2021](https://doi.org/10.1137/1.9781611976465.106) | Problem definition and headline bounds, carried forward from PR16 screening. No full proof review or claimed transfer to the convex complement constraint. |
| S10 | Jeff Erickson, [Algorithms, dynamic-programming chapter](https://jeffe.cs.illinois.edu/teaching/algorithms/book/03-dynprog.pdf), 2019 textbook | Printed p.126, convex-subsequence exercise (f), previously checked. Also checked [Illinois CS374 Fall 2020 lab solution](https://courses.grainger.illinois.edu/cs374/fa2020/labs/sol/lab_07_a_sol.pdf), final subsection's pair-state recurrence. |

Additional discovery/screening records:

- [Truant, Longest Convex Subsequence, 1 February 2014](https://algnotes.wordpress.com/2014/02/01/longest-convex-subsequence/): alternate DP discussion and a link back to Stack Overflow. Not an independent source for priority over S1.
- [Pixel Druid, Longest Convex Subsequence DP](https://pixel-druid.com/articles/longest-convex-subsequence-dp), page creation 24 September 2021, last edit 30 May 2022: displayed triple-loop recurrence is cubic, not a stronger quadratic resource algorithm. Its introductory all-triples wording is stronger than its consecutive-triple recurrence; not used as a proof source.
- S3 traces its bisection ancestry to Du and Hwang, *Competitive group testing*, Discrete Applied Mathematics 45(3) (1993), 221–232, and its search/decision background to Fellows and Langston (STOC 1989). **Bibliographic leads only:** original proofs not retrieved in this pass; no exact theorem attributed to them here.
- S4 traces interval-oracle enumeration to Lawler, *A procedure for computing the k best solutions to discrete optimization problems and its application to the shortest path problem*, Management Science 18(7) (1972), 401–405. **Citation-chain lead only**, not independently full-text verified here.

The investigation followed S3 forward to S4 and backward through its explicit
references. It did not exhaust all citing papers, subscription indexes, languages,
theses, code archives, or unpublished work. This is why exact global priority
cannot be certified despite a concrete overlap verdict.
