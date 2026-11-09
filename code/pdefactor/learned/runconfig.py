"""Per-case computation and candidate knobs for the controller C (sessions/LEARNED/C/PLAN.md §2).

`RunConfig` is the declared search space of the controller: class-(b) knobs and nuisance choices
that may vary per case. Class-(a) scoring (evidence, Occam term, structure prior, label thresholds)
is not here and never varies per case.

Every field defaults to None, meaning "today's value": the module constant or call default the
pipeline uses when no config is given (so L2d's `patched()` constants are still honoured).
`run_loop(config=..., _memo=...)` makes a config and a memo active for its duration through context
variables; the pipeline reads a knob with `knob(name, today)`. With no config active every knob
returns `today`, so the off path is unchanged bit for bit (tests/test_runconfig.py).
"""
from __future__ import annotations

import contextlib
import contextvars
import hashlib
import json
from dataclasses import asdict, dataclass, fields, replace

NOISE = ("input", "white")


@dataclass(frozen=True)
class RunConfig:
    # class searched by the loop (run_loop arguments)
    bounds: tuple | None = None      # starting (m, dx); today START_BOUNDS
    grow: bool | None = None         # today True
    recurse: bool | None = None      # today True
    max_depth: int | None = None     # today 2
    varpro: bool | None = None       # VarPro poles in the core (run_loop refine=); today False
    m_limit: int | None = None       # growth ceiling in tau; today loop.M_LIMIT
    dx_limit: int | None = None      # growth ceiling in xi; today loop.DX_LIMIT
    # core (pass-through keywords of analyze_structured)
    max_order: int | None = None     # pencil order range; today 8
    extra: int | None = None         # BIC orders above the Hankel rank; today 2
    inits: int | None = None         # random restarts of the alternating fit; today 8
    iters: int | None = None         # iterations of the alternating fit; today 30
    # decider and search width
    top: int | None = None           # structures scored by the decider; today 5
    decide_ndraw: int | None = None  # bayes_split Monte Carlo size in the decider; today 2
    alt_top: int | None = None       # alternative structures refined; today loop.ALT_TOP
    highk: bool | None = None        # H0 raw-residual scan; today off
    # refinement and band
    max_full: int | None = None      # refine_raw support search size; today 6
    kmax_pad: int | None = None      # wavenumbers beyond the largest observed mode in the raw band; today 2
    # Monte Carlo sizes (only raised, never lowered, by the controller)
    split_ndraw: int | None = None   # split_layer Monte Carlo size; today 200
    # samples and nuisance (handled by the controller before run_loop)
    n_samples: int | None = None     # posterior samples used; today all given
    noise: str | None = None         # "input" (today) | "white" (structure-free sigma re-estimate)

    def __post_init__(self):
        if self.noise is not None and self.noise not in NOISE:
            raise ValueError(f"noise must be one of {NOISE}")

    def delta(self, **kw):
        return replace(self, **kw)

    def changed(self):
        """The fields set away from today's value."""
        return {k: v for k, v in asdict(self).items() if v is not None}

    def key(self):
        """Stable hash of the set fields (the visited-config identity)."""
        return hashlib.sha256(json.dumps(self.changed(), sort_keys=True, default=str).encode()).hexdigest()[:16]

    def resolved(self):
        """Every field with today's value filled in (for reports and the T2 literal test)."""
        return {f.name: (getattr(self, f.name) if getattr(self, f.name) is not None else today(f.name))
                for f in fields(self)}


DEFAULT = RunConfig()

# run_loop keyword for each class field
LOOP_ARGS = {"bounds": "bounds", "grow": "grow", "recurse": "recurse", "max_depth": "max_depth",
             "varpro": "refine"}
CORE_ARGS = ("max_order", "extra", "inits", "iters")


def today(name):
    """Today's value of a knob, read from the modules at call time."""
    from .. import loop

    vals = dict(bounds=loop.START_BOUNDS, grow=True, recurse=True, max_depth=2, varpro=False,
                m_limit=loop.M_LIMIT, dx_limit=loop.DX_LIMIT, max_order=8, extra=2, inits=8, iters=30,
                top=5, decide_ndraw=2, alt_top=loop.ALT_TOP, highk=False, max_full=6, kmax_pad=2,
                split_ndraw=200, n_samples=None, noise="input")
    return vals[name]


_CFG = contextvars.ContextVar("pdefactor_runconfig", default=None)
_MEMO = contextvars.ContextVar("pdefactor_memo", default=None)


def knob(name, value):
    """The active config's value of `name`, else `value` (today's)."""
    cfg = _CFG.get()
    v = None if cfg is None else getattr(cfg, name)
    return value if v is None else v


def core_kw():
    """Non-default core keywords of the active config (empty off: the core call is unchanged)."""
    cfg = _CFG.get()
    return {} if cfg is None else {k: getattr(cfg, k) for k in CORE_ARGS if getattr(cfg, k) is not None}


def memo():
    return _MEMO.get()


@contextlib.contextmanager
def scoped(config, memo_):
    """Make `config` and `memo_` active (None keeps the outer one)."""
    t1 = _CFG.set(config) if config is not None else None
    t2 = _MEMO.set(memo_) if memo_ is not None else None
    try:
        yield
    finally:
        if t2 is not None:
            _MEMO.reset(t2)
        if t1 is not None:
            _CFG.reset(t1)
