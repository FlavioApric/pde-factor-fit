"""Corpus I: injected failures on simulator draws (sessions/LEARNED/V1/PLAN.md sec. 1).

Failure targets only, never fitting targets (LEARNED PLAN sec. 1.8). Every generator is generic in
the factor structure and the tau-order: it works on the product Q of the draw's true factors (a
real polynomial, monic in tau), never on a named case.

Strength is scale-free (rule 8):
- the four law deviations (two_laws, nonlinear, varcoef, fractional) are set by the omnibus
  chi^2 z-score of the injected deviation against the noise, z = ||u_eps - u_0||^2 /
  (sigma^2 sqrt(2N)), N = nt nx: the expected excess of the V0.1 omnibus statistic if the clean law
  were fitted exactly. The injection parameter is found by bisection per draw;
- coloured noise by its AR(1) correlation rho (same rho in t and x, marginal variance sigma^2);
- heteroscedastic noise by the ratio max sigma / min sigma (mean variance sigma^2);
- aliasing by r = max|Im lambda| dt / pi of the frame-shifted law Q(tau + V xi, xi).
"""
from __future__ import annotations

import numpy as np
import sympy as sp

TYPES = ("two_laws", "coloured", "heteroscedastic", "nonlinear", "varcoef", "fractional", "aliasing")
LEVELS = {
    "two_laws": (2.0, 8.0, 32.0),
    "nonlinear": (2.0, 8.0, 32.0),
    "varcoef": (2.0, 8.0, 32.0),
    "fractional": (2.0, 8.0, 32.0),
    "coloured": (0.3, 0.6, 0.9),
    "heteroscedastic": (2.0, 5.0, 20.0),
    "aliasing": (1.2, 2.0, 3.0),
}
NOISE = 0.05
NSUB = 8  # solver sub-steps per observation step


# ------------------------------------------------------------------ the law as a companion system
def law_poly(factors):
    """Q = prod(factors) as {j: callable a_j(xi)} with Q = tau^m + sum_{j<m} a_j(xi) tau^j."""
    from pdefactor.symbols import tau, xi

    Q = sp.expand(sp.prod(factors))
    p = sp.Poly(Q, tau)
    lc = sp.simplify(p.LC())
    if lc.free_symbols:
        raise ValueError("Q is not monic in tau with a constant leading coefficient")
    m = p.degree()
    co = {m - i: sp.expand(c / lc) for i, c in enumerate(p.all_coeffs())}
    return m, {j: co.get(j, sp.Integer(0)) for j in range(m)}


def _num(c):
    from pdefactor.symbols import xi

    f = sp.lambdify(xi, c, "numpy")
    return lambda z: np.broadcast_to(np.asarray(f(z), complex), np.shape(z)).copy()


def companion(m, a, kappa):
    """Per kappa the m x m matrix A with d/dt (u, u_t, ..) = A (..) in Fourier (xi = i kappa)."""
    z = 1j * kappa
    A = np.zeros((len(kappa), m, m), complex)
    for j in range(m - 1):
        A[:, j, j + 1] = 1.0
    for j in range(m):
        A[:, m - 1, j] = -_num(a[j])(z)
    return A


def _expm_batch(A, h):
    from scipy.linalg import expm

    return np.stack([expm(Ak * h) for Ak in A])


def initial_state(field, m, x):
    """(m, nx) physical-space time derivatives d^j u / dt^j at t = 0 from the modal sum."""
    out = np.zeros((m, len(x)), complex)
    for c in field.components:
        tp = 0 if c.tpows is None else c.tpows
        if np.any(tp):
            raise ValueError("repeated roots (t^p e^{lam t}) are not supported by the solver")
        for j in range(m):
            z = (c.amps * c.lams**j * np.exp(1j * np.outer(x, c.kappas))).sum(-1)
            out[j] += 2 * z.real if c.real else z
    return out


