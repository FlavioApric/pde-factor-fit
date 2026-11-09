"""Debug: one cell, one extractor, print the points and the best structure."""
import sys
import time

import numpy as np

from pdefactor.domain.extract import EXTRACTORS
from pdefactor.domain.fit import select_cell
from pdefactor.synthetic import case

method = sys.argv[1] if len(sys.argv) > 1 else "esprit2d"
L = float(sys.argv[2]) if len(sys.argv) > 2 else np.pi
nz = float(sys.argv[3]) if len(sys.argv) > 3 else 1e-3
for name in sys.argv[4:] or ["wave", "transport_plus_diffusion"]:
    f = case(name)
    nx = int(round(128 * L / (2 * np.pi)))
    t = np.linspace(0, 2, 64)
    x = np.linspace(0, L, nx, endpoint=False)
    TT, XX = np.meshgrid(t, x, indexing="ij")
    u = f(TT, XX)
    sig = nz * np.std(u)
    u = u + sig * np.random.default_rng(1).standard_normal(u.shape)
    t0 = time.time()
    e = EXTRACTORS[method](u, t, x, sig)
    t1 = time.time()
    print(name, e.info, len(e.modes), f"{t1 - t0:.1f}s", "rss/(N s^2)", e.rss / max(sig, 1e-300) ** 2 / u.size)
    for i in np.argsort(e.modes.kappa):
        print(f"  k={e.modes.kappa[i]:+.4f} lam={e.modes.lam[i]:.4f} sl={e.sig_lam[i]:.1e} sk={e.sig_kappa[i]:.1e}")
    b, r, _ = select_cell(e)
    if b is not None:
        print(" ", b.structure, [str(Q.to_sympy(tol=1e-3)) for Q in b.factors], f"p={r[0][2]:.2f}", f"{time.time() - t1:.1f}s")
