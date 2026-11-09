"""S10-INT, EX10-b: Schroedinger armonico, normalizzazione unica H = -d^2 + x^2 (NOTAZIONE v6).
Equazione: i u_t = -u_xx + x^2 u. Verifica V-ex, non una prova.
(1) stato coerente u_c = exp(-x^2/2 + sqrt2 al x - al^2/2 - i t), al(t) = al0 e^{-2it}:
    residuo, rho_u = x^2 (ID-res), DM-phi (ID-fam), vacuita' in K = C(x, e^{2it}),
    non D-finitezza (d_x^b u / u ha grado b in al) => ID-ann in A_2 per VAR-C3Q2(c).
(2) combinazione di Hermite-Gauss u_h = e^{-x^2/2}(e^{-it} + 2x e^{-3it}): zeri isolati,
    rho_u = x^2 (ID-res), D-finita => non ID-ann in A_2 ((H-1)(H-3) la annulla).
(3) VAR-T10(3): U(t) = c e^{i g x^2} e^{i s d^2} e^{i g x^2}, g = (cos2t - 1)/(2 sin2t), s = sin(2t)/2;
    g = -tan(t)/2 esplode a cos t = 0; la parola risolve l'equazione su Gaussiane generiche;
    U(pi/2) = -i * parita' sulla base di Hermite (M = -I: la parola a tre fattori non esiste).
"""
import sympy as sp

t, x = sp.symbols('t x', real=True)
al0 = sp.symbols('alpha0')
ok = []
def schr(u):
    return sp.I * sp.diff(u, t) + sp.diff(u, x, 2) - x**2 * u

# (1) stato coerente
al = al0 * sp.exp(-2 * sp.I * t)
uc = sp.exp(-x**2 / 2 + sp.sqrt(2) * al * x - al**2 / 2 - sp.I * t)
ok.append(('(1) lo stato coerente risolve i u_t = -u_xx + x^2 u', sp.simplify(schr(uc) / uc) == 0))
rho = sp.simplify((sp.I * sp.diff(uc, t) + sp.diff(uc, x, 2)) / uc)
ok.append(('(1) rho_u = (i u_t + u_xx)/u = x^2  (ID-res; u senza zeri)', sp.simplify(rho - x**2) == 0))
phi = sp.Function('phi')(t)
up = sp.exp(sp.I * phi) * uc
rho_phi = sp.simplify((sp.I * sp.diff(up, t) + sp.diff(up, x, 2)) / up)
ok.append(('(1) DM-phi: rho = x^2 - phi\'(t)  (solo ID-fam, V modulo c(t))',
           sp.simplify(rho_phi - (x**2 - sp.diff(phi, t))) == 0))
ok.append(('(1) vacuita\' (VAR-N1): (d_x + x - sqrt2 al) u = 0, coefficienti in C(x, e^{2it})',
           sp.simplify(sp.diff(uc, x) + (x - sp.sqrt(2) * al) * uc) == 0))
A_ = sp.symbols('A')
degs = []
for bb in range(0, 6):
    q = sp.simplify(sp.diff(uc, x, bb) / uc)
    q = sp.expand(q.subs(al0, A_ * sp.exp(2 * sp.I * t)))
    degs.append(sp.Poly(q, A_).degree())
print('    grado in alpha di d_x^b u / u, b = 0..5:', degs)
ok.append(('(1) d_x^b u/u ha grado esatto b in alpha (alpha trascendente su C(t,x) => u non D-finita)',
           degs == list(range(6))))

# (2) Hermite-Gauss
uh = sp.exp(-x**2 / 2) * (sp.exp(-sp.I * t) + 2 * x * sp.exp(-3 * sp.I * t))
ok.append(('(2) u_h risolve l\'equazione', sp.simplify(schr(uh)) == 0))
rho_h = sp.simplify((sp.I * sp.diff(uh, t) + sp.diff(uh, x, 2)) / uh)
ok.append(('(2) rho_u = x^2 su {u != 0}  (ID-res)', sp.simplify(rho_h - x**2) == 0))
ok.append(('(2) zeri: u_h(0, -1/2) = 0 e u_h(pi/2, 1/2) = 0',
           sp.simplify(uh.subs({t: 0, x: -sp.Rational(1, 2)})) == 0 and
           sp.simplify(uh.subs({t: sp.pi / 2, x: sp.Rational(1, 2)})) == 0))
