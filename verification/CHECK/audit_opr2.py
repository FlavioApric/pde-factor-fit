# audit_opr2.py — S-CHECK-16, red team indipendente su work/OP-R2/PROOF_PACKAGE.md
# Scritto da zero (non riusa opr2_checks.py). Eseguire:
#   D:\ProblemaBase\.venv\Scripts\python.exe -u -I work/CHECK/sympy/audit_opr2.py
import sympy as sp, mpmath as mp, itertools, math, random, sys
sys.stdout.reconfigure(encoding="utf-8")

RES = []
def check(name, ok, info=""):
    RES.append((name, bool(ok)))
    print(("OK  " if ok else "FAIL") + "  " + name + (("   [" + str(info) + "]") if info != "" else ""))

t, x, s, r, eps, c, xi, L = sp.symbols('t x s r epsilon c xi L', real=True)

# ---------------- A. OPR2-L0 / OPR2-T1 ----------------
th = sp.Function('theta')(t, x); w = sp.Function('w')(t, x)
H = lambda f: sp.diff(f, t) - sp.diff(f, x, 2)
lhs = H(th*w)
rhs = th*H(w) + (sp.diff(th, t) + sp.diff(th, x, 2))*w + sp.diff(-2*sp.diff(th, x)*w, x)
check("A1 H(theta w) = theta Hw + (theta_t+theta_xx)w + d_x(-2 theta_x w)", sp.simplify(lhs - rhs) == 0)
cc = sp.symbols('c', positive=True)
sfun = lambda T_, X_: X_ - cc*T_
check("A2 s(y+tau1) = s(y) - eps(1+c), s(y+tau2) = s(y)+eps(1+c)",
      sp.simplify(sfun(t+eps, x-eps) - (sfun(t, x) - eps*(1+cc))) == 0 and sp.simplify(sfun(t-eps, x+eps) - (sfun(t, x) + eps*(1+cc))) == 0)
xs = sp.symbols('xs', positive=True); Lp = sp.symbols('Lp', positive=True)
K0 = sp.integrate(sp.exp(-r*xs**2), (r, 0, Lp)); K1 = xs*K0
check("A3a ||K0||_L1 = (1-e^{-L xi^2})/xi^2 <= L", sp.simplify(K0 - (1-sp.exp(-Lp*xs**2))/xs**2) == 0)
ok = True
for Lv in [0.1, 1, 3, 11]:
    for a in [10**k for k in range(-4, 5)] + [0.37, 2.9]:
        v1 = -math.expm1(-Lv*a*a)/a
        ok &= v1 <= math.sqrt(Lv)*(1+1e-12) and -math.expm1(-Lv*a*a)/a**2 <= Lv*(1+1e-12)
check("A3b ||K1||_L1 = (1-e^{-L xi^2})/|xi| <= sqrt(L) (griglia)", ok)
# Duhamel: d_t z = z[d_t G] se G(-1)=0 (esempio esplicito)
rr = sp.symbols('rr', real=True)
G = (rr+1)**2*sp.sin(rr)          # G(-1) = 0
z = sp.integrate(sp.exp(-(t-rr)*xs**2)*G, (rr, -1, t))
zG = sp.integrate(sp.exp(-(t-rr)*xs**2)*sp.diff(G, rr), (rr, -1, t))
check("A4 d_t(Duhamel[G]) = Duhamel[d_t G] quando G(-1)=0", sp.simplify(sp.diff(z, t) - zG) == 0)
check("A5 d_t z_hat = -xi^2 z_hat + G", sp.simplify(sp.diff(z, t) + xs**2*z - G.subs(rr, t)) == 0)
# Passo 3: rettangolo campione, ordine r -> delta -> eps0; traslati compatti e triangolo in B(C1,r)
random.seed(1)
def passo3(T, a, b, cv):
    C1 = (0.0, b); C2 = (T, a)
    rv = 0.2*min(T, b-a, math.hypot(T, b-a)/3)
    # delta: triangolo {s > b-delta} di vertici C1, (0,b-delta), (delta/c, b)
    d = 0.5*rv*min(1.0, cv)
    tri_ok = max(math.hypot(0, d), math.hypot(d/cv, 0)) < rv
    e0 = 0.25*min(rv, d)/(1+cv)
    good = True
    for _ in range(4000):
        # punto di Omega-bar in B(C1,3r)
        ang = random.random()*2*math.pi; rad = 3*rv*math.sqrt(random.random())
        tt, xx = C1[0]+rad*math.cos(ang), C1[1]+rad*math.sin(ang)
        if not (0 <= tt <= T and a <= xx <= b): continue
        e = e0*random.random() + 1e-9
        t2, x2 = tt+e, xx-e
        good &= (0 < t2 < T and a < x2 < b and min(t2, T-t2, x2-a, b-x2) >= e*0.999)
        # s-intervallo sull'anello B(2r)\B(r): lontano da b e da a - cT
        if rv <= rad <= 2*rv:
            sv = xx - cv*tt
            good &= (sv <= b - d + 1e-12) and (sv - e*(1+cv) > a - cv*T)
    return tri_ok and good
