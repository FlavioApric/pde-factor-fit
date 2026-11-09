# S-CHECK-12 — red team SymPy per l'audit di OP-ALG (controllo, non prova)
# Esecuzione: D:\ProblemaBase\.venv\Scripts\python.exe -I audit_opalg.py
import itertools, random, sys
sys.stdout.reconfigure(encoding="utf-8")
import sympy as sp

t, x, n, lam, mu, w, c = sp.symbols('t x n lambda mu w c')
tau, xi = sp.symbols('tau xi')
RES = []
def chk(name, cond):
    RES.append((name, bool(cond)))
    print(('OK  ' if cond else 'FAIL') + ' ' + name)

def ff(nv, j):  # fattoriale decrescente
    return sp.prod([nv - i for i in range(j)]) if j > 0 else sp.Integer(1)

def apply_t(L, f):
    """L = dict {(i,j): beta(x)} per sum beta_ij(x) t^i d_t^j"""
    return sp.expand(sum(b * t**i * sp.diff(f, t, j) for (i, j), b in L.items()))

# ---------------- L2: indiciale a parametro (t0 = 0) ----------------
def indicial(L, t0=0):
    # L dict {(j): b_j(t,x)}, espansione in (t - t0)
    s = sp.Symbol('s')
    terms = {}
    for j, b in L.items():
        pb = sp.Poly(sp.expand(sp.sympify(b).subs(t, s + t0)), s)
        for (i,), coef in pb.terms():
            terms[(i, j)] = terms.get((i, j), 0) + coef
    terms = {k: v for k, v in terms.items() if sp.simplify(v) != 0}
    delta = min(i - j for (i, j) in terms)
    iota = sp.expand(sum(v * ff(n, j) for (i, j), v in terms.items() if i - j == delta))
    return delta, iota

def K0_of(iota):
    P = sp.Poly(iota, x)
    g = 0
    for co in P.coeffs():
        g = sp.gcd(g, co)
    roots = [r for r in sp.roots(sp.Poly(g, n)).keys() if r.is_integer and r >= 0] if sp.Poly(g, n).degree() > 0 else []
    return max(roots) if roots else -1

# esempi del package + nuovi (punti singolari, indiciale dipendente da x)
ex = [({1: t, 0: -3}, t**3 * x, 3),
      ({1: (x + 1) * t, 0: -2 * (x + 1)}, t**2 * sp.exp(x), 2),
      ({1: t, 0: -x}, None, -1),                       # n - x: nessuna radice intera identica
      ({1: x * t**2, 0: -2 * x * t}, t**2 * (1 + x), 2),   # delta=1, iota = x(n-2)
      ({2: t**2, 1: -2 * t, 0: 2 - x**0 * 0}, None, None)]
d, io = indicial(ex[0][0]); chk('L2 t*d_t-3: K0=3', K0_of(io) == 3)
d, io = indicial(ex[1][0]); chk('L2 (x+1)(t d_t-2): K0=2', K0_of(io) == 2)
d, io = indicial(ex[2][0]); chk('L2 t d_t - x: Z vuoto (K0=-1)', K0_of(io) == -1)
d, io = indicial(ex[3][0]); chk('L2 x t^2 d_t - 2xt: delta=1, K0=2', d == 1 and K0_of(io) == 2)
for L, v, _ in ex[:2] + ex[3:4]:
    chk('L2 soluzione esatta annullata', sp.simplify(sum(b * sp.diff(v, t, j) for j, b in L.items())) == 0)

# Struttura della ricorrenza (prova di L2): coefficiente di t^(n0+delta) = iota(n0;x) c_{n0} + termini con c_m, m<n0
cs = [sp.Function('c%d' % k)(x) for k in range(7)]
for trial in range(6):
    random.seed(trial)
    L = {}
    for j in range(3):
        L[j] = sum(random.randint(-2, 2) * t**i * x**k for i in range(3) for k in range(2))
    if all(v == 0 for v in L.values()):
        continue
    delta, iota = indicial(L)
    v = sum(cs[k] * t**k for k in range(7))
    Lv = sp.expand(sum(b * sp.diff(v, t, j) for j, b in L.items()))
    ok = True
    for n0 in range(0, 4):
        e = n0 + delta
        if e < 0:
            continue
        co = sp.expand(Lv.coeff(t, e))
        # parte in c_{n0}
        part = sp.expand(co.coeff(cs[n0]))
        rest = sp.expand(co - part * cs[n0])
        higher = any(rest.has(cs[m]) for m in range(n0 + 1, 7))
        ok = ok and sp.simplify(part - iota.subs(n, n0)) == 0 and not higher
    chk('L2 ricorrenza su L casuale #%d (delta=%d)' % (trial, delta), ok)

