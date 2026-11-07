"""T94: the support path of the refinement stage over the xi-degree of the searched class (PATH_CLASS)."""
import numpy as np
import sympy as sp

from pdefactor import loop
from pdefactor.symbols import tau, xi


def _field(sig=1e-3, seed=0):
    """u_t = 0.1 u_xx - 0.002 u_xxxx ... as a symbol: tau - 0.1 xi^2 - 0.002 xi^4 (xi = i kappa), so
    lambda(kappa) = -0.1 kappa^2 + 0.002 kappa^4; modes at kappa = 1..5 on a periodic grid."""
    t = np.linspace(0, 2, 64)
    x = np.linspace(0, 2 * np.pi, 32, endpoint=False)
    u = np.zeros((len(t), len(x)))
    for k in range(1, 6):
        lam = -0.1 * k**2 + 0.002 * k**4
        u += (1.0 / k) * np.exp(lam * t)[:, None] * np.cos(k * x + 0.3 * k)[None, :]
    rng = np.random.default_rng(seed)
    return t, x, u + sig * rng.standard_normal(u.shape), sig


def _heat_report():
    q = tau - 0.1 * xi**2
    return loop.FactorReport(q, 1.0, {(1, 0): (1 + 0j,) * 3, (0, 2): (-0.1 + 0j,) * 3})


def _max_b(cands):
    return max(b for paths in cands.values() for path in paths for c in path for (_, b) in c)


def test_path_stays_within_the_factor_degree_when_off(monkeypatch):
    monkeypatch.setattr(loop, "PATH_CLASS", False)
    t, x, u, sig = _field()
    cands = loop.support_path([_heat_report()], u, t, x, sig, dx_class=4)
    assert _max_b(cands) <= 2


def test_path_reaches_the_class_degree_when_on(monkeypatch):
    """With the switch on, the backward-elimination path starts from every tau^a xi^b, b <= 4, so a
    support with the xi^4 term the factor lacks is a candidate; the evidence of refine then keeps it."""
    monkeypatch.setattr(loop, "PATH_CLASS", True)
    t, x, u, sig = _field()
    f = _heat_report()
    cands = loop.support_path([f], u, t, x, sig, dx_class=4)
    assert _max_b(cands) == 4
    assert any(set(c) == {(1, 0), (0, 2), (0, 4)} for path in cands[0] for c in path)
    obs = loop._grid_obs(u, t, x, sig)
    out = loop.refine_factors([f], obs, 7, candidates=cands)
    c = out["coefs"][0]
    assert (0, 4) in c and abs(c[(0, 4)].real + 0.002) < 2e-4
    assert sp.Poly(f.sympy, tau, xi).degree(xi) == 4


def test_without_dx_class_the_switch_changes_nothing(monkeypatch):
    monkeypatch.setattr(loop, "PATH_CLASS", True)
    t, x, u, sig = _field()
    assert _max_b(loop.support_path([_heat_report()], u, t, x, sig)) <= 2


def test_log_evidence_survives_a_non_converging_svd(monkeypatch):
    """A kernel whose basis LAPACK cannot decompose is scored like a non-finite one (the noise
    evidence), not a crash of the whole run."""
    from pdefactor import refine_raw
    from pdefactor.core.variety import PolySymbol

    rng = np.random.default_rng(0)
    n = 200
    ts, xs = rng.uniform(0, 2, n), rng.uniform(0, 2 * np.pi, n)
    obs = dict(ts=ts, xs=xs, ys=np.cos(xs) * np.exp(-0.1 * ts) + 0.01 * rng.standard_normal(n),
               period=2 * np.pi, sigma=0.01)
    heat = PolySymbol(1, [np.array([0, 0, -0.1], complex)])
    ok = refine_raw.log_evidence([heat], dict(obs), 4)
    empty = refine_raw.log_evidence([], dict(obs), 4)

    def bad(*a, **k):
        raise np.linalg.LinAlgError("SVD did not converge")

    monkeypatch.setattr(refine_raw.np.linalg, "svd", bad)
    v = refine_raw.log_evidence([heat], dict(obs), 4)
    assert np.isfinite(v) and abs(v - empty) < 1e-9 and v < ok
