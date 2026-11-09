"""KA ENC-P0: controlli simbolici.
(1) Ansatz puntuale+gauge generale u = e^{iS} r v(T(t),(x-xi)/rho), S = a x^2 + b x + d,
    per i u_t = -u_xx + (alpha x^2 + beta x + gamma) u, con i v_tau = -v_yy.
    Condizioni: T' = 1/rho^2; con T = id  => rho^2 = 1 => a = 0 => alpha = 0.
(2) Avron-Herbst / Kramers-Henneberger: V = beta(t) x, theta = id, soluzione esplicita.
(3) Lente di Niederer (H = -1/2 d^2 + 1/2 x^2, H_0 = -1/2 d^2): verifica della formula.
(4) Il chirp e^{i a x^2} non preserva H^2: f = (1+x^2)^(-1/2).
(5) Libertà di riparametrizzazione: W_id(t) = U_0(t - theta(t)) W(t) (verifica su onde piane).
"""
import sympy as sp

t, x = sp.symbols('t x', real=True)
I = sp.I

# ---------- (1) ansatz generale ----------
a, b, d, r, T, rho, xi = [sp.Function(n)(t) for n in ('a', 'b', 'd', 'r', 'T', 'rho', 'xi')]
al, be, ga = [sp.Function(n)(t) for n in ('alpha', 'beta', 'gamma')]
v, vy, vyy = sp.symbols('v v_y v_yy')
S = a*x**2 + b*x + d
y = (x - xi)/rho
St, Sx, Sxx = sp.diff(S, t), sp.diff(S, x), sp.diff(S, x, 2)
yt = sp.diff(y, t)
# u/(E r):
vtau = I*vyy  # i v_tau = -v_yy
ut = I*St*v + sp.diff(r, t)/r*v + vtau*sp.diff(T, t) + vy*yt
uxx = I*Sxx*v + (I*Sx)**2*v + 2*I*Sx*vy/rho + vyy/rho**2
V = al*x**2 + be*x + ga
res = sp.expand(I*ut + uxx - V*v)
cvyy = sp.simplify(res.coeff(vyy))
cvy = sp.Poly(sp.expand(res.coeff(vy)), x)
cv = sp.Poly(sp.expand(res.coeff(v).subs({vy: 0, vyy: 0})), x)
print('(1) coeff v_yy :', cvyy, ' => T\' = 1/rho^2')
print('(1) coeff v_y  (poly in x):', [sp.simplify(c) for c in cvy.all_coeffs()])
print('(1) coeff v    (poly in x):', [sp.simplify(c) for c in cv.all_coeffs()])
# theta = id: T = t, rho = 1
sub_id = {T: t, rho: sp.Integer(1)}
cvy_id = [sp.simplify(c.subs(sub_id).doit()) for c in cvy.all_coeffs()]
cv_id = [sp.simplify(c.subs(sub_id).doit()) for c in cv.all_coeffs()]
print('(1) theta=id, v_y coeffs:', cvy_id)
print('(1) theta=id, v coeffs  :', cv_id)
# from v_y: x^1 coeff -> a = 0 ; then x^2 coeff of v: alpha must vanish
x2 = sp.simplify(cv_id[0].subs(a, 0).doit())
print('(1) theta=id, a=0: coefficient of x^2 in v-equation =', x2, ' => alpha = 0 forced')

# ---------- (2) Avron-Herbst con beta(t) e theta = id ----------
B = sp.Function('B')(t)      # B' = beta  (primitive)
beta = sp.diff(B, t)
s = sp.symbols('s')
# u(t,x) = exp(-i B x - i int_0^t B^2) v(t, x - xi), xi' = -2 B  (for H = -d^2)
Xi = sp.Function('Xi')(t)
vf = sp.Function('vf')
Phi = sp.Function('Phi')(t)   # Phi' = B^2
u = sp.exp(-I*B*x - I*Phi)*vf(t, x - Xi)
expr = I*sp.diff(u, t) + sp.diff(u, x, 2) - beta*x*u
expr = expr.subs({sp.Derivative(Xi, t): -2*B, sp.Derivative(Phi, t): B**2})
# use free equation: vf_t = i vf_yy
yy = sp.symbols('yy')
expr = expr.subs(sp.Subs(sp.Derivative(vf(t, yy), t), yy, x - Xi), I*sp.Subs(sp.Derivative(vf(t, yy), yy, 2), yy, x - Xi))
expr = sp.simplify(sp.expand(expr.doit()/sp.exp(-I*B*x - I*Phi)))
print('(2) Avron-Herbst residuo (theta=id):', expr)

# ---------- (3) lente di Niederer ----------
tau, yv = sp.symbols('tau y', real=True)
k = sp.symbols('k', real=True)
# test con soluzioni libere esplicite (pacchetto gaussiano + onda piana), H_0 = -1/2 d^2
def vfree(tau_, y_):
    return sp.exp(I*k*y_ - I*k**2*tau_/2)
def vgauss(tau_, y_):
    return (1 + I*tau_)**sp.Rational(-1, 2)*sp.exp(-y_**2/(2*(1 + I*tau_)))
for name, vv in (('onda piana', vfree), ('gaussiana', vgauss)):
    uu = sp.cos(t)**sp.Rational(-1, 2)*sp.exp(-I*x**2*sp.tan(t)/2)*vv(sp.tan(t), x/sp.cos(t))
    resid = I*sp.diff(uu, t) + sp.diff(uu, x, 2)/2 - x**2*uu/2
    print('(3) lente, residuo', name, ':', sp.simplify(sp.expand(resid/uu)))

# ---------- (4) chirp non preserva H^2 ----------
aa = sp.symbols('aa', positive=True)
f = (1 + x**2)**sp.Rational(-1, 2)
g = sp.exp(I*aa*x**2)*f
g2 = sp.simplify(sp.diff(g, x, 2)*sp.exp(-I*aa*x**2))
lead = sp.limit(sp.Abs(g2)/sp.Abs(x), x, sp.oo)
print('(4) f in H^2: |f\'\'|^2 integrabile:', sp.integrate(sp.diff(f, x, 2)**2, (x, -sp.oo, sp.oo)))
print('(4) |(e^{iax^2} f)\'\'| / |x| -> ', lead, '  (quindi non in L^2)')

# ---------- (5) riparametrizzazione ----------
# su onde piane e^{iky}: U_0(s) e^{iky} = e^{-i k^2 s/2} e^{iky}; W_id(t) := U_0(t - theta(t)) W(t)
# soddisfa W_id(t) U_V(t) u0 = U_0(t) W(0) u0: basta U_0(t-theta)U_0(theta) = U_0(t)
th = sp.Function('theta')(t)
print('(5) fase U_0(t-theta)U_0(theta)/U_0(t) =', sp.simplify(sp.exp(-I*k**2*(t - th)/2)*sp.exp(-I*k**2*th/2)/sp.exp(-I*k**2*t/2)))
