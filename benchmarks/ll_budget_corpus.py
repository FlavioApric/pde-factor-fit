"""S-LEARNED-LB corpus runs (sessions/LEARNED/LB/PLAN.md §5) through the common harness `ll_corpus.py`.

Arms (added to ll_corpus.LEARNED in each worker, the harness file is not edited):
  lblog  Learned(budget=True) with no model: the guards record their features and never skip, so the
         answer is the off run's (tests/test_learned_budget.py); the rows are the LB training data and
         carry the tightened `changed` bit
  lb     Learned(budget="exact") with the fitted model `--model` (else no model: log-only)
  lbfast Learned(budget="fast") with the fitted model `--model-fast` (harmed <= 2 %, training/screening only)
  --log-as-off  the lblog arm is written as `learned = "off"` rows (with `lb_log = True`), with the LB memo
         switched off (budget.MEMO = False), so the rows are the off arm itself: same answers, off
         runtime; they replace a separate off run of the same draws (parent session, 2026-10-29)
Each row gets `lb` = {"features": {step: {...}}, "skipped": [...]} and `lp_trace` (every V0.1 lp computed
by loop._pred_logp, in call order; recipe copied from learned/constants.recording on the L2d branch).
--gp-cache DIR points ll_corpus's GP cache at DIR (S corpus: the shared cache, deterministic fits).
--tripwire N  with --log-as-off, the first N rows that finish within TRIP_MAX_S also run plain off
         (learned=None) in the same worker and compare label, factor strings, coefficient reprs and
         evidence; a mismatch writes TRIPWIRE_FAILED next to the output and every later task returns
         a CRASH row at once (parent session, 2026-10-30)

Usage: python ll_budget_corpus.py --corpus G --split fit cal --learned lblog --out analysis/exp/out/ll_lb_G.jsonl
       [--workers 4] [--cap 1200] [--families ...] [--designs ...] [--seeds ...] [--model path]
"""
from __future__ import annotations

import os

for _v in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import argparse
import json
import pickle
import sys
import traceback
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import ll_corpus as C  # noqa: E402

ARMS = {"lblog": dict(budget=True), "lb": dict(budget="exact"), "lbfast": dict(budget="fast")}
MODEL_ENV = "LB_MODEL"            # lb arm: the exact-profile model
MODEL_FAST_ENV = "LB_MODEL_FAST"  # lbfast arm: the fast-profile model
LOG_AS_OFF_ENV = "LB_LOG_AS_OFF"
GP_CACHE_ENV = "LB_GP_CACHE"
PART_ENV = "LB_PARTIAL_DIR"
TRIP_ENV = "LB_TRIPWIRE"
TRIP_MAX_S = 300.0


def _answer(r):
    coef = [{str(k): tuple(repr(complex(c)) for c in v) for k, v in f.coef.items()} for f in r.factors]
    return r.label, [str(f.sympy) for f in r.factors], coef, repr(r.evidence)


def _trip_slot(tdir, n):
    """Claim one of the n tripwire slots (exclusive file creation); False when all are taken."""
    for i in range(n):
        try:
            (tdir / f"slot{i}").open("x").close()
            return True
        except FileExistsError:
            continue
    return False


