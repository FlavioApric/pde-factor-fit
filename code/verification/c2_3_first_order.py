"""PR-C2a / C2.3 -- ODE del primo ordine: lineare (fattore integrante), separabile, esatta, omogenea;
Bernoulli, Riccati, Clairaut, Lagrange (d'Alembert) come casi nonlineari con linearizzazione esatta.
Eseguire: D:\\ProblemaBase\\.venv\\Scripts\\python.exe -I c2_3_first_order.py
"""
import sys
import sympy as sp
sys.stdout.reconfigure(encoding='utf-8')

x, C, k, n = sp.symbols('x C k n')
a = sp.Function('a')(x)
q = sp.Function('q')(x)
RES = []


def check(name, expr):
    ok = sp.simplify(sp.expand(expr)) == 0
    RES.append(ok)
    print(('[OK]  ' if ok else '[FAIL]') + ' ' + name)


# 1. Lineare omogenea T = D + a(x): ker T = span{ exp(-int a) }  (dimensione 1)
e = sp.exp(-sp.Integral(a, x))
check('(D + a(x)) exp(-int a) = 0', sp.diff(e, x) + a*e)
# fattore integrante mu = exp(int a): mu (y' + a y) = (mu y)'
y = sp.Function('y')(x)
mu = sp.exp(sp.Integral(a, x))
check('fattore integrante: mu(y\'+ay) = (mu y)\'', mu*(sp.diff(y, x) + a*y) - sp.diff(mu*y, x))
# forzata: y = mu^{-1}( int mu q + C )
yl = (sp.Integral(mu*q, x) + C)/mu
check('(D+a) [mu^{-1}(int mu q + C)] = q', sp.diff(yl, x) + a*yl - q)
# casi concreti: a = 2x (Gaussiana!) e a = k/x (potenza x^{-k})
check('(D + 2x) e^{-x^2} = 0  (nucleo gaussiano: termine x*u)', sp.diff(sp.exp(-x**2), x) + 2*x*sp.exp(-x**2))
check('(D + k/x) x^{-k} = 0  (termine u/x)', sp.diff(x**(-k), x) + k/x*x**(-k))
check('(xD - k) x^{k} = 0  (Euler del 1o ordine)', x*sp.diff(x**k, x) - k*x**k)

# 2. Bernoulli y' + p y = q y^n:  v = y^{1-n} soddisfa v' + (1-n) p v = (1-n) q (lineare)
p_, q_ = sp.symbols('p q')
vB = q_/p_ + C*sp.exp(-(1 - n)*p_*x)          # v = y^{1-n}
check('Bernoulli: v = y^{1-n} soddisfa v1 + (1-n)p v = (1-n)q (lineare)',
      sp.diff(vB, x) + (1 - n)*p_*vB - (1 - n)*q_)
# identita' di catena: con y = v^{1/(1-n)}, (y'+py-qy^n) = y^n/(1-n) (v'+(1-n)pv-(1-n)q)  (verifica n=3, n=1/2)
for nn in (3, sp.Rational(1, 2)):
    vv = vB.subs(n, nn); yy = vv**(1/(1 - sp.S(nn)))
    check(f'Bernoulli n={nn}: y = v^(1/(1-n)) risolve y1+py=qy^n (y1=dy/dx)', sp.simplify(sp.diff(yy, x) + p_*yy - q_*vv**(sp.S(nn)/(1 - sp.S(nn)))))  # ramo principale, v>0

# 3. Riccati y' = q0 + q1 y + q2 y^2  <->  lineare del 2o ordine via y = -w'/(q2 w)
q0, q1, q2 = [sp.Function(f'q{i}')(x) for i in range(3)]
w = sp.Function('w')(x)
yR = -sp.diff(w, x)/(q2*w)
lin = sp.diff(w, x, 2) - (q1 + sp.diff(q2, x)/q2)*sp.diff(w, x) + q0*q2*w   # = 0
resid = sp.diff(yR, x) - (q0 + q1*yR + q2*yR**2)
# resid deve essere proporzionale a lin: resid = -lin/(q2 w)
check('Riccati: y=-w\'/(q2 w) => y\'-q0-q1y-q2y^2 = -[w\'\'-(q1+q2\'/q2)w\'+q0q2w]/(q2 w)',
      resid + lin/(q2*w))
# esempio: y' = 1 + y^2 -> w'' + w = 0 -> y = tan(x + C)
check('Riccati y\'=1+y^2: y = tan(x+C)', sp.diff(sp.tan(x + C), x) - 1 - sp.tan(x + C)**2)

# 4. Clairaut y = x y' + f(y'): famiglia di rette y = Cx + f(C) + soluzione singolare (inviluppo)
f = lambda z: -z**2/4 + 0*z   # f(p) = -p^2/4  -> singolare y = x^2
yc = C*x + f(C)
check('Clairaut: y = Cx + f(C) risolve y = x y\' + f(y\')', yc - (x*sp.diff(yc, x) + f(sp.diff(yc, x))))
ys = x**2
check('Clairaut: inviluppo y = x^2 (soluzione singolare)', ys - (x*sp.diff(ys, x) + f(sp.diff(ys, x))))

# 5. Lagrange/d'Alembert y = x g(y') + h(y'): con p = y' parametro, x(p) risolve una ODE LINEARE
#    dx/dp (g(p) - p) + x g'(p) + h'(p) = 0.  Esempio g(p) = 2p, h(p) = p^2:
P = sp.symbols('P')
X = sp.Function('X')(P)
lin_eq = sp.diff(X, P)*(2*P - P) + X*2 + 2*P
sol = sp.dsolve(sp.Eq(lin_eq, 0), X)
print('   Lagrange: x(p) =', sol.rhs)
Xp = sol.rhs
Yp = Xp*2*P + P**2
# verifica parametrica: dy/dx = (dY/dP)/(dX/dP) = P
check('Lagrange: (dy/dp)/(dx/dp) = p sulla curva parametrica', sp.diff(Yp, P)/sp.diff(Xp, P) - P)

# 6. Esatta: M dx + N dy = 0 con M_y = N_x; potenziale F
X_, Y_ = sp.symbols('X Y')
M, N = 2*X_*Y_ + 1, X_**2 + 3*Y_**2
check('Esatta: M_y = N_x', sp.diff(M, Y_) - sp.diff(N, X_))
F = sp.integrate(M, X_) + sp.integrate(N - sp.diff(sp.integrate(M, X_), Y_), Y_)
check('Esatta: grad F = (M,N)', sp.diff(F, X_) - M + sp.diff(F, Y_) - N)

# 7. Omogenea y' = F(y/x): sostituzione y = x v -> separabile. Esempio y' = (x+y)/x -> y = x(log x + C)
yh = x*(sp.log(x) + C)
check('Omogenea: y = x(log x + C) risolve y\' = 1 + y/x', sp.diff(yh, x) - (1 + yh/x))

# 8. Autonoma logistica y' = y(1-y): y = 1/(1 + C e^{-x}); equilibri 0 (instabile), 1 (stabile)
yl2 = 1/(1 + C*sp.exp(-x))
check('Logistica: y = 1/(1+Ce^{-x})', sp.diff(yl2, x) - yl2*(1 - yl2))
F_ = lambda Y: Y*(1 - Y)
print('   F\'(0) =', sp.diff(F_(X_), X_).subs(X_, 0), ' F\'(1) =', sp.diff(F_(X_), X_).subs(X_, 1),
      '(segno -> stabilita\' linearizzata)')

print(f'\nTOTALE: {sum(RES)}/{len(RES)} OK')
