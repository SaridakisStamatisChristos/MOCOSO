"""Independent exact edge-weight-ordered DP with bitmask lex witnesses.

This algorithm is algorithmically different from the two-last-indices sweep:
it maintains only per-vertex/residue prefix states, grouped by edge difference.
"""

def solve_edge(a, m):
    if not isinstance(m, int) or m < 2 or any(not isinstance(x, int) for x in a):
        raise ValueError('signed integers and m>=2 expected')
    n = len(a)
    U = n*(n+1)//2
    if m > U:
        return ()
    rows = [[(-1, 0) for _ in range(m)] for _ in range(n+1)]
    for i in range(1, n+1):
        rows[i][i % m] = (1, 1 << (n-i))
    # A bit in position n-i represents selecting index i.
    # For equal cardinalities, the numerically larger bitmask is
    # the lexicographically smaller index sequence.
    edges = sorted((a[j-1]-a[i-1], i, j)
                   for i in range(1, n+1) for j in range(i+1, n+1))
    p=0
    while p<len(edges):
        q=p+1
        while q<len(edges) and edges[q][0]==edges[p][0]:
            q+=1
        staged={}
        for _,i,j in edges[p:q]:
            jbit=1<<(n-j)
            shift=j%m
            for r, (ell, bits) in enumerate(rows[i]):
                if ell < 0:
                    continue
                nr=r+shift
                if nr>=m:nr-=m
                cand=(ell+1, bits|jbit)
                key=j,nr
                old=staged.get(key,(-1,0))
                if cand > old:
                    staged[key]=cand
        # Apply only after the entire equal-difference batch was read.
        for (j,r), candidate in staged.items():
            if candidate>rows[j][r]:
                rows[j][r]=candidate
        p=q
    best=(0,0)
    for i in range(1,n+1):
        if rows[i][0]>best:
            best=rows[i][0]
    return tuple(i for i in range(1,n+1) if best[1]>>(n-i)&1)
