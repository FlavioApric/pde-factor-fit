# -*- coding: utf-8 -*-
"""S-CHECK-2D: red team / controlli per C3-P1, C3-T4, C3-T3, C3-T2(c)(d), C3-T5.
Eseguire: D:\\ProblemaBase\\.venv\\Scripts\\python.exe -I audit_c3_2d.py > audit_c3_2d.out
"""
import sys
import sympy as sp
sys.stdout.reconfigure(encoding='utf-8')

t, x, tau, xi, s = sp.symbols('t x tau xi s')
RESULTS = []


def check(name, cond, info=''):
    ok = bool(cond)
    RESULTS.append((name, ok))
    print(('OK   ' if ok else 'FAIL ') + name + ((' :: ' + str(info)) if info != '' else ''))


def apply_op(Q, u):
    """Q(tau,xi) polinomio -> Q(d_t,d_x) u."""
    Q = sp.Poly(sp.expand(Q), tau, xi)
    out = 0
    for (a, b), c in Q.terms():
        out += c * sp.diff(u, t, a, x, b)
    return sp.expand(out)


def monos(n):
    return [tau**a * xi**b for a in range(n + 1) for b in range(n + 1 - a)]


def ann_le_n(u, n, simp=sp.simplify):
    """base di Ann(u) ∩ R_{<=n} per u EP (calcolo diretto: Q(d)u == 0 identicamente)."""
    M = monos(n)
    cs = sp.symbols('c0:%d' % len(M))
    Q = sum(c * m for c, m in zip(cs, M))
    expr = sp.expand(simp(apply_op(Q, u)))
    # u EP: raccolgo per esponenziali e monomi in t, x
    expr = sp.expand(sp.powsimp(sp.expand(expr)))
    eqs = []
    terms = sp.Add.make_args(expr)
    groups = {}
    for term in terms:
        coeff_part = []
        rest = []
        for f in sp.Mul.make_args(term):
            if f.has(*cs):
                coeff_part.append(f)
            else:
                rest.append(f)
        key = sp.Mul(*rest)
        groups.setdefault(key, 0)
        groups[key] += sp.Mul(*coeff_part)
    # i "key" contengono exp(..)*t^a*x^b*costanti: normalizzo togliendo le costanti numeriche
    norm = {}
    for key, val in groups.items():
        c0, k0 = key.as_coeff_Mul()
        norm.setdefault(k0, 0)
        norm[k0] += c0 * val
    eqs = [sp.expand(v) for v in norm.values()]
    A = sp.Matrix([[sp.diff(e, c) for c in cs] for e in eqs]) if eqs else sp.zeros(1, len(M))
    ns = A.nullspace()
    return [sp.expand(sum(v[i] * M[i] for i in range(len(M)))) for v in ns], M


def jet_matrix(u, n, k, p0):
    """righe: beta con |beta|<=k ; colonne: monomi di R_{<=n}; voce d^beta(Q(d)u)(p0)."""
    M = monos(n)
    rows = []
    for a in range(k + 1):
        for b in range(k + 1 - a):
            row = []
            for m in M:
                v = apply_op(m, u)
                row.append(sp.simplify(sp.diff(v, t, a, x, b).subs({t: p0[0], x: p0[1]})))
            rows.append(row)
    return sp.Matrix(rows), M


print('=== C3-P1 ===')
# P1-a: P = tau - xi^2, u = nucleo del calore in p0 = (1,0), jet di ordine K = 3.
G = sp.exp(-x**2 / (4 * t)) / sp.sqrt(t)
check('P1-a0 G risolve il calore', sp.simplify(sp.diff(G, t) - sp.diff(G, x, 2)) == 0)
K = 3
betas = [(a, b) for a in range(K + 1) for b in range(K + 1 - a)]
jetG = sp.Matrix([sp.simplify(sp.diff(G, t, a, x, b).subs({t: 1, x: 0})) for a, b in betas])
svals = list(range(-3, 4))  # 7 frequenze
cols = []
for sv in svals:
    e = sp.exp(sv**2 * t + sv * x)
    cols.append([sp.diff(e, t, a, x, b).subs({t: 1, x: 0}) for a, b in betas])
