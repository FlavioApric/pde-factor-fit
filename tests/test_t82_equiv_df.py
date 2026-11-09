"""T95: the equivalence statistic of the benchmark scoring (e13_summary.chi2_gap, switch EQUIV_DF).

A law with more kernel columns lowers the V0.1 chi^2 by ~2 per column in every bin by fitting noise
(E chi^2 = df), so the raw gap over all bins charged a lower-order law ~2 per EMPTY bin (F5-131 grid
5 %: raw gap 139, 136 of it in the 61 empty bins). With EQUIV_DF the gap is taken over the excited band
and minus the df gap: an estimate of the signal one law explains and the other does not."""
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "code" / "experiments"))

import e13_summary  # noqa: E402

from pdefactor.symbols import tau, xi  # noqa: E402
from pdefactor.synthetic import Component, Field, grid  # noqa: E402

DECAY, HEAT = tau + 0.3, tau - 0.1 * xi**2


def _data(heat_amp, seed=0, noise=0.05):
    ks = np.array([1.0, 2.0, 3.0])
    comps = [Component("d", DECAY, ks, np.full(3, -0.3 + 0j), np.array([1.0, 0.8j, -0.6]))]
    if heat_amp:
        comps.append(Component("h", HEAT, ks, -0.1 * ks**2 + 0j, heat_amp * np.array([1.0, -0.7, 0.5j])))
    t, x, u = grid(Field("t82", comps))
    sig = noise * np.std(u)
    return u + sig * np.random.default_rng(seed).standard_normal(u.shape), t, x, sig


@pytest.mark.parametrize("seed", [0, 1])
def test_unexcited_extra_factor_is_not_charged_per_empty_bin(seed, monkeypatch):
    # truth lists a second factor the data never excite: the one-factor law is data-equivalent
    u, t, x, sig = _data(0.0, seed)
    monkeypatch.setattr(e13_summary, "EQUIV_DF", False)
    raw = e13_summary.chi2_gap([DECAY], [DECAY, HEAT], u, t, x, sig)
    monkeypatch.setattr(e13_summary, "EQUIV_DF", True)
    adj = e13_summary.chi2_gap([DECAY], [DECAY, HEAT], u, t, x, sig)
    assert raw > e13_summary.DCHI2_EQUIV  # old rule: ~2 per bin of pure noise fitting -> "not equivalent"
    assert abs(adj) < e13_summary.DCHI2_EQUIV


@pytest.mark.parametrize("seed", [0, 1])
def test_missing_excited_factor_is_still_not_equivalent(seed, monkeypatch):
    # the heat factor carries signal: a law without it is wrong, also when it has extra columns elsewhere
    u, t, x, sig = _data(0.3, seed)
    monkeypatch.setattr(e13_summary, "EQUIV_DF", True)
    assert e13_summary.chi2_gap([DECAY], [DECAY, HEAT], u, t, x, sig) > e13_summary.DCHI2_EQUIV


@pytest.mark.parametrize("seed", [0, 1])
def test_extra_columns_do_not_buy_equivalence_in_empty_bins(seed, monkeypatch):
    # mirror bias (F4-128 grid 5 %: raw gap -55 over all bins, +59 in the excited band): a wrong law with
    # more kernel columns than the truth fitted noise in every empty bin and passed as "equivalent"
    u, t, x, sig = _data(0.5, seed)
    spurious = [DECAY, tau + 1.5, tau + 2.5]  # three columns per bin, none on the heat branch
    monkeypatch.setattr(e13_summary, "EQUIV_DF", False)
    assert e13_summary.chi2_gap(spurious, [DECAY, HEAT], u, t, x, sig) < e13_summary.DCHI2_EQUIV
    monkeypatch.setattr(e13_summary, "EQUIV_DF", True)
    assert e13_summary.chi2_gap(spurious, [DECAY, HEAT], u, t, x, sig) > e13_summary.DCHI2_EQUIV
