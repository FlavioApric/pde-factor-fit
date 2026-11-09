# KA OPF5A-T2 / Lemma U — aggiudicazione (S-CHECK-20, 26/10/2026)
Attacco: KA_OPF5A_U_attack.md. Esito: **SURVIVES** (nessun regime di τ cattivo; GAP solo di presentazione).
Accolti: (1) coefficiente quadratico di Ψ_τ è −A²/(2tt*) (→ −A²/(2t*²)); resto O(√τ|A|⁵+τA²) [F5A-4, MINOR]; (2) il trasferimento di L3 a una famiglia astratta compatta di potenziali non è enunciato come lemma [F5A-5, MINOR: va scritto L3′, la prova di L3 si applica parola per parola]; (3) le stime dei momenti di L2(c) per t>t* nella regione esterna non sono scritte (seguono da ψ≥(c1/2)(z⁴+α²z²) per |z|≤z0 + margine per |z|≥z0, che per t>t* NON viene dalla convessità ma dal margine di OP-ANA Lemma 1(iii)/3) [F5A-6, MINOR].
Ordine delle costanti (K'(b) → Ξ → ν̂0 → K1 → K'(a)) verificato: non circolare.
Numerica: attaccante (u0=−sin y−ε sin2y, ε=0 e 0.3, ν=1e-4..1e-6, τ/√ν∈[0.3,100]): D∈[1.67,3.09]; aggiudicatore (s20_opf5a (3), sin): D post-shock ∈[2.80,3.08], pre-shock ∈[0.84,1.37], stabile in ν a K fisso.
**Verdetto: SURVIVES; T2 da PROVA SCRITTA a DIMOSTRATO mod [F1] dopo i fix F5A-4..6.**
