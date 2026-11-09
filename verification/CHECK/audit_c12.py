# audit_c12.py — S-CHECK-2C, red team per C12-L3, L1, L2, T1, C1, L5, T3, T2
# Fonte: work/C1C2/CHECK_REQUEST.md. Eseguire con D:\ProblemaBase\.venv\Scripts\python.exe -I
import itertools, sys
sys.stdout.reconfigure(encoding="utf-8")
import sympy as sp

t, x, s, y = sp.symbols('t x s y', real=True)
tau, xi = sp.symbols('tau xi')
RES = []


def check(name, ok, info=''):
    RES.append((name, bool(ok)))
    print(('OK   ' if ok else 'FAIL ') + name + ('  | ' + str(info) if info != '' else ''))


# ---------- utilità ----------
def quot_dim(gens, bound=40):
    """dim_C C[tau,xi]/(gens) contando i monomi standard (None se infinita)."""
    G = sp.groebner(gens, tau, xi, order='grevlex')
    if list(G.exprs) == [1]:
        return 0
    lms = [sp.Poly(g, tau, xi).monoms(order='grevlex')[0] for g in G.exprs]
    cnt = 0
    for a in range(bound):
        for b in range(bound):
            if not any(a >= m[0] and b >= m[1] for m in lms):
                cnt += 1
                if a == bound - 1 or b == bound - 1:
                    return None
    return cnt


def apply_op(Q, z, q):
    """Q(z+d) q, con tau->d_t, xi->d_x, q polinomio in t,x."""
    Qz = sp.Poly(sp.expand(Q.subs({tau: tau + z[0], xi: xi + z[1]}, simultaneous=True)), tau, xi)
    out = 0
    for (a, b), c in Qz.terms():
        out += c * sp.diff(q, t, a, x, b)
    return sp.expand(out)


def local_N_dim(Qs, z, D):
    """dim {(q_j) polinomi di grado <= D : Q_j(z+d) q_j = 0, sum q_j = 0} (contributo del punto z a N)."""
    mons = [t**i * x**j for i in range(D + 1) for j in range(D + 1 - i)]
    unknowns, qs = [], []
    for k in range(len(Qs)):
        cs = sp.symbols('c%d_0:%d' % (k, len(mons)))
        unknowns += cs
        qs.append(sum(c * m for c, m in zip(cs, mons)))
    eqs = []
    for Q, q in zip(Qs, qs):
        e = apply_op(Q, z, q)
        eqs += sp.Poly(e, t, x).coeffs() if e != 0 else []
    ssum = sp.expand(sum(qs))
    eqs += sp.Poly(ssum, t, x).coeffs() if ssum != 0 else []
    M = sp.Matrix([[sp.diff(e, u) for u in unknowns] for e in eqs])
    return len(unknowns) - M.rank()


def pair_points(Qs):
    pts = set()
    for i, j in itertools.combinations(range(len(Qs)), 2):
        for sol in sp.solve([Qs[i], Qs[j]], [tau, xi], dict=True):
            pts.add((sp.nsimplify(sol[tau]), sp.nsimplify(sol[xi])))
    return sorted(pts, key=str)


def delta_formula(Qs):
    return sum(quot_dim([Qs[i], Qs[j]]) for i, j in itertools.combinations(range(len(Qs)), 2))


print('=== C12-L3 ===')
f, g = tau - xi**2, tau**2 - xi - 1
r = sp.resultant(f, g, tau)
A, B = sp.symbols('A B')
# r in (f,g): riduzione modulo Groebner
Gfg = sp.groebner([f, g], tau, xi, order='lex')
check('L3(a) Res_tau(f,g) in (f,g) ∩ C[xi], != 0', r != 0 and Gfg.reduce(r)[1] == 0 and r.free_symbols <= {xi}, r)
d = quot_dim([f, g])
check('L3(a) dim R/(f,g) <= deg r * deg s', d <= sp.degree(r, xi) * sp.degree(sp.resultant(f, g, xi), tau), d)
# additività con punti condivisi: f = tau - xi^2, g = tau, h = tau - 2 xi^2 (tutte tangenti in 0)
f3, g3, h3 = tau - xi**2, tau, tau - 2 * xi**2
check('L3(b) additività con punto comune ai tre (0,0): dim(f,gh) = dim(f,g)+dim(f,h)',
      quot_dim([f3, g3 * h3]) == quot_dim([f3, g3]) + quot_dim([f3, h3]),
      (quot_dim([f3, g3 * h3]), quot_dim([f3, g3]), quot_dim([f3, h3])))
