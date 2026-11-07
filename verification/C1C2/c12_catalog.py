# S-C1C2 · CATALOGO_v2 / gram.md: verifiche T e = 0 per le basi delle schede ★,
# lato stazionario di avvezione-diffusione, Gram in forma chiusa.
# Esecuzione: D:\ProblemaBase\.venv\Scripts\python.exe -I c12_catalog.py
from sympy import (symbols, exp, diff, expand, simplify, factorial, Poly, I, groebner, factor_list,
                   integrate, conjugate, tanh, limit, oo, Function, Rational, summation, Symbol, nsimplify)

t, x, z, tau, xi = symbols('t x z tau xi')
x0 = symbols('x0', real=True)
c, D, L, rho = symbols('c D L rho', positive=True)
PASS = 0; FAIL = 0
def check(name, cond):
    global PASS, FAIL
    if cond: PASS += 1; print('PASS', name)
    else: FAIL += 1; print('FAIL', name)

def op(P, f):
    """P(tau,xi) -> P(d_t, d_x) applicato a f"""
    p = Poly(expand(P), tau, xi)
    return expand(sum(co*diff(f, t, i, x, j) for (i, j), co in p.terms()))

def a_op(apoly, f):
    p = Poly(apoly, z)
    return expand(sum(co*diff(f, x, k) for (k,), co in p.terms()))

def appell(apoly, n):
    a0 = Poly(apoly, z).eval(0); a1 = expand(apoly - a0)
    term = (x - x0)**n; v = 0; k = 0
    while term != 0:
        v += t**k/factorial(k)*term; term = a_op(a1, term); k += 1
    return expand(exp(a0*t)*v)

def quotient_dim(gens):
    """dim_C R/(gens) via base di Groebner (lex), contando i monomi standard (ideale 0-dim)."""
    G = groebner(gens, tau, xi, order='grevlex')
    lead = [Poly(g, tau, xi).monoms(order='grevlex')[0] for g in G.exprs]
    cnt = 0
    for i in range(0, 12):
        for j in range(0, 12):
            if not any(i >= a and j >= b for (a, b) in lead): cnt += 1
    return cnt, G

# ---------- trasporto  P = tau + c xi  (fattore tau - a, a = -c z) ----------
Ptr = tau + c*xi
for n in range(7):
    v = appell(-c*z, n)
    check(f'TR v_{n} = (x-x0-ct)^{n} in ker(d_t + c d_x)',
          simplify(v - (x - x0 - c*t)**n) == 0 and op(Ptr, v) == 0)
s, sp = symbols('s sp')
k = Symbol('k', integer=True, nonnegative=True)
rk = summation((s*sp/rho**2)**k, (k, 0, oo))
check('TR nucleo di Fock (q=1): sum (s sbar\')^n/rho^{2n} = rho^2/(rho^2 - s sbar\') per |s s\'|<rho^2',
      simplify(rk.args[0][0] - rho**2/(rho**2 - s*sp)) == 0 if hasattr(rk, 'args') and rk.func.__name__ == 'Piecewise'
      else simplify(rk - rho**2/(rho**2 - s*sp)) == 0)
check('TR irriducibile', len(factor_list(Ptr, tau, xi)[1]) == 1)

# ---------- calore  P = tau - xi^2 ----------
Pca = tau - xi**2
zeta = symbols('zeta', real=True)
check('CA e^{zeta x + zeta^2 t} in ker, zeta reale', op(Pca, exp(zeta*x + zeta**2*t)) == 0)
check('CA irriducibile', len(factor_list(Pca, tau, xi)[1]) == 1)
for n in range(6):
    check(f'CA v_{n} (Rosenbloom-Widder) in ker', op(Pca, appell(z**2, n)) == 0)

# ---------- onda  P = tau^2 - xi^2 = (tau - xi)(tau + xi) ----------
Pon = tau**2 - xi**2
fl = factor_list(Pon, tau, xi)[1]
check('ON fattori: tau - xi, tau + xi (molteplicita 1)', len(fl) == 2 and all(m == 1 for _, m in fl))
for n in range(6):
    vp = appell(z, n); vm = appell(-z, n)
    check(f'ON v_{n}^+ = (x-x0+t)^n in ker(tau-xi), v_{n}^- = (x-x0-t)^n in ker(tau+xi)',
          simplify(vp - (x - x0 + t)**n) == 0 and op(tau - xi, vp) == 0 and
          simplify(vm - (x - x0 - t)**n) == 0 and op(tau + xi, vm) == 0)
d, G = quotient_dim([tau - xi, tau + xi])
check('ON dim R/(tau-xi, tau+xi) = 1 (ambiguita = costanti)', d == 1)

# ---------- trave  P = tau^2 + xi^4 = (tau - i xi^2)(tau + i xi^2) ----------
Ptv = tau**2 + xi**4
check('TV fattorizzazione (tau - i xi^2)(tau + i xi^2)', expand((tau - I*xi**2)*(tau + I*xi**2) - Ptv) == 0)
for n in range(6):
    vp = appell(I*z**2, n); vm = appell(-I*z**2, n)
    check(f'TV v_{n}^+ in ker(tau - i xi^2), v_{n}^- in ker(tau + i xi^2), entrambi in ker P',
          op(tau - I*xi**2, vp) == 0 and op(tau + I*xi**2, vm) == 0 and op(Ptv, vp) == 0 and op(Ptv, vm) == 0)
