# S-CHECK-19: controllo indipendente dei limiti inferiori di OPF5C-P9.
# (A) k generico: getti degli N-solitoni calcolati DIRETTAMENTE da f = sum_S a_S X^S e^{(sum k_i) x}
#     (serie di Taylor mod p, nessun uso di (Nov'), Mumford o Gelfand-Dickey).
# (B) k = 0 graduato (OPF5C-L8): punti di Psi_0^{-1}(S°_0) con polinomi di GD ricavati
#     indipendentemente dall'identita' del risolvente 2GG''-G'^2+4(u+lam)G^2 = 4lam (non da Lenard).
# Rango pieno mod p => nessuna relazione su Q di quel grado (direzione valida).
import sys, random, itertools, time
import numpy as np
import sympy as sp
P = 2147483587
def inv(a): return pow(a % P, P-2, P)
def modq(x):
    x = sp.Rational(x); return int(x.p) % P * inv(int(x.q)) % P
def rank_mod(M):
    M = M.copy() % P; r = 0; rows, cols = M.shape
    for c in range(cols):
        nz = np.nonzero(M[r:, c])[0]
        if len(nz) == 0: continue
        piv = r + nz[0]
        if piv != r: M[[r, piv]] = M[[piv, r]]
        M[r] = (M[r] * inv(int(M[r, c]))) % P
        oth = np.nonzero(M[:, c])[0]; oth = oth[oth != r]
        if len(oth):
            f = M[oth, c].reshape(-1, 1)
            M[oth] = (M[oth] - (f * M[r]) % P) % P
        r += 1
        if r == rows: break
    return r
def monomials(nv, d):
    out = []
    for tot in range(d+1):
        for comb in itertools.combinations_with_replacement(range(nv), tot):
            e = [0]*nv
            for i in comb: e[i] += 1
            out.append(tuple(e))
    return out
def evalmat(pts, mons):
    M = np.zeros((len(pts), len(mons)), dtype=np.int64)
    for i, y in enumerate(pts):
        for j, m in enumerate(mons):
            t = 1
            for v, e in enumerate(m):
                if e: t = t*pow(y[v], e, P) % P
            M[i, j] = t
    return M
# ---------- (A) getti dei solitoni ----------
def soliton_jet(ks, K):
    N = len(ks); km = [modq(k) for k in ks]
    X = [random.randrange(1, P) for _ in range(N)]
    M = K + 3
    fact = [1]*(M+1)
    for i in range(1, M+1): fact[i] = fact[i-1]*i % P
    F = [0]*(M+1)
    for r in range(N+1):
        for S in itertools.combinations(range(N), r):
            a = sp.Integer(1)
            for i, j in itertools.combinations(S, 2):
                a *= ((ks[i]-ks[j])/(ks[i]+ks[j]))**2
            c = modq(a)
            for i in S: c = c*X[i] % P
            ssum = sum(km[i] for i in S) % P
            pw = 1
            for m in range(M+1):
                F[m] = (F[m] + c*pw % P*inv(fact[m])) % P
                pw = pw*ssum % P
    assert F[0] != 0
    Fp = [(m+1)*F[m+1] % P for m in range(M)]
    Q = [0]*M; i0 = inv(F[0])
    for m in range(M):
        acc = Fp[m]
        for j in range(1, m+1): acc -= F[j]*Q[m-j]
        Q[m] = acc % P * i0 % P
    L = [0] + [Q[m-1]*inv(m) % P for m in range(1, M+1)]
    return [2*fact[j+2] % P * L[j+2] % P for j in range(K+1)]
def generic(N, K, ks, dmax):
    ks = [sp.Rational(k) for k in ks]
    for d in range(1, dmax+1):
        mons = monomials(K+1, d)
        pts = [soliton_jet(ks, K) for _ in range(len(mons)+15)]
        nul = len(mons) - rank_mod(evalmat(pts, mons))
        print('[A] N=%d K=%d k=%s d=%d monomi=%d nullita=%d' % (N, K, [str(k) for k in ks], d, len(mons), nul)); sys.stdout.flush()
        if nul > 0:
            print('    => delta >= %d (certificato), candidato = %d' % (d, d)); return d
    print('    => delta >= %d (certificato)' % (dmax+1)); return None
