"""Spectral primitives: FFT in x and exponential fitting in t (matrix pencil).

On a grid u[t_k, x_l], for each wavenumber kappa:  u_hat(t, kappa) ~ sum_m A_m e^{lam_m t}.
The pairs (lam_m, i kappa) are points of the dispersion variety {P(tau, xi) = 0}.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class Modes:
    """Point cloud of the dispersion variety, one row per extracted mode."""
    kappa: np.ndarray  # real wavenumber
    lam: np.ndarray  # complex rate in t
    amp: np.ndarray  # complex amplitude at t = t0 (Fourier normalised)
    kidx: np.ndarray  # index of the FFT bin
    snr: np.ndarray  # |amp| / noise level of that bin

    def __len__(self):
        return len(self.lam)

    def subset(self, mask):
        return Modes(self.kappa[mask], self.lam[mask], self.amp[mask], self.kidx[mask], self.snr[mask])


def fft_x(u, x, window=None, pad=1):
    """FFT along x (axis 1). Returns (kappa, U) with U[t, k] normalised so that a mode
    A e^{i kappa x} gives U = A at its bin. `window`: None or 'tukey'; pad: zero-padding factor."""
    nx = u.shape[1]
    dx = x[1] - x[0]
    w = np.ones(nx)
    if window == "tukey":
        from scipy.signal.windows import tukey
        w = tukey(nx, 0.25)
    n = int(pad * nx)
    U = np.fft.fft(u * w, n=n, axis=1) / w.sum()
    kappa = 2 * np.pi * np.fft.fftfreq(n, d=dx)
    return kappa, U


def matrix_pencil(y, dt, order=None, pencil=None, rel_tol=1e-6, max_order=8):
    """Fit y_k = sum_m A_m exp(lam_m * k dt), k = 0..N-1 (Hua-Sarkar matrix pencil).

    order: number of exponentials; if None it is the numerical rank of the Hankel matrix
    (singular values above rel_tol * s_max), capped by max_order.
    Returns lam (complex), amp (complex), singular values.
    """
    y = np.asarray(y, complex)
    N = len(y)
    Lp = pencil or N // 2
    Y = np.array([y[i : i + Lp + 1] for i in range(N - Lp)])
    U, s, Vh = np.linalg.svd(Y, full_matrices=False)
    if order is None:
        order = int(np.sum(s > rel_tol * s[0])) if s[0] > 0 else 0
        order = min(order, max_order)
    if order == 0:
        return np.zeros(0, complex), np.zeros(0, complex), s
    V = Vh[:order].T  # rows of Y lie in the row space of Vh (no conjugation)
    V1, V2 = V[:-1], V[1:]
    z = np.linalg.eigvals(np.linalg.pinv(V1) @ V2)
    lam = np.log(z) / dt
    Z = np.exp(np.outer(np.arange(N) * dt, lam))
    amp, *_ = np.linalg.lstsq(Z, y, rcond=None)
    return lam, amp, s


def extract_modes(u, t, x, noise=0.0, kmax=None, snr_min=3.0, window=None, pad=1,
                  order=None, rel_tol=1e-6, max_order=8):
    """Dispersion point cloud from gridded data u[t, x] (uniform grids).

    noise: std of additive noise on u (0 for exact data). A bin is used only if its
    amplitude exceeds snr_min times the noise level of the bin.
    """
    dt = t[1] - t[0]
    kappa, U = fft_x(u, x, window=window, pad=pad)
    nx = u.shape[1]
    bin_noise = noise / np.sqrt(nx) if noise > 0 else 0.0
    floor = 1e-9 * np.abs(U).max()  # round-off floor for exact data
    bin_noise = max(bin_noise, floor / snr_min)
    rows = []
    for k in range(len(kappa)):
        if kmax is not None and abs(kappa[k]) > kmax:
            continue
        y = U[:, k]
        level = np.abs(y).max()
        if level == 0 or (bin_noise > 0 and level < snr_min * bin_noise):
            continue
        tol = max(rel_tol, (snr_min * bin_noise / level) if bin_noise > 0 else 0)
        lam, amp, _ = matrix_pencil(y, dt, order=order, rel_tol=tol, max_order=max_order)
        amp0 = amp * np.exp(-lam * t[0]) if t[0] != 0 else amp
        for lm, a in zip(lam, amp0):
            snr = abs(a) / bin_noise if bin_noise > 0 else np.inf
            if abs(a) > 0 and (bin_noise == 0 or abs(a) * np.exp(np.real(lm) * (t[-1] - t[0]) / 2) > snr_min * bin_noise / 3):
                rows.append((kappa[k], lm, a, k, snr))
    if not rows:
        e = np.zeros(0)
        return Modes(e, e.astype(complex), e.astype(complex), e.astype(int), e)
    k_, l_, a_, i_, s_ = map(np.array, zip(*rows))
    return Modes(k_.astype(float), l_.astype(complex), a_.astype(complex), i_.astype(int), s_.astype(float))
