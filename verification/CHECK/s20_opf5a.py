# S-CHECK-20 — controlli numerici indipendenti per OP-F5A (evidenza, NON prova).
# (1) costante di Pearcey P (quad adattiva, metodo diverso da opf5a_check3)
# (2) Gamma(sin) a t*=1 via Hopf/Cole-Hopf indipendente, nu = 1e-4,1e-5,1e-6
# (3) T1/T2: D(nu,s) = e/nu - 2 log(1/max(|t-1|,sqrt nu)) per t = 1 -/+ K sqrt(nu) e |t-1| = nu^(1/3), 0.05
# (4) T5: costante di t^{k/2+3/4} per c=0.7, D=0.3 (testa gli esponenti di D e la dipendenza da c), k=1,2
import sys, time
import numpy as np
from scipy import integrate
T0 = time.time()
def log(*a):
    print(*a); sys.stdout.flush()

# ---------------- (1) Pearcey
def m_of(b):
    # media di z per e^{-Q}, Q = z^4/12 + b z^3/3 + b^2 z^2/2 (minimo in z=0, Q>=0)
    Q = lambda z: z**4/12 + b*z**3/3 + b*b*z*z/2
    s = 1.0/max(1.0, abs(b))
    lim = 12.0*s + 6.0
    num = integrate.quad(lambda z: z*np.exp(-Q(z)), -lim, lim, points=[0.0], limit=400, epsabs=1e-15, epsrel=1e-12)[0]
    den = integrate.quad(lambda z: np.exp(-Q(z)), -lim, lim, points=[0.0], limit=400, epsabs=1e-15, epsrel=1e-12)[0]
    return num/den
# m(-b) = -m(b): integrando pari
def F(B):
    f = lambda b: b*b*abs(m_of(b))
    pts = [0.5, 1, 2, 4, 8, 16, 32, 64, 128]
    pts = [p for p in pts if p < B]
    return 4*integrate.quad(f, 0, B, points=pts, limit=800, epsrel=1e-11)[0]
log("(1) Pearcey: m(b)*b^3 per b grande (atteso -> -1):", [round(m_of(b)*b**3, 6) for b in (10.0, 30.0, 100.0)])
for B in (10.0, 20.0, 40.0, 80.0):
    PB = F(B) - 4*np.log(B)
    # coda: 2 b^2|m| = 2/b + c3/b^3 ... => F(inf-correction) ~ -c/B^2 ; stima c da differenze
    log(f"    B={B:5.0f}: P_B = {PB:.7f}")
Gamma_sin = 2*np.log(2.0)  # Gamma_out + log(kappa3/4) = 4log2 - log4
# ---------------- (2)-(3) Hopf per u0 = sin x
def amin(x, t):
    # minimizzante di Phi_x(y) = 1 - cos y + (x-y)^2/2t, x in (pi, 2pi]; ramo destro se t>1
    if t <= 1:
        lo, hi = x - t - 1e-12, x + t + 1e-12
    else:
        lo, hi = 2*np.pi - np.arccos(-1.0/t), x + t + 1e-12
    for _ in range(200):
        mid = 0.5*(lo+hi)
        if mid + t*np.sin(mid) < x: lo = mid
        else: hi = mid
    return 0.5*(lo+hi)
def err_L1(nu, t):
    r = np.concatenate([np.geomspace(1e-3*nu, 1.0, 3000)[:-1], np.linspace(1.0, np.pi, 600)])
    xs = np.pi + r
    h = 0.4*np.sqrt(nu)
    W = 2.6
    yy = np.arange(-W, W + h/2, h)
    vals = np.empty_like(xs)
    for i, x in enumerate(xs):
        a = amin(x, t)
        y = a + yy
        Phi = 1 - np.cos(y) + (x - y)**2/(2*t)
        w = np.exp(-(Phi - Phi.min())/(2*nu))
        mean_shift = np.sum(w*yy)/np.sum(w)      # <y> - a
        vals[i] = abs(mean_shift)/t               # |u - v|
    # |u-v| pari attorno a pi e a 0: integrale su un periodo = 2 * integrale su (pi, 2pi)
    return 2*np.trapezoid(vals, xs)
