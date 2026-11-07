"""v2.13 generalisations: order-3 candidates (G1), branch-partition split of any reducible factor (G4),
relative non-real test (G6), growth options in both directions (G7). Unit level, exact symbols."""
import numpy as np
import sympy as sp

from pdefactor.core.structfit import analyze_structured, candidate_structures
from pdefactor.loop import FactorReport, _grow_options, _nonreal, split_branches
from pdefactor.symbols import tau, xi
from pdefactor.synthetic import any_case, grid


def _rep(q, W=1.0):
    p = sp.Poly(sp.expand(q), tau, xi, domain="CC")
    coef = {}
    for mo, c in zip(p.monoms(), p.coeffs()):
        v = complex(c)
        coef[mo] = (v, v, v)
    return FactorReport(sp.expand(q), W, coef)


def _same(a, b, tol=1e-8):
    d = sp.Poly(sp.expand(a - b), tau, xi, domain="CC")
    return all(abs(complex(c)) < tol for c in d.coeffs())


def test_candidates_include_order3_irreducible():
    cs = candidate_structures(m_max=3, dx_max=2)
    assert ((3, 2),) in cs or any(len(s) == 1 and s[0][0] == 3 for s in cs)
    assert all(len(s) >= 1 and sum(m for m, _ in s) <= 3 for s in cs)


def test_core_fits_irreducible_cubic_in_tau():
    t, x, u = grid(any_case("cubic_tau"))
    r = analyze_structured(u, t, x, real=True)
    assert len(r.factors) == 1
    assert sp.Poly(r.factors[0].sympy, tau).degree() == 3


def test_split_branches_reducible_products():
    for q in [(tau + xi) * (tau - 0.3 * xi**2),
              (tau + xi) * (tau - xi) * (tau - 0.3 * xi**2),
              (tau + 0.2 - 0.1j * xi**2) * (tau + 0.2 + 0.1j * xi**2)]:
        out, src = split_branches([_rep(sp.expand(q))], 3.0)
        assert len(out) >= 2 and src == [0] * len(out)
        assert _same(sp.Mul(*[f.sympy for f in out]), sp.expand(q), 1e-6)
        assert all("reducible factor" in f.status for f in out)


def test_split_branches_leaves_irreducible_heat_and_transport():
    out, _ = split_branches([_rep(tau - 0.3 * xi**2), _rep(tau + xi)], 3.0)
    assert len(out) == 2 and all(f.status == "not checked" for f in out)


def test_nonreal_is_scale_free():
    small = _rep(tau - 1e-6j * xi**2)
    assert _nonreal(small)  # the old absolute 1e-9 test is passed too, but scale matters below
    tiny_imag = _rep(tau - (1e4 + 1e-6j) * xi**2)
    assert not _nonreal(tiny_imag)  # imaginary part negligible relative to the coefficient
    f = _rep(tau - 0.3j * xi**2)
    f.coef[(0, 2)] = (-0.3j, -0.5j, 0.1j)  # interval of the imaginary part covers 0
    assert not _nonreal(f)


def test_grow_options_both_directions():
    assert _grow_options((3, 4)) == [(3, 5), (4, 4)]
    assert _grow_options((4, 8)) == []
    assert _grow_options((4, 7)) == [(4, 8)]


def test_branch_point_of_irreducible_law_is_not_confluent():
    """Damped beam tau^2 + 0.2 tau + 0.03 xi^4: its two roots nearly meet near kappa ~ 0.76 (zero of the
    discriminant). That bin looked confluent and made the whole result UNDECIDED; a fitted squarefree
    factor now explains it (repeated factors stay UNDECIDED, test_core_v2)."""
    t, x, u = grid(any_case("damped_beam"))
    rng = np.random.default_rng(5)
    sig = 1e-2 * np.std(u)
    r = analyze_structured(u + sig * rng.standard_normal(u.shape), t, x, noise=sig, real=True)
    assert r.label != "UNDECIDED"
    assert len(r.factors) == 1 and sp.Poly(r.factors[0].sympy, tau).degree() == 2


def test_conj_closed():
    from pdefactor.loop import FactorReport, _conj_closed

    def rep(cd):
        return FactorReport(sum(tau**a * xi**b * v for (a, b), v in cd.items()), 1.0,
                            {k: (complex(v), complex(v), complex(v)) for k, v in cd.items()})

    a = rep({(1, 0): 1, (0, 1): 0.9, (0, 0): 0.3 + 0.4j})
    b = rep({(1, 0): 1, (0, 1): 0.9, (0, 0): 0.3 - 0.4j})
    c = rep({(1, 0): 1, (0, 1): -1.1, (0, 0): 0.3 - 0.3j})
    r = rep({(1, 0): 1, (0, 2): -0.3})
    assert _conj_closed([a, b, r]) and _conj_closed([r])
    assert not _conj_closed([a, c, r])  # two complex factors that are not conjugates (cubic_tau, 1 %)


