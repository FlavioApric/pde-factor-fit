"""F4-LIFT s1: Carleman per x' = lam x + beta x^2 (caso giocattolo).
Verifiche (solo controllo, V-ex):
 C1  y_1^N(t) del troncamento = polinomio di Taylor di grado N nel dato x0 del flusso esatto.
 C2  difetto di Veronese: sul troncato d/dt (y_N - y_1^N) = -N beta y_1^{N+1} quando y_k = y_1^k.
 C3  (x)^{N+1} e' D-stabile per D = F(x) d/dx  <=>  F(0) = 0  (test su F generico di grado 3).
 C4  matrice troncata = matrice di D su C[x]/(x^{N+1}) nella base x^k (k=1..N).
 C5  Dyson-Phillips con A0 = diag(k lam), V = sovradiagonale (k beta): termina all'ordine N-1 e
     il termine n-esimo (proiettato su y_1) = coefficiente di x0^{n+1} nel flusso esatto.
 C6  algebra di Lie di {D_lin, D_NL} su C[x]/(x^{N+1}) (N=4) per F = lam x + beta x^2 + g x^3: risolubile.
"""
import sympy as sp

t, lam, beta, x0, s = sp.symbols('t lambda beta x0 s')
ok = []

def carleman_matrix(N):
    M = sp.zeros(N, N)
    for k in range(1, N + 1):
        M[k-1, k-1] = k*lam
        if k < N:
            M[k-1, k] = k*beta
    return M

# esatto: x(t) = lam x0 e^{lam t} / (lam + beta x0 (1 - e^{lam t}))
def tri_solve(N, L, B, extra_top=0):
    """risolve il sistema bidiagonale troncato per back-substitution (L, B numeri razionali)."""
    s_ = sp.Symbol('s_')
    y = [None]*(N+2)
    y[N+1] = 0
    for k in range(N, 0, -1):
        inner = sp.expand(sp.exp(-k*L*s_)*(y[k+1].subs(t, s_) if y[k+1] != 0 else 0))
        y[k] = sp.expand(sp.exp(k*L*t)*(x0**k + k*B*sp.integrate(inner, (s_, 0, t))))
    return y
for (L, B) in [(-1, 1), (2, -3)]:
    xex_n = L*x0*sp.exp(L*t)/(L + B*x0*(1 - sp.exp(L*t)))
    assert sp.simplify(sp.diff(xex_n, t) - (L*xex_n + B*xex_n**2)) == 0
    for N in range(1, 6):
        y = tri_solve(N, L, B)
        taylor = sp.series(xex_n, x0, 0, N+1).removeO()
        c1 = sp.simplify(sp.expand(y[1] - taylor)) == 0
        ok.append(('C1 lam=%s beta=%s N=%d' % (L, B, N), c1))
xex = lam*x0*sp.exp(lam*t)/(lam + beta*x0*(1 - sp.exp(lam*t)))
# C2
for N in range(2, 6):
    y = sp.symbols('y1:%d' % (N+2))
    rhs = [ (k+1)*lam*y[k] + ((k+1)*beta*y[k+1] if k+1 < N else 0) for k in range(N)]
    # d/dt (y_N - y_1^N) lungo il troncato
    d = rhs[N-1] - N*y[0]**(N-1)*rhs[0]
    d_on_ver = sp.expand(d.subs({y[k]: y[0]**(k+1) for k in range(1, N)}))
    ok.append(('C2 N=%d' % N, sp.simplify(d_on_ver + N*beta*y[0]**(N+1)) == 0))

# C3
x, f0, f1, f2, f3 = sp.symbols('x f0 f1 f2 f3')
F = f0 + f1*x + f2*x**2 + f3*x**3
for N in range(1, 5):
    Dx = sp.expand(F*sp.diff(x**(N+1), x))
    rem = sp.Poly(Dx, x).rem(sp.Poly(x**(N+1), x)).as_expr()
    # stabile iff rem == 0 ; rem = (N+1) f0 x^N
    ok.append(('C3 N=%d' % N, sp.simplify(rem - (N+1)*f0*x**N) == 0))

