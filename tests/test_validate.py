"""V0 battery (PHASE4 V0): the per-bin posterior-predictive chi^2 is calibrated under the true law and
flags the bins of a missing factor."""
import numpy as np
import sympy as sp

from pdefactor.loop import FactorReport, LoopResult
from pdefactor.symbols import tau, xi
from pdefactor.synthetic import case, grid
from pdefactor.validate import predictive_bins, validate


def _res(qs):
    fr = []
    for q in qs:
        p = sp.Poly(sp.expand(q), tau, xi, domain="CC")
        coef = {mo: (complex(c), complex(c), complex(c)) for mo, c in zip(p.monoms(), p.coeffs())}
        fr.append(FactorReport(sp.expand(q), 1.0 / len(qs), coef, kappa_support=[1.0, 2.0, 3.0, 4.0]))
    return LoopResult("FIT-COMPATIBLE", fr, {}, {}, [], False, (3, 4), {})


def test_v01_calibrated_under_truth_and_flags_missing_factor():
    f = case("transport_plus_diffusion")
    t, x, u = grid(f)
    sig = 1e-2 * np.std(u)
    logps = []
    for s in range(20):
        un = u + sig * np.random.default_rng(s).standard_normal(u.shape)
        bins = predictive_bins([tau + xi, tau - 0.3 * xi**2], un, t, x, sig)
        logps.extend(b[3] for b in bins)
    p = 10 ** np.array(logps)
    assert abs(np.mean(p < 0.1) - 0.1) < 0.03 and abs(np.mean(p < 0.5) - 0.5) < 0.06  # uniform under H0
    un = u + sig * np.random.default_rng(0).standard_normal(u.shape)
    rep = validate(_res([tau + xi, tau - 0.3 * xi**2]), un, t, x, sig)
    assert not [c for c, _ in rep.flags if c == "V0.1"]
    rep = validate(_res([tau + xi]), un, t, x, sig)  # diffusion factor missing
    assert [c for c, _ in rep.flags if c == "V0.1"]
    assert rep.stats["v01_n_bad_bins"] >= 2 and 1.0 <= rep.stats["v01_max_bad_kappa"] <= 6.0
    assert np.isfinite(rep.features()["v01_omnibus_logp"])


def test_v02_flags_too_few_kappa():
    r = _res([tau - 0.3 * xi**2 + 0.01 * xi**4 + 0.02 * xi**3 + 0.1 * xi])
    r.factors[0].kappa_support = [1.0, 2.0]
    t, x, u = grid(case("heat"))
    rep = validate(r, u, t, x, 0.0)
    assert rep.stats["v02_min_margin"] == -3 and [c for c, _ in rep.flags if c == "V0.2"]


def test_v01_growing_mode_does_not_overflow():
    """A candidate factor with growing modes (backward heat) made exp(lambda t) overflow and the
    least-squares SVD fail; columns are scaled per mode, so the statistic stays finite and the
    decaying-mode statistics are unchanged."""
    f = case("transport_plus_diffusion")
    t, x, u = grid(f)
    sig = 1e-2 * np.std(u)
    un = u + sig * np.random.default_rng(0).standard_normal(u.shape)
    t_long = t * 200.0  # Re(lambda) t up to ~kappa^2 * 200 * T: overflows without scaling
    bins = predictive_bins([tau + xi, tau + 0.3 * xi**2], un, t_long, x, sig)
    assert bins and all(np.isfinite(b[1]) for b in bins)
    from pdefactor.validate import branch_roots, fft_x  # unscaled columns where nothing overflows
    kappa, U = fft_x(un, x)
    var = sig**2 / un.shape[1]
    for k, stat, _, _ in predictive_bins([tau + xi, tau - 0.3 * xi**2], un, t, x, sig):
        if k <= 0:
            continue
        j = int(np.argmin(np.abs(kappa - k)))
        lams = np.concatenate([branch_roots(q, k) for q in [tau + xi, tau - 0.3 * xi**2]])
        Z = np.exp(np.outer(t - t[0], lams))
        r = U[:, j] - Z @ np.linalg.lstsq(Z, U[:, j], rcond=None)[0]
        assert abs(2 * np.vdot(r, r).real / var - stat) <= 1e-6 * max(1.0, stat)
