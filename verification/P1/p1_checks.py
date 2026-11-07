"""S-P1 - controlli SymPy (solo VERIFICA di enunciati, vincolo k3).
Eseguire: D:\\ProblemaBase\\.venv\\Scripts\\python.exe -I p1_checks.py
Ogni controllo stampa [PASS]/[FAIL] con l'ID del claim di work/P1/PROOF_PACKAGE.md."""
import itertools
import sympy as sp

RES = []


def check(name, cond):
    RES.append((name, bool(cond)))
    print(f"[{'PASS' if cond else 'FAIL'}] {name}")


def zero(e):
    return sp.simplify(sp.expand(e)) == 0


t, s, x, z, zeta = sp.symbols('t s x z zeta')
D, c, beta = sp.symbols('D c beta', positive=True)

# ---------------------------------------------------------------- C1
# P1-L2: S_n(s) definito dalla serie sum s^k a_n(d)^k f / k! coincide, su x^l e^{zeta x},
# con d_zeta^l ( e^{s a_n(zeta)} e^{zeta x} )  (confronto coefficiente per coefficiente in s)
def apply_poly_op(coeffs, f):
    """a(d_x) f con a = sum coeffs[j] xi^j"""
    return sum(cj * sp.diff(f, x, j) for j, cj in enumerate(coeffs))


for label, coeffs in [("a_n = xi^2", [0, 0, 1]), ("a_n = -c xi + beta xi^3", [0, -c, 0, beta])]:
    an = sum(cj * zeta**j for j, cj in enumerate(coeffs))
    for l in (0, 1, 2):
        f = x**l * sp.exp(zeta * x)
        K = 5
        g = f
        series_coeffs = []
        for k in range(K + 1):
            series_coeffs.append(sp.expand(g / sp.factorial(k)))
            g = apply_poly_op(coeffs, g)
        closed = sp.diff(sp.exp(s * an) * sp.exp(zeta * x), zeta, l)
        closed_ser = sp.series(closed, s, 0, K + 1).removeO()
        okk = all(zero(closed_ser.coeff(s, k) - series_coeffs[k]) for k in range(K + 1))
        check(f"C1 P1-L2 serie = d_zeta^l(e^(s a_n)e^(zeta x)), {label}, l={l}, ordini s^0..s^{K}", okk)

# ---------------------------------------------------------------- C2
# P1-T2(v) identita' formale nel getto in t (ogni u0 liscio): u = sum_S prod_{n in S}(S_n - I) u0
f = sp.Function('f')(x)
ops = [[0, 0, D], [0, -c], [0, 0, 0, beta]]          # a_1 = D xi^2, a_2 = -c xi, a_3 = beta xi^3
atot = [0, -c, D, beta]
K = 4


def formal_exp(coeffs, h, order):
    out, g = 0, h
    for k in range(order + 1):
        out += t**k / sp.factorial(k) * g
        g = apply_poly_op(coeffs, g)
    return out


def trunc(e, order):
    e = sp.expand(e)
    return sum(e.coeff(t, k) * t**k for k in range(order + 1))


lhs = trunc(formal_exp(atot, f, K), K)
rhs = 0
for r in range(0, 4):
    for S in itertools.combinations(range(3), r):
        h = f
        for n in S:
            h = trunc(formal_exp(ops[n], h, K) - h, K)
        rhs += h
rhs = trunc(rhs, K)
check("C2 P1-T2(v) getto formale: u = sum_S prod(S_n-I)u0 fino a t^4, N=3, u0 = f(x) generica", zero(lhs - rhs))

# ---------------------------------------------------------------- C3
# P1-T2(ii) con molteplicita': g = d_zeta^2 (e^{t a(zeta)} e^{zeta x}) risolve u_t = a(d_x)u e
# E_add = d_zeta^2 [ e_{>=2}(z) e^{zeta x} ] (verifica: E = u - u0 - sum(u_n - u0) con u_n in forma chiusa)
a_list = [D * zeta**2, -c * zeta, beta * zeta**3]
a_sum = sum(a_list)
u = sp.diff(sp.exp(t * a_sum + zeta * x), zeta, 2)
check("C3a d_zeta^2(e^{t a + zeta x}) risolve u_t = (D d^2 - c d + beta d^3) u",
      zero(sp.diff(u, t) - apply_poly_op(atot, u)))
