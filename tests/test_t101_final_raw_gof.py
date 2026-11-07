"""T101: (a) the scattered per-bin scale profile with a column group of (numerically) zero norm;
(b) a subset drop of the split layer that would leave a claimed law is checked by T88 on the raw points."""
import numpy as np

from pdefactor import loop, refine_raw
from pdefactor.symbols import tau, xi


def test_per_bin_profile_with_a_vanished_column_group():
    """A group whose columns are below 1e-8 in norm made log(1e-8 / cn) exceed the upper bound and
    L-BFGS-B raise (two_pairs 400 1 % s0). Now its scale is fixed at the upper bound: the value is that
    of the profile without the group (to < 1e-6) and finite."""
    rng = np.random.default_rng(0)
    r = 12
    W = rng.standard_normal((r, 6))
    c = W[:, :3] @ rng.standard_normal(3) + 0.1 * rng.standard_normal(r)
    cg = np.array([0, 0, 1, 1, 2, 2])
    Wz = np.column_stack([W, 1e-12 * rng.standard_normal((r, 2)), np.zeros((r, 1))])
    cgz = np.concatenate([cg, [3, 3, 4]])
    v0 = refine_raw._per_bin_neg(c, W, cg, 0.5, True, 0.0)
    v1 = refine_raw._per_bin_neg(c, Wz, cgz, 0.5, True, 0.0)
    assert np.isfinite(v1) and abs(v1 - v0) < 1e-6
    v2 = refine_raw._per_bin_neg(c, Wz, cgz, 0.5, True, 0.0, warm={})
    assert abs(v2 - v0) < 1e-6


def _raw(rng, n=400, sig=0.05, damped=True):
    """heat u_t = 0.1 u_xx at kappa 1, 3 plus (damped) a mode of tau + 0.5 at kappa 4 (lambda = -0.5,
    heat would give -1.6), at n scattered points."""
    ts, xs = rng.uniform(0, 2, n), rng.uniform(0, 2 * np.pi, n)
    ys = np.exp(-0.1 * ts) * np.cos(xs) + 0.5 * np.exp(-0.9 * ts) * np.sin(3 * xs)
    if damped:
        ys = ys + 0.8 * np.exp(-0.5 * ts) * np.cos(4 * xs + 0.3)
    return dict(ts=ts, xs=xs, ys=ys + sig * rng.standard_normal(n), period=2 * np.pi, sigma=sig)


def test_drop_refused_when_the_reduced_law_fails_and_the_full_one_passes():
    raw = _raw(np.random.default_rng(1))
    full, sub = [tau - 0.1 * xi**2, tau + 0.5], [tau - 0.1 * xi**2]
    verdict, lp_sub, _, lp_full = loop.subset_drop_gof(full, sub, raw)
    assert verdict == "keep_all" and lp_sub < -10 and lp_full > loop.PRED_LOGP


def test_drop_with_both_laws_failing_is_not_claimed():
    raw = _raw(np.random.default_rng(2))
    full, sub = [tau - 0.02 * xi**2, tau + 3.0], [tau - 0.02 * xi**2]
    assert loop.subset_drop_gof(full, sub, raw)[0] == "misfit"


def test_drop_stands_when_the_reduced_law_passes():
    raw = _raw(np.random.default_rng(3), damped=False)
    full, sub = [tau - 0.1 * xi**2, tau + 0.5], [tau - 0.1 * xi**2]
    verdict, lp_sub, _, lp_full = loop.subset_drop_gof(full, sub, raw)
    assert verdict == "drop" and lp_sub > loop.PRED_LOGP and lp_full is None


def test_switch_follows_branch_ard_by_default():
    import os
    import subprocess
    import sys

    code = "from pdefactor import loop; print(loop.RAW_GOF_FINAL and loop.PATH_FULL)"
    env = {k: v for k, v in os.environ.items() if not k.startswith("PDEFACTOR_")}
    runs = [subprocess.run([sys.executable, "-c", code], env=dict(env, **e), capture_output=True, text=True)
            for e in ({}, {"PDEFACTOR_BRANCH_ARD": "0"}, {"PDEFACTOR_BRANCH_ARD": "1", "PDEFACTOR_RAW_GOF_FINAL": "0"})]
    out = [r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-500:] for r in runs]
    assert out == ["True", "False", "False"]  # bundle on by default since 2026-11-01


def _path_field(sig=1e-3, seed=0):
    """lambda(kappa) = -0.05 + 0.3 i kappa - 0.1 kappa^2 + 0.002 kappa^4 as a real field: the factor
    tau + 0.05 - 0.3 xi - 0.1 xi^2 - 0.002 xi^4 (xi = i kappa) uses every real term up to xi^4 but xi^3."""
    t = np.linspace(0, 2, 64)
    x = np.linspace(0, 2 * np.pi, 32, endpoint=False)
    u = np.zeros((len(t), len(x)))
    for k in range(1, 7):
        lam = -0.05 - 0.1 * k**2 + 0.002 * k**4
        u += (1.0 / k) * np.exp(lam * t)[:, None] * np.cos(k * x[None, :] + 0.3 * k * t[:, None] + 0.3 * k)
    rng = np.random.default_rng(seed)
    return t, x, u + sig * rng.standard_normal(u.shape), sig


def _report(q):
    c = loop._coef_dict(q)
    return loop.FactorReport(q, 1.0, {k: (complex(v),) * 3 for k, v in c.items()})


def test_t102_support_path_starts_at_the_full_support(monkeypatch):
    """T102: with PATH_FULL the backward-elimination path holds the full rectangular support it starts
    from (here {1, xi, xi^2, xi^3, xi^4}) as its first element; without it the first element already
    lacks one term."""
    t, x, u, sig = _path_field()
    f = _report(tau + 0.05 - 0.3 * xi - 0.1 * xi**2 - 0.002 * xi**4)
    full = {(1, 0), (0, 0), (0, 1), (0, 2), (0, 3), (0, 4)}
    monkeypatch.setattr(loop, "PATH_FULL", False)
    first = [set(p[0]) for p in loop.support_path([f], u, t, x, sig)[0][:-1]]  # the last path is Wald's
    assert first and all(len(s) < len(full) for s in first)
    monkeypatch.setattr(loop, "PATH_FULL", True)
    paths = loop.support_path([f], u, t, x, sig)[0][:-1]
    assert set(paths[0][0]) == full
    assert [len(p) for p in paths] == [len(p) + 1 for p in loop.support_path.__wrapped__([f], u, t, x, sig)[0][:-1]] \
        if hasattr(loop.support_path, "__wrapped__") else True
    assert abs(paths[0][0][(0, 3)]) < 1e-3  # the LS value of the absent xi^3 term is ~0
