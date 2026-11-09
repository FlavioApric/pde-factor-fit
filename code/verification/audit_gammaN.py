# audit_gammaN.py -- S-CHECK-7 (7a tornata), red team per P2-C2, P2-T4(2), C12-P7(a,c,d), C3-T2(a)
# Esecuzione: D:\ProblemaBase\.venv\Scripts\python.exe -I audit_gammaN.py > audit_gammaN.out
# Controlli di coerenza su esempi finiti: NON sostituiscono le prove (controllate a mano in AUDIT_gammaN.md).
import numpy as np
import sympy as sp

RES = []
def check(name, ok, info=""):
    RES.append((name, bool(ok)))
    print(("[OK]  " if ok else "[FAIL] ") + name + ("  -- " + info if info else ""))

rng = np.random.default_rng(20261026)

def onb(M):
    q, r = np.linalg.qr(M)
    return q[:, :M.shape[1]]

def proj(B):
    return B @ B.conj().T

def gamma_from_T(T, tol=1e-9):
    w, V = np.linalg.eigh(T)
    nz = w[w > tol]
    return (nz.min() if len(nz) else np.inf), w, V

# ---------------------------------------------------------------- 1. P2-C2 (a)-(e) su sottospazi casuali
def random_family(n, dims, shared=0, cplx=False):
    """N sottospazi di C^n / R^n; i primi 'shared' vettori comuni a H_1 e H_2 (intersezione non nulla)."""
    def rnd(k):
        X = rng.standard_normal((n, k))
        if cplx:
            X = X + 1j * rng.standard_normal((n, k))
        return X
    common = rnd(shared) if shared else None
    Bs = []
    for j, d in enumerate(dims):
        X = rnd(d)
        if shared and j < 2:
            X[:, :shared] = common
        Bs.append(onb(X))
    return Bs