# ---------------- L4/P2: confinamento EP, eliminanti "sporche" ----------------
def L4_data(L):
    """L dict {(i,j): beta(x)} ; restituisce T_t e N_t."""
    D = max(i for (i, j), b in L.items() if b != 0)
    MD = sp.expand(sum(b * tau**j for (i, j), b in L.items() if i == D))
    P = sp.Poly(MD, x)
    g = 0
    for co in P.coeffs():
        g = sp.gcd(g, co)
    T = list(sp.roots(sp.Poly(g, tau)).keys()) if sp.Poly(g, tau).degree() > 0 else []
    N = {}
    for tv in T:
        # L_tau = sum beta t^i (d_t + tv)^j = sum gamma_il t^i d_t^l
        gam = {}
        for (i, j), b in L.items():
            for l in range(j + 1):
                gam[(i, l)] = sp.expand(gam.get((i, l), 0) + b * sp.binomial(j, l) * tv**(j - l))
        gam = {k: v for k, v in gam.items() if v != 0}
        dt = max(i - l for (i, l) in gam)
        it = sp.expand(sum(v * ff(n, l) for (i, l), v in gam.items() if i - l == dt))
        N[tv] = K0_of(it)
    return T, N

def astar_apply(T, N, f, var):
    for tv in T:
        if N[tv] >= 0:
            for _ in range(N[tv] + 1):
                f = sp.diff(f, var) - tv * f
    return sp.simplify(f)

# w EP con esponenti e gradi; eliminante minimale moltiplicata a sinistra per operatori casuali
w1 = (t**2 + x) * sp.exp(2 * t + x) + 3 * t * sp.exp(-t)
# eliminante minimale in d_t: (d_t-2)^3 (d_t+1)^2 annulla la parte in t; costruiamo L = A * Lmin
def op_from_poly_dt(p):  # polinomio in tau -> dict
    P = sp.Poly(sp.expand(p), tau)
    return {(0, j): co for (j,), co in P.terms()}
Lmin = op_from_poly_dt((tau - 2)**3 * (tau + 1)**2)
def compose(A, B):
    # (A*B) per operatori in K[t,x]<d_t> come dict {(i,j):beta(x)}; uso azione su funzione generica
    f = sp.Function('f')(t, x)
    expr = sp.expand(apply_t(A, apply_t(B, f)))
    out = {}
    for j in range(12):
        co = sp.expand(expr.coeff(sp.Derivative(f, (t, j))) if j > 0 else expr.subs({sp.Derivative(f, (t, k)): 0 for k in range(1, 12)}).coeff(f))
        if co != 0:
            Pc = sp.Poly(co, t)
            for (i,), b in Pc.terms():
                out[(i, j)] = sp.expand(out.get((i, j), 0) + b)
    return out
okall = True
for seed in range(4):
    random.seed(10 + seed)
    A = {(random.randint(0, 2), random.randint(0, 1)): (random.randint(1, 3) * x + random.randint(-2, 2)) for _ in range(2)}
    L = compose(A, Lmin)
    chk('L4 eliminante sporca #%d annulla w1' % seed, sp.simplify(apply_t(L, w1)) == 0)
    T, N = L4_data(L)
    contains = (2 in T and N[2] >= 2) and (-1 in T and N[-1] >= 1)
    chk('L4 esponenti/gradi di w1 contenuti in (T_t,N_t) #%d' % seed, contains)
    chk('P2 a*(d_t) w1 = 0 #%d' % seed, astar_apply(T, N, w1, t) == 0)

# w non EP: e^{t^2}(2t-1) (P4-C4(b)), nucleo del calore, e^{t x}
G = t**sp.Rational(-1, 2) * sp.exp(-x**2 / (4 * t))
wC4 = (2 * t - 1) * sp.exp(t**2)
LC4 = {(1, 1): 2, (0, 1): -1, (2, 0): -4, (1, 0): 2, (0, 0): -2}
chk('P4-C4(b): L_w annulla w', sp.simplify(apply_t(LC4, wC4)) == 0)
T, N = L4_data(LC4)
chk('P4-C4(b): M_D costante => T_t vuoto', T == [])
chk('P4-C4(b): a* = 1 e w != 0 => non EP', astar_apply(T, N, wC4, t) != 0)
LG = {(2, 1): 4, (1, 0): 2, (0, 0): -x**2}     # 4t^2 d_t + 2t - x^2
chk('calore: 4t^2 d_t + 2t - x^2 annulla G', sp.simplify(apply_t(LG, G)) == 0)
T, N = L4_data(LG)
chk('calore: T_t = {0}, N_t(0) = -1 => a* = 1', T == [0] and N[0] == -1)
wtx = sp.exp(t * x)
Ltx = {(0, 1): 1, (0, 0): -x}
T, N = L4_data(Ltx)
chk('e^{tx}: T_t = vuoto (M_D = tau - x non identicamente nullo per nessun tau)', T == [])

