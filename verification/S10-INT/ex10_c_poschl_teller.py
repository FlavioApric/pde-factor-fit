"""S10-INT, EX10-c: Poschl-Teller q = -2 sech^2 x, fattorizzazione A^+A e catena di Darboux/Crum.
Equazione: i u_t = L_q u, L_q = -d^2 + q. Verifica V-ex, non una prova.
Dato (come ALGORITMO_ESTESO 9.2): u = e^{it} sech x + e^{-ik^2 t}(ik - tanh x)e^{ikx}, k = 3/2.
"""
import sympy as sp

t, x = sp.symbols('t x', real=True)
T = sp.tanh(x); S = sp.sech(x)
k = sp.Rational(3, 2)
q1 = -2 * S**2
q2 = -6 * S**2
f = sp.Function('f')(x)
ok = []
def L(q, g):
    return -sp.diff(g, x, 2) + q * g
def Aop(W, g):  return sp.diff(g, x) + W * g      # A = d + W
def Apl(W, g):  return -sp.diff(g, x) + W * g     # A^+ = -d + W
PTS = [(sp.Rational(3, 10), sp.Rational(-7, 10)), (sp.Rational(11, 10), sp.Rational(2, 5)),
       (sp.Rational(17, 10), sp.Rational(13, 10)), (sp.Rational(-1, 2), sp.Rational(-21, 10)),
       (sp.Rational(5, 2), sp.Rational(1, 10)), (sp.Rational(9, 10), sp.Rational(29, 10))]
def z(e):
    """Zero test. Se e contiene f (operatore su f generica): esatto, coefficiente per coefficiente
    di f, f', f'' (riscritti in exp). Altrimenti: valutazione a 45 cifre in 6 punti, |e| < 1e-35."""
    if e.has(f):
        e = sp.expand(e)
        derivs = [sp.diff(f, x, j) for j in (2, 1)] + [f]
        rest = e
        for d in derivs:
            c = rest.coeff(d)
            rest = sp.expand(rest - c * d)
            if sp.simplify(sp.expand(c.rewrite(sp.exp))) != 0:
                return False
        return sp.simplify(rest) == 0
    return max(abs(sp.N(e.subs({t: a, x: b}), 45)) for a, b in PTS) < 1e-35

# fattorizzazioni (passo 6 in C(tanh x)[d]: Loewy/Darboux)
ok.append(('(1) A^+A = L_q1 + 1,  A = d + tanh', z(Apl(T, Aop(T, f)) - (L(q1, f) + f))))
ok.append(('(1) AA^+ = L_0 + 1  (partner libero)', z(Aop(T, Apl(T, f)) - (L(0, f) + f))))
ok.append(('(1) catena di Crum: A2^+A2 = L_q2 + 4, A2 = d + 2 tanh', z(Apl(2 * T, Aop(2 * T, f)) - (L(q2, f) + 4 * f))))
ok.append(('(1) A2 A2^+ = L_q1 + 4', z(Aop(2 * T, Apl(2 * T, f)) - (L(q1, f) + 4 * f))))

ub = sp.exp(sp.I * t) * S
us = sp.exp(-sp.I * k**2 * t) * (sp.I * k - T) * sp.exp(sp.I * k * x)
u = ub + us
schr = lambda g: sp.I * sp.diff(g, t) - L(q1, g)
ok.append(('(2) u risolve i u_t = L_q u', z(schr(u))))
rho = (sp.I * sp.diff(u, t) + sp.diff(u, x, 2)) / u
ok.append(('(2) rho_u = q (ID-res, VAR-T1(b))', z(rho - q1)))

# ricostruzione per fattorizzazione dallo stato fondamentale (DM-phi: solo V - E0)
phi0 = S
W = sp.simplify(-sp.diff(phi0, x) / phi0)
ok.append(('(3) superpotenziale W = -phi0\'/phi0 = tanh x', z(W - T)))
ok.append(('(3) W^2 - W\' = q + 1 = V - E0: lo stato fondamentale da\' V solo modulo costante (ID-fam)',
           z(W**2 - sp.diff(W, x) - (q1 + 1))))
ok.append(('(3) con la fase osservata (DM3): rho_{u_b} = q esattamente',
           z((sp.I * sp.diff(ub, t) + sp.diff(ub, x, 2)) / ub - q1)))

# vacuita' nell'anello C(tanh x)[d_t, d_x] (VAR-N1)
ok.append(('(4) (d_x + tanh x) u_b = 0 e (d_t - i) u_b = 0: annullatori di ordine 1 in K = C(tanh x)',
           z(sp.diff(ub, x) + T * ub) and z(sp.diff(ub, t) - sp.I * ub)))
Tt = sp.symbols('Tt')
lds = sp.simplify(sp.diff(us, x) / us)
lds_T = sp.simplify(lds.rewrite(sp.tanh))
cand = sp.I * k - (1 - Tt**2) / (sp.I * k - Tt)
ok.append(('(4) u_s,x / u_s = ik - (1 - tanh^2)/(ik - tanh) in C(tanh x)', z(lds - cand.subs(Tt, T))))

# Ann nel sottoanello C[d_t, L_q]: due generatori estranei => non ID-ann
ok.append(('(5) (L_q + 1)(L_q - k^2) u = 0', z(L(q1, L(q1, u) - k**2 * u) + (L(q1, u) - k**2 * u))))
Dt = lambda g: sp.I * sp.diff(g, t)
ok.append(('(5) (i d_t + 1)(i d_t - k^2) u = 0', z(Dt(Dt(u) - k**2 * u) + (Dt(u) - k**2 * u))))

# componenti = fattori nel sottoanello commutativo C[L_q] (varieta' disgiunte: -1 != k^2)
Pb = (L(q1, u) - k**2 * u) / (-1 - k**2)
Ps = (L(q1, u) + u) / (k**2 + 1)
ok.append(('(6) proiettore (L_q - k^2)/(-1 - k^2) restituisce u_b', z(Pb - ub)))
ok.append(('(6) proiettore (L_q + 1)/(k^2 + 1) restituisce u_s', z(Ps - us)))

# Darboux come encoder: perdita del modo legato, il dato diventa EP (classe (C))
ok.append(('(7) A u_b = 0 (modo legato perso)', z(Aop(T, ub))))
ok.append(('(7) A u_s = -(1 + k^2) e^{i(kx - k^2 t)}: onda piana, dato EP',
           z(Aop(T, us) + (1 + k**2) * sp.exp(sp.I * (k * x - k**2 * t)))))
ok.append(('(7) A u risolve Schroedinger libero', z(sp.I * sp.diff(Aop(T, u), t) + sp.diff(Aop(T, u), x, 2))))

ok = [(n_, bool(v_)) for n_, v_ in ok]
for name, val in ok:
    print('PASS' if val else 'FAIL', name)
print('%d/%d PASS' % (sum(v for _, v in ok), len(ok)))
