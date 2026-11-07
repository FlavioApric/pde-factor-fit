"""Structured fit on a cell with the extractor's own uncertainty.

core.structfit.select computes sigma_lam from FFT bins; on a non-periodic cell the points come with a
2-D Fisher sigma_lam and a sigma_kappa instead, so the BIC ranking is redone here with the core's
`fit_structure` / `candidate_structures` (unchanged, black box). The kappa error is mapped onto lam
along the fitted variety: sigma_eff^2 = sigma_lam^2 + |d lam / d kappa|^2 sigma_kappa^2 (two passes,
slope from the first-pass best fit).
"""
from __future__ import annotations

import numpy as np

from ..core.structfit import candidate_structures, fit_structure


def _rank(lam, kappa, sig, m_max, dx_max, real):
    fits = [f for st in candidate_structures(m_max, dx_max)
            if (f := fit_structure(lam, kappa, sig, st, real=real)) is not None]
    if not fits:
        return None, []
    fits.sort(key=lambda f: f.bic)
    b = np.array([f.bic for f in fits])
    p = np.exp(-(b - b.min()) / 2)
    p /= p.sum()
    return fits[0], [(f.structure, f.bic, pi) for f, pi in zip(fits, p)]


def slope(Q, lam, kappa, h=1e-6):
    """d lam / d kappa on {Q(lam, i kappa) = 0}: -Q_kappa / Q_lam."""
    xi_ = 1j * kappa
    dl = (Q(lam + h, xi_) - Q(lam - h, xi_)) / (2 * h)
    dk = (Q(lam, 1j * (kappa + h)) - Q(lam, 1j * (kappa - h))) / (2 * h)
    return -dk / np.where(np.abs(dl) > 1e-12, dl, 1e-12)


def select_cell(ext, m_max=3, dx_max=4, real=False, floor=1e-9):
    """(best Fit, ranked [(structure, bic, p)], sigma_eff) for an Extraction."""
    m = ext.modes
    if len(m) == 0:
        return None, [], np.zeros(0)
    scale = max(np.abs(m.lam).max(), 1.0)
    sig = np.maximum(ext.sig_lam, floor * scale)
    best, ranked = _rank(m.lam, m.kappa, sig, m_max, dx_max, real)
    if best is None or not np.any(ext.sig_kappa > 0):
        return best, ranked, sig
    s = np.array([abs(slope(best.factors[j], m.lam[i], m.kappa[i])) for i, j in enumerate(best.labels)])
    sig2 = np.sqrt(sig**2 + (s * ext.sig_kappa) ** 2)
    best2, ranked2 = _rank(m.lam, m.kappa, sig2, m_max, dx_max, real)
    return (best2, ranked2, sig2) if best2 is not None else (best, ranked, sig)


# ------------------------------------------------------------------ data-level fit on a cell
def point_fits(ext, m_max=3, dx_max=4, real=False, top=8):
    """All point-level structure fits (core fit_structure, extractor sigma), best first."""
    m = ext.modes
    if len(m) < 2:
        return []
    scale = max(np.abs(m.lam).max(), 1.0)
    sig = np.maximum(ext.sig_lam, 1e-9 * scale)
    fits = [f for st in candidate_structures(m_max, dx_max)
            if (f := fit_structure(m.lam, m.kappa, sig, st, real=real)) is not None]
    fits.sort(key=lambda f: f.bic)
    return fits[:top]


def small_structures(m_tot=2, dx_max=2):
    return [st for st in candidate_structures(m_max=m_tot, dx_max=dx_max)]


def _split_seeds(fits, ftol=3e-2):
    """Factors of refined symbols with m >= 2 (numerical absolute factorisation, core.variety.factorise):
    a fitted tau^2 - xi^2 has the kernel of (tau - xi)(tau + xi); the split structure has fewer parameters
    and is scored in its own right."""
    from ..core.variety import factorise

    out = []
    for f in fits:
        for Q in f.factors:
            if Q.m >= 2:
                try:
                    fac, _ = factorise(Q, ftol=ftol)
                except (ValueError, np.linalg.LinAlgError):
                    continue
                if len(fac) > 1:
                    out.append(fac)
    return out


