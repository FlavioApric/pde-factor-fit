# MAP of `ml-layers`

```mermaid
flowchart TD
  R[README.md] --> P[paper/ml_layers.tex + .pdf]
  R --> C[code/]
  R --> T[tests/]
  R --> B[benchmarks/]
  R --> CL[claude/]
  C --> PF[pdefactor/: pipeline snapshot]
  PF --> LP[loop.py: hooks _lb_skip, _highk, attach]
  PF --> LRN[learned/]
  LRN --> CFG[config.py: Learned switches]
  LRN --> MEMO[memo.py, budget.py: LB]
  LRN --> VAL[validator.py, resid.py, features.py: V1, L2b]
  LRN --> CAL[calibrate.py, apply.py: L2c, L2d]
  LRN --> HK[highk.py: H0]
  LRN --> CT[controller.py, remedy.py, runconfig.py: C]
  LRN --> SD[expseeds.py, expsum.py: L0]
  C --> SI[s_interp_variant/]
  T --> TO[test_learned_off.py + data/learned_off_golden.json]
  T --> TC[test_ml_contract.py]
  T --> TL[test_learned_*.py, test_runconfig.py]
  B --> BC[ll_corpus.py, ll_inject.py: corpora]
  B --> BG[ll_gate.py, ll_v1.py, ll_ptop.py, ll_l2c.py: gates]
  B --> BB[ll_budget_*.py: LB]
  B --> BR[results/: reports and data behind every number]
  CL --> AR[archive/: session plans and reports]
  CL --> NO[notes/: Phase 4 plan, handoff]
  CL --> PV[PROVENANCE.md, INVENTORY.md, benchmark_tables/]
```

| paper section | code | tests |
|---|---|---|
| pipeline and ML inside it | `code/pdefactor/{interp,aggregate,bayes_split,loop}.py` | `test_interp.py`, `test_aggregate_cluster.py`, `test_phase3.py`, `test_loop.py` |
| contract and protocol | `learned/config.py`, `benchmarks/ll_corpus.py`, `ll_inject.py` | `test_learned_off.py`, `test_learned_inject.py` |
| memo, V1, calibration, scan | `learned/{memo,budget,validator,calibrate,highk}.py` | `test_learned_budget.py`, `test_learned_v1.py`, `test_learned_ptop.py`, `test_learned_layers.py` |
| controller | `learned/{controller,remedy,runconfig}.py` | `test_learned_controller.py`, `test_runconfig.py` |
