"""Step 1 of the pipeline: GP posterior on a uniform (t, x) grid from scattered noisy samples.

Model (standardised data): y_i = c + f(t_i, x_i) + eps_i, eps ~ N(0, s_n^2), and

    f ~ GP(0, sum_r s_r^2 k_t^(r)(t, t') k_x^(r)(x, x')),

a sum of R separable terms (R = 1 is the plain separable kernel). A family is a string such as
"rbf", "matern52" or "rbf+rbf". The sum is there because u = sum_j u_j with ker P = sum ker Q_j
(C12-T1, THEORY_TO_ALGO T1): the components of different factors have different (t, x) correlation
lengths, and one separable term undercovers on such fields (REPORT.md). The families get a
posterior from their evidence. x can be periodic, with the period given as prior knowledge.

Hyperparameters theta = ((log s_r, log l_t^r, log l_x^r)_r, log s_n, c) are marginalised (rule 4):
- "laplace": type-II MAP (multi-start on a subset, refined on all data), Laplace N(theta_hat, H^-1),
  then truncated importance reweighting of draws from a multivariate-t version of it:
  pi_h ∝ p(y, theta_h) / q(theta_h). The same weights estimate the family evidence. ESS reported.
- "nuts": NUTS on theta (NumPyro, CPU), equal weights; for small n.
- "subset" (default for n > n_exact): the exact "laplace" path on a random subset of n_exact points.
  It is a true posterior given less data, so its bands are conservative (wider) rather than overconfident.
- "ski": KISS-GP (GPyTorch) on the output grid; type-II ML only (flagged in info). EXPERIMENTAL:
  not calibrated (REPORT.md), opt-in only.

Each hyperparameter draw is a Gaussian component of the posterior. Its exact marginals on the grid
are kept, so the PIT of the truth is exact. Its function samples come from pathwise conditioning
(Matheron's rule): an exact prior draw on the grid (Kronecker Cholesky per term), the exact
conditional prior at the data given that draw, and the data update. No N x N grid covariance is
ever formed.

Theory: T12/T18 (Monte Carlo over interpolants), T15 (sigma is a posterior quantity), T11
(components need a smoother prior: `smoother`), T26 (derivative errors are amplified).
"""
from __future__ import annotations

import math
import time
from dataclasses import dataclass, field

import numpy as np
import torch
from scipy.special import logsumexp
from scipy.stats import multivariate_t, norm

FAMILIES = ("matern12", "matern32", "matern52", "rbf")
_ORDER = {f: i for i, f in enumerate(FAMILIES)}
# Matern-5/2 (plain, time envelope, sum of two), mixed by evidence. Coverage within +-5 points at
# n = 400 and 2000, 1 % and 5 % (REPORT section 2; one cell +5.3, conservative). RBF undercovers at
# n = 2000, Matern-3/2 overcovers at n = 400, and evidence over their union always picks RBF.
DEFAULT_FAMILIES = ("matern52", "matern52e", "matern52e+matern52e")


def smoother(family: str) -> str:
    """One order smoother kernel (C12-C1: components lose one derivative, so their prior is one
    order smoother than the prior of u). Matern nu -> nu + 1; RBF stays RBF. Applied per term."""
    out = []
    for f in _terms(family):
        b, env = _base(f)
        out.append(FAMILIES[min(_ORDER[b] + 1, len(FAMILIES) - 1)] + ("e" if env else ""))
    return "+".join(out)


def _terms(family):
    return family.split("+")


def _base(term):
    """'rbfe' -> ('rbf', True): a trailing 'e' adds the time envelope e^{beta (t + t' - 1)}."""
    return (term[:-1], True) if term.endswith("e") and term[:-1] in _ORDER else (term, False)


def _npar(term):
    return 4 if _base(term)[1] else 3


def _kt(term, a, b, ell, beta):
    """Time kernel of one term: stationary base kernel, times the envelope e^{beta (t + t' - 1)}
    when the term has one (modes e^{lam t} of a PDE solution, R2-T6; t scaled to [0, 1])."""
    k = _k1(_base(term)[0], a, b, ell)
    return k if beta is None else k * torch.exp(beta * (a[:, None] + b[None, :] - 1.0))


