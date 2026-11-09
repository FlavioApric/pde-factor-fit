"""Random linear constant-coefficient PDEs in 1+1 by family (PHASE4_ML_PLAN P0.3; plan v2.13).

The named cases of synthetic.py were used to debug the pipeline, so they cannot test whether the fixes
are general. Here a symbol is drawn from a declared prior per family, its modes are excited with a
random amplitude law, and the truth is known by construction. Nothing in the pipeline reads this
module, so it is a held-out test bed.

Families (PHASE4 P0.3):
  F1  real first order, dissipative: tau + sum_b c_b xi^b with real c_b (transport, heat, adv-diff,
      damped Airy, linear KS)
  F2  dispersive: a complex or odd real symbol, |Re lam| small (Schroedinger, Airy, beam-like pairs)
  F3  second order in tau, irreducible: tau^2 + p1(xi) tau + p0(xi), real (wave-like, KG, telegraph,
      damped beam)
  F4  products of 2-3 factors from F1-F3, total tau-order <= 3
  F5  edge cases: a pure decay factor tau + c, few excited kappa, a third-order irreducible law

Every draw is checked: Q_j(lam, i kappa) = 0 for each mode (exact dispersion), Re lam <= RE_MAX on the
band (stable up to a slow growth), |lam| below the time Nyquist of the default grid, and the slowest
decay per mode lets it live at least a fraction of T (else the mode carries no information; such
modes are dropped rather than kept as invisible truth).
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import sympy as sp

from .symbols import tau, xi
from .synthetic import Component, Field, branch_roots

FAMILIES = ("F1", "F2", "F3", "F4", "F5")
T_DEFAULT, NT_DEFAULT = 2.0, 64
RE_MAX = 0.1  # slow growth allowed (linear KS)
LAM_MAX = 0.8 * np.pi / (T_DEFAULT / (NT_DEFAULT - 1))  # below the time Nyquist of the default grid
DECAY_MIN_LIFE = 0.1  # a mode must keep e^{-1} of its amplitude for at least this fraction of T


@dataclass
class Draw:
    field: Field
    family: str
    factors: list  # true factors (sympy); a complex factor of a real field is listed with its conjugate
    kappas: np.ndarray
    amp_law: str
    seed: int

    @property
    def name(self):
        return f"{self.family}-{self.seed}"


def _logu(rng, lo, hi):
    return float(np.exp(rng.uniform(np.log(lo), np.log(hi))))


def _sign(rng):
    return 1.0 if rng.random() < 0.5 else -1.0


def _num(v, nd=3):
    """Round a coefficient to nd significant digits (readable truth; exact as a float)."""
    if v == 0:
        return 0.0
    return float(f"{v:.{nd}g}")


def _first_order(rng, kmax, dispersive=False):
    """tau + sum_b c_b xi^b. Dissipative: Re lam = -sum_{b even} c_b (i)^b kappa^b <= RE_MAX.
    lam = -sum_b c_b (i kappa)^b: b = 1 transport, b = 2 diffusion when c_2 < 0, b = 3 Airy,
    b = 4 hyperdiffusion when c_4 > 0."""
    dx = int(rng.integers(1, 5))
    c = {}
    for b in range(dx + 1):
        if b < dx and rng.random() < 0.4:
            continue
        # magnitudes scaled so that |c_b| kmax^b stays O(0.3..6)
        mag = _logu(rng, 0.3, 6.0) / kmax**b
        if b % 2 == 0:
            # even powers set the decay: (i kappa)^b = (-1)^(b/2) kappa^b; choose the dissipative sign
            s = -1.0 if (b // 2) % 2 == 1 else 1.0
            if b == 0:
                s = 1.0  # tau + c, c > 0 decays
            if dispersive:
                mag *= 0.1
            c[b] = s * mag
        else:
            c[b] = _sign(rng) * mag
    if not any(b >= 1 for b in c):
        c[1] = _sign(rng) * _logu(rng, 0.3, 3.0)
    Q = tau + sum(sp.Float(_num(v)) * xi**b for b, v in c.items())
    if dispersive and rng.random() < 0.6:
        # complex symbol (Schroedinger-like): tau - i a xi^2 (+ i b xi^4), lam = -i a kappa^2 ...
        a = _sign(rng) * _logu(rng, 0.3, 6.0) / kmax**2
        Q = Q - sp.I * sp.Float(_num(a)) * xi**2
    return sp.expand(Q)


def _second_order(rng, kmax):
    """tau^2 + p1(xi) tau + p0(xi), real: damping p1 >= 0 at xi = i kappa and a restoring p0."""
    p1 = 0
    if rng.random() < 0.6:
        p1 += sp.Float(_num(_logu(rng, 0.05, 1.0)))  # telegraph-like damping
    if rng.random() < 0.3:
        p1 += sp.Float(_num(_sign(rng) * _logu(rng, 0.1, 1.0))) * xi  # drift (KG with drift)
    kind = rng.integers(0, 3)
    if kind == 0:  # wave-like: -c^2 xi^2 (+ m^2)
        p0 = -sp.Float(_num(_logu(rng, 0.3, 3.0) ** 2)) * xi**2
        if rng.random() < 0.5:
            p0 += sp.Float(_num(_logu(rng, 0.3, 2.0)))
    elif kind == 1:  # beam-like: a xi^4
        p0 = sp.Float(_num(_logu(rng, 0.3, 6.0) / kmax**4)) * xi**4
    else:  # mixed
        p0 = -sp.Float(_num(_logu(rng, 0.1, 1.0))) * xi**2 + sp.Float(_num(_logu(rng, 0.3, 4.0) / kmax**4)) * xi**4
    return sp.expand(tau**2 + p1 * tau + p0)


def _third_order(rng, kmax):
    """tau^3 + a tau^2 + (b - c xi^2) tau + d, Routh-Hurwitz: a, b + c kappa^2, d > 0 and
    a (b + c kappa^2) > d for every kappa (checked numerically by the caller)."""
    a = _logu(rng, 0.3, 1.5)
    b = _logu(rng, 0.3, 2.0)
    c = _logu(rng, 0.2, 1.5)
    d = min(_logu(rng, 0.05, 1.0), 0.8 * a * b)
    return sp.expand(tau**3 + sp.Float(_num(a)) * tau**2 + (sp.Float(_num(b)) - sp.Float(_num(c)) * xi**2) * tau
                     + sp.Float(_num(d)))


def _amp_law(rng):
    kind = ("gauss", "power", "flat")[int(rng.integers(0, 3))]
    if kind == "gauss":
        s = rng.uniform(1.0, 3.0)
        return kind, lambda k: np.exp(-(k / s) ** 2 / 2)
    if kind == "power":
        p = rng.uniform(1.0, 3.0)
        return kind, lambda k: (1.0 + k) ** (-p)
    return kind, lambda k: np.ones_like(np.asarray(k, float))


def _admissible(Q, kappas, T=T_DEFAULT):
    """Every root on the band: Re lam <= RE_MAX, |lam| < LAM_MAX; and the field is not dead:
    at least one root per kappa lives for DECAY_MIN_LIFE T."""
    for k in kappas:
        r = branch_roots(Q, k)
        if np.any(r.real > RE_MAX) or np.any(np.abs(r) > LAM_MAX):
            return False
    return True


def _component(name, Q, kappas, amp_fn, rng, T=T_DEFAULT):
    ks, ls, As = [], [], []
    for k in kappas:
        for lam in branch_roots(Q, k):
            if -lam.real * DECAY_MIN_LIFE * T > 1.0:
                continue  # dead after a tenth of T: no information, not counted as truth
            ks.append(k)
            ls.append(lam)
            As.append(amp_fn(k) * np.exp(2j * np.pi * rng.random()))
    return Component(name, Q, np.array(ks, float), np.array(ls, complex), np.array(As, complex))


def _is_real(Q):
    return all(sp.im(sp.N(c)) == 0 for c in sp.Poly(Q, tau, xi).coeffs())


def random_pde(family, seed=0, L=2 * np.pi, max_tries=200):
    """One random PDE of the family, as a Draw with its true factors."""
    if family not in FAMILIES:
        raise KeyError(family)
    rng = np.random.default_rng([FAMILIES.index(family), seed])
    base = 2 * np.pi / L
    for _ in range(max_tries):
        kmax_i = int(rng.integers(3, 11))  # number of excited kappa
        if family == "F5" and rng.random() < 0.5:
            kmax_i = int(rng.integers(2, 4))  # few excited kappa
        kappas = base * np.arange(1, kmax_i + 1)
        kmax = kappas[-1]
        law, amp = _amp_law(rng)
        if family == "F1":
            Qs = [_first_order(rng, kmax)]
        elif family == "F2":
            Qs = [_first_order(rng, kmax, dispersive=True)]
        elif family == "F3":
            Qs = [_second_order(rng, kmax)]
        elif family == "F4":
            k = int(rng.integers(2, 4))
            Qs, m = [], 0
            while len(Qs) < k:
                pick = rng.random()
                if pick < 0.3 and m + 2 <= 3:
                    Qs.append(_second_order(rng, kmax))
                    m += 2
                elif m + 1 <= 3:
                    Qs.append(_first_order(rng, kmax, dispersive=rng.random() < 0.3))
                    m += 1
                else:
                    break
            if len(Qs) < 2 or len({sp.srepr(q) for q in Qs}) < len(Qs):
                continue
        else:
            pick = rng.random()
            if pick < 0.4:
                Qs = [tau + sp.Float(_num(_logu(rng, 0.1, 1.0))), _first_order(rng, kmax)]
            else:
                Qs = [_third_order(rng, kmax)]
        if not all(_admissible(Q, kappas) for Q in Qs):
            continue
        ws = rng.dirichlet(np.full(len(Qs), 2.0)) if len(Qs) > 1 else np.ones(1)
        comps = []
        for j, (Q, w) in enumerate(zip(Qs, ws)):
            comps.append(_component(f"f{j}", Q, kappas, lambda k, w=w: w * amp(k), rng))
        if any(len(c.lams) == 0 for c in comps):
            continue
        factors = []
        for Q in Qs:
            factors.append(Q)
            if not _is_real(Q):
                factors.append(sp.expand(sp.conjugate(Q).subs({sp.conjugate(tau): tau, sp.conjugate(xi): xi})))
        f = Field(f"{family}-{seed}", comps, note=f"amp={law}, kappa 1..{kmax_i}")
        return Draw(f, family, factors, kappas, law, seed)
    raise RuntimeError(f"no admissible draw for {family} seed {seed}")


def check_dispersion(draw, tol=1e-8):
    """max |Q_j(lam, i kappa)| / scale over all modes of all components (0 for an exact draw)."""
    worst = 0.0
    for c in draw.field.components:
        f = sp.lambdify((tau, xi), c.Q, "numpy")
        v = np.abs(f(c.lams, 1j * c.kappas))
        worst = max(worst, float(np.max(v / (1 + np.abs(c.lams) ** 3))) if len(v) else 0.0)
    return worst


def match(true_factors, found, rel=0.1, floor=0.01):
    """Right factor set, scale-aware: same number of factors and a one-to-one matching in which every
    coefficient satisfies |c - g| <= rel * max(|c|, floor * s), s = the factor's largest coefficient
    other than the leading one (a 0.01 xi^4 term is judged against 0.01, not against 0.05 absolute).
    Returns (ok, worst relative error)."""
    from itertools import permutations

    def cd(q):
        p = sp.Poly(sp.expand(sp.N(q)), tau, xi, domain="CC")
        lead = complex(dict(zip(p.monoms(), p.coeffs())).get((p.degree(tau), 0), 1))
        return {mo: complex(c) / lead for mo, c in zip(p.monoms(), p.coeffs())}

    T = [cd(q) for q in true_factors]
    F = [cd(q) for q in found]
    if len(T) != len(F):
        return False, np.inf

    def err(t, f):
        s = max([abs(v) for mo, v in t.items() if mo[0] < max(m[0] for m in t)] or [1.0])
        return max(abs(t.get(k, 0) - f.get(k, 0)) / max(abs(t.get(k, 0)), floor * s) for k in set(t) | set(f))

    best = np.inf
    for perm in permutations(range(len(F))):
        best = min(best, max(err(T[i], F[j]) for i, j in enumerate(perm)))
    return bool(best <= rel), float(best)
