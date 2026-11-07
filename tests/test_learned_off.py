"""S-LEARNED rule 1: with every learned layer off, run_loop is the B0 snapshot (PLAN.md §1.1).

The golden file was written by tests/data/make_learned_off_golden.py before any layer hook existed.
Exact equality of labels, factor strings and structures; coefficients, intervals and weights to
1e-9 relative (same machine; this only absorbs BLAS thread-order noise).
"""
import copy
import json
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).parent / "data"))
import make_learned_off_golden as G  # noqa: E402

from pdefactor.learned.config import OFF, Learned  # noqa: E402

GOLD = json.loads(G.OUT.read_text()) if G.OUT.exists() else {}
INPUTS = G.inputs() if GOLD else {}


def _close(a, b):
    return np.allclose(np.asarray(a, float), np.asarray(b, float), rtol=1e-9, atol=1e-12)


def _same(got, ref):
    assert got["label"] == ref["label"]
    assert got["factors"] == ref["factors"]
    assert got["structures"].keys() == ref["structures"].keys()
    assert _close(list(got["structures"].values()), list(ref["structures"].values()))
    assert len(got["coef"]) == len(ref["coef"])
    for g, r in zip(got["coef"], ref["coef"]):
        assert g.keys() == r.keys()
        for k in g:
            assert _close(g[k], r[k]), k
    assert _close(got["w_mean"], ref["w_mean"]) and _close(got["w_q"], ref["w_q"])
    assert got["note"] == ref["note"]


@pytest.mark.parametrize("name", sorted(GOLD))
@pytest.mark.parametrize("learned", [None, OFF], ids=["none", "off"])
def test_off_is_snapshot(name, learned):
    _same(G.run(name, copy.deepcopy(INPUTS[name]), learned), GOLD[name])  # run_loop mutates its inputs (main eaa8f9c)


def test_golden_present():
    assert GOLD, "run tests/data/make_learned_off_golden.py on the B0 snapshot"


def test_config_validates():
    with pytest.raises(ValueError):
        Learned(intervals="on")
    assert not OFF.any and Learned(highk="scan").any
