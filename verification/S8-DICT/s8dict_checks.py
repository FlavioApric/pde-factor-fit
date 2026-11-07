# S8-DICT — verifiche SymPy/mpmath/numpy (solo verifica, non prove). Esecuzione:
#   D:\ProblemaBase\.venv\Scripts\python.exe -I work/S8-DICT/sympy/s8dict_checks.py
import sympy as sp
import mpmath as mp
import numpy as np

RES = []
def check(name, ok, info=""):
    RES.append((name, bool(ok)))
    print(("OK  " if ok else "FAIL"), name, info)

t, x, y, z, s, r, th = sp.symbols('t x y z s r theta', real=True)
a, lam, tau = sp.symbols('a lambda tau', positive=True)

# ---------------- A: universalita' ----------------
# A0 U1-a: sistema triangolare dei coefficienti (1D, ordine 2)
a0, a1, a2 = sp.Function('a0')(y), sp.Function('a1')(y), sp.Function('a2')(y)
def T(f):  # operatore con coefficienti generici, applicato a f(z) e valutato in z=y
    return (a0*f + a1*sp.diff(f, z) + a2*sp.diff(f, z, 2)).subs(z, y)
m = [z**b/sp.factorial(b) for b in range(3)]
sol = sp.solve([sp.Eq(sp.Symbol('T%d' % b), T(m[b])) for b in range(3)], [a0, a1, a2], dict=True)[0]
Tm = [sp.Symbol('T%d' % b) for b in range(3)]
ok = sp.simplify(sol[a0] - Tm[0]) == 0 and sp.simplify(sol[a1] - (Tm[1] - y*Tm[0])) == 0
check("A0 U1-a coefficienti da T(m_beta) (triangolare)", ok)

# A1 U2: la realizzazione g_{x,j} ha r-getto j in x (chi = 1 vicino a x)
f = sp.sin(z) + z**3
j = sp.symbols('j0:3')
g = f + sum((j[k] - sp.diff(f, z, k).subs(z, x))*(z - x)**k/sp.factorial(k) for k in range(3))
ok = all(sp.simplify(sp.diff(g, z, k).subs(z, x) - j[k]) == 0 for k in range(3))
check("A1 U2 getto della realizzazione g_{x,j}", ok)

# A2 N2: funzioni bump esplicite
def S(u):
    return np.where(u > 0, np.exp(-1.0/np.maximum(u, 1e-300)), 0.0)
def phi(rr):
    rr = np.asarray(rr, float)
    return S(2 - rr)/(S(2 - rr) + S(rr - 1))
def psi(rr):
    return phi(rr) - phi(2*rr)
ok = abs(psi(1.0) - 1) < 1e-14 and abs(psi(0.5)) < 1e-14 and abs(psi(2.0)) < 1e-14
rr = np.linspace(1e-3, 2000, 400001)
tot = sum(psi(2.0**(-k)*rr) for k in range(1, 14))
ok = ok and psi(rr).min() >= -1e-15 and tot.max() <= 1 + 1e-12
check("A2 N2 psi(1)=1, psi(1/2)=psi(2)=0, psi>=0, somma<=1", ok, "max somma=%.6f" % tot.max())
# separazione: eps={3,5}, eps'={5}: sup |m_eps - m_eps'| <xi>^{-m} = 1
xi = np.linspace(0, 200, 2000001)
diff = np.abs(psi(2.0**-3*xi))  # (m_eps - m_eps')<xi>^{-m} = psi_3
check("A2b N2 separazione = 1", abs(diff.max() - 1) < 1e-9, "sup=%.12f" % diff.max())

# A3 U3(c): coda (1-chi(xi/R))<xi>^m in S^{m'}: sup <xi>^{m-m'}(1-chi) ~ R^{m-m'}
mm, mp_ = 1.0, 1.5
vals = []
for R in [10, 100, 1000]:
    xx = np.linspace(0, 50*R, 500001)
    vals.append(np.max((1 - phi(xx/R))*(1 + xx**2)**((mm - mp_)/2)))
