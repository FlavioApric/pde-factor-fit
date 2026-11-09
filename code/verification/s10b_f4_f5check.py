# S10-OPEN-B · ricontrollo di F5 (N=3) di s10b_f4.py: residuo relativo a |psi| e dipendenza dalla precisione (solo verifica).
import sympy as sp, itertools, mpmath as mp
x = sp.Symbol('x', real=True); kk = sp.Symbol('k')
N = 3
kap = [sp.Rational(p, 2) for p in [1, 3, 4]]; c = [sp.Rational(q, 5) for q in [3, 7, 2]]
phi = [sp.exp(-kap[j]*x) + (-1)**j*c[j]*sp.exp(kap[j]*x) for j in range(N)]
W = sp.Matrix(N, N, lambda a, b: sp.diff(phi[b], x, a)).det()
E = sp.exp(sp.I*kk*x)
WE = sp.Matrix(N+1, N+1, lambda a, b: sp.diff((phi+[E])[b], x, a)).det()
u = 2*sp.diff(sp.log(W), x, 2)
psi = WE/W
res = -sp.diff(psi, x, 2) - u*psi - kk**2*psi
f = sp.lambdify((x, kk), res, 'mpmath'); g = sp.lambdify((x, kk), psi, 'mpmath')
for dps in (40, 80, 120):
    mp.mp.dps = dps
    worst = max(abs(f(mp.mpf(xx), mp.mpf(kv)))/abs(g(mp.mpf(xx), mp.mpf(kv))) for xx in ('-1.3', '0.2', '2.1') for kv in ('0.7', '1.9'))
    print('dps=%d  max |res|/|psi| = %s' % (dps, mp.nstr(worst, 3)))
# valutazione senza lambdify: sostituzione esatta (x, k razionali) ed evalf a 60 cifre
worst = 0
for xx in ('-13/10', '1/5', '21/10'):
    for kv in ('7/10', '19/10'):
        s = {x: sp.Rational(xx), kk: sp.Rational(kv)}
        r = abs(sp.N(res.subs(s), 60)) / abs(sp.N(psi.subs(s), 60))
        worst = max(worst, r)
print('evalf esatto: max |res|/|psi| = %s' % sp.N(worst, 3))
