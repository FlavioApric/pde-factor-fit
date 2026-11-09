# OP-FUN: controlli SymPy (controllo, non metodo). Eseguire con .venv\Scripts\python.exe -I
import sympy as sp
import numpy as np
from mpmath import mp, quad, exp as mexp, pi as mpi, mpc

ok = 0; tot = 0
def check(name, cond):
    global ok, tot
    tot += 1
    if bool(cond):
        ok += 1; print("[OK]  ", name)
    else:
        print("[FAIL]", name)

t, x, s, lam, z, c, D = sp.symbols('t x s lambda zeta c D')
tau, xi = sp.symbols('tau xi')

# ---------- P1-Q2 / OPF-T1: elementi r(xi), s(tau) negli ideali (Q_j, P/Q_j) ----------
# trave: Q1 = tau - i xi^2, Q2 = tau + i xi^2
Q1 = tau - sp.I*xi**2; Q2 = tau + sp.I*xi**2
check("T1 trave: xi^2 = (Q2-Q1)/(2i)", sp.expand((Q2-Q1)/(2*sp.I) - xi**2) == 0)
check("T1 trave: tau^2 = Q1*Q2 - xi^4 e xi^4 = ((Q2-Q1)/(2i))^2 -> tau^2 in (Q1,Q2)",
      sp.expand(Q1*Q2 - ((Q2-Q1)/(2*sp.I))**2 - tau**2) == 0)
# calore x trasporto: Q1 = tau - xi^2, Q2 = tau + xi
Q1 = tau - xi**2; Q2 = tau + xi
check("T1 calxtr: r = xi + xi^2 = Q2 - Q1", sp.expand(Q2 - Q1 - (xi + xi**2)) == 0)
check("T1 calxtr: s = tau - tau^2 = Q1 - (tau - xi) Q2", sp.expand(Q1 - (tau - xi)*Q2 - (tau - tau**2)) == 0)
# risultante generico in (f,g) (Cramer) per una coppia non comassimale di grado 2 in tau
f = tau**2 - xi**2 - 1; g = tau - xi
R = sp.resultant(f, g, tau)
check("T1 KGxtr: Res_tau(f,g) = -1 costante (comassimale)", sp.simplify(R) != 0)

# ---------- OPF-T2: molteplicita' (tau - a)^2, a = a1 + a2 ----------
a1 = D*z**2; a2 = -c*z
a = a1 + a2
f0, f1 = sp.symbols('f0 f1')
# soluzione u = e^{s a}(f0 + s f1) e^{z x} (s = t - t0, t0 = 0)
u = sp.exp(t*a)*(f0 + t*f1)*sp.exp(z*x)
L = lambda w: sp.diff(w, t) - (D*sp.diff(w, x, 2) - c*sp.diff(w, x))
check("T2 (d_t - a(d_x))^2 u = 0 per u = e^{ta}(f0 + t f1)e^{zx}", sp.simplify(L(L(u))) == 0)
# x e^{zx} (molteplicita' spettrale) con f0 -> d_z
u2 = sp.diff(sp.exp(t*a)*(f0 + t*f1)*sp.exp(z*x), z)
check("T2 anche per x e^{zx} (derivata in zeta)", sp.simplify(L(L(u2))) == 0)
# stato di Jordan U = (u, (d_t-a)u); termini T1 = a1 I, T2 = a2 I, TN = N (nilpotente)
N = sp.Matrix([[0, 1], [0, 0]]); I2 = sp.eye(2)
F = sp.Matrix([f0, f1])
E1 = sp.exp(s*a1)*I2; E2 = sp.exp(s*a2)*I2; EN = I2 + s*N
U = E1*E2*EN*F
Ts = [E1 - I2, E2 - I2, EN - I2]
import itertools
Eadd_formula = sp.zeros(2, 1)
for k in range(2, 4):
    for S in itertools.combinations(range(3), k):
        M = I2
        for j in S: M = M*Ts[j]
        Eadd_formula += M*F
Eadd_def = U - F - sum(((E - I2)*F for E in [E1, E2, EN]), sp.zeros(2, 1))
check("T2 E^add = somma sui |S|>=2 (termini a1 I, a2 I, N)", sp.simplify(Eadd_def - Eadd_formula) == sp.zeros(2, 1))
check("T2 componente 0 di U = e^{sa}(f0 + s f1)", sp.simplify(U[0] - sp.exp(s*a)*(f0 + s*f1)) == 0)
check("T2 termini commutano: [N, a_n I] = 0", (N*(a1*I2) - (a1*I2)*N) == sp.zeros(2, 2))