A = sp.Matrix(cols).T
cvar = sp.symbols('a0:7')
sol = sp.linsolve((A, jetG), *cvar)
check('P1-a1 esiste v EP in ker(tau-xi^2) (7 modi) con lo stesso 3-jet di G in (1,0)', sol != sp.EmptySet, sol)
check('P1-a2 rango jet delle soluzioni = dim R_<=3 - dim (P)_<=3 = 10-3 = 7', A.rank() == 7, A.rank())

# P1-b: P = (tau - xi^2)^2 (non ridotto), K = 4: jet di e^z e t e^z, z in V(P1)
K = 4
betas = [(a, b) for a in range(K + 1) for b in range(K + 1 - a)]
cols = []
for sv in range(-4, 5):
    e = sp.exp(sv**2 * t + sv * x)
    for f in (e, t * e):
        cols.append([sp.diff(f, t, a, x, b).subs({t: 0, x: 0}) for a, b in betas])
A = sp.Matrix(cols).T
P1 = tau - xi**2
check('P1-b0 t*e^{z} risolve (tau-xi^2)^2 ma non tau-xi^2',
      apply_op(sp.expand(P1**2), t * sp.exp(4 * t + 2 * x)) == 0 and apply_op(P1, t * sp.exp(4 * t + 2 * x)) != 0)
check('P1-b1 rango jet EP = 15 - dim (P)_<=4 = 15 - 1 = 14 (= jet di tutte le soluzioni)', A.rank() == 14, A.rank())

# P1-c: lemma elementare "Q uccide ogni EP-soluzione => P | Q": testimone s^{e-1}e^z con s = <eta,y>
# P = (tau-xi^2)^2, Q = (tau-xi^2)*(tau+1): z = (4,2) liscio, Q'(z) = 5 != 0, eta = (0,1), s = x
v = x * sp.exp(4 * t + 2 * x)
check('P1-c x e^{z} risolve P=(tau-xi^2)^2', apply_op(sp.expand(P1**2), v) == 0)
check('P1-c Q=(tau-xi^2)(tau+1) non la uccide (quindi Q notin Ann(E))', apply_op(sp.expand(P1 * (tau + 1)), v) != 0)

# P1-d: dominio a U, P = tau: ogni v con Ann(v) contenente strettamente (tau) e' funzione di x sola,
# quindi l(v) = v(2.5,2.5) - v(0.5,2.5) = 0; la funzione phi(x)*1_{t>2} da' l = 1. [STRUTTURALE]
h = sp.Function('h')
vv = h(x)
check('P1-d [STRUTTURALE] l(v)=0 per v=v(x) (soluzioni EP di d_t su Omega connesso)',
      sp.simplify(vv.subs({t: sp.Rational(5, 2), x: sp.Rational(5, 2)}) - vv.subs({t: sp.Rational(1, 2), x: sp.Rational(5, 2)})) == 0)

print('=== C3-T4 ===')


def evol_set(u, n):
    """dimensione affine di {b in C[xi]_{<=n} : (d_t - b(d_x)) u = 0} (-1 se vuoto)."""
    bs = sp.symbols('b0:%d' % (n + 1))
    expr = sp.diff(u, t) - sum(bs[j] * sp.diff(u, x, j) for j in range(n + 1))
    expr = sp.expand(expr)
    # coefficienti rispetto a t, x, exp
    groups = {}
    for term in sp.Add.make_args(sp.expand(expr)):
        cp = [f_ for f_ in sp.Mul.make_args(term) if f_.has(*bs)]
        rp = [f_ for f_ in sp.Mul.make_args(term) if not f_.has(*bs)]
        c0, k0 = sp.Mul(*rp).as_coeff_Mul()
        groups[k0] = groups.get(k0, 0) + c0 * sp.Mul(*cp)
    eqs = [sp.expand(v_) for v_ in groups.values()]
    sol = sp.linsolve(eqs, *bs)
    if sol == sp.EmptySet:
        return -1, sol
    (vec,) = list(sol)
    free = set().union(*[sp.sympify(c).free_symbols for c in vec]) & set(bs)
    return len(free), sol


