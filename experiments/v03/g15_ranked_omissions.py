"""Research: one-pass canonical DP via exact-sum omission ranks.

Complete for U/2 < m <= U, including h=U-m >= n. Not production dispatch.
Ranks count distinct-part partitions and need O(sqrt(h+1)) bits; Python
big integers are NOT charged as fixed-width constant-time operations.
See research/v03/g15/THEOREM.md for the model and tradeoff.
"""
from __future__ import annotations

from experiments.v03.g10_direct_next import _SelectedIndices
from experiments.v03.g14_three_omission_certificate import certify_g14


def _counts(k, h):
    """C[i][s]: subsets of {i,...,k} with sum s; exact integers."""
    c = [[0] * (h + 1) for _ in range(k + 2)]
    c[k + 1][0] = 1
    for i in range(k, 0, -1):
        row, nxt = c[i], c[i + 1]
        row[:] = nxt
        for s in range(i, h + 1):
            row[s] += nxt[s - i]
    return c


def _unrank(c, k, h, rank):
    """Omission incidence order: keep=0 precedes omit=1."""
    if not 0 <= rank < c[1][h]:
        raise ValueError("rank outside exact-sum family")
    omitted = []
    remaining = h
    for i in range(1, k + 1):
        keep = c[i + 1][remaining]
        if rank >= keep:
            rank -= keep
            remaining -= i
            omitted.append(i)
    assert remaining == 0 and rank == 0
    return omitted


def _validate(a, m, *, check_values=True):
    n = len(a)
    u = n * (n + 1) // 2
    if (n < 2 or type(m) is not int or m < 2 or
            not u < 2 * m or m > u or
            (check_values and any(type(value) is not int for value in a))):
        raise ValueError("requires n>=2, signed integers and U/2<m<=U")
    return n, u - m


def solve_ranked(a, m, *, counters=None):
    """Exact canonical witness, with one event sweep and one unranking."""
    n, h = _validate(a, m)
    p, k = min(n, h + 2), min(n, h)
    if counters is not None:
        counters.update(mode="ranked", h=h, sweeps=0, events=0,
                        relaxations=0, states=0)
    for end in range(h + 3, n + 1):
        if a[end - 3] + a[end - 1] <= 2 * a[end - 2]:
            return ()

    c = _counts(k, h)
    # Beyond the mutable universe only the empty residual subset exists.
    c.extend([c[k + 1]] * max(0, p + 2 - len(c)))
    total = c[1][h]
    if not total:
        return ()
    triangular = lambda t: t * (t + 1) // 2
    # Each reachable state is (selected cardinality, prefix rank offset).
    score = [[0] * (h + 1) for _ in range(p + 1)]
    ranks = [[0] * (h + 1) for _ in range(p + 1)]
    active = [[] for _ in range(p + 1)]
    for i in range(1, min(p, h + 1) + 1):
        r = triangular(i - 1)
        if r > h:
            break
        if c[i + 1][h - r]:
            score[i][r] = 1
            ranks[i][r] = total - c[i][h - r]
            active[i].append(r)

    events = []
    for i in range(1, p):
        for j in range(i + 1, p + 1):
            if j > i + 1 and j - 1 > k:
                break
            gap = triangular(j - 1) - triangular(i)
            if gap > h:
                break
            events.append((a[j - 1] - a[i - 1], -j, i, j, gap))
    events.sort()
    relaxations = 0
    for _, _, i, j, gap in events:
        src, dst = score[i], score[j]
        src_rank, dst_rank = ranks[i], ranks[j]
        before, after, future = c[i + 1], c[j], c[j + 1]
        for r in active[i]:
            relaxations += 1
            r2 = r + gap
            if r2 > h or not future[h - r2]:
                continue
            # Telescoped rank increments for omitting i+1,...,j-1.
            candidate_rank = src_rank[r] + before[h - r] - after[h - r2]
            candidate_length = src[r] + 1
            old = dst[r2]
            if (candidate_length > old or
                    (candidate_length == old and candidate_rank < dst_rank[r2])):
                if not old:
                    active[j].append(r2)
                dst[r2] = candidate_length
                dst_rank[r2] = candidate_rank

    best = None
    if p < n:
        if score[p][h]:
            best = (score[p][h] + n - p, ranks[p][h])
    else:
        # Without two compulsory anchors, allow every legal final endpoint.
        for j in range(1, p + 1):
            tail = triangular(n) - triangular(j)
            if tail > h:
                continue
            value = (score[j][h - tail], ranks[j][h - tail])
            # The residual weight is the whole suffix's weight: its only
            # completion omits that suffix, so its rank offset is zero.
            if value[0] and (best is None or value[0] > best[0] or
                    (value[0] == best[0] and value[1] < best[1])):
                best = value
    if counters is not None:
        counters.update(sweeps=1, events=len(events),
                        relaxations=relaxations,
                        states=sum(map(len, active)), rank_bits=total.bit_length())
    if best is None:
        return ()
    omitted = _unrank(c, k, h, best[1])
    answer = tuple(_SelectedIndices(n, omitted, best[0]))
    assert len(answer) == best[0] and sum(answer) == m
    assert all(a[answer[t] - 1] + a[answer[t + 2] - 1] >
               2 * a[answer[t + 1] - 1] for t in range(len(answer) - 2))
    return answer


def solve_g15(a, m, *, counters=None):
    """Keep G14's linear certificates; replace only its complete fallback."""
    # Each selected subsolver performs full value validation once.
    n, h = _validate(a, m, check_values=False)
    if h < n:
        details = {} if counters is not None else None
        answer = certify_g14(a, m, counters=details)
        if answer is not None:
            if counters is not None:
                counters.update(mode="g14_certificate", certificate=details)
            return answer
    return solve_ranked(a, m, counters=counters)
