# Mechanism and claim map — 2026-10-29

## Sources inspected

1. Thomas M. Cover, *Enumerative Source Encoding*, IEEE Transactions on
   Information Theory 19(1), 73–77 (1973), Proposition 1 and inverse algorithm.
   https://isl.stanford.edu/~cover/papers/transIT/0073cove.pdf
   DOI https://doi.org/10.1109/TIT.1973.1054929
   Establishes the lexicographic rank as a sum of prefix-completion counts.
   This directly supplies G15's generic ranking ingredient; do not claim it
   as a new compression or canonicalization principle.
2. Evgeny Kluev, public technical answer (18 December 2013), steps 1–6.
   https://stackoverflow.com/questions/20664920/longest-convex-subsequence-in-an-array
   Supplies difference-sorted convex-subsequence DP and descending endpoint
   ordering for equal differences. A primary disclosure, not peer review.
3. Jörg Arndt, *Subset-lex: did we miss an order?*, arXiv:1405.6503v4.
   https://www.jjj.de/pub/arndt-subset-lex.pdf
   Section 1 distinguishes subset-list order from incidence-string order;
   Section 5.2 addresses distinct-part partitions. This is relevant ancestry,
   not evidence for G15's particular complexity or implementation.
4. Repository G10 proof and G14 code pinned at
   ccc8451911cc9d67f887bc6826c29bcfb6c148f3.
   Internal baselines share algorithmic ancestry; they are not independent
   mathematical referees. Selected-mask tests are a separate formulation.

## Research target and alternatives

- Repeated fixed-omission certificates: rejected as the main direction;
  they do not remove the full solver's reconstruction bottleneck.
- Full positional bitmask labels: valid common technique (already present
  in `edge_dp.py`), but require O(h) bits in the small-deficit core.
- Persistent comparison trees: plausible different time-space tradeoff,
  not implemented or claimed superior here.
- Exact-family enumerative rank: selected; O(sqrt(h+1)) bits, constant
  count-table operations per gap, additive continuation invariant, one sweep.

The bridge assumption was that a rank of the *entire* omission family could
be propagated additively from endpoint/resource states. The telescoping
identity and prefix-interval invariant prove that assumption; ranking alone
would not establish it. Integer width is explicitly charged.

## Claims and states

| Claim | Evidence | Status / limitation |
|---|---|---|
| Generic enumerative lex rank | Cover Proposition 1 | PRIOR_ART_FOUND |
| Difference-sorted strict-convex sweep | Kluev steps 1–6 | PRIOR_ART_FOUND |
| Telescoped rank transition preserves canonical dominance | THEOREM.md §§2–5 | Complete human-checkable derivation; not formal checking |
| Complete high-modulus solver including h>=n | THEOREM.md; selected-mask tests | Proof and finite executable checks are separate evidence |
| Better worst-case time than G10 in shared domain | Explicit multiword theorem | Potentially larger space; width condition cannot be omitted |
| Practical superiority | Frozen 935-case benchmark | Pending actual execution; report losses |
| Worldwide SOTA / priority | No exhaustive field comparison | UNRESOLVED; not asserted |

## Search boundary

Two web engines were queried for convex subsequences with modular constraints,
lexicographic paths, ranking exact-sum subsets and distinct-part partitions,
and Cover enumerative encoding. Primary full-text follow-up was performed
for the three sources above. The broad rank mechanism has clear prior art.
No inference of novelty is drawn from the absence of an exact matching title.
The possible research contribution is the specialized composition, its
resource accounting and measured crossover, subject to independent review.
