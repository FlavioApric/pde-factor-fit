"""PR-C2a / C2.4 -- ODE a coefficienti variabili: Euler-Cauchy, Frobenius (equazione indiciale, caso
logaritmico), riduzione d'ordine (Abel), punti singolari irregolari, serie divergenti, WKB, D-finitezza.
Eseguire: D:\\ProblemaBase\\.venv\\Scripts\\python.exe -I c2_4_variable_coeff.py
"""
import sys
import sympy as sp
sys.stdout.reconfigure(encoding='utf-8')

x = sp.symbols('x', positive=True)
r, al, be, a, b, kk = sp.symbols('r alpha beta a b k')
RES = []


def check(name, expr):
    ok = sp.simplify(sp.expand(expr)) == 0
    RES.append(ok)
    print(('[OK]  ' if ok else '[FAIL]') + ' ' + name)


# 1. Euler-Cauchy T = x^2 D^2 + a x D + b  (termini x^2 d^2, x d, 1): simbolo indiciale I(r) = r(r-1)+ar+b
EC = lambda f: x**2*sp.diff(f, x, 2) + a*x*sp.diff(f, x) + b*f
check('Euler-Cauchy: T x^r = I(r) x^r', EC(x**r) - (r*(r - 1) + a*r + b)*x**r)
# radice doppia r0 => x^r0 log x ; I(r) = (r - r0)^2 <=> a = 1 - 2 r0, b = r0^2
r0 = sp.symbols('r0')
check('Euler-Cauchy radice doppia: T[x^r0 log x] = 0', EC(x**r0*sp.log(x)).subs({a: 1 - 2*r0, b: r0**2}))
# radici complesse al +- i be: x^al cos(be log x)
f = x**al*sp.cos(be*sp.log(x))
check('Euler-Cauchy radici complesse: T[x^al cos(be log x)] = 0',
      EC(f).subs({a: 1 - 2*al, b: al**2 + be**2}))
# Euler-Cauchy = coeff. costanti nella variabile log: x D = d/d(log x)
tt = sp.symbols('t')
g = sp.Function('g')
check('x d/dx [g(log x)] = g\'(log x)  (theta = xD <-> d/dt, x = e^t)',
      x*sp.diff(g(sp.log(x)), x) - sp.Subs(sp.Derivative(g(tt), tt), tt, sp.log(x)).doit())

# 2. Frobenius: Bessel di ordine 0, x^2 y'' + x y' + x^2 y = 0 (punto singolare regolare in 0, r = 0 doppia)
B0 = lambda f: x**2*sp.diff(f, x, 2) + x*sp.diff(f, x) + x**2*f
N = 8
y1 = sum((-1)**k*(x/2)**(2*k)/sp.factorial(k)**2 for k in range(N + 1))
res1 = sp.expand(B0(y1))
print('   ordine minimo del residuo di J0 troncata a N=8:', sp.Poly(res1, x).monoms()[-1][0], '(>= 2N+2 = 18)')
RES.append(sp.Poly(res1, x).monoms()[-1][0] >= 2*N + 2)
# verifica esatta della ricorrenza per k generico: c_k = (-1)^k/(4^k k!^2) soddisfa (2k)^2 c_k + c_{k-1} = 0
ck = lambda k: (-1)**k/(4**k*sp.factorial(k)**2)
check('Frobenius J0: (2k)^2 c_k + c_{k-1} = 0 per k generico', sp.combsimp((2*kk)**2*ck(kk) + ck(kk - 1)))
# seconda soluzione logaritmica (caso r1 = r2): Y = J0 log x + sum (-1)^{k+1} H_k (x/2)^{2k}/k!^2
y2 = y1*sp.log(x) + sum((-1)**(k + 1)*sp.harmonic(k)*(x/2)**(2*k)/sp.factorial(k)**2 for k in range(1, N + 1))
res2 = sp.expand(sp.simplify(B0(y2)))
res2 = sp.expand(res2.subs(sp.log(x), 0)) + sp.expand(res2.coeff(sp.log(x)))*0  # i termini con log provengono da res1
lowest = min(m[0] for m in sp.Poly(sp.expand(B0(y2) - B0(y1)*sp.log(x)), x).monoms())
print('   ordine minimo del residuo della 2a soluzione (log) troncata:', lowest, '(>= 2N+2)')
RES.append(lowest >= 2*N + 2)
# equazione indiciale generica: x^2 y'' + x p(x) y' + q(x) y, p(0)=p0, q(0)=q0
p0, q0, p1, q1 = sp.symbols('p0 q0 p1 q1')
ind = sp.expand((x**2*sp.diff(x**r, x, 2) + x*(p0 + p1*x)*sp.diff(x**r, x) + (q0 + q1*x)*x**r)/x**r)
check('Equazione indiciale: coeff. di x^0 = r(r-1) + p0 r + q0', ind.coeff(x, 0) - (r*(r - 1) + p0*r + q0))

