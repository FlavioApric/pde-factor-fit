import sys, os, numpy as np
from pdefactor.synthetic import case, grid, sample_scattered
from pdefactor.interp import fit_gp
from pdefactor.core.structfit import extract_modes_ic, analyze_structured
cache = sys.argv[1]
f = case("transport_plus_diffusion"); tg, xg, u = grid(f)
if not os.path.exists(cache):
    t, x, y, s = sample_scattered(f, 2000, noise=0.01, rng=1)
    p = fit_gp(t, x, y, grid=(tg, xg), S=8, families=("rbf",))
    np.savez(cache, mean=p.mean, samples=p.samples, var=p.var, s=s, eff=p.effective_noise())
d = np.load(cache); s = float(d["s"]); eff = float(d["eff"])
rng = np.random.default_rng(0)
fields = {"truth": (u, 0.0), "truth+white": (u + s*rng.standard_normal(u.shape), s), "gp_mean": (d["mean"], eff), "gp_sample0": (d["samples"][0], eff)}
for k_, (fld, nz) in fields.items():
    m, bn, *_ = extract_modes_ic(fld, tg, xg, noise=nz)
    print(f"== {k_} noise={nz:.2e} bin_noise={bn:.2e} nmodes={len(m)}")
    for k in [1, 2, 3, 4, 5, 6]:
        sel = np.isclose(m.kappa, k)
        print("  k", k, " ".join(f"{l.real:+.3f}{l.imag:+.3f}i(snr{sn:.0f})" for l, sn in zip(m.lam[sel], m.snr[sel])))
    r = analyze_structured(fld, tg, xg, noise=nz); print("  ->", r.label, [str(q.sympy) for q in r.factors])
# error spectrum of the GP sample: per kappa rms over t of |FFT(err)|
E = np.fft.fft(d["samples"][0] - u, axis=1) / u.shape[1]; T = np.abs(np.fft.fft(u, axis=1) / u.shape[1])
print("err rms per k 0..8:", np.round(np.sqrt((np.abs(E[:, :9])**2).mean(0)), 5))
print("truth max per k 0..8:", np.round(T[:, :9].max(0), 4))
