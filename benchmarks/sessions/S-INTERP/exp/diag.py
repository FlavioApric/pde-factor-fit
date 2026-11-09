import sys, time, numpy as np
from pdefactor.synthetic import case, grid, sample_scattered
from pdefactor.interp import fit_gp
name, n, nz = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])
per = 2*np.pi if "per" in sys.argv else None
fams = tuple(a for a in sys.argv[4:] if a != "per") or ("matern32","matern52","rbf")
f = case(name); t, x, y, s = sample_scattered(f, n, noise=nz, rng=int(__import__("os").environ.get("SEED",1))); tg, xg, u = grid(f)
t0 = time.time(); post = fit_gp(t, x, y, grid=(tg, xg), S=8, H=12, period_x=per, families=fams)
print(name, n, nz, per, "time", round(time.time()-t0,1), "sig", round(s,5), "hat", round(post.sigma_hat,5), "fam", {k: round(v,3) for k,v in post.info["family_posterior"].items()})
print("theta_map", {k: np.round(np.exp(np.array(v["theta_map"])),3).tolist() for k,v in post.info["diag"].items()}, "ess", {k: round(v["ess"],1) for k,v in post.info["diag"].items()})
p = post.pit(u); inb = np.abs(p-0.5) <= 0.45
print("cov", {k: round(v,3) for k,v in post.coverage(u).items()})
print("cov90 by t-block", [round(inb[i:i+8].mean(),2) for i in range(0,64,8)])
print("cov90 by x-block", [round(inb[:,j:j+16].mean(),2) for j in range(0,128,16)])
z = (u-post.mean)/np.sqrt(post.var); print("z std", z.std(), "interior z std", z[4:-4,8:-8].std())
