"""LB budget layer (sessions/LEARNED/LB/PLAN.md §4): skips are exact, noted, and risk-controlled."""
import numpy as np
import pytest
import sympy as sp

from pdefactor.learned import budget as B
from pdefactor.learned.config import Learned
from pdefactor.loop import FactorReport, _fp, _Steps, run_loop
from pdefactor.symbols import tau, xi


def _answer(r):
    coef = [{str(k): tuple(complex(c) for c in v) for k, v in f.coef.items()} for f in r.factors]
    return (r.label, [str(f.sympy) for f in r.factors], coef, _without_skip_note(r.note),
            sorted((str(k), v) for k, v in (r.structures or {}).items()))


def _without_skip_note(note):
    i = note.find("step(s) ")
    if i < 0:
        return note
    j = note.find("risk-controlled).", i) + len("risk-controlled).")
    return (note[:i] + note[j:]).replace("  ", " ").strip()


@pytest.fixture(scope="module")
def heat():
    from pdefactor.synthetic import any_case, grid

    t, x, u = grid(any_case("heat"))
    rng = np.random.default_rng(7)
    sig = 0.05 * np.std(u)
    return [u + sig * rng.standard_normal(u.shape)], t, x, sig


@pytest.fixture(scope="module")
def runs(heat):
    S, t, x, sig = heat
    B._CACHE["lb_exact"] = None
    off = run_loop(S, t, x, sig, bootstrap=4)
    log = run_loop(S, t, x, sig, bootstrap=4, learned=Learned(budget=True))
    B._CACHE.pop("lb_exact", None)
    return off, log


def _model(steps, lam):
    return B.BudgetModel(kind="constant", models={s: 0.5 for s in steps}, lam=lam)


# ------------------------------------------------------------------ the changed bit (parent's fix)
def _fr(c):
    return FactorReport(sympy=tau + c * xi ** 2, W=1.0, coef={(1, 0): (1, 1, 1), (0, 2): (c, c - 0.1, c + 0.1)})


def test_changed_sees_coefficients_at_same_count():
    log = _Steps()
    log.mark("a", "n", _fp(factors=[_fr(1.0)], label="FIT-COMPATIBLE"))
    log.mark("b", "n", _fp(factors=[_fr(1.0)], label="FIT-COMPATIBLE"))
    log.mark("c", "n", _fp(factors=[_fr(1.5)], label="FIT-COMPATIBLE"))  # same count, new coefficient
    log.mark("d", "n", _fp(factors=[_fr(1.5)], label="ID-KER"))          # same factors, new label
    assert [r[2] for r in log.rows] == [False, False, True, True]


def test_changed_nan_is_stable():
    f = FactorReport(sympy=tau, W=float("nan"), coef={(1, 0): (complex("nan"), 1, 1)})
    log = _Steps()
    log.mark("a", "", _fp(factors=[f]))
    log.mark("b", "", _fp(factors=[f]))
    assert log.rows[1][2] is False


# ------------------------------------------------------------------ the layer
def test_log_only_mode_is_off(runs):
    off, log = runs
    assert _answer(log) == _answer(off)
    assert log.lb["skipped"] == [] and log.lb["features"]
    assert off.lb == {}
    for feats in log.lb["features"].values():
        assert set(feats) == set(B.FEATURES)


def test_never_skip_model_is_off(heat, runs):
    S, t, x, sig = heat
    off, _ = runs
    B._CACHE["lb_exact"] = _model(B.STEPS, lam=-1.0)
    try:
        on = run_loop(S, t, x, sig, bootstrap=4, learned=Learned(budget=True))
    finally:
        B._CACHE.pop("lb_exact", None)
    assert _answer(on) == _answer(off) and on.note == off.note


def test_exact_skip_of_unchanged_steps(heat, runs):
    """C1: a guarded step that logged changed = False is skipped with a bit-identical answer, and the
    skip is written into the note and the lb record."""
    S, t, x, sig = heat
    off, log = runs
    ch = {}
    for name, _, c in log.steps:
        ch[name] = ch.get(name, False) or c
    quiet = [s for s in log.lb["features"] if not ch.get(s, True)]
    assert quiet, "the heat draw should have at least one guarded step that changes nothing"
    B._CACHE["lb_exact"] = _model(quiet, lam=0.5)
    try:
        on = run_loop(S, t, x, sig, bootstrap=4, learned=Learned(budget=True))
    finally:
        B._CACHE.pop("lb_exact", None)
    assert sorted(on.lb["skipped"]) == sorted(quiet)
    assert "skipped by the LB budget layer" in on.note
    assert _answer(on) == _answer(off)
    # C2: the replay of the log row predicts no harm for this model
    row = dict(steps=log.steps, lb=log.lb)
    L, saved = B.replay(_model(quiet, 0.5), [row])
    assert L[0] == 0 and saved[0] >= 0


