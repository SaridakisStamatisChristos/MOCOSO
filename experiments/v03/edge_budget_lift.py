"""Independent 2013 sorted-convex-edge sweep + exact omission-budget DP.

Research-only PRIOR-ART COMPOSITION CONTROL, not a claim of novelty or an
optimized production implementation. Does not import G3, G4, v0.2 or T1.

Given high-modulus m, h=U-m, q=min(n,h), p=min(n,q+2):
* optimum LENGTH in O(n+p^2(h+1)+p^2 log(p+1)) wide-word work,
  O(p(h+1)+p^2) auxiliary words.
* full LEX-MIN optimal index tuple via standard feasibility self-reduction
  in O(n+p^3(h+1)+p^3 log(p+1)) work and the SAME auxiliary space.
  Returned O(n) witness and read-only input are excluded from auxiliary.
This word model must hold arbitrary signed input/intermediate differences;
Python big-integer time and hard memory ceilings are not asserted.

This independent derivation tests the originality boundary: both principal
techniques (ordered convex edges and resource-state DP) predate MOCOSO.
"""
from __future__ import annotations


def _check(a, m):
    if type(m) is not int or m < 2 or any(type(v) is not int for v in a):
        raise ValueError("input must be signed integers, modulus integer >=2")
    n = len(a)
    U = n * (n + 1) // 2
    if not (U < 2*m and m <= U):
        raise ValueError("requires U/2 < m <= U")
    h = U - m
    q = min(n, h)
    p = min(n, q + 2)
    return n, h, q, p


def best_length(a, m, *, must_select=(), must_omit=()):
    """Return optimum length with mandatory choices. -1 means impossible.

    The empty witness satisfies the constraints only if must_select is empty.
    Constraints apply to the full selected index tuple, not its complement.
    """
    n, h, q, p = _check(a, m)
    select = frozenset(must_select)
    omit = frozenset(must_omit)
    if any(type(i) is not int or not 1 <= i <= n
           for i in select | omit):
        raise ValueError("forced indices must be integers in [1,n]")
    if select & omit:
        return -1
    # Any nonempty modular witness must select q+1..n.
    if any(t > q for t in omit):
        return 0 if not select else -1

    # Fixed immutable suffix: every admissible nonempty witness has these.
    for k in range(q + 3, n + 1):
        if a[k-1] + a[k-3] <= 2 * a[k-2]:
            return 0 if not select else -1

    W = lambda t: t * (t + 1) // 2

    mandatory_prefix = [0] * (p + 1)
    for i in range(1, p + 1):
        mandatory_prefix[i] = mandatory_prefix[i - 1] + (i in select)

    # dp[j][s] is best selected-core path length ending at j, resource s,
    # with LAST EDGE DIFFERENCE strictly below the current event difference.
    # Incoming events processed in increasing difference, tied edges in
    # DECREASING second index, preventing same-difference chaining.
    dp = [[-1] * (h + 1) for _ in range(p + 1)]
    for i in range(1, p + 1):
        if i > q + 1 or i in omit or mandatory_prefix[i - 1]:
            continue
        s = W(min(i - 1, q))
        if s <= h:
            dp[i][s] = 1

    events = sorted(
        (a[j-1] - a[i-1], -j, i, j)
        for i in range(1, p)
        for j in range(i + 1, p + 1)
    )
    for _, _, i, j in events:
        if i in omit or j in omit:
            continue
        if mandatory_prefix[j-1] != mandatory_prefix[i]:
            continue  # An explicitly required position is skipped.
        if ((i <= q and j >= q + 2) or
                (i >= q + 1 and j > i + 1)):
            continue  # Immutable mandatory suffix index is skipped.
        gap = W(min(j-1, q)) - W(min(i, q))
        for r in range(h - gap + 1):
            predecessor = dp[i][r]
            if predecessor > 0 and predecessor + 1 > dp[j][r + gap]:
                dp[j][r + gap] = predecessor + 1

    answer = -1
    for j in range(1, p + 1):
        if mandatory_prefix[p] != mandatory_prefix[j]:
            continue
        if p > q:
            if j != p:
                continue
            r = h
        else:
            r = h - (W(q) - W(j))
        if 0 <= r <= h and dp[j][r] > 0:
            answer = max(answer, dp[j][r] + n - p)
    if answer < 0 and not select:
        return 0
    return answer


def solve_lex_by_recomputation(a, m):
    """Exact full lex-min witness from repeated constrained length oracles.

    Among equal-cardinality selected tuples, the first differing membership
    favors including the smaller index. Greedily try to include each mutable
    index iff one globally optimal completion still exists.
    """
    n, h, q, p = _check(a, m)
    target = best_length(a, m)
    if target == 0:
        return ()
    if target < 0:
        raise AssertionError("unconstrained empty witness unavailable")
    included, excluded = set(), set()
    for i in range(1, p + 1):
        if i > q:
            included.add(i)
            continue
        if best_length(a, m, must_select=included | {i},
                       must_omit=excluded) == target:
            included.add(i)
        else:
            excluded.add(i)
    witness = tuple(sorted(included | set(range(p + 1, n + 1))))
    assert len(witness) == target
    assert sum(witness) == m
    assert all(
        a[i-1] + a[k-1] > 2 * a[j-1]
        for i, j, k in zip(witness, witness[1:], witness[2:])
    )
    return witness
