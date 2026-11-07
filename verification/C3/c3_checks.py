"""S-C3 · verifiche SymPy per work/C3/PROOF_PACKAGE.md.
Eseguire: D:\\ProblemaBase\\.venv\\Scripts\\python.exe -I c3_checks.py
Ogni check stampa [OK] o [FAIL]. La numerica (S1b) e' solo un CONTROLLO, non un metodo.
"""
import itertools
import sympy as sp

t, x, s = sp.symbols('t x s', real=True)
tau, xi = sp.symbols('tau xi')
results = []


def check(name, cond):
    results.append((name, bool(cond)))
    print(('[OK]   ' if cond else '[FAIL] ') + name)


def apply_op(Q, u):
    """Q(tau,xi) polinomio -> Q(d_t,d_x) u."""
    Q = sp.Poly(sp.expand(Q), tau, xi)
    out = 0
    for (a, b), c in Q.terms():
        out += c * sp.diff(u, t, a, x, b)
    return sp.simplify(out)


# ---------------- S1: [C3-C1] estensione periodica: spettro infinito, Ann 0-dim
k = sp.symbols('k', integer=True)
ck = sp.simplify(sp.integrate(sp.exp(s) * sp.exp(-sp.I * k * s), (s, -sp.pi, sp.pi)) / (2 * sp.pi))
ck_claim = sp.sinh(sp.pi) * (-1) ** k / (sp.pi * (1 - sp.I * k))
check('S1a c_k = sinh(pi)(-1)^k/(pi(1-ik)), mai nullo',
      all(sp.simplify((ck - ck_claim).subs(k, kk).rewrite(sp.exp)) == 0 for kk in range(-6, 7))
      and all(ck_claim.subs(k, kk) != 0 for kk in range(-6, 7)))
# controllo numerico (non metodo): somma parziale simmetrica in s0 = 0.5
import mpmath as mp
s0 = mp.mpf('0.5'); N = 4000
S = sum(mp.sinh(mp.pi) * (-1) ** kk / (mp.pi * (1 - 1j * kk)) * mp.e ** (1j * kk * s0) for kk in range(-N, N + 1))
check('S1b controllo: somma parziale (N=4000) ~ e^{0.5} (errore < 1e-3)', abs(S - mp.e ** s0) < 1e-3)
u1 = sp.exp(x - t)
check('S1c (tau+1),(xi-1) annullano e^{x-t}: Ann 0-dimensionale, contiene tau+xi',
      apply_op(tau + 1, u1) == 0 and apply_op(xi - 1, u1) == 0 and apply_op(tau + xi, u1) == 0)

# ---------------- S2: nucleo del calore non EP (orbita infinito-dimensionale)
G = t ** sp.Rational(-1, 2) * sp.exp(-x ** 2 / (4 * t))
check('S2a G risolve il calore', sp.simplify(sp.diff(G, t) - sp.diff(G, x, 2)) == 0)
ok = True
for kk in range(0, 11):
    r = sp.simplify(sp.diff(G, x, kk) / G)
    pr = sp.Poly(sp.expand(r), x)
    ok &= (pr.degree() == kk)
check('S2b d_x^k G / G polinomio in x di grado esatto k (k<=10) => {d_x^k G} lin. indip., G non EP', ok)

# ---------------- S3: P non ridotto: u = tG, P = (tau - xi^2)^2
P1 = tau - xi ** 2
u3 = t * G
check('S3a (d_t-d_x^2)(tG) = G != 0 e (d_t-d_x^2)^2 (tG) = 0',
      sp.simplify(apply_op(P1, u3) - G) == 0 and apply_op(sp.expand(P1 ** 2), u3) == 0)

# ---------------- S4: onda, f EP, g non EP => Ann(u) contiene (xi-1)(tau-xi) fuori da (P)
u4 = sp.exp(x - t) + sp.exp(-(x + t) ** 2)
P4 = sp.expand((tau - xi) * (tau + xi))
Q4 = sp.expand((xi - 1) * (tau - xi))
check('S4a u risolve l onda', apply_op(P4, u4) == 0)
check('S4b w_+ = (d_t+d_x)u = 2 g\'(x+t) non nullo; w_- = (d_t-d_x)u = -2e^{x-t} EP',
      sp.simplify(apply_op(tau + xi, u4) - 2 * sp.diff(sp.exp(-s ** 2), s).subs(s, x + t)) == 0
      and sp.simplify(apply_op(tau - xi, u4) + 2 * sp.exp(x - t)) == 0)
check('S4c Q=(xi-1)(tau-xi) annulla u e P non divide Q',
      apply_op(Q4, u4) == 0 and sp.rem(sp.Poly(Q4, tau), sp.Poly(P4, tau)) != 0)
