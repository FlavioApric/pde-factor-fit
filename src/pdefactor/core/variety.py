"""Fit of the dispersion variety and its numerical factorisation.

P(tau, xi) = tau^m + sum_{k<m} p_k(xi) tau^k   (monic in tau: the identifiability setting, II-C1)
is fitted by weighted least squares on the points (lam, i kappa). Factors are found by tracking
the m roots lam_r(xi) along a generic complex line and testing which groups of branches have
polynomial elementary symmetric functions (approximate absolute factorisation).
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations

import numpy as np
import sympy as sp
from scipy.optimize import linear_sum_assignment

from ..symbols import tau, xi


@dataclass
class PolySymbol:
    """Monic-in-tau symbol: coeffs[k] = numpy poly coefficients (increasing powers of xi) of p_k, k < m."""
    m: int
    coeffs: list  # list of length m of complex arrays (increasing powers)

    def __call__(self, lam, xi_):
        lam = np.asarray(lam, complex)
        xi_ = np.asarray(xi_, complex)
        v = lam**self.m
        for k, c in enumerate(self.coeffs):
            v = v + np.polynomial.polynomial.polyval(xi_, c) * lam**k
        return v

    def roots(self, xi0):
        """The m roots in tau at xi = xi0."""
        c = [1.0 + 0j] + [np.polynomial.polynomial.polyval(xi0, self.coeffs[k]) for k in range(self.m - 1, -1, -1)]
        return np.roots(c)

    def to_sympy(self, tol=1e-8, digits=10):
        expr = tau**self.m
        for k, c in enumerate(self.coeffs):
            for b, v in enumerate(c):
                v = _clean(v, tol, digits)
                if v != 0:
                    expr += v * xi**b * tau**k
        return sp.expand(expr)

    def evolution_terms(self, tol=1e-8):
        """For m == 1: a(xi) = -p_0(xi); returns {n: c_n} with a(xi) = sum c_n xi^n."""
        if self.m != 1:
            return None
        return {b: -v for b, v in enumerate(self.coeffs[0]) if abs(v) > tol}


def _clean(v, tol, digits):
    re, im = float(np.real(v)), float(np.imag(v))
    re = 0.0 if abs(re) < tol else round(re, digits)
    im = 0.0 if abs(im) < tol else round(im, digits)
    return sp.Float(re) + sp.I * sp.Float(im) if im else sp.Float(re)


def _design(lam, xi_, m, dx, sl, sx):
    cols = []
    for k in range(m):
        for b in range(dx + 1):
            cols.append((lam / sl) ** k * (xi_ / sx) ** b)
    return np.stack(cols, axis=1)


def fit_monic(lam, kappa, m, dx, weights=None, real=False):
    """Weighted LS fit of tau^m + sum_{k<m, b<=dx} c_kb xi^b tau^k on points (lam, i kappa).

    Returns (PolySymbol, relative residual, number of unknowns)."""
    lam = np.asarray(lam, complex)
    xi_ = 1j * np.asarray(kappa, float)
    w = np.ones(len(lam)) if weights is None else np.asarray(weights, float)
    sl = max(np.abs(lam).max(), 1e-12)
    sx = max(np.abs(xi_).max(), 1e-12)
    A = _design(lam, xi_, m, dx, sl, sx) * w[:, None]
    rhs = -((lam / sl) ** m) * w
    if real:
        Ar = np.vstack([A.real, A.imag])
        br = np.concatenate([rhs.real, rhs.imag])
        c, *_ = np.linalg.lstsq(Ar, br, rcond=None)
        res = np.linalg.norm(Ar @ c - br) / max(np.linalg.norm(br), 1e-300)
    else:
        c, *_ = np.linalg.lstsq(A, rhs, rcond=None)
        res = np.linalg.norm(A @ c - rhs) / max(np.linalg.norm(rhs), 1e-300)
    coeffs = []
    i = 0
    for k in range(m):
        ck = np.zeros(dx + 1, complex)
        for b in range(dx + 1):
            ck[b] = c[i] * sl ** (m - k) / sx**b
            i += 1
        coeffs.append(ck)
    return PolySymbol(m, coeffs), res, m * (dx + 1)


def select_symbol(modes, m_max=4, dx_max=4, tol=1e-6, real=False, weights=None):
    """Smallest (m, dx) whose relative residual is below tol, with more points than unknowns.

    Returns (PolySymbol or None, info dict). None means MISFIT at every level within the budget."""
    lam, kappa = modes.lam, modes.kappa
    w = weights
    tried = []
    for m in range(1, m_max + 1):
        for dx in range(0, dx_max + 1):
            nunk = m * (dx + 1)
            if len(lam) < nunk + 1:
                tried.append((m, dx, None))
                continue
            P, res, _ = fit_monic(lam, kappa, m, dx, w, real)
            tried.append((m, dx, res))
            if res <= tol:
                return P, {"m": m, "dx": dx, "residual": res, "tried": tried}
    return None, {"tried": tried}


# ------------------------------------------------------------ factorisation
def track_roots(P, xis):
    """Roots of P(., xi) along the path xis, continuously matched step to step."""
    R = np.zeros((len(xis), P.m), complex)
    R[0] = P.roots(xis[0])
    for i in range(1, len(xis)):
        r = P.roots(xis[i])
        cost = np.abs(R[i - 1][:, None] - r[None, :])
        _, col = linear_sum_assignment(cost)
        R[i] = r[col]
    return R


def _elem_sym(R):
    """Elementary symmetric functions of the columns of R (rows = path points)."""
    n = R.shape[1]
    e = np.zeros((R.shape[0], n + 1), complex)
    e[:, 0] = 1
    for j in range(n):
        e[:, 1:] = e[:, 1:] - R[:, [j]] * e[:, :-1]  # builds prod (tau - r_j) coefficients
    return e[:, 1:]  # coefficients of tau^{n-1}, ..., tau^0


def factorise(P, deg_bound=None, ftol=1e-6, npath=400, seed=0):
    """Numerical absolute factorisation of a monic-in-tau PolySymbol.

    Returns a list of PolySymbol factors (each monic in tau) and the residual of each test."""
    m = P.m
    if m == 1:
        return [P], [0.0]
    dx = deg_bound if deg_bound is not None else max(len(c) - 1 for c in P.coeffs)
    rng = np.random.default_rng(seed)
    scale = max(1.0, max(np.abs(c).max() for c in P.coeffs) ** (1 / max(dx, 1)))
    theta = rng.uniform(0.3, 1.2)
    z0 = complex(rng.normal(), rng.normal()) * 0.1
    s = np.linspace(-1.0, 1.0, npath) * scale
    xis = z0 + s * np.exp(1j * theta)
    R = track_roots(P, xis)
    valid = {}
    for size in range(1, m):
        for S in combinations(range(m), size):
            if any(set(v) <= set(S) for v in valid):
                continue
            e = _elem_sym(R[:, S])
            coeffs, worst = [], 0.0
            for j in range(size):
                y = e[:, j]
                V = np.vander(xis, dx + 1, increasing=True)
                c, *_ = np.linalg.lstsq(V, y, rcond=None)
                r = np.linalg.norm(V @ c - y) / max(np.linalg.norm(y), 1.0)
                worst = max(worst, r)
                coeffs.append(c)
            if worst < ftol:
                # e[:, j] is the coefficient of tau^{size-1-j}
                valid[S] = (PolySymbol(size, coeffs[::-1]), worst)
    # partition {0..m-1} by minimal valid subsets
    remaining = set(range(m))
    out, res = [], []
    for S in sorted(valid, key=len):
        if set(S) <= remaining:
            out.append(valid[S][0])
            res.append(valid[S][1])
            remaining -= set(S)
    if remaining:
        S = tuple(sorted(remaining))
        e = _elem_sym(R[:, S])
        V = np.vander(xis, dx + 1, increasing=True)
        coeffs = [np.linalg.lstsq(V, e[:, j], rcond=None)[0] for j in range(len(S))]
        out.append(PolySymbol(len(S), coeffs[::-1]))
        res.append(0.0)
    return out, res


def assign(modes, factors):
    """Index of the factor whose normalised residual |Q_j(lam, i kappa)| is smallest, per mode."""
    xi_ = 1j * modes.kappa
    scores = []
    for Q in factors:
        num = np.abs(Q(modes.lam, xi_))
        den = np.abs(modes.lam) ** Q.m + 1.0
        scores.append(num / den)
    S = np.stack(scores, axis=1)
    return S.argmin(axis=1), S


def refine(modes, factors, labels, real=False, weights=None):
    """Refit every factor by LS on its own points (same m and coefficient degree)."""
    out = []
    for j, Q in enumerate(factors):
        mask = labels == j
        dx = max(len(c) - 1 for c in Q.coeffs)
        if mask.sum() < Q.m * (dx + 1) + 1:
            out.append(Q)
            continue
        w = None if weights is None else weights[mask]
        Qr, _, _ = fit_monic(modes.lam[mask], modes.kappa[mask], Q.m, dx, w, real=False)
        out.append(Qr)
    return out