def solve(field, factors, t, x, forcing=None, law_switch=None):
    """Integrate Q(d_t, d_x) u = forcing(u, x) from the draw's state at t = 0, on the grid (t, x).
    Integrating-factor RK4 with the exact linear propagator per kappa (no stiffness limit).
    forcing: callable(V, kappa) -> physical forcing on the top equation (V: (nx, m) Fourier state
    of u, u_t, ..), or None.
    law_switch: (t_s, factors_B): the law changes at t_s (state continuous)."""
    nx, nt = len(x), len(t)
    L = x[1] - x[0]
    kappa = 2 * np.pi * np.fft.fftfreq(nx, d=L)
    m, a = law_poly(factors)
    V = np.fft.fft(initial_state(field, m, x), axis=1).T  # (nx, m)
    dt = t[1] - t[0]
    h = dt / NSUB
    dealias = np.abs(np.fft.fftfreq(nx) * nx) <= nx / 3

    def props(fac):
        mm, aa = law_poly(fac)
        if mm != m:
            raise ValueError("law switch must keep the tau-order")
        A = companion(m, aa, kappa)
        return _expm_batch(A, h), _expm_batch(A, h / 2)

    E, E2 = props(factors)
    switched = law_switch is None

    def N(Vs):
        if forcing is None:
            return np.zeros_like(Vs)
        g = np.fft.fft(forcing(Vs, kappa)) * dealias
        out = np.zeros_like(Vs)
        out[:, m - 1] = g
        return out

    def mv(M, v):
        return np.einsum("kij,kj->ki", M, v)

    U = np.empty((nt, nx))
    U[0] = np.fft.ifft(V[:, 0]).real
    for i in range(1, nt):
        if not switched and t[i - 1] >= law_switch[0] - 1e-12:
            E, E2 = props(law_switch[1])
            switched = True
        for _ in range(NSUB):
            k1 = h * N(V)
            k2 = h * N(mv(E2, V + k1 / 2))
            k3 = h * N(mv(E2, V) + k2 / 2)
            k4 = h * N(mv(E, V) + mv(E2, k3))
            V = mv(E, V) + (mv(E, k1) + 2 * mv(E2, k2 + k3) + k4) / 6
            if not np.all(np.isfinite(V)):
                return None
        U[i] = np.fft.ifft(V[:, 0]).real
    return U


# ------------------------------------------------------------------ generators (eps -> field)
def _perturbed_law(factors, eps, g):
    """Every non-leading coefficient of Q multiplied by (1 + eps g_i), g fixed per draw."""
    from pdefactor.symbols import tau, xi

    Q = sp.Poly(sp.expand(sp.prod(factors)), tau, xi)
    m = sp.Poly(Q.as_expr(), tau).degree()
    terms = Q.terms()
    out = 0
    for i, ((p, q), c) in enumerate(terms):
        f = 1 if (p, q) == (m, 0) else (1 + eps * g[i % len(g)])
        out += sp.Float(float(sp.re(c)) * f) * tau**p * xi**q
    return [sp.expand(out)]


def _lowest_xi_term(a):
    from pdefactor.symbols import xi

    for j in sorted(a):
        part = sp.expand(a[j] - a[j].subs(xi, 0))
        if part != 0:
            return j, part
    raise ValueError("Q has no xi-dependent term")


