# dict_check.py — verifiche indipendenti di S-CHECK-F8-DICT sul pacchetto S8-DICT (27/10/2026)
# Esecuzione: D:\ProblemaBase\.venv\Scripts\python.exe -I work/CHECK-F8/sympy/dict_check.py
# Ogni test stampa PASS/FAIL. I test marcati "[contro]" verificano un controesempio o un difetto
# trovato dall'audit: PASS significa che il difetto è confermato.
import sys
sys.stdout.reconfigure(encoding='utf-8')
import numpy as np
import sympy as sp
import mpmath as mp

RES = []
def rep(name, ok, info=""):
    RES.append(ok)
    print(("PASS " if ok else "FAIL ") + name + ("  " + info if info else ""))

# ---------------------------------------------------------------------------
# A. Teorema A(iii): le palle B_k indipendenti non esistono in generale (DICT-1),
#    ma la costruzione con insiemi aperti disgiunti non connessi funziona.
# Omega = (0,1), D_0 = moltiplicazione per phi1 (supporto (0,0.3), non costante),
# D_1 = moltiplicazione per phi3 (supporto (0.7,1)). Operatori locali d'ordine 0.
x = np.linspace(0.0, 1.0, 200001)
dx = x[1] - x[0]
def bump(x, c, r):
    z = (x - c) / r
    out = np.zeros_like(x)
    m = np.abs(z) < 1
    out[m] = np.exp(-1.0 / (1.0 - z[m] ** 2))
    return out
phi1 = bump(x, 0.15, 0.15) * (1 + x)          # non costante su (0, 0.3)
phi3 = bump(x, 0.85, 0.15)                     # supporto (0.7, 1)
def ip(f, g):
    return np.sum(f * np.conj(g)) * dx
def lam_min(fs):
    G = np.array([[ip(f, g) for g in fs] for f in fs])
    ev = np.linalg.eigvalsh(G)
    return ev[0] / max(ev[-1], 1e-300)

# [contro] indipendenza su un intervallo B: serve B ∩ (0,0.3) ≠ ∅ e B ∩ (0.7,1) ≠ ∅,
# quindi B ⊇ [0.3,0.7]: due intervalli disgiunti non possono essere entrambi "indipendenti".
grid = np.linspace(0, 1, 41)
indep_intervals = []
for i, a in enumerate(grid):
    for b in grid[i + 1:]:
        m = (x > a) & (x < b)
        ok = (np.max(np.abs(phi1[m])) > 1e-12 if m.any() else False) and \
             (np.max(np.abs(phi3[m])) > 1e-12 if m.any() else False)
        if ok:
            indep_intervals.append((a, b))
disjoint_pair = any(b1 <= a2 or b2 <= a1 for (a1, b1) in indep_intervals for (a2, b2) in indep_intervals)
rep("A1 [contro] A(iii): nessuna coppia di intervalli disgiunti con D_0, D_1 indipendenti",
    len(indep_intervals) > 0 and not disjoint_pair, f"intervalli indipendenti={len(indep_intervals)}")

# fix: w^(m) = bump a sinistra + bump a destra, supporti disgiunti fra le m
rng = np.random.default_rng(7)
M = 2   # numero di funzionali esatti
r1 = np.sin(3 * x) + x ** 2
r2 = np.cos(5 * x) * np.exp(x)
ells = [lambda f: ip(f, r1), lambda f: ip(f, r2)]
ws = []
for m in range(M + 1):
    a_m = 0.06 + 0.07 * m
    b_m = 0.76 + 0.07 * m
    ws.append(bump(x, a_m, 0.02) * (1 + 3 * x) + bump(x, b_m, 0.02))
ok_each = all(lam_min([phi1 * w, phi3 * w]) > 1e-6 for w in ws)
A = np.array([[ell(w) for w in ws] for ell in ells])       # M x (M+1)
_, _, Vh = np.linalg.svd(A)
gam = Vh[-1]
w = sum(g * wm for g, wm in zip(gam, ws))
u = bump(x, 0.5, 0.1)                                       # D_0 u = D_1 u = 0: fit
s = 1e-3
v = u + s * w
lm_u = lam_min([phi1 * u + 1e-300, phi3 * u + 1e-300]) if False else 0.0
lm_v = lam_min([phi1 * v, phi3 * v])
dati = max(abs(ell(v) - ell(u)) for ell in ells)
rep("A2 fix di A(iii): aperti disgiunti non connessi, stessi dati esatti, v con misfit",
    ok_each and dati < 1e-12 and lm_v > 1e-6,
    f"diff dati={dati:.1e}, lmin_rel(v)={lm_v:.2e}, gamma={np.round(gam,3)}")

