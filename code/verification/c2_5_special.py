"""PR-C2a / C2.5 -- ODE delle funzioni speciali.
Strategia (esatta, per parametri GENERICI dove possibile):
 (A) serie ipergeometriche 2F1, 1F1, 0F1: verifica della ricorrenza dei coefficienti per k generico
     (=> T e = 0 come identita' formale esatta su tutta la serie);
 (B) identita' di operatore: ogni ODE speciale e' l'operatore ipergeometrico/confluente dopo un cambio
     di variabile e/o un fattore di gauge (Jacobi, Gegenbauer, Legendre, Chebyshev, Legendre associate,
     Hermite, Laguerre, Bessel, Airy);
 (C) verifiche dirette con le funzioni di SymPy (parametri simbolici o n = 0..6);
 (D) dati di Gram per C1 (ortogonalita' con peso) e Hermite functions come autofunzioni di -D^2 + x^2;
 (E) sferoidali: ricorrenza a TRE termini (non ipergeometrica), limite c -> 0 = Legendre.
Eseguire: D:\\ProblemaBase\\.venv\\Scripts\\python.exe -I c2_5_special.py
"""
import sys
import sympy as sp
sys.stdout.reconfigure(encoding='utf-8')

x, z, k = sp.symbols('x z k')
a, b, c, nu, n, alpha, beta, lam, m = sp.symbols('a b c nu n alpha beta lambda m')
RES = []


def check(name, expr):
    if isinstance(expr, sp.MatrixBase):
        ok = all(sp.simplify(sp.expand(e)) == 0 for e in expr)
    else:
        ok = sp.simplify(sp.expand(expr)) == 0
    RES.append(ok)
    print(('[OK]  ' if ok else '[FAIL]') + ' ' + name)


w = sp.Function('w')

# ---------------- (A) serie ipergeometriche --------------------------------------------------
H2 = lambda f: z*(1 - z)*sp.diff(f, z, 2) + (c - (a + b + 1)*z)*sp.diff(f, z) - a*b*f
K1 = lambda f: z*sp.diff(f, z, 2) + (b - z)*sp.diff(f, z) - a*f
Z0 = lambda f: z*sp.diff(f, z, 2) + b*sp.diff(f, z) - f
zk = z**k
check('2F1: H[z^k] = k(k-1+c) z^{k-1} - (k+a)(k+b) z^k',
      sp.expand(H2(zk) - (k*(k - 1 + c)*z**(k - 1) - (k + a)*(k + b)*z**k)))
t2 = lambda j: sp.rf(a, j)*sp.rf(b, j)/(sp.rf(c, j)*sp.factorial(j))
check('2F1: (k+1)(k+c) t_{k+1} = (k+a)(k+b) t_k  per k generico',
      sp.gammasimp(sp.expand_func((k + 1)*(k + c)*t2(k + 1)/t2(k))) - (k + a)*(k + b))
check('1F1: K[z^k] = k(k-1+b) z^{k-1} - (k+a) z^k',
      sp.expand(K1(zk) - (k*(k - 1 + b)*z**(k - 1) - (k + a)*z**k)))
t1 = lambda j: sp.rf(a, j)/(sp.rf(b, j)*sp.factorial(j))
check('1F1: (k+1)(k+b) t_{k+1} = (k+a) t_k', sp.gammasimp(sp.expand_func((k + 1)*(k + b)*t1(k + 1)/t1(k))) - (k + a))
t0 = lambda j: 1/(sp.rf(b, j)*sp.factorial(j))
check('0F1: Z[z^k] = k(k-1+b) z^{k-1} - z^k', sp.expand(Z0(zk) - (k*(k - 1 + b)*z**(k - 1) - z**k)))
check('0F1: (k+1)(k+b) t_{k+1} = t_k', sp.gammasimp(sp.expand_func((k + 1)*(k + b)*t0(k + 1)/t0(k))) - 1)
# seconde soluzioni (gauge z^{1-c}): se v in ker H(a-c+1,b-c+1,2-c) allora z^{1-c} v in ker H(a,b,c)
v = w(z)
sub2 = {a: a - c + 1, b: b - c + 1, c: 2 - c}
Hv = H2(v).subs(sub2, simultaneous=True)
lhs = H2(z**(1 - c)*v)
# lhs deve essere z^{-c} * z * Hv  (cioe' proporzionale a Hv)
check('2F1: H_{a,b,c}[z^{1-c} v] = z^{1-c} H_{a-c+1,b-c+1,2-c}[v]', sp.simplify(sp.expand(lhs/z**(1 - c)) - Hv))
Kv = K1(v).subs({a: a - b + 1, b: 2 - b}, simultaneous=True)
check('1F1: K_{a,b}[z^{1-b} v] = z^{1-b} K_{a-b+1,2-b}[v]', sp.simplify(sp.expand(K1(z**(1 - b)*v)/z**(1 - b)) - Kv))

