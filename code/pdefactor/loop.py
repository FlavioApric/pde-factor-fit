"""Outer loop (plan Phase 3, as changed by v2.9): grouping by factors only.

Per level the core (core v2, black box) runs on every posterior interpolant sample and the
results are pooled into the factor distribution W (aggregate). Then:
1. degree growth: when most posterior mass is MISFIT or ID-KER, the degree bounds (m, dx) are
   raised one step. A grown level is kept only if it (a) moves posterior mass to FIT-COMPATIBLE
   and (b) predicts held-out data better: factors fitted on the first part of the time window
   must explain the modes extracted from the rest (guard against fake higher-degree fits);
2. regroup at fixed k: when the posterior on the number of factors k is concentrated but the
   samples disagree on the structure, every sample is refitted with the consensus structure;
3. recursion per factor group: each factor's component field is analysed again on its own; a
   factor whose component still splits is replaced by its children.
The domain is never split here: where each factor carries its energy is an optional report.
Labels follow the output contract; no output claims a law is identified.
"""
from __future__ import annotations

import copy
import os
from dataclasses import dataclass, field

import numpy as np
import sympy as sp

from .aggregate import aggregate, build_cloud, run_core
from .core.structfit import _dist, analyze_structured, extract_modes_ic, sigma_lambda
from .symbols import tau, xi

START_BOUNDS = (3, 4)  # (total tau-degree, dx per factor) of core v2's default class
DX_LIMIT, M_LIMIT = 8, 4
P_CONCENTRATED = 0.9  # plan v2.5: posterior mass needed to call k or a structure settled
CAP = 3.0  # robust residual cap in sigma units, as in the core


# ------------------------------------------------------------------ results
@dataclass
class Level:
    bounds: tuple
    p_fit: float  # pooled posterior mass on FIT-COMPATIBLE
    heldout: tuple | None = None  # (mean, standard error) of capped z^2 of held-out modes, lower is better
    accepted: bool = True
    note: str = ""


@dataclass
class FactorReport:
    sympy: sp.Expr
    W: float  # mass of the factor's track in W
    coef: dict  # monomial (a, b) of tau^a xi^b -> (posterior median, q05, q95), complex
    status: str = "not checked"  # recursion outcome
    children: list = field(default_factory=list)
    kappa_support: list = field(default_factory=list)  # distinct |kappa| of its modes (identifiability)


@dataclass
class LoopResult:
    label: str
    factors: list
    p_k: dict
    structures: dict  # pooled structure posterior
    history: list
    regrouped: bool
    bounds: tuple
    labels: dict  # pooled core labels
    agg: object = None
    domain: dict | None = None
    note: str = ""
    split: dict | None = None  # Friedrichs-angle layer on the final factors (bayes_split), pooled
    evidence: dict | None = None  # data-level log evidence of the candidate structures (decider)
    dropped: list = field(default_factory=list)  # factors removed as redundant by the split evidence

    def pruned(self, digits=None):
        """The factors with every term whose 90 % interval (real and imaginary part) contains 0 left
        out, since the posterior does not distinguish it from 0. The leading tau^m term is kept."""
        out = []
        for f in self.factors:
            m = max(a for a, _ in f.coef)
            q = 0
            for (a, b), (mean, lo, hi) in f.coef.items():
                zero = lo.real <= 0 <= hi.real and lo.imag <= 0 <= hi.imag
                if zero and (a, b) != (m, 0):
                    continue
                c = mean if digits is None else complex(round(mean.real, digits), round(mean.imag, digits))
                c = c.real if abs(c.imag) <= 1e-12 * max(1.0, abs(c)) else c
                if digits is not None and not isinstance(c, float):
                    c = sp.Float(c.real, digits) + sp.I * sp.Float(c.imag, digits)
                q += c * tau**a * xi**b
            out.append(sp.expand(q))
        return out

    def equation(self, digits=4):
        """Product of the pruned factors (see pruned)."""
        if not self.factors:
            return "no factors"
        return " * ".join(f"({q})" for q in self.pruned(digits)) + " u = 0"

    def summary(self):
        top = next(iter(self.structures.items()), (None, 0.0))
        lines = [f"label={self.label}  equation: {self.equation()}",
                 f"P(k)={ {k: round(v, 3) for k, v in self.p_k.items()} }  top structure {top[0]} p={top[1]:.3f}",
                 f"bounds={self.bounds} regrouped={self.regrouped} labels={ {k: round(v, 3) for k, v in self.labels.items()} }"]
        for f in self.factors:
            lines.append(f"  W={f.W:.3f}  {f.sympy}   [{f.status}]")
        if self.split:
            sq = self.split
            lines.append(f"  split layer: P(split)={sq['p_split']:.3f} c_F={sq['cF']:.3g} weights "
                         + ", ".join(f"{m:.4f} [{lo:.4f}, {hi:.4f}]" for m, (lo, _, hi) in zip(sq['w_mean'], sq['w_q'])))
        for h in self.history:
            lines.append(f"  level {h.bounds}: p_fit={h.p_fit:.3f} heldout={h.heldout} accepted={h.accepted} {h.note}")
        if self.note:
            lines.append(f"  note: {self.note}")
        return "\n".join(lines)


# ------------------------------------------------------------------ helpers
def _run(samples, pis, t, x, sigma, bounds, refine, structures=None, noise_draws=None, **kw):
    res = run_core(samples, t, x, sigma, pis, m_max=bounds[0], dx_max=bounds[1], refine=refine,
                   structures=structures, noise_draws=noise_draws, **kw)
    return res, aggregate(res)


PRED_LOGP = -3.0  # V0.1 omnibus level (log10 p) that triggers degree growth (G7); a test level, not a fit knob


def _attach(res, samples):
    for (r, _), u in zip(res, samples):
        r.info["u"] = u


def _pred_logp(res, t, x, sigma, noise_draws):
    """V0.1 omnibus log10 p of the weightiest sample's own factors on that sample (white noise only;
    0 = no test). A fit whose factors leave significant structure in the data needs a larger class
    even when the core labels it FIT-COMPATIBLE or UNDECIDED (plan v2.13 G7)."""
    if not sigma or sigma <= 0 or noise_draws is not None or not res:
        return 0.0
    from .validate import _log10sf, predictive_bins

    r, _ = max(res, key=lambda rp: rp[1])
    u = r.info.get("u")
    if u is None or not r.factors:
        return 0.0
    b = predictive_bins([f.sympy for f in r.factors], u, t, x, sigma)
    return _log10sf(sum(v[1] for v in b), sum(v[2] for v in b))


def _p(agg, labels):
    return float(sum(agg.labels.get(lab, 0.0) for lab in labels))


def _p_k(agg):
    return dict(agg.dp.p_k) if agg.dp is not None else dict(agg.k_structure)


def _mean_sample(samples, pis):
    w = np.asarray(pis, float) / np.sum(pis)
    return sum(wi * s for wi, s in zip(w, samples))


def heldout_score(u, t, x, sigma, bounds, refine=False, frac=2 / 3, noise_draws=None, structures=None):
    """Fit the factors on t[:i] and score the modes extracted from t[i:] against them: mean of the
    capped z^2 = (distance / sigma_lam)^2. A fit that only matches the noise of the training
    window predicts the held-out modes worse than the simpler fit. Returns (mean, standard error).
    noise_draws (R, nt, nx) are split in time with the data."""
    i = int(frac * len(t))
    real = bool(np.isrealobj(u))
    nd = (None, None) if noise_draws is None else (noise_draws[:, :i], noise_draws[:, i:])
    r = analyze_structured(u[:i], t[:i], x, noise=sigma, m_max=bounds[0], dx_max=bounds[1], real=real,
                           refine=refine, noise_draws=nd[0], structures=structures)
    if not r.factors:
        return np.inf, 0.0
    modes, bn, _, _ = extract_modes_ic(u[i:], t[i:], x, noise=sigma, refine=refine, noise_draws=nd[1])
    if len(modes) == 0:
        return np.inf, 0.0
    sig = sigma_lambda(modes, t[i:], bn)
    D = np.stack([_dist(f.symbol, modes.lam, modes.kappa) for f in r.factors], axis=1) / sig[:, None]
    z2 = np.minimum(D.min(1) ** 2, CAP**2)
    return float(z2.mean()), float(z2.std(ddof=1) / np.sqrt(len(z2))) if len(z2) > 1 else 0.0


def _nonreal_c(c):
    """A coefficient (median, q05, q95) is non-real when its imaginary part is not negligible relative
    to its size and, where the interval is not degenerate, the interval of the imaginary part excludes 0
    (scale-free; v2.13 G6)."""
    med, lo, hi = c
    if abs(med.imag) <= 1e-9 * max(1.0, abs(med)):
        return False
    a, b = sorted((lo.imag, hi.imag))
    return not (a < b and a <= 0 <= b)


def _nonreal(f):
    return any(_nonreal_c(c) for c in f.coef.values())


def _distinct(a, b):
    """Two factor reports are told apart when some coefficient has disjoint 90 % intervals (real or
    imaginary part; a missing monomial has interval [0, 0])."""
    z = (0j, 0j, 0j)
    for mon in set(a.coef) | set(b.coef):
        _, la, ha = a.coef.get(mon, z)
        _, lb, hb = b.coef.get(mon, z)
        if ha.real < lb.real or hb.real < la.real or ha.imag < lb.imag or hb.imag < la.imag:
            return True
    return False


def _conj_pair(a, b):
    """b is the complex conjugate of a: no coefficient of conj(a) told apart from b's (90 % intervals),
    or equal means when the intervals are degenerate (one sample)."""
    z = (0j, 0j, 0j)
    ca = FactorReport(a.sympy, a.W, {k: tuple(np.conj(v) for v in c) for k, c in a.coef.items()})
    ca.coef = {k: (c[0], complex(c[1].real, min(c[1].imag, c[2].imag)), complex(c[2].real, max(c[1].imag, c[2].imag)))
               for k, c in ca.coef.items()}
    if not _distinct(ca, b):
        return True
    keys = set(a.coef) | set(b.coef)
    scale = 1 + max(abs(c[0]) for c in list(a.coef.values()) + list(b.coef.values()))
    return max(abs(np.conj(a.coef.get(k, z)[0]) - b.coef.get(k, z)[0]) for k in keys) < 1e-6 * scale


def _sympy_of(f):
    """Pruned sympy expression of one FactorReport (terms whose 90 % interval contains 0 dropped)."""
    m = max(a for a, _ in f.coef)
    q = 0
    for (a, b), (mean, lo, hi) in f.coef.items():
        if (a, b) != (m, 0) and lo.real <= 0 <= hi.real and lo.imag <= 0 <= hi.imag:
            continue
        q += (mean.real if abs(mean.imag) <= 1e-12 * max(1.0, abs(mean)) else mean) * tau**a * xi**b
    return sp.expand(q)


def _poly_symbol(q):
    """PolySymbol (monic in tau) of a pruned sympy factor."""
    from .core.variety import PolySymbol

    c = _coef_dict(q)
    m = max(a for a, _ in c)
    lead = c[(m, 0)]
    coeffs = []
    for k in range(m):
        dx = max([b for a, b in c if a == k], default=0)
        coeffs.append(np.array([c.get((k, b), 0.0) / lead for b in range(dx + 1)], complex))
    return PolySymbol(m, coeffs)


def kappa_support(u, t, x, sigma, factors, noise_draws=None, z=3.0, weights=None, signed=False, counts=False):
    """With weights given, also returns the indices of redundant factors: dropped one at a time
    (smallest weight first) while every mode the factor explains lies within z sigma_lam of the
    variety of another remaining factor (one factor fitted twice; mode-level test, no threshold
    beyond the CRB z-score already used for assignment).
    counts=True (no weights): per factor, {kappa: number of its observed modes there}.
    Distinct |kappa| at which each final factor has a mode of u within z sigma_lam (modes of real
    fields at -kappa mirror +kappa and carry no new information). A factor seen at one |kappa| only is
    determined there and nowhere else: every symbol through those modes fits (0b.6, ATTACK-9 sec. 3B)."""
    modes, bn, _, _ = extract_modes_ic(u, t, x, noise=sigma, noise_draws=noise_draws)
    if len(modes) == 0 or not factors:
        sup = [[] for _ in factors]
        return sup if weights is None else (sup, [])
    sig = sigma_lambda(modes, t, bn)
    syms = [_poly_symbol(q) for q in factors]
    D = np.stack([_dist(Q, modes.lam, modes.kappa) for Q in syms], axis=1) / sig[:, None]
    alive = list(range(len(syms)))
    dropped = []
    if weights is not None:
        changed = True
        while changed and len(alive) > 1:
            changed = False
            for j in sorted(alive, key=lambda i: weights[i]):
                rest = [i for i in alive if i != j]
                Da = D[:, alive]
                mine = (np.array(alive)[Da.argmin(1)] == j) & (Da.min(1) < z)
                if not mine.any() or np.all(D[np.ix_(mine, rest)].min(1) < z):
                    alive.remove(j)
                    dropped.append(j)
                    changed = True
                    break
            if not changed:
                pair = _duplicate_pair(modes, sig, syms, D, alive, z, weights, real=not signed)
                if pair is not None:
                    alive.remove(pair)
                    dropped.append(pair)
                    changed = True
    Da = D[:, alive]
    near = np.array(alive)[Da.argmin(1)]
    ok = Da.min(1) < z
    ak = np.round(modes.kappa if signed else np.abs(modes.kappa), 9)
    if counts:
        return [{k: int(np.sum((near == j) & ok & (ak == k))) for k in set(ak[(near == j) & ok].tolist())}
                for j in range(len(syms))]
    sup = [sorted(set(ak[(near == j) & ok].tolist())) for j in range(len(syms))]
    return sup if weights is None else (sup, dropped)


def _duplicate_pair(modes, sig, syms, D, alive, z, weights, real):
    """Two factors of the same order m in tau that are one law fitted twice: the merged fit (one monic
    factor of order m through the modes of both, weighted by 1/sigma_lam; for m = 1 one branch
    lam = -sum_b c_b (i kappa)^b) against the two separate ones, by BIC at the mode level, distances
    |Q|/|dQ/dtau| as in the core (v2.13 G10: any m). Returns the index to drop (smaller weight) or None."""
    from .core.variety import fit_monic

    Da = D[:, alive]
    near = np.array(alive)[Da.argmin(1)]
    ok = Da.min(1) < z
    best = None
    for a in range(len(alive)):
        for b in range(a + 1, len(alive)):
            i, j = alive[a], alive[b]
            m = syms[i].m
            if syms[j].m != m:
                continue
            sel = ok & ((near == i) | (near == j))
            if sel.sum() < 2 or not (ok & (near == i)).any() or not (ok & (near == j)).any():
                continue
            dx = max(len(c) for c in list(syms[i].coeffs) + list(syms[j].coeffs)) - 1
            npar_m = m * (dx + 1)
            if m > 1 and sel.sum() < npar_m + 1:
                continue
            P, _, _ = fit_monic(modes.lam[sel], modes.kappa[sel], m, dx, 1.0 / sig[sel], real)
            chi_m = float(np.sum((_dist(P, modes.lam[sel], modes.kappa[sel]) / sig[sel]) ** 2))
            chi_s = float(np.sum(D[sel & (near == i), i] ** 2) + np.sum(D[sel & (near == j), j] ** 2))
            npar = npar_m * (1 if real else 2)
            dbic = chi_m - chi_s - npar * np.log(2 * sel.sum())
            if dbic < 0 and (best is None or dbic < best[0]):
                best = (dbic, i if weights[i] < weights[j] else j)
    return None if best is None else best[1]


EPS_GRID = np.logspace(-4, np.log10(0.5), 12)  # outlier-bin rate, marginalised (uniform on the grid)


def _robust_logev(b, subset, nt, real):
    """Per-bin mixture: a bin follows the factors' kernels (prob. 1 - eps) or is an outlier explained
    by its own exponentials (eps; their decay rates are plug-in, BIC 0.5 x 2 log n each). eps is
    marginalised. Interpolation bias at high kappa (GP smoothing, T35) is not in the noise draws: an
    outlier bin then costs log eps instead of steering the structure (plan v2.1(c))."""
    em = b.bin_logev[subset]
    if b.free_logev is None or len(em) == 0:
        return float(np.sum(em))
    n_free = np.asarray(b.free_order, float)
    ef = b.free_logev - 0.5 * 2 * n_free * np.log(nt * (1 if real else 2))
    tot = [np.sum(np.logaddexp(np.log1p(-e) + em, np.log(e) + ef)) for e in EPS_GRID]
    return float(np.logaddexp.reduce(tot) - np.log(len(EPS_GRID)))


