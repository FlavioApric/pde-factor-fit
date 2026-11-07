"""Phase 3 additions: per-bin correlated noise (GLS) in the core, the Friedrichs-angle split layer,
the data-level structure decider and the grouping of factor tracks."""
import numpy as np
import sympy as sp

from pdefactor.bayes_split import bayes_split
from pdefactor.core.structfit import BinNoise, analyze_structured
from pdefactor.core.variety import PolySymbol
from pdefactor.loop import FactorReport, _distinct, decide_structure
from pdefactor.synthetic import case, grid

T_, X_ = np.linspace(0, 2, 64), np.linspace(0, 2 * np.pi, 128, endpoint=False)


def _sym(m, coeffs):
    return PolySymbol(m, [np.array(c, complex) for c in coeffs])


def test_binnoise_recovers_ar1_autocovariance():
    """from_draws: the per-bin autocovariance of white-in-x, AR(1)-in-t noise has lag-1 ratio rho."""
    rho, R, nt, nx = 0.8, 64, 64, 32
    rng = np.random.default_rng(0)
    e = np.zeros((R, nt, nx))
    e[:, 0] = rng.standard_normal((R, nx))
    for i in range(1, nt):
        e[:, i] = rho * e[:, i - 1] + np.sqrt(1 - rho**2) * rng.standard_normal((R, nx))
    bn = BinNoise.from_draws(e, np.linspace(0, 2 * np.pi, nx, endpoint=False))
    r1 = (bn.acov[:, 1] / bn.acov[:, 0]).real
    assert abs(np.median(r1) - rho) < 0.05
    assert abs(np.median(bn.sigma) - 1 / np.sqrt(nx)) < 0.05 / np.sqrt(nx)


def test_gls_with_white_draws_matches_white_core():
    """Noise draws that are white give the same factor as the white-noise core."""
    t, x, u = grid(case("heat"))
    sig = 1e-3 * np.std(u)
    rng = np.random.default_rng(1)
    un = u + sig * rng.standard_normal(u.shape)
    draws = sig * rng.standard_normal((32,) + u.shape)
    a = analyze_structured(un, t, x, noise=sig, real=True)
    b = analyze_structured(un, t, x, noise=0.0, noise_draws=draws, real=True)
    assert a.label == b.label == "FIT-COMPATIBLE" and len(a.factors) == len(b.factors) == 1
    ca, cb = (np.r_[f.symbol.coeffs[0], 0, 0][:3] for f in (a.factors[0], b.factors[0]))
    assert np.max(np.abs(ca - cb)) < 1e-3


def test_bayes_split_weights_cover_truth_and_null():
    """True factors of transport + diffusion: the 90 % weight interval covers the true weight; heat
    with a spurious second factor: P(split) ~ 0."""
    f = case("transport_plus_diffusion")
    t, x, u0 = grid(f, nt=48, nx=64)
    TT, XX = np.meshgrid(t, x, indexing="ij")
    wt = f.weights(TT, XX)
    facs = [_sym(1, [[0, 1.0]]), _sym(1, [[0, 0, -0.3]])]  # tau + xi, tau - 0.3 xi^2
    sig = 1e-2 * np.std(u0)
    hits = 0  # measured: 0.90 over 30 seeds at nominal 0.90
    for sd in range(20):
        u = u0 + sig * np.random.default_rng(sd).standard_normal(u0.shape)
        r = bayes_split(u, t, x, facs, noise=sig, seed=sd, snr_min=0.5)
        assert r.p_split > 0.99
        hits += np.all((r.weights_q[:, 0] <= wt) & (wt <= r.weights_q[:, 2]))
    assert hits >= 15
    th, xh, uh = grid(case("heat"), nt=48, nx=64)
    uh = uh + sig * np.random.default_rng(9).standard_normal(uh.shape)
    rn = bayes_split(uh, th, xh, [facs[1], facs[0]], noise=sig)
    assert rn.p_split < 0.01 and rn.p_include[0] > 0.99


