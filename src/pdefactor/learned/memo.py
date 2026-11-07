"""Exact memo of pipeline stages, shared by the controller C and the budget layer LB.

One mechanism (parent's decision, 2026-10-29): `run_loop(..., _memo=Memo())` makes a memo active
(learned/runconfig.scoped); a stage looks its result up by `key(stage, *arrays, **params)` and
stores it on a miss. Values are deep-copied in and out, because later steps mutate them in place
(e.g. loop._merge_tracks on an aggregate). A hit returns exactly what the stage would compute, so
results with and without a memo are identical (tests/test_learned_controller.py::test_memo).
Stage names are free strings; new stages add their own name.
"""
from __future__ import annotations

import copy
import hashlib

import numpy as np


def _feed(h, a):
    if a is None:
        h.update(b"N")
    elif isinstance(a, np.ndarray):
        a = np.ascontiguousarray(a)
        h.update(str((a.shape, a.dtype.str)).encode())
        h.update(a.tobytes())
    elif isinstance(a, (list, tuple)):
        h.update(f"L{len(a)}".encode())
        for b in a:
            _feed(h, b)
    elif isinstance(a, dict):
        h.update(f"D{len(a)}".encode())
        for k in sorted(a, key=str):
            h.update(str(k).encode())
            _feed(h, a[k])
    else:
        h.update(repr(a).encode())


def key(stage, *arrays, **params):
    """(stage, sha256 of the arrays and the sorted params)."""
    h = hashlib.sha256()
    _feed(h, list(arrays))
    _feed(h, params)
    return stage, h.hexdigest()


class Memo:
    def __init__(self):
        self._d = {}
        self.hits = 0
        self.misses = 0

    def get(self, k):
        if k in self._d:
            self.hits += 1
            return copy.deepcopy(self._d[k])
        self.misses += 1
        return None

    def put(self, k, value):
        self._d[k] = copy.deepcopy(value)
        return value

    def __contains__(self, k):
        return k in self._d

    def __len__(self):
        return len(self._d)
