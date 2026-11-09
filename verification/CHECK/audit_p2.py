# audit_p2.py - S-CHECK-4, red team per i claim di S-P2 (work/P2/CHECK_REQUEST.md)
# Esecuzione: D:\ProblemaBase\.venv\Scripts\python.exe -I audit_p2.py > audit_p2.out
import numpy as np, sympy as sp
rng = np.random.default_rng(20261025)
RES = []
def chk(name, ok, info=""):
    RES.append((name, bool(ok))); print(("OK  " if ok else "FAIL"), name, info)

def orth(M, tol=1e-10):
    u, s, vh = np.linalg.svd(M, full_matrices=False)
    return u[:, s > tol*max(1, s.max())]
def inter_basis(Q1, Q2, tol=1e-9):
    M = np.hstack([Q1, -Q2]); u, s, vh = np.linalg.svd(M)
    r = np.sum(s > tol)
    null = vh[r:].conj().T
    if null.shape[1] == 0: return np.zeros((Q1.shape[0], 0), dtype=Q1.dtype)
    return orth(Q1 @ null[:Q1.shape[1]])
def cF(Q1, Q2):
    I = inter_basis(Q1, Q2)
    PA = Q1 - I @ (I.conj().T @ Q1); PB = Q2 - I @ (I.conj().T @ Q2)
    A = orth(PA); B = orth(PB)
    return np.linalg.svd(A.conj().T @ B, compute_uv=False).max(), I.shape[1]
def rand_pair(n, d1, d2, k, cplx=False):
    f = (lambda *s: rng.standard_normal(s) + 1j*rng.standard_normal(s)) if cplx else (lambda *s: rng.standard_normal(s))
    Z = f(n, k); X = f(n, d1-k); Y = f(n, d2-k)
    return orth(np.hstack([Z, X])), orth(np.hstack([Z, Y]))

print("== P2-T3: spettro di S*S per due sottospazi ==")
for trial, (n, d1, d2, k, cp) in enumerate([(7,3,3,1,False),(9,4,3,2,False),(8,3,5,0,False),(10,5,4,3,True),(6,2,2,0,True),(12,6,7,2,False)]):
    Q1, Q2 = rand_pair(n, d1, d2, k, cp)
    c, dI = cF(Q1, Q2)
    S = np.hstack([Q1, Q2]); T = S.conj().T @ S
    ev = np.sort(np.linalg.eigvalsh(T)); nz = ev[ev > 1e-9]
    chk(f"T3a dim kerS = dim I (trial {trial})", np.sum(ev <= 1e-9) == dI, f"{np.sum(ev<=1e-9)} vs {dI}")
    chk(f"T3b min autoval. su (kerS)^perp = 1-c_F (trial {trial})", abs(nz.min() - (1-c)) < 1e-9, f"{nz.min():.6f} vs {1-c:.6f}")
    top = 2.0 if dI > 0 else 1 + c
    chk(f"T3a max = {'2' if dI>0 else '1+c_F'} (trial {trial})", abs(nz.max() - top) < 1e-9)
    core = nz[np.abs(nz - 2) > 1e-9]
    chk(f"T3a sigma(K) = -sigma(K) (trial {trial})", np.allclose(np.sort(core - 1), np.sort(1 - core), atol=1e-9))
    gam = 1 - c
    al = np.logspace(-8, 2, 400)
    nR = [np.linalg.norm(np.linalg.solve(T + a*np.eye(len(T)), S.conj().T), 2) for a in al]
    chk(f"T3c sup_alpha ||R_alpha|| = (1-c_F)^(-1/2) (trial {trial})", max(nR) <= gam**-0.5 + 1e-9 and abs(max(nR) - gam**-0.5) < 1e-3*gam**-0.5)
    w, V = np.linalg.eigh(T); idx = np.argmin(np.where(w > 1e-9, w, np.inf)); om = V[:, idx]
    u = S @ om; a = 0.3
    oma = np.linalg.solve(T + a*np.eye(len(T)), S.conj().T @ u)
    pinv = np.linalg.pinv(S) @ u
    lhs = np.linalg.norm(oma - pinv); rhs = a/(gam + a)*np.linalg.norm(pinv)
    chk(f"T3d ||w_a - S^+u|| = a/(gamma+a)||S^+u|| su autovettore (trial {trial})", abs(lhs - rhs) < 1e-8)
    chk(f"T3b ||S^+|| = (1-c_F)^(-1/2) (trial {trial})", abs(np.linalg.norm(np.linalg.pinv(S), 2) - gam**-0.5) < 1e-8)