def _child(conn, args):
    C._below_normal()
    warnings.filterwarnings("ignore")
    C.LEARNED.update(ARMS)
    import pdefactor.loop as L
    from pdefactor.learned import budget as B

    if os.environ.get(GP_CACHE_ENV):
        C.CACHE = Path(os.environ[GP_CACHE_ENV])
    ln = args[4]
    as_off = ln == "off" and os.environ.get(LOG_AS_OFF_ENV) == "1"
    trip = os.environ.get(TRIP_ENV)
    tdir, ntrip = (Path(trip.split("|")[0]), int(trip.split("|")[1])) if trip else (None, 0)
    if tdir is not None and (tdir / "TRIPWIRE_FAILED").exists():
        corpus, family, seed, design, ln0 = args
        conn.send(dict(corpus=corpus, family=family or "null", seed=seed, split=C.split_of(corpus, seed),
                       design=list(design), learned=ln0, label="CRASH", ok=False, err=float("inf"),
                       error="tripwire: an earlier log-as-off row differed from off"))
        conn.close()
        return
    if as_off:  # log-only LB under the off name: guards record, never skip, no memo
        C.LEARNED["off"] = dict(budget=True)
        B.MEMO = False
        ln = "lblog"
    for arm, env, name in (("lb", MODEL_ENV, "lb_exact"), ("lbfast", MODEL_FAST_ENV, "lb_fast")):
        B._CACHE[name] = (pickle.loads(Path(os.environ[env]).read_bytes())
                          if ln == arm and os.environ.get(env) else None)
    last = {}
    orig = L.run_loop

    def run_loop(*a, **k):
        last.setdefault("call", (a, k))  # the outermost call is the first one
        last["res"] = orig(*a, **k)
        return last["res"]

    L.run_loop = run_loop
    lps, o_lp = [], L._pred_logp  # lp_trace (as learned/constants.recording on the L2d branch)

    def rec(*a, **k):
        v = o_lp(*a, **k)
        lps.append(float(v))
        return v

    L._pred_logp = rec
    # a run killed at the cap still leaves its top-level step marks and guard features (merge_partial)
    part = Path(os.environ[PART_ENV]) / ("_".join(str(v) for v in (args[1] or "null", args[2], *args[3], args[4])) + ".jsonl")
    part.write_text("")
    o_mark, o_feat = L._Steps.mark, B.features

    def mark(self, name, note="", fp=None, changed=None):
        o_mark(self, name, note, fp, changed)
        if self is top.setdefault("log", self):
            with open(part, "a") as fh:
                fh.write(json.dumps(dict(kind="step", row=list(self.rows[-1]))) + "\n")

    def features(step, **kw):
        f = o_feat(step, **kw)
        with open(part, "a") as fh:
            fh.write(json.dumps(dict(kind="features", step=step, f=f)) + "\n")
        return f

    top = {}
    L._Steps.mark, B.features = mark, features
    try:
        row = C.run_one(*args)
        res = last.get("res")
        row["lb"] = getattr(res, "lb", {}) if res is not None else {}
        row["lb_model"] = {"lb": os.environ.get(MODEL_ENV), "lbfast": os.environ.get(MODEL_FAST_ENV)}.get(ln)
        row["lp_trace"] = lps
        row["lb_log"] = as_off
        row["sha"] = os.environ.get("LB_SHA")  # git sha of the pipeline that produced the row
        # exact answer (factor strings, coefficient reprs, evidence, factor reports) for ll_budget_harm.py
        row["lb_answer"] = repr((_answer(res), L._canon(res.factors))) if res is not None else None
        if (as_off and tdir is not None and res is not None and row.get("runtime", 1e9) <= TRIP_MAX_S
                and _trip_slot(tdir, ntrip)):
            import numpy as np

            a_, k_ = last["call"]
            B.MEMO = True
            L._pred_logp = o_lp
            with np.errstate(all="ignore"):
                ref = orig(*a_, **{**k_, "learned": None})
            row["tripwire"] = same = _answer(ref) == _answer(res)
            if not same:
                (tdir / "TRIPWIRE_FAILED").write_text(json.dumps([str(v) for v in args]))
        conn.send(row)
    except Exception as e:  # noqa: BLE001  (a crash is a reported failure)
        corpus, family, seed, design, ln = args
        conn.send(dict(corpus=corpus, family=family or "null", seed=seed, split=C.split_of(corpus, seed),
                       design=list(design), learned=ln, label="CRASH", ok=False, err=float("inf"),
                       error=f"{type(e).__name__}: {e}", trace=traceback.format_exc()[-1500:]))
    conn.close()