def test_children_never_consult_the_layer(heat):
    S, t, x, sig = heat
    B._CACHE["lb_exact"] = _model(B.STEPS, lam=2.0)
    try:
        r = run_loop(S, t, x, sig, grow=False, learned=Learned(budget=True), _depth=1)
    finally:
        B._CACHE.pop("lb_exact", None)
    assert r.lb == {} and "LB budget" not in r.note


# ------------------------------------------------------------------ risk control (synthetic)
def _scores(rng, n, p_bad=0.1):
    out = []
    for _ in range(n):
        p = rng.uniform()
        y = int(rng.uniform() < p * p_bad * 2)
        out.append([(p, y, 1.0)])
    return out


def test_crc_rule_and_monotone_loss():
    rng = np.random.default_rng(0)
    sc = _scores(rng, 400)
    lam = B.crc_threshold(sc, 0.02)
    n = len(sc)
    L, _ = B.loss_at(sc, lam)
    assert (n * L.mean() + 1) / (n + 1) <= 0.02
    nxt = min(p for s in sc for p, _, _ in s if p > lam)
    L2, _ = B.loss_at(sc, nxt)
    assert (n * L2.mean() + 1) / (n + 1) > 0.02
    grid = np.linspace(0, 1, 21)
    risks = [B.loss_at(sc, g)[0].mean() for g in grid]
    assert all(a <= b for a, b in zip(risks, risks[1:]))


def test_crc_needs_enough_runs():
    sc = [[(0.0, 0, 1.0)]] * 40  # zero loss, but (0 + 1) / 41 > 0.02
    assert B.crc_threshold(sc, 0.02) == -1.0
    sc = [[(0.0, 0, 1.0)]] * 60
    assert B.crc_threshold(sc, 0.02) == 0.0


def test_ltt_is_stricter_than_crc():
    rng = np.random.default_rng(1)
    sc = _scores(rng, 300)
    assert B.ltt_threshold(sc, 0.02, 0.1) <= B.crc_threshold(sc, 0.02)
    assert B.ltt_threshold([[(0.0, 0, 1.0)]] * 100, 0.02, 0.1) == -1.0  # 0.98^100 > 0.1
    assert B.ltt_threshold([[(0.0, 0, 1.0)]] * 120, 0.02, 0.1) == 0.0   # 0.98^120 < 0.1


def test_crc_matches_validator_rule():
    """Same rule as validator._risk_threshold (one set member per run: the step's change)."""
    from pdefactor.learned.validator import _risk_threshold

    rng = np.random.default_rng(2)
    sc = _scores(rng, 300)
    # validator runs {j: P_j >= lam}; a run is a miss when its changed step is not run, i.e. skipped
    # (P < lam). With P = p_change both rules pick the same skip set (strict vs non-strict grid point).
    P = np.array([[s[0][0]] for s in sc])
    Y = np.array([[s[0][1]] for s in sc])
    lam_v = _risk_threshold(P, Y, 0.02)
    lam = B.crc_threshold(sc, 0.02)
    Lb, _ = B.loss_at(sc, lam)
    Lv = ((P < lam_v) & (Y == 1)).any(1)
    assert Lb.sum() == Lv.sum()


# ------------------------------------------------------------------ features
class _Agg:
    def __init__(self):
        self.structures_pooled = {((1, 2),): 0.7, ((1, 1),): 0.3}
        self.labels = {"FIT-COMPATIBLE": 0.8, "UNDECIDED": 0.2}
        self.dp = None
        self.k_structure = {1: 1.0}


