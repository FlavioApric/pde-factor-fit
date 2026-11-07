"""L2b gate: calibrated P(top) vs the raw P(top) (sessions/LEARNED/V1/PLAN.md sec. 4).

Report-only layer: labels are unchanged by construction (tests/test_learned_v1.py), so the gate is
computed offline on the off-arm corpus rows. y = the top structure is the right factor set
(category "right"; --equiv also counts "equivalent").

Protocols:
- LOFO: fit on every row of four families, evaluate on every row of the fifth;
- split: fit on fit + cal, evaluate on test.
Gate (LEARNED PLAN 3.6): an arm passes if on every LOFO fold Brier and ECE are <= raw, and the
pooled LOFO Brier difference (arm - raw) has a 95 % paired bootstrap CI below 0. Among passing arms
the one with the fewest parameters ships.

  python ll_ptop.py <rows.jsonl> ... [--equiv] [--save]
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from pdefactor.learned.ptop import METHODS, PTopCalibrator, brier, ece_adaptive, feature_matrix, log_loss  # noqa: E402

FAMILIES = ("F1", "F2", "F3", "F4", "F5")
OUT = ROOT / "sessions" / "LEARNED" / "V1" / "results"


def load(paths):
    """Off-arm G/S rows with a P(top); CRASH / TIMEOUT rows are returned apart (no P(top) to calibrate)."""
    rows, bad = [], []
    for p in paths:
        for line in open(p):
            r = json.loads(line)
            if r.get("learned", "off") != "off" or r.get("corpus") not in ("G", "S"):
                continue
            if r.get("label") in ("TIMEOUT", "CRASH"):
                bad.append(r)
                continue
            if r.get("p_top") is None:
                continue
            rows.append(r)
    return rows, bad


def target(rows, equiv):
    ok = ("right", "equivalent") if equiv else ("right",)
    return np.array([r.get("category") in ok for r in rows], float)


def fit_eval(method, tr, te, y_tr):
    p_tr = np.array([r["p_top"] for r in tr])
    p_te = np.array([r["p_top"] for r in te])
    X_tr = feature_matrix(tr) if method == "logit-features" else None
    X_te = feature_matrix(te) if method == "logit-features" else None
    c = PTopCalibrator(method).fit(p_tr, y_tr, X_tr)
    return np.clip(np.asarray(c(p_te, X_te), float), 0, 1)


def boot_ci(d, B=2000, seed=0):
    rng = np.random.default_rng(seed)
    d = np.asarray(d, float)
    m = np.array([d[rng.integers(0, len(d), len(d))].mean() for _ in range(B)])
    return float(d.mean()), float(np.quantile(m, 0.025)), float(np.quantile(m, 0.975))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--equiv", action="store_true")
    ap.add_argument("--save", action="store_true", help="fit the shipped arm on all rows -> learned/models/ptop.joblib")
    a = ap.parse_args()
    rows, bad = load(a.files)
    y = target(rows, a.equiv)
    fam = np.array([r["family"] for r in rows])
    print(f"{len(rows)} rows, right rate {y.mean():.3f}, families {dict(zip(*np.unique(fam, return_counts=True)))}")

    res = {m: {"folds": {}, "pooled": None} for m in METHODS}
    pooled_p = {m: np.full(len(rows), np.nan) for m in METHODS}
    for f in FAMILIES:
        te = np.where(fam == f)[0]
        tr = np.where(fam != f)[0]
        if not len(te) or not len(tr) or y[tr].min() == y[tr].max():
            continue
        for m in METHODS:
            q = fit_eval(m, [rows[i] for i in tr], [rows[i] for i in te], y[tr])
            pooled_p[m][te] = q
            res[m]["folds"][f] = dict(n=int(len(te)), brier=brier(q, y[te]), ece=ece_adaptive(q, y[te]),
                                      logloss=log_loss(q, y[te]))
    have = np.isfinite(pooled_p["raw"])
    sq_raw = (pooled_p["raw"][have] - y[have]) ** 2
    for m in METHODS:
        sq = (pooled_p[m][have] - y[have]) ** 2
        res[m]["pooled"] = dict(brier=float(sq.mean()), ece=ece_adaptive(pooled_p[m][have], y[have]),
                                d_brier=boot_ci(sq - sq_raw))
    # fixed split
    sp = np.array([r["split"] for r in rows])
    tr, te = np.where(sp != "test")[0], np.where(sp == "test")[0]
    for m in METHODS:
        if len(te) and len(tr):
            q = fit_eval(m, [rows[i] for i in tr], [rows[i] for i in te], y[tr])
            res[m]["split"] = dict(n=int(len(te)), brier=brier(q, y[te]), ece=ece_adaptive(q, y[te]))

    raw = res["raw"]
    passing = []
    for m in METHODS[1:]:
        folds_ok = all(res[m]["folds"][f]["brier"] <= raw["folds"][f]["brier"]
                       and res[m]["folds"][f]["ece"] <= raw["folds"][f]["ece"] for f in raw["folds"])
        ci_ok = res[m]["pooled"]["d_brier"][2] < 0
        res[m]["gate"] = dict(every_fold=folds_ok, ci_below_0=ci_ok, passed=folds_ok and ci_ok)
        if folds_ok and ci_ok:
            passing.append(m)
    ship = passing[0] if passing else None  # METHODS is ordered by number of parameters

    OUT.mkdir(parents=True, exist_ok=True)
    tag = "equiv" if a.equiv else "right"
    (OUT / f"ptop_gate_{tag}.json").write_text(json.dumps(dict(n=len(rows), n_bad=len(bad), ship=ship, res=res), indent=1), encoding="utf-8")
    lines = [f"# L2b gate (y = {tag}; {len(rows)} rows G+S off arm; LOFO by family)", "",
             "| arm | " + " | ".join(f"{f} Brier / ECE" for f in raw["folds"]) +
             " | pooled Brier | pooled ECE | ΔBrier vs raw [95 % CI] | split Brier / ECE | gate |",
             "|---" * (len(raw["folds"]) + 6) + "|"]
    for m in METHODS:
        r = res[m]
        d = r["pooled"]["d_brier"]
        s = r.get("split", {})
        lines.append(f"| {m} | " + " | ".join(f"{r['folds'][f]['brier']:.3f} / {r['folds'][f]['ece']:.3f}"
                                             for f in raw["folds"]) +
                     f" | {r['pooled']['brier']:.4f} | {r['pooled']['ece']:.3f} | {d[0]:+.4f} [{d[1]:+.4f}, {d[2]:+.4f}]"
                     f" | {s.get('brier', np.nan):.3f} / {s.get('ece', np.nan):.3f} | "
                     f"{'—' if m == 'raw' else ('PASS' if r['gate']['passed'] else 'fail')} |")
    nb = {f: {lb: sum(r["family"] == f and r["label"] == lb for r in bad) for lb in ("CRASH", "TIMEOUT")} for f in FAMILIES}
    lines += ["", "CRASH / TIMEOUT rows (no P(top), not calibrated): " +
              ", ".join(f"{f} {v['CRASH']}/{v['TIMEOUT']}" for f, v in nb.items()) + " (crash/timeout)",
              f"right rate: {y.mean():.3f} on {len(rows)} scored rows; {y.sum() / max(len(rows) + len(bad), 1):.3f} "
              f"counting the {len(bad)} CRASH / TIMEOUT rows as not-right"]
    lines += ["", f"shipped arm: {ship or 'none (L2b stays off)'}"]
    (OUT / f"ptop_gate_{tag}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))

    if a.save and ship:
        import joblib

        X = feature_matrix(rows) if ship == "logit-features" else None
        c = PTopCalibrator(ship).fit(np.array([r["p_top"] for r in rows]), y, X)
        d = ROOT / "src" / "pdefactor" / "learned" / "models"
        d.mkdir(exist_ok=True)
        joblib.dump(c, d / "ptop.joblib")
        print("saved", d / "ptop.joblib")


if __name__ == "__main__":
    main()
