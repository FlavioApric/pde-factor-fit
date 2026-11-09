# F6-DICT — verifiche (solo controllo, non prova). Eseguire con:
#   D:\ProblemaBase\.venv\Scripts\python.exe -I research/F6-DICT/sympy/dict_checks.py
import numpy as np
import sympy as sp
from numpy.polynomial.legendre import leggauss
from math import gamma

OK = []
def check(name, cond, info=""):
    OK.append(bool(cond))
    print(("OK  " if cond else "FAIL") + f" [{name}] {info}")

# ---------- quadratura tensoriale su Omega = [-1/2,1/2]_x x [0,1]_t ----------
nq = 60
gx, wx = leggauss(nq); X = 0.5 * gx; WX = 0.5 * wx          # x in [-1/2,1/2]
gt, wt = leggauss(nq); T = 0.5 * (gt + 1); WT = 0.5 * wt    # t in [0,1]
XX, TT = np.meshgrid(X, T, indexing="ij"); W = np.outer(WX, WT)
ip = lambda f, g: np.sum(W * f * g)

def residual_level(Du0, atoms):
    """min_c ||Du0 + sum c_i atoms_i||_L2 (forma normalizzata L = D0 + sum c_i D_i):
    equazioni normali G c = -b; ritorna (c, r, G, b)."""
    N = len(atoms)
    G = np.array([[ip(atoms[i], atoms[j]) for j in range(N)] for i in range(N)])
    b = np.array([ip(atoms[i], Du0) for i in range(N)])
    c = np.linalg.solve(G, -b)
    res = Du0 + sum(c[i] * atoms[i] for i in range(N))
    return c, np.sqrt(ip(res, res)), G, b, res

# ===== (A) trasporto a coeff. NON polinomiale: u_t = a(x) u_x, a = 1/(1+x^2) =====
# psi' = 1/a = 1 + x^2, psi = x + x^3/3, u = sin(psi(x) + t)
psi = XX + XX**3 / 3; a = 1 / (1 + XX**2)
u_t = np.cos(psi + TT); u_x = np.cos(psi + TT) * (1 + XX**2)
check("A0 equazione", np.max(np.abs(u_t - a * u_x)) < 1e-12)
rs = []
for n in range(0, 9):
    atoms = [-(XX**j) * u_x for j in range(n + 1)]   # L = d_t - p(x) d_x, p = sum c_j x^j
    c, r, G, b, res = residual_level(u_t, atoms)
    rs.append(r)
    # Gram: r^2 = det G(D0u, D1u..)/det G(D1u..)
    allv = [u_t] + atoms
    Gfull = np.array([[ip(f, g) for g in allv] for f in allv])
    ratio = np.linalg.det(Gfull) / np.linalg.det(G)
    if n <= 4:
        check(f"A1 Gram-ratio n={n}", abs(ratio - r**2) <= 1e-6 * max(1e-30, r**2) + 1e-20,
              f"r^2={r**2:.3e} ratio={ratio:.3e}")
    # funzionale di Hahn-Banach phi = res/||res||: annulla gli atomi, phi(D0u) = r
    if r > 1e-10:
        ann = max(abs(ip(res, A)) for A in atoms) / (r * max(np.sqrt(ip(A, A)) for A in atoms))
        check(f"A2 certificato HB n={n}", ann < 1e-8 and abs(ip(res, u_t) / r - r) < 1e-8 * max(1, r),
              f"r_n={r:.3e}")
check("A3 residui monotoni", all(rs[i + 1] <= rs[i] * (1 + 1e-9) for i in range(len(rs) - 1)))
# a = 1/(1+x^2) su [-1/2,1/2]: poli in +-i -> ellisse di Bernstein rho = 2+sqrt(5) (scala [-1,1])
rho = 2 + np.sqrt(5)
fit = np.polyfit(np.arange(2, 8), np.log(rs[2:8]), 1)
check("A4 velocita' geometrica ~ rho^{-n}", -fit[0] > 0.5 * np.log(rho) ** 1 * 0.5,
      f"pendenza log r_n = {fit[0]:.3f}, log(rho) = {np.log(rho):.3f}")
# stima a posteriori: |c_n - c~_n| <= 2 eta / sqrt(lambda_min), c~ = interpolante di Chebyshev di a
for n in [2, 4, 6]:
    atoms = [-(XX**j) * u_x for j in range(n + 1)]
    c, r, G, b, res = residual_level(u_t, atoms)
    xc = 0.5 * np.cos((2 * np.arange(n + 1) + 1) * np.pi / (2 * n + 2))
    V = np.vander(xc, n + 1, increasing=True)
    ct = np.linalg.solve(V, 1 / (1 + xc**2))
    pt = sum(ct[j] * XX**j for j in range(n + 1))
    eta = np.sqrt(ip((a - pt) * u_x, (a - pt) * u_x))
    lam = np.min(np.linalg.eigvalsh(G))
    lhs = np.linalg.norm(c - ct); rhs = 2 * eta / np.sqrt(lam)
    check(f"A5 stima coeff n={n}", lhs <= rhs, f"|dc|={lhs:.3e} <= 2eta/sqrt(lam)={rhs:.3e} (lam={lam:.2e})")

