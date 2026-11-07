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
from pathlib import Path

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
    _scale: np.ndarray = None
    _cal_d: np.ndarray = None
    _cols: np.ndarray = None     # columns kept by fit (finite somewhere and not constant)

    def fit(self, X, Y):
        from sklearn.ensemble import HistGradientBoostingClassifier

        X, Y = np.asarray(X, float), np.asarray(Y, int)
        X = np.where(np.isfinite(X), X, np.nan)  # +-inf (e.g. an infinite evidence gap) = missing
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
        from sklearn.covariance import LedoitWolf

        self._fill = np.nanmedian(X, 0)
        Xf = np.where(np.isfinite(X), X, self._fill)
        self._mu = Xf.mean(0)
        self._scale = np.where(Xf.std(0) > 0, Xf.std(0), 1.0)
        Z = (Xf - self._mu) / self._scale  # standardised: features differ by orders of magnitude
        self._icov = LedoitWolf().fit(Z).precision_  # shrinkage: few runs, many features
        return self

    def proba(self, X):
        X = np.asarray(X, float)[:, self._cols]
        X = np.where(np.isfinite(X), X, np.nan)
        cols = []
        for m in self.modes:
            mdl = self._models[m]
            cols.append(np.full(len(X), mdl) if isinstance(mdl, float) else mdl.predict_proba(X)[:, 1])
        return np.column_stack(cols)

    def _dist(self, X):
        X = np.asarray(X, float)[:, self._cols]
        X = np.where(np.isfinite(X), X, self._fill)  # same fill as fit
        D = (X - self._mu) / self._scale
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


# ====================================================================== S-LEARNED-V1 (2026-10-29)
# Failure detector on the V0 battery, the V0 exports, the step log and the residual diagnostics
# (sessions/LEARNED/V1/PLAN.md sec. 3). Report only: it never changes a label.
V1_TAG = "prior: sim-v2"
V0_KEYS = ("v01_omnibus_logp", "v01_omnibus_z", "v01_n_bad_bins", "v01_max_bad_kappa", "v01_worst_logp",
           "v02_min_margin", "v03_gap", "v03_entropy", "v10_cF", "v10_gamma", "v10_w_rel", "v13_heldout")
RESID_KEYS = ("lb_t_logp", "acf1_t", "acf1_x", "flat_x", "kslope", "bp_logp", "half_ratio", "nyq_ratio")
EXPORT_KEYS = ("kappa_vand", "log_snr", "disagreement", "split_floor", "log_nobs", "mode_margin", "rel_width")
RUN_KEYS = ("p_top", "structure_entropy", "regrouped", "n_dropped", "evidence_gap", "n_factors", "coef_z_min",
            "coef_z_max", "support_min", "margin_min")
STEPS = ("core", "grow", "decide", "recurse", "kappa_support", "complex", "raw_subset", "refine", "split_branches",
         "alternatives", "bootstrap", "split_layer")
LABELS = ("FIT-COMPATIBLE", "MISFIT", "ID-KER", "UNDECIDED")


def feature_names(resid=True):
    names = [f"v0:{k}" for k in V0_KEYS]
    if resid:
        names += [f"resid:{k}" for k in RESID_KEYS]
    names += [f"export:{k}_{a}" for k in EXPORT_KEYS for a in ("min", "max", "mean")]
    names += [f"run:{k}" for k in RUN_KEYS]
    names += [f"step:{s}_changed" for s in STEPS]
    names += [f"label:{lab}" for lab in LABELS] + ["design:scattered"]
    return names


def _f(d, k):
    v = d.get(k)
    try:
        return float(v) if v is not None else np.nan
    except (TypeError, ValueError):
        return np.nan


def featurise(row, resid=True):
    """Fixed-length float vector (feature_names order) from a corpus row or a run-time row dict.
    Dimensionless only; no family, seed or case name. Missing values are NaN (trees handle them)."""
    out = []
    v0 = row.get("v0") or {}
    out += [_f(v0, k) for k in V0_KEYS]
    if resid:
        rs = row.get("resid") or {}
        # log p floored at -300 as validate._log10sf (rows written before resid used it hold -inf)
        out += [max(_f(rs, k), -300.0) if k.endswith("_logp") else _f(rs, k) for k in RESID_KEYS]
    ex = row.get("export") or []
    for k in EXPORT_KEYS:
        v = np.array([_f(e, k) for e in ex], float)
        v = v[np.isfinite(v)]
        out += [float(v.min()), float(v.max()), float(v.mean())] if v.size else [np.nan] * 3
    run = row.get("run") or {}
    out += [_f(run, k) for k in RUN_KEYS]
    # no wall-time fractions: they depend on load, machine and pipeline version (G fit+cal rows with
    # one more step were separated from G test / I rows by step:raw_subset_frac alone, AUROC 1.00)
    st = {s[0]: bool(s[2]) for s in (row.get("steps") or [])}
    out += [float(st[s]) if s in st else np.nan for s in STEPS]
    lab = str(row.get("label", ""))
    out += [float(lab.startswith(L)) for L in LABELS]
    des = row.get("design") or ["grid"]
    out += [float(isinstance(des[0], (int, float)))]  # scattered designs carry the point count
    v = np.asarray(out, float)
    return np.where(np.isfinite(v), v, np.nan)


