# S5-EX · E4 Airy PDE u_t = -u_xxx (P = tau + xi^3), KdV lineare (tau + c xi + xi^3);
#          E5 Airy EDO y'' = x y (operatore d^2 - x in A_1) e coefficienti variabili in D = A_1[d_t]
# Teoremi: C3-T1(d)/C3-T4, C3-T3, P2-T2, P1-T2(iv), P3-T1(a1) [coefficienti costanti];
#          P4-C1, OP-ALG-T4, OP-ALG-P5, OPR2-T3 [coefficienti variabili]
# Eseguire: D:\ProblemaBase\.venv\Scripts\python.exe -I ex4_airy.py
import sys
import sympy as sp
import mpmath as mp

sys.stdout.reconfigure(encoding='utf-8')
t, x = sp.symbols('t x', positive=True)
X = sp.symbols('X', real=True)
tau, xi = sp.symbols('tau xi')
RES = []


def check(name, cond, info=''):
    RES.append((name, bool(cond)))
    print(('[OK]   ' if cond else '[FAIL] ') + name + ((' :: ' + str(info)) if info != '' else ''))


def der(u, i, j, xx=x):
    for _ in range(i):
        u = sp.diff(u, t)
    for _ in range(j):
        u = sp.diff(u, xx)
    return u


def apply(Q, u):
    Q = sp.Poly(sp.expand(Q), tau, xi)
    return sp.expand(sum(cf * der(u, i, j) for (i, j), cf in Q.terms()))


def opx(a, f):
    a = sp.Poly(sp.expand(a), xi)
    return sp.expand(sum(cf * sp.diff(f, x, k) for (k,), cf in a.terms()))


def flow_poly(a, f, T):
    out, term, k = 0, f, 0
    while term != 0:
        out += term
        k += 1
        term = sp.expand(T * opx(a, term) / k)
    return sp.expand(out)


def mons(n):
    return [(i, k - i) for k in range(n + 1) for i in range(k + 1)]


def generic(n):
    ms = mons(n)
    cs = sp.symbols(f'c0:{len(ms)}')
    return sum(cf * tau**i * xi**j for cf, (i, j) in zip(cs, ms)), list(cs), ms


def nullspace_polys(eqs, cs, ms):
    M = sp.Matrix([[sp.diff(e, cf) for cf in cs] for e in eqs])
    return [sp.expand(sum(v[k] * tau**i * xi**j for k, (i, j) in enumerate(ms))) for v in M.nullspace()]


def span_dim(polys, n):
    if not polys:
        return 0
    return sp.Matrix([[sp.Poly(p, tau, xi).coeff_monomial(tau**i * xi**j) for (i, j) in mons(n)] for p in polys]).rank()


def same_span(A, B, n):
    return span_dim(A, n) == span_dim(B, n) == span_dim(A + B, n)


def coeff_eqs_EP(expr):
    expr = sp.expand(sp.powsimp(sp.expand(expr)))
    exps = sorted({a_ for a_ in expr.atoms(sp.exp)}, key=str)
    Es = sp.symbols(f'E0:{len(exps)}')
    return sp.Poly(expr.xreplace(dict(zip(exps, Es))), t, x, *Es).coeffs()


def quot_dim(gens, bound=12):
    G = sp.groebner(gens, tau, xi, order='grevlex')
    if list(G.exprs) == [1]:
        return 0
    LM = [sp.Poly(g, tau, xi).monoms(order='grevlex')[0] for g in G.exprs]
    std = [(i, j) for (i, j) in mons(bound) if not any(i >= a_ and j >= b_ for (a_, b_) in LM)]
    return None if any(i + j == bound for (i, j) in std) else len(std)


def dimRu_EP(u, kmax=9):
    ders = [sp.expand(der(u, i, j)) for (i, j) in mons(kmax)]
    cs = sp.symbols(f'a0:{len(ders)}')
    eqs = coeff_eqs_EP(sum(cf * d for cf, d in zip(cs, ders)))
    return sp.Matrix([[sp.diff(e, cf) for cf in cs] for e in eqs]).rank()


