"""PR-C2c / Q3: identificabilita' della KdV da 1-solitone vs 2-solitone (dizionario jet {u_t, u u_x, u_xxx, u_x, u_xx, u})."""
import sympy as sp, random
x, t = sp.symbols('x t', real=True)
k1, k2 = sp.Rational(3, 2), sp.Rational(4, 5)
e1 = sp.exp(k1*x - k1**3*t); e2 = sp.exp(k2*x - k2**3*t)
A12 = ((k1 - k2)/(k1 + k2))**2
cases = {'1-solitone': 2*sp.diff(sp.log(1 + e1), x, 2),
         '2-solitone': 2*sp.diff(sp.log(1 + e1 + e2 + A12*e1*e2), x, 2)}
names = ['u_t', 'u u_x', 'u_xxx', 'u_x', 'u_xx', 'u']
random.seed(3)
pts = [(sp.Rational(random.randint(-40, 40), 10), sp.Rational(random.randint(-20, 20), 10)) for _ in range(40)]
for name, u in cases.items():
    feats = [sp.diff(u, t), u*sp.diff(u, x), sp.diff(u, x, 3), sp.diff(u, x), sp.diff(u, x, 2), u]
    M = sp.Matrix([[sp.N(f.subs({x: a, t: b}), 40) for f in feats] for a, b in pts])
    import mpmath as mp; mp.mp.dps = 40
    sv = sorted(mp.svd_r(mp.matrix(M.tolist()), compute_uv=False))
    print(name, ': valori singolari della matrice jet 40x6 ->', [mp.nstr(s, 3) for s in sv])
    # residuo del vettore KdV (1,6,1,0,0,0) e del vettore trasporto (1,0,0,c,0,0)
    print('   |M(1,6,1,0,0,0)| =', sp.N(max(abs(r) for r in M*sp.Matrix([1, 6, 1, 0, 0, 0])), 3),
          ' |M(1,0,0,c,0,0)|, c=k1^2:', sp.N(max(abs(r) for r in M*sp.Matrix([1, 0, 0, k1**2, 0, 0])), 3))

