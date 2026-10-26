"""G11 engineering hybrid: bounded-deficit direct/G8 and large-deficit G10.

Exact canonical full selected-index tuple in U/2<m<=U, h=U-m<n.
Composes previously verified algorithms; not a novel primitive or a
worldwide SOTA claim. With fixed thresholds, the G10 wide-word bound
O(n+(h+1)**(5/2)*log(h+2)) time / O((h+1)**2) auxiliary space carries over
as an asymptotic upper bound. Runtime constants remain empirical.
"""
from __future__ import annotations

from experiments.v03.g10_direct_next import solve_g10
from experiments.v03.g11_bounded_g8 import solve_g8

SMALL_H = 18
G8_H_LIMIT = 64


def _validated_h(a,m,*,check_values=True):
    n=len(a)
    U=n*(n+1)//2
    if (type(m) is not int or m<2 or not U<2*m or m>U
            or (check_values and any(type(v) is not int for v in a))):
        raise ValueError("requires signed integer values and U/2<m<=U")
    h=U-m
    if h>=n:
        raise ValueError("requires h<n")
    return h


def solve_direct(a,m):
    """Exact omission-partition enumeration, only for h <= SMALL_H.

    A compact core test uses the two compulsory anchors, and a single scan
    verifies all fully compulsory suffix triples. Partitions have distinct
    positive parts, each representing an omitted original 1-based index.
    """
    h=_validated_h(a,m)
    if h>SMALL_H:
        raise ValueError("direct solver is only for bounded h")
    n=len(a)
    p=min(n,h+2)
    for k in range(h+3,n+1):
        if a[k-3]+a[k-1]<=2*a[k-2]:
            return ()
    best=None

    def consider(parts):
        nonlocal best
        omissions=tuple(parts)
        if best is not None and (len(omissions)>len(best) or
                (len(omissions)==len(best) and omissions<=best)):
            return
        dropped=set(omissions)
        prefix=[i for i in range(1,p+1) if i not in dropped]
        if any(a[prefix[k]-1]+a[prefix[k+2]-1]<=
               2*a[prefix[k+1]-1] for k in range(len(prefix)-2)):
            return
        best=omissions

    def partitions(remainder,next_part,parts):
        if remainder==0:
            consider(parts)
            return
        for value in range(next_part,remainder+1):
            parts.append(value)
            partitions(remainder-value,value+1,parts)
            parts.pop()

    partitions(h,1,[])
    if best is None:
        return ()
    omitted=set(best)
    return tuple(i for i in range(1,n+1) if i not in omitted)


def solve_g11(a,m,*,counters=None):
    """Research-only deterministic static threshold router.

    For counters, reports which mechanism ran; internal G10 counters are
    preserved under a nested key to avoid mislabeling G8/direct estimates.
    """
    # Delegate full element validation to the selected exact subsolver.
    # The direct solver also validates the array before enumeration.
    h=_validated_h(a,m,check_values=False)
    if h<=SMALL_H:
        answer=solve_direct(a,m)
        mode="direct"
    elif h<=G8_H_LIMIT:
        answer=solve_g8(a,m)
        mode="g8_bounded"
    else:
        nested={} if counters is not None else None
        answer=solve_g10(a,m,counters=nested)
        mode="g10"
    if counters is not None:
        counters.update(mode=mode,h=h)
        if mode=="g10":
            counters.update(nested)
    return answer
