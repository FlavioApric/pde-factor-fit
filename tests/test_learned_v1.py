"""V1 failure detector and the report-only hook (sessions/LEARNED/V1/PLAN.md 2.1)."""
import json
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).parent / "data"))
import make_learned_off_golden as G  # noqa: E402

from pdefactor.learned import validator as V  # noqa: E402
from pdefactor.learned.config import Learned  # noqa: E402
from pdefactor.learned.ptop import PTopCalibrator  # noqa: E402

GOLD = json.loads(G.OUT.read_text()) if G.OUT.exists() else {}


def test_featurise_shape_and_empty_row():
    for resid in (True, False):
        v = V.featurise({}, resid=resid)
        assert v.shape == (len(V.feature_names(resid)),)
    row = {"v0": {"v01_omnibus_z": 3.0}, "resid": {"acf1_t": 0.5}, "label": "MISFIT", "design": [400, 0.05],
           "steps": [["core", 2.0, True], ["refine", 2.0, False]], "export": [{"log_snr": 1.0}, {"log_snr": 3.0}]}
    v = dict(zip(V.feature_names(), V.featurise(row)))
    assert v["v0:v01_omnibus_z"] == 3.0 and v["resid:acf1_t"] == 0.5
    assert v["label:MISFIT"] == 1.0 and v["design:scattered"] == 1.0
    assert v["step:core_changed"] == 1.0 and v["step:refine_changed"] == 0.0
    assert not any(n.endswith("_frac") for n in V.feature_names())  # wall-time fractions are a pipeline shortcut
    assert v["export:log_snr_min"] == 1.0 and v["export:log_snr_mean"] == 2.0


