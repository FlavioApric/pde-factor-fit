# Verifica (non metodo) per P2-C2 (N >= 3 sottospazi, gamma_N) e per il fix T4-1.
# Esecuzione: D:\ProblemaBase\.venv\Scripts\python.exe -I p2_c2.py
import sympy as sp, numpy as np, itertools
ok = 0; tot = 0
def chk(name, cond):
    global ok, tot
    tot += 1; ok += bool(cond); print(("PASS " if cond else "FAIL ") + name)

def gamma(Sm, tol=1e-10):
    ev = np.linalg.eigvalsh(Sm.T @ Sm)
    nz = ev[ev > tol * max(1.0, ev.max())]
    return nz.min(), ev

# --- 1. Controesempio (non sufficienza): tre rette quasi complanari in R^3 -------------
e = sp.symbols('epsilon', positive=True)
v = [sp.Matrix([sp.cos(e)*sp.cos(2*sp.pi*k/3), sp.cos(e)*sp.sin(2*sp.pi*k/3), sp.sin(e)]) for k in range(3)]
G = sp.simplify(sp.Matrix(3, 3, lambda i, j: (v[i].T*v[j])[0]))
cc = -sp.cos(e)**2/2 + sp.sin(e)**2
chk("1a Gram fuori diagonale = -cos^2/2 + sin^2 (tutte le coppie)",
    all(sp.simplify(G[i, j]-cc) == 0 for i, j in [(0, 1), (0, 2), (1, 2)]))
S = sp.Matrix.hstack(*v)
chk("1b S S^T = diag(3/2 cos^2, 3/2 cos^2, 3 sin^2)",
    sp.simplify(S*S.T - sp.diag(sp.Rational(3, 2)*sp.cos(e)**2, sp.Rational(3, 2)*sp.cos(e)**2, 3*sp.sin(e)**2)) == sp.zeros(3))
chk("1c det S^T S = (9/4) cos^4 * 3 sin^2 > 0: ker S = 0 per eps in (0,pi/2)",
    sp.simplify((S.T*S).det() - sp.Rational(27, 4)*sp.cos(e)**4*sp.sin(e)**2) == 0)
# per tan^2 eps <= 1/2: gamma_3 = 3 sin^2 eps; |c| < 1/2
for ev in [sp.Rational(1, 2), sp.Rational(1, 10), sp.Rational(1, 1000)]:
    lam = min(sp.N(x, 40) for x in (S.T*S).subs(e, ev).eigenvals())
    cF = abs(sp.N(cc.subs(e, ev), 40))
    chk(f"1d eps={ev}: gamma_3 = 3 sin^2 eps = {float(lam):.3e}, c_F a coppie = {float(cF):.4f} < 1/2",
        abs(lam - 3*sp.sin(ev)**2) < 1e-30 and cF < sp.Rational(1, 2))
# |c(eps)| < 1/2 per ogni eps in (0, 1/2]: c = -1/2 + (3/2) sin^2 eps in (-1/2, 0)
chk("1e c(eps) = -1/2 + (3/2) sin^2 eps (quindi |c| < 1/2 per sin^2 eps < 2/3)",
    sp.simplify(cc - (-sp.Rational(1, 2) + sp.Rational(3, 2)*sp.sin(e)**2)) == 0)

# --- 2. Somma diretta ortogonale di blocchi eps_k = 2^-k (troncata a K blocchi) -------------
def blocks(K):
    H = 3*K
    B = [np.zeros((H, K)) for _ in range(3)]
    for k in range(K):
        ek = 2.0**-(k+1)
        for j in range(3):
            B[j][3*k:3*k+3, k] = [np.cos(ek)*np.cos(2*np.pi*j/3), np.cos(ek)*np.sin(2*np.pi*j/3), np.sin(ek)]
    return B
for K in [5, 12, 20]:
    B = blocks(K)
    cF = max(np.linalg.norm(B[i].T @ B[j], 2) for i, j in [(0, 1), (0, 2), (1, 2)])   # = ||P_i P_j|| (basi o.n.)
    Sf = np.hstack(B)
    lam = np.linalg.eigvalsh(Sf.T @ Sf)
    chk(f"2 K={K} blocchi: c_F a coppie = {cF:.4f} <= 1/2, ker S = 0 (lam_min>0), gamma_3 = {lam.min():.2e} = 3 sin^2(2^-K)",
        cF <= 0.5 and lam.min() > 0 and abs(lam.min() - 3*np.sin(2.0**-K)**2) < 1e-12)

