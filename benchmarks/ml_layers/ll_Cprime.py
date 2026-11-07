"""Controller C' data (P7): oracle sweep of single actions on off-failure cases, V1 as the trigger.

C' is NOT built here. This measures the ceiling: for each case, every action of the declared space is
run once from today's default (full settings, bootstrap as the corpus, cap 1200 s per run), and a case
counts as rescued when at least one action gives a right or equivalent answer where the off run did not.

Action space:
  - the 13 remedies of learned/controller.REMEDIES (RunConfig deltas from DEFAULT; one that changes
    nothing on this case, e.g. more_samples on a single noisy grid, is recorded as NA and not run);
  - skip_grow (grow=False), skip_recurse (recurse=False);
  - main's switches that are off by default: grow_past (loop.GROW_PAST, P3) and epgp_reinterp
    (loop.EPGP_REINTERP, P4; it acts only with raw scattered data, so NA on grids).

Rows are ll_corpus rows with learned = "act:<name>" (same truth scoring, same features).

  python ll_Cprime.py run --cases out/ll_Cprime_cases.json --out out/ll_Cprime.jsonl --workers 4
  python ll_Cprime.py report --sweep out/ll_Cprime.jsonl --off out/ll_V.jsonl --v1 <v1_gate json>
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

EXTRA = ("skip_grow", "skip_recurse", "grow_past", "epgp_reinterp")
GOOD = ("right", "equivalent")


def actions():
    from pdefactor.learned.controller import REMEDIES

    return list(REMEDIES) + list(EXTRA)


class NotApplicable(Exception):
    pass


def run_action(name, inp):
    """run_loop under one action on a corpus input (already deep-copied by ll_corpus.run_one)."""
    from pdefactor import loop
    from pdefactor.learned import controller as C
    from pdefactor.learned.runconfig import DEFAULT, RunConfig

    if inp["raw"] is not None:
        raise NotApplicable("scattered cases are not in this sweep (grid-heavy by design)")
    case = C.Case(list(inp["samples"]), np.ones(1), inp["t"], inp["x"], inp["sigma"], None, None, 1, inp["bootstrap"])
    if name in C.REMEDIES:
        cfg = C._delta(name, DEFAULT, case)
        if cfg is None:
            raise NotApplicable(f"{name} changes nothing on this case")
    elif name == "skip_grow":
        cfg = RunConfig(grow=False)
    elif name == "skip_recurse":
        cfg = RunConfig(recurse=False)
    elif name == "grow_past":
        loop.GROW_PAST = True  # this child process only
        cfg = DEFAULT
    elif name == "epgp_reinterp":
        raise NotApplicable("EPGP re-interpolation acts on raw scattered data only")
    elif name == "off":
        cfg = DEFAULT
    else:
        raise KeyError(name)
    return C.run_config(case, cfg)


def cmd_run(a):
    import ll_corpus as LC

    cases = json.loads(Path(a.cases).read_text())
    done = LC.done_keys(a.out)
    acts = actions() if not a.actions else a.actions
    tasks = [(c["corpus"], c["family"], c["seed"], tuple(c["design"]), f"act:{n}") for c in cases for n in acts]
    tasks = [t for t in tasks if (t[0], t[1], t[2], tuple(t[3]), t[4]) not in done]
    print(f"{len(tasks)} runs, {a.workers} workers", flush=True)
    LC.run_all(tasks, a.out, a.workers, a.cap)


def _key(r):
    return (r["corpus"], r["family"], r["seed"], json.dumps(r["design"]))


def cmd_report(a):
    sweep = [json.loads(l) for p in a.sweep for l in open(p)]
    off = {}
    for p in a.off:
        for l in open(p):
            r = json.loads(l)
            if r.get("learned") == "off":
                off[_key(r)] = r
    flags = {}
    if a.v1:
        R = json.loads(Path(a.v1).read_text())
        for r in R.get("downgrade", {}).get("rows", []):
            flags[(r["corpus"], r["family"], r["seed"], json.dumps(r["design"]))] = r["flag"]
    by = {}
    for r in sweep:
        if "NotApplicable" in str(r.get("error", "")):
            continue
        by.setdefault(_key(r), {})[r["learned"][4:]] = r
    L = ["# C' oracle sweep (single actions from today's default; full settings; cap 1200 s per run)", ""]
    L += ["| case | off | V1 flag | actions run | rescuing actions | crash / timeout |", "|---|---|---|---|---|---|"]
    n_fail = n_resc = n_resc_trig = n_trig = 0
    per_act = {}
    for k, acts in sorted(by.items(), key=lambda kv: str(kv[0])):
        o = off.get(k)
        oc = o.get("category") if o else "?"
        if o and o.get("label") in ("TIMEOUT", "CRASH"):
            oc = o["label"]
        fl = flags.get(k)
        resc = sorted(n for n, r in acts.items() if r.get("category") in GOOD)
        bad = sum(r.get("label") in ("TIMEOUT", "CRASH") for r in acts.values())
        fail = oc not in GOOD and oc != "abstain-ok"
        if fail:
            n_fail += 1
            n_resc += bool(resc)
            n_trig += bool(fl)
            n_resc_trig += bool(resc) and bool(fl)
            for n in resc:
                per_act[n] = per_act.get(n, 0) + 1
        L.append(f"| {k[1]} s{k[2]} {json.loads(k[3])} | {oc} | {fl} | {len(acts)} | {', '.join(resc) or '-'} | {bad} |")
    L += ["", f"- off failures in the sweep: {n_fail}",
          f"- oracle ceiling (any action rescues): {n_resc}/{n_fail}" + (f" = {n_resc / n_fail:.0%}" if n_fail else ""),
          f"- V1 triggers (flag at alpha 0.05, held-out family): {n_trig}/{n_fail} failures",
          f"- ceiling with V1 as the trigger (flagged and rescued): {n_resc_trig}/{n_fail}"
          + (f" = {n_resc_trig / n_fail:.0%}" if n_fail else ""),
          "- rescues per action: " + (", ".join(f"{n} {c}" for n, c in sorted(per_act.items(), key=lambda kv: -kv[1])) or "none")]
    if flags:
        clean_ok = [k for k, fl in flags.items() if off.get(k, {}).get("category") in GOOD + ("abstain-ok",)]
        fa = sum(flags[k] for k in clean_ok)
        L += [f"- V1 false alarms on clean cases the off run gets right (or abstains correctly): {fa}/{len(clean_ok)}"]
    md = "\n".join(L) + "\n"
    if a.md:
        Path(a.md).write_text(md, encoding="utf-8")
    print(md)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("--cases", required=True, help="json list of {corpus, family, seed, design}")
    r.add_argument("--out", required=True)
    r.add_argument("--actions", nargs="*", default=None)
    r.add_argument("--workers", type=int, default=4)
    r.add_argument("--cap", type=float, default=1200.0)
    p = sub.add_parser("report")
    p.add_argument("--sweep", nargs="+", required=True)
    p.add_argument("--off", nargs="+", required=True)
    p.add_argument("--v1", default=None, help="ll_v1 results json (per-row LOFO flags)")
    p.add_argument("--md", default=None)
    a = ap.parse_args()
    {"run": cmd_run, "report": cmd_report}[a.cmd](a)


if __name__ == "__main__":
    main()
