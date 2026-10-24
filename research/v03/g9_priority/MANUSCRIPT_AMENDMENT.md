# Concrete amendment for manuscript PR17

Status: **proposed replacement text, not yet integrated into the existing PDF,
DOCX, TeX, or manuscript.md**. Those artifacts are preserved as the earlier
snapshot. This file makes the scientific consequence of the priority investigation
reviewable without silently leaving generated exports out of sync.

Replace the related-work/contribution discussion of sparse reconstruction with:

> Sparse extraction from a decision oracle is established prior work.
> Björklund, Kaski, and Kowalik (ESA 2014; full version 2015) give deterministic
> extraction using O(k log N) inclusion-oracle queries. Their unrestricted
> partition procedure selects an arbitrary witness, rather than the particular
> lexicographic optimum required here. We use an ordered threshold self-reduction
> and prove that it preserves the complete original-index order. The inclusion
> and extension interfaces must be distinguished, as emphasized by Meeks:
> an efficient existence oracle does not automatically answer every forced-prefix
> query. In the present problem the necessary constrained score queries are
> available through the resource-lifted sweep. Alternatively, an inclusion-only
> ordered deletion maintains that its chosen prefix is essential to every
> remaining optimum, giving the same bound.

Add this comparison after the event/resource discussion:

> Kluev's 2013 public disclosure already supplies the difference-sorted endpoint
> sweep and descending-destination tie rule. Exact-resource DAG dynamic
> programming is also standard, for example in Turner. A temporal expansion of
> the kind described by Wu et al. gives an alternative path representation, but
> an explicit resource table over all expanded events would retain an extra
> logarithmic factor in space. The rolling endpoint representation avoids that
> storage. Our contribution is the specialized deficit reduction, legal-event
> count, and complete accounting of their combination with canonical extraction;
> we do not claim a new generic sweep or sparse-witness extraction method.

Use this bounded originality statement:

> We did not identify a prior source stating this exact combined theorem in the
> documented search completed on 24 October 2026. The result is an incremental
> specialization of established mechanisms. This search does not establish
> worldwide firstness or asymptotic optimality.

Use the directly inspected **Creignou et al. arXiv v2, §3.2, Proposition 5** for
the prefix-enumeration claim. Do not transfer proposition numbering between
preprint and journal versions without checking the relevant version.

Integrate `additions.bib` when revising the manuscript, then rebuild and visually
check every exported format. No new benchmark or lower-bound claim follows from
this literature investigation.
