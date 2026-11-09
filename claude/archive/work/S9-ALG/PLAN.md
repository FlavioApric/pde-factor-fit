# PLAN — S9-ALG (Fase 9: specifica dell'algoritmo esteso) · 27/10/2026

## Compito
Scrivere `ALGORITMO_ESTESO.md`: pipeline in 7 passi (modello di dato → livello di 𝓓_∞ → identificazione → misfit / migliore approssimazione → encoder per V → fattori, termini, E_int → convergenza). Per ogni passo: input/output, claim del LEDGER citati per ID con stato, ipotesi, costo, modi di fallimento (teoremi negativi), senso di "identifica" (ID-ann, ID-ker, ID-res, ID-fam, ID-lim). La specifica sarà attaccata da DEVIL-9.

## Skill caricate (in ordine d'uso)
1. `skills-local/session-protocol` (letta per intero): piano, inbox append-only, consegna, DONE.
2. `skills-local/claim-lifecycle` (letta per intero): vocabolario degli stati; la regola "lo stato non sale senza il controllo". S9-ALG **non crea claim nuovi**: la specifica è una composizione di claim esistenti. Gli esempi da manuale sono verifiche V-ex, non teoremi.
3. `caveman` solo per la chat; i file restano in prosa italiana normale.
Nessuno script `_vendor` eseguito.

## Fonti
PIANO_FASI_6-11 (Fase 9); PROBLEM v3.1 (G★′, G★′-NL, G★″); GATE8 (§2 strade, §3 Gate 8b, §5 rinvii, in particolare la regola DM3/DM2 e Magnus condizionato); NOTAZIONE v5; claims/LEDGER (Fasi 1–5 e Fase 8, con la tabella delle decisioni del coordinatore che prevale); ATTACK-8 (O1–O21, in particolare O4, O5, O7, O8, O10, O19, O20); REPORT_FINALE (catena scalare, S5-SINT); per i dettagli tecnici: work/S8-CONV/PROOF_PACKAGE §1–§2, §9; work/S8-DICT/PROOF_PACKAGE §0, §2, §3, §3.6, §4, §6; work/S8-VAR/PROOF_PACKAGE §1.6; work/C3/PROOF_PACKAGE C3-A1.

## Regole di stato adottate nella specifica
- Fondamento di un passo: solo righe DIMOSTRATO o CON-FONTE (incluse le promozioni della tabella del Gate 8).
- PROVA SCRITTA, CANDIDATO, APERTO, CONDIZIONALE, V-ex: citati solo marcati come tali, mai come garanzia.
- DICT-R6(f) e VAR-L2-cor: trattati come PROVA SCRITTA (nessun AVVISO in `inbox/S9-ALG.md` al momento della lettura).
- Identificazione dichiarata in DM3. In DM2 (e, più in generale, con dati rumorosi) solo i moduli di VAR-P3 e la negativa DICT-N1(ii); la robustezza resta domanda aperta (O8). Nota: GATE8 §5 e VAR-Q19 usano "DM2" per i dati rumorosi, mentre NOTAZIONE v5 chiama DM2 il jet in un punto. La specifica tiene separati i due sensi e segnala l'ambiguità al coordinatore (AVVISO).
- Magnus: (B) solo in dimensione finita o sotto Casas 2007 Thm 3.4 in rappresentazione d'interazione; altrimenti Dyson (O4).
- Encoder: solo traduzione a q noto (O7), mai sorgente d'informazione.

## Struttura di ALGORITMO_ESTESO.md
§0 convenzioni (stati, etichette ID-*, contratto A/B/C/Lim, (H-ex), (H-ID));
§1–§7 i sette passi, ciascuno con la scheda fissa (input, output, claim → stato, ipotesi, costo, fallimenti, senso di "identifica");
§8 la pipeline come catena (CONV-T7) e cosa promette all'utente;
§9 esempi da manuale per livello (L6 Dirac 1+1, L7 Pöschl–Teller, L8 Stark/Avron–Herbst, L9 frazionario indistinguibile, L10 dizionario sul calore), verificati in `work/S9-ALG/sympy/`;
§10 tabella «claim usati → stato»;
§11 domande aperte (rinvio a `open_questions.md`).

## Contatti
Coordinatore (`inbox/central-F6.md`): PLAN-READY, AVVISO sull'ambiguità DM2, DONE. DEVIL-9: attaccherà il testo dopo la consegna.

## Criterio di "fatto"
ALGORITMO_ESTESO.md completo con i 7 passi e le schede; esempi L6, L7, L8, L10 (più L9) con script SymPy eseguiti e uscita salvata; tabella claim → stato coerente con il LEDGER (decisioni Gate 8 prevalenti); open_questions.md; DONE S9-ALG in inbox/central-F6.md.