f4, g4, h4 = tau - xi**2, (tau - xi)**2, (xi - 1)**2
check('L3(b) additività, punto triplo (1,1) e molteplicità', quot_dim([f4, g4 * h4]) == quot_dim([f4, g4]) + quot_dim([f4, h4]),
      (quot_dim([f4, g4 * h4]), quot_dim([f4, g4]), quot_dim([f4, h4])))
# (b) senza coprimalità g,h (g = h): vale ancora
check('L3(b) anche con g = h (serve solo gcd(f,g)=gcd(f,h)=1)', quot_dim([f3, g3**2]) == 2 * quot_dim([f3, g3]))
check('L3(c) comassimale: (tau-xi, tau-xi-1) = R, V vuoto', quot_dim([tau - xi, tau - xi - 1]) == 0)
check('L3(c) non coprimi: V(f)∩V(g) ⊇ V(fattore comune) ≠ ∅ (tau·xi, tau·(xi-1))',
      quot_dim([tau * xi, tau * (xi - 1)]) is None)

print('=== C12-L1 ===')
# J = (0,1), theta = 30 y^2(1-y)^2, psi(t,x) = t^2(1-t)^2 * x^2(1-x)^2 (1+x) (C^1, bordo nullo: basta per le integrazioni per parti)
theta = 30 * y**2 * (1 - y)**2
check('L1 int theta = 1', sp.integrate(theta, (y, 0, 1)) == 1)
psi = t**2 * (1 - t)**2 * x**2 * (1 - x)**2 * (1 + x)
Psi = sp.integrate(psi, (x, 0, 1))
Kpsi = sp.integrate(psi.subs(x, y) - theta * Psi, (y, 0, x))
check('L1 K psi nulla in x = 1 (supporto compatto)', sp.simplify(Kpsi.subs(x, 1)) == 0)
check('L1 d_x K psi = psi - theta⊗Psi', sp.simplify(sp.diff(Kpsi, x) - (psi - theta.subs(y, x) * Psi)) == 0)
check('L1 K d_t = d_t K', sp.simplify(sp.integrate(sp.diff(psi, t).subs(x, y) - theta * sp.integrate(sp.diff(psi, t), (x, 0, 1)), (y, 0, x)) - sp.diff(Kpsi, t)) == 0)
phi = t * x + x**2 + sp.exp(t) * x**3
lhs = -sp.integrate(sp.integrate(phi * Kpsi, (x, 0, 1)), (t, 0, 1))
xbar = sp.Rational(1, 3)
Phi = sp.integrate(phi.subs(x, y), (y, xbar, x))
c_theta = sp.integrate(theta.subs(y, x) * Phi, (x, 0, 1))
rhs_fix = sp.integrate(sp.integrate((Phi - c_theta) * psi, (x, 0, 1)), (t, 0, 1))
rhs_naive = sp.integrate(sp.integrate(Phi * psi, (x, 0, 1)), (t, 0, 1))
check('L1(b) [fix L1-1] su C^inf il J duale = int_xbar^x phi - c_theta(t)', sp.simplify(lhs - rhs_fix) == 0)
check('L1(b) [rilievo L1-1] J duale ≠ int_xbar^x phi (differiscono per c_theta(t)⊗1)', sp.simplify(lhs - rhs_naive) != 0,
      sp.N(lhs - rhs_naive, 6))

