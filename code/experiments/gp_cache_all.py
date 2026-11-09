"""Fit and cache the GP posterior for every scattered input of the end-to-end benchmark."""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gp_cache import fit_and_cache  # noqa: E402

from pdefactor.synthetic import CASES  # noqa: E402

NS, NOISES, SEEDS = (400, 2000), (1e-3, 1e-2, 5e-2), (0, 1, 2)
if __name__ == "__main__":
    # optional: case names and noise levels, e.g. gp_cache_all.py --cases damped_beam kg_drift --noises 0.01 0.05
    a = sys.argv[1:]
    if "--cases" in a:
        i = a.index("--cases")
        j = a.index("--noises") if "--noises" in a else len(a)
        CASES = a[i + 1:j] if j > i else a[i + 1:]
    if "--noises" in a:
        NOISES = tuple(float(v) for v in a[a.index("--noises") + 1:] if not v.startswith("--"))
    for n in NS:
        for seed in SEEDS:
            for nz in NOISES:
                for name in CASES:
                    t0 = time.time()
                    fit_and_cache(name, n, nz, seed)
                    print(name, n, nz, seed, f"{time.time() - t0:.0f}s", flush=True)
