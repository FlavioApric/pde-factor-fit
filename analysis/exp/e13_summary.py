"""Summary of E13 (random PDEs by family) with abstention-aware scoring (PHASE4 P0.2).

Per method and family:
  right            right factor set (simulator.match, scale-aware)
  correct-abstain  ID-KER / UNDECIDED where some true factor is not resolvable at this noise
  false-confident  FIT-COMPATIBLE with a wrong set (SINDy has no labels: every wrong answer counts)
  score            right + correct-abstain, over all draws
Resolvable draws are also reported alone (right among them), since there the answer is in the data.
Usage: python e13_summary.py [jsonl] > md
"""
import json
import os
import sys

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[2] / "src"))
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ABSTAIN = {"ID-KER", "UNDECIDED"}


DCHI2_EQUIV = 25.0  # scoring choice: ~99 % point of chi^2 with ~10 df (the parameters of a 2-factor law)
# T95 (adopted 2026-10-31 after the rescored fc / E13 A/B; env PDEFACTOR_EQUIV_DF=0 restores the all-bin gap): the chi^2 gap of the
# equivalence test is taken over the excited band only (largest bin with data energy above noise, the
# data-only test of T77, + 2) and minus the gap in degrees of freedom. A law with more kernel columns
# lowers chi^2 by about 2 per column in every bin by fitting noise (Cochran: E chi^2 = df), so the raw gap
# over all 64 bins charged a lower-order law ~2 per empty bin (F5-131 grid 5 %: raw gap 139, of which 136 in
# the 61 empty bins, Delta df 127; in the excited bins 3.0). Gap - Delta df estimates the non-centrality,
# i.e. the signal one law explains and the other does not, which is what 'data-equivalent' means.
EQUIV_DF = os.environ.get("PDEFACTOR_EQUIV_DF", "1") == "1"


def chi2_gap(facs, truth, u, t, x, sig):
    """V0.1 chi^2 of `facs` minus that of `truth` on the grid u (the equivalence statistic, compared with
    DCHI2_EQUIV). EQUIV_DF: over |kappa| <= excited band + 2 and minus the degrees-of-freedom gap
    (an unbiased estimate of the non-centrality for nested kernels)."""
    import numpy as np

    from pdefactor.validate import predictive_bins

    kmax = None
    if EQUIV_DF:
        from pdefactor.refine_raw import _excited_bins

        u = np.asarray(u)
        nx = u.shape[1]
        g = dict(t=np.asarray(t) - t[0], nx=nx, Y=np.fft.fft(u, axis=1) / np.sqrt(nx))
        exc = _excited_bins(g, nx // 2 - 1, bool(np.isrealobj(u)), float(sig))
        period = (x[1] - x[0]) * nx
        kmax = 2 * np.pi * ((max(abs(b) for b in exc) if exc else 0) + 2) / period + 1e-9
    bf = predictive_bins(facs, u, t, x, sig, kmax=kmax)
    bt = predictive_bins(truth, u, t, x, sig, kmax=kmax)
    gap = sum(b[1] for b in bf) - sum(b[1] for b in bt)
    if EQUIV_DF:
        gap -= sum(b[2] for b in bf) - sum(b[2] for b in bt)
    return float(gap)

_DATA = {}


def _data(row):
    """The draw's noisy grid, regenerated exactly as in e13_random_pdes.run_one."""
    import numpy as np

    from pdefactor.simulator import random_pde
    from pdefactor.synthetic import grid

    key = (row["family"], row["seed"], row["noise"])
    if key not in _DATA:
        d = random_pde(row["family"], row["seed"])
        t, x, u = grid(d.field)
        rng = np.random.default_rng(1000 + row["seed"])
        sig = row["noise"] * np.std(u)
        _DATA[key] = (t, x, u + sig * rng.standard_normal(u.shape), sig, d)
    return _DATA[key]


def equivalent(row, m):
    """Same product polynomial as the truth, or explains the data as well as the truth (V0.1 chi^2
    excess <= DCHI2_EQUIV): a factorisation or support the data do not distinguish from the truth."""
    import sympy as sp

    from pdefactor.simulator import match

    facs = [sp.sympify(q) for q in row[m]["factors"]]
    if not facs:
        return False
    tr = [sp.sympify(q) for q in row["truth"]]
    if match([sp.expand(sp.Mul(*tr))], [sp.expand(sp.Mul(*facs))])[0]:
        return True
    t, x, un, sig, _ = _data(row)
    try:
        gap = chi2_gap(facs, tr, un, t, x, sig)
    except Exception:  # noqa: BLE001  (a factor the root finder cannot handle is not equivalent)
        return False
    return gap <= DCHI2_EQUIV


def classify(row, m):
    r = row[m]
    if r["ok"]:
        return "right"
    if equivalent(row, m):
        return "equivalent"
    lab = r["label"]
    if lab in ABSTAIN or (lab.startswith("ID-KER")):
        return "abstain-ok" if not row["all_ident"] else "abstain"
    if lab in ("FIT-COMPATIBLE", "n/a"):
        return "false-confident"
    return "other"


def main(path):
    rows = [json.loads(line) for line in Path(path).read_text().splitlines() if line.strip()]
    methods = [m for m in ("core", "pipeline", "pdefind", "weak_sindy", "ensemble_sindy") if any(m in r for r in rows)]
    fams = sorted({r["family"] for r in rows})
    print(f"# E13 random PDEs ({len(rows)} draws, noise {sorted({r['noise'] for r in rows})})\n")
    print("Cells: right / correct-abstain / false-confident (n); last column: right among resolvable draws.\n")
    print("| method | " + " | ".join(fams) + " | all | resolvable: right |")
    print("|---" * (len(fams) + 3) + "|")
    for m in methods:
        cells, tot = [], defaultdict(int)
        for f in fams + [None]:
            sub = [r for r in rows if m in r and (f is None or r["family"] == f)]
            c = defaultdict(int)
            for r in sub:
                c[classify(r, m)] += 1
            cells.append(f"{c['right']}+{c['equivalent']}/{c['abstain-ok']}/{c['false-confident']} ({len(sub)})")
        res = [r for r in rows if m in r and r["all_ident"]]
        cells.append(f"{sum(r[m]['ok'] for r in res)}/{len(res)}")
        print(f"| {m} | " + " | ".join(cells) + " |")
    print("\n## Per draw (pipeline)\n")
    for r in rows:
        if "pipeline" in r:
            p = r["pipeline"]
            print(f"- {r['family']}-{r['seed']} {'resolvable' if r['all_ident'] else 'NOT resolvable'}: "
                  f"truth {r['truth']} -> {p['label']} {p['factors']} ({classify(r, 'pipeline')})")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ROOT / "benchmarks" / "out" / "e13_random.jsonl")
