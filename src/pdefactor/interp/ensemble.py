"""Ablation for step 1: deep ensemble of SIREN (or tanh-MLP) interpolants (Lakshminarayanan et al.
2017; Sitzmann et al. 2020). Each member is trained on the full data with a Gaussian likelihood and
its own learned noise level. The latent field's predictive is N(mean, var) across members. The same
GPPosterior container as the GP is used, so coverage and the core bridge apply unchanged.

No theory: empirical (RESEARCH.md S-INTERP). It is known to be under-dispersed away from the data.
"""
from __future__ import annotations

import math
import time

import numpy as np
import torch
from torch import nn

from .gp import GPPosterior, _grid_axes


class _Sine(nn.Module):
    def __init__(self, fin, fout, w0, first):
        super().__init__()
        self.lin, self.w0 = nn.Linear(fin, fout), w0
        b = 1 / fin if first else math.sqrt(6 / fin) / w0
        nn.init.uniform_(self.lin.weight, -b, b)

    def forward(self, z):
        return torch.sin(self.w0 * self.lin(z))


def _net(arch, width, depth, w0):
    if arch == "siren":
        layers = [_Sine(2, width, w0, True)] + [_Sine(width, width, 1.0, False) for _ in range(depth - 1)]
        last = nn.Linear(width, 1)
        b = math.sqrt(6 / width)
        nn.init.uniform_(last.weight, -b, b)
        return nn.Sequential(*layers, last)
    mods, fin = [], 2
    for _ in range(depth):
        mods += [nn.Linear(fin, width), nn.Tanh()]
        fin = width
    return nn.Sequential(*mods, nn.Linear(fin, 1))


def fit_ensemble(t, x, y, *, grid=None, M=5, arch="siren", width=64, depth=3, w0=6.0, steps=3000,
                 lr=1e-3, device="auto", seed=0, period_x=None):
    """Deep-ensemble posterior on the grid; samples = the M members (pi = 1/M)."""
    t0 = time.perf_counter()
    if device == "auto":
        device = "cuda" if torch.cuda.is_available() else "cpu"
    tg, xg = _grid_axes(t, x, grid, period_x)
    tmn, tr = float(np.min(t)), float(np.ptp(t)) or 1.0
    xmn, xr = float(np.min(x)), float(np.ptp(x)) or 1.0
    ym, ys = float(np.mean(y)), float(np.std(y)) or 1.0
    sc = lambda a, m, r: 2 * (np.asarray(a, float) - m) / r - 1
    Z = torch.tensor(np.c_[sc(t, tmn, tr), sc(x, xmn, xr)], dtype=torch.float32, device=device)
    Y = torch.tensor((np.asarray(y) - ym) / ys, dtype=torch.float32, device=device)
    TT, XX = np.meshgrid(tg, xg, indexing="ij")
    G = torch.tensor(np.c_[sc(TT.ravel(), tmn, tr), sc(XX.ravel(), xmn, xr)], dtype=torch.float32, device=device)
    outs, sigs = [], []
    for m in range(M):
        torch.manual_seed(seed * 1000 + m)
        net = _net(arch, width, depth, w0).to(device)
        log_s = torch.tensor(math.log(0.1), device=device, requires_grad=True)
        opt = torch.optim.Adam(list(net.parameters()) + [log_s], lr=lr)
        for _ in range(steps):
            opt.zero_grad()
            r = net(Z)[:, 0] - Y
            loss = 0.5 * (r * r).mean() * torch.exp(-2 * log_s) + log_s
            loss.backward()
            opt.step()
        with torch.no_grad():
            outs.append(net(G)[:, 0].cpu().numpy().reshape(TT.shape) * ys + ym)
        sigs.append(math.exp(log_s.item()) * ys)
    outs = np.array(outs)
    mean, var = outs.mean(0), outs.var(0, ddof=1) if M > 1 else np.zeros_like(outs[0])
    sd = np.sqrt(np.maximum(var, 1e-14))
    info = {"method": f"ensemble-{arch}", "M": M, "steps": steps, "runtime_s": time.perf_counter() - t0}
    return GPPosterior(tg, xg, outs, np.full(M, 1.0 / M), float(np.mean(sigs)), np.array(sigs), mean, var,
                       mean[None], sd[None], np.ones(1), info)