ratios = [vals[i]/vals[i+1] for i in range(2)]
check("A3 U3(c) coda decresce come R^{m-m'}", all(abs(q - 10**(mp_ - mm)) < 0.05*10**(mp_-mm) for q in ratios), str(ratios))

# A4 Caffarelli–Silvestre: phi(r)=2^{1-s}/Gamma(s) r^s K_s(r)
mp.mp.dps = 60  # fix 27/10: y, r piu' piccoli; con y=1e-10 la correzione (xi y)^{2(1-s)} ~ 1e-4 superava la tolleranza
okA4 = True
for sv in [mp.mpf('0.25'), mp.mpf('0.5'), mp.mpf('0.8')]:
    ph = lambda q: 2**(1 - sv)/mp.gamma(sv)*q**sv*mp.besselk(sv, q)
    for q in [mp.mpf('0.3'), mp.mpf('1.7'), mp.mpf('5')]:
        res = mp.diff(ph, q, 2) + (1 - 2*sv)/q*mp.diff(ph, q) - ph(q)
        okA4 = okA4 and abs(res) < mp.mpf('1e-25')
    okA4 = okA4 and abs(ph(mp.mpf('1e-40')) - 1) < mp.mpf('1e-12')
    for XI in [mp.mpf('0.7'), mp.mpf('3')]:
        yy = mp.mpf('1e-40')
        neu = yy**(1 - 2*sv)*XI*2**(1 - sv)/mp.gamma(sv)*(XI*yy)**sv*mp.besselk(1 - sv, XI*yy)  # phi'(r) = -c r^s K_{1-s}(r)
        target = 2**(1 - 2*sv)*mp.gamma(1 - sv)/mp.gamma(sv)*XI**(2*sv)
        okA4 = okA4 and abs(neu/target - 1) < mp.mpf('1e-10')
check("A4 Caffarelli-Silvestre: EDO, phi(0)=1, costante di Neumann", okA4)

# A5 ritardo = trasporto
U = sp.Function('U')
w = U(t - th)
check("A5 w(t,theta)=u(t-theta): w_t + w_theta = 0", sp.simplify(sp.diff(w, t) + sp.diff(w, th)) == 0)

# A6 N3: sup_omega |e^{-i tau omega} - R(i omega)| >= 1
rng = np.random.default_rng(0)
om = np.linspace(-400, 400, 800001)
okA6 = True
mins = []
for trial in range(200):
    p = rng.normal(size=rng.integers(1, 4)); q = rng.normal(size=len(p) + rng.integers(0, 2))
    q[0] = abs(q[0]) + 0.5
    Rv = np.polyval(p, 1j*om)/np.polyval(q, 1j*om)
    if not np.all(np.isfinite(Rv)):
        continue
    val = np.max(np.abs(np.exp(-1j*1.0*om) - Rv))
    mins.append(val); okA6 = okA6 and val >= 1 - 1e-6
# Pade diagonale [3/3] di e^{-s}
from math import factorial
def pade_coeffs(n):
    return [factorial(2*n - k)*factorial(n)/(factorial(2*n)*factorial(k)*factorial(n - k)) for k in range(n + 1)]
c = pade_coeffs(3)
Pn = np.polyval(list(reversed([ck*(-1)**k for k, ck in enumerate(c)])), 1j*om)
Qn = np.polyval(list(reversed(c)), 1j*om)
valP = np.max(np.abs(np.exp(-1j*om) - Pn/Qn))
bandP = np.max(np.abs(np.exp(-1j*om) - Pn/Qn)[np.abs(om) < 1])
check("A6 N3 distanza >= 1 (200 razionali casuali + Pade [3/3])", okA6 and valP >= 1, "min=%.4f, Pade sup=%.3f, Pade su |w|<1: %.2e" % (min(mins), valP, bandP))

