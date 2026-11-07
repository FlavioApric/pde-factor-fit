# OP-R2 -- controlli SymPy (solo CONTROLLO, non metodo). Eseguire con:
#   D:\ProblemaBase\.venv\Scripts\python.exe -I work/OP-R2/sympy/opr2_checks.py
import sympy as sp
from sympy import Rational as Q
import random

RESULTS = []
def check(name, ok, info=""):
    RESULTS.append((name, bool(ok)))
    print(("OK  " if ok else "FAIL") + "  " + name + ("  -- " + info if info else ""))

t, x, s, h, k, c, T = sp.symbols('t x s h k c T', real=True)

# ---------------- A. OPF-Q1 (calore x trasporto) ----------------
th = sp.Function('theta')(t, x); w = sp.Function('w')(t, x)
H = lambda f: sp.diff(f, t) - sp.diff(f, x, 2)
lhs = H(th*w) - th*H(w)
rhs = (sp.diff(th, t) + sp.diff(th, x, 2))*w - 2*sp.diff(sp.diff(th, x)*w, x)
check("A1 commutatore [H,theta]w = (th_t+th_xx)w - 2 d_x(th_x w)", sp.simplify(sp.expand(lhs - rhs)) == 0)
# A2 shift della variabile caratteristica s = x - c t sotto y -> y + (h, -k)
sfun = lambda tt, xx: xx - c*tt
check("A2 s(y+(h,-k)) = s - (k + c h)", sp.simplify(sfun(t+h, x-k) - (sfun(t, x) - (k + c*h))) == 0)
# A3 norme L^1 dei nuclei di Duhamel
xi = sp.symbols('xi', positive=True)
I0 = sp.integrate(sp.exp(-t*xi**2), (t, 0, T))
I1 = sp.integrate(xi*sp.exp(-t*xi**2), (t, 0, T))
check("A3a int_0^T e^{-t xi^2} dt = (1-e^{-T xi^2})/xi^2", sp.simplify(I0 - (1 - sp.exp(-T*xi**2))/xi**2) == 0)
check("A3b int_0^T xi e^{-t xi^2} dt = (1-e^{-T xi^2})/xi", sp.simplify(I1 - (1 - sp.exp(-T*xi**2))/xi) == 0)
ok = True
for Tv in [Q(1,10), 1, 3, 10]:
    for xv in [Q(1,100), Q(1,10), Q(1,3), 1, 2, 7, 50]:
        val = (1 - sp.exp(-Tv*xv**2))/xv
        ok &= bool(sp.N(val) <= sp.N(sp.sqrt(Tv)) + 1e-15) and bool(sp.N((1 - sp.exp(-Tv*xv**2))/xv**2) <= Tv)
check("A3c (1-e^{-T xi^2})/xi <= sqrt(T) e (1-e^{-T xi^2})/xi^2 <= T su una griglia", ok)

# ---------------- B. OPF-Q2 (trasporti: integrale di Hilbert-Schmidt) ----------------
# rettangolo (0,1)x(0,1) in (t,x); direzione v = d_t (corde verticali di lunghezza 1), w = d_t + d_x (corde lungo s = x - t)
ss = sp.symbols('s', real=True)
# lunghezza (in parametro t) della corda {x - t = s} nel quadrato: s in (-1,1), ell(s) = 1 - |s|
# s in (-1,0): t in (-s,1), ell = 1+s ; s in (0,1): t in (0,1-s), ell = 1-s
HS = sp.integrate(sp.integrate(1/(1+ss), (t, -ss, 1)), (ss, -1, 0)) + sp.integrate(sp.integrate(1/(1-ss), (t, 0, 1-ss)), (ss, 0, 1))
check("B1 int_Omega dz/(ell_v ell_w) finito sul quadrato (ell_v = 1)", sp.simplify(HS - 2) == 0, "valore = %s" % sp.simplify(HS))
a, eps, l1, l2 = sp.symbols('a epsilon lambda1 lambda2', positive=True)
wedge = sp.integrate(sp.integrate(1/(a*(sp.Symbol('b'))), (sp.Symbol('b'), l1*a, l2*a)), (a, eps, 1))
check("B2 cuneo: int da db/(ab) = log(l2/l1) log(1/eps) (diverge)", sp.simplify(wedge - sp.log(l2/l1)*sp.log(1/eps)) == 0)
# B3 Gram 2x2 di {1, e^t} su corda di lunghezza L: det > 0 e nucleo del proiettore limitato per L >= L0
L, al = sp.symbols('L alpha', positive=True)
G = sp.Matrix([[sp.integrate(1, (t, al, al+L)), sp.integrate(sp.exp(t), (t, al, al+L))],
               [sp.integrate(sp.exp(t), (t, al, al+L)), sp.integrate(sp.exp(2*t), (t, al, al+L))]])
