"""Coarse-to-fine split of the (t, x) rectangle into cells with one law each (DOMAIN.md decision 2).

- Cells are rectangles of the sample grid: simply connected by construction (C12-T1', C12-P10).
- Evidence of a cell = data-level BIC of its best structure (kernelfit: RSS/sigma^2 + (2 dof + 2 npar) ln N,
  known sigma, so it adds over cells that cover the same samples). A cell is split when the children's
  summed BIC beats the parent's. Split positions are chosen by evidence among fractions of the side.
- A split is admissible only if every child is still analysable: gamma_N of its fitted factors on the child
  (core.components.gamma_N, full block Gram, P2-T3) >= gamma_floor, and every factor carries at least
  dx + 1 distinct kappa (Rayleigh-resolved, energy above noise) (R4-T4; spread kappa, P2-P6).
  A child whose best fit has gamma_N below the floor (nearly collinear factors: over-parametrised for that cell)
  takes its best structure with gamma_N >= floor instead of vetoing the split (REPORT.md section 4).
- x-splits are preferred to t-splits at equal evidence (gamma ~ T^2, DOMAIN.md decision 3).
- After the recursion, adjacent leaves that form a rectangle and whose structure posteriors agree are merged
  when the merged cell's evidence is not worse.

gamma_floor is a hyperparameter to be set by empirical Bayes on single-factor nulls (CLAUDE.md rule 4);
the default comes from the experiments in sessions/S-DOMAIN/REPORT.md (table G).
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from ..core.components import gamma_N
from .fit import analyze_cell
from .kernelfit import kernel_design

GAMMA_FLOOR = 0.02  # default; REPORT.md table G (to be replaced by empirical Bayes)
TIE_BIC = 2.0  # "equal evidence": |delta BIC| below this (Bayes factor < e)


@dataclass
class CellFit:
    it: tuple  # (i0, i1) sample indices in t
    ix: tuple  # (j0, j1) sample indices in x
    bic: float
    structure: tuple
    factors: list
    ranked: list
    rss: float
    n: int
    gamma: float = 1.0
    n_kappa: list = field(default_factory=list)
    children: list = field(default_factory=list)
    split: tuple | None = None  # (axis, index)
    note: str = ""  # structures skipped for gamma_N < floor

    @property
    def posterior(self):
        return {st: p for st, _, p in self.ranked}

    def bounds(self, t, x):
        return (t[self.it[0]], t[self.it[1] - 1], x[self.ix[0]], x[self.ix[1] - 1])

    def law(self, tol=1e-2):
        return [str(Q.to_sympy(tol=tol)) for Q in self.factors]


def _component_kappas(cell, fit, noise, snr=3.0):
    """Per factor: number of Rayleigh-resolved kappa (spacing 2 pi / L) whose component energy is above noise."""
    B_all = [kernel_design([Q], cell.kg, cell.T, cell.X, cell.lam_cap) for Q in fit.factors]
    B = np.concatenate(B_all, axis=1)
    nrm = np.linalg.norm(B, axis=0)
    nrm[nrm == 0] = 1
    a, *_ = np.linalg.lstsq(B / nrm, cell.y, rcond=1e-10)
    a = a / nrm
    nt, nx = cell.nt, cell.nx
    L = nx * cell.dx
    out, off = [], 0
    from scipy.signal.windows import blackmanharris

    w = blackmanharris(nx)
    bn = max(noise, cell.sigma) * np.sqrt((w**2).sum()) / w.sum()
    for Bj in B_all:
        uj = (Bj @ a[off : off + Bj.shape[1]]).reshape(nt, nx)
        off += Bj.shape[1]
        F = np.fft.fft(uj * w, n=nx, axis=1) / w.sum()  # bins at the Rayleigh spacing 2 pi / L
        S = np.sqrt((np.abs(F) ** 2).mean(0))
        out.append(int((S > snr * bn).sum()))
    return out, L


def _gamma(fit, cell, t, x):
    if len(fit.factors) < 2:
        return 1.0
    L = cell.nx * cell.dx
    m = int(cell.kg.max() * L / (2 * np.pi))
    kap = 2 * np.pi / L * np.arange(-m, m + 1)
    kap = kap[kap != 0] if len(kap) > 1 else kap
    return gamma_N(fit.factors, kap, t, x)[0]


def fit_cell(u, t, x, it, ix, noise, seed=None, gamma_floor=0.0, **kw):
    """Best admissible structure of the cell (see admissible()). A fit that fails the rules (nearly collinear
    factors, or a factor carried by fewer than dx+1 resolved kappa) is over-parametrised for this cell: the next
    structure by BIC is used instead (cf.note records the skipped ones), rather than vetoing the split.
    If no structure is admissible, the BIC-best is kept and the cell stays inadmissible."""
    sl = (slice(*it), slice(*ix))
    tt, xx = t[slice(*it)], x[slice(*ix)]
    r = analyze_cell(u[sl], tt, xx, noise, seed_factors=seed, **kw)
    cell = r["cell"]
    chosen, first, note = None, None, ""
    for f in r["fits"]:
        cf = CellFit(it, ix, f.bic, f.structure, f.factors, r["ranked"], f.rss, f.n)
        cf.gamma = _gamma(f, cell, tt, xx)
        cf.n_kappa, _ = _component_kappas(cell, f, noise)
        ok, why = admissible(cf, gamma_floor)
        if ok:
            chosen = cf
            break
        note += f"{f.structure}: {why}; "
        if first is None:
            first = cf
    if chosen is None:
        chosen = first
    chosen.note = note
    return chosen


def admissible(cf: CellFit, gamma_floor):
    if len(cf.factors) > 1 and cf.gamma < gamma_floor:
        return False, f"gamma_N={cf.gamma:.3g} < floor"
    for (m, dx), nk in zip(cf.structure, cf.n_kappa):
        if nk < dx + 1:
            return False, f"factor ({m},{dx}) has {nk} < {dx + 1} distinct kappa"
    return True, ""


def quadtree(u, t, x, noise, gamma_floor=GAMMA_FLOOR, min_nt=16, min_nx=16, max_depth=3,
             fracs_x=(0.25, 0.375, 0.5, 0.625, 0.75), fracs_t=(0.5,), merge=True, verbose=False, **kw):
    """Returns (root CellFit with the split tree, list of leaf CellFits after merging, log lines)."""
    u = np.asarray(u)
    log = []
    cache = {}

    def get(it, ix, seed):
        key = (it, ix)
        if key not in cache:
            cache[key] = fit_cell(u, t, x, it, ix, noise, seed=seed, gamma_floor=gamma_floor, **kw)
        return cache[key]

    def say(s):
        log.append(s)
        if verbose:
            print(s, flush=True)

    def rec(cf, depth):
        if depth >= max_depth:
            return
        (i0, i1), (j0, j1) = cf.it, cf.ix
        best = {}
        for axis, fracs in (("x", fracs_x), ("t", fracs_t)):
            n0, n1, mn = (j0, j1, min_nx) if axis == "x" else (i0, i1, min_nt)
            for fr in fracs:
                c = n0 + int(round(fr * (n1 - n0)))
                if c - n0 < mn or n1 - c < mn:
                    continue
                if axis == "x":
                    kids = [get(cf.it, (j0, c), cf.factors), get(cf.it, (c, j1), cf.factors)]
                else:
                    kids = [get((i0, c), cf.ix, cf.factors), get((c, i1), cf.ix, cf.factors)]
                ok = [admissible(k, gamma_floor) for k in kids]
                bsum = sum(k.bic for k in kids)
                say(f"  {'  ' * depth}try {axis}@{c}: children BIC {bsum:.0f} vs parent {cf.bic:.0f}; "
                    f"{[k.structure for k in kids]} adm={[o[0] for o in ok]}")
                if not all(o[0] for o in ok):
                    continue
                if axis not in best or bsum < best[axis][0]:
                    best[axis] = (bsum, c, kids)
        if not best:
            return
        pick = best.get("x")
        if "t" in best and (pick is None or best["t"][0] < pick[0] - TIE_BIC):
            pick, axis = best["t"], "t"
        else:
            axis = "x"
        bsum, c, kids = pick
        if bsum < cf.bic - TIE_BIC:
            cf.children, cf.split = kids, (axis, c)
            say(f"{'  ' * depth}SPLIT {axis} at index {c} ({(x if axis == 'x' else t)[c]:.3f}): {cf.bic:.0f} -> {bsum:.0f}")
            for k in kids:
                rec(k, depth + 1)

    root = get((0, len(t)), (0, len(x)), None)
    say(f"root: {root.structure} {root.law()} BIC {root.bic:.0f}")
    rec(root, 0)

    def leaves(cf):
        return [cf] if not cf.children else [lf for k in cf.children for lf in leaves(k)]

    out = leaves(root)
    if merge:
        out = merge_leaves(out, get, say)
    return root, out, log


def _agree(a: CellFit, b: CellFit, thr=0.5):
    pa, pb = a.posterior, b.posterior
    return a.structure == b.structure and sum(min(pa.get(s, 0), pb.get(s, 0)) for s in set(pa) | set(pb)) > thr


def merge_leaves(leaves, get, say=print):
    """Merge adjacent leaves that form a rectangle, agree in structure posterior and whose merged fit has
    evidence not worse than the pair (sum BIC + TIE_BIC)."""
    changed = True
    leaves = list(leaves)
    while changed:
        changed = False
        for i in range(len(leaves)):
            for j in range(i + 1, len(leaves)):
                a, b = leaves[i], leaves[j]
                if a.it == b.it and (a.ix[1] == b.ix[0] or b.ix[1] == a.ix[0]):
                    it, ix = a.it, (min(a.ix[0], b.ix[0]), max(a.ix[1], b.ix[1]))
                elif a.ix == b.ix and (a.it[1] == b.it[0] or b.it[1] == a.it[0]):
                    it, ix = (min(a.it[0], b.it[0]), max(a.it[1], b.it[1])), a.ix
                else:
                    continue
                if not _agree(a, b):
                    continue
                m = get(it, ix, a.factors)
                if m.bic <= a.bic + b.bic + TIE_BIC:
                    say(f"MERGE {a.it}{a.ix} + {b.it}{b.ix}: {a.bic + b.bic:.0f} -> {m.bic:.0f}")
                    leaves = [lf for k, lf in enumerate(leaves) if k not in (i, j)] + [m]
                    changed = True
                    break
            if changed:
                break
    return leaves
