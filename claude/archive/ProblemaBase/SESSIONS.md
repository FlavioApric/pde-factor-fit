# SESSIONS.md — roster della Fase 3 (v1, 25/10/2026, da approvare al Gate 2)

Obiettivo di Fase 3 (piano): dimostrare **G★′** (PROBLEM.md) lungo la scala L0 → L4, con ogni claim nel `claims/LEDGER.md`.
Regole comuni a tutte le sessioni: caricare per prima `skills-local/session-protocol`; ogni enunciato passa da `skills-local/claim-lifecycle`; cartella `work/<ID>/`; prodotto `PROOF_PACKAGE.md` + `sympy/`; chiusura `DONE <ID>` in `inbox/central.md`. Decisioni del Gate 1: H0 = ℝ, H1 = H^m(Ω) con Ω limitato, componente = fattore, coeff. variabili in classe a dimensione finita.
Profili (piano Fase 2): sessioni analitico-geometriche → catena proof-heavy (proof-writer, proof-checker, kill-argument); sessioni spazio/base → catena math-heavy (math-skill, sympy, kernel-catalog-entry).

## Ordine e dipendenze
```
            S-C3 (identificazione su ℝ) ─────────────────────┐
              │ (Z(u), Ann(u))                               ▼
S-C1 ⇔ S-C2/C4 (spazio dal catalogo; fattori) ──► S-P1 (E_int) ──► S-P2 ∥ S-P3 ──► S-P4 ──► G★′
              ▲                                       ▲
              └──────────── S-II (compagna / modulo) ──┘        S-TROP (scout, O1) · S-CHECK (revisore)
```
Prima ondata (in parallelo, nessuna dipende da un'altra): **S-C3, S-C1⇔S-C2/C4, S-II, S-TROP, S-CHECK**. Seconda ondata: S-P1. Terza: S-P2, S-P3. Quarta: S-P4.

## Schede

### S-C1 ⇔ S-C2/C4 (coppia accoppiata) — spazio dal catalogo e scomposizione per fattori
- **Compito.** (C2/C4) Teorema di scomposizione per fattori su Ω limitato ⊂ ℝ in H^m(Ω): u = Σ_j u_j, u_j ∈ ker P_j^{m_j}, ambiguità = ker(P_i,P_j); proiettori costruttivi (P_2u ∈ ker P_1); LCLM a coeff. variabili. Dire esplicitamente (G8, obiezione O1) che per evoluzioni del 1° ordine lo strato fattori è banale. (C1) Funtore C1.0: catalogo → (𝓗_𝒟, Gram, nucleo riproducente = Green, duali); limiti di Riesz dall'angolo di Friedrichs; base di Rosenbloom–Widder (RT-R3a) e suoi analoghi.
- **Ladder.** L0 → L3 (coeff. costanti), poi L4 (polinomiali).
- **Skill.** session-protocol · kernel-catalog-entry · math-skill (proof/solver) · sympy · proof-writer · claim-lifecycle.
- **Input.** research/R2, R3, R1, PR-C2a–e, PR-C2d (REPORT, cards); SYNTHESIS §2 righe C1, C2, C4.
- **Output.** work/C1C2/PROOF_PACKAGE.md, work/C1C2/gram.md (file condiviso della coppia, piano v3), work/C1C2/CATALOGO_v2.md.
- **Contatti.** S-C3 (Z(u) e dominio ℝ), S-II (proiettori spettrali della compagna = componenti), S-P1 (definizione di E_int per fattore).
- **Fatto quando.** Teorema di scomposizione su ℝ/H^m(Ω) DIMOSTRATO (proof-checker) + funtore C1.0 dimostrato per i casi ★ + SymPy su calore, trave, onda, avvezione–diffusione.

### S-C3 — identificazione dell'operatore dal nucleo (su ℝ)
- **Compito.** Riportare R4-T4/T5 da 𝕋 a Ω limitato ⊂ ℝ (G9, obiezione O3): Ann(u) = (P) ⟺ V(Ann u) = V(P), soglia di Bézout, con la rappresentazione di Ehrenpreis al posto dei modi di Fourier. Fissare il **modello di dato** (formula / jet in un punto / u ∈ H^m(Ω): obiezione O7) e la complessità. Riconciliare con l'ostruzione da simmetria (RT-R7c) e con P non ridotto (R4-Q2). Ridimensionare la novità (O4) con citazioni esatte (Scholl, He–Zhao–Zhong solo condizione sufficiente, Mourrain, Oberst).
- **Ladder.** L0, L2, L3; L4 nella classe polinomiale.
- **Skill.** session-protocol · proof-writer · math-skill (proof) · sympy · claim-lifecycle · kill-argument (cammino critico).
- **Input.** research/R4, R2, R7 §5.1, R8, CIT-AUDIT/AUDIT.md.
- **Output.** work/C3/PROOF_PACKAGE.md.
- **Contatti.** S-C1⇔S-C2/C4, S-II (vettore ciclico = jet), S-P4.
- **Fatto quando.** Teorema di identificabilità su ℝ DIMOSTRATO, con controesempi alle ipotesi e complessità esplicita.

### S-II — matrice/compagna/modulo e calcolo funzionale
- **Compito.** Struttura canonica = via (b) + modulo R[s]/(P) o D/DL (R6). Proiettori spettrali obliqui P_a come componenti (F1 corretta), rami su V(P) e discriminante, equazioni del 2° ordine in t trattate modo per modo (Wei–Norman su gl_m, PR-C2b P4). Decidere su RT-R6a (⋆-prodotto).
- **Skill.** session-protocol · math-skill (proof) · formula-derivation (`_vendor/.../formula-derivation`) · sympy · claim-lifecycle.
- **Input.** research/R6, R7 §2–3, R5 §4.
- **Output.** work/II/PROOF_PACKAGE.md + decisione di struttura per il Gate 3.
- **Contatti.** S-C1⇔S-C2/C4, S-C3, S-P1.
- **Fatto quando.** Tabella invarianti dimostrata e decisione di struttura motivata.

### S-P1 — struttura di E_int (seconda ondata)
- **Compito.** Definizione canonica di E_int per fattore e per quadro (R5-D1, NOTAZIONE v2); formula chiusa nel caso commutante e complessità O(N)/O(N²) con dimostrazione completa (rifare R5-T2 con claim-lifecycle); classificazione per algebra di Lie (finita risolubile / finita / infinita) con l'impossibilità nel caso infinito come obiettivo (R5-Q5); E_int dal bordo (PR-C2d).
- **Skill.** session-protocol · proof-writer · formula-derivation · sympy · claim-lifecycle · kill-argument.
- **Input.** research/R5, PR-C2b P3–P5, PR-C2d §4, R7 §4, work/C1C2, work/II.
- **Output.** work/P1/PROOF_PACKAGE.md. **Contatti.** S-P2, S-P3, S-TROP.

### S-P2 — regolarizzazione (terza ondata)
- **Compito.** Formalizzare R1-T6/T7/P8/P9 (B8 falso per E_int^⊥, ℓ¹ sull'ambiguità interna, nessun encoder lineare); valutare RT-R1a (MCA, cluster coherence < 1/2 su una coppia della scala).
- **Skill.** session-protocol · math-skill · sympy · claim-lifecycle. **Input.** research/R1, work/C1C2/gram.md. **Output.** work/P2/PROOF_PACKAGE.md. **Contatti.** S-P1, S-C1.

### S-P3 — duali e perturbazioni (terza ondata)
- **Compito.** Dyson/Kato con ipotesi verificabili (R5-T9), regole di selezione, elemento di matrice al 1° ordine (PR-C2d §4), duali biortogonali (R6-T3, Rosenbloom–Widder); valutare RT-S2a (Faddeev).
- **Skill.** session-protocol · proof-writer · sympy · claim-lifecycle. **Input.** research/R5, R6, PR-C2b P6, PR-C2d, SCOUT-2. **Output.** work/P3/PROOF_PACKAGE.md. **Contatti.** S-P1, S-II.

### S-P4 — Â⁻¹ e mappa di identificazione (quarta ondata)
- **Compito.** Sintesi spettrale su Z(u), risolvente = Padé, iniettività della restrizione 𝓛 → End Z(u) (R4-T3/T8, RT-R4a) su ℝ.
- **Skill.** session-protocol · proof-writer · sympy · claim-lifecycle. **Input.** work/C3, work/II, research/R4. **Output.** work/P4/PROOF_PACKAGE.md. **Contatti.** S-C3.

### S-TROP — scout della lettura per termine (obiezione O1)
- **Compito.** route-scout su [TROP-L2] (research/SCOUT-1/REPORT.md, Addendum): limiti di scala verso le forme iniziali estreme e stima ‖E_int‖/‖u‖ = O(ε^γ) per avvezione–diffusione e Klein–Gordon. Criterio di eliminazione già fissato: se la stima non si dimostra o contano solo i vertici estremi, merge in RT-2.
- **Skill.** session-protocol · route-scout · math-skill (proof) · sympy · novelty-check.
- **Output.** work/SCOUT-TROP/VERDETTO.md. **Contatti.** S-P1, S-C1⇔S-C2/C4.

### S-CHECK — revisore indipendente (proof-checker)
- **Compito.** Fare da "secondo revisore" di claim-lifecycle per le altre sessioni: riceve in inbox/S-CHECK.md enunciato + ipotesi + prova (senza il resto del contesto) e restituisce l'audit secondo `proof-checker`. Per primi: R2-T3, R4-T5, R5-T2 (priorità del Gate 1). Declassa a V-ex i claim verificati solo su esempi.
- **Skill.** session-protocol · proof-checker · scientific-critical-thinking · sympy.
- **Output.** work/CHECK/AUDIT_<claim>.md. **Contatti.** tutte le sessioni.

## Fuori dalla Fase 3 (piano)
Fase 4 (non lineare: RT-R7a, RT-R7b, Cole–Hopf, IST) dopo il Gate 3; Fase 5 (formalize-claim, Lean) dopo; Problema 1, Problema 2 e Idea I solo dopo la Fase 5. Uno scout di orizzonte resta attivo in Fase 3 (piano v4): S-TROP ne fa le veci.

---
# Roster della Fase 4 (v1, approvato al Gate 4a il 26/10/2026)
Obiettivo: G★′-NL (PROBLEM.md). Regole comuni: come in Fase 3 (session-protocol per primo, claim-lifecycle, `work/<ID>/`, PROOF_PACKAGE.md + sympy/, CHECK_REQUEST.md autosufficiente per S-CHECK, `DONE <ID>` in inbox/central.md) più: **predizione e criterio d'uscita scritti nel PLAN prima di iniziare** (DEVIL-4 O6); definizione di E_int = A9 di NOTAZIONE v3, senza confonderla con E^NL/E^trop (DEVIL-4 O1); dati su Ω limitato o limite dichiarato esplicitamente (O4). Gli scout di Fase 4 (research/F4-*) sono chiusi: le loro NOTE sono input.
Grafo: S4-TERM ↔ S4-INTEG (lemmi di trasporto usati come strumenti); S4-ID ↔ S4-INTEG (INT-T1, ALG-T1, MODREL-T1); S4-TERM ↔ S4-ID (la stessa u: chi identifica e chi scompone); tutti → S-CHECK, → central.

### S4-TERM (prioritaria) — E_int non lineare nel senso A9
- **Compito.** Punto 1 di G★′-NL. Burgers: E_int^add e E^mult prima e oltre lo shock (flusso del solo uu_x = soluzione entropica, Kružkov); ordine in t, dipendenza da ε e ν; poi KdV–Burgers, Fisher–KPP. Strumenti: splitting (Brezis–Pazy, Lie–Trotter non lineare), forma normale NF-1 (F4-HOR), F4L-P2 (Dyson sul sollevato), LIN-Q3 (F4-LIN), lemmi lineari P1-T2, P1-T4/T5, P3-T1.
- **Criterio d'uscita.** Una stima di ordine esplicito (atteso t²) valida oltre lo shock, oppure un teorema negativo registrato.
- **Skill.** session-protocol · proof-writer · formula-derivation · math-skill · sympy · claim-lifecycle · kill-argument.
- **Input.** research/F4-HOR, F4-LIFT, F4-LIN (NOTE), research/DEVIL/ATTACK-4.md (+ sympy4/e_int_a9.py), work/P1, work/P3. **Output.** work/S4-TERM/.

### S4-ID — identificazione relativa a un dizionario
- **Compito.** Punto 2 di G★′-NL. Criterio esatto per I(u) ∩ span(𝓓) = ⟨F⟩ con 𝓓 polinomiale di grado ≤ d (Burgers, KdV); dicotomia "forma chiusa ⇒ non identifica" come teorema; MODREL (Syz_f(u)), ALG-T1 (u analitica), MON-1, INT-T1 come caso 𝓗_M; INT-Q1 con limite di tempo; delta di novità rispetto a Scholl et al. (Mach. Learn. 2026) e He–Zhao–Zhong (FoCM 2024).
- **Criterio d'uscita.** Criterio esatto per Burgers e KdV con dizionari di grado ≤ d, oppure controesempio.
- **Skill.** session-protocol · proof-writer · math-skill · sympy · claim-lifecycle · novelty-check · kill-argument.
- **Input.** research/F4-ALG, F4-HOR, F4-INT (NOTE), work/C3, work/P4, research/CIT-AUDIT/AUDIT-4.md. **Output.** work/S4-ID/.

### S4-INTEG (corta) — lemmi di trasporto a DIMOSTRATO
- **Compito.** Punto 3 di G★′-NL. Portare a prova completa + CHECK_REQUEST: INT-T1/T2, F4LIN-T2 (costante 4ν ln 2: dichiarata elementare, Wang 1998), F4L-P3 (con confronto esplicito con Kieffer et al. arXiv:2512.12019), Hirota (E_int a coppie, ∫E_int = 0), ALG-L1/T1/P3/P4/P6, MODREL-T1; riduzione classica e modello di dato dichiarati; versione su Ω limitato o limite esplicito.
- **Criterio d'uscita.** Ogni lemma DIMOSTRATO, CON-FONTE o FALSO.
- **Skill.** session-protocol · proof-writer · math-skill · sympy · claim-lifecycle.
- **Input.** research/F4-INT, F4-LIN, F4-LIFT, F4-ALG, F4-HOR (NOTE), research/CIT-AUDIT/AUDIT-4.md. **Output.** work/S4-INTEG/.