def test_decider_rejects_constant_factors_per_kappa():
    """Modes at |kappa| = 1, 2 only: (tau + 0.3)(tau + 1.2) fits the modes as well as tau - 0.3 xi^2 with
    fewer parameters (the mode-level BIC prefers it), but its kernels predict unused modes in every
    bin; the data-level evidence picks the single diffusion factor."""
    TT, XX = np.meshgrid(T_, X_, indexing="ij")
    u0 = np.exp(-0.3 * TT) * np.cos(XX) + 0.5 * np.exp(-1.2 * TT) * np.cos(2 * XX + 0.4)
    sig = 1e-2 * np.std(u0)
    u = u0 + sig * np.random.default_rng(0).standard_normal(u0.shape)
    best, ev = decide_structure(u, T_, X_, sig, {((1, 0), (1, 0)): 0.6, ((1, 2),): 0.4}, (3, 4))
    assert best == ((1, 2),)
    assert ev[((1, 2),)] - ev[((1, 0), (1, 0))] > 5  # gap 9.4 with the outlier-bin mixture (caps per-bin loss)


def test_distinct_uses_interval_overlap():
    z = (0j, 0j, 0j)
    a = FactorReport(sp.Integer(0), 0.5, {(1, 0): (1 + 0j,) * 3, (0, 1): (1.0 + 0j, 0.99 + 0j, 1.01 + 0j)})
    b = FactorReport(sp.Integer(0), 0.5, {(1, 0): (1 + 0j,) * 3, (0, 1): (1.005 + 0j, 0.995 + 0j, 1.02 + 0j)})
    c = FactorReport(sp.Integer(0), 0.5, {(1, 0): (1 + 0j,) * 3, (0, 2): (-0.3 + 0j, -0.31 + 0j, -0.29 + 0j)})
    assert not _distinct(a, b)
    assert _distinct(a, c)
    assert z == (0j, 0j, 0j)


