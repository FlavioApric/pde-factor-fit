# MAP of `model-expansion`

```mermaid
flowchart TD
  R[README.md] --> P[paper/model_expansion.tex + .pdf]
  R --> C[code/]
  R --> T[tests/test_examples.py]
  R --> CL[claude/]
  P --> L[ladder L0-L10]
  P --> A[six-step algorithm + contract]
  P --> Q[four founding questions]
  P --> RT[routes tried, your ideas]
  P --> AP[appendix: specification step by step]
  C --> E6[ex_L6_dirac.py]
  C --> E7[ex_L7_poschl_teller.py]
  C --> E8[ex_L8_stark.py]
  C --> E9[ex_L9_L10_dict.py]
  C --> INJ[out_of_class_inject.py]
  CL --> SP[notes/ALGORITMO_ESTESO_it.md: full specification]
  CL --> PV[PROVENANCE.md, INVENTORY.md]
```

| paper section | where |
|---|---|
| vocabulary, ladder, six steps | spec sections 0-8 (`claude/notes/ALGORITMO_ESTESO_it.md`) |
| four questions, encoders, boundary theorems | `analytical` branch: `claude/notes/SYNTHESIS-2.md`, `claude/proofs/S8-*.md` |
| routes, your ideas | `analytical` branch: `claude/notes/ROUTES.md`, `claude/archive/origin/piano_di_ricerca.md` |
| worked examples | `code/ex_*.py`, `tests/test_examples.py` |
| minimal route | `main` branch: `code/pdefactor/validate.py`, `domain/`; `code/out_of_class_inject.py` |
