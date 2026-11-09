"""High-kappa bias of the smoothness prior (a low-pass filter) on diffusion.

For heat (u_t = 0.3 u_xx) from scattered samples, per kernel family:
  (a) amplitude transfer per kappa: median over t of |FFT_x(mean)| / |FFT_x(u_true)| (bins with truth > 3 sigma_bin);
  (b) decay-rate bias per kappa: Re lam_hat(kappa) from the core's mode extraction on the posterior mean
      vs the exact -D kappa^2;
  (c) D_hat from core v2 on the posterior mean and on the samples (median, 90 % interval), vs 0.3.
Reference: the core on the exact grid plus white noise of the same sigma (no interpolation).
usage: highk_bias.py out.json [n] [noise]
"""
import json
import sys
import time

import numpy as np

from pdefactor.core.structfit import analyze_structured, extract_modes_ic
from pdefactor.interp import fit_gp, run_core_on_samples
from pdefactor.synthetic import case, grid, sample_scattered

out = sys.argv[1]
n = int(sys.argv[2]) if len(sys.argv) > 2 else 2000
nz = float(sys.argv[3]) if len(sys.argv) > 3 else 0.01
D_true = 0.3
f = case("heat")
tg, xg, u = grid(f)
t, x, y, s = sample_scattered(f, n, noise=nz, rng=1)
K = np.arange(1, 7)


def per_kappa(field, noise):
    nx = field.shape[1]
    Ut = np.fft.fft(u, axis=1) / nx
    Uf = np.fft.fft(field, axis=1) / nx
    modes, *_ = extract_modes_ic(field, tg, xg, noise=noise)
    rows = {}
    for k in K:
        good = np.abs(Ut[:, k]) > 3 * max(noise, 1e-12) / np.sqrt(nx)
        transfer = float(np.median(np.abs(Uf[good, k]) / np.abs(Ut[good, k]))) if good.any() else None
        sel = np.isclose(modes.kappa, k)
        lam = modes.lam[sel]
        rel = float(np.min(np.abs(lam.real / (-D_true * k**2) - 1))) if len(lam) else None
        rows[int(k)] = {"transfer": transfer, "decay_rel_err": rel, "n_good_t": int(good.sum())}
    return rows


def D_of(res):
    for fr in res.factors:
        c = fr.terms.get(2) if isinstance(fr.terms, dict) else None
        if c is not None:
            return float(complex(c).real)
    return None


rec = {"n": n, "noise": nz, "sigma": s, "families": {}}
# reference: exact grid + white noise, no interpolation
rng = np.random.default_rng(0)
ref = u + s * rng.standard_normal(u.shape)
rr = analyze_structured(ref, tg, xg, noise=s)
rec["reference_grid_noise"] = {"per_kappa": per_kappa(ref, s), "D_hat": D_of(rr), "label": rr.label}
for fams in [("matern32",), ("matern52",), ("rbf",), ("rbf", "rbfe", "rbfe+rbfe")]:
    t0 = time.time()
    p = fit_gp(t, x, y, grid=(tg, xg), S=16, families=fams)
    sig = p.effective_noise()
    mres = analyze_structured(p.mean, tg, xg, noise=sig)
    res = run_core_on_samples(p.samples, tg, xg, sig, p.weights)
    Ds = np.array([D_of(r) if D_of(r) is not None else np.nan for r, _ in res])
    key = "+".join(fams) if len(fams) == 1 else "evidence-mix"
    rec["families"][key] = {
        "family_posterior": p.info["family_posterior"], "coverage": p.coverage(u),
        "per_kappa": per_kappa(p.mean, sig), "D_hat_mean_field": D_of(mres),
        "D_hat_samples": [float(np.nanmedian(Ds)), float(np.nanpercentile(Ds, 5)), float(np.nanpercentile(Ds, 95))]
        if np.isfinite(Ds).any() else None,
        "frac_samples_with_D": float(np.isfinite(Ds).mean()), "labels": [r.label for r, _ in res],
        "time": time.time() - t0, "effective_noise": sig,
    }
    print(key, json.dumps(rec["families"][key]["per_kappa"]), rec["families"][key]["D_hat_samples"], flush=True)
json.dump(rec, open(out, "w"), indent=1)
