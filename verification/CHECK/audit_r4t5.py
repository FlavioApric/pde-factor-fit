"""S-CHECK — audit R4-T5 (identificabilità per P ridotto, su I x T).
Controlli:
 1. (b, =>) costruzione del testimone Q in Ann(u) \\ (P) quando Z ∩ V(P_i) è finito:
    P = tau*(tau - xi^2) (monico, ridotto), u = parte di calore con molti modi + cos x stazionario.
    Testimone corretto (S-CHECK): Q = (P/P_i) * prod_{kappa in K_i} (xi - i kappa).
 2. Il testimone "ingenuo" con forme lineari in tau fallisce quando P_i = tau - c (dà Q = P).
 3. (c) soglia di Bézout: con |Z ∩ V(P)| = n*deg P (uguaglianza) esiste Q di grado <= n
    in Ann(u) non multiplo di P (calore, n = 2, modi kappa = ±1, ±2): la disuguaglianza stretta serve.
 4. Ipotesi "P monico in tau" necessaria: P = xi*tau ha P(., i*0) ≡ 0, il modo 0 è arbitrario.
 5. Parte indipendente dal dominio: (P) ⊆ I, V(I) = V(P), P ridotto => I = (P) (Nullstellensatz),
    verificato su un ideale esplicito (radicale tramite Gröbner).
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from sympy import (S, symbols, I, exp, cos, diff, expand, simplify, Poly, reduced, groebner,
                   Matrix, factor, rem, div)

tau, xi, t, x = symbols('tau xi t x')
ok = True
def check(name, cond):
    global ok
    ok = ok and bool(cond)
    print(('[OK]  ' if cond else '[FAIL]') + ' ' + name)

def op(P, u):
    p = Poly(P, tau, xi)
    return expand(sum(c * diff(u, t, a, x, b) if (a or b) else c * u
                      for (a, b), c in zip(p.monoms(), p.coeffs())))

# 1.
P1, P2 = tau, tau - xi**2
P = expand(P1 * P2)
K = 6
u_heat = sum(exp(-k**2 * t) * cos(k * x) / (k + 1) for k in range(0, K + 1))
u = u_heat + cos(x) + 3 * cos(2 * x)        # modi stazionari: kappa = ±1, ±2
check('P u = 0', simplify(op(P, u)) == 0)
# Z ∩ V(P1) = {(0, i kappa): kappa in {0, ±1, ±2}} (kappa=0 per la costante del calore)
Q = expand(P2 * xi * (xi**2 + 1) * (xi**2 + 4))   # (P/P1) * prod (xi - i kappa)
check('Q = (P/P1)·ξ(ξ²+1)(ξ²+4) annulla u', simplify(op(Q, u)) == 0)
check('Q non è multiplo di P (resto della divisione per la base di Gröbner {P} ≠ 0)', div(Q, P, tau, xi)[1] != 0)
# 2. testimone ingenuo con forma lineare in tau al punto z = (0, ·): (P/P1)·(tau - 0) = P
naive = expand(P2 * (tau - 0))
check('testimone ingenuo (P/P1)·(τ-τ_z) = P ∈ (P): la scelta della forma lineare conta', expand(naive - P) == 0)

# 3. soglia: calore P = tau - xi^2, n = 2, Z = {(-1, ±i), (-4, ±2i)} (4 = n*deg P punti)
Z = [(-1, I), (-1, -I), (-4, 2 * I), (-4, -2 * I)]
mons = [S.One, tau, xi, tau**2, tau * xi, xi**2]
A = Matrix([[m.subs({tau: z[0], xi: z[1]}) for m in mons] for z in Z])
ns = A.nullspace()
check(f'dim{{Q: deg Q <= 2, Q|_Z = 0}} = {len(ns)} > 1 = dim(multipli di P in grado <= 2)', len(ns) > 1)
Qs = [expand(sum(c * m for c, m in zip(v, mons))) for v in ns]
uh = exp(-t) * cos(x) + exp(-4 * t) * cos(2 * x)
nonmult = [q for q in Qs if div(q, tau - xi**2, tau, xi)[1] != 0]
check('esiste Q di grado 2 con Q u = 0 non multiplo di P (uguaglianza nella soglia non basta)',
      any(simplify(op(q, uh)) == 0 for q in nonmult))
print('     esempi:', nonmult)
# con un quinto modo (|Z| = 6 > 4) resta solo C·P
Z6 = Z + [(-9, 3 * I), (-9, -3 * I)]
A6 = Matrix([[m.subs({tau: z[0], xi: z[1]}) for m in mons] for z in Z6])
ns6 = A6.nullspace()
check(f'con |Z| = 6 > 4: dim = {len(ns6)} = 1 (solo multipli di P)', len(ns6) == 1)

# 4. non monico
Pn = xi * tau
w = t**3 + 1   # modo kappa = 0 arbitrario in t
check('P = ξτ non monico: u = t^3+1 (solo modo 0) risolve P u = 0 ma non un\'ODE in t fissata da P', op(Pn, w) == 0)

# 5. Nullstellensatz: I = (P, P*xi) ha V(I) = V(P) e I = (P) — caso banale; caso non banale:
# I = (P2^2, P2*xi) ⊇ (P2^2) non ridotto: V(I) = V(P2) ma I ≠ (P2) => serve P ridotto
Ired = groebner([expand(P2**2), expand(P2 * xi)], tau, xi, order='lex')
check('P non ridotto (P2^2): I=(P2^2, ξP2) ha V(I)=V(P2) ma P2 ∉ I (l\'ipotesi "ridotto" serve)',
      Ired.reduce(P2)[1] != 0)
print('\nESITO GLOBALE:', 'OK' if ok else 'FAIL')