print("== P2-T3 caso c_F = 1 (somma diretta di blocchi 2D con angolo theta_k -> 0) ==")
ths = [0.5**k for k in range(1, 12)]
lam_min = [1 - np.cos(t) for t in ths]
supR = [max(np.sqrt(l)/(l + a) for a in np.logspace(-10, 1, 400)) for l in lam_min]
chk("T3c sup_alpha ||R_alpha|| >= 1/(2 sqrt(lambda_k)) -> inf", all(s >= 0.5/np.sqrt(l) - 1e-9 for s, l in zip(supR, lam_min)) and supR[-1] > 100, f"ultimo {supR[-1]:.1f}")

print("== Red team N >= 3: c_F a coppie non governa la chiusura ==")
def gamma_N(lines):
    G = np.array([[np.dot(a, b) for b in lines] for a in lines]); ev = np.linalg.eigvalsh(G); return ev[ev > 1e-14].min()
def pair_cF(a, b): return abs(np.dot(a, b))
v = [np.array([np.cos(t), np.sin(t)]) for t in (0, 2*np.pi/3, 4*np.pi/3)]
g3 = gamma_N(v); pc = max(pair_cF(v[i], v[j]) for i in range(3) for j in range(i+1, 3))
chk("N3a tre rette a 120 gradi in R^2: gamma_3 = 1.5 mentre 1 - max c_F = 0.5", abs(g3 - 1.5) < 1e-12 and abs((1 - pc) - 0.5) < 1e-12)
gs = []
for eps in [1e-1, 1e-2, 1e-3, 1e-4]:
    w3 = [np.array([np.cos(t), np.sin(t), (eps if i == 0 else 0.0)]) for i, t in enumerate((0, 2*np.pi/3, 4*np.pi/3))]
    w3 = [q/np.linalg.norm(q) for q in w3]
    gs.append((gamma_N(w3), max(pair_cF(w3[i], w3[j]) for i in range(3) for j in range(i+1, 3))))
chk("N3b rette quasi complanari in R^3: c_F a coppie ~0.5, gamma_3 -> 0 (blocchi in somma diretta: somme a coppie chiuse, somma tripla non chiusa)", gs[-1][0] < 1e-7 and all(abs(p - 0.5) < 1e-2 for _, p in gs), str([f"{g:.2e}" for g, _ in gs]))

print("== Tabella P2-T3(e): trasporti paralleli c=0 ==")
d, T_ = sp.symbols('d T', positive=True); t = sp.symbols('t', real=True)
G11 = sp.integrate(1, (t, 0, T_)); G22 = sp.integrate(sp.exp(2*d*t), (t, 0, T_)); G12 = sp.integrate(sp.exp(d*t), (t, 0, T_))
g2 = sp.simplify((G12**2/(G11*G22) - sp.tanh(d*T_/2)/(d*T_/2)).rewrite(sp.exp))
chk("T3e gamma^2 = tanh(dT/2)/(dT/2)", g2 == 0)
chk("T3e gamma -> 1 per dT -> 0", sp.limit(sp.tanh(d*T_/2)/(d*T_/2), d, 0) == 1)

