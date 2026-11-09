"""Mode extraction on non-periodic rectangular cells (S-DOMAIN, plan v2.2).

Three extractors return the same `Extraction` (dispersion points + their own uncertainty):
(a) `extract_fft_tukey`: Tukey-windowed FFT in x with zero padding, peak bins, per-bin BIC pencil in t;
    sigma_lam from the per-bin CRB with the window leakage of the other peaks added to the noise.
(b) `extract_esprit`: x-first separable 2-D ESPRIT. In x every mode is undamped (|z| = 1), so a
    multichannel (all t rows) forward-backward ESPRIT in x is well conditioned and only needs the
    number of distinct kappa; a Vandermonde LS projection on those kappa decouples the cell exactly
    (no leakage), and each kappa channel is a short exponential sum in t (per-kappa BIC pencil, as in
    core.extract_modes_ic). The x-order is chosen jointly by BIC on the 2-D residual.
    sigma_lam, sigma_kappa from the full 2-D Fisher matrix of all modes (interference included).
(c) `extract_cadzow`: 2-D Cadzow (block-Hankel rank truncation + averaging), then (b).

No theory covers the conditioning of this step (P2-Q3, APERTO): the choice among (a)-(c) is empirical
(sessions/S-DOMAIN/REPORT.md). BCs are not encoded anywhere (CONV-B1): x-exponentials that are not
oscillatory (Re mu != 0, e.g. boundary layers or an interface) are kept in the projection but not
returned as dispersion points.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ..core.spectral import Modes, fft_x, matrix_pencil


@dataclass
class Extraction:
    modes: Modes
    sig_lam: np.ndarray  # std of lam per mode
    sig_kappa: np.ndarray  # std of kappa per mode (0 when kappa is a fixed bin)
    rss: float  # residual sum of squares of the free-mode model on the cell
    n_samples: int
    noise: float  # noise std used (floored for exact data)
    method: str
    n_params: int = 0  # real parameters of the free-mode model
    info: dict | None = None


def _empty(method, rss, n, noise):
    e = np.zeros(0)
    m = Modes(e, e.astype(complex), e.astype(complex), e.astype(int), e)
    return Extraction(m, e, e, rss, n, noise, method, 0, {})


def _noise_floor(u, noise):
    return noise if noise > 0 else 1e-9 * max(np.abs(u).max(), 1e-300)


# ------------------------------------------------------------------ 1-D t-stage (per channel)
def _ls(Z, y):
    a, *_ = np.linalg.lstsq(Z, y, rcond=None)
    r = y - Z @ a
    return a, float(np.vdot(r, r).real)


def pencil_bic(y, tt, noise, snr_min=3.0, max_order=8, extra=2):
    """Exponential sum in t with the order chosen by BIC among r0..r0+extra (r0 = Hankel rank
    above the noise), as core.structfit.extract_modes_ic does per FFT bin."""
    dt = tt[1] - tt[0]
    level = np.abs(y).max()
    if level == 0 or level < snr_min * noise:
        return np.zeros(0, complex), np.zeros(0, complex)
    tol = max(1e-9, snr_min * noise / level)
    lam0, _, _ = matrix_pencil(y, dt, rel_tol=tol, max_order=max_order)
    nobs = 2 * len(tt)
    best = None
    for r in range(max(len(lam0), 1), min(len(lam0) + extra, max_order) + 1):
        lam = lam0 if r == len(lam0) else matrix_pencil(y, dt, order=r)[0]
        a, rss = _ls(np.exp(np.outer(tt, lam)), y)
        bic = rss / max(noise, 1e-12 * level) ** 2 + 4 * r * np.log(nobs)  # floor: exact data
        if best is None or bic < best[0]:
            best = (bic, lam, a)
    return best[1], best[2]


# ------------------------------------------------------------------ 2-D Fisher (CRB)
def fisher_sigmas(lam, kappa_c, amp, tt, xx, noise):
    """CRB std of (lam, kappa) for every mode of u = sum A_m exp(lam_m t + i kappa_m x) on the cell grid,
    all modes jointly (interference = 'leakage' between close modes is in the off-diagonal blocks).
    kappa_c may be complex (non-oscillatory x-exponentials)."""
    T, X = np.meshgrid(tt, xx, indexing="ij")
    T, X = T.ravel(), X.ravel()
    cols = []
    for l, k, a in zip(lam, kappa_c, amp):
        g = np.exp(l * T + 1j * k * X)
        cols += [g, a * T * g, 1j * a * X * g]
    J = np.stack(cols, axis=1)
    F = J.conj().T @ J
    try:
        C = np.linalg.pinv(F, rcond=1e-14, hermitian=True)
    except np.linalg.LinAlgError:
        n = len(lam)
        return np.full(n, np.inf), np.full(n, np.inf), np.full(n, np.inf)
    d = np.sqrt(np.maximum(np.real(np.diag(C)), 0)) * noise
    return d[1::3], d[2::3], d[0::3]


# ------------------------------------------------------------------ (b) x-first ESPRIT
def _x_esprit(U, dx, order, fb=True):
    """Shared x-poles mu (u ~ sum c_m(t) e^{mu_m x}) from the stacked Hankel of all t rows."""
    nt, nx = U.shape
    Lp = nx // 2
    rows = [np.array([U[j, i : i + Lp + 1] for i in range(nx - Lp)]) for j in range(nt)]
    if fb:  # backward rows: for |z| = 1 the reversed conjugate sequence has the same poles
        Ub = np.conj(U[:, ::-1])
        rows += [np.array([Ub[j, i : i + Lp + 1] for i in range(nx - Lp)]) for j in range(nt)]
    Y = np.concatenate(rows, axis=0)
    _, s, Vh = np.linalg.svd(Y, full_matrices=False)
    return s, Vh, Y.shape


def _mu_from_subspace(Vh, order, dx):
    V = Vh[:order].T
    z = np.linalg.eigvals(np.linalg.pinv(V[:-1]) @ V[1:])
    return np.log(z) / dx


def _oscillatory(mu, tol=0.05):
    return np.abs(mu.real) <= tol + tol * np.abs(mu.imag)


def _esprit_order(U, tt, xx, noise, mu, snr_min, max_order_t):
    """Full chain for one x-order: projection, per-kappa t-pencil, 2-D reconstruction.
    Returns (rss, n_params, rows) with rows = (mu, lam, amp)."""
    Vx = np.exp(np.outer(xx, mu))  # (nx, r)
    C, *_ = np.linalg.lstsq(Vx, U.T, rcond=None)  # (r, nt): c_m(t)
    G = np.linalg.pinv(Vx.conj().T @ Vx)
    rows = []
    for m in range(len(mu)):
        na = noise * np.sqrt(max(np.real(G[m, m]), 0.0))
        lam, a = pencil_bic(C[m], tt, max(na, 1e-300), snr_min=snr_min, max_order=max_order_t)
        rows += [(mu[m], l, b) for l, b in zip(lam, a)]
    if not rows:
        r = U
        return float(np.vdot(r, r).real), len(mu), rows
    mu_, lam_, _ = map(np.array, zip(*rows))
    # joint LS amplitudes of all 2-D modes on the cell
    T, X = np.meshgrid(tt, xx, indexing="ij")
    Z = np.exp(np.outer(T.ravel(), lam_) + np.outer(X.ravel(), mu_))
    amp, rss = _ls(Z, U.ravel())
    rows = [(m_, l_, a_) for m_, l_, a_ in zip(mu_, lam_, amp)]
    return rss, 4 * len(rows) + 2 * len(mu), rows


def extract_esprit(u, t, x, noise=0.0, snr_min=3.0, max_order_x=40, max_order_t=6, span=4,
                   osc_tol=0.05, U_override=None, method="esprit"):
    """(b) x-first multichannel FB-ESPRIT + Vandermonde projection + per-kappa BIC pencil in t.
    x-order chosen by BIC on the 2-D residual among r0-span..r0+span (r0 = rank above noise)."""
    U = np.asarray(u if U_override is None else U_override, complex)
    U0 = np.asarray(u, complex)
    nt, nx = U.shape
    N = U.size
    sig = _noise_floor(U0, noise)
    tt, xx = t - t[0], x - x[0]
    dx = xx[1]
    s, Vh, shp = _x_esprit(U, dx, None)
    # noise singular values of an R x C (FB-stacked) Hankel: ~ sigma (sqrt R + sqrt C)
    thr = sig * (np.sqrt(shp[0]) + np.sqrt(shp[1])) if noise > 0 else 1e-10 * s[0]
    r0 = int(min((s > thr).sum(), max_order_x, len(s) - 1))
    best = None
    for r in range(max(1, r0 - span), min(r0 + span, max_order_x, len(s) - 1) + 1):
        mu = _mu_from_subspace(Vh, r, dx)
        rss, k, rows = _esprit_order(U, tt, xx, sig, mu, snr_min, max_order_t)
        if U_override is not None:  # residual always against the raw data
            if rows:
                mu_, lam_, a_ = map(np.array, zip(*rows))
                T, X = np.meshgrid(tt, xx, indexing="ij")
                Z = np.exp(np.outer(T.ravel(), lam_) + np.outer(X.ravel(), mu_))
                a_, rss = _ls(Z, U0.ravel())
                rows = list(zip(mu_, lam_, a_))
        bic = rss / sig**2 + k * np.log(N)
        if best is None or bic < best[0]:
            best = (bic, r, rss, k, rows)
    _, r, rss, k, rows = best
    if not rows:
        return _empty(method, rss, N, sig)
    mu_, lam_, amp_ = map(np.array, zip(*rows))
    kap_c = -1j * mu_
    sl, sk, sa = fisher_sigmas(lam_, kap_c, amp_, tt, xx, sig)
    keep = _oscillatory(mu_, osc_tol) & (np.abs(amp_) > snr_min * sa)
    kap = kap_c.real
    amp0 = amp_ * np.exp(-1j * kap * x[0] - lam_ * 0.0)  # amplitude for e^{i kappa x} with absolute x
    # kidx: one index per distinct x-pole (modes sharing kappa share a "bin")
    _, kidx = np.unique(np.round(mu_, 12), return_inverse=True)
    m = Modes(kap[keep], lam_[keep], amp0[keep], kidx[keep].astype(int), (np.abs(amp_) / np.maximum(sa, 1e-300))[keep])
    return Extraction(m, sl[keep], sk[keep], rss, N, sig, method, k,
                      {"x_order": r, "x_order0": r0, "n_nonosc": int((~_oscillatory(mu_, osc_tol)).sum())})


# ------------------------------------------------------------------ (c) 2-D Cadzow
def cadzow_2d(u, rank, iters=10, Pt=None, Px=None):
    """Block-Hankel (Hankel-of-Hankel) rank-`rank` truncation + averaging, iterated."""
    U = np.asarray(u, complex)
    nt, nx = U.shape
    Pt = Pt or min(nt // 2, 24)
    Px = Px or min(nx // 2, 24)
    Qt, Qx = nt - Pt + 1, nx - Px + 1
    a, b, c, d = np.meshgrid(np.arange(Pt), np.arange(Px), np.arange(Qt), np.arange(Qx), indexing="ij")
    it = (a + c).reshape(Pt * Px, Qt * Qx)
    ix = (b + d).reshape(Pt * Px, Qt * Qx)
    flat = (it * nx + ix).ravel()
    cnt = np.bincount(flat, minlength=nt * nx)
    for _ in range(iters):
        H = U.ravel()[flat].reshape(Pt * Px, Qt * Qx)
        W, s, Vh = np.linalg.svd(H, full_matrices=False)
        Hr = (W[:, :rank] * s[:rank]) @ Vh[:rank]
        re = np.bincount(flat, weights=Hr.real.ravel(), minlength=nt * nx)
        im = np.bincount(flat, weights=Hr.imag.ravel(), minlength=nt * nx)
        U = ((re + 1j * im) / cnt).reshape(nt, nx)
    return U


def extract_cadzow(u, t, x, noise=0.0, iters=10, **kw):
    """(c) Cadzow denoising with rank = #2-D modes of (b) on the raw data, then (b) on the denoised field
    (residual and BIC still computed against the raw data)."""
    pre = extract_esprit(u, t, x, noise, **kw)
    rank = int(pre.n_params // 4) if pre.n_params else 1
    # number of 2-D modes of the free-mode model (incl. non-oscillatory) = (k - 2 r_x) / 4
    rank = max(1, (pre.n_params - 2 * pre.info.get("x_order", 0)) // 4) if pre.info else rank
    Ud = cadzow_2d(u, rank, iters=iters)
    out = extract_esprit(u, t, x, noise, U_override=Ud, method="cadzow", **kw)
    if out.info is not None:
        out.info["cadzow_rank"] = rank
    return out


# ------------------------------------------------------------------ (a) Tukey FFT
def extract_fft_tukey(u, t, x, noise=0.0, pad=4, alpha=0.25, snr_min=3.0, max_order=8):
    """(a) Tukey window + zero padding; peaks of the time-averaged spectrum; per-peak BIC pencil in t.
    Leakage-aware sigma_lam: the other peaks' window response at this bin is added to the bin noise."""
    from scipy.signal.windows import tukey

    from ..core.structfit import sigma_lambda

    U0 = np.asarray(u, complex)
    nt, nx = U0.shape
    sig = _noise_floor(U0, noise)
    tt = t - t[0]
    w = tukey(nx, alpha)
    kappa, U = fft_x(U0, x - x[0], window="tukey", pad=pad)
    bin_noise = sig * np.sqrt((w**2).sum()) / w.sum()
    S = np.sqrt((np.abs(U) ** 2).mean(0))
    n = len(kappa)
    peaks = [k for k in range(n) if S[k] >= S[(k - 1) % n] and S[k] > S[(k + 1) % n] and S[k] > snr_min * bin_noise]
    Wk = np.abs(np.fft.fft(w, n=n)) / w.sum()  # window response vs bin offset
    rows, rec = [], np.zeros_like(U0)
    lobe = int(np.ceil(pad * (1 + alpha)))  # main-lobe half width in padded bins
    for k in peaks:
        # inside the main lobe a neighbour is an extra exponential that the pencil models; outside it its
        # sidelobe is unmodelled interference, counted as noise
        leak = np.sqrt(sum((S[j] * Wk[(k - j) % n]) ** 2 for j in peaks
                           if min((k - j) % n, (j - k) % n) > lobe))
        bn = np.hypot(bin_noise, leak)
        lam, a = pencil_bic(U[:, k], tt, bn, snr_min=snr_min, max_order=max_order)
        for l, b in zip(lam, a):
            rows.append((kappa[k], l, b, k, abs(b) / bn, bn))
    N = U0.size
    if not rows:
        return _empty("fft_tukey", float(np.vdot(U0, U0).real), N, sig)
    k_, l_, a_, i_, s_, bn_ = map(np.array, zip(*rows))
    m = Modes(k_.real.astype(float), l_.astype(complex), a_.astype(complex), i_.real.astype(int), s_.real.astype(float))
    sl = np.zeros(len(m))
    for kk in np.unique(m.kidx):
        sel = m.kidx == kk
        sl[sel] = sigma_lambda(m.subset(sel), t, float(bn_[sel][0].real))
    # residual of the free-mode model on the cell (joint LS amplitudes)
    T, X = np.meshgrid(tt, x - x[0], indexing="ij")
    Z = np.exp(np.outer(T.ravel(), m.lam) + 1j * np.outer(X.ravel(), m.kappa))
    _, rss = _ls(Z, U0.ravel())
    dk = 2 * np.pi / (n * (x[1] - x[0]))
    return Extraction(m, sl, np.full(len(m), dk / np.sqrt(12)), rss, N, sig, "fft_tukey", 4 * len(m), {"peaks": len(peaks)})


