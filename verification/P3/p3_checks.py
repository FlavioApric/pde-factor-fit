"""S-P3 -- verifiche simboliche (solo controlli, non metodo di prova).
Eseguire: D:\\ProblemaBase\\.venv\\Scripts\\python.exe -I p3_checks.py
Sezioni C1..C8 corrispondono ai claim di work/P3/PROOF_PACKAGE.md.
"""
import sympy as sp

RESULTS = []


def check(name, cond):
    ok = bool(cond)
    RESULTS.append((name, ok))
    print(("PASS " if ok else "FAIL ") + name)


def is_zero(e):
    return sp.simplify(sp.expand(e)) == 0


# ---------------------------------------------------------------- C1
# P3-T1: ricorrenza di Beta per la stima di Mittag-Leffler, e sup y^k e^{-s d y^q}
t, s, y = sp.symbols('t s y', positive=True)
for beta in [sp.Rational(1, 2), sp.Rational(1, 3), sp.Rational(2, 3)]:
    g = 1 - beta
    for n in range(0, 4):
        lhs = sp.integrate((t - s) ** (n * g) * s ** (-beta), (s, 0, t)) / sp.gamma(1 + n * g)
        rhs = sp.gamma(g) * t ** ((n + 1) * g) / sp.gamma(1 + (n + 1) * g)
        ok1 = is_zero(sp.gammasimp(sp.hyperexpand(lhs) - rhs))
        if not ok1:  # forma ipergeometrica non semplificata: confronto a 40 cifre in due punti
            ok1 = all(abs(sp.N((lhs - rhs).subs(t, tv), 40)) < 1e-35 for tv in [sp.Rational(1, 3), 2])
        check(f"C1 Beta recursion beta={beta} n={n}", ok1)
d = sp.symbols('delta', positive=True)
for k, q in [(1, 2), (1, 4), (3, 4), (2, 6)]:
    f = y ** k * sp.exp(-s * d * y ** q)
    ycrit = sp.solve(sp.diff(sp.log(f), y), y)
    ycrit = [r for r in ycrit if r.is_positive]
    val = sp.simplify(f.subs(y, ycrit[0]))
    target = (sp.Integer(k) / (q * d * s * sp.E)) ** sp.Rational(k, q)
    check(f"C1 sup y^k e^(-s d y^q) k={k} q={q}", is_zero(sp.simplify(val / target) - 1))

# ---------------------------------------------------------------- C2
# P3-T2: formula dei cammini (differenze divise) per i termini di Dyson, via Van Loan.
z = sp.symbols('z')


def divdiff(points):
    """differenza divisa di f(z)=exp(t z) su punti (anche ripetuti) -- via Hermite-Genocchi
    con integrazione simbolica sul simplesso (valida sempre)."""
    j = len(points) - 1
    th = sp.symbols('th0:%d' % (j + 1))
    # integrale iterato sul simplesso standard: sum th = 1, th>=0
    expr = sp.exp(t * sum(th[i] * points[i] for i in range(j + 1)))
    expr = expr.subs(th[j], 1 - sum(th[:j]))
    res = expr * t ** j
    bounds = []
    for i in range(j - 1, -1, -1):
        upper = 1 - sum(th[:i])
        res = sp.integrate(res, (th[i], 0, upper))
    return sp.simplify(res)


lam = [0, -1, -3]
A = sp.diag(*lam)
V = sp.Matrix([[1, 2, -1], [3, 0, 5], [-2, 4, 1]])
Z3 = sp.zeros(3)
M1 = sp.Matrix(sp.BlockMatrix([[A, V], [Z3, A]]))
E1 = (M1 * t).exp()
F1 = E1[0:3, 3:6]
ok = True
for m in range(3):
    for n in range(3):
        pred = V[m, n] * divdiff([lam[n], lam[m]])
        ok &= is_zero(F1[m, n] - pred)
