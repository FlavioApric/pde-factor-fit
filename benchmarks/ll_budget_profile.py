"""S-LEARNED-LB P0 (sessions/LEARNED/LB/PLAN.md §5): where does run_loop spend its time, including the
runs that hit the corpus cap and leave no step log?

Each draw runs in its own process (slot pool, below-normal priority). Two records stream to disk while
it runs, so a run killed at the cap still leaves them:
  - every `_Steps.mark` (step name, seconds, changed, recursion depth), one json line per mark;
  - a stack sampler (1 s period): inclusive sample counts per function, rewritten every 30 s.

Usage: python ll_budget_profile.py --out analysis/exp/out/lb_p0 [--cap 2400] [--workers 4]
"""
from __future__ import annotations

import os

for _v in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import argparse
import collections
import json
import multiprocessing as mp
import sys
import threading
import time
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).parent))

# off-arm S draws: six that time out at 1200 s and four that finish (ll_S.jsonl, 2026-10-29)
DRAWS = [("F3", 210, (2000, 0.01)), ("F4", 209, (2000, 0.01)), ("F4", 210, (2000, 0.01)),
         ("F5", 209, (400, 0.05)), ("F5", 210, (400, 0.05)), ("F5", 210, (2000, 0.01)),
         ("F3", 210, (400, 0.05)), ("F4", 210, (400, 0.05)), ("F5", 209, (400, 0.05)),
         ("F3", 209, (2000, 0.01))]
DRAWS = list(dict.fromkeys(DRAWS))


def _sampler(main_ident, path, stop, period=1.0, dump=30.0):
    counts, n, last = collections.Counter(), 0, time.time()
    while not stop.is_set():
        fr = sys._current_frames().get(main_ident)
        seen = set()
        while fr is not None:
            c = fr.f_code
            key = f"{Path(c.co_filename).name}:{c.co_name}"
            if key not in seen:  # inclusive count, once per stack
                counts[key] += 1
                seen.add(key)
            fr = fr.f_back
        n += 1
        if time.time() - last > dump:
            Path(path).write_text(json.dumps(dict(n=n, top=counts.most_common(80))))
            last = time.time()
        stop.wait(period)
    Path(path).write_text(json.dumps(dict(n=n, top=counts.most_common(80))))


def _child(args, out):
    from ll_corpus import _below_normal, make_input

    import pdefactor.loop as L

    _below_normal()
    family, seed, design = args
    tag = f"{family}_{seed}_{design[0]}"
    marks = Path(out) / f"{tag}.marks.jsonl"
    marks.write_text("")
    orig = L._Steps.mark
    depth = {"d": 0}

    def mark(self, name, note="", fp=None, changed=None):
        orig(self, name, note, fp, changed)
        row = self.rows[-1]
        with open(marks, "a") as fh:
            fh.write(json.dumps(dict(id=id(self), step=row[0], sec=row[1], changed=row[2], t=time.time())) + "\n")

    L._Steps.mark = mark
    stop = threading.Event()
    th = threading.Thread(target=_sampler, args=(threading.main_thread().ident, Path(out) / f"{tag}.prof.json", stop),
                          daemon=True)
    th.start()
    t0 = time.perf_counter()
    try:
        inp = make_input("S", family, seed, design)
        t1 = time.perf_counter()
        import numpy as np

        with np.errstate(all="ignore"):
            res = L.run_loop(inp["samples"], inp["t"], inp["x"], inp["sigma"], inp["pis"],
                             noise_draws=inp["noise_draws"], raw=inp["raw"], bootstrap=inp["bootstrap"])
        info = dict(label=res.label, factors=[str(q) for q in res.pruned()], input_s=t1 - t0,
                    loop_s=time.perf_counter() - t1, steps=res.steps)
    except Exception as e:  # noqa: BLE001
        info = dict(label="CRASH", error=f"{type(e).__name__}: {e}", trace=traceback.format_exc()[-1500:])
    stop.set()
    th.join(5)
    (Path(out) / f"{tag}.done.json").write_text(json.dumps(info, default=str))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--cap", type=float, default=2400.0)
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    Path(a.out).mkdir(parents=True, exist_ok=True)
    from slots import Pool

    ctx = mp.get_context("spawn")
    pool, pending, live = Pool(), list(DRAWS), []
    while pending or live:
        while pending and len(live) < a.workers:
            s = pool.try_acquire()
            if s is None:
                break
            args = pending.pop(0)
            p = ctx.Process(target=_child, args=(args, a.out), daemon=True)
            p.start()
            live.append((p, args, time.time(), s))
        time.sleep(2)
        still = []
        for p, args, ts, s in live:
            if p.is_alive() and time.time() - ts <= a.cap:
                still.append((p, args, ts, s))
                continue
            if p.is_alive():
                p.terminate()
                p.join(5)
                print("TIMEOUT", args, flush=True)
            else:
                print("done", args, round(time.time() - ts), flush=True)
            pool.release(s)
        live = still


if __name__ == "__main__":
    main()
