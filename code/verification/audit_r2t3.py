"""S-CHECK — audit R2-T3 (G1 come uguaglianza).
Controlli:
 1. dim R/(L, L1^2) == 2 * dim R/(L1, L2) su coppie coprime (esempi del report + casuali).
 2. Esempio con frequenza di collisione non nulla: base esplicita di Sol(R/(L,L1^2)) e
    scomposizione esplicita di ogni elemento in ker L1 + ker L2 (direzione "⊇" di (b)).
 3. Necessità dell'iniettività: controesempio su I x T (u = t) per L1 = d_t + d_x, L2 = -d_t + d_x^2.
 4. Necessità della coprimalità: termini con fattore comune -> ideale non 0-dimensionale.
 5. Lemma aggiunto da S-CHECK: le componenti u1, u2 sono esponenziali-polinomi
    (u1 in Sol(R/(L1, L2^2))): verificato sull'esempio 2.
"""
import random, sys
sys.stdout.reconfigure(encoding="utf-8")
from sympy import (symbols, groebner, Poly, expand, exp, diff, simplify, Rational,
                   Matrix, solve, S, factor_list, gcd)

tau, xi, t, x = symbols('tau xi t x')
GENS = (tau, xi)


def std_monomials(polys):
    G = groebner(polys, *GENS, order='grevlex')
    if list(G.exprs) == [1]:
        return G, []
    lms = [Poly(g, *GENS).monoms(order='grevlex')[0] for g in G.exprs]
    pure_t = [a for (a, b) in lms if b == 0]
    pure_x = [b for (a, b) in lms if a == 0]
    if not pure_t or not pure_x:
        return G, None  # non 0-dimensionale
    A, B = min(pure_t), min(pure_x)
    std = [(a, b) for a in range(A) for b in range(B)
           if not any(a >= c and b >= d for (c, d) in lms)]
    return G, std


def dimq(polys):
    G, std = std_monomials(polys)
    return None if std is None else len(std)


def op(P, u):
    """applica P(d_t, d_x) a u"""
    p = Poly(P, *GENS)
    return expand(sum(c * diff(u, t, a, x, b) if (a or b) else c * u
                      for (a, b), c in zip(p.monoms(), p.coeffs())))


ok = True
def check(name, cond):
    global ok
    ok = ok and bool(cond)
    print(('[OK]  ' if cond else '[FAIL]') + ' ' + name)

# 1. dimensioni
pairs = [
    ('calore: L1=xi^2, L2=-tau', xi**2, -tau),
    ('avv-diff R2: L1=tau-xi^2, L2=xi', tau - xi**2, xi),
    ('avv-diff R5: L1=tau-xi^2, L2=-xi', tau - xi**2, -xi),
    ('avv-diff trasporto/diffusione: L1=tau+xi, L2=-xi^2', tau + xi, -xi**2),
    ('collisione non nulla: L1=tau-xi^2, L2=tau+xi', tau - xi**2, tau + xi),
]
random.seed(1)
mons = [1, tau, xi, tau**2, tau * xi, xi**2]
for k in range(25):
    L1 = sum(random.randint(-3, 3) * m for m in mons)
    L2 = sum(random.randint(-3, 3) * m for m in mons)
    if L1 == 0 or L2 == 0:
        continue
    if gcd(L1, L2).free_symbols:
        continue
    pairs.append((f'casuale {k}', L1, L2))
for name, L1, L2 in pairs:
    L = expand(L1 + L2)
    d1 = dimq([L, expand(L1**2)])
    d2 = dimq([L1, L2])
    check(f'dim R/(L,L1^2) = {d1} = 2*dim R/(L1,L2) = 2*{d2}  [{name}]',
          d1 is not None and d2 is not None and d1 == 2 * d2)

# 2. base esplicita e scomposizione, caso collisione {(0,0),(1,-1)}
# rappresentazione: u = sum_f q_f(t,x) e^{f.(t,x)}, P(d) (q e^{f}) = e^{f} P(d + f) q
FREQ = [(0, 0), (1, -1)]
def opq(P, q, f):
    Ps = expand(P.subs({tau: tau + f[0], xi: xi + f[1]}, simultaneous=True))
    return op(Ps, q)
