import sys; sys.path.insert(0, r'D:\ProblemaBase\work\CHECK\sympy')
import sympy as sp, time
from fractions import Fraction as Fr
from s19ka_common import *
from s19ka_jets import soliton_jets

for N in range(1, 4):
    Y = ysyms(2*N+1)
    U, V, fk, g, Gh = build_UV(N, [sp.Integer(0)]*N, Y)
    rs = remainder_coeffs(U, V, fk, N)
    sub = {Y[0]: 1}
    for j in range(1, N): sub[Y[j]] = 0
    free = list(reversed(Y[N:2*N]))
    eqs = [sp.expand(r.subs(sub)) for r in rs]
    G = sp.groebner(eqs, *free, order='lex')
    last = [p for p in G.exprs if set(p.free_symbols) <= {Y[N]}]
    print('N', N, 'k=0 fibre (1,0..): poly in y_N', [sp.factor(p) for p in last], flush=True)

# Pi_2 by elimination for numeric k
for kk in [(1, 3), (2, 7), (1, 0)]:
    N = 2
    Y = ysyms(4)
    U, V, fk, g, Gh = build_UV(N, [sp.Integer(x) for x in kk], Y)
    rs = remainder_coeffs(U, V, fk, N)
    t = time.time()
    G = sp.groebner(rs, Y[3], Y[2], Y[1], Y[0], order='lex')
    el = [p for p in G.exprs if Y[3] not in p.free_symbols]
    for p in el:
        P = sp.Poly(p, Y[2], Y[1], Y[0])
        print('k', kk, 'elim elt total deg', P.total_degree(), 'deg y2', sp.degree(p, Y[2]),
              'coeff y0^8', P.coeff_monomial(Y[0]**8), 'LC y2^4', P.coeff_monomial(Y[2]**4), 'factors', len(sp.factor_list(p)[1]), time.time()-t, flush=True)
        if kk[1] != 0:
            for Xv in [(Fr(2, 3), Fr(5, 7)), (Fr(4), Fr(1, 9))]:
                J = soliton_jets(kk, Xv, 3)
                print('  vanishes on soliton:', p.subs({Y[i]: sp.Rational(J[i].numerator, J[i].denominator) for i in range(3)}))
