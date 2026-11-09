# audit_p4.py — S-CHECK-6, red team / controlli su esempi per i claim di S-P4 (work/P4/CHECK_REQUEST.md)
# Eseguire con: D:\ProblemaBase\.venv\Scripts\python.exe -I audit_p4.py > audit_p4.out
# Sono verifiche su esempi (V-ex), non prove.
import itertools, sys
sys.stdout.reconfigure(encoding="utf-8")
import sympy as sp

t, x, tau, xi, z1, z2, n = sp.symbols('t x tau xi z1 z2 n')
RES = []


def check(name, ok):
    RES.append((name, bool(ok)))
    print(('OK   ' if ok else 'FAIL ') + name)


def monos(deg):
    return [(a, b) for a in range(deg + 1) for b in range(deg + 1 - a)]


def D(Q, u):
    """Q(d_t, d_x) u per Q polinomio in tau, xi."""
    Qp = sp.Poly(sp.expand(Q), tau, xi)
    return sp.expand(sum(c * sp.diff(u, t, a, x, b) for (a, b), c in Qp.terms()))


def ann_trunc(u, deg, zero_test):
    """Base di Ann(u) ∩ R_{<=deg}: risolve sum c_m d^m u == 0 con il test zero_test (lineare nei c)."""
    ms = monos(deg)
    cs = sp.symbols('c0:%d' % len(ms))
    expr = sum(c * sp.diff(u, t, a, x, b) for c, (a, b) in zip(cs, ms))
    eqs = zero_test(sp.expand(expr))
    sol = sp.solve(eqs, cs, dict=True)
    sol = sol[0] if sol else {}
    gen = [sp.expand(sum(c * tau**a * xi**b for c, (a, b) in zip(cs, ms)).subs(sol)) for _ in [0]][0]
    free = [c for c in cs if c not in sol]
    basis = [sp.expand(gen.subs({f: (1 if f == g else 0) for f in free})) for g in free]
    return basis


def coeff_eqs_exp(expr, exps):
    """expr = A(t,x) + sum_k B_k(t,x) e^{...}: equazioni = coefficienti dei polinomi davanti a ciascun esponenziale."""
    eqs = []
    rest = sp.expand(expr)
    for E in exps:
        part = sp.expand(rest).coeff(E)
        rest = sp.expand(rest - part * E)
        eqs += sp.Poly(sp.expand(part), t, x).coeffs()
    eqs += sp.Poly(sp.expand(rest), t, x).coeffs() if rest != 0 else []
    return eqs


# ---------------------------------------------------------------- P4-C2: u = t + e^{x^2}
E2 = sp.exp(x**2)
u = t + E2
B3 = ann_trunc(u, 3, lambda e: coeff_eqs_exp(e, [E2]))
idealC2 = [tau**2, tau * xi, tau**3, tau**2 * xi, tau * xi**2]
GB = sp.groebner([tau**2, tau * xi], tau, xi, order='grevlex')
check('C2a Ann(t+e^{x^2}) ∩ R_<=3 ha dimensione 5 = dim (tau^2, tau xi)_<=3', len(B3) == 5 and all(GB.reduce(b)[1] == 0 for b in B3))
# non spezzamento: d_t u = 1 ∈ W ∩ EP; nessun w' con d_t w' = 0 e u - w' costante (verifica della relazione usata)
check('C2b d_t u = 1 e d_t(1) = 0: 1 ∈ R·d_t u, u - c ha d_t = 1 ≠ 0 per ogni c', sp.diff(u, t) == 1 and sp.diff(u - 7, t) == 1)

# ---------------------------------------------------------------- Attacco KA-A: u = e^{x^2}, P = tau^2
uA = E2
BA = ann_trunc(uA, 3, lambda e: coeff_eqs_exp(e, [E2]))
GBt = sp.groebner([tau], tau, xi, order='grevlex')
check('KA-A Ann(e^{x^2}) ∩ R_<=3 = tau·R_<=2 (dim 6): Ann = (tau) principale, tau^2 ∈ Ann ma Ann ≠ (tau^2)',
      len(BA) == 6 and all(GBt.reduce(b)[1] == 0 for b in BA) and D(tau**2, uA) == 0 and D(tau, uA) == 0)

