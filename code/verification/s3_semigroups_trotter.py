"""PR-C2d / C2.53 — sum of generators, product formula, E_int identities, BCH commutator."""
import sympy as sp
x, xi, t, c = sp.symbols('x xi t c', real=True)
tp, Dp = sp.symbols('tp Dp', positive=True)
a1, a2 = sp.symbols('a1 a2')
res = []
def ok(name, cond):
    res.append((name, bool(cond))); print(('PASS ' if cond else 'FAIL ') + name)

# (a) commuting case (constant coeff.): heat kernel convolved with transport shift = advection-diffusion kernel
K = (4*sp.pi*Dp*tp)**sp.Rational(-1, 2)*sp.exp(-(x - c*tp)**2/(4*Dp*tp))   # = S_transport(t) S_heat(t) delta
ok('a1 K solves K_t = D K_xx - c K_x', sp.simplify(sp.diff(K, tp) - Dp*sp.diff(K, x, 2) + c*sp.diff(K, x)) == 0)

# (b) additive picture: e^{t(a1+a2)} - 1 = (e^{ta1}-1)+(e^{ta2}-1)+(e^{ta1}-1)(e^{ta2}-1)  =>  E_int = (K1-d)*(K2-d)*u0
E1, E2 = sp.exp(t*a1) - 1, sp.exp(t*a2) - 1
ok('b1 E_int bilinear identity (N=2)', sp.simplify(sp.exp(t*(a1+a2)) - 1 - (E1 + E2 + E1*E2)) == 0)
# N=3 inclusion-exclusion has 2^3-1 = 7 terms; log-symbol picture has 3
a3 = sp.symbols('a3'); E3 = sp.exp(t*a3) - 1
expand3 = sp.expand((1+E1)*(1+E2)*(1+E3) - 1)
ok('b2 N=3: product expansion has 2^3-1=7 monomials in E_i', len(sp.Add.make_args(sp.expand((1+sp.Symbol('p'))*(1+sp.Symbol('q'))*(1+sp.Symbol('w')) - 1))) == 7)
ok('b3 log-symbol: log(e^{ta1}e^{ta2}e^{ta3}) = t(a1+a2+a3) (3 terms)', sp.simplify(sp.expand_log(sp.log(sp.exp(t*a1)*sp.exp(t*a2)*sp.exp(t*a3)), force=True) - t*(a1+a2+a3)) == 0)

# (c) non-commuting (matrix model): e^{tA}e^{tB} - e^{t(A+B)} = (t^2/2)[A,B] + O(t^3)
A = sp.Matrix([[0, 1], [0, 0]]); B = sp.Matrix([[0, 0], [1, 0]])
eA = (t*A).exp(); eB = (t*B).exp(); eAB = (t*(A+B)).exp()
diff = (eA*eB - eAB).applyfunc(lambda z: sp.series(z, t, 0, 3).removeO())
ok('c1 BCH 2nd order: e^{tA}e^{tB}-e^{t(A+B)} = t^2/2 [A,B] + O(t^3)', sp.simplify(diff - t**2/2*(A*B - B*A)) == sp.zeros(2))
# Lie-Trotter: (e^{tA/n} e^{tB/n})^n -> e^{t(A+B)} ; error ~ t^2/(2n)[A,B]
nn = sp.Symbol('n', positive=True)
lt = ((t/nn*A).exp()*(t/nn*B).exp())
# first-order-in-1/n error term of the product formula, from BCH: log = (t/n)(A+B) + (t/n)^2/2 [A,B] + ...
# control (exact rational matrices, t=1): n*[(e^{A/n}e^{B/n})^n - e^{A+B}] -> (1/2)[A,B]·(correction) ; check error ratio ~ 1/n
def trotter_err(N):
    step = ((A/N).exp()*(B/N).exp()).evalf(40)
    P = step**N
    return (P - (A+B).exp().evalf(40)).norm()
e10, e100 = trotter_err(10), trotter_err(100)
ok('c2 Lie-Trotter error is O(1/n): err(10)/err(100) ~ 10', abs(e10/e100 - 10) < 0.5)

# (d) PDE commutator: [d_xx, x] = 2 d_x  (heat + linear potential: non-commuting, E_int via commutators)
f = sp.Function('f')
comm = sp.diff(x*f(x), x, 2) - x*sp.diff(f(x), x, 2)
ok('d1 [d_x^2, x] f = 2 f\'', sp.simplify(comm - 2*sp.diff(f(x), x)) == 0)
# (e) generator check: S(t) = e^{-D t xi^2} on Fourier side is a C0 contraction semigroup on L^2 (|symbol|<=1)
ok('e1 |e^{-D t xi^2 - i c t xi}| <= 1 (dissipative symbol, Lumer-Phillips)', sp.simplify(sp.Abs(sp.exp(tp*(-Dp*xi**2 - sp.I*c*xi))) - sp.exp(-Dp*tp*xi**2)) == 0)
# Airy: u_t + u_xxx = 0, symbol i xi^3 -> unitary group (Stone)
ok('e2 Airy symbol: |e^{i t xi^3}| = 1 (unitary group, Stone)', sp.simplify(sp.Abs(sp.exp(sp.I*tp*xi**3))) == 1)

print('ALL PASS' if all(c for _, c in res) else 'SOME FAIL')
