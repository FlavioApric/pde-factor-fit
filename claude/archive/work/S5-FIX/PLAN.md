# PLAN — S5-FIX · Fase 5 (integrazione) · 26/10/2026
Mandato (coordinatore, eccezionale): modificare i PROOF_PACKAGE di sessioni chiuse **solo** sui punti elencati, ognuno marcato `[fix <id>, S5-FIX]`, senza cambiare altro. Non toccare claims/LEDGER.md, NOTAZIONE.md (solo file nuovi: claims/LEDGER_v2.md, work/S5-FIX/NOTAZIONE_v4_proposta.md). Nessuno script `_vendor`. Se una scrittura è bloccata: non aggirarla, testo nella risposta finale.

## Fonti lette
RIPRESA.md (aggiornamenti fino a S5-INT), skills-local/session-protocol, skills-local/claim-lifecycle, work/S5-INT/INTEGRAZIONE_LINEARE.md (intero), claims/LEDGER.md, NOTAZIONE.md, work/CHECK/AUDIT_gammaN.md §7, AUDIT_C3-T2a.md §5, AUDIT_P4-L7.md §4, AUDIT_P1.md (P4-1), research/CIT-AUDIT/AUDIT-2.md (#1a, 1b, 2b), AUDIT-3.md (#7).
## Skill
session-protocol (struttura: piano, PLAN-READY, REPORT, DONE); claim-lifecycle (vocabolario degli stati per LEDGER_v2; nessuno stato alzato senza controllo: le correzioni di LEDGER_v2 riflettono solo audit già chiusi). SymPy non serve (nessun nuovo calcolo).

## (A) Fix nei PROOF_PACKAGE — elenco chiuso
| file | fix | luogo previsto | azione |
|---|---|---|---|
| work/P2/PROOF_PACKAGE.md | C2-1 | §7 P2-C2, riga "Dipendenze" (r. 163) | sostituire "Nessuna dipendenza da P2-T3" con la dipendenza da P2-T3(b) per (e) N=2 e (f) |
| work/P2/PROOF_PACKAGE.md | C2-2 | §7 P2-C2(f) *Non necessità* | "γ_3 ≥ 1" via σ(S*S)∖0 = σ(SS*)∖0 |
| work/C1C2/PROOF_PACKAGE.md | P7-1 | §6 C12-P7(a) tesi | "indipendenti" → "la densità non implica la chiusura; chiusa senza densa: APERTO (P2-Q1)" |
| work/C1C2/PROOF_PACKAGE.md | P7-2 | C12-P7 prova (a) | chiusura di ker_{H^m}P: rinvio a §1 (H^σ, σ<0) e a P(∂): H^m → 𝒟′ continua |
| work/C1C2/PROOF_PACKAGE.md | P7-3 | C12-P7 ipotesi N≥2 / (c) | prodotto scalare di H^m fissato; γ_N dipende da esso, γ_N>0 no |
| work/C1C2/PROOF_PACKAGE.md | P7-4 | C12-P7(d) prova | ε_k>0; c_F = sup dei blocchi (Cauchy–Schwarz); "Viceversa" con rinvio |
| work/C1C2/gram.md | P7-3, P7-4 | §2bis | stesse precisazioni |
| work/C3/PROOF_PACKAGE.md | T2a-1 | §5 C3-T2 *Ipotesi* | Ω aperto non vuoto basta per (a); q_k≠0 solo per V(Ann u) |
| work/C3/PROOF_PACKAGE.md | CIT-AUDIT-2 #1a–1b | r. 3, 11, 32, 137, 150, 153, 238, 248 | C3-P1[gen] CON-FONTE (verificata): Malgrange AIF 6, Chap. I §2 Thm 2 p. 292; Hörmander ICASV 3ª ed. Thm 7.6.14 (secondaria) |
| work/C3/PROOF_PACKAGE.md | CIT-AUDIT-2 #2b | C3-T2(c) [fix T2-2] (r. 124), tabella r. 242 | Fulton 2008 §5.3 p. 57, Cor. 3 p. 58 (verificato) |
| work/P4/PROOF_PACKAGE.md | L7-1 | P4-L7 enunciato e passo (3) | irriducibilità dei P_i in ℂ[τ,ξ] (K = ℚ̄ alg. chiuso; prova breve dell'audit) |
| work/P4/PROOF_PACKAGE.md | L7-2 | P4-L7 passo (1) | automorfismo di ℂ-algebre di ℂ[τ,ξ] che manda K[τ,ξ] in sé |
| work/P4/PROOF_PACKAGE.md | dip. nascoste | P4-T1(iv) (r. 35), P4-C4(a) (r. 199) | nota "(non auditato)" per C3-L1 / C3-P5(a) dove manca |
| work/P1/PROOF_PACKAGE.md | AVVISO P1-Q5 | r. 5, 42, 327, 354 | "chiuso al 1° ordine solo per dati modali finiti; dati generali P3-Q-bordo APERTO" |
| work/P1/PROOF_PACKAGE.md | CIT-AUDIT-3 #7 | tabella r. 340 | togliere "(+ CON-FONTE Rudin FA 10.27)" |
| work/P1/PROOF_PACKAGE.md | INT-5 | P1-P2(a) (r. 179) | citare II-T3 (ii)⇒(iv) al posto di C12-P1(b) |
Fuori mandato (non tocco, segnalo nel REPORT): tabelle stati indietro (§4.2 di INTEGRAZIONE), LD-1, intestazione P4-L7 "controllo indipendente in attesa", work/II, work/P3.

## (B) claims/LEDGER_v2.md
Copia di claims/LEDGER.md con L-1…L-23 (INTEGRAZIONE §5) applicate; vocabolario unificato (DIMOSTRATO, PROVA SCRITTA, CON-FONTE, CON-FONTE (verificata), V-ex, APERTO, PARZIALE, FALSO), colonne proof-checker aggiornate, P2-T4 fuso, segnaposto riempiti dai PROOF_PACKAGE, "dipende da" completate, P4-L7 ristretto (L7-3), R2-T3 esteso via C12-T1′/C12-L2′ come nota. Le nuove righe S5-L1, S5-L2, S5-SINT NON sono nel mandato (§5 le propone, il compito chiede solo L-1…L-23): non aggiunte, segnalate. Testata con legenda delle modifiche [L-n].

## (C) work/S5-FIX/NOTAZIONE_v4_proposta.md
Testo di §2.3 di INTEGRAZIONE_LINEARE, pronto da appendere (trascrizione fedele, blocco di codice tolto, tabella E_int resa come tabella Markdown valida).

## Criterio di fatto
Ogni fix con marcatore nel file; grep di controllo; REPORT.md con file/id/riga; DONE S5-FIX in inbox/central.md.
