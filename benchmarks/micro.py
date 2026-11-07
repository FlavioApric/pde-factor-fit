"""Targeted micro-benchmarks: at most MAX_INPUTS inputs per suite, each suite aimed at one open problem.

    .venv/Scripts/python.exe benchmarks/micro.py <suite> [--tag NAME] [--workers 4] [--methods pipeline]

Same inputs, method runner and scoring as bench_e2e (load_input / run_task / metrics.score), so a row
here equals the bench_e2e row for the same input. Output: benchmarks/out/micro/<suite>_<tag>.jsonl,
then a table per input against the reference: the run-6 row (benchmarks/out/e2e_run6.jsonl) when the
input is there, else the suite's previous run (--ref TAG). A fix is kept only when its suite improves
and the other suites do not regress (GOLD RULE: the suites mix the failing case with held-out ones).
"""
from __future__ import annotations

import argparse
import json
import sys
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "benchmarks"))

from bench_e2e import _run_pool  # noqa: E402

OUT = ROOT / "benchmarks" / "out" / "micro"
RUN6 = ROOT / "benchmarks" / "out" / "e2e_run6.jsonl"
MAX_INPUTS = 15

G, N2, N4 = "grid", 2000, 400
SUITES = {
    # outer-layer cost: the slowest run-7 inputs (refinement and split search) and a few cheap ones
    "speed": [("klein_gordon", 0.01, G, 0), ("klein_gordon", 0.05, G, 0), ("telegraph", 0.01, G, 0),
              ("telegraph", 0.05, G, 0), ("transport_plus_diffusion", 0.05, G, 0), ("wave", 0.01, G, 0),
              ("beam", 0.01, G, 0), ("heat", 0.01, N2, 0), ("klein_gordon", 0.01, N2, 0),
              ("telegraph", 0.01, N4, 0)],
    # conjugate pairs and complex factors: split after an adopted alternative, beam at 5 %
    "conjugate": [("beam", 0.05, G, 0), ("beam", 0.05, G, 2), ("beam", 0.001, G, 2), ("beam", 0.05, N2, 2),
                  ("beam", 0.05, N4, 0), ("beam", 0.05, N4, 1), ("beam", 0.05, N4, 2), ("schrodinger", 0.05, G, 0),
                  ("schrodinger", 0.01, N4, 1), ("damped_beam", 0.01, G, 0), ("two_pairs", 0.01, G, 0)],
    # held-out families (never used to tune): generality check for every fix
    "heldout": [("damped_beam", 0.01, G, 0), ("two_pairs", 0.01, G, 0), ("kg_drift", 0.01, G, 0),
                ("cubic_tau", 0.01, G, 0), ("ks_linear", 0.01, G, 0), ("damped_airy_drift", 0.01, G, 0),
                ("wave_heat", 0.01, G, 0), ("tpd_scaled", 0.01, G, 0), ("transport_fast", 0.01, G, 0),
                ("advdiff_flat", 0.01, G, 0), ("wave_lowk", 0.01, G, 0), ("damped_beam", 0.01, N4, 0),
                ("two_pairs", 0.01, N4, 0), ("cubic_tau", 0.01, N4, 0)],
    # repeated roots, shared kappa = 0 mode, small high-order terms (labels and supports)
    "edge": [("repeated_transport", 0.01, G, 0), ("repeated_transport", 0.05, G, 0),
             ("tpd_shared_kappa0", 0.01, G, 0), ("fifth_order", 0.01, G, 0), ("airy", 0.05, N4, 0),
             ("heat", 0.05, N4, 1), ("transport_plus_diffusion", 0.05, N4, 0)],
    # grid coefficient intervals (bootstrap of the refined estimator, T75): coverage against run 6, terms kept
    # by evidence not pruned; damped_beam 400 on more seeds (seed 0 is data-equivalent: the pair fits better)
    "intervals": [("heat", 0.05, G, 0), ("transport_plus_diffusion", 0.01, G, 0), ("klein_gordon", 0.01, G, 0),
                  ("telegraph", 0.05, G, 0), ("airy", 0.01, G, 0), ("schrodinger", 0.01, G, 0), ("wave", 0.05, G, 0),
                  ("beam", 0.01, G, 0), ("cubic_tau", 0.01, G, 0), ("kg_drift", 0.05, G, 0),
                  ("damped_airy_drift", 0.05, G, 0), ("ks_linear", 0.05, G, 0), ("damped_beam", 0.01, N4, 1),
                  ("damped_beam", 0.01, N4, 2)],
}
for _s, _v in SUITES.items():
    assert len(_v) <= MAX_INPUTS, _s


def _key(r):
    return (r["case"], float(r["noise"]), str(r["sampling"]), int(r["seed"]), r["method"])