xr = sp.symbols('xr', real=True)
fac = sp.expand(sp.simplify(uh.subs(t, sp.pi / 4) * sp.exp(x**2 / 2) * sp.exp(sp.I * sp.pi / 4)))
ok.append(('(2) a t = pi/4 nessuno zero reale (fattore 1 - 2 i x)',
           sp.simplify(fac - (1 - 2 * sp.I * x)) == 0))
Hx = lambda f: -sp.diff(f, x, 2) + x**2 * f
ok.append(('(2) (H - 1)(H - 3) u_h = 0: R in B = C[t,x]<d_x>, quindi Ann(u_h) != A_2 L (non ID-ann)',
           sp.simplify(Hx(Hx(uh) - 3 * uh) - (Hx(uh) - 3 * uh)) == 0))

# (3) parola chirp . libero . chirp
g = (sp.cos(2 * t) - 1) / (2 * sp.sin(2 * t))
s = sp.sin(2 * t) / 2
ok.append(('(3) g = -tan(t)/2', sp.simplify(g + sp.tan(t) / 2) == 0))
ok.append(('(3) 1/g -> 0 per t -> pi/2 (la parola si rompe a cos t = 0)',
           sp.limit(1 / g.rewrite(sp.tan), t, sp.pi / 2) == 0))
ok.append(('(3) s(pi/2) = 0 e M(pi/2) = -I', s.subs(t, sp.pi / 2) == 0 and
           sp.Matrix([[sp.cos(2 * t), sp.sin(2 * t)], [-sp.sin(2 * t), sp.cos(2 * t)]]).subs(t, sp.pi / 2) == -sp.eye(2)))
bq, cq = sp.symbols('b c')
gg = -sp.tan(t) / 2
a0 = -bq + sp.I * gg                       # dopo il primo chirp: exp(a0 x^2 + c x)
den = 1 - 4 * sp.I * a0 * s                # flusso libero phi_s = i phi_xx sulla Gaussiana
a1 = a0 / den; b1 = cq / den
Acoef = sp.simplify(a1 + sp.I * gg); Bcoef = sp.simplify(b1)
r2 = sp.simplify(sp.I * sp.diff(Acoef, t) + 4 * Acoef**2 - 1)
r1 = sp.simplify(sp.I * sp.diff(Bcoef, t) + 4 * Acoef * Bcoef)
ok.append(('(3) parola su exp(-b x^2 + c x): coefficiente di x^2 del residuo = 0', r2 == 0))
ok.append(('(3) parola su exp(-b x^2 + c x): coefficiente di x del residuo = 0', r1 == 0))
ok.append(('(3) parola -> identita\' per t -> 0', sp.limit(Acoef, t, 0) == -bq and sp.limit(Bcoef, t, 0) == cq))
# flusso libero: verifica dell'ansatz Gaussiano
ss, al_, be_ = sp.symbols('s alpha beta')
ph = sp.exp(al_ / (1 - 4 * sp.I * al_ * ss) * x**2 + be_ / (1 - 4 * sp.I * al_ * ss) * x
            + sp.I * be_**2 * ss / (1 - 4 * sp.I * al_ * ss)) / sp.sqrt(1 - 4 * sp.I * al_ * ss)
ok.append(('(3) ansatz Gaussiano risolve phi_s = i phi_xx', sp.simplify((sp.diff(ph, ss) - sp.I * sp.diff(ph, x, 2)) / ph) == 0))
# U(pi/2) = -i * parita' sulla base di Hermite
hs = [sp.hermite(n, x) * sp.exp(-x**2 / 2) for n in range(6)]
ok.append(('(3) e^{-i(2n+1)pi/2} h_n(x) = -i h_n(-x), n = 0..5',
           all(sp.simplify(sp.exp(-sp.I * (2 * n + 1) * sp.pi / 2) * h + sp.I * h.subs(x, -x)) == 0
               for n, h in enumerate(hs))))
ok.append(('(3) h_n autofunzioni di H con autovalore 2n+1', all(sp.simplify(Hx(h) - (2 * n + 1) * h) == 0 for n, h in enumerate(hs))))

ok = [(n_, bool(v_)) for n_, v_ in ok]
for name, val in ok:
    print('PASS' if val else 'FAIL', name)
print('%d/%d PASS' % (sum(v for _, v in ok), len(ok)))
