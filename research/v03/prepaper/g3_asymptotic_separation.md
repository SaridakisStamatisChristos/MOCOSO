# G3 — Asymptotic separation from the existing T1 enumerator

**Date:** 2026-10-24 UTC. Algorithm Foundry. **Claim scope:** separation of two **particular MOCOSO implementations**, not a novel complexity lower bound for the overall optimization problem, not a lower bound against all conceivable algorithms.

Let h>=1 and n=h+1. Then U=n(n+1)/2 and m=U-h. For h>=3, m>U/2: the inequality h<U/2 follows since U≈h²/2. For smaller positive h, check the high-modulus condition directly. Thus the high-modulus specialized domain contains an infinite family with q=h and p=h+2 capped by n, so in fact p=n=h+1.

Set integer array a_i=3^(i-1). For every selected triple i<j<k we have

~~~
a_k-a_j >= 2*a_j > a_j-a_i,
~~~

so **every selected subsequence is strictly convex**. Every omission subset O ⊆ [1..h] with sum h is therefore a feasible nonempty modular candidate, and every such O is a partition of h into distinct positive parts. The number of distinct omissions is precisely P_d(h), the classical distinct-part partition function (OEIS A000009: https://oeis.org/A000009).

The G2 T1 solver (experiments/v03/deficit.py) builds a reachability table and **visits each certified full omission candidate** in optimization mode K=None; it does not terminate upon finding an incumbent unless a threshold K is supplied. Hence, on this family, T1 incurs at least Omega(P_d(h)) candidate-processing steps, without needing to bound the work at each candidate.

The G3 DP independently has worst-case O(n+p²(h+1)) = O(h³) arithmetic-word time on the same family, by its proved state-count and monotone threshold sweep. Classical distinct-part partition asymptotics grow like exp(Theta(sqrt(h))) up to polynomial factors, which is superpolynomial in h. This establishes an **asymptotic separation between the two fixed algorithms** for successful exact optimization; it does not establish an unconditional problem lower bound, nor a claim that G3 is the fastest known algorithm.

Input values 3^(i-1) have Theta(n) bit length, so the above is specifically a qualified wide-word operation separation. The bit-operation translation includes those bit widths and remains polynomial for the G3 DP; do not call the code's Python timings a formal complexity proof.

**Important completeness edge:** h=1,2 may violate the intended n=h+1 high-modulus strict inequality; the infinite asymptotic family needs only all sufficiently large h. For h>=3 and n=h+1, U=(h+1)(h+2)/2 and U/2>h follows from (h+1)(h+2)>4h, which is equivalent to h²-h+2>0 and in fact holds for every integer h>=1. Thus the family condition holds for all h>=1 for n=h+1; for h=1, n=2, U=3,m=2 and m>1.5, and for h=2,n=3,U=6,m=4>3. (The proof covers these small values too.)

**Priority:** Nothing here proves a research-first algorithmic result. The separation arises from replacing output enumeration by a known-style pseudopolynomial resource-constrained path DP, a standard idea. G1/G6 must compare prior art and assess whether this application-specific combination is scientifically significant.
