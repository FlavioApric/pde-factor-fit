"""Contract of the main-pipeline interfaces the learned layers use (branch learned-layers, see
analysis/ML_INTEGRATION.md). A main change that would break a layer fails here instead of at
integration: rename or re-sign one of these only together with the layers that call it."""
import dataclasses
import inspect

import numpy as np


def _params(f):
    return list(inspect.signature(f).parameters)


def test_core_entry_points_keep_their_signatures():
    from pdefactor.core import spectral, structfit

    assert _params(structfit._dist)[:3] == ["Q", "lam", "kappa"]
    assert _params(structfit.sigma_lambda)[:3] == ["modes", "t", "bin_noise"]
    p = _params(structfit.extract_modes_ic)
    assert p[:4] == ["u", "t", "x", "noise"] and "seeds" in p and "noise_draws" in p
    assert _params(spectral.fft_x)[:2] == ["u", "x"]
    p = _params(structfit.analyze_structured)
    assert p[:4] == ["u", "t", "x", "noise"] and {"real", "structures", "noise_draws"} <= set(p)
    assert structfit.SEED_PROVIDER is None  # L0 hook present and off by default


def test_loop_helpers_keep_their_signatures():
    from pdefactor import loop, refine_raw

    assert _params(loop._poly_symbol) == ["q"]
    assert _params(loop._coef_dict) == ["q"]
    assert _params(loop._sympy_of) == ["f"]
    assert _params(refine_raw._basis) == ["syms", "ts", "xs", "period", "kmax", "real"]
    p = _params(loop.run_loop)
    assert p[:5] == ["samples", "t", "x", "sigma", "pis"]
    assert {"bounds", "refine", "grow", "noise_draws", "raw", "bootstrap"} <= set(p)


def test_result_fields_the_layers_read():
    from pdefactor import loop

    lr = {f.name for f in dataclasses.fields(loop.LoopResult)}
    assert {"label", "factors", "p_k", "structures", "labels", "agg", "note", "split", "evidence"} <= lr
    fr = {f.name for f in dataclasses.fields(loop.FactorReport)}
    assert {"sympy", "W", "coef", "status", "kappa_support"} <= fr


def test_run_loop_output_shape_on_heat():
    """End to end on exact-ish heat data: the label vocabulary (rule 5) and the per-factor coefficient
    triples (median, q05, q95) the calibration and feature layers consume."""
    from pdefactor.loop import run_loop
    from pdefactor.synthetic import any_case, grid

    f = any_case("heat")
    t, x, u = grid(f)
    sig = 0.01 * np.std(u)
    r = run_loop([u + sig * np.random.default_rng(0).standard_normal(u.shape)], t, x, sig, bootstrap=0)
    assert r.label in {"FIT-COMPATIBLE", "MISFIT", "ID-KER", "UNDECIDED"}
    assert r.factors and isinstance(r.note, str)
    for fr in r.factors:
        for k, v in fr.coef.items():
            assert len(k) == 2 and len(v) == 3
        assert isinstance(fr.kappa_support, list)


def test_tunable_knobs_still_exist():
    """Module constants the learned calibration and controller read or set (PHASE4_ML_PLAN knob
    inventory). A knob may change value or meaning only together with the layers' knob tables."""
    from pdefactor import loop
    from pdefactor.core import structfit

    for name in ("START_BOUNDS", "P_CONCENTRATED", "CAP", "PRED_LOGP", "W_DRAWS", "LOG_BF_STRONG", "LOG_BF_BARE",
                 "SPLIT_PROPOSE", "ALT_TOP", "M_LIMIT", "DX_LIMIT"):
        assert hasattr(loop, name), name
    assert loop.ALT_TOP is None or loop.ALT_TOP >= 1
    assert hasattr(structfit, "SEED_PROVIDER")
