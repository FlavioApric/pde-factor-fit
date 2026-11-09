# S-CHECK-18: controlli indipendenti (non prove) per OP-F5B
import sympy as sp
from itertools import product
ok = []
def rep(name, cond):
    ok.append(bool(cond)); print(('[OK]  ' if cond else '[FAIL]') + ' ' + name)

t, x, z1, z2 = sp.symbols('t x z1 z2')
# 1. Leibniz: P(d)(theta w) = sum_alpha d^alpha theta/alpha! * P^{(alpha)}(d) w, P generico grado 3
th = sp.Function('th')(t, x); w = sp.Function('w')(t, x)
coeffs = sp.symbols('c0:10')
mons = [(i, j) for i in range(4) for j in range(4) if i + j <= 3]
Pz = sum(c * z1**i * z2**j for c, (i, j) in zip(coeffs, mons))
def applyP(poly, f):
    poly = sp.Poly(sp.expand(poly), z1, z2); r = 0
    for (i, j), c in poly.terms():
        r += c * sp.diff(f, t, i, x, j) if (i or j) else c * f
    return r
lhs = applyP(Pz, th * w)
rhs = 0
for a1 in range(4):
    for a2 in range(4 - a1):
        der = sp.diff(Pz, z1, a1, z2, a2)
        if der == 0: continue
        dth = sp.diff(th, t, a1, x, a2) if (a1 or a2) else th
        rhs += dth / (sp.factorial(a1) * sp.factorial(a2)) * applyP(der, w)
rep('Leibniz P(d)(theta w) per P generico di grado 3', sp.simplify(sp.expand(lhs - rhs)) == 0)

# 2. temperanza: |p^(alpha)(z+h)| <= Ptilde(z) * sum |h|^|b|/b!  (trave, campioni casuali)
import random, math
random.seed(18)
ze1, ze2 = sp.symbols('ze1 ze2', real=True)
p = (sp.I*ze1)**2 + (sp.I*ze2)**4
ders = [sp.diff(p, ze1, a, ze2, b) for a in range(3) for b in range(5)]
ders = [d for d in ders if d != 0]
fs = [sp.lambdify((ze1, ze2), d, 'math') for d in ders]
def Pt(a, b): return math.sqrt(sum(abs(complex(f(a, b)))**2 for f in fs))
worst = 0
for _ in range(2000):
    a, b = random.uniform(-50, 50), random.uniform(-50, 50)
    h1, h2 = random.uniform(-20, 20), random.uniform(-20, 20)
    worst = max(worst, Pt(a+h1, b+h2) / ((1+math.hypot(h1, h2))**4 * Pt(a, b)))
rep(f'P~ temperato (trave), max rapporto {worst:.3g} <= C=sum 1/b! finito', worst < 10)

# 3. azione destra su D/xD: implementazione indipendente (operatori su polinomi test)
#    verifica: per f = d^i T^k, f*P_r = (T f' - eta f - eta^2 f')|_{eta->d} modulo x D
#    controllo: applico a monomi x^n e confronto i termini senza x a sinistra -> uso Weyl normal ordering esplicito
X, D, T = sp.symbols('X D T', commutative=False)
def weyl_mul(A, B):
    # A,B dict {(a,i,k):c} per x^a d^i T^k ; prodotto con d^i x^b = sum C(i,l) b!/(b-l)! x^{b-l} d^{i-l}
    R = {}
    for (a, i, k), c in A.items():
        for (b, j, l), e in B.items():
            for s in range(0, min(i, b) + 1):
                coef = sp.binomial(i, s) * sp.factorial(b) / sp.factorial(b - s)
                key = (a + b - s, i - s + j, k + l)
                R[key] = R.get(key, 0) + c * e * coef
    return {k: v for k, v in R.items() if v != 0}
Pr = {(1, 0, 1): 1, (1, 2, 0): -1, (0, 1, 0): -1}   # x T - x d^2 - d
eta = sp.Symbol('eta'); TT = sp.Symbol('T')
good = True
for i in range(7):
    for k in range(3):
        prod_ = weyl_mul({(0, i, k): 1}, Pr)
        red = sum(c * eta**ii * TT**kk for (a, ii, kk), c in prod_.items() if a == 0)
        f = eta**i * TT**k
        pred = TT*sp.diff(f, eta) - eta*f - eta**2*sp.diff(f, eta)
        good &= sp.expand(red - pred) == 0
