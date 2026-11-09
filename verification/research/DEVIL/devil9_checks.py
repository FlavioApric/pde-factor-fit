"""DEVIL-9: controlli su ALGORITMO_ESTESO.md (verifica, non prova; numerica solo come controllo).
Eseguire con: D:\\ProblemaBase\\.venv\\Scripts\\python.exe -I research/DEVIL/sympy9/devil9_checks.py

(R) riesecuzione dei quattro script di S9-ALG (work/S9-ALG/sympy/ex_*.py): ogni script deve stampare N/N PASS.
(A) L6, controesempio a «dato EP: rango deficitario» (§3b, §9.1(c)): somma di 4 onde piane di Dirac 1+1
    (dato EP) -> rango 8 nella classe hamiltoniana i psi_t = A psi_x + B psi. ID-ker vale con dato EP.
(B) DM1 (EP) non da' mai ID-ann (§0.5, §3a «Senso», §8 punto 1): u = e^{-t} cos x risolve il calore ma
    Ann(u) contiene d_t + 1 e d_x^2 + 1, non multipli di tau - xi^2.
(C) DM2 (§1, §8 punto 3): per ogni N il getto d'ordine N in (0,0) della soluzione non EP G(t+1, x)
    coincide con quello di un polinomio del calore v_N (EP). Il maggiorante d = dim R.u esiste solo per u EP.
(D) L7 (§9.2): il dato di Poeschl-Teller ha l'annullatore (L_q + 1)(L_q - k^2) nel sottoanello C[d_t, L_q]:
    non identifica i d_t - L_q in senso ID-ann neanche prima della traduzione (vale solo ID-res).
(E) L9 (§9.4): dato a modi finiti con frequenze +-1, 2: soddisfa u_t = -|D| u e una legge locale
    u_t = a(d_x) u per interpolazione (l'indistinguibilita' e' banale per ogni dato a modi finiti).
(F) DM-delta senza norma (§0.3): u = 1 (V = 0), u_d = 1 + d^2 sin(x/d): ||u_d - u||_{C^1} <= d + d^2,
    ma sup |V_d| = 1/(1 + d^2) -> 1. VAR-P3 «non continuo da C^1»: il modello DM-delta deve dire la norma.
(G) L10 (§9.5): r_2 col rapporto di Gram (MF2) a 15 cifre contro 30 cifre; vacuita' di 2 delta/rho >= 1 in 9.5(c).
(H) C_W (§5): per q = Q costante T(1) = cosh(sqrt(Q) x); confronto cosh(a sqrt Q) <= C_W = 1 + a^2 Q e^{a sqrt Q}
    e ordine di grandezza di C_W^2 (fattore dei certificati trasportati).
"""
import os, re, subprocess, sys
import sympy as sp
import mpmath as mp

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
ok = []
def rep(name, val):
    ok.append((name, bool(val)))

t, x = sp.symbols('t x', real=True)

# ---------------- (R) riesecuzione
s9 = os.path.join(ROOT, 'work', 'S9-ALG', 'sympy')
cw_line = None
for f in ['ex_L6_dirac.py', 'ex_L7_poschl_teller.py', 'ex_L8_stark.py', 'ex_L9_L10_dict.py']:
    p = subprocess.run([sys.executable, '-I', os.path.join(s9, f)], capture_output=True, text=True,
                       cwd=s9, timeout=1800)
    last = [l for l in p.stdout.strip().splitlines() if l.strip()][-1] if p.stdout.strip() else 'nessuna uscita'
    m_ = re.match(r'(\d+)/(\d+) PASS', last)
    print('    (R)', f, '->', last)
    rep('(R) %s: tutti PASS' % f, m_ is not None and m_.group(1) == m_.group(2) and p.returncode == 0)
    if f == 'ex_L9_L10_dict.py':
        for l in p.stdout.splitlines():
            if '2 delta/rho =' in l:
                cw_line = l

