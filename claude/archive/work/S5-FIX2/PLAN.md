# PLAN — S5-FIX2 · Fase 5 (recepimento dei fix d'audit) · 26/10/2026
**Mandato (delega eccezionale del coordinatore):** applicare nei PROOF_PACKAGE di sessioni chiuse SOLO i fix già decisi dagli audit; ogni modifica marcata `[fix <id>, S5-FIX2]`; nessun'altra modifica; nessuno stato oltre il LEDGER (claims/LEDGER.md). Modello: work/S5-FIX/REPORT.md.
**Skill caricate** (lettura dei SKILL.md): skills-local/session-protocol, skills-local/claim-lifecycle (solo per gli stati: lo stato registrato è quello del LEDGER). Nessuno script _vendor.
**File scrivibili:** work/S4-TERM/PROOF_PACKAGE.md, work/S4-ID/PROOF_PACKAGE.md, work/S4-INTEG/PROOF_PACKAGE.md, work/OP-ALG/PROOF_PACKAGE.md, work/C1C2/gram.md, work/S5-FIX2/, inbox/.

## Compiti (in ordine)
1. **S4-TERM** ← AUDIT_S4-TERM §3: T3-1 (MAJOR: titolo, Lettura, Esito di S4T-T3 come esito diviso (a) L∞/H^s negativo per definizione A9, (b) L¹ ≤ 1/2 solo per E^mult_AB, (c) L¹ di E^add APERTO S4T-Q1, numerica O(ν); ritirare "PR3 ✔ in L∞"); J-1, L1-1, F2-1 ([F2] DIMOSTRATO), T2-1, T2-2, T3-2, T3-3, Q1-1, P5-1, C1-1, C1-2; tabella §1 agli stati del LEDGER (r. 116–124).
2. **S4-ID** ← AUDIT_S4-ID §10: ID-1, ID-2, ID-3, ID-4 (testo ristretto), ID-5 (rinomina); tabella stati (LEDGER r. 91–100).
3. **S4-INTEG** ← AUDIT_S4-INTEG §9: P3-1..P3-4, K-1, K-2 (+ rinvio a work/KIEFFER/LETTURA.md, KIEFFER-C DIMOSTRATO), T1-1, P3a-1, P3a-2, M-1, P4-1, UC-1a, UC-1b, C-1, L-1, L-2, L-3; controllo della cifra 1.8·10⁻⁵ (mpmath se rapido, altrimenti marcata); tabella stati (LEDGER r. 82–90).
4. **OP-ALG** ← AUDIT_OP-ALG: OA-1 (L1′, P1′, uscite su 𝕂, nota sul campo), OA-2, OB-1 (+ OP-ALG-Q2 APERTO), OB-2, OB-3, OC-1, OI-1; tabella stati (LEDGER r. 109–115).
5. **C1C2/gram.md**: riga trasporti paralleli m ≥ 1: c_F = 1, densità provata (OP-FUN OPF-P5) — "PROVA SCRITTA, audit S-CHECK-14 in corso".
6. REPORT.md (elenco puntuale), DONE S5-FIX2 in inbox/central.md.

## Metodo
Edit puntuali (niente riscritture); dopo ogni file grep di `S5-FIX2` per controllare che ogni fix sia presente una sola volta. Script mpmath (solo per la cifra di L-3) in work/S5-FIX2/, .venv -I, timeout breve; non toccare processi altrui.
**Criterio di fatto:** ogni id elencato ha una marca nel file giusto o è dichiarato non applicabile con motivo nel REPORT.
