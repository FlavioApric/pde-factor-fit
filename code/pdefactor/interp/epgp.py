"""Factor-wise EPGP prior (Härkönen, Lange-Hegermann, Raiță, ICML 2023), specialised to 1+1 and
used for the refinement pass (step 6 -> step 1): given a list of factors Q_j(tau, xi), every prior
draw is an exact solution of P = prod Q_j, and the component of each factor has its own posterior.

Ehrenpreis-Palamodov (R2-T6, THEORY_TO_ALGO T25): u in ker Q on a convex domain is an integral of
e^{lam t + i kappa x} over the variety Q(lam, i kappa) = 0. We discretise kappa on a lattice
(spacing pi / L, or 2 pi / period when the domain is periodic, where it is a basis) and put
independent Gaussian weights on the features, so u_j = sum_k w_jk phi_jk(t, x) and

    w_jk ~ N(0, s_j^2 rho_nu(kappa_k) dkappa),

with rho_nu the Matern spectral density of smoothness nu (RBF: Gaussian). The components lose one
derivative with respect to u (C12-C1, T11), so the component prior uses nu_comp = nu_u + 1
(`smoother` of the family fitted to u). Each feature is scaled by its maximum modulus over the time
window, so growing or decaying branches are comparable and nothing overflows.

Hyperparameters (s_j, ell, s_n) by type-II ML on the closed-form evidence of the Bayesian linear
regression (M x M form, M = number of real features). This is a plug-in: their uncertainty is not
propagated here (it is in gp.py); flagged in info.
origin of the construction: Härkönen et al. 2023, Sec. 3 (EPGP) and haerski/EPGP demo.ipynb (MIT);
re-implemented, no code copied.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np
import sympy as sp
from scipy.optimize import minimize
from scipy.special import gammaln

from ..symbols import tau, xi

_NU = {"matern12": 0.5, "matern32": 1.5, "matern52": 2.5, "rbf": math.inf}


def spectral_density(kappa, ell, family):
    """1-D spectral density (unnormalised over kappa; normalised so that it integrates to 1)."""
    nu = _NU[family]
    if math.isinf(nu):
        return ell / math.sqrt(2 * math.pi) * np.exp(-0.5 * (ell * kappa) ** 2)
    c = math.exp(gammaln(nu + 0.5) - gammaln(nu) - 0.5 * math.log(math.pi)) * math.sqrt(2 * nu) / ell
    return c * (1 + (ell * kappa) ** 2 / (2 * nu)) ** (-(nu + 0.5))


def _roots_fn(Q):
    """kappa -> roots lam of Q(lam, i kappa) (Q monic or not in tau)."""
    p = sp.Poly(sp.expand(Q), tau)
    cs = [sp.lambdify(xi, c, "numpy") for c in p.all_coeffs()]

    def roots(k):
        return np.roots([complex(c(1j * k)) if callable(c) else complex(c) for c in cs])

    return roots


def _is_real_symbol(Q):
    """Q(lam, i kappa) with real coefficients in (tau, i xi): then kappa < 0 gives conjugates."""
    p = sp.Poly(sp.expand(Q.subs(xi, sp.I * sp.Symbol("k", real=True))), tau, sp.Symbol("k", real=True))
    return all(abs(complex(c).imag) < 1e-12 for c in p.coeffs())


@dataclass
class _Feat:
    j: np.ndarray  # factor index per real feature
    kappa: np.ndarray
    lam: np.ndarray
    part: np.ndarray  # 0 = real part, 1 = imaginary part
    scale: np.ndarray  # 1 / max |e^{lam t}| over the window


def _features(factors, kappa_grid, t_range, tc):
    J, K, L, P, Sc = [], [], [], [], []
    half = 0.5 * (t_range[1] - t_range[0])
    for j, Q in enumerate(factors):
        roots = _roots_fn(Q)
        ks = kappa_grid if _is_real_symbol(Q) else np.r_[-kappa_grid[::-1][:-1], kappa_grid]
        for k in ks:
            for lam in roots(k):
                sc = math.exp(-abs(lam.real) * half)
                for part in (0, 1):
                    if part == 1 and k == 0 and abs(lam.imag) < 1e-14:
                        continue  # identically zero imaginary part
                    J.append(j), K.append(k), L.append(lam), P.append(part), Sc.append(sc)
    return _Feat(np.array(J), np.array(K, float), np.array(L, complex), np.array(P), np.array(Sc))


def _design(F, t, x, tc):
    """Real design matrix (n, M): Re or Im of scale * e^{lam (t - tc) + i kappa x}."""
    z = np.exp(np.outer(np.asarray(t) - tc, F.lam) + 1j * np.outer(np.asarray(x), F.kappa)) * F.scale
    return np.where(F.part[None, :] == 0, z.real, z.imag)


@dataclass
class EPGPPosterior:
    factors: list
    feats: _Feat
    tc: float
    mean_w: np.ndarray
    chol_cov: np.ndarray  # lower Cholesky of the posterior covariance of w
    s_factor: np.ndarray
    ell: float
    sigma_hat: float
    family: str
    info: dict = field(default_factory=dict)

    def _phi(self, t_grid, x_grid):
        TT, XX = np.meshgrid(t_grid, x_grid, indexing="ij")
        return _design(self.feats, TT.ravel(), XX.ravel(), self.tc), TT.shape

    def component_samples(self, S, t_grid, x_grid, seed=0):
        """(S, J, nt, nx) posterior draws of each factor's component on the grid."""
        rng = np.random.default_rng(seed)
        Phi, shp = self._phi(t_grid, x_grid)
        W = self.mean_w[None] + rng.standard_normal((S, len(self.mean_w))) @ self.chol_cov.T
        out = np.empty((S, len(self.factors)) + shp)
        for j in range(len(self.factors)):
            m = self.feats.j == j
            out[:, j] = (W[:, m] @ Phi[:, m].T).reshape((S,) + shp)
        return out

    def component_mean(self, t_grid, x_grid):
        Phi, shp = self._phi(t_grid, x_grid)
        return np.stack([(Phi[:, self.feats.j == j] @ self.mean_w[self.feats.j == j]).reshape(shp)
                         for j in range(len(self.factors))])

    def sample(self, S, t_grid, x_grid, seed=0):
        """(S, nt, nx) draws of u = sum_j u_j; equal weights 1/S."""
        return self.component_samples(S, t_grid, x_grid, seed).sum(1)

    def weights(self, S, t_grid, x_grid, seed=0):
        """(S, J) component weights w_j = ||u_j|| / sum_k ||u_k|| per posterior draw."""
        c = self.component_samples(S, t_grid, x_grid, seed)
        nrm = np.sqrt((c**2).sum(axis=(2, 3)))
        return nrm / nrm.sum(1, keepdims=True)


