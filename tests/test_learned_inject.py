"""Corpus I generators (analysis/exp/ll_inject.py; sessions/LEARNED/V1/PLAN.md 1.2)."""
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "benchmarks" / "ml_layers"))
import ll_inject as I  # noqa: E402

from pdefactor.simulator import FAMILIES, random_pde  # noqa: E402
from pdefactor.synthetic import branch_roots, grid  # noqa: E402


@pytest.mark.parametrize("family", FAMILIES)
def test_solver_reproduces_the_exact_field(family):
    """eps = 0: the integrating-factor solver is the modal sum (any order, any factor structure)."""
    d = random_pde(family, 401)
    t, x, u = grid(d.field)
    U = I.solve(d.field, d.factors, t, x)
    assert np.abs(U - u).max() <= 1e-8 * np.abs(u).max()


@pytest.mark.parametrize("kind", ["two_laws", "nonlinear", "varcoef", "fractional"])
def test_law_types_clean_at_zero_and_hit_z(kind):
    d = random_pde("F3", 402)
    t, x, u0 = grid(d.field)
    sig = I.NOISE * np.std(u0)
    prm = {"g": list(np.random.default_rng(0).standard_normal(16)), "alpha": 0.7}
    assert np.abs(I.law_field(kind, d, t, x, 0.0, prm) - u0).max() <= 1e-8 * np.abs(u0).max()
    for z in (2.0, 32.0):
        eps = I.calibrate_eps(kind, d, t, x, u0, sig, z, prm)
        assert I.zscore(I.law_field(kind, d, t, x, eps, prm), u0, sig) == pytest.approx(z, rel=0.05)


def test_two_laws_is_continuous_and_changes_only_after_the_switch():
    d = random_pde("F4", 400)
    t, x, u0 = grid(d.field)
    prm = {"g": list(np.random.default_rng(1).standard_normal(16))}
    u = I.law_field("two_laws", d, t, x, 0.3, prm)
    k = len(t) // 2
    assert np.abs(u[: k + 1] - u0[: k + 1]).max() <= 1e-8 * np.abs(u0).max()
    assert np.abs(u[k + 2:] - u0[k + 2:]).max() > 1e-3 * np.abs(u0).max()


@pytest.mark.parametrize("rho", [0.0, 0.3, 0.9])
def test_ar1_noise(rho):
    e = I.ar1_noise(np.random.default_rng(2), (256, 256), rho)
    assert e.var() == pytest.approx(1.0, rel=0.05 if rho < 0.9 else 0.25)
    for ax in (0, 1):
        a, b = np.moveaxis(e, ax, 0)[1:], np.moveaxis(e, ax, 0)[:-1]
        assert (a * b).mean() / e.var() == pytest.approx(rho, abs=0.05)


@pytest.mark.parametrize("signal", [True, False])
@pytest.mark.parametrize("ratio", [1.0, 5.0, 20.0])
def test_hetero_profile(signal, ratio):
    d = random_pde("F2", 400)
    t, x, u = grid(d.field)
    h = I.hetero_profile(u, t, ratio, signal)
    assert np.mean(h**2) == pytest.approx(1.0)
    assert h.max() / h.min() == pytest.approx(ratio, rel=1e-6)


@pytest.mark.parametrize("family", FAMILIES)
@pytest.mark.parametrize("r", I.LEVELS["aliasing"])
def test_aliasing_frame_shift(family, r):
    d = random_pde(family, 403)
    t, _, _ = grid(d.field)
    dt = t[1] - t[0]
    a, V = I._aliased_draw(d, r, dt)
    im = max(np.abs(c.lams.imag).max() for c in a.field.components)
    assert im * dt / np.pi == pytest.approx(r, rel=1e-9)
    for c0, c in zip(d.field.components, a.field.components):
        assert np.allclose(c.lams.real, c0.lams.real)  # damping kept
        lam = branch_roots(c.Q, c.kappas[0])
        assert np.min(np.abs(lam - c.lams[0])) < 1e-6 * max(1.0, abs(c.lams[0]))  # still the law's root


@pytest.mark.parametrize("kind", I.TYPES)
def test_inject_input_is_reproducible(kind):
    a = I.inject_input(kind, 0, "F1", 400)
    b = I.inject_input(kind, 0, "F1", 400)
    assert np.array_equal(a["grid_data"], b["grid_data"])
    assert a["inject"]["type"] == kind and a["inject"]["level"] == 0


def test_feasibility_subset_is_balanced():
    from collections import Counter

    t = I.subset_tasks()
    assert len(t) == len(set((f, s, tuple(d)) for _, f, s, d, _ in t)) == 140
    assert set(Counter(f for _, f, *_ in t).values()) == {28}
    assert set(Counter(d[0].split(":")[0] for *_, d, _ in t).values()) == {20}
    assert set(Counter((f, d[0].split(":")[0]) for _, f, _, d, _ in t).values()) == {4}
    assert Counter(s for _, _, s, *_ in t) == {400: 105, 402: 18, 403: 17}
