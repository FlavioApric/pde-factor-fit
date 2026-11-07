"""S-INTERP: GP posterior samples with weights, coverage, EPGP factor-wise prior, core bridge."""
import numpy as np
import pytest

pytest.importorskip("torch")  # optional extras: pip install -e ".[ml]"
import sympy as sp
from scipy.stats import norm

from pdefactor.interp import factor_set_posterior, fit_gp, run_core_on_samples, smoother
from pdefactor.interp.epgp import fit_epgp
from pdefactor.interp.gp import GPPosterior
from pdefactor.symbols import tau, xi
from pdefactor.synthetic import case, grid, sample_scattered


@pytest.fixture(scope="module")
def heat_post():
    f = case("heat")
    t, x, y, s = sample_scattered(f, 400, noise=0.05, rng=1)
    tg, xg, u = grid(f, nt=48, nx=64)
    return fit_gp(t, x, y, grid=(tg, xg), S=16, H=8, families=("rbf",), method="laplace"), s, u


def test_gp_shapes_and_weights(heat_post):
    p, s, u = heat_post
    assert p.samples.shape == (len(p.weights), 48, 64)
    assert len(p.weights) >= 12
    assert np.all(p.weights >= 0) and abs(p.weights.sum() - 1) < 1e-12
    assert abs(p.comp_weights.sum() - 1) < 1e-12
    assert np.all(np.isfinite(p.samples))
    assert s / 1.5 < p.sigma_hat < 1.5 * s


def test_gp_coverage_loose(heat_post):
    """Loose bound (one realisation); the strict ±5 check is the REPORT benchmark."""
    p, _, u = heat_post
    c = p.coverage(u)
    assert 0.78 <= c[0.9] <= 0.99
    assert c[0.5] < c[0.9] < c[0.95]


def test_samples_match_marginals(heat_post):
    """Matheron samples agree with the exact marginals: standardised deviations ~ N(0, 1)."""
    p, _, _ = heat_post
    z = (p.samples - p.mean[None]) / np.sqrt(p.var)[None]
    assert abs(z.mean()) < 0.15 and 0.8 < z.std() < 1.2


def test_subset_path_for_large_n():
    """n > n_exact: the exact path on a random subset (conservative), flagged in info."""
    f = case("heat")
    t, x, y, _ = sample_scattered(f, 500, noise=0.05, rng=4)
    p = fit_gp(t, x, y, grid=(16, 16), S=4, H=4, families=("rbf",), n_exact=200)
    assert p.info["method"] == "subset" and p.info["n_used"] == 200 and p.info["n"] == 500
    assert p.samples.shape == (len(p.weights), 16, 16) and np.all(np.isfinite(p.samples))


def test_pit_mixture_matches_scipy():
    m = np.array([[[0.0]], [[1.0]]])
    sd = np.array([[[1.0]], [[2.0]]])
    w = np.array([0.3, 0.7])
    gp = GPPosterior(np.zeros(1), np.zeros(1), np.zeros((0, 1, 1)), np.zeros(0), 0.0, np.zeros(0),
                     m[0], sd[0] ** 2, m, sd, w)
    u = np.array([[0.4]])
    assert abs(gp.pit(u)[0, 0] - (0.3 * norm.cdf(0.4) + 0.7 * norm.cdf((0.4 - 1) / 2))) < 1e-12


def test_smoother():
    assert smoother("matern32") == "matern52"
    assert smoother("matern52") == "rbf"
    assert smoother("rbfe+matern12") == "rbfe+matern32"


def test_core_bridge_tpd():
    f = case("transport_plus_diffusion")
    t, x, y, _ = sample_scattered(f, 1200, noise=0.01, rng=3)
    tg, xg, _ = grid(f)
    p = fit_gp(t, x, y, grid=(tg, xg), S=4, H=4, families=("rbf",), method="laplace")
    res = run_core_on_samples(p.samples, tg, xg, p.effective_noise(), p.weights)
    assert len(res) == len(p.samples)
    assert abs(sum(w for _, w in res) - 1) < 1e-12
    post = factor_set_posterior(res)
    assert abs(sum(post.values()) - 1) < 1e-9


# ------------------------------------------------------------------ EPGP
def test_epgp_prior_draws_solve_transport():
    """A posterior draw for the single factor tau + xi is a function of x - t only."""
    f = case("transport")
    t, x, y, _ = sample_scattered(f, 300, noise=0.01, rng=0)
    e = fit_epgp(t, x, y, [tau + xi], period_x=2 * np.pi, kappa_max=8)
    xg = np.linspace(0, 2 * np.pi, 64, endpoint=False)
    late = e.sample(3, np.array([0.7]), xg, seed=1)  # same seed -> same weight draws
    early = e.sample(3, np.array([0.0]), xg - 0.7, seed=1)
    assert np.max(np.abs(late - early)) < 1e-9 * np.max(np.abs(early))


def test_epgp_features_on_variety():
    from pdefactor.interp.epgp import _features

    Q = tau - sp.Rational(3, 10) * xi**2
    F = _features([Q], np.array([0.0, 1.0, 2.5]), (0.0, 2.0), 1.0)
    for k, lam in zip(F.kappa, F.lam):
        assert abs(complex(Q.subs({tau: lam, xi: 1j * k}))) < 1e-12


def test_epgp_component_weights_tpd():
    f = case("transport_plus_diffusion")
    t, x, y, _ = sample_scattered(f, 1500, noise=0.01, rng=2)
    tg, xg, _ = grid(f)
    TT, XX = np.meshgrid(tg, xg, indexing="ij")
    w_true = f.weights(TT, XX)
    e = fit_epgp(t, x, y, [c.Q for c in f.components], family=smoother("rbf"), period_x=2 * np.pi, kappa_max=8)
    w = e.weights(16, tg, xg).mean(0)
    assert np.max(np.abs(w - w_true)) < 0.05


def test_ensemble_smoke():
    from pdefactor.interp.ensemble import fit_ensemble

    f = case("heat")
    t, x, y, _ = sample_scattered(f, 200, noise=0.05, rng=0)
    p = fit_ensemble(t, x, y, grid=(16, 16), M=2, steps=100)
    assert p.samples.shape == (2, 16, 16) and abs(p.weights.sum() - 1) < 1e-12
    assert np.all(np.isfinite(p.mean))