# --- 3. Non necessita': H_1, H_2 con c_F -> 1, H_3 = H (blocchi in R^2) --------------------
ok3 = True; g12 = []; g123 = []
for k in range(1, 13):
    th = 2.0**-k
    a = np.array([[1.0], [0.0]]); b = np.array([[np.cos(th)], [np.sin(th)]])
    g12.append(gamma(np.hstack([a, b]))[0])
    g123.append(gamma(np.hstack([a, b, np.eye(2)]))[0])
chk(f"3 coppia (1,2): gamma_2 = 1-cos(2^-k) = {min(g12):.2e} -> 0 (somma non chiusa); terna: inf gamma_3 = {min(g123):.4f} >= 1 (chiusa)",
    all(abs(g12[k-1] - 2*np.sin(2.0**-k/2)**2) < 1e-6*2*np.sin(2.0**-k/2)**2 for k in range(1, 13)) and min(g12) < 1e-6 and min(g123) >= 1 - 1e-12)

# --- 4. Stessi c_F a coppie, gamma_3 diversi (nessuna formula nei soli c_F a coppie) ------
Gp = sp.Matrix([[1, sp.Rational(1, 2), sp.Rational(1, 2)], [sp.Rational(1, 2), 1, sp.Rational(1, 2)], [sp.Rational(1, 2), sp.Rational(1, 2), 1]])
Gm = sp.Matrix([[1, -sp.Rational(1, 2), -sp.Rational(1, 2)], [-sp.Rational(1, 2), 1, -sp.Rational(1, 2)], [-sp.Rational(1, 2), -sp.Rational(1, 2), 1]])
evp = Gp.eigenvals(); evm = Gm.eigenvals()
chk(f"4a Gram (+1/2): autovalori {evp} -> gamma_3 = 1/2 (rette indipendenti in R^3)", evp == {2: 1, sp.Rational(1, 2): 2})
chk(f"4b Gram (-1/2) (rette a 120 gradi in R^2): autovalori {evm} -> gamma_3 = 3/2", evm == {0: 1, sp.Rational(3, 2): 2})
# realizzazione esplicita di 4b
w = [sp.Matrix([sp.cos(2*sp.pi*k/3), sp.sin(2*sp.pi*k/3)]) for k in range(3)]
chk("4c rette a 120 gradi: Gram = matrice (-1/2)", sp.simplify(sp.Matrix(3, 3, lambda i, j: (w[i].T*w[j])[0]) - Gm) == sp.zeros(3))
# Gram (+1/2) e' di Gram (definita positiva): Cholesky esiste
L = Gp.cholesky()
chk("4d Gram (+1/2) realizzata (Cholesky L L^T = G, colonne unitarie)", sp.simplify(L*L.T - Gp) == sp.zeros(3))

# --- 5. Condizione sufficiente: gamma_N >= 1 - ||C|| >= 1 - max_i sum_j c_ij (casi non banali) ---
rng = np.random.default_rng(7)
for trial in range(8):
    N = [3, 4, 5][trial % 3]; d = 2; Hd = 40
    Q = np.linalg.qr(rng.standard_normal((Hd, Hd)))[0]
    bases = []
    for j in range(N):
        X = Q[:, d*j:d*j+d] + 0.12*rng.standard_normal((Hd, d))   # quasi ortogonali
        bases.append(np.linalg.qr(X)[0])
    C = np.zeros((N, N))
    for i, j in itertools.permutations(range(N), 2):
        C[i, j] = np.linalg.norm(bases[i].T @ bases[j], 2)
    nC = np.abs(np.linalg.eigvalsh(C)).max(); rs = C.sum(1).max()
    Sf = np.hstack(bases); ev = np.linalg.eigvalsh(Sf.T @ Sf)
    chk(f"5 N={N}: gamma_N = {ev.min():.4f} >= 1-||C|| = {1-nC:.4f} >= 1-maxrow = {1-rs:.4f} > 0; ||S||^2 = {ev.max():.4f} <= 1+||C||",
        ev.min() >= 1-nC-1e-12 and 1-nC >= 1-rs-1e-12 and 1-nC > 0 and ev.max() <= 1+nC+1e-12)

