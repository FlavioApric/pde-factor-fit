# Paper of branch `ml-layers`

`ml_layers/main.tex`: *Learned Layers for a Factor-Based PDE Pipeline: What Worked, What Did Not, and Why*, by Flavio Pricoco.
Shared LaTeX infrastructure (document class fallback, preamble, notation macros, bibliography) is in `shared/`.

```bash
cd paper/ml_layers && latexmk -pdf main.tex
```

Without SIAM's `siamonline` class (not on CTAN) the paper builds with the fallback in `shared/siamshim.tex`.
Every number in the paper comes from `benchmarks/ml_layers/results/` or from the experiment scripts in `benchmarks/ml_layers/`.
Licensed CC BY 4.0, see `../LICENSE-papers.md`.
