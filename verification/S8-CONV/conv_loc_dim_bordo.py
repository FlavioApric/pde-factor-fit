# S8-CONV: verifiche (non prove) per CONV-T6 (localita', ritardo L+), CONV-P8/CONV-D (1+d), CONV-B (bordo),
# CONV-R2a (bordo periodico) e CONV-MZ (Mori-Zwanzig a coefficienti costanti).
import sympy as sp
ok = True
def check(name, cond):
    global ok
    ok = ok and bool(cond)
    print(('PASS ' if cond else 'FAIL ') + name)
t, x, x1, x2, th, s = sp.symbols('t x x1 x2 theta s', real=True)
tau, xi, xi1, xi2, k = sp.symbols('tau xi xi1 xi2 kappa')
kp = sp.symbols('kappa', positive=True)
# --- T6: relazioni algebriche sul grafo del simbolo
check('Poisson: tau=-|k|, xi=ik => tau^2+xi^2=0', sp.simplify((-kp)**2 + (sp.I*kp)**2) == 0)
check('KG ellittico: tau=-sqrt(1+k^2) => tau^2+xi^2-1=0', sp.simplify((sp.sqrt(1 + kp**2))**2 + (sp.I*kp)**2 - 1) == 0)
a = sp.symbols('a', positive=True)
tm = sp.symbols('tau_m')
# memoria esponenziale: tau = -k^2/(tau+a)  <=>  tau(tau+a) = xi^2 (xi = ik)
check('memoria esponenziale => telegrafo tau(tau+a)=xi^2', sp.simplify((tm*(tm + a) - (sp.I*kp)**2).subs(tm, sp.solve(sp.Eq(tm, -kp**2/(tm + a)), tm)[0])) == 0)
p_, q_ = 3, 2
check('frazionario alpha=p/q=3/2: tau=-k^(3/2) soddisfa (-tau)^q=(-i xi)^p', sp.simplify((kp**sp.Rational(p_, q_))**q_ - (-sp.I*sp.I*kp)**p_) == 0)
# ritardo: tau = xi^2 e^{-sigma tau}, ramo principale di Lambert: tau = W(sigma xi^2)/sigma
sg = sp.symbols('sigma', positive=True)
tw = sp.LambertW(-sg*kp**2)/sg
check('ritardo: tau = W(-sigma k^2)/sigma risolve tau = -k^2 e^{-sigma tau} (numerico in 5 punti)', all(abs(sp.N((tw - (-kp**2)*sp.exp(-sg*tw)).subs({sg: sp.nsimplify(sv), kp: sp.nsimplify(kv)}), 30)) < 1e-25 for sv, kv in [(1, 0.3), (2, 0.1), (0.5, 0.7), (1, 0.6), (3, 0.2)]))
check('ritardo: ramo reale e non costante per k^2 < 1/(sigma e)', sp.N(tw.subs({sg: 1, kp: sp.Rational(1, 3)})).is_real and sp.N(tw.subs({sg: 1, kp: sp.Rational(1, 3)})) != sp.N(tw.subs({sg: 1, kp: sp.Rational(1, 4)})))
# sistema aumentato di trasporto: w(t,theta,x) = u(t-theta,x)
U = sp.Function('U')
w = U(t - th, x)
check('ritardo in L+: w_t + w_theta = 0 per w = u(t-theta,x)', sp.simplify(sp.diff(w, t) + sp.diff(w, th)) == 0)
check('ritardo in L+: traccia w(t,0,x)=u, w(t,sigma,x)=u(t-sigma,x)', w.subs(th, 0) == U(t, x) and w.subs(th, sg) == U(t - sg, x))
# --- P8 / dimensione: esponenziali su V(Q1,Q2) in 3 variabili
Q1, Q2 = tau - xi1, tau + xi1
z = sp.symbols('z')
e = sp.exp(z*x2)
def act(Q, f):
    P = sp.Poly(Q, tau, xi1, xi2); out = 0
    for (i, j, l), c in P.terms():
        out += c*sp.diff(f, t, i, x1, j, x2, l)
    return sp.simplify(out)
check('1+2: e^{z x2} in ker Q1 cap ker Q2 per ogni z (ambiguita infinito-dimensionale)', act(Q1, e) == 0 and act(Q2, e) == 0)
F = sp.Function('f')
wf = F(t + x1)
check('1+2: f(t+x1) annullata da tau-xi1 e xi2 (classe eccezionale non EP)', act(tau - xi1, wf) == 0 and act(xi2, wf) == 0)
# in 1+1: (tau-xi, tau+xi) ha codimensione 1
G = sp.groebner([tau - xi, tau + xi], tau, xi, order='grevlex')
check('1+1: dim R/(tau-xi,tau+xi) = 1 (ideale massimale (tau,xi))', set(G.exprs) == {tau, xi})
# comassimali: (tau - xi1, tau - xi1 - 1) = (1)
check('comassimali => ambiguita nulla: (tau-xi1, tau-xi1-1) = (1)', sp.groebner([tau - xi1, tau - xi1 - 1], tau, xi1, xi2).exprs == [1])
# --- Bordo: Dirichlet e Neumann con lo stesso Ann
mu, kap = sp.symbols('mu kappa_0', positive=True)
uD = sp.exp(-kap*t)*sp.sin(mu*x); uN = sp.exp(-kap*t)*sp.cos(mu*x)
gens = [lambda f: sp.diff(f, t) + kap*f, lambda f: sp.diff(f, x, 2) + mu**2*f]
check('bordo: (tau+k0, xi^2+mu^2) annulla sia sin (Dirichlet in 0) sia cos (Neumann in 0)', all(sp.simplify(g(f)) == 0 for g in gens for f in (uD, uN)))
W = sp.Matrix([[sp.diff(f, x, j).subs({t: tv, x: xv}) for j in (0, 1)] for (tv, xv) in [(0, sp.Rational(1, 3)), (0, sp.Rational(2, 7))] for f in [uD]])
check('bordo: dim R.u = 2 per sin e per cos (u, u_x indipendenti) => Ann = (tau+k0, xi^2+mu^2) per entrambi', all(
    sp.simplify(sp.Matrix([[f.subs(x, xv), sp.diff(f, x).subs(x, xv)] for xv in (sp.Rational(1, 3), sp.Rational(2, 7))]).det().subs({t: 0, mu: 1})) != 0 for f in (uD, uN)))