u_heat = x**2 + 2 * t + sp.exp(t + x)
check('T4-0 u = x^2+2t+e^{t+x} risolve il calore', sp.simplify(sp.diff(u_heat, t) - sp.diff(u_heat, x, 2)) == 0)
D = 4
for n in range(2, 7):
    dim, sol = evol_set(u_heat, n)
    check('T4-1 calore, n=%d: dim affine = max(0, n+1-D) = %d' % (n, max(0, n + 1 - D)), dim == max(0, n + 1 - D), (dim, sol))
# advezione-diffusione a = xi^2 + 2 xi: modo (1+..) con q = x + 4t (delta=1), modo semplice in xi=-1
a = xi**2 + 2 * xi
u_ad = (x + 4 * t) * sp.exp(3 * t + x) + sp.exp(-t - x)
check('T4-2 u_ad risolve u_t = u_xx + 2u_x', sp.simplify(sp.diff(u_ad, t) - sp.diff(u_ad, x, 2) - 2 * sp.diff(u_ad, x)) == 0)
D = 3
for n in range(2, 6):
    dim, sol = evol_set(u_ad, n)
    check('T4-3 AD, n=%d: dim affine = max(0,n+1-D) = %d' % (n, max(0, n + 1 - D)), dim == max(0, n + 1 - D), (dim, sol))
# formula esplicita: n = 4 -> b = a + (xi-1)^2 (xi+1) * (c0 + c1 xi)
dim, sol = evol_set(u_ad, 4)
(vec,) = list(sol)
bpoly = sum(vec[j] * xi**j for j in range(5))
rem = sp.rem(sp.expand(bpoly - a), sp.expand((xi - 1)**2 * (xi + 1)), xi)
check('T4-4 b - a divisibile per prod (xi-xi_k)^{delta_k+1}', sp.simplify(rem) == 0, sp.factor(bpoly - a))

print('=== C3-T3 ===')
u3 = (1 + t) * sp.exp(t - x) + x
# d = dim R.u : spazio generato dalle derivate
gens = [sp.expand(sp.diff(u3, t, a, x, b), power_exp=False) for a in range(5) for b in range(5 - a)]
basis_funcs = [sp.exp(t - x), t * sp.exp(t - x), x, sp.Integer(1)]
cm = sp.Matrix([[sp.Poly(g.subs(sp.exp(t - x), s), t, x, s).coeff_monomial(m) for m in (s, t * s, x, 1)] for g in gens])
d = cm.rank()
check('T3-0 d = dim R.u = 4 per u=(1+t)e^{t-x}+x', d == 4, d)
p0 = (sp.Rational(1, 3), sp.Rational(-1, 2))
for n in range(1, 5):
    ann, M = ann_le_n(u3, n)
    Jd, _ = jet_matrix(u3, n, d - 1, p0)
    Jdm, _ = jet_matrix(u3, n, d - 2, p0)
    nd = len(Jd.nullspace())
    ndm = len(Jdm.nullspace())
    check('T3-1 (i) n=%d: dim Ann_<=n = dim ker(jet |beta|<=d-1)' % n, len(ann) == nd, (len(ann), nd, ndm))
    if n == 4:
        print('INFO T3-1b n=d=4, p0=(1/3,-1/2): dim ker con |beta|<=d-1 e con |beta|<=d-2 =', (nd, ndm), '(qui la soglia d-1 non e\' raggiunta: (iii) e\' un\'ottimalita\' nel caso peggiore, vedi T3-6..9)')
