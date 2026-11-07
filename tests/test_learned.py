"""Phase 4 learned layers: off switches, the L0 seed hook in the core, calibration guarantees."""
import numpy as np
import pytest

from pdefactor.core import structfit
from pdefactor.core.structfit import extract_modes_ic
from pdefactor.learned import expsum
from pdefactor.learned.calibrate import (IntervalInflator, ProbabilityCalibrator, loss_threshold,
                                         reliability, split_indices)
from pdefactor.learned.remedy import RemedyTable
from pdefactor.learned.validator import Validator, factor_aggregates
from pdefactor.synthetic import case, grid


def _modes_equal(a, b):
    return (np.array_equal(a.kappa, b.kappa) and np.array_equal(a.lam, b.lam)
            and np.array_equal(a.amp, b.amp))


# ------------------------------------------------------------------ L0 hook in the core
@pytest.fixture
def heat_noisy():
    f = case("heat", seed=0)
    t, x, u = grid(f)
    rng = np.random.default_rng(1)
    return t, x, u + 1e-2 * np.std(u) * rng.standard_normal(u.shape)


def test_seed_off_is_identical(heat_noisy):
    t, x, u = heat_noisy
    ref = extract_modes_ic(u, t, x, noise=1e-2 * np.std(u), refine=True)[0]
    off = extract_modes_ic(u, t, x, noise=1e-2 * np.std(u), refine=True, seeds=False)[0]
    assert _modes_equal(ref, off)  # an empty provider is "on": it adds the equal-budget second starts


def test_seed_module_switch(heat_noisy, monkeypatch):
    t, x, u = heat_noisy
    calls = []
    monkeypatch.setattr(structfit, "SEED_PROVIDER", lambda y, dt, s: calls.append(1) or [])
    extract_modes_ic(u, t, x, noise=1e-2 * np.std(u))
    assert calls  # the module default is used when seeds=None
    calls.clear()
    extract_modes_ic(u, t, x, noise=1e-2 * np.std(u), seeds=False)
    assert not calls


def _bic(y, tt, lam, nobs, sk):
    rss, _ = structfit._bin_rss(y, tt, lam, 1.0 / sk)
    return rss + 4 * len(lam) * np.log(nobs)


def test_seed_can_only_lower_bic_per_bin(heat_noisy):
    """A seed set joins the comparison as one more candidate: the selected per-bin BIC can only go
    down, whatever the seeds are (junk included)."""
    t, x, u = heat_noisy
    rng = np.random.default_rng(3)
    junk = lambda y, dt, s: [rng.normal(-3, 3, 3) + 1j * rng.normal(0, 3, 3) for _ in range(3)]
    nz = 1e-2 * np.std(u)
    m0, bn, _, U = extract_modes_ic(u, t, x, noise=nz, refine=True, seeds=False)
    m1, _, _, _ = extract_modes_ic(u, t, x, noise=nz, refine=True, seeds=junk)
    tt = t - t[0]
    for k in np.unique(m0.kidx):
        y = U[:, k]
        b0 = _bic(y, tt, m0.lam[m0.kidx == k], 2 * len(t), bn.sigma[k])
        if (m1.kidx == k).any():
            b1 = _bic(y, tt, m1.lam[m1.kidx == k], 2 * len(t), bn.sigma[k])
            assert b1 <= b0 + 1e-6 * abs(b0)


GOLDEN = ["heat", "transport_plus_diffusion", "wave", "schrodinger", "beam"]


def test_seed_off_matches_origin_main_golden():
    """Off is bit-for-bit the pre-Phase-4 core: modes recorded from origin/main's extract_modes_ic
    (tests/data/structfit_golden.npz, generated with the same data recipe) are reproduced exactly."""
    import os

    ref = np.load(os.path.join(os.path.dirname(__file__), "data", "structfit_golden.npz"))
    for i, name in enumerate(GOLDEN):
        t, x, u = grid(case(name))
        rng = np.random.default_rng(i)
        for nz in (1e-3, 5e-2):
            un = u + nz * np.std(u) * rng.standard_normal(u.shape)
            for refine in (False, True):
                with np.errstate(all="ignore"):
                    md = extract_modes_ic(un, t, x, noise=nz * np.std(u), refine=refine)[0]
                key = f"{name}_{nz}_{int(refine)}"
                # same modes (orders, kappa) exactly; values to 1e-5 relative: the golden file comes
                # from another platform (BLAS/LAPACK), where VarPro ends 1e-6 apart
                assert np.array_equal(md.kappa, ref[key + "_kappa"]), key
                assert np.allclose(md.lam, ref[key + "_lam"], rtol=1e-5, atol=1e-8), key
                assert np.allclose(md.amp, ref[key + "_amp"], rtol=1e-5, atol=1e-8 * np.abs(md.amp).max()), key