# ostruzione tangenziale: traccia su x=0 del dizionario {1, d_t, d_x} per u = e^{-t} sin x
ub = sp.exp(-t)*sp.sin(x)
tr = [sp.simplify(f.subs(x, 0)) for f in (ub, sp.diff(ub, t), sp.diff(ub, x))]
check('bordo: tracce (0, 0, e^{-t}) => nucleo di dimensione 2, margine rho = 0', tr[0] == 0 and tr[1] == 0 and tr[2] != 0)
# --- RT-R2a su I x T
def modes(f, g, kk):
    fk, gk = sp.Poly(f.subs(xi, sp.I*kk), tau), sp.Poly(g.subs(xi, sp.I*kk), tau)
    return fk, gk
f1, g1 = tau - xi**2, tau + xi
A, B, r = 1, -1, sp.expand(f1 - g1)
check('R2a: Bezout f - g = r(xi) = -xi(xi+1)', sp.factor(r) == -xi*(xi + 1))
res = [kk for kk in range(-20, 21) if sp.degree(sp.gcd(*[p.as_expr() for p in modes(f1, g1, kk)]), tau) > 0]
check('R2a: unico modo risonante k = 0 per f = tau - xi^2, g = tau + xi', res == [0])
fk0, gk0 = modes(f1, g1, 0)
check('R2a: codimensione al modo 0 = deg gcd(tau, tau) = 1 (testimone u = t)', sp.degree(sp.gcd(fk0.as_expr(), gk0.as_expr()), tau) == 1)
g2 = tau + xi + 1
check('R2a: f = tau - xi^2, g = tau + xi + 1: nessuna risonanza su iZ', all(sp.degree(sp.gcd(*[p.as_expr() for p in modes(f1, g2, kk)]), tau) == 0 for kk in range(-30, 31)))
check('R2a: radici comuni di f,g2: xi^2+xi+1 = 0, fuori da iZ', set(sp.solve(xi**2 + xi + 1, xi)) == {sp.Rational(-1, 2) - sp.sqrt(3)*sp.I/2, sp.Rational(-1, 2) + sp.sqrt(3)*sp.I/2})
uu = sp.Function('A')(t) + sp.Function('B')(x)
check('R2a: f = xi, g = tau (retta xi=0 in V(f)): ker(tau xi) = A(t) + B(x) = ker xi + ker tau', sp.diff(uu, t, x) == 0)
# --- Mori-Zwanzig 2x2 a coefficienti costanti (simboli scalari in xi)
a11, a12, a21, a22 = sp.symbols('a11 a12 a21 a22')
uS, vS = sp.Function('u')(t), sp.Function('v')(t)
# soluzione modale: (u,v)' = A (u,v); la legge chiusa per u: u' = a11 u + a12 int_0^t e^{(t-s)a22} a21 u(s) ds + a12 e^{t a22} v0
Amat = sp.Matrix([[a11, a12], [a21, a22]])
vals = {a11: -sp.Rational(1, 3), a12: sp.Rational(2, 5), a21: -sp.Rational(7, 4), a22: -2}
Mx = Amat.subs(vals)
u0, v0 = sp.Rational(1), sp.Rational(3, 2)
sol = (Mx*t).exp()*sp.Matrix([u0, v0])
us = sp.simplify(sol[0])
mem = sp.integrate(sp.exp((t - s)*vals[a22])*vals[a21]*us.subs(t, s), (s, 0, t))
rhs = vals[a11]*us + vals[a12]*mem + vals[a12]*sp.exp(t*vals[a22])*v0
check('MZ: equazione con memoria e "rumore" esatta per la componente u (numerico in 4 tempi)', all(abs(sp.N((sp.diff(us, t) - rhs).subs(t, tv), 30)) < 1e-20 for tv in (0, sp.Rational(1, 3), 1, sp.Rational(5, 2))))
check('MZ: eliminazione locale det(tau - A)(d_t) u = 0', sp.simplify(sp.diff(us, t, 2) - (vals[a11] + vals[a22])*sp.diff(us, t) + (vals[a11]*vals[a22] - vals[a12]*vals[a21])*us) == 0)
# memoria nulla <=> a12 a21 = 0; [P, A] = 0 <=> a12 = a21 = 0
Pm = sp.diag(1, 0)
check('MZ: [P,A] = 0 <=> a12 = a21 = 0', sp.solve(list(Pm*Amat - Amat*Pm), [a12, a21], dict=True) == [{a12: 0, a21: 0}])
check('MZ: controesempio (FALSO del criterio della strada): a21 = 0, a12 = 1: memoria nulla ma [P,A] != 0',
      sp.simplify(sp.Integer(1)*sp.exp(t*a22)*0) == 0 and (Pm*Amat - Amat*Pm).subs({a21: 0, a12: 1}) != sp.zeros(2))
print('ESITO:', 'TUTTI PASS' if ok else 'QUALCHE FAIL')