check("A6 Passo 3: tau1 manda Omega-bar∩B(C1,3r) in un compatto di Omega; anello: s<=b-delta, s-sigma > a-cT (4 rettangoli, scelte r->delta->eps0)",
      all(passo3(*p) for p in [(1, 0, 1, 1.0), (2, -1, 0.5, 0.3), (0.5, 0, 3, 4.0), (1, 0, 1, 0.05)]))

# ---------------- B. OPR2-L1 / T2 ----------------
z1, z2, aa, bb, th1 = sp.symbols('z1 z2 a b th1', real=True)
e = sp.Matrix([1, 0]); f = sp.Matrix([sp.cos(th1), sp.sin(th1)])
Y = sp.Matrix([z1, z2]) + aa*e; Yp = sp.Matrix([z1, z2]) + bb*f
Jac = sp.Matrix.vstack(Y, Yp).jacobian([z1, z2, aa, bb])
check("B1 dy dy' = |sin| dz da db (cambio di variabili HS)", sp.simplify(Jac.det()**2 - sp.sin(th1)**2) == 0)
# nucleo del prodotto: dsigma dsigma' = dy'/|sin|  (mappa (sigma,sigma') -> y + sigma e + sigma' f)
J2 = sp.Matrix([aa*e[0] + bb*f[0], aa*e[1] + bb*f[1]]).jacobian([aa, bb])
check("B2 delta lungo una corda integrata sull'altra: fattore 1/|sin|", sp.simplify(J2.det()**2 - sp.sin(th1)**2) == 0)
# quadrato unitario, v verticale (l=1), w=(1,1) parametro: int dz / l_w = 2 ; wedge: log-divergenza
lw = lambda X, Yy: min(1-X, 1-Yy) + min(X, Yy)    # lunghezza parametrica lungo (1,1)
n = 400; acc = 0.0
for i in range(n):
    for j in range(n):
        acc += 1.0/lw((i+.5)/n, (j+.5)/n)
acc /= n*n
check("B3 int_square dz/(l_v l_w) = 2 (w=(1,1) parametrico)", abs(acc-2) < 1e-2, round(acc, 4))
# Gram di esponenziali: definita positiva, continua in l; nucleo limitato su l in [l0, D]
d1, d2 = sp.Rational(0), sp.Rational(1)
def gram(l):
    fs = [lambda q: 1.0, lambda q: math.exp(q)]
    return mp.matrix([[mp.quad(lambda q: fs[i](q)*fs[j](q), [0, l]) for j in range(2)] for i in range(2)])
mins = [min(mp.eig(gram(l))[0]).real for l in [0.5, 1, 2, 3]]
check("B4 Gram {1, e^sigma} definita positiva per l in [0.5,3]", all(m > 0 for m in mins), [float(m) for m in mins])
# cuneo: int_{eps}^{1} int da db/(ab) su {lam1 a < b < lam2 a}: ~ log(lam2/lam1) log(1/eps)
lam1, lam2 = 0.5, 2.0
vals = []
for E in [1e-2, 1e-4]:
    I = mp.quad(lambda A: mp.log(lam2/lam1)/A, [E, 1])
    vals.append(float(I/mp.log(1/E)))