# ------------------------------------------------------------------ (b') true 2-D ESPRIT + joint NLS
def _block_hankel_index(nt, nx, Pt, Px):
    Qt, Qx = nt - Pt + 1, nx - Px + 1
    a, b, c, d = np.meshgrid(np.arange(Pt), np.arange(Px), np.arange(Qt), np.arange(Qx), indexing="ij")
    return (a + c).reshape(Pt * Px, Qt * Qx), (b + d).reshape(Pt * Px, Qt * Qx)


def esprit_2d(U, dt, dx, order=None, noise=0.0, Pt=None, Px=None, max_order=60, seed=0):
    """2-D ESPRIT on the block-Hankel matrix: shift invariance in t and in x of the signal subspace,
    poles paired by joint diagonalisation (eigenvectors of a random combination).
    Returns (lam, mu, singular values, order)."""
    nt, nx = U.shape
    Pt = Pt or min(nt // 2, 24)
    Px = Px or min(nx // 2, 24)
    it, ix = _block_hankel_index(nt, nx, Pt, Px)
    H = U[it, ix]
    W, s, _ = np.linalg.svd(H, full_matrices=False)
    if order is None:
        thr = noise * (np.sqrt(H.shape[0]) + np.sqrt(H.shape[1])) if noise > 0 else 1e-10 * s[0]
        order = int(min((s > thr).sum(), max_order))
    order = max(1, min(order, (Pt - 1) * Px - 1, Pt * (Px - 1) - 1))
    Ws = W[:, :order].reshape(Pt, Px, order)
    Ft = np.linalg.pinv(Ws[:-1].reshape(-1, order)) @ Ws[1:].reshape(-1, order)
    Fx = np.linalg.pinv(Ws[:, :-1].reshape(-1, order)) @ Ws[:, 1:].reshape(-1, order)
    beta = np.random.default_rng(seed).standard_normal(2)
    _, T = np.linalg.eig(beta[0] * Ft + beta[1] * Fx)
    Ti = np.linalg.pinv(T)
    zt = np.diag(Ti @ Ft @ T)
    zx = np.diag(Ti @ Fx @ T)
    return np.log(zt) / dt, np.log(zx) / dx, s, order


def _model(theta, M, T, X):
    a = theta[:M] + 1j * theta[M:2 * M]
    lam = theta[2 * M:3 * M] + 1j * theta[3 * M:4 * M]
    kap = theta[4 * M:5 * M]
    G = np.exp(np.outer(T, lam) + 1j * np.outer(X, kap))
    return a, lam, kap, G


def _design(T, X, lam, kap, real):
    G = np.exp(np.outer(T, lam) + 1j * np.outer(X, kap))
    return np.concatenate([2 * G.real, -2 * G.imag], axis=1) if real else G


def _amps(T, X, lam, kap, y, real):
    """LS amplitudes and RSS; real=True: u = 2 Re sum A e^{...} (conjugate pairs enforced)."""
    Z = _design(T, X, lam, kap, real)
    c, *_ = np.linalg.lstsq(Z, y.real if real else y, rcond=None)
    r = (y.real if real else y) - Z @ c
    a = c[: len(lam)] + 1j * c[len(lam):] if real else c
    return a, float(np.vdot(r, r).real)


def refine_nls(U, tt, xx, lam, kap, amp=None, max_nfev=40, real=False):
    """Joint Levenberg-Marquardt on all 2-D modes A e^{lam t + i kappa x} (A, lam complex, kappa real),
    analytic Jacobian; real=True fits u = 2 Re sum(...) (a real field: conjugate pairs enforced).
    At convergence the estimates attain the CRB of `fisher_sigmas`."""
    from scipy.optimize import least_squares

    T, X = np.meshgrid(tt, xx, indexing="ij")
    T, X, y = T.ravel(), X.ravel(), np.asarray(U, complex).ravel()
    M = len(lam)
    kap = np.real(kap)
    if amp is None:
        amp, _ = _amps(T, X, lam, kap, y, real)
    th0 = np.r_[amp.real, amp.imag, lam.real, lam.imag, kap]

    def res(th):
        a, _, _, G = _model(th, M, T, X)
        r = G @ a - y
        return 2 * (G @ a).real - y.real if real else np.r_[r.real, r.imag]

    def jac(th):
        a, _, _, G = _model(th, M, T, X)
        dL = G * a * T[:, None]
        Jc = np.concatenate([G, 1j * G, dL, 1j * dL, 1j * G * a * X[:, None]], axis=1)
        return 2 * Jc.real if real else np.concatenate([Jc.real, Jc.imag], axis=0)

    try:
        with np.errstate(over="raise", invalid="raise"):
            th = least_squares(res, th0, jac=jac, method="lm", max_nfev=max_nfev, xtol=1e-10, ftol=1e-10).x
    except (ValueError, FloatingPointError, np.linalg.LinAlgError):
        th = th0
    a, lam, kap, _ = _model(th, M, T, X)
    r = res(th)
    return lam, kap, a, float(np.dot(r, r))


def _residual_peak(R, tt, xx, real, pad=4):
    """Strongest (lam, kappa) candidate in a residual field: 2-D zero-padded periodogram peak (undamped
    guess), then a 1-mode NLS."""
    nt, nx = R.shape
    F = np.fft.fft2(R, s=(pad * nt, pad * nx))
    i, j = np.unravel_index(np.argmax(np.abs(F)), F.shape)
    om = 2 * np.pi * np.fft.fftfreq(pad * nt, d=tt[1])[i]
    ka = 2 * np.pi * np.fft.fftfreq(pad * nx, d=xx[1])[j]
    lam, kap, _, _ = refine_nls(R, tt, xx, np.array([1j * om]), np.array([ka]), max_nfev=20, real=real)
    return lam[0], kap[0]


def _sane(lam, tt):
    return np.isfinite(lam) & (np.abs(lam.real) * tt[-1] < 60)


def extract_esprit2d(u, t, x, noise=0.0, snr_min=3.0, osc_tol=0.05, max_add=40, U_init=None,
                     method="esprit2d", order=None, init="esprit2d"):
    """(b) 2-D modes with joint order selection. Initial poles from 2-D ESPRIT (block Hankel, joint shift
    invariance; oscillatory x-poles only, kappa real: boundary layers are not dispersion points, CONV-B1)
    or none (init="greedy"); then joint NLS of all 2-D modes, greedy RELAX-type addition of residual
    modes and pruning while the 2-D BIC (RSS/sigma^2 + 5 M ln N) decreases. A real field is fitted as
    2 Re sum(...), and both conjugate points are returned."""
    real = np.isrealobj(u)
    U0 = np.asarray(u, complex)
    nt, nx = U0.shape
    N = U0.size
    sig = _noise_floor(U0, noise)
    tt, xx = t - t[0], x - x[0]
    T, X = np.meshgrid(tt, xx, indexing="ij")
    T, X, y = T.ravel(), X.ravel(), U0.ravel()
    r0 = 0
    if init == "greedy":
        lam, kap = np.zeros(0, complex), np.zeros(0)
        amp, rss = np.zeros(0, complex), float(np.vdot(y, y).real)
    else:
        Ui = U0 if U_init is None else np.asarray(U_init, complex)
        lam, mu, _, r0 = esprit_2d(Ui, tt[1], xx[1], order=order, noise=noise)
        ok = _sane(lam, tt) & np.isfinite(mu) & _oscillatory(mu, osc_tol)
        lam, kap = lam[ok], mu[ok].imag
        if real:  # keep one of each conjugate pair (kappa >= 0 side)
            sel = kap >= 0
            lam, kap = lam[sel], kap[sel]
        lam, kap, amp, rss = refine_nls(U0, tt, xx, lam, kap, real=real)
    n_init = len(lam)

    def bic(rss_, M):
        return rss_ / sig**2 + 5 * M * np.log(N)

    b = bic(rss, len(lam))
    added = 0
    for _ in range(max_add):
        if len(lam):
            Z = _design(T, X, lam, kap, real)
            c = np.r_[amp.real, amp.imag] if real else amp
            R = (y - Z @ c).reshape(nt, nx)
        else:
            R = U0
        l1, k1 = _residual_peak(R, tt, xx, real)
        if not _sane(np.array([l1]), tt)[0]:
            break
        l2, k2, a2, rss2 = refine_nls(U0, tt, xx, np.r_[lam, l1], np.r_[kap, k1], real=real)
        b2 = bic(rss2, len(l2))
        if not b2 < b:
            break
        lam, kap, amp, rss, b = l2, k2, a2, rss2, b2
        added += 1
    pruned = 0
    while len(lam) > 1:  # drop modes whose removal lowers the BIC (spurious poles)
        cands = []
        for i in range(len(lam)):
            keep = np.arange(len(lam)) != i
            cands.append(bic(_amps(T, X, lam[keep], kap[keep], y, real)[1], keep.sum()))
        i = int(np.argmin(cands))
        if cands[i] >= b:
            break
        keep = np.arange(len(lam)) != i
        lam, kap, amp, rss = refine_nls(U0, tt, xx, lam[keep], kap[keep], real=real)
        b = bic(rss, len(lam))
        pruned += 1
    if real and len(lam):  # the conjugate partner of every mode is in the data too
        lamf, kapf, ampf = np.r_[lam, lam.conj()], np.r_[kap, -kap], np.r_[amp, amp.conj()]
    else:
        lamf, kapf, ampf = lam, kap, amp
    if not len(lamf):
        return _empty(method, rss, N, sig)
    # complex-noise Fisher on the full (paired) model; for a real field each pair carries the info twice
    sl, sk, sa = fisher_sigmas(lamf, kapf.astype(complex), ampf, tt, xx, sig)
    keep = np.abs(ampf) > snr_min * sa
    amp0 = ampf * np.exp(-1j * kapf * x[0])
    _, kidx = np.unique(np.round(kapf, 3), return_inverse=True)
    m = Modes(kapf[keep], lamf[keep], amp0[keep], kidx[keep].astype(int), (np.abs(ampf) / np.maximum(sa, 1e-300))[keep])
    return Extraction(m, sl[keep], sk[keep], rss, N, sig, method, 5 * len(lam),
                      {"order0": r0, "init": n_init, "added": added, "pruned": pruned, "n_total": len(lam)})


def extract_greedy(u, t, x, noise=0.0, **kw):
    """(b, init=greedy) RELAX-type: no subspace step, modes added one by one from the residual."""
    return extract_esprit2d(u, t, x, noise, init="greedy", method="greedy", **kw)


def extract_cadzow2d(u, t, x, noise=0.0, iters=10, **kw):
    """(c) Cadzow-denoised field (rank from the block-Hankel noise threshold) as the ESPRIT init, then (b)
    on the raw data."""
    U0 = np.asarray(u, complex)
    _, _, _, r0 = esprit_2d(U0, t[1] - t[0], x[1] - x[0], noise=noise)
    Ud = cadzow_2d(U0, r0, iters=iters)
    out = extract_esprit2d(u, t, x, noise, U_init=Ud, method="cadzow", **kw)
    out.info["cadzow_rank"] = r0
    return out


EXTRACTORS = {"fft_tukey": extract_fft_tukey, "esprit_x": extract_esprit, "esprit2d": extract_esprit2d,
              "greedy": extract_greedy,
              "cadzow": extract_cadzow2d, "cadzow_x": extract_cadzow}
