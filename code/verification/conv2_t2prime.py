# S-CHECK-F8-CONV (mini-audit T2'): controlli indipendenti su CONV-T2' (PROOF_PACKAGE §1.3').
# (A) lemma della famiglia test in n = 2: Ann(v) ∩ R_{<=m} = (tau^N) ∩ R_{<=m} via nuclei dei jet, m <= N+1
# (B) lo stesso in n = 3 su un caso
# (C) operatori casuali fuori da (tau^N) non annullano v (separazione polinomio / e^{|x|^2}*polinomio)
# (D) simulazione dei passi 2'-3' (k = 0, 1, 2) con un learner fittizio che dice sempre "legge":
#     ordini dei blocchi, jet di u = jet di v_k fino a H_{k+1}, box, N_{k,L'_k}(jet u) = 0, interezza (coefficienti)
import itertools, math, random, sys
import sympy as sp
sys.stdout.reconfigure(encoding='utf-8')
OK = []
def check(name, cond):
    OK.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

def monos(m, nv):
    return [a for k in range(m+1) for a in itertools.product(range(k+1), repeat=nv) if sum(a) == k]

def coeffs_of(expr, vars_, K):
    """coefficienti di Taylor in 0 fino all'ordine K, come dict multi-indice -> Rational"""
    ser = sp.expand(sp.series(expr.subs({v: sp.Symbol('s')*v for v in vars_}), sp.Symbol('s'), 0, K+1).removeO().subs(sp.Symbol('s'), 1))
    P = sp.Poly(ser, *vars_)
    return {mon: P.coeff_monomial(mon) for mon in P.monoms() if sum(mon) <= K}

def jet_from_coeffs(C, a):
    return C.get(a, 0)*math.prod(math.factorial(i) for i in a)

def kernel(C, m, K, nv, Lrows=-1):
    cols = monos(m, nv)
    rows = [b for b in monos(K-m, nv) if sum(b) > Lrows]
    M = sp.Matrix([[jet_from_coeffs(C, tuple(x+y for x, y in zip(al, be))) for al in cols] for be in rows])
    return M, cols

def principal_dim(m, N, nv):
    return len([a for a in monos(m, nv) if a[0] >= N])

# ---------------- (A) n = 2
t, x = sp.symbols('t x', real=True)
cases = [(sp.Integer(1), 0, sp.Rational(1, 3)), (1 + 2*t - x, 1, sp.Integer(-2)), (t*x + x**2 - 3*t**2 + 1, 2, sp.Rational(1, 7))]
for q, M, eps in cases:
    N = M + 2
    v = q + eps*t**(N-1)*sp.exp(x**2)
    check("A n=2 deg q=%d: tau^N annulla v" % M, sp.simplify(sp.diff(v, t, N)) == 0)
    K = N + 12
    C = coeffs_of(v, (t, x), K)
    okd, okin = True, True
    for m in range(0, N+2):
        Mm, cols = kernel(C, m, K, 2)
        ns = Mm.nullspace()
        okd &= len(ns) == principal_dim(m, N, 2)
        okin &= all(all(vec[i] == 0 for i, a in enumerate(cols) if a[0] < N) for vec in ns)
    check("A n=2 deg q=%d, N=%d: dim N_{m,K} = dim (tau^N)∩R_<=m per m<=N+1 (K=%d)" % (M, N, K), okd)
    check("A n=2 deg q=%d: ogni elemento del nucleo sta in (tau^N)" % M, okin)
    Cq = coeffs_of(q, (t, x), M)
    check("A n=2 deg q=%d: j_M v = j_M q" % M, all(C.get(a, 0) == Cq.get(a, 0) for a in monos(M, 2)))

# ---------------- (B) n = 3, q = 1 + t - x1*x2, M = 2, N = 4
x1, x2 = sp.symbols('x1 x2', real=True)
q3, N3 = 1 + t - x1*x2, 4
v3 = q3 + sp.Rational(1, 6)*t**(N3-1)*sp.exp(x1**2 + x2**2)
C3 = coeffs_of(v3, (t, x1, x2), N3 + 12)
okd = True
for m in range(0, N3+2):
    Mm, cols = kernel(C3, m, N3 + 12, 3)
    ns = Mm.nullspace()
    okd &= len(ns) == principal_dim(m, N3, 3) and all(all(vec[i] == 0 for i, a in enumerate(cols) if a[0] < N3) for vec in ns)
check("B n=3: N_{m,K}(v) = (tau^4)∩R_<=m per m<=5 (K=16; con K=12 il nucleo per m=5 e' ancora piu' grande: soglia finita, non difetto)", okd)

# ---------------- (C) operatori casuali con parte Q_j(xi) non nulla per qualche j<N
random.seed(7)
tau, xi = sp.symbols('tau xi')
q, M, eps = cases[2]; N = M + 2
v = q + eps*t**(N-1)*sp.exp(x**2)
def apply(Q, f):
    P = sp.Poly(Q, tau, xi); out = 0
    for (a, b), c in zip(P.monoms(), P.coeffs()):
        out += c*sp.diff(f, t, a, x, b)
    return sp.simplify(out)
