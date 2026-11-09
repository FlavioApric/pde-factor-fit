# Verifiche indipendenti S-CHECK-F8-ENC-rev2 sui claim nuovi di S8-ENC rev. 2.
# ENC-P0' (esempi su S(R): lente, Avron-Herbst, beta(t)x + gamma(t)), ENC-P0'-DIC,
# POLE-N^cl (polo mobile), ENC-T2(c') con q non polinomiale.
import sys
sys.stdout.reconfigure(encoding="utf-8")
import sympy as sp

res = []
def report(name, ok, info=""):
    res.append((name, bool(ok)))
    print(("OK  " if ok else "FAIL") + " " + name + ("  " + info if info else ""))

t, x, y, k, F, tau = sp.symbols('t x y k F tau', real=True)
a0 = sp.symbols('a0', positive=True)

# --- L1: lente nella normalizzazione 1/2. v(tau, y) = e^{iky - ik^2 tau/2} risolve i v_tau = -v_yy/2.
#     PP: v(tan t, y) = (cos t)^{1/2} e^{i y^2 sin t cos t / 2} u(t, y cos t).
#     Inversa: u(t, x) = (cos t)^{-1/2} e^{-i x^2 tan t / 2} v(tan t, x / cos t).
v = lambda T, Y: sp.exp(sp.I*k*Y - sp.I*k**2*T/2)
u = sp.cos(t)**sp.Rational(-1, 2)*sp.exp(-sp.I*x**2*sp.tan(t)/2)*v(sp.tan(t), x/sp.cos(t))
r = sp.I*sp.diff(u, t) + sp.diff(u, x, 2)/2 - x**2*u/2
report("L1 lente: u risolve i u_t = -u_xx/2 + x^2 u/2", sp.simplify(sp.expand(r/u)) == 0)
back = sp.cos(t)**sp.Rational(1, 2)*sp.exp(sp.I*y**2*sp.sin(t)*sp.cos(t)/2)*u.subs(x, y*sp.cos(t))
report("L2 lente: formula del PP nella variabile y inverte la mappa",
       sp.simplify(back/v(sp.tan(t), y) - 1) == 0)
# unitarieta' della mappa W(t) f(y) = (cos t)^{1/2} e^{...} f(y cos t): |.|^2 dy -> |f|^2 dx
tv = sp.Rational(1, 3)
fW = sp.cos(tv)**sp.Rational(1, 2)*sp.exp(sp.I*y**2*sp.sin(tv)*sp.cos(tv)/2)*sp.exp(-(y*sp.cos(tv))**2/2)
nW = sp.integrate(sp.simplify(fW*sp.conjugate(fW)), (y, -sp.oo, sp.oo))
report("L3 lente: W(t) isometrica (gaussiana, t = 1/3)", sp.simplify(nW - sp.sqrt(sp.pi)) == 0)

# --- AH: classe V = beta(t) x + gamma(t), normalizzazione del progetto i u_t = -u_xx + V u.
B = sp.Function('B')(t); Xi = sp.Function('Xi')(t); Ph = sp.Function('Ph')(t); G = sp.Function('G')(t)
vf = sp.exp(sp.I*k*(x - Xi) - sp.I*k**2*t)
uf = sp.exp(-sp.I*B*x - sp.I*Ph - sp.I*G)*vf
beta = sp.diff(B, t); gam = sp.diff(G, t)
r = sp.I*sp.diff(uf, t) + sp.diff(uf, x, 2) - (beta*x + gam)*uf
r = r.subs({sp.Derivative(Xi, t): -2*B, sp.Derivative(Ph, t): B**2})
report("BG1 V = beta x + gamma: u = e^{-iBx - iPhi - i int gamma} v(t, x - Xi)", sp.simplify(r/uf) == 0)
ah = uf.subs({B: F*t, Xi: -F*t**2, Ph: F**2*t**3/3, G: 0}).doit()
ah_ref = sp.exp(-sp.I*F*t*x - sp.I*F**2*t**3/3)*vf.subs(Xi, -F*t**2)
report("BG2 Avron-Herbst come caso beta = F (theta = id)", sp.simplify(ah/ah_ref - 1) == 0)

