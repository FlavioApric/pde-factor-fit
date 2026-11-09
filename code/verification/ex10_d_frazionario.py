"""S10-INT, EX10-d: calore frazionario u_t + (-d_x^2)^s u = 0, 0 < s < 1, su modi di Fourier.
Verifica V-ex, non una prova. Simbolo: e^{-|k|^{2s} t + ikx}; d_t -> -|k|^{2s}, d_x -> ik.
(1) s = 1/4, modi k = 1, 2, 3 (dato DM1): livello locale u_t = a(d_x)u con deg a = 1: MISFIT esatto;
    deg a = 2: legge locale unica (interpolazione dei simboli), che NON e' la legge frazionaria.
(2) classe parametrica FRAC {u_t = -c |D|^{2 sigma} u}: (c, sigma) = (1, 1/4) unici; nell'unione
    LIN_2 u FRAC due leggi esatte => nessuna unicita'.
(3) s razionale: la legge locale sollevata (-d_t)^4 = -d_x^2 (s = 1/4) annulla ogni modo.
(4) s = 1/2, dato di Poisson u = T/(T^2 + x^2), T = t + 1 (M3-hol): u_hat = pi e^{-T|kappa|}
    (u_t = -|D|u), Delta u = 0, test C3-T1 per Ann(u) = (d_t^2 + d_x^2); nessuna legge u_t = a(d_x)u
    con deg a <= 4.
"""
import sympy as sp
import mpmath as mp

t, x = sp.symbols('t x', real=True)
ok = []
s = sp.Rational(1, 4)
ks = [1, 2, 3]
lam = {kk: sp.Integer(kk)**(2 * s) for kk in ks}
u = sum(sp.exp(-lam[kk] * t + sp.I * kk * x) for kk in ks)

def local_law(deg, kset):
    c = sp.symbols('c0:%d' % (deg + 1))
    eqs = [sum(c[j] * (sp.I * kk)**j for j in range(deg + 1)) + lam[kk] for kk in kset]
    return c, sp.linsolve(eqs, c)
c1, sol1 = local_law(1, ks)
ok.append(('(1) livello deg a = 1: sistema incompatibile (MISFIT esatto)', sol1 == sp.EmptySet))
c2, sol2 = local_law(2, ks)
sol2 = list(sol2)
ok.append(('(1) livello deg a = 2: soluzione unica', len(sol2) == 1 and all(not e.free_symbols for e in sol2[0])))
coef = sol2[0]
a_op = lambda g: sum(coef[j] * sp.diff(g, x, j) for j in range(3))
ok.append(('(1) la legge locale u_t = a(d_x)u annulla il dato', sp.simplify(sp.diff(u, t) - a_op(u)) == 0))
u4 = sp.exp(-sp.Integer(4)**(2 * s) * t + 4 * sp.I * x)
ok.append(('(1) ... ma non il modo k = 4 della legge frazionaria: non e\' (-D^2)^s',
           sp.simplify(sp.diff(u4, t) - a_op(u4)) != 0))
print('    coefficienti della legge locale (deg 2):', [sp.nsimplify(e) for e in coef])

# (2) classe FRAC: rate lambda_k = c k^{2 sigma}
cc, sg = sp.symbols('c sigma', positive=True)
solF = sp.solve([cc * 1 - lam[1], cc * 2**(2 * sg) - lam[2]], [cc, sg], dict=True)
ok.append(('(2) FRAC: (c, sigma) = (1, 1/4) unica', len(solF) == 1 and solF[0][cc] == 1 and sp.simplify(solF[0][sg] - s) == 0))
ok.append(('(2) FRAC: il terzo modo e\' coerente (H-ex nella classe FRAC)', sp.simplify(3**(2 * s) - lam[3]) == 0))
ok.append(('(2) unione LIN_2 u FRAC: due leggi distinte entrambe esatte (nessuna unicita\')',
           sp.simplify(sp.diff(u, t) - a_op(u)) == 0 and
           all(sp.simplify(-lam[kk] + sp.Integer(kk)**(2 * s)) == 0 for kk in ks)))

# (3) legge sollevata per s = 1/4: (-d_t)^4 u = -d_x^2 u, per ogni insieme di modi (anche k < 0)
modes = [sp.exp(-sp.Abs(kk)**sp.Rational(1, 2) * t + sp.I * kk * x) for kk in (-3, -1, 1, 2, 5, 7)]
ok.append(('(3) d_t^4 u + d_x^2 u = 0 su ogni modo, k = -3, -1, 1, 2, 5, 7',
           all(sp.simplify(sp.diff(mm, t, 4) + sp.diff(mm, x, 2)) == 0 for mm in modes)))
tau, xi = sp.symbols('tau xi')
fl = sp.factor_list(tau**4 + xi**2, extension=sp.I)
ok.append(('(3) tau^4 + xi^2 = (tau^2 + i xi)(tau^2 - i xi): due fattori', len(fl[1]) == 2))

# (4) s = 1/2: nucleo di Poisson
T = t + 1
up = T / (T**2 + x**2)
ok.append(('(4) Delta u = u_tt + u_xx = 0', sp.simplify(sp.diff(up, t, 2) + sp.diff(up, x, 2)) == 0))
mp.mp.dps = 30
def ft(tt, kap):
    Tn = tt + 1
    # integrando pari: 2 * integrale oscillante su (0, inf)
    return 2 * mp.quadosc(lambda y: Tn / (Tn**2 + y**2) * mp.cos(kap * y), [0, mp.inf], omega=kap)
errs = []
for tt, kap in [(0, 0.5), (0.5, 1.0), (1.0, 2.0), (0.25, 3.0)]:
    errs.append(abs(ft(tt, kap) - mp.pi * mp.e**(-(tt + 1) * abs(kap))))
print('    errore |u_hat - pi e^{-T|k|}|:', ['%.1e' % float(e) for e in errs])
ok.append(('(4) u_hat(t, kappa) = pi e^{-(t+1)|kappa|} (quadratura, < 1e-15): u_t = -|D| u', max(errs) < 1e-15))
gm = sp.simplify((sp.diff(up, t) - sp.I * sp.diff(up, x)) * (x - sp.I * T)**2)
gp = sp.simplify((sp.diff(up, t) + sp.I * sp.diff(up, x)) * (x + sp.I * T)**2)
ok.append(('(4) (d_t -+ i d_x) u = cost./(x -+ iT)^2 (poli: non EP) => test C3-T1 superato',
           gm.free_symbols == set() and gp.free_symbols == set() and gm != 0 and gp != 0))
nolaw = True
for deg in range(1, 5):
    a = sp.symbols('a0:%d' % (deg + 1))
    res = sp.diff(up, t) - sum(a[j] * sp.diff(up, x, j) for j in range(deg + 1))
    num = sp.numer(sp.together(res))
    eqs = sp.Poly(sp.expand(num), t, x).coeffs()
    if sp.linsolve(eqs, a) != sp.EmptySet:
        nolaw = False
ok.append(('(4) nessuna legge u_t = a(d_x)u con deg a <= 4 (MISFIT al primo ordine in tau)', nolaw))

ok = [(n_, bool(v_)) for n_, v_ in ok]
for name, val in ok:
    print('PASS' if val else 'FAIL', name)
print('%d/%d PASS' % (sum(v for _, v in ok), len(ok)))
