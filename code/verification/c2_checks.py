# S-CHECK-F10-C2: controlli indipendenti sulle prove riscritte R.1 (C-15), R.2 (C-17), R.3 (C-19)
# di work/S10-OPEN-C/PROOF_PACKAGE.md, rev2. Solo controlli: il verdetto si basa sulla rilettura a mano.
# Metodi diversi da rev2_checks.py: esempi espliciti (Tychonoff troncata, gaussiana, boost),
# discretizzazione dell'operatore di Volterra simmetrico, dominio a L non convesso per il cono.
import math
import random
import sys

import numpy as np
import sympy as sp

sys.stdout.reconfigure(encoding="utf-8")
res = []


def ok(name, cond):
    res.append((name, bool(cond)))
    print(("OK  " if cond else "FAIL"), name)


I = sp.I
t, x = sp.symbols('t x', real=True)


def L0(f):
    return sp.simplify(I*sp.diff(f, t) + sp.diff(f, x, 2))


# =========================================================================== R.1 (C-15)
# (1) La lacuna è reale: serie di Tychonoff u = Σ g^{(k)}(t)(-i)^k x^{2k}/(2k)!, con g piatta in 0.
#     La troncata all'ordine K ha residuo L_0 = solo il termine di coda, e u(t,·) ≡ 0 per t ≤ 0.
gs = sp.Function('g')
K = 6
uT = sum(sp.diff(gs(t), t, k)*(-I)**k*x**(2*k)/sp.factorial(2*k) for k in range(K + 1))
tail = I*sp.diff(gs(t), t, K + 1)*(-I)**K*x**(2*K)/sp.factorial(2*K)
ok("C-15 Tychonoff troncata: L_0 u_K = solo il termine di coda (K = 6)",
   sp.simplify(I*sp.diff(uT, t) + sp.diff(uT, x, 2) - tail) == 0)
gflat = sp.Piecewise((sp.exp(-1/t**2), t > 0), (0, True))
ok("C-15 con g = e^{-1/t^2}1_{t>0}: u(t,·) ≡ 0 per t < 0 e u(t,0) = g(t) > 0 per t > 0",
   uT.subs(gs(t), gflat).doit().subs(t, -sp.Rational(1, 2)) == 0 and
   sp.N(gflat.subs(t, sp.Rational(1, 2))) > 0)

# (2) Passo 2 su un esempio esplicito con q_0 = 0: u = e^{-ict}(x^2+2it) ∈ S_c, u' = e^{-ic't}(x^2+2it) ∈ S_{c'}
c, cp = sp.symbols('c cp', real=True)
u = sp.exp(-I*c*t)*(x**2 + 2*I*t)
up = sp.exp(-I*cp*t)*(x**2 + 2*I*t)
ok("C-15 esempio: u ∈ S_c, u' ∈ S_c' (iu_t = -u_xx + c u)",
   sp.simplify(I*sp.diff(u, t) + sp.diff(u, x, 2) - c*u) == 0 and
   sp.simplify(I*sp.diff(up, t) + sp.diff(up, x, 2) - cp*up) == 0)
ok("C-15 esempio: u'/u = e^{-iδt}, cioè θ_1' = -δ",
   sp.simplify(up/u - sp.exp(-I*(cp - c)*t)) == 0)

# (3) Passo 4 con w esplicita e θ esplicita: L_0(e^{iθ}w) = -θ' e^{iθ} w
w = x**3 + 6*I*t*x
th = t**2 + sp.sin(t)
ok("C-15 passo 4 su esempio: L_0(e^{iθ}w) = -θ' e^{iθ} w",
   sp.simplify(L0(sp.exp(I*th)*w) + sp.diff(th, t)*sp.exp(I*th)*w) == 0)

# (4) Passi 6-7: operatore di Volterra simmetrico discretizzato su [-a,a] con nucleo limitato.
#     Raggio spettrale numerico → 0 al raffinarsi della griglia; Z = I + V non ha autovalori μ con |μ| = 1, μ ≠ 1
#     lontani da 1 (spettro di Z concentrato in 1).
rng = np.random.default_rng(7)
a = 1.0


def volterra_sym(n, kern):
    xs = np.linspace(-a, a, n)
    h = xs[1] - xs[0]
    M = np.zeros((n, n), dtype=complex)
    for i, xi in enumerate(xs):
        for j, rj in enumerate(xs):
            if abs(rj) < abs(xi) - 1e-12:
                M[i, j] = kern(xi, rj)*h
    return M


