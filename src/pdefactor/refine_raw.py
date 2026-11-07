"""Refinement pass on the observations (plan 0b.8 "refinement pass", v2.9 #1 last step, T51-T52).

The core reads the factors off dispersion points of an interpolant; at high kappa the interpolant is
biased (the GP smooths fast-decaying modes, T35), and a factor fitted to biased points can carry
spurious terms whose posterior interval excludes 0. Here the factor coefficients are fitted to the
observations themselves: the objective is the Gaussian evidence of the data in the span of the
factors' kernels (EPGP in closed form, bayes_split.raw_evidence), with the amplitude prior scale
tau^2 profiled (empirical Bayes). Then
- terms inside each factor are selected by the same evidence with the Occam term 0.5 p log n, over
  candidate supports with starting values from a mode-level least-squares path (linear, so no local
  optimum; the evidence surface in the coefficients oscillates with their phase errors);
- coefficient intervals come from the Laplace approximation at the optimum (Hessian of -log evidence).
The core is not touched: this layer only moves the outputs it reads (Monte Carlo elsewhere, rule 4;
the Laplace step is local around one optimum of a smooth objective, not a linearisation of E_int).
Grids are passed as observations too (every grid point), so grids and scattered data share this pass.
"""
from __future__ import annotations

import os

import numpy as np
from scipy.optimize import minimize, minimize_scalar

from .core.variety import PolySymbol

Z90 = 1.6448536269514722
# T76: one amplitude prior scale per wavenumber bin (|n| for a real field, n otherwise), each profiled by
# empirical Bayes, instead of one shared scale. The data identify Ann(u) only through the modes present
# (R4-T4, R4-T6): a bin the initial data do not excite carries no information on the law, and with a
# shared scale it still charged every model by the prior volume its kernel has there (damped_beam:
# the lambda = 0 mode at kappa = 0 of the true law cost ~4 nats against a damped alternative)
TAU2_PER_BIN = os.environ.get("PDEFACTOR_TAU2_PER_BIN", "0") == "1"
# T77 (repair of T76): only bins the data excite get their own scale; the bins whose data energy is
# consistent with noise alone (chi^2 test against sigma, Bonferroni over the bins, a data-only rule that
# does not depend on the model) share ONE pooled scale. Plain T76 gave every empty bin its own scale, so
# each fitted a little noise (< 1 nat each) and many empty bins together moved split-vs-unsplit
# comparisons (wave_lowk). Grid path only; implies TAU2_PER_BIN there.
TAU2_POOL_EMPTY = os.environ.get("PDEFACTOR_TAU2_POOL_EMPTY", "1") == "1"
EMPTY_ALPHA = 0.01  # family-wise level of the empty-bin test (divided by the number of bins)


def _t_basis_size(n_obs, n_ids, real):
    """Legendre degree count J shared by the grid and scattered bin tests (same rule, same data -> same J)."""
    J = T_DEG
    while J > 1 and (2 * n_ids - (1 if real else 0)) * J > n_obs // 2:
        J -= 1
    return J


def _excited_bins(g, kmax, real, sig):
    """Bins (|n| for a real field, n otherwise; n <= kmax) whose whitened data carry energy above noise in
    the span of Legendre(t) polynomials (j < J): the same statistic as _excited_bins_raw on the same points,
    because the unitary DFT columns of different bins are orthogonal, so the joint least-squares drop of a
    bin is the projection of its time series. Survival of chi^2 below EMPTY_ALPHA / #bins."""
    from scipy.stats import chi2

    Y, nx = g["Y"] / sig, g["nx"]
    nt = Y.shape[0]
    ids = list(range(0, kmax + 1)) if real else list(range(-kmax, kmax + 1))
    J = _t_basis_size(nt * nx, len(ids), real)
    t = np.asarray(g["t"], float) if g.get("t") is not None else np.arange(nt, dtype=float)
    s_ = 2 * (t - t.min()) / max(np.ptp(t), 1e-300) - 1
    Q, _ = np.linalg.qr(np.polynomial.legendre.legvander(s_, J - 1))  # orthonormal basis of the span
    a = EMPTY_ALPHA / len(ids)
    out = set()
    for b in ids:
        pe = float(np.sum(np.abs(Q.T @ Y[:, b % nx]) ** 2))  # projected energy
        if real:
            # Y_0 real (variance 1); for n > 0, Re and Im of Y_n have variance 1/2 each
            stat, dof = (pe, J) if b == 0 else (2 * pe, 2 * J)
        else:
            stat, dof = 2 * pe, 2 * J
        if chi2.sf(stat, dof) < a:
            out.add(b)
    return out


