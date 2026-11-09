# audit_s4id.py — S-CHECK-10, red team indipendente dei claim di S4-ID
# Esecuzione: D:\ProblemaBase\.venv\Scripts\python.exe -I audit_s4id.py > audit_s4id.out
# Scritto da zero dal revisore (non riusa gli script di S4-ID). Aritmetica esatta su QQ
# oppure modulo un primo p (solo per ranghi: dim ker mod p >= dim ker su QQ; l'uguaglianza
# con il valore atteso e' quindi un controllo, non una prova).
import sys, random, itertools
sys.stdout.reconfigure(encoding="utf-8")
import sympy as sp
import numpy as np

random.seed(20261026)
P = 1000003
RES = []
def check(name, ok, info=""):
    RES.append(bool(ok))
    print(("OK   " if ok else "FAIL ") + name + ("  | " + str(info) if info != "" else ""))
    sys.stdout.flush()

def inv(a): return pow(int(a) % P, P - 2, P)
def qmod(r):
    r = sp.Rational(r); return (int(r.p) % P) * inv(int(r.q)) % P

def rank_mod(M):
    """rank of integer numpy matrix mod P (Gaussian elimination)."""
    A = np.array(M, dtype=np.int64) % P
    r = 0; rows, cols = A.shape
    for c in range(cols):
        piv = None
        for i in range(r, rows):
            if A[i, c] != 0: piv = i; break
        if piv is None: continue
        A[[r, piv]] = A[[piv, r]]
        A[r] = (A[r] * inv(A[r, c])) % P
        nz = np.nonzero(A[:, c])[0]
        for i in nz:
            if i != r:
                A[i] = (A[i] - A[i, c] * A[r]) % P
        r += 1
        if r == rows: break
    return r

# ---------------------------------------------------------------- jet algebra A
M = 18
PART2 = "part2" in sys.argv  # seconda esecuzione: salta A, B, B2 (gia' in audit_s4id_part1.out) tranne n = 4, (2,4)
Y = sp.symbols('y0:%d' % M)
def Dx(p):
    p = sp.expand(p)
    return sp.expand(sum(sp.diff(p, Y[j]) * Y[j + 1] for j in range(M - 1) if p.has(Y[j])))
def Dpow(p, j):
    for _ in range(j): p = Dx(p)
    return p
def DN(p, N):
    p = sp.expand(p)
    return sp.expand(sum(sp.diff(p, Y[j]) * Dpow(N, j) for j in range(M) if p.has(Y[j])))

nu = sp.Rational(1, 3)
BENCH = {
    'Burgers': (2, nu * Y[2] - Y[0] * Y[1], nu),
    'Fisher': (2, Y[2] + Y[0] - Y[0] ** 2, 1),
    'KdV': (3, -Y[3] - 6 * Y[0] * Y[1], -1),
    'KdVB': (3, -Y[3] - Y[0] * Y[1] + nu * Y[2], -1),
}
psi_cache = {}
def psi_gen(name, N, a, b):
    key = (name, a, b)
    if key not in psi_cache:
        p = Y[b]
        for _ in range(a): p = DN(p, N)
        psi_cache[key] = sp.expand(p)
    return psi_cache[key]

def order_of(p):
    o = -1
    for j in range(M):
        if sp.expand(p).has(Y[j]): o = j
    return o

print("== A. ALG-L1 / L2: commutazione [D, D_N] = 0, triangolarita' di psi")
for name, (n, N, sig) in (BENCH.items() if not PART2 else []):
    ok = True
    for _ in range(3):
        q = sum(random.randint(-3, 3) * Y[random.randint(0, 3)] * Y[random.randint(0, 3)] for _ in range(4)) + Y[1]
        ok &= sp.expand(Dx(DN(q, N)) - DN(Dx(q), N)) == 0
    check("[D,D_N]=0 su polinomi casuali, %s" % name, ok)
    ok2 = True; info = []
    delta = max(sp.Poly(N, *Y).total_degree(), 1)
    for a in range(0, 3):
        for b in range(0, 3):
            if n * a + b >= M - 1: continue
            ps = psi_gen(name, N, a, b)
            lam = n * a + b
            lead_ok = sp.expand(sp.diff(ps, Y[lam]) - sp.Rational(sig) ** a) == 0
            rest = sp.expand(ps - sp.Rational(sig) ** a * Y[lam])
            ord_ok = order_of(rest) < lam
            deg_ok = sp.Poly(ps, *Y).total_degree() <= 1 + a * (delta - 1)
            ok2 &= lead_ok and ord_ok and deg_ok
    check("L2: psi(d_t^a d_x^b y) = sigma^a y_{na+b} + ordine minore, grado <= 1+a(delta-1), %s, a,b<=2" % name, ok2)

