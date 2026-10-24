"""Research-only baselines. Same modular-index/strict-convex/lex objective.

The tuple edge baseline is a faithful *modular augmentation* of Kluev's
strictly increasing edge-difference ordering, not Kluev's original method.
Tuple copying costs O(n) per transition, unlike word-model bitmask copies.
"""


def solve_mask(a, m):
    """Faithful full 2^q mask scan from v0.2's complement branch.

    This isolates the branch's enumeration cost; v0.2's public solve()
    additionally performs validation, sorting, other prechecks/shortcuts.
    """
    n = len(a)
    U = n * (n + 1) // 2
    if not (2 * m > U and m <= U and m >= 2):
        raise ValueError('high modulus only')
    h = U - m
    q = min(n, h)
    best = ()
    for mask in range(1 << q):
        if sum(j for j in range(1, q + 1) if mask & (1 << (j - 1))) != h:
            continue
        witness = tuple(i for i in range(1, n + 1)
                        if i > q or not (mask & (1 << (i - 1))))
        if any(a[z - 1] - a[y - 1] <= a[y - 1] - a[x - 1]
               for x, y, z in zip(witness, witness[1:], witness[2:])):
            continue
        if len(witness) > len(best) or (len(witness) == len(best) and witness < best):
            best = witness
    return best


def solve_edge_tuple(a, m):
    """Kluev-style increasing-edge sweep with exact residue/lex states.

    Equal-weight edges are staged: a candidate created at difference d
    cannot be extended by another edge of the same difference d.
    Dense residue states are kept to expose O(nm) state footprint;
    lex tuples can occupy O(n) words EACH in worst case.
    """
    if not isinstance(m, int) or m < 2:
        raise ValueError('m >= 2 required')
    n = len(a)
    if m > n * (n + 1) // 2:
        return ()
    rows = [[None] * m for _ in range(n + 1)]
    for i in range(1, n + 1):
        rows[i][i % m] = (i,)
    edges = sorted((a[j-1] - a[i-1], i, j)
                   for i in range(1, n+1) for j in range(i+1, n+1))
    pos = 0
    while pos < len(edges):
        end = pos+1
        while end < len(edges) and edges[end][0] == edges[pos][0]:
            end += 1
        staged = {}
        for _, i, j in edges[pos:end]:
            for r, prior in enumerate(rows[i]):
                if prior is None:
                    continue
                candidate = prior + (j,)
                key = (j, (r + j) % m)
                old = staged.get(key)
                if old is None or len(candidate) > len(old) or (len(candidate) == len(old)
                        and candidate < old):
                    staged[key] = candidate
        for (j, r), candidate in staged.items():
            old = rows[j][r]
            if old is None or len(candidate) > len(old) or (len(candidate) == len(old)
                    and candidate < old):
                rows[j][r] = candidate
        pos = end
    best = ()
    for row in rows[1:]:
        candidate = row[0]
        if candidate and (len(candidate) > len(best) or
                (len(candidate) == len(best) and candidate < best)):
            best = candidate
    return best
