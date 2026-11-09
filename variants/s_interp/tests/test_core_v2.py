"""Core v2 (plan v2.1): structured fit with model comparison, confluent test, shared modes."""
import numpy as np
import pytest
import sympy as sp

from pdefactor.core.structfit import analyze_structured, candidate_structures
from pdefactor.symbols import factors as exact_factors, tau, xi
from pdefactor.synthetic import CASES, case, extra_case, grid


def _truth(name, f):
    if name == "schrodinger":
        return [tau - sp.I * sp.Float(0.3) * xi**2]
    if name == "beam":
        return [tau - sp.I * sp.Float(0.3) * xi**2, tau + sp.I * sp.Float(0.3) * xi**2]
    return [q for q, _ in exact_factors(f.P)]


def _coef_err(a, b):
    d = sp.Poly(sp.expand(sp.N(a - b)), tau, xi, domain="CC")
    return 0.0 if d.is_zero else max(abs(complex(c)) for c in d.coeffs())


def _check_factors(truth, got, tol):
    assert len(got) == len(truth), (truth, got)
    for q in truth:
        assert min(_coef_err(q, g) for g in got) < tol, (q, got)


def _noisy(u, nz, seed=5):
    sig = nz * np.std(np.abs(u))
    rng = np.random.default_rng(seed)
    e = rng.standard_normal(u.shape) + (1j * rng.standard_normal(u.shape) if np.iscomplexobj(u) else 0)
    return u + sig * e, sig


@pytest.mark.parametrize("name", CASES)
def test_exact_factor_set(name):
    f = case(name)
    t, x, u = grid(f)
    r = analyze_structured(u, t, x)
    assert r.label == "FIT-COMPATIBLE"
    _check_factors(_truth(name, f), [fr.sympy for fr in r.factors], 1e-6)
    assert not r.confluent
    assert abs(sum(p for _, _, p in r.structures) - 1) < 1e-9


@pytest.mark.parametrize("name", ["transport_plus_diffusion", "wave", "klein_gordon", "telegraph"])
def test_noisy_factor_set(name):
    """v1 fails these at 1e-3 (KG and telegraph are falsely factored by ftol, E1)."""
    f = case(name)
    t, x, u = grid(f)
    v, sig = _noisy(u, 1e-3)
    r = analyze_structured(v, t, x, noise=sig)
    assert r.label == "FIT-COMPATIBLE"
    _check_factors(_truth(name, f), [fr.sympy for fr in r.factors], 5e-3)
    assert r.structures[0][2] > 0.5


def test_weights_transport_plus_diffusion():
    f = case("transport_plus_diffusion")
    t, x, u = grid(f)
    TT, XX = np.meshgrid(t, x, indexing="ij")
    w_true = f.weights(TT, XX)
    r = analyze_structured(u, t, x)
    got = {str(fr.sympy): fr.weight for fr in r.factors}
    assert abs(got["tau + 1.0*xi"] - w_true[0]) < 1e-6
    assert abs(got["tau - 0.3*xi**2"] - w_true[1]) < 1e-6


def test_shared_kappa0_mode():
    """lam = 0 at kappa = 0 lies on both varieties: it is shared, the factors are unchanged (C12-T2)."""
    f = extra_case("tpd_shared_kappa0")
    t, x, u = grid(f)
    r = analyze_structured(u, t, x)
    assert r.label == "FIT-COMPATIBLE"
    assert r.n_shared >= 1
    _check_factors(_truth("tpd_shared_kappa0", f), [fr.sympy for fr in r.factors], 1e-6)
    v, sig = _noisy(u, 1e-3)
    r = analyze_structured(v, t, x, noise=sig)
    _check_factors(_truth("tpd_shared_kappa0", f), [fr.sympy for fr in r.factors], 5e-3)


@pytest.mark.parametrize("nz", [0.0, 1e-3])
def test_repeated_factor_is_undecided(nz):
    """(tau + xi)^2 has no finite test (OPF5B-T6): v1 returned a confident simple factor (E4)."""
    f = extra_case("repeated_transport")
    t, x, u = grid(f)
    v, sig = _noisy(u, nz) if nz else (u, 0.0)
    r = analyze_structured(v, t, x, noise=sig)
    assert r.label == "UNDECIDED"
    assert r.confluent
    assert "OPF5B-T6" in r.info["reason"]


def test_candidate_structures_canonical():
    st = candidate_structures(3, 2)
    assert len(st) == len(set(st))
    assert ((1, 1), (1, 2)) in st and ((1, 2), (1, 1)) not in st
    assert all(sum(m for m, _ in s) <= 3 for s in st)
