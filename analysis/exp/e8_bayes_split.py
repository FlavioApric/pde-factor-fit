"""E8: bayes_split (src) coverage of the 90 % weight interval and P(split), with the true factors
(as E5) and with the core's factors; plus the null test (single-factor data + a spurious factor).
Usage: e8_bayes_split.py [seeds]"""
import sys
from pathlib import Path

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from pdefactor.bayes_split import bayes_split  # noqa: E402
from pdefactor.core.variety import PolySymbol  # noqa: E402
from pdefactor.synthetic import case, grid  # noqa: E402


def sym(q):
    from pdefactor.symbols import tau, xi

    p = sp.Poly(sp.expand(q), tau)
    m = p.degree()
    coeffs = []
    lead = complex(p.coeff_monomial(tau**m).subs(xi, 0))
    for kk in range(m):
        c = sp.Poly(sp.expand(p.coeff_monomial(tau**kk)), xi)
        dx = c.degree() if not c.is_zero else 0
        coeffs.append(np.array([complex(c.coeff_monomial(xi**b)) / lead for b in range(dx + 1)]))
    return PolySymbol(m, coeffs)


SNR = float(sys.argv[2]) if len(sys.argv) > 2 else 3.0


def run(name, Ts=(0.25, 0.5, 1.0, 2.0), noise=1e-2, seeds=10):
    print(f"{name}, noise {noise:.0e}: T  c_F  coverage90(w)  width  P(split)", flush=True)
    for T in Ts:
        cov, wid, ps, cfs = [], [], [], []
        for sd in range(seeds):
            f = case(name, seed=sd)
            t, x, u0 = grid(f, T=T, nt=48, nx=64)
            TT, XX = np.meshgrid(t, x, indexing="ij")
            wt = f.weights(TT, XX)
            facs = [sym(c.Q) for c in f.components]
            sig = noise * np.std(np.abs(u0))
            rng = np.random.default_rng(1000 + sd)
            u = u0 + sig * rng.standard_normal(u0.shape)
            r = bayes_split(u, t, x, facs, noise=sig, seed=sd, snr_min=SNR)
            lo, hi = r.weights_q[:, 0], r.weights_q[:, 2]
            cov.append(np.all((lo <= wt) & (wt <= hi)))
            wid.append(np.mean(hi - lo))
            ps.append(r.p_split)
            cfs.append(r.cF)
        print(f"  T={T:5.2f} c_F={np.mean(cfs):.3f} cov={np.mean(cov):.2f} width={np.mean(wid):.4f} "
              f"P(split)={np.mean(ps):.3f}", flush=True)


def null(seeds=10, noise=1e-2):
    from pdefactor.symbols import tau, xi

    ps = []
    for sd in range(seeds):
        f = case("heat", seed=sd)
        t, x, u0 = grid(f, nt=48, nx=64)
        sig = noise * np.std(u0)
        u = u0 + sig * np.random.default_rng(sd).standard_normal(u0.shape)
        r = bayes_split(u, t, x, [sym(tau - sp.Float(0.3) * xi**2), sym(tau + xi)], noise=sig)
        ps.append(r.p_split)
    print(f"null (heat + spurious transport): P(split) mean {np.mean(ps):.3f}, max {np.max(ps):.3f}")


if __name__ == "__main__":
    S = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    for nm in ("transport_plus_diffusion", "wave"):
        run(nm, seeds=S)
    null(S)