# ---------------------------------------------------------------- B. dim ker psi|V_{d,k}
def gens(k):
    return [(a, b) for a in range(k + 1) for b in range(k + 1 - a)]
def monos(gl, d):
    out = []
    for e in range(d + 1):
        out += list(itertools.combinations_with_replacement(range(len(gl)), e))
    return out

def kerdim_psi(name, N, d, k):
    gl = gens(k)
    imgs = [psi_gen(name, N, a, b) for (a, b) in gl]
    ms = monos(gl, d)
    cols = []
    allkeys = {}
    for m in ms:
        e = sp.Integer(1)
        for i in m: e = e * imgs[i]
        pol = sp.Poly(sp.expand(e), *Y) if m else sp.Poly(sp.Integer(1), *Y)
        col = {}
        for mon, cf in pol.terms():
            if mon not in allkeys: allkeys[mon] = len(allkeys)
            col[allkeys[mon]] = qmod(cf)
        cols.append(col)
    Mx = np.zeros((len(allkeys), len(cols)), dtype=np.int64)
    for j, col in enumerate(cols):
        for i, v in col.items(): Mx[i, j] = v
    return len(cols) - rank_mod(Mx), len(cols)

print("\n== B. S4ID-P1: dim([F] ∩ V_{d,k}) = dim ker psi|V (ALG-L1), contro i valori dichiarati")
expected = {('Burgers', 2, 2): 1, ('Burgers', 2, 3): 3, ('Burgers', 3, 2): 7, ('Burgers', 3, 3): 34,
            ('Fisher', 2, 2): 1, ('Fisher', 2, 3): 6, ('Fisher', 3, 2): 7,
            ('KdV', 2, 3): 1, ('KdV', 2, 4): 3, ('KdV', 3, 3): 11,
            ('KdVB', 2, 3): 1}
for (name, d, k), ex in (expected.items() if not PART2 else []):
    n, N, sig = BENCH[name]
    kd, nc = kerdim_psi(name, N, d, k)
    check("P1 %s (d,k)=(%d,%d): dim [F]∩V = %d (dichiarato %d), dim V = %d" % (name, d, k, kd, ex, nc), kd == ex)

print("\n== B2. P1 su N casuali di grado 2 (n = 1..4): =1 solo per (2,n), >=2 altrove (d<=3, k<=n+1)")
for n in ([1, 2, 3, 4] if not PART2 else [4]):
    for trial in range(2):
        sig = random.choice([1, -2, 3])
        Np = sum(random.randint(-2, 2) * Y[random.randint(0, n - 1)] for _ in range(2))
        Nq = 0
        while Nq == 0:
            Nq = sum(random.randint(-2, 2) * Y[random.randint(0, n - 1)] * Y[random.randint(0, n - 1)] for _ in range(2))
            Nq = sp.expand(Nq)
        N = sp.expand(sig * Y[n] + Np + Nq)
        name = 'rand_n%d_%d' % (n, trial)
        res = {}
        for d in [2, 3]:
            for k in [n, n + 1]:
                if (d == 3 and k == n + 1 and n >= 3) or (n == 4 and (d, k) != (2, 4)): continue  # troppo grande (MemoryError nella prima esecuzione)
                res[(d, k)] = kerdim_psi(name, N, d, k)[0]
        ok = res[(2, n)] == 1 and all(v >= 2 for key, v in res.items() if key != (2, n))
        check("P1 random n=%d N=%s: %s" % (n, N, res), ok)