def _k1(fam, a, b, ell, period=None):
    """1-D stationary kernel matrix k(a_i, b_j) with unit variance."""
    fam = _base(fam)[0]
    d = (a[:, None] - b[None, :]).abs()
    if period is not None:
        s = torch.sin(math.pi * d / period)
        return torch.exp(-2.0 * s * s / ell**2)
    r = d / ell
    if fam == "rbf":
        return torch.exp(-0.5 * r * r)
    if fam == "matern12":
        return torch.exp(-r)
    if fam == "matern32":
        q = math.sqrt(3.0) * r
        return (1 + q) * torch.exp(-q)
    if fam == "matern52":
        q = math.sqrt(5.0) * r
        return (1 + q + q * q / 3.0) * torch.exp(-q)
    raise KeyError(fam)


def _chol(A, jitter=1e-10):
    """Cholesky with escalating diagonal jitter (relative to the mean diagonal)."""
    scale = A.diagonal().mean().abs().item() or 1.0
    eye = torch.eye(A.shape[0], dtype=A.dtype, device=A.device)
    j = jitter
    for _ in range(8):
        L, info = torch.linalg.cholesky_ex(A + j * scale * eye)
        if info.item() == 0:
            return L
        j *= 100
    raise torch.linalg.LinAlgError("cholesky failed")


# ------------------------------------------------------------------ priors on theta (standardised units)
# per term: log s ~ N(0, 1.5^2); log l ~ N(log 0.2, 1.5^2) (coordinates scaled to [0, 1]);
# log s_n ~ N(log 0.05, 2.5^2) (0.03 % .. 700 % of the std at 2 sd); c ~ N(0, 1).
# envelope rate beta ~ N(0, 2^2) per unit of scaled time.
def _prior(fams):
    mu, sd = [], []
    for f in fams:
        mu += [0.0, math.log(0.2), math.log(0.2)] + ([0.0] if _base(f)[1] else [])
        sd += [1.5, 1.5, 1.5] + ([2.0] if _base(f)[1] else [])
    return np.r_[mu, math.log(0.05), 0.0], np.r_[sd, 2.5, 1.0]


class _Data:
    def __init__(self, t, x, y, period_x, device):
        self.t0, self.tr = float(np.min(t)), float(np.ptp(t)) or 1.0
        self.x0, self.xr = float(np.min(x)), float(np.ptp(x)) or 1.0
        self.ym, self.ys = float(np.mean(y)), float(np.std(y)) or 1.0
        self.dev = device
        self.t, self.x = self.tens(self.st(t)), self.tens(self.sx(x))
        self.y = self.tens((np.asarray(y, float) - self.ym) / self.ys)
        self.period = None if period_x is None else period_x / self.xr
        self.n = len(self.y)

    def st(self, t):
        return (np.asarray(t, float) - self.t0) / self.tr

    def sx(self, x):
        return (np.asarray(x, float) - self.x0) / self.xr

    def tens(self, a):
        return torch.as_tensor(np.asarray(a, float), dtype=torch.float64, device=self.dev)

    def subset(self, m, seed=0):
        idx = torch.as_tensor(np.random.default_rng(seed).choice(self.n, m, replace=False), device=self.dev)
        S = object.__new__(_Data)
        S.__dict__.update(self.__dict__)
        S.t, S.x, S.y, S.n = self.t[idx], self.x[idx], self.y[idx], m
        return S


def _unpack(th, fams):
    """theta -> [(s, l_t, l_x, beta or None)] per term, s_n, c."""
    terms, i = [], 0
    for f in fams:
        beta = th[i + 3] if _base(f)[1] else None
        terms.append((torch.exp(th[i]), torch.exp(th[i + 1]), torch.exp(th[i + 2]), beta))
        i += _npar(f)
    return terms, torch.exp(th[i]), th[i + 1]


