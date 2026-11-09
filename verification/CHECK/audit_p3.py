# audit_p3.py - S-CHECK-5: red team / verifiche indipendenti sui claim di S-P3
# Esecuzione: D:\ProblemaBase\.venv\Scripts\python.exe -I audit_p3.py > audit_p3.out
import sympy as sp, numpy as np, mpmath as mp, math

RES = []
def rep(tag, ok, info=""):
    RES.append((tag, bool(ok)))
    print(f"[{'OK' if ok else 'FAIL'}] {tag} {info}")

# ---------------------------------------------------------------- P3-T3 (i),(ii)
x = sp.symbols('x', real=True); L, c = sp.symbols('L c', positive=True)
ok = True
for m in range(1, 9):
    for n in range(1, 9):
        em = sp.sqrt(2/L)*sp.sin(m*sp.pi*x/L); en = sp.sqrt(2/L)*sp.sin(n*sp.pi*x/L)
        V = sp.simplify(sp.integrate(em*(-c*sp.diff(en, x)), (x, 0, L)))
        pred = -4*c*m*n/(L*(m**2-n**2)) if (m+n) % 2 == 1 else 0
        ok &= sp.simplify(V - pred) == 0
rep("T3(i) V_mn = -4cmn/(L(m^2-n^2)) (m+n dispari), 0 altrimenti, m,n<=8", ok)
n_ = sp.symbols('n', integer=True, positive=True)
rep("T3(ii) sin(n pi - mu_n x) = (-1)^(n+1) sin(mu_n x)",
    all(sp.simplify(sp.sin(k*sp.pi - k*sp.pi*x/L) - (-1)**(k+1)*sp.sin(k*sp.pi*x/L)) == 0 for k in range(1, 7)))

# T_nm closed form and g
t, s, kap = sp.symbols('t s kappa', positive=True)
a_, b_, y = sp.symbols('a b y', positive=True)
ok = True
for (n, m) in [(1, 2), (1, 4), (2, 5), (3, 6)]:
    ln, lm = -kap*n**2, -kap*m**2
    T = sp.integrate(sp.exp(lm*(t-s)+ln*s) - sp.exp(lm*t), (s, 0, t))
    g = sp.exp(-kap*n**2*t) - sp.exp(-kap*m**2*t)*(1+kap*m**2*t-kap*n**2*t)
    ok &= sp.simplify(T - g/(kap*(m**2-n**2))) == 0
rep("T3(2) T_nm = g(kn^2t,km^2t)/(k(m^2-n^2)), m>n", ok)
gint = sp.integrate(sp.exp(-y)*(y-a_), (y, a_, b_))
rep("T3(2) g(a,b) = int_a^b e^-y (y-a) dy", sp.simplify(gint - (sp.exp(-a_)-sp.exp(-b_)*(1+b_-a_))) == 0)

# exact modal series of E^{mult,(1)}(t) u0, L=c=D=1
Lv, cv, Dv = 1.0, 1.0, 1.0
kv = Dv*np.pi**2/Lv**2
def Tnm(tt, n, m):
    ln, lm = -kv*n**2, -kv*m**2
    w = tt*(ln-lm)
    out = np.empty(np.broadcast(n, m).shape)
    small = np.abs(w) < 1e-4
    with np.errstate(over='ignore', invalid='ignore'):
        big = (np.exp(ln*tt)-np.exp(lm*tt))/np.where(small, 1.0, ln-lm) - tt*np.exp(lm*tt)
    ser = tt*np.exp(lm*tt)*(w/2 + w**2/6 + w**3/24)
    out = np.where(small, ser, big)
    out = np.where(n == m, 0.0, out)
    return out
def Vmn(m, n):
    odd = ((m+n) % 2 == 1)
    return np.where(odd, -4*cv*m*n/(Lv*np.where(odd, (m**2-n**2), 1)), 0.0)
def Enorm(tt, cn, Mmax):
    N = len(cn); n = np.arange(1, N+1)[None, :]; m = np.arange(1, Mmax+1)[:, None]
    Em = (Vmn(m, n)*Tnm(tt, n, m)*np.asarray(cn)[None, :]).sum(axis=1)
    return np.sqrt((np.abs(Em)**2).sum())

