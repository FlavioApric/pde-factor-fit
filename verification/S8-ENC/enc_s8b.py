# S8-ENC (seconda parte) — verifiche (non metodo) per:
#   ENC-T2(c) getti nel punto base; ENC-K0 ricorsione dei coefficienti; ENC-K1' passo di Darboux generico;
#   A9: E^mult esatto per V lineare, stima raffinata, limite E^mult/t^2 -> (1/2)[H0,V];
#   NS-EQUIV su Omega limitato: Dirichlet -> Dirichlet, Neumann -> Robin (lente, Avron-Herbst); periodo della lente;
#   FW: Foldy-Wouthuysen esatto per Dirac 1+1 libero; FAD: componenti di Faddeev a energia fissata.
import sys
sys.stdout.reconfigure(encoding="utf-8")
import sympy as sp
import numpy as np
from scipy.integrate import solve_ivp

res = []
def report(name, ok, extra=''):
    res.append((name, ok)); print(('OK  ' if ok else 'FAIL') + ' ' + name + ' ' + str(extra))

x, s, y = sp.symbols('x s y', real=True)
t = sp.Symbol('t', positive=True)
F = sp.Symbol('F', positive=True)

# ---------- 1. ENC-T2(c): (T f)'' = q T f + T(f''), quindi (T f)''(0) = f''(0) + q(0) f(0); getti triangolari
X, E = sp.symbols('xi eta')
a_, b_ = sp.symbols('a b')
def goursat(qfun, N):
    u = sp.Symbol('u')
    base = sp.Rational(1, 2)*sp.integrate(qfun(u), (u, 0, X/2))
    Hn = base
    for _ in range(N):
        integrand = sp.expand(qfun((a_+b_)/2)*Hn.subs({X: a_, E: b_}, simultaneous=True))
        Hn = sp.expand(base + sp.Rational(1, 4)*sp.integrate(sp.integrate(integrand, (b_, 0, E)), (a_, 0, X)))
    return Hn
def T_apply(H, f):
    K = H.subs({X: x+s, E: x-s}, simultaneous=True)
    return sp.expand(f.subs(s, x) + sp.integrate(sp.expand(K*f), (s, -x, x)))
q0, q1, q2 = sp.Rational(3, 2), sp.Rational(-1, 3), sp.Rational(5, 7)
qf = lambda w: q0 + q1*w + q2*w**2
H = goursat(qf, 5)
cs = sp.symbols('f0:7')
fpoly = sum(cs[j]*s**j/sp.factorial(j) for j in range(7))
Tf = T_apply(H, fpoly)
jets = [sp.expand(sp.diff(Tf, x, n).subs(x, 0)) for n in range(5)]
ok = (sp.expand(jets[0] - cs[0]) == 0 and sp.expand(jets[1] - cs[1]) == 0
      and sp.expand(jets[2] - cs[2] - q0*cs[0]) == 0)
# triangolarita' unipotente: il coefficiente di f_n in (Tf)^(n)(0) e' 1, e f_m con m > n non compare
tri = all(sp.expand(jets[n]).coeff(cs[n]) == 1 and all(sp.expand(jets[n]).coeff(cs[m]) == 0 for m in range(n+1, 7)) for n in range(5))
# (Tf)^(n)(0) dipende solo da f_j con j <= n-2 oltre a f_n
lowdep = all(sp.expand(jets[n]).coeff(cs[n-1]) == 0 for n in range(2, 5))
report('ENC-T2(c) getti: (Tf)(0)=f(0), (Tf)\'(0)=f\'(0), (Tf)\'\'(0)=f\'\'(0)+q(0)f(0)', ok, jets[2])
report('ENC-T2(c) mappa dei getti triangolare unipotente (ordini <= 4), salto di 2', tri and lowdep, [jets[3], jets[4]])

# ---------- 2. ENC-K0: ricorsione w_{j-1}' = -(w_j'' + c w_j)/2 e w_0'' + c w_0 = 0: grado di w_{n-k} = k
c = sp.Symbol('c', nonzero=True)
def k0_chain(n):
    ws = {n: sp.Integer(1)}
    for j in range(n, 0, -1):
        ws[j-1] = sp.integrate(-(sp.diff(ws[j], x, 2) + c*ws[j])/2, x)
    last = sp.expand(sp.diff(ws[0], x, 2) + c*ws[0])
    return ws, last