# ---------------------------------------------------------------- P4-T2 su EP: u = x e^{t+x} + e^{4t+2x}
e1, e2 = sp.exp(t + x), sp.exp(4 * t + 2 * x)
uE = x * e1 + e2
zt = lambda e: [sp.diff(e, t, a, x, b).subs({t: 0, x: 0}) for (a, b) in monos(8)]   # jet di ordine 8 ≥ 2d−1 (C3-T3)
BE = ann_trunc(uE, 2, zt)
check('T2a Ann(u) ∩ R_<=2 ha dimensione 3 (come in S-P4 C3h)', len(BE) == 3)
# C3-T2(a): Ann = ∩ {Q : Q(z_k+d) q_k = 0}
def in_ann_C3T2a(Q):
    a1 = D(Q.subs({tau: tau + 1, xi: xi + 1}), x)            # Q(z1 + d) q1, q1 = x
    a2 = D(Q.subs({tau: tau + 4, xi: xi + 2}), sp.Integer(1))  # Q(z2 + d) 1
    return a1 == 0 and a2 == 0
tests = [(tau - 1) * (xi - 2), (tau - 1) * (tau - 4), (xi - 1)**2 * (xi - 2), (xi - 1) * (xi - 2), tau - 3 * xi + 2,
         (tau - 1) * (xi - 1) * (tau - 4), xi - 1, (xi - 1) * (tau - 4)]
check('T2b C3-T2(a) su 8 polinomi: Q(d)u = 0 ⟺ Q(z_k+d)q_k = 0 ∀k', all((D(Q, uE) == 0) == in_ann_C3T2a(Q) for Q in tests))
# (v)(b) non radicale: costruzione corretta l(z1+d) q1 ≠ 0 con l = xi - 1, l_2 = tau - 4
Qnr = (xi - 1) * (tau - 4)
check('T2c Q = (xi-1)(tau-4) ∈ m_z1 ∩ m_z2 ma Q(d)u ≠ 0: I non radicale', D(Qnr, uE) != 0)
# lapsus l(d) vs l(z+d): l = tau - 1 soddisfa l(d)q1 = -x ≠ 0 ma l(z1+d)q1 = d_t x = 0 e (tau-1)(tau-4) ∈ I
check('T2d [fix T2-3] con la lettura letterale l(d)q_k la scelta l = tau-1 è ammessa ma Q = (tau-1)(tau-4) ∈ I',
      D(tau - 1, x) == -x and D(tau, x) == 0 and D((tau - 1) * (tau - 4), uE) == 0)
# radicale: u = e^{t+x} + e^{4t+2x}
uR = e1 + e2
check('T2e u a coefficienti costanti: Ann ⊇ m_z1 ∩ m_z2 (generatori (tau-1)(tau-4), (xi-1)(xi-2), tau-3xi+2)',
      all(D(Q, uR) == 0 for Q in [(tau - 1) * (tau - 4), (xi - 1) * (xi - 2), tau - 3 * xi + 2]))
# sigma_p: autovettori congiunti in W per u EP non radicale: e^{t+x} = (xi-1)(d) di x e^{t+x}; costruiamo w = ((xi-1)(tau-4))(d)u
w = sp.simplify(D(Qnr, uE))
check('T2f w = ((xi-1)(tau-4))(d)u è autovettore congiunto per z1 = (1,1)', sp.simplify(sp.diff(w, t) - w) == 0 and sp.simplify(sp.diff(w, x) - w) == 0 and w != 0)

# ---------------------------------------------------------------- (LS)+teorema cinese su J = (tau^2, xi(xi-1)), V(J) = {(0,0),(0,1)}
J0 = sp.groebner([tau**2, xi * (xi - 1), tau * xi, xi**2], tau, xi, order='grevlex')      # J + m_0^2
J1 = sp.groebner([tau**2, xi * (xi - 1), tau**2, tau * (xi - 1), (xi - 1)**2], tau, xi, order='grevlex')  # J + m_1^2
check('LS1 J + m_0^2 = (tau^2, xi), J + m_1^2 = (tau^2, xi-1)', J0.exprs == sp.groebner([tau**2, xi], tau, xi, order='grevlex').exprs and J1.exprs == sp.groebner([tau**2, xi - 1], tau, xi, order='grevlex').exprs)
check('LS2 socle: v = tau ≠ 0 in R/(J+m_0^2) e m_0·v = 0', J0.reduce(tau)[1] != 0 and J0.reduce(tau**2)[1] == 0 and J0.reduce(xi * tau)[1] == 0)
# immagine in R/J (componente z=0, zero altrove): v' = tau·(1 - xi) ≡ tau mod (J+m_0^2), ≡ 0 mod (J+m_1^2)
vp = sp.expand(tau * (1 - xi))
Jg = sp.groebner([tau**2, xi * (xi - 1)], tau, xi, order='grevlex')
check("LS3 v1 = tau(1-xi) ∉ J e tau·v1, xi·v1 ∈ J (autovettore congiunto per z = 0 in R/J)", Jg.reduce(vp)[1] != 0 and Jg.reduce(tau * vp)[1] == 0 and Jg.reduce(xi * vp)[1] == 0)

