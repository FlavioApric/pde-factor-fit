# Audit S-CHECK-F10-B: controllo indipendente (senza Gelfand-Dickey ne' flusso di Mumford) di delta_N(2N)(k) >= N+1
# per k razionali fissati: getti dell'N-solitone di Hirota calcolati dai momenti D^m f / f (cumulanti), mod p.
import random, itertools, sys, time
import numpy as np
P = 2147483629
def inv(a): return pow(a % P, P-2, P)
def rank_mod(M):
    M = M.copy() % P; r = 0; rows, cols = M.shape
    for c in range(cols):
        nz = np.nonzero(M[r:, c])[0]
        if len(nz) == 0: continue
        piv = r + nz[0]
        if piv != r: M[[r, piv]] = M[[piv, r]]
        M[r] = (M[r]*inv(int(M[r, c]))) % P
        oth = np.nonzero(M[:, c])[0]; oth = oth[oth != r]
        if len(oth): M[oth] = (M[oth] - (M[oth, c].reshape(-1, 1)*M[r]) % P) % P
        r += 1
        if r == rows: break
    return r
def jets(k, K):
    N = len(k)
    X = [random.randrange(1, P) for _ in range(N)]
    terms = []
    for r in range(N+1):
        for S in itertools.combinations(range(N), r):
            a = 1
            for i, j in itertools.combinations(S, 2):
                a = a*((k[i]-k[j]) % P)**2 % P*inv((k[i]+k[j])**2) % P
            for i in S: a = a*X[i] % P
            terms.append((a, sum(k[i] for i in S) % P))
    f = sum(a for a, _ in terms) % P
    F = [(sum(a*pow(lam, m, P) for a, lam in terms) % P)*inv(f) % P for m in range(K+3)]
    from math import comb
    kap = [0]*(K+3)
    for n in range(1, K+3):
        kap[n] = (F[n] - sum(comb(n-1, m-1)*kap[m]*F[n-m] for m in range(1, n))) % P
    return [2*kap[j+2] % P for j in range(K+1)]
def mons(nv, d):
    out = []
    for tot in range(d+1):
        for comb_ in itertools.combinations_with_replacement(range(nv), tot):
            e = [0]*nv
            for i in comb_: e[i] += 1
            out.append(tuple(e))
    return out
def test(k, K, d):
    ms = mons(K+1, d); npts = len(ms)+20
    M = np.zeros((npts, len(ms)), dtype=np.int64)
    for i in range(npts):
        y = jets(k, K)
        for j, m in enumerate(ms):
            t = 1
            for v, e in enumerate(m):
                if e: t = t*pow(y[v], e, P) % P
            M[i, j] = t
    return len(ms) - rank_mod(M), len(ms)
random.seed(2026)
for k in [(1, 3), (2, 7), (1, 3, 4), (2, 5, 9), (1, 3, 4, 6)]:
    N = len(k); K = 2*N
    t0 = time.time()
    nul, nm = test(k, K, N)
    nul2, nm2 = test(k, K, N+1) if N <= 3 else (None, None)
    print('k=%s N=%d K=%d: grado <= %d nullita=%d (monomi %d) -> %s; grado <= %d nullita=%s  [%.1fs]' % (
        k, N, K, N, nul, nm, 'nessuna relazione (delta >= N+1)' if nul == 0 else 'FAIL', N+1, nul2, time.time()-t0))
    sys.stdout.flush()
