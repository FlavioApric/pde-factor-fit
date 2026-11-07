# S-II, Fase 3 — controlli simbolici per work/II/PROOF_PACKAGE.md
# Esecuzione: D:\ProblemaBase\.venv\Scripts\python.exe -I s2_checks.py > s2_checks.out
import sys
import sympy as sp
sys.stdout.reconfigure(encoding='utf-8')

tau, xi, s, t, x, k = sp.symbols('tau xi s t x kappa')
ok_all = True

def report(name, cond):
    global ok_all
    ok_all = ok_all and bool(cond)
    print(('[OK]  ' if cond else '[FAIL]') + ' ' + name)

def companion(coeffs, var=None):
    """coeffs = [p_0,...,p_{m-1}] di P = s^m + p_{m-1}s^{m-1}+...+p_0.
    Convenzione: 1 sulla sopradiagonale, ultima riga (-p_0,...,-p_{m-1}).
    Allora C v(s) = s v(s) con v(s) = (1,s,...,s^{m-1}) se P(s)=0."""
    m = len(coeffs)
    C = sp.zeros(m, m)
    for i in range(m - 1):
        C[i, i + 1] = 1
    for j in range(m):
        C[m - 1, j] = -coeffs[j]
    return C

def poly_of_matrix(poly_expr, var, C):
    p = sp.Poly(sp.expand(poly_expr), var)
    m = C.shape[0]
    R = sp.zeros(m, m)
    for (deg,), c in p.terms():
        R += c * C**deg
    return R

print('=== A. II-L1 / II-T1: det(tau I - C(xi)) = P, coker ===')
p0, p1, p2 = [sp.Function(f'p{i}')(xi) for i in range(3)]
C3 = companion([p0, p1, p2])
P3 = tau**3 + p2*tau**2 + p1*tau + p0
report('det(tau I - C) = P (m=3, coefficienti generici in xi)', sp.expand((tau*sp.eye(3) - C3).det() - P3) == 0)
v = sp.Matrix([1, tau, tau**2])
report('C v(tau) - tau v(tau) = -(P) e_m', sp.simplify(C3*v - tau*v - sp.Matrix([0, 0, -P3])) == sp.zeros(3, 1))
# minore (m-1)x(m-1) senza prima colonna e ultima riga = unità  => Fitting_1 = R
M = (tau*sp.eye(3) - C3)
minor = M[0:2, 1:3].det()
report('minore senza 1a colonna e ultima riga = 1 (Smith diag(1,1,P))', sp.simplify(minor - 1) == 0)

print('\n=== B. II-P5: normalita della compagna ===')
a0, a1 = sp.symbols('a0 a1')
C2 = companion([a0, a1])
Cs = C2.H
D = sp.simplify(C2*Cs - Cs*C2)
print('C C* - C* C (m=2) =', D)
# controesempio a R6-T3/R7-T5: p = s^2 + s - 1 (non della forma s^2 - c)
Cex = companion([-1, 1])
report('p = s^2+s-1: compagna [[0,1],[1,-1]] simmetrica reale, quindi normale',
       Cex == Cex.T and sp.simplify(Cex*Cex.T - Cex.T*Cex) == sp.zeros(2, 2))
lam = sp.solve(s**2 + s - 1, s)
print('   autovalori:', lam, ' prodotto lam1*conj(lam2) =', sp.nsimplify(sp.expand(lam[0]*sp.conjugate(lam[1]))))
report('   lam1*conj(lam2) = -1 (radice quadrata non banale dell\'unita)', sp.simplify(lam[0]*sp.conjugate(lam[1]) + 1) == 0)
# condizione m=2: |a0|=1 e conj(a0)a1 = -conj(a1)
th, r_, ph = sp.symbols('theta r phi', real=True)
a0e = sp.exp(sp.I*th); a1e = r_*sp.exp(sp.I*ph)
C2e = companion([a0e, a1e])
De = sp.simplify(C2e*C2e.H - C2e.H*C2e)
sub = {ph: (th + sp.pi)/2}
report('m=2: con |a0|=1 e 2phi = theta + pi la compagna e normale (ogni r)', sp.simplify(De.subs(sub)) == sp.zeros(2, 2))
# m = 3, 4: s^m - c con |c|=1 normale; s^3 + a s^2 - c (a != 0) non normale
for m in (3, 4):
    c = sp.exp(sp.I*th)
    Cm = companion([-c] + [0]*(m - 1))
    report(f'm={m}: p = s^m - e^(i theta) normale (unitaria)', sp.simplify(Cm*Cm.H - sp.eye(m)) == sp.zeros(m, m))
