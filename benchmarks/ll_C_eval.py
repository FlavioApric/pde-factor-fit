"""Live evaluation of the controller C on corpus cases (sessions/LEARNED/C/PLAN.md §7).

One task = one case: run_controlled with the chosen policy and mode. Each task writes two rows in the
ll_corpus format, paired by construction: learned="off" (the controller's own R0, the off pipeline on
the same machine and code) and learned=<arm> (the reported answer), plus the controller fields
(actions, stop reason, accepted, changed, confirmed, visited, missing mass, runtime). --trace records
the would-be output at every loop depth with the stopping rule disabled (forking-paths null test).
LOFO: --policy contextual|table loads the model trained without the case's family.

  python analysis/exp/ll_C_eval.py --corpus G --split test --policy rules --out analysis/exp/out/ll_C_eval_G.jsonl
  python analysis/exp/ll_C_eval.py --corpus N --policy force --mode none --trace --max-loops 20 --out ...
"""
from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import os
import pickle
import sys
import time
import traceback
import warnings
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ll_corpus as LC  # noqa: E402
from ll_C_logs import _jsonable, case_of  # noqa: E402

warnings.filterwarnings("ignore")
MODELS = LC.ROOT / "code" / "pdefactor" / "learned" / "models"


def make_policy(name, family, banned):
    from pdefactor.learned import controller as C

    if name == "rules":
        return C.RulePolicy(K=3, banned=banned)
    if name == "force":  # forced depth: every applicable remedy in a fixed order (null test)
        return C.SequencePolicy([r for r in C.REMEDIES if r not in banned])
    if name in ("table", "contextual"):
        p = MODELS / f"controller_{name}_lofo_{family}.pkl"
        if not p.exists():
            p = MODELS / f"controller_{name}.pkl"
        obj = pickle.loads(p.read_bytes())
        return obj.policy(banned=banned)
    raise ValueError(name)


def full_row(res, inp, base):
    from ll_C_logs import row_of

    row = row_of(res, inp, base)
    d = inp["draw"]
    truth = [] if d is None else list(d.factors)
    if truth:
        row["coef"] = LC.coef_rows(res, truth)
        sp_ = res.split or {}
        row["w_mean"] = np.asarray(sp_.get("w_mean", []), float).tolist()
        row["w_q"] = np.asarray(sp_.get("w_q", []), float).tolist()
        try:
            row["w_true"] = LC.true_weights(inp, truth)
        except Exception:  # noqa: BLE001
            row["w_true"] = None
        if sp_ and row.get("w_true") is not None and res.factors:
            from benchmarks.metrics import coef_dist

            pr = res.pruned()
            row["w_match"] = [min(range(len(pr)), key=lambda k: coef_dist(q, pr[k])) for q in truth]
    return row


def work(args, part, opts):
    corpus, family, seed, design = args
    from pdefactor.learned import controller as C

    case, inp = case_of(corpus, family, seed, tuple(design))
    ident = LC.ident_oracle(inp)
    base = dict(corpus=corpus, family=family or "null", seed=seed, split=LC.split_of(corpus, seed),
                design=list(design), ident=ident, all_ident=bool(all(i[0] for i in ident)) if ident else False)
    pol = make_policy(opts["policy"], family, opts["banned"])
    t0 = time.perf_counter()
    cr = C.run_controlled(case.pool, case.t, case.x, case.sigma, case.pool_pis, raw=case.raw,
                          noise_draws=case.noise_draws, bootstrap=case.bootstrap, n_use=case.n_use, policy=pol,
                          max_loops=opts["max_loops"], mode=opts["mode"], trace=opts["trace"])
    rt = time.perf_counter() - t0
    off = full_row(cr.r0, inp, dict(base, learned="off", runtime=None))
    arm = opts["arm"]
    on = full_row(cr.result, inp, dict(base, learned=arm, runtime=rt, n_actions=cr.n_actions,
                                       actions=cr.actions, stop=cr.stop_reason, accepted=cr.accepted,
                                       changed=cr.changed, confirmed=cr.confirmed, config=cr.config.changed(),
                                       visited=cr.visited, missing_mass=cr.missing_mass))
    if opts["trace"]:
        truth = [] if inp["draw"] is None else list(inp["draw"].factors)
        tr = []
        for t_ in cr.trace:
            r = dict(t_)
            r["category"] = LC.category(dict(label=t_["label"], factors=t_["factors"], truth=[str(q) for q in truth],
                                             ok=False, all_ident=base["all_ident"]))
            tr.append(r)
        on["trace"] = tr
    with open(part, "a") as fh:
        for r in (off, on):
            fh.write(json.dumps({k: _jsonable(v) for k, v in r.items()}, default=str) + "\n")