check("C2 primo ordine = V_mn e^{t.}[l_n,l_m] (PR-C2d P3.2)", ok)
M2 = sp.Matrix(sp.BlockMatrix([[A, V, Z3], [Z3, A, V], [Z3, Z3, A]]))
E2 = (M2 * t).exp()
F2 = E2[0:3, 6:9]
ok = True
for m in range(3):
    for n in range(3):
        pred = sum(V[m, k] * V[k, n] * divdiff([lam[n], lam[k], lam[m]]) for k in range(3))
        ok &= is_zero(F2[m, n] - pred)
check("C2 secondo ordine = somma sui cammini n->k->m", ok)
# filtrazione: V strettamente triangolare (abbassa il grado) => Dyson finito
Vn = sp.Matrix([[0, 2, 7], [0, 0, 5], [0, 0, 0]])
lam4 = [0, -1, -3]
A4 = sp.diag(*lam4)
eps = sp.symbols('epsilon')
full = ((A4 + eps * Vn) * t).exp()
deg_eps = sp.Poly(sp.expand(full[0, 2]), eps).degree()
check("C2 V nilpotente (abbassa il grado) => polinomio in eps di grado <= 2", deg_eps <= 2)
# commutante: lambda tutti uguali => e^{t.}[l,..,l] = t^j e^{tl}/j!
check("C2 punti coincidenti: e^{t.}[l,l,l] = t^2 e^{tl}/2", is_zero(divdiff([-1, -1, -1]) - t ** 2 * sp.exp(-t) / 2))

# ---------------------------------------------------------------- C3
# P3-T3: AD con Dirichlet su (0,L): elementi di matrice di V=-c d/dx nella base dei seni
x = sp.symbols('x', real=True)
L, c, D = sp.symbols('L c D', positive=True)
ok = True
for m in range(1, 7):
    for n in range(1, 7):
        em = sp.sqrt(2 / L) * sp.sin(m * sp.pi * x / L)
        en = sp.sqrt(2 / L) * sp.sin(n * sp.pi * x / L)
        Vmn = sp.integrate(em * (-c) * sp.diff(en, x), (x, 0, L))
        if (m + n) % 2 == 0:
            pred = 0
        else:
            pred = -c * 4 * m * n / (L * (m ** 2 - n ** 2))
        ok &= is_zero(sp.simplify(Vmn - pred))
check("C3 V_mn = -4cmn/(L(m^2-n^2)) per m+n dispari, 0 altrimenti (m,n<=6)", ok)
# g(a,b) = e^{-a} - e^{-b}(1+b-a) = int_a^b e^{-y}(y-a) dy
a_, b_ = sp.symbols('a b', positive=True)
gint = sp.integrate(sp.exp(-y) * (y - a_), (y, a_, b_))
check("C3 g = int_a^b e^{-y}(y-a)dy", is_zero(gint - (sp.exp(-a_) - sp.exp(-b_) * (1 + b_ - a_))))
# termine T_m: forma chiusa del coefficiente modale
lm, l1 = sp.symbols('lambda_m lambda_1')
coef = (sp.exp(l1 * t) - sp.exp(lm * t)) / (l1 - lm) - t * sp.exp(lm * t)
kap, mm = sp.symbols('kappa m', positive=True)
coef_sub = coef.subs({l1: -kap, lm: -kap * mm ** 2})
gform = (sp.exp(-kap * t) - sp.exp(-kap * mm ** 2 * t) * (1 + kap * (mm ** 2 - 1) * t)) / (kap * (mm ** 2 - 1))
check("C3 coefficiente modale = g(kt, km^2 t)/(k(m^2-1))", is_zero(sp.simplify(coef_sub - gform)))
# controllo numerico (NON prova) della pendenza 5/4 per u0 = e_1
import math


def normE(tt, Lv=1.0, cv=1.0, Dv=1.0):
    kv = Dv * math.pi ** 2 / Lv ** 2
    N = int(60 / math.sqrt(tt)) + 50
    tot = 0.0
    for mv in range(2, N, 2):
        Vm1 = -cv * 4 * mv / (Lv * (mv ** 2 - 1))
        a1 = kv * tt
        b1 = kv * mv ** 2 * tt
        gv = math.exp(-a1) - math.exp(-b1) * (1 + b1 - a1)
        tot += (Vm1 * gv / (kv * (mv ** 2 - 1))) ** 2
    return math.sqrt(tot)


