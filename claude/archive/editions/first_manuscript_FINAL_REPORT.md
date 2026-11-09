# Report finale: revisione del paper (v3)

File: `paper.tex` / `paper.pdf` (35 pagine, prima 29). Copia di sicurezza della versione precedente: `paper_v3_backup.tex`.
Compilazione: `latexmk -pdf`, nessun errore, nessun riferimento o citazione non risolti, 5 overfull hbox da 0,3 a 5,6 pt.
Verifica visiva: ho guardato a occhio tutte le pagine modificate (4, 6–26, 28, 34–35). Corretti dopo il controllo: frase spezzata dalla Figura 4 in 5.4, intervallo "Sections 2–6" in 7.4, badge di Tab. 1 e Sez. 9 per la Prop. 5.1 (ora con nota E9). Restano difetti estetici già presenti: etichette sovrapposte in Fig. 2, qualche spazio bianco a fine pagina (p. 8, p. 24).
Nota: nella cartella c'è `paper_old.pdf` (identico alla mia prima compilazione, rinominato da qualcuno); `paper.pdf` è stato rigenerato.

## 0. Revisione grafica (v4)

Solo layout, contenuto invariato. Copia precedente: `paper_v4_backup.tex`. Modello grafico: `paper_old.pdf` (titoli neri, box dei teoremi, "Intuition", "Why it matters").
- Paragrafi fitti delle mie aggiunte spezzati in box "Notation" (grigi, come "In this section") e note laterali ambra (come "Why it matters"), con elenchi e formule in display.
- Tolti titoli colorati, interlinea larga ed esempi in riquadro, per restare vicini al vecchio stile.
- Dentro ai box i paragrafi hanno ora spaziatura propria.
- Ora 38 pagine, nessun errore. Ho ricontrollato a occhio le pagine 7, 9, 11, 12, 14, 17, 19, 20, 22, 26; le altre non sono state rivedute dopo questa riorganizzazione.
- Piccole differenze di forma: nel box dei termini di 4.3 le etichette sono "Jet of order k", ecc. invece di "The jet of order k...".

## 1. Errori trovati durante la revisione (da leggere per primi)

1. **Numeri di riferimento sbagliati in tutto il paper.** Le `\ref` ai teoremi, lemmi e definizioni stampavano il numero della *sottosezione* invece di quello del teorema (per esempio "Lemma 2.3" al posto di "Lemma 2.5", "Thm 7.3" al posto di "Thm 7.2"). Causa: i riquadri `tcolorbox` non aggiornavano `\@currentlabel`. Corretto nel preambolo (`labelfix`). Ora i numeri coincidono con i titoli dei riquadri.
2. **Proposizione 5.1 falsa come scritta.** Diceva che ker L ∩ (ker L₁ + ker L₂) è contenuto nel nucleo comune ker(L₁, L₂). Controesempio: u = x²/2 + Dt per il calore. Corretta in "contenuto in ker(L, L₁L₂)", con dimostrazione breve. Ho tolto il badge "proved" perché l'enunciato nuovo non è stato rivisto da nessuno: va rivisto.
3. **Dimostrazione del Lemma 2.3 imprecisa.** "Any two of them without a common factor" è falso come scritto (J = (τ, ξ), elementi τ e τξ). Sostituita con la costruzione esplicita di due elementi senza fattore comune.
4. **Esempio di Sez. 4.2 incoerente.** La frase su P = τ, u = e^{x²} non mostrava quello che affermava (τ è irriducibile, e V(Ann u) è una retta, non uno spettro puntuale). Sostituita con l'esempio verificato P = τ², u = e^{x²}. Va confermato dall'autore (nota E12).
5. **Dimostrazione "easy direction" del Teorema 4.1** usava F3 e il Lemma 2.5 senza dirlo: ora è esplicito.

## 2. Modifiche per sezione

