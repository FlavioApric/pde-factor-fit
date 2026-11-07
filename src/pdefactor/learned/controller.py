"""Controller C: an adaptive closed loop around run_loop (sessions/LEARNED/C/PLAN.md).

diagnose -> choose a remedy (a RunConfig delta) -> rerun -> stop when more loops cannot help.

The controller never sets a label and never changes the frozen scoring. It chooses configurations
from the declared space (learned/runconfig.RunConfig); the label is always the frozen pipeline's
output on a configuration. Protection against forking paths (PLAN §4):
  1. R0 = the off run on the full data; it is the answer unless a change is confirmed.
  2. Gaussian data fission (Leiner et al. 2025): A = y + Z, B = y - Z with Z ~ N(0, sigma^2), so A
     and B are independent and keep the design. The search runs on A; the chosen structure and R0's
     are refined on B with the same budget and compared by the frozen evidence - Occam term; then
     the roles swap. A change of the factor set is kept only if confirmed in both directions.
  3. Everything is seeded from a hash of the input arrays: same data, same loops, same answer.
"""
from __future__ import annotations

import copy
import hashlib
import re
import time
from dataclasses import dataclass, field

import numpy as np

from .config import Learned, active
from .memo import Memo
from .runconfig import DEFAULT, LOOP_ARGS, RunConfig

# ------------------------------------------------------------------ diagnoses and remedies
DIAGNOSES = ("no_factors", "misfit", "idker", "undecided", "unexplained_kappa", "ident_margin",
             "ambiguous_structure", "weights_inseparable", "samples_disagree", "at_class_limit",
             "growth_overfit", "spurious_dropped")
STOP_DIAGNOSES = ("low_snr", "no_modes")  # early stop, no search (PLAN §5)


@dataclass(frozen=True)
class Remedy:
    name: str
    needs: str = ""  # "" | "samples" (a posterior sample pool) | "grid" (one noisy grid)


def _delta(name, cfg, case):
    """The config after applying remedy `name` to `cfg` (cumulative), or None if it changes nothing."""
    r = cfg.resolved()
    if name == "more_samples":
        n = case.n_pool
        cur = r["n_samples"] or case.n_use
        return cfg.delta(n_samples=min(n, 2 * cur)) if cur < n else None
    if name == "more_restarts":
        return cfg.delta(inits=2 * r["inits"], iters=2 * r["iters"])
    if name == "wide_alternatives":
        # main refines every alternative by default (loop.ALT_TOP = None): then only the decider widens
        return cfg.delta(alt_top=None if r["alt_top"] is None else 2 * r["alt_top"], top=r["top"] + 3)
    if name == "highk_scan":
        return None if r["highk"] else cfg.delta(highk=True)
    if name == "narrow_band":
        return cfg.delta(kmax_pad=r["kmax_pad"] - 1) if r["kmax_pad"] > 0 else None
    if name == "lower_degree":
        m, dx = r["bounds"]
        nb = (max(1, m - 1), max(0, dx - 2))
        return None if nb == (m, dx) else cfg.delta(bounds=nb)
    if name == "raise_limit":
        return cfg.delta(dx_limit=r["dx_limit"] + 2, m_limit=r["m_limit"] + 1)
    if name == "max_order_up":
        return cfg.delta(max_order=r["max_order"] + 4, extra=r["extra"] + 2)
    if name == "varpro":
        return None if r["varpro"] else cfg.delta(varpro=True)
    if name == "more_mc":
        return cfg.delta(decide_ndraw=4 * r["decide_ndraw"], split_ndraw=2 * r["split_ndraw"])
    if name == "refine_budget":
        return cfg.delta(max_full=r["max_full"] + 4)
    if name == "deeper_recursion":
        return cfg.delta(max_depth=r["max_depth"] + 1)
    if name == "sigma_reest":
        return None if r["noise"] == "white" else cfg.delta(noise="white")
    raise KeyError(name)


REMEDIES = {r.name: r for r in (
    Remedy("more_samples", "samples"), Remedy("more_restarts"), Remedy("wide_alternatives"),
    Remedy("highk_scan"), Remedy("narrow_band"), Remedy("lower_degree"), Remedy("raise_limit"),
    Remedy("max_order_up"), Remedy("varpro"), Remedy("more_mc"), Remedy("refine_budget"),
    Remedy("deeper_recursion"), Remedy("sigma_reest", "grid"))}

