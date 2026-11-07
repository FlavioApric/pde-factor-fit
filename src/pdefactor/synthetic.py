"""Synthetic exact solutions of linear constant-coefficient PDEs in 1+1, with ground truth.

A field is a sum of components; component j solves Q_j(d_t, d_x) u_j = 0 and is a finite
sum of modes A e^{lam t + i kappa x} with Q_j(lam, i kappa) = 0 (Ehrenpreis-Palamodov).
Real fields are obtained by adding the conjugate mode (valid for real symbols).
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import sympy as sp

from .symbols import tau, xi


def branch_roots(Q, kappa):
    """All lam with Q(lam, i kappa) = 0 (numerically), for a monic-in-tau factor Q."""
    p = sp.Poly(sp.expand(Q), tau)
    coeffs = [complex(sp.N(c.subs(xi, sp.I * kappa))) for c in p.all_coeffs()]
    return np.roots(coeffs)


@dataclass
class Component:
    name: str
    Q: sp.Expr  # factor symbol
    kappas: np.ndarray
    lams: np.ndarray
    amps: np.ndarray
    real: bool = True
    tpows: np.ndarray | None = None  # power of t per mode: t^p e^{lam t} (repeated roots, OPF-T2)

    def __call__(self, t, x):
        t = np.asarray(t, float)[..., None]
        x = np.asarray(x, float)[..., None]
        tp = 1.0 if self.tpows is None else t ** self.tpows
        z = (self.amps * tp * np.exp(self.lams * t + 1j * self.kappas * x)).sum(-1)
        return 2 * z.real if self.real else z


@dataclass
class Field:
    name: str
    components: list
    terms: dict = field(default_factory=dict)  # factor name -> {n: c_n} for evolution factors
    note: str = ""

    def __call__(self, t, x):
        return sum(c(t, x) for c in self.components)

    @property
    def P(self):
        return sp.expand(sp.prod([c.Q for c in self.components]))

    def weights(self, t, x):
        """Ground-truth weight w_j = ||u_j|| / sum_k ||u_k|| on the given points."""
        n = np.array([np.linalg.norm(c(t, x)) for c in self.components])
        return n / n.sum()


def modal_component(name, Q, kappas, amp_fn, branch="all", rng=None):
    """Component with modes on every root branch of Q at each kappa."""
    ks, ls, As = [], [], []
    for k in kappas:
        roots = branch_roots(Q, k)
        if branch != "all":
            roots = roots[[branch]]
        for lam in roots:
            ks.append(k)
            ls.append(lam)
            phase = np.exp(2j * np.pi * rng.random()) if rng is not None else 1.0
            As.append(amp_fn(k) * phase)
    return Component(name, Q, np.array(ks, float), np.array(ls, complex), np.array(As, complex))


def default_kappas(L=2 * np.pi, kmax=8, n=None):
    """Wavenumbers 2 pi m / L, m = 1..n (n modes up to kmax)."""
    base = 2 * np.pi / L
    m = np.arange(1, int(kmax / base) + 1) if n is None else np.arange(1, n + 1)
    return base * m


# ---------------------------------------------------------------- cases
def _amp(k, s=1.5):
    return np.exp(-(k / s) ** 2 / 2)


def case(name, seed=0, kmax=6.0, L=2 * np.pi):
    """Named v1 cases. Each returns a Field with ground truth."""
    rng = np.random.default_rng(seed)
    K = default_kappas(L, kmax)
    c, D = 1.0, 0.3
    if name == "transport":
        Q = tau + c * xi
        return Field(name, [modal_component("transport", Q, K, _amp, rng=rng)], {"transport": {1: -c}})
    if name == "heat":
        Q = tau - D * xi**2
        return Field(name, [modal_component("diffusion", Q, K, _amp, rng=rng)], {"diffusion": {2: D}})
    if name == "advection_diffusion":
        Q = tau + c * xi - D * xi**2
        return Field(name, [modal_component("adv-diff", Q, K, _amp, rng=rng)], {"adv-diff": {1: -c, 2: D}})
    if name == "transport_plus_diffusion":
        # the note's structure P = (tau + xi)(tau - D xi^2) with rich data (many modes per factor)
        Q1, Q2 = tau + c * xi, tau - D * xi**2
        return Field(
            name,
            [
                modal_component("transport", Q1, K, lambda k: 0.7 * _amp(k), rng=rng),
                modal_component("diffusion", Q2, K, lambda k: 0.3 * _amp(k), rng=rng),
            ],
            {"transport": {1: -c}, "diffusion": {2: D}},
        )
    if name == "wave":
        Q1, Q2 = tau - c * xi, tau + c * xi
        return Field(
            name,
            [modal_component("right", Q2, K, _amp, rng=rng), modal_component("left", Q1, K, lambda k: 0.5 * _amp(k), rng=rng)],
            {"right": {1: -c}, "left": {1: c}},
        )
    if name == "beam":
        Q1, Q2 = tau - sp.I * D * xi**2, tau + sp.I * D * xi**2
        return Field(
            name,
            [modal_component("schr+", Q1, K, _amp, rng=rng), modal_component("schr-", Q2, K, lambda k: 0.5 * _amp(k), rng=rng)],
            {"schr+": {2: sp.I * D}, "schr-": {2: -sp.I * D}},
            note="complex factors; each real component contains both conjugate branches, "
            "so per-factor ground-truth weights are not defined by Field.weights (they are 1/2, 1/2)",
        )
    if name == "klein_gordon":
        m = 1.0
        Q = tau**2 - xi**2 + m**2
        return Field(name, [modal_component("KG", Q, K, _amp, rng=rng)], {}, note="irreducible 2nd order in tau")
    if name == "telegraph":
        g = 0.4
        Q = tau**2 + 2 * g * tau - c**2 * xi**2
        return Field(name, [modal_component("telegraph", Q, K, _amp, rng=rng)], {}, note="irreducible 2nd order in tau")
    if name == "airy":
        Q = tau + 0.05 * xi**3
        return Field(name, [modal_component("airy", Q, K, _amp, rng=rng)], {"airy": {3: -0.05}})
    if name == "schrodinger":
        Q = tau - sp.I * D * xi**2
        comp = modal_component("schr", Q, K, _amp, rng=rng)
        comp.real = False  # complex field: a real part would add the conjugate branch tau + i D xi^2
        return Field(name, [comp], {"schr": {2: sp.I * D}}, note="complex symbol, complex field")
    raise KeyError(name)


CASES = [
    "transport", "heat", "advection_diffusion", "transport_plus_diffusion",
    "wave", "beam", "klein_gordon", "telegraph", "airy", "schrodinger",
]


# Extra cases (Phase 1 v2): not in CASES, because the v1 core is not expected to handle them.
EXTRA_CASES = ["tpd_shared_kappa0", "repeated_transport", "fifth_order"]


def extra_case(name, seed=0, kmax=6.0, L=2 * np.pi):
    """tpd_shared_kappa0: transport + diffusion plus a constant, the kappa = 0 mode lam = 0 that lies
    on both varieties (delta(P) > 0 path, C12-T2).
    repeated_transport: P = (tau + xi)^2, modes (A + B t) e^{i kappa (x - t)} (OPF-T2, OPF5B-T6)."""
    rng = np.random.default_rng(seed)
    K = default_kappas(L, kmax)
    if name == "tpd_shared_kappa0":
        f = case("transport_plus_diffusion", seed=seed, kmax=kmax, L=L)
        tr = f.components[0]
        f.components[0] = Component(tr.name, tr.Q, np.r_[0.0, tr.kappas], np.r_[0j, tr.lams], np.r_[0.1 + 0j, tr.amps])
        f.name = name
        f.note = "the constant (kappa = 0, lam = 0) is shared by both factors; it is stored in the transport component"
        return f
    if name == "repeated_transport":
        Q = tau + xi
        c = modal_component("transport", Q, K, _amp, rng=rng)
        comp = Component("transport^2", Q**2, np.r_[c.kappas, c.kappas], np.r_[c.lams, c.lams],
                         np.r_[c.amps, 0.5 * c.amps], tpows=np.r_[np.zeros(len(K)), np.ones(len(K))])
        return Field(name, [comp], {}, note="repeated factor: the only correct output is UNDECIDED")
    if name == "fifth_order":
        # dx = 5 lies outside core v2's default class (dx <= 4): exercises degree growth in the loop
        Q = tau + 0.002 * xi**5
        return Field(name, [modal_component("fifth", Q, K, _amp, rng=rng)], {"fifth": {5: -0.002}})
    raise KeyError(name)


# Generalisation families (plan v2.13): held out, never used to tune the pipeline. Shapes the 10 v1
# cases do not cover: damped odd dispersion, growing modes, irreducible damped order 2 in a real
# field, mixed tau*xi terms, three factors, two conjugate pairs, an irreducible order-3 law, rescaled
# coefficients and other excitation spectra.
GENERAL_CASES = [
    "damped_airy_drift", "ks_linear", "damped_beam", "kg_drift", "wave_heat", "two_pairs",
    "cubic_tau", "transport_fast", "tpd_scaled", "advdiff_flat", "wave_lowk",
]


def general_case(name, seed=0, kmax=6.0, L=2 * np.pi):
    rng = np.random.default_rng(seed)
    K = default_kappas(L, kmax)
    one = lambda nm, Q, amp=_amp, ks=K: Field(name, [modal_component(nm, Q, ks, amp, rng=rng)])  # noqa: E731
    if name == "damped_airy_drift":
        return one("airy-d", tau + sp.Float(0.1) + xi + sp.Float(0.05) * xi**3)
    if name == "ks_linear":
        # linear Kuramoto-Sivashinsky: Re lam = 0.05 k^2 - 0.01 k^4 > 0 for k <= 2 (growing modes)
        return one("ks", tau + sp.Float(0.05) * xi**2 + sp.Float(0.01) * xi**4)
    if name == "damped_beam":
        # tau^2 + 0.2 tau + 0.03 xi^4: discriminant not a square, irreducible over C; real field
        return one("dbeam", tau**2 + sp.Float(0.2) * tau + sp.Float(0.03) * xi**4)
    if name == "kg_drift":
        return one("kgd", tau**2 + sp.Float(0.5) * tau * xi - xi**2 + 1)
    if name == "wave_heat":
        return Field(name, [modal_component("right", tau + xi, K, _amp, rng=rng),
                            modal_component("left", tau - xi, K, lambda k: 0.5 * _amp(k), rng=rng),
                            modal_component("heat", tau - sp.Float(0.3) * xi**2, K, lambda k: 0.4 * _amp(k), rng=rng)])
    if name == "two_pairs":
        # real field from two complex factors: (tau -+ 0.3 i xi^2) and (tau + 0.2 -+ 0.1 i xi^2)
        return Field(name, [modal_component("p1", tau - sp.I * sp.Float(0.3) * xi**2, K, _amp, rng=rng),
                            modal_component("p2", tau + sp.Float(0.2) - sp.I * sp.Float(0.1) * xi**2, K,
                                            lambda k: 0.6 * _amp(k), rng=rng)])
    if name == "cubic_tau":
        # tau^3 + 0.6 tau^2 + (1 - xi^2) tau + 0.2: Routh-Hurwitz stable for every real kappa
        return one("cubic", tau**3 + sp.Float(0.6) * tau**2 + (1 - xi**2) * tau + sp.Float(0.2))
    if name == "transport_fast":
        return one("tfast", tau + 10 * xi)
    if name == "tpd_scaled":
        return Field(name, [modal_component("transport", tau + 3 * xi, K, lambda k: 0.7 * _amp(k), rng=rng),
                            modal_component("diffusion", tau - sp.Float(0.05) * xi**2, K, lambda k: 0.3 * _amp(k), rng=rng)])
    if name == "advdiff_flat":
        return one("adf", tau + xi - sp.Float(0.05) * xi**2, amp=lambda k: 1.0)
    if name == "wave_lowk":
        Kl = default_kappas(L, 3.0)
        return Field(name, [modal_component("right", tau + xi, Kl, _amp, rng=rng),
                            modal_component("left", tau - xi, Kl, lambda k: 0.5 * _amp(k), rng=rng)])
    raise KeyError(name)


def any_case(name, seed=0, **kw):
    """Any named case: v1 CASES, EXTRA_CASES or GENERAL_CASES."""
    if name in CASES:
        return case(name, seed=seed, **kw)
    if name in EXTRA_CASES:
        return extra_case(name, seed=seed, **kw)
    return general_case(name, seed=seed, **kw)


def note_example():
    """The note's example 0.7 e^{-(x-t)^2} + 0.3 e^{-t} cos x (closed form, not modal)."""
    def u(t, x):
        return 0.7 * np.exp(-((x - t) ** 2)) + 0.3 * np.exp(-t) * np.cos(x)
    return u


def grid(field_, T=2.0, L=2 * np.pi, nt=64, nx=128, x0=0.0):
    t = np.linspace(0, T, nt)
    x = x0 + np.linspace(0, L, nx, endpoint=False)
    TT, XX = np.meshgrid(t, x, indexing="ij")
    return t, x, field_(TT, XX)


def sample_scattered(field_, n, noise=0.0, T=2.0, L=2 * np.pi, rng=None, relative=True):
    """n uniform random samples (t_i, x_i, y_i) with Gaussian noise (relative to the field's std)."""
    rng = np.random.default_rng(rng)
    t = rng.uniform(0, T, n)
    x = rng.uniform(0, L, n)
    y = field_(t, x)
    s = noise * (np.std(y) if relative else 1.0)
    return t, x, y + s * rng.standard_normal(n), s
