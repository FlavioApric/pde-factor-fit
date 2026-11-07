# OP-ANA Q1 (S4T-Q1): controllo numerico (NON prova) del Teorema OPA-T1
#   ||u - v||_{L1}/nu -> Lambda_uv,   ||E^add||_{L1}/nu -> Lambda_add
# Burgers su T, t > t*. u da Cole-Hopf (quadratura con esponenti normalizzati),
# v = (x - a(x))/t da Lax-Oleinik, h = S_A(t)u0 (calore, esatto).
import numpy as np
from scipy.optimize import brentq

def grid(nu, shocks, nx=3000, half=0.06):
    edges = [0.0]
    for s0 in sorted(shocks):
        edges += [s0 - half, s0 + half]
    edges.append(2*np.pi)
    X, Wt = [], []
    for i in range(len(edges) - 1):
        lo, hi = edges[i], edges[i+1]
        fine = (i % 2 == 1)
        n = int((hi - lo)/(nu/40)) if fine else max(int(nx*(hi - lo)/(2*np.pi)), 10)
        h = (hi - lo)/n
        X.append(lo + h*(np.arange(n) + 0.5)); Wt.append(np.full(n, h))
    return np.concatenate(X), np.concatenate(Wt)

def evaluate(D, t, nu, xs, ny=40001):
    u0, U0, u0p = D["u0"], D["U0"], D["u0p"]
    R = 3.0*t + 1.0
    U, V, A = np.empty(len(xs)), np.empty(len(xs)), np.empty(len(xs))
    for i, x in enumerate(xs):
        y = np.linspace(x - R, x + R, ny)
        Phi = U0(y) + (x - y)**2/(2*t)
        a = y[np.argmin(Phi)]
        for _ in range(40):
            a -= (u0(a) - (x - a)/t)/(u0p(a) + 1/t)
        W = np.exp(-(Phi - Phi.min())/(2*nu))
        Ey = np.sum(y*W)/np.sum(W)
        U[i], V[i], A[i] = (x - Ey)/t, (x - a)/t, a
    return U, V, A

def predicted(D, t):
    X = np.linspace(0, 2*np.pi, 20000, endpoint=False) + np.pi/20000
    _, _, A = evaluate(D, t, 1e-3, X, ny=4001)
    J = 1 + t*D["u0p"](A)
    s_uv = np.mean(t*np.abs(D["u0pp"](A))/J**2)*2*np.pi
    s_add = np.mean(np.abs(t*D["u0pp"](A)/J**2 - t*D["u0pp"](X)))*2*np.pi
    sh = sum(4*np.log(2*np.cosh(r/2)) for r in D["rho"](t))
    return s_uv, s_add, sh

def run(D, t, nus):
    print("==", D["name"], " t =", t, flush=True)
    s_uv, s_add, sh = predicted(D, t)
    print(f"PREDICTED Lambda_uv  = {s_uv:.4f} (liscio) + {sh:.4f} (shock) = {s_uv+sh:.4f}")
    print(f"PREDICTED Lambda_add = {s_add:.4f} (liscio) + {sh:.4f} (shock) = {s_add+sh:.4f}", flush=True)
    for nu in nus:
        X, Wt = grid(nu, D["shocks"](t))
        U, V, A = evaluate(D, t, nu, X)
        H = D["heat"](X, t, nu)
        Eadd = (U - V) - (H - D["u0"](X))
        print(f"nu={nu:.1e}  ||u-v||_1/nu = {np.sum(np.abs(U-V)*Wt)/nu:.4f}   ||E^add||_1/nu = {np.sum(np.abs(Eadd)*Wt)/nu:.4f}", flush=True)

SIN = dict(name="u0 = sin x", u0=np.sin, U0=lambda y: 1 - np.cos(y), u0p=np.cos,
           u0pp=lambda y: -np.sin(y), heat=lambda x, t, nu: np.exp(-nu*t)*np.sin(x),
           shocks=lambda t: [np.pi], rho=lambda t: [0.0])