print("\n== B3. Fuori ipotesi (deg N = 3, oppure y_n non lineare): P1(c) puo' cadere? (informativo)")
# mKdV: N = -y3 - 6 y0^2 y1 (deg 3): V_{2,3} non contiene F; V_{3,3}
Nm = -Y[3] - 6 * Y[0] ** 2 * Y[1]
print("INFO mKdV (deg N=3): il monomio y0^2 y1 di F ha grado 3, quindi F non sta in V_{2,3}: il dizionario minimo non e' (2,n). Calcolo di [F]∩V_{3,3} omesso (memoria).")
# inviscid Burgers N = -y0 y1, n = 1, sigma = 0 (fuori ipotesi sigma != 0)
Ni = -Y[0] * Y[1]
kd, nc = kerdim_psi('invB', Ni, 2, 1)
print("INFO Burgers inviscido (sigma=0) dim [F]∩V_{2,1} =", kd)

# ---------------------------------------------------------------- C. serie formali (indipendente da ALG-L1)
class Ser:
    def __init__(self, a): self.a = np.array(a, dtype=np.int64) % P
    @staticmethod
    def zeros(T, X): return Ser(np.zeros((T + 1, X + 1), dtype=np.int64))
    def __add__(s, o):
        if isinstance(o, Ser): return Ser(s.a + o.a)
        z = s.a.copy(); z[0, 0] += qmod(o); return Ser(z)
    __radd__ = __add__
    def __sub__(s, o): return s + (o * (-1) if isinstance(o, Ser) else -sp.Rational(o))
    def __mul__(s, o):
        if not isinstance(o, Ser): return Ser(s.a * qmod(o))
        T, X = s.a.shape
        z = np.zeros((T, X), dtype=np.int64)
        for i in range(T):
            if not s.a[i].any(): continue
            for j in range(T - i):
                if not o.a[j].any(): continue
                cv = np.convolve(s.a[i], o.a[j])[:X] % P
                z[i + j] = (z[i + j] + cv) % P
        return Ser(z)
    __rmul__ = __mul__
    def dx(s):
        T, X = s.a.shape
        z = np.zeros((T, X), dtype=np.int64)
        z[:, :-1] = (s.a[:, 1:] * np.arange(1, X)) % P
        return Ser(z)
    def dt(s):
        T, X = s.a.shape
        z = np.zeros((T, X), dtype=np.int64)
        z[:-1, :] = (s.a[1:, :] * np.arange(1, T)[:, None]) % P
        return Ser(z)

def Nfun(name):
    if name == 'Burgers': return lambda y: y[2] * nu - y[0] * y[1]
    if name == 'Fisher': return lambda y: y[2] + y[0] - y[0] * y[0]
    if name == 'KdV': return lambda y: y[3] * (-1) - y[0] * y[1] * 6
    if name == 'KdVB': return lambda y: y[3] * (-1) - y[0] * y[1] + y[2] * nu

def solve_series(name, n, g, T, X):
    u = Ser.zeros(T, X)
    u.a[0, :len(g)] = np.array(g[:X + 1], dtype=np.int64) % P
    f = Nfun(name)
    for i in range(T):
        ys = [u]
        for _ in range(n): ys.append(ys[-1].dx())
        Nu = f(ys)
        u.a[i + 1] = (Nu.a[i] * inv(i + 1)) % P
    return u

def I_cap_V_dim(u, n, d, k, Ti, Xj):
    gl = gens(k)
    gs = []
    for (a, b) in gl:
        s = u
        for _ in range(a): s = s.dt()
        for _ in range(b): s = s.dx()
        gs.append(s)
    ms = monos(gl, d)
    rows = []
    for m in ms:
        if not m:
            e = Ser.zeros(u.a.shape[0] - 1, u.a.shape[1] - 1); e.a[0, 0] = 1
        else:
            e = gs[m[0]]
            for i in m[1:]: e = e * gs[i]
        rows.append(e.a[:Ti + 1, :Xj + 1].flatten())
    Mx = np.array(rows, dtype=np.int64).T
    return len(ms) - rank_mod(Mx)

