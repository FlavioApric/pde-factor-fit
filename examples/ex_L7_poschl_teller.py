"""S9-ALG, esempio L7: Schroedinger con V(x) = -2 sech^2 x (Poeschl-Teller, senza riflessione).
Verifica V-ex (non una prova). Convenzione del progetto: i u_t = -u_xx + V u, residuo V = (i u_t + u_xx)/u.
(a) u = e^{it} sech x + e^{-i k^2 t}(ik - tanh x) e^{ikx} (stato legato E = -1 + stato di scattering E = k^2)
    risolve l'equazione; il residuo restituisce V = -2 sech^2 x (VAR-T1(b), ID-res, DM3).
(b) DM-phi: la sola parte stazionaria e^{-iEt} sech x, nota a meno della fase, da' solo V - E (VAR-P4).
(c) encoder di Darboux (traduzione a q noto): A = d_x + tanh x, A L_q = L_0 A (c = 0), ker A = C sech x;
    A u e' soluzione libera (il modo legato e' perso: dim ker W = 1, (E1)).
(d) fattorizzazioni A^+A = L_q + 1, A A^+ = L_0 + 1.
"""
import sympy as sp

t, x = sp.symbols('t x', real=True)
k = sp.Rational(3, 2)
q = -2 * sp.sech(x)**2
ok = []

def Lq(f):  # operatore spaziale L_q = -d^2 + q
    return -sp.diff(f, x, 2) + q * f
def L0(f):
    return -sp.diff(f, x, 2)
def schr_res(u, V):
    return sp.I * sp.diff(u, t) + sp.diff(u, x, 2) - V * u

def z(e):
    # tanh, sech -> esponenziali; numeratore espanso (esatto)
    e = sp.together(sp.expand(e.rewrite(sp.exp)))
    n = sp.expand(sp.numer(e))
    return sp.simplify(n) == 0

u_b = sp.exp(sp.I * t) * sp.sech(x)
u_s = sp.exp(-sp.I * k**2 * t) * (sp.I * k - sp.tanh(x)) * sp.exp(sp.I * k * x)
u = u_b + u_s
ok.append(('(a) stato legato risolve', z(schr_res(u_b, q))))
ok.append(('(a) stato di scattering risolve', z(schr_res(u_s, q))))
Vrec = (sp.I * sp.diff(u, t) + sp.diff(u, x, 2)) / u
ok.append(('(a) residuo (i u_t + u_xx)/u = -2 sech^2 x (verificato come (i u_t + u_xx) - q u = 0)', z(schr_res(u, q))))

# (b) DM-phi: u_b moltiplicato per una fase globale e^{i phi(t)} arbitraria
phi = sp.Function('phi')(t)
ub_phi = sp.exp(sp.I * phi) * u_b
Vphi = sp.simplify((sp.I * sp.diff(ub_phi, t) + sp.diff(ub_phi, x, 2)) / ub_phi)
ok.append(('(b) DM-phi: residuo = V - phi\'(t) (solo V a meno di costante/funzione di t)',
           z(Vphi - (q - sp.diff(phi, t)))))

# (c) Darboux
def A(f):
    return sp.diff(f, x) + sp.tanh(x) * f
def Ad(f):
    return -sp.diff(f, x) + sp.tanh(x) * f
g = sp.Function('g')(x)
ok.append(('(c) A L_q = L_0 A (su g generica)', z(A(Lq(g)) - L0(A(g)))))
ok.append(('(c) ker A contiene sech x', z(A(sp.sech(x)))))
Au = A(u)
ok.append(('(c) A u risolve Schroedinger libero', z(sp.I * sp.diff(Au, t) + sp.diff(Au, x, 2))))
ok.append(('(c) A u_b = 0 (modo legato perso)', z(A(u_b))))
# A u_s e' un'onda piana: Ann(Au) contiene i d_t + d_x^2 e d_x - ik (dato EP dopo la traduzione)
ok.append(('(c) A u_s e\' multiplo di e^{i(kx - k^2 t)}', z(sp.diff(A(u_s), x) - sp.I * k * A(u_s))))
# (d)
ok.append(('(d) A^+A = L_q + 1', z(Ad(A(g)) - (Lq(g) + g))))
ok.append(('(d) A A^+ = L_0 + 1', z(A(Ad(g)) - (L0(g) + g))))

for name, val in ok:
    print('PASS' if val else 'FAIL', name)
print('%d/%d PASS' % (sum(1 for _, v in ok if v), len(ok)))
