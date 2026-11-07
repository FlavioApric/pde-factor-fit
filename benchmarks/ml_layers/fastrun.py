"""fastrun: the general fast-evaluation harness for corpus runs (sessions/LEARNED/SPEEDUP.md).

It wraps ll_corpus (same cases, same run_one, same CPU slot pool) and adds, for ANY corpus, ANY learned
arm and ANY pipeline version:
  1 reuse      a row already computed for the same case, arm and pipeline version (sha of src/) is copied,
               not rerun; rows are stamped with `code_sha`, so a changed pipeline never reuses stale rows
  2 order      cases run in rounds of one case per family (any prefix is family-balanced), each round
               longest-predicted first (LPT), the arms of a case back to back (pairs finish together)
  3 runtime    a learned runtime model (shrunk group means of log runtime, corpus > design > family >
               arm), trained on whatever rows exist and updated online after every finished run; it
               adapts by itself when the pipeline changes, and an unseen corpus/arm falls back to
               broader groups. Saved in analysis/exp/models/runtime.json.
  4 stop early an anytime-valid confidence sequence (hedged betting CS, Waudby-Smith & Ramdas 2023) on
               the paired differences arm - base: stop for gain (lower > 0), harm (false-confident
               difference lower > 0) or no gain (upper < delta). Valid under optional stopping, so
               stopping early stays honest. Nulls (corpus N) and the final §2.4 gate are run in full.
  5 cap        optional per-case timeout = k x predicted runtime of the base arm (same for every arm).

Usage (all ll_corpus case options work):
  python fastrun.py train --rows out/*.jsonl                       # (re)fit the runtime model
  python fastrun.py run --corpus G --split test --arms off highk --out out/ll_G.jsonl \
        --reuse ../../../other/out/*.jsonl --sequential --delta 0.1   # fast paired evaluation
  python fastrun.py replay --rows out/ll_S.jsonl --arm highk        # what stopping/ordering would save
"""
from __future__ import annotations

import argparse
import glob
import json
import math
import subprocess
import sys
import time
from collections import defaultdict
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MODEL = HERE / "models" / "runtime.json"
SHRINK = 3.0  # pseudo-count of the parent group in the shrunk mean


SHARED_ROOT = Path(r"D:\Larned layers")
SOURCES = [  # every place a session writes rows; the main checkout is read-only (benchmark / E13 rows)
    str(SHARED_ROOT / "PDEFactorML" / "analysis" / "exp" / "out" / "*.jsonl"),
    str(SHARED_ROOT / ".claude" / "worktrees" / "*" / "PDEFactorML" / "analysis" / "exp" / "out" / "*.jsonl"),
    str(Path(r"D:\PDEFactorML") / "benchmarks" / "out" / "*.jsonl"),
    str(Path(r"D:\PDEFactorML") / "benchmarks" / "out" / "micro" / "*.jsonl"),
]
INDEX = SHARED_ROOT / "PDEFactorML" / "analysis" / "exp" / "out" / "DATA_INDEX.json"


def normalize(r, path=""):
    """A row in the ll_corpus schema, or None. Main's benchmark rows (case, method, sampling, noise) and
    E13 rows (family, seed, noise, pipeline{...}) become corpus 'bench' / 'E13' rows with arm 'main'
    (the newer main pipeline): usable for the runtime model and, after the sync, as off rows."""
    if all(k in r for k in ("corpus", "design", "learned")) and isinstance(r["design"], list):
        return r
    if "case" in r and "method" in r and r.get("method") == "pipeline":
        return dict(corpus="bench", family=r["case"], seed=r.get("seed", 0),
                    design=[r.get("sampling", "?"), r.get("noise", 0)], learned="main",
                    runtime=r.get("runtime"), label=r.get("label"), source=path)
    if "family" in r and isinstance(r.get("pipeline"), dict):
        q = r["pipeline"]
        return dict(corpus="E13", family=r["family"], seed=r.get("seed", 0), design=["grid", r.get("noise", 0)],
                    learned="main", runtime=q.get("runtime"), label=q.get("label"), source=path)
    return None


def all_rows(sources=None):
    for p in sorted({p for g in (sources or SOURCES) for p in glob.glob(str(g))}):
        try:
            for line in Path(p).read_text().splitlines():
                if line.strip():
                    try:
                        r = normalize(json.loads(line), p)
                    except (json.JSONDecodeError, TypeError):
                        continue
                    if r is not None:
                        yield p, r
        except OSError:
            continue


def case_key(r):
    return (r["corpus"], r.get("family") or "null", r["seed"], tuple(r["design"]))


