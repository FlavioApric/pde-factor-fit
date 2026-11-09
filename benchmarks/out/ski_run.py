import sys, time, json, numpy as np
from pdefactor.synthetic import case, grid, sample_scattered
from pdefactor.interp import fit_gp
meth = sys.argv[3] if len(sys.argv) > 3 else "ski"
for name in sys.argv[2].split(","):
    f = case(name); tg, xg, u = grid(f)
    t, x, y, s = sample_scattered(f, int(sys.argv[1]), noise=0.01, rng=1)
    t0 = time.time(); p = fit_gp(t, x, y, grid=(tg, xg), S=8, method=meth); dt = time.time() - t0
    rec = dict(case=name, n=int(sys.argv[1]), noise=0.01, method=meth, cov=p.coverage(u), sigma=s, sigma_hat=p.sigma_hat,
               rmse=float(np.sqrt(np.mean((p.mean - u)**2))), time=dt, finite=bool(np.isfinite(p.samples).all()))
    print(json.dumps(rec)); open("sessions/S-INTERP/out/ski.jsonl", "a").write(json.dumps(rec) + "\n")
