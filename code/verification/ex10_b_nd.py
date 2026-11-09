# S-CHECK-EX10 -- controllo indipendente di EX10-b-ND
# u_c = exp(-x^2/2 + sqrt2 a x - a^2/2 - i t), a = a0 e^{-2it}, a0 != 0
# Tesi: u_c non D-finita su C(t,x); quindi (VAR-C3Q2(c)) Ann_{A_2}(u_c) = A_2 (i d_t + d_x^2 - x^2).
import sympy as sp
import mpmath as mp
import random

t, x = sp.symbols('t x', real=True)
a0, al, E = sp.symbols('a0 alpha E')          # E sta per e^{-2it}
ok = []

alpha_t = a0 * sp.exp(-2 * sp.I * t)
u = sp.exp(-x**2 / 2 + sp.sqrt(2) * alpha_t * x - alpha_t**2 / 2 - sp.I * t)

# (1) u risolve (i d_t + d_x^2 - x^2) u = 0
res = sp.I * sp.diff(u, t) + sp.diff(u, x, 2) - x**2 * u
ok.append(('(1) (i d_t + d_x^2 - x^2) u_c = 0', sp.simplify(res / u) == 0))

# (2) forma monica: -i L = d_t - M con M = i d_x^2 - i x^2 in B
f = sp.Function('f')(t, x)
Lf = sp.I * sp.diff(f, t) + sp.diff(f, x, 2) - x**2 * f
Mf = sp.I * sp.diff(f, x, 2) - sp.I * x**2 * f
ok.append(('(2) -i L = d_t - M, M = i d_x^2 - i x^2 in B = C[t,x]<d_x> (monico, m = 1)',
           sp.expand(-sp.I * Lf - (sp.diff(f, t) - Mf)) == 0))

# (3) d_x^b u / u = p_b(x, alpha), grado esatto b in alpha, coefficiente di testa sqrt2^b (costante)
ua = sp.exp(-x**2 / 2 + sp.sqrt(2) * al * x - al**2 / 2 - sp.I * t)   # alpha come simbolo (d_x non tocca alpha)
degs, lcs, polys = [], [], []
for b in range(0, 9):
    p = sp.expand(sp.simplify(sp.diff(ua, x, b) / ua))
    P = sp.Poly(p, al)
    degs.append(P.degree()); lcs.append(sp.simplify(P.LC() - sp.sqrt(2)**b) == 0)
    polys.append(p)
print('    gradi in alpha, b = 0..8:', degs)
ok.append(('(3) deg_alpha(d_x^b u/u) = b, coeff. di testa sqrt2^b, b = 0..8',
           degs == list(range(9)) and all(lcs)))

# (3') passo induttivo simbolico: p di grado b con testa c => (p_x + p(-x + sqrt2 alpha)) ha grado b+1, testa sqrt2 c
bb = 4
cs = sp.symbols('c0:%d' % (bb + 1))
qs = [sp.Function('q%d' % j)(x) for j in range(bb)]
p = cs[bb] * al**bb + sum(qs[j] * al**j for j in range(bb))
step = sp.expand(sp.diff(p, x) + p * (-x + sp.sqrt(2) * al))
P = sp.Poly(step, al)
ok.append(('(3\') passo induttivo: testa c costante => grado b+1, testa sqrt2 c (b = 4, parte bassa generica)',
           P.degree() == bb + 1 and sp.simplify(P.LC() - sp.sqrt(2) * cs[bb]) == 0))

# (4) nessuna R in B (ord <= d, coeff. polinomiali in t,x di grado <= N) annulla u.
# R u / u = sum_b r_b(t,x) p_b(x, a0 E); E trattata come indeterminata (trascendenza di e^{-2it} su C(t,x)).
d, N = 4, 3
mons = [t**i * x**j for i in range(N + 1) for j in range(N + 1 - i)]
unk = []
expr = 0
for b in range(d + 1):
    for m in mons:
        c = sp.Symbol('r_%d_%d' % (b, len(unk))); unk.append(c)
        expr += c * m * polys[b].subs(al, a0 * E)
expr = sp.expand(expr.subs(a0, sp.Rational(3, 2)))
eqs = sp.Poly(expr, t, x, E).coeffs()
sol = sp.linsolve(eqs, unk)
ok.append(('(4) R in B, ord <= 4, deg coeff <= 3, R u = 0 (E indeterminata) => R = 0 (%d incognite)' % len(unk),
           sol == sp.FiniteSet(tuple([0] * len(unk)))))

# (4') senza usare la trascendenza: rango numerico della matrice dei valori t^i x^j d_x^b u nei punti di campionamento
mp.mp.dps = 40
a0n = mp.mpf(3) / 2
pfun = [sp.lambdify((t, x, sp.Symbol('AL')), polys[b].subs(al, sp.Symbol('AL')), 'mpmath') for b in range(d + 1)]
random.seed(7)
pts = [(mp.mpf(random.uniform(-1, 1)), mp.mpf(random.uniform(-1, 1))) for _ in range(len(unk) + 20)]
rows = []
for (tt, xx) in pts:
    AL = a0n * mp.e**(-2j * tt)
    U = mp.e**(-xx**2 / 2 + mp.sqrt(2) * AL * xx - AL**2 / 2 - 1j * tt)
    row = []
    for b in range(d + 1):
        pb = pfun[b](tt, xx, AL)
        for (i, j) in [(i, j) for i in range(N + 1) for j in range(N + 1 - i)]:
            row.append(tt**i * xx**j * pb * U)
    rows.append(row)
Mnum = mp.matrix(rows)
sv = mp.svd_c(Mnum, compute_uv=False)
svl = sorted([abs(s) for s in sv])
print('    sigma_min / sigma_max (valori numerici):', mp.nstr(svl[0], 5), '/', mp.nstr(svl[-1], 5))
ok.append(('(4\') rango numerico pieno della matrice dei valori (sigma_min/sigma_max > 1e-25)',
           svl[0] / svl[-1] > mp.mpf('1e-25')))

# (5) kill: a0 = 0 => u D-finita, (d_x + x) u = 0 in B: l'ipotesi a0 != 0 serve
u0 = u.subs(a0, 0)
ok.append(('(5) kill: a0 = 0 => (d_x + x) u = 0, R in B: ipotesi a0 != 0 necessaria',
           sp.simplify(sp.diff(u0, x) + x * u0) == 0))

# (6) kill: nel campo C(x, e^{2it}) l'annullatore d'ordine 1 esiste (l'anello conta)
ok.append(('(6) (d_x + x - sqrt2 alpha(t)) u = 0: coefficiente fuori da C[t,x], non in B',
           sp.simplify(sp.diff(u, x) + (x - sp.sqrt(2) * alpha_t) * u) == 0))

# (7) kill: un operatore misto con d_t si riduce (VAR-C3Q2(a)) a resto in B; controllo su Q = d_t d_x:
# Q = d_x * (d_t - M) + d_x M  =>  Q u = (d_x M) u, e (d_x M) u != 0
Qu = sp.diff(u, t, x)
DMu = sp.diff(sp.I * sp.diff(u, x, 2) - sp.I * x**2 * u, x)
ok.append(('(7) divisione: d_t d_x u = (d_x o M) u e il resto d_x o M non annulla u',
           sp.simplify((Qu - DMu) / u) == 0 and sp.simplify(DMu / u) != 0))

for name, v in ok:
    print('PASS' if v else 'FAIL', name)
print('%d/%d PASS' % (sum(1 for _, v in ok if v), len(ok)))
