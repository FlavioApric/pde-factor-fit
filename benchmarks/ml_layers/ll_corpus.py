"""S-LEARNED corpora (sessions/LEARNED/PLAN.md §2.2): the pipeline on random PDEs from
pdefactor.simulator, one jsonl row per run, with a learned-layer configuration.

Corpora (seeds fixed in PLAN.md, never changed):
  G  noisy grid, families F1-F5, noise 1 % / 5 %, bootstrap B = 16 (the benchmark's grid path)
  S  scattered: 400 pts @ 5 %, 2000 pts @ 1 %, GP posterior (fit_gp, S = 16), raw observations
  N  pure noise: grids and 400-pt scattered sets with no PDE in them

Each run executes in its own process (spawn) at below-normal priority, with a wall-clock cap; a run
that hits the cap is recorded as TIMEOUT in both arms of a comparison alike.

Usage:
  python ll_corpus.py --corpus G --split fit --learned off --workers 4 --out analysis/exp/out/ll_G_off.jsonl
"""
from __future__ import annotations

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")  # one BLAS thread per worker: the machine is shared

import argparse
import json
import multiprocessing as mp
import sys
import time
import traceback
import warnings
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).parent))
warnings.filterwarnings("ignore")

FAMILIES = ("F1", "F2", "F3", "F4", "F5")
SEEDS = {
    "G": dict(fit=range(100, 120), cal=range(120, 128), test=range(128, 136)),
    "S": dict(fit=range(200, 207), cal=range(207, 209), test=range(209, 212)),
    "N": dict(fit=range(300, 310), cal=range(310, 315), test=range(315, 320)),
    "I": dict(fit=range(400, 402), cal=range(402, 403), test=range(403, 404)),  # injected failures (V1)
    # P7 (2026-10-31): fresh clean 5 % grid draws for V1's conformal gate (>= 19 clean cal rows per LOFO fold)
    "V": dict(fit=range(600, 608), cal=range(608, 616), test=range(616, 620)),
}
DESIGNS = {"G": [("grid", 0.01), ("grid", 0.05)], "S": [(400, 0.05), (2000, 0.01)],
           "N": [("grid", 1.0), (400, 1.0)],
           "V": [("grid", 0.05)],
           # corpus I: design "<type>:<level>" on the G grid at 5 % noise (ll_inject.py; failure targets only)
           "I": [(f"{k}:{lv}", 0.05) for k in ("two_laws", "coloured", "heteroscedastic", "nonlinear", "varcoef",
                                                  "fractional", "aliasing") for lv in range(3)]}
CAP_S = 1200.0
BOOT = int(os.environ.get("LL_BOOT", "16"))  # LL_BOOT=0: screening runs only (SPEEDUP §6), never a gate
S_GP = 16
S_LOOP = 8
CACHE = ROOT / "analysis" / "exp" / "cache"


def split_of(corpus, seed):
    for name, rg in SEEDS[corpus].items():
        if seed in rg:
            return name
    return "other"


# ------------------------------------------------------------------ inputs
def grid_input(family, seed, noise):
    from pdefactor.simulator import random_pde
    from pdefactor.synthetic import grid

    d = random_pde(family, seed)
    t, x, u = grid(d.field)
    rng = np.random.default_rng(1000 + seed)  # as e13_random_pdes.run_one
    sig = noise * np.std(u)
    un = u + sig * rng.standard_normal(u.shape)
    return dict(draw=d, t=t, x=x, u=u, samples=[un], pis=None, sigma=sig, noise_draws=None, raw=None,
                bootstrap=BOOT, grid_data=un, grid_sigma=sig)


def _gp(ts, xs, ys, t, x, L, seed):
    from pdefactor.interp.gp import fit_gp

    cplx = np.iscomplexobj(ys)
    parts = [ys.real, ys.imag] if cplx else [ys]
    fits = [fit_gp(ts, xs, y, grid=(t, x), period_x=L, S=S_GP, seed=seed) for y in parts]
    if cplx:
        return fits[0].samples + 1j * fits[1].samples, fits[0].weights * fits[1].weights
    return fits[0].samples, fits[0].weights