| Sez. | Cosa è stato fatto |
|---|---|
| 2.2 | F1–F3 spiegati (cosa sono, a cosa servono, valgono su ℂ, riferimento Cox–Little–O'Shea); simboli del Lemma 2.3 definiti; dimostrazione corretta; due esempi estremi di G_u, J_u |
| 2.3 | Paragrafo di notazione: ℛ, ℛw, ℛ/Ann(w), p_j, esponenti (τ_j, ξ_j), dim_ℂ |
| 3 | Simboli definiti (D, m = Σ m_j, λ_j, m_j, q_j, ker); perché le soluzioni hanno quella forma; esempio (λ−1)²(λ+2)³; a_k nella matrice compagna; riquadro "Takeaway" finale |
| 4.1 | Terminologia (EP(Ω), ridotto, monico in τ, k, t-jet); nuova Proposizione di unicità; Esempio 4.1 (calore) esteso in tre casi con calcoli; dimostrazione giustificata |
| 4.2 | Notazione e derivazione dell'equivalenza (Nullstellensatz); illustrazione estesa; esempio sui fattori ripetuti corretto |
| 4.3 | Tabella 3 con la nuova colonna "What it means for the algorithm"; definizioni di jet, oracolo, ideale olonomo, algebra di Weyl |
| 5.1 | Proposizione corretta (vedi sopra) con dimostrazione; Esempio 5.1 con tutti i passaggi e il controesempio |
| 5.2 | Esempio dell'onda con verifica esplicita e display; paragrafo "Why factors work and terms do not" (identità di Bézout in una variabile contro ambiguità in due); didascalia della Fig. 3 |
| 5.5 | Formula variazionale di γ_N con spiegazione e controllo per N = 2 (γ₂ = 1 − c_F); riquadro "Two problems with regularity"; conflitto di simbolo N risolto (M₁, M₂) |
| 6 | Paragrafo introduttivo dalla somma degli operatori a E_int; Fourier introdotta esplicitamente; commutatività; Δ_n definito; dimostrazione estesa a N generico; 6.3 chiude con la formula esatta usata (forma prodotto, O(N) per κ); 6.5 con scopo, lettura della serie e cosa se ne ricava |
| 7 | 7.2 riorganizzata in tre regimi (prima, durante, dopo lo shock) con tabella riepilogativa, t\* = 1 per sin x; J_u dell'ostruzione rinominato 𝒥_u; nuova 7.4 "Linear versus nonlinear" con tabella di confronto e takeaway |
| Appendice D | Nuove note per l'autore E8–E13 |

## 3. Cosa resta da verificare o decidere (per l'autore)

- **E8**: il parametro d della soglia 2d−1 in Tab. 3 non è definito.
- **E9**: la Proposizione 5.1 corretta va riesaminata (badge tolto).
- **E10**: in 6.5 non è detto quale coppia (A₁, B), in quale norma e da dove venga l'esponente 3/4.
- **E11**: l'isomorfismo ℛu ∩ EP ≅ ℛ/J_u non è dimostrato nel testo.
- **E12**: conferma dell'esempio P = τ², u = e^{x²}.
- **E13**: ψ, "evolutionary dictionary", "complete dictionary" non definiti.
- Note già presenti e non risolte: Fisher–KPP nell'abstract senza enunciato (E2), implicazione del Passo 1 (E3), simboli sovraccarichi S, D, J, σ, c (E5), solo la direzione facile del Teorema 4.1 (E6), "Stein" senza voce bibliografica (E4).

## 4. Cosa non è stato fatto

- Le sezioni 8 e 9 e le appendici A–C non sono state riscritte (solo la numerazione automatica dei riferimenti cambia).
- L'esempio per la sequenza esatta del Teorema 7.2 non è stato aggiunto: non si può derivare con sicurezza dal testo esistente.
- Le correzioni dell'altra sessione ("fork 2") non sono state applicate: ho usato solo le note date in questa sessione.
- Non ho riscritto il `CHANGELOG.md`: questo file lo sostituisce per la v3.
- Gli enunciati nuovi (unicità, γ₂ = 1 − c_F, Prop. 5.1 corretta, derivazione della Prop. 4.3) sono dimostrati nel testo da me, non rivisti da una persona terza.
