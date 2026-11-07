"""Benchmark grid (skill benchmark-protocol): case x noise x sampling x seed, all methods.

    .venv/Scripts/python.exe benchmarks/bench.py [--workers 6] [--quick]

Writes one JSON row per (input, method) to benchmarks/out/runs.jsonl (resumable: inputs already
present are skipped). Scattered inputs go through `interpolator` (default: the griddata
PLACEHOLDER of benchmarks/interp.py, until S-INTERP's GP exists).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import traceback
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
OUT = ROOT / "benchmarks" / "out"

NOISES = (0.0, 1e-3, 1e-2, 5e-2)
SAMPLINGS = ("grid", 2000, 400)
SEEDS = (0, 1, 2, 3, 4)
METHODS = ("core_v2", "core_v1", "pdefind", "weak_sindy", "ensemble_sindy", "sbr_sindy", "bopdmd")
T_SPAN, L_SPAN = 2.0, 2 * np.pi  # synthetic.grid defaults
# HANDOFF 3.6: by default every seed shares the seed-0 field (only sample points and noise change), so
# repeated misses are not independent evidence. PDEFACTOR_FIELD_SEED=1 draws an independent field per seed
# (the same named law, new modal amplitudes); off by default so run 6 stays comparable.
FIELD_SEED = os.environ.get("PDEFACTOR_FIELD_SEED", "0") == "1"


def field_of(name, seed):
    from pdefactor.synthetic import any_case

    return any_case(name, seed=seed if FIELD_SEED else 0)


CPLX_SIGMA = os.environ.get("PDEFACTOR_CPLX_SIGMA", "1") == "1"  # grid sigma of complex fields (=0: old)


def make_input(name, noise, sampling, seed, interpolator=None):
    """Gridded input for one benchmark cell. Noise std = noise * std(|u|) on the grid (as E1/E1c),
    complex for complex fields. Returns dict(U, t, x, sigma, field, meta)."""
    from pdefactor.synthetic import any_case as case, grid

    from benchmarks.interp import griddata_placeholder

    f = field_of(name, seed)
    t, x, u = grid(f, T=T_SPAN, L=L_SPAN)
    sig = noise * float(np.std(np.abs(u)))
    cplx = np.iscomplexobj(u)

    def eps(rng, shape):
        e = rng.standard_normal(shape)
        return sig * (e + 1j * rng.standard_normal(shape) if cplx else e)

    if sampling == "grid":
        rng = np.random.default_rng(100 + seed)
        # the pipeline reads complex noise as CN(0, sigma^2) (sigma^2 / 2 per part, validate.py); eps puts
        # sig on each part, so the declared std is sqrt(2) sig (same data: run-6 rows stay comparable)
        s_decl = sig * np.sqrt(2) if cplx and CPLX_SIGMA else sig
        return dict(U=u + eps(rng, u.shape), t=t, x=x, sigma=s_decl, field=f, meta={"interp": None})
    n = int(sampling)
    rng = np.random.default_rng(1000 + 7919 * seed + n)
    ts, xs = rng.uniform(0, T_SPAN, n), rng.uniform(0, L_SPAN, n)
    ys = f(ts, xs) + eps(rng, n)
    interp = interpolator or griddata_placeholder
    U, s_eff = interp(ts, xs, ys, t, x, L_SPAN, sigma=sig, seed=seed)
    return dict(U=U, t=t, x=x, sigma=s_eff, field=f,
                meta={"interp": getattr(interp, "__name__", str(interp)), "sigma_nominal": sig})


def _coeffs_json(c):
    return {f"{a},{b}": [complex(v).real, complex(v).imag] for (a, b), v in c.items()}


def run_method(method, name, inp, sbr_kw=None):
    """One method on one input -> row dict (metrics included)."""
    from benchmarks import metrics as M

    U, t, x, sig, f = inp["U"], inp["t"], inp["x"], inp["sigma"], inp["field"]
    row = {"case": name, "method": method, "sigma_eff": sig}
    t0 = time.perf_counter()
    try:
        if method == "core_v2":
            from pdefactor.core.structfit import analyze_structured

            r = analyze_structured(U, t, x, noise=sig)
            facs = [fr.sympy for fr in r.factors]
            wts = [fr.weight for fr in r.factors]
            row.update(label=r.label, probs=[[list(map(list, s)), float(p)] for s, _, p in r.structures[:30]],
                       reason=r.info.get("reason", ""),
                       core_structure=[list(s) for s in r.structures[0][0]] if r.structures else [])
        elif method == "core_v1":
            from pdefactor.core import analyze

            r = analyze(U, t, x, noise=sig)
            facs = [fr.sympy for fr in r.factors]
            wts = [fr.weight for fr in r.factors]
            row.update(label=r.label, probs=None, reason=r.info.get("reason", ""))
        else:
            from pdefactor.baselines import BASELINES

            kw = (sbr_kw or {}) if method == "sbr_sindy" else {}
            r = BASELINES[method](U, t, x, noise=sig, **kw)
            facs, wts = r.factors, None
            row.update(label="n/a", applicable=r.applicable, reason=r.reason, m=r.m,
                       coeffs=_coeffs_json(r.coeffs),
                       probs=None if r.structure_probs is None else
                       [[list(map(list, s)), float(p)] for s, p in r.structure_probs])
        row["runtime"] = time.perf_counter() - t0
        row.update(M.score(name, f, t, x, facs, wts))
        from pdefactor.baselines.common import structure_of

        st = structure_of(facs) if facs else ()
        row["structure"] = [list(s) for s in st]
        row["true_structure"] = [list(s) for s in M.true_structure(name, f)]
        row["struct_ok"] = row["structure"] == row["true_structure"]
        row["factors"] = [str(q) for q in facs]
        row["weights"] = wts
        row["error"] = None
    except Exception as e:  # noqa: BLE001  (a crash is a reported failure, not a stop)
        row.update(runtime=time.perf_counter() - t0, error=f"{type(e).__name__}: {e}",
                   trace=traceback.format_exc()[-800:], factor_set=False, coef_err=float("inf"),
                   weight_err=None, label=row.get("label", "ERROR"), struct_ok=False)
    return row


def run_task(name, noise, sampling, seed, methods=METHODS, sbr_kw=None):
    inp = make_input(name, noise, sampling, seed)
    rows = []
    for m in methods:
        row = run_method(m, name, inp, sbr_kw)
        row.update(noise=noise, sampling=str(sampling), seed=seed, interp=inp["meta"]["interp"])
        rows.append(row)
    return rows


def tasks(cases, noises=NOISES, samplings=SAMPLINGS, seeds=SEEDS):
    for name in cases:
        for s in samplings:
            for nz in noises:
                for sd in seeds:
                    yield (name, nz, s, sd)
                    if nz == 0 and s == "grid":
                        break  # exact gridded data: deterministic, one run


def _init_worker():
    for k in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS"):
        os.environ[k] = "1"
    os.environ["XLA_FLAGS"] = "--xla_cpu_multi_thread_eigen=false intra_op_parallelism_threads=1"
    import warnings

    warnings.filterwarnings("ignore")


def _key(r):
    return (r["case"], float(r["noise"]), str(r["sampling"]), int(r["seed"]))


def run_grid(cases=None, out=OUT / "runs.jsonl", workers=6, methods=METHODS, **grid_kw):
    from pdefactor.synthetic import CASES

    out.parent.mkdir(parents=True, exist_ok=True)
    done = set()
    if out.exists():
        for line in out.read_text().splitlines():
            if line.strip():
                done.add(_key(json.loads(line)))
    todo = [tk for tk in tasks(cases or CASES, **grid_kw) if (tk[0], float(tk[1]), str(tk[2]), tk[3]) not in done]
    print(f"{len(todo)} inputs to run ({len(done)} done)", flush=True)
    t0 = time.time()
    with ProcessPoolExecutor(workers, initializer=_init_worker) as ex, open(out, "a") as fh:
        futs = {ex.submit(run_task, *tk, methods): tk for tk in todo}
        for i, fu in enumerate(as_completed(futs), 1):
            tk = futs[fu]
            try:
                rows = fu.result()
            except Exception as e:  # noqa: BLE001
                print("TASK FAILED", tk, e, flush=True)
                continue
            for r in rows:
                fh.write(json.dumps(r, default=str) + "\n")
            fh.flush()
            if i % 10 == 0 or i == len(todo):
                print(f"{i}/{len(todo)}  {time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--cases", nargs="*")
    ap.add_argument("--out", default=str(OUT / "runs.jsonl"))
    a = ap.parse_args()
    run_grid(a.cases, Path(a.out), a.workers)