ts = [1e-4, 1e-5, 1e-6]
vals = [normE(tt) for tt in ts]
slopes = [math.log(vals[i + 1] / vals[i]) / math.log(ts[i + 1] / ts[i]) for i in range(2)]
print("   [controllo numerico] pendenze log-log:", slopes)
check("C3 [controllo] pendenza ~ 5/4", all(abs(sl - 1.25) < 0.02 for sl in slopes))

# ---------------------------------------------------------------- C4
# P3-T4: perturbazione eps*x di un fattore tau - a(xi)
al = sp.symbols('alpha0:4')
xi, zeta, sig = sp.symbols('xi zeta sigma')
a = sum(al[k] * xi ** k for k in range(4))
B = sp.integrate(a.subs(xi, xi + eps * sig), (sig, 0, t))
u = sp.exp((zeta + eps * t) * x + B.subs(xi, zeta))
# a(d/dx) u = a(zeta+eps t) u per un esponenziale in x
lhs = sp.diff(u, t)
rhs = a.subs(xi, zeta + eps * t) * u + eps * x * u
check("C4 u = exp((zeta+eps t)x + int a) risolve u_t = a(d)u + eps x u", is_zero(sp.simplify((lhs - rhs) / u)))
series = sum(sp.diff(a, xi, k) * eps ** k * t ** (k + 1) / sp.factorial(k + 1) for k in range(1, 4))
check("C4 B_t - t a = sum_{k>=1} a^(k) eps^k t^{k+1}/(k+1)!", is_zero(sp.expand(B - t * a - series)))
check("C4 grado in eps di B_t - t a = deg a = 3", sp.Poly(sp.expand(B - t * a), eps).degree() == 3)
# regola di selezione nella base di Appell: (x-x0) v_n = v_{n+1} - t sum_j C(n,j) a^{(j+1)}(0) v_{n-j}
x0, zz = sp.symbols('x0 z')
az = a.subs(xi, zz)
G = sp.exp(zz * (x - x0) + t * az)
vv = [sp.simplify(sp.diff(G, zz, n).subs(zz, 0)) for n in range(8)]
ok = True
for n in range(0, 6):
    rhs = vv[n + 1] - t * sum(sp.binomial(n, j) * sp.diff(az, zz, j + 1).subs(zz, 0) * vv[n - j] for j in range(0, n + 1))
    ok &= is_zero(sp.expand((x - x0) * vv[n] - rhs))
check("C4 (x-x0)v_n = v_{n+1} - t sum C(n,j) a^(j+1)(0) v_{n-j} (n<=5)", ok)

# ---------------------------------------------------------------- C5
# P3-P2: Kato al 1° ordine per la compagna = accoppiamento con i duali di Lagrange
l = sp.symbols('l1:4')
tt_ = sp.symbols('t0:3')
S = sp.symbols('S')
P = sp.expand((S - l[0]) * (S - l[1]) * (S - l[2]))
T = tt_[0] + tt_[1] * S + tt_[2] * S ** 2


def companion(poly, k):
    co = sp.Poly(poly, S).all_coeffs()[::-1]  # p0..pk
    C = sp.zeros(k)
    for i in range(k - 1):
        C[i, i + 1] = 1
    for j in range(k):
        C[k - 1, j] = -co[j] / co[k]
    return C


C0 = companion(P, 3)
C1 = companion(P + eps * T, 3) - C0
C1 = C1.applyfunc(lambda e: sp.diff(e, eps).subs(eps, 0))
Vand = sp.Matrix([[l[j] ** i for j in range(3)] for i in range(3)])
W = Vand.inv()
ok = True
for a_i in range(3):
    va = Vand[:, a_i]
    wa = W[a_i, :]
    lhs = (wa * C1 * va)[0, 0]
    rhs = -T.subs(S, l[a_i]) / sp.diff(P, S).subs(S, l[a_i])
    ok &= is_zero(sp.simplify(lhs - rhs))