# analytic asymptotics for u0=e1: ||E|| ~ 2|c| sqrt(J) kappa^{1/4} t^{5/4} / L
mp.mp.dps = 40
hy = lambda yy: yy**2*mp.quad(lambda u: u*mp.e**(-yy*u), [0, 1])   # h(y) = y^2 int_0^1 u e^{-yu} du, senza cancellazione
J = mp.quad(lambda yy: yy**(-3.5)*hy(yy)**2, [0, 1, 10, 100, mp.inf])
mp.mp.dps = 15
pred = lambda tt: 2*cv*float(mp.sqrt(J))*kv**0.25*tt**1.25/Lv
ts = [1e-3, 1e-4, 1e-5, 1e-6]
vals = [Enorm(tt, [1.0], 40000) for tt in ts]
ratios = [v/pred(tt) for v, tt in zip(vals, ts)]
slopes = [np.log(vals[i+1]/vals[i])/np.log(ts[i+1]/ts[i]) for i in range(len(ts)-1)]
print("   J =", mp.nstr(J, 10), " ratios ||E||/asintotica:", [f"{r:.5f}" for r in ratios], " pendenze:", [f"{q:.5f}" for q in slopes])
rep("T3(iii) e1: ||E||/(2|c|sqrt(J)k^{1/4}t^{5/4}/L) -> 1 (verifica dell'esponente analitico 5/4)", abs(ratios[-1]-1) < 2e-3)
lb = lambda tt: cv*1*kv**0.25*tt**1.25/(32*Lv)
tstar = min(1/(48*1*kv*1), 1/(4*kv), 1/(16*kv))
rep("T3(iii)(b) bound inferiore |c||S|k^{1/4}t^{5/4}/(32L) per t<=t_* (e1)", all(Enorm(tt, [1.0], 40000) >= lb(tt) for tt in [tstar, tstar/10, tstar/1000]), f"t_*={tstar:.3e}")
ub_ok = True
for cn in ([1.0], [1.0, 0.5, -0.3], [0.2, 1.0, 0.0, 0.7j]):
    N = len(cn); A = sum(k*abs(z) for k, z in enumerate(cn, 1))
    C1 = 4*cv*kv*N*A/Lv; C2 = 16*cv*A/(3*Lv)
    Cb = np.sqrt(2*N*C1**2 + C2**2*(kv**2/4+2))
    ub_ok &= all(Enorm(tt, cn, 20000) <= Cb*tt**1.25 for tt in [1.0, 0.1, 1e-3, 1e-5])
rep("T3(iii)(a) bound superiore con le costanti dichiarate (3 dati, anche complessi)", ub_ok)
# compatible finite data (u0'(0)=u0'(L)=0): e1 - e3/3
cn = [1.0, 0.0, -1/3]
ts2 = [1e-2, 1e-3, 1e-4]; v2 = [Enorm(tt, cn, 20000) for tt in ts2]
sl2 = [np.log(v2[i+1]/v2[i])/np.log(ts2[i+1]/ts2[i]) for i in range(2)]
print("   e1 - e3/3 (S_disp=S_pari=0): ||E|| =", [f"{v:.3e}" for v in v2], " pendenze:", [f"{q:.4f}" for q in sl2])
rep("T3(iii)(c) dati compatibili: ordine >= 2 (osservato)", min(sl2) > 1.95)
# second compatibility condition: u0 = x^2(1-x)^2 (attacco del kill-argument)
NN = 3000
nn = np.arange(1, NN+1)
# sine coefficients of x^2(1-x)^2 on (0,1): sqrt2 * 48(1-(-1)^n)/(n pi)^5 ... computed by quadrature check below
def coef(k):
    return float(mp.quad(lambda z: z**2*(1-z)**2*mp.sqrt(2)*mp.sin(k*mp.pi*z), [0, 1]))
