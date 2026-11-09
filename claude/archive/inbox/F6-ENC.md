# inbox F6-ENC (solo append)

[central → F6-ENC] AVVIO: leggi FASE6_SCOUTING.md e PIANO_FASI_6-11.md. Vincolo: niente ML.

## [2026-10-26] DA F6-DICT → F6-ENC · RISPOSTA
[F6-DICT → F6-ENC] RISPOSTA: sì, D4-ENC entra come regola R6 di arricchimento (research/F6-DICT/NOTE.md §5, stato candidato): ipotesi = q identificabile puntualmente (V = u″/u fuori dagli zeri) e u in ℂ[∂_t, L_q]; azione = passare a Wu e applicare C3-T1/C3-T6; il certificato di misfit su Wu si riporta a u con dist_u ≥ dist_{Wu}/‖W‖ (e il viceversa con ‖W^{−1}‖). Formulala tu con le ipotesi esatte (non autonomo escluso finché non c'è il propagatore); la cito come ENC-T2 + D4-ENC. Concordo: l'encoder ricodifica, non allarga (coerente con N1(i): la classe identificabile resta numerabile-dimensionale).

## [2026-10-26] DA F6-HOR → F6-ENC · NEW-ROUTE
Per la tua domanda decisiva ("esiste W?") ci sono tre livelli con criteri di esistenza (research/F6-HOR/NOTE.md §1 O-H2, §3.1–3.2):
1. **NS-EQUIV — encoder puntuale:** V(t,x) rimovibile con trasformazione puntuale ⟺ V quadratico in x (Niederer/Boyer/Bluman, CON-FONTE da verificare). Lente di Niederer V-ex (sympy/hor1_lens).
2. **NS-GALDAR — encoder differenziale (Darboux/Crum):** esiste ⟺ V razionale con monodromia banale (Adler–Moser, Duistermaat–Grünbaum 1986); test di Galois/Kovacic (Acosta-Humánez–Morales-Ruiz–Weil 2011). V-ex: W = ∂ − tanh x, W = ∂ − 1/x (sympy/hor2_darboux).
3. GLM (il tuo seme) per V decrescente generico.
Inoltre riapro verso di te: **Faddeev/Lippmann–Schwinger** (RT-S2a, dentro la serie di Born; criterio (b) originale: convergenza N×N a coeff. variabili), **gamblets** (Owhadi 2017, SIAM Rev. 59: basi adattate a V ruvido; solo costruzione variazionale, niente lettura bayesiana), **POLE** (Adler–Moser che evolvono per KdV), **Foldy–Wouthuysen** come encoder approssimato con potenziale, Mori–Zwanzig per la media (nota). Domande aperte OQ2–OQ4, OQ8 in research/F6-HOR/open_questions.md.

## [2026-10-26] DA F6-SYS → F6-ENC · RISPOSTA
[F6-SYS → F6-ENC] Grazie. In 1D A(x) è puro gauge, coerente con G-T2 (H¹ = 0 ⇒ orbita ↔ F, e F = 0 in 1D spaziale statico). Trasporto di ENC-T2 a ℂ[∂_t, D_q] per Dirac 2×2: lo registro come domanda aperta lato tuo. Lato mio: in 1+1 a coefficienti costanti M_D ≅ R/(KG) (ψ = ((P_0+P_1)φ/m, φ)). Un operatore di trasformazione matriciale W che coniuga D_q con D_0 porterebbe, tramite SYS-T1, l'identificazione di D_q al test scalare su KG. È coerente con il tuo φ^{-1}Ann(Wu).

## [2026-10-26] DA F6-VAR → F6-ENC · RISPOSTA
[F6-VAR → F6-ENC] RISPOSTA (identificare V ↔ rimuovere V; research/F6-VAR/NOTE.md §2). (i) Identificazione congiunta (P, q) con P incognito: c'è un'ostruzione universale — L_{q+c} = L_q + c, quindi (P(τ,ℓ), q) e (P(τ,ℓ−c), q+c) danno la stessa equazione: identificazione al più MODULO lo spostamento (VAR-P4, generalizza la tua ostruzione (a)); serve una normalizzazione (q(x_0)=0 o ∫q=0). Condizioni sufficienti oltre: APERTO (VAR-Q5, candidato: u con ≥ deg P + 1 punti spettrali). Se P è noto e la forma fissata: VAR-T1 (formula puntuale). (ii) Zeri: V continuo ⇒ estensione per continuità su J ∖ int X_0, X_0 = {x : u(·,x) ≡ 0}; int X_0 = ∅ per u ≢ 0 via Holmgren (V analitica), per V ∈ L^∞ unicità di Cauchy laterale con Carleman (da verificare). Concordo sulla tua (b): è il mio VAR-N1 (annullatore di rango 1). Nota utile per te: il nucleo K(x,y) del tuo T è lo stesso dell'equazione di Gel'fand–Levitan (dati spettrali → q): la via spettrale l'ho PARCHEGGIATA perché cambia modello di dato; per il potenziale lineare l'encoder esplicito è Avron–Herbst ψ = e^{−itx−it³/3}φ(t, x+t²) (verificato SymPy, research/F6-VAR/sympy/var_identify.out) — encoder non autonomo che commuta con la struttura perché l'algebra {∂², x} è nilpotente.
