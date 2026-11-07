"""learned/resid.py: deterministic residual diagnostics for V1 (sessions/LEARNED/V1/PLAN.md 3.1)."""
import numpy as np
import pytest

from pdefactor.learned.resid import KEYS, diagnostics
from pdefactor.simulator import random_pde
from pdefactor.symbols import tau, xi
from pdefactor.synthetic import grid

T = np.linspace(0, 2.0, 64)
X = np.linspace(0, 2 * np.pi, 128, endpoint=False)


def _ar1(rng, shape, rho, axis):
    e = rng.standard_normal(shape)
    out = np.empty(shape)
    sl = [slice(None)] * 2
    sl[axis] = 0
    out[tuple(sl)] = e[tuple(sl)]
    for i in range(1, shape[axis]):
        cur, prev = [slice(None)] * 2, [slice(None)] * 2
        cur[axis], prev[axis] = i, i - 1
        out[tuple(cur)] = rho * out[tuple(prev)] + np.sqrt(1 - rho**2) * e[tuple(cur)]
    return out


def test_white_noise_is_not_flagged():
    from scipy.stats import kstest

    p = []
    for s in range(60):
        rng = np.random.default_rng(s)
        d = diagnostics([], rng.standard_normal((64, 128)), T, X)
        assert set(d) == set(KEYS)
        assert all(np.isfinite(v) for v in d.values())
        p.append(10 ** d["lb_t_logp"])
    assert kstest(p, "uniform").pvalue > 0.01


def test_correct_fit_on_a_draw_is_clean():
    dr = random_pde("F3", 100)
    t, x, u = grid(dr.field)
    rng = np.random.default_rng(1)
    un = u + 0.05 * np.std(u) * rng.standard_normal(u.shape)
    d = diagnostics(dr.factors, un, t, x)
    assert d["lb_t_logp"] > -3
    assert d["bp_logp"] > -3
    assert abs(d["acf1_t"]) < 0.1 and abs(d["acf1_x"]) < 0.1
    assert abs(d["nyq_ratio"]) < 0.3


@pytest.mark.parametrize("axis,key", [(0, "acf1_t"), (1, "acf1_x")])
def test_coloured_noise_is_seen(axis, key):
    rng = np.random.default_rng(3)
    d = diagnostics([], _ar1(rng, (64, 128), 0.6, axis), T, X)
    assert abs(d[key] - 0.6) < 0.08
    if axis == 0:
        assert d["lb_t_logp"] < -3


def test_heteroscedastic_noise_is_seen():
    rng = np.random.default_rng(4)
    e = rng.standard_normal((64, 128)) * np.exp(1.5 * T / T[-1])[:, None]
    d = diagnostics([], e, T, X)
    assert d["bp_logp"] < -3
    assert d["half_ratio"] > 0.5


def test_scale_invariance():
    """u -> 1e3 u, and t -> c t with the law rescaled (tau -> tau / c): statistics unchanged."""
    q = tau + 0.7 * xi
    rng = np.random.default_rng(5)
    TT, XX = np.meshgrid(T, X, indexing="ij")
    u = np.cos(XX - 0.7 * TT) + 0.3 * np.cos(3 * (XX - 0.7 * TT)) + 0.05 * rng.standard_normal(TT.shape)
    a = diagnostics([q], u, T, X)
    b = diagnostics([q], 1e3 * u, T, X)
    c = 4.0
    cc = diagnostics([tau + 0.7 / c * xi], u, c * T, X)
    for k in KEYS:
        assert a[k] == pytest.approx(b[k], rel=1e-8, abs=1e-10)
        assert a[k] == pytest.approx(cc[k], rel=1e-6, abs=1e-8)


def test_degenerate_inputs_do_not_raise():
    d = diagnostics([], np.zeros((64, 128)), T, X)
    assert set(d) == set(KEYS)


def test_residual_is_the_v0_projection():
    """Per kappa bin, the chi^2 of resid.residual equals validate.predictive_bins' (same projection)."""
    from pdefactor.learned.resid import residual
    from pdefactor.validate import predictive_bins

    d = random_pde("F3", 1)
    t, x, u = grid(d.field)
    sigma = 0.05 * np.std(u)
    un = u + sigma * np.random.default_rng(0).standard_normal(u.shape)
    facs = [f.sympy if hasattr(f, "sympy") else f for f in d.factors]
    kappa, _, R = residual(facs, un, t, x)
    var = sigma**2 / un.shape[1]
    for k, stat, df, _ in predictive_bins(facs, un, t, x, sigma):
        j = int(np.argmin(np.abs(kappa - k)))
        r = R[:, j].real if k == 0 else R[:, j]
        mine = np.sum(r**2) / var if k == 0 else 2 * np.sum(np.abs(r) ** 2) / var  # validate: sigma^2/(2 nx) per part
        assert np.isclose(mine, stat, rtol=1e-6), (k, mine, stat)
