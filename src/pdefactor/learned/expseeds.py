"""L0: learned pole-set proposals for the per-bin exponential fit (PHASE4_ML_PLAN.md, L0).

Architecture: Xie, Wakin & Tang, "Data-driven parameter estimation of contaminated damped
exponentials" (Asilomar 2021). A representation net maps the samples to a 2-D damping-frequency
heatmap, and a counting net gives the number of exponentials (the damped extension of DeepFreq,
Izacard et al., NeurIPS 2019). The code is reimplemented here: DeepFreq has no licence and
handles undamped lines only, and no code for Xie et al. was found (sessions/S-PHASE4-ML/RESEARCH.md).

Plane: s = lam * T (T = time span of the series), Re s in RE_S, Im s in IM_S, cells of CELL.
Targets are unit Gaussians at the *detectable* poles only (expsum.detectable): a pole below the
noise carries no information, and learning it would import the training prior (PHASE4 P0).

Use in the pipeline: `enable(model)` sets core.structfit.SEED_PROVIDER. Each proposed pole set is
one more candidate in the per-bin BIC order comparison, with the same refine budget as the pencil
candidates. Seeds can change which candidates are scored, never their score (PHASE4 §0, §2).
`disable()` restores the deterministic pipeline.

The theory leaves this step open: T10 / P2-Q3 (Prony/Hankel conditioning) has no result.
"""
from __future__ import annotations

import numpy as np

from . import expsum

CELL = 0.5  # grid step in s units
RE_GRID = np.arange(expsum.RE_S[0], expsum.RE_S[1] + CELL, CELL)   # 67 cells
IM_GRID = np.arange(expsum.IM_S[0], expsum.IM_S[1] + CELL, CELL)   # 161 cells
PEAK_WIDTH = 0.3  # Gaussian std of a target peak, in s units: pairs >= ~0.8 apart give two maxima


def target_heatmap(s):
    """Sum of unit Gaussians at the poles s (complex, dimensionless), on the (RE_GRID, IM_GRID) grid."""
    H = np.zeros((len(RE_GRID), len(IM_GRID)), np.float32)
    for p in np.atleast_1d(s):
        gr = np.exp(-0.5 * ((RE_GRID - p.real) / PEAK_WIDTH) ** 2)
        gi = np.exp(-0.5 * ((IM_GRID - p.imag) / PEAK_WIDTH) ** 2)
        H = np.maximum(H, np.outer(gr, gi).astype(np.float32))
    return H


def make_batch(rng, n):
    X = np.zeros((n, 4, expsum.NT), np.float32)
    H = np.zeros((n, len(RE_GRID), len(IM_GRID)), np.float32)
    R = np.zeros(n, np.int64)
    for i in range(n):
        d = expsum.draw(rng)
        x, snr = expsum.encode(d.y, d.sigma)
        X[i, :3] = x
        X[i, 3] = np.clip(snr, 0, 4) / 4.0  # log10 SNR, clipped to the training range [0, 4]
        s, _ = expsum.detectable(d)
        H[i] = target_heatmap(s)
        R[i] = len(s)
    return X, H, R


def _torch():
    import torch

    return torch


def build_model(width=64, hidden=512):
    torch = _torch()
    nn = torch.nn
    nre, nim = len(RE_GRID), len(IM_GRID)

    class ExpSeedNet(nn.Module):
        def __init__(self):
            super().__init__()
            self.enc = nn.Sequential(
                nn.Conv1d(4, width, 5, padding=2), nn.GELU(),
                nn.Conv1d(width, width, 5, padding=2), nn.GELU(),
                nn.Conv1d(width, width, 5, padding=2), nn.GELU(),
                nn.Conv1d(width, width, 5, padding=2), nn.GELU(),
            )
            self.trunk = nn.Sequential(nn.Flatten(), nn.Linear(width * expsum.NT, hidden), nn.GELU(),
                                       nn.Linear(hidden, hidden), nn.GELU())
            self.heat = nn.Linear(hidden, nre * nim)
            self.count = nn.Linear(hidden, expsum.MAX_ORDER + 1)

        def forward(self, x):
            h = self.trunk(self.enc(x))
            return self.heat(h).view(-1, nre, nim), self.count(h)

    return ExpSeedNet()


