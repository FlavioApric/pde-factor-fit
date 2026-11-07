"""Keep every benchmark result for later estimation (learned-layer training, calibration, trend tables).

    .venv/Scripts/python.exe benchmarks/archive.py

benchmarks/out/ is scratch space (gitignored); this copies its result files (*.jsonl, micro suites,
and the analysis/exp/out tables) into the tracked benchmarks/data/, never overwriting a different file
of the same name, and rewrites benchmarks/data/INDEX.md with rows, size and the code commit at
archive time. Descriptions of known files are kept in DESCRIBE; add one when a new run is archived.
"""
from __future__ import annotations

import datetime as dt
import filecmp
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "benchmarks" / "data"
SOURCES = [(ROOT / "benchmarks" / "out", "*.jsonl", ""), (ROOT / "benchmarks" / "out" / "micro", "*.jsonl", "micro/"),
           (ROOT / "analysis" / "exp" / "out", "*.csv", "exp/"), (ROOT / "analysis" / "exp" / "out", "*.txt", "exp/")]
SKIP = {"e2e.jsonl"}  # the working copy of the latest full run (archived under its run name)
DESCRIBE = {
    "e2e_grid_v1.jsonl": "full benchmark, grid only, core v1 era",
    "e2e_run2.jsonl": "full benchmark run 2 (Phase 3)",
    "e2e_run3.jsonl": "full benchmark run 3",
    "e2e_run4.jsonl": "full benchmark run 4",
    "e2e_run5.jsonl": "full benchmark run 5",
    "e2e_run6.jsonl": "full benchmark run 6 (v2.11 reference: pipeline + SINDy variants, 270 inputs x 7 methods)",
    "e2e_run7_pre867.jsonl": "run 7 on code before 867dcc0 (stopped at 157/270; pipeline + core_v2)",
    "e2e_run7.jsonl": "run 7 --quick on 867dcc0 (stopped at 33/120; pipeline + core_v2)",
    "runs.jsonl": "core-only benchmark grid (bench.py), Phase 1-2",
    "e13_random.jsonl": "E13 random PDEs, first run",
    "e13_v2.jsonl": "E13 random PDEs seeds 0-2 (14 draws), code before c3457c9",
    "e13_v3.jsonl": "E13 random PDEs, the 6 remaining draws, code c3457c9",
    "micro/speed_v1.jsonl": "micro suite 'speed', code 66b5893-era (10 inputs)",
    "micro/conjugate_v2.jsonl": "micro suite 'conjugate', same-family split rule (11 inputs)",
}


def _commit():  # the D: repository that commits PDEFactorML/ (the nested PDEFactorML/.git is a stale local one)
    try:
        return subprocess.run(["git", "-c", "safe.directory=*", "-C", str(ROOT.parent), "rev-parse", "--short", "HEAD"],
                              capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "?"


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    idx = DATA / "INDEX.md"
    old = {}
    if idx.exists():
        for ln in idx.read_text(encoding="utf-8").splitlines()[4:]:
            c = [x.strip() for x in ln.strip("|").split("|")]
            if len(c) == 6:
                old[c[0]] = c
    commit, today = _commit(), dt.date.today().isoformat()
    for src, pat, pre in SOURCES:
        if not src.exists():
            continue
        for f in sorted(src.glob(pat)):
            if f.name in SKIP:
                continue
            name = pre + f.name
            dst = DATA / name
            dst.parent.mkdir(parents=True, exist_ok=True)
            if dst.exists() and filecmp.cmp(f, dst, shallow=False):
                continue
            if dst.exists():  # changed since last archive (a resumed run): keep both
                dst = dst.with_name(f"{dst.stem}.{today}{dst.suffix}")
                name = str(dst.relative_to(DATA)).replace("\\", "/")
            shutil.copy2(f, dst)
            rows = sum(1 for _ in open(dst, encoding="utf-8", errors="ignore"))
            old[name] = [name, str(rows), f"{dst.stat().st_size // 1024} KB", today, commit,
                         DESCRIBE.get(name.split(".20")[0] + dst.suffix if ".20" in name else name, "")]
            print("archived", name)
    lines = ["# Benchmark data archive", "", "| file | rows | size | archived | code at archive | what |",
             "|---|---|---|---|---|---|"]
    lines += ["| " + " | ".join(c) + " |" for _, c in sorted(old.items())]
    idx.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