u0 = sp.diff(sp.exp(zeta * x), zeta, 2)
un = [sp.diff(sp.exp(t * an + zeta * x), zeta, 2) for an in a_list]
E = u - u0 - sum(v - u0 for v in un)
zs = [sp.exp(t * an) - 1 for an in a_list]
e_ge2 = sp.prod([1 + w for w in zs]) - 1 - sum(zs)
check("C3b E_add(x^2 e^{zeta x}) = d_zeta^2[e_{>=2}(z(zeta)) e^{zeta x}]",
      zero(E - sp.diff(e_ge2 * sp.exp(zeta * x), zeta, 2)))

# ---------------------------------------------------------------- C4
# P1-T3 aggregati per ordine via coefficienti di prod(1+lambda z_n) (O(N^2)) = forza bruta, N = 7
N = 7
zz = sp.symbols('z1:%d' % (N + 1))
lam = sp.Symbol('lam')
coef = [sp.Integer(1)] + [sp.Integer(0)] * N           # programmazione dinamica
for w in zz:
    new = coef[:]
    for k in range(1, N + 1):
        new[k] = coef[k] + w * coef[k - 1]
    coef = [sp.expand(q) for q in new]
brute = [sp.expand(sum(sp.prod(cm) for cm in itertools.combinations(zz, k))) for k in range(N + 1)]
check("C4a DP e_k = forza bruta per k = 0..7 (N = 7)", all(zero(coef[k] - brute[k]) for k in range(N + 1)))
nmon = len(sp.Add.make_args(sp.expand(sp.prod([1 + w for w in zz]) - 1 - sum(zz))))
check("C4b numero di coefficienti di Moebius |S|>=2 = 2^N - N - 1 = 120", nmon == 2**N - N - 1)

# ---------------------------------------------------------------- C5
# P1-E1: AD, dato stazionario e^{cx/D}: E_add = (e^{-theta}-1)(e^{theta}-1) e^{cx/D} = (2-2cosh theta) e^{cx/D}
zeta0 = c / D
a1, a2 = -c * zeta0, D * zeta0**2
uAD = sp.exp(t * (a1 + a2) + zeta0 * x)
check("C5a e^{cx/D} stazionaria (a(c/D) = 0)", zero(a1 + a2))
EAD = uAD - sp.exp(zeta0 * x) - (sp.exp(t * a1 + zeta0 * x) - sp.exp(zeta0 * x)) - (sp.exp(t * a2 + zeta0 * x) - sp.exp(zeta0 * x))
th = c**2 * t / D
check("C5b E_add = (2 - 2 cosh theta) e^{cx/D}, theta = c^2 t/D",
      zero(sp.expand((EAD - (2 - 2 * sp.cosh(th)) * sp.exp(zeta0 * x)).rewrite(sp.exp))))

# ---------------------------------------------------------------- C6
# P1-P6: fattore del 2o ordine; onda tau^2 - zeta^2: phi_1 = cosh(zeta t); zeri solo per |t| >= pi/(2|zeta|)
phi = sp.cosh(zeta * t)
check("C6a phi_1 = cosh(zeta t) risolve phi'' = zeta^2 phi, phi(0)=1, phi'(0)=0",
      zero(sp.diff(phi, t, 2) - zeta**2 * phi) and phi.subs(t, 0) == 1 and sp.diff(phi, t).subs(t, 0) == 0)
w = sp.Symbol('w')
sol = sp.solveset(sp.cosh(w), w, domain=sp.S.Complexes)
check("C6b zeri di cosh: w in i(pi/2 + pi Z) (quindi |t| >= pi/(2|zeta|))",
      all(sp.simplify(sp.cosh(sp.I * sp.pi / 2 + sp.I * sp.pi * k)) == 0 for k in range(-2, 3)) and sol != sp.S.EmptySet)