# A7 memoria: immersione markoviana e rappresentazione diffusiva di Caputo
sv_ = sp.symbols('sigma', positive=True)
fexpr = sv_**2 + sp.sin(sv_)
wint = sp.integrate(sp.exp(-lam*(t - sv_))*fexpr, (sv_, 0, t))
check("A7 w' = -lambda w + f", sp.simplify(sp.diff(wint, t) + lam*wint - fexpr.subs(sv_, t)) == 0)
al = sp.Rational(1, 3)
lhs = sp.integrate(sp.exp(-lam*t)*lam**(al - 1), (lam, 0, sp.oo))/(sp.gamma(al)*sp.gamma(1 - al))
check("A7b Caputo: int e^{-lt} l^{a-1}/(G(a)G(1-a)) = t^{-a}/G(1-a)", all(abs(sp.N((lhs - t**(-al)/sp.gamma(1 - al)).subs(t, tv))) < 1e-12 for tv in [0.1, 1, 7]))

# A8 trapezi per t^{-beta}: errore relativo uniforme in t, <= 2 cos(a)^{-beta}/(e^{2 pi a/h}-1)
mp.mp.dps = 25
beta = mp.mpf('0.5'); aa = mp.pi/4
okA8 = True; worst = 0
for h in [mp.mpf('0.5'), mp.mpf('0.35')]:
    bound = 2*mp.cos(aa)**(-beta)/(mp.exp(2*mp.pi*aa/h) - 1)
    for tv in [mp.mpf('1e-6'), mp.mpf('1e-2'), 1, mp.mpf('1e3'), mp.mpf('1e6')]:
        smin = -mp.log(tv) - 80; smax = -mp.log(tv) + 6
        jmin = int(mp.floor(smin/h)); jmax = int(mp.ceil(smax/h))
        Ssum = h*mp.fsum(mp.exp(beta*jj*h - mp.exp(jj*h)*tv) for jj in range(jmin, jmax + 1))
        rel = abs(Ssum/(mp.gamma(beta)*tv**(-beta)) - 1)
        worst = max(worst, rel/bound)
        okA8 = okA8 and rel <= bound
check("A8 trapezi t^{-beta}: errore relativo <= bound uniforme in t", okA8, "max rel/bound=%.3f" % float(worst))

# ---------------- B: N1 ----------------
n_, d_ = sp.symbols('n d', positive=True, integer=True)
expr = ((n_ + 1)*(n_ + 2) - (n_ - d_ + 1)*(n_ - d_ + 2))/2 - d_*(2*n_ + 3 - d_)/2
check("B1 N1(iii) dim R_{<=n} - dim (L)_{<=n} = d(2n+3-d)/2", sp.expand(expr) == 0)

# B2 (a'): P + a, a = -P(u)/u, annulla u
uu = sp.exp(t + x**2) + 2   # senza zeri
P = lambda F: (1 + t*x)*sp.diff(F, x, 2) + x**2*sp.diff(F, t) + sp.sin(t)*sp.diff(F, x)
aa_ = -P(uu)/uu
check("B2 (a') (P - P(u)/u) u = 0", sp.simplify(P(uu) + aa_*uu) == 0)