def scattered_input(family, seed, n, noise, null=False):
    from benchmarks.bench_e2e import smooth_noise
    from pdefactor.simulator import random_pde
    from pdefactor.synthetic import grid

    L = 2 * np.pi
    if null:
        d = None
        t, x = np.linspace(0, 2.0, 64), np.linspace(0, L, 128, endpoint=False)
        u = np.zeros((64, 128))
    else:
        d = random_pde(family, seed)
        t, x, u = grid(d.field)
    tag = "null" if null else family
    p = CACHE / f"ll_{tag}_{seed}_{n}_{noise:g}.npz"
    if p.exists():
        c = dict(np.load(p))
    else:
        rng = np.random.default_rng(7919 * seed + n)
        ts, xs = rng.uniform(0, t[-1], n), rng.uniform(0, L, n)
        sig = noise if null else noise * float(np.std(u))
        ys = (np.zeros(n) if null else d.field(ts, xs)) + sig * rng.standard_normal(n)
        S, w = _gp(ts, xs, ys, t, x, L, seed)
        c = dict(samples=S, weights=w / w.sum(), ts=ts, xs=xs, ys=ys, sigma=sig)
        p.parent.mkdir(parents=True, exist_ok=True)
        tmp = p.with_name(f"{p.stem}.{os.getpid()}.tmp.npz")  # both arms of a pair may fit it at once
        np.savez(tmp, **c)
        os.replace(tmp, p)
    S, w = c["samples"][:S_LOOP], c["weights"][:S_LOOP]
    w = w / w.sum()
    mean = np.tensordot(w, S, 1)
    return dict(draw=d, t=t, x=x, u=u, samples=list(S), pis=w, sigma=0.0,
                noise_draws=np.sqrt(2) * (S - mean[None]),
                raw=dict(ts=c["ts"], xs=c["xs"], ys=c["ys"], period=L, sigma=float(c["sigma"])),
                bootstrap=0, grid_data=mean, grid_sigma=smooth_noise(S, w), n_obs=n,
                obs_sigma=float(c["sigma"]))


def null_grid_input(seed):
    t, x = np.linspace(0, 2.0, 64), np.linspace(0, 2 * np.pi, 128, endpoint=False)
    rng = np.random.default_rng(5000 + seed)
    un = rng.standard_normal((64, 128))
    return dict(draw=None, t=t, x=x, u=np.zeros_like(un), samples=[un], pis=None, sigma=1.0, noise_draws=None,
                raw=None, bootstrap=BOOT, grid_data=un, grid_sigma=1.0)


def make_input(corpus, family, seed, design):
    kind, noise = design
    if corpus == "I":
        from ll_inject import inject_input

        typ, lv = kind.split(":")
        return inject_input(typ, int(lv), family, seed, noise)
    if corpus == "N":
        return null_grid_input(seed) if kind == "grid" else scattered_input(None, seed, kind, noise, null=True)
    if kind == "grid":
        return grid_input(family, seed, noise)
    return scattered_input(family, seed, kind, noise)


# ------------------------------------------------------------------ truth-side quantities
def ident_oracle(inp):
    """Main's truth-only identifiability oracle (e13_random_pdes.identifiable). For scattered data
    the grid formula is used with the noise of an equivalent grid, sigma * sqrt(nt nx / n)."""
    from e13_random_pdes import identifiable

    d = inp["draw"]
    if d is None:
        return []
    t, x = inp["t"], inp["x"]
    sig = inp["grid_sigma"] if inp["raw"] is None else inp["obs_sigma"] * np.sqrt(len(t) * len(x) / inp["n_obs"])
    return [[bool(a), int(b), int(c), float(z)] for a, b, c, z in identifiable(d, t, x, sig)]


def coef_rows(res, truth):
    """Per true factor matched to the nearest reported one: (factor index, monomial, true, mean, lo,
    hi) for every monomial of either (an absent monomial has interval [0, 0]); complex parts kept."""
    from benchmarks.metrics import coef_dist
    from e1_noise import coef_vec

    out = []
    if not res.factors:
        return out
    for i, q in enumerate(truth):
        j = min(range(len(res.factors)), key=lambda k: coef_dist(q, res.factors[k].sympy))
        f = res.factors[j]
        tv = coef_vec(q, 0, 0)
        for mon in sorted(set(tv) | set(f.coef)):
            v = complex(tv.get(mon, 0))
            mean, lo, hi = (complex(z) for z in f.coef.get(mon, (0j, 0j, 0j)))
            out.append(dict(true_i=i, rep_j=j, mon=list(mon), true=[v.real, v.imag], mean=[mean.real, mean.imag],
                            lo=[lo.real, lo.imag], hi=[hi.real, hi.imag]))
    return out