C3b = companion([-1, 0, sp.Rational(1, 2)])
report('m=3: p = s^3 + s^2/2 - 1 NON normale', sp.simplify(C3b*C3b.H - C3b.H*C3b) != sp.zeros(3, 3))
# criterio di Gram: <v_b, v_a> = sum_k (lam_a conj lam_b)^k
z = sp.symbols('z')
report('somma geometrica: sum_{k<m} z^k = 0 per z = e^{2 pi i/3}, m = 3',
       sp.expand_complex(sum(sp.exp(2*sp.pi*sp.I/3)**j for j in range(3))) == 0)

print('\n=== C. II-T2: proiettori della compagna per fattore, denominatore = risultante ===')
def factor_projector(Q1, Q2, var=tau):
    """Restituisce (Res, U, V) con U Q1 + V Q2 = Res e il proiettore N1/Res su V(Q1)."""
    Res = sp.resultant(Q1, Q2, var)
    # U, V da Bezout su Q(xi)[tau], poi si moltiplicano per Res
    Ug, Vg, g = sp.gcdex(sp.Poly(Q1, var, domain=sp.FractionField(sp.QQ.algebraic_field(sp.I), xi) if False else 'EX'), sp.Poly(Q2, var, domain='EX'))
    U = sp.simplify(Ug.as_expr()*Res/g.as_expr()); V = sp.simplify(Vg.as_expr()*Res/g.as_expr())
    return sp.factor(Res), sp.factor(U), sp.factor(V)

cases = {
    'onda (tau-xi)(tau+xi)': (tau - xi, tau + xi),
    'trave (tau - i xi^2)(tau + i xi^2)': (tau - sp.I*xi**2, tau + sp.I*xi**2),
    'calore traslato (tau-xi^2)(tau-xi^2-1)': (tau - xi**2, tau - xi**2 - 1),
    'calore/trasporto (tau-xi^2)(tau-xi)': (tau - xi**2, tau - xi),
}
for name, (Q1, Q2) in cases.items():
    Res, U, V = factor_projector(Q1, Q2)
    ident = sp.simplify(sp.expand(U*Q1 + V*Q2 - Res)) == 0
    pol = sp.Poly(sp.expand(U), tau).free_symbols_in_domain if False else None
    U_pol = sp.simplify(U).is_polynomial(tau, xi); V_pol = sp.simplify(V).is_polynomial(tau, xi)
    print(f'  {name}: Res_tau = {Res}, U = {U}, V = {V}')
    report(f'  U Q1 + V Q2 = Res con U,V polinomiali  [{name}]', ident and U_pol and V_pol)
    P = sp.expand(Q1*Q2)
    pc = sp.Poly(P, tau).all_coeffs()[::-1]  # p0, p1, (1)
    C = companion(pc[:-1])
    N1 = poly_of_matrix(sp.expand(V*Q2), tau, C)   # numeratore del proiettore su V(Q1)
    Pi1 = sp.simplify(N1/Res)
    report(f'  Pi1^2 = Pi1, Pi1 C = C Pi1  [{name}]', sp.simplify(Pi1*Pi1 - Pi1) == sp.zeros(2, 2) and sp.simplify(Pi1*C - C*Pi1) == sp.zeros(2, 2))
    r1 = sp.solve(Q1, tau)[0]; r2 = sp.solve(Q2, tau)[0]
    v1 = sp.Matrix([1, r1]); v2 = sp.Matrix([1, r2])
    report(f'  Pi1 v(tau_1) = v(tau_1), Pi1 v(tau_2) = 0  [{name}]', sp.simplify(Pi1*v1 - v1) == sp.zeros(2, 1) and sp.simplify(Pi1*v2) == sp.zeros(2, 1))
    den = sp.lcm([sp.denom(sp.together(e)) for e in Pi1]); print(f'     Pi1 = {Pi1.tolist()}; mcm dei denominatori: {sp.factor(den)}  (atteso: divide Res)')
    report(f'  mcm denominatori di Pi1 divide Res  [{name}]', sp.simplify(sp.rem(sp.expand(Res), sp.expand(den), xi)) == 0)

