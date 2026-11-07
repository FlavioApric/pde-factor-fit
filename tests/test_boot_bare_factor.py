"""With the bundle on (BRANCH_ARD / SPLIT_FINEST) the exact finest split can leave a bare factor
tau^m (no coefficient) next to the refined ones after the refinement; heat grid 1 % reports
(tau + 0.3 xi^2) tau. Each bootstrap copy's refinement drops the bare factor, and the copy was skipped
because its active set was shorter than the factor list, so every copy was skipped and the xi^2
interval kept the split's zero width (lo == hi == med). The bootstrap must refit it anyway."""
import numpy as np
import sympy as sp

from pdefactor import loop as L
from pdefactor import refine_raw as R
from pdefactor.symbols import tau, xi
from pdefactor.synthetic import case, grid


def _factors():
    out = []
    for e in (tau - 0.29931434240342597 * xi**2, tau):
        cd = L._coef_dict(sp.expand(e))
        out.append(L.FactorReport(sp.expand(e), 1.0, {k: (complex(v),) * 3 for k, v in cd.items()}))
    return out


def _heat():
    t, x, u0 = grid(case("heat"), nt=48, nx=64)
    sig = 1e-2 * np.std(u0)
    return t, x, u0 + sig * np.random.default_rng(0).standard_normal(u0.shape), sig


def test_bootstrap_width_with_a_bare_split_factor_bundle_on(monkeypatch):
    monkeypatch.setattr(L, "SPLIT_FINEST", True)
    monkeypatch.setattr(R, "BRANCH_ARD", True)
    t, x, u, sig = _heat()
    fs = _factors()
    L.bootstrap_intervals(fs, u, t, x, sig, B=12, kmax=5)
    med, lo, hi = fs[0].coef[(0, 2)]
    assert hi.real - lo.real > 1e-5
    assert lo.real <= med.real <= hi.real
    assert fs[1].coef == {(1, 0): (1 + 0j,) * 3}


def test_bootstrap_unchanged_with_the_bundle_off(monkeypatch):
    monkeypatch.setattr(L, "SPLIT_FINEST", False)
    monkeypatch.setattr(R, "BRANCH_ARD", False)
    t, x, u, sig = _heat()
    fs = _factors()
    L.bootstrap_intervals(fs, u, t, x, sig, B=6, kmax=5)
    med, lo, hi = fs[0].coef[(0, 2)]
    assert lo == hi == med  # off: the old rule (copies with a dropped factor skipped)