def _raw_kmax(modes, period):
    """Band of the raw-data evidence: two wavenumbers beyond the largest one with an observed mode."""
    return int(np.max(np.abs(np.round(modes.kappa * period / (2 * np.pi))))) + 2 if len(modes) else 4


def raw_subset(factors, raw, kmax):
    """Most probable subset of the final factors by raw-data evidence (uniform prior over non-empty
    subsets). A factor that only explains an interpolation artifact is not supported by the raw
    observations. Returns (kept indices, {subset: log evidence})."""
    from itertools import combinations

    from .bayes_split import raw_evidence

    syms = [_poly_symbol(_sympy_of(f) if isinstance(f, FactorReport) else f) for f in factors]
    # real data: the real span of a factor's kernel contains its conjugate's, so a conjugate pair is
    # one unit (kept or dropped together)
    units, used = [], set()
    for i in range(len(factors)):
        if i in used:
            continue
        u_ = [i]
        if np.isrealobj(raw["ys"]) and isinstance(factors[i], FactorReport):
            for j in range(i + 1, len(factors)):
                if j not in used and isinstance(factors[j], FactorReport) and _conj_pair(factors[i], factors[j])                         and _nonreal(factors[i]):
                    u_.append(j)
                    break
        used.update(u_)
        units.append(u_)
    ev = {}
    for r in range(1, len(units) + 1):
        for us in combinations(range(len(units)), r):
            sub = tuple(sorted(j for k in us for j in units[k]))
            ev[sub] = raw_evidence([syms[j] for j in sub], raw["ts"], raw["xs"], raw["ys"], raw["period"], kmax,
                                   sigma=raw.get("sigma"))[0]
    return max(ev, key=ev.get), ev


def decide_structure(u, t, x, sigma, pooled, bounds, refine=False, noise_draws=None, top=5, min_mass=1e-6,
                     raw=None):
    """Data-level decider among the candidate structures (v2.9 #2(c), the EPGP idea in closed form):
    each of the `top` pooled structures is refitted on u (core, structure fixed) and scored by the
    Gaussian evidence of the data in the span of its factors' kernels (bayes_split, all factors).
    A factor's kernel predicts modes at every kappa: a fake factor (e.g. one constant factor per
    observed |kappa|) carries unused kernel directions in every bin and pays their Occam factor,
    which the mode-level BIC cannot see. raw: dict(ts, xs, ys, period, sigma) of the scattered
    observations; when given, the evidence is that of the raw data (raw_evidence), which carries no
    interpolation artifact. Returns (best structure, {structure: log evidence})."""
    from .bayes_split import bayes_split

    cand = [s for s, p in sorted(pooled.items(), key=lambda kv: -kv[1]) if p >= min_mass][:top]
    # also every structure with one factor less (the data decide if it was needed), on grids too
    # (v2.13: the moves are not specific to scattered data)
    if True:
        for st in list(cand):
            for j in range(len(st)):
                sub = st[:j] + st[j + 1:]
                if sub and sub not in cand:
                    cand.append(sub)
            # and every pair of factors merged into their product's class (m1 + m2, dx1 + dx2): a
            # near-reducible irreducible factor (telegraph ~ two damped transports) is then scored
            # against its factorisation (regroup merge move, v2.9 #5). Any pair of orders is merged
            # (v2.13 G3: a damped transport times a quadratic is near an irreducible cubic just as two
            # transports are near telegraph), but only factors that depend on xi (dx >= 1): a pure
            # decay tau + c (dx = 0) merged into a law Q gives (tau + c) Q, which hides a spurious
            # factor from the raw subset check (KG -> tau KG)
            for i in range(len(st)):
                for j in range(i + 1, len(st)):
                    if min(st[i][1], st[j][1]) < 1 and not MERGE_DX0:
                        continue
                    # the product's class (dx1 + dx2) and the smallest class that can hold an
                    # irreducible law near it (max dx): the product class pays for coefficients an
                    # irreducible neighbour does not have (cubic_tau: (3, 2), not (3, 4))
                    for mg in {(st[i][0] + st[j][0], st[i][1] + st[j][1]),
                               (st[i][0] + st[j][0], max(st[i][1], st[j][1]))}:
                        if mg[0] <= bounds[0] and mg[1] <= bounds[1]:
                            new = tuple(sorted(st[:i] + st[i + 1:j] + st[j + 1:] + (mg,)))
                            if new not in cand:
                                cand.append(new)
    ev, saturated = {}, {}
    real = bool(np.isrealobj(u))
    # free model per bin: the bin's own exponentials (pencil, order by IC) for the outlier-bin mixture
    m0, _, _, _ = extract_modes_ic(u, t, x, noise=sigma, noise_draws=noise_draws)
    free = {int(k): m0.lam[m0.kidx == k] for k in np.unique(m0.kidx)}
    for st in cand:
        r = analyze_structured(u, t, x, noise=sigma, m_max=bounds[0], dx_max=bounds[1], real=real,
                               refine=refine, structures=[st], noise_draws=noise_draws)
        if not r.factors:
            continue
        b = bayes_split(u, t, x, [f.symbol for f in r.factors], noise=sigma, noise_draws=noise_draws, ndraw=2,
                        free_modes=free)
        # the symbols' coefficients are fitted (plug-in), not integrated: Laplace/BIC Occam factor
        # 0.5 p log n for them, else a higher-degree symbol through the same modes ties with the true
        # one (same kernel on the band) and wins on noise
        # identifiability count (R4-T4 / He-Zhao-Zhong, with one residual degree of freedom): each
        # observed kappa gives m complex roots = 2m real equations; a factor with m (dx + 1)
        # coefficients (real field: real; complex field: complex, i.e. twice) that has no more
        # equations than unknowns interpolates its modes and fits their noise
        # equations = observed roots, at most m per kappa: a branch never seen (one-way waves of a
        # complex field fitted by an m = 2 factor) gives no equation
        cnt = kappa_support(u, t, x, sigma, [f.sympy for f in r.factors], noise_draws, signed=not real,
                            counts=True)
        saturated[st] = any(2 * sum(min(m, n) for n in c.values()) <= m * (dx + 1) * (1 if real else 2)
                            for (m, dx), c in zip(st, cnt))
        if raw is not None:
            from .bayes_split import raw_evidence

            e_raw, _ = raw_evidence([f.symbol for f in r.factors], raw["ts"], raw["xs"], raw["ys"], raw["period"],
                                    _raw_kmax(m0, raw["period"]), sigma=raw.get("sigma"))
            n_raw = len(raw["ys"]) * (1 if real else 2)
            ev[st] = e_raw - 0.5 * sum(m * (dx + 1) for m, dx in st) * (1 if real else 2) * np.log(n_raw)
            continue
        n_obs = len(b.bins) * len(t) * (1 if real else 2)
        p_sym = sum(m * (dx + 1) for m, dx in st) * (1 if real else 2)
        ev[st] = _robust_logev(b, tuple(range(len(r.factors))), len(t), real) - 0.5 * p_sym * np.log(max(n_obs, 2))
    if not ev:
        return None, ev
    ok = [s for s in ev if not saturated.get(s)] or list(ev)
    return max(ok, key=ev.get), ev


MERGE_DX0 = True  # v2.13 G3: merge a pure decay tau + c too (split_branches + refined factor drops undo it)
W_DRAWS = 16  # coefficient draws for the weight posterior (Monte Carlo size, not a tuning knob)


def coef_draws(reports, R, seed=0):
    """R draws of the pruned factor list from the coefficient posteriors: each kept coefficient part
    ~ N(median, ((q95 - q05) / (2 z90))^2), independent; a factor that is the conjugate of an earlier
    one follows it (the real-field closure). Monte Carlo over the factor uncertainty (rule 4)."""
    from .refine_raw import Z90

    rng = np.random.default_rng(seed)
    pruned = [_coef_dict(q) for q in LoopResult("", reports, {}, {}, [], False, (0, 0), {}).pruned()]
    partner = {j: i for j in range(len(reports)) for i in range(j)
               if _nonreal(reports[j]) and _conj_pair(reports[i], reports[j])}
    out = []
    for _ in range(R):
        qs = []
        for j, (f, keep) in enumerate(zip(reports, pruned)):
            if j in partner:
                qs.append(sp.expand(sp.conjugate(qs[partner[j]]).subs({sp.conjugate(tau): tau, sp.conjugate(xi): xi})))
                continue
            m = max(a for a, _ in f.coef)
            q = 0
            for k in keep:
                med, lo, hi = f.coef.get(k, (keep[k], keep[k], keep[k]))
                c = complex(med)
                if k != (m, 0):
                    sr, si = (hi.real - lo.real) / (2 * Z90), abs(hi.imag - lo.imag) / (2 * Z90)
                    c = complex(med.real + sr * rng.standard_normal() if sr > 0 else med.real,
                                med.imag + si * rng.standard_normal() if si > 0 else med.imag)
                q += (c.real if c.imag == 0 else c) * tau ** k[0] * xi ** k[1]
            qs.append(sp.expand(q))
        out.append(qs)
    return out


def split_layer(samples, pis, t, x, sigma, factors, noise_draws=None, ndraw=200, seed=0, coef_lists=None):
    """bayes_split on every posterior sample with the final factors; pooled: P(split) and inclusion
    probabilities are pi-weighted means, the weight posterior is the pi-weighted mixture of the
    per-sample Monte Carlo draws (outer MC over interpolants, inner closed form, 0b.10 output 3).
    coef_lists: optional list of factor lists drawn from the coefficient posteriors (coef_draws); the weight
    posterior then mixes over them as well (sample i % S paired with draw i), so the weight intervals
    carry the factor uncertainty, while P(split) and the subset posterior stay at the medians."""
    from .bayes_split import bayes_split

    syms = [_poly_symbol(q) for q in factors]
    rng = np.random.default_rng(seed)
    draws, ps, pinc, cfs, gs, psub = [], [], [], [], [], []
    w = np.asarray(pis, float) / np.sum(pis)
    for i, (u, p) in enumerate(zip(samples, w)):
        r = bayes_split(u, t, x, syms, noise=sigma, noise_draws=noise_draws, ndraw=ndraw, seed=seed + i,
                        snr_min=0.5)
        nd = max(1, int(round(p * ndraw * len(samples))))
        draws.append(r.weight_draws[rng.integers(0, len(r.weight_draws), nd)])
        ps.append(r.p_split)
        pinc.append(r.p_include)
        cfs.append(r.cF)
        gs.append(r.gamma)
        keys = list(r.log_evidence)
        lp = np.array([r.log_evidence[s] for s in keys])
        post = np.exp(lp - lp.max())
        psub.append(dict(zip(keys, post / post.sum())))
    if coef_lists:
        S = len(samples)
        nev = max(S, len(coef_lists))
        per = max(1, int(round(ndraw * S / nev)))
        draws_w = []
        for i in range(nev):
            si = i % S
            try:
                r = bayes_split(samples[si], t, x, [_poly_symbol(q) for q in coef_lists[i % len(coef_lists)]], noise=sigma,
                                noise_draws=noise_draws, ndraw=per, seed=seed + 1000 + i, snr_min=0.5)
            except Exception:  # noqa: BLE001 - a draw with a degenerate kernel adds no weight draws
                continue
            if np.all(np.isfinite(r.weight_draws)):
                draws_w.append(r.weight_draws[rng.integers(0, len(r.weight_draws), max(1, int(round(w[si] * per * S))))])
        if draws_w:
            draws = draws_w
    D = np.concatenate(draws)
    p_subset = {s: float(sum(wi * d[s] for wi, d in zip(w, psub))) for s in psub[0]}
    return {"p_split": float(np.dot(w, ps)), "p_include": np.average(pinc, axis=0, weights=w).tolist(),
            "w_mean": D.mean(0).tolist(), "w_q": np.quantile(D, [0.05, 0.5, 0.95], axis=0).T.tolist(),
            "cF": float(np.dot(w, cfs)), "gamma": float(np.dot(w, gs)), "p_subset": p_subset}


def _grow(bounds):
    m, dx = bounds
    if dx < DX_LIMIT:
        return (m, dx + 1)
    if m < M_LIMIT:
        return (m + 1, dx)
    return None


def _grow_options(bounds):
    """G7: both one-step enlargements of the class (more spatial degree, more total order in tau);
    the loop fits each and keeps the one with more FIT-COMPATIBLE mass, so a law that needs a
    higher order in tau is not forced through the whole dx ladder first."""
    m, dx = bounds
    return [b for b in ((m, dx + 1), (m + 1, dx)) if b[0] <= M_LIMIT and b[1] <= DX_LIMIT]


# P3: growth past M_LIMIT / DX_LIMIT while V0.1 still fails at the bound (env PDEFACTOR_GROW_PAST=1; off by default)
GROW_PAST = os.environ.get("PDEFACTOR_GROW_PAST", "0") == "1"
GROW_PAST_M, GROW_PAST_DX = 1, 2  # hard cap: at most M_LIMIT + 1 in tau, DX_LIMIT + 2 in xi
GROW_PAST_STEPS = 2  # hard cap on accepted steps past the bound


def _grow_past_options(bounds):
    """One-step enlargements of the class beyond M_LIMIT / DX_LIMIT, within the hard cap."""
    m, dx = bounds
    return [b for b in ((m, dx + 1), (m + 1, dx))
            if b[0] <= M_LIMIT + GROW_PAST_M and b[1] <= DX_LIMIT + GROW_PAST_DX]


def _accept_past(lp, lp2, sc2, p2, cur, p_cur):
    """A step past the bound is accepted only on both tests already in use: the V0.1 omnibus improves
    by the same 3 decades as gain_pred, and the refined evidence - Occam term beats the current level
    by the bare-mention rule (_beats, T74). A missing score (None) never accepts."""
    if sc2 is None or cur is None:
        return False
    return lp2 > lp + 3.0 and _beats(sc2, p2, cur, p_cur)


def _level_score(agg, samples, pis, t, x, sigma, nd, raw):
    """(refined evidence - Occam, real parameters) of a level's pooled factors on the observations
    (raw, or the grid itself); (None, None) when there is no observation set to score on. Works on copies."""
    obs = raw if raw is not None else (_grid_obs(samples[0], t, x, sigma)
                                       if len(samples) == 1 and nd is None and sigma > 0 else None)
    if obs is None or not obs.get("sigma"):
        return None, None
    try:
        a = copy.deepcopy(agg)
        pk = _p_k(a)
        if pk:
            _merge_tracks(a, max(pk, key=pk.get))
        fa = [fr for _, fr in _factor_reports(a)]
        if not fa:
            return None, None
        if np.isrealobj(samples[0]):
            conjugate_closure(fa)
        u_ref = _mean_sample(samples, pis)
        ndh = None if nd is None else nd / np.sqrt(2)
        m_ref, _, _, _ = extract_modes_ic(u_ref, t, x, noise=sigma, noise_draws=ndh)
        ro = refine_factors(fa, obs, _raw_kmax(m_ref, obs["period"]))
    except (np.linalg.LinAlgError, ValueError, ZeroDivisionError):
        return None, None
    occ = 0.5 * np.log(len(obs["ys"]) * (1 if np.isrealobj(obs["ys"]) else 2))
    return ro["logev"] - occ * ro["p"], _n_real_params([fa[j] for j in ro["active"]])


def _grow_past(samples, pis, t, x, sigma, bounds, refine, nd, raw, res, agg, lp, history):
    """P3: at the class bound with V0.1 still failing, try one-step enlargements past it (hard cap
    GROW_PAST_M / GROW_PAST_DX, at most GROW_PAST_STEPS steps); each step is kept only by _accept_past.
    Returns (res, agg, bounds, lp)."""
    cur, p_cur = _level_score(agg, samples, pis, t, x, sigma, nd, raw)
    for _ in range(GROW_PAST_STEPS):
        opts = _grow_past_options(bounds)
        if lp >= PRED_LOGP or not opts or cur is None:
            break
        fits = []
        for ob in opts:
            r_o, a_o = _run(samples, pis, t, x, sigma, ob, refine, noise_draws=nd)
            _attach(r_o, samples)
            lp_o = _pred_logp(r_o, t, x, sigma, nd)
            sc_o, p_o = _level_score(a_o, samples, pis, t, x, sigma, nd, raw)
            fits.append((ob, r_o, a_o, lp_o, sc_o, p_o))
        ok = [f for f in fits if _accept_past(lp, f[3], f[4], f[5], cur, p_cur)]
        best = max(ok, key=lambda f: f[4]) if ok else max(fits, key=lambda f: f[3])
        lev = Level(best[0], _p(best[2], ["FIT-COMPATIBLE"]), accepted=bool(ok))
        if not ok:
            lev.note = ("rejected past the class bound: no V0.1 gain with refined evidence beating the "
                        "current level (_beats)")
            history.append(lev)
            break
        lev.note = "grown past the class bound (P3): V0.1 gain and refined evidence (_beats)"
        history.append(lev)
        bounds, res, agg, lp, cur, p_cur = best[0], best[1], best[2], best[3], best[4], best[5]
    return res, agg, bounds, lp