# bound esplicito: |phi_1 - 1| <= e^{|t| max(1, beta+gamma)} - 1; KG con zeta reale |zeta|<m: t* = pi/(2 sqrt(m^2-zeta^2))
m = sp.Integer(2)
for zv in [sp.Integer(0), sp.Rational(1), sp.Rational(3, 2)]:
    tstar = sp.pi / (2 * sp.sqrt(m**2 - zv**2))
    gam = abs(m**2 - zv**2)                    # c(zeta) = m^2 - zeta^2 per tau^2 - zeta^2 + m^2, b = 0
    T_lb = sp.log(2) / max(1, gam)
    check(f"C6c KG m=2, zeta={zv}: T*_bound = log2/max(1,gamma) <= t* = pi/(2 sqrt(m^2-zeta^2))", sp.N(T_lb - tstar) < 0)

# ---------------------------------------------------------------- C7
# P1-T4 (risolubile): OU, X1 = x d, X2 = d^2, [X1, X2] = -2 X2; Wei-Norman: e^{t(d^2 - x d)} = e^{-t x d} e^{g2 d^2},
# g2 = (1 - e^{-2t})/2. Verifica su x^n (n <= 6): U(t)x^n risolve u_t = u_xx - x u_x, U(0)x^n = x^n.
g2 = (1 - sp.exp(-2 * t)) / 2


def heat_flow(p, h):  # e^{h d^2} p per polinomio p (serie finita)
    out, q, j = 0, p, 0
    while q != 0:
        out += h**j / sp.factorial(j) * q
        q = sp.diff(q, x, 2)
        j += 1
    return sp.expand(out)


okWN = True
for n in range(0, 7):
    v = heat_flow(x**n, g2).subs(x, sp.exp(-t) * x)   # e^{-t x d} p(x) = p(e^{-t} x)
    okWN &= zero(sp.diff(v, t) - sp.diff(v, x, 2) + x * sp.diff(v, x)) and zero(v.subs(t, 0) - x**n)
check("C7a Wei-Norman OU: e^{-t x d} e^{g2 d^2} x^n risolve OU, n = 0..6 (g2 intera)", okWN)
X1 = lambda q: x * sp.diff(q, x)
X2 = lambda q: sp.diff(q, x, 2)
q = sp.Function('q')(x)
check("C7b [x d, d^2] = -2 d^2 (ideale span{d^2}: algebra risolubile)", zero(X1(X2(q)) - X2(X1(q)) + 2 * X2(q)))

# ---------------------------------------------------------------- C8
# P1-P5 (non risolubile): sl2, A = E - F, ordine di Gauss L D U: L_21 = -tan t (scoppia a t = pi/2)
Em = sp.Matrix([[0, 1], [0, 0]]); Fm = sp.Matrix([[0, 0], [1, 0]])
Phi = sp.simplify((t * (Em - Fm)).exp())
L21 = sp.simplify(Phi[1, 0] / Phi[0, 0])
check("C8 e^{t(E-F)} = rotazione, coordinata di Gauss L21 = -tan t (singolare in pi/2)",
      zero(Phi[0, 0] - sp.cos(t)) and zero(L21 + sp.tan(t)))

# ---------------------------------------------------------------- C9
# P1-T6 impossibilita': (a) orbita di ad_X su Y per X = x^a d, Y = d: gradi k(a-1), coefficienti non nulli
def vf_bracket(fa, fb):  # [fa d, fb d] = (fa fb' - fb fa') d
    return sp.expand(fa * sp.diff(fb, x) - fb * sp.diff(fa, x))


for a in (3, 4):
    orb, cur, okk = [], sp.Integer(1), True
    for k in range(8):
        orb.append(cur)
        okk &= (cur != 0) and sp.Poly(cur, x).degree() == k * (a - 1)
        cur = vf_bracket(x**a, cur)
    check(f"C9a X = x^{a} d, Y = d: ad_X^k Y = c_k x^(k(a-1)) d, c_k != 0, k = 0..7 (lin. indip., X fuori dallo span)", okk)
