import sys; sys.path.insert(0, r'D:\ProblemaBase\work\CHECK\sympy')
import sympy as sp
from s19ka_common import *

# L4 direct: k=0, jets y0=c=1, y1..yN=0, y_{N+1}..y_{2N-1} free unknowns -> F=0 must be inconsistent
for N in range(1, 7):
    Y = ysyms(2*N+1)
    U, V, fk, g, Gh = build_UV(N, [sp.Integer(0)]*N, Y)
    rs = remainder_coeffs(U, V, fk, N)
    sub = {Y[0]: 1}
    for j in range(1, N+1): sub[Y[j]] = 0
    free = list(Y[N+1:2*N])
    eqs = [sp.expand(r.subs(sub)) for r in rs]
    if free:
        G = sp.groebner(eqs, *free, order='grevlex')
        print('N', N, 'free', free, 'GB =', list(G.exprs)[:3], flush=True)
    else:
        print('N', N, 'eqs', eqs, flush=True)
    # also: check the formula -t_{N+1}/(N+2)
# also check L4 via (U,V)-coordinates check of T1(a) rank: at k=0, fibre over y0..y_{N-1}=(1,0..) count solutions
for N in range(1, 5):
    Y = ysyms(2*N+1)
    U, V, fk, g, Gh = build_UV(N, [sp.Integer(0)]*N, Y)
    rs = remainder_coeffs(U, V, fk, N)
    sub = {Y[0]: 1}
    for j in range(1, N): sub[Y[j]] = 0
    free = list(Y[N:2*N])
    eqs = [sp.expand(r.subs(sub)) for r in rs]
    G = sp.groebner(eqs, *free, order='lex')
    last = [p for p in G.exprs if set(p.free_symbols) <= {Y[N]}]
    print('N', N, 'fibre over (1,0..0) at k=0: univariate in y_N:', [sp.factor(p) for p in last], 'deg', [sp.degree(p, Y[N]) for p in last], flush=True)
