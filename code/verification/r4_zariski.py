"""R4 - [R4-T3] controllo: punti spettrali di una soluzione del calore su T.
Z_M = {(tau,xi) = (-k^2, i k) : 0 < |k| <= M}. Dimensione di {Q : deg Q <= n, Q|_Z = 0}.
Previsione: per M grande la dimensione e' dim (P)_{<=n} = dim C[tau,xi]_{<=n-2}... con P = tau - xi^2 (grado 2)
cioe' C(n,2) (numero di monomi di grado <= n-2) -> per n=2: 1 (solo P), n=3: 3 (P, tau P, xi P).
"""
import sympy as sp
tau, xi = sp.symbols('tau xi')

def mons(n):
    return [tau**a*xi**b for a in range(n+1) for b in range(n+1-a)]

for n in (2, 3):
    for M in (1, 2, 3, 4, 6):
        pts = [(-k**2, sp.I*k) for k in list(range(1, M+1)) + list(range(-M, 0))]
        A = sp.Matrix([[m.subs({tau: p[0], xi: p[1]}) for m in mons(n)] for p in pts])
        dimker = len(mons(n)) - A.rank()
        print(f"n={n} M={M} punti={len(pts)} dim{{Q: deg<=n, Q|Z=0}} = {dimker}")
print("atteso a regime: n=2 -> 1 (tau - xi^2 identificato), n=3 -> 3 (= dim dei multipli di P di grado <=3)")