def smooth_noise(samples, w, r=4, factor=np.sqrt(2)):
    """GPPosterior.effective_noise(kind="smooth") restated on arrays.
    origin: PDEFactorML/benchmarks/bench_e2e.py:48 (copied so the package does not import benchmarks)."""
    from numpy.polynomial import legendre

    samples = np.asarray(samples)
    w = np.asarray(w, float) / np.sum(w)
    d = samples - np.tensordot(w, samples, 1)[None]
    nt, nx = d.shape[-2:]
    B = np.fft.fft(d, axis=-1) / nx
    Q, _ = np.linalg.qr(legendre.legvander(np.linspace(-1, 1, nt), r - 1))
    P = np.einsum("ta,stk->sak", Q, B)
    b2 = (np.sum(w[:, None, None] * (np.abs(P) ** 2).sum(1), axis=0) / r).max()
    return float(factor * np.sqrt(b2) * np.sqrt(nx))


def runtime_row(res, samples, pis, t, x, sigma, noise_draws, raw):
    """The corpus row fields V1 / L2b read (benchmarks/ml_layers/ll_corpus._features), built at run time from
    the same inputs. Each part is guarded: a failure leaves that part missing (NaN features)."""
    from . import features as F
    from .resid import diagnostics

    pis = np.ones(len(samples)) if pis is None else np.asarray(pis, float)
    if len(samples) == 1:
        u, gs = samples[0], sigma
    else:
        u = np.tensordot(pis / pis.sum(), np.asarray(samples), 1)
        gs = sigma if sigma and sigma > 0 else smooth_noise(samples, pis)
    row = dict(label=res.label, steps=list(res.steps or []), design=["grid" if raw is None else len(raw["ys"])])
    try:
        row["run"] = F.run_features(res)
    except Exception:  # noqa: BLE001
        pass
    try:
        from ..validate import validate

        row["v0"] = validate(res, u, t, x, gs).features()
    except Exception:  # noqa: BLE001
        pass
    try:
        from ..loop import l2c_data

        row["export"] = F.export_features(res, l2c_data(samples, pis, t, x, sigma, noise_draws, raw))
    except Exception:  # noqa: BLE001
        pass
    try:
        row["resid"] = diagnostics(res.factors, u, t, x)
    except Exception:  # noqa: BLE001
        pass
    return row


def _hgb(seed=0):
    from sklearn.ensemble import HistGradientBoostingClassifier

    return HistGradientBoostingClassifier(max_iter=200, max_depth=3, learning_rate=0.05, min_samples_leaf=10,
                                          l2_regularization=1.0, random_state=seed)


def conformal_pvalue(cal_scores, s):
    """Conformal outlier p-value (Bates et al. 2023): larger score = more anomalous."""
    c = np.sort(np.asarray(cal_scores, float))
    s = np.atleast_1d(np.asarray(s, float))
    n = len(c)
    return (1 + n - np.searchsorted(c, s, side="left")) / (n + 1)


