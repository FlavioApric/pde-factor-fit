"""T6 dispersivo (C2.10, C2.30, C2.46) e T7 reazione (C2.11, C2.42)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sympy as sp
from _common import check, check_true, summary, quotient_dim

x = sp.symbols('x', real=True)
t, D, r, cs, v = sp.symbols('t D r c_s v', positive=True)
xi, tau, kap = sp.symbols('xi tau kappa')
g = sp.Function('g')

Ai = lambda u: sp.diff(u, t) + sp.diff(u, x, 3)
# C2.10 Airy
check("C2.10 e^{xi x - xi^3 t}", Ai(sp.exp(xi*x - xi**3*t)))
Kair = (3*t)**sp.Rational(-1, 3)*sp.airyai(x/(3*t)**sp.Rational(1, 3))
check("C2.10 soluzione fondamentale (3t)^{-1/3} Ai(x/(3t)^{1/3})", Ai(Kair))
for n in range(6):
    p = sp.expand(sp.diff(sp.exp(xi*x - xi**3*t), xi, n).subs(xi, 0))
    check(f"C2.10 polinomio di Airy p_{n}", Ai(p))
# relazione di dispersione: e^{i(kx - w t)}: w = -k^3, velocita' di gruppo -3k^2
w = sp.solve(sp.Eq(-sp.I*sp.Symbol('w') + (sp.I*kap)**3, 0), sp.Symbol('w'))[0]
check("C2.10 omega(k) = -k^3", w + kap**3)

# C2.30 Schroedinger libero i u_t + u_xx = 0
Sc = lambda u: sp.I*sp.diff(u, t) + sp.diff(u, x, 2)
check("C2.30 propagatore (4 pi i t)^{-1/2} e^{i x^2/4t}", Sc(sp.exp(sp.I*x**2/(4*t))/sp.sqrt(4*sp.pi*sp.I*t)))
check("C2.30 modi e^{i k x - i k^2 t}", Sc(sp.exp(sp.I*kap*x - sp.I*kap**2*t)))
for n in range(5):
    p = sp.expand(sp.diff(sp.exp(xi*x + sp.I*xi**2*t), xi, n).subs(xi, 0))
    check(f"C2.30 polinomio 'di Schroedinger' q_{n} (calore a tempo immaginario)", Sc(p))
# Galileo: u -> e^{i(v x/2 - v^2 t/4)} u(x - v t, t)
# Galileo: u -> e^{i(v x/2 - v^2 t/4)} u(x - v t, t), testato su propagatore e su q_3 (soluzioni concrete)
K = lambda X, T_: sp.exp(sp.I*X**2/(4*T_))/sp.sqrt(4*sp.pi*sp.I*T_)
q3 = lambda X, T_: X**3 + 6*sp.I*T_*X
for nm, U in (("propagatore", K), ("q_3", q3)):
    ug = sp.exp(sp.I*(v*x/2 - v**2*t/4))*U(x - v*t, t)
    check(f"C2.30 invarianza di Galileo su {nm}", Sc(ug))

# C2.46 KdV soliton (controllo del termine non lineare; parte lineare = Airy)
u = cs/2*sp.sech(sp.sqrt(cs)/2*(x - cs*t))**2
check("C2.46 solitone KdV u_t+6uu_x+u_xxx=0", sp.diff(u, t) + 6*u*sp.diff(u, x) + sp.diff(u, x, 3))

# dimensioni delle intersezioni tra classi dispersive/diffusive
check_true("T6 dim (tau+xi^3, tau-D xi^2) = 3 (Bezout 1*3)", quotient_dim([tau + xi**3, tau - D*xi**2], [tau, xi]) == 3)
check_true("T6 dim (tau+xi^3, tau-i xi^2) = 3", quotient_dim([tau + xi**3, tau - sp.I*xi**2], [tau, xi]) == 3)

# T7 C2.11 reazione
check("C2.11 e^{rt} g(x) in ker(d_t - r)", sp.diff(sp.exp(r*t)*g(x), t) - r*sp.exp(r*t)*g(x))
check_true("C2.11 ker(d_t - r) non e' finito-dimensionale in x: (tau - r) non dipende da xi, quoziente infinito",
           quotient_dim([tau - r], [tau, xi]) is None)
RD = lambda u: sp.diff(u, t) - D*sp.diff(u, x, 2) - r*u
G = sp.exp(-x**2/(4*D*t))/sp.sqrt(4*sp.pi*D*t)
check("C2.11 reazione-diffusione: e^{rt} G (prodotto dei semigruppi commutanti)", RD(sp.exp(r*t)*G))
k = sp.symbols('k', real=True)
check("C2.11 modi e^{ikx + (r - D k^2) t}", RD(sp.exp(sp.I*k*x + (r - D*k**2)*t)))
# fronte lineare Fisher-KPP: e^{xi(x - s t)} sse D xi^2 + s xi + r = 0; xi reale sse s^2 >= 4 r D
s = sp.symbols('s', positive=True)
expr = sp.simplify(RD(sp.exp(xi*(x - s*t)))/sp.exp(xi*(x - s*t)))
check("C2.11 onda viaggiante: residuo = -(D xi^2 + s xi + r)", expr + D*xi**2 + s*xi + r)
disc = sp.discriminant(D*xi**2 + s*xi + r, xi)
check("C2.11 discriminante s^2 - 4 r D (velocita' minima 2 sqrt(rD))", disc - (s**2 - 4*r*D))
# Fisher-KPP esatto (Ablowitz-Zeppetella 1979): u_t = u_xx + u(1-u), u = (1+e^{(x - 5t/sqrt6)/sqrt6})^{-2}
uz = (1 + sp.exp((x - 5*t/sp.sqrt(6))/sp.sqrt(6)))**-2
check("C2.11/C2.42 Ablowitz-Zeppetella (Fisher-KPP)", sp.diff(uz, t) - sp.diff(uz, x, 2) - uz*(1 - uz))
# C2.42 Turing: J = [[1,-1],[3,-2]], Dm = diag(1,d): h(k^2) = det(J - k^2 Dm)
q, d = sp.symbols('q d', positive=True)
J = sp.Matrix([[1, -1], [3, -2]])
h = sp.expand((J - q*sp.diag(1, d)).det())
check("C2.42 h(q) = d q^2 - (d-2) q + 1", h - (d*q**2 - (d - 2)*q + 1))
check_true("C2.42 traccia J<0, det J>0 (stabile senza diffusione)", J.trace() < 0 and J.det() > 0)
check_true("C2.42 d=10, q=2/5: h<0 -> instabilita' di Turing", h.subs({d: 10, q: sp.Rational(2, 5)}) < 0, str(h.subs({d: 10, q: sp.Rational(2, 5)})))
summary("t6_t7")