# ---------------------------------------------------------------- P4-T3: serie del jet per uE in p0 = 0
S = 1 / ((z1 - 1) * (z2 - 1)**2) + 1 / ((z1 - 4) * (z2 - 2))
# verifica dei coefficienti s_ab = d_t^a d_x^b u(0) contro la serie
ok = True
for a in range(4):
    for b in range(4):
        sab = sp.diff(uE, t, a, x, b).subs({t: 0, x: 0})
        ser = sp.series(sp.series(S.subs({z1: 1 / sp.Symbol('p'), z2: 1 / sp.Symbol('q')}), sp.Symbol('p'), 0, 6).removeO(), sp.Symbol('q'), 0, 6).removeO()
        coef = sp.expand(ser).coeff(sp.Symbol('p'), a + 1).coeff(sp.Symbol('q'), b + 1)
        ok = ok and sp.simplify(coef - sab) == 0
check('T3a S_u = 1/((z1-1)(z2-1)^2) + 1/((z1-4)(z2-2)) riproduce s_ab (a,b ≤ 3)', ok)
muA, muB = (z1 - 1) * (z1 - 4), (z2 - 1)**2 * (z2 - 2)
check('T3b mu_A mu_B S_u polinomio; con b = (z2-1)(z2-2) no', sp.denom(sp.cancel(muA * muB * S)) == 1 and sp.denom(sp.cancel(muA * (z2 - 1) * (z2 - 2) * S)) != 1)
GBel = sp.groebner([(tau - 1) * (tau - 4), (xi - 1)**2 * (xi - 2)], tau, xi, order='grevlex')
check('T3c (tau-1)(xi-2) ∈ Ann(u) ma ∉ ((tau-1)(tau-4), (xi-1)^2(xi-2))', D((tau - 1) * (xi - 2), uE) == 0 and GBel.reduce((tau - 1) * (xi - 2))[1] != 0)

# ---------------------------------------------------------------- P4-C3: I0(2 sqrt(tx))
N = 8
uI = sum((t * x)**k / sp.factorial(k)**2 for k in range(N + 1))
check('C3a s_ab = delta_ab per a,b ≤ 6', all(sp.diff(uI, t, a, x, b).subs({t: 0, x: 0}) == (1 if a == b else 0) for a in range(7) for b in range(7)))
res = sp.expand(sp.diff(uI, t, x) - uI)
check('C3b (d_t d_x - 1)u = O((tx)^N) (serie troncata)', sp.Poly(res, t, x).total_degree() >= 2 * N)
# nessuna eliminante a(tau) di grado ≤ 6: matrice di Hankel s_{k+i, b} ha nucleo nullo
Hm = sp.Matrix(7, 7, lambda b, k: 1 if k == b else 0)
check('C3c a(tau) ∈ Ann ⇒ a = 0 (deg ≤ 6): matrice (s_{k,b}) invertibile', Hm.rank() == 7)

# ---------------------------------------------------------------- P4-T5 Passo 2: P = (tau - xi^2)^2, K = 5, p0 = 0
P = (tau - xi**2)**2
K = 5
ms = monos(K)
def jet(fun):
    return sp.Matrix([sp.diff(fun, t, a, x, b).subs({t: 0, x: 0}) for (a, b) in ms])
gens_all, gens_top = [], []
for k in range(-6, 7):
    ez = sp.exp(k**2 * t + k * x)              # z = (k^2, k) ∈ V(tau - xi^2), grad P_1 = (1, -2k): eta = e1, s = t
    gens_all += [jet(ez), jet(t * ez)]
    gens_top += [jet(t * ez)]
VK = sp.Matrix.hstack(*gens_all)
VKtop = sp.Matrix.hstack(*gens_top)
dimPK = len(monos(K - 4))                        # (P) ∩ R_<=5 = P·R_<=1
check('T5a dim V_K = dim R_<=K - dim (P)∩R_<=K = 21 - 3 = 18', VK.rank() == len(ms) - dimPK)
# ortogonalita' di (P)∩R_<=K: <Q, J> = sum_alpha q_alpha J_alpha
def pairvec(Q):
    Qp = sp.Poly(sp.expand(Q), tau, xi)
    return sp.Matrix([[Qp.coeff_monomial(tau**a * xi**b) for (a, b) in ms]])
