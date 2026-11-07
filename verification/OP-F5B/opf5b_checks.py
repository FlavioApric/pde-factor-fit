# OP-F5B — controlli SymPy/numerici (solo controllo, non prova). Eseguire con .venv python -I.
import sympy as sp, random, math, itertools
import numpy as np
OK = []
def check(name, cond):
    OK.append(bool(cond)); print(('[OK]  ' if cond else '[FAIL]') + ' ' + name)

t, x = sp.symbols('t x', real=True)
# ---------- A: OPF-Q3 / OPF5B-T1 (densità per P qualsiasi) ----------
th = sp.Function('theta')(t, x); w = sp.Function('w')(t, x)
tau, xi = sp.symbols('tau xi')
def Pop(f, Ppoly):
    poly = sp.Poly(sp.expand(Ppoly), tau, xi); out = 0
    for (a, b), c in poly.terms():
        out += c * sp.diff(f, t, a, x, b) if (a or b) else c * f
    return out
for name, Ppoly in [('trave tau^2+xi^4', tau**2 + xi**4), ('calore x trasporto (tau-xi^2)(tau+xi)', (tau - xi**2)*(tau + xi)),
                    ('onda tau^2-xi^2', tau**2 - xi**2)]:
    lhs = Pop(th*w, Ppoly) - th*Pop(w, Ppoly)
    rhs = 0
    for a in range(0, 5):
        for b in range(0, 5):
            if a == b == 0: continue
            Pab = sp.diff(Ppoly, tau, a, xi, b)
            if Pab == 0: continue
            rhs += sp.diff(th, t, a, x, b) / (sp.factorial(a)*sp.factorial(b)) * Pop(w, Pab)
    check(f'A1 Leibniz [P,theta]w = sum_(alpha!=0) d^alpha theta/alpha! P^(alpha)(D) w  ({name})', sp.simplify(sp.expand(lhs - rhs)) == 0)

# A2 temperanza di P~ (trave): P~(z+h) <= C (1+|h|)^4 P~(z), campionamento
def Ptilde(Ppoly, tv, xv):
    s = 0.0
    for a in range(0, 5):
        for b in range(0, 5):
            d = sp.diff(Ppoly, tau, a, xi, b)
            if d == 0: continue
            f = sp.lambdify((tau, xi), d, 'numpy')
            s += abs(complex(f(1j*tv, 1j*xv)))**2
    return math.sqrt(s)
random.seed(1); Pb = tau**2 + xi**4; worst = 0
for _ in range(400):
    z = (random.uniform(-50, 50), random.uniform(-50, 50)); h = (random.uniform(-20, 20), random.uniform(-20, 20))
    r = Ptilde(Pb, z[0]+h[0], z[1]+h[1]) / (Ptilde(Pb, *z) * (1 + math.hypot(*h))**4)
    worst = max(worst, r)
check(f'A2 temperanza P~ trave: max P~(z+h)/((1+|h|)^4 P~(z)) = {worst:.3f} (costante finita, Taylor dà C<=sum 1/beta!)', worst < 10)

# A3 geometria: parallelogramma {0<t<2, t<x<t+1}: y + eps(o-p) dista >= eps*rho/2 dal bordo per y in B(p,rho/2) ∩ chiusura
def dist_in(tv, xv, L=2.0):
    return min(tv, L - tv, (xv - tv)/math.sqrt(2), (tv + 1 - xv)/math.sqrt(2))
o = (1.0, 1.5); rho = dist_in(*o)
okg = True; random.seed(2)
for _ in range(20000):
    p = (random.uniform(0, 2), None);
    # punto di bordo casuale
    side = random.randrange(4); s = random.uniform(0, 1)
    if side == 0: p = (0.0, s)
    elif side == 1: p = (2.0, 2.0 + s)
    elif side == 2: tt = 2*s; p = (tt, tt)
    else: tt = 2*s; p = (tt, tt + 1)
    ang = random.uniform(0, 2*math.pi); rr = random.uniform(0, rho/2)
    y = (p[0] + rr*math.cos(ang), p[1] + rr*math.sin(ang))
    if dist_in(*y) < 0: continue  # fuori dalla chiusura
    eps = random.choice([0.5, 0.1, 0.01])
    yt = (y[0] + eps*(o[0]-p[0]), y[1] + eps*(o[1]-p[1]))
    if dist_in(*yt) < eps*rho/2 - 1e-12: okg = False
