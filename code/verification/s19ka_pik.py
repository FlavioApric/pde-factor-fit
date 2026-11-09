import sys; sys.path.insert(0, r'D:\ProblemaBase\work\CHECK\sympy')
import sympy as sp
from s19ka_common import *
N = 2
Y = ysyms(4)
I = sp.I
for kk in [(1, I), (1, 1 + I), (2, 2*I), (3, sp.Rational(1, 3))]:
    U, V, fk, g, Gh = build_UV(N, [sp.sympify(x) for x in kk], Y)
    rs = remainder_coeffs(U, V, fk, N)
    G = sp.groebner(rs, Y[3], Y[2], Y[1], Y[0], order='lex', extension=I) if any(sp.sympify(x).has(I) for x in kk) else sp.groebner(rs, Y[3], Y[2], Y[1], Y[0], order='lex')
    el = [p for p in G.exprs if Y[3] not in p.free_symbols]
    for p in el:
        P = sp.Poly(p, Y[2], Y[1], Y[0])
        disc = sp.discriminant(sp.Poly(p, Y[2]))
        print('k', kk, 'totdeg', P.total_degree(), 'degy2', sp.degree(p, Y[2]), 'c y0^8', P.coeff_monomial(Y[0]**8),
              'factors', [sp.Poly(f, Y[2], Y[1], Y[0]).total_degree() for f, e in sp.factor_list(p, extension=I)[1]],
              'disc!=0', sp.expand(disc) != 0, flush=True)
