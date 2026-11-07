"""T100: under BRANCH_ARD the support path of the refinement covers the class xi-degree (PATH_CLASS, T94).
E13 F1-3 grid 1 %: truth tau + 1.51e-4 xi^4 - 2.28e-3 xi^3; the core rounds the xi^4 term to 0. The true law
outranks the 5-term order-2 law the run reported on the branch evidence itself (the score is right), so the
failure was the search: the xi^4 support must be offered to refine."""
import os

import numpy as np
import sympy as sp

from pdefactor import loop as L
from pdefactor import refine_raw as R
from pdefactor.simulator import random_pde
from pdefactor.symbols import tau, xi
from pdefactor.synthetic import grid

TRUTH = tau + 0.000151 * xi**4 - 0.00228 * xi**3
QUAD = (tau**2 - 0.00226337674981885 * tau * xi**3 - 0.0123542223144204 * tau * xi**2
        + 0.0163314823322383 * tau * xi - 0.00075568065896185 * xi**3 - 0.00426177127315549 * xi)


def _f13():
    d = random_pde("F1", 3)
    t, x, u = grid(d.field)
    rng = np.random.default_rng(1003)
    sig = 0.01 * np.std(u)
    return t, x, u + sig * rng.standard_normal(u.shape), sig


def test_switch_follows_branch_ard_by_default():
    if os.environ.get("PDEFACTOR_PATH_CLASS") is None:
        assert L.PATH_CLASS == (os.environ.get("PDEFACTOR_BRANCH_ARD", "1") == "1")


def test_true_first_order_law_beats_the_order_two_law_on_the_branch_evidence():
    t, x, u, sig = _f13()
    obs = L._grid_obs(u, t, x, sig)
    ev_t = R.log_evidence_branch([L._poly_symbol(sp.expand(TRUTH))], obs, 9)
    ev_q = R.log_evidence_branch([L._poly_symbol(sp.expand(QUAD))], obs, 9)
    occ = 0.5 * np.log(len(obs["ys"]))
    assert ev_t - 2 * occ > ev_q - 5 * occ + 25.0  # +56 nats raw, p = 2 vs 5


def test_support_path_offers_the_rounded_xi4_term(monkeypatch):
    monkeypatch.setattr(L, "PATH_CLASS", True)
    t, x, u, sig = _f13()
    core = tau - 0.0022763328 * xi**3  # the core's pooled factor: xi^4 rounded to 0
    cd = L._coef_dict(sp.expand(core))
    f = L.FactorReport(sp.expand(core), 1.0, {k: (complex(v),) * 3 for k, v in cd.items()})
    on = L.support_path([f], u, t, x, sig, dx_class=4)
    sups = [set(c) for paths in on.values() for path in paths for c in path]
    assert {(1, 0), (0, 3), (0, 4)} in sups
    monkeypatch.setattr(L, "PATH_CLASS", False)
    off = L.support_path([f], u, t, x, sig, dx_class=4)
    assert all((0, 4) not in c for paths in off.values() for path in paths for c in path)
    # the class path is added after the factor's own path, never substituted for it (two_pairs grid 1 %)
    assert len(on[0]) == len(off[0]) + 1
    assert [set(c) for c in on[0][0]] == [set(c) for c in off[0][0]]
    assert [set(c) for c in on[0][-1]] == [set(c) for c in off[0][-1]]  # the Wald path
