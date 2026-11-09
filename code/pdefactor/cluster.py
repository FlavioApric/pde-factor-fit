"""Step 4 of the note, domain grouping (GROUPING.md type B), on rectangular windows.

Every window is a rectangle [t0, t1) x [x0, x1) (CLAUDE.md rule 6, C12-T1'). The core runs on
each window's posterior samples; the window's encoder features are analytic only (P2-P4,
THEORY_TO_ALGO T8): the mass of its factors on each global factor cluster of W, its posterior over
the number of factors, its sorted energy fractions and gamma_N. PCA may be added on top.

Clustering: GMM, k-means, spectral and agglomerative, initialised from W (one centre per dominant
global factor, the note's theta_bar_j), with a connectivity constraint on the window adjacency
graph, so every group is a union of edge-adjacent rectangles. Groups are checked for holes.
Baseline: dominant balance (Callaham et al., Nat. Commun. 2021), a GMM on local term magnitudes.

The per-window field comes from a provider `field_on(rect) -> (u, t, x)`. The non-periodic mode
extractor is S-DOMAIN's job (DOMAIN.md E3); until it lands, `exact_provider` feeds the exact
component(s) active in each rectangle, on a periodic x-grid over the rectangle's time span.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .aggregate import Aggregate, Cloud, aggregate, fake_posterior, run_core


# ------------------------------------------------------------------ rectangles
@dataclass(frozen=True)
class Rect:
    t0: float
    t1: float
    x0: float
    x1: float
    it: int = 0  # index in the window grid (time)
    ix: int = 0  # index in the window grid (space)

    @property
    def area(self):
        return (self.t1 - self.t0) * (self.x1 - self.x0)


def rectangles(T, L, nt_win, nx_win, t0=0.0, x0=0.0):
    """Regular grid of nt_win x nx_win rectangles covering [t0, t0+T) x [x0, x0+L)."""
    te = t0 + np.linspace(0, T, nt_win + 1)
    xe = x0 + np.linspace(0, L, nx_win + 1)
    return [Rect(te[i], te[i + 1], xe[j], xe[j + 1], i, j) for i in range(nt_win) for j in range(nx_win)]


def adjacency(rects, tol=1e-12):
    """A[i, j] = 1 when rectangles i and j share an edge of positive length."""
    n = len(rects)
    A = np.zeros((n, n), int)
    for i, a in enumerate(rects):
        for j, b in enumerate(rects):
            if i == j:
                continue
            ov_t = min(a.t1, b.t1) - max(a.t0, b.t0)
            ov_x = min(a.x1, b.x1) - max(a.x0, b.x0)
            touch_x = abs(a.x1 - b.x0) < tol or abs(b.x1 - a.x0) < tol
            touch_t = abs(a.t1 - b.t0) < tol or abs(b.t1 - a.t0) < tol
            if (touch_x and ov_t > tol) or (touch_t and ov_x > tol):
                A[i, j] = 1
    return A


def connected_split(labels, A):
    """Split every label into its connected components on the graph A (the connectivity constraint)."""
    from scipy.sparse.csgraph import connected_components

    out = -np.ones(len(labels), int)
    nxt = 0
    for c in np.unique(labels):
        ii = np.where(labels == c)[0]
        _, comp = connected_components(A[np.ix_(ii, ii)], directed=False)
        for k in np.unique(comp):
            out[ii[comp == k]] = nxt
            nxt += 1
    return out


def has_hole(rects, labels):
    """For a regular window grid: True when some group's union of rectangles encloses cells of
    another group (a hole: C12-T1' fails, defect <= delta(P) b_1)."""
    from scipy.ndimage import label as cc

    nt = max(r.it for r in rects) + 1
    nx = max(r.ix for r in rects) + 1
    G = -np.ones((nt, nx), int)
    for r, l in zip(rects, labels):
        G[r.it, r.ix] = l
    for c in np.unique(labels):
        comp, n = cc(np.pad(G != c, 1, constant_values=True))
        if n > 1:  # some region outside group c does not reach the border
            return True
    return False


# ------------------------------------------------------------------ providers
def exact_provider(regions, T_total=None, nt=48, nx=64, L=2 * np.pi):
    """regions: [(callable field(t, x), x_a, x_b)]. A rectangle sees the sum of the fields whose
    interval it overlaps, scaled by the overlap fraction, evaluated on a periodic x-grid of length
    L over the rectangle's time span (exact components as input)."""
    def field_on(rect):
        t = np.linspace(rect.t0, rect.t1, nt)
        x = np.linspace(0, L, nx, endpoint=False)
        TT, XX = np.meshgrid(t, x, indexing="ij")
        u = np.zeros_like(TT)
        for f, a, b in regions:
            ov = max(0.0, min(b, rect.x1) - max(a, rect.x0)) / (rect.x1 - rect.x0)
            if ov > 0:
                u = u + ov * f(TT, XX)
        return u, t, x
    return field_on


def region_truth(rects, regions):
    """Ground-truth label per rectangle: the region with the largest overlap."""
    out = []
    for r in rects:
        ov = [max(0.0, min(b, r.x1) - max(a, r.x0)) for _, a, b in regions]
        out.append(int(np.argmax(ov)))
    return np.array(out)


# ------------------------------------------------------------------ features
@dataclass
class WindowData:
    rects: list
    aggs: list  # per-window Aggregate (no DP)
    glob: Aggregate  # global W (union of the window clouds, pi proportional to area)
    F: np.ndarray  # encoder features
    names: list
    dominant: list  # global DP clusters with mass, heaviest first
    reg: float = 1e-6  # feature noise variance (posterior spread inside windows)


def _union_results(per_window, rects):
    tot = sum(r.area for r in rects)
    out = []
    for res, r in zip(per_window, rects):
        for sr, p in res:
            out.append((sr, p * r.area / tot))
    return out


def window_features(rects, field_on, rel_noise=1e-2, S=8, seed=0, k_max=3, with_pk=False, **core_kw):
    """Run the core on S fake posterior samples per window, aggregate per window and globally, and
    build the analytic features (P2-P4): per sample, the mass of its factors on each global DP
    cluster, the two largest energy fractions and gamma_N; the window feature is their pi-mean.
    with_pk adds the structure posterior over k (off by default: it is split between equivalent
    dx choices and varies between windows of the same law, see REPORT)."""
    rng = np.random.default_rng(seed)
    per_window, aggs = [], []
    for r in rects:
        u, t, x = field_on(r)
        sig = rel_noise * float(np.std(u)) if np.std(u) > 0 else rel_noise
        us, pis = fake_posterior(u, sig, S, rng)
        res = run_core(us, t, x, sig, pis, **core_kw)
        per_window.append(res)
        aggs.append(aggregate(res, dp=False))
    glob = aggregate(_union_results(per_window, rects))
    dp = glob.dp
    dominant = [int(c) for c in np.argsort(-dp.cluster_mass) if dp.cluster_mass[c] > 0]
    nC = len(dp.cluster_mass)
    names = [f"mass_c{c}" for c in range(nC)] + ["w_1", "w_2", "gamma"]
    if with_pk:
        names += [f"P(k={k})" for k in range(1, k_max + 1)]
    F, V = [], []
    for res, a in zip(per_window, aggs):
        cl = a.cloud
        R = dp.predict_resp(cl.theta, cl.m, pad=cl.pad) if len(cl) else np.zeros((0, nC))
        rows, ps = [], []
        for s, (sr, p) in enumerate(res):  # one feature row per posterior sample
            sel = cl.sample == s
            mass = (R[sel] * cl.w[sel][:, None]).sum(0) if sel.any() else np.zeros(nC)
            mass = mass / max(mass.sum(), 1e-300)
            w = np.sort(cl.w[sel])[::-1][:2]
            fr = np.r_[w, np.zeros(2 - len(w))]
            row = np.r_[mass, fr, sr.gamma if sr.factors else 0.0]
            if with_pk:
                pk = np.zeros(k_max)
                for st, _, q in sr.structures:
                    if len(st) <= k_max:
                        pk[len(st) - 1] += q
                row = np.r_[row, pk]
            rows.append(row)
            ps.append(p)
        rows, ps = np.array(rows), np.array(ps) / np.sum(ps)
        mu = ps @ rows
        F.append(mu)
        V.append(ps @ (rows - mu) ** 2)
    F, V = np.array(F), np.array(V)
    # empirical-Bayes covariance floor: the features' posterior spread inside a window
    reg = float(max(V.mean(), 1e-8))
    return WindowData(rects, aggs, glob, F, names, dominant, reg)


def encode(F, n_components=None, var=0.99):
    """Optional PCA on top of the analytic features (never on raw fields, P2-P4)."""
    from sklearn.decomposition import PCA

    if n_components is None:
        p = PCA().fit(F)
        n_components = int(np.searchsorted(np.cumsum(p.explained_variance_ratio_), var) + 1)
    n_components = max(1, min(n_components, F.shape[1], len(F)))
    return PCA(n_components).fit_transform(F)


def pure_centres(wd, k):
    """Initial centres from W: the feature vector of a window holding only global factor cluster c
    (one-hot mass, one factor, energy fraction 1, gamma 1), for the k heaviest clusters."""
    nC = len(wd.glob.dp.cluster_mass)
    out = []
    for c in wd.dominant[:k]:
        v = np.zeros(wd.F.shape[1])
        v[c] = 1.0
        v[nC], v[nC + 2] = 1.0, 1.0  # one factor with all the energy, gamma = 1
        out.append(v)
    return np.array(out) if len(out) == k else None


# ------------------------------------------------------------------ clustering
def k_posterior(F, reg, k_max=6, seed=0):
    """BIC posterior over the number of groups (finite GMM, diag covariances, covariance floor =
    the features' posterior noise variance)."""
    from sklearn.mixture import GaussianMixture

    bic = {}
    for k in range(1, min(k_max, len(F) - 1) + 1):
        g = GaussianMixture(k, covariance_type="diag", reg_covar=reg, n_init=4, random_state=seed).fit(F)
        bic[k] = g.bic(F)
    b = np.array(list(bic.values()))
    p = np.exp(-(b - b.min()) / 2)
    return dict(zip(bic.keys(), p / p.sum()))


def cluster_windows(wd, method="gmm", k=None, A=None, use_pca=False, seed=0):
    """Labels per window. k: None = MAP of the BIC posterior over k; 'keff' = the note's
    ceil(k_eff) of the global W. Initialised from W when the number of dominant clusters allows.
    The connectivity constraint is built into spectral/agglomerative and applied to GMM/k-means by
    splitting each label into connected components."""
    from sklearn.cluster import AgglomerativeClustering, KMeans, SpectralClustering
    from sklearn.mixture import GaussianMixture

    F = encode(wd.F) if use_pca else wd.F
    A = adjacency(wd.rects) if A is None else A
    if k is None:
        pk = k_posterior(F, wd.reg, seed=seed)
        k = max(pk, key=pk.get)
    elif k == "keff":
        k = wd.glob.k_det
    k = int(max(1, min(k, len(F))))
    init = None if use_pca else pure_centres(wd, k)
    if method == "gmm":
        g = GaussianMixture(k, covariance_type="diag", reg_covar=wd.reg, random_state=seed,
                            means_init=init, n_init=1 if init is not None else 4)
        lab = g.fit_predict(F)
        return connected_split(lab, A)
    if method == "kmeans":
        km = KMeans(k, init=init if init is not None else "k-means++", n_init=1 if init is not None else 10,
                    random_state=seed)
        return connected_split(km.fit_predict(F), A)
    if method == "spectral":
        D = np.linalg.norm(F[:, None] - F[None], axis=2)
        d_adj = D[A > 0]
        h = float(np.mean(d_adj)) if len(d_adj) and np.mean(d_adj) > 0 else 1.0
        W = A * np.exp(-(D / h) ** 2) + 1e-9 * A
        sc = SpectralClustering(k, affinity="precomputed", random_state=seed, assign_labels="cluster_qr")
        return connected_split(sc.fit_predict(W), A)
    if method == "agglomerative":
        ag = AgglomerativeClustering(k, connectivity=A, linkage="ward")
        return ag.fit_predict(F)
    raise ValueError(method)


# ------------------------------------------------------------------ baseline: dominant balance
def dominant_balance_labels(u, t, x, rects, k=2, seed=0):
    """Callaham et al. 2021: GMM on the local magnitudes of the terms (u_t, u_x, u_xx; finite
    differences), then a majority vote per rectangle. Needs a known term library."""
    from sklearn.mixture import GaussianMixture

    ut = np.gradient(u, t, axis=0)
    ux = np.gradient(u, x, axis=1)
    uxx = np.gradient(ux, x, axis=1)
    eps = 1e-12 * np.abs(u).max()
    X = np.stack([np.log10(np.abs(v).ravel() + eps) for v in (ut, ux, uxx)], 1)
    g = GaussianMixture(k, covariance_type="full", random_state=seed, n_init=3).fit(X)
    lab = g.predict(X).reshape(u.shape)
    TT, XX = np.meshgrid(t, x, indexing="ij")
    out = []
    for r in rects:
        sel = (TT >= r.t0) & (TT < r.t1 + 1e-12) & (XX >= r.x0) & (XX < r.x1)
        out.append(int(np.bincount(lab[sel], minlength=k).argmax()) if sel.any() else 0)
    return np.array(out)
