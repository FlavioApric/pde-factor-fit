# S-C1C2 · C12-T6: basi di Appell v_n = e^{t a(d_x)} x^n per i fattori tau - a(xi) (analoghi di Rosenbloom-Widder)
# Esecuzione: D:\ProblemaBase\.venv\Scripts\python.exe -I c12_appell.py
from sympy import (symbols, exp, diff, expand, simplify, factorial, series, Poly, Rational, hermite,
                   integrate, oo, sqrt, pi, I, Abs, N, binomial, floor)
t, x, z = symbols('t x z')
PASS = 0; FAIL = 0
def check(name, cond):
    global PASS, FAIL
    if cond: PASS += 1; print('PASS', name)
    else: FAIL += 1; print('FAIL', name)

def a_op(apoly, f):
    p = Poly(apoly, z)
    return expand(sum(c*diff(f, x, k) for (k,), c in p.terms()))

def appell(apoly, n):
    """v_n = sum_k t^k/k! a(d_x)^k x^n (serie finita se a(0)=0; altrimenti fattore e^{a(0) t})"""
    a0 = Poly(apoly, z).eval(0)
    a1 = expand(apoly - a0)
    term = x**n; v = 0; k = 0
    while term != 0:
        v += t**k/factorial(k)*term
        term = a_op(a1, term); k += 1
    return expand(exp(a0*t)*v)

symbols_list = {
  'calore':  z**2,
  'AD':      -2*z + 3*z**2,      # u_t = -2 u_x + 3 u_xx
  'Airy':    -z**3,              # u_t = -u_xxx
  'trave+':  I*z**2,             # ramo della trave
  'reazione-diffusione': z**2 - 5,
}
for name, a in symbols_list.items():
    for n in range(0, 7):
        v = appell(a, n)
        res = simplify(diff(v, t) - a_op(a, v))
        ok = (res == 0) and simplify(v.subs(t, 0) - x**n) == 0
        if n >= 1:
            ok = ok and simplify(diff(v, x) - n*appell(a, n - 1)) == 0   # proprieta' di Appell
        check(f'T6 {name}: v_{n} soluzione, v_n(0,x)=x^n, d_x v_n = n v_(n-1)', ok)
    # funzione generatrice: sum v_n z^n/n! = e^{zx + t a(z)}
    gen = exp(z*x + t*a)
    ser = series(gen, z, 0, 7).removeO()
    okg = all(simplify(ser.coeff(z, n)*factorial(n) - appell(a, n)) == 0 for n in range(7))
    check(f'T6 {name}: funzione generatrice e^(zx + t a(z))', okg)

# calore: v_n = polinomi del calore di Rosenbloom-Widder; v_n(x,-s) = Hermite riscalati (R1-P11)
s = symbols('s', positive=True)
for n in range(0, 6):
    v = appell(z**2, n)
    rw = factorial(n)*sum(x**(n - 2*k)*t**k/(factorial(k)*factorial(n - 2*k)) for k in range(n//2 + 1))
    check(f'T6 calore: v_{n} = polinomio del calore RW', simplify(v - rw) == 0)
# ortogonalita' in L^2(G_s dx) di v_n(.,-s) e norma (2s)^n n!  (consistenza con R1-P11, pesi w_n = rho^{2n} n!, rho^2 = 2s)
Gs = exp(-x**2/(4*s))/sqrt(4*pi*s)
for n in range(0, 4):
    for m in range(0, 4):
        val = simplify(integrate(appell(z**2, n).subs(t, -s)*appell(z**2, m).subs(t, -s)*Gs, (x, -oo, oo)))
        target = (2*s)**n*factorial(n) if n == m else 0
        check(f'T6 calore: <v_{n}, v_{m}>_s = {target}', simplify(val - target) == 0)
# Airy: v_n(.,-s) NON ortogonali per alcun peso gaussiano simmetrico di prova (controllo del no-go C12-P6, solo esempio)
v0, v1, v2, v3 = [appell(-z**3, n).subs(t, -s) for n in range(4)]
print('  Airy v_3(x,-s) =', v3)

# stima |v_n| <= (n!)^{1-1/q} K^n con K = exp(2 - 1/q + X + T*A) (lambda = 1), controllo numerico (non metodo)
import math
for name, a, q in (('calore', z**2, 2), ('AD', -2*z + 3*z**2, 2), ('Airy', -z**3, 3)):
    A = sum(abs(complex(c)) for c in Poly(a, z).coeffs())
    X, T = 1.0, 1.0
    K = math.exp(2 - 1/q + X + T*A)
    ok = True
    for n in range(0, 16):
        v = appell(a, n)
        mx = max(abs(complex(N(v.subs({x: xx, t: tt})))) for xx in (-1, -0.5, 0, 0.5, 1) for tt in (0, 0.5, 1))
        ok = ok and mx <= math.factorial(n)**(1 - 1/q)*K**n
    check(f'T6 stima di crescita {name} (n<16, controllo numerico su griglia)', ok)

print(f'\nRISULTATO: {PASS} PASS, {FAIL} FAIL')