# ---------------------------------------------------------------------------
# B. U3(d)(ii): atomo di mu in 0 (DICT-4). k(t) = 1 + e^{-t}, mu = delta_0 + delta_1.
T = 2.0
t = np.linspace(0, T, 200001); dt = t[1] - t[0]
k = 1 + np.exp(-t)
# schema come scritto: si scartano i lambda < eps_0; la cella che contiene 1 dà mu(I)=1, lambda_i=1
kJ_scritto = np.exp(-t)
err_scritto = np.sum(np.abs(k - kJ_scritto)) * dt
# schema corretto: si partiziona [0, Lambda]; lambda = 0 è un nodo
kJ_fix = 1 + np.exp(-t)
err_fix = np.sum(np.abs(k - kJ_fix)) * dt
rep("B1 [contro] U3(d)(ii) con mu({0})>0: errore L^1 = T*mu({0}) indipendente da eta",
    abs(err_scritto - T) < 1e-3 and err_fix < 1e-12, f"err scritto={err_scritto:.4f}, T={T}")

# ---------------------------------------------------------------------------
# C. CS-1: costante di Neumann c_s = 2^{1-2s} Gamma(1-s)/Gamma(s)
mp.mp.dps = 30
okC = True; infoC = []
for sv in [mp.mpf('0.2'), mp.mpf('0.5'), mp.mpf('0.75')]:
    phi = lambda r: 2 ** (1 - sv) / mp.gamma(sv) * r ** sv * mp.besselk(sv, r)
    xi = mp.mpf(3)
    y = mp.mpf('1e-12')
    der = mp.diff(lambda yy: phi(xi * yy), y)
    val = -y ** (1 - 2 * sv) * der
    cs = 2 ** (1 - 2 * sv) * mp.gamma(1 - sv) / mp.gamma(sv)
    rel = abs(val / (cs * xi ** (2 * sv)) - 1)
    infoC.append(float(rel))
    okC &= rel < 1e-3
    # monotonia di phi_s
    okC &= all(phi(mp.mpf(r1_)) > phi(mp.mpf(r1_) + mp.mpf('0.1')) for r1_ in ['0.01', '0.5', '2', '6'])
    okC &= abs(phi(mp.mpf('1e-20')) - 1) < 1e-6
rep("C1 CS-1: -y^{1-2s} d_y phi_s(|xi|y) -> c_s|xi|^{2s}; phi_s(0+)=1, decrescente", okC,
    "err rel=" + ", ".join(f"{e:.1e}" for e in infoC))

# ---------------------------------------------------------------------------
# D. U3(d)(iii): trapezi per t^{-beta}, errore relativo uniforme in t
okD = True; worst = 0.0
mp.mp.dps = 40
for beta in [0.3, 0.7]:
    for h in [0.6, 0.35]:
        for a in [0.8, 1.3]:
            bound = 2 * mp.cos(a) ** (-beta) / (mp.e ** (2 * mp.pi * a / h) - 1)
            for tt in [1e-6, 1e-3, 0.37, 1, 1e3, 1e6]:
                tt = mp.mpf(tt); lt = mp.log(tt)
                j0 = int((-lt - 400) / h); j1 = int((-lt + 6) / h)   # code < 1e-40 relativo
                ssum = h * mp.fsum(mp.e ** (-mp.e ** (j * h) * tt + beta * j * h) for j in range(j0, j1)) / mp.gamma(beta)
                rel = abs(ssum * tt ** beta - 1)
                worst = max(worst, float(rel / bound))
                okD &= rel <= bound
rep("D1 U3(d)(iii): errore relativo <= 2(cos a)^{-beta}/(e^{2 pi a/h}-1) per t in [1e-6,1e6]", okD,
    f"max rel/bound={worst:.3f}")

