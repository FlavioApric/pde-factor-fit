"""OP-NL: checks for S4ID-K1 (Burgers N-shocks: no autonomous relation of degree <= N).
Only a CHECK of the written proof (PROOF_PACKAGE.md §2). Exact arithmetic (SymPy over Q, or mod a prime)."""
import random
import sys
import os
from itertools import combinations_with_replacement
from math import comb
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sympy as sp
from sympy.utilities.iterables import partitions
from modlin import P, rank_mod, monomials, cumulants_from_moments

ok = 0
tot = 0


def report(name, cond, info=""):
    global ok, tot
    tot += 1
    ok += bool(cond)
    print(("OK  " if cond else "FAIL"), name, info)


# ---------- A. Lemma K1' (power sums p_mu, l(mu) <= N, independent in N variables) ----------
for N in range(1, 5):
    xs = sp.symbols('x1:%d' % (N + 1))
    for n in range(1, 9):
        mus = []
        for prt in partitions(n):
            mu = []
            for part, mult in prt.items():
                mu += [part] * mult
            if len(mu) <= N:
                mus.append(tuple(sorted(mu, reverse=True)))
        polys = []
        for mu in mus:
            e = sp.Integer(1)
            for part in mu:
                e *= sum(x ** part for x in xs)
            polys.append(sp.Poly(sp.expand(e), *xs))
        monos = sorted({m for q in polys for m in q.as_dict().keys()})
        M = sp.Matrix([[q.as_dict().get(m, 0) for m in monos] for q in polys])
        r = M.rank()
        report("K1' N=%d n=%d" % (N, n), r == len(mus), "(#mu=%d, rank=%d)" % (len(mus), r))

# ---------- A2. triangularity p_mu = c_mu m_mu + (shorter lambda) ----------
for N in (2, 3):
    xs = sp.symbols('x1:%d' % (N + 1))
    for n in (4, 5, 6):
        for prt in partitions(n):
            mu = []
            for part, mult in prt.items():
                mu += [part] * mult
            if len(mu) > N:
                continue
            mu = sorted(mu, reverse=True)
            e = sp.Integer(1)
            for part in mu:
                e *= sum(x ** part for x in xs)
            d = sp.Poly(sp.expand(e), *xs).as_dict()
            # every monomial exponent sorted is a coarsening; with same length only mu itself
            good = True
            cmu = 0
            for ex, c in d.items():
                lam = sorted([a for a in ex if a > 0], reverse=True)
                if len(lam) == len(mu) and lam != mu:
                    good = False
                if lam == mu and tuple(ex) == tuple(mu + [0] * (N - len(mu))):
                    cmu = c
            report("triang N=%d mu=%s" % (N, mu), good and cmu > 0, "(coeff of x^mu = %s)" % cmu)

# ---------- B. top-weight part of kappa_n = truncated cumulant (N=2, k=(1,2) and k=(2,-1)) ----------
for ks in [(1, 2), (2, -1), (3, 5)]:
    N = len(ks)
    rs = sp.symbols('r1:%d' % (N + 1))
    V = sp.Matrix([[sp.Integer(k) ** j for k in ks] for j in range(1, N + 1)])
    pvec = V.inv() * sp.Matrix(rs)
    nmax = 7
    r = [sp.Integer(1)] + [sum(sp.Integer(ks[i]) ** j * pvec[i] for i in range(N)) for j in range(1, nmax + 1)]
    r = [sp.expand(x) for x in r]
    kap = [0] * (nmax + 1)
    for n in range(1, nmax + 1):
        s = r[n]
        for m in range(1, n):
            s -= comb(n - 1, m - 1) * kap[m] * r[n - m]
        kap[n] = sp.expand(s)
    # truncated
    rt = [sp.Integer(1)] + [rs[j - 1] if j <= N else sp.Integer(0) for j in range(1, nmax + 1)]
    kt = [0] * (nmax + 1)
    for n in range(1, nmax + 1):
        s = rt[n]
        for m in range(1, n):
            s -= comb(n - 1, m - 1) * kt[m] * rt[n - m]
        kt[n] = sp.expand(s)
    lam = sp.Symbol('lam')
    for n in range(1, nmax + 1):
        sub = {rs[l]: lam ** (l + 1) * rs[l] for l in range(N)}
        e = sp.Poly(sp.expand(kap[n].subs(sub, simultaneous=True)), lam)
        top = e.degree()
        topc = sp.expand(e.coeff_monomial(lam ** top))
        report("topweight k=%s n=%d" % (str(ks), n), top == n and sp.expand(topc - kt[n]) == 0)

# ---------- C. K1 directly, mod p: no relation of degree <= N among kappa_1..kappa_{K+1} ----------
random.seed(12345)


def k1_test(ks, K, deg):
    N = len(ks)
    # linear forms r_j (j > N) in r_1..r_N mod p: r_j = sum_i k_i^j p_i, p = V^{-1} r
    V = sp.Matrix([[sp.Integer(k) ** j for k in ks] for j in range(1, N + 1)])
    Vi = V.inv()
    L = {}
    for j in range(N + 1, K + 2):
        row = sp.Matrix([[sp.Integer(k) ** j for k in ks]]) * Vi
        L[j] = [int(sp.Rational(c).p * pow(int(sp.Rational(c).q), P - 2, P)) % P for c in row]
    monos = monomials(K + 1, deg)
    rows = []
    npts = len(monos) + 25
    for _ in range(npts):
        rr = [1] + [random.randrange(1, P) for _ in range(N)]
        for j in range(N + 1, K + 2):
            rr.append(sum(L[j][l] * rr[l + 1] for l in range(N)) % P)
        kap = cumulants_from_moments(rr, K + 1)
        y = kap[1:K + 2]
        row = []
        for m in monos:
            v = 1
            for i, e in enumerate(m):
                if e:
                    v = v * pow(y[i], e, P) % P
            row.append(v)
        rows.append(row)
    rk, _ = rank_mod(rows)
    return len(monos), rk


for ks, Kmax in [((1, 2), 7), ((2, -1), 6), ((1, 2, 3), 6), ((2, -1, 5), 5), ((1, 2, 3, 5), 5), ((1, 3, 4, 7, 9), 5)]:
    N = len(ks)
    for K in range(N, Kmax + 1):
        nm, rk = k1_test(ks, K, N)
        report("K1 deg<=N  k=%s K=%d" % (str(ks), K), rk == nm, "(#mon=%d rank=%d)" % (nm, rk))
    for K in range(N, min(Kmax, N + 2) + 1):
        nm, rk = k1_test(ks, K, N + 1)
        # sharpness: relations of degree N+1 exist from order N on (R_N); the dimension is reported (INFO)
        report("deg N+1 relations exist k=%s K=%d" % (str(ks), K), nm - rk >= 1,
               "(INFO dim J cap A_{<=N+1,<=K} = %d)" % (nm - rk))

print("TOTAL %d/%d OK" % (ok, tot))