def _pair(nz=1e-3):
    rng = np.random.default_rng(0)
    t = np.linspace(0, 2, 64)
    lam = np.array([-1.0, -1.3 + 0.0j])
    x = np.linspace(0, 2 * np.pi, 8, endpoint=False)
    clean = np.exp(np.outer(t, lam)) @ np.array([1.0, -0.9])
    u = np.outer(clean, np.ones(8)).real + nz * rng.standard_normal((64, 8))
    return t, x, u, lam


def test_seed_never_adds_an_order_outside_the_pencil_range():
    """Honesty rule: with extra=0 the pencil range is its rank order only (1 for this merged pair);
    a seed of order 2 is ignored, so the order IC keeps its search space."""
    t, x, u, lam = _pair()
    kw = dict(noise=1e-3, refine=True, extra=0, snr_min=40.0)
    m_on = extract_modes_ic(u, t, x, seeds=lambda y, dt, s: [lam], **kw)[0]
    assert (m_on.kappa == 0).sum() == 1


def test_seed_inside_the_range_is_scored():
    """Inside r0..r0+extra a seed is one more start, scored by the same BIC: the true pair as a
    seed is selected when the data support two poles (CRB-limited at this SNR: tolerance 0.1)."""
    t, x, u, lam = _pair()
    kw = dict(noise=1e-3, refine=True, extra=1, snr_min=40.0)
    m_on = extract_modes_ic(u, t, x, seeds=lambda y, dt, s: [lam], **kw)[0]
    got = np.sort_complex(m_on.lam[m_on.kappa == 0])
    assert len(got) == 2 and np.allclose(got, np.sort_complex(lam), atol=0.1)


def test_equal_starts_per_order(monkeypatch):
    """With a provider on, every order in the range gets two starts: a seed or a second pencil."""
    calls = []
    orig = structfit.matrix_pencil

    def spy(y, dt, order=None, pencil=None, **kw):
        calls.append((order, pencil))
        return orig(y, dt, order=order, pencil=pencil, **kw)

    monkeypatch.setattr(structfit, "matrix_pencil", spy)
    t, x, u, lam = _pair()
    extract_modes_ic(u, t, x, noise=1e-3, extra=2, snr_min=40.0, seeds=lambda y, dt, s: [lam[:1]])
    second = [o for o, p in calls if p is not None]
    assert 1 not in second and len(second) == 2  # order 1 seeded; orders 2 and 3 get a second pencil


def test_null_gate_junk_seeds_on_single_pole():
    """One clean pole per bin, junk seeds of every order: no extra mode survives the BIC."""
    rng = np.random.default_rng(4)
    t = np.linspace(0, 2, 64)
    x = np.linspace(0, 2 * np.pi, 16, endpoint=False)
    u = np.outer(np.exp(-0.7 * t), np.ones(16)) + 1e-3 * rng.standard_normal((64, 16))
    junk = lambda y, dt, s: [rng.normal(-3, 2, r) + 1j * rng.normal(0, 3, r) for r in range(1, 9)]
    m = extract_modes_ic(u, t, x, noise=1e-3, refine=True, seeds=junk)[0]
    assert len(m) == 1 and abs(m.lam[0] + 0.7) < 0.01


def test_null_gate_pure_noise():
    """Pure noise: no bin passes the SNR gate, so no mode appears (the seed is never asked; the
    single-pole test above is the null that exercises the provider)."""
    rng = np.random.default_rng(2)
    t = np.linspace(0, 2, 64)
    x = np.linspace(0, 2 * np.pi, 32, endpoint=False)
    u = 1e-3 * rng.standard_normal((64, 32))
    many = lambda y, dt, s: [np.linspace(-5, -1, 8) + 1j * np.linspace(-3, 3, 8)]
    m = extract_modes_ic(u, t, x, noise=1e-3, refine=True, seeds=many)[0]
    assert len(m) == 0