check(f'A3 traslazione locale verso o=(1,1.5) sul parallelogramma L=2: dist >= eps*rho/2 (rho={rho:.3f}), 20000 punti', okg)

# ---------- B: OPR2-Q2′ modello tangente (Mellin) ----------
beta = math.pi/2; alphas = [0.3, 0.8, 1.25]  # n_j = (cos a, sin a): n_j.omega = cos(phi - a) > 0 su [0, beta]
phis = np.linspace(0, beta, 4001)
def gram(a_exp):
    E = [np.cos(phis - al)**a_exp for al in alphas]
    G = np.array([[np.trapezoid(Ei*np.conj(Ej), phis) for Ej in E] for Ei in E])
    d = np.sqrt(np.real(np.diag(G))); return G/np.outer(d, d)
lmins = []; offs = []
for sg in np.linspace(-80, 80, 641):
    G = gram(-1 + 1j*sg); lmins.append(np.min(np.linalg.eigvalsh(G))); offs.append(np.max(np.abs(G - np.diag(np.diag(G)))) if abs(sg) > 60 else 0)
check(f'B1 cuneo: inf_sigma lambda_min(Gram normalizzata) = {min(lmins):.4f} > 0 su |sigma|<=80', min(lmins) > 1e-3)
check(f'B2 off-diagonali -> 0 (fase non stazionaria): max per |sigma|>60 = {max(offs):.4f}', max(offs) < 0.2)
check('B3 controllo di sanità: esponente a=1 (forme lineari) dà Gram singolare', np.min(np.linalg.eigvalsh(gram(1.0))) < 1e-10)
check('B4 esponente a=2 (potenze quadrate di 3 forme distinte) Gram non singolare', np.min(np.linalg.eigvalsh(gram(2.0))) > 1e-8)

# ---------- C: OPR2-Q3 classe M1⊕M2 con J (esempio OP-ALG-C1) ----------
lam = sp.symbols('lambda')
def P1(f): return sp.diff(f, t) - x*sp.diff(f, x)
def P2(f): return P1(f) + f
u1s = sp.exp(x*sp.exp(t)); u2s = sp.exp(-t)*sp.exp(-x*sp.exp(t)); us = u1s + u2s
check('C0 u* = u*_1+u*_2 risolve P = P1 P2', sp.simplify(P1(P2(us))) == 0)
Rl = -( (P1(us)) + lam*sp.diff(P1(us), x) )   # R_lambda u* = -(1+lam d_x) P1 u*
ul = u2s + lam*sp.diff(u2s, x)
check('C1 R_lambda u* = (1+lam d_x) u*_2 (endomorfismo E_lambda applicato a u*)', sp.simplify(Rl - ul) == 0)
check('C2 P u_lambda = 0', sp.simplify(P1(P2(ul))) == 0)
Ql = lambda f: P2(f) + lam*sp.diff(P1(f), x)
check('C3 Q_lambda u_lambda = 0 (Ann(u_lambda) != DP)', sp.simplify(Ql(ul)) == 0)
f = sp.Function('f')(t, x)
check('C4 intertwiner P1 d_x = d_x P2', sp.simplify(P1(sp.diff(f, x)) - sp.diff(P2(f), x)) == 0)
mu = sp.symbols('mu')
check('C5 Q_lambda u_mu = (mu-lambda) d_x u*_2', sp.simplify(Ql(u2s + mu*sp.diff(u2s, x)) - (mu - lam)*sp.diff(u2s, x)) == 0)