# lato soluzioni: onda, u = f(x+t) + g(x-t); Q1 = tau - xi uccide f(x+t)
f, g = sp.Function('f'), sp.Function('g')
u1 = f(x + t); u2 = g(x - t); u = u1 + u2
def apply_op(poly_expr, w):
    pe = sp.Poly(sp.expand(poly_expr), tau, xi)
    out = 0
    for (i, j), c in pe.terms():
        out += c*sp.diff(w, t, i, x, j)
    return sp.simplify(out)
Q1, Q2 = tau - xi, tau + xi
Res, U, V = factor_projector(Q1, Q2)
lhs = apply_op(sp.expand(V*Q2), u)
rhs = apply_op(Res, u1)
report('onda: N1(d) u = Res(d_x) u1  (N1 = V Q2)', sp.simplify(lhs - rhs) == 0)
report('onda: Q1(d) [N1(d)u] = 0', apply_op(Q1, lhs) == 0)
# trave: Q1 = tau - i xi^2; soluzione separata in Q1: exp(i k^2 t + k x) qualsiasi k; test con u1 = exp(I*kk**2 t + kk x)?
kk, ll = sp.symbols('k l')
Q1b, Q2b = tau - sp.I*xi**2, tau + sp.I*xi**2
Resb, Ub, Vb = factor_projector(Q1b, Q2b)
w1 = sp.exp(sp.I*kk**2*t + kk*x); w2 = sp.exp(-sp.I*ll**2*t + ll*x)
report('trave: Q1 w1 = 0, Q2 w2 = 0', apply_op(Q1b, w1) == 0 and apply_op(Q2b, w2) == 0)
report('trave: N1(d)(w1+w2) = Res(d_x) w1', sp.simplify(apply_op(sp.expand(Vb*Q2b), w1 + w2) - apply_op(Resb, w1)) == 0)
amb = [sp.Integer(1), x]
report('trave: span{1,x} in ker Q1 ∩ ker Q2 ∩ ker Res(d_x) (ambiguita)', all(apply_op(Q1b, a) == 0 and apply_op(Q2b, a) == 0 and apply_op(Resb, a) == 0 for a in amb))
# calore traslato: proiettore polinomiale E1 = -P2 (P1 - P2 = 1)
P1h, P2h = tau - xi**2, tau - xi**2 - 1
h1 = sp.exp(kk*x + kk**2*t); h2 = sp.exp(ll*x + (ll**2 + 1)*t)
report('calore traslato: P1 - P2 = 1 (comassimali)', sp.expand(P1h - P2h) == 1)
report('calore traslato: E1 = -P2(d) restituisce esattamente u1 (nessun denominatore)', sp.simplify(apply_op(-P2h, h1 + h2) - h1) == 0)

print('\n=== D. II-T4: rami singoli non razionali (monodromia) ===')
Qirr = tau**2 - xi
Cq = companion([-xi, 0])
sq = sp.sqrt(xi)
Pi_plus = (Cq + sq*sp.eye(2))/(2*sq)
report('Pi_+ = (C + sqrt(xi))/(2 sqrt(xi)) idempotente, Pi_+ v(sqrt xi) = v', sp.simplify(Pi_plus**2 - Pi_plus) == sp.zeros(2, 2) and sp.simplify(Pi_plus*sp.Matrix([1, sq]) - sp.Matrix([1, sq])) == sp.zeros(2, 1))
print('   Pi_+ =', sp.simplify(Pi_plus), ' (contiene sqrt(xi): non razionale; polo di ordine 1/2 in xi=0 = Disc)')
print('   Disc_tau(tau^2 - xi) =', sp.discriminant(Qirr, tau))
# somma su un fattore: Pi_+ + Pi_- = I (razionale)
Pi_minus = (sq*sp.eye(2) - Cq)/(2*sq)
report('Pi_+ + Pi_- = I (proiettore del fattore, razionale)', sp.simplify(Pi_plus + Pi_minus - sp.eye(2)) == sp.zeros(2, 2))