kern = lambda xi, r: 3.0*np.cos(2*xi + r) + 2j*np.sin(xi*r) + 1.0
radii = []
for n in (41, 81, 161):
    V = volterra_sym(n, kern)
    radii.append(max(abs(np.linalg.eigvals(V))))
print("    raggi spettrali discreti di V:", [float(round(r_, 6)) for r_ in radii])
# la discretizzazione con |r| < |x| stretto è nilpotente (ordinamento per |x|): V^{m} = 0 con m = numero di livelli |x|
Vn41 = volterra_sym(41, kern)
ok("C-15 passo 6: V discreto nilpotente (V^21 = 0 su 41 nodi) e raggio spettrale numerico ~ 0",
   np.abs(np.linalg.matrix_power(Vn41, 21)).max() < 1e-9 and max(radii) < 1e-6)
Vn = volterra_sym(81, kern)
nrm = [np.linalg.norm(np.linalg.matrix_power(Vn, m), np.inf) for m in range(1, 13)]
bnd = [(2*6.0*a)**m/math.factorial(m) for m in range(1, 13)]   # ‖k‖_∞ ≤ 6
ok("C-15 passo 6: ‖V^n‖_∞ ≤ (2‖k‖a)^n/n! (discreto, n ≤ 12)", all(p <= q*1.05 for p, q in zip(nrm, bnd)))

# =========================================================================== R.2 (C-17)
# (5) Derivazione di (i) passo per passo, per u libera generica: iU_t = -U_xx - 2UU_x
Uf = sp.Function('u')(t, x)
Pf = sp.Function('p')(t, x)


def red(e, funcs):
    def is_td(d):
        return isinstance(d, sp.Derivative) and d.expr in funcs and dict(d.variable_count).get(t, 0) > 0

    def rep(d):
        vc = dict(d.variable_count)
        return I**vc.get(t, 0)*sp.Derivative(d.expr, (x, vc.get(x, 0) + 2*vc.get(t, 0)))
    e = sp.expand(e.doit())
    for _ in range(4):
        e = sp.expand(e.replace(is_td, rep).doit())
    return sp.simplify(e)


Uq = sp.diff(Uf, x)/Uf
ok("C-17 (i) riga 1: iU_t = -U_xx - 2UU_x (u libera generica)",
   sp.simplify(red(I*sp.diff(Uq, t), (Uf,)) - red(-sp.diff(Uq, x, 2) - 2*Uq*sp.diff(Uq, x), (Uf,))) == 0)
chi = sp.diff(Pf, x) - Uq*Pf
ok("C-17 (i) riga 2: iχ_t = -φ_xxx - iU_tφ + Uφ_xx",
   sp.simplify(red(I*sp.diff(chi, t) - (-sp.diff(Pf, x, 3) - I*sp.diff(Uq, t)*Pf + Uq*sp.diff(Pf, x, 2)), (Uf, Pf))) == 0)
ok("C-17 (i) riga 3: χ_xx = φ_xxx - U_xxφ - 2U_xφ_x - Uφ_xx",
   sp.simplify(sp.diff(chi, x, 2) - (sp.diff(Pf, x, 3) - sp.diff(Uq, x, 2)*Pf - 2*sp.diff(Uq, x)*sp.diff(Pf, x)
                                       - Uq*sp.diff(Pf, x, 2))) == 0)

# (6) κ su una coppia diversa da quella del pacchetto: u = boost di Galileo, φ = gaussiana libera.
kk, aa = sp.Rational(1, 3), sp.Integer(5)
uG = (x - 2*kk*t + aa)*sp.exp(I*(kk*x - kk**2*t))
phG = (1 + 4*I*t)**sp.Rational(-1, 2)*sp.exp(-x**2/(1 + 4*I*t))
ok("C-17 u_G e la gaussiana sono libere", L0(uG) == 0 and L0(phG) == 0)
chiG = sp.diff(phG, x) - sp.diff(uG, x)/uG*phG
x0 = sp.Integer(1)
kap = ((sp.diff(chiG, x) + sp.diff(uG, x)/uG*chiG)/uG).subs(x, x0)
ok("C-17 (ii) ∂_t(φ/u)(t,x_0) = iκ(t) (gaussiana, boost)",
   sp.simplify(sp.diff(phG/uG, t).subs(x, x0) - I*kap) == 0)
