"""OP-NL: KdV N-solitons, generator Pi_N of J_u cap C[y_0..y_N] (formal family, X free).
CHECK only (PROOF_PACKAGE.md §3). Computations mod a prime with numpy; X_i random in GF(p).
u = 2 D^2 log f, f = sum_S a_S X^S, D X_i = k_i X_i, a_S = prod_{i<j in S} ((k_i-k_j)/(k_i+k_j))^2.
Search: minimal weight W (wt y_j = j+2) such that some nonzero polynomial with monomials of weight <= W
vanishes on the family (any relation for fixed k is a multiple of Pi_N(k); Pi(k;y) is weighted-homogeneous
in (k,y) by the scaling symmetry, so Pi_N(k0) involves only monomials of weight <= W_N)."""
import sys
import os
import random
import time
from itertools import combinations
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from modlin import P, rank_mod, weighted_monomials, cumulants_from_moments, inv
import numpy as np

random.seed(2026)
ok = 0
tot = 0


def report(name, cond, info=""):
    global ok, tot
    tot += 1
    ok += bool(cond)
    print(("OK  " if cond else "FAIL"), name, info, flush=True)


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


def search(ks, K, W, extra=40):
    wts = [j + 2 for j in range(K + 1)]
    monos = weighted_monomials(wts, W)
    rows = []
    for _ in range(len(monos) + extra):
        y = jet_point(ks, K)
        row = []
        for m in monos:
            v = 1
            for i, e in enumerate(m):
                if e:
                    v = v * pow(y[i], e, P) % P
            row.append(v)
        rows.append(row)
    rk, ker = rank_mod(rows)
    return monos, rk, ker


def analyse(monos, vec, K):
    supp = [monos[i] for i in range(len(monos)) if vec[i] % P]
    deg = max(sum(m) for m in supp)
    degN = max(m[K] for m in supp)
    wmax = max(sum((j + 2) * m[j] for j in range(K + 1)) for m in supp)
    y0pure = any(m[0] == deg and sum(m) == deg for m in supp)
    return deg, degN, wmax, y0pure, len(supp)


# N = 1: expect W = 6, Pi_1 = y1^2 - k^2 y0^2 + 2 y0^3 (degree 3)
for ks in [(1,), (3,)]:
    for W in range(2, 7):
        monos, rk, ker = search(ks, 1, W)
        if len(monos) - rk > 0:
            break
    d = analyse(monos, ker[0], 1)
    report("N=1 k=%s: minimal weight 6, degree 3" % (ks,), W == 6 and d[0] == 3, "(W=%d, deg,deg_yN,wmax,y0^top,|supp| = %s)" % (W, d))

# N = 2: expect W = 16, degree 8 for several k (the V-ex of S4-ID was for k=(1,2) only)
for ks in [(1, 2), (1, 3), (2, 5), (3, 7), (1, 6)]:
    t0 = time.time()
    found = None
    for W in range(10, 19):
        monos, rk, ker = search(ks, 2, W)
        if len(monos) - rk > 0:
            found = W
            break
    d = analyse(monos, ker[0], 2)
    report("N=2 k=%s: minimal weight 16, degree 8, nullity 1" % (ks,), found == 16 and d[0] == 8 and len(ker) == 1,
           "(W=%s, deg,deg_y2,wmax,y0^8 present,|supp| = %s, %.1fs)" % (found, d, time.time() - t0))

# N = 3 (formal family; generic k, here k=(1,2,4) and (1,3,7))
for ks in [(1, 2, 4), (1, 3, 7)]:
    for W in [int(a) for a in (sys.argv[1:] or ["24", "30", "36", "40"])]:
        t0 = time.time()
        monos, rk, ker = search(ks, 3, W, extra=60)
        nul = len(monos) - rk
        info = "#mon=%d nullity=%d (%.1fs)" % (len(monos), nul, time.time() - t0)
        if nul:
            info += " first kernel vector: deg,deg_y3,wmax,y0pure,|supp| = %s" % (analyse(monos, ker[0], 3),)
        print("INFO N=3 k=%s W=%d: %s" % (ks, W, info), flush=True)

print("TOTAL %d/%d OK" % (ok, tot))
