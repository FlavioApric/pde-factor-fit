# S-CHECK-F8-ENC — controlli indipendenti sul pacchetto S8-ENC (27/10/2026).
# Esecuzione: D:\ProblemaBase\.venv\Scripts\python.exe -I work/CHECK-F8/sympy/enc_check_f8.py
# Nessuno script della sessione autrice e' importato: tutto e' ricostruito dagli enunciati.
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import sympy as sp
import numpy as np
import mpmath as mp

ok_all = []
def report(tag, cond, msg=""):
    ok_all.append(bool(cond))
    print(f"[{'OK' if cond else 'FAIL'}] {tag} {msg}")

x, s, xi, eta, a_, b_, r = sp.symbols('x s xi eta alpha beta r')
I = sp.I

# ------------------------------------------------------------------ ENC-1 (G), (2), (3)
# Picard simbolico per q polinomiale complesso: Phi(xi,eta), K(x,s) = Phi(x+s, x-s).
q_expr = sp.Rational(3, 2) - x/3 + sp.Rational(5, 7)*x**2 + I*x
qf = sp.Lambda(x, q_expr)
NT = 6   # iterazioni: K esatto fino al grado 2*NT, getti di T f esatti fino all'ordine 2*NT+1

def picard(sign, arg):
    # sign=+1: K (Phi_xi_eta = q((xi+eta)/2) Phi / 4); sign=-1: H (= -q((xi-eta)/2) Psi / 4)
    phi0 = sign*sp.Rational(1, 2)*sp.integrate(qf(r), (r, 0, xi/2))
    tot, d = phi0, phi0
    for _ in range(NT):
        integrand = sp.expand(qf(arg(a_, b_))*d.subs({xi: a_, eta: b_}, simultaneous=True))
        d = sign*sp.Rational(1, 4)*sp.integrate(sp.integrate(integrand, (b_, 0, eta)), (a_, 0, xi))
        d = sp.expand(d)
        tot += d
    return sp.expand(tot)

Phi = picard(+1, lambda al, be: (al + be)/2)
Psi = picard(-1, lambda al, be: (al - be)/2)
K = sp.expand(Phi.subs({xi: x + s, eta: x - s}, simultaneous=True))
H = sp.expand(Psi.subs({xi: x + s, eta: x - s}, simultaneous=True))

def low(e, var, deg):
    # parte di grado totale <= deg (in x, s)
    p = sp.Poly(sp.expand(e), x, s)
    return sum(c*x**i*s**j for (i, j), c in p.terms() if i + j <= deg)

DEG = 2*NT
resK = low(sp.diff(K, x, 2) - sp.diff(K, s, 2) - q_expr*K, None, DEG - 1)
report("E1a", sp.expand(resK) == 0 and sp.expand(K.subs(s, -x)) == 0
       and sp.expand(K.subs(s, x) - sp.integrate(q_expr, (x, 0, x))/2) == 0,
       "K: K_xx-K_ss=qK (fino al grado troncato), K(x,-x)=0, K(x,x)=(1/2)int_0^x q  [q complesso]")
qs = q_expr.subs(x, s)
resH = low(sp.diff(H, x, 2) - sp.diff(H, s, 2) + qs*H, None, DEG - 1)
report("E1b", sp.expand(resH) == 0 and sp.expand(H.subs(s, -x)) == 0
       and sp.expand(H.subs(s, x) + sp.integrate(q_expr, (x, 0, x))/2) == 0,
       "H: H_xx-H_ss=-q(s)H, H(x,-x)=0, H(x,x)=-(1/2)int_0^x q")

# T e^{k.} contro la soluzione in serie di -y''+qy=-k^2 y, y(0)=1, y'(0)=k
k = sp.Rational(2, 3)
ORD = 2*NT + 1
ek = sum((k*s)**m/sp.factorial(m) for m in range(ORD + 3))
Tek = sp.expand(ek.subs(s, x) + sp.integrate(sp.expand(K*ek), (s, -x, x)))
# serie della ODE: y'' = (q + k^2) y
c = [sp.Integer(1), k] + [0]*(ORD + 2)
qp = sp.Poly(q_expr, x).all_coeffs()[::-1]
for n in range(ORD):
    # coefficiente di x^n in (q+k^2) y
    acc = k**2*c[n] + sum(qp[j]*c[n - j] for j in range(len(qp)) if n - j >= 0)
    c[n + 2] = sp.nsimplify(acc/((n + 2)*(n + 1)))
