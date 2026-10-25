"""G9 research-only full-lex solver with QUADRATIC auxiliary wide words.

For U/2 < m <= U, h=U-m < n and H=h+1:
    time O(n + H**(5/2)*log(h+2)**2), auxiliary O(H**2) wide words.
The returned tuple is the lexicographically least entire optimal witness.
Signed values/differences must fit charged *wide* words; not a fixed-RAM,
Python RSS, world-novelty or production claim. Input/output excluded.
"""
from __future__ import annotations


def solve_g9(a, m, *, counters=None):
    n = len(a)
    U = n * (n + 1) // 2
    if (type(m) is not int or m < 2 or not U < 2*m or
            m > U or any(type(x) is not int for x in a)):
        raise ValueError("requires signed integers and high modulus")
    h = U - m
    if h >= n:
        raise ValueError("requires h<n")
    p = min(n, h+2)
    for k in range(h+3, n+1):
        if a[k-3] + a[k-1] <= 2*a[k-2]:
            return ()
    W = lambda i: i*(i+1)//2

    # Prepare eligible convex edges ONCE, then reuse for every score query.
    # Fixed i: omitted weight and compulsory-index violations increase with j.
    events = []
    for i in range(1, p):
        for j in range(i+1, p+1):
            if (i <= h and j >= h+2) or (i >= h+1 and j > i+1):
                break
            gap = W(min(j-1, h)) - W(min(i, h))
            if gap > h:
                break
            events.append((a[j-1]-a[i-1], -j, i, j, gap))
    events.sort()  # descending destination breaks equal differences

    queries = 0
    relaxations = 0

    def max_length(fixed_omissions, first_allowed_omission):
        """Best full length subject to:
        * all fixed_omissions are omitted;
        * every index below first_allowed_omission, other than fixed omissions,
          is selected;
        * the normal high-modulus and convexity rules.
        Returns 0 if no NONEMPTY witness exists.

        Lex histories are never stored.  This is a scalar resource DP.
        """
        nonlocal queries, relaxations
        queries += 1
        forbidden = [False]*(p+1)
        for t in fixed_omissions:
            forbidden[t] = True
        required = [0]*(p+1)
        for t in range(1, p+1):
            required[t] = required[t-1] + (
                t < first_allowed_omission and not forbidden[t])
        dp = [[-1]*(h+1) for _ in range(p+1)]
        for i in range(1, min(p, h+1)+1):
            r = W(i-1)
            if r <= h and not forbidden[i] and required[i-1] == 0:
                dp[i][r] = 1

        for _, _, i, j, gap in events:
            if (forbidden[i] or forbidden[j] or
                    required[j-1] != required[i]):
                continue
            source, dest = dp[i], dp[j]
            for r in range(h-gap+1):
                relaxations += 1
                prefix = source[r]
                if prefix > 0 and prefix+1 > dest[r+gap]:
                    dest[r+gap] = prefix+1
        core = dp[p][h]
        return core + n-p if core > 0 else 0

    optimum = max_length((), 1)
    if optimum == 0:
        return ()
    omitted_count = n - optimum
    assert omitted_count*(omitted_count+1)//2 <= h

    chosen_omissions = []
    previous = 0
    for _ in range(omitted_count):
        # At threshold x, all positions <x outside chosen_omissions
        # MUST be selected.  A remaining omitted index must be >=x.
        # Feasibility is monotone in x. Binary-search its greatest true x.
        lo, hi = previous+1, h+1
        assert max_length(chosen_omissions, lo) == optimum
        while lo+1 < hi:
            mid = (lo+hi)//2
            if max_length(chosen_omissions, mid) == optimum:
                lo = mid
            else:
                hi = mid
        assert lo <= h
        chosen_omissions.append(lo)
        previous = lo

    omission_set = set(chosen_omissions)
    selected = tuple(i for i in range(1, n+1) if i not in omission_set)
    assert len(selected) == optimum and sum(selected) == m
    assert all(a[x-1]+a[z-1] > 2*a[y-1]
               for x,y,z in zip(selected, selected[1:], selected[2:]))
    if counters is not None:
        counters.update(queries=queries, events=len(events),
                        relaxations=relaxations, omissions=omitted_count)
    return selected
