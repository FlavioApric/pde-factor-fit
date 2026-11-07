"""Worked example for the paper: one benchmark input, run with exactly the benchmark protocol,
then handed to final_report for the full report (factors, posterior, Friedrichs layer, E_int,
images of the factor "directions" and of the grouping in operator space).

Protocol (identical to benchmarks/bench_e2e.py, gridded input):
  one noisy grid, white noise sigma, run_loop(..., bootstrap=16), equation = res.pruned().

Run from the repository root (package `pdefactor` installed):
    python ../paper/shared/experiments/worked_example.py --case transport_plus_diffusion --noise 0.05
Outputs go to --out (report.md, report.json, images, res.pkl, input.npz).
"""
from __future__ import annotations

import argparse
import json
import pickle
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path.cwd()  # the repository root
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "benchmarks"))

BOOT = 16  # as bench_e2e.BOOT


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--case", default="transport_plus_diffusion")
    ap.add_argument("--noise", type=float, default=0.05)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", required=True)
    ap.add_argument("--reuse", action="store_true")
    a = ap.parse_args(argv)

    from benchmarks.bench import make_input
    from final_report import final_report
    from pdefactor.loop import run_loop

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    inp = make_input(a.case, a.noise, "grid", a.seed)
    U, t, x, sig, f = inp["U"], inp["t"], inp["x"], inp["sigma"], inp["field"]
    np.savez_compressed(out / "input.npz", U=U, t=t, x=x, sigma=sig)
    cache = out / "res.pkl"
    t0 = time.perf_counter()
    if a.reuse and cache.exists():
        res = pickle.loads(cache.read_bytes())
    else:
        res = run_loop([U], t, x, sig, np.ones(1), bootstrap=BOOT)
        cache.write_bytes(pickle.dumps(res))
    wall = time.perf_counter() - t0
    final_report(res, samples=[U], pis=np.ones(1), t=t, x=x, sigma=sig, truth=f,
                 kwargs={"case": a.case, "noise": a.noise, "seed": a.seed, "protocol": "bench_e2e grid",
                         "bootstrap": BOOT}, out=str(out))
    pr = [str(q) for q in res.pruned()]
    (out / "pruned.json").write_text(json.dumps({"pruned": pr, "wall_s": wall}, indent=1))
    print(res.summary())
    print("pruned:", pr, f"wall {wall:.1f}s")


if __name__ == "__main__":
    main()
