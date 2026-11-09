"""E2: gamma_N (P2-T3/P2-C2) vs time span T, x-window length L, and kappa-band, for the
two-factor cases. gamma_N^{-1/2} is the amplification of any component error (P2-T4).
Factors are the true symbols (this measures the geometry, not the fit)."""
import sys
from pathlib import Path

import numpy as np
import sympy as sp

sys.path.insert(0, str(Path(__file__).parent))
from pdefactor.core.components import gamma_N  # noqa: E402
from pdefactor.symbols import tau, xi  # noqa: E402
from pdefactor.synthetic import branch_roots  # noqa: E402


class Sym:
    def __init__(self, Q):
        self.Q = Q

    def roots(self, xi0):
        return branch_roots(self.Q, (xi0 / 1j).real)


D, c = 0.3, 1.0
PAIRS = {
    "transport_plus_diffusion": (tau + c * xi, tau - D * xi**2),
    "wave": (tau - c * xi, tau + c * xi),
    "beam": (tau - sp.I * D * xi**2, tau + sp.I * D * xi**2),
}


def g(name, T=2.0, L=2 * np.pi, kmax=6.0, kmin=1.0, nt=48, nx=64, Lper=2 * np.pi):
    """Kernels truncated to wavenumbers 2 pi m / Lper in [kmin, kmax], sampled on [0,T] x [0,L]."""
    ks = 2 * np.pi / Lper * np.arange(1, 64)
    ks = ks[(ks >= kmin - 1e-9) & (ks <= kmax + 1e-9)]
    t = np.linspace(0, T, nt)
    x = np.linspace(0, L, nx, endpoint=False)
    fac = [Sym(q) for q in PAIRS[name]]
    gam, cf, n0 = gamma_N(fac, ks, t, x)
    return gam


def run():
    out = []
    print("gamma_N vs T (L = 2pi, band 1..6)")
    for name in PAIRS:
        row = [g(name, T=T) for T in (0.1, 0.25, 0.5, 1, 2, 4, 8)]
        out.append((name, "T", row))
        print(f"  {name:26s}" + " ".join(f"{v:8.1e}" for v in row))
    print("gamma_N vs x-window L (T = 2, kappa on the 2pi lattice, L <= 2pi: sub-window)")
    for name in PAIRS:
        row = [g(name, L=L) for L in (0.5, 1, 2, 3, 2 * np.pi)]
        out.append((name, "L", row))
        print(f"  {name:26s}" + " ".join(f"{v:8.1e}" for v in row))
    print("gamma_N vs band [kmin, kmax] (T = 2, L = 2pi)")
    for name in PAIRS:
        row = [g(name, kmin=a, kmax=b) for a, b in ((1, 2), (1, 4), (1, 6), (3, 6), (5, 6))]
        out.append((name, "band", row))
        print(f"  {name:26s}" + " ".join(f"{v:8.1e}" for v in row))
    return out


if __name__ == "__main__":
    run()
