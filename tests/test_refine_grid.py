"""The grid form of the refinement evidence (per DFT bin pair) equals the dense form exactly."""
import numpy as np

from pdefactor.loop import _grid_obs
from pdefactor.refine_raw import log_evidence, refine
from pdefactor.core.variety import PolySymbol
from pdefactor.synthetic import any_case, grid


def _syms(coefs, ms):
    out = []
    for c, m in zip(coefs, ms):
        cs = []
        for a in range(m):
            dx = max([b for (aa, b) in c if aa == a], default=0)
            cs.append(np.array([c.get((a, b), 0j) for b in range(dx + 1)], complex))
        out.append(PolySymbol(m, cs))
    return out


def _check(case, coefs, ms, kmax):
    f = any_case(case)
    t, x, u = grid(f)
    sig = 0.01 * np.std(np.abs(u))
    un = u + sig * np.random.default_rng(0).standard_normal(u.shape)
    if np.iscomplexobj(u):
        un = un + 1j * sig * np.random.default_rng(1).standard_normal(u.shape)
    og = _grid_obs(un, t, x, sig)
    od = {k: v for k, v in og.items() if k != "grid"}
    syms = _syms(coefs, ms)
    a, b = log_evidence(syms, og, kmax), log_evidence(syms, od, kmax)
    assert abs(a - b) < 1e-6 * abs(b), (a, b)


def test_grid_evidence_real_field():
    wave = [{(1, 0): 1, (0, 1): -1.0}, {(1, 0): 1, (0, 1): 1.0}, {(1, 0): 1, (0, 2): -0.3}]
    _check("wave_heat", wave, [1, 1, 1], 6)
    _check("wave_heat", [{(1, 0): 1, (0, 2): -0.26 + 0.01j, (0, 0): 0.3 + 0.06j}], [1], 6)  # complex factor
    _check("klein_gordon", [{(2, 0): 1, (0, 2): -1.0, (0, 0): 1.0}], [2], 5)


def test_grid_evidence_complex_field():
    _check("schrodinger", [{(1, 0): 1, (0, 2): -1j}], [1], 6)


def test_refine_same_on_grid_and_dense():
    f = any_case("heat")
    t, x, u = grid(f)
    sig = 0.01 * np.std(u)
    un = u + sig * np.random.default_rng(0).standard_normal(u.shape)
    og = _grid_obs(un, t, x, sig)
    od = {k: v for k, v in og.items() if k != "grid"}
    c = [{(1, 0): 1, (0, 2): -0.29, (0, 1): 0.01}]
    ra, rb = refine(c, [1], og, 5), refine(c, [1], od, 5)
    # same objective on both paths; with the pooled prior (T77) the grid profiles the scales by
    # vectorised search and the dense path by L-BFGS, so they agree to the optimisers' tolerance
    assert abs(ra["logev"] - rb["logev"]) < 1e-2 and ra["active"] == rb["active"]


def test_vectorised_grid_spectrum_equals_reference():
    """_grid_spectrum (batched roots, array-built blocks) gives the reference's eigenvalues and
    projections, for factors of order 1-3, real and complex coefficients, real and complex fields."""
    from pdefactor.refine_raw import _grid_spectrum, _grid_spectrum_ref

    sets = [("wave_heat", [{(1, 0): 1, (0, 1): -1.0}, {(1, 0): 1, (0, 2): -0.3}], [1, 1]),
            ("klein_gordon", [{(2, 0): 1, (1, 1): 0.5, (0, 2): -1.0, (0, 0): 1.0}], [2]),
            ("cubic_tau", [{(3, 0): 1, (2, 0): 0.6, (1, 2): -1.0, (1, 0): 1.0, (0, 0): 0.2}], [3]),
            ("beam", [{(1, 0): 1, (0, 2): 0.3j}, {(1, 0): 1, (0, 2): -0.3j}], [1, 1]),
            ("schrodinger", [{(1, 0): 1, (0, 2): -0.3j, (0, 1): 0.02 + 0.01j}], [1])]
    for case, coefs, ms in sets:
        f = any_case(case)
        t, x, u = grid(f)
        sig = 0.01 * np.std(np.abs(u))
        og = _grid_obs(u + sig * np.random.default_rng(0).standard_normal(u.shape), t, x, sig)
        syms = _syms(coefs, ms)
        for real in ((True, False) if np.isrealobj(u) else (False,)):
            a = _grid_spectrum(syms, og["grid"], og["period"], 6, real, sig)
            b = _grid_spectrum_ref(syms, og["grid"], og["period"], 6, real, sig)
            assert np.allclose(np.sort(a[0]), np.sort(b[0]), rtol=1e-8), case
            assert np.isclose(a[1].sum(), b[1].sum(), rtol=1e-8) and np.isclose(a[2], b[2], rtol=1e-8, atol=1e-8), case