# B3 (b'): K = 2 coefficienti funzionali => nucleo phi*(T2u, -T1u)
u3 = sp.exp(t)*sp.cos(x) + t*x
T1u, T2u = sp.diff(u3, x), u3
ph_ = sp.Function('ph')(t, x)
check("B3 (b') K=2: rho_u(phi T2u, -phi T1u) = 0", sp.simplify(ph_*T2u*T1u - ph_*T1u*T2u) == 0)
# Schrodinger: V = (i u_t + u_xx)/u identificato; V reale falsificabile
u4 = sp.exp(-sp.I*t)*(2 + sp.cos(x)) + sp.I*t*x/5
V4 = sp.simplify((sp.I*sp.diff(u4, t) + sp.diff(u4, x, 2))/u4)
val = complex(V4.subs({t: 0.3, x: 0.7}).evalf())
check("B3b Schrodinger: V_u ha parte immaginaria != 0 => nessuna legge con V reale (falsificabile)", abs(val.imag) > 1e-3, "V(0.3,0.7)=%s" % val)
u5 = sp.exp(-sp.I*t)*(2 + sp.cos(x))
V5 = sp.simplify((sp.I*sp.diff(u5, t) + sp.diff(u5, x, 2))/u5)
check("B3c Schrodinger: per u stazionario V_u reale = 1 - cos x/(2+cos x)", sp.simplify(V5 - (1 - sp.cos(x)/(2 + sp.cos(x)))) == 0, str(V5))
# u_t = a(t,x) u_x identifica a con u_x != 0
u6 = x + t*x**3 + t**2
a6 = sp.simplify(sp.diff(u6, t)/sp.diff(u6, x))
check("B3d u_t = a(t,x)u_x: a = u_t/u_x", sp.simplify(sp.diff(u6, t) - a6*sp.diff(u6, x)) == 0, str(a6))
# B4 DEVIL C3: u = t - x^2 nessuna legge normalizzata in 0
A_, B_ = sp.symbols('A B')
u7 = t - x**2
expr7 = (sp.diff(u7, t) + A_*sp.diff(u7, x) + B_*u7).subs({t: 0, x: 0})
check("B4 u=t-x^2: (d_t + a d_x + b)u (0,0) = 1", expr7 == 1)

# B5 N1(v) non lineare: coefficiente di grado massimo in s del determinante
uB = 1 + x + t**2
wB = x*t + x**2
Ps = [lambda F: F, lambda F: F**2, lambda F: F*sp.diff(F, x)]
Ptop = Ps  # omogenei
degs = [1, 2, 2]
psis = [1, x, t]
def ell(Fexpr, ps):
    return sp.integrate(sp.integrate(sp.expand(Fexpr*ps), (x, 0, 1)), (t, 0, 1))
Mts = sp.Matrix(3, 3, lambda i, jj: ell(Ps[i](uB + s*wB), psis[jj]))
detp = sp.Poly(sp.expand(Mts.det()), s)
lead = detp.coeff_monomial(s**sum(degs))
Mw = sp.Matrix(3, 3, lambda i, jj: ell(Ptop[i](wB), psis[jj]))
check("B5 N1(v) NL: coeff. di s^{sum e_i} = det(l_j(P_i^top(w)))", sp.simplify(lead - Mw.det()) == 0 and Mw.det() != 0, "det=%s" % Mw.det())

# ---------------- C: misfit, B2, R3, R-STOP ----------------
rng = np.random.default_rng(1)
okC1 = True
for trial in range(300):
    M, N = 40, 4
    A = rng.normal(size=(M, N)); d0 = rng.normal(size=M)
    G = A.T @ A; lmin = np.linalg.eigvalsh(G)[0]
    cn = -np.linalg.solve(G, A.T @ d0)
    ct = cn + rng.normal(scale=rng.uniform(0.01, 2), size=N)
    eta = np.linalg.norm(d0 + A @ ct)
    okC1 = okC1 and np.linalg.norm(cn - ct) <= 2*eta/np.sqrt(lmin) + 1e-12
check("C1 B2 |c_n - c~| <= 2 eta / sqrt(lambda_min)", okC1)
okC2 = True
for trial in range(300):
    M, N = 30, 3
    A = rng.normal(size=(M, N)); d0 = rng.normal(size=M); Du = rng.normal(size=M)
    def resid(Amat):
        c_ = np.linalg.lstsq(Amat, -d0, rcond=None)[0]; return d0 + Amat @ c_
    rn = resid(A); rn1 = resid(np.column_stack([A, Du]))
    Q, _ = np.linalg.qr(A); Pp = Du - Q @ (Q.T @ Du)
    gain = (rn @ Du)**2/(Pp @ Pp)
    okC2 = okC2 and abs((rn @ rn - rn1 @ rn1) - gain) < 1e-9*(1 + rn @ rn)
