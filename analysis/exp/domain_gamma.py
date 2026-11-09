"""gamma_N of the true factors on the E3 cells (L x T), kappa on the Rayleigh grid 2 pi m / L, |kappa| <= 7
(as quadtree.fit_cell), next to recovery (REPORT table G)."""
import numpy as np

from pdefactor.core.components import gamma_N
from pdefactor.core.variety import PolySymbol

TRUE = {"transport_plus_diffusion": [[0, 1], [0, 0, -0.3]], "wave": [[0, 1], [0, -1]]}
for name, cs in TRUE.items():
    facs = [PolySymbol(1, [np.array(c, complex)]) for c in cs]
    for T in (2.0, 1.0):
        line = f"{name:26s} T={T}"
        for L in (2 * np.pi, np.pi, np.pi / 2, np.pi / 4):
            nx = int(round(128 * L / (2 * np.pi)))
            t = np.linspace(0, T, int(64 * T / 2))
            x = np.linspace(0, L, nx, endpoint=False)
            dk = 2 * np.pi / L
            m = int(7 // dk)
            kap = dk * np.r_[-np.arange(1, m + 1), np.arange(1, m + 1)] if m else np.array([-dk, dk])
            line += f"  L={L:4.2f}: {gamma_N(facs, kap, t, x)[0]:.3g}"
        print(line)
