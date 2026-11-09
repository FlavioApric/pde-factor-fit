# S-CHECK-F10-B2 . controllo indipendente del fix T1-a (coefficiente di e^{-ikx} in psi_+ a -inf).
# Convenzione OPF5D: L = -d^2 - u, psi_+(x,k) ~ e^{ikx} (x -> +inf), psi_-(x,k) ~ e^{-ikx} (x -> -inf),
#                    psi_-(k) = a(k) psi_+(-k) + b(k) psi_+(k).
# Tesi T1-a: psi_+(k) = a(k) psi_-(-k) - b(-k) psi_-(k).
# (A) forma astratta: spazio delle soluzioni di dimensione 2 con Wronskiano antisimmetrico.
# (B) potenziale concreto con riflessione: u = g*delta(x) (soluzioni esatte a tratti).
import sympy as sp
ok = []
def rep(name, c):
    ok.append(bool(c)); print(('OK  ' if c else 'FAIL') + ' ' + name)

# (A) base e1 = psi_+(k), e2 = psi_+(-k); W(e1,e2) = -2ik (calcolato a +inf).
k = sp.Symbol('k', nonzero=True)
ap, am, bp, bm = sp.symbols('a_p a_m b_p b_m')   # a(k), a(-k), b(k), b(-k)
# vettori nella base (e1, e2); W(x, y) = (x1*y2 - x2*y1) * W(e1, e2)
def Wr(x, y): return (x[0]*y[1] - x[1]*y[0])*(-2*sp.I*k)
psim_k = (bp, ap)      # psi_-(k)  = a(k) e2 + b(k) e1
psim_mk = (am, bm)     # psi_-(-k) = a(-k) e1 + b(-k) e2   (k -> -k scambia e1, e2)
# vincolo: W(psi_-(k), psi_-(-k)) = 2ik (calcolato a -inf)  <=>  a(k)a(-k) - b(k)b(-k) = 1
cons = sp.expand(Wr(psim_k, psim_mk) - 2*sp.I*k)
rep('(A) vincolo di Wronskiano <=> a(k)a(-k) - b(k)b(-k) = 1', sp.simplify(cons/(2*sp.I*k) - (ap*am - bp*bm - 1)) == 0)
A_, B_ = sp.symbols('A B')
sol = sp.solve([A_*psim_mk[0] + B_*psim_k[0] - 1, A_*psim_mk[1] + B_*psim_k[1]], [A_, B_], dict=True)[0]
Asol = sp.simplify(sol[A_].subs(am, (1 + bp*bm)/ap)); Bsol = sp.simplify(sol[B_].subs(am, (1 + bp*bm)/ap))
rep('(A) coefficiente di psi_-(-k) (cioe di e^{ikx} a -inf) = a(k): %s' % Asol, sp.simplify(Asol - ap) == 0)
rep('(A) coefficiente di psi_-(k)  (cioe di e^{-ikx} a -inf) = -b(-k): %s' % Bsol, sp.simplify(Bsol + bm) == 0)

# (B) u = g delta: -psi'' - g delta psi = k^2 psi  =>  salto psi'(0+) - psi'(0-) = -g psi(0)
g = sp.Symbol('g', positive=True)
def jost_minus(kk):
    al, be = sp.symbols('al be')
    s = sp.solve([al + be - 1, (-sp.I*kk*al + sp.I*kk*be) - (-sp.I*kk) + g*1], [al, be], dict=True)[0]
    return sp.simplify(s[al]), sp.simplify(s[be])        # x>0: al e^{-ikx} + be e^{ikx}  => a = al, b = be
def jost_plus(kk):
    A, B = sp.symbols('A B')
    s = sp.solve([A + B - 1, sp.I*kk - (sp.I*kk*A - sp.I*kk*B) + g*1], [A, B], dict=True)[0]
    return sp.simplify(s[A]), sp.simplify(s[B])          # x<0: A e^{ikx} + B e^{-ikx}
