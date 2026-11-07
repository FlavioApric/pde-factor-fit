"""Components u_j from the modes assigned to each factor; weights; E_int; gamma_N and c_F."""
from __future__ import annotations

import numpy as np


def shared_modes(scores, tol):
    """Modes on more than one factor variety (intersection: the delta(P) ambiguity)."""
    return (scores < tol).sum(axis=1) > 1


def component_fields(modes, labels, scores, nfac, t, x, share_tol=1e-8):
    """u_j on the grid. A mode lying on several varieties is split equally between them:
    this is the minimum-norm representative of the finite ambiguity (C12-T1)."""
    T = t[:, None, None]
    X = x[None, :, None]
    shared = shared_modes(scores, share_tol)
    fields = []
    for j in range(nfac):
        coef = np.where(labels == j, 1.0, 0.0)
        if shared.any():
            on_j = scores[:, j] < share_tol
            nshare = (scores < share_tol).sum(axis=1)
            coef = np.where(shared, np.where(on_j, 1.0 / np.maximum(nshare, 1), 0.0), coef)
        sel = coef > 0
        if not sel.any():
            fields.append(np.zeros((len(t), len(x))))
            continue
        m = (coef[sel] * modes.amp[sel])[None, None, :] * np.exp(
            modes.lam[sel][None, None, :] * (T - t[0]) + 1j * modes.kappa[sel][None, None, :] * X
        )
        fields.append(m.sum(-1))
    return fields


def weights(fields):
    n = np.array([np.linalg.norm(f) for f in fields])
    s = n.sum()
    return n / s if s > 0 else n


def eint_ratio(terms, modes_j, Tspan):
    """rho = ||E_int(T)|| / ||u(T) - u_0|| for one evolution factor with terms {n: c_n}.

    Closed form (note, sec. II.2 (iv)): E_hat = [prod_n e^{T a_n} - 1 - sum_n (e^{T a_n} - 1)] u0_hat,
    a_n(kappa) = c_n (i kappa)^n. Cost O(N) per wavenumber."""
    if not terms or len(terms) < 2:
        return 0.0, 0.0
    k = modes_j.kappa
    u0 = modes_j.amp
    E = np.exp(np.outer(np.full(len(k), Tspan), np.ones(len(terms))) * np.stack(
        [c * (1j * k) ** n for n, c in terms.items()], axis=1))
    Ehat = (np.prod(E, axis=1) - 1 - (E - 1).sum(axis=1)) * u0
    Dhat = (np.prod(E, axis=1) - 1) * u0
    ne, nd = np.linalg.norm(Ehat), np.linalg.norm(Dhat)
    return ne, (ne / nd if nd > 0 else 0.0)


def kernel_basis(Q, kappas, t, x):
    """Columns e^{lam t + i kappa x} for all roots lam of Q(., i kappa), kappa in the band, on the grid."""
    cols = []
    TT, XX = np.meshgrid(t - t[0], x, indexing="ij")
    for k in kappas:
        for lam in Q.roots(1j * k):
            cols.append(np.exp(lam * TT + 1j * k * XX).ravel())
    return np.stack(cols, axis=1) if cols else np.zeros((TT.size, 0))


def gamma_N(factors, kappas, t, x, tol=1e-9):
    """gamma_N = inf sigma(S*S on (ker S)^perp) for S: (+)_j ker Q_j -> sum, kernels truncated to the band.

    ||S^+|| = gamma_N^{-1/2} amplifies every component error (P2-T3/T4). For N = 2, gamma = 1 - c_F.
    Returns (gamma_N, c_F, dim of the intersection seen in the band)."""
    Bs = []
    for Q in factors:
        B = kernel_basis(Q, kappas, t, x)
        if B.shape[1] == 0:
            continue
        q, r = np.linalg.qr(B)
        keep = np.abs(np.diag(r)) > tol * np.abs(np.diag(r)).max()
        Bs.append(q[:, keep])
    if len(Bs) < 2:
        return 1.0, 0.0, 0
    S = np.concatenate(Bs, axis=1)
    ev = np.linalg.eigvalsh(S.conj().T @ S)
    nz = ev[ev > 1e-8]
    n0 = int((ev <= 1e-8).sum())
    g = float(nz.min()) if len(nz) else 0.0
    return g, 1.0 - g, n0
