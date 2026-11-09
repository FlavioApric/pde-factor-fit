"""Extract the data behind the paper's figures from the worked-example runs into small files.

Needs the `pdefactor` package (run from the repository root):
    python ../code/experiments/extract_data.py --runs <dir with run folders> --out ../benchmarks/data

Run folders used (produced by worked_example.py and benchmarks/final_report.py):
    tpd_grid5_bench   transport + diffusion, grid, 5 % noise, benchmark protocol (one grid + bootstrap)
    tpd_5pct_S32      transport + diffusion, grid, 5 % noise, 32 posterior samples (cloud of factors)
    beam_grid5, klein_gordon_grid5, telegraph_grid5, advdiff_grid5   appendix cases (reports only)
"""
from __future__ import annotations

import argparse
import json
import pickle
import shutil
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path.cwd() / "code"))
sys.path.insert(0, str(Path.cwd() / "benchmarks"))


def cplx(z):
    z = np.asarray(z)
    return {"re": np.real(z).tolist(), "im": np.imag(z).tolist()}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    runs, out = Path(a.runs), Path(a.out)
    out.mkdir(parents=True, exist_ok=True)

    from final_report import components, symbol_of
    from pdefactor.core import spectral as SP
    from pdefactor.core.components import kernel_basis
    from pdefactor.synthetic import any_case, grid

    # ---- reports (copied verbatim, they are the provenance of every number quoted in the text)
    for name in ["tpd_grid5_bench", "tpd_5pct_S32", "beam_grid5", "klein_gordon_grid5", "telegraph_grid5",
                 "advdiff_grid5", "advdiff_S16"]:
        d = runs / name
        if (d / "report.json").exists():
            shutil.copy(d / "report.json", out / f"{name}_report.json")
            shutil.copy(d / "report.md", out / f"{name}_report.md")
        if (d / "pruned.json").exists():
            shutil.copy(d / "pruned.json", out / f"{name}_pruned.json")

    # ---- worked example: input, modes, components, band
    d = runs / "tpd_grid5_bench"
    inp = np.load(d / "input.npz")
    U, t, x, sig = inp["U"], inp["t"], inp["x"], float(inp["sigma"])
    res = pickle.loads((d / "res.pkl").read_bytes())
    truth_field = any_case("transport_plus_diffusion", seed=0)
    _, _, u_true = grid(truth_field)
    modes = SP.extract_modes(U, t, x, noise=sig)
    Qs = [symbol_of(f.coef) for f in res.factors]
    lam, kap = np.asarray(modes.lam), np.asarray(modes.kappa)
    dist = np.stack([np.abs(Q.eval(lam, 1j * kap)) / np.maximum(np.abs(Q.deriv_tau(lam, 1j * kap)), 1e-12)
                     for Q in Qs]) if hasattr(Qs[0], "deriv_tau") else None
    if dist is None:  # distance to the nearest root of each factor at the mode's wavenumber
        dist = np.stack([[min(abs(lm - r) for r in Q.roots(1j * k)) for lm, k in zip(lam, kap)] for Q in Qs])
    group = np.argmin(dist, axis=0)
    kappas = np.array(sorted({s * abs(float(k)) for f in res.factors for k in (f.kappa_support or []) for s in (1, -1)}))
    comps = components(Qs, kappas, t, x, U)
    # FFT amplitudes for the band figure
    kk, Uh = SP.fft_x(U, x)
    kk_t, Uh_t = SP.fft_x(u_true, x)
    np.savez_compressed(out / "worked_fields.npz", U=U, u_true=u_true, t=t, x=x, sigma=sig,
                        kappa_fft=kk, Uhat=Uh, Uhat_true=Uh_t,
                        components=np.stack([np.asarray(f) for f in comps["fields"]]),
                        joint_rel_residual=float(comps["joint_rel_residual"]))
    (out / "worked_modes.json").write_text(json.dumps({
        "kappa": kap.tolist(), "lam": cplx(lam), "snr": np.asarray(modes.snr).tolist(), "group": group.tolist(),
        "factors": [str(f.sympy) for f in res.factors], "dropped": [str(f.sympy) for f in res.dropped],
        "kappa_support": [list(map(float, f.kappa_support or [])) for f in res.factors],
        "nx": int(U.shape[1]), "dt": float(t[1] - t[0]), "dx": float(x[1] - x[0]),
        "evidence": sorted(([str(k), float(v)] for k, v in res.evidence.items()), key=lambda r: -r[1])[:8],
        "component_keys": [k for k, v in comps.items()],
    }, indent=1))

    # ---- cloud of factors over 32 posterior samples
    r32 = pickle.loads((runs / "tpd_5pct_S32" / "res.pkl").read_bytes())
    c = r32.agg.cloud
    (out / "cloud_S32.json").write_text(json.dumps({
        "theta": np.asarray(c.theta).tolist(), "w": np.asarray(c.w).tolist(), "pi": np.asarray(c.pi).tolist(),
        "sample": np.asarray(c.sample).tolist(), "m": np.asarray(c.m).tolist(), "track": np.asarray(c.track).tolist(),
        "pad": list(map(int, np.asarray(c.pad).ravel()[:2])) if np.ndim(c.pad) else None,
        "terms": [{str(k): [complex(v).real, complex(v).imag] for k, v in tm.items()} for tm in c.terms],
        "sympy": [str(s) for s in c.sympy],
        "track_sympy": [str(s) for s in r32.agg.track_sympy], "W_track": list(map(float, r32.agg.W_track)),
    }, indent=1))
    # principal angles between all cloud factors (largest angle between sampled kernels)
    from scipy.linalg import subspace_angles
    ks = np.arange(1, 5, dtype=float)
    ks = np.concatenate([-ks[::-1], ks])
    bases = []
    for tm, mm in zip(c.terms, c.m):
        from pdefactor.core.variety import PolySymbol
        dx = max(int(k) for k in tm) if tm else 0
        C = np.zeros((1, dx + 1), complex)
        for k, v in tm.items():
            C[0, int(k)] = -complex(v)  # terms are -coefficients of xi^k in tau = sum c_k xi^k
        Q = PolySymbol(1, [C[0]])
        bases.append(kernel_basis(Q, ks, t, x))
    n = len(bases)
    ang = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            ang[i, j] = ang[j, i] = float(np.max(subspace_angles(bases[i], bases[j])))
    np.save(out / "cloud_S32_angles.npy", ang)
    print("wrote", sorted(p.name for p in out.iterdir()))


if __name__ == "__main__":
    main()
