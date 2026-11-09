# S5-EX · E3 calore x trasporto: P = (tau - xi^2)(tau + c xi)  (e (tau-xi^2)(tau-xi^2-1), varieta' disgiunte)
# Teoremi: C12-T1'(i)-(iii) (delta(P), ambiguita' EP), C3-T1(a,d), C3-T6, P4-T2
# Eseguire: D:\ProblemaBase\.venv\Scripts\python.exe -I ex3_due_fattori.py
import sys
import sympy as sp

sys.stdout.reconfigure(encoding='utf-8')
t, x = sp.symbols('t x', positive=True)
tau, xi = sp.symbols('tau xi')
c = sp.Integer(2)          # velocita' di trasporto (valore concreto per l'algebra lineare esatta)
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
    return sp.expand(sum(cf * der(u, i, j) for (i, j), cf in Q.terms()))


def mons(n):
    return [(i, k - i) for k in range(n + 1) for i in range(k + 1)]


def generic(n):
    ms = mons(n)
    cs = sp.symbols(f'c0:{len(ms)}')
    return sum(cf * tau**i * xi**j for cf, (i, j) in zip(cs, ms)), list(cs), ms


def nullspace_polys(eqs, cs, ms):
    M = sp.Matrix([[sp.diff(e, cf) for cf in cs] for e in eqs])
    return [sp.expand(sum(v[k] * tau**i * xi**j for k, (i, j) in enumerate(ms))) for v in M.nullspace()]


def span_dim(polys, n):
    ms = mons(n)
    if not polys:
        return 0
    return sp.Matrix([[sp.Poly(p, tau, xi).coeff_monomial(tau**i * xi**j) for (i, j) in ms] for p in polys]).rank()


def same_span(A, B, n):
    return span_dim(A, n) == span_dim(B, n) == span_dim(A + B, n)


def ideal_trunc(gens, n):
    out = []
    for g in gens:
        dg = sp.Poly(g, tau, xi).total_degree()
        if n - dg >= 0:
            out += [sp.expand(g * tau**i * xi**j) for (i, j) in mons(n - dg)]
    return out


def quot_dim(gens, bound=12):
    G = sp.groebner(gens, tau, xi, order='grevlex')
    if list(G.exprs) == [1]:
        return 0
    LM = [sp.Poly(g, tau, xi).monoms(order='grevlex')[0] for g in G.exprs]
    std = [(i, j) for (i, j) in mons(bound) if not any(i >= a_ and j >= b_ for (a_, b_) in LM)]
    return None if any(i + j == bound for (i, j) in std) else len(std)


def ann_parts(parts, n):
    """u = sum f_k*h_k, h_k 'basi' linearmente indipendenti su C(t,x) (gaussiane distinte, esponenziali)."""
    Q, cs, ms = generic(n)
    eqs = []
    for f, h in parts:
        r = sp.numer(sp.together(sp.simplify(apply(Q, f * h) / h)))
        eqs += sp.Poly(sp.expand(r), t, x).coeffs()
    return nullspace_polys(eqs, cs, ms)


Q1, Q2 = tau - xi**2, tau + c * xi
P = sp.expand(Q1 * Q2)
G = t**sp.Rational(-1, 2) * sp.exp(-x**2 / (4 * t))

print('== E3.1 C12-T1\'(ii): delta(P) = dim R/(Q1,Q2) e ambiguita\' N = ker Q1 ∩ ker Q2 ==')
dl = quot_dim([Q1, Q2])
check('E3.1a delta(P) = dim C[tau,xi]/(tau-xi^2, tau+c xi) = 2', dl == 2, dl)
pts = sp.solve([Q1, Q2], [tau, xi], dict=True)
check('E3.1b V(Q1) ∩ V(Q2) = {(0,0), (c^2,-c)} (punti semplici)', {(p_[tau], p_[xi]) for p_ in pts} == {(0, 0), (c**2, -c)})
N = [sp.Integer(1), sp.exp(c**2 * t - c * x)]
check('E3.1c N = span{1, e^{c^2 t - c x}}: entrambe in ker Q1 ∩ ker Q2', all(apply(Q1, w) == 0 and apply(Q2, w) == 0 for w in N))
# ker Q1 ∩ ker Q2 contiene solo questi tra gli EP di dimensione bassa: Ann(w) ⊇ (Q1,Q2) => w ∈ Sol(R/(Q1,Q2)), dim = 2
check('E3.1d dim Sol(R/(Q1,Q2)) = dim R/(Q1,Q2) = 2 = numero di generatori trovati (C12-L2)', dl == len(N))

print('== E3.2 C12-T1\'(i): scomposizione di u = G + f(x-ct) (f gaussiana) ==')
fG = sp.exp(-(x - c * t)**2)
u = G + fG
check('E3.2a P(d)u = 0', sp.simplify(apply(P, u)) == 0)
al, be = sp.symbols('alpha beta')
u1 = G + al + be * N[1]
u2 = fG - al - be * N[1]
check('E3.2b u1 = G + alpha + beta e^{c^2t-cx} ∈ ker Q1, u2 ∈ ker Q2, u1+u2 = u, per ogni (alpha,beta): famiglia di dim delta = 2',
      sp.simplify(apply(Q1, u1)) == 0 and sp.simplify(apply(Q2, u2)) == 0 and sp.simplify(u1 + u2 - u) == 0)