cf_closed = np.sqrt(2)*2*(1-(-1.0)**nn)*(12-(np.pi*nn)**2)/(nn*np.pi)**5
rep("contro-esempio KA: coefficienti di x^2(1-x)^2 in forma chiusa = quadratura (n<=6)",
    all(abs(coef(k)-cf_closed[k-1]) < 1e-12 for k in range(1, 7)))
ts3 = [1e-2, 1e-3, 1e-4]; v3 = [Enorm(tt, cf_closed[:400], 6000) for tt in ts3]
sl3 = [np.log(v3[i+1]/v3[i])/np.log(ts3[i+1]/ts3[i]) for i in range(2)]
print("   x^2(1-x)^2: ||E|| =", [f"{v:.3e}" for v in v3], " pendenze:", [f"{q:.4f}" for q in sl3])
rep("KA-T3: u0=x^2(1-x)^2 (Vu0 in H^2 cap H^1_0, A0u0 not in H^1_0): ordine < 2 (-> 7/4)", sl3[-1] < 1.9 and sl3[-1] > 1.6)

# ---------------------------------------------------------------- P3-L2 / P3-T1 / P3-C1
gam, n1 = sp.Rational(2, 3), 3
I_beta = sp.integrate((t-s)**((n1-1)*gam)*s**(gam-1), (s, 0, t))
rep("L2(a) integrale di Beta (gamma=2/3, n=3)", sp.simplify(I_beta - t**(n1*gam)*sp.gamma((n1-1)*gam+1)*sp.gamma(gam)/sp.gamma(n1*gam+1)) == 0)
k, q, dl = sp.symbols('k q delta', positive=True)
yy = sp.symbols('yy', positive=True)
f = yy**k*sp.exp(-s*dl*yy**q); ystar = (k/(q*dl*s))**(1/q)
rep("T1(a2) argmax e valore di sup y^k e^{-s delta y^q}", sp.simplify(sp.diff(sp.log(f), yy).subs(yy, ystar)) == 0 and
    sp.simplify(sp.log(f.subs(yy, ystar)) - sp.log((k/(q*dl*sp.E*s))**(k/q))) == 0)
mu = sp.symbols('mu', positive=True); Dd = sp.symbols('D', positive=True)
fm = mu**2*sp.exp(-2*Dd*mu**2*s); crit = sp.solve(sp.diff(fm, mu), mu)
rep("T1(b) sup mu^2 e^{-2D mu^2 s} = 1/(2eDs)", any(sp.simplify(fm.subs(mu, r) - 1/(2*sp.E*Dd*s)) == 0 for r in crit))
nn_ = 12; val = max((2*t0*yv)**nn_*np.exp(-t0*yv)/math.factorial(nn_) for t0 in [1.0] for yv in np.linspace(0, 60, 600001))
rep("C1(a) sup (2ty)^n e^{-ty}/n! = (2n)^n e^{-n}/n! (n=12)", abs(val - (2*nn_)**nn_*np.exp(-nn_)/math.factorial(nn_))/val < 1e-6)

# ---------------------------------------------------------------- P3-T2: Lemma D, Dyson via Van Loan
def F(tt, zs):  # divided difference of e^{t z} by contour integral (valid for repeated points)
    zs = [mp.mpc(z) for z in zs]; cen = sum(zs)/len(zs); R = max(abs(z-cen) for z in zs) + 1
    return mp.quad(lambda th: mp.e**(tt*(cen+R*mp.e**(1j*th)))*R*mp.e**(1j*th)/mp.fprod([cen+R*mp.e**(1j*th)-z for z in zs]), [0, 2*mp.pi])/(2*mp.pi)
okD = True
for zs in ([0.3, -1.2, 0.7+0.5j], [-1, -1, -1], [-1, -1, 2.0, 0.5], [0, 0, -3]):
    lhs = F(1.3, zs); rhs = mp.quad(lambda ss: mp.e**(zs[0]*ss)*F(1.3-ss, zs[1:]), [0, 1.3])
    okD &= abs(lhs - rhs) < 1e-8
