"""Core v2 (plan v2.1): structured factor fit with Bayesian model comparison.

Instead of fitting one P and factoring it with a fixed tolerance (ill-posed on float
coefficients; no data-free threshold, CONV-T5), every candidate factor structure is fitted
directly on the dispersion points (k-varieties alternating regression) and the structures are
compared by BIC (Laplace approximation of the evidence). Residuals are in units of each
point's own uncertainty sigma_lam (Cramer-Rao bound of the exponentials in its FFT bin).

Also here:
- per-bin pencil order chosen by an information criterion (extract_modes_ic);
- a confluent-mode test (A + B t) e^{lam t} per bin: a repeated factor Q^2 has no finite
  test (OPF5B-T6), so when the confluent model wins the output is UNDECIDED with a reason.

Prototype and evidence: analysis/exp/structfit.py, e1b_structfit.py, e4_theory.py.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from itertools import product

import numpy as np
from scipy.optimize import least_squares, minimize

from . import components as C
from .spectral import Modes, fft_x, matrix_pencil
from .variety import fit_monic


# ------------------------------------------------------------------ modes with order selection
class BinNoise:
    """Noise of the FFT-bin time series y_k(t), k = bin index.

    White (default): one std per bin, sigma[k]; whitening is 1 / sigma[k] and every formula below
    reduces to the plain least-squares one. Correlated: a stationary autocovariance in t per bin,
    acov[k, lag], estimated from draws of the noise field (e.g. GP posterior sample deviations, whose
    error is smooth in t: S-INTERP REPORT sec. 4). Then the bin fits are generalised least squares:
    residuals and Fisher matrices are whitened by L_k^{-1}, L_k the Cholesky factor of the Toeplitz
    covariance. A smooth error then counts as a few effective observations instead of nt, so the
    order criterion stops reading it as extra exponentials (plan v2.9, per-bin noise)."""

    JITTER = 1e-3  # relative diagonal load of the Toeplitz covariance (numerical conditioning only)

    def __init__(self, sigma, acov=None):
        self.sigma = np.asarray(sigma, float)
        self.acov = acov
        self._W = {}

    @classmethod
    def from_draws(cls, draws, x, noise=0.0, window=None, pad=1, floor=0.0):
        """Autocovariance per bin from noise draws (R, nt, nx), in the core's own FFT normalisation;
        a white part noise / sqrt(nx) (measurement noise, independent of the draws) adds to lag 0."""
        D = np.stack([fft_x(np.asarray(d), x, window=window, pad=pad)[1] for d in draws])  # (R, nt, nb)
        R, nt, nb = D.shape
        acov = np.stack([np.einsum("rtk,rtk->k", D[:, L:], D[:, : nt - L].conj()) / (R * nt)
                         for L in range(nt)], axis=1)  # biased estimator: positive semidefinite
        nx = np.asarray(draws[0]).shape[1]
        acov[:, 0] += (noise / np.sqrt(nx)) ** 2 if noise > 0 else 0.0
        acov[:, 0] = np.maximum(acov[:, 0].real, floor**2)
        return cls(np.sqrt(acov[:, 0].real), acov)

    def W(self, k, n):
        """Whitening for bin k on n time samples: a scalar (white) or an (n, n) matrix. Stationary
        model: any window of n consecutive samples has the same covariance."""
        if self.acov is None:
            return 1.0 / self.sigma[k]
        key = (k, n)
        if key not in self._W:
            from scipy.linalg import cholesky, solve_triangular, toeplitz

            c = self.acov[k, :n]
            C = toeplitz(c, c.conj()) + self.JITTER * c[0].real * np.eye(n)
            L = cholesky(C, lower=True)
            self._W[key] = solve_triangular(L, np.eye(n), lower=True)
        return self._W[key]

    def scalar(self):
        return float(np.median(self.sigma))


def _apply(W, a):
    return W * a if np.isscalar(W) else W @ a


def _bin_rss(y, tt, lam, W=None):
    """Least squares of one bin on exponentials; with whitening W the RSS is the whitened (GLS) one."""
    Z = np.exp(np.outer(tt, lam))
    if W is None:
        a, *_ = np.linalg.lstsq(Z, y, rcond=None)
        r = y - Z @ a
    else:
        Zw, yw = _apply(W, Z), _apply(W, y)
        a, *_ = np.linalg.lstsq(Zw, yw, rcond=None)
        r = yw - Zw @ a
    return float(np.vdot(r, r).real), a


def varpro_refine(y, tt, lam, W=None):
    """Maximum-likelihood poles for one bin (white Gaussian noise): variable projection
    (Golub-Pereyra), amplitudes projected out, Levenberg-Marquardt on (Re lam, Im lam) started
    at the pencil poles. The pencil is not ML and its decay rates are biased at low SNR; the ML
    poles are asymptotically unbiased and reach the CRB that sigma_lambda assumes (plan v2.9.1).
    Falls back to the pencil poles if the refinement does not lower the RSS."""
    from scipy.optimize import least_squares

    lam = np.asarray(lam, complex)
    if len(lam) == 0:
        return lam
    r0 = len(lam)

    def res(v):
        lm = v[:r0] + 1j * v[r0:]
        Z = np.exp(np.outer(tt, lm))
        Zw, yw = (Z, y) if W is None else (_apply(W, Z), _apply(W, y))
        a, *_ = np.linalg.lstsq(Zw, yw, rcond=None)
        r = yw - Zw @ a
        return np.r_[r.real, r.imag]

    v0 = np.r_[lam.real, lam.imag]
    rss0 = float(np.sum(res(v0) ** 2))
    try:
        sol = least_squares(res, v0, method="lm", xtol=1e-12, ftol=1e-14, max_nfev=200 * len(v0))
    except (np.linalg.LinAlgError, ValueError):
        return lam
    if not np.all(np.isfinite(sol.x)) or 2 * sol.cost > rss0:
        return lam
    return sol.x[:r0] + 1j * sol.x[r0:]


# Optional learned proposal of pole sets per bin (Phase 4 L0, pdefactor.learned.expseeds). None is
# the deterministic pipeline. A provider is called as provider(y, dt, sigma) -> list of complex pole
# arrays. Honesty rule (PHASE4 C(2)): a seed never adds an order outside the pencil's r0..r0+extra
# (the order IC keeps its search space), at most one seed per order is used, and every order in that
# range then gets the same number of starts (an order without a seed gets a second pencil start with
# a shorter pencil parameter), so no order wins by extra optimisation.
SEED_PROVIDER = None


def extract_modes_ic(u, t, x, noise=0.0, snr_min=3.0, window=None, pad=1, max_order=8, extra=2,
                     refine=False, noise_draws=None, seeds=None):
    """Dispersion points like spectral.extract_modes, but in each bin the pencil order is the
    one with the lowest BIC among r0..r0+extra (r0 = Hankel rank above the noise), so that an
    exponential merged into another one (unresolved) gets its own pole when the data support it.
    refine=True replaces the pencil poles by the ML (VarPro) poles before the order comparison.
    noise_draws: optional draws (R, nt, nx) of the noise field (e.g. sqrt(2) x the deviations of GP
    posterior samples from their mean); the bins are then fitted by GLS with the per-bin
    autocovariance estimated from them (BinNoise), added to the white part `noise`.
    seeds: a seed provider (see SEED_PROVIDER; None uses the module default, False disables it).
    Returns (Modes, BinNoise, kappa grid, U)."""
    provider = SEED_PROVIDER if seeds is None else (seeds or None)
    dt = t[1] - t[0]
    tt = t - t[0]
    kappa, U = fft_x(u, x, window=window, pad=pad)
    nx = u.shape[1]
    floor = 1e-9 * np.abs(U).max()
    if noise_draws is None:
        bn = BinNoise(np.full(len(kappa), max(noise / np.sqrt(nx) if noise > 0 else 0.0, floor / snr_min)))
    else:
        bn = BinNoise.from_draws(noise_draws, x, noise=noise, window=window, pad=pad, floor=floor / snr_min)
    rows = []
    nobs = 2 * len(t)
    for k in range(len(kappa)):
        y = U[:, k]
        level = np.abs(y).max()
        sk = bn.sigma[k]
        if level == 0 or level < snr_min * sk:
            continue
        W = bn.W(k, len(t))
        tol = max(1e-6, snr_min * sk / level)
        lam0, _, s = matrix_pencil(y, dt, rel_tol=tol, max_order=max_order)
        best = None
        orders = range(max(len(lam0), 1), min(len(lam0) + extra, max_order) + 1)
        cands = [(r, lam0 if r == len(lam0) else matrix_pencil(y, dt, order=r)[0]) for r in orders]
        if provider is not None:
            seeded = {}
            for p in provider(y, dt, sk):
                p = np.asarray(p, complex)
                if len(p) in orders and len(p) not in seeded and np.all(np.isfinite(p)):
                    seeded[len(p)] = p
            cands += [(r, seeded[r] if r in seeded else matrix_pencil(y, dt, order=r, pencil=len(y) // 3)[0])
                      for r in orders]
        for r, lam in cands:
            if refine:
                lam = varpro_refine(y, tt, lam, W)
            rss, a = _bin_rss(y, tt, lam, W)  # whitened: rss is already in noise units
            bic = rss + 4 * r * np.log(nobs)
            if best is None or bic < best[0]:
                best = (bic, lam, a)
        _, lam, amp = best
        for lm, a in zip(lam, amp):
            snr = abs(a) / sk
            if abs(a) * np.exp(np.real(lm) * tt[-1] / 2) > snr_min * sk / 3:
                rows.append((kappa[k], lm, a, k, snr))
    if not rows:
        e = np.zeros(0)
        return Modes(e, e.astype(complex), e.astype(complex), e.astype(int), e), bn, kappa, U
    k_, l_, a_, i_, s_ = map(np.array, zip(*rows))
    m = Modes(k_.astype(float), l_.astype(complex), a_.astype(complex), i_.astype(int), s_.astype(float))
    return m, bn, kappa, U


# ------------------------------------------------------------------ uncertainty of each point
def sigma_lambda(modes, t, bin_noise, floor=1e-9):
    """CRB std of lam for each mode: full Fisher of all (A_j, lam_j) sharing the same FFT bin,
    so that interference between exponentials in one bin is accounted for. bin_noise: a scalar
    std (white, same in every bin) or a BinNoise (per bin, possibly correlated in t: GLS Fisher)."""
    tt = t - t[0]
    out = np.full(len(modes), np.inf)
    for k in np.unique(modes.kidx):
        idx = np.where(modes.kidx == k)[0]
        cols = []
        for i in idx:
            g = np.exp(modes.lam[i] * tt)
            cols += [g, modes.amp[i] * tt * g]
        J = np.stack(cols, axis=1)
        if isinstance(bin_noise, BinNoise):
            J, scale = _apply(bin_noise.W(k, len(tt)), J), 1.0
        else:
            scale = bin_noise
        try:
            Cm = np.linalg.inv(J.conj().T @ J)
        except np.linalg.LinAlgError:
            continue
        for r, i in enumerate(idx):
            out[i] = np.sqrt(max(np.real(Cm[2 * r + 1, 2 * r + 1]), 0)) * scale
    scale = np.abs(modes.lam).max() if len(modes) else 1.0
    return np.maximum(out, floor * max(scale, 1.0))


def _dist(Q, lam, kappa):
    """First-order distance in lam from the point to the variety {Q = 0}: |Q| / |dQ/dtau|."""
    xi_ = 1j * kappa
    v = Q(lam, xi_)
    h = 1e-6 * (1 + np.abs(lam))
    d = (Q(lam + h, xi_) - Q(lam - h, xi_)) / (2 * h)
    return np.abs(v) / np.maximum(np.abs(d), 1e-12)


# ------------------------------------------------------------------ structured fit
@dataclass
class Fit:
    structure: tuple  # ((m_1, dx_1), ..., (m_k, dx_k))
    factors: list
    labels: np.ndarray
    D: np.ndarray  # distances in sigma units, (n_modes, k)
    chi2: float
    scale2: float  # robust noise scale s^2 >= 1
    nparam: int
    bic: float


def _fit_factor(lam, kappa, w, m, dx, real):
    if len(lam) < m * (dx + 1) + 1:
        return None
    P, _, _ = fit_monic(lam, kappa, m, dx, w, real)
    return P


def fit_structure(lam, kappa, sig, structure, real=False, inits=8, iters=30, seed=0, cap=3.0):
    """Alternating k-varieties regression for one structure; best Fit over initialisations."""
    rng = np.random.default_rng(seed)
    n = len(lam)
    k = len(structure)
    w = 1.0 / sig
    best = None
    init_labels = []
    # deterministic inits: sort branches at each kappa by Im lam, then by Re lam
    for key in (np.imag, np.real):
        lab = np.zeros(n, int)
        for kv in np.unique(kappa):
            idx = np.where(kappa == kv)[0]
            order = idx[np.argsort(key(lam[idx]))]
            for r, i in enumerate(order):
                lab[i] = min(r, k - 1)
        init_labels.append(lab)
    init_labels += [rng.integers(0, k, n) for _ in range(inits)]
    for lab in init_labels:
        lab = lab.copy()
        facs = None
        for _ in range(iters):
            new = []
            for j, (m, dx) in enumerate(structure):
                sel = lab == j
                Q = _fit_factor(lam[sel], kappa[sel], w[sel], m, dx, real)
                if Q is None:
                    break
                new.append(Q)
            if len(new) < k:
                break
            facs = new
            D = np.stack([_dist(Q, lam, kappa) for Q in facs], axis=1) / sig[:, None]
            nl = D.argmin(1)
            if np.array_equal(nl, lab):
                break
            lab = nl
        if facs is None or len(facs) < k:
            continue
        D = np.stack([_dist(Q, lam, kappa) for Q in facs], axis=1) / sig[:, None]
        # robust: a uniform background class caps each point at z^2 = (cap s)^2, with s >= 1 a
        # robust scale of the residuals (median of chi^2_1 is 0.455)
        z2 = D.min(1) ** 2
        s2 = max(1.0, float(np.median(z2)) / 0.455)
        chi2 = float(np.minimum(z2, cap**2 * s2).sum())
        npar = sum(m * (dx + 1) for m, dx in structure) * (1 if real else 2)
        nn = 2 * n
        # noise scale s >= 1 (cannot beat the CRB), Jeffreys on s: n log(max(chi2/n, 1))
        bic = nn * np.log(max(chi2 / nn, 1.0)) + npar * np.log(nn)
        if best is None or bic < best.bic:
            best = Fit(tuple(structure), facs, D.argmin(1), D, chi2, s2, npar, bic)
    return best


def candidate_structures(m_max=3, dx_max=4, deg_options=None):
    """Every canonical structure ((m_j, dx_j), ...) with sum m_j <= m_max. deg_options: allowed
    orders of one irreducible factor; default every order up to m_max (an irreducible law of order 3
    in tau is a candidate; v2.13 G1)."""
    if deg_options is None:
        deg_options = tuple(range(1, m_max + 1))
    out = []
    for k in range(1, m_max + 1):
        for degs in product(deg_options, repeat=k):
            if sum(degs) > m_max or list(degs) != sorted(degs):
                continue
            for dxs in product(range(dx_max + 1), repeat=k):
                st = tuple(zip(degs, dxs))
                if list(st) != sorted(st):  # canonical order, no duplicates
                    continue
                out.append(st)
    return out


def select(modes, t, bin_noise, m_max=3, dx_max=4, real=False, structures=None):
    """All structures, BIC-ranked: (best Fit, [(structure, bic, posterior weight)], sigma_lam).
    `structures`: restrict the comparison to these (e.g. the outer loop's regroup at fixed k)."""
    sig = sigma_lambda(modes, t, bin_noise)
    fits = []
    for st in (candidate_structures(m_max, dx_max) if structures is None else structures):
        f = fit_structure(modes.lam, modes.kappa, sig, st, real=real)
        if f is not None:
            fits.append(f)
    if not fits:
        return None, [], sig
    fits.sort(key=lambda f: f.bic)
    b = np.array([f.bic for f in fits])
    p = np.exp(-(b - b.min()) / 2)
    p /= p.sum()
    return fits[0], [(f.structure, f.bic, pi) for f, pi in zip(fits, p)], sig


# ------------------------------------------------------------------ repeated roots
def confluent_test(modes, t, U, bin_noise, sep=4.0):
    """For each bin with two close poles (|d lam| < sep / T), compare by BIC the simple model
    (two exponentials, poles refined) with the confluent one (A + B t) e^{lam t} (one pole fewer).
    Returns a list of (kappa, lam, delta_bic) for the bins where the confluent model wins."""
    tt = t - t[0]
    T = tt[-1]
    nobs = 2 * len(t)
    out = []
    if not isinstance(bin_noise, BinNoise):
        bin_noise = BinNoise(np.full(U.shape[1], float(bin_noise)))
    for k in np.unique(modes.kidx):
        idx = np.where(modes.kidx == k)[0]
        if len(idx) < 2:
            continue
        lam = modes.lam[idx]
        d = np.abs(lam[:, None] - lam[None, :]) + np.eye(len(lam)) * 1e300
        i, j = np.unravel_index(np.argmin(d), d.shape)
        if d[i, j] > sep / T:
            continue
        y = U[:, k]
        Wk = bin_noise.W(k, len(tt))
        others = np.delete(lam, [i, j])

        yw = _apply(Wk, y)

        def res_simple(v):
            Zw = _apply(Wk, np.exp(np.outer(tt, np.r_[others, v[0] + 1j * v[1], v[2] + 1j * v[3]])))
            a, *_ = np.linalg.lstsq(Zw, yw, rcond=None)
            r = yw - Zw @ a
            return np.r_[r.real, r.imag]

        def res_conf(v):
            lc = v[0] + 1j * v[1]
            Z = np.concatenate([np.exp(np.outer(tt, others)), np.exp(lc * tt)[:, None], (tt * np.exp(lc * tt))[:, None]], 1)
            Zw = _apply(Wk, Z)
            a, *_ = np.linalg.lstsq(Zw, yw, rcond=None)
            r = yw - Zw @ a
            return np.r_[r.real, r.imag]

        def best(res, v0):
            # variable projection: the amplitudes are solved exactly, the poles by Levenberg-Marquardt
            # from the pencil start (smooth least squares; the start is kept if it is better)
            r0 = res(v0)
            try:
                f = least_squares(res, v0, method="lm", xtol=1e-12, ftol=1e-15, gtol=1e-15, max_nfev=400).fun
            except (ValueError, np.linalg.LinAlgError):
                f = r0
            rss = float(f @ f) if np.all(np.isfinite(f)) else np.inf
            return min(rss, float(r0 @ r0))

        li, lj = lam[i], lam[j]
        rs = best(res_simple, np.array([li.real, li.imag, lj.real, lj.imag]))
        lc = (li + lj) / 2
        rc = best(res_conf, np.array([lc.real, lc.imag]))
        # simple: 2 amplitudes + 2 poles = 8 real parameters; confluent: 2 amplitudes + 1 pole = 6
        dbic = (rc - rs) - 2 * np.log(nobs)  # whitened RSS: already in noise units
        if dbic < 0:
            out.append((float(modes.kappa[idx[0]]), complex(lc), float(dbic)))
    return out


def _branch_point(conf, symbols, modes, T, sep=4.0):
    """A confluent bin (kappa, lam, dbic) is explained by a fitted factor Q of order >= 2 when two of
    Q's own roots at that kappa lie within sep / T of each other and of lam: a branch point of an
    irreducible variety, where the discriminant of Q in tau vanishes. A squarefree Q has a discriminant
    with finitely many zeros (a polynomial in xi, not identically 0), so its roots are close at a few
    kappa only; a repeated factor (Q = R^2, OPF5B-T6) has close roots at every kappa. Q explains the bin
    only if its roots are close at fewer than half of the observed |kappa| (v2.13: damped beam)."""
    kap, lam = conf[0], conf[1]
    ks = np.unique(np.abs(modes.kappa))
    for Q in symbols:
        if Q.m < 2:
            continue
        r = Q.roots(1j * kap)
        d = np.abs(r[:, None] - r[None, :]) + np.eye(len(r)) * 1e300
        i, j = np.unravel_index(np.argmin(d), d.shape)
        if d[i, j] > sep / T or abs((r[i] + r[j]) / 2 - lam) > sep / T:
            continue
        close = 0
        for k in ks:
            rk = Q.roots(1j * k)
            dk = np.abs(rk[:, None] - rk[None, :]) + np.eye(len(rk)) * 1e300
            close += dk.min() <= sep / T
        if close < 0.5 * len(ks):
            return True
    return False


# ------------------------------------------------------------------ real field, half plane (T98)
def half_plane(modes, tol=1e-12):
    """The modes of a real field on one half of the signed wavenumbers: kappa > 0, plus the kappa = 0
    modes with Im lam >= 0. The FFT of a real field is Hermitian, U(-kappa) = conj U(kappa), so the
    kappa < 0 modes are the conjugates of the kappa > 0 ones and carry no new information. If A is the
    minimal (in general complex) annihilator of the half-plane modes, the mirror's is conj A and the
    field's real annihilator is lcm(A, conj A). On the full signed set a complex-coefficient fit needs
    separate factors for the mirror (twice the factors: the class bound hides the pair) and a real fit
    must follow the observed sheet, which switches from A to conj A at the double point kappa = 0
    (A = tau - i c xi^2: lam = -i c kappa |kappa|, not a polynomial branch, so approximated by odd
    powers of xi). On the half plane A is fitted at its own degree. kappa = 0 is its own mirror (its
    modes come in conjugate pairs): one of each pair is kept."""
    keep = (modes.kappa > tol) | ((np.abs(modes.kappa) <= tol) & (modes.lam.imag >= -tol))
    return modes.subset(keep)


def real_restrict(best, modes, sig, cap=3.0):
    """Half-plane fit of a real field: a factor A with conj A = A (a real factor, e.g. transport) is the
    nested real-coefficient model (half the parameters). Each factor is refitted with real coefficients
    on its own modes (on the half plane the mirror adds nothing: |R(conj lam, -i kappa)| = |R(lam, i kappa)|
    for real R) and kept real when the structure's BIC (same formula as fit_structure) is lower."""
    lam, kappa = modes.lam, modes.kappa
    w = 1.0 / sig
    nn = 2 * len(lam)
    facs = list(best.factors)
    real_f = [False] * len(facs)

    def score(fs, rf):
        D = np.stack([_dist(Q, lam, kappa) for Q in fs], axis=1) / sig[:, None]
        z2 = D.min(1) ** 2
        s2 = max(1.0, float(np.median(z2)) / 0.455)
        chi2 = float(np.minimum(z2, cap**2 * s2).sum())
        npar = sum(m * (dx + 1) * (1 if r else 2) for (m, dx), r in zip(best.structure, rf))
        return nn * np.log(max(chi2 / nn, 1.0)) + npar * np.log(nn), D, chi2, s2, npar

    cur = score(facs, real_f)
    for j, (m, dx) in enumerate(best.structure):
        sel = best.labels == j
        Q = _fit_factor(lam[sel], kappa[sel], w[sel], m, dx, True)
        if Q is None:
            continue
        fs, rf = facs[:j] + [Q] + facs[j + 1:], real_f[:j] + [True] + real_f[j + 1:]
        sc = score(fs, rf)
        if sc[0] < cur[0]:
            facs, real_f, cur = fs, rf, sc
    if not any(real_f):
        return best
    bic, D, chi2, s2, npar = cur
    return Fit(best.structure, facs, D.argmin(1), D, chi2, s2, npar, bic)


# ------------------------------------------------------------------ entry point
@dataclass
class StructResult:
    label: str
    factors: list = field(default_factory=list)  # FactorResult (same type as core v1)
    structures: list = field(default_factory=list)  # [(structure, bic, posterior weight)], best first
    gamma: float = 1.0
    cF: float = 0.0
    n_shared: int = 0
    n_modes: int = 0
    scale2: float = 1.0
    confluent: list = field(default_factory=list)
    info: dict = field(default_factory=dict)
    components: list = field(default_factory=list)

    def summary(self):
        top = self.structures[0] if self.structures else None
        lines = [f"label={self.label} modes={self.n_modes} best={top[0] if top else None} "
                 f"p={top[2] if top else 0:.3f} s^2={self.scale2:.3g}",
                 f"gamma_N={self.gamma:.4g} c_F={self.cF:.4g} shared={self.n_shared} confluent={len(self.confluent)}"]
        for f in self.factors:
            lines.append(f"  w={f.weight:.4f} Q={f.sympy} terms={f.terms} nk={f.n_kappa} id={f.identifiable}")
        if self.info.get("reason"):
            lines.append(f"  reason: {self.info['reason']}")
        return "\n".join(lines)


def analyze_structured(u, t, x, noise=0.0, *, m_max=3, dx_max=4, snr_min=3.0, window=None,
                       real=False, share_z=3.0, outlier_frac_misfit=0.5, want_components=False,
                       refine=False, structures=None, noise_draws=None, half=False):
    """Core v2: modes (order by BIC) -> structured fit with posterior over structures ->
    confluent test -> components, weights, gamma_N. Labels as in core v1 (sec. 0.5), plus
    UNDECIDED when a confluent mode wins (repeated factor, OPF5B-T6). noise_draws: draws of a
    correlated noise field (see extract_modes_ic); the bin fits then use GLS.
    half=True (real data, complex-coefficient fit; T98): only the half-plane modes are fitted
    (half_plane) and each factor of the best fit is replaced by its real-coefficient restriction when
    that lowers the BIC (real_restrict)."""
    from .analyze import FactorResult  # local import: analyze imports this module's siblings

    modes, bin_noise, _, U = extract_modes_ic(u, t, x, noise=noise, snr_min=snr_min, window=window,
                                              refine=refine, noise_draws=noise_draws)
    half = bool(half and np.isrealobj(u) and not real)
    if half:
        modes = half_plane(modes)
    if len(modes) == 0:
        return StructResult("UNDECIDED", info={"reason": "no modes above noise"})
    best, ranked, sig = select(modes, t, bin_noise, m_max=m_max, dx_max=dx_max, real=real, structures=structures)
    if best is None:
        return StructResult("UNDECIDED", n_modes=len(modes), info={"reason": "too few modes for any structure"})
    if half:
        best = real_restrict(best, modes, sig)
    facs = best.factors
    D = best.D
    shared = (D < share_z).sum(1) > 1
    fields = C.component_fields(modes, best.labels, np.where(D < share_z, 0.0, 1.0), len(facs), t, x, share_tol=0.5)
    wts = C.weights(fields)
    g, cF, n0 = C.gamma_N(facs, np.unique(modes.kappa), t, x) if len(facs) > 1 else (1.0, 0.0, 0)
    tol = 1e-8 if noise == 0 and noise_draws is None else 1e-3
    out, all_ok, unsupported = [], True, []
    for j, Q in enumerate(facs):
        sel = best.labels == j
        nk = len(np.unique(modes.kappa[sel]))
        dx = max(len(c) - 1 for c in Q.coeffs)
        # II-C1 (T23): tau-degree m needs m independent exponentials at one kappa; a factor whose
        # modes never show m of them at the same kappa fits one branch and invents the others
        _, per_k = np.unique(modes.kidx[sel], return_counts=True)
        support = int(per_k.max()) if len(per_k) else 0
        ok = sel.sum() >= Q.m * (dx + 1) + 1 and nk >= dx + 1 and support >= Q.m
        all_ok &= ok
        out.append(FactorResult(Q, Q.to_sympy(tol=tol), float(wts[j]), Q.evolution_terms(tol=tol), nk, ok))
        if support < Q.m:
            unsupported.append((j, Q.m, support))
    conf = confluent_test(modes, t, U, bin_noise)
    conf_all = conf
    conf = [c for c in conf if not _branch_point(c, [f.symbol for f in out], modes, t[-1] - t[0])]
    z2 = D.min(1) ** 2
    frac_out = float((z2 >= 9.0 * best.scale2).mean())
    info = {"outlier_fraction": frac_out, "bin_noise": bin_noise.scalar()}
    if len(conf_all) > len(conf):
        info["branch_points"] = [c for c in conf_all if c not in conf]  # confluent bins a factor explains
    if unsupported:
        info["unsupported_degree"] = unsupported  # (factor, m, max modes at one kappa)
    if conf:
        label = "UNDECIDED"
        info["reason"] = (f"confluent (A + B t) e^(lam t) modes in {len(conf)} bins: a repeated factor is "
                          "possible and has no finite test (OPF5B-T6)")
    elif frac_out > outlier_frac_misfit:
        label = "MISFIT"
        info["reason"] = f"{frac_out:.0%} of the modes are outliers for every structure"
    else:
        label = "FIT-COMPATIBLE" if all_ok else "ID-KER"
        if unsupported:
            info["reason"] = ("tau-degree not supported by the data (II-C1): factor(s) "
                              + ", ".join(f"{j} has m={m} but at most {s} mode(s) at one kappa" for j, m, s in unsupported))
    res = StructResult(label, out, ranked, g, cF, int(shared.sum()), len(modes), best.scale2, conf, info)
    if want_components:
        res.components = fields
    return res