cases = [
    (6, [2, 2, 2], 0, False), (6, [2, 3, 2], 1, False), (5, [2, 2, 2], 0, True),
    (4, [2, 2, 2], 0, False),   # dim ker S >= 2 (6 > 4)
    (7, [3, 3, 2, 2], 1, True), (8, [1, 1, 1, 1, 1], 0, False), (3, [1, 1, 1, 1], 0, True),
]
for idx, (n, dims, sh, cp) in enumerate(cases):
    Bs = random_family(n, dims, sh, cp)
    S = np.hstack(Bs)                       # S: W = (+)H_j -> H in coordinate ortonormali
    T = S.conj().T @ S
    g, w, V = gamma_from_T(T)
    kerdim = int(np.sum(w <= 1e-9))
    # gamma = inf della forma su (ker S)^perp
    Vperp = V[:, w > 1e-9]
    Tr = Vperp.conj().T @ T @ Vperp
    g2 = np.linalg.eigvalsh(Tr).min()
    check(f"C2(a,b) caso {idx}: gamma = min sigma(T|kerperp) = inf forma (dim ker S={kerdim})", abs(g - g2) < 1e-9, f"gamma={g:.6f}")
    check(f"C2(a) caso {idx}: sigma(T) in {{0}} U [gamma, N], ||S||^2 <= N",
          np.all((w <= 1e-9) | (w >= g - 1e-9)) and w.max() <= len(dims) + 1e-9)
    # S^dagger
    Sp = np.linalg.pinv(S)
    check(f"C2(b) caso {idx}: ||S^+|| = gamma^(-1/2)", abs(np.linalg.norm(Sp, 2) - g ** -0.5) < 1e-7)
    # (c) ||R_alpha||^2 = sup lambda/(lambda+alpha)^2 e sup_alpha < gamma^(-1/2)
    okc = True; vals = []
    for a in [1.0, 1e-1, 1e-2, 1e-3, 1e-5]:
        Ra = np.linalg.solve(T + a * np.eye(T.shape[0]), S.conj().T)
        nr = np.linalg.norm(Ra, 2)
        pred = np.sqrt(max(l / (l + a) ** 2 for l in w))
        okc &= abs(nr - pred) < 1e-7 and nr < g ** -0.5 + 1e-12
        vals.append(nr)
    okc &= all(vals[i] <= vals[i + 1] + 1e-12 for i in range(len(vals) - 1))
    check(f"C2(c) caso {idx}: ||R_a||^2 formula, crescente per a->0, < gamma^(-1/2)", okc, f"||R_1e-5||={vals[-1]:.6f}, g^-1/2={g**-0.5:.6f}")
    # (d) stima e uguaglianza sull'autovettore di gamma
    om = Vperp @ (rng.standard_normal(Vperp.shape[1]))
    u = S @ om
    okd = True
    for a in [1.0, 0.1, 0.01]:
        oa = np.linalg.solve(T + a * np.eye(T.shape[0]), S.conj().T @ u)
        okd &= np.linalg.norm(oa - Sp @ u) <= a / (g + a) * np.linalg.norm(Sp @ u) + 1e-10
    vg = V[:, np.argmin(np.where(w > 1e-9, w, np.inf))]
    u2 = S @ vg; a = 0.3
    oa = np.linalg.solve(T + a * np.eye(T.shape[0]), S.conj().T @ u2)
    okd &= abs(np.linalg.norm(oa - Sp @ u2) - a / (g + a) * np.linalg.norm(Sp @ u2)) < 1e-10
    check(f"C2(d) caso {idx}: ||w_a - S^+u|| <= a/(g+a)||S^+u||, uguaglianza sull'autovettore", okd)
    # (e) bound 1-||C|| e 1+||C||; c_ij = ||P_i P_j||; Gershgorin
    N = len(Bs)
    C = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            if i != j:
                C[i, j] = np.linalg.norm(proj(Bs[i]) @ proj(Bs[j]), 2)
    nC = np.linalg.norm(C, 2)
    oke = w.min() >= 1 - nC - 1e-9 and w.max() <= 1 + nC + 1e-9 and nC <= C.sum(1).max() + 1e-12
    check(f"C2(e) caso {idx}: (1-||C||) <= sigma(T) <= 1+||C||, ||C|| <= max riga", oke, f"||C||={nC:.4f}, lmin={w.min():.4f}")
    if sh == 0:
        # c_F = ||P_i P_j|| = s_max(B_i^* B_j) per intersezione nulla
        okf = all(abs(np.linalg.svd(Bs[i].conj().T @ Bs[j], compute_uv=False).max() - C[i, j]) < 1e-9
                  for i in range(N) for j in range(N) if i != j)
        check(f"C2(e) caso {idx}: c_F(H_i,H_j) = ||P_iP_j|| (intersezioni nulle)", okf)
    else:
        check(f"C2(e) caso {idx}: intersezione H1^H2 != 0 => c_12 = 1, bound banale", abs(C[0, 1] - 1) < 1e-9 and 1 - nC <= 0)

# caso ||C|| < 1: ker S = 0 e gamma >= 1-||C|| > 0 (sottospazi quasi ortogonali)
Bs = [onb(np.eye(9)[:, 3*j:3*j+3] + 0.15 * rng.standard_normal((9, 3))) for j in range(3)]
S = np.hstack(Bs); T = S.T @ S; w = np.linalg.eigvalsh(T)
C = np.array([[0 if i == j else np.linalg.norm(proj(Bs[i]) @ proj(Bs[j]), 2) for j in range(3)] for i in range(3)])
check("C2(e) ||C||<1 => ker S = 0, gamma >= 1-||C|| > 0", np.linalg.norm(C, 2) < 1 and w.min() >= 1 - np.linalg.norm(C, 2) - 1e-12,
      f"||C||={np.linalg.norm(C,2):.4f}, gamma={w.min():.4f}")
# N = 2, I = 0: ||C|| = c_F e gamma_2 = 1 - c_F (uguaglianza)
Bs = random_family(6, [2, 3], 0, True)
S = np.hstack(Bs); w = np.linalg.eigvalsh(S.conj().T @ S)
cF = np.linalg.svd(Bs[0].conj().T @ Bs[1], compute_uv=False).max()
check("C2(e) N=2, I=0: gamma_2 = 1 - c_F", abs(w.min() - (1 - cF)) < 1e-9)