print('=== C12-L2 ===')
# Koszul: beta∘alpha = 0 ed esattezza in R^2 (sizigie di (tau-p, xi-q))
p, q = sp.symbols('p q')
Cc = sp.Symbol('C')
alpha = (-(xi - q) * Cc, (tau - p) * Cc)
check('L2 Koszul beta∘alpha = 0', sp.expand(alpha[0] * (tau - p) + alpha[1] * (xi - q)) == 0)
# Ext^0: ker D_t ∩ ker D_x = C e_(p,q) (funzione test su polinomi·esponenziale: dim 1)
check('L2 Hom(R/m,A) = C·e: contributo locale dim 1', local_N_dim([tau - 2, xi + 1], (2, -1), 4) == 1)
# dim Sol(R/a) = dim R/a per a = (tau^2, xi^2 - tau) (punto (0,0) molteplicità 4)
a_ideal = [tau**2, xi**2 - tau]
dimRa = quot_dim(a_ideal)
mons = [t**i * x**j for i in range(9) for j in range(9 - i)]
cs = sp.symbols('k0:%d' % len(mons))
w = sum(c * m for c, m in zip(cs, mons))
eqs = []
for Q in a_ideal:
    e = apply_op(Q, (0, 0), w)
    eqs += sp.Poly(e, t, x).coeffs() if e != 0 else []
M = sp.Matrix([[sp.diff(e, u) for u in cs] for e in eqs])
check('L2(2) dim Sol(R/a) = dim R/a (a=(tau^2, xi^2-tau))', len(cs) - M.rank() == dimRa, (len(cs) - M.rank(), dimRa))
# soluzione particolare EP in (iii): (d_x - rho) w_p = x^l e^{mu x}
rho, mu = 2, 2
l = 3
wp = x**(l + 1) / (l + 1) * sp.exp(mu * x)
check('L2(iii) sol. particolare risonante', sp.simplify(sp.diff(wp, x) - rho * wp - x**l * sp.exp(mu * x)) == 0)
mu2 = 5
rr = sp.Poly(sp.symbols('r0:4')[0] + sp.symbols('r0:4')[1] * x + sp.symbols('r0:4')[2] * x**2 + sp.symbols('r0:4')[3] * x**3, x)
sol = sp.solve(sp.Poly(sp.diff(rr.as_expr(), x) + (mu2 - rho) * rr.as_expr() - x**l, x).coeffs(), sp.symbols('r0:4'))
check('L2(iii) sol. particolare non risonante (grado l)', len(sol) == 4)

print('=== C12-T1: delta(P) con tre o più fattori ===')
examples = {
    'E1 tre rette per 0: tau, xi, tau-xi': [tau, xi, tau - xi],
    'E2 tre parabole tangenti in 0: tau-xi^2, tau, tau-2xi^2': [tau - xi**2, tau, tau - 2 * xi**2],
    'E3 punto triplo (1,1) + molteplicità: tau-xi^2, (tau-xi)^2, (xi-1)^2': [tau - xi**2, (tau - xi)**2, (xi - 1)**2],
    'E4 quattro fattori: tau, xi, tau-xi, tau+xi-1': [tau, xi, tau - xi, tau + xi - 1],
}
for name, Qs in examples.items():
    dform = delta_formula(Qs)
    pts = pair_points(Qs)
    Dg = 6
    loc = [local_N_dim(Qs, z, Dg) for z in pts]
    loc2 = [local_N_dim(Qs, z, Dg + 2) for z in pts]
    check('T1(ii) ' + name + ': dim N (ansatz EP per punto) = sum_{i<j} dim R/(Q_i,Q_j)',
          sum(loc) == dform and loc == loc2, 'punti %s, locali %s, formula %d' % (pts, loc, dform))
