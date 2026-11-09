"""E1b: noise sweep of the structured fit with BIC model comparison (prototype structfit.py),
against the same truth as E1. Prints success fraction / median coefficient error."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from e1_noise import match_err, truth  # noqa: E402
from structfit import select  # noqa: E402

from pdefactor.core.spectral import extract_modes
from pdefactor.synthetic import CASES, case, grid


def run(noises=(0.0, 1e-4, 1e-3, 1e-2, 3e-2, 1e-1), seeds=(0, 1, 2), cases=CASES):
    print(f"{'case':26s}" + "".join(f"{n:>13.0e}" for n in noises))
    res = {}
    for name in cases:
        f = case(name)
        t, x, u = grid(f)
        tr = truth(name, f)
        line = f"{name:26s}"
        for nz in noises:
            errs, pw = [], []
            for s in seeds:
                rng = np.random.default_rng(100 + s)
                sig = nz * np.std(np.abs(u))
                noise = sig * (rng.standard_normal(u.shape) + (1j * rng.standard_normal(u.shape) if np.iscomplexobj(u) else 0))
                m = extract_modes(u + noise, t, x, noise=sig)
                bn = sig / np.sqrt(len(x)) if sig > 0 else 1e-9 * np.abs(m.amp).max()
                best, ranked, _ = select(m, t, bn, real=False)
                got = [Q.to_sympy(tol=1e-3 if nz else 1e-8) for Q in best.factors]
                errs.append(match_err(tr, got))
                pw.append(ranked[0][2])
                if nz == 0:
                    break
            ok = np.mean([e < 0.05 for e in errs])
            med = np.median(errs)
            res[(name, nz)] = (ok, med, np.mean(pw))
            line += f"  {ok:.1f}/{med:6.0e}/{np.mean(pw):.2f}" if np.isfinite(med) else f"  {ok:.1f}/  inf/{np.mean(pw):.2f}"
        print(line, flush=True)
    return res


if __name__ == "__main__":
    run(cases=sys.argv[1:] or CASES)
