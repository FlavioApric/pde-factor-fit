# CHIUSURA DELLA FASE 10 (coordinatore, 27/10/2026)

## 1. Cosa è stato fatto
- **Gate 9** approvato (`GATE9.md`): ALGORITMO_ESTESO rev. 2 + errata di Fase 10.
- **Revisione limitata di Gate 3** applicata (GATE3, PROBLEM, SYNTHESIS-2 §0.2(b′)); NOTAZIONE v7.
- **Problemi aperti di tutte le fasi** passati in rassegna da S10-OPEN-A (fasi 1–4), S10-OPEN-B (fase 5) e S10-OPEN-C (fase 8). Ogni pacchetto ha avuto un audit indipendente, e dove servivano fix anche un secondo giro.
- **[COL]**: (COL-ii) dimostrata (S10-COL), quindi S10A-T3 non dipende più dalla fonte.
- **Verifiche di citazione** CIT-AUDIT-9, AUDIT-COL e AUDIT-GTU.
- **Lean**: 37 voci, di cui 27 fedeli, 7 più deboli e 3 diverse, nessuna vacua. Gli 85 `#print axioms` usano solo gli assiomi standard.
- **Esempi da manuale** (Dirac libero, oscillatore armonico, Pöschl–Teller, calore frazionario, Maxwell nel vuoto): 80/80 PASS, più tre argomenti nuovi DIMOSTRATO.
- **Tutte le righe** sono in `claims/LEDGER.md`, sezione «Fase 10» (F10-A, B, B2, C, C2, COL, GTU, G9, LEAN, INT, EX). Lì prevalgono le righe con lo stesso ID nelle sezioni precedenti.

## 2. Esiti principali
- **Nuovi FALSI:**
  - P1-Q6 come scritto (controesempio reazione–diffusione);
  - P2-Q1 come enunciato universale (domini con buchi);
  - estensione di OPF5B-T1 ai non convessi (S10B-C1);
  - Q-S8SYS-4;
  - P11(e) con B solo continuo.
- **Chiusi (DIMOSTRATO), tra gli altri:**
  - P1-Q6 nella forma corretta;
  - P1-Q7 sotto (Dil);
  - densità sui lipschitziani semplicemente connessi (mod F1, F2);
  - C12-P7;
  - C3-Q1 per modello;
  - [F4⁻], [Hm], OPF5C-T5;
  - OPA-Q1 (mod [F1]);
  - VAR-P11(e), VAR-L2-cor;
  - VAR-Q10;
  - Maxwell Q6;
  - II-T2(b′)-CRIT;
  - Q-S8SYS-1 (a, b);
  - ENC-T2(c′)-P, ENC-Q4-S, ENC-Q10-D;
  - DICT-ILIM-Hs, DICT-Q4-C;
  - DM-δ minimax Θ(ε^{1/3}).

## 3. Problemi che restano APERTI (onestamente)
Non sono stati chiusi e non vengono dichiarati chiusi. Per ciascuno è registrato nel LEDGER quanto è provato.

**Con riduzione o condizione provata:**
| ID | cosa resta |
|---|---|
| P1-Q7 | algebre con (H) senza dilatazione pesata (Dil) |
| C12-Q2 = OPF-Q2 | terne con ≥ 2 coppie Π_iΠ_j non compatte, fuori dai trasporti reali |
| OPF5C-Q1 | caso graduato |
| OPR2-Q3 | realizzabilità degli atomi (caratterizzazione S10B-P10) |
| OPR2-Q2′ | condizione sufficiente: (L-v) a ogni vertice |
| INT-Q1 | equivalente a (R), mod S4ID-P8, [GT-u_m], (WP) |
| [GT-u₀] | limitatezza delle costanti di Hölder di GT (5.20)–(5.21) e della ε del disaccoppiamento per k₀ in compatti |
| [GT-u_m] | giustificazione della derivazione in GT Rem. 5.5 (Deift–Zhou CMP 165, non letto) |

