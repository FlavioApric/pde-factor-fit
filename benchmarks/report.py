"""Summarise benchmarks/out/runs.jsonl -> benchmarks/out/summary.md, reliability.png, slopes.

    .venv/Scripts/python.exe benchmarks/report.py [runs.jsonl]
"""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from benchmarks import metrics as M  # noqa: E402
from benchmarks.bench import METHODS, NOISES, OUT, SAMPLINGS  # noqa: E402

SAMP = [str(s) for s in SAMPLINGS]
PROB_METHODS = ("core_v2", "ensemble_sindy", "sbr_sindy")


def load(path):
    return [json.loads(line) for line in Path(path).read_text().splitlines() if line.strip()]


def _q(v):
    v = np.asarray([z for z in v if z is not None and np.isfinite(z)], float)
    if not len(v):
        return "—"
    a, b, c = np.percentile(v, [25, 50, 75])
    return f"{b:.1e} [{a:.0e}, {c:.0e}]"


def _rate(rows, key="factor_set"):
    return np.mean([bool(r[key]) for r in rows]) if rows else np.nan


def group(rows, *keys):
    g = defaultdict(list)
    for r in rows:
        g[tuple(str(r[k]) for k in keys)].append(r)
    return g


def calib_pairs(rows):
    p, y = [], []
    for r in rows:
        if not r.get("probs"):
            continue
        tr = r["true_structure"]
        seen = False
        for st, pi in r["probs"]:
            hit = st == tr
            seen |= hit
            p.append(pi)
            y.append(1.0 if hit else 0.0)
        if not seen:
            p.append(0.0)
            y.append(1.0)
    return np.array(p), np.array(y)


def table_main(rows):
    g = group(rows, "method", "sampling", "noise")
    hdr = "| method | sampling | " + " | ".join(f"σ={n:g}" for n in NOISES) + " |"
    out = [hdr, "|" + "---|" * (2 + len(NOISES))]
    for m in METHODS:
        for s in SAMP:
            cells = []
            for n in NOISES:
                rr = g.get((m, s, str(n)), [])
                if not rr:
                    cells.append("—")
                    continue
                ok = [r for r in rr if r["factor_set"]]
                med = np.median([r["coef_err"] for r in ok]) if ok else np.nan
                cells.append(f"{_rate(rr):.2f} ({len(rr)}) / {med:.0e}" if ok else f"{_rate(rr):.2f} ({len(rr)}) / —")
            out.append(f"| {m} | {s} | " + " | ".join(cells) + " |")
    return "\n".join(out)


def table_per_case(rows, sampling="grid"):
    from pdefactor.synthetic import CASES

    g = group([r for r in rows if r["sampling"] == sampling], "case", "method")
    out = ["| case | " + " | ".join(METHODS) + " |", "|" + "---|" * (1 + len(METHODS))]
    for c in CASES:
        cells = []
        for m in METHODS:
            rr = g.get((c, m), [])
            byn = group(rr, "noise")
            cells.append(" ".join(f"{_rate(byn.get((str(n),), [])):.1f}" if byn.get((str(n),)) else "·" for n in NOISES))
        out.append(f"| {c} | " + " | ".join(cells) + " |")
    return "\n".join(out)


def table_struct(rows):
    g = group(rows, "method", "sampling")
    out = ["| method | " + " | ".join(SAMP) + " |", "|" + "---|" * (1 + len(SAMP))]
    for m in METHODS:
        out.append(f"| {m} | " + " | ".join(f"{_rate(g.get((m, s), []), 'struct_ok'):.2f}" for s in SAMP) + " |")
    return "\n".join(out)


def table_labels(rows):
    out = ["| method | sampling | σ | FIT-COMPATIBLE | MISFIT | ID-KER | UNDECIDED | ERROR |", "|---|---|---|---|---|---|---|---|"]
    g = group(rows, "method", "sampling", "noise")
    for m in ("core_v2", "core_v1"):
        for s in SAMP:
            for n in NOISES:
                rr = g.get((m, s, str(n)), [])
                if not rr:
                    continue
                c = Counter(("ERROR" if r.get("error") else r["label"].split("(")[0]) for r in rr)
                tot = len(rr)
                out.append(f"| {m} | {s} | {n:g} | " + " | ".join(
                    f"{c.get(k, 0) / tot:.2f}" for k in ("FIT-COMPATIBLE", "MISFIT", "ID-KER", "UNDECIDED", "ERROR")) + " |")
    return "\n".join(out)


