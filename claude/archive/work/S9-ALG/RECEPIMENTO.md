# RECEPIMENTO — ATTACK-9 (DEVIL-9) in ALGORITMO_ESTESO.md · S9-ALG · 27/10/2026

**Fonte.** `research/DEVIL/ATTACK-9.md`: 0 FATAL, 2 CRITICAL, 12 MAJOR, 18 MINOR. Proposta di Gate 9: «passa con fix obbligatori O1, O2, O3, O4, O14».

**Notazione.** Allineata a NOTAZIONE v6:
- DM2 = getto;
- DM-δ = dato rumoroso con norma dichiarata;
- sensi ID-*;
- (E2) con c(t) e (E2₀);
- (H-ID) come nome unico;
- H-DIRAC sotto H-DIRAC-1/2;
- oscillatore H = −∂² + x²;
- anello dei coefficienti e oggetto canonico ((D·u, u), ρ_u).

**Esito.** Tutti i 32 punti sono recepiti. Nessuno è respinto. Due sono recepiti in parte:
- O8: la riga LEDGER per Trotter–Kato spetta al coordinatore;
- O31: rinominare il minorante in VAR-P3 è una modifica del LEDGER; nella specifica si usa κ, con un rinvio a VAR-P3.

## Fix obbligatori

| fix | gravità | modifica in ALGORITMO_ESTESO.md |
|---|---|---|
| **O1** | CRITICAL | §0.4 riscritto in due strati: i passi 1–3 sono **condizionamento**, con uscite discrete fuori da CONV-T7 e completezza (C); la **correttezza condizionata** «al livello n, nella classe K» vale sulla sottocatena 4 → 6, l'unica a cui si applica CONV-T7. Etichetta doppia (completezza, correttezza). Aggiunta la riga «Contratto» ai passi 1, 2, 3a, 3b, 3c. §7: Input/Output aggiornati, motivo CONV-T3 tra i fallimenti. §8 riscritto: schema a due strati e promesse 1–6 tutte «condizionate al livello e alla classe» |
| **O2** | CRITICAL | §0.2: ID-ann «mai per u EP» (P4-T2). §0.3: tabella dei modelli. DM1 ammette solo ID-ker relativa in una classe finita (C3-T4, C3-T2(c,d)). Introdotto **M3-hol** (forma chiusa olonoma non EP). §1 e §3a: «Senso» corretto, controesempio e^{−t}cos x tra i fallimenti. §0.5 e §8 punto 2. §9: gli esempi 9.1–9.3 sono dichiarati M3-hol/DM3 |
| **O3** | MAJOR (obbligatorio) | §0.3: DM2 solo ID-lim, contratto (Lim), nessun certificato (CONV-T1, C3-P1[M2]). §1: C3-T3 citato «solo per u EP», CONV-T1 tra i claim e il controesempio dei getti (ATTACK-9 §3(C)) tra i fallimenti. §8 punto 4: DM2 → `ID-LIM(n)`. §0.5: nuova etichetta `ID-LIM(n)` |
| **O4** | MAJOR (obbligatorio) | §0.3: aggiunti **M2⁺** (getto + test di zero / ideale olonomo dichiarato; P4-T6 modulo (AC)) e **M3-hol** (OP-ALG-T1), ciascuno con i sensi ID-* e il contratto. §1: P4-T6 attribuito a M2⁺ e OP-ALG-T1 a M3-hol |
| **O14** | MAJOR (obbligatorio) | Precondizione soddisfatta: CIT-AUDIT-9 (`research/CIT-AUDIT/AUDIT-9.md`) ha letto Oberst 1990 (VERIFICATO); Oberst 1993 è PARZIALE (testo pieno non accessibile). §3b, «Claim → stato»: SYS-EX su Ω arbitrario DIMOSTRATO con prova propria, ℝ^n NOTO, convesso PROBABILMENTE NOTO. Riga «Contratto»: **novità condizionata a CIT Oberst 1993**, rischio basso–medio. §8: il delta di SYS-EX non è dichiarato come novità. §10: elenco delle citazioni da chiudere |

## MAJOR