yser = sum(c[n]*x**n for n in range(ORD + 1))
diffT = [sp.simplify(sp.Poly(Tek, x).coeff_monomial(x**n) - c[n]) for n in range(ORD + 1)]
report("E1c", all(d == 0 for d in diffT),
       f"T e^(k.) = soluzione con dati (1,k) in 0, coefficienti di Taylor uguali fino all'ordine {ORD}: L_q T = T L_0 e dati di Cauchy")
Wy = sp.expand(yser + sp.integrate(sp.expand(H*yser.subs(x, s)), (s, -x, x)))
diffW = [sp.simplify(sp.Poly(Wy, x).coeff_monomial(x**n) - k**n/sp.factorial(n)) for n in range(ORD + 1)]
report("E1d", all(d == 0 for d in diffW), f"W y = e^(k.) fino all'ordine {ORD}: W = T^(-1) con il nucleo H di ENC-1(3)")

# ------------------------------------------------------------------ ENC-U1: coefficiente B
# K arbitrario (non di Goursat), f polinomiale: L_q T f - T L_0 f = A f(x) + B f(-x) + int C f
Kg = 1 + x**2*s + s**3 + 2*x*s
qg = x + 1
f = sp.Lambda(s, 1 + 2*s + 3*s**2 + 5*s**3 + s**4)
g = f(x) + sp.integrate(Kg*f(s), (s, -x, x))
lhs = -sp.diff(g, x, 2) + qg*g + sp.diff(f(x), x, 2) + sp.integrate(Kg*sp.diff(f(s), s, 2), (s, -x, x))
A = qg - 2*sp.diff(Kg.subs(s, x), x)
B_true = -2*sp.diff(Kg.subs(s, -x), x)
B_pkg = -sp.diff(Kg.subs(s, -x), x)
C = sp.diff(Kg, s, 2) - sp.diff(Kg, x, 2) + qg*Kg
rhs = lambda B: A*f(x) + B*f(-x) + sp.integrate(C*f(s), (s, -x, x))
report("U1a", sp.expand(lhs - rhs(B_true)) == 0 and sp.expand(lhs - rhs(B_pkg)) != 0,
       "B = -2 d/dx K(x,-x) (il pacchetto scrive -d/dx K(x,-x): refuso di un fattore 2, conclusione invariata)")
# T_{k0} con q = 0: K = k0 commuta con L_0
k0 = sp.Symbol('k0')
g0 = f(x) + k0*sp.integrate(f(s), (s, -x, x))
report("U1b", sp.expand(-sp.diff(g0, x, 2) - (-sp.diff(f(x), x, 2) - k0*sp.integrate(sp.diff(f(s), s, 2), (s, -x, x)))) == 0
       and sp.expand(sp.diff(g0, x).subs(x, 0) - (sp.diff(f(x), x).subs(x, 0) + 2*k0*f(0))) == 0,
       "q=0: I + k0 int_{-x}^{x} commuta con L_0 e (T f)'(0) = f'(0) + 2 k0 f(0)")

# ------------------------------------------------------------------ ENC-1(6) punto base
cq, kk, x0n, x1n, xe = 2.0, 1.5, 0.0, 0.2, 1/3
mu = np.sqrt(kk**2 - cq + 0j)
Tb = lambda xb, xx: np.exp(1j*kk*xb)*(np.cos(mu*(xx - xb)) + 1j*kk*np.sin(mu*(xx - xb))/mu)
dd = Tb(x0n, xe) - Tb(x1n, xe)
report("E6", abs(dd - (0.092 + 0.012j)) < 5e-3, f"T^(0) e^(ik.)(1/3) - T^(1/5) e^(ik.)(1/3) = {dd:.4f}")

