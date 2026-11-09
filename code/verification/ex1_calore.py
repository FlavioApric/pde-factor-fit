# S5-EX · E1 equazione del calore P = tau - xi^2 (e (tau - xi^2)^2) contro C3-T1/T4/T6/T3/C2, P4-T2
# Eseguire: D:\ProblemaBase\.venv\Scripts\python.exe -I ex1_calore.py
import itertools
import sympy as sp
import sys
sys.stdout.reconfigure(encoding="utf-8")

t, x = sp.symbols('t x', positive=True)
tau, xi = sp.symbols('tau xi')
RES = []


def check(name, cond, info=''):
    RES.append((name, bool(cond)))
    print(('[OK]   ' if cond else '[FAIL] ') + name + ((' :: ' + str(info)) if info != '' else ''))


def der(u, i, j):
    for _ in range(i):
        u = sp.diff(u, t)
    for _ in range(j):
        u = sp.diff(u, x)
    return u


def apply(Q, u):
    Q = sp.Poly(sp.expand(Q), tau, xi)
    return sp.expand(sum(c * der(u, i, j) for (i, j), c in Q.terms()))


def mons(n):
    return [(i, k - i) for k in range(n + 1) for i in range(k + 1)]


def generic(n, name='c'):
    ms = mons(n)
    cs = sp.symbols(f'{name}0:{len(ms)}')
    return sum(c * tau**i * xi**j for c, (i, j) in zip(cs, ms)), list(cs), ms


def nullspace_polys(eqs, cs, ms):
    """sottospazio di R_{<=n} soluzione del sistema lineare eqs=0 nei coefficienti cs"""
    if not eqs:
        M = sp.zeros(0, len(cs))
    else:
        M = sp.Matrix([[sp.diff(e, c) for c in cs] for e in eqs])
    ns = M.nullspace()
    return [sp.expand(sum(v[k] * tau**i * xi**j for k, (i, j) in enumerate(ms))) for v in ns]


def coeff_eqs_EP(expr, extra_syms=()):
    """expr = somma di polinomi(t,x) * exp(lineare): equazioni 'tutti i coefficienti nulli'"""
    expr = sp.expand(sp.powsimp(sp.expand(expr)))
    exps = sorted({a for a in expr.atoms(sp.exp)}, key=str)
    Es = sp.symbols(f'E0:{len(exps)}')
    e2 = expr.xreplace(dict(zip(exps, Es)))
    P = sp.Poly(e2, t, x, *Es)
    return [c for c in P.coeffs()]


def ann_EP(u, n):
    Q, cs, ms = generic(n)
    return nullspace_polys(coeff_eqs_EP(apply(Q, u)), cs, ms), (cs, ms)


def ann_jet(u, n, k, p0):
    Q, cs, ms = generic(n)
    w = apply(Q, u)
    eqs = []
    for (i, j) in mons(k):
        eqs.append(sp.expand(der(w, i, j).subs({t: p0[0], x: p0[1]})))
    return nullspace_polys(eqs, cs, ms)


def span_dim(polys, n):
    ms = mons(n)
    if not polys:
        return 0
    M = sp.Matrix([[sp.Poly(p, tau, xi).coeff_monomial(tau**i * xi**j) for (i, j) in ms] for p in polys])
    return M.rank()


def same_span(A, B, n):
    return span_dim(A, n) == span_dim(B, n) == span_dim(A + B, n)


def ideal_trunc(gens, n):
    out = []
    for g in gens:
        dg = sp.Poly(g, tau, xi).total_degree()
        for (i, j) in mons(n - dg) if n - dg >= 0 else []:
            out.append(sp.expand(g * tau**i * xi**j))
    return out


def quot_dim(gens, bound=12):
    G = sp.groebner(gens, tau, xi, order='grevlex')
    if list(G.exprs) == [1]:
        return 0
    LM = [sp.Poly(g, tau, xi).monoms(order='grevlex')[0] for g in G.exprs]
    cnt = 0
    for (i, j) in mons(bound):
        if not any(i >= a and j >= b for (a, b) in LM):
            cnt += 1
    # controllo di zero-dimensionalita': nessun monomio standard di grado = bound
    top = [(i, j) for (i, j) in mons(bound) if i + j == bound and not any(i >= a and j >= b for (a, b) in LM)]
    return cnt if not top else None