def _coef_dict(q):
    p = sp.Poly(sp.expand(sp.N(q)), tau, xi, domain="CC")
    return {mon: complex(c) for mon, c in zip(p.monoms(), p.coeffs())}


def _wq(v, w, q):
    o = np.argsort(v)
    c = np.cumsum(w[o]) / w.sum()
    return float(v[o][np.searchsorted(c, q).clip(0, len(v) - 1)])


def _merge_tracks(agg, k_star):
    """The DP may split one factor into several tracks across samples (Miller-Harrison). Two tracks
    that never occur in the same sample and have the same tau-degree are one factor: merge the
    lightest such pair until the number of tracks equals the MAP number of factors."""
    cl = agg.cloud
    while True:
        ids = [j for j in np.unique(cl.track)]
        if len(ids) <= k_star:
            break
        W = {j: cl.mass[cl.track == j].sum() for j in ids}
        samples = {j: set(cl.sample[cl.track == j]) for j in ids}
        m = {j: int(np.bincount(cl.m[cl.track == j]).argmax()) for j in ids}
        pairs = [(W[a] + W[b], a, b) for a in ids for b in ids
                 if a < b and m[a] == m[b] and not samples[a] & samples[b]]
        if not pairs:
            break
        _, a, b = min(pairs)
        cl.track[cl.track == b] = a
    used = np.unique(cl.track)
    cl.track = np.searchsorted(used, cl.track)
    if len(used) > k_star:
        _align_tracks(cl, k_star)
        used = np.unique(cl.track)
    W = np.array([cl.mass[cl.track == j].sum() for j in range(len(used))])
    agg.W_track = W / W.sum() if W.sum() > 0 else W


def _align_tracks(cl, k_star, iters=20):
    """Grouping by factors when the DP tracks still outnumber the MAP k (tracks that co-occur in some
    sample cannot be merged pairwise): constrained k-means on the factor coefficient vectors, with
    at most one factor of each sample per group (Hungarian matching per sample). Started from the
    heaviest sample that has exactly k factors. Extra factors of a sample with more than k go to
    their nearest group."""
    from scipy.optimize import linear_sum_assignment

    S = np.unique(cl.sample)
    rows = {s: np.where(cl.sample == s)[0] for s in S}
    full = [s for s in S if len(rows[s]) == k_star]
    if not full:
        return
    ref = max(full, key=lambda s: cl.pi[rows[s][0]])
    C = cl.theta[rows[ref]].copy()
    lab = np.zeros(len(cl), int)
    for _ in range(iters):
        new = np.zeros(len(cl), int)
        for s in S:
            i = rows[s]
            D = ((cl.theta[i][:, None, :] - C[None]) ** 2).sum(-1)
            r, c = linear_sum_assignment(D)
            new[i] = D.argmin(1)
            new[i[r]] = c
        for j in range(k_star):
            sel = new == j
            if sel.any():
                C[j] = np.average(cl.theta[sel], axis=0, weights=cl.mass[sel] + 1e-300)
        if np.array_equal(new, lab):
            break
        lab = new
    cl.track = lab


def _factor_reports(agg):
    cl = agg.cloud
    out = []
    for j in np.argsort(-agg.W_track):
        sel = np.where(cl.track == j)[0]
        if not len(sel):
            continue
        out.append((j, _report([_coef_dict(cl.sympy[i]) for i in sel], cl.mass[sel], float(agg.W_track[j]))))
    return out


LOG_BF_STRONG = np.log(150.0)  # Kass & Raftery (1995): "very strong" evidence
LOG_BF_BARE = 1.0  # Kass & Raftery (1995): 2 ln B < 2 is "not worth more than a bare mention"


def screen_samples(agg, raw, u_ref, t, x, sigma, noise_draws=None):
    """Per-sample fits seen by the raw observations: each sample's factor set is scored by
    raw_evidence; a sample whose set the raw data reject very strongly against the weighted median
    sample (log Bayes factor > LOG_BF_STRONG) is a failed per-sample fit (the alternating fit kept a
    factor through one kappa and capped the rest as outliers), not posterior spread: its mass is set
    to 0 in the cloud. At least half of the mass is kept by construction. Returns the number rejected."""
    from .bayes_split import raw_evidence

    cl = agg.cloud
    ss = np.unique(cl.sample)
    if len(ss) < 3:
        return 0
    m0, _, _, _ = extract_modes_ic(u_ref, t, x, noise=sigma, noise_draws=noise_draws)
    kmax = _raw_kmax(m0, raw["period"])
    ev, pw = [], []
    for s in ss:
        sel = np.where(cl.sample == s)[0]
        syms = [_poly_symbol(cl.sympy[i]) for i in sel]
        ev.append(raw_evidence(syms, raw["ts"], raw["xs"], raw["ys"], raw["period"], kmax,
                               sigma=raw.get("sigma"))[0])
        pw.append(cl.pi[sel[0]])
    ev, pw = np.array(ev), np.array(pw)
    ref = _wq(ev, pw + 1e-300, 0.5)
    bad = ss[ev < ref - LOG_BF_STRONG]
    for s in bad:
        cl.pi[cl.sample == s] = 0.0
    return len(bad)


def _report(dicts, mass, W):
    """FactorReport from the coefficient dicts of one factor across samples: per coefficient the
    weighted posterior median (robust to the few samples whose fit went astray) and 5 / 95 % quantiles."""
    w = np.asarray(mass, float) + 1e-300
    # T79: a factor has one order in tau. The groupings that feed this (DP tracks, _align_tracks, the
    # conjugate k-means of _canonical_conj_reports) do not constrain it, and pooling fits of different
    # orders put a leading coefficient whose median is 0 into the report (ZeroDivisionError in
    # refine_factors, learned-layers corpus S). Pool only the fits of the weighted-majority order.
    def _order(d):
        return max((a for (a, _), v in d.items() if abs(complex(v)) > 0), default=0)

    ords = np.array([_order(d) for d in dicts])
    if len(set(ords.tolist())) > 1:
        tot = {o: float(w[ords == o].sum()) for o in set(ords.tolist())}
        m_ = max(tot, key=lambda o: (tot[o], -o))
        dicts = [{k: v for k, v in d.items() if k[0] <= m_} for d, o in zip(dicts, ords) if o == m_]
        w = w[ords == m_]
    keys = sorted(set().union(*dicts))
    coef = {}
    for kk in keys:
        v = np.array([d.get(kk, 0.0) for d in dicts])
        med = complex(_wq(v.real, w, 0.5), _wq(v.imag, w, 0.5))
        lo = complex(_wq(v.real, w, 0.05), _wq(v.imag, w, 0.05))
        hi = complex(_wq(v.real, w, 0.95), _wq(v.imag, w, 0.95))
        coef[kk] = (med, lo, hi)
    expr = sum((c[0].real if abs(c[0].imag) < 1e-12 else c[0]) * tau**a * xi**b for (a, b), c in coef.items())
    return FactorReport(sp.expand(expr), W, coef)


def _canonical_conj_reports(agg, n_pairs=1):
    """Real field, complex-coefficient run with n_pairs conjugate pairs {Q, conj Q} per sample: the DP
    tracks may swap Q and conj Q between samples. Every non-real factor is put in one orientation (the
    largest imaginary coefficient positive), the oriented fits are grouped into n_pairs clusters
    (k-means on the coefficient vectors, farthest-point start), each cluster is pooled and reported with
    its conjugate (v2.13 G5: any number of pairs)."""
    cl = agg.cloud
    real_i, cpx = [], []
    for i in range(len(cl)):
        d = _coef_dict(cl.sympy[i])
        if any(abs(v.imag) > 1e-9 * max(1.0, abs(v)) for v in d.values()):
            kk = max(d, key=lambda k: abs(d[k].imag))
            cpx.append((i, d if d[kk].imag > 0 else {k: np.conj(v) for k, v in d.items()}))
        else:
            real_i.append(i)
    if not cpx:
        return None
    keys = sorted(set().union(*[d for _, d in cpx]))
    V = np.array([[d.get(k, 0j) for k in keys] for _, d in cpx])
    V = np.concatenate([V.real, V.imag], axis=1)
    m = np.array([cl.mass[i] for i, _ in cpx])
    g = max(1, min(int(n_pairs), len(cpx)))
    cen = [V[int(np.argmax(m))]]
    while len(cen) < g:
        dist = np.min([np.linalg.norm(V - c, axis=1) for c in cen], axis=0)
        cen.append(V[int(np.argmax(dist))])
    cen = np.array(cen)
    for _ in range(50):
        lab = np.argmin(np.linalg.norm(V[:, None] - cen[None], axis=2), axis=1)
        new = np.array([np.average(V[lab == c], axis=0, weights=m[lab == c] + 1e-300) if np.any(lab == c) else cen[c]
                        for c in range(g)])
        if np.allclose(new, cen):
            break
        cen = new
    out = []
    tot = max(cl.mass.sum(), 1e-300)
    for c in range(g):
        sel = lab == c
        if not np.any(sel):
            continue
        Wc = float(m[sel].sum() / tot)
        a = _report([d for (_, d), s_ in zip(cpx, sel) if s_], m[sel], Wc / 2)
        b = FactorReport(sp.expand(sp.conjugate(a.sympy).subs({sp.conjugate(tau): tau, sp.conjugate(xi): xi})), Wc / 2,
                         {k: (np.conj(c_[0]), complex(c_[1].real, -c_[2].imag), complex(c_[2].real, -c_[1].imag))
                          for k, c_ in a.coef.items()})
        out += [a, b]
    tr = {}
    for i in real_i:
        tr.setdefault(int(cl.track[i]), []).append(i)
    for j, ii in tr.items():
        out.append(_report([_coef_dict(cl.sympy[i]) for i in ii], cl.mass[ii], float(cl.mass[ii].sum() / max(cl.mass.sum(), 1e-300))))
    return out


def _half_plane_reports(ac, n_real):
    """T98. Factor reports of a half-plane complex-coefficient run of a real field (structfit.half_plane):
    every factor A fitted on kappa > 0 is reported with its conjugate (the kappa < 0 mirror lies on conj A),
    each with half of A's track mass; a factor the core kept real (real_restrict) is its own conjugate and
    keeps its mass. The half plane fixes the orientation, so no conjugate matching across samples is needed
    (cf. _canonical_conj_reports). Returns None unless some factor is non-real and the closed set has more
    factors than the n_real factors of the real run (only a split over C is new here)."""
    pk = _p_k(ac)
    _merge_tracks(ac, max(pk, key=pk.get))
    crep = [fr for _, fr in _factor_reports(ac)]
    nonreal = [fr for fr in crep if _nonreal(fr)]
    if not nonreal:
        return None
    for fr in crep:
        if _nonreal(fr):
            fr.W = fr.W / 2
            fr.status = "factor over C (complex-coefficient run on the half plane kappa > 0; one of a conjugate pair)"
        else:
            fr.status = "real factor of the half-plane complex-coefficient run (its own conjugate)"
    conjugate_closure(crep)
    return crep if len(crep) > n_real else None


def _track_components(results, agg, j):
    """Per sample, the component field of the factor that sits in track j (None if absent)."""
    tr = agg.cloud.track
    i, comps, pis = 0, [], []
    for r, p in results:
        hit = None
        for jf in range(len(r.factors)):
            if tr[i] == j and r.components:
                hit = r.components[jf]
            i += 1
        if hit is not None:
            comps.append(hit)
            pis.append(p)
    return comps, np.asarray(pis, float)


def domain_report(results, agg, t, x, blocks=(4, 8)):
    """Report only: for each factor track, its share of the energy in each (t, x) block, pooled
    over samples. Shares over the tracks sum to 1 in every block that has energy."""
    nbt, nbx = blocks
    it = np.array_split(np.arange(len(t)), nbt)
    ix = np.array_split(np.arange(len(x)), nbx)
    nt = len(agg.W_track)
    E = np.zeros((nt, nbt, nbx))
    for j in range(nt):
        comps, pis = _track_components(results, agg, j)
        for c, p in zip(comps, pis):
            a2 = np.abs(c) ** 2
            E[j] += p * np.array([[a2[np.ix_(a, b)].sum() for b in ix] for a in it])
    tot = E.sum(0, keepdims=True)
    share = np.where(tot > 0, E / np.where(tot > 0, tot, 1), 0.0)
    return {"blocks": blocks, "t_edges": [t[a[0]] for a in it] + [t[-1]],
            "x_edges": [x[b[0]] for b in ix] + [x[-1]], "share": share}


