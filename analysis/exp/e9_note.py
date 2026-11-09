"""E9: plan verification on the note's own example 0.7 e^{-(x-t)^2} + 0.3 e^{-t} cos x, from n noisy
scattered samples (GP posterior -> outer loop -> split layer). The transport part is periodised over
x in [0, 2 pi) (sum of shifts by 2 pi k) so that it is an exact solution on the periodic grid.
Expected (0b.6): transport tau + xi recovered with weight ~ the 0.7 part's share; the e^{-t} cos x part
is one mode (|kappa| = 1), so the diffusion factor is ID-KER: any symbol through (lam=-1, kappa=+-1) fits.
Usage: e9_note.py [n] [noise] [seed]"""
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from benchmarks.bench import L_SPAN, T_SPAN  # noqa: E402
from pdefactor.interp.gp import fit_gp  # noqa: E402
from pdefactor.loop import run_loop  # noqa: E402


def transport(t, x):
    return 0.7 * sum(np.exp(-((x - t + 2 * np.pi * k) ** 2)) for k in (-2, -1, 0, 1, 2))


def diffusion(t, x):
    return 0.3 * np.exp(-t) * np.cos(x)


def main(n=400, noise=0.01, seed=0, S=16):
    t = np.linspace(0, T_SPAN, 64)
    x = np.linspace(0, L_SPAN, 128, endpoint=False)
    TT, XX = np.meshgrid(t, x, indexing="ij")
    u = transport(TT, XX) + diffusion(TT, XX)
    nu = [np.linalg.norm(transport(TT, XX)), np.linalg.norm(diffusion(TT, XX))]
    w_true = np.array(nu) / sum(nu)
    sig = noise * float(np.std(u))
    rng = np.random.default_rng(1000 + 7919 * seed + n)
    ts, xs = rng.uniform(0, T_SPAN, n), rng.uniform(0, L_SPAN, n)
    ys = transport(ts, xs) + diffusion(ts, xs) + sig * rng.standard_normal(n)
    t0 = time.time()
    g = fit_gp(ts, xs, ys, grid=(t, x), period_x=L_SPAN, S=S, seed=seed)
    Sm, w = g.samples[:8], g.weights[:8]
    nd = np.sqrt(2) * (g.samples - g.mean[None])
    r = run_loop(list(Sm), t, x, 0.0, w / w.sum(), noise_draws=nd)
    print(f"=== note example n={n} noise={noise} seed={seed}  ({time.time() - t0:.0f}s)")
    print(r.summary())
    print("equation:", r.equation())
    for f in r.factors:
        print("  factor", f.sympy, "kappa support", f.kappa_support, "|", f.status)
    print("true weights (transport, diffusion):", np.round(w_true, 4))
    if r.split:
        print("split weights:", np.round(r.split["w_mean"], 4), "90%:", np.round(r.split["w_q"], 4).tolist())
    return r


if __name__ == "__main__":
    a = sys.argv[1:]
    main(int(a[0]) if a else 400, float(a[1]) if len(a) > 1 else 0.01, int(a[2]) if len(a) > 2 else 0)
