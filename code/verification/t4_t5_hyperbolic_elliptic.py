"""T4 iperbolico (C2.8, C2.22, C2.31) e T5 ellittico (C2.9, C2.20, C2.34, C2.35)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sympy as sp
from _common import check, check_true, summary, quotient_dim

t, x, y = sp.symbols('t x y', real=True)
c, m, kap = sp.symbols('c m kappa', positive=True)
tau, xi = sp.symbols('tau xi')
f, g = sp.Function('f'), sp.Function('g')
k = sp.symbols('k', integer=True, nonzero=True)
n = sp.symbols('n', integer=True)

W = lambda u: sp.diff(u, t, 2) - c**2*sp.diff(u, x, 2)
# C2.8 d'Alembert e fattorizzazione
check("C2.8 fattorizzazione tau^2-c^2xi^2 = (tau-c xi)(tau+c xi)", sp.expand((tau - c*xi)*(tau + c*xi)) - (tau**2 - c**2*xi**2))
u = f(x - c*t) + g(x + c*t)
check("C2.8 d'Alembert f(x-ct)+g(x+ct)", W(u))
check("C2.8 estrazione componente: (d_t + c d_x)u = 2c g'(x+ct)",
      sp.diff(u, t) + c*sp.diff(u, x) - 2*c*sp.diff(g(x + c*t), x))
check_true("C2.8 dim ker(d_t-c d_x, d_t+c d_x) = 1 (costanti)", quotient_dim([tau - c*xi, tau + c*xi], [tau, xi]) == 1)
check("C2.8 onda stazionaria sin(kx)cos(ckt)", W(sp.sin(k*x)*sp.cos(c*k*t)))
check("C2.8 sin(kx)cos(ckt) = (sin k(x-ct) + sin k(x+ct))/2",
      sp.expand_trig(sp.sin(k*x)*sp.cos(c*k*t) - (sp.sin(k*(x - c*t)) + sp.sin(k*(x + c*t)))/2))
# Gram tra classi destra/sinistra su T x [0, pi/c]: nullo per k != 0
T0 = sp.pi/c
gr = sp.integrate(sp.exp(-2*sp.I*c*k*t), (t, 0, T0))
check("C2.8 <e^{ik(x-ct)}, e^{ik(x+ct)}> su [0,pi/c] = 0 (k!=0)", sp.simplify(gr.rewrite(sp.cos)))

# C2.22 sistema iperbolico U_t + A U_x = 0, A = [[0,c],[c,0]]
A = sp.Matrix([[0, c], [c, 0]])
P, Dg = A.diagonalize()
Linv = P.inv()
check_true("C2.22 autovalori reali distinti +-c", set(Dg.diagonal()) == {c, -c})
U = sum((P[:, j]*sp.Function(f'g{j}')(x - Dg[j, j]*t) for j in range(2)), sp.zeros(2, 1))
res = U.diff(t) + A*U.diff(x)
check("C2.22 U = sum r_j g_j(x - lambda_j t)", sp.simplify(res[0]) + sp.simplify(res[1]))
check("C2.22 duale: L R = I (autovettori sinistri biortogonali)", sp.simplify((Linv*P - sp.eye(2)).norm()))
# riduzione: u_t = c v_x, v_t = c u_x  ==> u_tt = c^2 u_xx
check("C2.22 det(tau I + A xi) = tau^2 - c^2 xi^2", sp.expand((tau*sp.eye(2) + A*xi).det() - (tau**2 - c**2*xi**2)))

# C2.31 Klein-Gordon u_tt - u_xx + m^2 u = 0
KG = lambda u: sp.diff(u, t, 2) - sp.diff(u, x, 2) + m**2*u
rho = sp.sqrt(t**2 - x**2)
check("C2.31 funzione di Riemann J0(m sqrt(t^2-x^2))", KG(sp.besselj(0, m*rho)))
om = sp.sqrt(kap**2 + m**2)
check("C2.31 onda piana e^{i kappa x - i omega t}", KG(sp.exp(sp.I*kap*x - sp.I*om*t)))
# irriducibilita': forma quadratica tau^2 - xi^2 + m^2 omogeneizzata ha matrice non singolare
Q = sp.Matrix([[1, 0, 0], [0, -1, 0], [0, 0, m**2]])
check_true("C2.31 tau^2-xi^2+m^2 irriducibile (det forma 3x3 = -m^2 != 0)", sp.simplify(Q.det()) != 0)

# T5 C2.9 Laplace nel piano (t,x) ~ (y,x)
Lap = lambda u: sp.diff(u, x, 2) + sp.diff(u, y, 2)
check("C2.9 tau^2+xi^2 = (tau+i xi)(tau-i xi)", sp.expand((tau + sp.I*xi)*(tau - sp.I*xi)) - (tau**2 + xi**2))
check("C2.9 f(x+iy)+g(x-iy) armonica", Lap(f(x + sp.I*y) + g(x - sp.I*y)))
check_true("C2.9 dim ker(d_y+i d_x, d_y-i d_x) = 1", quotient_dim([tau + sp.I*xi, tau - sp.I*xi], [tau, xi]) == 1)
r = sp.sqrt(x**2 + y**2)
check("C2.9 log r armonica (x!=0)", Lap(sp.log(r)))
rr, th = sp.symbols('r theta', positive=True)
Pk = (1 - rr**2)/(1 - 2*rr*sp.cos(th) + rr**2)
LapPol = lambda u: sp.diff(u, rr, 2) + sp.diff(u, rr)/rr + sp.diff(u, th, 2)/rr**2
check("C2.34 nucleo di Poisson del disco armonico", LapPol(Pk))
for nn in range(4):
    check(f"C2.9 r^{nn} cos({nn} theta) armonica", LapPol(rr**nn*sp.cos(nn*th)))
# Bergman: <z^n, z^m>_{L2(D)} = pi/(n+1) delta; K(z,w) = sum (n+1)/pi (z wbar)^n = 1/(pi(1-z wbar)^2)
rho_, ph = sp.symbols('rho phi', positive=True)
okb = True
for a_ in range(3):
    for b_ in range(3):
        val = sp.integrate(sp.integrate(rho_**(a_ + b_)*sp.exp(sp.I*(a_ - b_)*ph)*rho_, (ph, 0, 2*sp.pi)), (rho_, 0, 1))
        okb &= sp.simplify(val - (sp.pi/(a_ + 1) if a_ == b_ else 0)) == 0
check_true("C2.9 Bergman: <z^a,z^b> = pi/(a+1) delta (a,b<=2)", okb)
q = sp.symbols('q')
check("C2.9 kernel di Bergman: sum_{n<=20} (n+1) q^n = serie di 1/(1-q)^2", sum((j + 1)*q**j for j in range(21)) - sp.series(1/(1 - q)**2, q, 0, 21).removeO())

# C2.35 Helmholtz
kk = sp.symbols('k_h', positive=True)
Hel = lambda u: LapPol(u) + kk**2*u
for nn in range(4):
    check(f"C2.35 J_{nn}(kr) cos({nn} theta)", Hel(sp.besselj(nn, kk*rr)*sp.cos(nn*th)))
check("C2.35 Y_0(kr) (radiale, r>0)", Hel(sp.bessely(0, kk*rr)))
d = sp.symbols('d', real=True)
check("C2.35 onda piana e^{ik(x cos d + y sin d)}", Lap(sp.exp(sp.I*kk*(x*sp.cos(d) + y*sp.sin(d)))) + kk**2*sp.exp(sp.I*kk*(x*sp.cos(d) + y*sp.sin(d))))
check("C2.35 Helmholtz modificato K_0(kr)", LapPol(sp.besselk(0, kk*rr)) - kk**2*sp.besselk(0, kk*rr))
# Jacobi-Anger (controllo numerico, non metodo): e^{i z cos th} = sum i^n J_n(z) e^{i n th}
import mpmath as mp
zv, tv = 1.7, 0.6
lhs = mp.e**(1j*zv*mp.cos(tv))
rhs = sum((1j)**nn*mp.besselj(nn, zv)*mp.e**(1j*nn*tv) for nn in range(-30, 31))
check_true("C2.35 Jacobi-Anger (controllo numerico)", abs(lhs - rhs) < 1e-12, f"err={float(abs(lhs-rhs)):.1e}")
# C2.20 BVP 1D: -u'' = lambda u, Dirichlet su [0,pi]: sin(nx), lambda=n^2 ; Robin u'(0)=h u(0)
nn_ = sp.symbols('nn', positive=True, integer=True)
check("C2.20 Dirichlet: sin(n x) autofunzione, sin(n pi)=0", sp.sin(nn_*sp.pi))
summary("t4_t5")