check("C5 w_a^T C1 v_a = -T(l_a)/P'(l_a)", ok)
# coerenza con la derivata implicita della radice
lam_eps = sp.symbols('lam_eps')
dl = -sp.diff(P + eps * T, eps) / sp.diff(P + eps * T, S)
check("C5 derivata implicita della radice", is_zero(sp.simplify(dl.subs({eps: 0, S: l[0]}) + T.subs(S, l[0]) / sp.diff(P, S).subs(S, l[0]))))
# ultima coordinata del duale = 1/P'(l_a)
check("C5 (w_a)_k = 1/P'(l_a)", all(is_zero(sp.simplify(W[i, 2] - 1 / sp.diff(P, S).subs(S, l[i]))) for i in range(3)))

# ---------------------------------------------------------------- C6
# P3-T6: Faddeev / bilancio, livello spettrale (zeta fissato, valori a_i dei termini)
ai = sp.symbols('a1:4')
atot = sum(ai)
Eis = [(ai[i] / atot) * (sp.exp(atot * s) - 1) - (sp.exp(ai[i] * s) - 1) for i in range(3)]
Eadd = sp.exp(atot * s) - 1 - sum(sp.exp(ai[i] * s) - 1 for i in range(3))
check("C6 E^add = sum_i E^(i)", is_zero(sp.simplify(sum(Eis) - Eadd)))
ok = True
for i in range(3):
    ser = sp.series(Eis[i], s, 0, 3).removeO()
    pred = s ** 2 / 2 * ai[i] * (atot - ai[i])
    ok &= is_zero(sp.expand(ser - pred))
check("C6 E^(i) = (s^2/2) a_i sum_{j!=i} a_j + O(s^3) (attribuzione simmetrica)", ok)
# sistema accoppiato: u^(i) = G_i A_i (u0 + sum_{j!=i} u^(j)), G_i f = int_0^t e^{a_i(t-r)} f(r) dr
r = sp.symbols('r', positive=True)
ui = [(ai[i] / atot) * (sp.exp(atot * t) - 1) for i in range(3)]  # u0 = 1 (modo fissato)
ok = True
for i in range(3):
    f = 1 + sum(ui[j] for j in range(3) if j != i)
    # u^(i) = G_i A_i f  <=>  (d_t - a_i) u^(i) = a_i f  e  u^(i)(0) = 0 (unicita' per l'ODE lineare)
    ok &= is_zero(sp.simplify(sp.diff(ui[i], t) - ai[i] * ui[i] - ai[i] * f)) and is_zero(ui[i].subs(t, 0))
check("C6 equazioni di Faddeev accoppiate (N=3) sui modi", ok)
# risonanza secolare: G_c A_c su g(s,x)=e^{i k (x+s)}, trasporto d/dx (gruppo f(x) -> f(x+r))
kk = sp.symbols('k', positive=True)
gfun = lambda rr, xx: sp.exp(sp.I * kk * (xx + rr))
integrand = sp.I * kk * gfun(r, x + (t - r))  # T(t-r) d_x g(r)
res = sp.integrate(integrand, (r, 0, t))
check("C6 risonanza: G_c A_c g = i k t e^{ik(x+t)} (norma ~ k t, illimitata)", is_zero(sp.simplify(res - sp.I * kk * t * sp.exp(sp.I * kk * (x + t)))))

# ---------------------------------------------------------------- C7
# P3-T5: duali di Rosenbloom-Widder generalizzati
# (a) parte algebrica: (d^m e^{s a(d)} v_n(-s,.))(x0) = n! delta_{mn}, a cubico generico
ss = sp.symbols('s')
vn_t = lambda n, tv: sp.diff(sp.exp(zz * (x - x0) + tv * az), zz, n).subs(zz, 0)


