"""Multi-seed benchmark on the grid designs: every case, noise 1% and 5%, seeds 1-3, with an
independent field AND noise draw per seed (PDEFACTOR_FIELD_SEED=1), so that repeated cells are
independent trials. Same protocol as benchmarks/bench_e2e.py (one noisy grid, bootstrap intervals).

Run from the repository root (package installed):
    PDEFACTOR_FIELD_SEED=1 python ../paper/shared/experiments/multiseed.py --out ms.jsonl --workers 4 \
        --methods pipeline weak_sindy
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "analysis" / "exp"))
sys.path.insert(0, str(ROOT / "benchmarks"))

CASES = ["transport", "heat", "advection_diffusion", "transport_plus_diffusion", "wave", "beam",
         "klein_gordon", "telegraph", "airy", "schrodinger"]


def one(job):
    os.environ["PDEFACTOR_FIELD_SEED"] = "1"
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    from benchmarks.bench_e2e import load_input, run_method
    from benchmarks.micro import outcome

    method, name, noise, seed = job
    inp = load_input(name, noise, "grid", seed)
    row = run_method(method, name, inp)
    row.update(noise=noise, seed=seed, design="grid", field_seed=True)
    if method == "pipeline":
        row["outcome"] = outcome(row)
    else:
        row["outcome"] = "right" if row.get("factor_set") else "false-confident"
    row.pop("trace", None)
    return row


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--seeds", type=int, nargs="+", default=[1, 2, 3])
    ap.add_argument("--noises", type=float, nargs="+", default=[0.01, 0.05])
    ap.add_argument("--methods", nargs="+", default=["pipeline"])
    a = ap.parse_args(argv)
    out = Path(a.out)
    done = set()
    if out.exists():
        for line in out.read_text().splitlines():
            r = json.loads(line)
            done.add((r["method"], r["case"], r["noise"], r["seed"]))
    jobs = [(m, c, nz, s) for m in a.methods for nz in a.noises for s in a.seeds for c in CASES
            if (m, c, nz, s) not in done]
    with ProcessPoolExecutor(a.workers) as ex, out.open("a") as fh:
        futs = {ex.submit(one, j): j for j in jobs}
        for f in as_completed(futs):
            try:
                r = f.result()
            except Exception as e:  # noqa: BLE001
                m, c, nz, s = futs[f]
                r = {"method": m, "case": c, "noise": nz, "seed": s, "error": repr(e), "outcome": "error"}
            fh.write(json.dumps(r, default=str) + "\n")
            fh.flush()
            print(r["method"], r["case"], r["noise"], r["seed"], r.get("outcome"), round(r.get("runtime", 0), 1),
                  flush=True)


if __name__ == "__main__":
    main()
