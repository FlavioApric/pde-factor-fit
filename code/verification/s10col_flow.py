# S10-COL: controlli numerici per (COL-ii).
# Dominio: poligono stellato a zig-zag con 24 vertici (lipschitziano, non convesso).
# Campo: W = sum_k phi_k e_k (phi_k bump su B(v_k, r_k), e_k direzione di carta
# scelta vicino al bordo del cono ammissibile, alternando i lati), V = -W.
# Verifiche:
#  (1) le palle B(v_k,r_k) sono carte: Omega cap B = epigrafico in direzione e_k;
#  (2) le palle ricoprono il bordo;
#  (3) kappa = min_{bordo} V.nu > 0 (Teorema B si applica anche a questo V);
#  (4) Monte Carlo: dist(psi_t(x), C Omega) >= c t per x in bar Omega, t in (0, sigma0];
#  (5) Teorema B con un campo perturbato (non costruito per carte) con kappa > 0;
#  (6) controllo negativo: una e_k fuori dal cono -> violazioni.
import numpy as np

rng = np.random.default_rng(20261027)

m = 12
NV = 2 * m
ang = np.pi * np.arange(NV) / m
rad = np.where(np.arange(NV) % 2 == 0, 1.0, 0.6)
P = np.stack([rad * np.cos(ang), rad * np.sin(ang)], axis=1)  # CCW
A = P
B = np.roll(P, -1, axis=0)
D = B - A
ell = np.linalg.norm(D, axis=1)
Nin = np.stack([-D[:, 1], D[:, 0]], axis=1) / ell[:, None]  # normale interna (CCW)


def inside(X):
    # ray casting, X shape (N,2)
    x, y = X[:, 0][:, None], X[:, 1][:, None]
    ax, ay, bx, by = A[:, 0], A[:, 1], B[:, 0], B[:, 1]
    cond = (ay > y) != (by > y)
    xint = ax + (y - ay) * (bx - ax) / np.where(by - ay == 0, 1e-300, by - ay)
    return (np.sum(cond & (x < xint), axis=1) % 2) == 1


def dist_bd(X):
    AP = X[:, None, :] - A[None, :, :]
    t = np.clip(np.sum(AP * D[None], axis=2) / ell[None] ** 2, 0, 1)
    Q = A[None] + t[..., None] * D[None]
    return np.min(np.linalg.norm(X[:, None, :] - Q, axis=2), axis=1)


def sdist(X):
    # distanza dal complementare (positiva dentro, negativa fuori)
    d = dist_bd(X)
    return np.where(inside(X), d, -d)


# direzioni di carta: cono ammissibile al vertice k = {e: e.n_{k-1}>0, e.n_k>0}
def adm_arc(k):
    a1 = np.arctan2(*Nin[k - 1][::-1])
    a2 = np.arctan2(*Nin[k][::-1])
    # intervallo (a-pi/2, a+pi/2) per ciascuno; intersezione
    d = (a2 - a1 + np.pi) % (2 * np.pi) - np.pi
    lo = max(-np.pi / 2, d - np.pi / 2)
    hi = min(np.pi / 2, d + np.pi / 2)
    return a1 + lo, a1 + hi


def chart_dirs(frac_lo, frac_hi):
    E = np.zeros((NV, 2))
    for k in range(NV):
        lo, hi = adm_arc(k)
        f = frac_lo if k % 4 in (0, 1) else frac_hi  # alterna verso i due bordi del cono
        phi = lo + f * (hi - lo)
        E[k] = [np.cos(phi), np.sin(phi)]
    return E


rr = 0.55 * ell.min()
R = np.full(NV, rr)


def phis(X):
    d2 = np.sum((X[:, None, :] - P[None]) ** 2, axis=2) / R[None] ** 2
    out = np.zeros_like(d2)
    msk = d2 < 1
    out[msk] = np.exp(1 - 1 / (1 - d2[msk]))
    return out


def make_W(E, pert=0.0):
    def W(X):
        w = phis(X) @ E
        if pert:
            w = w + pert * np.stack([np.sin(3 * X[:, 1] + 1), np.cos(2 * X[:, 0] - 0.5)], 1) * np.sum(phis(X), 1)[:, None]
        return w
    return W


def flow(W, X, T, dt=2e-4, record=None):
    Y = X.copy()
    n = int(round(T / dt))
    recs = {}
    for i in range(1, n + 1):
        k1 = W(Y); k2 = W(Y + dt / 2 * k1); k3 = W(Y + dt / 2 * k2); k4 = W(Y + dt * k3)
        Y = Y + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        if record is not None and i in record:
            recs[i * dt] = Y.copy()
    return Y, recs


def bd_samples(n_per_edge):
    s = np.linspace(0, 1, n_per_edge, endpoint=False)
    return np.concatenate([A[k] + s[:, None] * D[k] for k in range(NV)]), np.repeat(np.arange(NV), n_per_edge)


ok_all = True


def report(name, ok, msg):
    global ok_all
    ok_all &= ok
    print(f"[{'OK' if ok else 'FAIL'}] {name}: {msg}")


