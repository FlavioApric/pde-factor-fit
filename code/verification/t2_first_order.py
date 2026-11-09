"""T2 — PDE del primo ordine (C2.6 trasporto, C2.18 Lagrange, C2.25 HJ/iconale)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sympy as sp
from _common import check, check_true, summary

t, x, s = sp.symbols('t x s', real=True)
c, r, a, b, k = sp.symbols('c r a b k', nonzero=True)
xi = sp.symbols('xi')
g, Phi, cf, rf = sp.Function('g'), sp.Function('Phi'), sp.Function('c'), sp.Function('r')

T = lambda u: sp.diff(u, t) + c*sp.diff(u, x)

# C2.6 trasporto: ker = {g(x-ct)}; esponenziali e polinomi
check("C2.6 T g(x-ct)=0", T(g(x - c*t)))
check("C2.6 T e^{xi(x-ct)}=0", T(sp.exp(xi*(x - c*t))))
for n in range(5):
    check(f"C2.6 T (x-ct)^{n}=0 (= d^n/dxi^n e^(xi(x-ct)) a xi=0)", T((x - c*t)**n))
# simbolo P = tau + c xi; V(P) = {tau = -c xi}
tau = sp.symbols('tau')
check("C2.6 simbolo: T e^{tau t+xi x} = (tau+c xi) e", T(sp.exp(tau*t + xi*x)) - (tau + c*xi)*sp.exp(tau*t + xi*x))

# velocita' variabile: d_t + c(x) d_x, u = g(Phi(x) - t), Phi' = 1/c
u = g(Phi(x) - t)
expr = sp.diff(u, t) + cf(x)*sp.diff(u, x)
expr = expr.subs(sp.Derivative(Phi(x), x), 1/cf(x))
check("C2.6 velocita' variabile: u=g(Phi(x)-t), Phi'=1/c", expr)

# trasporto + reazione costante (termini commutanti): u = e^{-rt} g(x-ct)  [prodotto]
u = sp.exp(-r*t)*g(x - c*t)
check("C2.6 trasporto+reazione: e^{-rt}g(x-ct)", T(u) + r*u)
# split moltiplicativo esatto: S_tr(t) S_re(t) u0 = soluzione (operatori commutano)

# trasporto + reazione VARIABILE r(x): termini NON commutanti
# A = -c d_x, B = -r(x): [A,B] f = c r'(x) f
f = sp.Function('f')
A = lambda w: -c*sp.diff(w, x)
B = lambda w: -rf(x)*w
check("C2.6 commutatore [A,B] = c r'(x)", A(B(f(x))) - B(A(f(x))) - c*sp.diff(rf(x), x)*f(x))
# soluzione esatta (Dyson = media di r lungo la caratteristica), r concreto polinomiale
rr = lambda z: z**3 + 2*z
u0 = sp.Function('u0')
Eexact = -sp.integrate(rr(x - c*s), (s, 0, t))
uex = sp.exp(Eexact)*u0(x - c*t)
check("C2.6 r(x)=x^3+2x: u=exp(-int_0^t r(x-cs)ds) u0(x-ct) risolve u_t+cu_x+r u=0",
      sp.diff(uex, t) + c*sp.diff(uex, x) + rr(x)*uex)
# split di Lie: e^{tA}e^{tB}u0 = e^{-t r(x-ct)} u0(x-ct); Zassenhaus II ordine: e^{tA}e^{tB}e^{-t^2/2 [A,B]}
Esplit1 = -t*rr(x - c*t)
Esplit2 = -t*rr(x - c*t) - t**2/2*c*sp.diff(rr(x), x).subs(x, x - c*t)
d1 = sp.series(Eexact - Esplit1, t, 0, 3).removeO()
d2 = sp.series(Eexact - Esplit2, t, 0, 3).removeO()
check_true("C2.6 Lie split: errore O(t^2) non nullo", sp.simplify(d1) != 0, f"(Eexact-Esplit1 fino a t^2 = {sp.factor(d1)})")
check("C2.6 Zassenhaus con -t^2/2[A,B]: errore O(t^3)", d2)

# C2.18 Lagrange lineare a u_x + b u_t = k u (coeff. costanti)
u = sp.exp(k*t/b)*g(a*t - b*x)
check("C2.18 Lagrange: e^{kt/b} g(at-bx)", a*sp.diff(u, x) + b*sp.diff(u, t) - k*u)
# Lagrange a coefficienti variabili: x u_x + t u_t = 0 -> g(x/t) (omogenee di grado 0)
u = g(x/t)
check("C2.18 Lagrange x u_x + t u_t = 0: g(x/t)", x*sp.diff(u, x) + t*sp.diff(u, t))

# C2.25 dominio log: u = e^S, heat u_t = u_xx  <=>  S_t = S_xx + S_x^2 (HJ viscoso, Cole-Hopf)
S = sp.Function('S')(t, x)
u = sp.exp(S)
lhs = sp.simplify((sp.diff(u, t) - sp.diff(u, x, 2))/u)
check("C2.25 Cole-Hopf: (u_t-u_xx)/u = S_t - S_xx - S_x^2", lhs - (sp.diff(S, t) - sp.diff(S, x, 2) - sp.diff(S, x)**2))
# HJ con H(p) = -p^2 ha soluzioni lineari S = tau t + xi x con tau = xi^2 = V(P_heat) (iconale = varieta' caratteristica)
check("C2.25 S lineare: S_t - S_x^2 = 0 sse tau = xi^2", (tau*t + xi*x).diff(t) - (tau*t + xi*x).diff(x)**2 - (tau - xi**2))
summary("t2_first_order")