# (ii) generatori di grado <= d e base di Groebner
annd, _ = ann_le_n(u3, d)
Gb = sp.groebner(annd, tau, xi, order='grevlex')
degs = [sp.Poly(g, tau, xi).total_degree() for g in Gb.exprs]
check('T3-2 (ii) base di Groebner ridotta di (Ann_<=d): gradi <= d', max(degs) <= d, degs)
ann_more, _ = ann_le_n(u3, d + 2)
red_ok = all(Gb.reduce(q)[1] == 0 for q in ann_more)
check('T3-3 (ii) Ann_<=d+2 contenuto in (Ann_<=d)', red_ok)
# monomi standard = d
LM = [sp.Poly(g, tau, xi).monoms(order='grevlex')[0] for g in Gb.exprs]
std = [(a, b) for a in range(d + 1) for b in range(d + 1) if not any(a >= m[0] and b >= m[1] for m in LM)]
check('T3-4 (ii) #monomi standard = d', len(std) == d, std)
# il grado d e' raggiunto (generatore di grado d necessario) nell'esempio 1D
u1 = sum(sp.exp(j * x) for j in (1, 2, 3))
ann1, _ = ann_le_n(u1, 3)
G1 = sp.groebner(ann1, tau, xi, order='grevlex')
check('T3-5 u=e^x+e^{2x}+e^{3x}: Ann=(tau, (xi-1)(xi-2)(xi-3)), grado max = d = 3',
      max(sp.Poly(g, tau, xi).total_degree() for g in G1.exprs) == 3, G1.exprs)

# (iii) ottimalita' forte, d = 3: u' con lo stesso jet di ordine 2d-2 = 4 in 0 e Ann diverso
dd = 3
m = [sum(sp.Integer(j)**k for j in range(1, dd + 1)) for k in range(2 * dd + 2)]
H = sp.Matrix(dd - 1, dd + 1, lambda i, j: m[i + j])
ker = H.nullspace()
check('T3-6 (iii) Hankel (d-1)x(d+1): nucleo di dim 2 (> 1 = dim Ann_<=d in C[xi])', len(ker) == 2)
# scelgo Q' nel nucleo con Q'(0) = 0 (radice prescritta zeta = 0)
al, be = sp.symbols('al be')
qv = al * ker[0] + be * ker[1]
sol = sp.solve([qv[0]], [al], dict=True)[0]
qv = sp.simplify(qv.subs(sol).subs(be, 1))
Qp = sp.expand(sum(qv[i] * xi**i for i in range(dd + 1)))
roots = sp.roots(sp.Poly(Qp, xi))
rts = []
for r_, mult in roots.items():
    rts += [r_] * mult
check('T3-7 (iii) Q\' di grado d con radici distinte, non proporzionale a (xi-1)(xi-2)(xi-3)',
      sp.Poly(Qp, xi).degree() == dd and len(set(rts)) == dd and sp.rem(Qp, (xi - 1) * (xi - 2) * (xi - 3), xi) != 0, (sp.factor(Qp), rts))
V = sp.Matrix(dd, dd, lambda k, j: rts[j]**k)
w = V.LUsolve(sp.Matrix(m[:dd]))
mp = [sp.simplify(sum(w[j] * rts[j]**k for j in range(dd))) for k in range(2 * dd + 1)]
check('T3-8 (iii) u\'=sum w_j e^{mu_j x}: momenti (= derivate in 0) uguali fino all\'ordine 2d-2',
      all(sp.simplify(mp[k] - m[k]) == 0 for k in range(2 * dd - 1)), [sp.nsimplify(sp.simplify(mp[k] - m[k])) for k in range(2 * dd + 1)])
check('T3-9 (iii) ... e diversi all\'ordine 2d-1 (Ann(u\') != Ann(u))', sp.simplify(mp[2 * dd - 1] - m[2 * dd - 1]) != 0)

print('=== C3-T2 (c),(d) ===')
P = tau - xi**2


def simple_modes(Z):
    return sum(sp.exp(z[0] * t + z[1] * x) for z in Z)


def ann_simple(Z, n):
    """Ann(u) ∩ R_<=n per modi semplici = {Q : Q(z)=0 per z in Z} (C3-T2(a))."""
    M = monos(n)
    A = sp.Matrix([[mm.subs({tau: z[0], xi: z[1]}) for mm in M] for z in Z])
    return [sp.expand(sum(v[i] * M[i] for i in range(len(M)))) for v in A.nullspace()]


for n in range(2, 5):
    Z = [(j**2, j) for j in range(-n, n + 1)]  # 2n+1 > n*deg P
    ann = ann_simple(Z, n)
    okdiv = all(sp.rem(q, P, tau) == 0 for q in ann)
    check('T2-c parabola n=%d, |Z|=2n+1: Ann_<=n = P*R_<=n-2 (dim %d)' % (n, sp.binomial(n, 2)),
          len(ann) == sp.binomial(n, 2) and okdiv, (len(ann), okdiv))