def dimRu_EP(u, kmax=10):
    """dim R.u per u EP: rango della famiglia delle derivate fino all'ordine kmax"""
    ders = [sp.expand(der(u, i, j)) for (i, j) in mons(kmax)]
    cs = sp.symbols(f'a0:{len(ders)}')
    eqs = coeff_eqs_EP(sum(c * d for c, d in zip(cs, ders)))
    M = sp.Matrix([[sp.diff(e, c) for c in cs] for e in eqs])
    return M.rank()


P = tau - xi**2
G = t**sp.Rational(-1, 2) * sp.exp(-x**2 / (4 * t))
p0 = (sp.Rational(1, 2), sp.Rational(1, 3))

print('== E1.1 nucleo del calore G: non EP, identifica (C3-T4(a), C3-T1(d)) ==')
check('E1.1a P(d)G = 0', sp.simplify(apply(P, G)) == 0)
degs = [sp.Poly(sp.simplify(der(G, 0, k) / G), x).degree() for k in range(11)]
check('E1.1b deg_x(d_x^k G / G) = k, k<=10 => dim R.G = inf => G non EP (C3-L3(e))', degs == list(range(11)), degs)


def ann_nonEP(parts, n):
    """u = sum f_i * h_i con h_i 'base' indipendenti su C(t,x): parts = [(f_i, h_i)]"""
    Q, cs, ms = generic(n)
    eqs = []
    for f, h in parts:
        r = sp.together(sp.simplify(apply(Q, f * h) / h))
        num = sp.numer(r)
        eqs += sp.Poly(sp.expand(num), t, x).coeffs()
    return nullspace_polys(eqs, cs, ms)


for n in (2, 3, 4):
    A = ann_nonEP([(1, G)], n)
    check(f'E1.1c Ann(G) ∩ R_<={n} = P·R_<={n-2} (identificazione, C3-T4(a))', same_span(A, ideal_trunc([P], n), n), f'dim {len(A)}')

print('== E1.2 molteplicita: P = (tau-xi^2)^2 (C3-T1(a), C3-T6) ==')
P2 = P**2
u = t * G
check('E1.2a P2(d)(tG) = 0', sp.simplify(apply(P2, u)) == 0)
w = sp.simplify(apply(P, u))
check('E1.2b (P2/P1)(d)(tG) = G (non EP) => Ann(tG) = (P2)', sp.simplify(w - G) == 0)
for n in (4, 5):
    A = ann_nonEP([(t, G)], n)
    check(f'E1.2c Ann(tG) ∩ R_<={n} = P2·R_<={n-4}', same_span(A, ideal_trunc([P2], n), n), f'dim {len(A)}')
# G con P2: S_1 = {0,1} -> f_1 = 1 -> G_u = P
check('E1.2d C3-T6 per u=G, P=P2: (P2/P1)G = 0 ∈ EP, (P2/P1^2)G = G ∉ EP => G_u = tau-xi^2',
      sp.simplify(apply(P, G)) == 0)
# u = G + t e^{t+x}: G_u = P, J_u = (tau-1, xi-1)
u = G + t * sp.exp(t + x)
check('E1.2e P2(d)(G + t e^{t+x}) = 0', sp.simplify(apply(P2, u)) == 0)
wv = sp.simplify(apply(P, u))
check('E1.2f (P2/P1)u = e^{t+x} ∈ EP => non identifica P2 (C3-T1(a))', sp.simplify(wv - sp.exp(t + x)) == 0)
pred = [sp.expand(P * (tau - 1)), sp.expand(P * (xi - 1))]
for n in (3, 4):
    Q, cs, ms = generic(n)
    eqs = []
    r1 = sp.numer(sp.together(sp.simplify(apply(Q, G) / G)))
    eqs += sp.Poly(sp.expand(r1), t, x).coeffs()
    r2 = sp.numer(sp.together(sp.simplify(apply(Q, t * sp.exp(t + x)) / sp.exp(t + x))))
    eqs += sp.Poly(sp.expand(r2), t, x).coeffs()
    A = nullspace_polys(eqs, cs, ms)
    check(f'E1.2g Ann(G+te^(t+x)) ∩ R_<={n} = [G_u·J_u]_<={n}, G_u = tau-xi^2, J_u = (tau-1, xi-1) (C3-T6, P4-T2)',
          same_span(A, ideal_trunc(pred, n), n), f'dim {len(A)}')
