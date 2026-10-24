"""G7 research-only full-lex high-modulus sorted-edge DP with compact omissions.

Regime: U/2 < m <= U, h=U-m<n, p=min(n,h+2).
Time O(n+p^2*(h+1)*(1+sqrt(h+1))) wide-word operations;
auxiliary space O(p^2+p*(h+1)*(1+sqrt(h+1))) wide words.
Input/output excluded, numeric operands must fit the stated wide-word model.
This is a Pareto composition of established methods, not a priority claim.
"""
from __future__ import annotations
from math import isqrt


def solve_compact_lex(a, m):
    n = len(a)
    U = n * (n + 1) // 2
    if type(m) is not int or m < 2 or not U // 2 < m <= U:
        raise ValueError("requires integer m>=2 and U/2<m<=U")
    if any(type(x) is not int for x in a):
        raise ValueError("arbitrary signed integer values required")
    h = U - m
    if h >= n:
        raise ValueError("compact Pareto algorithm requires h<n")
    q = h
    p = min(n, q + 2)

    for k in range(q + 3, n + 1):
        if a[k-1] + a[k-3] <= 2*a[k-2]:
            return ()

    def W(t):
        return t * (t + 1) // 2

    # DP for the CURRENT edge-difference threshold:
    # dp[j][r] = (max prefix cardinality, lex-largest omitted tuple)
    # of a convex selected prefix through j omitting exact sum r.
    # Comparing omitted tuples in descending lex order is exactly
    # comparing equal-length selected prefixes in ascending lex order.
    dp = [[None] * (h+1) for _ in range(p+1)]
    for i in range(1, min(p, q+1)+1):
        r = W(i-1)
        if r <= h:
            dp[i][r] = (1, tuple(range(1, i)))

    events = sorted((a[j-1]-a[i-1], -j, i, j)
                    for i in range(1,p) for j in range(i+1,p+1))
    for _, _, i, j in events:
        if (i <= q and j >= q+2) or (i >= q+1 and j > i+1):
            continue  # Would skip a compulsory suffix index.
        g = W(min(j-1,q)) - W(min(i,q))
        if g > h:
            continue
        missing = tuple(range(i+1, min(j,q+1)))
        for r in range(h-g+1):
            state = dp[i][r]
            if state is None:
                continue
            candidate = (state[0] + 1, state[1] + missing)
            old = dp[j][r+g]
            if old is None or candidate > old:
                dp[j][r+g] = candidate

    # h<n implies p>q; EVERY nonempty valid witness contains p
    # and every index >p, hence a single target state dp[p][h].
    final = dp[p][h]
    if final is None:
        return ()
    omitted = set(final[1])
    selected = tuple(i for i in range(1,n+1) if i not in omitted)
    assert len(selected) == final[0] + n-p
    assert sum(selected) == m
    assert len(final[1]) <= (isqrt(8*h+1)-1)//2
    assert all(a[x-1]+a[z-1] > 2*a[y-1]
               for x,y,z in zip(selected, selected[1:], selected[2:]))
    return selected