# controllo diretto su u (non solo via (a)) per n = 2
Z = [(j**2, j) for j in range(-2, 3)]
annu, _ = ann_le_n(simple_modes(Z), 2)
check('T2-c0 coerenza con (a): Ann_<=2 calcolato su u = Ann_<=2 via Q|_Z = 0', len(annu) == len(ann_simple(Z, 2)))
for n in range(1, 5):
    Zn = [(j**2, sg * j) for j in range(1, n + 1) for sg in (1, -1)]
    Qn = sp.prod([tau - j**2 for j in range(1, n + 1)])
    check('T2-d n=%d: |Z_n| = 2n, Q_n in Ann(u), P non divide Q_n' % n,
          len(set(Zn)) == 2 * n and apply_op(sp.expand(Qn), simple_modes(Zn)) == 0 and sp.rem(sp.expand(Qn), P, tau) != 0)
# due fattori: P = (tau - xi^2)(tau + xi + 1), n = 3: >6 punti sulla parabola, >3 sulla retta
P2 = sp.expand((tau - xi**2) * (tau + xi + 1))
Z = [(j**2, j) for j in range(-3, 4)] + [(-j - 1, j) for j in (5, 6, 7, 8)]
ann = ann_simple(Z, 3)
check('T2-c2 due fattori n=3: Ann_<=3 = C*P', len(ann) == 1 and sp.simplify(sp.cancel(ann[0] / P2)).is_number, ann)
# con soli 3 punti sulla retta (= n*deg P_2): la soglia non e' soddisfatta; si vede se il risultato cade
Z3 = [(j**2, j) for j in range(-3, 4)] + [(-j - 1, j) for j in (5, 6, 7)]
ann3 = ann_simple(Z3, 3)
print('INFO T2-c3 soli 3 punti sulla retta (soglia non soddisfatta): dim Ann_<=3 =', len(ann3), '(la soglia e\' sufficiente, non sempre necessaria)')
# Bezout affine: Q coprimo con P_i => #V(Q) ∩ V(P_i) <= deg Q deg P_i ; esempio estremale
Qx = sp.prod([tau - j**2 for j in range(1, 4)])
sols = sp.solve([Qx, P], [tau, xi], dict=True)
check('T2-c4 Bezout raggiunto: #V(Q_3) ∩ V(tau-xi^2) = 6 = 3*2', len(sols) == 6)

print('=== C3-T5 ===')
c = sp.symbols('c', real=True, nonzero=True)
f, g = sp.Function('f'), sp.Function('g')
uw = f(x - c * t) + g(x + c * t)
check('T5-a0 onda: P(d)u = 0', sp.simplify(sp.diff(uw, t, 2) - c**2 * sp.diff(uw, x, 2)) == 0)
w_plus = sp.simplify(sp.diff(uw, t) + c * sp.diff(uw, x))
w_minus = sp.simplify(sp.diff(uw, t) - c * sp.diff(uw, x))
check('T5-a1 (d_t + c d_x)u = 2c g\'(x+ct)  [= (P/P_1)u con P_1 = tau - c xi]',
      sp.simplify(w_plus - 2 * c * sp.diff(g(x + c * t), x)) == 0)
check('T5-a2 (d_t - c d_x)u = -2c f\'(x-ct) [= (P/P_2)u con P_2 = tau + c xi]',
      sp.simplify(w_minus + 2 * c * sp.diff(f(x - c * t), x)) == 0)