# ------------------------------------------------------------------ L0 training distribution
def test_expsum_draw_and_encode():
    rng = np.random.default_rng(0)
    for _ in range(50):
        d = expsum.draw(rng)
        assert d.y.shape == (d.nt,) and 32 <= d.nt <= expsum.NT
        assert np.all(d.s.real >= expsum.RE_S[0]) and np.all(np.abs(d.s.imag) <= expsum.IM_S[1])
        x, snr = expsum.encode(d.y, d.sigma)
        assert x.shape == (3, expsum.NT) and x[2].sum() == d.nt and np.isfinite(snr)
    d = expsum.draw(rng, r=0)
    assert len(expsum.detectable(d)[0]) == 0
    d = expsum.draw(rng, r=1, snr_db=80)
    assert len(expsum.detectable(d)[0]) == 1


# ------------------------------------------------------------------ L2 calibration
def test_loss_threshold():
    assert loss_threshold(1, 1) == 0.5 and abs(loss_threshold(9, 1) - 0.9) < 1e-12


def test_split_lofo_groups_disjoint():
    g = np.repeat(np.arange(5), 20)
    a, b, c = split_indices(len(g), groups=g, rng=0)
    sets = [set(g[i]) for i in (a, b, c)]
    assert not (sets[0] & sets[1]) and not (sets[0] & sets[2]) and not (sets[1] & sets[2])
    assert len(a) + len(b) + len(c) == len(g)


def test_isotonic_improves_reliability():
    rng = np.random.default_rng(0)
    p_true = rng.uniform(0, 1, 6000)
    y = rng.uniform(size=6000) < p_true
    p_over = p_true**0.3  # overconfident reported probability
    cal = ProbabilityCalibrator().fit(p_over[:3000], y[:3000])
    e_raw = reliability(p_over[3000:], y[3000:])[1]
    e_cal = reliability(cal(p_over[3000:]), y[3000:])[1]
    assert e_cal < 0.5 * e_raw
    assert np.all(np.diff(cal(np.linspace(0, 1, 50))) >= 0)  # monotone: never reorders runs
    assert np.array_equal(ProbabilityCalibrator()(p_over), p_over)  # off


def _interval_data(rng, n):
    feats = {k: rng.uniform(0, 1, n) for k in ("split_amp", "mode_margin", "kappa_vand", "log_snr",
                                                "disagreement")}
    true_scale = 1 + 3 * feats["split_amp"]  # undercoverage grows with the split amplification
    z = np.abs(rng.standard_normal(n)) * true_scale / 1.645  # nominal 90 % half width = 1
    return feats, z


def test_interval_inflator_coverage_and_monotone():
    rng = np.random.default_rng(0)
    f_fit, z_fit = _interval_data(rng, 3000)
    f_cal, z_cal = _interval_data(rng, 1500)
    f_te, z_te = _interval_data(rng, 4000)
    inf = IntervalInflator(regime_edges=(0.33, 0.66))
    assert np.all(inf(f_te) == 1)  # off before calibration
    inf.fit(f_fit, z_fit).calibrate(f_cal, z_cal)
    raw = np.mean(z_te <= 1)
    cov = np.mean(z_te <= inf(f_te))
    assert raw < 0.8 and abs(cov - 0.90) < 0.03
    grid_ = {k: np.full(20, 0.5) for k in f_te}
    grid_["split_amp"] = np.linspace(0, 1, 20)
    assert np.all(np.diff(inf.base(grid_)) >= -1e-12)


# ------------------------------------------------------------------ V1
def _validator_data(rng, n, shift=0.0):
    X = rng.standard_normal((n, 6)) + shift
    Y = np.column_stack([(X[:, j] + 0.3 * rng.standard_normal(n)) > 1.0 for j in range(3)]).astype(int)
    return X, Y


