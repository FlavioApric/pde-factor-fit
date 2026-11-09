"""Train the controller policies from the randomised remedy logs (sessions/LEARNED/C/PLAN.md §6).

Inputs: ll_C_logs.py rows (step 0 = off run, step >= 1 = one remedy from the off state, or a random
sequence). Per logged remedy row, from the state before it:
  success = the answer became right/equivalent and the off answer was not;
  harm    = the answer became false-confident and the previous one was not (G off-right rows, N rows).
C1 (table): RemedyTable over (diagnosis, remedy, success, cost).
C2 (contextual): per remedy, logistic (L2) on the dimensionless state features, isotonic calibration
on the cal split; minus the remedy's harm rate (Beta(1,1) mean); cost = ridge on runtime / off runtime.
Banned: a remedy whose N rows ever turn an abstention false-confident (kept removed for the gate).
lambda: knee on the cal split by replay of the one-step logs (largest lambda keeping >= 90 % of the
best replayed success). OPE: IPS and doubly robust value on the uniformly random rows only.
LOFO: one model per held-out family, trained without that family's rows.

  python analysis/exp/ll_C_train.py --logs analysis/exp/out/ll_C_logs_G.jsonl analysis/exp/out/ll_C_logs_N.jsonl
"""
from __future__ import annotations

import argparse
import json
import pickle
import sys
from collections import defaultdict
from pathlib import Path
from types import SimpleNamespace

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ll_corpus as LC  # noqa: E402

from pdefactor.learned import controller as C  # noqa: E402
from pdefactor.learned.remedy import RemedyTable  # noqa: E402
from pdefactor.learned.runconfig import DEFAULT  # noqa: E402

RIGHT = ("right", "equivalent")
MODELS = LC.ROOT / "code" / "pdefactor" / "learned" / "models"
LAMS = (0.0, 0.02, 0.05, 0.1, 0.2, 0.5)
MIN_ROWS = 8


def ckey(r):
    return (r["corpus"], r["family"], r["seed"], tuple(r["design"]))


def load(paths):
    off, acts = {}, []
    for p in paths:
        for line in Path(p).read_text().splitlines():
            r = json.loads(line)
            if r.get("label") in ("CRASH", "TIMEOUT") or r.get("step", -1) < 0:
                continue
            (off.__setitem__(ckey(r), r) if r["step"] == 0 else acts.append(r))
    rows = []
    for r in acts:
        o = off.get(ckey(r))
        if o is None:
            continue
        prev_cat = o["category"] if r["step"] == 1 else None
        if r.get("kind") == "sequence" and r["step"] > 1:
            continue  # multi-step rows: reported (depth effect), not used to fit the one-step models
        case = SimpleNamespace(grid=r["design"][0] == "grid")
        st = C.State(set(r["prev_diags"]), r["prev_feats"], [], 0, DEFAULT, case, 0.0, np.inf)
        rows.append(dict(key=ckey(r), family=r["family"], corpus=r["corpus"], split=r["split"], remedy=r["remedy"],
                         kind=r["kind"], prop=r["propensity"], diags=r["prev_diags"], x=C.featurize(st),
                         success=float(r["category"] in RIGHT and prev_cat not in RIGHT),
                         harm=float(r["category"] == "false-confident" and prev_cat != "false-confident"),
                         cost=float(r["runtime"] or 0.0) / max(float(o["runtime"] or 1.0), 1.0),
                         off_right=prev_cat in RIGHT))
    return off, rows


def banned_from(rows):
    return sorted({r["remedy"] for r in rows if r["corpus"] == "N" and r["harm"]})


def fit_table(rows):
    t = RemedyTable(default=C.DEFAULT_TABLE)
    cost = defaultdict(list)
    for r in rows:
        if r["off_right"] or r["corpus"] == "N":
            continue
        for d in r["diags"]:
            t.record(d, r["remedy"], r["success"], r["cost"])
        cost[r["remedy"]].append(r["cost"])
    return t, {k: float(np.mean(v)) for k, v in cost.items()}


def _std(X):
    mu, sd = X.mean(0), X.std(0)
    sd[sd < 1e-9] = 1.0
    return mu, sd


def fit_contextual(rows_fit, rows_cal):
    from sklearn.isotonic import IsotonicRegression
    from sklearn.linear_model import LogisticRegression, Ridge

    succ, cost = {}, {}
    for rem in C.REMEDIES:
        fr = [r for r in rows_fit if r["remedy"] == rem and not r["off_right"] and r["corpus"] != "N"]
        hr = [r for r in rows_fit + rows_cal if r["remedy"] == rem and (r["off_right"] or r["corpus"] == "N")]
        harm = (1 + sum(r["harm"] for r in hr)) / (2 + len(hr))
        if len(fr) < MIN_ROWS:
            continue
        X = np.array([r["x"] for r in fr])
        y = np.array([r["success"] for r in fr])
        mu, sd = _std(X)
        if y.min() == y.max():  # one class: constant model at the Beta(1,1) mean
            w, b = np.zeros(X.shape[1]), float(np.log((1 + y.sum()) / (1 + len(y) - y.sum())))
        else:
            m = LogisticRegression(C=0.1, max_iter=2000).fit((X - mu) / sd, y)
            w, b = m.coef_[0], float(m.intercept_[0])
        model = C.LogitIso(w, b, [], [], mu, sd, harm)
        cr = [r for r in rows_cal if r["remedy"] == rem and not r["off_right"] and r["corpus"] != "N"]
        if len(cr) >= MIN_ROWS:
            raw = np.array([C.LogitIso(w, b, [], [], mu, sd)(r["x"]) for r in cr])
            iso = IsotonicRegression(y_min=0, y_max=1, out_of_bounds="clip").fit(raw, [r["success"] for r in cr])
            model = C.LogitIso(w, b, iso.X_thresholds_, iso.y_thresholds_, mu, sd, harm)
        succ[rem] = model
        Xc = np.array([r["x"] for r in fr])
        rg = Ridge(alpha=10.0).fit((Xc - mu) / sd, [r["cost"] for r in fr])
        cost[rem] = C.Linear(rg.coef_, rg.intercept_, mu, sd)
    return {"success": succ, "cost": cost}