| fix | modifica |
|---|---|
| **O5** | §3b: nuova riga «H-DIRAC, due sensi». H-DIRAC-ann ha la premessa ψ_2 ∉ EP; H-DIRAC-ker ha rango 8, che vale anche per un dato EP con ≥ 4 modi generici e fallisce con 1 sola onda piana. §9.1(c) corretto («il fallimento dipende dal numero di modi, non dall'essere EP»), con rinvio ad ATTACK-9 §3(A) |
| **O6** | §0.1: fondamento = DIMOSTRATO o CON-FONTE **verificata**; gli altri passi sono «condizionati a verifica». Marcati nei passi 3c, 4, 5, 6, 7: VAR-T6, DICT-ILIM (H2), DICT-B3, FW-1 con V, S4T-T3 [F1], P1-T4 (Humphreys), VAR-P8(b) «⟸», VAR-P11(e), VAR-T10(4). §10: lista «Citazioni da chiudere» |
| **O7** | §0.1, §3a e §7 (classe (A)): C3-A1 → «(A) condizionato a C3-A1» |
| **O8** | §7, classe (B): Trotter–Kato/splitting solo per V limitato (o relativamente limitato, con ipotesi dichiarate); per V non limitato classe (C) (VAR-T10(5)). §10: «nessuna riga LEDGER: non è un fondamento; richiesta al coordinatore». §11 punto 12 |
| **O9** | §7: VAR-T10 per parti, con (4) Magnus CON-FONTE (Casas Thm 3.4) e (3)(iii) CON-FONTE + V-ex. Classe (B): Magnus solo per generatori limitati o per troncamenti con ‖H_N‖τ < π; «per una PDE quasi vuoto». Classe (C): Stark L8, ∫‖A_I‖ = ∞. §9.3: «Magnus qui è (C)» |
| **O10** | §4: nuova riga «Calcolo»: r_n come residuo di minimi quadrati, non come rapporto di Gram. Costo: precisione di lavoro ≳ log₁₀(1/λ_min) cifre. Contratto: misfit (A) solo con un'inclusione rigorosa, altrimenti (B). §9.5(a): misfit dichiarato (B); verifica (a′) aggiunta allo script, con r_1 come residuo diretto uguale al valore di Gram |
| **O11** | §6, «Fallimenti»: aggiunti C12-P10, OPF-T4, CONV-D1, OPA-T3(a–d), P1-P1(e) FALSO e CONV-B1, ciascuno con l'uscita (`NON-DECISO` o (C)). C12-T1′ citato tra i claim. §10 aggiornato |
| **O12** | §5: nuova tabella «limitata contro Darboux». Darboux è (C); con q stimato dal passo 3c il trasporto è (C), perché la costante di q ↦ W_q non è esplicita. §9.2(a): il senso è solo ID-res, con l'annullatore (L_q + 1)(L_q − k²) nel sottoanello. §9.2(c): Darboux dichiarato caso (C). §11 punto 10 |
| **O13** | §0.3: DM-δ(Y) con norma dichiarata; norme ammesse C^{1,2} o H^m con m ≥ ordine + 1; controesempio in C¹ (nota 2). §1: fallimento «DM-δ in C¹» |

## MINOR

| fix | modifica |
|---|---|
| **O15** | §9.5(c): il caso ε = 1e-3 è dichiarato vacuo (2δ/ρ = 1,43 > 1). Aggiunto il caso (c′) ε = 1e-4 con 2δ/ρ < 1 nello script `ex_L9_L10_dict.py` (nuovo check) |
| **O16** | DICT-R6 (a)–(f) DIMOSTRATO in §0.1, §5 e §10 |
| **O17** | VAR-L2-cor tolto dal passo 3c; resta nel §10 come «non usato» |
| **O18** | §5: ENC-T2 DIMOSTRATO citato tra i claim |
| **O19** | §3b e §10: LAME-3 con ρ ≠ 0, μ ≠ 0, λ + μ ≠ 0, λ + 2μ ≠ 0 |
| **O20** | §3b, §9.1 e §10: H-DIRAC sotto H-DIRAC-1/2, m ≠ 0, base delle matrici fissata |
| **O21** | §6 e §10: «S4T-*» e «OPF-*» sostituiti dagli ID singoli; S4T-L2 e S4T-T3 marcati «mod [F1], condizionato» |
| **O22** | §7: «Bézout su 𝕋» = R4-T5[𝕋] DIMOSTRATO |
| **O23** | P1-T3 spostato dal passo 3a al passo 6 (costo) |
| **O24** | §3a: C3-T4 come ID-ker relativa |
| **O25** | §1 e §2: budget n_max in ingresso; uscita `NON-DECISO`. §0.5: etichetta definita |
| **O26** | §0.5 riscritto con un'unica formulazione (DM3, M3-hol, M2⁺; DM1 solo relativa) |
| **O27** | §0.5: aggiunte `IDENTIFICATA[ID-fam]` e `ID-LIM(n)` |
| **O28** | §9.4: l'esempio è dichiarato banale (interpolazione dei simboli a modi finiti); rinvio a CONV-T6 per il caso non banale |
| **O29** | §2: conteggio solo per LIN, nessuna stima generale per le altre famiglie. §5: costo di Goursat O(M²), indicativo. §7: bound della catena in O(k) |
| **O30** | §0.3, nota 1: DM-δ è un'estensione di PROBLEM v3.1 |
| **O31** | §0.3: il minorante di \|u\| si chiama κ nella specifica, con il rinvio «VAR-P3 lo chiama δ». La rinomina nella riga LEDGER spetta al coordinatore |
| **O32** | §5: riga «Perdita del bound» (C_W² contro cosh², quattro ordini a a√Q = 5); il bound più stretto è una domanda aperta (§11 punto 9) |

## File toccati
- `ALGORITMO_ESTESO.md`: revisione 2.
- `work/S9-ALG/sympy/ex_L9_L10_dict.py`: check (c′) ed (a′) aggiunti; `.out` rigenerato.
- `work/S9-ALG/open_questions.md`: domande nuove 12–15.
- `work/S9-ALG/RECEPIMENTO.md`: questo file.
