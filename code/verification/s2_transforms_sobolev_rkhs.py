"""PR-C2d / C2.14, C2.52 — Fourier/Plancherel, heat kernel, Sobolev RKHS kernels.
Convention: F u(xi) = int u(x) e^{-i x xi} dx ; Plancherel ||u||^2 = (1/2pi) ||Fu||^2.
"""
import sympy as sp
x, y, xi, t, D, a, c = sp.symbols('x y xi t D a c', real=True)
tp, Dp, ap = sp.symbols('tp Dp ap', positive=True)
res = []
def ok(name, cond):
    res.append((name, bool(cond))); print(('PASS ' if cond else 'FAIL ') + name)

F = lambda f: sp.simplify(sp.integrate(f*sp.exp(-sp.I*x*xi), (x, -sp.oo, sp.oo), conds='none'))

# (a) heat kernel K_t = (4 pi D t)^{-1/2} exp(-x^2/(4Dt)); F K_t = exp(-D t xi^2)
K = (4*sp.pi*Dp*tp)**sp.Rational(-1, 2)*sp.exp(-x**2/(4*Dp*tp))
ok('a1 F[heat kernel] = exp(-D t xi^2)', sp.simplify(F(K) - sp.exp(-Dp*tp*xi**2)) == 0)
ok('a2 heat kernel solves K_t = D K_xx', sp.simplify(sp.diff(K, tp) - Dp*sp.diff(K, x, 2)) == 0)

# (b) Plancherel on a Gaussian
g = sp.exp(-ap*x**2)
lhs = sp.integrate(g**2, (x, -sp.oo, sp.oo))
Fg = F(g)
rhs = sp.integrate(sp.simplify(Fg*sp.conjugate(Fg)), (xi, -sp.oo, sp.oo))/(2*sp.pi)
ok('b1 Plancherel ||g||^2 = (1/2pi)||Fg||^2', sp.simplify(lhs - rhs) == 0)

# (c) H^1(R) with <u,v> = int (u v + u' v'): RK = (1/2) e^{-|x-y|}  (Fourier: 1/(2pi) int e^{i xi (x-y)}/(1+xi^2))
K1hat = 1/(1+xi**2)
K1 = sp.simplify(sp.integrate(K1hat*sp.cos(xi*x), (xi, -sp.oo, sp.oo))/(2*sp.pi))
ok('c1 inverse F of 1/(1+xi^2) = e^{-|x|}/2 (x>0 branch)', sp.simplify(K1.subs(x, sp.Symbol('q', positive=True)) - sp.exp(-sp.Symbol('q', positive=True))/2) == 0)
# reproducing property at point y0 for test u = exp(-s^2)
s, y0 = sp.symbols('s y0', real=True)
u = sp.exp(-s**2)
kl = sp.exp(-(y0-s))/2   # s<y0
kr = sp.exp(-(s-y0))/2   # s>y0
ip = sp.integrate(kl*u + sp.diff(kl, s)*sp.diff(u, s), (s, -sp.oo, y0)) + sp.integrate(kr*u + sp.diff(kr, s)*sp.diff(u, s), (s, y0, sp.oo))
ok('c2 <K(y0,.),u>_{H^1} = u(y0)', sp.simplify(ip - u.subs(s, y0)) == 0)
# consequence: Sobolev embedding H^1(R) in C_b with sharp constant |u(y)| <= K(y,y)^{1/2} ||u|| = ||u||/sqrt 2
ok('c3 K(y,y)=1/2  =>  sup|u| <= ||u||_{H^1}/sqrt(2)', sp.Rational(1, 2) == sp.limit(sp.exp(-sp.Symbol('q', positive=True))/2, sp.Symbol('q', positive=True), 0))

# (d) Paley-Wiener space PW_pi (band [-pi,pi]): RK sinc; check F-side: kernel hat = 1_{[-pi,pi]} e^{-i xi y}
ksinc = sp.simplify(sp.integrate(sp.exp(sp.I*xi*(x-y)), (xi, -sp.pi, sp.pi))/(2*sp.pi))
ok('d1 PW_pi reproducing kernel = sin(pi(x-y))/(pi(x-y))', sp.simplify(ksinc.rewrite(sp.sin) - sp.sin(sp.pi*(x-y))/(sp.pi*(x-y))) == 0)
# sampling: integer translates orthonormal: <sinc(.-0), sinc(.-1)> = 0 computed on F side
ok('d2 <sinc_0,sinc_1> = (1/2pi) int_{-pi}^{pi} e^{i xi} dxi = 0', sp.integrate(sp.exp(sp.I*xi), (xi, -sp.pi, sp.pi)) == 0)

# (e) exponential-polynomial kernel classes are NOT in L^2(R): e^{x} has infinite norm, x e^{-x^2} is fine
ok('e1 int_R e^{2x} dx diverges (kernel of d/dx-1 not in L^2(R))', sp.integrate(sp.exp(2*x), (x, -sp.oo, sp.oo)) == sp.oo)

# (f) Fourier symbol of transport+diffusion: u_t = D u_xx - c u_x  ->  u^ = exp(t(-D xi^2 - i c xi)) u0^
uhat = sp.exp(tp*(-Dp*xi**2 - sp.I*c*xi))
ok('f1 symbol additivity: log uhat / t = -D xi^2 - i c xi', sp.simplify(sp.expand_log(sp.log(uhat), force=True)/tp - (-Dp*xi**2 - sp.I*c*xi)) == 0)

print('ALL PASS' if all(c for _, c in res) else 'SOME FAIL')
