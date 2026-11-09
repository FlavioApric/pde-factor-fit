# PLAN-F5 — CIT-AUDIT-F5 (chiusura Fase 5: fonti CON-FONTE / CONDIZIONALE dei problemi aperti)

Data: 2026-10-26 · Agente: CIT-AUDIT-F5 (nome di file -F5 per non collidere con il CIT-AUDIT-6 della sessione fork) · Metodo: come AUDIT-5 §0 (gradi SÌ primaria / SÌ secondaria / PARZIALE / NO; nessun numero proposto senza riscontro).
Input: RIPRESA.md (ultimi AGGIORNAMENTI), claims/LEDGER.md (righe S4T-*, OPA-*, OPF-*, OPR2-*, OP-*, S4ID-P8, INT-T1/T2), work/OP-ANA, OP-ALG, OP-FUN, OP-NL, OP-R2, S4-TERM (PROOF_PACKAGE: sezioni fonti e dipendenze).

## 1. Voci (priorità: quelle che reggono uno stato CONDIZIONALE o CON-FONTE)
| # | voce | usata in | stato che regge | cosa verificare |
|---|---|---|---|---|
| A1 (prio) | [F1] Lax–Oleinik = soluzione entropica di Kružkov (Evans PDE §3.4, §11.4; Kružkov Mat. Sb. 81 (1970)) | S4-TERM [F1], S4T-L2, S4T-T3; OPA-T1 | DIMOSTRATO mod [F1] | sezioni di Evans 2ª ed.; enunciato (periodico, L^∞, q.o. x); metadati Kružkov |
| A2 (prio) | [F3] Kuznetsov 1976, tasso √ν in L¹ | S4T-T3(iv),(v) | CONDIZIONALE [F3] | metadati (rivista, volume, pagine, DOI), forma della stima |
| A3 | Tang–Teng, Math. Comp. 66 (1997) 495–526 | OPA-R1, S4T-T3(vi), letteratura OPA-T1 | osservazione/letteratura | metadati, enunciato (ε|log ε| ai tempi di formazione; O(ε) senza) |
| A4 (prio) | Turán–Nazarov (Nazarov, St. Petersburg Math. J. 5 (1994) 663–717; arXiv 1107.0039) | OPA-T3(e) | CONDIZIONALE [Naz] | metadati, forma della disuguaglianza per somme esponenziali con frequenze complesse, costante |
| A5 (prio) | (WP) KdV ben posta in 𝒮 (Bona–Smith 1975; Kato 1983; GGKM; Marchenko) | OP-C3′ | DIMOSTRATO mod (WP) | metadati Bona–Smith, enunciato per dati di Schwartz |
| A6 | Novikov 1974 (equazione stazionaria degli N-solitoni), Lax 1975 | OPR2-P4, S4ID-T3(d) | mod Novikov CON-FONTE | metadati; enunciato (N-solitone soddisfa equazione di Novikov di ordine N) |
| A7 | Kay–Moses 1956 (senza riflessione; autovalori −κ_j²) | OP-C3′ (osservazione), corollario di OP-P17 | CON-FONTE non portante | metadati, enunciato |
| A8 (prio) | AKNS 1974; Beals–Coifman (Jost di ZS); Zhou CPAM 42 (1989) | OP-P18 (n ≥ 4), INT-T2 | CONDIZIONALE [(ZC)] | metadati, data Beals–Coifman, enunciato |
| A9 (prio) | Grunert–Teschl 2009 (arXiv:0807.5041), Lemma 2.2, Thm 5.4; Deift–Zhou | S4ID-P8, OP-NL F1/F2/F3/(WP), OPR2 (SR) | CONDIZIONALE | numerazione su arXiv/rivista, enunciato; metadati Deift–Zhou |
| A10 (prio) | Lax 1968 / Gelfand–Dickey 1975 (identità di Lax ∀n) | OP-P17 (n ≥ 4) | CONDIZIONALE [(Lax)] | metadati; forma B_n = (L^{(2n+1)/2})_+ |
| A11 | Runge (polinomi sull'inviluppo polinomiale; Rudin RCA cap. 13) | OPF-P4(b)(i) | CON-FONTE | sede in Rudin (Thm 13.7/13.9?) — non proporre numeri senza riscontro |
| A12 | Hörmander ALPDO II §10.6–10.7; SCV Thm 1.4.4; Rudin RCA cap. 13 | OPF-T4 (iii),(iv)(c),(d) | CON-FONTE | indici (ALPDO II cap. X; SCV cap. I) |
| A13 | Adams–Fournier (densità di C^∞(Ω̄) per domini con proprietà del segmento) | OPF-L3/T5 | CON-FONTE | numero del teorema (3.22?) |
| A14 | Stein, Singular Integrals cap. VI §3 (operatore d'estensione) | OPR2-T1 (estensione) | CON-FONTE | sede |
| A15 | ipoellitticità del calore (Hörmander ALPDO II cap. 11) | OPR2-T1 passo 1 | CON-FONTE | sede (11.1) |
| A16 | Pazy §6.3; Henry cap. 3 (LWP + alternativa di blow-up) | OPR2-T5 | mod (LWP) | indici |
| A17 | Oaku–Takayama–Tsai arXiv:math/0001064 | OP-ALG letteratura | non portante | sede (JPAA 2001?) |
| A18 | DLMF 9.7 (asintotica di Airy) | OP-O5 | DIMOSTRATO mod DLMF 9.7 | eq. 9.7.9–9.7.11 |
| A19 | Hundsdorfer–Verwer 2003 cap. IV; Einkemmer–Ostermann 2015 | OPA letteratura (P1-Q5) | non portante | metadati, contenuto (riduzione d'ordine degli splitting) |

## 2. Skill (lette con Read; nessuno script `_vendor` eseguito)
1. `skills-local/session-protocol/SKILL.md`.
2. `_vendor/scientific-agent-skills/skills/citation-management/SKILL.md` (metadati da Crossref/OpenAlex; mai inventare pagine/volumi/numeri).
3. `_vendor/scientific-agent-skills/skills/paper-lookup/SKILL.md` (provenienza ripetibile; 200 vuoto / 403 / paywall ≠ conferma; dichiarare i vuoti).

## 3. Fonti e strumenti
Crossref API, arXiv (abs/PDF ad accesso aperto, pdftotext se disponibile), DLMF (sito ufficiale), WebSearch/WebFetch per indici editoriali, zbMATH/MathSciNet pubblici, note di corso. Nessuna copia non autorizzata. Temporanei nello scratchpad con prefisso citf5_.

## 4. Comunicazione
PLAN-READY CIT-AUDIT-F5 in inbox/central.md; alla fine TABELLA + "DONE CIT-AUDIT-F5". Scrivo solo in research/CIT-AUDIT/ (file -F5) e inbox/central.md. Le azioni sui claim sono proposte al coordinatore (non modifico LEDGER né i package).

## 5. Criterio di fatto
research/CIT-AUDIT/AUDIT-F5.md con tabella (voce | usata in | esiste | numero/pagina | enunciato verificato | fonte | azione: stato del claim da aggiornare) e provenienza; TABELLA in central; DONE.
