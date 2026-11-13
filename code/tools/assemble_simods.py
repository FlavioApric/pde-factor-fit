"""Assemble paper/simods.tex and paper/simods_supplement.tex from structure_B's preamble, the parts and the
cited bibliography. The two documents reference each other through xr-hyper (\\externaldocument), as in SIAM's
ex_article/ex_supplement templates."""
import re
import sys
from pathlib import Path

P = Path(sys.argv[1])  # the paper/ folder
B = (P / "structure_B.tex").read_text(encoding="utf8")
pre = B[: B.index("\\title{")].replace(
    "% Paper B: the proposed structure",
    "% SIMODS version (one idea: groups are factors); built from structure_B. Earlier header:", 1)
bib = B[B.index("\\begin{thebibliography}"): B.index("\\end{thebibliography}")]
chunks = re.split(r"(?=\\bibitem\{)", bib)
head, items = chunks[0], chunks[1:]
key = lambda it: re.match(r"\\bibitem\{([^}]*)\}", it).group(1)
extra = [r"""\bibitem{Pri26code}
Flavio Pricoco.
\newblock pde-factor-fit: reading the factor structure of linear {PDE}s from data.
\newblock \url{https://github.com/FlavioApric/pde-factor-fit}, 2026.
\newblock Software and benchmark data.

""", r"""\bibitem{Ful08}
William Fulton.
\newblock {\em Algebraic Curves: An Introduction to Algebraic Geometry}.
\newblock 2008.
\newblock Electronic edition of the 1969 book (W.\,A. Benjamin, New York).

""", r"""\bibitem{Rha55}
Georges de~Rham.
\newblock {\em Vari\'et\'es diff\'erentiables: formes, courants, formes harmoniques}.
\newblock Hermann, Paris, 1955.

""", r"""\bibitem{Bre11}
Haim Brezis.
\newblock {\em Functional Analysis, Sobolev Spaces and Partial Differential Equations}.
\newblock Universitext. Springer, New York, 2011.

"""]
pool = items + extra


def bibliography(body):
    cited = {k.strip() for g in re.findall(r"\\cite(?:\[[^]]*\])?\{([^}]*)\}", body) for k in g.split(",")}
    keep = sorted((it for it in pool if key(it) in cited), key=key)
    missing = cited - {key(k) for k in keep}
    assert not missing, missing
    # never leave the References heading alone at the foot of a page
    return "\\Needspace{8\\baselineskip}\n" + head + "".join(keep) + "\\end{thebibliography}\n"


SIAM_ONLY = "\\makeatletter\\ifx\\paperclass\\pfshimname\\else\\externaldocument[][nocite]{%s}\\fi\\makeatother\n"

# ---- typography for the SIAM page (fonts, spacing, float placement, figures drawn at the text width)
TYPO = r"""
% ---- typography
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage[final]{microtype}
\renewcommand{\topfraction}{0.9}
\renewcommand{\bottomfraction}{0.8}
\renewcommand{\textfraction}{0.07}
\renewcommand{\floatpagefraction}{0.85}
\setcounter{topnumber}{3}
\setcounter{bottomnumber}{2}
\setcounter{totalnumber}{4}
\setlength{\abovecaptionskip}{6pt}
\usepackage{needspace}
"""
assert "\\graphicspath{{figures/}}" in pre
pre = pre.replace("\\graphicspath{{figures/}}", "\\graphicspath{{figures/simods/}{figures/}}", 1)
pre = pre + TYPO

# ---- main paper
sm = r"""
% ---- references to the supplementary materials (resolved through xr-hyper with the official class)
\newcommand{\SMproofs}{\cref{sm:proofs}}
\newcommand{\SMinteraction}{\cref{sm:interaction}}
\newcommand{\SMalgo}{\cref{sm:algo}}
\newcommand{\SMcases}{\cref{sm:cases}}
\newcommand{\SMbeyond}{\cref{sm:beyond}}
""" + SIAM_ONLY % "simods_supplement"
parts = ["s1_intro", "s2_theory", "s3_algorithm", "s4_evidence", "s5_discussion"]
body = "".join((P / "parts" / f"{f}.tex").read_text(encoding="utf8") for f in parts)
(P / "simods.tex").write_text(pre + sm + "\n" + body + "\n" + bibliography(body) + "\n\\end{document}\n",
                              encoding="utf8", newline="\n")

# ---- supplement
spre = pre.replace("[review,onefignum,onetabnum]", "[review,supplement,onefignum,onetabnum]")
assert spre != pre
sbody = (P / "parts" / "sm_body.tex").read_text(encoding="utf8")
sbody = sbody.replace("\\input{parts/sm_reading}", (P / "parts" / "sm_reading.tex").read_text(encoding="utf8"))
(P / "simods_supplement.tex").write_text(spre + SIAM_ONLY % "simods" + "\n" + sbody + "\n" + bibliography(sbody)
                                         + "\n\\end{document}\n", encoding="utf8", newline="\n")

# ---- reading copies: the same documents in SIAM's class without the review option (no line numbers, no
# "for review purposes" footer). Cross-references still resolve against the review versions (same numbers).
for name in ("simods", "simods_supplement"):
    src = (P / f"{name}.tex").read_text(encoding="utf8")
    out = src.replace("[review,onefignum,onetabnum]", "[onefignum,onetabnum]").replace(
        "[review,supplement,onefignum,onetabnum]", "[supplement,onefignum,onetabnum]")
    assert out != src
    (P / f"{name}_reading.tex").write_text(out, encoding="utf8", newline="\n")
print("ok")