# --- DIC: ansatz puntuale + gauge u = rho^{-1/2} e^{i a x^2} v(T, x/rho) per V = alpha x^2.
a = sp.Function('a')(t); rho = sp.Function('rho')(t); T = sp.Function('T')(t)
al = sp.Function('alpha')(t)
vv = sp.Function('v')
Y = x/rho
w = rho**sp.Rational(-1, 2)*vv(T, Y)
U = sp.exp(sp.I*a*x**2)*w
r = sp.I*sp.diff(U, t) + sp.diff(U, x, 2) - al*x**2*U
# sostituisci v_T = i v_YY (soluzione libera i v_T = -v_YY)
vT = sp.Derivative(vv(T, Y), T)
r = r.doit()
r = sp.expand(sp.simplify(r*sp.exp(-sp.I*a*x**2)*rho**sp.Rational(1, 2)))
sym = {sp.Derivative(T, t): 1/rho**2, sp.Derivative(rho, t): 4*a*rho, sp.Derivative(a, t): -4*a**2 - al}
r2 = r.subs(sym)
r2 = r2.replace(lambda e: isinstance(e, sp.Subs), lambda e: e.doit())
# controllo numerico su una soluzione libera esplicita al posto di v generica
Tt, Yy = sp.symbols('Tt Yy')
vfree = sp.exp(sp.I*k*Yy - sp.I*k**2*Tt)
Ue = sp.exp(sp.I*a*x**2)*rho**sp.Rational(-1, 2)*vfree.subs({Tt: T, Yy: x/rho})
re = sp.I*sp.diff(Ue, t) + sp.diff(Ue, x, 2) - al*x**2*Ue
re = sp.simplify((re/Ue).subs(sym))
report("DIC1 sistema T' = 1/rho^2, rho' = 4 a rho, a' + 4a^2 = -alpha annulla il residuo", re == 0)
# theta = id forza alpha = 0: T' = 1 => rho = 1 => a = 0 => alpha = 0
rpos = [sol for sol in sp.solve(sp.Eq(1/sp.Symbol('R')**2, 1), sp.Symbol('R')) if sol > 0]
a_from = sp.diff(sp.Integer(rpos[0]), t)/(4*rpos[0])        # a = rho'/(4 rho) con rho = 1
alpha_from = -sp.diff(a_from, t) - 4*a_from**2
report("DIC2 theta = id => rho = 1 (rho(0) = 1) => a = 0 => alpha = 0", rpos == [1] and alpha_from == 0)
# controesempio al verso "alpha = 0 => theta = id" per OGNI rappresentante: V = 0, a = a0/(1+4 a0 t)
asol = a0/(1 + 4*a0*t); rsol = 1 + 4*a0*t; Tsol = t/(1 + 4*a0*t)
ok = (sp.simplify(sp.diff(asol, t) + 4*asol**2) == 0 and sp.simplify(sp.diff(rsol, t) - 4*asol*rsol) == 0
      and sp.simplify(sp.diff(Tsol, t) - 1/rsol**2) == 0)
Uc = sp.exp(sp.I*asol*x**2)*rsol**sp.Rational(-1, 2)*vfree.subs({Tt: Tsol, Yy: x/rsol})
rc = sp.simplify((sp.I*sp.diff(Uc, t) + sp.diff(Uc, x, 2))/Uc)
report("DIC3 V = 0 (alpha = 0) ha un rappresentante con theta(t) = t/(1+4a0 t) != id (pseudo-conforme)",
       ok and rc == 0 and sp.simplify(Tsol - t) != 0)