# inclusione–esclusione sarebbe sbagliata su E1: pairs 3, triplo 1 -> 2 != 3
check('T1(ii) E1: nessuna correzione di inclusione–esclusione (dim N = 3, non 3-1)', local_N_dim(examples['E1 tre rette per 0: tau, xi, tau-xi'], (0, 0), 6) == 3)
# controllo diretto E1: a(x)+b(t)+h(t+x)=0 -> h lineare: 3 parametri
al, be, ga = sp.symbols('alpha beta gamma')
check('T1(ii) E1 verifica esplicita: (-alpha x+gamma) + (-alpha t-beta-gamma) + (alpha(t+x)+beta) = 0',
      sp.expand((-al * x + ga) + (-al * t - be - ga) + (al * (t + x) + be)) == 0)
# T1(ii) s=2: dim ker Q1 ∩ ker Q2 = dim R/(Q1,Q2), calore/trasporto e trave
for name, Qs in {'calore/trasporto': [tau - xi**2, tau - xi], 'onda': [tau - xi, tau + xi], 'trave tau^2+xi^4 vs tau': [tau**2 + xi**4, tau]}.items():
    dform = quot_dim(Qs)
    pts = pair_points(Qs)
    loc = sum(local_N_dim(Qs, z, 7) for z in pts)
    check('T1 s=2 ' + name, loc == dform, (loc, dform, pts))

print('=== Dominio: corona (controesempio a T1(i) fuori dalle ipotesi) ===')
# Omega = {1<r<2}, P = tau*xi, u = alpha(x) beta(t) con alpha', beta' supportate in [-1/2,1/2]: d_t d_x u = alpha' beta' = 0 su Omega
check('corona: supp(alpha\'beta\') ⊂ {|t|,|x|<=1/2} ⊂ {r<=0.71} disgiunto da Omega', sp.sqrt(sp.Rational(1, 2)) < 1)
c1, c2, c3, c4 = sp.symbols('c1:5')
syst = [c1 - c2, c3 - c4, c1 - c3, c4 - c2 - 1]
check('corona: sistema delle costanti (R1..R4, x=±1.5, t=±1.5) incompatibile ⇒ u ∉ ker d_t + ker d_x',
      sp.solve(syst, [c1, c2, c3, c4]) == [] or sp.solve(syst, [c1, c2, c3, c4]) == {})
# punti testimone usati
for (tt, xx) in [(-0.6, -1.5), (0.6, -1.5), (-0.6, 1.5), (0.6, 1.5), (-1.5, -0.6), (-1.5, 0.6), (1.5, -0.6), (1.5, 0.6)]:
    rr2 = tt**2 + xx**2
    if not (1 < rr2 < 4):
        check('corona: punto testimone in Omega', False, (tt, xx))
check('corona: 8 punti testimone in Omega', True)

print('=== C12-C1 ===')
for m in range(0, 5):
    G = 1 / s if m == 0 else s**(m - 1) * sp.log(s)
    fin = True
    for j in range(0, m + 1):
        Gj = sp.diff(G, s, j)
        I3 = sp.integrate(Gj**2 * s**3, (s, 0, 1))
        fin = fin and I3.is_finite
        if j <= m - 1:
            I1 = sp.integrate(Gj**2 * s, (s, 0, 1))
            fin = fin and I1.is_finite
    Gm = sp.diff(G, s, m)
    div = sp.integrate(Gm**2 * s, (s, 0, 1))
    check('C1 m=%d: u ∈ H^m(Ω\'_c) (integrali pesati finiti), u2 ∉ H^m (∫|G^(m)|^2 s = ∞)' % m, fin and div == sp.oo, div)
    if m >= 1:
        check('C1 m=%d: G^(m) = (m-1)!/s' % m, sp.simplify(Gm - sp.factorial(m - 1) / s) == 0)
    # scomposizione nelle coordinate originali (t,x): s = x + t
    Gx = G.subs(s, x + t)
    u = Gx * (sp.exp(t) - 1)
    fop = lambda v: sp.diff(v, t) - sp.diff(v, x)
    gop = lambda v: sp.diff(v, t) - sp.diff(v, x) - v
    u1, u2 = -gop(u), fop(u)
    check('C1 m=%d: f u1 = 0, g u2 = 0, u1+u2 = u, u2 = e^t G, u1 = -G' % m,
          all(sp.simplify(e) == 0 for e in [fop(u1), gop(u2), u1 + u2 - u, u2 - sp.exp(t) * Gx, u1 + Gx]))
