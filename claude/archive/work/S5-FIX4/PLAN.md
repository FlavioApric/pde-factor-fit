# PLAN — S5-FIX4 · Fase 5, ultimo recepimento (fix d'audit OP-ANA, OP-R2; stato S4-TERM) · 26/10/2026

**Mandato (delega eccezionale del coordinatore):** applicare nei PROOF_PACKAGE di sessioni chiuse SOLO i fix già decisi dagli audit; ogni modifica marcata `[fix <id>, S5-FIX4]`; nessun altro cambiamento; nessuno stato oltre claims/LEDGER.md. Modello: work/S5-FIX3/REPORT.md. File temporanei: prefisso `fix4_` (scratchpad).
**Skill caricate:** skills-local/session-protocol, skills-local/claim-lifecycle (lettura dei SKILL.md; nessuno script _vendor eseguito). Nessun nuovo claim: niente proof-writer/proof-checker; gli enunciati nuovi (O9′, prova di (LWP), divergenza C1-1) sono trascritti dagli audit con rinvio.
**Fonti:** RIPRESA.md (ultimi aggiornamenti), claims/LEDGER.md (righe OPA-*, S4T-*, OPR2-*), work/CHECK/AUDIT_OP-ANA.md §2–§8, work/CHECK/AUDIT_OP-R2.md §1–§10, AUDIT-F5 (via LEDGER r. 142, per OPA-T3(e)).

## Interventi (in ordine)
1. **work/OP-ANA/PROOF_PACKAGE.md** ← AUDIT_OP-ANA (S-CHECK-15): T1-1 (MAJOR: "a t fissato, non uniforme in t", Λ(t) ~ 2log(1/(t−1)), coerenza con Tang–Teng) in §1, enunciato, r. 41, §6; T1-2 ((H_t) sufficiente; genericità = OPA-Q2; punti tripli = congettura); T1-3 (DIMOSTRATO mod [F1]); C1-1 (divergenza in OPA-C1, OPA-R1 ridotta → OPA-Q1); C1-2 (monotonia via inviluppo; positività di 1 − t cos b per continuità); L2-1 (∫k_s dy = 1 − S^D(s)1 ≤ erfc + erfc; frase sulle immagini corretta; originale come storico); T2-1 (C_* = 1.301); T3e-1 (dicotomia grappolo/gap; n e max|Re λ| fissi) + OPA-T3(e) DIMOSTRATO (Friedland–Yomdin arXiv:1107.0039 Thm 1.1; Nazarov St. Petersburg Math. J. 5(4) 1994 663–717); nuovi APERTI OPA-Q1, OPA-Q2; tabella stati = LEDGER.
2. **work/OP-R2/PROOF_PACKAGE.md** ← AUDIT_OP-R2 §10: per primi O9-1 (O9 FALSO, sostituita da O9′ con p′ = y₀y₃ − y₁y₂ + 3y₀²y₁; originale come storico) e T5-1 (prova diretta di (LWP) via Duhamel e lisciamento (νt)^{−1/2} al posto di Pazy/Henry); poi T1-1..T1-4, L1-1, T2-1, L3-1, T3-1, T3-2, T3-3, L2-1, C2-1, C2-2, P4-1, T5-2, T5-3, P6-1, O8-1; tabella stati = LEDGER.
3. **work/S4-TERM/PROOF_PACKAGE.md**: §1 Esito (c) e §11: S4T-Q1 CHIUSO a t fissato (OPA-T1, Θ(ν), non uniforme in t); S4T-Q2 CHIUSO mod (LWP) (OPR2-T5). Solo stato + rinvio.
Prima: grep dei marcatori (nessun `S5-FIX4` preesistente). Dopo: grep dei marcatori per id.
Fuori mandato (solo segnalazione): commento F3c in work/OP-R2/sympy/opr2_checks.py (O9-1); righe S4T-T4(iii) della tabella §1 di S4-TERM.

## Criterio di "fatto"
Tutti gli id sopra presenti con marcatore; tabelle stati coerenti col LEDGER; REPORT.md; DONE S5-FIX4 in inbox/central.md.
