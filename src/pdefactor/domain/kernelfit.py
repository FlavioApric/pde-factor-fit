"""Data-level structured fit on a cell: distance of u to sum_j ker_band(Q_j) (C12-T1', rectangles).

Why: on a small non-periodic cell the free 2-D mode model is not identifiable (the Fisher matrix of
(lam, kappa) at the true modes is singular to working precision once neighbouring kappa are below the
Rayleigh spacing 2 pi / L: s e^{i kappa s} lies in the span of e^{i (kappa +- 1) s} on a short window;
REPORT.md, table F). The factors are identifiable: u lies in sum_j ker Q_j, whose band-limited part on
the cell is spanned by e^{lam_r(kappa) t + i kappa x}, lam_r roots of Q_j(., i kappa), kappa on a fine grid
(the same basis as core.components.kernel_basis). So each candidate structure is scored on the raw
samples of the cell:
    RSS(theta) = || u - P_{S(theta)} u ||^2,   BIC = RSS / sigma^2 + (2 dof + 2 npar) ln N,
dof = numerical rank of the kernel basis, npar = complex coefficients of the factors. theta is found by
variable projection (Levenberg-Marquardt on the factor coefficients only), started from point-level fits
of the extractors (extract.py) and from simple seeds.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.optimize import least_squares

from ..core.variety import PolySymbol


def kappa_grid(u, x, t, noise, snr_min=3.0, oversample=4, kmax_cap=None):
    """Band [-K, K] where the cell has energy above noise (Blackman-Harris spectrum, sidelobes < -92 dB, so
    leakage of strong modes does not widen the band; + one Rayleigh cell),
    grid step 2 pi / (oversample (L + 2 T)) (the kernel functions vary along characteristics, whose
    length in the cell is up to L + |c| T)."""
    from scipy.signal.windows import blackmanharris

    nx = u.shape[1]
    dx = x[1] - x[0]
    L = nx * dx
    T = t[-1] - t[0]
    w = blackmanharris(nx)
    F = np.fft.fft(np.asarray(u) * w, n=4 * nx, axis=1) / w.sum()
    k = 2 * np.pi * np.fft.fftfreq(4 * nx, d=dx)
    S = np.sqrt((np.abs(F) ** 2).mean(0))
    bn = max(noise, 1e-12 * np.abs(u).max()) * np.sqrt((w**2).sum()) / w.sum()
    sig = S > snr_min * bn
    K = (np.abs(k[sig]).max() if sig.any() else 2 * np.pi / L) + 2 * np.pi / L
    if kmax_cap:
        K = min(K, kmax_cap)
    step = 2 * np.pi / (oversample * (L + 2 * T))
    n = int(np.ceil(K / step))
    return step * np.arange(-n, n + 1)


def _roots_all(Q, kg):
    if Q.m == 1:
        return -np.polynomial.polynomial.polyval(1j * kg, Q.coeffs[0])[:, None]
    return np.stack([Q.roots(1j * k) for k in kg])


def kernel_design(factors, kg, T, X, lam_cap=None):
    """Columns e^{lam t + i kappa x} for every root branch of every factor at every grid kappa.
    Columns that blow up on the cell (Re lam t > lam_cap) are dropped (they are not in L^2 of the data scale)."""
    cols = []
    for Q in factors:
        R = _roots_all(Q, kg)
        L = R.ravel()
        K = np.repeat(kg, R.shape[1])
        if lam_cap is not None:
            ok = np.isfinite(L) & (L.real * T.max() < lam_cap)
            L, K = L[ok], K[ok]
        cols.append(np.exp(np.outer(T, L) + 1j * np.outer(X, K)))
    return np.concatenate(cols, axis=1) if cols else np.zeros((len(T), 0), complex)


def project(B, y, tol=1e-12):
    """Least-squares projection of y on span(B) via the (eigen-truncated) Gram matrix.
    Returns (residual vector, dof)."""
    if B.shape[1] == 0:
        return y.copy(), 0
    nrm = np.linalg.norm(B, axis=0)
    nrm[nrm == 0] = 1
    Bn = B / nrm
    G = Bn.conj().T @ Bn
    ev, V = np.linalg.eigh(G)
    keep = ev > tol * ev.max()
    W = Bn @ (V[:, keep] / np.sqrt(ev[keep]))  # orthonormal basis of the kept span
    r = y - W @ (W.conj().T @ y)
    return r, int(keep.sum())


def _pack(factors):
    return np.concatenate([np.r_[c.real, c.imag] for Q in factors for c in Q.coeffs])


def _unpack(theta, structure):
    out, i = [], 0
    for m, dx in structure:
        cs = []
        for _ in range(m):
            n = dx + 1
            cs.append(theta[i : i + n] + 1j * theta[i + n : i + 2 * n])
            i += 2 * n
        out.append(PolySymbol(m, cs))
    return out


def _conform(Q, m, dx):
    """Coefficients of a PolySymbol cut/padded to (m, dx)."""
    if Q.m != m:
        return None
    cs = []
    for c in Q.coeffs:
        c = np.asarray(c, complex)[: dx + 1]
        cs.append(np.r_[c, np.zeros(dx + 1 - len(c), complex)])
    return PolySymbol(m, cs)


@dataclass
class DataFit:
    structure: tuple
    factors: list
    rss: float
    dof: int
    npar: int
    bic: float
    n: int
    sigma: float


def _geom(a, n, h):
    """sum_{k<n} exp(a k h), elementwise, stable near a = 0."""
    z = a * h
    small = np.abs(z) < 1e-7
    with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
        g = np.where(small, n + z * n * (n - 1) / 2, np.expm1(n * z) / np.where(small, 1, np.expm1(z)))
    return g


class CellData:
    """Raw samples of one rectangular cell (uniform sub-grid) and the fast kernel projection.

    The kernel columns are separable, e^{lam t} (x) e^{i kappa x}, so the Gram matrix is a product of two
    geometric sums and B^H y needs only the x-DFT of the data on the kappa grid (precomputed): an RSS
    evaluation costs O(p^2 + nt p) instead of O(N p^2)."""

    def __init__(self, u, t, x, noise, kg=None, lam_cap=40.0):
        self.u = np.asarray(u)
        self.t, self.x = t, x
        self.nt, self.nx = self.u.shape
        self.dt, self.dx = t[1] - t[0], x[1] - x[0]
        TT, XX = np.meshgrid(t - t[0], x - x[0], indexing="ij")
        self.T, self.X = TT.ravel(), XX.ravel()
        self.y = self.u.ravel().astype(complex)
        self.yy = float(np.vdot(self.y, self.y).real)
        self.N = self.y.size
        self.sigma = noise if noise > 0 else 1e-9 * max(np.abs(self.u).max(), 1e-300)
        self.kg = kappa_grid(self.u, x, t, noise) if kg is None else kg
        self.lam_cap = lam_cap
        xx = x - x[0]
        self.Yk = self.u.astype(complex) @ np.exp(-1j * np.outer(xx, self.kg))  # (nt, nk)
        self.tt = t - t[0]

    def _cols(self, factors):
        lam, ki = [], []
        for Q in factors:
            R = _roots_all(Q, self.kg)
            lam.append(R.ravel())
            ki.append(np.repeat(np.arange(len(self.kg)), R.shape[1]))
        lam, ki = np.concatenate(lam), np.concatenate(ki)
        ok = np.isfinite(lam) & (lam.real * self.tt[-1] < self.lam_cap)
        return lam[ok], ki[ok]

    def proj_norm2(self, factors, tol=1e-12, ridge=1e-13):
        """(||P y||^2, dof) from the closed-form Gram (fast path, used inside the optimiser)."""
        lam, ki = self._cols(factors)
        if len(lam) == 0:
            return 0.0, 0
        kap = self.kg[ki]
        G = _geom(np.conj(lam)[:, None] + lam[None, :], self.nt, self.dt) *             _geom(1j * (kap[None, :] - kap[:, None]), self.nx, self.dx)
        E = np.exp(np.outer(self.tt, np.conj(lam)))  # conj(e^{lam t})
        c = np.einsum("tp,tp->p", E, self.Yk[:, ki])
        d = np.sqrt(np.maximum(np.real(np.diag(G)), 1e-300))
        Gn = G / d[:, None] / d[None, :]
        cn = c / d
        ev, V = np.linalg.eigh((Gn + Gn.conj().T) / 2)
        keep = ev > tol * ev.max()
        w = V[:, keep].conj().T @ cn
        return float(np.sum(np.abs(w) ** 2 / ev[keep]).real), int(keep.sum())

    def residual(self, factors):
        B = kernel_design(factors, self.kg, self.T, self.X, self.lam_cap)
        return project(B, self.y)

    def score(self, structure, factors, exact=True):
        if exact:
            r, dof = self.residual(factors)
            rss = float(np.vdot(r, r).real)
        else:
            p2, dof = self.proj_norm2(factors)
            rss = max(self.yy - p2, 0.0)
        npar = sum(m * (dx + 1) for m, dx in structure)
        bic = rss / self.sigma**2 + (2 * dof + 2 * npar) * np.log(self.N)
        return DataFit(tuple(structure), factors, rss, dof, npar, bic, self.N, self.sigma)

    def rss_grad(self, th, structure, ridge=1e-10):
        """RSS(theta) and its gradient (variable projection, Golub-Pereyra):
        dRSS = -2 Re r^H (dB) a, dB_col = t * B_col * d lam_col, d lam / d c_{k,b} = -xi^b lam^k / Q_lam."""
        factors = _unpack(th, structure)
        lam, ki, dl, pidx = [], [], [], []
        off = 0
        for (m, dx), Q in zip(structure, factors):
            R = _roots_all(Q, self.kg)  # (nk, m)
            xi_ = (1j * self.kg)[:, None]
            Ql = m * R ** (m - 1) + sum(k * np.polynomial.polynomial.polyval(xi_, Q.coeffs[k]) * R ** (k - 1)
                                        for k in range(1, m)) if m > 1 else np.ones_like(R)
            for k in range(m):
                for bb in range(dx + 1):
                    d = -(xi_**bb) * R**k / Ql  # (nk, m)
                    dl.append((off, d.ravel()))
                    off += 1
            lam.append(R.ravel())
            ki.append(np.repeat(np.arange(len(self.kg)), m))
            pidx.append(len(dl))
        ncoef = off
        lam_all = np.concatenate(lam)
        ki_all = np.concatenate(ki)
        # derivative matrix D (p_cols, ncoef) complex: column block of each factor only
        D = np.zeros((len(lam_all), ncoef), complex)
        start, ci = 0, 0
        for j, (m, dx) in enumerate(structure):
            n = len(lam[j])
            for _ in range(m * (dx + 1)):
                D[start:start + n, ci] = dl[ci][1]
                ci += 1
            start += n
        ok = np.isfinite(lam_all) & (lam_all.real * self.tt[-1] < self.lam_cap)
        lam_all, ki_all, D = lam_all[ok], ki_all[ok], D[ok]
        if len(lam_all) == 0:
            return self.yy / self.sigma**2, np.zeros(2 * ncoef)
        kap = self.kg[ki_all]
        Et = np.exp(np.outer(self.tt, lam_all))  # (nt, p)
        Ex = np.exp(1j * np.outer(self.x - self.x[0], kap))  # (nx, p)
        G = (Et.conj().T @ Et) * (Ex.conj().T @ Ex)  # separable Gram (Hadamard product)
        c = np.einsum("tp,tp->p", Et.conj(), self.Yk[:, ki_all])
        dg = np.sqrt(np.maximum(np.real(np.diag(G)), 1e-300))
        Gn = G / dg[:, None] / dg[None, :]
        Gn[np.diag_indices_from(Gn)] += ridge * 10  # ridge-regularised LS (smooth in theta)
        try:
            from scipy.linalg import cho_factor, cho_solve
            an = cho_solve(cho_factor(Gn, lower=True, check_finite=False), c / dg, check_finite=False)
        except (np.linalg.LinAlgError, ValueError):
            an = np.linalg.lstsq(Gn, c / dg, rcond=1e-12)[0]
        acoef = an / dg
        # residual in (t, kappa-grid) form is not enough for r; build r on the grid (separable product)
        Bu = (Et * acoef) @ Ex.T  # (nt, nx) = sum_col a e^{lam t} e^{i kap x}
        r = self.u - Bu
        rss = float(np.sum(np.abs(r) ** 2))
        # s_col = a_col sum conj(r) t e^{lam t} e^{i kap x}
        W = np.conj(r) @ Ex  # (nt, p): sum_x conj(r) e^{i kap x}
        s_col = acoef * np.einsum("tp,tp->p", W * self.tt[:, None], Et)
        gc = s_col @ D  # complex, per coefficient: sum_col s_col dlam/dc
        g = np.r_[-2 * np.real(gc), 2 * np.imag(gc)]
        # pack order: per factor, per coeff array k: [Re c_0..c_dx, Im c_0..c_dx]
        out = np.zeros(2 * ncoef)
        i, ci = 0, 0
        for m, dx in structure:
            for _ in range(m):
                n = dx + 1
                out[i:i + n] = g[ci:ci + n]
                out[i + n:i + 2 * n] = g[ncoef + ci:ncoef + ci + n]
                i += 2 * n
                ci += n
        return rss / self.sigma**2, out / self.sigma**2

    def refine(self, structure, factors, maxiter=120):
        """Variable projection: minimise RSS(theta) over the factor coefficients, L-BFGS with the
        analytic VarPro gradient."""
        from scipy.optimize import minimize

        factors = [_conform(Q, m, dx) for Q, (m, dx) in zip(factors, structure)]
        th0 = _pack(factors)

        def fg(th):
            with np.errstate(all="ignore"):
                v, g = self.rss_grad(th, structure)
            if not (np.isfinite(v) and np.all(np.isfinite(g))):
                return 1e300, np.zeros_like(th)
            return v, g

        f0 = fg(th0)[0]
        try:
            sol = minimize(fg, th0, jac=True, method="L-BFGS-B", options={"maxiter": maxiter, "ftol": 1e-11, "gtol": 1e-7})
            th = sol.x if sol.fun < f0 else th0
        except (ValueError, np.linalg.LinAlgError):
            th = th0
        facs = _unpack(th, structure)
        order = sorted(range(len(structure)), key=lambda j: structure[j])
        return self.score(tuple(structure[j] for j in order), [facs[j] for j in order])


def seed_factors(pool, structure):
    """Initial factor lists for a structure from a pool of PolySymbols (point-level fits): for each slot the
    pool members of the right m, cut/padded to dx; at most a few combinations."""
    from itertools import product

    slots = []
    for m, dx in structure:
        c = [q for Q in pool if (q := _conform(Q, m, dx)) is not None]
        if not c:
            return []
        slots.append(c[:4])
    out = []
    for combo in product(*slots):
        if len(structure) > 1 and len({id(q) for q in combo}) < len(combo):
            pass
        out.append(list(combo))
        if len(out) >= 12:
            break
    return out


def select_data(cell: CellData, candidates, pool, refine=True, n_refine=6, seeds_per=2):
    """Score every candidate structure on the data with its best pool seed (fast Gram path), refine the
    n_refine best structures by VarPro (seeds_per seeds each), rank all by BIC.
    Returns (best DataFit, ranked [(structure, bic, posterior weight)], all fits)."""
    seeded = []
    for st in candidates:
        seeds = seed_factors(pool, st)
        if not seeds:
            continue
        sc = sorted((cell.score(st, sd, exact=False) for sd in seeds), key=lambda f: f.bic)
        seeded.append(sc[:seeds_per])
    seeded.sort(key=lambda sc: sc[0].bic)
    fits = []
    for i, sc in enumerate(seeded):
        best = cell.score(sc[0].structure, sc[0].factors)
        if refine and i < n_refine:
            for f0 in sc:
                f1 = cell.refine(f0.structure, f0.factors)
                if f1.bic < best.bic:
                    best = f1
        fits.append(best)
    if not fits:
        return None, [], []
    fits.sort(key=lambda f: f.bic)
    b = np.array([f.bic for f in fits])
    p = np.exp(-(b - b.min()) / 2)
    p /= p.sum()
    return fits[0], [(f.structure, f.bic, pi) for f, pi in zip(fits, p)], fits