# ---------- algebra di Weyl A_1 = C[x]<d>: operatori come dict {(i,j): coeff} = sum coeff x^i d^j ----------
def wmul(A, B):
    out = {}
    for (a, b), ca in A.items():
        for (cc, d), cb in B.items():
            # d^b x^cc = sum_l C(b,l) cc!/(cc-l)! x^(cc-l) d^(b-l)
            for l in range(0, min(b, cc) + 1):
                coef = ca * cb * sp.binomial(b, l) * sp.factorial(cc) / sp.factorial(cc - l)
                key = (a + cc - l, b - l + d)
                out[key] = sp.expand(out.get(key, 0) + coef)
    return {k: v for k, v in out.items() if v != 0}


def wadd(A, B, s=1):
    out = dict(A)
    for k, v in B.items():
        out[k] = sp.expand(out.get(k, 0) + s * v)
    return {k: v for k, v in out.items() if v != 0}


def wapply(A, f, xx=x):
    return sp.expand(sum(cf * xx**i * sp.diff(f, xx, j) for (i, j), cf in A.items()))


def box(I, J):
    return [(i, j) for i in range(I + 1) for j in range(J + 1)]


Ai, Aip = sp.symbols('Ai Aip')


def ai_coeffs(expr, xx=x):
    e = sp.expand(expr).subs({sp.airyai(xx): Ai, sp.airyaiprime(xx): Aip})
    return sp.Poly(e, xx, Ai, Aip).coeffs()


print('== E4.1 Airy PDE: soluzione fondamentale u = (3t)^(-1/3) Ai(x/(3t)^(1/3)) ==')
P = tau + xi**3
s3 = (3 * t)**sp.Rational(1, 3)
uA = sp.airyai(x / s3) / s3
check('E4.1a P(d)u = u_t + u_xxx = 0', sp.simplify(apply(P, uA)) == 0)
# C3-T1(d) con m = 1: identifica <=> nessun b(d_x) ≠ 0 con b(d_x)u = 0. A t = 1/3: d_x^k u = Ai^(k)(x)
K = 12
gs = sp.symbols(f'g0:{K+1}')
rel = sum(gs[k] * sp.diff(sp.airyai(X), X, k) for k in range(K + 1))
eqs = ai_coeffs(rel, X)
sol = sp.solve(eqs, gs, dict=True)
check(f'E4.1b nessuna relazione sum_(k<={K}) g_k Ai^(k) = 0 non banale (Ai, Ai\' indipendenti su C(x)) => t-getto libero (V-ex fino a K={K})',
      sol == [] or all(v == 0 for v in sol[0].values()) and len(sol[0]) == K + 1, sol)
z1, z2, z3 = [mp.airyaizero(k) for k in (1, 2, 3)]
check('E4.1c (argomento generale) Ai ha infiniti zeri reali (primi tre ~ -2.338, -4.088, -5.521) => Ai\'/Ai non razionale => Ai, Ai\' indipendenti su C(x)',
      abs(z1 + 2.33810741) < 1e-6 and abs(z2 + 4.08794944) < 1e-6 and abs(z3 + 5.52055983) < 1e-6)

print('== E4.2 Airy PDE, dati EP: C3-T3 (jet 2d-1), C3-C2 ==')
p0 = (sp.Integer(0), sp.Integer(0))   # origine: entrate razionali (con esponenziali in punti generici il nullspace esatto è lento)
for name, u in {'x^3-6t': x**3 - 6 * t, 'e^{x-t}+e^{2x-8t}+e^{-x+t}': sp.exp(x - t) + sp.exp(2 * x - 8 * t) + sp.exp(-x + t),
                'x^4-24tx': x**4 - 24 * t * x}.items():
    check(f'E4.2a [{name}] P(d)u = 0', sp.simplify(apply(P, u)) == 0)
    d = dimRu_EP(u)
    Q, cs, ms = generic(d)
    A_d = nullspace_polys(coeff_eqs_EP(apply(Q, u)), cs, ms)
    check(f'E4.2b [{name}] d = {d}; dim R/(Ann_<=d) = d', quot_dim(A_d) == d)
    w = apply(Q, u)
    eqj = [sp.expand(der(w, i, j).subs({t: p0[0], x: p0[1]})) for (i, j) in mons(d - 1)]
    A_j = nullspace_polys(eqj, cs, ms)
    check(f'E4.2c [{name}] jet di ordine 2d-1 = {2*d-1} ricostruisce Ann_<=d', same_span(A_j, A_d, d))
    nm = [q for q in A_d if sp.rem(sp.Poly(q, tau), sp.Poly(P, tau)).as_expr() != 0]
    check(f'E4.2d [{name}] C3-C2: Ann(u) ≠ (P)', len(nm) > 0)

