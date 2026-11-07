# OP-F5A — P1-Q5 dati compatibili: controllo numerico (NON prova) di OPF5A-L5/T5.
# AD Dirichlet su (0,L): A = D d2 - c d. E^mult(t)u0 = S(t)u0 - S^D(t) S_2(t) u0, S_2 = trasporto con inflow in 0.
# (1) costanti: Ntil_k = || w g_k(w) ||_{L2(0,inf)}, g_k(w) = int_0^inf G_1(w+v) v^k dv  vs  k*N_{k-1} (OP-ANA)
# (2) E^mult esatto (serie modale della coniugazione) vs formula chiusa B_0 + B_L
# (3) ||E^mult|| / t^{k/2+3/4} -> c Ntil_k D^{k/2-1/4} sqrt(l0^2+lL^2)
import numpy as np
from scipy.integrate import quad

G1 = lambda z: np.exp(-z*z/4)/np.sqrt(4*np.pi)
def g(k, w):
    return quad(lambda v: G1(w+v)*v**k, 0, np.inf, limit=200)[0]
def Ntil(k):
    return np.sqrt(quad(lambda w: (w*g(k, w))**2, 0, np.inf, limit=200)[0])
N_OPA = {0: 0.234005, 1: 0.162622, 2: 0.203448}
ok = 0; tot = 0
print("(1) costanti")
for k in (1, 2, 3):
    a, b = Ntil(k), k*N_OPA[k-1]
    tot += 1; ok += abs(a-b) < 2e-5
    print(f"  k={k}: Ntil_k={a:.6f}  k*N_(k-1)={b:.6f}  {'OK' if abs(a-b)<2e-5 else 'FAIL'}")

L, D, c = 1.0, 1.0, 1.0
th = c/(2*D)
NX = 4001
x = np.linspace(0, L, NX); dx = x[1]-x[0]
wq = np.full(NX, dx); wq[0] = wq[-1] = dx/2
def l2(f): return np.sqrt(np.sum(wq*f*f))
NM = 1500
n = np.arange(1, NM+1); mu = n*np.pi/L
E = np.sqrt(2/L)*np.sin(np.outer(mu, x))            # NM x NX
def heatD(f, t):                                    # Dirichlet heat, modal
    co = E @ (wq*f)
    return (np.exp(-D*mu**2*t)*co) @ E
def S_full(f, t):                                   # exact: conjugation
    return np.exp(th*x - c*c*t/(4*D))*heatD(np.exp(-th*x)*f, t)
def S2(f_fun, t):
    return np.where(x > c*t, f_fun(np.clip(x - c*t, 0, L)), 0.0)
def Gt(z, t): return np.exp(-z*z/(4*D*t))/np.sqrt(4*np.pi*D*t)
def closed(f_fun, t):
    # B_0 + B_L (immagini principali j=0,1; le altre sono esponenzialmente piccole)
    yy = np.linspace(0, L, 6001); wy = np.full(6001, yy[1]-yy[0]); wy[0] = wy[-1] = wy[0]/2
    fy = f_fun(yy)
    I0 = np.array([np.sum(wy*Gt(xx+yy, t)*np.exp(-th*yy)*fy) for xx in x])
    IL = np.array([np.sum(wy*Gt(2*L-xx-yy, t)*np.exp(th*(L-yy))*fy) for xx in x])
    pre = 2*np.exp(-c*c*t/(4*D))
    return -pre*np.sinh(th*x)*I0 + pre*np.sinh(th*(L-x))*IL
def first_order(f_fun, t):
    yy = np.linspace(0, L, 6001); wy = np.full(6001, yy[1]-yy[0]); wy[0] = wy[-1] = wy[0]/2
    fy = f_fun(yy)
    I0 = np.array([np.sum(wy*Gt(xx+yy, t)*fy) for xx in x])
    IL = np.array([np.sum(wy*Gt(2*L-xx-yy, t)*fy) for xx in x])
    return -(c/D)*(x*I0 - (L-x)*IL)

cases = [("sin(pi x)  k=1", lambda y: np.sin(np.pi*y), 1, np.pi, np.pi),
         ("x^2(1-x)^2 k=2", lambda y: y**2*(1-y)**2, 2, 1.0, 1.0),
         ("x^3(1-x)^3 k=3", lambda y: y**3*(1-y)**3, 3, 1.0, 1.0),
         ("x^2(1-x)^3 k=(2,3)", lambda y: y**2*(1-y)**3, 2, 1.0, 0.0)]
print("(2)-(3) E^mult a eps=1 (c=D=L=1)")
for name, f, k, l0, lL in cases:
    pred = abs(c)*Ntil(k)*D**(k/2-0.25)*np.hypot(l0, lL)
    print(f"  {name}: predetto ||E||/t^(k/2+3/4) -> {pred:.6f}")
    for t in (1e-2, 3e-3, 1e-3, 3e-4):
        Em = S_full(f(x), t) - heatD(S2(f, t), t)
        Ec = closed(f, t)
        E1 = first_order(f, t)
        rel = l2(Em-Ec)/l2(Em)
        r = l2(Em)/t**(k/2+0.75)
        r2 = l2(Em-E1)/t**(k/2+1.25)
        print(f"    t={t:.0e}: ||E||/t^p={r:.5f}  |E_modale-E_chiusa|/|E|={rel:.1e}  ||E-E1||/t^(p+1/2)={r2:.4f}")
        tot += 1; ok += rel < 2e-3
print(f"esito: {ok}/{tot} OK")