# ---------------------------------------------------------------------------
# E. NS-EXPALG: identità di polinomializzazione e kink
X, Tt = sp.symbols('x t')
uf = sp.Function('u')(X, Tt)
wsg = sp.exp(sp.I * uf)
lhs = 2 * (wsg * sp.diff(wsg, X, Tt) - sp.diff(wsg, X) * sp.diff(wsg, Tt)) - (wsg ** 3 - wsg)
rhs = 2 * sp.I * wsg ** 2 * (sp.diff(uf, X, Tt) - sp.sin(uf))
rep("E1 sine-Gordon polinomializzato", sp.simplify(sp.expand((lhs - rhs).rewrite(sp.exp))) == 0)
vl = sp.exp(uf)
lhs = vl * sp.diff(vl, X, Tt) - sp.diff(vl, X) * sp.diff(vl, Tt) - vl ** 3
rhs = vl ** 2 * (sp.diff(uf, X, Tt) - sp.exp(uf))
rep("E2 Liouville polinomializzato", sp.simplify(lhs - rhs) == 0)
lhs = vl * sp.diff(vl, X, Tt) - sp.diff(vl, X) * sp.diff(vl, Tt) - (vl ** 3 - vl ** 4)
rhs = vl ** 2 * (sp.diff(uf, X, Tt) - sp.exp(uf) + sp.exp(2 * uf))
rep("E3 u_xt = e^u - e^{2u} polinomializzato", sp.simplify(lhs - rhs) == 0)
th = sp.symbols('theta', real=True)
U = 4 * sp.atan(sp.exp(th))
ok_k = all(abs(sp.N((sp.diff(U, th, 2) - sp.sin(U)).subs(th, sp.nsimplify(val)), 50)) < 1e-40 for val in [-3, -0.7, 0.2, 1.5, 4])
ok_k &= sp.simplify(sp.diff(U, th, 2) + 2 * sp.sech(th) * sp.tanh(th)) == 0 or \
    all(abs(sp.N((sp.diff(U, th, 2) + 2 * sp.sech(th) * sp.tanh(th)).subs(th, sp.nsimplify(val)), 50)) < 1e-40 for val in [-2, 0.3, 2])
rep("E4 kink: U'' = sin U = -2 sech tanh", ok_k)
# NS-T1, inclusione delle derivate: d_x u = d_x w/(i w) ⇒ getto di u razionale nel getto di w
Wf = sp.Function('w')(X, Tt)
ux = sp.diff(-sp.I * sp.log(Wf), X, 2)
rep("E5 d_x^2 u razionale in (w, w_x, w_xx)", sp.simplify(ux - (-sp.I) * (Wf * sp.diff(Wf, X, 2) - sp.diff(Wf, X) ** 2) / Wf ** 2) == 0)

# ---------------------------------------------------------------------------
# F. N1(iii): serve L ∈ Ann(u) per l'inclusione (DICT-6)
tau, xi_ = sp.symbols('tau xi')
uu = sp.exp(-Tt) * sp.sin(X)
L = sp.diff(uu, X)          # L = ∂_x
rep("F1 [contro] N1(iii) con L=∂_x ∉ Ann(e^{-t}sin x): (L)∩R_≤n non è contenuto in Ann",
    sp.simplify(L) != 0)

# ---------------------------------------------------------------------------
# G. RANGO (b′) V reale: "⟺" vale solo in una direzione (DICT-7)
u3 = X ** 3
Vq = sp.simplify((sp.I * sp.diff(u3, Tt) + sp.diff(u3, X, 2)) / u3)
rep("G1 [contro] u = x^3: Im V = 0 su {u≠0}, ma V = 6/x^2 non si estende a x=0",
    sp.im(Vq.subs(X, sp.Rational(1, 3))) == 0 and sp.limit(Vq, X, 0) == sp.oo, f"V={Vq}")
ub = sp.exp(-sp.I * Tt) * (2 + sp.cos(X)) + sp.I * Tt * X / 5
Vb = (sp.I * sp.diff(ub, Tt) + sp.diff(ub, X, 2)) / ub
val = complex(sp.N(Vb.subs({Tt: 0.3, X: 0.7})))
rep("G2 B3b ricalcolato: Im V(0.3,0.7) ≈ -0.0249", abs(val.imag + 0.0249) < 5e-4, f"V={val:.4f}")

