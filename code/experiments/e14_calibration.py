"""E14 (S-PHASE4-ML): L2b, L2c and V1 fitted on the E13 corpus, tested on held-out families.

Train families: the v1 CASES. Test families: the GENERAL_CASES (plan v2.13: shapes the v1 cases do
not cover, never used to tune the pipeline). This is the PHASE4 §9 leave-family-out protocol at the
level the current simulator allows (P0.3's random families will replace it). Inside the train
families, fit and calibrate are split by family (grouped), so the conformal step never sees a
family the monotone map was fitted on.

Reported, each off vs on:
- L2b: ECE and Brier of P(top) as a probability of the right factor set; isotonic map from train.
- L2c: coverage of the nominal 90 % coefficient intervals (z <= 1), raw vs inflated.
- V1:  "wrong factor set" flag with conformal risk control (missed-wrong rate <= alpha in-prior),
       its realised missed rate and flag rate on the test families, and the OOD share.

Usage:  python code/experiments/e14_calibration.py   (reads code/experiments/out/e13_corpus.jsonl)
"""
from __future__ import annotations

import json
import os

import numpy as np

from pdefactor.learned import PRIOR_TAG
from pdefactor.learned.calibrate import (IntervalInflator, ProbabilityCalibrator, VennAbersCalibrator,
                                         reliability, split_indices)
from pdefactor.learned.validator import Validator
from pdefactor.synthetic import CASES

HERE = os.path.dirname(os.path.abspath(__file__))
IN = os.path.join(HERE, "out", "e13_corpus.jsonl")
OUT = os.path.join(HERE, "out", "e14_calibration.md")


def load():
    rows = [json.loads(l) for l in open(IN) if l.strip()]
    return [r for r in rows if "error" not in r]


def brier(p, y):
    return float(np.mean((np.asarray(p) - np.asarray(y, float)) ** 2))


