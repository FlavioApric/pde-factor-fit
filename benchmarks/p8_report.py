"""Final P8 report: pipeline vs SINDy (vs pipeline + ML) on the 30 P8 inputs, plus the E13 table.

    OMP_NUM_THREADS=1 .venv/Scripts/python.exe benchmarks/p8_report.py [--ml PATH] [--out PATH]

Reads finished benchmark rows only; it runs no method. Inputs (defaults under benchmarks/out, falling
back to benchmarks/data):
  --pipeline       p8_pipeline.jsonl (bench_e2e rows, method "pipeline")
  --sindy          e2e_run6.jsonl: the SINDy rows (inputs unchanged since run 6, p8_sindy_arm.md) and
                   the run-6 pipeline reference row
  --sindy-override p8_sindy_schrodinger_cplxsigma.jsonl: the Schrodinger grid baseline rows on the
                   current complex-noise input (bench.CPLX_SIGMA); they replace the run-6 rows
  --ml             pipeline + ML arm (optional; reported as pending when the file is missing)
  --ml-same NOTE   the pipeline + ML arm is the pipeline arm (no ML layer changes an output); NOTE says
                   why. The arm then shows the pipeline rows and the note, nothing is rerun
  --e13            e13_v4.jsonl (E13 random-PDE draws, one row per draw, one key per method)

pipeline + ML schema: one JSON object per line, the bench_e2e pipeline row (same keys as
p8_pipeline.jsonl: case, method, noise, sampling, seed, label, factors, factor_set, struct_ok,
cover90, w_cover90, runtime, error, ...) plus `layers`, the learned layers that were on (a list of
names or a {name: bool} dict). `method` may be anything ("pipeline_ml" suggested); rows are matched
to cells by (case, noise, sampling, seed).

Classes (the E13 vocabulary): right / equivalent / abstain-ok / abstain / false-confident / wrong /
CRASH. "wrong" is e13_summary's "other" (a wrong answer under a label that is neither a claim nor an
abstention).
  P8 rows: benchmarks/micro.py outcome() (error -> CRASH; an answer is a claim only when labelled
  FIT-COMPATIBLE; repeated-root truths count UNDECIDED as right). A false-confident row is
  "equivalent" when the product of its factors equals the true symbol (simulator.match on the
  expanded products, the first half of e13_summary.equivalent; the chi^2 half needs the input data
  and is not run here); it is "wrong" when its label is neither FIT-COMPATIBLE nor n/a. An abstention
  is "abstain-ok" only when the row says the truth is not resolvable (all_ident false); the P8 rows
  carry no such flag, so every P8 abstention is "abstain".
  E13 rows: code/experiments/e13_summary.py classify() (its equivalent() regenerates the draw's grid and
  compares predictive chi^2: a few seconds per non-right row), with CRASH for rows labelled CRASH, as
  in e13_v4_summary.md. --e13-cache PATH stores those classes so a rerun is instant.
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for _p in (ROOT / "code", ROOT, ROOT / "benchmarks", ROOT / "code" / "experiments"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

CASES = ("advection_diffusion", "airy", "beam", "heat", "klein_gordon", "schrodinger", "telegraph", "transport",
         "transport_plus_diffusion", "wave")
DESIGNS = (("grid", 0.01), ("grid", 0.05), ("400", 0.05))
SEED = 0
CLASSES = ("right", "equivalent", "abstain-ok", "abstain", "false-confident", "wrong", "CRASH")
BASELINES = ("pdefind", "weak_sindy", "ensemble_sindy", "sbr_sindy", "bopdmd")
CLAIM = ("FIT-COMPATIBLE", "n/a")  # labels that claim an answer (SINDy methods have no labels: n/a)


def design_name(d):
    s, nz = d
    return f"{s} {nz * 100:g} %"


def _default(name):
    for sub in ("out", "data"):
        p = ROOT / "benchmarks" / sub / name
        if p.exists():
            return p
    return ROOT / "benchmarks" / "out" / name


def read_jsonl(p):
    p = Path(p)
    if not p.exists():
        return None
    return [json.loads(line) for line in p.read_text(encoding="utf-8").splitlines() if line.strip()]


def cell(r):
    return (r["case"], float(r["noise"]), str(r["sampling"]), int(r["seed"]))


P8_CELLS = [(c, nz, s, SEED) for s, nz in DESIGNS for c in CASES]


def by_cell(rows, method=None):
    """{cell: row} over the P8 cells (later rows win, as micro._rows)."""
    keep = set(P8_CELLS)
    out = {}
    for r in rows or ():
        if (method is None or r.get("method") == method) and cell(r) in keep:
            out[cell(r)] = r
    return out


# ---------------------------------------------------------------- P8 classification

def _truth(case):
    from benchmarks import metrics as M

    from pdefactor.synthetic import any_case

    return M.truth(case, any_case(case))


def product_equivalent(r):
    """Same product polynomial as the truth (simulator.match on the expanded products)."""
    import sympy as sp

    from pdefactor.simulator import match

    if not r.get("factors"):
        return False
    try:
        facs = [sp.sympify(q) for q in r["factors"]]
        return bool(match([sp.expand(sp.Mul(*_truth(r["case"])))], [sp.expand(sp.Mul(*facs))])[0])
    except Exception:  # noqa: BLE001  (an unparsable answer is not equivalent)
        return False


def classify_p8(r, equiv=product_equivalent):
    """E13 class of one P8 row, from micro.outcome (see the module docstring)."""
    from micro import outcome

    o = outcome(r)
    if o == "error":
        return "CRASH"
    if o == "right":
        return "right"
    if o == "abstain":
        return "abstain-ok" if r.get("all_ident") is False else "abstain"
    if equiv(r):
        return "equivalent"
    return "false-confident" if r.get("label") in CLAIM else "wrong"


# ---------------------------------------------------------------- arms

def load_arms(a):
    """[(arm name, {cell: row} or None when pending, note)]."""
    arms = []
    pipe = read_jsonl(a.pipeline)
    arms.append(("pipeline", by_cell(pipe, "pipeline") if pipe is not None else None, str(a.pipeline)))
    ml = read_jsonl(a.ml) if a.ml else None
    ml_note = str(a.ml) if a.ml else "no --ml file given"
    if getattr(a, "ml_same", None) and pipe is not None:
        ml, ml_note = [dict(r, method="pipeline_ml") for r in pipe if r.get("method") == "pipeline"],             f"= pipeline arm ({a.ml_same})"
    elif ml is not None:
        lay = sorted({json.dumps(r.get("layers"), sort_keys=True) for r in ml})
        ml_note += f"; layers {', '.join(lay)}"
    arms.append(("pipeline + ML", by_cell(ml) if ml is not None else None, ml_note))
    run6 = read_jsonl(a.sindy) or []
    over = read_jsonl(a.sindy_override) or []
    for m in BASELINES:
        rows = by_cell(run6, m)
        rows.update(by_cell(over, m))
        arms.append((m, rows, f"{a.sindy} + {a.sindy_override}"))
    arms.append(("pipeline (run 6)", by_cell(run6, "pipeline"), str(a.sindy)))
    return arms


def _f(v, fmt="{:.2f}"):
    return "-" if v is None else fmt.format(v)


def arm_stats(rows, classify=classify_p8):
    cls = {k: classify(r) for k, r in rows.items()}
    c = Counter(cls.values())
    rt = [float(r["runtime"]) for r in rows.values() if r.get("runtime") is not None]
    cv = [float(r["cover90"]) for r in rows.values() if r.get("cover90") is not None]
    wcv = [float(r["w_cover90"]) for r in rows.values() if r.get("w_cover90") is not None]
    return dict(cls=cls, count=c, n=len(rows), missing=len(P8_CELLS) - len(rows),
                fs=sum(bool(r.get("factor_set")) for r in rows.values()),
                so=sum(bool(r.get("struct_ok")) for r in rows.values()),
                rt_med=statistics.median(rt) if rt else None, rt_tot=sum(rt) if rt else None,
                cover=(statistics.mean(cv), len(cv)) if cv else None,
                wcover=(statistics.mean(wcv), len(wcv)) if wcv else None)


def p8_tables(arms, classify=classify_p8):
    L = []
    stats = {name: (None if rows is None else arm_stats(rows, classify)) for name, rows, _ in arms}
    hdr = ("| arm | n | " + " | ".join(CLASSES) + " | right+equiv | factor_set | struct_ok | coef cover90 (n) "
           "| weight cover90 (n) | runtime median s | runtime total s |")
    L += ["## Totals over the 30 P8 inputs", "", hdr, "|---" * (len(CLASSES) + 9) + "|"]
    for name, rows, _ in arms:
        s = stats[name]
        if s is None:
            L.append(f"| {name} | pending | " + " | ".join(["-"] * (len(CLASSES) + 8)) + " |")
            continue
        c = s["count"]
        n = f"{s['n']}/30" + (f" ({s['missing']} missing)" if s["missing"] else "")
        cov = "-" if s["cover"] is None else f"{s['cover'][0]:.2f} ({s['cover'][1]})"
        wcov = "-" if s["wcover"] is None else f"{s['wcover'][0]:.2f} ({s['wcover'][1]})"
        L.append(f"| {name} | {n} | " + " | ".join(str(c[k]) for k in CLASSES)
                 + f" | {c['right'] + c['equivalent']} | {s['fs']} | {s['so']} | {cov} | {wcov} | "
                 f"{_f(s['rt_med'], '{:.1f}')} | {_f(s['rt_tot'], '{:.0f}')} |")
    L += ["", "## Per design", "",
          "Cells: right+equivalent / abstain(-ok) / false-confident / wrong / CRASH (n).", "",
          "| arm | " + " | ".join(design_name(d) for d in DESIGNS) + " |", "|---" * (len(DESIGNS) + 1) + "|"]
    for name, rows, _ in arms:
        s = stats[name]
        if s is None:
            L.append(f"| {name} | " + " | ".join(["pending"] * len(DESIGNS)) + " |")
            continue
        cells = []
        for sm, nz in DESIGNS:
            c = Counter(v for k, v in s["cls"].items() if k[2] == sm and k[1] == nz)
            n = sum(c.values())
            cells.append(f"{c['right'] + c['equivalent']}/{c['abstain'] + c['abstain-ok']}/{c['false-confident']}/"
                         f"{c['wrong']}/{c['CRASH']} ({n})")
        L.append(f"| {name} | " + " | ".join(cells) + " |")
    present = [(n, r) for n, r, _ in arms if r is not None]
    L += ["", "## Per input", "", "| input | " + " | ".join(n for n, _ in present) + " |",
          "|---" * (len(present) + 1) + "|"]
    for k in P8_CELLS:
        L.append(f"| {k[0]} {k[2]} {k[1] * 100:g} % | "
                 + " | ".join(stats[n]["cls"].get(k, "missing") for n, _ in present) + " |")
    L += ["", "## False-confident and wrong rows", ""]
    for name, rows in present:
        bad = [k for k in P8_CELLS if stats[name]["cls"].get(k) in ("false-confident", "wrong", "CRASH")]
        if not bad:
            L.append(f"- {name}: none")
            continue
        if name in BASELINES:  # no labels, no intervals: the inputs only
            L.append(f"- {name} ({len(bad)}): " + ", ".join(f"{k[0]} {k[2]} {k[1] * 100:g} %" for k in bad))
            continue
        L.append(f"- {name} ({len(bad)}):")
        for k in bad:
            r = rows[k]
            what = r.get("error") if stats[name]["cls"][k] == "CRASH" else "; ".join(r.get("factors") or []) or "-"
            L.append(f"  - {k[0]} {k[2]} {k[1] * 100:g} %: {stats[name]['cls'][k]}, label {r.get('label')}, "
                     f"cover90 {_f(r.get('cover90'))}: {what}")
    L += t96_p8(arms, stats)
    return L, stats


def t96_p8(arms, stats):
    """T96 (loop.GRID_SMOOTH_GOF) rows of the pipeline arm: rows carrying `smooth_gof` (benchmarks/rescore_t96.py)
    and the downgraded ones; plus the rows whose factors are right but whose label abstains."""
    rows = dict(arms[0][1] or {})
    if not any("smooth_gof" in r for r in rows.values()):
        return []
    L = ["", "## T96 smooth residual test (pipeline arm)", ""]
    sg = [(k, r) for k, r in sorted(rows.items(), key=lambda kv: P8_CELLS.index(kv[0])) if r.get("smooth_gof") is not None]
    L.append(f"Applied to {len(sg)} rows (real-valued grid rows labelled FIT-COMPATIBLE; complex fields and "
             "scattered rows are out of its scope, as in run_loop). Downgrade when log10 p < -3.")
    L += ["", "| input | smooth_gof log10 p | downgraded | class |", "|---|---|---|---|"]
    L += [f"| {k[0]} {k[2]} {k[1] * 100:g} % | {r['smooth_gof']:.3g} | {'yes' if r.get('t96_downgraded') else 'no'} | "
          f"{stats[arms[0][0]]['cls'][k]} |" for k, r in sg]
    dn = [k for k, r in rows.items() if r.get("t96_downgraded")]
    L += ["", f"Rows changed by T96: {', '.join(f'{k[0]} {k[2]} {k[1] * 100:g} %' for k in dn) or 'none'}."]
    rab = [k for k, r in rows.items() if r.get("factor_set") and r.get("label") in ("UNDECIDED", "ID-KER")]
    L += [f"Right factors but abstained (factor_set true, label abstains; counted as abstain above): "
          f"{', '.join(f'{k[0]} {k[2]} {k[1] * 100:g} %' for k in rab) or 'none'}."]
    return L


# ---------------------------------------------------------------- E13

E13_METHODS = ("pipeline", "core", "pdefind", "weak_sindy", "ensemble_sindy")


def classify_e13(row, m):
    """e13_summary.classify, with CRASH for rows labelled CRASH and "other" named "wrong"."""
    import e13_summary

    if row[m].get("label") == "CRASH":
        return "CRASH"
    c = e13_summary.classify(row, m)
    return "wrong" if c == "other" else c


def e13_classes(rows, cache=None):
    """{(family, seed, method): class}; cache: JSON file of classes keyed "family-seed-noise-method"
    plus the row's reported factors (an entry is reused only when the factors are unchanged)."""
    store = {}
    if cache and Path(cache).exists():
        store = json.loads(Path(cache).read_text(encoding="utf-8"))
    out, dirty = {}, False
    for r in rows:
        for m in E13_METHODS:
            if m not in r:
                continue
            key = f"{r['family']}-{r['seed']}-{r['noise']}-{m}"
            sig = [r[m].get("label"), r[m].get("factors")]
            hit = store.get(key)
            if hit is None or hit[1] != sig:
                hit = [classify_e13(r, m), sig]
                store[key], dirty = hit, True
            out[(r["family"], r["seed"], m)] = hit[0]
    if cache and dirty:
        Path(cache).write_text(json.dumps(store, indent=0), encoding="utf-8")
    return out