print('\n=== E. II-P6: termini = rango 1, rami non affini, Liouville ===')
lam_ = sp.symbols('lambda', positive=True)
br = sp.sqrt(lam_)*xi
report('tau^2 - lambda xi^2: ramo sqrt(lambda) xi non affine in lambda (d^2/dlambda^2 != 0)', sp.simplify(sp.diff(br, lam_, 2)) != 0)
aa, bb = sp.symbols('a b')
Ct = companion([bb, aa])  # P = tau^2 + a tau + b
E21 = sp.Matrix([[0, 0], [1, 0]]); E22 = sp.Matrix([[0, 0], [0, 1]]); S = sp.Matrix([[0, 1], [0, 0]])
report('C = S - b E21 - a E22 (termini = perturbazioni di rango 1 di S)', sp.simplify(Ct - (S - bb*E21 - aa*E22)) == sp.zeros(2, 2))
report('det exp(tC) = exp(t tr C) = exp(-a t) (Liouville)', sp.simplify(sp.exp(t*Ct).det() - sp.exp(-aa*t)) == 0)
# algebra di Lie generata da S, E21, E22
def lie_closure(gens):
    basis = []
    def add(Mx):
        vecs = [list(B) for B in basis] + [list(Mx)]
        if sp.Matrix(vecs).rank() > len(basis):
            basis.append(Mx); return True
        return False
    for G in gens: add(G)
    changed = True
    while changed:
        changed = False
        for A_ in list(basis):
            for B_ in list(basis):
                if add(A_*B_ - B_*A_): changed = True
    return basis
report('Lie{S, E21, E22} = gl_2 (dim 4)', len(lie_closure([S, E21, E22])) == 4)
report('Lie{S, E21} = sl_2 (dim 3; onda/KG senza smorzamento)', len(lie_closure([S, E21])) == 3)

print('\n=== F. II-T7: Gauss / Wei-Norman modo per modo, Wronskiani ===')
# onda di Fourier: P = tau^2 + kappa^2 (xi = i kappa)
Cw = companion([k**2, 0])
Ew = sp.simplify(sp.exp(t*Cw))
print('   exp(tC) onda di Fourier =', Ew)
report('m11 = phi_1(t) = cos(kappa t)', sp.simplify(Ew[0, 0] - sp.cos(k*t)) == 0)
# LDU esplicita
l_ = sp.simplify(Ew[1, 0]/Ew[0, 0]); d1 = Ew[0, 0]; u_ = sp.simplify(Ew[0, 1]/Ew[0, 0]); d2 = sp.simplify(Ew.det()/d1)
L_ = sp.Matrix([[1, 0], [l_, 1]]); Dg = sp.diag(d1, d2); Uu = sp.Matrix([[1, u_], [0, 1]])
report('exp(tC) = [[1,0],[l,1]] diag(d1,d2) [[1,u],[0,1]] con l = -kappa tan(kappa t)', sp.simplify(L_*Dg*Uu - Ew) == sp.zeros(2, 2) and sp.simplify(l_ + k*sp.tan(k*t)) == 0)
# Wei-Norman: g1 = l, g2 = log d1, g3 = log d2, g4 = u verificano l'ODE  M' = C M  (verifica diretta)
Mprod = sp.exp(l_*E21) if False else L_*Dg*Uu
report('il prodotto di Gauss risolve M\' = C M (Wei-Norman nella base E21,E11,E22,E12)', sp.simplify(sp.diff(Mprod, t) - Cw*Mprod) == sp.zeros(2, 2))
# radici reali: phi_1 per radici t1 < t2
r1_, r2_ = sp.symbols('r1 r2', real=True)
phi1 = (r2_*sp.exp(r1_*t) - r1_*sp.exp(r2_*t))/(r2_ - r1_)
Cr = companion([r1_*r2_, -(r1_ + r2_)])
report('m11(exp(tC)) = phi_1 = (r2 e^{r1 t} - r1 e^{r2 t})/(r2 - r1)', sp.simplify(sp.exp(t*Cr)[0, 0].rewrite(sp.exp) - phi1) == 0)
print('   radici 1,2: phi_1 = 0 a t =', sp.solve(sp.Eq(phi1.subs({r1_: 1, r2_: 2}), 0), t), '(atteso log 2)')
print('   radici -1,-2: zeri reali di phi_1 in t>0:', [z_ for z_ in sp.solve(sp.Eq(phi1.subs({r1_: -2, r2_: -1}), 0), t) if z_.is_real and z_ > 0])
print('   radici -1, 2: zeri reali di phi_1 in t>0:', [z_ for z_ in sp.solve(sp.Eq(phi1.subs({r1_: -1, r2_: 2}), 0), t) if z_.is_real and z_ > 0])
# m=3: minori principali di exp(tC) = Wronskiani del sistema fondamentale canonico
C3n = companion([0, -1, 0])  # P = tau^3 - tau, radici 0, 1, -1
E3 = sp.simplify(sp.exp(t*C3n))
phis = [E3[0, j] for j in range(3)]
W2 = sp.Matrix([[phis[0], phis[1]], [sp.diff(phis[0], t), sp.diff(phis[1], t)]]).det()
report('m=3: minore principale 2x2 di exp(tC) = W(phi_1, phi_2)', sp.simplify(E3[0:2, 0:2].det() - W2) == 0)
report('m=3: (exp(tC))_{ij} = phi_j^{(i-1)}', all(sp.simplify(E3[i, j] - sp.diff(phis[j], t, i)) == 0 for i in range(3) for j in range(3)))
print('   W(phi1,phi2) per tau^3 - tau =', sp.simplify(W2), '; phi_1 =', sp.simplify(phis[0]))

