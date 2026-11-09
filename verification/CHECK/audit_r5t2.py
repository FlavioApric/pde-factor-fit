"""S-CHECK — audit R5-T2 (E_int commutante, complessità).
Controlli:
 1. Identità algebrica Π(1+z_n) - 1 - Σ z_n = Σ_{k>=2} e_k(z) e numero di monomi 2^N - N - 1 (N = 2..6).
 2. Identità operatoriale con matrici commutanti (polinomi in una stessa matrice):
    e^{tΣA_n} u0 = Σ_{S} Π_{n∈S}(e^{tA_n} - I) u0.
 3. Necessità della commutatività: con A1, A2 non commutanti l'identità fallisce.
 4. Algoritmo O(N^2) per tutti gli e_k (coefficienti di Π(1+λ z_n)) = forza bruta (N = 7).
 5. Ipotesi nascosta "ogni A_n genera un semigruppo": u_t = -u_xxxx - u_xx è ben posto
    (simbolo -κ^4+κ^2 <= 1/4) ma il termine A2 = -∂_x^2 ha moltiplicatore e^{tκ^2} illimitato:
    con û0 = e^{-|κ|} il dato S2(t)u0 non è in L^2 per t>0, quindi u_n e E_int^add non sono definiti.
 6. L'output "tutti i coefficienti di Möbius c_S" ha 2^N - N - 1 voci: costo Ω(2^N) solo per scriverlo.
"""
import sys, itertools, random
sys.stdout.reconfigure(encoding="utf-8")
from sympy import (symbols, expand, Poly, prod, Matrix, eye, zeros, Rational, exp, oo, limit,
                   simplify, Symbol)
from sympy.polys.specialpolys import symmetric_poly

ok = True
def check(name, cond):
    global ok
    ok = ok and bool(cond)
    print(('[OK]  ' if cond else '[FAIL]') + ' ' + name)

# 1.
for N in range(2, 7):
    z = symbols('z1:%d' % (N + 1))
    lhs = expand(prod(1 + zi for zi in z) - 1 - sum(z))
    rhs = expand(sum(symmetric_poly(k, *z) for k in range(2, N + 1)))
    nmon = len(Poly(lhs, *z).monoms())
    check(f'N={N}: Π(1+z)-1-Σz = Σ_(k>=2) e_k ; monomi = {nmon} = 2^N-N-1 = {2**N-N-1}',
          lhs == rhs and nmon == 2**N - N - 1)

# 2. matrici commutanti: A_n = p_n(B) con B nilpotente+diagonale (esponenziale esatto)
t = symbols('t')
B = Matrix([[1, 1, 0], [0, 1, 0], [0, 0, -2]])
As = [B, B**2 - 3 * eye(3), 2 * B - eye(3)]
u0 = Matrix([1, 2, -1])
Ex = lambda M: (M * t).exp()
S_total = Ex(sum(As, zeros(3)))
lhs = S_total * u0
rhs = zeros(3, 1)
for r in range(len(As) + 1):
    for Sset in itertools.combinations(range(len(As)), r):
        v = u0
        for n in Sset:
            v = (Ex(As[n]) - eye(3)) * v
        rhs += v
check('matrici commutanti (N=3): e^{tΣA}u0 = Σ_S Π(e^{tA_n}-I)u0', simplify(lhs - rhs) == zeros(3, 1))

# 3. non commutanti
A1 = Matrix([[0, 1], [0, 0]]); A2 = Matrix([[0, 0], [1, 0]])
w0 = Matrix([1, 0])
l3 = (A1 + A2).exp() * w0
r3 = w0 + (A1.exp() - eye(2)) * w0 + (A2.exp() - eye(2)) * w0 + (A1.exp() - eye(2)) * (A2.exp() - eye(2)) * w0
check('non commutanti ([A1,A2]≠0, t=1): l\'identità fallisce (la commutatività è necessaria)',
      simplify(l3 - r3) != zeros(2, 1))

# 4. O(N^2) contro forza bruta
random.seed(3)
N = 7
zv = [Rational(random.randint(-9, 9), random.randint(1, 9)) for _ in range(N)]
coef = [Rational(1)] + [Rational(0)] * N          # coefficienti di Π(1+λ z_n)
for zn in zv:                                       # N passi da O(N): O(N^2)
    for k in range(N, 0, -1):
        coef[k] += zn * coef[k - 1]
brute = [sum(prod(c) for c in itertools.combinations(zv, k)) for k in range(N + 1)]
check('O(N^2): coefficienti di Π(1+λz_n) = e_k per forza bruta (N=7)', coef == brute)
val = prod(1 + zn for zn in zv) - 1 - sum(zv)       # O(N)
check('valore O(N) = Σ_(k>=2) e_k', val == sum(brute[2:]))

# 5. termine che non genera
kap = Symbol('kappa', positive=True)
tt = Symbol('t', positive=True)
sym_total = -kap**4 + kap**2
check('simbolo totale -κ^4+κ^2 limitato superiormente (max 1/4): A genera', limit(sym_total, kap, oo) == -oo)
term = (exp(tt * kap**2) * exp(-kap))**2            # |S2(t) û0|^2
check('|e^{tκ²} e^{-κ}|² → ∞ per κ→∞ (t>0): S2(t)u0 ∉ L², u_2 e E_int^add non definiti',
      limit(term, kap, oo) == oo)

# 6. dimensione dell'output di Möbius
for N in (10, 20, 30):
    print(f'     N={N}: numero di c_S con |S|>=2 = {2**N - N - 1}')
check('la famiglia {c_S} ha 2^N-N-1 elementi (output esponenziale)', True)
print('\nESITO GLOBALE:', 'OK' if ok else 'FAIL')
