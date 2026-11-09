# S5-EX · E2 trasporto + diffusione (avvezione-diffusione) u_t + c u_x = D u_xx: il caso con E_int
# P = tau - a(xi), a = a1 + a2, a1 = -c xi (trasporto), a2 = D xi^2 (diffusione)
# Teoremi: C3-T4, C3-T3, P2-T2, P1-T2 (i)-(iv), P1-E1, P1-T3, P1-P1(e), P3-T1(a1), P3-P1, P3-T3
# Eseguire: D:\ProblemaBase\.venv\Scripts\python.exe -I ex2_AD.py
import sys
import itertools
import random
import sympy as sp
import mpmath as mp

sys.stdout.reconfigure(encoding='utf-8')
t, x = sp.symbols('t x', positive=True)
tau, xi, zeta, s = sp.symbols('tau xi zeta s')
c, D = sp.symbols('c D', positive=True)
RES = []


def check(name, cond, info=''):
    RES.append((name, bool(cond)))
    print(('[OK]   ' if cond else '[FAIL] ') + name + ((' :: ' + str(info)) if info != '' else ''))


def der(u, i, j):
    for _ in range(i):
        u = sp.diff(u, t)
    for _ in range(j):
        u = sp.diff(u, x)
    return u


def apply(Q, u):
    Q = sp.Poly(sp.expand(Q), tau, xi)
    return sp.expand(sum(cf * der(u, i, j) for (i, j), cf in Q.terms()))


def opx(a, f, var=x):
    """a(d_x) f, a polinomio in xi"""
    a = sp.Poly(sp.expand(a), xi)
    return sp.expand(sum(cf * sp.diff(f, var, k) for (k,), cf in a.terms()))


def flow_poly(a, f, T):
    """e^{T a(d_x)} f per f polinomio in x (serie finita)"""
    out, term, k = 0, f, 0
    while term != 0:
        out += term
        k += 1
        term = sp.expand(T * opx(a, term) / k)
        if k > 60:
            raise RuntimeError
    return sp.expand(out)


a1, a2 = -c * xi, D * xi**2
a = a1 + a2
P = tau - a

print('== E2.1 nucleo di AD: non EP, identifica (C3-T4(a)) ==')
GAD = (4 * sp.pi * D * t)**sp.Rational(-1, 2) * sp.exp(-(x - c * t)**2 / (4 * D * t))
check('E2.1a P(d)G_AD = 0', sp.simplify(apply(P, GAD)) == 0)
degs = [sp.Poly(sp.simplify(der(GAD, 0, k) / GAD), x).degree() for k in range(9)]
check('E2.1b deg_x(d_x^k G_AD/G_AD) = k => G_AD non EP => Ann = (P)', degs == list(range(9)), degs)

print('== E2.2 P2-T2: {E_perp = 0} = Sol(tau-a, g), g = (a-a1)(a-a2) = -cD xi^3 ==')
g = sp.expand((a - a1) * (a - a2))
check('E2.2a g = -c D xi^3, K = 3', sp.expand(g + c * D * xi**3) == 0)
Qt = sp.expand((tau - a1) * (tau - a2))
check('E2.2b Q - g ∈ (tau - a)R (divisione): Q(d)u = g(d_x)u su ker P', sp.rem(sp.Poly(Qt - g, tau), sp.Poly(P, tau)).as_expr() == 0)
umode = sp.exp(a.subs(xi, zeta) * t + zeta * x)
check('E2.2c sul modo e^{a(z)t+zx}: Q(d)u = -cD z^3 u (≠0 per z≠0: E_perp ≠ 0, P2-L1)',
      sp.simplify(apply(Qt, umode) / umode + c * D * zeta**3) == 0)
A0, A1, A2 = sp.symbols('A0 A1 A2', cls=sp.Function)
upol = A0(t) + A1(t) * x + A2(t) * x**2
eqs = sp.Poly(sp.expand(apply(P, upol)), x).coeffs()
sol = sp.dsolve(eqs, [A0(t), A1(t), A2(t)])
ugen = sp.expand(upol.subs({sl.lhs: sl.rhs for sl in sol}))
consts = sorted(ugen.free_symbols - {t, x, c, D}, key=str)
basis = [sp.expand(sp.diff(ugen, k)) for k in consts]
target = [sp.Integer(1), x - c * t, sp.expand((x - c * t)**2 + 2 * D * t)]
M = sp.Matrix([[sp.Poly(sp.expand(b), x, t).coeff_monomial(m) for m in [1, x, t, x**2, x * t, t**2]] for b in basis + target])
check('E2.2d Sol(tau-a, xi^3) = span{1, x-ct, (x-ct)^2+2Dt} (dim 3)', len(basis) == 3 and M.rank() == 3)
v1 = (x - c * t)**2 - 2 * D / c * (x - c * t)
v2 = 2 * D / c * x
check('E2.2e (x-ct)^2+2Dt = v1 + v2, v1 ∈ ker(tau-a1), v2 ∈ ker(tau-a2) (componenti in D_1, D_2)',
      sp.expand(v1 + v2 - target[2]) == 0 and apply(tau - a1, v1) == 0 and apply(tau - a2, v2) == 0)