check("B5 cuneo: integrale HS ~ log(lam2/lam1) log(1/eps) (diverge)", all(abs(v - math.log(4)) < 1e-9 for v in vals))

# ---------------- C. OPR2-T3: esempi di similitudine ----------------
# I = integrazione da 0 (inversa destra di d_x); [x, I] = I^2 (Cauchy), quindi con b = I: b^2 = [x,b]
fpoly = sp.Function('f')
y = sp.symbols('y', real=True)
def Iop(expr):
    return sp.integrate(expr.subs(x, y), (y, 0, x))
test_fs = [x**3 + 2*x, sp.exp(2*x), sp.sin(x)]
ok = all(sp.simplify(x*Iop(g) - Iop(x*g) - Iop(Iop(g))) == 0 for g in test_fs)
check("C1 [x, d_x^{-1}] = d_x^{-2} (realizzato con I = int_0^x)", ok)
# (d_t - x + I)(d_t - x - I) = (d_t - x)^2 su funzioni u(t,x)=a(t)g(x)
at = sp.Function('A')(t)
def Dt(u): return sp.diff(u, t)
def op1(u): return Dt(u) - x*u - Iop(u)     # d_t - x - I
def op2(u): return Dt(u) - x*u + Iop(u)     # d_t - x + I
def opsq(u): v = Dt(u) - x*u; return Dt(v) - x*v
ok = True
for g in test_fs:
    u = at*g
    ok &= sp.simplify(sp.expand(op2(op1(u)) - opsq(u))) == 0
check("C2 (d_t - x)^2 = (d_t - x + d_x^{-1})(d_t - x - d_x^{-1}) in K[d_t]: secondo divisore destro ⇒ (d_t - x)^2 NON uniseriale (rilievo T3-2)", ok)
# Esempio (i): P = d_t(d_t - x) = (d_t - x)d_t con d_t centrale in A_1[d_t]
u = sp.Function('U')(t, x)
check("C3 d_t(d_t - x) = (d_t - x) d_t in A_1[d_t] (d_t commuta con x)",
      sp.simplify(sp.diff(sp.diff(u, t) - x*u, t) - (sp.diff(sp.diff(u, t), t) - x*sp.diff(u, t))) == 0)
# a costante: (d_t - a)^2 uniseriale (b^2 = [a,b] = 0 => b = 0) — controllo nel commutativo
bsym = sp.symbols('bs')
check("C4 a centrale: b^2 = [a,b] = 0 => b = 0 (uniseriale)", sp.solve(sp.Eq(bsym**2, 0), bsym) == [0])

# ---------------- D. OPR2-L2 ----------------
nN = sp.symbols('n', integer=True, nonnegative=True)
def g_der_coeff(i, n_): return sp.Rational(1, sp.factorial(n_)*sp.factorial(n_+i))
for N in [3, 7]:
    M = sp.Matrix([[g_der_coeff(i, n_) for i in range(N+1)] for n_ in range(N+3)])
    check(f"D1 g, g', ..., g^({N}) linearmente indipendenti (rango dei coefficienti di Taylor = {N+1})", M.rank() == N+1)
# |g^(i)(z)| <= e^{2 sqrt R}
ok = True
for R in [0.5, 4, 30]:
    for i in [0, 1, 5, 20]:
        val = mp.nsum(lambda k: mp.mpf(R)**k/(mp.factorial(k)*mp.factorial(k+i)), [0, mp.inf])
        ok &= val <= mp.e**(2*mp.sqrt(R))
