# OP-F5A â€” controlli numerici (NON prove), seconda tornata.
# (T) punto triplo: integrale di strato chiuso 2 log((sum p)^2/(p1 p3)) vs quadratura del profilo;
#     quadratura di Hopf raffinata (r piu' piccolo, griglia y piu' fine) per capire lo scarto 6.0472 vs 6.0612.
import numpy as np
import sympy as sp

ys = sp.symbols('y')
Ws = (ys+1)**2*ys**2*(ys-sp.Rational(3, 2))**2*(1+sp.Rational(3, 10)*ys**2)
W = sp.lambdify(ys, Ws, 'numpy'); W1 = sp.lambdify(ys, sp.diff(Ws, ys), 'numpy')
W2 = sp.lambdify(ys, sp.diff(Ws, ys, 2), 'numpy'); W3 = sp.lambdify(ys, sp.diff(Ws, ys, 3), 'numpy')
A = np.array([-1.0, 0.0, 1.5])
p = np.array([W2(a)**-0.5 for a in A])
const3 = 2*np.log(p.sum()**2/(p[0]*p[2]))
# (T1) profilo: 2 * int ds |a(s) - sum p_j a_j e^{s a_j}/sum p_j e^{s a_j}|  (x = 2 nu s)
s = np.linspace(-60, 60, 2000001)
E = np.exp(np.outer(s, A) - (np.outer(s, A)).max(axis=1, keepdims=True))*p
mean = (E*A).sum(1)/E.sum(1)
a_s = np.where(s < 0, A[0], A[2])
prof = 2*np.trapezoid(np.abs(a_s - mean), s)
print(f"(T1) profilo integrato = {prof:.6f}   formula = {const3:.6f}")

# (T2) Hopf raffinato
def branch(x, a0):
    a = a0
    for _ in range(80):
        a -= (W1(a) - x)/W2(a)
    return a
def inviscid_min(x):
    c = [branch(x, a0) for a0 in A]
    v = [W(a) - x*a for a in c]
    return c[int(np.argmin(v))]
def run(nu, r, ny):
    y = np.linspace(-2.2, 2.7, ny)
    Wy = W(y)
    def shift(x):
        Phi = Wy - x*y
        w = np.exp(-(Phi - Phi.min())/(2*nu))
        return np.sum(w*y)/np.sum(w)
    xs = np.concatenate([np.linspace(-r, -40*nu, 500), np.linspace(-40*nu, 40*nu, 1200), np.linspace(40*nu, r, 500)])
    av = np.array([inviscid_min(x) for x in xs])
    uv = np.array([av[i] - shift(x) for i, x in enumerate(xs)])
    kap = np.array([W3(a)/W2(a)**2 for a in av])
    e = np.trapezoid(np.abs(uv), xs)
    sm = np.trapezoid(np.abs(kap), xs)
    # resto liscio con segno: confronta uv con nu*kap fuori dallo strato
    out = np.abs(xs) > 40*nu
    rel = np.max(np.abs(uv[out] - nu*kap[out]))/nu
    return (e - nu*sm)/nu, rel
for nu, r, ny in ((1e-4, 0.05, 400001), (2.5e-5, 0.05, 800001)):
    L, rel = run(nu, r, ny)
    print(f"(T2) nu={nu:.1e} r={r} ny={ny}: (e - nu int|kappa|)/nu = {L:.5f}  (formula {const3:.5f});  max|uv-nu kap|/nu fuori strato = {rel:.3e}")