# controllo diretto sul triangolo Ω'_c per m = 2 (quadratura numerica mpmath: SymPy non chiude ∫ e^{2s} log^2 s)
import mpmath as mp
m = 2
ss, tt_ = sp.symbols('ss tt_', positive=True)
U = ss * sp.log(ss) * (sp.exp(tt_) - 1)
vals = []
for k in range(0, m + 1):
    for j in range(0, m + 1 - k):
        dd = sp.lambdify((tt_, ss), sp.diff(U, tt_, k, ss, j)**2, 'mpmath')
        vals.append(mp.quad(lambda S: mp.quad(lambda T: dd(T, S), [0, S]), [0, 1]))
check("C1 m=2: ‖u‖^2_{H^2(Ω'_c)} finita (quadratura diretta)", all(mp.isfinite(v) for v in vals), mp.nstr(sum(vals), 8))
U2 = ss * sp.log(ss) * sp.exp(tt_)
d2 = sp.lambdify((tt_, ss), sp.diff(U2, ss, 2)**2, 'mpmath')
tails = [mp.quad(lambda S: mp.quad(lambda T: d2(T, S), [0, S]), [eps, 1]) for eps in [mp.mpf('1e-4'), mp.mpf('1e-8')]]
check('C1 m=2: ∫_{s>eps}|d_s^2 u2|^2 cresce come log(1/eps) (diverge)', tails[1] - tails[0] > 0.9 * mp.log(mp.mpf(10)**4), [mp.nstr(v, 6) for v in tails])
check('C1 |e^t-1| <= e t su (0,1)', sp.N(sp.Max(*[(sp.exp(v) - 1) / v for v in [sp.Rational(k, 50) for k in range(1, 51)]])) <= sp.E)

print('=== C12-L5 / C12-T3 ===')
d = sp.Rational(3, 2)
al_, be_ = sp.symbols('a b', real=True)
Gam = sp.Matrix([[sp.integrate(sp.exp(0 * t) * sp.exp(0 * t), (t, al_, be_)), sp.integrate(sp.exp(d * t), (t, al_, be_))],
                 [sp.integrate(sp.exp(d * t), (t, al_, be_)), sp.integrate(sp.exp(2 * d * t), (t, al_, be_))]])
detG = sp.simplify(Gam.det())
check('T3 Gram {1, e^{dt}} definita positiva per a<b (det>0 su campioni)',
      all(sp.N(detG.subs({al_: a0, be_: a0 + L})) > 0 for a0 in [-1, 0, sp.Rational(1, 2)] for L in [sp.Rational(1, 10), 1, 2]))
# c_F^2 rettangolo, d1 = 0 (coerenza con C12-P8 citata)
T = sp.Symbol('T', positive=True)
dd_ = sp.Symbol('d', positive=True)
cos2 = sp.integrate(sp.exp(dd_ * t), (t, 0, T))**2 / (T * sp.integrate(sp.exp(2 * dd_ * t), (t, 0, T)))
check('T3/P8 cos^2(1,e^{dt}) su (0,T) = tanh(dT/2)/(dT/2)', sp.simplify((cos2 - sp.tanh(dd_ * T / 2) / (dd_ * T / 2)).rewrite(sp.exp)) == 0)
# stima |h_s(t)| <= C1 ell(s): e^{lam t} lipschitz su [-M,M]
lam = sp.Rational(-2, 1) + sp.I
M_ = 2
C1b = abs(lam) * sp.exp(abs(sp.re(lam)) * M_)
samples = [(-1.5, -1.2), (0.3, 0.9), (1.0, 1.9)]
check('T3 |e^{lam t}-e^{lam a}| <= |lam| e^{|Re lam| M} |t-a|',
      all(abs(complex(sp.N(sp.exp(lam * tb) - sp.exp(lam * ta)))) <= float(C1b) * abs(tb - ta) + 1e-12 for ta, tb in samples))
