"""S9-ALG, esempio L8: V(t,x) = beta(t) x (Stark dipendente dal tempo, Avron-Herbst). Verifica V-ex.
Convenzione: i u_t = -u_xx + V u, residuo V = (i u_t + u_xx)/u.
(a) w libera gaussiana; u = e^{i(-B x + g)} w(t, x - s), B' = beta, s' = -2B, g' = -B^2,
    risolve l'equazione con V = beta(t) x  (rappresentante puntuale + gauge con theta = id: ENC-P0'-DIC, alpha = 0).
(b) u non ha zeri: int Z(u) = vuoto, il residuo identifica V(t,x) (VAR-T1(c), ID-res, DM3).
(c) DM-phi: una fase globale e^{i phi(t)} sposta il residuo di -phi'(t): V solo modulo funzioni di t.
"""
import sympy as sp

t, x = sp.symbols('t x', real=True)
beta = t                       # beta(t) = t
B = sp.integrate(beta, (t, 0, t))          # t^2/2
s = sp.integrate(-2 * B, (t, 0, t))        # -t^3/3
g = sp.integrate(-B**2, (t, 0, t))         # -t^5/20
ok = []

# Si lavora con l = log u (u = e^l non ha zeri): residuo = i l_t + l_xx + l_x^2, tutto razionale in (t, x).
def residuo(l):
    return sp.cancel(sp.I * sp.diff(l, t) + sp.diff(l, x, 2) + sp.diff(l, x)**2)
lw = -sp.log(1 + 4 * sp.I * t) / 2 - x**2 / (1 + 4 * sp.I * t)
ok.append(('(a) w gaussiana risolve Schroedinger libero (residuo 0)', residuo(lw) == 0))
lu = sp.I * (-B * x + g) - sp.log(1 + 4 * sp.I * t) / 2 - (x - s)**2 / (1 + 4 * sp.I * t)
ok.append(('(a)-(b) u = e^{i(-Bx+g)} w(t, x-s): residuo = t x', sp.cancel(residuo(lu) - beta * x) == 0))
# u = exp(lu) non si annulla mai: Z(u) vuoto (VAR-T1(c) si applica)
ok.append(('(b) u = exp(l), l finito su I x R: nessuno zero', True))
phi = sp.Function('phi')(t)
ok.append(("(c) DM-phi: residuo di e^{i phi} u = t x - phi'(t)",
           sp.simplify(residuo(lu + sp.I * phi) - (beta * x - sp.diff(phi, t))) == 0))
# controllo numerico diretto su u (non sul logaritmo), 40 cifre
u = sp.exp(lu)
res = sp.I * sp.diff(u, t) + sp.diff(u, x, 2) - beta * x * u
mx = max(sp.Abs(sp.N(res.subs({t: sp.Rational(a), x: sp.Rational(b)}), 40))
         for a, b in [('3/10', '1/5'), ('11/10', '-7/10'), ('2', '3/2')])
print('    max |residuo diretto| =', mx)
ok.append(('(a) controllo diretto su u (|res| < 1e-30)', mx < 1e-30))

for name, val in ok:
    print('PASS' if val else 'FAIL', name)
print('%d/%d PASS' % (sum(1 for _, v in ok if v), len(ok)))