V1 = -2*sp.diff(sp.log(uG), x, 2)
ok("C-17 (i) L_0χ = V_1χ sulla coppia (gaussiana, boost)", sp.simplify(L0(chiG) - V1*chiG) == 0)

# (7) Costruzione di ψ con quadratura numerica e test di L_0ψ = 0 per differenze finite (t, x reali, punti campione)
uN = sp.lambdify((t, x), uG, 'mpmath')
chiN = sp.lambdify((t, x), chiG, 'mpmath')
kapN = sp.lambdify(t, kap, 'mpmath')
import mpmath as mp
mp.mp.dps = 30


def psi(tt, xx, c0=mp.mpf('0.3')):
    cint = c0 + mp.quad(lambda s: 1j*kapN(s), [0, tt])
    return uN(tt, xx)*(mp.quad(lambda y: chiN(tt, y)/uN(tt, y), [x0, xx]) + cint)


hstep = mp.mpf('1e-5')
worst = 0
for (tt, xx) in [(mp.mpf('0.2'), mp.mpf('1.7')), (mp.mpf('0.5'), mp.mpf('2.3')), (mp.mpf('0.9'), mp.mpf('0.6'))]:
    pt = (psi(tt + hstep, xx) - psi(tt - hstep, xx))/(2*hstep)
    pxx = (psi(tt, xx + hstep) - 2*psi(tt, xx) + psi(tt, xx - hstep))/hstep**2
    worst = max(worst, abs(1j*pt + pxx))
print("    max |L_0 ψ| (differenze finite):", mp.nstr(worst, 3))
ok("C-17 ψ costruita con c' = iκ è libera (differenze finite, |L_0ψ| < 1e-6)", worst < 1e-6)
# e con c' sbagliato (c' = 0) non lo è
def psi_bad(tt, xx):
    return uN(tt, xx)*(mp.quad(lambda y: chiN(tt, y)/uN(tt, y), [x0, xx]))
tt, xx = mp.mpf('0.5'), mp.mpf('2.3')
pt = (psi_bad(tt + hstep, xx) - psi_bad(tt - hstep, xx))/(2*hstep)
pxx = (psi_bad(tt, xx + hstep) - 2*psi_bad(tt, xx) + psi_bad(tt, xx - hstep))/hstep**2
ok("C-17 controllo negativo: con c' = 0 ψ non è libera", abs(1j*pt + pxx) > 1e-3)

# =========================================================================== R.3 (C-19)
# (8) Passo 1 nel caso limite: Lip φ = L esatta, φ con spigolo (|·|), x arbitrariamente vicino al grafico.
random.seed(3)
Lp = 2.0
phi = lambda y: -Lp*abs(y - 0.1) + 0.3*math.sin(y) * 0  # Lip esattamente 2
good = True
for _ in range(50000):
    xp = random.uniform(-1, 1)
    xn = phi(xp) + 10**random.uniform(-12, -1)
    zp = random.uniform(-0.5, 0.5)
    zn = Lp*abs(zp) + 10**random.uniform(-12, -1)
    good &= xn + zn > phi(xp + zp)
ok("C-19 passo 1: x_N + z_N > φ(x'+z') con Lip φ = L e spigolo (50000 campioni)", good)

# (9) Conclusione del lemma su un dominio NON convesso con angolo rientrante (L-shape) in N = 2:
#     Ω = (-1,1)^2 ∖ [0,1)×(-1,0]. Con L = tan(π/2 - π/8) (semi-apertura π/8) e h = 0.05,
#     per ogni x campionato esiste una direzione (griglia di 64) con x + R Γ(L,h) ⊂ Ω (test su 200 punti del cono).
def inOm(p):
    X, Y = p
    return -1 < X < 1 and -1 < Y < 1 and not (X >= 0 and Y <= 0)


half = math.pi/8
hh = 0.05
cone_pts = []
for i in range(1, 11):
    for j in range(-10, 11):
        rr = hh*i/10.5
        al_ = half*j/10.5
        cone_pts.append((rr*math.sin(al_), rr*math.cos(al_)))


def fits(p, ang):
    ca, sa = math.cos(ang), math.sin(ang)
    return all(inOm((p[0] + ca*z1 - sa*z2, p[1] + sa*z1 + ca*z2)) for (z1, z2) in cone_pts)


