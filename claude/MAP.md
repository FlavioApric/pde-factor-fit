# MAP of `ml-layers`

```mermaid
flowchart TD
  R[README.md] --> P[paper/ml_layers/main.tex]
  R --> S[src/pdefactor]
  R --> T[tests]
  R --> B[benchmarks/ml_layers]
  R --> C[claude]
  S --> LP[loop.py: hooks _lb_skip, _highk, attach]
  S --> LRN[learned/]
  LRN --> CFG[config.py: Learned switches]
  LRN --> MEMO[memo.py, budget.py: LB]
  LRN --> VAL[validator.py, resid.py, features.py: V1, L2b]
  LRN --> CAL[calibrate.py, apply.py: L2c, L2d]
  LRN --> HK[highk.py: H0]
  LRN --> CT[controller.py, remedy.py, runconfig.py: C]
  LRN --> SD[expseeds.py, expsum.py: L0]
  T --> TO[test_learned_off.py + data/learned_off_golden.json]
  T --> TC[test_ml_contract.py]
  T --> TL[test_learned_*.py, test_runconfig.py]
  B --> BC[ll_corpus.py, ll_inject.py: corpora]
  B --> BG[ll_gate.py, ll_v1.py, ll_ptop.py, ll_l2c.py: gates]
  B --> BB[ll_budget_*.py: LB]
  B --> BR[results/: reports behind every number]
```

| paper section | code | tests |
|---|---|---|
| 3 contract | `learned/config.py` | `test_learned_off.py`, `test_ml_contract.py` |
| 4 protocol | `ll_corpus.py`, `ll_inject.py`, `ll_gate.py` | `test_learned_inject.py` |
| 5 memo | `learned/memo.py` | `test_learned_budget.py` |
| 6 V1 | `learned/validator.py` | `test_learned_v1.py`, `test_learned_resid.py` |
| 7.1 LB skip | `learned/budget.py` | `test_learned_budget.py` |
| 7.2 L2b/c/d | `learned/ptop.py`, `calibrate.py` | `test_learned_ptop.py`, `test_learned_layers.py` |
| 7.4 C | `learned/controller.py` | `test_learned_controller.py`, `test_runconfig.py` |
