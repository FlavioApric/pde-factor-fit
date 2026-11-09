# OP-F5C: delta_N(K) = grado minimo di una relazione non nulla in C[y_0..y_K] sulla famiglia degli N-solitoni
# (k fissato), calcolato come grado minimo nell'ideale I(Z_k) ∩ C[y_0..y_K], Z_k = Psi^{-1}(M_k)
# (OPF5C-T1: Z_k = chiusura dei getti d'ordine 2N-1 degli N-solitoni, per k ammissibile).
# Punti di Z_k mod p dalla parametrizzazione sigma dello strato principale:
#   U = prod (lam + sigma_j^2), V(-sigma_j^2) = sigma_j * h(sigma_j^2), h(x) = prod (kappa_i - x), kappa_i = k_i^2/4,
# poi y dalla mappa triangolare di Gelfand-Dickey (u_j = Ghat_j, v_j = D Ghat_j / 2).
# Rango mod p della matrice di valutazione: rango pieno => nessuna relazione su Q (direzione valida);
# nullita' > 0 mod p => SOLO candidato (l'esistenza su Q va provata a parte).
# Uso: python opf5c_delta.py N K dmax [k1,k2,...]   (k omesso => k = 0, livello razionale)
import sympy as sp, pickle, sys, random, itertools, time
import numpy as np
P = 2147483629  # primo < 2^31
g = [sp.sympify(s) for s in pickle.load(open('opf5c_gd.pkl', 'rb'))]
Y = sp.symbols('y0:%d' % 40)
def Dop(e, top):
    return sp.expand(sum(sp.diff(e, Y[m])*Y[m+1] for m in range(top)))
def inv(a): return pow(a % P, P-2, P)
def setup(N, kappa):
    # coefficienti a_j = e_j(kappa) di G_inf(lam) = prod (lam + kappa_i)
    lam = sp.Symbol('lam')
    Ginf = sp.Poly(sp.Mul(*[(lam + q) for q in kappa]) if kappa else lam**N, lam)
    a = [Ginf.coeff_monomial(lam**(N-j)) for j in range(N+1)]
    sexpr = []   # s_1..s_2N come polinomi in y
    for j in range(1, N+1):
        Gh = sp.expand(sum(a[j-i]*g[i] for i in range(j+1)))
        sexpr.append(Gh)
        sexpr.append(sp.expand(Dop(Gh, 2*N)/2))
    fns = []
    # D(v_N) = D^2(Ghat_N)/2 = c*y_{2N} + resto
    sexpr.append(sp.expand(Dop(sexpr[-1], 2*N+1)))
    for i, e in enumerate(sexpr):
        c = sp.diff(e, Y[i]); assert c.is_number and c != 0
        rest = sp.expand(e - c*Y[i])
        assert all(sp.diff(rest, Y[m]) == 0 for m in range(i, 2*N+2))
        fns.append((int(sp.Rational(c).p) * inv(int(sp.Rational(c).q)) % P,
                    sp.lambdify(Y[:i] if i > 0 else [Y[0]], rest, 'sympy') if i > 0 else None,
                    rest))
    return fns, [modq(x) for x in a]
def modq(x):
    x = sp.Rational(x); return int(x.p) % P * inv(int(x.q)) % P
def polymulmod(A, B):
    r = [0]*(len(A)+len(B)-1)
    for i, x in enumerate(A):
        for j, z in enumerate(B): r[i+j] = (r[i+j] + x*z) % P
    return r
