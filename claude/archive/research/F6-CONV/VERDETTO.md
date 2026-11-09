# VERDETTO — F6-CONV (Fase 6, scouting R13 + R15) — 26/10/2026

Stato onesto: tutti gli enunciati sono **candidati con prova scritta** (research/F6-CONV/NOTE.md), non auditati. Niente DIMOSTRATO senza S-CHECK. Skill caricate: session-protocol, route-scout, claim-lifecycle, novelty-check (fasi A–B; fase C con revisore esterno non disponibile), math-skill (modo proof), scientific-critical-thinking. SymPy/numerica solo come controllo: `sympy/conv_learner.out`, `conv_locality.out`, `conv_stab.out` (tutti OK). Criteri: quelli di PLAN.md, fissati prima della ricerca.

## Risposta breve alla domanda dell'utente ("possiamo garantire la convergenza dell'algoritmo a un'equazione differenziale?")
- **(C1) Consistenza: sì, ma solo nel limite e mai certificata.** Con il jet che cresce, la regola del grado minimo L\* restituisce **esattamente** P da un passo finito K\* in poi, ogni volta che Ann(u) = (P), senza conoscere deg P, con al più (d+1)(d+2)/2 cambi di ipotesi (uniforme in u) [CONV-T1]. Il tempo K\* non è limitato da alcuna funzione di d (esempio esplicito) e nessun dato finito dice che K\* è stato raggiunto (C3-P1). Con maggiorante di grado si ottiene l'ideale intero (G_u compreso).
- **Confine (teorema negativo):** nessuna regola, **nemmeno non calcolabile o non continua**, decide nel limite "esiste una legge differenziale" (Ann(u) ≠ 0) contro "non esiste" [CONV-T2, Gold analitico, costruzione diagonale con u intera]. La località è verificabile nel limite, refutabile con certificato finito a ogni livello, non decidibile nel limite.
- **Rumore:** l'identificazione è discontinua in ogni punto (H^m, C^k, C^∞) [CONV-T3]; è stabile solo **al livello 𝓓_n e con margine**: sin∠ ≤ 2δ/ρ (ρ = σ_2 del operatore di feature; ordine ottimale), Hölder δ^{s/(n+s)} con limite a priori in H^{n+s} [CONV-T4]; con la regola di discrepanza (livello minimo con σ_1 ≤ δ_m) l'uscita converge a P con quella velocità per δ < δ₀(u), soglia non calcolabile [CONV-T5]. Concordato con F6-DICT: **R-STOP = CONV-T5**; I-LIM = CONV-T1 (ramo esatto) + F6-DICT §7 (ramo approssimato).
- **(C2) Località:** a livello operatore, locale ⟺ differenziale ⟺ simbolo polinomiale (Peetre, CON-FONTE da verificare). A livello di **una soluzione**, Ann(u) = ideale di annullamento del grafo del simbolo sopra lo spettro di u [CONV-T6]: c'è una legge differenziale ⟺ il simbolo è algebrico sullo spettro. Conseguenze verificate: Poisson e^{−t|D|} ⇒ u armonica (Laplace); e^{−t√(1−∂²)} ⇒ Klein–Gordon; memoria esponenziale ⇒ telegrafo; frazionario irrazionale o ritardo ⇒ nessuna legge differenziale. "Locale o non locale" **non è una proprietà di u** ma della coppia (u, classe di leggi): tricotomia (L) locale / (L⁺) locale dopo aggiunta di variabili (Caffarelli–Silvestre, memoria → sistema aumentato, Dirichlet-to-Neumann) / (N) nessuna legge.
- **(C3) Parti iterative:** "contratto di convergenza" [CONV-T7]: ogni passo è (A) finito/esatto, (B) convergente con maggiorante esplicito (Dyson–Phillips, Magnus limitato con ∫‖A‖ < π, Trotter–Kato), o (C) asintotico/senza garanzia (Magnus/BCH illimitati, algebre non risolubili P1-T5, splitting con Dirichlet: riduzione d'ordine, P3-T3); la catena garantita contiene solo (A)/(B), errore totale per telescopica. Raggi per V(t,x): F6-VAR (DOMANDA inviata, risposta non ancora arrivata).
- **Dimensione 1+d:** riduzione indipendente dalla dimensione Ann(u) = (P) ⟺ Ann(w_i) = (P_i) ∀i [CONV-P8]; in 1+1 è C3-T1 (eccezione = EP), in 1+d, d ≥ 2, l'eccezione è un sistema sovradeterminato con soluzioni infinito-dimensionali (es. f(t+x)) ⇒ niente soglia di jet alla C3-T3; CONV-T1/T2/T4/T5 valgono invariati. Scomposizione: esiste su convessi (Ehrenpreis–Palamodov), ambiguità finita ⟺ nulla ⟺ fattori comassimali (Krull).
- **Bordo:** invisibile ad Ann(u); serve un dizionario di tracce (CONV-T4/T5 si trasportano); il bordo rompe la commutazione (P3-T3) e crea non località (DtN).

## Domanda guida I/S/E (regola 3)
| strada | (I) identificazione | (S) fattori/termini | (E) E_int | costo F8 | novità |
|---|---|---|---|---|---|
| CONV-LIM (T1, T2) | **sì**: C3-T1/P4-T2 nel limite (P esatto in tempo finito, non certificabile); confine T2 | parziale: con maggiorante di grado si ha l'ideale intero ⇒ fattori via C12-T1′ | no (non pertinente) | ≤ 1 sessione | media (3–4/10): Gold/Angluin e "decidibile nel limite ⟺ Δ⁰₂" noti; applicazione ad Ann(u) da jet, conteggio dei cambi e costruzione con u intera non trovati |
| CONV-STAB (T3–T5) | **sì** relativo a 𝓓_n con margine ρ | parziale: le componenti sono stabili ⟺ γ_N > 0 (già P2-C2/C12-P7) | no: coerente con R5-T2[H^m] FALSO | ≤ 0,5 | bassa (2/10): tipo Davis–Kahan/Wedin + interpolazione + Morozov; utile come specifica |
| CONV-LOC (T6 + Peetre + tricotomia) | **sì**: Ann(u) = I(grafo del simbolo) | parziale: rami del simbolo algebrico ↔ fattori (Poisson: (τ+iξ)(τ−iξ)) | no | ≤ 0,5 | bassa-media (3/10): ingredienti classici, enunciato a livello di dato non trovato |
| CONV-ITER (T7) | n/a | n/a | **sì** come contratto (A/B/C) | 0,25 | nulla come teorema |
| CONV-DIM (P8 + scomposizione 1+d) | parziale (classe eccezionale infinito-dim.) | parziale (esistenza sì, unicità ⟺ comassimali) | sì (R5-T2 indipendente dalla dimensione) | ≤ 0,5 | bassa |
| CONV-BORDO | no (bc invisibili ad Ann; serve dizionario di tracce) | ? | parziale (P3-T3, riduzione d'ordine) | > 1 | — |

## Raccomandazioni (criteri di PLAN.md)
- **PROMUOVI CONV-LIM** (T1 + T2 + CONV-L1): enunciati nuovi rispetto al LEDGER, prove scritte, compatibili con C3-P1/P4-T5 (li usano come confine), analitici, costo ≤ 1 sessione. T2 è il teorema negativo che marca il confine di T1 (regola N1).
- **PROMUOVI CONV-STAB** (T3, T4, T5) come specifica del passo "rumore" e regola di arresto unica R-STOP (accordata con F6-DICT); novità bassa ma (b) soddisfatto (nessuna riga del LEDGER dà stabilità con costante esplicita), costo minimo.
- **PROMUOVI CONV-LOC** (T6 + tricotomia L/L⁺/N); Peetre resta CON-FONTE da far verificare a CIT-AUDIT.
- **MERGE CONV-ITER** in ALGORITMO_ESTESO passo 7 (contratto A/B/C), con i raggi di F6-VAR.
- **PROMUOVI CONV-P8** come lemma (economico); il resto di CONV-DIM (domini non convessi, Hartogs) **PARCHEGGIA** (CONV-Q5).
- **PARCHEGGIA CONV-BORDO** (dizionario di tracce non scritto; ordine globale implicato da P3-T3 aperto: CONV-Q6).
- **ELIMINA**: consistenza "statistica" (regressione sparsa ℓ¹, SINDy, teoria asintotica con rumore stocastico) come *metodo*: viola il vincolo niente-ML; resta solo come confronto di novità.

## Rischi / da verificare (scientific-critical-thinking)
- T2: la costruzione usa il jet formale reale e coefficienti scelti in aperti densi; passo cardine (ii) da far controllare (rango pieno della sottomatrice delle righe |β| > L). T1(6): esempio verificato in SymPy (N = 3) e con prova.
- T4(b): numero del teorema di interpolazione (Adams–Fournier) da verificare; ottimalità dell'esponente s/(n+s) non dimostrata (CONV-Q2).
- T6: richiede f̂ a supporto compatto (u intera in x); per dati generali in H^m(Ω) la rappresentazione di Ehrenpreis non è unica e il criterio va riformulato (CONV-Q4).
- L'ordine "1,25" di riduzione per Strang con Dirichlet NON è stato trovato in letteratura (ricerca: Einkemmer–Ostermann 2015; Dang–Einkemmer–Ostermann 2025 riportano ordine 1 con Dirichlet, 1,5 con Neumann/Robin): il legame con Θ(t^{5/4}) di P3-T3 resta una domanda (CONV-Q6), non un claim.

## Righe LEDGER proposte (stato "prova scritta", non DIMOSTRATO)
CONV-L1, CONV-T1(1–7), CONV-T2, CONV-T3, CONV-T4(a–c), CONV-T5(1–4), CONV-T6(1–4), CONV-P8; CONV-T7 come specifica; Peetre come CON-FONTE da verificare. Dettaglio in inbox/central-F6.md (TABELLA).
