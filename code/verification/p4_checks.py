# S-P4 -- controlli SymPy (verifica, non metodo). Esecuzione:
#   D:\ProblemaBase\.venv\Scripts\python.exe -I p4_checks.py > p4_checks.out
import sys
sys.stdout.reconfigure(encoding='utf-8')
import sympy as sp

t, x, z1, z2, s, lam = sp.symbols('t x z1 z2 s lam')
RES = []
def check(name, cond, info=''):
    RES.append((name, bool(cond)))
    print(('[OK]   ' if cond else '[FAIL] ') + name + ((' :: ' + str(info)) if info != '' else ''))

def Dop(Q, u, tv=t, xv=x):
    """Applica Q(d_t,d_x) (dict {(a,b):coeff}) a u."""
    return sp.expand(sum(c * sp.diff(u, tv, a, xv, b) if (a or b) else c * u for (a, b), c in Q.items()))

def monos(n):
    return [(a, b) for a in range(n + 1) for b in range(n + 1 - a)]

# ---------------------------------------------------------------- C1: L4, Weyl
# (c0 + c1 d) agisce su A1.e^x = C[x]e^x ; nullo su x e^x  => c0=c1=0 (restrizione iniettiva)
c0, c1 = sp.symbols('c0 c1')
u = sp.exp(x)
expr = sp.simplify((c0 * x * u + c1 * sp.diff(x * u, x)) / u)
sol = sp.solve(sp.Poly(expr, x).coeffs(), [c0, c1], dict=True)
check('C1a Weyl: (c0+c1 d)|_{C[x]e^x}=0 => c0=c1=0', sol == [{c0: 0, c1: 0}], sol)
check('C1b Weyl: (d-1) e^x = 0 (Ann ∩ span{1,d} != 0)', sp.simplify(sp.diff(u, x) - u) == 0)
# simplicita' (ingrediente della prova): [d, x^i d^j] = i x^(i-1) d^j , [x^i d^j, x] = j x^i d^(j-1)
f = sp.Function('f')
for i, j in [(2, 3), (3, 1), (1, 2)]:
    Qf = lambda g: x**i * sp.diff(g, x, j)
    lhs1 = sp.diff(Qf(f(x)), x) - Qf(sp.diff(f(x), x))
    lhs2 = Qf(x * f(x)) - x * Qf(f(x))
    ok1 = sp.simplify(lhs1 - i * x**(i - 1) * sp.diff(f(x), x, j)) == 0
    ok2 = sp.simplify(lhs2 - j * x**i * sp.diff(f(x), x, j - 1)) == 0
    check(f'C1c commutatori ad_d, ad_x su x^{i} d^{j}', ok1 and ok2)

# ---------------------------------------------------------------- C2: u = t + e^{x^2}
u = t + sp.exp(x**2)
n = 3
cs = {m: sp.Symbol(f'q{m[0]}{m[1]}') for m in monos(n)}
Qu = Dop(cs, u)
B = sp.expand(Qu).coeff(sp.exp(x**2))
A = sp.expand(Qu - B * sp.exp(x**2))
eqs = sp.Poly(A, t, x).coeffs() + sp.Poly(sp.expand(B), x).coeffs()
M = sp.Matrix([[sp.diff(e, cs[m]) for m in monos(n)] for e in eqs])
ns = M.nullspace()
expected = [m for m in monos(n) if m[0] >= 2 or (m[0] >= 1 and m[1] >= 1)]
span_ok = len(ns) == len(expected) and all(
    all(v[k] == 0 for k, m in enumerate(monos(n)) if m not in expected) for v in ns)
check('C2a Ann(t+e^{x^2}) ∩ R_{<=3} = (tau^2, tau xi)_{<=3}', span_ok, f'dim={len(ns)}')
check('C2b tau.u = 1 (parte EP = C), xi.1 = 0', sp.diff(u, t) == 1)

