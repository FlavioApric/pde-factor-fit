"""T97: the refinement-stage fit guard (FIT_GUARD) and the plug-in fit on the excited bins."""
import numpy as np
import sympy as sp

from pdefactor import loop, refine_raw
from pdefactor.symbols import tau, xi


def _report(q):
    p = sp.Poly(sp.expand(q), tau, xi)
    return loop.FactorReport(sp.expand(q), 1.0, {mo: (complex(c),) * 3 for mo, c in zip(p.monoms(), p.coeffs())})


def _f22():
    from pdefactor.simulator import random_pde
    from pdefactor.synthetic import grid

    d = random_pde("F2", 2)
    t, x, u = grid(d.field)
    sig = 0.01 * np.std(u)
    un = u + sig * np.random.default_rng(1002).standard_normal(u.shape)
    return d, t, x, un, sig


# refined coefficients of the two models (refine_raw.refine on the observations, T97 diagnosis)
TRUTH = [tau + 0.43934945479143983 * xi + 0.03381988359611076j * xi**2,
         tau + 0.43934945479143983 * xi - 0.03381988359611076j * xi**2]
ALT = [tau + 0.3860138848565232 * xi + 0.0037418108685463047 * xi**3,
       tau + 0.343605790986997 * xi + 0.0028733053211530838 * xi**3]


def test_grid_and_scattered_fit_agree():
    """The grid shortcut of fit_excited (block-diagonal Gram) equals the dense least squares on the
    same points with the same excited bins."""
    t = np.linspace(0, 2, 32)
    x = np.linspace(0, 2 * np.pi, 16, endpoint=False)
    u = sum(np.exp(-0.1 * k**2 * t)[:, None] * np.cos(k * x + k)[None] / k for k in (1, 2, 3))
    sig = 1e-2
    u = u + sig * np.random.default_rng(0).standard_normal(u.shape)
    obs = loop._grid_obs(u, t, x, sig)
    syms = [loop._poly_symbol(tau - 0.1 * xi**2)]
    g = refine_raw.fit_excited(syms, obs, 5)
    dense = {k: v for k, v in obs.items() if k != "grid"}
    s = refine_raw.fit_excited(syms, dense, 5)
    assert g[1] == s[1] == 6  # bins 1-3 excited, Re/Im of one root each
    assert abs(g[0] - s[0]) < 1e-6 * max(abs(s[0]), 1.0)
    assert abs(2 * g[0] - u.size) < 4 * np.sqrt(2 * u.size)  # chi^2 of white noise


def test_guard_refuses_a_change_the_fit_does_not_support(monkeypatch):
    """F2-2 (a one-way dispersive wave: only the branch lambda_1(kappa), kappa > 0, is excited): the
    refined kernel evidence - Occam prefers two near-collinear real factors with xi^3 terms over the true
    conjugate pair (the truth's unexcited branch costs prior volume in every excited bin), while the
    plug-in fit prefers the truth with fewer parameters. The guard refuses truth -> alternative and
    allows alternative -> truth; off, it allows everything."""
    d, t, x, u, sig = _f22()
    obs = loop._grid_obs(u, t, x, sig)
    kmax, occ = 10, 0.5 * np.log(u.size)
    tr, al = [_report(q) for q in TRUTH], [_report(q) for q in ALT]
    ev_t = refine_raw.log_evidence([loop._poly_symbol(TRUTH[0])], obs, kmax) - occ * 2
    ev_a = refine_raw.log_evidence([loop._poly_symbol(q) for q in ALT], obs, kmax) - occ * 4
    assert ev_a > ev_t + 10  # the disagreement being guarded against
    assert loop._fit_score(tr, obs, kmax, occ) > loop._fit_score(al, obs, kmax, occ) + 5
    monkeypatch.setattr(loop, "FIT_GUARD", "0")
    assert loop._fit_guard(al, tr, obs, kmax, occ)
    monkeypatch.setattr(loop, "FIT_GUARD", "1")
    log = []
    assert not loop._fit_guard(al, tr, obs, kmax, occ, log) and len(log) == 1
    assert loop._fit_guard(tr, al, obs, kmax, occ)