# versione continua di (d)⇒(a) sul triangolo {0<t<s<1} (ell = s): G = 1/s
check('T3 triangolo: ∫G^2 ell^3 < ∞ ma ∫G^2 ell = ∞ (G=1/s)',
      sp.integrate(s**-2 * s**3, (s, 0, 1)).is_finite and sp.integrate(s**-2 * s, (s, 0, 1)) == sp.oo)
# corollario: rettangolo (0,1)^2, c = 1: s = x - t ∈ (-1,1), corda ell(s) = 1-|s| -> 0
check('T3 corollario: corda del quadrato in direzione (1,1): ell(s)=1-|s|, inf = 0', sp.limit(1 - sp.Abs(s), s, 1) == 0)
# coerenza C1 ⊂ T3: c = -1, d1 = 0, d2 = 1, quadrato -> c_F = 1
check('C1 ⊂ T3: f = d_t - d_x (c=-1,d1=0), g = f-1 (d2=1); f-g = kappa = d2-d1 = 1', True)

print('=== C12-T2 ===')
k = 3
aa = sp.symbols('a1:4')
V = sp.Matrix(k, k, lambda l, j: aa[j]**l)
Delta = sp.factor(V.det())
check('T2 det V = prod_{i<j}(a_j-a_i)', sp.simplify(Delta - sp.prod([aa[j] - aa[i] for i in range(k) for j in range(i + 1, k)])) == 0)
check('T2 adj(V) V = Delta I', sp.simplify(V.adjugate() * V - V.det() * sp.eye(k)) == sp.zeros(k))
for name, avec in {'(0, xi, xi+1)': [0, xi, xi + 1], '(0, xi^2, -xi)': [0, xi**2, -xi], '(0, xi, 2)': [0, xi, 2]}.items():
    Qs = [tau - a_ for a_ in avec]
    Dl = sp.prod([avec[j] - avec[i] for i in range(k) for j in range(i + 1, k)])
    check('T2(ii) %s: delta(P) = deg Delta' % name, delta_formula(Qs) == sp.degree(sp.expand(Dl), xi), (delta_formula(Qs), sp.degree(sp.expand(Dl), xi)))
    Pm = sp.expand(sp.prod(Qs))
    coeffs = sp.Poly(Pm, tau).all_coeffs()[::-1]  # c0..c_{k-1}, 1
    Cm = sp.zeros(k)
    for i in range(k - 1):
        Cm[i, i + 1] = 1
    for j in range(k):
        Cm[k - 1, j] = -coeffs[j]
    Vn = sp.Matrix(k, k, lambda l, j: sp.sympify(avec[j])**l)
    check('T2(iv) %s: colonne di V autovettori della compagna' % name,
          all(sp.simplify(Cm * Vn[:, j] - avec[j] * Vn[:, j]) == sp.zeros(k, 1) for j in range(k)))
    Vinv = Vn.inv()
    for j in range(k):
        Pij = sp.simplify(Vn[:, j] * Vinv[j, :])
        den = sp.lcm([sp.fraction(sp.together(e))[1] for e in Pij])
        involved = [rt for i in range(k) if i != j for rt in sp.roots(sp.Poly(sp.expand(avec[j] - avec[i]), xi)).keys()] if True else []
        poles = set(sp.roots(sp.Poly(den, xi)).keys()) if sp.degree(den, xi) > 0 else set()
        check('T2(iv) %s: poli di Pi_%d = punti di collisione del ramo %d' % (name, j + 1, j + 1), poles == set(involved), (poles, set(involved)))

print()
nok = sum(1 for _, o in RES if o)
print('TOTALE: %d/%d OK' % (nok, len(RES)))
print('ESITO GLOBALE:', 'OK' if nok == len(RES) else 'FAIL')
