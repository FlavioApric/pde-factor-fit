"""Scattered -> grid interpolators for the benchmark.

PLACEHOLDER: `griddata_placeholder` is a deterministic piecewise-linear interpolation (scipy
griddata) used only until S-INTERP's GP exists. It has no posterior, so the core sees one
interpolant. Any callable with the same signature can replace it:

    interpolator(ts, xs, ys, t, x, L) -> (U[t, x], sigma_eff)

where sigma_eff is the per-grid-point noise std the core should assume (for the GP: the
posterior std; here: nominal noise plus a hold-out estimate of the interpolation error).
"""
from __future__ import annotations

import numpy as np
from scipy.interpolate import griddata


def _grid_real(ts, xs, ys, t, x, L):
    # periodic padding in x so that the hull covers [0, L)
    tp = np.r_[ts, ts, ts]
    xp = np.r_[xs - L, xs, xs + L]
    yp = np.r_[ys, ys, ys]
    TT, XX = np.meshgrid(t, x, indexing="ij")
    U = griddata((tp, xp), yp, (TT, XX), method="linear")
    bad = ~np.isfinite(U)
    if bad.any():  # outside the hull in t: nearest
        U[bad] = griddata((tp, xp), yp, (TT[bad], XX[bad]), method="nearest")
    return U


def _grid(ts, xs, ys, t, x, L):
    if np.iscomplexobj(ys):
        return _grid_real(ts, xs, ys.real, t, x, L) + 1j * _grid_real(ts, xs, ys.imag, t, x, L)
    return _grid_real(ts, xs, ys, t, x, L)


def griddata_placeholder(ts, xs, ys, t, x, L, sigma=0.0, holdout=0.1, seed=0):
    """PLACEHOLDER interpolator (see module doc). sigma_eff = sqrt(sigma^2 + s_hold^2), where s_hold
    is the RMS error at a 10 % hold-out set when interpolating from the other 90 %."""
    rng = np.random.default_rng(seed)
    n = len(ys)
    mask = rng.random(n) < holdout
    pred = _grid_hold(ts[~mask], xs[~mask], ys[~mask], ts[mask], xs[mask], L)
    s_hold = float(np.sqrt(np.mean(np.abs(pred - ys[mask]) ** 2))) if mask.any() else 0.0
    U = _grid(ts, xs, ys, t, x, L)
    return U, float(np.sqrt(sigma**2 + s_hold**2))


def _grid_hold(ts, xs, ys, tq, xq, L):
    def one(y):
        tp, xp, yp = np.r_[ts, ts, ts], np.r_[xs - L, xs, xs + L], np.r_[y, y, y]
        v = griddata((tp, xp), yp, (tq, xq), method="linear")
        bad = ~np.isfinite(v)
        if bad.any():
            v[bad] = griddata((tp, xp), yp, (tq[bad], xq[bad]), method="nearest")
        return v

    return one(ys.real) + 1j * one(ys.imag) if np.iscomplexobj(ys) else one(ys)


INTERPOLATORS = {"griddata_placeholder": griddata_placeholder}
