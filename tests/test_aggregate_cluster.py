"""S-AGG-CLUSTER: aggregation W, posterior over k, domain grouping (fake posteriors = exact grid +
independent noise draws, standing in for S-INTERP)."""
import copy

import numpy as np
import pytest
from sklearn.metrics import adjusted_rand_score

from pdefactor import cluster as CL
from pdefactor.aggregate import aggregate, align, build_cloud, factor_vector, fake_posterior, run_core
from pdefactor.core.variety import PolySymbol
from pdefactor.synthetic import case, grid

pytestmark = pytest.mark.filterwarnings("ignore")


def _results(name, rel=1e-3, S=8, seed=0):
    f = case(name)
    t, x, u = grid(f, nt=48, nx=64)
    sig = rel * u.std()
    us, pis = fake_posterior(u, sig, S, rng=seed)
    return run_core(us, t, x, sig, pis)


@pytest.fixture(scope="module")
def tpd():
    return _results("transport_plus_diffusion")


@pytest.fixture(scope="module")
def heat():
    return _results("heat", rel=1e-2)


# ------------------------------------------------------------------ cloud and alignment
def test_factor_vector_padding_invariance():
    a = PolySymbol(1, [np.array([0.0, 1.0])])
    b = PolySymbol(1, [np.array([0.0, 1.0, 0.0])])
    assert np.allclose(factor_vector(a), factor_vector(b))
    c = PolySymbol(2, [np.array([1.0]), np.array([0.4])])
    assert not np.allclose(factor_vector(a), factor_vector(c))


def test_alignment_is_invariant_to_factor_order(tpd):
    shuffled = []
    for i, (r, p) in enumerate(tpd):
        r = copy.copy(r)
        r.factors = r.factors[::-1] if i % 2 else list(r.factors)
        shuffled.append((r, p))
    for res in (tpd, shuffled):
        cl = build_cloud(res)
        align(cl)
        # the transport factor (coefficient of xi ~ 1) always lands in the same track
        tr = np.abs(cl.theta[:, 1] - 1.0) < 0.1
        assert len(np.unique(cl.track[tr])) == 1 and len(np.unique(cl.track[~tr])) == 1
        assert cl.track[tr][0] != cl.track[~tr][0]
    a = aggregate(shuffled)
    assert len(a.W_track) == 2


# ------------------------------------------------------------------ W statistics
def test_tpd_aggregate(tpd):
    a = aggregate(tpd)
    W = np.sort(a.W_track)[::-1]
    assert len(W) == 2 and abs(W[0] - 0.77) < 0.05
    assert 1.5 < a.k_eff < 2.0 and a.k_det == 2
    # DP posterior over k: most mass on 2
    assert a.dp.k_map == 2 and a.dp.p_k.get(2, 0) > 0.5
    assert max(a.finite_k, key=a.finite_k.get) == 2
    # the two factors co-occur in every sample
    assert np.allclose(a.track_cooccurrence, 1.0)
    # gamma_N, c_F as distributions; N = 2: c_F = 1 - gamma (P2-C2, THEORY_TO_ALGO T5)
    assert abs(a.gamma.mean - 0.174) < 0.02
    assert abs(a.cF.mean - (1 - a.gamma.mean)) < 1e-9
    assert a.gamma.quantile(0.05) <= a.gamma.mean <= a.gamma.quantile(0.95)
    # single-term factors: E_int = 0 up to noise-level spurious terms
    assert a.rho.mean < 0.05
    assert a.k_structure.get(2, 0) > 0.9
    assert abs(sum(a.structures_pooled.values()) - 1) < 1e-9


def test_heat_aggregate(heat):
    a = aggregate(heat)
    assert a.dp.k_map == 1 and a.dp.p_k.get(1, 0) > 0.5
    assert a.k_det == 1 and abs(a.k_eff - 1) < 1e-9
    assert a.gamma.mean == 1.0 and a.cF.mean == 0.0


# ------------------------------------------------------------------ domain grouping
def test_rectangles_and_adjacency():
    rects = CL.rectangles(2.0, 2 * np.pi, 2, 3)
    A = CL.adjacency(rects)
    assert A.sum() == 2 * 7  # 2x3 grid: 7 shared edges
    lab = CL.connected_split(np.array([0, 1, 0, 0, 0, 0]), A)  # label 0 is connected
    assert len(np.unique(lab)) == 2
    lab = CL.connected_split(np.array([0, 1, 0, 1, 1, 1]), A)  # label 0 split in two pieces
    assert len(np.unique(lab)) == 3
    rects = CL.rectangles(3.0, 3.0, 3, 3)
    ring = np.array([0, 0, 0, 0, 1, 0, 0, 0, 0])
    assert CL.has_hole(rects, ring) and not CL.has_hole(rects, np.array([0, 0, 0, 1, 1, 1, 1, 1, 1]))


@pytest.fixture(scope="module")
def two_regime():
    tr, he = case("transport"), case("heat")
    regions = [(tr, 0.0, np.pi), (he, np.pi, 2 * np.pi)]
    rects = CL.rectangles(2.0, 2 * np.pi, 2, 6)
    wd = CL.window_features(rects, CL.exact_provider(regions), rel_noise=1e-2, S=6)
    return wd, CL.region_truth(rects, regions), regions


@pytest.mark.parametrize("method", ["gmm", "kmeans", "spectral", "agglomerative"])
def test_two_regime_ari(two_regime, method):
    wd, truth, _ = two_regime
    lab = CL.cluster_windows(wd, method)
    assert adjusted_rand_score(truth, lab) >= 0.9
    assert not CL.has_hole(wd.rects, lab)
    A = CL.adjacency(wd.rects)
    assert np.array_equal(np.unique(CL.connected_split(lab, A)).size, np.unique(lab).size)


def test_two_regime_global_W(two_regime):
    wd, _, _ = two_regime
    # every window has one law, so per sample k = 1, while the domain holds two laws (k_eff = 2)
    assert wd.glob.dp.k_map == 1
    # k_eff ~ 2; the note's ceil(k_eff) is fragile: ~1 % spurious mass from one noisy window
    # already gives ceil = 3 (REPORT), so the number of groups is the BIC posterior's MAP instead
    assert abs(wd.glob.k_eff - 2) < 0.25
    pk = CL.k_posterior(wd.F, wd.reg)
    assert max(pk, key=pk.get) == 2


def test_dominant_balance_baseline_runs(two_regime):
    wd, truth, regions = two_regime
    t = np.linspace(0, 2, 96)
    x = np.linspace(0, 2 * np.pi, 128, endpoint=False)
    TT, XX = np.meshgrid(t, x, indexing="ij")
    u = np.where(XX < np.pi, regions[0][0](TT, XX), regions[1][0](TT, XX))
    lab = CL.dominant_balance_labels(u, t, x, wd.rects)
    ari = adjusted_rand_score(truth, lab)
    assert -1.0 <= ari <= 1.0  # reported, no threshold (baseline)
