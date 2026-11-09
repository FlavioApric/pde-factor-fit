"""Randomised remedy logs for the controller C (sessions/LEARNED/C/PLAN.md §6.5).

One task = one corpus case. In one worker (one machine slot, shared memo): the off run, then from the
off state each remedy the off diagnosis indicates (DEFAULT_TABLE order, at most 5) plus one remedy drawn
uniformly from the other applicable ones (propensity recorded). A case whose off answer is already
right gets one uniformly drawn remedy only (it measures harm). --steps K > 1 instead applies one random
sequence of K remedies (multi-step logs). Rows stream to <out>.parts/<case>.jsonl and are merged into
<out> when the case ends (a timed-out case keeps the rows it wrote).

  python analysis/exp/ll_C_logs.py --corpus S --split fit cal --out analysis/exp/out/ll_C_logs_S.jsonl
"""
from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import os
import sys
import time
import traceback
import warnings
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ll_corpus as LC  # noqa: E402  (puts src/ and the repo root on sys.path)

warnings.filterwarnings("ignore")
SHARED_CACHE = Path(r"D:\Larned layers\PDEFactorML\analysis\exp\cache")
MAX_INDICATED = 5
CAP_RUN = 1200.0


def case_of(corpus, family, seed, design):
    """(controller Case, corpus input dict). Scattered: the whole cached pool of GP samples (16),
    the default config uses the corpus's first 8, as ll_corpus.scattered_input."""
    from pdefactor.learned.controller import Case

    inp = LC.make_input(corpus, family, seed, design)
    kind, noise = design
    if inp["raw"] is None:
        return Case(list(inp["samples"]), np.ones(1), inp["t"], inp["x"], inp["sigma"], None, None, 1,
                    inp["bootstrap"]), inp
    tag = "null" if corpus == "N" else family
    p = next(q for q in (LC.CACHE / f"ll_{tag}_{seed}_{kind}_{noise:g}.npz",
                         SHARED_CACHE / f"ll_{tag}_{seed}_{kind}_{noise:g}.npz") if q.exists())
    c = dict(np.load(p))
    return Case(list(c["samples"]), c["weights"] / c["weights"].sum(), inp["t"], inp["x"], 0.0, inp["raw"], "gp",
                LC.S_LOOP, 0), inp


def row_of(res, inp, base):
    from pdefactor.simulator import match

    d = inp["draw"]
    truth = [] if d is None else list(d.factors)
    facs = res.pruned()
    ok, err = match(truth, facs) if (facs and truth) else (False, float("inf"))
    row = dict(base, label=res.label, factors=[str(q) for q in facs], ok=bool(ok), err=float(err),
               truth=[str(q) for q in truth], note=res.note,
               p_top=float(max(res.structures.values())) if res.structures else None)
    row["all_ident"] = base["all_ident"]
    row["equiv"] = bool(not ok and truth and facs and LC.equivalent(truth, facs, inp))
    row["category"] = LC.category(row)
    return row


def _jsonable(v):
    if isinstance(v, (set, frozenset)):
        return sorted(v)
    if isinstance(v, (np.floating, np.integer)):
        return v.item()
    return v


def work(args, part):
    corpus, family, seed, design, steps = args
    from pdefactor.learned import controller as C
    from pdefactor.learned.memo import Memo
    from pdefactor.learned.runconfig import DEFAULT

    case, inp = case_of(corpus, family, seed, tuple(design))
    ident = LC.ident_oracle(inp)
    base = dict(corpus=corpus, family=family or "null", seed=seed, split=LC.split_of(corpus, seed),
                design=list(design), ident=ident, all_ident=bool(all(i[0] for i in ident)) if ident else False)
    rng = np.random.default_rng(C.case_seed(case))
    memo = Memo()

    def emit(row):
        with open(part, "a") as fh:
            fh.write(json.dumps({k: _jsonable(v) for k, v in row.items()}, default=str) + "\n")

    t0 = time.perf_counter()
    r0 = C.run_config(case, DEFAULT, memo)
    rt0 = time.perf_counter() - t0
    d0, f0 = C.diagnose(r0, case, DEFAULT)
    off = row_of(r0, inp, dict(base, step=0, remedy=None, runtime=rt0, diags=sorted(d0), feats=f0,
                               early_stop=C.early_stop(r0, f0)))
    emit(off)
    st = C.State(d0, f0, [], 0, DEFAULT, case, 0.0, np.inf)
    appl = C.applicable(st)
    if steps > 1:  # one random sequence from the off state, cumulative configs
        cfg, tried, d, f = DEFAULT, [], d0, f0
        for k in range(steps):
            st = C.State(d, f, tried, k, cfg, case, 0.0, np.inf)
            ok_ = C.applicable(st)
            if not ok_:
                break
            r = ok_[int(rng.integers(len(ok_)))]
            tried.append(r)
            cfg = C._delta(r, cfg, case)
            t1 = time.perf_counter()
            res = C.run_config(case, cfg, memo)
            d, f = C.diagnose(res, case, cfg)
            emit(row_of(res, inp, dict(base, step=k + 1, remedy=r, sequence=list(tried), propensity=1 / len(ok_),
                                       kind="sequence", runtime=time.perf_counter() - t1, prev_diags=sorted(st.diags),
                                       prev_feats=st.feats, diags=sorted(d), feats=f, config=cfg.changed(),
                                       off_category=off["category"])))
        return
    plan = []
    if off["category"] in ("right", "equivalent"):
        if appl:
            plan.append((appl[int(rng.integers(len(appl)))], "random", 1 / len(appl)))
    else:
        ind = []
        for dg in C.DIAGNOSES:
            if dg in d0:
                ind += [r for r in C.DEFAULT_TABLE.get(dg, []) if r in appl and r not in ind]
        ind = ind[:MAX_INDICATED]
        plan += [(r, "indicated", 1.0) for r in ind]
        rest = [r for r in appl if r not in ind]
        if rest:
            plan.append((rest[int(rng.integers(len(rest)))], "random", 1 / len(rest)))
    for r, kind, prop in plan:
        cfg = C._delta(r, DEFAULT, case)
        t1 = time.perf_counter()
        try:
            res = C.run_config(case, cfg, memo)
        except Exception as e:  # noqa: BLE001
            emit(dict(base, step=1, remedy=r, kind=kind, propensity=prop, label="CRASH", category="crash",
                      error=repr(e), off_category=off["category"]))
            continue
        d, f = C.diagnose(res, case, cfg)
        emit(row_of(res, inp, dict(base, step=1, remedy=r, kind=kind, propensity=prop, n_applicable=len(appl),
                                   runtime=time.perf_counter() - t1, prev_diags=sorted(d0), prev_feats=f0,
                                   diags=sorted(d), feats=f, config=cfg.changed(), off_category=off["category"],
                                   memo_hits=memo.hits)))


