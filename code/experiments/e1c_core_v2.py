"""E1c: noise sweep of core v2 (pdefactor.core.structfit.analyze_structured: order-IC modes,
structured fit, confluent test), same truth and seeds as E1/E1b. Regression benchmark for v2."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from e1_noise import match_err, truth  # noqa: E402

from pdefactor.core.structfit import analyze_structured  # noqa: E402
from pdefactor.synthetic import CASES, case, grid  # noqa: E402


def run(noises=(0.0, 1e-4, 1e-3, 1e-2, 3e-2, 1e-1), seeds=(0, 1, 2), cases=CASES):
    print(f"{'case':26s}" + "".join(f"{n:>17.0e}" for n in noises))
    for name in cases:
        f = case(name)
        t, x, u = grid(f)
        tr = truth(name, f)
        line = f"{name:26s}"
        for nz in noises:
            errs, pw, labs = [], [], []
            for s in seeds:
                rng = np.random.default_rng(100 + s)
                sig = nz * np.std(np.abs(u))
                noise = sig * (rng.standard_normal(u.shape) + (1j * rng.standard_normal(u.shape) if np.iscomplexobj(u) else 0))
                r = analyze_structured(u + noise, t, x, noise=sig)
                errs.append(match_err(tr, [fr.sympy for fr in r.factors]) if r.factors else np.inf)
                pw.append(r.structures[0][2] if r.structures else 0)
                labs.append(r.label[0])
                if nz == 0:
                    break
            ok = np.mean([e < 0.05 for e in errs])
            med = np.median(errs)
            ms = f"{med:6.0e}" if np.isfinite(med) else "   inf"
            line += f"  {ok:.1f}/{ms}/{np.mean(pw):.2f}/{''.join(labs):3s}"
        print(line, flush=True)


if __name__ == "__main__":
    run(cases=sys.argv[1:] or CASES)