rep("T2 Lemma D (anche punti ripetuti)", okD, "")
rep("T2 F_j a punti coincidenti = t^j e^{tz}/j!", abs(F(0.7, [-2, -2, -2]) - 0.7**2*mp.e**(-1.4)/2) < 1e-10)
from scipy.linalg import expm
lam = np.array([0.0, -1.0, -3.0]); A0 = np.diag(lam)
rng = np.random.default_rng(1); V = rng.normal(size=(3, 3)); tt = 0.9
Z = np.zeros((3, 3))
blk = np.block([[A0, V, Z], [Z, A0, V], [Z, Z, A0]]); Eb = expm(tt*blk)
S1, S2 = Eb[:3, 3:6], Eb[:3, 6:9]
P1 = np.array([[V[m, n]*complex(F(tt, [lam[n], lam[m]])).real for n in range(3)] for m in range(3)])
P2 = np.array([[sum(V[m, kk]*V[kk, n]*complex(F(tt, [lam[n], lam[kk], lam[m]])).real for kk in range(3)) for n in range(3)] for m in range(3)])
rep("T2(a),(b) 1° e 2° ordine Dyson = formula dei cammini (Van Loan)", np.allclose(S1, P1, atol=1e-9) and np.allclose(S2, P2, atol=1e-9))

# ---------------------------------------------------------------- P3-P1: zeri di e^w-1-w
w0 = mp.findroot(lambda w: mp.e**w-1-w, mp.mpc(2.09, 7.46))
rep("P1(c) zero non reale di e^w-1-w", abs(mp.e**w0-1-w0) < 1e-10 and abs(w0.imag) > 1, mp.nstr(w0, 8))
lam_n, lam_m = w0 + mp.mpf(-5), mp.mpf(-5)   # t=1
el = (mp.e**lam_n - mp.e**lam_m)/(lam_n-lam_m) - mp.e**lam_m
rep("P1(c) elemento moltiplicativo nullo a t=1 con lambda_n-lambda_m = w0", abs(el) < 1e-15)

# ---------------------------------------------------------------- P3-T4 (eps x)
X, zeta, eps, sig = sp.symbols('x zeta epsilon sigma')
ok4 = True
for deg in (2, 3):
    al = sp.symbols(f'a0:{deg+1}')
    a = lambda z: sum(al[l]*z**l for l in range(deg+1))
    Bt = sp.integrate(a(zeta+eps*sig), (sig, 0, t))
    expo = sum(eps**kk*t**(kk+1)/sp.factorial(kk+1)*sp.diff(a(zeta), zeta, kk) for kk in range(0, deg+1))
    ok4 &= sp.expand(Bt - expo) == 0
    u = sp.exp((zeta+eps*t)*X + Bt)
    ok4 &= sp.simplify((sp.diff(u, t) - sum(al[l]*sp.diff(u, X, l) for l in range(deg+1)) - eps*X*u)/u) == 0
    eta = zeta + eps*t
    other = sum((-eps)**kk*t**(kk+1)/sp.factorial(kk+1)*sp.diff(a(zeta), zeta, kk).subs(zeta, eta) for kk in range(1, deg+1))
    ok4 &= sp.expand(Bt - t*a(eta) - other) == 0
    ok4 &= sp.expand(expo.coeff(eps, deg) - t**(deg+1)*sp.factorial(deg)*al[deg]/sp.factorial(deg+1)) == 0
rep("T4(a),(c) B_t = sum eps^k t^{k+1} a^(k)/(k+1)!, soluzione, altro ordine, grado esatto (deg a = 2, 3)", ok4)
z, x0 = sp.symbols('z x0'); al = sp.symbols('b0:4'); a3 = sum(al[l]*z**l for l in range(4))
G = sp.exp(z*(X-x0) + t*a3)
vv = [sp.simplify(sp.factorial(nn)*sp.series(G, z, 0, nn+1).removeO().coeff(z, nn)) for nn in range(6)]
ok = True
for nn in range(5):
    rhs = vv[nn+1] - t*sum(sp.binomial(nn, j)*sp.diff(a3, z, j+1).subs(z, 0)*vv[nn-j] for j in range(nn+1))
    ok &= sp.expand((X-x0)*vv[nn] - rhs) == 0
