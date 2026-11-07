"""T92: run_loop does not modify its inputs, so a call's result does not depend on earlier calls.
refine_raw memoises per observation set (_excited, and the _lts warm starts of the per-bin scales,
which change the L-BFGS start and so the last digits); those memos must live in a per-call copy."""
import hashlib

import numpy as np

from pdefactor.aggregate import fake_posterior
from pdefactor.loop import run_loop
from pdefactor.synthetic import case, grid, sample_scattered


def _input():
    f = case("heat")
    t, x, u = grid(f, nt=32, nx=64)
    sig = 1e-3 * np.std(np.abs(u))
    s, pis = fake_posterior(u, sig, 2, rng=1)
    ts, xs, ys, s_raw = sample_scattered(f, 150, noise=0.01, rng=3)
    raw = dict(ts=ts, xs=xs, ys=ys, period=2 * np.pi, sigma=s_raw)
    return s, pis, t, x, sig, raw


def _fp(o):
    """Fingerprint of nested dicts / lists / arrays (keys and array bytes)."""
    if isinstance(o, dict):
        return tuple(sorted((str(k), _fp(v)) for k, v in o.items()))
    if isinstance(o, (list, tuple)):
        return tuple(_fp(v) for v in o)
    if isinstance(o, np.ndarray):
        return (o.dtype.str, o.shape, hashlib.md5(np.ascontiguousarray(o).tobytes()).hexdigest())
    return repr(o)


def _result(r):
    return (r.label, r.equation(), [sorted((k, tuple(np.atleast_1d(v).tolist())) for k, v in fr.coef.items())
                                    for fr in r.factors])


def test_two_calls_on_the_same_scattered_input_are_identical_and_leave_it_unchanged():
    s, pis, t, x, sig, raw = _input()
    before = _fp([s, pis, t, x, raw])
    r1 = _result(run_loop(s, t, x, sig, pis, raw=raw))
    assert _fp([s, pis, t, x, raw]) == before
    assert set(raw) == {"ts", "xs", "ys", "period", "sigma"}
    r2 = _result(run_loop(s, t, x, sig, pis, raw=raw))
    assert r1 == r2
    # a raw dict that already carries stale memos (e.g. from a pre-T92 call) gives the clean result
    stale = dict(raw, _lts={"junk": np.zeros(1)}, _excited={})
    assert _result(run_loop(s, t, x, sig, pis, raw=stale)) == r1
