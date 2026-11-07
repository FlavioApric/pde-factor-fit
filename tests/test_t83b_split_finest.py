"""T99: an exact split (T80) is repeated down to the finest factorisation of the same symbol.
tau^3 + c tau xi^4 = tau (tau - i sqrt(c) xi^2)(tau + i sqrt(c) xi^2): one grouping step proposes
{tau} | {tau^2 + c xi^4}; the finest exact split of a real field is the conjugation-closed set over C."""
import numpy as np
import sympy as sp

from pdefactor import loop as L
from pdefactor.symbols import tau, xi


def _rep(expr):
    cd = L._coef_dict(sp.expand(expr))
    return L.FactorReport(sp.expand(expr), 1.0, {k: (complex(v), complex(v), complex(v)) for k, v in cd.items()},
                          status="test", kappa_support=[1.0, 2.0])


def test_cubic_with_a_superfluous_root_splits_to_the_conjugate_pair():
    c = 0.0903
    f = _rep(tau**3 + c * tau * xi**4)
    kband = 2 * np.pi * 5 / (2 * np.pi)
    props, src = L.split_branches([f], kband)
    assert len(props) == 2 and L._same_product(props, [f])  # one step stops at tau | tau^2 + c xi^4
    fin, s2 = L._split_exact_finest(props, src, kband, real=True)
    assert len(fin) == 3 and s2 == [0, 0, 0]
    assert L._same_product(fin, [f], rtol=1e-8) and L._conj_closed(fin)
    nonreal = [g for g in fin if L._nonreal(g)]
    assert len(nonreal) == 2
    for g in nonreal:
        b = complex(g.coef[(0, 2)][0])
        assert abs(abs(b.imag) - np.sqrt(c)) < 1e-6 and abs(b.real) < 1e-8


def test_irreducible_factor_is_left_alone():
    f = _rep(tau**2 + 0.3 * tau + 0.5 * xi**2)  # damped wave: discriminant 0.09 - 2 xi^2 is not a square
    fin, s2 = L._split_exact_finest([f], [0], 5.0, real=True)
    assert len(fin) == 1 and s2 == [0]


def test_switch_follows_branch_ard_by_default():
    import os
    if os.environ.get("PDEFACTOR_SPLIT_FINEST") is None:
        assert L.SPLIT_FINEST == (os.environ.get("PDEFACTOR_BRANCH_ARD", "1") == "1")