oks = []
for n in range(0, 7):
    ws, last = k0_chain(n)
    degs_ok = all(sp.Poly(ws[n-k], x).degree() == k for k in range(n+1))
    lead_ok = sp.simplify(sp.Poly(ws[0], x).LC() - (-c/2)**n/sp.factorial(n)) == 0
    last_ok = sp.Poly(last, x).degree() == n and sp.simplify(sp.Poly(last, x).LC() - c*(-c/2)**n/sp.factorial(n)) == 0
    oks.append(degs_ok and lead_ok and last_ok)
report('ENC-K0 ricorsione: deg w_{n-k} = k, LC(w_0) = (-c/2)^n/n!, w_0\'\'+c w_0 di grado n (n<=6)', all(oks))
# controllo diretto della formula del commutatore: W L_c - L_0 W = [d^2, W] + c W
g = sp.Function('g')(x)
wf = [sp.Function('w%d' % j)(x) for j in range(4)]
Wop = lambda h: sum(wf[j]*sp.diff(h, x, j) for j in range(4))
lhs = sp.expand(Wop(-sp.diff(g, x, 2) + c*g) + sp.diff(Wop(g), x, 2))
rhs = sp.expand(sum(sp.diff(wf[j], x, 2)*sp.diff(g, x, j) + 2*sp.diff(wf[j], x)*sp.diff(g, x, j+1) for j in range(4)) + c*Wop(g))
report('ENC-K0 W L_c - L_0 W = sum(w_j\'\' d^j + 2 w_j\' d^{j+1}) + c W', sp.expand(lhs - rhs) == 0)

# ---------- 3. ENC-K1': un passo di Darboux con seme generico psi (L_q psi = lam psi)
lam = sp.Symbol('lam')
psi = sp.Function('psi')(x)
qq = sp.diff(psi, x, 2)/psi + lam          # q tale che L_q psi = lam psi
gg = sp.diff(psi, x)/psi
A1 = lambda h: sp.diff(h, x) - gg*h
q1 = qq - 2*sp.diff(gg, x)
Lq = lambda h: -sp.diff(h, x, 2) + qq*h
Lq1 = lambda h: -sp.diff(h, x, 2) + q1*h
r = sp.simplify(A1(Lq(g)) - Lq1(A1(g)))
report('ENC-K1\' A_1 L_q = L_{q_1} A_1, A_1 = d - psi\'/psi, q_1 = q - 2(psi\'/psi)\'', r == 0, r)
Asharp = lambda h: -sp.diff(h, x) - gg*h
r2 = sp.simplify(Asharp(A1(g)) - (Lq(g) - lam*g))
report('ENC-K1\' L_q - lam = A_1^# A_1', r2 == 0, r2)

# ---------- 4. A9, V = F x: E^mult = e^{-itV/2} e^{-itp^2} [e^{-iF^2t^3/12} - e^{iFt^2 p - iF^2 t^3/4}] e^{-itV/2}
K0 = lambda z: (4*sp.pi*sp.I*t)**sp.Rational(-1, 2)*sp.exp(sp.I*z**2/(4*t))
# nucleo del secondo pezzo: e^{-itFx/2} K0(x + F t^2 - y) e^{-iF^2t^3/4} e^{-itFy/2}  deve essere il nucleo di U0 e^{-itV}: K0(x-y) e^{-iFty}
k2 = sp.exp(-sp.I*t*F*x/2)*K0(x + F*t**2 - y)*sp.exp(-sp.I*F**2*t**3/4)*sp.exp(-sp.I*t*F*y/2)
report('A9 lineare: e^{-itV/2}e^{-itp^2}e^{iFt^2p - iF^2t^3/4}e^{-itV/2} = U0(t)e^{-itV}', sp.simplify(k2/(K0(x - y)*sp.exp(-sp.I*F*t*y))) == 1)
# norma: |e^{-iF^2t^3/12} - e^{i(F t^2 p - F^2 t^3/4)}| = |1 - e^{i(F t^2 p - F^2 t^3/6)}|, sup = 2
pp = np.linspace(-50, 50, 200001); tv, Fv = 0.7, 1.3
mult = np.abs(np.exp(-1j*Fv**2*tv**3/12) - np.exp(1j*(Fv*tv**2*pp - Fv**2*tv**3/4)))
report('A9 lineare: ||E^mult(t)||_{L2->L2} = 2 (sup del moltiplicatore)', abs(mult.max() - 2) < 1e-6, mult.max())

