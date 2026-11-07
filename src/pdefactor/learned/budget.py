"""LB: learned skip of expensive optional steps of run_loop (sessions/LEARNED/LB/PLAN.md).

`run_loop(..., learned=Learned(budget=True))` asks, before each guarded step, whether the fitted model
predicts that the step will change nothing; if so the step is skipped and the skip is written into the
note. A skip removes candidates, it never changes a score or a label.

- Harm (as in CALM, Schuster et al. 2022): the label or the final factor set differs from the off run.
- Loss label: the off run's `changed` bit of the step (`loop._fp`: note, label, factor strings,
  coefficient tuples, evidence). A step with changed = False left the state exactly as it was, so
  skipping it is exact (C1); the bit over-counts harm when changed = True (conservative).
- Exact replay (C2): steps run in a fixed order and a skip with changed = False leaves the state of
  every later step as in the off run, so the per-run loss and the saved seconds of any threshold are
  computed from off-run logs alone (`replay`).
- One threshold lam for every step (skip when p_change <= lam), chosen by conformal risk control at
  alpha = 0.02 (`validator._risk_threshold`'s rule; Angelopoulos et al. 2022); the Learn-then-Test
  bound (binomial tail, fixed sequence) is reported next to it (`ltt_threshold`).

Zero-harm rule (user direction 2026-10-30, accuracy over speed): `calibrate(..., rule="zero")` takes the
largest lam with no harmed calibrate run; the shipped claim is the held-out count, 0 of n harmed, with
its one-sided 95 % Clopper-Pearson upper bound 1 - 0.05 ** (1 / n) (about 3 / n), stated in the REPORT.

With budget=True and no fitted model the layer is log-only: the guards record their features and never
skip, so the output equals the off run (used to build the training corpus).
"""
from __future__ import annotations

import math
import os
import pickle
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

STEPS = ("grow", "recurse", "complex", "alternatives")
ALPHA = 0.02
MEMO = True  # exact mode-step memo with budget=True (core cache=); False only for log-only off-equivalent rows
MEMO_DEFAULT = os.environ.get("PDEFACTOR_LB_MEMO", "1") == "1"  # memo on in every run_loop, layers off too (P7 user decision)
MODELS = Path(__file__).with_name("models")
_CACHE = {}

FEATURES = ("p_top", "entropy", "n_struct", "log_gap12", "pk_top", "k_top", "p_fit", "p_misfit", "p_idker",
            "n_factors", "m_bound", "dx_bound", "log_snr", "log_n_obs", "log_n_samples", "scattered", "real",
            "lp", "ch_grow", "ch_decide", "ch_recurse", "ch_kappa_support", "ch_complex", "ch_refine",
            "ch_split_branches", "n_grow_options", "max_m_factor", "n_alt")


def features(step, *, agg, bounds, sigma, samples, raw=None, rows=(), n_factors=None, factors=None, lp=None,
             n_grow_options=None):
    """Dimensionless features at the guard of `step`, before it runs (rule 8: logs, ratios, counts,
    probabilities; no seconds, no raw scales). NaN where undefined."""
    nan = float("nan")
    st = dict(agg.structures_pooled or {})
    ps = np.sort(np.asarray(list(st.values()), float))[::-1] if st else np.zeros(0)
    pk = dict(agg.dp.p_k) if getattr(agg, "dp", None) is not None else dict(getattr(agg, "k_structure", {}) or {})
    labs = dict(agg.labels or {})
    u = samples[0]
    n_obs = len(raw["ys"]) if raw is not None and "ys" in raw else np.size(u)
    sd = float(np.std(np.real(u)) + (np.std(np.imag(u)) if np.iscomplexobj(u) else 0.0))
    ch = {name: float(c) for name, _, c in rows}
    f = dict(
        p_top=float(ps[0]) if ps.size else nan,
        entropy=float(-np.sum(ps[ps > 0] * np.log(ps[ps > 0]))) if ps.size else nan,
        n_struct=float(np.sum(ps >= 0.01)),
        log_gap12=float(np.log(ps[0] / ps[1])) if ps.size > 1 and ps[1] > 0 else nan,
        pk_top=float(max(pk.values())) if pk else nan,
        k_top=float(max(pk, key=pk.get)) if pk else nan,
        p_fit=float(labs.get("FIT-COMPATIBLE", 0.0)),
        p_misfit=float(labs.get("MISFIT", 0.0)),
        p_idker=float(labs.get("ID-KER", 0.0)),
        n_factors=nan if n_factors is None else float(n_factors),
        m_bound=float(bounds[0]),
        dx_bound=float(bounds[1]),
        log_snr=float(np.log(sd / sigma)) if sigma and sigma > 0 and sd > 0 else nan,
        log_n_obs=float(np.log(n_obs)),
        log_n_samples=float(np.log(len(samples))),
        scattered=float(raw is not None),
        real=float(np.isrealobj(u)),
        lp=nan if lp is None else float(max(lp, -50.0)),
        n_grow_options=nan if n_grow_options is None else float(n_grow_options),
        max_m_factor=float(max((max(a for a, _ in fr.coef) for fr in factors), default=0)) if factors else nan,
        n_alt=float(max(np.sum(ps >= 0.01) - 1, 0)) if ps.size else nan,
    )
    for name in ("grow", "decide", "recurse", "kappa_support", "complex", "refine", "split_branches"):
        f[f"ch_{name}"] = ch.get(name, nan)
    return {k: f[k] for k in FEATURES}