log("(2) Gamma(sin) a t*=1: (e - nu|log nu|)/nu, atteso 2.57497 (+O(sqrt nu))")
for nu in (1e-4, 1e-5, 1e-6):
    e = err_L1(nu, 1.0)
    log(f"    nu={nu:.0e}: {(e - nu*abs(np.log(nu)))/nu:.5f}   [t={time.time()-T0:.0f}s]")
log("(3) D = e/nu - 2 log(1/max(|t-1|, sqrt nu))  (T1/T2: deve restare O(1) e uniforme)")
for nu in (1e-4, 1e-5, 1e-6):
    row = []
    for lab, s in (("-16", -16*np.sqrt(nu)), ("-4", -4*np.sqrt(nu)), ("-1", -np.sqrt(nu)),
                   ("+1", np.sqrt(nu)), ("+4", 4*np.sqrt(nu)), ("+16", 16*np.sqrt(nu)),
                   ("+nu^1/3", nu**(1/3)), ("+0.05", 0.05), ("-0.05", -0.05)):
        e = err_L1(nu, 1.0 + s)
        D = e/nu - 2*np.log(1/max(abs(s), np.sqrt(nu)))
        row.append(f"{lab}:{D:.3f}")
    log(f"    nu={nu:.0e}: " + "  ".join(row) + f"   [t={time.time()-T0:.0f}s]")

# ---------------- (4) T5 con c=0.7, D=0.3, L=1
c, Dd, L = 0.7, 0.3, 1.0
th = c/(2*Dd)
G1 = lambda z: np.exp(-z*z/4)/np.sqrt(4*np.pi)
def Ntil(k):
    g = lambda w: integrate.quad(lambda v: G1(w+v)*v**k, 0, np.inf, epsabs=1e-14)[0]
    return np.sqrt(integrate.quad(lambda w: (w*g(w))**2, 0, np.inf, epsabs=1e-16, limit=200)[0])
Nt = {k: Ntil(k) for k in (1, 2)}
log("(4) Ntilde_k:", {k: round(v, 6) for k, v in Nt.items()}, " (package: 0.234005, 0.325244)")
NG = 8000
gx, gw = np.polynomial.legendre.leggauss(NG)
X = 0.5*(gx+1)*L; WX = 0.5*L*gw
NM = 1400
n = np.arange(1, NM+1); mu = n*np.pi/L
def coef_on(f_vals, xs, ws):
    return (np.sqrt(2/L)*np.sin(np.outer(mu, xs))) @ (ws*f_vals)
EvX = np.sqrt(2/L)*np.sin(np.outer(mu, X))
def heat_eval(co, t):
    return (np.exp(-Dd*mu**2*t)*co) @ EvX
data = {1: (lambda y: y*(1-y), 1.0, -1.0), 2: (lambda y: y*y*(1-y)**2, 2.0, 2.0)}
import math
for k, (u0, dk0, dkL) in data.items():
    pred = c*Nt[k]/math.factorial(k)*Dd**(k/2-0.25)*np.sqrt(dk0**2+dkL**2)
    cS = coef_on(np.exp(-th*X)*u0(X), X, WX)
    R = []
    for t in (4e-4, 1e-4, 2.5e-5):
        Su = np.exp(th*X - c*c*t/(4*Dd))*heat_eval(cS, t)
        a = c*t
        gy, gwy = np.polynomial.legendre.leggauss(NG)
        Y = a + 0.5*(gy+1)*(L-a); WY = 0.5*(L-a)*gwy
        cT = coef_on(u0(Y - a), Y, WY)
        E = Su - heat_eval(cT, t)
        nrm = np.sqrt(np.sum(WX*E*E))
        R.append(nrm/t**(k/2+0.75))
    rich = 2*R[2] - R[1]
    log(f"    k={k}: ||E||/t^p = {R[0]:.6f}, {R[1]:.6f}, {R[2]:.6f} (t=4e-4,1e-4,2.5e-5); Richardson(sqrt t) {rich:.6f}; predetto {pred:.6f}  [t={time.time()-T0:.0f}s]")
log("fine")