# ---------- 5. A9, stima raffinata e limite sul toro (V = 2 cos x, H0 = -d^2), propagatore esatto in base di Fourier
Nn = 512; xs = np.linspace(0, 2*np.pi, Nn, endpoint=False); kf = np.fft.fftfreq(Nn, d=1.0/Nn)
V = 2*np.cos(xs); Vp, Vpp = 2.0, 2.0
f = np.exp(np.sin(xs))*(1 + 0.3*np.cos(3*xs))
M = 64; kk = np.arange(-M, M+1)
Hm = np.diag(kk.astype(float)**2) + (np.eye(2*M+1, k=1) + np.eye(2*M+1, k=-1))
w_, P_ = np.linalg.eigh(Hm)
def to_c(h):
    fh = np.fft.fft(h)/Nn; return np.array([fh[int(j) % Nn] for j in kk])
def from_c(cv):
    out = np.zeros(Nn, complex)
    for j, cj in zip(kk, cv): out += cj*np.exp(1j*j*xs)
    return out
def U0(tv, h): return np.fft.ifft(np.exp(-1j*tv*kf**2)*np.fft.fft(h))
norm = lambda h: np.sqrt(np.sum(np.abs(h)**2)*2*np.pi/Nn)
fprime = np.real(np.fft.ifft(1j*kf*np.fft.fft(f)))
d2 = lambda h: np.fft.ifft(-(kf**2)*np.fft.fft(h))
comm = -d2(V*f) + V*d2(f)          # [H0, V] f con H0 = -d^2
fc = to_c(f); oks = []; info = []
for tv in [0.002, 0.01, 0.05, 0.2, 0.5, 1.0]:
    Uf = from_c(P_ @ (np.exp(-1j*tv*w_)*(P_.conj().T @ fc)))
    Em = Uf - U0(tv, np.exp(-1j*tv*V)*f)
    bound = tv**2/2*(Vpp*norm(f) + 2*Vp*norm(fprime)) + 2*tv**3/3*Vp**2*norm(f)
    oks.append(norm(Em) <= bound); info.append((tv, round(norm(Em), 7), round(bound, 7)))
report('A9 stima ||E^mult f|| <= t^2/2(|V\'\'| |f| + 2|V\'| |f\'|) + 2t^3/3 |V\'|^2 |f| (toro)', all(oks), info)
ratios = []
for tv in [1e-2, 1e-3, 1e-4]:
    Uf = from_c(P_ @ (np.exp(-1j*tv*w_)*(P_.conj().T @ fc)))
    Em = Uf - U0(tv, np.exp(-1j*tv*V)*f)
    ratios.append(norm(Em/tv**2 - comm/2)/norm(comm/2))
report('A9 limite: E^mult(t) f / t^2 -> (1/2)[H0,V] f, scarto relativo O(t) (t = 1e-2, 1e-3, 1e-4)', ratios[2] < 2e-3 and ratios[0]/ratios[1] > 5 and ratios[1]/ratios[2] > 5, ratios)