print("== P2-L1 / P2-T2 ==")
x, c, D, lam, z = sp.symbols('x c D lambda zeta')
tt = sp.symbols('t'); xi = sp.symbols('xi'); tau = sp.symbols('tau')
def op_poly(pol, f):
    P = sp.Poly(sp.expand(pol), xi); return sum(co*sp.diff(f, x, m[0]) for m, co in zip(P.monoms(), P.coeffs()))
def evo(an, f):
    return sp.diff(f, tt) - op_poly(an, f)
for name, terms in [("AD", [-c*xi, D*xi**2]), ("tre termini", [D*xi**2, -c*xi, -lam])]:
    a = sum(terms); g = sp.expand(sp.prod([a - an for an in terms]))
    u = sp.exp(a.subs(xi, z)*tt + z*x)
    Qu = u
    for an in terms: Qu = evo(an, Qu)
    chk(f"T2a {name}: Q(d)u = g(d_x)u sui modi", sp.simplify(Qu - op_poly(g, u)) == 0)
    K = sp.degree(g, xi); chk(f"T2b {name}: K = deg g = sum deg(a-a_n)", K == sum(sp.degree(sp.expand(a - an), xi) for an in terms), f"K={K}")
    roots = sp.roots(sp.Poly(g, xi))
    ok = True
    for r in roots:
        mode = sp.exp(a.subs(xi, r)*tt + r*x)
        ok &= any(sp.simplify(evo(an, mode)) == 0 for an in terms)
    chk(f"T2b {name}: ogni modo con g(zeta)=0 sta in qualche D_n", ok, str(list(roots)))
# identita' operatoriale su u generica: Q(d)u - g(d_x)u = combinazione di derivate di (u_t - a(d_x)u)
F = sp.Function('F')(tt, x)
a = D*xi**2 - c*xi
QF = evo(D*xi**2, evo(-c*xi, F)); gF = op_poly(sp.expand((a + c*xi)*(a - D*xi**2)), F)
L = evo(a, F)
diffQ = sp.expand(QF - gF)
# (d_t - a_1)(d_t - a_2) - (a-a_1)(a-a_2) = (d_t - a)(d_t + a - a_1 - a_2) = (d_t - a) d_t  (N=2, a = a_1 + a_2)
chk("T2a AD: Q(d) - g(d_x) = (d_t - a(d_x)) d_t come operatori (quindi = 0 su ker(d_t - a))", sp.simplify(diffQ - sp.expand(sp.diff(L, tt))) == 0)
basis = [sp.Integer(1), x - c*tt, (x - c*tt)**2 + 2*D*tt]
chk("T2b AD: base {1, x-ct, (x-ct)^2+2Dt} risolve u_t = a(d_x)u e u_xxx = 0", all(sp.simplify(evo(a, b)) == 0 and sp.diff(b, x, 3) == 0 for b in basis))
u1 = (x - c*tt)**2 - 2*D/c*(x - c*tt); u2 = 2*D/c*x
chk("T2b AD: scomposizione esplicita in D_1 + D_2", sp.simplify(evo(-c*xi, u1)) == 0 and sp.simplify(evo(D*xi**2, u2)) == 0 and sp.simplify(u1 + u2 - basis[2]) == 0)
chk("T2b AD: la componente in D_1 NON sta in Sol(J_1)=ker(d_t+c d_x) cap ker d_x^2 (serve F5)", sp.diff(u1, x, 2) != 0)
GJ = sp.groebner([tau - D*xi**2 + c*xi, xi**3], tau, xi, order='lex')
G1 = sp.groebner([tau + c*xi, xi**2], tau, xi, order='lex'); G2 = sp.groebner([tau - D*xi**2, xi], tau, xi, order='lex')
chk("T2b AD: xi^2 in J_1 cap J_2 ma non in J (J != J_1 cap J_2)", GJ.reduce(xi**2)[1] != 0 and G1.reduce(xi**2)[1] == 0 and G2.reduce(xi**2)[1] == 0)
chk("T2c AD: modo generico zeta=1 ha g(1) = -cD != 0 (E^perp != 0)", sp.expand((D*xi**2*(-c*xi)).subs(xi, 1)) == -c*D)

