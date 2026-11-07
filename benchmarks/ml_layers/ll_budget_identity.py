"""S-LEARNED-LB: check on a few corpus draws that the log-only arm (budget=True, no model, MEMO off) and the
memo arm (budget=True, no model, MEMO on) give the off run's answer exactly: label, factor strings,
coefficient tuples, structures, evidence, note. One slot from the machine pool.

Usage: python ll_budget_identity.py [--gp-cache DIR]
"""
from __future__ import annotations

import os

for _v in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import argparse
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import ll_corpus as C  # noqa: E402

DRAWS = [("G", "F1", 100, ("grid", 0.01)), ("G", "F2", 101, ("grid", 0.05)), ("G", "F3", 102, ("grid", 0.01)),
         ("S", "F1", 200, (400, 0.05)), ("S", "F2", 201, (400, 0.05))]


def answer(r):
    coef = [{str(k): tuple(repr(complex(c)) for c in v) for k, v in f.coef.items()} for f in r.factors]
    note = r.note
    return (r.label, [str(f.sympy) for f in r.factors], coef, repr(sorted((str(k), v) for k, v in (r.structures or {}).items())),
            repr(r.evidence), note)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gp-cache", default=None)
    a = ap.parse_args()
    if a.gp_cache:
        C.CACHE = Path(a.gp_cache)
    from slots import Pool

    import pdefactor.loop as L
    from pdefactor.learned import budget as B
    from pdefactor.learned.config import Learned

    B._CACHE["lb_exact"] = None
    C._below_normal()
    with Pool() as pool:
        s = None
        while s is None:
            s = pool.try_acquire()
            if s is None:
                time.sleep(5)
        bad = 0
        try:
            for corpus, fam, seed, design in DRAWS:
                inp = C.make_input(corpus, fam, seed, design)
                kw = dict(noise_draws=inp["noise_draws"], raw=inp["raw"], bootstrap=inp["bootstrap"])
                args = (inp["samples"], inp["t"], inp["x"], inp["sigma"], inp["pis"])
                out, secs = {}, {}
                for arm, memo, lrn in (("off", True, None), ("log", False, Learned(budget=True)),
                                       ("memo", True, Learned(budget=True))):
                    B.MEMO = memo
                    t0 = time.perf_counter()
                    with np.errstate(all="ignore"):
                        out[arm] = L.run_loop(*args, learned=lrn, **kw)
                    secs[arm] = time.perf_counter() - t0
                same = {arm: answer(out[arm]) == answer(out["off"]) for arm in ("log", "memo")}
                bad += not all(same.values())
                print(corpus, fam, seed, design, out["off"].label, same,
                      {k: round(v, 1) for k, v in secs.items()}, flush=True)
        finally:
            pool.release(s)
    print("ALL IDENTICAL" if not bad else f"{bad} DRAW(S) DIFFER", flush=True)


if __name__ == "__main__":
    main()
