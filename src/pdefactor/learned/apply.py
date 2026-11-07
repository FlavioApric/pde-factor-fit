"""Run-time application of fitted S-LEARNED layers (sessions/LEARNED/PLAN.md section 3).

L2c: scale_intervals widens (or narrows) each coefficient's 90 % interval about its posterior median
by a per-factor factor s from the fitted interval model (learned/models/l2c.pkl, made by
benchmarks/ml_layers/ll_l2c.py on the simulator prior "prior: sim-v2"). Only (lo, hi) change: the median,
the factor set and the label never do.
"""
from __future__ import annotations

import pickle
from pathlib import Path

import numpy as np

MODELS = Path(__file__).with_name("models")
_CACHE = {}


def load(name):
    """A fitted layer model by name (None when the file is absent: the layer then does nothing)."""
    if name not in _CACHE:
        p = MODELS / f"{name}.pkl"
        _CACHE[name] = pickle.loads(p.read_bytes()) if p.exists() else None
    return _CACHE[name]


def scale_intervals(factors, scales):
    """In place: every non-leading coefficient interval (lo, hi) -> median + s (lo - median, hi - median),
    real and imaginary parts alike, s the factor's scale."""
    for f, s in zip(factors, scales):
        if not np.isfinite(s) or s == 1.0:
            continue
        m = max(a for a, _ in f.coef)
        for k, (med, lo, hi) in list(f.coef.items()):
            if k == (m, 0):
                continue
            med, lo, hi = complex(med), complex(lo), complex(hi)
            f.coef[k] = (med, med + s * (lo - med), med + s * (hi - med))


class ScaleModel:
    """The L2c interval model as shipped: either the GBM inflator (calibrate.IntervalInflator) on the
    per-factor features, or the scalar competitor (one conformal factor for every coefficient).
    clip: the scale range (PLAN.md 3.1: [0.5, 5])."""

    def __init__(self, kind, q=1.0, inflator=None, names=(), clip=(0.5, 5.0), tag=""):
        self.kind, self.q, self.inflator, self.names, self.clip, self.tag = kind, q, inflator, tuple(names), clip, tag

    def scales(self, feats):
        """feats: list of per-factor dicts (features.export_factors). One scale per factor."""
        if self.kind == "scalar" or self.inflator is None:
            s = np.full(len(feats), self.q)
        else:
            X = {k: np.array([f.get(k, np.nan) for f in feats], float) for k in self.names}
            s = self.inflator.raw_scale(X)
        return np.clip(s, *self.clip)


def l2c_scales(factors, agg, data, model_name="l2c"):
    """Per-factor scales for the factors at the L2c hook, or None without a fitted model."""
    from .features import export_factors

    model = load(model_name)
    if model is None or not factors:
        return None
    return model.scales(export_factors(factors, agg, None, data))
