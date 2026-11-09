#!/usr/bin/env python3
"""Build a file/dependency graph of a set of git refs (one logical repository).

    python tools/build_graph.py --name new --repo /path/to/repo --refs main analytical ml-layers model-expansion --out graphs
    python tools/build_graph.py --name old --repo /path/to/old --refs origin/ml origin/other ... --out graphs

Nodes   every file (type: paper-tex, pdf, python-src, test, benchmark-script, lean, doc, data, log, junk, other)
Edges   contain (dir -> file), tex (\\input, \\include, \\bibliography, \\includegraphics), py (import),
        ref (a document or script mentions another file by path)
Output  <out>/graph_<name>.json, <out>/graph_<name>.mmd (directory-level Mermaid), <out>/graph_<name>.html (interactive)

Part of pde-factor-fit (c) 2026 Flavio Pricoco, MIT.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path, PurePosixPath

TEXT_EXT = {".md", ".tex", ".py", ".bib", ".txt", ".json", ".jsonl", ".csv", ".lean", ".toml", ".yml", ".yaml", ".cff", ".sh",
            ".out", ".sty", ".cls", ".bst", ".gitignore", ".bat", ".cfg", ".ini", ".graphifyignore", ".err", ".log", ".tsv"}
MAX_TEXT = 4_000_000
SANITIZE = [(re.compile(r"C:/Users/<user>\b"), r"C:\\Users\\<user>"),
            (re.compile(r"[A-Za-z0-9._-]+@(?:gmail|outlook|hotmail)\.com"), "<email>")]
PRIVATE_PAT = re.compile(r"do not read", re.I)
BACKUP_PAT = re.compile(r"(_backup|_old\b|_pre[A-Z][A-Za-z0-9]*_backup|\.v1\.|_v[0-9]_backup|backup)", re.I)
REPORT_PAT = re.compile(r"(^|/)(PLAN|REPORT|HANDOFF|HANDOFF_FORK|SESSIONS|SESSIONS-F8|STATE|RIPRESA|BOARD|COORDINAMENTO|CHECK_REQUEST[_0-9]*|AUDIT[^/]*|"
                        r"open_questions|VERDETTO|RECEPIMENTO|SPEEDUP|SYNC|RESEARCH|central|TRIAGE[^/]*|CHIUSURA[^/]*|FINAL_REPORT[^/]*|CHANGELOG|PROTOCOLLO|tiers)\.md$|/inbox/")


def sh(repo, *args, text=True):
    r = subprocess.run(["git", "-C", repo, *args], capture_output=True)
    if r.returncode:
        raise RuntimeError(r.stderr.decode()[:300])
    return r.stdout.decode("utf-8", "replace") if text else r.stdout


def list_refs(repo, refs):
    files = {}
    for ref in refs:
        out = sh(repo, "ls-tree", "-r", "-l", "-z", ref, text=False).split(b"\0")
        for ent in out:
            if not ent:
                continue
            meta, path = ent.split(b"\t", 1)
            mode, typ, sha, size = meta.decode().split(None, 3)
            if typ != "blob":
                continue
            path = path.decode("utf-8", "replace").rstrip("/")
            d = files.setdefault(path, {"variants": {}, "refs": []})
            d["variants"][sha] = int(size) if size.strip() != "-" else 0
            d["refs"].append(ref)
    return files


def classify(path: str, size: int, head: bytes = b"") -> str:
    p = PurePosixPath(path)
    name, ext = p.name, p.suffix.lower()
    low = path.lower()
    if PRIVATE_PAT.search(name):
        return "private"
    if "_tools/elan" in low:
        return "toolchain"
    if ext in {".aux", ".fls", ".fdb_latexmk", ".toc", ".blg", ".bbl", ".synctex.gz", ".pyc"} or name.endswith(".egg-info") or "egg-info/" in low or "__pycache__" in low:
        return "junk"
    if ext == ".out" and head.startswith(b"\\BOOKMARK"):
        return "junk"
    if ext in {".log", ".err"}:
        return "log"
    if BACKUP_PAT.search(name) or "/pdf/paper_old" in low:
        return "backup"
    if ("code/experiments/out/" in low or "/cache/" in low) and ext in {".npz", ".pkl", ".pt"}:
        return "cache"
    if ext == ".pdf":
        return "pdf"
    if ext in {".tex", ".bib", ".sty", ".cls", ".bst"}:
        return "paper-tex"
    if ext == ".lean" or name in {"lakefile.toml", "lake-manifest.json", "lean-toolchain"}:
        return "lean"
    if ext == ".py":
        if "/tests/" in "/" + low or name.startswith("test_"):
            return "test"
        if "benchmarks/" in low or "/code/experiments/" in low or "/exp/" in low:
            return "benchmark-script"
        return "python-src"
    if ext == ".md":
        return "report-plan" if REPORT_PAT.search(path) else "doc"
    if ext in {".json", ".jsonl", ".csv", ".npz", ".pkl", ".png", ".txt", ".out", ".pt", ".tsv"}:
        return "data"
    return "other"


def norm_text(b: bytes) -> str:
    s = b.decode("utf-8", "replace").lstrip("\ufeff").replace("\r\n", "\n").replace("\r", "\n")
    for pat, rep in SANITIZE:
        s = pat.sub(rep, s)
    return "\n".join(x.rstrip() for x in s.split("\n")).rstrip("\n")


class Blobs:
    def __init__(self, repo):
        self.repo = repo
        self.cache = {}

    def get(self, sha):
        if sha not in self.cache:
            self.cache[sha] = sh(self.repo, "cat-file", "blob", sha, text=False)
        return self.cache[sha]


def content_hash(blobs: Blobs, sha: str, path: str, size: int) -> str:
    ext = PurePosixPath(path).suffix.lower()
    if ext in TEXT_EXT and size <= MAX_TEXT:
        return "t:" + hashlib.sha1(norm_text(blobs.get(sha)).encode()).hexdigest()
    return "b:" + sha


RX_TEX = re.compile(r"\\(?:input|include|inc|includegraphics(?:\[[^\]]*\])?|bibliography|externaldocument(?:\[[^\]]*\])?)\{([^}]+)\}")
RX_PYIMP = re.compile(r"^\s*(?:from\s+([\w.]+)\s+import|import\s+([\w., ]+))", re.M)
RX_PATH = re.compile(r"[\w./\\-]+\.(?:py|tex|md|json|jsonl|csv|pdf|bib|lean|out|txt|png|npz)\b")


def build(name, repo, refs, outdir):
    files = list_refs(repo, refs)
    blobs = Blobs(repo)
    paths = sorted(files)
    suffix = defaultdict(list)
    for p in paths:
        parts = p.split("/")
        for i in range(len(parts)):
            suffix["/".join(parts[i:])].append(p)
    base = defaultdict(list)
    for p in paths:
        base[PurePosixPath(p).name].append(p)

    def resolve(token, frm, exts=("",)):
        token = token.replace("\\", "/").lstrip("./")
        cands = []
        for e in exts:
            cands += suffix.get(token + e, [])
        if not cands:
            return None
        if len(cands) == 1:
            return cands[0]
        d = str(PurePosixPath(frm).parent)
        return max(cands, key=lambda c: len(__import__("os").path.commonprefix([d, c])))

    nodes, edges = [], []
    for p in paths:
        v = files[p]["variants"]
        sha = max(v, key=v.get)
        size = v[sha]
        head = blobs.get(sha)[:16] if (PurePosixPath(p).suffix.lower() == ".out") else b""
        nodes.append({"id": p, "type": classify(p, size, head), "size": size, "sha": sha, "hash": content_hash(blobs, sha, p, size),
                      "hashes": sorted({content_hash(blobs, s, p, z) for s, z in v.items()}), "refs": sorted(set(files[p]["refs"]))})
        parent = str(PurePosixPath(p).parent)
        edges.append([parent, p, "contain"])
    dirs = {str(x) for p in paths for x in PurePosixPath(p).parents if str(x) != "."}
    for d in sorted(dirs):
        nodes.append({"id": d, "type": "dir", "size": 0})
        par = str(PurePosixPath(d).parent)
        if par != ".":
            edges.append([par, d, "contain"])

    for n in list(nodes):
        p = n["id"]
        if n["type"] in ("dir", "pdf", "junk", "log", "cache", "toolchain", "private"):
            continue
        ext = PurePosixPath(p).suffix.lower()
        if ext not in TEXT_EXT or n["size"] > MAX_TEXT:
            continue
        sha = max(files[p]["variants"], key=files[p]["variants"].get)
        txt = blobs.get(sha).decode("utf-8", "replace")
        found = set()
        if ext in {".tex", ".sty", ".cls"}:
            for m in RX_TEX.finditer(txt):
                for tok in m.group(1).split(","):
                    t = resolve(tok.strip(), p, ("", ".tex", ".bib", ".pdf", ".png", ".sty"))
                    if t:
                        found.add((t, "tex"))
        elif ext == ".py":
            for m in RX_PYIMP.finditer(txt):
                mods = [m.group(1)] if m.group(1) else [x.strip().split(" as ")[0] for x in m.group(2).split(",")]
                for mod in mods:
                    if not mod:
                        continue
                    rel = mod.replace(".", "/")
                    t = resolve(rel + ".py", p) or resolve(rel + "/__init__.py", p)
                    if not t and "." not in mod:
                        cand = [c for c in base.get(mod + ".py", [])]
                        t = cand[0] if len(cand) == 1 else None
                    if t and t != p:
                        found.add((t, "py"))
        if ext in {".md", ".py", ".tex", ".sh", ".txt", ".json", ".toml", ".yml"}:
            for m in RX_PATH.finditer(txt):
                t = resolve(m.group(0), p)
                if t and t != p and (t, "tex") not in found and (t, "py") not in found:
                    found.add((t, "ref"))
        for t, kind in found:
            edges.append([p, t, kind])

    graph = {"name": name, "refs": refs, "nodes": nodes, "edges": edges}
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    (out / f"graph_{name}.json").write_text(json.dumps(graph, separators=(",", ":")), encoding="utf-8")
    write_overview(graph, out)
    return graph


def group_of(path: str, depth=2):
    return "/".join(path.split("/")[:depth]) or path


def write_overview(g, out: Path):
    name = g["name"]
    types = {n["id"]: n["type"] for n in g["nodes"] if n["type"] != "dir"}
    cnt = Counter()
    tcnt = defaultdict(Counter)
    for p, t in types.items():
        gk = group_of(p)
        cnt[gk] += 1
        tcnt[gk][t] += 1
    ecnt = Counter()
    for s, d, k in g["edges"]:
        if k == "contain" or s not in types or d not in types:
            continue
        a, b = group_of(s), group_of(d)
        if a != b:
            ecnt[(a, b, k)] += 1
    top = [k for k, _ in cnt.most_common(40)]
    ids = {k: f"n{i}" for i, k in enumerate(top)}
    lines = ["flowchart LR"]
    for k in top:
        main_t = tcnt[k].most_common(1)[0][0]
        lines.append(f'  {ids[k]}["{k}<br/>{cnt[k]} files ({main_t})"]')
    for (a, b, k), c in ecnt.most_common(80):
        if a in ids and b in ids:
            lines.append(f"  {ids[a]} -->|{k} x{c}| {ids[b]}")
    (out / f"graph_{name}.mmd").write_text("\n".join(lines) + "\n", encoding="utf-8")
    vis_nodes = [{"id": k, "label": f"{k}\n{cnt[k]}", "value": cnt[k], "title": ", ".join(f"{t}:{c}" for t, c in tcnt[k].most_common())} for k in cnt]
    vis_edges = [{"from": a, "to": b, "label": f"{k} x{c}", "arrows": "to", "value": c} for (a, b, k), c in ecnt.items()]
    html = ("<!doctype html><meta charset=utf-8><title>%s graph</title>"
            "<script src='https://cdnjs.cloudflare.com/ajax/libs/vis-network/9.1.9/standalone/umd/vis-network.min.js'></script>"
            "<body style='margin:0;font-family:sans-serif'><div style='padding:8px'>%s: %d files, %d folders (depth 2). "
            "Node size = file count; hover for the type mix. Full file-level graph: graph_%s.json.</div>"
            "<div id=g style='height:92vh'></div><script>new vis.Network(document.getElementById('g'),"
            "{nodes:new vis.DataSet(%s),edges:new vis.DataSet(%s)},{nodes:{shape:'dot',scaling:{min:8,max:40}},"
            "edges:{scaling:{min:1,max:6},font:{size:9}},physics:{stabilization:true}});</script>"
            % (name, name, len(types), len(cnt), name, json.dumps(vis_nodes), json.dumps(vis_edges)))
    (out / f"graph_{name}.html").write_text(html, encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--refs", nargs="+", required=True)
    ap.add_argument("--out", default="graphs")
    a = ap.parse_args()
    g = build(a.name, a.repo, a.refs, a.out)
    c = Counter(n["type"] for n in g["nodes"])
    print(a.name, "nodes", len(g["nodes"]), "edges", len(g["edges"]), dict(c.most_common()))


if __name__ == "__main__":
    main()