# ------------------------------------------------------------------ ENC-T2(c): getti in x_0 e fuori da x_0
# Getti in 0 di T f per f polinomiale: (Tf)^(n)(0) = f^(n)(0) + sum_{j<=n-2} c_{n,j} f^(j)(0)
fj = sp.symbols('f0:10')
fpoly = sum(fj[m]*s**m/sp.factorial(m) for m in range(10))
Tf = sp.expand(fpoly.subs(s, x) + sp.integrate(sp.expand(K*fpoly), (s, -x, x)))
tri = True
for n in range(0, 8):
    dn = sp.expand(sp.diff(Tf, x, n).subs(x, 0))
    # coefficiente di f_n deve essere 1, di f_{n-1} deve essere 0, di f_m (m>n) 0
    if sp.expand(dn.coeff(fj[n]) - 1) != 0: tri = False
    if n >= 1 and sp.expand(dn.coeff(fj[n - 1])) != 0: tri = False
    for m in range(n + 1, 10):
        if sp.expand(dn.coeff(fj[m])) != 0: tri = False
report("T2c1", tri, "getti in x_0 di T f: unipotenti e con banda j <= n-2, ordini 0..7 (induzione del pacchetto confermata oltre l'ordine 3)")
# fuori da x_0: h0 = (x - x1)^M ha getto nullo in x1 ma T h0 no
x1 = sp.Rational(1, 5)
Mh = 4
h0 = (s - x1)**Mh
Th0 = sp.expand(h0.subs(s, x) + sp.integrate(sp.expand(K*h0), (s, -x, x)))
jet = [sp.N(sp.diff(Th0, x, n).subs(x, x1)) for n in range(3)]
report("T2c2", any(abs(complex(v)) > 1e-8 for v in jet),
       f"in x_1 = 1/5 != x_0: j^2 h0 = 0 ma j^2(T h0) = {[complex(v) for v in jet]} != 0 (la prova di (c) vale solo in x_0)")
# prova alternativa in ogni punto: P(alpha, L_q)(x - x1)^M ha termine di grado minimo c (x-x1)^(M-2d) != 0
sig = sp.Symbol('sigma')
Lq = lambda u: -sp.diff(u, x, 2) + q_expr*u
u = (x - x1)**8
v = Lq(Lq(u)) + 3*Lq(u)          # P(alpha, sigma) = sigma^2 + 3 sigma (d = 2)
vv = sp.expand(v.subs(x, x1 + r))
report("T2c3", sp.expand(vv.coeff(r, 4) - sp.factorial(8)/sp.factorial(4)) == 0 and all(vv.coeff(r, j) == 0 for j in range(4)),
       "P(alpha,L_q)(x-x1)^8 = (8!/4!)(x-x1)^4 + ordini superiori: non certificabilita' in ogni punto, senza W")

# ------------------------------------------------------------------ ENC-T2(b) parita' di lcm
tau, X = sp.symbols('tau xi')
def gen(Q):
    Qt = Q.subs(X, -X)
    L = sp.lcm(Q, Qt)
    if sp.expand(L.subs(X, -X) - L) == 0: return sp.factor(L)
    return sp.factor(X*L)
report("T2b", gen(tau + X - 1) == sp.factor((tau + X - 1)*(tau - X - 1)) and gen(X) == X**2 and gen(tau + X**2) == tau + X**2,
       "generatore: lcm(Q,Q~) se pari, xi*lcm se dispari (Q = xi -> xi^2)")