FAST_BINS = os.environ.get("PDEFACTOR_FAST_BINS", "1") == "1"  # vectorised per-bin profiling (adopted 2026-10-30; env =0 disables)
# scattered per-bin scales: start L-BFGS at the previous optimum for the same groups and basis shape
# (refinement probes differ by finite-difference steps, so it is near the new optimum)
WARM_BINS = os.environ.get("PDEFACTOR_WARM_BINS", "1") == "1"  # T85 (adopted 2026-10-31; env =0 disables)


def _profile_bins(lam, proj, gid, real, n_grid=256, n_gold=60):
    """Sum over bin groups of min over log tau^2 of the group's -log evidence term, all groups at once:
    a grid of n_grid points on each group's bounds (the same bounds as the per-bin minimize_scalar),
    then golden-section search in the bracket around the best grid point (width shrinks by 0.618^n_gold).
    The same objective as the per-bin loop, minimised at least as accurately (global on the grid,
    then to ~1e-8 in log tau^2), about two orders of magnitude fewer Python calls."""
    ug, inv = np.unique(gid, return_inverse=True)
    G = len(ug)
    lmax = np.zeros(G)
    np.maximum.at(lmax, inv, lam)
    lo, hi = np.log(1e-8 / np.maximum(lmax, 1e-300)), np.full(G, np.log(1e8))
    f_ = 0.5 if real else 1.0

    def val(lt):  # lt: (G, k) -> (G, k)
        t2 = np.exp(lt[inv])  # (N, k)
        v = proj[:, None] / (1 + t2 * lam[:, None]) + np.log1p(t2 * lam[:, None])
        out = np.zeros(lt.shape)
        np.add.at(out, inv, v)
        return f_ * out

    u = np.linspace(0.0, 1.0, n_grid)
    L = lo[:, None] + (hi - lo)[:, None] * u[None]
    V = val(L)
    j = np.argmin(V, axis=1)
    step = (hi - lo) / (n_grid - 1)
    a = np.maximum(L[np.arange(G), j] - step, lo)
    b = np.minimum(L[np.arange(G), j] + step, hi)
    gr = (np.sqrt(5) - 1) / 2
    c, d = b - gr * (b - a), a + gr * (b - a)
    fc, fd = val(c[:, None])[:, 0], val(d[:, None])[:, 0]
    for _ in range(n_gold):
        left = fc < fd
        b = np.where(left, d, b)
        a = np.where(left, a, c)
        c_new = b - gr * (b - a)
        d_new = a + gr * (b - a)
        c, d = c_new, d_new
        fc, fd = val(c[:, None])[:, 0], val(d[:, None])[:, 0]
    best = np.minimum(np.minimum(fc, fd), V[np.arange(G), j])
    return float(best.sum())


T_DEG = 6  # Legendre polynomials in t per bin for the scattered empty-bin test