# PHASE4 §4 C table, extended to the remedies above (rule baseline C0; prior order of C1/C2)
DEFAULT_TABLE = {
    "no_factors": ["varpro", "more_samples", "lower_degree", "sigma_reest"],
    "misfit": ["more_restarts", "raise_limit", "more_samples", "max_order_up"],
    "idker": ["highk_scan", "lower_degree", "more_samples"],
    "undecided": ["more_samples", "more_restarts", "varpro"],
    "unexplained_kappa": ["highk_scan", "raise_limit", "max_order_up", "sigma_reest"],
    "ident_margin": ["highk_scan", "lower_degree", "narrow_band"],
    "ambiguous_structure": ["wide_alternatives", "more_mc", "refine_budget", "more_samples"],
    "weights_inseparable": [],
    "samples_disagree": ["more_samples", "more_restarts"],
    "at_class_limit": ["raise_limit"],
    "growth_overfit": ["lower_degree", "more_samples", "narrow_band"],
    "spurious_dropped": ["wide_alternatives", "refine_budget", "deeper_recursion"],
}


# ------------------------------------------------------------------ the data of one case
@dataclass
class Case:
    pool: list                 # posterior samples available (a noisy grid: [u])
    pool_pis: np.ndarray
    t: np.ndarray
    x: np.ndarray
    sigma: float               # run_loop's sigma (0 on the GP path)
    raw: dict | None
    noise_draws: object        # array, None, or "gp" (sqrt 2 x deviations of the used samples)
    n_use: int                 # samples used by the default config
    bootstrap: int = 0
    kw: dict = field(default_factory=dict)

    @property
    def n_pool(self):
        return len(self.pool)

    @property
    def grid(self):
        return len(self.pool) == 1 and self.raw is None and not isinstance(self.noise_draws, np.ndarray)

    def inputs(self, cfg):
        """(samples, pis, sigma, noise_draws) under config cfg."""
        n = cfg.n_samples or self.n_use
        S = list(self.pool[:n])
        w = np.asarray(self.pool_pis[:n], float)
        w = w / w.sum()
        nd = self.noise_draws
        if isinstance(nd, str):  # "gp"
            A = np.asarray(S)
            nd = np.sqrt(2) * (A - np.tensordot(w, A, 1)[None])
        sig = self.sigma
        if cfg.noise == "white" and self.grid:
            sig = sigma_highband(S[0], self.x)
        return S, w, sig, nd

    def obs(self):
        """The observation set of the refinement pass (loop.py step 5)."""
        from ..loop import _grid_obs

        if self.raw is not None:
            return self.raw
        S, _, sig, _ = self.inputs(DEFAULT)
        return _grid_obs(S[0], self.t, self.x, sig) if sig > 0 else None


def sigma_highband(u, x):
    """Structure-free white-noise level of a grid: robust scale of the top quarter of the
    x-wavenumbers (|n| >= 3 nx / 8), where a field in the kernel of a smooth symbol has decayed
    or is absent. Re and Im of fft(u)/sqrt(nx) each have variance sigma^2 / 2 there."""
    nx = u.shape[-1]
    F = np.fft.fft(u, axis=-1) / np.sqrt(nx)
    n = np.abs(np.fft.fftfreq(nx, 1.0 / nx))
    v = F[..., (n >= 3 * nx / 8) & (n < nx / 2)]
    parts = np.concatenate([v.real.ravel(), v.imag.ravel()])
    return float(1.4826 * np.median(np.abs(parts - np.median(parts))) * np.sqrt(2))


def case_seed(case):
    from .memo import key

    return int(key("seed", list(case.pool), case.t, case.x, case.sigma,
                   None if case.raw is None else case.raw.get("ys"))[1][:8], 16)


# ------------------------------------------------------------------ fission
def _gp_samples(ts, xs, ys, t, x, period, S, seed):
    from ..interp.gp import fit_gp

    cplx = np.iscomplexobj(ys)
    parts = [ys.real, ys.imag] if cplx else [ys]
    fits = [fit_gp(ts, xs, y, grid=(t, x), period_x=period, S=S, seed=seed) for y in parts]
    if cplx:
        return fits[0].samples + 1j * fits[1].samples, fits[0].weights * fits[1].weights
    return fits[0].samples, fits[0].weights


