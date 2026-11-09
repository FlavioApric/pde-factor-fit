# KA ENC-N1 — aggiudicazione (S-CHECK-F8-ENC, 27/10/2026)

Attacco: `KA_ENC_N1_attack.md`, scritto da un subagente indipendente che ha letto solo `KA_ENC_N1_input.md`; script dell'attaccante `sympy/enc_ka_n1_checks.py`. Esito dichiarato dall'attaccante: **WOUNDED**, nessun FATAL o CRITICAL.
Avvertenza di metodo: il prompt dell'attaccante elencava alcune piste di attacco (chiusura per ~ con DM-φ, banalità del controesempio v = 0, tautologia di (iii), verifica di (iv)). Le piste venivano dal mio controllo, fatto prima di lanciare l'attacco (`AUDIT_S8-ENC.md` §1, ENC-5). L'attacco quindi non è cieco rispetto a quelle piste. I punti P5 (seconda parte), P6, P7, P8, P9 e P10 sono invece contributi autonomi dell'attaccante.
Verifica dell'aggiudicatore: ho rifatto a mano l'identità di (iv) e il conto della famiglia stretta su un'onda stazionaria. Con W_c normalizzato in x_0 si ha W_c(e^{−iλt}cos √λ(x − x_0)) = e^{−iλt}cos √(λ + c)(x − x_0). Il conto è coerente con ENC-1(6), che l'attaccante non vedeva.

## Punti dell'attacco

**P1 — Con DM-φ il quadro è mal posto (proposto MAJOR).** *Verdetto: still_unresolved nel testo attuale, accolto come MAJOR.* L'insieme delle soluzioni non è chiuso per ~, e la sua saturazione non è uno spazio lineare. Il controesempio (iv) funziona **solo** nella lettura saturata: con gli insiemi letterali, u ∈ 𝒮_{q_0} ∩ 𝒮_{q_0+c} implica u = 0. Un controesempio che dipende da una definizione non scritta è una lacuna UNJUSTIFIED + LOCAL, quindi MAJOR. Alzo da MINOR a MAJOR il mio fix **ENC-5(a)**; la riparazione resta quella di ENC-5(a) (classi [𝒮_V], W_V lineare sull'ambiente, compatibilità W_V(e^{iθ}u) = e^{iθ}W_V u).

**P2 — 𝒪 ridondante con DM-φ, indefinito con DM3 (MINOR).** *Verdetto: accolto, MINOR.* È coperto da ENC-5(a) (𝒪 := 𝒟_0/≈, con ≈ esplicita in ciascun modello). Aggiungo la normalizzazione N_V(v) := e^{ic_V t}v proposta dall'attaccante, che rende E(u) = [N_V W_V u] ben tipata anche con DM3.

**P3 — Controesempio a F6 banale; la versione caritatevole è falsa solo per (iv) (proposto MAJOR).** *Verdetto: accolto; severità MINOR.* Coincide con il mio ENC-5(b). Il verdetto FALSO resta, e va solo cambiato il testimone. L'attaccante nota due cose in più: nell'istanza V(x) con DM3 la versione caritatevole F6* è **vera**; il testo rimanda a (iii) dove usa (ii). Entrambe vanno nel fix. È MINOR perché lo stato registrato (FALSO) non cambia.

**P4 — (i)–(iii) tautologiche; "forma richiesta dal roster" ottenuta per ipotesi (proposto MAJOR).** *Verdetto: partially_answered, accolto come parte del MAJOR ENC-5.* Il testo e la riga di LEDGER parlano già di "lemma di riduzione", ma l'etichetta "Teorema" e la frase sul roster restano. Va scritto in modo esplicito che (S) ∧ (C) ⟺ identificabilità, per definizione, e che nessuna istanza nota ha (S) non vacua. Per G★″ e per il roster il contenuto registrabile è: "l'equivalenza richiesta vale solo in forma condizionale, con un'ipotesi equivalente alla tesi". Aggiungo questo come ENC-5(e).

**P5 — L'esistenza dell'encoder cieco dipende dalla famiglia (proposto MAJOR).** *Verdetto: accolto.* Coincide con il mio ENC-5(c) e lo rafforza con un conto esplicito: con la famiglia stretta (C) fallisce sulla classe {c}. Severità: MAJOR insieme a P1 (stessa riparazione: quantificare "per una famiglia fissata 𝒲").

**P6 — (iv) è un controesempio di gauge (MINOR).** *Verdetto: accolto; è un contributo importante per G★″.* Con DM-φ, (iw_t + w_xx)/w = q(x) − θ′(t), quindi q è identificato modulo costanti da ogni dato regolare non nullo con θ ∈ C¹. La formulazione corretta per il roster è: **"encoder cieco ⟺ identificabilità modulo il gruppo di gauge del modello di dato"**. In questa forma (iv) non è più un controesempio, e l'equivalenza resta tautologica salvo un'ipotesi di separazione modulo gauge. Va sostituita la citazione VAR-P4(a), che riguarda gli stati stazionari, con la formula sopra (ENC-5(f)).

**P7 — Istanza magnetica: non sequitur (proposto MAJOR).** *Verdetto: accolto; severità MINOR.* Per (iv), la non identificabilità non esclude un encoder cieco, e quella magnetica è tipicamente di gauge. In più il caso n ≥ 2 è fuori dal quadro unidimensionale. È MINOR perché è una frase di un'istanza, non un enunciato registrato: va tolta o scritta come "aperto" (ENC-13).

**P8 — Istanza V(t, x): la domanda è vuota solo per encoder indipendenti dal tempo (MINOR o MAJOR).** *Verdetto: accolto, MINOR (ENC-13).* Si scrive "vuota per encoder strutturati indipendenti dal tempo (P0(b) e P0(b)^cl di ENC-4); aperta per W(t) strutturati". È coerente con ENC-2.

**P9 — Istanza V(x), DM3 (MINOR).** *Verdetto: partially_answered.* Sulla continuazione unica: VAR-T1(b), nella forma auditata (`AUDIT_S8-VAR.md` §2.1), dà V = V′ q.o. per u ≢ 0. La prova usa una continuazione laterale elementare (VAR-L1), quindi l'ipotesi richiesta c'è, ma va citata (mio ENC-5(d)). Su "costruttivo (non stabile)" e su onda e calore fuori dal quadro (E2′) con i∂_t: accolto, MINOR (ENC-13).

**P10 — Dettagli formali (MINOR).** *Verdetto: accolto, MINOR (ENC-13).* Si scrive Φ(V, v) ~ Φ(V′, v′) al posto dell'uguaglianza. Φ è definita su tutto 𝒱 × 𝒮 solo se W_V è suriettivo: va bene per Volterra, in generale no.

## Esito

**ENC-N1 (F6): FALSO confermato**, con testimone (iv) al posto di v = 0. **ENC-N1′: SURVIVES come lemma (osservazione logica) dopo i fix.** Il fix ENC-5 sale a MAJOR (P1, P4, P5), più ENC-13 MINOR (P7–P10). Nessun punto tocca la logica di (i)–(iv). Cambiano la buona posizione del quadro con DM-φ, l'etichetta e la portata delle istanze. Per G★″ la frase da registrare è: "encoder cieco ⟺ coerenza (C) per una famiglia fissata; ⟸ identificabilità; l'equivalenza piena vale solo sotto (S), ipotesi equivalente alla tesi; modulo il gauge del modello di dato, l'esempio DM-φ rientra".
