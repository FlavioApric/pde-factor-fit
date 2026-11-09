"""Ablation: deep ensemble (SIREN / MLP) vs exact GP on coverage, rmse and runtime.
usage: ensemble_ablation.py out.jsonl [n] [noise] [cases]"""
import json
import sys
import time

import numpy as np

from pdefactor.interp.ensemble import fit_ensemble
from pdefactor.synthetic import case, grid, sample_scattered

out = sys.argv[1]
n = int(sys.argv[2]) if len(sys.argv) > 2 else 2000
nz = float(sys.argv[3]) if len(sys.argv) > 3 else 0.01
cases = sys.argv[4].split(",") if len(sys.argv) > 4 else ["heat", "transport", "transport_plus_diffusion"]
for name in cases:
    f = case(name)
    tg, xg, u = grid(f)
    t, x, y, s = sample_scattered(f, n, noise=nz, rng=1)
    for arch in ["siren", "mlp"]:
        t0 = time.time()
        p = fit_ensemble(t, x, y, grid=(tg, xg), M=5, arch=arch)
        rec = {"case": name, "n": n, "noise": nz, "arch": arch, "cov": {str(k): v for k, v in p.coverage(u).items()},
               "rmse": float(np.sqrt(np.mean((p.mean - u) ** 2))), "sd": float(np.sqrt(p.var.mean())),
               "sigma": s, "sigma_hat": p.sigma_hat, "time": time.time() - t0}
        print(json.dumps(rec), flush=True)
        open(out, "a").write(json.dumps(rec) + chr(10))
