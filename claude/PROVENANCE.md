# PROVENANCE: what every part of branch `main` is, why it is here, where it came from

The earlier private research repository ("the old repo") contained, on its `main` branch, the algorithm `PDEFactorML/` (package `pdefactor`) and a spec; other branches held analysis, benchmarks, session reports, the two manuscripts and explained editions.

| now | what it is | why it is here | came from (old repo) | in the papers? |
|---|---|---|---|---|
| `paper/structure_B.tex` + `.pdf` | the main paper (41 pp): grouping principle, algorithm, Bayesian layer, benchmark, discussion | the deliverable (recommended structure) | branch `claude/adoring-feynman`: `paper/B_proposed_structure` + `paper/shared` (inlined into one file) | it is the paper |
| `paper/structure_A.tex` + `.pdf` | the same paper in the author's outline (theory first) (40 pp) | the author's preferred order | same, `paper/A_user_structure` | it is the paper |
| `paper/explained.tex` + `.pdf` | the explained algorithm: each section with a plain-language walk-through, tests and results (46 pp) | the algorithm in step-by-step form | `PDEFactorML/EXPLAINED/alg_explained.tex` and `s01-s13*.tex` (inlined) | companion to the papers |
| `paper/figures/` | five vector figures of the papers | included by the papers | `paper/shared/figures` (regenerate with `code/experiments/make_figs.py`) | yes |
| `code/pdefactor/` | the algorithm: core (modes, structured fit, components), outer Bayesian loop, interpolation, domains, aggregation, validation, simulator, baselines | the code | `PDEFactorML/src/pdefactor` (main) | yes |
| `code/experiments/` | experiment scripts E1-E16 (noise, calibration, domains, random PDEs, GP caches), the paper's worked example, multi-seed benchmark, data extraction and figure scripts | they produced the numbers of the papers | `PDEFactorML/analysis/exp/*.py`, `paper/shared/experiments/*.py`, `make_figs.py` | numbers and figures |
| `code/tools/` | repository tools: paper checks, graph builder and comparison, LaTeX flattening, coverage check, the migration helper | keep the repository verifiable | new | no |
| `tests/` | 33 test files, 224 tests | verification | `PDEFactorML/tests` | explained edition |
| `benchmarks/*.py` | benchmark drivers: benchmark rows, baselines, report generators, micro suites, final report | rerun the evaluations | `PDEFactorML/benchmarks/*.py` | benchmark sections |
| `benchmarks/out/`, `benchmarks/data/` | stored results: benchmark rows, session outputs, example output of the final report, the data behind the figures | the evidence behind the numbers | `PDEFactorML/benchmarks/{out,data}`, `sessions/*`, branch `final-report`, `paper/shared/experiments/data` | yes |
| `claude/benchmark_tables/` | benchmark result tables as markdown (P8 final table, end-to-end summary, queue notes, ...) | readable result tables | `PDEFactorML/benchmarks/out/*.md`, `paper/shared/experiments/data/*.md` | quoted in the papers |
| `claude/archive/pipeline/` | the pipeline's working documents: theory-to-code table T1-T103 (`analysis/THEORY_TO_ALGO.md`), limits, parameters, grouping and domain notes, hand-offs, research log, roadmap | for continuing the work | `PDEFactorML/analysis/*.md`, `HANDOFF*.md`, `RESEARCH.md`, `SESSIONS.md`, `ROADMAP_FOR_CLAUDE.md` | no |
| `claude/archive/sessions/` | plans and reports of the pipeline sessions (aggregation, baselines, domain, interpolation) | what was tried | `PDEFactorML/sessions/*` | no |
| `claude/graph/`, `claude/INVENTORY.md`, `claude/inventory.csv`, `claude/superseded.csv` | graphs (JSON, Mermaid, HTML) of the old and the new repository, the old-vs-new comparison, and the list of files merged into other documents | proof that nothing is missing | built with `code/tools/` | no |

## What was merged or dropped (nothing lost)
- **Flattened papers.** Each manuscript was a project of ~20 files; it is now one `.tex` (the text extracted from the new PDF equals the old PDF's text word for word).
- **Earlier editions** of the analytical and ML material were merged into the papers of branches `analytical` and `ml-layers` (coverage checks in their `claude/PROVENANCE.md`).
- **Not copied:** LaTeX build files, raw run logs, backups, the Lean toolchain binaries, and 225 MB of regenerable Gaussian-process caches (`analysis/exp/cache/*.npz`; `code/experiments/gp_cache*.py` regenerate them).
- **Local Windows paths and the private notes file name** were replaced by placeholders in text files.
