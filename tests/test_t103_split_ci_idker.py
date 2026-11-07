"""T103: (a) the factors of a split carry the unsplit factor's intervals through the split map (an exact
split is not refined afterwards, so on scattered input its zero-width point intervals were reported);
(b) the core's ID-KER verdict on its own factors is re-checked on the reported factors; (c) the kappa
support is that of the reported factors, shared by a real field's conjugate pair."""
import os

import numpy as np
import sympy as sp

from pdefactor import loop as L
from pdefactor.symbols import tau, xi


def _rep(expr, coef=None, ks=(1.0, 2.0)):
    cd = L._coef_dict(sp.expand(expr))
    c = coef or {k: (complex(v), complex(v), complex(v)) for k, v in cd.items()}
    return L.FactorReport(sp.expand(expr), 1.0, c, status="test", kappa_support=list(ks))


def test_split_intervals_follow_the_unsplit_factor(monkeypatch):
    monkeypatch.setattr(L, "SPLIT_CI", True)
    c = 0.09
    f = _rep(tau**2 + c * xi**4, {(2, 0): (1 + 0j, 1 + 0j, 1 + 0j), (0, 4): (c + 0j, 0.085 + 0j, 0.095 + 0j)})
    props, src = L.split_branches([f], 3.0)
    assert len(props) == 2 and src == [0, 0] and L._same_product(props, [f])
    lo_t, hi_t = np.sqrt(0.085), np.sqrt(0.095)  # sqrt is monotone: the 90 % interval maps through it
    for g in props:
        v, lo, hi = g.coef[(0, 2)]
        assert abs(abs(v.imag) - np.sqrt(c)) < 1e-9
        a, b = sorted((abs(lo.imag), abs(hi.imag)))
        assert a < abs(v.imag) < b
        assert abs(a - lo_t) < 0.003 and abs(b - hi_t) < 0.003  # Monte Carlo (200 draws)
        assert g.coef[(1, 0)] == (1 + 0j, 1 + 0j, 1 + 0j)
    # the finest exact split of tau (tau^2 + c xi^4) keeps them (two steps, T99)
    f3 = _rep(sp.expand(tau * (tau**2 + c * xi**4)),
              {(3, 0): (1 + 0j, 1 + 0j, 1 + 0j), (1, 4): (c + 0j, 0.085 + 0j, 0.095 + 0j)})
    fin, _ = L._split_exact_finest(*L.split_branches([f3], 3.0), 3.0, True)
    widths = sorted(abs(g.coef[(0, 2)][2].imag - g.coef[(0, 2)][1].imag) for g in fin if (0, 2) in g.coef)
    assert len(widths) == 2 and all(0.01 < w < 0.02 for w in widths)


def test_split_without_widths_and_switch_off_keep_point_intervals(monkeypatch):
    f = _rep(tau**2 + 0.09 * xi**4)  # zero-width source: nothing to carry
    monkeypatch.setattr(L, "SPLIT_CI", True)
    props, _ = L.split_branches([f], 3.0)
    assert all(v[1] == v[0] == v[2] for g in props for v in g.coef.values())
    g = _rep(tau**2 + 0.09 * xi**4, {(2, 0): (1 + 0j, 1 + 0j, 1 + 0j), (0, 4): (0.09 + 0j, 0.085 + 0j, 0.095 + 0j)})
    monkeypatch.setattr(L, "SPLIT_CI", False)
    props, _ = L.split_branches([g], 3.0)
    assert all(v[1] == v[0] == v[2] for h in props for v in h.coef.values())


def test_identified_is_the_core_test_on_the_reported_factors():
    a = _rep(tau - 0.3j * xi**2)
    # 4 modes at 4 |kappa|: n >= m (dx + 1) + 1 = 4, nk >= 3, 1 mode at one kappa >= m = 1
    assert L._identified([a], [{1.0: 1, 2.0: 1, 3.0: 1, 4.0: 1}])
    assert not L._identified([a], [{1.0: 1, 2.0: 1, 3.0: 1}])  # 3 modes < 4
    assert not L._identified([a], [{1.0: 2, 2.0: 2}])  # 2 distinct |kappa| < dx + 1
    # mirror modes of a real field count once per |kappa|
    assert not L._identified([a], [{1.0: 1, -1.0: 1, 2.0: 1, -2.0: 1, 3.0: 1}])
    # II-C1: an order-3 factor needs 3 modes at one kappa (tau^3 + c tau xi^4: the third branch is unexcited)
    b = _rep(tau**3 + 0.09 * tau * xi**4)
    assert not L._identified([b], [{k: 2 for k in (1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0)}])
    assert not L._identified([a], [{}])


def test_conjugate_pair_shares_its_kappa_support():
    a, b, h = _rep(tau - 0.3j * xi**2), _rep(tau + 0.3j * xi**2), _rep(tau - 0.1 * xi**2)
    sup = L._conj_shared_support([a, b, h], [[1.0, 2.0, 4.0, 5.0], [1.0], [3.0]])
    assert sup == [[1.0, 2.0, 4.0, 5.0], [1.0, 2.0, 4.0, 5.0], [3.0]]
    c = _rep(tau + 0.31j * xi**2)  # not the conjugate: supports stay their own
    assert L._conj_shared_support([a, c], [[1.0, 2.0], [1.0]]) == [[1.0, 2.0], [1.0]]


def test_switches_follow_branch_ard_by_default():
    import importlib

    keys = ("PDEFACTOR_BRANCH_ARD", "PDEFACTOR_SPLIT_CI", "PDEFACTOR_IDKER_FINAL")
    old = {k: os.environ.get(k) for k in keys}
    try:
        for v in ("0", "1"):
            for k in keys:
                os.environ.pop(k, None)
            os.environ["PDEFACTOR_BRANCH_ARD"] = v
            m = importlib.reload(L)
            assert m.SPLIT_CI == (v == "1") and m.IDKER_FINAL == (v == "1")
    finally:
        for k, v in old.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
        importlib.reload(L)