def _structure_of(factors, tol=1e-3):
    st = []
    for Q in factors:
        dx = 0
        for c in Q.coeffs:
            nz = np.where(np.abs(c) > tol * max(1.0, np.abs(c).max()))[0]
            dx = max(dx, int(nz.max()) if len(nz) else 0)
        st.append((Q.m, dx))
    return tuple(sorted(st))


def analyze_cell(u, t, x, noise, extractor="esprit_x", m_max=3, dx_max=4, extra=None, refine=True,
                 n_refine=4, oversample=2, seed_factors=None):
    """Data-level structure selection on one rectangular cell.

    Seeds: (i) point-level fits of the extractor's dispersion points (core fit_structure); (ii) pursuit
    seeds from the data alone: best single factor (1, 2) and (2, 2) from tau / tau^2, then a second
    first-order factor next to the first; (iii) absolute factorisation of every refined m >= 2 symbol.
    Every candidate structure is scored by the data-level BIC of kernelfit (u - P_ker u).
    Returns dict(best, ranked, fits, ext, cell, point_fits)."""
    from ..core.variety import PolySymbol
    from .extract import EXTRACTORS
    from .kernelfit import CellData, kappa_grid, select_data

    z1 = PolySymbol(1, [np.zeros(1, complex)])
    z2 = PolySymbol(2, [np.zeros(1, complex), np.zeros(1, complex)])
    ext = EXTRACTORS[extractor](u, t, x, noise=noise) if extractor else None
    pf = point_fits(ext, m_max, dx_max) if ext is not None else []
    kg = kappa_grid(np.asarray(u), x, t, noise, oversample=oversample)
    cell = CellData(u, t, x, noise, kg=kg)
    pool = list(seed_factors or []) + [Q for f in pf for Q in f.factors] + [z1, z2]
    if seed_factors:  # structures of the seeds (e.g. the parent cell's fit) are candidates too
        extra = list(extra or []) + [tuple(sorted(_structure_of(seed_factors)))]
    # pursuit seeds
    q1 = cell.refine(((1, 2),), [z1])
    q12 = cell.refine(((1, 2), (1, 2)), [q1.factors[0], z1])
    q2 = cell.refine(((2, 2),), [z2])
    pursuit = [q1, q12, q2]
    pool = [Q for f in pursuit for Q in f.factors] + pool
    cands = list(dict.fromkeys([f.structure for f in pf[:6]] + small_structures() + list(extra or [])))
    best, ranked, fits = select_data(cell, cands, pool, refine=refine, n_refine=n_refine)
    fits = list(fits) + pursuit
    # absolute factorisation of the m >= 2 symbols -> split structures, refined
    for fac in _split_seeds(sorted(fits, key=lambda f: f.bic)[:4]):
        stf = tuple(_structure_of([Q])[0] for Q in fac)
        fits.append(cell.refine(stf, fac))
    # greedy degree reduction of the leading fits (BIC decides: a dx slot with ~0 coefficients costs
    # 2 ln N per complex coefficient)
    for f in sorted(fits, key=lambda f: f.bic)[:2]:
        cur = f
        while True:
            trials = []
            for j, (m_, d_) in enumerate(cur.structure):
                if d_ == 0:
                    continue
                st = list(cur.structure)
                st[j] = (m_, d_ - 1)
                trials.append(cell.refine(tuple(st), cur.factors))
            if not trials:
                break
            nb = min(trials, key=lambda g: g.bic)
            fits += trials
            if nb.bic >= cur.bic:
                break
            cur = nb
    # keep the best fit per structure, rank
    byst = {}
    for f in fits:
        if f.structure not in byst or f.bic < byst[f.structure].bic:
            byst[f.structure] = f
    fits = sorted(byst.values(), key=lambda f: f.bic)
    b = np.array([f.bic for f in fits])
    p = np.exp(-(b - b.min()) / 2)
    p /= p.sum()
    ranked = [(f.structure, f.bic, pi) for f, pi in zip(fits, p)]
    return {"best": fits[0], "ranked": ranked, "fits": fits, "ext": ext, "cell": cell, "point_fits": pf}
