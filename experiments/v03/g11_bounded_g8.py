"""Research derivative of original G8: avoids O(n) output-sized slice temporaries.

Diff from experiments/v03/g8_persistent_intervals.py is only the final indexed
strict-convexity assertion. Historical implementation is untouched.
"""
"""G8 research-only exact full-lex sparse-gap interval DP.

For U/2<m<=U, h=U-m<n and H=h+1, returns the globally
lex-least entire maximum-length selected-index tuple.
Time O(n+H**(5/2)*log(h+2)); auxiliary O(H**2*log(h+2)) wide words.
Input/output excluded, signed operands must fit wide words.
No fixed-word bit complexity, RSS or production claim.
"""
from __future__ import annotations


def solve_g8(a, m):
    n = len(a)
    U = n * (n + 1) // 2
    if (type(m) is not int or m < 2 or not U < 2*m or
            m > U or any(type(x) is not int for x in a)):
        raise ValueError("requires integer signed values and high modulus")
    h = U-m
    if h >= n:
        raise ValueError("requires h<n")
    p = min(n, h+2)
    for k in range(h+3, n+1):
        if a[k-3]+a[k-1] <= 2*a[k-2]:
            return ()
    W = lambda t: t*(t+1)//2

    # Immutable (previous, first omitted, last omitted) chains.
    nodes = [(-1, 0, 0)]
    def attach(previous, lo, hi):
        if lo > hi:
            return previous
        nodes.append((previous, lo, hi))
        return len(nodes)-1
    def omitted(chain):
        runs = []
        while chain:
            chain, lo, hi = nodes[chain]
            runs.append((lo, hi))
        for lo, hi in reversed(runs):
            yield from range(lo, hi+1)

    dp = [[None]*(h+1) for _ in range(p+1)]
    for i in range(1, min(p, h+1)+1):
        r = W(i-1)
        if r <= h:
            dp[i][r] = (1, attach(0, 1, i-1))

    # Safe early breaks: gap cost and compulsory-index illegality
    # are nondecreasing with destination j for fixed source i.
    events = []
    for i in range(1, p):
        for j in range(i+1, p+1):
            if ((i <= h and j >= h+2) or
                    (i >= h+1 and j > i+1)):
                break
            gap = W(min(j-1, h)) - W(min(i, h))
            if gap > h:
                break
            events.append((a[j-1]-a[i-1], -j, i, j))
    events.sort()

    # Equal differences are processed by descending destination.
    for _, _, i, j in events:
        lo, hi = i+1, min(j-1, h)
        gap = W(hi)-W(min(i, h))
        for r in range(h-gap+1):
            prefix = dp[i][r]
            if prefix is None:
                continue
            old = dp[j][r+gap]
            length = prefix[0]+1
            if old is not None:
                if length < old[0]:
                    continue
                if length == old[0]:
                    candidate = tuple(omitted(prefix[1])) + tuple(range(lo, hi+1))
                    if candidate <= tuple(omitted(old[1])):
                        continue
            # Allocate one immutable interval only for accepted
            # positive-gap updates; adjacent edges share history.
            dp[j][r+gap] = (length, attach(prefix[1], lo, hi))

    final = dp[p][h]
    if final is None:
        return ()
    excluded = set(omitted(final[1]))
    selected = tuple(i for i in range(1, n+1) if i not in excluded)
    assert len(selected) == final[0] + n-p and sum(selected) == m
    assert all(a[selected[k]-1]+a[selected[k+2]-1] >
               2*a[selected[k+1]-1] for k in range(len(selected)-2))
    return selected