def fission(case, seed, tau=1.0, gp_S=None):
    """Two independent folds with the design of `case` (Leiner et al. 2025, Gaussian case):
    A = y + tau Z, B = y - Z / tau, Z ~ N(0, sigma^2); the noise of A is sigma sqrt(1 + tau^2), of B
    sigma sqrt(1 + 1/tau^2). Grid: the noisy grid; scattered: the raw observations, each fold
    re-interpolated by the GP. None when the case has neither (GP samples without raw data)."""
    rng = np.random.default_rng(seed)
    sa, sb = np.sqrt(1 + tau ** 2), np.sqrt(1 + 1 / tau ** 2)
    if case.raw is not None:
        raw = case.raw
        ys = np.asarray(raw["ys"])
        sig = float(raw["sigma"])
        Z = sig * (rng.standard_normal(ys.shape) + (1j * rng.standard_normal(ys.shape) if np.iscomplexobj(ys) else 0))
        out = []
        for i, (y, s) in enumerate(((ys + tau * Z, sa), (ys - Z / tau, sb))):
            r2 = dict(raw, ys=y, sigma=sig * s)
            S, w = _gp_samples(raw["ts"], raw["xs"], y, case.t, case.x, raw["period"], gp_S or case.n_pool,
                               (seed + 7 * i) % 2 ** 31)
            out.append(Case(list(S), w / w.sum(), case.t, case.x, case.sigma, r2, "gp", min(case.n_use, len(S)),
                            case.bootstrap, dict(case.kw)))
        return tuple(out)
    if case.grid and case.sigma > 0:
        u = np.asarray(case.pool[0])
        Z = case.sigma * (rng.standard_normal(u.shape) + (1j * rng.standard_normal(u.shape) if np.iscomplexobj(u) else 0))
        return tuple(Case([y], np.ones(1), case.t, case.x, case.sigma * s, None, None, 1, case.bootstrap, dict(case.kw))
                     for y, s in ((u + tau * Z, sa), (u - Z / tau, sb)))
    return None


# ------------------------------------------------------------------ one run, its diagnosis, its score
EXPLORE = dict(split=False, bootstrap=0, report_domain=False)


def run_config(case, cfg, memo=None, explore=False, learned=None):
    """run_loop on `case` under config `cfg` (exploration profile: no split layer, no bootstrap)."""
    from ..loop import run_loop

    S, w, sig, nd = case.inputs(cfg)
    kw = dict(case.kw)
    kw.update({LOOP_ARGS[k]: v for k, v in cfg.changed().items() if k in LOOP_ARGS})
    ll = active(learned)
    if cfg.highk:
        ll = Learned(**{**ll.__dict__, "highk": "scan", "controller": False})
    else:
        ll = Learned(**{**ll.__dict__, "controller": False})
    kw.update(raw=case.raw, noise_draws=nd, bootstrap=case.bootstrap, learned=ll if ll.any else None)
    if explore:
        kw.update(EXPLORE)
    with np.errstate(all="ignore"):
        return run_loop(S, case.t, case.x, sig, w, config=cfg, _memo=memo, **kw)


def _v0(res, case, cfg):
    from ..validate import validate

    S, w, sig, nd = case.inputs(cfg)
    u = np.tensordot(w, np.asarray(S), 1)
    if sig <= 0 and nd is not None:
        sig = smooth_noise(np.asarray(S), w)
    try:
        return validate(res, u, case.t, case.x, sig)
    except Exception:  # noqa: BLE001 - a failed check is no flag, the run itself stands
        return None


def smooth_noise(samples, w, r=4, factor=np.sqrt(2)):
    """GPPosterior.effective_noise(kind="smooth") on arrays (as benchmarks/bench_e2e.smooth_noise)."""
    from numpy.polynomial import legendre

    d = samples - np.tensordot(w, samples, 1)[None]
    nt, nx = d.shape[-2:]
    B = np.fft.fft(d, axis=-1) / nx
    Q, _ = np.linalg.qr(legendre.legvander(np.linspace(-1, 1, nt), r - 1))
    P = np.einsum("ta,stk->sak", Q, B)
    b2 = (np.sum(w[:, None, None] * (np.abs(P) ** 2).sum(1), axis=0) / r).max()
    return float(factor * np.sqrt(b2) * np.sqrt(nx))