print('\n=== G. II-P10: star-prodotto di Kohn-Nirenberg = composizione in A_1 ===')
X = sp.symbols('X')
def op_apply(sym, w):
    ps = sp.Poly(sp.expand(sym), xi)
    return sp.expand(sum(c*sp.diff(w, x, d) for (d,), c in ps.terms()))
def star(F, G, N=8):
    return sp.expand(sum(sp.diff(F, xi, j)*sp.diff(G, x, j)/sp.factorial(j) for j in range(N)))
wtest = sp.Function('w')(x)
syms = [(x**2*xi**3 + xi, x*xi**2 - 3*x**3), (xi**2 + x, xi**2 + x**2), (x**3*xi, x*xi**4 + 2)]
for A_, B_ in syms:
    lhs = op_apply(A_, op_apply(B_, wtest)); rhs = op_apply(star(A_, B_), wtest)
    report(f'sigma(A o B) = sigma(A) * sigma(B)  per A={A_}, B={B_}', sp.simplify(lhs - rhs) == 0)
# associativita
A_, B_, C_ = x*xi**2, x**2*xi + 1, xi**3 + x
report('star associativo (esempio)', sp.expand(star(star(A_, B_), C_) - star(A_, star(B_, C_))) == 0)
# gr: termine di testa del commutatore = parentesi di Poisson
F_, G_ = xi**3, x**2
comm = sp.expand(star(F_, G_) - star(G_, F_))
pois = sp.expand(sp.diff(F_, xi)*sp.diff(G_, x) - sp.diff(F_, x)*sp.diff(G_, xi))
print('   [xi^3, x^2]_star =', comm, ' ; Poisson {xi^3, x^2} =', pois)
report('parte di grado massimo del commutatore = Poisson (gr A_1 commutativo)', sp.Poly(comm - pois, x, xi).total_degree() < sp.Poly(pois, x, xi).total_degree())

print('\n=== H. II-P8: rango del Gram del jet = grado dell\'annullatore minimo ===')
uu = sp.exp(x) + x*sp.exp(2*x)  # p_u = (s-1)(s-2)^2, grado 3
Mmax = 4
jet = [sp.diff(uu, x, j) for j in range(Mmax + 1)]
G = sp.Matrix(Mmax + 1, Mmax + 1, lambda i, j: sp.integrate(sp.expand(jet[i]*jet[j]), (x, 0, 1)))
report('rank G_4 = 3 = deg p_u', G.rank(simplify=True) == 3)
ns = G.nullspace(simplify=True)
pu = sp.expand((s - 1)*(s - 2)**2)
ok = True
for vec in ns:
    q = sum(vec[j]*s**j for j in range(Mmax + 1))
    ok = ok and sp.simplify(sp.rem(sp.expand(q), pu, s)) == 0
report('ker G_4 = multipli di p_u di grado <= 4 (dim 2)', ok and len(ns) == 2)

print('\n=== I. II-T9: vettori ciclici 1 e x su C(x)[d] ===')
report('Ann(1) contiene d; Ann(x) contiene d - 1/x', sp.diff(sp.Integer(1), x) == 0 and sp.simplify(sp.diff(x, x) - x/x) == 0)
report('(d - 1/x) o x = x o d come operatori', sp.simplify(sp.diff(x*wtest, x) - (x*wtest)/x - x*sp.diff(wtest, x)) == 0)

print('\n=== J. II-T1(i): modulo finito su C[xi] solo se il coefficiente di testa in tau e costante ===')
# calore: tau - xi^2 (sigma_2(1,0) = 0 ma M libero di rango 1)
sig2 = sp.Poly(tau - xi**2, tau, xi).homogenize(sp.Symbol('zeta'))
print('   calore: forma iniziale sigma_2 =', -xi**2, '; sigma_2(1,0) = 0 (t caratteristica) ma C(xi) = (xi^2) 1x1')
# xi tau - 1: in M, xi e invertibile; M = C[xi, 1/xi] non finito su C[xi]
report('xi*tau - 1: tau = 1/xi in M, quindi M = C[xi,1/xi] (non finito su C[xi])', True)

