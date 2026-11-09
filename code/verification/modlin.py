"""Utility: exact linear algebra modulo a prime with numpy (int64).
Used only as a CHECK. Full column rank mod p implies linear independence over Q
of the corresponding p-integral rational vectors."""
import numpy as np

P = 2147483629  # prime < 2^31


def inv(a, p=P):
    return pow(int(a) % p, p - 2, p)


def rank_mod(M, p=P):
    """Rank of integer matrix M (rows x cols) modulo p; returns rank and a kernel basis of columns."""
    A = np.array(M, dtype=np.int64) % p
    rows, cols = A.shape
    r = 0
    pivcols = []
    for c in range(cols):
        if r >= rows:
            break
        nz = np.nonzero(A[r:, c])[0]
        if nz.size == 0:
            continue
        i = r + nz[0]
        if i != r:
            A[[r, i]] = A[[i, r]]
        iv = inv(A[r, c], p)
        A[r] = (A[r] * iv) % p
        col = A[:, c].copy()
        col[r] = 0
        nzr = np.nonzero(col)[0]
        if nzr.size:
            A[nzr] = (A[nzr] - (col[nzr, None] * A[r][None, :]) % p) % p
        pivcols.append(c)
        r += 1
    # kernel (null space of columns): free columns
    free = [c for c in range(cols) if c not in set(pivcols)]
    ker = []
    for f in free:
        v = np.zeros(cols, dtype=np.int64)
        v[f] = 1
        for k, pc in enumerate(pivcols):
            v[pc] = (-A[k, f]) % p
        ker.append(v)
    return r, ker


def monomials(nvars, maxdeg):
    """exponent tuples of total degree <= maxdeg"""
    out = []

    def rec(i, rem, cur):
        if i == nvars:
            out.append(tuple(cur))
            return
        for e in range(rem + 1):
            cur.append(e)
            rec(i + 1, rem - e, cur)
            cur.pop()
    rec(0, maxdeg, [])
    return out


def weighted_monomials(weights, W, exact=False):
    out = []

    def rec(i, rem, cur):
        if i == len(weights):
            if (not exact) or rem == 0:
                out.append(tuple(cur))
            return
        e = 0
        while e * weights[i] <= rem:
            cur.append(e)
            rec(i + 1, rem - e * weights[i], cur)
            cur.pop()
            e += 1
    rec(0, W, [])
    return out


def cumulants_from_moments(r, nmax, p=P):
    """r[1..nmax] moments (r[0]=1). kappa_n = r_n - sum_{m=1}^{n-1} C(n-1,m-1) kappa_m r_{n-m} (mod p)."""
    from math import comb
    kap = [0] * (nmax + 1)
    for n in range(1, nmax + 1):
        s = r[n]
        for m in range(1, n):
            s -= comb(n - 1, m - 1) * kap[m] * r[n - m]
        kap[n] = s % p
    return kap
