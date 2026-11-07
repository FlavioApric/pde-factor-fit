"""Symbols of linear constant-coefficient operators in (t, x).

The operator P(d_t, d_x) is represented by its symbol P(tau, xi), a sympy polynomial.
Exact algebra only: factoring, coprimality, the split ambiguity delta(P).
"""
from __future__ import annotations

from itertools import combinations

import sympy as sp

t, x = sp.symbols("t x")
tau, xi = sp.symbols("tau xi")


def apply_op(P, f):
    """Apply P(d_t, d_x) to the sympy expression f(t, x).

    origin: D:\\ProblemaBase\\work\\C1C2\\sympy\\c12_catalog.py:16 (op)
    """
    p = sp.Poly(sp.expand(P), tau, xi)
    return sp.expand(sum(c * sp.diff(f, t, i, x, j) for (i, j), c in p.terms()))


def factors(P, extension=sp.I):
    """Irreducible factors of P over Q(i), monic in their leading term.

    Returns a list of (Q, multiplicity). Constant content is dropped.
    """
    _, fl = sp.factor_list(sp.expand(P), tau, xi, extension=extension)
    out = []
    for q, m in fl:
        q = sp.Poly(q, tau, xi)
        if q.total_degree() == 0:
            continue
        out.append((sp.expand(q.as_expr() / q.LC()), m))
    return out


def quotient_dim(gens, bound=40):
    """dim_C C[tau, xi]/(gens) for a zero-dimensional ideal, by counting standard monomials.

    Returns None if the ideal is not zero-dimensional within the bound.
    origin: D:\\ProblemaBase\\work\\C1C2\\sympy\\c12_catalog.py:32
    """
    G = sp.groebner(gens, tau, xi, order="grevlex")
    if G.exprs == [1]:
        return 0
    lead = [sp.Poly(g, tau, xi).monoms(order="grevlex")[0] for g in G.exprs]
    has_pure_tau = any(b == 0 and a > 0 for a, b in lead)
    has_pure_xi = any(a == 0 and b > 0 for a, b in lead)
    if not (has_pure_tau and has_pure_xi):
        return None
    return sum(
        1
        for i in range(bound)
        for j in range(bound)
        if not any(i >= a and j >= b for a, b in lead)
    )


def split_ambiguity(factor_list_):
    """delta(P) = sum_{i<j} dim R/(Q_i, Q_j) (C12-T1): dimension of the finite ambiguity of u = sum u_j."""
    qs = [q for q, _ in factor_list_]
    total = 0
    for a, b in combinations(qs, 2):
        d = quotient_dim([a, b])
        if d is None:
            return None  # not coprime / common component: infinite ambiguity
        total += d
    return total


def evolution_branch(Q):
    """If Q = tau - a(xi) (monic, degree 1 in tau) return a(xi), else None."""
    p = sp.Poly(Q, tau)
    if p.degree() != 1:
        return None
    lc = p.coeffs()[0]
    if sp.Poly(lc, xi).degree() != 0:
        return None
    return sp.expand(-p.as_expr().subs(tau, 0) / lc)


def disc_is_square(Q):
    """For Q monic of degree 2 in tau: does Q split over C[xi] (C12-P2)?

    origin: D:\\ProblemaBase\\work\\C1C2\\sympy\\c12_factors.py:80 (disc_square)
    """
    p = sp.Poly(Q, tau)
    if p.degree() != 2:
        return None
    a, b, c = p.all_coeffs()
    d = sp.expand(b**2 - 4 * a * c)
    _, fl = sp.factor_list(d, xi, extension=sp.I)
    return all(m % 2 == 0 for _, m in fl)


def symbol_from_terms(terms):
    """Build tau - a(xi) from a dict {power n: coefficient c_n} meaning a(xi) = sum c_n xi^n."""
    return tau - sum(c * xi**n for n, c in terms.items())


def symbol_to_str(Q):
    """Readable operator form: tau -> d_t, xi -> d_x."""
    s = sp.sstr(sp.expand(Q))
    return s.replace("tau", "dt").replace("xi", "dx")