def table_weights(rows):
    g = group([r for r in rows if r.get("weight_err") is not None], "method", "sampling")
    out = ["| method | " + " | ".join(SAMP) + " |", "|" + "---|" * (1 + len(SAMP))]
    for m in ("core_v2", "core_v1"):
        out.append(f"| {m} | " + " | ".join(f"{_q([r['weight_err'] for r in g.get((m, s), [])])} (n={len(g.get((m, s), []))})" for s in SAMP) + " |")
    return "\n".join(out)


def table_calibration(rows):
    out = ["| method | sampling | pairs | runs | ECE | Brier | mean p(true) |", "|---|---|---|---|---|---|---|"]
    for m in PROB_METHODS:
        for s in SAMP + ["all"]:
            rr = [r for r in rows if r["method"] == m and (s == "all" or r["sampling"] == s) and not r.get("error")]
            p, y = calib_pairs(rr)
            if not len(p):
                continue
            pt = [max([pi for st, pi in r["probs"] if st == r["true_structure"]] or [0]) for r in rr if r.get("probs")]
            out.append(f"| {m} | {s} | {len(p)} | {len(pt)} | {M.ece(p, y):.3f} | {M.brier(p, y):.3f} | {np.mean(pt):.2f} |")
    return "\n".join(out)


def table_runtime(rows):
    g = group(rows, "method", "sampling")
    out = ["| method | " + " | ".join(SAMP) + " | total (s) |", "|" + "---|" * (2 + len(SAMP))]
    for m in METHODS:
        tot = sum(r["runtime"] for r in rows if r["method"] == m)
        out.append(f"| {m} | " + " | ".join(
            (lambda v: f"{np.median(v):.2f} [{np.percentile(v, 25):.2f}, {np.percentile(v, 75):.2f}]")(
                [r["runtime"] for r in g.get((m, s), [])] or [np.nan]) for s in SAMP) + f" | {tot:.0f} |")
    return "\n".join(out)


def table_rounding(rows):
    """Baselines on the full grid: factor-set rate when the fitted symbol is rounded to d decimals."""
    from pdefactor.baselines.common import factor_symbol
    from pdefactor.synthetic import case, grid

    fields = {}
    out = ["| method | d=1 | d=2 (default) | d=3 |", "|---|---|---|---|"]
    for m in ("pdefind", "weak_sindy", "ensemble_sindy", "sbr_sindy", "bopdmd"):
        rr = [r for r in rows if r["method"] == m and r["sampling"] == "grid" and r.get("coeffs")]
        cells = []
        for d in (1, 2, 3):
            ok = []
            for r in rr:
                c = {tuple(map(int, k.split(","))): complex(*v) for k, v in r["coeffs"].items()}
                c = {k: (v.real if v.imag == 0 else v) for k, v in c.items()}
                if r["case"] not in fields:
                    f = case(r["case"])
                    fields[r["case"]] = (f, *grid(f)[:2])
                f, t, x = fields[r["case"]]
                facs, _ = factor_symbol(c, d)
                ok.append(M.score(r["case"], f, t, x, facs)["factor_set"])
            cells.append(f"{np.mean(ok):.2f}" if ok else "—")
        out.append(f"| {m} | " + " | ".join(cells) + " |")
    return "\n".join(out)


def slopes(rows):
    """log-log slope of the median coef_err (correct runs) vs noise, full grid, per method (T14: <= 1/3 worst case)."""
    out = ["| method | slope | noises used |", "|---|---|---|"]
    for m in METHODS:
        xs, ys = [], []
        for n in NOISES[1:]:
            v = [r["coef_err"] for r in rows if r["method"] == m and r["sampling"] == "grid" and r["noise"] == n and r["factor_set"]]
            if len(v) >= 5:
                xs.append(np.log10(n))
                ys.append(np.log10(np.median(v)))
        if len(xs) >= 2:
            out.append(f"| {m} | {np.polyfit(xs, ys, 1)[0]:.2f} | {len(xs)} |")
    return "\n".join(out)