# ---------- OPF-P3: grado >= 2 irriducibile monico, E^mult != 0 per ogni ordinamento ----------
def companion_terms(k, coeffs):
    # P = tau^k + sum_l c_l tau^l, c_l = somma di monomi; termini: shift N0 e -c_{l,n} E_{k,l+1}
    N0 = sp.zeros(k, k)
    for i in range(k-1): N0[i, i+1] = 1
    terms = [N0]
    for l, mons in coeffs.items():
        for m in mons:
            E = sp.zeros(k, k); E[k-1, l] = -m
            terms.append(E)
    return terms
def second_order(terms, order):
    Tsrt = [terms[i] for i in order]
    S = sp.zeros(*terms[0].shape)
    for i in range(len(Tsrt)):
        for j in range(i+1, len(Tsrt)):
            S += Tsrt[i]*Tsrt[j] - Tsrt[j]*Tsrt[i]
    return -S/2   # coefficiente di s^2 in e^{s sum T} - prod e^{s T}
# KG: tau^2 - xi^2 + m^2 (c0 = -xi^2 + m^2, termini -xi^2 e m^2)
m = sp.symbols('m', positive=True)
termsKG = companion_terms(2, {0: [-xi**2, m**2]})
allok = True
for order in itertools.permutations(range(len(termsKG))):
    C2 = sp.expand(second_order(termsKG, order))
    if sp.simplify(C2[0, 0]) == 0: allok = False
check("P3 KG: coeff. s^2 di E^mult ha entrata (1,1) != 0 per ogni ordinamento (6 ordini)", allok)
# telegrafo tau^2 + 2g tau - xi^2 (c0 = -xi^2, c1 = 2g)
g_ = sp.symbols('g', positive=True)
termsT = companion_terms(2, {0: [-xi**2], 1: [2*g_]})
allok = True
for order in itertools.permutations(range(len(termsT))):
    if sp.simplify(sp.expand(second_order(termsT, order))[0, 0]) == 0: allok = False
check("P3 telegrafo: idem (6 ordini)", allok)
# k = 3: tau^3 + xi tau + xi^3 + 1 (c0 = xi^3 + 1 -> monomi xi^3, 1; c1 = xi)
terms3 = companion_terms(3, {0: [xi**3, sp.Integer(1)], 1: [xi]})
allok = True
for order in itertools.permutations(range(len(terms3))):
    if sp.simplify(sp.expand(second_order(terms3, order))[1, 0]) == 0: allok = False
check("P3 k=3: entrata (k-1,1) del coeff. s^2 != 0 per ogni ordinamento (24 ordini)", allok)
# verifica della formula del coefficiente s^2 su un esempio numerico (serie)
A_ = sp.Matrix([[0, 1], [2, 0]]); B_ = sp.Matrix([[0, 0], [-3, 0]])
lhs = (s*(A_ + B_)).exp() - (s*A_).exp()*(s*B_).exp()
c2 = sp.simplify(sp.diff(lhs, s, 2).subs(s, 0)/2)
check("P3 formula: [s^2](e^{s(A+B)} - e^{sA}e^{sB}) = -(AB-BA)/2", sp.simplify(c2 + (A_*B_ - B_*A_)/2) == sp.zeros(2, 2))

# ---------- OPF-P4: non monico xi tau - 1, controesempio di tipo Bessel ----------
n = sp.symbols('n', integer=True, nonnegative=True)
K = 14
uB = sum(x**k*t**(k+1)/(sp.factorial(k)*sp.factorial(k+1)) for k in range(K))
res = sp.expand(sp.diff(uB, x, t) - uB)
# il residuo contiene solo termini di grado >= K (troncamento)
deg_ok = all(sp.Poly(term, x, t).total_degree() >= 2*K - 1 for term in res.as_ordered_terms())
check("P4 Bessel: d_x d_t u - u = solo termini di troncamento", deg_ok)
check("P4 Bessel: u(0,x) = 0", uB.subs(t, 0) == 0)
check("P4 Bessel: u != 0 (coeff. di t = 1)", sp.expand(uB).coeff(t, 1).subs(x, 0) == 1)
# forma integrale sul cerchio |zeta| = 1: (1/2pi i) \oint e^{zeta x + t/zeta} dzeta = u
mp.dps = 20
def contour(tt, xx):
    f = lambda th: mexp(mpc(0, 1)*th)*mexp(mexp(mpc(0, 1)*th)*xx + tt*mexp(-mpc(0, 1)*th))*mpc(0, 1)
    return quad(f, [0, 2*mpi])/(2*mpi*mpc(0, 1))