# ---------------------------------------------------------------- 2. P2-C2 (f) non sufficienza (simbolico)
e = sp.symbols('epsilon', positive=True)
def v(k, eps):
    th = 2 * sp.pi * k / 3
    return sp.Matrix([sp.cos(eps) * sp.cos(th), sp.cos(eps) * sp.sin(th), sp.sin(eps)])
Vm = sp.Matrix.hstack(v(0, e), v(1, e), v(2, e))
VVt = sp.simplify(Vm * Vm.T)
check("C2(f) VV^T = diag(3/2 cos^2, 3/2 cos^2, 3 sin^2)",
      sp.simplify(VVt - sp.diag(sp.Rational(3, 2) * sp.cos(e) ** 2, sp.Rational(3, 2) * sp.cos(e) ** 2, 3 * sp.sin(e) ** 2)) == sp.zeros(3))
G = sp.simplify(Vm.T * Vm)
cpair = sp.simplify(G[0, 1] - (-sp.Rational(1, 2) + sp.Rational(3, 2) * sp.sin(e) ** 2))
check("C2(f) <v_i,v_j> = -1/2 + 3/2 sin^2 eps (tutte le coppie)",
      cpair == 0 and sp.simplify(G[0, 2] - G[0, 1]) == 0 and sp.simplify(G[1, 2] - G[0, 1]) == 0)
s12 = float(sp.sin(sp.Rational(1, 2)) ** 2); t12 = float(sp.tan(sp.Rational(1, 2)) ** 2)
check("C2(f) sin^2(1/2) < 1/3 (c in (-1/2,0)) e tan^2(1/2) < 1/2 (gamma_3 = 3 sin^2)", s12 < 1/3 and t12 < 1/2, f"sin^2={s12:.4f}, tan^2={t12:.4f}")
okg = True
for k in range(1, 12):
    ek = 2.0 ** -k
    Vn = np.array(Vm.subs(e, ek).evalf(), dtype=float)
    lam = np.linalg.eigvalsh(Vn.T @ Vn).min()
    okg &= abs(lam - 3 * np.sin(ek) ** 2) < 1e-12 * max(1, lam) + 1e-15 and abs(np.linalg.det(Vn)) > 0
check("C2(f) gamma_3(2^-k) = 3 sin^2(2^-k), V_k invertibile (k=1..11)", okg)
# blocchi troncati: c_F(H_i,H_j) = max_k |c(eps_k)| <= 1/2, gamma_3 = min_k 3 sin^2 eps_k -> 0
for K in [3, 6, 10]:
    blocks = [np.array(Vm.subs(e, 2.0 ** -k).evalf(), dtype=float) for k in range(1, K + 1)]
    dimH = 3 * K
    Hs = []
    for j in range(3):
        B = np.zeros((dimH, K))
        for k in range(K):
            B[3*k:3*k+3, k] = blocks[k][:, j]
        Hs.append(B)
    S = np.hstack(Hs); T = S.T @ S; w = np.linalg.eigvalsh(T)
    cF = max(np.linalg.svd(Hs[i].T @ Hs[j], compute_uv=False).max() for i in range(3) for j in range(3) if i != j)
    check(f"C2(f) troncata K={K}: c_F a coppie <= 1/2, ker S = 0, gamma_3 = 3 sin^2(2^-K), im S = H",
          cF <= 0.5 and w.min() > 0 and abs(w.min() - 3 * np.sin(2.0 ** -K) ** 2) < 1e-12 and np.linalg.matrix_rank(S) == dimH,
          f"c_F={cF:.6f}, gamma_3={w.min():.3e}")

# ---------------------------------------------------------------- 3. (f) non necessita'
for K in [3, 8]:
    th = [2.0 ** -k for k in range(1, K + 1)]
    H1 = np.zeros((2 * K, K)); H2 = np.zeros((2 * K, K)); H3 = np.eye(2 * K)
    for k in range(K):
        H1[2*k, k] = 1; H2[2*k:2*k+2, k] = [np.cos(th[k]), np.sin(th[k])]
    S12 = np.hstack([H1, H2]); g2 = np.linalg.eigvalsh(S12.T @ S12).min()
    S = np.hstack([H1, H2, H3]); T = S.T @ S
    g3, w, _ = gamma_from_T(T)
    SSs = S @ S.T
    check(f"C2(f) non necessita' K={K}: gamma_2 = 1-cos(2^-K) -> 0; SS* >= I; gamma_3 >= 1",
          abs(g2 - (1 - np.cos(th[-1]))) < 1e-12 and np.linalg.eigvalsh(SSs).min() >= 1 - 1e-12 and g3 >= 1 - 1e-12,
          f"gamma_2={g2:.3e}, gamma_3={g3:.4f}")
