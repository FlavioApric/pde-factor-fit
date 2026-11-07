"""T77+: bugs reported by the learned-layers corpus runs (HANDOFF §4.8), each reproduced and fixed
generally. One test per fix; each fails on the code before the fix."""
import numpy as np

from pdefactor.core.variety import PolySymbol


def _sym(m, coeffs):
    return PolySymbol(m, [np.array(c, complex) for c in coeffs])


def test_raw_evidence_with_more_columns_than_observations():
    """Real data, a basis wider than the data (2 * sum(m) * (2 kmax + 1) > n): the QR mask had n
    entries for p columns and raised IndexError (learned-layers corpus S). The evidence is finite and
    the kept basis spans at most n columns."""
    from pdefactor.bayes_split import raw_evidence

    rng = np.random.default_rng(0)
    n = 30
    ts, xs = rng.uniform(0, 2, n), rng.uniform(0, 2 * np.pi, n)
    ys = np.exp(-0.3 * ts) * np.cos(xs) + 1e-2 * rng.standard_normal(n)
    heat, wave = _sym(1, [[0, 0, -0.3]]), _sym(2, [[0, 0, -1.0], [0]])
    ev, rank = raw_evidence([heat, wave], ts, xs, ys, 2 * np.pi, 10, sigma=1e-2)
    assert np.isfinite(ev) and 0 < rank <= n


def test_raw_evidence_with_no_columns_is_finite():
    """No root in the band gives an empty basis: the evidence is that of pure noise, not a crash."""
    from pdefactor.bayes_split import raw_evidence

    rng = np.random.default_rng(1)
    ts, xs, ys = rng.uniform(0, 2, 20), rng.uniform(0, 2 * np.pi, 20), rng.standard_normal(20)
    ev, rank = raw_evidence([], ts, xs, ys, 2 * np.pi, 3, sigma=1.0)
    assert np.isfinite(ev) and rank == 0


def test_empty_bin_test_is_calibrated_and_finds_excited_bins():
    """T77 (T76 repair): the data-only chi^2 test marks no bin on pure noise (at most 2 of 20 seeds at
    family-wise level 0.01) and exactly the excited bins on a field with |n| in {1, 3} only."""
    from pdefactor.refine_raw import _excited_bins

    nt, nx, kmax, sig = 48, 64, 8, 0.1
    t = np.linspace(0, 2, nt)
    x = np.linspace(0, 2 * np.pi, nx, endpoint=False)
    hits = 0
    for sd in range(20):
        u = sig * np.random.default_rng(sd).standard_normal((nt, nx))
        hits += bool(_excited_bins(dict(Y=np.fft.fft(u, axis=1, norm="ortho"), nx=nx), kmax, True, sig))
    assert hits <= 2
    u = np.exp(-0.1 * t)[:, None] * (np.cos(x) + 0.5 * np.sin(3 * x))[None] \
        + sig * np.random.default_rng(99).standard_normal((nt, nx))
    assert _excited_bins(dict(Y=np.fft.fft(u, axis=1, norm="ortho"), nx=nx), kmax, True, sig) == {1, 3}


def test_scattered_empty_bin_test_is_calibrated_and_finds_excited_bins():
    """T77 scattered: the least-squares bin test marks no bin on pure noise (<= 2 of 20 seeds) and the
    excited bins {1, 3} of a slowly decaying field sampled at 400 random points."""
    from pdefactor.refine_raw import _excited_bins_raw

    n, kmax, sig = 400, 8, 0.05
    hits = 0
    for sd in range(20):
        rng = np.random.default_rng(sd)
        ts, xs = rng.uniform(0, 2, n), rng.uniform(0, 2 * np.pi, n)
        hits += bool(_excited_bins_raw(ts, xs, sig * rng.standard_normal(n), 2 * np.pi, kmax, True, sig))
    assert hits <= 2
    rng = np.random.default_rng(99)
    ts, xs = rng.uniform(0, 2, n), rng.uniform(0, 2 * np.pi, n)
    ys = np.exp(-0.1 * ts) * (np.cos(xs) + 0.5 * np.sin(3 * xs)) + sig * rng.standard_normal(n)
    assert _excited_bins_raw(ts, xs, ys, 2 * np.pi, kmax, True, sig) == {1, 3}