def fit_epgp(t, x, y, factors, *, family="matern52", kappa_max=None, dkappa=None, period_x=None,
             t_range=None, ell0=1.0):
    """Factor-wise EPGP posterior from scattered samples. `factors`: list of sympy expressions in
    (tau, xi) (pdefactor.symbols), e.g. the factors returned by the core. `family`: spectral
    smoothness of the component prior (pass `smoother(family of u)`, C12-C1)."""
    t, x, y = (np.asarray(a, float) for a in (t, x, y))
    Lx = float(np.ptp(x)) or 1.0
    if dkappa is None:
        dkappa = 2 * math.pi / period_x if period_x is not None else math.pi / Lx
    if kappa_max is None:
        # resolution of the data: mean spacing in x of n points spread over the t-extent
        kappa_max = min(math.pi * math.sqrt(len(y)) / Lx, 40.0)
    kgrid = np.arange(0.0, kappa_max + 1e-12, dkappa)
    t_range = (float(t.min()), float(t.max())) if t_range is None else t_range
    tc = 0.5 * (t_range[0] + t_range[1])
    F = _features(factors, kgrid, t_range, tc)
    Phi = _design(F, t, x, tc)
    n, M = Phi.shape
    J = len(factors)
    PtP, Pty, yy = Phi.T @ Phi, Phi.T @ y, float(y @ y)

    def prior_var(th):
        s = np.exp(th[:J])
        ell = math.exp(th[J])
        return s[F.j] ** 2 * spectral_density(F.kappa, ell, family) * dkappa

    def nlml(th):
        v = prior_var(th) + 1e-14
        s2 = math.exp(2 * th[J + 1])
        A = np.diag(1 / v) + PtP / s2
        try:
            L = np.linalg.cholesky(A)
        except np.linalg.LinAlgError:
            return 1e30
        b = np.linalg.solve(L, Pty / s2)
        quad = yy / s2 - b @ b
        logdet = 2 * np.log(np.diag(L)).sum() + np.log(v).sum() + n * math.log(s2)
        return 0.5 * (quad + logdet + n * math.log(2 * math.pi))

    th0 = np.r_[np.full(J, math.log(np.std(y) + 1e-12)), math.log(ell0), math.log(0.1 * np.std(y) + 1e-12)]
    best = None
    for l0 in (0.3, 1.0, 3.0):
        th0[J] = math.log(l0)
        r = minimize(nlml, th0, method="L-BFGS-B")
        if best is None or r.fun < best.fun:
            best = r
    th = best.x
    v = prior_var(th) + 1e-14
    s2 = math.exp(2 * th[J + 1])
    A = np.diag(1 / v) + PtP / s2
    La = np.linalg.cholesky(A)
    mean_w = np.linalg.solve(A, Pty / s2)
    chol_cov = np.linalg.inv(La).T  # cov = A^-1 = La^-T La^-1 -> factor La^-T
    info = {"nlml": float(best.fun), "M": M, "n": n, "hyper": "type-II ML (plug-in)",
            "kappa_max": kappa_max, "dkappa": dkappa}
    return EPGPPosterior(list(factors), F, tc, mean_w, chol_cov, np.exp(th[:J]), math.exp(th[J]),
                         math.exp(th[J + 1]), family, info)
