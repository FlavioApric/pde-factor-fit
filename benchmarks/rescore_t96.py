"""Exact T96 rescoring of stored rows (no pipeline rerun): E13 v4 and the P8 pipeline arm.

    OMP_NUM_THREADS=1 .venv/Scripts/python.exe benchmarks/rescore_t96.py [--e13 IN OUT] [--p8 IN OUT]

T96 (loop.GRID_SMOOTH_GOF) downgrades a final FIT-COMPATIBLE to UNDECIDED when
validate.smooth_gof_log10p(reported factors, grid, t, x, sigma) < loop.PRED_LOGP. run_loop applies it only
at depth 0 on one real-valued grid sample with white sigma > 0 (raw is None, noise_draws is None), so:
  - E13: the pipeline arm (run_loop([un], t, x, sig, bootstrap=0) in e13_random_pdes.run_one); the grid is
    regenerated exactly as there (e13_summary._data: default_rng(1000 + seed), sigma = noise * std(u)).
    core and the SINDy methods are not run_loop: unchanged (their equivalence is rescored by the report
    through e13_summary, T95 on).
  - P8: grid rows only (bench_e2e.load_input -> bench.make_input, default_rng(100 + seed)); complex fields
    are skipped (np.isrealobj false, as in run_loop); scattered (400-point) rows have raw / noise_draws and
    stay unchanged.
Every row gets `smooth_gof` (log10 p; null where T96 does not apply) and `t96_downgraded` (bool). The label
of a downgraded row becomes UNDECIDED; nothing else is touched (the P8 report reads the label, so its
classes follow; e13_summary.classify checks `ok` first, so a downgraded right E13 row stays "right": the
report lists those separately).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
for _p in (ROOT / "code", ROOT, ROOT / "benchmarks", ROOT / "code" / "experiments"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))
OUT = ROOT / "benchmarks" / "out"


def _gof(factors, u, t, x, sigma):
    import sympy as sp

    from pdefactor.validate import smooth_gof_log10p

    with np.errstate(all="ignore"):
        lp, _ = smooth_gof_log10p([sp.sympify(q) for q in factors], u, t, x, sigma)
    return float(lp)


def _applies(label, factors, u, sigma):
    return bool(label == "FIT-COMPATIBLE" and factors and sigma and sigma > 0 and np.isrealobj(u))


def rescore_e13(src, dst):
    import e13_summary

    from pdefactor import loop

    rows = [json.loads(s) for s in Path(src).read_text(encoding="utf-8").splitlines() if s.strip()]
    changed = []
    for r in rows:
        p = r.get("pipeline")
        if p is None:
            continue
        p["smooth_gof"], p["t96_downgraded"] = None, False
        if not loop.GRID_SMOOTH_GOF or p.get("error"):
            continue
        t, x, un, sig, _ = e13_summary._data(r)
        if not _applies(p["label"], p["factors"], un, sig):
            continue
        p["smooth_gof"] = _gof(p["factors"], un, t, x, sig)
        if p["smooth_gof"] < loop.PRED_LOGP:
            p["label"], p["t96_downgraded"] = "UNDECIDED", True
            changed.append(f"{r['family']}-{r['seed']}")
        print(f"E13 {r['family']}-{r['seed']}: smooth_gof {p['smooth_gof']:.3g} ok={p['ok']}"
              f"{' -> UNDECIDED' if p['t96_downgraded'] else ''}", flush=True)
    Path(dst).write_text("".join(json.dumps(r, default=str) + "\n" for r in rows), encoding="utf-8")
    return changed


def rescore_p8(src, dst):
    from bench_e2e import load_input

    from pdefactor import loop

    rows = [json.loads(s) for s in Path(src).read_text(encoding="utf-8").splitlines() if s.strip()]
    changed = []
    for r in rows:
        r["smooth_gof"], r["t96_downgraded"] = None, False
        if not loop.GRID_SMOOTH_GOF or r.get("error") or str(r["sampling"]) != "grid" or r.get("method") != "pipeline":
            continue
        inp = load_input(r["case"], float(r["noise"]), "grid", int(r["seed"]))
        u = inp["samples"][0]
        if not _applies(r["label"], r["factors"], u, inp["sigma"]):
            continue
        r["smooth_gof"] = _gof(r["factors"], u, inp["t"], inp["x"], inp["sigma"])
        if r["smooth_gof"] < loop.PRED_LOGP:
            r["label"], r["t96_downgraded"] = "UNDECIDED", True
            changed.append(f"{r['case']} grid {float(r['noise']) * 100:g} %")
        print(f"P8 {r['case']} grid {r['noise']}: smooth_gof {r['smooth_gof']:.3g} factor_set={r['factor_set']}"
              f"{' -> UNDECIDED' if r['t96_downgraded'] else ''}", flush=True)
    Path(dst).write_text("".join(json.dumps(r, default=str) + "\n" for r in rows), encoding="utf-8")
    return changed


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--e13", nargs=2, type=Path, default=[OUT / "e13_v4.jsonl", OUT / "e13_v4_t96.jsonl"])
    ap.add_argument("--p8", nargs=2, type=Path, default=[OUT / "p8_pipeline.jsonl", OUT / "p8_pipeline_t96.jsonl"])
    a = ap.parse_args(argv)
    print("E13 downgraded:", rescore_e13(*a.e13))
    print("P8 downgraded:", rescore_p8(*a.p8))


if __name__ == "__main__":
    main()