# ---------------- Rilievo A1: campo di definizione (controesempio K vs 𝕂) ----------------
pi_ = sp.Symbol('p', positive=True)  # trascendente simbolico
u = sp.exp(x) * (t + pi_ * x)
I_ops = [sp.diff(u, t, 2), sp.diff(sp.diff(u, x) - u, t), sp.diff(u, x, 2) - 2 * sp.diff(u, x) + u]
chk('A1: I = (d_t^2, d_t(d_x-1), (d_x-1)^2) annulla u = e^x(t+p x)', all(sp.simplify(e) == 0 for e in I_ops))
chk('A1: (p d_t - d_x + 1) u = 0', sp.simplify(pi_ * sp.diff(u, t) - sp.diff(u, x) + u) == 0)
# Ann(u) cap span{tau, xi-1, (xi-1)^2, tau^2, tau(xi-1)} via getti in 0
a = sp.symbols('a0:5')
Q = a[0] * tau + a[1] * (xi - 1) + a[2] * (xi - 1)**2 + a[3] * tau**2 + a[4] * tau * (xi - 1)
def Qapply(Qp, f):
    P = sp.Poly(sp.expand(Qp), tau, xi)
    return sp.expand(sum(co * sp.diff(f, t, i, x, j) if (i or j) else co * f for (i, j), co in P.terms()))
v = Qapply(Q, u)
eqs = [sp.expand(sp.diff(v, t, i, x, j).subs({t: 0, x: 0}) if (i or j) else v.subs({t: 0, x: 0})) for i in range(3) for j in range(3)]
M = sp.Matrix([[sp.diff(e, ai) for ai in a] for e in eqs])
ker = M.nullspace()
chk('A1: dim Ann(u) cap 𝓛 = 4 (gradi <= 2, 5 generatori)', len(ker) == 4)
# vettore (p, -1, 0,0,0) nel nucleo: non razionale su K
vec = sp.Matrix([pi_, -1, 0, 0, 0])
chk('A1: p*tau - (xi-1) in Ann(u)', all(sp.simplify(e) == 0 for e in (M * vec)))
# Ann ∩ 𝓛 non ha base in K: il sottospazio non e' stabile per p -> p+1 (definito su K implicherebbe indipendenza da p)
Mshift = M.subs(pi_, pi_ + 1)
chk('A1: il sottospazio dipende da p (non definito su ℚ̄)', not all(sp.simplify(e) == 0 for e in (Mshift * vec)))
# Fix: eliminante simultanea su K per u e d_t u  (Q_k in A_2(K)): L = d_t^2 annulla entrambe => annulla p*d_t u - d_x u + u
chk('A1 fix: d_t^2 annulla tutte le Q_k u (Q_k in {1, d_t, d_x})', all(sp.simplify(sp.diff(sp.diff(u, t, i, x, j), t, 2)) == 0 for i, j in [(0, 0), (1, 0), (0, 1)]))

# ---------------- T3(f): avversario su P = (tau-xi)(tau+xi) (fattori distinti), p0 = 0 ----------------
s = x - t
ut = sp.exp(s**2)                         # Ann = (tau+xi): u~ = g(x-t), g non EP
e = sp.exp(t + x)                         # z0 = (1,1) in V(tau - xi), P2(z0) = 2 != 0
uu = ut + e
def Papply(Pp, f):
    return Qapply(Pp, f)
chk('T3f: P(d) u = 0', sp.simplify(Papply((tau - xi) * (tau + xi), uu)) == 0)
chk('T3f: (P/P1) u = 2 e^{t+x} (chi = 0)', sp.simplify(Papply(tau + xi, uu) - 2 * e) == 0)
k0 = 2
def jet(f):
    return [sp.simplify(sp.diff(f, t, i, x, j).subs({t: 0, x: 0}) if (i or j) else f.subs({t: 0, x: 0})) for i in range(k0 + 1) for j in range(k0 + 1 - i)]
