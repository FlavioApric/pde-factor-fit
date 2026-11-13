"""Large benchmark on random PDEs: many distinct equations, independent draws, all methods.

    python benchmarks/bench_large.py --seeds 0-99 --noises 0.01 0.05 --workers 6
    python benchmarks/bench_large.py --seeds 0-1 --families F1 --dry-run

Every (family, seed) of pdefactor.simulator.random_pde is a different equation with a known truth and an
independent field; none was used to tune the pipeline. For each (family, seed, noise) the noisy grid is the
one of code/experiments/e13_random_pdes.run_one (same generator seeds, so draws 0-3 at noise 0.01 reproduce
the E13 rows). One row per draw, one key per method, appended to benchmarks/out/large.jsonl (resumable:
finished (family, seed, noise) are skipped). Each draw runs in its own Python process so a crash or a hang
is confined to that draw (killed after --stall seconds, reported, not retried).
Report: python benchmarks/large_report.py
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "benchmarks" / "out" / "large.jsonl"
FAMILIES = ("F1", "F2", "F3", "F4", "F5")
METHODS = ("pipeline", "core", "pdefind", "weak_sindy", "ensemble_sindy", "sbr_sindy", "bopdmd")
MARK = "@@ROW@@ "
STALL = 10800  # s: hang guard only (accuracy first)


def parse_seeds(items):
    out = []
    for s in items:
        if "-" in s:
            a, b = s.split("-")
            out += range(int(a), int(b) + 1)
        else:
            out.append(int(s))
    return out


def key(r):
    return (r["family"], int(r["seed"]), float(r["noise"]))


def _one(spec):
    sys.path.insert(0, str(ROOT / "code" / "experiments"))
    import warnings

    warnings.filterwarnings("ignore")
    from e13_random_pdes import run_one

    fam, seed, noise, methods = json.loads(spec)
    print(MARK + json.dumps(run_one(fam, seed, noise, methods), default=str), flush=True)


def main():
    if len(sys.argv) > 2 and sys.argv[1] == "--one":
        return _one(sys.argv[2])
    ap = argparse.ArgumentParser()
    ap.add_argument("--families", nargs="*", default=list(FAMILIES))
    ap.add_argument("--seeds", nargs="*", default=["0-99"], help="e.g. 0-99 or 3 7 10-20")
    ap.add_argument("--noises", nargs="*", type=float, default=[0.01, 0.05])
    ap.add_argument("--methods", nargs="*", default=list(METHODS))
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--stall", type=int, default=STALL)
    ap.add_argument("--out", type=Path, default=OUT)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    a.out.parent.mkdir(parents=True, exist_ok=True)
    done = set()
    if a.out.exists():
        done = {key(json.loads(ln)) for ln in a.out.read_text().splitlines() if ln.strip()}
    todo = [(f, s, nz) for s in parse_seeds(a.seeds) for nz in a.noises for f in a.families if (f, s, nz) not in done]
    si, sn = int(os.environ.get("QAF_SHARD_INDEX", 1)), int(os.environ.get("QAF_SHARD_TOTAL", 1))
    todo = todo[si - 1::sn]  # pool shards: disjoint slices of the same task list
    print(f"{len(todo)} draws to run ({len(done)} done), methods {a.methods}", flush=True)
    if a.dry_run:
        return
    env = dict(os.environ, OMP_NUM_THREADS="1", MKL_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", PYTHONWARNINGS="ignore")
    queue, running, n, t0 = list(todo), {}, 0, time.time()
    with open(a.out, "a") as fh:
        while queue or running:
            while queue and len(running) < a.workers:
                tk = queue.pop(0)
                spec = json.dumps([tk[0], tk[1], tk[2], a.methods])
                pr = subprocess.Popen([sys.executable, "-u", str(Path(__file__).resolve()), "--one", spec],
                                      stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=(ef := tempfile.TemporaryFile(mode='w+')),
                                      text=True, env=env, cwd=str(ROOT))
                running[pr] = (tk, time.time(), ef)
            time.sleep(0.5)
            for pr in list(running):
                tk, ts, ef = running[pr]
                if pr.poll() is None:
                    if time.time() - ts > a.stall:
                        pr.kill()
                        pr.communicate()
                        del running[pr]
                        n += 1
                        print("TIMEOUT", tk, flush=True)
                    continue
                so, _ = pr.communicate()
                ef.seek(0)
                se = ef.read()
                del running[pr]
                n += 1
                line = next((ln for ln in so.splitlines() if ln.startswith(MARK)), None)
                if pr.returncode != 0 or line is None:
                    print("FAILED", tk, (se.strip().splitlines() or [""])[-1][:200], flush=True)
                    continue
                fh.write(line[len(MARK):] + "\n")
                fh.flush()
                print(f"{n}/{len(todo)} {tk} {time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