def diagnose(res, case, cfg):
    """(active diagnoses, features) of one run, from what run_loop and V0 already report."""
    from .. import loop

    d = set()
    if not res.factors:
        d.add("no_factors")
    lab = res.label
    if lab == "MISFIT":
        d.add("misfit")
    elif lab.startswith("ID-KER"):
        d.add("idker")
    elif lab == "UNDECIDED" and res.factors:
        d.add("undecided")
    rep = _v0(res, case, cfg)
    flags = {c for c, _ in rep.flags} if rep is not None else set()
    for code, name in (("V0.1", "unexplained_kappa"), ("V0.2", "ident_margin"), ("V0.3", "ambiguous_structure"),
                       ("V0.10", "weights_inseparable")):
        if code in flags:
            d.add(name)
    if "rejected very strongly" in res.note:
        d.add("samples_disagree")
    r = cfg.resolved()
    if res.bounds and (res.bounds[0] >= r["m_limit"] or res.bounds[1] >= r["dx_limit"]):
        d.add("at_class_limit")
    if any("overfit guard" in (h.note or "") for h in res.history):
        d.add("growth_overfit")
    if res.dropped:
        d.add("spurious_dropped")
    feats = {"n_factors": len(res.factors), "p_top": max(res.structures.values()) if res.structures else 0.0}
    if rep is not None:
        for k, v in rep.features().items():
            feats[k] = v
    try:
        from .features import export_features

        S, w, sig, nd = case.inputs(cfg)
        ex = export_features(res, loop.l2c_data(S, w, case.t, case.x, sig, nd, case.raw))
        for k in ("kappa_vand", "log_snr", "disagreement", "mode_margin", "rel_width", "log_nobs"):
            vals = [e[k] for e in ex if np.isfinite(e.get(k, np.nan))]
            feats[k] = float(np.min(vals)) if vals else np.nan
    except Exception:  # noqa: BLE001
        pass
    return d, feats


def early_stop(res, feats):
    """PLAN §5: no search when the data cannot identify anything (T13, T40, T46)."""
    if not res.factors and res.label == "UNDECIDED" and not res.structures:
        return "no modes above noise: nothing to search"
    mm = feats.get("mode_margin", np.nan)
    if res.factors and np.isfinite(mm) and mm < 0:
        return (f"SNR below identifiability: every factor has fewer distinct observed |kappa| than its "
                f"coefficients need (V0.2 margin {mm:.0f})")
    return None


def _band(res, case):
    """The raw band a run's refinement used: H0's widened band when it fired, else the default."""
    m = re.search(r"band widened to (\d+)", res.note or "")
    return int(m.group(1)) if m else None


def base_band(case):
    from ..core.structfit import extract_modes_ic
    from ..loop import _mean_sample, _raw_kmax

    S, w, sig, nd = case.inputs(DEFAULT)
    m, _, _, _ = extract_modes_ic(_mean_sample(S, w), case.t, case.x, noise=sig,
                                  noise_draws=None if nd is None else nd / np.sqrt(2))
    period = case.raw["period"] if case.raw is not None else (case.x[1] - case.x[0]) * len(case.x)
    return _raw_kmax(m, period)


def fset(res_or_factors):
    """Identity of a factor set: per factor the monomials kept by `pruned` (support), sorted."""
    from ..loop import LoopResult

    fs = res_or_factors.factors if hasattr(res_or_factors, "factors") else res_or_factors
    qs = LoopResult("", list(fs), {}, {}, [], False, (0, 0), {}).pruned()
    import sympy as sp

    from ..symbols import tau, xi

    return tuple(sorted(tuple(sorted(sp.Poly(q, tau, xi).monoms())) for q in qs))


