# PLAN — S-C3 · Identificazione dell'operatore dal nucleo su Ω limitato ⊂ ℝ (Fase 3)
Data 25/10/2026. Scheda: SESSIONS.md §S-C3. Vincoli Gate 1: H0 = ℝ, H1 = H^m(Ω), Ω = I×(a,b) limitato (o aperto connesso limitato ⊂ ℝ²). Notazione: NOTAZIONE.md v2 (R = ℂ[τ,ξ], ∂_t ↔ τ, ∂_x ↔ ξ).
Cartella vuota all'avvio (nessun lavoro da riprendere); inbox/S-C3.md vuota.

## 1. Domande / enunciati (ID degli appunti, item del piano)
Q1 (G9, O3, C3.2/P4.3, appunti D2, E2) — Riportare R4-T5 da 𝕋 a Ω limitato senza modi di Fourier. Strategia: criterio **intrinseco** via struttura degli ideali di ℂ[τ,ξ] che contengono P (I = gcd(I)·J con V(J) finito) e caratterizzazione degli esponenziali-polinomi (EP) come le distribuzioni con orbita R·w di dimensione finita. Bersaglio [C3-T1]: Ann(u) = (P) ⟺ per ogni fattore irriducibile P_i, (P/P_i)(∂)u ∉ EP(Ω). Vale anche per P NON ridotto (risponde a R4-Q2) e per P ridotto equivale a V(Ann u) = V(P).
Q2 (O3) — Mostrare perché la trasposizione ingenua fallisce: controesempio con insieme spettrale infinito (serie di Fourier di un'estensione) ma Ann(u) 0-dimensionale [C3-C1]; i dati EP non identificano mai nell'anello intero [C3-C2]. Versione con "unicità dello sviluppo" come ipotesi esplicita [C3-P4] (ponte con R4-T5).
Q3 (O7) — Fissare il **modello di dato** [C3-D1]: M1 formula EP con M modi; M2 jet in un punto di u analitica; M3 u ∈ H^m(Ω) noto esattamente. Per ciascuno: cosa si può certificare, con quale costo. Bersagli: [C3-T2] (M1: criterio di rango, soglia di Bézout, sua ottimalità, complessità), [C3-T3] (M2: jet di ordine n+d−1 basta, generalizza R4-T2), [C3-P1] (impossibilità: nessuna famiglia finita di dati certifica Ann(u) = (P)), [C3-P2] (semi-decisione relativa a una classe finita).
Q4 (ladder L0, L2, L3) — Corollari: L0 = R4-T1; L2 u_t = a(∂_x)u: identifica ⟺ u ∉ EP, e con dati EP ⟺ ≥ n+1 frequenze ξ distinte (R4-T4 su ℝ) [C3-T4]; L3 onda (d'Alembert: f, g ∉ EP), KG, trave [C3-T5].
Q5 (RT-R7c) — Riconciliare l'ostruzione da simmetria con [C3-T1] [C3-P3].
Q6 (O4) — Ridimensionare la novità con citazioni esatte (Oberst 1990, Nullstellensatz, Mourrain 2018, He–Zhao–Zhong Thm 3.2 solo sufficiente, Scholl Cor. 1 e Prop. 10 solo ordine ≥ 2, Pierce 1979 = autovalori sì, coefficienti no, Stanhope–Rubin–Swigon).
Q7 (S-II) — Lemma "vettore ciclico = jet": per P monico in τ, Ann(u) = (P) ⟺ u, ∂_t u, …, ∂_t^{m−1}u sono ℂ[∂_x]-linearmente indipendenti [C3-T1(d)]; per u EP, R·u ≅ R/Ann(u) e la Hankel del jet ha nucleo Ann(u).
L4 (coeff. polinomiali): solo stato dell'arte con fonti (R4-T7, Scholl Prop. 10) + problema aperto; non sul cammino critico.

## 2. Skill, in ordine d'uso
1. skills-local/session-protocol (caricata per prima, letta per intero).
2. skills-local/claim-lifecycle (ciclo di ogni enunciato; righe LEDGER).
3. _vendor/Auto-claude-code-research-in-sleep/skills/proof-writer (struttura del PROOF_PACKAGE: claim, assunzioni, triage, mappa delle dipendenze, prova, rischi).
4. _vendor/math-skill (modo proof: esplorazione separata dalla prova, controesempi presto) + references/proof-playbook.md.
5. _vendor/scientific-agent-skills/skills/sympy (verifiche in work/C3/sympy/, `.venv\Scripts\python.exe -I`).
6. Revisione: proof-checker tramite S-CHECK (DOMANDA in inbox/S-CHECK.md con solo enunciato+ipotesi+prova di C3-T1 e lemmi).
7. _vendor/.../kill-argument su C3-T1 (cammino critico): due subagenti Claude freschi senza contesto (attacco ~200 parole, poi arbitrato per punti), al posto di Codex per decisione dell'utente.
Nessuno script _vendor eseguito.

## 3. Fonti
research/R4 (REPORT, open_questions Q2, Q4), R2 (T1, T2, T6, T7: Oberst, Malgrange, Hörmander ICASV 7.6), R7 §5.1 (R7-L4), R8, CIT-AUDIT/AUDIT.md (correzioni HZZ, Pierce, Scholl). Classici: Fulton, *Algebraic Curves* (Ch. 1 §6 Prop. 2; Bézout Ch. 5); Hörmander ALPDO I Thm 3.1.4'; Nullstellensatz.

## 4. Contatti
- S-C1C2: AVVISO/TABELLA — il criterio vale su ogni aperto connesso (non serve la convessità), mentre la scomposizione per fattori (R2-T2) usa l'iniettività sui convessi; condivisione di Lemma EP e della struttura I = G·J.
- S-II: TABELLA/DOMANDA — vettore ciclico = t-jet (u, u_t, …, ∂_t^{m−1}u) su ℂ[∂_x]; Hankel del jet.
- S-P4: AVVISO — input per la mappa di identificazione (iniettività 𝓛 → End(R·u)).
- S-CHECK: DOMANDA (audit di C3-T1 + L2, L3).
- central: PLAN-READY, righe LEDGER proposte, DONE.

## 5. Criterio di "fatto"
C3-T1 scritto con prova completa, verificato su esempi SymPy, inviato a S-CHECK, passato per kill-argument; controesempi alle ipotesi (C3-C1, C3-C2, C3-C3, P non ridotto, simmetria); modello di dato fissato con complessità esplicita (C3-A1); righe LEDGER proposte; stato onesto (DIMOSTRATO solo se proof-checker superato, altrimenti "prova scritta, in attesa").

## Ripresa 25/10 sera (dopo DONE S-CHECK-2A)
Input letti: RIPRESA.md (ultimo AGGIORNAMENTO), PROTOCOLLO.md, skills-local/session-protocol e claim-lifecycle (ricaricate), PROOF_PACKAGE.md, inbox/S-C3.md (RISPOSTA S-CHECK-2A), work/CHECK/AUDIT_C3-T1.md.
Passi:
1. Recepire nel PROOF_PACKAGE i fix MINOR dell'audit, ciascuno marcato con il suo id: F-1 (caso deg_τ P_i = 0 in (F) + "quindi" V(P_i) ⊆ V(Ann w)), L2-1 (Fulton: numero non verificabile qui → derivazione autosufficiente via eliminazione/Gauss, citazione tenuta solo come "cfr."), L3-1 (prova breve φ = χ⊗Φ + ∂_tψ al posto della sola citazione di Hörmander 3.1.4′ + nota sul dominio a U), L3-2 (passo 3 via L3(b) su E_{Q_y} − E_{Q_0} + fascio, Hörmander 2.2.1), L3-3 (ψ biortogonali), T1-1 (direzione ⇐ di (e)), T6-1 (P ≠ 0, G_u ∼, k = 0 ∈ S_i).
2. Compilare §9.1 (verdetti PASS-con-fix, stati DIMOSTRATO per C3-L2, L3, T1, T6; portata: caratterizzazione, non decidibilità, C3-Q1 APERTO) e aggiornare le righe di stato in §0, §3, §4, §9, §11.
3. Rispondere alla DOMANDA di S-II (modello di dato) in inbox/S-II.md.
4. TABELLA LEDGER in inbox/central.md per gli altri claim (C3-L1, T2, T3, T4, T5, P1–P5, C1, C2, A1, D1) con stato onesto; raccomandazioni per S-CHECK. Poi DONE S-C3.
Criterio di fatto: tutti i 7 fix presenti con id; §9.1 compilato; risposta a S-II; tabella + DONE in central.

## Ripresa 2 — audit 2D (25/10/2026, sera)
Input letti: RIPRESA.md (ultimo AGGIORNAMENTO: DONE S-CHECK-2D, lancio "S-C3 ripresa 2"), skills-local/session-protocol (per prima) e claim-lifecycle (ricaricate), questo PLAN, PROOF_PACKAGE.md, inbox/S-C3.md (RISPOSTA S-CHECK-2D), work/CHECK/AUDIT_C3-secondari.md, coda di inbox/central.md (TABELLA S-CHECK-2D già proposta al LEDGER).
Passi:
1. Recepire nel PROOF_PACKAGE i fix dell'audit 2D, ciascuno marcato [fix <id>]:
   - C3-P1 → **P1-1**: divisione in C3-P1[M2] (lemma P1-M2, prova autosufficiente dell'audit, Ω connesso qualsiasi, DIMOSTRATO) e C3-P1[gen] (funzionali continui qualsiasi, Ω convesso: CON-FONTE da verificare; nessun numero di teorema affermato, in attesa di CIT-AUDIT-2); **P1-2** (riga Ann(v) ⊋ (P)); **P1-3** (convessità necessaria: controesempio sul dominio a U).
   - C3-T4 → **T4-1** (z_k distinti, q_k ≠ 0; deg a ≤ n essenziale).
   - C3-T3 → **T3-1** (prova di (iii) per ogni d, forma debole e forte, dall'audit) + nota T3-2.
   - C3-T2 → **T2-1** (Q costante; omogeneizzate senza componenti comuni), **T2-2** (Fulton §5.3 da confermare, stima affine), **T2-3** ((d) = "non migliorabile in generale").
   - C3-T5 → **T5-1** (c ∈ ℝ∖{0}; d'Alembert come ipotesi), **T5-2** (etichette w_1, w_2), **T5-3** (prova globale di F(x−ct) ∈ EP ⇒ F ∈ EP).
2. Aggiornare §0, la riga di stato in testa, i titoli-stato dei claim, §9 (nuova §9.3 "Esito S-CHECK-2D" con tabella degli stati), §10 (C3-Q5 collegato a P1[gen]), §11.
3. inbox/central.md: AVVISO di recepimento (le righe LEDGER le ha già proposte S-CHECK-2D; nessuna modifica di stato rispetto a quelle) e "DONE S-C3 (ripresa 2)".
Vincoli: scrivo solo in work/C3/ e inbox/; nessuno script _vendor; nessun numero di teorema inventato (Malgrange/Hörmander, Fulton restano "da verificare" finché CIT-AUDIT-2 non risponde).
Criterio di fatto: 11 fix presenti con marcatura [fix id]; §0, §9.3, tabella stati aggiornati; DONE in central.