# ===== (B) coefficiente polinomiale: a = 1 + x, u = sin(log(1+x) + t): identificazione esatta al livello 1 =====
ub_t = np.cos(np.log(1 + XX) + TT); ub_x = np.cos(np.log(1 + XX) + TT) / (1 + XX)
for n in [0, 1, 2, 3]:
    atoms = [-(XX**j) * ub_x for j in range(n + 1)]
    c, r, G, b, res = residual_level(ub_t, atoms)
    if n == 0:
        check("B0 misfit al livello 0", r > 1e-3, f"r_0={r:.3e}")
    else:
        target = np.zeros(n + 1); target[0] = 1; target[1] = 1
        check(f"B1 livello {n}: r=0 e c=(1,1,0..)", r < 1e-9 and np.allclose(c, target, atol=1e-7),
              f"r={r:.1e}")

# ===== (C) non monotonia dell'identificazione per dati EP (esatto, SymPy) =====
t, x = sp.symbols("t x", real=True)
u = sp.exp(-t) * sp.sin(x)       # calore: Ann(u) contiene tau+1, xi^2+1, tau - xi^2
ops = {"d_t": sp.diff(u, t), "d_xx": sp.diff(u, x, 2), "1": u, "d_x": sp.diff(u, x)}
def kernel_dim(names):
    cs = sp.symbols("c0:%d" % len(names))
    expr = sp.expand(sum(ci * ops[nm] for ci, nm in zip(cs, names)) / sp.exp(-t))
    eqs = [sp.expand(expr).coeff(f) for f in [sp.sin(x), sp.cos(x)]]
    M = sp.Matrix([[sp.diff(e, ci) for ci in cs] for e in eqs])
    return len(names) - M.rank()
check("C1 livello {d_t, d_xx}: nucleo dim 1 (calore)", kernel_dim(["d_t", "d_xx"]) == 1)
check("C2 livello {d_t, d_xx, 1}: nucleo dim 2 (non identifica)", kernel_dim(["d_t", "d_xx", "1"]) == 2)
check("C3 livello {d_t, d_xx, 1, d_x}: nucleo dim 2", kernel_dim(["d_t", "d_xx", "1", "d_x"]) == 2)

# ===== (D) ordine frazionario: | |xi|^s - |xi|^s' | <xi>^{-m'} <= C |s - s'|, m' > max(s,s') =====
xi = np.logspace(-3, 6, 4000)
for (s, s2, mp) in [(0.5, 0.5 + 1e-3, 0.6), (1.5, 1.5 - 1e-2, 1.6)]:
    lhs = np.max(np.abs(xi**s - xi**s2) * (1 + xi**2) ** (-mp / 2)) / abs(s - s2)
    # stima: |xi^s - xi^s'| <= |s-s'| |log xi| max(xi^s, xi^s'); sup |log xi| xi^{max} <xi>^{-m'} < inf
    bound = np.max(np.abs(np.log(xi)) * np.maximum(xi**s, xi**s2) * (1 + xi**2) ** (-mp / 2))
    check(f"D1 s={s}", lhs <= bound * (1 + 1e-9), f"rapporto={lhs:.3f} <= {bound:.3f}")

# ===== (E) memoria: t^{-1/2} come somma di esponenziali (trapezi in log-variabile) =====
beta = 0.5
tt = np.logspace(-3, 0, 400)
for h in [1.0, 0.6, 0.4]:
    # troncamento: coda inferiore ~ e^{beta s_min}/(beta Gamma(beta)) -> s_min = -40; superiore ~ exp(-e^{s_max} t_min)
    s = np.arange(-40, 15 + 1e-9, h)       # lambda = e^s
    lam_, w_ = np.exp(s), h * np.exp(beta * s) / gamma(beta)
    approx = np.array([np.sum(w_ * np.exp(-lam_ * ti)) for ti in tt])
    rel = np.max(np.abs(approx - tt**(-beta)) * tt**beta)
    print(f"     E h={h}: termini={len(s)}, errore relativo max su [1e-3,1] = {rel:.2e}")
check("E1 somma di esponenziali, errore rel < 1e-6 con h=0.4", rel < 1e-6)

# ===== (F) immersione markoviana: w(t) = int_0^t e^{-l(t-s)} f(s) ds  <=>  w' = -l w + f, w(0)=0 =====
l, s_ = sp.symbols("l s", positive=True)
f = sp.sin(3 * s_) + s_**2
w = sp.integrate(sp.exp(-l * (t - s_)) * f, (s_, 0, t))
check("F1 memoria esponenziale = sistema locale aumentato",
      sp.simplify(sp.diff(w, t) + l * w - f.subs(s_, t)) == 0 and sp.simplify(w.subs(t, 0)) == 0)

# ===== (G) blocchi diadici: S^m non separabile (separazione 1 tra m_eps) =====
# psi diadico: psi(r) = phi(r) - phi(2r), phi = 1 su [0,1], 0 per r >= 2 (C^inf); qui verifica della
# separazione: sup |m_eps - m_eps'| <xi>^{-m} >= sup_r psi(2^{-k} r) = 1 per k in eps \ eps'
def phi(r):
    r = np.asarray(r, float)
    g = lambda z: np.where(z > 0, np.exp(-1 / np.maximum(z, 1e-300)), 0.0)
    return g(2 - r) / (g(2 - r) + g(r - 1))
rr = np.linspace(0, 64, 200001)
psis = [phi(rr / 2**k) - phi(2 * rr / 2**k) for k in range(1, 5)]
check("G1 max psi_k = 1 e supporti a sovrapposizione limitata",
      all(abs(p.max() - 1) < 1e-3 for p in psis) and np.max(sum(psis)) <= 1 + 1e-9)

print(f"\nTOTALE: {sum(OK)}/{len(OK)} OK")
