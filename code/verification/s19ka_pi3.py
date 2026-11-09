import sys; sys.path.insert(0, r'D:\ProblemaBase\work\CHECK\sympy')
import sympy as sp, time
from s19ka_common import *
N = 3
kk = (1, 2, 4)
Y = ysyms(6)
U, V, fk, g, Gh = build_UV(N, [sp.Integer(x) for x in kk], Y)
rs = remainder_coeffs(U, V, fk, N)
t = time.time()
# resultant-free route: groebner lex eliminating y5,y4
G = sp.groebner(rs, Y[5], Y[4], Y[3], Y[2], Y[1], Y[0], order='lex')
el = [p for p in G.exprs if not ({Y[4], Y[5]} & p.free_symbols)]
print('time', time.time()-t, 'n elim', len(el), flush=True)
for p in el:
    P = sp.Poly(p, Y[3], Y[2], Y[1], Y[0])
    print('total deg', P.total_degree(), 'deg y3', sp.degree(p, Y[3]), 'coeff y0^20', P.coeff_monomial(Y[0]**20), 'LC', P.coeff_monomial(Y[3]**8), flush=True)