# ---------------------------------------------------------------- C3: u EP, spettro, Pade 2D
u = x * sp.exp(t + x) + sp.exp(4 * t + 2 * x)
basis = [x * sp.exp(t + x), sp.exp(t + x), sp.exp(4 * t + 2 * x)]
E1s, E2s = sp.symbols('E1 E2')
def coords(w):
    ws = sp.expand(sp.powsimp(sp.expand(w, power_exp=False)), power_exp=False)
    ws = ws.subs({sp.exp(t + x): E1s, sp.exp(4 * t + 2 * x): E2s})
    pw = sp.Poly(ws, E1s, E2s, x)
    return sp.Matrix([pw.coeff_monomial(E1s * x), pw.coeff_monomial(E1s), pw.coeff_monomial(E2s)])
At = sp.Matrix.hstack(*[coords(sp.diff(b, t)) for b in basis])
Bx = sp.Matrix.hstack(*[coords(sp.diff(b, x)) for b in basis])
check('C3a A,B commutano', At * Bx == Bx * At)
# rango del modulo ciclico: d = 3
ders = [sp.diff(u, t, a, x, b) for (a, b) in monos(4)]
J = sp.Matrix([list(coords(w)) for w in ders])
check('C3b dim R.u = 3', J.rank() == 3)
# autovettori congiunti: (1,1) e (4,2)
eig = []
for (ta, xb) in [(1, 1), (4, 2), (1, 2), (4, 1)]:
    K = sp.Matrix.vstack(At - ta * sp.eye(3), Bx - xb * sp.eye(3)).nullspace()
    eig.append(len(K))
check('C3c spettro puntuale = {(1,1),(4,2)}, molteplicita geometrica 1', eig == [1, 1, 0, 0], eig)
# A diagonalizzabile, B no (q = x non costante): W non semisemplice
check('C3d B non diagonalizzabile (Jordan per xi=1)', not Bx.is_diagonalizable())
mu_t = sp.factor(sp.Matrix(At).charpoly(z1).as_expr())
# polinomi minimi
def minpoly(Mx, z):
    for k in range(1, 4):
        pass
    cp = sp.factor_list(Mx.charpoly(z).as_expr())
    return cp
# risolvente: S = ev_{p0} (z1-A)^{-1}(z2-B)^{-1} u , p0 = (0,0)
ev = sp.Matrix([[b.subs({t: 0, x: 0}) for b in basis]])
cu = coords(u)
S = sp.simplify((ev * (z1 * sp.eye(3) - At).inv() * (z2 * sp.eye(3) - Bx).inv() * cu)[0])
Sf = sp.factor(S)
den = sp.denom(sp.together(Sf))
check('C3e denominatore di S separabile = (z1-1)(z1-4)(z2-1)^2(z2-2) (a meno di costanti)',
      sp.simplify(sp.factor(den) / ((z1 - 1) * (z1 - 4) * (z2 - 1)**2 * (z2 - 2))).is_constant(), sp.factor(den))
# sviluppo di S in z^{-1} contro il jet
w1, w2 = sp.symbols('w1 w2')
T = sp.simplify(S.subs({z1: 1 / w1, z2: 1 / w2}) / (w1 * w2))
ser = sp.expand(sp.series(sp.series(T, w1, 0, 4).removeO(), w2, 0, 4).removeO())
okj = True
for a in range(3):
    for b in range(3):
        sab = sp.diff(u, t, a, x, b).subs({t: 0, x: 0})
        okj &= sp.simplify(ser.coeff(w1, a).coeff(w2, b) - sab) == 0
check('C3f coefficienti di S = jet s_ab (a,b<=2)', okj)
# a(z1) b(z2) S polinomio con a=(z1-1)(z1-4), b=(z2-1)^2(z2-2); con b=(z2-1)(z2-2) no
N1 = sp.cancel((z1 - 1) * (z1 - 4) * (z2 - 1)**2 * (z2 - 2) * S)
N2 = sp.cancel((z1 - 1) * (z1 - 4) * (z2 - 1) * (z2 - 2) * S)
check('C3g a(z1)b(z2)S polinomio con le eliminanti minime', N1.is_polynomial(z1, z2) and not N2.is_polynomial(z1, z2))
# eliminanti: (tau-1)(tau-4), (xi-1)^2(xi-2) annullano u ; (xi-1)(xi-2) no
check('C3h eliminanti di Ann(u)', sp.simplify(Dop({(2, 0): 1, (1, 0): -5, (0, 0): 4}, u)) == 0 and
      sp.simplify(Dop({(0, 3): 1, (0, 2): -4, (0, 1): 5, (0, 0): -2}, u)) == 0 and
      sp.simplify(Dop({(0, 2): 1, (0, 1): -3, (0, 0): 2}, u)) != 0)