print("== P2-T5 (MCA) ==")
def mca_instance(n=8, d1=3, d2=3, seed=0, adapted=False):
    r = np.random.default_rng(seed)
    e = r.standard_normal(n); e /= np.linalg.norm(e)
    X = r.standard_normal((n, d1-1)); Y = r.standard_normal((n, d2-1))
    X -= np.outer(e, e @ X); Y -= np.outer(e, e @ Y)
    if adapted:
        B1 = np.hstack([e[:, None], orth(X)]); B2 = np.hstack([e[:, None], orth(Y)])
    else:
        B1 = orth(np.hstack([e[:, None], X])); B2 = orth(np.hstack([e[:, None], Y]))
        B1 = B1 @ np.linalg.qr(r.standard_normal((d1, d1)))[0]; B2 = B2 @ np.linalg.qr(r.standard_normal((d2, d2)))[0]
    return e, B1, B2
def fz(zs, u1, u2, e, B1, B2):
    return np.array([np.abs(B1.T @ (u1 + s*e)).sum() + np.abs(B2.T @ (u2 - s*e)).sum() for s in zs])
def argmin_f(u1, u2, e, B1, B2):
    bp = []
    c1 = B1.T @ e; c2 = B2.T @ e
    for cc, uu in ((c1, B1.T @ u1), (c2, -(B2.T @ u2))):
        for ci, ui in zip(cc, uu):
            if abs(ci) > 1e-14: bp.append(-ui/ci)
    bp = np.array(bp + [0.0]); vals = fz(bp, u1, u2, e, B1, B2); return bp[np.argmin(vals)], vals.min(), bp, vals
okii = True; okiii = True; cnt = 0; nnsp = 0
for seed in range(300):
    e, B1, B2 = mca_instance(seed=seed)
    L1 = [0]; L2 = [1]
    G = B1.T @ B2   # G[i,j] = <phi1_i, phi2_j>
    kappa = max(np.abs(G[L1, :]).sum(axis=0).max(), np.abs(G[:, L2]).sum(axis=1).max())
    r = np.random.default_rng(1000 + seed)
    a1 = np.zeros(3); a1[L1] = r.standard_normal(1); a1 += 0.01*r.standard_normal(3)
    a2 = np.zeros(3); a2[L2] = r.standard_normal(1); a2 += 0.01*r.standard_normal(3)
    u1 = B1 @ a1; u2 = B2 @ a2
    delta = np.abs(np.delete(a1, L1)).sum() + np.abs(np.delete(a2, L2)).sum()
    s, fmin, bp, vals = argmin_f(u1, u2, e, B1, B2)
    if kappa < 0.5:
        cnt += 1
        for sb, vb in zip(bp, vals):
            if vb <= fmin + 1e-12:
                okii &= 2*abs(sb) <= 2*delta/(1 - 2*kappa) + 1e-10
    c1 = B1.T @ e; c2 = B2.T @ e
    nsp = np.abs(c1[L1]).sum() + np.abs(c2[L2]).sum() < np.abs(np.delete(c1, L1)).sum() + np.abs(np.delete(c2, L2)).sum()
    b1 = np.zeros(3); b1[L1] = r.standard_normal(1); b2 = np.zeros(3); b2[L2] = r.standard_normal(1)
    v1 = B1 @ b1; v2 = B2 @ b2
    s2, fm2, bp2, vals2 = argmin_f(v1, v2, e, B1, B2)
    f0 = fz([0.0], v1, v2, e, B1, B2)[0]
    if nsp:
        nnsp += 1
        okiii &= (f0 <= fm2 + 1e-10) and all(abs(sb) < 1e-9 for sb, vb in zip(bp2, vals2) if vb <= fm2 + 1e-10)
    else:
        w1 = -B1 @ np.where(np.isin(range(3), L1), c1, 0); w2 = B2 @ np.where(np.isin(range(3), L2), c2, 0)
        okiii &= fz([1.0], w1, w2, e, B1, B2)[0] <= fz([0.0], w1, w2, e, B1, B2)[0] + 1e-12