def opU(P, Q):  # Q: dict freq -> polinomio
    return {f: expand(opq(P, Q[f], f)) for f in FREQ}
def coeffs_all(D):
    out = []
    for f in FREQ:
        if D[f] != 0:
            out += Poly(D[f], t, x).coeffs()
    return out
mon = [t**i * x**j for i in range(5) for j in range(5 - i)]
L1, L2 = tau - xi**2, tau + xi
L = expand(L1 + L2)
cs = symbols('c0:%d' % (2 * len(mon)))
Uq = {FREQ[0]: sum(c * m for c, m in zip(cs[:len(mon)], mon)),
      FREQ[1]: sum(c * m for c, m in zip(cs[len(mon):], mon))}
eqs = coeffs_all(opU(L, Uq)) + coeffs_all(opU(expand(L1**2), Uq))
sol = solve(eqs, cs, dict=True)[0]
free = [c for c in cs if c not in sol]
basis = []
for c in free:
    sub = {cc: (1 if cc == c else 0) for cc in free}
    basis.append({f: expand(Uq[f].subs(sol).subs(sub)) for f in FREQ})
check(f'dim Sol(R/(L,L1^2)) (ansatz grado<=4) = {len(basis)} = 2*dim R/(L1,L2) = 4', len(basis) == 4)
def show(Q):
    return ' + '.join(f'({Q[f]})e^({f[0]}t+{f[1]}x)' for f in FREQ if Q[f] != 0)
for Q in basis:
    ds = symbols('d0:%d' % (2 * len(mon)))
    U1 = {FREQ[0]: sum(d * m for d, m in zip(ds[:len(mon)], mon)),
          FREQ[1]: sum(d * m for d, m in zip(ds[len(mon):], mon))}
    U2 = {f: Q[f] - U1[f] for f in FREQ}
    s2 = solve(coeffs_all(opU(L1, U1)) + coeffs_all(opU(L2, U2)), ds, dict=True)
    good = bool(s2)
    if good:
        u1 = {f: expand(U1[f].subs(s2[0]).subs({d: 0 for d in ds})) for f in FREQ}
        u2 = {f: expand(Q[f] - u1[f]) for f in FREQ}
        good = (all(v == 0 for v in opU(L1, u1).values()) and all(v == 0 for v in opU(L2, u2).values())
                and all(v == 0 for v in opU(expand(L2**2), u1).values()))
        print('     u =', show(Q), ' -> u1 =', show(u1), ', u2 =', show(u2))
    check('scomposizione esplicita u = u1+u2, u1 in ker L1 ∩ ker L2^2 (esp-pol), u2 in ker L2', good)

# 3. controesempio su I x T (iniettività necessaria)
L1, L2 = tau + xi, -tau + xi**2
L = expand(L1 + L2)
u = t
check('u=t: L u = 0', op(L, u) == 0)
check('u=t: L1^2 u = 0', op(expand(L1**2), u) == 0)
check('su R: t = (t-x) + x con t-x in ker L1, x in ker L2', op(L1, t - x) == 0 and op(L2, x) == 0)
# su T: modo k=0 -> L1_0 = tau, L2_0 = -tau: ker = costanti, quindi t non si scompone
L10, L20 = L1.subs(xi, 0), L2.subs(xi, 0)
check('su T, modo 0: L1_0 = tau, L2_0 = -tau => ker L1_0 + ker L2_0 = costanti, t escluso',
      L10 == tau and L20 == -tau)

# 4. fattore comune: termini d_t d_x e d_x^2
L1, L2 = tau * xi, xi**2
check('fattore comune xi: R/(L, L1^2) non 0-dimensionale (dim infinita)', dimq([expand(L1 + L2), expand(L1**2)]) is None)

print('\nESITO GLOBALE:', 'OK' if ok else 'FAIL')