detG = sp.simplify(G.det())
ok = all(sp.N(detG.subs({L: Lv, al: av})) > 0 for Lv in [Q(1,10), Q(1,2), 1, 2] for av in [-2, 0, 1])
check("B3 det Gram{1,e^t} > 0 su corde di lunghezza positiva", ok)

# ---------------- C. OP-ALG-Q2 (P4-L7 globale) ----------------
n = sp.symbols('n', integer=True, nonnegative=True)
N_ = 40
gx = sum(x**j/sp.factorial(j)**2 for j in range(N_))
# C1 indipendenza lineare di g, g', ..., g^(K): matrice dei coefficienti di x^n, n = 0..K
Kd = 7
M = sp.Matrix([[sp.Poly(sp.diff(gx, x, i), x).coeff_monomial(x**nn) for i in range(Kd+1)] for nn in range(Kd+1)])
check("C1 g = sum x^n/(n!)^2: g, ..., g^(7) linearmente indipendenti (rango 8)", M.rank() == Kd+1)
# C2 serie globale per un P in forma di Kovalevskaya: P = tau^2 - xi^2 + xi (p1 = 0, p0 = -xi^2 + xi)
lam0, lam1 = Q(1), Q(2)
U = {0: lam0*gx, 1: lam1*gx}
for kk in range(2, 12):
    # u_k = -p1(d)u_{k-1} - p0(d) u_{k-2} = (d^2 - d) u_{k-2}
    U[kk] = sp.expand(sp.diff(U[kk-2], x, 2) - sp.diff(U[kk-2], x))
useries = sum(t**kk/sp.factorial(kk)*U[kk] for kk in range(12))
res = sp.expand(sp.diff(useries, t, 2) - sp.diff(useries, x, 2) + sp.diff(useries, x))
# il residuo deve contenere solo potenze t^k con k >= 10
lowres = [sp.expand(res.coeff(t, j)) for j in range(10)]
check("C2 ricorrenza di Kovalevskaya: residuo P(d)u_trunc = O(t^10)", all(r == 0 for r in lowres))
# C3 crescita: |u_k(z)| <= C^k e^{2 sqrt R}: controllo numerico su |z| = 4
ok = True
for kk in range(12):
    val = abs(sp.N(U[kk].subs(x, 4)))
    ok &= val <= (3**kk)*float(sp.N(sp.exp(2*sp.sqrt(4))))*2 + 1e-9
check("C3 |u_k(4)| <= 2*3^k e^{2 sqrt 4} per k <= 11 (C = 3 basta: a_k <= 2 a_{k-2}... )", ok)
# C4 jet razionali
check("C4 getti in 0 razionali", all(sp.diff(U[kk], x, b).subs(x, 0).is_rational for kk in range(6) for b in range(4)))

# ---------------- D. delta_N(2N) <= N+1 (Novikov integrato) ----------------
y = sp.symbols('y0:9')
def Dtot(p, kmax=8):
    return sum(sp.diff(p, y[j])*y[j+1] for j in range(kmax))
