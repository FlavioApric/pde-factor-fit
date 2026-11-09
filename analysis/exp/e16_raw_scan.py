"""E16 (S-PHASE4-ML): is the top-ranked candidate (a raw-data mode scan, L1a(i)) worth it?

Heat u_t = 0.3 u_xx at 400 scattered points, 5 % noise (the open failure cell of PHASE4 §1). Per
spatial wavenumber kappa, the decay lam(kappa) is estimated two ways:
- GP path (today): fit_gp posterior on the grid, then core.extract_modes_ic with the GP noise
  draws (GLS), the per-bin modes at |kappa|;
- raw scan (candidate): joint variable projection directly on the scattered observations with the
  basis exp(lam_k t) {cos k x, sin k x}, k = 1..K, plus a constant; lam_k started from a 1-D
  matched-filter scan per k on the residual (a generalised Lomb-Scargle for damped modes).
Truth: lam = -0.3 k^2. Reported: |dlam| per kappa for both and the raw-data CRB of lam_k, which
says whether the information is there at all (PHASE4 P0: absent vs lost by the GP).

This is a measurement for LAYER_CANDIDATES.md; the layer itself is deterministic and belongs to
the local session (L1a(i)). No pipeline code changes here.

Usage:  python analysis/exp/e16_raw_scan.py [--seeds 3]
"""
from __future__ import annotations

import argparse
import os

import numpy as np
from scipy.optimize import least_squares

from pdefactor.synthetic import case, sample_scattered

D, K, L = 0.3, 6, 2 * np.pi
HERE = os.path.dirname(os.path.abspath(__file__))


def design(lams, t, x):
    cols = [np.ones_like(t)]
    for k, lm in enumerate(lams, start=1):
        e = np.exp(lm * t)
        cols += [e * np.cos(k * x), e * np.sin(k * x)]
    return np.stack(cols, 1)


def raw_scan(t, x, y):
    lams = np.zeros(K)
    r = y - y.mean()
    grid = -np.linspace(0, 15, 301)
    for k in range(1, K + 1):  # matched filter per k on the residual of the lower k
        best = None
        for lm in grid:
            B = np.stack([np.exp(lm * t) * np.cos(k * x), np.exp(lm * t) * np.sin(k * x)], 1)
            c, *_ = np.linalg.lstsq(B, r, rcond=None)
            gain = np.sum((B @ c) ** 2)
            if best is None or gain > best[0]:
                best = (gain, lm, B @ c)
        lams[k - 1] = best[1]
        r = r - best[2]

    def res(v):
        A = design(v, t, x)
        c, *_ = np.linalg.lstsq(A, y, rcond=None)
        return y - A @ c

    sol = least_squares(res, lams, bounds=(-30, 5))
    lam = sol.x
    A = design(lam, t, x)
    c, *_ = np.linalg.lstsq(A, y, rcond=None)
    sig = np.std(y - A @ c)
    # CRB of lam_k (amplitudes profiled): Fisher from the Jacobian of the full model
    J = []
    for k in range(1, K + 1):
        e = np.exp(lam[k - 1] * t)
        J.append(t * e * (c[2 * k - 1] * np.cos(k * x) + c[2 * k] * np.sin(k * x)))
    Jf = np.column_stack([A] + J)
    try:
        C = np.linalg.inv(Jf.T @ Jf) * sig**2
        crb = np.sqrt(np.maximum(np.diag(C)[A.shape[1]:], 0))
    except np.linalg.LinAlgError:
        crb = np.full(K, np.inf)
    amp = np.hypot(c[1::2], c[2::2])
    return lam, crb, amp, sig


def gp_path(t, x, y, seed):
    from pdefactor.core.structfit import extract_modes_ic
    from pdefactor.interp.gp import fit_gp

    post = fit_gp(t, x, y, S=8, period_x=L, seed=seed)
    S, w = post.samples, post.weights
    mean = np.tensordot(w, S, 1)
    tg, xg = post.t, post.x
    with np.errstate(all="ignore"):
        m = extract_modes_ic(mean, tg, xg, noise=0.0, refine=True, noise_draws=np.sqrt(2) * (S - mean[None]))[0]
    out = np.full(K, np.nan)
    for k in range(1, K + 1):
        sel = np.isclose(np.abs(m.kappa), k, atol=1e-6)
        if sel.any():
            out[k - 1] = m.lam[sel][np.argmax(m.snr[sel])].real
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=3)
    ap.add_argument("--n", type=int, default=400)
    ap.add_argument("--noise", type=float, default=0.05)
    a = ap.parse_args()
    truth = -D * np.arange(1, K + 1) ** 2
    rows = []
    for sd in range(a.seeds):
        f = case("heat", seed=sd)
        t, x, y, _ = sample_scattered(f, a.n, noise=a.noise, rng=sd)
        lam_r, crb, amp, sig = raw_scan(t, x, np.real(y))
        try:
            lam_g = gp_path(t, x, np.real(y), sd)
        except Exception as exc:  # noqa: BLE001
            print("GP path failed:", exc)
            lam_g = np.full(K, np.nan)
        rows.append((np.abs(lam_r - truth), crb, amp / sig, np.abs(lam_g - truth)))
        print(f"seed {sd}: raw |dlam| {np.round(rows[-1][0], 2)}  CRB {np.round(crb, 2)}  "
              f"GP |dlam| {np.round(rows[-1][3], 2)}", flush=True)
    R = np.array([r[0] for r in rows]); C = np.array([r[1] for r in rows])
    G = np.array([r[3] for r in rows]); A = np.array([r[2] for r in rows])
    lines = [f"# E16 — raw-data mode scan vs GP path, heat {a.n} pts @ {100 * a.noise:g} % ({a.seeds} seeds)", "",
             "| kappa | true lam | raw scan median abs dlam | raw CRB median | GP path median abs dlam (NaN = mode not found) | amp/sigma |",
             "|---|---|---|---|---|---|"]
    for k in range(K):
        lines.append(f"| {k + 1} | {truth[k]:.1f} | {np.median(R[:, k]):.3f} | {np.median(C[:, k]):.3f} | "
                     f"{np.nanmedian(G[:, k]) if np.isfinite(G[:, k]).any() else float('nan'):.3f} "
                     f"({int(np.isfinite(G[:, k]).sum())}/{len(G)}) | {np.median(A[:, k]):.2f} |")
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    with open(os.path.join(HERE, "out", "e16_raw_scan.md"), "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
