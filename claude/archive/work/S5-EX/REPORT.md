# REPORT — S5-EX · Fase 5 (verifica sugli esempi da manuale) · 26/10/2026
(Ricostruito dal coordinatore: il subagente della sessione parallela non ha potuto scrivere questo file e il testo integrale non è stato conservato. Fonti: PLAN.md, script e output in work/S5-EX/sympy/, TABELLA in inbox/central.md.)
**Mandato (piano, Verifica Fase 5):** controllare la teoria sugli esempi noti: calore, Airy, Bessel, trasporto + diffusione con E_int.
**Esito:** 150/150 controlli OK (ex1_calore, ex2_AD, ex3_due_fattori, ex4_airy, ex5_bessel). Nessun CONFLITTO con il LEDGER.
| riga proposta | esempio | teoremi controllati | stato |
|---|---|---|---|
| EX-CAL | calore | C3-T1/T3/T4/T6, P4-T2 | V-ex |
| EX-AD | trasporto + diffusione con E_int | P1-T2/T3, P2-T2 (span{1, x−ct, (x−ct)²+2Dt} è P2-T2, non P2-T1), P3-T3 | V-ex |
| EX-CT | calore × trasporto | C12-T1′, OPR2-T1 | V-ex |
| EX-AIRY | Airy (PDE ed EDO) | C3-T4, P3-T1 | V-ex |
| EX-VAR | coefficienti variabili | P4-C1, OP-ALG-T4, OPR2-T3 | V-ex |
| EX-BES | Bessel (nucleo radiale u = t⁻¹e^{−x²/4t}, P_r u = 0; J_0′/J_0 non razionale; u ∉ 𝒯 su box(3,3) V-ex; Dyson–Phillips converge solo per r₀ > 0) | OP-ALG-T4, P3-T1 | V-ex |
**Precisazioni segnalate:** (1) la riga P1-Q5 "altrimenti O(t²)" va allineata a OPA-T2(iii): osservato t^{9/4} con costante esatta; (2) P3-T1(a) non copre termini dispersivi del 3° ordine; (3) C3-T3(iii): e^{−4t}sin 2x è un esempio naturale in cui 2d−2 non basta; (4) span{1, x−ct, (x−ct)²+2Dt} è P2-T2.
**Nuovo aperto minore:** EX-Q1 — OP-ALG-T4 per P non monico in ∂_t (caso Bessel radiale).
