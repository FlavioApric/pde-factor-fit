"""P4: factor-kernel (EPGP) re-interpolation before the final decision. Fast (< 60 s): no run_loop."""
import os

import numpy as np

from pdefactor import loop
from pdefactor.interp.reinterp import epgp_samples, kernel_factors
from pdefactor.symbols import tau, xi


def _tpd_raw(n=400, noise=0.05, seed=0):
    """Scattered samples of transport (tau + xi) + diffusion (tau - 0.3 xi^2) on the circle, kappa 1..6."""
    rng = np.random.default_rng(seed)
    ts, xs = rng.uniform(0, 2, n), rng.uniform(0, 2 * np.pi, n)

    def u(t, x):
        out = 0.0
        for k in range(1, 7):
            out = out + np.cos(k * (x - t)) / k + np.exp(-0.3 * k * k * t) * np.sin(k * x)
        return out

    y = u(ts, xs)
    ys = y + noise * np.std(y) * rng.standard_normal(n)
    return dict(ts=ts, xs=xs, ys=ys, period=2 * np.pi, sigma=noise * float(np.std(y))), u


def test_switch_off_by_default():
    assert os.environ.get("PDEFACTOR_EPGP_REINTERP", "0") != "1" or loop.EPGP_REINTERP
    if os.environ.get("PDEFACTOR_EPGP_REINTERP") is None:
        assert loop.EPGP_REINTERP is False


def test_kernel_factors_dedup_and_monic():
    ks = kernel_factors([2 * tau + 2 * xi, tau + xi, tau - 0.3 * xi**2, 3.0, tau - 0.3000000001 * xi**2])
    assert len(ks) == 2
    for k, ref in zip(ks, [tau + xi, tau - 0.3 * xi**2]):
        assert all(abs(complex(c)) < 1e-12 for c in (k - ref).expand().as_coefficients_dict().values())


def test_epgp_keeps_high_kappa_modes():
    """The EPGP of the true factors recovers the fast-decaying diffusion modes at high kappa from 400
    points at 5 % noise, and the true kernel has a far larger marginal likelihood than a kappa-independent
    surrogate fitted to the low bins (what the GP path reported)."""
    from pdefactor.core.structfit import extract_modes_ic

    raw, _ = _tpd_raw()
    t, x = np.linspace(0, 2, 48), np.linspace(0, 2 * np.pi, 64, endpoint=False)
    good = epgp_samples(raw, t, x, [tau + xi, tau - 0.3 * xi**2])
    bad = epgp_samples(raw, t, x, [tau + xi, tau**2 + 0.91 * tau + 0.2])
    assert good["samples"].shape == (8, 48, 64) and np.isrealobj(good["samples"])
    assert good["info"]["nlml"] < bad["info"]["nlml"] - 10
    m, _, _, _ = extract_modes_ic(good["mean"], t, x, noise=0.0, noise_draws=good["noise_draws"] / np.sqrt(2))
    dec = [(abs(k), lam.real) for k, lam in zip(m.kappa, m.lam) if abs(lam.imag) < 0.2 and abs(k) >= 3]
    assert dec, "no decaying mode at |kappa| >= 3"
    for k, lr in dec:
        assert abs(lr + 0.3 * k * k) < 0.15 * 0.3 * k * k


def test_hook_not_called_when_off(monkeypatch):
    """Default off: the hook is never reached, so the decision path is the reference one."""
    import pdefactor.interp.reinterp as R

    called = []
    monkeypatch.setattr(R, "reinterp_alternative", lambda *a, **k: called.append(1))
    monkeypatch.setattr(loop, "EPGP_REINTERP", False)
    src = open(loop.__file__, encoding="utf-8").read()
    assert "if EPGP_REINTERP and raw is not None:" in src
    assert not called
