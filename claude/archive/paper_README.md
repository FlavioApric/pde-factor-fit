# Two manuscripts for SIMODS: grouping structure of linear PDEs in learning

Two complete versions of the same paper, built from one set of shared sections, so that a correction is made once.

| Folder | Structure |
|---|---|
| `A_user_structure/` | the author's outline: analytical part → nonlinear → algorithm → statistical layer → results → solvable/unsolvable inference problems → conclusions |
| `B_proposed_structure/` | one idea first ("groups are factors"): running example in the introduction, grouping principle with a theorem dependency graph, learning within one sample, grouping across samples, evidence, discussion |
| `shared/` | `macros.tex` (notation, one symbol one meaning), `sections/*.tex` (all content modules), `refs.bib`, `figures/` (PDF figures + `make_figs.py`), `experiments/` (run scripts and the stored data behind every number) |
| `tools/` | `hygiene.sh` (no internal vocabulary in the manuscripts), `check_notation.py` (every notation macro is in the notation table) |

`COMPARISON.md` compares the two versions.

## Build

```
cd paper/A_user_structure && latexmk -pdf main.tex
cd paper/B_proposed_structure && latexmk -pdf main.tex
```

SIMODS is typeset with SIAM's `siamonline` class, which is not on CTAN. Put `siamonline<date>.cls` and
`siamplain.bst` from SIAM's author page in each paper folder (or in `shared/`); `shared/docclass.tex` picks it up
automatically. Without it the papers build with the fallback `shared/siamshim.tex` (same theorem environments,
keywords, MSC codes and headers), which is fine for reading but not for submission. The CI job `.github/workflows/paper.yml`
builds both papers and tries to fetch the class.

## Reproduce the numbers and figures

The runs use the package `pdefactor` (`src/`) and the report script `benchmarks/final_report.py`. From the repository root with the package installed (`pip install -e .`):

```
python paper/shared/experiments/worked_example.py --case transport_plus_diffusion --noise 0.05 --out runs/tpd_grid5_bench
python benchmarks/final_report.py --case transport_plus_diffusion --noise 0.05 --S 32 --out runs/tpd_5pct_S32
python paper/shared/experiments/worked_example.py --case beam --noise 0.05 --out runs/beam_grid5     # also klein_gordon, telegraph, advection_diffusion (out: advdiff_grid5)
python paper/shared/experiments/extract_data.py --runs runs --out paper/shared/experiments/data
python paper/shared/figures/make_figs.py
PDEFACTOR_FIELD_SEED=1 python paper/shared/experiments/multiseed.py --out paper/shared/experiments/data/multiseed.jsonl --workers 4 --methods pipeline weak_sindy
```

The benchmark tables come from `shared/experiments/data/p8_final_v5.md` (copied from branch `ml`,
`benchmarks/p8_final_v5.md`).

## Before submission

- Install the official SIAM class and rebuild.
- The proofs are complete in Appendix A but have not yet been checked by an independent human referee.