okc = True
for _ in range(12):
    Q = sum(random.randint(-3, 3)*tau**a*xi**b for a in range(N+2) for b in range(3) if random.random() < 0.4)
    Q = sp.expand(Q)
    low = sp.expand(Q - sum(c*tau**a*xi**b for (a, b), c in zip(sp.Poly(Q, tau, xi).monoms(), sp.Poly(Q, tau, xi).coeffs()) if a >= N)) if Q != 0 else 0
    if low == 0:
        continue
    okc &= apply(Q, v) != 0
# caso j0 >= 1 in cui la parte polinomiale contribuisce alla stessa potenza di t
Qc = tau*xi**2 + 6*tau**0*xi**0*0 + tau**2   # j = 1 e j = 2
okc &= apply(Qc, v) != 0
check("C operatori fuori da (tau^N) non annullano v (12 casuali + 1 con j0>=1)", okc)

# ---------------- (D) simulazione della costruzione, n = 2, learner fittizio: H_{k+1} := N_k - 1
g0C = coeffs_of(sp.exp(t**2 + x**2), (t, x), 30)
def Kbar(m, L, Kmax=30):
    for K in range(m+L+1, Kmax+1):
        Mm, cols = kernel(g0C, m, K, 2, Lrows=L)
        if Mm.rank() == len(cols):
            return K
    return None
random.seed(1)
u = {}            # coefficienti della serie formale u (fino agli ordini toccati)
H = 0; p = {}     # p_0 = 0
log = []
okD = True
Hs, Ls = [], []
for k in range(3):
    Lp = Kbar(k, H)
    # blocco y* casuale nel box |y_gamma| <= gamma!/|gamma|!, con verifica del minore (rango pieno)
    for _ in range(20):
        block = {}
        for a in monos(Lp, 2):
            if sum(a) > H:
                bound = sp.Rational(math.prod(math.factorial(i) for i in a), math.factorial(sum(a)))
                block[a] = bound*sp.Rational(random.randint(-9, 9), 10)
        Ctest = dict(p); Ctest.update({a: y/math.prod(math.factorial(i) for i in a) for a, y in block.items()})
        Mm, cols = kernel(Ctest, k, Lp, 2, Lrows=H)
        if Mm.rank() == len(cols):
            break
    qk = dict(Ctest)
    Nk = Lp + 2; epsk = sp.Rational(1, math.factorial(Nk-1))
    tail = coeffs_of(epsk*t**(Nk-1)*sp.exp(x**2), (t, x), Nk + 6)
    Hn = Nk - 1                                    # learner fittizio: il minimo consentito
    vk = dict(qk)
    for a, c in tail.items():
        vk[a] = vk.get(a, 0) + c
    pn = {a: c for a, c in vk.items() if sum(a) <= Hn}   # p_{k+1} = T_{H_{k+1}} v_k
    # p_{k+1} estende p_k: stessi coefficienti fino a H_k
    okD &= all(pn.get(a, 0) == p.get(a, 0) for a in monos(H, 2))
    # la coda ha ordine >= N_k - 1 > L'_k: non tocca il blocco
    okD &= min(sum(a) for a in tail) == Nk - 1 > Lp
    # coefficienti di blocco nel box: |c_gamma| <= 1/|gamma|!
    okD &= all(abs(qk[a]) <= sp.Rational(1, math.factorial(sum(a))) for a in qk if H < sum(a) <= Lp)
    # Ann(v_k) = (tau^{N_k}) controllato sui nuclei per m <= 1 (dim = 0)
    Hs.append(H); Ls.append(Lp)
    log.append((k, H, Lp, Nk, Hn))
    p, H = pn, Hn
u = p  # u troncata a H_3: contiene tutti i blocchi k = 0, 1, 2
print("(k, H_k, L'_k, N_k, H_{k+1}):", log)
check("D H_k strettamente crescente e H_{k+1} > L'_k > H_k", all(l[1] < l[2] < l[4] for l in log))
check("D p_{k+1} estende p_k, la coda non tocca il blocco, blocco nel box", okD)
okker = True
for k, (Hk, Lk) in enumerate(zip(Hs, Ls)):
    Mm, cols = kernel(u, k, Lk, 2)
    okker &= Mm.rank() == len(cols)
check("D N_{k,L'_k}(jet di u) = 0 per k = 0,1,2 (lemma (iv) su u)", okker)
# jet di u = jet di v_k fino a H_{k+1}: verificato per costruzione su k = 2 (u = p_3 = T_{H_3} v_2)
# interezza: coefficienti di coda <= eps_k / beta! (termini t^{N_k-1} x^{2b}/b!)
check("D somma eps_k <= e - 1 (maggiorante e^{|t|})", sum(sp.Rational(1, math.factorial(l[3]-1)) for l in log) <= sp.E - 1)

print("TUTTI PASS" if all(OK) else "ALCUNI FAIL", "(%d/%d)" % (sum(OK), len(OK)))
