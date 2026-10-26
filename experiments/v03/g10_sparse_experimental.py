"""Experimental G10-S: sparse-resource exact direct-next-omission event DP.

Same high-modulus input/output contract as G10. Dicts hold only attained exact
resource states; no claim of uniform speedup or improved asymptotic bounds.
Python dict operations have amortized/average-case costs, so this source does
NOT claim a deterministic worst-case O(H^(5/2) log H) time guarantee.
Auxiliary state count O(H^2) wide-word entries; actual Python heap differs.
Research only: production modconvex.solve is unchanged.
"""
from __future__ import annotations


class _SelectedIndices:
    def __init__(self, n, omissions, count):
        self.n = n
        self.omissions = omissions
        self.count = count
        self.index = 1
        self.cursor = 0

    def __iter__(self):
        return self

    def __length_hint__(self):
        return self.count

    def __next__(self):
        while self.index <= self.n:
            i = self.index
            self.index += 1
            if (self.cursor < len(self.omissions)
                    and i == self.omissions[self.cursor]):
                self.cursor += 1
            else:
                self.count -= 1
                return i
        raise StopIteration


def solve_g10_sparse(a, m, *, counters=None):
    n = len(a)
    U = n * (n + 1) // 2
    if (type(m) is not int or m < 2 or not U < 2 * m or m > U
            or any(type(x) is not int for x in a)):
        raise ValueError("requires signed integers and U/2 < m <= U")
    h = U - m
    if h >= n:
        raise ValueError("requires h < n")
    p = min(n, h + 2)
    for k in range(h + 3, n + 1):
        if a[k-3] + a[k-1] <= 2 * a[k-2]:
            return ()

    def W(i):
        return i * (i + 1) // 2

    events = []
    for i in range(1, p):
        for j in range(i + 1, p + 1):
            if (i <= h and j >= h + 2) or (i >= h + 1 and j > i + 1):
                break
            gap = W(min(j - 1, h)) - W(min(i, h))
            if gap > h:
                break
            events.append((a[j-1] - a[i-1], -j, i, j, gap))
    events.sort()
    INF = p + 1
    calls = 0
    relaxations = 0

    def best_next(fixed, first_allowed):
        nonlocal calls, relaxations
        calls += 1
        forbidden = [False] * (p + 2)
        for i in fixed:
            forbidden[i] = True
        required = [0] * (p + 2)
        for t in range(1, p + 1):
            required[t] = required[t-1] + (
                t < first_allowed and not forbidden[t])
        first_free = [INF] * (p + 3)
        for i in range(p, 0, -1):
            first_free[i] = first_free[i+1] if forbidden[i] else i

        # Every entry holds (max cardinality, max earliest remaining omission).
        dp = [{} for _ in range(p + 1)]
        for i in range(1, min(p, h + 1) + 1):
            r = W(i - 1)
            if r <= h and not forbidden[i] and required[i-1] == 0:
                dp[i][r] = (1, first_free[1] if first_free[1] < i else INF)
        for _, _, i, j, g in events:
            if (forbidden[i] or forbidden[j]
                    or required[j-1] != required[i]):
                continue
            source = dp[i]
            if not source:
                continue
            free_gap = first_free[i+1]
            if free_gap >= j:
                free_gap = INF
            dest = dp[j]
            max_r = h - g
            for r, state in source.items():
                if r > max_r:
                    continue
                relaxations += 1
                length, z = state
                nxt = z if z < free_gap else free_gap
                candidate = (length + 1, nxt)
                key = r + g
                if candidate > dest.get(key, (-1, 0)):
                    dest[key] = candidate
        length, z = dp[p].get(h, (-1, INF))
        return (length + n - p, z) if length >= 1 else (0, INF)

    optimum, first = best_next((), 1)
    if optimum == 0:
        return ()
    omission_count = n - optimum
    Q = []
    for step in range(omission_count):
        if step:
            current, first = best_next(Q, Q[-1] + 1)
            assert current == optimum
        previous = Q[-1] if Q else 0
        assert previous < first <= h
        Q.append(first)
    selected = tuple(_SelectedIndices(n, Q, optimum))
    assert len(selected) == optimum and sum(selected) == m
    assert all(a[selected[k]-1] + a[selected[k+2]-1]
               > 2 * a[selected[k+1]-1]
               for k in range(len(selected) - 2))
    if counters is not None:
        counters.update(queries=calls, events=len(events),
                        relaxations=relaxations, omissions=omission_count)
    return selected
