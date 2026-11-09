"""T3 — parabolico (C2.7 diffusione, C2.21 parabolico generale, C2.39 mezzi porosi)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sympy as sp
from _common import check, check_true, summary, quotient_dim

x = sp.symbols('x', real=True)
t, D, T0 = sp.symbols('t D T', positive=True)
c = sp.symbols('c', nonzero=True)
xi, tau = sp.symbols('xi tau')
k = sp.symbols('k', integer=True)

H = lambda u: sp.diff(u, t) - D*sp.diff(u, x, 2)

# C2.7 esponenziali su V(P): tau = D xi^2
check("C2.7 H e^{D xi^2 t + xi x} = 0", H(sp.exp(D*xi**2*t + xi*x)))
check("C2.7 modi su T: e^{ikx - D k^2 t}", H(sp.exp(sp.I*k*x - D*k**2*t)))
G = sp.exp(-x**2/(4*D*t))/sp.sqrt(4*sp.pi*D*t)
check("C2.7 nucleo del calore G", H(G))
check("C2.7 massa di G = 1", sp.integrate(G, (x, -sp.oo, sp.oo)) - 1)

# polinomi del calore v_n = d^n/dxi^n e^{D xi^2 t + xi x}|_{xi=0} (Rosenbloom-Widder, D=1 nel loro testo)
def v(n, tt=t):
    return sp.expand(sp.diff(sp.exp(D*xi**2*tt + xi*x), xi, n).subs(xi, 0))
for n in range(6):
    check(f"C2.7 polinomio del calore v_{n} risolve", H(v(n)))
check("C2.7 v_4 = x^4 + 12 D t x^2 + 12 D^2 t^2", v(4) - (x**4 + 12*D*t*x**2 + 12*D**2*t**2))

# funzioni associate w_m = (-d_x)^m G; biortogonalita' int v_n(x,-t) w_m(x,t) dx = n! delta_nm
def w(m):
    return (-1)**m*sp.diff(G, x, m)
ok_all = True
for n in range(5):
    for m in range(5):
        val = sp.simplify(sp.integrate(v(n, -t)*w(m), (x, -sp.oo, sp.oo)))
        target = sp.factorial(n) if n == m else 0
        ok_all &= sp.simplify(val - target) == 0
check_true("C2.7 biortogonalita' <v_n(.,-t), w_m(.,t)> = n! delta_nm  (n,m<=4)", ok_all)
for m in range(5):
    check(f"C2.7 w_{m} risolve il calore", H(w(m)))
# w_n = (4Dt)^{-n/2} H_n(x/sqrt(4Dt)) G  (funzioni di Hermite)
for n in range(5):
    check(f"C2.7 w_{n} = (4Dt)^(-n/2) H_{n}(x/sqrt(4Dt)) G",
          w(n) - (4*D*t)**sp.Rational(-n, 2)*sp.hermite(n, x/sp.sqrt(4*D*t))*G)

# trasformata di Appell (D=1): u(x,t) -> G(x,t) u(x/t, -1/t) manda soluzioni in soluzioni
G1 = G.subs(D, 1)
H1 = lambda u: sp.diff(u, t) - sp.diff(u, x, 2)
for n in range(4):
    vn = v(n).subs(D, 1)
    app = G1*vn.subs({x: x/t, t: -1/t}, simultaneous=True)
    check(f"C2.7 Appell(v_{n}) risolve il calore", H1(app))

# Gram su T x [0,T]: <e^{ikx-Dk^2 t}, e^{ilx-Dl^2 t}> = 2 pi delta_kl (1-e^{-2Dk^2T})/(2Dk^2)
kk = sp.symbols('kk', positive=True)
ip = sp.integrate(sp.exp(-2*D*kk**2*t), (t, 0, T0))*2*sp.pi
check("C2.7 Gram diagonale nel modo k", ip - 2*sp.pi*(1 - sp.exp(-2*D*kk**2*T0))/(2*D*kk**2))

# intersezione ker(trasporto) ∩ ker(calore): ideale (tau + c xi, tau - D xi^2), dim 2
dim = quotient_dim([tau + c*xi, tau - D*xi**2], [tau, xi])
check_true("C2.7xC2.6 dim C[tau,xi]/(tau+c xi, tau-D xi^2) = 2", dim == 2, f"dim={dim}")
e2 = sp.exp((c**2*t - c*D*x)/D**2)  # punto (tau,xi) = (c^2/D, -c/D)
e2 = sp.exp(c**2*t/D - c*x/D)
check("C2.7xC2.6 e^{c^2 t/D - c x/D} in ker(trasporto)", sp.diff(e2, t) + c*sp.diff(e2, x))
check("C2.7xC2.6 e^{c^2 t/D - c x/D} in ker(calore)", H(e2))

# C2.21 parabolico a coeff. variabili
# OU: u_t = u_xx - x u_x, autofunzioni He_n(x) e^{-n t}
def He(n, z):
    return sp.expand(2**sp.Rational(-n, 2)*sp.hermite(n, z/sp.sqrt(2)))
for n in range(6):
    u = He(n, x)*sp.exp(-n*t)
    check(f"C2.21 OU: He_{n}(x)e^(-{n}t)", sp.diff(u, t) - sp.diff(u, x, 2) + x*sp.diff(u, x))
# algebra di Lie {d^2, x d, x^2, 1}: chiusa (sl2 + centro) -> Wei-Norman / Mehler
f = sp.Function('f')(x)
d2 = lambda w_: sp.diff(w_, x, 2)
xd = lambda w_: x*sp.diff(w_, x)
x2 = lambda w_: x**2*w_
check("C2.21 [d^2, x d] = 2 d^2", d2(xd(f)) - xd(d2(f)) - 2*d2(f))
check("C2.21 [d^2, x^2] = 4 x d + 2", d2(x2(f)) - x2(d2(f)) - (4*xd(f) + 2*f))
check("C2.21 [x d, x^2] = 2 x^2", xd(x2(f)) - x2(xd(f)) - 2*x2(f))
# Euler/Black-Scholes: u_t = x^2 u_xx + x u_x = (x d)^2 u, soluzioni x^xi e^{xi^2 t}
xp = sp.symbols('xp', positive=True)
u = xp**xi*sp.exp(xi**2*t)
check("C2.21 (x d)^2: x^xi e^{xi^2 t}", sp.diff(u, t) - xp**2*sp.diff(u, xp, 2) - xp*sp.diff(u, xp))
# diffusivita' variabile (forma divergenza) esempio esatto: u_t = (x^2 u_x)_x su x>0 -> x^m e^{m(m+1)t}
m = sp.symbols('m')
u = xp**m*sp.exp(m*(m + 1)*t)
check("C2.21 (x^2 u_x)_x: x^m e^{m(m+1)t}", sp.diff(u, t) - sp.diff(xp**2*sp.diff(u, xp), xp))

# C2.39 mezzo poroso m=2 (u_t = (u^2)_xx), Barenblatt nella regione di supporto
C0 = sp.symbols('C0', positive=True)
u = t**sp.Rational(-1, 3)*(C0 - x**2/(12*t**sp.Rational(2, 3)))
check("C2.39 Barenblatt m=2 (interno supporto)", sp.diff(u, t) - sp.diff(u**2, x, 2))
summary("t3_parabolic")