good = True
cnt = 0
while cnt < 3000:
    p = (random.uniform(-1, 1), random.uniform(-1, 1))
    if not inOm(p):
        continue
    cnt += 1
    good &= any(fits(p, 2*math.pi*m/64) for m in range(64))
ok("C-19 L-shape (angolo rientrante): esiste sempre un cono congruente in Ω (3000 punti)", good)
# vicino all'angolo rientrante in particolare
good = True
for _ in range(2000):
    rr = 10**random.uniform(-8, -1)
    ang = random.uniform(0, 1.5*math.pi) + 0.0
    p = (rr*math.cos(ang + 0.0), rr*math.sin(ang))
    p = (rr*math.cos(ang), rr*math.sin(ang))
    if not inOm(p):
        continue
    good &= any(fits(p, 2*math.pi*m/64) for m in range(64))
ok("C-19 L-shape: punti a distanza 1e-8..1e-1 dall'angolo rientrante", good)

# (10) |Γ(L,r)| in N = 3 (metodo indipendente dal caso N = 2): (2π/3)r^3(1 - cos α), α = arctan(1/L)
Ls, r, rho, th_, ph_ = sp.symbols('L r rho theta phi', positive=True)
al = sp.atan(1/Ls)
vol = sp.integrate(sp.integrate(sp.integrate(rho**2*sp.sin(th_), (rho, 0, r)), (th_, 0, al)), (ph_, 0, 2*sp.pi))
ok("C-19 N = 3: |Γ(L,r)| = r^3|Γ(L,1)| = (2π/3) r^3 (1 - cos arctan(1/L))",
   sp.simplify(vol - r**3*vol.subs(r, 1)) == 0 and
   sp.simplify(vol - 2*sp.pi/3*r**3*(1 - sp.cos(al))) == 0)
# Monte Carlo per L = 1
pts = np.random.default_rng(11).uniform(-1, 1, size=(400000, 3))
inside = (pts[:, 2] > np.hypot(pts[:, 0], pts[:, 1])) & (np.linalg.norm(pts, axis=1) < 1)
mc = 8*inside.mean()
ok("C-19 N = 3, L = 1: Monte Carlo ≈ (2π/3)(1 - 1/√2)", abs(mc - 2*math.pi/3*(1 - 1/math.sqrt(2))) < 0.01)

# (11) Uniformità della costante sui polinomi ruotati (passo 3 di §13): N = 2, s = 2,
#      rapporto max_β|D^βP(0)| / ‖P‖_{L²(RΓ)} limitato uniformemente in R (24 rotazioni).
X, Y = sp.symbols('X Y', real=True)
mons = [1, X, Y, X**2, X*Y, Y**2]
Lc = 1.0
rr_, aa_ = sp.symbols('rr aa', positive=True)


def gram(angle):
    ca, sa = sp.cos(angle), sp.sin(angle)
    G = sp.zeros(6, 6)
    for i, m1 in enumerate(mons):
        for j, m2 in enumerate(mons):
            f = sp.sympify(m1*m2)
            # punto del cono ruotato: (X,Y) = R(z1,z2), z = rr(sin aa, cos aa)
            z1, z2 = rr_*sp.sin(aa_), rr_*sp.cos(aa_)
            fx = f.subs({X: ca*z1 - sa*z2, Y: sa*z1 + ca*z2}, simultaneous=True)
            G[i, j] = sp.integrate(sp.integrate(sp.expand(fx)*rr_, (rr_, 0, 1)), (aa_, -sp.pi/4, sp.pi/4))
    return np.array(G.evalf(), dtype=float)


vals = []
for m in range(0, 24, 3):
    Gm = gram(sp.pi*m/12)
    # norma del funzionale "coefficienti" rispetto alla norma L²: sqrt(λ_max(G^{-1}))
    vals.append(math.sqrt(max(np.linalg.eigvalsh(np.linalg.inv(Gm)))))
print("    costanti c_0(R) su 8 rotazioni:", [round(v, 3) for v in vals])
ok("C-19 passo 3: c_0(R) uniforme in R (max/min < 3)", max(vals)/min(vals) < 3)

nok = sum(1 for _, cnd in res if cnd)
print(f"\nTotale: {nok}/{len(res)} OK")
sys.exit(0 if nok == len(res) else 1)