def true_weights(inp, truth):
    """Weights of the true factors from the field's components (Field.weights); a complex factor
    and its conjugate share their component (a real field's mode set), so their weight is split
    in half. None where a factor has no component."""
    import sympy as sp

    d = inp["draw"]
    TT, XX = np.meshgrid(inp["t"], inp["x"], indexing="ij")
    w = d.field.weights(TT, XX)
    out = []
    for q in truth:
        hit = None
        for c, wc in zip(d.field.components, w):
            cq = sp.expand(c.Q)
            conj = sp.expand(sp.conjugate(cq).subs({sp.conjugate(sp.Symbol("tau")): sp.Symbol("tau")}))
            if sp.expand(cq - q) == 0:
                hit = float(wc)
            elif sp.expand(sp.conjugate(c.Q) - q) == 0 or sp.expand(conj - q) == 0:
                hit = float(wc)
        out.append(hit)
    # a conjugate pair listed as two factors shares one component
    names = [str(q) for q in truth]
    return out if all(v is not None for v in out) and len(names) == len(set(names)) else None


def equivalent(truth, facs, inp):
    """e13_summary.equivalent on this run's data: the same product polynomial as the truth, or a
    V0.1 chi^2 excess over the truth <= DCHI2_EQUIV on the data the pipeline saw (the noisy grid, or
    the GP posterior mean with its smoothed noise level)."""
    import sympy as sp
    from e13_summary import DCHI2_EQUIV

    from pdefactor.simulator import match
    from pdefactor.validate import predictive_bins

    if match([sp.expand(sp.Mul(*truth))], [sp.expand(sp.Mul(*facs))])[0]:
        return True
    u, t, x, sig = inp["grid_data"], inp["t"], inp["x"], inp["grid_sigma"]
    try:
        c_f = sum(b[1] for b in predictive_bins(facs, u, t, x, sig))
        c_t = sum(b[1] for b in predictive_bins(truth, u, t, x, sig))
    except Exception:  # noqa: BLE001
        return False
    return bool(c_f - c_t <= DCHI2_EQUIV)


ABSTAIN = ("ID-KER", "UNDECIDED")


def category(row):
    """e13_summary.classify for one row; on a null (no truth) every FIT-COMPATIBLE answer with a
    factor is false-confident and every other label is a correct abstention."""
    lab = row["label"]
    if not row["truth"]:
        return "false-confident" if lab == "FIT-COMPATIBLE" and row["factors"] else "abstain-ok"
    if row["ok"]:
        return "right"
    if row.get("equiv"):
        return "equivalent"
    if lab.startswith(ABSTAIN):
        return "abstain-ok" if not row["all_ident"] else "abstain"
    if lab == "FIT-COMPATIBLE":
        return "false-confident"
    return "other"


# ------------------------------------------------------------------ one run
def _features(res, inp):
    from pdefactor.learned import features as F
    from pdefactor.validate import validate

    row = {}
    try:
        row["run"] = F.run_features(res)
    except Exception as e:  # noqa: BLE001
        row["run_err"] = repr(e)
    try:
        rep = validate(res, inp["grid_data"], inp["t"], inp["x"], inp["grid_sigma"])
        row["v0"] = rep.features()
        row["v0_flags"] = [c for c, _ in rep.flags]
    except Exception as e:  # noqa: BLE001
        row["v0_err"] = repr(e)
    try:
        row["factor_feats"] = [F.interval_features(res, j) for j in range(len(res.factors))]
    except Exception as e:  # noqa: BLE001
        row["factor_err"] = repr(e)
    try:
        from pdefactor.loop import l2c_data

        row["export"] = F.export_features(res, l2c_data(inp["samples"], np.ones(len(inp["samples"])) if inp["pis"] is None else inp["pis"], inp["t"], inp["x"], inp["sigma"],
                                                       inp["noise_draws"], inp["raw"]))
    except Exception as e:  # noqa: BLE001
        row["export_err"] = repr(e)
    try:  # V1 residual diagnostics (learned/resid.py): deterministic, no fit, never fails a row
        from pdefactor.learned.resid import diagnostics

        row["resid"] = diagnostics(res.factors, inp["grid_data"], inp["t"], inp["x"])
    except Exception as e:  # noqa: BLE001
        row["resid"] = None
        row["resid_err"] = repr(e)
    return row


