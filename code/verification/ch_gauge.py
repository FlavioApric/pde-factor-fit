"""F4-LIN ch_gauge.py -- Cole-Hopf as a gauge (flat connection) and transport of Ann(phi).
Checks (verification only, not a method):
 G1  omega_u = u dx + (nu u_x - u^2/2) dt closed  <=>  Burgers_nu[u] = 0
 G2  phi = exp(-psi/(2 nu)) with d psi = omega_u solves heat; D_x = d_x + g_x, D_t = d_t + g_t commute iff Burgers
 G3  B_Q[u] := phi^{-1} Q(d) phi = Q(D)1 is a differential polynomial in u; B_{tau - nu xi^2} = 0
 G4  1-front phi = 1 + e^{k x + nu k^2 t}: tau - nu k xi in Ann(phi);  u_t = nu k u_x for the front
 G5  jet transport: d^a phi / phi at a point = polynomial in the x-jet of u (u_t eliminated), orders
 G6  Burgers term flows in phi are NONLINEAR: phi_t = nu phi_x^2/phi (from -u u_x) and nu(phi_xx - phi_x^2/phi) (from nu u_xx on psi)
 G7  term flows in u vs psi: u_t = nu u_xx corresponds to psi_t = nu psi_xx; u_t = -u u_x to psi_t = -psi_x^2/2
 G8  sign-changing phi gives singular u: phi = sinh-type -> pole (positivity needed)
"""
import sympy as sp

t, x = sp.symbols('t x', real=True)
nu, k, c = sp.symbols('nu k c', positive=True)
res = []
def check(name, cond):
    res.append((name, bool(cond)))
    print(('[OK]  ' if cond else '[FAIL]') + ' ' + name)

u = sp.Function('u')(t, x)
burg = sp.diff(u, t) + u*sp.diff(u, x) - nu*sp.diff(u, x, 2)
# G1: d(omega) = d_t(u) - d_x(nu u_x - u^2/2)
curl = sp.diff(u, t) - sp.diff(nu*sp.diff(u, x) - u**2/2, x)
check('G1 curl(omega_u) == Burgers[u]', sp.simplify(curl - burg) == 0)

# G2: with g = -psi/(2nu): g_x = -u/(2nu), g_t = -(nu u_x - u^2/2)/(2nu)
gx = -u/(2*nu)
gt = -(nu*sp.diff(u, x) - u**2/2)/(2*nu)
# heat residual of phi divided by phi: g_t - nu (g_xx + g_x^2)
heat_over_phi = gt - nu*(sp.diff(gx, x) + gx**2)
check('G2a (phi_t - nu phi_xx)/phi == 0 identically given potential', sp.simplify(heat_over_phi) == 0)
# commutator [D_t, D_x] f = (d_t g_x - d_x g_t) f
comm = sp.diff(gx, t) - sp.diff(gt, x)
check('G2b [D_t,D_x] = -(1/2nu) Burgers[u]', sp.simplify(comm + burg/(2*nu)) == 0)

# G3: B_Q via operator D acting on 1; implement D as functions on expressions
def Dx(f): return sp.diff(f, x) + gx*f
def Dt(f): return sp.diff(f, t) + gt*f
one = sp.Integer(1)
BQ0 = Dt(one) - nu*Dx(Dx(one))
check('G3a B_{tau-nu xi^2}[u] == 0 identically', sp.simplify(BQ0) == 0)
BQ1 = Dx(Dx(Dx(one)))
print('     B_{xi^3}[u] =', sp.factor(sp.expand(BQ1)))
check('G3b B_{xi^3} is a differential polynomial in u (no exp)', not BQ1.has(sp.exp))

# G4: 1-front
phi1 = 1 + sp.exp(k*x + nu*k**2*t)
check('G4a heat(phi1)=0', sp.simplify(sp.diff(phi1, t) - nu*sp.diff(phi1, x, 2)) == 0)
check('G4b (d_t - nu k d_x) phi1 = 0', sp.simplify(sp.diff(phi1, t) - nu*k*sp.diff(phi1, x)) == 0)
u1 = -2*nu*sp.diff(phi1, x)/phi1
check('G4c u1 solves Burgers', sp.simplify(burg.subs(u, u1).doit()) == 0)
check('G4d u1_t = nu k u1_x (transported relation)', sp.simplify(sp.diff(u1, t) - nu*k*sp.diff(u1, x)) == 0)
# translated through B_Q: B_{tau - nu k xi}[u] = g_t - nu k g_x must vanish on u1
Bt = (gt - nu*k*gx).subs(u, u1).doit()
check('G4e B_{tau - nu k xi}[u1] == 0', sp.simplify(Bt) == 0)
# it is NOT a consequence of Burgers for generic u: B is first-order nonlinear expression
Bgen = sp.expand(gt - nu*k*gx)
print('     B_{tau-nu k xi}[u] =', Bgen, ' (Riccati-type x-relation: nu u_x = u^2/2 + nu k u)')

