"""Golden outputs of run_loop with every learned layer off (S-LEARNED B0; PLAN.md §1.1).

Generated once, from the B0 snapshot (sessions/LEARNED/SYNC.md) before any layer hook existed.
tests/test_learned_off.py reruns the same inputs with learned=None and learned=Learned() and
compares. Usage: python tests/data/make_learned_off_golden.py
"""
from __future__ import annotations

import json
import sys
import warnings
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))
warnings.filterwarnings("ignore")

OUT = Path(__file__).with_name("learned_off_golden.json")


def inputs():
    """name -> (samples, t, x, sigma, kwargs) for run_loop."""
    from pdefactor.simulator import random_pde
    from pdefactor.synthetic import any_case, grid

    out = {}
    for fam, seed, noise in (("F1", 0, 0.01), ("F1", 0, 0.05), ("F5", 1, 0.01)):
        d = random_pde(fam, seed)
        t, x, u = grid(d.field)
        rng = np.random.default_rng(1000 + seed)
        sig = noise * np.std(u)
        out[f"{fam}-{seed}-{noise}"] = ([u + sig * rng.standard_normal(u.shape)], t, x, sig, dict(bootstrap=4))
    t, x, u = grid(any_case("heat"))
    rng = np.random.default_rng(7)
    sig = 0.05 * np.std(u)
    out["heat-grid-0.05"] = ([u + sig * rng.standard_normal(u.shape)], t, x, sig, dict(bootstrap=4))
    rng = np.random.default_rng(11)
    out["pure-noise-grid"] = ([rng.standard_normal(u.shape)], t, x, 1.0, dict(bootstrap=0))
    p = ROOT / "benchmarks" / "cache" / "heat_400_0.05_0.npz"
    if p.exists():  # scattered path: GP samples + raw observations (cache copied from the main repo)
        d = dict(np.load(p))
        S, w = d["samples"][:8], d["weights"][:8]
        mean = np.tensordot(w / w.sum(), S, 1)
        sys.path.insert(0, str(ROOT))
        from benchmarks.bench import L_SPAN

        # as benchmarks/bench_e2e.run_method: sigma 0 and GLS noise draws for GP samples
        out["heat-400-0.05"] = (list(S), d["t"], d["x"], 0.0,
                                dict(pis=w / w.sum(), noise_draws=np.sqrt(2) * (S - mean[None]),
                                     raw=dict(ts=d["ts"], xs=d["xs"], ys=d["ys"], period=L_SPAN,
                                              sigma=float(d["sigma"]))))
    return out


def summary(r):
    """Everything a learned layer could touch: label, factors, coefficient intervals, split weights."""
    facs = []
    for f in r.factors:
        facs.append({f"{a},{b}": [[complex(v).real, complex(v).imag] for v in vals] for (a, b), vals in f.coef.items()})
    sp_ = r.split or {}
    return dict(label=r.label, factors=[str(q) for q in r.pruned()], coef=facs,
                structures={str(k): float(v) for k, v in (r.structures or {}).items()},
                w_mean=np.asarray(sp_.get("w_mean", []), float).tolist(),
                w_q=np.asarray(sp_.get("w_q", []), float).tolist(), note=r.note)


def run(name, inp, learned=None):
    from pdefactor.loop import run_loop

    S, t, x, sig, kw = inp
    with np.errstate(all="ignore"):
        return summary(run_loop(S, t, x, sig, learned=learned, **kw))


if __name__ == "__main__":
    res = {name: run(name, inp) for name, inp in inputs().items()}
    OUT.write_text(json.dumps(res, indent=1))
    print("wrote", OUT, list(res))