def run_one(corpus, family, seed, design, learned_name):
    from pdefactor.learned.config import Learned
    from pdefactor.loop import run_loop
    from pdefactor.simulator import match

    if learned_name == "nomemo":  # LB re-gate (P7): today's off pipeline with the default exact memo switched off
        from pdefactor.learned import budget

        budget.MEMO_DEFAULT = False
    learned = (Learned(**LEARNED[learned_name]) if learned_name not in ("none", "nomemo") and not learned_name.startswith("act:")
               else None)
    inp = make_input(corpus, family, seed, design)
    d = inp["draw"]
    truth = [] if d is None else list(d.factors)
    row = dict(corpus=corpus, family=family or "null", seed=seed, split=split_of(corpus, seed),
               design=[design[0], design[1]], learned=learned_name, truth=[str(q) for q in truth],
               amp_law=None if d is None else d.amp_law, n_kappa=None if d is None else len(d.kappas))
    if "inject" in inp:
        row["inject"] = inp["inject"]
    row["ident"] = ident_oracle(inp)
    row["all_ident"] = bool(all(i[0] for i in row["ident"])) if row["ident"] else False
    t0 = time.perf_counter()
    with np.errstate(all="ignore"):
        import copy  # main's run_loop mutates its inputs on the scattered path: give it copies

        c = copy.deepcopy({k: inp[k] for k in ("samples", "t", "x", "pis", "noise_draws", "raw")})
        if learned_name.startswith("act:"):  # controller C' oracle sweep (ll_Cprime.py): one action, full settings
            from ll_Cprime import run_action

            res = run_action(learned_name[4:], dict(inp, **c))
        else:
            res = run_loop(c["samples"], c["t"], c["x"], inp["sigma"], c["pis"], noise_draws=c["noise_draws"],
                           raw=c["raw"], bootstrap=inp["bootstrap"], learned=learned)
    row["runtime"] = time.perf_counter() - t0
    row["bootstrap"] = inp["bootstrap"]
    facs = res.pruned()
    ok, err = match(truth, facs) if (facs and truth) else (False, float("inf"))
    sp_ = res.split or {}
    row.update(label=res.label, factors=[str(q) for q in facs], ok=bool(ok), err=float(err),
               structures={str(k): float(v) for k, v in (res.structures or {}).items()},
               p_top=float(max(res.structures.values())) if res.structures else None,
               note=res.note, steps=getattr(res, "steps", []),
               w_mean=np.asarray(sp_.get("w_mean", []), float).tolist(),
               w_q=np.asarray(sp_.get("w_q", []), float).tolist())
    row["equiv"] = bool(not ok and truth and facs and equivalent(truth, facs, inp))
    row["category"] = category(row)
    if truth:
        row["coef"] = coef_rows(res, truth)
        try:
            row["w_true"] = true_weights(inp, truth)
        except Exception:  # noqa: BLE001
            row["w_true"] = None
        if sp_ and row["w_true"] is not None and res.factors:
            from benchmarks.metrics import coef_dist

            pr = res.pruned()
            row["w_match"] = [min(range(len(pr)), key=lambda k: coef_dist(q, pr[k])) for q in truth]
    row.update(_features(res, inp))
    return row


# ------------------------------------------------------------------ learned configurations by name
LEARNED = {
    "off": {},
    "highk": dict(highk="scan"),
    "intervals": dict(intervals="coef"),
    "intervals_w": dict(intervals="coef+weights"),
}


def _below_normal():
    if sys.platform == "win32":
        import ctypes

        ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x00004000)
    else:
        os.nice(10)


