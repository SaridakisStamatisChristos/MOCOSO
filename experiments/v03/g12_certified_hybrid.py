"""G12 research-only exact solver: linear certificate followed by G11 fallback.

The certificate is an independently auditable algorithmic improvement; it
cannot return a nonoptimal tuple. G11 is used only when >2 omissions might
be needed. G11/G10 published-performance and word-model caveats carry over.
No public modconvex.solve dispatch is altered.
"""
from __future__ import annotations

from experiments.v03.g12_linear_certificate import certify_up_to_two_omissions
from experiments.v03.g11_hybrid import solve_g11


def solve_g12(a,m,*,counters=None):
    info={} if counters is not None else None
    witness=certify_up_to_two_omissions(a,m,counters=info)
    if witness is not None:
        if counters is not None:
            counters.update(mode="linear_certificate",certificate=info)
        return witness
    fallback={} if counters is not None else None
    witness=solve_g11(a,m,counters=fallback)
    if counters is not None:
        counters.update(mode="G11_fallback",certificate=info,
                        fallback=fallback)
    return witness
