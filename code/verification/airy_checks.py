"""OP-NL: checks for the linear (Airy) analogue of INT-Q1 (PROOF_PACKAGE.md §1.3).
u(t,x) = int_R exp(-a k^2 + i k x + i k^3 t) dk  (a > 0), a Schwartz solution of u_t + u_xxx = 0
with nowhere-vanishing spatial Fourier transform, has the closed form
u = 2 pi (3t)^(-1/3) exp(a x/(3t) + 2a^3/(27 t^2)) Ai(Z), Z = (x + a^2/(3t)) / (3t)^(1/3),
and satisfies an autonomous polynomial ODE in x of order 4 for every t > 0."""
import sympy as sp
import mpmath as mp

ok = 0
tot = 0


def report(name, cond, info=""):
    global ok, tot
    tot += 1
    ok += bool(cond)
    print(("OK  " if cond else "FAIL"), name, info)


t, x, a, z = sp.symbols('t x a z', positive=True)
A = sp.Function('A')
tau = (3 * t) ** sp.Rational(1, 3)
Z = (x + a ** 2 / (3 * t)) / tau
C = a * x / (3 * t) + 2 * a ** 3 / (27 * t ** 2)
u = 2 * sp.pi / tau * sp.exp(C) * A(Z)


def airy_reduce(e):
    # replace A'' -> z A, repeatedly, for A evaluated at Z
    for _ in range(6):
        e = e.subs(sp.Derivative(A(Z), (Z, 2)), Z * A(Z))
        e = e.replace(lambda q: isinstance(q, sp.Subs), lambda q: q.doit())
    return e


# 1. u solves the Airy equation u_t + u_xxx = 0 (using A'' = z A)
Ad, Ad1 = sp.symbols('Ad Ad1')  # values A(Z), A'(Z)


def to_vals(e):
    """express derivatives of A(Z) through A(Z), A'(Z) using A''=zA."""
    e = e.doit()
    # sympy writes derivatives as Subs(Derivative(A(_xi), _xi, n), _xi, Z)
    def repl(q):
        n = q.expr.derivative_count if isinstance(q.expr, sp.Derivative) else 0
        return sp.Symbol('Dn%d' % n)
    e = e.replace(lambda q: isinstance(q, sp.Subs), repl)
    e = e.subs(A(Z), Ad)
    # reduce Dn_k: D0=Ad, D1=Ad1, D_{k+2} = d^k/dz^k (z A)
    zz = sp.Symbol('zz')
    # build table of A^{(n)} in terms of A, A' as polynomials in z
    tab = {0: (sp.Integer(1), sp.Integer(0)), 1: (sp.Integer(0), sp.Integer(1))}
    for n in range(2, 8):
        c0, c1 = tab[n - 1]  # A^{(n-1)} = c0 A + c1 A'
        # derivative: c0' A + c0 A' + c1' A' + c1 z A
        tab[n] = (sp.diff(c0, zz) + c1 * zz, c0 + sp.diff(c1, zz))
    for n in range(2, 8):
        c0, c1 = tab[n]
        e = e.subs(sp.Symbol('Dn%d' % n), (c0 * Ad + c1 * Ad1).subs(zz, Z))
    e = e.subs(sp.Symbol('Dn1'), Ad1)
    return sp.simplify(e)


res = to_vals(sp.diff(u, t) + sp.diff(u, x, 3))
report("Airy equation u_t + u_xxx = 0 for the closed form", sp.simplify(res) == 0)

# 2. Riccati form: w = u_x/u = a/(3t) + R/tau, R = A'(Z)/A(Z), dR/dz = z - R^2
R = sp.Symbol('R')
w = a / (3 * t) + R / tau
dRdx = (Z - R ** 2) / tau


def dx(e):
    return sp.diff(e, x) + sp.diff(e, R) * dRdx


w1 = dx(w)
w2 = dx(w1)
w3 = dx(w2)
gam = 1 / (3 * t)
E1 = sp.simplify(w2 + 2 * (w - a * gam) * w1 - gam)
report("w_xx + 2(w - a/(3t)) w_x = 1/(3t)", E1 == 0)
G = (w3 + 2 * w1 ** 2 + 2 * w * w2) * (1 + 2 * a * w1) - 2 * a * w2 * (w2 + 2 * w * w1)
report("autonomous relation G(w,w_x,w_xx,w_xxx)=0 (t eliminated)", sp.simplify(G) == 0)

