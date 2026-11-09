import sys; sys.path.insert(0, r'D:\ProblemaBase\work\CHECK\sympy')
import sympy as sp, random
from fractions import Fraction as Fr
from s19ka_common import *
from s19ka_jets import soliton_jets
random.seed(3)
for N, kk in [(2, [1, 3]), (3, [1, 2, -4]), (3, [2, 5, 7]), (4, [1, 2, 3, -5])]:
    Y = ysyms(2*N+1)
    U, V, fk, g, Gh = build_UV(N, [sp.Integer(x) for x in kk], Y)
    rs = remainder_coeffs(U, V, fk, N)
    for t in range(2):
        Xv = [Fr(random.randint(1, 9), random.randint(1, 9)) for _ in range(N)]
        J = soliton_jets(kk, Xv, 2*N+1)
        vals = [r.subs({Y[i]: sp.Rational(J[i].numerator, J[i].denominator) for i in range(2*N+1)}) for r in rs]
        print('N', N, 'k', kk, 'rem', vals, flush=True)
