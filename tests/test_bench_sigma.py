"""Benchmark inputs declare the noise std the pipeline assumes: complex fields are read as
CN(0, sigma^2) (validate.predictive_bins), so V0.1 of the true law is calibrated (chi^2/df ~ 1)."""
import os
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "benchmarks")]


def _ratio(case):
    from bench import make_input

    from pdefactor.synthetic import any_case
    from pdefactor.validate import predictive_bins

    inp = make_input(case, 0.01, "grid", 0)
    b = predictive_bins([any_case(case).P], inp["U"], inp["t"], inp["x"], inp["sigma"])
    return sum(v[1] for v in b) / sum(v[2] for v in b), np.iscomplexobj(inp["U"])


def test_true_law_v01_is_calibrated_on_real_and_complex_grids():
    assert os.environ.get("PDEFACTOR_CPLX_SIGMA", "1") == "1"
    for case in ("schrodinger", "heat"):
        r, _ = _ratio(case)
        assert 0.9 < r < 1.1, (case, r)
    assert _ratio("schrodinger")[1] and not _ratio("heat")[1]


def test_scattered_complex_raw_sigma_is_calibrated():
    """The raw scattered observations of a complex field carry sqrt(2) x the cached per-part std, so
    the raw goodness of fit of the true law is not rejected (cached schrodinger 400 inputs)."""
    import pytest
    import sympy as sp

    from bench_e2e import load_input

    from pdefactor.core.variety import PolySymbol
    from pdefactor.raw_gof import raw_gof_log10p
    from pdefactor.symbols import tau, xi
    from pdefactor.synthetic import any_case

    inp = load_input("schrodinger", 0.01, 400, 1)
    if inp is None:
        pytest.skip("no cached GP input")
    p = sp.Poly(sp.expand(any_case("schrodinger").P), tau, xi, domain="CC")
    d = {mo: complex(c) for mo, c in zip(p.monoms(), p.coeffs())}
    q = PolySymbol(1, [np.array([d.get((0, b), 0) for b in range(3)], complex)])
    assert raw_gof_log10p([q], inp["raw"])[0] > -3
