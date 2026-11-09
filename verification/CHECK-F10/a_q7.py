# S-CHECK-F10-A: verifica indipendente di S10A-T2 (P1-Q7)
import sympy as sp

ok = 0; tot = 0
def chk(name, cond):
    global ok, tot
    tot += 1
    if cond: ok += 1
    print(("OK   " if cond else "FAIL ") + name)

s, nu, e0 = sp.symbols('s nu epsilon0')

# (1) Hankel dei momenti destri m_k = e0 s^{k+1}/(k+1): det = e0^n s^{n^2} det Hilb_n != 0
for n in range(1, 7):
    H = sp.Matrix(n, n, lambda i, j: e0*s**(i+j+1)/(i+j+1))
    Hil = sp.Matrix(n, n, lambda i, j: sp.Rational(1, i+j+1))
    good = sp.simplify(H.det() - e0**n*s**(n*n)*Hil.det()) == 0 and Hil.det() != 0
    chk(f"Hankel destro n={n}: det = e0^n s^(n^2) det Hilb_n, non nullo", good)

# (2) Hankel sinistro da p nodi: m_k = sum_i q_i tau_i^k, n = p+1 => det identicamente nullo
for p in range(1, 4):
    q = sp.symbols(f'q1:{p+1}'); tau = sp.symbols(f't1:{p+1}')
    n = p + 1
    H = sp.Matrix(n, n, lambda i, j: sum(q[l]*tau[l]**(i+j) for l in range(p)))
    chk(f"Hankel sinistro p={p}: det identicamente nullo", sp.expand(H.det()) == 0)

# (3) kill-argument: con p nodi i vincoli k = 0..2p-1 SONO risolubili (quadratura di Gauss su [0,s]),
#     il vincolo k = 2p no. Quindi la prova usa (H) solo fino a Y_{2p}, ed e' ottimale in questo senso.
for p in (1, 2, 3):
    xs, ws = [], []
    P = sp.legendre(p, sp.Symbol('y'))
    roots = sp.Poly(P, sp.Symbol('y')).nroots(n=40)
    for rt in roots:
        y = sp.nsimplify(rt) if p == 1 else rt
        xs.append(s*(1 + y)/2)
        dP = sp.diff(P, sp.Symbol('y')).subs(sp.Symbol('y'), rt)
        ws.append(s/2 * 2/((1 - rt**2)*dP**2))
    res = [sp.N(sp.expand(sum(w*xx**k for w, xx in zip(ws, xs)) - s**(k+1)/(k+1)).subs(s, 1), 25)
           for k in range(2*p+1)]
    good = all(abs(v) < 1e-20 for v in res[:2*p]) and abs(res[2*p]) > 1e-6
    chk(f"Gauss p={p}: momenti k<2p esatti, k=2p no (residuo {sp.N(res[2*p],4)})", good)

# (4) Weyl A_1: sigma(x) = mu x, sigma(d) = d/mu realizzato da T g(x) = g(mu x), su funzioni test concrete
xx, mu = sp.symbols('x mu', positive=True)
tests = [sp.exp(xx)*sp.sin(2*xx), xx**7 + 3*xx**2 + 1, sp.cos(xx**2)]
Tinv = lambda g: g.subs(xx, xx/mu)
T = lambda g: g.subs(xx, mu*xx)
for a in (3, 4):
    c1 = all(sp.simplify(T(xx**a*sp.diff(Tinv(g), xx)) - mu**(a-1)*xx**a*sp.diff(g, xx)) == 0 for g in tests)
    c2 = all(sp.simplify(T(sp.diff(Tinv(g), xx)) - sp.diff(g, xx)/mu) == 0 for g in tests)
    # sigma(d) sigma(x) - sigma(x) sigma(d) = id  (sigma x = mu x, sigma d = d/mu)
    c3 = all(sp.simplify(sp.diff(mu*xx*g, xx)/mu - mu*xx*sp.diff(g, xx)/mu - g) == 0 for g in tests)
    chk(f"Weyl a={a}: sigma X = mu^(a-1) X, sigma Y = mu^-1 Y, [d,x]=1 preservato", c1 and c2 and c3)

# (5) Passi 0-3 in un'algebra libera troncata: parola Y X Y X, alpha = 1, beta = -1 (a = 2).
#     Si verifica che il coefficiente di nu^a del prodotto riscalato coincide con
#     r X e^{sX} + sum_i q_i e^{G_i X} Y e^{(s-G_i)X}, troncando a s^3, con tempi generici.
X, Y = sp.symbols('X Y', commutative=False)
ORD = 3
def trunc_s(expr, n=ORD):
    expr = sp.expand(expr)
    return sum(expr.coeff(s, k)*s**k for k in range(n+1))
def expo(h, Z):
    out = 1; term = 1
    for k in range(1, ORD+1):
        term = trunc_s(term*h*Z)/1
        out += term/sp.factorial(k)
        term = term  # potenze accumulate
    # ricostruzione corretta: sum (hZ)^k/k!
    out = 1; pw = 1
    for k in range(1, ORD+1):
        pw = trunc_s(pw*(h*Z))
        out += pw/sp.factorial(k)
    return sp.expand(out)
alpha, beta = 1, -1; aa = alpha - beta
word = [Y, X, Y, X]
g = [[sp.Symbol(f'g{i}_{k}') for k in range(1, ORD+1)] for i in range(len(word))]
h = []
for i, Z in enumerate(word):
    w = alpha if Z == X else beta
    h.append(sum(g[i][k-1]*nu**(alpha*k - w)*s**k for k in range(1, ORD+1)))
# esponenti in nu: >= 0 per X, >= a per Y
chk("valutazioni in nu: X >= 0, Y >= a",
    all(sp.Poly(h[i], nu).monoms()[-1][0] >= (0 if word[i] == X else aa) for i in range(len(word))))
prod = 1
for i, Z in enumerate(word):
    prod = trunc_s(sp.expand(prod*expo(h[i], Z)))
coef_rhs = sp.expand(prod).coeff(nu, aa)
H0 = sum(h[i].subs(nu, 0) for i in range(len(word)) if word[i] == X)
rH = sum(sp.expand(h[i]).coeff(nu, aa) for i in range(len(word)) if word[i] == X)
pred = 0
# termine (alpha): coefficiente di nu^a di e^{H X} (fattori X commutano) = d/dnu^a di exp(H X)
Hfull = sum(h[i] for i in range(len(word)) if word[i] == X)
pred += sp.expand(expo(Hfull, X)).coeff(nu, aa)
for i, Z in enumerate(word):
    if Z == Y:
        qi = sp.expand(h[i]).coeff(nu, aa)
        Gi = sum(h[j].subs(nu, 0) for j in range(i) if word[j] == X)
        pred += trunc_s(sp.expand(expo(Gi, X)*qi*Y*expo(H0 - Gi, X)))
chk("Passo 3: coeff. di nu^a = [e^{HX}]_a + sum_i q_i e^{G_iX} Y e^{(H0-G_i)X} (nessun termine misto)",
    sp.expand(trunc_s(coef_rhs) - trunc_s(pred)) == 0)

print(f"{ok}/{tot} OK")