def _synthetic(n, rng, types=("a", "b", "c")):
    """Clean runs ~ N(0, I); failure type k shifts feature k."""
    Xc = rng.normal(size=(n, 6))
    Xf, tf = [], []
    for k, t in enumerate(types):
        X = rng.normal(size=(n // len(types), 6))
        X[:, k] += 3.0
        Xf.append(X)
        tf += [t] * len(X)
    return Xc, np.vstack(Xf), np.array(tf)


def test_conformal_false_alarm_is_controlled():
    rng = np.random.default_rng(0)
    Xc, Xf, tf = _synthetic(600, rng)
    det = V.FailureDetector(alpha=0.05).fit(np.vstack([Xc, Xf]), np.r_[np.zeros(len(Xc)), np.ones(len(Xf))], None)
    Xcal, _, _ = _synthetic(400, rng)
    det.calibrate(Xcal)
    fa = np.mean([det.flag(rng.normal(size=(400, 6))).mean() for _ in range(10)])
    assert fa <= 0.05 + 2 * np.sqrt(0.05 * 0.95 / 4000)
    _, Xt, _ = _synthetic(400, rng)
    assert det.flag(Xt).mean() > 0.5


def test_open_set_reports_other_for_an_unseen_type():
    rng = np.random.default_rng(1)
    Xc, Xf, tf = _synthetic(900, rng)
    seen = tf != "c"
    X = np.vstack([Xc, Xf[seen]])
    y = np.r_[np.zeros(len(Xc)), np.ones(seen.sum())]
    det = V.FailureDetector().fit(X, y, np.r_[[None] * len(Xc), tf[seen]])
    Xc2, Xf2, tf2 = _synthetic(600, rng)
    det.calibrate(Xc2, Xf2[tf2 != "c"], tf2[tf2 != "c"])
    seen_t = det.type_of(Xf2[tf2 == "a"])
    assert np.mean([t == "a" for t in seen_t]) > 0.8
    unseen = det.type_of(Xf2[tf2 == "c"])
    assert np.mean([t in ("a", "b") for t in unseen]) < 0.5  # mostly "other", rarely a confident wrong type


@pytest.fixture
def models(tmp_path, monkeypatch):
    import joblib

    rng = np.random.default_rng(2)
    n = len(V.feature_names())
    X = rng.normal(size=(200, n))
    y = (X[:, 0] > 1).astype(int)
    det = V.FailureDetector().fit(X, y, np.where(y == 1, np.where(X[:, 1] > 0, "a", "b"), None))
    det.calibrate(X[y == 0])
    joblib.dump(det, tmp_path / "v1.joblib")
    p = rng.random(200)
    joblib.dump(PTopCalibrator("temperature").fit(p, rng.random(200) < p), tmp_path / "ptop.joblib")
    monkeypatch.setattr(V, "MODEL_DIR", tmp_path)
    return tmp_path


@pytest.mark.skipif(not GOLD, reason="golden file missing")
@pytest.mark.parametrize("name", ["heat-grid-0.05", "heat-400-0.05", "pure-noise-grid"])
def test_flags_on_change_only_the_report(name, models):
    """Labels, factors, intervals, structures, weights unchanged; only learned_report and note lines."""
    inputs = G.inputs()
    if name not in inputs:
        pytest.skip("input cache missing")
    got = G.run(name, inputs[name], Learned(validator=True, prob_calibration=True))
    ref = GOLD[name]
    note_ref = ref["note"]
    assert got["note"].startswith(note_ref)
    got["note"] = note_ref
    sys.path.insert(0, str(Path(__file__).parent))
    from test_learned_off import _same

    _same(got, ref)


def test_report_fields(models):
    from pdefactor.loop import run_loop
    from pdefactor.simulator import random_pde
    from pdefactor.synthetic import grid

    d = random_pde("F1", 0)
    t, x, u = grid(d.field)
    un = u + 0.05 * np.std(u) * np.random.default_rng(0).standard_normal(u.shape)
    off = run_loop([un], t, x, 0.05 * np.std(u), bootstrap=0)
    on = run_loop([un], t, x, 0.05 * np.std(u), bootstrap=0, learned=Learned(validator=True, prob_calibration=True))
    assert off.learned_report is None
    assert set(on.learned_report) == {"v1", "ptop"}
    assert 0 <= on.learned_report["v1"]["p_value"] <= 1
    assert 0 <= on.learned_report["ptop"]["p_top_calibrated"] <= 1
    assert on.label == off.label and [str(f.sympy) for f in on.factors] == [str(f.sympy) for f in off.factors]


def test_resid_logp_floored_as_v0():
    v = dict(zip(V.feature_names(), V.featurise({"resid": {"lb_t_logp": -np.inf, "bp_logp": -12.0}})))
    assert v["resid:lb_t_logp"] == -300.0 and v["resid:bp_logp"] == -12.0 and np.isnan(v["resid:acf1_t"])


class _AlwaysFlag:
    """Stub detector: flags every run (p = 0)."""
    resid, designs, tag, alpha = True, ("grid", "scattered"), "stub", 0.05

    def report(self, x):
        return {"p_failure": 1.0, "p_value": 0.0, "flag": True, "type": None, "alpha": self.alpha, "tag": self.tag}


def test_downgrade_only_turns_fit_compatible_into_undecided(monkeypatch):
    """validator="downgrade": a flagged FIT-COMPATIBLE run becomes UNDECIDED with the same factors;
    validator=True never changes the label; a non-flagged run is never changed (never an upgrade)."""
    from pdefactor.loop import run_loop
    from pdefactor.simulator import random_pde
    from pdefactor.synthetic import grid

    d = random_pde("F1", 0)
    t, x, u = grid(d.field)
    sig = 0.05 * np.std(u)
    un = u + sig * np.random.default_rng(0).standard_normal(u.shape)
    off = run_loop([un.copy()], t, x, sig, bootstrap=0)
    assert off.label == "FIT-COMPATIBLE"
    monkeypatch.setattr(V, "load_model", lambda name: _AlwaysFlag() if name == "v1.joblib" else None)
    rep = run_loop([un.copy()], t, x, sig, bootstrap=0, learned=Learned(validator=True))
    assert rep.label == off.label
    dn = run_loop([un.copy()], t, x, sig, bootstrap=0, learned=Learned(validator="downgrade"))
    assert dn.label == "UNDECIDED" and dn.learned_report["v1"]["downgraded"]
    assert [str(f.sympy) for f in dn.factors] == [str(f.sympy) for f in off.factors]
    stub = _AlwaysFlag()
    stub.report = lambda x: {"p_failure": 0.0, "p_value": 1.0, "flag": False, "type": None, "alpha": 0.05, "tag": "s"}
    monkeypatch.setattr(V, "load_model", lambda name: stub if name == "v1.joblib" else None)
    nf = run_loop([un.copy()], t, x, sig, bootstrap=0, learned=Learned(validator="downgrade"))
    assert nf.label == off.label


def test_validator_values_checked():
    with pytest.raises(ValueError):
        Learned(validator="upgrade")