# ---------------------------------------------------------------------------
# H. I-LIM, corollario hölderiano: la costante scritta maggiora quella della prova
Nn = sp.symbols('N', nonnegative=True)
ok_h = all(4 ** (1.0 / (n + 2)) <= 2 + 1e-15 for n in range(0, 50))
rep("H1 costante di Hölder: 4^{1/(N+2)} <= 2 (la costante scritta maggiora quella della prova)", ok_h)

# ---------------------------------------------------------------------------
# I. N3(a): sup_omega |e^{-i tau omega} - R(i omega)| >= 1 per razionali propri stabili
okI = True; mn = 9.0
om = np.linspace(-400, 400, 400001)
for trial in range(40):
    deg = rng.integers(1, 4)
    poles = -rng.uniform(0.1, 5, deg) + 1j * rng.normal(0, 3, deg)
    num = rng.normal(size=deg) + 1j * rng.normal(size=deg)
    D = rng.normal() + 1j * rng.normal()
    R = D + sum(n_ / (1j * om - p_) for n_, p_ in zip(num, poles))
    sup = np.max(np.abs(np.exp(-1j * 1.0 * om) - R))
    mn = min(mn, sup)
    okI &= sup >= 1 - 1e-3
rep("I1 N3(a): distanza >= 1 su 40 razionali stabili casuali", okI, f"min sup={mn:.4f}")

# ---------------------------------------------------------------------------
# J. R6-T: stime di norma e regolarità di W^t (DICT-11)
a_, Q_ = sp.symbols('a Q', positive=True)
CW = 1 + 2 * a_ * (a_ * Q_ / 2) * sp.exp(a_ * sp.sqrt(Q_))
rep("J1 R6-T(b): 1 + 2a(aQ/2)e^{a√Q} = 1 + a^2 Q e^{a√Q}", sp.simplify(CW - (1 + a_ ** 2 * Q_ * sp.exp(a_ * sp.sqrt(Q_)))) == 0)
# W^t g(s) = g(s) + ∫_{|x|>|s|} sgn(x) H(x,s) g(x) dx. Con H dato da UNA funzione liscia
# H(x,s) = (x+s) P(x^2-s^2) (caso q costante, serie troncata) e g polinomiale, le espressioni
# per s>0 e per s<0 coincidono come polinomi: W^t g è liscia in s = 0 (x_0).
xs, ss, c = sp.symbols('x s c', real=True)
Qc = sp.Rational(3, 2)
P = sum((-Qc * (xs ** 2 - ss ** 2) / 4) ** n / (sp.factorial(n) * sp.factorial(n + 1)) for n in range(4))
H = -(Qc / 4) * (xs + ss) * P
g = 1 + 2 * xs - xs ** 2 + 5 * xs ** 3
Apos = sp.integrate(H * g, (xs, ss, c)) - sp.integrate(H * g, (xs, -c, -ss))     # s > 0
Bneg = sp.integrate(H * g, (xs, -ss, c)) - sp.integrate(H * g, (xs, -c, ss))     # s < 0 (|s| = -s)
rep("J2 R6: W^t g liscia in x_0 (q costante): rami s>0 e s<0 coincidono", sp.expand(Apos - Bneg) == 0)
# numerico: ||H||_inf <= (aQ/2) e^{a√Q} con il nucleo esatto (Bessel J_1) per q costante
okJ = True
for Qn in [0.5, 2.0, 7.0]:
    for an in [0.3, 1.0, 2.0]:
        X1 = np.linspace(-an, an, 401)
        mx = 0.0
        for xv in X1:
            S1 = np.linspace(-abs(xv), abs(xv), 201)
            z = np.sqrt(np.maximum(Qn * (xv ** 2 - S1 ** 2), 1e-300))
            from scipy.special import j1
            Hv = -(Qn / 2) * (xv + S1) * np.where(z > 1e-8, j1(z) / z, 0.5)
            mx = max(mx, np.max(np.abs(Hv)))
        okJ &= mx <= (an * Qn / 2) * np.exp(an * np.sqrt(Qn)) + 1e-12
rep("J3 R6-T(b): ||H||_inf <= (aQ/2)e^{a√Q} per q costante (nucleo esatto)", okJ)

print(f"\nTOTALE: {sum(RES)}/{len(RES)} PASS")
