# OP-ALG — controlli SymPy (solo controllo, aritmetica esatta; mai metodo di prova)
# Esecuzione: D:\ProblemaBase\.venv\Scripts\python.exe -I op_alg_checks.py > op_alg_checks.out
import random
import sympy as sp

t, x, s, n, tau, xi, lam = sp.symbols('t x s n tau xi lam')
RES = []


def check(name, cond, info=''):
    ok = bool(cond)
    RES.append((name, ok))
    print(('OK  ' if ok else 'FAIL') + ' ' + name + ((' :: ' + str(info)) if info != '' else ''))


# ---------- utilita' -------------------------------------------------------
def apply_dt_ops(coeffs, f, var):
    """coeffs: lista [b_0, b_1, ...] (polinomi), operatore sum_j b_j d_var^j applicato a f."""
    return sum(c * sp.diff(f, var, j) for j, c in enumerate(coeffs))


def rational_ratio(expr, f):
    return sp.simplify(sp.together(expr / f))


def find_eliminant(parts, var, order, deg):
    """Cerca L = sum_{j<=order} b_j(t,x) d_var^j, deg_tot b_j <= deg, con L f = 0 per ogni f in parts
    (condizione sufficiente per L u = 0, u = sum parts). Restituisce la lista dei b_j o None."""
    unknowns = []
    coeffs = []
    for j in range(order + 1):
        cj = 0
        for a in range(deg + 1):
            for b in range(deg + 1 - a):
                c = sp.Symbol('c_%d_%d_%d' % (j, a, b))
                unknowns.append(c)
                cj += c * t**a * x**b
        coeffs.append(cj)
    eqs = []
    for f in parts:
        r = sp.together(sp.expand(apply_dt_ops(coeffs, f, var) / f))
        num = sp.numer(sp.together(sp.simplify(r)))
        num = sp.expand(num)
        eqs += sp.Poly(num, t, x).coeffs()
    sol = sp.linsolve(eqs, unknowns)
    sol = list(sol)[0]
    free = sorted(set().union(*[sp.sympify(v).free_symbols for v in sol]) & set(unknowns), key=str)
    if not free:
        return None
    subs = {fv: 0 for fv in free}
    subs[free[0]] = 1
    vals = [sp.sympify(v).subs(subs) for v in sol]
    m = dict(zip(unknowns, vals))
    res = [sp.expand(c.subs(m)) for c in coeffs]
    if all(r == 0 for r in res):
        return None
    return res


def exponent_set_and_degree(coeffs, var, other):
    """Lemma D (OP-ALG-L4): da L = sum_j b_j(t,x) d_var^j calcola T (radici di M_D) e N(tau)."""
    # scrittura L = sum beta_{ij}(other) var^i d^j
    terms = {}
    for j, b in enumerate(coeffs):
        P = sp.Poly(sp.expand(b), var)
        for (i,), c in P.terms():
            terms[(i, j)] = sp.expand(c)
    D = max(i for (i, j) in terms)
    MD = sp.expand(sum(terms.get((D, j), 0) * tau**j for j in range(len(coeffs))))
    # radici comuni dei coefficienti in 'other'
    cs = sp.Poly(MD, other).coeffs()
    g = cs[0]
    for c in cs[1:]:
        g = sp.gcd(g, c)
    T = [r for r in sp.roots(sp.Poly(g, tau)).keys()] if sp.Poly(g, tau).degree() > 0 else []
    Nmap = {}
    for r in T:
        # operatore coniugato L_r = sum beta_{ij} var^i (d + r)^j
        gam = {}
        for (i, j), c in terms.items():
            for l in range(j + 1):
                gam[(i, l)] = sp.expand(gam.get((i, l), 0) + c * sp.binomial(j, l) * r**(j - l))
        gam = {k: v for k, v in gam.items() if v != 0}
        dl = max(i - l for (i, l) in gam)
        iota = sp.expand(sum(v * sp.ff(n, l) for (i, l), v in gam.items() if i - l == dl))
        ci = sp.Poly(iota, other).coeffs()
        gi = ci[0]
        for c in ci[1:]:
            gi = sp.gcd(gi, c)
        roots = [k for k in sp.roots(sp.Poly(gi, n)).keys() if k.is_integer and k >= 0] if sp.Poly(gi, n).degree() > 0 else []
        Nmap[r] = max(roots) if roots else -1
    return D, MD, T, Nmap


