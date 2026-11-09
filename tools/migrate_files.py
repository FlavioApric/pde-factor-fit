#!/usr/bin/env python3
"""Copy every old-repository file that has no counterpart yet into the right branch and folder of this repository.

    python tools/import_old.py --old-graph graphs/graph_old.json --new-graph graphs/graph_new.json \
        --old-repo /path/to/old --new-repo /path/to/new [--dry-run]

The destination rules are in `dest_for()`. Text files are stored with LF line endings; local Windows user paths and e-mail addresses
are replaced by placeholders. Excluded types (junk, logs, backups, caches, toolchain, private notes) are never copied.

Part of pde-factor-fit (c) 2026 Flavio Pricoco, MIT.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import PurePosixPath

sys.path.insert(0, str(PurePosixPath(__file__).parent))
from build_graph import SANITIZE, TEXT_EXT  # noqa: E402

EXCLUDE = {"junk", "log", "backup", "cache", "toolchain", "private", "dir"}
CODE_EXT = {".py", ".out", ".pkl", ".json", ".jsonl", ".csv", ".sh", ".bat", ".pt", ".npz", ".png", ".tsv"}
DATA_MAX = 2_000_000
LL = re.compile(r"(^|/)ll_|(^|/)fastrun\.py$|(^|/)slots\.py$")


def split(p):
    return p.split("/")


def dest_for(p: str, ext: str):
    """old path -> (branch, new path) or None."""
    parts = split(p)
    name = parts[-1]
    # ---------------------------------------------------------------- ProblemaBase (theory) -> analytical
    if parts[0] == "ProblemaBase":
        sub = parts[1] if len(parts) > 1 else ""
        if sub in ("work", "research") and len(parts) >= 4:
            sess = parts[2]
            if ext in CODE_EXT or ext in {".tex"} and "/sympy/" in p:
                base = f"verification/{sess}/{name}" if sub == "work" else f"verification/research/{sess}/{name}"
                return "analytical", base
            return "analytical", f"claude/archive/{sub}/{sess}/{'/'.join(parts[3:])}"
        if sub == "work" or sub == "research":
            return "analytical", f"claude/archive/{sub}/{'/'.join(parts[2:])}"
        if sub == "FASI_ALL":
            return "analytical", "paper/analytical_complete/" + "/".join(parts[2:])
        if sub == "FASI05":
            return "analytical", "paper/analytical_phases05/" + "/".join(parts[2:])
        if sub == "PAPER":
            return "analytical", "paper/analytical_original/" + "/".join(parts[2:])
        if sub == "PAPER_EXPLAINED":
            return "analytical", "paper/analytical_explained/" + "/".join(parts[2:])
        if sub == "NOTE_ML":
            return "ml-layers", "paper/ml_pipeline_note/" + "/".join(parts[2:])
        if sub == "VOLUMES":
            return "analytical", "claude/archive/origin/VOLUMES/" + "/".join(parts[2:])
        if sub == "claims":
            return "analytical", "claude/archive/claims/" + "/".join(parts[2:])
        if sub == "inbox":
            return "analytical", "claude/archive/inbox/" + "/".join(parts[2:])
        if sub == "PBLean":
            return "analytical", "proofs/lean_project/" + "/".join(parts[2:])
        if sub == "PBLean_src":
            return "analytical", "proofs/lean/" + "/".join(parts[2:])
        if len(parts) == 2:
            if ext == ".py":
                return "analytical", f"verification/{name}"
            return "analytical", f"claude/archive/ProblemaBase/{name}"
        return "analytical", "claude/archive/ProblemaBase/" + "/".join(parts[1:])
    if parts[0] == "example_output":
        return "main", "benchmarks/final_report_example/" + "/".join(parts[1:])
    if parts[0] in (".github", "paper") or p in ("README.md", ".gitignore"):
        return None  # already present (possibly edited)
    if p == "piano di ricerca.md":
        return "analytical", "claude/archive/origin/piano_di_ricerca.md"
    # ---------------------------------------------------------------- PDEFactorML-S-INTERP -> ml-layers variant
    if parts[0] == "PDEFactorML-S-INTERP":
        rest = "/".join(parts[1:])
        if parts[1] == "sessions" and ext in {".md", ".txt"}:
            return "ml-layers", "claude/archive/sessions/s_interp_variant/" + "/".join(parts[2:])
        return "ml-layers", "variants/s_interp/" + rest
    # ---------------------------------------------------------------- PDEFactorML
    if parts[0] == "PDEFactorML":
        sub = parts[1] if len(parts) > 1 else ""
        rest = "/".join(parts[2:])
        if len(parts) == 2:
            if ext == ".md":
                return "main", f"claude/archive/pipeline/{name}"
            if name == "pyproject.toml" or name == ".gitignore":
                return None
            return "main", f"claude/archive/pipeline/{name}"
        if sub == "EXPLAINED":
            if name.startswith("ml_layers"):
                return "ml-layers", "paper/ml_explained/" + "/".join(parts[2:])
            return "main", "paper/explained/" + "/".join(parts[2:])
        if sub == "analysis":
            if len(parts) == 3 and ext == ".md":
                return "main", "claude/archive/pipeline/analysis/" + name
            if parts[2] == "exp":
                tail = "/".join(parts[3:])
                if LL.search(p) or parts[3:4] == ["models"]:
                    if ext in {".py", ".json"} and parts[3:4] != ["out"]:
                        return "ml-layers", "benchmarks/ml_layers/" + ("models/" + name if parts[3:4] == ["models"] else name)
                    return "ml-layers", "benchmarks/ml_layers/results/" + name
                if parts[3:4] == ["out"]:
                    return "main", "benchmarks/results/analysis_exp/" + "/".join(parts[4:])
                return "main", "analysis/exp/" + tail
            return "main", "claude/archive/pipeline/analysis/" + "/".join(parts[2:])
        if sub == "benchmarks":
            return "main", "benchmarks/" + rest
        if sub == "sessions":
            sess = parts[2]
            ml = sess in {"LEARNED", "S-PHASE4-ML"}
            br = "ml-layers" if ml else "main"
            if ext in {".md", ".txt"}:
                return br, f"claude/archive/sessions/{sess}/" + "/".join(parts[3:])
            if ml:
                return br, f"benchmarks/ml_layers/sessions/{sess}/" + "/".join(parts[3:])
            return br, f"benchmarks/sessions/{sess}/" + "/".join(parts[3:])
        if sub in ("src", "tests"):
            return None  # present in main / ml-layers by construction; version differences are intended
        return "main", "claude/archive/pipeline/" + rest
    return None


def sanitize_bytes(b: bytes, ext: str) -> bytes:
    if ext in TEXT_EXT and ext not in (".err", ".log"):
        s = b.decode("utf-8", "replace").lstrip("﻿").replace("\r\n", "\n").replace("\r", "\n")
        for pat, rep in SANITIZE:
            s = pat.sub(rep, s)
        return s.encode("utf-8")
    return b


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--old-graph", required=True)
    ap.add_argument("--new-graph", required=True)
    ap.add_argument("--old-repo", required=True)
    ap.add_argument("--new-repo", required=True)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--only", help="regex on old path")
    ap.add_argument("--message", help="commit message")
    a = ap.parse_args()
    old = json.load(open(a.old_graph, encoding="utf-8"))
    new = json.load(open(a.new_graph, encoding="utf-8"))
    new_paths = {n["id"] for n in new["nodes"]}
    have = {h for n in new["nodes"] if n["type"] != "dir" for h in n.get("hashes", [n["hash"]])}
    todo = defaultdict(list)
    unmapped, skipped = [], Counter()
    for n in old["nodes"]:
        if n["type"] in EXCLUDE:
            continue
        if any(h in have for h in n.get("hashes", [n["hash"]])) or n["id"] in new_paths:
            continue
        p, ext = n["id"], PurePosixPath(n["id"]).suffix.lower()
        if n["type"] == "pdf" and False:
            continue
        if n["type"] == "data" and n["size"] > DATA_MAX:
            skipped["data>2MB"] += 1
            continue
        if a.only and not re.search(a.only, p):
            continue
        d = dest_for(p, ext)
        if d is None:
            unmapped.append(p)
            continue
        todo[d[0]].append((p, d[1], n["sha"], ext))
    for br, items in todo.items():
        seen = Counter()
        for i, (p, dst, sha, ext) in enumerate(items):
            seen[dst] += 1
            if seen[dst] > 1:  # basename clash inside one folder: keep the parent folder in the name
                par = split(p)[-2]
                items[i] = (p, str(PurePosixPath(dst).with_name(f"{par}__{PurePosixPath(dst).name}")), sha, ext)
    print({b: len(v) for b, v in todo.items()}, "unmapped", len(unmapped), dict(skipped))
    for p in unmapped[:40]:
        print("  unmapped:", p)
    if a.dry_run:
        return 0
    for br, items in todo.items():
        subprocess.run(["git", "-C", a.new_repo, "checkout", "-q", br], check=True)
        for p, dst, sha, ext in items:
            b = subprocess.run(["git", "-C", a.old_repo, "cat-file", "blob", sha], capture_output=True, check=True).stdout
            out = PurePosixPath(a.new_repo) / dst
            import os
            os.makedirs(out.parent, exist_ok=True)
            open(out, "wb").write(sanitize_bytes(b, ext))
        subprocess.run(["git", "-C", a.new_repo, "add", "-f", "-A"], check=True)
        print(br, "staged", len(items))
        msg = (a.message or "Add the missing files from the research repository") + (
            "\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01QKcsJ3ETQYUT5vMFsX8HBi")
        subprocess.run(["git", "-C", a.new_repo, "commit", "-q", "-m", msg], check=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