def _excited_bins_raw(ts, xs, ys, period, kmax, real, sig):
    """Scattered version of _excited_bins: joint least squares of y on e^{i kappa_n x} P_j(t) (Legendre
    in t, j < J) over every bin |n| <= kmax, then per bin the drop in chi^2 when that bin's columns are
    removed, against chi^2(dof of the bin) with known sigma. A data-only rule. A mode too fast for J
    polynomials can be missed; its bin is then pooled, i.e. it falls back to the shared scale used
    before T76, so a miss can only cost what the default already costs."""
    from scipy.stats import chi2

    ts, xs, ys = np.asarray(ts, float), np.asarray(xs, float), np.asarray(ys)
    n = len(ys)
    ids = list(range(0, kmax + 1)) if real else list(range(-kmax, kmax + 1))
    J = _t_basis_size(n, len(ids), real)
    s = 2 * (ts - ts.min()) / max(np.ptp(ts), 1e-300) - 1
    P = np.polynomial.legendre.legvander(s, J - 1)  # (n, J)
    cols, gid = [], []
    for b in ids:
        kap = 2 * np.pi * b / period
        if real:
            parts = [np.ones(n)] if b == 0 else [np.cos(kap * xs), np.sin(kap * xs)]
        else:
            parts = [np.exp(1j * kap * xs)]
        for v in parts:
            cols.append(v[:, None] * P)
            gid += [b] * J
    A, gid = np.concatenate(cols, axis=1) / sig, np.array(gid)
    yw = ys / sig

    def rss(M):
        c, *_ = np.linalg.lstsq(M, yw, rcond=None)
        r = yw - M @ c
        return float(np.vdot(r, r).real)

    full = rss(A)
    a = EMPTY_ALPHA / len(ids)
    out = set()
    for b in ids:
        sel = gid != b
        k = int(np.sum(~sel))
        drop = rss(A[:, sel]) - full
        stat, dof = (drop, k) if real else (2 * drop, 2 * k)
        if chi2.sf(stat, dof) < a:
            out.add(b)
    return out


def _basis(syms, ts, xs, period, kmax, real):
    return _basis_groups(syms, ts, xs, period, kmax, real)[0]


def _basis_groups(syms, ts, xs, period, kmax, real):
    """_basis and the bin of each column (|n| for a real field, n otherwise), for T76."""
    cols, gid = [], []
    for Q in syms:
        for n in range(-kmax, kmax + 1):
            kap = 2 * np.pi * n / period
            for lam in np.atleast_1d(Q.roots(1j * kap)):
                cols.append(np.exp(np.clip(lam.real * ts, -700, 50) + 1j * (lam.imag * ts + kap * xs)))
                gid.append(abs(n) if real else n)
    B = np.stack(cols, axis=1) if cols else np.zeros((len(ts), 0), complex)
    B = np.concatenate([B.real, B.imag], axis=1) if real else B
    return B, np.array(gid * 2 if real else gid, int)


def _roots_all(Q, xis):
    """Q.roots(xi0) for every xi0 in xis at once, shape (len(xis), m): the eigenvalues of the stacked
    companion matrices (what np.roots computes one by one); root order is irrelevant downstream."""
    xis = np.asarray(xis, complex)
    c = [np.polynomial.polynomial.polyval(xis, Q.coeffs[k]) * np.ones_like(xis) for k in range(Q.m)]
    if Q.m == 1:
        return -c[0][:, None]
    C = np.zeros((len(xis), Q.m, Q.m), complex)
    C[:, 0, :] = -np.stack(c[::-1], axis=1)  # first row: -p_{m-1}, ..., -p_0
    C[:, np.arange(1, Q.m), np.arange(Q.m - 1)] = 1.0
    return np.linalg.eigvals(C)


