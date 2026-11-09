#!/usr/bin/env python3
"""Checks on the flat manuscripts paper/structure_A.tex and paper/structure_B.tex.

    python code/tools/paper_checks.py

1. hygiene: no internal project vocabulary (ledger labels, phase names, file names of the research repository) in the manuscripts;
2. notation: every notation macro defined in the macro block is listed in the notation table of the same file.
Part of pde-factor-fit (c) 2026 Flavio Pricoco, MIT.
"""
import re
import sys
from pathlib import Path

PAPERS = [Path(__file__).resolve().parents[2] / "paper" / f for f in ("structure_A.tex", "structure_B.tex")]
PATTERN = re.compile(r"\b(FASI|HANDOFF|ledger|Phase ?[0-9]|PHASE|T[0-9]{1,3}\b|C3-|C12-|P[0-9]-T|S4ID|S4T|OPF|OPA-|R2-T|II-T|AI agent|Lean 4|no ML rule|ProblemaBase|PDEFactorML|TODO|XXX)")
SKIP = {"R", "C", "Z", "dd", "Id", "abs", "norm", "ip", "lab", "roleinalg", "inbrief", "Normal", "E", "gcdop", "spn", "rank", "diag", "tr", "Hs", "noise"}


def block(text, name):
    m = re.search(r"% ---- begin [^\n]*" + re.escape(name) + r"\n(.*?)\n% ---- end [^\n]*" + re.escape(name), text, re.S)
    return m.group(1) if m else ""


def main():
    bad = 0
    for p in PAPERS:
        t = p.read_text(encoding="utf-8")
        hits = [f"{p.name}:{i}: {l.strip()[:100]}" for i, l in enumerate(t.split("\n"), 1) if PATTERN.search(l) and "usepackage" not in l and not l.lstrip().startswith("%")]
        if hits:
            bad += 1
            print("internal vocabulary in", p.name, *hits[:10], sep="\n  ")
        macros, table = block(t, "macros.tex"), block(t, "notation.tex")
        defined = re.findall(r"\\(?:newcommand|DeclareMathOperator)\{\\(\w+)\}", macros)
        missing = [m for m in defined if m not in SKIP and f"\\{m}" not in table]
        if missing:
            bad += 1
            print(p.name, "notation macros not listed in the notation table:", ", ".join(missing))
        print(f"{p.name}: hygiene {'clean' if not hits else 'FAILED'}, notation {len(defined)} macros {'all listed' if not missing else 'INCOMPLETE'}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