# ---------------- (A) Dirac: dato EP a 4 modi
m = sp.Integer(1)
sx = sp.Matrix([[0, 1], [1, 0]]); sz = sp.Matrix([[1, 0], [0, -1]]); I2 = sp.eye(2)
a = sp.symbols('a0:4'); b = sp.symbols('b0:4')
A = sp.Matrix(2, 2, a); B = sp.Matrix(2, 2, b); unk = list(a) + list(b)
modes = [(sp.Rational(1, 2), 1), (sp.Integer(1), -1), (sp.Rational(3, 2), 1), (sp.Integer(2), -1)]
psi = sp.zeros(2, 1); rows = []
for k, sgn in modes:
    E = sgn * sp.sqrt(k**2 + m**2)
    v = sp.Matrix([k, E - m])
    rep('(A) v autovettore di H(k) = k sx + m sz con autovalore %s' % E,
        sp.simplify((k * sx + m * sz) * v - E * v) == sp.zeros(2, 1))
    psi += v * sp.exp(sp.I * (k * x - E * t))
    eq = (sp.I * k * A + B) * v - E * v          # condizione per modo (esponenziali indipendenti)
    rows += [[sp.diff(e, u_) for u_ in unk] for e in eq]
Hop = lambda w: -sp.I * sx * sp.diff(w, x) + m * sz * w
rep('(A) psi (4 onde piane, EP) risolve Dirac', sp.simplify(sp.I * sp.diff(psi, t) - Hop(psi)) == sp.zeros(2, 1))
Mmode = sp.Matrix(rows)
rk = Mmode.rank(simplify=True)
print('    (A) rango esatto (per modi) =', rk)
rep('(A) dato EP a 4 modi: rango 8 nella classe hamiltoniana (ID-ker con dato EP)', rk == 8)
# stesso test col metodo di S9-ALG (sistema puntuale su punti campione)
pts = [(sp.Rational(23, 10), sp.Rational(7, 10)), (sp.Rational(31, 10), -sp.Rational(6, 5)),
       (sp.Rational(17, 10), sp.Rational(2, 5)), (sp.Integer(4), sp.Rational(5, 2)),
       (sp.Rational(1, 3), sp.Rational(-1, 7))]
eqs = sp.I * sp.diff(psi, t) - A * sp.diff(psi, x) - B * psi
Mp = sp.Matrix([[sp.diff(e, u_).subs({t: p0, x: p1}) for u_ in unk] for p0, p1 in pts for e in eqs])
Mn = mp.matrix([[complex(sp.N(Mp[i, j], 30)) for j in range(8)] for i in range(Mp.rows)])
sv = sorted(float(abs(s_)) for s_ in mp.svd_c(Mn, compute_uv=False))
print('    (A) valori singolari puntuali:', ['%.3e' % s_ for s_ in sv])
rep('(A) rango puntuale 8 (sigma_min > 1e-6)', sv[0] > 1e-6)
true = {a[0]: 0, a[1]: -sp.I, a[2]: -sp.I, a[3]: 0, b[0]: 1, b[1]: 0, b[2]: 0, b[3]: -1}
# il sistema non omogeneo (con -E v) ha soluzione unica = legge vera
inh = []
for k, sgn in modes:
    E = sgn * sp.sqrt(k**2 + m**2); v = sp.Matrix([k, E - m])
    inh += list((sp.I * k * A + B) * v - E * v)
s_inh = sp.solve(inh, unk, dict=True)
rep('(A) soluzione unica = (A, B) = (-i sx, m sz)', len(s_inh) == 1 and
    all(sp.simplify(s_inh[0][u_] - true[u_]) == 0 for u_ in unk))

# ---------------- (B) DM1: EP non identifica
uB = sp.exp(-t) * sp.cos(x)
rep('(B) e^{-t} cos x risolve il calore', sp.simplify(sp.diff(uB, t) - sp.diff(uB, x, 2)) == 0)
rep('(B) (d_t + 1) u = 0 e (d_x^2 + 1) u = 0: Ann(u) != (tau - xi^2)',
    sp.simplify(sp.diff(uB, t) + uB) == 0 and sp.simplify(sp.diff(uB, x, 2) + uB) == 0)
tau, xi = sp.symbols('tau xi')
rep('(B) tau + 1 non e\' multiplo di tau - xi^2', sp.rem(sp.Poly(tau + 1, tau, xi), sp.Poly(tau - xi**2, tau, xi)) != 0)