check("D2 sup_{|z|<=R}|g^(i)| <= e^{2 sqrt R} uniformemente in i", ok)
# Ricorrenza di Kovalevskaya per P = tau^2 - 2 xi tau + xi^2 - xi (monico, deg_tau = deg = 2): P(d)U = 0 a ordine troncato
gx = sum(x**k/sp.factorial(k)**2 for k in range(40))
p1 = lambda f_: -2*sp.diff(f_, x)                    # coefficiente di tau^1: -2 xi
p0 = lambda f_: sp.diff(f_, x, 2) - sp.diff(f_, x)    # tau^0: xi^2 - xi
lam = [sp.Rational(1), sp.Rational(2)]
us = [lam[0]*gx, lam[1]*gx]
for k in range(2, 8):
    us.append(sp.expand(-(p0(us[k-2]) + p1(us[k-1]))))
U = sum(t**k*us[k]/sp.factorial(k) for k in range(8))
PU = sp.diff(U, t, 2) - 2*sp.diff(U, t, x) + sp.diff(U, x, 2) - sp.diff(U, x)
PUs = sp.series(sp.expand(PU), t, 0, 6).removeO()
low = sp.Poly(sp.expand(PUs), t)
okk = all(sp.expand(sp.series(cf, x, 0, 25).removeO()) == 0 for cf in [PUs.coeff(t, k) for k in range(6)])
check("D3 ricorrenza u_k = -sum p_l(d_x)u_{k-m+l}: P(d)U = 0 (ordini t^0..t^5, x^0..x^24)", okk)
check("D4 getti in 0 razionali (lambda in Q)", all(sp.diff(U, t, i, x, j).subs({t: 0, x: 0}).is_rational for i in range(4) for j in range(4)))
# crescita a_k <= C^k: somma dei |gamma_{k,i}|
def coeffs(k):
    # rappresenta u_k come polinomio in D (u_k = q_k(D) g), q_0 = 1, q_1 = 2
    return None
D = sp.symbols('D')
q = [sp.Integer(1), sp.Integer(2)]
for k in range(2, 30):
    q.append(sp.expand(-((D**2 - D)*q[k-2] - 2*D*q[k-1])))
a_k = [sum(abs(cf) for cf in sp.Poly(qq, D).all_coeffs()) for qq in q]
ratios = [float(a_k[k+1]/a_k[k]) for k in range(10, 28)]
check("D5 a_k cresce al piu' geometricamente (rapporti limitati)", max(ratios) < 10, round(max(ratios), 3))

# ---------------- E. OPR2-P4 (Gelfand–Dickey, Novikov integrato) ----------------
uu = sp.Function('u')(x)
def GD(nmax):
    Rs = [sp.Rational(1, 2)]
    for n_ in range(nmax):
        rhs_ = sp.diff(Rs[-1], x, 3) + 4*uu*sp.diff(Rs[-1], x) + 2*sp.diff(uu, x)*Rs[-1]
        # integrazione nell'algebra differenziale: si cerca R con dR = rhs_ via ansatz su monomi di peso giusto
        Rs.append(integrate_diff(rhs_, 2*(n_+1)))
    return Rs
ysy = sp.symbols('y0:12')
def to_y(expr):
    rep = {sp.diff(uu, x, j): ysy[j] for j in range(11, 0, -1)}
    return sp.expand(expr.subs(rep).subs(uu, ysy[0]))
def from_y(p):
    return p.subs({ysy[j]: sp.diff(uu, x, j) for j in range(12)})
def weight_monomials(W):
    out = []
    def rec(j, rem, cur):
        if rem == 0: out.append(cur); return
        if j > 11: return
        wj = j + 2
        k = 0
        while k*wj <= rem:
            rec(j+1, rem - k*wj, cur*ysy[j]**k); k += 1
    rec(0, W, sp.Integer(1)); return out
def integrate_diff(rhs_, W):
    mons = weight_monomials(W); cs = sp.symbols('k0:%d' % len(mons))
    cand = sum(ci*mi for ci, mi in zip(cs, mons))
    eqs = sp.Poly(sp.expand(to_y(sp.diff(from_y(cand), x)) - to_y(rhs_)), *ysy).coeffs()
    sol = sp.solve(eqs, cs, dict=True)[0]
    return from_y(cand.subs(sol).subs({ci: 0 for ci in cs}))
