#!/usr/bin/env python3
"""Compare the graph of the old repository with the graph of the new one and write INVENTORY.md.

    python tools/compare_graphs.py --old /tmp/graphs/graph_old.json --new /tmp/graphs/graph_new.json --out INVENTORY.md --csv inventory.csv

Every old file is matched to the new repository (1) by normalised content hash (identical, possibly moved), (2) by file name with
mostly the same lines (modified: e.g. author name, paths), else it is *missing*. Missing files are *expected* (build junk, logs, backups,
caches, toolchain binaries, private notes, session reports and plans) or a *real gap* (papers, code, tests, benchmarks, Lean, theory documents,
small data). The exit code is 1 while a real gap exists.

Part of pde-factor-fit (c) 2026 Flavio Pricoco, MIT.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import PurePosixPath

DATA_MAX = 2_000_000
EXPECTED_REASON = {
    "junk": "LaTeX build / Python cache files",
    "log": "raw run logs",
    "backup": "superseded backup copies",
    "cache": "regenerable cache (>100 MB; scripts that make it are kept)",
    "toolchain": "Lean toolchain installer binaries",
    "private": "private notes (never published)",
    "report-plan": "session report / plan / audit document (accepted as expected; archived when present)",
}


def load(p):
    return json.loads(open(p, encoding="utf-8").read())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--old", required=True)
    ap.add_argument("--new", required=True)
    ap.add_argument("--out", default="INVENTORY.md")
    ap.add_argument("--csv", default="inventory.csv")
    ap.add_argument("--list-gaps", type=int, default=0, help="print N real gaps")
    ap.add_argument("--superseded", help="CSV 'regex,reason': old files merged into another document (a coverage check must back each rule)")
    a = ap.parse_args()
    old, new = load(a.old), load(a.new)
    onodes = [n for n in old["nodes"] if n["type"] != "dir"]
    nnodes = [n for n in new["nodes"] if n["type"] != "dir"]
    by_hash = defaultdict(list)
    by_name = defaultdict(list)
    for n in nnodes:
        for h in n.get("hashes", [n["hash"]]):
            by_hash[h].append(n["id"])
        by_name[PurePosixPath(n["id"]).name].append(n)
    old_stems = {(str(PurePosixPath(n["id"]).parent), PurePosixPath(n["id"]).stem) for n in onodes if n["id"].endswith(".tex")}

    import re
    sup = []
    if a.superseded:
        for line in open(a.superseded, encoding="utf-8"):
            line = line.strip()
            if line and not line.startswith("#"):
                rx, why = line.split(",", 1)
                sup.append((re.compile(rx), why))
    rows = []
    for n in onodes:
        p, t = n["id"], n["type"]
        status, dest = None, ""
        for h in n.get("hashes", [n["hash"]]):
            if h in by_hash:
                dests = by_hash[h]
                dest = p if p in dests else dests[0]
                status = "identical" if p in dests else "moved"
                break
        if status is None:
            same = by_name.get(PurePosixPath(p).name, [])
            if same and t not in ("pdf",):
                status, dest = "modified", same[0]["id"]
        if status is None:
            if t == "pdf":
                stem = (str(PurePosixPath(p).parent), PurePosixPath(p).stem)
                if stem in old_stems:
                    status, reason = "expected-missing", "PDF rebuilt from the included LaTeX source"
                else:
                    status, reason = "GAP", "PDF without source"
            elif t in EXPECTED_REASON:
                status, reason = "expected-missing", EXPECTED_REASON[t]
            elif t == "data" and n["size"] > DATA_MAX:
                status, reason = "expected-missing", "data file larger than 2 MB (regenerable)"
            else:
                status, reason = "GAP", f"{t} not found in the new repository"
            if status == "GAP":
                for rx, why in sup:
                    if rx.search(p):
                        status, reason = "superseded", why
                        break
            dest = reason
        rows.append((p, t, status, dest, n["size"]))

    cnt = Counter((t, s) for _, t, s, _, _ in rows)
    types = sorted({t for _, t, *_ in rows})
    gaps = [r for r in rows if r[2] == "GAP"]
    with open(a.csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["old_path", "type", "status", "new_path_or_reason", "bytes"])
        w.writerows(rows)

    # structural check: tex / py edges between matched files
    newedges = {(s, d) for s, d, k in new["edges"] if k in ("tex", "py")}
    pos = {p: d for p, t, s, d, _ in rows if s in ("identical", "moved", "modified")}
    lost = []
    for s, d, k in old["edges"]:
        if k in ("tex", "py") and s in pos and d in pos and (pos[s], pos[d]) not in newedges:
            lost.append((s, d, k))

    L = ["# INVENTORY: old repository vs this repository", "",
         "Generated by `tools/compare_graphs.py` from `graphs/graph_old.json` (union of the 9 old branches) and `graphs/graph_new.json` (the 4 branches of this repository).", "",
         f"Old files: {len(rows)}. Matched: {sum(1 for r in rows if r[2] in ('identical','moved','modified'))}. "
         f"Expected missing: {sum(1 for r in rows if r[2]=='expected-missing')}. Merged into another document (superseded): {sum(1 for r in rows if r[2]=='superseded')}. **Real gaps: {len(gaps)}.**", "",
         "## By type", "", "| type | old | identical | moved | modified | expected missing | superseded | real gap |", "|---|---|---|---|---|---|---|---|"]
    for t in types:
        tot = sum(c for (tt, s), c in cnt.items() if tt == t)
        L.append(f"| {t} | {tot} | {cnt[(t,'identical')]} | {cnt[(t,'moved')]} | {cnt[(t,'modified')]} | {cnt[(t,'expected-missing')]} | {cnt[(t,'superseded')]} | {cnt[(t,'GAP')]} |")
    L += ["", "## Why files are excluded", "", "| reason | files |", "|---|---|"]
    rc = Counter(d for p, t, s, d, _ in rows if s in ("expected-missing", "superseded"))
    for r, c in rc.most_common():
        L.append(f"| {r} | {c} |")
    L += ["", "## Real gaps", ""]
    if not gaps:
        L.append("None: every paper, code, test, benchmark, Lean file, theory document and small data file of the old repository is present.")
    else:
        g = defaultdict(list)
        for p, t, s, d, z in gaps:
            g["/".join(p.split("/")[:3])].append(p)
        L += ["| folder | files |", "|---|---|"] + [f"| `{k}` | {len(v)} |" for k, v in sorted(g.items(), key=lambda kv: -len(kv[1]))]
    L += ["", "## Structure", "",
          f"Old import / include links between matched files: {sum(1 for s,d,k in old['edges'] if k in ('tex','py') and s in pos and d in pos)}; "
          f"not present in the new graph: {len(lost)} (links that cross a moved or merged file are expected to differ).", ""]
    open(a.out, "w", encoding="utf-8").write("\n".join(L))
    print(f"old={len(rows)} matched={sum(1 for r in rows if r[2] in ('identical','moved','modified'))} "
          f"expected_missing={sum(1 for r in rows if r[2]=='expected-missing')} superseded={sum(1 for r in rows if r[2]=='superseded')} GAPS={len(gaps)}")
    for r in gaps[: a.list_gaps]:
        print("  GAP", r[1], r[0], r[4])
    return 1 if gaps else 0


if __name__ == "__main__":
    sys.exit(main())
