"""Coverage of the GP credible bands on the synthetic cases (REPORT table).
usage: coverage.py OUT.jsonl --cases a,b --n 400,2000 --noise 0.01,0.05 --seeds 1,2 [--fam rbf,...] [--per]"""
import argparse, json, time, numpy as np
from pdefactor.synthetic import case, grid, sample_scattered
from pdefactor.interp import fit_gp
ap = argparse.ArgumentParser(); ap.add_argument("out")
ap.add_argument("--cases", default="transport,heat,advection_diffusion,transport_plus_diffusion,wave,beam,klein_gordon,telegraph,airy")
ap.add_argument("--n", default="400,2000"); ap.add_argument("--noise", default="0.01,0.05"); ap.add_argument("--seeds", default="1,2")
ap.add_argument("--fam", default=None); ap.add_argument("--per", action="store_true"); ap.add_argument("--H", type=int, default=16)
a = ap.parse_args()
kw = {} if a.fam is None else {"families": tuple(a.fam.split(","))}
for name in a.cases.split(","):
    f = case(name); tg, xg, u = grid(f)
    for n in map(int, a.n.split(",")):
        for nz in map(float, a.noise.split(",")):
            for sd in map(int, a.seeds.split(",")):
                t, x, y, s = sample_scattered(f, n, noise=nz, rng=sd)
                t0 = time.time()
                p = fit_gp(t, x, y, grid=(tg, xg), H=a.H, period_x=2*np.pi if a.per else None, want_samples=False, seed=sd, **kw)
                rec = dict(case=name, n=n, noise=nz, seed=sd, per=a.per, cov=p.coverage(u), sigma=s, sigma_hat=p.sigma_hat,
                           rmse=float(np.sqrt(np.mean((p.mean-u)**2))), sd=float(np.sqrt(p.var.mean())),
                           fam=p.info["family_posterior"], ess={k: v["ess"] for k, v in p.info["diag"].items()},
                           method=p.info["method"], time=time.time()-t0)
                print(json.dumps(rec), flush=True)
                open(a.out, "a").write(json.dumps(rec) + "\n")