def test_conj_pair_and_duplicate_merge():
    """_conj_pair recognises tau -+ 0.3 i xi^2 as conjugates; _duplicate_pair merges two copies of one
    first-order law (modes of tau + xi split between them) and keeps two different laws apart."""
    from types import SimpleNamespace

    from pdefactor.loop import _conj_pair, _duplicate_pair

    def rep(c):
        return FactorReport(sp.Integer(0), 0.5, {(1, 0): (1 + 0j,) * 3, (0, 2): (c, c, c)})

    assert _conj_pair(rep(-0.3j), rep(0.3j)) and not _conj_pair(rep(-0.3j), rep(-0.3j))
    rng = np.random.default_rng(0)
    k = np.arange(1.0, 9.0)
    sig = np.full(len(k), 1e-3)
    lam = -1j * k + sig * rng.standard_normal(len(k))
    modes = SimpleNamespace(lam=lam, kappa=k)
    a = _sym(1, [[0.0005, 1.0002]])  # the same law fitted on two halves of the modes
    b = _sym(1, [[-0.0005, 0.9998]])
    from pdefactor.core.structfit import _dist

    D = np.stack([_dist(Q, lam, k) for Q in (a, b)], axis=1) / sig[:, None]
    D[: len(k) // 2, 1] += 50  # first half nearest to a, second half to b
    D[len(k) // 2:, 0] += 50
    assert _duplicate_pair(modes, sig, [a, b], D, [0, 1], 3.0, [0.6, 0.4], real=True) == 1
    c = _sym(1, [[0, 0, -0.3]])  # heat: a different law
    lam2 = np.r_[lam[:4], -0.3 * k[4:] ** 2]
    D2 = np.stack([_dist(Q, lam2, k) for Q in (a, c)], axis=1) / sig[:, None]
    assert _duplicate_pair(SimpleNamespace(lam=lam2, kappa=k), sig, [a, c], D2, [0, 1], 3.0, [0.6, 0.4],
                           real=True) is None


def test_decider_rejects_symbol_that_interpolates_few_modes():
    """Schroedinger with 5 observed kappa: a (1, 4) symbol has as many complex coefficients as modes,
    interpolates them and wins the plug-in evidence on their noise; the identifiability count
    (R4-T4, one residual degree of freedom) makes it inadmissible."""
    TT, XX = np.meshgrid(T_, X_, indexing="ij")
    u0 = sum(np.exp(-1j * 0.3 * k**2 * TT + 1j * k * XX) / k for k in range(1, 6))
    sig = 1e-2 * np.std(np.abs(u0))
    rng = np.random.default_rng(3)
    u = u0 + sig * (rng.standard_normal(u0.shape) + 1j * rng.standard_normal(u0.shape))
    best, ev = decide_structure(u, T_, X_, sig, {((1, 2),): 0.6, ((1, 4),): 0.4}, (3, 4))
    assert best == ((1, 2),)


def test_decider_counts_only_observed_branches():
    """Schroedinger with 4 observed kappa, one branch each: a (2, 1) factor has 4 complex coefficients
    but sees only 4 roots (its second branch is never observed), so it interpolates and is
    inadmissible; the (1, 2) law (3 coefficients) is kept."""
    TT, XX = np.meshgrid(T_, X_, indexing="ij")
    u0 = sum(np.exp(-1j * 0.3 * k**2 * TT + 1j * k * XX) / k for k in range(1, 5))
    sig = 1e-3 * np.std(np.abs(u0))
    rng = np.random.default_rng(1)
    u = u0 + sig * (rng.standard_normal(u0.shape) + 1j * rng.standard_normal(u0.shape))
    best, ev = decide_structure(u, T_, X_, sig, {((2, 1),): 0.6, ((1, 2),): 0.4}, (3, 4))
    assert best == ((1, 2),)


def test_raw_evidence_rejects_interpolation_artifact():
    """Raw scattered heat data: the evidence of {heat} beats {heat, tau + 4} (a GP-mean artifact) and a
    degree-4 symbol that bends at high kappa."""
    from pdefactor.bayes_split import raw_evidence

    rng = np.random.default_rng(0)
    n = 400
    ts, xs = rng.uniform(0, 2, n), rng.uniform(0, 2 * np.pi, n)
    y0 = sum(np.exp(-0.3 * k**2 * ts) * np.cos(k * xs + k) / k for k in range(1, 5))
    ys = y0 + 1e-2 * np.std(y0) * rng.standard_normal(n)
    heat = _sym(1, [[0, 0, -0.3]])
    e_h = raw_evidence([heat], ts, xs, ys, 2 * np.pi, 6)[0]
    assert e_h > raw_evidence([heat, _sym(1, [[4.0]])], ts, xs, ys, 2 * np.pi, 6)[0] + 5
    assert e_h > raw_evidence([_sym(1, [[0, 0, -0.27, 0, -0.002]])], ts, xs, ys, 2 * np.pi, 6)[0] + 5

def test_bootstrap_intervals_cover_heat_coefficient():
    """Noisy heat grids: the parametric-bootstrap interval of the xi^2 coefficient has width and
    contains -0.3 on most seeds (single-sample quantiles are degenerate, width 0)."""
    from pdefactor.loop import run_loop

    t, x, u0 = grid(case("heat"), nt=48, nx=64)
    sig = 1e-2 * np.std(u0)
    hits = 0
    for sd in range(5):
        u = u0 + sig * np.random.default_rng(sd).standard_normal(u0.shape)
        r = run_loop([u], t, x, sig, bootstrap=12, split=False)
        med, lo, hi = r.factors[0].coef[(0, 2)]
        assert hi.real - lo.real > 0
        hits += lo.real <= -0.3 <= hi.real
    assert hits >= 3
