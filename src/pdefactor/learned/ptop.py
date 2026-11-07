"""L2b: calibrated P(top structure is right), report only (sessions/LEARNED/PLAN.md 3.6, V1/PLAN.md 4).

The raw P(top) is the pooled structure posterior's maximum. A calibrator maps it (optionally with a
few dimensionless run features) to the probability that the top structure is the right factor set,
fitted offline on the simulator prior and tagged with it. It never changes a label or a threshold.

Arms (fewest parameters first): raw (identity), temperature (1 parameter on logit p; Guo et al.
2017), Platt (2), isotonic, inductive Venn-Abers (calibrate.py, E14), logit-features (L2 logistic
on logit p and <= 4 exports). E14 found isotonic and Venn-Abers worse than raw out of family; the
low-variance arms are the new hypothesis.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

TAG = "prior: sim-v2"
EPS = 1e-6
METHODS = ("raw", "temperature", "platt", "isotonic", "venn-abers", "logit-features")
FEATURES = ("log_snr_min", "kappa_vand_max", "disagreement_max", "evidence_gap")


def logit(p):
    p = np.clip(np.asarray(p, float), EPS, 1 - EPS)
    return np.log(p) - np.log1p(-p)


def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-np.asarray(z, float)))


def brier(p, y):
    return float(np.mean((np.asarray(p, float) - np.asarray(y, float)) ** 2))


def ece_adaptive(p, y, bins=15):
    """Expected calibration error with equal-mass bins (less biased than equal width at small n)."""
    p, y = np.asarray(p, float), np.asarray(y, float)
    if len(p) == 0:
        return np.nan
    order = np.argsort(p, kind="stable")
    out = 0.0
    for idx in np.array_split(order, min(bins, len(p))):
        if len(idx):
            out += len(idx) / len(p) * abs(p[idx].mean() - y[idx].mean())
    return float(out)


def log_loss(p, y):
    p = np.clip(np.asarray(p, float), EPS, 1 - EPS)
    y = np.asarray(y, float)
    return float(-np.mean(y * np.log(p) + (1 - y) * np.log1p(-p)))


def feature_matrix(rows):
    """FEATURES from corpus rows (or report dicts with the same keys): NaN -> column median later."""
    X = np.full((len(rows), len(FEATURES)), np.nan)
    for i, r in enumerate(rows):
        ex = r.get("export") or []
        run = r.get("run") or {}

        def agg(key, fn):
            v = np.array([e.get(key, np.nan) for e in ex], float)
            v = v[np.isfinite(v)]
            return float(fn(v)) if v.size else np.nan

        X[i] = [agg("log_snr", np.min), agg("kappa_vand", np.max), agg("disagreement", np.max),
                np.log1p(max(run.get("evidence_gap", np.nan), 0.0)) if np.isfinite(run.get("evidence_gap", np.nan))
                else np.nan]
    return X


@dataclass
class PTopCalibrator:
    method: str = "temperature"
    tag: str = TAG
    params: dict = field(default_factory=dict)
    _model: object = None

    def fit(self, p, y, X=None):
        p, y = np.asarray(p, float), np.asarray(y, float)
        z = logit(p)
        m = self.method
        if m == "raw":
            pass
        elif m == "temperature":
            from scipy.optimize import minimize_scalar

            r = minimize_scalar(lambda lt: log_loss(sigmoid(z / np.exp(lt)), y), bounds=(-5, 5), method="bounded")
            self.params = {"T": float(np.exp(r.x))}
        elif m == "platt":
            from scipy.optimize import minimize

            r = minimize(lambda ab: log_loss(sigmoid(ab[0] * z + ab[1]), y), x0=[1.0, 0.0], method="Nelder-Mead")
            self.params = {"a": float(r.x[0]), "b": float(r.x[1])}
        elif m == "isotonic":
            from .calibrate import ProbabilityCalibrator

            self._model = ProbabilityCalibrator().fit(p, y)
        elif m == "venn-abers":
            from .calibrate import VennAbersCalibrator

            self._model = VennAbersCalibrator().fit(p, y)
        elif m == "logit-features":
            from sklearn.linear_model import LogisticRegressionCV

            F = self._design(z, X, fit=True)
            self._model = LogisticRegressionCV(Cs=10, cv=5, scoring="neg_log_loss", max_iter=2000).fit(F, y)
        else:
            raise KeyError(m)
        return self

    def _design(self, z, X, fit=False):
        X = np.asarray(X, float)
        if fit:
            self.params["fill"] = np.nanmedian(X, 0).tolist()
            Xf = np.where(np.isfinite(X), X, self.params["fill"])
            self.params["mu"] = Xf.mean(0).tolist()
            self.params["sd"] = np.where(Xf.std(0) > 0, Xf.std(0), 1.0).tolist()
        Xf = np.where(np.isfinite(X), X, self.params["fill"])
        return np.column_stack([z, (Xf - self.params["mu"]) / self.params["sd"]])

    def __call__(self, p, X=None):
        p = np.asarray(p, float)
        m = self.method
        if m == "raw":
            return p.copy()
        if m == "temperature":
            return sigmoid(logit(p) / self.params["T"])
        if m == "platt":
            return sigmoid(self.params["a"] * logit(p) + self.params["b"])
        if m in ("isotonic", "venn-abers"):
            return np.asarray(self._model(p), float)
        return self._model.predict_proba(self._design(logit(p), X))[:, 1]

    def interval(self, p):
        """Venn-Abers multiprobability (p0, p1); other methods return (p', p')."""
        if self.method == "venn-abers":
            return self._model.interval(p)
        q = self(p)
        return q, q
