# Audit S-CHECK-F10-B: controllo indipendente di S10B-T1 ([F4-]).
# Variabile E = e^x, derivata D = E d/dE; kappa interi distinti => tutto e' razionale in E (esatto).
import sympy as sp, random, itertools, sys
E, s = sp.symbols('E s')
def D(g): return sp.together(E*sp.diff(g, E))
def Dn(g, n):
    for _ in range(n): g = D(g)
    return g
def wr(fs):
    n = len(fs)
    M = sp.Matrix(n, n, lambda a, b: Dn(fs[b], a))
    return sp.factor(M.det())
ok = []
def rep(name, c): ok.append(bool(c)); print(('OK  ' if c else 'FAIL') + ' ' + name); sys.stdout.flush()
random.seed(5)
cases = [(1, 2), (1, 3), (2, 5), (1, 2, 3), (1, 3, 4), (1, 2, 4, 5), (1, 2, 3, 5, 7)]
for kap in cases:
    N = len(kap)
    c = [sp.Rational(random.randint(1, 9), random.randint(1, 9)) for _ in range(N)]
    eps = [(-1)**j for j in range(N)]           # eps_j = (-1)^{j-1}, j = 1..N
    phi = [E**(-kap[j]) + eps[j]*c[j]*E**kap[j] for j in range(N)]
    W = wr(phi)
    V0 = sp.Mul(*[(-kap[j]) - (-kap[i]) for i in range(N) for j in range(i+1, N)])
    d = [sp.Mul(*[sp.Rational(kap[j]+kap[l], abs(kap[j]-kap[l])) for l in range(N) if l != j]) for j in range(N)]
    k = [2*q for q in kap]
    f = 0
    for r in range(N+1):
        for S in itertools.combinations(range(N), r):
            term = sp.Mul(*[c[j]*d[j]*E**(2*kap[j]) for j in S])
            term *= sp.Mul(*[sp.Rational(k[i]-k[j], k[i]+k[j])**2 for i, j in itertools.combinations(S, 2)])
            f += term
    rep('T1-W  kappa=%s: W = V0 e^{-sum kappa x} f (esatto)' % (kap,), sp.simplify(W - V0*E**(-sum(kap))*f) == 0)
    if N > 3: continue
    u = sp.together(2*D(D(f)/f))
    g = E**s
    Ag = sp.together(wr(phi + [g])/W/E**s)          # (A e^{sx}) e^{-sx}, razionale in E, polinomiale in s
    Ag = sp.cancel(Ag)
    psi = Ag*E**s
    res = sp.simplify((-Dn(psi, 2) - u*psi + s**2*psi)/E**s)
    rep('T1-L  kappa=%s: (-d^2 - u) A e^{sx} = -s^2 A e^{sx}' % (kap,), res == 0)
    lim_p = sp.limit(Ag, E, sp.oo); lim_m = sp.limit(Ag, E, 0)
    rep('T1-A+ kappa=%s: A e^{sx} e^{-sx} -> prod(s - kappa_j) per x -> +oo' % (kap,), sp.expand(lim_p - sp.Mul(*[s - q for q in kap])) == 0)
    rep('T1-A- kappa=%s: A e^{sx} e^{-sx} -> prod(s + kappa_j) per x -> -oo' % (kap,), sp.expand(lim_m - sp.Mul(*[s + q for q in kap])) == 0)
    # L2-autofunzioni: A applicato a e^{-kappa_j x} non serve; controllo che -kappa_j^2 sia autovalore:
    # psi_j := W(phi_1..^j..phi_N)/W (formula di Crum) decade ai due estremi
    for j in range(N):
        others = [phi[i] for i in range(N) if i != j]
        pj = sp.cancel(wr(others)/W) if others else sp.cancel(1/W)
        r2 = sp.simplify(-Dn(pj, 2) - u*pj + kap[j]**2*pj)
        dec = sp.limit(pj, E, sp.oo) == 0 and sp.limit(pj, E, 0) == 0
        rep('T1-ev kappa=%s j=%d: -kappa_j^2 autovalore con autofunzione decrescente' % (kap, j+1), r2 == 0 and dec)
print('TOTALE: %d/%d OK' % (sum(ok), len(ok)))
