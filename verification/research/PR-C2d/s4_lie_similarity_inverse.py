"""PR-C2d / C2.49, C2.50, C2.60, C2.48 — similarity, Lie symmetries, identification via jet-Gram kernel, WKB."""
import sympy as sp
x, t, v, k, eps = sp.symbols('x t v k epsilon', real=True)
tp = sp.symbols('tp', positive=True)
res = []
def ok(name, cond):
    res.append((name, bool(cond))); print(('PASS ' if cond else 'FAIL ') + name)
heat = lambda u, T=t: sp.simplify(sp.diff(u, T) - sp.diff(u, x, 2))

# (a) similarity (C2.49): u = t^{-1/2} f(x/sqrt t) reduces heat eq to ODE f'' + (z/2) f' + f/2 = 0 ; Gaussian solves
z = sp.Symbol('z'); fz = sp.exp(-z**2/4)
ok('a1 similarity ODE solved by exp(-z^2/4)', sp.simplify(sp.diff(fz, z, 2) + z/2*sp.diff(fz, z) + fz/2) == 0)
ok('a2 => t^{-1/2} exp(-x^2/4t) solves heat', heat(tp**sp.Rational(-1, 2)*sp.exp(-x**2/(4*tp)), tp) == 0)

# (b) Lie (C2.50): Galilean boost of heat eq maps solutions to solutions: u -> e^{-v x + v^2 t} u(x-2vt, t)
for name, u0 in [('exp(kx+k^2t)', lambda X, T: sp.exp(k*X + k**2*T)), ('x^2+2t', lambda X, T: X**2 + 2*T)]:
    assert heat(u0(x, t)) == 0
    ub = sp.exp(-v*x + v**2*t)*u0(x - 2*v*t, t)
    ok(f'b1 Galilean boost preserves heat solution {name}', heat(ub) == 0)
# scaling symmetry x->lam x, t->lam^2 t
lam = sp.Symbol('lam', positive=True)
ok('b2 scaling u(lam x, lam^2 t) of exp(kx+k^2t) solves heat', heat(sp.exp(k*lam*x + k**2*lam**2*t)) == 0)

# (c) inverse/identification (C2.60, link to C3/P4): Gram of the jet on a dictionary
# dictionary Phi(u) = (u_t, u_x, u_xx, u)
def jet_gram(u):
    Phi = sp.Matrix([sp.diff(u, t), sp.diff(u, x), sp.diff(u, x, 2), u])
    M = Phi*Phi.T
    return M.applyfunc(lambda e: sp.integrate(sp.integrate(sp.expand(e), (x, 0, 2*sp.pi)), (t, 0, 1)))
u2 = sp.exp(-t)*sp.sin(x) + sp.exp(-4*t)*sp.sin(2*x)
G2 = jet_gram(u2); ns2 = G2.nullspace()
ok('c1 two modes: dim ker Gram = 1 and kernel ~ (1,0,-1,0) (u_t-u_xx=0 identified)',
   len(ns2) == 1 and sp.simplify(ns2[0]/ns2[0][0] - sp.Matrix([1, 0, -1, 0])) == sp.zeros(4, 1))
u1 = sp.exp(-t)*sp.sin(x)
G1 = jet_gram(u1); ns1 = G1.nullspace()
ok('c2 one mode: dim ker Gram = 2 (non-identifiable: u_t+u=0 and u_xx+u=0 also annihilate)', len(ns1) == 2)

# (d) WKB (C2.48): eps^2 y'' = Q(x) y, Q=1+x^2 ; y ~ Q^{-1/4} exp(+-(1/eps) int sqrt Q): residual is O(eps^2) relative
Q = 1 + x**2
S0 = sp.integrate(sp.sqrt(Q), x)
yW = Q**sp.Rational(-1, 4)*sp.exp(S0/eps)
resid = sp.simplify((eps**2*sp.diff(yW, x, 2) - Q*yW)/yW)
ok('d1 WKB residual (eps^2 y\'\' - Q y)/y = O(eps^2) (no O(1), O(eps) terms)', sp.simplify(sp.limit(resid/eps**2, eps, 0) - resid/eps**2) == 0 and sp.limit(resid, eps, 0) == 0)

print('ALL PASS' if all(c for _, c in res) else 'SOME FAIL')
