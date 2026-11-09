# PLAN — S5-INT (Fase 5, integrazione, parte 1: pacchetto lineare Fasi 1–3)
Data: 26/10/2026. Scrive solo in work/S5-INT/ e inbox/. Non modifica LEDGER né file di altre sessioni: propone.

## Skill caricate (in ordine d'uso)
1. skills-local/session-protocol (letto per primo) — piano, inbox, consegna, DONE.
2. skills-local/claim-lifecycle — stati ammessi (DIMOSTRATO/CON-FONTE/V-ex/APERTO/FALSO) per giudicare righe LEDGER.
3. skills-local/spec-sync — confronto definizioni PROBLEM/NOTAZIONE vs PROOF_PACKAGE (passo 3), AVVISI proposti.
4. _vendor/Auto-claude-code-research-in-sleep/skills/proof-checker/SKILL.md — SOLO la checklist di coerenza: Dependency DAG, Assumption Ledger (dove è scaricata ciascuna ipotesi), Typed Symbol Table (simboli che cambiano significato), REFERENCE_MISMATCH, SCOPE_OVERCLAIM, HIDDEN_ASSUMPTION; scala di severità FATAL/CRITICAL/MAJOR/MINOR (asse stato × impatto).
5. _vendor/scientific-agent-skills/skills/scientific-critical-thinking/SKILL.md — separare ciò che è dimostrato da ciò che è assunto; critica tracciabile (luogo, osservazione, conseguenza, rimedio).
SymPy: solo se una verifica lo richiede (work/S5-INT/sympy/).

## Compiti
(1) Coerenza delle ipotesi lungo le catene "dipende da" per C3-T1, C12-T1′, P1-T2, P2-T3/P2-C2, P3-T1/T3, P4-T2, P4-T6: per ogni lemma usato, ipotesi (dominio, spazio, P monico, ridotto, N, dati modali) vs contesto d'uso. Mismatch con severità.
(2) Notazione: simboli con due significati / concetti con due nomi (EP, 𝔅, γ_N/c_F, E_int nei quadri, Ω, S, Π, R, …) → correzioni NOTAZIONE.md (v4 proposta).
(3) Teorema di sintesi del caso lineare: catena di ID LEDGER (identificazione → fattori → termini → complessità/impossibilità) con ipotesi cumulate; punti di rottura.
(4) Residui: fix MINOR non recepiti (S-CHECK-7 C2-1, C2-2, P7-1..4, T2a-1; S-CHECK-8 L7-1, L7-2, LD-1; AVVISO P1-Q5; CIT-AUDIT-2/3/4) confrontando audit e testi (grep); claim mai auditati; citazioni con numero non confermato.
(5) Righe LEDGER incoerenti o duplicate.

## Fonti
RIPRESA, PROTOCOLLO, NOTAZIONE v1–v3, PROBLEM, GATE3, LEDGER, ROUTES; work/{C1C2,C3,II,P1,P2,P3,P4,SCOUT-TROP}/PROOF_PACKAGE.md (o VERDETTO); work/CHECK/AUDIT_*.md; research/CIT-AUDIT/AUDIT-2/3/4.md; inbox/S-P1.md (AVVISO).

## Contatti
central (PLAN-READY, TABELLA, DONE). Eventuali AVVISI alle sessioni solo proposti nella tabella "azione | file | chi".

## Criterio di "fatto"
work/S5-INT/INTEGRAZIONE_LINEARE.md con sezioni 1–5 + tabella finale; TABELLA in inbox/central.md; "DONE S5-INT (lineare)".
