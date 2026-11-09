"""Library copy of jet_point from kdv_checks.py (KdV N-soliton jets mod p, X random)."""
import random
from itertools import combinations
from modlin import P, inv, cumulants_from_moments


def jet_point(ks, K):
    N = len(ks)
    A = {}
    for i, j in combinations(range(N), 2):
        q = (ks[i] - ks[j]) * inv(ks[i] + ks[j]) % P
        A[(i, j)] = q * q % P
    while True:
        X = [random.randrange(1, P) for _ in range(N)]
        terms = []
        for m in range(1 << N):
            S = [i for i in range(N) if m >> i & 1]
            aS = 1
            for i, j in combinations(S, 2):
                aS = aS * A[(i, j)] % P
            mon = aS
            for i in S:
                mon = mon * X[i] % P
            sig = sum(ks[i] for i in S) % P
            terms.append((mon, sig))
        f = sum(t[0] for t in terms) % P
        if f == 0:
            continue
        fi = inv(f)
        r = [1]
        for n in range(1, K + 3):
            r.append(sum(mon * pow(sig, n, P) for mon, sig in terms) % P * fi % P)
        kap = cumulants_from_moments(r, K + 2)
        return [2 * kap[j + 2] % P for j in range(K + 1)]  # u_j = 2 D^{j+2} log f


