"""S-LEARNED layers (sessions/LEARNED/PLAN.md section 3): H0 scan, L2c interval scaling, V0 exports,
step log. The off path is tests/test_learned_off.py."""
import numpy as np
import pytest
import sympy as sp

from pdefactor.learned import apply as A
from pdefactor.learned import highk
from pdefactor.learned.config import Learned
from pdefactor.learned.features import _vand, export_factors
from pdefactor.loop import FactorReport, l2c_data, run_loop
from pdefactor.symbols import tau, xi
from pdefactor.synthetic import any_case, grid


def _transport_obs(extra, n=600, seed=0, sig=0.05):
    """cos(x - t) (+ extra * cos(6 (x - t))) on n scattered points: factor tau + xi, kappa 1 (and 6)."""
    rng = np.random.default_rng(seed)
    ts, xs = rng.uniform(0, 2, n), rng.uniform(0, 2 * np.pi, n)
    ys = np.cos(xs - ts) + extra * np.cos(6 * (xs - ts)) + sig * rng.standard_normal(n)
    f = FactorReport(tau + xi, 1.0, {(1, 0): (1, 1, 1), (0, 1): (1, 1, 1)})
    return dict(ts=ts, xs=xs, ys=ys, period=2 * np.pi, sigma=sig), f


def test_highk_scan_finds_mode_beyond_band():
    obs, f = _transport_obs(0.3)
    sc = highk.scan(obs, [f], kmax=3)
    assert sc.found == [6] and sc.proposal == 6


def test_highk_scan_quiet_on_noise():
    obs, f = _transport_obs(0.0)
    assert highk.scan(obs, [f], kmax=3).proposal is None


def test_highk_grid_scan():
    t, x = np.linspace(0, 2, 64), np.linspace(0, 2 * np.pi, 128, endpoint=False)
    TT, XX = np.meshgrid(t, x, indexing="ij")
    rng = np.random.default_rng(1)
    from pdefactor.loop import _grid_obs

    f = FactorReport(tau + xi, 1.0, {(1, 0): (1, 1, 1), (0, 1): (1, 1, 1)})
    for extra, want in ((0.05, [9]), (0.0, [])):
        u = np.cos(XX - TT) + extra * np.cos(9 * (XX - TT)) + 0.05 * rng.standard_normal(TT.shape)
        assert highk.scan(_grid_obs(u, t, x, 0.05), [f], kmax=3).found == want


def test_scale_intervals_about_median():
    f = FactorReport(tau - 0.3 * xi**2, 1.0, {(1, 0): (1 + 0j, 1 + 0j, 1 + 0j), (0, 2): (-0.3 + 0j, -0.4 + 0j, -0.25 + 0j)})
    A.scale_intervals([f], [2.0])
    assert f.coef[(1, 0)] == (1, 1, 1)
    med, lo, hi = f.coef[(0, 2)]
    assert np.isclose(med, -0.3) and np.isclose(lo, -0.5) and np.isclose(hi, -0.2)


def test_vandermonde_condition():
    assert _vand([1.0, 2.0], 0) == 0.0
    assert _vand([1.0], 2) == 16.0
    assert 0 < _vand([1.0, 2.0, 3.0], 2) < 3


@pytest.fixture(scope="module")
def heat():
    t, x, u = grid(any_case("heat"))
    rng = np.random.default_rng(7)
    sig = 0.05 * np.std(u)
    return [u + sig * rng.standard_normal(u.shape)], t, x, sig


def test_l2c_changes_intervals_only(heat, monkeypatch):
    S, t, x, sig = heat
    off = run_loop(S, t, x, sig, bootstrap=4)
    monkeypatch.setitem(A._CACHE, "l2c", A.ScaleModel("scalar", q=2.0))
    on = run_loop(S, t, x, sig, bootstrap=4, learned=Learned(intervals="coef"))
    assert on.label == off.label and [str(f.sympy) for f in on.factors] == [str(f.sympy) for f in off.factors]
    for fa, fb in zip(off.factors, on.factors):
        for k, (med, lo, hi) in fa.coef.items():
            m2, l2, h2 = fb.coef[k]
            assert np.isclose(m2, med)
            assert np.isclose(h2 - l2, 2 * (hi - lo)) or np.isclose(hi - lo, 0)
    feats = export_factors(off.factors, off.agg, off.split, l2c_data(S, np.ones(1), t, x, sig, None, None))
    assert len(feats) == len(off.factors) and np.isfinite(feats[0]["log_snr"]) and feats[0]["disagreement"] == 1.0


def test_l2c_without_model_is_off(heat, monkeypatch):
    S, t, x, sig = heat
    monkeypatch.setitem(A._CACHE, "l2c", None)
    off = run_loop(S, t, x, sig)
    on = run_loop(S, t, x, sig, learned=Learned(intervals="coef"))
    assert {str(k): v for f in off.factors for k, v in f.coef.items()} == \
        {str(k): v for f in on.factors for k, v in f.coef.items()}


def test_step_log(heat):
    S, t, x, sig = heat
    r = run_loop(S, t, x, sig)
    names = [s[0] for s in r.steps]
    assert names[0] == "core" and names[-1] == "split_layer" and "refine" in names
    assert all(s[1] >= 0 for s in r.steps)
