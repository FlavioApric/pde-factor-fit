# AUDIT del TRIAGE (CHECK-F10): controlli SymPy indipendenti per le voci 1 (P1-Q7), 3 (SYS-DIRAC-POL complesso),
# 4 (Amitsur elementare), 5 (Bjork: dimensione 3 di gr(A2/A2L)).  Nessuna importazione da triage_scripts.
import itertools, random
import sympy as sp

results = []
def ok(name, cond):
    results.append((name, bool(cond))); print(('OK  ' if cond else 'FAIL') + '  ' + name)

# ---------------- voce 1: P1-Q7, candidato X = (x^3+x)d, Y = d ----------------
x, s, nu, eps = sp.symbols('x s nu epsilon')
X0 = lambda f: sp.expand(x**3 * sp.diff(f, x))
X1 = lambda f: sp.expand(x * sp.diff(f, x))
Yop = lambda f: sp.expand(sp.diff(f, x))
S = 4  # ordine in s

def exp_apply(op, coef, f, order=S):
    # e^{coef * op} f troncato: coef e' una serie in s senza termine costante (grado >= 1)
    out = 0; term = f
    for n in range(order + 1):
        out += term
        term = sp.expand(coef * op(term) / (n + 1))
        term = sp.series(term, s, 0, order + 1).removeO() if term != 0 else 0
    return sp.expand(sp.series(out, s, 0, order + 1).removeO())

def trunc(e, order=S):
    return sp.expand(sp.series(sp.expand(e), s, 0, order + 1).removeO()) if e != 0 else 0

# (1a) sigma_mu e sostituzione t = nu^2 s: membro sinistro e^{s(X0 + nu^2 X1 + eps nu^3 Y)}
A = lambda f: sp.expand(X0(f) + nu**2 * X1(f) + eps * nu**3 * Yop(f))
def lhs(f):
    out = 0; term = f
    for n in range(S + 1):
        out += s**n * term / sp.factorial(n); term = A(term)
    return sp.expand(out)
def duhamel_X0(f):
    # sum_n s^n/n! sum_{a+b=n-1} X0^a Y X0^b f
    out = 0
    for n in range(1, S + 1):
        acc = 0
        for a in range(n):
            b = n - 1 - a; g = f
            for _ in range(b): g = X0(g)
            g = Yop(g)
            for _ in range(a): g = X0(g)
            acc += g
        out += s**n * acc / sp.factorial(n)
    return sp.expand(out)
good1 = True; good3 = True
for j in range(0, 4):
    f = x**j; L = sp.Poly(lhs(f), nu)
    c1 = L.coeff_monomial(nu); c3 = L.coeff_monomial(nu**3)
    good1 &= sp.expand(c1) == 0
    good3 &= sp.expand(c3 - eps * duhamel_X0(f)) == 0
ok('P1-Q7 sinistra: coeff. di nu^1 nullo, coeff. di nu^3 = eps * Duhamel con il solo X0 (nessun X1), f = x^j, j<=3, s^<=4', good1 and good3)

# (1b) membro destro per una parola X Y X Y X con tempi formali generici: coeff. di nu^3 = sola formula (beta)
word = ['X', 'Y', 'X', 'Y', 'X']
gs = [[sp.Symbol('g%d_%d' % (i, k)) for k in range(1, S + 1)] for i in range(len(word))]
def factor_apply(i, f):
    Z = word[i]
    if Z == 'X':
        h = sum(gs[i][k - 1] * nu**(2 * k - 2) * s**k for k in range(1, S + 1))   # esponente su X0 + nu^2 X1
        op = lambda g: sp.expand(X0(g) + nu**2 * X1(g))
    else:
        h = sum(gs[i][k - 1] * nu**(2 * k + 1) * s**k for k in range(1, S + 1))
        op = Yop
    return exp_apply(op, h, f)
def rhs(f):
    g = f
    for i in reversed(range(len(word))): g = factor_apply(i, g)
    return sp.expand(g)
