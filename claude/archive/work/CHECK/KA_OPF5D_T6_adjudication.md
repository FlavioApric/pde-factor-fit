# KA OPF5D-T6 — aggiudicazione (S-CHECK-17, 26/10/2026)
Input: KA_OPF5D_T6_input.md. Attacco: KA_OPF5D_T6_attack.md (subagente fresco, con un controllo numerico proprio per u_0 = sin x e u_0 = 0,5 + sin x, t = 2, ν = 0,1 … 0,003, in cui il rapporto errore/limite va da 0,05 a 0,009). Aggiudicatore: S-CHECK-17, che ha ricontrollato i passi (1)–(5) a mano: costante finale, verso di Jensen, scambio di Tonelli con la periodicità, caso di media non nulla.

**Esito: SOPRAVVISSUTO.** Il kill-argument non trova obiezioni alla stima principale. L'unica obiezione residua (MINOR) riguarda il corollario (6).

| punto dell'attacco | verdetto | riparazione |
|---|---|---|
| (6): Θ(√ν) e (v) dipendono da S4T-T3(iii),(vi), che non sono nell'input | **parzialmente fondato, MINOR** (= F5D-9) | Ho controllato S4-TERM: S4T-T3(iii) non usa [F3]. Dà il limite inferiore 2D√(t/π) con le ipotesi u_0 ∈ C^∞ non costante e t > t*. Il corollario va quindi enunciato con queste ipotesi, non con «u_0 ∈ C¹». Anche (v), tramite (vi), richiede u_0 ∈ C². Inoltre E^{mult}_{AB} è definito con S_B: l'identificazione S_B = Lax–Oleinik è T7, mod [K-U], che ora è CON-FONTE verificata. |
| refuso ‖u_0′‖ senza pedice ∞ | cosmetico | — |

Osservazione: il limite O(√ν) per ‖u − v‖_{L¹} non è stretto. Sia la numerica dell'attacco sia burgers_l1 danno O(ν), coerentemente con S4T-Q1. T6 non pretende l'ottimalità, quindi questo non è un difetto.

**Stato:** T6 è OK con fix MINOR e il kill-argument è sopravvissuto. Stato proposto: **DIMOSTRATO**. Il corollario S4T-T3(iv) senza [F3] vale con le ipotesi di S4T-T3 e S_B come in T7.