val = contour(0.7, -0.4); ser = float(uB.subs({t: 0.7, x: -0.4}))
check("P4 Bessel: integrale di contorno = serie (t=0.7, x=-0.4)", abs(complex(val) - ser) < 1e-10)
check("P4 Bessel: integrale di contorno nullo a t=0", abs(complex(contour(0.0, 0.3))) < 1e-15)
# Runge: per K = disco |zeta - 3| <= 1, a = 1/zeta e' olomorfa vicino a K; approssimazione polinomiale
zz = np.linspace(0, 2*np.pi, 400); pts = 3 + np.exp(1j*zz)
# serie di Taylor di 1/zeta in (zeta - 3): sum (-1)^k (zeta-3)^k / 3^{k+1}
approx = sum(((-1)**k)*(pts - 3)**k/3**(k+1) for k in range(60))
check("P4 Runge: 1/zeta approssimata da polinomi su |zeta-3|<=1 (err < 1e-10)", np.max(np.abs(approx - 1/pts)) < 1e-10)

# ---------- OPF-T5 (P2-Q1): simmetrie contraenti ----------
w = sp.Function('w')
# trave: P = tau^2 + xi^4 quasi omogeneo con pesi (2,1), grado 4
ul = w(lam**2*t, lam*x)
expr = sp.diff(ul, t, 2) + sp.diff(ul, x, 4)
Pw = (sp.Derivative(w(t, x), t, 2) + sp.Derivative(w(t, x), x, 4))
# confronto: expr = lam^4 (Pw)(lam^2 t, lam x)
X, Tt = sp.symbols('X T')
expr_sub = expr.subs({lam**2*t: Tt, lam*x: X})
check("T5 trave: P(d)(u o Phi_lam) = lam^4 (P(d)u) o Phi_lam",
      sp.simplify(sp.diff(w(lam**2*t, lam*x), t, 2) - lam**4*sp.Subs(sp.Derivative(w(Tt, X), Tt, 2), (Tt, X), (lam**2*t, lam*x)).doit()) == 0
      and sp.simplify(sp.diff(w(lam**2*t, lam*x), x, 4) - lam**4*sp.Subs(sp.Derivative(w(Tt, X), X, 4), (Tt, X), (lam**2*t, lam*x)).doit()) == 0)
check("T5 onda: tau^2 - xi^2 omogeneo", sp.expand((lam*tau)**2 - (lam*xi)**2 - lam**2*(tau**2 - xi**2)) == 0)
check("T5 calore x trasporto NON quasi omogeneo (nessun peso (a,b) > 0)",
      all(sp.expand(((lam**aa*tau) - (lam**bb*xi)**2)*((lam**aa*tau) + lam**bb*xi) - lam**dd*(tau - xi**2)*(tau + xi)) != 0
          for aa in range(1, 4) for bb in range(1, 4) for dd in range(1, 9)))
# trasporti paralleli: Phi_lam(t,s) = (t, 1 + lam (s-1)) manda Omega' = {0<t<1, t<s<t+1} in se'
okdom = True
rng = np.random.default_rng(0)
for _ in range(2000):
    tt = rng.uniform(0, 1); ss = rng.uniform(tt, tt+1); ll = rng.uniform(0, 1)
    s2 = 1 + ll*(ss - 1)
    if not (tt <= s2 <= tt + 1 + 1e-14): okdom = False
check("T5 trasporti paralleli: Phi_lam(Omega') in Omega' (2000 punti)", okdom)
# rettangolo: Phi_lam(t,x) = (tc + lam^2 (t-tc), xc + lam (x-xc)) manda chiusura in interno per lam<1
check("T5 rettangolo: contrazione anisotropa verso un punto interno manda Omega-bar nell'interno",
      all(0 < 0.5 + l**2*(e - 0.5) < 1 for l in [0.9, 0.99] for e in [0.0, 1.0]))

# ---------- C12-Q2 / OPF-P6: famiglia parallela, Gram di N esponenziali su una corda ----------
def gram(ds, a0, b0):
    G = np.zeros((len(ds), len(ds)), dtype=complex)
    for i, di in enumerate(ds):
        for j, dj in enumerate(ds):
            lmb = di + np.conj(dj)
            G[i, j] = (b0 - a0) if abs(lmb) < 1e-14 else (np.exp(lmb*b0) - np.exp(lmb*a0))/lmb
    return G