def beta_formula(f):
    # sum_{i: Y} [prod_{j<i} e^{h_j(s,0) X0}] (g_{i,1} s Y) [prod_{j>i} e^{h_j(s,0) X0}] f
    out = 0
    for i, Z in enumerate(word):
        if Z != 'Y': continue
        g = f
        for jj in reversed(range(i + 1, len(word))):
            if word[jj] == 'X': g = exp_apply(X0, gs[jj][0] * s, g)
        g = trunc(gs[i][0] * s * Yop(g))
        for jj in reversed(range(0, i)):
            if word[jj] == 'X': g = exp_apply(X0, gs[jj][0] * s, g)
        out += g
    return trunc(out)
good = True; goododd = True
for j in [0, 1, 2]:
    f = x**j; R = sp.Poly(rhs(f), nu)
    goododd &= sp.expand(R.coeff_monomial(nu)) == 0
    good &= sp.expand(R.coeff_monomial(nu**3) - beta_formula(f)) == 0
ok('P1-Q7 destra (parola XYXYX, tempi formali): coeff. nu^1 nullo; coeff. nu^3 = solo termini (beta), nessun contributo X1', good and goododd)

# (1c) (H) per (x^3 d, d): Y_k = ad_{X0}^k Y ha grado 2k  => indipendenti; e anche ad_X^k Y per X = (x^3+x)d
def br(p, q): return sp.expand(p * sp.diff(q, x) - q * sp.diff(p, x))
for X0p, nm in [(x**3, 'x^3 d'), (x**3 + x, '(x^3+x) d')]:
    Yk = [sp.Integer(1)]
    for k in range(1, 9): Yk.append(br(X0p, Yk[-1]))
    ok('(H) per (%s, d): deg Y_k = 2k, k<=8, e X fuori dallo span' % nm,
       all(sp.degree(Yk[k], x) == 2 * k for k in range(9)) and sp.degree(X0p, x) % 2 == 1)

# (1d) Duhamel = e^{sX0} sum_k (-1)^k s^{k+1}/(k+1)! Y_k  (P1-L5), su polinomi
def adk(k):
    p = sp.Integer(1)
    for _ in range(k): p = br(x**3, p)
    return p
good = True
for j in range(3):
    f = x**j; inner = 0
    for k in range(S):
        inner += (-1)**k * s**(k + 1) / sp.factorial(k + 1) * sp.expand(adk(k) * sp.diff(f, x))
    good &= sp.expand(trunc(exp_apply(X0, s, trunc(inner))) - trunc(duhamel_X0(f))) == 0
ok('Duhamel con X0: formula di P1-L5 (ordine s^4)', good)

# ---------------- voce 3: SYS-DIRAC-POL, asintotica del bersaglio ----------------
xi, t, m = sp.symbols('xi t m', positive=True)
w = sp.sqrt(xi**2 + m**2)
# (e^{tA})_11 = cos wt + i xi sin(wt)/w = e^{iwt} + i (xi/w - 1) sin wt  (identita' esatta)
W11 = sp.cos(w * t) + sp.I * xi * sp.sin(w * t) / w
ok('Dirac: (e^{tA})_11 = e^{iwt} + i(xi/w - 1) sin wt', sp.simplify(sp.expand_complex(W11 - sp.exp(sp.I * w * t) - sp.I * (xi / w - 1) * sp.sin(w * t))) == 0)
e_ = sp.Symbol('e', positive=True)
ph = sp.series((m**2 / (w + xi)).subs(xi, 1 / e_), e_, 0, 3).removeO()     # w - xi = m^2/(w+xi)
ser1 = sp.series(sp.exp(sp.I * t * ph) - 1, e_, 0, 2).removeO()
ser2 = sp.series((xi / w - 1).subs(xi, 1 / e_), e_, 0, 2).removeO()
ok('Dirac: e^{i(w-xi)t} - 1 = i m^2 t/(2 xi) + O(xi^-2) e xi/w - 1 = O(xi^-2) => G e^{-i xi t} ~ i m^2 t/(2 xi)', sp.simplify(ser1 - sp.I * m**2 * t * e_ / 2) == 0 and sp.simplify(ser2) == 0)
# Lemma E': esempio numerico (media quadratica della classe dominante)
import mpmath as mp
R = [lambda z: z**2 + 1j * z, lambda z: 3 * z + 1j * z + 0.5j, lambda z: z**3 + 2j * z]
d = [1.0, 2.0, 5.0]
def Sfun(z): return sum(dj * mp.e**(1j * Rj(z)) for dj, Rj in zip(d, R))
X = 40.0
ms = mp.quad(lambda z: abs(Sfun(z) * mp.e**(z))**2, [X, 2 * X], maxdegree=10) / X
# classe dominante: Im R = z per R_0, R_1 (differenza costante 0.5); attesa |1|^2 + |2 e^{-0.5}|^2
target = 1 + (2 * mp.e**(-0.5))**2
ok("Lemma E' (esempio): media quadratica di S e^{Im R_j0} su [X,2X] ~ sum |d'_j|^2 (scarto %.3f)" % float(abs(ms - target)), abs(ms - target) < 0.15)

