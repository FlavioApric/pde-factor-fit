"""Controller C invariants (sessions/LEARNED/C/PLAN.md §8, tests T3-T11).

Logic tests stub the expensive pieces (run_config, diagnose, score) with fakes; the real-run tests use
a 32 x 64 heat grid (~20 s) and a pure-noise grid (instant).
"""
import numpy as np
import pytest

from pdefactor import loop
from pdefactor.learned import controller as C
from pdefactor.learned.memo import Memo, key
from pdefactor.learned.runconfig import DEFAULT, RunConfig


# ------------------------------------------------------------------ fixtures
def heat(noise=0.02, seed=3):
    from pdefactor.synthetic import any_case, grid

    t, x, u = grid(any_case("heat"), nt=32, nx=64)
    s = noise * np.std(u)
    return [u + s * np.random.default_rng(seed).standard_normal(u.shape)], t, x, s


def noise_grid(seed=11):
    from pdefactor.synthetic import grid

    t, x, _ = grid(lambda T, X: 0 * T, nt=32, nx=64)
    return [np.random.default_rng(seed).standard_normal((32, 64))], t, x, 1.0


class F:  # a fake factor: tau + c xi^2 (+ e xi)
    def __init__(self, c, e=0.0):
        self.coef = {(1, 0): (1.0, 1.0, 1.0), (0, 2): (c, c - 0.01, c + 0.01)}
        if e:
            self.coef[(0, 1)] = (e, e - 0.01, e + 0.01)
        self.status, self.W, self.kappa_support = "", 1.0, [1.0, 2.0]


def fake(factors, label="FIT-COMPATIBLE"):
    return loop.LoopResult(label, factors, {1: 1.0}, {((1, 2),): 1.0}, [], False, (3, 4), {label: 1.0})


class Never:
    name = "never"

    def choose(self, st):
        return None


# ------------------------------------------------------------------ T3
def test_never_acting_policy_returns_r0():
    S, t, x, s = heat()
    off = loop.run_loop(S, t, x, s)
    cr = C.run_controlled(S, t, x, s, policy=Never())
    assert cr.n_actions == 0 and not cr.changed
    assert cr.result.label == off.label and [str(q) for q in cr.result.pruned()] == [str(q) for q in off.pruned()]


# ------------------------------------------------------------------ T4
A_CONSTANTS = [("loop", n) for n in ("P_CONCENTRATED", "CAP", "PRED_LOGP", "EPS_GRID", "LOG_BF_STRONG")] + \
              [("bayes_split", "TAU2_GRID"), ("aggregate", "CONCENTRATION_GRID"), ("refine_raw", "Z90")]


def _snapshot():
    import importlib

    out = {}
    for mod, name in A_CONSTANTS:
        v = getattr(importlib.import_module(f"pdefactor.{mod}"), name)
        out[(mod, name)] = np.asarray(v).tobytes()
    return out


def test_frozen_scoring(monkeypatch):
    before = _snapshot()
    S, t, x, s = heat()
    monkeypatch.setattr(C, "early_stop", lambda r, f: None)
    C.run_controlled(S, t, x, s, policy=C.SequencePolicy(["wide_alternatives"]), max_loops=1)
    assert _snapshot() == before


# ------------------------------------------------------------------ T5
def test_fission_independent_and_seeded():
    S, t, x, s = noise_grid()  # pure N(0, 1) field: y = noise, sigma = 1
    case = C.Case(S, np.ones(1), t, x, 1.0, None, None, 1)
    a, b = C.fission(case, 123)
    a2, _ = C.fission(case, 123)
    assert np.array_equal(a.pool[0], a2.pool[0])
    assert np.allclose(a.pool[0] + b.pool[0], 2 * S[0])
    # y + Z and y - Z have covariance var(noise) - var(Z) = 0
    assert abs(np.corrcoef(a.pool[0].ravel(), b.pool[0].ravel())[0, 1]) < 0.05
    assert a.sigma == pytest.approx(np.sqrt(2)) and b.sigma == pytest.approx(np.sqrt(2))


