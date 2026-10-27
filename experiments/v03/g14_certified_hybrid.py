"""G14 partial O(n) certified early solver with unchanged G11 fallback.

Research only. Does not rewrite public modconvex.solve or historical solvers.
Unrestricted correctness and resource bounds inherit the G11/G10 conditions.
"""
from experiments.v03.g14_three_omission_certificate import certify_g14
from experiments.v03.g11_hybrid import solve_g11


def solve_g14(a,m,*,counters=None):
    details={} if counters is not None else None
    answer=certify_g14(a,m,counters=details)
    if answer is not None:
        if counters is not None:
            counters.update(mode='G14_certificate',certificate=details)
        return answer
    fallback={} if counters is not None else None
    answer=solve_g11(a,m,counters=fallback)
    if counters is not None:
        counters.update(mode='G11_fallback',certificate=details,
                        fallback=fallback)
    return answer