def _heat_obs(n=120, seed=1, sig=0.05):
    rng = np.random.default_rng(seed)
    ts, xs = rng.uniform(0, 2, n), rng.uniform(0, 2 * np.pi, n)
    y = sum(a * np.exp(-0.3 * k**2 * ts) * np.cos(k * xs + p) for k, a, p in [(1, 1.0, 0.3), (2, 0.4, 1.0)])
    return dict(ts=ts, xs=xs, ys=y + sig * rng.standard_normal(n), period=2 * np.pi, sigma=sig)


def test_per_bin_evidence_equals_dense_maximum(monkeypatch):
    """T76: the per-bin evidence is the dense Gaussian log density maximised over one prior scale
    per |n| bin (brute force), and is never below the shared-scale evidence (nested)."""
    import sympy as sp
    from scipy.optimize import minimize
    from scipy.stats import multivariate_normal

    import pdefactor.refine_raw as RR
    from pdefactor.loop import _poly_symbol
    from pdefactor.symbols import tau, xi

    sym = _poly_symbol(sp.expand(tau - sp.Float(0.3) * xi**2))
    obs, kmax = _heat_obs(), 3
    B, cg = RR._basis_groups([sym], obs["ts"], obs["xs"], obs["period"], kmax, True)
    ug = np.unique(cg)
    n, s = len(obs["ys"]), obs["sigma"]

    def dense(lts):
        d = np.exp(np.asarray(lts))[np.searchsorted(ug, cg)]
        return multivariate_normal(np.zeros(n), s**2 * (np.eye(n) + (B * d) @ B.T), allow_singular=True).logpdf(obs["ys"])

    best = -minimize(lambda v: -dense(v), np.zeros(len(ug)), method="Nelder-Mead",
                     options=dict(maxiter=4000, xatol=1e-6, fatol=1e-8)).fun
    monkeypatch.setattr(RR, "TAU2_POOL_EMPTY", False)  # T76 alone: one free scale per bin
    monkeypatch.setattr(RR, "TAU2_PER_BIN", False)
    shared = RR.log_evidence([sym], obs, kmax)
    monkeypatch.setattr(RR, "TAU2_PER_BIN", True)
    fast = RR.log_evidence([sym], obs, kmax)
    assert abs(fast - best) < 1e-3 and fast >= shared - 1e-9


def test_per_bin_grid_equals_dense_and_ignores_unexcited_bins(monkeypatch):
    """T76 on a grid: the block-diagonal path equals the dense one; and two laws that agree on the
    only excited bin (kappa = 1) and differ on bins without data (Ann(u) is the same, R4-T6) get the
    same evidence, which a shared prior scale does not give."""
    import sympy as sp

    import pdefactor.refine_raw as RR
    from pdefactor.loop import _poly_symbol
    from pdefactor.symbols import tau, xi

    rng = np.random.default_rng(2)
    t, x, sig = np.linspace(0, 2, 24), np.linspace(0, 2 * np.pi, 32, endpoint=False), 0.05
    TT, XX = np.meshgrid(t, x, indexing="ij")
    u = np.exp(-0.3 * TT) * np.cos(XX + 0.3)
    og = _grid_obs(u + sig * rng.standard_normal(u.shape), t, x, sig)
    dense = {k: v for k, v in og.items() if k != "grid"}
    heat = _poly_symbol(sp.expand(tau - sp.Float(0.3) * xi**2))
    other = _poly_symbol(sp.expand(tau - sp.Float(0.4) * xi**2 - sp.Float(0.1) * xi**4))  # same root at kappa = 1
    monkeypatch.setattr(RR, "TAU2_POOL_EMPTY", True)  # T77 (default): empty bins pooled
    monkeypatch.setattr(RR, "TAU2_PER_BIN", False)
    gap_pool = RR.log_evidence([other], og, 3) - RR.log_evidence([heat], og, 3)
    assert abs(RR.log_evidence([heat], og, 3) - RR.log_evidence([heat], dense, 3)) < 1e-2
    monkeypatch.setattr(RR, "TAU2_POOL_EMPTY", False)  # T76 alone: one free scale per bin
    monkeypatch.setattr(RR, "TAU2_PER_BIN", True)
    assert abs(RR.log_evidence([heat], og, 3) - RR.log_evidence([heat], dense, 3)) < 1e-2
    gap_pb = RR.log_evidence([other], og, 3) - RR.log_evidence([heat], og, 3)
    monkeypatch.setattr(RR, "TAU2_PER_BIN", False)
    gap_shared = RR.log_evidence([other], og, 3) - RR.log_evidence([heat], og, 3)
    # what is left is the per-bin scale fitting pure noise in the bins without data (well under one nat)
    assert abs(gap_pb) < 1.0 < abs(gap_shared)
    assert abs(gap_pool) < 1.0
