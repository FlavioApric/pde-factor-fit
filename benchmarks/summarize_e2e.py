"""Summary table of benchmarks/out/e2e.jsonl: per sampling x noise x method, right factor set, exact
structure, median coefficient error (over all inputs, failures = inf), weight error, calibration."""
import collections
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def main(path=ROOT / "benchmarks" / "out" / "e2e.jsonl"):
    rows = [json.loads(line) for line in open(path) if line.strip()]
    g = collections.defaultdict(list)
    for r in rows:
        g[(str(r["sampling"]), float(r["noise"]), r["method"])].append(r)
    out = ["| sampling | noise | method | n | right set | exact structure | median coef err | median weight err | cover90 | w_cover90 | crashes |",
           "|---|---|---|---|---|---|---|---|---|---|---|"]
    order = {"pipeline": 0, "core_v2": 1, "weak_sindy": 2, "ensemble_sindy": 3, "sbr_sindy": 4, "pdefind": 5, "bopdmd": 6}
    for k in sorted(g, key=lambda k: (k[0], k[1], order.get(k[2], 9))):
        v = g[k]
        ce = np.array([r.get("coef_err") if r.get("coef_err") is not None else np.inf for r in v], float)
        we = [r["weight_err"] for r in v if r.get("weight_err") is not None]
        cv = [r["cover90"] for r in v if r.get("cover90") is not None]
        wc = [r["w_cover90"] for r in v if r.get("w_cover90") is not None]
        f = lambda a: f"{np.median(a):.2g}" if len(a) else "-"  # noqa: E731
        m = lambda a: f"{np.mean(a):.2f}" if len(a) else "-"  # noqa: E731
        out.append(f"| {k[0]} | {k[1]:g} | {k[2]} | {len(v)} | {np.mean([bool(r.get('factor_set')) for r in v]):.2f} | "
                   f"{np.mean([bool(r.get('struct_ok')) for r in v]):.2f} | {f(ce)} | {f(we)} | {m(cv)} | {m(wc)} | "
                   f"{sum(1 for r in v if r.get('error'))} |")
    return "\n".join(out)


if __name__ == "__main__":
    print(main(*(sys.argv[1:])))
