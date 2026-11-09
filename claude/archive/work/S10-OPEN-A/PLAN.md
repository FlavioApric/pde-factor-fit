# PLAN — S10-OPEN-A (27/10/2026)

Compito: dare un esito onesto (prova, controesempio, oppure ostruzione/riduzione dimostrata) per le righe APERTO delle Fasi 1–4 elencate nel mandato. Scrivo solo in `work/S10-OPEN-A/` e in `inbox/` (append).

Skill caricate: `skills-local/session-protocol`, `skills-local/claim-lifecycle` (letti per intero). Dalla catena di claim-lifecycle uso proof-writer (triage PROVABLE AS STATED / AFTER WEAKENING / NOT JUSTIFIED, prova o rapporto di blocco) e SymPy solo come verifica (`.venv\Scripts\python.exe -I`). Gli audit (proof-checker, kill-argument) sono richiesti al coordinatore in `CHECK_REQUEST.md`: nessuno stato proposto supera PROVA SCRITTA.

## 0. Ricognizione (fatta)
Lettura del LEDGER completo. Molte delle righe elencate nel mandato sono righe **storiche**: il LEDGER ha righe successive con lo stesso problema già chiuso e auditato (regola "lo stato valido è l'ultimo", riga 165). Le tratto come "chiusura già registrata": controllo che la riga di chiusura esista, che l'audit sia citato e che non resti un residuo. Se resta un residuo, lo attacco.

## 1. Ordine di trattabilità, predizione, limite di tempo

| # | problema | sede | predizione | limite |
|---|---|---|---|---|
| 1 | II-L1(b) | LEDGER r. 70 | già DIMOSTRATO (S-CHECK-6); in lista per la parola "APERTO-con-prova" | 5 min |
| 2 | P4-Q-min, P4-T5 ("esattamente") | OP-ALG-T3 (r. 111), OPR2-C2 (r. 156) | chiusura già registrata, nessun residuo | 10 min |
| 3 | OP-ALG-Q1, OP-ALG-Q2 | OPR2-T3 (r. 154), OPR2-C2 (r. 156) | chiusura già registrata | 10 min |
| 4 | EX-Q1 | OPF5B-C4 (r. 170) | chiusura già registrata | 5 min |
| 5 | OPF-Q1, OPF-Q3 | OPR2-T1 (r. 151), OPF5B-T1 (r. 166–167) | chiusi (il parallelogramma è convesso) | 10 min |
| 6 | P1-Q5 = OPA-P4 | OPF5A-T5 (r. 182) | chiuso (dati compatibili, ogni k) | 5 min |
| 7 | P3-Q-bordo | OPA-T2 (r. 146), OPF5A-T5 | chiuso | 5 min |
| 8 | C12-Q6 | OPF-T4 (r. 138) | chiuso come criterio coomologico; parti (iii),(iv)(c,d) mod CON-FONTE | 10 min |
| 9 | C3-Q1 | OP-ALG-T1, P4-T5, OP-ALG-T3, CONV-T2 | chiudibile come **classificazione per modello di dati** (nessuna matematica nuova, solo composizione di righe DIMOSTRATE) | 20 min |
| 10 | P1-Q6 | OPA-T3, OPA-P3 | residuo: termini **costanti** (ordine zero) e (ND). Predizione: lemma di riduzione che elimina i termini costanti ⇒ classificazione completa per termini monomi: no-go ⟺ almeno due monomi non costanti; controesempio all'enunciato letterale: reazione–diffusione | 45 min |
| 11 | P2-Q1 (domini non convessi) | OPF5B-T1 + C1(d) | predizione: (a) densità su ogni Ω lipschitziano limitato semplicemente connesso (Passi 2 e 8 riscritti; collare CON-FONTE); (b) **FALSO** con buchi: Laplaciano sull'anello, codimensione = b₁; (c) limite generale codim ≤ δ(P)·b₁(Ω); residuo: domini non lipschitziani | 90 min |
| 12 | P1-Q7 | P1-T5, AUDIT_P1 O-2 | predizione: l'ipotesi si toglie quando l'algebra ammette dilatazioni pesate (algebra libera, esempio x^a∂, ∂ del pacchetto), anche a ε fissato; caso generale ridotto a algebre senza dilatazioni | 90 min |
| 13 | C12-Q2 = OPF-Q2 | OPR2-L1, OPR2-T2, OPF5B-P8 | predizione: nessun controesempio né prova generale; riduzione dimostrata: con coppie chiuse, se un fattore ha interazioni compatte con gli altri due la tripla è chiusa ⇒ un controesempio richiede ≥ 2 coppie a interazione non compatta | 45 min |

## 2. Criterio di "fatto"
Per ogni problema una riga in `LEDGER_ROWS.md` con esito (a)/(b)/(c); prove in `PROOF_PACKAGE.md`; SymPy in `sympy/`; richieste di audit in `CHECK_REQUEST.md`; residui in `open_questions.md`; `DONE S10-OPEN-A` in `inbox/central-F6.md`.

## 3. Contatti
Coordinatore via `inbox/central-F6.md`. Sessioni sorelle S10-OPEN-B/C: nessuna sovrapposizione nota (i loro problemi non sono nella mia lista).