@dataclass
class FailureDetector:
    """Binary failure score (HGB: injected failure vs clean-data run), conformalised on clean
    calibration runs so the false-alarm rate on exchangeable clean runs is <= alpha; plus an
    open-set type head: a failure type is reported only when its probability passes a threshold
    fitted on calibration failures of seen types, else "other"."""

    alpha: float = 0.05
    type_level: float = 0.10     # fraction of seen-type calibration failures allowed below the type threshold
    resid: bool = True
    designs: tuple = ("grid", "scattered")  # data designs present in the training corpus
    tag: str = V1_TAG
    _clf: object = None
    _types: object = None
    _cal: np.ndarray = None
    _tau: float = 1.0
    _cols: np.ndarray = None

    def _x(self, X):
        return np.asarray(X, float)[:, self._cols]

    def fit(self, X, y_fail, types=None):
        X, y = np.asarray(X, float), np.asarray(y_fail, int)
        fin = np.isfinite(X)
        lo = np.where(fin, X, np.inf).min(0)
        hi = np.where(fin, X, -np.inf).max(0)
        self._cols = np.where(fin.any(0) & (hi > lo))[0]  # all-NaN or constant columns carry nothing
        X = X[:, self._cols]
        self._clf = _hgb().fit(X, y)
        if types is not None:
            t = np.asarray(types, object)
            m = y == 1
            if len(set(t[m])) >= 2:
                self._types = _hgb(seed=1).fit(X[m], t[m].astype(str))
        return self

    def score(self, X):
        return self._clf.predict_proba(self._x(X))[:, 1]

    def calibrate(self, X_clean, X_fail=None, types_fail=None):
        self._cal = np.sort(self.score(X_clean))
        if self._types is not None and X_fail is not None and len(X_fail):
            P = self._types.predict_proba(self._x(X_fail))
            cls = list(self._types.classes_)
            pt = np.array([P[i, cls.index(str(k))] if str(k) in cls else np.nan for i, k in enumerate(types_fail)])
            pt = pt[np.isfinite(pt)]
            if pt.size:
                self._tau = float(np.quantile(pt, self.type_level))
        return self

    def pvalue(self, X):
        return conformal_pvalue(self._cal, self.score(X))

    def flag(self, X):
        return self.pvalue(X) <= self.alpha

    def type_of(self, X):
        if self._types is None:
            return [None] * len(X)
        P = self._types.predict_proba(self._x(X))
        cls = self._types.classes_
        return [str(cls[i]) if p[i] >= self._tau else "other" for p, i in zip(P, P.argmax(1))]

    def report(self, x):
        x = np.asarray(x, float)[None]
        pv = float(self.pvalue(x)[0])
        fl = bool(pv <= self.alpha)
        return {"p_failure": float(self.score(x)[0]), "p_value": pv, "flag": fl,
                "type": self.type_of(x)[0] if fl else None, "alpha": self.alpha, "tag": self.tag}


# ---------------------------------------------------------------------- run-time report (hook)
MODEL_DIR = Path(__file__).parent / "models"


def load_model(name):
    import joblib

    p = MODEL_DIR / name
    return joblib.load(p) if p.exists() else None


def attach(out, ll, samples, pis, t, x, sigma, noise_draws, raw):
    """End of run_loop at depth 0 (validator / prob_calibration on): writes out.learned_report[<layer>]
    and one note line. The label is untouched, except validator="downgrade": a V1-flagged FIT-COMPATIBLE
    label becomes UNDECIDED (a downgrade to an abstention, never an upgrade)."""
    row = runtime_row(out, samples, pis, t, x, sigma, noise_draws, raw)
    rep = dict(out.learned_report or {})
    msg = []
    if ll.validator:
        det = load_model("v1.joblib")
        design = "grid" if raw is None else "scattered"
        if det is None:
            rep["v1"] = {"status": "no model", "tag": V1_TAG}
        elif design not in det.designs:
            rep["v1"] = {"status": f"{design} data not covered by the training corpus", "tag": det.tag}
        else:
            rep["v1"] = det.report(featurise(row, resid=det.resid))
            if rep["v1"]["flag"]:
                msg.append(f"V1: run unlike clean in-prior runs (conformal p = {rep['v1']['p_value']:.3g}, "
                           f"type {rep['v1']['type']}; {V1_TAG})")
                if ll.validator == "downgrade" and out.label == "FIT-COMPATIBLE":
                    # downgrade only (never an upgrade): a flagged confident answer is withheld
                    out.label = "UNDECIDED"
                    rep["v1"]["downgraded"] = True
                    msg.append("V1 downgrade: label FIT-COMPATIBLE -> UNDECIDED (the factors are kept as the "
                               "pipeline's candidate, not claimed)")
    if ll.prob_calibration:
        cal = load_model("ptop.joblib")
        p = (row.get("run") or {}).get("p_top")
        if cal is None or p is None:
            rep["ptop"] = {"status": "no model" if cal is None else "no structures", "tag": V1_TAG}
        else:
            from .ptop import feature_matrix

            X = feature_matrix([row]) if cal.method == "logit-features" else None
            q = float(np.ravel(cal(np.array([p]), X))[0])
            lo, hi = cal.interval(np.array([p])) if cal.method == "venn-abers" else ([q], [q])
            rep["ptop"] = {"p_top": float(p), "p_top_calibrated": q,
                           "interval": (float(np.ravel(lo)[0]), float(np.ravel(hi)[0])), "method": cal.method,
                           "tag": cal.tag}
            msg.append(f"L2b: calibrated P(top) = {q:.3g} (raw {p:.3g}; {cal.tag})")
    out.learned_report = rep
    if msg:
        out.note = (out.note + "\n" if out.note else "") + "\n".join(msg)
