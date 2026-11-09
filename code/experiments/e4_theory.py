"""E4: theory checks on the core and on structfit.
(a) kappa = 0 shared mode (delta(P) > 0 path, C12-T2): transport+diffusion plus a constant,
    which lies in ker(tau + xi) and ker(tau - D xi^2) (both vanish at (0, 0)).
(b) repeated factor (tau + xi)^2: modes (A + B t) e^{i kappa (x - t)} (OPF5B-T6: repeated
    roots must give UNDECIDED, not a confident simple factor).
(c) discriminant-square test (C12-P2) for m = 2 on fitted quadratics: wave (square) vs KG (not)."""
import sys
from pathlib import Path

import numpy as np
import sympy as sp

sys.path.insert(0, str(Path(__file__).parent))
from structfit import select  # noqa: E402

from pdefactor.core import analyze  # noqa: E402
from pdefactor.core.spectral import extract_modes  # noqa: E402
from pdefactor.core.variety import fit_monic  # noqa: E402
from pdefactor.symbols import tau, xi  # noqa: E402
from pdefactor.synthetic import case, grid  # noqa: E402


def run_both(label, u, t, x, nz):
    sig = nz * np.std(u)
    rng = np.random.default_rng(3)
    v = u + sig * rng.standard_normal(u.shape)
    r = analyze(v, t, x, noise=sig)
    m = extract_modes(v, t, x, noise=sig)
    bn = sig / np.sqrt(len(x)) if sig > 0 else 1e-9 * np.abs(m.amp).max()
    best, ranked, _ = select(m, t, bn)
    print(f"  {label:34s} noise={nz:6.0e} core: {r.label:15s} shared={r.n_shared} "
          f"factors={[str(f.sympy) for f in r.factors]}")
    print(f"  {'':34s}              structfit: {best.structure} p={ranked[0][2]:.2f} "
          f"factors={[str(Q.to_sympy(tol=1e-3)) for Q in best.factors]}")


def kappa0():
    print("(a) kappa = 0 shared mode")
    f = case("transport_plus_diffusion")
    t, x, u = grid(f)
    for nz in (0.0, 1e-3):
        run_both("tpd + 0.2 (constant)", u + 0.2, t, x, nz)


def repeated():
    print("(b) repeated factor (tau + xi)^2")
    t = np.linspace(0, 2, 64)
    x = np.linspace(0, 2 * np.pi, 128, endpoint=False)
    TT, XX = np.meshgrid(t, x, indexing="ij")
    u = sum(np.exp(-(k / 1.5) ** 2 / 2) * (1 + 0.5 * TT) * np.cos(k * (XX - TT) + k) for k in range(1, 7))
    for nz in (0.0, 1e-3):
        run_both("(A + B t) cos(k(x - t))", u, t, x, nz)


def disc_square():
    """For a fitted monic quadratic tau^2 + b(xi) tau + c(xi): is b^2 - 4c a square in C[xi]?
    Numerical test: sqrt of the discriminant polynomial by fitting a polynomial r with r^2 = disc,
    relative residual small <=> reducible (C12-P2)."""
    print("(c) discriminant-square test on fitted quadratics")
    for name in ("wave", "klein_gordon", "telegraph"):
        f = case(name)
        t, x, u = grid(f)
        for nz in (0.0, 1e-3, 1e-2):
            sig = nz * np.std(u)
            v = u + sig * np.random.default_rng(4).standard_normal(u.shape)
            m = extract_modes(v, t, x, noise=sig)
            P, _, _ = fit_monic(m.lam, m.kappa, 2, 2, None, False)
            Ps = sp.Poly(sp.expand(P.to_sympy(tol=1e-12)), tau)
            b, c = (Ps.all_coeffs() + [0, 0])[1:3]
            disc = sp.Poly(sp.expand(b**2 - 4 * c), xi)
            # square <=> roots of disc pair up (even multiplicity). Drop coefficients below 1e-3 of
            # the largest (noise), then pair roots greedily; score = max pair gap / root scale.
            cs = np.array([complex(c_) for c_ in disc.all_coeffs()])
            cs = cs[np.argmax(np.abs(cs) > 1e-3 * np.abs(cs).max()):]
            rts = list(np.roots(cs)) if len(cs) > 1 else []
            if len(rts) % 2:
                res = np.inf
            else:
                gaps = []
                while rts:
                    r0 = rts.pop(0)
                    j = int(np.argmin([abs(r0 - r1) for r1 in rts]))
                    gaps.append(abs(r0 - rts.pop(j)))
                scale = max(1.0, max(abs(np.roots(cs))))
                res = max(gaps) / scale if gaps else 0.0
            print(f"  {name:14s} noise={nz:6.0e} disc={sp.N(disc.as_expr(), 4)}  root-pair gap={res:.1e}")


if __name__ == "__main__":
    kappa0()
    repeated()
    disc_square()
