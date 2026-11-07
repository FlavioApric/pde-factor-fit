"""PySINDy baselines on a linear derivative library: PDE-FIND (strong form), Weak SINDy,
Ensemble SINDy (bagging on the weak system) and SBR (horseshoe NUTS on the weak system).

pysindy's PDELibrary / WeakPDELibrary target u_t only; the truth here can be 2nd order in t
with mixed d_t d_x terms (wave, TPD, beam, KG, telegraph), so the features are built in
`common` and pysindy supplies the optimizers.
"""
from __future__ import annotations

import time
import warnings

import numpy as np
import pysindy as ps

from .common import (BaselineResult, bic, factor_symbol, realify, strong_system, structure_distribution,
                     symbol_coeffs, to_sympy, unrealify, weak_system)

M_SET = (1, 2, 3)
THRESHOLDS = np.r_[0.0, np.logspace(-4, 0, 13)]
RHO0 = 1e-3  # relative residual floor in the BIC: systematic discretisation error below 0.1 % is not fitted


def _normalise(A):
    s = np.linalg.norm(A, axis=0)
    s[s == 0] = 1
    return A / s, s


def _stlsq(A, y, thr, alpha=1e-6):
    An, s = _normalise(A)
    yn = np.linalg.norm(y) or 1.0
    opt = ps.STLSQ(threshold=thr, alpha=alpha, max_iter=50)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        opt.fit(An, y / yn)
    return opt.coef_.ravel() * yn / s


def _path(build, m_set=M_SET, thresholds=THRESHOLDS):
    """STLSQ over (m, threshold), BIC-selected. Returns best (bic, m, c, idx, cplx) and all systems."""
    best, systems = None, {}
    for m in m_set:
        Th, y, idx = build(m)
        A, yy, cplx = realify(Th, y)
        systems[m] = (A, yy, idx, cplx)
        floor = RHO0**2 * float(yy @ yy)
        for thr in thresholds:
            c = _stlsq(A, yy, thr)
            r = yy - A @ c
            # parameters: nonzeros + 1 per m (the target's order is a structural choice)
            b = bic(float(r @ r) + floor, len(yy), int((c != 0).sum()) + m, floor)
            if best is None or b < best[0]:
                best = (b, m, c, idx, cplx, thr)
    return best, systems


def _result(method, m, c, idx, cplx, t0, decimals, **info):
    coeffs = symbol_coeffs(unrealify(c, cplx), idx, m)
    facs, st = factor_symbol(coeffs, decimals)
    return BaselineResult(method, True, "", to_sympy(coeffs), coeffs, m, facs, st, None,
                          time.perf_counter() - t0, info)


def pdefind(u, t, x, noise=0.0, dx_max=4, decimals=2):
    t0 = time.perf_counter()
    best, _ = _path(lambda m: strong_system(u, t, x, m, dx_max))
    _, m, c, idx, cplx, thr = best
    return _result("pdefind", m, c, idx, cplx, t0, decimals, threshold=thr)


def _weak_build(u, t, x, dx_max, K, seed):
    return lambda m: weak_system(u, t, x, m, dx_max, K=K, seed=seed)


def weak_sindy(u, t, x, noise=0.0, dx_max=4, K=200, decimals=2, seed=0):
    t0 = time.perf_counter()
    best, _ = _path(_weak_build(u, t, x, dx_max, K, seed))
    _, m, c, idx, cplx, thr = best
    return _result("weak_sindy", m, c, idx, cplx, t0, decimals, threshold=thr)


def ensemble_sindy(u, t, x, noise=0.0, dx_max=4, K=200, n_models=50, decimals=2, seed=0):
    """E-WSINDy (Fasel et al. 2022): (m, threshold) from the weak BIC path, then bagging of rows.
    The aggregated model is the median; structure probabilities are member frequencies."""
    t0 = time.perf_counter()
    best, systems = _path(_weak_build(u, t, x, dx_max, K, seed))
    _, m, _, idx, cplx, thr = best
    A, yy, idx, cplx = systems[m]
    An, s = _normalise(A)
    yn = np.linalg.norm(yy) or 1.0
    np.random.seed(seed)  # EnsembleOptimizer samples with the global numpy RNG
    opt = ps.EnsembleOptimizer(ps.STLSQ(threshold=thr, alpha=1e-6, max_iter=50), bagging=True, n_models=n_models)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        opt.fit(An, yy / yn)
    members = [np.asarray(cm).ravel() * yn / s for cm in opt.coef_list]
    c = np.median(np.stack(members), 0)
    res = _result("ensemble_sindy", m, c, idx, cplx, t0, decimals, threshold=thr)
    res.structure_probs = structure_distribution(
        [symbol_coeffs(unrealify(cm, cplx), idx, m) for cm in members], decimals)
    res.runtime = time.perf_counter() - t0
    return res


def sbr_sindy(u, t, x, noise=0.0, dx_max=4, K=200, num_warmup=300, num_samples=500, n_struct=100,
              decimals=2, seed=0):
    """SBR (regularised horseshoe, NUTS) on the weak system of the BIC-selected m.
    Structure probabilities: frequencies over n_struct posterior coefficient samples."""
    t0 = time.perf_counter()
    best, systems = _path(_weak_build(u, t, x, dx_max, K, seed))
    m = best[1]
    A, yy, idx, cplx = systems[m]
    An, s = _normalise(A)
    yn = np.linalg.norm(yy) or 1.0
    opt = ps.SBR(num_warmup=num_warmup, num_samples=num_samples,
                 mcmc_kwargs={"progress_bar": False, "num_chains": 1})
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        opt.fit(An, yy / yn)
    samples = np.asarray(opt.mcmc_.get_samples()["beta"]).reshape(num_samples, -1) * yn / s
    c = np.asarray(opt.coef_).ravel() * yn / s
    res = _result("sbr_sindy", m, c, idx, cplx, t0, decimals)
    pick = np.random.default_rng(seed).choice(num_samples, min(n_struct, num_samples), replace=False)
    res.structure_probs = structure_distribution(
        [symbol_coeffs(unrealify(samples[i], cplx), idx, m) for i in pick], decimals)
    res.runtime = time.perf_counter() - t0
    return res
