"""E13 (plan v2.13, PHASE4 P0.3): the pipeline on random PDEs drawn by family (pdefactor.simulator),
none of which was used to tune anything. Noisy grid (the benchmark's grid path: one sample, white
noise sigma), core alone, the outer loop, and the SINDy baselines.

Per factor, an information proxy computed from the truth only (not from any method's output, so the
score is not circular): a mode is visible when its grid matched-filter SNR
|A| sqrt(nx sum_t |e^{lam t}|^2) / sigma >= 3 (the core's snr_min), and a factor is identifiable when
it has visible modes at >= dx + 1 distinct |kappa| (R4-T4 / T40). Where some factor is not
identifiable, ID-KER / UNDECIDED is the correct answer (correct abstain, PHASE4 P0.2), and a
FIT-COMPATIBLE answer with a wrong set is false-confident.

Usage: python e13_random_pdes.py --seeds 0 1 2 --noise 0.01 --out benchmarks/out/e13.jsonl
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import traceback
import warnings
from pathlib import Path

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
warnings.filterwarnings("ignore")

from pdefactor.simulator import FAMILIES, match, random_pde  # noqa: E402
from pdefactor.symbols import tau, xi  # noqa: E402
from pdefactor.synthetic import grid  # noqa: E402

SINDY = ("pdefind", "weak_sindy", "ensemble_sindy")


def _roots(q, k):
    from pdefactor.synthetic import branch_roots

    return branch_roots(q, k)


def identifiable(draw, t, x, sigma, snr=3.0, z=3.0):
    """Per true factor: (resolvable, number of |kappa| with a visible mode, dx, smallest term z-score).
    Visible mode: grid matched-filter SNR >= snr. Resolvable factor: visible modes at >= dx + 1
    distinct |kappa| (R4-T4 / T40) AND every term of the factor shifts some visible root by more than
    z sigma_lam when it is removed (sigma_lam ~ sqrt(6) / (SNR T), the CRB order of a damped
    exponential's rate). A term below that is not in the data at this noise: the lower-degree law is
    then the right answer of a noisy fit, and the case counts as not resolvable."""
    out = []
    nx = len(x)
    T = t[-1] - t[0]
    for q in draw.factors:
        p = sp.Poly(q, tau, xi)
        dx = max(b for _, b in p.monoms())
        vis = []  # (kappa, snr)
        for c in draw.field.components:
            same = sp.expand(c.Q - q) == 0
            conj = not same and sp.expand(sp.conjugate(c.Q).subs({sp.conjugate(tau): tau, sp.conjugate(xi): xi}) - q) == 0
            if not (same or conj):
                continue
            for k, lam, a in zip(c.kappas, c.lams, c.amps):
                s = abs(a) * np.sqrt(nx * np.sum(np.abs(np.exp(lam * t)) ** 2)) / max(sigma, 1e-300)
                if s >= snr:
                    vis.append((float(k), float(s)))
        ks = {round(abs(k), 9) for k, _ in vis}
        lead = max(a for a, _ in p.monoms())
        zmin = np.inf
        for mo, cval in zip(p.monoms(), p.coeffs()):
            if mo == (lead, 0):
                continue
            q0 = sp.expand(q - cval * tau**mo[0] * xi**mo[1])
            zt = 0.0
            for k, s in vis:
                r1, r0 = _roots(q, k), _roots(q0, k)
                if len(r0) != len(r1):
                    zt = np.inf
                    break
                shift = max(np.min(np.abs(r0 - v)) for v in r1)
                zt = max(zt, shift * s * T / np.sqrt(6))
            zmin = min(zmin, zt)
        out.append((bool(len(ks) >= dx + 1 and zmin >= z), len(ks), dx, float(zmin)))
    return out


def run_one(family, seed, noise, methods):
    d = random_pde(family, seed)
    t, x, u = grid(d.field)
    rng = np.random.default_rng(1000 + seed)
    sig = noise * np.std(u)
    un = u + sig * rng.standard_normal(u.shape)
    ident = identifiable(d, t, x, sig)
    row = dict(family=family, seed=seed, noise=noise, truth=[str(q) for q in d.factors], amp_law=d.amp_law,
               n_kappa=len(d.kappas), ident=[[bool(a), int(b), int(c), float(zz)] for a, b, c, zz in ident], all_ident=bool(all(i[0] for i in ident)))
    for m in methods:
        t0 = time.perf_counter()
        try:
            if m == "core":
                from pdefactor.core.structfit import analyze_structured

                r = analyze_structured(un, t, x, noise=sig, real=True)
                facs, label = [fr.sympy for fr in r.factors], r.label
            elif m == "pipeline":
                from pdefactor.loop import run_loop

                r = run_loop([un], t, x, sig, bootstrap=0)
                facs, label = r.pruned(), r.label
            else:
                from pdefactor.baselines import BASELINES as B

                r = B[m](un, t, x, noise=sig)
                facs, label = r.factors, "n/a"
            ok, err = match(d.factors, facs) if facs else (False, float("inf"))
            row[m] = dict(label=label, factors=[str(q) for q in facs], ok=ok, err=err,
                          runtime=time.perf_counter() - t0)
        except Exception as e:  # noqa: BLE001  (a crash is a reported failure)
            row[m] = dict(label="CRASH", factors=[], ok=False, err=float("inf"), runtime=time.perf_counter() - t0,
                          error=f"{type(e).__name__}: {e}", trace=traceback.format_exc()[-600:])
    return row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--families", nargs="*", default=list(FAMILIES))
    ap.add_argument("--seeds", nargs="*", type=int, default=[0, 1, 2, 3])
    ap.add_argument("--noise", type=float, default=0.01)
    ap.add_argument("--methods", nargs="*", default=["core", "pipeline", *SINDY])
    ap.add_argument("--out", default=str(ROOT / "benchmarks" / "out" / "e13_random.jsonl"))
    a = ap.parse_args()
    done = set()
    out = Path(a.out)
    if out.exists():
        for line in out.read_text().splitlines():
            r = json.loads(line)
            done.add((r["family"], r["seed"], r["noise"]))
    for s in a.seeds:
        for fam in a.families:
            if (fam, s, a.noise) in done:
                continue
            row = run_one(fam, s, a.noise, a.methods)
            with out.open("a") as fh:
                fh.write(json.dumps(row, default=str) + "\n")
            print(fam, s, "ident" if row["all_ident"] else "not-ident",
                  {m: (row[m]["label"], row[m]["ok"], round(row[m]["runtime"])) for m in a.methods}, flush=True)


if __name__ == "__main__":
    main()