# polinomi di Gelfand-Dickey per u_t = u_xxx + 6 u u_x: d R_{n+1} = (d^3 + 4u d + 2u_x) R_n, R_0 = 1/2
def next_R(Rn, wt):
    target = sp.expand(Dtot(Dtot(Dtot(Rn))) + 4*y[0]*Dtot(Rn) + 2*y[1]*Rn)
    # ansatz: polinomio quasi-omogeneo di peso wt (peso y_j = j+2)
    mons = [m for m in sp.itermonomials(y[:7], wt//2+1) if sp.Poly(m, *y[:7]).total_degree() >= 0]
    def weight(m):
        p = sp.Poly(m, *y[:7]); return sum((j+2)*e for j, e in enumerate(p.monoms()[0]))
    mons = [m for m in mons if m != 1 and weight(m) == wt]
    cs = sp.symbols('c0:%d' % len(mons))
    R = sum(ci*mi for ci, mi in zip(cs, mons))
    eqs = sp.Poly(sp.expand(Dtot(R) - target), *y[:8]).coeffs()
    sol = sp.solve(eqs, cs, dict=True)[0]
    return sp.expand(R.subs(sol).subs({ci: 0 for ci in cs}))
R1 = y[0]
R2 = next_R(R1, 4); R3 = next_R(R2, 6); R4 = next_R(R3, 8)
check("D0 R2 = y2 + 3y0^2", sp.expand(R2 - (y[2] + 3*y[0]**2)) == 0, str(R2))
check("D0' R3 = y4 + 10y0y2 + 5y1^2 + 10y0^3", sp.expand(R3 - (y[4] + 10*y[0]*y[2] + 5*y[1]**2 + 10*y[0]**3)) == 0, str(R3))
def soliton_jets(ks, Xvals, order):
    Xs = sp.symbols('X1:%d' % (len(ks)+1))
    def A(i, j): return ((ks[i]-ks[j])/(ks[i]+ks[j]))**2
    import itertools
    f = 0
    for r in range(len(ks)+1):
        for S in itertools.combinations(range(len(ks)), r):
            aS = 1
            for i, j in itertools.combinations(S, 2): aS *= A(i, j)
            term = aS
            for i in S: term *= Xs[i]
            f += term
    Dop = lambda g: sum(ks[i]*Xs[i]*sp.diff(g, Xs[i]) for i in range(len(ks)))
    lf = sp.log(f)
    u = 2*Dop(Dop(lf))
    jets = [u]
    for _ in range(order):
        jets.append(Dop(jets[-1]))
    return [[sp.cancel(jj.subs(dict(zip(Xs, Xv)))) for jj in jets] for Xv in Xvals]
# N = 1
ks = [Q(1)]
pts = [[Q(1,2)], [Q(3)], [Q(7,5)]]
J1 = soliton_jets(ks, pts, 2)
okN1 = all(sp.simplify(jt[2] + 3*jt[0]**2 - ks[0]**2*jt[0]) == 0 for jt in J1)
check("D1 N=1: R2 - k^2 R1 = 0 sul solitone (ordine 2 = 2N, grado 2 = N+1)", okN1)
# N = 2, k = (1,2): cerco c1, c0 con R3 + c1 R2 + c0 R1 = 0
ks = [Q(1), Q(2)]
random.seed(1)
pts = [[Q(random.randint(1, 9), random.randint(1, 9)) for _ in range(2)] for _ in range(6)]
J2 = soliton_jets(ks, pts, 4)
c1, c0 = sp.symbols('c1 c0')
G2 = lambda jt: (R3 + c1*R2 + c0*R1).subs({y[i]: jt[i] for i in range(5)})
sol = sp.solve([G2(J2[0]), G2(J2[1])], [c1, c0], dict=True)
okN2 = bool(sol) and all(sp.simplify(G2(jt).subs(sol[0])) == 0 for jt in J2[2:])
check("D2 N=2 k=(1,2): R3 + c1 R2 + c0 R1 = 0 (ordine 4 = 2N, grado 3 = N+1)", okN2, str(sol))
# N = 3, k = (1,2,3): controllo NUMERICO ad alta precisione (50 cifre), u(x) = 2 (log f)'' con X_i = c_i e^{k_i x}
import mpmath as mp
mp.mp.dps = 60
kv = [1, 2, 3]; cv = [mp.mpf('0.7'), mp.mpf('1.3'), mp.mpf('0.4')]
def Aij(i, j): return ((mp.mpf(kv[i]) - kv[j])/(kv[i] + kv[j]))**2
import itertools
def fx(xx):
    tot = 0
    for r in range(4):
        for S in itertools.combinations(range(3), r):
            term = mp.mpf(1)
            for i, j in itertools.combinations(S, 2): term *= Aij(i, j)
            for i in S: term *= cv[i]*mp.e**(kv[i]*xx)
            tot += term
    return tot
def ujets(xx, order=6):
    return [2*mp.diff(lambda z: mp.log(fx(z)), xx, n+2) for n in range(order+1)]
R4f = sp.lambdify(y[:7], R4, 'mpmath'); R3f = sp.lambdify(y[:7], R3, 'mpmath')
R2f = sp.lambdify(y[:7], R2, 'mpmath'); R1f = sp.lambdify(y[:7], R1, 'mpmath')
xs = [mp.mpf(v) for v in ['-0.9', '-0.2', '0.35', '0.8', '1.4']]
rows = []; rhs_ = []
for xx in xs:
    jt = ujets(xx)
    rows.append([R3f(*jt), R2f(*jt), R1f(*jt)]); rhs_.append(-R4f(*jt))
Mm = mp.matrix(rows[:3]); bb = mp.matrix(rhs_[:3])
dsol = mp.lu_solve(Mm, bb)
resid = max(abs(sum(rows[i][j]*dsol[j] for j in range(3)) - rhs_[i]) for i in range(3, 5))
check("D3 N=3 k=(1,2,3): R4 + d2 R3 + d1 R2 + d0 R1 = 0 (ordine 6, grado 4) [V-ex numerico 60 cifre]",
      resid < mp.mpf('1e-30'), "d = %s, residuo %s" % ([mp.nstr(v, 12) for v in dsol], mp.nstr(resid, 3)))

# ---------------- E. S4T-Q2 (KdV-Burgers) ----------------
aa, tt = sp.symbols('a t', real=True)
u0 = sp.Function('u0')
Jj = 1 + tt*sp.diff(u0(aa), aa)
dx = lambda F: sp.diff(F, aa)/Jj          # d/dx in coordinate lagrangiane a tempo fisso
vx = dx(u0(aa)); vxx = dx(vx); vxxx = dx(vxx)
p1, p2, p3 = [sp.diff(u0(aa), aa, j) for j in (1, 2, 3)]
check("E1 v_xx = u0''/J^3", sp.simplify(vxx - p2/Jj**3) == 0)
check("E1' v_xxx = u0'''/J^4 - 3 t u0''^2/J^5", sp.simplify(vxxx - (p3/Jj**4 - 3*tt*p2**2/Jj**5)) == 0)
deltad = (1/Jj)*(-tt*p3*(1+Jj)/(2*Jj**2) + tt**2*p2**2*(2+Jj)/(2*Jj**3))
# d/dt (delta_d J) a "a" fissato deve valere -J v_xxx
lhsE = sp.diff(deltad*Jj, tt)
check("E2 d/dt(delta_d J) = -J v_xxx (forma chiusa di delta_d) e delta_d(0) = 0",
      sp.simplify(lhsE + Jj*vxxx) == 0 and sp.simplify(deltad.subs(tt, 0)) == 0)
# E3 algebra dell'equazione per w = e - nu delta - d delta_d (simboli astratti)
nu, dd = sp.symbols('nu d', real=True)
U_, V_, Dl, Dd = [sp.Function(nm)(t, x) for nm in ('u', 'v', 'delta', 'deltad')]
ut = nu*sp.diff(U_, x, 2) - dd*sp.diff(U_, x, 3) - U_*sp.diff(U_, x)
vt = -V_*sp.diff(V_, x)
Dlt = -sp.diff(V_*Dl, x) + sp.diff(V_, x, 2)
Ddt = -sp.diff(V_*Dd, x) - sp.diff(V_, x, 3)
E_ = U_ - V_; W_ = E_ - nu*Dl - dd*Dd
Wt = ut - vt - nu*Dlt - dd*Ddt
LHS = Wt + sp.diff(V_*W_, x) - nu*sp.diff(W_, x, 2) + dd*sp.diff(W_, x, 3)
RHS = nu**2*sp.diff(Dl, x, 2) + nu*dd*(sp.diff(Dd, x, 2) - sp.diff(Dl, x, 3)) - dd**2*sp.diff(Dd, x, 3) - E_*sp.diff(E_, x)
check("E3 w_t + (v w)_x - nu w_xx + d w_xxx = nu^2 delta_xx + nu d(deltad_xx - delta_xxx) - d^2 deltad_xxx - e e_x",
      sp.simplify(sp.expand(LHS - RHS)) == 0)
# E4 identita' d'energia su T (polinomi trigonometrici)
Wtr = 3*sp.sin(x) - sp.cos(2*x) + Q(1,2)*sp.sin(3*x); Vtr = 1 + sp.cos(x) + sp.sin(2*x)
i1 = sp.integrate(Wtr*sp.diff(Wtr, x, 3), (x, 0, 2*sp.pi))
i2 = sp.integrate(sp.diff(Vtr*Wtr, x)*Wtr - Q(1,2)*sp.diff(Vtr, x)*Wtr**2, (x, 0, 2*sp.pi))
check("E4 int w w_xxx = 0 e int (v w)_x w = 1/2 int v_x w^2 su T", sp.simplify(i1) == 0 and sp.simplify(i2) == 0)
# E5 resto di Taylor del gruppo di Airy: |e^{i th} - 1 - i th| <= th^2/2
ok = all(abs(complex(sp.N(sp.exp(sp.I*v) - 1 - sp.I*v))) <= v**2/2 + 1e-15 for v in [0.01, 0.3, 1.0, 2.5, 7.0, 40.0])
check("E5 |e^{i th}-1-i th| <= th^2/2", ok)

# ---------------- F. INT-Q1 ----------------
U0 = sp.symbols('U')
phi = sp.Function('phi')(U0); cf = sp.Function('cc')(U0)
# u_x = phi(u), u_t = c(u) u_x  =>  (u_x)_t - (u_t)_x = phi' c phi - (c' phi^2 + c phi' phi) = -c' phi^2
compat = sp.diff(phi, U0)*cf*phi - (sp.diff(cf, U0)*phi**2 + cf*sp.diff(phi, U0)*phi)
check("F1 compatibilita' ordine 1: (u_x)_t - (u_t)_x = -c'(u) phi(u)^2", sp.simplify(compat + sp.diff(cf, U0)*phi**2) == 0)
# F2 relazione autonoma delle soluzioni autosimili di KdV u_t + 6uu_x + u_xxx = 0
# x = [3t(6uu_x+u_xxx) - 2u]/u_x ;  1 = 3t*d_x(A/u_x) - d_x(2u/u_x), A = 6uu_x + u_xxx ; 3t = (1 + d_x(2u/u_x))/d_x(A/u_x)
def Dx(p): return sum(sp.diff(p, y[j])*y[j+1] for j in range(8))
A_ = 6*y[0]*y[1] + y[3]
B1 = Dx(A_/y[1]); B2 = Dx(2*y[0]/y[1])
Rss = sp.together(Dx((1 + B2)/B1))
num = sp.factor(sp.numer(Rss))
check("F2a relazione autosimile: numeratore polinomio non nullo d'ordine 5", num != 0 and sp.Poly(num, *y[:8]).degree(y[5]) >= 1, "grado totale %d" % sp.Poly(num, *y[:8]).total_degree())
# verifica sull'ansatz u = (3t)^(-2/3) f(z), z = x (3t)^(-1/3), con f''' = 2f + z f' - 6 f f'
z = sp.symbols('z'); F0, F1, F2 = sp.symbols('F0 F1 F2')
fj = [F0, F1, F2]
def Dz(expr):
    # derivata in z di un polinomio in z, F0, F1, F2 con F2' = 2F0 + z F1 - 6 F0 F1
    return sp.diff(expr, z) + sp.diff(expr, F0)*F1 + sp.diff(expr, F1)*F2 + sp.diff(expr, F2)*(2*F0 + z*F1 - 6*F0*F1)
tau3 = sp.symbols('tau3', positive=True)   # tau3 = (3t)^(1/3)
jets = []
g = F0
for j in range(7):
    jets.append(g*tau3**(-2-j))
    g = sp.expand(Dz(g))
val = sp.simplify(num.subs({y[j]: jets[j] for j in range(7)}))
check("F2b la relazione si annulla identicamente sulle soluzioni autosimili (Painleve)", val == 0)
# F3 p = Pi1 + y0*D(Pi1), Pi1 = y1^2 - k^2 y0^2 + 2 y0^3 (solitone u = (k^2/2) sech^2(kx/2))
kk_ = sp.symbols('k', positive=True)
Pi1 = y[1]**2 - kk_**2*y[0]**2 + 2*y[0]**3
pF = sp.expand(Pi1 + y[0]*Dx(Pi1))
usol = kk_**2/2*sp.sech(kk_*x/2)**2
sub = {y[j]: sp.diff(usol, x, j) for j in range(3)}
check("F3a Pi1 si annulla sul solitone e p = Pi1 + y0 D(Pi1) anche", sp.simplify(Pi1.subs(sub).rewrite(sp.exp)) == 0 and sp.simplify(pF.subs(sub).rewrite(sp.exp)) == 0)
check("F3b p irriducibile in Q(k)[y0,y1,y2]", len(sp.factor_list(pF, *y[:3])[1]) == 1 and sp.factor_list(pF, *y[:3])[1][0][1] == 1)
low = sp.expand(sum(term for term in sp.Add.make_args(pF) if sp.Poly(term, *y[:3]).total_degree() == 2))
check("F3c componente omogenea minima = y1^2 - k^2 y0^2 (in I_PW: si annulla su v''= k^2 v)", sp.expand(low - (y[1]**2 - kk_**2*y[0]**2)) == 0)

print()
print("TOTALE: %d/%d OK" % (sum(1 for _, o in RESULTS if o), len(RESULTS)))
