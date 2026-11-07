"""S9-ALG, esempi L9 e L10 (verifiche V-ex, numerica solo come controllo).
L9: u = e^{-t}e^{ix} + e^{-2t}e^{2ix} risolve u_t = -|D| u (moltiplicatore |k|, non locale) e ANCHE la legge
    locale u_t = i u_x: dato EP, legge non locale indistinguibile (CONV-T6, C3-C2).
L10: dizionario a coefficienti costanti, D_0 = d_t, sul calore u = (t+1)^{-1/2} exp(-x^2/(4(t+1))),
    Omega = (0,1) x (-1,1), Y = L^2(Omega).
    (a) livello affine 1 (atomi 1, d_x): r_1 > 0, misfit certificato da MF2 (rapporto di Gram);
    (b) livello affine 2 (atomi 1, d_x, d_x^2, d_t d_x, d_t^2): r_2 = 0, minimizzatore d_t - d_x^2;
        livello omogeneo 2: una sola lambda_min nulla (Ann(u) cap R_{<=2} = C(tau - xi^2));
    (c) CONV-T4(a): perturbazione u~ = u + eps*cos(3x): sin(angolo) <= 2 delta / rho, delta = ||u~ - u||_{H^2};
    (d) DICT-RANGO / (H-ex): u = t + sin x nella classe u_t = a u_xx + b u: ker Phi_u = 0 ma nessuna legge.
"""
import sympy as sp
import mpmath as mp

t, x = sp.symbols('t x', real=True)
ok = []

# ---------- L9
u9 = sp.exp(-t) * sp.exp(sp.I * x) + sp.exp(-2 * t) * sp.exp(2 * sp.I * x)
absD_u9 = 1 * sp.exp(-t) * sp.exp(sp.I * x) + 2 * sp.exp(-2 * t) * sp.exp(2 * sp.I * x)  # |D| sui modi k = 1, 2
ok.append(('L9 u_t = -|D| u', sp.simplify(sp.diff(u9, t) + absD_u9) == 0))
ok.append(('L9 u_t = i u_x (legge locale)', sp.simplify(sp.diff(u9, t) - sp.I * sp.diff(u9, x)) == 0))

# ---------- L10
mp.mp.dps = 25
u = (t + 1)**sp.Rational(-1, 2) * sp.exp(-x**2 / (4 * (t + 1)))
ok.append(('L10 u risolve il calore', sp.simplify(sp.diff(u, t) - sp.diff(u, x, 2)) == 0))
atoms = {'1': u, 'dx': sp.diff(u, x), 'dxx': sp.diff(u, x, 2), 'dtdx': sp.diff(u, t, x),
         'dtt': sp.diff(u, t, 2), 'dt': sp.diff(u, t)}
fl = {k: sp.lambdify((t, x), v, 'mpmath') for k, v in atoms.items()}
def ip(f, g):
    return mp.quad(lambda a, b: f(a, b) * g(a, b), [0, 1], [-1, 1])
def gram(names):
    return mp.matrix([[ip(fl[i], fl[j]) for j in names] for i in names])
def rres(names):  # r_n^2 = det G(D0, D...)/det G(D...)
    return mp.sqrt(mp.det(gram(['dt'] + names)) / mp.det(gram(names)))
lev1 = ['1', 'dx']
lev2 = ['1', 'dx', 'dxx', 'dtdx', 'dtt']
r1 = rres(lev1)
G2 = gram(lev2); b2 = mp.matrix([ip(fl[i], fl['dt']) for i in lev2])
c2 = mp.lu_solve(G2, -b2)
res2 = lambda a, b: fl['dt'](a, b) + sum(c2[i] * fl[n](a, b) for i, n in enumerate(lev2))
r2 = mp.sqrt(ip(res2, res2))
print('    r_1 =', mp.nstr(r1, 8), '  r_2 =', mp.nstr(r2, 5))
print('    coefficienti livello 2 (1, dx, dxx, dtdx, dtt):', [mp.nstr(c, 8) for c in c2])
ok.append(('L10(a) misfit al livello 1: r_1 > 1e-3', r1 > 1e-3))
ok.append(('L10(b) fit al livello 2: r_2 < 1e-10', r2 < 1e-10))
ok.append(('L10(b) minimizzatore = d_t - d_x^2', abs(c2[2] + 1) < 1e-10 and
           max(abs(c2[i]) for i in (0, 1, 3, 4)) < 1e-10))
hom2 = ['1', 'dt', 'dx', 'dxx', 'dtdx', 'dtt']
ev = sorted(mp.eigsy(gram(hom2))[0])
print('    autovalori Gram omogeneo livello 2:', [mp.nstr(e, 4) for e in ev])
ok.append(('L10(b) esattamente un autovalore nullo', abs(ev[0]) < 1e-15 and ev[1] > 1e-8))

