"""PR-C2a / C2.1 -- ODE lineari a coefficienti costanti.  Verifiche T e = 0 e identita' chiave.
Eseguire: D:\\ProblemaBase\\.venv\\Scripts\\python.exe -I c2_1_const_coeff.py
"""
import sys
import sympy as sp
sys.stdout.reconfigure(encoding='utf-8')

x, s, r, lam, mu, a, b = sp.symbols('x s r lambda mu a b')
RES = []


def check(name, expr):
    ok = sp.simplify(sp.expand(expr)) == 0
    RES.append(ok)
    print(('[OK]  ' if ok else '[FAIL]') + ' ' + name)


def pD(coeffs, f):
    """p(D) f con p = sum coeffs[k] D^k."""
    return sum(c * sp.diff(f, x, k) for k, c in enumerate(coeffs))


# 1. Nucleo di (D - lam)^m : x^k e^{lam x}, k < m  (radice multipla)
for m in range(1, 6):
    for k in range(m):
        e = x**k * sp.exp(lam * x)
        f = e
        for _ in range(m):
            f = sp.diff(f, x) - lam * f
        check(f'(D-lam)^{m} [x^{k} e^(lam x)] = 0', f)
# e x^m e^{lam x} NON e' nel nucleo: (D-lam)^m x^m e^{lam x} = m! e^{lam x}
f = x**3 * sp.exp(lam * x)
for _ in range(3):
    f = sp.diff(f, x) - lam * f
check('(D-lam)^3 x^3 e^(lam x) = 3! e^(lam x)  (fuori dal nucleo)', f - 6 * sp.exp(lam * x))

# 2. Radici complesse: (D-a)^2 + b^2 annulla e^{ax} cos bx, e^{ax} sin bx; con molteplicita' 2 anche x e^{ax} cos bx
for g in (sp.exp(a*x)*sp.cos(b*x), sp.exp(a*x)*sp.sin(b*x)):
    check(f'((D-a)^2+b^2) {g} = 0', pD([a**2 + b**2, -2*a, 1], g))
q = lambda f: sp.diff(f, x, 2) - 2*a*sp.diff(f, x) + (a**2 + b**2)*f
for g in (x*sp.exp(a*x)*sp.cos(b*x), x*sp.exp(a*x)*sp.sin(b*x)):
    check(f'((D-a)^2+b^2)^2 {g} = 0', q(q(g)))

# 3. ERF (exponential response formula, MIT 18.03 L13): p(D) e^{rx} = p(r) e^{rx} per p generico di grado 4
c = sp.symbols('c0:5')
p = lambda z: sum(c[k]*z**k for k in range(5))
check('ERF: p(D)e^{rx} = p(r) e^{rx}', pD(c, sp.exp(r*x)) - p(r)*sp.exp(r*x))
# 3b. Exponential shift rule: p(D)(e^{rx} g) = e^{rx} p(D+r) g
g = sp.Function('g')(x)
lhs = pD(c, sp.exp(r*x)*g)
rhs_inner = 0
# p(D+r) g = sum c_k (D+r)^k g
for k in range(5):
    t = g
    for _ in range(k):
        t = sp.diff(t, x) + r*t
    rhs_inner += c[k]*t
check('Exponential shift: p(D)(e^{rx}g) = e^{rx} p(D+r) g', lhs - sp.exp(r*x)*rhs_inner)
# 3c. Risonanza (ERF generalizzata): se p(r)=0, p'(r)!=0, y = x e^{rx}/p'(r) risolve p(D)y = e^{rx}
#     esempio p(z) = (z-1)(z+2)(z-3), r = 1
P = sp.expand((s - 1)*(s + 2)*(s - 3))
co = [P.coeff(s, k) for k in range(4)]
y = x*sp.exp(x)/sp.diff(P, s).subs(s, 1)
check('Risonanza semplice: p(D)[x e^x / p\'(1)] = e^x', pD(co, y) - sp.exp(x))
# 3d. Risonanza di ordine m: p(r)=...=p^{(m-1)}(r)=0 => y = x^m e^{rx}/p^{(m)}(r)
P2 = sp.expand((s - 1)**3*(s + 2))
co2 = [P2.coeff(s, k) for k in range(5)]
y2 = x**3*sp.exp(x)/sp.diff(P2, s, 3).subs(s, 1)
check('Risonanza ordine 3: p(D)[x^3 e^x / p\'\'\'(1)] = e^x', pD(co2, y2) - sp.exp(x))