def _neg_log_joint(family, D, th):
    """-log p(y, theta) = -log p(y | theta) - log p(theta)."""
    fams = _terms(family)
    terms, sn, c = _unpack(th, fams)
    K = sn**2 * torch.eye(D.n, dtype=torch.float64, device=D.dev)
    for f, (s, lt, lx, b) in zip(fams, terms):
        K = K + s**2 * _kt(f, D.t, D.t, lt, b) * _k1(f, D.x, D.x, lx, D.period)
    L = _chol(K, 1e-9)
    r = (D.y - c)[:, None]
    a = torch.cholesky_solve(r, L)
    nll = 0.5 * (r * a).sum() + torch.log(L.diagonal()).sum() + 0.5 * D.n * math.log(2 * math.pi)
    mu, sd = (torch.as_tensor(v, dtype=th.dtype, device=th.device) for v in _prior(fams))
    nlp = 0.5 * (((th - mu) / sd) ** 2).sum() + torch.log(sd).sum() + 0.5 * len(th) * math.log(2 * math.pi)
    return nll + nlp


def _starts(fams, device):
    R = len(fams)
    if R == 1:
        ls = [[(0.08, 0.08)], [(0.25, 0.25)], [(0.8, 0.8)]]
    else:  # one short and one long term, both orientations
        ls = [[(0.08, 0.08), (0.6, 0.3)], [(0.15, 0.05), (1.0, 0.15)], [(0.05, 0.15), (0.3, 0.8)]]
    out = []
    for combo in ls:
        v = []
        for f, (lt, lx) in zip(fams, combo):
            v += [math.log(1 / math.sqrt(R)), math.log(lt), math.log(lx)] + ([0.0] if _base(f)[1] else [])
        out.append(torch.tensor(v + [math.log(0.1), 0.0], dtype=torch.float64, device=device))
    return out


def _map_from(family, D, starts, max_iter=100):
    best = None
    for th0 in starts:
        th = th0.clone().requires_grad_(True)
        opt = torch.optim.LBFGS([th], lr=1, max_iter=max_iter, line_search_fn="strong_wolfe",
                                tolerance_grad=1e-6, tolerance_change=1e-9)

        def closure():
            opt.zero_grad()
            v = _neg_log_joint(family, D, th)
            v.backward()
            return v

        try:
            opt.step(closure)
            v = _neg_log_joint(family, D, th).item()
        except (torch.linalg.LinAlgError, RuntimeError):
            continue
        if np.isfinite(v) and (best is None or v < best[0]):
            best = (v, th.detach().clone())
    if best is None:
        raise RuntimeError(f"MAP failed for family {family}")
    return best


def _map(family, D, n_sub=600):
    """Type-II MAP: multi-start on a random subset (when n > n_sub), then refine on all data."""
    starts = _starts(_terms(family), D.dev)
    if D.n > n_sub:
        _, th = _map_from(family, D.subset(n_sub), starts)
        return _map_from(family, D, [th], max_iter=40)
    return _map_from(family, D, starts)


def _hessian(family, D, th0, h=1e-4):
    """Hessian of -log p(y, theta) by central differences of the autograd gradient."""
    def grad(th):
        z = th.clone().requires_grad_(True)
        v = _neg_log_joint(family, D, z)
        (g,) = torch.autograd.grad(v, z)
        return g.cpu().numpy()

    d = len(th0)
    Hm = np.empty((d, d))
    for i in range(d):
        e = torch.zeros_like(th0)
        e[i] = h
        Hm[i] = (grad(th0 + e) - grad(th0 - e)) / (2 * h)
    return 0.5 * (Hm + Hm.T)


