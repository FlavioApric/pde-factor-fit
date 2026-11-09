# PLAN — S8-VAR (Fase 8, L7–L8: coefficienti variabili, identificazione di V, non autonomo, C3-Q2)
27/10/2026. Riparto da `research/F6-VAR/{VERDETTO,NOTE}.md` (completare, non ricominciare). Canale: `inbox/central-F6.md`. Scrivo solo in `work/S8-VAR/` e in `inbox/` (append).

## 0. Letture e skill caricate (lettura integrale dei SKILL.md, nessuno script `_vendor`)
Letti: SESSIONS-F8.md (riga S8-VAR), GATE6.md, research/SYNTHESIS-2.md (fix F1–F10, §7 CIT-AUDIT-6), research/F6-VAR/VERDETTO.md, NOTE.md, open_questions.md, sources.bib, research/DEVIL/ATTACK-6.md (O1, O5, O9, O10), research/CIT-AUDIT/AUDIT-6.md (righe 19, 31, F6-VAR, §3.6), PROTOCOLLO.md, LEDGER (C3-T1, P1-T4/T5/P5, P3-T1; C3-Q2 e C12-Q5 non hanno riga: sono in work/C3 e work/C1C2), research/R5/REPORT.md (R5-P7), work/P1/PROOF_PACKAGE.md (P1-T4, P1-P5).
Skill: `session-protocol`, `claim-lifecycle` → catena `proof-writer` (struttura del pacchetto: enunciato, ipotesi, stato, strategia, dipendenze, prova, rischi) → `math-skill` modo `proof` (controesempi e casi limite prima della prova) + `sympy` → `proof-checker` **non** lanciato come subagente (l'audit indipendente è S-CHECK-F8, per la regola 3 di SESSIONS-F8; preparo CHECK_REQUEST.md con la checklist della skill: ipotesi, quantificatori, ordine dei limiti) → `kill-argument` solo come auto-attacco scritto sui claim del cammino critico (VAR-T1, VAR-P8) → `scientific-critical-thinking` per gli stati finali.

## 1. Predizione scritta (prima del lavoro)
1. **VAR-T1** (zeri di u): prevedo una caratterizzazione **incondizionata** dell'identificabilità in termini dell'insieme X_0 = {x : u(·,x) ≡ 0} (V ∈ C: ⟺ int X_0 = ∅; V ∈ L^∞: ⟺ |X_0| = 0) e una parte **condizionata** all'unicità del Cauchy laterale: Holmgren la dà per V analitico (con un argomento di spazzata per globalizzare); per V ∈ L^∞ mi aspetto di **non** poter chiudere: registrerò il teorema candidato (Saut–Scheurer 1987 / Tataru 1995 — da verificare) come lacuna dichiarata.
2. **VAR-P3, P4, P5, N1, P9, P12**: prove elementari complete; P3 con controesempio esplicito di non continuità e stabilità hölderiana con esponente esplicito; P4 col modello DM-φ dichiarato.
3. **VAR-T2/T6**: prova autosufficiente a partire dal solo teorema di Galois E^G = K (van der Put–Singer, numero da verificare); per ordine 2 un criterio elementare senza Galois (u identifica ⟺ u′/u ∉ K). Esempio oscillatore chiuso completamente (risolve in parte VAR-Q6). Confronto VMPUM: delta = criterio strutturale + ostruzione iperesponenziale (proprio la classe di dati di SLZ 2011).
4. **VAR-P8** riscritto (F5): prevedo di estendere la parte "⟹" a **V liscia qualsiasi** (risolvendo VAR-Q3) e di dare il propagatore esplicito di Pöschl–Teller via Darboux con E_int A9 in forma chiusa.
5. **VAR-T10** corretto: parola chirp·libero·chirp valida per |t| < π; più in generale per ω(t) valida finché M_12(t) ≠ 0 (primo punto coniugato). Magnus: Casas 2007 (Hilbert), Moan–Niesen solo matrici reali.
6. **VAR-P11**: prova completa della forma mild (Dyson–Phillips non autonomo), regolarità classica CON-FONTE.
7. **C3-Q2** (tempo limitato): prevedo un risultato **parziale**: criterio per operatori monici in ∂_t (divisione), caso libero e oscillatore risolti esplicitamente; ostruzione registrata per operatori non monici e V non quadratici. Kill: se la riduzione per divisione fallisse (non lo prevedo).
Criterio d'uscita: ogni claim della riga con prova completa, FALSO, o lacuna dichiarata con teorema candidato; CHECK_REQUEST pronto; C3-Q2 risultato o ostruzione registrata.

## 2. Ordine di lavoro (salvataggio dopo ogni enunciato)
PLAN → PROOF_PACKAGE §1 (N1, T1, P3, P4, P5) → §2 (T2, T6, VMPUM, C7) → §3 (P8, Pöschl–Teller) → §4 (P9, P11, T10, P12) → §5 (C3-Q2) → SymPy (`sympy/s8_*.py`, .out) → CHECK_REQUEST, LEDGER_ROWS, open_questions → inbox (S8-SYS, S8-ENC, S8-CONV; DONE in central-F6).
Contatti: S8-SYS (Dirac VAR-P5, VMPUM), S8-ENC (Pöschl–Teller esplicito, DM-φ), S8-CONV (etichette A/B/C di VAR-T10).
