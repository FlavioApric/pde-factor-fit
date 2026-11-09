"""S-LEARNED gate (sessions/LEARNED/PLAN.md §2.4): one learned arm against the off arm on the same
corpus runs (paired by corpus, family, seed, design). Prints a markdown table and the verdict.

  1 primary target improved, paired bootstrap 95 % CI of the difference excluding 0
  2 right-set (right + equivalent) >= off - 0.02 and false-confident <= off
  3 coefficient 90 % coverage: |cov - 0.9| not worse by more than 0.02
  4 nulls (corpus N): false-confident not above off
  (5 named cases and 6 fresh-context review are checked outside this script)

Usage: python ll_gate.py OFF.jsonl ON.jsonl --arm highk --target right [--split test]
targets: right (right-set rate), coverage (|cov - 0.9|, lower is better), iscore (interval score of
the 90 % coefficient intervals, lower is better), runtime (seconds, lower is better)
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

ALPHA = 0.1  # 90 % intervals


def load(paths, arm, splits):
    rows = {}
    for p in paths:
        for line in Path(p).read_text().splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            if r.get("learned") != arm or (splits and r.get("split") not in splits):
                continue
            rows[(r["corpus"], r["family"], r["seed"], tuple(r["design"]))] = r
    return rows


def right_set(r):
    return float(r.get("category") in ("right", "equivalent"))


def false_conf(r):
    return float(r.get("category") == "false-confident")


def coef_cells(r):
    """(hit, interval score) per real or imaginary part of each coefficient of the truth, on runs whose
    factor set is right (the intervals are conditional on the selected structure)."""
    out = []
    if r.get("category") != "right":
        return out
    for c in r.get("coef", []):
        for i in (0, 1):
            v, lo, hi = c["true"][i], c["lo"][i], c["hi"][i]
            if lo == hi == v == 0:
                continue
            w = hi - lo
            pen = (2 / ALPHA) * (max(lo - v, 0) + max(v - hi, 0))
            scale = max(abs(v), 1e-3)
            out.append((float(lo <= v <= hi), (w + pen) / scale))
    return out


def per_run(r, target):
    if target == "right":
        return right_set(r)
    if target == "runtime":
        return float(r.get("runtime", np.nan))
    cells = coef_cells(r)
    if not cells:
        return np.nan
    a = np.array(cells)
    return float(a[:, 0].mean()) if target == "coverage" else float(np.median(a[:, 1]))


def boot_ci(d, B=2000, seed=0):
    d = np.asarray(d, float)
    d = d[np.isfinite(d)]
    if not len(d):
        return np.nan, np.nan, np.nan
    rng = np.random.default_rng(seed)
    m = rng.choice(d, (B, len(d))).mean(1)
    return float(d.mean()), float(np.quantile(m, 0.025)), float(np.quantile(m, 0.975))


def coverage(rows):
    c = [h for r in rows for h, _ in coef_cells(r)]
    return float(np.mean(c)) if c else np.nan, len(c)


def weight_cover(rows):
    """cover90 of the split-layer weights: true weight of each true factor inside the 90 % band of
    the reported factor it is matched to (runs with a right factor set and defined true weights)."""
    h = []
    for r in rows:
        wt, wq, mt = r.get("w_true"), r.get("w_q"), r.get("w_match")
        if r.get("category") != "right" or not wt or not wq or not mt:
            continue
        for v, j in zip(wt, mt):
            if v is not None and j < len(wq):
                h.append(float(wq[j][0] <= v <= wq[j][2]))
    return (float(np.mean(h)) if h else np.nan), len(h)


def gate(off, on, target, null_off=None, null_on=None):
    keys = sorted(set(off) & set(on), key=repr)  # designs mix "grid" and ints
    a, b = [off[k] for k in keys], [on[k] for k in keys]
    lines, ok = [], True
    if target == "coverage":
        # the primary of a calibration layer is |cov - 0.9| over the pooled cells: CI by resampling runs
        rng = np.random.default_rng(0)
        idx = np.arange(len(keys))
        diffs = []
        for _ in range(2000):
            s = rng.choice(idx, len(idx))
            ca, _ = coverage([a[i] for i in s])
            cb, _ = coverage([b[i] for i in s])
            diffs.append(abs(ca - 0.9) - abs(cb - 0.9))
        diffs = np.array(diffs)[np.isfinite(diffs)]
        m, lo, hi = float(diffs.mean()), float(np.quantile(diffs, 0.025)), float(np.quantile(diffs, 0.975))
        better = lo > 0
    else:
        d = [per_run(y, target) - per_run(x, target) for x, y in zip(a, b)]
        m, lo, hi = boot_ci(d)
        better = lo > 0 if target == "right" else hi < 0
    ok &= better
    lines.append(f"| 1 primary ({target}) | on - off = {m:+.4f} [95 % CI {lo:+.4f}, {hi:+.4f}] | "
                 f"{'PASS' if better else 'FAIL'} |")
    rs_a, rs_b = np.mean([right_set(r) for r in a]), np.mean([right_set(r) for r in b])
    fc_a, fc_b = sum(false_conf(r) for r in a), sum(false_conf(r) for r in b)
    g2 = rs_b >= rs_a - 0.02 and fc_b <= fc_a
    ok &= g2
    lines.append(f"| 2 right-set / false-confident | {rs_a:.3f} -> {rs_b:.3f}; {fc_a:.0f} -> {fc_b:.0f} | "
                 f"{'PASS' if g2 else 'FAIL'} |")
    (ca, na), (cb, nb) = coverage(a), coverage(b)
    g3 = not (abs(cb - 0.9) > abs(ca - 0.9) + 0.02) if np.isfinite(ca) and np.isfinite(cb) else True
    ok &= g3
    lines.append(f"| 3 coefficient coverage (90 %) | {ca:.3f} (n={na}) -> {cb:.3f} (n={nb}) | {'PASS' if g3 else 'FAIL'} |")
    (wa, nwa), (wb, nwb) = weight_cover(a), weight_cover(b)
    lines.append(f"| (info) weight cover90 | {wa:.3f} (n={nwa}) -> {wb:.3f} (n={nwb}) | |")
    if null_off is not None:
        nk = sorted(set(null_off) & set(null_on), key=repr)
        fa = sum(false_conf(null_off[k]) for k in nk)
        fb = sum(false_conf(null_on[k]) for k in nk)
        g4 = fb <= fa
        ok &= g4
        lines.append(f"| 4 nulls false-confident | {fa:.0f} -> {fb:.0f} of {len(nk)} | {'PASS' if g4 else 'FAIL'} |")
    to_a = sum(r.get("label") == "TIMEOUT" for r in a)
    to_b = sum(r.get("label") == "TIMEOUT" for r in b)
    rt_a = np.nanmedian([r.get("runtime", np.nan) for r in a]) if a else np.nan
    rt_b = np.nanmedian([r.get("runtime", np.nan) for r in b]) if b else np.nan
    lines.append(f"| (info) paired runs / timeouts / median runtime s | {len(keys)}; {to_a} -> {to_b}; "
                 f"{rt_a:.0f} -> {rt_b:.0f} | |")
    return ok, lines


def by_family(off, on):
    fams = sorted({k[1] for k in set(off) & set(on)})
    out = ["| family | n | right-set off | right-set on | false-conf off | false-conf on |", "|---|---|---|---|---|---|"]
    for f in fams:
        ks = [k for k in set(off) & set(on) if k[1] == f]
        out.append(f"| {f} | {len(ks)} | {np.mean([right_set(off[k]) for k in ks]):.2f} | "
                   f"{np.mean([right_set(on[k]) for k in ks]):.2f} | {sum(false_conf(off[k]) for k in ks):.0f} | "
                   f"{sum(false_conf(on[k]) for k in ks):.0f} |")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--arm", required=True)
    ap.add_argument("--target", default="right", choices=["right", "coverage", "iscore", "runtime"])
    ap.add_argument("--split", nargs="*", default=["test"])
    ap.add_argument("--nulls", nargs="*", default=[])
    a = ap.parse_args()
    off, on = load(a.files, "off", a.split), load(a.files, a.arm, a.split)
    noff = non = None
    if a.nulls:
        noff, non = load(a.nulls, "off", a.split), load(a.nulls, a.arm, a.split)
    ok, lines = gate(off, on, a.target, noff, non)
    print(f"## Gate: {a.arm} vs off (splits {a.split}, target {a.target})\n")
    print("| criterion | value | result |\n|---|---|---|")
    print("\n".join(lines))
    print("\n" + "\n".join(by_family(off, on)))
    print(f"\n**verdict: {'PASS' if ok else 'FAIL'}** (criteria 5-6 checked separately)")


if __name__ == "__main__":
    main()
