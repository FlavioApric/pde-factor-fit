# REPORT — S5-FIX · Fase 5 (integrazione) · 26/10/2026
(Salvato dal coordinatore: la scrittura del subagente era bloccata dall'ambiente; testo integrale nella sua risposta finale. Sintesi fedele.)
**Mandato:** applicare nei PROOF_PACKAGE di sessioni chiuse solo i fix decisi dagli audit (INTEGRAZIONE_LINEARE §4) e da CIT-AUDIT-5; ogni modifica marcata `[fix <id>, S5-FIX]`. Prodotti: claims/LEDGER_v2.md, work/S5-FIX/NOTAZIONE_v4_proposta.md. Nessun fix doppio (controllo grep dopo l'interruzione per limite API). claims/LEDGER.md e NOTAZIONE.md non toccati dall'agente.

## (A) Fix applicati
| file | fix | dove | cosa |
|---|---|---|---|
| work/P2/PROOF_PACKAGE.md | C2-1 | r.163, P2-C2 Dipendenze | dipende da P2-T3(b) solo per (e) con N=2 e per (f) |
| work/P2/PROOF_PACKAGE.md | C2-2 | r.169, P2-C2(f) | γ_3≥1 via σ(S*S)∖0 = σ(SS*)∖0, SS*≥I |
| work/C1C2/PROOF_PACKAGE.md | P7-3, P7-1, P7-2, P7-4 | r.222–230, C12-P7 | prodotto scalare fissato; "densa ⇏ chiusa", "chiusa senza densa" APERTO; rinvio H^σ; ε_k>0, c_F = sup dei blocchi |
| work/C1C2/gram.md | P7-3, P7-4 | §2bis | idem |
| work/C3/PROOF_PACKAGE.md | T2a-1; CIT-AUDIT-2 #1a–1b, #2b; CIT5-9 | r.118; varie; r.124, 242; r.191 | Ω aperto non vuoto per (a); Malgrange verificato; Fulton §5.3; Hörmander ALPDO II §11.4 |
| work/P4/PROOF_PACKAGE.md | L7-1, L7-2, CIT5-3, CIT5-2, dipendenza nascosta | r.157–161, r.20, r.199 | irriducibilità assoluta; automorfismo di ℂ[τ,ξ]; Cauchy–Kovalevskaya (olomorfa / (Re u, Im u)); (AC) con Cohen, Loos, Trager; C3-P5(a) non auditata |
| work/P1/PROOF_PACKAGE.md | AVVISO P1-Q5; CIT-AUDIT-3 #7; INT-5 | r.5, 42, 327, 354; r.340; r.179 | "solo dati modali finiti"; tolto Rudin FA 10.27; P1-P2(a) ← II-T3 |
| work/II/PROOF_PACKAGE.md | CIT5-1, CIT5-6, CIT5-8 | r.89, 123, 141 | II-T2(b′) con lemma del vettore ciclico; Kato I §5.3/§5.6; Horn–Johnson MA Cor. 3.5.4 (2ª ed.) |
| work/S5-INT/INTEGRAZIONE_LINEARE.md | CIT5-4 | r.255, S5-L2(iii) | Kato IV §5.2 → lemma della mappa aperta (AUDIT-5 §2.3) |
**Fuori mandato, non toccati:** tabelle/intestazioni di stato in ritardo rispetto al LEDGER (C3-T2(a); C12-P7 "audit in attesa"; tabella §1 di P2; intestazioni di P4 e P4-L7; tabella 0-bis di II); LD-1; unificazione S→Σ; II-T2(d)/II-T3 → C12-T1′; work/P3; tabella §4.4 di INTEGRAZIONE (cita ancora Kato IV §5.2).

## (B) claims/LEDGER_v2.md
Correzioni L-1…L-23 di INTEGRAZIONE_LINEARE §5 marcate [L-n]/[CIT5-n]: R2-T3 esteso (nota); C12-T1 ipotesi; TROP-5..8 PROVA SCRITTA (TROP-6 V-ex); riga II divisa (II-C1 DIMOSTRATO, altri PROVA SCRITTA); segnaposto riempiti (C3-T2(a), II-L1(b), P1-L5); C12-P7(a–d) fuso e DIMOSTRATO; P2-C2 (S-CHECK-7); P2-T4 riga unica; C3-Q1 PARZIALE; P4-T5, P4-T6, riga P4, P4-T2, P4-L7 (ristretto, L7-3); P1-Q5 = P3-Q2; dipendenze P3; C3-T4; C12-L1′/L2′; II-T9; P1-P2(a) ← II-T3. Vocabolario unificato (stato + qualifica); note CIT5. S5-L1, S5-L2, S5-SINT NON aggiunti (fuori mandato). 77 righe di tabella contro 76.

## (C) work/S5-FIX/NOTAZIONE_v4_proposta.md
Testo di INTEGRAZIONE §2.3, contenuto invariato, pronto da appendere a NOTAZIONE.md.
