# PLAN — S-TROP (scout di Fase 3, route-scout su [TROP-L2] = RT-S1a ∪ RT-S2b) · 25/10/2026

## Skill caricate (lettura integrale del SKILL.md, nessuno script _vendor eseguito)
1. `skills-local/session-protocol` (per prima) — piano, inbox, consegna, DONE.
2. `skills-local/route-scout` — procedura: domanda decisiva → caso di prova minimo → verdetto di una pagina → proposta promote/park/merge-into/kill rispetto ai criteri GIÀ fissati (ROUTES.md righe RT-S1a, RT-S2b; ATTACK.md §3).
3. `_vendor/math-skill` modo `proof` (+ references/proof-playbook.md) — prima falsificare, poi provare; separare esplorazione e prova.
4. `_vendor/scientific-agent-skills/skills/sympy` — verifiche simboliche in `work/SCOUT-TROP/sympy/` con `.venv\Scripts\python.exe -I`.
5. `_vendor/Auto-claude-code-research-in-sleep/skills/novelty-check` — fasi A, B (WebSearch), D; fase C (revisore Codex) esclusa per decisione dell'utente → REVIEW_UNAVAILABLE, giudizio sotto i "verdict limits".
6. `skills-local/claim-lifecycle` — solo per formattare le righe LEDGER proposte (gli stati restano V-ex/DIMOSTRATO-bozza finché S-CHECK non audita).

## Criteri fissati PRIMA (non modificabili)
- Promuovi se: (a) teorema dei limiti di scala verso le forme iniziali estreme, con tasso; (b) "vertice ⇔ classe propria"; (c) ‖E_int‖/‖u‖ = O(ε^γ) con ε letto dal simbolo (Péclet per AD, m per KG).
- Merge in RT-2 se: la stima (c) non regge, oppure contano solo i vertici estremi.

## Domanda decisiva
Esiste una stima ‖E_int‖/‖u‖ = O(ε^γ), con ε funzione del SOLO simbolo, per la scomposizione a bande di [TROP-L2], su avvezione–diffusione (AD) u_t + c u_x = D u_xx e Klein–Gordon (KG) u_tt − u_xx + m²u = 0? Se no, quale parametro serve e la scomposizione batte l'approssimazione con la sola parte principale?

## Enunciati da affrontare (appunti A5, A6, A8, A9, D1; item C4, P1)
- TROP-1 limiti di scala AD (t→0 diffusione, t→∞ trasporto) con tasso esatto (W₁ del nucleo riscalato).
- TROP-2 limiti di scala KG (alta frequenza → onda; bassa → oscillatore + modulazione Schrödinger), tasso.
- TROP-3 stima uniforme in t sulle bande a faccia dissipativa (ε = rapporto dei tassi, γ = 1), con ottimalità.
- TROP-4 ostruzione sulle facce conservative (KG; banda trasporto di AD): nessuna stima uniforme in t (media di Cesàro → 2).
- TROP-5 stima su orizzonte T: ε = T·(tasso subdominante), γ = 1, ottimale; punto di rottura ottimo = κ* del poligono.
- TROP-6 caso peggiore: la scomposizione a bande non migliora l'ordine rispetto alla sola parte principale (vertice estremo).
- TROP-7 Ω limitato: poligono 2D di τ + cξ − Dξ² ha una terza faccia cξ − Dξ² (strato limite e^{cx/D}); controesempio con E_rel indipendente da Pe; non-intrinsecità delle bande (rappresentazione di Ehrenpreis non unica).
- TROP-8 vertice medio (L3, u_t + cu_x = Du_xx − βu_xxx): esiste una banda propria sse D² > cβ; è l'unica con stima uniforme (diffusione in mezzo).

## Caso di prova minimo
AD su ℝ (Fourier) e su Ω = (0,T)×(0,L) con soluzione esponenziale; KG su ℝ, modo per modo.

## Fonti
SCOUT-1 Addendum, SCOUT-2 §S2-B, ATTACK.md O1/§3, R5 (R5-T2), PR-C2b P1/P4, PR-C2d §4. Letteratura (novelty-check): Bender–Orszag (dominant balance), Reddy–Trefethen 1994 (pseudospettri AD), Masmoudi–Nakanishi 2002 (limite non relativistico KG), Donoho–Kutyniok 2013.

## Contatti
- S-C1C2: AVVISO/TABELLA su O1/G8 e faccia "strato limite" su Ω limitato (DOMANDA: la scomposizione per fattori su H^m(Ω) la vede?).
- S-P1: TABELLA con le stime di E_int per regime (TROP-3/4/5) da usare nella definizione di E_int per quadro.
- Inbox S-TROP letta all'inizio (vuota), a metà, prima di consegnare.

## Fatto quando
VERDETTO.md (1 pagina, formato route-scout) + sympy/ con esiti PASS + proposta in inbox/central.md + righe LEDGER proposte + DONE S-TROP.