# ---------------- (B) identita' di operatore -----------------------------------------------------
y = sp.Function('y')
# Jacobi: (1-x^2)y'' + (beta-alpha-(alpha+beta+2)x) y' + n(n+alpha+beta+1) y ; x = 1 - 2z
Jac = lambda f, X: (1 - X**2)*sp.diff(f, X, 2) + (beta - alpha - (alpha + beta + 2)*X)*sp.diff(f, X) \
    + n*(n + alpha + beta + 1)*f
JacZ = Jac(w(sp.Rational(1, 2) - x/2), x).subs(x, 1 - 2*z).doit()
Hab = H2(w(z)).subs({a: -n, b: n + alpha + beta + 1, c: alpha + 1}, simultaneous=True)
check('Jacobi(x=1-2z) = H(a=-n, b=n+alpha+beta+1, c=alpha+1)', sp.simplify(JacZ - Hab))
# Gegenbauer = Jacobi con alpha=beta=lam-1/2 ; Legendre lam=1/2 ; Chebyshev T lam=0 ; Chebyshev U lam=1
Geg = lambda f, X: (1 - X**2)*sp.diff(f, X, 2) - (2*lam + 1)*X*sp.diff(f, X) + n*(n + 2*lam)*f
check('Gegenbauer = Jacobi(alpha=beta=lam-1/2)',
      sp.simplify(Geg(y(x), x) - Jac(y(x), x).subs({alpha: lam - sp.Rational(1, 2), beta: lam - sp.Rational(1, 2)})))
