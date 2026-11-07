"""Final report of one run_loop result: everything the run decided, in one Markdown + JSON, plus images
of the found directions (operators) in the frequency plane.

    .venv/Scripts/python.exe benchmarks/final_report.py --case heat
    .venv/Scripts/python.exe benchmarks/final_report.py --case random:F2:3 --noise 1e-2

or from code: final_report(res, samples=..., pis=..., t=t, x=x, sigma=sig, truth=field_or_draw).

Pixels of a direction image are points of the frequency plane (kappa, tau): an operator P(d_t, d_x) acts
on e^{tau t + i kappa x} by its symbol P(tau, i kappa), so neighbouring pixels are neighbouring Fourier
modes and the dark set is the dispersion variety (the operator's kernel). tau is complex, so each factor
gets two images: the oscillation slice (kappa, Im tau) and the damping slice (kappa, Re tau), each pixel
the minimum of log|P| over the other coordinate. The grid size comes from the ring degree: a symbol of
degree (m, dx) is fixed by (m+1)(dx+1) values, and the grid oversamples that by OVERSAMPLE on each axis.
Report only, nothing here feeds back into the pipeline (add-only, T12/T18: distributions as quantiles).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from pdefactor import aggregate as AG  # noqa: E402
from pdefactor import bayes_split as BS  # noqa: E402
from pdefactor import loop as LP  # noqa: E402
from pdefactor.core import structfit as SF  # noqa: E402
from pdefactor.core.components import gamma_N, kernel_basis  # noqa: E402
from pdefactor.core.variety import PolySymbol  # noqa: E402

OVERSAMPLE = 24  # pixels per ring degree of freedom on each axis (resolution only, not a fit knob)
MIN_PIX = 96
N_MODES_SHOWN = 3
QS = (0.05, 0.5, 0.95)


# ------------------------------------------------------------------ operators
def symbol_of(coef):
    """PolySymbol from a FactorReport.coef {(a, b): (median, lo, hi)} (posterior medians, made monic)."""
    m = max(a for a, _ in coef)
    dx = max(b for _, b in coef)
    lead = complex(coef.get((m, 0), (1.0,))[0]) or 1.0
    C = np.zeros((m, dx + 1), complex)
    for (a, b), (med, _, _) in coef.items():
        if a < m:
            C[a, b] = complex(med) / lead
    return PolySymbol(m, [C[k] for k in range(m)])


def symbol_of_theta(theta, m, pad):
    mm, dx = pad
    n = mm * (dx + 1)
    V = (theta[:n] + 1j * theta[n:]).reshape(mm, dx + 1)
    return PolySymbol(int(m), [V[k] for k in range(int(m))])


def _kappas(res, x):
    """Wavenumbers used for the kernel bases: +- the union of the factors' kappa support."""
    ks = sorted({abs(float(k)) for f in res.factors for k in (f.kappa_support or [])})
    if not ks:  # fall back to the grid's resolved wavenumbers
        L = (x[1] - x[0]) * len(x)
        ks = list(2 * np.pi / L * np.arange(1, len(x) // 4))
    return np.array(sorted({s * k for k in ks for s in (1, -1)}))


# ------------------------------------------------------------------ fit quality and components
def components(Qs, kappas, t, x, u):
    """u_j = B_j c_j from the least-squares fit of u on the stacked kernel bases [B_1 | ... | B_k];
    per factor also the residual of u on B_j alone (how much of the data that factor alone explains)."""
    shape = (len(t), len(x))
    Bs = [kernel_basis(Q, kappas, t, x) for Q in Qs]
    y = np.asarray(u, complex).ravel()
    ny = np.linalg.norm(y)
    out = {"per_factor": [], "fields": []}
    if not Bs or ny == 0:
        return out
    B = np.concatenate(Bs, axis=1)
    c, *_ = np.linalg.lstsq(B, y, rcond=None)
    out["joint_rel_residual"] = float(np.linalg.norm(y - B @ c) / ny)
    i0 = 0
    for Bj in Bs:
        cj = c[i0:i0 + Bj.shape[1]]
        i0 += Bj.shape[1]
        uj = (Bj @ cj).reshape(shape)
        alone, *_ = np.linalg.lstsq(Bj, y, rcond=None) if Bj.shape[1] else (np.zeros(0),)
        r_alone = np.linalg.norm(y - Bj @ alone) / ny if Bj.shape[1] else 1.0
        out["fields"].append(uj)
        out["per_factor"].append({"n_modes": int(Bj.shape[1]), "norm_u_j": float(np.linalg.norm(uj)),
                                  "rel_residual_alone": float(r_alone),
                                  "energy_explained_alone": float(1 - r_alone**2)})
    nrm = np.array([p["norm_u_j"] for p in out["per_factor"]])
    for p, w in zip(out["per_factor"], nrm / max(nrm.sum(), 1e-300)):
        p["weight_from_u_j"] = float(w)
    return out


# ------------------------------------------------------------------ frequency-plane images
def frequency_box(Qs, kappas, bounds):
    m, dx = bounds
    kmax = 1.25 * max(np.abs(kappas).max(), 1.0)
    nk = max(MIN_PIX, OVERSAMPLE * (dx + 1))
    nt = max(MIN_PIX, OVERSAMPLE * (m + 1))
    K = np.linspace(-kmax, kmax, nk)
    roots = np.concatenate([Q.roots(1j * k) for Q in Qs for k in K]) if Qs else np.zeros(1)
    re = np.abs(roots.real).max() * 1.2 + 1e-3
    im = np.abs(roots.imag).max() * 1.2 + 1e-3
    return K, np.linspace(-re, re, nt), np.linspace(-im, im, nt)


def slices(Q, K, MU, OM):
    """(osc, damp): min over Re tau of log10|Q| on (Im tau, kappa), and min over Im tau on (Re tau, kappa)."""
    tau_ = MU[None, :, None] + 1j * OM[None, None, :]
    v = np.log10(np.abs(Q(tau_, 1j * K[:, None, None])) + 1e-12)  # (kappa, mu, omega)
    return v.min(axis=1).T, v.min(axis=2).T


def op_distance(Qa, Qb, K, MU, OM):
    """Sup-norm distance of the normalised symbols on the box: the operator norm of the difference on the
    band-limited functions of the box (Plancherel), each operator scaled to unit norm there."""
    tau_ = MU[None, :, None] + 1j * OM[None, None, :]
    xi_ = 1j * K[:, None, None]
    a, b = Qa(tau_, xi_), Qb(tau_, xi_)
    a, b = a / np.abs(a).max(), b / np.abs(b).max()
    return float(np.abs(a - b).max())


def kernel_angles(Qa, Qb, kappas, t, x, tol=1e-6):
    """Principal angles between the kernels (band-truncated). Returns (Friedrichs angle, gap):
    Friedrichs = smallest angle outside the intersection (pi/2 if none, i.e. equal spaces);
    gap = largest angle, a distance (0 iff the kernels are the same space)."""
    from scipy.linalg import subspace_angles
    A, B = kernel_basis(Qa, kappas, t, x), kernel_basis(Qb, kappas, t, x)
    if A.shape[1] == 0 or B.shape[1] == 0:
        return np.pi / 2, np.pi / 2
    th = subspace_angles(A, B)
    out = th[th > tol]
    return float(out.min()) if len(out) else np.pi / 2, float(th.max())


def _order(D):
    try:
        from scipy.cluster.hierarchy import leaves_list, linkage
        from scipy.spatial.distance import squareform
        return leaves_list(linkage(squareform(D, checks=False), "average")) if len(D) > 2 else np.arange(len(D))
    except Exception:  # noqa: BLE001
        return np.arange(len(D))


def mds(D, dim=2):
    n = len(D)
    J = np.eye(n) - 1.0 / n
    Bm = -0.5 * J @ (D**2) @ J
    ev, V = np.linalg.eigh(Bm)
    o = np.argsort(ev)[::-1][:dim]
    return V[:, o] * np.sqrt(np.maximum(ev[o], 0))


# ------------------------------------------------------------------ parameters
def parameters(kwargs):
    mods = {"loop": LP, "aggregate": AG, "bayes_split": BS, "core.structfit": SF}
    out = {}
    for name, mod in mods.items():
        for k, v in vars(mod).items():
            if k.isupper() and not k.startswith("_") and isinstance(v, (bool, int, float, str, tuple, type(None),
                                                                         np.ndarray)):
                out[f"{name}.{k}"] = v.tolist() if isinstance(v, np.ndarray) else v
    env = {k: v for k, v in os.environ.items() if k.startswith("PDEFACTOR_")}
    return {"constants": out, "env_overrides": env, "run_loop_kwargs": kwargs,
            "doc": "analysis/PARAMETERS.md (meaning, defaults, verdicts)"}


# ------------------------------------------------------------------ the report
def _q(d):
    return {"q05": d.quantile(QS[0]), "q50": d.quantile(QS[1]), "q95": d.quantile(QS[2]), "mean": d.mean} \
        if d is not None else None


def _sd(Sigma):
    """Posterior sd of theta: diag of Sigma, per track when Sigma is (k, d, d)."""
    S = np.asarray(Sigma, float)
    if S.ndim < 2:
        return np.sqrt(np.clip(S, 0, None)).tolist()
    d = np.diagonal(S, axis1=-2, axis2=-1)
    return np.sqrt(np.clip(d, 0, None)).tolist()


def _c(z):
    z = complex(z)
    return [z.real, z.imag]


def final_report(res, *, samples, t, x, sigma, pis=None, truth=None, kwargs=None, out="benchmarks/out/final/run"):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    pis = np.full(len(samples), 1 / len(samples)) if pis is None else np.asarray(pis, float)
    u_mean = np.tensordot(pis / pis.sum(), np.asarray(samples), axes=1)
    Qs = [symbol_of(f.coef) for f in res.factors]
    kap = _kappas(res, x)
    agg = res.agg
    R = {}

    # 1 PDE (+ truth)
    R["pde"] = {"equation": res.equation(), "factors": [str(f.sympy) for f in res.factors],
                "pruned": [str(q) for q in res.pruned(4)], "grid": {"nt": len(t), "nx": len(x),
                "T": float(t[-1] - t[0]), "L": float((x[1] - x[0]) * len(x))}, "sigma": float(sigma),
                "n_samples": len(samples)}
    if truth is not None:
        from pdefactor.simulator import match
        tf = list(truth.factors) if hasattr(truth, "factors") else [c.Q for c in truth.components]
        ok, err = match(tf, res.pruned()) if res.factors else (False, float("inf"))
        R["pde"]["truth"] = {"factors": [str(q) for q in tf], "factor_set_match": ok, "worst_rel_err": err}
        if hasattr(truth, "amp_law"):
            R["pde"]["truth"].update(amp_law=truth.amp_law, family=truth.family, seed=truth.seed)

    # 2 label / model chosen
    R["model"] = {"label": res.label, "note": res.note, "bounds": list(res.bounds), "regrouped": res.regrouped,
                  "p_k": {str(k): float(v) for k, v in res.p_k.items()},
                  "structures": {str(k): float(v) for k, v in list(res.structures.items())[:10]},
                  "evidence": {str(k): float(v) for k, v in (res.evidence or {}).items()},
                  "core_labels": {k: float(v) for k, v in res.labels.items()},
                  "dropped": [str(getattr(d, "sympy", d)) for d in res.dropped]}

    # 3 posterior / distribution
    if agg is not None:
        R["posterior"] = {"k_eff": float(agg.k_eff), "k_det": int(agg.k_det), "k_eff_per_sample": _q(agg.k_eff_s),
                          "W_track": [float(w) for w in agg.W_track], "track_sympy": [str(s) for s in agg.track_sympy],
                          "theta_bar": np.asarray(agg.theta_bar).tolist(),
                          "theta_sd": _sd(agg.Sigma),
                          "k_structure": {str(k): float(v) for k, v in agg.k_structure.items()},
                          "p_k_DP": {str(k): float(v) for k, v in (agg.dp.p_k if agg.dp else {}).items()},
                          "p_k_finite_BIC": {str(k): float(v) for k, v in (agg.finite_k or {}).items()},
                          "cF": _q(agg.cF), "gamma": _q(agg.gamma), "n_cloud": int(len(agg.cloud.theta))}

    # 4 factors, 5 fit, 6 u_j
    comp = components(Qs, kap, t, x, u_mean)
    R["factors"] = []
    for j, f in enumerate(res.factors):
        d = {"sympy": str(f.sympy), "W": float(f.W), "status": f.status,
             "kappa_support": [float(k) for k in f.kappa_support], "children": [str(c) for c in f.children],
             "coef": {f"tau^{a} xi^{b}": {"median": _c(v[0]), "q05": _c(v[1]), "q95": _c(v[2])}
                      for (a, b), v in sorted(f.coef.items())}}
        if j < len(comp["per_factor"]):
            d["fit"] = comp["per_factor"][j]
        R["factors"].append(d)
    R["fit"] = {"levels": [{"bounds": list(h.bounds), "p_fit": float(h.p_fit),
                            "heldout_mean_se": list(h.heldout) if h.heldout else None,
                            "accepted": h.accepted, "note": h.note} for h in res.history],
                "joint_rel_residual": comp.get("joint_rel_residual"),
                "kappas_used": kap.tolist()}

    # 7 Friedrichs / superposition, 8 interaction
    R["friedrichs"] = {}
    if res.split:
        s = res.split
        R["friedrichs"]["split_layer"] = {
            "p_split": float(s["p_split"]), "cF": float(s["cF"]), "gamma": float(s["gamma"]),
            "p_include": np.asarray(s.get("p_include", [])).tolist(), "w_mean": np.asarray(s["w_mean"]).tolist(),
            "w_q": np.asarray(s["w_q"]).tolist(),
            "p_subset": {str(k): float(v) for k, v in (s.get("p_subset") or {}).items()}}
    if len(Qs) >= 2:
        g, cF, n0 = gamma_N(Qs, kap, t, x)
        R["friedrichs"]["gamma_N_block_gram"] = {"gamma_N": g, "cF": cF, "dim_intersection": n0,
                                                 "error_amplification": float(g**-0.5) if g > 0 else None}
    rho = _q(agg.rho) if agg is not None else None
    unused = rho is None or not np.any(np.abs(agg.rho.values[np.isfinite(agg.rho.values)]) > 0)
    R["interaction"] = {"rho_Eint": rho, "status": "not computed by core v2 (structfit); reported for completeness"
                        if unused else "computed", "domain": None if res.domain is None else
                        {"blocks": np.asarray(res.domain.get("blocks")).tolist() if res.domain.get("blocks") is not None
                         else None, "share": np.asarray(res.domain.get("share")).tolist()}}
    R["parameters"] = parameters(kwargs or {})

    # B images
    figs = []
    if Qs:
        K, MU, OM = frequency_box(Qs, kap, res.bounds)
        R["images"] = {"pixels": {"kappa": len(K), "re_tau": len(MU), "im_tau": len(OM)},
                       "box": {"kappa": [K[0], K[-1]], "re_tau": [MU[0], MU[-1]], "im_tau": [OM[0], OM[-1]]}}
        n = len(Qs)
        fig, ax = plt.subplots(2, n, figsize=(3.2 * n, 6), squeeze=False)
        for j, Q in enumerate(Qs):
            osc, damp = slices(Q, K, MU, OM)
            for r, (img, ext, lab) in enumerate(((osc, OM, "Im tau"), (damp, MU, "Re tau"))):
                ax[r, j].imshow(img, origin="lower", aspect="auto", cmap="magma",
                                extent=[K[0], K[-1], ext[0], ext[-1]])
                ax[r, j].set_xlabel("kappa")
                ax[r, j].set_ylabel(lab)
            ax[0, j].set_title(f"factor {j}  W={res.factors[j].W:.2f}", fontsize=9)
        fig.suptitle("directions: log10|Q(tau, i kappa)|, dark = kernel (dispersion variety)")
        fig.tight_layout()
        fig.savefig(out / "directions.png", dpi=130)
        plt.close(fig)
        figs.append("directions.png")

        # posterior uncertainty of each direction's image: 5-95 % width over cloud draws of its track
        if agg is not None and agg.cloud.track is not None and len(agg.cloud.theta):
            cl = agg.cloud
            fig, ax = plt.subplots(1, n, figsize=(3.2 * n, 3), squeeze=False)
            for j in range(n):
                tr = j if j < len(agg.W_track) else None
                idx = np.where(cl.track == tr)[0][:40]
                if len(idx) < 2:
                    ax[0, j].set_axis_off()
                    continue
                imgs = np.array([slices(symbol_of_theta(cl.theta[i], cl.m[i], cl.pad), K, MU, OM)[0] for i in idx])
                ax[0, j].imshow(np.percentile(imgs, 95, 0) - np.percentile(imgs, 5, 0), origin="lower",
                                aspect="auto", cmap="viridis", extent=[K[0], K[-1], OM[0], OM[-1]])
                ax[0, j].set_title(f"track {j}: 90% width ({len(idx)} draws)", fontsize=8)
            fig.tight_layout()
            fig.savefig(out / "directions_uncertainty.png", dpi=130)
            plt.close(fig)
            figs.append("directions_uncertainty.png")

        # distances between operators: operator norm and kernel gap (principal angles), and a 2-D map of the cloud
        names = [f"f{j}" for j in range(n)]
        syms = list(Qs)
        if agg is not None and len(agg.cloud.theta):
            cl = agg.cloud
            pick = np.linspace(0, len(cl.theta) - 1, min(len(cl.theta), 30)).astype(int)
            for i in pick:
                syms.append(symbol_of_theta(cl.theta[i], cl.m[i], cl.pad))
                names.append(f"s{cl.sample[i]}t{cl.track[i] if cl.track is not None else '?'}")
        N = len(syms)
        Dop, Dang, Dfr = np.zeros((N, N)), np.zeros((N, N)), np.zeros((N, N))
        for i in range(N):
            for k in range(i + 1, N):
                Dop[i, k] = Dop[k, i] = op_distance(syms[i], syms[k], K, MU, OM)
                fr, gap = kernel_angles(syms[i], syms[k], kap, t, x)
                Dang[i, k] = Dang[k, i] = gap
                Dfr[i, k] = Dfr[k, i] = fr
        R["distances"] = {"names": names, "operator_norm": Dop[:n, :n].tolist(),
                          "friedrichs_angle_rad": Dfr[:n, :n].tolist(), "kernel_gap_rad": Dang[:n, :n].tolist()}
        fig, ax = plt.subplots(1, 3, figsize=(15, 4.6))
        for a, D, ttl in ((ax[0], Dop, "operator-norm distance"),
                          (ax[1], Dang, "kernel gap: largest principal angle (rad)")):
            o = _order(D)
            im = a.imshow(D[np.ix_(o, o)], cmap="cividis")
            a.set_xticks(range(N), [names[i] for i in o], rotation=90, fontsize=6)
            a.set_yticks(range(N), [names[i] for i in o], fontsize=6)
            a.set_title(ttl + " (clustered order)")
            fig.colorbar(im, ax=a, fraction=0.046)
        P = mds(Dang)
        col = [(-1 if i < n else (cl.track[i - n] if agg is not None and cl.track is not None else 0))
               for i in range(N)]
        ax[2].scatter(P[n:, 0], P[n:, 1], c=col[n:], cmap="tab10", s=18, alpha=0.6, label="posterior draws")
        ax[2].scatter(P[:n, 0], P[:n, 1], c="k", marker="*", s=[200 * max(f.W, 0.05) for f in res.factors],
                      label="reported factors")
        for j in range(n):
            ax[2].annotate(names[j], P[j], fontsize=8)
        ax[2].set_title("operator space map (MDS of kernel gaps)")
        ax[2].legend(fontsize=7)
        fig.tight_layout()
        fig.savefig(out / "operator_space.png", dpi=130)
        plt.close(fig)
        figs.append("operator_space.png")

        # kernel modes (the directions in function space) and u_j
        fig, ax = plt.subplots(n, N_MODES_SHOWN + 1, figsize=(2.6 * (N_MODES_SHOWN + 1), 2.3 * n), squeeze=False)
        for j, Q in enumerate(Qs):
            B = kernel_basis(Q, kap[np.argsort(np.abs(kap))][: 2 * N_MODES_SHOWN], t, x)
            for c in range(N_MODES_SHOWN):
                a = ax[j, c]
                if c < B.shape[1]:
                    a.imshow(B[:, c].reshape(len(t), len(x)).real, aspect="auto", cmap="RdBu_r", origin="lower")
                a.set_title(f"f{j} mode {c}", fontsize=7)
                a.set_axis_off()
            if j < len(comp["fields"]):
                ax[j, -1].imshow(comp["fields"][j].real, aspect="auto", cmap="RdBu_r", origin="lower")
            ax[j, -1].set_title(f"u_{j}(t, x)", fontsize=7)
            ax[j, -1].set_axis_off()
        fig.tight_layout()
        fig.savefig(out / "modes_and_components.png", dpi=130)
        plt.close(fig)
        figs.append("modes_and_components.png")

    if agg is not None:
        fig, ax = plt.subplots(1, 3, figsize=(10, 2.6))
        for a, (nm, d) in zip(ax, (("c_F", agg.cF), ("gamma", agg.gamma), ("rho (E_int)", agg.rho))):
            v, w = d._ok()
            if len(v):
                a.hist(v, weights=w, bins=20, color="0.4")
            a.set_title(nm, fontsize=9)
        fig.tight_layout()
        fig.savefig(out / "distributions.png", dpi=130)
        plt.close(fig)
        figs.append("distributions.png")
    R["images_files"] = figs

    (out / "report.json").write_text(json.dumps(R, indent=1, default=_json), encoding="utf-8")
    (out / "report.md").write_text(_markdown(res, R), encoding="utf-8")
    return R


def _json(o):
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, complex):
        return [o.real, o.imag]
    return str(o)


def _f(v, d=4):
    return "—" if v is None else (f"{v:.{d}g}" if isinstance(v, float) else str(v))


def _markdown(res, R):
    L = ["# Final report", "", "## 1. PDE", "", f"- equation: `{R['pde']['equation']}`",
         f"- grid nt×nx = {R['pde']['grid']['nt']}×{R['pde']['grid']['nx']}, T = {_f(R['pde']['grid']['T'])}, "
         f"L = {_f(R['pde']['grid']['L'])}, sigma = {_f(R['pde']['sigma'])}, samples = {R['pde']['n_samples']}"]
    if "truth" in R["pde"]:
        tr = R["pde"]["truth"]
        L.append(f"- truth: {' · '.join(f'`{q}`' for q in tr['factors'])} — factor set matches: "
                 f"**{tr['factor_set_match']}** (worst rel. err {_f(tr['worst_rel_err'])})")
    m = R["model"]
    L += ["", "## 2. Model chosen", "", f"- label: **{m['label']}**", f"- bounds (m, dx): {m['bounds']}, "
          f"regrouped: {m['regrouped']}", f"- P(k): {m['p_k']}", f"- core labels: {m['core_labels']}",
          f"- dropped as redundant: {m['dropped'] or 'none'}", f"- note: {m['note'] or '—'}", "",
          "| structure | posterior | log evidence |", "|---|---|---|"]
    for s, p in m["structures"].items():
        L.append(f"| {s} | {p:.3f} | {_f(m['evidence'].get(s))} |")
    if "posterior" in R:
        p = R["posterior"]
        L += ["", "## 3. Posterior / distribution", "", f"- k_eff = {p['k_eff']:.3f} (k_det = {p['k_det']}), "
              f"per sample q05/50/95 = {_f(p['k_eff_per_sample']['q05'])}/{_f(p['k_eff_per_sample']['q50'])}/"
              f"{_f(p['k_eff_per_sample']['q95'])}", f"- P(k) structures {p['k_structure']}; DP {p['p_k_DP']}; "
              f"finite-BIC {p['p_k_finite_BIC']}", f"- tracks: " + "; ".join(
                  f"W={w:.3f} `{s}`" for w, s in zip(p["W_track"], p["track_sympy"])),
              f"- c_F q05/50/95: {_f(p['cF']['q05'])}/{_f(p['cF']['q50'])}/{_f(p['cF']['q95'])}; "
              f"gamma: {_f(p['gamma']['q05'])}/{_f(p['gamma']['q50'])}/{_f(p['gamma']['q95'])}",
              f"- cloud size {p['n_cloud']}; theta_bar and its sd are in report.json"]
    L += ["", "## 4. Factors", ""]
    for j, f in enumerate(R["factors"]):
        L += [f"### factor {j}: `{f['sympy']}`", "", f"- W = {f['W']:.4f}, status: {f['status']}, "
              f"kappa support: {[round(k, 3) for k in f['kappa_support']]}"]
        if "fit" in f:
            ft = f["fit"]
            L.append(f"- fit: {ft['n_modes']} kernel modes, alone explains {100 * ft['energy_explained_alone']:.2f}% "
                     f"(rel. residual {ft['rel_residual_alone']:.3g}); ‖u_j‖ = {ft['norm_u_j']:.4g}, "
                     f"weight from u_j = {ft['weight_from_u_j']:.4f}")
        L += ["", "| term | median | q05 | q95 |", "|---|---|---|---|"]
        for k, v in f["coef"].items():
            L.append(f"| {k} | {_cx(v['median'])} | {_cx(v['q05'])} | {_cx(v['q95'])} |")
        L.append("")
    fi = R["fit"]
    L += ["## 5. Fit per loop level", "", f"- joint relative residual of the mean field on all kernels: "
          f"{_f(fi['joint_rel_residual'])}", "", "| bounds | p_fit | held-out (mean, se) | accepted | note |",
          "|---|---|---|---|---|"]
    for h in fi["levels"]:
        L.append(f"| {h['bounds']} | {h['p_fit']:.3f} | {h['heldout_mean_se']} | {h['accepted']} | {h['note']} |")
    fr = R["friedrichs"]
    L += ["", "## 6. Friedrichs / superposition layer", ""]
    if "gamma_N_block_gram" in fr:
        g = fr["gamma_N_block_gram"]
        L.append(f"- gamma_N (block Gram) = {_f(g['gamma_N'])}, c_F = {_f(g['cF'])}, intersection dim "
                 f"{g['dim_intersection']}, error amplification gamma_N^-1/2 = {_f(g['error_amplification'])}")
    if "split_layer" in fr:
        s = fr["split_layer"]
        L += [f"- P(split) = {s['p_split']:.3f}, c_F = {_f(s['cF'])}, gamma = {_f(s['gamma'])}, "
              f"P(include) = {s['p_include']}", "- weights w_j mean [q05, q50, q95]: " + "; ".join(
                  f"{w:.4f} {[round(v, 4) for v in q]}" for w, q in zip(s["w_mean"], s["w_q"])),
              f"- P(subset): {s['p_subset']}"]
    if "distances" in R:
        L += ["- pairwise (display only, γ_N above is the headline): operator-norm distance "
              f"{np.round(R['distances']['operator_norm'], 4).tolist()}, Friedrichs angle (rad) "
              f"{np.round(R['distances']['friedrichs_angle_rad'], 4).tolist()}"]
    it = R["interaction"]
    L += ["", "## 7. Interaction term E_int", "", f"- rho = ‖E_int‖/‖u(T)-u0‖: {it['rho_Eint']} — {it['status']}",
          f"- domain blocks/share: {'none (report_domain off)' if it['domain'] is None else it['domain']}",
          "", "## 8. Parameters", "", "| name | value |", "|---|---|"]
    for k, v in R["parameters"]["constants"].items():
        L.append(f"| {k} | {str(v)[:80]} |")
    L += ["", f"- env overrides: {R['parameters']['env_overrides'] or 'none (defaults)'}",
          f"- run_loop kwargs: {R['parameters']['run_loop_kwargs']}", f"- meanings: {R['parameters']['doc']}",
          "", "## 9. Images", ""]
    if "images" in R:
        L.append(f"- frequency grid {R['images']['pixels']} pixels over box "
                 f"{ {k: [round(float(a), 3) for a in v] for k, v in R['images']['box'].items()} }")
    L += [f"![{f}]({f})" for f in R["images_files"]]
    return "\n".join(L) + "\n"


def _cx(v):
    re, im = v
    return f"{re:.5g}" if abs(im) <= 1e-12 * max(1, abs(re)) else f"{re:.5g}{im:+.5g}i"


# ------------------------------------------------------------------ CLI
def _data(spec, noise, S, seed):
    from pdefactor.synthetic import any_case, grid
    if spec.startswith("random:"):
        from pdefactor.simulator import random_pde
        _, fam, sd = spec.split(":")
        truth = random_pde(fam, int(sd))
        f = truth.field
    else:
        f = truth = any_case(spec, seed=seed)
    t, x, u = grid(f)
    sig = noise * np.std(np.abs(u))
    samples, pis = AG.fake_posterior(u, sig, S, rng=seed + 1)
    return samples, pis, t, x, sig, truth


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--case", default="transport_plus_diffusion",
                    help="synthetic case name (any_case) or random:<family>:<seed>")
    ap.add_argument("--noise", type=float, default=1e-3, help="noise std relative to std|u|")
    ap.add_argument("--S", type=int, default=3, help="posterior samples")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", default=None)
    ap.add_argument("--reuse", action="store_true", help="reuse the cached run (res.pkl in --out) if present")
    a = ap.parse_args(argv)
    samples, pis, t, x, sig, truth = _data(a.case, a.noise, a.S, a.seed)
    kw = {}
    out = a.out or str(ROOT / "benchmarks" / "out" / "final" / a.case.replace(":", "_"))
    cache = Path(out) / "res.pkl"
    if a.reuse and cache.exists():
        import pickle
        res = pickle.loads(cache.read_bytes())
    else:
        res = LP.run_loop(samples, t, x, sig, pis, **kw)
        try:
            import pickle
            Path(out).mkdir(parents=True, exist_ok=True)
            cache.write_bytes(pickle.dumps(res))
        except Exception:  # noqa: BLE001  (cache is a convenience only)
            pass
    final_report(res, samples=samples, pis=pis, t=t, x=x, sigma=sig, truth=truth,
                 kwargs={"case": a.case, "noise": a.noise, "S": a.S, "seed": a.seed, **kw}, out=out)
    print(res.summary())
    print(f"\nreport: {out}/report.md")


if __name__ == "__main__":
    main()
