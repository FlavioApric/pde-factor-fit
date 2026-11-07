"""RunConfig (controller C, sessions/LEARNED/C/PLAN.md §2.2, test T2).

A config with every field at today's value, or no config, is the pipeline of the golden file bit for
bit; the core pass-through keywords with their defaults change nothing; a non-default value reaches
the place it controls.
"""
import inspect
import json
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).parent / "data"))
import make_learned_off_golden as G  # noqa: E402

from pdefactor import loop  # noqa: E402
from pdefactor.core import structfit  # noqa: E402
from pdefactor.learned import runconfig as R  # noqa: E402
from pdefactor.learned.runconfig import DEFAULT, RunConfig  # noqa: E402

GOLD = json.loads(G.OUT.read_text()) if G.OUT.exists() else {}


def _default(fn, name):
    return inspect.signature(fn).parameters[name].default


def test_today_matches_literals():
    r = DEFAULT.resolved()
    assert r["bounds"] == loop.START_BOUNDS == _default(loop.run_loop, "bounds")
    assert r["max_depth"] == _default(loop.run_loop, "max_depth")
    assert r["varpro"] == _default(loop.run_loop, "refine")
    assert (r["m_limit"], r["dx_limit"], r["alt_top"]) == (loop.M_LIMIT, loop.DX_LIMIT, loop.ALT_TOP)
    assert r["max_order"] == _default(structfit.extract_modes_ic, "max_order")
    assert r["extra"] == _default(structfit.extract_modes_ic, "extra")
    assert r["inits"] == _default(structfit.fit_structure, "inits")
    assert r["iters"] == _default(structfit.fit_structure, "iters")
    assert r["top"] == _default(loop.decide_structure, "top")
    assert r["split_ndraw"] == _default(loop.split_layer, "ndraw")
    from pdefactor.refine_raw import refine

    assert r["max_full"] == _default(refine, "max_full")


def test_knob_scope_restores():
    assert R.knob("alt_top", 2) == 2 and R.core_kw() == {}
    with pytest.raises(RuntimeError):
        with R.scoped(RunConfig(alt_top=4, inits=3), None):
            assert R.knob("alt_top", 2) == 4 and R.core_kw() == {"inits": 3}
            raise RuntimeError
    assert R.knob("alt_top", 2) == 2 and R.core_kw() == {}


def test_key_stable():
    assert RunConfig().key() == DEFAULT.key()
    assert RunConfig(alt_top=4).key() != DEFAULT.key()
    assert RunConfig(alt_top=4).key() == RunConfig().delta(alt_top=4).key()
    with pytest.raises(ValueError):
        RunConfig(noise="pink")


def _grid():
    from pdefactor.simulator import random_pde
    from pdefactor.synthetic import grid

    d = random_pde("F1", 0)
    t, x, u = grid(d.field)
    sig = 0.01 * np.std(u)
    return u + sig * np.random.default_rng(1000).standard_normal(u.shape), t, x, sig


def _same_struct(a, b):
    assert a.label == b.label and a.n_modes == b.n_modes
    assert [str(f.symbol) for f in a.factors] == [str(f.symbol) for f in b.factors]
    assert a.structures == b.structures


def test_core_passthrough_defaults_identical():
    u, t, x, sig = _grid()
    with np.errstate(all="ignore"):
        a = structfit.analyze_structured(u, t, x, noise=sig, real=True)
        b = structfit.analyze_structured(u, t, x, noise=sig, real=True, max_order=8, extra=2, inits=8, iters=30)
    _same_struct(a, b)


def test_core_passthrough_reaches(monkeypatch):
    seen = {}
    orig = structfit.fit_structure

    def spy(*a, **k):
        seen.setdefault("inits", set()).add(k.get("inits"))
        seen.setdefault("iters", set()).add(k.get("iters"))
        return orig(*a, **k)

    monkeypatch.setattr(structfit, "fit_structure", spy)
    u, t, x, sig = _grid()
    with np.errstate(all="ignore"):
        structfit.analyze_structured(u, t, x, noise=sig, real=True, inits=3, iters=7)
    assert seen["inits"] == {3} and seen["iters"] == {7}


@pytest.mark.parametrize("name", sorted(GOLD))
def test_default_config_is_snapshot(name):
    from test_learned_off import _same

    inputs = G.inputs()
    S, t, x, sig, kw = inputs[name]
    with np.errstate(all="ignore"):
        got = G.summary(loop.run_loop(S, t, x, sig, config=RunConfig(), **kw))
    _same(got, GOLD[name])