# ---------- D: EX-Q1 Bessel radiale ----------
def Pr(f): return x*sp.diff(f, t) - x*sp.diff(f, x, 2) - sp.diff(f, x)
uG = sp.exp(-x**2/(4*t))/t
check('D1 P_r u_G = 0, u_G = t^-1 exp(-x^2/4t)', sp.simplify(Pr(uG)) == 0)
check('D2 P_r = x * (d_t - d_x^2 - x^-1 d_x) (Phat monico in A_1[x^-1][d_t])', sp.simplify(Pr(f) - x*(sp.diff(f, t) - sp.diff(f, x, 2) - sp.diff(f, x)/x)) == 0)
# Weyl algebra: dict {(a,i,k): c} = x^a d^i T^k (T = d_t centrale)
def mul(A, B):
    out = {}
    for (a, i, k), c in A.items():
        for (b, j, l), e in B.items():
            for r in range(0, min(i, b) + 1):
                coef = c*e*sp.binomial(i, r)*sp.ff(b, r)
                key = (a + b - r, i - r + j, k + l); out[key] = out.get(key, 0) + coef
    return {kk: v for kk, v in out.items() if v != 0}
X = {(1, 0, 0): 1}; D = {(0, 1, 0): 1}; T = {(0, 0, 1): 1}
PrW = {}
for term in [mul(X, T), {kk: -v for kk, v in mul(mul(D, X), D).items()}]:
    for kk, v in term.items(): PrW[kk] = PrW.get(kk, 0) + v
eta, Ts = sp.symbols('eta T')
okD3 = True
for i in range(0, 7):
    for k in range(0, 3):
        prod = mul({(0, i, k): 1}, PrW)
        cls = sum(v*eta**ii*Ts**kk for (a, ii, kk), v in prod.items() if a == 0)
        fp = eta**i*Ts**k
        formula = Ts*sp.diff(fp, eta) - eta*fp - eta**2*sp.diff(fp, eta)
        if sp.expand(cls - formula) != 0: okD3 = False
check('D3 azione destra di P_r su D/xD = C[eta,T]: f -> T f\' - eta f - eta^2 f\' (eta^i T^k, i<=6, k<=2)', okD3)
# iniettività su polinomi di grado <= 8 in eta, <= 3 in T
cs = sp.symbols('c0:36'); fgen = sum(cs[9*k + i]*eta**i*Ts**k for i in range(9) for k in range(4))
img = sp.expand(Ts*sp.diff(fgen, eta) - eta*fgen - eta**2*sp.diff(fgen, eta))
eqs = sp.Poly(img, eta, Ts).coeffs()
sol = sp.solve(eqs, cs, dict=True)
check('D4 iniettività: f·P_r = 0 => f = 0 (grado <= 8 in eta, <= 3 in T)', sol == [] or all(all(v == 0 for v in s.values()) and len(s) == 36 for s in sol))
# u_G non di torsione su A_1: b = sum_{j<=3} beta_j(x) d_x^j, beta_j di grado <= 3
bs = sp.symbols('b0:16'); s_ = sp.symbols('s', positive=True)
g = sp.exp(-s_*x**2/4)
expr = sum(sum(bs[4*j + d]*x**d for d in range(4))*sp.diff(g, x, j) for j in range(4))
H = sp.expand(sp.simplify(expr/g))
eqsG = sp.Poly(H, x, s_).coeffs()
solG = sp.solve(eqsG, bs, dict=True)
check('D5 u_G non è di A_1-torsione (ordine <= 3, grado <= 3: solo b = 0)', all(all(v == 0 for v in s.values()) for s in solG))
uk = sp.exp(-4*t)*sp.besselj(0, 2*x)
check('D6 modo e^{-k^2 t}J_0(kx) (k=2) è di torsione: (x d^2 + d + k^2 x) u = 0', sp.simplify((x*sp.diff(uk, x, 2) + sp.diff(uk, x) + 4*x*uk).rewrite(sp.besselj)) == 0)
print(f'TOTALE {sum(OK)}/{len(OK)}')
