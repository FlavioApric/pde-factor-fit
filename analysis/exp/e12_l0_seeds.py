"""E12 (S-PHASE4-ML): L0 learned seeds vs pencil + BIC on held-out exponential sums.

Per series the same selection as core.structfit.extract_modes_ic: pencil orders r0..r0+extra,
VarPro refinement, BIC; L0 on = the same plus the learned pole sets as extra candidates.

Metrics, by SNR band and by the minimum pole spacing |ds| (s = lam T):
- order accuracy: selected order == number of detectable poles (expsum.detectable);
- lam efficiency: matched |d lam| / CRB sigma_lam at the truth (structfit.sigma_lambda Fisher);
- false modes on the null class (pure noise passing the SNR gate) and on single-pole series.

Usage:  python analysis/exp/e12_l0_seeds.py [--train STEPS] [--n N]
Writes analysis/exp/out/e12_l0_seeds.{md,json}; the model to analysis/exp/cache/l0_expseeds.pt.
"""
from __future__ import annotations

import argparse
import json
import os
import time

import numpy as np
from scipy.optimize import linear_sum_assignment

from pdefactor.core.spectral import matrix_pencil
from pdefactor.core.structfit import _bin_rss, varpro_refine
from pdefactor.learned import expseeds, expsum

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "out")
CACHE = os.path.join(HERE, "cache")


