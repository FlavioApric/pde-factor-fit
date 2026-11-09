"""E6 (plan v2.9.1): bias of the dispersion points, pencil vs VarPro (ML) refinement.

Part A: per-mode signed error of lam against the nearest true branch at its kappa, pooled over
seeds: mean (bias) and RMS, split by Re/Im. Part B: factor-set recovery and coefficient error of
core v2 with refine=False/True (same truth, seeds and noise as E1c).
Usage: python e6_bias.py [A|B]   (default both). Output on stdout; logs go to out/e6_*.log.
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from e1_noise import match_err, truth  # noqa: E402

from pdefactor.core.structfit import analyze_structured, extract_modes_ic  # noqa: E402
from pdefactor.synthetic import CASES, branch_roots, case, grid  # noqa: E402


def _noisy(u, nz, s):
    rng = np.random.default_rng(100 + s)
    sig = nz * np.std(np.abs(u))
    e = rng.standard_normal(u.shape) + (1j * rng.standard_normal(u.shape) if np.iscomplexobj(u) else 0)
    return u + sig * e, sig


def point_bias(name, nz, seeds=range(10)):
    f = case(name)
    t, x, u = grid(f)
    tr = truth(name, f)
    out = {}
    for refine in (False, True):
        err = []
        for s in seeds:
            v, sig = _noisy(u, nz, s)
            m, *_ = extract_modes_ic(v, t, x, noise=sig, refine=refine)
            for k, lm in zip(m.kappa, m.lam):
                roots = np.concatenate([branch_roots(q, k) for q in tr])
                d = lm - roots[np.argmin(np.abs(lm - roots))]
                if abs(d) < 1.0:  # spurious modes are not bias
                    err.append(d)
        e = np.array(err)
        out[refine] = (len(e), e.real.mean(), e.imag.mean(), np.sqrt(np.mean(np.abs(e) ** 2)))
    return out


def part_a(cases=("heat", "transport_plus_diffusion", "wave", "beam"), noises=(1e-2, 3e-2, 1e-1)):
    print("A: per-mode lam error vs truth (n, mean Re, mean Im, rms) pencil | varpro")
    for name in cases:
        for nz in noises:
            o = point_bias(name, nz)
            a, b = o[False], o[True]
            print(f"{name:26s} {nz:6.0e}  {a[0]:4d} {a[1]:+.2e} {a[2]:+.2e} {a[3]:.2e}  |  "
                  f"{b[0]:4d} {b[1]:+.2e} {b[2]:+.2e} {b[3]:.2e}", flush=True)


def part_b(noises=(1e-2, 3e-2, 1e-1), seeds=(0, 1, 2), cases=CASES):
    print("B: rate right factor set / median coef err   pencil | varpro")
    for name in cases:
        f = case(name)
        t, x, u = grid(f)
        tr = truth(name, f)
        line = f"{name:26s}"
        for nz in noises:
            cell = []
            for refine in (False, True):
                errs = []
                for s in seeds:
                    v, sig = _noisy(u, nz, s)
                    r = analyze_structured(v, t, x, noise=sig, refine=refine)
                    errs.append(match_err(tr, [fr.sympy for fr in r.factors]) if r.factors else np.inf)
                ok = np.mean([e < 0.05 for e in errs])
                med = np.median(errs)
                cell.append(f"{ok:.1f}/{med:6.0e}" if np.isfinite(med) else f"{ok:.1f}/   inf")
            line += f"  {nz:5.0e}: {cell[0]} | {cell[1]}"
        print(line, flush=True)


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "AB"
    if "A" in which:
        part_a()
    if "B" in which:
        part_b()
