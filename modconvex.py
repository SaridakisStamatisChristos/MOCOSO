"""Exact modular convex subsequence optimization with verifiable certificates.

Input indices 1-based, signed arbitrary-precision values.
``solve`` returns a SolverResult. Decision predicate is length >= K.
"""
from __future__ import annotations
from array import array
from dataclasses import dataclass
import time
import tracemalloc
from typing import Optional

@dataclass
class Result:
    status: str
    indices: tuple[int, ...]
    lower_bound: int
    upper_bound: int
    length: Optional[int]
    operations: int
    reason: str = ''


def _dense_codes(n):
    """Smallest portable array fields covering all DP lengths and indices."""
    lengths = 'h' if n <= 32767 else ('i' if n <= 2147483647 else 'q')
    successors = 'H' if n <= 65535 else ('I' if n <= 4294967295 else 'Q')
    return lengths, successors


def dense_dp_payload_bytes(n, m):
    """Exact payload bytes of both dense tables on this Python platform.

    This excludes Python objects, input, sorting, temporary sweep buffers, and
    allocator overhead; it is a necessary, not sufficient, memory budget.
    """
    if not isinstance(n, int) or n < 0 or not isinstance(m, int) or m < 2:
        raise ValueError('n must be nonnegative and m >= 2')
    lc, sc = _dense_codes(n)
    return (n * (n - 1) // 2) * m * (array(lc).itemsize + array(sc).itemsize)


def verify(a, m, selected):
    if not isinstance(m, int) or m < 2:
        raise ValueError('m must be an integer >= 2')
    if not isinstance(selected, (tuple, list)):
        return False
    if any(not isinstance(i, int) or i < 1 or i > len(a) for i in selected):
        return False
    if any(x >= y for x, y in zip(selected, selected[1:])):
        return False
    if sum(selected) % m:
        return False
    return all(a[z - 1] - a[y - 1] > a[y - 1] - a[x - 1]
               for x, y, z in zip(selected, selected[1:], selected[2:]))


def index_only_upper(n, m):
    # Every feasible length t must have a multiple of m between
    # the minimum and maximum sums of t distinct indices in [1,n].
    for t in range(n, 0, -1):
        lo = t * (t + 1) // 2
        hi = t * (2 * n - t + 1) // 2
        if (lo + m - 1) // m <= hi // m:
            return t
    return 0


def solve(a, m, *, K=None, max_operations=None, max_seconds=None,
          max_heap_bytes=None, complement_cutoff=15):
    """Exact optimization / threshold decision, with soft execution limits.

    K=None => OPTIMAL or RESOURCE_LIMIT.
    K=int => FEASIBLE/INFEASIBLE/RESOURCE_LIMIT; early feasible allowed.
    max_operations caps counted loops (not CPU instructions).
    max_seconds and max_heap_bytes are periodically checked SOFT limits.
    MemoryError becomes RESOURCE_LIMIT and does not imply INFEASIBLE.
    """
    if not isinstance(m, int) or m < 2 or any(not isinstance(x, int) for x in a):
        raise ValueError('array must contain integers and m >= 2')
    if K is not None and not isinstance(K, int):
        raise ValueError('K must be an integer')
    if not isinstance(complement_cutoff,int) or not 0 <= complement_cutoff <= 20:
        raise ValueError('complement_cutoff must be in 0..20')
    if max_operations is not None and max_operations < 0:
        raise ValueError('max_operations must be >= 0')
    if max_seconds is not None and max_seconds < 0:
        raise ValueError('max_seconds must be >= 0')
    if max_heap_bytes is not None and max_heap_bytes < 0:
        raise ValueError('max_heap_bytes must be >= 0')

    start = time.monotonic()
    monitoring_started = False
    if max_heap_bytes is not None and not tracemalloc.is_tracing():
        tracemalloc.start()
        monitoring_started = True
    n = len(a)
    if K is not None and K > n:
        if monitoring_started:
            tracemalloc.stop()
        return Result('INFEASIBLE', (), 0, n, None, 0, 'K exceeds n')
    U = n * (n + 1) // 2
    ops = 0
    best = ()
    chosen_head = ()
    chosen_len = 0
    # The coarse n bound is valid during preprocessing interruptions.
    ub = n
    asc = []
    d = 0
    lengths = successors = None
    def limit():
        if max_operations is not None and ops > max_operations:
            return 'operation budget'
        if max_seconds is not None and time.monotonic() - start > max_seconds:
            return 'soft time budget'
        if max_heap_bytes is not None and tracemalloc.get_traced_memory()[0] > max_heap_bytes:
            return 'soft traced-heap budget'
        return ''
    def offset(i, j):
        return ((i - 1) * (2 * n - i) // 2 + (j - i - 1)) * m

    def answer(status, reason=''):
        if chosen_len > len(chosen_head):
            seq = list(chosen_head)
            left, right = seq
            rem = (-(left + right)) % m
            while True:
                nxt = successors[offset(left, right) + rem]
                if nxt == 0:
                    break
                seq.append(nxt)
                rem = (rem - nxt) % m
                left, right = right, nxt
            witness = tuple(seq)
        else:
            witness = tuple(chosen_head)
        result = Result(status, witness, len(witness), ub,
                        len(witness) if status == 'OPTIMAL' else None,
                        ops, reason)
        if monitoring_started:
            tracemalloc.stop()
        return result

    def offer(candidate):
        nonlocal best, chosen_head, chosen_len
        if len(candidate) > chosen_len or (len(candidate) == chosen_len and candidate < chosen_head):
            best = candidate
            chosen_head = candidate
            chosen_len = len(candidate)

    try:
        if K is not None and K <= 0:
            return answer('FEASIBLE', 'empty witness')
        if m > U:
            ub = 0
            return answer('OPTIMAL' if K is None else 'INFEASIBLE',
                          'no nonempty index sum divisible by modulus')
        exceeded = limit()
        if exceeded:
            return answer('RESOURCE_LIMIT', exceeded)
        # The built-in sort is not interruptible; check its limits on both sides.
        asc = sorted(range(1, n + 1), key=lambda i: a[i-1])
        d = sum(t == 0 or a[asc[t]-1] != a[asc[t-1]-1]
                for t in range(len(asc)))
        exceeded = limit()
        if exceeded:
            return answer('RESOURCE_LIMIT', exceeded)
        ub = min(index_only_upper(n, m), d * (d - 1) + 2)
        exceeded = limit()
        if exceeded:
            return answer('RESOURCE_LIMIT', exceeded)
        if K is not None and K > ub:
            return answer('INFEASIBLE', 'index-sum upper bound')
        if ub == 0:
            return answer('OPTIMAL' if K is None else 'INFEASIBLE', 'no nonempty index sum divisible by modulus')
        if d == 1:
            # Every triple has two equal differences. Max length = 2.
            if m <= n:
                offer((m,))  # lex-first modular singleton
            for i in range(1, n):
                if i % 128 == 0:
                    exceeded = limit()
                    if exceeded:
                        return answer('RESOURCE_LIMIT', exceeded)
                # Smallest j>i with i+j == 0 (mod m).
                j = i + 1 + ((-2 * i - 1) % m)
                if j <= n:
                    offer((i, j))
                    break
            if K is not None:
                return answer('FEASIBLE' if chosen_len >= K else 'INFEASIBLE', 'constant-value exact shortcut')
            return answer('OPTIMAL', 'constant-value exact shortcut')
        # Complement enumeration: for m > U/2, the only positive
        # admissible index sum is m. Omitted indices sum h=U-m.
        # h=0 is linear; h<=15 is a conservative practical switch.
        if m > U // 2 and U - m <= complement_cutoff:
            h = U - m
            q = min(n, h)
            for mask in range(1 << q):
                if max_operations is not None and ops >= max_operations:
                    return answer('RESOURCE_LIMIT', 'operation budget')
                ops += 1
                if mask & 63 == 0:
                    if max_seconds is not None and time.monotonic() - start > max_seconds:
                        return answer('RESOURCE_LIMIT', 'soft time budget')
                    if max_heap_bytes is not None and tracemalloc.get_traced_memory()[0] > max_heap_bytes:
                        return answer('RESOURCE_LIMIT', 'soft traced-heap budget')
                omitted_sum = sum(j + 1 for j in range(q) if mask >> j & 1)
                if omitted_sum != h:
                    continue
                seq = tuple(i for i in range(1, n + 1)
                            if i > q or not (mask >> (i - 1) & 1))
                if verify(a, m, seq):
                    offer(seq)
                    if K is not None and chosen_len >= K:
                        return answer('FEASIBLE', 'complement witness')
            return answer('OPTIMAL' if K is None else 'INFEASIBLE',
                          'complete complement enumeration')
        # Baseline witnesses before the expensive DP are certified.
        for i in range(1, n + 1):
            if i % 128 == 0:
                exceeded = limit()
                if exceeded:
                    return answer('RESOURCE_LIMIT', exceeded)
            if i % m == 0:
                offer((i,))
        if K is not None and chosen_len >= K:
            return answer('FEASIBLE', 'singleton witness')
        for i in range(1, n):
            exceeded = limit()
            if exceeded:
                return answer('RESOURCE_LIMIT', exceeded)
            for j in range(i + 1, n + 1):
                if j % 256 == 0:
                    exceeded = limit()
                    if exceeded:
                        return answer('RESOURCE_LIMIT', exceeded)
                if (i + j) % m == 0:
                    offer((i, j))
        if K is not None and chosen_len >= K:
            return answer('FEASIBLE', 'pair witness')
        if ub <= 2:
            return answer('OPTIMAL' if K is None else 'INFEASIBLE', 'upper bound at most two')
        # Check again before computing and allocating the DP tables.
        exceeded = limit()
        if exceeded:
            return answer('RESOURCE_LIMIT', exceeded)

        pairs = n * (n - 1) // 2
        slots = pairs * m
        length_code, successor_code = _dense_codes(n)
        if max_heap_bytes is not None:
            # Proven minimum payload; do not pretend this is a hard RSS limit.
            mandatory_bytes = dense_dp_payload_bytes(n, m)
            if mandatory_bytes + tracemalloc.get_traced_memory()[0] > max_heap_bytes:
                return answer('RESOURCE_LIMIT', 'DP-array preflight exceeds traced-heap budget')
        lengths = array(length_code, [-1]) * slots
        successors = array(successor_code, [0]) * slots

        desc = asc[::-1]
        # Iteration is by SECOND index descending, so all (j,k) are ready.
        for j in range(n, 1, -1):
            best_len = [-1] * m
            best_next = [0] * m
            ks = [k for k in desc if k > j]  # descending value
            cursor = 0
            # i ascending value => threshold decreases. The sweep's
            # admissible k set therefore only grows.
            for i in asc:
                if i >= j:
                    continue
                threshold = 2 * a[j - 1] - a[i - 1]
                while cursor < len(ks) and a[ks[cursor] - 1] > threshold:
                    k = ks[cursor]
                    cursor += 1
                    source = offset(j, k)
                    shift = k % m
                    for s in range(m):
                        if max_operations is not None and ops >= max_operations:
                            return answer('RESOURCE_LIMIT', 'operation budget')
                        ops += 1
                        length = lengths[source + s]
                        if length >= 0:
                            residue = s + shift
                            if residue >= m:
                                residue -= m
                            candidate = length + 1
                            if candidate > best_len[residue] or (
                                candidate == best_len[residue] and k < best_next[residue]
                            ):
                                best_len[residue] = candidate
                                best_next[residue] = k
                    exceeded = limit()
                    if exceeded:
                        return answer('RESOURCE_LIMIT', exceeded)
                target = offset(i, j)
                for r in range(m):
                    if max_operations is not None and ops >= max_operations:
                        return answer('RESOURCE_LIMIT', 'operation budget')
                    ops += 1
                    v = best_len[r]
                    if r == 0 and v < 0:
                        v = 0
                    lengths[target + r] = v
                    successors[target + r] = best_next[r] if v > 0 else 0
                # Candidate pair is complete. Lex ties compare first two
                # indices, so no witness construction is necessary here.
                required = (-(i + j)) % m
                v = lengths[target + required]
                if v >= 0:
                    candidate_len = v + 2
                    if (candidate_len > chosen_len or
                        (candidate_len == chosen_len and (i, j) < chosen_head[:2])):
                        chosen_len = candidate_len
                        chosen_head = (i, j)
                if K is not None and chosen_len >= K:
                    return answer('FEASIBLE', 'exact witness from completed DP state')
                exceeded = limit()
                if exceeded:
                    return answer('RESOURCE_LIMIT', exceeded)
        return answer('OPTIMAL' if K is None else 'INFEASIBLE', 'complete dynamic program')
    except (MemoryError, OverflowError):
        return answer('RESOURCE_LIMIT', 'allocation failed (MemoryError/OverflowError)')


def oracle(a, m):
    n = len(a)
    best = ()
    for mask in range(1 << n):
        seq = tuple(i + 1 for i in range(n) if mask >> i & 1)
        if verify(a, m, seq) and (len(seq) > len(best) or
                                   (len(seq) == len(best) and seq < best)):
            best = seq
    return best


def cubic_dp(a, m):
    """Structurally distinct naive forward triple-loop DP; reconstruct via tuples.

    Only for small n; O(n^3 m * n) worst-case for tuple operations.
    """
    n = len(a)
    states = {}
    best = ()
    def improve(seq):
        nonlocal best
        if sum(seq) % m == 0 and (len(seq) > len(best) or
            (len(seq) == len(best) and seq < best)):
            best = seq
    for i in range(1, n + 1):
        improve((i,))
        for j in range(i + 1, n + 1):
            seq = (i, j)
            states[(i, j, (i + j) % m)] = seq
            improve(seq)
    for j in range(2, n):
        for k in range(j + 1, n + 1):
            for i in range(1, j):
                if a[k - 1] - a[j - 1] <= a[j - 1] - a[i - 1]:
                    continue
                for r in range(m):
                    prior = states.get((i, j, r))
                    if prior is None:
                        continue
                    seq = prior + (k,)
                    key = (j, k, (r + k) % m)
                    previous = states.get(key)
                    if previous is None or len(seq) > len(previous) or (len(seq) == len(previous) and seq < previous):
                        states[key] = seq
                        improve(seq)
    return best
