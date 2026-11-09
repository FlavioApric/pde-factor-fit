"""V1 gate: failure detection on corpus I at a fixed false-alarm rate on clean runs
(sessions/LEARNED/V1/PLAN.md sec. 3.3-3.5).

Report-only layer: labels are unchanged by construction, so everything is computed offline from the
off-arm rows. Clean = G (and S where it has the same features) off rows; failure = I rows.
Every arm's score is conformalised on clean calibration rows (alpha = 0.05; Bates et al. 2023).

Arms: B0 V0 omnibus only; B1 max robust z over the fixed test statistics (no label learning); B2 isolation
forest; B3 Mahalanobis (Ledoit-Wolf); B4 kNN distance; V1 supervised HGB (FailureDetector).

Protocols (never tuned on test):
- split:  fit on fit, calibrate on cal (clean cal rows), evaluate on test;
- LOFO:   fit on the fit rows of four families, calibrate on their cal rows, evaluate on every row
          of the fifth family;
- LOTO:   fit without one injection type (all families), calibrate as split, evaluate the held-out
          type on every I row of that type; the type head must say "other", not a wrong type.
Target (b) (LEARNED PLAN 3.7): run failure on clean data (category not right / equivalent /
abstain-ok): HGB score with a conformal-risk threshold for missed <= 0.10 on cal; report missed and
false-flag on test and per LOFO fold.

  python ll_v1.py --clean ll_G*.jsonl [ll_S.jsonl] --fail ll_I.jsonl [--nulls ll_N.jsonl] [--save]
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))

from pdefactor.learned import validator as V  # noqa: E402

FAMILIES = ("F1", "F2", "F3", "F4", "F5")
ALPHA = 0.05
OUT = ROOT / "sessions" / "LEARNED" / "V1" / "results"
ARMS = ("B0_v0", "B1_minp", "B2_iforest", "B3_mahal", "B4_knn", "V1_hgb")
# fixed test statistics for B1: (feature name, direction) with +1 = larger is more anomalous
B1_STATS = (("v0:v01_omnibus_logp", -1), ("resid:lb_t_logp", -1), ("resid:bp_logp", -1), ("resid:acf1_t", 0),
            ("resid:acf1_x", 0), ("resid:half_ratio", 0), ("resid:nyq_ratio", +1), ("resid:flat_x", -1),
            ("resid:kslope", 0))
BAD = ("TIMEOUT", "CRASH")


def load(paths, corpus=None):
    rows = []
    for p in paths:
        for line in open(p):
            r = json.loads(line)
            if r.get("learned", "off") != "off" or (corpus and r.get("corpus") not in corpus):
                continue
            rows.append(r)
    return rows


def itype(r):
    return (r.get("inject") or {}).get("type") or str(r["design"][0]).split(":")[0]


def ilevel(r):
    return int((r.get("inject") or {}).get("level", str(r["design"][0]).split(":")[-1]))


# ------------------------------------------------------------------ unsupervised / fixed arms
class Arm:
    """fit(X_clean_fit, X_all_fit, y_fit, types) -> score(X) (larger = more anomalous)."""

    def __init__(self, name, resid):
        self.name, self.resid = name, resid
        self.names = V.feature_names(resid)

    def _prep_fit(self, X):
        self.fill = np.nanmedian(X, 0)
        self.fill = np.where(np.isfinite(self.fill), self.fill, 0.0)
        Xf = np.where(np.isfinite(X), X, self.fill)
        self.mu, sd = Xf.mean(0), Xf.std(0)
        self.sd = np.where(sd > 0, sd, 1.0)
        self.keep = sd > 0
        return ((Xf - self.mu) / self.sd)[:, self.keep]

    def _prep(self, X):
        Xf = np.where(np.isfinite(X), X, self.fill)
        return ((Xf - self.mu) / self.sd)[:, self.keep]

    def fit(self, Xc, X, y, types):
        n = self.name
        if n == "B0_v0":
            self.j = self.names.index("v0:v01_omnibus_logp")
        elif n == "B1_minp":
            self.cols = [(self.names.index(f), d) for f, d in B1_STATS if f in self.names]
            self.ref = {}
            for j, d in self.cols:  # robust location / scale of each statistic on clean fit rows
                v = self._stat(Xc[:, j], d)
                v = v[np.isfinite(v)]
                med = np.median(v) if v.size else 0.0
                mad = 1.4826 * np.median(np.abs(v - med)) if v.size else 1.0
                self.ref[j] = (med, mad if mad > 0 else (np.std(v) or 1.0))
        elif n == "B2_iforest":
            from sklearn.ensemble import IsolationForest

            self.m = IsolationForest(n_estimators=300, random_state=0).fit(self._prep_fit(Xc))
        elif n == "B3_mahal":
            from sklearn.covariance import LedoitWolf

            Z = self._prep_fit(Xc)
            self.m = LedoitWolf().fit(Z)
        elif n == "B4_knn":
            from sklearn.neighbors import NearestNeighbors

            self.Z = self._prep_fit(Xc)
            self.m = NearestNeighbors(n_neighbors=min(10, len(self.Z) - 1)).fit(self.Z)
        elif n == "V1_hgb":
            self.m = V.FailureDetector(alpha=ALPHA, resid=self.resid).fit(X, y, types)
        return self

    @staticmethod
    def _stat(v, d):
        v = np.where(np.isfinite(v), v, np.nan)
        return v * d if d else np.abs(v)

    def score(self, X):
        n = self.name
        if n == "B0_v0":
            v = -X[:, self.j]
            return np.where(np.isfinite(v), v, -np.inf)
        if n == "B1_minp":
            zs = []
            for j, d in self.cols:
                med, sc = self.ref[j]
                z = (self._stat(X[:, j], d) - med) / sc
                zs.append(np.where(np.isfinite(z), z, -np.inf))
            return np.max(np.array(zs), 0)  # max robust z: continuous min-p analogue (no ties at the floor)
        if n == "B2_iforest":
            return -self.m.score_samples(self._prep(X))
        if n == "B3_mahal":
            return self.m.mahalanobis(self._prep(X))
        if n == "B4_knn":
            dist, _ = self.m.kneighbors(self._prep(X))
            return dist.mean(1)
        return self.m.score(X)


def evaluate(arm, cal_clean, X_eval_clean, X_eval_fail):
    sc = arm.score(cal_clean)
    thr_p = lambda X: V.conformal_pvalue(sc, arm.score(X)) <= ALPHA  # noqa: E731
    fa = thr_p(X_eval_clean) if len(X_eval_clean) else np.array([])
    det = thr_p(X_eval_fail) if len(X_eval_fail) else np.array([])
    return fa, det


def boot_diff(a, b, B=2000, seed=0):
    rng = np.random.default_rng(seed)
    d = np.asarray(a, float) - np.asarray(b, float)
    m = np.array([d[rng.integers(0, len(d), len(d))].mean() for _ in range(B)])
    return float(d.mean()), float(np.quantile(m, 0.025)), float(np.quantile(m, 0.975))


def _finite(v):
    v = np.asarray(v, float)
    lo = np.nanmin(v[np.isfinite(v)]) - 1 if np.isfinite(v).any() else 0.0
    return np.where(np.isfinite(v), v, np.where(v > 0, -lo + 1e9, lo))


def _auc(sc, sf):
    """P(score of an injected run > score of a clean run), ties count 1/2."""
    if not len(sc) or not len(sf):
        return np.nan
    d = sf[:, None] - sc[None, :]
    return float(((d > 0) + 0.5 * (d == 0)).mean())


def lofo_auc(folds, types, B=2000, seed=0):
    """Mean over held-out families of the per-family AUROC; paired cluster bootstrap CI (base draws,
    i.e. seeds, resampled inside each family with all their rows; the same draw for every arm). Per type:
    the injected rows of that type only. "fc": FIT-COMPATIBLE runs only on both sides (the confident case)."""
    if not folds:
        return {}
    rng = np.random.default_rng(seed)
    out = {"n_folds": len(folds), "arms": {}, "types": {}}
    sub = {"all": {k: (np.ones(f["nc"], bool), np.ones(f["nf"], bool)) for k, f in folds.items()},
           "fc": {k: (f["fcc"], f["fcf"]) for k, f in folds.items()}}
    for tag, m in sub.items():
        key = "arms" if tag == "all" else "arms_fc"
        out[key] = {}
        for n in ARMS:
            by = {k: _auc(f["s"][n][0][m[k][0]], f["s"][n][1][m[k][1]]) for k, f in folds.items()}
            out[key][n] = dict(auc=float(np.nanmean(list(by.values()))), by_fold=by)
        draws = {n: [] for n in ARMS}
        for _ in range(B):
            idx = {}
            for k, f in folds.items():
                g = np.unique(np.r_[f["gc"], f["gf"]])
                pick = rng.choice(g, len(g))
                idx[k] = (np.concatenate([np.where((f["gc"] == p) & m[k][0])[0] for p in pick]),
                          np.concatenate([np.where((f["gf"] == p) & m[k][1])[0] for p in pick]))
            for n in ARMS:
                draws[n].append(np.nanmean([_auc(f["s"][n][0][idx[k][0]], f["s"][n][1][idx[k][1]]) for k, f in folds.items()]))
        for n in ARMS:
            d = np.array(draws[n]) - np.array(draws["B0_v0"])
            out[key][n]["ci"] = (float(np.nanquantile(draws[n], 0.025)), float(np.nanquantile(draws[n], 0.975)))
            out[key][n]["vs_B0"] = (out[key][n]["auc"] - out[key]["B0_v0"]["auc"],
                                    float(np.nanquantile(d, 0.025)), float(np.nanquantile(d, 0.975)))
    out["n_fc"] = (int(sum(f["fcc"].sum() for f in folds.values())), int(sum(f["fcf"].sum() for f in folds.values())))
    # level 1 mixes the seed-400 draw (shared by all levels) with fresh draws 402/403: report both at level 1
    out["seeds"] = {g: {n: float(np.nanmean([_auc(f["s"][n][0], f["s"][n][1][(f["levels"] == 1) & (f["seed400"] == (g == "level 1, draw 400"))])
                                             for f in folds.values()])) for n in ARMS}
                    for g in ("level 1, draw 400", "level 1, fresh draws 402/403")}
    out["levels"] = {lv: {n: float(np.nanmean([_auc(f["s"][n][0], f["s"][n][1][f["levels"] == lv])
                                              for f in folds.values()])) for n in ARMS} for lv in range(3)}
    for t in types:
        out["types"][t] = {n: float(np.nanmean([_auc(f["s"][n][0], f["s"][n][1][f["types"] == t])
                                                for f in folds.values()])) for n in ARMS}
    return out


def binom_hi(k, n):
    from scipy.stats import beta

    return float(beta.ppf(0.975, k + 1, n - k)) if n else np.nan


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--clean", nargs="+", required=True)
    ap.add_argument("--fail", nargs="+", required=True)
    ap.add_argument("--nulls", nargs="*", default=[])
    ap.add_argument("--no-resid", action="store_true", help="features without the residual diagnostics")
    ap.add_argument("--save", action="store_true")
    ap.add_argument("--tag", default="", help="suffix of the result file names")
    a = ap.parse_args()
    resid = not a.no_resid

    clean_all = load(a.clean, ("G", "S", "V"))
    clean = [r for r in clean_all if r.get("label") not in BAD]
    if resid:  # rows without resid would teach "missing resid = clean": keep only rows that have it
        dropped = sum(1 for r in clean if not r.get("resid"))
        clean = [r for r in clean if r.get("resid")]
    else:
        dropped = 0
    fail_all = load(a.fail, ("I",))
    n_bad = sum(r.get("label") in BAD for r in fail_all)
    fail = [r for r in fail_all if r.get("label") not in BAD]
    nulls = [r for r in load(a.nulls, ("N",)) if r.get("label") not in BAD and (r.get("resid") or not resid)]
    dz = lambda r: "scattered" if isinstance(r["design"][0], (int, float)) else "grid"  # as featurise  # noqa: E731
    dk = lambda r: (dz(r), float(r["design"][1]))  # design kind and noise level  # noqa: E731
    f_designs = {dk(r) for r in fail_all}
    n_other = sum(dk(r) not in f_designs for r in clean)
    # same design kind AND noise level as the injected rows: no design shortcut (G mixes 1 % and 5 % noise, I is 5 %)
    clean = [r for r in clean if dk(r) in f_designs]
    dropped = f"{dropped} without resid, {n_other} of a design the injected rows lack"
    designs = sorted({dz(r) for r in clean})
    print(f"clean {len(clean)} (dropped {dropped}; designs {designs}), fail {len(fail)} "
          f"(+{n_bad} timeout/crash), nulls {len(nulls)}")

    Xc = np.array([V.featurise(r, resid) for r in clean])
    Xf = np.array([V.featurise(r, resid) for r in fail])
    Xn = np.array([V.featurise(r, resid) for r in nulls]) if nulls else np.zeros((0, Xc.shape[1]))
    c_sp, f_sp = np.array([r["split"] for r in clean]), np.array([r["split"] for r in fail])
    c_fam, f_fam = np.array([r["family"] for r in clean]), np.array([r["family"] for r in fail])
    f_type, f_lvl = np.array([itype(r) for r in fail]), np.array([ilevel(r) for r in fail])
    types = sorted(set(f_type))

    def fit_arms(ci, fi, drop_type=None):
        fi = fi[f_type[fi] != drop_type] if drop_type else fi
        X = np.vstack([Xc[ci], Xf[fi]])
        y = np.r_[np.zeros(len(ci)), np.ones(len(fi))]
        ty = np.r_[[None] * len(ci), f_type[fi]].astype(object)
        return {n: Arm(n, resid).fit(Xc[ci], X, y, ty) for n in ARMS}

    results = {"split": {}, "lofo": {}, "loto": {}}

    # ---- split
    ci_fit, fi_fit = np.where(c_sp == "fit")[0], np.where(f_sp == "fit")[0]
    ci_cal, fi_cal = np.where(c_sp == "cal")[0], np.where(f_sp == "cal")[0]
    ci_te, fi_te = np.where(c_sp == "test")[0], np.where(f_sp == "test")[0]
    split_ok = all(len(v) for v in (ci_fit, fi_fit, ci_cal))  # rows of one split only: skip split and LOTO
    if not split_ok:
        print("split: no fit or cal rows; split and LOTO skipped")
    else:
        arms = fit_arms(ci_fit, fi_fit)
        arms["V1_hgb"].m.calibrate(Xc[ci_cal], Xf[fi_cal], f_type[fi_cal])
        det_split = {}
        for n, arm in arms.items():
            fa, det = evaluate(arm, Xc[ci_cal], Xc[ci_te], Xf[fi_te])
            fa_n, _ = evaluate(arm, Xc[ci_cal], Xn, Xn[:0]) if len(Xn) else (np.array([]), None)
            det_split[n] = det
            results["split"][n] = dict(
                fa=float(fa.mean()) if fa.size else np.nan, n_clean=int(fa.size), fa_hi=binom_hi(int(fa.sum()), fa.size),
                det=float(det.mean()) if det.size else np.nan, n_fail=int(det.size),
                fa_nulls=float(fa_n.mean()) if fa_n.size else np.nan,
                det_by_type={t: float(det[f_type[fi_te] == t].mean()) for t in types if (f_type[fi_te] == t).any()},
                det_by_level={int(lv): float(det[f_lvl[fi_te] == lv].mean()) for lv in range(3) if (f_lvl[fi_te] == lv).any()})
        if det_split["V1_hgb"].size:
            results["split"]["V1_hgb"]["vs_B0"] = boot_diff(det_split["V1_hgb"], det_split["B0_v0"])
            ty = arms["V1_hgb"].m.type_of(Xf[fi_te])
            results["split"]["V1_hgb"]["type_acc_flagged"] = float(np.mean(
                [t == k for t, k, d in zip(ty, f_type[fi_te], det_split["V1_hgb"]) if d] or [np.nan]))

    # ---- LOFO
    pooled, pooled_i = {n: [] for n in ARMS}, []
    v1_flag_clean, v1_flag_fail = {}, {}  # row index -> V1 flag in its held-out-family fold (downgrade effect)
    for fam in FAMILIES:
        ci = np.where((c_fam != fam) & (c_sp == "fit"))[0]
        fi = np.where((f_fam != fam) & (f_sp == "fit"))[0]
        cc, fc = np.where((c_fam != fam) & (c_sp == "cal"))[0], np.where((f_fam != fam) & (f_sp == "cal"))[0]
        ce, fe = np.where(c_fam == fam)[0], np.where(f_fam == fam)[0]
        if not len(ci) or not len(fi) or not len(ce) or not len(fe) or not len(cc):
            continue
        arms = fit_arms(ci, fi)
        arms["V1_hgb"].m.calibrate(Xc[cc], Xf[fc], f_type[fc])
        results["lofo"][fam] = {}
        pooled_i.append(fe)
        for n, arm in arms.items():
            fa, det = evaluate(arm, Xc[cc], Xc[ce], Xf[fe])
            pooled[n].append(det)
            if n == "V1_hgb":
                v1_flag_clean.update({int(i): bool(f) for i, f in zip(ce, fa)})
                v1_flag_fail.update({int(i): bool(f) for i, f in zip(fe, det)})
            results["lofo"][fam][n] = dict(fa=float(fa.mean()), n_clean=int(fa.size), fa_hi=binom_hi(int(fa.sum()), fa.size),
                                           det=float(det.mean()), n_fail=int(det.size),
                                           det_mid=float(det[f_lvl[fe] == 1].mean()) if (f_lvl[fe] == 1).any() else np.nan)
    if pooled["V1_hgb"]:
        results["lofo_pooled_vs_B0"] = boot_diff(np.concatenate(pooled["V1_hgb"]), np.concatenate(pooled["B0_v0"]))

    # ---- LOFO AUROC (alpha-free effect size). Train on every row of the other families, any split:
    # the held-out family is never seen. Conformal detection needs >= 1/alpha - 1 = 19 clean cal rows
    # per fold to flag anything; AUROC does not, so it is the feasibility read at small n.
    auc_folds = {}
    for fam in FAMILIES:
        ci, fi = np.where(c_fam != fam)[0], np.where(f_fam != fam)[0]
        ce, fe = np.where(c_fam == fam)[0], np.where(f_fam == fam)[0]
        if len(ci) < 3 or len(fi) < 3 or not len(ce) or not len(fe):
            continue
        arms = fit_arms(ci, fi)
        s = {}
        for n, arm in arms.items():  # non-finite scores mapped once over the pooled clean + injected scores
            v = _finite(np.r_[arm.score(Xc[ce]), arm.score(Xf[fe])])
            s[n] = (v[:len(ce)], v[len(ce):])
        # cluster = base draw (seed): the injected variants of one draw and its matched clean run move together
        draw = {d: i for i, d in enumerate(sorted({clean[i]["seed"] for i in ce} | {fail[i]["seed"] for i in fe}))}
        auc_folds[fam] = dict(nc=len(ce), nf=len(fe), types=f_type[fe], levels=f_lvl[fe], s=s,
                              gc=np.array([draw[clean[i]["seed"]] for i in ce]), gf=np.array([draw[fail[i]["seed"]] for i in fe]),
                              fcc=np.array([clean[i]["label"] == "FIT-COMPATIBLE" for i in ce]),
                              fcf=np.array([fail[i]["label"] == "FIT-COMPATIBLE" for i in fe]),
                              seed400=np.array([fail[i]["seed"] == 400 for i in fe]))
    results["lofo_auc"] = lofo_auc(auc_folds, types)

    # ---- CRASH / TIMEOUT rows: no output, so no arm can score them. Counted per type, and a second
    # detection line counts them as detected (the run failed visibly, not with a confident wrong label).
    bad = [r for r in fail_all if r.get("label") in BAD and r["family"] in results["lofo"]]
    fe_all = np.concatenate(pooled_i) if pooled_i else np.zeros(0, int)
    results["bad"] = {"clean": {lb: sum(r.get("label") == lb for r in clean_all) for lb in BAD}, "types": {}}
    for t in types + sorted({itype(r) for r in bad} - set(types)):
        nb = {lb: sum(itype(r) == t and r.get("label") == lb for r in bad) for lb in BAD}
        m = f_type[fe_all] == t
        e = dict(n_scored=int(m.sum()), **nb)
        for n in ARMS:
            d = np.concatenate(pooled[n])[m] if pooled[n] else np.zeros(0)
            k = d.size + sum(nb.values())
            e[n] = dict(det=float(d.mean()) if d.size else np.nan,
                        det_incl_bad=float((d.sum() + sum(nb.values())) / k) if k else np.nan)
        results["bad"]["types"][t] = e

    # ---- LOTO
    for t in types if split_ok else []:
        arms = fit_arms(ci_fit, fi_fit, drop_type=t)
        keep = fi_cal[f_type[fi_cal] != t]
        arms["V1_hgb"].m.calibrate(Xc[ci_cal], Xf[keep], f_type[keep])
        fe = np.where(f_type == t)[0]
        results["loto"][t] = {}
        for n, arm in arms.items():
            fa, det = evaluate(arm, Xc[ci_cal], Xc[ci_te], Xf[fe])
            results["loto"][t][n] = dict(det=float(det.mean()), fa=float(fa.mean()) if fa.size else np.nan)
        # open-set check on the runs V1 flags (a type is reported only for flagged runs)
        flagged = arms["V1_hgb"].m.flag(Xf[fe])
        ty = arms["V1_hgb"].m.type_of(Xf[fe][flagged]) if flagged.any() else []
        results["loto"][t]["V1_hgb"]["wrong_type"] = float(np.mean([k not in ("other", None) for k in ty])) if len(ty) else 0.0
        results["loto"][t]["V1_hgb"]["n_flagged"] = int(flagged.sum())

    # ---- target (b): run failure on clean data
    yb = np.array([r.get("category") not in ("right", "equivalent", "abstain-ok") for r in clean], int)
    results["target_b"] = target_b(Xc, yb, c_sp, c_fam)
    results["downgrade"] = downgrade_effect(clean, v1_flag_clean)
    results["downgrade_injected"] = downgrade_effect(fail, v1_flag_fail)

    gate = gate_v1(results, types)
    results["gate"] = gate
    OUT.mkdir(parents=True, exist_ok=True)
    tag = ("resid" if resid else "noresid") + (f"_{a.tag}" if a.tag else "")
    (OUT / f"v1_gate_{tag}.json").write_text(json.dumps(results, indent=1, default=float), encoding="utf-8")
    md = report_md(results, types, len(clean), len(fail), n_bad, dropped, tag)
    (OUT / f"v1_gate_{tag}.md").write_text(md, encoding="utf-8")
    print(md)

    if a.save and gate["passed"]:
        import joblib

        ci, fi = np.where(c_sp != "test")[0], np.where(f_sp != "test")[0]
        ci_c, fi_c = np.where(c_sp == "cal")[0], np.where(f_sp == "cal")[0]
        ci_f, fi_f = np.where(c_sp == "fit")[0], np.where(f_sp == "fit")[0]
        det = V.FailureDetector(alpha=ALPHA, resid=resid, designs=tuple(designs))
        det.fit(np.vstack([Xc[ci_f], Xf[fi_f]]), np.r_[np.zeros(len(ci_f)), np.ones(len(fi_f))],
                np.r_[[None] * len(ci_f), f_type[fi_f]].astype(object))
        det.calibrate(Xc[ci_c], Xf[fi_c], f_type[fi_c])
        d = ROOT / "code" / "pdefactor" / "learned" / "models"
        d.mkdir(exist_ok=True)
        joblib.dump(det, d / "v1.joblib")
        print("saved", d / "v1.joblib")


def downgrade_effect(clean, flags):
    """validator="downgrade" replayed on the held-out clean rows (LOFO folds): a flagged FIT-COMPATIBLE
    row becomes UNDECIDED (category recomputed by ll_corpus.category); counts before / after."""
    from ll_corpus import category

    cats = ("right", "equivalent", "false-confident", "abstain-ok", "abstain", "other")
    before, after = {c: 0 for c in cats}, {c: 0 for c in cats}
    moved = []
    for i, fl in flags.items():
        r = clean[i]
        c0 = r.get("category") or category(r)
        c1 = c0
        if fl and r.get("label") == "FIT-COMPATIBLE":
            c1 = category(dict(r, label="UNDECIDED", ok=False, equiv=False))
            moved.append((r["family"], r["seed"], c0, c1))
        before[c0] = before.get(c0, 0) + 1
        after[c1] = after.get(c1, 0) + 1
    rows = [dict(corpus=clean[i]["corpus"], family=clean[i]["family"], seed=clean[i]["seed"], design=clean[i]["design"],
                 label=clean[i].get("label"), category=clean[i].get("category"), flag=bool(fl)) for i, fl in flags.items()]
    return dict(n=len(flags), n_flagged=int(sum(flags.values())), before=before, after=after, moved=moved, rows=rows)


def target_b(X, y, sp, fam, alpha=0.10):
    from sklearn.ensemble import HistGradientBoostingClassifier

    def run(tr, cal, te):
        if not len(tr) or not len(te) or y[tr].min() == y[tr].max() or not y[cal].any():
            return None
        fin = np.isfinite(X[tr])
        lo, hi = np.where(fin, X[tr], np.inf).min(0), np.where(fin, X[tr], -np.inf).max(0)
        cols = np.where(fin.any(0) & (hi > lo))[0]  # all-NaN / constant columns break the binning
        m = HistGradientBoostingClassifier(max_iter=200, max_depth=3, learning_rate=0.05, min_samples_leaf=10,
                                           random_state=0).fit(X[tr][:, cols], y[tr])
        s_cal = m.predict_proba(X[cal][:, cols])[:, 1]
        pos = np.sort(s_cal[y[cal] == 1])
        n = len(pos)
        # risk control for the missed rate: threshold = the largest lam with (#pos below lam + 1)/(n+1) <= alpha
        k = int(np.floor(alpha * (n + 1) - 1))
        lam = pos[k] if k >= 0 else -np.inf
        s = m.predict_proba(X[te][:, cols])[:, 1]
        fl = s >= lam
        yt = y[te]
        return dict(missed=float(np.mean(~fl[yt == 1])) if (yt == 1).any() else np.nan,
                    false_flag=float(np.mean(fl[yt == 0])) if (yt == 0).any() else np.nan,
                    n_pos=int((yt == 1).sum()), n_neg=int((yt == 0).sum()))

    out = {"split": run(np.where(sp == "fit")[0], np.where(sp == "cal")[0], np.where(sp == "test")[0]), "lofo": {}}
    for f in FAMILIES:
        r = run(np.where((fam != f) & (sp == "fit"))[0], np.where((fam != f) & (sp == "cal"))[0], np.where(fam == f)[0])
        if r:
            out["lofo"][f] = r
    return out


def gate_v1(R, types):
    s = R["split"]
    if not s:  # fails closed: no split, no gate
        return dict(passed=False, ships_wrong_set_flag=False, reason="no fit/cal split rows")
    g = {}
    ci = s["V1_hgb"].get("vs_B0", (np.nan, np.nan, np.nan))
    best_base = max(s[n]["det"] for n in ARMS[1:-1])
    g["primary_split"] = bool(ci[1] > 0 and s["V1_hgb"]["det"] >= best_base)
    lp = R.get("lofo_pooled_vs_B0", (np.nan, np.nan, np.nan))
    g["primary_lofo"] = bool(lp[1] > 0 and all(R["lofo"][f]["V1_hgb"]["det"] >= R["lofo"][f]["B0_v0"]["det"]
                                                for f in R["lofo"]))
    g["fa_split"] = bool(s["V1_hgb"]["fa"] <= ALPHA or s["V1_hgb"]["fa_hi"] >= ALPHA)  # within binomial MC error
    g["fa_lofo"] = all(R["lofo"][f]["V1_hgb"]["fa"] <= ALPHA or R["lofo"][f]["V1_hgb"]["fa_hi"] >= ALPHA
                       for f in R["lofo"])
    g["loto"] = all(R["loto"][t]["V1_hgb"]["wrong_type"] <= 0.10
                    and R["loto"][t]["V1_hgb"]["det"] >= R["loto"][t]["B0_v0"]["det"] for t in types)
    mid = s["V1_hgb"]["det_by_level"].get(1, np.nan)
    g["useful_mid_level"] = bool(mid >= 0.5)
    tb = R["target_b"]
    g["target_b"] = bool(tb["split"] and all(v["missed"] <= 0.12 and v["false_flag"] <= 0.10
                                             for v in [tb["split"], *tb["lofo"].values()] if v))
    g["passed"] = all(g[k] for k in ("primary_split", "primary_lofo", "fa_split", "fa_lofo", "loto", "useful_mid_level"))
    g["ships_wrong_set_flag"] = g["passed"] and g["target_b"]
    return g


def report_md(R, types, n_c, n_f, n_bad, dropped, tag):
    s = R["split"]
    L = [f"# V1 gate ({tag}; clean {n_c} rows, dropped {dropped}; I {n_f} rows, {n_bad} timeout/crash)",
         "", "## Split (fit / cal / test); alpha = 0.05", "",
         "| arm | false alarm G/S test [95 % hi] | false alarm N | detection I test | " +
         " | ".join(types) + " | level 0 / 1 / 2 |", "|---" * (5 + len(types)) + "|"]
    for n in ARMS if s else []:
        r = s[n]
        L.append(f"| {n} | {r['fa']:.3f} [{r['fa_hi']:.3f}] (n={r['n_clean']}) | {r['fa_nulls']:.3f} | "
                 f"{r['det']:.3f} (n={r['n_fail']}) | " + " | ".join(f"{r['det_by_type'].get(t, np.nan):.2f}" for t in types) +
                 " | " + " / ".join(f"{r['det_by_level'].get(lv, np.nan):.2f}" for lv in range(3)) + " |")
    if s and "vs_B0" in s["V1_hgb"]:
        d = s["V1_hgb"]["vs_B0"]
        L += ["", f"V1 − B0 detection (paired bootstrap): {d[0]:+.3f} [{d[1]:+.3f}, {d[2]:+.3f}]; "
                  f"type accuracy on flagged test runs {s['V1_hgb'].get('type_acc_flagged', np.nan):.2f}"]
    L += ["", "## LOFO (held-out family: all its rows)", "", "| family | " + " | ".join(f"{n} FA / det" for n in ARMS) + " |",
          "|---" * (1 + len(ARMS)) + "|"]
    for f, rr in R["lofo"].items():
        L.append(f"| {f} | " + " | ".join(f"{rr[n]['fa']:.2f} / {rr[n]['det']:.2f}" for n in ARMS) + " |")
    if "lofo_pooled_vs_B0" in R:
        d = R["lofo_pooled_vs_B0"]
        L += ["", f"LOFO pooled V1 − B0 detection: {d[0]:+.3f} [{d[1]:+.3f}, {d[2]:+.3f}]"]
    L += ["", "## LOTO (held-out injection type)", "", "| type | " + " | ".join(f"{n} det" for n in ARMS) +
          " | V1 wrong-type rate |", "|---" * (2 + len(ARMS)) + "|"]
    for t, rr in R["loto"].items():
        L.append(f"| {t} | " + " | ".join(f"{rr[n]['det']:.2f}" for n in ARMS) + f" | {rr['V1_hgb']['wrong_type']:.2f} |")
    A = R.get("lofo_auc") or {}
    if A:
        L += ["", f"## LOFO AUROC, injected vs clean (alpha-free; {A['n_folds']} held-out families; mean of per-family AUROC;"
              " CI: paired cluster bootstrap over base draws)"]
        for key, title in (("arms", "all scored runs"),
                           ("arms_fc", f"FIT-COMPATIBLE runs only (clean {A['n_fc'][0]}, injected {A['n_fc'][1]})")):
            L += ["", f"{title}:", "", "| arm | AUROC [95 % CI] | − B0 [95 % CI] | " + " | ".join(A[key]["B0_v0"]["by_fold"]) + " |",
                  "|---" * (3 + len(A[key]["B0_v0"]["by_fold"])) + "|"]
            for n in ARMS:
                a = A[key][n]
                L.append(f"| {n} | {a['auc']:.3f} [{a['ci'][0]:.3f}, {a['ci'][1]:.3f}] | {a['vs_B0'][0]:+.3f} "
                         f"[{a['vs_B0'][1]:+.3f}, {a['vs_B0'][2]:+.3f}] | " + " | ".join(f"{v:.2f}" for v in a["by_fold"].values()) + " |")
        L += ["", "| type | " + " | ".join(ARMS) + " |", "|---" * (1 + len(ARMS)) + "|"]
        for t, e in [*A["types"].items(), *((f"level {lv}", e) for lv, e in A["levels"].items()),
                     *((f"injected {g}", e) for g, e in A["seeds"].items())]:
            L.append(f"| {t} | " + " | ".join(f"{e[n]:.2f}" for n in ARMS) + " |")
    B = R.get("bad", {})
    if B.get("types"):
        L += ["", "## CRASH / TIMEOUT injected runs (LOFO pooled; no output, so no arm scores them)", "",
              "| type | scored | crash | timeout | " + " | ".join(f"{n} det / incl. bad" for n in ARMS) + " |",
              "|---" * (4 + len(ARMS)) + "|"]
        for t, e in B["types"].items():
            L.append(f"| {t} | {e['n_scored']} | {e['CRASH']} | {e['TIMEOUT']} | " +
                     " | ".join(f"{e[n]['det']:.2f} / {e[n]['det_incl_bad']:.2f}" for n in ARMS) + " |")
        L += ["", f"clean G/S rows: {B['clean']['CRASH']} crash, {B['clean']['TIMEOUT']} timeout (not right; excluded from FA)"]
    tb = R["target_b"]
    L += ["", "## Target (b): run failure on clean data (missed / false flag; risk control alpha = 0.10)", ""]
    if tb["split"]:
        L.append(f"- split: missed {tb['split']['missed']:.2f}, false flag {tb['split']['false_flag']:.2f} "
                 f"(pos {tb['split']['n_pos']}, neg {tb['split']['n_neg']})")
    for f, v in tb["lofo"].items():
        L.append(f"- LOFO {f}: missed {v['missed']:.2f}, false flag {v['false_flag']:.2f} (pos {v['n_pos']}, neg {v['n_neg']})")
    for key, what in (("downgrade", "held-out clean rows"), ("downgrade_injected", "held-out injected rows")):
        D = R.get(key)
        if not D:
            continue
        L += ["", f"## V1 downgrade replay ({what}, LOFO; {D['n']} rows, {D['n_flagged']} flagged)", "",
              "| category | off | downgrade |", "|---|---|---|"]
        L += [f"| {c} | {D['before'][c]} | {D['after'][c]} |" for c in D["before"]]
        L += ["", "moved: " + "; ".join(f"{f} {s}: {a} -> {b}" for f, s, a, b in D["moved"])]
    L += ["", "## Gate", "", *[f"- {k}: {v}" for k, v in R["gate"].items()], ""]
    return "\n".join(L)


if __name__ == "__main__":
    main()