def law_field(kind, d, t, x, eps, prm):
    """The injected noise-free field for a law deviation of strength eps (eps = 0: clean)."""
    from pdefactor.synthetic import grid

    if kind == "fractional":
        comps = []
        for c in d.field.components:
            c2 = type(c)(c.name, c.Q, c.kappas, c.lams - eps * np.abs(c.kappas) ** prm["alpha"], c.amps, c.real,
                         c.tpows)
            comps.append(c2)
        f = type(d.field)(d.field.name, comps)
        return grid(f, T=t[-1], L=x[-1] + x[1] - x[0], nt=len(t), nx=len(x))[2]
    if eps == 0:
        return grid(d.field, T=t[-1], L=x[-1] + x[1] - x[0], nt=len(t), nx=len(x))[2]
    if kind == "two_laws":
        return solve(d.field, d.factors, t, x, law_switch=(t[len(t) // 2], _perturbed_law(d.factors, eps, prm["g"])))
    if kind == "nonlinear":
        def burgers(V, k):
            return eps * np.fft.ifft(V[:, 0]).real * np.fft.ifft(1j * k * V[:, 0]).real

        return solve(d.field, d.factors, t, x, forcing=burgers)
    if kind == "varcoef":
        # (1 + eps cos x) on the xi-dependent part of the lowest tau-order coefficient a_j:
        # extra right-hand side -eps cos(x) part(d_x) d_t^j u
        m, a = law_poly(d.factors)
        j, part = _lowest_xi_term(a)
        sym, cx = _num(part), np.cos(x)

        def vc(V, k):
            return -eps * cx * np.fft.ifft(sym(1j * k) * V[:, j]).real

        return solve(d.field, d.factors, t, x, forcing=vc)
    raise KeyError(kind)


def zscore(u_eps, u0, sigma):
    if u_eps is None:
        return np.inf
    return float(np.sum((u_eps - u0) ** 2) / (sigma**2 * np.sqrt(2 * u0.size)))


def calibrate_eps(kind, d, t, x, u0, sigma, z_target, prm, iters=40):
    """Bisection (in log eps) for z(eps) = z_target; z is monotone in eps near 0 for every type."""
    lo, hi = 0.0, 1e-3
    for _ in range(60):
        if zscore(law_field(kind, d, t, x, hi, prm), u0, sigma) >= z_target:
            break
        lo, hi = hi, hi * 4
    else:
        raise RuntimeError("z target not reached")
    for _ in range(iters):
        mid = np.sqrt(lo * hi) if lo > 0 else hi / 4
        z = zscore(law_field(kind, d, t, x, mid, prm), u0, sigma)
        if z < z_target:
            lo = mid
        else:
            hi = mid
        if hi / max(lo, 1e-300) < 1.002:
            break
    return hi


# ------------------------------------------------------------------ noise generators
def ar1_noise(rng, shape, rho):
    """Separable AR(1) in t and x, unit marginal variance (stationary start)."""
    e = rng.standard_normal(shape)
    s = np.sqrt(1 - rho**2)
    for axis in (0, 1):
        e = np.moveaxis(e, axis, 0)
        out = np.empty_like(e)
        out[0] = e[0]
        for i in range(1, len(e)):
            out[i] = rho * out[i - 1] + s * e[i]
        e = np.moveaxis(out, 0, axis)
    return e


def hetero_profile(u, t, ratio, signal):
    """sigma(t, x) profile h with max h / min h = ratio and mean h^2 = 1."""
    if signal:
        v = np.abs(u) / np.abs(u).max()
        lo_v = v.min()
        # (1 + a) / (1 + a lo_v) = ratio  ->  a = (ratio - 1) / (1 - ratio lo_v)
        a = (ratio - 1) / max(1 - ratio * lo_v, 1e-12)
        h = 1 + a * v
    else:
        h = np.broadcast_to(np.exp(np.log(ratio) * (t - t[0]) / (t[-1] - t[0]))[:, None], u.shape)
    return h / np.sqrt(np.mean(h**2))


# ------------------------------------------------------------------ one injected input
def _aliased_draw(d, r, dt):
    """Frame shift tau -> tau + V xi: every lambda(kappa) -> lambda - i V kappa (Re lambda kept), a
    legal real constant-coefficient law of the same structure and order. V > 0 is the root of
    max |Im lambda'| = r pi / dt (continuous, from below the simulator's LAM_MAX < pi / dt to
    infinity), so the field is under-sampled in time by the factor r."""
    from scipy.optimize import brentq

    from pdefactor.simulator import Draw
    from pdefactor.symbols import tau, xi

    target = r * np.pi / dt
    ks = np.concatenate([c.kappas for c in d.field.components])
    lm = np.concatenate([c.lams for c in d.field.components])

    def f(V):
        return np.abs(lm.imag - V * ks).max() - target

    hi = 1.0
    while f(hi) < 0:
        hi *= 2
    V = brentq(f, 0.0, hi, xtol=1e-12)
    sh = {tau: tau + sp.Float(V) * xi}
    comps = [type(c)(c.name, sp.expand(c.Q.subs(sh, simultaneous=True)), c.kappas, c.lams - 1j * V * c.kappas,
                     c.amps, c.real, c.tpows) for c in d.field.components]
    facs = [sp.expand(q.subs(sh, simultaneous=True)) for q in d.factors]
    f_ = type(d.field)(d.field.name + f"-alias{r:g}", comps)
    return Draw(f_, d.family, facs, d.kappas, d.amp_law, d.seed), V


def inject_input(kind, level, family, seed, noise=NOISE):
    """The ll_corpus input dict for one injected run (grid design), plus inp['inject']."""
    from pdefactor.simulator import random_pde
    from pdefactor.synthetic import grid

    k_i = TYPES.index(kind)
    strength = LEVELS[kind][level]
    rng = np.random.default_rng([7, k_i, level, seed])
    d = random_pde(family, seed)
    prm = {}
    t, x, u0 = grid(d.field)
    if kind == "aliasing":
        d, V = _aliased_draw(d, strength, t[1] - t[0])
        prm["V"] = float(V)
        t, x, u0 = grid(d.field)
    sig = noise * float(np.std(u0))
    u = u0
    if kind in ("two_laws", "nonlinear", "varcoef", "fractional"):
        if kind == "two_laws":
            prm["g"] = rng.standard_normal(16).tolist()
        if kind == "fractional":
            al = rng.uniform(0.3, 1.7)
            while abs(al - 1) <= 0.1:
                al = rng.uniform(0.3, 1.7)
            prm["alpha"] = float(al)
        eps = calibrate_eps(kind, d, t, x, u0, sig, strength, prm)
        u = law_field(kind, d, t, x, eps, prm)
        prm.update(eps=float(eps), z=zscore(u, u0, sig))
    e = rng.standard_normal(u.shape)
    if kind == "coloured":
        e = ar1_noise(rng, u.shape, strength)
    elif kind == "heteroscedastic":
        signal = seed % 2 == 0
        e = e * hetero_profile(u0, t, strength, signal)
        prm["profile"] = "signal" if signal else "time"
    un = u + sig * e
    prm.pop("g", None)
    return dict(draw=d, t=t, x=x, u=u, samples=[un], pis=None, sigma=sig, noise_draws=None, raw=None,
                bootstrap=16, grid_data=un, grid_sigma=sig,
                inject=dict(type=kind, level=level, strength=strength, **prm))


# ---- feasibility subset (LL-common-brief "Scope change", 2026-10-30): 140 of the 420 runs
FAMILIES = ("F1", "F2", "F3", "F4", "F5")


def subset_tasks():
    """Every type x level x family once on seed 400 (fit: LOFO / LOTO train and held-out rows),
    plus the middle level once more per type x family, on seed 402 (cal) when type index + family
    index is even, else on seed 403 (test). Balanced: 4 rows per type x family, 20 per type, 28 per family."""
    from ll_corpus import DESIGNS

    tasks = []
    for seed in (400, 402, 403):
        for dz in DESIGNS["I"]:
            typ, lv = dz[0].split(":")
            for fi, f in enumerate(FAMILIES):
                if seed == 400 or (lv == "1" and (TYPES.index(typ) + fi) % 2 == (seed == 403)):
                    tasks.append(("I", f, seed, dz, "off"))
    return tasks


if __name__ == "__main__":  # python ll_inject.py --run out/ll_I.jsonl [--workers 3]: runs the subset, resumable
    import argparse

    from ll_corpus import done_keys, run_all

    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--clean-control", action="store_true",
                    help="the uninjected base draws of the subset (G grid, 5 %% noise, seeds 400-403), same pipeline")
    a = ap.parse_args()
    done = done_keys(a.run)
    all_tasks = ([("G", f, s, ("grid", NOISE), "off") for f in FAMILIES for s in (400, 401, 402, 403)]
                 if a.clean_control else subset_tasks())
    tasks = [t for t in all_tasks if (t[0], t[1], t[2], tuple(t[3]), t[4]) not in done]
    print(f"{len(tasks)} of {len(all_tasks)} runs to do, {a.workers} workers", flush=True)
    run_all(tasks, a.run, a.workers)
