# MAP of `model-expansion`

```mermaid
flowchart TD
  R[README.md] --> P[paper/model_expansion/main.tex]
  R --> EX[examples/]
  R --> S[src/pdefactor]
  R --> B[benchmarks/out_of_class_inject.py]
  R --> C[claude/notes/ALGORITMO_ESTESO_it.md]
  P --> L[ladder L0-L10]
  P --> A[six-step algorithm]
  P --> D[directions table]
  EX --> E6[L6 Dirac]
  EX --> E7[L7 Poschl-Teller]
  EX --> E8[L8 Stark]
  EX --> E9[L9/L10 dictionary]
  S --> V[validate.py: detectors]
  S --> DM[domain/, aggregate.py, cluster.py: frozen-coefficient cells]
  B --> INJ[nonlinear, varcoef, fractional, two_laws, coloured, hetero, aliasing]
```

| paper | where |
|---|---|
| section 2 vocabulary | notes, spec section 0 |
| section 3 algorithm | notes, spec sections 1-8 |
| section 5 examples | `examples/*.py`, `tests/test_examples.py` |
| section 6 route | `src/pdefactor/validate.py`, `domain/`, `benchmarks/out_of_class_inject.py` |