chk("T5ii stima 2delta/(1-2kappa) su tutte le istanze con kappa<1/2", okii and cnt > 0, f"istanze con kappa<1/2: {cnt}/300")
chk("T5iii NSP sul gauge => unicita'; NSP falsa => controesempio della prova", okiii, f"istanze con NSP: {nnsp}/300")
e, B1, B2 = mca_instance(seed=7, adapted=True)
c1 = B1.T @ e; c2 = B2.T @ e
chk("T5iv basi adattate: Phi_j^* z concentrato sull'indice di eps", np.allclose(c1, [1, 0, 0]) and np.allclose(c2, [1, 0, 0]))
L1, L2 = [1], [2]
nsp_ok = abs(c1[L1]).sum() + abs(c2[L2]).sum() < abs(np.delete(c1, L1)).sum() + abs(np.delete(c2, L2)).sum()
L1b = [0, 1]
nsp_bad = abs(c1[L1b]).sum() + abs(c2[L2]).sum() < abs(np.delete(c1, L1b)).sum() + abs(np.delete(c2, L2)).sum()
chk("T5iv NSP vale iff eps fuori dai grappoli", nsp_ok and not nsp_bad)
u1 = B1 @ np.array([0, 1.3, -0.4]); u2 = B2 @ np.array([0, 0.7, 2.0])
zs = np.linspace(-1, 1, 41)
chk("T5iv f(z) = f(0) + 2|z| per u_j ortogonali a I", np.allclose(fz(zs, u1, u2, e, B1, B2), fz([0.0], u1, u2, e, B1, B2)[0] + 2*np.abs(zs)))

print("== P2-P7: ortogonalita' in H^1 su (0,1)x(0,2) ==")
xx, ss = sp.symbols('x s', real=True)
def ip_H1(f, g):
    f = sp.sympify(f); g = sp.sympify(g)
    return sp.integrate(f*g + sp.diff(f, ss)*sp.diff(g, ss) + sp.diff(f, xx)*sp.diff(g, xx), (ss, 0, 1), (xx, 0, 2))
A = ss**3 - sp.Rational(1, 4); Bf = xx**2 - sp.Rational(4, 3)
chk("P7 <A(t)x1, 1xB(x)>_{H^1} = int A * int B (=0 se una media e' nulla)", ip_H1(A, Bf) == 0 and ip_H1(A, 1) == 0 and ip_H1(ss, xx) == sp.integrate(ss, (ss, 0, 1))*sp.integrate(xx, (xx, 0, 2)))

print("== P2-P2: esempio R1 ==")
X = sp.symbols('X', real=True)
f = sp.exp(X); basis = [sp.Integer(1), X]
Gm = sp.Matrix(2, 2, lambda i, j: sp.integrate(basis[i]*basis[j], (X, 0, 1)))
bv = sp.Matrix([sp.integrate(b*f, (X, 0, 1)) for b in basis])
co = Gm.LUsolve(bv); proj = sum(co[i]*basis[i] for i in range(2))
res2 = sp.simplify(sp.integrate((f - proj)**2, (X, 0, 1)))
chk("P2 ||P^perp e^x||^2_{L2(0,1)} = 20e - 7e^2/2 - 57/2", sp.simplify(res2 - (20*sp.E - sp.Rational(7, 2)*sp.E**2 - sp.Rational(57, 2))) == 0, f"{float(res2):.6e}")

