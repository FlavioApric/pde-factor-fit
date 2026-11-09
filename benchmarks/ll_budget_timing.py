"""S-LEARNED-LB: paired same-load timing, off vs lb rows of one file (ll_budget_corpus.py --learned off lb).

Usage: python ll_budget_timing.py analysis/exp/out/ll_lb_G_timing.jsonl
Prints per-pair runtimes and the lb/off ratio (geometric mean per run, and total) with 95 % paired bootstrap CIs.
"""
import json
import sys

import numpy as np
off, on = {}, {}
for l in open(sys.argv[1]):
    r = json.loads(l)
    k = (r["family"], r["seed"], json.dumps(r["design"]))
    (off if r["learned"] == "off" else on)[k] = r
ks = sorted(set(off) & set(on))
fin = [k for k in ks if off[k]["label"] not in ("TIMEOUT", "CRASH") and on[k]["label"] not in ("TIMEOUT", "CRASH")]
a = np.array([off[k]["runtime"] for k in fin]); b = np.array([on[k]["runtime"] for k in fin])
same = sum(off[k]["label"] == on[k]["label"] and off[k].get("factors") == on[k].get("factors") for k in fin)
print("pairs", len(ks), "finished both", len(fin), "same label+factors", same)
for k in ks:
    print(k, off[k]["label"], round(off[k]["runtime"], 1), on[k]["label"], round(on[k]["runtime"], 1))
rng = np.random.default_rng(0)
lr = np.log(b / a)
bs = [np.exp(np.mean(lr[i])) for i in rng.integers(0, len(lr), (10000, len(lr)))]
bt = [(b[i].sum() / a[i].sum()) for i in rng.integers(0, len(lr), (10000, len(lr)))]
print("geo-mean ratio on/off %.3f [%.3f, %.3f]" % (np.exp(lr.mean()), *np.percentile(bs, [2.5, 97.5])))
print("total ratio %.3f [%.3f, %.3f]; total %.0f -> %.0f s" % (b.sum() / a.sum(), *np.percentile(bt, [2.5, 97.5]), a.sum(), b.sum()))
