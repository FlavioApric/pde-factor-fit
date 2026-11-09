"""Micro-benchmarks on random PDE draws (simulator.random_pde), at most MAX_INPUTS inputs per suite.

    .venv/Scripts/python.exe benchmarks/micro_draws.py <suite> [--tag NAME] [--ref TAG] [--workers 5] [--report]

The named cases of micro.py were used to tune the pipeline; draws were not, so a suite of draws is a
held-out check. Inputs are built exactly as the learned-layers corpus harness builds them
(ll_corpus.grid_input / scattered_input), so a row here reproduces that harness's row on main's code:
grid noise from default_rng(1000 + seed), bootstrap B = 16; scattered inputs read the cached GP
posterior (ll_<family>_<seed>_<n>_<noise>.npz) from main's cache or the learned-layers cache.
Scoring is e13_summary's: right / equivalent / abstain-ok / abstain / false-confident / other / CRASH.
Output: benchmarks/out/micro/draws_<suite>_<tag>.jsonl.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import traceback
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "benchmarks"))
sys.path.insert(0, str(ROOT / "code" / "experiments"))

from bench_e2e import MARK, _init_worker, _run_pool  # noqa: E402

OUT = ROOT / "benchmarks" / "out" / "micro"
CACHES = [ROOT / "code" / "experiments" / "cache", Path("D:/Larned layers/PDEFactorML/code/experiments/cache")]
MAX_INPUTS = 15
BOOT, S_LOOP = 16, 8
G = "grid"

SUITES = {
    # false-confident with every layer off on the learned-layers G test corpus (ll_G.jsonl, off arm),
    # plus the grid draws that crashed on the V0.1 SVD (fixed in 435b048: regression check) and the
    # scattered draws that raised ZeroDivisionError in refine_factors
    "fc": [("F4", 128, G, 0.05), ("F3", 130, G, 0.01), ("F3", 130, G, 0.05), ("F4", 130, G, 0.01),
           ("F2", 134, G, 0.01), ("F3", 133, G, 0.05), ("F2", 135, G, 0.05), ("F5", 131, G, 0.05),
           ("F4", 135, G, 0.05), ("F4", 129, G, 0.01), ("F4", 131, G, 0.05), ("F4", 209, 400, 0.05),
           ("F5", 209, 2000, 0.01)],
}
for _s, _v in SUITES.items():
    assert len(_v) <= MAX_INPUTS, _s


def make_input(family, seed, design, noise):
    from pdefactor.simulator import random_pde
    from pdefactor.synthetic import grid

    d = random_pde(family, seed)
    t, x, u = grid(d.field)
    if design == G:
        rng = np.random.default_rng(1000 + seed)
        sig = noise * np.std(u)
        un = u + sig * rng.standard_normal(u.shape)
        return dict(draw=d, t=t, x=x, samples=[un], pis=None, sigma=sig, noise_draws=None, raw=None,
                    bootstrap=BOOT, grid_data=un, grid_sigma=sig)
    from bench_e2e import smooth_noise

    name = f"ll_{family}_{seed}_{int(design)}_{noise:g}.npz"
    p = next((c / name for c in CACHES if (c / name).exists()), None)
    if p is None:
        raise FileNotFoundError(f"no cached GP posterior {name}")
    c = dict(np.load(p))
    S, w = c["samples"][:S_LOOP], c["weights"][:S_LOOP]
    w = w / w.sum()
    mean = np.tensordot(w, S, 1)
    return dict(draw=d, t=t, x=x, samples=list(S), pis=w, sigma=0.0, noise_draws=np.sqrt(2) * (S - mean[None]),
                raw=dict(ts=c["ts"], xs=c["xs"], ys=c["ys"], period=2 * np.pi, sigma=float(c["sigma"])),
                bootstrap=0, grid_data=mean, grid_sigma=smooth_noise(S, w))


def _equivalent(truth, facs, inp):
    import sympy as sp
    from e13_summary import DCHI2_EQUIV, chi2_gap

    from pdefactor.simulator import match

    if match([sp.expand(sp.Mul(*truth))], [sp.expand(sp.Mul(*facs))])[0]:
        return True
    u, t, x, sig = inp["grid_data"], inp["t"], inp["x"], inp["grid_sigma"]
    try:
        gap = chi2_gap(facs, truth, u, t, x, sig)  # T95: EQUIV_DF switch inside
    except Exception:  # noqa: BLE001
        return False
    return bool(gap <= DCHI2_EQUIV)


def rescore(suite, ref, tag, ref_dir=OUT):
    """Recompute equiv / category of the rows of draws_<suite>_<ref>.jsonl with the current scoring (no
    pipeline rerun; the factors are read from the rows) into draws_<suite>_<tag>.jsonl."""
    import sympy as sp

    from pdefactor.simulator import random_pde

    from pdefactor import loop

    rows = _rows(Path(ref_dir) / f"draws_{suite}_{ref}.jsonl")
    out = OUT / f"draws_{suite}_{tag}.jsonl"
    with open(out, "w") as fh:
        for k, r in rows.items():
            r = dict(r)
            if (loop.GRID_SMOOTH_GOF and k[2] == G and not r.get("error") and r["factors"]
                    and r["label"] == "FIT-COMPATIBLE"):
                # T96: the label rule is a function of the reported (pruned) factors and the grid only,
                # so it is applied to the stored rows exactly as run_loop applies it (no rerun)
                from pdefactor.validate import smooth_gof_log10p

                inp = make_input(k[0], k[1], G, k[3])
                lp_s, _ = smooth_gof_log10p([sp.sympify(q) for q in r["factors"]], inp["grid_data"], inp["t"],
                                            inp["x"], inp["grid_sigma"])
                r["smooth_gof"] = lp_s
                if lp_s < loop.PRED_LOGP:
                    r["label"] = "UNDECIDED"
            if not r.get("error") and not r["ok"] and r["factors"]:
                try:
                    inp = make_input(k[0], k[1], k[2] if k[2] == G else int(k[2]), k[3])
                    facs = [sp.sympify(q) for q in r["factors"]]
                    r["equiv"] = bool(_equivalent(list(random_pde(k[0], k[1]).factors), facs, inp))
                except FileNotFoundError:
                    pass  # scattered input without a cached GP posterior: the stored score is kept
            r["category"] = category(r)
            fh.write(json.dumps(r, default=str) + "\n")


def category(r):
    """e13_summary.classify on one row."""
    if r.get("error"):
        return "CRASH"
    if r["ok"]:
        return "right"
    if r.get("equiv"):
        return "equivalent"
    lab = r["label"]
    if lab in ("ID-KER", "UNDECIDED") or lab.startswith("ID-KER"):
        return "abstain-ok" if not r["all_ident"] else "abstain"
    if lab == "FIT-COMPATIBLE":
        return "false-confident"
    return "other"


def run_one(family, seed, design, noise):
    from e13_random_pdes import identifiable

    from pdefactor.loop import run_loop
    from pdefactor.simulator import match

    inp = make_input(family, seed, design, noise)
    d = inp["draw"]
    row = dict(family=family, seed=seed, design=design, noise=noise, truth=[str(q) for q in d.factors])
    sig = inp["grid_sigma"]
    if inp["raw"] is not None:
        sig = inp["raw"]["sigma"] * np.sqrt(len(inp["t"]) * len(inp["x"]) / int(design))
    ident = identifiable(d, inp["t"], inp["x"], sig)
    row["all_ident"] = bool(all(i[0] for i in ident))
    t0 = time.perf_counter()
    try:
        with np.errstate(all="ignore"):
            res = run_loop(inp["samples"], inp["t"], inp["x"], inp["sigma"], inp["pis"],
                           noise_draws=inp["noise_draws"], raw=inp["raw"], bootstrap=inp["bootstrap"])
        facs = res.pruned()
        ok, err = match(d.factors, facs) if facs else (False, float("inf"))
        row.update(label=res.label, factors=[str(q) for q in facs], ok=bool(ok), err=float(err), note=res.note,
                   equiv=bool(facs) and not ok and _equivalent(list(d.factors), facs, inp))
    except Exception as e:  # noqa: BLE001  (a crash is a reported failure)
        row.update(label="CRASH", factors=[], ok=False, err=float("inf"), error=f"{type(e).__name__}: {e}",
                   trace=traceback.format_exc()[-1500:])
    row["runtime"] = time.perf_counter() - t0
    row["category"] = category(row)
    return row


def _key(r):
    return (r["family"], int(r["seed"]), str(r["design"]), float(r["noise"]))


def _rows(p):
    p = Path(p)
    if not p.exists():
        return {}
    return {_key(r): r for r in map(json.loads, filter(str.strip, p.read_text().splitlines()))}


def _argv(tk, ms):
    return [sys.executable, "-u", str(Path(__file__).resolve()), "--one", json.dumps(list(tk))]


def table(suite, tag, ref=None, ref_dir=OUT):
    cur = _rows(OUT / f"draws_{suite}_{tag}.jsonl")
    old = _rows(Path(ref_dir) / f"draws_{suite}_{ref}.jsonl") if ref else {}
    lines = ["| input | label | category | err | time s | ref category | ref time |", "|---|---|---|---|---|---|---|"]
    cnt, rcnt = {}, {}
    for fam, sd, des, nz in SUITES[suite]:
        k = (fam, sd, str(des), float(nz))
        r = cur.get(k)
        if r is None:
            continue
        o = old.get(k)
        cnt[r["category"]] = cnt.get(r["category"], 0) + 1
        if o:
            rcnt[o["category"]] = rcnt.get(o["category"], 0) + 1
        lines.append(f"| {fam}-{sd} {des} {nz:g} | {r['label']} | {r['category']} | {r['err']:.2g} | "
                     f"{r['runtime']:.0f} | {o['category'] if o else '-'} | {f'{o['runtime']:.0f}' if o else '-'} |")
    lines.append(f"\n{suite} [{tag}]: {dict(sorted(cnt.items()))} (reference {dict(sorted(rcnt.items()))})")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("suite", choices=sorted(SUITES))
    ap.add_argument("--tag", default="cur")
    ap.add_argument("--ref")
    ap.add_argument("--workers", type=int, default=5)
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--design", nargs="*", help="run only these designs (grid, 400, 2000)")
    ap.add_argument("--rescore", metavar="REF", help="rescore the rows of REF into TAG (no pipeline run)")
    ap.add_argument("--ref-dir", default=str(OUT), help="directory of the REF rows (default: this checkout's)")
    a = ap.parse_args()
    out = OUT / f"draws_{a.suite}_{a.tag}.jsonl"
    if a.rescore:
        OUT.mkdir(parents=True, exist_ok=True)
        rescore(a.suite, a.rescore, a.tag, Path(a.ref_dir))
        a.report, a.ref = True, a.ref or a.rescore
    if not a.report:
        OUT.mkdir(parents=True, exist_ok=True)
        done = set(_rows(out))
        todo = [(tk, ("pipeline",)) for tk in SUITES[a.suite] if (tk[0], tk[1], str(tk[2]), float(tk[3])) not in done
                and (not a.design or str(tk[2]) in a.design)]
        print(f"{a.suite}: {len(todo)} inputs to run", flush=True)
        _run_pool(todo, out, a.workers, argv=_argv)
    print(table(a.suite, a.tag, a.ref, a.ref_dir), flush=True)


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--one":
        _init_worker()
        print(MARK + json.dumps([run_one(*json.loads(sys.argv[2]))], default=str), flush=True)
        sys.exit(0)
    main()