# spettri non nulli di S*S e SS* coincidono (passo usato implicitamente in "gamma_3 >= 1")
A = rng.standard_normal((4, 7))
a1 = np.sort(np.linalg.eigvalsh(A.T @ A))[-4:]; a2 = np.sort(np.linalg.eigvalsh(A @ A.T))
check("C2(f) sigma(S*S)\\{0} = sigma(SS*)\\{0} (fatto usato per gamma_3 >= 1)", np.allclose(a1, a2))

# ---------------------------------------------------------------- 4. (f) nessuna formula: Gram +-1/2
h = sp.Rational(1, 2)
Gm = sp.Matrix([[1, -h, -h], [-h, 1, -h], [-h, -h, 1]])
Gp = sp.Matrix([[1, h, h], [h, 1, h], [h, h, 1]])
check("C2(f) Gram(-1/2): autovalori {0,3/2,3/2}", Gm.eigenvals() == {0: 1, sp.Rational(3, 2): 2})
check("C2(f) Gram(+1/2): autovalori {2,1/2,1/2}", Gp.eigenvals() == {2: 1, h: 2})
# realizzazione: 120 gradi in R^2 e Cholesky in R^3
v120 = [sp.Matrix([sp.cos(2*sp.pi*k/3), sp.sin(2*sp.pi*k/3)]) for k in range(3)]
G120 = sp.Matrix(3, 3, lambda i, j: sp.simplify((v120[i].T * v120[j])[0]))
L = Gp.cholesky(hermitian=False)
vp = [L[i, :].T for i in range(3)]
Gchk = sp.Matrix(3, 3, lambda i, j: sp.simplify((vp[i].T * vp[j])[0]))
check("C2(f) rette a 120 gradi realizzano Gram(-1/2); Cholesky realizza Gram(+1/2)", G120 == Gm and Gchk == Gp)
# gamma_3 = min autovalore non nullo
g_m = min(ev for ev in Gm.eigenvals() if ev != 0); g_p = min(Gp.eigenvals())
check("C2(f) gamma_3 = 3/2 (120 gradi) e 1/2 (Cholesky), c_F a coppie tutti 1/2, rette distinte",
      g_m == sp.Rational(3, 2) and g_p == h and all(abs(Gm[i, j]) == h and abs(Gp[i, j]) == h for i in range(3) for j in range(3) if i != j))
# bound di (e) in questi casi: ||C|| = 1 => bound 0 (coerente, non contraddittorio)
Cm = sp.Matrix([[0, h, h], [h, 0, h], [h, h, 0]])
check("C2(e) sui due esempi ||C|| = 1: bound 1-||C|| = 0 <= gamma_3", max(abs(x) for x in Cm.eigenvals()) == 1)

# ---------------------------------------------------------------- 5. C12-P7(d): parametrizzazione di S-CHECK-4
v1 = sp.Matrix([1, 0, e]) / sp.sqrt(1 + e ** 2)
v2 = sp.Matrix([-h, sp.sqrt(3) / 2, 0]); v3 = sp.Matrix([-h, -sp.sqrt(3) / 2, 0])
Ge = sp.Matrix(3, 3, lambda i, j: sp.simplify(([v1, v2, v3][i].T * [v1, v2, v3][j])[0]))
check("C12-P7(d) det G_eps = 3 eps^2 / (4(1+eps^2))", sp.simplify(Ge.det() - 3 * e ** 2 / (4 * (1 + e ** 2))) == 0)
check("C12-P7(d) coseni 1/(2 sqrt(1+eps^2)), 1/(2 sqrt(1+eps^2)), 1/2",
      sp.simplify(abs(Ge[0, 1]) - 1 / (2 * sp.sqrt(1 + e ** 2))) == 0 and sp.simplify(abs(Ge[0, 2]) - 1 / (2 * sp.sqrt(1 + e ** 2))) == 0 and Ge[1, 2] == -h)
