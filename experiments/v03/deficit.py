"""Isolated exact high-modulus deficit-partition research solver.

Applicable only when U/2 < m <= U, U=n(n+1)/2. Does NOT replace
modconvex.solve. Budgets are soft; no hard RSS ceiling is promised.
"""
from dataclasses import dataclass
import math
import time
import tracemalloc


@dataclass(frozen=True)
class DeficitResult:
    status: str
    indices: tuple[int, ...]
    lower_bound: int
    upper_bound: int
    length: int | None
    operations: int
    candidates: int
    nodes: int
    reason: str = ''


def solve_deficit(a, m, *, K=None, max_operations=None,
                  max_seconds=None, max_heap_bytes=None):
    """Exact or certified partial answer in the high-modulus regime.

    OPTIMAL: length and lex-smallest optimum indices.
    FEASIBLE: valid witness of length >= K; not necessarily optimal.
    INFEASIBLE: exhaustive proof that no witness reaches K.
    RESOURCE_LIMIT: valid lower-bound witness and n as sound upper bound.

    max_operations counts a subset of core loops and is NOT CPU steps.
    max_seconds / max_heap_bytes are monitored soft limits; the latter is
    tracemalloc current Python allocations, NOT a hard process RSS cap.
    """
    if not isinstance(m, int) or isinstance(m, bool) or m < 2:
        raise ValueError('m must be an integer >= 2')
    if any(not isinstance(x, int) for x in a):
        raise ValueError('a must contain integers')
    if K is not None and (not isinstance(K, int) or isinstance(K, bool)):
        raise ValueError('K must be an integer')
    if max_operations is not None and (
        isinstance(max_operations, bool) or not isinstance(max_operations, int)
        or max_operations < 0
    ):
        raise ValueError('max_operations must be a nonnegative integer')
    if max_seconds is not None and (
        isinstance(max_seconds, bool) or not isinstance(max_seconds, (int, float))
        or max_seconds < 0 or
        (isinstance(max_seconds, float) and not math.isfinite(max_seconds))
    ):
        raise ValueError('max_seconds must be finite and nonnegative')
    if max_heap_bytes is not None and (
        isinstance(max_heap_bytes, bool) or not isinstance(max_heap_bytes, int)
        or max_heap_bytes < 0
    ):
        raise ValueError('max_heap_bytes must be a nonnegative integer')
    n = len(a)
    U = n * (n + 1) // 2
    if not (U // 2 < m <= U and 2 * m > U):
        raise ValueError('deficit method requires U/2 < m <= U')
    started = time.monotonic()
    trace_owned = False
    if max_heap_bytes is not None and not tracemalloc.is_tracing():
        tracemalloc.start()
        trace_owned = True
    ops = 0
    nodes = 0
    candidates = 0
    best_omitted = None
    best_prefix = ()
    best_len = 0
    upper = n
    q = 0

    def result(status, reason=''):
        witness = (tuple(i for i in range(1, n + 1)
                         if i > q or not best_omitted[i])
                   if best_omitted is not None else ())
        if trace_owned:
            tracemalloc.stop()
        return DeficitResult(status, witness, len(witness), upper,
                             len(witness) if status == 'OPTIMAL' else None,
                             ops, candidates, nodes, reason)

    def budget():
        if max_operations is not None and ops >= max_operations:
            return 'operation budget'
        if max_seconds is not None and time.monotonic() - started > max_seconds:
            return 'soft time budget'
        if max_heap_bytes is not None and tracemalloc.get_traced_memory()[0] > max_heap_bytes:
            return 'soft traced-heap budget'
        return ''

    def tick():
        nonlocal ops
        reason = budget()
        if reason:
            raise _BudgetExceeded(reason)
        ops += 1

    try:
        if K is not None and K > n:
            return result('INFEASIBLE', 'threshold exceeds n')
        if K is not None and K <= 0:
            return result('FEASIBLE', 'empty witness')
        tick()
        h = U - m
        q = min(n, h)
        # Every selected triple ending at index >= q+3 belongs entirely to
        # the immutable suffix q+1..n. This is a necessary condition.
        for k in range(q + 3, n + 1):
            tick()
            if a[k - 1] - a[k - 2] <= a[k - 2] - a[k - 3]:
                upper = 0
                return result('OPTIMAL' if K is None else 'INFEASIBLE',
                              'immutable suffix fails strict convexity')
        # R[t][s] iff a distinct subset of [1..t] sums to s.
        # Explicit bytearrays give O(qh) bytes and O(qh) word operations.
        R = [bytearray(h + 1)]
        R[0][0] = 1
        for t in range(1, q + 1):
            last = R[-1]
            row = bytearray(last)
            for s in range(t, h + 1):
                tick()
                if last[s - t]:
                    row[s] = 1
            R.append(row)
        if not R[q][h]:
            upper = 0
            return result('OPTIMAL' if K is None else 'INFEASIBLE',
                          'no distinct omission partition')
        omitted = [False] * (q + 1)
        # Explicit DFS frames avoid Python's recursion depth bound for q>1000.
        # Frame phases: 0=enter, 1=include branch, 2=undo inclusion.
        stack = [(q, h, 0)]
        while stack:
            t, rem, phase = stack.pop()
            if phase == 2:
                omitted[t] = False
                continue
            if phase == 1:
                if rem >= t and R[t - 1][rem - t]:
                    omitted[t] = True
                    stack.append((t, rem, 2))
                    stack.append((t - 1, rem - t, 0))
                continue
            tick()
            nodes += 1
            if t == 0:
                if rem:
                    raise AssertionError('reachability pruning broken')
                candidates += 1
                # Only triples whose final selected index <= q+2 depend on
                # omissions; all remaining triples were checked above.
                prefix = tuple(i for i in range(1, min(n, q + 2) + 1)
                               if i > q or not omitted[i])
                if any(a[z - 1] - a[y - 1] <= a[y - 1] - a[x - 1]
                       for x, y, z in zip(prefix, prefix[1:], prefix[2:])):
                    continue
                length = n - sum(omitted)
                if best_omitted is None or length > best_len or (
                    length == best_len and prefix < best_prefix
                ):
                    best_len = length
                    best_prefix = prefix
                    best_omitted = tuple(omitted)
                if K is not None and best_len >= K:
                    return result('FEASIBLE', 'certified witness')
                continue
            stack.append((t, rem, 1))
            if R[t - 1][rem]:
                stack.append((t - 1, rem, 0))
        upper = best_len
        return result('OPTIMAL' if K is None else 'INFEASIBLE',
                      'all feasible partitions examined')
    except _BudgetExceeded as exc:
        return result('RESOURCE_LIMIT', str(exc))
    except (MemoryError, OverflowError):
        return result('RESOURCE_LIMIT', 'allocation failed')


class _BudgetExceeded(Exception):
    pass
