# OP-F5A — punto triplo (OPF5A-T3): controllo numerico (NON prova).
# Modello locale di Hopf: Phi_x(y) = W(y) - (x - x0) y / t0, t0 = 1, x0 = 0, con
# W = (y+1)^2 y^2 (y-1.5)^2 (1+0.3 y^2): tre minimizzanti a = -1, 0, 1.5 in x = 0 (punto triplo).
# Predizione: int_{|x|<r} |u-v| dx = nu * int |kappa(a(x))| dx + 2 nu log((p1+p2+p3)^2/(p1 p3)) + o(nu),
# p_i = W''(a_i)^{-1/2}, kappa = W'''/W''^2 (t0 = 1).  Il ramo centrale aumenta la costante.
import numpy as np
import sympy as sp

ys = sp.symbols('y')
Ws = (ys+1)**2*ys**2*(ys-sp.Rational(3, 2))**2*(1+sp.Rational(3, 10)*ys**2)
W = sp.lambdify(ys, Ws, 'numpy'); W1 = sp.lambdify(ys, sp.diff(Ws, ys), 'numpy')
W2 = sp.lambdify(ys, sp.diff(Ws, ys, 2), 'numpy'); W3 = sp.lambdify(ys, sp.diff(Ws, ys, 3), 'numpy')
A = [-1.0, 0.0, 1.5]
p = np.array([W2(a)**-0.5 for a in A])
const3 = 2*np.log(p.sum()**2/(p[0]*p[2]))
const2 = 2*np.log((p[0]+p[2])**2/(p[0]*p[2]))
print(f"W''(a_i) = {[float(W2(a)) for a in A]}")
print(f"costante predetta (3 minimizzanti) = {const3:.6f};  senza il ramo centrale = {const2:.6f}")

def branch(x, a0):
    a = a0
    for _ in range(60):
        a -= (W1(a) - x)/W2(a)
    return a

def inviscid_min(x):
    cands = [branch(x, a0) for a0 in A]
    vals = [W(a) - x*a for a in cands]
    return cands[int(np.argmin(vals))]

y = np.linspace(-2.2, 2.7, 400001)
def shift(x, nu):
    Phi = W(y) - x*y
    w = np.exp(-(Phi - Phi.min())/(2*nu))
    return np.sum(w*y)/np.sum(w)

r = 0.2
for nu in (4e-4, 1e-4, 2.5e-5):
    xs = np.concatenate([np.linspace(-r, -40*nu, 800), np.linspace(-40*nu, 40*nu, 1601)[1:-1], np.linspace(40*nu, r, 800)])
    av = np.array([inviscid_min(x) for x in xs])
    uv = np.array([av[i] - shift(x, nu) for i, x in enumerate(xs)])
    smooth = np.array([abs(W3(a))/W2(a)**2 for a in av])
    e = np.trapezoid(np.abs(uv), xs)
    layer = (e - nu*np.trapezoid(smooth, xs))/nu
    print(f"nu={nu:.1e}: (e - nu*int|kappa|)/nu = {layer:.5f}   predetto {const3:.5f}")