def e13_tables(rows, cls):
    fams = sorted({r["family"] for r in rows})
    seeds = sorted({r["seed"] for r in rows})
    L = [f"## E13 random PDEs ({len(rows)} draws, families {', '.join(fams)}, seeds {seeds}, "
         f"noise {sorted({r['noise'] for r in rows})})", "",
         "| method | n | " + " | ".join(CLASSES) + " | right+equiv | resolvable right |",
         "|---" * (len(CLASSES) + 4) + "|"]
    for m in E13_METHODS:
        sub = [r for r in rows if m in r]
        if not sub:
            continue
        c = Counter(cls[(r["family"], r["seed"], m)] for r in sub)
        res = [r for r in sub if r["all_ident"]]
        L.append(f"| {m} | {len(sub)} | " + " | ".join(str(c[k]) for k in CLASSES)
                 + f" | {c['right'] + c['equivalent']} | {sum(bool(r[m]['ok']) for r in res)}/{len(res)} |")
    L += ["", "Pipeline per family:", "", "| family | n | " + " | ".join(CLASSES) + " |",
          "|---" * (len(CLASSES) + 2) + "|"]
    for f in fams:
        sub = [r for r in rows if r["family"] == f and "pipeline" in r]
        c = Counter(cls[(r["family"], r["seed"], "pipeline")] for r in sub)
        L.append(f"| {f} | {len(sub)} | " + " | ".join(str(c[k]) for k in CLASSES) + " |")
    sg = [r for r in rows if r.get("pipeline", {}).get("smooth_gof") is not None]
    if sg:
        L += ["", "T96 smooth residual test (pipeline rows labelled FIT-COMPATIBLE on the real grid; downgrade when "
              "log10 p < -3):", "", "| draw | smooth_gof log10 p | downgraded | class |", "|---|---|---|---|"]
        L += [f"| {r['family']}-{r['seed']} | {r['pipeline']['smooth_gof']:.3g} | "
              f"{'yes' if r['pipeline'].get('t96_downgraded') else 'no'} | {cls[(r['family'], r['seed'], 'pipeline')]} |"
              for r in sg]
        dn = [f"{r['family']}-{r['seed']}" for r in sg if r["pipeline"].get("t96_downgraded")]
        L += ["", f"Rows changed by T96: {', '.join(dn) or 'none'}."]
    rab = [r for r in rows if "pipeline" in r and r["pipeline"].get("ok")
           and (r["pipeline"].get("label") in ("UNDECIDED",) or str(r["pipeline"].get("label")).startswith("ID-KER"))]
    L += ["", "Right factors but abstained (pipeline; e13_summary.classify checks `ok` first, so these count as "
          "right above although no law is claimed): "
          + (", ".join(f"{r['family']}-{r['seed']} ({r['pipeline']['label']}"
                       f"{', T96' if r['pipeline'].get('t96_downgraded') else ''})" for r in rab) or "none") + "."]
    eab = [r for r in rows if "pipeline" in r and not r["pipeline"].get("ok")
           and cls[(r["family"], r["seed"], "pipeline")] == "equivalent"
           and (r["pipeline"].get("label") == "UNDECIDED" or str(r["pipeline"].get("label")).startswith("ID-KER"))]
    L += ["", "Equivalent factors but abstained (pipeline; classify tests equivalence before the label, so these "
          "count as equivalent above although no law is claimed): "
          + (", ".join(f"{r['family']}-{r['seed']} ({r['pipeline']['label']}, "
                       f"{'resolvable' if r['all_ident'] else 'not resolvable'})" for r in eab) or "none") + "."]
    fc = [(r, m) for r in rows for m in ("pipeline", "core") if m in r
          and cls[(r["family"], r["seed"], m)] in ("false-confident", "wrong", "CRASH")]
    L += ["", "False-confident / wrong / CRASH (pipeline, core):", ""]
    L += [f"- {m} {r['family']}-{r['seed']}: {cls[(r['family'], r['seed'], m)]}, truth {r['truth']} -> "
          f"{r[m]['label']} {r[m]['factors']}" for r, m in fc] or ["- none"]
    return L


