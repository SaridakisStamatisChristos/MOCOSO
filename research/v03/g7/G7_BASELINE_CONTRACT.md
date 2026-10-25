# G7.0 baseline, exact model and immutable source ledger

Date 2026-10-24. Parent: unmerged draft PR #12, exact SHA \`4016049054de743a12307aad70822e0423e3a3f7\`. The parent was checked live before branching. PR #11 parent \`eda773e01e1a2a21aa1e26631fc36c0173a37359\` and both drafts remain unmerged.

## Objective and model

For signed integer values a[1..n], m>=2, a nonempty increasing index tuple I is feasible if its selected-index sum is 0 mod m and its selected successive value differences are strictly increasing. Return a maximum-cardinality feasible I, breaking ties by lexicographically smallest **entire** tuple. Empty is a fallback. Define U=n(n+1)/2, U/2<m<=U, h=U-m, q=min(n,h), p=min(n,q+2).

For any nonempty solution 0<sum(I)<=U<2m, so sum(I)=m and its omitted-index sum is exactly h. Every omitted index is at most q; all indices q+1..n are compulsory. Each consecutive selected triple ending >=q+3 is fixed and checkable once in O(n); all earlier/crossing triples occur in 1..p.

The **G7 compact-omission implementation is specifically for h<n**, hence q=h, p=min(n,h+2)>q. Any nonempty solution contains p and the suffix p+1..n. Singleton solutions are permitted, e.g. n=2,m=2.

Work is counted in a *wide-word abstraction* in which all signed input values, intermediate differences, indices, DP counters and table addresses fit single charged words. The same precondition applies to G3. A high-bit-count Python integer does not generally cost O(1) time or one standard machine word. An omitted index is stored as an individual word, **never packed into an uncharged huge integer**. DP entry counts exclude input and the final returned tuple; Python runtime overhead and RSS are not predicted by asymptotic word bounds.

## Frozen baseline comparators

| Source | Time (h<n) | Auxiliary words (h<n) | Witness |
|---|---|---|---|
| T1 omission enumerator, v0.3 prior branch | O(n+qh+q D_q(h)) candidate-bound | O(qh+q) | exact full lex; potentially superpolynomial deficit enumeration |
| G3 reverse-pair F(i,j,r), \`research/v03/prepaper/g3_polynomial_deficit_theorem.md\`, frozen theorem commit \`53b2276c7ed450ba8c27adc0e1e02c1493b4e592\` | O(n+(h+1)^3) | O((h+1)^3) | exact full lex |
| PR #11 sorted-edge exact resource, \`experiments/v03/edge_budget_lift.py\` | O(n+(h+1)^3) | O((h+1)^2) | **length only** |
| PR #11 forced-choice recomputation | O(n+(h+1)^4) | O((h+1)^2) | exact full lex |
| G7 explicit omission-list witness (this PR) | O(n+(h+1)^(7/2)) | O((h+1)^(5/2)) | exact full lex |

G7 is **incomparable** to G3 in time/space: less storage for a slower worst-case time. It is also incomparable to PR #11's quartic/quadratic full-lex point. It does not establish the originally requested cubic-time/quadratic-space bound.

Historical \`edge_dp.py\` at \`7595130fecb1a21dc8ca8823d9ee8d5d136af97a\` already has sorted-edge/full-lex bitmask states in the unrestricted setting; this is internal antecedent. G6 audit commit \`00d7f1870bbb3d35e1e62da1057c76ff4dde712d\` and PR #12 are not overridden. Production \`modconvex.py\` is frozen.

## Differential evidence

Local standalone independent selected-subset oracle (not a DP or omission enumerator): 21,321 ternary-alphabet high-modulus h<n cases, 145,632 four-valued signed-alphabet cases, 1,000 deterministic giant-signed random cases, and focused suffix/equality cases succeeded on Linux CPython 3.13.5. The local demonstration files and committed CI code have the same algorithm but are separate transcriptions: **do not assert binary-identical hashes**. The committed tests add frozen G3 comparison for the 1,000 random inputs and superconvex controls; CI status is separately checked.