def run_key(r):
    return case_key(r) + (r["learned"],)


def src_sha():
    """Tree hash of src/ at HEAD, plus '-dirty' when src/ has uncommitted changes."""
    try:
        sha = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD:./src"], capture_output=True,
                             text=True, check=True).stdout.strip()
        dirty = subprocess.run(["git", "-C", str(ROOT), "status", "--porcelain", "--", "src"],
                               capture_output=True, text=True).stdout.strip()
        return sha[:12] + ("-dirty" if dirty else "")
    except Exception:  # noqa: BLE001
        return "unknown"


def read_rows(paths):
    for p in paths:
        for line in Path(p).read_text().splitlines():
            if line.strip():
                yield json.loads(line)


# ------------------------------------------------------------------ 3 runtime model
class RuntimeModel:
    """log runtime ~ shrunk mean over nested groups; every group keeps (n, sum, sum of squares)."""

    def __init__(self, groups=None):
        self.g = defaultdict(lambda: [0.0, 0.0, 0.0], groups or {})

    @staticmethod
    def _levels(corpus, family, design, arm):
        d = f"{design[0]}|{design[1]}"
        return ["*", corpus, f"{corpus}/{d}", f"{corpus}/{d}/{family}", f"{corpus}/{d}/{family}/{arm}"]

    def update(self, row):
        rt = row.get("runtime")
        if not rt or rt <= 0:
            return self
        y = math.log(rt)
        for k in self._levels(row["corpus"], row.get("family") or "null", row["design"], row["learned"]):
            s = self.g[k]
            s[0] += 1
            s[1] += y
            s[2] += y * y
        return self

    def fit(self, rows):
        for r in rows:
            self.update(r)
        return self

    def log_mean(self, key):
        corpus, family, _seed, design, arm = key
        m = math.log(60.0)  # prior before any data: one minute
        for k in self._levels(corpus, family or "null", design, arm):
            n, s, _ = self.g.get(k, (0.0, 0.0, 0.0))
            m = (s + SHRINK * m) / (n + SHRINK)
        return m

    def predict(self, key):
        return math.exp(self.log_mean(key))

    def save(self, path=MODEL):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_text(json.dumps(dict(self.g), indent=0))

    @classmethod
    def load(cls, path=MODEL):
        p = Path(path)
        return cls(json.loads(p.read_text())) if p.exists() else cls()


# ------------------------------------------------------------------ 2 order
def order(tasks, model, seed=0):
    """Rounds of one case per family (shuffled by seed), longest predicted first inside a round; the
    arms of a case stay together in the given arm order."""
    rng = np.random.default_rng(seed)
    cases = defaultdict(list)
    for t in tasks:
        cases[t[:4]].append(t)
    by_fam = defaultdict(list)
    for c in cases:
        by_fam[c[1] or "null"].append(c)
    for f in by_fam:
        by_fam[f].sort(key=str)
        rng.shuffle(by_fam[f])
    out = []
    for r in range(max((len(v) for v in by_fam.values()), default=0)):
        rnd = [by_fam[f][r] for f in sorted(by_fam) if r < len(by_fam[f])]
        rnd.sort(key=lambda c: -sum(model.predict(t) for t in cases[c]))
        for c in rnd:
            out.extend(cases[c])
    return out


# ------------------------------------------------------------------ 4 anytime-valid stop
class ConfSeq:
    """Hedged betting confidence sequence for the mean of values in [-1, 1] (Waudby-Smith & Ramdas
    2023, JRSS-B, predictable plug-in bets, running intersection). Valid at every n simultaneously."""

    def __init__(self, alpha=0.05, c=0.75, grid=2001):
        self.alpha, self.c = alpha, c
        self.m = np.linspace(0.0, 1.0, grid)
        self.lkp = np.zeros(grid)
        self.lkm = np.zeros(grid)
        self.out = np.zeros(grid, bool)
        self.n, self.sx, self.sv = 0, 0.0, 0.0

    def update(self, d):
        x = (float(d) + 1.0) / 2.0
        t = self.n + 1
        mu = (0.5 + self.sx) / t
        var = (0.25 + self.sv) / t
        lam = math.sqrt(2 * math.log(2 / self.alpha) / (var * t * math.log(1 + t)))
        with np.errstate(divide="ignore"):
            lp = np.minimum(lam, self.c / np.maximum(self.m, 1e-12))
            lm = np.minimum(lam, self.c / np.maximum(1 - self.m, 1e-12))
        self.lkp += np.log1p(lp * (x - self.m))
        self.lkm += np.log1p(-lm * (x - self.m))
        k = 0.5 * np.exp(self.lkp) + 0.5 * np.exp(self.lkm)
        self.out |= k >= 1 / self.alpha
        self.n, self.sx = t, self.sx + x
        self.sv += (x - mu) ** 2

    def interval(self):
        keep = self.m[~self.out]
        if keep.size == 0:
            return (float("nan"), float("nan"))
        return (2 * keep.min() - 1, 2 * keep.max() - 1)