# 3. relation as a polynomial in the u-jet (y0..y4), constant coefficients (a = 1/4)
y = sp.symbols('y0:5')
W = [y[1] / y[0]]
for _ in range(3):
    e = W[-1]
    W.append(sp.together(sum(sp.diff(e, y[j]) * y[j + 1] for j in range(4))))
aa = sp.Rational(1, 4)
Gy = (W[3] + 2 * W[1] ** 2 + 2 * W[0] * W[2]) * (1 + 2 * aa * W[1]) - 2 * aa * W[2] * (W[2] + 2 * W[0] * W[1])
num = sp.factor(sp.numer(sp.together(Gy)))
pol = sp.Poly(sp.expand(sp.numer(sp.together(Gy))), *y)
print("INFO relation p(y0..y4) =", sp.factor(pol.as_expr()))
degs = sorted({sum(m) for m in pol.as_dict()})
print("INFO homogeneous degrees present:", degs, " total degree:", pol.total_degree())
report("relation has order 4 (y4 present)", pol.degree(y[4]) >= 1)

# numeric check of the relation on the explicit closed form at a few points (mpmath Airy)
mp.mp.dps = 40


def u_closed(tv, xv, av):
    tau_ = mp.cbrt(3 * tv)
    Zv = (xv + av ** 2 / (3 * tv)) / tau_
    return 2 * mp.pi / tau_ * mp.e ** (av * xv / (3 * tv) + 2 * av ** 3 / (27 * tv ** 2)) * mp.airyai(Zv)


def u_int(tv, xv, av):
    f = lambda k: mp.e ** (-av * k ** 2) * mp.cos(k * xv + k ** 3 * tv)
    return 2 * mp.quad(f, [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 14, 16, 18, 20, 24])


for (tv, xv) in [(mp.mpf('0.5'), mp.mpf('0.3')), (mp.mpf(1), mp.mpf(-2)), (mp.mpf('0.2'), mp.mpf(1))]:
    av = mp.mpf('0.25')
    d = abs(u_closed(tv, xv, av) - u_int(tv, xv, av))
    report("closed form = Fourier integral at t=%s x=%s" % (tv, xv), d < mp.mpf('1e-20'), "(diff %s)" % mp.nstr(d, 3))
    jet = [mp.diff(lambda s: u_closed(tv, s, av), xv, n) for n in range(5)]
    val = pol.as_expr().subs({y[i]: sp.Float(str(jet[i]), 40) for i in range(5)})
    scale = max(abs(j) for j in jet) ** max(degs)
    report("relation vanishes numerically at t=%s x=%s" % (tv, xv), abs(val) < 1e-15 * (1 + float(scale)),
           "(|p|=%s)" % sp.N(abs(val), 3))

# 4. lowest homogeneous component lies in I_PW (vanishes on jets of A cos(kappa x + theta)),
#    as predicted by the stationary-phase analogue of S4ID-P8
e0 = degs[0]
pe0 = sum(c * sp.prod([y[i] ** m[i] for i in range(5)]) for m, c in pol.as_dict().items() if sum(m) == e0)
Am, ka, th = sp.symbols('Am kappa theta', real=True)
pw = {y[j]: Am * ka ** j * sp.cos(th + j * sp.pi / 2) for j in range(5)}
report("lowest component p_e0 (degree %d) in I_PW" % e0, sp.simplify(sp.expand(pe0.subs(pw))) == 0)
cc = sp.Symbol('c')
aa0, bb0 = sp.symbols('alpha beta')
jetc = {}
for j in range(5):
    jetc[y[j]] = cc ** (j // 2) * (aa0 if j % 2 == 0 else bb0)
report("p_e0 vanishes on jets of all solutions of v''=cv", sp.expand(pe0.subs(jetc)) == 0)
print("INFO p_e0 =", sp.factor(pe0))

print("TOTAL %d/%d OK" % (ok, tot))
