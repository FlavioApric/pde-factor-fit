"""CRB std of (lam, kappa) at the TRUE modes of the E3 cases on [0, L] x [0, 2], noise 1e-3 (REPORT table F).
Modes: kappa = +-1..K, lam = roots of each true factor at xi = i kappa; amplitudes by LS on the exact field."""
import numpy as np

from pdefactor.domain.extract import fisher_sigmas
from pdefactor.synthetic import case

ROOTS = {"transport_plus_diffusion": lambda k: [-1j * k, -0.3 * k**2], "wave": lambda k: [-1j * k, 1j * k]}
for name, roots in ROOTS.items():
    f = case(name)
    for L in (2 * np.pi, np.pi, np.pi / 2):
        nx = int(round(128 * L / (2 * np.pi)))
        t = np.linspace(0, 2.0, 64)
        x = np.linspace(0, L, nx, endpoint=False)
        TT, XX = np.meshgrid(t, x, indexing="ij")
        u = f(TT, XX)
        kap = np.r_[-np.arange(1, 7), np.arange(1, 7)].astype(float)
        lam, kk = [], []
        for k in kap:
            for r in roots(k):
                lam.append(r)
                kk.append(k)
        lam, kk = np.array(lam), np.array(kk)
        B = np.exp(np.outer(TT.ravel(), lam) + 1j * np.outer(XX.ravel(), kk))
        a, *_ = np.linalg.lstsq(B, u.ravel().astype(complex), rcond=None)
        res = np.linalg.norm(B @ a - u.ravel()) / np.linalg.norm(u)
        keep = np.abs(a) > 1e-6 * np.abs(a).max()
        sl, sk, _ = fisher_sigmas(lam[keep], kk[keep], a[keep], t, x, 1e-3 * np.std(u))
        print(f"{name:26s} L={L:4.2f} modes={keep.sum():2d} fitres={res:.1e}  sigma_lam med/max {np.median(sl):.2g}/{sl.max():.2g}"
              f"  sigma_kap med/max {np.median(sk):.2g}/{sk.max():.2g}")
