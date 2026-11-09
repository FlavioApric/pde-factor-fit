# S-PHASE4-ML — indice di tutti i file (strati ML della Fase 4)

Branch GitHub: `claude/relaxed-mendel-k3gpne` (PR FlavioApric/ML-PDE-fit#1). Ogni percorso qui sotto è relativo a `PDEFactorML\` (in locale: `D:\PDEFactorML\`).

## Come portarli su D:
In `D:\`, senza toccare il lavoro non committato dell'altra sessione, puoi:
- **solo leggere** i file:
  `git fetch origin claude/relaxed-mendel-k3gpne`
  `git worktree add D:\wt-phase4-ml origin/claude/relaxed-mendel-k3gpne`
  I file finiscono in `D:\wt-phase4-ml\PDEFactorML\...`;
- **integrarli in main**: fai il merge della PR #1 su GitHub, poi `git pull` in `D:\`.

## Documenti (leggere prima questi)
| file | cosa contiene |
|---|---|
| `sessions/S-PHASE4-ML/REPORT.md` | **rapporto finale**: cosa è stato costruito, verdetto del gate per ogni strato (L0 spento, L2c acceso, L2b/V1 spenti), numeri, righe proposte T52–T54 per THEORY_TO_ALGO |
| `sessions/S-PHASE4-ML/LAYER_CANDIDATES.md` | **librerie, repository e algoritmi** valutati come strati aggiuntivi, ordinati per guadagno atteso, con le misure (E15, E16) |
| `sessions/S-PHASE4-ML/RESEARCH.md` | ricerca su modelli pre-costruiti (DeepFreq, Xie–Wakin–Tang, SAMP, MAPIE, nonconform, …), licenze, scelte |
| `sessions/S-PHASE4-ML/PLAN.md` | piano della sessione e stato finale |
| `analysis/PHASE4_ML_PLAN.md` | il piano di Fase 4 (dall'altra sessione, branch `phase4-ml-plan`), copiato qui senza modifiche |
| `SESSIONS.md` | aggiunta la riga S-PHASE4-ML (solo aggiunta) |

## Codice
| file | cosa fa |
|---|---|
| `src/pdefactor/learned/__init__.py` | pacchetto degli strati appresi; etichetta del prior `prior: sim-v1` |
| `src/pdefactor/learned/expsum.py` | generatore di somme di esponenziali smorzati (dati di addestramento di L0, indipendenti dalla PDE) |
| `src/pdefactor/learned/expseeds.py` | **L0**: rete PyTorch (heatmap smorzamento-frequenza + conteggio), focal loss, proposte con cache, `enable()`/`disable()` |
| `src/pdefactor/learned/calibrate.py` | **L2b/L2c**: isotonica, Venn–Abers, soglie da una loss, inflazione monotona degli intervalli + conformal Mondrian, split per famiglia |
| `src/pdefactor/learned/validator.py` | **V1**: classificatore dei modi di fallimento, controllo del rischio conforme, gate OOD |
| `src/pdefactor/learned/remedy.py` | ordinamento offline dei rimedi per il controller |
| `src/pdefactor/learned/features.py` | adattatori `LoopResult` → caratteristiche (senza identificatori) |
| `src/pdefactor/core/structfit.py` | unica modifica al core: argomento opzionale `seeds=` / `SEED_PROVIDER` in `extract_modes_ic`. Spento = identico a main (golden test) |
| `tests/test_learned.py`, `tests/data/structfit_golden.npz` | 24 test degli strati appresi, più il riferimento bit-per-bit di main |

## Esperimenti (script) e risultati delle simulazioni
Gli script stanno in `analysis/exp/`. Copie dei risultati in `sessions/S-PHASE4-ML/results/` (la cartella `analysis/exp/out/` è esclusa da git).

| esperimento | script | risultato (in `results/`) | esito in breve |
|---|---|---|---|
| E12: L0 contro pencil+BIC | `e12_l0_seeds.py` | `e12_l0_seeds_v1_mse.md/.json`; modello `l0_expseeds_v1_mse.pt` (32 MB, versione con loss MSE) | L0 = controllo (accuratezza d'ordine 0.847 contro 0.847): nessun guadagno |
| E13: corpus di 126 esecuzioni del loop | `e13_corpus.py` | `e13_corpus.jsonl` (dati), `e13_corpus.log` | 10 famiglie v1 per l'addestramento, 11 famiglie GENERAL per il test |
| E14: calibrazione su famiglie mai viste | `e14_calibration.py` | `e14_calibration.md` | **L2c: copertura degli intervalli 0.756 → 0.923** (passa). L2b e V1 falliscono in LOFO |
| E15: limite superiore di qualsiasi seme | `e15_seed_bounds.py` | `e15_seed_bounds.md` | nemmeno i poli veri come semi migliorano: passo per-bin già efficiente (CRB) |
| E16: scansione sui dati grezzi contro percorso GP | `e16_raw_scan.py` | `e16_raw_scan.md` | errore su λ da 1.5 a 3 volte più piccolo per κ ≤ 3; κ = 4 recuperato (il GP non lo trova); κ ≥ 5 senza informazione |
