"""T86: raw goodness of fit of the reported law on scattered observations."""
import numpy as np

from pdefactor.core.variety import PolySymbol


def _sym(m, coeffs):
    return PolySymbol(m, [np.array(c, complex) for c in coeffs])


def _field(rng, n, sig):
    """u = e^{-0.1 t} cos x + 0.5 e^{-0.9 t} sin 3x: heat u_t = 0.1 u_xx (kappa 1, 3) at 400 points."""
    ts, xs = rng.uniform(0, 2, n), rng.uniform(0, 2 * np.pi, n)
    ys = np.exp(-0.1 * ts) * np.cos(xs) + 0.5 * np.exp(-0.9 * ts) * np.sin(3 * xs)
    return dict(ts=ts, xs=xs, ys=ys + sig * rng.standard_normal(n), period=2 * np.pi, sigma=sig)


def test_true_law_passes_and_is_calibrated():
    """Under the true law the test is a chi^2 test at its nominal level: no rejection at log10 p < -3
    on 20 noise seeds."""
    from pdefactor.raw_gof import raw_gof_log10p

    heat = _sym(1, [[0, 0, -0.1]])  # tau - 0.1 xi^2 (xi = i kappa)
    lps = [raw_gof_log10p([heat], _field(np.random.default_rng(s), 400, 0.05))[0] for s in range(20)]
    assert min(lps) > -3


def test_wrong_law_that_misses_a_mode_fails():
    """A law with the wrong decay at kappa = 3 (diffusion 0.02 instead of 0.1) leaves the sin 3x mode
    in the residual: rejected far below the V0.1 level."""
    from pdefactor.raw_gof import raw_gof_log10p

    wrong = _sym(1, [[0, 0, -0.02]])
    assert raw_gof_log10p([wrong], _field(np.random.default_rng(0), 400, 0.05))[0] < -10