# ------------------------------------------------------------------ ENC-A9(b2): stima e costante 2/3
F, t = 1.0, 1.0
Lx, N = 600.0, 2**16
xs = np.linspace(-Lx, Lx, N, endpoint=False); dx = xs[1] - xs[0]
p = 2*np.pi*np.fft.fftfreq(N, d=dx)
sig_ = 25.0
f0 = np.exp(-xs**2/(2*sig_**2)); f0 /= np.sqrt(np.sum(abs(f0)**2)*dx)
nrm = lambda w: np.sqrt(np.sum(abs(w)**2)*dx)
U0 = lambda w, tt: np.fft.ifft(np.exp(-1j*tt*p**2)*np.fft.fft(w))
# U(t) f con la formula di Avron-Herbst (verificata sotto in modo simbolico), U_0 f gaussiano in forma chiusa
def U0gauss(xx, tt):
    z = sig_**2 + 2j*tt
    return np.sqrt(sig_**2/z)*np.exp(-xx**2/(2*z))/np.sqrt(np.sqrt(np.pi)*sig_)
Uf = np.exp(-1j*t*F*xs - 1j*F**2*t**3/3)*U0gauss(xs + F*t**2, t)
Emf = Uf - U0(np.exp(-1j*t*F*xs)*f0, t)
fp = np.fft.ifft(1j*p*np.fft.fft(f0))
E_norm = nrm(Emf)
bound_pkg = F*t**2*nrm(fp) + F**2*t**3/6*nrm(f0)
bound_ok = F*t**2*nrm(fp) + 2*F**2*t**3/3*nrm(f0)
exact = nrm(np.fft.ifft((1 - np.exp(1j*(F*t**2*p - 2*F**2*t**3/3)))*np.fft.fft(f0)))
report("A9b2a", E_norm > bound_pkg, f"V=Fx, f gaussiana larga: ||E^mult f|| = {E_norm:.4f} > {bound_pkg:.4f} (stima di (b2) FALSA)")
report("A9b2b", abs(E_norm - exact) < 1e-6 and E_norm <= bound_ok + 1e-9,
       f"||E^mult f|| = ||(1 - e^(i(Ft^2 p - 2F^2t^3/3))) f|| = {exact:.4f} <= Ft^2||f'|| + (2/3)F^2t^3||f|| = {bound_ok:.4f}")
# nitidezza della costante 2/3 in ENC-A9(a): con la formula esatta (A9b2b), f gaussiana di larghezza sigma,
# ||E f|| / (F t^2 ||f'|| + (2/3) F^2 t^3 ||f||) -> 1 per sigma -> inf e t -> 0
def ratio_exact(tt, sg):
    pq = np.linspace(-40/sg, 40/sg, 400001); dp = pq[1] - pq[0]
    fh2 = np.exp(-(pq*sg)**2)            # |f^(p)|^2 a meno di costante
    nf = np.sqrt(np.sum(fh2)*dp); nfp = np.sqrt(np.sum(pq**2*fh2)*dp)
    nE = np.sqrt(np.sum(abs(1 - np.exp(1j*(F*tt**2*pq - 2*F**2*tt**3/3)))**2*fh2)*dp)
    return nE/(F*tt**2*nfp + 2*F**2*tt**3/3*nf)
ratios = [ratio_exact(tt, sg) for tt, sg in [(0.3, 1e2), (0.1, 1e3), (0.03, 1e5)]]
report("A9a", ratios[-1] > 0.99 and max(ratios) <= 1 + 1e-9,
       f"||E^mult f|| / (F t^2||f'|| + (2/3)F^2 t^3||f||) = {[round(v, 5) for v in ratios]} -> 1: la costante 2/3 di ENC-A9(a) e' ottimale (V = Fx)")

# Avron-Herbst simbolico (normalizzazione del progetto) e forma ½ di F6-ENC NOTE §5
tt, Fs, kk_ = sp.symbols('t F k', real=True)
vfree = sp.exp(I*kk_*x - I*kk_**2*tt)                       # i v_t = -v_yy
uAH = sp.exp(-I*Fs*tt*x - I*Fs**2*tt**3/3)*vfree.subs(x, x + Fs*tt**2)
report("AH1", sp.simplify((I*sp.diff(uAH, tt) + sp.diff(uAH, x, 2) - Fs*x*uAH)/uAH) == 0,
       "u = e^(-iFtx - iF^2t^3/3) v(t, x+Ft^2) risolve i u_t = -u_xx + Fxu")