# ---------------- (C) DM2: getti di un dato non EP riprodotti da dati EP
G = (t + 1)**sp.Rational(-1, 2) * sp.exp(-x**2 / (4 * (t + 1)))
allC = True
for N in (2, 4, 6):
    c = [sp.diff(G, x, n).subs({t: 0, x: 0}) / sp.factorial(n) for n in range(2 * N + 1)]
    p0 = sum(c[n] * x**n for n in range(2 * N + 1))
    v = sum(t**kk / sp.factorial(kk) * sp.diff(p0, x, 2 * kk) for kk in range(N + 1))
    heat_ok = sp.expand(sp.diff(v, t) - sp.diff(v, x, 2)) == 0
    jet_ok = all(sp.simplify(sp.diff(G, t, aa, x, bb).subs({t: 0, x: 0}) - sp.diff(v, t, aa, x, bb).subs({t: 0, x: 0})) == 0
                 for aa in range(N + 1) for bb in range(N + 1 - aa))
    ep_ok = sp.diff(v, x, 2 * N + 1) == 0      # v polinomio: d_x^{2N+1} v = 0, Ann(v) != (tau - xi^2)
    allC = allC and heat_ok and jet_ok and ep_ok
    print('    (C) N = %d: v_N calore %s, getto d\'ordine N uguale %s, d_x^{2N+1} v = 0 %s' % (N, heat_ok, jet_ok, ep_ok))
rep('(C) per N = 2, 4, 6 il getto d\'ordine N di G(t+1,x) coincide con quello di un polinomio del calore (EP)', allC)

# ---------------- (D) Poeschl-Teller nel sottoanello C[d_t, L_q]
k = sp.Rational(3, 2); q = -2 * sp.sech(x)**2
Lq = lambda f: -sp.diff(f, x, 2) + q * f
def z(e):
    e = sp.together(sp.expand(e.rewrite(sp.exp)))
    return sp.simplify(sp.expand(sp.numer(e))) == 0
u_b = sp.exp(sp.I * t) * sp.sech(x)
u_s = sp.exp(-sp.I * k**2 * t) * (sp.I * k - sp.tanh(x)) * sp.exp(sp.I * k * x)
uD = u_b + u_s
w = Lq(uD) + uD
rep('(D) (L_q + 1)(L_q - k^2) u = 0 (annullatore senza d_t)', z(Lq(w) - k**2 * w))
rep('(D) (i d_t + 1)(i d_t - k^2) u = 0 (annullatore senza x)',
    z((lambda f: sp.I * sp.diff(f, t) - k**2 * f)(sp.I * sp.diff(uD, t) + uD)))

# ---------------- (E) L9: interpolazione locale
uE = sp.exp(-t) * (sp.exp(sp.I * x) + sp.exp(-sp.I * x)) + sp.exp(-2 * t) * sp.exp(2 * sp.I * x)
absD = sp.exp(-t) * (sp.exp(sp.I * x) + sp.exp(-sp.I * x)) + 2 * sp.exp(-2 * t) * sp.exp(2 * sp.I * x)
c0, c1, c2 = sp.symbols('c0 c1 c2')
aa_ = lambda s: c0 + c1 * s + c2 * s**2
cs = sp.solve([aa_(sp.I * kk) + abs(kk) for kk in (1, -1, 2)], [c0, c1, c2], dict=True)[0]
loc = cs[c0] * uE + cs[c1] * sp.diff(uE, x) + cs[c2] * sp.diff(uE, x, 2)
print('    (E) legge locale interpolante: u_t = (%s) + (%s) d_x + (%s) d_x^2' % (cs[c0], cs[c1], cs[c2]))
rep('(E) u_t = -|D| u', sp.simplify(sp.diff(uE, t) + absD) == 0)
rep('(E) u_t = a(d_x) u con a polinomio di grado 2 (interpolazione)', sp.simplify(sp.diff(uE, t) - loc) == 0)

# ---------------- (F) DM-delta: dipendenza dalla norma
d = sp.symbols('delta', positive=True)
ud = 1 + d**2 * sp.sin(x / d)
Vd = sp.diff(ud, x, 2) / ud
c1norm = d**2 + d                       # sup|u_d - u| + sup|(u_d - u)_x|
Vpeak = sp.simplify(Vd.subs(x, -d * sp.pi / 2))
print('    (F) ||u_d - u||_C1 <=', c1norm, ';  |V_d(-d pi/2)| =', Vpeak)
rep('(F) d = 1e-3: ||u_d - u||_C1 < 2e-3 ma |V_d| > 0.99 (V = 0)',
    float(c1norm.subs(d, sp.Rational(1, 1000))) < 2e-3 and float(abs(Vpeak.subs(d, sp.Rational(1, 1000)))) > 0.99)