def point(N, kappa_mod, fns, restpolys):
    # sigma casuali mod p
    sig = [random.randrange(1, P) for _ in range(N)]
    mu = [(-s*s) % P for s in sig]
    # U = prod (lam - mu_j), coefficienti dal grado alto
    U = [1]
    for m in mu: U = polymulmod(U, [1, (-m) % P])
    # V(mu_j) = sigma_j * prod(kappa_i - sigma_j^2)
    vals = []
    for s in sig:
        h = 1
        for q in kappa_mod: h = h*((q - s*s) % P) % P
        if not kappa_mod: h = pow((-s*s) % P, N, P)  # k = 0: V(mu) = sigma^{2N+1} = sigma*(sigma^2)^N
        vals.append(s*h % P)
    # Lagrange: V = sum vals_j * prod_{i!=j} (lam - mu_i)/(mu_j - mu_i)
    V = [0]*N
    for j in range(N):
        num = [1]; den = 1
        for i in range(N):
            if i != j:
                num = polymulmod(num, [1, (-mu[i]) % P]); den = den*((mu[j]-mu[i]) % P) % P
        c = vals[j]*inv(den) % P
        for t in range(N): V[t] = (V[t] + c*num[t]) % P
    # s = (u1, v1, u2, v2, ...): u_j = U[j], v_j = V[j-1] (V = v1 lam^{N-1} + ... + vN)
    s = []
    for j in range(1, N+1): s += [U[j], V[j-1]]
    y = []
    for i in range(2*N):
        c, _, rest = fns[i]
        rv = evalmod(restpolys[i], y)
        y.append((s[i] - rv) % P * inv(c) % P)
    # V' = W - (y0 + lam) U, con W = (V^2 + lam*Ginf^2) / U (divisione esatta)
    Gi = A_MOD
    num = polymulmod(V, V)                      # grado 2N-2
    G2 = polymulmod(Gi, Gi) + [0]               # lam*Ginf^2, grado 2N+1
    num = [0]*(len(G2)-len(num)) + num
    num = [(x+z) % P for x, z in zip(num, G2)]
    # divisione per U monico
    rem = num[:]; W = []
    for i in range(len(num)-len(U)+1):
        c = rem[i]; W.append(c)
        for j in range(len(U)): rem[i+j] = (rem[i+j] - c*U[j]) % P
    assert all(x == 0 for x in rem), 'U non divide V^2+f'
    Ul = U + [0]
    yU = [y[0]*x % P for x in U]
    Vp = [(W[i] - Ul[i] - ([0]+yU)[i]) % P for i in range(len(W))]
    assert Vp[0] == 0 and Vp[1] == 0 if len(Vp) > N+1 else True
    vNp = Vp[-1]                                 # termine noto di V' = D(v_N)
    c, _, rest = fns[2*N]
    rv = evalmod(restpolys[2*N], y)
    y.append((vNp - rv) % P * inv(c) % P)   # sexpr[2N] = D(v_N)
    return y
def evalmod(poly, y):
    # poly: dict monom->coeff (mod p), monomi su y_0..y_{len-1}
    tot = 0
    for mon, c in poly:
        t = c
        for idx, e in mon: t = t*pow(y[idx], e, P) % P
        tot = (tot + t) % P
    return tot
def topoly(expr, nvars):
    if expr == 0: return []
    Pp = sp.Poly(expr, *Y[:max(nvars, 1)])
    out = []
    for mon, c in zip(Pp.monoms(), Pp.coeffs()):
        out.append(([(i, e) for i, e in enumerate(mon) if e > 0], modq(c)))
    return out
def rank_mod(M):
    M = M.copy() % P
    r = 0; rows, cols = M.shape
    for c in range(cols):
        piv = None
        nz = np.nonzero(M[r:, c])[0]
        if len(nz) == 0: continue
        piv = r + nz[0]
        if piv != r: M[[r, piv]] = M[[piv, r]]
        iv = inv(int(M[r, c]))
        M[r] = (M[r] * iv) % P
        others = np.nonzero(M[:, c])[0]
        others = others[others != r]
        if len(others):
            f = M[others, c].reshape(-1, 1)
            M[others] = (M[others] - (f * M[r]) % P) % P
        r += 1
        if r == rows: break
    return r
def monomials(nv, d):
    res = []
    for tot in range(d+1):
        for comb in itertools.combinations_with_replacement(range(nv), tot):
            e = [0]*nv
            for i in comb: e[i] += 1
            res.append(tuple(e))
    return res
