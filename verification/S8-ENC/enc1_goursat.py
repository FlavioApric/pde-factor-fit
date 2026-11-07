# S8-ENC — verifica di ENC-1 / ENC-U1 (operatore di trasformazione di Volterra simmetrico), punto base x0 = 0.
# Goursat in coordinate caratteristiche xi = x+s, eta = x-s:
#   H(xi,eta) = k0 + 1/2 int_0^{xi/2} q + 1/4 int_0^xi int_0^eta q((a+b)/2) H(a,b) db da
# K(x,s) = H(x+s, x-s);  T f(x) = f(x) + int_{-x}^{x} K(x,s) f(s) ds.
# Con approssimazioni successive troncate al passo N il residuo dell'intertwining deve essere O(x^{alto}).
import sympy as sp

x, s, a, b, X, E = sp.symbols('x s a b xi eta')
k0 = sp.Symbol('k0')
res = []
def report(name, ok, extra=''):
    res.append((name, ok)); print(('OK  ' if ok else 'FAIL') + ' ' + name + ' ' + str(extra))

def goursat(qfun, N, k0val=0, sign=+1, arg='x'):
    # sign=+1, arg='x': 4 H_{xi eta} = q(x) H  (nucleo di T, L_q T = T L_0)
    # sign=-1, arg='s': 4 H_{xi eta} = -q(s) H (nucleo di T', L_0 T' = T' L_q)
    u = sp.Symbol('u')
    base = k0val + sign*sp.Rational(1, 2)*sp.integrate(qfun(u), (u, 0, X/2))
    Hn = base
    for _ in range(N):
        qa = qfun((a+b)/2) if arg == 'x' else qfun((a-b)/2)
        integrand = sp.expand(qa*Hn.subs({X: a, E: b}, simultaneous=True))
        Hn = sp.expand(base + sign*sp.Rational(1, 4)*sp.integrate(sp.integrate(integrand, (b, 0, E)), (a, 0, X)))
    return Hn

def T_apply(Hxe, f):
    K = Hxe.subs({X: x+s, E: x-s}, simultaneous=True)
    return sp.expand(f.subs(s, x) + sp.integrate(sp.expand(K*f), (s, -x, x)))

def lowest_order(expr):
    p = sp.Poly(sp.expand(expr), x)
    if p.is_zero: return 10**9
    return min(m[0] for m in p.monoms())

N = 5
fpoly = 1 + 2*s - s**2 + 3*s**3 + s**5   # f generica (polinomiale), nessuna condizione al bordo
for name, qf in [('q = x', lambda w: w), ('q = 1 + w^2 (q(x)=1+x^2)', lambda w: 1 + w**2)]:
    H = goursat(qf, N)
    Tf = T_apply(H, fpoly)
    L0f = -sp.diff(fpoly, s, 2)
    resid = sp.expand(-sp.diff(Tf, x, 2) + qf(x)*Tf - T_apply(H, L0f))
    lo = lowest_order(resid)
    report('ENC-1 intertwining L_q T f = T L_0 f, %s: residuo O(x^%d)' % (name, lo), lo >= 2*N, '')
    # dati di Cauchy in 0
    report('ENC-1 dati di Cauchy conservati, %s' % name,
           sp.simplify(Tf.subs(x, 0) - fpoly.subs(s, 0)) == 0 and sp.simplify(sp.diff(Tf, x).subs(x, 0) - sp.diff(fpoly, s).subs(s, 0)) == 0)
    # condizioni di Goursat
    K = H.subs({X: x+s, E: x-s}, simultaneous=True)
    report('ENC-1 K(x,-x)=0 e K(x,x)=1/2 int q, %s' % name,
           sp.expand(K.subs(s, -x)) == 0 and sp.expand(K.subs(s, x) - sp.Rational(1, 2)*sp.integrate(qf(sp.Symbol('u')), (sp.Symbol('u'), 0, x))) == 0)
    # inverso: T' da Goursat con -q(s); T'T f = f + O(alto)
    Hp = goursat(qf, N, sign=-1, arg='s')
    TpTf = T_apply(Hp, Tf.subs(x, s))
    lo2 = lowest_order(TpTf - fpoly.subs(s, x))
    report("ENC-1 inverso T'T f = f, %s: errore O(x^%d)" % (name, lo2), lo2 >= 2*N, '')
    # T' intreccia nel verso opposto: L_0 T' g = T' L_q g
    g = fpoly
    Tpg = T_apply(Hp, g)
    resid3 = sp.expand(-sp.diff(Tpg, x, 2) - T_apply(Hp, -sp.diff(g, s, 2) + qf(s)*g))
    lo3 = lowest_order(resid3)
    report("ENC-1 L_0 T' = T' L_q, %s: residuo O(x^%d)" % (name, lo3), lo3 >= 2*N, '')

# ENC-U1: famiglia a un parametro k0 (K(x,-x)=k0, K(x,x)=k0+1/2 int q): tutti intrecciano, solo k0=0 conserva Cauchy
qf = lambda w: w
Hk = goursat(qf, N, k0val=k0)
Tf = T_apply(Hk, fpoly)
resid = sp.expand(-sp.diff(Tf, x, 2) + qf(x)*Tf - T_apply(Hk, -sp.diff(fpoly, s, 2)))
report('ENC-U1 T_{k0} intreccia per ogni k0 (residuo O(x^%d))' % lowest_order(resid.subs(k0, sp.Rational(7, 3))), lowest_order(resid.subs(k0, sp.Rational(7, 3))) >= 2*N)
d1 = sp.simplify(sp.diff(Tf, x).subs(x, 0) - sp.diff(fpoly, s).subs(s, 0))
report('ENC-U1 (T_{k0} f)\'(0) = f\'(0) + 2 k0 f(0)', sp.simplify(d1 - 2*k0*fpoly.subs(s, 0)) == 0, d1)
# q = 0, K = k0: I + k0 int_{-x}^{x} commuta con L_0 (commutante non banale)
Tk = fpoly.subs(s, x) + k0*sp.integrate(fpoly, (s, -x, x))
r = sp.expand(-sp.diff(Tk, x, 2) - (-sp.diff(fpoly, s, 2)).subs(s, x) - k0*sp.integrate(-sp.diff(fpoly, s, 2), (s, -x, x)))
report('ENC-U1 q=0: I + k0 int_{-x}^{x} commuta con L_0', r == 0, r)

# Dipendenza dal punto base per q = c costante: T_{x0} e^{ikx} = e^{ikx0}[cos mu(x-x0) + i k sin(mu(x-x0))/mu], mu^2 = k^2 - c
c, kk = sp.Rational(2), sp.Rational(3, 2)
mu = sp.sqrt(kk**2 - c)
def Tx0(x0):
    return sp.exp(sp.I*kk*x0)*(sp.cos(mu*(x-x0)) + sp.I*kk*sp.sin(mu*(x-x0))/mu)
y0, y1 = Tx0(0), Tx0(sp.Rational(1, 5))
ok_eig = all(sp.simplify(-sp.diff(yy, x, 2) + c*yy - kk**2*yy) == 0 for yy in (y0, y1))
diff_val = complex(sp.N((y0 - y1).subs(x, sp.Rational(1, 3))))
report('punto base: T_0 e^{ikx} != T_{1/5} e^{ikx} per q = 2 (entrambe autofunzioni)', ok_eig and abs(diff_val) > 1e-3, diff_val)

print('\nTOTALE: %d/%d OK' % (sum(1 for _, o in res if o), len(res)))
