"""Fast smoke tests for S-BASELINES-BENCH (baselines + benchmark harness)."""
import sys
from pathlib import Path

import numpy as np
import pytest
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from benchmarks import metrics as M  # noqa: E402
from benchmarks.bench import make_input, run_method  # noqa: E402
from benchmarks.interp import griddata_placeholder  # noqa: E402
from pdefactor.baselines import bopdmd, factor_symbol, pdefind, weak_sindy  # noqa: E402
from pdefactor.synthetic import case, grid  # noqa: E402


@pytest.mark.parametrize("coeffs,st", [
    ({(2, 0): 1, (0, 2): -1.0}, ((1, 1), (1, 1))),                              # wave
    ({(2, 0): 1, (1, 2): -0.3, (1, 1): 1, (0, 3): -0.3}, ((1, 1), (1, 2))),      # transport x diffusion
    ({(2, 0): 1, (1, 0): 0.8, (0, 2): -1.0}, ((2, 2),)),                        # telegraph: irreducible
    ({(2, 0): 1, (0, 4): 0.09}, ((1, 2), (1, 2))),                              # beam over Q(i)
])
def test_factor_symbol_structures(coeffs, st):
    facs, got = factor_symbol(coeffs)
    assert got == st
    prod = sp.expand(sp.prod(facs))
    # refined factors reproduce P
    from pdefactor.symbols import tau, xi
    P = sum(c * tau**a * xi**b for (a, b), c in coeffs.items())
    assert M.coef_dist(sp.expand(P), prod) < 1e-6


def _transport():
    f = case("transport")
    t, x, u = grid(f)
    return f, t, x, u


@pytest.mark.parametrize("fn", [pdefind, weak_sindy, bopdmd])
def test_baselines_recover_transport_exact(fn):
    f, t, x, u = _transport()
    r = fn(u, t, x)
    s = M.score("transport", f, t, x, r.factors)
    assert s["factor_set"], (r.method, r.P, r.factors)
    assert r.structure == ((1, 1),)


def test_placeholder_interpolator():
    f, t, x, u = _transport()
    rng = np.random.default_rng(0)
    ts, xs = rng.uniform(0, 2, 2000), rng.uniform(0, 2 * np.pi, 2000)
    U, s = griddata_placeholder(ts, xs, f(ts, xs), t, x, 2 * np.pi, sigma=0.0)
    assert U.shape == u.shape and np.isfinite(U).all()
    assert s > 0  # interpolation error is not zero
    assert np.sqrt(np.mean((U - u) ** 2)) < 0.2 * np.std(u)


def test_pluggable_interpolator():
    calls = []

    def exact(ts, xs, ys, t, x, L, sigma=0.0, seed=0):
        calls.append(len(ys))
        f = case("heat")
        return grid(f)[2], sigma

    inp = make_input("heat", 0.0, 400, 0, interpolator=exact)
    assert calls == [400] and inp["sigma"] == 0.0


@pytest.mark.parametrize("method", ["core_v2", "core_v1", "pdefind", "weak_sindy", "ensemble_sindy",
                                    "sbr_sindy", "bopdmd"])
def test_run_method_row(method):
    if method == "sbr_sindy":
        pytest.importorskip("numpyro")  # pysindy.SBR needs the optional Bayesian extras (pip install -e ".[ml]")
        import pysindy
        if not hasattr(pysindy, "SBR"):
            pytest.skip("this pysindy build has no SBR")
    inp = make_input("heat", 1e-3, "grid", 0)
    row = run_method(method, "heat", inp, sbr_kw={"num_warmup": 50, "num_samples": 50, "n_struct": 20})
    assert row["error"] is None, row.get("trace")
    for k in ("factor_set", "coef_err", "runtime", "label", "structure", "true_structure", "struct_ok"):
        assert k in row
    if method in ("core_v2", "core_v1", "weak_sindy"):
        assert row["factor_set"]
    if method in ("core_v2", "ensemble_sindy", "sbr_sindy"):
        assert row["probs"] and abs(sum(p for _, p in row["probs"]) - 1) < 0.05


def test_calibration_metrics():
    p = np.array([0.05, 0.05, 0.95, 0.95])
    y = np.array([0, 0, 1, 1])
    assert M.ece(p, y) == pytest.approx(0.05)
    assert M.brier(p, y) == pytest.approx(0.0025)
    rows = M.reliability(p, y, bins=10)
    assert sum(r[4] for r in rows) == 4


def test_true_weights_tpd():
    f = case("transport_plus_diffusion")
    t, x, _ = grid(f)
    w = M.true_weights("transport_plus_diffusion", f, t, x)
    assert w is not None and abs(sum(w.values()) - 1) < 1e-9
    assert M.true_weights("beam", case("beam"), t, x) is None
