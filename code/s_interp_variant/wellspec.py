"""Well-specified check: truth drawn from the RBF GP prior; coverage must be nominal (code check)."""
import sys, numpy as np, torch
from pdefactor.interp import fit_gp
from pdefactor.interp.gp import _k1, _chol
n, nz = int(sys.argv[1]), float(sys.argv[2])
res = []
for seed in range(int(sys.argv[3]) if len(sys.argv) > 3 else 3):
    g = torch.Generator().manual_seed(seed)
    tg = torch.linspace(0, 2, 64, dtype=torch.float64); xg = torch.linspace(0, 2*np.pi, 128, dtype=torch.float64)
    Lt = _chol(_k1("rbf", tg, tg, torch.tensor(0.5)), 1e-10); Lx = _chol(_k1("rbf", xg, xg, torch.tensor(0.8)), 1e-10)
    u = (Lt @ torch.randn(64, 128, generator=g, dtype=torch.float64) @ Lx.T).numpy()
    rng = np.random.default_rng(seed); idx = rng.choice(64*128, n, replace=False)
    TT, XX = np.meshgrid(tg.numpy(), xg.numpy(), indexing="ij")
    y = u.ravel()[idx] + nz * rng.standard_normal(n)
    p = fit_gp(TT.ravel()[idx], XX.ravel()[idx], y, grid=(tg.numpy(), xg.numpy()), families=("rbf",), want_samples=False, seed=seed)
    c = p.coverage(u); res.append([c[.5], c[.9], c[.95]])
    print(seed, {k: round(v, 3) for k, v in c.items()}, "sig_hat", round(p.sigma_hat, 4), flush=True)
print("mean", np.round(np.mean(res, 0), 3))