# ------------------------------------------------------------------ T6
def _stub(monkeypatch, runs, scores):
    """run_config returns runs[cfg.key()] per fold (by sigma tag), diagnose always flags, score by fset."""
    def run_config(case, cfg, memo=None, explore=False, learned=None):
        return runs[cfg.key()]

    monkeypatch.setattr(C, "run_config", run_config)
    monkeypatch.setattr(C, "diagnose", lambda res, case, cfg: ({"ambiguous_structure"}, {}))
    monkeypatch.setattr(C, "early_stop", lambda r, f: None)
    monkeypatch.setattr(C, "base_band", lambda case: 4)
    monkeypatch.setattr(C, "score", lambda case, fs, kmax: scores(case, fs))


def test_confirm_required(monkeypatch):
    S, t, x, s = noise_grid()
    r0 = fake([F(0.3)])
    spur = fake([F(0.3), F(-1.0, 0.5)])
    c1 = C._delta("wide_alternatives", DEFAULT, None)
    folds = {}

    def scores(case, fs):  # the spurious set wins on fold A (where it was found) and loses on fold B
        tag = folds.setdefault(id(case), len(folds))
        return float(len(fs)) if tag == 0 else -float(len(fs))

    _stub(monkeypatch, {DEFAULT.key(): r0, c1.key(): spur}, scores)
    cr = C.run_controlled(S, t, x, s, policy=C.SequencePolicy(["wide_alternatives"]), max_loops=1)
    assert not cr.changed and C.fset(cr.result) == C.fset(r0)
    assert cr.confirmed.get("A->B") is False


def test_confirmed_both_ways_is_kept(monkeypatch):
    S, t, x, s = noise_grid()
    r0 = fake([F(0.3)])
    better = fake([F(0.3), F(-1.0, 0.5)])
    c1 = C._delta("wide_alternatives", DEFAULT, None)
    _stub(monkeypatch, {DEFAULT.key(): r0, c1.key(): better}, lambda case, fs: float(len(fs)))
    cr = C.run_controlled(S, t, x, s, policy=C.SequencePolicy(["wide_alternatives"]), max_loops=1)
    assert cr.changed and cr.accepted and cr.confirmed == {"A->B": True, "B->A": True}


def test_single_direction_is_not_enough(monkeypatch):
    S, t, x, s = noise_grid()
    r0 = fake([F(0.3)])
    better = fake([F(0.3), F(-1.0, 0.5)])
    c1 = C._delta("wide_alternatives", DEFAULT, None)
    folds = {}

    def scores(case, fs):  # fold B confirms, fold A does not
        tag = folds.setdefault(id(case), len(folds))
        return float(len(fs)) if tag == 1 else -float(len(fs))

    _stub(monkeypatch, {DEFAULT.key(): r0, c1.key(): better}, scores)
    cr = C.run_controlled(S, t, x, s, policy=C.SequencePolicy(["wide_alternatives"]), max_loops=1)
    assert not cr.changed


# ------------------------------------------------------------------ T7
def test_determinism():
    S, t, x, s = heat()
    pol = C.SequencePolicy(["narrow_band"])
    a = C.run_controlled(S, t, x, s, policy=pol, max_loops=1, trace=True)
    b = C.run_controlled(S, t, x, s, policy=pol, max_loops=1, trace=True)
    assert [x_[:4] for x_ in a.actions] == [x_[:4] for x_ in b.actions]
    assert a.result.label == b.result.label and a.result.note == b.result.note
    assert a.trace == b.trace and a.visited == b.visited


# ------------------------------------------------------------------ T8
def test_caps_and_no_repeats(monkeypatch):
    S, t, x, s = noise_grid()
    r0 = fake([F(0.3)])

    class AnyRun(dict):
        def __missing__(self, k):
            return r0

    _stub(monkeypatch, AnyRun(), lambda case, fs: 0.0)
    cr = C.run_controlled(S, t, x, s, policy=C.SequencePolicy(list(C.REMEDIES)), max_loops=4)
    per_fold = {}
    for fk, k, r, key_, _ in cr.actions:
        per_fold.setdefault(fk, []).append(r)
    assert all(len(v) <= 4 and len(set(v)) == len(v) for v in per_fold.values())
    cr = C.run_controlled(S, t, x, s, policy=C.SequencePolicy(list(C.REMEDIES)), max_loops=20, budget_s=0.0)
    assert cr.n_actions == 0 and "budget" in cr.stop_reason