def a_star(T, Nmap, sym):
    out = sp.Integer(1)
    for r in T:
        if Nmap[r] >= 0:
            out *= (sym - r)**(Nmap[r] + 1)
    return sp.expand(out)


def apply_poly_d(poly, sym, f, var):
    P = sp.Poly(poly, sym)
    return sum(c * sp.diff(f, var, k) for (k,), c in P.terms())


def zero_test_K0(coeffs, var, var0, other):
    """Lemma B (OP-ALG-L2): indicial a parametro in var = var0. Restituisce delta, iota, K0."""
    terms = {}
    for j, b in enumerate(coeffs):
        P = sp.Poly(sp.expand(sp.expand(b).subs(var, s + var0)), s)
        for (i,), c in P.terms():
            terms[(i, j)] = sp.expand(c)
    terms = {k: v for k, v in terms.items() if v != 0}
    dl = min(i - j for (i, j) in terms)
    iota = sp.expand(sum(v * sp.ff(n, j) for (i, j), v in terms.items() if i - j == dl))
    ci = sp.Poly(iota, other).coeffs()
    gi = ci[0]
    for c in ci[1:]:
        gi = sp.gcd(gi, c)
    roots = [k for k in sp.roots(sp.Poly(gi, n)).keys() if k.is_integer and k >= 0] if sp.Poly(gi, n).degree() > 0 else []
    return dl, iota, (max(roots) if roots else -1)


G = t**sp.Rational(-1, 2) * sp.exp(-x**2 / (4 * t))
E = sp.exp(t + x)

print('=== Q1: test EP via eliminanti (OP-ALG-T1) ===')
# E1: u = G + e^{t+x}; P = tau - xi^2 irriducibile: Ann(u) = (P) <=> u non EP
Lt = next(L for L in (find_eliminant([G, E], t, 2, dd) for dd in range(1, 6)) if L is not None)
check('Q1-E1a eliminante in t per G + e^{t+x} trovato', Lt is not None, Lt)
check('Q1-E1b L_t annulla u', sp.simplify(apply_dt_ops(Lt, G + E, t)) == 0)
D, MD, Tt, Nt = exponent_set_and_degree(Lt, t, x)
check('Q1-E1c esponente tau=1 di e^{t+x} in T_t', 1 in Tt, (MD, Tt, Nt))
Lx = next(L for L in (find_eliminant([G, E], x, 2, dd) for dd in range(1, 6)) if L is not None)
check('Q1-E1d eliminante in x trovato', Lx is not None, Lx)
Dx, MDx, Tx, Nx = exponent_set_and_degree(Lx, x, t)
check('Q1-E1e esponente xi=1 in T_x', 1 in Tx, (MDx, Tx, Nx))
as_ = a_star(Tt, Nt, tau)
bs_ = a_star(Tx, Nx, xi)
u = G + E
A1 = sp.simplify(apply_poly_d(as_, tau, u, t))
check('Q1-E1f a*(d_t)u != 0  => u non EP => Ann(u)=(tau-xi^2)', A1 != 0, as_)
# parte EP da sola: e^{t+x}
A2 = sp.simplify(apply_poly_d(as_, tau, E, t))
B2 = sp.simplify(apply_poly_d(bs_, xi, E, x))
check('Q1-E1g e^{t+x}: a*(d_t)E = 0 e b*(d_x)E = 0 (EP riconosciuto)', A2 == 0 and B2 == 0)