# Legendre associate: y = (1-x^2)^{m/2} v(x), v in ker Gegenbauer(lam = m+1/2, n -> n-m)
V = sp.Function('V')(x)
Leg_assoc = lambda f: (1 - x**2)*sp.diff(f, x, 2) - 2*x*sp.diff(f, x) + (n*(n + 1) - m**2/(1 - x**2))*f
lhsA = Leg_assoc((1 - x**2)**(m/2)*V)
rhsA = (1 - x**2)**(m/2)*Geg(V, x).subs({lam: m + sp.Rational(1, 2), n: n - m}, simultaneous=True)
check('Legendre associate: gauge (1-x^2)^{m/2} -> Gegenbauer(m+1/2, n-m)', sp.simplify(sp.simplify(sp.powsimp(sp.expand(lhsA/(1 - x**2)**(m/2)), force=True)) - rhsA/(1 - x**2)**(m/2)))
# Hermite y'' - 2xy' + 2n y = 0 ; y(x) = w(x^2) -> 4 [ z w'' + (1/2 - z) w' + (n/2) w ]
He = lambda f: sp.diff(f, x, 2) - 2*x*sp.diff(f, x) + 2*n*f
HeZ = He(w(x**2)).doit()
Kh = K1(w(z)).subs({a: -n/2, b: sp.Rational(1, 2)}, simultaneous=True).subs(z, x**2)
check('Hermite pari: He[w(x^2)] = 4 Kummer(a=-n/2, b=1/2)[w](x^2)', sp.simplify(HeZ - 4*Kh.doit()))
# Laguerre x y'' + (alpha+1-x) y' + n y  = Kummer(a=-n, b=alpha+1) (stesso operatore)
La = lambda f: z*sp.diff(f, z, 2) + (alpha + 1 - z)*sp.diff(f, z) + n*f
check('Laguerre = Kummer(a=-n, b=alpha+1)', sp.simplify(La(w(z)) - K1(w(z)).subs({a: -n, b: alpha + 1})))
# Bessel: y = x^nu W(-x^2/4), W in ker 0F1(b=nu+1)  -> x^2 y'' + x y' + (x^2 - nu^2) y = 0
Bes = lambda f: x**2*sp.diff(f, x, 2) + x*sp.diff(f, x) + (x**2 - nu**2)*f
zz = -x**2/4
# approccio robusto: funzione di prova con derivate simboliche
f0, f1, f2 = sp.symbols('f0 f1 f2')
Y = x**nu*f0
dY = nu*x**(nu - 1)*f0 + x**nu*f1*(-x/2)
d2Y = (nu*(nu - 1)*x**(nu - 2)*f0 + 2*nu*x**(nu - 1)*f1*(-x/2) + x**nu*(f2*(x**2/4) + f1*(-sp.Rational(1, 2))))
BesY = x**2*d2Y + x*dY + (x**2 - nu**2)*Y
rule = {f2: -((nu + 1)*f1 - f0)/zz}
check('Bessel: x^nu 0F1(;nu+1;-x^2/4) e\' in ker Bessel (via ODE 0F1)', sp.simplify(BesY.subs(rule)))
# Airy: y = sqrt(x) Z(zeta), zeta = 2/3 x^{3/2}, Z Bessel modificata d'ordine 1/3 -> y'' = x y
xi = sp.Rational(2, 3)*x**sp.Rational(3, 2)
g0, g1, g2 = sp.symbols('g0 g1 g2')
dxi = sp.diff(xi, x); d2xi = sp.diff(xi, x, 2)
Yy = sp.sqrt(x)*g0
dYy = sp.diff(sp.sqrt(x), x)*g0 + sp.sqrt(x)*g1*dxi
d2Yy = sp.diff(sp.sqrt(x), x, 2)*g0 + 2*sp.diff(sp.sqrt(x), x)*g1*dxi + sp.sqrt(x)*(g2*dxi**2 + g1*d2xi)
mod_bessel_rule = {g2: -(xi*g1 - (xi**2 + sp.Rational(1, 9))*g0)/xi**2}
check('Airy: sqrt(x) I/K_{1/3}(2/3 x^{3/2}) risolve y\'\' = x y', sp.simplify((d2Yy - x*Yy).subs(mod_bessel_rule)))

# ---------------- (C) verifiche dirette con SymPy ------------------------------------------------
X = sp.symbols('X')
for name, F in (('J_nu', sp.besselj(nu, X)), ('Y_nu', sp.bessely(nu, X))):
    check(f'Bessel: {name} in ker x^2D^2+xD+(x^2-nu^2)',
          sp.simplify(X**2*sp.diff(F, X, 2) + X*sp.diff(F, X) + (X**2 - nu**2)*F))
# Bessel modificata: identita' esatta di operatore y(x) = Z(i x), Z in ker Bessel => y in ker Bessel modificata
h0, h1, h2 = sp.symbols('h0 h1 h2')   # Z, Z', Z'' valutate in i x
modB = X**2*(sp.I**2*h2) + X*(sp.I*h1) - (X**2 + nu**2)*h0
besB_at_iX = (sp.I*X)**2*h2 + (sp.I*X)*h1 + ((sp.I*X)**2 - nu**2)*h0
check('Bessel modificata: x^2 y2+x y1-(x^2+nu^2)y = Bessel[Z](ix) per y=Z(ix)  (I_nu, K_nu)', modB - besB_at_iX)
# controllo numerico (solo controllo, non metodo): residuo di I_{1/3}, K_{1/3} in x = 1.7
for F in (sp.besseli(sp.Rational(1, 3), X), sp.besselk(sp.Rational(1, 3), X)):
    val = (X**2*sp.diff(F, X, 2) + X*sp.diff(F, X) - (X**2 + sp.Rational(1, 9))*F).subs(X, sp.Rational(17, 10)).evalf(30)
    ok = bool(abs(val) < 1e-25); RES.append(ok)
    print(('[OK]  ' if ok else '[FAIL]') + f' controllo numerico {F}: residuo = {sp.N(val, 3)}')
