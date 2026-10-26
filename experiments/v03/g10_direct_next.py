"""G10 experimental candidate: direct next-omission coordinate in event DP.

Research candidate, not externally refereed or priority-certified. Intended for
U/2 < m <= U, h=U-m<n, H=h+1. Proposed wide-word bound:
time O(n+H**(5/2)*log(h+2)), auxiliary space O(H**2).
Read research/v03/g10/G10_DIRECT_NEXT_PROOF.md for obligations/caveats.
"""
from __future__ import annotations


class _SelectedIndices:
    """Build just the returned tuple, with constant temporary workspace."""
    def __init__(self,n,omissions,count):
        self.n=n
        self.omissions=omissions
        self.count=count
        self.index=1
        self.cursor=0

    def __iter__(self):
        return self

    def __length_hint__(self):
        return self.count

    def __next__(self):
        while self.index<=self.n:
            i=self.index
            self.index+=1
            if self.cursor<len(self.omissions) and i==self.omissions[self.cursor]:
                self.cursor+=1
            else:
                self.count-=1
                return i
        raise StopIteration


def solve_g10(a,m,*,counters=None):
    n=len(a)
    U=n*(n+1)//2
    if (type(m) is not int or m<2 or not U<2*m or m>U or
            any(type(x) is not int for x in a)):
        raise ValueError('requires signed integers and U/2<m<=U')
    h=U-m
    if h>=n:
        raise ValueError('requires h<n')
    p=min(n,h+2)
    for k in range(h+3,n+1):
        if a[k-3]+a[k-1]<=2*a[k-2]:
            return ()
    def W(i):
        return i*(i+1)//2
    events=[]
    for i in range(1,p):
        for j in range(i+1,p+1):
            if (i<=h and j>=h+2) or (i>=h+1 and j>i+1):
                break
            gap=W(min(j-1,h))-W(min(i,h))
            if gap>h:
                break
            events.append((a[j-1]-a[i-1],-j,i,j,gap))
    events.sort()  # Equal differences: descending destination.
    INF=p+1
    calls=0
    relaxations=0

    def best_next(fixed,first_allowed):
        """Return (best full length, largest first omission outside fixed).

        Every non-fixed position below first_allowed is required selected.
        The second coordinate is a path-prefix minimum but a DP *maximum*
        in equal-cardinality ties; appending a fixed gap applies min().
        """
        nonlocal calls,relaxations
        calls+=1
        forbidden=[False]*(p+2)
        for i in fixed:
            forbidden[i]=True
        required=[0]*(p+2)
        for t in range(1,p+1):
            required[t]=required[t-1]+(t<first_allowed and not forbidden[t])
        first_free=[INF]*(p+3)
        for i in range(p,0,-1):
            first_free[i]=first_free[i+1] if forbidden[i] else i
        score=[[-1]*(h+1) for _ in range(p+1)]
        next_missing=[[0]*(h+1) for _ in range(p+1)]
        for i in range(1,min(p,h+1)+1):
            r=W(i-1)
            if r<=h and not forbidden[i] and required[i-1]==0:
                score[i][r]=1
                next_missing[i][r]=first_free[1] if first_free[1]<i else INF
        for _,_,i,j,g in events:
            if forbidden[i] or forbidden[j] or required[j-1]!=required[i]:
                continue
            free_gap=first_free[i+1]
            if free_gap>=j:
                free_gap=INF
            src,src_next=score[i],next_missing[i]
            dst,dst_next=score[j],next_missing[j]
            for r in range(h-g+1):
                relaxations+=1
                length=src[r]
                if length<1:
                    continue
                nxt=src_next[r] if src_next[r]<free_gap else free_gap
                if (length+1>dst[r+g] or
                        (length+1==dst[r+g] and nxt>dst_next[r+g])):
                    dst[r+g]=length+1
                    dst_next[r+g]=nxt
        length=score[p][h]
        if length<1:
            return (0,INF)
        return (length+n-p,next_missing[p][h])

    optimum,first=best_next((),1)
    if optimum==0:
        return ()
    omission_count=n-optimum
    Q=[]
    for step in range(omission_count):
        if step:
            current,first=best_next(Q,Q[-1]+1)
            assert current==optimum
        previous=Q[-1] if Q else 0
        assert previous<first<=h
        Q.append(first)
    selected=tuple(_SelectedIndices(n,Q,optimum))
    assert len(selected)==optimum and sum(selected)==m
    assert all(a[selected[k]-1]+a[selected[k+2]-1]>2*a[selected[k+1]-1]
               for k in range(len(selected)-2))
    if counters is not None:
        counters.update(queries=calls,events=len(events),
                        relaxations=relaxations,omissions=omission_count)
    return selected
