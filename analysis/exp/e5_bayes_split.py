"""E5: Friedrichs-angle Bayesian split layer (plan 0b.10), with the true factors.
u = B1 a1 + B2 a2 + e, a ~ CN(0, tau^2 I), e ~ N(0, s^2 I). Posterior a | u is Gaussian with
covariance s^2 (S^H S + s^2/tau^2 I)^{-1}; tau^2 by empirical Bayes (closed-form evidence).
Outputs per time span T (which sets theta_F, E2): c_F, coverage of the 90% interval of w_1,
mean interval width, and P(split) from the evidence of M_split vs M_1, M_2 (equal priors)."""
import sys
from pathlib import Path

import numpy as np
import sympy as sp

sys.path.insert(0, str(Path(__file__).parent))
from e2_gamma import PAIRS, Sym  # noqa: E402

from pdefactor.core.components import gamma_N, kernel_basis  # noqa: E402
from pdefactor.synthetic import case  # noqa: E402


def log_evidence(S, u, s2, tau2):
    """log N(u; 0, s2 I + tau2 S S^H), via the small Gram (Woodbury / determinant lemma)."""
    n, p = S.shape
    G = S.conj().T @ S
    M = G + (s2 / tau2) * np.eye(p)
    L = np.linalg.cholesky(M)
    b = np.linalg.solve(L, S.conj().T @ u)
    quad = (np.vdot(u, u).real - np.vdot(b, b).real) / s2
    logdet = 2 * np.log(np.abs(np.diag(L))).sum() + p * np.log(tau2 / s2) + n * np.log(s2)
    return -0.5 * (quad + logdet + n * np.log(2 * np.pi))


def eb_tau2(S, u, s2):
    grid = np.logspace(-6, 2, 33)
    ev = [log_evidence(S, u, s2, t2) for t2 in grid]
    return grid[int(np.argmax(ev))], max(ev)


def run(name="transport_plus_diffusion", Ts=(0.25, 0.5, 1.0, 2.0), noise=1e-2, seeds=20, nt=32, nx=64,
        ndraw=400):
    print(f"{name}, noise {noise:.0e}: T  c_F  coverage90(w1)  width(w1)  P(split)")
    Q1, Q2 = (Sym(q) for q in PAIRS[name])
    rows = []
    for T in Ts:
        t = np.linspace(0, T, nt)
        x = np.linspace(0, 2 * np.pi, nx, endpoint=False)
        ks = np.concatenate([-np.arange(6, 0, -1), np.arange(1, 7)]).astype(float)
        B1, B2 = kernel_basis(Q1, ks, t, x), kernel_basis(Q2, ks, t, x)
        S = np.concatenate([B1, B2], 1)
        g, cF, _ = gamma_N([Q1, Q2], ks, t, x)
        TT, XX = np.meshgrid(t, x, indexing="ij")
        cover, width, psplit, bias = [], [], [], []
        for sd in range(seeds):
            f = case(name, seed=sd)
            # order components like PAIRS (match by symbol)
            comps = sorted(f.components, key=lambda c: 0 if sp.simplify(c.Q - Q1.Q) == 0 else 1)
            c1, c2 = (c(TT, XX).ravel() for c in comps)
            w_true = np.linalg.norm(c1) / (np.linalg.norm(c1) + np.linalg.norm(c2))
            u0 = c1 + c2
            sig = noise * np.std(u0)
            rng = np.random.default_rng(1000 + sd)
            u = u0 + sig * rng.standard_normal(u0.shape)
            s2 = sig**2
            tau2, ev_split = eb_tau2(S, u, s2)
            ev1 = eb_tau2(B1, u, s2)[1]
            ev2 = eb_tau2(B2, u, s2)[1]
            e = np.array([ev_split, ev1, ev2])
            p = np.exp(e - e.max())
            psplit.append(p[0] / p.sum())
            # posterior on a, then MC on the nonlinear weight
            p1 = B1.shape[1]
            M = S.conj().T @ S + (s2 / tau2) * np.eye(S.shape[1])
            C = s2 * np.linalg.inv(M)
            mu = np.linalg.solve(M, S.conj().T @ u)
            Lc = np.linalg.cholesky((C + C.conj().T) / 2 + 1e-14 * np.eye(len(C)))
            z = (rng.standard_normal((len(mu), ndraw)) + 1j * rng.standard_normal((len(mu), ndraw))) / np.sqrt(2)
            A = mu[:, None] + Lc @ z
            n1 = np.linalg.norm(B1 @ A[:p1], axis=0)
            n2 = np.linalg.norm(B2 @ A[p1:], axis=0)
            w = n1 / (n1 + n2)
            lo, hi = np.quantile(w, [0.05, 0.95])
            cover.append(lo <= w_true <= hi)
            bias.append(abs(np.median(w) - w_true))
            width.append(hi - lo)
        rows.append((T, cF, np.mean(cover), np.mean(width), np.mean(psplit)))
        print(f"  T={T:5.2f}  c_F={cF:.3f}  cov={np.mean(cover):.2f}  width={np.mean(width):.4f}  |bias|={np.mean(bias):.4f}  P(split)={np.mean(psplit):.3f}",
              flush=True)
    return rows


if __name__ == "__main__":
    for nm in ("transport_plus_diffusion", "wave"):
        run(nm)