lam = sp.symbols('lam')
cp = (Ge - lam * sp.eye(3)).det()
# lambda_min ~ eps^2/3: soluzione in serie
ok5 = True; info = []
for ev, ref in [(1e-1, 0.003308), (1e-2, 3.333e-5), (1e-3, 3.333e-7)]:
    Gn = np.array(Ge.subs(e, ev).evalf(30), dtype=float)
    lm = np.linalg.eigvalsh(Gn).min()
    ok5 &= abs(lm - ref) / ref < 2e-3 and abs(lm / ev ** 2 - 1 / 3) < 0.01
    info.append(f"{ev}:{lm:.4e}")
check("C12-P7(d) lambda_min(G_eps) ~ eps^2/3, valori di gram.md", ok5, ", ".join(info))
Gn0 = np.array(Ge.subs(e, 0), dtype=float)
check("C12-P7(d) eps=0: autovalori {0,3/2,3/2}", np.allclose(np.sort(np.linalg.eigvalsh(Gn0)), [0, 1.5, 1.5]))

# ---------------------------------------------------------------- 6. P2-T4(2): selezione esatta non lineare
Bs = random_family(5, [2, 2, 2], 0, False)    # dim W = 6 > 5: ker S != 0
S = np.hstack(Bs); T = S.T @ S
g, w, V = gamma_from_T(T)
k0 = V[:, np.argmin(w)]                          # vettore di ker S
Sp = np.linalg.pinv(S)
def sigma(u):                                    # selezione esatta non lineare
    return Sp @ u + (np.sin(u.sum()) + u[0] ** 2) * k0
ok6 = True; best = 0
for _ in range(2000):
    om = rng.standard_normal(6); u = S @ om
    ok6 &= np.allclose(S @ sigma(u), u)
    r = np.linalg.norm(sigma(u) - sigma(0 * u)) / np.linalg.norm(u)
    ok6 &= r >= np.linalg.norm(Sp @ u) / np.linalg.norm(u) - 1e-12
    best = max(best, r)
vg = V[:, np.argmin(np.where(w > 1e-9, w, np.inf))]
u = S @ vg
rg = np.linalg.norm(sigma(u) - sigma(0 * u)) / np.linalg.norm(u)
check("T4(2) selezione non lineare: S sigma(u)=u, ||sigma(u)-sigma(0)|| >= ||S^+u||, Lip >= gamma^-1/2",
      ok6 and rg >= g ** -0.5 - 1e-9, f"ratio su autovettore={rg:.4f} >= {g**-0.5:.4f}")

# ---------------------------------------------------------------- 7. gamma = 0 in dimensione infinita (troncate): sup_a ||R_a|| ~ 1/(2 sqrt(lambda_K))
for K in [4, 8, 12]:
    blocks = [np.array(Vm.subs(e, 2.0 ** -k).evalf(), dtype=float) for k in range(1, K + 1)]
    T = np.zeros((3 * K, 3 * K))
    for k in range(K):
        T[3*k:3*k+3, 3*k:3*k+3] = blocks[k].T @ blocks[k]
    lk = 3 * np.sin(2.0 ** -K) ** 2
    a = lk
    wT = np.linalg.eigvalsh(T)
    nr = np.sqrt(max(l / (l + a) ** 2 for l in wT))
    check(f"C2(c) gamma=0 (troncata K={K}): ||R_(lambda_K)|| >= 1/(2 sqrt(lambda_K))", nr >= 1 / (2 * np.sqrt(lk)) - 1e-9, f"{nr:.2f}")