def _grid_spectrum(syms, g, period, kmax, real, sig, groups=False):
    """_grid_spectrum_ref with the per-bin Python loops replaced by array operations: all roots at
    once (_roots_all), each bin pair's block built from the (roots x time) exponentials. Same Gram
    blocks up to a column permutation, so the same eigenvalues and projections (test_refine_grid)."""
    t, nx, Y = g["t"], g["nx"], g["Y"] / sig
    sq = np.sqrt(nx)
    yy = float(np.vdot(Y, Y).real)
    ns = np.arange(-kmax, kmax + 1)
    R = [_roots_all(Q, 1j * 2 * np.pi * ns / period) for Q in syms]
    R = np.concatenate(R, axis=1) if R else np.zeros((len(ns), 0), complex)  # (2 kmax + 1, sum m)
    E = np.exp(np.clip(R.real[..., None] * t, -700, 50) + 1j * R.imag[..., None] * t)  # (nk, r, nt)
    if not np.all(np.isfinite(E)):
        return np.zeros(0), np.zeros(0), yy
    h = sq / 2
    if real:  # bin pair {n, -n} stacked: rows (Y[:, n], Y[:, -n]); Re / Im of e^{lam t + i kappa x}
        e, f = E[kmax + 1:], E[kmax - 1::-1] if kmax else E[:0]  # kappa_n and kappa_{-n}, n = 1..kmax
        cat = lambda p_, q_: np.concatenate([p_, q_], axis=-1)
        Bt = np.concatenate([cat(h * e, h * e.conj()), cat(-1j * h * e, 1j * h * e.conj()),
                             cat(h * f.conj(), h * f), cat(1j * h * f.conj(), -1j * h * f)], axis=1)
        yb = np.stack([np.concatenate([Y[:, n % nx], Y[:, (-n) % nx]]) for n in range(1, kmax + 1)]) if kmax else None
        B0, y0 = np.concatenate([sq * E[kmax].real, sq * E[kmax].imag], axis=0), Y[:, 0]
    else:  # every bin on its own
        Bt = sq * np.concatenate([E[kmax + 1:], E[:kmax]], axis=0)
        yb = np.stack([Y[:, n % nx] for n in list(range(1, kmax + 1)) + list(range(-kmax, 0))]) if kmax else None
        B0, y0 = sq * E[kmax], Y[:, 0]
    lam, proj, gid = [], [], []
    if E.shape[1]:
        U, s_, _ = np.linalg.svd(B0.T, full_matrices=False)
        lam.append(s_**2)
        proj.append(np.abs(U.conj().T @ y0) ** 2)
        gid.append(np.zeros(len(s_), int))
        if kmax:
            U, s_, _ = np.linalg.svd(np.swapaxes(Bt, 1, 2), full_matrices=False)  # batched over bins
            lam.append((s_**2).ravel())
            proj.append((np.abs(np.einsum("kar,ka->kr", U.conj(), yb)) ** 2).ravel())
            ids = np.arange(1, kmax + 1) if real else np.concatenate([np.arange(1, kmax + 1), np.arange(-kmax, 0)])
            gid.append(np.repeat(ids, s_.shape[1]))
    lam, proj = (np.concatenate(lam), np.concatenate(proj)) if lam else (np.zeros(0), np.zeros(0))
    gid = np.concatenate(gid) if gid else np.zeros(0, int)
    smax = np.sqrt(lam.max()) if lam.size else 0.0
    keep = np.sqrt(lam) > 1e-12 * smax
    lam, proj, gid = lam[keep], proj[keep], gid[keep]
    rest = max(yy - float(proj.sum()), 0.0)
    if groups:
        return lam, proj, rest, gid
    return lam, proj, rest


