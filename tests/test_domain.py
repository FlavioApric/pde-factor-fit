"""S-DOMAIN: extractors, data-level structured fit and quadtree on non-periodic cells."""
import numpy as np
import pytest

from pdefactor.core.variety import PolySymbol
from pdefactor.domain.extract import cadzow_2d, extract_esprit
from pdefactor.domain.fit import analyze_cell
from pdefactor.domain.kernelfit import CellData, _pack
from pdefactor.domain.quadtree import CellFit, admissible, quadtree
from pdefactor.synthetic import case


def _cell(name, L, nz, seed=1, nt=64, T=2.0):
    f = case(name)
    nx = int(round(128 * L / (2 * np.pi)))
    t = np.linspace(0, T, nt)
    x = np.linspace(0, L, nx, endpoint=False)
    TT, XX = np.meshgrid(t, x, indexing="ij")
    u = f(TT, XX)
    sig = nz * np.std(u)
    return t, x, u + sig * np.random.default_rng(seed).standard_normal(u.shape), sig


def _two_field(nz=1e-3, x_if=np.pi, nt=64, T=2.0):
    ft, fh = case("transport"), case("heat")
    t = np.linspace(0, T, nt)
    x = np.linspace(0, 2 * np.pi, 128, endpoint=False)
    TT, XX = np.meshgrid(t, x, indexing="ij")
    chi = 0.5 * (1 + np.tanh((XX - x_if) / 0.15))
    u = (1 - chi) * ft(TT, XX) + chi * fh(TT, XX)
    sig = nz * np.std(u)
    return t, x, u + sig * np.random.default_rng(2).standard_normal(u.shape), sig


def _coef(Q, k=0):
    return np.asarray(Q.coeffs[k])


def test_esprit_x_exact_window():
    """Exact heat field on a non-periodic window: x-first ESPRIT gives kappa and lam exactly."""
    t, x, u, _ = _cell("heat", np.pi, 0.0)
    e = extract_esprit(u, t, x, 0.0)
    m = e.modes
    assert len(m) == 12
    assert np.allclose(np.sort(np.abs(m.kappa)), np.repeat(np.arange(1, 7), 2), atol=1e-6)
    assert np.allclose(m.lam.real, -0.3 * m.kappa**2, atol=1e-6)


def test_cadzow_keeps_low_rank_and_denoises():
    t, x, u0, _ = _cell("heat", np.pi, 0.0)
    rng = np.random.default_rng(0)
    assert np.allclose(cadzow_2d(u0, 12, iters=2), u0, atol=1e-8)
    noisy = u0 + 1e-2 * rng.standard_normal(u0.shape)
    d = cadzow_2d(noisy, 12, iters=5)
    assert np.linalg.norm(d - u0) < 0.5 * np.linalg.norm(noisy - u0)


def test_varpro_gradient():
    t, x, u, sig = _cell("transport_plus_diffusion", np.pi, 1e-3)
    c = CellData(u, t, x, sig)
    st = ((1, 1), (1, 2))
    th = _pack([PolySymbol(1, [np.array([0.1, 0.9], complex)]), PolySymbol(1, [np.array([0, 0.1, -0.25], complex)])])
    _, g = c.rss_grad(th, st)
    h = 1e-6
    gn = np.array([(c.rss_grad(th + h * e, st)[0] - c.rss_grad(th - h * e, st)[0]) / (2 * h) for e in np.eye(len(th))])
    assert np.allclose(g, gn, rtol=1e-3, atol=1e-4 * np.abs(g).max())


@pytest.mark.parametrize("name,structure,coefs", [
    ("transport_plus_diffusion", ((1, 1), (1, 2)), [(1, 1.0), (2, -0.3)]),
    ("wave", ((1, 1), (1, 1)), [(1, 1.0), (1, -1.0)]),
])
def test_structure_on_L_pi_noise_1e3(name, structure, coefs):
    """Done criterion (plan v2.2): right structure on the non-periodic window L = pi at noise 1e-3."""
    t, x, u, sig = _cell(name, np.pi, 1e-3)
    r = analyze_cell(u, t, x, sig, extractor="esprit_x")
    b = r["best"]
    assert b.structure == structure
    assert r["ranked"][0][2] > 0.9
    assert b.rss / (b.n * b.sigma**2) < 1.1  # fits to the noise level
    # leading xi coefficient of each factor (degree d of its slot)
    lead = sorted(complex(_coef(Q)[d]).real for Q, (_, d) in zip(b.factors, b.structure))
    assert np.allclose(lead, sorted(c for _, c in coefs), atol=2e-3), lead


def test_two_regime_halves():
    """Each half of the two-regime field (glue zone excluded) returns its own law."""
    t, x, u, sig = _two_field()
    left = analyze_cell(u[:, :54], t, x[:54], sig, extractor=None)["best"]
    right = analyze_cell(u[:, 74:], t, x[74:], sig, extractor=None)["best"]
    assert left.structure == ((1, 1),)
    assert np.allclose(_coef(left.factors[0]), [0, 1], atol=5e-3)
    assert right.structure == ((1, 2),)
    assert np.allclose(_coef(right.factors[0]), [0, 0, -0.3], atol=5e-3)


def test_admissible_rules():
    q = PolySymbol(1, [np.array([0, 1], complex)])
    cf = CellFit((0, 1), (0, 1), 0.0, ((1, 1), (1, 1)), [q, q], [], 0.0, 1, gamma=0.001, n_kappa=[5, 5])
    assert not admissible(cf, 0.02)[0]
    cf.gamma, cf.n_kappa = 0.5, [5, 1]
    assert not admissible(cf, 0.02)[0]
    cf.n_kappa = [2, 2]
    assert admissible(cf, 0.02)[0]


def test_quadtree_finds_interface():
    """Two-regime field: the first split is in x near pi; the left side carries transport.
    (At depth 1 the right child still holds the glue zone x in [pi, pi + 0.5], a mixture of both laws; heat on the
    clean right side is checked by test_two_regime_halves and by the depth-2 run, REPORT.md section 4.)"""
    t, x, u, sig = _two_field(nt=32)
    root, leaves, _ = quadtree(u, t, x, sig, max_depth=1, fracs_x=(0.375, 0.5, 0.625), fracs_t=(), extractor=None)
    assert root.split is not None and root.split[0] == "x"
    assert abs(x[root.split[1]] - np.pi) < 0.5
    lt = next(kid for kid in root.children if kid.ix[0] == 0)
    def transport(Q):  # tau + xi, possibly held in a higher-dx slot with ~0 top coefficients
        c = np.r_[_coef(Q), np.zeros(3)]
        return Q.m == 1 and abs(c[1] - 1) < 0.05 and abs(c[0]) < 0.05 and np.all(np.abs(c[2:]) < 0.05)

    assert any(transport(Q) for Q in lt.factors), lt.law()
