# OP-F5C: polinomi di Gelfand-Dickey, mappa triangolare getti <-> (U,V), verifica (Nov) e U | V^2 - R sugli N-solitoni.
# Convenzione: u_t + 6 u u_x + u_xxx = 0, u = 2 D^2 log f, L = -d^2 - u.
import sympy as sp, itertools, sys
NMAX = 6
y = sp.symbols('y0:%d' % (2*NMAX+6))
def D(p):
    return sum(sp.diff(p, y[j])*y[j+1] for j in range(len(y)-1))
def wt_monomials(w):
    # monomi in y_j (peso j+2) di peso esattamente w
    res = []
    def rec(j, rem, cur):
        if rem == 0:
            res.append(cur); return
        if j+2 > rem: return
        # use y_j some times
        k = 0
        while (j+2)*k <= rem:
            rec(j+1, rem-(j+2)*k, cur*y[j]**k)
            k += 1
    rec(0, w, sp.Integer(1))
    return res
def lenard_rhs(g):
    # -(1/4)(g''' + 4 u g' + 2 u' g)
    return -sp.Rational(1,4)*(D(D(D(g))) + 4*y[0]*D(g) + 2*y[1]*g)
g = [sp.Integer(1)]
for j in range(1, NMAX+2):
    rhs = sp.expand(lenard_rhs(g[-1]))
    mons = wt_monomials(2*j)
    cs = sp.symbols('c0:%d' % len(mons))
    ans = sum(c*m for c, m in zip(cs, mons))
    sol = sp.solve(sp.Poly(sp.expand(D(ans) - rhs), *y).coeffs(), cs, dict=True)
    assert sol, j
    gj = sp.expand(ans.subs(sol[0]).subs({c: 0 for c in cs}))
    g.append(gj)
for j in range(0, 5):
    print('g_%d =' % j, g[j])
# controllo: g_j su potenziale costante = coefficienti di (1+c/lam)^(-1/2)
c, lam = sp.symbols('c lam')
ser = sp.series((1+c/lam)**sp.Rational(-1,2), lam, sp.oo, NMAX+3).removeO()
ok = True
for j in range(NMAX+2):
    val = g[j].subs({y[0]: c, **{y[i]: 0 for i in range(1, len(y))}})
    coeff = sp.expand(ser).coeff(lam, -j) if j > 0 else 1
    ok &= sp.simplify(val - coeff) == 0
print('[GD-const] g_j(costante c) = coeff di (1+c/lam)^(-1/2):', 'OK' if ok else 'FAIL')
# triangolarita: g_j = cost*y_{2j-2} + (polinomio nei getti di ordine < 2j-2)
ok = True
for j in range(1, NMAX+2):
    lin = sp.diff(g[j], y[2*j-2])
    ok &= lin.is_number and lin != 0
    ok &= all(sp.diff(g[j], y[i]) == 0 for i in range(2*j-1, len(y)))
print('[GD-tri] g_j = c_j y_{2j-2} + ordine inferiore, c_j != 0 (j<=%d):' % (NMAX+1), 'OK' if ok else 'FAIL')
import pickle
pickle.dump([str(x) for x in g], open(sys.argv[1] if len(sys.argv) > 1 else 'opf5c_gd.pkl', 'wb'))