def _grid_spectrum_ref(syms, g, period, kmax, real, sig):
    """Eigenvalues of the whitened Gram and the data's projections on its eigenvectors, for a full
    periodic grid (obs["grid"]: t from 0, nx, Y = unitary DFT over x of the (nt, nx) data). Exact
    rewrite of the dense computation: the DFT over x is unitary, a column e^{lam t + i kappa x}
    lives in bin kappa only (its Re/Im parts in bins +-kappa), so the Gram is block-diagonal over
    the bin pairs {n, -n}; the evidence depends on B B^H only, so the column phase e^{i kappa x0}
    (a rotation of each Re/Im pair) is dropped."""
    t, nx, Y = g["t"], g["nx"], g["Y"] / sig
    sq = np.sqrt(nx)
    lam, proj = [], []
    yy = float(np.vdot(Y, Y).real)
    for n in range(0, kmax + 1):
        if real:
            groups = [([0], [0])] if n == 0 else [([n % nx, (-n) % nx], [n, -n])]
        else:
            groups = [([0], [0])] if n == 0 else [([n % nx], [n]), ([(-n) % nx], [-n])]
        for bs, signs in groups:
            cols = []
            for nn in signs:
                kap = 2 * np.pi * nn / period
                for Q in syms:
                    for lm in np.atleast_1d(Q.roots(1j * kap)):
                        e = np.exp(np.clip(lm.real * t, -700, 50) + 1j * lm.imag * t)
                        if not real:
                            cols.append(sq * e)
                            continue
                        b_p, b_m = nn % nx, (-nn) % nx
                        for part in (0, 1):  # Re, Im of the column
                            v = np.zeros((len(bs), len(t)), complex)
                            cp = sq * e / 2 * (1 if part == 0 else -1j)
                            cm = sq * np.conj(e) / 2 * (1 if part == 0 else 1j)
                            for r_, b in enumerate(bs):
                                if b == b_p:
                                    v[r_] += cp
                                if b == b_m:
                                    v[r_] += cm
                            cols.append(v.ravel())
            if not cols:
                continue
            Bb = np.stack(cols, axis=1)
            yb = np.concatenate([Y[:, b] for b in bs])
            if not np.all(np.isfinite(Bb)):
                return np.zeros(0), np.zeros(0), yy
            U, s_, _ = np.linalg.svd(Bb, full_matrices=False)
            lam.append(s_**2)
            proj.append(np.abs(U.conj().T @ yb) ** 2)
    lam, proj = (np.concatenate(lam), np.concatenate(proj)) if lam else (np.zeros(0), np.zeros(0))
    smax = np.sqrt(lam.max()) if lam.size else 0.0
    keep = np.sqrt(lam) > 1e-12 * smax
    lam, proj = lam[keep], proj[keep]
    rest = max(yy - float(proj.sum()), 0.0)
    return lam, proj, rest


def log_evidence(syms, obs, kmax):
    """log N(y; 0, sigma^2 I + tau^2 sigma^2 B B^H) maximised over tau^2 (continuous), via the
    eigenvalues of the Gram B^H B / sigma^2 (rank deficiency of the real basis is harmless)."""
    ts, xs, ys, sig = obs["ts"], obs["xs"], obs["ys"], obs["sigma"]
    real = bool(np.isrealobj(ys))
    yw = ys / sig
    n = len(ys)
    yy = float(np.vdot(yw, yw).real)
    g = obs.get("grid")
    gid = None
    if g is not None and 2 * kmax < g["nx"]:
        lam, proj, rest, gid = _grid_spectrum(syms, g, obs["period"], kmax, real, sig, groups=True)
        B = None
    else:
        B, cg = _basis_groups(syms, ts, xs, obs["period"], kmax, real)
        B = B / sig
    if B is None:
        pass
    elif B.shape[1] == 0 or not np.all(np.isfinite(B)):
        lam, proj, rest = np.zeros(0), np.zeros(0), yy
    else:
        # SVD form: the part of y outside the span is a residual norm (>= 0 by construction), so
        # columns of very different scale (fast decay, growth) do not cancel catastrophically
        U, s, Vh = np.linalg.svd(B, full_matrices=False)
        keep = s > 1e-12 * s.max()
        U, s, Vh = U[:, keep], s[keep], Vh[keep]
        c = U.conj().T @ yw
        lam, proj = s**2, np.abs(c) ** 2
        rest = max(float(np.vdot(yw - U @ c, yw - U @ c).real), 0.0)

    def neg(lt):
        t2 = np.exp(lt)
        q = rest + np.sum(proj / (1 + t2 * lam))
        ld = np.sum(np.log1p(t2 * lam))
        return 0.5 * (q + ld) if real else (q + ld)

    r = minimize_scalar(neg, bounds=(np.log(1e-8), np.log(1e8)), method="bounded", options={"xatol": 1e-3})
    const = 0.5 * n * np.log(2 * np.pi) + n * np.log(sig) if real else n * np.log(np.pi) + 2 * n * np.log(sig)
    if not (TAU2_PER_BIN or TAU2_POOL_EMPTY) or not lam.size:
        return float(-r.fun - const)
    if TAU2_POOL_EMPTY and gid is not None:  # T77: the bins without data energy above noise share one scale
        memo = g.setdefault("_excited", {})  # data-only, so computed once per observation set (exact)
        key = (int(kmax), bool(real), float(sig))
        if key not in memo:
            memo[key] = _excited_bins(g, kmax, real, sig)
        gid = np.where(np.isin(gid, list(memo[key])), gid, -(10**9))
    if gid is not None and FAST_BINS:
        tot = (0.5 * rest if real else rest) + _profile_bins(lam, proj, gid, real)
        return float(-min(tot, r.fun) - const)
    if gid is not None:  # grid: the Gram is block-diagonal over bins, each bin's scale is profiled on its own
        tot = 0.5 * rest if real else rest
        for b in np.unique(gid):
            lb, pb = lam[gid == b], proj[gid == b]

            def nb(lt, lb=lb, pb=pb):
                t2 = np.exp(lt)
                v = np.sum(pb / (1 + t2 * lb)) + np.sum(np.log1p(t2 * lb))
                return 0.5 * v if real else v

            # lower bound relative to the bin's largest Gram eigenvalue: a bin without data can be
            # switched off whatever the scale of its columns (a growing mode has a huge norm)
            tot += minimize_scalar(nb, bounds=(np.log(1e-8 / lb.max()), np.log(1e8)), method="bounded",
                                   options={"xatol": 1e-3}).fun
        return float(-min(tot, r.fun) - const)
    if TAU2_POOL_EMPTY:  # T77 scattered: the empty bins share one scale
        memo = obs.setdefault("_excited", {})  # data-only, so computed once per observation set (exact)
        key = (int(kmax), bool(real), float(sig), len(ys))
        if key not in memo:
            memo[key] = _excited_bins_raw(ts, xs, ys, obs["period"], kmax, real, sig)
        cg = np.where(np.isin(cg, list(memo[key])), cg, -(10**9))
    warm = obs.setdefault("_lts", {}) if WARM_BINS else None
    return float(-min(_per_bin_neg(c, s[:, None] * Vh, cg, rest, real, r.x, warm), r.fun) - const)


