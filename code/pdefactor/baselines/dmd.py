"""BOP-DMD baseline (PyDMD BOPDMD, Sashidhar & Kutz 2022).

BOP-DMD returns eigenvalues lam_j and spatial modes. For a constant-coefficient PDE on a periodic
grid each mode is (close to) a Fourier mode, so kappa_j = signed FFT peak of the mode, and
(lam_j, i kappa_j) are points of the dispersion variety. Our adapter fits a monic symbol on these
points (least squares, (m, dx) by BIC) and factors it with sympy. The adapter is not part of
BOP-DMD: the eigenvalues are.
"""
from __future__ import annotations

import time
import warnings

import numpy as np

from .common import BaselineResult, factor_symbol, lib_index, to_sympy


RHO0 = 1e-3  # relative residual floor, as in the SINDy baselines


def variety_fit(lam, kappa, real, sig=None, m_set=(1, 2, 3), dx_max=4):
    """Monic P(tau, xi) = tau^m + sum c_ab tau^a xi^b with P(lam, i kappa) ~ 0, BIC over (m, dx).
    Residuals are in lam units (rows reweighted once by 1/|d_tau P|) and, when given, divided by
    the BOP-DMD bagging std relative to its median (sig only ranks the points: its absolute size
    underestimates the error on exact data). BIC = n log(RSS/n + rho0^2 mean|lam|^2) + k log n,
    n = number of distinct points (a real field's conjugate points carry no extra information)."""
    z = 1j * kappa
    if sig is None:
        rel = np.ones(len(lam))
    else:
        sig = np.asarray(sig, float)
        rel = np.clip(sig / max(np.median(sig), 1e-12), 0.1, 10.0)
    n_eff = len(lam) // 2 if real else len(lam)
    scale = RHO0**2 * float(np.mean(np.abs(lam) ** 2))
    best = None
    for m in m_set:
        for dx in range(dx_max + 1):
            idx = lib_index(m, dx)
            k = len(idx) * (1 if real else 2)
            if n_eff <= k + 1:
                continue
            A0 = np.stack([lam**a * z**b for a, b in idx], 1)
            y0 = -lam**m
            w = 1 / (rel * np.maximum(np.abs(m * lam ** (m - 1)), 1e-3))
            for _ in range(2):
                A, y = A0 * w[:, None], y0 * w
                if real:
                    Ar, yr = np.r_[A.real, A.imag], np.r_[y.real, y.imag]
                    c, *_ = np.linalg.lstsq(Ar, yr, rcond=None)
                    r = yr - Ar @ c
                else:
                    c, *_ = np.linalg.lstsq(A, y, rcond=None)
                    rc = y - A @ c
                    r = np.r_[rc.real, rc.imag]
                dP = m * lam ** (m - 1) + sum(a * cc * lam ** (a - 1) * z**b for (a, b), cc in zip(idx, c) if a > 0)
                w = 1 / (rel * np.maximum(np.abs(dP), 1e-3))
            rss = float(r @ r) / (2 if real else 1)
            b = n_eff * np.log(rss / n_eff + scale) + (k + m) * np.log(n_eff)
            if best is None or b < best[0]:
                best = (b, m, dx, c, idx)
    return best


def noise_rank(X, noise, rel=1e-10, cap=None):
    """Number of singular values above the noise edge 1.1 sigma (sqrt(n) + sqrt(m)) (Marchenko-Pastur,
    sigma known) or rel * s_0 on exact data. Gavish-Donoho (svd_rank=0) keeps too few modes when
    the amplitudes decay fast in kappa (KG: 6 of 24)."""
    s = np.linalg.svd(X, compute_uv=False)
    edge = max(rel * s[0], 1.1 * noise * (np.sqrt(X.shape[0]) + np.sqrt(X.shape[1])))
    r = int((s > edge).sum())
    return max(1, min(r, cap or X.shape[1] // 2))


def bopdmd(u, t, x, noise=0.0, svd_rank=None, num_trials=20, dx_max=4, decimals=2, peak_frac=0.3, delays=8, max_rel_std=0.05):
    from pydmd import BOPDMD

    t0 = time.perf_counter()
    real = not np.iscomplexobj(u)
    # time-delay (Hankel) embedding: plain DMD sees at most rank(u) eigenvalues, too few for standing
    # waves (KG, telegraph: 6 of 24); the modes' first block is the spatial mode at time t
    nt = len(t) - delays + 1
    X = np.concatenate([np.asarray(u)[d:d + nt].T for d in range(delays)], 0)  # (space * delays, time)
    t = t[:nt]
    svd_rank = noise_rank(X, noise) if svd_rank is None else svd_rank
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        try:
            dmd = BOPDMD(svd_rank=svd_rank, num_trials=num_trials, trial_size=0.6, use_proj=True)
            dmd.fit(X, t)
        except Exception as e:  # noqa: BLE001
            return BaselineResult("bopdmd", False, f"BOPDMD failed: {e}", runtime=time.perf_counter() - t0)
    lam = np.asarray(dmd.eigs)
    modes = np.asarray(dmd.modes)[: len(x)]
    k = 2 * np.pi * np.fft.fftfreq(len(x), d=x[1] - x[0])
    F = np.abs(np.fft.fft(modes, axis=0))
    sig0 = np.asarray(dmd.eigenvalues_std) if num_trials else np.ones(len(lam))
    # BOP-DMD's own UQ: drop eigenvalues whose bagging std exceeds max_rel_std (1 + |lam|)
    keep = (sig0 <= max_rel_std * (1 + np.abs(lam))) if num_trials else np.ones(len(lam), bool)
    lam, F, sig0 = lam[keep], F[:, keep], sig0[keep]
    # one (lam, kappa) point per significant FFT peak of the mode: on real data an eigenvalue is shared
    # by two Fourier modes (e.g. wave: lam = i kappa for e^{-i kappa x} (right, conj) and e^{i kappa x} (left))
    L, K, S = [], [], []
    for j in range(len(lam)):
        for i in np.flatnonzero(F[:, j] >= peak_frac * F[:, j].max()):
            L.append(lam[j]); K.append(k[i]); S.append(sig0[j])
    lam, kappa, sig = np.array(L), np.array(K), (np.array(S) if num_trials else None)
    best = variety_fit(lam, kappa, real, sig, dx_max=dx_max)
    if best is None:
        return BaselineResult("bopdmd", False, "too few DMD eigenvalues for any symbol",
                              runtime=time.perf_counter() - t0, info={"eigs": lam.tolist()})
    _, m, dx, c, idx = best
    coeffs = {(m, 0): 1.0}
    for (a, b), v in zip(idx, c):
        coeffs[(a, b)] = v
    facs, st = factor_symbol(coeffs, decimals)
    return BaselineResult("bopdmd", True, "", to_sympy(coeffs), coeffs, m, facs, st, None,
                          time.perf_counter() - t0, {"rank": len(lam)})