# T3(i): Ann(u) ∩ R_{<=2} da contrazione sulla serie = calcolo diretto
def ann_direct(u, n):
    cols = [coords(sp.diff(u, t, m[0], x, m[1])) for m in monos(n)]
    return sp.Matrix.hstack(*cols).nullspace()
def ann_contr(u, n, K):
    rows = []
    for (a, b) in monos(K):
        rows.append([sp.diff(u, t, a + m[0], x, b + m[1]).subs({t: 0, x: 0}) for m in monos(n)])
    return sp.Matrix(rows).nullspace()
nd, nc = ann_direct(u, 2), ann_contr(u, 2, 4)
check('C3i Ann ∩ R_<=2: contrazione (jet ordine 6) = diretto', len(nd) == len(nc) and
      sp.Matrix.hstack(*nd).rank() == sp.Matrix.hstack(*(nd + nc)).rank(), (len(nd), len(nc)))

# ---------------------------------------------------------------- C4: I0(2 sqrt(tx)), tau xi - 1
Nn = 8
uI = sum((t * x)**k / sp.factorial(k)**2 for k in range(Nn + 1))
okd = all(sp.diff(uI, t, a, x, b).subs({t: 0, x: 0}) == (1 if a == b else 0) for a in range(6) for b in range(6))
check('C4a s_ab = delta_ab (a,b<=5)', okd)
res = sp.expand(sp.diff(uI, t, 1, x, 1) - uI)
check('C4b (d_t d_x - 1)u = O((tx)^N) (serie troncata)', sp.Poly(res, t, x).total_degree() >= 2 * Nn)
Tser = sp.series(1 / (1 - w1 * w2), w1, 0, 6).removeO()
check('C4c S = 1/(z1 z2 - 1): coefficienti delta_ab', all(sp.expand(Tser).coeff(w1, a).coeff(w2, b) == (1 if a == b else 0)
                                                         for a in range(5) for b in range(5)))
# nessun a(tau) di grado <=6 compatibile col jet: sum_k a_k s_{k+i,b}=0 per i,b<=6
aa = sp.symbols('a0:7')
eqs = [sum(aa[k] * (1 if k + i == b else 0) for k in range(7)) for i in range(7) for b in range(7)]
check('C4d nessuna eliminante in tau di grado <=6', sp.solve(eqs, aa, dict=True) == [{a_: 0 for a_ in aa}])
check('C4e su W: d_x inverte d_t (tau xi = 1 nel modulo)', sp.expand(sp.diff(sp.diff(uI, x), t) - uI).subs({t: 0}) == 0)

# ---------------------------------------------------------------- C5: identificazione per componenti
G = sp.exp(-x**2 / (4 * t)) / sp.sqrt(t)
u2 = sp.exp(x - t)
w2 = sp.simplify(sp.diff(u2, t) - sp.diff(u2, x, 2))           # (tau - xi^2) u_2 = -2 e^{x-t}
check('C5a (tau-xi^2)(G+e^{x-t}) = -2 e^{x-t} in EP', sp.simplify(sp.diff(G + u2, t) - sp.diff(G + u2, x, 2) + 2 * u2) == 0)
w1 = sp.simplify(sp.diff(G, t) + sp.diff(G, x))
# grado polinomiale crescente: d_x^k w1 / G polinomio in x di grado k+2 (k<=4) => w1 non EP
okg = True
for k in range(5):
    r = sp.simplify(sp.diff(w1, x, k) / G)
    num = sp.together(r)
    pol = sp.Poly(sp.numer(num), x)
    okg &= pol.degree() == k + 2
