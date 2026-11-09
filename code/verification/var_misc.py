# S-CHECK-F8-VAR (27/10/2026) - controlli indipendenti su VAR-E1, VAR-VMPUM, VAR-P3, VAR-P5(c),
# VAR-P9(d), VAR-T10(3)(ii), portata L^infinito di VAR-T1(b), VAR-E2, stima di Cauchy (Tychonoff).
import sympy as sp
import numpy as np
import mpmath as mp

x, t, E = sp.symbols('x t E')
ok = True
def chk(name, cond):
    global ok
    ok &= bool(cond)
    print(("OK   " if cond else "FAIL ") + name)

# (1) VAR-E1: il passo "ai poli di w, w'+w^2 ha un polo" e' falso: w = 1/x ha w'+w^2 = 0.
w = 1/x
chk("E1: w=1/x  =>  w'+w^2 = 0 (polo semplice di residuo 1 cancellato)", sp.simplify(sp.diff(w, x) + w**2) == 0)
# argomento corretto: w = P + sum 1/(x-a_j); all'infinito w'+w^2 ~ P^2 (deg 2d) oppure limitato (d=0): mai = x
c0, c1, N = sp.symbols('c0 c1 N')
wd0 = c0 + N/x            # d = 0: sviluppo all'infinito
lead = sp.limit((sp.diff(wd0, x) + wd0**2)/x, x, sp.oo)
chk("E1: con d=0, (w'+w^2)/x -> 0 all'infinito (non puo' essere x)", lead == 0)

# (2) VAR-VMPUM delta (3): un segnale EP con due esponenziali non e' iperesponenziale
u = sp.exp(x) + sp.exp(2*x)
r = sp.simplify(sp.diff(u, x)/u)
y = sp.symbols('y')
r_y = sp.simplify(r.subs(sp.exp(x), y))
chk("VMPUM: u'/u = (1+2e^x)/(1+e^x) dipende da e^x (non in C(x))", sp.diff(r_y, y) != 0)
# u, u' indipendenti su C(x): det Wronskiano di (e^x, e^{2x}) non nullo e L_u = (d-1)(d-2) di ordine 2
L = sp.diff(u, x, 2) - 3*sp.diff(u, x) + 2*u
chk("VMPUM: (d-1)(d-2) uccide u, ordine minimo 2", sp.simplify(L) == 0)

# (3) VAR-P3: nitidezza dell'esponente 1/3 per la STIMA DI STABILITA' (non solo per l'interpolazione)
# famiglia (b): u1 = e^{-iEt}, V1 = E; u2 = e^{-iEt}(1 + a sin kx), V2 = E - a k^2 sin kx/(1 + a sin kx)
for (aa, kk) in [(1e-3, 10.0), (1e-5, 40.0), (1e-7, 100.0)]:
    xs = np.linspace(0, 2*np.pi, 200001)
    dV = np.max(np.abs(aa*kk**2*np.sin(kk*xs)/(1 + aa*np.sin(kk*xs))))
    e, M = aa, aa*kk**3
    print(f"   P3: a={aa:g}, k={kk:g}: ||V1-V2|| / (||e||^(1/3) ||e_xxx||^(2/3)) = {dV/(e**(1/3)*M**(2/3)):.6f}")
chk("P3: rapporto -> 1 (esponente 1/3 nitido anche per V)", abs(dV/(e**(1/3)*M**(2/3)) - 1) < 1e-3)

# (4) VAR-P5(c): controesempio al '<=>' nella classe CONTINUA. Dirac libero m=0, V=0:
# psi = f(x-t) v_+ + h(x+t) v_-, con sigma1 v_pm = pm v_pm. x0 = 1, I = (0,1).
# h supportata in (0.8, 1.0): h(x0+t) = 0 per t in (0,1) => span{psi(t,x0)} = C v_+ (una retta),
# ma per x in (0.8,1) lo span e' C^2: un W continuo con W psi = 0 si annulla su (0.8,1), quindi in x0.
def bump(s, l, r_):
    m, hw = (l + r_)/2, (r_ - l)/2
    y = np.clip(1 - ((s - m)/hw)**2, 1e-300, None)
    return np.where((s > l) & (s < r_), np.exp(-1/y), 0.0)
f = lambda s: 1.0 + 0*s                 # f costante (soluzione lecita)
h = lambda s: bump(s, 0.8, 1.0)
vp = np.array([1, 1])/np.sqrt(2); vm = np.array([1, -1])/np.sqrt(2)
ts = np.linspace(0.001, 0.999, 999)
def span_rank(x0):
    Psi = np.array([f(x0 - tt)*vp + h(x0 + tt)*vm for tt in ts])
    sv = np.linalg.svd(Psi, compute_uv=False)
    return int(np.sum(sv > 1e-8*sv[0]))