rep('azione destra su D/xD: f.P_r = T f\' - eta f - eta^2 f\' (i<=6,k<=2)', good)

# 4. u_G, modi J0, torsione in A_2
uG = sp.exp(-x**2/(4*t))/t
Prop = lambda u: x*sp.diff(u, t) - x*sp.diff(u, x, 2) - sp.diff(u, x)
rep('P_r u_G = 0', sp.simplify(Prop(uG)) == 0)
rep('(2t d_x + x) u_G = 0', sp.simplify(2*t*sp.diff(uG, x) + x*uG) == 0)
k = sp.Symbol('k', positive=True)
uk = sp.exp(-k**2*t)*sp.besselj(0, k*x)
rep('P_r u_k = 0 e (x d^2 + d + k^2 x) u_k = 0',
    sp.simplify(Prop(uk)) == 0 and sp.simplify(x*sp.diff(uk, x, 2) + sp.diff(uk, x) + k**2*x*uk) == 0)
# u_G non A_1-torsione: ordine<=4, grado<=4 coefficienti generici
s = sp.Symbol('s')
order, deg = 4, 4
cs = sp.symbols('b0:%d' % ((order+1)*(deg+1)))
g = sp.exp(-s*x**2/4)
expr = 0; idx = 0
for j in range(order+1):
    for d in range(deg+1):
        expr += cs[idx]*x**d*sp.diff(g, x, j); idx += 1
H = sp.expand(sp.simplify(expr/g))
eqs = sp.Poly(H, x, s).coeffs()
sol = sp.solve(eqs, cs, dict=True)
rep('u_G non di A_1-torsione (ordine<=4, grado<=4: solo b=0)', sol == [] or all(all(v == 0 for v in so.values()) and len(so) == len(cs) for so in sol))

# 5. P7(c): intrecciatore e u_lambda
lam = sp.Symbol('lam')
P1 = lambda u: sp.diff(u, t) - x*sp.diff(u, x)
P2 = lambda u: P1(u) + u
rep('P1 d_x = d_x P2 (su funzione generica)', sp.simplify(P1(sp.diff(w, x)) - sp.diff(P2(w), x)) == 0)
u1 = sp.exp(x*sp.exp(t)); u2 = sp.exp(-t)*sp.exp(-x*sp.exp(t)); us = u1 + u2
rep('P1P2 u* = 0', sp.simplify(P1(P2(us))) == 0)
Rl = lambda u: -(P1(u) + lam*sp.diff(P1(u), x))   # R_lam = -c^{-1}(1+lam J)P1, c=1
rep('R_lam u* = (1 + lam d_x) u*_2', sp.simplify(Rl(us) - (u2 + lam*sp.diff(u2, x))) == 0)
# E_lam corrisponde a moltiplicazione destra per R_lam: verifica P R_lam in D P (formale, su w)
#   P R_lam w deve annullarsi su ker P: test su u*
rep('P(R_lam u*) = 0', sp.simplify(P1(P2(Rl(us)))) == 0)

# 6. P8: Mellin di F(n.y) e indipendenza delle fibre (sigma=0: poli)
import numpy as np
beta = np.pi/2; al = [0.3, 0.8, 1.25]
phis = np.linspace(0, beta, 4001)
def gram(sig):
    E = np.array([np.cos(phis - a)**(-1 + 1j*sig) for a in al])
    W = np.trapezoid(E[:, None, :]*np.conj(E[None, :, :]), phis, axis=2)
    dg = np.sqrt(np.real(np.diag(W)))
    return W/np.outer(dg, dg)
mins = [np.linalg.eigvalsh(gram(sg)).min() for sg in np.linspace(-40, 40, 161)]
rep(f'P8 Gram normalizzata: min autovalore su |sigma|<=40 = {min(mins):.4g} > 0', min(mins) > 0)
print('TOTALE %d/%d' % (sum(ok), len(ok)))
