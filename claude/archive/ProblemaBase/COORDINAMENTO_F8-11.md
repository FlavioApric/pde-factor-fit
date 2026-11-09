# COORDINAMENTO — Fasi 8–11 (coordinatore, 27/10/2026)
Fonti: `PIANO_FASI_6-11.md`, `SESSIONS-F8.md`, `GATE6.md`, `RIPRESA.md` (punto di ripresa fork), `REPORT_FINALE.md` §6.3.

## 0. Stato verificato su disco (27/10/2026)
- Fasi 1–5: chiuse (REPORT_FINALE v2, LEDGER, PBLean `lake build` OK, graphify-out).
- Fase 6: chiusa (SYNTHESIS-2, ATTACK-6, AUDIT-6, GATE6 auto-approvato).
- Fase 7: chiusa (nessuna skill nuova; roster SESSIONS-F8).
- Fase 8: avviata e interrotta dal limite d'uso. Su disco: PLAN.md in S8-SYS, S8-VAR, S8-ENC, S8-DICT; nulla in S8-CONV. SymPy parziale solo in S8-ENC (3 script) e S8-DICT (1 script). Nessun PROOF_PACKAGE, nessun DONE.
- **GATE6 §2 punto 4 NON applicato**: PROBLEM.md è ancora v2 (manca G★″), ROUTES senza SYNTHESIS-2 §4, NOTAZIONE senza v4. Il blocco "dopo REPORT_FINALE" è caduto: REPORT_FINALE esiste.
- Fasi 9, 10, 11: non iniziate (nessun ALGORITMO_ESTESO.md; PBLean senza target di Fase 10; PAPER/paper.tex senza sezione "Algoritmo esteso").

## 1. Cosa manca al completamento (in ordine)
1. **C0 (coordinatore, subito):** applicare GATE6 §2.4 → PROBLEM v3 (G★″ = SYNTHESIS-2 §5), ROUTES (SYNTHESIS-2 §4), NOTAZIONE v4 (DM-φ, DM-inv, MF1–MF3, (H-ID), E^conj). La fork non ha più vincoli su LEDGER/BOARD/ROUTES/PROBLEM/NOTAZIONE: canale unico torna `inbox/central.md` (central-F6 resta leggibile).
2. **Fase 8:** rilancio S8-SYS, S8-VAR, S8-ENC, S8-DICT, S8-CONV ("riprendi da work/<ID>/"). Audit S-CHECK-F8 per sessione, DEVIL-8, CIT-AUDIT-8, `GATE8.md` (8a strade, 8b revisione struttura Gate 3 / G★′-NL), righe LEDGER.
3. **Fase 9:** `ALGORITMO_ESTESO.md` (7 passi) + DEVIL-9.
4. **Fase 10:** S10-INT (integrazione notazione/ipotesi) poi S10-LEAN (target algebrici in PBLean, no sorry, solo assiomi standard, revisore indipendente) + esempi da manuale.
5. **Fase 11:** S11-PAPER (estende PAPER/paper.tex) + audit finale (proof-checker, CIT, DEVIL). Gate finale con l'utente.
6. Facoltativo, parallelo e a bassa priorità: residui di REPORT_FINALE §6.3 (INT-Q1, L-loc, OPF5C-Q1, domini non convessi…). Non bloccano G★″.

## 2. Grafo delle dipendenze
```
C0 (PROBLEM v3/ROUTES/NOTAZIONE v4)
 │
 ├─► S8-SYS ──────────────┐            (L6; dà U4 a DICT, gauge a ENC)
 ├─► S8-VAR ──► S8-ENC ───┤            (ENC-N1 e ENC-T2 usano VAR-T1/VAR-P4)
 ├─► S8-CONV ─► S8-DICT ──┤            (I-LIM di DICT usa CONV-T*; DICT usa U4 da SYS)
 │        ▲ VAR-P3 (stabilità) → CONV
 │                        ▼
 │   S-CHECK-F8 (pipeline: un audit per sessione appena DONE, con KA sui claim critici)
 │                        ▼
 │        DEVIL-8 ∥ CIT-AUDIT-8 ─► GATE8 (8a, 8b) ─► LEDGER (coordinatore)
 │                        ▼
 │        Fase 9: ALGORITMO_ESTESO ─► DEVIL-9
 │                        ▼
 │        Fase 10: S10-INT ─► S10-LEAN (può partire prima sul nucleo SYS auditato)
 │                        ▼
 └──────► Fase 11: S11-PAPER ─► audit finale ─► Gate finale (utente)
```
Le frecce dentro la Fase 8 sono **dipendenze morbide**: le cinque sessioni partono insieme e si scambiano risultati via `inbox/<ID>.md`. Le dipendenze dure sono solo tra fasi (audit → gate → LEDGER → fase successiva).

## 3. Come coordinare le sessioni
- **Coordinatore = questa sessione.** Unico che scrive BOARD, ROUTES, NOTAZIONE, PROBLEM, LEDGER, RIPRESA.
- **Ondata A (subito):** S8-SYS, S8-VAR, S8-CONV — sono a monte. **Ondata B:** S8-ENC e S8-DICT, appena VAR e CONV pubblicano in inbox gli enunciati portanti (non serve il DONE). Se il budget d'uso lo consente, tutte e cinque insieme. Motivo dello scaglionamento: la Fase 8 è già stata interrotta una volta dal limite d'uso.
- Ogni sessione: prompt = riga di SESSIONS-F8 + regole comuni + "riprendi da work/<ID>/" + `/caveman` (solo per la chat; i file su disco restano in prosa normale).
- Al `DONE <ID>` in inbox: il coordinatore lancia subito S-CHECK-F8-<ID> (pipeline, non attende le altre).
- Dopo ogni passo: aggiornare RIPRESA.md (ripresa da altra sessione).
- Gate: auto-approvati per delega dell'utente (26/10), registrati e revocabili; Gate finale con l'utente.

## 4. Skill e strumenti
- Bastano le skill di progetto (`skills-local/`: session-protocol, claim-lifecycle, route-scout, kernel-catalog-entry, formalize-claim, spec-sync) e i SKILL.md letti da `_vendor` (proof-checker, proof-writer, kill-argument, lean-formalize, academic-paper). Nessuna skill nuova necessaria.
- Lean/elan/lake presenti; PBLean compila.
- Ancora in sospeso dallo Step 0 (decisione dell'utente): installazione globale delle skill ARIS in `~/.claude/skills` (utile ma non necessaria: le sessioni leggono i SKILL.md) e Mathpix (non necessario).
