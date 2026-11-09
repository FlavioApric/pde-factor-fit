"""F4-LIN miura_darboux.py -- Miura as factorization of the Lax operator, Darboux = factor swap,
Crum/Wronskian components with pairwise (Vandermonde) interaction.
Conventions: KdV  u_t - 6 u u_x + u_xxx = 0 ;  mKdV v_t - 6 v^2 v_x + v_xxx = 0 ; L = -d^2 + u.
Checks:
 M1 (-d - v)(d - v) = -d^2 + (v^2 + v_x)   [Miura u = v^2 + v_x is a right-factor choice of L]
 M2 KdV[v^2 + v_x] = (2v + d) mKdV[v]  (Miura intertwining)
 M3 Darboux: (d - v)(-d - v) = -d^2 + (v^2 - v_x) = -d^2 + u - 2 v_x, v = psi_x/psi, L psi = 0
 M4 jet homomorphism u_k -> d^k(v^2 + v_x) injective: Jacobian wrt v_1..v_{K+1} triangular, full rank (K<=6)
 M5 kernel of (2v + d): w = C exp(-2 int v) = C / psi^2  (Miura not an equivalence)
 M6 Crum N=2: u = -2 d^2 log Wr(psi1,psi2), psi_j eigenfunctions of L0 = -d^2 (time: psi_t = -4 psi_xxx) solves KdV
 M7 Wronskian of exponentials = Vandermonde in the signed wavenumbers => interaction coefficient A_12 = ((k1-k2)/(k1+k2))^2 (cross-ratio)
 M8 N=3: all triple coefficients factor into pairwise ones (A_123 = A_12 A_13 A_23)
"""
import sympy as sp
from itertools import product

res = []
def check(name, cond):
    res.append((name, bool(cond)))
    print(('[OK]  ' if cond else '[FAIL]') + ' ' + name)

t, x = sp.symbols('t x', real=True)
v = sp.Function('v')(t, x)
f = sp.Function('f')(t, x)
d = lambda g: sp.diff(g, x)
lhs = -d(d(f) - v*f) - v*(d(f) - v*f)
check('M1 (-d - v)(d - v) = -d^2 + v^2 + v_x', sp.simplify(lhs - (-d(d(f)) + (v**2 + d(v))*f)) == 0)
u = v**2 + d(v)
kdv = lambda w: sp.diff(w, t) - 6*w*d(w) + sp.diff(w, x, 3)
mkdv = sp.diff(v, t) - 6*v**2*d(v) + sp.diff(v, x, 3)
check('M2 KdV[v^2+v_x] = (2v + d) mKdV[v]', sp.simplify(sp.expand(kdv(u) - (2*v*mkdv + d(mkdv)))) == 0)
lhs3 = d(-d(f) - v*f) - v*(-d(f) - v*f)
check('M3 (d - v)(-d - v) = -d^2 + v^2 - v_x = -d^2 + u - 2 v_x', sp.simplify(lhs3 - (-d(d(f)) + (v**2 - d(v))*f)) == 0)
psi = sp.Function('psi')(t, x)
vv = d(psi)/psi
check('M3b v = psi_x/psi  =>  (-d^2 + v^2 + v_x) psi = 0', sp.simplify(-sp.diff(psi, x, 2) + (vv**2 + d(vv))*psi) == 0)

K = 6
V = sp.symbols('V0:%d' % (K + 3))
def xd(e): return sum(sp.diff(e, V[i])*V[i+1] for i in range(K + 2))
Uk = [V[0]**2 + V[1]]
for k in range(K):
    Uk.append(sp.expand(xd(Uk[-1])))
J = sp.Matrix([[sp.diff(Uk[k], V[j]) for j in range(1, K + 2)] for k in range(K + 1)])
check('M4 Jacobian d(u_0..u_K)/d(v_1..v_{K+1}) is lower-triangular with unit diagonal (det = 1)', sp.simplify(J.det()) == 1)

C = sp.symbols('C')
w = C/psi**2
check('M5 (2v + d)(C/psi^2) = 0 with v = psi_x/psi', sp.simplify(2*vv*w + d(w)) == 0)

k1, k2, k3 = sp.symbols('k1 k2 k3', positive=True)
th = lambda k: k*x - 4*k**3*t
p1 = sp.cosh(th(k1)); p2 = sp.sinh(th(k2))
check('M6a psi_j: -psi_xx = -k^2 psi and psi_t = -4 psi_xxx',
      all(sp.simplify(sp.diff(p, t) + 4*sp.diff(p, x, 3)) == 0 and sp.simplify(sp.diff(p, x, 2) - kk**2*p) == 0 for p, kk in [(p1, k1), (p2, k2)]))
W2 = p1*d(p2) - d(p1)*p2
u2 = -2*sp.diff(sp.log(W2), x, 2)
val = kdv(u2).subs({k1: sp.Rational(1, 2), k2: sp.Rational(3, 2)})
num = [sp.N(val.subs({x: xv, t: tv})) for xv, tv in [(0.3, 0.1), (-1.2, 0.05), (2.0, -0.2)]]
check('M6b Crum 2-soliton solves KdV (exact expression, evaluated at 3 points, |res|<1e-10)', all(abs(n) < 1e-10 for n in num))

# M7/M8: Wronskian of signed exponentials e^{s_j k_j x}: coefficient = Vandermonde(s k)
ks = [k1, k2, k3]
def wr_coeffs(n):
    coeffs = {}
    for s in product([1, -1], repeat=n):
        lam = [si*ki for si, ki in zip(s, ks[:n])]
        M = sp.Matrix([[l**r for l in lam] for r in range(n)])
        coeffs[s] = sp.factor(M.det())
    return coeffs
c2 = wr_coeffs(2)
A12 = sp.simplify(c2[(1, 1)]*c2[(-1, -1)]/(c2[(1, -1)]*c2[(-1, 1)]))
print('     cross-ratio N=2 =', A12)
check('M7 cross-ratio of Wronskian coefficients = ((k1-k2)/(k1+k2))^2 = Hirota A_12',
      sp.simplify(A12 - ((k1 - k2)/(k1 + k2))**2) == 0)
c3 = wr_coeffs(3)
# normalized coefficient for subset S of "flipped" indices relative to all -1
def norm(s):
    return sp.simplify(c3[s]/c3[(-1, -1, -1)])
e = {i: norm(tuple(1 if j == i else -1 for j in range(3))) for i in range(3)}
pair = {}
for i in range(3):
    for j in range(i + 1, 3):
        s = tuple(1 if m in (i, j) else -1 for m in range(3))
        pair[(i, j)] = sp.simplify(norm(s)/(e[i]*e[j]))
trip = sp.simplify(norm((1, 1, 1))/(e[0]*e[1]*e[2]))
check('M8 N=3: triple interaction = product of pairwise (A_123 = A_12 A_13 A_23)',
      sp.simplify(trip - pair[(0, 1)]*pair[(0, 2)]*pair[(1, 2)]) == 0)
print('     pairwise:', {kk: sp.factor(vv_) for kk, vv_ in pair.items()})

print('\nSUMMARY: %d/%d OK' % (sum(r for _, r in res), len(res)))