def test_pooled_evidence_equals_shared_when_every_bin_is_excited_or_empty():
    """T77: with every bin empty, the pooled evidence is the shared-scale evidence (one group); the
    switch is off by default so the default evidence is unchanged."""
    import pdefactor.refine_raw as RR

    rng = np.random.default_rng(3)
    n, sig = 200, 1.0
    ts, xs = rng.uniform(0, 2, n), rng.uniform(0, 2 * np.pi, n)
    obs = dict(ts=ts, xs=xs, ys=sig * rng.standard_normal(n), period=2 * np.pi, sigma=sig)
    heat = _sym(1, [[0, 0, -0.3]])
    old = RR.TAU2_POOL_EMPTY
    RR.TAU2_POOL_EMPTY = False
    e0 = RR.log_evidence([heat], obs, 4)
    try:
        RR.TAU2_POOL_EMPTY = True
        e1 = RR.log_evidence([heat], obs, 4)
    finally:
        RR.TAU2_POOL_EMPTY = old
    assert abs(e1 - e0) < 1e-3


def test_report_pools_only_fits_of_the_majority_tau_order():
    """T79: a group of fits holding one first-order and one lighter second-order fit is reported as the
    first-order factor (monic, leading coefficient 1), not as a median with a zero leading term that
    made refine_factors divide by zero (learned-layers corpus S, F4/F5 seed 209)."""
    from pdefactor.loop import _report

    d1 = {(1, 0): 1.0 + 0j, (0, 0): 0.5 + 0.2j}
    d2 = {(2, 0): 1.0 + 0j, (1, 0): 0.3 + 0j, (0, 2): -0.1 + 0j}
    r = _report([d1, d1, d2], [0.4, 0.4, 0.2], 1.0)
    assert max(a for a, _ in r.coef) == 1
    assert abs(r.coef[(1, 0)][0] - 1) < 1e-12 and abs(r.coef[(0, 0)][0] - (0.5 + 0.2j)) < 1e-12
    same = _report([d1, d1], [0.4, 0.4], 1.0)  # one order: unchanged path
    assert same.coef == _report([d1, d1], [0.4, 0.4], 1.0).coef


def test_branch_split_of_an_exactly_reducible_factor_has_the_same_product():
    """T80: tau^2 - 0.97 xi^2 splits by root branches into tau -+ sqrt(0.97) xi whose product is the
    unsplit symbol to rounding (_same_product), so the split is the same kernel and is kept without a
    refit; an irreducible wave-like symbol with a xi^4 term does not pass the same test."""
    import sympy as sp

    from pdefactor.loop import FactorReport, _same_product, split_branches
    from pdefactor.symbols import tau, xi

    def rep(expr):
        p = sp.Poly(sp.expand(expr), tau, xi)
        return FactorReport(sp.expand(expr), 1.0, {mo: (complex(c),) * 3 for mo, c in zip(p.monoms(), p.coeffs())})

    f = rep(tau**2 - sp.Float(0.97) * xi**2)
    props, src = split_branches([f], 6.0)
    assert len(props) == 2 and src == [0, 0] and _same_product(props, [f])
    g = rep(tau**2 - sp.Float(0.548) * xi**2 + sp.Float(0.00128) * xi**4)
    props, _ = split_branches([g], 6.0)
    assert len(props) == 1 or not _same_product(props, [g])


def test_vectorised_bin_profile_matches_or_beats_the_per_bin_loop():
    """The vectorised per-bin profiling minimises the same objective as the per-bin minimize_scalar
    loop: never higher than it (minimisation), and equal to within 1e-3 nats on random spectra."""
    from scipy.optimize import minimize_scalar

    from pdefactor.refine_raw import _profile_bins

    rng = np.random.default_rng(0)
    for trial in range(20):
        gid = rng.integers(0, 6, 40)
        lam = 10 ** rng.uniform(-3, 4, 40)
        proj = rng.chisquare(2, 40) * (1 + lam * 10 ** rng.uniform(-6, 0))
        real = bool(trial % 2)
        ref = 0.0
        for b in np.unique(gid):
            lb, pb = lam[gid == b], proj[gid == b]

            def nb(lt, lb=lb, pb=pb):
                t2 = np.exp(lt)
                v = np.sum(pb / (1 + t2 * lb)) + np.sum(np.log1p(t2 * lb))
                return 0.5 * v if real else v

            ref += minimize_scalar(nb, bounds=(np.log(1e-8 / lb.max()), np.log(1e8)), method="bounded",
                                   options={"xatol": 1e-3}).fun
        fast = _profile_bins(lam, proj, gid, real)
        assert fast <= ref + 1e-6 and ref - fast < 1e-3


