"""L2b / L2c: calibration of probabilities and intervals on a declared simulator prior.

What is learned here and why (analysis/PHASE4_ML_PLAN.md, L2):
- Decision thresholds are not tuned: once a probability is calibrated, the Bayes decision for a
  loss pair gives the threshold, p* = L_false / (L_false + L_miss) (`loss_threshold`). This
  replaces hand values such as P_CONCENTRATED (CONV-T5: no data-free threshold exists, so the
  threshold is prior- and loss-relative and must say so).
- The structure posterior P(top) is recalibrated by one isotonic map (`ProbabilityCalibrator`):
  monotone, so it never reorders runs, and with one degree of freedom per level it cannot learn
  the simulator's case identities. Reliability (T18, T29) is the acceptance test.
- Interval widths are inflated by one monotone map per quantity type (`IntervalInflator`) on a
  few dimensionless theory features whose sign the theory fixes:
    split amplification gamma_N^{-1/2} sigma / |w|  (T5, T6)          -> non-decreasing
    mode-count margin n_kappa - (dx + 1)          (T13, T40)          -> non-increasing
    Vandermonde condition kappa_Vand              (T9, P2-P6)         -> non-decreasing
    per-factor SNR                                 (empirical)         -> non-increasing
    posterior-sample disagreement                  (T48)               -> non-decreasing
  and a Mondrian split-conformal step on a separate calibrate split gives finite-sample coverage
  within the simulator prior (and only there: weighted conformal degrades by an unknowable TV
  term outside it). Coverage is conditional on correct structure selection, reported with it.

Everything carries PRIOR_TAG. Off means scale 1 and the raw probabilities: today's pipeline.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from . import PRIOR_TAG

# feature name -> monotone direction of the needed inflation (+1 non-decreasing, -1 non-increasing)
THEORY_FEATURES = {
    "split_amp": +1,       # gamma_N^{-1/2} sigma / |w|
    "mode_margin": -1,     # n_kappa - (dx + 1)
    "kappa_vand": +1,      # log10 Vandermonde condition
    "log_snr": -1,         # log10 per-factor SNR
    "disagreement": +1,    # posterior-sample spread / reported sd
}


def loss_threshold(loss_false, loss_miss):
    """Bayes threshold on a calibrated probability: accept when P > L_false / (L_false + L_miss)."""
    return float(loss_false) / (float(loss_false) + float(loss_miss))


def split_indices(n, fracs=(0.5, 0.25, 0.25), groups=None, rng=0):
    """Disjoint fit / calibrate / test indices. With `groups` (e.g. a family label per run) whole
    groups go to one split, so a held-out family is never seen by fit or calibrate (LOFO)."""
    rng = np.random.default_rng(rng)
    if groups is None:
        perm = rng.permutation(n)
        a, b = int(fracs[0] * n), int((fracs[0] + fracs[1]) * n)
        return perm[:a], perm[a:b], perm[b:]
    groups = np.asarray(groups)
    ug = rng.permutation(np.unique(groups))
    if len(ug) < 3:
        raise ValueError("grouped split needs >= 3 groups (fit, calibrate, test each get one)")
    a = min(max(int(fracs[0] * len(ug)), 1), len(ug) - 2)
    b = min(max(int((fracs[0] + fracs[1]) * len(ug)), a + 1), len(ug) - 1)
    pick = lambda gs: np.where(np.isin(groups, gs))[0]
    return pick(ug[:a]), pick(ug[a:b]), pick(ug[b:])


def reliability(p, y, bins=10):
    """Reliability table and expected calibration error of probabilities p for binary outcomes y."""
    p, y = np.asarray(p, float), np.asarray(y, float)
    edges = np.linspace(0, 1, bins + 1)
    idx = np.clip(np.digitize(p, edges[1:-1]), 0, bins - 1)
    rows, ece = [], 0.0
    for b in range(bins):
        m = idx == b
        if m.any():
            conf, acc = p[m].mean(), y[m].mean()
            rows.append((edges[b], edges[b + 1], int(m.sum()), conf, acc))
            ece += m.mean() * abs(conf - acc)
    return rows, float(ece)


@dataclass
class ProbabilityCalibrator:
    """Isotonic recalibration of P(top structure) (Zadrozny-Elkan; Kuleshov et al. 2018)."""

    tag: str = PRIOR_TAG
    _iso: object = None

    def fit(self, p, correct):
        from sklearn.isotonic import IsotonicRegression

        self._iso = IsotonicRegression(y_min=0.0, y_max=1.0, out_of_bounds="clip")
        self._iso.fit(np.asarray(p, float), np.asarray(correct, float))
        return self

    def __call__(self, p):
        p = np.asarray(p, float)
        return p if self._iso is None else self._iso.predict(p)


@dataclass
class VennAbersCalibrator:
    """Inductive Venn-Abers predictor (Vovk, Petej, Fedorova 2015): for a test score s, isotonic
    fits on the calibration set augmented with (s, 0) and with (s, 1) give p0 <= p1, a multi-
    probability that is calibrated in the Venn sense for exchangeable runs; the point estimate is
    p1 / (1 - p0 + p1). It needs no tuning and is meant for small calibration sets, where a single
    isotonic map overfits. An alternative L2b map to ProbabilityCalibrator (compared in E14)."""

    tag: str = PRIOR_TAG
    _s: np.ndarray = None
    _y: np.ndarray = None

    def fit(self, p, correct):
        self._s = np.asarray(p, float)
        self._y = np.asarray(correct, float)
        return self

    def interval(self, p):
        from sklearn.isotonic import IsotonicRegression

        p = np.atleast_1d(np.asarray(p, float))
        if self._s is None:
            return p, p
        lo, hi = np.empty(len(p)), np.empty(len(p))
        for i, s in enumerate(p):
            x = np.r_[self._s, s]
            for lab, out in ((0.0, lo), (1.0, hi)):
                iso = IsotonicRegression(y_min=0.0, y_max=1.0, out_of_bounds="clip")
                out[i] = iso.fit(x, np.r_[self._y, lab]).predict([s])[0]
        return lo, hi

    def __call__(self, p):
        p = np.asarray(p, float)
        if self._s is None:
            return p
        lo, hi = self.interval(p)
        return hi / (1.0 - lo + hi)


def _design(feats, names):
    if isinstance(feats, dict):
        return np.column_stack([np.asarray(feats[k], float) for k in names])
    return np.asarray(feats, float)


@dataclass
class IntervalInflator:
    """Monotone map from theory features to a multiplicative width factor, then Mondrian conformal.

    Score per run and quantity: z = |estimate - truth| / half_width (the nominal-level half width).
    fit:        HistGradientBoosting on log z with monotone constraints (fit split)
    calibrate:  per regime (Mondrian bins), the conformal quantile of z / g(features) at level 1-alpha
                (calibrate split), so the final factor is q_regime * g(features)
    The scale is never below 1: recalibration widens intervals, it does not claim more precision
    than the model gives (rule 4: Monte Carlo spread is a floor, not a target)."""

    names: tuple = tuple(THEORY_FEATURES)
    alpha: float = 0.10
    regime_feature: str | None = "split_amp"
    regime_edges: tuple = ()
    tag: str = PRIOR_TAG
    signs: dict | None = None  # monotone sign per feature (None: THEORY_FEATURES)
    _g: object = None
    _q: dict = field(default_factory=dict)
    _keep: np.ndarray = None

    def _regime(self, X):
        if self.regime_feature is None or not self.regime_edges:
            return np.zeros(len(X), int)
        j = self.names.index(self.regime_feature)
        v = X[:, j]
        return np.where(np.isfinite(v), np.digitize(v, self.regime_edges), -1)  # NaN -> pooled

    def fit(self, feats, z):
        from sklearn.ensemble import HistGradientBoostingRegressor

        X = _design(feats, self.names)
        fin = np.isfinite(X)
        lo = np.where(fin, X, np.inf).min(0)
        hi = np.where(fin, X, -np.inf).max(0)
        self._keep = np.where(fin.any(0) & (hi > lo))[0]  # features not exported yet are all-NaN
        if len(self._keep) == 0:
            self._g = None
            return self
        X = X[:, self._keep]
        cst = [(self.signs or THEORY_FEATURES).get(self.names[j], 0) for j in self._keep]
        self._g = HistGradientBoostingRegressor(max_iter=200, max_depth=3, learning_rate=0.05,
                                                monotonic_cst=cst, min_samples_leaf=40)
        self._g.fit(X, np.log(np.maximum(np.asarray(z, float), 1e-6)))
        return self

    def base(self, feats):
        X = _design(feats, self.names)
        if self._g is None:
            return np.ones(len(X))
        return np.exp(self._g.predict(X[:, self._keep]))

    def calibrate(self, feats, z):
        X = _design(feats, self.names)
        r = self._regime(X)
        s = np.asarray(z, float) / self.base(X)
        self._q = {-1: conformal_quantile(s, self.alpha)}  # pooled: used for small or unseen regimes
        for k in np.unique(r):
            sk = s[r == k]
            if k >= 0 and len(sk) >= int(np.ceil(1 / self.alpha)):  # enough runs for a finite quantile
                self._q[int(k)] = conformal_quantile(sk, self.alpha)
        return self

    def raw_scale(self, feats):
        """Width factor per run without the floor at 1 (S-LEARNED L2c clips it to [0.5, 5] itself)."""
        X = _design(feats, self.names)
        if not self._q:
            return np.ones(len(X))
        r = self._regime(X)
        return np.array([self._q.get(int(k), self._q[-1]) for k in r]) * self.base(X)

    def __call__(self, feats):
        """Width factor per run (>= 1). Before calibrate(): 1 everywhere (layer off)."""
        X = _design(feats, self.names)
        if not self._q:
            return np.ones(len(X))
        r = self._regime(X)
        q = np.array([self._q.get(int(k), self._q[-1]) for k in r])
        return np.maximum(q * self.base(X), 1.0)


def conformal_quantile(scores, alpha):
    """Split-conformal (1 - alpha) quantile with the finite-sample correction."""
    s = np.sort(np.asarray(scores, float))
    n = len(s)
    i = int(np.ceil((n + 1) * (1 - alpha))) - 1
    return float(s[min(i, n - 1)]) if i < n else float("inf")