check('C5b (tau+xi)G: d_x^k w/G ha grado k+2 (non EP, coerente con P4-L5)', okg)

# ---------------------------------------------------------------- C6: lemmi di decidibilita'
def weyl_split(Lc):
    """Lc: dict {(i,j): c} per x^i d^j. Ritorna D e M_D(xi)."""
    D = max(i for (i, j) in Lc)
    xi = sp.Symbol('xi')
    MD = sum(c * xi**j for (i, j), c in Lc.items() if i == D)
    return D, sp.expand(MD), xi
def conj_lambda(Lc, la):
    """L_lambda = sum x^i M_i(d+lambda): dict {(i,j): m_ij}"""
    xi = sp.Symbol('xi')
    out = {}
    for (i, j), c in Lc.items():
        pe = sp.Poly(sp.expand(c * (xi + la)**j), xi)
        for (jj,), cc in pe.terms():
            out[(i, jj)] = sp.expand(out.get((i, jj), 0) + cc)
    return {k: v for k, v in out.items() if v != 0}
def iota_inf(Lc, la):
    m = conj_lambda(Lc, la)
    dl = max(i - j for (i, j) in m)
    nn = sp.Symbol('n')
    return sp.expand(sum(c * sp.ff(nn, j) for (i, j), c in m.items() if i - j == dl)), nn
def B_bound(Lc):
    D, MD, xi = weyl_split(Lc)
    roots = sp.roots(sp.Poly(MD, xi)) if sp.Poly(MD, xi).degree() > 0 else {}
    tot = 0
    for la in roots:
        io, nn = iota_inf(Lc, la)
        ints = [r for r in sp.roots(sp.Poly(io, nn)) if r.is_integer and r >= 0] if sp.Poly(io, nn).degree() > 0 else []
        tot += (max(ints) + 1) if ints else 0
    return tot
def applyL(Lc, g):
    return sp.expand(sum(c * x**i * sp.diff(g, x, j) if j else c * x**i * g for (i, j), c in Lc.items()))
L1 = {(1, 1): 1, (0, 0): -5}                         # x d - 5 : soluzione x^5
check('C6a B(x d - 5) = 6 e x^5 soluzione', B_bound(L1) == 6 and applyL(L1, x**5) == 0)
L2 = {(0, 1): 1, (1, 0): 2}                          # d + 2x : soluzione e^{-x^2}
check('C6b B(d + 2x) = 0 (nessuna soluzione EP non nulla)', B_bound(L2) == 0 and sp.simplify(applyL(L2, sp.exp(-x**2))) == 0)
L3 = {(0, 3): 1, (0, 2): -5, (0, 1): 8, (0, 0): -4}  # (d-2)^2(d-1)
check('C6c B((d-2)^2(d-1)) = 3', B_bound(L3) == 3)
L4h = {(0, 1): 2, (1, 0): 1}                          # 2d + x : fetta del calore e^{-x^2/4}
check('C6d fetta del calore: B = 0 => G identifica (P4-T5)', B_bound(L4h) == 0)
# indicial a x0: x d - 5 in x0=0: iota(n)=n-5 => K=5
def iota_at(Lc, x0):
    m = {}
    for (i, j), c in Lc.items():
        pe = sp.Poly(sp.expand(c * (s + x0)**i), s)
        for (ii,), cc in pe.terms():
            m[(ii, j)] = sp.expand(m.get((ii, j), 0) + cc)
    m = {k: v for k, v in m.items() if v != 0}
    dl = min(i - j for (i, j) in m)
    nn = sp.Symbol('n')
    return sp.expand(sum(c * sp.ff(nn, j) for (i, j), c in m.items() if i - j == dl)), nn
