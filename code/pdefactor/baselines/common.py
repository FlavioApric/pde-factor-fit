"""Shared pieces of the baselines: result type, linear derivative library, symbol factoring.

Convention (same as the core): library term d_t^a d_x^b u <-> tau^a xi^b; the model
d_t^m u = sum c_ab d_t^a d_x^b u has symbol P = tau^m - sum c_ab tau^a xi^b.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import sympy as sp
from scipy.optimize import least_squares

from ..symbols import tau, xi


@dataclass
class BaselineResult:
    method: str
    applicable: bool = True
    reason: str = ""
    P: object = None  # sympy symbol, monic in tau^m
    coeffs: dict = field(default_factory=dict)  # {(a, b): c} of P (includes (m, 0): 1)
    m: int = 0
    factors: list = field(default_factory=list)  # sympy, monic in tau
    structure: tuple = ()  # sorted ((m_j, dx_j), ...), like structfit.candidate_structures
    structure_probs: list | None = None  # [(structure, p)] if the method gives a distribution
    runtime: float = 0.0
    info: dict = field(default_factory=dict)


def lib_index(m, dx_max=4):
    return [(a, b) for a in range(m) for b in range(dx_max + 1)]


# ------------------------------------------------------------------ strong-form derivatives
def dx_spectral(u, x, b):
    """d_x^b u along axis 1 on a periodic uniform grid."""
    if b == 0:
        return u
    L = (x[1] - x[0]) * len(x)
    k = 2 * np.pi * np.fft.fftfreq(len(x), d=L / len(x))
    d = np.fft.ifft((1j * k) ** b * np.fft.fft(u, axis=1), axis=1)
    return d if np.iscomplexobj(u) else d.real


def dt_fd(u, t, a, order=4):
    """d_t^a u along axis 0 with pysindy's FiniteDifference (order 4: order 2 is too coarse for the
    fast-decaying modes at dt = T/63; see REPORT)."""
    if a == 0:
        return u
    import pysindy as ps

    if np.iscomplexobj(u):
        return dt_fd(u.real, t, a, order) + 1j * dt_fd(u.imag, t, a, order)
    return ps.FiniteDifference(order=order, d=a, axis=0)(u, t)


def strong_system(u, t, x, m, dx_max=4, trim=4):
    """Theta (rows = grid points, cols = lib_index(m)) and target d_t^m u, edges in t trimmed."""
    idx = lib_index(m, dx_max)
    cache = {}

    def D(a, b):
        if (a, b) not in cache:
            cache[(a, b)] = dt_fd(dx_spectral(u, x, b), t, a)[trim:-trim].ravel()
        return cache[(a, b)]

    Th = np.stack([D(a, b) for a, b in idx], 1)
    return Th, D(m, 0), idx


# ------------------------------------------------------------------ weak form
def _bump(lo, hi, p):
    """numpy Polynomial ((s - lo)(hi - s))^p, zero with p-1 derivatives at both ends."""
    P = np.polynomial.Polynomial
    return (P([-lo, 1]) * P([hi, -1])) ** p


def weak_system(u, t, x, m, dx_max=4, K=200, p=6, Ht=None, Hx=None, seed=0):
    """Weak-form system: rows = test functions phi_k = psi_t(t) psi_x(x),
    G[k, (a,b)] = (-1)^(a+b) int u d_t^a d_x^b phi_k,  y[k] = (-1)^m int u d_t^m phi_k.
    Same math as pysindy.WeakPDELibrary (Messenger & Bortz 2021)."""
    rng = np.random.default_rng(seed)
    T0, T1 = t[0], t[-1]
    L = (x[1] - x[0]) * len(x)
    Ht = Ht or (T1 - T0) / 4
    Hx = Hx or L / 4
    wt = np.gradient(t)  # trapezoid-like weights
    wx = np.full(len(x), x[1] - x[0])
    idx = lib_index(m, dx_max)
    G = np.zeros((K, len(idx)), dtype=complex if np.iscomplexobj(u) else float)
    y = np.zeros(K, dtype=G.dtype)
    for k in range(K):
        a0 = rng.uniform(T0, T1 - Ht)
        b0 = rng.uniform(x[0], x[0] + L - Hx)
        pt, px = _bump(a0, a0 + Ht, p), _bump(b0, b0 + Hx, p)
        mt = (t >= a0) & (t <= a0 + Ht)
        mx = (x >= b0) & (x <= b0 + Hx)
        sc_t, sc_x = (Ht / 2) ** (2 * p), (Hx / 2) ** (2 * p)  # normalise peak to 1

        def phi(a, b):
            ft = np.where(mt, pt.deriv(a)(t) if a else pt(t), 0.0) / sc_t
            fx = np.where(mx, px.deriv(b)(x) if b else px(x), 0.0) / sc_x
            return (wt * ft) @ u @ (wx * fx)

        for j, (a, b) in enumerate(idx):
            G[k, j] = (-1) ** (a + b) * phi(a, b)
        y[k] = (-1) ** m * phi(m, 0)
    return G, y, idx


def realify(Th, y):
    """Complex system -> real stacked system for complex coefficients c = cr + i ci."""
    if not np.iscomplexobj(Th) and not np.iscomplexobj(y):
        return Th, y, False
    A = np.block([[Th.real, -Th.imag], [Th.imag, Th.real]])
    return A, np.r_[y.real, y.imag], True


def unrealify(c, cplx):
    if not cplx:
        return c
    n = len(c) // 2
    return c[:n] + 1j * c[n:]


def bic(rss, n, k, floor):
    return n * np.log(max(rss, floor) / n) + k * np.log(n)


# ------------------------------------------------------------------ symbol and factors
def symbol_coeffs(c, idx, m):
    """Regression coefficients -> {(a, b): coefficient of P}."""
    out = {(m, 0): 1.0}
    for (a, b), v in zip(idx, c):
        if v != 0:
            out[(a, b)] = out.get((a, b), 0) - v
    return out


def to_sympy(coeffs):
    return sp.expand(sum(sp.Float(complex(v).real, 12) * tau**a * xi**b
                         + sp.I * sp.Float(complex(v).imag, 12) * tau**a * xi**b
                         for (a, b), v in coeffs.items() if abs(v) > 0))


def _rat(v, d):
    v = complex(v)
    return sp.Rational(int(round(v.real * 10**d)), 10**d) + sp.I * sp.Rational(int(round(v.imag * 10**d)), 10**d)


def structure_of(fs, tol=1e-2):
    """Sorted ((deg_tau, deg_xi), ...) of the factors, ignoring monomials with |c| < tol
    (the truth has no coefficient below 0.05)."""
    st = []
    for q in fs:
        d = _poly_dict(q)
        mons = [mon for mon, c in d.items() if abs(c) >= tol] or list(d)
        st.append((max(a for a, _ in mons), max(b for _, b in mons)))
    return tuple(sorted(st))


def _poly_dict(q):
    p = sp.Poly(sp.expand(q), tau, xi)
    return {mon: complex(c) for mon, c in zip(p.monoms(), p.coeffs())}


def factor_symbol(coeffs, decimals=2, refine=True):
    """Round P's coefficients to `decimals`, factor over Q(i) with sympy, then refine each factor's
    coefficients (same monomial support) by least squares against the unrounded P.
    Returns (factors as sympy monic in their leading tau power, structure). A hand tolerance:
    there is no data-free threshold (CONV-T5)."""
    Pr = sp.expand(sum(_rat(v, decimals) * tau**a * xi**b for (a, b), v in coeffs.items()))
    if Pr == 0:
        return [], ()
    _, fl = sp.factor_list(Pr, tau, xi, extension=sp.I)
    facs = []
    for q, mult in fl:
        p = sp.Poly(q, tau, xi)
        if p.total_degree() == 0:
            continue
        dt = p.degree(tau)
        lead = p.coeff_monomial(tau**dt) if dt > 0 else p.LC()
        if not lead.is_number:  # leading tau coefficient depends on xi: keep as is, normalise by LC
            lead = p.LC()
        qn = sp.expand(q / lead)
        facs += [qn] * mult
    if refine and facs:
        facs = _refine(facs, coeffs)
    return facs, structure_of(facs)


def _refine(facs, coeffs):
    """Least-squares refinement of factor coefficients so that prod(factors) matches P."""
    dicts = [_poly_dict(q) for q in facs]
    lead = []
    free = []
    for q, d in zip(facs, dicts):
        dt = sp.Poly(q, tau, xi).degree(tau)
        lm = (dt, 0) if (dt, 0) in d and abs(d[(dt, 0)] - 1) < 1e-12 else None
        lead.append(lm)
        free.append([mon for mon in d if mon != lm])
    cplx = any(abs(v.imag) > 0 for d in dicts for v in d.values()) or any(abs(complex(v).imag) > 0 for v in coeffs.values())
    x0 = np.concatenate([[d[mon] for mon in fr] for d, fr in zip(dicts, free)]).astype(complex)
    keys = sorted(set(coeffs) | _prod_keys(dicts))
    target = np.array([complex(coeffs.get(k, 0)) for k in keys])

    def unpack(z):
        out, i = [], 0
        for d, fr, lm in zip(dicts, free, lead):
            dd = {lm: 1.0} if lm is not None else {}
            for mon in fr:
                dd[mon] = z[i]
                i += 1
            out.append(dd)
        return out

    def resid(r):
        z = r[: len(x0)] + (1j * r[len(x0):] if cplx else 0)
        prod = {(0, 0): 1.0}
        for dd in unpack(z):
            prod = _mul(prod, dd)
        v = np.array([prod.get(k, 0) for k in keys]) - target
        return np.r_[v.real, v.imag] if cplx else v.real

    r0 = np.r_[x0.real, x0.imag] if cplx else x0.real
    try:
        sol = least_squares(resid, r0, method="lm" if len(r0) <= 2 * len(keys) else "trf")
        r = sol.x
    except Exception:
        return facs
    z = r[: len(x0)] + (1j * r[len(x0):] if cplx else 0)
    out = []
    for dd in unpack(z):
        out.append(to_sympy(dd))
    return out


def _prod_keys(dicts):
    prod = {(0, 0): 1.0}
    for d in dicts:
        prod = _mul(prod, d)
    return set(prod)


def _mul(p, q):
    out = {}
    for (a1, b1), c1 in p.items():
        for (a2, b2), c2 in q.items():
            k = (a1 + a2, b1 + b2)
            out[k] = out.get(k, 0) + c1 * c2
    return out


def structure_distribution(coeff_list, decimals=2):
    """Frequency of each factor structure over a list of coefficient dicts (ensemble members / samples)."""
    counts = {}
    for c in coeff_list:
        _, st = factor_symbol(c, decimals, refine=False)
        counts[st] = counts.get(st, 0) + 1
    n = sum(counts.values())
    return sorted(((s, k / n) for s, k in counts.items()), key=lambda z: -z[1])
