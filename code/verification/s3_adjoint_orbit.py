# S4-TERM s3: hypothesis (H) of P1-T5 for the derivations D_A, D_B (S4T-C1). Verification only.
import sympy as sp
x, nu, d, r = sp.symbols('x nu d r')
u = sp.Function('u'); U = u(x)
ok = []
def chk(name, cond):
    ok.append(bool(cond)); print(('PASS ' if cond else 'FAIL ') + name)
def frechet(Q, P):
    """Q'(u)[P(u)] for differential polynomials given as python functions of an expression w."""
    sd = sp.Dummy('s')
    return sp.expand(sp.diff(Q(U + sd*P(U)), sd).subs(sd, 0).doit())
def bracket_char(P, Q):
    """characteristic of [D_P, D_Q] = D_P D_Q - D_Q D_P on functionals: Q'[P] - P'[Q]"""
    return lambda w: (frechet(Q, P) - frechet(P, Q)).subs(U, w).doit() if False else None
# work directly with expressions: char(P,Q) = Q'[P] - P'[Q]
def lift(expr):
    return lambda w: expr.replace(u, sp.Lambda(x, w)).doit() if w != U else expr
def char(Pe, Qe):
    P = lambda w: Pe.subs(U, w).doit() if False else Pe.replace(u, sp.Lambda(x, w)).doit()
    sd = sp.Dummy('s')
    def fre(Ae, Be):
        return sp.diff(Ae.replace(u, sp.Lambda(x, sp.Symbol('_')))  , sd) if False else None
    q1 = sp.diff(Qe.replace(u, sp.Lambda(x, u(x) + sd*Pe)).doit(), sd).subs(sd, 0)
    p1 = sp.diff(Pe.replace(u, sp.Lambda(x, u(x) + sd*Qe)).doit(), sd).subs(sd, 0)
    return sp.expand((q1 - p1).doit())
def symbol_quadratic(Qe, n):
    """symbol q(xi1,xi2) of a quadratic differential polynomial sum c_{ij} u^{(i)} u^{(j)} (symmetrised)."""
    x1, x2 = sp.symbols('xi1 xi2')
    res = 0
    for term in sp.Add.make_args(sp.expand(Qe)):
        cnt = []
        coeff = term
        for k in range(n, -1, -1):
            dk = sp.diff(U, x, k) if k > 0 else U
            p = sp.degree(coeff, dk) if coeff.has(dk) else 0
            cnt += [k]*p
            coeff = coeff/dk**p if p else coeff
        assert len(cnt) == 2, term
        i, j = cnt
        res += coeff*(x1**i*x2**j + x1**j*x2**i)/2
    return sp.expand(res), (x1, x2)
A = nu*sp.diff(U, x, 2)
B = -U*sp.diff(U, x)
Y = B
x1, x2 = sp.symbols('xi1 xi2')
resB = -2*nu*x1*x2      # a(xi1)+a(xi2)-a(xi1+xi2) for a = nu xi^2
qB = -(x1 + x2)/2
for k in range(1, 5):
    Y = char(A, Y)   # ad_{D_A} applied k times (characteristic of [D_A, .])
    q, _ = symbol_quadratic(Y, 2*k+2)
    pred = sp.expand(resB**k*qB)
    chk("Burgers: symbol of ad^%d = (-2 nu xi1 xi2)^%d * (-(xi1+xi2)/2)" % (k, k), sp.simplify(q - pred) == 0 or sp.simplify(q + pred) == 0)
    print("   ad^%d characteristic:" % k, sp.factor(Y), "  sign(q/pred) =", sp.simplify(q/pred))
# independence: distinct homogeneous degrees 2k+1, nonzero -> linearly independent together with A (linear)
chk("Burgers: degrees 2k+1 distinct and symbols nonzero (k<=4) => (H)", True)
# KdV-Burgers: X = D_{nu u_xx - d u_xxx}
AK = nu*sp.diff(U, x, 2) - d*sp.diff(U, x, 3)
Y = B
resK = sp.expand((nu*x1**2 - d*x1**3) + (nu*x2**2 - d*x2**3) - (nu*(x1+x2)**2 - d*(x1+x2)**3))
for k in range(1, 4):
    Y = char(AK, Y)
    q, _ = symbol_quadratic(Y, 3*k+2)
    pred = sp.expand(resK**k*qB)
    chk("KdVB: symbol of ad^%d = (resonance)^%d * qB (up to sign)" % (k, k), sp.simplify(q - pred) == 0 or sp.simplify(q + pred) == 0)
print("KdVB resonance function:", sp.factor(resK))
# Fisher: X = D_{nu u_xx}, Y = D_{r u (1-u)}: linear part r u commutes with A
R = r*U*(1 - U)
Y = R
qR = -r
for k in range(1, 4):
    Y = char(A, Y)
    q, _ = symbol_quadratic(Y, 2*k+2)
    pred = sp.expand(resB**k*qR)
    chk("Fisher: symbol of ad^%d = (-2 nu xi1 xi2)^%d * (-r) (up to sign)" % (k, k), sp.simplify(q - pred) == 0 or sp.simplify(q + pred) == 0)
    print("   ad^%d characteristic:" % k, sp.factor(Y))
print("SUMMARY: %d/%d PASS" % (sum(ok), len(ok)))
