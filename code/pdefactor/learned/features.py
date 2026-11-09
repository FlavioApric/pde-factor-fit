"""Read-only adapters: LoopResult -> feature rows for L2b, L2c and V1.

These only read fields the deterministic pipeline already reports (loop.LoopResult, FactorReport,
split dict), so the learned layers can be trained and evaluated without touching loop.py. When the
deterministic V0 battery (pdefactor.validate, other session) lands, its statistics are appended to
`run_features` by the caller; nothing here recomputes them.
"""
from __future__ import annotations

import numpy as np

from .validator import factor_aggregates

Z90 = 1.6448536269514722  # half width of a central 90 % Gaussian interval in sd units


def _sd90(lo, hi):
    """sd from a 90 % interval; complex coefficients have separate real and imaginary intervals,
    so the larger of the two widths is used (|hi - lo| would mix them)."""
    d = complex(hi) - complex(lo)
    return max(max(abs(d.real), abs(d.imag)) / (2 * Z90), 1e-300)


def factor_row(f):
    """Per-factor features of a FactorReport."""
    m = max(a for a, _ in f.coef)
    dx = max(b for _, b in f.coef)
    z = [abs(mean) / _sd90(lo, hi) for (a, b), (mean, lo, hi) in f.coef.items() if (a, b) != (m, 0)]
    support = len(set(np.round(np.abs(f.kappa_support), 9))) if f.kappa_support else 0
    return {"coef_z": np.asarray(z, float) if z else np.array([np.nan]),
            "support": float(support),
            "margin": float(support - (dx + 1)),     # T13, T40: >= 0 needed for identifiability
            "W": float(f.W)}


def run_features(res):
    """One row (dict of floats) per LoopResult: structure-posterior summaries, factor aggregates and
    split-layer quantities. Identifiers (case, seed) are never included."""
    st = np.array(list((res.structures or {}).values()), float)
    st = st / st.sum() if st.size and st.sum() > 0 else st
    row = {
        "p_top": float(st.max()) if st.size else np.nan,
        "structure_entropy": float(-(st[st > 0] * np.log(st[st > 0])).sum()) if st.size else np.nan,
        "regrouped": float(bool(res.regrouped)),
        "n_dropped": float(len(res.dropped or [])),
    }
    ev = res.evidence or {}
    if len(ev) >= 2:
        v = np.sort(np.array(list(ev.values()), float))[::-1]
        row["evidence_gap"] = float(v[0] - v[1])  # V0.3-type statistic, read off the decider
    fr = [factor_row(f) for f in res.factors]
    for k, v in factor_aggregates(fr).items():
        row[k] = v
    sp_ = res.split or {}
    if sp_:
        g = sp_.get("gamma", np.nan)
        row["gamma"] = float(g)
        row["cF"] = float(sp_.get("cF", np.nan))
        row["p_split"] = float(sp_.get("p_split", np.nan))
        wq = np.asarray(sp_.get("w_q", []), float)
        wm = np.abs(np.asarray(sp_.get("w_mean", []), float))
        if wq.size and wm.size:
            rel = (wq[:, 2] - wq[:, 0]) / np.maximum(wm, 1e-12)
            row["split_amp"] = float(np.max(rel) / np.sqrt(max(g, 1e-12)))  # T5/T6: gamma^-1/2 sigma/|w|
    return row


def interval_features(res, factor_index):
    """The L2c theory features (calibrate.THEORY_FEATURES) for one factor of a LoopResult. Those the
    current LoopResult does not report (kappa_vand, log_snr, disagreement) are NaN until the
    deterministic layer exports them; the monotone GBM treats NaN as its own branch."""
    f = factor_row(res.factors[factor_index])
    run = run_features(res)
    return {"split_amp": run.get("split_amp", np.nan),
            "mode_margin": f["margin"],
            "kappa_vand": np.nan,
            "log_snr": np.nan,
            "disagreement": np.nan}


def _vand(ks, dx):
    """log10 condition number of the factor's coefficient design in xi at its kappa support (T9):
    columns (i kappa)^b, b = 0..dx, each scaled to unit norm. Fewer distinct kappa than dx + 1
    leaves the design rank deficient; that is reported as 16 (double-precision limit)."""
    ks = np.unique(np.round(np.abs(np.asarray(ks, float)), 9))
    if dx == 0:
        return 0.0
    if len(ks) < dx + 1:
        return 16.0
    V = (1j * ks[:, None]) ** np.arange(dx + 1)[None, :]
    V = V / np.linalg.norm(V, axis=0, keepdims=True)
    return float(min(np.log10(np.linalg.cond(V)), 16.0))


def export_features(res, data):
    """export_factors on a finished LoopResult."""
    return export_factors(res.factors, res.agg, res.split, data)