def failures(rows):
    """Cells (method, case, sampling, noise) with factor-set rate 0 among methods that are right on exact grid."""
    out = []
    g = group(rows, "method", "case", "sampling", "noise")
    for (m, c, s, n), rr in sorted(g.items()):
        if s == "grid" and _rate(rr) < 1:
            labs = Counter(r["label"] for r in rr)
            sts = Counter(json.dumps(r.get("structure")) for r in rr)
            errs = Counter(r["error"].split(":")[0] for r in rr if r.get("error"))
            out.append(f"- {m} · {c} · σ={n}: rate {_rate(rr):.1f}; labels {dict(labs)}; structures {dict(sts.most_common(2))}"
                       + (f"; errors {dict(errs)}" if errs else ""))
    return "\n".join(out)


def reliability_plot(rows, path):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, len(PROB_METHODS), figsize=(4.2 * len(PROB_METHODS), 4.2), sharey=True)
    for ax, m in zip(axes, PROB_METHODS):
        for s, mk in zip(SAMP, ("o", "s", "^")):
            p, y = calib_pairs([r for r in rows if r["method"] == m and r["sampling"] == s and not r.get("error")])
            if not len(p):
                continue
            rel = M.reliability(p, y, bins=10)
            px = [r[2] for r in rel if r[4] >= 5]
            py = [r[3] for r in rel if r[4] >= 5]
            ax.plot(px, py, marker=mk, label=f"{s} (ECE {M.ece(p, y):.2f})")
        ax.plot([0, 1], [0, 1], "k--", lw=0.8)
        ax.set_title(m)
        ax.set_xlabel("predicted p(structure)")
        ax.legend(fontsize=8, loc="upper left")
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
    axes[0].set_ylabel("observed frequency (structure = truth)")
    fig.suptitle("Reliability of structure probabilities (bins with ≥ 5 pairs)")
    fig.tight_layout()
    fig.savefig(path, dpi=130)


def main(path=OUT / "runs.jsonl"):
    rows = load(path)
    n_err = sum(1 for r in rows if r.get("error"))
    parts = [
        f"# Benchmark summary\n\nrows: {len(rows)}, method errors (crashes): {n_err}. "
        "Scattered inputs use the griddata PLACEHOLDER interpolator.\n",
        "## Factor-set recovery: rate (n runs) / median coef_err of correct runs\n", table_main(rows),
        "\n## Full grid, per case: factor-set rate at σ = " + ", ".join(f"{n:g}" for n in NOISES) + "\n", table_per_case(rows, "grid"),
        "\n## 2000 scattered, per case\n", table_per_case(rows, "2000"),
        "\n## 400 scattered, per case\n", table_per_case(rows, "400"),
        "\n## Exact structure (degrees, |c| ≥ 1e-2) rate\n", table_struct(rows),
        "\n## Core labels\n", table_labels(rows),
        "\n## Weight error (cores, runs with right factor set, beam excluded): median [IQR]\n", table_weights(rows),
        "\n## Calibration of structure probabilities\n", table_calibration(rows),
        "\n## Rounding sensitivity of the baselines (full grid)\n", table_rounding(rows),
        "\n## Slope of coef_err vs noise (full grid)\n", slopes(rows),
        "\n## Runtime per run (s): median [IQR]\n", table_runtime(rows),
        "\n## Full-grid cells below rate 1\n", failures(rows),
    ]
    (OUT / "summary.md").write_text("\n".join(parts), encoding="utf-8")
    reliability_plot(rows, OUT / "reliability.png")
    print(f"wrote {OUT / 'summary.md'} and reliability.png ({len(rows)} rows)")


if __name__ == "__main__":
    main(*sys.argv[1:])