def score(case, factors, kmax):
    """Frozen evidence - Occam term of a factor set on `case`'s observations, refined with the same
    budget for every set compared (loop.py step 5, T51-T52). Empty set: the noise-only evidence."""
    from ..loop import _mean_sample, refine_factors, support_path
    from ..refine_raw import log_evidence

    obs = case.obs()
    if obs is None:
        return np.nan
    if not factors:
        return float(log_evidence([], obs, kmax))
    S, w, sig, nd = case.inputs(DEFAULT)
    fs = copy.deepcopy(list(factors))
    ndh = None if nd is None else nd / np.sqrt(2)
    occ = 0.5 * np.log(len(obs["ys"]) * (1 if np.isrealobj(obs["ys"]) else 2))
    try:
        cand = support_path(fs, _mean_sample(S, w), case.t, case.x, sig, ndh)
        ro = refine_factors(fs, obs, kmax, candidates=cand)
    except (np.linalg.LinAlgError, ValueError, ZeroDivisionError, IndexError):
        return np.nan
    return float(ro["logev"] - occ * ro["p"])


# ------------------------------------------------------------------ policies
@dataclass
class State:
    diags: set
    feats: dict
    tried: list
    k: int
    cfg: RunConfig
    case: Case
    elapsed: float
    budget: float


def applicable(state):
    """Remedies whose precondition holds, that change the config and were not tried."""
    out = []
    for name, r in REMEDIES.items():
        if name in state.tried:
            continue
        if r.needs == "samples" and (state.case.grid or not isinstance(state.case.noise_draws, str)):
            continue
        if r.needs == "grid" and not state.case.grid:
            continue
        if _delta(name, state.cfg, state.case) is None:
            continue
        out.append(name)
    return out


class RulePolicy:
    """C0: the default table in order, first untried applicable remedy, at most K actions."""
    name = "rules"

    def __init__(self, K=3, table=None, banned=()):
        self.K, self.table, self.banned = K, table or DEFAULT_TABLE, set(banned)

    def choose(self, st):
        if st.k >= self.K:
            return None
        ok = [r for r in applicable(st) if r not in self.banned]
        for d in DIAGNOSES:
            if d in st.diags:
                for r in self.table.get(d, []):
                    if r in ok:
                        return r
        return None


class TablePolicy:
    """C1: RemedyTable lower bound of success per (diagnosis, remedy) minus lam x cost; stop when no
    remedy has a positive index (Weitzman 1979, binary reward: G p - lam c, G = 1)."""
    name = "table"

    def __init__(self, table, lam=0.0, cost=None, banned=()):
        self.table, self.lam, self.cost, self.banned = table, lam, cost or {}, set(banned)

    def choose(self, st):
        ok = [r for r in applicable(st) if r not in self.banned]
        best, bv = None, 0.0
        for r in ok:
            lb = max((self.table.rate(d, r)[1] for d in st.diags if (d, r) in self.table._n), default=0.0)
            v = lb - self.lam * self.cost.get(r, 0.0)
            if v > bv:
                best, bv = r, v
        return best


class ContextualPolicy:
    """C2: per-remedy calibrated success model p_r(x) and cost model c_r(x) (fitted offline by
    benchmarks/ml_layers/ll_C_train.py); greedy on the lower bound p_lb - lam c, stop when none is positive."""
    name = "contextual"

    def __init__(self, models, lam=0.0, banned=()):
        self.m, self.lam, self.banned = models, lam, set(banned)

    def choose(self, st):
        ok = [r for r in applicable(st) if r not in self.banned and r in self.m["success"]]
        if not ok:
            return None
        x = featurize(st)
        best, bv = None, 0.0
        for r in ok:
            p = float(self.m["success"][r](x))
            c = float(self.m["cost"].get(r, lambda _: 0.0)(x))
            v = p - self.lam * c
            if v > bv:
                best, bv = r, v
        return best


class SequencePolicy:
    """A fixed sequence of remedies (logging, tests, the forced-depth null test)."""
    name = "sequence"

    def __init__(self, seq):
        self.seq = list(seq)

    def choose(self, st):
        ok = applicable(st)
        for r in self.seq:
            if r in ok:
                return r
        return None


class LogitIso:
    """Logistic score then isotonic calibration (Zadrozny & Elkan 2002); plain arrays, picklable.
    `harm` (the remedy's rate of turning a non-false-confident answer false-confident) is subtracted."""

    def __init__(self, w, b, xs, ys, mu, sd, harm=0.0):
        self.w, self.b, self.xs, self.ys, self.mu, self.sd = (np.asarray(w, float), float(b), np.asarray(xs, float),
                                                              np.asarray(ys, float), np.asarray(mu), np.asarray(sd))
        self.harm = float(harm)

    def __call__(self, x):
        z = float((np.asarray(x) - self.mu) / self.sd @ self.w + self.b)
        s = 1.0 / (1.0 + np.exp(-np.clip(z, -30, 30)))
        return (float(np.interp(s, self.xs, self.ys)) if len(self.xs) else s) - self.harm