def _child(conn, args):
    _below_normal()
    warnings.filterwarnings("ignore")
    try:
        conn.send(run_one(*args))
    except Exception as e:  # noqa: BLE001  (a crash is a reported failure)
        corpus, family, seed, design, ln = args
        conn.send(dict(corpus=corpus, family=family or "null", seed=seed, split=split_of(corpus, seed),
                       design=list(design), learned=ln, label="CRASH", ok=False, err=float("inf"),
                       error=f"{type(e).__name__}: {e}", trace=traceback.format_exc()[-1500:]))
    conn.close()


def run_all(tasks, out, workers=4, cap=CAP_S, on_row=None, should_stop=None, cap_of=None):
    """on_row(row) may edit a finished row before it is written (fastrun: sha stamp, online updates);
    should_stop() true launches no further task (running ones finish); cap_of(args) gives a per-task cap."""
    ctx = mp.get_context("spawn")
    pending = list(tasks)
    live = []  # (proc, conn, args, t_start)
    from slots import Pool  # machine-wide CPU slots shared across sessions

    pool = Pool()
    while pending or live:
        if should_stop is not None and pending and should_stop():
            pending.clear()
        while pending and len(live) < workers:
            slot = pool.try_acquire()
            if slot is None:
                break
            args = pending.pop(0)
            a, b = ctx.Pipe(duplex=False)
            p = ctx.Process(target=_child, args=(b, args), daemon=True)
            p.start()
            live.append((p, a, args, time.time(), slot, cap_of(args) if cap_of else cap))
        time.sleep(0.5)
        still = []
        for p, conn, args, ts, slot, cap_i in live:
            row = None
            if conn.poll():
                row = conn.recv()
                p.join(5)
            elif time.time() - ts > cap_i:
                p.terminate()
                p.join(5)
                corpus, family, seed, design, ln = args
                row = dict(corpus=corpus, family=family or "null", seed=seed, split=split_of(corpus, seed),
                           design=list(design), learned=ln, label="TIMEOUT", ok=False, err=float("inf"),
                           runtime=cap_i)
            elif not p.is_alive():
                corpus, family, seed, design, ln = args
                row = dict(corpus=corpus, family=family or "null", seed=seed, split=split_of(corpus, seed),
                           design=list(design), learned=ln, label="CRASH", ok=False, err=float("inf"),
                           error=f"process exit {p.exitcode}")
            if row is None:
                still.append((p, conn, args, ts, slot, cap_i))
                continue
            pool.release(slot)
            if on_row is not None:
                row = on_row(row) or row
            with open(out, "a") as fh:
                fh.write(json.dumps(row, default=str) + "\n")
            print(row["corpus"], row["family"], row["seed"], row["design"], row["learned"], row["label"],
                  row.get("ok"), round(row.get("runtime", 0)), flush=True)
        live = still


def done_keys(out):
    keys = set()
    if Path(out).exists():
        for line in Path(out).read_text().splitlines():
            r = json.loads(line)
            keys.add((r["corpus"], r["family"], r["seed"], tuple(r["design"]), r["learned"]))
    return keys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", required=True, choices=list(SEEDS))
    ap.add_argument("--split", nargs="*", default=["fit", "cal", "test"])
    ap.add_argument("--families", nargs="*", default=list(FAMILIES))
    ap.add_argument("--designs", nargs="*", type=int, default=None, help="indices into DESIGNS[corpus]")
    ap.add_argument("--seeds", nargs="*", type=int, default=None)
    ap.add_argument("--learned", nargs="*", default=["off"])
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--cap", type=float, default=CAP_S)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    designs = DESIGNS[a.corpus] if a.designs is None else [DESIGNS[a.corpus][i] for i in a.designs]
    seeds = a.seeds if a.seeds is not None else [s for sp_ in a.split for s in SEEDS[a.corpus][sp_]]
    fams = [None] if a.corpus == "N" else a.families
    done = done_keys(a.out)
    tasks = [(a.corpus, f, s, dz, ln) for s in seeds for dz in designs for f in fams for ln in a.learned
             if (a.corpus, f or "null", s, tuple(dz), ln) not in done]
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    print(f"{len(tasks)} runs, {a.workers} workers", flush=True)
    run_all(tasks, a.out, a.workers, a.cap)


if __name__ == "__main__":
    main()
