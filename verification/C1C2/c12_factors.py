# S-C1C2 · verifiche simboliche per C12-L3, C12-T1 (dimensioni), C12-T2 (Vandermonde), C12-P2, C12-P3
# Eseguire: D:\ProblemaBase\.venv\Scripts\python.exe -I c12_factors.py
from sympy import (symbols, groebner, factor_list, Poly, expand, simplify, exp, diff, I, sqrt,
                   resultant, Matrix, degree, sqf_part, Function, sin, cos, Rational, factor)
from itertools import combinations

tau, xi, t, x = symbols('tau xi t x')
PASS = 0; FAIL = 0
def check(name, cond):
    global PASS, FAIL
    if cond: PASS += 1; print('PASS', name)
    else: FAIL += 1; print('FAIL', name)

def apply_op(Pexpr, u):
    """applica P(d_t, d_x) a u"""
    p = Poly(expand(Pexpr), tau, xi)
    res = 0
    for (i, j), c in p.terms():
        res += c*diff(u, t, i, x, j)
    return simplify(res)

def quot_dim(gens):
    """dim_C C[tau,xi]/(gens) tramite monomi standard di una base di Groebner (grevlex)"""
    G = groebner(gens, tau, xi, order='grevlex')
    if list(G.exprs) == [1]: return 0
    lead = [Poly(g, tau, xi).monoms(order='grevlex')[0] for g in G.exprs]
    # conta i monomi non divisibili da alcun leading monomial (finito se zero-dim)
    N = 60; cnt = 0
    for a in range(N):
        for b in range(N):
            if not any(a >= l[0] and b >= l[1] for l in lead): cnt += 1
    # controllo di finitezza: nessun monomio standard al bordo
    for a in range(N):
        if not any(a >= l[0] and N-1 >= l[1] for l in lead): return None
        if not any(N-1 >= l[0] and a >= l[1] for l in lead): return None
    return cnt

# ---------------- C12-L3: risultanti nell'ideale, dimensione finita
f = tau - xi**2; g = tau + xi
r = resultant(f, g, tau)          # polinomio in xi
check('L3 Res_tau(calore,trasporto) in C[xi], !=0', r.free_symbols <= {xi} and r != 0)
check('L3 Res in (f,g)', groebner([f, g], tau, xi, order='lex').contains(r))
check('L3 dim R/(calore,trasporto) = 2', quot_dim([f, g]) == 2)
# additivita' dim R/(f,gh) = dim R/(f,g) + dim R/(f,h)
h = tau - xi
check('L3 additivita dim', quot_dim([f, g*h]) == quot_dim([f, g]) + quot_dim([f, h]))

# ---------------- esempi: fattori, delta(P), Delta
examples = {
 'onda':      tau**2 - xi**2,
 'trave':     tau**2 + xi**4,
 'calore':    tau - xi**2,
 'AD':        tau + 2*xi - 3*xi**2,          # c=2, D=3
 'Airy':      tau + xi**3,
 'KG':        tau**2 - xi**2 + 1,
 'telegrafo': tau**2 + 2*tau - xi**2,
 'caloreXtrasporto': (tau - xi**2)*(tau + xi),
 'dtdx':      tau*xi,
 'trasportiParalleli': (tau - xi)*(tau - xi - 1),
}
for name, P in examples.items():
    fl = factor_list(P, tau, xi, extension=I)[1]
    Q = [fa**m for fa, m in fl]
    if len(Q) >= 2:
        delta = sum(quot_dim([Q[i], Q[j]]) for i, j in combinations(range(len(Q)), 2))
    else:
        delta = 0
    print(f'  {name}: fattori {[(fa, m) for fa, m in fl]}  delta(P) = {delta}')
    if name in ('calore', 'AD', 'Airy'):
        check(f'P3 {name}: 1 solo fattore (G8)', len(fl) == 1 and fl[0][1] == 1)
    if name in ('KG', 'telegrafo'):
        check(f'P2 {name}: irriducibile anche su Q(i)', len(fl) == 1)
    if name == 'onda': check('T1 onda delta=1', delta == 1)
    if name == 'trave': check('T1 trave delta=2', delta == 2)
    if name == 'caloreXtrasporto': check('T1 caloreXtrasporto delta=2', delta == 2)
    if name == 'trasportiParalleli': check('T1 trasporti paralleli delta=0 (comassimale)', delta == 0)
    if name == 'dtdx': check('T1 dtdx delta=1', delta == 1)

