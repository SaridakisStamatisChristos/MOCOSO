"""G12 exact linear-time certificate for witnesses with at most two omissions.

Contract: n>=2, arbitrary signed integers, U/2<m<=U, h=U-m<n.
Returns canonical optimum tuple (possibly empty) when certified; returns None
when the optimum might require >=3 omitted indices. No false positives.

Worst-case time O(n+h)=O(n), O(h+1) auxiliary wide words, excluding
read-only input and one returned tuple. Python RSS and global SOTA are NOT
claimed. For a failed fixed compulsory suffix, returns () exactly.
"""
from __future__ import annotations


class _SelectedIndices:
    """Emit exactly one returned tuple without an output-sized temporary.

    The length hint gives tuple() the exact final allocation in CPython.
    This is a research implementation detail, not an RSS guarantee.
    """
    def __init__(self,n,omissions,count):
        self.n=n
        self.omissions=omissions
        self.i=1
        self.cursor=0
        self.remaining=count

    def __iter__(self):
        return self

    def __length_hint__(self):
        return self.remaining

    def __next__(self):
        while self.i<=self.n:
            index=self.i
            self.i+=1
            if (self.cursor<len(self.omissions) and
                    self.omissions[self.cursor]==index):
                self.cursor+=1
            else:
                self.remaining-=1
                return index
        raise StopIteration


def certify_up_to_two_omissions(a, m, *, counters=None):
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
    for k in range(1,p+1):
        bad[k] = bad[k-1] + int(
            k >= 3 and a[k-3] + a[k-1] <= 2*a[k-2])
    bad_total = bad[p]
    tested_pairs = 0

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

    if valid((h,)):
        if counters is not None:
            counters.update(status="one_omission",pairs_checked=0)
        return tuple(_SelectedIndices(n,(h,),n-1))

    # Larger first omitted index gives the lexicographically smaller
    # selected tuple for an equal number of omissions.
    for first in range((h-1)//2,0,-1):
        second = h-first
        tested_pairs += 1
        if valid((first,second)):
            if counters is not None:
                counters.update(status="two_omissions",
                                pairs_checked=tested_pairs)
            return tuple(_SelectedIndices(n,(first,second),n-2))

    # For h<=5 three distinct positive indices cannot sum to h,
    # since 1+2+3=6. Exhausting all 0/1/2-omission candidates proves
    # infeasibility whenever h<=5.
    if counters is not None:
        counters.update(status="infeasible" if h<=5 else "unresolved",
                        pairs_checked=tested_pairs)
    return () if h<=5 else None