def _per_bin_neg(c, W, cg, rest, real, lt0, warm=None):
    """-log evidence (without constants) minimised over one prior scale per column group: in the
    orthonormal basis of the span (B = U W), Sigma = I + W D W^H with D = diag(tau^2 of each column's
    bin); rest = |y outside the span|^2. Analytic gradient; started at the shared scale lt0."""
    from scipy.linalg import solve_triangular
    from scipy.optimize import minimize

    ug, inv = np.unique(cg, return_inverse=True)
    r = W.shape[0]
    f_ = 0.5 if real else 1.0

    def fg(lts):
        d = np.exp(lts)[inv]
        K = np.eye(r) + (W * d) @ W.conj().T
        try:
            L_ = np.linalg.cholesky(K)
        except np.linalg.LinAlgError:
            return np.inf, np.zeros_like(lts)
        # one triangular solve: with z = L^-1 c and Z = L^-1 W, c^H K^-1 c = |z|^2,
        # diag(W^H K^-1 W) = column norms of Z and W^H K^-1 c = Z^H z (exact identities)
        zZ = solve_triangular(L_, np.column_stack([c, W]), lower=True, check_finite=False)
        z, Z = zZ[:, 0], zZ[:, 1:]
        q = rest + float(np.vdot(z, z).real)
        ld = 2 * float(np.sum(np.log(np.abs(np.diag(L_)))))
        gj = np.sum(np.abs(Z) ** 2, axis=0) - np.abs(Z.conj().T @ z) ** 2
        grad = np.bincount(inv, weights=d * gj, minlength=len(ug))
        return f_ * (q + ld), f_ * grad

    # lower bounds relative to each group's largest column norm (a bin without data can be switched off)
    cn = np.zeros(len(ug))
    np.maximum.at(cn, inv, np.sum(np.abs(W) ** 2, axis=0))
    lo = np.log(1e-8 / np.maximum(cn, 1e-300))
    key = (tuple(ug), W.shape)
    x0 = warm.get(key, np.full(len(ug), lt0)) if warm is not None else np.full(len(ug), lt0)
    res = minimize(fg, np.clip(x0, lo, np.log(1e8)), jac=True, method="L-BFGS-B",
                   bounds=list(zip(lo, [np.log(1e8)] * len(ug))))
    if warm is not None and np.isfinite(res.fun):
        warm[key] = res.x
    return float(res.fun)