vhalf = sp.exp(I*kk_*x - I*kk_**2*tt/2)                     # i v_t = -½ v_yy
uAHh = sp.exp(-I*Fs*tt*x - I*Fs**2*tt**3/6)*vhalf.subs(x, x + Fs*tt**2/2)
report("AH2", sp.simplify((I*sp.diff(uAHh, tt) + sp.diff(uAHh, x, 2)/2 - Fs*x*uAHh)/uAHh) == 0
       and sp.simplify((I*sp.diff(uAHh, tt) + sp.diff(uAHh, x, 2) - Fs*x*uAHh)/uAHh) != 0,
       "la formula di F6-ENC NOTE §5 (Ft^2/2, F^2t^3/6) vale per H = -½d² + Fx e non per H = -d² + Fx: errata confermata")
# Fourier: fase F^2 t^3/12 di Strang
pp = sp.Symbol('p', real=True)
phi_ex = pp**2*tt + pp*Fs*tt**2 + Fs**2*tt**3/3
report("AH3", sp.expand(sp.diff(phi_ex, tt) - Fs*sp.diff(phi_ex, pp) - pp**2) == 0
       and sp.expand(phi_ex - tt*(pp + Fs*tt/2)**2 - Fs**2*tt**3/12) == 0,
       "fase esatta p^2t + pFt^2 + F^2t^3/3 e differenza con Strang = F^2t^3/12")

# ------------------------------------------------------------------ NS-EQUIV-Omega
uf = sp.Function('u')
yv = sp.Symbol('y', real=True)
# Avron-Herbst: v(t,y) = e^{i phi} u(t, y - F t^2); coniugati di d_y e d_t
ph = Fs*tt*(yv - Fs*tt**2) + Fs**2*tt**3/3
vv_ = sp.exp(I*ph)*uf(tt, yv - Fs*tt**2)
Xs = sp.Symbol('X')
def back(expr):
    return sp.simplify((sp.exp(-I*ph)*expr).subs(yv, Xs + Fs*tt**2))
dy = back(sp.diff(vv_, yv))
dt = back(sp.diff(vv_, tt))
u_ = uf(tt, Xs)
ux = sp.diff(u_, Xs); ut = sp.diff(u_, tt)
report("NS1", sp.simplify(dy - (ux + I*Fs*tt*u_)) == 0,
       "Avron-Herbst: Phi^-1 d_y Phi = d_x + iFt, Neumann u_x = 0 <=> v_y = iFt v")
report("NS2", sp.simplify(dt - (ut - 2*Fs*tt*ux + I*Fs*Xs*u_ - I*Fs**2*tt**2*u_)) == 0,
       "Avron-Herbst: Phi^-1 d_t Phi = d_t - 2Ft d_x + iFx - iF^2t^2 (coefficienti polinomiali in (t,x), non solo in t)")
# lente: u = (cos t)^(-1/2) e^{-i x^2 tan t/2} v(tan t, x/cos t), con v libera per -½d²
y_, ta = sp.symbols('y tau')
for vname, vfun in [("gauss", (1 + I*ta)**sp.Rational(-1, 2)*sp.exp(-y_**2/(2*(1 + I*ta)))),
                    ("onda", sp.exp(I*kk_*y_ - I*kk_**2*ta/2))]:
    ul = sp.cos(tt)**sp.Rational(-1, 2)*sp.exp(-I*x**2*sp.tan(tt)/2)*vfun.subs({ta: sp.tan(tt), y_: x/sp.cos(tt)}, simultaneous=True)
    res = sp.simplify((I*sp.diff(ul, tt) + sp.diff(ul, x, 2)/2 - x**2*ul/2)/ul)
    report(f"NS3-{vname}", res == 0, "lente: u risolve i u_t = -½u_xx + ½x²u")
