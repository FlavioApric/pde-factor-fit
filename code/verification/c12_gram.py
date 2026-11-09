# S-C1C2 · gram.md: blocchi di Gram in forma chiusa su Omega = (0,T)x(a,b) e angoli di Friedrichs (C12-P4, C12-T3)
# Esecuzione: D:\ProblemaBase\.venv\Scripts\python.exe -I c12_gram.py
from sympy import (symbols, exp, integrate, simplify, conjugate, Matrix, Rational, diff, sqrt, N, I,
                   Function, expand, oo, log, cos, pi)
t, x = symbols('t x', real=True)
T, a, b = symbols('T a b', positive=True)
PASS = 0; FAIL = 0
def check(name, cond):
    global PASS, FAIL
    if cond: PASS += 1; print('PASS', name)
    else: FAIL += 1; print('FAIL', name)

# 1) Gram L^2(Omega) di esponenziali e^{tau t + xi x}: prodotto di due funzioni E
def E(sig, lo, hi):
    return (exp(sig*hi) - exp(sig*lo))/sig
t1, t2, k1, k2 = symbols('t1 t2 k1 k2', positive=True)  # somme != 0: evita il ramo Piecewise sigma=0
lhs = integrate(exp((t1 + t2)*t)*exp((k1 + k2)*x), (t, 0, T), (x, a, b))
rhs = E(t1 + t2, 0, T)*E(k1 + k2, a, b)
check('G1 <e1,e2>_{L2} = E(t1+t2;0,T) E(k1+k2;a,b) (reali)', simplify(lhs - rhs) == 0)
# H^m: fattore (1 + sum_{1<=|alpha|<=m} (tau1 conj tau2)^{a1} (xi1 conj xi2)^{a2}) -- verificato per m=1
lhs1 = integrate(sum(diff(exp(t1*t + k1*x), t, i, x, j)*diff(exp(t2*t + k2*x), t, i, x, j)
                     for i in range(2) for j in range(2) if i + j <= 1), (t, 0, T), (x, a, b))
rhs1 = (1 + t1*t2 + k1*k2)*rhs
check('G2 <e1,e2>_{H^1} = (1 + t1 t2 + k1 k2) <e1,e2>_{L2}', simplify(lhs1 - rhs1) == 0)

# 2) d_t d_x sul rettangolo: ker d_t = a(x)... attenzione: tau*xi ; ker d_x = A(t), ker d_t = B(x)
A = Function('A'); B = Function('B')
# <A(t), B(x)>_{H^m} = <A,B>_{L2} (le derivate miste si annullano) = int A * int B
for m in range(0, 3):
    terms = 0
    for i in range(m + 1):
        for j in range(m + 1 - i):
            terms += diff(A(t), t, i, x, j)*diff(B(x), t, i, x, j)
    check(f'P4 dtdx: <A(t),B(x)>_H{m} ha solo il termine alpha=0', simplify(terms - A(t)*B(x)) == 0)

# 3) trasporti paralleli: coseno tra u1 = -G(s) e u2 = e^t G(s) su famiglia G = 1_{s<eps}: -> 1 (controllo)
s, eps = symbols('s epsilon', positive=True)
n11 = integrate(integrate(1, (t, 0, s)), (s, 0, eps))
n22 = integrate(integrate(exp(2*t), (t, 0, s)), (s, 0, eps))
n12 = integrate(integrate(exp(t), (t, 0, s)), (s, 0, eps))
cosang = n12/sqrt(n11*n22)
from sympy import limit
check('T3 coseno(ker f, ker g) su G=1_{s<eps} -> 1 per eps->0', limit(cosang, eps, 0) == 1)
print('  coseno a eps=1/10:', N(cosang.subs(eps, Rational(1, 10)), 12))

# 4) onda sul quadrato: coordinate (s,r)=(x+t,x-t), quadrato = rombo |r|<s<2-|r|, Jacobiano 1/2.
#    controllo della disuguaglianza ||F||^2+||G||^2 <= C||F+G||^2 su una famiglia polinomiale (numerico, non metodo)
r = symbols('r', real=True)
cs = symbols('c0:4'); ds = symbols('d0:4')
Fp = sum(cs[i]*s**i for i in range(1, 4)); Gp = sum(ds[i]*r**i for i in range(1, 4))
def ip(f, g):  # L^2 del quadrato in coordinate (s,r)
    return (integrate(integrate(f*g, (s, abs(r), 2 - abs(r))), (r, -1, 1))/2)
def ip2(f, g):
    # spezzo r<0 e r>0 per evitare abs
    i1 = integrate(integrate(f*g, (s, -r, 2 + r)), (r, -1, 0))
    i2 = integrate(integrate(f*g, (s, r, 2 - r)), (r, 0, 1))
    return (i1 + i2)/2
basis = [s**i for i in range(0, 4)] + [r**i for i in range(1, 4)]   # costanti solo una volta
Gm = Matrix(len(basis), len(basis), lambda i, j: ip2(basis[i], basis[j]))
ev = [N(e, 15) for e in Gm.eigenvals(multiple=True)]
print('  onda: autovalori della Gram di {1,s,s^2,s^3,r,r^2,r^3} sul quadrato:', [float(e) for e in ev])
check('P4 onda: Gram unione (mod costanti) definita positiva (controllo)', min(float(e) for e in ev) > 0)
# angolo tra span{s,s^2,s^3} ⊖ 1 e span{r,r^2,r^3} ⊖ 1: coseno < 1 (controllo numerico)
import numpy as np
Gn = np.array(Gm.evalf(), dtype=float)
# proiezione ortogonale fuori dalle costanti
def orth_const(Gn):
    c = Gn[0, :] / Gn[0, 0]
    P = np.eye(7) - np.outer(np.eye(7)[:, 0], c)   # v -> v - <v,1>/<1,1> 1 (coefficienti)
    return P
P = orth_const(Gn)
Gp_ = P.T @ Gn @ P
iS = [1, 2, 3]; iR = [4, 5, 6]
G11 = Gp_[np.ix_(iS, iS)]; G22 = Gp_[np.ix_(iR, iR)]; G12 = Gp_[np.ix_(iS, iR)]
def msqrt_inv(M):
    w, V = np.linalg.eigh(M); return V @ np.diag(w**-0.5) @ V.T
cF = np.linalg.norm(msqrt_inv(G11) @ G12 @ msqrt_inv(G22), 2)
print('  onda: coseno di Friedrichs su sottospazi polinomiali di grado <=3:', cF)
check('P4 onda: coseno < 1 sui polinomi di grado <= 3 (controllo)', cF < 0.999)

print(f'\nRISULTATO: {PASS} PASS, {FAIL} FAIL')
