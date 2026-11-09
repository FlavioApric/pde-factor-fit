# STATUS of `model-expansion` (2026-11-07)

- Specification: paper section 3 (ladder, six steps); full original in `claude/notes/ALGORITMO_ESTESO_it.md` (Italian).
- Examples: four scripts, 35 checks in total, all pass (`tests/test_examples.py`).
- Code: nothing of the extension is in `src/`. `code/out_of_class_inject.py` generates inputs outside the class; its runner needs `ml-layers`.

## Next steps (minimal route, paper section 6)
1. Detect-and-refuse tests with a theoretical null (no learned detector: a learned one flagged 0 of the injected nonlinear, variable-coefficient and two-law failures).
2. Frozen-coefficient cells for slowly varying V(x) (reuse `domain/`, `aggregate.py`, `cluster.py`).
3. Residual-map identification with a declared class (V(x), then V(t,x) off the silence bands).
4. Nonlinear through a declared dictionary with the least-squares misfit certificate.

## Open
See paper section 7: robustness for variable coefficients under noise, infinite-mode nonlocal example, rigorous enclosure for the misfit residual, tighter bound than C_W, non-monic symbols, higher-dimension sum closure.

## Completeness (2026-11-09)
Paper now 13 pages: added the four questions and answers, the encoder table and boundary theorems, the registry of routes (Gates 1, 4a, 6, 8) with the author's ideas, and the algorithm-side state and open problems.
Sources of every statement: `analytical` branch (`claude/notes/ROUTES.md`, `SYNTHESIS-2.md`, `claude/archive/origin/piano_di_ricerca.md`) and `claude/notes/ALGORITMO_ESTESO_it.md`.

## Layout change (2026-11-09)
The paper is one flat file (`paper/model_expansion.tex`, 21 pp, with the specification appendix). The duplicate copy of the pipeline (`src/`, 34 test files) was removed: the pipeline lives on `main`. Examples and the generator are flat in `code/`.
