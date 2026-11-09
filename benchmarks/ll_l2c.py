"""S-LEARNED B3: fit and evaluate L2c (coefficient interval calibration), PLAN.md section 3.1.

Data: the off arm of corpora G and S (ll_corpus.py), coefficients of correctly selected factors.
Cell = one real or imaginary part of one true coefficient whose monomial the reported factor holds:
  z = |true - median| / half-width of the reported 90 % interval.
Models:
  gbm     calibrate.IntervalInflator on the per-factor exports (monotone signs below), Mondrian
          conformal over 3 regimes of the mode margin; scale clipped to [0.5, 5]
  scalar  one split-conformal factor (the competitor that must be beaten)
Evaluation: test split and leave-one-family-out (fit + calibrate on four families, test on the fifth).
Writes the chosen model to code/pdefactor/learned/models/l2c.pkl and a markdown table to stdout.

Usage: python ll_l2c.py analysis/exp/out/ll_G_off.jsonl analysis/exp/out/ll_S_off.jsonl
"""
from __future__ import annotations

import json
import pickle
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))

from pdefactor.learned import PRIOR_TAG  # noqa: E402
from pdefactor.learned.apply import MODELS, ScaleModel  # noqa: E402
from pdefactor.learned.calibrate import IntervalInflator, conformal_quantile  # noqa: E402

NAMES = ("mode_margin", "log_snr", "kappa_vand", "disagreement", "rel_width", "log_nobs")
SIGNS = {"mode_margin": -1, "log_snr": -1, "kappa_vand": +1, "disagreement": +1, "rel_width": +1, "log_nobs": -1}
ALPHA = 0.10
CLIP = (0.5, 5.0)
EDGES = (0.5, 2.5)  # mode margin regimes: < 1 (at the identifiability edge), 1-2, >= 3


def cells(paths):
    out = []
    for p in paths:
        for line in Path(p).read_text().splitlines():
            r = json.loads(line)
            if r.get("learned") != "off" or r.get("category") != "right" or not r.get("export"):
                continue
            for c in r.get("coef", []):
                j = c["rep_j"]
                if j >= len(r["export"]):
                    continue
                f = r["export"][j]
                for i in (0, 1):
                    v, med, lo, hi = c["true"][i], c["mean"][i], c["lo"][i], c["hi"][i]
                    hw = (hi - lo) / 2
                    if hw <= 0:  # leading coefficient, an absent monomial, or a part fixed at 0
                        continue
                    out.append(dict(family=r["family"], split=r["split"], corpus=r["corpus"],
                                    z=abs(v - med) / hw, hw=hw, err=abs(v - med), scale=max(abs(v), 1e-3),
                                    **{k: f.get(k, np.nan) for k in NAMES}))
    return out


def X(rows):
    return {k: np.array([r[k] for r in rows], float) for k in NAMES}


def fit_gbm(fit, cal):
    inf = IntervalInflator(names=NAMES, alpha=ALPHA, regime_feature="mode_margin", regime_edges=EDGES,
                           tag=PRIOR_TAG, signs=SIGNS)
    inf.fit(X(fit), [r["z"] for r in fit]).calibrate(X(cal), [r["z"] for r in cal])
    return ScaleModel("gbm", inflator=inf, names=NAMES, clip=CLIP, tag=PRIOR_TAG)


def fit_scalar(cal):
    q = conformal_quantile([r["z"] for r in cal], ALPHA)
    return ScaleModel("scalar", q=q, clip=CLIP, tag=PRIOR_TAG)


def evaluate(model, rows):
    """coverage, median relative interval score, mean scale over the cells of rows."""
    if not rows:
        return np.nan, np.nan, np.nan
    s = np.ones(len(rows)) if model is None else model.scales([{k: r[k] for k in NAMES} for r in rows])
    z = np.array([r["z"] for r in rows])
    hw = np.array([r["hw"] for r in rows]) * s
    err = np.array([r["err"] for r in rows])
    isc = (2 * hw + (2 / ALPHA) * np.maximum(err - hw, 0)) / np.array([r["scale"] for r in rows])
    return float(np.mean(z <= s)), float(np.median(isc)), float(np.mean(s))


def main(paths):
    rows = cells(paths)
    fams = sorted({r["family"] for r in rows})
    by = lambda sp_: [r for r in rows if r["split"] == sp_]  # noqa: E731
    fit, cal, test = by("fit"), by("cal"), by("test")
    print(f"# L2c (coefficient intervals): {len(rows)} cells ({len(fit)} fit / {len(cal)} cal / {len(test)} test)\n")
    gbm, sca = fit_gbm(fit, cal), fit_scalar(cal)
    print("| evaluation | model | n | coverage | median interval score | mean scale |\n|---|---|---|---|---|---|")
    res = {}
    for name, m in (("off", None), ("scalar", sca), ("gbm", gbm)):
        c, i, s = evaluate(m, test)
        res[name] = (c, i)
        print(f"| test split | {name} | {len(test)} | {c:.3f} | {i:.4f} | {s:.2f} |")
    lofo = {"off": [], "scalar": [], "gbm": []}
    for f in fams:
        tr = [r for r in rows if r["family"] != f]
        te = [r for r in rows if r["family"] == f]
        trf = [r for r in tr if r["split"] == "fit"]
        trc = [r for r in tr if r["split"] != "fit"]
        for name, m in (("off", None), ("scalar", fit_scalar(trc)), ("gbm", fit_gbm(trf, trc))):
            c, i, s = evaluate(m, te)
            lofo[name].append((c, i))
            print(f"| LOFO {f} | {name} | {len(te)} | {c:.3f} | {i:.4f} | {s:.2f} |")
    print()
    ok = {}
    for name in ("scalar", "gbm"):
        covs = [c for c, _ in lofo[name]] + [res[name][0]]
        in_band = all(0.85 <= c <= 0.95 for c in covs)
        is_ok = res[name][1] <= res["off"][1] and np.mean([i for _, i in lofo[name]]) <= np.mean([i for _, i in lofo["off"]])
        ok[name] = in_band and is_ok
        print(f"- {name}: coverage in [0.85, 0.95] on test and every LOFO fold: {in_band}; "
              f"interval score <= off: {is_ok}")
    pick = None
    if ok["gbm"] and res["gbm"][1] <= res["scalar"][1] and \
            np.mean([i for _, i in lofo["gbm"]]) <= np.mean([i for _, i in lofo["scalar"]]):
        pick = gbm
    elif ok["scalar"]:
        pick = sca
    print(f"\n**chosen: {pick.kind if pick else 'none (layer stays off)'}**"
          + (f" (scalar q = {sca.q:.3f})" if pick is sca else ""))
    if pick is not None:
        MODELS.mkdir(exist_ok=True)
        (MODELS / "l2c.pkl").write_bytes(pickle.dumps(pick))
    return pick


if __name__ == "__main__":
    main(sys.argv[1:])