print("\n== C. S4ID-T1(b) indipendente: dato di Cauchy generico (serie formale), dim I(u)∩V = dim [F]∩V")
for (name, d, k) in [('Burgers', 2, 2), ('Burgers', 2, 3), ('Burgers', 3, 2), ('Fisher', 2, 2), ('Fisher', 2, 3), ('KdV', 2, 3), ('KdVB', 2, 3)]:
    n = BENCH[name][0]
    Ti = 10; Xj = 28; T = Ti + k + 1; X = Xj + k + n * T + 2
    g = [random.randrange(P) for _ in range(X + 1)]
    u = solve_series(name, n, g, T, X)
    dI = I_cap_V_dim(u, n, d, k, Ti, Xj)
    ex = expected[(name, d, k)]
    check("T1(b) %s V_{%d,%d}, u generica: dim I(u)∩V = %d = dim [F]∩V = %d (J_u∩psi(V)=0 atteso)" % (name, d, k, dI, ex), dI == ex)

print("\n== D. N-shock esatti (Taylor esatta in 0, c_i = 0): dim I(u)∩V_{2,2} = 1 + dim J_u∩psi(V_{2,2})")
def shock_data(ks, X):
    # u(0,x) = -2 nu sum k_i E_i / (1 + sum E_i), E_i = exp(k_i x), Taylor mod P
    fact = [1]
    for j in range(1, X + 2): fact.append(fact[-1] * j % P)
    E = [[qmod(sp.Rational(k) ** j) * inv(fact[j]) % P for j in range(X + 1)] for k in ks]
    phi = [1 + sum(E[i][j] for i in range(len(ks))) if j == 0 else sum(E[i][j] for i in range(len(ks))) for j in range(X + 1)]
    phi = [v % P for v in phi]
    num = [(-2 * qmod(nu) * sum(qmod(ks[i]) * E[i][j] for i in range(len(ks)))) % P for j in range(X + 1)]
    # series division num/phi
    q = [0] * (X + 1); i0 = inv(phi[0])
    for j in range(X + 1):
        s = num[j] - sum(q[l] * phi[j - l] for l in range(j))
        q[j] = s % P * i0 % P
    return q
claimed = {1: 21, 2: 4, 3: 1}
for Nsh, ks in [(1, [2]), (2, [1, 3]), (3, [1, 2, -3])]:
    n = 2; d = 2; k = 2; Ti = 10; Xj = 28; T = Ti + k + 1; X = Xj + k + n * T + 2
    g = shock_data(ks, X)
    u = solve_series('Burgers', n, g, T, X)
    dI = I_cap_V_dim(u, n, d, k, Ti, Xj)
    check("T1(b)/T2 %d-shock k=%s: dim I(u)∩V_{2,2} = %d (S4-ID dichiara %d)" % (Nsh, ks, dI, claimed[Nsh]), dI == claimed[Nsh])

# ---------------------------------------------------------------- E. T2 simbolico: R_N, Bell, ideale
print("\n== E. S4ID-T2: R_N da Bell, R_N in J_u (in C(X)), linearita' in y_N, grado N+1, dimensioni di J_u ∩ A_{<=d,<=N}")
w = sp.symbols('w0:12')
def bell(m):
    Yb = [sp.Integer(1)]
    for _ in range(m):
        prev = Yb[-1]
        dprev = sum(sp.diff(prev, w[j]) * w[j + 1] for j in range(11))
        Yb.append(sp.expand(dprev + w[0] * prev))
    return Yb
YB = bell(5)
z = sp.Symbol('z')
def R_N(ks, nuv):
    poly = sp.Poly(sp.expand(z * sp.prod([z - kk for kk in ks])), z)
    e = {m: poly.coeff_monomial(z ** m) for m in range(1, len(ks) + 2)}
    sub = {w[j]: -Y[j] / (2 * nuv) for j in range(11)}
    return sp.expand(sum(e[m] * YB[m].subs(sub, simultaneous=True) for m in range(1, len(ks) + 2)))
Xs = sp.symbols('X1:5')
def wjet_shock(ks, K):
    phi = 1 + sum(Xs[i] for i in range(len(ks)))
    Dphi = lambda f: sum(sp.diff(f, Xs[i]) * ks[i] * Xs[i] for i in range(len(ks)))
    wv = sp.together(Dphi(phi) / phi)
    jet = [wv]
    for _ in range(K): jet.append(sp.together(Dphi(jet[-1])))
    return jet