def apply_exp_a(poly_in_x, sv, order=40):
    # e^{s a(d)} = e^{s alpha0} e^{s (a-alpha0)(d)}; il secondo fattore e' nilpotente sui polinomi
    res = 0
    term = poly_in_x
    for kq in range(order):
        res += sv ** kq / sp.factorial(kq) * term
        term = sp.expand(sum(al[j] * sp.diff(term, x, j) for j in range(1, 4)))
        if term == 0:
            break
    return sp.expand(sp.exp(sv * al[0]) * res)


ok = True
for n in range(0, 4):
    pol = sp.expand(vn_t(n, -ss))
    ev = apply_exp_a(pol, ss, order=2 * n + 3)
    for m in range(0, 4):
        val = sp.diff(ev, x, m).subs(x, x0)
        ok &= is_zero(sp.simplify(val - (sp.factorial(n) if m == n else 0)))
check("C7 (d^m e^{s a(d)} v_n(-s))(x0) = n! delta (a cubico, n,m<=3)", ok)
# (b) AD: nucleo gaussiano esplicito K_s(z) = G(z - c s, s), integrale
s_p = sp.symbols('s_p', positive=True)
yv = sp.symbols('yv', real=True)
x0r = sp.symbols('x0r', real=True)
aAD = D * zz ** 2 - c * zz
Gz = lambda zv: sp.exp(-(zv) ** 2 / (4 * D * s_p)) / sp.sqrt(4 * sp.pi * D * s_p)
Ks = lambda zv: Gz(zv - c * s_p)
ok = True
for n in range(0, 3):
    vn = sp.expand(sp.diff(sp.exp(zz * (yv - x0r) - s_p * aAD), zz, n).subs(zz, 0))
    for m in range(0, 3):
        wq = sp.symbols('wq', real=True)
        Km = sp.diff(Ks(wq), wq, m).subs(wq, x0r - yv)
        val = sp.integrate(sp.expand(vn * Km), (yv, -sp.oo, sp.oo))
        ok &= is_zero(sp.simplify(val - (sp.factorial(n) if m == n else 0)))
check("C7 AD: int v_n(-s,y) K_s^(m)(x0-y) dy = n! delta (n,m<=2)", ok)
# (c) criterio: Re a(i k) per KdV-Burgers a = -xi^3 + D xi^2 ha grado pari 2, coeff -D
kr = sp.symbols('kr', real=True)
aKB = -zz ** 3 + D * zz ** 2
check("C7 KdV-Burgers: Re a(ik) = -D k^2", is_zero(sp.re(sp.expand(aKB.subs(zz, sp.I * kr))) + D * kr ** 2))
aAiry = zz ** 3
check("C7 Airy: Re a(ik) = 0 (nessun nucleo di Schwartz)", is_zero(sp.re(sp.expand(aAiry.subs(zz, sp.I * kr)))))

# ---------------------------------------------------------------- C8
# P3-P1: E_int al 1° ordine nei quadri; caso commutante => R5-T2
lmb, lnb = sp.symbols('lambda_m lambda_n')
dd1 = (sp.exp(lnb * t) - sp.exp(lmb * t)) / (lnb - lmb)
Emult = dd1 - t * sp.exp(lmb * t)
Eadd1 = dd1 - t
check("C8 mult: lambda_n -> lambda_m da' 0 (commutante)", is_zero(sp.limit(Emult, lnb, lmb)))
check("C8 add: lambda_n -> lambda_m da' t(e^{t l}-1) = R5-T2 al 1° ordine", is_zero(sp.limit(Eadd1, lnb, lmb) - t * (sp.exp(lmb * t) - 1)))
check("C8 mult = t e^{t l_m} phi(t(l_n-l_m)), phi(w)=(e^w-1-w)/w", is_zero(sp.simplify(Emult - t * sp.exp(lmb * t) * ((sp.exp(t * (lnb - lmb)) - 1 - t * (lnb - lmb)) / (t * (lnb - lmb))))))

print()
npass = sum(1 for _, o in RESULTS if o)
print(f"TOTALE: {npass}/{len(RESULTS)} PASS")
