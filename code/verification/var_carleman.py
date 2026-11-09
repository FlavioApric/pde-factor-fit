# S-CHECK-F8-VAR (27/10/2026) - verifica SIMBOLICA dell'identita' di Carleman di VAR-L0.
# Metodo: con z = a + i b (a, b reali), la densita'
#   D = |P z|^2 - |S z|^2 - |A z|^2 - q_dens(z)
# e' una divergenza totale (quindi ha integrale nullo per z a supporto compatto)
# se e solo se il suo operatore di Eulero-Lagrange rispetto ad a e a b e' identicamente nullo.
# Questo prova l'identita' ||P z||^2 = ||S z||^2 + ||A z||^2 + q(z) per phi generica.
import sympy as sp
from sympy.calculus.euler import euler_equations

t, x, lam = sp.symbols('t x lambda', real=True)
phi = sp.Function('phi')(t, x)
a = sp.Function('a')(t, x)
b = sp.Function('b')(t, x)
z = a + sp.I*b
L0 = lambda f: sp.I*sp.diff(f, t) + sp.diff(f, x, 2)

ok = True
# (1) P_lambda = e^{lam phi} L0 e^{-lam phi} = S + A
P = sp.simplify(sp.exp(lam*phi)*L0(sp.exp(-lam*phi)*z))
px, pt = sp.diff(phi, x), sp.diff(phi, t)
S = sp.diff(z, x, 2) + lam**2*px**2*z + sp.I*sp.diff(z, t)
A = -2*lam*px*sp.diff(z, x) - lam*sp.diff(phi, x, 2)*z - sp.I*lam*pt*z
r1 = sp.simplify(sp.expand(P - S - A))
print("(1) P - S - A =", r1); ok &= (r1 == 0)

# parte reale/immaginaria esplicita (a, b, phi reali)
def reim(w):
    w = sp.expand(w)
    im = sp.expand(w.coeff(sp.I))
    re = sp.expand(w - sp.I*im)
    assert not re.has(sp.I) and not im.has(sp.I)
    return re, im

def mod2(w):
    re, im = reim(w)
    return sp.expand(re**2 + im**2)

phxx = sp.diff(phi, x, 2); phxt = sp.diff(phi, x, t)
zx = sp.diff(z, x)
ImZxZb = sp.diff(b, x)*a - sp.diff(a, x)*b          # Im(z_x conj(z))
q = (4*lam*phxx*(sp.diff(a, x)**2 + sp.diff(b, x)**2)
     + 4*lam*phxt*ImZxZb
     + (4*lam**3*px**2*phxx - lam*sp.diff(phi, x, 4) + lam*sp.diff(phi, t, 2))*(a**2 + b**2))
D = sp.expand(mod2(P) - mod2(S) - mod2(A) - q)
EL = euler_equations(D, [a, b], [t, x])
res = [sp.simplify(e.lhs) for e in EL]
print("(2) Eulero-Lagrange di D rispetto ad a, b:", res)
ok &= all(r == 0 for r in res)

# controllo di sensibilita': col segno opposto del termine incrociato l'identita' fallisce
qbad = q - 8*lam*phxt*ImZxZb
Dbad = sp.expand(mod2(P) - mod2(S) - mod2(A) - qbad)
ELb = euler_equations(Dbad, [a, b], [t, x])
resb = [sp.simplify(e.lhs) for e in ELb]
print("(3) segno opposto: E-L non nullo?", any(r != 0 for r in resb))
ok &= any(r != 0 for r in resb)

# (4) peso del lemma: phi = -s + mu s^2 - (t-t0)^2, s = x - g(t): phi_x in [-3/2,-1/2] su |s|<=b, phi_xx = 2 mu, phi_xxxx = 0
s_, mu, bb, t0 = sp.symbols('s mu b t0', real=True)
g = sp.Function('g')(t)
ph = -(x - g) + mu*(x - g)**2 - (t - t0)**2
print("(4) phi_xx =", sp.simplify(sp.diff(ph, x, 2)), " phi_xxxx =", sp.diff(ph, x, 4),
      " phi_x(s=+-b, mu=1/(4b)) =", [sp.simplify((-1 + 2*mu*sv).subs(mu, 1/(4*bb))) for sv in (bb, -bb)])
ok &= sp.diff(ph, x, 4) == 0
# assorbimento: 4|p||q| <= 8 mu p^2 + q^2/(2 mu)  <=>  (sqrt(8mu)p - q/sqrt(2mu))^2 >= 0
pp, qq = sp.symbols('p q', positive=True)
gap = sp.expand(8*mu*pp**2 + qq**2/(2*mu) - 4*pp*qq)
print("(5) 8mu p^2 + q^2/(2mu) - 4pq =", sp.factor(gap))
print("TUTTO OK" if ok else "FALLITO")