# G5: jet transport. Let x-jet symbols U0..U8 at a point; eliminate u_t via Burgers.
N = 8
U = sp.symbols('U0:%d' % (N+1))
def xder(expr):
    # derivative in x of a polynomial in U0..UN (U_i -> U_{i+1})
    return sum(sp.diff(expr, U[i])*U[i+1] for i in range(N))
def tder(expr):
    # u_t = nu u_xx - u u_x ; d_t U_i = d_x^i (nu U2 - U0 U1)
    ut = [None]*(N-1)
    base = nu*U[2] - U[0]*U[1]
    ut[0] = base
    for i in range(1, N-1):
        ut[i] = sp.expand(xder(ut[i-1]))
    return sp.expand(sum(sp.diff(expr, U[i])*ut[i] for i in range(N-1)))
# phi^{-1} d^a phi computed recursively: for phi = e^g, d(phi) /phi = d g + ..., use D operators on 1
GX = -U[0]/(2*nu)
GT = -(nu*U[1] - U[0]**2/2)/(2*nu)
def DX(f): return sp.expand(xder(f) + GX*f)
def DT(f): return sp.expand(tder(f) + GT*f)
orders_ok = True
for i in range(0, 3):
    for j in range(0, 4):
        f = one
        for _ in range(j): f = DX(f)
        for _ in range(i): f = DT(f)
        used = [m for m in range(N+1) if f.has(U[m])]
        mx = max(used) if used else -1
        expected = (2*i + j - 1) if (i + j) > 0 else -1
        if mx != expected:
            orders_ok = False
            print('     order mismatch', i, j, mx, expected)
check('G5 d_t^i d_x^j phi/phi uses x-jet of u up to order exactly 2i+j-1 (i<=2,j<=3)', orders_ok)

# G6: term flows in phi
phi = sp.Function('phi')(t, x)
psi = -2*nu*sp.log(phi)
uu = sp.diff(psi, x)
# psi-flow psi_t = -psi_x^2/2 corresponds to phi_t = nu phi_x^2/phi
lhs = sp.diff(psi, t) + sp.diff(psi, x)**2/2
cand = lhs.subs(sp.Derivative(phi, t), nu*sp.diff(phi, x)**2/phi)
check('G6a HJ term flow in phi: phi_t = nu phi_x^2/phi', sp.simplify(cand.doit()) == 0)
lhs2 = sp.diff(psi, t) - nu*sp.diff(psi, x, 2)
cand2 = lhs2.subs(sp.Derivative(phi, t), nu*(sp.diff(phi, x, 2) - sp.diff(phi, x)**2/phi))
check('G6b diffusive term flow in phi: phi_t = nu(phi_xx - phi_x^2/phi)', sp.simplify(cand2.doit()) == 0)
check('G6c the two phi-flows sum to the heat flow', sp.simplify(nu*sp.diff(phi, x)**2/phi + nu*(sp.diff(phi, x, 2) - sp.diff(phi, x)**2/phi) - nu*sp.diff(phi, x, 2)) == 0)
# neither phi-flow is linear: test superposition on two exponentials
e1 = sp.exp(x); e2 = sp.exp(2*x)
F = lambda f: nu*sp.diff(f, x)**2/f
check('G6d HJ phi-flow is not additive (F(e1+e2) != F(e1)+F(e2))', sp.simplify(F(e1+e2) - F(e1) - F(e2)) != 0)

# G7: u-flows correspond to psi-flows (differentiate)
psi_f = sp.Function('psi')(t, x)
check('G7 d_x of psi_t + psi_x^2/2 is u_t + u u_x with u = psi_x',
      sp.simplify(sp.diff(sp.diff(psi_f, t) + sp.diff(psi_f, x)**2/2, x) - (sp.diff(sp.diff(psi_f, x), t) + sp.diff(psi_f, x)*sp.diff(psi_f, x, 2))) == 0)

# G8: sign-changing heat solution -> singular Burgers
phis = sp.exp(k*x + nu*k**2*t) - sp.exp(-k*x + nu*k**2*t)
us = sp.simplify(-2*nu*sp.diff(phis, x)/phis)
check('G8 phi = 2 e^{nu k^2 t} sinh(kx) gives u = -2 nu k coth(kx) (pole at x=0)', sp.simplify(us + 2*nu*k*sp.cosh(k*x)/sp.sinh(k*x)) == 0)

print('\nSUMMARY: %d/%d OK' % (sum(r for _, r in res), len(res)))
