"""Probe of the outer loop (loop.run_loop) on fake posterior samples. Usage: loop_probe.py case [noise] [S]."""
import sys
import time

import numpy as np

from pdefactor.aggregate import fake_posterior
from pdefactor.loop import run_loop
from pdefactor.synthetic import CASES, case, extra_case, grid

name = sys.argv[1]
nz = float(sys.argv[2]) if len(sys.argv) > 2 else 1e-3
S = int(sys.argv[3]) if len(sys.argv) > 3 else 4
f = case(name) if name in CASES else extra_case(name)
t, x, u = grid(f)
sig = nz * np.std(np.abs(u))
samples, pis = fake_posterior(u, sig, S, rng=1)
t0 = time.time()
r = run_loop(samples, t, x, sig, pis, report_domain=True)
print(f"{name} noise {nz} S={S}  {time.time() - t0:.0f}s")
print(r.summary())
if r.domain:
    print("domain share of factor 0 per block (t rows, x cols):")
    print(np.round(r.domain["share"][0], 2))