# ---------------------------------------------------------------- main

NOTES = [
    "## Notes", "",
    "- Not independent trials. All 30 P8 inputs are seed 0: within one seed the arms see the identical noisy "
    "input, and the designs of one case share the noise draw (same generator seed, different noise scale or "
    "sampling). Arm differences are paired comparisons on the same data; the 30 rows are 10 cases x 3 "
    "correlated designs, not 30 independent draws, so no binomial interval over 30 applies. The same holds "
    "for E13: every method runs on the same draw.",
    "- P8 classes come from benchmarks/micro.py outcome(); equivalent = same product polynomial as the truth "
    "(simulator.match), without the chi^2 half of e13_summary.equivalent. P8 rows carry no resolvability flag, "
    "so abstentions count as abstain, not abstain-ok.",
    "- SINDy methods have no labels (n/a), so every wrong SINDy answer is false-confident.",
    "- factor_set / struct_ok are the bench_e2e columns (metrics.score), shown for comparison with earlier "
    "tables. coef cover90 = fraction of true coefficients inside the 90 % intervals; weight cover90 = true "
    "weights inside the split layer's 90 % intervals (only where the truth has per-factor weights and a split "
    "was reported); means over the rows that have them.",
    "- Runtime = per-input wall time. Pipeline arms ran with several workers on a shared machine, so their wall "
    "times include contention; SINDy times are from run 6.",
]


