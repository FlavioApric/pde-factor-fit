# PLAN — OP-F5B · chiusura Fase 5 (prima esecuzione effettiva) · 26/10/2026
Mandato: OPR2-Q2′, OPF-Q3, OPR2-Q3, EX-Q1. Per ciascuno: prova completa, controesempio, o risultato parziale con ostruzione precisa.
**Limite di tempo dichiarato:** una sessione (questa), circa 4 ore-agente; ciò che non si chiude entro il limite esce come PARZIALE con ostruzione scritta.

## Skill (ordine d'uso)
1. skills-local/session-protocol (letta per prima) — piano, inbox, consegne.
2. skills-local/claim-lifecycle — stati: tutto il nuovo esce come PROVA SCRITTA; audit S-CHECK a valle (CHECK_REQUEST.md).
3. _vendor/.../proof-writer/SKILL.md — triage, mappa delle dipendenze, prova o rapporto di blocco.
4. _vendor/math-skill/SKILL.md (modo proof) — esplorazione separata, controesempi presto.
5. _vendor/scientific-agent-skills/skills/sympy/SKILL.md — controlli in work/OP-F5B/sympy/ (python -I, timeout, prefisso opf5b_). Nessuno script _vendor eseguito.

## Domande e strategia
| ID | domanda | strategia prevista | criterio di fatto |
|---|---|---|---|
| OPF-Q3 | densità di Σ ker_{H^m}Q_j in ker_{H^m}P per la trave sul parallelogramma caratteristico | **non** per simmetrie (OPF-T5 fallisce: (C) falsa); traslazioni **locali** verso l'interno (come OPR2-T1) ma con correzione per **P intero**, non fattore per fattore: soluzione fondamentale di Hörmander di classe P̃ (CON-FONTE) che guadagna esattamente quanto perde il commutatore [P,θ] (|P^{(α)}| ≤ P̃). Atteso: teorema per ogni P a coefficienti costanti su ogni convesso limitato, ogni m. | prova scritta + SymPy (Leibniz, temperanza di P̃, geometria delle traslazioni) |
| EX-Q1 | OP-ALG-T4 per P non monico (Bessel radiale P_r = x∂_t − ∂_x x ∂_x) | (i) forma saturata di T4 per P qualsiasi (Ann ⊆ 𝔎P); (ii) coefficiente direttore funzione π(x): localizzare in π, T4 per P̂ monico, e criterio "M senza π-torsione"; (iii) Bessel: x-torsione nulla (azione destra su 𝒟/x𝒟), nucleo gaussiano identifica. | teorema + verifica |
| OPR2-Q3 | zoccolo ripetuto: "nessun test finito" in generale, con soluzioni che realizzano gli atomi | riduzione: soluzioni u_R = R u* da endomorfismi di M = 𝔇/𝔇P e una soluzione identificante u*; L_{u_R}/𝔇P = ker E_R. Classe dimostrabile: M = M_1 ⊕ M_2 con J: M_1 → M_2 iniettivo. Ostruzione residua: sollevamento degli endomorfismi da 𝔎 a 𝔇, esistenza di u*. | teorema nella classe + ostruzione |
| OPR2-Q2′ | N = 3, coppie chiuse, tripla non chiusa (cuneo) | modello tangente: cono infinito, trasporti omogenei; trasformata di Mellin ⇒ fibre di dimensione 1; indipendenza delle potenze (n_j·ω)^{−1+iσ} e fase non stazionaria ⇒ somma chiusa nel modello. Ostruzione: localizzazione al poligono limitato (Fredholm modulo vertici); ordine ≥ 2. | teorema nel modello + ostruzione |

## Fonti
work/OP-R2, work/OP-FUN, work/OP-ALG (§4), work/C1C2 (C12-T1′, C12-P7), work/S5-EX; audit AUDIT_OP-R2, AUDIT_OP-FUN. Classici: Hörmander ALPDO II cap. 10 (soluzione fondamentale in B^{loc}_{∞,P̃}), Stein (estensione), Ore/localizzazioni (McConnell–Robson) — CON-FONTE, numeri non verificati.

## Contatti
inbox/central.md (PLAN-READY, TABELLA, DONE). Eventuale CONFLITTO se il teorema di densità generale contraddice un claim registrato (atteso: lo estende, OPF-T5/OPR2-T1 diventano casi particolari).

## Consegne
PROOF_PACKAGE.md (incrementale), CHECK_REQUEST.md, TABELLA LEDGER + DONE OP-F5B in inbox/central.md.
