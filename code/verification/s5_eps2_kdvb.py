# S4-TERM s5: (a) order-eps^2 A9 interaction for exponential data (S4T-P6) vs DEVIL-4 exact computation;
# (b) KdV-Burgers: first order in d of the dispersive correction in Lagrangian form (S4T-T4(iii), candidate);
# (c) identity E^add = E^NL - (S_B u0 - u0).  Verification only.
import sympy as sp
t, x, nu, eps, a, d = sp.symbols('t x nu epsilon a d')
k1, k2 = sp.symbols('k1 k2', nonzero=True)
ok = []
def chk(name, cond):
    ok.append(bool(cond)); print(('PASS ' if cond else 'FAIL ') + name)
# (a) bracket for a pair of modes (k1, k2), K = k1+k2:  E^add_[2] coefficient of c1 c2 e^{iKx} is (-iK/2) * Br
Br = (sp.exp(-nu*(k1**2 + k2**2)*t) - sp.exp(-nu*(k1 + k2)**2*t))/(2*nu*k1*k2) - t
chk("small-t: Br = -nu t^2 (k1^2+k1k2+k2^2) + O(t^3)", sp.expand(sp.series(Br.subs({k1:sp.Integer(2),k2:sp.Integer(-3)}), t, 0, 3).removeO() + nu*t**2*7) == 0)
chk("Br = O(nu): Br(nu)/nu bounded, numeric nu=1e-12", abs(sp.N(Br.subs({k1:2,k2:-3,t:sp.Rational(7,10),nu:sp.Rational(1,10**12)}),40))<1e-9)
# u0 = eps sin x = eps (e^{ix} - e^{-ix})/(2i): c_{+1} = 1/(2i), c_{-1} = -1/(2i)
c = {1: 1/(2*sp.I), -1: -1/(2*sp.I)}
E2 = 0
for l in (1, -1):
    for m in (1, -1):
        K = l + m
        if K == 0:
            continue    # mode 0: forcing -(iK/2)... = 0
        br = Br.subs({k1: l, k2: m})
        E2 += (-sp.I*K/2)*c[l]*c[m]*sp.exp(sp.I*K*x)*br
E2 = E2*eps**2
Eint2_devil = eps**2*(2*nu*t*sp.exp(4*nu*t) - sp.exp(2*nu*t) + 1)*sp.exp(-4*nu*t)/(4*nu)*sp.sin(2*x)
pts = [(0.3,0.7,0.2,1.1),(1.7,2.9,0.05,0.4),(0.9,5.1,1.3,2.2)]
chk("eps^2 Fourier formula = DEVIL-4 exact E_int^A9 (u0 = eps sin x), 3 float points, tol 1e-12", all(abs(sp.N((E2-Eint2_devil).subs({t:a1,x:a2,nu:a3,eps:a4}),30))<1e-12 for a1,a2,a3,a4 in pts))
# (b) KdV-Burgers: delta_d solves delta_t + (v delta)_x = -v_xxx, delta(0) = 0 (first-order-in-d correction)
f = sp.Function('f'); F, F1, F2, F3 = f(a), f(a).diff(a), f(a).diff(a, 2), f(a).diff(a, 3)
J = 1 + t*F1
dx = lambda g: sp.diff(g, a)/J
dt = lambda g: sp.diff(g, t) - F*sp.diff(g, a)/J
v = F
vxxx = sp.simplify(dx(dx(dx(v))))
chk("v_xxx = f3/J^4 - 3 t f2^2/J^5", sp.simplify(vxxx - (F3/J**4 - 3*t*F2**2/J**5)) == 0)
# antiderivatives computed by hand: int_0^t (1+sb)^-3 ds = t(1+J)/(2J^2), int_0^t s(1+sb)^-4 ds = t^2(2+J)/(6J^3)
q = -t*F3*(1 + J)/(2*J**2) + 3*F2**2*t**2*(2 + J)/(6*J**3)
s_, b_ = sp.symbols('s b', positive=True)
chk('antiderivative 1 (d/dt and value at 0)', sp.simplify(sp.diff(t*(2+t*b_)/(2*(1+t*b_)**2), t) - (1+t*b_)**-3) == 0)
chk('antiderivative 2 (d/dt and value at 0)', sp.simplify(sp.diff(t**2*(3+t*b_)/(6*(1+t*b_)**3), t) - t*(1+t*b_)**-4) == 0)
deltad = sp.simplify(q/J)
print("delta_d (Lagrangian) =", sp.factor(deltad))
chk("delta_d solves delta_t + (v delta)_x = -v_xxx", sp.simplify(dt(deltad) + dx(v*deltad) + vxxx) == 0)
chk("delta_d(0) = 0", sp.simplify(deltad.subs(t, 0)) == 0)
# (c) E^add = E^NL - (S_B u0 - u0) with E^NL = S u0 - e^{tA} u0 and S_A = e^{tA}: algebraic identity
Su, eA, SB, u0 = sp.symbols('Su eA SB u0')
chk("E^add = E^NL - (S_B u0 - u0)", sp.simplify((Su - eA - SB + u0) - ((Su - eA) - (SB - u0))) == 0)
print("SUMMARY: %d/%d PASS" % (sum(ok), len(ok)))
