"""C' trigger data (P7): can an ANALYTIC detector on the off run's reported factors serve as the trigger?

    OMP_NUM_THREADS=1 .venv/Scripts/python.exe benchmarks/cprime_trigger.py [--ll "D:/Larned layers/PDEFactorML"]

Data (read only) from the learned-layers tree: the off runs (analysis/exp/out/ll_V.jsonl, ll_Gmatch_p7.jsonl,
learned == "off"), the oracle sweep (ll_Cprime.jsonl, ll_Cprime_timeout.jsonl; a case is rescued when an
action gives right / equivalent), the 12 sweep cases (ll_Cprime_cases*.json) and the 86 clean cases of
cprime_oracle_p7.md (rows of sessions/LEARNED/V1/results/v1_gate_resid_p7.json whose off category is right,
equivalent or abstain-ok). Inputs are regenerated as ll_corpus.grid_input (default_rng(1000 + seed),
sigma = noise * std(u)); every case is a noisy grid.

Detectors (truth-free; the T95 df-adjusted chi^2 gap is not one, it uses the truth):
  T96   validate.smooth_gof_log10p(reported factors) < loop.PRED_LOGP (-3)
  V0.1  omnibus log10 p of validate.predictive_bins < PRED_LOGP (-3); also validate's V0.1 flag
        (omnibus p < P_OMNIBUS and a bin below P_BIN / #bins)
  T88   raw_gof: scattered inputs only, so n/a on every case here
Output: <ll>/analysis/exp/out/cprime_trigger_p7.jsonl and .md (new files only).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "analysis" / "exp"))
GOOD = ("right", "equivalent")


def _key(r):
    return (r["corpus"], r["family"], int(r["seed"]), json.dumps(list(r["design"])))


def _jsonl(p):
    return [json.loads(s) for s in Path(p).read_text(encoding="utf-8").splitlines() if s.strip()]


def detectors(row):
    import sympy as sp

    from pdefactor.loop import PRED_LOGP
    from pdefactor.simulator import random_pde
    from pdefactor.synthetic import grid
    from pdefactor.validate import P_BIN, P_OMNIBUS, _log10sf, predictive_bins, smooth_gof_log10p

    sm, noise = row["design"]
    assert sm == "grid"
    d = random_pde(row["family"], int(row["seed"]))
    t, x, u = grid(d.field)
    rng = np.random.default_rng(1000 + int(row["seed"]))
    sig = noise * np.std(u)
    un = u + sig * rng.standard_normal(u.shape)
    facs = [sp.sympify(q) for q in row["factors"]]
    with np.errstate(all="ignore"):
        lp, kw, det = smooth_gof_log10p(facs, un, t, x, sig, detail=True)
        bins = predictive_bins(facs, un, t, x, sig)
    om = _log10sf(sum(b[1] for b in bins), sum(b[2] for b in bins))
    bad = [b for b in bins if b[3] < np.log10(P_BIN / max(len(bins), 1))]
    return dict(t96=float(lp), t96_fire=bool(lp < PRED_LOGP), t96_worst_kappa=None if kw is None else float(abs(kw)),
                v01=float(om), v01_fire=bool(om < PRED_LOGP), v01_flag=bool(om < np.log10(P_OMNIBUS) and bad),
                v01_stored=(row.get("v0") or {}).get("v01_omnibus_logp"), t88=None)


def t95_category(row, factors, label):
    """The row's class under main's scoring (T95 EQUIV_DF on); uses the truth, so it is scoring, not a detector."""
    import sympy as sp
    from e13_summary import DCHI2_EQUIV, chi2_gap

    from pdefactor.simulator import match, random_pde
    from pdefactor.synthetic import grid

    if not factors:
        return label
    d = random_pde(row["family"], int(row["seed"]))
    t, x, u = grid(d.field)
    rng = np.random.default_rng(1000 + int(row["seed"]))
    sig = row["design"][1] * np.std(u)
    un = u + sig * rng.standard_normal(u.shape)
    f, tr = [sp.sympify(q) for q in factors], list(d.factors)
    if match(tr, f)[0]:
        return "right"
    try:
        if match([sp.expand(sp.Mul(*tr))], [sp.expand(sp.Mul(*f))])[0] or chi2_gap(f, tr, un, t, x, sig) <= DCHI2_EQUIV:
            return "equivalent"
    except Exception:  # noqa: BLE001
        pass
    if label in ("UNDECIDED", "ID-KER") or str(label).startswith("ID-KER"):
        return "abstain-ok" if not row.get("all_ident") else "abstain"
    return "false-confident" if label == "FIT-COMPATIBLE" else "other"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--ll", type=Path, default=Path("D:/Larned layers/PDEFactorML"))
    a = ap.parse_args(argv)
    out = a.ll / "analysis" / "exp" / "out"
    off = {_key(r): r for p in ("ll_V.jsonl", "ll_Gmatch_p7.jsonl") for r in _jsonl(out / p) if r.get("learned") == "off"}
    cases = [_key(dict(c)) for p in ("ll_Cprime_cases.json", "ll_Cprime_cases_timeout.json")
             for c in json.loads((out / p).read_text())]
    sweep = {}
    for p in ("ll_Cprime.jsonl", "ll_Cprime_timeout.jsonl"):
        for r in _jsonl(out / p):
            if "NotApplicable" not in str(r.get("error", "")):
                sweep.setdefault(_key(r), {})[r["learned"][4:]] = r
    v1 = json.loads((a.ll / "sessions/LEARNED/V1/results/v1_gate_resid_p7.json").read_text())["downgrade"]["rows"]
    v1flag = {_key(r): bool(r["flag"]) for r in v1}
    clean = [_key(r) for r in v1 if off.get(_key(r), {}).get("category") in GOOD + ("abstain-ok",)]
    res = []
    for kind, keys in (("failure", cases), ("clean", clean)):
        for k in keys:
            o = off[k]
            acts = sweep.get(k, {})
            rec = dict(kind=kind, corpus=k[0], family=k[1], seed=k[2], design=json.loads(k[3]), off_label=o["label"],
                       off_category=o.get("category", o["label"]), truth=o.get("truth"), off_factors=o.get("factors"),
                       v1_flag=v1flag.get(k), rescuers=sorted(n for n, r in acts.items() if r.get("category") in GOOD),
                       lower_degree=({n: acts["lower_degree"].get(n) for n in ("label", "category", "factors")}
                                     if "lower_degree" in acts else None))
            if o.get("factors"):
                rec.update(detectors(o))
            if kind == "failure" or rec["off_category"] == "equivalent":
                rec["off_category_t95"] = t95_category(o, o.get("factors"), o["label"])
            else:
                rec["off_category_t95"] = rec["off_category"]
            if kind == "failure":
                ld = acts.get("lower_degree", {})
                rec["rescuers_t95"] = sorted(n for n, r in acts.items()
                                             if t95_category(dict(o, all_ident=o.get("all_ident", r.get("all_ident"))),
                                                             r.get("factors"), r.get("label")) in GOOD)
                rec["lower_degree_t95"] = t95_category(o, ld.get("factors"), ld.get("label")) if ld else None
            res.append(rec)
            print(kind, k[1], k[2], rec["off_label"], {n: rec.get(n) for n in ("t96", "v01", "v01_stored")}, flush=True)
    (out / "cprime_trigger_p7.jsonl").write_text("".join(json.dumps(r, default=str) + "\n" for r in res), encoding="utf-8")

    F = [r for r in res if r["kind"] == "failure"]
    C = [r for r in res if r["kind"] == "clean"]
    L = ["# C' trigger data: analytic detectors on the off run's reported factors (P7 cases)", "",
         f"{len(F)} off failures (cprime_oracle_p7.md; {sum(not r.get('off_factors') for r in F)} of them TIMEOUT: no "
         f"reported factors, no detector can be computed) and {len(C)} clean cases (off right / equivalent / "
         "abstain-ok). All are grid 5 % inputs, so T88 raw_gof (scattered only) is n/a everywhere. "
         "Fire = log10 p < -3 (loop.PRED_LOGP).", "",
         "| detector | failures flagged (of 8 with factors) | of 12 | clean false alarms | clean FIT-COMPATIBLE false alarms "
         "| ceiling: flagged AND rescued (of 12) | + TIMEOUT as trigger |",
         "|---|---|---|---|---|---|---|"]
    cfc = [r for r in C if r["off_label"] == "FIT-COMPATIBLE"]
    tmo = [r for r in F if not r.get("off_factors")]
    for name, f in (("T96 smooth_gof", lambda r: r.get("t96_fire")), ("V0.1 omnibus", lambda r: r.get("v01_fire")),
                    ("V0.1 validate flag", lambda r: r.get("v01_flag")),
                    ("T96 or V0.1 omnibus", lambda r: r.get("t96_fire") or r.get("v01_fire")),
                    ("V1 (memo)", lambda r: r.get("v1_flag")), ("T88 raw_gof", lambda r: None)):
        fl = [r for r in F if f(r)]
        ceil = [r for r in fl if r["rescuers"]]
        tceil = len(ceil) + sum(bool(r["rescuers"]) for r in tmo)
        L.append(f"| {name} | {sum(bool(f(r)) for r in F if r.get('off_factors'))} | {len(fl)} | "
                 f"{sum(bool(f(r)) for r in C)}/{len(C)} | {sum(bool(f(r)) for r in cfc)}/{len(cfc)} | "
                 f"{len(ceil)}/12 | {tceil}/12 |" if name != "T88 raw_gof" else
                 f"| {name} | n/a | n/a | n/a | n/a | 0/12 | {sum(bool(r['rescuers']) for r in tmo)}/12 |")
    L += ["", "Per failure:", "",
          "| case | off | T96 log10 p | V0.1 omnibus log10 p | V1 | rescuers | lower_degree -> | off factors | truth |",
          "|---|---|---|---|---|---|---|---|---|"]
    fmt = (lambda v: "-" if v is None else f"{v:.3g}")
    for r in F:
        ld = r["lower_degree"] or {}
        L.append(f"| {r['corpus']} {r['family']} s{r['seed']} | {r['off_label']} ({r['off_category']}) | {fmt(r.get('t96'))} | "
                 f"{fmt(r.get('v01'))} | {r['v1_flag']} | {', '.join(r['rescuers']) or '-'} | "
                 f"{ld.get('label')} ({ld.get('category')}): {'; '.join(ld.get('factors') or [])} | "
                 f"{'; '.join(r.get('off_factors') or []) or '-'} | {'; '.join(r.get('truth') or [])} |")
    F2 = [r for r in F if r["off_category_t95"] not in GOOD + ("abstain-ok",)]
    C2 = [r for r in res if r["off_category_t95"] in GOOD + ("abstain-ok",)]
    tm2 = [r for r in F2 if not r.get("off_factors")]
    L += ["", "## Under main's scoring (T95 equivalence on; rescues rescored the same way)", "",
          "Off failures that are no longer failures: "
          + (", ".join(f"{r['corpus']} {r['family']} s{r['seed']} ({r['off_label']} -> {r['off_category_t95']})"
                       for r in F if r not in F2) or "none")
          + f". Clean cases whose class changes: "
          + (", ".join(f"{r['corpus']} {r['family']} s{r['seed']} ({r['off_category']} -> {r['off_category_t95']})"
                       for r in C if r["off_category_t95"] != r["off_category"]) or "none") + ".", "",
          f"Failures: {len(F2)} ({len(F2) - len(tm2)} with factors, {len(tm2)} TIMEOUT); oracle ceiling "
          f"{sum(bool(r['rescuers_t95']) for r in F2)}/{len(F2)}; lower_degree rescues "
          f"{sum('lower_degree' in r['rescuers_t95'] for r in F2)}.", "",
          f"| detector | failures flagged (of {len(F2) - len(tm2)} with factors) | clean false alarms "
          f"| ceiling: flagged AND rescued (of {len(F2)}) | + TIMEOUT as trigger |", "|---|---|---|---|---|"]
    for name, f in (("T96 smooth_gof", lambda r: r.get("t96_fire")), ("V0.1 omnibus", lambda r: r.get("v01_fire")),
                    ("V0.1 validate flag", lambda r: r.get("v01_flag")), ("V1 (memo)", lambda r: r.get("v1_flag"))):
        fl = [r for r in F2 if f(r)]
        ce = sum(bool(r["rescuers_t95"]) for r in fl)
        L.append(f"| {name} | {len(fl)} | {sum(bool(f(r)) for r in C2)}/{len(C2)} | {ce}/{len(F2)} | "
                 f"{ce + sum(bool(r['rescuers_t95']) for r in tm2)}/{len(F2)} |")
    L += ["", "| case | off (T95 class) | T96 | V0.1 | rescuers (T95) | lower_degree (T95 class) |", "|---|---|---|---|---|---|"]
    L += [f"| {r['corpus']} {r['family']} s{r['seed']} | {r['off_label']} ({r['off_category_t95']}) | {fmt(r.get('t96'))} | "
          f"{fmt(r.get('v01'))} | {', '.join(r['rescuers_t95']) or '-'} | "
          f"{(r['lower_degree'] or {}).get('label')} ({r['lower_degree_t95']}) |" for r in F]
    q = lambda xs: (f"min {min(xs):.3g}, 5 % {np.quantile(xs, .05):.3g}, median {np.median(xs):.3g}" if xs else "-")
    L += ["", "Clean-case distributions (log10 p):", "",
          f"- T96: {q([r['t96'] for r in C if 't96' in r])}; fires on: "
          + (", ".join(f"{r['corpus']} {r['family']} s{r['seed']} ({r['off_label']}, {r['t96']:.3g})" for r in C if r.get('t96_fire')) or "none"),
          f"- V0.1 omnibus: {q([r['v01'] for r in C if 'v01' in r])}; fires on: "
          + (", ".join(f"{r['corpus']} {r['family']} s{r['seed']} ({r['off_label']}, {r['v01']:.3g})" for r in C if r.get('v01_fire')) or "none")]
    md = "\n".join(L) + "\n"
    (out / "cprime_trigger_p7.md").write_text(md, encoding="utf-8")
    print(md)


if __name__ == "__main__":
    main()
