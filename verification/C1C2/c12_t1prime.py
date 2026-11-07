# S-C1C2 (ripresa 2) · esplorazione e controlli per C12-T1' (scomposizione per fattori su Omega
# semplicemente connesso), C12-P10 (necessità), fix II-T2-F1 su C12-T2(iv).
# Eseguire: D:\ProblemaBase\.venv\Scripts\python.exe -I c12_t1prime.py
# Nota: è esplorazione/controllo, NON la prova (math-skill: esplorazione separata dalla prova).
from sympy import (symbols, Function, exp, log, diff, simplify, expand, I, pi, cos, sin, integrate,
                   Matrix, Poly, groebner, linsolve, eye, zeros, Rational, atan2, sqrt, re, im, N,
                   factor, cancel, together, limit, oo, Symbol)
import mpmath as mp

tau, xi, t, x, th = symbols('tau xi t x theta', real=True)
p, q = symbols('p q')
PASS = 0; FAIL = 0
def check(name, cond):
    global PASS, FAIL
    if cond: PASS += 1; print('PASS', name)
    else: FAIL += 1; print('FAIL', name)

def apply_op(Pexpr, u):
    P_ = Poly(expand(Pexpr), tau, xi)
    return sum(c*diff(u, t, i, x, j) for (i, j), c in P_.terms())

def quot_dim(gens):
    G = groebner(gens, tau, xi, order='grevlex')
    if list(G.exprs) == [1]: return 0
    lead = [Poly(g, tau, xi).monoms(order='grevlex')[0] for g in G.exprs]
    cnt = 0
    for a in range(40):
        for b in range(40):
            if not any(a >= l[0] and b >= l[1] for l in lead): cnt += 1
    return cnt

print('== E1: Koszul torto = de Rham coniugato (indipendente da Omega) ==')
wt, ph, ps = [Function(n)(t, x) for n in ('wt', 'ph', 'ps')]
e = exp(p*t + q*x)
Dt = lambda f: diff(f, t) - p*f
Dx = lambda f: diff(f, x) - q*f
beta = lambda w: (Dt(w), Dx(w))
alpha = lambda a, b: -Dx(a) + Dt(b)
b1, b2 = beta(e*wt)
check('E1 e^-1 beta*(e w) = (w_t, w_x)', simplify(b1/e - diff(wt, t)) == 0 and simplify(b2/e - diff(wt, x)) == 0)
check('E1 e^-1 alpha*(e phi, e psi) = d(phi dt + psi dx) = psi_t - phi_x',
      simplify(alpha(e*ph, e*ps)/e - (diff(ps, t) - diff(ph, x))) == 0)
check('E1 alpha* o beta* = 0', simplify(alpha(*beta(e*wt))) == 0)

print('== E2: Laplaciano su corona / disco bucato: ostruzione = periodo non nullo ==')
P = tau**2 + xi**2; Q1 = tau - I*xi; Q2 = tau + I*xi
check('E2 P = Q1 Q2', expand(Q1*Q2 - P) == 0)
check('E2 dim R/(Q1,Q2) = 1 (V = {0})', quot_dim([Q1, Q2]) == 1)
u = log(t**2 + x**2)
check('E2 u = log r^2 in ker P', simplify(apply_op(P, u)) == 0)
F = simplify(apply_op(Q2, u))
check('E2 F := Q2 u = 2/(t - i x)', simplify(F - 2/(t - I*x)) == 0)
check('E2 F in ker Q1', simplify(apply_op(Q1, F)) == 0)
# se u = h + k, Q1 h = 0, Q2 k = 0 allora Q2 h = F e Q1 h = 0 => dh = (F/2) dt + (F/(2i)) dx
a_, b_ = F/2, F/(2*I)
check('E2 forma (F/2)dt + (F/2i)dx chiusa', simplify(diff(b_, t) - diff(a_, x)) == 0)
para = {t: cos(th), x: sin(th)}
integrand = simplify((a_.subs(para))*diff(cos(th), th) + (b_.subs(para))*diff(sin(th), th))
per = simplify(integrate(integrand, (th, 0, 2*pi)))
print('   periodo sul cerchio unitario =', per)
check('E2 periodo = -2 pi i != 0 => nessuna h su Omega che contiene il cerchio e non 0', simplify(per + 2*pi*I) == 0)

print('== E3: disco tagliato (semplicemente connesso, NON convesso, NON rettangolo): la scomposizione esiste ==')
h = log(t - I*x); k = log(t + I*x)   # rami principali; t -+ i x non in (-inf,0] fuori dal taglio {x=0, t<=0}
check('E3 Q1 h = 0', simplify(apply_op(Q1, h)) == 0)
check('E3 Q2 k = 0', simplify(apply_op(Q2, k)) == 0)
pts = [(0.3, 0.4), (-0.5, 0.01), (-0.5, -0.01), (-0.2, 0.7), (0.01, -0.9), (-0.9, 0.3)]
ok = True
for (tt, xx) in pts:
    val = complex(mp.log(mp.mpc(tt, -xx)) + mp.log(mp.mpc(tt, xx)))
    ok = ok and abs(val - float(mp.log(tt**2 + xx**2))) < 1e-12
check('E3 Log(t-ix)+Log(t+ix) = log r^2 sul disco tagliato (6 punti, anche vicino al taglio)', ok)

