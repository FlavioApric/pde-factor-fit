# S8-CONV: verifica numerica (non prova) di CONV-T4(a), CONV-T5(1),(3) e della costruzione di CONV-T5(3).
import numpy as np
import sympy as sp
rng = np.random.default_rng(20261027)
ok = True
def check(name, cond):
    global ok
    ok = ok and bool(cond)
    print(('PASS ' if cond else 'FAIL ') + name)

# (A) T4(a) e T5(1),(3) in dimensione finita: Phi con nucleo di dimensione r, perturbazione ||E|| <= delta
worst = 0.0; worst3 = 0.0
for trial in range(4000):
    M, r = rng.integers(3, 9), 1 + (trial % 2)
    U, _ = np.linalg.qr(rng.normal(size=(20, 20)) + 1j*rng.normal(size=(20, 20)))
    Vh, _ = np.linalg.qr(rng.normal(size=(M, M)) + 1j*rng.normal(size=(M, M)))
    sv = np.concatenate([np.zeros(r), np.sort(rng.uniform(0.05, 3, size=M - r))])
    Phi = U[:, :M] @ np.diag(sv) @ Vh.conj().T
    K = Vh[:, :r]                                        # base ortonormale del nucleo
    delta = 10**rng.uniform(-4, -1)
    E = rng.normal(size=(20, M)) + 1j*rng.normal(size=(20, M)); E *= delta/np.linalg.norm(E, 2)
    _, _, Wh = np.linalg.svd(Phi + E)
    lam = Wh.conj().T[:, -1]
    dist = np.linalg.norm(lam - K @ (K.conj().T @ lam))
    bound = 2*delta/sv[r]                               # sv[r] = sigma_{r+1}
    worst = max(worst, dist/bound) if r == 1 else worst
    worst3 = max(worst3, dist/bound) if r == 2 else worst3
check('T4(a): sin <= 2 delta/sigma_2 (r=1), max rapporto %.3f' % worst, worst <= 1 + 1e-9)
check('T5(1): dist <= 2 delta/sigma_{r+1} (r=2), max rapporto %.3f' % worst3, worst3 <= 1 + 1e-9)
# ottimalita' dell'ordine (esempio 2x2)
rho, d = sp.symbols('rho delta', positive=True)
A = sp.Matrix([[0, 0], [0, rho]]); Ep = sp.Matrix([[0, 0], [d, 0]])
G = (A + Ep).T*(A + Ep)
ev = G.eigenvects()
vmin = min(ev, key=lambda e: sp.limit(e[0].subs(d, rho/10), rho, 1))[2][0]
sinth = sp.simplify(abs(vmin[1])/sp.sqrt(vmin[0]**2 + vmin[1]**2))
check('T4(a) ottimalita: sin = delta/sqrt(rho^2+delta^2)', sp.simplify(sinth - d/sp.sqrt(rho**2 + d**2)) == 0)

# (B) funzioni: Gram su Omega = (0,1)^2 con quadratura di Gauss
t, x = sp.symbols('t x')
xg, wg = np.polynomial.legendre.leggauss(40); xg = (xg + 1)/2; wg = wg/2
TT, XX = np.meshgrid(xg, xg, indexing='ij'); WW = np.outer(wg, wg)
def feats(u, m):
    cols = []
    for i in range(m + 1):
        for j in range(m + 1 - i):
            f = sp.lambdify((t, x), sp.diff(u, t, i, x, j), 'numpy')
            cols.append(np.broadcast_to(f(TT, XX), TT.shape).ravel()*np.sqrt(WW.ravel()))
    return np.array(cols).T
def svals(u, m): return np.sort(np.linalg.svd(feats(u, m), compute_uv=False))
u = (t + 1)**sp.Rational(-1, 2)*sp.exp(-x**2/(4*(t + 1)))      # calore, non EP: Ann = (tau - xi^2), d = 2
s0, s1 = svals(u, 0)[0], svals(u, 1)[0]
sd = svals(u, 2)
check('calore: sigma_1(Phi_2(u)) ~ 0 (%.2e), sigma_2 = %.3e > 0' % (sd[0], sd[1]), sd[0] < 1e-10 and sd[1] > 1e-4)
check('calore: s_0 = %.3e, s_1 = %.3e > 0' % (s0, s1), s0 > 1e-3 and s1 > 1e-5)
# rumore H^2: rule R_delta sceglie m = 2 e l'angolo rispetta 2 delta/rho
P = np.zeros(6); mons = [(i, j) for i in range(3) for j in range(3 - i)]
P[mons.index((1, 0))] = 1; P[mons.index((0, 2))] = -1; P /= np.linalg.norm(P)
for delta in (1e-3, 1e-4):
    w = sp.sin(7*t + 3*x)*sp.Rational(1, 1)
    nw = np.linalg.norm(feats(w, 2), 2)                          # ||Phi_2(w)|| >= ...; norma H^2 di w via Gram
    hn = np.sqrt(sum(np.linalg.norm(c)**2 for c in feats(w, 2).T))
    ut = u + sp.Float(delta/hn)*w                                 # ||ut - u||_{H^2} = delta
    sel = [m for m in range(0, 4) if svals(ut, m)[0] <= delta][0]
    _, _, Wh = np.linalg.svd(feats(ut, 2)); lam = Wh.conj().T[:, -1]
    sinang = np.sqrt(max(0, 1 - abs(lam.conj() @ P)**2))
    check('T5(1) rumore H^2 delta=%g: m(delta) = %d, sin = %.2e <= 2delta/rho = %.2e' % (delta, sel, sinang, 2*delta/sd[1]), sel == 2 and sinang <= 2*delta/sd[1])
# (C) T5(3): u' = u + eps t^2 x^2 ha Ann(u') cap R_{<=2} = 0 e sigma_1(Phi_2(u')) <= eps ||P(d) p||
p = t**2*x**2
Pp = sp.diff(p, t) - sp.diff(p, x, 2)
nPp = np.sqrt(np.sum(sp.lambdify((t, x), Pp**2, 'numpy')(TT, XX)*WW))
for eps in (1e-2, 1e-3):
    up = u + eps*p
    s2 = svals(up, 2)[0]
    check('T5(3) eps=%g: sigma_1(Phi_2(u+eps p)) = %.2e <= eps ||Pp||/|P| = %.2e' % (eps, s2, eps*nPp/np.sqrt(2)), s2 <= eps*nPp/np.sqrt(2) + 1e-12)
    check('T5(3) eps=%g: sigma_1(Phi_2(u+eps p)) > 0 (nessuna legge di grado <= 2)' % eps, s2 > 1e-12)
# Ann(t^2 x^2) cap R_{<=2} = 0 (simbolico)
qs = sp.symbols('q0:6'); Q = sum(qs[k]*sp.diff(p, t, i, x, j) for k, (i, j) in enumerate(mons))
sol = sp.solve(sp.Poly(sp.expand(Q), t, x).coeffs(), qs, dict=True)
check('Ann(t^2 x^2) cap R_{<=2} = 0', sol == [{q: 0 for q in qs}])
print('ESITO:', 'TUTTI PASS' if ok else 'QUALCHE FAIL')
