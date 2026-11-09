"""Generic damped complex exponential sums: the training distribution of L0.

Every FFT bin of an in-scope field is y(t) = sum_j a_j exp(lam_j t) + noise (Ehrenpreis-Palamodov,
R2-T6 / T34), whatever the PDE. So L0 is trained on these sums, never on PDE solutions, and has no
PDE family to overfit. Poles are drawn in the dimensionless plane s = lam * T (T = time span), the
same plane the network outputs on, so one model serves every dt and T.

The draw covers what the pencil finds hard (THEORY_TO_ALGO T10, P2-Q3 open): near-merged pairs
(|ds| down to 0.3), amplitude ratios down to 1e-3, low SNR, and noise correlated in t (the GP
posterior-sample error is smooth in t: T36, T37).
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

# dimensionless pole box s = lam * T; Re s from fast decay to slight growth, |Im s| below Nyquist
RE_S = (-30.0, 3.0)
IM_S = (-40.0, 40.0)
MAX_ORDER = 8
NT = 64  # network input length; shorter series are zero-padded with a mask


@dataclass
class Draw:
    y: np.ndarray       # (nt,) complex, noisy
    s: np.ndarray       # (r,) complex poles in the s = lam T plane
    amp: np.ndarray     # (r,) complex amplitudes
    sigma: float        # white-equivalent noise std per sample
    nt: int
    colored: bool = False  # AR(1) noise in t


def _poles(rng, r):
    s = np.empty(r, complex)
    for j in range(r):
        if j > 0 and rng.random() < 0.35:  # near-merged with an earlier pole
            base = s[rng.integers(j)]
            d = rng.uniform(0.3, 3.0) * np.exp(2j * np.pi * rng.random())
            s[j] = base + d
        elif rng.random() < 0.3:  # real pole (diffusive bins)
            s[j] = rng.uniform(*RE_S)
        else:
            s[j] = rng.uniform(*RE_S) + 1j * rng.uniform(*IM_S)
    s.real = np.clip(s.real, *RE_S)
    s.imag = np.clip(s.imag, *IM_S)
    return s


def _noise(rng, nt, sigma):
    """Circular complex noise, E|e|^2 = sigma^2; with probability 0.4 AR(1)-correlated in t (same
    marginal std). Returns (noise, colored)."""
    e = (rng.standard_normal(nt) + 1j * rng.standard_normal(nt)) * sigma / np.sqrt(2)
    colored = rng.random() < 0.4
    if colored:
        phi = rng.uniform(0.3, 0.95)
        out = np.empty(nt, complex)
        out[0] = e[0]
        for i in range(1, nt):
            out[i] = phi * out[i - 1] + np.sqrt(1 - phi**2) * e[i]
        e = out
    return e, colored


def draw(rng, nt=None, r=None, snr_db=None):
    """One random sum. r = 0 gives pure noise (the null class)."""
    nt = int(nt or rng.integers(32, NT + 1))
    r = int(rng.integers(0, MAX_ORDER + 1) if r is None else r)
    s = _poles(rng, r)
    # amplitudes: a dominant one and log-uniform ratios down to 1e-3
    mag = 10 ** rng.uniform(-3, 0, r)
    if r:
        mag[rng.integers(r)] = 1.0
    amp = mag * np.exp(2j * np.pi * rng.random(r))
    u = np.linspace(0, 1, nt)
    clean = np.exp(np.outer(u, s)) @ amp if r else np.zeros(nt, complex)
    snr_db = rng.uniform(0, 80) if snr_db is None else snr_db
    rms = np.sqrt(np.mean(np.abs(clean) ** 2)) if r else 1.0
    sigma = rms / 10 ** (snr_db / 20)
    e, colored = _noise(rng, nt, sigma)
    return Draw(clean + e, s, amp, float(sigma), nt, colored)


def detectable(d: Draw, snr_min=3.0, rule="pipeline"):
    """The poles a correct per-bin fit should return; targets are only these. A pole buried in
    the noise carries no information and must not be learned (PHASE4 P0: absent means abstain).
    rule="pipeline": the keep rule of extract_modes_ic, |a| exp(Re s / 2) > snr_min sigma / 3
                     (amplitude at mid-record above the per-sample noise), the operational target;
    rule="matched":  matched-filter SNR |a| sqrt(sum_i |exp(s u_i)|^2) / sigma > snr_min, the
                     information-theoretic one (looser: such a pole is present but below the
                     pipeline's keep rule)."""
    if len(d.s) == 0:
        return d.s, d.amp
    if rule == "pipeline":
        keep = np.abs(d.amp) * np.exp(d.s.real / 2) > snr_min * d.sigma / 3
    else:
        u = np.linspace(0, 1, d.nt)
        energy = np.sqrt(np.exp(2 * np.outer(u, d.s.real)).sum(0))
        keep = np.abs(d.amp) * energy > snr_min * d.sigma
    return d.s[keep], d.amp[keep]


def encode(y, sigma, nt_max=NT):
    """Network input (3, nt_max): Re, Im of y / max|y| and a mask, plus log10 SNR as a scalar."""
    y = np.asarray(y, complex)[:nt_max]
    nt = len(y)
    scale = max(np.abs(y).max(), 1e-300)
    x = np.zeros((3, nt_max), np.float32)
    x[0, :nt] = (y.real / scale)
    x[1, :nt] = (y.imag / scale)
    x[2, :nt] = 1.0
    snr = np.log10(max(scale / max(sigma, 1e-300), 1e-3))
    return x, np.float32(snr)
