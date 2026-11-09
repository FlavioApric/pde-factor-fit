"""PR-C2a / C2.2 -- ODE forzate e sistemi lineari: Green/risposta all'impulso, convoluzione,
funzione di trasferimento, variazione dei parametri, esponenziale di matrice, Jordan, matrice compagna,
matrici fondamentali, Abel-Liouville.
Eseguire: D:\\ProblemaBase\\.venv\\Scripts\\python.exe -I c2_2_forced_systems.py
"""
import sys
import sympy as sp
sys.stdout.reconfigure(encoding='utf-8')

x, s, t, z = sp.symbols('x s t z')
lam = sp.symbols('lambda')
RES = []


def check(name, expr):
    if isinstance(expr, sp.MatrixBase):
        ok = all(sp.simplify(sp.expand(e)) == 0 for e in expr)
    else:
        ok = sp.simplify(sp.expand(expr)) == 0
    RES.append(ok)
    print(('[OK]  ' if ok else '[FAIL]') + ' ' + name)


def pD(coeffs, f, v=x):
    return sum(c * sp.diff(f, v, k) for k, c in enumerate(coeffs))


# --- Operatore di prova: p(D) = D^3 - D^2 - 8D + 12 = (D-2)^2 (D+3)
P = sp.expand((s - 2)**2*(s + 3))
co = [P.coeff(s, k) for k in range(4)]
m = 3

# 1. Risposta all'impulso (Green causale) g: p(D)g = 0, g(0)=g'(0)=0, g''(0)=1
g = sp.inverse_laplace_transform(1/P, s, x)
g = sp.simplify(g.subs(sp.Heaviside(x), 1))
check('p(D) g = 0 (g = L^{-1}[1/p])', pD(co, g))
ic = [sp.diff(g, x, k).subs(x, 0) for k in range(3)]
print('   condizioni iniziali g, g\', g\'\' in 0 =', ic, '(atteso [0,0,1])')
RES.append(ic == [0, 0, 1])
# Funzione di trasferimento = simbolo inverso: L[g](s) = 1/p(s)
Lg = sp.laplace_transform(g, x, s, noconds=True)
check('Funzione di trasferimento: L[g] = 1/p(s)', Lg - 1/P)

# 2. Formula di Duhamel/convoluzione: y = int_0^x g(x-t) f(t) dt risolve p(D)y = f, y^{(k)}(0)=0
for f in (sp.sin(t), t**2, sp.exp(-t)):
    y = sp.integrate(g.subs(x, x - t)*f, (t, 0, x))
    check(f'p(D)(g * f) = f  per f = {f}', pD(co, y) - f.subs(t, x))

# 3. Variazione dei parametri (2° ordine) per y'' + y = sec x  -> y_p = x sin x + cos x log cos x
y1, y2 = sp.cos(x), sp.sin(x)
W = sp.simplify(y1*sp.diff(y2, x) - y2*sp.diff(y1, x))
f = 1/sp.cos(x)
yp = -y1*sp.integrate(y2*f/W, x) + y2*sp.integrate(y1*f/W, x)
check('Variazione dei parametri: (D^2+1) y_p = sec x', sp.diff(yp, x, 2) + yp - f)

# 4. Matrice compagna (via II-b) e esponenziale: Y = (y, y', y'')^T, Y' = C Y
C = sp.zeros(m, m)
for i in range(m - 1):
    C[i, i + 1] = 1
for k in range(m):
    C[m - 1, k] = -co[k]
charp = sp.expand((s*sp.eye(m) - C).det())
check('det(sI - C) = p(s)  (polinomio caratteristico = operatore)', charp - P)
Jform = C.jordan_form()
print('   forma di Jordan di C:', Jform[1].tolist(), '(blocco 2x2 per lambda=2 <-> x e^{2x})')
RES.append(Jform[1] == sp.Matrix([[-3, 0, 0], [0, 2, 1], [0, 0, 2]]))
E = sp.simplify((C*x).exp())
check('d/dx e^{xC} = C e^{xC}', sp.simplify(sp.diff(E, x) - C*E))
# riga 0, colonna m-1 di e^{xC} = risposta all'impulso g (Green = esponenziale della compagna)
check('[e^{xC}]_{0,m-1} = g(x)', E[0, m - 1] - g)
# Liouville/Abel: det e^{xC} = e^{x tr C}
check('Abel-Liouville: det e^{xC} = e^{x tr C}', sp.simplify(E.det() - sp.exp(x*C.trace())))

# 5. Sistema generico con blocco di Jordan: A = J_3(lam) => e^{xA} = e^{lam x}[1, x, x^2/2; ...]
J3 = sp.Matrix([[lam, 1, 0], [0, lam, 1], [0, 0, lam]])
EJ = sp.simplify((J3*x).exp())
target = sp.exp(lam*x)*sp.Matrix([[1, x, x**2/2], [0, 1, x], [0, 0, 1]])
check('e^{x J_3(lam)} = e^{lam x} * polinomi in x', sp.simplify(EJ - target))

# 6. Sistema 2x2 a coefficienti costanti non diagonalizzabile: matrice fondamentale e soluzione forzata
A = sp.Matrix([[1, 1], [-1, 3]])   # autovalore doppio 2, un solo autovettore
Phi = sp.simplify((A*x).exp())
check('Phi\' = A Phi (matrice fondamentale)', sp.simplify(sp.diff(Phi, x) - A*Phi))
F = sp.Matrix([sp.exp(x), 0])
Yp = Phi*sp.integrate(sp.simplify(Phi.subs(x, t).inv()*F.subs(x, t)), (t, 0, x))
check('Variazione delle costanti per sistemi: Y_p\' = A Y_p + F', sp.simplify(sp.diff(Yp, x) - A*Yp - F))

# 7. Risposta sinusoidale (gain/phase, MIT 18.03 L7, L14): p(D) y = cos(wx), y = Re(e^{iwx}/p(iw))
w = sp.symbols('omega', positive=True)
P2 = s**2 + 3*s + 2
xr = sp.symbols('xr', real=True)
yc = sp.re(sp.expand_complex(sp.exp(sp.I*w*xr)/P2.subs(s, sp.I*w)))
check('Risposta in frequenza: (D^2+3D+2) Re[e^{iwx}/p(iw)] = cos wx',
      sp.diff(yc, xr, 2) + 3*sp.diff(yc, xr) + 2*yc - sp.cos(w*xr))

print(f'\nTOTALE: {sum(RES)}/{len(RES)} OK')