Rs = GD(4)
Ry = [to_y(R_) for R_ in Rs]
check("E1 R_1 = y0, R_2 = y2 + 3y0^2, R_3 = y4 + 10 y0 y2 + 5 y1^2 + 10 y0^3",
      Ry[1] == ysy[0] and Ry[2] == ysy[2] + 3*ysy[0]**2 and sp.expand(Ry[3] - (ysy[4] + 10*ysy[0]*ysy[2] + 5*ysy[1]**2 + 10*ysy[0]**3)) == 0)
cn = [sp.Poly(Ry[n_], *ysy).coeff_monomial(ysy[0]**n_) for n_ in range(1, 5)]
check("E2 coefficiente di y0^n in R_n: c_{n+1} = (4n+2)c_n/(n+1) (1,3,10,35) — deg R_n = n", cn == [1, 3, 10, 35], cn)
# N = 2 solitone k = (1,2): u = 2 D^2 log f, f = 1 + E1 + E2 + A12 E1 E2
k1, k2 = 1, 2
E1 = sp.exp(k1*x); E2 = sp.exp(k2*x); A12 = sp.Rational((k1-k2)**2, (k1+k2)**2)
fN = 1 + E1 + E2 + A12*E1*E2
u2 = 2*sp.diff(sp.log(fN), x, 2)
def evalR(Rexpr, ufun):
    return Rexpr.subs({sp.diff(uu, x, j): sp.diff(ufun, x, j) for j in range(8, 0, -1)}).subs(uu, ufun)
p2 = Rs[3] - 5*Rs[2] + 4*Rs[1]
vals = [abs(sp.N(evalR(p2, u2).subs(x, xv), 30)) for xv in [sp.Rational(-13,10), sp.Rational(1,5), sp.Rational(9,10), sp.Rational(5,2)]]
check("E3 N=2, k=(1,2): R_3 - 5R_2 + 4R_1 = 0 sul 2-solitone (c_j = (-1)^{N-j} e_{N-j}(k^2))", max(vals) < 1e-20, max(vals))
u1 = 2*sp.diff(sp.log(1+sp.exp(x)), x, 2)
vals = [abs(sp.N(evalR(Rs[2] - 1*Rs[1], u1).subs(x, xv), 30)) for xv in [sp.Integer(-1), sp.Rational(3,10), sp.Integer(2)]]
check("E4 N=1, k=1: R_2 - k^2 R_1 = 0", max(vals) < 1e-25)
check("E5 deg p_2 = 3, ordine 4, y4 con coefficiente 1", sp.Poly(to_y(p2), *ysy).total_degree() == 3 and sp.Poly(to_y(p2), *ysy).coeff_monomial(ysy[4]) == 1)