def _profile_bins_add_at(lam, proj, gid, real, n_grid=256, n_gold=60):
    """_profile_bins as it was before T97 (np.add.at group sums), the reference for bit-identity."""
    ug, inv = np.unique(gid, return_inverse=True)
    G = len(ug)
    lmax = np.zeros(G)
    np.maximum.at(lmax, inv, lam)
    lo, hi = np.log(1e-8 / np.maximum(lmax, 1e-300)), np.full(G, np.log(1e8))
    f_ = 0.5 if real else 1.0

    def val(lt):
        t2 = np.exp(lt[inv])
        v = proj[:, None] / (1 + t2 * lam[:, None]) + np.log1p(t2 * lam[:, None])
        out = np.zeros(lt.shape)
        np.add.at(out, inv, v)
        return f_ * out

    u = np.linspace(0.0, 1.0, n_grid)
    L = lo[:, None] + (hi - lo)[:, None] * u[None]
    V = val(L)
    j = np.argmin(V, axis=1)
    step = (hi - lo) / (n_grid - 1)
    a = np.maximum(L[np.arange(G), j] - step, lo)
    b = np.minimum(L[np.arange(G), j] + step, hi)
    gr = (np.sqrt(5) - 1) / 2
    c, d = b - gr * (b - a), a + gr * (b - a)
    fc, fd = val(c[:, None])[:, 0], val(d[:, None])[:, 0]
    for _ in range(n_gold):
        left = fc < fd
        b = np.where(left, d, b)
        a = np.where(left, a, c)
        c, d = b - gr * (b - a), a + gr * (b - a)
        fc, fd = val(c[:, None])[:, 0], val(d[:, None])[:, 0]
    best = np.minimum(np.minimum(fc, fd), V[np.arange(G), j])
    return float(best.sum())


def test_profile_bins_bit_identical():
    rng = np.random.default_rng(3)
    for real in (True, False):
        for n, groups in ((40, 5), (300, 23), (7, 1)):
            lam = rng.exponential(1e3, n) * rng.choice([1e-6, 1.0, 1e3], n)
            proj = rng.exponential(1.0, n) * rng.choice([1.0, 1e4], n)
            gid = rng.integers(-3, groups, n)
            gid[gid < 0] = -(10**9)
            assert refine_raw._profile_bins(lam, proj, gid, real) == _profile_bins_add_at(lam, proj, gid, real)


def test_basis_groups_bit_identical():
    """The vectorised kernel basis (T97) equals the column-by-column reference bit for bit: orders 1-3,
    real and complex coefficients, a zero constant term (np.roots' trailing-zero path at kappa = 0),
    clipped growing modes, real and complex fields."""
    from pdefactor.core.variety import PolySymbol

    rng = np.random.default_rng(5)
    ts, xs = rng.uniform(0, 2, 150), rng.uniform(0, 2 * np.pi, 150)
    syms = [PolySymbol(1, [np.array([0, 1.3, -0.1], complex)]),
            PolySymbol(1, [np.array([0.2, 0.44, 0.0338j], complex)]),
            PolySymbol(2, [np.array([0.0, 0, 0.19, 0, 1e-3], complex), np.array([0, 0.87], complex)]),
            PolySymbol(2, [np.array([0.66, 0.1], complex), np.array([1.58, 0, -0.3], complex)]),
            PolySymbol(3, [np.array([0.5], complex), np.array([0.3, 0, 2.0], complex), np.array([0.8, 0.1j], complex)]),
            PolySymbol(1, [np.array([0, 0, -40.0], complex)])]  # e^{+40 kappa^2 t}: clipped at 50
    for k in range(1, len(syms) + 1):
        for real in (True, False):
            for kmax in (0, 3, 9):
                B1, g1 = refine_raw._basis_groups(syms[:k], ts, xs, 2 * np.pi, kmax, real)
                B0, g0 = refine_raw._basis_groups_ref(syms[:k], ts, xs, 2 * np.pi, kmax, real)
                assert B1.shape == B0.shape and B1.dtype == B0.dtype
                assert np.array_equal(B1, B0) and np.array_equal(g1, g0)
                assert np.array_equal(np.signbit(B1.real), np.signbit(B0.real))
