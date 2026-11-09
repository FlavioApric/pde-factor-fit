# PLAN — OP-R2 (secondo giro sui problemi aperti residui) · 26/10/2026

**Skill caricate** (lettura dei SKILL.md; nessuno script _vendor eseguito): skills-local/session-protocol (per primo), skills-local/claim-lifecycle; _vendor/Auto-claude-code-research-in-sleep/skills/proof-writer (per ogni claim: enunciato normalizzato, ipotesi, triage PROVABLE / AFTER WEAKENING / NOT JUSTIFIED, dipendenze, prova a passi, rapporto di blocco se serve); _vendor/math-skill (modo proof: controesempi e casi limite prima, esplorazione separata dalla prova); _vendor/scientific-agent-skills/skills/sympy (controlli simbolici, solo controllo); _vendor/Auto-claude-code-research-in-sleep/skills/research-lit (nessuna ricerca web eseguita: le fonti sono quelle già citate nei package o classiche, marcate CON-FONTE con "numero non verificato").
**Input letti:** RIPRESA.md (ultimi aggiornamenti), REPORT_FINALE.md (indice), NOTAZIONE v4, PROBLEM.md, claims/LEDGER.md (righe pertinenti), work/OP-FUN §3–§4, work/OP-ALG §3–§4, work/CHECK/AUDIT_OP-ALG.md (OA-1, OB-1), work/P4 (P4-T5, P4-L7), work/OP-NL §1, §3, work/S4-TERM §2, §5, §7.
**Escluso** (in carico a OP-ANA): S4T-Q1, P3-Q-bordo, P1-Q6, P1-Q5.
**Scrittura:** solo work/OP-R2/ e inbox/. SymPy: `D:\ProblemaBase\.venv\Scripts\python.exe -I work/OP-R2/sympy/opr2_checks.py` (nessun processo altrui toccato).

## Problemi, predizione, criterio d'uscita, limite di tempo
| # | problema | predizione (prima di lavorare) | criterio d'uscita | limite |
|---|---|---|---|---|
| 1 | **OPF-Q1** densità per calore × trasporto in H^m(rettangolo) | VERA: il difetto è locale nei due angoli dove le corde del trasporto degenerano; lì una traslazione verso l'interno è una simmetria di P; il trasporto si incolla con tagli in s (commutano con il trasporto), il calore con una correzione parabolica (guadagno di una derivata) | prova completa per ogni m e ogni rettangolo; oppure rapporto di blocco con il passo mancante | 90 min |
| 2 | **OPF-Q2 = C12-Q2** (3 fattori, coppie chiuse, tripla non chiusa) nel candidato "due paralleli + uno trasversale" | NO nel candidato: tra famiglie di direzioni diverse il prodotto dei proiettori è Hilbert–Schmidt, quindi S*S = I + compatto (Fredholm) | teorema per la famiglia dei trasporti reali del 1° ordine (m = 0, Ω convesso) + residuo preciso | 60 min |
| 3a | **OP-ALG-Q1** coeff. variabili, fattori a due a due non simili ⇒ test finiti? | SÌ: gli ideali saturati minimali (atomi) corrispondono ai sottomoduli semplici di 𝔎/𝔎P (𝔎 = Frac(𝔄)[∂_t;δ]); fattori non simili ⇒ socle senza molteplicità ⇒ finiti atomi | criterio con r ≤ m test + direzione inversa (socle con molteplicità ⇒ infiniti atomi) | 45 min |
| 3b | **OP-ALG-Q2** T3(f) per ogni dominio | SÌ: serve P4-L7 globale; dati di Cauchy interi d'ordine < 1 a coefficienti di Taylor razionali danno soluzioni intere | P4-L7 globale + T3(f) per ogni (Ω, p₀) | 30 min |
| 4 | **OP-K15 / δ_N** | difficile; atteso solo parziale: δ_N(2N) ≤ N+1 dall'equazione di Novikov integrata una volta | parziale dimostrato + ostruzione precisa | 40 min |
| 5 | **S4T-Q2** resto per KdV–Burgers | chiudibile: il termine dispersivo è antisimmetrico in L², stime d'energia H^k + bootstrap | stima ‖u − v − νδ − dδ_d‖_{H^k} ≤ C(ν+|d|)² su [0,T], T < t* | 60 min |
| 6 | **INT-Q1 per dati analitici** | resta APERTO; parziali: nessuna relazione d'ordine ≤ 1 (r ≢ 0); un solo autovalore: J_u ⊆ J_soliton (condizionale); ostruzione algebrica (soluzioni autosimili hanno J_u ≠ 0) | parziali dimostrati + ostruzione documentata | 45 min |

## Metodo per claim
proof-writer (enunciato, ipotesi, prova) → SymPy di controllo (identità algebriche, formule chiuse, casi limite) → passaggio avversariale in linea → riga LEDGER proposta con stato PROVA SCRITTA (nessun DIMOSTRATO prima dell'audit) → CHECK_REQUEST.md autosufficiente.

## Fatto
PROOF_PACKAGE.md con esito per problema (chiuso / parziale + ostruzione precisa), sympy/opr2_checks.py con output, CHECK_REQUEST.md, TABELLA LEDGER in inbox/central.md, "DONE OP-R2".
