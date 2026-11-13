"""Figures of the SIMODS paper, typeset to match the SIAM page (paper/figures/simods/*.pdf).

    python code/experiments/make_figs_simods.py

Same data and same drawing functions as make_figs.py and make_fig_evidence.py; only the typography changes:
- every figure is drawn at the SIAM text width (6.15 in), with its original aspect ratio, so that it is included at
  100 % and its text prints at the size chosen here instead of being shrunk by LaTeX;
- the font is Computer Modern (cmr10 for text, cm for mathematics), the font of the paper's body text;
- tick labels, legends and annotations at 8 pt, axis labels and panel titles at 9 pt (body text is 10.95 pt).
The figures of structure_A/B (paper/figures/fig_*.pdf) are not touched.
"""
from __future__ import annotations

import matplotlib.pyplot as plt

import make_figs as M

TEXTWIDTH_IN = 444.53284 / 72.27  # \the\textwidth of siamonline250211, in inches
OUT = M.ROOT / "paper" / "figures" / "simods"

M.mpl.rcParams.update({
    "font.family": "serif", "font.serif": ["cmr10"], "mathtext.fontset": "cm", "axes.formatter.use_mathtext": True,
    "font.size": 8.5, "axes.titlesize": 9, "axes.labelsize": 9, "legend.fontsize": 8,
    "xtick.labelsize": 8, "ytick.labelsize": 8, "axes.unicode_minus": True,
    "lines.linewidth": 1.1, "axes.linewidth": 0.6, "pdf.fonttype": 42,
})

_subplots = plt.subplots


TARGET = {"w": TEXTWIDTH_IN}  # width of the axes area; lowered for a figure whose labels stick out


def _subplots_at_textwidth(*args, **kw):
    w, h = kw.get("figsize", M.mpl.rcParams["figure.figsize"])
    s = TARGET["w"] / w
    kw["figsize"] = (TARGET["w"], h * s)
    return _subplots(*args, **kw)


plt.subplots = _subplots_at_textwidth
OUT.mkdir(parents=True, exist_ok=True)
M.HERE = OUT

import make_fig_evidence as E  # noqa: E402  (imports save/HERE from make_figs: patched above)

E.save = M.save

if __name__ == "__main__":
    M.fig_directions()
    M.fig_grouping()
    M.fig_components()
    TARGET["w"] = TEXTWIDTH_IN - 0.55  # its long row labels widen the tight bounding box by about 0.55 in
    E.main()