# T1(d): relazione b0(d_x)u + b1(d_x)u_t = 0 con b1 = xi-1, b0 = -xi(xi-1)
b1 = xi - 1; b0 = -xi * (xi - 1)
rel = apply_op(b0, u4) + apply_op(b1 * tau, u4)
check('S4d relazione C[d_x]-lineare tra u e u_t (vettore ciclico = t-jet)', sp.simplify(rel) == 0)

# ---------------- S5: soglia di Bezout ottimale (calore)
ok_sharp = True; ok_thr = True
for n in (2, 3, 4):
    Z = [(j ** 2, j) for j in range(1, n + 1)] + [(j ** 2, -j) for j in range(1, n + 1)]
    u5 = sum(sp.exp(a * t + b * x) for a, b in Z)
    Qn = sp.prod([tau - j ** 2 for j in range(1, n + 1)])
    ok_sharp &= (apply_op(Qn, u5) == 0 and apply_op(P1, u5) == 0
                 and sp.rem(sp.Poly(sp.expand(Qn), xi), sp.Poly(P1, xi)) != 0 and len(Z) == n * 2)
    # con |Z| = 2n+1 > n deg P: annullatori di grado <= n = P * R_{<= n-2}
    Z2 = Z + [((n + 1) ** 2, n + 1)]
    mons = [(a, b) for a in range(n + 1) for b in range(n + 1 - a)]
    M = sp.Matrix([[za ** a * zb ** b for (a, b) in mons] for (za, zb) in Z2])
    dimker = len(mons) - M.rank()
    ok_thr &= (dimker == (n - 1) * n // 2)
check('S5a |Z| = n deg P: Q = prod(tau-j^2) annulla, P non divide Q (n=2,3,4): soglia ottimale', ok_sharp)
check('S5b |Z| = 2n+1 > n deg P: dim Ann_{<=n} = dim R_{<=n-2} (= multipli di P) per n=2,3,4', ok_thr)

# ---------------- S6: [C3-T3] jet di ordine n+d-1 determina Ann(u)_{<=n}
def ann_exact(modes, n):
    """modes: lista (z=(a,b), q(t,x)). Ann_{<=n} tramite Q(z+d)q = 0 (Lemma EP)."""
    mons = [(a, b) for a in range(n + 1) for b in range(n + 1 - a)]
    lam = sp.symbols('l0:%d' % len(mons))
    eqs = []
    for (za, zb), q in modes:
        expr = 0
        for c, (a, b) in zip(lam, mons):
            # (z+d)^alpha q = sum binom * z^.. d^.. q
            term = 0
            for i in range(a + 1):
                for j in range(b + 1):
                    term += sp.binomial(a, i) * sp.binomial(b, j) * za ** (a - i) * zb ** (b - j) * sp.diff(q, t, i, x, j)
            expr += c * term
        eqs += sp.Poly(sp.expand(expr), t, x).coeffs() if sp.expand(expr) != 0 else []
    A = sp.Matrix([[sp.diff(e, c) for c in lam] for e in eqs]) if eqs else sp.zeros(0, len(mons))
    return mons, A


def ann_jet(u, n, order):
    mons = [(a, b) for a in range(n + 1) for b in range(n + 1 - a)]
    rows = []
    for bt in range(order + 1):
        for bx in range(order + 1 - bt):
            rows.append([sp.diff(u, t, a + bt, x, b + bx).subs({t: 0, x: 0}) for (a, b) in mons])
    return mons, sp.Matrix(rows)


modes = [((1, 2), sp.Integer(1)), ((-1, 0), 1 + x), ((4, -1), sp.Integer(3))]
u6 = sum(q * sp.exp(a * t + b * x) for (a, b), q in modes)
d = 1 + 2 + 1  # dim R.u = somma delle dimensioni delle orbite
ok6 = True
for n in (1, 2, 3):
    mons, A = ann_exact(modes, n)
    _, J = ann_jet(u6, n, d - 1)
    ok6 &= (A.rank() == J.rank()) and all(sp.simplify(e) == 0 for e in (J * A.nullspace()[0])) if A.nullspace() else (A.rank() == J.rank())
    # stessi nuclei: rango di [A; J] = rango di A
    ok6 &= (A.col_join(J).rank() == A.rank())
check('S6a 2D: Ann_{<=n} esatto = Ann_{<=n} dal jet d\'ordine n+d-1 (d=4, n=1,2,3)', ok6)
# ottimalita' 1D: u = sum_{j=1}^d e^{jx}, n = d: jet d'ordine 2d-2 insufficiente, 2d-1 sufficiente
ok7 = True
for dd in (2, 3, 4):
    u7 = sum(sp.exp(j * x) for j in range(1, dd + 1))
    Hfull = sp.Matrix([[sp.diff(u7, x, a + b).subs(x, 0) for a in range(dd + 1)] for b in range(dd)])      # |beta|<=d-1
    Hshort = sp.Matrix([[sp.diff(u7, x, a + b).subs(x, 0) for a in range(dd + 1)] for b in range(dd - 1)])  # |beta|<=d-2
    ok7 &= (dd + 1 - Hfull.rank() == 1) and (dd + 1 - Hshort.rank() == 2)
check('S6b 1D (Prony): ordine 2d-1 identifica p_u, ordine 2d-2 no (d=2,3,4): soglia n+d-1 ottimale', ok7)

# ---------------- S7: [C3-T4] evoluzione u_t = a(d_x)u con dati EP: Lagrange
a = lambda z: z ** 2 + 3 * z
ok8 = True
for nmodes in (2, 3, 4):
    xs = list(range(1, nmodes + 1))
    n = 2
    bco = sp.symbols('b0:%d' % (n + 1))
    eqs = [sum(bco[i] * z ** i for i in range(n + 1)) - a(z) for z in xs]
    sol = sp.linsolve(eqs, bco)
    dim = len(list(sol)[0].free_symbols) if sol else -1
    ok8 &= (dim == max(0, n + 1 - nmodes))
check('S7 classe {tau-b(xi), deg b<=2}: dim soluzioni = max(0, 3 - #xi distinti)', ok8)

# ---------------- S8: [C3-L1] Gram su Omega=(0,1)^2: ker = Ann cap span
u8 = sp.exp(t + x) + sp.exp(4 * t + 2 * x)
feats = [sp.diff(u8, t), sp.diff(u8, x), sp.diff(u8, x, 2), u8]
Gm = sp.Matrix(4, 4, lambda i, j: sp.integrate(sp.integrate(feats[i] * feats[j], (t, 0, 1)), (x, 0, 1)))
check('S8 Gram (0,1)^2: dim ker = 2 = dim (Ann cap span{tau,xi,xi^2,1})', 4 - Gm.rank() == 2)

# ---------------- S9: [C3-P3] onde viaggianti di KG sono EP
c, mu = sp.symbols('c mu', positive=True)
f = sp.Function('f')
eq = apply_op(tau ** 2 - xi ** 2 + mu ** 2, f(x - c * t))
red = sp.simplify(eq.subs(x, s + c * t))
check('S9 KG su f(x-ct): (c^2-1) f\'\' + mu^2 f = 0 (ODE a coeff. costanti => f EP)',
      sp.simplify(red - ((c ** 2 - 1) * sp.diff(f(s), s, 2) + mu ** 2 * f(s))) == 0)

# ---------------- S10: [C3-T4(d)] evoluzione, dati EP con ampiezze polinomiali: Hermite
# calore a(xi)=xi^2; u = (x^2+2t) [z=0, delta=2] + e^{t+x} [z=(1,1), delta=0]: D = 3+1 = 4
u10 = (x ** 2 + 2 * t) + sp.exp(t + x)
ok10 = True
for n, expect_dim in ((2, 0), (3, 0), (4, 1), (5, 2)):
    bco = sp.symbols('b0:%d' % (n + 1))
    bpoly = sum(bco[i] * xi ** i for i in range(n + 1))
    # per L3(b) le due parti (modi z=0 e z=(1,1)) devono annullarsi separatamente
    partP = sp.expand(apply_op(tau - bpoly, x ** 2 + 2 * t))
    partE = sp.simplify(apply_op(tau - bpoly, sp.exp(t + x)) / sp.exp(t + x))
    eqs = (sp.Poly(partP, t, x).coeffs() if partP != 0 else []) + ([partE] if partE != 0 else [])
    sol = sp.linsolve(eqs, bco)
    sols = list(sol)
    dim = len(sols[0].free_symbols) if sols else -1
    # D = 4 >= n+1 sse n <= 3: unico; altrimenti dim n+1-D
    ok10 &= (dim == expect_dim)
check('S10 Hermite: dim {b, deg<=n : tau-b in Ann} = max(0, n+1-D), D = sum(delta_k+1) = 4', ok10)

# ---------------- S11: [C3-P3] G e' invariante di scala (annullatore a coeff. variabili) ma Ann_{C[d]}(G) = (tau - xi^2)
check('S11 (2t d_t + x d_x + 1) G = 0', sp.simplify(2 * t * sp.diff(G, t) + x * sp.diff(G, x) + G) == 0)

# ---------------- S12: [C3-P5] dati locali, trasporto: u = e^{x-t} + phi(x-t)
# phi liscia a supporto in (2,3): su Omega' con x-t in (-1,1) u = e^{x-t} (EP); su Omega grande u non EP.
phi = sp.Piecewise((sp.exp(-1 / ((s - 2) * (3 - s))), (s > 2) & (s < 3)), (0, True))
check('S12 phi(2.5) != 0 e phi = 0 su (-1,1): u|Omega\' = e^{x-t}, u|Omega != e^{x-t} su (2,3)',
      phi.subs(s, sp.Rational(5, 2)) != 0 and phi.subs(s, sp.Rational(1, 2)) == 0)

print('\nTOTALE: %d/%d OK' % (sum(r for _, r in results), len(results)))
