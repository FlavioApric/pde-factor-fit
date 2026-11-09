"""E15 (S-PHASE4-ML): how much can *any* seed provider improve the per-bin pole step?

Arms, all through the same selection as extract_modes_ic (honesty rule: seeds only inside
r0..r0+extra, one per order, equal starts; VarPro; BIC), on held-out white-noise exponential sums:
- control: provider on, no seeds (a second pencil start per order): the equal-budget baseline;
- espira:  ESPIRA (Derevianko, Plonka, Petz, IMA J. Numer. Anal. 2023, arXiv:2106.15140): AAA
           rational approximation of the DFT, F_l = sum_j a_j (1 - z_j^N) / (1 - z_j w_l), whose
           poles in w are 1/z_j (scipy.interpolate.AAA); reported more robust than ESPRIT / MPM;
- oracle:  the true detectable poles as seeds (every prefix by amplitude): an upper bound for
           every learned or deterministic proposal method.
If the oracle does not beat the control, no seed method (L0 included) can improve this step.

Usage:  python analysis/exp/e15_seed_bounds.py [--n 500]
"""
from __future__ import annotations

import argparse
import importlib.util
import os
import warnings

import numpy as np

from pdefactor.learned import expsum

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("e12", os.path.join(HERE, "e12_l0_seeds.py"))
e12 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(e12)


def espira(y, dt, sigma, orders=range(1, 9)):
    from scipy.interpolate import AAA

    N = len(y)
    F = np.fft.fft(y)
    w = np.exp(-2j * np.pi * np.arange(N) / N)
    out = []
    for r in orders:
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                p = AAA(w, F, max_terms=r + 1, rtol=0.0, clean_up=False).poles()
        except Exception:  # noqa: BLE001 - a failed rational fit proposes nothing
            continue
        p = p[np.isfinite(p) & (np.abs(p) > 1e-12)]
        if len(p) == r:
            out.append(np.log(1 / p) / dt)
    return out


def arm_rows(kind, draws):
    rows = []
    for d in draws:
        if kind == "control":
            prov = lambda y, dt, sg: []  # noqa: E731
        elif kind == "espira":
            prov = espira
        else:
            s, a = expsum.detectable(d)
            o = np.argsort(-np.abs(a))
            prov = lambda y, dt, sg, s=s, o=o: [s[o[:r]] / 2.0 for r in range(1, len(s) + 1)]  # noqa: E731
        with np.errstate(all="ignore"):
            rows += e12.evaluate(prov, [d])
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=500)
    a = ap.parse_args()
    rng = np.random.default_rng(4242)
    draws = [d for d in (expsum.draw(rng) for _ in range(a.n)) if not d.colored]
    lines = [f"# E15 — seed-method upper bound ({len(draws)} white-noise draws)", "",
             "| arm | order acc | |dλ|/CRB median | p90 | merged pairs (|ds|<1.5, SNR>=40 dB) acc |",
             "|---|---|---|---|---|"]
    for kind in ("control", "espira", "oracle"):
        rows = arm_rows(kind, draws)
        eff = np.concatenate([np.asarray(r["eff"]) for r in rows if r["eff"]])
        tab = e12.summarise(rows)
        mp = tab.get(">=40 / |ds|<1.5", {}).get("order_acc", float("nan"))
        acc = np.mean([r["r_hat"] == r["r_true"] for r in rows])
        lines.append(f"| {kind} | {acc:.3f} | {np.median(eff):.2f} | {np.quantile(eff, 0.9):.2f} | {mp:.3f} |")
        print(lines[-1], flush=True)
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    with open(os.path.join(HERE, "out", "e15_seed_bounds.md"), "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