def test_features_dimensionless_and_nan_safe():
    rng = np.random.default_rng(3)
    u = rng.standard_normal((32, 64))
    f1 = B.features("recurse", agg=_Agg(), bounds=(3, 4), sigma=0.1, samples=[u], rows=[("grow", 1.0, False)])
    f2 = B.features("recurse", agg=_Agg(), bounds=(3, 4), sigma=0.1 * 7.3, samples=[7.3 * u],
                    rows=[("grow", 99.0, False)])
    for k in B.FEATURES:
        a, b = f1[k], f2[k]
        assert (np.isnan(a) and np.isnan(b)) or a == pytest.approx(b), k
    assert np.isnan(f1["lp"]) and np.isnan(f1["ch_decide"]) and f1["ch_grow"] == 0.0
    m = B.fit([], kind="hgb")
    assert m.models == {}


# ------------------------------------------------------------------ LB memo (core change: tested here)
def _struct_answer(r):
    return (r.label, [str(f.sympy) for f in r.factors], [float(f.weight) for f in r.factors],
            repr(r.structures), repr(r.confluent), repr(r.gamma), repr(r.info.get("reason")))


def test_core_cache_is_exact(heat):
    from pdefactor.core.structfit import analyze_structured

    S, t, x, sig = heat
    ref = analyze_structured(S[0], t, x, noise=sig, want_components=True)
    from pdefactor.learned.memo import Memo

    cache = Memo()
    a = analyze_structured(S[0], t, x, noise=sig, want_components=True, cache=cache)
    assert len(cache) == 1
    b = analyze_structured(S[0], t, x, noise=sig, want_components=True, cache=cache)  # hit
    c = analyze_structured(S[0], t, x, noise=sig, m_max=2, dx_max=2, want_components=True, cache=cache)
    c_ref = analyze_structured(S[0], t, x, noise=sig, m_max=2, dx_max=2, want_components=True)
    assert len(cache) == 1
    assert _struct_answer(a) == _struct_answer(ref) == _struct_answer(b)
    assert _struct_answer(c) == _struct_answer(c_ref)
    d = analyze_structured(S[0] * 1.0001, t, x, noise=sig, cache=cache)  # other data: a new key
    assert len(cache) == 2 and d.label


def test_memo_is_released_after_the_call(heat):
    from pdefactor.learned.runconfig import memo

    S, t, x, sig = heat
    B._CACHE["lb_exact"] = None
    try:
        run_loop(S, t, x, sig, grow=False, recurse=False, split=False, learned=Learned(budget=True))
    finally:
        B._CACHE.pop("lb_exact", None)
    assert memo() is None


def _harm_rows():
    base = dict(corpus="G", family="F1", split="test", design=["grid", 0.01], coef={"a": [1.0, 2.0]})
    off = [dict(base, seed=i, learned="off", label="FIT-COMPATIBLE", factors=["D_t - D_x**2"]) for i in range(4)]
    lb = [dict(r, learned="lb") for r in off]
    lb[1] = dict(lb[1], factors=["D_t"])                     # harmed: factor set differs
    lb[2] = dict(lb[2], coef={"a": [1.0, 2.0 + 1e-6]})       # not harmed, coefficient differs
    off[3] = dict(off[3], label="TIMEOUT")                   # a skip turned a timeout into an answer
    return off + lb


def test_harm_check_counts():
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "benchmarks" / "ml_layers"))
    import ll_budget_harm as H

    r = H.compare(_harm_rows())
    assert (r["n_pairs"], r["n_compared"], r["n_harmed"], r["n_coef_diff"]) == (4, 3, 1, 1)
    assert len(r["stop_changed"]) == 1 and r["harmed_cp95"] > r["harmed_rate"]
    assert H.cp_upper(0, 150) < 0.02 < H.cp_upper(0, 100)


def test_zero_harm_rule():
    # one run harmed at p = 0.3; the zero rule stops just below it, the bound is the 0-of-n bound
    sc = [[(0.1, 0, 5.0)], [(0.2, 0, 5.0)], [(0.3, 1, 5.0)], [(0.4, 0, 5.0)]]
    assert B.zero_threshold(sc) == 0.2
    assert B.zero_threshold([[(0.1, 1, 1.0)]]) == -1.0
    assert abs(B.zero_bound(100) - 0.0295) < 1e-3 and B.zero_bound(100) <= 3 / 100


def test_profiles():
    assert B.model_name(True) == B.model_name("exact") == "lb_exact" and B.model_name("fast") == "lb_fast"
    Learned(budget="fast")
    with pytest.raises(ValueError):
        Learned(budget="turbo")