# ---------------- voce 4: Amitsur elementare, algoritmo della prova ----------------
def amitsur(Ds, Zbasis, trials=30):
    # Ds: matrici (V x n) ; Z = span delle colonne di Zbasis. Restituisce (r, c) secondo la prova del triage.
    Ds = [sp.Matrix(D) * Zbasis for D in Ds]  # restrizioni a Z in coordinate
    k = Zbasis.shape[1]
    best = (-1, None)
    for _ in range(trials):
        u0 = sp.Matrix([random.randint(-5, 5) for _ in range(k)])
        r = sp.Matrix.hstack(*[D * u0 for D in Ds]).rank()
        if r > best[0]: best = (r, u0)
    r, u0 = best
    cols = [D * u0 for D in Ds]
    idx = []
    for i in range(len(Ds)):
        if sp.Matrix.hstack(*[cols[a] for a in idx + [i]]).rank() == len(idx) + 1: idx.append(i)
        if len(idx) == r: break
    j = next(i for i in range(len(Ds)) if i not in idx)
    Sset = idx + [j]
    # funzionali phi: righe scelte con det != 0 sulle colonne idx
    Vdim = cols[0].shape[0]
    phi = None
    for rows in itertools.combinations(range(Vdim), r):
        Mt = sp.Matrix([[cols[i][a] for i in idx] for a in rows])
        if r == 0 or Mt.det() != 0: phi = rows; break
    Mfull = sp.Matrix([[cols[i][a] for i in Sset] for a in phi]) if r > 0 else sp.zeros(0, len(Sset))
    alpha = []
    for c in range(len(Sset)):
        sub = Mfull[:, [cc for cc in range(len(Sset)) if cc != c]] if r > 0 else sp.zeros(0, 0)
        alpha.append((-1)**c * (sub.det() if r > 0 else 1))
    coeff = [0] * len(Ds)
    for c, i in enumerate(Sset): coeff[i] = alpha[c]
    Dsum = sum((coeff[i] * Ds[i] for i in range(len(Ds))), sp.zeros(*Ds[0].shape))
    return r, coeff, Dsum.rank()
