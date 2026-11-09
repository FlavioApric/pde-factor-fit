# S-CHECK-COL: kill-argument numerici indipendenti per S10COL-TA/TB/TC.
#  (K1) grafico con tangenti oscillanti g(x) = x sin(log|x|): in 0 g non e' differenziabile e
#       g' riempie [-sqrt2, sqrt2] in ogni intorno. Campo non costante con kappa>0 q.o.:
#       test del testimone di D(0) e del flusso. Caso limite: W(0) sul bordo del cono di Clarke
#       -> kappa_ess -> 0 vicino a 0 (l'ipotesi fallisce, coerente).
#  (K2) zig-zag con angoli che si accumulano in 0 (g(x) = |x| tri(log2|x|)): flusso dagli angoli.
#  (K3) two-brick in R^3: D(p) vuoto e nessun vettore w con w.nu >= kappa sulle facce vicine a p.
#  (K4) poligono a pettine con fessure strette (non stellato, angoli rientranti): campo di carta
#       con direzioni casuali vicino al bordo dei coni, pesi casuali, carte vertice+lato;
#       Monte Carlo del flusso. (K4neg) controlli negativi.
import numpy as np

rng = np.random.default_rng(271026)
ok_all = True


def report(name, ok, msg):
    global ok_all
    ok_all &= bool(ok)
    print(f"[{'OK' if ok else 'FAIL'}] {name}: {msg}")


def rk4(F, Y, T, dt):
    n = int(round(T / dt))
    out = [Y.copy()]
    for _ in range(n):
        k1 = F(Y); k2 = F(Y + dt / 2 * k1); k3 = F(Y + dt / 2 * k2); k4 = F(Y + dt * k3)
        Y = Y + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        out.append(Y.copy())
    return out


# ---------------------------------------------------------------- (K1)
def g1(x):
    ax = np.abs(x)
    return np.where(ax > 0, x * np.sin(np.log(np.where(ax > 0, ax, 1.0))), 0.0)


def dg1(x):
    lx = np.log(np.abs(x))
    return np.sin(lx) + np.cos(lx)


def W1(X):
    x, y = X[:, 0], X[:, 1]
    return np.stack([0.3 + 0.1 * np.sin(3 * y + x), 1.0 + 0.1 * np.cos(2 * x)], 1)


# griglia logaritmica bilaterale fino a 1e-12
xs = np.concatenate([-np.logspace(-12, -0.3, 200000), np.logspace(-12, -0.3, 200000)])
Q = np.stack([xs, g1(xs)], 1)
G = dg1(xs)
Wq = W1(Q)
kap1 = np.min((Wq[:, 1] - Wq[:, 0] * G) / np.sqrt(1 + G ** 2))
print(f"      K1: range g' campionato = [{G.min():.4f}, {G.max():.4f}], kappa = {kap1:.4f}")
report("(K1a) kappa > 0 q.o.", kap1 > 0, f"kappa = {kap1:.4f}")

