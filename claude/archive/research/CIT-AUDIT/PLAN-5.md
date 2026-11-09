# PLAN-5 — CIT-AUDIT-5 (Fase 5, citazioni con numero non confermato che reggono passi di prove)

Data: 2026-10-26 · Agente: CIT-AUDIT-5 · Input: work/S5-INT/INTEGRAZIONE_LINEARE.md §4.4 (e INT-13, INT-21, S5-L2 §3.4), AUDIT-2/3/4 (metodo e voci già coperte), testi d'uso: work/II/PROOF_PACKAGE.md (II-T1, II-T2(b,b′), II-P5, II-T7), work/P4/PROOF_PACKAGE.md (AC, P4-L7), work/P4/CHECK_REQUEST_2.md, work/C3/PROOF_PACKAGE.md (C3-L2(iii), C3-P5(b)).

## 1. Domande (voce → passo che la usa → cosa verificare)
| # | voce | usata in | cosa verificare |
|---|---|---|---|
| Q1 (prio) | Horn–Johnson, *Topics in Matrix Analysis*, Thm 4.4.17 | II-T2(b′) (⇒): centralizzatore di una non derogatoria = ℂ[C₀] | esistenza, numero, enunciato; se no: prova autosufficiente (vettore ciclico della compagna) |
| Q2 (prio) | Cohen, GTM 138, cap. 4 | P4 (AC): aritmetica effettiva in ℚ̄, radici di polinomi univariati, test α ∈ ℤ≥0 | metadati; contenuto del cap. 4 (o altri capitoli); fonte alternativa verificabile |
| Q3 (prio) | Cauchy–Kovalevskaya (Folland, *Intro to PDE*, cap. 1; o John) | P4-L7 passo (2): lineare coeff. costanti, forma di Kovalevskaya, dati analitici | fonte, numero (sezione/teorema), forma dell'enunciato (sistema/lineare, unicità analitica) |
| Q4 (prio) | Kato, *Perturbation Theory*, IV §5.2 | S5-L2 (iii): immagine di operatore limitato con codimensione finita è chiusa | sezione/numero; enunciato; prova autosufficiente |
| Q5 | Atiyah–Macdonald Prop. 7.14, 2.4 | C3-L2(iii) (√J f.g. ⇒ (√J)^N ⊆ J), II-T1 (trucco del determinante) | numeri ed enunciati |
| Q6 | Kato I §5.3–5.4 (Riesz) | II-T2(b), II-P5(a) | sezione |
| Q7 | Horn–Johnson *Matrix Analysis* §3.5 Cor. 3.5.6 vs 3.5.4; Thm 2.5.3 (teorema spettrale normali) | II-T7(c), II-P5(c) | già PARZIALE in AUDIT-2 (3.5.4): solo ricontrollo rapido; 2.5.3 nuovo |
| Q8 | Hörmander ALPDO II §11.4 (Petrowsky) | C3-P5(b) | sezione |
| Q9 | Kato II §1 / II §1.2 (monodromia) | lettura di II-T4 | sezione (non portante) |
Già coperte da AUDIT-2/3 e non ripetute: Rudin RCA 13.11, Lee ISM, Hörmander ALPDO I 1.4.5/2.2.x/3.1.4′, CLO cap. 3, Humphreys §4.1, Borel 14.4, Deutsch 9.35, Higham 1.12.

## 2. Skill (lette con Read; nessuno script `_vendor` eseguito)
1. `skills-local/session-protocol/SKILL.md` (per prima).
2. `_vendor/scientific-agent-skills/skills/citation-management/SKILL.md`: metadati da Crossref/OpenAlex; mai inventare pagine, volumi, numeri.
3. `_vendor/scientific-agent-skills/skills/paper-lookup/SKILL.md`: provenienza ripetibile; 200 vuoto / 403 / paywall ≠ conferma; dichiarare i vuoti.

## 3. Fonti e strumenti
Crossref API, OpenAlex, WebSearch/WebFetch (indici editoriali, note di corso, articoli arXiv che citano i teoremi con numero, zbMATH), pdftotext su PDF ad accesso aperto; nessuna copia non autorizzata. Gradi come AUDIT-3: SÌ (primaria) / SÌ (secondaria) / PARZIALE / NO; nessun numero proposto senza riscontro. Per le voci non verificabili: prova autosufficiente breve (Q1, Q4, eventualmente Q5) o fonte alternativa verificabile.

## 4. Comunicazione
PLAN-READY in inbox/central.md; alla fine TABELLA + DONE CIT-AUDIT-5. Scrivo solo in research/CIT-AUDIT/ e inbox/central.md.

## 5. Criterio di fatto
research/CIT-AUDIT/AUDIT-5.md con tabella (voce | usata in | esiste | numero/pagina | enunciato ↔ uso | fonte | azione), prove autosufficienti per le voci portanti non verificate, provenienza; TABELLA in central; DONE.