def _laplace_is(family, D, H, rng, df=4.0, inflate=1.2):
    """Laplace around the MAP + truncated importance reweighting with a multivariate-t proposal.
    Returns draws (H, d), normalised weights, log-evidence estimate, diagnostics."""
    v0, th0 = _map(family, D)
    w, V = np.linalg.eigh(_hessian(family, D, th0))
    w = np.maximum(w, 1e-3)
    cov = (V / w) @ V.T * inflate**2
    th0n = th0.cpu().numpy()
    q = multivariate_t(loc=th0n, shape=cov, df=df)
    draws = np.vstack([th0n, q.rvs(H - 1, random_state=rng).reshape(H - 1, -1)])
    logp = np.empty(H)
    for i, th in enumerate(draws):
        try:
            logp[i] = -_neg_log_joint(family, D, D.tens(th)).item()
        except (torch.linalg.LinAlgError, RuntimeError):
            logp[i] = -np.inf
    lw = logp - q.logpdf(draws)
    # the MAP point is included as a member; the evidence uses the random draws only
    logZ = float(logsumexp(lw[1:]) - math.log(H - 1))
    lap = float(-v0 + 0.5 * len(th0n) * math.log(2 * math.pi) - 0.5 * np.sum(np.log(w)))
    lw_t = np.minimum(lw, logsumexp(lw) - math.log(H) + 0.5 * math.log(H))  # truncated IS (Ionides 2008)
    pw = np.exp(lw_t - logsumexp(lw_t))
    return draws, pw, logZ, {"theta_map": th0n, "ess": float(1.0 / np.sum(pw**2)), "log_evidence_laplace": lap}


def _nuts(family, D, H, seed, warmup=300):
    """NUTS on theta with NumPyro (CPU, float64); H thinned draws with equal weights."""
    import jax
    import jax.numpy as jnp
    import numpyro
    import numpyro.distributions as dist
    from numpyro.infer import MCMC, NUTS

    jax.config.update("jax_enable_x64", True)
    t, x, y = (jnp.asarray(a.cpu().numpy()) for a in (D.t, D.x, D.y))
    per, fams = D.period, _terms(family)
    mu, sd = _prior(fams)

    def k1(f, a, b, ell, periodic):
        d = jnp.abs(a[:, None] - b[None, :])
        if periodic and per is not None:
            s = jnp.sin(jnp.pi * d / per)
            return jnp.exp(-2 * s * s / ell**2)
        r = d / ell
        f = _base(f)[0]
        if f == "rbf":
            return jnp.exp(-0.5 * r * r)
        if f == "matern12":
            return jnp.exp(-r)
        if f == "matern32":
            q = jnp.sqrt(3.0) * r
            return (1 + q) * jnp.exp(-q)
        q = jnp.sqrt(5.0) * r
        return (1 + q + q * q / 3) * jnp.exp(-q)

    def model():
        th = numpyro.sample("th", dist.Normal(jnp.asarray(mu), jnp.asarray(sd)).to_event(1))
        K, i = 0.0, 0
        for f in fams:
            s, lt, lx = jnp.exp(th[i]), jnp.exp(th[i + 1]), jnp.exp(th[i + 2])
            kt = k1(f, t, t, lt, False)
            if _base(f)[1]:
                kt = kt * jnp.exp(th[i + 3] * (t[:, None] + t[None, :] - 1.0))
            K = K + s**2 * kt * k1(f, x, x, lx, True)
            i += _npar(f)
        K = K + (jnp.exp(2 * th[i]) + 1e-9) * jnp.eye(len(y))
        numpyro.sample("y", dist.MultivariateNormal(th[i + 1] * jnp.ones(len(y)), covariance_matrix=K), obs=y)

    mcmc = MCMC(NUTS(model), num_warmup=warmup, num_samples=4 * H, progress_bar=False)
    mcmc.run(jax.random.PRNGKey(seed))
    th = np.asarray(mcmc.get_samples()["th"])[::4][:H]
    return th, np.full(len(th), 1.0 / len(th))