# --- 6. (b),(c),(d) per N = 3 con ker S != 0 (sottospazi di R^6 di dim 2,2,3) --------------
for trial in range(4):
    bases = [np.linalg.qr(rng.standard_normal((6, dd)))[0] for dd in (2, 2, 3)]
    Sf = np.hstack(bases); T = Sf.T @ Sf
    lam, U = np.linalg.eigh(T)
    tol = 1e-10
    ker = (lam < tol).sum(); g = lam[lam >= tol].min()
    Sp = np.linalg.pinv(Sf)
    nSp = np.linalg.norm(Sp, 2)
    sups = []
    for al in np.logspace(-6, 1, 200):
        Ra = np.linalg.solve(T + al*np.eye(7), Sf.T)
        sups.append(np.linalg.norm(Ra, 2))
    vmin = U[:, np.argmin(np.where(lam >= tol, lam, np.inf))]
    u = Sf @ vmin; om_dag = Sp @ u
    al = 0.37
    om_al = np.linalg.solve(T + al*np.eye(7), Sf.T @ u)
    rate = np.linalg.norm(om_al - om_dag) / np.linalg.norm(om_dag)
    # generic u in the sum: bound
    ug = Sf @ rng.standard_normal(7); od = Sp @ ug
    rg = np.linalg.norm(np.linalg.solve(T + al*np.eye(7), Sf.T @ ug) - od) / np.linalg.norm(od)
    chk(f"6 prova {trial}: dim ker S = {ker} (=1), ||S^+|| = gamma^-1/2 ({nSp:.4f}), sup_a||R_a|| = {max(sups):.4f} <= gamma^-1/2, tasso = a/(g+a) sull'autovettore, <= in generale",
        ker == 1 and abs(nSp - g**-0.5) < 1e-8 and max(sups) <= g**-0.5 + 1e-9 and max(sups) > 0.99*g**-0.5
        and abs(rate - al/(g+al)) < 1e-9 and rg <= al/(g+al) + 1e-12)

# --- 7. gamma_3 = 0 (blocchi del punto 2, K grande): sup_a ||R_a|| cresce come gamma^-1/2/2 ---
B = blocks(18); Sf = np.hstack(B); T = Sf.T @ Sf
lamT = np.linalg.eigvalsh(T); lk = lamT.min()
Ra = np.linalg.solve(T + lk*np.eye(T.shape[0]), Sf.T)
chk(f"7 gamma_3 -> 0: ||R_(lambda_k)|| = {np.linalg.norm(Ra,2):.1f} >= 1/(2 sqrt(lambda_k)) = {0.5/np.sqrt(lk):.1f}",
    np.linalg.norm(Ra, 2) >= 0.5/np.sqrt(lk) - 1e-6)

# --- 8. Fix T4-1: ogni preimmagine ha norma >= ||S^+ u||; selezione non lineare ----------
bases = [np.linalg.qr(rng.standard_normal((5, dd)))[0] for dd in (2, 2, 2)]
Sf = np.hstack(bases); Sp = np.linalg.pinv(Sf)
_, _, Vt = np.linalg.svd(Sf); Kb = Vt[5:].T            # base di ker S (dim 1)
def sigma(u):                                          # selezione esatta non lineare
    return Sp @ u + np.tanh(u[0])*3.0*Kb[:, 0]
okp = True; ratios = []
for _ in range(2000):
    u = Sf @ rng.standard_normal(6)
    om = Sp @ u + Kb @ rng.standard_normal(Kb.shape[1])   # preimmagine qualsiasi
    okp &= np.linalg.norm(om) >= np.linalg.norm(Sp @ u) - 1e-12
    okp &= np.allclose(Sf @ sigma(u), u)
    w2 = Sf @ rng.standard_normal(6)
    ratios.append(np.linalg.norm(sigma(u) - sigma(w2)) / np.linalg.norm(u - w2))
# su u = S v_min: ||sigma(u)-sigma(0)|| >= ||S^+ u|| = ||S^+|| ||u||
lam, U = np.linalg.eigh(Sf.T @ Sf); g = lam[lam > 1e-10].min(); vmin = U[:, np.where(lam > 1e-10)[0][np.argmin(lam[lam > 1e-10])]]
u = Sf @ vmin
r0 = np.linalg.norm(sigma(u) - sigma(0*u)) / np.linalg.norm(u)
chk(f"8 T4-1: ogni preimmagine >= ||S^+u||; selezione non lineare esatta; Lip(sigma) >= {r0:.4f} >= ||S^+|| = {g**-0.5:.4f}",
    okp and r0 >= g**-0.5 - 1e-9)

# --- 9. N = 2: gamma_2 = 1 - c_F (coerenza con P2-T3) ---------------------------------
th = sp.Rational(3, 10)
a = sp.Matrix([1, 0, 0]); b = sp.Matrix([sp.cos(th), sp.sin(th), 0])
G2 = sp.Matrix.hstack(a, b).T*sp.Matrix.hstack(a, b)
chk("9 N=2: gamma_2 = 1 - cos(theta) = 1 - c_F", min(sp.N(x, 30) for x in G2.eigenvals()) - sp.N(1 - sp.cos(th), 30) < 1e-25)

print(f"\nTOTALE: {ok}/{tot} PASS")