io0, nn = iota_at(L1, 0)
check('C6e polinomio indiciale di x d - 5 in 0: n - 5', sp.expand(io0 - (nn - 5)) == 0)
# Hankel 1D (C3-T3 in una variabile): f = x e^{2x} + e^x, B = 3, jet di ordine 5 in 0
fE = x * sp.exp(2 * x) + sp.exp(x)
Bb = 3
mom = [sp.diff(fE, x, k).subs(x, 0) for k in range(2 * Bb)]
H = sp.Matrix(Bb, Bb + 1, lambda i, j: mom[i + j])
kv = H.nullspace()
xi = sp.Symbol('xi')
pk = sp.factor(sum(kv[0][j] * xi**j for j in range(Bb + 1))) if len(kv) == 1 else None
check('C6f Hankel 3x4: nucleo = (xi-2)^2(xi-1)', pk is not None and sp.simplify(pk / ((xi - 2)**2 * (xi - 1))).is_constant(), pk)
# algoritmo completo su f = A e^{-x^2/4} + e^{1+x} (calore + modo): span formale su Q(x) di h1=e^{-x^2/4}, h2=e^x
# derivazione nello span: D h1 = -x/2 h1, D h2 = h2 ; f = h1 + e h2
def Dvec(v):
    return sp.Matrix([sp.diff(v[0], x) - x / 2 * v[0], sp.diff(v[1], x) + v[1]])
v0 = sp.Matrix([1, sp.E])
vs = [v0]
for k in range(2):
    vs.append(sp.simplify(Dvec(vs[-1])))
Mrel = sp.Matrix.hstack(*vs)                         # 2x3 su Q(x): relazione non banale
rel = Mrel.nullspace()[0]
den_ = sp.lcm([sp.denom(sp.together(r)) for r in rel])
relp = [sp.factor(sp.simplify(r * den_)) for r in rel]
fH = sp.exp(-x**2 / 4) + sp.exp(1 + x)
Lf = sp.simplify(sum(relp[j] * sp.diff(fH, x, j) for j in range(3)))
check('C6g annullatore costruito per span formale: L_f f = 0', Lf == 0, relp)
Lc = {}
for j in range(3):
    for (i,), c in sp.Poly(sp.expand(relp[j]), x).terms():
        Lc[(i, j)] = sp.expand(Lc.get((i, j), 0) + c)
Bf = B_bound(Lc)
check('C6h B(L_f) >= 1 (modo e^x ammesso)', Bf >= 1, Bf)
mom = [sp.simplify(sp.diff(fH, x, k).subs(x, 0)) for k in range(2 * Bf)]
H = sp.Matrix(Bf, Bf + 1, lambda i, j: mom[i + j])
kv = H.nullspace()
verdict = None
if not kv:
    verdict = 'non EP'
else:
    p = sum(kv[0][j] * sp.Symbol('xi')**j for j in range(Bf + 1))
    g = sp.simplify(sum(kv[0][j] * sp.diff(fH, x, j) for j in range(Bf + 1)))
    verdict = 'EP' if g == 0 else 'non EP'
check('C6i algoritmo: fetta di G + e^{t+x} non EP => Ann(u)=(tau-xi^2)', verdict == 'non EP', verdict)
# stesso algoritmo su f = e^{1+x} (EP): L = d - 1
fE2 = sp.exp(1 + x); Lc2 = {(0, 1): 1, (0, 0): -1}
Bf2 = B_bound(Lc2)
mom = [sp.diff(fE2, x, k).subs(x, 0) for k in range(2 * Bf2)]
H = sp.Matrix(Bf2, Bf2 + 1, lambda i, j: mom[i + j]); kv = H.nullspace()
g = sp.simplify(sum(kv[0][j] * sp.diff(fE2, x, j) for j in range(Bf2 + 1))) if kv else None
check('C6j algoritmo: fetta EP riconosciuta', Bf2 == 1 and g == 0)

