import sys; sys.path.insert(0, r'D:\ProblemaBase\work\CHECK\sympy')
import sympy as sp, random
from itertools import combinations
from s19ka_common import *

random.seed(7)
def soliton_jets(N, k, M, Xv):
    X = sp.symbols('X1:%d' % (N+1))
    f = 0
    for r in range(N+1):
        for S in combinations(range(N), r):
            aS = sp.prod([((k[i]-k[j])/(k[i]+k[j]))**2 for i, j in combinations(S, 2)])
            f += aS*sp.prod([X[i] for i in S])
    D = lambda h: sum(k[i]*X[i]*sp.diff(h, X[i]) for i in range(N))
    u = 2*(f*D(D(f)) - D(f)**2)/f**2
    jets = [u]
    for j in range(1, M):
        jets.append(sp.together(D(jets[-1])))
    sub = dict(zip(X, Xv))
    return [sp.nsimplify(sp.simplify(J.subs(sub))) for J in jets]

for N, kk in [(1, [sp.Rational(3)]), (2, [sp.Rational(1), sp.Rational(3)]), (2, [sp.Rational(2), sp.Rational(-5)]),
              (3, [sp.Rational(1), sp.Rational(2), sp.Rational(-4)])]:
    Y = ysyms(2*N+1)
    U, V, fk, g, Gh = build_UV(N, kk, Y)
    rs = remainder_coeffs(U, V, fk, N)
    for trial in range(2):
        Xv = [sp.Rational(random.randint(1, 9), random.randint(1, 9)) for _ in range(N)]
        J = soliton_jets(N, kk, 2*N+1, Xv)
        vals = [sp.simplify(r.subs(dict(zip(Y, J)))) for r in rs]
        print('N', N, 'k', kk, 'X', Xv, 'remainders', vals, flush=True)
print('g:', gd_polys(3, ysyms(6)))