u3 = sp.expand((x - c * t)**3 + 6 * D * t * (x - c * t))
check('E2.2f u = (x-ct)^3+6Dt(x-ct) ∈ ker P ma g(d_x)u = -6cD ≠ 0 => E_perp(u) ≠ 0 (fuori dallo spazio K=3)',
      apply(P, u3) == 0 and sp.expand(opx(g, u3) + 6 * c * D) == 0)
check('E2.2g nota P2-T2: la componente v1 non sta in Sol(R/J_1), J_1 = (tau-a1, a-a1): D xi^2 v1 ≠ 0',
      sp.expand(opx(D * xi**2, v1)) != 0)

print('== E2.3 P1-T2: formula chiusa di E_int^add, E^mult = 0 (classe B) ==')
z1 = sp.exp(a1.subs(xi, zeta) * t) - 1
z2 = sp.exp(a2.subs(xi, zeta) * t) - 1
u0 = sp.exp(zeta * x)
un = [sp.exp(an.subs(xi, zeta) * t + zeta * x) for an in (a1, a2)]
check('E2.3a flussi per termine u_n = e^{t a_n(z)} e^{zx} risolvono (d_t - a_n(d_x))u_n = 0, u_n(0) = u0',
      all(sp.simplify(apply(tau - an, un_)) == 0 and un_.subs(t, 0) == u0 for an, un_ in zip((a1, a2), un)))
Eadd = umode - u0 - sum(un_ - u0 for un_ in un)
check('E2.3b (ii)-(iii): E^add = z1 z2 e^{zx}', sp.simplify(Eadd - z1 * z2 * u0) == 0)
check('E2.3c E^mult = 0 sul modo: e^{t a} = e^{t a1} e^{t a2}', sp.simplify(umode - sp.exp(a1.subs(xi, zeta) * t) * un[1]) == 0)
# molteplicita' l = 1: u0 = x e^{z0 x}
z0 = sp.Rational(3, 2)
uM = sp.diff(umode, zeta).subs(zeta, z0)
unM = [sp.diff(un_, zeta).subs(zeta, z0) for un_ in un]
EaddM = uM - uM.subs(t, 0) - sum(w - w.subs(t, 0) for w in unM)
predM = sp.diff(z1 * z2 * u0, zeta).subs(zeta, z0)
check('E2.3d (iii) con molteplicità: u0 = x e^{z0 x}, E^add = d_z[e_{>=2}(z) e^{zx}]_{z0}',
      sp.simplify(EaddM - predM) == 0 and sp.simplify(uM.subs(t, 0) - x * sp.exp(z0 * x)) == 0)
# dati polinomiali
for k, pred in ((2, 0), (3, -6 * c * D * t**2), (4, None)):
    f = x**k
    uk = flow_poly(a, f, t)
    u1k, u2k = flow_poly(a1, f, t), flow_poly(a2, f, t)
    E = sp.expand(uk - f - (u1k - f) - (u2k - f))
    Eform = sp.expand(sum(t**m / sp.factorial(m) * sum(sp.binomial(m, m1) * opx(a1**m1 * a2**(m - m1), f)
                                                      for m1 in range(1, m)) for m in range(2, 2 * k + 2)))
    ok = apply(P, uk) == 0 and sp.expand(E - Eform) == 0 and (pred is None or sp.expand(E - pred) == 0)
    check(f'E2.3e u0 = x^{k}: E^add = {sp.factor(E)} = serie formale (iv)' + (f', predetto {pred}' if pred is not None else ''), ok)
# getto formale (iv) per f generica, N = 3 (AD + reazione lam)
lam = sp.symbols('lam')
f = sp.Function('f')(x)
terms = [a1, a2, sp.Integer(0) * xi + lam]
atot = sum(terms)
for m in range(2, 5):
    lhs = opx(atot**m, f) - sum(opx(tn**m, f) for tn in terms)   # coefficiente s^m/m! di E^{add,form}
    rhs = 0
    for ks in itertools.product(range(m + 1), repeat=3):
        if sum(ks) == m and sum(1 for kk in ks if kk > 0) >= 2:
            rhs += sp.factorial(m) / sp.prod([sp.factorial(kk) for kk in ks]) * opx(sp.prod([tn**kk for tn, kk in zip(terms, ks)]), f)
    check(f'E2.3f (iv) N=3 (trasporto+diffusione+reazione), coefficiente di s^{m}/{m}! per f generica', sp.expand(lhs - rhs) == 0)