ABSTAIN = {"UNDECIDED", "ID-KER", "MISFIT"}  # labels that make no identification claim


@lru_cache(maxsize=None)
def _repeated_root(case):
    """True when the true symbol has a repeated irreducible factor: then UNDECIDED is the only
    correct label (confluent model, OPF5B-T6) and no factor set counts as identified."""
    from pdefactor.symbols import factors
    from pdefactor.synthetic import any_case

    import sympy as sp

    P = sp.nsimplify(sp.expand(any_case(case).P), rational=True)  # floats: no factoring over Q(i)
    return any(m > 1 for _, m in factors(P))


def outcome(r):
    """right / abstain / false-confident / error. The `factor_set` column ignores the label; this one
    reads it: an answer is a claim only when the label is FIT-COMPATIBLE. Additive to the old column,
    so old tables stay comparable."""
    if r.get("error"):
        return "error"
    lab = r.get("label")
    if _repeated_root(r["case"]):
        return "right" if lab == "UNDECIDED" else ("abstain" if lab in ABSTAIN else "false-confident")
    if lab in ABSTAIN:
        return "abstain"
    return "right" if r.get("factor_set") else "false-confident"


def _rows(p):
    p = Path(p)
    if not p.exists():
        return {}
    return {_key(r): r for r in map(json.loads, filter(str.strip, p.read_text().splitlines()))}


def table(suite, tag, ref=None, methods=("pipeline",)):
    cur = _rows(OUT / f"{suite}_{tag}.jsonl")
    old = _rows(OUT / f"{suite}_{ref}.jsonl") if ref else {}
    r6 = _rows(RUN6)
    lines = ["| input | label | right | outcome | coef err | cover90 | time s | reference | ref right | ref outcome | "
             "ref cover90 | ref time |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    cv = lambda r_: "-" if r_ is None or r_.get("cover90") is None else f"{r_['cover90']:.2f}"
    tot = {"right": 0, "ref_right": 0, "t": 0.0, "rt": 0.0, "n": 0}
    oc, roc = {}, {}
    for c, nz, s, sd in SUITES[suite]:
        for m in methods:
            k = (c, float(nz), str(s), int(sd), m)
            r = cur.get(k)
            if r is None:
                continue
            o, src = (old[k], ref) if k in old else ((r6[k], "run6") if k in r6 else (None, "-"))
            ok = bool(r.get("factor_set"))
            ce = r.get("coef_err")
            out_, rout = outcome(r), (None if o is None else outcome(o))
            oc[out_] = oc.get(out_, 0) + 1
            if rout:
                roc[rout] = roc.get(rout, 0) + 1
            lines.append(f"| {c} {nz:g} {s} s{sd} | {r.get('label')} | {'yes' if ok else 'NO'} | {out_} | "
                         f"{'-' if ce is None else f'{ce:.2g}'} | {cv(r)} | {r.get('runtime', 0):.0f} | {src} | "
                         f"{'-' if o is None else ('yes' if o.get('factor_set') else 'NO')} | {rout or '-'} | {cv(o)} | "
                         f"{'-' if o is None else f'{o.get('runtime', 0):.0f}'} |")
            tot["n"] += 1
            tot["right"] += ok
            tot["t"] += r.get("runtime", 0)
            if o is not None:
                tot["ref_right"] += bool(o.get("factor_set"))
                tot["rt"] += o.get("runtime", 0)
    lines.append(f"\n{suite} [{tag}]: right {tot['right']}/{tot['n']} (reference {tot['ref_right']}); "
                 f"total time {tot['t']:.0f} s (reference {tot['rt']:.0f} s)\n"
                 f"outcomes {dict(sorted(oc.items()))} (reference {dict(sorted(roc.items()))})")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("suite", choices=sorted(SUITES))
    ap.add_argument("--tag", default="cur")
    ap.add_argument("--ref")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--methods", nargs="*", default=["pipeline"])
    ap.add_argument("--report", action="store_true", help="only print the table of an existing run")
    ap.add_argument("--sampling", nargs="*", help="run only these samplings (grid, 400, 2000)")
    a = ap.parse_args()
    out = OUT / f"{a.suite}_{a.tag}.jsonl"
    if not a.report:
        OUT.mkdir(parents=True, exist_ok=True)
        done = set(_rows(out))
        todo = [((c, nz, s, sd), tuple(m for m in a.methods if (c, float(nz), str(s), sd, m) not in done))
                for c, nz, s, sd in SUITES[a.suite] if not a.sampling or str(s) in a.sampling]
        todo = [(tk, ms) for tk, ms in todo if ms]
        print(f"{a.suite}: {len(todo)} inputs to run", flush=True)
        _run_pool(todo, out, a.workers)
    print(table(a.suite, a.tag, a.ref, tuple(a.methods)), flush=True)


if __name__ == "__main__":
    main()