print("== P2-P4(b) ==")
N = 10000
k = np.arange(1, N+1); wv = 1/k; wv /= np.linalg.norm(wv)
Ew = wv/k
y = wv*k; y /= np.linalg.norm(y)
dist = abs(Ew @ y)
chk("P4b dist(Ew, EM) ~ N^{-1/2} (troncamento N=10^4)", dist < 0.02, f"{dist:.4f}")

print("== P2-P5(b): AD ==")
kap = np.linspace(-50, 50, 2001); tg = np.linspace(0, 3, 61)
mx = max(abs((np.exp(-1j*1.3*tv*kap) - 1)*(np.exp(-0.7*kap**2*tv) - 1)).max() for tv in tg)
chk("P5b AD: |e_{>=2}(z)| = |z1 z2| <= 2", mx <= 2 + 1e-12, f"max {mx:.4f}")
bb = sp.symbols('b1:4', nonnegative=True)
e2 = sp.expand(sp.prod([1 + b for b in bb]) - 1 - sum(bb))
chk("P5 e_{>=2} ha coefficienti >= 0 (N=3)", all(cf > 0 for cf in sp.Poly(e2, *bb).coeffs()))

print("== P2-P6: Vandermonde ==")
okv = True
for dd in range(2, 6):
    for trial in range(5):
        r = np.random.default_rng(100*dd + trial)
        nodes = [sp.Rational(int(v), 7) for v in r.choice(np.arange(-20, 21), dd+1, replace=False)]
        V = sp.Matrix(dd+1, dd+1, lambda i, j: nodes[i]**j); Vi = V.inv()
        n11 = max(sum(abs(Vi[i, kk]) for i in range(dd+1)) for kk in range(dd+1))
        ub = max(sp.prod([(1 + abs(nodes[j]))/abs(nodes[kk] - nodes[j]) for j in range(dd+1) if j != kk]) for kk in range(dd+1))
        lb = max(sp.prod([1/abs(nodes[kk] - nodes[j]) for j in range(dd+1) if j != kk]) for kk in range(dd+1))
        okv &= bool(lb <= n11 <= ub)
    h = sp.Rational(1, 3); nodes = [1 + j*h for j in range(dd+1)]
    Vi = sp.Matrix(dd+1, dd+1, lambda i, j: nodes[i]**j).inv()
    n11 = max(sum(abs(Vi[i, kk]) for i in range(dd+1)) for kk in range(dd+1))
    okv &= bool(n11 >= h**(-dd)/(sp.factorial(dd//2)*sp.factorial(dd - dd//2)))
chk("P6 (a),(b),(c) su nodi razionali casuali ed equispaziati, d=2..5", okv)

print("== P2-T4: illustrazione (Tikhonov, c_F = 1): L_alpha = ||R_alpha|| -> inf ==")
lams = np.array(lam_min)
La = [np.sqrt(lams/(lams + a)**2).max() for a in [1e-1, 1e-2, 1e-3, 1e-4, 1e-5]]
chk("T4 costanti di Lipschitz crescenti al decrescere di alpha", all(np.diff(La) > 0), str([f"{v:.1f}" for v in La]))
# T4 versione non lineare: selezione esatta sigma qualsiasi ha Lip >= ||S^+||
Q1, Q2 = rand_pair(6, 3, 3, 1)
S = np.hstack([Q1, Q2]); Sp = np.linalg.pinv(S)
uu = S @ rng.standard_normal(6)
kerv = np.linalg.svd(S)[2][-1]
sel = Sp @ uu + 0.7*kerv   # altra rappresentazione esatta
chk("T4-1 ogni rappresentazione esatta ha norma >= ||S^+ u||", np.linalg.norm(sel) >= np.linalg.norm(Sp @ uu) - 1e-12 and np.allclose(S @ sel, uu))

n_ok = sum(o for _, o in RES); print(f"\nESITO: {n_ok}/{len(RES)} OK")