# Robin della lente
vg = sp.Function('v')
ul = sp.cos(tt)**sp.Rational(-1, 2)*sp.exp(-I*x**2*sp.tan(tt)/2)*vg(sp.tan(tt), x/sp.cos(tt))
uxl = sp.diff(ul, x)
pref = sp.cos(tt)**sp.Rational(-1, 2)*sp.exp(-I*x**2*sp.tan(tt)/2)
vy = sp.Subs(sp.Derivative(vg(ta, y_), y_), (ta, y_), (sp.tan(tt), x/sp.cos(tt))).doit()
expr = sp.simplify(uxl/pref - (vy - I*x*sp.sin(tt)*vg(sp.tan(tt), x/sp.cos(tt)))/sp.cos(tt))
report("NS4", expr == 0, "lente: u_x = 0 <=> v_y = i x sin t v = i y sin t cos t v")
# stellatezza e non convessita' (J = (-b,b), I contiene 0)
report("NS5", all(sv*np.sqrt(1 + T**2) <= np.sqrt(1 + (sv*T)**2) + 1e-15 for sv in np.linspace(0, 1, 21) for T in np.linspace(-20, 20, 41)),
       "s sqrt(1+tau^2) <= sqrt(1+s^2 tau^2) per s in [0,1]")
# U(pi) = -iP per H = -½d² + ½x² = ½(-d² + x²)
report("NS6", all(abs(np.exp(-1j*np.pi*(n + 0.5)) - (-1j)*(-1)**n) < 1e-12 for n in range(10))
       and all(abs(np.exp(-1j*(np.pi/2)*(2*n + 1)) - (-1j)*(-1)**n) < 1e-12 for n in range(10)),
       "U_(½)(pi) = U_VAR(pi/2) = -iP: coerente con VAR-T10 (H = -d² + x², periodo pi/2)")

# ------------------------------------------------------------------ ENC-A9(b4): nucleo erfc
def Gpkg(tv, z):
    w = mp.sqrt(1j*tv)
    return mp.e**(1j*tv)/4*(mp.e**(-z)*mp.erfc(w - z/(2*w)) + mp.e**(z)*mp.erfc(w + z/(2*w)))
def Gfourier(tv, z, Kc=400.0, n=4_000_001):
    kq = np.linspace(-Kc, Kc, n)
    integrand = np.exp(-1j*tv*kq**2 + 1j*kq*z)/(1 + kq**2)
    h = kq[1] - kq[0]
    val = h*(np.sum(integrand) - 0.5*(integrand[0] + integrand[-1]))
    return val/(2*np.pi)
errs = []
for tv, z in [(0.5, 0.0), (0.5, 1.3), (1.2, -2.0), (0.3, 4.0)]:
    errs.append(abs(complex(Gpkg(tv, z)) - Gfourier(tv, z)))
report("B4a", max(errs) < 2e-4, f"G(t,z) = trasformata inversa di e^(-itk^2)/(1+k^2) in 4 punti, errore max {max(errs):.1e}")
report("B4b", abs(complex(Gpkg(1e-12, 0.7)) - 0.5*np.exp(-0.7)) < 1e-5 and abs(complex(Gpkg(0.7, 60.0))) < 0.05,
       "G(0+,z) = ½e^(-|z|); |G(t,z)| -> 0 per |z| grande (temperata, decadimento ~1/|z|)")

# ------------------------------------------------------------------ FW-1
th, pm, mm = sp.symbols('theta p m', positive=True)
sx = sp.Matrix([[0, 1], [1, 0]]); sz = sp.Matrix([[1, 0], [0, -1]])
Uw = sp.cos(th)*sp.eye(2) + sz*sx*sp.sin(th)
Hd = sx*pm + sz*mm
R = sp.simplify(Uw*Hd*Uw.H)
th0 = sp.atan(pm/mm)/2
Rs = sp.simplify(R.subs(th, th0))
report("FW", sp.simplify(Uw*Uw.H - sp.eye(2)) == sp.zeros(2) and sp.simplify(Rs - sz*sp.sqrt(pm**2 + mm**2)) == sp.zeros(2),
       "U = cos th + beta alpha sin th unitario, U H U^+ = beta E con tan 2th = p/m")


print(f"\nTotale: {sum(ok_all)}/{len(ok_all)} OK")