# ---------- 6. NS-EQUIV su Omega limitato: lente (H = -1/2 d2 + 1/2 x^2) e Avron-Herbst, condizioni al bordo
v = sp.Function('v')
tau_ = sp.tan(t); yy = x/sp.cos(t)
pref = sp.cos(t)**sp.Rational(-1, 2)*sp.exp(-sp.I*x**2*sp.tan(t)/2)
u_lens = pref*v(tau_, yy)
ux = sp.diff(u_lens, x)
vy = sp.Subs(sp.Derivative(v(sp.Symbol('T'), sp.Symbol('Y')), sp.Symbol('Y')), (sp.Symbol('T'), sp.Symbol('Y')), (tau_, yy))
pred = pref*(-sp.I*x*sp.tan(t)*v(tau_, yy) + vy/sp.cos(t))
report('NS-EQ lente: u_x = pref*(-i x tan t v + v_y / cos t) (Neumann -> Robin)', sp.simplify((ux - pred).doit()) == 0)
# Avron-Herbst nella normalizzazione del progetto (i u_t = -u_xx + F x u): u = exp(-iFtx - iF^2t^3/3) v(t, x + F t^2)
u_ah = sp.exp(-sp.I*F*t*x - sp.I*F**2*t**3/3)*v(t, x + F*t**2)
ux = sp.diff(u_ah, x)
vy = sp.Subs(sp.Derivative(v(t, sp.Symbol('Y')), sp.Symbol('Y')), sp.Symbol('Y'), x + F*t**2)
pred = sp.exp(-sp.I*F*t*x - sp.I*F**2*t**3/3)*(-sp.I*F*t*v(t, x + F*t**2) + vy)
report('NS-EQ Avron-Herbst: u_x = e^{...}(-iFt v + v_y) (Neumann -> Robin v_y = iFt v)', sp.simplify((ux - pred).doit()) == 0)
# A-H: verifica che u risolva i u_t = -u_xx + F x u quando v e' libera (v = onda piana)
kk_ = sp.Symbol('k', real=True)
vfree = lambda T, Y: sp.exp(sp.I*kk_*Y - sp.I*kk_**2*T)
u2 = sp.exp(-sp.I*F*t*x - sp.I*F**2*t**3/3)*vfree(t, x + F*t**2)
r = sp.simplify((sp.I*sp.diff(u2, t) + sp.diff(u2, x, 2) - F*x*u2)/u2)
report('NS-EQ Avron-Herbst: onda piana libera -> soluzione con V = F x', r == 0, r)
# lente: periodo. Oscillatore H = -1/2 d2 + 1/2 x^2: e^{-i pi H} h_n = e^{-i pi (n+1/2)} h_n = -i (-1)^n h_n = -i P h_n
nn = sp.Symbol('n', integer=True, nonnegative=True)
report('NS-EQ lente: e^{-i pi (n+1/2)} = -i (-1)^n per n = 0..20 (quindi U(pi) = -i P)', all(abs(complex(sp.N(sp.exp(-sp.I*sp.pi*(n_ + sp.Rational(1, 2))) + sp.I*(-1)**n_))) < 1e-14 for n_ in range(21)))
# immagine del dominio: |x| < b, |t| < pi/2  ->  |y| < b sqrt(1 + tau^2): stellato rispetto all'origine, non convesso
bb = 1.0
inside = lambda T, Y: abs(Y) < bb*np.sqrt(1 + T**2)
Tq = 3.0; Yq = bb*np.sqrt(1 + Tq**2) - 1e-3
nonconvex = inside(Tq, Yq) and inside(-Tq, Yq) and not inside(0.0, Yq)
rng = np.random.default_rng(0); star = True
for _ in range(20000):
    T0, Y0 = rng.uniform(-5, 5), rng.uniform(-6, 6)
    if inside(T0, Y0):
        sv = rng.uniform(0, 1)
        star = star and inside(sv*T0, sv*Y0)
report('NS-EQ lente: immagine di un rettangolo non convessa ma stellata (test a campione)', nonconvex and star)

# ---------- 7. Foldy-Wouthuysen, Dirac 1+1 libero: H = alpha p + beta m, alpha = sigma_x, beta = sigma_z
p, m = sp.symbols('p m', positive=True)
sx = sp.Matrix([[0, 1], [1, 0]]); sz = sp.Matrix([[1, 0], [0, -1]])
Hd = sx*p + sz*m
En = sp.sqrt(p**2 + m**2)
th = sp.atan(p/m)/2
Ufw = sp.cos(th)*sp.eye(2) + sz*sx*sp.sin(th)
Hfw = sp.simplify(Ufw*Hd*Ufw.H)
report('FW: U H U^dag = beta sqrt(p^2+m^2), U = exp(beta alpha theta), tan 2theta = p/m', sp.simplify(Hfw - sz*En) == sp.zeros(2), Hfw)
report('FW: U unitario', sp.simplify(Ufw*Ufw.H) == sp.eye(2))
# il moltiplicatore e' non polinomiale in p: sin(theta) non e' razionale in p
report('FW: entrate di U non razionali in p (moltiplicatore non locale)', not sp.simplify(sp.sin(th)**2).is_rational_function(p), sp.simplify(sp.sin(th)**2))