def test_warm_started_bin_scales_reach_the_cold_optimum():
    """WARM_BINS: starting the scattered per-bin L-BFGS at the previous optimum (same groups, a nearby
    basis) reaches the same minimum as the cold start from the shared scale, to 1e-3 nats."""
    from pdefactor.refine_raw import _per_bin_neg

    rng = np.random.default_rng(5)
    r, p = 30, 40
    cg = rng.integers(0, 5, p)
    W0 = rng.standard_normal((r, p)) * 10 ** rng.uniform(-1, 1, p)
    c = rng.standard_normal(r) * 3
    warm = {}
    for step in range(6):
        W = W0 + 1e-4 * step * rng.standard_normal((r, p))
        cold = _per_bin_neg(c, W, cg, 1.0, True, 0.0)
        hot = _per_bin_neg(c, W, cg, 1.0, True, 0.0, warm)
        assert abs(hot - cold) < 1e-3
    assert len(warm) == 1


def test_grid_and_scattered_bin_tests_agree_on_the_same_points():
    """One rule on both paths: the grid test (projection of each DFT bin on Legendre(t)) and the
    scattered least-squares test pick the same excited bins on the same grid points, so pooling and
    hence the evidence do not depend on the representation."""
    from pdefactor.refine_raw import _excited_bins, _excited_bins_raw

    nt, nx, kmax, sig = 24, 32, 6, 0.05
    t = np.linspace(0, 2, nt)
    x = np.linspace(0, 2 * np.pi, nx, endpoint=False)
    TT, XX = np.meshgrid(t, x, indexing="ij")
    for sd, amp in enumerate((0.0, 0.02, 0.05, 1.0)):
        u = amp * (np.exp(-0.3 * TT) * np.cos(XX) + np.exp(-1.2 * TT) * np.sin(2 * XX + 0.4)) \
            + sig * np.random.default_rng(sd).standard_normal(u.shape if sd else TT.shape)
        g = dict(Y=np.fft.fft(u, axis=1, norm="ortho"), nx=nx, t=t)
        assert _excited_bins(g, kmax, True, sig) == _excited_bins_raw(TT.ravel(), XX.ravel(), u.ravel(),
                                                                      2 * np.pi, kmax, True, sig)


def test_per_bin_profile_triangular_form_equals_the_direct_formula():
    """T85: _per_bin_neg uses c^H K^-1 c = |L^-1 c|^2 and diag(W^H K^-1 W) = column norms of L^-1 W
    (one triangular solve) instead of explicit solves; the minimum equals the one computed with the
    direct formula to rounding."""
    from scipy.optimize import minimize

    from pdefactor.refine_raw import _per_bin_neg

    rng = np.random.default_rng(5)
    for real in (True, False):
        r, p = 30, 40
        W = rng.standard_normal((r, p)) + (0 if real else 1j * rng.standard_normal((r, p)))
        c = W @ rng.standard_normal(p) + rng.standard_normal(r)
        cg = rng.integers(0, 4, p)
        ug, inv = np.unique(cg, return_inverse=True)

        def direct(lts):
            K = np.eye(r) + (W * np.exp(lts)[inv]) @ W.conj().T
            v = float(np.vdot(c, np.linalg.solve(K, c)).real) + np.linalg.slogdet(K)[1] + 3.0
            return (0.5 if real else 1.0) * v

        ref = minimize(direct, np.zeros(len(ug)), method="Nelder-Mead",
                       options=dict(maxiter=6000, xatol=1e-8, fatol=1e-10)).fun
        assert abs(_per_bin_neg(c, W, cg, 3.0, real, 0.0) - ref) < 1e-4