E = chart_dirs(0.04, 0.96)

# (1) carte
worst = 0
for k in range(NV):
    e = E[k]; u = np.array([e[1], -e[0]])
    Xs = P[k] + rr * np.sqrt(rng.random(20000))[:, None] * np.stack(
        [np.cos(th := 2 * np.pi * rng.random(20000)), np.sin(th)], 1)
    s = (Xs - P[k]) @ u; h = (Xs - P[k]) @ e
    nb = [P[k - 1], P[(k + 1) % NV]]
    sn = [(q - P[k]) @ u for q in nb]; hn = [(q - P[k]) @ e for q in nb]
    assert sn[0] * sn[1] < 0, "vicini dallo stesso lato: carta non grafico"
    g = np.where(np.sign(s) == np.sign(sn[0]), hn[0] / sn[0] * s, hn[1] / sn[1] * s)
    epi = h > g
    worst += int(np.sum(epi != inside(Xs)))
    Lmax = max(Lmax, abs(hn[0] / sn[0]), abs(hn[1] / sn[1])) if k else max(abs(hn[0] / sn[0]), abs(hn[1] / sn[1]))
report("(1) carte", worst == 0, f"disaccordi Omega vs epigrafico su {NV}x20000 punti = {worst}; L max delle carte = {Lmax:.2f}")
# distanza dei vertici dai lati non adiacenti
dn = min(np.min([np.linalg.norm(P[k] - (A[j] + np.clip((P[k] - A[j]) @ D[j] / ell[j] ** 2, 0, 1) * D[j]))
                 for j in range(NV) if j not in (k, (k - 1) % NV)]) for k in range(NV))
report("(1b) palle senza lati non adiacenti", dn > rr, f"min dist vertice-lati non adiacenti = {dn:.4f} > r = {rr:.4f}")

# (2) ricoprimento
Xb, eid = bd_samples(400)
cov = np.sum(phis(Xb), 1)
report("(2) ricoprimento", cov.min() > 0, f"min sum phi_k sul bordo = {cov.min():.3e}")

# (3) kappa
W = make_W(E)
kap = np.min(np.sum(W(Xb) * Nin[eid], 1))  # V.nu = W.n_in
ang_disagree = max(np.degrees(np.arccos(np.clip(E[k] @ E[(k + 1) % NV], -1, 1))) for k in range(NV))
report("(3) kappa", kap > 0, f"min V.nu = {kap:.4f}; max angolo tra e_k di carte adiacenti = {ang_disagree:.1f} gradi")

# (4) Monte Carlo
def mc(W, label, sigma0=0.04, N=6000):
    Xb2, _ = bd_samples(60)
    # punti vicini al bordo dentro Omega e punti interni
    Z = rng.random((60000, 2)) * 2.2 - 1.1
    Z = Z[inside(Z)]
    near = Z[dist_bd(Z) < 0.08][:N]
    far = Z[:2000]
    X0 = np.concatenate([P, Xb2, near, far])
    steps = [int(round(t / 2e-4)) for t in (0.002, 0.005, 0.01, 0.02, 0.03, 0.04)]
    _, recs = flow(W, X0, sigma0, record=set(steps))
    cmin = np.inf; viol = 0
    for t, Y in sorted(recs.items()):
        sd = sdist(Y)
        viol += int(np.sum(sd <= 0))
        cmin = min(cmin, np.min(sd / t))
        print(f"      t={t:.3f}: min dist(psi_t x, C Omega)/t = {np.min(sd / t):.4f}")
    report(label, viol == 0 and cmin > 0, f"{len(X0)} punti iniziali, violazioni = {viol}, c_emp = {cmin:.4f}")
    return viol


mc(W, "(4) inclusione, campo di carta (direzioni al 4%/96% del cono)")
E4b = chart_dirs(0.2, 0.8); W4b = make_W(E4b)
print(f"      direzioni al 20%/80%: kappa = {np.min(np.sum(W4b(Xb) * Nin[eid], 1)):.4f}")
mc(W4b, "(4b) inclusione, campo di carta (direzioni al 20%/80%)")

# (5) Teorema B: campo perturbato
E5 = chart_dirs(0.2, 0.8)
W5 = make_W(E5, pert=0.08)
kap5 = np.min(np.sum(W5(Xb) * Nin[eid], 1))
print(f"      campo perturbato: kappa = {kap5:.4f}")
if kap5 > 0:
    mc(W5, "(5) inclusione, campo perturbato con kappa>0")
else:
    report("(5)", False, "kappa non positivo: scegliere altra perturbazione")

# (6) controllo negativo: e_0 fuori dal cono (esterna)
E6 = E.copy(); E6[0] = -E6[0]
W6 = make_W(E6)
Y6, _ = flow(W6, P[:1].copy(), 0.01)
neg = sdist(Y6)[0]
report("(6) controllo negativo", neg < 0, f"vertice 0 con e_0 invertita: sdist dopo t=0.01 = {neg:.4e} (<0 atteso)")

print("ESITO:", "TUTTO OK" if ok_all else "CI SONO FALLIMENTI")

