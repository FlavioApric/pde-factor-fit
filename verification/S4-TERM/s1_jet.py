# S4-TERM s1: Lie-series jets of E^add, E^mult (S4T-T1). Verification only.
import sympy as sp
x, t, nu, eps, d, r, s = sp.symbols('x t nu epsilon d r s')
u = sp.Function('u')
U = u(x)
ok = []
def chk(name, cond):
    ok.append((name, bool(cond))); print(('PASS ' if cond else 'FAIL ') + name)

def D(F, G):
    """Lie derivative of functional G along vector field F: (D_F G)(w) = d/ds G(w + s F(w)) at s=0."""
    def H(w):
        sd = sp.Dummy('s')
        return sp.diff(G(w + sd*F(w)), sd).subs(sd, 0).doit()
    return H
idf = lambda w: w
def Dpow(F, k, G=idf):
    for _ in range(k):
        G = D(F, G)
    return G
def jet_add(Fs, k):
    Ftot = lambda w: sum(F(w) for F in Fs)
    e = Dpow(Ftot, k)(U) - sum(Dpow(F, k)(U) for F in Fs)
    return sp.expand(e/sp.factorial(k))
def jet_mult(F1, F2, k):
    # S_1(t) o S_2(t): f(S1 S2 u) = e^{tD_2} e^{tD_1} f ; coefficient of t^k
    Ftot = lambda w: F1(w) + F2(w)
    full = Dpow(Ftot, k)(U)/sp.factorial(k)
    prod = 0
    for i in range(k+1):
        j = k - i
        prod += Dpow(F2, i, Dpow(F1, j))(U)/(sp.factorial(i)*sp.factorial(j))
    return sp.expand(full - prod)

A = lambda w: nu*sp.diff(w, x, 2)
B = lambda w: -w*sp.diff(w, x)
u1, u2, u3, u4, u5 = [sp.diff(U, x, k) for k in range(1, 6)]
# --- Burgers t^2
e2 = jet_add([A, B], 2)
chk("Burgers E^add_2 = -nu(2u'u''+u u''')", sp.simplify(e2 + nu*(2*u1*u2 + U*u3)) == 0)
m2AB = jet_mult(A, B, 2)   # S - S_A S_B
m2BA = jet_mult(B, A, 2)   # S - S_B S_A
chk("Burgers E^mult_AB_2 = nu u'u''", sp.simplify(m2AB - nu*u1*u2) == 0)
chk("Burgers E^mult_BA_2 = -nu u'u''", sp.simplify(m2BA + nu*u1*u2) == 0)
# anticommutator form: (1/2)(A'B + B'A)
Bp_A = sp.diff(B(U + s*A(U)), s).subs(s, 0).doit()
Ap_B = A(B(U))
chk("E^add_2 = (1/2)(A'B+B'A)", sp.simplify(e2 - (Ap_B + Bp_A)/2) == 0)
chk("E^mult_AB_2 = (1/2)(B'A - A'B)", sp.simplify(m2AB - (Bp_A - Ap_B)/2) == 0)
# first orders vanish
chk("E^add_1 = 0", sp.simplify(jet_add([A, B], 1)) == 0)
chk("E^mult_AB_1 = 0", sp.simplify(jet_mult(A, B, 1)) == 0)
# DEVIL-4 reference: u0 = eps sin x -> (3/2) nu eps^2 sin 2x
val = e2.subs(U, eps*sp.sin(x)).doit() if False else sp.simplify(e2.replace(u, sp.Lambda(x, eps*sp.sin(x))).doit())
chk("u0=eps sin x: E^add_2 = (3/2)nu eps^2 sin2x", sp.simplify(val - sp.Rational(3, 2)*nu*eps**2*sp.sin(2*x)) == 0)
# --- t^3 and homogeneity (degree in u, power of nu)
e3 = jet_add([A, B], 3)
lam = sp.symbols('lam')
e3s = sp.expand(e3.replace(u, sp.Lambda(x, lam*u(x))).doit())
poly = sp.Poly(e3s, lam, nu)
degs = sorted(poly.monoms())
print("E^add_3 monomials (deg_u, deg_nu):", degs)
chk("E^add_3 only (deg_u,deg_nu) in {(3,1),(2,2)} (words a+b=3, a,b>=1)", set(degs) <= {(3, 1), (2, 2)})
e4 = jet_add([A, B], 4)
e4s = sp.expand(e4.replace(u, sp.Lambda(x, lam*u(x))).doit())
degs4 = set(sp.Poly(e4s, lam, nu).monoms())
print("E^add_4 monomials:", sorted(degs4))
chk("E^add_4 only deg_u=b+1, deg_nu=a, a+b=4, a,b>=1", degs4 <= {(4, 1), (3, 2), (2, 3)})
print("E^add_3 =", sp.factor(e3))
print("number of monomials in E^add_k (k=2,3,4):", [len(sp.Add.make_args(jet_add([A,B],k))) for k in (2,3,4)])
# --- KdV-Burgers: three terms A, C=-d u_xxx, B
C = lambda w: -d*sp.diff(w, x, 3)
e2kb = jet_add([A, C, B], 2)
pred = -nu*(2*u1*u2 + U*u3) - nu*d*u5 + d*(2*U*u4 + 5*u1*u3 + 3*u2**2)/2
chk("KdVB E^add_2 formula", sp.simplify(e2kb - pred) == 0)
valkb = sp.simplify(e2kb.replace(u, sp.Lambda(x, eps*sp.sin(x))).doit())
print("KdVB E^add_2 at eps sin x:", sp.simplify(sp.expand_trig(valkb)))
# --- Fisher-KPP: A and R = r u (1-u)
R = lambda w: r*w*(1 - w)
e2f = jet_add([A, R], 2)
chk("Fisher E^add_2 = r nu (u'' - u'^2 - 2 u u'')", sp.simplify(e2f - r*nu*(u2 - u1**2 - 2*U*u2)) == 0)
m2f = jet_mult(A, R, 2)
print("Fisher E^mult_AR_2 =", sp.factor(m2f))
chk("Fisher E^mult_AR_2 = r nu u'^2", sp.simplify(m2f - r*nu*u1**2) == 0)
print("SUMMARY: %d/%d PASS" % (sum(o for _, o in ok), len(ok)))
