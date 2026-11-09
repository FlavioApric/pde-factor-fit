# GATE 8 — chiusura delle prove di Fase 8 (coordinatore, 27/10/2026)
Fonti:
- `research/DEVIL/ATTACK-8.md` (DEVIL-8: FATAL 0, CRITICAL 2, MAJOR 8, MINOR 11);
- `research/CIT-AUDIT/AUDIT-8.md` (55 voci: 28 VERIFICATO, 9 DATI CORRETTI, 18 PARZIALE, 0 CONTENUTO DIVERSO, 0 NON TROVATO);
- `work/CHECK-F8/AUDIT_S8-{SYS,VAR,CONV,ENC,DICT}.md`, `AUDIT_S8-ENC_rev2.md`, `AUDIT_S8-DICT_rev2.md`, `AUDIT_S8-CONV_T2prime.md`, `KA_*`;
- `work/S8-*/{PROOF_PACKAGE,LEDGER_ROWS,RECEPIMENTO}.md`;
- `inbox/central-F6.md`.

## 1. Esito
- **Copertura.** Cinque pacchetti su cinque consegnati, auditati e con i fix recepiti (S8-SYS, S8-VAR, S8-CONV, S8-ENC, S8-DICT).
- **Kill-argument.** Nessun claim del cammino critico è stato ucciso: SYS-EX, H-DIRAC, CONV-T1/T2, ENC-N1′, ENC-P0, DICT-N1 sopravvivono, alcuni con fix.
- **Mini-audit dei claim nati nel recepimento:**
  - CONV-T2′: PASS-con-fix (T2P-1…3, MINOR).
  - ENC rev2: tre MAJOR (ENC2-1, ENC2-4, ENC2-6). ENC-P0(b)^loc ed ENC-P0′-DIC sono FALSI come scritti e veri dopo il fix.
  - DICT rev2: DICT-MAG-NU vale dopo MAG-1 e MAG-2; la promozione di DICT-R6 è legittima.
- **Cammino critico.** ENC-1 → ENC-C1 → ENC-T2 → DICT-R6 è intatto.
- **Verdetto di DEVIL-8.** G★″ sopravvive come impianto (nessun FATAL). Il testo di PROBLEM v3 e SYNTHESIS-2 conteneva però due frasi FALSE (O1, O2), più F5 di DEVIL-6, ritirata (O3). **Sono corrette in questo gate** (§4).

## 2. Gate 8a — strade (proposta di DEVIL-8 §4, adottata)
| strada | decisione | motivo / trigger |
|---|---|---|
| RT-SYS | ATTIVA (ridotta) | aperti Maxwell (Q6), II-T2(b′), Q-S8SYS-1; ogni rivendicazione su ℝ^n richiede la lettura di Oberst 1990/1993 (AUDIT-8: rischio di novità altissimo per SYS-EX/N1/T0; delta solo per Ω arbitrario) |
| RT-IDV | ATTIVA | VAR-T1 in (SF); aperti VAR-Q10, VAR-Q17, VAR-Q18; sorgente di q per ENC e DICT |
| RT-ODE-GAL | ATTIVA, ristretta a C3-Q2 | C3-Q2 chiuso per L monico in ∂_t; resta il caso generale (VAR-C3Q2-open, VAR-Q12/13) |
| RT-NA | PARCHEGGIATA | quasi tutto CON-FONTE (Wei–Norman, Casas, Pazy); trigger VAR-Q8, Q11, Q18 |
| RT-ENC | PARCHEGGIATA come strada | nessun potere identificativo (O7); i lemmi ENC-1, C1, T2, P0(b)^cl, A9 passano a RT-DICT e RT-IDV; trigger ENC-Q4, ENC-Q10 |
| RT-DICT | ATTIVA | strato algoritmico della Fase 9 (R6, ILIM, RANGO); aperti DICT-Q3, Q4, ILIM-Hs |
| RT-CONV | ATTIVA | contratto CONV-T7 per ALGORITMO_ESTESO, con Magnus condizionato (O4) |
| RT-5 (→ SYS); RIGID, STOKES (→ IDV); CONV-BORDO | PARCHEGGIATE | mai toccate in F8 (O18) |
| Mori–Zwanzig, RT-R2a (→ CONV) | ELIMINATE come strade | criteri FALSI (CONV-MZ3-F, CONV-R1-F); restano i lemmi |
| POLE, gamblets (→ ENC) | ELIMINATE | POLE-N è negativo; gamblets solo CON-FONTE (GAM-O1) |
| Faddeev; MICRO/FW; MPUM; NS-EQUIV, NS-GALDAR; NS-EXPALG; F4-ALG | FUSE | rispettivamente in FAD-1; FW-1; SYS-R1 e VAR-VMPUM; RT-ENC (parcheggiata; NS-EQ-Ω resta lemma); RT-DICT; N1(v)-ALG |
| PAINLEVÉ | STRUMENTO | DICT-R4 |

