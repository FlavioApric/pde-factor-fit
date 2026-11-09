# PLAN — S-P1 (struttura di E_int) · Fase 3, seconda ondata · 25/10/2026
Scheda: SESSIONS.md §S-P1. Prima esecuzione (cartella creata ora). Decisioni Gate 1: H0 = ℝ, H1 = H^m(Ω) con Ω limitato, componente = fattore.
Item del piano: P1 (P1.1–P1.4), P3 (in parte), C4.3; appunti A8, A9, B2, B3, B4; G3, G8; G★′ punto 3 e 4 (PROBLEM.md).

## 1. Domande (con ID)
- **Q-P1.1 (definizione, NOTAZIONE v2 R5-D1, Gate 1, C12-C1).** Definizione canonica di E_int a due livelli: (a) *tra fattori* (componente = fattore, C12-T1): quadro "nucleo" in 𝒟′ / C^∞ / H^m(Ω), coerente con C12-C1 (in H^m l'ostruzione è un difetto di regolarità, non un termine d'interazione nel senso di A9); (b) *dentro un fattore* τ − a(ξ), a = Σ a_n (termini): quadri additivo, moltiplicativo, log-simbolo, su Ω limitato **senza condizioni al bordo**. Punto critico (AUDIT_R5-T2 I-3): su Ω limitato u₀ non determina i flussi dei singoli termini; serve una classe in cui S_n(t) sia intrinseco. Proposta: classe 𝔅(Ω) delle funzioni di tipo esponenziale (∂_x limitato), dove S_n(s) = e^{s a_n(∂_x)} è una serie di operatori limitati che commutano; più la versione formale (getto in t) valida per ogni u.
- **Q-P1.2 (R5-T2[H1], LEDGER APERTO).** Rifare R5-T2 con claim-lifecycle su Ω limitato con le ipotesi I-1, I-2 incorporate (commutazione dei gruppi, ogni termine genera, classe di unicità), la restrizione I-4 (valore e aggregati per ordine O(N), O(N²); tabella {c_S} Ω(2^N)) e il modello di costo esplicito (I-5) nel modello di dato "esponenziale-polinomio" (O7). Necessità della classe (non unicità dei flussi per termine fuori da 𝔅).
- **Q-P1.3 (fattori del 2° ordine e scomposizione in 𝔅).** Le componenti per fattore di u ∈ 𝔅 stanno in 𝔅? (necessario per applicare Q-P1.2 a ogni fattore). Fattori del 2° ordine in t (II-P6: sl₂/gl₂): E_int^mult per modo = coordinate di Gauss (II-T7); in 𝔅_ρ esiste un tempo uniforme T*(ρ) > 0 (risposta al punto 3 dell'AVVISO corretto di S-II: inf|φ₁| uniforme).
- **Q-P1.4 (classificazione per algebra di Lie, R5-P7, R5-Q5, R7-P5).** (i) finita risolubile ⇒ E_int^mult esatto con d = dim 𝔤 funzioni intere (quadrature); (ii) finita non risolubile ⇒ germi analitici, globalità non garantita (sl₂: tan t; II-T7); (iii) infinita ⇒ obiettivo: teorema d'impossibilità. Prima va resa precisa R5-Q5 (come scritta è banalmente falsa?), poi dimostrata nella forma più forte raggiungibile.
- **Q-P1.5 (E_int dal bordo, PR-C2d §4).** Con condizioni al bordo i termini a coeff. costanti non commutano: enunciato quantitativo (quanto è grande E_int^mult creato dal bordo) e confronto con il quadro senza bordo (𝔅), con TROP-7 (strato limite) e C12-C1 (angolo).

## 2. Skill (ordine d'uso)
1. `skills-local/session-protocol` — letta per intera per prima (orientamento, PLAN, inbox, consegna).
2. `skills-local/claim-lifecycle` — ciclo di ogni claim; righe LEDGER.
3. `_vendor/Auto-claude-code-research-in-sleep/skills/formula-derivation/SKILL.md` — per Q-P1.1 (scelta dell'oggetto invariante: il propagatore per termine su 𝔅; separazione identità / proposizione / interpretazione).
4. `_vendor/Auto-claude-code-research-in-sleep/skills/proof-writer/SKILL.md` — triage (PROVABLE AS STATED / AFTER WEAKENING / NOT JUSTIFIED) e struttura di ogni prova.
5. `_vendor/scientific-agent-skills/skills/sympy/SKILL.md` — controlli in `work/P1/sympy/` (solo verifica), `D:\ProblemaBase\.venv\Scripts\python.exe -I`.
6. `_vendor/Auto-claude-code-research-in-sleep/skills/kill-argument/SKILL.md` — sul risultato principale (P1-T2 = R5-T2[H1] + definizione): due subagenti Claude freschi (attacco ~200 parole; giudizio per punti), niente Codex; verdetto calcolato con la tabella della skill.
7. proof-checker: non eseguito da me — audit a S-CHECK (CHECK_REQUEST.md autosufficiente + DOMANDA in inbox/S-CHECK.md). Nessun claim DIMOSTRATO senza audit.

## 3. Fonti
research/R5 (REPORT §1–4, open_questions Q4–Q6), work/CHECK/AUDIT_R5-T2.md, research/PR-C2b (P3–P5), research/PR-C2d §4, research/R7 §4, work/C1C2/PROOF_PACKAGE.md (C12-T1, P1, T2, C1, T5), work/II/PROOF_PACKAGE.md §5 (II-P6, II-T7 con fix), work/SCOUT-TROP/VERDETTO.md (TROP-3′, 4, 7), claims/LEDGER.md. Letteratura citata solo se necessaria e marcata: Wei–Norman 1963/64, Engel–Nagel 2000, Rudin FA (calcolo funzionale olomorfo), Pólya/Boas (tipo esponenziale). Nessuna ricerca web prevista.

## 4. Contatti
- S-P2 (inbox/S-P2.md): TABELLA — E_int^⊥/E_int^∥ restano di S-P2; da me: classe 𝔅, definizione dei quadri, formula commutante e costo.
- S-P3 (inbox/S-P3.md): TABELLA — interaction picture, Dyson/Magnus, Wei–Norman formale, E_int dal bordo (per regole di selezione ed elemento di matrice).
- S-TROP, S-II, S-C1C2 (chiuse): RISPOSTA nelle loro inbox agli AVVISI ricevuti (non contengono DOMANDE).
- S-CHECK: DOMANDA (audit). central: PLAN-READY, TABELLA LEDGER, DONE.

## 5. Criterio di "fatto"
- PROOF_PACKAGE.md con: definizione canonica (P1-D1…D3), P1-T2 (R5-T2 su Ω limitato) con prova completa e necessità della classe, costo con modello dichiarato, scomposizione per fattori in 𝔅, classificazione di Lie con (i) dimostrata, (ii) con controesempio alla globalità, (iii) riformulazione precisa di R5-Q5 e un teorema d'impossibilità dimostrato (anche se parziale), E_int dal bordo con enunciato quantitativo.
- SymPy: tutti i controlli PASS, citati.
- kill-argument eseguito su P1-T2 e verdetto registrato.
- CHECK_REQUEST.md + DOMANDA a S-CHECK; TABELLE a S-P2/S-P3; righe LEDGER in central; DONE S-P1.

---
## Ripresa — audit 3 (25/10/2026)
Rilancio breve del coordinatore (RIPRESA.md, ultimo AGGIORNAMENTO: "S-P1 ripresa (fix S-CHECK-3)"). Lavoro già consegnato: non si ricomincia, si modifica solo PROOF_PACKAGE.md.
**Input letti.** skills-local/session-protocol (per primo), skills-local/claim-lifecycle; inbox/S-P1.md (RISPOSTA di S-CHECK-3, RISPOSTA di S-P3 su P1-Q5, RISPOSTA di S-P2, AVVISI del coordinatore, di S-II e di S-C1C2); work/CHECK/AUDIT_P1.md (per intero); claims/LEDGER.md (righe R5-T2[𝔅], R5-T2[H^m], R5-Q5, P1-*); PROBLEM.md G★′ punto 2 (riformulato, approvato dall'utente).
**Compiti (criterio di "fatto" = tutti spuntati nel PROOF_PACKAGE, ogni modifica marcata `[fix <id>]`).**
1. Fix MINOR dell'audit, nell'ordine del PROOF_PACKAGE: L1-1, L1-2 (§2); L3-1, L3-2 (§2); P1e-1, P1e-2 con l'enunciato rafforzato "per ogni tempo base t₀ ∈ Ī" (§4, P1-P1(e), prova per t₀ < T e per t₀ = T); P1a-1, P1b-1 (§4); T2-1 (ρ′ > max(ρ,r)), T2-2 (§4); T3-1 (costo della tabella Θ(M2^N(L+1)²)), T3-2 (real-RAM con oracolo exp) (§5); P2-1, P2-2, P3-1 (§6); P4-1 (argomento dei caratteri al posto di Rudin FA 10.27), P4-2, P4-3, P4-4 (§7); C1-1 (refuso: 𝔈^mult = e^{−tT₂}e^{−tT₁}e^{t(T₁+T₂)}), C1-2 (§8); T5-1 (polidisco comune, intorno fisso di ε), T5-2, T5-3 (§8); P6-1, P6-2 (§9).
2. Problemi aperti (§12): aggiungere P1-Q7 (P1-T5 senza "flussi di Y spenti a ε = 0", O-2 dell'audit); recepire la chiusura al 1° ordine nell'accoppiamento di P1-Q5 da S-P3 (P3-T3, legge Θ(t^{5/4}); residuo a ε = 1 = P3-Q2).
3. Quadro di Ω: dove si usa la scomposizione per fattori in 𝒟′/C^∞ (P1-D2) passare da "rettangolo" a "Ω limitato, connesso e semplicemente connesso" (C12-T1′, DIMOSTRATO; PROBLEM.md G★′ punto 2 riformulato), con l'ostruzione topologica C12-P10 fuori da questa classe; la classe 𝔅 e P1-P2/P1-P3/P1-P4 restano sul rettangolo (che è semplicemente connesso).
4. Tabella degli stati (§1) e righe LEDGER (§11): DIMOSTRATO per i claim passati, con le righe già registrate dal coordinatore (R5-T2[𝔅] DIMOSTRATO, R5-T2[H^m] FALSO, R5-Q5 FALSO come scritta, P1-P1(b) CON-FONTE, P1-Q6/Q7 APERTI).
**Skill.** session-protocol, claim-lifecycle (stati = ultimo controllo superato: l'audit S-CHECK-3 è il proof-checker; nessun nuovo enunciato portante oltre al rafforzamento P1e-2, già verificato dall'audit, O-1 e SymPy P1e.4). Nessuno script _vendor; nessun nuovo script SymPy necessario (i fix sono di scrittura; i controlli numerici di P1e-2 sono in work/CHECK/sympy/audit_p1.out).
**Scrittura.** Solo work/P1/ e inbox/. Chiusura: "DONE S-P1 (ripresa audit)" in inbox/central.md.