# ------------------------------------------------------------------ parametrisation
class Param:
    """Real parameters of a factor set: (factor j, monomial (a, b), part 0 = Re / 1 = Im). Factors
    tied as conjugates (real field) are not parametrised: they follow their partner."""

    def __init__(self, coefs, ms, free, ties, active=None):
        self.coefs = [dict(c) for c in coefs]  # {(a, b): complex}, leading (m, 0) -> 1
        self.ms = ms
        self.free = list(free)
        self.ties = ties  # {j: partner index}: factor j = conj(partner)
        self.active = set(range(len(coefs))) if active is None else set(active)

    def vector(self):
        return np.array([(self.coefs[j][k].imag if p else self.coefs[j][k].real) for j, k, p in self.free])

    def set(self, v):
        for (j, k, p), val in zip(self.free, v):
            c = self.coefs[j].get(k, 0j)
            self.coefs[j][k] = complex(c.real, val) if p else complex(val, c.imag)
        for j, i in self.ties.items():
            self.coefs[j] = {k: np.conj(c) for k, c in self.coefs[i].items()}

    def symbols(self, skip_tied=False):
        out = []
        for j, (c, m) in enumerate(zip(self.coefs, self.ms)):
            if (skip_tied and j in self.ties) or j not in self.active:
                continue
            coeffs = []
            for a in range(m):
                dx = max([b for (aa, b) in c if aa == a], default=0)
                coeffs.append(np.array([c.get((a, b), 0j) for b in range(dx + 1)], complex))
            out.append(PolySymbol(m, coeffs))
        return out


def _objective(par, obs, kmax, real):
    # real field: the real span of a complex factor's kernel already holds its conjugate's
    def f(v):
        par.set(v)
        return -log_evidence(par.symbols(skip_tied=real), obs, kmax)

    return f


def _optimise(par, obs, kmax, real, maxiter=200):
    v0 = par.vector()
    if len(v0) == 0:
        par.set(v0)
        return log_evidence(par.symbols(skip_tied=real), obs, kmax)
    scale = np.maximum(np.abs(v0), 1e-2)
    f = _objective(par, obs, kmax, real)
    g = lambda w: f(v0 + scale * w)  # noqa: E731
    r = minimize(g, np.zeros(len(v0)), method="L-BFGS-B", options={"maxiter": maxiter})
    w = r.x if r.fun <= g(np.zeros(len(v0))) else np.zeros(len(v0))
    best = -g(w)
    par.set(v0 + scale * w)
    return float(best)


def _hessian(par, obs, kmax, real):
    """Hessian of -log evidence in the free parameters (central differences, relative steps)."""
    v0 = par.vector()
    f = _objective(par, obs, kmax, real)
    p = len(v0)
    h = 1e-4 * np.maximum(np.abs(v0), 1e-2)
    H = np.zeros((p, p))
    f0 = f(v0)
    for i in range(p):
        for j in range(i, p):
            e_i, e_j = np.eye(p)[i] * h[i], np.eye(p)[j] * h[j]
            if i == j:
                H[i, i] = (f(v0 + e_i) - 2 * f0 + f(v0 - e_i)) / h[i] ** 2
            else:
                H[i, j] = H[j, i] = (f(v0 + e_i + e_j) - f(v0 + e_i - e_j) - f(v0 - e_i + e_j)
                                     + f(v0 - e_i - e_j)) / (4 * h[i] * h[j])
    par.set(v0)
    return H


def _free(coefs, ms, ties, active=None):
    """Free real parameters: every non-zero part of every non-leading coefficient (a part that is
    exactly 0 is outside the support), tied conjugates and inactive factors excluded."""
    act = set(range(len(coefs))) if active is None else set(active)
    return [(j, k, p) for j, (c, m) in enumerate(zip(coefs, ms)) if j not in ties and j in act
            for k in sorted(c) if k != (m, 0) for p in (0, 1) if (c[k].imag if p else c[k].real) != 0.0]


