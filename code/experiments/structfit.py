"""Prototype (Phase 0b): structured factor fit with model comparison (mode-space grouping A).

Instead of fitting one P and factoring it with a fixed tolerance, fit every candidate
factor structure directly on the dispersion points and compare structures by BIC
(Laplace approximation of the evidence), with residuals in units of the pencil's own
uncertainty sigma_lam (Cramer-Rao of a damped exponential).
- A factored structure does not need both branches at every kappa (diffusion modes lost
  under noise are no longer a problem).
- Irreducibility is decided statistically (CONV-T5: no data-free threshold), not by ftol.
Structures: k factors (k = 1..3), each monic in tau of degree m_j in {1, 2}, each with its
own xi-degree dx_j <= dx_max. Output: best structure + posterior weights over structures.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import product

import numpy as np

from pdefactor.core.variety import PolySymbol, fit_monic


def sigma_lambda(modes, t, bin_noise, floor=1e-9):
    """CRB std of lam for each mode: full Fisher of all (A_j, lam_j) sharing the same FFT bin,
    so that interference between exponentials in one bin is accounted for."""
    tt = t - t[0]
    out = np.full(len(modes), np.inf)
    for k in np.unique(modes.kidx):
        idx = np.where(modes.kidx == k)[0]
        cols = []
        for i in idx:
            g = np.exp(modes.lam[i] * tt)
            cols += [g, modes.amp[i] * tt * g]
        J = np.stack(cols, axis=1)
        try:
            C = np.linalg.inv(J.conj().T @ J)
        except np.linalg.LinAlgError:
            continue
        for r, i in enumerate(idx):
            out[i] = np.sqrt(max(np.real(C[2 * r + 1, 2 * r + 1]), 0)) * bin_noise
    scale = np.abs(modes.lam).max() if len(modes) else 1.0
    return np.maximum(out, floor * max(scale, 1.0))


def _dist(Q, lam, kappa):
    """First-order distance in lam from the point to the variety {Q = 0}: |Q| / |dQ/dtau|."""
    xi_ = 1j * kappa
    v = Q(lam, xi_)
    h = 1e-6 * (1 + np.abs(lam))
    d = (Q(lam + h, xi_) - Q(lam - h, xi_)) / (2 * h)
    return np.abs(v) / np.maximum(np.abs(d), 1e-12)


@dataclass
class Fit:
    structure: tuple  # ((m_1, dx_1), ..., (m_k, dx_k))
    factors: list
    labels: np.ndarray
    chi2: float
    nparam: int
    bic: float


def _fit_factor(lam, kappa, w, m, dx, real):
    if len(lam) < m * (dx + 1) + 1:
        return None
    P, _, _ = fit_monic(lam, kappa, m, dx, w, real)
    return P


def fit_structure(lam, kappa, sig, structure, real=False, inits=8, iters=30, seed=0):
    """Alternating k-varieties regression for a given structure; returns the best Fit over inits."""
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
        # robust: mixture with a uniform background class caps each point at z^2 = (3 s)^2, where
        # s >= 1 is a robust scale of the residuals (median of chi^2_1 is 0.455), so that an
        # underestimated sigma_lam does not turn every point into an outlier
        z2 = D.min(1) ** 2
        s2 = max(1.0, float(np.median(z2)) / 0.455)
        chi2 = float(np.minimum(z2, 9.0 * s2).sum())
        npar = sum(m * (dx + 1) for m, dx in structure) * (1 if real else 2)
        nn = 2 * n
        # noise scale s >= 1 (cannot beat the CRB), Jeffreys on s: n log(max(chi2/n, 1))
        bic = nn * np.log(max(chi2 / nn, 1.0)) + npar * np.log(nn)
        if best is None or bic < best.bic:
            best = Fit(tuple(structure), facs, D.argmin(1), chi2, npar, bic)
    return best


def candidate_structures(m_max=3, dx_max=4, deg_options=(1, 2)):
    out = []
    for k in range(1, m_max + 1):
        for degs in product(deg_options, repeat=k):
            if sum(degs) > m_max or list(degs) != sorted(degs):
                continue
            for dxs in product(range(dx_max + 1), repeat=k):
                st = tuple(zip(degs, dxs))
                # canonical order to avoid duplicates
                if list(st) != sorted(st):
                    continue
                out.append(st)
    return out


def select(modes, t, bin_noise, m_max=3, dx_max=4, real=False):
    """All structures, BIC-ranked; returns (best Fit, list of (structure, bic, posterior weight))."""
    sig = sigma_lambda(modes, t, bin_noise)
    fits = []
    for st in candidate_structures(m_max, dx_max):
        f = fit_structure(modes.lam, modes.kappa, sig, st, real=real)
        if f is not None:
            fits.append(f)
    fits.sort(key=lambda f: f.bic)
    b = np.array([f.bic for f in fits])
    p = np.exp(-(b - b.min()) / 2)
    p /= p.sum()
    return fits[0], [(f.structure, f.bic, pi) for f, pi in zip(fits, p)], sig