def right_set(r):
    return float(r.get("category") in ("right", "equivalent"))


def false_conf(r):
    return float(r.get("category") == "false-confident")


class SeqGate:
    """Paired arm vs base on finished cases. Primary: right-set (or any 0/1 row metric); safety:
    false-confident. alpha is split over the two sequences."""

    def __init__(self, arm, base="off", alpha=0.05, delta=0.1, min_pairs=10, primary=right_set):
        self.arm, self.base, self.delta, self.min_pairs, self.primary = arm, base, delta, min_pairs, primary
        self.cs_p, self.cs_f = ConfSeq(alpha / 2), ConfSeq(alpha / 2)
        self.half = defaultdict(dict)
        self.pairs = 0

    def add(self, row):
        if row["learned"] not in (self.arm, self.base):
            return
        h = self.half[case_key(row)]
        h[row["learned"]] = row
        if self.arm in h and self.base in h and "done" not in h:
            h["done"] = True
            a, b = h[self.arm], h[self.base]
            self.cs_p.update(self.primary(a) - self.primary(b))
            self.cs_f.update(false_conf(a) - false_conf(b))
            self.pairs += 1

    def verdict(self):
        (lo, hi), (flo, fhi) = self.cs_p.interval(), self.cs_f.interval()
        v = dict(pairs=self.pairs, primary=(lo, hi), false_conf=(flo, fhi), stop=False, reason="running")
        if self.pairs < self.min_pairs:
            return v
        if flo > 0:
            v.update(stop=True, reason="harm")
        elif lo > 0:
            v.update(stop=True, reason="gain")
        elif hi < self.delta:
            v.update(stop=True, reason="no gain")
        return v


# ------------------------------------------------------------------ 1 reuse
class ReuseIndex:
    def __init__(self, paths, sha, accept_nosha=False):
        self.rows = {}
        for _, r in all_rows(paths):
            if r.get("learned") == "main":
                continue  # newer pipeline: never reused before the sync
            if r.get("label") in ("CRASH", "TIMEOUT") and r.get("code_sha") != sha:
                continue
            ok = r.get("code_sha") == sha or (accept_nosha and "code_sha" not in r)
            if ok:
                self.rows.setdefault(run_key(r), r)

    def get(self, key):
        return self.rows.get(key)


# ------------------------------------------------------------------ commands
def cmd_train(a):
    need = ("corpus", "design", "learned", "runtime")
    rows = [r for _, r in all_rows(a.rows or None) if all(r.get(k) for k in need)]
    m = RuntimeModel().fit(rows)
    # leave-one-out error on log runtime against a single global median
    err_m, err_0 = [], []
    med = float(np.median([math.log(r["runtime"]) for r in rows])) if rows else 0.0
    for r in rows:
        y = math.log(r["runtime"])
        loo = RuntimeModel({k: list(v) for k, v in m.g.items()})
        for k in loo._levels(r["corpus"], r.get("family") or "null", r["design"], r["learned"]):
            s = loo.g[k]
            s[0] -= 1
            s[1] -= y
            s[2] -= y * y
        err_m.append(abs(loo.log_mean(run_key(r)) - y))
        err_0.append(abs(med - y))
    m.save(a.model)
    print(f"{len(rows)} rows -> {a.model}")
    if rows:
        print(f"LOO median |log error|: model {np.median(err_m):.2f} (x{math.exp(np.median(err_m)):.1f}), "
              f"global median {np.median(err_0):.2f} (x{math.exp(np.median(err_0)):.1f})")