def vec(feats):
    return np.array([feats.get(k, np.nan) for k in FEATURES], float)


@dataclass
class BudgetModel:
    """Per-step classifiers of P(step changes the state) and one risk-controlled threshold."""

    kind: str                      # "constant" | "logistic" | "hgb"
    models: dict                   # step -> fitted estimator with predict_proba, or a float (constant)
    lam: float = -1.0              # skip when p_change <= lam; < 0 never skips
    alpha: float = ALPHA
    meta: dict = field(default_factory=dict)

    def p_change(self, step, feats):
        m = self.models.get(step)
        if m is None:
            return 1.0
        if isinstance(m, (float, int)):
            return float(m)
        return float(m.predict_proba(vec(feats)[None])[0, 1])

    def skip(self, step, feats):
        return step in self.models and self.p_change(step, feats) <= self.lam


PROFILES = {True: "lb_exact", "exact": "lb_exact", "fast": "lb_fast"}


def model_name(flag):
    """Learned.budget -> model file name. "exact" (= True): 0 harmed runs observed on held-out cases,
    the candidate for normal use; "fast": harmed runs <= alpha = 2 % by risk control, for training and
    screening runs only (user direction 2026-10-30)."""
    return PROFILES[flag]


def load(name="lb_exact"):
    """The fitted model, or None (log-only mode). Cached per process; tests set `_CACHE[name]`."""
    if name not in _CACHE:
        p = MODELS / f"{name}.pkl"
        _CACHE[name] = pickle.loads(p.read_bytes()) if p.exists() else None
    return _CACHE[name]


# ------------------------------------------------------------------ fitting and risk control (offline)
def step_table(rows):
    """Per (run, guarded step) records from log-mode rows: run index, step, features, changed, seconds."""
    out = []
    for i, r in enumerate(rows):
        lb = r.get("lb") or {}
        secs = {}
        chg = {}
        for name, sec, c in r.get("steps") or []:
            if name in STEPS:
                secs[name] = secs.get(name, 0.0) + sec
                chg[name] = chg.get(name, False) or bool(c)
        for step, feats in (lb.get("features") or {}).items():
            if step in chg:
                out.append(dict(run=i, step=step, x=vec(feats), y=int(chg[step]), sec=secs[step]))
    return out


def fit(rows, kind="hgb", seed=0):
    """Per-step classifiers of the changed bit (lam is set separately by `calibrate`)."""
    from sklearn.ensemble import HistGradientBoostingClassifier
    from sklearn.feature_selection import VarianceThreshold
    from sklearn.impute import SimpleImputer
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler

    tab = step_table(rows)
    models = {}
    for step in STEPS:
        d = [r for r in tab if r["step"] == step]
        if not d:
            continue
        X, y = np.array([r["x"] for r in d]), np.array([r["y"] for r in d])
        if kind == "constant" or min(y.sum(), len(y) - y.sum()) < 2 or (kind == "hgb" and len(y) < 20):
            # too few events of one class (or too few rows for the histogram bins): the smoothed rate
            # Laplace-smoothed rate: a step never seen changing still gets p > 0
            models[step] = float((y.sum() + 1) / (len(y) + 2))
        elif kind == "logistic":
            models[step] = make_pipeline(SimpleImputer(strategy="median", keep_empty_features=True), StandardScaler(),
                                         LogisticRegression(C=1.0, max_iter=2000)).fit(X, y)
        else:
            # constant fill + variance filter: HGB's binning fails on a column with one distinct value
            models[step] = make_pipeline(SimpleImputer(strategy="constant", fill_value=-1e3, keep_empty_features=True),
                                         VarianceThreshold(0.0),
                                         HistGradientBoostingClassifier(max_iter=100, learning_rate=0.1,
                                                                        max_leaf_nodes=8, min_samples_leaf=5,
                                                                        random_state=seed)).fit(X, y)
    return BudgetModel(kind=kind, models=models, meta=dict(n_fit=len(rows)))


