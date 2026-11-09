"""Deterministic residual diagnostics for V1 (sessions/LEARNED/V1/PLAN.md sec. 3.1).

The residual is the V0.1 one (`validate.predictive_bins`): per kappa bin, the data's time series
minus its least-squares fit on the modes e^{lambda t} of the reported factors. No new fit is made.
Every statistic is dimensionless (a correlation, a ratio or a log p-value), so it does not change
when u is rescaled or when t, x are rescaled together with the law (rule 8).

What each statistic targets (T50: the bootstrap and the evidence assume white Gaussian noise at a
constant sigma):
- lb_t_logp, acf1_t: whiteness in time (Ljung-Box pooled over bins): coloured noise, two laws,
  nonlinearity;
- acf1_x, flat_x, kslope: whiteness across kappa: coloured noise in x, fractional symbols, lost
  high-kappa modes;
- bp_logp: Breusch-Pagan n R^2 of r^2 on (|u_fit|, t): heteroscedastic noise;
- half_ratio: residual energy after T/2 over before: a law that changes in time;
- nyq_ratio: residual energy in the top 1/8 of temporal frequencies over its white-noise share:
  modes beyond the time Nyquist (aliasing).
No statistic is a label or a threshold: they are features (report only).
"""
from __future__ import annotations

import numpy as np

KEYS = ("lb_t_logp", "acf1_t", "acf1_x", "flat_x", "kslope", "bp_logp", "half_ratio", "nyq_ratio")
NYQ_FRAC = 1 / 8


def _chi2_log10sf(stat, df):
    from ..validate import _log10sf  # the V0 helper (floored at -300)

    return _log10sf(stat, df)


def residual(factors, u, t, x):
    """(kappa, fitted spectrum, residual spectrum), each U[t, k] as `core.spectral.fft_x` (no
    window). factors: sympy, monic in tau. Same projection as validate.predictive_bins, which
    returns only the per-bin chi^2, not the residual series; the roots are computed from the
    tau-coefficients lambdified once (synthetic.branch_roots calls sympy per bin, ~4.7 s per run).
    tests/test_learned_resid.py checks the chi^2 per bin equals predictive_bins'."""
    import sympy as sp

    from ..core.spectral import fft_x
    from ..symbols import tau, xi

    kappa, U = fft_x(u, x)
    tt = np.asarray(t, float) - t[0]
    R = np.empty_like(U, dtype=complex)
    # tau-coefficients of each factor as numpy functions of xi (synthetic.branch_roots, lambdified once)
    polys = [[sp.lambdify(xi, c, "numpy") for c in sp.Poly(sp.expand(q), tau).all_coeffs()] for q in factors]

    def roots(k):
        z = 1j * k
        return [np.roots([complex(c(z)) for c in p]) for p in polys]

    for j, k in enumerate(kappa):
        lams = np.concatenate(roots(k)) if factors else np.zeros(0, complex)
        lams = lams[np.isfinite(lams)]
        y = U[:, j]
        if lams.size:
            Z = np.exp(np.outer(tt, lams))
            a, *_ = np.linalg.lstsq(Z, y, rcond=None)
            R[:, j] = y - Z @ a
        else:
            R[:, j] = y
    return kappa, U - R, R


def diagnostics(factors, u, t, x):
    """Dict of the KEYS statistics (NaN when undefined). factors: LoopResult factors (objects with
    .sympy) or sympy expressions."""
    facs = [getattr(f, "sympy", f) for f in factors]
    u = np.asarray(u)
    nt, nx = u.shape
    real = bool(np.isrealobj(u))
    kappa, F, R = residual(facs, u, t, x)
    out = dict.fromkeys(KEYS, np.nan)

    # bins used for the time statistics: kappa != 0 (and kappa > 0 below Nyquist for real data,
    # whose negative bins are conjugate mirrors); the kappa = 0 bin of real data is real.
    k_int = np.rint(kappa / (kappa[1] if nx > 1 else 1.0)).astype(int)
    use = (k_int > 0) & (k_int < nx / 2) if real else (k_int != 0)
    Rb = R[:, use]
    pw = (np.abs(Rb) ** 2).sum(0)
    ok = pw > 0
    if ok.sum() >= 1 and nt >= 8:
        Rb = Rb[:, ok]
        H = max(1, int(np.sqrt(nt)))
        Q, rho1 = 0.0, []
        den = (np.abs(Rb) ** 2).sum(0)
        for lag in range(1, H + 1):
            rho = (Rb[lag:] * np.conj(Rb[:-lag])).sum(0) / den  # complex ACF per bin
            Q += (nt * (nt + 2) / (nt - lag) * 2 * np.abs(rho) ** 2).sum()  # 2 n |rho|^2 ~ chi2_2
            if lag == 1:
                rho1 = rho.real
        out["lb_t_logp"] = _chi2_log10sf(Q, 2 * H * Rb.shape[1])
        out["acf1_t"] = float(np.mean(rho1))
        # temporal spectrum of each bin's residual: share of energy in the top NYQ_FRAC of |freq|
        S = np.abs(np.fft.fft(Rb, axis=0)) ** 2
        f = np.abs(np.fft.fftfreq(nt))
        top = f >= 0.5 * (1 - NYQ_FRAC)
        share = S[top].sum() / S.sum()
        out["nyq_ratio"] = float(np.log(share / top.mean()))

    # residual power per kappa bin (time-averaged): flatness and log-log slope
    if real:
        sel = (k_int > 0) & (k_int < nx / 2)
    else:
        sel = k_int != 0
    P = (np.abs(R[:, sel]) ** 2).mean(0)
    ks = np.abs(kappa[sel])
    if P.size >= 3 and np.all(P > 0):
        out["flat_x"] = float(np.exp(np.mean(np.log(P))) / np.mean(P))
        out["kslope"] = float(np.polyfit(np.log(ks), np.log(P), 1)[0])

    # physical-space residual and fit
    r = np.fft.ifft(R * nx, axis=1)
    fit = np.fft.ifft(F * nx, axis=1)
    if real:
        r, fit = r.real, fit.real
    e2 = np.abs(r) ** 2
    tot = e2.sum()
    if tot > 0:
        out["acf1_x"] = float((r * np.conj(np.roll(r, -1, axis=1))).real.sum() / tot)
        half = np.asarray(t) >= t[0] + 0.5 * (t[-1] - t[0])
        a, b = e2[half].sum(), e2[~half].sum()
        if a > 0 and b > 0:
            out["half_ratio"] = float(np.log((a / half.sum()) / (b / (~half).sum())))
        # Breusch-Pagan (Koenker form): n R^2 of e^2 on (1, |fit|, t), ~ chi2_2 under homoscedasticity
        y = (e2 / e2.mean()).ravel()
        TT = np.broadcast_to(np.asarray(t, float)[:, None], e2.shape).ravel()
        A = np.abs(fit).ravel()
        X = np.column_stack([np.ones_like(y), (A - A.mean()) / (A.std() or 1.0), (TT - TT.mean()) / (TT.std() or 1.0)])
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        res_ = y - X @ beta
        r2 = 1 - (res_ @ res_) / ((y - y.mean()) @ (y - y.mean()))
        out["bp_logp"] = _chi2_log10sf(len(y) * max(r2, 0.0), 2)
    return out
