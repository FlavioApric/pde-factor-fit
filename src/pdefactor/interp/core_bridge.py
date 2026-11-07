"""Run the analytic core (black box, core v2) on every posterior sample (rule 3 and rule 4:
uncertainty is propagated by Monte Carlo over interpolants, never by linearisation)."""
from __future__ import annotations

from collections import defaultdict

import numpy as np

from ..core.structfit import analyze_structured


def run_core_on_samples(samples, t, x, sigma, weights=None, **core_kw):
    """Call `analyze_structured(u_s, t, x, noise=sigma)` on each sample u_s (array (S, nt, nx)).
    sigma: scalar noise std handed to the core (for GP samples use GPPosterior.effective_noise()),
    or an array (S,) with one value per sample. Returns [(StructResult, pi_s)]."""
    S = len(samples)
    w = np.full(S, 1.0 / S) if weights is None else np.asarray(weights, float) / np.sum(weights)
    sig = np.broadcast_to(np.asarray(sigma, float), (S,))
    return [(analyze_structured(np.asarray(u), t, x, noise=float(s), **core_kw), float(p))
            for u, s, p in zip(samples, sig, w)]


def factor_key(res, digits=2):
    """Hashable factor set of one core result: rounded sympy strings, sorted (label kept apart)."""
    return frozenset(str(_round(fr.sympy, digits)) for fr in res.factors)


def _round(expr, digits):
    import sympy as sp

    return sp.expand(expr).xreplace({n: sp.Float(round(float(n), digits), 6)
                                     for n in sp.expand(expr).atoms(sp.Float)})


def factor_set_posterior(results, digits=2):
    """Posterior over factor sets: sum of pi_s by (label, rounded factor set)."""
    acc = defaultdict(float)
    for res, p in results:
        acc[(res.label, factor_key(res, digits))] += p
    return dict(sorted(acc.items(), key=lambda kv: -kv[1]))


def bench_interpolator(ts, xs, ys, t, x, L, sigma=0.0, seed=0, S=8, **fit_kw):
    """Adapter to the benchmark interface of S-BASELINES-BENCH (`benchmarks/bench.py make_input`):
    returns (posterior mean on the (t, x) grid, effective white-noise std for the core). x is
    periodic with period L (prior knowledge of the synthetic domain). Complex data: Re and Im are
    fitted as independent GPs and the noise stds add in quadrature. A point interpolant only: the
    pipeline proper runs the core on the samples (`run_core_on_samples`); `sigma` (nominal) unused."""
    from .gp import fit_gp

    ys = np.asarray(ys)
    parts = [ys.real, ys.imag] if np.iscomplexobj(ys) else [ys]
    fits = [fit_gp(ts, xs, y, grid=(t, x), period_x=L, S=S, seed=seed, **fit_kw) for y in parts]
    U = fits[0].mean if len(fits) == 1 else fits[0].mean + 1j * fits[1].mean
    return U, float(np.sqrt(sum(p.effective_noise() ** 2 for p in fits)))