# v1: combinazione di e^{a(x-t)} con lo stesso 2-getto di u~ (getti in s: 1,0,2)
v1 = sp.exp(s) + sp.exp(-s) - 1
chk('T3f: J_2(v1) = J_2(u~)', jet(v1) == jet(ut))
Qlist = [xi, tau - 1, tau + xi, (tau + xi) * tau, tau**2 - xi**2 + 1, xi - 3]
Qp = [q for q in Qlist if sp.rem(sp.Poly(q, tau, xi), sp.Poly(tau + xi, tau, xi)) != 0 and sp.simplify(sp.Poly(q, tau, xi).as_expr()) != 0]
Qp = [q for q in Qlist if sp.simplify(sp.expand(q).subs(tau, -xi)) != 0]
# e_Q: combinazioni di e^{a s} (a in A) con 2-getto nullo e Q(d) e_Q != 0
A_ = [4, 5, 6, 7]
cc = sp.symbols('cc0:4')
eQ_gen = sum(ci * sp.exp(ai * s) for ci, ai in zip(cc, A_))
Mj = sp.Matrix([[sp.diff(jj, ci) for ci in cc] for jj in jet(eQ_gen)])
nsp = Mj.nullspace()
chk('T3f: nucleo dei getti per e_Q non nullo', len(nsp) >= 1)
eQ = sum(nsp[0][i] * sp.exp(A_[i] * s) for i in range(4))
chk('T3f: J_2(e_Q) = 0', all(sp.simplify(j) == 0 for j in jet(eQ)))
# F: punti di V(tau+xi) nuovi, |F| > B + N0 con B "restituito" = 5, N0 = 6
B = 5; N0 = 6
Fpts = list(range(10, 10 + B + N0 + 1))
cF = sp.symbols('cf0:%d' % len(Fpts))
gF = sum(ci * sp.exp(ai * s) for ci, ai in zip(cF, Fpts))
MF = sp.Matrix([[sp.diff(jj, ci) for ci in cF] for jj in jet(gF)])
SF = MF.nullspace()
chk('T3f: dim S_F >= |F| - N0', len(SF) >= len(Fpts) - N0)
random.seed(7)
cvec = sum((random.randint(1, 9) * vv for vv in SF), sp.zeros(len(Fpts), 1))
lamQ = 3
up = v1 + lamQ * eQ + sum(cvec[i] * sp.exp(Fpts[i] * s) for i in range(len(Fpts))) + e
chk('T3f: J_2(u\') = J_2(u)', all(sp.simplify(p_ - q_) == 0 for p_, q_ in zip(jet(up), jet(uu))))
same = True
for q in Qlist:
    zu = sp.simplify(Qapply(q, uu)) == 0
    zp = sp.simplify(Qapply(q, up)) == 0
    same = same and (zu == zp)
chk('T3f: stesse risposte di zero sui 6 operatori campione', same)
nz = sum(1 for i in range(len(Fpts)) if cvec[i] != 0)
chk('T3f: modi nuovi con c_z != 0 > B (dim R.u\' >= #esponenti > B)', nz > B)
chk('T3f: P(d) u\' = 0', sp.simplify(Papply((tau - xi) * (tau + xi), up)) == 0)