# E2: P non monico (P4-C4(b)): u = e^{t^2}, P = xi (tau - 1)
U2 = sp.exp(t**2)
w = sp.diff(U2, t) - U2
Lw = [-(4 * t**2 - 2 * t + 2), 2 * t - 1]
check('Q1-E2a L_w = (2t-1)d_t - (4t^2-2t+2) annulla w = (2t-1)e^{t^2}', sp.simplify(apply_dt_ops(Lw, w, t)) == 0)
D2, MD2, T2, N2 = exponent_set_and_degree(Lw, t, x)
check('Q1-E2b T_t vuoto => w EP solo se w = 0; w != 0 => w non EP', T2 == [] and sp.simplify(w) != 0, (D2, MD2))
check('Q1-E2c fattore tau-1: (P/(tau-1))u = d_x u = 0 (EP) => G_u = xi', sp.diff(U2, x) == 0)

# E3: test di zero con indiciale a parametro in p0=(1,0) per G: L = 4t^2 d_t + 2t - x^2
LG = [2 * t - x**2, 4 * t**2]
check('Q1-E3a L annulla G', sp.simplify(apply_dt_ops(LG, G, t)) == 0)
dl, io, K0 = zero_test_K0(LG, t, 1, x)
check('Q1-E3b indiciale iota(n)=4n, K0=0 (punto regolare)', K0 == 0, (dl, io))
# punto singolare: v = t^3 * x  annullato da t d_t - 3 ; in t0 = 0: K0 = 3
dl2, io2, K02 = zero_test_K0([-3, t], t, 0, x)
check('Q1-E3c t d_t - 3 in t0=0: K0 = 3 (servono 4 coefficienti)', K02 == 3, (dl2, io2))
# coefficiente a parametro che si annulla solo per alcuni x: L = x d_t - 2 t ... in t0 = 0
dl3, io3, K03 = zero_test_K0([-(x + 1) * 2, (x + 1) * t], t, 0, x)
check('Q1-E3d iota(n;x) = (x+1)(n-2): K0 = 2', K03 == 2, io3)

print('=== QMIN: avversario per B (OP-ALG-T3) ===')
# P = (tau - xi^2)^2, Ptilde = tau - xi^2, u = G + e, e = (t-1) e^{(t-1)+x}, p0 = (1,0)
p0 = {t: 1, x: 0}
e = (t - 1) * sp.exp((t - 1) + x)
uq = G + e
heat = lambda f: sp.diff(f, t) - sp.diff(f, x, 2)
check('QMIN-a P(d)u = 0', sp.simplify(heat(heat(uq))) == 0)
check('QMIN-b (tau-xi^2)u = e^{(t-1)+x} (EP, chi=0)', sp.simplify(heat(uq) - sp.exp(t - 1 + x)) == 0)
k0 = 2
alphas = [(a, b) for a in range(k0 + 1) for b in range(k0 + 1 - a)]
N0 = len(alphas)


def jet(f):
    return [sp.nsimplify(sp.simplify(sp.diff(f, t, a, x, b).subs(p0))) for (a, b) in alphas]


JG = jet(G)
check('QMIN-c getti di G in (1,0) razionali', all(v.is_rational for v in JG), JG)


def mode_jet(k):
    z = (k**2, k)
    return [sp.Integer(z[0])**a * sp.Integer(z[1])**b for (a, b) in alphas]


