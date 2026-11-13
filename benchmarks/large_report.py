"""Report of the large random-PDE benchmark (benchmarks/bench_large.py): counts, 95 % intervals, paired tests.

    python benchmarks/large_report.py [--in benchmarks/out/large.jsonl] [--out claude/benchmark_tables/large.md]

Reads finished rows only. Classes are those of p8_report / e13_summary (right, equivalent, abstain-ok,
abstain, false-confident, wrong, CRASH). Per method and per (family, noise): n, right+equivalent with a
Wilson 95 % interval, false-confident with a Clopper-Pearson 95 % upper bound (0 events: 3/n rule is
exceeded by the exact bound, which is reported). Paired comparison pipeline vs each other method on the
same draws: exact two-sided sign (McNemar) test on right+equivalent. Draws are independent equations and
independent noise, so the intervals are valid binomial intervals over draws.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from math import comb, sqrt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "benchmarks"))
import p8_report as P  # noqa: E402  (classify_e13, e13_classes, CLASSES; adds code/ and experiments to sys.path)

METHODS = ("pipeline", "core", "pdefind", "weak_sindy", "ensemble_sindy", "sbr_sindy", "bopdmd")
GOOD = ("right", "equivalent")


def wilson(k, n, z=1.959964):
    if n == 0:
        return (float("nan"),) * 2
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h


def _binom_cdf(k, n, p):
    return sum(comb(n, i) * p**i * (1 - p) ** (n - i) for i in range(k + 1))


def cp_upper(k, n, alpha=0.05):
    """Clopper-Pearson one-sided 95 % upper bound of a proportion (bisection on the binomial cdf)."""
    if n == 0:
        return float("nan")
    if k >= n:
        return 1.0
    lo, hi = k / n, 1.0
    for _ in range(60):
        m = (lo + hi) / 2
        lo, hi = (m, hi) if _binom_cdf(k, n, m) > alpha else (lo, m)
    return hi


def sign_test(b, c):
    """Exact two-sided McNemar: b = pipeline right and other not, c = the reverse."""
    n = b + c
    if n == 0:
        return 1.0
    return min(1.0, 2 * sum(comb(n, i) for i in range(min(b, c) + 1)) / 2**n)


def pct(k, n):
    lo, hi = wilson(k, n)
    return f"{100 * k / n:.1f} [{100 * lo:.1f}, {100 * hi:.1f}]" if n else "-"


def build(rows, cls):
    ms = [m for m in METHODS if any(m in r for r in rows)]
    noises = sorted({float(r["noise"]) for r in rows})
    fams = sorted({r["family"] for r in rows})
    L = [f"# Large random-PDE benchmark", "",
         f"{len(rows)} draws (equations x noise), families {', '.join(fams)}, "
         f"{len({(r['family'], r['seed']) for r in rows})} distinct equations, noise {noises} (x std u), "
         "noisy regular grid. Each draw is an independent equation with an independent field; none was used "
         "to tune the pipeline. Intervals are 95 %.", ""]

    def cl(r, m):
        return cls[(r["family"], r["seed"], r["noise"], m)]

    def block(title, sub):
        out = [f"## {title} (n = {len(sub)})", "",
               "| method | right+equiv % [Wilson] | " + " | ".join(P.CLASSES) + " | false-conf upper 95 % |",
               "|---" * (len(P.CLASSES) + 3) + "|"]
        for m in ms:
            s = [r for r in sub if m in r]
            c = Counter(cl(r, m) for r in s)
            g = sum(c[k] for k in GOOD)
            fc = c["false-confident"] + c["wrong"]
            out.append(f"| {m} | {pct(g, len(s))} | " + " | ".join(str(c[k]) for k in P.CLASSES)
                       + f" | {100 * cp_upper(fc, len(s)):.1f} % |")
        pairs = []
        for m in ms[1:]:
            both = [r for r in sub if "pipeline" in r and m in r]
            b = sum(cl(r, "pipeline") in GOOD and cl(r, m) not in GOOD for r in both)
            c_ = sum(cl(r, "pipeline") not in GOOD and cl(r, m) in GOOD for r in both)
            pairs.append(f"{m}: pipeline-only {b}, {m}-only {c_}, p = {sign_test(b, c_):.2g}")
        return out + ["", "Paired on the same draws (exact sign test, right+equivalent): " + "; ".join(pairs), ""]

    L += block("All draws", rows)
    for nz in noises:
        L += block(f"Noise {nz:g}", [r for r in rows if float(r["noise"]) == nz])
    for f in fams:
        L += block(f"Family {f}", [r for r in rows if r["family"] == f])
    bad = [(r, m) for r in rows for m in ("pipeline", "core") if m in r
           and cl(r, m) in ("false-confident", "wrong", "CRASH")]
    L += ["## False-confident / wrong / CRASH (pipeline, core)", ""]
    L += [f"- {m} {r['family']}-{r['seed']} noise {r['noise']}: {cl(r, m)}, truth {r['truth']} -> {r[m]['label']} "
          f"{r[m]['factors']}" for r, m in bad] or ["- none"]
    have = {(r["family"], int(r["seed"]), float(r["noise"])) for r in rows}
    top = max(int(r["seed"]) for r in rows)
    miss = sorted((f, s, nz) for f in fams for s in range(top + 1) for nz in noises if (f, s, nz) not in have)
    L += ["", f"## Draws without a result ({len(miss)} of {len(fams) * (top + 1) * len(noises)} planned)", "",
          "These draws hit the per-draw time limit (3 h) or failed; they carry no row, so they are NOT counted in "
          "the tables above. Reading the tables as if they were abstentions would be wrong: the denominators exclude them. "
          "Share per family: " + ", ".join(f"{f} {sum(m[0] == f for m in miss)}/{(top + 1) * len(noises)}" for f in fams) + ".", ""]
    if "pipeline" in ms:
        gp = sum(cl(r, "pipeline") in GOOD for r in rows)
        tot = len(rows) + len(miss)
        L += [f"Worst case for the pipeline, counting every missing draw as a failure: {gp}/{tot} = {100 * gp / tot:.1f} % "
              f"right+equivalent (Wilson 95 % {100 * wilson(gp, tot)[0]:.1f}-{100 * wilson(gp, tot)[1]:.1f}). "
              "The tables above are conditional on the draw finishing within the limit; the slowest draws are not a random subset.", "",
              "Reading the baselines: weak_sindy always returns one equation and never abstains, so every wrong "
              "answer is counted as false-confident by construction.", ""]
    L += [f"- {f}-{s} noise {nz:g}" for f, s, nz in miss] or ["- none"]
    return "\n".join(L) + "\n"


def classes(rows):
    out = {}
    for r in rows:
        one = P.e13_classes([r])  # {(family, seed, method): class}
        for (f, s, m), v in one.items():
            out[(f, s, r["noise"], m)] = v
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", type=Path, default=ROOT / "benchmarks" / "out" / "large.jsonl")
    ap.add_argument("--out", type=Path, default=ROOT / "claude" / "benchmark_tables" / "large.md")
    a = ap.parse_args()
    rows = [json.loads(ln) for ln in a.inp.read_text(encoding="utf-8").splitlines() if ln.strip()]
    P.E13_METHODS = METHODS
    md = build(rows, classes(rows))
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(md, encoding="utf-8", newline="\n")
    print(md[:3000])


if __name__ == "__main__":
    main()