def cmd_index(a):
    """The shared data index: one line per row file of any session (and main), with what it holds."""
    files = {}
    for p, r in all_rows(a.sources or None):
        f = files.setdefault(p, dict(path=p, rows=0, corpora=set(), arms=set(), splits=set(), shas=set(),
                                     fields=set(), crash=0))
        f["rows"] += 1
        f["corpora"].add(r["corpus"])
        f["arms"].add(r["learned"])
        f["splits"].add(str(r.get("split")))
        f["shas"].add(r.get("code_sha", "none"))
        f["crash"] += r.get("label") in ("CRASH", "TIMEOUT")
        f["fields"] |= {k for k in ("export", "resid", "lp_trace", "steps", "coef", "guard") if k in r}
    out = []
    for p, f in sorted(files.items()):
        wt = Path(p).parts
        producer = wt[wt.index("worktrees") + 1] if "worktrees" in wt else ("main" if wt[1] == "PDEFactorML" else "S-LEARNED")
        out.append({k: (sorted(v) if isinstance(v, set) else v) for k, v in f.items()} | dict(
            producer=producer, mtime=time.strftime("%Y-%m-%d %H:%M", time.localtime(Path(p).stat().st_mtime))))
    Path(a.out).write_text(json.dumps(out, indent=1))
    md = ["# Shared data index (fastrun.py index; regenerate any time)", "",
          "| producer | file | rows | crash/timeout | corpora | arms | splits | fields | sha |", "|---|---|---|---|---|---|---|---|---|"]
    for f in out:
        md.append(f"| {f['producer']} | {Path(f['path']).name} | {f['rows']} | {f['crash']} | {','.join(f['corpora'])} | "
                  f"{','.join(f['arms'])} | {','.join(f['splits'])} | {','.join(f['fields'])} | {','.join(f['shas'])} |")
    Path(a.out).with_suffix(".md").write_text("\n".join(md) + "\n")
    print(f"{len(out)} files, {sum(f['rows'] for f in out)} rows -> {a.out} (+ .md)")


def makespan(durs, workers):
    free = [0.0] * workers
    for d in durs:
        i = int(np.argmin(free))
        free[i] += d
    return max(free) if durs else 0.0


def cmd_replay(a):
    rows = list(read_rows(a.rows))
    model = RuntimeModel.load(a.model)
    byk = {run_key(r): r for r in rows}
    tasks = [k for k in byk if k[4] in (a.base, a.arm)]
    pairs = {k[:4] for k in tasks if k[:4] + (a.base,) in byk and k[:4] + (a.arm,) in byk}
    tasks = [k for k in tasks if k[:4] in pairs]
    od = order(tasks, model, a.seed)
    g = SeqGate(a.arm, a.base, a.alpha, a.delta, a.min_pairs)
    spent, stop_at = 0.0, None
    total = sum(byk[k].get("runtime") or 0 for k in od)
    for k in od:
        spent += byk[k].get("runtime") or 0
        g.add(byk[k])
        v = g.verdict()
        if v["stop"] and stop_at is None:
            stop_at = (v["pairs"], spent, v)
    v = g.verdict()
    print(f"{len(pairs)} pairs, arm {a.arm} vs {a.base}: final CS right-set {v['primary'][0]:+.2f}..{v['primary'][1]:+.2f}, "
          f"false-conf {v['false_conf'][0]:+.2f}..{v['false_conf'][1]:+.2f}")
    if stop_at:
        n, s, vv = stop_at
        print(f"sequential stop after {n} pairs ({vv['reason']}): {s:.0f} s of {total:.0f} s CPU ({s / total:.0%})")
    else:
        print(f"no early stop at delta={a.delta}: all {len(pairs)} pairs needed")
    durs_old = [byk[k].get("runtime") or 0 for k in sorted(tasks, key=lambda k: (k[2], str(k[3]), k[1], k[4]))]
    durs_new = [byk[k].get("runtime") or 0 for k in od]
    print(f"makespan on {a.workers} workers: ll_corpus order {makespan(durs_old, a.workers):.0f} s, "
          f"fastrun order {makespan(durs_new, a.workers):.0f} s")


