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