# ---------------- F. OPR2-L5 / OPR2-T5 ----------------
a_, tt = sp.symbols('a t', real=True)
u0 = sp.Function('u0')
J = 1 + tt*u0(a_).diff(a_)
u2_, u3_ = u0(a_).diff(a_, 2), u0(a_).diff(a_, 3)
dd = J**-1*(-tt*u3_*(1+J)/(2*J**2) + tt**2*u2_**2*(2+J)/(2*J**3))
check("F1 OPR2-L5: d/dt(delta_d J) = -u0'''/J^3 + 3t u0''^2/J^4", sp.simplify(sp.diff(dd*J, tt) - (-u3_/J**3 + 3*tt*u2_**2/J**4)) == 0)
check("F2 OPR2-L5: delta_d(0) = 0", sp.simplify(dd.subs(tt, 0)) == 0)
# v_xxx in lagrangiane: v = u0(a), x = a + t u0(a)
vfun = u0(a_); dx = lambda F_: sp.diff(F_, a_)/J
check("F3 v_xxx = u0'''/J^4 - 3t u0''^2/J^5", sp.simplify(dx(dx(dx(vfun))) - (u3_/J**4 - 3*tt*u2_**2/J**5)) == 0)
# equazione per w: calcolo simbolico con funzioni generiche
X = sp.symbols('X'); T_ = sp.symbols('T')
nu, dpar = sp.symbols('nu d')
V, Dl, Dd, W = [sp.Function(nm)(T_, X) for nm in ['V', 'Dl', 'Dd', 'W']]
E_ = W + nu*Dl + dpar*Dd   # e = w + nu delta + d delta_d
Lop = lambda F_: sp.diff(F_, T_) + sp.diff(V*F_, X) - nu*sp.diff(F_, X, 2) + dpar*sp.diff(F_, X, 3)
eq_e = Lop(E_) + E_*sp.diff(E_, X) - (nu*sp.diff(V, X, 2) - dpar*sp.diff(V, X, 3))   # = 0
subs_d = {sp.diff(Dl, T_): -sp.diff(V*Dl, X) + sp.diff(V, X, 2), sp.diff(Dd, T_): -sp.diff(V*Dd, X) - sp.diff(V, X, 3)}
expr = sp.expand(eq_e.subs(subs_d))
f_claim = nu**2*sp.diff(Dl, X, 2) + nu*dpar*(sp.diff(Dd, X, 2) - sp.diff(Dl, X, 3)) - dpar**2*sp.diff(Dd, X, 3) - E_*sp.diff(E_, X)
check("F4 w_t + (vw)_x - nu w_xx + d w_xxx = f (forma di f del Passo 2)", sp.simplify(expr - (Lop(W) - f_claim)) == 0)
# antisimmetria e dissipazione su T (Fourier): int d^3 e * e = 0, int e_xx e = -||e_x||^2
th_ = sp.symbols('th', real=True)
ef = sp.cos(th_) + 3*sp.sin(2*th_) - sp.cos(5*th_)/2
check("F5 int_T e''' e = 0 ; int_T e'' e = -int e'^2",
      sp.integrate(sp.diff(ef, th_, 3)*ef, (th_, 0, 2*sp.pi)) == 0 and sp.simplify(sp.integrate(sp.diff(ef, th_, 2)*ef + sp.diff(ef, th_)**2, (th_, 0, 2*sp.pi))) == 0)
check("F6 int v (d^j e)_x d^j e = -1/2 int v_x (d^j e)^2 (per parti su T)",
      sp.simplify(sp.integrate((sp.sin(th_)+2)*sp.diff(ef, th_)*ef + sp.Rational(1, 2)*sp.cos(th_)*ef**2, (th_, 0, 2*sp.pi))) == 0)
# trucco (Y+eta)^{1/2}: Y' <= C(1+sqrt Y)Y + 2g sqrt Y  ⇒  Z' <= C Z + g  (Z = sqrt(Y+eta), sqrt Y <= 1)
ok = True
random.seed(3)
for _ in range(20000):
    Yv = random.random(); et = 10**random.uniform(-12, 0); Cv = random.uniform(0, 5); gv = random.uniform(0, 5)
    Zv = math.sqrt(Yv + et)
    Yp = Cv*(1+math.sqrt(Yv))*Yv + 2*gv*math.sqrt(Yv)
    ok &= Yp/(2*Zv) <= Cv*Zv + gv + 1e-12
check("F7 (domanda 4) Z = (Y+eta)^{1/2}: Z' = Y'/(2Z) <= C Z + g se sqrt Y <= 1; Z(0) = sqrt eta -> 0", ok)
thv = sp.symbols('thv', real=True)
ok = True
for v_ in [0.01, 0.5, 1, 3, 10, 100]:
    ok &= abs(math.e**(-v_) - 1 + v_) <= v_**2/2 + 1e-15 and abs(complex(math.cos(v_), math.sin(v_)) - 1 - 1j*v_) <= v_**2/2 + 1e-12