for F in (sp.airyai(X), sp.airybi(X)):
    check(f'Airy: {F} in ker D^2 - x', sp.diff(F, X, 2) - X*F)
okP = all(sp.expand((1 - X**2)*sp.diff(sp.legendre(N, X), X, 2) - 2*X*sp.diff(sp.legendre(N, X), X)
                    + N*(N + 1)*sp.legendre(N, X)) == 0 for N in range(7))
RES.append(okP); print(('[OK]  ' if okP else '[FAIL]') + ' Legendre P_n, n=0..6')
okA = all(sp.simplify((1 - X**2)*sp.diff(sp.assoc_legendre(N, M, X), X, 2) - 2*X*sp.diff(sp.assoc_legendre(N, M, X), X)
                      + (N*(N + 1) - M**2/(1 - X**2))*sp.assoc_legendre(N, M, X)) == 0
          for N in range(5) for M in range(N + 1))
RES.append(okA); print(('[OK]  ' if okA else '[FAIL]') + ' Legendre associate P_n^m, n<=4')
okH = all(sp.expand(sp.diff(sp.hermite(N, X), X, 2) - 2*X*sp.diff(sp.hermite(N, X), X) + 2*N*sp.hermite(N, X)) == 0
          for N in range(7))
RES.append(okH); print(('[OK]  ' if okH else '[FAIL]') + ' Hermite H_n, n=0..6')
okL = all(sp.simplify(X*sp.diff(sp.assoc_laguerre(N, alpha, X), X, 2) + (alpha + 1 - X)*sp.diff(sp.assoc_laguerre(N, alpha, X), X)
                      + N*sp.assoc_laguerre(N, alpha, X)) == 0 for N in range(6))
RES.append(okL); print(('[OK]  ' if okL else '[FAIL]') + ' Laguerre L_n^alpha (alpha simbolico), n=0..5')
okT = all(sp.expand((1 - X**2)*sp.diff(sp.chebyshevt(N, X), X, 2) - X*sp.diff(sp.chebyshevt(N, X), X)
                    + N**2*sp.chebyshevt(N, X)) == 0 for N in range(7))
okU = all(sp.expand((1 - X**2)*sp.diff(sp.chebyshevu(N, X), X, 2) - 3*X*sp.diff(sp.chebyshevu(N, X), X)
                    + N*(N + 2)*sp.chebyshevu(N, X)) == 0 for N in range(7))
RES += [okT, okU]; print(('[OK]  ' if okT and okU else '[FAIL]') + ' Chebyshev T_n, U_n, n=0..6')
okG = all(sp.simplify(Geg(sp.gegenbauer(N, lam, X), X).subs(n, N)) == 0 for N in range(5))
okJ = all(sp.simplify(Jac(sp.jacobi(N, alpha, beta, X), X).subs(n, N)) == 0 for N in range(4))
RES += [okG, okJ]; print(('[OK]  ' if okG and okJ else '[FAIL]') + ' Gegenbauer C_n^lam (n<=4), Jacobi P_n^(a,b) (n<=3), parametri simbolici')
# Chebyshev T come funzione trigonometrica: T_n(cos th) = cos(n th) (nucleo di D_th^2 + n^2)
th = sp.symbols('theta')
okTc = all(sp.expand(sp.expand_trig(sp.chebyshevt(N, sp.cos(th)) - sp.cos(N*th))) == 0 for N in range(6))
RES.append(okTc); print(('[OK]  ' if okTc else '[FAIL]') + ' T_n(cos th) = cos(n th): Chebyshev = Fourier in theta')

