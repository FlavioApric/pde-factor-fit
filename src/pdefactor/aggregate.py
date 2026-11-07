"""Step 3 of the note: from posterior interpolant samples to the distribution over factors.

Input: a list of (StructResult, pi_s), one per interpolant sample (core v2 run as a black box).
Output (`Aggregate`):
- the cloud W = {(theta, w_j, pi_s)} of factor coefficient vectors (note, Step 3);
- tracks: factors matched across samples, only within equal tau-degree m (an invariant of the
  factor: II-C1) and distinct within a sample. With the DP fitted, a track is a DP cluster;
  without it, Hungarian matching to a reference sample (`align`). Each track has mass W_j, mean
  theta_bar_j and covariance Sigma_j;
- k_eff = exp(-sum W_j log W_j) and the note's deterministic k = ceil(k_eff), kept as a comparison;
- per-sample distributions of k_eff, rho, c_F and gamma_N (Monte Carlo only: E_int and Ann(.)
  are discontinuous, OPA-T3 / CONV-T3, THEORY_TO_ALGO T12, T18);
- the co-occurrence matrix of the factor clusters;
- the structure posterior pooled over samples (grouping D), also pooled by number of factors k;
- a variational Dirichlet-process mixture on the cloud, giving a posterior over k by Monte Carlo
  (sample s ~ pi, a label per factor ~ responsibilities, k = number of distinct labels), and a
  finite-mixture BIC posterior over k next to it (the DP posterior on k is not consistent,
  Miller & Harrison 2013).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from math import ceil
from types import SimpleNamespace

import numpy as np
from scipy.optimize import linear_sum_assignment

from .core import components as C
from .core.structfit import analyze_structured

M_MAX, DX_MAX = 2, 4  # core v2 factors: m_j in {1, 2}, dx_j <= 4 (candidate_structures)
CONCENTRATION_GRID = (1e-3, 1e-2, 1e-1, 1.0, 10.0)  # DP gamma_0, chosen by the ELBO (empirical Bayes)


# ------------------------------------------------------------------ inputs
def fake_posterior(u, sigma, S, rng=None):
    """Stand-in for S-INTERP: S copies of the exact grid with independent Gaussian noise of std
    sigma, equal weights pi_s = 1/S."""
    rng = np.random.default_rng(rng)
    return [u + sigma * rng.standard_normal(u.shape) for _ in range(S)], np.full(S, 1.0 / S)


def run_core(samples, t, x, sigma, pis=None, core=None, **core_kw):
    """Core v2 per sample (black box). Returns [(StructResult, pi_s)].
    `core`: another analyser with the same call and result shape (e.g. an S-DOMAIN adapter for
    non-periodic cells): core(u, t, x, noise=..., want_components=True, **kw) -> StructResult-like
    (.label, .factors[FactorResult], .structures, .gamma, .cF, .info, .components)."""
    pis = np.full(len(samples), 1.0 / len(samples)) if pis is None else np.asarray(pis, float)
    core = analyze_structured if core is None else core
    core_kw.setdefault("real", bool(np.isrealobj(samples[0])))
    if core_kw.get("noise_draws", 0) is None:
        core_kw.pop("noise_draws")  # other analysers need not know the keyword
    out = []
    for u, p in zip(samples, pis):
        r = core(u, t, x, noise=sigma, want_components=True, **core_kw)
        r.info.setdefault("grid", (t, x))
        out.append((r, float(p)))
    return out


# ------------------------------------------------------------------ factor coefficients
def factor_vector(Q, m_max=M_MAX, dx_max=DX_MAX):
    """Real vector [Re c_kb, Im c_kb] of the monic-in-tau symbol tau^m + sum c_kb xi^b tau^k,
    zero-padded to (m_max, dx_max + 1). Padding makes equivalent structures ((1,2) with c_2 = 0
    and (1,1)) give the same vector, so the structure posterior's split over dx does not split
    the cloud."""
    V = np.zeros((m_max, dx_max + 1), complex)
    for k, c in enumerate(Q.coeffs):
        c = np.asarray(c, complex)[: dx_max + 1]
        V[k, : len(c)] = c
    return np.concatenate([V.real.ravel(), V.imag.ravel()])


@dataclass
class Cloud:
    theta: np.ndarray  # (n, d) factor coefficient vectors
    w: np.ndarray  # weight of the factor in its sample
    pi: np.ndarray  # weight of its sample
    sample: np.ndarray  # sample index
    m: np.ndarray  # tau-degree of the factor
    sympy: list
    terms: list
    track: np.ndarray = None  # matched identity across samples
    pad: tuple = (M_MAX, DX_MAX)  # (m_max, dx_max) of the zero padding of theta

    @property
    def mass(self):
        return np.nan_to_num(self.w * self.pi, nan=0.0, posinf=0.0)  # a NaN core weight carries no mass

    def __len__(self):
        return len(self.w)


def build_cloud(results):
    # padding grows with the largest factor present (the outer loop may raise the degree bounds)
    m_max, dx_max = M_MAX, DX_MAX
    for r, _ in results:
        for f in r.factors:
            m_max = max(m_max, f.symbol.m)
            dx_max = max(dx_max, max(len(c) - 1 for c in f.symbol.coeffs))
    rows = []
    for s, (r, p) in enumerate(results):
        for f in r.factors:
            rows.append((factor_vector(f.symbol, m_max, dx_max), f.weight, p, s, f.symbol.m, f.sympy, f.terms))
    if not rows:
        e = np.zeros(0)
        return Cloud(np.zeros((0, 2 * M_MAX * (DX_MAX + 1))), e, e, e.astype(int), e.astype(int), [], [])
    th, w, p, s, m, sy, te = zip(*rows)
    return Cloud(np.array(th), np.array(w, float), np.array(p, float), np.array(s), np.array(m), list(sy), list(te),
                 pad=(m_max, dx_max))


def repad(theta, pad_from, pad_to):
    """Re-pad factor vectors (rows of theta) from one (m_max, dx_max) padding to another; terms
    beyond the target padding are dropped (a factor larger than the fitted mixture's class)."""
    theta = np.atleast_2d(theta)
    (m0, d0), (m1, d1) = pad_from, pad_to
    if (m0, d0) == (m1, d1):
        return theta
    n = len(theta)
    V = theta[:, : m0 * (d0 + 1)].reshape(n, m0, d0 + 1) + 1j * theta[:, m0 * (d0 + 1):].reshape(n, m0, d0 + 1)
    W = np.zeros((n, m1, d1 + 1), complex)
    mm, dd = min(m0, m1), min(d0, d1)
    W[:, :mm, : dd + 1] = V[:, :mm, : dd + 1]
    return np.concatenate([W.real.reshape(n, -1), W.imag.reshape(n, -1)], axis=1)


# ------------------------------------------------------------------ alignment across samples
def align(cloud):
    """Track id per cloud point. The reference is the heaviest sample among those whose number of
    factors is the pi-weighted mode; every other sample is matched to the current track centroids
    by the Hungarian algorithm on coefficient distance, only within equal m (structure-aware).
    A factor opens a new track only when its sample has more factors of that m than there are
    tracks, so no distance gate is needed."""
    n = len(cloud)
    track = -np.ones(n, int)
    if n == 0:
        cloud.track = track
        return track
    samples = np.unique(cloud.sample)
    nfac = {s: int((cloud.sample == s).sum()) for s in samples}
    pis = {s: cloud.pi[cloud.sample == s][0] for s in samples}
    counts = {}
    for s in samples:
        counts[nfac[s]] = counts.get(nfac[s], 0.0) + pis[s]
    k_mode = max(counts, key=counts.get)
    order = sorted(samples, key=lambda s: (nfac[s] != k_mode, -pis[s]))
    cent, cm, cw = [], [], []  # centroid, m, accumulated mass
    for s in order:
        idx = np.where(cloud.sample == s)[0]
        for m in np.unique(cloud.m[idx]):
            ii = idx[cloud.m[idx] == m]
            tj = [j for j in range(len(cent)) if cm[j] == m]
            if tj:
                D = np.linalg.norm(cloud.theta[ii][:, None, :] - np.array([cent[j] for j in tj])[None], axis=2)
                r, c = linear_sum_assignment(D)
                for a, b in zip(r, c):
                    j = tj[b]
                    track[ii[a]] = j
                    mass = cloud.mass[ii[a]]
                    cent[j] = (cent[j] * cw[j] + cloud.theta[ii[a]] * mass) / max(cw[j] + mass, 1e-300)
                    cw[j] += mass
            for a in range(len(ii)):
                if track[ii[a]] < 0:
                    track[ii[a]] = len(cent)
                    cent.append(cloud.theta[ii[a]].copy())
                    cm.append(m)
                    cw.append(cloud.mass[ii[a]])
    cloud.track = track
    return track


# ------------------------------------------------------------------ rho from the closed form
def factor_rho(result, j):
    """rho_j = ||E_int|| / ||u_j(T) - u_j(0)|| for evolution factor j, from the closed Fourier form
    (core.components.eint_ratio, P1-T2), with u0_hat from the FFT of the component at t_0."""
    f = result.factors[j]
    if not f.terms or len(f.terms) < 2 or not result.components:
        return 0.0
    t, x = result.info["grid"]
    u0 = result.components[j][0]
    U = np.fft.fft(u0) / len(x)
    k = 2 * np.pi * np.fft.fftfreq(len(x), d=x[1] - x[0])
    keep = np.abs(U) > 1e-12 * max(np.abs(U).max(), 1e-300)
    _, rho = C.eint_ratio(f.terms, SimpleNamespace(kappa=k[keep], amp=U[keep]), t[-1] - t[0])
    return float(rho)


# ------------------------------------------------------------------ DP posterior over k
@dataclass
class DPResult:
    p_k: dict  # {k: posterior probability}
    labels: np.ndarray  # MAP cluster per cloud point (distinct within a sample)
    resp: np.ndarray  # (n, n_clusters) responsibilities (global cluster ids)
    cluster_mass: np.ndarray  # mass of W on each cluster
    means: np.ndarray  # cluster means in theta space
    models: dict = field(default_factory=dict)  # m -> (BayesianGaussianMixture, scale, offset)
    reg_covar: float = 0.0
    concentration: dict = field(default_factory=dict)  # m -> (chosen gamma_0, {gamma_0: ELBO})
    cmap: np.ndarray = None  # raw DP component -> merged cluster id
    pad: tuple = (M_MAX, DX_MAX)  # padding of the cloud it was fitted on

    @property
    def k_map(self):
        return max(self.p_k, key=self.p_k.get) if self.p_k else 0

    def predict_resp(self, theta, m, pad=None):
        """Responsibilities of new factor vectors under the fitted mixture (global cluster ids). pad:
        the (m_max, dx_max) padding of theta when it differs from the fitted cloud's."""
        theta = np.atleast_2d(theta)
        if pad is not None and len(theta):
            theta = repad(theta, pad, self.pad)
        m = np.atleast_1d(m)
        R = np.zeros((len(theta), len(self.cmap)))
        for mm, (g, mu, sd, off, keep) in self.models.items():
            sel = m == mm
            if sel.any():
                R[sel, off:off + g.n_components] = g.predict_proba((theta[sel][:, keep] - mu) / sd)
        out = np.zeros((len(theta), len(self.cluster_mass)))
        for c in range(len(self.cmap)):
            out[:, self.cmap[c]] += R[:, c]
        return out


def _within_track_var(cloud, X):
    """Median within-track variance of the standardised cloud: the empirical-Bayes floor of the
    mixture covariances (reg_covar)."""
    v = []
    for j in np.unique(cloud.track):
        sel = cloud.track == j
        if sel.sum() >= 2:
            v.append(X[sel].var(0).mean())
    return float(np.median(v)) if v else 0.0


def dp_posterior_k(cloud, tokens=1.0, n_components=8, concentration=None, draws=4000, seed=0,
                   reg_covar=1e-6):
    """Variational DP mixture (truncated stick-breaking, sklearn) fitted per tau-degree m on the
    observed factors plus tokens resampled from W with probability pi_s w_j (W is a weighted
    cloud; sklearn has no sample weights). reg_covar is only a numerical floor (standardised units): the cluster covariances are
    learned by the variational posterior. P(k): Monte Carlo over s ~ pi and labels ~ responsibilities; the factors of one sample
    are distinct factors, so each sample's labels are drawn without repetition when possible."""
    from sklearn.mixture import BayesianGaussianMixture

    rng = np.random.default_rng(seed)
    n = len(cloud)
    if n == 0:
        return DPResult({0: 1.0}, np.zeros(0, int), np.zeros((0, 0)), np.zeros(0), np.zeros((0, 0)))
    if cloud.track is None:
        align(cloud)
    S = len(np.unique(cloud.sample))
    models, blocks, off, conc = {}, [], 0, {}
    regs = []
    for m in np.unique(cloud.m):
        ii = np.where(cloud.m == m)[0]
        X = cloud.theta[ii]
        keep = np.abs(X).max(0) > 0
        if not keep.any():
            keep[:] = True
        mu = X[:, keep].mean(0)
        # one isotropic scale (RMS norm of the cloud): a coefficient weighs by its size, so
        # negligible coefficients (a 1e-4 xi^3 term in some samples) do not split a factor
        sd = np.full(keep.sum(), max(float(np.sqrt((X[:, keep] ** 2).sum(1).mean())), 1e-12))
        Z = (X[:, keep] - mu) / sd
        reg = reg_covar
        regs.append(reg)
        p = np.nan_to_num(cloud.mass[ii], nan=0.0, posinf=0.0) + 1e-300  # a zero/NaN-weight factor
        p = p / p.sum()  # still counts once (degenerate component), never breaks the draw
        # every observed factor once, plus round(tokens * n) draws proportional to pi_s w_j: the
        # mass weighting of W without inventing evidence (many duplicated tokens make the DP
        # split the noise of one factor into tight sub-clusters)
        tok = np.r_[np.arange(len(ii)), rng.choice(len(ii), size=int(round(tokens * len(ii))), p=p)]
        ntok = len(tok)
        nc = int(min(n_components, max(1, len(np.unique(np.round(Z, 8), axis=0)))))
        Zt = Z[tok] + np.sqrt(reg) * 1e-3 * rng.standard_normal((ntok, Z.shape[1]))
        grid = CONCENTRATION_GRID if concentration is None else (concentration,)
        g, elbo = None, {}
        for a in grid:  # empirical Bayes on the DP concentration: maximise the variational ELBO
            gi = BayesianGaussianMixture(
                n_components=nc, covariance_type="diag", weight_concentration_prior_type="dirichlet_process",
                weight_concentration_prior=a, reg_covar=reg, max_iter=500, n_init=3,
                random_state=seed, init_params="k-means++",
            ).fit(Zt)
            elbo[a] = gi.lower_bound_
            if g is None or gi.lower_bound_ > g.lower_bound_:
                g = gi
        conc[int(m)] = (g.weight_concentration_prior_, elbo)
        models[int(m)] = (g, mu, sd, off, keep)
        blocks.append((ii, off, g.n_components))
        off += g.n_components
    R = np.zeros((n, off))
    means = np.zeros((off, cloud.theta.shape[1]))
    for m, (g, mu, sd, o, keep) in models.items():
        ii = np.where(cloud.m == m)[0]
        Z = (cloud.theta[ii][:, keep] - mu) / sd
        R[ii, o:o + g.n_components] = g.predict_proba(Z)
        means[o:o + g.n_components][:, keep] = g.means_ * sd + mu
    # MAP labels, distinct within a sample (Hungarian on -log responsibility)
    labels = np.zeros(n, int)
    for s in np.unique(cloud.sample):
        ii = np.where(cloud.sample == s)[0]
        cost = -np.log(np.maximum(R[ii], 1e-300))
        r, c = linear_sum_assignment(cost)
        labels[ii[r]] = c
    # merge over-split clusters (DPM inconsistency): BIC test with the pooled within-cluster variance
    Zall = np.zeros((n, cloud.theta.shape[1]))
    for m, (g, mu, sd, o, keep) in models.items():
        ii = np.where(cloud.m == m)[0]
        Zall[np.ix_(ii, np.where(keep)[0])] = (cloud.theta[ii][:, keep] - mu) / sd
    cmap = merge_clusters(Zall, labels, cloud.sample, off)
    labels = cmap[labels]
    nC = int(cmap.max()) + 1
    Rm = np.zeros((n, nC))
    for c in range(off):
        Rm[:, cmap[c]] += R[:, c]
    mw = np.array([cloud.mass[labels == c].sum() for c in range(nC)])
    means = np.array([np.average(cloud.theta[labels == c], 0, cloud.mass[labels == c] + 1e-300) if (labels == c).any()
                      else np.zeros(cloud.theta.shape[1]) for c in range(nC)])
    R, off = Rm, nC
    mass = mw
    mass = mass / max(mass.sum(), 1e-300)
    # Monte Carlo posterior over k
    samples = np.unique(cloud.sample)
    ps = np.array([cloud.pi[cloud.sample == s][0] for s in samples])
    ps = ps / ps.sum()
    counts = {}
    for _ in range(draws):
        s = samples[rng.choice(len(samples), p=ps)]
        used = set()
        for i in np.where(cloud.sample == s)[0]:
            r = R[i].copy()
            if used and r[[c for c in range(off) if c not in used]].sum() > 0:
                r[list(used)] = 0.0  # distinct factors of one sample -> distinct clusters
            r = r / r.sum()
            used.add(int(rng.choice(off, p=r)))
        counts[len(used)] = counts.get(len(used), 0) + 1
    p_k = {k: v / draws for k, v in sorted(counts.items())}
    res = DPResult(p_k, labels, R, mass, means, models, float(np.median(regs)), conc, cmap, pad=cloud.pad)
    return res


def merge_clusters(Z, labels, sample, n_comp):
    """Greedy merge of DP clusters. Two clusters are candidates only if no sample has a factor in
    both (the factors of one sample are distinct factors). A pair is merged when BIC prefers one
    mean over two, with a covariance shared by the pair and estimated under each model (ML):
    dBIC = n log(det S1 / det S2) - (d + 1) log n. The covariance is full, because fitted
    coefficients are strongly correlated (corr(c_0, c_2) = 0.97 on heat), and diagonal when the
    pair has too few points (n <= d + 1). This is a finite-mixture test, consistent
    in the number of clusters, unlike the DP count (Miller & Harrison 2013). Returns the map
    raw component -> merged id (compact)."""
    groups = {c: np.where(labels == c)[0] for c in np.unique(labels)}
    parent = np.arange(n_comp)
    dims = np.abs(Z).max(0) > 0
    d = int(dims.sum())
    ss = lambda I: ((Z[I][:, dims] - Z[I][:, dims].mean(0)) ** 2).sum(0)

    def scat(I):
        Y = Z[I][:, dims] - Z[I][:, dims].mean(0)
        return Y.T @ Y
    while d > 0:
        ids = sorted(groups)
        best = None
        for i in range(len(ids)):
            for j in range(i + 1, len(ids)):
                A, B = groups[ids[i]], groups[ids[j]]
                if set(sample[A]) & set(sample[B]):
                    continue
                U = np.r_[A, B]
                v1, v2 = ss(U), ss(A) + ss(B)
                ok = v1 > 0
                pen = (d + 1) * np.log(len(U))
                if not ok.any():
                    score = -np.inf  # identical points
                elif len(U) > d + 1:
                    S1, S2 = scat(U), scat(A) + scat(B)
                    eps = 1e-12 * np.trace(S1) / d
                    l1 = np.linalg.slogdet(S1 + eps * np.eye(d))[1]
                    l2 = np.linalg.slogdet(S2 + eps * np.eye(d))[1]
                    score = len(U) * (l1 - l2) - pen
                else:
                    score = len(U) * np.log(v1[ok] / np.maximum(v2[ok], 1e-300)).sum() - pen
                if score < 0 and (best is None or score < best[0]):
                    best = (score, ids[i], ids[j])
        if best is None:
            break
        _, a, b = best
        groups[a] = np.r_[groups[a], groups.pop(b)]
        parent[parent == b] = a
    used = np.unique(parent)
    return np.searchsorted(used, parent)


def finite_k_posterior(cloud, k_max=4, seed=0):
    """BIC (Laplace) posterior over the number of Gaussian clusters of the unique cloud points,
    finite mixtures k = 1..k_max, per m block summed. The consistent counterpart of the DP count."""
    from sklearn.mixture import GaussianMixture

    if len(cloud) == 0:
        return {0: 1.0}
    X = cloud.theta.copy()
    keep = X.std(0) > 0
    if not keep.any():
        return {1: 1.0}
    Z = (X[:, keep] - X[:, keep].mean(0)) / X[:, keep].std(0)
    Z = np.c_[Z, 10.0 * cloud.m]  # m separates exactly
    reg = max(_within_track_var(cloud, Z), 1e-6) if cloud.track is not None else 1e-6
    bic = {}
    for k in range(1, min(k_max, len(Z)) + 1):
        g = GaussianMixture(k, covariance_type="diag", reg_covar=reg, n_init=3, random_state=seed).fit(Z)
        bic[k] = g.bic(Z)
    b = np.array(list(bic.values()))
    p = np.exp(-(b - b.min()) / 2)
    p /= p.sum()
    return dict(zip(bic.keys(), p))


# ------------------------------------------------------------------ the aggregate
@dataclass
class Dist:
    """A sampled quantity: values with weights pi_s (Monte Carlo, never linearised)."""
    values: np.ndarray
    weights: np.ndarray

    @property
    def mean(self):
        v, w = self._ok()
        return float(np.sum(v * w) / w.sum()) if len(v) else float("nan")

    def quantile(self, q):
        v, w = self._ok()
        if not len(v):
            return float("nan")
        o = np.argsort(v)
        c = np.cumsum(w[o]) / w.sum()
        return float(v[o][np.searchsorted(c, q, side="left").clip(0, len(v) - 1)])

    def _ok(self):
        ok = np.isfinite(self.values)
        return self.values[ok], self.weights[ok]


@dataclass
class Aggregate:
    cloud: Cloud
    W_track: np.ndarray
    theta_bar: np.ndarray
    Sigma: np.ndarray
    track_sympy: list
    k_eff: float
    k_det: int
    k_eff_s: Dist
    rho: Dist
    cF: Dist
    gamma: Dist
    cooccurrence: np.ndarray  # P(cluster a and cluster b both present in a sample), DP cluster ids
    track_cooccurrence: np.ndarray  # same, on the tracks (= DP clusters when the DP is fitted)
    structures_pooled: dict
    k_structure: dict
    labels: dict  # pooled core labels {label: p}
    dp: DPResult = None
    finite_k: dict = None

    def summary(self):
        lines = [f"k_eff={self.k_eff:.3f} (k_det={self.k_det}); per-sample k_eff mean {self.k_eff_s.mean:.3f}",
                 f"rho_bar={self.rho.mean:.3g} cF_bar={self.cF.mean:.3g} gamma_bar={self.gamma.mean:.3g}",
                 f"labels={self.labels}",
                 f"P(k) structures={ {k: round(v, 3) for k, v in self.k_structure.items()} }"]
        if self.dp is not None:
            lines.append(f"P(k) DP={ {k: round(v, 3) for k, v in self.dp.p_k.items()} } "
                         f"finite-BIC={ {k: round(v, 3) for k, v in (self.finite_k or {}).items()} }")
        for j, W in enumerate(self.W_track):
            lines.append(f"  track {j}: W={W:.3f} {self.track_sympy[j]}")
        return "\n".join(lines)


def _entropy_exp(p):
    p = np.asarray(p, float)
    p = p[p > 0] / p[p > 0].sum() if p.sum() > 0 else p
    return float(np.exp(-(p * np.log(p)).sum())) if len(p) else 0.0


def _cooc(labels, cloud, n):
    M = np.zeros((n, n))
    tot = 0.0
    for s in np.unique(cloud.sample):
        sel = cloud.sample == s
        p = cloud.pi[sel][0]
        tot += p
        present = np.unique(labels[sel])
        M[np.ix_(present, present)] += p
    return M / max(tot, 1e-300)


def aggregate(results, dp=True, **dp_kw):
    """Build W and its statistics from [(StructResult, pi_s)]."""
    pis = np.array([p for _, p in results], float)
    pis = pis / pis.sum()
    results = [(r, p) for (r, _), p in zip(results, pis)]
    cloud = build_cloud(results)
    align(cloud)
    dpres = None
    if dp and len(cloud):
        # with the DP fitted, a track is a DP cluster: matching across samples by (Mahalanobis)
        # coefficient distance, within equal m, distinct within a sample (Hungarian). The ungated
        # Hungarian tracks would merge different laws that share m (e.g. transport and heat).
        dpres = dp_posterior_k(cloud, **dp_kw)
        cloud.track = dpres.labels.copy()
    used = np.unique(cloud.track)
    cloud.track = np.searchsorted(used, cloud.track)  # compact ids
    nt = len(used)
    W = np.array([cloud.mass[cloud.track == j].sum() for j in range(nt)])
    Wn = W / W.sum() if W.sum() > 0 else W
    theta_bar = np.array([np.average(cloud.theta[cloud.track == j], 0, cloud.mass[cloud.track == j] + 1e-300)
                          for j in range(nt)]).reshape(nt, cloud.theta.shape[1])  # nt = 0: empty cloud
    Sigma = np.array([np.cov(cloud.theta[cloud.track == j].T, aweights=cloud.mass[cloud.track == j] + 1e-300)
                      if (cloud.track == j).sum() > 1 else np.zeros((cloud.theta.shape[1],) * 2)
                      for j in range(nt)]).reshape(nt, cloud.theta.shape[1], cloud.theta.shape[1])
    track_sympy = [cloud.sympy[int(np.argmax(np.where(cloud.track == j, cloud.mass, -1)))] for j in range(nt)]
    k_eff = _entropy_exp(Wn)
    k_s, rho, cF, gam = [], [], [], []
    structs, kst, labs = {}, {}, {}
    for r, p in results:
        w = np.array([f.weight for f in r.factors])
        k_s.append(_entropy_exp(w) if len(w) else np.nan)
        rho.append(float(sum(f.weight * factor_rho(r, j) for j, f in enumerate(r.factors))) if r.factors else np.nan)
        cF.append(r.cF if r.factors else np.nan)
        gam.append(r.gamma if r.factors else np.nan)
        labs[r.label] = labs.get(r.label, 0.0) + p
        for st, _, q in r.structures:
            structs[st] = structs.get(st, 0.0) + p * q
            kst[len(st)] = kst.get(len(st), 0.0) + p * q
    structs = dict(sorted(structs.items(), key=lambda kv: -kv[1]))
    out = Aggregate(
        cloud, Wn, theta_bar, Sigma, track_sympy, k_eff, int(ceil(k_eff - 1e-9)) if k_eff > 0 else 0,
        Dist(np.array(k_s), pis), Dist(np.array(rho), pis), Dist(np.array(cF), pis), Dist(np.array(gam), pis),
        np.zeros((0, 0)), _cooc(cloud.track, cloud, nt) if nt else np.zeros((0, 0)),
        structs, dict(sorted(kst.items())), labs,
    )
    if dpres is not None:
        out.dp = dpres
        out.cooccurrence = _cooc(dpres.labels, cloud, dpres.resp.shape[1])
        out.finite_k = finite_k_posterior(cloud)
    return out
