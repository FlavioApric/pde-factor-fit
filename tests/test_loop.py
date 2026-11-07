"""Outer loop (plan v2.9): grouping by factors, degree growth with held-out guard, regroup at fixed k,
recursion per factor; and the two core additions it relies on (VarPro poles, II-C1 degree support)."""
import numpy as np
import sympy as sp

from pdefactor.aggregate import fake_posterior
from pdefactor.core.spectral import matrix_pencil
from pdefactor.core.structfit import analyze_structured, varpro_refine
from pdefactor.loop import run_loop
from pdefactor.symbols import tau, xi
from pdefactor.synthetic import case, extra_case, grid


def _coef(q, a, b):
    p = sp.Poly(sp.expand(sp.N(q)), tau, xi, domain="CC")
    return complex(dict(zip(p.monoms(), p.coeffs())).get((a, b), 0))


def _samples(f, nz=1e-3, S=3):
    t, x, u = grid(f)
    sig = nz * np.std(np.abs(u))
    s, pis = fake_posterior(u, sig, S, rng=1)
    return s, pis, t, x, sig


def test_varpro_reduces_close_pole_error():
    """Two damped poles in one bin (resolvable on T = 2): the ML poles are closer to the truth than the
    pencil's (measured: mean error 0.26/0.14 -> 0.18/0.06)."""
    tt = np.linspace(0, 2, 64)
    lam = np.array([-0.3 + 2.0j, -0.8 + 4.5j])
    y0 = np.exp(np.outer(tt, lam)) @ np.array([1.0, 0.6])
    e_p, e_v = [], []
    for s in range(40):
        rng = np.random.default_rng(s)
        y = y0 + 0.05 * (rng.standard_normal(64) + 1j * rng.standard_normal(64))
        lp = matrix_pencil(y, tt[1] - tt[0], order=2)[0]
        lv = varpro_refine(y, tt, lp)
        e_p.append(np.abs(np.sort_complex(lp) - np.sort_complex(lam)).max())
        e_v.append(np.abs(np.sort_complex(lv) - np.sort_complex(lam)).max())
    assert np.mean(e_v) < np.mean(e_p)


def test_core_flags_unsupported_tau_degree():
    """tau + 0.002 xi^5 is outside dx <= 4: the core used to return an irreducible (2, 4) factor that
    fits the one observed branch and invents the second. II-C1: it is now ID-KER with a reason."""
    t, x, u = grid(extra_case("fifth_order"))
    r = analyze_structured(u, t, x, real=True)
    assert r.label == "ID-KER"
    assert "II-C1" in r.info["reason"]
    r5 = analyze_structured(u, t, x, real=True, dx_max=5)
    assert r5.label == "FIT-COMPATIBLE" and len(r5.factors) == 1
    assert abs(_coef(r5.factors[0].sympy, 0, 5) - 0.002) < 1e-6


def test_loop_heat_single_factor_no_growth():
    s, pis, t, x, sig = _samples(case("heat"))
    r = run_loop(s, t, x, sig, pis, report_domain=True)
    assert r.label == "FIT-COMPATIBLE"
    assert max(r.p_k, key=r.p_k.get) == 1 and len(r.factors) == 1
    assert abs(_coef(r.factors[0].sympy, 0, 2) + 0.3) < 2e-3
    assert len(r.history) == 1  # nothing to grow
    sh = r.domain["share"]
    assert np.allclose(sh.sum(0), 1.0)
    assert "tau" in r.equation()


def test_loop_groups_by_factors_tpd():
    s, pis, t, x, sig = _samples(case("transport_plus_diffusion"))
    r = run_loop(s, t, x, sig, pis)
    assert r.label == "FIT-COMPATIBLE"
    assert max(r.p_k, key=r.p_k.get) == 2 and len(r.factors) == 2
    got = sorted(r.factors, key=lambda f: -f.W)
    assert abs(_coef(got[0].sympy, 0, 1) - 1.0) < 2e-3  # transport, the heavier component
    assert abs(_coef(got[1].sympy, 0, 2) + 0.3) < 2e-3  # diffusion
    assert abs(got[0].W - 0.768) < 0.05
    assert all(f.status.startswith("clean") for f in r.factors)


def test_loop_grows_degree_with_heldout_guard():
    s, pis, t, x, sig = _samples(extra_case("fifth_order"))
    r = run_loop(s, t, x, sig, pis)
    assert r.bounds == (3, 5)
    assert r.history[0].p_fit < 0.5 and r.history[1].accepted and r.history[1].heldout is not None
    assert len(r.factors) == 1
    assert abs(_coef(r.factors[0].sympy, 0, 5) - 0.002) < 1e-5
    assert r.equation().count("xi**5") == 1
