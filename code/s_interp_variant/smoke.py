import sys, time, numpy as np
from pdefactor.synthetic import case, grid, sample_scattered
from pdefactor.interp import fit_gp
name, n, nz = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])
f = case(name)
t, x, y, s = sample_scattered(f, n, noise=nz, rng=1)
tg, xg, u = grid(f)
t0 = time.time()
post = fit_gp(t, x, y, grid=(tg, xg), S=16, period_x=2*np.pi if len(sys.argv) > 4 else None)
print(name, n, nz, "time", round(time.time()-t0,1), "sigma", s, "hat", post.sigma_hat)
print("fam", post.info["family_posterior"], "ncomp", post.info["n_components"],
      "ess", {k: round(v["ess"],1) for k, v in post.info["diag"].items()})
print("cov", post.coverage(u), "rmse mean", np.sqrt(np.mean((post.mean-u)**2)), "sd", np.sqrt(post.var.mean()))
print("sample rmse", np.sqrt(np.mean((post.samples-u)**2)), "eff noise", post.effective_noise())
