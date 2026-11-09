# S-CHECK-F10-B2 . controllo indipendente di L8-a (forma iniziale del generatore aggiunto per K = 2N).
# Per N = 1, 2 si verifica sui getti esatti dell'N-solitone di Hirota (u = 2 (log f)'') che
#   y_{2N} = Phi(k; y_0..y_{2N-1})  con Phi polinomio pesato-omogeneo (peso y_j = j+2, peso k = 1)
# e che la forma iniziale (k = 0) e' y_{2N} - Phi(0; y), monica in y_{2N}.
# N = 1: y_2 = c1 y_0 - 3 y_0^2 ; N = 2: y_4 + 10 y0 y2 + 5 y1^2 + 10 y0^3 + c1 (y2 + 3 y0^2) + c2 y0 = 0,
# con (c1, c2) da determinare e confrontare con le funzioni simmetriche di k_i^2.
import sympy as sp, itertools, random
ok = []
def rep(name, c):
    ok.append(bool(c)); print(('OK  ' if c else 'FAIL') + ' ' + name)
x = sp.Symbol('x', real=True)
def jets(kv, d0, n):
    N = len(kv); f = 0
    for r in range(N+1):
        for S in itertools.combinations(range(N), r):
            a = sp.Mul(*[((kv[i]-kv[j])/(kv[i]+kv[j]))**2 for i, j in itertools.combinations(S, 2)])
            f += a*sp.exp(sum(kv[i]*x + d0[i] for i in S))
    u = 2*sp.diff(sp.log(f), x, 2)
    return [sp.diff(u, x, j) for j in range(n+1)]
random.seed(3)
# N = 1
kv = [sp.Rational(3, 2)]; Y = jets(kv, [sp.Rational(1, 3)], 2)
worst = 0
for xx in ['-1.1', '0.2', '0.9', '2.3']:
    y = [sp.N(t.subs(x, sp.Rational(xx)), 50) for t in Y]
    worst = max(worst, abs(y[2] - (kv[0]**2*y[0] - 3*y[0]**2)))
rep('N=1: y_2 = k^2 y_0 - 3 y_0^2 (residuo %s)' % sp.N(worst, 3), worst < 1e-40)
# N = 2
for kv in ([sp.Rational(1), sp.Rational(5, 2)], [sp.Rational(3, 4), sp.Rational(7, 5)]):
    Y = jets(kv, [sp.Rational(1, 5), sp.Rational(-2, 7)], 4)
    pts = ['-1.7', '-0.3', '0.4', '1.2', '2.6']
    rows = []
    for xx in pts:
        y = [sp.N(t.subs(x, sp.Rational(xx)), 60) for t in Y]
        G3 = y[4] + 10*y[0]*y[2] + 5*y[1]**2 + 10*y[0]**3
        rows.append((y[2] + 3*y[0]**2, y[0], -G3))
    M = sp.Matrix([[r[0], r[1]] for r in rows[:2]]); rhs = sp.Matrix([r[2] for r in rows[:2]])
    c1, c2 = list(M.LUsolve(rhs))
    res = max(abs(r[0]*c1 + r[1]*c2 - r[2]) for r in rows[2:])
    e1 = abs(c1 + (kv[0]**2 + kv[1]**2)); e2 = abs(c2 - kv[0]**2*kv[1]**2)
    rep('N=2 k=%s: relazione y_4 = Phi(k; y_0..y_3) sui getti (residuo %s); c1 = -(k1^2+k2^2) (err %s), c2 = k1^2 k2^2 (err %s)'
        % (kv, sp.N(res, 3), sp.N(e1, 3), sp.N(e2, 3)), res < 1e-40 and e1 < 1e-40 and e2 < 1e-40)
# omogeneita' pesata e forma iniziale
K1, K2 = sp.symbols('k1 k2'); y = sp.symbols('y0:5'); lam = sp.Symbol('lam')
Phi = -(10*y[0]*y[2] + 5*y[1]**2 + 10*y[0]**3) + (K1**2 + K2**2)*(y[2] + 3*y[0]**2) - K1**2*K2**2*y[0]
sc = {K1: lam*K1, K2: lam*K2, **{y[j]: lam**(j+2)*y[j] for j in range(5)}}
rep('Phi pesato-omogeneo di peso 6 = peso di y_4', sp.expand(Phi.subs(sc, simultaneous=True) - lam**6*Phi) == 0)
G = y[4] - Phi
# componente di peso massimo in y: si pesa solo y (k peso 0) e si prende la parte di peso 6
ext = sp.Poly(sp.expand(G.subs({y[j]: lam**(j+2)*y[j] for j in range(5)}, simultaneous=True)), lam)
top = ext.coeff_monomial(lam**6)
rep('forma iniziale = y_4 - Phi(0; y) = %s' % sp.expand(top), sp.expand(top - G.subs({K1: 0, K2: 0})) == 0)
rep('forma iniziale monica di grado 1 in y_4', sp.Poly(top, y[4]).degree() == 1 and sp.Poly(top, y[4]).LC() == 1)
print('TOTALE: %d/%d OK' % (sum(ok), len(ok)))
