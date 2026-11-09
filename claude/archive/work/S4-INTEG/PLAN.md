# PLAN — S4-INTEG (Fase 4, sessione corta) · 26/10/2026
Scheda: SESSIONS.md, Roster della Fase 4, "S4-INTEG". Obiettivo: punto 3 di G★′-NL (trasporto dei risultati lineari), cioè i lemmi di trasporto emersi dallo scouting portati a prova completa pronta per l'audit, con **riduzione classica** (DEVIL-4 O3) e **modello di dato + dominio** (O4) dichiarati.

## 1. Lemmi da trattare (ID degli scout; appunti A9, G4, G7; item C3/P1)
| ID | fonte | contenuto | dominio previsto |
|---|---|---|---|
| INT-T1 | research/F4-INT/NOTE §1 | KdV in 𝓗_M: ambiguità = max(0, M+1−\|Λ(u)\|) | I×ℝ; Ω limitato via UC (Saut–Scheurer: solo flusso vero d'ordine 3) o via analiticità (N-solitoni) |
| INT-T2 | F4-INT §1 | NLS in 𝓗_M^NLS | I×ℝ (condizionale) |
| F4LIN-T2 | F4-LIN §4 | log-sum-exp, 4ν ln 2 per shock, L^p/Ḣ^s, (iii) K shock | ℝ a t fisso (dato M1: miscele finite di onde) |
| F4L-P3 | F4-LIFT §B | raggio in ampiezza ≥ 2πν/osc(U₀), ottimale | ℝ e (nuovo) intervallo limitato con u = 0 al bordo (Neumann per φ) |
| Hirota (INT-P5, INT-P6) | F4-INT §3 | E_int = 2∂²log Z a coppie; ∫E_int dx = 0; costo O(N³) | ℝ (P6 intrinsecamente su ℝ) |
| ALG-L1, ALG-T1, ALG-P3, ALG-P4, ALG-P6 | F4-ALG §2, §5 | [F] primo; I(u) = [F] ⟺ trdeg = ∞ (u analitica); trasporti Cole–Hopf, Miura | Ω aperto connesso qualsiasi (limitato incluso) |
| MODREL-T1 | F4-HOR §1 | rango 1 + relazione primitiva ⇒ Syz = R·v; corollario d = 2 | Ω aperto qualsiasi |

## 2. Predizione (scritta prima di iniziare, DEVIL-4 O6)
- Tutti i lemmi tranne INT-T1(a,b) generale e INT-T2 diventano DIMOSTRATO-pronti con prova elementare (corollari di fatti classici: Gauss/gcd, zero generico + separante, log-sum-exp, profilo tanh, determinante di Cauchy, lemma della striscia dei cumulanti).
- F4L-P3 **è** un caso del lemma della striscia dei cumulanti (Re E e^{sX} > 0 per |Im s|·w < π): lo dimostro così; la novità residua è solo il raggio esplicito uniforme in t e la correzione di Kieffer et al.
- INT-T1: la parte N-solitoni (c) si prova senza scattering (fasi del multi-solitone + indipendenza delle ∂_{c_j}u); la parte con radiazione resta **condizionale** a F1–F3 (IST, fonti non lette). UC: Saut–Scheurer basta quando il flusso VERO è d'ordine 3 (perché w = K_d[u] risolve la linearizzazione del flusso vero), per qualsiasi M della classe.
- Nessun FALSO atteso; possibili correzioni d'enunciato (ipotesi di analiticità, segni, k_i > 0).

## 3. Criterio d'uscita
Ogni lemma ha uno stato ∈ {DIMOSTRATO-pronto (prova completa qui, in attesa di S-CHECK), CON-FONTE (enunciato identico pubblicato e verificato), FALSO (controesempio)}; dove una prova dipende da fatti classici NON verificati sulla fonte lo stato è "CONDIZIONALE a F…" (dichiarato come uscita onesta, non DIMOSTRATO). Più: CHECK_REQUEST.md autosufficiente, DOMANDA in inbox/S-CHECK.md, TABELLA a S4-TERM e S4-ID, TABELLA LEDGER in inbox/central.md, DONE S4-INTEG.

## 4. Skill (in ordine d'uso; caricate leggendo i SKILL.md, nessuno script _vendor eseguito)
1. skills-local/session-protocol (per prima) — piano, inbox, consegne.
2. skills-local/claim-lifecycle — stati e riga di LEDGER; audit delegato a S-CHECK (CHECK_REQUEST).
3. _vendor/Auto-claude-code-research-in-sleep/skills/proof-writer/SKILL.md — struttura Claim/Status/Assumptions/Strategy/Dependency/Proof/Risks per ogni lemma.
4. _vendor/math-skill/SKILL.md (modo proof) — mappa, controesempi presto.
5. _vendor/scientific-agent-skills/skills/sympy/SKILL.md — verifiche in work/S4-INTEG/sympy/ con D:\ProblemaBase\.venv\Scripts\python.exe -I (solo controllo).

## 5. Fonti
research/CIT-AUDIT/AUDIT-4.md (Saut–Scheurer, Kieffer et al., Scholl et al., Wang 1998, Kay–Moses, Miura, Hopf, Cole); research/DEVIL/ATTACK-4.md (O3, O4) e sympy4/radius_checks.py. Eventuale lettura di arXiv:2512.12019 per il confronto di costanti (solo lettura).

## 6. Contatti
S4-TERM, S4-ID (inbox: leggere all'inizio, a metà, prima della consegna; TABELLA degli enunciati finali), S-CHECK (DOMANDA), central (PLAN-READY, LEDGER, DONE).