# 4. Fattorizzazione => split additivo (G2, caso ODE): ker((D-1)(D+2)^2) = ker(D-1) (+) ker((D+2)^2)
P3 = sp.expand((s - 1)*(s + 2)**2)
co3 = [P3.coeff(s, k) for k in range(4)]
A, B, C = sp.symbols('A B C')
u = A*sp.exp(x) + (B + C*x)*sp.exp(-2*x)
check('ker(P1 P2) contiene ker P1 + ker P2', pD(co3, u))
# Bezout: 1 = alpha P1 + beta P2 => proiettori u1 = beta(D)P2(D) u, u2 = alpha(D)P1(D) u
P1, P2b = s - 1, (s + 2)**2
al, be, gc = sp.gcdex(P1, P2b, s)  # al*P1 + be*P2b = 1
assert sp.simplify(gc - 1) == 0
coef = lambda poly: [sp.Poly(sp.expand(poly), s).coeff_monomial(s**k) for k in range(sp.degree(sp.expand(poly), s) + 1)]
u1 = pD(coef(sp.expand(be*P2b)), u)
u2 = pD(coef(sp.expand(al*P1)), u)
check('Proiettore di Bezout: (beta P2)(D) u = A e^x', u1 - A*sp.exp(x))
check('Proiettore di Bezout: (alpha P1)(D) u = (B+Cx)e^{-2x}', u2 - (B + C*x)*sp.exp(-2*x))

# 5. Somma di termini (G1, caso ODE): L = D^2 + 1 = T1 + T2 con T1 = D^2, T2 = 1.
#    ker T1 = {alpha + beta x}, ker T2 = {0}.  sin x in ker L ma NON in ker T1 + ker T2.
check('sin x in ker(D^2+1)', pD([1, 0, 1], sp.sin(x)))
al_, be_ = sp.symbols('al be')
sol = sp.solve(sp.Poly(pD([1, 0, 1], al_ + be_*x), x).all_coeffs(), [al_, be_], dict=True)
print('   ker(D^2+1) ∩ ker(D^2) =', sol, ' (solo 0: A8 additivo falso per somme)')
RES.append(sol == [{al_: 0, be_: 0}])

# 6. Identificazione (C3/G4, caso ODE): da u = e^x + x e^{-2x} si ricostruisce p = (D-1)(D+2)^2.
#    Metodo: matrice di Wronski dei jet [u, u', u'', u'''] valutata in 4 punti -> nucleo.
u = sp.exp(x) + x*sp.exp(-2*x)
jet = [sp.diff(u, x, k) for k in range(4)]
M = sp.Matrix([[j.subs(x, xi) for j in jet] for xi in (0, 1, 2, 3)])
ns = M.nullspace()
lamvec = sp.simplify(ns[0] / ns[0][3])
print('   coeff. ricostruiti (c0..c3) =', list(lamvec), ' atteso', [P3.coeff(s, k) for k in range(4)])
RES.append(list(lamvec) == [P3.coeff(s, k) for k in range(4)])
# Wronskiano di {u,u',u''} non nullo => ordine minimo 3 (nessun annullatore di ordine 2)
W = sp.Matrix([[sp.diff(sp.diff(u, x, i), x, j) for i in range(3)] for j in range(3)]).det()
print('   W(u,u\',u\'\')(0) =', sp.simplify(W.subs(x, 0)), '(!=0 => ordine minimo = 3)')
RES.append(sp.simplify(W.subs(x, 0)) != 0)

# 7. Dati di Gram per C1: <x^j e^{-s1 x}, x^k e^{-s2 x}>_{L^2(0,inf)} = (j+k)!/(s1+s2)^{j+k+1}  (matrice di tipo Cauchy)
s1, s2 = sp.symbols('s1 s2', positive=True)
for (j, kq) in ((0, 0), (1, 2), (3, 1)):
    I = sp.integrate(x**j*sp.exp(-s1*x)*x**kq*sp.exp(-s2*x), (x, 0, sp.oo))
    check(f'Gram exp-poly j={j},k={kq}: (j+k)!/(s1+s2)^(j+k+1)', I - sp.factorial(j + kq)/(s1 + s2)**(j + kq + 1))

print(f'\nTOTALE: {sum(RES)}/{len(RES)} OK')
