"""G14 exact linear certificate: G13 plus bounded three-omission search.

With any originally bad adjacent triple, every feasible three-index omitted
set must hit it. Exact omitted sum h then yields three ordered O(h) streams;
their 3-way merge and constant-local validation take O(h) work. For h<=9
the certificate is globally complete because 1+2+3+4=10.
Returns an exact globally canonical tuple or None (safe abstention).
Worst-case O(n+h)=O(n) time, O(h+1) auxiliary wide words.
"""
from __future__ import annotations

from heapq import merge
from experiments.v03.g13_two_sided_certificate import certify_g13
from experiments.v03.g10_direct_next import _SelectedIndices


def certify_g14(a,m,*,counters=None):
    earlier={}
    result=certify_g13(a,m,counters=earlier)
    if result is not None:
        if counters is not None:
            counters.update(earlier)
        return result

    n=len(a)
    h=n*(n+1)//2-m
    p=min(n,h+2)
    bad=[0]*(p+1)
    first_bad=None
    for k in range(1,p+1):
        failed=k>=3 and a[k-3]+a[k-1]<=2*a[k-2]
        bad[k]=bad[k-1]+int(failed)
        if failed and first_bad is None:
            first_bad=k
    count_bad=bad[p]

    def valid_three(omitted):
        # Union of at most 3 length-3 bad-triple endpoint intervals.
        gone=0
        last=2
        for q in omitted:
            lo=max(3,q,last+1)
            hi=min(p,q+2)
            if lo<=hi:
                gone+=bad[hi]-bad[lo-1]
                last=hi
        if gone!=count_bad:
            return False
        endpoints=set()
        for q in omitted:
            endpoints.update(range(q+1,min(p,q+5)+1))
        for k in endpoints:
            if k in omitted:
                continue
            preceding=[]
            index=k-1
            while index>=1 and len(preceding)<2:
                if index not in omitted:
                    preceding.append(index)
                index-=1
            if len(preceding)==2:
                middle,first=preceding
                if a[first-1]+a[k-1]<=2*a[middle-1]:
                    return False
        return True

    if count_bad>9:
        if counters is not None:
            counters.update(status='unresolved_bad_gt_nine',triples_checked=0)
        return None

    if first_bad is None:
        if h>9:
            if counters is not None:
                counters.update(status='unresolved_no_bad_anchor',
                                triples_checked=0)
            return None
        # h<=9 is an absolute bounded domain, so O(h²) enumeration remains
        # O(1) relative to unbounded n.
        triples=[]
        for first in range(1,h+1):
            for middle in range(first+1,h+1):
                last=h-first-middle
                if middle<last:
                    triples.append((first,middle,last))
        candidates=iter(sorted(triples,reverse=True))
    else:
        def with_anchor(r):
            remainder=h-r
            for first in range((remainder-1)//2,0,-1):
                last=remainder-first
                if first!=r and last!=r:
                    yield tuple(sorted((r,first,last)))
        streams=[with_anchor(r) for r in
                 (first_bad-2,first_bad-1,first_bad) if 1<=r<=h]
        # Every stream is in DESCENDING lex order: as the smaller
        # unfixed omitted index increases, the sorted triple increases.
        candidates=merge(*streams,reverse=True)

    checked=0
    previous=None
    for omitted in candidates:
        if omitted==previous:
            continue
        previous=omitted
        checked+=1
        if valid_three(omitted):
            if counters is not None:
                counters.update(status='three_omissions',
                                triples_checked=checked)
            return tuple(_SelectedIndices(n,omitted,n-3))

    if h<=9:
        if counters is not None:
            counters.update(status='h_le_nine_infeasible',
                            triples_checked=checked)
        return ()
    if counters is not None:
        counters.update(status='unresolved',triples_checked=checked)
    return None