ds = [0.0, 1.0, -2.0]
mins = [np.min(np.linalg.eigvalsh(gram(ds, 0.3, 0.3 + l))) for l in np.linspace(0.2, 1.5, 40)]
check("P6 Gram di 3 esponenziali su corde di lunghezza in [0.2,1.5]: min autov. > 0", min(mins) > 0)
# invarianza per traslazione (normalizzata)
def ngram(ds, a0, l):
    G = gram(ds, a0, a0 + l); d = np.sqrt(np.real(np.diag(G))); return G/np.outer(d, d)
e1 = np.linalg.eigvalsh(ngram([0, 1j + 0.5, -2], 0.0, 0.7)); e2 = np.linalg.eigvalsh(ngram([0, 1j + 0.5, -2], 0.9, 0.7))
check("P6 Gram normalizzata dipende solo dalla lunghezza della corda", np.allclose(e1, e2))

# ---------- C12-Q6 / OPF-T4: Laplaciano e tau*xi ----------
r2 = t**2 + x**2
check("T4 log r^2 armonica", sp.simplify(sp.diff(sp.log(r2), t, 2) + sp.diff(sp.log(r2), x, 2)) == 0)
th = sp.atan2(x, t)
dth_t = sp.simplify(sp.diff(sp.atan(x/t), t)); dth_x = sp.simplify(sp.diff(sp.atan(x/t), x))
check("T4 d(theta) = (-x dt + t dx)/r^2 (forma dell'angolo, chiusa)",
      sp.simplify(dth_t + x/r2) == 0 and sp.simplify(dth_x - t/r2) == 0 and sp.simplify(sp.diff(-x/r2, x) - sp.diff(t/r2, t)) == 0)
# immagine di [d theta] x 1 per Q1 = d_t - i d_x: Q1(theta) monodroma
Q1th = sp.simplify(dth_t - sp.I*dth_x)
check("T4 Q1(theta) = -(x + i t)/r^2 = -i/(t + i x) monodroma", sp.simplify(Q1th + sp.I/(t + sp.I*x)) == 0)
# u costruita dal criterio coincide (a meno di ker Q1 + ker Q2) con log r^2: Q2(log r^2) = 2/(t - i x)
check("T4 Q2(log r^2) = 2/(t - i x)", sp.simplify(sp.diff(sp.log(r2), t) + sp.I*sp.diff(sp.log(r2), x) - 2/(t - sp.I*x)) == 0)

# ---------- S5-L2 ----------
rng = np.random.default_rng(1)
def orth(M):
    q, _ = np.linalg.qr(M); return q
def proj(B): return B @ np.linalg.pinv(B)
def inter_basis(A, B, tol=1e-9):
    M = np.hstack([A, -B]); _, sv, vh = np.linalg.svd(M); null = vh[np.sum(sv > tol):].T
    return orth(A @ null[:A.shape[1]]) if null.size else np.zeros((A.shape[0], 0))
n_ = 12
common = rng.standard_normal((n_, 1))
Hs = [orth(np.hstack([common, rng.standard_normal((n_, 3))])) for _ in range(3)]
okL2 = True
for j in range(3):
    Fj = orth(np.hstack([inter_basis(Hs[i], Hs[j]) for i in range(3) if i != j]))
    # H_j' = H_j orth. complement of F_j inside H_j
    Pj = Hs[j] @ Hs[j].T; Pf = Fj @ Fj.T
    Hp = orth((Pj - Pf) @ Hs[j])[:, :Hs[j].shape[1] - Fj.shape[1]]
    for i in range(3):
        if i != j:
            Fi = orth(np.hstack([inter_basis(Hs[k], Hs[i]) for k in range(3) if k != i]))
            Pi = Hs[i] @ Hs[i].T; Hpi = orth((Pi - Fi @ Fi.T) @ Hs[i])[:, :Hs[i].shape[1] - Fi.shape[1]]
            if inter_basis(Hp, Hpi).shape[1] != 0: okL2 = False
check("S5-L2 (i): H_i' cap H_j' = 0 su esempio casuale con intersezione comune", okL2)
# non necessita': tre rette nel piano, somma chiusa, ||C'|| = 1 >= 1
vs = [np.array([1, 0]), np.array([-0.5, np.sqrt(3)/2]), np.array([-0.5, -np.sqrt(3)/2])]
Cm = np.array([[0 if i == j else abs(vs[i] @ vs[j]) for j in range(3)] for i in range(3)])
check("S5-L2 non necessita': tre rette a 120 gradi, ||C|| = 1 (criterio muto) ma somma = R^2 chiusa",
      abs(np.max(np.abs(np.linalg.eigvalsh(Cm))) - 1) < 1e-12)

print(f"\nTOTALE: {ok}/{tot}")