def main():
    rows = load()
    train = [r for r in rows if r["family"] in CASES]
    test = [r for r in rows if r["family"] not in CASES]
    if len(train) < 10 or not test:
        print(f"corpus not ready: {len(train)} train, {len(test)} test runs")
        return
    lines = [f"# E14 — learned calibration on held-out families ({PRIOR_TAG})", "",
             f"Corpus: {len(rows)} runs ({len(train)} train on v1 CASES, {len(test)} test on GENERAL_CASES). "
             "Grid data, stand-in posterior (fake_posterior, S = 4), noise 0.1 / 1 / 5 %.", ""]

    # ---------------- L2b: P(top) -> P(right set)
    p_tr = np.array([r["features"]["p_top"] for r in train])
    y_tr = np.array([r["correct"] for r in train], float)
    p_te = np.array([r["features"]["p_top"] for r in test])
    y_te = np.array([r["correct"] for r in test], float)
    cal = ProbabilityCalibrator().fit(p_tr, y_tr)
    va = VennAbersCalibrator().fit(p_tr, y_tr)
    e_off, e_on, e_va = (reliability(p_te, y_te)[1], reliability(cal(p_te), y_te)[1],
                         reliability(va(p_te), y_te)[1])
    lines += ["## L2b — P(top structure) as P(right factor set)", "",
              f"right-set rate: train {y_tr.mean():.2f}, test {y_te.mean():.2f}", "",
              "| | ECE test | Brier test |", "|---|---|---|",
              f"| off (raw P(top)) | {e_off:.3f} | {brier(p_te, y_te):.3f} |",
              f"| on (isotonic, fitted on train families) | {e_on:.3f} | {brier(cal(p_te), y_te):.3f} |",
              f"| on (inductive Venn-Abers) | {e_va:.3f} | {brier(va(p_te), y_te):.3f} |", ""]

    # ---------------- L2c: coefficient interval inflation
    def coef_table(rs):
        feats, z, fam = [], [], []
        for r in rs:
            for c in r["coef"]:
                if np.isfinite(c["z"]):
                    feats.append(c)
                    z.append(c["z"])
                    fam.append(r["family"])
        names = IntervalInflator().names
        X = {k: np.array([f[k] for f in feats], float) for k in names}
        return X, np.array(z), np.array(fam)

    Xtr, ztr, ftr = coef_table(train)
    Xte, zte, _ = coef_table(test)
    if len(ztr) > 40 and len(zte):
        a, b, _ = split_indices(len(ztr), fracs=(0.6, 0.4, 0.0), groups=ftr, rng=0) if len(set(ftr)) >= 3 else (None, None, None)
        sub = lambda X, i: {k: v[i] for k, v in X.items()}
        inf = IntervalInflator(regime_feature="mode_margin", regime_edges=(0.5,))
        inf.fit(sub(Xtr, a), ztr[a]).calibrate(sub(Xtr, b), ztr[b])
        fac = inf(Xte)
        lines += ["## L2c — coverage of nominal 90 % coefficient intervals (z <= 1)", "",
                  "| | train (fit+cal) | test families |", "|---|---|---|",
                  f"| off | {np.mean(ztr <= 1):.3f} | {np.mean(zte <= 1):.3f} |",
                  f"| on | {np.mean(ztr <= inf(Xtr)):.3f} | {np.mean(zte <= fac):.3f} |",
                  f"| median width factor (test) | | {np.median(fac):.2f} |", "",
                  f"coefficients: {len(ztr)} train, {len(zte)} test. The kappa_vand, log_snr and disagreement "
                  "features are NaN until the deterministic layer exports them.", ""]

    # ---------------- V1: flag a wrong factor set
    keys = sorted({k for r in rows for k in r["features"]})
    M = lambda rs: np.array([[r["features"].get(k, np.nan) for k in keys] for r in rs], float)
    Ytr = (1 - y_tr)[:, None].astype(int)
    Yte = (1 - y_te)[:, None].astype(int)
    fam_tr = np.array([r["family"] for r in train])
    a, b, _ = split_indices(len(train), fracs=(0.6, 0.4, 0.0), groups=fam_tr, rng=1)
    v = Validator(modes=("wrong_set",), alpha=0.1)
    if Ytr[a].min() != Ytr[a].max():
        v.fit(M(train)[a], Ytr[a]).calibrate(M(train)[b], Ytr[b])
        out = v.predict(M(test))
        ood = np.array([o["ood"] for o in out])
        flag = np.array([bool(o["set"]) for o in out if not o["ood"]])
        wrong = Yte[~ood, 0] == 1
        miss = float(np.mean(~flag[wrong])) if wrong.any() else float("nan")
        lines += ["## V1 — 'wrong factor set' flag (risk control alpha = 0.1, in-prior)", "",
                  f"test runs: {len(test)}; OOD (probabilities withheld): {ood.mean():.2f}; "
                  f"in-range wrong sets missed: {miss:.2f}; in-range flag rate: {flag.mean() if flag.size else float('nan'):.2f}", ""]
    else:
        lines += ["## V1", "", "no wrong factor sets in the fit split: nothing to learn (all runs right).", ""]

    # ---------------- LOFO over all families (PHASE4 §9): L2b and V1 need failures in training
    fams = sorted({r["family"] for r in rows})
    P_off, P_iso, P_va, Ylofo, flags, oods = [], [], [], [], [], []
    Mall = M(rows)
    yall = np.array([r["correct"] for r in rows], float)
    pall = np.array([r["features"]["p_top"] for r in rows])
    famall = np.array([r["family"] for r in rows])
    for fam in fams:
        te = famall == fam
        tr_idx = np.where(~te)[0]
        P_off += list(pall[te])
        P_iso += list(ProbabilityCalibrator().fit(pall[tr_idx], yall[tr_idx])(pall[te]))
        P_va += list(VennAbersCalibrator().fit(pall[tr_idx], yall[tr_idx])(pall[te]))
        Ylofo += list(yall[te])
        a2, b2, _ = split_indices(len(tr_idx), fracs=(0.6, 0.4, 0.0), groups=famall[tr_idx], rng=2)
        fi, ci = tr_idx[a2], tr_idx[b2]
        Yw = (1 - yall)[:, None].astype(int)
        if Yw[fi].min() == Yw[fi].max():
            flags += [None] * int(te.sum())
            oods += [False] * int(te.sum())
            continue
        vv = Validator(modes=("wrong_set",), alpha=0.1).fit(Mall[fi], Yw[fi]).calibrate(Mall[ci], Yw[ci])
        for o in vv.predict(Mall[te]):
            oods.append(o["ood"])
            flags.append(None if o["ood"] else bool(o["set"]))
    Ylofo = np.array(Ylofo)
    lines += ["## LOFO over all 21 families (each family held out once; fit/calibrate grouped by family)", "",
              f"runs {len(Ylofo)}, right-set rate {Ylofo.mean():.2f}", "",
              "| L2b map | ECE | Brier |", "|---|---|---|"]
    for nm, P in (("off (raw P(top))", P_off), ("isotonic", P_iso), ("inductive Venn-Abers", P_va)):
        lines.append(f"| {nm} | {reliability(P, Ylofo)[1]:.3f} | {brier(P, Ylofo):.3f} |")
    fl = np.array([f for f in flags if f is not None], bool)
    wr = np.array([1 - y for y, f in zip(Ylofo, flags) if f is not None], bool)
    if fl.size:
        lines += ["", f"V1 'wrong factor set' flag: OOD (withheld) {np.mean(oods):.2f}; in range: "
                  f"wrong sets caught {fl[wr].mean() if wr.any() else float('nan'):.2f} "
                  f"({int(wr.sum())} wrong), false-flag rate on right sets {fl[~wr].mean():.2f}", ""]
    lines += ["Labels are never changed by these layers; the numbers above are prior-dependent "
              f"({PRIOR_TAG}).", ""]
    with open(OUT, "w") as fh:
        fh.write("\n".join(lines))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