# (4a) prodotto vettore: D_i w = e_i x w su C^3, localmente dipendenti (span <= 2)
E = [sp.Matrix(3, 1, lambda a, b: 1 if a == i else 0) for i in range(3)]
cross = [sp.Matrix([[0, -e[2], e[1]], [e[2], 0, -e[0]], [-e[1], e[0], 0]]) for e in E]
r, c, rk = amitsur(cross, sp.eye(3))
ok('Amitsur elementare, prodotto vettore (N+1=3): r=%d, c=%s != 0, rango(sum c_i D_i)=%d <= r' % (r, c, rk), any(c) and rk <= r)
# (4b) famiglia casuale localmente dipendente: D_i = B * C_i con B di rango 2 su V = C^4, 4 operatori (N = 3), Z sottospazio
random.seed(5)
B = sp.Matrix(4, 2, lambda a, b: random.randint(-3, 3))
Cs = [sp.Matrix(2, 5, lambda a, b: random.randint(-3, 3)) for _ in range(4)]
Ds = [B * C for C in Cs]
Zb = sp.Matrix(5, 3, lambda a, b: random.randint(-3, 3))
r, c, rk = amitsur(Ds, Zb)
ok('Amitsur elementare, D_i = B C_i (rango locale <= 2 < 4): r=%d, rango(sum c_i D_i|_Z)=%d <= r, c != 0' % (r, rk), any(c) and rk <= r)
# (4c) famiglia con rango locale r=3 < N+1 = 4 ma senza fattore comune: D_i w = (e_i x w, <e_i, w>) ... controllo diretto
def Dmat(i):
    M = sp.zeros(4, 4)
    M[:3, :3] = cross[i] if i < 3 else sp.zeros(3, 3)
    if i == 3: M[3, 3] = 1
    return M
Ds = [Dmat(i) for i in range(4)]
r, c, rk = amitsur(Ds, sp.eye(4))
ok('Amitsur elementare, blocco (prodotto vettore) + identita: r=%d, rango=%d <= r' % (r, rk), any(c) and rk <= r)

# ---------------- voce 5: Bjork, gr(A2/A2L) di dimensione 3 ----------------
# algebra di Weyl A2 in forma normale x^a t^b dx^c dt^d; prodotto con la formula di Leibniz
from math import comb, factorial
def wmul(P1, P2):
    out = {}
    for (a1, b1, c1, d1), v1 in P1.items():
        for (a2, b2, c2, d2), v2 in P2.items():
            for i in range(min(c1, a2) + 1):
                for j in range(min(d1, b2) + 1):
                    co = v1 * v2 * comb(c1, i) * comb(d1, j) * (factorial(a2) // factorial(a2 - i)) * (factorial(b2) // factorial(b2 - j))
                    key = (a1 + a2 - i, b1 + b2 - j, c1 + c2 - i, d1 + d2 - j)
                    out[key] = out.get(key, 0) + co
    return {k: v for k, v in out.items() if v != 0}
def bdeg(Pp): return max(sum(k) for k in Pp)
def symb(Pp):
    dg = bdeg(Pp); return {k: v for k, v in Pp.items() if sum(k) == dg}
def pmulc(S1, S2):
    out = {}
    for k1, v1 in S1.items():
        for k2, v2 in S2.items():
            k = tuple(a + b for a, b in zip(k1, k2)); out[k] = out.get(k, 0) + v1 * v2
    return {k: v for k, v in out.items() if v != 0}
random.seed(11)
Lop = {(0, 0, 0, 2): 1, (1, 0, 1, 0): 3, (0, 1, 0, 0): -2, (2, 0, 0, 0): 1}   # L = dt^2 + 3 x dx - 2 t + x^2 (monico in dt)
good = True
for _ in range(20):
    Q = {}
    for _ in range(5):
        Q[tuple(random.randint(0, 3) for _ in range(4))] = random.randint(-4, 4) or 1
    Q = {k: v for k, v in Q.items() if v}
    QL = wmul(Q, Lop)
    good &= bdeg(QL) == bdeg(Q) + bdeg(Lop) and symb(QL) == pmulc(symb(Q), symb(Lop))
ok('Bjork: sigma(QL) = sigma(Q) sigma(L) e deg QL = deg Q + deg L (filtrazione di Bernstein, 20 Q casuali)', good)
j = sp.Symbol('j'); dL = bdeg(Lop)
hilb = sp.expand(sp.binomial(j + 4, 4) - sp.binomial(j - dL + 4, 4))
ok('Bjork: dim F_j(A2/A2L) = C(j+4,4) - C(j-%d+4,4) ha grado 3 in j (dimensione 3 > 2)' % dL, sp.degree(sp.expand_func(hilb), j) == 3)

print('RISULTATO: %d/%d' % (sum(r for _, r in results), len(results)))