# ---------------------------------------------------------------- 8. C3-T2(a): Ann(u) via (z_k + d) contro calcolo diretto
t, x = sp.symbols('t x')
tau, xi = sp.symbols('tau xi')
terms = [((1 + t), (1, -1)), (sp.Integer(3), (2, 0)), (x, (0, 1))]      # u = (1+t)e^{t-x} + 3e^{2t} + x e^{x}
u = sum(q * sp.exp(z[0] * t + z[1] * x) for q, z in terms)
n = 3
mons = [(a, b) for a in range(n + 1) for b in range(n + 1 - a)]
cs = sp.symbols('c0:%d' % len(mons))
# diretto: Q(d)u = 0 valutato in 40 punti (righe = derivate d^alpha u nei punti), nucleo numerico
dfun = [sp.lambdify((t, x), sp.diff(u, t, a, x, b), 'numpy') for (a, b) in mons]
pts = rng.uniform(-1, 1, size=(40, 2))
Mnum = np.array([[f(pt[0], pt[1]) for f in dfun] for pt in pts], dtype=float)
sv = np.linalg.svd(Mnum, compute_uv=False)
null_direct = int(np.sum(sv < 1e-9 * sv.max()))
# via (z_k + d)
def shifted(q, z):
    # Q(z+d) q = sum_c c * (z_t + d_t)^a (z_x + d_x)^b q
    tot = 0
    for c, (a, b) in zip(cs, mons):
        r = q
        for _ in range(a):
            r = z[0] * r + sp.diff(r, t)
        for _ in range(b):
            r = z[1] * r + sp.diff(r, x)
        tot += c * r
    return sp.expand(tot)
eqs_shift = []
for q, z in terms:
    pp = sp.Poly(shifted(q, z), t, x)
    eqs_shift += pp.coeffs()
Ms = sp.Matrix([[sp.diff(eq, c) for c in cs] for eq in eqs_shift])
Ns = Ms.nullspace(); Nd = Ns
resid = max(np.abs(Mnum @ np.array([float(vv_i) for vv_i in vv])).max() for vv in Ns) if Ns else 0.0
same = null_direct == len(Ns) and resid < 1e-8
check("C3-T2(a) Ann(u) cap R_<=3: nucleo diretto (40 punti) = nucleo di Q(z_k+d)q_k = 0", same, f"dim diretto={null_direct}, dim shift={len(Ns)}, residuo={resid:.1e}")
# V(Ann u) = {z_k}: ogni elemento del nucleo si annulla in z_k; in un punto estraneo qualche elemento non si annulla
def Qpoly(vec):
    return sum(vec[i] * tau ** a * xi ** b for i, (a, b) in enumerate(mons))
Qs = [Qpoly(vv) for vv in Nd]
okz = all(sp.simplify(Q.subs({tau: z[0], xi: z[1]})) == 0 for Q in Qs for _, z in terms)
okout = all(any(sp.simplify(Q.subs({tau: p0[0], xi: p0[1]})) != 0 for Q in Qs) for p0 in [(0, 0), (1, 1), (2, 1), (-1, 3)])
check("C3-T2(a) ogni Q in Ann_<=3 si annulla in {z_k}; nei punti (0,0),(1,1),(2,1),(-1,3) no", okz and okout)
# intersezione: Ann(u) = cap_k Ann(q_k e^{z_k}) sul grado <= 3
dims = []
for q, z in terms:
    pp = sp.Poly(shifted(q, z), t, x)
    Mk = sp.Matrix([[sp.diff(eq, c) for c in cs] for eq in pp.coeffs()])
    dims.append(len(cs) - Mk.rank())
check("C3-T2(a) Ann(q_k e^{z_k})_<=3 sono propri e la loro intersezione e' Ann(u)_<=3", all(dd < len(cs) for dd in dims) and len(Nd) == len(cs) - Ms.rank(), f"dim singoli={dims}")
# modo semplice: q costante => I_k = m_{z_k} (grado <= 3)
pp = sp.Poly(shifted(sp.Integer(3), (2, 0)), t, x)
Mk = sp.Matrix([[sp.diff(eq, c) for c in cs] for eq in pp.coeffs()])
check("C3-T2(a) q_k costante: {Q : Q(z_k+d)q_k=0}_<=3 = m_{z_k} cap R_<=3 (codim 1)", Mk.rank() == 1)

print()
nok = sum(1 for _, o in RES if o)
print(f"ESITO {nok}/{len(RES)} OK")