for ks in [[2], [1, 3], [2, -1, 5]]:
    Nn = len(ks)
    R = R_N([sp.Rational(k) for k in ks], nu)
    jet = wjet_shock([sp.Rational(k) for k in ks], Nn)
    ujet = [sp.together(-2 * nu * jj) for jj in jet]
    val = sp.simplify(R.subs({Y[j]: ujet[j] for j in range(Nn + 1)}, simultaneous=True))
    lin = sp.expand(sp.diff(R, Y[Nn], 2)) == 0 and sp.expand(sp.diff(R, Y[Nn]) + 1 / (2 * nu)) == 0
    pol = sp.Poly(R, *Y[:Nn + 1])
    top = sum(c * sp.prod([Y[i] ** e for i, e in enumerate(mon)]) for mon, c in pol.terms() if sum(mon) == Nn + 1)
    topok = sp.expand(top - (-2 * nu) ** (-(Nn + 1)) * Y[0] ** (Nn + 1)) == 0
    check("T2(b) N=%d k=%s: R_N(u)=0, R_N = -y_N/2nu + beta, deg = N+1, top = (-2nu)^{-N-1} y0^{N+1}" % (Nn, ks), val == 0 and lin and pol.total_degree() == Nn + 1 and topok, "R_N(u)=%s" % val)

def jet_numeric(jetfun_list, npts, nvars):
    pts = []
    for _ in range(npts):
        pts.append([random.randint(1, 10 ** 6) for _ in range(nvars)])
    return pts
def J_cap_dim(ujet, nvars, d, K, npts):
    # dim J_u ∩ A_{<=d,<=K} via valutazione in punti casuali X (esatta mod P)
    vars_ = list(range(K + 1))
    ms = []
    for e in range(d + 1): ms += list(itertools.combinations_with_replacement(vars_, e))
    def modpoly(e):
        pol = sp.Poly(sp.expand(e), *Xs[:nvars])
        return [(mon, qmod(c)) for mon, c in pol.terms()]
    def evp(tl, pt):
        s = 0
        for mon, c in tl:
            t_ = c
            for i, ee in enumerate(mon): t_ = t_ * pow(pt[i], ee, P) % P
            s += t_
        return s % P
    nums_dens = []
    for jj in ujet[:K + 1]:
        nu_, de_ = sp.fraction(sp.together(jj))
        nums_dens.append((modpoly(nu_), modpoly(de_)))
    rows = []
    for _ in range(npts):
        pt = [random.randint(1, P - 1) for i in range(nvars)]
        vals = []
        for (nu_, de_) in nums_dens:
            dv = evp(de_, pt)
            vals.append(evp(nu_, pt) * inv(dv) % P)
        row = []
        for m in ms:
            v = 1
            for i in m: v = v * vals[i] % P
            row.append(v)
        rows.append(row)
    return len(ms) - rank_mod(np.array(rows, dtype=np.int64))
for ks in [[2], [1, 3], [2, -1, 5]]:
    Nn = len(ks)
    jet = wjet_shock([sp.Rational(k) for k in ks], Nn + 1)
    ujet = [sp.together(-2 * nu * jj) for jj in jet]
    d0 = J_cap_dim(ujet, Nn, Nn, Nn, 260)
    d1 = J_cap_dim(ujet, Nn, Nn + 1, Nn, 260)
    exp1 = sp.binomial(Nn + 1, Nn + 1)
    dlow = J_cap_dim(ujet, Nn, 6 if Nn < 3 else 4, Nn - 1, 260) if Nn >= 1 else 0
    check("T2(a)(b) N=%d: J∩A_{<=%d,<=%d}=%d (0), J∩A_{<=%d,<=%d}=%d (binom=1), J∩A_{<=%s,<=N-1}=%d (0)" % (Nn, Nn, Nn, d0, Nn + 1, Nn, d1, 6 if Nn < 3 else 4, dlow), d0 == 0 and d1 == 1 and dlow == 0)