def _child(args, part):
    LC._below_normal()
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    warnings.filterwarnings("ignore")
    try:
        work(args, part)
    except Exception as e:  # noqa: BLE001
        with open(part, "a") as fh:
            fh.write(json.dumps(dict(corpus=args[0], family=args[1] or "null", seed=args[2], design=list(args[3]),
                                     step=-1, label="CRASH", error=f"{type(e).__name__}: {e}",
                                     trace=traceback.format_exc()[-1500:])) + "\n")


def part_name(out, args):
    corpus, family, seed, design, steps = args
    return Path(str(out) + ".parts") / f"{corpus}_{family or 'null'}_{seed}_{design[0]}_{design[1]:g}_k{steps}.jsonl"


def run_all(tasks, out, workers, cap_case):
    from slots import Pool

    ctx = mp.get_context("spawn")
    Path(str(out) + ".parts").mkdir(parents=True, exist_ok=True)
    pending, live, pool = list(tasks), [], Pool()
    while pending or live:
        while pending and len(live) < workers:
            slot = pool.try_acquire()
            if slot is None:
                break
            args = pending.pop(0)
            part = part_name(out, args)
            part.unlink(missing_ok=True)
            p = ctx.Process(target=_child, args=(args, str(part)), daemon=True)
            p.start()
            live.append((p, args, part, time.time(), slot))
        time.sleep(1.0)
        still = []
        for p, args, part, ts, slot in live:
            timeout = time.time() - ts > cap_case
            if p.is_alive() and not timeout:
                still.append((p, args, part, ts, slot))
                continue
            if p.is_alive():
                p.terminate()
                p.join(5)
                with open(part, "a") as fh:
                    fh.write(json.dumps(dict(corpus=args[0], family=args[1] or "null", seed=args[2],
                                             design=list(args[3]), step=-1, label="TIMEOUT", runtime=cap_case)) + "\n")
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
    ap.add_argument("--split", nargs="*", default=["fit"])
    ap.add_argument("--families", nargs="*", default=list(LC.FAMILIES))
    ap.add_argument("--designs", nargs="*", type=int, default=None)
    ap.add_argument("--seeds", nargs="*", type=int, default=None)
    ap.add_argument("--steps", type=int, default=1)
    ap.add_argument("--frac", type=float, default=1.0, help="fraction of the cases (deterministic subset)")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    designs = [LC.DESIGNS[a.corpus][i] for i in (a.designs or range(len(LC.DESIGNS[a.corpus])))]
    seeds = a.seeds or [s for sp in a.split for s in LC.SEEDS[a.corpus][sp]]
    fams = [None] if a.corpus == "N" else a.families
    done = set()
    if Path(a.out).exists():
        for line in Path(a.out).read_text().splitlines():
            r = json.loads(line)
            done.add((r["corpus"], r["family"], r["seed"], tuple(r["design"])))
    tasks = []
    for s in seeds:  # seed-major: every family and design early
        for d in designs:
            for f in fams:
                if (a.corpus, f or "null", s, tuple(d)) in done:
                    continue
                tasks.append((a.corpus, f, s, list(d), a.steps))
    if a.frac < 1:  # hash() is salted per process: use a stable subset instead
        rng = np.random.default_rng(12345)
        tasks = [t for t in tasks if rng.random() < a.frac]
    print(len(tasks), "cases", flush=True)
    cap_case = CAP_RUN * (2 + (MAX_INDICATED + 1 if a.steps == 1 else a.steps) / 2)
    run_all(tasks, a.out, a.workers, cap_case)


if __name__ == "__main__":
    main()
