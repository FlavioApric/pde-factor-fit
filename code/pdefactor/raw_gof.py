"""T86: goodness of fit of a reported law on the raw scattered observations.

The kernel of the reported factors spans, in the band of the excited bins, a basis of columns
e^{lambda t + i kappa x}; the raw points y are fitted by least squares on that basis and the residual
is compared with the known noise: |r|^2 / sigma^2 ~ chi^2(n - rank) (real field; complex: twice
the statistic on 2 (n - rank) dof) when the law holds. Data-level and model-specific: a law that the
evidence preferred among the candidates but that leaves structure in the raw data fails it, whatever
the interpolation did. Used only on scattered inputs (on a grid V0.1 already tests the fit)."""
from __future__ import annotations

import numpy as np
from scipy.stats import chi2

from .refine_raw import _basis_groups, _excited_bins_raw


def raw_gof_log10p(syms, raw, kmax_max=16):
    """log10 p of the raw residual after the least-squares fit on the kernel basis of `syms`
    (PolySymbol list); band = largest excited bin (_excited_bins_raw, data only) + 2. Returns
    (log10 p, kmax)."""
    ts, xs, ys, per, sig = raw["ts"], raw["xs"], raw["ys"], raw["period"], raw["sigma"]
    real = bool(np.isrealobj(ys))
    exc = _excited_bins_raw(ts, xs, ys, per, kmax_max, real, sig)
    kmax = (max(exc) if exc else 0) + 2
    B, _ = _basis_groups(list(syms), ts, xs, per, kmax, real)
    rank = 0
    res = np.asarray(ys)
    if B.shape[1] and np.all(np.isfinite(B)):
        U, s, _ = np.linalg.svd(B, full_matrices=False)
        U = U[:, s > 1e-10 * s.max()]
        res = ys - U @ (U.conj().T @ ys)
        rank = U.shape[1]
    st = float(np.vdot(res, res).real) / sig**2
    df = (len(ys) - rank) * (1 if real else 2)
    if df <= 0:
        return 0.0, kmax  # no residual dof: no test
    return float(chi2.logsf(st if real else 2 * st, df) / np.log(10)), kmax
