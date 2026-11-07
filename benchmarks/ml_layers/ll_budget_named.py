"""S-LEARNED-LB named cases (gate criterion 5) through the common runner `ll_named.py`: adds the `lb` arm
(Learned(budget=True) with the fitted model src/pdefactor/learned/models/lb_exact.pkl, or --model) in each
worker; the runner file is not edited.

Usage: python ll_budget_named.py --learned off lb --out analysis/exp/out/ll_lb_named.jsonl [--model path]
"""
from __future__ import annotations

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import pickle
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import ll_named as N  # noqa: E402

MODEL_ENV = "LB_MODEL"
_orig_child = N._child


def _child(conn, args):
    import ll_corpus as C
    from pdefactor.learned import budget as B

    C.LEARNED["lb"] = dict(budget=True)
    if os.environ.get(MODEL_ENV):
        B._CACHE["lb_exact"] = pickle.loads(Path(os.environ[MODEL_ENV]).read_bytes())
    _orig_child(conn, args)


if __name__ == "__main__":
    if "--model" in sys.argv:
        i = sys.argv.index("--model")
        os.environ[MODEL_ENV] = str(Path(sys.argv[i + 1]).resolve())
        del sys.argv[i:i + 2]
    N._child = _child
    N.main()
