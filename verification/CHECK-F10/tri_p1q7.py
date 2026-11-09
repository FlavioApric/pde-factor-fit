# TRIAGE P1-Q7: candidato X = (x^3+x)d, Y = d in A_1.
# (1) (H) per (X, Y): Y_k = ad_X^k Y = p_k(x) d con deg p_k = 2k e coeff. direttore = quello di (x^3 d, d); X, Y_0, Y_1,... indipendenti.
# (2) dilatazione filtrata: sigma_mu(X) = mu^2 (x^3 d + mu^{-2} x d), sigma_mu(Y) = mu^{-1} d  (x -> mu x, d -> d/mu).
# (3) (H) per la coppia graduata (x^3 d, d).
import sympy as sp
x, mu = sp.symbols('x mu')
def br(p, q):  # [p d, q d] = (p q' - q p') d
    return sp.expand(p*sp.diff(q, x) - q*sp.diff(p, x))
ok = True
for X0, name in [(x**3 + x, '(x^3+x)d'), (x**3, 'x^3 d')]:
    Yk = [sp.Integer(1)]
    for k in range(1, 8): Yk.append(br(X0, Yk[-1]))
    degs = [sp.degree(p, x) for p in Yk]
    lead = [sp.LC(sp.Poly(p, x)) for p in Yk]
    # indipendenza: matrice dei coefficienti di X0, Y_0..Y_7
    polys = [X0] + Yk
    D = max(sp.degree(p, x) for p in polys)
    M = sp.Matrix([[sp.Poly(p, x).coeff_monomial(x**i) for i in range(D + 1)] for p in polys])
    r = M.rank()
    print(name, 'gradi Y_k:', degs, 'coeff. direttori:', lead, 'rango', r, 'su', len(polys))
    ok &= (r == len(polys))
# leading coefficients coincide between the two families
Ya = [sp.Integer(1)]; Yb = [sp.Integer(1)]
for k in range(1, 8):
    Ya.append(br(x**3 + x, Ya[-1])); Yb.append(br(x**3, Yb[-1]))
same = all(sp.LC(sp.Poly(a, x)) == sp.LC(sp.Poly(b, x)) and sp.degree(a, x) == sp.degree(b, x) for a, b in zip(Ya, Yb))
print('coeff. direttori uguali a quelli di (x^3 d, d):', same); ok &= same
# sigma_mu: p(x) d -> p(mu x) d / mu
sX = sp.expand(((mu*x)**3 + mu*x)/mu)
print('sigma_mu(X) =', sX, '(d)'); ok &= sp.simplify(sX - (mu**2*x**3 + x)) == 0
# parita': con t = nu^2 s, nu = 1/mu: t*sigma(X) = s*(x^3 + nu^2 x) d ; t*eps*sigma(Y) = eps*nu^3 s d
nu, s, eps = sp.symbols('nu s eps')
tX = sp.expand(nu**2*s*(sX.subs(mu, 1/nu)))
tY = sp.expand(nu**2*s*eps/(1/nu))
print('t sigma(X) =', tX, ' ; t eps sigma(Y) =', tY)
ok &= sp.expand(tX - s*(x**3 + nu**2*x)) == 0 and sp.expand(tY - eps*nu**3*s) == 0
print('TUTTO OK' if ok else 'FAIL')