# testimone per g EP: u = f(x-ct) + e^{x+ct}: Q = (xi - 1)(tau + c xi) in Ann, P non divide Q
ug = f(x - c * t) + sp.exp(x + c * t)
Qw = sp.expand((xi - 1) * (tau + c * xi))
check('T5-a3 g = e^s: Q = (xi-1)(tau+c xi) uccide u (Ann != (P))', sp.simplify(apply_op(Qw, ug)) == 0)
check('T5-a3b P = tau^2 - c^2 xi^2 non divide Q', sp.rem(Qw, tau**2 - c**2 * xi**2, tau) != 0)
# EP globale: E con (d_t + c d_x)E = 0 => E(t,x) = E(0, x - ct)
E = (x - c * t)**2 * sp.exp(3 * (x - c * t)) + sp.cos(x - c * t)
check('T5-a4 E EP con (d_t+c d_x)E=0 => E(t,x) = E(0,x-ct)',
      sp.simplify(sp.diff(E, t) + c * sp.diff(E, x)) == 0 and sp.simplify(E - E.subs(t, 0).subs(x, x - c * t)) == 0)
# primitive di EP sono EP
q = s**2 * sp.exp(3 * s) + s + sp.exp(-s)
Fq = sp.integrate(q, s)
check('T5-a5 primitiva di un EP e\' EP (esempio)', sp.simplify(sp.diff(Fq, s) - q) == 0 and not Fq.has(sp.Integral), Fq)
# coniche: determinante della matrice orlata
mu, al_, cc = sp.symbols('mu alpha c_t', nonzero=True)


def bordered(Pq):
    Pp = sp.Poly(Pq, tau, xi)
    A_ = Pp.coeff_monomial(tau**2); B_ = Pp.coeff_monomial(tau * xi); C_ = Pp.coeff_monomial(xi**2)
    D_ = Pp.coeff_monomial(tau); E_ = Pp.coeff_monomial(xi); F_ = Pp.coeff_monomial(1)
    return sp.Matrix([[A_, B_ / 2, D_ / 2], [B_ / 2, C_, E_ / 2], [D_ / 2, E_ / 2, F_]]).det()


dKG = sp.simplify(bordered(tau**2 - xi**2 + mu**2))
dTel = sp.simplify(bordered(tau**2 + al_ * tau - cc**2 * xi**2))
check('T5-b1 KG: det orlato = -mu^2', sp.simplify(dKG + mu**2) == 0, dKG)
check('T5-b2 telegrafo: det orlato = c^2 alpha^2/4', sp.simplify(dTel - cc**2 * al_**2 / 4) == 0, dTel)
check('T5-b3 KG mu=1 irriducibile su Q(i)', len(sp.factor_list(tau**2 - xi**2 + 1, tau, xi, extension=sp.I)[1]) == 1)
check('T5-b4 telegrafo alpha=1,c=2 irriducibile su Q(i)', len(sp.factor_list(tau**2 + tau - 4 * xi**2, tau, xi, extension=sp.I)[1]) == 1)
check('T5-b5 controprova: alpha=0 (onda) e\' riducibile, det = 0',
      len(sp.factor_list(tau**2 - 4 * xi**2, tau, xi)[1]) == 2 and bordered(tau**2 - 4 * xi**2) == 0)
check('T5-c1 trave: tau^2 + xi^4 = (tau - i xi^2)(tau + i xi^2)', sp.expand((tau - sp.I * xi**2) * (tau + sp.I * xi**2) - tau**2 - xi**4) == 0)
uu = sp.Function('U')(t, x)
check('T5-c2 trave: (d_t + i d_x^2)(d_t - i d_x^2)U = U_tt + U_xxxx (U generica)', sp.simplify(sp.diff(sp.diff(uu, t) - sp.I * sp.diff(uu, x, 2), t) + sp.I * sp.diff(sp.diff(uu, t) - sp.I * sp.diff(uu, x, 2), x, 2) - sp.diff(uu, t, 2) - sp.diff(uu, x, 4)) == 0)
# testimone trave: u = e^{i t + x}? P(z)=0 per z=(i,1): (i)^2 + 1 = 0 -> EP => non identifica
ub = sp.exp(sp.I * t + x)
check('T5-c3 trave: e^{it+x} in ker P (EP, quindi Ann != (P))', sp.simplify(apply_op(tau**2 + xi**4, ub)) == 0)

print()
nfail = sum(1 for _, ok in RESULTS if not ok)
print('TOTALE: %d controlli, %d FAIL' % (len(RESULTS), nfail))
print('ESITO GLOBALE: ' + ('OK' if nfail == 0 else 'FAIL'))
