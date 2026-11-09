# OP-F5C: verifica (V-ex, aritmetica razionale esatta) di (Nov'): per l'N-solitone formale
# u = 2 D^2 log f, f = sum_S a_S X^S e^{(sum_{i in S} k_i) x}, a_S = prod_{i<j in S} ((k_i-k_j)/(k_i+k_j))^2,
# in punti X razionali, i getti in x = 0 soddisfano U | V^2 + lam*Ginf^2, con
# U = sum_j Ghat_j lam^(N-j), V = D(U)/2, Ghat_j = sum_i a_{j-i} g_i, Ginf = prod (lam + k_i^2/4).
# (Versione veloce di opf5c_nov.py: serie di Taylor esatte invece di derivate simboliche.)
import sympy as sp, pickle, itertools, random, sys
from fractions import Fraction as Fr
from math import factorial
g = [sp.sympify(s) for s in pickle.load(open('opf5c_gd.pkl', 'rb'))]
Y = sp.symbols('y0:%d' % 40)
lam = sp.Symbol('lam')
def taylor_u(ks, X, order):
    N = len(ks); M = order + 3
    f = [Fr(0)]*M
    for r in range(N+1):
        for S in itertools.combinations(range(N), r):
            aS = Fr(1)
            for i, j in itertools.combinations(S, 2): aS *= (Fr(ks[i]-ks[j], ks[i]+ks[j]))**2
            c = aS
            for i in S: c *= X[i]
            K = sum(Fr(ks[i]) for i in S)
            for n in range(M): f[n] += c*K**n/factorial(n)
    # L = log f come serie: L' = f'/f
    fp = [f[n+1]*(n+1) for n in range(M-1)]
    q = [Fr(0)]*(M-1)  # q = f'/f
    for n in range(M-1):
        q[n] = (fp[n] - sum(q[m]*f[n-m] for m in range(n)))/f[0]
    # u = 2 (log f)'' = 2 q'
    u = [2*q[n+1]*(n+1) for n in range(M-2)]
    # getti y_j = u^{(j)}(0) = j! u_j
    return [u[j]*factorial(j) for j in range(order+1)]
def Dop(e, top): return sp.expand(sum(sp.diff(e, Y[m])*Y[m+1] for m in range(top)))
def check(ks, seed):
    N = len(ks); random.seed(seed)
    kap = [Fr(k)**2/4 for k in ks]
    Ginf = sp.Poly(sp.Mul(*[(lam + sp.Rational(q.numerator, q.denominator)) for q in kap]), lam)
    a = [Ginf.coeff_monomial(lam**(N-j)) for j in range(N+1)]
    Gh = [sp.expand(sum(a[j-i]*g[i] for i in range(j+1))) for j in range(N+1)]
    Ghp = [Dop(e, 2*N+1) for e in Gh]
    ok = True
    for trial in range(3):
        X = [Fr(random.randint(1, 9), random.randint(1, 9)) for _ in range(N)]
        jets = taylor_u(ks, X, 2*N+2)
        sub = {Y[j]: sp.Rational(jets[j].numerator, jets[j].denominator) for j in range(2*N+2)}
        U = sum(Gh[j].subs(sub)*lam**(N-j) for j in range(N+1))
        V = sum((Ghp[j].subs(sub)/2)*lam**(N-j) for j in range(N+1))
        r = sp.rem(sp.expand(V**2 + lam*Ginf.as_expr()**2), sp.expand(U), lam)
        ok &= sp.expand(r) == 0
    return ok
for ks in [(1,), (3,), (1, 2), (1, 3), (2, 5), (1, 2, 4), (1, 3, 7), (1, 2, 3, 5), (1, 2, 4, 7), (1, 2, 3, 5, 8)]:
    print('[NOV2] k =', ks, ':', 'OK' if check(ks, sum(ks)) else 'FAIL'); sys.stdout.flush()
