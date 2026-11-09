"""Publication figures for both papers (vector PDF). Needs numpy + matplotlib only.

    python code/experiments/make_figs.py

Reads benchmarks/data (written by experiments/extract_data.py and copied benchmark
reports) and writes paper/figures/fig_*.pdf. Colours: the two groups of the running example are
always blue (factor tau + c xi, transport) and orange (factor tau - nu xi^2, diffusion); the palette was
checked for colour-vision deficiency, and every colour is doubled by a label or a marker shape.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "benchmarks" / "data"
MD = ROOT / "claude" / "benchmark_tables"
HERE = ROOT / "paper" / "figures"
BLUE, ORANGE, AQUA, GRAY, INK = "#2a78d6", "#eb6834", "#1baf7a", "#8a8984", "#0b0b0b"
C_TRUE, NU_TRUE = 1.0, 0.3

mpl.rcParams.update({
    "font.family": "serif", "font.size": 9, "axes.titlesize": 9, "axes.labelsize": 9,
    "legend.fontsize": 8, "xtick.labelsize": 8, "ytick.labelsize": 8, "axes.linewidth": 0.6,
    "xtick.major.width": 0.6, "ytick.major.width": 0.6, "axes.spines.top": False, "axes.spines.right": False,
    "axes.edgecolor": "#52514e", "axes.labelcolor": INK, "xtick.color": "#52514e", "ytick.color": "#52514e",
    "legend.frameon": False, "savefig.bbox": "tight", "savefig.pad_inches": 0.02, "pdf.fonttype": 42,
    "mathtext.fontset": "cm",
})


def save(fig, name):
    fig.savefig(HERE / f"{name}.pdf")
    plt.close(fig)
    print("wrote", name)


def cloud():
    c = json.loads((DATA / "cloud_S32.json").read_text())
    # tau = sum_k t_k xi^k  <=>  factor tau - sum_k t_k xi^k ; coefficient of xi^k in the factor is -t_k
    coef = []
    for tm in c["terms"]:
        v = {int(k): complex(*z) for k, z in tm.items()}
        coef.append(v)
    mass = np.asarray(c["pi"]) * np.asarray(c["w"])
    track = np.asarray(c["track"])
    # identify which track is transport (coefficient of xi near +1 in the factor)
    t_is_transport = {}
    for tr in set(track.tolist()):
        b1 = np.mean([-coef[i].get(1, 0).real for i in np.where(track == tr)[0]])
        t_is_transport[tr] = b1 > 0.5
    return coef, mass, track, t_is_transport, c


# ------------------------------------------------------------------------------------ directions
def fig_directions():
    coef, mass, track, is_tr, _ = cloud()
    m = json.loads((DATA / "worked_modes.json").read_text())
    kap = np.asarray(m["kappa"]); lam = np.asarray(m["lam"]["re"]) + 1j * np.asarray(m["lam"]["im"])
    grp = np.asarray(m["group"])
    # group 0 of the worked run is transport (factor list order: tau + c xi first)
    k = np.linspace(-6, 6, 400)
    fig, axs = plt.subplots(1, 2, figsize=(6.6, 2.6), constrained_layout=True)
    for ax, part, lab in [(axs[0], np.imag, r"$\mathrm{Im}\,\lambda$ (oscillation)"),
                          (axs[1], np.real, r"$\mathrm{Re}\,\lambda$ (growth / decay)")]:
        for v, tr in zip(coef, track):
            lamk = sum(t * (1j * k) ** p for p, t in v.items())
            ax.plot(k, part(lamk), color=BLUE if is_tr[tr] else ORANGE, lw=0.6, alpha=0.18, zorder=1)
        ax.plot(k, part(-1j * C_TRUE * k), color=INK, lw=0.8, ls=(0, (4, 3)), zorder=2)
        ax.plot(k, part(-NU_TRUE * k**2 + 0j), color=INK, lw=0.8, ls=(0, (4, 3)), zorder=2)
        for g, col, mk, name in [(0, BLUE, "o", r"modes on $\tau+c\xi$"), (1, ORANGE, "s", r"modes on $\tau-\nu\xi^2$")]:
            sel = grp == g
            ax.scatter(kap[sel], part(lam[sel]), s=22, marker=mk, facecolor=col, edgecolor="white", lw=0.8,
                       zorder=3, label=name)
        ax.set_xlabel(r"wavenumber $\kappa$")
        ax.set_ylabel(lab)
        ax.axhline(0, color="#d8d7d2", lw=0.5, zorder=0)
    axs[0].set_ylim(-6.5, 6.5); axs[1].set_ylim(-11, 1.5)
    axs[0].set_title("(a) oscillation slice", loc="left")
    axs[1].set_title("(b) damping slice", loc="left")
    h, l = axs[0].get_legend_handles_labels()
    h += [mpl.lines.Line2D([], [], color=INK, lw=0.8, ls=(0, (4, 3))),
          mpl.lines.Line2D([], [], color=GRAY, lw=1.0, alpha=0.6)]
    l += ["true branches", "posterior factors (32 samples)"]
    fig.legend(h, l, loc="outside lower center", ncol=4, handlelength=2.2)
    save(fig, "fig_directions")


# ------------------------------------------------------------------------------------ grouping
def fig_grouping():
    coef, mass, track, is_tr, c = cloud()
    ang = np.load(DATA / "cloud_S32_angles.npy")
    b1 = np.array([-v.get(1, 0).real for v in coef])
    b2 = np.array([-v.get(2, 0).real for v in coef])
    col = np.array([BLUE if is_tr[t] else ORANGE for t in track])
    fig, axs = plt.subplots(1, 2, figsize=(6.6, 2.75), constrained_layout=True,
                            gridspec_kw={"width_ratios": [1.15, 1]})
    ax = axs[0]
    s = 12 + 260 * mass / mass.max()
    for tr in sorted(set(track.tolist())):
        sel = track == tr
        ax.scatter(b1[sel], b2[sel], s=s[sel], color=col[sel][0], alpha=0.55, edgecolor="white", lw=0.6,
                   marker="o" if is_tr[tr] else "s",
                   label=(r"cluster 1: $\tau+\beta_1\xi$" if is_tr[tr] else r"cluster 2: $\tau+\beta_2\xi^2$"))
    ax.scatter([C_TRUE, 0], [0, -NU_TRUE], marker="+", s=80, color=INK, lw=1.0, label="true factors", zorder=4)
    ax.set_xlabel(r"coefficient of $\xi$ in the factor")
    ax.set_ylabel(r"coefficient of $\xi^2$ in the factor")
    ax.set_title("(a) cloud of factors, 32 samples", loc="left")
    ax.legend(loc="center", fontsize=7.5, handletextpad=0.3, markerscale=0.5)
    ax.set_xlim(-0.2, 1.25); ax.set_ylim(-0.42, 0.08)
    # angle matrix ordered by cluster, then by mass
    order = np.lexsort((-mass, [0 if is_tr[t] else 1 for t in track]))
    A = ang[np.ix_(order, order)]
    ax = axs[1]
    im = ax.imshow(A, cmap="Blues", vmin=0, vmax=np.pi / 2 * 0.85, interpolation="nearest")
    n1 = sum(1 for t in track if is_tr[t])
    for v in (n1 - 0.5,):
        ax.axhline(v, color="white", lw=1.2); ax.axvline(v, color="white", lw=1.2)
    ax.set_xticks([n1 / 2, n1 + (len(order) - n1) / 2]); ax.set_xticklabels(["cluster 1", "cluster 2"])
    ax.set_yticks([n1 / 2, n1 + (len(order) - n1) / 2]); ax.set_yticklabels(["cluster 1", "cluster 2"], rotation=90,
                                                                            va="center")
    ax.tick_params(length=0)
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.set_title("(b) largest principal angle between kernels", loc="left")
    cb = fig.colorbar(im, ax=ax, shrink=0.85, pad=0.02)
    cb.set_label("angle (rad)"); cb.outline.set_visible(False); cb.set_ticks([0, 0.4, 0.8, 1.2])
    save(fig, "fig_grouping")


# ------------------------------------------------------------------------------------ components
def fig_components():
    f = np.load(DATA / "worked_fields.npz")
    U, t, x = f["U"], f["t"], f["x"]
    u1, u2 = f["components"][0].real, f["components"][1].real
    R = U - u1 - u2
    vmax = np.abs(U).max()
    fig, axs = plt.subplots(1, 4, figsize=(6.8, 1.95), constrained_layout=True, sharey=True)
    ext = [x[0], x[-1], t[0], t[-1]]
    titles = [r"(a) data $u$ (5% noise)", r"(b) group 1, $u_1$", r"(c) group 2, $u_2$", r"(d) residual $\times 5$"]
    for ax, F, ti in zip(axs, [U, u1, u2, 5 * R], titles):
        im = ax.imshow(F, origin="lower", aspect="auto", extent=ext, cmap="RdBu_r", vmin=-vmax, vmax=vmax)
        ax.set_title(ti, loc="left", fontsize=8.5)
        ax.set_xlabel(r"$x$")
        ax.set_xticks([0, np.pi, 2 * np.pi]); ax.set_xticklabels(["0", r"$\pi$", r"$2\pi$"])
    axs[0].set_ylabel(r"$t$")
    cb = fig.colorbar(im, ax=axs, shrink=0.9, pad=0.01)
    cb.outline.set_visible(False)
    save(fig, "fig_components")


# ------------------------------------------------------------------------------------ band
def fig_nyquist():
    f = np.load(DATA / "worked_fields.npz")
    m = json.loads((DATA / "worked_modes.json").read_text())
    Uh, Uht, kk, sig = f["Uhat"], f["Uhat_true"], f["kappa_fft"], float(f["sigma"])
    nx = m["nx"]
    pos = kk > 0
    order = np.argsort(kk[pos])
    k = kk[pos][order]
    a0 = np.abs(Uh[0, pos])[order]; aT = np.abs(Uh[-1, pos])[order]
    t0 = np.abs(Uht[0, pos])[order]
    floor = 3 * sig / np.sqrt(nx)
    fig, ax = plt.subplots(figsize=(4.4, 2.5), constrained_layout=True)
    ax.semilogy(k, np.maximum(t0, 1e-12), color=GRAY, lw=0.9, label=r"noise-free $|\hat u(0,\kappa)|$")
    ax.semilogy(k, a0, "o", ms=3.2, color=BLUE, mec="white", mew=0.4, label=r"data, $t=0$")
    ax.semilogy(k, aT, "s", ms=3.0, color=ORANGE, mec="white", mew=0.4, label=r"data, $t=T$")
    ax.axhline(floor, color=INK, lw=0.8, ls=(0, (4, 3)))
    ax.text(20, floor * 2.2, r"detection threshold $z\sigma_\kappa$", fontsize=7.5)
    used = sorted({abs(v) for v in m["kappa"]})
    ax.axvspan(0.5, max(used) + 0.5, color=AQUA, alpha=0.13, lw=0)
    ax.text(max(used) + 0.9, 3e-1 * a0.max(), "band $\\mathcal{K}$\nused", fontsize=7.5, va="top")
    ax.axvline(np.pi / m["dx"], color=GRAY, lw=0.8)
    ax.text(np.pi / m["dx"] - 1, 3e-1 * a0.max(), r"$\pi/\Delta x$", ha="right", fontsize=7.5, va="top")
    ax.set_xlim(0, 66)
    ax.set_ylim(1e-6, 3 * a0.max())
    ax.set_xlabel(r"wavenumber $\kappa$"); ax.set_ylabel("Fourier amplitude")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.22), ncol=3, fontsize=7.5)
    save(fig, "fig_nyquist")


# ------------------------------------------------------------------------------------ benchmark
def parse_p8():
    txt = (MD / "p8_final_v5.md").read_text()
    sec = txt.split("## Totals over the 30 P8 inputs")[1].split("## Per design")[0]
    rows = {}
    for line in sec.splitlines():
        if line.startswith("| ") and not line.startswith("| arm") and not line.startswith("|---"):
            c = [s.strip() for s in line.strip("|").split("|")]
            rows[c[0]] = dict(right=int(c[2]), equiv=int(c[3]), abst=int(c[5]) + int(c[4]), fc=int(c[6]),
                              runtime=float(c[15]) if c[15] not in ("-", "") else np.nan)
    return rows


def fig_bench():
    rows = parse_p8()
    names = [("pipeline", "this method"), ("weak_sindy", "weak SINDy"), ("ensemble_sindy", "ensemble SINDy"),
             ("sbr_sindy", "SBR SINDy"), ("pdefind", "PDE-FIND"), ("bopdmd", "BOP-DMD")]
    fig, ax = plt.subplots(figsize=(4.6, 2.2), constrained_layout=True)
    y = np.arange(len(names))[::-1]
    for yi, (key, lab) in zip(y, names):
        r = rows[key]
        left = 0
        for val, col, hatch in [(r["right"], BLUE, None), (r["equiv"], "#86b6ef", None),
                                (r["abst"], "#d8d7d2", None), (r["fc"], ORANGE, "////")]:
            if val:
                ax.barh(yi, val - 0.15, left=left + 0.075, height=0.62, color=col, hatch=hatch,
                        edgecolor="white", lw=0)
            left += val
        ax.text(31, yi, f"{r['right']}/30", va="center", fontsize=7.5, color=INK)
    ax.set_yticks(y); ax.set_yticklabels([l for _, l in names])
    ax.set_xlim(0, 34); ax.set_xticks([0, 10, 20, 30])
    ax.set_xlabel("number of the 30 inputs")
    ax.tick_params(axis="y", length=0)
    hs = [mpl.patches.Patch(color=BLUE), mpl.patches.Patch(color="#86b6ef"),
          mpl.patches.Patch(facecolor=ORANGE, hatch="////", edgecolor="white")]
    ax.legend(hs, ["right", "equivalent", "false-confident"], loc="upper center", bbox_to_anchor=(0.45, 1.2),
              ncol=3, handlelength=1.2)
    save(fig, "fig_bench")


if __name__ == "__main__":
    fig_directions()
    fig_grouping()
    fig_components()
    fig_nyquist()
    fig_bench()
