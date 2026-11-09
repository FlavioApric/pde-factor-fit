# OP-F5A — controlli numerici (NON prove), terza tornata.
# (P) P1-Q5: E^mult = B_0 + B_L + R_L + (immagini, esponenzialmente piccole), con
#     R_L(xi) = -int_0^{ct} [G(xi - r) - G(xi + r)] u0(L - ct + r) dr,  xi = L - x   (OPF5A-L5)
# (Q) costante di Pearcey P = lim_B (2 int_{|b|<B} b^2 |m(b)| db - 4 log B), m(b) = media di z per e^{-Q(b,z)},
#     Q = z^4/12 + b z^3/3 + b^2 z^2/2;  predizione per u0 = sin x a t* = 1:  Gamma = 4 log 2 + log(1/4) + P ~ 2.575
import numpy as np

# ---------------- (P)
L, D, c = 1.0, 1.0, 1.0
th = c/(2*D)
NX = 4001
x = np.linspace(0, L, NX); dx = x[1]-x[0]
wq = np.full(NX, dx); wq[0] = wq[-1] = dx/2
def l2(f): return np.sqrt(np.sum(wq*f*f))
NM = 1500
n = np.arange(1, NM+1); mu = n*np.pi/L
Em = np.sqrt(2/L)*np.sin(np.outer(mu, x))
def heatD(f, t):
    co = Em @ (wq*f)
    return (np.exp(-D*mu**2*t)*co) @ Em
def S_full(f, t): return np.exp(th*x - c*c*t/(4*D))*heatD(np.exp(-th*x)*f, t)
def S2(ff, t): return np.where(x > c*t, ff(np.clip(x - c*t, 0, L)), 0.0)
def Gt(z, t): return np.exp(-z*z/(4*D*t))/np.sqrt(4*np.pi*D*t)
def quadgrid(a, b, m=6001):
    yy = np.linspace(a, b, m); wy = np.full(m, yy[1]-yy[0]); wy[0] = wy[-1] = wy[0]/2
    return yy, wy
def closed_exact(ff, t):
    yy, wy = quadgrid(0, L); fy = ff(yy)
    I0 = np.array([np.sum(wy*Gt(xx+yy, t)*np.exp(-th*yy)*fy) for xx in x])
    IL = np.array([np.sum(wy*Gt(2*L-xx-yy, t)*np.exp(th*(L-yy))*fy) for xx in x])
    pre = 2*np.exp(-c*c*t/(4*D))
    B = -pre*np.sinh(th*x)*I0 + pre*np.sinh(th*(L-x))*IL
    rr, wr = quadgrid(0, c*t, 2001); fr = ff(L - c*t + rr)
    xi = L - x
    RL = -np.array([np.sum(wr*(Gt(z - rr, t) - Gt(z + rr, t))*fr) for z in xi])
    return B, RL
cases = [("sin(pi x)", lambda y: np.sin(np.pi*y)), ("x^2(1-x)^2", lambda y: y**2*(1-y)**2),
         ("x^3(1-x)^3", lambda y: y**3*(1-y)**3), ("x^2(1-x)^3", lambda y: y**2*(1-y)**3)]
print("(P) |E_modale - (B0+BL)|/|E|  e  |E_modale - (B0+BL+RL)|/|E|")
for name, ff in cases:
    for t in (1e-2, 1e-3):
        Ex = S_full(ff(x), t) - heatD(S2(ff, t), t)
        B, RL = closed_exact(ff, t)
        print(f"  {name:12s} t={t:.0e}: senza R_L {l2(Ex-B)/l2(Ex):.2e}   con R_L {l2(Ex-B-RL)/l2(Ex):.2e}   |R_L|/|E| {l2(RL)/l2(Ex):.2e}")

# ---------------- (Q)
z = np.linspace(-40, 40, 160001)
def m(b):
    Q = z**4/12 + b*z**3/3 + b*b*z*z/2
    w = np.exp(-(Q - Q.min()))
    return np.sum(w*z)/np.sum(w)
for B in (20.0, 40.0, 80.0):
    bs = np.concatenate([-np.geomspace(B, 1e-4, 4000), [0.0], np.geomspace(1e-4, B, 4000)])
    vals = np.array([b*b*abs(m(b)) for b in bs])
    P = 2*np.trapezoid(vals, bs) - 4*np.log(B)
    # correzione di coda: integrando ~ 2/|b| (1 + O(1/b^2))
    print(f"(Q) B={B}: P_B = {P:.5f}   Gamma(sin) = 4log2 + log(1/4) + P_B = {4*np.log(2)+np.log(0.25)+P:.5f}  (numerica Cole-Hopf: 2.5757 a nu=1e-5, in discesa)")