# (c) CONV-T4(a) al livello minimo d = 2 (omogeneo)
rho = mp.sqrt(ev[1])
eps = mp.mpf('1e-3')
pert = {'1': lambda a, b: mp.cos(3 * b), 'dt': lambda a, b: 0, 'dx': lambda a, b: -3 * mp.sin(3 * b),
        'dxx': lambda a, b: -9 * mp.cos(3 * b), 'dtdx': lambda a, b: 0, 'dtt': lambda a, b: 0}
flp = {k: (lambda k: (lambda a, b: fl[k](a, b) + eps * pert[k](a, b)))(k) for k in hom2}
Gp = mp.matrix([[ip(flp[i], flp[j]) for j in hom2] for i in hom2])
evp, vecp = mp.eigsy(Gp)
imin = min(range(len(hom2)), key=lambda i: evp[i])
lam = mp.matrix([vecp[i, imin] for i in range(len(hom2))])
lstar = mp.matrix([0, 1, 0, -1, 0, 0]) / mp.sqrt(2)
cosang = abs(sum(lam[i] * lstar[i] for i in range(len(hom2)))) / mp.norm(lam)
sinang = mp.sqrt(1 - cosang**2)
# delta = ||eps cos 3x||_{H^2} con la norma di CONV-T4 (somma su |alpha| <= 2 di ||d^alpha e||^2)
delta = eps * mp.sqrt(sum(ip(pert[k], pert[k]) for k in hom2))
print('    rho =', mp.nstr(rho, 6), ' delta =', mp.nstr(delta, 6), ' sin =', mp.nstr(sinang, 6),
      ' 2 delta/rho =', mp.nstr(2 * delta / rho, 6))
ok.append(('L10(c) CONV-T4(a): sin <= 2 delta/rho', sinang <= 2 * delta / rho))

# (c') caso non vacuo (ATTACK-9 O15): eps tale che 2 delta/rho < 1
def angolo(eps_):
    f_ = {k: (lambda k: (lambda a, b: fl[k](a, b) + eps_ * pert[k](a, b)))(k) for k in hom2}
    G_ = mp.matrix([[ip(f_[i], f_[j]) for j in hom2] for i in hom2])
    ev_, vec_ = mp.eigsy(G_)
    i_ = min(range(len(hom2)), key=lambda i: ev_[i])
    l_ = mp.matrix([vec_[i, i_] for i in range(len(hom2))])
    c_ = abs(sum(l_[i] * lstar[i] for i in range(len(hom2)))) / mp.norm(l_)
    return mp.sqrt(1 - c_**2), eps_ * mp.sqrt(sum(ip(pert[k], pert[k]) for k in hom2))
s2, d2 = angolo(mp.mpf('1e-4'))
print("    (c') eps = 1e-4: delta =", mp.nstr(d2, 6), ' sin =', mp.nstr(s2, 6), ' 2 delta/rho =', mp.nstr(2 * d2 / rho, 6))
ok.append(("L10(c') CONV-T4(a) non vacuo: 2 delta/rho < 1 e sin <= 2 delta/rho", 2 * d2 / rho < 1 and s2 <= 2 * d2 / rho))
# (a') r_1 come residuo diretto di minimi quadrati (ATTACK-9 O10), oltre al rapporto di Gram
G1 = gram(lev1); b1 = mp.matrix([ip(fl[i], fl['dt']) for i in lev1]); c1 = mp.lu_solve(G1, -b1)
res1 = lambda a, b: fl['dt'](a, b) + sum(c1[i] * fl[n](a, b) for i, n in enumerate(lev1))
r1ls = mp.sqrt(ip(res1, res1))
print("    (a') r_1 per residuo diretto =", mp.nstr(r1ls, 8))
ok.append(("L10(a') r_1 residuo diretto = r_1 Gram (rel. 1e-10)", abs(r1ls - r1) < 1e-10 * r1))

# (d) (H-ex): u = t + sin x, classe u_t = a u_xx + b u, a, b costanti
a, b = sp.symbols('a b')
ud = t + sp.sin(x)
Phi = a * sp.diff(ud, x, 2) + b * ud            # Phi_u(a, b)
ker = sp.solve([sp.expand(Phi).coeff(t), sp.expand(Phi).subs(t, 0).coeff(sp.sin(x))], [a, b], dict=True)
ok.append(('L10(d) ker Phi_u = 0 (ID-ker)', ker == [{a: 0, b: 0}]))
law = sp.expand(sp.diff(ud, t) - Phi)           # 1 - b t + (a - b) sin x
sol = sp.solve([law.subs({t: 0, x: 0}), law.coeff(t), law.subs(t, 0).coeff(sp.sin(x))], [a, b], dict=True)
ok.append(('L10(d) nessuna legge (H-ex falsa)', sol == []))

for name, val in ok:
    print('PASS' if val else 'FAIL', name)
print('%d/%d PASS' % (sum(1 for _, v in ok if v), len(ok)))
