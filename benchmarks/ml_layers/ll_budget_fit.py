"""S-LEARNED-LB: fit the per-step skip models on log-mode rows, set lam by risk control, replay (C2).

  fit split        -> classifiers (constant / logistic / hgb)
  calibrate split  -> lam by conformal risk control at alpha (LTT reported)
  test split, LOFO -> offline replay: harmed-run rate (conservative) and seconds saved
Two profiles: exact (zero-harm rule) and fast (CRC at alpha); for each, the model with the largest
calibrate-split saving under its rule is written to --save-dir/lb_<profile>.pkl.

Usage: python ll_budget_fit.py ROWS.jsonl [ROWS2.jsonl ...] [--alpha 0.02] [--save-dir src/pdefactor/learned/models]
       python ll_budget_fit.py --retrain [--workers 4] [--gp-cache DIR]
--retrain rebuilds the layer on the current pipeline in one command: log-only (log-as-off) corpus rows
of S fit+cal and G fit+cal through ll_budget_corpus.py (resumable: done rows are kept), then fit,
calibrate and save to the default model; the pipeline's git sha goes into the model's meta.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pickle
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from pdefactor.learned import budget as B  # noqa: E402

KINDS = ("constant", "logistic", "hgb")
FAMS = ("F1", "F2", "F3", "F4", "F5")


def load(paths, arm="lblog"):
    rows = []
    for p in paths:
        for line in Path(p).read_text().splitlines():
            if line.strip():
                r = json.loads(line)
                # log-as-off rows; TIMEOUT rows of that file carry the streamed partial log (lb.partial)
                logged = r.get("lb_log") or (r.get("lb") or {}).get("partial")
                if (r.get("learned") == arm or (r.get("learned") == "off" and logged)) and (r.get("lb") or {}).get("features") is not None and r.get("steps"):
                    rows.append(r)
    return rows


def summary(model, rows):
    """Replay: harmed rate (conservative), median and total fraction of runtime saved, skips per step."""
    if not rows:
        return dict(n=0)
    L, S = B.replay(model, rows)
    rt = np.array([r["runtime"] for r in rows])
    frac = S / np.maximum(rt, 1e-9)
    on = rt - S
    return dict(n=len(rows), harmed=float(L.mean()), n_harmed=int(L.sum()), bound0=B.zero_bound(len(rows)),
                med_off=float(np.median(rt)), med_on=float(np.median(on)),
                saved_total=float(S.sum() / rt.sum()), saved_med=float(np.median(frac)))


def pick(rows, alpha, fams=FAMS, rule="zero"):
    fit = [r for r in rows if r["split"] == "fit" and r["family"] in fams]
    cal = [r for r in rows if r["split"] == "cal" and r["family"] in fams]
    best, table = None, {}
    for kind in KINDS:
        m = B.calibrate(B.fit(fit, kind), cal, alpha, rule=rule)
        s = summary(m, cal)
        table[kind] = dict(lam=m.lam, lam_crc=m.meta["lam_crc"], lam_ltt=m.meta["lam_ltt"], **s)
        if best is None or s.get("saved_total", 0) > best[1].get("saved_total", 0):
            best = (m, s)
    return best[0], table


def retrain(workers=4, gp_cache=None, out_dir=ROOT / "analysis" / "exp" / "out"):
    import subprocess

    paths = []
    for corpus in ("S", "G"):
        out = Path(out_dir) / f"ll_{corpus}_fitcal_off.jsonl"
        cmd = [sys.executable, str(Path(__file__).with_name("ll_budget_corpus.py")), "--corpus", corpus, "--split",
               "fit", "cal", "--learned", "off", "--log-as-off", "--tripwire", "10", "--workers", str(workers),
               "--out", str(out)]
        if gp_cache and corpus == "S":
            cmd += ["--gp-cache", str(gp_cache)]
        subprocess.run(cmd, check=True)
        paths.append(str(out))
    return paths


def git_sha():
    import subprocess

    try:
        return subprocess.run(["git", "-c", "safe.directory=*", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                              capture_output=True, text=True).stdout.strip() or None
    except OSError:
        return None


PROFILE_RULE = {"exact": "zero", "fast": "crc"}  # budget profile -> threshold rule (budget.PROFILES)


def crossfit_scores(rows, kind):
    """Out-of-family scores: each family's runs are scored by a model fit on the other four families'
    fit + cal runs (so the calibration set is every run, n = 165 here, instead of the cal split)."""
    sc = [None] * len(rows)
    for f in FAMS:
        rest = [r for r in rows if r["family"] != f]
        idx = [i for i, r in enumerate(rows) if r["family"] == f]
        if not idx or not rest:
            continue
        s = B.run_scores(B.fit(rest, kind), [rows[i] for i in idx])
        for i, v in zip(idx, s):
            sc[i] = v
    return [v or [] for v in sc]


def report_cv(rows, alpha, rule, profile):
    """Cross-fitted calibration (cross-conformal; the guarantee holds approximately, about 2 alpha in the
    worst case, Barber et al. 2021): lam by `rule` on the out-of-family scores of every run; the final
    model is fit on all runs and gets that lam. The real held-out check is the test split."""
    rt = np.array([r["runtime"] for r in rows])
    md = [f"## profile `{profile}`: cross-fitted calibration (rule {rule}, alpha = {alpha}, n = {len(rows)})", "",
          "| model | lam | runs harmed | 95 % bound if 0 | saved (total) | saved (median) | per family harmed / n |",
          "|---|---|---|---|---|---|---|"]
    best = None
    for kind in KINDS:
        sc = crossfit_scores(rows, kind)
        lam = B.zero_threshold(sc) if rule == "zero" else B.crc_threshold(sc, alpha)
        L, S = B.loss_at(sc, lam)
        fam = " ".join(f"{f} {int(sum(L[i] for i, r in enumerate(rows) if r['family'] == f))}/"
                       f"{sum(r['family'] == f for r in rows)}" for f in FAMS)
        saved = float(S.sum() / rt.sum())
        md.append(f"| {kind} | {lam:.3g} | {int(L.sum())} | {B.zero_bound(len(rows)):.3f} | {saved:.3f} | "
                  f"{float(np.median(S / np.maximum(rt, 1e-9))):.3f} | {fam} |")
        if best is None or saved > best[2]:
            best = (kind, lam, saved)
    kind, lam, _ = best
    m = B.fit(rows, kind)
    m.lam, m.alpha = lam, alpha
    m.meta.update(rule=rule, calibration="crossfit-lofo", n_cal=len(rows))
    md += ["", f"chosen: {kind}, lam = {lam:.3g} (final model fit on all {len(rows)} runs)"]
    return m, md


def report(rows, alpha, rule, profile):
    """Markdown section of one profile and its chosen model (fit on fit, lam on cal, replay held out)."""
    m, table = pick(rows, alpha, rule=rule)
    md = [f"## profile `{profile}` (rule {rule}, alpha = {alpha})", "", "### calibrate split, all families", "",
          "| model | lam | lam (CRC) | lam (LTT) | n | harmed | saved (total) | saved (median) |",
          "|---|---|---|---|---|---|---|---|"]
    for k, s in table.items():
        md.append(f"| {k} | {s['lam']:.3g} | {s.get('lam_crc', float('nan')):.3g} | {s['lam_ltt']:.3g} | {s.get('n', 0)} | "
                  f"{s.get('harmed', float('nan')):.3f} | {s.get('saved_total', float('nan')):.3f} | "
                  f"{s.get('saved_med', float('nan')):.3f} |")
    test = [r for r in rows if r["split"] == "test"]
    if test:
        md += ["", f"### chosen {m.kind}, lam = {m.lam:.3g}: test split replay", "", "```",
               json.dumps(summary(m, test), indent=1), "```"]
    md += ["", f"### chosen {m.kind}, lam = {m.lam:.3g}. LOFO: fit + calibrate on four families, replay on the "
           "fifth (all its rows)", "",
           "| held out | kind | lam | n | harmed | 95 % bound if 0 | saved (total) | median off -> on (s) |",
           "|---|---|---|---|---|---|---|---|"]
    tot_n = tot_h = 0
    for f in FAMS:
        mf, _ = pick(rows, alpha, fams=tuple(g for g in FAMS if g != f), rule=rule)
        s = summary(mf, [r for r in rows if r["family"] == f])
        if s["n"]:
            tot_n, tot_h = tot_n + s["n"], tot_h + s["n_harmed"]
            md.append(f"| {f} | {mf.kind} | {mf.lam:.3g} | {s['n']} | {s['n_harmed']} | {s['bound0']:.3f} | "
                      f"{s['saved_total']:.3f} | {s['med_off']:.0f} -> {s['med_on']:.0f} |")
    md.append(f"| all | | | {tot_n} | {tot_h} | {B.zero_bound(tot_n):.3f} | | |")
    return m, md


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("rows", nargs="*")
    ap.add_argument("--retrain", action="store_true")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--gp-cache", default=None)
    ap.add_argument("--alpha", type=float, default=B.ALPHA)
    ap.add_argument("--profiles", nargs="*", default=["exact", "fast"])
    ap.add_argument("--calib", default="crossfit", choices=["crossfit", "split"],
                    help="crossfit: lam on out-of-family scores of every run (default); split: the cal split")
    ap.add_argument("--save-dir", default=None, help="writes lb_<profile>.pkl for each profile")
    ap.add_argument("--out", default=None, help="markdown results file")
    a = ap.parse_args()
    if a.retrain:
        a.rows = retrain(a.workers, a.gp_cache)
        a.save_dir = a.save_dir or str(B.MODELS)
        a.out = a.out or str(ROOT / "sessions" / "LEARNED" / "LB" / "fit_results.md")
    rows = load(a.rows)
    counts = {s: sum(r["split"] == s for r in rows) for s in ("fit", "cal", "test")}
    md = ["# LB fit / calibrate / replay", "", f"rows: {len(rows)} {counts}; files {a.rows}; fit sha {git_sha()}", ""]
    h = hashlib.sha256("".join(sorted(json.dumps([r["corpus"], r["family"], r["seed"], r["design"]]) for r in rows))
                       .encode()).hexdigest()[:16]
    for prof in a.profiles:
        m, sec = (report_cv if a.calib == "crossfit" else report)(rows, a.alpha, PROFILE_RULE[prof], prof)
        md += sec + [""]
        if a.save_dir:
            m.meta.update(profile=prof, corpus_hash=h, prior="prior: sim-v2", constants="default",
                          files=[str(p) for p in a.rows], fit_sha=git_sha(),
                          row_shas=sorted({r.get("sha") or "unrecorded" for r in rows}))
            out = Path(a.save_dir) / f"{B.PROFILES[prof]}.pkl"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(pickle.dumps(m))
            md.append(f"saved {out}")
    text = "\n".join(md)
    print(text)
    if a.out:
        Path(a.out).write_text(text + "\n")


if __name__ == "__main__":
    main()
