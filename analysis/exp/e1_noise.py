"""E1: noise sweep of the deterministic core on gridded data (no interpolation layer).

For each case and noise level (relative to std(u)): label, whether the factor set is right,
max coefficient error of the matched factors. Output: analysis/exp/out/e1_noise.csv + summary.
"""
import sys
from pathlib import Path

import numpy as np
import sympy as sp

from pdefactor.core import analyze
from pdefactor.symbols import factors as exact_factors, tau, xi
from pdefactor.synthetic import CASES, case, grid

OUT = Path(__file__).parent / "out"
OUT.mkdir(exist_ok=True)


def truth(name, f):
    if name == "schrodinger":
        return [tau - sp.I * sp.Float(0.3) * xi**2]
    if name == "beam":
        return [tau - sp.I * sp.Float(0.3) * xi**2, tau + sp.I * sp.Float(0.3) * xi**2]
    # a real component of a non-real factor holds the conjugate branch too (real field): both factors
    cq = []
    for c in f.components:
        Q = sp.expand(sp.N(c.Q))
        if any(abs(sp.im(v)) > 0 for v in sp.Poly(Q, tau, xi).coeffs()):
            cq += [Q] + ([sp.expand(sp.conjugate(Q).subs({sp.conjugate(tau): tau, sp.conjugate(xi): xi}))]
                         if c.real else [])
    if cq:
        return cq
    return [q for q, _ in exact_factors(f.P)]


def coef_vec(q, m, dx):
    """Coefficients of a monic-in-tau sympy polynomial as a dict {(k, b): c}."""
    p = sp.Poly(sp.expand(sp.N(q)), tau, xi, domain="CC")
    return {mon: complex(c) for mon, c in zip(p.monoms(), p.coeffs())}


def match_err(tr, got):
    """Max over true factors of the min coefficient distance to a fitted factor (inf if counts differ)."""
    if len(tr) != len(got):
        return np.inf
    errs = []
    for q in tr:
        cq = coef_vec(q, 0, 0)
        best = np.inf
        for g in got:
            cg = coef_vec(g, 0, 0)
            keys = set(cq) | set(cg)
            best = min(best, max(abs(cq.get(k, 0) - cg.get(k, 0)) for k in keys))
        errs.append(best)
    return max(errs)


def run(noises=(0.0, 1e-4, 1e-3, 1e-2, 3e-2, 1e-1), seeds=(0, 1, 2), cases=CASES):
    rows = []
    for name in cases:
        f = case(name)
        t, x, u = grid(f)
        tr = truth(name, f)
        for nz in noises:
            for s in seeds:
                rng = np.random.default_rng(100 + s)
                sig = nz * np.std(np.abs(u))
                noise = sig * (rng.standard_normal(u.shape) + (1j * rng.standard_normal(u.shape) if np.iscomplexobj(u) else 0))
                r = analyze(u + noise, t, x, noise=sig)
                got = [fr.sympy for fr in r.factors]
                e = match_err(tr, got) if r.factors else np.inf
                rows.append((name, nz, s, r.label, len(got), len(tr), e, r.gamma))
                if nz == 0:
                    break
    import csv
    with open(OUT / "e1_noise.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["case", "noise", "seed", "label", "nfac", "ntrue", "coef_err", "gamma"])
        w.writerows(rows)
    # summary: per case and noise, fraction with right factor set (err < 0.05) and median error
    print(f"{'case':26s}" + "".join(f"{n:>11.0e}" for n in noises))
    for name in cases:
        line = f"{name:26s}"
        for nz in noises:
            rr = [r for r in rows if r[0] == name and r[1] == nz]
            ok = np.mean([r[6] < 0.05 for r in rr])
            med = np.median([r[6] for r in rr])
            line += f"  {ok:.1f}/{med:6.0e}" if np.isfinite(med) else f"  {ok:.1f}/  inf "
        print(line)
    return rows


if __name__ == "__main__":
    run(cases=sys.argv[1:] or CASES)