def cmd_run(a):
    import ll_corpus as lc

    sha = src_sha()
    need = ("corpus", "design", "learned", "runtime")
    model = RuntimeModel().fit(r for _, r in all_rows() if all(r.get(k) for k in need))  # always the latest model
    if a.reuse_shared:
        a.reuse = list(a.reuse) + SOURCES[:2]
    designs = lc.DESIGNS[a.corpus] if a.designs is None else [lc.DESIGNS[a.corpus][i] for i in a.designs]
    seeds = a.seeds if a.seeds is not None else [s for sp in a.split for s in lc.SEEDS[a.corpus][sp]]
    fams = [None] if a.corpus == "N" else a.families
    tasks = [(a.corpus, f, s, dz, ln) for s in seeds for dz in designs for f in fams for ln in a.arms]
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    have = {run_key(r): r for r in read_rows([out])} if out.exists() else {}
    gates = [SeqGate(arm, a.arms[0], a.alpha, a.delta, a.min_pairs) for arm in a.arms[1:]]
    for r in have.values():
        for g in gates:
            g.add(r)
    reuse = ReuseIndex(sorted({p for g in a.reuse for p in glob.glob(g)}), sha, a.accept_nosha) if a.reuse else None
    todo, reused = [], 0
    for t in tasks:
        k = (t[0], t[1] or "null", t[2], tuple(t[3]), t[4])
        if k in have:
            continue
        r = reuse.get(k) if reuse else None
        if r is not None:
            r = dict(r, reused=True)
            with open(out, "a") as fh:
                fh.write(json.dumps(r, default=str) + "\n")
            for g in gates:
                g.add(r)
            reused += 1
        else:
            todo.append(t)
    todo = order(todo, model, a.seed)
    print(f"sha {sha}: {len(tasks)} runs, {len(have)} done, {reused} reused, {len(todo)} to run, {a.workers} workers",
          flush=True)

    def on_row(row):
        row["code_sha"] = sha
        model.update(row)
        for g in gates:
            g.add(row)
            v = g.verdict()
            print(f"  [{g.arm}] pairs {v['pairs']} right-set CS {v['primary'][0]:+.2f}..{v['primary'][1]:+.2f} "
                  f"fc {v['false_conf'][0]:+.2f}..{v['false_conf'][1]:+.2f} {v['reason']}", flush=True)
        return row

    def should_stop():
        return a.sequential and a.corpus != "N" and gates and all(g.verdict()["stop"] for g in gates)

    def cap_of(args):
        if not a.adaptive_cap:
            return a.cap
        base = (args[0], args[1] or "null", args[2], tuple(args[3]), a.arms[0])
        return min(a.cap, max(a.min_cap, a.adaptive_cap * model.predict(base)))

    lc.run_all(todo, str(out), a.workers, a.cap, on_row=on_row, should_stop=should_stop, cap_of=cap_of)
    model.save(a.model)
    for g in gates:
        print(f"[{g.arm}] final: {g.verdict()}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("train")
    t.add_argument("--rows", nargs="*", default=[], help="globs; default: every shared source (all sessions + main)")
    t.add_argument("--model", default=str(MODEL))
    i = sub.add_parser("index")
    i.add_argument("--sources", nargs="*", default=[])
    i.add_argument("--out", default=str(INDEX))
    r = sub.add_parser("replay")
    r.add_argument("--rows", nargs="+", required=True)
    r.add_argument("--arm", required=True)
    r.add_argument("--base", default="off")
    for p in (r,):
        p.add_argument("--model", default=str(MODEL))
        p.add_argument("--alpha", type=float, default=0.05)
        p.add_argument("--delta", type=float, default=0.1)
        p.add_argument("--min-pairs", type=int, default=10)
        p.add_argument("--seed", type=int, default=0)
        p.add_argument("--workers", type=int, default=4)
    u = sub.add_parser("run")
    u.add_argument("--corpus", required=True)
    u.add_argument("--split", nargs="*", default=["fit", "cal", "test"])
    u.add_argument("--families", nargs="*", default=["F1", "F2", "F3", "F4", "F5"])
    u.add_argument("--designs", nargs="*", type=int, default=None)
    u.add_argument("--seeds", nargs="*", type=int, default=None)
    u.add_argument("--arms", nargs="+", default=["off"], help="first arm is the base of the comparison")
    u.add_argument("--out", required=True)
    u.add_argument("--reuse", nargs="*", default=[], help="row files (globs) to copy matching rows from")
    u.add_argument("--reuse-shared", action="store_true", help="reuse from every session's out/ (see DATA_INDEX)")
    u.add_argument("--accept-nosha", action="store_true", help="also reuse rows without code_sha (legacy)")
    u.add_argument("--sequential", action="store_true", help="stop launching runs once every arm is decided")
    u.add_argument("--adaptive-cap", type=float, default=0.0, help="per-case cap = k x predicted base runtime")
    u.add_argument("--min-cap", type=float, default=120.0)
    u.add_argument("--cap", type=float, default=1200.0)
    u.add_argument("--workers", type=int, default=4)
    u.add_argument("--model", default=str(MODEL))
    u.add_argument("--alpha", type=float, default=0.05)
    u.add_argument("--delta", type=float, default=0.1)
    u.add_argument("--min-pairs", type=int, default=10)
    u.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()
    {"train": cmd_train, "replay": cmd_replay, "run": cmd_run, "index": cmd_index}[a.cmd](a)


if __name__ == "__main__":
    main()