def bootstrap_intervals(factors, u, t, x, sigma, B=16, seed=0, kmax=None):
    """Coefficient intervals of the final factors on a single noisy grid (no posterior samples, so
    the pooled quantiles are degenerate): parametric bootstrap at the fixed final structure. Given u,
    the copies u + sigma eps differ only by the added noise of std sigma, so the spread of the
    refitted coefficients about their median is that of a fit at noise sigma; it is added to the
    reported median (Monte Carlo; the core is the same black box). Factors are matched to the refit
    ones by coefficient distance. kmax given: the factors were refined on the grid observations
    (T51), so each copy is refitted by that same refinement at the fixed final support (the bootstrap
    of the estimator that produced the reported values; the core's mode-level spread is far wider and
    put 0 inside the interval of terms the refined evidence keeps, T75). In place."""
    from scipy.optimize import linear_sum_assignment

    real = bool(np.isrealobj(u)) and not any(_nonreal(f) for f in factors)
    st = tuple(sorted((max(a for a, _ in f.coef), max(b for _, b in f.coef)) for f in factors))
    rng = np.random.default_rng(seed)
    deltas = [{k: [] for k in f.coef} for f in factors]
    for _ in range(B):
        ub = u + sigma * rng.standard_normal(u.shape)
        if kmax is not None:
            fb = copy.deepcopy(factors)
            try:
                ro = refine_factors(fb, _grid_obs(ub, t, x, np.sqrt(2) * sigma), kmax)
            except (np.linalg.LinAlgError, ValueError, ZeroDivisionError):
                continue
            if len(ro["active"]) != len(factors):
                # a bare factor (tau^m alone, e.g. split off after the refinement by the exact finest
                # split) has no coefficient to bootstrap; a copy whose refinement drops only such factors
                # still refits every reported coefficient (skipping it skipped every copy: zero width)
                from . import refine_raw

                if not ((SPLIT_FINEST or refine_raw.BRANCH_ARD)
                        and all(len(factors[j].coef) == 1 for j in range(len(factors)) if j not in ro["active"])):
                    continue
            for i, f in enumerate(fb):
                for k in factors[i].coef:
                    deltas[i][k].append(complex(f.coef.get(k, (0j,))[0]))
            continue
        r = analyze_structured(ub, t, x, noise=np.sqrt(2) * sigma, real=real, structures=[st])
        if len(r.factors) != len(factors):
            continue
        ds = [_coef_dict(fr.sympy) for fr in r.factors]
        C = np.array([[sum(abs(f.coef.get(k, (0j,))[0] - d.get(k, 0.0)) for k in set(f.coef) | set(d))
                       for d in ds] for f in factors])
        rows, cols = linear_sum_assignment(C)
        for i, j in zip(rows, cols):
            for k in factors[i].coef:
                deltas[i][k].append(complex(ds[j].get(k, 0.0)))
    for f, dk in zip(factors, deltas):
        for k, v in dk.items():
            if len(v) < max(4, B // 2):
                continue
            v = np.array(v)
            c = np.median(v.real) + 1j * np.median(v.imag)
            d = v - c
            med = f.coef[k][0]
            if k == (max(a for a, _ in f.coef), 0):
                continue  # the normalised leading term
            f.coef[k] = (med, complex(med.real + np.quantile(d.real, 0.05), med.imag + np.quantile(d.imag, 0.05)),
                         complex(med.real + np.quantile(d.real, 0.95), med.imag + np.quantile(d.imag, 0.95)))


def _refit_support(lam, kappa, w, m, params):
    """Weighted LS of the monic factor tau^m + sum_params c tau^a xi^b on its modes. params: list of
    ((a, b), part), part 0 = real part of c, 1 = imaginary part (real unknowns). w = 1 / (sigma_lam
    |dQ/dtau|) at the full fit, so the residuals are distances to the variety in sigma units.
    Returns ({(a, b): complex}, chi2)."""
    xi_ = 1j * np.asarray(kappa, float)
    sl = max(np.abs(lam).max(), 1e-12)
    sx = max(np.abs(xi_).max(), 1e-12)
    rhs = -((lam / sl) ** m) * w
    if params:
        A = np.stack([(1j if p else 1.0) * (lam / sl) ** a * (xi_ / sx) ** b for (a, b), p in params], 1) * w[:, None]
        Ar, br = np.vstack([A.real, A.imag]), np.concatenate([rhs.real, rhs.imag])
        c, *_ = np.linalg.lstsq(Ar, br, rcond=None)
        res = Ar @ c - br
    else:
        c, res = np.zeros(0), -np.concatenate([rhs.real, rhs.imag])
    coef = {(m, 0): 1.0 + 0j}
    for ((a, b), p), ci in zip(params, c):
        coef[(a, b)] = coef.get((a, b), 0j) + (1j if p else 1.0) * ci * sl ** (m - a) / sx**b
    return coef, float(res @ res)


def support_path(factors, u, t, x, sigma, noise_draws=None, z=3.0, dx_class=None):
    """Mode-level backward-elimination path of each factor's support: starting from all its real
    parameters, the one whose removal raises the weighted chi^2 least is removed, down to the bare
    tau^m; every support on the path comes with its weighted-LS coefficients (a linear solve: no local
    optimum). Returns {j: [path, ...]} (candidates for refine_raw.refine), with the pooled Wald path
    of each factor added (_wald_path). dx_class: with PATH_CLASS on, the xi-degree of the searched class
    (the loop's bound); the path then starts from every tau^a xi^b, b <= dx_class, not only b <= the
    factor's own xi-degree (T94)."""
    modes, bn, _, _ = extract_modes_ic(u, t, x, noise=sigma, noise_draws=noise_draws)
    if len(modes) == 0 or not factors:
        return {}
    sig = sigma_lambda(modes, t, bn)
    real_u = bool(np.isrealobj(u))
    syms = [_poly_symbol(_sympy_of(f)) for f in factors]
    D = np.stack([_dist(Q, modes.lam, modes.kappa) for Q in syms], axis=1) / sig[:, None]
    near = D.argmin(1)
    out = {}
    for j, (f, Q) in enumerate(zip(factors, syms)):
        mine = near == j
        if not mine.any():
            continue
        s_rob = max(1.0, np.sqrt(np.median(D[mine, j] ** 2) / 0.455))
        sel = mine & (D[:, j] < z * s_rob)
        lam, kap = modes.lam[sel], modes.kappa[sel]
        m = max(a for a, _ in f.coef)
        cplx = not real_u or _nonreal(f)
        # the full rectangular class of the factor (every tau^a xi^b, a < m, b <= its xi-degree): a term
        # the core rounded to 0 (absolute tolerance, small high-order coefficients) can come back if the
        # observations support it (v2.13 G2)
        dxf = max(b for _, b in f.coef)
        dxs = [dxf]
        if PATH_CLASS and dx_class is not None and int(dx_class) > dxf:
            # T94: a term of higher xi-degree than the core's pooled fit kept (a small xi^4 rounded to 0)
            # can only return through the path; the evidence - Occam term of refine decides.
            # T100: the class path is ADDED after the factor's own path, not substituted for it: the backward
            # elimination from the larger class can leave the own-degree supports (two_pairs grid 1 %: the
            # class path from xi^0..xi^3 ran through odd-xi supports and never met {1, xi^2} of the true
            # tau + 0.192 - 0.099 i xi^2, refined 27460.9 at p = 4 vs the truth's 27481.9 at p = 3)
            dxs.append(int(dx_class))
        if not len(lam):
            continue
        h = 1e-6 * (1 + np.abs(lam))
        dQ = np.abs((Q(lam + h, 1j * kap) - Q(lam - h, 1j * kap)) / (2 * h))
        w = max(np.abs(lam).max(), 1e-12) ** m / (np.maximum(dQ, 1e-12) * sig[sel])
        paths = []
        for dxp in dxs:
            params = [((a, b), p) for a in range(m) for b in range(dxp + 1) for p in ((0, 1) if cplx else (0,))]
            path = []
            if PATH_FULL and params:
                # T102: the path starts AT the full rectangular support, not after its first removal
                path.append(_refit_support(lam, kap, w, m, params)[0])
            while params:
                best = None
                for i in range(len(params)):
                    ps = params[:i] + params[i + 1:]
                    c2, x2 = _refit_support(lam, kap, w, m, ps)
                    if best is None or x2 < best[1]:
                        best = (ps, x2, c2)
                params = best[0]
                path.append(best[2])
            if path:
                paths.append(path)
        if not paths:
            continue
        out[j] = paths
    for j, f in enumerate(factors):
        out.setdefault(j, []).append(_wald_path(f))
    return out


def _wald_path(f):
    """Nested supports of a factor from its pooled posterior: real parameters removed in order of
    their Wald ratio |median| / 90 % half-width (weakest first), the rest kept at their medians."""
    m = max(a for a, _ in f.coef)
    parts = []
    for k, (med, lo, hi) in f.coef.items():
        if k == (m, 0):
            continue
        for p, v, h in ((0, med.real, (hi.real - lo.real) / 2), (1, med.imag, (hi.imag - lo.imag) / 2)):
            if v != 0.0:
                parts.append((abs(v) / max(h, 1e-12 * max(abs(v), 1.0)), k, p))
    parts.sort()
    cur = {k: complex(v[0]) for k, v in f.coef.items()}
    path = []
    for _, k, p in parts:
        cur = dict(cur)
        cur[k] = complex(cur[k].real, 0.0) if p else complex(0.0, cur[k].imag)
        if cur[k] == 0:
            del cur[k]
        path.append(cur)
    return path


def refine_factors(factors, obs, kmax, candidates=None):
    """Refinement pass of the final factors on the observations (refine_raw, T51-T52): coefficients
    by maximum raw kernel evidence, the support by evidence with the Occam term over the candidate
    supports, Laplace 90 % intervals. obs: dict(ts, xs, ys, period, sigma), the scattered observations
    or every grid point. A factor of a real field that is the conjugate of another is tied to it.
    In place; returns refine's output."""
    from .refine_raw import refine

    real = bool(np.isrealobj(obs["ys"]))
    ms = [max(a for a, _ in f.coef) for f in factors]
    coefs = [{k: complex(v[0]) / complex(f.coef[(m, 0)][0]) for k, v in f.coef.items()} for f, m in zip(factors, ms)]
    ties = {}
    if real:
        for j, f in enumerate(factors):
            if j in ties or not _nonreal(f):
                continue
            for i in range(j + 1, len(factors)):
                if i not in ties and i not in ties.values() and _conj_pair(f, factors[i]):
                    ties[i] = j
                    break
    cands = {j: c for j, c in (candidates or {}).items() if j not in ties}
    out = refine(coefs, ms, obs, kmax, ties=ties, candidates=cands)
    for j, f in enumerate(factors):
        if j not in out["active"]:
            f.status += "; dropped: the refined factor set without it has larger evidence on the observations"
    for j, (f, m, c) in enumerate(zip(factors, ms, out["coefs"])):
        if j not in out["active"]:
            continue
        gone = sorted(set(f.coef) - set(c))
        new = {}
        for k, v in c.items():
            if k == (m, 0):
                new[k] = (1.0 + 0j, 1.0 + 0j, 1.0 + 0j)
                continue
            h = out["half"].get((j, k))
            if h is not None and np.isfinite(h.real) and np.isfinite(h.imag):
                new[k] = (complex(v), complex(v) - h, complex(v) + h)
            else:  # no Laplace width: the pooled interval, moved with the refined value
                med, lo, hi = f.coef.get(k, (v, v, v))
                d = complex(v) - complex(med)
                new[k] = (complex(v), complex(lo) + d, complex(hi) + d)
        f.coef = new
        f.sympy = sp.expand(sum((v[0].real if abs(v[0].imag) < 1e-12 else v[0]) * tau**a * xi**b
                                for (a, b), v in new.items()))
        f.status += "; refined on the observations"
        if gone:
            f.status += " (terms " + ", ".join(f"tau^{a} xi^{b}" for a, b in gone) + " dropped by evidence)"
    from . import refine_raw

    if refine_raw.BRANCH_ARD and out["active"]:
        # T98: the score every model comparison reads (logev - Occam) uses one prior scale per root
        # branch in each excited bin; the coefficients and their intervals stay those of the per-bin evidence
        # a tied conjugate is skipped as in refine (the real span of A's kernel holds conj A's)
        ev = refine_raw.log_evidence_branch([_poly_symbol(factors[j].sympy) for j in out["active"] if j not in ties],
                                            obs, kmax)
        if ev is not None:
            out["logev_bin"], out["logev"] = out["logev"], ev
    return out


def _poly_sqrt(d):
    """r with r^2 matching d (coefficients low -> high, even degree 2e) in degrees e..2e, by the
    square-root recursion from the top; returns (r, residual d - r^2 in degrees 0..e-1)."""
    e = (len(d) - 1) // 2
    r = np.zeros(e + 1, complex)
    r[e] = np.sqrt(complex(d[2 * e]))
    for i in range(e - 1, -1, -1):
        s = sum(r[a] * r[i + e - a] for a in range(i + 1, e))
        r[i] = (d[i + e] - s) / (2 * r[e])
    rr = np.convolve(r, r)
    return r, (np.asarray(d, complex) - rr)[:e]


def split_quadratics(factors, ndraw=400, seed=0, test=True):
    """A monic quadratic tau^2 + p(xi) tau + q(xi) is reducible over C iff its discriminant
    p^2 - 4q is a square in C[xi] (C12-P2/P3); it then factors as tau + (p -+ r) / 2. Decided like the
    pruning rule: every residual coefficient of the square-root recursion has 0 inside its 90 % Monte
    Carlo interval (draws from the coefficient intervals, rule 4). The core's and the complex rerun's
    fit can miss this split when the factor's coefficients were refined after them (beam:
    tau^2 + c^2 xi^4). test=False: the split is proposed wherever the recursion runs (the caller decides
    by evidence; the Monte Carlo test is one-sided where the discriminant lacks low-degree terms, e.g.
    -r_0^2 <= 0). Returns (new factor list, index of the source factor of each)."""
    rng = np.random.default_rng(seed)
    out = []
    for i_f, f in enumerate(factors):
        if max(a for a, _ in f.coef) != 2:
            out.append((f, i_f))
            continue
        dx = max(b for _, b in f.coef)

        def disc(cf):
            p = np.array([cf.get((1, b), 0j) for b in range(dx + 1)])
            q = np.array([cf.get((0, b), 0j) for b in range(dx + 1)])
            dd = np.convolve(p, p) - 4 * np.concatenate([q, np.zeros(dx)])
            nz = np.nonzero(np.abs(dd) > 1e-12 * max(np.abs(dd).max(), 1e-300))[0]
            return p, dd[: nz[-1] + 1] if len(nz) else dd[:1]

        med = {k: complex(v[0]) for k, v in f.coef.items()}
        p0, d0 = disc(med)
        if len(d0) % 2 == 0 or len(d0) < 3:  # odd degree: never a square (degree 0 is a repeated root)
            out.append((f, i_f))
            continue
        r0, res0 = _poly_sqrt(d0)
        sd = {k: ((complex(v[2]) - complex(v[1])) / (2 * 1.6448536269514722)) for k, v in f.coef.items()}
        draws, facs = [], []
        for _ in range(ndraw):
            cf = {k: med[k] + complex(sd[k].real * rng.standard_normal(), sd[k].imag * rng.standard_normal())
                  for k in med}
            p, d = disc(cf)
            if len(d) != len(d0):
                continue
            r, res = _poly_sqrt(d)
            if np.vdot(r, r0).real < 0:
                r = -r
            draws.append(res)
            facs.append((p, r))
        if len(draws) < ndraw // 2:
            out.append((f, i_f))
            continue
        R = np.array(draws)
        lo, hi = np.quantile(R.real, 0.05, axis=0), np.quantile(R.real, 0.95, axis=0)
        loi, hii = np.quantile(R.imag, 0.05, axis=0), np.quantile(R.imag, 0.95, axis=0)
        tol = 1e-6 * max(np.abs(d0).max(), 1.0)
        zero = np.all(((lo <= 0) & (hi >= 0)) | (np.abs(res0.real) < tol)) and \
            np.all(((loi <= 0) & (hii >= 0)) | (np.abs(res0.imag) < tol))
        if test and not zero:
            out.append((f, i_f))
            continue
        for sgn in (-1, 1):
            vals = np.array([(p + sgn * np.concatenate([r, np.zeros(len(p) - len(r))])) / 2 if len(p) >= len(r)
                             else (np.concatenate([p, np.zeros(len(r) - len(p))]) + sgn * r) / 2 for p, r in facs])
            cen = (p0 if len(p0) >= len(r0) else np.concatenate([p0, np.zeros(len(r0) - len(p0))]))
            r0p = np.concatenate([r0, np.zeros(len(cen) - len(r0))])
            c0 = (cen + sgn * r0p) / 2
            coef = {(1, 0): (1.0 + 0j, 1.0 + 0j, 1.0 + 0j)}
            for b in range(len(c0)):
                v = vals[:, b]
                q5 = complex(np.quantile(v.real, 0.05), np.quantile(v.imag, 0.05))
                q95 = complex(np.quantile(v.real, 0.95), np.quantile(v.imag, 0.95))
                coef[(0, b)] = (complex(c0[b]), q5, q95)
            g = FactorReport(sp.expand(tau + sum((c[0].real if abs(c[0].imag) < 1e-12 else c[0]) * xi**b
                                                 for (a, b), c in coef.items() if a == 0)),
                             f.W / 2, coef, status=f"factor of the reducible quadratic {f.sympy} "
                                                    "(discriminant a square, C12-P2/P3)",
                             kappa_support=list(f.kappa_support))
            out.append((g, i_f))
    return [o[0] for o in out], [o[1] for o in out]


SPLIT_PROPOSE = 0.05  # relative misfit below which a branch grouping is proposed (the evidence decides)


def _track_roots(f, kap):
    """Roots lam_i(kappa) of the monic factor f at xi = i kappa, ordered continuously along kappa
    (assignment of each kappa's roots to the previous kappa's). Returns (len(kap), m) complex."""
    from scipy.optimize import linear_sum_assignment

    m = max(a for a, _ in f.coef)
    c = {k: complex(v[0]) for k, v in f.coef.items()}
    lead = c[(m, 0)]
    out = []
    for kp in kap:
        xi_ = 1j * kp
        poly = [sum(v * xi_**b for (a, b), v in c.items() if a == aa) / lead for aa in range(m, -1, -1)]
        r = np.roots(poly)
        if len(r) < m:
            r = np.concatenate([r, np.full(m - len(r), np.nan + 0j)])
        if out:
            # assignment to the linear extrapolation of the branches (close, nearly parallel branches
            # are not swapped)
            prev = out[-1] if len(out) < 2 else 2 * out[-1] - out[-2]
            C = np.abs(prev[:, None] - r[None])
            C = np.where(np.isfinite(C), C, 1e300)
            _, col = linear_sum_assignment(C)
            r = r[col]
        out.append(r)
    return np.array(out)


# T103: the 90 % intervals of the factors of a split (split_branches) are those of the unsplit factor
# carried through the split map (Monte Carlo over its coefficient intervals, the grouping held fixed), not
# the zero-width (v, v, v) of a point split. An exact split (T80/T99) is not refined afterwards, so on
# scattered input (no bootstrap) its zero-width intervals were the reported ones (beam 400 5 % s0/s2:
# cover90 0.5). Default: on with PDEFACTOR_BRANCH_ARD (env PDEFACTOR_SPLIT_CI=0/1 overrides)
SPLIT_CI = os.environ.get("PDEFACTOR_SPLIT_CI", os.environ.get("PDEFACTOR_BRANCH_ARD", "0")) == "1"
_Z90 = 1.6448536269514722


def _poly_rows(R):
    """np.poly row by row: R (n, g) roots -> (n, g + 1) monic coefficients, highest degree first."""
    E = np.zeros((R.shape[0], R.shape[1] + 1), complex)
    E[:, 0] = 1.0
    for i in range(R.shape[1]):
        E[:, 1:i + 2] = E[:, 1:i + 2] - R[:, i:i + 1] * E[:, 0:i + 1]
    return E


def _split_part_intervals(f, kap, L, V, groups, parts, ndraw=200, seed=0):
    """T103: 90 % intervals of the coefficients of each part of a split of f (root groups `groups` of the
    branches L tracked on kap, Vandermonde V in i kappa), from ndraw draws of f's coefficients (normal,
    real and imaginary parts independent, sd = 90 % half width / z, as split_quadratics). In each draw
    the roots are matched to the central branches per kappa, each group's elementary symmetric functions
    are fitted on the central part's monomials, and the 5 / 95 % quantiles are read per coefficient
    (central value kept). Returns one {monomial: (v, lo, hi)} per part, or None when f has no finite
    widths or too few draws succeed."""
    from itertools import permutations

    m = max(a for a, _ in f.coef)
    med = {k: complex(v[0]) for k, v in f.coef.items()}
    sd = {}
    for k, v in f.coef.items():
        h = (complex(v[2]) - complex(v[1])) / (2 * _Z90)
        sd[k] = complex(abs(h.real), abs(h.imag)) if np.isfinite(h.real) and np.isfinite(h.imag) else 0j
    if not any(abs(h) > 0 for k, h in sd.items() if k != (m, 0)):
        return None
    rng = np.random.default_rng(seed)
    xs = 1j * np.asarray(kap)
    perms = np.array(list(permutations(range(m))))  # m <= M_LIMIT: brute-force matching of the roots
    draws = [[] for _ in parts]
    for _ in range(ndraw):
        c = {k: med[k] + (0j if k == (m, 0) else complex(sd[k].real * rng.standard_normal(),
                                                          sd[k].imag * rng.standard_normal())) for k in med}
        P = np.zeros((len(xs), m + 1), complex)  # P[:, a] = coefficient of tau^a
        for (a, b), v in c.items():
            P[:, a] += v * xs**b
        P = P / P[:, m:m + 1]
        C = np.zeros((len(xs), m, m), complex)  # companion matrices, roots = eigenvalues
        C[:, 0, :] = -P[:, m - 1::-1]
        if m > 1:
            C[:, np.arange(1, m), np.arange(m - 1)] = 1.0
        try:
            r = np.linalg.eigvals(C)
        except np.linalg.LinAlgError:
            continue
        if not np.all(np.isfinite(r)):
            continue
        cost = np.abs(L[:, None, :] - r[:, perms]).sum(-1)  # (nk, n_perm)
        Ld = r[np.arange(len(xs))[:, None], perms[np.argmin(cost, 1)]]
        for i_p, (grp, cf) in enumerate(zip(groups, parts)):
            E = _poly_rows(Ld[:, list(grp)])
            vals = {}
            for a in range(1, len(grp) + 1):
                bs = sorted(b for (aa, b) in cf if aa == len(grp) - a)
                if not bs:
                    continue
                cb, *_ = np.linalg.lstsq(V[:, bs], E[:, a], rcond=None)
                vals.update({(len(grp) - a, b): complex(v) for b, v in zip(bs, cb)})
            draws[i_p].append(vals)
    if min(len(d) for d in draws) < ndraw // 2:
        return None
    out = []
    for cf, ds in zip(parts, draws):
        ci = {}
        for k, v in cf.items():  # the monic leading term is not in the draws: kept as (1, 1, 1)
            arr = np.array([d[k] for d in ds if k in d])
            if not len(arr):
                continue
            lo = complex(min(np.quantile(arr.real, 0.05), v.real), min(np.quantile(arr.imag, 0.05), v.imag))
            hi = complex(max(np.quantile(arr.real, 0.95), v.real), max(np.quantile(arr.imag, 0.95), v.imag))
            ci[k] = (complex(v), lo, hi)
        out.append(ci)
    return out


def split_branches(factors, kband):
    """Generalised split of a factor of order m >= 2 in tau (v2.13 G4; C12-P2/P3 is the case m = 2):
    Q is reducible iff its root branches lam_i(kappa) fall into groups whose elementary symmetric
    functions are polynomials in xi. The branches are tracked on kappa in (0, kband], every grouping
    into two parts is tried, each part's symmetric functions are fitted as polynomials in xi of degree
    <= the factor's xi-degree (complex least squares), and the grouping with the smallest relative
    misfit is proposed when that misfit is below SPLIT_PROPOSE. The caller accepts it only by refined
    evidence - Occam term. Returns (new factor list, index of the source factor of each)."""
    from itertools import combinations

    out = []
    for i_f, f in enumerate(factors):
        m = max(a for a, _ in f.coef)
        if m < 2:
            out.append((f, i_f))
            continue
        dx = max(b for _, b in f.coef)
        nk = max(40, 8 * m * (dx + 1))
        kap = np.linspace(kband / nk, kband, nk)
        try:
            L = _track_roots(f, kap)
        except (np.linalg.LinAlgError, ValueError):
            out.append((f, i_f))
            continue
        if not np.all(np.isfinite(L)):
            out.append((f, i_f))
            continue
        V = np.vander(1j * kap, dx + 1, increasing=True)
        best = None
        for g in range(1, m // 2 + 1):
            for G in combinations(range(m), g):
                if 2 * g == m and 0 not in G:
                    continue
                H = tuple(i for i in range(m) if i not in G)
                parts, worst = [], 0.0
                for grp in (G, H):
                    E = np.array([np.poly(L[j, list(grp)]) for j in range(nk)])  # (nk, |grp| + 1), monic
                    cf = {}
                    for a in range(1, len(grp) + 1):
                        y = E[:, a]
                        c, *_ = np.linalg.lstsq(V, y, rcond=None)
                        # relative to the size of e_a (|lam|^a), not to e_a itself, which may vanish
                        scale = np.linalg.norm(np.abs(L[:, list(grp)]).max(1) ** a)
                        rel = np.linalg.norm(V @ c - y) / max(scale, 1e-300)
                        worst = max(worst, rel)
                        for b, cb in enumerate(c):
                            if abs(cb) > 1e-12 * max(np.abs(c).max(), 1e-300):
                                cf[(len(grp) - a, b)] = complex(cb)
                    cf[(len(grp), 0)] = 1.0 + 0j
                    parts.append(cf)
                if best is None or worst < best[0]:
                    best = (worst, parts, (G, H))
        if best is None or best[0] > SPLIT_PROPOSE:
            out.append((f, i_f))
            continue
        cis = _split_part_intervals(f, kap, L, V, best[2], best[1]) if SPLIT_CI else None
        for i_p, cf in enumerate(best[1]):
            coef = {k: (v, v, v) for k, v in cf.items()}
            if cis is not None:
                coef.update(cis[i_p])
            g = FactorReport(sp.expand(sum((v.real if abs(v.imag) < 1e-12 else v) * tau**a * xi**b
                                           for (a, b), v in cf.items())), f.W / 2, coef,
                             status=f"factor of the reducible factor {f.sympy} (root branches grouped, relative misfit "
                                    f"{best[0]:.2g}; C12-P2/P3 generalised)",
                             kappa_support=list(f.kappa_support))
            out.append((g, i_f))
    return [o[0] for o in out], [o[1] for o in out]


ALT_MIN_MASS = 1e-6  # pooled structures below this mass are not refined (the decider's own min_mass)
ALT_TOP = None  # optional cap on the refined alternatives (None = all; kept as a knob for the learned controller)
SPLIT_BEATS = os.environ.get("PDEFACTOR_SPLIT_BEATS", "1") == "1"  # T78 (adopted 2026-10-30; env =0 disables)
EXACT_SPLIT = os.environ.get("PDEFACTOR_EXACT_SPLIT", "1") == "1"  # T80 (adopted 2026-10-30; env =0 disables)
EPGP_REINTERP = os.environ.get("PDEFACTOR_EPGP_REINTERP", "0") == "1"  # P4 (off by default; interp/reinterp.py)
RAW_GOF = os.environ.get("PDEFACTOR_RAW_GOF", "1") == "1"  # T88 raw goodness of fit (adopted 2026-10-31; env =0 disables)
# T94 support path over the class xi-degree. T100: default = PDEFACTOR_BRANCH_ARD (off on main). T94 was not
# adopted because of E13 F2-2, where the newly reachable support won on the prior volume the per-bin scale
# charged to the true pair's unexcited branch (T97); the per-branch scales of T98 remove that charge. Without
# T94 a small high-xi-degree term the core rounded to 0 cannot return, and under BRANCH_ARD a law of higher
# time order (one more root branch, unpriced) takes its place (E13 F1-3 grid 1 %: a 5-term tau^2 law at branch
# evidence 15793.9 vs the true tau + 1.51e-4 xi^4 - 2.28e-3 xi^3 at 15849.8, never offered). Env PDEFACTOR_PATH_CLASS=0/1 overrides
PATH_CLASS = os.environ.get("PDEFACTOR_PATH_CLASS", os.environ.get("PDEFACTOR_BRANCH_ARD", "1")) == "1"
# T96: smooth residual test of the reported law on a real noisy grid (validate.smooth_gof_log10p);
# adopted 2026-10-31 (downgrade only; no false alarm on 150 fresh true-law draws nor on stored right rows); env =0 disables
GRID_SMOOTH_GOF = os.environ.get("PDEFACTOR_GRID_SMOOTH_GOF", "1") == "1"
# T97 fit guard (off): a refinement-stage model change (split over C reverted, merge, branch split,
# refined alternative, P4 re-interpolation) must also not lose on the plug-in fit scored with the same
# Occam unit (Schwarz: 0.5 chi^2 + 0.5 log n per real coefficient AND per real amplitude, excited bins
# only; refine_raw.fit_excited). "1": such a change is refused and the current model kept; "2": refused,
# and the label becomes UNDECIDED (the kernel evidence and the fit disagree: the data do not decide)
FIT_GUARD = os.environ.get("PDEFACTOR_FIT_GUARD", "0")
# T97 (off): the refined alternatives also come from the PRE-regroup pooled structure posterior (mass >=
# ALT_MIN_MASS), not only from the decider's scored list and the post-regroup posterior (which the regroup
# concentrates on one structure); suggested by the t95 diagnosis of F4-128 grid 5 %
ALT_PRE = os.environ.get("PDEFACTOR_ALT_PRE", "0") == "1"


def _fit_score(factors, obs, kmax, occ):
    """T97: Schwarz score of the plug-in fit of a factor set on the observations' excited bins:
    -(0.5 chi^2) - occ (real coefficients, a conjugate pair counted once, + real amplitudes)."""
    from .refine_raw import fit_excited

    nll, r = fit_excited([_poly_symbol(_sympy_of(f)) for f in factors], obs, kmax)
    return -nll - occ * (_supports(factors)[1] + r)


def _fit_guard(new, cur, obs, kmax, occ, log=None):
    """T97: True when the model change cur -> new passes the fit guard (always with FIT_GUARD off): the
    new model's plug-in Schwarz score is not below the current one's by more than LOG_BF_BARE nats (the
    bare-mention band of _beats). A refused change is appended to `log` as (new score, current score)."""
    if FIT_GUARD not in ("1", "2"):
        return True
    try:
        s_new, s_cur = _fit_score(new, obs, kmax, occ), _fit_score(cur, obs, kmax, occ)
    except (np.linalg.LinAlgError, ValueError, ZeroDivisionError):
        return True
    ok = bool(s_new >= s_cur - LOG_BF_BARE)
    if log is not None and not ok:
        log.append((float(s_new), float(s_cur)))
    return ok
# T98: the complex-coefficient rerun of a real field fits the half plane kappa > 0 only (Hermitian FFT:
# the kappa < 0 modes are the mirror) and reports lcm(A, conj A) (off by default; structfit.half_plane)
CONJ_HALF = os.environ.get("PDEFACTOR_CONJ_HALF", "1") == "1"  # T98 adopted 2026-11-01 (bundle A/B v5); env =0 disables


def _same_product(a, b, rtol=1e-9):
    """The expanded products of two factor lists agree coefficient by coefficient to rounding
    (relative to the largest coefficient): an exact refactorisation of the same symbol."""
    pa = _coef_dict(sp.expand(sp.Mul(*[_sympy_of(f) for f in a])))
    pb = _coef_dict(sp.expand(sp.Mul(*[_sympy_of(f) for f in b])))
    s = max([abs(v) for v in list(pa.values()) + list(pb.values())] + [1e-300])
    return all(abs(pa.get(k, 0) - pb.get(k, 0)) <= rtol * s for k in set(pa) | set(pb))


# T99: an exact split (T80) is repeated until no factor splits exactly any more, so the report is the
# finest factorisation of the same symbol (over C, closed under conjugation for a real field: C12-T1).
# A single grouping step can stop half way: tau^3 + c tau xi^4 = tau (tau^2 + c xi^4) is proposed as
# {tau} | {tau^2 + c xi^4}, whose quadratic is itself (tau - i sqrt(c) xi^2)(tau + i sqrt(c) xi^2).
# Default: on with PDEFACTOR_BRANCH_ARD (env PDEFACTOR_SPLIT_FINEST=0/1 overrides)
SPLIT_FINEST = os.environ.get("PDEFACTOR_SPLIT_FINEST",
                              os.environ.get("PDEFACTOR_BRANCH_ARD", "1")) == "1"

# T101: T88 (raw goodness of fit) tests the factor set at the label step, but the split layer's subset
# evidence (computed on the interpolated samples) can afterwards drop factors and, when the dropped one
# carried the ID-KER status, turn the label into FIT-COMPATIBLE: the reported law was then never tested on
# the raw points (F4-209 400 5 %: the one kept factor has raw log10 p = -inf, log evidence -1528.7 vs
# 122.8 for the truth). With RAW_GOF_FINAL a drop that would leave a claimed (FIT-COMPATIBLE) law is
# checked on the raw observations: if the reduced law fails T88 while the full set passes, the raw data
# contradict the premise of the drop (the dropped kernels do explain data) and the drop is refused; if
# both fail, the drop stands and the law is not claimed (MISFIT, as T88). Scattered inputs only (known
# sigma). Default: on with PDEFACTOR_BRANCH_ARD (env PDEFACTOR_RAW_GOF_FINAL=0/1 overrides)
RAW_GOF_FINAL = os.environ.get("PDEFACTOR_RAW_GOF_FINAL",
                               os.environ.get("PDEFACTOR_BRANCH_ARD", "1")) == "1"


# T102: support_path's backward elimination appended each support AFTER a removal, so the full rectangular
# support it starts from (every tau^a xi^b, a < m, b <= the path's xi-degree) was never a candidate of
# refine: a factor whose true support is the full class could not be reported (E13 F4-128 grid 5 %: truth
# tau + 3.27 - 0.0788 xi - 0.00704 xi^2 + 0.00162 xi^3 + 0.000242 xi^4 needs all five terms; the path began
# at {1, xi, xi^2, xi^4}; the true pair refined scores 7171.6 vs 7162.5 for the reported law in branch
# evidence - Occam). With PATH_FULL the full support is the first (largest) element of every path; refine's
# evidence - Occam still decides. Default: on with PDEFACTOR_BRANCH_ARD (env PDEFACTOR_PATH_FULL=0/1 overrides)
PATH_FULL = os.environ.get("PDEFACTOR_PATH_FULL", os.environ.get("PDEFACTOR_BRANCH_ARD", "1")) == "1"


def _raw_gof_of(exprs, raw):
    """T88 statistic (log10 p, kmax) of sympy factors on the raw observations."""
    from .raw_gof import raw_gof_log10p

    return raw_gof_log10p([_poly_symbol(q) for q in exprs], raw)


def subset_drop_gof(full_law, sub_law, raw):
    """T101 decision on a subset drop that would leave a claimed law: "drop" (the reduced law passes T88),
    "keep_all" (it fails while the full set passes: the drop is refused) or "misfit" (both fail).
    Returns (verdict, log10 p reduced, kmax, log10 p full or None)."""
    lp_sub, k_sub = _raw_gof_of(sub_law, raw)
    if lp_sub >= PRED_LOGP:
        return "drop", lp_sub, k_sub, None
    lp_full, _ = _raw_gof_of(full_law, raw)
    return ("keep_all" if lp_full >= PRED_LOGP else "misfit"), lp_sub, k_sub, lp_full


def _split_exact_finest(factors, src, kband, real):
    """Repeat split_branches on an exact split (factors, src: index of the source factor of each) while
    the proposals multiply back to the current factors to rounding (_same_product) and, for a real field,
    stay closed under conjugation; returns the finest (factors, src). Each step is the same kernel
    (C12-T1), so no evidence is involved."""
    for _ in range(M_LIMIT):
        props, s2 = split_branches(factors, kband)
        if len(props) <= len(factors) or not _same_product(props, factors) or (real and not _conj_closed(props)):
            break
        factors, src = props, [src[i] for i in s2]
    return factors, src


def _structure(factors):
    return tuple(sorted((max(a for a, _ in f.coef), max(b for _, b in f.coef)) for f in factors))


def _beats(sc, p, cur, p_cur):
    """A refined model (score sc = evidence - Occam, p real parameters of its product) displaces the
    current one (cur, p_cur) only on evidence: a gap of at most LOG_BF_BARE nats is not worth a bare
    mention (Kass & Raftery 1995), and within it the model with fewer real parameters is kept (T74)."""
    if sc > cur + LOG_BF_BARE:
        return True
    return sc > cur - LOG_BF_BARE and p < p_cur


def _refine_alternatives(factors, evidence, pooled, samples, pis, t, x, sigma, bounds, refine, nd, obs, kmax, occ,
                         cur, u_ref, glog=None, pre=None):
    """Refine every other structure the decider scored and every pooled structure with mass >=
    ALT_MIN_MASS (decider evidence first, then pooled mass) on the observations (accuracy first: a
    fixed search width missed the right structure when the decider's pick was poor); return (factors, structure, score) of the best one if its refined evidence - Occam
    term beats cur by _beats, else None."""
    st0 = _structure(factors)
    order = [s for s, _ in sorted((evidence or {}).items(), key=lambda kv: -kv[1])]
    order += [s for s, w in sorted(pooled.items(), key=lambda kv: -kv[1]) if s not in order and w >= ALT_MIN_MASS]
    if ALT_PRE and pre:  # T97: the pre-regroup pooled posterior too (the regroup leaves one structure)
        order += [s for s, w in sorted(pre.items(), key=lambda kv: -kv[1]) if s not in order and w >= ALT_MIN_MASS]
    alts = [s for s in order if s != st0][:ALT_TOP]
    sup0 = _supports(factors)
    p0 = _n_real_params(factors)
    best = None
    ndh = None if nd is None else nd / np.sqrt(2)
    for st in alts:
        try:
            _, aa = _run(samples, pis, t, x, sigma, bounds, refine, structures=[st], noise_draws=nd)
            pk = _p_k(aa)
            if pk:
                _merge_tracks(aa, max(pk, key=pk.get))
            fa = [fr for _, fr in _factor_reports(aa)]
            if not fa:
                continue
            if np.isrealobj(samples[0]):
                conjugate_closure(fa)
            cand = support_path(fa, u_ref, t, x, sigma, ndh, dx_class=bounds[1])
            ra = refine_factors(fa, obs, kmax, candidates=cand)
        except (np.linalg.LinAlgError, ValueError, ZeroDivisionError):
            continue
        sc = ra["logev"] - occ * ra["p"]
        kept = [fa[j] for j in ra["active"]]
        if _supports(kept) == sup0:
            continue        # same model after support selection: a score gap is optimiser noise
        if _beats(sc, _n_real_params(kept), cur, p0) and (best is None or sc > best[2]) and \
                _fit_guard(kept, factors, obs, kmax, occ, glog):  # T97 (off by default)
            best = (kept, st, sc)
    return best


class _ReportSymbol:
    """A FactorReport seen as a core symbol (m, roots in tau at xi = xi0), for core criteria that are
    re-evaluated on the final, refined factors."""

    def __init__(self, f):
        self.m = max(a for a, _ in f.coef)
        self._f = f

    def roots(self, xi0):
        c = [0j] * (self.m + 1)
        for (a, b), v in self._f.coef.items():
            c[self.m - a] += complex(v[0]) * xi0**b
        return np.roots(c)


# T103 (b): the core labels a sample ID-KER when one of ITS factors fails its identifiability test
# (structfit: m (dx + 1) + 1 modes, dx + 1 distinct |kappa|, m modes at one kappa, II-C1). When the reported
# factors are not the core's (refined, merged, split, another structure), that verdict is about a law that is
# not reported (beam 400 5 % s1: the core's tau^3 + c tau xi^4 has an unexcited third branch, II-C1 fails;
# the reported pair tau -+ i sqrt(c) xi^2 passes), so the test is re-run on the reported factors. Default: on
# with PDEFACTOR_BRANCH_ARD (env PDEFACTOR_IDKER_FINAL=0/1 overrides)
IDKER_FINAL = os.environ.get("PDEFACTOR_IDKER_FINAL", os.environ.get("PDEFACTOR_BRANCH_ARD", "0")) == "1"


def _identified(factors, counts):
    """T103 (b): every factor passes the core's identifiability test (structfit.analyze_structured: n >=
    m (dx + 1) + 1 modes, >= dx + 1 distinct |kappa|, >= m modes at one kappa) on its observed modes.
    counts: per factor {signed kappa: modes}; a real field's -kappa modes mirror +kappa, so each |kappa|
    counts max(n(+kappa), n(-kappa)), never their sum."""
    for f, cnt in zip(factors, counts):
        m = max(a for a, _ in f.coef)
        dx = max((b for (_, b), v in f.coef.items() if abs(complex(v[0])) > 0), default=0)
        per = {}
        for k, n in cnt.items():
            per[abs(k)] = max(per.get(abs(k), 0), int(n))
        if not per or sum(per.values()) < m * (dx + 1) + 1 or len(per) < dx + 1 or max(per.values()) < m:
            return False
    return True


def _conj_means(a, b, rtol=1e-6):
    """b's coefficients are the conjugates of a's (point values, relative to the largest): an exact pair
    (refine ties a real field's conjugates, conjugate_closure and exact splits conjugate to rounding)."""
    keys = set(a.coef) | set(b.coef)
    z = (0j, 0j, 0j)
    scale = max([abs(complex(c[0])) for c in list(a.coef.values()) + list(b.coef.values())] + [1e-300])
    return max(abs(np.conj(complex(a.coef.get(k, z)[0])) - complex(b.coef.get(k, z)[0])) for k in keys) <= rtol * scale


def _conj_shared_support(factors, sup):
    """T103 (c): a non-real factor of a real field and its conjugate partner get the union of their kappa
    supports (the -kappa mirror of A's modes lies on conj A, so conj A is determined wherever A is)."""
    out = [list(ks) for ks in sup]
    for j, f in enumerate(factors):
        if not _nonreal(f):
            continue
        for i, g in enumerate(factors):
            if i != j and _conj_means(f, g):
                out[j] = sorted(set(out[j]) | set(sup[i]))
    return out


def _relabel_branch_points(res, factors, sup, T):
    """Label masses of the core results with each sample's confluent bins re-checked against the final
    factors by the core's own branch-point criterion (structfit._branch_point). The core labels a
    sample UNDECIDED when a confluent bin is not explained by ITS factors; a first fit (e.g. a pair of
    complex first-order factors approximating an irreducible real quadratic) cannot carry a branch
    point, the refined factor can. A sample whose every confluent bin is a branch point of a final
    factor is relabelled as the core would have (MISFIT by its outlier fraction, else FIT-COMPATIBLE;
    single-|kappa| factors become ID-KER below). A repeated factor has close roots at every kappa and
    stays UNDECIDED (OPF5B-T6)."""
    from types import SimpleNamespace

    from .core.structfit import _branch_point

    misfit = analyze_structured.__kwdefaults__["outlier_frac_misfit"]

    syms = [_ReportSymbol(f) for f in factors]
    if len(factors) > 1:  # roots of different factors meeting (a shared mode, e.g. a conjugate pair at kappa = 0):
        # the product of distinct factors is squarefree, so its roots meet at a few kappa only (same criterion)
        cd = _coef_dict(sp.expand(sp.Mul(*[_sympy_of(f) for f in factors])))
        syms.append(_ReportSymbol(FactorReport(None, 0.0, {k: (v, v, v) for k, v in cd.items()})))
    ks = np.array(sorted({float(k) for s in sup for k in s}))
    if not len(ks):
        return _label_masses(res)
    modes = SimpleNamespace(kappa=ks)
    labs = {}
    for r, p in res:
        lab = r.label
        if lab == "UNDECIDED" and r.confluent and all(_branch_point(c, syms, modes, T) for c in r.confluent):
            lab = "MISFIT" if r.info.get("outlier_fraction", 0.0) > misfit else "FIT-COMPATIBLE"
        labs[lab] = labs.get(lab, 0.0) + p
    return labs


def _label_masses(res):
    labs = {}
    for r, p in res:
        labs[r.label] = labs.get(r.label, 0.0) + p
    return labs


def _supports(factors):
    """Model signature of a factor set: the monomials (and real / imaginary parts) of the expanded
    product, and the number of free real parameters (a conjugate pair counted once: its factors share
    them). ker of the product is the sum of the factors' kernels (C12-T1), so two sets with the same
    signature are the same model family, whatever structure label or factorisation produced them
    (e.g. a conjugate pair and its real product, T66)."""
    cd = _coef_dict(sp.expand(sp.Mul(*[_sympy_of(f) for f in factors])))
    m = max(k[0] for k in cd)
    lead = cd.pop((m, 0), 1.0)
    sc = 1e-9 * max([abs(v / lead) for v in cd.values()] + [1.0])
    sup = tuple(sorted((k, abs((v / lead).real) > sc, abs((v / lead).imag) > sc) for k, v in cd.items()
                       if abs(v / lead) > sc))
    p = sum(_n_params(f) for f in factors)
    left = [j for j, f in enumerate(factors) if _nonreal(f)]
    while left:
        j = left.pop(0)
        hit = next((i for i in left if _conj_pair(factors[j], factors[i])), None)
        if hit is not None:
            left.remove(hit)
            p -= _n_params(factors[j])
    return sup, p


def _n_params(f):
    """Real parameters of a factor report: non-zero real / imaginary parts of its non-leading
    coefficients (the support the refinement kept)."""
    m = max(a for a, _ in f.coef)
    return sum((complex(c[0]).real != 0) + (complex(c[0]).imag != 0) for k, c in f.coef.items() if k != (m, 0))


def _n_real_params(factors):
    """Real parameters of the expanded product of the factors (non-leading coefficients; real and
    imaginary parts counted separately when non-zero relative to the coefficient scale)."""
    cd = _coef_dict(sp.expand(sp.Mul(*[_sympy_of(f) for f in factors])))
    m = max(k[0] for k in cd)
    lead = cd.pop((m, 0), 1.0)
    sc = 1e-9 * max([abs(v / lead) for v in cd.values()] + [1.0])
    return sum((abs((v / lead).real) > sc) + (abs((v / lead).imag) > sc) for v in cd.values())


def _conj_closed(factors):
    """Every non-real factor has a conjugate partner in the list (a real field's annihilator is closed
    under conjugation, T53)."""
    left = [j for j, f in enumerate(factors) if _nonreal(f)]
    while left:
        j = left.pop(0)
        hit = next((i for i in left if _conj_pair(factors[j], factors[i])), None)
        if hit is None:
            return False
        left.remove(hit)
    return True


def _refine_merges(factors, u_ref, t, x, sigma, ndh, obs, kmax, occ, cur, glog=None):
    """G3 at the refinement stage: two units (a real factor, or a conjugate pair of a real field) are
    replaced by their product, whose support is chosen along its mode-level path and refined on the
    observations; the best merge is returned as (factors, score) if its evidence - Occam term beats
    cur (an irreducible law that the core read as a near-reducible product). Greedy: repeated while a
    merge improves."""
    from itertools import combinations

    real = bool(np.isrealobj(obs["ys"]))
    best = None
    cur_f = factors
    while len(cur_f) > 1:
        units, used = [], set()
        for j, f in enumerate(cur_f):
            if j in used:
                continue
            grp = [j]
            if real and _nonreal(f):
                i = next((i for i in range(j + 1, len(cur_f)) if i not in used and _conj_pair(f, cur_f[i])), None)
                if i is None:
                    grp = None  # a lone complex factor: its product is not real
                else:
                    grp.append(i)
            used.update(grp or [j])
            if grp:
                units.append(grp)
        step = None
        for a, b in combinations(range(len(units)), 2):
            idx = units[a] + units[b]
            q = sp.expand(sp.Mul(*[_sympy_of(cur_f[i]) for i in idx]))
            cd = _coef_dict(q)
            if real:
                cd = {k: complex(v.real, 0.0) for k, v in cd.items() if v.real != 0.0}
            m = max(k[0] for k in cd)
            if m > M_LIMIT or max(k[1] for k in cd) > DX_LIMIT:
                continue
            lead = cd[(m, 0)]
            cd = {k: v / lead for k, v in cd.items()}
            new = FactorReport(sum((tau**k[0] * xi**k[1] * v for k, v in cd.items()), sp.Integer(0)),
                               sum(cur_f[i].W for i in idx), {k: (v, v, v) for k, v in cd.items()},
                               status="merged: product of two factors refined as one")
            trial = [copy.deepcopy(f) for i, f in enumerate(cur_f) if i not in idx] + [new]
            try:
                cand = support_path(trial, u_ref, t, x, sigma, ndh)
                ro = refine_factors(trial, obs, kmax, candidates=cand)
            except (np.linalg.LinAlgError, ValueError, ZeroDivisionError):
                continue
            sc = ro["logev"] - occ * ro["p"]
            kept = [trial[j] for j in ro["active"]]
            if sc > cur and (step is None or sc > step[1]) and _fit_guard(kept, cur_f, obs, kmax, occ, glog):
                step = (kept, sc)
        if step is None:
            break
        cur_f, cur = step
        best = step
    return best


def _grid_obs(u, t, x, sigma):
    """Every point of a periodic grid as an observation set for the refinement pass."""
    TT, XX = np.meshgrid(t - t[0], x, indexing="ij")
    u = np.asarray(u)
    return dict(ts=TT.ravel(), xs=XX.ravel(), ys=u.ravel(), period=(x[1] - x[0]) * len(x), sigma=float(sigma),
                grid=dict(t=t - t[0], nx=len(x), Y=np.fft.fft(u, axis=1) / np.sqrt(len(x))))


def conjugate_closure(factors):
    """A real field's annihilator is closed under complex conjugation, so with the split over C
    (C12-T1) every factor with non-real coefficients comes with its conjugate. A lone complex factor
    gets its conjugate added (coefficients and intervals conjugated). In place; returns the indices of
    the factors whose conjugate was added."""
    add, src = [], []
    for i, f in enumerate(factors):
        if not _nonreal(f):
            continue
        if any(g is not f and _conj_pair(f, g) for g in factors + add):
            continue
        cc = {k: (np.conj(c[0]), complex(c[1].real, -c[2].imag), complex(c[2].real, -c[1].imag))
              for k, c in f.coef.items()}
        g = FactorReport(sp.expand(sum(c[0] * tau**a * xi**b for (a, b), c in cc.items())), f.W, cc, status="added: complex conjugate of a lone complex factor of a real field "
                                         "(conjugation-closed annihilator, C12-T1)",
                         kappa_support=list(f.kappa_support))
        add.append(g)
        src.append(i)
    factors.extend(add)
    return src


# ------------------------------------------------------------------ the loop
def run_loop(samples, t, x, sigma, pis=None, *, bounds=START_BOUNDS, refine=False, grow=True,
             regroup=True, recurse=True, max_depth=2, report_domain=False, subdomains=False, noise_draws=None,
             split=True, decide=True, raw=None, bootstrap=0, refine_obs=True, _depth=0):
    """samples: posterior interpolant samples on the grid (S-INTERP, or aggregate.fake_posterior);
    pis: their weights. sigma: white noise std of the samples. noise_draws: draws (R, nt, nx) of
    their correlated error, e.g. sqrt(2) (samples - posterior mean) for GP samples (the core then
    fits each bin by GLS). raw: optional dict(ts, xs, ys, period, sigma) of the scattered observations
    behind the samples; the structure decider and the final factor subset are then scored on them
    (no interpolation artifacts). bootstrap: with one sample (a noisy grid) and white noise sigma,
    the number of parametric-bootstrap refits for the coefficient intervals (bootstrap_intervals;
    0 = off). Returns LoopResult. The caller's raw dict is not modified: the per-observation-set memos
    (refine_raw: _excited, _lts warm starts) live in a per-call shallow copy, so a call's result does
    not depend on earlier calls (T92)."""
    if raw is not None:  # T92: memos stay inside this call; stale ones from an earlier call are dropped
        raw = {k: v for k, v in raw.items() if not str(k).startswith("_")}
    pis = np.full(len(samples), 1.0 / len(samples)) if pis is None else np.asarray(pis, float)
    nd = noise_draws
    boot_kmax = None  # set when the factors are refined on a grid (bootstrap of that estimator)
    res, agg = _run(samples, pis, t, x, sigma, bounds, refine, noise_draws=nd)
    history = [Level(bounds, _p(agg, ["FIT-COMPATIBLE"]))]
    note = ""

    # 1. degree growth with the held-out guard
    if grow:
        opts = _grow_options(bounds)
        u_mean = None
        _attach(res, samples)
        lp = _pred_logp(res, t, x, sigma, nd)
        und = lambda a: GROW_PAST and _p(a, ["UNDECIDED"]) > 0.5  # noqa: E731  P3 trigger (off by default)
        sc_cur = None
        while opts and (_p(agg, ["MISFIT", "ID-KER"]) > 0.5 or lp < PRED_LOGP or und(agg)):
            fits = []
            for ob in opts:
                r_o, a_o = _run(samples, pis, t, x, sigma, ob, refine, noise_draws=nd)
                _attach(r_o, samples)
                fits.append((ob, r_o, a_o, _pred_logp(r_o, t, x, sigma, nd)))
            # more FIT-COMPATIBLE mass first, then the better predictive fit
            nb, r2, a2, lp2 = max(fits, key=lambda f: (_p(f[2], ["FIT-COMPATIBLE"]), f[3]))
            lev = Level(nb, _p(a2, ["FIT-COMPATIBLE"]), accepted=False)
            gain_fit = lev.p_fit > _p(agg, ["FIT-COMPATIBLE"])
            gain_pred = lp < PRED_LOGP and lp2 > lp + 3.0 and lev.p_fit >= _p(agg, ["FIT-COMPATIBLE"])
            gain_ev = False
            if und(agg) and not (gain_fit or gain_pred) and lev.p_fit >= _p(agg, ["FIT-COMPATIBLE"]):
                # P3: an UNDECIDED (confluent) level grows only on refined evidence - Occam (_beats, T74)
                if sc_cur is None:
                    sc_cur = _level_score(agg, samples, pis, t, x, sigma, nd, raw)
                sc2 = _level_score(a2, samples, pis, t, x, sigma, nd, raw)
                gain_ev = (sc2[0] is not None and sc_cur[0] is not None
                           and _beats(sc2[0], sc2[1], sc_cur[0], sc_cur[1]))
            if gain_fit or gain_pred or gain_ev:
                u_mean = _mean_sample(samples, pis) if u_mean is None else u_mean
                h_old = heldout_score(u_mean, t, x, sigma, bounds, refine, noise_draws=nd)
                lev.heldout = heldout_score(u_mean, t, x, sigma, nb, refine, noise_draws=nd)
                # keep the larger class only if it predicts held-out modes no worse than the
                # smaller one, within two standard errors of the difference
                if lev.heldout[0] <= h_old[0] + 2 * np.hypot(lev.heldout[1], h_old[1]):
                    lev.accepted = True
                    res, agg, bounds, lp = r2, a2, nb, lp2
                    sc_cur = sc2 if gain_ev else None
                else:
                    lev.note = (f"rejected: held-out score {lev.heldout[0]:.3g} worse than {h_old[0]:.3g} "
                                "(overfit guard)")
            else:
                lev.note = "rejected: no gain in FIT-COMPATIBLE mass nor in the predictive fit (V0.1)"
            history.append(lev)
            opts = _grow_options(nb)
        if GROW_PAST and lp < PRED_LOGP and not _grow_options(bounds):
            res, agg, bounds, lp = _grow_past(samples, pis, t, x, sigma, bounds, refine, nd, raw, res, agg, lp,
                                              history)

    # 2. structure decided by data-level evidence (v2.9 #2(c)), then regroup at it
    pooled_pre = dict(agg.structures_pooled or {})  # T97: the refined alternatives may also draw from it
    regrouped = False
    evidence = None
    if regroup and decide and agg.structures_pooled and len(agg.structures_pooled) > 1:
        u_mean = _mean_sample(samples, pis)
        s_ev, evidence = decide_structure(u_mean, t, x, sigma, agg.structures_pooled, bounds, refine,
                                          None if nd is None else nd / np.sqrt(2), raw=raw)
        s_map = max(agg.structures_pooled, key=agg.structures_pooled.get)
        npar = lambda st: sum(m * (dx + 1) for m, dx in st)  # noqa: E731
        if raw is None and s_ev is not None and s_ev != s_map and npar(s_ev) > npar(s_map):
            # overfit guard (v2.9 #5): a richer symbol than the mode-level MAP must predict held-out
            # (later-time) modes no worse, within two standard errors; with few observed kappa a
            # high-degree symbol interpolates the modes and fits their noise
            ndh = None if nd is None else nd / np.sqrt(2)
            h_ev = heldout_score(u_mean, t, x, sigma, bounds, refine, noise_draws=ndh, structures=[s_ev])
            h_map = heldout_score(u_mean, t, x, sigma, bounds, refine, noise_draws=ndh, structures=[s_map])
            if h_ev[0] > h_map[0] + 2 * np.hypot(h_ev[1], h_map[1]):
                note += (f"data-level evidence preferred {s_ev}, rejected by the held-out guard "
                         f"({h_ev[0]:.3g} vs {h_map[0]:.3g} for {s_map}). ")
                s_ev = s_map
        if s_ev is not None and agg.structures_pooled.get(s_ev, 0.0) < P_CONCENTRATED:
            res, agg = _run(samples, pis, t, x, sigma, bounds, refine, structures=[s_ev], noise_draws=nd)
            regrouped = True
            note += f"structure {s_ev} chosen by data-level evidence; all samples regrouped at it. "
    p_k = _p_k(agg)
    if regroup and not regrouped and p_k and agg.structures_pooled:
        k_star = max(p_k, key=p_k.get)
        st_k = {s: p for s, p in agg.structures_pooled.items() if len(s) == k_star}
        if st_k and p_k[k_star] >= P_CONCENTRATED:
            s_star = max(st_k, key=st_k.get)
            if agg.structures_pooled[s_star] < P_CONCENTRATED:
                res, agg = _run(samples, pis, t, x, sigma, bounds, refine, structures=[s_star], noise_draws=nd)
                regrouped = True
                note += f"regrouped all samples at k={k_star} with structure {s_star}. "

    # 3. recursion per factor group
    p_k = _p_k(agg)
    if p_k:
        _merge_tracks(agg, max(p_k, key=p_k.get))
    if raw is not None and _depth == 0:
        n_out = screen_samples(agg, raw, _mean_sample(samples, pis), t, x, sigma,
                               None if nd is None else nd / np.sqrt(2))
        if n_out:
            note += (f"{n_out} sample fit(s) rejected very strongly by the raw observations (a local optimum of "
                     "the per-sample fit) carry no weight in the pooled coefficients. ")
    reports = _factor_reports(agg)
    factors = []
    if recurse and len(reports) > 1 and _depth < max_depth:
        for j, fr in reports:
            comps, cp = _track_components(res, agg, j)
            if len(comps) == 0:
                factors.append(fr)
                continue
            comps = [c.real for c in comps] if np.isrealobj(samples[0]) else comps
            child = run_loop(comps, t, x, sigma, cp, bounds=bounds, refine=refine, grow=False, regroup=regroup,
                             recurse=True, max_depth=max_depth, noise_draws=nd, _depth=_depth + 1)
            kc = max(child.p_k, key=child.p_k.get) if child.p_k else 0
            if kc == 1 or len(child.factors) <= 1:
                fr.status = f"clean (component alone: k=1, label {child.label})"
                factors.append(fr)
            elif not all(_distinct(a, b) for i, a in enumerate(child.factors) for b in child.factors[i + 1:]):
                # the children are not told apart by their own posterior: one factor fitted twice
                fr.status = f"clean (component alone splits into {len(child.factors)} indistinguishable factors)"
                factors.append(fr)
            else:
                fr.status = f"split by recursion into {len(child.factors)}"
                fr.children = child.factors
                factors.extend(child.factors)
    else:
        factors = [fr for _, fr in reports]

    labs = agg.labels
    best_label = max(labs, key=labs.get) if labs else "UNDECIDED"
    idker_set = False
    if _depth == 0 and factors:
        u_ref = _mean_sample(samples, pis)
        # with raw observations the factor subset is decided on them below; else at the mode level here
        sup, red = kappa_support(u_ref, t, x, sigma, [_sympy_of(f) for f in factors],
                                 None if nd is None else nd / np.sqrt(2),
                                 weights=None if raw is not None else [f.W for f in factors],
                                 signed=not np.isrealobj(samples[0])) if raw is None else (
            kappa_support(u_ref, t, x, sigma, [_sympy_of(f) for f in factors],
                          None if nd is None else nd / np.sqrt(2), signed=not np.isrealobj(samples[0])), [])
        if red:
            for j in red:
                factors[j].status += "; dropped: redundant (its modes lie on another factor's variety)"
            dropped_modes = [factors[j] for j in red]
            sup = [ks for j, ks in enumerate(sup) if j not in red]
            factors = [f for j, f in enumerate(factors) if j not in red]
            note += f"{len(red)} redundant factor(s) dropped (modes explained by another factor). "
        else:
            dropped_modes = []
        # a factor with no observed mode within z sigma_lam of its variety explains nothing in the data
        # (with raw data the mode-level redundancy test above is skipped, so it is caught here); it must
        # go before the complex rerun, which compares factor counts
        empty = [j for j, ks in enumerate(sup) if not ks] if len(factors) > 1 else []
        if empty and len(empty) < len(factors):
            for j in empty:
                factors[j].status += "; dropped: no observed mode lies on its variety"
            dropped_modes = dropped_modes + [factors[j] for j in empty]
            sup = [ks for j, ks in enumerate(sup) if j not in empty]
            factors = [f for j, f in enumerate(factors) if j not in empty]
            note += f"{len(empty)} factor(s) without observed modes dropped. "
        pre_c = None
        # 4. real field with a factor of order m >= 2 in tau: it may split over C into a conjugate pair
        # (beam: tau^2 + c^2 xi^4 = (tau - i c xi^2)(tau + i c xi^2)). The factor split of ker P is over C
        # (C12-T1), so the core is rerun with complex coefficients and its own structure posterior decides
        if (np.isrealobj(samples[0]) and factors
                and any(max(a for a, _ in f.coef) >= 2 for f in factors)):
            rc, ac = _run(samples, pis, t, x, sigma, bounds, refine, noise_draws=nd, real=False,
                          **({"half": True} if CONJ_HALF else {}))
            p_more = sum(p for s_, p in ac.structures_pooled.items() if len(s_) > len(factors))
            pk_c = _p_k(ac)
            if CONJ_HALF:
                crep = _half_plane_reports(ac, len(factors)) if pk_c else None
                if crep is not None:
                    pre_c = dict(factors=copy.deepcopy(factors), sup=list(sup), res=res, agg=agg, labs=labs,
                                 best_label=best_label)
                    factors = crep
                    labs = ac.labels
                    best_label = max(labs, key=labs.get) if labs else "UNDECIDED"
                    note += ("the complex-coefficient run on the half plane kappa > 0 (the kappa < 0 modes of a real "
                             "field are its mirror) gives non-real factors; their conjugates complete the real "
                             "annihilator lcm(A, conj A). ")
                    res, agg = rc, ac
                    sup = kappa_support(u_ref, t, x, sigma, [_sympy_of(f) for f in factors],
                                        None if nd is None else nd / np.sqrt(2))
            elif p_more >= 0.5 and pk_c:
                _merge_tracks(ac, max(pk_c, key=pk_c.get))
                crep = [fr for _, fr in _factor_reports(ac)]
                n_pairs = sum(1 for s_ in [max(ac.structures_pooled, key=ac.structures_pooled.get)]
                              for _ in s_) - len(factors)
                if n_pairs >= 1:  # real factors became conjugate pairs: pool each pair in one orientation
                    n_c = max(n_pairs, sum(1 for fr in crep if _nonreal(fr)) // 2)
                    crep = _canonical_conj_reports(ac, n_c) or crep
                # only a split over C is new here: a split into real factors was already scored by the
                # real run and the data-level decider (telegraph ~ two damped transports)
                nonreal = [a for a in crep if _nonreal(a)]
                if nonreal and all(any(_conj_pair(a, b) for b in crep) for a in nonreal):
                    pre_c = dict(factors=copy.deepcopy(factors), sup=list(sup), res=res, agg=agg, labs=labs,
                                 best_label=best_label)
                    for fr in crep:
                        cplx = _nonreal(fr)
                        fr.status = ("factor over C (complex-coefficient run; one of a conjugate pair)" if cplx else
                                     "factor of a reducible order-2 real factor (split by the complex-coefficient run)")
                    factors = crep
                    labs = ac.labels
                    best_label = max(labs, key=labs.get) if labs else "UNDECIDED"
                    note += (f"a factor of order >= 2 splits further over C (P={p_more:.2f} for more factors in the "
                             "complex-coefficient structure posterior); its factors are reported. ")
                    res, agg = rc, ac
                    sup = kappa_support(u_ref, t, x, sigma, [_sympy_of(f) for f in factors],
                                        None if nd is None else nd / np.sqrt(2))
        if raw is not None and len(factors) > 1:
            m_ref, _, _, _ = extract_modes_ic(u_ref, t, x, noise=sigma,
                                              noise_draws=None if nd is None else nd / np.sqrt(2))
            keep, _ = raw_subset(factors, raw, _raw_kmax(m_ref, raw["period"]))
            if len(keep) < len(factors):
                for j, f in enumerate(factors):
                    if j not in keep:
                        f.status += "; dropped: not supported by the raw observations (interpolation artifact)"
                dropped_modes = dropped_modes + [f for j, f in enumerate(factors) if j not in keep]
                note += (f"{len(factors) - len(keep)} factor(s) dropped: the raw scattered data prefer the subset "
                         "without them. ")
                factors = [factors[j] for j in keep]
                sup = [sup[j] for j in keep]
        # 5. conjugate closure of a real field, then the refinement pass on the observations (T51-T52):
        # coefficients, terms and intervals from the raw kernel evidence; a grid is its own observation set
        if np.isrealobj(samples[0]):
            src = conjugate_closure(factors)
            if src:
                sup = list(sup) + [sup[i] for i in src]
                note += "a lone complex factor of the real field was completed with its conjugate. "
        obs = raw if raw is not None else (_grid_obs(samples[0], t, x, sigma)
                                           if len(samples) == 1 and nd is None and sigma > 0 else None)
        if refine_obs and obs is not None and obs.get("sigma"):
            m_ref, _, _, _ = extract_modes_ic(u_ref, t, x, noise=sigma,
                                              noise_draws=None if nd is None else nd / np.sqrt(2))
            cand = support_path(factors, u_ref, t, x, sigma, None if nd is None else nd / np.sqrt(2),
                                dx_class=bounds[1])
            ro = refine_factors(factors, obs, _raw_kmax(m_ref, obs["period"]), candidates=cand)
            gone = [f for j, f in enumerate(factors) if j not in ro["active"]]
            if gone:
                dropped_modes = dropped_modes + gone
                sup = [sup[j] for j in ro["active"]]
                factors = [factors[j] for j in ro["active"]]
                note += f"{len(gone)} factor(s) dropped by the refined evidence. "
            note += (f"factors refined on the observations (log evidence {ro['logev0']:.1f} -> {ro['logev']:.1f}, "
                     f"{ro['p']} real coefficient(s) kept by evidence). ")
            # a quadratic near a square discriminant: its split pair (C12-P2/P3) is refined and kept
            # if its evidence - Occam term is not lower than the quadratic's
            occ = 0.5 * np.log(len(obs["ys"]) * (1 if np.isrealobj(obs["ys"]) else 2))
            kmax = _raw_kmax(m_ref, obs["period"])
            boot_kmax = kmax if raw is None else None  # a grid is its own observation set
            cur = ro["logev"] - occ * ro["p"]
            glog = []  # T97: model changes refused by the fit guard (new, current Schwarz fit scores)
            if pre_c is not None:
                # the split over C was chosen by the core's structure posterior on mode-level fits; like every
                # other split (T64) it is kept only if its refined evidence - Occam term is not below that
                # of the unsplit real factors (same-family gap within one Occam unit: the factored form)
                pf = pre_c["factors"]
                cand_p = support_path(pf, u_ref, t, x, sigma, None if nd is None else nd / np.sqrt(2),
                                      dx_class=bounds[1])
                ro_p = refine_factors(pf, obs, kmax, candidates=cand_p)
                kept_p = [pf[j] for j in ro_p["active"]]
                sc_p = ro_p["logev"] - occ * ro_p["p"]
                same = _supports(kept_p) == _supports(factors) and sc_p - cur <= occ
                if not same and _beats(sc_p, _n_real_params(kept_p), cur, _n_real_params(factors)) and \
                        _fit_guard(kept_p, factors, obs, kmax, occ, glog):
                    note += (f"the split over C is not kept: the unsplit real factor(s) score higher after refinement "
                             f"(refined evidence - Occam {sc_p:.1f} vs {cur:.1f}). ")
                    factors, sup = kept_p, [pre_c["sup"][j] for j in ro_p["active"]]
                    res, agg, labs, best_label = pre_c["res"], pre_c["agg"], pre_c["labs"], pre_c["best_label"]
                    ro, cur = ro_p, sc_p
            mg = _refine_merges(factors, u_ref, t, x, sigma, None if nd is None else nd / np.sqrt(2), obs, kmax,
                                occ, cur, glog)
            if mg is not None:
                factors, cur = mg
                sup = kappa_support(u_ref, t, x, sigma, [_sympy_of(f) for f in factors],
                                    None if nd is None else nd / np.sqrt(2), signed=not np.isrealobj(samples[0]))
                note += f"two factors merged into their product after refinement (refined evidence - Occam {cur:.1f}). "
            def try_split(factors, sup, cur):
                props, src = split_branches(factors, 2 * np.pi * kmax / obs["period"])
                if len(props) <= len(factors):
                    return factors, sup, cur, ""
                if EXACT_SPLIT and _same_product(props, factors) and (
                        not np.isrealobj(samples[0]) or _conj_closed(props)):
                    # T80: the proposals multiply back to the unsplit factors to rounding, so they are the
                    # same kernel (C12-T1) with the same evidence; kept as they are, the factored form wins
                    # the tie by construction. A refit could add a 1e-4 cross term, make the supports
                    # differ and lose the tie on optimiser noise (wave_lowk)
                    if SPLIT_FINEST:  # T99: down to the finest exact factorisation (same product)
                        n0 = len(props)
                        props, src = _split_exact_finest(props, src, 2 * np.pi * kmax / obs["period"],
                                                         np.isrealobj(samples[0]))
                        if len(props) > n0:
                            return (props, [sup[i] for i in src], cur,
                                    f"a factor splits exactly into {len(props) - len(factors) + 1} factors (root "
                                    "branches grouped, repeated to the finest exact split; same product). ")
                    return (props, [sup[i] for i in src], cur,
                            "a factor splits exactly into two factors (root branches grouped; same product). ")
                trial = copy.deepcopy(props)
                sp2 = support_path(trial, u_ref, t, x, sigma, None if nd is None else nd / np.sqrt(2))
                cand2 = {j: sp2.get(j, [_wald_path(g)]) for j, g in enumerate(trial) if "reducible factor" in g.status}
                ro2 = refine_factors(trial, obs, kmax, candidates=cand2)
                kept2 = [trial[j] for j in ro2["active"]]
                # a split re-parametrises its product (same kernel, C12-T1): the Occam term counts the
                # unsplit factors' real coefficients, so an exact split is not charged twice and ties go to
                # the factored form (grouping by factors)
                p_now = sum(_n_params(f) for f in factors)
                sc2 = ro2["logev"] - occ * min(ro2["p"], p_now)
                # a split in the same model family as the unsplit factors (T68: same product support and
                # free parameters) re-parametrises it where the factorisation exists, so a gap below one
                # parameter's Occam unit is optimiser noise and the factored form is kept (grouping by
                # factors); a larger gap means the data leave the split family. Real field: closed under
                # conjugation (T53)
                same = _supports(kept2) == _supports(factors) and cur - sc2 <= occ
                # T78: a split that is NOT the same model is a model change like any other, so it must pass
                # the bare-mention rule (_beats, T74); before, any gain (0.2 nats on F3-130) displaced the law
                worse = (not _beats(sc2, _n_real_params(kept2), cur, _n_real_params(factors)) if SPLIT_BEATS
                         else sc2 < cur)
                if (worse and not same) or (np.isrealobj(samples[0]) and not _conj_closed(kept2)):
                    return factors, sup, cur, ""
                if not same and not _fit_guard(kept2, factors, obs, kmax, occ, glog):  # T97 (off by default)
                    return factors, sup, cur, ""
                return (kept2, [sup[src[j]] for j in ro2["active"]], max(sc2, cur) if same else sc2,
                        "a factor splits into two factors (root branches grouped, C12-P2/P3 generalised; refined "
                        f"evidence - Occam {sc2:.1f} vs {cur:.1f}). ")

            factors, sup, cur, nt_ = try_split(factors, sup, cur)
            note += nt_
            # the next structures of the decider / the pooled posterior, refined the same way: the chosen
            # structure was scored with coefficients read off biased modes, the refined score is the
            # honest comparison (evidence - Occam term on the observations, T51)
            alt = _refine_alternatives(factors, evidence, agg.structures_pooled, samples, pis, t, x, sigma, bounds,
                                       refine, nd, obs, kmax, occ, cur, u_ref, glog, pooled_pre)
            if alt is not None:
                factors, s_alt, e_alt = alt
                sup = kappa_support(u_ref, t, x, sigma, [_sympy_of(f) for f in factors],
                                    None if nd is None else nd / np.sqrt(2), signed=not np.isrealobj(samples[0]))
                note += (f"structure {s_alt} preferred after refinement (refined evidence - Occam {e_alt:.1f} vs "
                         f"{cur:.1f}). ")
                cur = e_alt
                factors, sup, cur, nt_ = try_split(factors, sup, cur)
                note += nt_
            if EPGP_REINTERP and raw is not None:
                # P4: re-interpolate with the candidates' EPGP kernel (keeps high-kappa modes the GP smooths);
                # a changed answer is accepted only on the raw-data evidence with _beats
                from .interp.reinterp import reinterp_alternative
                ri = reinterp_alternative(factors, dropped_modes, obs, t, x, bounds, refine, kmax, occ, cur,
                                          real=np.isrealobj(samples[0]))
                if ri is not None and _fit_guard(ri["factors"], factors, obs, ri["kmax"], occ, glog):
                    factors, sup, cur, kmax = ri["factors"], ri["sup"], ri["score"], ri["kmax"]
                    note += ri["note"]
                    factors, sup, cur, nt_ = try_split(factors, sup, cur)
                    note += nt_
            if glog:
                note += (f"{len(glog)} refinement-stage model change(s) refused by the fit guard: the refined "
                         "evidence preferred them, the plug-in fit with the same Occam unit did not (Schwarz "
                         + ", ".join(f"{a:.1f} vs {b:.1f}" for a, b in glog) + ", T97). ")
                if FIT_GUARD == "2" and best_label == "FIT-COMPATIBLE":
                    best_label = "UNDECIDED"
                    note += "the kernel evidence and the fit disagree, so the law is not claimed (T97). "
        else:
            new, src = split_quadratics(factors)
            if len(new) > len(factors):
                factors, sup = new, [sup[i] for i in src]
                note += "a quadratic factor with a square discriminant was split into its two factors (C12-P2/P3). "
        if IDKER_FINAL and factors:
            # T103 (c): the kappa support (ID-KER, the branch-point relabel) is that of the REPORTED factors:
            # refinement, merges and splits can move a factor far from the one whose modes were counted
            # (beam 400 1 %: a real tau + c factor of the half-plane run refined into conj A kept its support
            # {1}); a real field's conjugate pair shares its support (conj A is fixed by A, the -kappa mirror)
            real_f = bool(np.isrealobj(samples[0]))
            sup = kappa_support(u_ref, t, x, sigma, [_sympy_of(f) for f in factors],
                                None if nd is None else nd / np.sqrt(2), signed=not real_f)
            if real_f:
                sup = _conj_shared_support(factors, sup)
        if best_label == "UNDECIDED":
            labs2 = _relabel_branch_points(res, factors, sup, t[-1] - t[0])
            if labs2 != labs:
                labs = labs2
                best_label = max(labs, key=labs.get)
                if best_label != "UNDECIDED":
                    note += ("the confluent bins are branch points of a final factor (its discriminant vanishes at "
                             "a few kappa only), not a repeated factor (OPF5B-T6), so the label is not UNDECIDED. ")
        if IDKER_FINAL and best_label == "ID-KER" and labs.get("ID-KER", 0.0) > 0:
            # T103: the core's ID-KER masses are its verdicts on ITS factors; the label is about the reported
            # ones, so the core's own identifiability test is re-run on them (single-|kappa| factors: below)
            cnt = kappa_support(u_ref, t, x, sigma, [_sympy_of(f) for f in factors],
                                None if nd is None else nd / np.sqrt(2), signed=True, counts=True)
            if _identified(factors, cnt):
                labs = dict(labs)
                labs["FIT-COMPATIBLE"] = labs.get("FIT-COMPATIBLE", 0.0) + labs.pop("ID-KER")
                best_label = max(labs, key=labs.get)
                if best_label != "ID-KER":
                    note += ("the core's ID-KER verdict was on its own factors; every reported factor passes the "
                             "core's identifiability test on the observed modes (II-C1: m modes at one kappa, "
                             "m (dx + 1) + 1 modes at dx + 1 distinct |kappa|), so the label is not ID-KER (T103). ")
        single = []
        for f, ks in zip(factors, sup):
            f.kappa_support = ks
            dx = max((b for (_, b) in f.coef), default=0)
            if len(ks) == 1 and dx >= 0:
                single.append(ks[0])
                f.status += f"; ID-KER: seen only at |kappa| = {ks[0]:.3g}, any symbol through these modes fits"
        if single and best_label == "FIT-COMPATIBLE":
            best_label, idker_set = "ID-KER", True
            note += ("a factor is observed at a single |kappa| only, so it is not identified beyond that "
                     "frequency (0b.6): the printed factor is the lowest-degree one through its modes. ")
    if bootstrap and _depth == 0 and factors and len(samples) == 1 and nd is None and sigma > 0:
        bootstrap_intervals(factors, samples[0], t, x, sigma, B=bootstrap, kmax=boot_kmax)
        note += f"coefficient intervals from {bootstrap} parametric-bootstrap refits at the final structure. "
    if (RAW_GOF and _depth == 0 and raw is not None and raw.get("sigma") and factors
            and best_label == "FIT-COMPATIBLE"):
        from .raw_gof import raw_gof_log10p

        lp_raw, k_raw = raw_gof_log10p([_poly_symbol(_sympy_of(f)) for f in factors], raw)
        if lp_raw < PRED_LOGP:
            best_label = "MISFIT"
            note += (f"the reported law leaves structure in the raw observations (least squares on its kernel "
                     f"basis, |kappa| <= {k_raw}: log10 p = {lp_raw:.3g} < {PRED_LOGP:g}), so it is not claimed (T88). ")
    if best_label == "MISFIT" and "(T88)" not in note:
        note += ("most posterior mass is MISFIT at the largest accepted degree: the data may follow different "
                 "laws in different regions (see the domain report). ")
    out = LoopResult(best_label, factors, p_k, agg.structures_pooled, history, regrouped, bounds, labs, agg,
                     note=note.strip(), evidence=evidence)
    if _depth == 0 and factors:
        out.dropped = dropped_modes
    if split and _depth == 0 and len(factors) > 1:
        out.split = split_layer(samples, pis, t, x, sigma, out.pruned(), noise_draws=nd,
                                coef_lists=coef_draws(factors, W_DRAWS))
        # factors outside the most probable subset are redundant: their kernels add nothing the
        # others do not already explain in the data (e.g. one factor fitted twice at different kappa)
        keep = max(out.split["p_subset"], key=out.split["p_subset"].get)
        if np.isrealobj(samples[0]):
            # a real field's real span of a complex factor's kernel holds its conjugate's, so the
            # evidence cannot prefer the pair over one of them: the conjugate is kept with its partner
            keep = tuple(sorted(set(keep) | {
                j for j in range(len(factors)) if j not in keep
                and _nonreal(factors[j])
                and any(_conj_pair(factors[j], factors[i]) for i in keep)}))
        gof_final = None
        if (RAW_GOF_FINAL and len(keep) < len(factors) and raw is not None and raw.get("sigma")
                and (out.label == "FIT-COMPATIBLE"
                     or (idker_set and not any("ID-KER" in factors[j].status for j in keep)))):
            # T101: the law that would be reported after the drop must pass T88 on the raw points
            full_law, held = out.pruned(), out.factors
            out.factors = [factors[j] for j in keep]
            sub_law = out.pruned()
            out.factors = held
            verdict, lp_sub, k_sub, lp_full = subset_drop_gof(full_law, sub_law, raw)
            if verdict != "drop":
                if verdict == "keep_all":
                    keep = tuple(range(len(factors)))
                    out.note = (out.note + f" the split layer's subset evidence would drop factor(s), but the "
                                f"reduced law fails the raw goodness of fit (|kappa| <= {k_sub}: log10 p = "
                                f"{lp_sub:.3g} < {PRED_LOGP:g}) while the full set passes ({lp_full:.3g}), so "
                                "the dropped kernels explain raw data and every factor is kept (T101).").strip()
                else:
                    gof_final = (lp_sub, k_sub)
        if len(keep) < len(factors):
            for j, f in enumerate(factors):
                if j not in keep:
                    f.status += f"; dropped: redundant by data-level evidence (P(included)={out.split['p_include'][j]:.2f})"
            out.dropped = out.dropped + [f for j, f in enumerate(factors) if j not in keep]
            out.factors = [factors[j] for j in keep]
            out.note = (out.note + f" {len(out.dropped)} redundant factor(s) dropped by the split layer's subset "
                        "evidence.").strip()
            if len(out.factors) > 1:
                out.split = split_layer(samples, pis, t, x, sigma, out.pruned(), noise_draws=nd,
                                        coef_lists=coef_draws(out.factors, W_DRAWS))
            else:
                out.split = None
            if idker_set and not any("ID-KER" in f.status for f in out.factors):
                out.label = "FIT-COMPATIBLE"
            if gof_final is not None and out.label == "FIT-COMPATIBLE":
                out.label = "MISFIT"
                out.note = (out.note + f" the reported law leaves structure in the raw observations (least "
                            f"squares on its kernel basis, |kappa| <= {gof_final[1]}: log10 p = {gof_final[0]:.3g} "
                            f"< {PRED_LOGP:g}), so it is not claimed (T88, T101).").strip()
    if (GRID_SMOOTH_GOF and _depth == 0 and raw is None and nd is None and len(samples) == 1 and sigma
            and sigma > 0 and np.isrealobj(samples[0]) and out.factors and out.label == "FIT-COMPATIBLE"):
        # T96: the reported law must leave no smooth structure in the excited bins of the grid
        # (exact chi^2 null with known sigma); V0.1 dilutes an early-time misfit over 2 (nt - r) dof per bin
        from .validate import smooth_gof_log10p

        lp_s, k_s, det = smooth_gof_log10p(out.pruned(), samples[0], t, x, sigma, detail=True)
        if lp_s < PRED_LOGP:
            out.label = "UNDECIDED"
            out.note = (out.note + f" the reported law leaves smooth structure in the excited bins of the grid "
                        f"(residual on the Legendre(t) basis, |n| <= {det['band']}: worst bin |kappa| = {abs(k_s):.3g}, "
                        f"log10 p = {det['bin']:.3g}; omnibus chi2 {det['stat']:.1f} on {det['df']} dof, log10 p = "
                        f"{det['omnibus']:.3g}; combined {lp_s:.3g} < {PRED_LOGP:g}), so no law is claimed (T96).").strip()
    if report_domain and _depth == 0:
        out.domain = domain_report(res, agg, t, x)
        if subdomains:
            from .domain.quadtree import quadtree
            out.domain["quadtree"] = quadtree(_mean_sample(samples, pis), t, x, sigma)
    return out
