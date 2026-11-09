"""E13 (S-PHASE4-ML): corpus of pipeline runs for the learned calibration layers (L2b, L2c, V1).

One row per run of loop.run_loop on a gridded case with a stand-in posterior (fake_posterior), at
several noise levels and seeds:
- run features (learned.features.run_features: no identifiers), the label, P(top);
- correct = right factor set (benchmarks.metrics.score, TOL 0.05);
- per coefficient of each matched factor: z = |estimate - truth| / (90 % half width), per real and
  imaginary part, with the factor's interval features (learned.features.interval_features).
`family` is the case name (the LOFO group). The v1 CASES are the training families; the
GENERAL_CASES (plan v2.13, never used to tune the pipeline) are the held-out test families.

Usage:  python code/experiments/e13_corpus.py [--workers 4] [--seeds 3] [--quick]
Writes code/experiments/out/e13_corpus.jsonl (appends; finished keys are skipped on restart).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import traceback
from concurrent.futures import ProcessPoolExecutor, as_completed

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", ".."))  # benchmarks package
OUT = os.path.join(HERE, "out", "e13_corpus.jsonl")
NOISES = (1e-3, 1e-2, 5e-2)


def _coef_rows(res, name, f):
    from benchmarks.metrics import coef_dist
    from e1_noise import coef_vec, truth
    from pdefactor.learned.features import interval_features

    rows = []
    tr = truth(name, f)
    import sympy as sp

    for j, fr in enumerate(res.factors):
        g = sp.expand(fr.sympy)
        q = min(tr, key=lambda q: coef_dist(q, g))
        if coef_dist(q, g) > 0.05:
            continue  # unmatched factor: no truth to score its intervals against
        cq = coef_vec(q, 0, 0)
        feats = interval_features(res, j)
        m = max(a for a, _ in fr.coef)
        for mon, (mean, lo, hi) in fr.coef.items():
            if mon == (m, 0):
                continue  # monic leading term
            tv = complex(cq.get(mon, 0.0))
            for part in ("real", "imag"):
                hw = abs(getattr(complex(hi), part) - getattr(complex(lo), part)) / 2
                d = abs(getattr(complex(mean), part) - getattr(tv, part))
                if hw <= 0 and d < 1e-12:
                    continue  # identically zero part (e.g. imaginary part of a real factor)
                rows.append({"z": float(d / hw) if hw > 0 else float("inf"), **feats})
    return rows


def run_one(name, noise, seed):
    from benchmarks.metrics import score
    from pdefactor.aggregate import fake_posterior
    from pdefactor.learned.features import run_features
    from pdefactor.loop import run_loop
    from pdefactor.synthetic import any_case, grid

    t0 = time.time()
    f = any_case(name, seed=seed)
    t, x, u = grid(f)
    u = np.real_if_close(u)
    sig = noise * np.std(np.abs(u))
    s, pis = fake_posterior(u, sig, 4, rng=1000 + seed)
    with np.errstate(all="ignore"):
        res = run_loop(s, t, x, sig, pis)
    sc = score(name, f, t, x, [fr.sympy for fr in res.factors])
    return {"key": f"{name}|{noise}|{seed}", "family": name, "noise": noise, "seed": seed,
            "label": res.label, "correct": bool(sc["factor_set"]), "coef_err": sc["coef_err"],
            "features": run_features(res), "coef": _coef_rows(res, name, f),
            "seconds": time.time() - t0}


def _safe(args):
    try:
        return run_one(*args)
    except Exception:  # noqa: BLE001 - a crashed run is recorded, not fatal for the corpus
        return {"key": "|".join(map(str, args)), "error": traceback.format_exc(limit=3)}


def main():
    from pdefactor.synthetic import CASES, GENERAL_CASES

    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--seeds", type=int, default=3)
    ap.add_argument("--quick", action="store_true", help="2 cases x 1 noise x 1 seed (smoke test)")
    a = ap.parse_args()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    done = set()
    if os.path.exists(OUT):
        with open(OUT) as fh:
            done = {json.loads(l)["key"] for l in fh if l.strip()}
    names = ["heat", "damped_beam"] if a.quick else list(CASES) + list(GENERAL_CASES)
    jobs = [(n, nz, sd) for n in names for nz in (NOISES[:1] if a.quick else NOISES)
            for sd in range(1 if a.quick else a.seeds) if f"{n}|{nz}|{sd}" not in done]
    print(f"{len(jobs)} runs to do ({len(done)} done)", flush=True)
    t0 = time.time()
    with ProcessPoolExecutor(a.workers) as ex, open(OUT, "a") as fh:
        futs = [ex.submit(_safe, j) for j in jobs]
        for i, fu in enumerate(as_completed(futs)):
            r = fu.result()
            fh.write(json.dumps(r, default=float) + "\n")
            fh.flush()
            print(f"[{i + 1}/{len(jobs)}] {r['key']} {'ERR' if 'error' in r else r['label']} "
                  f"{time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