# ---------------- (D) dati di Gram (C1) -----------------------------------------------------------
G_leg = sp.Matrix(4, 4, lambda i, j: sp.integrate(sp.legendre(i, X)*sp.legendre(j, X), (X, -1, 1)))
check('Gram Legendre = diag(2/(2n+1))', G_leg - sp.diag(*[sp.Rational(2, 2*i + 1) for i in range(4)]))
G_her = sp.Matrix(4, 4, lambda i, j: sp.integrate(sp.exp(-X**2)*sp.hermite(i, X)*sp.hermite(j, X), (X, -sp.oo, sp.oo)))
check('Gram Hermite (peso e^{-x^2}) = diag(sqrt(pi) 2^n n!)',
      G_her - sp.diag(*[sp.sqrt(sp.pi)*2**i*sp.factorial(i) for i in range(4)]))
G_lag = sp.Matrix(3, 3, lambda i, j: sp.integrate(sp.exp(-X)*X**2*sp.assoc_laguerre(i, 2, X)*sp.assoc_laguerre(j, 2, X), (X, 0, sp.oo)))
check('Gram Laguerre alpha=2 (peso x^2 e^{-x}) = diag(Gamma(n+3)/n!)',
      G_lag - sp.diag(*[sp.gamma(i + 3)/sp.factorial(i) for i in range(3)]))
G_ch = sp.Matrix(3, 3, lambda i, j: sp.integrate(sp.chebyshevt(i, sp.cos(th))*sp.chebyshevt(j, sp.cos(th)), (th, 0, sp.pi)))
check('Gram Chebyshev T (peso (1-x^2)^{-1/2}) = diag(pi, pi/2, pi/2)', G_ch - sp.diag(sp.pi, sp.pi/2, sp.pi/2))
# Hermite functions psi_n = e^{-x^2/2} H_n: autofunzioni di -D^2 + x^2 con autovalore 2n+1 (oscillatore)
okHF = all(sp.simplify(-sp.diff(sp.exp(-X**2/2)*sp.hermite(N, X), X, 2) + X**2*sp.exp(-X**2/2)*sp.hermite(N, X)
                       - (2*N + 1)*sp.exp(-X**2/2)*sp.hermite(N, X)) == 0 for N in range(6))
RES.append(okHF); print(('[OK]  ' if okHF else '[FAIL]') + ' Hermite functions: (-D^2 + x^2) psi_n = (2n+1) psi_n, n=0..5')

# ---------------- (E) sferoidali (m = 0) -----------------------------------------------------------
cs, ev = sp.symbols('c lambda_ev')
Sph = lambda f: (1 - X**2)*sp.diff(f, X, 2) - 2*X*sp.diff(f, X) + (ev - cs**2*X**2)*f
check('Sferoidale: S[x^k] = k(k-1)x^{k-2} - (k(k+1)-lambda) x^k - c^2 x^{k+2}  (ricorrenza a 3 termini)',
      sp.expand(Sph(X**k) - (k*(k - 1)*X**(k - 2) - (k*(k + 1) - ev)*X**k - cs**2*X**(k + 2))))
check('Sferoidale con c=0, lambda=n(n+1): coincide con Legendre',
      sp.simplify(Sph(y(X)).subs({cs: 0, ev: n*(n + 1)}) - ((1 - X**2)*sp.diff(y(X), X, 2) - 2*X*sp.diff(y(X), X) + n*(n + 1)*y(X))))
# serie troncata con coefficienti dalla ricorrenza: residuo solo agli ordini >= N
Nt = 10
coef = {0: sp.Integer(1), 1: sp.Integer(0), -1: 0, -2: 0}
for kk in range(0, Nt - 1):
    coef[kk + 2] = ((kk*(kk + 1) - ev)*coef[kk] + cs**2*coef.get(kk - 2, 0))/((kk + 2)*(kk + 1))
S_tr = sum(coef[j]*X**j for j in range(Nt + 1))
resS = sp.Poly(sp.expand(Sph(S_tr)), X)
low = min(mm[0] for mm in resS.monoms())
print('   sferoidale: serie pari troncata a grado 10, ordine minimo del residuo =', low, '(>= 10)')
RES.append(low >= Nt)

print(f'\nTOTALE: {sum(RES)}/{len(RES)} OK')
