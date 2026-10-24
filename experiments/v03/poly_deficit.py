"""G3 research: exact polynomial-deficit convex-edge sweep.

This is a *research-only* high-modulus specialization. It does not modify,
import from, or replace the v0.2 production solver or the G2 T1 enumerator.

Given U/2 < m <= U, h=U-m, q=min(n,h), p=min(n,q+2):
  O(n + p^2 * (h+1)) arithmetic-word time and
  O(p^2 * (h+1)) auxiliary words, excluding input/output, assuming arithmetic
  on arbitrary signed values and DP indices fits the charged word model.

Real Python big-integer/allocator cost and hard RSS/time limits are different.
The preflight state-cell limit is a *soft research feasibility guard*, not a
process-memory ceiling. RESOURCE_LIMIT never means mathematically infeasible.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class PolyDeficitResult:
    status: str
    indices: tuple[int, ...]
    lower_bound: int
    upper_bound: int
    length: int | None
    state_cells: int
    relaxations: int
    reason: str = ""


def solve_poly_deficit(a, m, *, K=None, max_state_cells=1000000):
    """Exact max-length / full-lex witness, or a sound partial certificate.

    For K=None: OPTIMAL or RESOURCE_LIMIT.
    For integer K: FEASIBLE, INFEASIBLE or RESOURCE_LIMIT.
    max_state_cells=None disables the cooperative preflight allocation guard.
    """
    if not isinstance(m, int) or isinstance(m, bool) or m < 2:
        raise ValueError("m must be an integer >= 2")
    if any(not isinstance(v, int) or isinstance(v, bool) for v in a):
        raise ValueError("values must be signed integers")
    if K is not None and (not isinstance(K, int) or isinstance(K, bool)):
        raise ValueError("K must be an integer")
    if max_state_cells is not None and (
        isinstance(max_state_cells, bool)
        or not isinstance(max_state_cells, int)
        or max_state_cells < 0
    ):
        raise ValueError("max_state_cells must be nonnegative or None")
    n = len(a)
    U = n * (n + 1) // 2
    if not (2 * m > U and m <= U):
        raise ValueError("requires U/2 < m <= U")

    def outcome(status, seq=(), *, ub=None, cells=0, relax=0, reason=""):
        return PolyDeficitResult(
            status, tuple(seq), len(seq), n if ub is None else ub,
            len(seq) if status == "OPTIMAL" else None, cells, relax, reason,
        )

    if K is not None and K <= 0:
        return outcome("FEASIBLE", reason="empty witness reaches threshold")
    if K is not None and K > n:
        return outcome("INFEASIBLE", reason="threshold exceeds n")

    h = U - m
    q = min(n, h)
    p = min(n, q + 2)
    # All candidates contain the entire suffix [q+1..n]. Any ordinary
    # fixed triple ending at >=q+3 violates convexity for every candidate.
    for k in range(q + 3, n + 1):
        if a[k - 1] - a[k - 2] <= a[k - 2] - a[k - 3]:
            return outcome(
                "OPTIMAL" if K is None else "INFEASIBLE",
                ub=0, reason="immutable suffix fails strict convexity",
            )

    cells = p * (p - 1) // 2 * (h + 1)
    if max_state_cells is not None and cells > max_state_cells:
        return outcome(
            "RESOURCE_LIMIT", cells=cells,
            reason="cooperative state-cell preflight exceeded",
        )

    def W(t):
        return t * (t + 1) // 2

    def gap(j, k):
        """Omitted-index sum strictly between two selected indices.

        Return None if the gap skips a mandatory index >q.
        """
        if (j <= q and k >= q + 2) or (j >= q + 1 and k > j + 1):
            return None
        return W(min(k - 1, q)) - W(min(j, q))

    # F[i,j][r]: max number of FURTHER selected local indices after pair
    # (i,j), with exactly r omitted-index weight remaining after j,
    # enforcing all obligatory indices q+1..p. -1 = unreachable.
    # N[i,j][r]: first selected successor k among lex-min optimal tails.
    F = {}
    N = {}
    relaxations = 0
    try:
        asc = sorted(range(1, p + 1), key=lambda i: (a[i - 1], i))
        desc = asc[::-1]
        for j in range(p, 1, -1):
            best = [-1] * (h + 1)
            best_next = [0] * (h + 1)
            successors = [(k, gap(j, k)) for k in desc if k > j]
            successors = [(k, g) for k, g in successors
                          if g is not None and g <= h]
            cursor = 0
            for i in asc:
                if i >= j:
                    continue
                threshold = 2 * a[j - 1] - a[i - 1]
                # Because i increases in a[i], the threshold decreases.
                # All newly admissible k have a[k] > threshold (strict).
                while (cursor < len(successors)
                       and a[successors[cursor][0] - 1] > threshold):
                    k, omitted_gap = successors[cursor]
                    cursor += 1
                    suffix = F[j, k]
                    for tail_cost in range(h - omitted_gap + 1):
                        relaxations += 1
                        child = suffix[tail_cost]
                        if child < 0:
                            continue
                        total_cost = tail_cost + omitted_gap
                        length = child + 1
                        if (length > best[total_cost] or
                            (length == best[total_cost]
                             and k < best_next[total_cost])):
                            best[total_cost] = length
                            best_next[total_cost] = k
                row = best.copy()
                pointer = best_next.copy()
                # Termination permitted if no obligatory local indices remain.
                # If p=q=n, all trailing indices may be omitted at a cost.
                if p <= q or j == p:
                    tail_cost = W(q) - W(j) if j <= q else 0
                    if tail_cost <= h and row[tail_cost] < 0:
                        row[tail_cost] = 0
                F[i, j] = row
                N[i, j] = pointer

        best_seq = ()
        best_len = 0
        best_pair = None
        if m <= n:  # Only possible for very small valid n, notably n=2.
            best_seq = (m,)
            best_len = 1

        # Complete the candidate by choosing its first two local indices.
        # Omitted positions before i, and between i,j, are charged once.
        fixed_beyond_p = n - p
        for (i, j), row in F.items():
            if i > q + 1:  # Would omit mandatory q+1.
                continue
            skipped_between = gap(i, j)
            if skipped_between is None:
                continue
            required = h - W(min(i - 1, q)) - skipped_between
            if not (0 <= required <= h):
                continue
            extension = row[required]
            if extension < 0:
                continue
            length = 2 + extension + fixed_beyond_p
            if (length > best_len or
                (length == best_len and
                 (best_pair is None or (i, j) < best_pair))):
                best_len = length
                best_pair = (i, j)

        if best_pair is not None:
            i, j = best_pair
            selected = [i, j]
            remaining = h - W(min(i - 1, q)) - gap(i, j)
            while True:
                k = N[i, j][remaining]
                if k == 0:
                    break
                cost = gap(j, k)
                if cost is None:
                    raise AssertionError("mandatory gap skipped")
                remaining -= cost
                selected.append(k)
                i, j = j, k
            assert remaining == (W(q) - W(j) if p <= q and j <= q else 0)
            selected.extend(range(p + 1, n + 1))
            best_seq = tuple(selected)

        # Redundant end-to-end soundness assertion in research implementation.
        if best_seq:
            assert sum(best_seq) == m
            assert all(
                a[z - 1] - a[y - 1] > a[y - 1] - a[x - 1]
                for x, y, z in zip(best_seq, best_seq[1:], best_seq[2:])
            )
        ub = len(best_seq)
        if K is None:
            return outcome("OPTIMAL", best_seq, ub=ub,
                           cells=cells, relax=relaxations)
        if ub >= K:
            return outcome("FEASIBLE", best_seq, ub=ub,
                           cells=cells, relax=relaxations)
        return outcome("INFEASIBLE", best_seq, ub=ub,
                       cells=cells, relax=relaxations)
    except MemoryError:
        # This is best effort: a catastrophic allocation failure or process
        # kill may prevent any result object from being constructed.
        return outcome("RESOURCE_LIMIT", cells=cells, relax=relaxations,
                       reason="Python allocation failed")
