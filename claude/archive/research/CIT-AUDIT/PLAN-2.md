# PLAN-2 — CIT-AUDIT-2 (Fase 3, verifica mirata di citazioni usate in prove del LEDGER)

Data: 2026-10-25 · Agente: CIT-AUDIT-2 · Input: RIPRESA.md (agg. 25/10 sera), PROTOCOLLO.md, skills-local/session-protocol, research/CIT-AUDIT/AUDIT.md + PLAN.md (metodo 1ª tornata), claims/LEDGER.md, inbox/central.md (TABELLE S-CHECK-2C/2D), work/C3, work/C1C2, work/II, work/CHECK/AUDIT_*.md.

## 1. Domande (citazione → claim del LEDGER che la usa)
| # | citazione da verificare | usata in |
|---|---|---|
| Q1 | Malgrange (AIF 6, 1955–56): densità delle soluzioni esponenziali-polinomiali in ker P su Ω convesso (C^∞, D′); numero in Hörmander (ICASV 7.6.14? ALPDO II? §7.3?), Trèves, Ehrenpreis, Palamodov | C3-P1[gen] (work/C3/PROOF_PACKAGE.md#C3-P1; AUDIT_C3-secondari P1-1 MAJOR); C12-Q3; C12-T1 su convessi |
| Q2a | Fulton, *Algebraic Curves*, cap. 1 §6: V(F,G) finito per F,G senza fattori comuni (Prop. 1 o 2?) | C3-L2 (L2-1), II (Fatto V) |
| Q2b | Fulton, Bézout (§5.3) | C3-T2(c,d), II-C2, R4-T5[𝕋] |
| Q3 | Hörmander ALPDO I Thm 3.1.4′ (∂_t v = 0 su X×I) e Thm 2.2.1 (incollamento/fascio) | C3-L3 (L3-1, L3-2) |
| Q4 | Weibel Thm 2.7.6 (Ext da risoluzione proiettiva / bilanciamento) e Koszul §4.5 | C12-L2 (L2-1) |
| Q5 | Horn–Johnson §3.5 (LU/LDU ⟺ minori principali, "Cor. 3.5.6"); Borel LAG Prop. 14.4 (prodotto di sottogruppi radice in ordine arbitrario) | II-T7(a–d) (MC-3, MC-4) |
| Q6 | Higham FM Thm 1.12; Shohat 1936 (Appell ortogonali = Hermite); Deutsch BAIPS Thm 9.35 (somma chiusa ⟺ angolo) | II-P5, II-T4; C12-P6; C12-P7 |
Per ciascuna: enunciato esatto, numero, pagina se reperibile, edizione. Esiti: VERIFICATA / PARZIALE / NON VERIFICATA (mai numeri inventati).

## 2. Skill caricate (lette con Read; nessuno script `_vendor` eseguito)
1. `skills-local/session-protocol/SKILL.md` (per primo): piano, inbox, consegna, DONE.
2. `_vendor/scientific-agent-skills/skills/citation-management/SKILL.md`: fonti canoniche dei metadati (Crossref/DOI/OpenAlex), "never invent pages, volume", log delle fonti.
3. `_vendor/scientific-agent-skills/skills/paper-lookup/SKILL.md`: provenienza riproducibile, diffidare delle risposte vuote/200, dichiarare i vuoti.
4. `_vendor/Auto-claude-code-research-in-sleep/skills/research-lit/SKILL.md`: ricerca web multi-fonte e tagging verified/UNVERIFIED (solo istruzioni Markdown; nessun helper).

## 3. Fonti / stringhe di ricerca
- WebSearch/WebFetch: indici e anteprime (Springer link capitoli, Google Books), zbMATH Open (`zbmath.org/?q=`), recensioni, note di corso e articoli che citano il teorema con numero (es. "Hörmander Theorem 7.6.14", "Fulton Proposition 2 section 1.6", "Weibel Theorem 2.7.6 balancing Ext", "Borel Proposition 14.4 unipotent product", "Horn Johnson Corollary 3.5.6 LU", "Higham Theorem 1.12 functions of matrices", "Deutsch Theorem 9.35 Friedrichs angle closed sum", "Shohat 1936 Appell orthogonal").
- Numdam per Malgrange (AIF 6, DOI 10.5802/aif.65).
- Regola: un numero è VERIFICATO solo se letto in una fonte primaria (indice/anteprima) o in ≥1 fonte secondaria affidabile che lo cita esplicitamente con lo stesso enunciato; altrimenti PARZIALE/NON VERIFICATO.

## 4. Comunicazione
- inbox/CIT-AUDIT.md letta (vuota). Output: `PLAN-READY CIT-AUDIT-2` e poi TABELLA + `DONE CIT-AUDIT-2` in inbox/central.md. Scrivo solo in research/CIT-AUDIT/ e inbox/.

## 5. Criterio di fatto
- research/CIT-AUDIT/AUDIT-2.md con tabella (citazione | dove è usata | verificata sì/no/parziale | riferimento corretto | fonte della verifica | azione proposta) per tutte le voci Q1–Q6; TABELLA di correzioni al LEDGER in inbox/central.md; DONE.