check('T5b P·{1,tau,xi} ⊥ V_K', all((pairvec(P * m) * VK).is_zero_matrix for m in [1, tau, xi]))
check('T5c (nota) con i soli generatori j = e_i - 1 lo span ha rango ' + str(VKtop.rank()) + ' (≤ 13 punti): i j < e_i servono',
      VKtop.rank() <= 13)
# jet di u = G (nucleo del calore non normalizzato) in (1,0) con K = 2: razionali, in V_K per P = tau - xi^2
G = sp.exp(-x**2 / (4 * t)) / sp.sqrt(t)
jG = [sp.diff(G, t, a, x, b).subs({t: 1, x: 0}) for (a, b) in monos(3)]
check('T5d jet di G = t^{-1/2}e^{-x^2/4t} in (1,0) razionali (u ammissibile in P4-T5, C8)', all(j.is_rational for j in jG))

# ---------------------------------------------------------------- P4-L3 / P4-L4: polinomi indiciali
# L = x d - 5: M_1 = xi, M_0 = -5; lambda = 0: iota(n) = n - 5 ⇒ N = 5, B = 6 ; soluzione x^5
L = lambda f: x * sp.diff(f, x) - 5 * f
check('L3a x d - 5: x^5 soluzione, iota(n) = n - 5, B = 6', L(x**5) == 0 and sp.solve(n - 5, n) == [5])
# L4 al punto x0 = 0: K0 = 5; h = x^5 ha derivate nulle fino a 4 ma non è nulla
check('L4a x^5 ha h^(k)(0) = 0 per k ≤ 4 = K0 - 1 e non è zero: la soglia K0 è necessaria', all(sp.diff(x**5, x, k).subs(x, 0) == 0 for k in range(5)))
# iota non nullo: falling factorials indipendenti
ff = [sp.expand(sp.ff(n, j)) for j in range(5)]
check('L3b fattoriali decrescenti n^(j), j ≤ 4, linearmente indipendenti', sp.Matrix([[sp.Poly(f, n).coeff_monomial(n**i) for i in range(5)] for f in ff]).rank() == 5)

# ---------------------------------------------------------------- P4-L6(b) + II-L1(b): onda P = tau^2 - xi^2, dati (x e^x, e^{2x}) in t0 = 0
C = sp.Matrix([[0, 1], [xi**2, 0]])            # compagna di tau^2 - xi^2
Fd = sp.Matrix([x * sp.exp(x), sp.exp(2 * x)])
# modo xi_1 = 1: Q_1 = (x, 0); modo xi_2 = 2: Q_2 = (0, 1); M_k = C(xi_k + d_x) su (C[x]_{<=1})^2
def Mop(xik, vec):  # applica C(xi_k + d_x) a un vettore di polinomi in x
    return sp.Matrix([vec[1], sp.expand((xik + 0) ** 2 * vec[0] + 2 * xik * sp.diff(vec[0], x) + sp.diff(vec[0], x, 2))])
def expM(xik, Q0, deg=12):
    # serie esponenziale in t (troncata ma esatta su polinomi: M nilpotente+scalare -> usiamo serie fino a deg e confronto simbolico via ODE)
    terms, cur = [Q0], Q0
    for k in range(1, deg):
        cur = Mop(xik, cur)
        terms.append(cur * t**k / sp.factorial(k))
    return sum(terms, sp.zeros(2, 1))
U = sp.exp(x) * expM(1, sp.Matrix([x, 0])) + sp.exp(2 * x) * expM(2, sp.Matrix([0, 1]))
E = U[0]
resid = sp.expand(sp.diff(E, t, 2) - sp.diff(E, x, 2))
# E è la serie troncata: verifichiamo P(d)E = O(t^{deg-2}) e i dati di Cauchy
check('L6a E(0,x) = x e^x, d_t E(0,x) = e^{2x} (costruzione con exp((t-t0)M_k))',
      sp.simplify(E.subs(t, 0) - x * sp.exp(x)) == 0 and sp.simplify(sp.diff(E, t).subs(t, 0) - sp.exp(2 * x)) == 0)
