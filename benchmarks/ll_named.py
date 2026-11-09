"""S-LEARNED gate criterion 5: the named cases (synthetic.CASES) are an external test only, never
fitted. Each case on a 5 % grid and on 400 pts @ 5 % / 2000 pts @ 1 % (seed 0, main's GP caches),
pipeline off and with one learned arm, exactly as benchmarks/bench_e2e.run_method. One jsonl row per
run; a summary table with --summary.

Usage: python ll_named.py --learned off highk --out analysis/exp/out/ll_named.jsonl
       python ll_named.py --summary analysis/exp/out/ll_named.jsonl --arm highk
"""
from __future__ import annotations

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import argparse
import json
import multiprocessing as mp
import sys
import time
import warnings
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
for p in (ROOT / "code", ROOT, Path(__file__).parent):
    sys.path.insert(0, str(p))
warnings.filterwarnings("ignore")

DESIGNS = [("grid", 0.05), (400, 0.05), (2000, 0.01)]


def run_one(name, design, arm):
    from benchmarks import metrics as M
    from benchmarks.bench_e2e import BOOT, S_LOOP, _cover, _w_cover, load_input
    from ll_corpus import LEARNED

    from pdefactor.learned.config import Learned
    from pdefactor.loop import run_loop

    sampling, noise = design
    inp = load_input(name, noise, sampling, 0)
    if inp is None:
        return None
    t, x, f = inp["t"], inp["x"], inp["field"]
    grid_in = inp["draws"] is None
    S, w = inp["samples"][:S_LOOP], inp["weights"][:S_LOOP]
    nd = None if grid_in else np.sqrt(2) * inp["draws"]  # as bench_e2e: all draws
    t0 = time.perf_counter()
    with np.errstate(all="ignore"):
        r = run_loop(list(S), t, x, inp["sigma"] if grid_in else 0.0, w / w.sum(), noise_draws=nd, raw=inp.get("raw"),
                     bootstrap=BOOT if grid_in else 0, learned=Learned(**LEARNED[arm]))
    facs = r.pruned()
    sc = M.score(name, f, t, x, facs)
    row = dict(case=name, design=list(design), learned=arm, label=r.label, factors=[str(q) for q in facs],
               factor_set=sc["factor_set"], coef_err=sc["coef_err"], cover90=_cover(r.factors, M.truth(name, f)),
               w_cover90=_w_cover(name, f, t, x, facs, r.split["w_q"]) if r.split else None,
               runtime=time.perf_counter() - t0, note=r.note)
    return row


def _child(conn, args):
    from ll_corpus import _below_normal

    _below_normal()
    try:
        conn.send(run_one(*args))
    except Exception as e:  # noqa: BLE001
        conn.send(dict(case=args[0], design=list(args[1]), learned=args[2], label="CRASH", factor_set=False,
                       error=f"{type(e).__name__}: {e}"))
    conn.close()


def run_all(tasks, out, workers, cap=1200.0):
    ctx = mp.get_context("spawn")
    pending, live = list(tasks), []
    from slots import Pool  # machine-wide CPU slots shared across sessions

    pool = Pool()
    while pending or live:
        while pending and len(live) < workers:
            slot = pool.try_acquire()
            if slot is None:
                break
            args = pending.pop(0)
            a, b = ctx.Pipe(duplex=False)
            p = ctx.Process(target=_child, args=(b, args), daemon=True)
            p.start()
            live.append((p, a, args, time.time(), slot))
        time.sleep(0.5)
        still = []
        for p, conn, args, ts, slot in live:
            row = None
            if conn.poll():
                row = conn.recv() or "skip"
                p.join(5)
            elif time.time() - ts > cap or not p.is_alive():
                p.terminate()
                p.join(5)
                row = dict(case=args[0], design=list(args[1]), learned=args[2], factor_set=False,
                           label="TIMEOUT" if time.time() - ts > cap else "CRASH")
            if row is None:
                still.append((p, conn, args, ts, slot))
                continue
            pool.release(slot)
            if row != "skip":
                with open(out, "a") as fh:
                    fh.write(json.dumps(row, default=str) + "\n")
                print(row["case"], row["design"], row["learned"], row["label"], row.get("factor_set"), flush=True)
        live = still


def summary(path, arm):
    rows = [json.loads(line) for line in Path(path).read_text().splitlines() if line.strip()]
    key = lambda r: (r["case"], tuple(r["design"]))  # noqa: E731
    off = {key(r): r for r in rows if r["learned"] == "off"}
    on = {key(r): r for r in rows if r["learned"] == arm}
    ks = sorted(set(off) & set(on), key=str)
    print(f"## Named cases: {arm} vs off ({len(ks)} pairs)\n")
    print("| case | design | off: label / set / cover90 | on: label / set / cover90 |\n|---|---|---|---|")
    worse = 0
    for k in ks:
        a, b = off[k], on[k]
        fmt = lambda r: f"{r['label']} / {'right' if r.get('factor_set') else 'wrong'} / {r.get('cover90')}"  # noqa: E731
        if (a.get("factor_set") and not b.get("factor_set")) or a["label"] != b["label"] or a.get("factors") != b.get("factors"):
            worse += bool(a.get("factor_set") and not b.get("factor_set"))
            print(f"| {k[0]} | {k[1]} | {fmt(a)} | {fmt(b)} |")
    print(f"\nright sets: off {sum(bool(off[k].get('factor_set')) for k in ks)} / on "
          f"{sum(bool(on[k].get('factor_set')) for k in ks)} of {len(ks)}; lost by the layer: {worse}; "
          "rows not listed are identical in label and factors.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--learned", nargs="*", default=["off"])
    ap.add_argument("--cases", nargs="*", default=None)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--out")
    ap.add_argument("--summary")
    ap.add_argument("--arm")
    a = ap.parse_args()
    if a.summary:
        return summary(a.summary, a.arm)
    from pdefactor.synthetic import CASES

    done = set()
    if Path(a.out).exists():
        for line in Path(a.out).read_text().splitlines():
            r = json.loads(line)
            done.add((r["case"], tuple(r["design"]), r["learned"]))
    tasks = [(c, d, ln) for c in (a.cases or CASES) for d in DESIGNS for ln in a.learned if (c, d, ln) not in done]
    print(f"{len(tasks)} runs", flush=True)
    run_all(tasks, a.out, a.workers)


if __name__ == "__main__":
    main()