# ------------------------------------------------------------------ posterior on the grid, one component
def _component(family, D, th, tg, xg, R, gen, want_samples=True):
    """Exact marginals on the grid and R pathwise samples for one hyperparameter value th."""
    fams = _terms(family)
    terms, sn, c = _unpack(D.tens(th), fams)
    n, nt, nx = D.n, len(tg), len(xg)
    eye = torch.eye(n, dtype=torch.float64, device=D.dev)
    KtX, KxX, Kyy = [], [], sn**2 * eye
    for f, (s, lt, lx, b) in zip(fams, terms):
        KtX.append(_kt(f, tg, D.t, lt, b))  # (nt, n)
        KxX.append(_k1(f, xg, D.x, lx, D.period))  # (nx, n)
        Kyy = Kyy + s**2 * _kt(f, D.t, D.t, lt, b) * _k1(f, D.x, D.x, lx, D.period)
    L = _chol(Kyy, 1e-10)

    def cross(vec_or_mat):  # K(grid, X) @ v for v (n,) or (n, R): sum over terms
        v = vec_or_mat if vec_or_mat.dim() == 2 else vec_or_mat[:, None]
        out = sum(s**2 * torch.einsum("in,jn,nr->rij", kt, kx, v) for (s, *_), kt, kx in zip(terms, KtX, KxX))
        return out if vec_or_mat.dim() == 2 else out[0]

    alpha = torch.cholesky_solve((D.y - c)[:, None], L)[:, 0]
    mean = c + cross(alpha)
    prior_var = sum(s**2 * _kt(f, tg, tg, lt, b).diagonal() for f, (s, lt, _, b) in zip(fams, terms))  # (nt,)
    var = torch.empty(nt, nx, dtype=torch.float64, device=D.dev)
    for i in range(nt):  # var = prior - || L^-1 k_X(g) ||^2, by t-rows to bound memory
        kg = sum(s**2 * kt[i][None, :] * kx for (s, *_), kt, kx in zip(terms, KtX, KxX))  # (nx, n)
        V = torch.linalg.solve_triangular(L, kg.T, upper=False)
        var[i] = prior_var[i] - (V * V).sum(0)
    out = {"mean": mean, "sd": var.clamp_min(1e-14).sqrt()}
    if not want_samples or R == 0:
        return out
    # Matheron: per term, exact prior draw on the grid (Kronecker) and at X given it; then update
    fg = torch.zeros(R, nt, nx, dtype=torch.float64, device=D.dev)
    fX = torch.zeros(R, n, dtype=torch.float64, device=D.dev)
    for f, (s, lt, lx, b), kt, kx in zip(fams, terms, KtX, KxX):
        Lt = _chol(_kt(f, tg, tg, lt, b), 1e-8)
        Lx = _chol(_k1(f, xg, xg, lx, D.period), 1e-8)
        z = torch.randn(R, nt, nx, dtype=torch.float64, device=D.dev, generator=gen)
        fg = fg + s * Lt @ z @ Lx.T
        Wt = torch.linalg.solve_triangular(Lt, kt, upper=False).T  # (n, nt)
        Wx = torch.linalg.solve_triangular(Lx, kx, upper=False).T  # (n, nx)
        C = s**2 * (_kt(f, D.t, D.t, lt, b) * _k1(f, D.x, D.x, lx, D.period) - (Wt @ Wt.T) * (Wx @ Wx.T))
        Lc = _chol(0.5 * (C + C.T) + 1e-9 * s**2 * eye, 1e-9)
        fX = fX + s * torch.einsum("mi,rij,mj->rm", Wt, z, Wx) \
            + (Lc @ torch.randn(n, R, dtype=torch.float64, device=D.dev, generator=gen)).T
    eps = sn * torch.randn(R, n, dtype=torch.float64, device=D.dev, generator=gen)
    A = torch.cholesky_solve(((D.y - c)[None, :] - fX - eps).T, L)  # (n, R)
    out["samples"] = c + fg + cross(A)
    return out