# binom(d, N+1) per d = N+2
for ks in [[2], [1, 3]]:
    Nn = len(ks)
    jet = wjet_shock([sp.Rational(k) for k in ks], Nn + 1)
    ujet = [sp.together(-2 * nu * jj) for jj in jet]
    d2 = J_cap_dim(ujet, Nn, Nn + 2, Nn, 300)
    check("T2(b) N=%d: dim J∩A_{<=N+2,<=N} = %d = binom(N+2,N+1) = %d" % (Nn, d2, sp.binomial(Nn + 2, Nn + 1)), d2 == sp.binomial(Nn + 2, Nn + 1))
# (c) a ordine K = N+1: dim J ∩ A_{<=N+1,<=N+1} = dim (R_N, D R_N) in grado <= N+1
for ks in [[2], [1, 3]]:
    Nn = len(ks)
    jet = wjet_shock([sp.Rational(k) for k in ks], Nn + 2)
    ujet = [sp.together(-2 * nu * jj) for jj in jet]
    dd = J_cap_dim(ujet, Nn, Nn + 1, Nn + 1, 300)
    # in (R_N, D R_N) i multipli di grado <= N+1: solo costanti * R_N e costanti * D R_N (deg D R_N = N+1)
    check("T2(c) N=%d: dim J∩A_{<=N+1,<=N+1} = %d (atteso 2: R_N, D R_N)" % (Nn, dd), dd == 2)

print("\n== F. T2(e) grado 1: D^j(1/(1+X)) ha polo d'ordine esattamente j+1 in X = -1")
Xv, kk = sp.symbols('X k', nonzero=True)
okF = True
for j in range(1, 7):
    f = 1 / (1 + Xv)
    for _ in range(j): f = sp.together(kk * Xv * sp.diff(f, Xv))
    num, den = sp.fraction(sp.factor(f))
    ordp = sp.Poly(den, Xv).as_expr()
    mult = sp.roots(sp.Poly(den, Xv)).get(-1, 0)
    okF &= (mult == j + 1) and sp.simplify(num.subs(Xv, -1)) != 0
check("T2(e): polo d'ordine j+1 (j=1..6), numeratore non nullo in -1", okF)

# ---------------------------------------------------------------- G. T3
print("\n== G. S4ID-T3: Pi_1 per il 1-solitone; 2-solitone: nessuna relazione d'ordine 1 (L5), grado di Pi_2")
xx, tt, k1 = sp.symbols('x t k', positive=True)
E = sp.exp(k1 * xx - k1 ** 3 * tt)
u1 = 2 * sp.diff(sp.log(1 + E), xx, 2)
chk = sp.simplify(sp.diff(u1, tt) + 6 * u1 * sp.diff(u1, xx) + sp.diff(u1, xx, 3))
Pi1 = sp.diff(u1, xx) ** 2 - k1 ** 2 * u1 ** 2 + 2 * u1 ** 3
check("T3(b) 1-solitone risolve KdV e Pi_1 = y1^2 - k^2 y0^2 + 2 y0^3 ∈ J_u", chk == 0 and sp.simplify(Pi1) == 0)
# 2-solitone k = (1,2) nel campo C(X1,X2), D X_i = k_i X_i
def kdv_jet(ks, K):
    A12 = ((ks[0] - ks[1]) / (ks[0] + ks[1])) ** 2
    f = 1 + Xs[0] + Xs[1] + A12 * Xs[0] * Xs[1]
    D = lambda g: sum(sp.diff(g, Xs[i]) * ks[i] * Xs[i] for i in range(2))
    uu = sp.together(2 * (f * D(D(f)) - D(f) ** 2) / f ** 2)
    jet = [uu]
    for _ in range(K): jet.append(sp.together(D(jet[-1])))
    return jet
kj = kdv_jet([sp.Integer(1), sp.Integer(2)], 3)
d_o1 = J_cap_dim(kj, 2, 10, 1, 200)
check("T3(a) 2-solitone k=(1,2): J∩A_{<=10,<=1} = %d (atteso 0, L5)" % d_o1, d_o1 == 0)
d7 = J_cap_dim(kj, 2, 7, 2, 400)
d8 = J_cap_dim(kj, 2, 8, 2, 400)
check("T3(c) V-ex 2-solitone k=(1,2): J∩A_{<=7,<=2} = %d (0), J∩A_{<=8,<=2} = %d (1) => deg Pi_2 = 8" % (d7, d8), d7 == 0 and d8 == 1)
kj2 = kdv_jet([sp.Integer(1), sp.Integer(3)], 2)
d7b = J_cap_dim(kj2, 2, 7, 2, 400); d8b = J_cap_dim(kj2, 2, 8, 2, 400)
print("INFO 2-solitone k=(1,3): J∩A_{<=7,<=2} =", d7b, " J∩A_{<=8,<=2} =", d8b, "(deg Pi_2 per un secondo k; non dichiarato da S4-ID)")

