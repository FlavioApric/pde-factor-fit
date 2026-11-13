"""Evidence figure of the 20-page paper (paper/figures/fig_evidence.pdf). Needs numpy + matplotlib only.

    python code/experiments/make_fig_evidence.py

(a) large random-PDE benchmark per family, from claude/benchmark_tables/large.md (benchmarks/large_report.py);
(b) the 30-input development benchmark, from claude/benchmark_tables/p8_final_v5.md (as fig_bench).
Outcome colours (validated with the dataviz palette checker): right = dark blue, equivalent = light blue,
abstained or no answer = neutral gray, false-confident = orange with hatching (never colour alone).
"""
from __future__ import annotations

import re

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

from make_figs import MD, INK, save, parse_p8  # noqa: F401  (also applies the shared rcParams)

RIGHT, EQUIV, ABST, FC = "#1c5cab", "#6da7ec", "#8a8984", "#eb6834"
FAMILY = {"F1": "F1 first order", "F2": "F2 dispersive", "F3": "F3 irreducible 2nd order",
          "F4": "F4 products", "F5": "F5 3rd order / reaction"}


def parse_large():
    txt = (MD / "large.md").read_text(encoding="utf8")
    out = {}
    for head, body in re.findall(r"^## (.+?)\n(.*?)(?=^## |\Z)", txt, flags=re.S | re.M):
        m = re.match(r"(All draws|Family (F\d))", head)
        if not m:
            continue
        key = m.group(2) or "all"
        for line in body.splitlines():
            c = [s.strip() for s in line.strip().strip("|").split("|")]
            if c[0] in ("pipeline", "weak_sindy"):
                r, e, aok, ab, fc, wr, cr = (int(v) for v in c[2:9])
                out[(key, c[0])] = dict(right=r, equiv=e, abst=aok + ab + cr, fc=fc + wr, n=r + e + aok + ab + fc + wr + cr)
    return out


def bars(ax, rows, ylabels, scale):
    y = np.arange(len(rows))[::-1]
    for yi, r in zip(y, rows):
        left = 0.0
        for val, col, hatch in [(r["right"], RIGHT, None), (r["equiv"], EQUIV, None),
                                (r["abst"], ABST, None), (r["fc"], FC, "////")]:
            w = val * scale(r)
            if w:
                ax.barh(yi, w, left=left, height=0.66, color=col, hatch=hatch, edgecolor="white", lw=0.8)
            left += w
    ax.set_yticks(y)
    ax.set_yticklabels(ylabels)
    ax.tick_params(axis="y", length=0)
    return y


def main():
    L = parse_large()
    fig, (a, b) = plt.subplots(1, 2, figsize=(6.5, 2.9), gridspec_kw=dict(width_ratios=[1.35, 1], wspace=0.75))
    keys = ["all", "F1", "F2", "F3", "F4", "F5"]
    rows, labels = [], []
    for k in keys:
        for meth, lab in (("pipeline", "this method"), ("weak_sindy", "weak SINDy")):
            rows.append(L[(k, meth)])
            name = "all 285" if k == "all" else FAMILY[k]
            labels.append(f"{name}: {lab}" if meth == "pipeline" else lab)
    y = bars(a, rows, labels, lambda r: 100.0 / r["n"])
    for yi, r in zip(y, rows):
        a.text(101.5, yi, f"{100 * (r['right'] + r['equiv']) / r['n']:.0f}%", va="center", fontsize=7, color=INK)
    for yi in y[1::2][:-1]:
        a.axhline(yi - 0.5, color="#d8d7d2", lw=0.6)
    a.set_xlim(0, 100)
    a.set_xticks([0, 25, 50, 75, 100])
    a.set_xlabel("share of draws (%)")
    a.set_title("(a) 285 random equations, grid, 1% noise", loc="left")
    a.tick_params(axis="y", labelsize=6.8)

    P = parse_p8()
    names = [("pipeline", "this method"), ("weak_sindy", "weak SINDy"), ("ensemble_sindy", "ensemble SINDy"),
             ("sbr_sindy", "SBR SINDy"), ("pdefind", "PDE-FIND"), ("bopdmd", "BOP-DMD")]
    y = bars(b, [P[k] for k, _ in names], [l for _, l in names], lambda r: 1.0)
    for yi, (k, _) in zip(y, names):
        b.text(30.6, yi, f"{P[k]['right'] + P[k]['equiv']}/30", va="center", fontsize=7, color=INK)
    b.set_xlim(0, 30)
    b.set_xticks([0, 10, 20, 30])
    b.set_xlabel("number of the 30 inputs")
    b.set_title("(b) development benchmark", loc="left")
    b.tick_params(axis="y", labelsize=7.2)

    hs = [mpl.patches.Patch(color=RIGHT), mpl.patches.Patch(color=EQUIV), mpl.patches.Patch(color=ABST),
          mpl.patches.Patch(facecolor=FC, hatch="////", edgecolor="white")]
    fig.legend(hs, ["right", "equivalent", "abstained / no result", "false-confident"], loc="upper center",
               bbox_to_anchor=(0.5, 1.06), ncol=4, handlelength=1.2)
    save(fig, "fig_evidence")


if __name__ == "__main__":
    main()
