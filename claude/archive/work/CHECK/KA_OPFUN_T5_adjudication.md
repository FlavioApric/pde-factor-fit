# KA OPF-T5 — Thread 2 (arbitrato, subagente Claude fresco ac6a13b0b5bf0060d, 26/10/2026)
Input: KA_OPFUN_T5_input.md + KA_OPFUN_T5_attack.md (nient'altro). Testo dell'arbitro, riportato per punti (fedele).

- **P1 — la trave non ha (C) sul parallelogramma.** answered_by_current_text. Calcolo dell'attaccante corretto (anzi (C) fallisce per ogni L ≥ 1: con c = 2t_o − x_o, lato superiore 1 − L + c > 0, inferiore c < 0); non contraddice nulla: il corollario (b) è enunciato solo per rettangoli e (C) è ipotesi di T5; il fallimento di (C) non confuta la densità.
- **P2 — la frase riassuntiva senza dominio non è dimostrata.** still_unresolved, **minor**. Cor. (a): P omogeneo su ogni convesso limitato (corretto); Cor. (b): P quasi omogeneo solo su rettangoli (con lati paralleli agli assi, implicito). L'"Esito P2-Q1" ("per ogni P (quasi) omogeneo", "nessuna somma è chiusa senza essere densa") lascia cadere entrambe le restrizioni. Fix: "P omogeneo su ogni convesso limitato; P quasi omogeneo su rettangoli con lati paralleli agli assi; altri domini aperti".
- **P3 — l'estensione di P5 richiede corde annidate.** answered_by_current_text (ipotesi già scritta; verificata).
- **P4 — "è lo stesso parallelogramma di P5".** answered_by_current_text: P5 non usa T5 né (C), solo Ψ_λ(Ω′) ⊂ Ω′ e regolarità interna.
- **P5 — O1 esclude solo mappe non pesate; esiste una simmetria pesata.** partially_answered, minor. L'identità pesata è corretta, ma O1 come enunciato (non pesato) è vero e la mappa pesata è un'involuzione isolata (det −1), non una famiglia → id; verifica dell'arbitro: con peso e^{at+bx} e Φ = (αt, βx+γt) si ottiene b ∈ {0,−1}: identità o l'involuzione. Ma il testo non contiene l'argomento pesato: "ostruzione dimostrata" va ristretta o completata.
- **P6 — ritirare "chiuso con densità in queste classi".** partially_answered, minor: i casi elencati sono dimostrati (P5, Cor. (a),(b)); solo le due frasi vanno ristrette.

**Summary:** answered 3, partially 2 (minor), still_unresolved 1 (minor); critical 0, major 0.
**Net assessment (arbitro):** nessun enunciato di OPF-L3, T5, Cor. (a),(b), P5, O1 è falso o non dimostrato; è troppo larga la formulazione dell'Esito P2-Q1.
**Top action items:** (1) riscrivere l'Esito con i domini; (2) lemma sulle simmetrie affini pesate di (τ−ξ²)(τ+ξ) (solo id e l'involuzione) o "dimostrata per simmetrie affini"; (3) nel Cor. (b) "rettangolo con lati paralleli agli assi".

**Verdetto (calcolato da S-CHECK-14 con la tabella della skill):** 1 still_unresolved di severità minor ⇒ **WARN** (`unresolved_major_or_minor`). Il punto riguarda la frase riassuntiva, non un enunciato; fix T5-1, O1-1 nell'audit.