check("F8 |e^{-y}-1+y| <= y^2/2, |e^{iy}-1-iy| <= y^2/2", ok)
# (LWP): il generatore nu d^2 - d d^3 NON e' settoriale (arg lambda_n -> pi/2): Pazy §6.3 / Henry cap.3 non si applicano per d != 0
nuv, dv = 0.01, 1.0
args = [math.atan2(dv*n_**3, -nuv*n_**2) for n_ in [1, 10, 100, 1000, 10**4]]
check("F9 (rilievo T5-1) spettro -nu n^2 + i d n^3: arg -> pi/2 (nessun settore d'angolo < pi/2 attorno al semiasse negativo)",
      abs(args[-1] - math.pi/2) < 1e-5 and all(abs(math.exp(-nuv*n_**2*1.0)) <= 1 for n_ in range(50)), [round(a__, 6) for a__ in args])
# smoothing comunque disponibile: sup_n n e^{-nu t n^2} <= C (nu t)^{-1/2}
ok = all(max(n_*math.exp(-0.01*tv*n_**2) for n_ in range(1, 4000)) <= (0.01*tv)**-0.5 for tv in [0.01, 0.1, 1, 10])
check("F10 lisciamento: ||d_x S(t)|| <= (nu t)^{-1/2} (modulo del moltiplicatore e^{-nu t n^2})", ok)

# ---------------- G. OPR2-P6 / O8 / O9 ----------------
U_ = sp.symbols('U'); phi = sp.Function('phi')(U_); cfun = sp.Function('cf')(U_)
# u_x = phi(u), u_t = c(u) u_x: compatibilita' (u_x)_t - (u_t)_x
ux = phi; ut = cfun*phi
uxt = sp.diff(phi, U_)*ut
utx = sp.diff(ut, U_)*ux
check("G1 (OPR2-P6) compatibilita': (u_x)_t - (u_t)_x = -c'(u) phi(u)^2", sp.simplify(uxt - utx + sp.diff(cfun, U_)*phi**2) == 0)
al, be, cc0 = sp.symbols('alpha beta c0')
g_ = sp.Function('g')(x)
# beta g'' + alpha/2 g^2 + c g = 0 ⇒ (beta g'^2 + alpha/3 g^3 + c g^2)' = 2 g'(...)
check("G2 (OPR2-P6) integrale primo: d/dx(beta g'^2 + alpha/3 g^3 + c g^2) = 2g'(beta g'' + alpha/2 g^2 + c g)",
      sp.simplify(sp.diff(be*g_.diff(x)**2 + al/3*g_**3 + cc0*g_**2, x) - 2*g_.diff(x)*(be*g_.diff(x, 2) + al/2*g_**2 + cc0*g_)) == 0)
# O8: relazione autonoma per soluzioni autosimili di KdV u_t + 6uu_x + u_xxx = 0
Y0 = sp.symbols('Y0:7')
uF = sp.Function('uF')(x)
Wf = 6*uF*uF.diff(x) + uF.diff(x, 3)
expr = sp.diff((1 + sp.diff(2*uF/uF.diff(x), x))/sp.diff(Wf/uF.diff(x), x), x)
num = sp.numer(sp.together(expr))
def to_Y(e_):
    rep = {uF.diff(x, j): Y0[j] for j in range(6, 0, -1)}
    return sp.expand(e_.subs(rep).subs(uF, Y0[0]))
Rnum = to_Y(num)
check("G3 (OPR2-O8) R ≠ 0 e d'ordine 5", Rnum != 0 and Rnum.has(Y0[5]) and not Rnum.has(Y0[6]))
# verifica su una soluzione autosimile numerica: f''' = 2f + z f' - 6 f f' (u = (3t)^{-2/3} f(x (3t)^{-1/3}))
mp.mp.dps = 30
def fode(zv, Yv): return [Yv[1], Yv[2], 2*Yv[0] + zv*Yv[1] - 6*Yv[0]*Yv[1]]
sol = mp.odefun(fode, 0, [mp.mpf('0.3'), mp.mpf('-0.2'), mp.mpf('0.1')])
tv = mp.mpf('0.7'); xv = mp.mpf('0.4')
def ufun(T__, X__):
    return (3*T__)**(-mp.mpf(2)/3)*sol(X__*(3*T__)**(-mp.mpf(1)/3))[0]