def test_n_real_params_counts_the_product():
    from pdefactor.loop import FactorReport, _n_real_params

    def rep(cd):
        return FactorReport(sum(tau**a * xi**b * v for (a, b), v in cd.items()), 1.0,
                            {k: (complex(v), complex(v), complex(v)) for k, v in cd.items()})

    assert _n_real_params([rep({(1, 0): 1, (0, 1): 1.0}), rep({(1, 0): 1, (0, 1): -1.0})]) == 1  # tau^2 - xi^2
    assert _n_real_params([rep({(1, 0): 1, (0, 2): 0.3j}), rep({(1, 0): 1, (0, 2): -0.3j})]) == 1  # beam


def test_supports_identifies_the_same_model_across_structure_labels():
    from pdefactor.loop import FactorReport, _supports

    def rep(cd):
        return FactorReport(sum(tau**a * xi**b * v for (a, b), v in cd.items()), 1.0,
                            {k: (complex(v), complex(v), complex(v)) for k, v in cd.items()})

    heat = rep({(1, 0): 1, (0, 2): -0.3})
    heat_from_dx3 = rep({(1, 0): 1, (0, 2): -0.2995, (0, 3): 0, (0, 1): 0})  # (1,3) with xi^3, xi dropped
    adv = rep({(1, 0): 1, (0, 1): 0.1, (0, 2): -0.3})
    assert _supports([heat]) == _supports([heat_from_dx3])
    assert _supports([heat]) != _supports([adv])
    assert _supports([heat, adv]) == _supports([adv, heat])


def test_supports_matches_a_conjugate_pair_with_its_product_only():
    """Same family = same product support and same free real parameters (conjugate pair counted
    once). The beam pair (tau -/+ i a xi^2) and tau^2 + c xi^4 are one family (1 parameter); TPD
    factored (2 parameters) is not the irreducible quadratic with the same product support (3)."""
    from pdefactor.loop import FactorReport, _supports

    def rep(cd):
        return FactorReport(sum(tau**a * xi**b * v for (a, b), v in cd.items()), 1.0,
                            {k: (complex(v), complex(v), complex(v)) for k, v in cd.items()})

    pair = [rep({(1, 0): 1, (0, 2): 0.3j}), rep({(1, 0): 1, (0, 2): -0.3j})]
    prod = [rep({(2, 0): 1, (0, 4): 0.0900042})]
    assert _supports(pair) == _supports(prod)
    tpd = [rep({(1, 0): 1, (0, 1): 1.0}), rep({(1, 0): 1, (0, 2): -0.3})]
    irr = [rep({(2, 0): 1, (1, 1): 1.0, (1, 2): -0.3, (0, 3): -0.29})]
    assert _supports(tpd)[0] == _supports(irr)[0]   # same product support
    assert _supports(tpd) != _supports(irr)         # but a larger family
    k = 2.5  # scale invariance: rescaled coefficients keep the signature
    assert _supports([rep({(1, 0): 1, (0, 2): 0.3j * k}), rep({(1, 0): 1, (0, 2): -0.3j * k})]) == _supports(pair)


def test_confluent_bins_rechecked_against_final_factors():
    """A sample the core labelled UNDECIDED for a confluent bin is relabelled only when the bin is a
    branch point of a final factor (structfit._branch_point): the damped beam's real quadratic
    tau^2 + 0.2 tau + 0.03 xi^4 has close roots near kappa = 1 only. A repeated factor (tau + xi)^2
    has close roots at every kappa and stays UNDECIDED (OPF5B-T6)."""
    from types import SimpleNamespace

    from pdefactor.loop import FactorReport, _relabel_branch_points

    def rep(cd):
        return FactorReport(sum(tau**a * xi**b * v for (a, b), v in cd.items()), 1.0,
                            {k: (complex(v), complex(v), complex(v)) for k, v in cd.items()})

    ks = [list(range(1, 9))]
    for scale in (1.0, 4.0):  # rates x scale, T / scale: the criterion is in units of 1/T
        T = 2.0 / scale
        res = [(SimpleNamespace(label="UNDECIDED", confluent=[(1.0, -0.1 * scale, 30.0)], info={}), 1.0)]
        damped = rep({(2, 0): 1, (1, 0): 0.2 * scale, (0, 4): 0.03 * scale**2})
        assert _relabel_branch_points(res, [damped], ks, T) == {"FIT-COMPATIBLE": 1.0}
    res = [(SimpleNamespace(label="UNDECIDED", confluent=[(1.0, -1j, 30.0)], info={}), 1.0)]
    repeated = rep({(2, 0): 1, (1, 1): 2.0, (0, 2): 1.0})
    assert _relabel_branch_points(res, [repeated], ks, 2.0) == {"UNDECIDED": 1.0}
    assert _relabel_branch_points(res, [rep({(1, 0): 1, (0, 1): 1.0})], ks, 2.0) == {"UNDECIDED": 1.0}


