"""V1: learned multi-label combiner of the deterministic V0 diagnostics (PHASE4_ML_PLAN.md, V).

Input: a fixed-length feature vector per run, made of the V0 statistics (each a calibrated p-value
or a raw statistic, produced by the deterministic battery `pdefactor.validate`, other session) and
permutation-invariant aggregates of the factor list (`factor_aggregates`). Identifiers (case name,
seed) are never features: a model that can see them learns the simulator, not the failure.

Output, per run:
- a probability per failure mode (one-vs-rest gradient-boosted trees; monotone where the sign of a
  statistic is known), only meaningful within the simulator prior (tagged PRIOR_TAG);
- a reported *set* of failure modes chosen by conformal risk control (Angelopoulos et al. 2022):
  one threshold lambda on the per-mode probabilities such that the expected fraction of true
  failure modes missed is <= alpha on exchangeable runs (multi-label, so single-label conformal
  sets do not apply);
- an OOD gate: a conformal outlier p-value (Bates et al. 2023) of the Mahalanobis distance of the
  feature vector to the calibration runs. When OOD, the probabilities are withheld and the report
  says "outside the validator's training range": the failures that matter most on real data are
  out of scope, and a classifier trained in-prior must not pretend to grade them.

V1 diagnoses only. It never changes a label (rule 5) and never acts: actions are the controller's
(remedy.py orders them).
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from . import PRIOR_TAG

# failure modes of PHASE4 sec. 8 that a run-level combiner can usefully separate
FAILURE_MODES = (
    "high_kappa_loss",      # V0.1   -> L1a / L0 / L1b
    "too_few_kappa",        # V0.2   -> ID-KER (no fix)
    "spurious_factor",      # V0.3   -> raw_subset / refine
    "local_optimum",        # V0.4   -> restarts, more samples
    "noise_misspecified",   # V0.5   -> report noise model
    "degree_too_low",       # V0.6 saturating -> _grow
    "out_of_class",         # V0.6 non-saturating, V0.7, V0.8 -> stop, MISFIT/UNDECIDED
    "unsplit_reducible",    # V0.9   -> split_quadratics
    "weights_inseparable",  # V0.10  -> report the floor
    "repeated_factor",      # V0.11  -> UNDECIDED
)


def factor_aggregates(factors):
    """Permutation-invariant summary of a variable-length factor list. Each factor is a dict with
    any of: coef_z (array of |coef| / sd), support (number of kappa), incl (inclusion probability),
    rho, kappa_vand, margin (n_kappa - (dx+1)). Only keys present in some factor are aggregated;
    a factor missing a present key counts as NaN (trees handle it)."""
    keys = ("coef_z", "support", "incl", "rho", "kappa_vand", "margin")
    out = {"n_factors": float(len(factors))}
    for k in keys:
        if not any(k in f for f in factors):
            continue
        v = []
        for f in factors:
            x = f.get(k, np.nan)
            v.append(np.nanmin(x) if np.ndim(x) else x)  # weakest coefficient of a factor
        v = np.asarray(v, float) if v else np.array([np.nan])
        ok = v[np.isfinite(v)]
        out[f"{k}_min"] = float(ok.min()) if ok.size else np.nan
        out[f"{k}_max"] = float(ok.max()) if ok.size else np.nan
        out[f"{k}_mean"] = float(ok.mean()) if ok.size else np.nan
    return out


def _risk_threshold(P, Y, alpha):
    """Conformal risk control for the false-negative rate of the reported set {j : P_j >= lam}.
    Loss per run: fraction of its true modes missed (0 if it has none), bounded by 1. Choose the
    largest lam with (n R_hat(lam) + 1) / (n + 1) <= alpha; R_hat is monotone in lam."""
    n = len(P)
    pos = Y.sum(1)
    grid = np.unique(np.r_[0.0, P.ravel()])[::-1]  # from high to low lam

    def risk(lam):
        miss = ((P < lam) & (Y == 1)).sum(1)
        return np.where(pos > 0, miss / np.maximum(pos, 1), 0.0).mean()

    for lam in grid:  # largest lam that satisfies the bound gives the smallest sets
        if (n * risk(lam) + 1) / (n + 1) <= alpha:
            return float(lam)
    return 0.0


@dataclass
class Validator:
    """One-vs-rest GBM per failure mode + conformal risk control + OOD gate. Off = not fitted:
    `predict` returns None and the report shows the V0 statistics only."""

    modes: tuple = FAILURE_MODES
    alpha: float = 0.10          # target missed-failure rate
    ood_level: float = 0.01      # conformal outlier p-value below which the run is OOD
    monotone: dict = field(default_factory=dict)  # feature index -> +1 / -1, applied to every mode
    tag: str = PRIOR_TAG
    _models: dict = field(default_factory=dict)
    _fill: np.ndarray = None
    _lam: float = 0.5
    _mu: np.ndarray = None
    _icov: np.ndarray = None
    _cal_d: np.ndarray = None
    _cols: np.ndarray = None     # columns kept by fit (finite somewhere and not constant)

    def fit(self, X, Y):
        from sklearn.ensemble import HistGradientBoostingClassifier

        X, Y = np.asarray(X, float), np.asarray(Y, int)
        fin = np.isfinite(X)
        lo = np.where(fin, X, np.inf).min(0)
        hi = np.where(fin, X, -np.inf).max(0)
        self._cols = np.where(fin.any(0) & (hi > lo))[0]  # all-NaN or constant columns carry nothing
        cst = [self.monotone.get(j, 0) for j in self._cols]
        X = X[:, self._cols]
        self._models = {}
        for j, m in enumerate(self.modes):
            y = Y[:, j]
            if y.min() == y.max():  # never (or always) seen: constant probability
                self._models[m] = float(y[0])
                continue
            clf = HistGradientBoostingClassifier(max_iter=200, max_depth=3, learning_rate=0.05,
                                                 min_samples_leaf=20, monotonic_cst=cst)
            self._models[m] = clf.fit(X, y)
        self._fill = np.nanmedian(X, 0)
        Xf = np.where(np.isfinite(X), X, self._fill)
        self._mu = Xf.mean(0)
        C = np.cov(Xf, rowvar=False) + 1e-6 * np.eye(X.shape[1])
        self._icov = np.linalg.pinv(np.atleast_2d(C))
        return self

    def proba(self, X):
        X = np.asarray(X, float)[:, self._cols]
        cols = []
        for m in self.modes:
            mdl = self._models[m]
            cols.append(np.full(len(X), mdl) if isinstance(mdl, float) else mdl.predict_proba(X)[:, 1])
        return np.column_stack(cols)

    def _dist(self, X):
        X = np.asarray(X, float)[:, self._cols]
        X = np.where(np.isfinite(X), X, self._fill)  # same fill as fit
        D = X - self._mu
        return np.sqrt(np.einsum("ij,jk,ik->i", D, self._icov, D))

    def calibrate(self, X, Y):
        """Risk-control threshold and the OOD reference distances, on the calibrate split only."""
        self._lam = _risk_threshold(self.proba(X), np.asarray(Y, int), self.alpha)
        self._cal_d = np.sort(self._dist(X))
        return self

    def ood_pvalue(self, X):
        d = self._dist(X)
        n = len(self._cal_d)
        return (1 + n - np.searchsorted(self._cal_d, d, side="left")) / (n + 1)

    def predict(self, X):
        """List per run: {'ood', 'p_ood', 'proba', 'set', 'tag'}; None when the layer is off."""
        if not self._models or self._cal_d is None:
            return None
        P, pv = self.proba(X), self.ood_pvalue(X)
        out = []
        for i in range(len(P)):
            ood = bool(pv[i] < self.ood_level)
            out.append({
                "ood": ood,
                "p_ood": float(pv[i]),
                "proba": None if ood else dict(zip(self.modes, map(float, P[i]))),
                "set": None if ood else [m for m, p in zip(self.modes, P[i]) if p >= self._lam],
                "tag": self.tag,
            })
        return out
