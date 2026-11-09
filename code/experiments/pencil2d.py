"""Prototype (Phase 0b, E3): mode extraction on a non-periodic cell, without the FFT.

Step 1: multi-channel matrix pencil in t (all x columns share the poles z = e^{lam dt}).
Step 2: for each lam, amplitude profile A_lam(x) by least squares; matrix pencil in x on it
gives mu = i kappa (several kappa may share one lam, e.g. wave branches).
No periodicity is assumed, so a sub-window of the domain can be analysed (DOMAIN study).
"""
from __future__ import annotations

import numpy as np

from pdefactor.core.spectral import Modes, matrix_pencil


def _order(s, noise_level, rel_tol=1e-11, max_order=60):
    thr = max(rel_tol * s[0], noise_level)
    return int(min((s > thr).sum(), max_order))


def mc_pencil(U, dt, noise=0.0, max_order=60):
    """Poles shared by all columns of U[t, x]."""
    nt, nx = U.shape
    Lp = nt // 2
    Y = np.concatenate([np.array([U[i : i + Lp + 1, j] for i in range(nt - Lp)]) for j in range(nx)], axis=0)
    _, s, Vh = np.linalg.svd(Y, full_matrices=False)
    # noise singular values of the stacked Hankel ~ noise * sqrt(rows)
    order = _order(s, 3 * noise * np.sqrt(Y.shape[0]) if noise > 0 else 0, max_order=max_order)
    V = Vh[:order].T
    z = np.linalg.eigvals(np.linalg.pinv(V[:-1]) @ V[1:])
    return np.log(z) / dt


def extract_modes_2d(u, t, x, noise=0.0, max_order=60, snr_min=3.0):
    dt, dx = t[1] - t[0], x[1] - x[0]
    U = np.asarray(u, complex)
    lam = mc_pencil(U, dt, noise, max_order)
    tt = t - t[0]
    Z = np.exp(np.outer(tt, lam))
    A, *_ = np.linalg.lstsq(Z, U, rcond=None)  # (M, nx)
    rows = []
    for m, l in enumerate(lam):
        a = A[m]
        # noise on a: ~ noise * sqrt(diag (Z^H Z)^-1)
        nlev = noise * np.sqrt(np.real(np.linalg.pinv(Z.conj().T @ Z)[m, m])) if noise > 0 else 0
        if np.abs(a).max() < snr_min * max(nlev, 1e-12 * np.abs(A).max()):
            continue
        tol = max(1e-4, snr_min * nlev / np.abs(a).max()) if nlev > 0 else 1e-4
        mu, b, _ = matrix_pencil(a, dx, rel_tol=tol, max_order=8)
        for mu_, b_ in zip(mu, b):
            amp = b_ * np.exp(mu_ * x[0])
            # bounded oscillation in x (kappa real) and above noise / round-off
            if abs(mu_.real) > 0.05 + 0.05 * abs(mu_.imag):
                continue
            if abs(b_) < max(snr_min * nlev / np.sqrt(len(x)), 1e-7 * np.abs(A).max()):
                continue
            rows.append((np.imag(mu_), l, amp, abs(amp) / max(nlev, 1e-300)))
    if not rows:
        e = np.zeros(0)
        return Modes(e, e.astype(complex), e.astype(complex), e.astype(int), e)
    k_, l_, a_, s_ = map(np.array, zip(*rows))
    # bins: modes whose kappa round to the same value share a "bin" for the CRB in structfit
    kidx = np.round(k_.real * 1e3).astype(int)
    return Modes(k_.astype(float), l_.astype(complex), a_.astype(complex), kidx, s_.astype(float))