check('E1.2h P4-T2: sigma_p = V(J_u) = {(1,1)}: w = G_u(d)u = e^{t+x} autovettore congiunto',
      sp.simplify(sp.diff(wv, t) - wv) == 0 and sp.simplify(sp.diff(wv, x) - wv) == 0)
check('E1.2i P4-T2(iii): dim(R·u ∩ EP) = dim R/J_u = 1', quot_dim([tau - 1, xi - 1]) == 1)

print('== E1.3 dati EP: C3-C2 (mai identificazione), C3-T3 (jet 2d-1), P4-T2 (G_u = 1) ==')
EPs = {
    'x^2+2t': x**2 + 2 * t,
    'x^3+6tx': x**3 + 6 * t * x,
    'e^{-4t}sin 2x': sp.exp(-4 * t) * (sp.exp(2 * sp.I * x) - sp.exp(-2 * sp.I * x)) / (2 * sp.I),
    '(x^2+2t)+e^{t+x}': x**2 + 2 * t + sp.exp(t + x),
    'e^{t+x}+e^{4t+2x}+e^{9t+3x}': sp.exp(t + x) + sp.exp(4 * t + 2 * x) + sp.exp(9 * t + 3 * x),
}
for name, u in EPs.items():
    check(f'E1.3a [{name}] P(d)u = 0', sp.simplify(apply(P, u)) == 0)
    d = dimRu_EP(u)
    A_d, _ = ann_EP(u, d)
    qd = quot_dim(A_d)
    check(f'E1.3b [{name}] d = dim R·u = {d}; Ann generato in grado <= d: dim R/(Ann_<=d) = d (C3-T3(ii))', qd == d, f'quot_dim={qd}')
    A_jet = ann_jet(u, d, d - 1, p0)
    check(f'E1.3c [{name}] jet di ordine 2d-1 = {2*d-1} in p0 ricostruisce Ann_<=d (C3-T3(i)-(ii))', same_span(A_jet, A_d, d))
    A_jet2 = ann_jet(u, d, d - 2, p0) if d >= 2 else None
    if A_jet2 is not None:
        print(f'       [info] [{name}] jet di ordine 2d-2: dim nucleo {len(A_jet2)} vs dim Ann_<=d {len(A_d)}'
              f' ({"basta già" if len(A_jet2) == len(A_d) else "non basta"}; C3-T3(iii) è solo nel caso peggiore)')
    # C3-C2: esiste Q in Ann, P non divide Q
    notmult = [q for q in A_d if sp.rem(sp.Poly(q, tau), sp.Poly(P, tau)).as_expr() != 0]
    check(f'E1.3d [{name}] C3-C2: Ann(u) ≠ (P) (esiste Q ∈ Ann_<=d non multiplo di P)', len(notmult) > 0)
    # P4-T2: G_u = 1 per EP: gcd di Ann_<=d è costante
    g = sp.Poly(sp.gcd_list(A_d), tau, xi) if len(A_d) > 1 else sp.Poly(A_d[0], tau, xi)
    check(f'E1.3e [{name}] P4-T2(v)(b): u EP => G_u = gcd Ann = 1, sigma_p = V(Ann) finito', g.total_degree() == 0)

print('== E1.4 C3-T4(b): u = (x^2+2t)+e^{t+x}, D = 4: tau-b ∈ Ann con deg b <= n unico per n <= 3 ==')
u = x**2 + 2 * t + sp.exp(t + x)
for n in range(1, 6):
    bs = sp.symbols(f'b0:{n+1}')
    b = sum(c * xi**k for k, c in enumerate(bs))
    eqs = coeff_eqs_EP(apply(tau - b, u))
    sol = sp.linsolve(eqs, bs)
    sol = list(sol)
    dimsol = len(sol[0].free_symbols) if sol else -1
    if n < 2:
        print(f'       [info] E1.4 n={n}: fuori dalla ipotesi essenziale deg a = 2 <= n di C3-T4(b); osservato: insieme vuoto (dim {dimsol})')
        continue
    pred = 0 if n <= 3 else n + 1 - 4
    check(f'E1.4 n={n}: dim affine soluzioni = {dimsol}, predetto {pred}', dimsol == pred)

nok = sum(1 for _, ok in RES if ok)
print(f'\nTOTALE E1: {nok}/{len(RES)} OK')