def export_factors(factors, agg, split, data):
    """The S-LEARNED section 3.0 exports, one dict per reported factor, read-only from the LoopResult
    and the data it was fitted on. data: dict(grid_data, t, x, grid_sigma, noise_draws (or None),
    n_obs (scattered only)).
      kappa_vand   log10 condition of the per-factor Vandermonde in xi at its kappa support (T9)
      log_snr      log10 median matched-filter SNR of the observed modes on the factor's variety,
                   (|A| / bin noise) * sqrt(sum_t |exp(lam t)|^2), modes of the posterior mean
      disagreement spread of the factor's track over the posterior samples / reported half-width
                   (T48); 1 on a single grid sample, whose intervals are the bootstrap spread itself
      split_floor  gamma^-1/2 sigma_w / |w| of the split layer (T5/T6), NaN for one factor
      log_nobs     log10 of the observation count (grid: nt nx)"""
    from ..core.structfit import _dist, extract_modes_ic, sigma_lambda
    from ..loop import _poly_symbol

    if not factors:
        return []
    u, t, x, sig = data["grid_data"], data["t"], data["x"], float(data["grid_sigma"])
    nd = data.get("noise_draws")
    modes, bn, _, _ = extract_modes_ic(u, t, x, noise=sig, noise_draws=None if nd is None else nd / np.sqrt(2))
    from ..loop import LoopResult

    qs = LoopResult("", factors, {}, {}, [], False, (0, 0), {}).pruned()
    n_obs = data.get("n_obs") or u.size
    sp_ = split or {}
    g = float(sp_.get("gamma", np.nan)) if sp_ else np.nan
    wq = np.asarray(sp_.get("w_q", []), float)
    wm = np.abs(np.asarray(sp_.get("w_mean", []), float))
    snr = [np.nan] * len(qs)
    if len(modes):
        sl = sigma_lambda(modes, t, bn)
        D = np.stack([_dist(_poly_symbol(q), modes.lam, modes.kappa) for q in qs], axis=1) / sl[:, None]
        near, ok = D.argmin(1), D.min(1) < 3.0
        tt = t - t[0]
        mf = modes.snr * np.sqrt(np.sum(np.abs(np.exp(np.outer(modes.lam, tt))) ** 2, axis=1))
        for j in range(len(qs)):
            v = mf[(near == j) & ok]
            snr[j] = float(np.log10(max(np.median(v), 1e-12))) if len(v) else np.nan
    track = _track_spread(factors, agg)
    out = []
    for j, f in enumerate(factors):
        dx = max(b for _, b in f.coef)
        m = max(a for a, _ in f.coef)
        hw = [max(abs(complex(hi) - complex(lo)) / 2, 1e-300) / max(abs(complex(mean)), 1e-300)
              for (a, b), (mean, lo, hi) in f.coef.items() if (a, b) != (m, 0)] or [np.nan]
        dis = 1.0 if track is None else (track[j] / float(np.nanmedian(hw)) if j < len(track) else np.nan)
        floor = (float((wq[j, 2] - wq[j, 0]) / max(wm[j], 1e-12) / np.sqrt(max(g, 1e-12)))
                 if wq.ndim == 2 and j < len(wq) and j < len(wm) else np.nan)
        out.append({"kappa_vand": _vand(f.kappa_support, dx), "log_snr": snr[j], "disagreement": dis,
                    "split_floor": floor, "log_nobs": float(np.log10(n_obs)),
                    "mode_margin": factor_row(f)["margin"], "rel_width": float(np.nanmedian(hw))})
    return out


def _track_spread(factors, agg):
    """Median relative spread of each factor's track over the posterior samples (weighted sd of
    the cloud coordinates / |track mean|), tracks matched to factors by coefficient distance. None
    for a single sample (grid path)."""
    c = getattr(agg, "cloud", None)
    if c is None or c.track is None or len(np.unique(c.sample)) < 2:
        return None
    from ..loop import _coef_dict

    out = []
    tracks = [k for k in np.unique(c.track) if k >= 0]
    for f in factors:
        cq = _coef_dict(f.sympy)
        best, rel = np.inf, np.nan
        for k in tracks:
            sel = c.track == k
            if not sel.any():
                continue
            i0 = np.flatnonzero(sel)[0]
            ck = _coef_dict(c.sympy[i0])
            d = max(abs(complex(cq.get(m, 0)) - complex(ck.get(m, 0))) for m in set(cq) | set(ck))
            if d < best:
                th = c.theta[sel]
                w = np.nan_to_num(c.pi[sel], nan=0.0) + 1e-300
                mu = np.average(th, axis=0, weights=w)
                sd = np.sqrt(np.average(np.abs(th - mu) ** 2, axis=0, weights=w))
                best, rel = d, float(np.median(sd / np.maximum(np.abs(mu), 1e-12)))
        out.append(rel)
    return out