chk("P5(c): rango dello span in x0=1 e' 1", span_rank(1.0) == 1)
chk("P5(c): rango dello span in x=0.9 e' 2 (quindi V(1) determinato per continuita')", span_rank(0.9) == 2)

# (5) VAR-P9(d): ||e^{Y/2}e^{X/2} - e^{X/2}e^{Y/2}|| = 1/4 con X = E12, Y = E21
X = sp.Matrix([[0, 1], [0, 0]]); Y = sp.Matrix([[0, 0], [1, 0]])
Dm = (Y/2).exp()*(X/2).exp() - (X/2).exp()*(Y/2).exp()
chk("P9(d): differenza = diag(-1/4, 1/4)", sp.simplify(Dm - sp.diag(-sp.Rational(1, 4), sp.Rational(1, 4))) == sp.zeros(2))

# (6) VAR-T10(3)(ii): parola L.U.L unipotente per M in SL2
g1, g2, sg = sp.symbols('gamma1 gamma2 sigma')
W = sp.Matrix([[1, 0], [g1, 1]])*sp.Matrix([[1, sg], [0, 1]])*sp.Matrix([[1, 0], [g2, 1]])
solI = sp.solve(list(W - sp.eye(2)), [g1, g2, sg], dict=True)
solmI = sp.solve(list(W + sp.eye(2)), [g1, g2, sg], dict=True)
print("   T10: soluzioni per M = I :", solI, " per M = -I :", solmI)
chk("T10: M = I ammette la parola degenere (sigma = 0, gamma1 = -gamma2)", len(solI) > 0)
chk("T10: M = -I (parita', t = pi/2 per H = -d^2 + x^2) non ammette la parola", len(solmI) == 0)
tt_ = sp.symbols('t', real=True)
gam = (sp.cos(2*tt_) - 1)/(2*sp.sin(2*tt_))
chk("T10: gamma(t) = -tan(t)/2 (diverge a cos t = 0 nella normalizzazione H)", sp.simplify(gam + sp.tan(tt_)/2) == 0)

# (7) portata di VAR-T1(b): con V(x) a salto in x1 e u in C^{1,2}, Vu continua forza u(t,x1) = 0
# stazionario h'' = (V - E) h: salto di h'' in x1 = [V] h(x1); h in C^2 => h(x1) = 0 se [V] != 0.
Vl, Vr, hx1 = sp.symbols('V_l V_r h1')
jump = (Vr - E)*hx1 - (Vl - E)*hx1
chk("T1(b): salto di h'' = (V_r - V_l) h(x1)", sp.simplify(jump - (Vr - Vl)*hx1) == 0)

# (8) VAR-E2: nella soluzione razionale di Riccati w = eps x + c + sum 1/(x-a_j) la costante c e' nulla
eps, c, a1 = sp.symbols('epsilon c a1')
wE = eps*x + c + 1/(x - a1)
expr = sp.series((sp.diff(wE, x) + wE**2 - (x**2 - E)).subs(eps**2, 1), x, sp.oo, 3)
coef_x = sp.expand(sp.diff(wE, x) + wE**2).subs(eps**2, 1)
lin = sp.limit((sp.diff(wE, x) + wE**2 - x**2*eps**2)/x, x, sp.oo)
chk("E2: coefficiente di x in w'+w^2 e' 2 eps c (=> c = 0)", sp.simplify(lin - 2*eps*c) == 0)

# (9) stima di Cauchy (VAR-T1(c)(iii)): |g^(k)(t)| <= k! (t/10)^(-k) e^{-1/(2t^2)}, g = exp(-t^-2)
mp.mp.dps = 40
worst = 0.0
for tv in [0.05, 0.1, 0.2, 0.5, 0.9]:
    for k in [0, 1, 2, 4, 8, 12, 16]:
        d = abs(mp.diff(lambda s: mp.exp(-1/s**2), tv, k))
        bound = mp.factorial(k)*(tv/10)**(-k)*mp.exp(-1/(2*tv**2))
        worst = max(worst, float(d/bound))
print(f"   Tychonoff: max |g^(k)| / maggiorante = {worst:.3e}")
chk("Tychonoff: stima di Cauchy rispettata su 35 coppie (t, k)", worst <= 1.0)
print("TUTTO OK" if ok else "FALLITO")