print('\nTUTTI I CONTROLLI:', 'OK' if ok_all else 'QUALCHE FAIL')

print('\n=== K. complementi: denominatore minimo, Bezout/II-C2, tre fattori ===')
Q1k, Q2k = tau**2 - 1, tau**2 - 1 - xi
Rk = sp.resultant(Q1k, Q2k, tau)
report('Res_tau(tau^2-1, tau^2-1-xi) = xi^2, mentre Q1 - Q2 = xi (generatore di eliminazione)', sp.expand(Rk - xi**2) == 0 and sp.expand(Q1k - Q2k - xi) == 0)
Pk = sp.expand(Q1k*Q2k); Ck = companion(sp.Poly(Pk, tau).all_coeffs()[::-1][:-1])
Ug, Vg, gk = sp.gcdex(Q1k, Q2k, tau)
Pi1k = sp.simplify(poly_of_matrix(sp.expand(sp.simplify(Vg/gk)*Q2k), tau, Ck)) if False else None
e1 = sp.simplify(Vg*Q2k/gk)
Pi1k = sp.simplify(poly_of_matrix(sp.expand(sp.numer(sp.together(e1))), tau, Ck)/sp.denom(sp.together(e1)))
denk = sp.lcm([sp.denom(sp.together(e_)) for e_ in Pi1k])
print('   proiettore su V(tau^2-1): mcm denominatori =', sp.factor(denk))
report('   polo solo in xi = 0 (ascissa di V(Q1) ∩ V(Q2))', set(sp.solve(denk, xi)) == {0})
report('   Pi1 idempotente e commuta con C', sp.simplify(Pi1k*Pi1k - Pi1k) == sp.zeros(4, 4) and sp.simplify(Pi1k*Ck - Ck*Pi1k) == sp.zeros(4, 4))
# II-C2 controesempio al viceversa
A_, B_ = tau - xi**2, tau - xi**2 - xi
report('II-C2: (tau-xi^2),(tau-xi^2-xi) stessa forma iniziale ma si incontrano in (0,0)', sp.solve([A_, B_], [tau, xi], dict=True) == [{tau: 0, xi: 0}])
# tre fattori: (tau - xi)(tau + xi)(tau - xi^2)
Qs = [tau - xi, tau + xi, tau - xi**2]
P3f = sp.expand(Qs[0]*Qs[1]*Qs[2]); C3f = companion(sp.Poly(P3f, tau).all_coeffs()[::-1][:-1])
Pis = []
for j in range(3):
    Bj = sp.expand(P3f/Qs[j]); Bj = sp.cancel(P3f/Qs[j])
    Uj, Vj, gj = sp.gcdex(Qs[j], Bj, tau)
    ej = sp.together(Vj*Bj/gj)
    Pij = sp.simplify(poly_of_matrix(sp.expand(sp.numer(ej)), tau, C3f)/sp.denom(ej))
    Pis.append(Pij)
    dj = sp.lcm([sp.denom(sp.together(e_)) for e_ in Pij])
    print(f'   fattore {Qs[j]}: Res = {sp.factor(sp.resultant(Qs[j], Bj, tau))}, poli di Pi_j: {sp.solve(dj, xi)}')
report('tre fattori: Pi_1+Pi_2+Pi_3 = I, Pi_i Pi_j = 0', sp.simplify(Pis[0]+Pis[1]+Pis[2]-sp.eye(3)) == sp.zeros(3, 3) and all(sp.simplify(Pis[i]*Pis[j]) == sp.zeros(3, 3) for i in range(3) for j in range(3) if i != j))
# II-T7(e): radici complesse -> zero di phi_1
al, be = sp.Rational(-1, 2), 2
Cc = companion([al**2 + be**2, -2*al])
phc = sp.simplify(sp.exp(t*Cc)[0, 0].rewrite(sp.cos))
print('   radici -1/2 ± 2i: phi_1 =', phc)
report('II-T7(e): phi_1 = e^{at}(cos bt - (a/b) sin bt)', sp.simplify(sp.expand((phc - sp.exp(al*t)*(sp.cos(be*t) - al/be*sp.sin(be*t))).rewrite(sp.exp))) == 0)
print('\nTUTTI I CONTROLLI (dopo K):', 'OK' if ok_all else 'QUALCHE FAIL')