def merge_partial(out):
    """TIMEOUT rows get `steps` and `lb` from the streamed partial log (steps completed before the cap)."""
    pdir = Path(str(out) + ".partial")
    lines = Path(out).read_text().splitlines() if Path(out).exists() else []
    rows = [json.loads(s) for s in lines if s.strip()]
    for r in rows:
        if r.get("label") != "TIMEOUT" or r.get("steps"):
            continue
        p = pdir / ("_".join(str(v) for v in (r["family"], r["seed"], *r["design"], r["learned"])) + ".jsonl")
        if not p.exists():
            continue
        ev = [json.loads(s) for s in p.read_text().splitlines() if s.strip()]
        r["steps"] = [e["row"] for e in ev if e["kind"] == "step"]
        r["lb"] = dict(features={e["step"]: e["f"] for e in ev if e["kind"] == "features"}, skipped=[], partial=True)
    Path(out).write_text("".join(json.dumps(r, default=str) + "\n" for r in rows))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", required=True, choices=list(C.SEEDS))
    ap.add_argument("--split", nargs="*", default=["fit", "cal"])
    ap.add_argument("--families", nargs="*", default=list(C.FAMILIES))
    ap.add_argument("--designs", nargs="*", type=int, default=None)
    ap.add_argument("--seeds", nargs="*", type=int, default=None)
    ap.add_argument("--learned", nargs="*", default=["lblog"])
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--cap", type=float, default=C.CAP_S)
    ap.add_argument("--model", default=None)
    ap.add_argument("--model-fast", default=None)
    ap.add_argument("--log-as-off", action="store_true")
    ap.add_argument("--gp-cache", default=None)
    ap.add_argument("--tripwire", type=int, default=0)
    ap.add_argument("--match", nargs="*", default=None,
                    help="only draws that have an off row in these files (pairs with another session's off arm)")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    if a.model:
        os.environ[MODEL_ENV] = str(Path(a.model).resolve())
    if a.model_fast:
        os.environ[MODEL_FAST_ENV] = str(Path(a.model_fast).resolve())
    if a.log_as_off:
        os.environ[LOG_AS_OFF_ENV] = "1"
    if a.gp_cache:
        os.environ[GP_CACHE_ENV] = str(Path(a.gp_cache).resolve())
    if not os.environ.get("LB_SHA"):  # a frozen copy outside git sets LB_SHA itself
        import subprocess

        try:
            os.environ["LB_SHA"] = subprocess.run(["git", "-c", "safe.directory=*", "rev-parse", "--short", "HEAD"],
                                                  cwd=Path(__file__).parent, capture_output=True,
                                                  text=True).stdout.strip()
        except OSError:
            pass
    designs = C.DESIGNS[a.corpus]
    designs = [designs[i] for i in a.designs] if a.designs is not None else designs
    fams = [None] if a.corpus == "N" else a.families
    seeds = a.seeds if a.seeds else [s for sp_ in a.split for s in C.SEEDS[a.corpus][sp_]]
    done = C.done_keys(a.out)
    # arms innermost: the off and lb runs of a draw start side by side (paired runtime, same machine load)
    tasks = [(a.corpus, f, s, d, ln) for d in designs for f in fams for s in seeds for ln in a.learned
             if (a.corpus, f or "null", s, tuple(d), ln) not in done]
    if a.match:
        keep = {(r["family"], r["seed"], tuple(r["design"])) for p in a.match for line in Path(p).read_text().splitlines()
                if line.strip() and (r := json.loads(line)).get("learned") == "off"}
        tasks = [t for t in tasks if (t[1] or "null", t[2], tuple(t[3])) in keep]
    # slow families last would idle slots at the end; interleave so long runs start early
    tasks.sort(key=lambda t: (-(t[1] in ("F3", "F4", "F5")), t[2]))
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    print(f"{len(tasks)} tasks -> {a.out}", flush=True)
    pdir = Path(str(a.out) + ".partial")
    pdir.mkdir(parents=True, exist_ok=True)
    os.environ[PART_ENV] = str(pdir.resolve())
    if a.tripwire and a.log_as_off:
        tdir = Path(str(a.out) + ".tripwire")
        tdir.mkdir(parents=True, exist_ok=True)
        os.environ[TRIP_ENV] = f"{tdir.resolve()}|{a.tripwire}"
    C._child = _child
    C.run_all(tasks, a.out, workers=a.workers, cap=a.cap)
    merge_partial(a.out)
    if a.tripwire and a.log_as_off and (Path(str(a.out) + ".tripwire") / "TRIPWIRE_FAILED").exists():
        sys.exit("tripwire: log-as-off differs from off; rows after the failure are CRASH")


if __name__ == "__main__":
    main()
