"""P3: growth past M_LIMIT / DX_LIMIT (env PDEFACTOR_GROW_PAST, off by default) and conjugate
orientation for n_pairs >= 2 in _canonical_conj_reports. Fast: the core runs are mocked."""
from types import SimpleNamespace

import numpy as np
import sympy as sp

from pdefactor import loop as L
from pdefactor.symbols import tau, xi


def test_grow_past_is_off_by_default():
    import os
    if os.environ.get("PDEFACTOR_GROW_PAST") is None:
        assert L.GROW_PAST is False


def test_grow_past_options_respect_the_hard_cap():
    assert L._grow_options((L.M_LIMIT, L.DX_LIMIT)) == []
    o = L._grow_past_options((L.M_LIMIT, L.DX_LIMIT))
    assert set(o) == {(L.M_LIMIT, L.DX_LIMIT + 1), (L.M_LIMIT + 1, L.DX_LIMIT)}
    capped = (L.M_LIMIT + L.GROW_PAST_M, L.DX_LIMIT + L.GROW_PAST_DX)
    assert L._grow_past_options(capped) == []


def test_accept_past_needs_both_v01_gain_and_evidence():
    cur, p = 100.0, 6
    assert L._accept_past(-10.0, -5.0, 105.0, 8, cur, p)          # V0.1 +5 decades, evidence +5 nats
    assert not L._accept_past(-10.0, -8.0, 105.0, 8, cur, p)      # V0.1 gain under 3 decades
    assert not L._accept_past(-10.0, -5.0, 100.5, 8, cur, p)      # within the bare-mention gap, more params
    assert not L._accept_past(-10.0, -5.0, None, 8, cur, p)       # no score: never
    assert not L._accept_past(-10.0, -5.0, 105.0, 8, None, p)


def _mock(monkeypatch, lp_of, sc_of):
    """_run returns a tag per bounds; _pred_logp / _level_score read it from the tag."""
    monkeypatch.setattr(L, "_run", lambda s, p, t, x, sig, b, r, **kw: ([("res", b)], SimpleNamespace(b=b)))
    monkeypatch.setattr(L, "_attach", lambda r, s: None)
    monkeypatch.setattr(L, "_pred_logp", lambda r, *a: lp_of(r[0][1]))
    monkeypatch.setattr(L, "_level_score", lambda a, *args: sc_of(a.b))
    monkeypatch.setattr(L, "_p", lambda a, labs: 0.0)


def test_grow_past_accepts_one_step_then_stops_when_v01_passes(monkeypatch):
    b0 = (L.M_LIMIT, L.DX_LIMIT)
    lp = {b0: -20.0, (L.M_LIMIT + 1, L.DX_LIMIT): -1.0, (L.M_LIMIT, L.DX_LIMIT + 1): -15.0}
    sc = {b0: (100.0, 10), (L.M_LIMIT + 1, L.DX_LIMIT): (130.0, 12), (L.M_LIMIT, L.DX_LIMIT + 1): (101.0, 11)}
    _mock(monkeypatch, lambda b: lp.get(b, -1.0), lambda b: sc.get(b, (0.0, 1)))
    hist = []
    res, agg, b, lpo = L._grow_past([0], [1.0], None, None, 1.0, b0, False, None, None,
                                    [("res", b0)], SimpleNamespace(b=b0), -20.0, hist)
    assert b == (L.M_LIMIT + 1, L.DX_LIMIT) and lpo == -1.0
    assert len(hist) == 1 and hist[0].accepted        # V0.1 passes after the step: no further growth


def test_grow_past_rejects_without_evidence(monkeypatch):
    b0 = (L.M_LIMIT, L.DX_LIMIT)
    # V0.1 improves but the refined evidence does not beat the current level
    _mock(monkeypatch, lambda b: -20.0 if b == b0 else -1.0, lambda b: (100.0, 10) if b == b0 else (100.2, 14))
    hist = []
    _, _, b, lpo = L._grow_past([0], [1.0], None, None, 1.0, b0, False, None, None,
                                [("res", b0)], SimpleNamespace(b=b0), -20.0, hist)
    assert b == b0 and lpo == -20.0
    assert len(hist) == 1 and not hist[0].accepted


def test_grow_past_obeys_the_step_cap(monkeypatch):
    b0 = (L.M_LIMIT, L.DX_LIMIT)
    # every step improves V0.1 and evidence but V0.1 never passes: stops at the cap
    _mock(monkeypatch, lambda b: -100.0 + 10 * (b[0] + b[1]), lambda b: (100.0 * (b[0] + b[1]), b[0] + b[1]))
    hist = []
    _, _, b, _ = L._grow_past([0], [1.0], None, None, 1.0, b0, False, None, None,
                              [("res", b0)], SimpleNamespace(b=b0), -100.0 + 10 * sum(b0), hist)
    assert sum(h.accepted for h in hist) <= L.GROW_PAST_STEPS
    assert b[0] <= L.M_LIMIT + L.GROW_PAST_M and b[1] <= L.DX_LIMIT + L.GROW_PAST_DX


def test_canonical_conj_reports_two_pairs_with_ambiguous_orientation():
    """Two conjugate pairs; noisy fits of Q1 whose largest-|Im| coefficient flips sign choice. The
    clusters must be {Q1, conj Q1} and {Q2, conj Q2}, not a factor mixed with its conjugate."""
    rng = np.random.default_rng(0)
    q1 = {(1, 0): 1.0, (0, 1): 0.3j, (0, 2): -0.3j}        # |Im| of xi and xi^2 tied
    q2 = {(1, 0): 1.0, (0, 0): 0.2, (0, 2): -1.5j}
    syms, mass, track = [], [], []
    for i in range(40):
        q = q1 if i % 2 == 0 else q2
        d = {k: v + 0.02 * (rng.normal() + 1j * rng.normal()) * (k != (1, 0)) for k, v in q.items()}
        if rng.random() < 0.5:
            d = {k: np.conj(v) for k, v in d.items()}
        syms.append(sp.expand(sum(complex(v) * tau**a * xi**b for (a, b), v in d.items())))
        mass.append(1.0)
        track.append(i % 2)
    class _Cloud(SimpleNamespace):
        def __len__(self):
            return len(self.sympy)

    agg = SimpleNamespace(cloud=_Cloud(sympy=syms, mass=np.array(mass), track=np.array(track)))
    out = L._canonical_conj_reports(agg, n_pairs=2)
    assert len(out) == 4
    got = sorted(abs(complex(f.coef[(0, 2)][0]).imag) for f in out)
    assert np.allclose(got, [0.3, 0.3, 1.5, 1.5], atol=0.05)
    for f in out:  # Q1's xi coefficient: the pooled median keeps |Im| 0.3 (no cancellation by mixed orientation)
        if abs(complex(f.coef[(0, 2)][0]).imag) < 1:
            assert abs(abs(complex(f.coef[(0, 1)][0]).imag) - 0.3) < 0.05