# ------------------------------------------------------------------ T9
def test_early_stop_on_noise():
    S, t, x, s = noise_grid()
    cr = C.run_controlled(S, t, x, s, policy=C.SequencePolicy(list(C.REMEDIES)))
    assert cr.n_actions == 0 and "no modes" in cr.stop_reason
    assert cr.result.label != "FIT-COMPATIBLE"


def test_early_stop_margin():
    class R:
        factors, label, structures = [object()], "FIT-COMPATIBLE", {1: 1}

    assert "identifiability" in C.early_stop(R(), {"mode_margin": -2.0})
    assert C.early_stop(R(), {"mode_margin": 1.0}) is None


# ------------------------------------------------------------------ T10
def test_visited_report(monkeypatch):
    S, t, x, s = noise_grid()
    r0 = fake([F(0.3)])
    other = fake([F(0.3), F(-1.0, 0.5)])
    seq = ["wide_alternatives", "refine_budget"]
    c1 = C._delta(seq[0], DEFAULT, None)
    c2 = C._delta(seq[1], c1, None)
    _stub(monkeypatch, {DEFAULT.key(): r0, c1.key(): other, c2.key(): r0}, lambda case, fs: -float(len(fs)))
    cr = C.run_controlled(S, t, x, s, policy=C.SequencePolicy(seq), max_loops=2)
    # per fold the structures seen: r0 twice, other once -> 6 proposals, the 2-factor set seen twice
    # (once per fold) and r0's four times: no singleton, missing mass 0
    assert cr.missing_mass == pytest.approx(0.0)
    assert sum(cr.visited.values()) == pytest.approx(1 - cr.missing_mass)
    assert max(cr.visited, key=cr.visited.get) == str(loop._structure(r0.factors))


# ------------------------------------------------------------------ T11
def test_memo_exact():
    S, t, x, s = heat()
    m = Memo()
    a = loop.run_loop(S, t, x, s, bootstrap=0, _memo=m)
    n_miss = m.misses
    b = loop.run_loop(S, t, x, s, bootstrap=0, _memo=m)
    c = loop.run_loop(S, t, x, s, bootstrap=0)
    assert m.hits >= n_miss > 0 and m.misses == n_miss
    for r in (b, c):
        assert r.label == a.label and [str(q) for q in r.pruned()] == [str(q) for q in a.pruned()]
        assert r.note == a.note


def test_memo_key():
    a = np.arange(6.0).reshape(2, 3)
    assert key("run", a, x=1) == key("run", a.copy(), x=1)
    assert key("run", a, x=1) != key("run", a.T.copy(), x=1)
    assert key("run", a, x=1) != key("core", a, x=1)


def test_remedies_change_config():
    case = C.Case([np.zeros((2, 2))] * 16, np.ones(16), None, None, 0.0, None, "gp", 8)
    for r in C.REMEDIES:
        d = C._delta(r, DEFAULT, case)
        assert d is None or d.key() != DEFAULT.key(), r
    assert C._delta("more_samples", DEFAULT, case).n_samples == 16
    assert C._delta("more_samples", RunConfig(n_samples=16), case) is None


def test_fitted_policy_roundtrip():
    import pickle

    from pdefactor.learned.remedy import RemedyTable

    d = len(C.featurize(C.State(set(), {}, [], 0, DEFAULT, C.Case([0], np.ones(1), None, None, 1.0, None, None, 1),
                                0.0, np.inf)))
    z = np.zeros(d)
    good = C.LogitIso(z, 2.0, [], [], z, np.ones(d), harm=0.1)
    m = {"success": {"narrow_band": good}, "cost": {"narrow_band": C.Linear(z, 0.5, z, np.ones(d))}}
    fx = pickle.loads(pickle.dumps(C.Fitted("contextual", 0.2, models=m)))
    case = C.Case([np.zeros((4, 4))], np.ones(1), None, None, 1.0, None, None, 1)
    st = C.State({"undecided"}, {}, [], 0, DEFAULT, case, 0.0, np.inf)
    assert fx.policy().choose(st) == "narrow_band"
    assert fx.policy(banned=["narrow_band"]).choose(st) is None
    t = RemedyTable(default=C.DEFAULT_TABLE).fit([("undecided", "narrow_band", True)] * 30)
    assert C.Fitted("table", 0.0, table=t, cost={}).policy().choose(st) == "narrow_band"