# ---------------- C12-P2: criterio del discriminante (2o ordine monico in tau)
def disc_square(b, c):
    d = expand(b**2 - 4*c)
    # d quadrato in C[xi] <=> sqf_part ha grado 0 e coefficiente direttore arbitrario
    fl = factor_list(d, xi, extension=I)
    return all(m % 2 == 0 for _, m in fl[1])
check('P2 onda disc quadrato', disc_square(0, -xi**2))
check('P2 trave disc quadrato', disc_square(0, xi**4))
check('P2 KG disc non quadrato', not disc_square(0, -xi**2 + 1))
check('P2 telegrafo disc non quadrato', not disc_square(2, -xi**2))

# ---------------- C12-T2: formula di Vandermonde
def vandermonde_check(alist, comps, label):
    """alist: simboli a_j(xi); comps: funzioni u_j con (d_t - a_j(d_x)) u_j = 0"""
    k = len(alist)
    for j in range(k):
        check(f'T2 {label}: u_{j} in ker(tau-a_{j})', apply_op(tau - alist[j], comps[j]) == 0)
    u = sum(comps)
    V = Matrix(k, k, lambda l, j: alist[j]**l)
    Delta = expand(V.det())
    A = V.adjugate()
    # Delta(d_x) u_j  ==  sum_l adj_{jl}(d_x) d_t^l u
    for j in range(k):
        lhs = apply_op(Delta, comps[j])
        rhs = 0
        for l in range(k):
            rhs += apply_op(A[j, l], diff(u, t, l))
        check(f'T2 {label}: Delta(dx)u_{j} = sum_l adj_jl d_t^l u', simplify(lhs - rhs) == 0)
    # delta(P) = deg Delta = sum_{i<j} deg(a_i - a_j)
    dd = sum(degree(alist[i] - alist[j], xi) for i, j in combinations(range(k), 2))
    check(f'T2 {label}: deg Delta = sum deg(a_i-a_j) = {dd}', degree(Delta, xi) == dd)
    return Delta

F = Function('F'); G = Function('G')
# onda: a = +xi, -xi ; u_+ = F(x+t), u_- = G(x-t)
D_onda = vandermonde_check([xi, -xi], [F(x+t), G(x-t)], 'onda')
print('  Delta onda =', D_onda)
# trave: a = +i xi^2, -i xi^2 ; componenti esponenziali-polinomi di prova
s1, s2 = symbols('s1 s2')
D_trave = vandermonde_check([I*xi**2, -I*xi**2],
        [exp(I*s1**2*t + s1*x) + x, exp(-I*s2**2*t + s2*x) + 1], 'trave')
print('  Delta trave =', D_trave)
# calore x trasporto: a1 = xi^2, a2 = -xi
D_ct = vandermonde_check([xi**2, -xi], [exp(s1**2*t + s1*x) + x**2 + 2*t, G(x - t)], 'caloreXtrasporto')
print('  Delta caloreXtrasporto =', factor(D_ct))
# tre fattori: tau(tau-xi)(tau+xi^2)
D_3 = vandermonde_check([0*xi, xi, -xi**2], [F(x)+x, G(x+t), exp(-s1**2*t + s1*x)], 'tre fattori')
print('  Delta tre fattori =', factor(D_3))

# ambiguita' della trave: span{1, x} sta in entrambi i nuclei
for w in (1, x):
    check(f'T1 trave: {w} in ker(tau - i xi^2) cap ker(tau + i xi^2)',
          apply_op(tau - I*xi**2, w) == 0 and apply_op(tau + I*xi**2, w) == 0)
# ambiguita' calore x trasporto: span{1, e^{t-x}}
for w in (1, exp(t - x)):
    check(f'T1 caloreXtrasporto: {w} nei due nuclei', apply_op(tau - xi**2, w) == 0 and apply_op(tau + xi, w) == 0)

# ---------------- C12-P1: idempotenti polinomiali nel caso comassimale (trasporti paralleli)
f1 = tau - xi; g1 = tau - xi - 1          # f1 - g1 = 1
E1 = -g1; E2 = f1                          # u_1 = -g u in ker f ; u_2 = f u in ker g
uu = F(x + t) + exp(t)*G(x + t)
check('P1 E1 u in ker f', apply_op(f1, apply_op(E1, uu)) == 0)
check('P1 E2 u in ker g', apply_op(g1, apply_op(E2, uu)) == 0)
check('P1 E1 u + E2 u = u', simplify(apply_op(E1, uu) + apply_op(E2, uu) - uu) == 0)
check('P1 E2 u = e^t G(x+t) (componente)', simplify(apply_op(E2, uu) - exp(t)*G(x+t)) == 0)

print(f'\nRISULTATO: {PASS} PASS, {FAIL} FAIL')
