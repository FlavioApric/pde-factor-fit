"""S-LEARNED-LB harm check (sessions/LEARNED/LB/PLAN.md §1, §7): pairs the `lb` arm with the off arm on
the same draws and counts

- harmed: the label or the final factor set differs from off (parent session, 2026-10-29); a row that
  is TIMEOUT or CRASH on exactly one arm is listed apart (a skip may turn a timeout into an answer);
- coefficient / interval differences beyond 1e-9 on rows that are not harmed (expected zero: a skip of
  a step that changes nothing is exact);
- the one-sided 95 % Clopper-Pearson upper bound of the harmed rate.

Usage: python ll_budget_harm.py FILES.jsonl ... [--arm lb] [--base off] [--split test] [--out md]
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

STOP = ("TIMEOUT", "CRASH")


def load(paths):
    rows = []
    for p in paths:
        for line in Path(p).read_text().splitlines():
            if line.strip():
                rows.append(json.loads(line))
    return rows


def key(r):
    return r["corpus"], r["family"], r["seed"], tuple(r["design"])


def cp_upper(k, n, conf=0.95):
    """One-sided Clopper-Pearson upper bound of a binomial rate."""
    if n == 0:
        return float("nan")
    if k >= n:
        return 1.0
    from scipy.stats import beta

    return float(beta.ppf(conf, k + 1, n - k))


def _nums(v):
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        return [float(v)]
    if isinstance(v, dict):
        return [x for k in sorted(v) for x in _nums(v[k])]
    if isinstance(v, (list, tuple)):
        return [x for e in v for x in _nums(e)]
    return []


def coef_differs(a, b, tol=1e-9):
    if a.get("lb_answer") is not None and b.get("lb_answer") is not None:
        return a["lb_answer"] != b["lb_answer"]
    na, nb = _nums(a.get("coef")), _nums(b.get("coef"))
    if len(na) != len(nb):
        return True
    x, y = np.array(na), np.array(nb)
    both_nan = np.isnan(x) & np.isnan(y)
    return bool(np.any(~both_nan & ~(np.abs(x - y) <= tol * np.maximum(1.0, np.abs(x)))))


def compare(rows, arm="lb", base="off", splits=("test",)):
    A = {key(r): r for r in rows if r.get("learned") == base and r.get("split") in splits}
    B = {key(r): r for r in rows if r.get("learned") == arm and r.get("split") in splits}
    keys = sorted(set(A) & set(B), key=str)
    harmed, stop_changed, coef, both_stop = [], [], [], 0
    for k in keys:
        a, b = A[k], B[k]
        sa, sb = a["label"] in STOP, b["label"] in STOP
        if sa and sb:
            both_stop += 1
            continue
        if sa != sb:
            stop_changed.append(k)
            continue
        if a["label"] != b["label"] or sorted(a.get("factors") or []) != sorted(b.get("factors") or []):
            harmed.append(k)
        elif coef_differs(a, b):
            coef.append(k)
    n = len(keys) - both_stop - len(stop_changed)
    return dict(n_pairs=len(keys), n_compared=n, both_stopped=both_stop, n_harmed=len(harmed),
                harmed_rate=len(harmed) / n if n else float("nan"), harmed_cp95=cp_upper(len(harmed), n),
                n_coef_diff=len(coef), stop_changed=[list(map(str, k)) for k in stop_changed],
                harmed_keys=[list(map(str, k)) for k in harmed], coef_keys=[list(map(str, k)) for k in coef])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--arm", default="lb")
    ap.add_argument("--base", default="off")
    ap.add_argument("--split", nargs="*", default=["test"])
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    res = compare(load(a.files), a.arm, a.base, tuple(a.split))
    text = "\n".join([f"# LB harm check: {a.arm} vs {a.base}, splits {a.split}", "", "```",
                      json.dumps(res, indent=1), "```"])
    print(text)
    if a.out:
        Path(a.out).write_text(text + "\n")


if __name__ == "__main__":
    main()
