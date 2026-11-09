"""S-AGG-CLUSTER probe: core v2 timing and output on whole-domain and windowed cells."""
import time
import numpy as np
from pdefactor.synthetic import case, grid
from pdefactor.core.structfit import analyze_structured

for name in ["transport_plus_diffusion", "heat", "transport"]:
    f = case(name)
    t, x, u = grid(f, nt=48, nx=64)
    for noise in [0.0, 1e-2]:
        rng = np.random.default_rng(1)
        s = noise * u.std()
        t0 = time.time()
        r = analyze_structured(u + s * rng.standard_normal(u.shape), t, x, noise=s, real=True)
        print(name, noise, f"{time.time()-t0:.1f}s", r.label, [(st, round(p, 3)) for st, _, p in r.structures[:3]])
        for fr in r.factors:
            print("   ", fr.symbol.m, [np.round(c, 3) for c in fr.symbol.coeffs], round(fr.weight, 3), fr.terms)

# two-regime windows
tr, he = case("transport"), case("heat")
def two(T, X):
    return np.where(X < np.pi, tr(T, X), he(T, X))
t = np.linspace(0, 2, 48)
for nw in [4, 8]:
    edges = np.linspace(0, 2 * np.pi, nw + 1)
    for a, b in zip(edges[:-1], edges[1:]):
        x = np.linspace(a, b, 64, endpoint=False)
        TT, XX = np.meshgrid(t, x, indexing="ij")
        u = two(TT, XX)
        for w in [None, "tukey"]:
            t0 = time.time()
            r = analyze_structured(u, t, x, noise=0.0, real=True, window=w)
            print(nw, round(a, 2), w, f"{time.time()-t0:.1f}s", r.label, r.n_modes, [(st, round(p, 3)) for st, _, p in r.structures[:2]], [str(fr.sympy)[:40] for fr in r.factors])