def select(y, dt, sigma, provider=None, snr_min=3.0, max_order=8, extra=2):
    """One bin, exactly the extract_modes_ic selection (white noise, refine=True), honesty rule
    included: seeds only inside r0..r0+extra, one per order, a second pencil start otherwise."""
    tt = np.arange(len(y)) * dt
    level = np.abs(y).max()
    if level < snr_min * sigma:
        return np.zeros(0, complex)
    W = 1.0 / sigma
    tol = max(1e-6, snr_min * sigma / level)
    lam0, _, _ = matrix_pencil(y, dt, rel_tol=tol, max_order=max_order)
    orders = range(max(len(lam0), 1), min(len(lam0) + extra, max_order) + 1)
    cands = [(r, lam0 if r == len(lam0) else matrix_pencil(y, dt, order=r)[0]) for r in orders]
    if provider is not None:
        seeded = {}
        for p in provider(y, dt, sigma):
            p = np.asarray(p, complex)
            if len(p) in orders and len(p) not in seeded and np.all(np.isfinite(p)):
                seeded[len(p)] = p
        cands += [(r, seeded[r] if r in seeded else matrix_pencil(y, dt, order=r, pencil=len(y) // 3)[0])
                  for r in orders]
    best = None
    nobs = 2 * len(y)
    for r, lam in cands:
        lam = varpro_refine(y, tt, lam, W)
        rss, a = _bin_rss(y, tt, lam, W)
        bic = rss + 4 * r * np.log(nobs)
        if best is None or bic < best[0]:
            best = (bic, lam, a)
    _, lam, a = best
    keep = np.abs(a) * np.exp(np.real(lam) * tt[-1] / 2) > snr_min * sigma / 3
    return lam[keep]


def crb(s, amp, nt, sigma, T):
    """CRB std of each lam at the truth (white complex noise sigma), joint Fisher of all poles."""
    if len(s) == 0:
        return np.zeros(0)
    t = np.linspace(0, T, nt)
    lam = s / T
    cols = []
    for l, a in zip(lam, amp):
        g = np.exp(l * t)
        cols += [g, a * t * g]
    J = np.stack(cols, 1) / sigma  # circular complex noise E|e|^2 = sigma^2: Cov = (J^H J)^-1
    try:
        Cm = np.linalg.pinv(J.conj().T @ J)
    except np.linalg.LinAlgError:
        return np.full(len(s), np.inf)
    return np.sqrt(np.maximum(np.real(np.diag(Cm))[1::2], 0))


def evaluate(provider, draws):
    rows = []
    for d in draws:
        T = 2.0
        dt = T / (d.nt - 1)
        s_true, a_true = expsum.detectable(d)
        lam_hat = select(d.y, dt, d.sigma, provider)
        lam_true = s_true / T
        sd = crb(s_true, a_true, d.nt, d.sigma, T)
        eff = []
        if len(lam_true) and len(lam_hat):
            C = np.abs(lam_true[:, None] - lam_hat[None, :])
            i, j = linear_sum_assignment(C)
            eff = list(C[i, j] / np.maximum(sd[i], 1e-12))
        sep = np.inf
        if len(s_true) > 1:
            D = np.abs(s_true[:, None] - s_true[None, :])
            sep = D[np.triu_indices(len(s_true), 1)].min()
        snr_db = 20 * np.log10(np.sqrt(np.mean(np.abs(d.y) ** 2)) / d.sigma)
        rows.append(dict(r_true=len(s_true), r_hat=len(lam_hat), eff=eff, sep=float(sep), snr_db=float(snr_db),
                         colored=bool(d.colored)))
    return rows


def gated_null(rng, n, snr_min=3.0):
    """Pure-noise series that pass the per-bin SNR gate (max|y| >= snr_min sigma): unconditioned,
    only ~0.5 % do, and a null that never reaches the selection tests nothing."""
    out = []
    while len(out) < n:
        d = expsum.draw(rng, r=0)
        if np.abs(d.y).max() >= snr_min * d.sigma:
            out.append(d)
    return out


def summarise(rows):
    def band(r):
        return "<20" if r["snr_db"] < 20 else ("20-40" if r["snr_db"] < 40 else ">=40")

    def sepb(r):
        return "single/none" if r["r_true"] <= 1 else ("|ds|<1.5" if r["sep"] < 1.5 else "|ds|>=1.5")

    out = {}
    for key in sorted({(band(r), sepb(r)) for r in rows}):
        sel = [r for r in rows if (band(r), sepb(r)) == key]
        eff = np.concatenate([np.asarray(r["eff"]) for r in sel if r["eff"]] or [np.zeros(0)])
        out[" / ".join(key)] = dict(
            n=len(sel),
            order_acc=float(np.mean([r["r_hat"] == r["r_true"] for r in sel])),
            over=float(np.mean([r["r_hat"] > r["r_true"] for r in sel])),
            eff_median=float(np.median(eff)) if eff.size else float("nan"),
            eff_p90=float(np.quantile(eff, 0.9)) if eff.size else float("nan"),
        )
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--train", type=int, default=0, help="train for this many steps (0: load cache)")
    ap.add_argument("--n", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=12345)
    ap.add_argument("--threads", type=int, default=4)
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, "l0_expseeds.pt")
    if a.train:
        import torch

        torch.set_num_threads(a.threads)
        t0 = time.time()
        model = expseeds.train(steps=a.train, log=print)
        expseeds.save(model, path)
        print(f"trained in {time.time() - t0:.0f} s")
    model = expseeds.load(path)
    rng = np.random.default_rng(a.seed)  # held-out: a seed never used in training (train seed 0)
    draws = [expsum.draw(rng) for _ in range(a.n)]
    nulls = gated_null(rng, 300) + [expsum.draw(rng, r=1) for _ in range(300)]
    prov = lambda y, dt, sg: expseeds.proposals(model, y, dt, sg)
    res = {}
    # control: provider on but empty = the same extra (second-pencil) starts without learning
    arms = (("pencil+BIC", None), ("pencil+BIC+2nd start (control)", lambda y, dt, sg: []),
            ("pencil+BIC+L0", prov))
    for name, p in arms:
        t0 = time.time()
        rows = evaluate(p, draws)
        nrows = evaluate(p, nulls)
        white = [r for r in rows if not r["colored"]]
        res[name] = dict(
            table=summarise(white),
            table_colored=summarise([r for r in rows if r["colored"]]),
            order_acc=float(np.mean([r["r_hat"] == r["r_true"] for r in rows])),
            null_false_modes=float(np.mean([r["r_hat"] > r["r_true"] for r in nrows])),
            seconds=time.time() - t0,
        )
    with open(os.path.join(OUT, "e12_l0_seeds.json"), "w") as f:
        json.dump(res, f, indent=1)
    lines = ["# E12 — L0 learned seeds vs pencil + BIC (held-out exponential sums)", "",
             f"n = {a.n} draws (seed {a.seed}), nulls = 300 pure-noise series that pass the SNR gate + 300 single pole.", ""]
    for name, r in res.items():
        lines += [f"## {name}", f"order accuracy {r['order_acc']:.3f}; null/single-pole over-order rate "
                  f"{r['null_false_modes']:.3f}; {r['seconds']:.0f} s", "",
                  "White noise (the CRB is exact here):", "",
                  "| SNR dB / spacing | n | order acc | over-order | |dλ|/CRB median | p90 |", "|---|---|---|---|---|---|"]
        for k, v in r["table"].items():
            lines.append(f"| {k} | {v['n']} | {v['order_acc']:.3f} | {v['over']:.3f} | {v['eff_median']:.2f} | {v['eff_p90']:.2f} |")
        lines += ["", "AR(1) noise (white-noise selection and CRB, both misspecified; order columns only):", "",
                  "| SNR dB / spacing | n | order acc | over-order |", "|---|---|---|---|"]
        for k, v in r["table_colored"].items():
            lines.append(f"| {k} | {v['n']} | {v['order_acc']:.3f} | {v['over']:.3f} |")
        lines.append("")
    with open(os.path.join(OUT, "e12_l0_seeds.md"), "w") as f:
        f.write("\n".join(lines))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