class Linear:
    """Ridge cost model in units of the off run's runtime, clipped at 0."""

    def __init__(self, w, b, mu, sd):
        self.w, self.b, self.mu, self.sd = np.asarray(w, float), float(b), np.asarray(mu), np.asarray(sd)

    def __call__(self, x):
        return max(0.0, float((np.asarray(x) - self.mu) / self.sd @ self.w + self.b))


@dataclass
class Fitted:
    """A trained policy as saved by benchmarks/ml_layers/ll_C_train.py (C1 table or C2 contextual)."""
    kind: str
    lam: float
    table: object = None
    cost: dict = None
    models: dict = None
    meta: dict = None

    def policy(self, banned=()):
        if self.kind == "table":
            return TablePolicy(self.table, self.lam, self.cost, banned)
        return ContextualPolicy(self.models, self.lam, banned)


FEATS = ("n_factors", "p_top", "v01_omnibus_logp", "v01_n_bad_bins", "v02_min_margin", "v03_gap", "v03_entropy",
         "v10_w_rel", "kappa_vand", "log_snr", "disagreement", "mode_margin", "rel_width", "log_nobs")


def featurize(st):
    """Dimensionless feature vector: features (NaN -> 0 plus a missing bit), diagnosis bits, tried bits,
    loop index, design (grid / samples)."""
    v = []
    for k in FEATS:
        a = st.feats.get(k, np.nan)
        a = float(a) if a is not None else np.nan
        v += [0.0 if not np.isfinite(a) else float(np.clip(a, -50, 50)), float(not np.isfinite(a))]
    v += [float(d in st.diags) for d in DIAGNOSES]
    v += [float(r in st.tried) for r in REMEDIES]
    v += [float(st.k), float(st.case.grid)]
    return np.asarray(v)


# ------------------------------------------------------------------ the controller
@dataclass
class Visit:
    loop: int
    remedy: str | None
    cfg: RunConfig
    res: object
    diags: set
    feats: dict
    seconds: float
    band: int | None = None


@dataclass
class ControlledResult:
    result: object                       # the reported LoopResult (frozen labels)
    r0: object                           # the off run on the full data
    actions: list                        # (fold, loop, remedy, config key, seconds)
    n_actions: int
    stop_reason: str
    visited: dict                        # structure -> posterior weight (sums to 1 - missing_mass)
    missing_mass: float
    accepted: bool                       # the controller's configuration is reported
    changed: bool                        # the reported factor set differs from R0's
    confirmed: dict                      # {"A->B": bool, "B->A": bool}
    config: RunConfig
    fission: dict
    runtime: float
    trace: list = field(default_factory=list)  # per depth k: the would-be output (forced-depth runs)


def _search(case, policy, max_loops, deadline, memo, learned, t_off, trace_depth=None):
    """Loop on one fold: R0 of the fold, then remedies until the policy stops."""
    t0 = time.perf_counter()
    cfg = DEFAULT
    res = run_config(case, cfg, memo, explore=True, learned=learned)
    d, f = diagnose(res, case, cfg)
    visits = [Visit(0, None, cfg, res, d, f, time.perf_counter() - t0, _band(res, case))]
    tried = []
    stop = "policy"
    while True:
        k = len(visits) - 1
        if k >= max_loops:
            stop = "max_loops"
            break
        if time.perf_counter() > deadline:
            stop = "budget"
            break
        st = State(visits[-1].diags, visits[-1].feats, tried, k, cfg, case, time.perf_counter() - t0, deadline)
        if not st.diags and trace_depth is None:
            stop = "no diagnosis"
            break
        r = policy.choose(st)
        if r is None:
            stop = "policy"
            break
        tried.append(r)
        c2 = _delta(r, cfg, case)
        t1 = time.perf_counter()
        try:
            res = run_config(case, c2, memo, explore=True, learned=learned)
        except Exception as e:  # noqa: BLE001 - a failed remedy is a visited dead end
            visits.append(Visit(k + 1, r, c2, None, set(), {}, time.perf_counter() - t1))
            visits[-1].feats["error"] = repr(e)
            continue
        cfg = c2
        d, f = diagnose(res, case, cfg)
        visits.append(Visit(k + 1, r, cfg, res, d, f, time.perf_counter() - t1, _band(res, case)))
    return visits, stop