# 3. Riduzione d'ordine / formula di Abel: y'' + P y' + Q y = 0, y2 = y1 int exp(-int P)/y1^2
#    Esempio Legendre n=1: (1-x^2)y'' - 2xy' + 2y = 0, y1 = x => y2 = x/2 log((1+x)/(1-x)) - 1 = Q_1
xs = sp.symbols('xs')
Pc = -2*xs/(1 - xs**2)
W = sp.exp(-sp.integrate(Pc, xs))
y2L = sp.simplify(xs*sp.integrate(sp.simplify(W/xs**2), xs))
print('   riduzione d\'ordine Legendre n=1: y2 =', y2L)
check('Riduzione d\'ordine: y2 in ker Legendre(n=1)',
      (1 - xs**2)*sp.diff(y2L, xs, 2) - 2*xs*sp.diff(y2L, xs) + 2*y2L)

# 4. Punto singolare irregolare: x^2 y' + y = 0 => y = e^{1/x} (singolarita' essenziale, nessuna serie di Frobenius)
check('Irregolare: x^2 y\' + y = 0 ha y = e^{1/x}', x**2*sp.diff(sp.exp(1/x), x) + sp.exp(1/x))
# Serie di Eulero x^2 y' + y = x: serie formale y ~ sum (-1)^n n! x^{n+1} (raggio 0); residuo troncato = O(x^{N+2})
M = 10
yE = sum((-1)**n*sp.factorial(n)*x**(n + 1) for n in range(M))
resE = sp.expand(x**2*sp.diff(yE, x) + yE - x)
print('   serie di Eulero troncata a M=10: residuo =', resE, '(singolo termine O(x^{M+1}), coefficienti n! -> divergente)')
RES.append(sp.Poly(resE, x).monoms() == [(M + 1,)])

# 5. Asintotica WKB: y'' = Q(x) y, y ~ Q^{-1/4} exp(+-int sqrt Q). Residuo relativo = O(Q''/Q^2, Q'^2/Q^3)
Q = sp.Function('Q')(x)
yW = Q**sp.Rational(-1, 4)*sp.exp(sp.Integral(sp.sqrt(Q), x))
relres = sp.simplify((sp.diff(yW, x, 2) - Q*yW)/yW)
expected = 5*sp.diff(Q, x)**2/(16*Q**2) - sp.diff(Q, x, 2)/(4*Q)
check('WKB: (y\'\'-Qy)/y = 5Q\'^2/(16Q^2) - Q\'\'/(4Q)  (errore di ordine 2)', relres - expected)
# Caso Airy Q = x: residuo relativo = 5/(16 x^2) -> 0 ; termine principale Ai ~ x^{-1/4} e^{-2/3 x^{3/2}}
print('   WKB per Airy (Q=x): residuo relativo =', sp.simplify(expected.subs(Q, x).doit()))

# 6. D-finitezza (olonomia): chiusura per somma e prodotto. e^x sin x: annullatore D^2 - 2D + 2 (ordine 2 = 1*2)
h = sp.exp(x)*sp.sin(x)
check('prodotto D-finito: (D^2-2D+2)(e^x sin x) = 0', sp.diff(h, x, 2) - 2*sp.diff(h, x) + 2*h)
# x e^{x^2}: (D - 2x - 1/x) u = 0, operatore a coeff. polinomiali x D - (2x^2+1)
u = x*sp.exp(x**2)
check('D-finito a coeff. polinomiali: (x D - 2x^2 - 1) x e^{x^2} = 0', x*sp.diff(u, x) - (2*x**2 + 1)*u)

print(f'\nTOTALE: {sum(RES)}/{len(RES)} OK')