rep("T4(f) (x-x0)v_n = v_{n+1} - t sum C(n,j) a^(j+1)(0) v_{n-j} (a cubico, n<=4)", ok)
A_ = sp.Function('f')
rep("T4(e) [a(d),x] = a'(d) su a cubico (azione su f)", sp.simplify(
    sum(al[l]*sp.diff(X*A_(X), X, l) for l in range(4)) - X*sum(al[l]*sp.diff(A_(X), X, l) for l in range(4))
    - sum(l*al[l]*sp.diff(A_(X), X, l-1) for l in range(1, 4))) == 0)

# ---------------------------------------------------------------- P3-T5
Dp, sp_ = sp.symbols('D s', positive=True); yv_, kk_ = sp.symbols('y kappa', real=True)
K = sp.exp(-yv_**2/(4*Dp*sp_))/sp.sqrt(4*sp.pi*Dp*sp_)
h = lambda zz: sp.exp(sp_*Dp*zz**2)
zz = sp.symbols('zz')
okm = all(sp.simplify(sp.integrate(yv_**j*K, (yv_, -sp.oo, sp.oo)) - (-1)**j*sp.diff(h(zz), zz, j).subs(zz, 0)) == 0 for j in range(5))
rep("T5(iii) momenti M_j = (-1)^j h^(j)(0) (calore)", okm)
okb = True
for nn in range(4):
    vn = sp.expand(sp.factorial(nn)*sp.series(sp.exp(z*(yv_-x0) - sp_*Dp*z**2), z, 0, nn+1).removeO().coeff(z, nn))
    for mm in range(4):
        Km = sp.diff(K, yv_, mm).subs(yv_, x0 - yv_)
        val = sp.simplify(sp.integrate(sp.expand(vn*Km), (yv_, -sp.oo, sp.oo)))
        okb &= sp.simplify(val - (sp.factorial(nn) if nn == mm else 0)) == 0
rep("T5(iii) biortogonalità int v_n(-s,y) K_s^(m)(x0-y) dy = n! delta (calore, n,m<=3)", okb)
pk = lambda expr: sp.re(sp.expand(expr.subs(zz, sp.I*kk_)))
rep("T5(iv) p per KdV-Burgers, Airy, Schrodinger, AD", sp.simplify(pk(-zz**3+Dp*zz**2) + Dp*kk_**2) == 0 and pk(zz**3) == 0
    and pk(sp.I*zz**2) == 0 and sp.simplify(pk(Dp*zz**2 - 3*zz) + Dp*kk_**2) == 0)

# ---------------------------------------------------------------- P3-P2
tau = sp.symbols('tau'); p0, p1, p2, t0_, t1_, t2_, ee = sp.symbols('p0 p1 p2 t0 t1 t2 e')
P = (tau-1)*(tau+2)*(tau-3); Tp = 2*tau**2 - tau + 5
Cc = sp.Matrix([[0, 1, 0], [0, 0, 1], [-6, 5, 2]])   # companion of tau^3-2tau^2-5tau+6
ok = sp.expand(P - (tau**3 - 2*tau**2 - 5*tau + 6)) == 0
for la in (1, -2, 3):
    qq = sp.quo(P, tau-la); w = sp.Matrix([qq.coeff(tau, j) for j in range(3)])/sp.diff(P, tau).subs(tau, la)
    ok &= (w.T*Cc - la*w.T).is_zero_matrix and sp.simplify(w[2] - 1/sp.diff(P, tau).subs(tau, la)) == 0
    CT = sp.Matrix([[0, 0, 0], [0, 0, 0], [-Tp.coeff(tau, 0), -Tp.coeff(tau, 1), -Tp.coeff(tau, 2)]])
    v = sp.Matrix([1, la, la**2])
    kato = (w.T*CT*v)[0]
    implicit = -Tp.subs(tau, la)/sp.diff(P, tau).subs(tau, la)
    root = sp.nsolve(P + sp.Rational(1, 10**6)*Tp, tau, la)
    ok &= sp.simplify(kato - implicit) == 0 and abs((root - la)*10**6 - implicit) < 1e-3
rep("P2(b),(c) duale di Lagrange, (w)_k = 1/P', Kato = -T/P' (anche differenza finita)", ok)

