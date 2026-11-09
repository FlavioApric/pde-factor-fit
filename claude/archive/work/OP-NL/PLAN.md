# PLAN — OP-NL · problemi aperti dell'identificazione non lineare (chiusura Fasi 4–5)
Data 26/10/2026. Agente OP-NL. Input letti: RIPRESA.md (ultimi AGGIORNAMENTI), REPORT_FINALE.md §4, §6, skills-local/session-protocol (per primo), skills-local/claim-lifecycle, NOTAZIONE.md v3–v4, PROBLEM.md (G★′-NL e precisazione S4ID-P1), claims/LEDGER.md (righe INT-*, KIEFFER-C), work/S4-ID/PROOF_PACKAGE.md (T1–T4, K1, P8), work/S4-INTEG/PROOF_PACKAGE.md (§0 fatti F1–F4, INT-T1, INT-T2, Hirota), research/F4-INT/NOTE.md (INT-P4, INT-Q1), work/CHECK/AUDIT_S4-INTEG.md, work/CHECK/AUDIT_S4-ID.md (S-CHECK-10). Cartella nuova (nessuna ripresa).

## Skill (caricate leggendo i SKILL.md; nessuno script _vendor eseguito)
1. skills-local/session-protocol: PLAN → PLAN-READY → consegna → TABELLA → DONE.
2. skills-local/claim-lifecycle: bozza → SymPy → (audit S-CHECK via CHECK_REQUEST) → riga LEDGER proposta.
3. proof-writer: per ogni claim enunciato, ipotesi, triage, mappa delle dipendenze, prova a passi, rischi.
4. math-skill (modo proof): esplorazione e caccia ai controesempi prima della prova.
5. sympy: solo controllo, in work/OP-NL/sympy/, `.venv\Scripts\python.exe -I`; non uccido processi python altrui.
6. research-lit: solo sorgente `web` (WebSearch/WebFetch in sola lettura) per F1–F4, ZS, (H-as), buona posizione di KdV in 𝒮; niente download.

## Problemi, predizioni (registrate prima di iniziare), criteri d'uscita
### P1 — INT-Q1 (priorità 1)
Domanda: KdV, u(t,·) ∈ 𝒮 per ogni t, r ≢ 0: può J_u ≠ 0?
*Predizione.* (a) Prova completa del "no" per una classe esplicita via un meccanismo elementare (non asintotico) — candidato: se un profilo u(t₀,·) non è analitico su nessun sottointervallo, J_u = 0 (le relazioni autonome minimali forzano l'analiticità tramite il teorema della funzione implicita + analiticità delle soluzioni di ODE analitiche). Probabilità alta. (b) Per dati analitici il "no" generale resta fuori portata; prevedo un'**ostruzione precisa**: l'analogo lineare (Airy) ha soluzioni di Schwartz con spettro di supporto pieno che soddisfano un'ODE autonoma ⇒ nessun argomento basato solo sull'ordine dominante (come S4ID-P8) può chiudere INT-Q1. Probabilità media (da verificare con un esempio esplicito).
*Criterio d'uscita.* Teorema con prova completa per una classe esplicita di dati di Schwartz con r ≢ 0 **oppure** controesempio; per il resto, ostruzione documentata con un enunciato dimostrato che la giustifichi.

### P2 — S4ID-K1 (priorità 2)
Congettura: gli N-shock di Burgers non hanno relazioni autonome di grado ≤ N a nessun ordine.
*Predizione.* Dimostrabile riducendo, tramite i momenti (T2(II)) e un grading per pesi, al caso confluente (logaritmi derivati di polinomi di grado N ⇒ somme di potenze di N variabili), dove l'indipendenza dei p_μ con ℓ(μ) ≤ N segue dalla triangolarità p → m. Probabilità medio-alta.
*Criterio d'uscita.* Prova completa di K1 (→ criterio esatto del dizionario evolutivo per ogni K) o controesempio esplicito verificato.

### P3 — S4ID-T3 (priorità 3)
Grado di Π_N e criterio completo per KdV.
*Predizione.* deg Π_2 = 8 indipendente da k (dimostrabile per k generico; per ogni k con calcolo simbolico nei parametri); deg Π_N in generale: congettura da formulare (evidenza N = 3 solo se il calcolo è fattibile). Criterio completo: probabilmente solo parziale (tabella δ_N(K) V-ex per N = 2, risultati strutturali).
*Criterio d'uscita.* (i) deg Π_N costante su un aperto di Zariski dei k (prova), (ii) N = 2 con parametri simbolici, (iii) criterio per KdV ridotto alla funzione δ_N(K) con i valori dimostrati e il resto V-ex/APERTO; oppure ostruzione documentata.

### P4 — condizionali di S4-INTEG (F1–F4, ZS, H-as)
*Predizione.* Le fonti classiche si individuano (Deift–Trubowitz CPAM 1979; Lax 1968; Kay–Moses 1956; Beals–Coifman 1984; Zhou 1989; Grunert–Teschl 2009) ma i testi non sono leggibili (rete): stato al più "metadati verificati". In parallelo: dimostrare direttamente le parti che non richiedono la teoria dello scattering completa (p.es. INT-T2 per i multi-solitoni di NLS via analiticità e indipendenza, come Lemma B1 per KdV).
*Criterio d'uscita.* Per ciascun fatto: fonte (enunciato e numero) verificata, oppure prova diretta, oppure stato invariato con il motivo preciso.

## Contatti
central (PLAN-READY, TABELLA, DONE); S-CHECK tramite CHECK_REQUEST.md autosufficiente. Scrivo solo in work/OP-NL/ e inbox/.

## Consegne
work/OP-NL/PLAN.md, PROOF_PACKAGE.md (incrementale), CHECK_REQUEST.md, sympy/ (script + .out).