def replay(policy_fn, rows):
    """One-step replay on off-wrong cases: the policy picks among the remedies logged for the case
    (and None); value = success rate over cases, cost = mean relative cost of the picks."""
    by = defaultdict(list)
    for r in rows:
        if not r["off_right"] and r["corpus"] != "N":
            by[r["key"]].append(r)
    if not by:
        return 0.0, 0.0, 0
    s = c = 0.0
    for k, rs in by.items():
        pick = policy_fn(rs)
        if pick is not None:
            s += pick["success"]
            c += pick["cost"]
    return s / len(by), c / len(by), len(by)


def pick_contextual(models, lam, banned):
    def fn(rs):
        best, bv = None, 0.0
        for r in rs:
            if r["remedy"] in banned or r["remedy"] not in models["success"]:
                continue
            v = models["success"][r["remedy"]](r["x"]) - lam * models["cost"][r["remedy"]](r["x"])
            if v > bv:
                best, bv = r, v
        return best
    return fn


def pick_table(table, cost, lam, banned):
    def fn(rs):
        best, bv = None, 0.0
        for r in rs:
            if r["remedy"] in banned:
                continue
            lb = max((table.rate(d, r["remedy"])[1] for d in r["diags"] if (d, r["remedy"]) in table._n), default=0)
            v = lb - lam * cost.get(r["remedy"], 0.0)
            if v > bv:
                best, bv = r, v
        return best
    return fn


def pick_rules(banned):
    def fn(rs):
        have = {r["remedy"]: r for r in rs if r["remedy"] not in banned}
        for d in C.DIAGNOSES:
            if d in rs[0]["diags"]:
                for rem in C.DEFAULT_TABLE.get(d, []):
                    if rem in have:
                        return have[rem]
        return None
    return fn


def knee(fn_of_lam, rows):
    vals = [(lam, *replay(fn_of_lam(lam), rows)) for lam in LAMS]
    top = max(v[1] for v in vals)
    lam = max(v[0] for v in vals if v[1] >= 0.9 * top - 1e-12)
    return lam, vals


def ope(models, lam, banned, rows):
    """IPS and DR value of the contextual policy's pick on the uniformly random rows (Dudik et al. 2011)."""
    rnd = [r for r in rows if r["kind"] == "random" and not r["off_right"] and r["corpus"] != "N"]
    if not rnd:
        return None
    fn = pick_contextual(models, lam, banned)
    ips, dr = [], []
    for r in rnd:
        same = [q for q in rows if q["key"] == r["key"]]
        pick = fn(same)
        hit = float(pick is not None and pick["remedy"] == r["remedy"])
        qhat = models["success"][pick["remedy"]](pick["x"]) if pick is not None else 0.0
        qr = models["success"][r["remedy"]](r["x"]) if r["remedy"] in models["success"] else 0.0
        ips.append(hit * r["success"] / r["prop"])
        dr.append(qhat + hit * (r["success"] - qr) / r["prop"])
    return dict(n=len(rnd), ips=float(np.mean(ips)), dr=float(np.mean(dr)))


def train(rows, banned, holdout=None):
    use = [r for r in rows if holdout is None or r["family"] != holdout]
    fit_ = [r for r in use if r["split"] == "fit"]
    cal = [r for r in use if r["split"] == "cal"]
    table, cost = fit_table(fit_)
    lam_t, vt = knee(lambda lam: pick_table(table, cost, lam, banned), cal or fit_)
    models = fit_contextual(fit_, cal)
    lam_c, vc = knee(lambda lam: pick_contextual(models, lam, banned), cal or fit_)
    meta = dict(holdout=holdout, n_fit=len(fit_), n_cal=len(cal), banned=banned, replay_table=vt,
                replay_contextual=vc, replay_rules=replay(pick_rules(banned), cal or fit_),
                ope=ope(models, lam_c, banned, cal or fit_))
    return (C.Fitted("table", lam_t, table=table, cost=cost, meta=meta),
            C.Fitted("contextual", lam_c, models=models, meta=meta))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--logs", nargs="+", required=True)
    ap.add_argument("--out", default=str(MODELS))
    a = ap.parse_args()
    _, rows = load(a.logs)
    banned = banned_from(rows)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "controller_banned.json").write_text(json.dumps(banned))
    summary = {}
    for hold in [None] + sorted({r["family"] for r in rows if r["corpus"] != "N"}):
        tb, cx = train(rows, banned, hold)
        sfx = "" if hold is None else f"_lofo_{hold}"
        (out / f"controller_table{sfx}.pkl").write_bytes(pickle.dumps(tb))
        (out / f"controller_contextual{sfx}.pkl").write_bytes(pickle.dumps(cx))
        summary[hold or "all"] = dict(lam_table=tb.lam, lam_contextual=cx.lam, **cx.meta)
    print(json.dumps(summary, indent=1, default=str))
    (out / "controller_train_summary.json").write_text(json.dumps(summary, indent=1, default=str))


if __name__ == "__main__":
    main()
