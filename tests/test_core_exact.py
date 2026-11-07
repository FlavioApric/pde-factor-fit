"""Phase 1 acceptance: the deterministic core on exact gridded data."""
import numpy as np
import pytest
import sympy as sp

from pdefactor.core import analyze
from pdefactor.symbols import factors as exact_factors, split_ambiguity, tau, xi
from pdefactor.synthetic import CASES, case, grid


def _poly_close(a, b, tol=1e-6):
    d = sp.Poly(sp.expand(sp.N(a - b)), tau, xi, domain="CC")
    return all(abs(complex(c)) < tol for c in d.coeffs()) if not d.is_zero else True


@pytest.mark.parametrize("name", CASES)
def test_factor_set(name):
    f = case(name)
    t, x, u = grid(f)
    r = analyze(u, t, x)
    assert r.label == "FIT-COMPATIBLE"
    # complex symbols: exact factor_list cannot coerce float*I; truth is known by construction
    if name == "schrodinger":
        truth = [tau - sp.I * sp.Float(0.3) * xi**2]
    elif name == "beam":
        truth = [tau - sp.I * sp.Float(0.3) * xi**2, tau + sp.I * sp.Float(0.3) * xi**2]
    else:
        truth = [q for q, _ in exact_factors(f.P)]
    got = [fr.sympy for fr in r.factors]
    assert len(got) == len(truth)
    for q in truth:
        assert any(_poly_close(q, g) for g in got), (q, got)


@pytest.mark.parametrize("name", ["transport", "heat", "advection_diffusion", "airy"])
def test_terms(name):
    f = case(name)
    t, x, u = grid(f)
    r = analyze(u, t, x)
    (fr,) = r.factors
    (true_terms,) = f.terms.values()
    # a(xi) convention: Q = tau - a(xi), a = sum c_n xi^n; synthetic stores the same
    for n, c in true_terms.items():
        assert abs(fr.terms[n] - complex(c)) < 1e-6


def test_weights_transport_plus_diffusion():
    f = case("transport_plus_diffusion")
    t, x, u = grid(f)
    r = analyze(u, t, x)
    TT, XX = np.meshgrid(t, x, indexing="ij")
    wt = f.weights(TT, XX)
    got = {("transport" if fr.terms and 1 in fr.terms else "diffusion"): fr.weight for fr in r.factors}
    assert abs(got["transport"] - wt[0]) < 1e-6
    assert abs(got["diffusion"] - wt[1]) < 1e-6


def test_components_sum_to_data():
    f = case("wave")
    t, x, u = grid(f)
    r = analyze(u, t, x, want_components=True)
    s = sum(r.components)
    assert np.abs(s.real - u).max() < 1e-8 * np.abs(u).max()


def test_eint_advection_diffusion_closed_form():
    f = case("advection_diffusion")
    t, x, u = grid(f)
    r = analyze(u, t, x)
    (fr,) = r.factors
    assert 0 < fr.rho <= 2.0  # |E_hat|/|u0_hat| <= 2 for AD (note, II.2 (iv)); ratio is O(1)


@pytest.mark.parametrize("P,delta", [
    (tau**2 - xi**2, 1),
    (tau**2 + xi**4, 2),
    ((tau + xi) * (tau - xi**2), 2),
])
def test_split_ambiguity_catalogue(P, delta):
    assert split_ambiguity(exact_factors(P)) == delta
