# Roster della Fase 8 (prove) — v1, 26/10/2026 (coordinatore, sessione fork; Gate 6 auto-approvato)
Bersaglio: G★″ (`research/SYNTHESIS-2.md` §5; `GATE6.md`). Obiettivi per sessione: SYNTHESIS-2 §6 + fix F1–F10 di DEVIL-6 + correzioni di CIT-AUDIT-6.

## Regole comuni (come in Fase 3–4)
1. Carica `skills-local/session-protocol`, `skills-local/claim-lifecycle` (catena: proof-writer → PROOF_PACKAGE.md; math-skill in modo controesempio/limite; SymPy; CHECK_REQUEST.md per S-CHECK; kill-argument sui claim del cammino critico), e `skills-local/kernel-catalog-entry` se catalogi nuclei. Leggi i SKILL.md esterni indicati da claim-lifecycle; **non eseguire script `_vendor`**.
2. **PLAN prima di tutto** in `work/<ID>/PLAN.md` con **predizione scritta** (che cosa ti aspetti di dimostrare o refutare) e criterio d'uscita; poi `PLAN-READY <ID>` in `inbox/central-F6.md`.
3. Stati onesti: niente DIMOSTRATO senza S-CHECK. Riferimenti: usa le correzioni di `research/CIT-AUDIT/AUDIT-6.md`; numeri di teorema non verificati marcati "da verificare".
4. **Niente machine learning.** SymPy solo come verifica: `D:\ProblemaBase\.venv\Scripts\python.exe -I work/<ID>/sympy/<script>.py`.
5. Scrivi **solo** in `work/<ID>/` e `inbox/` (append). **Non** toccare LEDGER, BOARD, ROUTES, PROBLEM, NOTAZIONE, RIPRESA, PBLean, `work/S4-*`, `work/S5-*`, `work/CHECK`, `inbox/central.md` (li usa la sessione che chiude la Fase 5). Canale verso il coordinatore: `inbox/central-F6.md`.
6. Consegne: `PLAN.md`, `PROOF_PACKAGE.md` (enunciati con ipotesi complete, prove), `CHECK_REQUEST.md` (per S-CHECK-F8: claim, punti delicati, domande mirate), `LEDGER_ROWS.md` (righe proposte nel formato di `claims/LEDGER.md`), `sympy/`, `open_questions.md`. Ultima riga in central-F6: `DONE <ID>`.
7. Comunicazione: `inbox/<ID>.md`, formato "[<ID> → X] TIPO: …" (TIPO ∈ DOMANDA, RISPOSTA, TABELLA, AVVISO). Leggi la tua inbox all'inizio, a metà e prima di consegnare.

## Roster
| ID | contenuto (G★″) | criterio d'uscita | contatti |
|---|---|---|---|
| **S8-SYS** | L6: SYS-T1 confrontato con Oberst 1990 e con Schindelar–Levandovskyy–Zerz 2011 (delta dichiarato o declassamento); **criterio d'esistenza** di una soluzione identificante (zoccoli ≤ 1); SYS-N1, SYS-T0, SYS-S1 (anche Ω non convesso semplicemente connesso); SYS-E (P1-T5 per sistemi, corretto F2; Wei–Norman su sl_2⊗ℂ[ξ]); gauge G-T2/SYS-N3; risposta a "λ ∈ Mat 4×4" (forma hamiltoniana) | ogni claim con prova completa o FALSO; CHECK_REQUEST pronto | S8-VAR, S8-DICT |
| **S8-VAR** | L7–L8: VAR-T1 (con zeri di u: Holmgren per V analitico; unicità laterale per V ∈ L^∞), VAR-P3, VAR-P4 (modello DM-φ), VAR-P5, VAR-N1, VAR-T2/T6 (Galois, confronto VMPUM), VAR-P8 riscritto (F5, con Pöschl–Teller esplicito), VAR-P9, VAR-T10 corretto (oscillatore senza "rottura a cos t = 0"; Casas 2007), VAR-P11/P12; C3-Q2 in A_2 (tentativo con limite di tempo) | idem; C3-Q2: risultato o ostruzione registrata | S8-SYS, S8-ENC, S8-CONV |
| **S8-ENC** | B2: ENC-1 (Volterra, ipotesi nell'enunciato), ENC-T2 come lemma "a q noto" (F6), ENC-P0 (eccezioni che cambiano il tempo), ENC-N1 (cieco ⟺ identificabilità congiunta), tabella encoder (F7) con Duistermaat–Grünbaum (V → 0); E_int **A9** per Schrödinger con V (non E^conj); definizione (E2) "modulo costanti" | idem | S8-VAR, S8-DICT |
| **S8-DICT** | L9–L10: U1+N0, U2 (liscezza di F, KMS 18.16), U3(c)+N2, U3(d), ritardo come sistema aumentato (F4), U4; N1(i)–(v) + (a′)/(b′) (F1); Teorema A, MF1–MF3, B2, regole R1–R6, R-STOP; I-LIM con (H-ID); NS-EXPALG (sine-Gordon, e^u via w = e^{iu}, Ax 1971); frazionari (S8-NLOC fuso qui) | idem; N1 con kill-argument | S8-CONV, S8-SYS, S8-ENC |
| **S8-CONV** | P-C: CONV-T1…T6, CONV-P8 (1+d), CONV-T7 come contratto per ALGORITMO_ESTESO; rumore (T3–T5, anche L² hölderiano); bordo e dimensione (S8-NOISE/DIM fuso qui); CONV-Q6 (P3-T3 vs Einkemmer–Ostermann, Dirichlet non omogeneo) | idem | S8-DICT, S8-VAR |
Dopo le consegne: **S-CHECK-F8** (revisore indipendente, `work/CHECK-F8/`), **DEVIL-8** (kill-argument, Gate 8a/8b), **CIT-AUDIT-8**. Gate 8a (strade) e 8b (revisione della struttura di Gate 3 / G★′-NL) auto-approvati con decisioni registrate e revocabili.