# testimone in p=0: x in Omega-bar vicino a 0 (punti di bordo + punti sopra), u in B(W(0),r), t in (0,r]
W0 = W1(np.zeros((1, 2)))[0]
r = 0.02
N = 400000
xb = np.concatenate([np.sign(rng.standard_normal(N // 2)) * np.logspace(-12, np.log10(r / 2), N // 2), (rng.random(N // 2) - 0.5) * r])
yb = g1(xb) + np.where(np.arange(N) < N // 2, 0.0, rng.random(N) * r / 2)
ang = 2 * np.pi * rng.random(N); rad = r * np.sqrt(rng.random(N))
U = W0[None] + np.stack([rad * np.cos(ang), rad * np.sin(ang)], 1)
t = r * rng.random(N) + 1e-15
Y = np.stack([xb, yb], 1) + t[:, None] * U
gap = Y[:, 1] - g1(Y[:, 0])
ratio = np.min(gap / t)
report("(K1b) testimone di W(0) in D(0)", ratio >= kap1 / 2, f"min (y_2-g(y_1))/t = {ratio:.4f} >= kappa/2 = {kap1/2:.4f} su {N} terne (x,u,t)")

# flusso di W1 da punti del bordo fino a 1e-10 da 0, e dal punto angoloso 0 stesso
x0 = np.concatenate([[0.0], np.sign(rng.standard_normal(3000)) * np.logspace(-10, -1, 3000)])
X0 = np.stack([x0, g1(x0)], 1)
traj = rk4(W1, X0, 0.02, 1e-4)
cmin = np.inf
for k in (10, 50, 100, 200):
    Yk = traj[k]; tk = k * 1e-4
    cmin = min(cmin, np.min((Yk[:, 1] - g1(Yk[:, 0])) / tk))
report("(K1c) flusso dal bordo oscillante", cmin > 0, f"min (y_2-g(y_1))/t lungo il flusso = {cmin:.4f} (atteso >= ~kappa/2)")

# caso limite: W(0) = (1, sqrt2)/|.|: W2 - W1 s = 0 per s = sqrt2
Wb = np.array([1.0, np.sqrt(2)]) / np.sqrt(3)
kb = []
for R0 in (1e-1, 1e-3, 1e-6, 1e-9):
    m = np.abs(xs) < R0
    kb.append(np.min((Wb[1] - Wb[0] * G[m]) / np.sqrt(1 + G[m] ** 2)))
report("(K1d) W(0) sul bordo del cono di Clarke: kappa_ess -> 0", max(kb) < 1e-6,
       "kappa su |x|<1e-1,1e-3,1e-6,1e-9 = " + ", ".join(f"{v:.1e}" for v in kb) + " (l'ipotesi di TB fallisce, nessun controesempio)")

# ---------------------------------------------------------------- (K2)
def tri(s):
    f = s - np.floor(s)
    return 0.5 - np.abs(f - 0.5)  # in [0, 0.5], pendenza +-1


def g2(x):
    ax = np.abs(x)
    return np.where(ax > 0, ax * 0.4 * tri(np.log2(np.where(ax > 0, ax, 1.0))), 0.0)


# g' = 0.4*sign(x)*(tri + tri'/ln2): |g'| <= 0.4*(0.5+1/ln2) ~ 0.777
xs2 = np.concatenate([-np.logspace(-12, -0.3, 300000), np.logspace(-12, -0.3, 300000)])
h = 1e-9 * np.abs(xs2)
G2 = (g2(xs2 + h) - g2(xs2 - h)) / (2 * h)


def W2(X):
    x, y = X[:, 0], X[:, 1]
    return np.stack([0.5 * np.sin(5 * x) + 0.2 * np.cos(4 * y), 1.0 + 0.2 * np.sin(3 * x * y)], 1)


Wq2 = W2(np.stack([xs2, g2(xs2)], 1))
kap2 = np.min((Wq2[:, 1] - Wq2[:, 0] * G2) / np.sqrt(1 + G2 ** 2))
print(f"      K2: |g'| max = {np.abs(G2).max():.4f}, kappa = {kap2:.4f}")
# angoli: log2|x| = k/2 (tri ha angoli negli interi e nei semi-interi)
kk = np.arange(-60, -1)
corners = np.concatenate([2.0 ** (kk / 2), -2.0 ** (kk / 2), [0.0]])
X0 = np.stack([corners, g2(corners)], 1)
traj = rk4(W2, X0, 0.02, 1e-4)
cmin2 = np.inf
for k in (1, 5, 20, 100, 200):
    Yk = traj[k]; tk = k * 1e-4
    cmin2 = min(cmin2, np.min((Yk[:, 1] - g2(Yk[:, 0])) / tk))
report("(K2) flusso dagli angoli che si accumulano", kap2 > 0 and cmin2 > 0,
       f"kappa = {kap2:.4f}; {len(corners)} angoli (fino a |x| = 2^-30); min (y_2-g)/t = {cmin2:.4f}")

# ---------------------------------------------------------------- (K3) two-brick
def in_brick(X):
    x, y, z = X[:, 0], X[:, 1], X[:, 2]
    U1 = (0 < x) & (x < 2) & (0 < y) & (y < 1) & (0 < z) & (z < 1)
    U2 = (0 < x) & (x < 1) & (0 < y) & (y < 2) & (-1 < z) & (z < 0)
    F = (0 < x) & (x < 1) & (0 < y) & (y < 1) & (z == 0)
    return U1 | U2 | F


p = np.array([1.0, 1.0, 0.0])
Wdirs = rng.standard_normal((20000, 3)); Wdirs /= np.linalg.norm(Wdirs, axis=1)[:, None]
fail = 0
for hh in (1e-3,):
    xa = p + np.array([hh, -hh, 0.0])   # faccia inferiore del mattone superiore (esterno sotto)
    xb_ = p + np.array([-hh, hh, 0.0])  # faccia superiore del mattone inferiore (esterno sopra)
    ts = np.array([1e-5, 1e-4, 5e-4])
    good = np.ones(len(Wdirs), bool)
    for xx in (xa, xb_):
        for tt in ts:
            good &= in_brick(xx[None] + tt * Wdirs)
    fail = int(np.sum(good))
report("(K3a) two-brick: D(p) vuoto", fail == 0, f"direzioni (su 20000) che entrano da entrambe le facce z=0 vicino a p: {fail}")
# facce che si accumulano in p e loro normali esterne: z=0 (sup., x>1): -e3 ; z=0 (inf., y>1): +e3
nus = np.array([[0, 0, -1], [0, 0, 1], [0, 1, 0], [1, 0, 0]], float)
best = np.max(np.min(Wdirs @ nus.T, axis=1))
report("(K3b) two-brick: nessun V continuo con V.nu >= kappa", best <= 0,
       f"max_w min_faccia w.nu = {best:.4f} <= 0 (le normali +-e3 si accumulano in p)")

# ---------------------------------------------------------------- (K4) pettine con fessure strette
def comb(width):
    P = [(0, 0), (7, 0), (7, 3)]
    x = 7.0
    for k in range(3):
        P += [(x - 1, 3), (x - 1, 1), (x - 1 - width, 1), (x - 1 - width, 3)]
        x = x - 1 - width
    P += [(0, 3)]
    return np.array(P, float)


def poly_tools(P):
    A = P; B = np.roll(P, -1, 0); D = B - A; ell = np.linalg.norm(D, axis=1)
    area = 0.5 * np.sum(A[:, 0] * B[:, 1] - B[:, 0] * A[:, 1])
    sgn = 1 if area > 0 else -1
    Nin = sgn * np.stack([-D[:, 1], D[:, 0]], 1) / ell[:, None]

    def inside(X):
        x, y = X[:, 0][:, None], X[:, 1][:, None]
        c = (A[:, 1] > y) != (B[:, 1] > y)
        den = np.where(B[:, 1] - A[:, 1] == 0, 1e-300, B[:, 1] - A[:, 1])
        xi = A[:, 0] + (y - A[:, 1]) * (B[:, 0] - A[:, 0]) / den
        return (np.sum(c & (x < xi), 1) % 2) == 1

    def dseg(X, idx=None):
        AA, DD, LL = (A, D, ell) if idx is None else (A[idx], D[idx], ell[idx])
        AP = X[:, None, :] - AA[None]
        tt = np.clip(np.sum(AP * DD[None], 2) / LL[None] ** 2, 0, 1)
        return np.linalg.norm(AP - tt[..., None] * DD[None], axis=2)

    def sdist(X):
        d = np.min(dseg(X), 1)
        return np.where(inside(X), d, -d)
    return A, B, D, ell, Nin, inside, dseg, sdist


def build_field(P, frac_lo, frac_hi, flip=None, tangent_edge=None):
    A, B, D, ell, Nin, inside, dseg, sdist = poly_tools(P)
    NV = len(P)
    centers, radii, dirs = [], [], []
    rv = np.zeros(NV)
    for k in range(NV):
        others = [j for j in range(NV) if j not in (k, (k - 1) % NV)]
        rv[k] = 0.45 * min(np.min(dseg(P[k:k + 1], others)), ell[k], ell[k - 1])
    for k in range(NV):
        n1, n2 = Nin[k - 1], Nin[k]
        # cono ammissibile {e: e.n1 > 0, e.n2 > 0}: arco di angoli
        a1, a2 = np.arctan2(n1[1], n1[0]), np.arctan2(n2[1], n2[0])
        dd = (a2 - a1 + np.pi) % (2 * np.pi) - np.pi
        lo, hi = max(-np.pi / 2, dd - np.pi / 2), min(np.pi / 2, dd + np.pi / 2)
        f = frac_lo + (frac_hi - frac_lo) * rng.random()
        f = frac_lo if rng.random() < 0.5 else frac_hi  # vicino al bordo del cono
        ph = a1 + lo + f * (hi - lo)
        centers.append(P[k]); radii.append(rv[k]); dirs.append([np.cos(ph), np.sin(ph)])
    for k in range(NV):
        others = [j for j in range(NV) if j != k and j != (k - 1) % NV and j != (k + 1) % NV]
        s = 0.5 * rv[k]
        while s < ell[k] - 0.5 * rv[(k + 1) % NV]:
            c = A[k] + s / ell[k] * D[k]
            rc = 0.9 * min(s, ell[k] - s, np.min(dseg(c[None], others)))
            ph0 = np.arctan2(Nin[k][1], Nin[k][0])
            f = (frac_lo if rng.random() < 0.5 else frac_hi)
            ph = ph0 + (f - 0.5) * np.pi
            if tangent_edge is not None and k == tangent_edge:
                ph = ph0 + np.pi / 2  # direzione tangente: kappa = 0 su un arco
            centers.append(c); radii.append(rc); dirs.append([np.cos(ph), np.sin(ph)])
            s += 0.5 * rc
    C = np.array(centers); R = np.array(radii); E = np.array(dirs)
    wts = 0.2 + 0.8 * rng.random(len(C))
    if flip is not None:
        E[flip] = -E[flip]

    def phis(X):
        d2 = np.sum((X[:, None, :] - C[None]) ** 2, 2) / R[None] ** 2
        out = np.zeros_like(d2); m = d2 < 1
        out[m] = np.exp(1 - 1 / (1 - d2[m]))
        return out * wts[None]

    def W(X):
        return phis(X) @ E
    return dict(C=C, R=R, E=E, NV=NV, rv=rv, W=W, phis=phis, tools=(A, B, D, ell, Nin, inside, dseg, sdist))


def check_charts(P, F, n=4000):
    A, B, D, ell, Nin, inside, dseg, sdist = F["tools"]
    bad = 0
    for k in range(F["NV"]):
        e = F["E"][k]; u = np.array([e[1], -e[0]]); r0 = F["rv"][k]
        th = 2 * np.pi * rng.random(n); rr = r0 * np.sqrt(rng.random(n))
        Xs = P[k] + np.stack([rr * np.cos(th), rr * np.sin(th)], 1)
        s = (Xs - P[k]) @ u; hgt = (Xs - P[k]) @ e
        nb = [P[k - 1], P[(k + 1) % F["NV"]]]
        sn = [(q - P[k]) @ u for q in nb]; hn = [(q - P[k]) @ e for q in nb]
        if sn[0] * sn[1] >= 0:
            bad += n; continue
        g = np.where(np.sign(s) == np.sign(sn[0]), hn[0] / sn[0] * s, hn[1] / sn[1] * s)
        bad += int(np.sum((hgt > g) != inside(Xs)))
    return bad


def mc_flow(P, F, T=0.03, dt=2e-4, Nnear=4000):
    A, B, D, ell, Nin, inside, dseg, sdist = F["tools"]
    sb = np.linspace(0, 1, 80, endpoint=False)
    Xb = np.concatenate([A[k] + sb[:, None] * D[k] for k in range(len(A))])
    eid = np.repeat(np.arange(len(A)), 80)
    kap = np.min(np.sum(F["W"](Xb) * Nin[eid], 1))
    cov = np.min(np.sum(F["phis"](Xb), 1))
    lo, hi = P.min(0) - 0.1, P.max(0) + 0.1
    Z = lo + (hi - lo) * rng.random((200000, 2)); Z = Z[inside(Z)]
    near = Z[np.min(dseg(Z), 1) < 0.05][:Nnear]
    X0 = np.concatenate([P, Xb, near])
    traj = rk4(F["W"], X0, T, dt)
    viol, cmin = 0, np.inf
    for k in (5, 25, 50, 100, len(traj) - 1):
        sd = sdist(traj[k]); viol += int(np.sum(sd <= 0)); cmin = min(cmin, np.min(sd / (k * dt)))
    return kap, cov, viol, cmin, len(X0), traj, X0


for width, lab in ((1.0, "fessure larghe 1"), (0.15, "fessure larghe 0.15")):
    P = comb(width)
    F = build_field(P, 0.03, 0.97)
    bad = check_charts(P, F)
    kap, cov, viol, cmin, n0, _, _ = mc_flow(P, F)
    ang = max(np.degrees(np.arccos(np.clip(F["E"][i] @ F["E"][j], -1, 1)))
              for i in range(len(F["C"])) for j in range(len(F["C"]))
              if i < j and np.linalg.norm(F["C"][i] - F["C"][j]) < F["R"][i] + F["R"][j])
    # angolo massimo tra direzioni di carte che contengono uno stesso punto del bordo
    A_, B_, D_, ell_, Nin_, inside_, dseg_, sdist_ = F["tools"]
    sb = np.linspace(0, 1, 400, endpoint=False)
    Xb = np.concatenate([A_[k] + sb[:, None] * D_[k] for k in range(len(A_))])
    memb = np.sum((Xb[:, None, :] - F["C"][None]) ** 2, 2) < F["R"][None] ** 2
    angb = 0.0
    for i in range(len(Xb)):
        idx = np.where(memb[i])[0]
        if len(idx) > 1:
            Ei = F["E"][idx]
            angb = max(angb, np.degrees(np.arccos(np.clip(np.min(Ei @ Ei.T), -1, 1))))
    print(f"      K4 [{lab}]: {len(F['C'])} carte, disaccordi carte-vertice = {bad}, min sum phi = {cov:.2e}, "
          f"kappa = {kap:.2e}; angolo max tra carte con palle sovrapposte = {ang:.1f} gradi "
          f"(sovrapposizione fuori dal bordo), tra carte con un punto di bordo comune = {angb:.1f} gradi")
    report(f"(K4) pettine, {lab}", bad == 0 and cov > 0 and kap > 0 and viol == 0 and cmin > 0,
           f"{n0} punti iniziali, violazioni = {viol}, c_emp = {cmin:.2e}")

# negativi
P = comb(0.15)
F = build_field(P, 0.03, 0.97, flip=3)
_, _, viol, cmin, n0, traj, X0 = mc_flow(P, F)
report("(K4neg1) una direzione di carta invertita", viol > 0, f"violazioni = {viol} (attese > 0)")
F = build_field(P, 0.2, 0.8, tangent_edge=0)
kap, _, viol, cmin, n0, _, _ = mc_flow(P, F)
report("(K4neg2) direzioni tangenti su un lato (kappa = 0)", kap <= 1e-12 and cmin < 1e-3,
       f"kappa = {kap:.2e}, c_emp = {cmin:.2e}, violazioni = {viol} (uniformita' persa)")

print("ESITO:", "TUTTO OK" if ok_all else "CI SONO FALLIMENTI")