def main():
    N = int(sys.argv[1]); K = int(sys.argv[2]); dmax = int(sys.argv[3])
    ks = [sp.Rational(x) for x in sys.argv[4].split(',')] if len(sys.argv) > 4 else []
    kappa = [k**2/4 for k in ks]
    random.seed(12345)
    global A_MOD
    fns, A_MOD = setup(N, kappa)
    restpolys = [topoly(f[2], 2*N) for f in fns]
    kappa_mod = [modq(q) for q in kappa]
    t0 = time.time()
    npts = None
    for d in range(1, dmax+1):
        mons = monomials(K+1, d)
        npts = len(mons) + 20
        pts = [point(N, kappa_mod, fns, restpolys)[:K+1] for _ in range(npts)]
        M = np.zeros((npts, len(mons)), dtype=np.int64)
        for i, yv in enumerate(pts):
            pw = [[1]*(d+1) for _ in range(K+1)]
            for v in range(K+1):
                for e in range(1, d+1): pw[v][e] = pw[v][e-1]*yv[v] % P
            for j, m in enumerate(mons):
                t = 1
                for v, e in enumerate(m):
                    if e: t = t*pw[v][e] % P
                M[i, j] = t
        rk = rank_mod(M)
        nul = len(mons) - rk
        print('N=%d K=%d k=%s d=%d: monomi=%d rango=%d nullita(mod p)=%d  [%.1fs]' % (N, K, ks if ks else '0', d, len(mons), rk, nul, time.time()-t0))
        sys.stdout.flush()
        if nul > 0:
            print('  => nessuna relazione di grado <= %d su Q; candidato delta = %d' % (d-1, d)); break
def main_graded():
    # livello k = 0: l'ideale dei getti di M_0 e' omogeneo per il peso (wt y_j = j+2), quindi basta
    # cercare relazioni peso per peso. Fornisce un LIMITE INFERIORE per delta_N(K)(k), k qualsiasi
    # (forma iniziale per il peso: OPF5C-L8). Uso: python opf5c_delta.py N K dmax graded
    N = int(sys.argv[1]); K = int(sys.argv[2]); dmax = int(sys.argv[3])
    random.seed(777)
    global A_MOD
    fns, A_MOD = setup(N, [])
    restpolys = [topoly(f[2], 2*N+1) for f in fns]
    t0 = time.time()
    allmons = monomials(K+1, dmax)
    wt = lambda m: sum((j+2)*e for j, e in enumerate(m))
    byw = {}
    for m in allmons: byw.setdefault(wt(m), []).append(m)
    pts = None
    best = None
    for w in sorted(byw):
        mons = sorted(byw[w], key=lambda m: sum(m))
        npts = len(mons) + 10
        pts_w = [point(N, [], fns, restpolys)[:K+1] for _ in range(npts)]
        # grado minimo di una relazione di peso w: aggiungo i monomi per grado crescente
        for d in range(1, dmax+1):
            sub = [m for m in mons if sum(m) <= d]
            if not sub: continue
            M = np.zeros((npts, len(sub)), dtype=np.int64)
            for i, yv in enumerate(pts_w):
                for j, m in enumerate(sub):
                    t = 1
                    for v, e in enumerate(m):
                        if e: t = t*pow(yv[v], e, P) % P
                    M[i, j] = t
            nul = len(sub) - rank_mod(M)
            if nul > 0:
                if best is None or d < best[0]: best = (d, w)
                break
    print('N=%d K=%d k=0 (graduato), gradi <= %d: grado minimo di una relazione omogenea = %s  [%.1fs]'
          % (N, K, dmax, ('%d (peso %d)' % best) if best else 'nessuna', time.time()-t0))
    if best is None: print('  => delta_N(K)(k) >= %d per ogni k (limite inferiore)' % (dmax+1))
    else: print('  => delta_N(K)(k) >= %d per ogni k (limite inferiore)' % best[0])
if len(sys.argv) > 4 and sys.argv[4] == 'graded': main_graded()
else: main()