def test_validator_risk_control_and_ood():
    rng = np.random.default_rng(0)
    modes = ("a", "b", "c")
    v = Validator(modes=modes, alpha=0.1)
    assert v.predict(np.zeros((1, 6))) is None  # off
    Xf, Yf = _validator_data(rng, 3000)
    Xc, Yc = _validator_data(rng, 1500)
    Xt, Yt = _validator_data(rng, 3000)
    v.fit(Xf, Yf).calibrate(Xc, Yc)
    out = v.predict(Xt)
    miss = []
    for o, y in zip(out, Yt):
        if o["ood"] or y.sum() == 0:
            continue
        miss.append(sum(1 for j, m in enumerate(modes) if y[j] and m not in o["set"]) / y.sum())
    fnr = np.sum(miss) / len(Yt)
    assert fnr <= 0.1 + 0.02
    ood_in = np.mean([o["ood"] for o in out])
    ood_out = np.mean([o["ood"] for o in v.predict(_validator_data(rng, 500, shift=6.0)[0])])
    assert ood_in < 0.03 and ood_out > 0.9
    assert all(o["proba"] is None for o in v.predict(Xt[:1] + 50))


def test_factor_aggregates_permutation_invariant():
    fs = [{"coef_z": np.array([3.0, 9.0]), "support": 5, "incl": 0.9},
          {"coef_z": np.array([1.5]), "support": 2, "incl": 0.4, "margin": -1}]
    a, b = factor_aggregates(fs), factor_aggregates(fs[::-1])
    assert a.keys() == b.keys()
    assert all((np.isnan(a[k]) and np.isnan(b[k])) or a[k] == b[k] for k in a)
    assert a["coef_z_min"] == 1.5 and a["n_factors"] == 2


# ------------------------------------------------------------------ C remedy order
def test_remedy_order():
    tab = RemedyTable(default={"high_kappa_loss": ["L1a_search", "L0_seeds", "L1a_prior"]})
    assert tab.order("high_kappa_loss") == ["L1a_search", "L0_seeds", "L1a_prior"]  # off
    tab.fit([("high_kappa_loss", "L0_seeds", True)] * 80 + [("high_kappa_loss", "L0_seeds", False)] * 20
            + [("high_kappa_loss", "L1a_search", True)] * 2)
    # 2/2 has a lower credible bound than 80/100: the well-measured remedy goes first
    assert tab.order("high_kappa_loss") == ["L0_seeds", "L1a_search", "L1a_prior"]


# ------------------------------------------------------------------ feature adapters
def test_run_features_from_loop_result():
    from pdefactor.aggregate import fake_posterior
    from pdefactor.learned.features import run_features
    from pdefactor.loop import run_loop

    t, x, u = grid(case("heat"))
    sig = 1e-3 * np.std(u)
    s, pis = fake_posterior(u, sig, 3, rng=1)
    r = run_loop(s, t, x, sig, pis)
    row = run_features(r)
    assert 0 < row["p_top"] <= 1 and row["n_factors"] == 1
    assert row["support_min"] >= 3 and row["margin_min"] >= 0  # heat: many kappa, dx = 2
    assert all(isinstance(v, float) for v in row.values())
    assert not any(k in row for k in ("case", "seed", "name"))


def test_split_three_groups_nonempty_and_too_few_raises():
    g = np.repeat(np.arange(3), 10)
    for seed in range(5):
        assert all(len(i) for i in split_indices(len(g), groups=g, rng=seed))
    with pytest.raises(ValueError):
        split_indices(20, groups=np.repeat([0, 1], 10))


def test_validator_tolerates_dead_columns():
    rng = np.random.default_rng(1)
    X, Y = _validator_data(rng, 800)
    X = np.column_stack([X, np.full(len(X), np.nan), np.ones(len(X))])  # all-NaN and constant
    v = Validator(modes=("a", "b", "c")).fit(X, Y).calibrate(X, Y)
    out = v.predict(X[:5])
    assert out is not None and all(np.isfinite(o["p_ood"]) for o in out)


def test_remedy_per_cost_without_cost_is_not_favoured():
    tab = RemedyTable(default={"d": ["a", "b"]})
    tab.fit([("d", "a", True, 10.0)] * 50 + [("d", "b", True)] * 50)  # b: no recorded cost
    assert tab.order("d", per_cost=True)[0] in ("a", "b")  # finite, no division by ~0
    tab2 = RemedyTable(default={"d": ["a", "b"]}).fit([("d", "a", True, 10.0)] * 50 + [("d", "b", True, 1.0)] * 50)
    assert tab2.order("d", per_cost=True) == ["b", "a"]