# ---------------- C1: identita' in A_2 su funzione generica ----------------
f = sp.Function('f')(t, x)
dt = lambda g: sp.diff(g, t); dx = lambda g: sp.diff(g, x)
th = lambda g: x * dx(g)
P1 = lambda g: dt(g) - th(g)
P2 = lambda g: dt(g) - th(g) + g
Ql = lambda g, l: P2(g) + l * dx(P1(g))
chk('C1 P1P2 = P2P1', sp.simplify(P1(P2(f)) - P2(P1(f))) == 0)
chk('C1 P1 d_x = d_x P2', sp.simplify(P1(dx(f)) - dx(P2(f))) == 0)
chk('C1 (1+lam d_x)P = P1 Q_lam', sp.simplify(P1(P2(f)) + lam * dx(P1(P2(f))) - P1(Ql(f, lam))) == 0)
u2 = sp.exp(-t) * sp.exp(x**2 * sp.exp(2 * t))
ul = u2 + lam * dx(u2)
chk('C1 P2 u2 = 0', sp.simplify(P2(u2)) == 0)
chk('C1 P u^(lam) = 0', sp.simplify(P1(P2(ul))) == 0)
chk('C1 P1 u^(lam) = -u2', sp.simplify(P1(ul) + u2) == 0)
chk('C1 P2 u^(lam) = lam d_x u2', sp.simplify(P2(ul) - lam * dx(u2)) == 0)
chk('C1 Q_lam u^(lam) = 0', sp.simplify(Ql(ul, lam)) == 0)
umu = u2 + mu * dx(u2)
chk('C1 Q_lam u^(mu) = (mu-lam) d_x u2', sp.simplify(Ql(umu, lam) - (mu - lam) * dx(u2)) == 0)
us = sp.exp(x * sp.exp(t)) + sp.exp(-t) * sp.exp(-x * sp.exp(t))
chk('C1 u*: P u* = 0', sp.simplify(P1(P2(us))) == 0)
# Lemma NT (V-ex): nessun b = sum_{j<=2} beta_j(t,x) d_x^j, beta_j di grado <= 2 in (t,x), annulla u2
bc = sp.symbols('b0:18')
mons = [t**i * x**k for i in range(3) for k in range(3 - i)]
beta = [sum(bc[6 * j + m] * mons[m] for m in range(6)) for j in range(3)]
expr = sp.expand(sp.simplify(sum(beta[j] * sp.diff(u2, x, j) for j in range(3)) / sp.exp(x**2 * sp.exp(2 * t)) * sp.exp(t)))
expr = sp.expand(expr.subs(sp.exp(t), w).subs(sp.exp(2 * t), w**2).subs(sp.exp(3 * t), w**3).subs(sp.exp(4 * t), w**4))
expr = sp.expand(expr.rewrite(sp.exp).subs(sp.exp(t), w))
Pp = sp.Poly(expr, t, x, w)
sol = sp.solve(Pp.coeffs(), bc, dict=True)
chk('Lemma NT (V-ex): nessun b di ordine <=2, grado <=2 annulla u2', len(sol) == 1 and all(v == 0 for v in sol[0].values()) and len(sol[0]) == len(bc))
# Relazione b0 u* + b1 d_t u* = 0 con b_j in A_1 di ordine <= 1, grado <= 1: solo banale (V-ex di T4(b))
bb = sp.symbols('bb0:8')
def A1op(cf, g):
    return cf[0] * g + cf[1] * x * g + cf[2] * dx(g) + cf[3] * x * dx(g)
rel = A1op(bb[:4], us) + A1op(bb[4:], dt(us))
rel = sp.expand(sp.simplify(rel))
# valutazione su punti per ottenere sistema lineare
pts = [(sp.Rational(i, 3), sp.Rational(j, 5)) for i in range(-2, 3) for j in range(-2, 3)]
Ms = sp.Matrix([[sp.N(sp.diff(rel, b).subs({t: p[0], x: p[1]}), 30) for b in bb] for p in pts])
chk('C1(v) (V-ex): nessuna relazione a coefficienti A_1 di grado basso per u*', Ms.rank(iszerofunc=lambda z: abs(z) < 1e-20) == 8)
# relazione per u^(lam): b1 = 1 + lam d_x, b0 = 1 - theta - lam d_x theta
chk('C1(ii) relazione esplicita Q_lam (t-getto non libero)', sp.simplify((ul + lam * dx(ul)) * 0 + dt(ul) + lam * dx(dt(ul)) + ul - th(ul) - lam * dx(th(ul))) == 0)

# ---------------- P5: nucleo del calore in A_2 non identifica ----------------
chk('P5: (2t d_x + x) G = 0 => G di torsione su 𝒜', sp.simplify(2 * t * dx(G) + x * G) == 0)

# ---------------- INT-18 ----------------
Gt = t * G
chk('INT-18 (tau-xi^2)(tG) = G', sp.simplify(dt(Gt) - sp.diff(Gt, x, 2) - G) == 0)
u3 = G + (t - 1) * sp.exp((t - 1) + x)
heat = lambda g: dt(g) - sp.diff(g, x, 2)
chk('INT-18 P u3 = 0 e (tau-xi^2)u3 = e^{(t-1)+x}', sp.simplify(heat(heat(u3))) == 0 and sp.simplify(heat(u3) - sp.exp(t - 1 + x)) == 0)
chk('INT-18 (1,1) in V(tau - xi^2) (punto assorbito)', (1 - 1**2) == 0)

ok = sum(1 for _, r in RES if r)
print('TOTALE %d/%d OK' % (ok, len(RES)))
