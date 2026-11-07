"""End-to-end benchmark (Phase 3): the full pipeline against the baselines on the same inputs.

    .venv/Scripts/python.exe benchmarks/bench_e2e.py [--workers 6]

Inputs: every case of synthetic.CASES, noise 1e-3 / 1e-2 / 5e-2, seeds 0-2, sampled
- on the grid (white noise, as bench.make_input), or
- scattered (n = 400, 2000; the draw of bench.make_input), interpolated by the GP posterior of
  S-INTERP (cached by analysis/exp/gp_cache_all.py).

Methods:
- "pipeline": outer loop (loop.run_loop) on the posterior samples, core v2 per sample with the GLS
  per-bin noise from sqrt(2) (sample - mean); factors = the pruned equation (terms whose 90 %
  interval contains 0 dropped). On gridded input: the loop on the one noisy grid, white noise, with
  coefficient intervals from BOOT parametric-bootstrap refits at the final structure.
- "core_v2": core v2 once, on the GP posterior mean with GLS noise draws (sample - mean), or on
  the grid.
- baselines (PDE-FIND, weak / ensemble / SBR SINDy, BOP-DMD): on the same GP posterior mean, with
  the effective white noise of the GP (GPPosterior.effective_noise, "smooth"), or on the grid.
Rows go to benchmarks/out/e2e.jsonl (resumable).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import traceback
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "analysis" / "exp"))
OUT = ROOT / "benchmarks" / "out" / "e2e.jsonl"

NOISES = (1e-3, 1e-2, 5e-2)
SAMPLINGS = ("grid", 2000, 400)
SEEDS = (0, 1, 2)
# --quick: every case and sampling, the two noise levels where methods differ (run 6: all cells at
# 1e-3 were 1.00), seeds 0-1; 120 inputs instead of 270
QUICK = dict(noises=(1e-2, 5e-2), seeds=(0, 1))
BASELINES = ("pdefind", "weak_sindy", "ensemble_sindy", "sbr_sindy", "bopdmd")
METHODS = ("pipeline", "core_v2") + BASELINES
S_LOOP = 8  # posterior samples handed to the loop
BOOT = 16  # parametric-bootstrap refits for the coefficient intervals on gridded input


def smooth_noise(samples, w, r=4, factor=np.sqrt(2)):
    """GPPosterior.effective_noise(kind="smooth") restated on cached arrays."""
    from numpy.polynomial import legendre

    d = samples - np.tensordot(w, samples, 1)[None]
    nt, nx = d.shape[-2:]
    B = np.fft.fft(d, axis=-1) / nx
    Q, _ = np.linalg.qr(legendre.legvander(np.linspace(-1, 1, nt), r - 1))
    P = np.einsum("ta,stk->sak", Q, B)
    b2 = (np.sum(w[:, None, None] * (np.abs(P) ** 2).sum(1), axis=0) / r).max()
    return float(factor * np.sqrt(b2) * np.sqrt(nx))


def load_input(name, noise, sampling, seed):
    from benchmarks.bench import make_input
    from gp_cache import cache_path

    from pdefactor.synthetic import any_case as case

    if sampling == "grid":
        inp = make_input(name, noise, "grid", seed)
        inp.update(samples=inp["U"][None], weights=np.ones(1), draws=None, mean=inp["U"])
        return inp
    p = cache_path(name, int(sampling), noise, seed)
    if not p.exists():
        return None
    d = dict(np.load(p))
    S, w = d["samples"], d["weights"]
    mean = np.tensordot(w, S, 1)
    from benchmarks.bench import CPLX_SIGMA, L_SPAN, field_of

    # the cache stores the noise std of each part; the pipeline reads complex noise as CN(0, sigma^2)
    s_raw = float(d["sigma"]) * (np.sqrt(2) if CPLX_SIGMA and np.iscomplexobj(d["ys"]) else 1.0)
    return dict(U=mean, t=d["t"], x=d["x"], sigma=smooth_noise(S, w), field=field_of(name, seed), samples=S, weights=w,
                draws=S - mean[None], mean=mean,
                raw=dict(ts=d["ts"], xs=d["xs"], ys=d["ys"], period=L_SPAN, sigma=s_raw))


def _cover(rep_factors, truth_factors):
    """Fraction of true coefficients inside the pipeline's 90 % intervals (matched factor by factor;
    a monomial the factor lacks has interval [0, 0])."""
    from benchmarks.metrics import coef_dist
    from e1_noise import coef_vec

    hits = []
    for q in truth_factors:
        if not rep_factors:
            return None
        f = min(rep_factors, key=lambda r: coef_dist(q, r.sympy))
        tv = coef_vec(q, 0, 0)
        for mon in set(tv) | set(f.coef):
            v = complex(tv.get(mon, 0))
            mean, lo, hi = f.coef.get(mon, (0j, 0j, 0j))
            tol = 1e-9 * max(1.0, abs(v))
            hits.append(lo.real - tol <= v.real <= hi.real + tol and lo.imag - tol <= v.imag <= hi.imag + tol)
    return float(np.mean(hits)) if hits else None


def _w_cover(name, f, t, x, facs, w_q):
    """True weights inside the split layer's 90 % intervals (each true factor matched to the nearest
    reported one); None where the truth has no per-factor weights."""
    from benchmarks.metrics import coef_dist, true_weights, truth

    tw = true_weights(name, f, t, x)
    if tw is None:
        return None
    hits = []
    for j, q in enumerate(truth(name, f)):
        g = min(range(len(facs)), key=lambda i: coef_dist(q, facs[i]))
        hits.append(w_q[g][0] <= tw[j] <= w_q[g][2])
    return float(np.mean(hits))


def run_method(method, name, inp):
    from benchmarks import metrics as M

    from pdefactor.baselines.common import structure_of

    U, t, x, sig, f = inp["U"], inp["t"], inp["x"], inp["sigma"], inp["field"]
    grid_in = inp["draws"] is None
    row = {"case": name, "method": method}
    t0 = time.perf_counter()
    try:
        if method == "pipeline":
            from pdefactor.loop import run_loop

            S, w = inp["samples"][:S_LOOP], inp["weights"][:S_LOOP]
            nd = None if grid_in else np.sqrt(2) * inp["draws"]
            r = run_loop(list(S), t, x, sig if grid_in else 0.0, w / w.sum(), noise_draws=nd, raw=inp.get("raw"),
                         bootstrap=BOOT if grid_in else 0)
            facs = r.pruned()
            wts = r.split["w_mean"] if r.split else [fr.W for fr in r.factors]
            if r.split:
                row.update(p_split=r.split["p_split"], w_q=r.split["w_q"], cF=r.split["cF"],
                           w_cover90=_w_cover(name, f, t, x, facs, r.split["w_q"]))
            row.update(label=r.label, equation=r.equation(), p_k={str(k): v for k, v in r.p_k.items()},
                       bounds=list(r.bounds), regrouped=r.regrouped,
                       statuses=[fr.status for fr in r.factors], note=r.note,
                       cover90=_cover(r.factors, M.truth(name, f)))
        elif method == "core_v2":
            from pdefactor.core.structfit import analyze_structured

            kw = dict(noise=sig) if grid_in else dict(noise=0.0, noise_draws=inp["draws"])
            r = analyze_structured(U, t, x, real=bool(np.isrealobj(U)), **kw)
            facs = [fr.sympy for fr in r.factors]
            wts = [fr.weight for fr in r.factors]
            row.update(label=r.label, p_top=float(r.structures[0][2]) if r.structures else None)
        else:
            from pdefactor.baselines import BASELINES as B

            r = B[method](U, t, x, noise=sig)
            facs, wts = r.factors, None
            row.update(label="n/a", applicable=r.applicable)
        row["runtime"] = time.perf_counter() - t0
        row.update(M.score(name, f, t, x, facs, wts))
        st = structure_of(facs) if facs else ()
        row["structure"] = [list(s) for s in st]
        row["struct_ok"] = row["structure"] == [list(s) for s in M.true_structure(name, f)]
        row["factors"] = [str(q) for q in facs]
        row["weights"] = wts
        row["error"] = None
    except Exception as e:  # noqa: BLE001  (a crash is a reported failure, not a stop)
        row.update(runtime=time.perf_counter() - t0, error=f"{type(e).__name__}: {e}",
                   trace=traceback.format_exc()[-800:], factor_set=False, coef_err=float("inf"),
                   weight_err=None, struct_ok=False)
    return row


def run_task(name, noise, sampling, seed, methods=METHODS):
    inp = load_input(name, noise, sampling, seed)
    if inp is None:
        return None
    rows = []
    for m in methods:
        row = run_method(m, name, inp)
        row.update(noise=noise, sampling=str(sampling), seed=seed)
        rows.append(row)
    return rows


def _init_worker():
    for k in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS"):
        os.environ[k] = "1"
    import warnings

    warnings.filterwarnings("ignore")


def _key(r):
    return (r["case"], float(r["noise"]), str(r["sampling"]), int(r["seed"]))


def run_grid(cases=None, out=OUT, workers=6, samplings=SAMPLINGS, methods=METHODS, noises=NOISES, seeds=SEEDS):
    from gp_cache import cache_path

    from pdefactor.synthetic import CASES

    out.parent.mkdir(parents=True, exist_ok=True)
    done = set()
    if out.exists():
        done = {_key(r) + (r["method"],) for r in map(json.loads, filter(str.strip, out.read_text().splitlines()))}
    todo = []
    for s in samplings:
        for sd in seeds:
            for nz in noises:
                for c in cases or CASES:
                    ms = tuple(m for m in methods if (c, float(nz), str(s), sd, m) not in done)
                    if ms and (s == "grid" or cache_path(c, int(s), nz, sd).exists()):
                        todo.append(((c, nz, s, sd), ms))
    print(f"{len(todo)} inputs to run", flush=True)
    _run_pool(todo, out, workers)


STALL = 10800  # s: a hang guard, not a time budget (accuracy first: slow inputs must finish); killed after this
MARK = "@@ROWS@@ "  # prefix of the result line a child prints


def _child_argv(tk, ms):
    return [sys.executable, "-u", str(Path(__file__).resolve()), "--one", json.dumps([list(tk), list(ms)])]


def _run_pool(todo, out, workers, argv=None, stall=None):
    """Run the inputs, each in its own Python process (at most `workers` at a time). Windows process
    pools broke here (WinError 6 in the pool's queue) and a broken pool loses every input in flight;
    one process per input confines a crash or a hang to that input: a child that dies is reported as
    failed, one still running after `stall` seconds is killed and reported as timed out."""
    import subprocess

    argv, stall = argv or _child_argv, stall or STALL
    env = dict(os.environ, OMP_NUM_THREADS="1", MKL_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1",
               PYTHONWARNINGS="ignore")
    t0, i, n = time.time(), 0, len(todo)
    queue, running = list(todo), {}
    with open(out, "a") as fh:
        while queue or running:
            while queue and len(running) < workers:
                tk, ms = queue.pop(0)
                pr = subprocess.Popen(argv(tk, ms), stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE, text=True, env=env, cwd=str(ROOT))
                running[pr] = (tk, time.time())
            time.sleep(0.5)
            for pr in list(running):
                tk, ts = running[pr]
                if pr.poll() is None:
                    if time.time() - ts > stall:
                        pr.kill()
                        pr.communicate()
                        del running[pr]
                        i += 1
                        print("TASK TIMEOUT", tk, flush=True)
                    continue
                so, se = pr.communicate()
                del running[pr]
                i += 1
                line = next((ln for ln in so.splitlines() if ln.startswith(MARK)), None)
                if pr.returncode != 0 or line is None:
                    print("TASK FAILED", tk, f"exit {pr.returncode}:", (se.strip().splitlines() or [""])[-1], flush=True)
                    continue
                for r in json.loads(line[len(MARK):]) or []:
                    fh.write(json.dumps(r, default=str) + "\n")
                fh.flush()
                print(f"{i}/{n} {tk}  {time.time() - t0:.0f}s", flush=True)


def _one(spec):
    _init_worker()
    tk, ms = json.loads(spec)
    print(MARK + json.dumps(run_task(*tk, tuple(ms)), default=str), flush=True)


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--one":
        _one(sys.argv[2])
        sys.exit(0)
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--cases", nargs="*")
    ap.add_argument("--samplings", nargs="*")
    ap.add_argument("--out", default=str(OUT))
    ap.add_argument("--methods", nargs="*")
    ap.add_argument("--noises", nargs="*", type=float)
    ap.add_argument("--seeds", nargs="*", type=int)
    ap.add_argument("--quick", action="store_true", help="smaller benchmark (QUICK)")
    a = ap.parse_args()
    samp = tuple(s if s == "grid" else int(s) for s in a.samplings) if a.samplings else SAMPLINGS
    base = QUICK if a.quick else dict(noises=NOISES, seeds=SEEDS)
    run_grid(a.cases, Path(a.out), a.workers, samp, tuple(a.methods) if a.methods else METHODS,
             tuple(a.noises) if a.noises else base["noises"], tuple(a.seeds) if a.seeds else base["seeds"])