check('L6b P(d)E = 0 fino all ordine t^9 (troncamento)', all(sp.simplify(sp.diff(resid, t, k).subs(t, 0)) == 0 for k in range(9)))
# forma chiusa: soluzione d'Alembert
Ecl = (sp.Rational(1, 2) * ((x + t) * sp.exp(x + t) + (x - t) * sp.exp(x - t)) + (sp.exp(2 * (x + t)) - sp.exp(2 * (x - t))) / 4)
check('L6c forma chiusa (d Alembert) EP: P(d)Ecl = 0 e stessi dati', sp.simplify(sp.diff(Ecl, t, 2) - sp.diff(Ecl, x, 2)) == 0
      and sp.simplify(Ecl.subs(t, 0) - x * sp.exp(x)) == 0 and sp.simplify(sp.diff(Ecl, t).subs(t, 0) - sp.exp(2 * x)) == 0)
# II-L1(b) simbolico, m = 3, p_j(xi) generici di grado 2
f = sp.Function('f')(t, x)
a = sp.symbols('a0:9')
p = [a[3 * j] + a[3 * j + 1] * xi + a[3 * j + 2] * xi**2 for j in range(3)]
Pm = tau**3 + sum(p[j] * tau**j for j in range(3))
Uv = [f, sp.diff(f, t), sp.diff(f, t, 2)]
last = sp.diff(Uv[2], t) + sum(D(p[j], Uv[j]) for j in range(3))
check('II-L1(b) d_t U_3 + sum p_j(d_x) U_{j+1} = P(d) U_1 (m = 3, p_j generici)', sp.simplify(last - D(Pm, f)) == 0)

# ---------------------------------------------------------------- P4-L1: commutatori nell'algebra di Weyl
g = sp.Function('g')(x)
ok = True
for i in range(4):
    for j in range(4):
        op = lambda h: x**i * sp.diff(h, x, j)
        lhs1 = sp.diff(op(g), x) - op(sp.diff(g, x))                 # [d, x^i d^j]
        rhs1 = i * x**max(i - 1, 0) * sp.diff(g, x, j) if i > 0 else 0
        lhs2 = op(x * g) - x * op(g)                                  # [x^i d^j, x]
        rhs2 = j * x**i * sp.diff(g, x, j - 1) if j > 0 else 0
        ok = ok and sp.simplify(lhs1 - rhs1) == 0 and sp.simplify(lhs2 - rhs2) == 0
check('L1a [d, x^i d^j] = i x^{i-1} d^j, [x^i d^j, x] = j x^i d^{j-1} (i,j ≤ 3)', ok)
check('C1b (c0 + c1 d) su x e^x: c0 x + c1 (1+x) = 0 ⇒ c0 = c1 = 0', sp.solve(sp.Poly(sp.symbols('c0') * x + sp.symbols('c1') * (1 + x), x).coeffs(), sp.symbols('c0 c1')) == {sp.symbols('c0'): 0, sp.symbols('c1'): 0})

# ---------------------------------------------------------------- P4-T2(vi) e LEDGER: P = tau, risolvente di d_t su W per u = e^{x^2}
# W = C[d_x] e^{x^2}; d_t = 0 su W: d_t - tau0 biiettivo ⟺ tau0 ≠ 0 (risolvente C \ {0}, non "quasi vuoto")
check('T2g P = tau identificato da e^{x^2}: d_t ≡ 0 su W, quindi risolvente di d_t = C \\ {0} (il LEDGER omette la qualifica di (vi))',
      all(sp.diff(sp.diff(E2, x, k), t) == 0 for k in range(4)))

# ---------------------------------------------------------------- P4-C4(b): P = xi(tau-1), u = e^{t^2}
uB = sp.exp(t**2)
check('C4b P(d)e^{t^2} = 0, (tau-1)(d)u = (2t-1)e^{t^2}', D(xi * (tau - 1), uB) == 0 and sp.simplify(D(tau - 1, uB) - (2 * t - 1) * uB) == 0)

# ---------------------------------------------------------------- Lemma di esistenza (fix T5-2): P = tau^2, Q = tau, prima riga di M_Q nulla
# tau^l·tau mod tau^2 in base (1, tau): l=0 -> tau (coeff di 1 = 0), l=1 -> 0
check('T5e P = tau^2, Q = P/P_1 = tau: c^Q_{l0} = 0 per l = 0,1 (con f_0 sola i dati di Cauchy di Q(d)u sono nulli): serve una scelta generica dei dati',
      sp.rem(tau * 1, tau**2, tau).coeff(tau, 0) == 0 and sp.rem(tau * tau, tau**2, tau) == 0)

print('\nTOTALE:', sum(ok for _, ok in RES), '/', len(RES), 'OK')