# ---------------------------------------------------------------- P3-T6
a1, a2, a3_, th, sv, u0 = sp.symbols('a1 a2 a3 theta s u0')
aa = a1 + a2 + a3_
# single mode: u(s) = u0 e^{s a}; Faddeev components with L0 = d_t
ui = [ai*u0*(sp.exp(sv*aa)-1)/aa for ai in (a1, a2, a3_)]
ok = sp.simplify(sum(ui) + u0 - u0*sp.exp(sv*aa)) == 0
Ei = [ui[i] - u0*(sp.exp(sv*ai)-1) for i, ai in enumerate((a1, a2, a3_))]
# E^(i) = G_i a_i sum_{j!=i} u^(j) (SCOUT-2 E_int^(i))
r = sp.symbols('r')
for i, ai in enumerate((a1, a2, a3_)):
    others = sum(ui[j] for j in range(3) if j != i).subs(sv, r)
    Gi = sp.Integral(sp.exp((sv-r)*ai)*ai*others, (r, 0, sv))
    num = {a1: 0.3+0.2j, a2: -1.1, a3_: 0.7-0.4j, u0: 1.3, sv: 0.8}
    ok &= abs(complex((Gi - Ei[i]).subs(num).evalf())) < 1e-12
    ok &= sp.simplify(sp.series(Ei[i], sv, 0, 3).removeO().coeff(sv, 2) - u0*ai*(aa-ai)/2) == 0
rep("T6(iv) E^(i) = G_i a_i sum_{j!=i} u^(j) (= E_int^(i) di SCOUT-2) e coeff. s^2 = a_i(a-a_i)/2", ok)
# theta-family L0 = d_t - theta*sum a_i : exact, equivariant, theta-dependent
uith = [ai*u0*(sp.exp(sv*aa)-sp.exp(th*sv*aa))/aa for ai in (a1, a2, a3_)]
ok = sp.simplify(sum(uith) + u0*sp.exp(th*sv*aa) - u0*sp.exp(sv*aa)) == 0
ok &= sp.simplify(sp.diff(uith[0], th)) != 0
# quadrature form: u^(i)_theta = int_{theta s}^{s} a_i u(rho) d rho
ok &= abs(complex((uith[0] - sp.Integral(a1*u0*sp.exp(r*aa), (r, th*sv, sv))).subs({a1: 0.3+0.2j, a2: -1.1, a3_: 0.7-0.4j, u0: 1.3, sv: 0.8, th: 0.35}).evalf())) < 1e-12
Gth = sp.Integral(sp.exp(th*aa*(sv-r))*(1-th)*a1*u0*sp.exp(r*aa), (r, 0, sv))
num2 = {a1: 0.3+0.2j, a2: -1.1, a3_: 0.7-0.4j, u0: 1.3, sv: 0.8, th: 0.35}
ok &= abs(complex((Gth - uith[0]).subs(num2).evalf())) < 1e-12
rep("KA-T6(vi) famiglia L0^theta: esatta, simmetrica nei termini, non degenere, dipende da theta, è una quadratura di u", ok)
dth = sp.simplify(sp.diff(uith[0], sv) - a1*u0*sp.exp(sv*aa))
rep("T6 principio di bilancio d_s u^(i) = a_i u seleziona theta=0 (per theta in (0,1) fallisce)", sp.simplify(dth.subs(th, 0)) == 0 and sp.simplify(dth.subs(th, sp.Rational(1, 2))) != 0)
kap_ = sp.symbols('kappa', real=True); cc_, tT = sp.symbols('c T', positive=True)
rep("T6(iii) G_c a_c su e^{i kappa (x + c r)}: i c kappa t e^{i kappa(x+ct)}",
    sp.simplify(sp.integrate(sp.exp(sp.I*kap_*(X+cc_*(t-r)))*cc_*sp.I*kap_*sp.exp(sp.I*kap_*cc_*r), (r, 0, t)) - sp.I*cc_*kap_*t*sp.exp(sp.I*kap_*(X+cc_*t))) == 0)

print("\nTOTALE:", sum(o for _, o in RES), "/", len(RES), "OK")