# v1 in span{e^{z(y-p0)}: z=(k^2,k)} con stesso 2-getto di G
ks = list(range(-4, 5))
M = sp.Matrix([mode_jet(k) for k in ks]).T  # N0 x |ks|
cvec = sp.symbols('cv0:%d' % len(ks))
sol = sp.linsolve((M, sp.Matrix(JG)), cvec)
sol = list(sol)[0]
random.seed(7)
fr = sorted(set().union(*[sp.sympify(v).free_symbols for v in sol]), key=str)
subsv = {f: sp.Rational(random.randint(1, 50), random.randint(1, 9)) for f in fr}
cv = [sp.sympify(v).subs(subsv) for v in sol]
v1 = sum(c * sp.exp(k**2 * (t - 1) + k * x) for c, k in zip(cv, ks))
check('QMIN-d v1 EP in ker(tau-xi^2) con 2-getto di G', [sp.simplify(a - b) for a, b in zip(jet(v1), JG)] == [0] * N0)
# padding eta con getto nullo e molti esponenti nuovi
Bclaimed = 5  # uscita ipotetica dell'algoritmo
newk = list(range(5, 5 + Bclaimed + N0 + 1))
Mn = sp.Matrix([mode_jet(k) for k in newk]).T
ns = Mn.nullspace()
check('QMIN-e spazio dei padding a getto nullo: dim >= |F| - N0', len(ns) >= len(newk) - N0, len(ns))
eta_c = sum((sp.Rational(random.randint(1, 30), random.randint(1, 7)) * vv for vv in ns), sp.zeros(len(newk), 1))
nonzero_modes = sum(1 for c in eta_c if c != 0)
check('QMIN-f padding generico: > B modi non nulli', nonzero_modes > Bclaimed, nonzero_modes)
eta = sum(c * sp.exp(k**2 * (t - 1) + k * x) for c, k in zip(eta_c, newk))
up = v1 + eta + e
check('QMIN-g u\' ha lo stesso 2-getto di u', [sp.simplify(a - b) for a, b in zip(jet(up), jet(uq))] == [0] * N0)
# risposte di zero su un Q campione
def Qapply(Q, f):
    P_ = sp.Poly(Q, tau, xi)
    return sum(c * sp.diff(f, t, a, x, b) if (a or b) else c * f for (a, b), c in P_.terms())
Qs = [(tau - xi**2) * (xi - 1), (tau - xi**2) * (tau - 1), tau - xi**2, xi, tau + 1, (tau - xi**2)**2]
same = True
for Q in Qs:
    z1 = sp.simplify(Qapply(Q, uq)) == 0
    z2 = sp.simplify(Qapply(Q, up)) == 0
    same = same and (z1 == z2)
check('QMIN-h stesse risposte di zero su 6 operatori campione', same)
check('QMIN-i u\' EP con > B esponenti distinti: dim R u\' > B, mentre dim(R u cap EP) = 1', nonzero_modes + 1 > Bclaimed)