def run_controlled(samples, t, x, sigma, pis=None, *, raw=None, noise_draws=None, bootstrap=0, learned=None,
                   policy=None, max_loops=20, budget_s=None, mode="fission", n_use=None, seed=None,
                   trace=False, **run_loop_kw):
    """The controller (Learned(controller=True)). samples: the posterior sample pool (a noisy grid:
    [u]); n_use: samples the default config uses (default all); noise_draws="gp": draws from the used
    samples (sqrt 2 x deviations from their mean). mode: "fission" (cross-fitted, default), "single"
    (search on A, confirm on B only), "none" (search and score on the full data: the old rule, the
    forking-paths control). trace: record the would-be output at every loop depth (null test).
    Returns ControlledResult; `.result` is a LoopResult with frozen labels."""
    T0 = time.perf_counter()
    pis = np.full(len(samples), 1.0 / len(samples)) if pis is None else np.asarray(pis, float)
    case = Case(list(samples), pis, t, x, sigma, raw, noise_draws, n_use or len(samples), bootstrap,
                dict(run_loop_kw))
    policy = policy or RulePolicy()
    seed = case_seed(case) if seed is None else seed
    memo = Memo()
    r0 = run_config(case, DEFAULT, memo, learned=learned)
    t_off = time.perf_counter() - T0
    budget = budget_s if budget_s is not None else max(3 * t_off, 600.0)
    deadline = T0 + t_off + budget
    d0, f0 = diagnose(r0, case, DEFAULT)

    def out(result, reason, **kw):
        base = dict(result=result, r0=r0, actions=[], n_actions=0, stop_reason=reason, visited={},
                    missing_mass=0.0, accepted=False, changed=False, confirmed={}, config=DEFAULT, fission={},
                    runtime=time.perf_counter() - T0)
        base.update(kw)
        return ControlledResult(**base)

    def noted(res, msg):
        res = copy.copy(res)
        res.note = (res.note + " " + msg).strip()
        return res

    why = early_stop(r0, f0)
    if why and not trace:
        return out(noted(r0, f"controller: stopped before any search ({why})."), why)
    if not d0 and not trace:
        return out(r0, "no diagnosis")

    if mode == "none":
        folds = None
    else:
        folds = fission(case, seed)
        if folds is None:
            return out(noted(r0, "controller: no fission possible (no raw data, no single grid)."), "no fission")
    fission_info = {} if folds is None else {"tau": 1.0, "seed": seed, "sigma": float(
        case.raw["sigma"] if case.raw is not None else case.sigma)}

    if mode == "none":
        visits, stop = _search(case, policy, max_loops, deadline, memo, learned, t_off, trace_depth=trace or None)
        runs = {"F": visits}
    else:
        A, B = folds
        va, sa = _search(A, policy, max_loops, deadline, Memo(), learned, t_off, trace or None)
        runs = {"A": va}
        stop = sa
        if mode == "fission":
            vb, sb = _search(B, policy, max_loops, deadline, Memo(), learned, t_off, trace or None)
            runs["B"] = vb
            stop = f"A: {sa}; B: {sb}"
    actions = [(fk, v.loop, v.remedy, v.cfg.key(), round(v.seconds, 2)) for fk, vs in runs.items() for v in vs[1:]]
    fold_case = {"F": case} if mode == "none" else {"A": folds[0], "B": folds[1]}
    other = {"A": "B", "B": "A", "F": "F"}

    # scores: each visited set on its own fold (to pick) and on the other fold (to confirm), one band
    # per fold = the widest band any visited run of either fold used
    bands = {fk: base_band(c) for fk, c in fold_case.items()}
    wide = max([v.band for vs in runs.values() for v in vs if v.band] or [0])
    bands = {fk: max(b, wide) for fk, b in bands.items()}
    cache = {}

    def sc(fk, factors):
        key_ = (fk, fset(factors))
        if key_ not in cache:
            cache[key_] = score(fold_case[fk], factors, bands[fk])
        return cache[key_]

    def pick(fk, upto):
        best = None
        for v in runs[fk][:upto + 1]:
            if v.res is None:
                continue
            s = sc(fk, v.res.factors)
            if np.isfinite(s) and (best is None or s > best[0] + 1e-9):
                best = (s, v)
        return best[1] if best else runs[fk][0]

    def decide(upto):
        """(config, confirmed dict) the controller would report after `upto` loops per fold."""
        conf = {}
        picks = {fk: pick(fk, upto) for fk in runs}
        if mode == "none":
            return picks["F"].cfg, {"F": True}, picks
        for fk, v in picks.items():
            ok_ = other[fk]
            if ok_ not in fold_case or v.res is None:
                continue
            s_new = sc(ok_, v.res.factors)
            s_old = sc(ok_, r0.factors)
            conf[f"{fk}->{ok_}"] = bool(np.isfinite(s_new) and np.isfinite(s_old) and s_new > s_old)
        held = {fk: (sc(other[fk], v.res.factors) if v.res is not None else -np.inf) for fk, v in picks.items()}
        held = {fk: (h if np.isfinite(h) else -np.inf) for fk, h in held.items()}
        return picks[max(sorted(held), key=held.get)].cfg, conf, picks

    def final(cfg, conf, picks):
        """The full-data run of cfg, kept if its factor set equals R0's or is confirmed both ways."""
        if cfg.key() == DEFAULT.key():
            return r0, False, False
        res = run_config(case, cfg, memo, learned=learned)
        changed = fset(res) != fset(r0)
        if not changed:
            return res, True, False
        if mode == "none":
            return res, True, True
        need = ["A->B", "B->A"] if mode == "fission" else ["A->B"]
        confirmed_sets = {fset(v.res) for v in picks.values() if v.res is not None}
        if all(conf.get(k_) for k_ in need) and fset(res) in confirmed_sets:
            return res, True, True
        return None, False, True

    tr = []
    if trace:
        depth = max(len(vs) for vs in runs.values()) - 1
        for k in range(depth + 1):
            cfg_k, conf_k, picks_k = decide(k)
            res_k, acc_k, ch_k = final(cfg_k, conf_k, picks_k)
            res_k = r0 if res_k is None else res_k
            tr.append(dict(depth=k, label=res_k.label, factors=[str(q) for q in res_k.pruned()],
                           accepted=acc_k, changed=ch_k and acc_k, confirmed=conf_k))
    cfg, conf, picks = decide(max(len(vs) for vs in runs.values()))
    res, acc, ch = final(cfg, conf, picks)
    msg = f"controller: {len(actions)} action(s) ({stop})"
    if res is None:
        res, acc, ch = r0, False, False
        msg += "; the proposed factor set was not confirmed out of fold, the off answer stands"
    elif acc:
        msg += f"; configuration {cfg.changed()} " + ("changed the factor set (confirmed out of fold)" if ch else
                                                       "kept the factor set")
    if why:
        msg += f"; note: {why}"
    # report: posterior over visited structures (held-out scores) + Good-Turing missing mass
    from ..loop import _structure

    seen = {}
    for fk, vs in runs.items():
        for v in vs:
            if v.res is not None:
                s_ = str(_structure(v.res.factors)) if v.res.factors else "()"
                seen.setdefault(s_, []).append(sc(other[fk], v.res.factors))
    props = sum(len(v) for v in seen.values())
    n1 = sum(1 for v in seen.values() if len(v) == 1)
    miss = n1 / props if props else 0.0
    lw = {s_: np.nanmean(v) if np.isfinite(v).any() else -np.inf for s_, v in seen.items()}
    mx = max(lw.values()) if lw else 0.0
    wts = {s_: float(np.exp(v - mx)) if np.isfinite(v) else 0.0 for s_, v in lw.items()}
    tot = sum(wts.values()) or 1.0
    visited = {s_: (1 - miss) * w_ / tot for s_, w_ in sorted(wts.items(), key=lambda kv: -kv[1])}
    return ControlledResult(noted(res, msg + "."), r0, actions, len(actions), stop, visited, miss, acc, ch, conf, cfg,
                            fission_info, time.perf_counter() - T0, tr)