# ---------------------------------------------------------------- H. L4
print("\n== H. S4ID-L4: D_B^m(y0^2) = (-1)^m (2/(m+2)) D^m(y0^{m+2}); ker psi su R_{<=3} y ⊕ R_{<=3} y^2")
NB = BENCH['Burgers'][1]
DB = lambda p: sp.expand(sum(sp.diff(p, Y[j]) * Dpow(-Y[0] * Y[1], j) for j in range(M - 2) if sp.expand(p).has(Y[j])))
okH = True
for m in range(0, 5):
    lhs = Y[0] ** 2
    for _ in range(m): lhs = DB(lhs)
    rhs = (-1) ** m * sp.Rational(2, m + 2) * Dpow(Y[0] ** (m + 2), m)
    okH &= sp.expand(lhs - rhs) == 0
check("L4 identita' D_B^m(y0^2), m = 0..4", okH)
# kernel of psi on {Q1(d) y + Q2(d) y^2 : deg Q_i <= 3}; atteso: {A F_B : deg A <= 1} -> dim 3
tau_xi = [(a, b) for a in range(4) for b in range(4 - a)]
cols = []; keys = {}
def apply_op(a, b, base):
    p = base
    for _ in range(b): p = Dx(p)
    for _ in range(a): p = DN(p, NB)
    return sp.expand(p)
for base in [Y[0], Y[0] ** 2]:
    for (a, b) in tau_xi:
        pol = sp.Poly(apply_op(a, b, base), *Y)
        col = {}
        for mon, cf in pol.terms():
            if mon not in keys: keys[mon] = len(keys)
            col[keys[mon]] = qmod(cf)
        cols.append(col)
Mx = np.zeros((len(keys), len(cols)), dtype=np.int64)
for j, col in enumerate(cols):
    for i, v in col.items(): Mx[i, j] = v
kd = len(cols) - rank_mod(Mx)
check("L4: dim([F_B] ∩ (R_{<=3}y ⊕ R_{<=3}y^2)) = %d (atteso 3 = dim{A : deg A <= 1})" % kd, kd == 3)
# nu = 0 (Burgers inviscido, ammesso da L4 'nu qualsiasi')
cols = []; keys = {}
N0 = -Y[0] * Y[1]
for base in [Y[0], Y[0] ** 2]:
    for (a, b) in tau_xi:
        p = base
        for _ in range(b): p = Dx(p)
        for _ in range(a): p = DN(p, N0)
        pol = sp.Poly(sp.expand(p), *Y)
        col = {}
        for mon, cf in pol.terms():
            if mon not in keys: keys[mon] = len(keys)
            col[keys[mon]] = qmod(cf)
        cols.append(col)
Mx = np.zeros((len(keys), len(cols)), dtype=np.int64)
for j, col in enumerate(cols):
    for i, v in col.items(): Mx[i, j] = v
kd0 = len(cols) - rank_mod(Mx)
# con nu = 0: A tau y + A xi/2 y^2, deg(A tau) <= 3 => deg A <= 2 -> dim 6
check("L4 con nu = 0: dim = %d (atteso 6 = dim{A : deg A <= 2})" % kd0, kd0 == 6)

# ---------------------------------------------------------------- I. T4
print("\n== I. S4ID-T4(ii): disuguaglianza di conteggio con D* = (n+1)c^n - n; T4(iv) riduzione autosimile")
okI = True
for n_ in range(0, 6):
    for c in range(1, 9):
        Ds = (n_ + 1) * c ** n_ - n_
        okI &= sp.binomial(Ds + n_ + 1, n_ + 1) > sp.binomial(c * Ds + n_, n_)
