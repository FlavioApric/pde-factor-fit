"""Coverage table (markdown) from coverage.py jsonl: mean over cases and seeds per (n, noise), plus per case.
usage: cov_table.py file.jsonl [file2.jsonl ...]"""
import json
import sys
from collections import defaultdict

import numpy as np

for fn in sys.argv[1:]:
    R = [json.loads(l) for l in open(fn)]
    print(f"\n### {fn.split('/')[-1]} ({len(R)} fits)\n")
    print("| n | noise | fits | cov50 | cov90 | cov95 | σ̂/σ | rmse/sd | time s |")
    print("|---|---|---|---|---|---|---|---|---|")
    g = defaultdict(list)
    for r in R:
        g[(r["n"], r["noise"])].append(r)
    for (n, nz), rs in sorted(g.items()):
        c = np.array([[r["cov"][k] for k in ("0.5", "0.9", "0.95")] for r in rs])
        sh = np.median([r["sigma_hat"] / r["sigma"] for r in rs])
        rr = np.median([r["rmse"] / r["sd"] for r in rs])
        print(f"| {n} | {nz} | {len(rs)} | {c[:, 0].mean():.3f} | {c[:, 1].mean():.3f} | {c[:, 2].mean():.3f} | "
              f"{sh:.2f} | {rr:.2f} | {np.median([r['time'] for r in rs]):.0f} |")
    print("\nper case (cov90, mean over seeds):\n")
    cases = sorted({r["case"] for r in R})
    keys = sorted(g)
    print("| case | " + " | ".join(f"{n}/{nz}" for n, nz in keys) + " |")
    print("|---|" + "---|" * len(keys))
    for cs in cases:
        row = []
        for k in keys:
            v = [r["cov"]["0.9"] for r in g[k] if r["case"] == cs]
            row.append(f"{np.mean(v):.3f}" if v else "–")
        print(f"| {cs} | " + " | ".join(row) + " |")
