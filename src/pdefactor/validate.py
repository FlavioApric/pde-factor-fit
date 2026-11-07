"""V0: deterministic diagnostic battery on a finished LoopResult (PHASE4_ML_PLAN.md, V0).

Read-only on the result: it never changes a label or a factor (rule 5); it reports statistics with a
known null and flags. The controller (or the user) acts on the flags; the learned combiner V1
(pdefactor.learned.validator) reads `V0Report.features()`.

Implemented here (the ones with an analytic or already-computed null):
  V0.1  posterior-predictive misfit per kappa bin: the data's time series in each Fourier bin is
        projected on the exponentials e^{lam_j(kappa) t} that the final factors predict there (all
        roots of every factor). Under the fitted law and white noise sigma the whitened residual is
        chi^2 with 2 (nt - r) degrees of freedom (r fitted complex amplitudes; nt - r for the real
        kappa = 0 bin). Bins far above it carry modes no factor explains: a missing factor, a
        high-kappa loss, a wrong coefficient, or an out-of-class law. Omnibus: the sum over bins.
        The null is exact for white noise on a grid with fixed factors; the factors were fitted on
        the same data (a few df per factor, negligible against nt per bin). For GP samples (coloured
        error) pass the raw grid if available; otherwise the p-values are indicative only.
  V0.2  mode-count margin per factor: distinct |kappa| support - (dx + 1)  (T13, T40)
  V0.3  evidence gap between the chosen structure and the next one, and the structure entropy (T39)
  V0.10 split floor: c_F, gamma_N, and the 90 % weight interval width relative to the weight (T5/T6)
  V0.13 held-out-in-time score of the final structure (optional, costs one core fit; T15)
Not yet: V0.4-V0.9, V0.11-V0.12 (need the re-simulation hook and the sample tracks).
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import sympy as sp
from scipy.stats import chi2

from .core.spectral import fft_x
from .synthetic import branch_roots
from .symbols import tau, xi

P_BIN = 1e-3  # family-wise level for flagging a bin (Bonferroni over the bins)
P_OMNIBUS = 1e-3
LOG_BF_AMBIGUOUS = np.log(3.0)  # Kass-Raftery: a gap below log 3 is "not worth more than a mention"


@dataclass
class V0Report:
    stats: dict = field(default_factory=dict)
    flags: list = field(default_factory=list)  # (code, text)

    def features(self):
        """Flat float features for V1 (no identifiers)."""
        s = self.stats
        out = {}
        for k in ("v01_omnibus_logp", "v01_omnibus_z", "v01_n_bad_bins", "v01_max_bad_kappa", "v01_worst_logp",
                  "v02_min_margin", "v03_gap", "v03_entropy", "v10_cF", "v10_gamma", "v10_w_rel",
                  "v13_heldout"):
            v = s.get(k)
            out[k] = float(v) if v is not None and np.isfinite(v) else np.nan
        return out

    def summary(self):
        lines = [f"{c}: {t}" for c, t in self.flags] or ["no flag"]
        return "\n".join(lines)


def _log10sf(stat, df):
    """log10 of the chi^2 survival function, floored at -300 (underflow for a gross misfit)."""
    v = chi2.logsf(stat, df) / np.log(10)
    return float(max(v, -300.0)) if np.isfinite(v) or v < 0 else 0.0


def predictive_bins(factors, u, t, x, sigma, kmax=None):
    """V0.1 per bin: list of (kappa, chi2 stat, df, log10 p). factors: sympy, monic in tau."""
    kappa, U = fft_x(u, x)
    nx, nt = u.shape[1], len(t)
    tt = t - t[0]
    real = bool(np.isrealobj(u))
    var = sigma**2 / nx  # variance of U per bin and time (complex: sigma^2 / (2 nx) per part)
    out = []
    for j in np.argsort(np.abs(kappa)):
        k = kappa[j]
        if real and k < 0:
            continue  # mirror of +kappa
        if kmax is not None and abs(k) > kmax:
            continue
        lams = np.concatenate([branch_roots(q, k) for q in factors]) if factors else np.zeros(0, complex)
        lams = lams[np.isfinite(lams)]
        y = U[:, j]
        # each column scaled by its own maximum modulus (same span, same residual): a growing mode
        # would overflow exp(lambda t) to inf and break the least-squares SVD
        E = np.outer(tt, lams)
        Z = np.exp(E - E.real.max(0, initial=-np.inf)) if E.size else np.exp(E)
        if real and k == 0:
            Z = np.concatenate([Z.real, Z.imag], 1) if Z.size else Z
            y = y.real
        if Z.size:
            a, *_ = np.linalg.lstsq(Z, y, rcond=None)
            r = y - Z @ a
            rank = np.linalg.matrix_rank(Z)
        else:
            r, rank = y, 0
        if real and k == 0:
            stat, df = float(np.sum(r**2) / var), max(nt - rank, 1)
        else:
            stat, df = float(2 * np.vdot(r, r).real / var), max(2 * (nt - rank), 1)
        out.append((float(k), stat, df, _log10sf(stat, df)))
    return out


def validate(res, u, t, x, sigma, heldout=False, bounds=None):
    """V0 battery for a LoopResult `res` on the data grid u (the noisy grid, or the GP mean with
    its noise level) with white noise std sigma."""
    rep = V0Report()
    s = rep.stats
    facs = [f.sympy for f in res.factors]

    # V0.1
    if sigma and sigma > 0:
        bins = predictive_bins(facs, u, t, x, sigma)
        tot = sum(b[1] for b in bins)
        df = sum(b[2] for b in bins)
        s["v01_bins"] = bins
        s["v01_omnibus_logp"] = _log10sf(tot, df)
        s["v01_omnibus_z"] = float((tot - df) / np.sqrt(2 * df))
        s["v01_chi2_per_df"] = tot / df
        lvl = np.log10(P_BIN / max(len(bins), 1))
        bad = [b for b in bins if b[3] < lvl]
        s["v01_n_bad_bins"] = len(bad)
        s["v01_max_bad_kappa"] = max((abs(b[0]) for b in bad), default=0.0)
        s["v01_worst_logp"] = min((b[3] for b in bins), default=0.0)
        if s["v01_omnibus_logp"] < np.log10(P_OMNIBUS) and bad:
            ks = ", ".join(f"{abs(b[0]):.3g}" for b in sorted(bad, key=lambda b: b[3])[:6])
            rep.flags.append(("V0.1", f"data not explained by the factors at kappa = {ks} "
                                      f"(chi2/df = {s['v01_chi2_per_df']:.3g}, omnibus p = 1e{s['v01_omnibus_logp']:.1f}): "
                                      "a missing factor, high-kappa loss, wrong coefficients or an out-of-class law"))

    # V0.2
    margins = []
    for f in res.factors:
        dx = max(b for _, b in f.coef)
        sup = len(set(np.round(np.abs(f.kappa_support), 9))) if f.kappa_support else 0
        margins.append(sup - (dx + 1))
    s["v02_margins"] = margins
    s["v02_min_margin"] = min(margins) if margins else np.nan
    for f, mg in zip(res.factors, margins):
        if mg < 0:
            rep.flags.append(("V0.2", f"{f.sympy}: {mg + max(b for _, b in f.coef) + 1} distinct |kappa| for "
                                      f"{max(b for _, b in f.coef) + 1} needed (identifiability, T40)"))

    # V0.3
    ev = res.evidence or {}
    if len(ev) >= 2:
        v = np.sort(np.array(list(ev.values()), float))[::-1]
        s["v03_gap"] = float(v[0] - v[1])
        if s["v03_gap"] < LOG_BF_AMBIGUOUS:
            rep.flags.append(("V0.3", f"the next structure is within log BF {s['v03_gap']:.2g} of the chosen one"))
    st = np.array(list((res.structures or {}).values()), float)
    if st.size and st.sum() > 0:
        st = st / st.sum()
        s["v03_entropy"] = float(-(st[st > 0] * np.log(st[st > 0])).sum())

    # V0.10
    sp_ = res.split or {}
    if sp_:
        s["v10_cF"] = float(sp_.get("cF", np.nan))
        s["v10_gamma"] = float(sp_.get("gamma", np.nan))
        wq = np.asarray(sp_.get("w_q", []), float)
        wm = np.abs(np.asarray(sp_.get("w_mean", []), float))
        if wq.size and wm.size:
            s["v10_w_rel"] = float(np.max((wq[:, 2] - wq[:, 0]) / np.maximum(wm, 1e-12)))
            if s["v10_w_rel"] > 0.5:
                rep.flags.append(("V0.10", f"weights not separable at this noise (90 % width {s['v10_w_rel']:.2g} "
                                           f"of the weight; c_F = {s['v10_cF']:.3g})"))

    # V0.13
    if heldout and facs:
        from .loop import heldout_score

        st_final = tuple(sorted((sp.Poly(q, tau).degree(), max(b for _, b in f.coef)) for q, f in zip(facs, res.factors)))
        h = heldout_score(u, t, x, sigma, bounds or res.bounds, structures=[st_final])
        s["v13_heldout"] = h[0]
    return rep