print('== E4: disco bucato, P = tau xi, u = H(x)H(t) in D\': sistema delle costanti incompatibile ==')
ap, am, bp, bm = symbols('a_p a_m b_p b_m')
# A = a_+(x) su {x>0}, a_-(x) su {x<0} (semidischi convessi, L5); B = b_+(t), b_-(t); costanti dai quadranti
sys = [ap + bp - 1, am + bp, am + bm, ap + bm]   # Q1 (x>0,t>0): u=1; altrove u=0
check('E4 sistema dei quadranti senza soluzione', len(linsolve(sys, [ap, am, bp, bm])) == 0)

print('== E5: disco bucato, P = tau xi in C^infty: la scomposizione ESISTE (dipende da P e da A) ==')
# u liscia in ker d_t d_x sul disco bucato: phi = d_t u e' funzione della sola t (fette orizzontali connesse per t != 0,
# continuita' in t = 0). Esempio esplicito: u = alpha(x) beta(t) con alpha' beta' = 0 su Omega forza alpha' = 0 o beta' = 0
# vicino a ogni punto; controllo su un esempio non banale costruito: u = a(x) + b(t) + c * (t*x)^0 -> banale.
# Controllo strutturale: per u = H_eps(x)H_eps(t) (liscia su R^2) fgu = d_t d_x u = delta_eps(t)delta_eps(x) NON nullo vicino a 0:
# non e' in ker su un disco bucato con buco di raggio < eps*sqrt(2): nessun controesempio liscio di tipo O-1 con buco puntiforme.
eps = Rational(1, 10)
print("   (nota, nessun controllo automatico: il caso C^infty e' dimostrato in PROOF_PACKAGE C12-P10(c))")

print('== E6: versione torta del controesempio Laplaciano ==')
Pt = expand((tau - p - I*(xi - q))*(tau - p + I*(xi - q)))
ut = exp(p*t + q*x)*log(t**2 + x**2)
check('E6 e^{pt+qx} log r^2 in ker P_(p,q)', simplify(apply_op(Pt, ut)) == 0)
Pn = Pt.subs({p: 2, q: -1})
check('E6 dim R/(Q1,Q2) = 1 nel punto (2,-1)', quot_dim([tau - 2 - I*(xi + 1), tau - 2 + I*(xi + 1)]) == 1)

print('== E7: corrente di Heaviside: periodo della forma mollificata = +-1 (prova di C12-P10, caso tau xi) ==')
epsv = mp.mpf('0.02')
dl = lambda s: mp.exp(-(s/epsv)**2)/(epsv*mp.sqrt(mp.pi))
Hs = lambda s: (1 + mp.erf(s/epsv))/2
# forma omega_eps = H_eps(x) delta_eps(t) dt, cerchio (t,x) = (cos th, sin th)
val = mp.quad(lambda s: Hs(mp.sin(s))*dl(mp.cos(s))*(-mp.sin(s)), [0, mp.pi/2 - 0.2, mp.pi/2, mp.pi/2 + 0.2, 3*mp.pi/2 - 0.2, 3*mp.pi/2, 3*mp.pi/2 + 0.2, 2*mp.pi])
print('   periodo =', mp.nstr(val, 12))
check('E7 periodo = -1 (|err| < 1e-8)', abs(val + 1) < 1e-8)

print('== E8: fix II-T2-F1 su C12-T2(iv): a = (2, xi, -xi), punto rho = 0 dove collidono i rami 2,3 ==')
a = [2 + 0*xi, xi, -xi]
k_ = 3
Pa = expand((tau - a[0])*(tau - a[1])*(tau - a[2]))
c = Poly(Pa, tau).all_coeffs()[::-1]      # c0, c1, c2, 1
C = zeros(k_, k_)
for i in range(k_ - 1): C[i, i + 1] = 1
for j in range(k_): C[k_ - 1, j] = -c[j]
V = Matrix(k_, k_, lambda l, j: a[j]**l)
check('E8 colonne di V autovettori destri della compagna (1 sopradiag., ultima riga -c_j) [T2-2]',
      all(simplify(C*V[:, j] - a[j]*V[:, j]) == zeros(k_, 1) for j in range(k_)))
Vi = V.inv()
Pi = [simplify(V[:, j]*Vi[j, :]) for j in range(k_)]
def has_pole0(M):
    return any(limit(abs(m), xi, 0) == oo for m in M if cancel(m).as_numer_denom()[1].subs(xi, 0) == 0)
check('E8 Pi_1 regolare in 0 (il suo ramo non collide)', all(cancel(m).as_numer_denom()[1].subs(xi, 0) != 0 for m in Pi[0]))
check('E8 Pi_2, Pi_3 hanno un polo in 0', all(any(cancel(m).as_numer_denom()[1].subs(xi, 0) == 0 for m in Pi[j]) for j in (1, 2)))
P10 = Pi[0].subs(xi, 0); C0 = C.subs(xi, 0)
B1 = (C0 - a[1].subs(xi, 0)*eye(3))*(C0 - a[2].subs(xi, 0)*eye(3))   # B_1(0, C0) = C0^2
kerB = B1.nullspace(); kerC = C0.nullspace()
check('E8 dim ker B_1(0,C0) = 2, dim ker(C0 - a_2(0)) = 1 (blocco di Jordan)', len(kerB) == 2 and len(kerC) == 1)
check('E8 Pi_1(0) annulla ker B_1(0,C0) (proietta LUNGO ker B_j, fix F1)', all(P10*v == zeros(3, 1) for v in kerB))
check('E8 Pi_1(0) di rango 1, idempotente, immagine = v_1(0)', P10.rank() == 1 and simplify(P10*P10 - P10) == zeros(3, 3)
      and simplify(P10*V[:, 0].subs(xi, 0) - V[:, 0].subs(xi, 0)) == zeros(3, 1))

print()
print(f'RISULTATO: {PASS} PASS, {FAIL} FAIL')
