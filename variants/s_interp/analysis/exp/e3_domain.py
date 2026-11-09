"""E3: domain study. (a) one law, sub-windows of the domain (non-periodic cell, 2-D pencil);
(b) two regimes side by side: big domain vs the two halves (cells)."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from e1_noise import match_err, truth  # noqa: E402
from pencil2d import extract_modes_2d  # noqa: E402
from structfit import select  # noqa: E402

from pdefactor.synthetic import case  # noqa: E402


def analyse(u, t, x, sig):
    m = extract_modes_2d(u, t, x, noise=sig)
    if len(m) < 4:
        return None, None, len(m)
    bn = sig / np.sqrt(len(x)) if sig > 0 else 1e-9 * np.abs(m.amp).max()
    best, ranked, _ = select(m, t, bn)
    return best, ranked, len(m)


def subwindows(names=("transport_plus_diffusion", "wave", "heat"), noises=(0.0, 1e-3, 1e-2),
               Ls=(2 * np.pi, np.pi, np.pi / 2), T=2.0):
    print("(a) sub-window [0, L] of the 2pi-periodic field; 2-D pencil; ok/err/top-weight/#modes")
    for name in names:
        f = case(name)
        tr = truth(name, f)
        for nz in noises:
            line = f"  {name:26s} {nz:7.0e}"
            for L in Ls:
                nx = int(round(128 * L / (2 * np.pi)))
                t = np.linspace(0, T, 64)
                x = np.linspace(0, L, nx, endpoint=False)
                TT, XX = np.meshgrid(t, x, indexing="ij")
                u = f(TT, XX)
                rng = np.random.default_rng(1)
                sig = nz * np.std(u)
                best, ranked, nm = analyse(u + sig * rng.standard_normal(u.shape), t, x, sig)
                if best is None:
                    line += f"   L={L:4.2f}: no modes ({nm})"
                    continue
                e = match_err(tr, [Q.to_sympy(tol=1e-3 if nz else 1e-8) for Q in best.factors])
                line += f"   L={L:4.2f}: {int(e < .05)}/{e:6.0e}/{ranked[0][2]:.2f}/{nm}"
            print(line, flush=True)


def two_regimes(nz=1e-3, T=2.0):
    """Left half: transport modes; right half: heat modes (glued with a smooth partition;
    the glue zone is not a solution of either law: it is what a real interface looks like)."""
    print("(b) two regimes: transport on x<pi, heat on x>pi")
    ft, fh = case("transport"), case("heat")
    t = np.linspace(0, T, 64)
    x = np.linspace(0, 2 * np.pi, 128, endpoint=False)
    TT, XX = np.meshgrid(t, x, indexing="ij")
    chi = 0.5 * (1 + np.tanh((XX - np.pi) / 0.15))
    u = (1 - chi) * ft(TT, XX) + chi * fh(TT, XX)
    sig = nz * np.std(u)
    u = u + sig * np.random.default_rng(2).standard_normal(u.shape)
    for lab, sl in (("whole [0,2pi]", slice(0, 128)), ("left [0,pi-.5]", slice(0, 54)),
                    ("right [pi+.5,2pi]", slice(74, 128))):
        best, ranked, nm = analyse(u[:, sl], t, x[sl], sig)
        if best is None:
            print(f"  {lab:20s} no modes")
            continue
        facs = [str(Q.to_sympy(tol=1e-2)) for Q in best.factors]
        print(f"  {lab:20s} #modes={nm:3d} best={best.structure} p={ranked[0][2]:.2f} factors={facs}")


if __name__ == "__main__":
    subwindows()
    two_regimes()
