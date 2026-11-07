"""learned/ptop.py: L2b calibrated P(top) (sessions/LEARNED/V1/PLAN.md 2.1, 4)."""
import numpy as np
import pytest

from pdefactor.learned.ptop import METHODS, PTopCalibrator, brier, ece_adaptive, sigmoid


def _data(n=2000, T=1.0, seed=0):
    rng = np.random.default_rng(seed)
    z = rng.normal(0, 2, n)
    p_true = sigmoid(z)
    y = (rng.random(n) < p_true).astype(float)
    return sigmoid(z * T), y  # reported p is over/under-confident by T


def test_metrics_hand_values():
    assert brier([1, 0, 0.5], [1, 0, 1]) == pytest.approx(0.25 / 3)
    assert ece_adaptive([0.2, 0.2, 0.8, 0.8], [0, 1, 1, 1], bins=2) == pytest.approx(0.5 * 0.3 + 0.5 * 0.2)


def test_temperature_recovers_overconfidence_and_identity():
    p, y = _data(T=3.0)
    c = PTopCalibrator("temperature").fit(p, y)
    assert c.params["T"] == pytest.approx(3.0, rel=0.15)
    p, y = _data(T=1.0, seed=1)
    assert PTopCalibrator("temperature").fit(p, y).params["T"] == pytest.approx(1.0, rel=0.15)


@pytest.mark.parametrize("method", [m for m in METHODS if m != "logit-features"])
def test_maps_are_monotone_and_improve_overconfident_scores(method):
    p, y = _data(T=3.0, seed=2)
    pt, yt = _data(T=3.0, seed=3)
    c = PTopCalibrator(method).fit(p, y)
    grid = np.linspace(0.01, 0.99, 50)
    q = c(grid)
    assert np.all(np.diff(q) >= -1e-12)
    assert np.all((q >= 0) & (q <= 1))
    if method != "raw":
        assert brier(c(pt), yt) < brier(pt, yt)


def test_logit_features_uses_features():
    rng = np.random.default_rng(4)
    n = 1500
    X = rng.normal(size=(n, 4))
    p = np.full(n, 0.7)
    y = (rng.random(n) < sigmoid(2 * X[:, 0])).astype(float)
    X[rng.random((n, 4)) < 0.05] = np.nan
    c = PTopCalibrator("logit-features").fit(p, y, X)
    q = c(p, X)
    assert brier(q, y) < brier(p, y) - 0.02


def test_raw_is_identity():
    p = np.linspace(0, 1, 11)
    assert np.array_equal(PTopCalibrator("raw").fit(p, p > 0.5)(p), p)