check('E3.2c dalla sola u: Q2(d)u1 = Q2(d)u (u1 determinata a meno di ker Q1 ∩ ker Q2)',
      sp.simplify(apply(Q2, u1) - apply(Q2, u)) == 0)

print('== E3.3 C12-T1\'(iii): varieta\' disgiunte, P = (tau-xi^2)(tau-xi^2-1): delta = 0, proiettori espliciti ==')
R1, R2 = tau - xi**2, tau - xi**2 - 1
check('E3.3a (R1,R2) = R: delta = 0', quot_dim([R1, R2]) == 0)
v = G + sp.exp(t) * G + (x**2 + 2 * t) + sp.exp(t) * (x**2 + 2 * t)
check('E3.3b P(d)v = 0', sp.simplify(apply(sp.expand(R1 * R2), v)) == 0)
v1 = -apply(R2, v)      # R1 - R2 = 1  =>  v = R1 v - R2 v, con -R2 v ∈ ker R1, R1 v ∈ ker R2
v2 = apply(R1, v)
check('E3.3c componenti uniche: -R2(d)v = G + x^2+2t ∈ ker R1, R1(d)v = e^t(G + x^2+2t) ∈ ker R2',
      sp.simplify(v1 - G - x**2 - 2 * t) == 0 and sp.simplify(v2 - sp.exp(t) * (G + x**2 + 2 * t)) == 0)

print('== E3.4 C3-T1(a): u = G + f(x-ct) identifica P (w_i ∉ EP) ==')
w1 = sp.simplify(apply(Q2, u))     # (P/P1)u = (tau + c xi)u
w2 = sp.simplify(apply(Q1, u))     # (P/P2)u = (tau - xi^2)u
d1 = [sp.Poly(sp.simplify(der(w1, 0, k) / G), x).degree() for k in range(6)]
check('E3.4a w_1 = (d_t + c d_x)G: deg_x(d_x^k w_1 / G) = k+2 strettamente crescente => w_1 ∉ EP', d1 == [k + 2 for k in range(6)], d1)
d2 = [sp.Poly(sp.simplify(der(w2, 0, k) / fG), x).degree() for k in range(6)]
check('E3.4b w_2 = (d_t - d_x^2) f(x-ct): deg_x(d_x^k w_2 / f) = k+2 => w_2 ∉ EP', d2 == [k + 2 for k in range(6)], d2)
for n in (2, 3, 4):
    A = ann_parts([(1, G), (1, fG)], n)
    check(f'E3.4c Ann(u) ∩ R_<={n} = P·R_<={n-3} (osservato: identificazione)', same_span(A, ideal_trunc([P], n), n), f'dim {len(A)}')

print('== E3.5 C3-T1(a,d), C3-T6, P4-T2: u = G + e^{x-ct} non identifica ==')
u = G + sp.exp(x - c * t)
check('E3.5a P(d)u = 0', sp.simplify(apply(P, u)) == 0)
w2 = sp.simplify(apply(Q1, u))
check('E3.5b w_2 = (P/P_2)(d)u = (tau-xi^2)u = (-c-1) e^{x-ct} ∈ EP', sp.simplify(w2 - (-c - 1) * sp.exp(x - c * t)) == 0)
Qw = sp.expand((xi - 1) * Q1)
check('E3.5c testimone di C3-T1(a,=>): Q = (xi-1)(tau-xi^2) ∈ Ann(u), P ∤ Q', sp.simplify(apply(Qw, u)) == 0 and sp.rem(sp.Poly(Qw, tau), sp.Poly(P, tau)).as_expr() != 0)
b1, b0 = xi - 1, -xi**2 * (xi - 1)
rel = sp.simplify(apply(b1, sp.diff(u, t)) + apply(b0, u))
check('E3.5d C3-T1(d) (P monico in tau, m=2): relazione non banale b1(d_x)u_t + b0(d_x)u = 0, b1 = xi-1, b0 = -xi^2(xi-1)', rel == 0)
pred = [sp.expand(Q1 * (tau + c)), sp.expand(Q1 * (xi - 1))]
for n in (3, 4):
    A = ann_parts([(1, G), (1, sp.exp(x - c * t))], n)
    check(f'E3.5e Ann(u) ∩ R_<={n} = [G_u·J_u]_<={n} con G_u = tau-xi^2 (C3-T6: f_2 = 0), J_u = (tau+c, xi-1)', same_span(A, ideal_trunc(pred, n), n), f'dim {len(A)}')
check('E3.5f P ∈ G_u·J_u (P = G_u·((tau+c) + c(xi-1)))', sp.expand(P - Q1 * ((tau + c) + c * (xi - 1))) == 0)
check('E3.5g P4-T2(ii): sigma_p(u) = V(J_u) = {(-c,1)}; w_2 autovettore congiunto',
      sp.simplify(sp.diff(w2, t) + c * w2) == 0 and sp.simplify(sp.diff(w2, x) - w2) == 0 and quot_dim([tau + c, xi - 1]) == 1)
check('E3.5h C3-T6(ii)/P4-T2(v)(a): G_u(d)u = w_2 ≠ 0 => Ann(u) non principale, coerente con sigma_p ≠ ∅',
      sp.simplify(w2) != 0)

nok = sum(1 for _, ok in RES if ok)
print(f'\nTOTALE E3: {nok}/{len(RES)} OK')