# ---------- (B) livello k = 0 ----------
Y = sp.symbols('y0:40')
def Dop(e, top): return sp.expand(sum(sp.diff(e, Y[m])*Y[m+1] for m in range(top)))
def gd(n, top):
    g = [sp.Integer(1)]
    def d(e, r):
        for _ in range(r): e = Dop(e, top)
        return e
    for m in range(1, n+1):
        acc = 4*sum(g[a]*g[m-a] for a in range(1, m))
        acc += sum(2*g[a]*d(g[m-1-a], 2) - d(g[a], 1)*d(g[m-1-a], 1) + 4*Y[0]*g[a]*g[m-1-a] for a in range(m))
        g.append(sp.expand(-acc/8))
    return g
def setup0(N):
    top = 2*N+2
    g = gd(N, top)
    sexpr = []
    for j in range(1, N+1):
        sexpr.append(g[j]); sexpr.append(sp.expand(Dop(g[j], top)/2))
    steps = []
    for i, e in enumerate(sexpr):
        c = sp.diff(e, Y[i]); assert c.is_number and c != 0
        rest = sp.expand(e - c*Y[i])
        assert all(sp.diff(rest, Y[m]) == 0 for m in range(i, top))
        steps.append((modq(c), sp.Poly(rest, *Y[:max(i, 1)]) if rest != 0 else None))
    return steps
def pmul(A, B):
    r = [0]*(len(A)+len(B)-1)
    for i, x in enumerate(A):
        for j, z in enumerate(B): r[i+j] = (r[i+j] + x*z) % P
    return r
def point0(N, steps):
    sig = [random.randrange(1, P) for _ in range(N)]
    mu = [(-s*s) % P for s in sig]
    assert len(set(mu)) == N
    U = [1]
    for m in mu: U = pmul(U, [1, (-m) % P])
    vals = [s*pow((-s*s) % P, N, P) % P for s in sig]   # V(mu)^2 = -mu^{2N+1}
    V = [0]*N
    for j in range(N):
        num = [1]; den = 1
        for i in range(N):
            if i != j: num = pmul(num, [1, (-mu[i]) % P]); den = den*((mu[j]-mu[i]) % P) % P
        assert den != 0
        c = vals[j]*inv(den) % P
        for t in range(N): V[t] = (V[t] + c*num[t]) % P
    # controllo: U | V^2 + lam^{2N+1}
    num = [1] + [0]*(2*N+1); V2 = pmul(V, V)
    num = [(x + z) % P for x, z in zip(num, [0]*(len(num)-len(V2)) + V2)]
    rem = num[:]
    for i in range(len(num)-len(U)+1):
        c = rem[i]
        for j in range(len(U)): rem[i+j] = (rem[i+j] - c*U[j]) % P
    assert all(x == 0 for x in rem)
    s = []
    for j in range(1, N+1): s += [U[j], V[j-1]]
    y = []
    for i in range(2*N):
        c, rest = steps[i]
        rv = 0
        if rest is not None:
            for mon, co in zip(rest.monoms(), rest.coeffs()):
                t = modq(co)
                for idx, e in enumerate(mon):
                    if e: t = t*pow(y[idx], e, P) % P
                rv = (rv + t) % P
        y.append((s[i] - rv) % P * inv(c) % P)
    return y
def graded(N, K, dmax):
    steps = setup0(N)
    wt = lambda m: sum((j+2)*e for j, e in enumerate(m))
    byw = {}
    for m in monomials(K+1, dmax): byw.setdefault(wt(m), []).append(m)
    best = None
    for w in sorted(byw):
        mons = byw[w]
        pts = [point0(N, steps)[:K+1] for _ in range(len(mons)+10)]
        for d in range(1, dmax+1):
            sub = [m for m in mons if sum(m) <= d]
            if not sub: continue
            nul = len(sub) - rank_mod(evalmat(pts, sub))
            if nul > 0:
                if best is None or d < best[0]: best = (d, w)
                break
    lb = best[0] if best else dmax+1
    print('[B] N=%d K=%d k=0 graduato gradi<=%d: minimo grado relazione omogenea = %s => delta_N(K)(k) >= %d per ogni k' % (N, K, dmax, best, lb)); sys.stdout.flush()
    return lb
if __name__ == '__main__':
    random.seed(1919)
    mode = sys.argv[1]
    t0 = time.time()
    if mode == 'gen':
        generic(int(sys.argv[2]), int(sys.argv[3]), sys.argv[4].split(','), int(sys.argv[5]))
    else:
        graded(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
    print('   [%.1fs]' % (time.time()-t0))