print('== E2.4 P1-E1: dato stazionario e^{cx/D}, E^add = -4 sinh^2(theta/2) e^{cx/D}, theta = c^2 t/D ==')
zs = c / D
check('E2.4a a(c/D) = 0 (stazionario)', sp.simplify(a.subs(xi, zs)) == 0)
th = c**2 * t / D
E = (z1 * z2).subs(zeta, zs)
check('E2.4b E^add/u0 = -4 sinh^2(theta/2)', sp.simplify((E + 4 * sp.sinh(th / 2)**2).rewrite(sp.exp)) == 0)

print('== E2.5 P1-T3: aggregati per ordine in O(N^2) (DP) vs tabella di Moebius Theta(2^N) ==')
random.seed(1)
for N in range(2, 9):
    zz = [sp.Rational(random.randint(-9, 9), random.randint(1, 9)) for _ in range(N)]
    mults = 0
    e = [sp.Integer(1)] + [sp.Integer(0)] * N
    for n_, zn in enumerate(zz, start=1):
        for k in range(n_, 0, -1):
            e[k] = e[k] + zn * e[k - 1]
            mults += 1
    tab, tmult = {}, 0
    for n_ in range(N):
        tab[(n_,)] = zz[n_]
    for size in range(2, N + 1):
        for S in itertools.combinations(range(N), size):
            tab[S] = tab[S[:-1]] * zz[S[-1]]
            tmult += 1
    brute = [sum(sp.prod([zz[i] for i in S]) for S in itertools.combinations(range(N), k)) for k in range(N + 1)]
    ok = all(e[k] == brute[k] for k in range(2, N + 1)) and mults == N * (N + 1) // 2 and tmult == 2**N - N - 1
    Eadd_val = sp.prod([1 + zn for zn in zz]) - 1 - sum(zz)
    ok = ok and Eadd_val == sum(e[2:])
    check(f'E2.5 N={N}: e_k(z) da DP = somma sui sottoinsiemi; molt. DP = N(N+1)/2 = {mults}; tabella 2^N-N-1 = {tmult}; E^add = sum_k>=2 e_k', ok)

print('== E2.6 P1-P1(e): u -> E^add non continua in H^m(Omega) (c = D = 1, Omega = (0,1)^2, m = 1) ==')
mp.mp.dps = 30


def ratio(zv, m=1):
    zv = mp.mpf(zv)
    A = zv**2 - zv                           # a(zeta) per c = D = 1
    ex2 = mp.quad(lambda X: mp.e**(2 * zv * X), [0, 1])
    # ||E||_{L2}^2 = int_0^1 |z1 z2|^2 dt * ||e^{zx}||^2
    En = mp.quad(lambda T: ((mp.e**(-zv * T) - 1) * (mp.e**(zv**2 * T) - 1))**2, [0, 1]) * ex2
    # ||u||_{H^1}^2 = sum_{i+j<=1} ||d^alpha u||^2 = (1 + A^2 + z^2) int e^{2At} * ||e^{zx}||^2
    Un = (1 + A**2 + zv**2) * mp.quad(lambda T: mp.e**(2 * A * T), [0, 1]) * ex2
    return En / Un


rs = [ratio(zv) for zv in (2, 4, 8, 16)]
check('E2.6 rapporto ||E^add||^2_{L2}/||u||^2_{H1} crescente e > 10^3 volte per z: 2 -> 16 (P1-P1(e), V-ex)',
      all(rs[i] < rs[i + 1] for i in range(3)) and rs[-1] / rs[0] > 1e3, [mp.nstr(r, 5) for r in rs])

print('== E2.7 P3-T1(a1): criterio (Par) sul simbolo ==')
kap = sp.symbols('kappa', real=True)
ReA = sp.re(sp.expand(a.subs(xi, sp.I * kap)))
check('E2.7 Re a(i kappa) = -D kappa^2: q = 2 pari, Re(alpha_q i^q) = -D < 0 => (Par) vale, Dyson-Phillips per AD su L2(R)',
      sp.simplify(ReA + D * kap**2) == 0)

print('== E2.8 P3-P1 / P3-T3: AD su (0,L) con Dirichlet, accoppiamento V = -c d_x ==')
L = sp.symbols('L', positive=True)
Ds = sp.symbols('Dd', positive=True)
mu = lambda n: n * sp.pi / L
e_ = lambda n: sp.sqrt(2 / L) * sp.sin(mu(n) * x)
okV = True
for m_ in range(1, 7):
    for n_ in range(1, 7):
        Vmn = sp.simplify(sp.integrate(e_(m_) * (-c) * sp.diff(e_(n_), x), (x, 0, L)))
        pred = (-4 * c * m_ * n_ / (L * (m_**2 - n_**2))) if (m_ + n_) % 2 == 1 else 0
        okV = okV and sp.simplify(Vmn - pred) == 0
