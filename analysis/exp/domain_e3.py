"""E3 on non-periodic cells with the S-DOMAIN extractors (adapted from e3_domain.py).

(a) sub-windows [0, L] of the 2pi-periodic field, extractors fft_tukey / esprit / cadzow / pencil2d (baseline);
(b) two regimes (transport | heat glued at x = pi): halves and quadtree.
Usage: python domain_e3.py [sub|two|quad] [extractor ...]
"""
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from e1_noise import match_err, truth  # noqa: E402
from pencil2d import extract_modes_2d  # noqa: E402

from pdefactor.core.structfit import select  # noqa: E402
from pdefactor.domain.extract import EXTRACTORS  # noqa: E402
from pdefactor.domain.fit import analyze_cell, select_cell  # noqa: E402
from pdefactor.synthetic import case  # noqa: E402

OUT = Path(__file__).parent / "out"
OUT.mkdir(exist_ok=True)


def analyse(u, t, x, sig, method):
    """method: pencil2d (E3 baseline) | fft_tukey | esprit_x | esprit2d | greedy | cadzow | cadzow_x
    (point-level: extractor points + structured fit with the extractor's sigma) | kernel (data-level fit
    seeded by esprit_x) | kernel0 (data-level, pursuit seeds only)."""
    if method in ("kernel", "kernel0"):
        r = analyze_cell(u, t, x, sig, extractor="esprit_x" if method == "kernel" else None)
        return r["best"], r["ranked"], len(r["ext"].modes) if r["ext"] is not None else 0
    if method == "pencil2d":
        m = extract_modes_2d(u, t, x, noise=sig)
        if len(m) < 4:
            return None, None, len(m)
        bn = sig / np.sqrt(len(x)) if sig > 0 else 1e-9 * np.abs(m.amp).max()
        best, ranked, _ = select(m, t, bn)
        return best, ranked, len(m)
    ext = EXTRACTORS[method](u, t, x, noise=sig)
    if len(ext.modes) < 4:
        return None, None, len(ext.modes)
    best, ranked, _ = select_cell(ext)
    return best, ranked, len(ext.modes)


def two_field(nz=1e-3, T=2.0, seed=2, x_if=np.pi):
    ft, fh = case("transport"), case("heat")
    t = np.linspace(0, T, 64)
    x = np.linspace(0, 2 * np.pi, 128, endpoint=False)
    TT, XX = np.meshgrid(t, x, indexing="ij")
    chi = 0.5 * (1 + np.tanh((XX - x_if) / 0.15))
    u = (1 - chi) * ft(TT, XX) + chi * fh(TT, XX)
    sig = nz * np.std(u)
    return t, x, u + sig * np.random.default_rng(seed).standard_normal(u.shape), sig


TRUE_ST = {"transport_plus_diffusion": ((1, 1), (1, 2)), "wave": ((1, 1), (1, 1)), "heat": ((1, 2),)}


def subwindows(methods, names=("transport_plus_diffusion", "wave", "heat"), noises=(0.0, 1e-3, 1e-2),
               Ls=(2 * np.pi, np.pi, np.pi / 2), T=2.0, seeds=(1,)):
    print("(a) sub-window [0, L]; ok(struct&coef<.05)/coef err/top p/#modes")
    rows = []
    for method in methods:
        for name in names:
            f = case(name)
            tr = truth(name, f)
            for nz in noises:
                line = f"  {method:9s} {name:26s} {nz:7.0e}"
                for L in Ls:
                    nx = int(round(128 * L / (2 * np.pi)))
                    t = np.linspace(0, T, 64)
                    x = np.linspace(0, L, nx, endpoint=False)
                    TT, XX = np.meshgrid(t, x, indexing="ij")
                    u = f(TT, XX)
                    for s in seeds:
                        rng = np.random.default_rng(s)
                        sig = nz * np.std(u)
                        t0 = time.time()
                        best, ranked, nm = analyse(u + sig * rng.standard_normal(u.shape), t, x, sig, method)
                        dt = time.time() - t0
                        if best is None:
                            rows.append((method, name, nz, L, s, 0, 0, np.inf, 0.0, nm, dt))
                            line += f"   L={L:4.2f}: none({nm})"
                            continue
                        e = match_err(tr, [Q.to_sympy(tol=1e-3 if nz else 1e-8) for Q in best.factors])
                        st_ok = int(tuple(sorted(best.structure)) == TRUE_ST[name])
                        ok = int(st_ok and e < .05)
                        rows.append((method, name, nz, L, s, st_ok, ok, e, ranked[0][2], nm, dt))
                        line += f"   L={L:4.2f}: {st_ok}{ok}/{e:6.0e}/{ranked[0][2]:.2f}/{nm}"
                print(line, flush=True)
    return rows


def halves(methods, nz=1e-3):
    t, x, u, sig = two_field(nz)
    print("(b) two regimes: transport on x<pi, heat on x>pi")
    for method in methods:
        for lab, sl in (("whole", slice(0, 128)), ("left [0,pi-.5]", slice(0, 54)), ("right [pi+.5,2pi]", slice(74, 128)),
                        ("left [0,pi]", slice(0, 64)), ("right [pi,2pi]", slice(64, 128))):
            best, ranked, nm = analyse(u[:, sl], t, x[sl], sig, method)
            if best is None:
                print(f"  {method:9s} {lab:20s} no modes ({nm})")
                continue
            facs = [str(Q.to_sympy(tol=1e-2)) for Q in best.factors]
            print(f"  {method:9s} {lab:20s} #modes={nm:3d} best={best.structure} p={ranked[0][2]:.2f} factors={facs}", flush=True)


def quad(nz=1e-3, x_if=np.pi, extractor=None, gamma_floor=None, max_depth=2):
    from pdefactor.domain.quadtree import GAMMA_FLOOR, quadtree

    t, x, u, sig = two_field(nz, x_if=x_if)
    t0 = time.time()
    root, leaves, _ = quadtree(u, t, x, sig, gamma_floor=GAMMA_FLOOR if gamma_floor is None else gamma_floor,
                               max_depth=max_depth, verbose=True, extractor=extractor,
                               fracs_x=(0.375, 0.5, 0.625), fracs_t=(0.5,), n_refine=2)
    print(f"quadtree two-regime (interface x={x_if:.3f}, noise {nz:g}) {time.time() - t0:.0f}s; split={root.split}")
    for lf in sorted(leaves, key=lambda c: (c.ix[0], c.it[0])):
        b = lf.bounds(t, x)
        print(f"  leaf t[{b[0]:.2f},{b[1]:.2f}] x[{b[2]:.2f},{b[3]:.2f}] {lf.structure} p={lf.ranked[0][2]:.2f} "
              f"law={lf.law()} gamma={lf.gamma:.3g} nk={lf.n_kappa}")
    return root, leaves


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "sub"
    methods = sys.argv[2:] or ["esprit"]
    if what == "sub":
        import os
        nz = tuple(float(v) for v in os.environ.get("DOMAIN_NOISES", "0,1e-3,1e-2").split(","))
        rows = subwindows(methods, noises=nz)
        import csv
        with open(OUT / f"domain_e3_{'_'.join(methods)}.csv", "w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["method", "case", "noise", "L", "seed", "struct_ok", "ok", "coef_err", "p_top", "n_modes", "sec"])
            w.writerows(rows)
    elif what == "two":
        halves(methods)
    elif what == "quad":
        xi = float(sys.argv[2]) if len(sys.argv) > 2 else np.pi
        quad(x_if=xi)