# C4: D su C[x]/(x^{N+1}) nella base x^1..x^N (F(0)=0): D x^k = k lam x^k + k beta x^{k+1}
for N in range(1, 6):
    Mq = sp.zeros(N, N)
    for k in range(1, N+1):
        img = sp.Poly(sp.expand((lam*x + beta*x**2)*k*x**(k-1)), x)
        for j in range(1, N+1):
            Mq[k-1, j-1] = img.coeff_monomial(x**j)
    ok.append(('C4 N=%d' % N, Mq == carleman_matrix(N)))

# C5 Dyson-Phillips (lam=-1, beta=1): S0 diagonale, V sovradiagonale nilpotente
L, B = -1, 1
xex_n = L*x0*sp.exp(L*t)/(L + B*x0*(1 - sp.exp(L*t)))
N = 4
A0 = sp.diag(*[k*L for k in range(1, N+1)])
V = sp.zeros(N, N)
for k in range(1, N):
    V[k-1, k] = k*B
S0 = lambda tau: sp.diag(*[sp.exp(k*L*tau) for k in range(1, N+1)])
terms = [S0(t)]
for n in range(1, N+1):
    s_ = sp.Symbol('s_')
    prevm = terms[-1].subs(t, s_)
    integrand = S0(t - s_)*V*prevm
    terms.append(integrand.applyfunc(lambda e: sp.expand(sp.integrate(sp.expand(e), (s_, 0, t)))))
Y0 = sp.Matrix([x0**k for k in range(1, N+1)])
ok.append(('C5 termina (termine N nullo)', terms[N] == sp.zeros(N, N)))
for n in range(0, N):
    proj = sp.expand((terms[n]*Y0)[0])
    coeff = sp.expand(sp.series(xex_n, x0, 0, n+2).removeO().coeff(x0, n+1)*x0**(n+1))
    ok.append(('C5 termine Dyson n=%d = coeff x0^%d' % (n, n+1), sp.simplify(proj - coeff) == 0))

# C6 Lie algebra su jet: derivazioni f(x) d/dx mod x^{N+1}, rappresentate dal polinomio f (f(0)=0)
N = 4
g = sp.symbols('g')
def br(f, h):  # [f d, h d] = (f h' - h f') d
    return sp.expand(f*sp.diff(h, x) - h*sp.diff(f, x))
def trunc(f):  # azione su C[x]/(x^{N+1}): contano solo i termini x^j con j <= N
    p = sp.Poly(f, x)
    return sum(p.coeff_monomial(x**j)*x**j for j in range(1, N+1))
Dl, Dn = lam*x, beta*x**2 + g*x**3
basis = []
def add(v):
    v = trunc(v)
    if v == 0:
        return False
    vecs = [[sp.Poly(b, x).coeff_monomial(x**j) for j in range(1, N+1)] for b in basis+[v]]
    if sp.Matrix(vecs).rank() > len(basis):
        basis.append(v); return True
    return False
add(Dl); add(Dn)
changed = True
while changed:
    changed = False
    for a in list(basis):
        for b in list(basis):
            if add(br(a, b)):
                changed = True
dimg = len(basis)
# serie derivata
def span_rank(vs):
    vs = [trunc(v) for v in vs if trunc(v) != 0]
    if not vs: return 0
    return sp.Matrix([[sp.Poly(v, x).coeff_monomial(x**j) for j in range(1, N+1)] for v in vs]).rank()
d1 = [br(a, b) for a in basis for b in basis]
d2 = [br(a, b) for a in d1 for b in d1]
d3 = [br(a, b) for a in d2 for b in d2]
ok.append(('C6 dim g_N=%d, rank derivate %d,%d,%d (risolubile se ->0)' % (dimg, span_rank(d1), span_rank(d2), span_rank(d3)),
           span_rank(d3) == 0))

for name, v in ok:
    print(('PASS ' if v else 'FAIL ') + name)
print('totale %d/%d' % (sum(v for _, v in ok), len(ok)))
