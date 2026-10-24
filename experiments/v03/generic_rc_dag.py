"""Independent generic resource-constrained pair-DAG path DP (G4 control).

Purpose: fair SEMANTIC control, not optimized production or claim of the
literature's fastest known algorithm. Forward relaxation over every legal
selected-index edge, with exact omission resource and full tuple witnesses.
Unlike G3, this implementation does NOT sort by value, threshold sweep or
share G3 recurrence/code. It copies tuples, so high-memory and slower than
compressed-witness methods; do not use it as a performance lower bound.

Only U/2 < m <= U; no time/heap cap asserted.
"""


def solve_generic_rc_dag(a, m, *, max_states=120000):
    if type(m) is not int or m < 2 or any(type(v) is not int for v in a):
        raise ValueError("integer input and m>=2 required")
    n = len(a)
    U = n * (n + 1) // 2
    if not (U < 2 * m and m <= U):
        raise ValueError("requires high-modulus regime")
    h, q = U - m, min(n, U-m)
    p = min(n, q+2)
    for k in range(q+3, n+1):
        if 2*a[k-2] >= a[k-3]+a[k-1]:
            return ()
    cells = (p*(p-1)//2)*(h+1)
    if cells > max_states:
        raise MemoryError("generic comparator registered state cap exceeded")

    def W(x):
        return x*(x+1)//2

    def gap(j,k):
        if (j <= q and k >= q+2) or (j >= q+1 and k > j+1):
            return None
        return W(min(k-1,q))-W(min(j,q))

    def offer(table,key,seq):
        old=table.get(key)
        if old is None or len(seq)>len(old) or (
                len(seq)==len(old) and seq<old):
            table[key]=seq

    dp = {}
    for i in range(1,p):
        if i>q+1:
            break
        start=W(min(i-1,q))
        for j in range(i+1,p+1):
            g=gap(i,j)
            if g is not None and start+g<=h:
                offer(dp,(i,j,start+g),(i,j))
    for j in range(2,p):
        for i in range(1,j):
            for c in range(h+1):
                path=dp.get((i,j,c))
                if path is None:
                    continue
                for k in range(j+1,p+1):
                    g=gap(j,k)
                    if g is None or c+g>h:
                        continue
                    if a[k-1]-a[j-1] <= a[j-1]-a[i-1]:
                        continue
                    offer(dp,(j,k,c+g),path+(k,))

    best=()
    if m<=n:
        best=(m,)
    tail=tuple(range(p+1,n+1))
    for (i,j,c),partial in dp.items():
        if p>q:
            if j!=p or c!=h:
                continue
        else:
            if c+W(q)-W(j)!=h:
                continue
        whole=partial+tail
        if len(whole)>len(best) or (
                len(whole)==len(best) and whole<best):
            best=whole
    assert sum(best)%m==0 and all(
        a[k-1]-a[j-1]>a[j-1]-a[i-1]
        for i,j,k in zip(best,best[1:],best[2:])
    )
    return best
