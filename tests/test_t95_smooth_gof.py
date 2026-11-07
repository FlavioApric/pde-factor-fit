"""T96: excited-band smooth residual test of the reported law on a grid (validate.smooth_residual_bins,
loop switch GRID_SMOOTH_GOF).

A fast-decaying branch that the reported law mis-places leaves a smooth residual concentrated at early
times; V0.1 spreads it over 2 (nt - r) dof per bin and misses it (F4-128 grid 5 %: report chi^2 144 on
122 dof at kappa = 10, p = 0.08), the projection on the T77 Legendre basis does not. Under the true law
the statistic is exactly chi^2, so the test must stay calibrated."""
import numpy as np

from pdefactor.symbols import tau, xi
from pdefactor.synthetic import Component, Field, grid
from pdefactor.validate import smooth_gof_log10p, smooth_residual_bins

SLOW = tau + 0.4 + 0.3 * xi
FAST = tau + 3.3 - 0.007 * xi**2 + 0.00025 * xi**4  # decay 3.3 + 0.007 k^2 + 0.00025 k^4
KS = np.arange(1.0, 11.0)


def _data(seed, noise=0.05):
    lam_s = np.array([complex(-0.4 - 0.3j * k) for k in KS])
    lam_f = np.array([complex(-(3.3 + 0.007 * k**2 + 0.00025 * k**4)) for k in KS])
    rng = np.random.default_rng(seed)
    comps = [Component("s", SLOW, KS, lam_s, rng.standard_normal(len(KS)) + 1j * rng.standard_normal(len(KS))),
             Component("f", FAST, KS, lam_f, 2.0 * (rng.standard_normal(len(KS)) + 1j * rng.standard_normal(len(KS))))]
    t, x, u = grid(Field("t95", comps))
    sig = noise * np.std(u)
    return u + sig * np.random.default_rng(100 + seed).standard_normal(u.shape), t, x, sig


def test_true_law_is_calibrated():
    lps = [smooth_gof_log10p([SLOW, FAST], *_data(s))[0] for s in range(12)]
    assert min(lps) > -3.0
    # exact chi^2 null: the adjusted p-values are not piled up near 0
    assert np.median(lps) > -1.0


def test_dispersion_without_quartic_term_is_rejected_at_high_kappa():
    # a first-order surrogate of the fast branch (its kappa <= 6 average): fits the low bins, not kappa 8-10
    bad = tau + 3.5
    lp_bad, k_bad = smooth_gof_log10p([SLOW, bad], *_data(0))
    assert lp_bad < -3.0 and abs(k_bad) >= 7
    bins, nb = smooth_residual_bins([SLOW, FAST], *_data(0))
    assert nb >= 10 and all(b[2] > 0 for b in bins)


def test_no_excited_bin_means_no_test():
    rng = np.random.default_rng(0)
    t, x = np.linspace(0, 2, 64), np.linspace(0, 2 * np.pi, 128, endpoint=False)
    u = 0.1 * rng.standard_normal((64, 128))
    assert smooth_gof_log10p([SLOW], u, t, x, 0.1) == (0.0, None)