def test_confluent_bins_between_factors_rechecked_on_their_product():
    """Roots of two different final factors meeting at one kappa (a conjugate pair at kappa = 0, the
    shared-mode case) are explained through the squarefree product; two identical factors (a repeated
    factor) have a non-squarefree product, close roots at every kappa, and stay UNDECIDED (OPF5B-T6)."""
    from types import SimpleNamespace

    from pdefactor.loop import FactorReport, _relabel_branch_points

    def rep(cd):
        return FactorReport(sum(tau**a * xi**b * v for (a, b), v in cd.items()), 1.0,
                            {k: (complex(v), complex(v), complex(v)) for k, v in cd.items()})

    ks = [list(range(0, 9))]
    pair = [rep({(1, 0): 1, (0, 2): 0.3j}), rep({(1, 0): 1, (0, 2): -0.3j})]
    res = [(SimpleNamespace(label="UNDECIDED", confluent=[(0.0, 0.0, 30.0)], info={}), 1.0)]
    assert _relabel_branch_points(res, pair, ks, 2.0) == {"FIT-COMPATIBLE": 1.0}
    twice = [rep({(1, 0): 1, (0, 1): 1.0}), rep({(1, 0): 1, (0, 1): 1.0})]
    res = [(SimpleNamespace(label="UNDECIDED", confluent=[(1.0, -1j, 30.0)], info={}), 1.0)]
    assert _relabel_branch_points(res, twice, ks, 2.0) == {"UNDECIDED": 1.0}


def test_bare_mention_tie_rule():
    """T74: a refined-score gap within LOG_BF_BARE is not evidence; inside it the model with fewer real
    parameters is kept, outside it the higher score wins whatever its size (scale-free)."""
    from pdefactor.loop import LOG_BF_BARE, _beats

    assert not _beats(522.9, 2, 522.7, 1)           # beam 400 s1: +0.2 nat with one more parameter
    assert _beats(522.7, 1, 522.9, 2)               # the same pair seen from the other side
    assert not _beats(10.5, 2, 10.0, 2)             # equal size: the current model stays
    assert _beats(10.0 + LOG_BF_BARE + 0.1, 5, 10.0, 1)
    assert not _beats(10.0 - LOG_BF_BARE - 0.1, 0, 10.0, 3)
    for scale in (1e-3, 1.0, 1e4):                  # depends on score differences only
        assert _beats(scale + 2.0, 3, scale, 1) and not _beats(scale + 0.5, 3, scale, 1)


def test_bootstrap_of_the_refined_estimator_keeps_supported_terms():
    """T75: on a grid the reported coefficients come from the refinement on the observations, so the
    bootstrap refits each copy by that refinement. The core's mode-level spread put 0 inside the
    interval of the constant of tau^3 + 0.6 tau^2 + (1 - xi^2) tau + 0.2 and pruned() dropped it."""
    from pdefactor.loop import (_coef_dict, _grid_obs, _raw_kmax, bootstrap_intervals, extract_modes_ic,
                                refine_factors)

    t, x, u = grid(any_case("cubic_tau"))
    sig = 0.01 * np.abs(u).max()
    u = u + sig * np.random.default_rng(0).standard_normal(u.shape)
    obs = _grid_obs(u, t, x, sig)
    m_ref, *_ = extract_modes_ic(u, t, x, noise=sig)
    kmax = _raw_kmax(m_ref, obs["period"])
    e = sp.expand(tau**3 + sp.Float(0.6) * tau**2 + (1 - xi**2) * tau + sp.Float(0.2))
    f = [FactorReport(e, 1.0, {k: (v, v, v) for k, v in _coef_dict(e).items()})]
    refine_factors(f, obs, kmax)
    bootstrap_intervals(f, u, t, x, sig, B=8, kmax=kmax)
    med, lo, hi = f[0].coef[(0, 0)]
    assert lo.real > 0 and lo.real <= 0.2 * 1.05 and hi.real >= 0.2 * 0.95