jets = [mp.diff(lambda X__: ufun(tv, X__), xv, j) for j in range(6)]
Rval = sp.N(Rnum.subs({Y0[j]: sp.Float(str(jets[j]), 25) for j in range(6)}), 20)
scale = sum(abs(sp.N(tm.subs({Y0[j]: sp.Float(str(jets[j]), 25) for j in range(6)}), 20)) for tm in Rnum.as_ordered_terms())
check("G4 (OPR2-O8) R si annulla (rel.) sul getto di una soluzione autosimile numerica", abs(Rval)/scale < 1e-12, float(abs(Rval)/scale))
# O9: y1^2 - k^2 y0^2 ∈ I_PW ?  I_PW = ker(Phi*), Phi(alpha,beta,c) = (alpha, beta, c alpha, c beta, ...)
k = sp.symbols('k', positive=True); alpha, beta, cP = sp.symbols('alpha beta cP')
Phi = {ysy[0]: alpha, ysy[1]: beta, ysy[2]: cP*alpha, ysy[3]: cP*beta, ysy[4]: cP**2*alpha}
low9 = ysy[1]**2 - k**2*ysy[0]**2
check("G5 (RILIEVO O9-1) y1^2 - k^2 y0^2 NON sta in I_PW (Phi*: beta^2 - k^2 alpha^2 ≠ 0)", sp.expand(low9.subs(Phi)) != 0, sp.expand(low9.subs(Phi)))
# sul getto di cosh(kx) (soluzione di v'' = k^2 v): vale -k^2
vch = sp.cosh(k*x)
check("G6 (RILIEVO O9-1) su v = cosh(kx), v''=k^2 v: y1^2 - k^2 y0^2 = -k^2 ≠ 0", sp.simplify((vch.diff(x)**2 - k**2*vch**2)) == -k**2)
# riparazione: p' = y0 y3 - y1 y2 + 3 y0^2 y1
pp = ysy[0]*ysy[3] - ysy[1]*ysy[2] + 3*ysy[0]**2*ysy[1]
sol1 = k**2/2*sp.sech(k*x/2)**2
jet1 = {ysy[j]: sol1.diff(x, j) for j in range(4)}
check("G7 (O9′) p' = y0y3 - y1y2 + 3y0^2y1 si annulla sul solitone (ogni k)", sp.simplify(pp.subs(jet1).rewrite(sp.exp)) == 0)
check("G8 (O9′) componente omogenea minima y0y3 - y1y2 ∈ I_PW (minore)", sp.expand((ysy[0]*ysy[3] - ysy[1]*ysy[2]).subs(Phi)) == 0)
fl = sp.factor_list(pp, *ysy[:4])
check("G9 (O9′) p' irriducibile su Q (e su C: lineare in y3, coefficienti coprimi)", len(fl[1]) == 1 and fl[1][0][1] == 1 and sp.gcd(ysy[0], sp.expand(pp - ysy[0]*ysy[3])) == 1)
check("G10 (O9′) p' non ha parte lineare; ordine 3 >= 2 (coerente con OPR2-P6)", all(sp.Poly(m_, *ysy).total_degree() >= 2 for m_ in pp.as_ordered_terms()))
# controllo: Pi_1 + y0 D(Pi_1) di OP-R2 si annulla sul solitone (vero) — il difetto e' solo l'appartenenza a I_PW
Pi1 = ysy[1]**2 - k**2*ysy[0]**2 + 2*ysy[0]**3
jet2 = {ysy[j]: sol1.diff(x, j) for j in range(3)}
DPi1 = 2*ysy[1]*ysy[2] - 2*k**2*ysy[0]*ysy[1] + 6*ysy[0]**2*ysy[1]
check("G11 p = Pi1 + y0 D(Pi1) si annulla sul solitone (parte corretta di O9)", sp.simplify((Pi1 + ysy[0]*DPi1).subs(jet2).rewrite(sp.exp)) == 0)

print()
nok = sum(1 for _, o in RES if o)
print(f"ESITO: {nok}/{len(RES)} OK")
