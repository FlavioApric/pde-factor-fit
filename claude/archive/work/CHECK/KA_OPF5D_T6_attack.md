# KA OPF5D-T6 — memo d'attacco (subagente fresco, 26/10/2026; input KA_OPF5D_T6_input.md)

**Esito: non sono riuscito a rompere la stima principale (passi 1–5). Obiezione residua più forte: MINOR, e riguarda solo il corollario (6).**

Ho cercato un errore nei punti in cui una prova di questo tipo di solito cede, ma ogni verifica è andata a buon fine.

- **Passo (3).** Da a_1 ≤ a_2 e x_i = a_i + tu_0(a_i) segue x_2 − x_1 ≤ (1 + t‖u_0′‖_∞)(a_2 − a_1) = tM(a_2 − a_1). Questa è una stima *dal basso* sull'incremento di G_0′ = a/t, con modulo 1/(t²M): verso e costante sono giusti. Poiché x ↦ D_x(y) = G_0(x) − xy/t + h(y) è ≥ 0 e fortemente convessa, ha un minimo e vale D_x(y) ≥ (x − x_y)²/(2t²M).
- **Passo (4).** Ho verificato lo scambio "Fubini + periodicità": ∫_{[0,2π]×ℝ} = ∫_{ℝ×[0,2π]}, perché l'integrando è invariante per (x,y) ↦ (x+2π, y+2π). Ho ricalcolato la gaussiana: √(4πνt²M). Il rapporto con c_0 = √(4πν/M) dà esattamente tM. Jensen è nel verso corretto, perché log è concavo.
- **Media non nulla di u_0.** Φ_{x+2π}(y+2π) = Φ_x(y) + 2π·mean(u_0) cambia solo per una costante. Quindi D_x, I, ε restano periodici e a(x+2π) = a(x) + 2π continua a valere.
- **Passo (5).** Le corde danno il segno giusto, perché si scarta −ε(x) ≤ 0. Poi ∫_0^{2π}[g′(x+h) − g′(x−h)] = ∫_{−h}^{h}[g′(x+2π) − g′(x)] = 4πh/t. Ottimizzando, h = √(2νt·L) con L = log(tM), e il risultato è esattamente 8π√(2νL/t).
- **Verifica numerica.** Caso u_0 = sin x (e 0,5 + sin x), t = 2 > t* = 1, ν ∈ {0,1; 0,03; 0,01; 0,003}. Ho usato Cole–Hopf su ℝ con quadratura fine. ‖u − v‖_{L¹} vale da 0,435 a 0,012, contro un bound da 8,33 a 1,44: il rapporto va da 0,05 a 0,009, quindi nessuna violazione. Il bound è però molto largo: l'errore osservato scala come O(ν), mentre il bound prevede O(√ν).

**Obiezione residua (MINOR).** Il passo (6) non è verificabile dall'input. Il Θ(√ν) per E^{mult}_{AB} si regge interamente su S4T-T3(iii), che l'input non riporta. Per lo stesso motivo non si può controllare che (iii) non usi [F3] e che non richieda una costante d'ordine inferiore alla 8π√(2L/t) dimostrata qui; la triangolare da sola non dà il limite inferiore. Anche il rimando a "(v): (vi)+(5)" è opaco. Inoltre nell'enunciato del corollario ‖u_0′‖ compare senza pedice ∞. La stima T6 in sé regge.

## Punti atomici
- §Prova (3): la stima x_2 − x_1 ≤ tM(a_2 − a_1) è corretta e implica la forte convessità con modulo 1/(t²M) — nessun difetto.
- §Prova (4): Fubini, periodicità, gaussiana √(4πνt²M) e verso di Jensen sono corretti; il rapporto con c_0 dà esattamente tM.
- §Prova (5): l'integrale periodico 4πh/t e l'ottimo h = √(2νt log(tM)) danno esattamente la costante 8π√(2ν log(tM)/t).
- Media non nulla: Φ cambia solo per una costante sotto la traslazione (x,y) ↦ (x+2π, y+2π), quindi la periodicità di ε regge.
- Verifica numerica (sin x, t = 2): errore/bound tra 0,05 e 0,009 per ν tra 0,1 e 0,003; il bound non è stretto, l'errore reale va come O(ν).
- §Enunciato, "Di conseguenza…", e §Prova (6): il Θ(√ν) e la parte (v) dipendono da S4T-T3(iii),(vi), che l'input non mostra — MINOR.
- §Enunciato, corollario: ‖u_0′‖ è scritto senza pedice ∞ — refuso.