# dato asimmetrico: u0 = sin x + 0.3 cos 2x (un solo shock a t=1.5; rho != 0)
def U0b(y): return (1 - np.cos(y)) + 0.15*np.sin(2*y)
def make_asym():
    u0 = lambda y: np.sin(y) + 0.3*np.cos(2*y)
    u0p = lambda y: np.cos(y) - 0.6*np.sin(2*y)
    u0pp = lambda y: -np.sin(y) - 1.2*np.cos(2*y)
    heat = lambda x, t, nu: np.exp(-nu*t)*np.sin(x) + 0.3*np.exp(-4*nu*t)*np.cos(2*x)
    def locate(t):
        # shock: x where two global minimizers coexist; bisection on Delta(x) = Phi(a+) - Phi(a-)
        def minimizers(x):
            y = np.linspace(x - 3*t - 1, x + 3*t + 1, 200001)
            Phi = U0b(y) + (x - y)**2/(2*t)
            return y, Phi
        xs = np.linspace(0, 2*np.pi, 4001)
        a = []
        for x in xs:
            y, Phi = minimizers(x); a.append(y[np.argmin(Phi)] - x)
        a = np.array(a); j = np.argmax(np.diff(a))  # largest jump of minimizer
        return xs[j], xs[j+1]
    D = dict(name="u0 = sin x + 0.3 cos 2x", u0=u0, U0=U0b, u0p=u0p, u0pp=u0pp, heat=heat)
    cache = {}
    def shock_data(t):
        if t in cache: return cache[t]
        lo, hi = locate(t)
        def branches(x):
            y = np.linspace(x - 3*t - 1, x + 3*t + 1, 400001)
            Phi = U0b(y) + (x - y)**2/(2*t)
            # local minima
            idx = np.where((Phi[1:-1] < Phi[:-2]) & (Phi[1:-1] <= Phi[2:]))[0] + 1
            idx = idx[np.argsort(Phi[idx])][:2]
            return sorted(y[idx]), Phi[idx]
        f = lambda x: (lambda b: (U0b(b[1]) + (x-b[1])**2/(2*t)) - (U0b(b[0]) + (x-b[0])**2/(2*t)))(branches(x)[0])
        xs0 = brentq(f, lo, hi, xtol=1e-12)
        am, ap = branches(xs0)[0]
        for _ in range(40):
            am -= (u0(am) - (xs0 - am)/t)/(u0p(am) + 1/t)
            ap -= (u0(ap) - (xs0 - ap)/t)/(u0p(ap) + 1/t)
        Jm, Jp = 1 + t*u0p(am), 1 + t*u0p(ap)
        cache[t] = (xs0 % (2*np.pi), 0.5*np.log(Jm/Jp), Jm, Jp)
        return cache[t]
    D["shocks"] = lambda t: [shock_data(t)[0]]
    D["rho"] = lambda t: [shock_data(t)[1]]
    D["info"] = shock_data
    return D

if __name__ == "__main__":
    t = 2.0
    run(SIN, t, [4e-3, 2e-3, 1e-3, 5e-4])
    b = brentq(lambda b: b - 2*np.sin(b), 1.0, 3.0)
    print(f"forma chiusa (sin, t=2): parte liscia di Lambda_uv = 2[log3 - log(1-2cos b)] = {2*(np.log(3)-np.log(1-2*np.cos(b))):.4f}, D = b = {b:.5f}")
    AS = make_asym()
    t2 = 1.5
    xs0, rho, Jm, Jp = AS["info"](t2)
    print(f"[asimmetrico] t={t2}: shock x_s={xs0:.6f}, J-={Jm:.4f}, J+={Jp:.4f}, rho={rho:.4f}, costante di shock 4log(2cosh(rho/2))={4*np.log(2*np.cosh(rho/2)):.4f} (vs 4ln2={4*np.log(2):.4f})")
    run(AS, t2, [2e-3, 1e-3, 5e-4])
