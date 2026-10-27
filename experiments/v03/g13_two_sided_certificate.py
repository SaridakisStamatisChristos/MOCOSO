"""G13 two-sided linear-time certificates: near-complete optimum OR infeasibility.

Contract: n>=2, arbitrary signed integers, U/2<m<=U, h=U-m<n.
Returns canonical optimum tuple (possibly empty) when certified; returns None
when the optimum might require >=3 omitted indices. No false positives.

Worst-case time O(n+h)=O(n), O(h+1) auxiliary wide words, excluding
read-only input and one returned tuple. Python RSS and global SOTA are NOT
claimed. Also detects impossible instances by minimum-weight hitting of failed triples.
"""
from __future__ import annotations

from experiments.v03.g10_direct_next import _SelectedIndices


def certify_g13(a, m, *, counters=None):
    n = len(a)
    U = n * (n + 1) // 2
    if (type(m) is not int or m < 2 or not U < 2*m or m > U or
            any(type(value) is not int for value in a)):
        raise ValueError("requires signed integer values and U/2 < m <= U")
    h = U - m
    if h >= n:
        raise ValueError("requires h < n")
    p = min(n, h+2)

    # All indices >h are compulsory, so these triples cannot be repaired.
    for k in range(h+3, n+1):
        if a[k-3] + a[k-1] <= 2*a[k-2]:
            if counters is not None:
                counters.update(status="suffix_infeasible",pairs_checked=0)
            return ()

    bad = [0] * (p+1)
    first_bad = None
    for k in range(1,p+1):
        failed = k >= 3 and a[k-3] + a[k-1] <= 2*a[k-2]
        bad[k] = bad[k-1] + int(failed)
        if failed and first_bad is None:
            first_bad = k
    bad_total = bad[p]
    tested_pairs = 0

    def min_required_weight():
        """Minimum total omitted-index weight hitting all bad triples.

        DP mask records omission of the previous two original positions;
        deleting position k costs k, and no index beyond h is deletable.
        Every surviving original invalid triple would invalidate the result.
        """
        INF = h+1
        dp = [0, INF, INF, INF]
        for k in range(1,p+1):
            failure = bad[k] != bad[k-1]
            nxt = [INF]*4
            for mask, cost in enumerate(dp):
                if cost > h:
                    continue
                for omit in ((0,1) if k <= h else (0,)):
                    if failure and mask==0 and omit==0:
                        continue
                    newmask = ((mask&1)<<1)|omit
                    candidate = cost + k*omit
                    if candidate < nxt[newmask]:
                        nxt[newmask] = candidate
            dp = nxt
            if min(dp) > h:
                return INF
        return min(dp)

    def valid(omitted):
        # Exactly the original adjacent triples containing an omitted
        # position may disappear. Every other bad original triple persists.
        left = max(3,omitted[0])
        right = min(p,omitted[0]+2)
        gone = bad[right]-bad[left-1] if right>=left else 0
        if len(omitted)==2:
            left2 = max(3,omitted[1])
            right2 = min(p,omitted[1]+2)
            if right2>=left2:
                gone += bad[right2]-bad[left2-1]
            overlap_left = max(left,left2)
            overlap_right = min(right,right2)
            if overlap_right>=overlap_left:
                gone -= bad[overlap_right]-bad[overlap_left-1]
        if gone != bad_total:
            return False

        # Every affected selected triple crosses an omitted index. With at
        # most two omissions it ends at most four original positions later.
        endings = set()
        for missing in omitted:
            endings.update(range(missing+1,min(p,missing+4)+1))
        for k in endings:
            if k in omitted:
                continue
            previous = []
            i = k-1
            while i >= 1 and len(previous) < 2:
                if i not in omitted:
                    previous.append(i)
                i -= 1
            if len(previous)==2:
                j,first = previous
                if a[first-1] + a[k-1] <= 2*a[j-1]:
                    return False
        return True

    if h == 0:
        if counters is not None:
            counters.update(status="all_selected" if bad_total==0
                            else "infeasible",pairs_checked=0)
        return tuple(range(1,n+1)) if bad_total==0 else ()

    # One deletion eliminates at most three originally invalid triples.
    if bad_total <= 3 and valid((h,)):
        if counters is not None:
            counters.update(status="one_omission",pairs_checked=0)
        return tuple(_SelectedIndices(n,(h,),n-1))

    # Every originally bad adjacent triple must contain an omitted index.
    # If one bad triple exists, at least one of its three indices is omitted,
    # leaving at most THREE two-part candidates under exact omitted sum h.
    if bad_total == 0:
        pairs = ((u,h-u) for u in range((h-1)//2,0,-1))
    elif bad_total <= 6:
        options = set()
        for index in (first_bad-2,first_bad-1,first_bad):
            other = h-index
            if 1<=index<=h and 1<=other<=h and index!=other:
                options.add(tuple(sorted((index,other))))
        pairs = iter(sorted(options,reverse=True))
    else:
        # Two omissions eliminate at most six original adjacent triples.
        pairs = iter(())

    for first, second in pairs:
        tested_pairs += 1
        if valid((first,second)):
            if counters is not None:
                counters.update(status="two_omissions",
                                pairs_checked=tested_pairs)
            return tuple(_SelectedIndices(n,(first,second),n-2))

    # Three distinct positive omission indices sum at least 1+2+3=6.
    if h<=5:
        if counters is not None:
            counters.update(status="h_le_five_infeasible",
                            pairs_checked=tested_pairs)
        return ()

    # Necessary condition for any feasible omitted set: it hits each bad
    # original triple. If even the MINIMUM weight hitting set exceeds h,
    # no exact-sum omitted set can exist. Otherwise abstain safely.
    if bad_total > 0 and min_required_weight() > h:
        if counters is not None:
            counters.update(status="weighted_hitting_infeasible",
                            pairs_checked=tested_pairs)
        return ()

    if counters is not None:
        counters.update(status="unresolved",pairs_checked=tested_pairs)
    return None