check("C2 R3 guadagno esatto = <res,Du>^2/|P^perp Du|^2", okC2)
okC3 = True
for trial in range(300):
    A = rng.normal(size=(20, 5)); E = rng.normal(scale=0.1, size=(20, 5))
    s1 = np.linalg.svd(A, compute_uv=False)[-1]; s2 = np.linalg.svd(A + E, compute_uv=False)[-1]
    okC3 = okC3 and abs(s1 - s2) <= np.linalg.norm(E, 2) + 1e-12
check("C3 Weyl |sigma_min(A)-sigma_min(A+E)| <= |E|", okC3)

# ---------------- D: NS-EXPALG ----------------
uf = sp.Function('u')(x, t)
W = sp.exp(sp.I*uf)
lhs = 2*(W*sp.diff(W, x, t) - sp.diff(W, x)*sp.diff(W, t)) - (W**3 - W)
rhs = 2*sp.I*W**2*(sp.diff(uf, x, t) - sp.sin(uf))
check("D1 sine-Gordon: 2(w w_xt - w_x w_t) - (w^3-w) = 2i w^2 (u_xt - sin u)", sp.simplify((lhs - rhs).rewrite(sp.exp)) == 0)
Vv = sp.exp(uf)
lhs2 = Vv*sp.diff(Vv, x, t) - sp.diff(Vv, x)*sp.diff(Vv, t) - Vv**3
check("D2 Liouville: v v_xt - v_x v_t - v^3 = v^2 (u_xt - e^u)", sp.simplify(lhs2 - Vv**2*(sp.diff(uf, x, t) - sp.exp(uf))) == 0)
ak = sp.Rational(3, 2)
uk = 4*sp.atan(sp.exp(ak*x + t/ak))
rels = [sp.diff(uk, x, t) - sp.sin(uk), sp.diff(uk, x, 2) - ak**2*sp.diff(uk, x, t), sp.diff(uk, t, 2) - sp.diff(uk, x, t)/ak**2]
okD3 = all(abs(complex(sp.N(e_.subs({x: xv, t: tv})))) < 1e-12 for e_ in rels for (xv, tv) in [(0.3, -0.2), (-1.1, 0.5), (0.0, 0.0)])
# rango delle 5 funzioni atomo {u_xt, sin u, u_xx, u_tt, u} su griglia
fl = [sp.lambdify((x, t), e_) for e_ in [sp.diff(uk, x, t), sp.sin(uk), sp.diff(uk, x, 2), sp.diff(uk, t, 2), uk]]
pts = [(xv, tv) for xv in np.linspace(-2, 2, 15) for tv in np.linspace(-2, 2, 15)]
Mat = np.array([[float(F(*p)) for F in fl] for p in pts])
sv5 = np.linalg.svd(Mat, compute_uv=False)
rank = int(np.sum(sv5 > 1e-9*sv5[0]))
check("D3 kink: 3 relazioni, rango 2 => nucleo 3 (non identifica)", okD3 and rank == 2, "sv=%s" % np.array2string(sv5, precision=2))
# D4 trasporto dei getti: u_x = -i w_x / w, u_xx = -i (w w_xx - w_x^2)/w^2
okD4 = sp.simplify(sp.diff(uf, x) - (-sp.I*sp.diff(W, x)/W)) == 0 and \
       sp.simplify(sp.diff(uf, x, 2) - (-sp.I*(W*sp.diff(W, x, 2) - sp.diff(W, x)**2)/W**2)) == 0
check("D4 getti di u razionali nei getti di w = e^{iu}", okD4)

# ---------------- E: I-LIM ----------------
th_, ss, NN = sp.symbols('theta_ s N', positive=True)
solth = sp.solve(sp.Eq(ss, -th_*NN/2 + (1 - th_)*(ss + 1)), th_)[0]
check("E1 esponente di interpolazione per scaling theta = 2/(2s+2+N)", sp.simplify(solth - 2/(2*ss + 2 + NN)) == 0, str(solth))

print("\nTOTALE: %d/%d OK" % (sum(1 for _, o in RES if o), len(RES)))