d, G = quotient_dim([tau - I*xi**2, tau + I*xi**2])
check('TV dim R/(tau - i xi^2, tau + i xi^2) = 2', d == 2)
check('TV ambiguita span{1, x}: 1 e x in entrambi i nuclei',
      all(op(f, w) == 0 for f in (tau - I*xi**2, tau + I*xi**2) for w in (1 + 0*x, x)))

# ---------- avvezione-diffusione  P = tau + c xi - D xi^2 ----------
Pad = tau + c*xi - D*xi**2
check('AD irriducibile (strato fattori banale, C12-P3)', len(factor_list(Pad, tau, xi)[1]) == 1)
e_bl = exp(c*x/D)
check('AD strato limite e^{cx/D} in ker P', simplify(op(Pad, e_bl)) == 0)
check('AD e^{cx/D} in ker d_t e in ker(c d_x - D d_x^2) (sotto-equazione stazionaria)',
      diff(e_bl, t) == 0 and simplify(c*diff(e_bl, x) - D*diff(e_bl, x, 2)) == 0)
d, G = quotient_dim([Pad, tau])
check('AD dim R/(P, tau) = 2: Sol = ker P cap ker d_t = span{1, e^{cx/D}}', d == 2)
check('AD Groebner (P, tau) = (tau, D xi^2 - c xi) a meno di normalizzazione',
      set(Poly(g, tau, xi).monic().as_expr() for g in G.exprs) ==
      set([tau, expand(xi**2 - c*xi/D)]))
a_ad = -c*z + D*z**2
check('AD a(c/D) = 0: e^{cx/D} = e_zeta con zeta = c/D reale, a(zeta) = 0 (punto (0,c/D) di V(P))',
      simplify(a_ad.subs(z, c/D)) == 0)
for n in range(5):
    check(f'AD v_{n} (Appell, q=2) in ker P', simplify(op(Pad, appell(a_ad, n))) == 0)
# Gram del lato stazionario in L^2(0,L) (indipendente da t)
g11 = L; g12 = integrate(e_bl, (x, 0, L)); g22 = integrate(e_bl**2, (x, 0, L))
Pe = symbols('Pe', positive=True)
cos2 = simplify((g12**2/(g11*g22)).subs(c, Pe*D/L))
check('AD Gram {1, e^{cx/D}} in L^2(0,L): cos^2 = tanh(Pe/2)/(Pe/2), Pe = cL/D',
      simplify((cos2 - tanh(Pe/2)/(Pe/2)).rewrite(exp)) == 0)
check('AD cos^2 -> 1 per Pe -> 0, -> 0 per Pe -> oo', limit(cos2, Pe, 0) == 1 and limit(cos2, Pe, oo) == 0)
# e^{cx/D} non sta in ker(d_t + c d_x) + ker(d_t - D d_x^2) (split per termini, non per fattori)
F = Function('F')
lhs = (diff(e_bl, t) - D*diff(e_bl, x, 2))           # (d_t - D d_x^2) e^{cx/D}
rhs = (diff(F(x - c*t), t) - D*diff(F(x - c*t), x, 2))  # (d_t - D d_x^2) F(x - ct)
check('AD split per termini impossibile: (d_t + c d_x) annulla il membro di destra ma non quello di sinistra',
      simplify(diff(rhs, t) + c*diff(rhs, x)) == 0 and simplify(diff(lhs, t) + c*diff(lhs, x)) != 0)

# ---------- Gram di esponenziali (forma chiusa, complessi) ----------
def E(lam, a, b):
    return (b - a) if lam == 0 else (exp(lam*b) - exp(lam*a))/lam
T0, a0_, b0_ = 1, 0, 2
for (t1, k1, t2, k2) in [(I, 1 + I, -1, 2), (Rational(1, 2), -I, 2*I, 3), (0, 1, 0, -1)]:
    e1 = exp(t1*t + k1*x); e2 = exp(t2*t + k2*x)
    ip = integrate(integrate(expand(e1*conjugate(e2)), (t, 0, T0)), (x, a0_, b0_))
    cf = E(t1 + conjugate(t2), 0, T0)*E(k1 + conjugate(k2), a0_, b0_)
    check(f'GR <e_({t1},{k1}), e_({t2},{k2})>_L2 = E(tau1+conj tau2) E(xi1+conj xi2)', simplify(ip - cf) == 0)
    ip1 = ip + sum(integrate(integrate(expand(diff(e1, v)*conjugate(diff(e2, v))), (t, 0, T0)), (x, a0_, b0_))
                   for v in (t, x))
    check(f'GR <.,.>_H1 = (1 + tau1 conj tau2 + xi1 conj xi2) <.,.>_L2', simplify(ip1 - (1 + t1*conjugate(t2) + k1*conjugate(k2))*cf) == 0)

print(f'\nRISULTATO: {PASS} PASS, {FAIL} FAIL')
