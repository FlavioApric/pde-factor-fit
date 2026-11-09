"""Smallest end-to-end demo: simulate a PDE, run the algorithm, read the answer in plain words.

    python -m pdefactor.demo                      # default case, 5 % noise
    python -m pdefactor.demo heat --noise 0.02    # another case
    python -m pdefactor.demo --list               # all built-in cases

Part of pde-factor-fit (c) 2026 Flavio Pricoco, MIT.
"""
from __future__ import annotations

import argparse

import numpy as np

from . import aggregate as AG
from .loop import run_loop
from .synthetic import CASES, EXTRA_CASES, GENERAL_CASES, any_case, grid

MEANING = {
    "FIT-COMPATIBLE": "the data are consistent with a product of the factors printed below (NOT a proof the law is that equation)",
    "MISFIT": "no factor structure within the search bounds explains the data",
    "UNDECIDED": "the data cannot decide between structures",
}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("case", nargs="?", default="transport_plus_diffusion")
    ap.add_argument("--noise", type=float, default=0.05, help="noise std relative to std|u| (default 0.05)")
    ap.add_argument("--S", type=int, default=3, help="noisy copies standing in for the posterior (default 3)")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--list", action="store_true", help="print the built-in case names and exit")
    a = ap.parse_args(argv)
    if a.list:
        print("\n".join(CASES + EXTRA_CASES + GENERAL_CASES))
        return
    truth = any_case(a.case, seed=a.seed)
    t, x, u = grid(truth)
    sigma = a.noise * np.std(np.abs(u))
    samples, pis = AG.fake_posterior(u, sigma, a.S, rng=a.seed + 1)
    print(f"case '{a.case}': simulated field on a {len(t)} x {len(x)} grid, noise sigma = {sigma:.3g}")
    res = run_loop(samples, t, x, sigma, pis)
    print("\n" + res.summary())
    print("\nIn plain words:")
    print(" ", MEANING.get(res.label.split("(")[0].strip(), f"label {res.label}: see README, 'How to read the result'"))
    print("  recovered equation:", res.equation())


if __name__ == "__main__":
    main()
