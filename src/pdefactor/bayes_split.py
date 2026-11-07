"""Friedrichs-angle Bayesian split layer (plan 0b.10, with the v2.4 fixes). Outer layer: it uses only
the core's outputs (the factor symbols Q_j) and the data; the core is not touched.

Model, per FFT bin kappa (the FFT in x decouples the bins on a periodic grid):
    y_k(t) = sum_j B_jk(t) a_jk + e_k,   B_jk = [e^{lam t} for the roots lam of Q_j(., i kappa)],
    a_jk ~ N(0, tau_k^2 I) (one scale per bin, shared by the factors: an equal-variance prior, whose
    posterior mean splits the shared directions equally, i.e. the core's minimum-norm choice, 0b.10),
    e_k ~ N(0, C_k) with C_k white or the per-bin correlated covariance of the core's BinNoise (GLS;
    noise from the GP posterior, v2.4 fix 2).
Real fields (v2.4 fix 1, conjugate-pair parametrisation): the kappa = 0 bin is real, with the real
basis spanned by Re/Im of its exponentials and a real Gaussian likelihood; bins kappa > 0 carry the
mirrored bins -kappa (y_{-k} = conj y_k), have complex amplitudes and count twice in every norm.

Outputs:
- posterior of the weights w_j = ||u_j|| / sum_k ||u_k|| by Monte Carlo over the Gaussian posterior
  of the amplitudes (no linearisation, rule 4), with credible intervals;
- evidence of every non-empty subset of the factors (tau_k^2 by empirical Bayes per bin and model),
  hence P(split) = P(all factors needed) and per-factor inclusion probabilities. When theta_F -> 0
  the evidence ratio -> 1 and P(split) returns to its prior (the data cannot separate the factors);
- c_F and gamma_N of the sampled bases (whitened when the noise is correlated: generalised angle).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from itertools import combinations

import numpy as np

from .core.spectral import fft_x
from .core.structfit import BinNoise

TAU2_GRID = np.logspace(-8, 4, 49)  # relative to the bin's noise variance (empirical Bayes grid)


@dataclass
class SplitResult:
    weights_mean: np.ndarray
    weights_q: np.ndarray  # (k, 3): 5 %, 50 %, 95 %
    weight_draws: np.ndarray  # (ndraw, k)
    p_split: float
    p_include: np.ndarray  # (k,)
    log_evidence: dict  # subset (tuple of factor indices) -> log evidence
    cF: float
    gamma: float
    bins: list = field(default_factory=list)
    bin_logev: dict = field(default_factory=dict)  # subset -> per-bin log evidence (order of `bins_all`)
    free_logev: np.ndarray | None = None  # per bin: evidence of the bin's own exponentials (free model)
    bins_all: list = field(default_factory=list)  # kappa of every bin that entered the evidence
    free_order: list = field(default_factory=list)  # number of free exponentials per bin

    def summary(self):
        lines = [f"P(split)={self.p_split:.3f}  c_F={self.cF:.3g} gamma_N={self.gamma:.3g}"]
        for j, (m, q) in enumerate(zip(self.weights_mean, self.weights_q)):
            lines.append(f"  factor {j}: w={m:.4f} [{q[0]:.4f}, {q[2]:.4f}]  P(include)={self.p_include[j]:.3f}")
        return "\n".join(lines)


def _bin_basis(Q, kappa, tt):
    lam = np.atleast_1d(Q.roots(1j * kappa))
    return np.exp(np.outer(tt, lam)) if len(lam) else np.zeros((len(tt), 0), complex)


def _realify(B):
    """Real basis of {Re(B c)}: Re and Im parts of the columns, rank-reduced."""
    R = np.concatenate([B.real, B.imag], axis=1)
    if R.shape[1] == 0:
        return R
    U, s, _ = np.linalg.svd(R, full_matrices=False)
    keep = s > 1e-10 * s.max()
    return U[:, keep] * s[keep]


def _whiten(W, a):
    return W * a if np.isscalar(W) else W @ a


def _log_ev(Bw, yw, tau2, real):
    """log N(yw; 0, I + tau2 Bw Bw^H) (whitened data and basis), via the small Gram."""
    n, p = Bw.shape
    if p == 0:
        q, ld = np.vdot(yw, yw).real, 0.0
    else:
        M = Bw.conj().T @ Bw + np.eye(p) / tau2
        L = np.linalg.cholesky(M)
        b = np.linalg.solve(L, Bw.conj().T @ yw)
        q = np.vdot(yw, yw).real - np.vdot(b, b).real
        ld = 2 * np.log(np.abs(np.diag(L))).sum() + p * np.log(tau2)
    if real:
        return -0.5 * (q + ld + n * np.log(2 * np.pi))
    return -(q + ld + n * np.log(np.pi))


def bayes_split(u, t, x, factors, noise=0.0, noise_draws=None, snr_min=3.0, ndraw=400, seed=0,
                p_prior=None, free_modes=None):
    """u: field on the (t, x) grid (one posterior sample or the data). factors: the core's factor
    symbols (FactorResult.symbol). noise: white std; noise_draws: draws of a correlated noise field
    (as for the core). p_prior: prior over subsets (default uniform over non-empty subsets).
    free_modes: optional {bin index: lam array}, the bin's own exponentials (e.g. from the pencil); the
    per-bin evidence of that free model is returned (robust outlier-bin mixture in the decider).
    Returns SplitResult."""
    u = np.asarray(u)
    real = bool(np.isrealobj(u))
    tt = t - t[0]
    nt, nx = u.shape
    kappa, U = fft_x(u, x)
    floor = 1e-9 * np.abs(U).max()
    bn = (BinNoise(np.full(len(kappa), max(noise / np.sqrt(nx) if noise > 0 else 0.0, floor / snr_min)))
          if noise_draws is None else BinNoise.from_draws(noise_draws, x, noise=noise, floor=floor / snr_min))
    k = len(factors)
    subsets = [s for r in range(1, k + 1) for s in combinations(range(k), r)]
    logev = {s: 0.0 for s in subsets}
    bin_ev = {s: [] for s in subsets}
    free_ev, bins_all, free_order = [], [], []
    rng = np.random.default_rng(seed)
    norms2 = np.zeros((ndraw, k))
    G_all, bins = [], []
    for b in range(len(kappa)):
        if real and kappa[b] < 0:
            continue  # mirrored bin: carried by +kappa
        y = U[:, b]
        if np.abs(y).max() < snr_min * bn.sigma[b]:
            continue
        rbin = real and kappa[b] == 0
        mult = 1.0 if (not real or kappa[b] == 0) else 2.0
        W = bn.W(b, nt)
        Bs = []
        for Q in factors:
            B = _bin_basis(Q, kappa[b], tt)
            Bs.append(_realify(B) if rbin else B)
        yb = y.real if rbin else y
        yw = _whiten(W, yb)
        if rbin and not np.isscalar(W):
            yw = yw.real
        Bws = [_whiten(W, B) for B in Bs]
        if rbin:
            Bws = [B.real if np.iscomplexobj(B) else B for B in Bws]
        # evidence of every subset, tau^2 by empirical Bayes per bin
        best_full = None
        for s in subsets:
            Bw = np.concatenate([Bws[j] for j in s], axis=1)
            ev = [(_log_ev(Bw, yw, t2, rbin), t2) for t2 in TAU2_GRID]
            e, t2 = max(ev)
            logev[s] += e
            bin_ev[s].append(e)
            if len(s) == k:
                best_full = t2
        bins_all.append(float(kappa[b]))
        if free_modes is not None:
            lf = np.asarray(free_modes.get(b, []), complex)
            Bf = np.exp(np.outer(tt, lf)) if len(lf) else np.zeros((nt, 0), complex)
            Bf = _realify(Bf) if rbin else Bf
            Bfw = _whiten(W, Bf)
            if rbin:
                Bfw = Bfw.real if np.iscomplexobj(Bfw) else Bfw
            free_order.append(len(lf))
            free_ev.append(max(_log_ev(Bfw, yw, t2, rbin) for t2 in TAU2_GRID))
        # posterior on the amplitudes of the full model, MC over the weights
        Bw = np.concatenate(Bws, axis=1)
        p = Bw.shape[1]
        if p == 0:
            continue
        M = Bw.conj().T @ Bw + np.eye(p) / best_full
        Minv = np.linalg.inv(M)
        mu = Minv @ (Bw.conj().T @ yw)
        Cp = (Minv + Minv.conj().T) / 2
        L = np.linalg.cholesky(Cp + 1e-14 * np.trace(Cp).real / p * np.eye(p))
        if rbin:
            z = rng.standard_normal((p, ndraw))
        else:
            z = (rng.standard_normal((p, ndraw)) + 1j * rng.standard_normal((p, ndraw))) / np.sqrt(2)
        A = mu[:, None] + L @ z
        i0 = 0
        for j, B in enumerate(Bs):
            pj = B.shape[1]
            comp = B @ A[i0:i0 + pj]  # unwhitened component in this bin, (nt, ndraw)
            norms2[:, j] += mult * nx * (np.abs(comp) ** 2).sum(0)
            i0 += pj
        G_all.append((Bws, mult))
        bins.append(float(kappa[b]))
    nrm = np.sqrt(norms2)
    wd = nrm / np.maximum(nrm.sum(1, keepdims=True), 1e-300)
    # subset posterior
    keys = list(logev)
    lp = np.array([logev[s] for s in keys])
    if p_prior is not None:
        lp = lp + np.log(np.array([p_prior.get(s, 0.0) for s in keys]) + 1e-300)
    post = np.exp(lp - lp.max())
    post /= post.sum()
    p_split = float(sum(p for s, p in zip(keys, post) if len(s) == k)) if k > 1 else 0.0
    p_inc = np.array([sum(p for s, p in zip(keys, post) if j in s) for j in range(k)])
    gamma, cF = _angles(G_all, k)
    return SplitResult(wd.mean(0), np.quantile(wd, [0.05, 0.5, 0.95], axis=0).T, wd, p_split, p_inc,
                       {s: float(v) for s, v in logev.items()}, cF, gamma, bins,
                       {s: np.array(v) for s, v in bin_ev.items()},
                       np.array(free_ev) if free_modes is not None else None, bins_all, free_order)


def _angles(G_all, k):
    """gamma_N = smallest nonzero eigenvalue of S^H S with S the column-normalised union of the
    (whitened) kernel bases over the band; c_F = 1 - gamma for k = 2 (P2-T3)."""
    if k < 2 or not G_all:
        return 1.0, 0.0
    blocks = []
    for Bws, mult in G_all:
        Qs = []
        for B in Bws:
            if B.shape[1] == 0:
                continue
            q, r = np.linalg.qr(B)
            keep = np.abs(np.diag(r)) > 1e-9 * np.abs(np.diag(r)).max()
            Qs.append(q[:, keep])
        if len(Qs) >= 2:
            blocks.append(np.concatenate(Qs, axis=1))
    if not blocks:
        return 1.0, 0.0
    ev = np.concatenate([np.linalg.eigvalsh(S.conj().T @ S) for S in blocks])
    ev = ev[ev > 1e-9]
    g = float(ev.min()) if len(ev) else 1.0
    return g, max(0.0, 1.0 - g)


def raw_evidence(factors, ts, xs, ys, period, kmax, sigma=None, tau2_grid=TAU2_GRID, sig_grid=None):
    """Log evidence of raw scattered observations (t_i, x_i, y_i) in the span of the factors' kernels
    (v2.9 #2(c), EPGP in closed form): features e^{lam t + i kappa x} for every root lam of
    Q_j(., i kappa), kappa = 2 pi n / period, |n| <= kmax; amplitudes ~ N(0, tau^2 I), white noise.
    Unlike the evidence on the GP posterior mean, interpolation artifacts (the GP's own decay at high
    kappa) are not in these data. tau^2 (relative to sigma^2) and, when sigma is None, sigma (grid
    around the residual scale) by empirical Bayes. Real y: real basis (Re/Im of the columns)."""
    ys = np.asarray(ys)
    real = bool(np.isrealobj(ys))
    from . import refine_raw

    if (refine_raw.TAU2_PER_BIN or refine_raw.TAU2_POOL_EMPTY) and sigma is not None:  # per-bin scales (T76/T77), as in the refinement
        B = refine_raw._basis(factors, np.asarray(ts), np.asarray(xs), period, kmax, real)
        rank = int(np.linalg.matrix_rank(B)) if B.size else 0
        obs = dict(ts=np.asarray(ts), xs=np.asarray(xs), ys=ys, period=period, sigma=sigma)
        return float(refine_raw.log_evidence(factors, obs, kmax)), rank
    tt = np.asarray(ts) - 0.0
    cols = []
    for Q in factors:
        for n in range(-kmax, kmax + 1):
            kap = 2 * np.pi * n / period
            for lam in np.atleast_1d(Q.roots(1j * kap)):
                cols.append(np.exp(np.clip(lam.real * tt, -700, 50) + 1j * (lam.imag * tt + kap * np.asarray(xs))))
    B = np.stack(cols, axis=1) if cols else np.zeros((len(ys), 0), complex)
    if real:
        B = np.concatenate([B.real, B.imag], axis=1)
        if B.shape[1] > B.shape[0]:  # more columns than observations (T77): diag(r) has only n entries,
            # so the mask below would not index the columns; keep a basis of the span instead
            # (pivoted QR, the same 1e-10 relative rank rule), at most n columns
            from scipy.linalg import qr as _qr

            _, r, piv = _qr(B, mode="economic", pivoting=True)
            d = np.abs(np.diag(r))
            B = B[:, np.sort(piv[: int(np.sum(d > 1e-10 * max(d.max(initial=0.0), 1e-300)))])]
        elif B.shape[1]:
            q, r = np.linalg.qr(B)
            keep = np.abs(np.diag(r)) > 1e-10 * max(np.abs(np.diag(r)).max(), 1e-300)
            B = B[:, keep]
    sigs = [sigma] if sigma is not None else (sig_grid if sig_grid is not None else
                                              np.std(ys) * np.logspace(-4, 0, 25))
    best = -np.inf
    for s in sigs:
        for t2 in tau2_grid:
            best = max(best, _log_ev(B / s, ys / s, t2, real) - len(ys) * np.log(s) * (1 if real else 2))
    return float(best), B.shape[1]
