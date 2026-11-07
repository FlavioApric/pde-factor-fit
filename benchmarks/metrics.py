"""Benchmark metrics (skill benchmark-protocol): factor-set recovery, coefficient error, weight
error, true-structure indicator, calibration (reliability diagram, ECE, Brier)."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "analysis" / "exp"))
from e1_noise import coef_vec, match_err, truth  # noqa: E402,F401  (ground truth of E1/E1c)

from pdefactor.baselines.common import structure_of  # noqa: E402
from pdefactor.symbols import tau, xi  # noqa: E402

TOL = 0.05  # factor matched if max coefficient distance < TOL (as in E1/E1c)
# beam: real components hold both conjugate branches, so Field.weights do not give per-factor weights
NO_WEIGHTS = {"beam"}


def coef_dist(q, g):
    cq, cg = coef_vec(q, 0, 0), coef_vec(g, 0, 0)
    return max(abs(cq.get(k, 0) - cg.get(k, 0)) for k in set(cq) | set(cg))


def true_weights(name, field_, t, x):
    """{index of true factor: weight} from Field.weights, or None where undefined."""
    if name in NO_WEIGHTS:
        return None
    TT, XX = np.meshgrid(t, x, indexing="ij")
    w = field_.weights(TT, XX)
    tr = truth(name, field_)
    out = {}
    for j, q in enumerate(tr):
        # the component whose Q is this factor
        for c, wc in zip(field_.components, w):
            if sp.expand(sp.N(c.Q) - sp.N(q)) == 0 or coef_dist(sp.N(c.Q), q) < 1e-9:
                out[j] = float(wc)
    return out if len(out) == len(tr) else None


def score(name, field_, t, x, factors, weights=None):
    """factor_set, coef_err, weight_err for a list of sympy factors (and core weights)."""
    tr = truth(name, field_)
    err = match_err(tr, factors) if factors else np.inf
    ok = bool(err < TOL)
    werr = None
    if weights is not None and ok:
        tw = true_weights(name, field_, t, x)
        if tw is not None:
            werr = 0.0
            for j, q in enumerate(tr):
                g = min(range(len(factors)), key=lambda i: coef_dist(q, factors[i]))
                werr = max(werr, abs(weights[g] - tw[j]))
    return {"factor_set": ok, "coef_err": float(err), "weight_err": werr}


def true_structure(name, field_):
    return structure_of(truth(name, field_))


# ------------------------------------------------------------------ calibration
def reliability(p, y, bins=10):
    """Reliability table: per bin [lo, hi): mean predicted p, observed frequency, count."""
    p, y = np.asarray(p, float), np.asarray(y, float)
    edges = np.linspace(0, 1, bins + 1)
    idx = np.clip(np.digitize(p, edges) - 1, 0, bins - 1)
    rows = []
    for b in range(bins):
        s = idx == b
        rows.append((edges[b], edges[b + 1], float(p[s].mean()) if s.any() else np.nan,
                     float(y[s].mean()) if s.any() else np.nan, int(s.sum())))
    return rows


def ece(p, y, bins=10):
    rows = reliability(p, y, bins)
    n = sum(r[4] for r in rows)
    return float(sum(r[4] * abs(r[2] - r[3]) for r in rows if r[4]) / max(n, 1))


def brier(p, y):
    p, y = np.asarray(p, float), np.asarray(y, float)
    return float(np.mean((p - y) ** 2))