check('E2.8a V_mn = <e_m, -c d_x e_n> = -4cmn/(L(m^2-n^2)) se m+n dispari, 0 altrimenti (m,n <= 6)', okV)
lm, ln = sp.symbols('lambda_m lambda_n')
ss = sp.symbols('s_', positive=True)
F1 = sp.integrate(sp.exp(lm * (t - ss)) * sp.exp(ln * ss), (ss, 0, t), conds='none')
w = t * (ln - lm)
phi = (sp.exp(w) - 1 - w) / w
check('E2.8b P3-P1(b): F_1 - t e^{lm t} = t e^{lm t} phi(t(ln-lm)), phi(w) = (e^w-1-w)/w',
      sp.simplify(sp.piecewise_fold(F1).args[-1][0] - t * sp.exp(lm * t) - t * sp.exp(lm * t) * phi if isinstance(F1, sp.Piecewise) else F1 - t * sp.exp(lm * t) - t * sp.exp(lm * t) * phi) == 0)


def Emult_norm(tv, coeffs, Lv=1.0, Dv=1.0, cv=1.0):
    """|| E^{mult,(1)}(t) u0 ||_{L2} per u0 = sum coeffs[n] e_n (dati modali finiti), somma troncata adattiva"""
    kap_ = Dv * mp.pi**2 / Lv**2
    lam_ = lambda n: -kap_ * n * n

    def ph(wv):
        return (mp.expm1(wv) - wv) / wv if wv != 0 else mp.mpf(0)
    Mmax = int(40 / mp.sqrt(kap_ * tv)) + 50
    tot = mp.mpf(0)
    for m_ in range(1, Mmax):
        sm = mp.mpf(0)
        for n_, cn in coeffs.items():
            if (m_ + n_) % 2 == 1:
                Vmn = -4 * cv * m_ * n_ / (Lv * (m_**2 - n_**2))
                sm += cn * Vmn * tv * mp.e**(lam_(m_) * tv) * ph(tv * (lam_(n_) - lam_(m_)))
        tot += sm**2
    return mp.sqrt(tot)


mp.mp.dps = 20
ts = [mp.mpf(10)**(-k) for k in (3, 4, 5, 6)]
n1 = [Emult_norm(tv, {1: 1}) for tv in ts]
sl1 = [mp.log10(n1[i] / n1[i + 1]) for i in range(3)]
check('E2.8c P3-T3: u0 = e_1 ((u0\'(0),u0\'(L)) ≠ 0): pendenza log-log di ||E^{mult,(1)}|| -> 5/4 (V-ex numerico)',
      abs(sl1[-1] - 1.25) < 0.02, [mp.nstr(v, 5) for v in sl1])
n2 = [Emult_norm(tv, {1: 1, 3: -mp.mpf(1) / 3}) for tv in ts]
sl2 = [mp.log10(n2[i] / n2[i + 1]) for i in range(3)]
check('E2.8d P3-T3: u0 = e_1 - e_3/3 (u0\'(0) = u0\'(L) = 0): pendenza >= 2 - 0.02 (O(t^2)) (V-ex numerico)',
      sl2[-1] > 1.98, [mp.nstr(v, 5) for v in sl2])

# costanti di OPA-T2(iii): ||E|| ~ |c| N_{k-1} D^{k/2-1/4} sqrt(u0^(k)(0)^2+u0^(k)(L)^2)/(k-1)! t^{k/2+3/4}
C1 = mp.mpf('0.234005') * 2 * mp.pi                  # k = 1, e_1: sqrt(2 pi^2 + 2 pi^2) = 2 pi
C3 = mp.mpf('0.203448') * 16 * mp.pi**3 / 2           # k = 3, e_1 - e_3/3: u0'''(0) = 8 sqrt2 pi^3 = -u0'''(L)
r1 = n1[-1] / ts[-1]**mp.mpf(1.25)
r3 = n2[-1] / ts[-1]**mp.mpf(2.25)
check('E2.8e OPA-T2(iii) k=1: costante ||E||/t^{5/4} -> |c| N_0 * 2pi (t = 1e-6)', abs(r1 / C1 - 1) < 2e-3, [mp.nstr(r1, 6), mp.nstr(C1, 6)])
check('E2.8f OPA-T2(iii) k=3 (contatto cubico): esponente 9/4 e costante |c| N_2 * 8 pi^3 (t = 1e-6)', abs(r3 / C3 - 1) < 1e-2, [mp.nstr(r3, 6), mp.nstr(C3, 6)])

nok = sum(1 for _, ok in RES if ok)
print(f'\nTOTALE E2: {nok}/{len(RES)} OK')