# --- POLE: polo mobile. psi = x - z(t) autofunzione di L_0 (lambda = 0); A = d - 1/(x-z);
#     V = 2/(x-z)^2; W = A^# = -d - 1/(x-z) soddisfa W L_V = L_0 W a ogni t, ma non intreccia i d_t.
z = sp.Function('z')(t)
g = sp.Function('g')(t, x)
Wop = lambda f: -sp.diff(f, x) - f/(x - z)
LV = lambda f: -sp.diff(f, x, 2) + 2*f/(x - z)**2
L0 = lambda f: -sp.diff(f, x, 2)
inst = sp.simplify(Wop(LV(g)) - L0(Wop(g)))
report("POLE1 W L_V = L_0 W istantaneo con polo mobile", inst == 0)
par = sp.simplify(Wop(sp.I*sp.diff(g, t) - LV(g)) - (sp.I*sp.diff(Wop(g), t) - L0(Wop(g))))
dWg = -sp.diff(z, t)*g/(x - z)**2          # (d_t W) g
report("POLE2 residuo parabolico = -i (d_t W) g, non nullo se z' != 0",
       sp.simplify(par - (-sp.I*dWg)) == 0)
# rettangolo: z(t) = t, tempi 0 e 2, U = (1/2, 3/2) libero da poli in t = 0 e t = 2 ma non in t = 1
zt = lambda tt: tt
report("POLE3 U libero da poli ai due tempi ma non sul segmento [0,2] x U",
       not (0.5 < zt(0) < 1.5) and not (0.5 < zt(2) < 1.5) and (0.5 < zt(1) < 1.5))

# --- T2(c'): q non polinomiale, sviluppo in serie attorno a x1.
X = sp.symbols('X')
x1 = sp.Rational(2, 5)
q = sp.sin(x) + sp.exp(x/3)
qX = q.subs(x, X + x1)
Lq = lambda f: -sp.diff(f, X, 2) + qX*f
def lowest(P_coeffs, M):
    acc = 0; f = X**M
    for c_ in P_coeffs:
        acc += c_*f; f = Lq(f)
    s = sp.series(sp.expand(acc), X, 0, M + 2).removeO()
    pol = sp.Poly(sp.expand(s), X)
    lo = min(pol.monoms())[0]
    return lo, pol.coeff_monomial(X**lo)
M = 9
lo, lc = lowest([2, 0, -1, sp.Rational(1, 2)], M)          # d = 3, p_3 = 1/2
exp_c = sp.Rational(1, 2)*(-1)**3*sp.factorial(M)/sp.factorial(M - 6)
report("T2c'1 q = sin x + e^{x/3}, d = 3: ordine minimo M - 2d, coeff p_d(-1)^d M!/(M-2d)!",
       lo == M - 6 and sp.simplify(lc - exp_c) == 0, "ordine %d, coeff %s" % (lo, lc))
lo0, lc0 = lowest([7], 4)
report("T2c'2 caso d = 0: P_* = p_0, P_*(alpha, L_q)(x-x1)^M = p_0 (x-x1)^M", lo0 == 4 and lc0 == 7)
lo2, lc2 = lowest([0, 0, 1], 4)                             # M = 2d: termine costante
report("T2c'3 caso limite M = 2d: termine costante p_d (-1)^d M! != 0", lo2 == 0 and lc2 == sp.factorial(4))
# getto nullo: tutte le derivate miste di ordine <= N di e^{alpha t}(x-x1)^M in (t1, x1) sono nulle, M > N
al_, N = sp.Rational(3, 2), 5
h = sp.exp(al_*t)*(x - x1)**(N + 1)
ok = all(sp.diff(h, t, i, x, j).subs({t: sp.Rational(1, 7), x: x1}) == 0
         for i in range(N + 1) for j in range(N + 1 - i))
report("T2c'4 j^N h = 0 in (t1, x1) per M = N + 1", ok)

print('\nTOTALE: %d/%d OK' % (sum(1 for _, o in res if o), len(res)))