print('== E4.3 KdV lineare u_t = -c u_x - u_xxx (termini a1 = -c xi, a2 = -xi^3): P2-T2 e P1-T2(iv) ==')
c = sp.symbols('c', positive=True)
a1, a2 = -c * xi, -xi**3
a = a1 + a2
PK = tau - a
g = sp.expand((a - a1) * (a - a2))
check('E4.3a g = c xi^4, K = 4', sp.expand(g - c * xi**4) == 0)
Bs = sp.symbols('B0:4', cls=sp.Function)
upol = sum(Bs[k](t) * x**k for k in range(4))
eqs = sp.Poly(sp.expand(apply(PK, upol)), x).coeffs()
sol = sp.dsolve(eqs, [B(t) for B in Bs])
ugen = sp.expand(upol.subs({sl.lhs: sl.rhs for sl in sol}))
consts = sorted(ugen.free_symbols - {t, x, c}, key=str)
basis = [sp.expand(sp.diff(ugen, k)) for k in consts]
target = [sp.Integer(1), x - c * t, sp.expand((x - c * t)**2), sp.expand((x - c * t)**3 - 6 * t)]
allv = basis + target
monsx = sorted({m for v in allv for m in sp.Poly(v, x, t).monoms()})
M = sp.Matrix([[sp.Poly(v, x, t).coeff_monomial(x**i * t**j) for (i, j) in monsx] for v in allv])
check('E4.3b Sol(tau-a, xi^4) = span{1, x-ct, (x-ct)^2, (x-ct)^3-6t} (dim 4): spazio {E_perp = 0} di P2-T2', len(basis) == 4 and M.rank() == 4)
v1 = (x - c * t)**3 + 6 / c * (x - c * t)   # [corretto: segno]
v2 = -6 / c * x
check('E4.3c (x-ct)^3-6t = v1 + v2, v1 ∈ ker(tau+c xi), v2 ∈ ker(tau+xi^3)',
      sp.expand(v1 + v2 - target[3]) == 0 and apply(tau - a1, v1) == 0 and apply(tau - a2, v2) == 0)
f = x**4
E = sp.expand(flow_poly(a, f, t) - f - (flow_poly(a1, f, t) - f) - (flow_poly(a2, f, t) - f))
check('E4.3d P1-T2: u0 = x^4, E^add = (S1-I)(S2-I)x^4 = 24 c t^2', sp.expand(E - 24 * c * t**2) == 0, E)

print('== E4.4 P3-T1(a1): (Par) fallisce per i termini dispersivi del 3° ordine ==')
kap = sp.symbols('kappa', real=True)
for name, sym in {'Airy -xi^3': -xi**3, 'KdV-Burgers lineare D xi^2 - xi^3': sp.Rational(1, 1) * xi**2 - xi**3}.items():
    ReA = sp.simplify(sp.re(sp.expand(sym.subs(xi, sp.I * kap))))
    q = sp.Poly(sym, xi).degree()
    check(f'E4.4 [{name}] q = {q} dispari, Re a(i kappa) = {ReA}: (Par) non vale => P3-T1(a) non si applica con questo A_0',
          q % 2 == 1 and sp.limit(ReA + kap**q, kap, sp.oo) != -sp.oo)

print('== E5.1 Airy EDO: Ann_{A_1}(Ai) e P4-C1 ==')
M_ = {(0, 2): 1, (1, 0): -1}           # d^2 - x
check('E5.1a (d^2 - x) Ai = 0, (d^2 - x) Bi = 0', sp.simplify(wapply(M_, sp.airyai(x))) == 0 and sp.simplify(wapply(M_, sp.airybi(x))) == 0)
B_ = box(3, 4)
cs = sp.symbols(f'k0:{len(B_)}')
Lgen = dict(zip(B_, cs))
eqs = ai_coeffs(wapply(Lgen, sp.airyai(x)))
Mx = sp.Matrix([[sp.diff(e, cf) for cf in cs] for e in eqs])
ns = Mx.nullspace()
# ogni elemento di Ann ∩ box ha resto nullo nella divisione a destra per d^2 - x (monico)


