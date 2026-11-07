"""Random PDE simulator (PHASE4 P0.3 gate: exact dispersion of every draw)."""
import numpy as np
import sympy as sp

from pdefactor.simulator import FAMILIES, LAM_MAX, RE_MAX, check_dispersion, match, random_pde
from pdefactor.symbols import tau, xi


def test_every_draw_is_exact_stable_and_deterministic():
    for fam in FAMILIES:
        for s in range(12):
            d = random_pde(fam, s)
            assert check_dispersion(d) < 1e-10, (fam, s)
            for c in d.field.components:
                assert len(c.lams) > 0
                assert np.all(c.lams.real <= RE_MAX + 1e-12) and np.all(np.abs(c.lams) < LAM_MAX)
            assert [str(q) for q in random_pde(fam, s).factors] == [str(q) for q in d.factors]


def test_families_have_their_shape():
    for s in range(12):
        assert all(sp.Poly(q, tau).degree() == 1 for q in random_pde("F1", s).factors)
        assert all(sp.Poly(q, tau).degree() == 2 for q in random_pde("F3", s).factors)
        assert len(random_pde("F4", s).field.components) >= 2


def test_complex_factor_of_real_field_listed_with_conjugate():
    for s in range(12):
        d = random_pde("F2", s)
        cplx = [q for q in d.factors if any(sp.im(sp.N(c)) != 0 for c in sp.Poly(q, tau, xi).coeffs())]
        assert len(cplx) % 2 == 0


def test_match_is_scale_aware():
    q = tau + 0.01 * xi**4 + xi
    assert match([q], [tau + 0.0104 * xi**4 + xi])[0]
    assert not match([q], [tau + 0.03 * xi**4 + xi])[0]  # absolute 0.02 off would pass a 0.05 rule
    assert not match([q], [tau + xi])[0]
    assert match([tau + xi, tau - 0.3 * xi**2], [tau - 0.301 * xi**2, tau + 1.002 * xi])[0]