check("T4(ii) binom(D*+n+1,n+1) > binom(cD*+n,n) per n<=5, c<=8", okI)
# controllo diretto del conteggio sul 1-shock: n=1 (solo E), a=b=1, c=2, D*=3: esiste relazione in A_{<=3,<=1}
jet1 = wjet_shock([sp.Integer(2)], 1); uj1 = [sp.together(-2 * nu * jj) for jj in jet1]
dd = J_cap_dim(uj1, 1, 3, 1, 100)
check("T4(ii) 1-shock: J∩A_{<=D*=3,<=1} = %d > 0" % dd, dd > 0)
Wf = sp.Function('W'); zz = sp.Symbol('z')
tt2, xx2 = sp.symbols('t x', positive=True)
zexpr = xx2 * (3 * tt2) ** sp.Rational(-1, 3)
uas = (3 * tt2) ** sp.Rational(-2, 3) * Wf(zexpr)
expr = sp.diff(uas, tt2) + 6 * uas * sp.diff(uas, xx2) + sp.diff(uas, xx2, 3)
ode = Wf(zz).diff(zz, 3) + 6 * Wf(zz) * Wf(zz).diff(zz) - 2 * Wf(zz) - zz * Wf(zz).diff(zz)
ratio = sp.simplify((expr / ((3 * tt2) ** sp.Rational(-5, 3))).subs(xx2, zz * (3 * tt2) ** sp.Rational(1, 3)).doit() - ode)
check("T4(iv): u = (3t)^{-2/3} W(x(3t)^{-1/3}) risolve KdV ⟺ W''' + 6WW' - 2W - zW' = 0", sp.simplify(ratio) == 0, ratio)

# ---------------------------------------------------------------- J. P7, P8
print("\n== J. S4ID-P7 (1-shock: u_xx = H(u) u_x) e S4ID-P8 (I_PW)")
kk2, nn2 = sp.symbols('k nu', positive=True)
Es = sp.exp(kk2 * xx + nn2 * kk2 ** 2 * tt)
ush = -2 * nn2 * kk2 * Es / (1 + Es)
burg = sp.simplify(sp.diff(ush, tt) + ush * sp.diff(ush, xx) - nn2 * sp.diff(ush, xx, 2))
Hs = sp.simplify(sp.diff(ush, xx, 2) / sp.diff(ush, xx))
Hu = sp.simplify(Hs - (kk2 + ush / nn2))
Hu2 = sp.simplify(Hs - (-kk2 - ush / nn2))
print("INFO 1-shock u = -2 nu k E/(1+E): u_xx/u_x - (k + u/nu) =", Hu, "; u_xx/u_x - (-k - u/nu) =", Hu2)
check("P7(iii) 1-shock: u_xx/u_x e' funzione polinomiale (affine) di u (H globale) e u risolve Burgers", burg == 0 and (Hu == 0 or Hu2 == 0))
A_, ka, th, xv = sp.symbols('A kappa theta x', real=True)
pw = A_ * sp.cos(ka * xv + th)
yj = [sp.diff(pw, xv, j) for j in range(6)]
check("P8: y0y3 - y1y2 e y0y4 - y2^2 ∈ I_PW", sp.simplify(yj[0] * yj[3] - yj[1] * yj[2]) == 0 and sp.simplify(yj[0] * yj[4] - yj[2] ** 2) == 0)
cs = sp.symbols('c0:4')
lin = sum(cs[j] * yj[j] for j in range(4)).subs(A_, 1)
eqs = [sp.expand(lin.subs({xv: 0, th: thv, ka: kv})) for thv in [0, sp.pi / 2] for kv in [1, 2, 3, 5]]
sol = sp.solve(eqs, cs, dict=True)
check("P8: forma lineare complessa nulla su tutte le onde piane => c = 0 (anche c_j complessi)", sol == [{c: 0 for c in cs}] or all(v == 0 for v in sol[0].values()), sol)
# Pi_1: parte minima y1^2 - k^2 y0^2 non in I_PW
v = (yj[1] ** 2 - 4 * yj[0] ** 2).subs({A_: 1, ka: 1, th: 0, xv: 0})
check("P8: y1^2 - k^2 y0^2 (k=2) ∉ I_PW", v != 0, v)

print("\n== Totale: %d/%d OK" % (sum(RES), len(RES)))