def rdiv_monic(L, Mon, mdeg=2):
    L = dict(L)
    while True:
        top = max((j for (i, j) in L), default=-1)
        if top < mdeg:
            return L
        for (i, j) in [k for k in L if k[1] == top]:
            cf = L[(i, j)]
            L = wadd(L, wmul({(i, j - mdeg): cf}, Mon), -1)


ok = all(rdiv_monic({k: v[n] for n, k in enumerate(B_) if v[n] != 0}, M_) == {} for v in ns)
expected = len(box(2, 2))   # R in box(I-1, J-2) = box(2,2): R(d^2-x) ha x-grado <= 3 e d-grado <= 4
check(f'E5.1b Ann_A1(Ai) ∩ box(3,4) ⊆ A_1(d^2-x) (resto della divisione nullo); dim = {len(ns)} = dim A_1(d^2-x) ∩ box = {expected}',
      ok and len(ns) == expected)
# P4-C1(a): rho_u iniettiva: L agisce come 0 su A_1·Ai solo se L = 0
eqs2 = []
for (k_, l_) in box(3, 3):
    eqs2 += ai_coeffs(wapply(Lgen, x**k_ * sp.diff(sp.airyai(x), x, l_)))
M2 = sp.Matrix([[sp.diff(e, cf) for cf in cs] for e in eqs2])
check('E5.1c P4-C1(a): rho_Ai : A_1 -> End(A_1·Ai) iniettiva su box(3,4) (nucleo 0) mentre Ann ∩ box ≠ 0',
      len(M2.nullspace()) == 0 and len(ns) > 0)
Lsmall = [(0, 0), (0, 1), (0, 2), (1, 0)]
cs2 = sp.symbols('m0:4')
eqs3 = ai_coeffs(wapply(dict(zip(Lsmall, cs2)), sp.airyai(x)))
ns3 = sp.Matrix([[sp.diff(e, cf) for cf in cs2] for e in eqs3]).nullspace()
check('E5.1d 𝓛 = span{1, d, d^2, x}: Ann ∩ 𝓛 = C(d^2 - x) (dim 1): Ai identifica in 𝓛', len(ns3) == 1 and list(ns3[0]) == [0, 0, 1, -1] or (len(ns3) == 1 and ns3[0][2] == -ns3[0][3]))

print('== E5.2 coefficienti variabili in D = A_1[d_t]: P = d_t - d_x^2 + x (monico, m = 1), OP-ALG-T4 ==')
mu = sp.Rational(3, 2)


def Pvar(u):
    return sp.diff(u, t) - sp.diff(u, x, 2) + x * u


u_mu = sp.exp(mu * t) * sp.airyai(x + mu)
check('E5.2a u_mu = e^{mu t} Ai(x+mu): P u_mu = 0', sp.simplify(Pvar(u_mu)) == 0)
check('E5.2b u_mu ∈ 𝒯 (b = d_x^2 - x - mu ∈ A_1 la annulla) => per OP-ALG-T4(d) Ann ≠ D·P: testimone b ∉ D·P (grado 0 in d_t)',
      sp.simplify(sp.diff(u_mu, x, 2) - (x + mu) * u_mu) == 0)
Gs = lambda T, Y: T**sp.Rational(-1, 2) * sp.exp(-Y**2 / (4 * T))
us = sp.exp(-x * t + t**3 / 3) * Gs(t, x - t**2)
check('E5.2c u* = exp(-xt + t^3/3) G(t, x - t^2) (G nucleo del calore): P u* = 0', sp.simplify(Pvar(us)) == 0)
Kb, Db = 4, 4
Bb = box(Db, Kb)
cb = sp.symbols(f'p0:{len(Bb)}')
r = sp.numer(sp.together(sp.simplify(wapply(dict(zip(Bb, cb)), us) / us)))
eqs = sp.Poly(sp.expand(r), t, x).coeffs()
nsb = sp.Matrix([[sp.diff(e, cf) for cf in cb] for e in eqs]).nullspace()
check(f'E5.2d u* ∉ 𝒯: nessun b ∈ A_1 ∩ box({Db},{Kb}) non nullo con b u* = 0 (V-ex; prova generale: coefficiente di t^(-K))',
      len(nsb) == 0)