**Senza riduzione:**
- P2-Q1-NL: domini non lipschitziani.
- P2-Q1-COD: codimensione esatta per P generale.
- C12-Q1: chiusura della somma per (τ−ξ²)(τ+cξ).
- VAR-Q18: moltiplicazioni.
- VAR-Q17(b), riformulato.
- VAR-P12(d) nel caso generale.
- VAR-C3Q2-open: caso non monico; VAR-Q13.
- SYS-DIRAC-POL a tempi complessi.
- ENC-Q4: lettura DM3.
- ENC-Q10: residuo con V reale, riformulato.
- DICT-U3d-v: ottimalità.
- DICT-Q3(c), riformulato come divisione C^∞.
- S10B-V9: N = 5 non riprodotto, N = 6 non eseguito.
- S10B-P3: "aperta e densa" dopo il fix P3-c (la densità è DIMOSTRATO).

**Condizionali su fonti** (CON-FONTE non lette per intero):
- Oberst 1993, letto solo nell'abstract;
- [F1] Oleinik ⟺ Kružkov;
- Malgrange 1966;
- Amitsur 1965 / Brešar–Šemrl 1999;
- Björk;
- (WP) esistenza globale in 𝒮.

## 4. Stato delle sessioni
Le sessioni di ricerca sono chiuse; S9-ALG ha ancora attività in background e va archiviata dalla barra laterale. Il grafo è in `graphify-out/`.

## 5. Aggiornamento del 28/10/2026: triage indipendente e chiusure
Un triage indipendente (`work/CHECK-F10/TRIAGE_APERTI.md`) ha classificato ogni voce del §3 in tre classi: chiudibile ora, problema di ricerca, oppure richiede fonti non disponibili offline. Gli abbozzi della prima classe sono stati auditati da un revisore separato (`work/CHECK-F10/AUDIT_TRIAGE.md`). Le righe sono in LEDGER «F10-TRIAGE».

**Chiusi o ridotti ora:**
- S10B-P3 «aperta e densa»: DIMOSTRATO (forma P3-c).
- S10B-V9: N = 5 e δ₆(12) = 7 DIMOSTRATO computer-assisted mod (Nov)/(Nov′); δ₆(11) = 8 PROVA SCRITTA.
- P1-Q7: il candidato (x³+x)∂, ∂ è DIMOSTRATO; il caso generale resta APERTO.
- P2-Q1-NL: il caso modello Δ, m ≥ 1 con L^{1,2} ⊂ L² è DIMOSTRATO; il caso generale resta APERTO.
- SYS-DIRAC-POL: il caso t, m reali è DIMOSTRATO; i tempi complessi restano APERTO.
- Condizioni su fonti rimosse: Amitsur / Brešar–Šemrl (sostituito da DICT-LOCDEP) e Björk (sostituito per (a′) da VAR-C3Q2-R).

**Restano APERTI, con la classe del triage:**
- *Problemi di ricerca senza strada nota:* C12-Q2, OPF5C-Q1 (N generale), OPR2-Q3, OPR2-Q2′, INT-Q1, P2-Q1-COD, C12-Q1, VAR-Q18, VAR-P12(d), VAR-C3Q2-open / VAR-Q13, ENC-Q4, DICT-Q3(c), AM-CL, il caso generale di P1-Q7 e di P2-Q1-NL, SYS-DIRAC-POL a tempi complessi.
- *Bloccati su fonti non disponibili offline* (il progetto vieta di scaricare file): [GT-u₀], [GT-u_m], VAR-Q17(b), ENC-Q10, DICT-U3d-v, Malgrange 1966, (WP), Oberst 1993 (solo per la novità: non è portante).
- *[F1] Oleinik ⟺ Kružkov:* il triage dà un piano (viscosità evanescente su Cole–Hopf), ma senza una prova scritta né auditata; resta CON-FONTE.

Il triage indipendente conferma che nessuna di queste voci è chiudibile con un'azione limitata e con le risorse disponibili. Chiuderle richiede ricerca nuova o la lettura di testi da procurare: è il punto di partenza di una fase successiva.

## 6. Chiusura della parte analitica (28/10/2026)
Su decisione dell'utente la parte analitica del progetto è chiusa. Tutte le voci ancora APERTE o CONDIZIONALI di §3, §5 e di REPORT_FINALE §6.3 sono raccolte in **PROBLEMI_APERTI.md**, con classe, risultato parziale e che cosa servirebbe. Nessuna è portante per i risultati centrali: le dipendenze esistenti ([F1], [L-loc], [GT-u], [F4⁻], Malgrange) sono già marcate «mod …» nel REPORT. Gli stati nel LEDGER restano invariati.
