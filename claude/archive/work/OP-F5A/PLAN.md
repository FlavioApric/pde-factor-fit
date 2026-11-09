# PLAN — OP-F5A · chiusura OPA-Q1, OPA-Q2 (+ congettura dei punti tripli), P1-Q5 dati compatibili · 26/10/2026
Skill caricate (lettura dei SKILL.md, nessuno script `_vendor` eseguito): skills-local/session-protocol, skills-local/claim-lifecycle; _vendor proof-writer (triage, mappa delle dipendenze, nessun passo nascosto), math-skill modo `proof` + sympy (solo controlli), proof-checker → CHECK_REQUEST per revisore indipendente.
Input letti: REPORT_FINALE §4.2, §6.2; claims/LEDGER.md (OPA-*, S4T-*, P1-Q5); NOTAZIONE v4; work/OP-ANA/PROOF_PACKAGE.md (punto di partenza); work/CHECK/AUDIT_OP-ANA.md; work/S4-TERM, work/P3 (quadro).

## Bersagli e strategia
1. **OPA-Q1** (tasso uniforme in t, Burgers su 𝕋). Strumenti: (a) potenziale di Laplace R(x) = −2ν log ∫e^{−(Φ_x−m)/2ν}dy, R′ = u − v, quindi ‖u−v‖_{L¹} = TV(R); (b) limiti universali su R (lemma di sottolivello con Φ⁗ = u₀‴ > 0 ⇒ ∫ ≲ ν^{1/4}); (c) lemma di Laplace riscalato (scala h = distanza dal punto di cuspide, h ≥ Kν^{1/4}); (d) monotonia di Oleinik (u − x/t, v − x/t non crescenti) per la scatola di Pearcey; (e) disuguaglianza di Kato prima dello shock: ‖u−v‖ ≤ ν TV(log J). Obiettivo: sup_{t≤t*+τ₀}‖u−v‖ = ν|log ν| + O(ν) (costante 1 universale), formula uniforme prima di t*, estensione a (0,T] per dati generici (lemma multi-pozzo + compattezza).
2. **OPA-Q2** (genericità di (H_t)). Strumenti: J = 0 in un minimizzante ⇒ u₀″ = 0 (Sard), isolamento dei punti tripli via trasversalità delle curve d'urto (pendenze di Rankine–Hugoniot distinte), esclusione dell'accumulo ai tempi A3. Esito atteso: per ogni u₀ ∈ C² (H_t) vale per q.o. t; per u₀′ di Morse (aperto denso in C^k, prevalente) l'insieme dei tempi cattivi è chiuso e discreto. Punti tripli: OPA-T1 vale sotto la sola (H_t)(i) con costante 2ν log((Σp_j)²/(p₁p_k)).
3. **P1-Q5 dati compatibili**. Strumento: coniugazione esatta D∂² − c∂ = e^{θx}(D∂² − c²/4D)e^{−θx} con Dirichlet ⇒ formula chiusa di E^mult (semiretta: −2e^{−c²t/4D} sinh(θx)∫G_{Dt}(x+y)e^{−θy}u₀(y)dy), che sostituisce l'identità di doppio commutatore. Esito atteso: ‖E^mult‖ = ‖E^{mult,(1)}‖(1 + O(t^{1/2})) = Θ(t^{k/2+3/4}) per ogni ordine di contatto k.

## Controlli (solo evidenza) — work/OP-F5A/sympy/
opf5a_q3_bordo.py (formula esatta vs serie modale; costanti N_α), opf5a_q1_burgers.py (Cole–Hopf a t*, prima e dopo), opf5a_triple.py (costante del punto triplo), opf5a_sym.py (identità simboliche).

## Fatto quando
PROOF_PACKAGE.md con ID OPF5A-*, stati onesti (PROVA SCRITTA / V-ex / APERTO / FALSO), righe LEDGER proposte; CHECK_REQUEST.md; DONE OP-F5A in inbox/central.md.

## Ripresa (26/10/2026 sera) e limite di tempo
Ripresa dopo interruzione: script e .out esistenti riusati; aggiunti opf5a_check2(.b).py (punto triplo: lo scarto 6.047 vs 6.061 di opf5a_triple.out era un artefatto della griglia in x = 0, dove i tre rami sono pari), opf5a_check3.py (decomposizione esatta di bordo con R_L; costante di Pearcey P).
**Limite di tempo dichiarato:** una sessione di lavoro (≈ 4 ore di calcolo/scrittura dalla ripresa). Ciò che non è chiuso entro il limite è consegnato come risultato parziale con ostruzione precisa (finestra post-shock di OPA-Q1 per τ ≥ K√ν: passo di uniformità; costante esatta ai punti tripli nella forma uniforme in t).