h1 = sp.simplify(sp.diff(us, x) / us)
check('E5.2e (log u*)_x = -x/(2t) - t/2: il termine dominante in t^-1 rende la prova del punto d generale', sp.simplify(h1 + x / (2 * t) + t / 2) == 0)
Lop = sp.simplify(2 * t * sp.diff(us, x) + (x + t**2) * us)
check('E5.2f OP-ALG-P5 (in A_2 una soluzione olonoma non identifica): L = 2t d_x + x + t^2 ∈ C[t,x]<d_x> annulla u*', Lop == 0)

print('== E5.3 OPR2-T3, esempio (i): P = d_t (d_t - x) in D, fattori non simili, test D_1 = d_t, D_2 = d_t - x ==')


def Pr2(u):
    return sp.diff(sp.diff(u, t) - x * u, t)


u1_ = sp.exp(x * t) + 1
check('E5.3a u = e^{xt} + 1: P u = 0; (d_t - x)u = -x ∈ 𝒯 => non identifica; testimone Q = d_x^2 (d_t - x) ∉ D·P, Q u = 0',
      sp.simplify(Pr2(u1_)) == 0 and sp.simplify(sp.diff(sp.diff(u1_, t) - x * u1_, x, 2)) == 0)
Ee = sp.exp(sp.exp(x))
u2_ = sp.exp(x * t) + Ee
check('E5.3b u = e^{xt} + exp(e^x): P u = 0', sp.simplify(Pr2(u2_)) == 0)
# d_t u = x e^{xt} ∉ 𝒯 (prova: grado in t), (d_t - x)u = -x exp(e^x) ∉ 𝒯 (V-ex: exp(e^x) non D-finita)
cb2 = sp.symbols(f'q0:{len(Bb)}')
r1 = sp.expand(sp.simplify(wapply(dict(zip(Bb, cb2)), x * sp.exp(x * t)) / sp.exp(x * t)))
ns1 = sp.Matrix([[sp.diff(e, cf) for cf in cb2] for e in sp.Poly(r1, t, x).coeffs()]).nullspace()
r2 = sp.expand(sp.simplify(wapply(dict(zip(Bb, cb2)), -x * Ee) / Ee))
ns2 = sp.Matrix([[sp.diff(e, cf) for cf in cb2] for e in sp.Poly(r2, x, sp.exp(x)).coeffs()]).nullspace()
check('E5.3c test di OPR2-T3: D_1 u = x e^{xt} ∉ 𝒯 e D_2 u = -x exp(e^x) ∉ 𝒯 (box(4,4); V-ex) => predetto Ann = D·P',
      len(ns1) == 0 and len(ns2) == 0)
# controllo diretto: t-getto libero su A_1 (OP-ALG-T4(b)) nel box: b1 d_t u + b0 u = 0 => b0 = b1 = 0
B3 = box(3, 3)
cA = sp.symbols(f'r0:{len(B3)}')
cB = sp.symbols(f's0:{len(B3)}')
expr = wapply(dict(zip(B3, cA)), sp.diff(u2_, t)) + wapply(dict(zip(B3, cB)), u2_)
expr = sp.expand(expr)
eA = sp.expand(sp.simplify(expr.coeff(sp.exp(x * t))))
rest = sp.expand(sp.simplify((expr - eA * sp.exp(x * t)) / Ee))
eqs = sp.Poly(eA, t, x).coeffs() + sp.Poly(rest, x, sp.exp(x)).coeffs()
nsT = sp.Matrix([[sp.diff(e, cf) for cf in cA + cB] for e in eqs]).nullspace()
check('E5.3d osservato: nessuna relazione b1 d_t u + b0 u = 0 con b_i ∈ box(3,3) (t-getto libero, OP-ALG-T4(b))', len(nsT) == 0)

nok = sum(1 for _, ok in RES if ok)
print(f'\nTOTALE E4/E5: {nok}/{len(RES)} OK')
