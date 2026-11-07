"""benchmarks/p8_report.py on tiny synthetic rows (no method is run, no input data is built)."""
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "benchmarks"))

import p8_report as R  # noqa: E402


def _row(case, sampling, noise, method="pipeline", label="FIT-COMPATIBLE", ok=True, factors=None, **kw):
    r = dict(case=case, method=method, label=label, noise=noise, sampling=sampling, seed=0, factor_set=ok,
             struct_ok=ok, factors=factors if factors is not None else ["1.0*tau + 1.0*xi"], runtime=2.0,
             error=None)
    r.update(kw)
    return r


@pytest.mark.parametrize("row, want", [
    (_row("heat", "grid", 0.01, factors=["1.0*tau - 0.3*xi**2"]), "right"),
    (_row("heat", "grid", 0.01, label="UNDECIDED", ok=False), "abstain"),
    (_row("heat", "grid", 0.01, label="ID-KER", ok=False, all_ident=False), "abstain-ok"),
    (_row("heat", "grid", 0.01, ok=False, factors=["1.0*tau + 0.5"]), "false-confident"),
    (_row("heat", "grid", 0.01, method="weak_sindy", label="n/a", ok=False, factors=["1.0*tau + 0.5"]),
     "false-confident"),
    (_row("wave", "grid", 0.01, method="weak_sindy", label="n/a", ok=False, factors=["1.0*tau**2 - 1.0*xi**2"]),
     "equivalent"),
    (_row("heat", "grid", 0.01, label="SOMETHING", ok=False, factors=["1.0*tau + 0.5"]), "wrong"),
    (_row("heat", "grid", 0.01, ok=False, error="ValueError: boom"), "CRASH"),
])
def test_classify_p8(row, want):
    assert R.classify_p8(row) == want


def test_classify_e13(monkeypatch):
    import e13_summary

    monkeypatch.setattr(e13_summary, "equivalent", lambda row, m: m == "core")
    row = dict(family="F1", seed=0, noise=0.01, truth=["tau + xi"], all_ident=True,
               pipeline=dict(label="FIT-COMPATIBLE", factors=["tau + xi"], ok=True),
               core=dict(label="FIT-COMPATIBLE", factors=["tau"], ok=False),
               pdefind=dict(label="n/a", factors=["tau"], ok=False),
               weak_sindy=dict(label="CRASH", factors=[], ok=False),
               ensemble_sindy=dict(label="MISFIT", factors=["tau"], ok=False))
    got = {m: R.classify_e13(row, m) for m in R.E13_METHODS}
    assert got == dict(pipeline="right", core="equivalent", pdefind="false-confident", weak_sindy="CRASH",
                       ensemble_sindy="wrong")


def _write(p, rows):
    p.write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")
    return p


def test_build(tmp_path, monkeypatch):
    import e13_summary

    monkeypatch.setattr(e13_summary, "equivalent", lambda row, m: False)
    cells = R.P8_CELLS
    pipe = [_row(c, s, nz, factors=["1.0*tau - 0.3*xi**2"], cover90=1.0, ok=(c == "heat")) for c, nz, s, _ in cells]
    pipe.append(_row("heat", "400", 0.01))  # not a P8 cell: ignored
    run6 = [_row(c, s, nz, method=m, label="n/a", ok=(c == "heat"), factors=["1.0*tau + 0.5"])
            for m in R.BASELINES for c, nz, s, _ in cells]
    run6 += [_row(c, s, nz, label="UNDECIDED", ok=False) for c, nz, s, _ in cells]
    over = [_row("heat", "grid", 0.01, method="pdefind", label="n/a", ok=False, factors=["1.0*tau + 0.5"])]
    e13 = [dict(family="F1", seed=0, noise=0.01, truth=["tau + xi"], all_ident=True,
                pipeline=dict(label="FIT-COMPATIBLE", factors=["tau + xi"], ok=True),
                core=dict(label="CRASH", factors=[], ok=False))]
    a = R.parse(["--pipeline", str(_write(tmp_path / "p.jsonl", pipe)), "--sindy", str(_write(tmp_path / "s.jsonl", run6)),
                 "--sindy-override", str(_write(tmp_path / "o.jsonl", over)), "--ml", str(tmp_path / "missing.jsonl"),
                 "--e13", str(_write(tmp_path / "e.jsonl", e13)), "--e13-cache", str(tmp_path / "c.json")])
    md = R.build(a)
    assert "| pipeline + ML | pending |" in md
    # pipeline: 3 heat cells right, the 27 others false-confident (factors are heat's, not the case's)
    assert "| pipeline | 30/30 | 3 | 0 | 0 | 0 | 27 | 0 | 0 | 3 |" in md
    # the override turns pdefind heat grid 1 % into false-confident: 2 right
    assert "| pdefind | 30/30 | 2 | 0 | 0 | 0 | 28 |" in md
    assert "| pipeline (run 6) | 30/30 | 0 | 0 | 0 | 30 |" in md
    assert "| core | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |" in md
    assert "not independent" in md.lower()
    assert json.loads((tmp_path / "c.json").read_text())["F1-0-0.01-core"][0] == "CRASH"

    ml = [dict(r, method="pipeline_ml", layers=["L1", "L3"]) for r in pipe]
    a.ml = _write(tmp_path / "ml.jsonl", ml)
    md = R.build(a)
    assert "| pipeline + ML | 30/30 | 3 |" in md
    assert '["L1", "L3"]' in md


def test_ml_same_and_t96(tmp_path, monkeypatch):
    import e13_summary

    monkeypatch.setattr(e13_summary, "equivalent", lambda row, m: False)
    pipe = [_row(c, s, nz, factors=["1.0*tau - 0.3*xi**2"], ok=(c == "heat"),
                 smooth_gof=(-0.5 if s == "grid" else None), t96_downgraded=False) for c, nz, s, _ in R.P8_CELLS]
    k = next(i for i, r in enumerate(pipe) if r["case"] == "heat" and r["sampling"] == "grid")
    pipe[k].update(label="UNDECIDED", smooth_gof=-4.0, t96_downgraded=True)
    e13 = [dict(family="F1", seed=0, noise=0.01, truth=["tau + xi"], all_ident=True,
                pipeline=dict(label="UNDECIDED", factors=["tau + xi"], ok=True, smooth_gof=-5.0, t96_downgraded=True))]
    a = R.parse(["--pipeline", str(_write(tmp_path / "p.jsonl", pipe)), "--sindy", str(_write(tmp_path / "s.jsonl", [])),
                 "--sindy-override", str(tmp_path / "none.jsonl"), "--ml-same", "LB memo bit-identical",
                 "--e13", str(_write(tmp_path / "e.jsonl", e13))])
    md = R.build(a)
    assert "| pipeline + ML | 30/30 | 2 | 0 | 0 | 1 |" in md  # heat grid 1 % downgraded: abstain
    assert "= pipeline arm (LB memo bit-identical)" in md
    assert "Rows changed by T96: heat grid 1 %." in md
    assert "Right factors but abstained (factor_set true, label abstains; counted as abstain above): heat grid 1 %." in md
    assert "Rows changed by T96: F1-0." in md
    assert "F1-0 (UNDECIDED, T96)" in md
