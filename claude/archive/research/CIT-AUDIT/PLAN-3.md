# PLAN-3 — CIT-AUDIT-3 (Fase 3, verifica mirata di citazioni residue)

Data: 2026-10-25 · Agente: CIT-AUDIT-3 · Input: RIPRESA.md (ultimo AGGIORNAMENTO 25/10 sera), PROTOCOLLO.md, skills-local/session-protocol, research/CIT-AUDIT/PLAN-2.md + AUDIT-2.md (metodo), claims/LEDGER.md, inbox/CIT-AUDIT.md (vuota), contesti d'uso in work/C1C2, work/P1, work/P3, work/CHECK/AUDIT_*.md.

## 1. Domande (citazione → claim che la usa)
| # | citazione | usata in |
|---|---|---|
| Q1 | Rudin, *Real and Complex Analysis* (3ª ed.), Thm 13.11: equivalenze della semplice connessione per regioni piane | C12-P10 (premessa sull'indice ⟺ "non s.c."), fix P10-1; C12-L1′ (viceversa H¹_dR=0 ⇒ s.c.) |
| Q2a | Hörmander ALPDO I Thm 1.4.5 (partizione dell'unità); "ivi Thm 2.2.4" (fascio) | C12-L1′ (fix L1p-2) |
| Q2b | Lee, *Introduction to Smooth Manifolds* 2ª ed., cap. 11 (s.c. ⇒ ogni 1-forma chiusa esatta; H¹_dR(ℝ²∖{0}) ) | C12-L1′, C12-P10 (P10-3) |
| Q3 | Cox–Little–O'Shea, *Ideals, Varieties, and Algorithms*, cap. 3 §6 (risultanti; Prop. 3 e 5? edizione) | C12-L3 (L3-2), II-T2 (MC-2) |
| Q4 | Humphreys, *Introduction to Lie Algebras…*, §4.1 Cor. A (Lie: catena di ideali) | P1-T4 |
| Q5 | F. John, *Partial Differential Equations*, cap. 7 (esempio di Tychonoff) | P1-P1(b); AUDIT_R5-T2 (b) |
| Q6 | Wei–Norman, J. Math. Phys. 4 (1963); Proc. AMS 15 (1964) | P1-T4, P1-P4/P1-L…, II-T7 |
| Q7 | Rudin, *Functional Analysis*, Thm 10.27 (calcolo funzionale olomorfo omomorfismo) | P1-P4 (fix P4-1: evitabile) |
| Q8 | Engel–Nagel, *One-Parameter Semigroups…*, Thm III.3.14 / Cor. III.3.16 (Miyadera–Voigt) | P3-L2(d), P3-T1 |
| Q9 | Deutsch, *Best Approximation in Inner Product Spaces*, Thm 9.35 (2° tentativo) | C12-P7 (ora non portante: P2-T3) |
Per ciascuna: enunciato, numero, edizione, pagina se reperibile. Esiti: SÌ (primaria) / SÌ (secondaria) / PARZIALE / NO — mai numeri inventati.

## 2. Skill caricate (lette con Read; nessuno script `_vendor` eseguito)
1. `skills-local/session-protocol/SKILL.md` (per primo): piano, inbox, consegna, DONE.
2. `_vendor/scientific-agent-skills/skills/citation-management/SKILL.md`: metadati da fonti canoniche (Crossref/DOI), "never invent pages, volume", log delle fonti.
3. `_vendor/scientific-agent-skills/skills/paper-lookup/SKILL.md`: provenienza ripetibile (endpoint, data di accesso), le risposte vuote/200 non valgono come conferma, dichiarare i vuoti.

## 3. Fonti / stringhe di ricerca
- WebSearch/WebFetch (e curl per PDF aperti): Crossref API per i DOI di Wei–Norman (J. Math. Phys., Proc. AMS); PDF AMS ad accesso aperto (Proc. AMS è libero dopo 5 anni); indici/anteprime dei libri; note di corso e articoli arXiv che citano il numero con l'enunciato ("Rudin Theorem 13.11 simply connected", "Hörmander Theorem 1.4.5 partition of unity", "Humphreys Corollary A 4.1", "Engel Nagel Theorem III.3.14 Miyadera", "Corollary III.3.16", "Rudin Functional Analysis Theorem 10.27", "Cox Little O'Shea Proposition 3 resultant §3.6", "Fritz John Tychonoff chapter 7", "Deutsch Theorem 9.35").
- Regola (come AUDIT-2): VERIFICATO solo se letto in fonte primaria o in ≥1 fonte secondaria affidabile che cita esplicitamente numero + enunciato; altrimenti PARZIALE/NO.

## 4. Comunicazione
- PLAN-READY CIT-AUDIT-3 in inbox/central.md; alla fine TABELLA di correzioni LEDGER + DONE CIT-AUDIT-3 in inbox/central.md. Scrivo solo in research/CIT-AUDIT/ e inbox/.

## 5. Criterio di fatto
research/CIT-AUDIT/AUDIT-3.md con tabella (citazione | dove usata | verificata | riferimento corretto | fonte della verifica | azione) per Q1–Q9, provenienza; TABELLA in central; DONE.
