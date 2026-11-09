"""S-AGG-CLUSTER: aggregate on fake posteriors (exact grid + noise draws) for the v1 cases."""
import sys, time
import numpy as np
from pdefactor.synthetic import case, grid
from pdefactor.aggregate import fake_posterior, run_core, aggregate

names = sys.argv[1:] or ["transport_plus_diffusion", "heat"]
for name in names:
    for rel in [1e-3, 1e-2]:
        f = case(name)
        t, x, u = grid(f, nt=48, nx=64)
        sig = rel * u.std()
        us, pis = fake_posterior(u, sig, 8, rng=0)
        t0 = time.time()
        res = run_core(us, t, x, sig, pis)
        a = aggregate(res)
        print(f"== {name} noise={rel} ({time.time()-t0:.1f}s)")
        print(a.summary(), flush=True)
