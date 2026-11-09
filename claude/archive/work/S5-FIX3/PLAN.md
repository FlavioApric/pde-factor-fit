# PLAN — S5-FIX3 · Fase 5 (recepimento dei fix d'audit OP-FUN, OP-NL) · 26/10/2026

**Mandato (delega eccezionale del coordinatore):** applicare nei PROOF_PACKAGE di sessioni chiuse SOLO i fix già decisi dagli audit; ogni modifica marcata `[fix <id>, S5-FIX3]`; nessun altro cambiamento; nessuno stato oltre claims/LEDGER.md. Modello: work/S5-FIX2/REPORT.md. File temporanei con prefisso `fix3_` nello scratchpad condiviso.
**Skill caricate:** skills-local/session-protocol, skills-local/claim-lifecycle (lettura dei SKILL.md; nessuno script _vendor eseguito). Nessun nuovo claim: niente proof-writer/proof-checker; gli enunciati nuovi (lemma dell'involuzione pesata, costruzione T4-1, certificato NL-1) sono trascritti dagli audit con il loro rinvio.
**Fonti:** RIPRESA.md (ultimi aggiornamenti), claims/LEDGER.md (righe OP-*, OPF-*, S5-L2, S4ID-K1), work/CHECK/AUDIT_OP-FUN.md §2–§12, work/CHECK/AUDIT_OP-NL.md §1–§12.

## Interventi (in ordine)
1. **work/OP-FUN/PROOF_PACKAGE.md** ← AUDIT_OP-FUN: T2-1, P3-1, P3-2, P4-1, P4-2, C1-1, T5-1, T5-2, T5-3, O1-1 (lemma: le sole simmetrie affini pesate di (τ−ξ²)(τ+ξ) sono l'identità e l'involuzione v = e^{t−x}w(t,2t−x); verifica S-CHECK-14), T4-1 (costruzione per ξ = Σ[θ_k]⊗n_k qualsiasi), T4-2 (CON-FONTE dichiarate; (i),(ii), criterio indipendenti), P6-1 (C12-T1′(iii) o argomento comassimale), S5L2-1 ((v) corretta + controesempio ℝ³), nuovo APERTO OPF-Q3; tabella stati = LEDGER.
2. **work/S5-INT/INTEGRAZIONE_LINEARE.md**: S5-L2(v) con la correzione S5L2-1.
3. **work/OP-NL/PROOF_PACKAGE.md** ← AUDIT_OP-NL: NL-1 (certificato esatto: W_2 = 16, deg Π_2 ≤ 8 ∀k ∈ U_0, = 8 su un aperto di Zariski), NL-2, NL-3, NL-4 (i)–(v), NL-5, NL-6, NL-7, NL-8, NL-9, NL-10; tabella stati = LEDGER.
4. **work/S4-ID/PROOF_PACKAGE.md**: S4ID-K1 DIMOSTRATO tramite OP-T7 (rinvio), tabella stati.
5. **work/C1C2/gram.md** §1 r. 3: densità con OPF-T5, OPF-P5 (DIMOSTRATO, S-CHECK-14); APERTI OPF-Q1, OPF-Q3.
Prima di ogni fix: grep per evitare doppioni. Dopo: grep dei marcatori `S5-FIX3`.

## Criterio di "fatto"
Tutti gli id sopra presenti con marcatore nei file; tabelle stati coerenti col LEDGER; REPORT.md con elenco puntuale; DONE S5-FIX3 in inbox/central.md.