## 3. Gate 8b — struttura di Gate 3 e G★′-NL
**Gate 3: revisione limitata** (DEVIL-8 §5). È registrata qui e va applicata in NOTAZIONE v6 e nel testo di Gate 3 durante la Fase 10 (S10-INT):
1. **Anello dei coefficienti.** Con coefficienti in un campo chiuso per derivazione, l'oggetto canonico (D·u, u) è vacuo (VAR-N1: 𝒦[∂]/Ann(u) ≅ 𝒦u per ogni u senza zeri). Gate 3 va enunciato con l'anello specificato: ℂ[∂]; ℂ(x)[∂] o Weyl A_n; oppure una classe parametrica fissata. Per le classi strutturate L7–L9 l'oggetto canonico include la mappa residuo ρ_u.
2. **Sistemi.** "Componente = fattore" richiede Ext¹(N, 𝒜) = 0. SYS-S1-C è FALSO su un dominio semplicemente connesso. Lo scalare C12-T1′ (n = 2, N di lunghezza finita) è invariato.
3. Nessun'altra parte di Gate 3 è toccata.

**G★′-NL: invariato.** Nessun claim di F8 lo contraddice: DICT-NS e CONV-B1–B3 sono compatibili.

## 4. Correzioni applicate in questo gate (dal coordinatore)
- **O1, O2 (CRITICAL).** PROBLEM v3 → v3.1, punti 4 e 6: tolti ENC-N1 ("cieco ⟺ identificabilità congiunta", FALSO) e "le eccezioni quadratiche cambiano il tempo" (FALSO). Al loro posto ENC-N1′ come lemma di riduzione, ENC-P0(b)/(b)^cl, e la forma esistenziale "esiste un rappresentante con θ = id ⟺ α ≡ 0". SYNTHESIS-2 corretta nei punti §0.1 (encoder), tabella ENC-P0/ENC-N1, tabella encoder (puntuale + gauge) e §5.4, con una nota in testa. Backup: `PROBLEM_v3_preGate8_backup.md`, `research/SYNTHESIS-2_preGate8_backup.md`.
- **O3 (MAJOR).** SYNTHESIS-2, riga VAR-P9/T10: F5 di DEVIL-6 ritirata. In H = −∂² + x² la rottura a cos t = 0 esiste.

## 5. Correzioni rinviate (girate alle sessioni o alle fasi successive)
- **Alle sessioni S8-\*** (recepimento prima della promozione delle righe condizionate, O10):
  - S8-ENC: ENC2-1…6.
  - S8-DICT: MAG-1…5, più R6(f) da citare via N1(ii) e Teorema A (O19).
  - S8-CONV: T2P-1…3 e contratto CONV-T7 con Magnus condizionato (O4).
  - S8-SYS: β(1) ≠ 0 in SYS-S1-C (O21) e riassunto di SYS-N3 con div(ρ²B) = 0 (O15).
  - S8-VAR: VAR-P3 non è un certificato di robustezza (O8); audit di VAR-L2-cor.
  - A tutte: correzioni bibliografiche di AUDIT-8 §5.
- **NOTAZIONE v6 (Fase 10, S10-INT):**
  - etichette ID-ann, ID-ker, ID-res, ID-fam, ID-lim e ipotesi (H-ex) (O5);
  - (E2) con c ∈ C(I) e (E2₀) (O12);
  - (ID) → (H-ID) (O13);
  - H-DIRAC sotto H-DIRAC-1, 2 (O11);
  - oscillatore normalizzato H = −∂² + x² (O3);
  - aggiornamento della §0.2(b′) di SYNTHESIS-2: "fuori dalle fasce di silenzio, in (SF)" (O17).
- **Prima del Gate 9:** CIT su Oberst 1990/1993, Isakov 1993 (al posto di Saut–Scheurer per VAR-L2), Andrianov–Sokolov 2003 / Sokolov 2008 (O6). In G★″ il contributo dichiarato è la composizione L6–L10 più le negative nuove, non i singoli lemmi positivi.
- **Fase 9:** identificazione dichiarata in DM3; in DM2 solo i moduli di VAR-P3 e la negativa DICT-N1(ii); robustezza in DM2 come domanda (O8). S-O1 da riallineare a SYS-S1-C (O14).

## 6. LEDGER
Le righe di Fase 8 entrano in `claims/LEDGER.md` (sezione «Fase 8») con gli stati proposti da DEVIL-8 §6. La regola è: solo verso il basso; le righe "DIMOSTRATO dopo fix rev2" restano PROVA SCRITTA finché il recepimento non è verificato.

---
## ESITO DEL GATE 8 (27/10/2026) — approvazione automatica per delega dell'utente
Gate 8a e 8b sono approvati come al §2 e al §3, per la delega dell'utente del 26/10, **registrati e revocabili**. L'utente ha chiesto esplicitamente, il 27/10: «scrivi GATE8.md (8a secondo la proposta di DEVIL-8, 8b con revisione limitata di Gate 3), correggi i 2 CRITICAL in PROBLEM e SYNTHESIS-2, poi gira i fix alle sessioni S8-* e scrivi le righe LEDGER».