def train(steps=20000, batch=256, lr=1e-3, seed=0, log=None, pool=20000, refresh=2000):
    """Train on fresh draws. A pool of `pool` draws is regenerated every `refresh` steps (draws are
    cheap but Python-bound; the pool keeps the CPU on the network). Returns the model."""
    torch = _torch()
    torch.manual_seed(seed)
    rng = np.random.default_rng(seed)
    model = build_model()
    opt = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-4)
    sched = torch.optim.lr_scheduler.OneCycleLR(opt, max_lr=lr, total_steps=steps)
    ce = torch.nn.CrossEntropyLoss()
    X = H = R = None
    for step in range(steps):
        if step % refresh == 0:
            X, H, R = map(torch.from_numpy, make_batch(rng, pool))
        idx = torch.randint(0, len(X), (batch,))
        ph, pc = model(X[idx])
        loss_h = torch.mean((ph - H[idx]) ** 2) * 100.0
        loss_c = ce(pc, R[idx])
        loss = loss_h + loss_c
        opt.zero_grad()
        loss.backward()
        opt.step()
        sched.step()
        if log and step % 500 == 0:
            log(f"step {step} heat {loss_h.item():.4f} count {loss_c.item():.4f}")
    return model.eval()


def save(model, path):
    _torch().save(model.state_dict(), path)


def load(path):
    torch = _torch()
    model = build_model()
    model.load_state_dict(torch.load(path, map_location="cpu", weights_only=True))
    return model.eval()


def _peaks(H, k):
    """Up to k local maxima of the heatmap, with parabolic sub-cell refinement, as s = re + i im."""
    nre, nim = H.shape
    P = np.pad(H, 1, constant_values=-np.inf)
    core = P[1:-1, 1:-1]
    is_max = np.ones_like(core, bool)
    for di in (-1, 0, 1):
        for dj in (-1, 0, 1):
            if di or dj:
                is_max &= core >= P[1 + di:nre + 1 + di, 1 + dj:nim + 1 + dj]
    ii, jj = np.where(is_max & (core > 0.1))
    order = np.argsort(-core[ii, jj])[:k]
    out = []
    for i, j in zip(ii[order], jj[order]):
        def sub(a, b, c):
            den = a - 2 * b + c
            return 0.0 if den >= 0 else 0.5 * (a - c) / den
        di = sub(P[i, j + 1], P[i + 1, j + 1], P[i + 2, j + 1]) if 0 < i < nre - 1 else 0.0
        dj = sub(P[i + 1, j], P[i + 1, j + 1], P[i + 1, j + 2]) if 0 < j < nim - 1 else 0.0
        out.append(complex(RE_GRID[i] + di * CELL, IM_GRID[j] + dj * CELL))
    return np.array(out, complex)


def predict(model, ys, sigmas):
    """Heatmaps and order probabilities for a list of series (each of length <= expsum.NT)."""
    torch = _torch()
    X = np.zeros((len(ys), 4, expsum.NT), np.float32)
    for i, (y, sg) in enumerate(zip(ys, sigmas)):
        x, snr = expsum.encode(y, sg)
        X[i, :3], X[i, 3] = x, np.clip(snr, 0, 4) / 4.0
    with torch.no_grad():
        ph, pc = model(torch.from_numpy(X))
    return ph.numpy(), torch.softmax(pc, 1).numpy()


def proposals(model, y, dt, sigma, n_orders=3):
    """Pole sets (lam, physical units) for one bin, one per order: for each of the n_orders most
    probable orders r >= 1, the r highest heatmap peaks. When r exceeds the number of peaks (two
    poles closer than the heatmap resolves merge into one maximum), the dominant peak is split
    into a pair +-CELL along the axis where it is widest; VarPro then refines the pair. Series
    longer than expsum.NT are decimated (the time span, and hence the s plane, is kept)."""
    y = np.asarray(y, complex)
    stride = int(np.ceil(len(y) / expsum.NT))
    yd = y[::stride]
    T = (len(yd) - 1) * dt * stride
    if len(yd) < 8 or T <= 0:
        return []
    H, pr = predict(model, [yd], [sigma])
    H, pr = H[0], pr[0]
    peaks = _peaks(H, expsum.MAX_ORDER)
    if len(peaks) == 0:
        return []
    i, j = np.argmin(np.abs(RE_GRID - peaks[0].real)), np.argmin(np.abs(IM_GRID - peaks[0].imag))
    wre = np.sum(H[:, j] > 0.5 * H[i, j])
    wim = np.sum(H[i, :] > 0.5 * H[i, j])
    step = CELL if wre >= wim else 1j * CELL
    split = np.r_[peaks[0] - step, peaks[0] + step, peaks[1:]]
    out = []
    for r in np.argsort(-pr):
        if r >= 1:
            src = peaks if r <= len(peaks) else split
            if r <= len(src):
                out.append(src[:r] / T)
        if len(out) >= n_orders:
            break
    return out


def enable(model, n_orders=3):
    """Switch L0 on for every extract_modes_ic call (core.structfit.SEED_PROVIDER)."""
    from ..core import structfit

    structfit.SEED_PROVIDER = lambda y, dt, sigma: proposals(model, y, dt, sigma, n_orders)


def disable():
    from ..core import structfit

    structfit.SEED_PROVIDER = None
