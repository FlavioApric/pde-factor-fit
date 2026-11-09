"""Core v2 (plan v2.1): structured factor fit with Bayesian model comparison.

Instead of fitting one P and factoring it with a fixed tolerance (ill-posed on float
coefficients; no data-free threshold, CONV-T5), every candidate factor structure is fitted
directly on the dispersion points (k-varieties alternating regression) and the structures are
compared by BIC (Laplace approximation of the evidence). Residuals are in units of each
point's own uncertainty sigma_lam (Cramer-Rao bound of the exponentials in its FFT bin).

Also here:
- per-bin pencil order chosen by an information criterion (extract_modes_ic);
- a confluent-mode test (A + B t) e^{lam t} per bin: a repeated factor Q^2 has no finite
  test (OPF5B-T6), so when the confluent model wins the output is UNDECIDED with a reason.

Prototype and evidence: analysis/exp/structfit.py, e1b_structfit.py, e4_theory.py.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from itertools import product

import numpy as np
from scipy.optimize import minimize

from . import components as C
from .spectral import Modes, fft_x, matrix_pencil
from .variety import fit_monic


# ------------------------------------------------------------------ modes with order selection
def _bin_rss(y, tt, lam):
    Z = np.exp(np.outer(tt, lam))
    a, *_ = np.linalg.lstsq(Z, y, rcond=None)
    r = y - Z @ a
    return float(np.vdot(r, r).real), a


def extract_modes_ic(u, t, x, noise=0.0, snr_min=3.0, window=None, pad=1, max_order=8, extra=2):
    """Dispersion points like spectral.extract_modes, but in each bin the pencil order is the
    one with the lowest BIC among r0..r0+extra (r0 = Hankel rank above the noise), so that an
    exponential merged into another one (unresolved) gets its own pole when the data support it.
    Returns (Modes, bin_noise, kappa grid, U)."""
    dt = t[1] - t[0]
    tt = t - t[0]
    kappa, U = fft_x(u, x, window=window, pad=pad)
    nx = u.shape[1]
    floor = 1e-9 * np.abs(U).max()
    bin_noise = max(noise / np.sqrt(nx) if noise > 0 else 0.0, floor / snr_min)
    rows = []
    nobs = 2 * len(t)
    for k in range(len(kappa)):
        y = U[:, k]
        level = np.abs(y).max()
        if level == 0 or level < snr_min * bin_noise:
            continue
        tol = max(1e-6, snr_min * bin_noise / level)
        lam0, _, s = matrix_pencil(y, dt, rel_tol=tol, max_order=max_order)
        best = None
        for r in range(max(len(lam0), 1), min(len(lam0) + extra, max_order) + 1):
            lam = lam0 if r == len(lam0) else matrix_pencil(y, dt, order=r)[0]
            rss, a = _bin_rss(y, tt, lam)
            bic = rss / bin_noise**2 + 4 * r * np.log(nobs)
            if best is None or bic < best[0]:
                best = (bic, lam, a)
        _, lam, amp = best
        for lm, a in zip(lam, amp):
            snr = abs(a) / bin_noise
            if abs(a) * np.exp(np.real(lm) * tt[-1] / 2) > snr_min * bin_noise / 3:
                rows.append((kappa[k], lm, a, k, snr))
    if not rows:
        e = np.zeros(0)
        return Modes(e, e.astype(complex), e.astype(complex), e.astype(int), e), bin_noise, kappa, U
    k_, l_, a_, i_, s_ = map(np.array, zip(*rows))
    m = Modes(k_.astype(float), l_.astype(complex), a_.astype(complex), i_.astype(int), s_.astype(float))
    return m, bin_noise, kappa, U


# ------------------------------------------------------------------ uncertainty of each point
def sigma_lambda(modes, t, bin_noise, floor=1e-9):
    """CRB std of lam for each mode: full Fisher of all (A_j, lam_j) sharing the same FFT bin,
    so that interference between exponentials in one bin is accounted for."""
    tt = t - t[0]
    out = np.full(len(modes), np.inf)
    for k in np.unique(modes.kidx):
        idx = np.where(modes.kidx == k)[0]
        cols = []
        for i in idx:
            g = np.exp(modes.lam[i] * tt)
            cols += [g, modes.amp[i] * tt * g]
        J = np.stack(cols, axis=1)
        try:
            Cm = np.linalg.inv(J.conj().T @ J)
        except np.linalg.LinAlgError:
            continue
        for r, i in enumerate(idx):
            out[i] = np.sqrt(max(np.real(Cm[2 * r + 1, 2 * r + 1]), 0)) * bin_noise
    scale = np.abs(modes.lam).max() if len(modes) else 1.0
    return np.maximum(out, floor * max(scale, 1.0))


def _dist(Q, lam, kappa):
    """First-order distance in lam from the point to the variety {Q = 0}: |Q| / |dQ/dtau|."""
    xi_ = 1j * kappa
    v = Q(lam, xi_)
    h = 1e-6 * (1 + np.abs(lam))
    d = (Q(lam + h, xi_) - Q(lam - h, xi_)) / (2 * h)
    return np.abs(v) / np.maximum(np.abs(d), 1e-12)


# ------------------------------------------------------------------ structured fit
@dataclass
class Fit:
    structure: tuple  # ((m_1, dx_1), ..., (m_k, dx_k))
    factors: list
    labels: np.ndarray
    D: np.ndarray  # distances in sigma units, (n_modes, k)
    chi2: float
    scale2: float  # robust noise scale s^2 >= 1
    nparam: int
    bic: float


def _fit_factor(lam, kappa, w, m, dx, real):
    if len(lam) < m * (dx + 1) + 1:
        return None
    P, _, _ = fit_monic(lam, kappa, m, dx, w, real)
    return P


def fit_structure(lam, kappa, sig, structure, real=False, inits=8, iters=30, seed=0, cap=3.0):
    """Alternating k-varieties regression for one structure; best Fit over initialisations."""
    rng = np.random.default_rng(seed)
    n = len(lam)
    k = len(structure)
    w = 1.0 / sig
    best = None
    init_labels = []
    # deterministic inits: sort branches at each kappa by Im lam, then by Re lam
    for key in (np.imag, np.real):
        lab = np.zeros(n, int)
        for kv in np.unique(kappa):
            idx = np.where(kappa == kv)[0]
            order = idx[np.argsort(key(lam[idx]))]
            for r, i in enumerate(order):
                lab[i] = min(r, k - 1)
        init_labels.append(lab)
    init_labels += [rng.integers(0, k, n) for _ in range(inits)]
    for lab in init_labels:
        lab = lab.copy()
        facs = None
        for _ in range(iters):
            new = []
            for j, (m, dx) in enumerate(structure):
                sel = lab == j
                Q = _fit_factor(lam[sel], kappa[sel], w[sel], m, dx, real)
                if Q is None:
                    break
                new.append(Q)
            if len(new) < k:
                break
            facs = new
            D = np.stack([_dist(Q, lam, kappa) for Q in facs], axis=1) / sig[:, None]
            nl = D.argmin(1)
            if np.array_equal(nl, lab):
                break
            lab = nl
        if facs is None or len(facs) < k:
            continue
        D = np.stack([_dist(Q, lam, kappa) for Q in facs], axis=1) / sig[:, None]
        # robust: a uniform background class caps each point at z^2 = (cap s)^2, with s >= 1 a
        # robust scale of the residuals (median of chi^2_1 is 0.455)
        z2 = D.min(1) ** 2
        s2 = max(1.0, float(np.median(z2)) / 0.455)
        chi2 = float(np.minimum(z2, cap**2 * s2).sum())
        npar = sum(m * (dx + 1) for m, dx in structure) * (1 if real else 2)
        nn = 2 * n
        # noise scale s >= 1 (cannot beat the CRB), Jeffreys on s: n log(max(chi2/n, 1))
        bic = nn * np.log(max(chi2 / nn, 1.0)) + npar * np.log(nn)
        if best is None or bic < best.bic:
            best = Fit(tuple(structure), facs, D.argmin(1), D, chi2, s2, npar, bic)
    return best


def candidate_structures(m_max=3, dx_max=4, deg_options=(1, 2)):
    out = []
    for k in range(1, m_max + 1):
        for degs in product(deg_options, repeat=k):
            if sum(degs) > m_max or list(degs) != sorted(degs):
                continue
            for dxs in product(range(dx_max + 1), repeat=k):
                st = tuple(zip(degs, dxs))
                if list(st) != sorted(st):  # canonical order, no duplicates
                    continue
                out.append(st)
    return out


def select(modes, t, bin_noise, m_max=3, dx_max=4, real=False):
    """All structures, BIC-ranked: (best Fit, [(structure, bic, posterior weight)], sigma_lam)."""
    sig = sigma_lambda(modes, t, bin_noise)
    fits = []
    for st in candidate_structures(m_max, dx_max):
        f = fit_structure(modes.lam, modes.kappa, sig, st, real=real)
        if f is not None:
            fits.append(f)
    if not fits:
        return None, [], sig
    fits.sort(key=lambda f: f.bic)
    b = np.array([f.bic for f in fits])
    p = np.exp(-(b - b.min()) / 2)
    p /= p.sum()
    return fits[0], [(f.structure, f.bic, pi) for f, pi in zip(fits, p)], sig


# ------------------------------------------------------------------ repeated roots
def confluent_test(modes, t, U, bin_noise, sep=4.0):
    """For each bin with two close poles (|d lam| < sep / T), compare by BIC the simple model
    (two exponentials, poles refined) with the confluent one (A + B t) e^{lam t} (one pole fewer).
    Returns a list of (kappa, lam, delta_bic) for the bins where the confluent model wins."""
    tt = t - t[0]
    T = tt[-1]
    nobs = 2 * len(t)
    out = []
    for k in np.unique(modes.kidx):
        idx = np.where(modes.kidx == k)[0]
        if len(idx) < 2:
            continue
        lam = modes.lam[idx]
        d = np.abs(lam[:, None] - lam[None, :]) + np.eye(len(lam)) * 1e300
        i, j = np.unravel_index(np.argmin(d), d.shape)
        if d[i, j] > sep / T:
            continue
        y = U[:, k]
        others = np.delete(lam, [i, j])

        def rss_simple(v):
            return _bin_rss(y, tt, np.r_[others, v[0] + 1j * v[1], v[2] + 1j * v[3]])[0]

        def rss_conf(v):
            lc = v[0] + 1j * v[1]
            Z = np.concatenate([np.exp(np.outer(tt, others)), np.exp(lc * tt)[:, None], (tt * np.exp(lc * tt))[:, None]], 1)
            a, *_ = np.linalg.lstsq(Z, y, rcond=None)
            r = y - Z @ a
            return float(np.vdot(r, r).real)

        li, lj = lam[i], lam[j]
        rs = minimize(rss_simple, [li.real, li.imag, lj.real, lj.imag], method="Nelder-Mead",
                      options={"xatol": 1e-10, "fatol": 1e-30, "maxiter": 4000}).fun
        rs = min(rs, rss_simple([li.real, li.imag, lj.real, lj.imag]))
        lc = (li + lj) / 2
        rc = minimize(rss_conf, [lc.real, lc.imag], method="Nelder-Mead",
                      options={"xatol": 1e-10, "fatol": 1e-30, "maxiter": 2000}).fun
        # simple: 2 amplitudes + 2 poles = 8 real parameters; confluent: 2 amplitudes + 1 pole = 6
        dbic = (rc - rs) / bin_noise**2 - 2 * np.log(nobs)
        if dbic < 0:
            out.append((float(modes.kappa[idx[0]]), complex(lc), float(dbic)))
    return out


# ------------------------------------------------------------------ entry point
@dataclass
class StructResult:
    label: str
    factors: list = field(default_factory=list)  # FactorResult (same type as core v1)
    structures: list = field(default_factory=list)  # [(structure, bic, posterior weight)], best first
    gamma: float = 1.0
    cF: float = 0.0
    n_shared: int = 0
    n_modes: int = 0
    scale2: float = 1.0
    confluent: list = field(default_factory=list)
    info: dict = field(default_factory=dict)
    components: list = field(default_factory=list)

    def summary(self):
        top = self.structures[0] if self.structures else None
        lines = [f"label={self.label} modes={self.n_modes} best={top[0] if top else None} "
                 f"p={top[2] if top else 0:.3f} s^2={self.scale2:.3g}",
                 f"gamma_N={self.gamma:.4g} c_F={self.cF:.4g} shared={self.n_shared} confluent={len(self.confluent)}"]
        for f in self.factors:
            lines.append(f"  w={f.weight:.4f} Q={f.sympy} terms={f.terms} nk={f.n_kappa} id={f.identifiable}")
        if self.info.get("reason"):
            lines.append(f"  reason: {self.info['reason']}")
        return "\n".join(lines)


def analyze_structured(u, t, x, noise=0.0, *, m_max=3, dx_max=4, snr_min=3.0, window=None,
                       real=False, share_z=3.0, outlier_frac_misfit=0.5, want_components=False):
    """Core v2: modes (order by BIC) -> structured fit with posterior over structures ->
    confluent test -> components, weights, gamma_N. Labels as in core v1 (sec. 0.5), plus
    UNDECIDED when a confluent mode wins (repeated factor, OPF5B-T6)."""
    from .analyze import FactorResult  # local import: analyze imports this module's siblings

    modes, bin_noise, _, U = extract_modes_ic(u, t, x, noise=noise, snr_min=snr_min, window=window)
    if len(modes) == 0:
        return StructResult("UNDECIDED", info={"reason": "no modes above noise"})
    best, ranked, sig = select(modes, t, bin_noise, m_max=m_max, dx_max=dx_max, real=real)
    if best is None:
        return StructResult("UNDECIDED", n_modes=len(modes), info={"reason": "too few modes for any structure"})
    facs = best.factors
    D = best.D
    shared = (D < share_z).sum(1) > 1
    fields = C.component_fields(modes, best.labels, np.where(D < share_z, 0.0, 1.0), len(facs), t, x, share_tol=0.5)
    wts = C.weights(fields)
    g, cF, n0 = C.gamma_N(facs, np.unique(modes.kappa), t, x) if len(facs) > 1 else (1.0, 0.0, 0)
    tol = 1e-8 if noise == 0 else 1e-3
    out, all_ok = [], True
    for j, Q in enumerate(facs):
        sel = best.labels == j
        nk = len(np.unique(modes.kappa[sel]))
        dx = max(len(c) - 1 for c in Q.coeffs)
        ok = sel.sum() >= Q.m * (dx + 1) + 1 and nk >= dx + 1
        all_ok &= ok
        out.append(FactorResult(Q, Q.to_sympy(tol=tol), float(wts[j]), Q.evolution_terms(tol=tol), nk, ok))
    conf = confluent_test(modes, t, U, bin_noise)
    z2 = D.min(1) ** 2
    frac_out = float((z2 >= 9.0 * best.scale2).mean())
    info = {"outlier_fraction": frac_out, "bin_noise": bin_noise}
    if conf:
        label = "UNDECIDED"
        info["reason"] = (f"confluent (A + B t) e^(lam t) modes in {len(conf)} bins: a repeated factor is "
                          "possible and has no finite test (OPF5B-T6)")
    elif frac_out > outlier_frac_misfit:
        label = "MISFIT"
        info["reason"] = f"{frac_out:.0%} of the modes are outliers for every structure"
    else:
        label = "FIT-COMPATIBLE" if all_ok else "ID-KER"
    res = StructResult(label, out, ranked, g, cF, int(shared.sum()), len(modes), best.scale2, conf, info)
    if want_components:
        res.components = fields
    return res