# ------------------------------------------------------------------ result
@dataclass
class GPPosterior:
    t: np.ndarray
    x: np.ndarray
    samples: np.ndarray  # (S, nt, nx)
    weights: np.ndarray  # (S,)
    sigma_hat: float
    sigma_samples: np.ndarray  # (S,)
    mean: np.ndarray
    var: np.ndarray
    comp_mean: np.ndarray  # (H, nt, nx) marginal mean of each hyperparameter component
    comp_sd: np.ndarray  # (H, nt, nx)
    comp_weights: np.ndarray  # (H,)
    info: dict = field(default_factory=dict)

    def pit(self, u_true):
        """Mixture CDF of the posterior at the true field, per grid point (exact, no MC)."""
        z = (np.asarray(u_true)[None] - self.comp_mean) / self.comp_sd
        return np.tensordot(self.comp_weights, norm.cdf(z), axes=1)

    def coverage(self, u_true, levels=(0.5, 0.9, 0.95)):
        """Fraction of grid points whose central credible band at each level covers the truth."""
        p = self.pit(u_true)
        return {lv: float(np.mean(np.abs(p - 0.5) <= lv / 2)) for lv in levels}

    def effective_noise(self, kind="smooth", r=4, factor=math.sqrt(2.0)):
        """Noise std to hand to the core (which assumes white noise: bin_noise = noise / sqrt(nx)).

        The error of a GP sample is not white: in each FFT bin it is a smooth function of t, so it
        lies in the same low-dimensional subspace as the exponentials the pencil fits, and its whole
        power biases lam (REPORT: a separable prior even produces a spurious factor tau + c). kind=
        "smooth" (default) returns the white level with the same power per dimension after
        projection on an r-dim smooth subspace of t (Legendre, r = 4), b^2 = tr(P_V C_k) / r,
        maximised over bins. kind="white" uses the plain per-bin variance averaged over the bins
        (it understates the error ~3x on TPD). factor sqrt(2): û_s - u_true = (û_s - mean) -
        (u_true - mean) under calibration."""
        d = self.samples - self.mean[None]
        nt, nx = d.shape[-2:]
        B = np.fft.fft(d, axis=-1) / nx  # (S, nt, nx)
        w = self.weights[:, None]
        if kind == "white":
            b2 = np.sum(w[..., None] * np.abs(B) ** 2, axis=0).mean()
        else:
            from numpy.polynomial import legendre

            Q, _ = np.linalg.qr(legendre.legvander(np.linspace(-1, 1, nt), r - 1))
            P = np.einsum("ta,stk->sak", Q, B)  # coefficients on the smooth subspace
            b2 = (np.sum(w * (np.abs(P) ** 2).sum(1), axis=0) / r).max()
        return float(factor * math.sqrt(b2) * math.sqrt(nx))


def _grid_axes(t, x, grid, period_x):
    if grid is None:
        grid = (64, 128)
    tg, xg = grid
    if np.isscalar(tg):
        tg = np.linspace(np.min(t), np.max(t), int(tg))
    if np.isscalar(xg):
        if period_x is not None:
            x0 = np.floor(np.min(x) / period_x) * period_x
            xg = x0 + np.linspace(0, period_x, int(xg), endpoint=False)
        else:
            xg = np.linspace(np.min(x), np.max(x), int(xg))
    return np.asarray(tg, float), np.asarray(xg, float)