def build(a):
    arms = load_arms(a)
    L = ["# P8 final report", "",
         "Cells: 10 synthetic cases x {" + ", ".join(design_name(d) for d in DESIGNS) + "}, seed 0 (30 inputs).", "",
         "Sources:", ""]
    L += [f"- {n}: {'pending' if r is None else f'{len(r)} rows'} ({src})" for n, r, src in arms]
    L.append("")
    body, _ = p8_tables(arms)
    L += body + [""]
    e13 = read_jsonl(a.e13)
    if e13 is None:
        L += ["## E13", "", f"{a.e13} not found.", ""]
    elif not a.no_e13:
        L += e13_tables(e13, e13_classes(e13, a.e13_cache)) + [""]
    L += NOTES
    return "\n".join(L) + "\n"


def parse(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--pipeline", type=Path, default=_default("p8_pipeline.jsonl"))
    ap.add_argument("--sindy", type=Path, default=_default("e2e_run6.jsonl"))
    ap.add_argument("--sindy-override", type=Path, default=_default("p8_sindy_schrodinger_cplxsigma.jsonl"))
    ap.add_argument("--ml", type=Path, default=None, help="pipeline + ML arm jsonl (may not exist yet)")
    ap.add_argument("--ml-same", default=None, help="the ML arm equals the pipeline arm; the reason (no rerun)")
    ap.add_argument("--e13", type=Path, default=_default("e13_v4.jsonl"))
    ap.add_argument("--e13-cache", type=Path, default=None, help="JSON cache of E13 classes")
    ap.add_argument("--no-e13", action="store_true", help="skip the E13 table")
    ap.add_argument("--out", type=Path, default=None, help="markdown output (default: stdout)")
    return ap.parse_args(argv)


def main(argv=None):
    a = parse(argv)
    md = build(a)
    if a.out:
        a.out.write_text(md, encoding="utf-8", newline="\n")
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stdout.write(md)


if __name__ == "__main__":
    main()
