# GATE 9 — specifica dell'algoritmo esteso (coordinatore, 27/10/2026)
Fonti:
- `ALGORITMO_ESTESO.md` rev. 2 (S9-ALG);
- `research/DEVIL/ATTACK-9.md` (DEVIL-9: FATAL 0, CRITICAL 2, MAJOR 12, MINOR 18);
- `work/S9-ALG/RECEPIMENTO.md`;
- `research/CIT-AUDIT/AUDIT-9.md` (CIT-AUDIT-9: 21 voci, 12 VERIFICATO, 3 DATI CORRETTI, 6 PARZIALE, 0 CONTENUTO DIVERSO, 0 NON TROVATO);
- `inbox/central-F6.md`.

## 1. Esito
- **Proposta di DEVIL-9.** «Passa con fix obbligatori O1, O2, O3, O4, O14».
- **Recepimento.** S9-ALG ha recepito tutti i 32 punti. Due sono in parte delegati al coordinatore: O8 e O31, chiusi al §3.
- **Verifica del coordinatore.**
  - §0.4/§8 a due strati: condizionamento (C) e correttezza condizionata sulla sottocatena 4 → 6 (O1).
  - Tassonomia DM con M2⁺ e M3-hol; DM1 senza ID-ann (O2, O4); DM2 solo ID-LIM(n) (O3).
  - Riga «Contratto» con la novità di SYS-EX condizionata alla CIT su Oberst 1993 (O14).
  - Script degli esempi rieseguiti dal coordinatore con `.venv -I`: L6 Dirac 7/7, L7 Pöschl–Teller 11/11, L8 Stark 5/5, L9–L10 dizionario 12/12, **tutti PASS**.
- **Fonti (CIT-AUDIT-9).**
  - SYS-EX è NOTO su ℝ^n (Oberst 1993, letto solo nell'abstract) e PROBABILMENTE NOTO su Ω convesso (Oberst 1990 (4.32), VERIFICATO). Resta un delta proprio solo per Ω connesso con C^∞(Ω) non iniettivo.
  - SYS-N1 è folklore.
  - SYS-T0 (Heij 1992), ENC-K1′ (Andrianov–Sokolov 2003) e VAR-L0–L2 (Isakov 1993, via Huang 2021) sono NOTI.
  - B2/CONV-Q17 è chiuso con Oberst 1990 (4.32).
  - I valori di verità non cambiano: cambia solo l'attribuzione della novità. Nessun lemma positivo citato è dichiarato nuovo.

## 2. Decisione
**ALGORITMO_ESTESO.md rev. 2 è approvato come specifica di Fase 9**, con il contratto a due strati:
1. **Strato di condizionamento (passi 1–3):** completezza (C) e uscite discrete, compresa `NON-DECISO` a budget n_max.
2. **Strato di correttezza condizionata (passi 4 → 6):** «al livello n, nella classe K», sotto CONV-T7 con Magnus condizionato.

Il senso di "identifica" è sempre dichiarato tra ID-ann, ID-ker, ID-res, ID-fam e ID-lim, insieme al modello di dati (DM1 relativa, DM2 → ID-LIM(n), M2⁺, M3-hol, DM3, DM-δ(Y) con norma dichiarata).

Novità dichiarata (ATTACK-8 O6, ATTACK-9 O14): la composizione L6–L10 sotto un unico contratto e le negative nuove (DICT-N1, DICT-A-iii, CONV-T2′, VAR-T1(c)-F, ENC-P0(b)). I singoli lemmi positivi non sono dichiarati nuovi.

## 3. Punti delegati al coordinatore (chiusi qui)
- **O8.** Trotter–Kato/splitting non è un fondamento della specifica. Riga LEDGER «ALG-TK» (Fase 10, F10-G9) registrata come CON-FONTE (Trotter 1959; Kato 1978; Engel–Nagel III.5.8) solo per V limitato o relativamente limitato con ipotesi dichiarate. Per V non limitato vale la classe (C) (VAR-T10(5)).
- **O31.** Nel LEDGER il minorante di |u| in VAR-P3 si chiama κ; δ resta riservato al rumore DM-δ. La nota di rinomina è registrata nella sezione «Fase 10» del LEDGER. I valori non cambiano.

## 4. Rinvii alla Fase 10
- S10-INT: applicazione della revisione limitata di Gate 3 (GATE8 §3) e della §0.2(b′) di SYNTHESIS-2 (O17 di ATTACK-8). NOTAZIONE v6 è già scritta.
- Esempi da manuale: Dirac libero, Schrödinger armonico e di Pöschl–Teller, calore frazionario, Maxwell nel vuoto.
- Chiusura dei problemi aperti (S10-OPEN-A/B/C): ogni APERTO esce risolto, confutato o come «APERTO — ridotto a …», con un'ostruzione provata.

---
## ESITO DEL GATE 9 (27/10/2026) — approvazione automatica per delega dell'utente
Gate 9 è approvato come al §2, per la delega dell'utente del 26/10, **registrato e revocabile**. L'utente ha chiesto il 27/10: «FINISCI CON IL GATE 9 POI PREPARA E FINISCI LA FASE 10».