def _child(args, part, opts):
    LC._below_normal()
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    warnings.filterwarnings("ignore")
    try:
        work(args, part, opts)
    except Exception as e:  # noqa: BLE001
        with open(part, "a") as fh:
            fh.write(json.dumps(dict(corpus=args[0], family=args[1] or "null", seed=args[2], design=list(args[3]),
                                     split=LC.split_of(args[0], args[2]), learned=opts["arm"], label="CRASH",
                                     category="crash", error=f"{type(e).__name__}: {e}",
                                     trace=traceback.format_exc()[-1500:])) + "\n")


def run_all(tasks, out, workers, cap, opts):
    from slots import Pool

    ctx = mp.get_context("spawn")
    pdir = Path(str(out) + ".parts")
    pdir.mkdir(parents=True, exist_ok=True)
    pending, live, pool = list(tasks), [], Pool()
    while pending or live:
        while pending and len(live) < workers:
            slot = pool.try_acquire()
            if slot is None:
                break
            args = pending.pop(0)
            part = pdir / f"{args[0]}_{args[1] or 'null'}_{args[2]}_{args[3][0]}_{args[3][1]:g}_{opts['arm']}.jsonl"
            part.unlink(missing_ok=True)
            p = ctx.Process(target=_child, args=(args, str(part), opts), daemon=True)
            p.start()
            live.append((p, args, part, time.time(), slot))
        time.sleep(1.0)
        still = []
        for p, args, part, ts, slot in live:
            if p.is_alive() and time.time() - ts <= cap:
                still.append((p, args, part, ts, slot))
                continue
            if p.is_alive():
                p.terminate()
                p.join(5)
                with open(part, "a") as fh:
                    fh.write(json.dumps(dict(corpus=args[0], family=args[1] or "null", seed=args[2],
                                             design=list(args[3]), split=LC.split_of(args[0], args[2]),
                                             learned=opts["arm"], label="TIMEOUT", category="timeout",
                                             runtime=cap)) + "\n")
            pool.release(slot)
            rows = part.read_text().splitlines() if part.exists() else []
            with open(out, "a") as fh:
                for line in rows:
                    fh.write(line + "\n")
            print(args, len(rows), "rows", round(time.time() - ts), "s", flush=True)
        live = still


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", required=True, choices=list(LC.SEEDS))
    ap.add_argument("--split", nargs="*", default=["test"])
    ap.add_argument("--families", nargs="*", default=list(LC.FAMILIES))
    ap.add_argument("--designs", nargs="*", type=int, default=None)
    ap.add_argument("--seeds", nargs="*", type=int, default=None)
    ap.add_argument("--policy", default="rules", choices=["rules", "table", "contextual", "force"])
    ap.add_argument("--mode", default="fission", choices=["fission", "single", "none"])
    ap.add_argument("--trace", action="store_true")
    ap.add_argument("--max-loops", type=int, default=20)
    ap.add_argument("--banned", nargs="*", default=None, help="remedies removed by the N null logs (file or names)")
    ap.add_argument("--arm", default=None)
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--cap", type=float, default=6 * 3600.0)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    banned = []
    if a.banned:
        for b in a.banned:
            banned += json.loads(Path(b).read_text()) if Path(b).exists() else [b]
    arm = a.arm or f"C_{a.policy}_{a.mode}" + ("_trace" if a.trace else "")
    opts = dict(policy=a.policy, mode=a.mode, trace=a.trace, max_loops=a.max_loops, banned=banned, arm=arm)
    designs = [LC.DESIGNS[a.corpus][i] for i in (a.designs or range(len(LC.DESIGNS[a.corpus])))]
    seeds = a.seeds or [s for sp in a.split for s in LC.SEEDS[a.corpus][sp]]
    fams = [None] if a.corpus == "N" else a.families
    done = set()
    if Path(a.out).exists():
        for line in Path(a.out).read_text().splitlines():
            r = json.loads(line)
            if r.get("learned") == arm:
                done.add((r["corpus"], r["family"], r["seed"], tuple(r["design"])))
    tasks = [(a.corpus, f, s, list(d)) for s in seeds for d in designs for f in fams
             if (a.corpus, f or "null", s, tuple(d)) not in done]
    print(len(tasks), "cases", arm, flush=True)
    run_all(tasks, a.out, a.workers, a.cap, opts)


if __name__ == "__main__":
    main()
