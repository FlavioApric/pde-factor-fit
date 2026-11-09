"""E7: per-bin correlated noise (GLS) in the core on GP posterior samples (plan v2.9, S-INTERP sec. 4).
Usage: e7_gls.py case n noise seed. Compares, per GP sample, the core with the old scalar
effective noise ("smooth") and with noise_draws = sqrt(2) (samples - mean) (GLS)."""
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "code" / "experiments"))
from gp_cache import fit_and_cache  # noqa: E402

from benchmarks import metrics as M  # noqa: E402
from pdefactor.core.structfit import analyze_structured  # noqa: E402
from pdefactor.synthetic import CASES, case, extra_case  # noqa: E402


def smooth_noise(samples, w, r=4, factor=np.sqrt(2)):
    # GPPosterior.effective_noise(kind="smooth"), restated on cached arrays
    from numpy.polynomial import legendre

    d = samples - np.tensordot(w, samples, 1)[None]
    nt, nx = d.shape[-2:]
    B = np.fft.fft(d, axis=-1) / nx
    Q, _ = np.linalg.qr(legendre.legvander(np.linspace(-1, 1, nt), r - 1))
    P = np.einsum("ta,stk->sak", Q, B)
    b2 = (np.sum(w[:, None, None] * (np.abs(P) ** 2).sum(1), axis=0) / r).max()
    return float(factor * np.sqrt(b2) * np.sqrt(nx))


def main(name, n, noise, seed, S_use=8):
    d = fit_and_cache(name, n, noise, seed)
    f = case(name) if name in CASES else extra_case(name)
    S, w, t, x = d["samples"], d["weights"], d["t"], d["x"]
    real = bool(np.isrealobj(S))
    mean = np.tensordot(w, S, 1)
    draws = np.sqrt(2) * (S - mean[None])
    s_old = smooth_noise(S, w)
    for mode in ("smooth", "gls"):
        ok, t0 = [], time.time()
        for i in range(min(S_use, len(S))):
            kw = dict(noise=s_old) if mode == "smooth" else dict(noise=0.0, noise_draws=draws)
            r = analyze_structured(S[i], t, x, real=real, **kw)
            sc = M.score(name, f, t, x, [fr.sympy for fr in r.factors], [fr.weight for fr in r.factors])
            ok.append(bool(sc["factor_set"]) and r.label == "FIT-COMPATIBLE")
            print(f"  {mode} s{i}: {r.label} {[str(fr.sympy) for fr in r.factors][:4]} coef_err={sc['coef_err']:.2g}",
                  flush=True)
        print(f"{name} {n} {noise} {mode}: right set {np.mean(ok):.2f}  ({time.time() - t0:.0f}s)", flush=True)


if __name__ == "__main__":
    a = sys.argv[1:]
    main(a[0], int(a[1]), float(a[2]), int(a[3]))