# ---------- 8. Faddeev a energia fissata su [0,1]: u = u0 + G0(V u), u_i = G0(V_i u); E^add / eps^2 -> sum_{i!=j} G0 V_i G0 V_j u0
kv = 3.0; lamv = kv**2
xg = np.linspace(0, 1, 4001); h = xg[1] - xg[0]
V1 = 8*np.exp(-((xg - 0.3)/0.08)**2); V2 = -6*np.exp(-((xg - 0.7)/0.1)**2)
u0 = np.exp(1j*kv*xg)
def G0(fv):
    # (G0 f)(x) = int_0^x sin(k(x-y))/k f(y) dy ; w'' + k^2 w = f, w(0)=w'(0)=0
    out = np.zeros_like(fv, dtype=complex)
    for i in range(1, len(xg)):
        integ = np.sin(kv*(xg[i] - xg[:i+1]))/kv*fv[:i+1]
        out[i] = h*(integ.sum() - 0.5*(integ[0] + integ[-1]))
    return out
def lippmann(Vv, it=60):
    u = u0.copy()
    for _ in range(it): u = u0 + G0(Vv*u)
    return u
def ode(Vfun):
    def rhs(xx, Y): return [Y[1], (Vfun(xx) - lamv)*Y[0]]
    sol = solve_ivp(rhs, [0, 1], [1+0j, 1j*kv], t_eval=xg, rtol=1e-11, atol=1e-12)
    return sol.y[0]
Vtot = V1 + V2
u_ls = lippmann(Vtot)
u_ex = ode(lambda xx: 8*np.exp(-((xx - 0.3)/0.08)**2) - 6*np.exp(-((xx - 0.7)/0.1)**2))
report('FAD: Lippmann-Schwinger di Volterra converge senza piccolezza (vs ODE)', np.max(np.abs(u_ls - u_ex)) < 1e-4, np.max(np.abs(u_ls - u_ex)))
comp1, comp2 = G0(V1*u_ls), G0(V2*u_ls)
report('FAD: u = u0 + u^(1) + u^(2) (componenti di Faddeev)', np.max(np.abs(u_ls - u0 - comp1 - comp2)) < 1e-10)
eps_list = [0.1, 0.05, 0.025]; errs = []
pred2 = G0(V1*G0(V2*u0)) + G0(V2*G0(V1*u0))
for ep in eps_list:
    uE = lippmann(ep*Vtot); u1E = lippmann(ep*V1); u2E = lippmann(ep*V2)
    Eadd = uE - u1E - u2E + u0
    errs.append(np.max(np.abs(Eadd/ep**2 - pred2)))
report('FAD: E^add/eps^2 -> G0V1G0V2u0 + G0V2G0V1u0 (errore O(eps))', errs[2] < errs[1] < errs[0] and errs[0]/errs[2] > 3, errs)


# ---------- 9. Poschl-Teller, nucleo con erfc di U0(t)(L0+1)^{-1}: verifica SIMBOLICA (ramo sqrt(it) = e^{i pi/4} sqrt t)
zz = sp.Symbol('z', real=True)
rr_ = sp.exp(sp.I*sp.pi/4)*sp.sqrt(t)
Gk = sp.exp(sp.I*t)/4*(sp.exp(-zz)*sp.erfc(rr_ - zz/(2*rr_)) + sp.exp(zz)*sp.erfc(rr_ + zz/(2*rr_)))
K0z = (4*sp.pi*sp.I*t)**sp.Rational(-1, 2)*sp.exp(sp.I*zz**2/(4*t))
e2 = sp.simplify(sp.expand(-sp.diff(Gk, zz, 2) + Gk))
ratio2 = sp.simplify(e2/K0z)
report('PT simbolico: (1 - d_z^2) G = K0 (nucleo libero)', abs(complex(sp.N(ratio2)) - 1) < 1e-15, ratio2)
e1 = sp.simplify(sp.expand(sp.I*sp.diff(Gk, t) + sp.diff(Gk, zz, 2)))
report('PT simbolico: i G_t + G_zz = 0', e1 == 0, e1)

print('\nTOTALE: %d/%d OK' % (sum(1 for _, o in res if o), len(res)))