cur, okk = sp.Integer(1), False
for k in range(4):
    cur = vf_bracket(x**2, cur)
okk = (cur == 0)
check("C9b controllo: X = x^2 d (sl2) ha orbita finita di Y = d", okk)
# (b) termine di primo ordine in eps: e^{-tX} d_eps e^{t(X+eps Y)}|_0 = sum_k (-1)^k t^{k+1}/(k+1)! ad_X^k Y (matrici generiche)
Xm = sp.Matrix([[1, 2, 0], [0, -1, 1], [3, 0, 2]]); Ym = sp.Matrix([[0, 1, 1], [2, 0, 0], [1, -1, 0]])
eps = sp.Symbol('eps')
Ord = 6


def mexp_series(M, order):
    out, P = sp.eye(3), sp.eye(3)
    for k in range(1, order + 1):
        P = P * M / k
        out += P
    return out


lhsM = (mexp_series(-t * Xm, Ord) * sp.diff(mexp_series(t * (Xm + eps * Ym), Ord), eps).subs(eps, 0)).applyfunc(lambda e: trunc(e, Ord))
adk, rhsM = Ym, sp.zeros(3)
for k in range(Ord):
    rhsM += (-1)**k * t**(k + 1) / sp.factorial(k + 1) * adk
    adk = Xm * adk - adk * Xm
check("C9c d_eps e^{t(X+eps Y)} = e^{tX} sum (-1)^k t^{k+1}/(k+1)! ad_X^k Y (fino a t^6)",
      all(zero(e) for e in (lhsM - rhsM.applyfunc(lambda e: trunc(e, Ord)))))
# (c) Hankel dei momenti m_k = t^{k+1}/(k+1): det = t^{n^2} det(Hilbert_n) != 0  => nessuna somma finita sum q_i tau_i^k
okH = True
for n in range(1, 8):
    H = sp.Matrix(n, n, lambda i, j: t**(i + j + 1) / (i + j + 1))
    dH = sp.factor(H.det())
    okH &= zero(dH - t**(n * n) * sp.Matrix(n, n, lambda i, j: sp.Rational(1, i + j + 1)).det()) and dH != 0
check("C9d det Hankel[t^{i+j+1}/(i+j+1)]_{n} = t^{n^2} det Hilbert_n != 0, n = 1..7", okH)
q1, q2, T1, T2 = sp.symbols('q1 q2 tau1 tau2')
Hfin = sp.Matrix(3, 3, lambda i, j: q1 * T1**(i + j) + q2 * T2**(i + j))
check("C9e controllo: Hankel 3x3 di una somma di p = 2 esponenziali ha det = 0", zero(Hfin.det()))

# ---------------------------------------------------------------- C10
# P1-P7 (bordo): (a) M A M^{-1} = D d^2 - c^2/(4D) con M = e^{-cx/(2D)}; (b) risolvente del trasporto con inflow
wf = sp.Function('w')(x)
Aop = lambda v: D * sp.diff(v, x, 2) - c * sp.diff(v, x)
conj = sp.exp(-c * x / (2 * D)) * Aop(sp.exp(c * x / (2 * D)) * wf)
check("C10a e^{-cx/2D}(D d^2 - c d)(e^{cx/2D} w) = D w'' - c^2/(4D) w", zero(conj - (D * sp.diff(wf, x, 2) - c**2 / (4 * D) * wf)))
y, lamb = sp.symbols('y lamb', positive=True)
ff = sp.Function('ff')
Ru = sp.Integral(sp.exp(-lamb * (x - y) / c) * ff(y), (y, 0, x)) / c
check("C10b u = (1/c) int_0^x e^{-lam(x-y)/c} f(y) dy risolve lam u + c u' = f, u(0) = 0",
      zero(sp.simplify(lamb * Ru + c * sp.diff(Ru, x) - ff(x)).doit()) and Ru.subs(x, 0).doit() == 0)

print()
npass = sum(1 for _, r in RES if r)
print(f"ESITO: {npass}/{len(RES)} PASS")