def run_scores(model, rows):
    """Per run: list of (p_change, changed, seconds) of its guarded steps."""
    tab = step_table(rows)
    out = [[] for _ in rows]
    for r in tab:
        m = model.models.get(r["step"])
        if m is None:
            continue
        p = float(m) if isinstance(m, (float, int)) else float(m.predict_proba(r["x"][None])[0, 1])
        out[r["run"]].append((p, r["y"], r["sec"]))
    return out


def loss_at(scores, lam):
    """Per-run loss (some skipped step changed the state) and saved seconds at threshold lam (C2)."""
    L = np.array([float(any(p <= lam and y for p, y, _ in s)) for s in scores])
    S = np.array([sum(sec for p, _, sec in s if p <= lam) for s in scores])
    return L, S


def crc_threshold(scores, alpha=ALPHA):
    """Conformal risk control: largest lam with (n R_hat(lam) + 1) / (n + 1) <= alpha (loss in [0, 1],
    non-decreasing in lam); -1 (never skip) when none qualifies."""
    n = len(scores)
    grid = np.unique([p for s in scores for p, _, _ in s])
    best = -1.0
    for lam in grid:  # R_hat is non-decreasing in lam: stop at the first violation
        L, _ = loss_at(scores, lam)
        if (n * L.mean() + 1) / (n + 1) <= alpha:
            best = float(lam)
        else:
            break
    return best


def zero_threshold(scores):
    """Largest lam with no harmed run on these scores; -1 (never skip) when even the smallest skips harm."""
    grid = np.unique([p for s in scores for p, _, _ in s])
    best = -1.0
    for lam in grid:
        L, _ = loss_at(scores, lam)
        if L.sum() == 0:
            best = float(lam)
        else:
            break
    return best


def zero_bound(n, conf=0.95):
    """One-sided upper confidence bound of the harmed rate after 0 harmed of n runs."""
    return 1.0 - (1.0 - conf) ** (1.0 / n) if n > 0 else 1.0


def binom_cdf(k, n, p):
    return float(sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(k + 1)))


def ltt_threshold(scores, alpha=ALPHA, delta=0.1):
    """Learn then Test (Angelopoulos et al. 2021): fixed-sequence test from the most conservative lam
    upward of H0: R(lam) > alpha with the exact binomial p-value P(Bin(n, alpha) <= n R_hat); the last
    rejected lam before the first non-rejection controls P(R(lam) > alpha) <= delta."""
    n = len(scores)
    grid = np.unique([p for s in scores for p, _, _ in s])
    best = -1.0
    for lam in grid:
        L, _ = loss_at(scores, lam)
        if binom_cdf(int(L.sum()), n, alpha) <= delta:
            best = float(lam)
        else:
            break
    return best


def calibrate(model, cal_rows, alpha=ALPHA, delta=0.1, rule="crc"):
    """lam by conformal risk control at alpha (rule "crc") or the zero-harm rule ("zero")."""
    sc = run_scores(model, cal_rows)
    model.lam = zero_threshold(sc) if rule == "zero" else crc_threshold(sc, alpha)
    model.alpha = alpha
    model.meta.update(n_cal=len(cal_rows), lam_ltt=ltt_threshold(sc, alpha, delta), delta=delta, rule=rule,
                      lam_crc=crc_threshold(sc, alpha))
    return model


def replay(model, rows, lam=None):
    """Offline on-arm from log-mode rows (C2): per run, harmed (conservative) and seconds saved."""
    L, S = loss_at(run_scores(model, rows), model.lam if lam is None else lam)
    return L, S
