"""Single entry point of the deterministic analytic core: analyze(u, t, x) -> CoreResult.

The core never claims identification from numerical data (DICT-A-iii). Labels follow
ALGORITMO_ESTESO sec. 0.5: FIT-COMPATIBLE, MISFIT, ID-KER (relative to the declared class), UNDECIDED.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from . import components as C
from .spectral import extract_modes
from .variety import assign, factorise, refine, select_symbol


@dataclass
class FactorResult:
    symbol: object  # PolySymbol
    sympy: object
    weight: float
    terms: dict | None  # {n: c_n}, a(xi) = sum c_n xi^n, for evolution factors
    n_kappa: int  # distinct wavenumbers carrying its modes
    identifiable: bool  # enough distinct modes for its coefficient count (R4-T4)
    eint: float = 0.0
    rho: float = 0.0


@dataclass
class CoreResult:
    label: str
    P: object = None
    factors: list = field(default_factory=list)
    gamma: float = 1.0
    cF: float = 0.0
    n_shared: int = 0
    level: tuple = None
    residual: float = None
    n_modes: int = 0
    info: dict = field(default_factory=dict)
    components: list = field(default_factory=list)

    def summary(self):
        lines = [f"label={self.label} level={self.level} residual={self.residual} modes={self.n_modes}"]
        lines.append(f"gamma_N={self.gamma:.4g} c_F={self.cF:.4g} shared={self.n_shared}")
        for f in self.factors:
            lines.append(f"  w={f.weight:.4f} Q={f.sympy} terms={f.terms} nk={f.n_kappa} id={f.identifiable} rho={f.rho:.3g}")
        return "\n".join(lines)


def analyze(u, t, x, noise=0.0, *, m_max=4, dx_max=4, fit_tol=None, factor_tol=None,
            snr_min=3.0, kmax=None, window=None, real=None, share_tol=1e-6,
            want_components=False, max_order=8):
    """Analyse gridded data u[t, x] (uniform grid, x periodic or windowed)."""
    real = np.isrealobj(u) if real is None else real
    fit_tol = fit_tol if fit_tol is not None else (1e-7 if noise == 0 else 3e-2)
    factor_tol = factor_tol if factor_tol is not None else (1e-6 if noise == 0 else 5e-2)
    modes = extract_modes(u, t, x, noise=noise, kmax=kmax, snr_min=snr_min, window=window,
                          max_order=max_order)
    if len(modes) == 0:
        return CoreResult("UNDECIDED", info={"reason": "no modes above noise"})
    w = None
    if noise > 0:
        w = np.sqrt(np.minimum(modes.snr, 1e6))
    P, info = select_symbol(modes, m_max=m_max, dx_max=dx_max, tol=fit_tol, real=real, weights=w)
    if P is None:
        return CoreResult("MISFIT", n_modes=len(modes), info=info)
    facs, fres = factorise(P, ftol=factor_tol)
    labels, scores = assign(modes, facs)
    if len(facs) > 1:
        facs = refine(modes, facs, labels, weights=w)
        labels, scores = assign(modes, facs)
    fields = C.component_fields(modes, labels, scores, len(facs), t, x, share_tol=share_tol)
    wts = C.weights(fields)
    band = np.unique(np.abs(modes.kappa))
    band_signed = np.unique(modes.kappa)
    g, cF, n0 = C.gamma_N(facs, band_signed, t, x)
    out = []
    all_ok = True
    for j, Q in enumerate(facs):
        mj = modes.subset(labels == j)
        nk = len(np.unique(mj.kappa))
        dx = max(len(c) - 1 for c in Q.coeffs)
        ok = len(mj) >= Q.m * (dx + 1) + 1 and nk >= dx + 1
        all_ok &= ok
        terms = Q.evolution_terms(tol=1e-8 if noise == 0 else 1e-3)
        e, rho = C.eint_ratio(terms, mj, t[-1] - t[0]) if terms else (0.0, 0.0)
        out.append(FactorResult(Q, Q.to_sympy(tol=1e-8 if noise == 0 else 1e-3), float(wts[j]), terms, nk, ok, e, rho))
    label = "FIT-COMPATIBLE" if all_ok else "ID-KER"
    res = CoreResult(label, P.to_sympy(), out, g, cF, n0, (info["m"], info["dx"]), info["residual"],
                     len(modes), {"factor_residuals": fres, "band": band})
    if want_components:
        res.components = fields
    return res
