"""Fit the GP posterior on one scattered benchmark input and cache it (samples, weights, mean, grid).
Usage: gp_cache.py case n noise seed [S]   -> analysis/exp/cache/<case>_<n>_<noise>_<seed>.npz"""
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from benchmarks.bench import FIELD_SEED, L_SPAN, T_SPAN, field_of  # noqa: E402
from pdefactor.interp.gp import fit_gp  # noqa: E402
from pdefactor.synthetic import any_case, grid  # noqa: E402


def cache_path(name, n, noise, seed):
    fs = "_fs" if FIELD_SEED and seed else ""  # an independent field per seed has its own cache
    return ROOT / "analysis" / "exp" / "cache" / f"{name}_{n}_{noise:g}_{seed}{fs}.npz"


def fit_and_cache(name, n, noise, seed, S=16):
    p = cache_path(name, n, noise, seed)
    if p.exists():
        return dict(np.load(p))
    f = field_of(name, seed)
    t, x, u = grid(f, T=T_SPAN, L=L_SPAN)
    sig = noise * float(np.std(np.abs(u)))
    rng = np.random.default_rng(1000 + 7919 * seed + n)  # same draw as benchmarks.bench.make_input
    ts, xs = rng.uniform(0, T_SPAN, n), rng.uniform(0, L_SPAN, n)
    cplx = np.iscomplexobj(u)
    e = rng.standard_normal(n)
    e = sig * (e + 1j * rng.standard_normal(n) if cplx else e)
    ys = f(ts, xs) + e
    parts = [ys.real, ys.imag] if cplx else [ys]
    fits = [fit_gp(ts, xs, y, grid=(t, x), period_x=L_SPAN, S=S, seed=seed) for y in parts]
    if cplx:
        samples = fits[0].samples + 1j * fits[1].samples
        mean = fits[0].mean + 1j * fits[1].mean
        w = fits[0].weights * fits[1].weights
    else:
        samples, mean, w = fits[0].samples, fits[0].mean, fits[0].weights
    out = dict(samples=samples, mean=mean, weights=w / w.sum(), t=t, x=x, u=u, sigma=sig,
               ts=ts, xs=xs, ys=ys)
    p.parent.mkdir(parents=True, exist_ok=True)
    np.savez(p, **out)
    return out


if __name__ == "__main__":
    a = sys.argv[1:]
    d = fit_and_cache(a[0], int(a[1]), float(a[2]), int(a[3]), int(a[4]) if len(a) > 4 else 16)
    print(a, d["samples"].shape)