a_k, b_k = jost_minus(k); a_mk, b_mk = jost_minus(-k)
A, B = jost_plus(k)
print('   delta: a(k) =', a_k, ', b(k) =', b_k, ', psi_+ a -inf: A =', A, ', B =', B)
rep('(B) delta: coefficiente di e^{ikx} in psi_+ a -inf = a(k)', sp.simplify(A - a_k) == 0)
rep('(B) delta: coefficiente di e^{-ikx} in psi_+ a -inf = -b(-k)', sp.simplify(B + b_mk) == 0)
rep('(B) delta: a(k)a(-k) - b(k)b(-k) = 1', sp.simplify(a_k*a_mk - b_k*b_mk - 1) == 0)
print('   (per u pari b e\' immaginario puro su R e -b(-k) = b(k): serve un potenziale non simmetrico)')

# (C) potenziale non simmetrico u = g1 delta(x) + g2 delta(x - 1): -b(-k) != b(k) in generale.
g1, g2 = sp.Rational(3, 2), sp.Rational(-1, 3)
pts = [(0, g1), (1, g2)]
def cross(cl, p, gg, kk):
    # coefficienti (c1, c2) di c1 e^{ikx} + c2 e^{-ikx} a sinistra di p -> a destra di p
    d1, d2 = sp.symbols('d1 d2'); E = sp.exp(sp.I*kk*p); Em = sp.exp(-sp.I*kk*p)
    val_l = cl[0]*E + cl[1]*Em; der_l = sp.I*kk*(cl[0]*E - cl[1]*Em)
    s = sp.solve([d1*E + d2*Em - val_l, sp.I*kk*(d1*E - d2*Em) - der_l + gg*val_l], [d1, d2], dict=True)[0]
    return (sp.simplify(s[d1]), sp.simplify(s[d2]))
def cross_back(cr, p, gg, kk):
    c1, c2 = sp.symbols('c1 c2'); E = sp.exp(sp.I*kk*p); Em = sp.exp(-sp.I*kk*p)
    val = cr[0]*E + cr[1]*Em; der_r = sp.I*kk*(cr[0]*E - cr[1]*Em)
    s = sp.solve([c1*E + c2*Em - val, der_r - sp.I*kk*(c1*E - c2*Em) + gg*val], [c1, c2], dict=True)[0]
    return (sp.simplify(s[c1]), sp.simplify(s[c2]))
def ab(kk):          # psi_- : e^{-ikx} a -inf, a destra = a e^{-ikx} + b e^{ikx}
    c = (sp.Integer(0), sp.Integer(1))
    for p, gg in pts: c = cross(c, p, gg, kk)
    return sp.simplify(c[1]), sp.simplify(c[0])
def plus_left(kk):   # psi_+ : e^{ikx} a +inf, a sinistra = A e^{ikx} + B e^{-ikx}
    c = (sp.Integer(1), sp.Integer(0))
    for p, gg in reversed(pts): c = cross_back(c, p, gg, kk)
    return sp.simplify(c[0]), sp.simplify(c[1])
a2, b2 = ab(k); a2m, b2m = ab(-k); A2, B2 = plus_left(k)
rep('(C) due delta: coefficiente di e^{ikx} in psi_+ a -inf = a(k)', sp.simplify(A2 - a2) == 0)
rep('(C) due delta: coefficiente di e^{-ikx} in psi_+ a -inf = -b(-k)', sp.simplify(B2 + b2m) == 0)
kv = sp.Rational(7, 10)
rep('(C) due delta: e diverso da b(k) (k = 7/10: B = %s, b(k) = %s)' % (sp.N(B2.subs(k, kv), 6), sp.N(b2.subs(k, kv), 6)),
    abs(sp.N((B2 - b2).subs(k, kv), 30)) > 1e-6)
rep('(C) due delta: a(k)a(-k) - b(k)b(-k) = 1', abs(sp.N((a2*a2m - b2*b2m - 1).subs(k, kv), 30)) < 1e-25)
print('TOTALE: %d/%d OK' % (sum(ok), len(ok)))