# ---------------------------------------------------------------- C7: lemma dei dati di Cauchy (onda)
# P = tau^2 - xi^2, compagna C(xi) = [[0,1],[xi^2,0]] ; dati EP f0 = x e^x, f1 = e^{2x}
def evolve(F_terms, m_deg=1):
    """F_terms: lista (xi_k, [q_0(x), q_1(x)]) ; ritorna U(t,x) = sum e^{xi_k x} exp(t M_k) Q_k."""
    U = sp.zeros(2, 1)
    for xk, Qk in F_terms:
        dmax = max(sp.Poly(q, x).degree() for q in Qk if q != 0)
        mon = [x**e for e in range(dmax + 1)]
        def vec(q):
            pq = sp.Poly(q, x); return [pq.coeff_monomial(x**e) for e in range(dmax + 1)]
        # base di (C[x]_{<=d})^2 : (component, exponent)
        idx = [(c, e) for c in range(2) for e in range(dmax + 1)]
        def Mapply(Qv):
            q0, q1 = Qv
            xi_op = lambda q: sp.expand(xk * q + sp.diff(q, x))
            return [q1, sp.expand(xi_op(xi_op(q0)))]   # C(xi+d) = [[0,1],[(xi+d)^2,0]]
        cols = []
        for (c, e) in idx:
            Qv = [0, 0]; Qv[c] = x**e
            r = Mapply(Qv)
            cols.append(vec(r[0]) + vec(r[1]))
        Mk = sp.Matrix(cols).T
        E = (t * Mk).exp()
        q0v = sp.Matrix(vec(Qk[0]) + vec(Qk[1]))
        out = E * q0v
        n1 = dmax + 1
        U[0] += sp.exp(xk * x) * sum(out[e] * x**e for e in range(n1))
        U[1] += sp.exp(xk * x) * sum(out[n1 + e] * x**e for e in range(n1))
    return U
U = evolve([(1, [x, 0]), (2, [0, 1])])
E1 = sp.simplify(U[0])
okw = sp.simplify(sp.diff(E1, t, 2) - sp.diff(E1, x, 2)) == 0
okd = sp.simplify(E1.subs(t, 0) - x * sp.exp(x)) == 0 and sp.simplify(sp.diff(E1, t).subs(t, 0) - sp.exp(2 * x)) == 0
check('C7 E EP costruita da dati di Cauchy EP risolve l onda con quei dati', okw and okd)

# ---------------------------------------------------------------- C8: impossibilita' a scatola nera (P4-T6), esempio
# P = tau - xi^2, u = G in p0=(1,0), K=2 ; query di zero Q1 = xi, Q2 = tau + 1 (non in (P))
p0 = {t: 1, x: 0}
jetG = {m: sp.diff(G, t, m[0], x, m[1]).subs(p0) for m in monos(2)}
pts = list(range(-4, 5))                              # z = (k^2, k) su V(tau - xi^2), algebrici
ez = [sp.exp(k**2 * (t - 1) + k * x) for k in pts]
cc = sp.symbols(f'c0:{len(pts)}')
v = sum(ci * ei for ci, ei in zip(cc, ez))
eqs = [sp.diff(v, t, m[0], x, m[1]).subs(p0) - jetG[m] for m in monos(2)]
sol = sp.solve(eqs, cc[:6], dict=True)[0]
free = {ci: sp.Rational(k + 2, 7) for k, ci in enumerate(cc[6:])}
vv = sp.simplify(v.subs(sol).subs(free))
same = all(sp.simplify(sp.diff(vv, t, m[0], x, m[1]).subs(p0) - jetG[m]) == 0 for m in monos(2))
inP = sp.simplify(sp.diff(vv, t) - sp.diff(vv, x, 2)) == 0
q1 = sp.simplify(sp.diff(vv, x)) != 0
q2 = sp.simplify(sp.diff(vv, t) + vv) != 0
check('C8 v EP in ker P con lo stesso 2-jet di G e risposte di zero-test uguali (xi, tau+1)', same and inP and q1 and q2)

# ---------------------------------------------------------------- C9: spettro di d_t su R.u = pi_tau V(Ann u)
# u EP del C3: spettro di A = {1,4} = proiezione di {(1,1),(4,2)}
check('C9 spettro di A = proiezione tau di V(Ann u)', set(At.eigenvals().keys()) == {1, 4})

print('\nTOTALE:', sum(ok for _, ok in RES), '/', len(RES), 'OK')
