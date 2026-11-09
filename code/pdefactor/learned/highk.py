"""H0: high-kappa candidate modes from a raw-residual scan (S-LEARNED PLAN.md section 3.2).

Deterministic. The refinement pass scores the factors on the raw observations inside a band
|kappa| <= kmax read off the modes of the GP posterior mean (loop._raw_kmax). Where the GP loses the
high-kappa modes that the raw data still carry (E16: heat, 400 points at 5 %), the band is too narrow
and each factor is fitted with fewer equations than the data hold (T13/T40).

H0 only proposes a wider band; the refined raw evidence decides (refine_factors, evidence - Occam):
  1. residual r = y - P_B y of the observations off the span B of the current factors' kernels in
     the current band (least squares, the EPGP posterior mean at large tau^2);
  2. a damped matched-filter scan of r per wavenumber n in (kmax, n_max]: S_n = max over a grid of
     rates lambda of |<r, e^{lambda t + i kappa_n x}>|^2 / (sigma^2 ||e||^2), the generalised
     Lomb-Scargle statistic of one damped mode; on scattered points greedily (OMP, at most
     MAX_MODES), since a mode leaks into every wavenumber there;
  3. look-elsewhere threshold (Davies problem, CONV-T5): the 0.99 quantile of max_n S_n over
     B = 50 parametric re-simulations of the residual under the current fit, (I - P_B) sigma eps;
  4. proposal: kmax' = the largest n above the threshold. The caller refines at kmax' and keeps it
     only if the refined evidence - Occam term is not lower than at kmax.
Proposals (b) a new factor and (c) a degree-up factor of PLAN 3.2 are not built: see REPORT.md.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

B_NULL = 50
P_LEVEL = 0.01
# The scan grid is scale-free (CLAUDE.md rule 8: no constant tuned to a case), in units of the
# observation window T and the sampling: Re lambda T in [RE_LO, RE_HI] at spacing 1 / T (a mode decaying
# faster than e^-8 over the window carries no recoverable signal); Im lambda up to the time Nyquist
# pi / dt at half the Rayleigh spacing pi / (2 T). Scattered data: dt = T / sqrt(n) and the wavenumber
# band n <= sqrt(n_obs) / 2 (sqrt(n) points per axis, half of them per Nyquist).
RE_LO, RE_HI = -8.0, 1.0
MAX_MODES = 6  # greedy steps of the scattered scan


@dataclass
class Scan:
    kmax: int  # current band
    stat: dict  # n -> S_n
    threshold: float  # 0.99 null quantile of max_n S_n
    found: list  # wavenumbers above the threshold
    proposal: int | None  # the wider band, or None


def _syms(factors):
    from ..loop import _poly_symbol, _sympy_of

    return [_poly_symbol(_sympy_of(f)) for f in factors]


def _lam_grid(T, dt):
    re = np.arange(RE_LO, RE_HI + 0.5, 1.0) / T
    im_max = np.pi / dt
    im = np.arange(-im_max, im_max + 1e-9, np.pi / (2 * T))
    re, im = np.meshgrid(re, im, indexing="ij")
    return (re + 1j * im).ravel()


# ------------------------------------------------------------------ scattered observations
def _orth(B):
    if B.shape[1] == 0 or not np.all(np.isfinite(B)):
        return np.zeros((B.shape[0], 0), B.dtype)
    U, s, _ = np.linalg.svd(B, full_matrices=False)
    return U[:, s > 1e-10 * s.max()]


def _best(r, xs, period, ns, E, norm2):
    """(S, n, sign, lambda index) of the largest one-mode statistic of r over ns x {+-} x lambda."""
    best = (-1.0, None, 1, 0)
    for n in ns:
        for sgn in (1, -1):
            v = np.abs((r * np.exp(-1j * sgn * 2 * np.pi * n * xs / period)) @ E) ** 2 / norm2
            i = int(np.argmax(v))
            if v[i] > best[0]:
                best = (float(v[i]), n, sgn, i)
    return best


def _scan_obs(obs, factors, kmax, rng):
    """Greedy (OMP) scan: on irregular points the modes leak into every wavenumber, so the strongest
    one-mode peak is taken, its column joins the projection and the residual is rescanned, at most
    MAX_MODES times, while the peak exceeds the look-elsewhere threshold of the first step."""
    from ..refine_raw import _basis

    ts, xs, ys, period, sig = obs["ts"], obs["xs"], np.asarray(obs["ys"]), obs["period"], obs["sigma"]
    real = bool(np.isrealobj(ys))
    B = _basis(_syms(factors), ts, xs, period, kmax, real)
    T = float(np.ptp(ts)) or 1.0
    lam = _lam_grid(T, T / np.sqrt(len(ts)))
    arg = np.outer(ts, np.conj(lam))
    E = np.exp(np.clip(arg.real, -700, 50) + 1j * arg.imag)
    norm2 = np.sum(np.abs(E) ** 2, axis=0)
    ns = list(range(kmax + 1, int(np.sqrt(len(ts)) / 2) + 1))
    if not ns:
        return {}, np.inf
    U = _orth(B)
    proj = lambda v, U=U: v - U @ (U.conj().T @ v)  # noqa: E731
    null = []
    for _ in range(B_NULL):
        e = rng.standard_normal(len(ys)) if real else (rng.standard_normal(len(ys)) + 1j * rng.standard_normal(len(ys))) / np.sqrt(2)
        null.append(_best(proj(sig * e), xs, period, ns, E, norm2)[0] / sig**2)
    thr = float(np.quantile(null, 1 - P_LEVEL))
    stat, cols = {}, [B]
    for _ in range(MAX_MODES):
        r = proj(ys)
        S, n, sgn, i = _best(r, xs, period, ns, E, norm2)
        S /= sig**2
        stat[n] = max(stat.get(n, 0.0), S)
        if S <= thr:
            break
        c = np.exp(np.clip(lam[i].real * ts, -700, 50) + 1j * (lam[i].imag * ts + sgn * 2 * np.pi * n * xs / period))
        cols.append(np.stack([c.real, c.imag], 1) if real else c[:, None])
        U = _orth(np.concatenate(cols, axis=1))
        proj = lambda v, U=U: v - U @ (U.conj().T @ v)  # noqa: E731
    return stat, thr


# ------------------------------------------------------------------ full periodic grid
def _scan_grid(obs, factors, kmax, rng):
    """Same scan on a grid, per DFT bin. The current factors' columns live in bins |n| <= kmax only
    (refine_raw._grid_spectrum: block-diagonal over bins), so beyond the band the residual of bin n
    is the bin's own time series; its null is white noise of variance sigma^2 (unitary DFT)."""
    g, sig = obs["grid"], obs["sigma"]
    t, nx, Y = g["t"], g["nx"], g["Y"]
    lam = _lam_grid(float(t[-1] - t[0]), float(t[1] - t[0]))
    E = np.exp(np.clip(np.outer(t, np.conj(lam)).real, -700, 50) + 1j * np.outer(t, np.conj(lam)).imag)
    norm2 = np.sum(np.abs(E) ** 2, axis=0)
    ns = list(range(kmax + 1, nx // 2))
    if not ns:
        return {}, np.inf

    def stat_of(Yb):
        A = np.abs(Yb.T @ E) ** 2 / norm2  # (nx, n_lambda)
        best = A.max(1)
        return {n: max(best[n % nx], best[(-n) % nx]) / sig**2 for n in ns}

    stat = stat_of(Y)
    null = []
    for _ in range(B_NULL):
        e = (rng.standard_normal(Y.shape) + 1j * rng.standard_normal(Y.shape)) / np.sqrt(2)
        null.append(max(stat_of(sig * e).values()))
    return stat, float(np.quantile(null, 1 - P_LEVEL))


def scan(obs, factors, kmax, seed=0):
    """Scan of the observations beyond the current band. Returns a Scan; proposal is the widest
    band holding every wavenumber above the look-elsewhere threshold (None when there is none)."""
    rng = np.random.default_rng(seed)
    g = obs.get("grid")
    stat, thr = _scan_grid(obs, factors, kmax, rng) if g is not None else _scan_obs(obs, factors, kmax, rng)
    found = sorted(n for n, s in stat.items() if s > thr)
    return Scan(kmax, stat, thr, found, max(found) if found else None)
