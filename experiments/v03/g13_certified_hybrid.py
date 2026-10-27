"""G13 research hybrid: exact two-sided O(n) certificate then G11 fallback.

This does NOT assert a better unrestricted asymptotic bound than the
conditional G10 theorem, and it does NOT modify modconvex.solve.
"""
from experiments.v03.g13_two_sided_certificate import certify_g13
from experiments.v03.g11_hybrid import solve_g11


def solve_g13(a,m,*,counters=None):
    record={} if counters is not None else None
    output=certify_g13(a,m,counters=record)
    if output is not None:
        if counters is not None:
            counters.update(mode="G13_certificate",certificate=record)
        return output
    extra={} if counters is not None else None
    output=solve_g11(a,m,counters=extra)
    if counters is not None:
        counters.update(mode="G11_fallback",certificate=record,
                        fallback=extra)
    return output
