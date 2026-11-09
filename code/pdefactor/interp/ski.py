"""EXPERIMENTAL (not calibrated, opt-in via method="ski"; the large-n default is "subset", REPORT.md).
Large-n path of step 1: KISS-GP / SKI (Wilson & Nickisch 2015) with GPyTorch. The inducing grid
is the output grid itself, so the posterior on it is read directly; samples by LOVE
(`fast_pred_samples`). Hyperparameters by type-II ML only: their uncertainty is NOT propagated on
this path (info["hyper_uncertainty"] = False), so its bands are expected to be narrower than those
of the exact Laplace/NUTS path. One ARD-RBF term (separable), no envelope, no periodicity.
"""
from __future__ import annotations

import math
import time

import gpytorch
import numpy as np
import torch

from .gp import GPPosterior


class _SKI(gpytorch.models.ExactGP):
    def __init__(self, X, y, lik, family, grid_size, bounds, period):
        super().__init__(X, y, lik)
        self.mean_module = gpytorch.means.ConstantMean()

        # ARD RBF = product of 1-D RBFs, so the kernel is separable; GridKernel needs a kernel on
        # both dims (a ProductKernel with active_dims is not supported). Periodicity is not used here.
        if family == "rbf":
            base = gpytorch.kernels.RBFKernel(ard_num_dims=2)
        else:
            nu = {"matern12": 0.5, "matern32": 1.5, "matern52": 2.5}[family]
            base = gpytorch.kernels.MaternKernel(nu=nu, ard_num_dims=2)  # not separable (ARD distance)
        self.covar_module = gpytorch.kernels.ScaleKernel(
            gpytorch.kernels.GridInterpolationKernel(base, grid_size=grid_size, num_dims=2, grid_bounds=bounds))

    def forward(self, X):
        return gpytorch.distributions.MultivariateNormal(self.mean_module(X), self.covar_module(X))


def fit_ski(t, x, y, tg, xg, *, S=32, family="rbf", period_x=None, device="cuda", seed=0, iters=60, lr=0.01,
            n_init=1000):
    t0 = time.perf_counter()
    torch.manual_seed(seed)
    ym, ys = float(np.mean(y)), float(np.std(y)) or 1.0
    tmn, tr = float(np.min(tg)), float(np.ptp(tg)) or 1.0
    xmn, xr = float(np.min(xg)), float(np.ptp(xg)) or 1.0
    f32 = lambda a: torch.as_tensor(np.asarray(a, float), dtype=torch.float32, device=device)
    X = torch.stack([f32((t - tmn) / tr), f32((x - xmn) / xr)], -1)
    Y = f32((np.asarray(y) - ym) / ys)
    pad_t, pad_x = 2.0 / (len(tg) - 1), 2.0 / max(len(xg) - 1, 1)
    bounds = [(-pad_t, 1 + pad_t), (-pad_x, 1 + pad_x)]
    lik = gpytorch.likelihoods.GaussianLikelihood().to(device)
    per = None if period_x is None else period_x / xr
    model = _SKI(X, Y, lik, family, [len(tg) + 4, len(xg) + 4], bounds, per).to(device)
    # initialise from the exact-path MAP on a random subset (Adam from the default init can stall
    # with all signal in the noise); same scaling: t, x to [0, 1], y standardised
    from .gp import _Data, _map

    rng = np.random.default_rng(seed)
    idx = rng.choice(len(y), min(n_init, len(y)), replace=False)
    D = _Data(t[idx], x[idx], np.asarray(y)[idx], None, device)
    _, th = _map(family, D)
    th = th.cpu().numpy()
    ell = np.exp(th[1:3]) * np.array([D.tr / tr, D.xr / xr])
    model.covar_module.outputscale = float(np.exp(2 * th[0])) * (D.ys / ys) ** 2
    model.covar_module.base_kernel.base_kernel.lengthscale = torch.tensor(ell, dtype=torch.float32, device=device)
    lik.noise = max(float(np.exp(2 * th[3])) * (D.ys / ys) ** 2, 2e-4)  # GPyTorch noise floor 1e-4
    model.mean_module.constant.data.fill_(float(th[4] * D.ys + D.ym - ym) / ys)
    model.train(), lik.train()
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    mll = gpytorch.mlls.ExactMarginalLogLikelihood(lik, model)
    with gpytorch.settings.max_cg_iterations(500), gpytorch.settings.cg_tolerance(1e-2):
        for _ in range(iters):
            opt.zero_grad()
            loss = -mll(model(X), Y)
            loss.backward()
            opt.step()
    model.eval(), lik.eval()
    TT, XX = np.meshgrid((tg - tmn) / tr, (xg - xmn) / xr, indexing="ij")
    G = torch.stack([f32(TT.ravel()), f32(XX.ravel())], -1)
    shp = TT.shape
    with torch.no_grad(), gpytorch.settings.fast_pred_var(), gpytorch.settings.fast_pred_samples(), \
            gpytorch.settings.max_root_decomposition_size(200):
        post = model(G)
        mean = post.mean.cpu().numpy().reshape(shp) * ys + ym
        var = post.variance.clamp_min(1e-12).cpu().numpy().reshape(shp) * ys**2
        smp = post.rsample(torch.Size([S])).cpu().numpy().reshape((S,) + shp) * ys + ym
    sig = math.sqrt(lik.noise.item()) * ys
    info = {"method": "ski", "n": len(y), "hyper_uncertainty": False, "family": family,
            "runtime_s": time.perf_counter() - t0, "device": device}
    return GPPosterior(np.asarray(tg), np.asarray(xg), smp, np.full(S, 1.0 / S), sig, np.full(S, sig),
                       mean, var, mean[None], np.sqrt(var)[None], np.ones(1), info)
