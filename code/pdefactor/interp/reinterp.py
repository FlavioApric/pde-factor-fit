"""P4: factor-kernel re-interpolation before the final decision (THEORY_TO_ALGO, row proposed with P4).

At a few hundred scattered points and a few % noise the generic GP interpolant (step 1) shrinks the
fast-decaying, high-wavenumber modes towards zero: they are below its smoothness prior, so the core
never sees them and a branch whose modes live at high |kappa| (beam, the diffusion factor of
transport + diffusion) is lost or replaced by a kappa-independent surrogate fitted to the low bins.

Remedy (Ehrenpreis-Palamodov, R2-T6 / T25; EPGP, `epgp.py`): re-interpolate the raw observations with a
GP whose every draw solves the product of the *candidate* factors (the current final factors and the
ones dropped on the way). Its features are exponentials on the candidates' varieties up to the data's
resolution in kappa, so the interpolant extrapolates each bin along a variety instead of shrinking it,
and the modes re-extracted from it carry the data's high-kappa information (the variety is a prior, the
amplitudes and the posterior are the data's). The core then reads factors off these samples.

The re-interpolated field is NOT evidence: a kernel built from the candidates favours them. Any changed
answer is accepted only through the analytic raw-data evidence (refine_raw / bayes_split.raw_evidence via
loop._refine_alternatives) with the existing `_beats` rule (refined evidence - Occam term higher by more
than LOG_BF_BARE, or within it with fewer real parameters). Off by default (env PDEFACTOR_EPGP_REINTERP=1).
"""
from __future__ import annotations

import copy

import numpy as np
import sympy as sp

from ..symbols import tau, xi
from .epgp import fit_epgp

S_REINTERP = 8  # posterior draws handed to the core (as the benchmark's S_LOOP; Monte Carlo size, not a knob)


def kernel_factors(exprs, digits=6):
    """Distinct non-constant factors (sympy in tau, xi), made monic in tau; duplicates (same monic
    coefficients to `digits`) kept once, order of first appearance."""
    out, seen = [], set()
    for q in exprs:
        q = sp.expand(sp.sympify(q))
        if not q.has(tau):
            continue
        lead = sp.Poly(q, tau, xi).coeff_monomial(tau ** sp.degree(q, tau))
        if lead == 0:
            continue
        q = sp.expand(q / lead)
        key = tuple(sorted((mon, round(complex(c).real, digits), round(complex(c).imag, digits))
                           for mon, c in sp.Poly(q, tau, xi).terms()))
        if key not in seen:
            seen.add(key)
            out.append(q)
    return out


def epgp_samples(raw, t, x, factors, S=S_REINTERP, seed=0, family="matern52"):
    """Posterior of the raw observations under the EPGP prior of `factors`, on the grid (t, x).
    Returns dict(samples (S, nt, nx), pis, mean, noise_draws = sqrt(2) (samples - mean), info)
    in the loop's input convention (white sigma 0, correlated error from the draws)."""
    e = fit_epgp(raw["ts"], raw["xs"], raw["ys"], factors, family=family, period_x=raw["period"],
                 t_range=(float(t[0]), float(t[-1])))
    Sm = e.sample(S, t, x, seed=seed)
    if np.isrealobj(raw["ys"]):
        Sm = Sm.real
    mean = Sm.mean(0)
    info = dict(e.info, sigma_hat=e.sigma_hat, ell=e.ell, factors=[str(q) for q in factors])
    return dict(samples=Sm, pis=np.full(S, 1.0 / S), mean=mean, noise_draws=np.sqrt(2) * (Sm - mean[None]),
                info=info)


def reinterp_alternative(factors, dropped, obs, t, x, bounds, refine, kmax, occ, cur, real, S=S_REINTERP):
    """Re-interpolate obs with the candidates' EPGP kernel, rerun the core on its samples and refine every
    structure it proposes on the observations. Returns None (keep the current answer) or
    dict(factors, sup, score, kmax, structure, note, info) when a proposal `_beats` the current factors
    on the raw-data evidence. `cur` is the current refined evidence - Occam term at band `kmax`; if the
    re-interpolated modes reach higher |kappa|, the band is widened and the current factors rescored at it
    first, so both sides are judged on the same data."""
    from .. import loop as L
    from ..core.structfit import extract_modes_ic

    syms = kernel_factors([L._sympy_of(f) for f in list(factors) + list(dropped or [])])
    if not syms:
        return None
    try:
        ep = epgp_samples(obs, t, x, syms, S=S)
    except (np.linalg.LinAlgError, ValueError):
        return None
    samples, pis, nd, u_e = list(ep["samples"]), ep["pis"], ep["noise_draws"], ep["mean"]
    ndh = nd / np.sqrt(2)
    m_e, _, _, _ = extract_modes_ic(u_e, t, x, noise=0.0, noise_draws=ndh)
    kmax_e = max(int(kmax), L._raw_kmax(m_e, obs["period"]))
    if kmax_e > kmax:
        r0 = L.refine_factors(copy.deepcopy(factors), obs, kmax_e)
        cur = r0["logev"] - occ * r0["p"]
    _, agg_e = L._run(samples, pis, t, x, 0.0, bounds, refine, noise_draws=nd)
    if not agg_e.structures_pooled:
        return None
    # the EPGP structure posterior proposes; refined raw evidence with _beats decides (as for any alternative)
    alt = L._refine_alternatives(factors, None, agg_e.structures_pooled, samples, pis, t, x, 0.0, bounds, refine,
                                 nd, obs, kmax_e, occ, cur, u_e)
    info = dict(ep["info"], kmax=kmax_e, cur=cur, pooled={str(k): v for k, v in agg_e.structures_pooled.items()})
    if alt is None:
        return None
    new, st, sc = alt
    sup = L.kappa_support(u_e, t, x, 0.0, [L._sympy_of(f) for f in new], ndh, signed=not real)
    for f in new:
        f.status += "; proposed by the factor-kernel (EPGP) re-interpolation"
    note = (f"factor-kernel re-interpolation (EPGP on {len(syms)} candidate factor(s)) proposed structure {st}, "
            f"kept by the raw-data evidence (refined evidence - Occam {sc:.1f} vs {cur:.1f}, band kmax {kmax_e}). ")
    return dict(factors=new, sup=sup, score=sc, kmax=kmax_e, structure=st, note=note, info=info)