print('=== Q2: algebra di Weyl, controesempio alla struttura G.J (OP-ALG-C1) ===')
f = sp.Function('f')(t, x)
th = lambda g: x * sp.diff(g, x)
P1 = lambda g: sp.diff(g, t) - th(g)
P2 = lambda g: sp.diff(g, t) - th(g) + g
Dx = lambda g: sp.diff(g, x)
check('Q2-a P1 d_x = d_x P2', sp.simplify(P1(Dx(f)) - Dx(P2(f))) == 0)
check('Q2-b P1 P2 = P2 P1', sp.simplify(P1(P2(f)) - P2(P1(f))) == 0)
check('Q2-c P2 - P1 = 1 (comassimali)', sp.simplify(P2(f) - P1(f) - f) == 0)
Pfull = lambda g: P1(P2(g))
Ql = lambda g: P2(g) + lam * Dx(P1(g))
check('Q2-d (1 + lam d_x) P = P1 Q_lam', sp.simplify(Pfull(f) + lam * Dx(Pfull(f)) - P1(Ql(f))) == 0)
u2 = sp.exp(-t) * sp.exp(x**2 * sp.exp(2 * t))
ul = u2 + lam * Dx(u2)
check('Q2-e u2 in ker P2', sp.simplify(P2(u2)) == 0)
check('Q2-f P u^(lam) = 0', sp.simplify(Pfull(ul)) == 0)
check('Q2-g Q_lam u^(lam) = 0 (Q_lam di grado 1 in d_t: Ann != A P)', sp.simplify(Ql(ul)) == 0)
check('Q2-h (P/P2)u = P1 u = -u2', sp.simplify(P1(ul) + u2) == 0)
check('Q2-i (P/P1)u = P2 u = lam d_x u2', sp.simplify(P2(ul) - lam * Dx(u2)) == 0)
mu = sp.Symbol('mu')
Qm = lambda g: P2(g) + mu * Dx(P1(g))
check('Q2-j Q_mu u^(lam) = (lam - mu) d_x u2', sp.simplify(Qm(ul) - (lam - mu) * Dx(u2)) == 0)
# V-ex: u2 non e' di torsione: nessun b in A_1 di ordine <= 2, coeff. grado <= 2 annulla u2
cc = sp.symbols('b0:9')
b_op = lambda g: sum(cc[3 * j + d] * x**d * sp.diff(g, x, j) for j in range(3) for d in range(3))
expr = sp.expand(sp.simplify(b_op(u2) / u2))
eqs = sp.Poly(sp.expand(expr.subs(sp.exp(2 * t), s)), x, s).coeffs()
solb = sp.linsolve(eqs, cc)
check('Q2-k (V-ex) u2 non annullato da b in A_1 (ord<=2, grado<=2)', solb == sp.FiniteSet(tuple([0] * 9)))
# esempio identificante u* = exp(x e^t) + e^{-t} exp(-x e^t)
ustar1 = sp.exp(x * sp.exp(t))
ustar2 = sp.exp(-t) * sp.exp(-x * sp.exp(t))
check('Q2-l u*_1 in ker P1, u*_2 in ker P2', sp.simplify(P1(ustar1)) == 0 and sp.simplify(P2(ustar2)) == 0)
# V-ex: nessuna relazione c u1 + d u2 = 0 con c, d in A_1 di ordine <= 1, grado <= 1
cs_ = sp.symbols('c0:8')
c_op = lambda g: sum(cs_[2 * j + d] * x**d * sp.diff(g, x, j) for j in range(2) for d in range(2))
d_op = lambda g: sum(cs_[4 + 2 * j + d] * x**d * sp.diff(g, x, j) for j in range(2) for d in range(2))
r1 = sp.expand(sp.simplify(c_op(ustar1) / ustar1)).subs(sp.exp(t), s)
r2 = sp.expand(sp.simplify(d_op(ustar2) / ustar2)).subs(sp.exp(t), s)
eqs2 = sp.Poly(sp.expand(r1), x, s).coeffs() + sp.Poly(sp.expand(r2 * s), x, s).coeffs()
check('Q2-m (V-ex) u* identifica: nessuna relazione di ordine/grado <= 1', sp.linsolve(eqs2, cs_) == sp.FiniteSet(tuple([0] * 8)))

print('=== INT-18: esempi per il testo di G* punto 1 ===')
check('I18-a P=(tau-xi^2)^2, u=G: (P/P_1)u = 0 in EP => Ann(G) != (P)', sp.simplify(heat(G)) == 0)
check('I18-b ... ma (P/P_1^2)u = G non EP => V(Ann G) = V(P) (radicale uguale, ideale no)', sp.simplify(G) != 0)
check('I18-c u = tG: (P/P_1)u = G non EP => Ann(tG) = (P)', sp.simplify(heat(t * G) - G) == 0)
uu = G + (t - 1) * sp.exp(t - 1 + x)
check('I18-d u = G + (t-1)e^{t-1+x}: G_u = tau - xi^2, J_u = m_(1,1) (parte EP di dim 1)',
      sp.simplify(heat(uu) - sp.exp(t - 1 + x)) == 0)

print()
print('TOTALE: %d/%d OK' % (sum(1 for _, o in RES if o), len(RES)))
