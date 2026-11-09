# S4-TERM s2: closed forms at first order in nu before the shock (S4T-T2). Verification only.
import sympy as sp
t, a, x, nu, eps, s = sp.symbols('t a x nu epsilon s')
f = sp.Function('f')            # u0
F, F1, F2, F3 = f(a), f(a).diff(a), f(a).diff(a, 2), f(a).diff(a, 3)
J = 1 + t*F1
ok = []
def chk(name, cond):
    ok.append(bool(cond)); print(('PASS ' if cond else 'FAIL ') + name)
# Eulerian derivatives of a Lagrangian function g(t,a): d_x = g_a/J, d_t|x = g_t - F*g_a/J
dx = lambda g: sp.diff(g, a)/J
dt = lambda g: sp.diff(g, t) - F*sp.diff(g, a)/J
v = F
chk("inviscid: v_t + v v_x = 0", sp.simplify(dt(v) + v*dx(v)) == 0)
vxx = sp.simplify(dx(dx(v)))
chk("v_xx = f2/J^3", sp.simplify(vxx - F2/J**3) == 0)
delta = t*F2/J**2
chk("delta_t + (v delta)_x = v_xx", sp.simplify(dt(delta) + dx(v*delta) - vxx) == 0)
chk("delta(0) = 0", delta.subs(t, 0) == 0)
zeta = F2/J
chk("zeta_t + (v zeta)_x = 0, zeta(0)=f2", sp.simplify(dt(zeta) + dx(v*zeta)) == 0 and sp.simplify(zeta.subs(t, 0) - F2) == 0)
chk("delta - t v_xx = t^2 f1 f2/J^3", sp.simplify(delta - t*vxx - t**2*F1*F2/J**3) == 0)
chk("delta - t zeta = -t^2 f1 f2/J^2", sp.simplify(delta - t*zeta + t**2*F1*F2/J**2) == 0)
# --- jets in t at fixed Eulerian x: f(y) = sum c_k (y-x)^k/k!, a = x + alpha, alpha = -t f(a)
N = 4          # keep t^0..t^N
K = 2*N + 4
c = sp.symbols('c0:%d' % (K+1))
def trunc(e):
    e = sp.expand(e)
    return sum(e.coeff(t, k)*t**k for k in range(N+1))
def fj(j, al):   # f^{(j)}(x+al), al = O(t): only powers al^k with k <= N matter
    return trunc(sum(c[k+j]*al**k/sp.factorial(k) for k in range(0, N+1)))
al = sp.Integer(0)
for _ in range(N+1):
    al = trunc(-t*fj(0, al))
def inv_series(Jt):   # 1/J as truncated series, J = 1 + O(t)
    q = trunc(Jt - 1); res = sp.Integer(1); p = sp.Integer(1)
    for k in range(1, N+1):
        p = trunc(-p*q); res += p
    return trunc(res)
def to_euler_generic(num, Jpow):
    Jt = trunc(1 + t*fj(1, al))
    iJ = inv_series(Jt)
    r = trunc(num)
    for _ in range(Jpow):
        r = trunc(r*iJ)
    return r
chk("Lagrange inversion: a + t f(a) = x", trunc(al + t*fj(0, al)) == 0)
G0, G1, G2, G3, G4 = c[0], c[1], c[2], c[3], c[4]
E1add = trunc(to_euler_generic(t*fj(2, al), 2) - t*G2)
c2 = sp.simplify(E1add.coeff(t, 2))
chk("t^2 coeff of nu-coefficient of E^add = -(2 u1 u2 + u u3)", sp.simplify(c2 + 2*G1*G2 + G0*G3) == 0)
c3 = sp.simplify(E1add.coeff(t, 3))
pred3 = (3*G0**2*G4 + 18*G0*G1*G3 + 12*G0*G2**2 + 18*G1**2*G2)/6   # nu^1 part of E^add_3 from s1
chk("t^3 coeff of nu-coefficient of E^add = nu^1 part of jet E^add_3 (s1)", sp.simplify(c3 - pred3) == 0)
E1AB = to_euler_generic(t**2*fj(1, al)*fj(2, al), 3)
chk("t^2 coeff of nu-coeff of E^mult_AB = u1 u2", sp.simplify(E1AB.coeff(t, 2) - G1*G2) == 0)
E1BA = to_euler_generic(-t**2*fj(1, al)*fj(2, al), 2)
chk("t^2 coeff of nu-coeff of E^mult_BA = -u1 u2", sp.simplify(E1BA.coeff(t, 2) + G1*G2) == 0)
# --- independent check against the exact eps^2 computation (DEVIL-4): u0 = eps sin x
Eint2 = eps**2*(2*nu*t*sp.exp(4*nu*t) - sp.exp(2*nu*t) + 1)*sp.exp(-4*nu*t)/(4*nu)*sp.sin(2*x)
lin_nu = sp.simplify(sp.limit(sp.diff(Eint2, nu), nu, 0))
sub = {c[k]: eps*sp.diff(sp.sin(x), x, k) for k in range(K+1)}
E1add_sin = sp.expand(E1add.subs(sub))
E1add_sin2 = sp.simplify(E1add_sin.coeff(eps, 2))
print("d/dnu E_int^A9(eps^2) at nu=0 :", lin_nu)
print("closed form, eps^2 coefficient (series to t^4):", E1add_sin2)
chk("nu-linear part of exact eps^2 E_int (DEVIL) = eps^2 coeff of closed form, to O(t^5)",
    sp.simplify(sp.series(lin_nu, t, 0, N+1).removeO() - eps**2*E1add_sin2) == 0)
print("closed form, eps^3 coefficient (to t^4):", sp.simplify(sp.expand_trig(E1add_sin.coeff(eps, 3))))
# --- blow-up constants near t* (S4T-P3): sup_z z/(1+z^2)^2 and z/(1+z^2)^3
z = sp.symbols('z', positive=True)
m2 = sp.maximum(z/(1+z**2)**2, z, sp.Interval(0, sp.oo)); m3 = sp.maximum(z/(1+z**2)**3, z, sp.Interval(0, sp.oo))
print("sup z/(1+z^2)^2 =", sp.nsimplify(m2), " sup z/(1+z^2)^3 =", sp.nsimplify(m3))
chk("sup z/(1+z^2)^2 = 3*sqrt(3)/16", sp.simplify(m2 - 3*sp.sqrt(3)/16) == 0)
chk("sup z/(1+z^2)^3 = 25*sqrt(5)/216", sp.simplify(m3 - 25*sp.sqrt(5)/216) == 0)
print("SUMMARY: %d/%d PASS" % (sum(ok), len(ok)))