def fit_gp(t, x, y, *, grid=None, S=32, H=16, families=DEFAULT_FAMILIES, period_x=None,
           method="auto", device="auto", seed=0, n_exact=6000, n_nuts=300, min_family_prob=1e-3,
           want_samples=True):
    """GP posterior samples on a uniform grid from scattered samples (t_i, x_i, y_i).

    grid: (t_grid, x_grid) arrays or (nt, nx) sizes (default (64, 128) over the data box).
    S: number of function samples; H: hyperparameter draws per kernel family.
    families: kernel families compared by evidence ("rbf", "matern52", "rbf+rbf", ...).
    period_x: known period in x (prior knowledge, e.g. a periodic domain); None = not periodic.
    method: "auto" (nuts if n <= n_nuts, laplace if n <= n_exact, else subset), or one of
    "nuts", "laplace", "subset", "ski" (experimental).
    Returns a GPPosterior with samples, weights pi_s and sigma_hat (data units)."""
    t0 = time.perf_counter()
    y = np.asarray(y)
    if np.iscomplexobj(y):
        raise NotImplementedError("complex data: fit Re and Im separately")
    n = len(y)
    if device == "auto":
        device = "cuda" if torch.cuda.is_available() else "cpu"
    if method == "auto":
        method = "nuts" if n <= n_nuts else ("laplace" if n <= n_exact else "subset")
    tg_np, xg_np = _grid_axes(t, x, grid, period_x)
    if method == "subset":
        idx = np.sort(np.random.default_rng(seed).choice(n, min(n_exact, n), replace=False))
        p = fit_gp(np.asarray(t)[idx], np.asarray(x)[idx], y[idx], grid=(tg_np, xg_np), S=S, H=H,
                   families=families, period_x=period_x, method="laplace", device=device, seed=seed,
                   n_exact=n_exact, min_family_prob=min_family_prob, want_samples=want_samples)
        p.info.update(method="subset", n=n, n_used=len(idx), runtime_s=time.perf_counter() - t0)
        return p
    if method == "ski":
        from .ski import fit_ski

        return fit_ski(t, x, y, tg_np, xg_np, S=S, family="rbf",
                       period_x=period_x, device=device, seed=seed)
    rng = np.random.default_rng(seed)
    D = _Data(t, x, y, period_x, device)
    tg, xg = D.tens(D.st(tg_np)), D.tens(D.sx(xg_np))
    fam_res = {}
    for fam in families:
        draws, pw, logZ, diag = _laplace_is(fam, D, H, rng)
        if method == "nuts":  # the evidence for the family comparison still comes from Laplace-IS
            draws, pw = _nuts(fam, D, H, seed)
            diag = dict(diag, method="nuts")
        fam_res[fam] = (draws, pw, logZ, diag)
    logZs = np.array([fam_res[f][2] for f in families])
    pfam = np.exp(logZs - logsumexp(logZs))
    gen = torch.Generator(device=device).manual_seed(seed)
    comps = []  # (family, theta, weight)
    for f, pf in zip(families, pfam):
        if pf < min_family_prob:
            continue
        for th_h, w_h in zip(fam_res[f][0], fam_res[f][1]):
            if w_h * pf > 1e-6:
                comps.append((f, th_h, w_h * pf))
    W = np.array([c[2] for c in comps])
    W /= W.sum()
    counts = np.floor(W * S).astype(int)  # samples per component ∝ weight
    for i in np.argsort(-(W * S - counts))[: S - counts.sum()]:
        counts[i] += 1
    cm, csd, samples, sw, ssig = [], [], [], [], []
    sig_c = np.array([math.exp(th[-2]) * D.ys for f, th, _ in comps])
    for (f, th_h, w_h), r, sg in zip(comps, counts, sig_c):
        out = _component(f, D, th_h, tg, xg, int(r) if want_samples else 0, gen, want_samples)
        cm.append(out["mean"].cpu().numpy() * D.ys + D.ym)
        csd.append(out["sd"].cpu().numpy() * D.ys)
        if want_samples and r > 0:
            samples.append(out["samples"].cpu().numpy() * D.ys + D.ym)
            sw += [w_h / r] * r
            ssig += [sg] * r
    cm, csd, sw = np.array(cm), np.array(csd), np.array(sw)
    mean = np.tensordot(W, cm, axes=1)
    var = np.tensordot(W, csd**2 + cm**2, axes=1) - mean**2
    info = {
        "method": method, "n": n, "family_posterior": dict(zip(families, pfam.tolist())),
        "log_evidence": dict(zip(families, logZs.tolist())),
        "diag": {f: {k: (v.tolist() if isinstance(v, np.ndarray) else v) for k, v in fam_res[f][3].items()}
                 for f in families},
        "n_components": len(comps), "device": device, "runtime_s": time.perf_counter() - t0,
        "sigma_sd": float(np.sqrt(np.sum(W * (sig_c - np.sum(W * sig_c)) ** 2))),
    }
    smp = np.concatenate(samples) if samples else np.zeros((0, len(tg_np), len(xg_np)))
    return GPPosterior(tg_np, xg_np, smp, sw / sw.sum() if len(sw) else sw, float(np.sum(W * sig_c)),
                       np.array(ssig), mean, var, cm, csd, W, info)
