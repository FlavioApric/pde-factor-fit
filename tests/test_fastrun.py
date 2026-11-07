"""fastrun (sessions/LEARNED/SPEEDUP.md): the general fast-evaluation harness for corpus runs.
Pieces tested without running the pipeline: the anytime-valid confidence sequence, the stratified LPT
order, the online runtime model, reuse by key and code sha, and the stop decision."""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "analysis" / "exp"))

import fastrun as fr  # noqa: E402


def test_cs_shrinks_on_identical_pairs():
    cs = fr.ConfSeq(alpha=0.05)
    for _ in range(30):
        cs.update(0.0)
    lo, hi = cs.interval()
    assert lo <= 0.0 <= hi and hi - lo < 0.3


def test_cs_detects_clear_gain():
    cs = fr.ConfSeq(alpha=0.05)
    for _ in range(15):
        cs.update(1.0)
    assert cs.interval()[0] > 0


def test_cs_coverage_under_optional_stopping():
    rng = np.random.default_rng(0)
    miss = 0
    reps = 300
    for _ in range(reps):
        cs = fr.ConfSeq(alpha=0.1)
        bad = False
        for _ in range(60):  # true mean 0.1 of differences in {-1, 0, 1}
            cs.update(float(rng.choice([-1, 0, 1], p=[0.1, 0.7, 0.2])))
            lo, hi = cs.interval()
            bad |= not (lo <= 0.1 <= hi)  # looked at every step: still covered
        miss += bad
    assert miss / reps <= 0.1


def test_order_stratified_prefix_and_pairs_adjacent():
    tasks = [("G", f, s, ("grid", 0.01), a) for f in ("F1", "F2", "F3") for s in range(4) for a in ("off", "on")]
    order = fr.order(tasks, fr.RuntimeModel(), seed=0)
    assert sorted(order) == sorted(tasks)
    cases = []
    for t in order:
        c = t[:4]
        if not cases or cases[-1] != c:
            cases.append(c)
    assert len(cases) == 12  # the arms of a case run back to back
    for k in range(1, 5):
        fams = [c[1] for c in cases[: 3 * k]]
        assert all(fams.count(f) == k for f in ("F1", "F2", "F3"))  # every prefix round is balanced


def test_runtime_model_learns_and_roundtrips(tmp_path):
    rows = [dict(corpus=c, family=f, design=[d, 0.05], learned="off", runtime=rt, label="UNDECIDED")
            for c, rt in (("N", 2.0), ("S", 300.0)) for f in ("F1", "F2") for d in (400, 2000)]
    m = fr.RuntimeModel().fit(rows)
    assert m.predict(("S", "F1", 7, (400, 0.05), "off")) > 10 * m.predict(("N", "F1", 7, (400, 0.05), "off"))
    p = tmp_path / "rt.json"
    m.save(p)
    m2 = fr.RuntimeModel.load(p)
    key = ("S", "F2", 1, (2000, 0.05), "off")
    assert abs(m2.predict(key) - m.predict(key)) < 1e-9
    # an unseen arm / corpus falls back to the broader groups, never fails
    assert m2.predict(("Z", "F9", 1, ("grid", 0.5), "new_arm")) > 0
    # online update moves the prediction toward new evidence
    before = m2.predict(key)
    for _ in range(20):
        m2.update(dict(corpus="S", family="F2", design=[2000, 0.05], learned="off", runtime=3000.0, label="X"))
    assert m2.predict(key) > before


def test_reuse_by_key_and_sha(tmp_path):
    f = tmp_path / "old.jsonl"
    good = dict(corpus="G", family="F1", seed=1, design=["grid", 0.01], learned="off", label="ID-KER", code_sha="abc")
    stale = dict(good, seed=2, code_sha="old")
    legacy = {k: v for k, v in dict(good, seed=3).items() if k != "code_sha"}
    f.write_text("\n".join(json.dumps(r) for r in (good, stale, legacy)) + "\n")
    idx = fr.ReuseIndex([f], sha="abc", accept_nosha=False)
    assert idx.get(("G", "F1", 1, ("grid", 0.01), "off"))["label"] == "ID-KER"
    assert idx.get(("G", "F1", 2, ("grid", 0.01), "off")) is None  # other pipeline version
    assert idx.get(("G", "F1", 3, ("grid", 0.01), "off")) is None  # no sha: only with accept_nosha
    assert fr.ReuseIndex([f], sha="abc", accept_nosha=True).get(("G", "F1", 3, ("grid", 0.01), "off"))


def test_stop_rule():
    g = fr.SeqGate(arm="on", base="off", alpha=0.05, delta=0.1, min_pairs=10)
    row = lambda s, a, cat: dict(corpus="G", family="F1", seed=s, design=["grid", 0.01], learned=a, category=cat)
    for s in range(70):
        g.add(row(s, "off", "right"))
        g.add(row(s, "on", "right"))
    v = g.verdict()
    assert v["stop"] and v["reason"] == "no gain"  # identical arms: futility (about 55 pairs at delta 0.1)
    g2 = fr.SeqGate(arm="on", base="off", alpha=0.05, delta=0.05, min_pairs=10)
    for s in range(40):
        g2.add(row(s, "off", "abstain-ok"))
        g2.add(row(s, "on", "false-confident" if s % 2 else "abstain-ok"))
    assert g2.verdict()["reason"] == "harm"


def test_slot_reservation(tmp_path):
    import slots

    a = slots.Pool(total=3, directory=tmp_path, tag="other")
    b = slots.Pool(total=3, directory=tmp_path, tag="lb")
    (tmp_path / "reserve.json").write_text('{"tag": "lb", "n": 2}')
    assert a.try_acquire() is not None  # 3 free, 2 reserved: one left for others
    assert a.try_acquire() is None
    assert b.try_acquire() is not None and b.try_acquire() is not None
    assert b.try_acquire() is None  # pool full
    assert (tmp_path / "slot0").read_text().split()[1] == "other"