# ---------------- (G) L10: precisione del rapporto di Gram e vacuita' di 2 delta/rho
uG = (t + 1)**sp.Rational(-1, 2) * sp.exp(-x**2 / (4 * (t + 1)))
atoms = {'1': uG, 'dx': sp.diff(uG, x), 'dxx': sp.diff(uG, x, 2), 'dtdx': sp.diff(uG, t, x),
         'dtt': sp.diff(uG, t, 2), 'dt': sp.diff(uG, t)}
fl = {kk: sp.lambdify((t, x), vv, 'mpmath') for kk, vv in atoms.items()}
lev2 = ['1', 'dx', 'dxx', 'dtdx', 'dtt']
def r2_both(dps):
    mp.mp.dps = dps
    ip = lambda f, g: mp.quad(lambda s, y: f(s, y) * g(s, y), [0, 1], [-1, 1])
    gm = lambda nm: mp.matrix([[ip(fl[i], fl[j]) for j in nm] for i in nm])
    try:                                   # MF2: r_2^2 = det G(D_0, D...)/det G(D...)
        ratio = mp.det(gm(['dt'] + lev2)) / mp.det(gm(lev2))
    except Exception as e_:
        ratio = 'non calcolabile (%s)' % type(e_).__name__
    G2 = gm(lev2); b2 = mp.matrix([ip(fl[i], fl['dt']) for i in lev2])
    c2 = mp.lu_solve(G2, -b2)              # minimi quadrati via equazioni normali (come S9-ALG)
    res = lambda s, y: fl['dt'](s, y) + sum(c2[i] * fl[n](s, y) for i, n in enumerate(lev2))
    return ratio, mp.sqrt(ip(res, res))
rat15, r15 = r2_both(15); rat30, r30 = r2_both(30)
print('    (G) MF2 (rapporto di Gram) a 15 cifre:', rat15 if isinstance(rat15, str) else mp.nstr(rat15, 5),
      '; a 30 cifre:', rat30 if isinstance(rat30, str) else mp.nstr(rat30, 5))
print('    (G) r_2 (equazioni normali + quadratura) a 15 cifre =', mp.nstr(r15, 5), '; a 30 cifre =', mp.nstr(r30, 5))
rep('(G) a 15 cifre r_2 < 1e-12: il misfit per minimi quadrati è stabile (ipotesi di DEVIL-9 smentita)', r15 < 1e-12)
rep('(G) MF2 come rapporto di determinanti di Gram non calcolabile in mpmath a 15 e 30 cifre', isinstance(rat15, str) and isinstance(rat30, str))
rep('(G) a 30 cifre r_2 < 1e-20', r30 < 1e-20)
mp.mp.dps = 15
if cw_line:
    val = float(re.search(r'2 delta/rho =\s*([0-9.eE+-]+)', cw_line).group(1))
    print('    (G) 9.5(c): 2 delta/rho =', val)
    rep('(G) 9.5(c): 2 delta/rho >= 1, il bound CONV-T4(a) e\' vacuo (sin <= 1 sempre)', val >= 1)

# ---------------- (H) C_W
allH = True
for s_ in (0.5, 1, 3, 5):
    T1 = mp.cosh(s_); CW = 1 + s_**2 * mp.e**s_
    allH = allH and T1 <= CW
    print('    (H) a sqrt(Q) = %.1f: ||T 1||_inf = cosh = %.4g <= C_W = %.4g; C_W^2 = %.3g, cosh^2 = %.3g'
          % (s_, T1, CW, CW**2, T1**2))
rep('(H) cosh(a sqrt Q) <= C_W per a sqrt Q in {0.5, 1, 3, 5} (nessun controesempio al bound)', allH)

for name, val in ok:
    print('PASS' if val else 'FAIL', name)
print('%d/%d PASS' % (sum(v for _, v in ok), len(ok)))