def refine(coefs, ms, obs, kmax, ties=None, candidates=None, max_full=6):
    """coefs: list of {(a, b): complex} per factor (monic: (m, 0) -> 1); a part exactly 0 is outside
    the support. obs: dict(ts, xs, ys, period, sigma). ties: {j: i} for factor j = conj(factor i)
    (real field). candidates: {j: [coef dict, ...]}: other supports of factor j with starting values,
    largest first (a mode-level least-squares path). Score of a factor set: refined log evidence
    - 0.5 p log n (p real parameters; the Laplace/BIC Occam term of the structure decider).
    1. supports: per factor, the candidates from the smallest up, stopping after two that do not
       improve the score; the given coefficients (optimised only with at most max_full parameters)
       are the reference;
    2. factors: a factor (with its tied conjugate) is dropped while that improves the score (a spurious
       factor otherwise bends the others' coefficients to share its columns);
    3. supports again if a factor was dropped.
    Returns dict with the refined coefficients, the active factors, Laplace 90 % half-widths
    {(j, (a, b)): complex}, the log evidence before / after and the number of parameters."""
    ties = ties or {}
    real = bool(np.isrealobj(obs["ys"]))
    n_eff = len(obs["ys"]) * (1 if real else 2)
    occ = 0.5 * np.log(n_eff)

    def make(cs, active):
        cs = [{k: complex(v) for k, v in c.items() if v != 0 or k == (m, 0)} for c, m in zip(cs, ms)]
        return Param(cs, ms, _free(cs, ms, ties, active), ties, active)

    def run(par, opt=True):
        if opt:
            e = _optimise(par, obs, kmax, real)
        else:
            e = -_objective(par, obs, kmax, real)(par.vector())
            par.set(par.vector())
        return e, e - occ * len(par.free)

    par = make(coefs, set(range(len(coefs))))
    ev0 = -_objective(par, obs, kmax, real)(par.vector())
    ev, score = run(par, opt=len(par.free) <= max_full)

    def supports(par, ev, score):
        for j, cands in (candidates or {}).items():
            if j not in par.active or j in ties:
                continue
            for path in cands:
                # smallest support first; once the path has improved the score, two candidates in a
                # row without improvement end it (the score along a nested path rises, then falls)
                miss, gained = 0, False
                for cj in reversed(path):
                    cs = [dict(c) for c in par.coefs]
                    cs[j] = dict(cj)
                    p2 = make(cs, par.active)
                    e2, s2 = run(p2)
                    if s2 > score:
                        par, ev, score, miss, gained = p2, e2, s2, 0, True
                    else:
                        miss += 1
                        if gained and miss >= 2:
                            break
        return par, ev, score

    par, ev, score = supports(par, ev, score)
    dropped_any = False
    while True:
        units = [j for j in sorted(par.active) if j not in ties]
        if len(units) <= 1:
            break
        best = None
        for j in units:
            act = par.active - {j} - {i for i, pj in ties.items() if pj == j}
            p2 = make(par.coefs, act)
            e2, s2 = run(p2)
            if s2 > score and (best is None or s2 > best[2]):
                best = (p2, e2, s2)
        if best is None:
            break
        par, ev, score = best
        dropped_any = True
    if dropped_any:
        par, ev, score = supports(par, ev, score)
    half = {}
    if par.free:
        H = _hessian(par, obs, kmax, real)
        try:
            cov = np.linalg.inv(H)
            sd = np.sqrt(np.where(np.diag(cov) > 0, np.diag(cov), np.nan))
        except np.linalg.LinAlgError:
            sd = np.full(len(par.free), np.nan)
        for (j, k, p), s_ in zip(par.free, sd):
            h = half.get((j, k), 0j)
            half[(j, k)] = complex(h.real, Z90 * s_) if p else complex(Z90 * s_, h.imag)
        for j, i in ties.items():
            for (jj, k), h in list(half.items()):
                if jj == i:
                    half[(j, k)] = complex(h.real, h.imag)
    return {"coefs": par.coefs, "active": sorted(par.active), "half": half, "logev0": float(ev0), "logev": float(ev),
            "p": len(par.free)}
