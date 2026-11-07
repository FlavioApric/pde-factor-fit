"""T98: complex-coefficient fit of a real field on the half plane kappa > 0 (env PDEFACTOR_CONJ_HALF,
off by default). A real field built from a conjugate pair {A, conj A} shows A's branch at kappa > 0 and
conj A's at kappa < 0 (Hermitian FFT); on the half plane A is fitted at its own degree, a real factor stays
real (nested real-coefficient restriction by BIC), and the reports are closed under conjugation."""
import numpy as np
import sympy as sp

from pdefactor import loop as L
from pdefactor.aggregate import aggregate, run_core
from pdefactor.core.spectral import Modes
from pdefactor.core.structfit import analyze_structured, half_plane
from pdefactor.symbols import tau, xi
from pdefactor.synthetic import Field, _amp, default_kappas, grid, modal_component


def _field(comps, seed=0):
    rng = np.random.default_rng(seed)
    K = default_kappas(2 * np.pi, 5.0)
    return Field("t", [modal_component(n, Q, K, a, rng=rng) for n, Q, a in comps])


def _close(expr, ref, tol):
    d = sp.Poly(sp.expand(expr - ref), tau, xi)
    return max(abs(complex(c)) for c in d.coeffs()) < tol if d.coeffs() else True


def test_switch_is_on_by_default():
    import os
    if os.environ.get("PDEFACTOR_CONJ_HALF") is None:
        assert L.CONJ_HALF is True  # adopted 2026-11-01


def test_half_plane_keeps_one_mirror():
    m = Modes(np.array([-1.0, 1.0, 0.0, 0.0, 2.0]), np.array([1j, -1j, 0.5j, -0.5j, -0.2 + 0j]),
              np.ones(5, complex), np.arange(5), np.ones(5))
    h = half_plane(m)
    assert sorted(h.kappa.tolist()) == [0.0, 1.0, 2.0]
    assert 0.5j in h.lam.tolist() and -0.5j not in h.lam.tolist()


def test_two_conjugate_pairs_fitted_at_their_own_degree():
    # (tau^2 + 0.09 xi^4)((tau + 0.2)^2 + 0.01 xi^4), the field of synthetic two_pairs, on a long window
    A1, A2 = tau - sp.I * sp.Float(0.3) * xi**2, tau + sp.Float(0.2) - sp.I * sp.Float(0.1) * xi**2
    f = _field([("p1", A1, _amp), ("p2", A2, lambda k: 0.6 * _amp(k))])
    t, x, u = grid(f, T=12.0, nt=192)
    full = analyze_structured(u, t, x, noise=0.0, m_max=3, dx_max=4, real=False)
    assert full.structures[0][0] != ((1, 2), (1, 2))  # the mirror needs separate factors: not A1, A2
    r = analyze_structured(u, t, x, noise=0.0, m_max=3, dx_max=4, real=False, half=True)
    assert r.structures[0][0] == ((1, 2), (1, 2))
    got = [fr.sympy for fr in r.factors]
    for A in (A1, A2):
        assert any(_close(g, A, 1e-4) for g in got), (A, got)


def test_real_factor_stays_real_and_reports_are_conjugation_closed():
    # a real transport factor and one conjugate pair: tau + xi and tau - 0.3 i xi^2 (+ conjugate)
    A = tau - sp.I * sp.Float(0.3) * xi**2
    f = _field([("tr", tau + xi, _amp), ("p", A, lambda k: 0.7 * _amp(k))], seed=1)
    t, x, u = grid(f, T=12.0, nt=192)
    res = run_core([u], t, x, 0.0, m_max=3, dx_max=4, real=False, half=True)
    r = res[0][0]
    coefs = [complex(c) for fr in r.factors for c in sp.Poly(fr.sympy, tau, xi).coeffs()]
    assert any(_close(fr.sympy, tau + xi, 1e-4) for fr in r.factors)
    tr = next(fr for fr in r.factors if _close(fr.sympy, tau + xi, 1e-4))
    assert all(abs(complex(c).imag) == 0 for c in sp.Poly(tr.sympy, tau, xi).coeffs())
    assert any(abs(c.imag) > 0.1 for c in coefs)
    reps = L._half_plane_reports(aggregate(res), 1)
    assert reps is not None and len(reps) == 3
    assert L._conj_closed(reps)
    assert abs(sum(fr.W for fr in reps) - 1.0) < 1e-9
    # the product is the real annihilator (tau + xi)(tau^2 + 0.09 xi^4)
    P = sp.expand(sp.Mul(*[fr.sympy for fr in reps]))
    assert _close(P, sp.expand((tau + xi) * (tau**2 + sp.Float(0.09) * xi**4)), 1e-3)


def _grid_obs_noisy(f, sigma=1e-3, seed=0):
    t, x, u = grid(f, T=4.0, nt=64, nx=64)
    u = u + sigma * np.random.default_rng(seed).standard_normal(u.shape)
    return L._grid_obs(u, t, x, sigma)


def test_branch_ard_is_on_by_default_and_never_below_the_per_bin_evidence():
    import os

    from pdefactor import refine_raw as R
    if os.environ.get("PDEFACTOR_BRANCH_ARD") is None:
        assert R.BRANCH_ARD is True  # adopted 2026-11-01
    f = _field([("tr", tau + xi, _amp)])
    obs = _grid_obs_noisy(f)
    syms = [L._poly_symbol(tau + xi)]
    assert R.log_evidence_branch(syms, obs, 6) >= R.log_evidence(syms, obs, 6) - 1e-6


def test_branch_ard_frees_only_the_unexcited_conjugate_branches():
    # the real law tau^2 + 0.09 xi^4 (scored by its factor A, the real span holds conj A's kernel):
    # data exciting only A's roots at kappa > 0 (chiral) are charged the prior volume of every conj-A
    # root under one scale per bin; data exciting both roots (the real beam) are not
    from pdefactor import refine_raw as R
    A = tau - sp.I * sp.Float(0.3) * xi**2
    syms = [L._poly_symbol(A)]
    chiral = _grid_obs_noisy(_field([("p", A, _amp)]))
    both = _grid_obs_noisy(_field([("b", tau**2 + sp.Float(0.09) * xi**4, _amp)]))
    gap = lambda o: R.log_evidence_branch(syms, o, 6) - R.log_evidence(syms, o, 6)  # noqa: E731
    g_chiral, g_both = gap(chiral), gap(both)
    assert g_chiral > 20.0
    assert g_both < 0.25 * g_chiral
