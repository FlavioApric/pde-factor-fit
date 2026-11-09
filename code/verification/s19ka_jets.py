from fractions import Fraction as Fr
from itertools import combinations
from math import factorial

def ps_mul(a, b, M):
    c = [Fr(0)]*M
    for i in range(M):
        if a[i] == 0: continue
        for j in range(M-i):
            c[i+j] += a[i]*b[j]
    return c

def ps_inv(a, M):
    b = [Fr(0)]*M
    b[0] = 1/a[0]
    for n in range(1, M):
        s = sum(a[i]*b[n-i] for i in range(1, n+1))
        b[n] = -s/a[0]
    return b

def soliton_jets(k, Xv, M):
    """jets y_0..y_{M-1} of u=2(log f)'' at x=0, X_i(x)=Xv_i exp(k_i x); exact for complex-free rationals"""
    N = len(k)
    L = M + 3
    f = [Fr(0)]*L
    for r in range(N+1):
        for S in combinations(range(N), r):
            aS = Fr(1)
            for i, j in combinations(S, 2):
                aS *= Fr(k[i]-k[j], 1)**2 / Fr(k[i]+k[j], 1)**2
            c = aS
            for i in S: c *= Xv[i]
            K = sum(k[i] for i in S)
            for n in range(L):
                f[n] += c * Fr(K)**n / factorial(n)
    # (log f)' = f'/f
    fp = [f[n+1]*(n+1) for n in range(L-1)] + [Fr(0)]
    lp = ps_mul(fp, ps_inv(f, L), L)
    # u = 2 (lp)'
    u = [2*lp[n+1]*(n+1) for n in range(L-1)]
    return [u[j]*factorial(j) for j in range(M)]
