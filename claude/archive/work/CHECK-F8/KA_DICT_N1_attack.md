# KA DICT-N1 — argomento d'attacco (revisore ostile, 27/10/2026)

Base: solo `work/CHECK-F8/KA_DICT_N1_input.md`. Controlli: `work/CHECK-F8/sympy/dict_ka_checks.py` (blocchi K1–K6), eseguito con `.venv\Scripts\python.exe -I`.

## 1. Memo d'attacco

L'argomento più dannoso non colpisce il nucleo topologico (N1(i), N1(v), Teorema A), che regge nella sostanza. Colpisce il blocco che dovrebbe sostituire N1(vi), cioè il Teorema RANGO e i suoi corollari. Qui il testo scambia sistematicamente "ker Φ_u = 0" con "identificabile" e "non esiste un'ostruzione puntuale" con "esiste una legge". Il punto (II) è dimostrato correttamente, ma caratterizza ker Φ_u = 0. Con la definizione data in §2.6 ("identificabile se esiste **al più** una legge"), però, ogni u che falsifica la classe è identificabile per vacuità. Ne seguono tre conseguenze.

(1) La frase "(IV): se K·dim𝔽 > dim(valori) la classe non è mai identificabile" e il corollario "(a′): mai identificabile" sono falsi. Controesempio: u = t con N = 2, m = 1 e classe ∂_t + θ_0 + θ_1∂_x. In t = 0 si ha u = u_x = 0 ma u_t = 1, quindi non c'è nessuna legge e la classe è identificabile per vacuità (K2). Il caso è dello stesso tipo di DEVIL-6, che il testo cita per le classi normalizzate senza vedere che contraddice (a′).

(2) Tutti i "⟺" della forma "identificabile ⟺ int Z(u) = ∅" (Schrödinger con V complesso e con V reale) e "identificabile ⟺ {u_x ≠ 0} denso" (trasporto) cadono nella direzione (⇒) per ogni u che falsifica la classe e ha zeri su un aperto.

(3) Il criterio di esistenza per V reale, "una legge esiste ⟺ Im((iu_t+u_xx)/u) ≡ 0 su {u ≠ 0}", vale solo in (⇒). Per u = e^{−it}(x + x²) il quoziente è (x²+x+2)/(x(x+1)), che è reale; eppure in x = 0 si ha u = 0 e iu_t + u_xx = 2e^{−it} ≠ 0, quindi nessuna legge esiste (K3). Il testo stesso ammette nel "caso intermedio Q3" che questo è un problema di divisione, e poi enuncia un "⟺" che lo ignora.

Si aggiunge il caso magnetico, che non rientra nel quadro lineare in θ: (∇−iA)² contiene div A, una derivata dell'incognita, e |A|², un termine quadratico. La descrizione "spazio affine sui campi a divergenza nulla" è falsa: B = (sin y, 0) ha divergenza nulla ma non è differenza di due leggi per u = (2+cos x)e^{iy} (K6). La condizione giusta, ricavata a mano, è div(|u|²B) = 0, e la V corrispondente dipende in modo quadratico da B.

Nessuno di questi difetti distrugge il messaggio qualitativo ("l'asse giusto è il conteggio K·dim𝔽 contro dim(valori)"). Ma §2.6 contiene più enunciati falsi così come sono scritti, e tutti si trovano proprio negli insiemi di zeri, il regime che il quadro dichiara di controllare. A questo si somma N1(iii), falso così com'è scritto (manca l'ipotesi L ∈ Ann(u)), e una prova del Teorema A(iii) in cui l'"ipotesi dichiarata" U_0 è vuota (U_0 = Ω la soddisfa sempre) e non fornisce ciò che la prova usa. Conclusione: il pacchetto non è uccidibile nel nucleo, ma non può essere accettato com'è.

## 2. Punti d'attacco

**P1. RANGO (IV) e corollario (a′): "mai identificabile".**
Accusa: con la definizione "identificabile ⟺ al più una legge", (II) fornisce solo ker Φ_u ≠ 0, e questo rende la classe non identificabile soltanto se esiste almeno una legge.
Controesempio: u = t, Ω ∋ (0, x), classe ∂_t + θ_0·1 + θ_1∂_x (N = 2, m = 1, K = 2, 2K = 4 > 2). In t = 0 l'equazione θ_0u + θ_1u_x = −u_t diventa 0 = −1: non ci sono leggi, quindi la classe è identificabile (K2). Lo stesso vale per qualunque u con un punto in cui tutte le ∂^αu, α ≠ e_t, si annullano mentre u_t ≠ 0. Il caso magnetico ("mai identificabile") ha lo stesso difetto.
Gravità: CRITICAL (falso locale, ripetuto in (IV), (a′) e SYS).
Riparazione: definire due nozioni distinte, "identificabile" come ker Φ_u = 0 (unicità condizionata) e "ben posta" come esistenza più unicità. Oppure riscrivere: "se esiste una legge, non è unica".

**P2. Corollari (b′) e trasporto: "identificabile ⟺ int Z(u) = ∅" e "⟺ {u_x ≠ 0} denso".**
Accusa: la direzione (⇒) è falsa per i dati che falsificano la classe.
Controesempio (trasporto): u = t + ψ(x) con ψ′ = 0 su un intervallo I. Su ℝ × I si ha u_x = 0 e u_t = 1, quindi non c'è legge e la classe è identificabile, ma {u_x ≠ 0} non è denso (K5). Un controesempio analogo per Schrödinger si ottiene moltiplicando per un cutoff nullo su un aperto l'esempio falsificante del testo; la falsificazione in (0,3; 0,7) resta (K4).
Gravità: CRITICAL.
Riparazione: enunciare "ker Φ_u = 0 ⟺ …", come in (II).

**P3. (b′) con V reale: criterio di esistenza "⟺ Im((iu_t+u_xx)/u) ≡ 0 su {u ≠ 0}".**
Accusa: vale solo (⇒). La direzione (⇐) richiede che il quoziente si estenda in modo liscio attraverso Z(u) e che iu_t + u_xx = 0 su Z(u).
Controesempio: u = e^{−it}(x + x²). Il quoziente vale (x²+x+2)/(x(x+1)) ed è reale, ma in x = 0 si ha −L_0u = −2e^{−it} ∉ im A_u = {0}, quindi u falsifica la classe per (III) (K3).
Gravità: CRITICAL (falso locale). L'enunciato contraddice anche la nota sul caso intermedio Q3.
Riparazione: "⟺" solo se u non ha zeri; in generale servono la condizione su Z(u) e il problema di divisione di Malgrange–Łojasiewicz.
L'esempio falsificante del testo regge: V(t=0,3; x=0,7) ha parte immaginaria −0,02491 (K4).

**P4. Sistemi: Schrödinger magnetico dentro il "quadro lineare in θ".**
Accusa: L_θ = L_0 + Σθ_kT_k con θ_k che moltiplica T_ku punto per punto non copre (∇−iA)² = Δ − 2iA·∇ − i(div A) − |A|². Il termine (div A)u coinvolge ∂θ, e |A|² è quadratico. Quindi non sono definiti né A_u(y) né (I) ("θ⁰ + ker Φ_u").
Controesempio alla struttura dichiarata: u = (2+cos x)e^{iy} ha la legge A = 0, V = (Δu)/u, che è reale. Prendiamo B = (sin y, 0), con div B = 0. La parte immaginaria di [(∇−iB)² − Δ]u/u vale 2 sin x sin y/(2+cos x) ≠ 0, e nessun V reale la compensa (K6). Le differenze di leggi, ricavate a mano, sono i B con div(|u|²B) = 0, e V′ è quadratica in B: l'insieme delle leggi non è uno spazio affine.
Gravità: MAJOR. La conclusione "non unica se esiste una legge" è probabilmente vera, ma la prova esce dal quadro e la struttura enunciata è falsa.
Riparazione: trattarlo con un lemma a parte (rappresentazione u = ρe^{iS} e condizione div(ρ²B) = 0), oppure togliere il rinvio a RANGO.

**P5. N1(iii): manca l'ipotesi L ∈ Ann(u).**
Accusa: "per ogni L ∈ R con deg L ≥ 1: Ann(u) ∩ R_{≤n} ⊋ (L) ∩ R_{≤n}" è un'inclusione stretta, ed è falsa se L ∉ Ann(u). La prova dimostra solo una disuguaglianza fra dimensioni.
Controesempio: u = e^t, N = 2, D = 1, n = 1 (C(2,1) = 2 > 1), L = τ + 5. Si ha Ann(u) ∩ R_{≤1} = span{τ−1, ξ}, mentre τ + 5 ∈ (L) ∩ R_{≤1} non appartiene ad Ann(u) (K1).
Gravità: CRITICAL formalmente (falso locale). La riparazione è banale: aggiungere "L ∈ Ann(u)" (allora (L) ⊂ Ann(u) perché Ann(u) è un ideale, e la stima delle dimensioni dà l'inclusione stretta).
Errore collegato: "la differenza delle dimensioni è costante (= deg L) per N = 1" contraddice la frase precedente. Per L ∈ Ann(u) e n ≥ deg L la differenza è deg L − D, che vale 0 per L = P_min. Gravità MINOR.

**P6. Teorema A(iii): l'"ipotesi dichiarata U_0" è vuota e non dà ciò che la prova usa.**
Accusa: "esiste un aperto U_0 ⊂ Ω su cui i D_i sono indipendenti" è sempre vera con U_0 = Ω. La prova però applica il Lemma ND su M+1 **palle** B_k ⊂ U_0, e questo richiede l'indipendenza su ciascuna palla, che non segue. Esempio: Ω unione di due palle disgiunte, D_0 = χ_1∂_t, D_1 = χ_2∂_t con χ_i supportata nella i-esima palla. I due operatori sono indipendenti su Ω, ma su ogni palla contenuta in Ω sono dipendenti. Inoltre l'enunciato (iii) non riporta l'ipotesi.
Il teorema è però vero senza alcuna ipotesi aggiuntiva. Dalla prova del Lemma ND (con U = Ω) si ottiene det[L_i(y_k)(j_k)] ≠ 0 su un prodotto di intorni W_1 × … × W_{N+1}. Si scelgono M+1 (N+1)-uple di punti tutti distinti, e per ciascuna si usa come "B_k" l'unione di N+1 palline minuscole: gli aperti B_k non sono connessi, ma sono a due a due disgiunti. L'argomento di località e il sistema M × (M+1) restano invariati. Il sistema (M equazioni, M+1 incognite), la località di D_iw su B_{k_0} e il coefficiente direttore det(ℓ′_j(D_iw)) sono corretti, e i funzionali ℓ_j non devono nemmeno essere continui.
Gravità: MAJOR (passo non giustificato localmente; il risultato sopravvive).
Riparazione: sostituire le palle con aperti disgiunti costruiti come sopra ed eliminare l'ipotesi e la nota.

**P7. Teorema A(i): "anche in topologie deboli (D′)" per operatori lineari continui qualsiasi C^∞ → D′.**
Accusa: la continuità di u ↦ ⟨D_iu, ψ⟩ nella topologia di D′ richiede che D_i^tψ ∈ C_c^∞. Questo vale per gli operatori differenziali, non per quelli generali. Esempio: Du = u(y_0)g non è continuo per la convergenza debole.
Gravità: MINOR.
Riparazione: limitare il "debole" ad atomi con trasposto che manda C_c^∞ in C_c^∞.

**P8. N1(i): "per ogni dizionario … con finiti parametri continui per atomo".**
Accusa: la prova richiede che la parametrizzazione P_k → X sia continua (o almeno che l'immagine sia σ-compatta). Per famiglie naturali questa continuità fallisce. Per esempio s ↦ χ|ξ|^s non è continua in S^m in s = m: sup ⟨ξ⟩^{−m}·||ξ|^s − |ξ|^m| tende a 1, non a 0. Il ritardo e^{−iτσ} non sta in nessun S^m. Con una parametrizzazione solo boreliana l'enunciato è falso: un isomorfismo boreliano ℝ → X dà un atomo a un parametro la cui immagine è tutto X.
Nel testo l'esito è innocuo, perché i parametri di §0 sono razionali e il dizionario è numerabile; nei casi citati inoltre l'immagine resta σ-compatta spezzando il dominio. La parte Riesz/Baire è corretta.
Gravità: MINOR.
Riparazione: richiedere esplicitamente la continuità in X, oppure l'immagine σ-compatta.

**P9. N1(iv)(c): giustificazione "Σ⁰₂ ∖ Π⁰₂" nel modello BSS.**
Accusa: nel modello BSS le regole fanno test esatti di uguaglianza e non sono continue. Un limite di regole Δ⁰₂ può decidere insiemi Σ⁰₃, quindi la classe di Borel da sola non esclude la decisione nel limite. La conclusione regge comunque per un argomento diagonale sui prefissi: ogni prefisso del getto si estende sia a getti con Ann(u) ≠ 0 sia a getti con Ann = 0, purché si controlli la crescita per restare fra le funzioni intere. Questo argomento va però citato, non il livello di Borel. N1(iv)(a) è corretto ma banale (conta le cardinalità e non dipende da C3-T4).
Gravità: MINOR (è un enunciato importato).

**P10. Corollario (a′): "K ≥ 2".**
Accusa: per N = 1 (d = 0) e m = 1 si ha K = 1 e 2K = 2 = dim(valori). La classe ∂_t + θ_0 è identificabile quando int Z(u) = ∅.
Gravità: MINOR (serve d ≥ 1 oppure m ≥ 2).

**P11. "Legame con F4-ALG": "quelle con I(u) ≠ 0 sono rare".**
Accusa: l'insieme delle u differenzialmente algebriche è magro e shy, ma è denso (contiene i polinomi), quindi non è raro nel senso tecnico usato in (a). Inoltre per u solo C^∞ resta ambiguo il caso "legge su un aperto ma non su tutto Ω". La versione locale (palle razionali) resta comunque magra e shy con la stessa prova.
Gravità: MINOR.

**Punti che reggono (detto brevemente).**
- Lemma ND: (⇐) via lo span di S, i getti realizzati in punti distinti e la località; l'esempio x∂_x è corretto.
- Lemma ND-NL.
- Base adattata al grado: la costruzione con i complementi è corretta.
- Chiusura di B_n: compattezza della sfera e continuità di P_i.
- Coefficiente di s^{Σe_i} per multilinearità.
- Rarità via Baire.
- Prevalenza: μ = legge di sw, a supporto compatto, con μ(B_n − u) = 0 per ogni u; B_n chiuso; unioni numerabili di insiemi shy (Christensen 1972; HSY 1992 per gli F-spazi).
- Passaggio a H^m, purché i D_i siano continui H^m → L², come dichiarato (con coefficienti illimitati non è automatico).
- MF3(a)–(d), incluso Weyl in norma di Frobenius.
- RANGO (I), (II) (semicontinuità del rango, apertura di {rango = max} e fibrato a rango costante: tutto corretto), (III) con la pseudo-inversa reale.
- Classe normalizzata con u = t − x²; forma algebrica di Ann_{𝒦[∂]}(u), dato che i due operatori di derivata logaritmica commutano.

## 3. Esito proposto

**SURVIVES-WITH-FIXES.** Il nucleo (N1(i), N1(v) con ND/ND-NL e prevalenza, Teorema A(i)–(iii)) sopravvive, con la prova di A(iii) da riscrivere (P6). Vanno corretti come enunciati falsi: N1(iii) (P5) e i corollari di RANGO (P1–P3), dove si confondono "ker Φ_u = 0" e identificabilità e si dichiara un "⟺" di esistenza che vale in una sola direzione. Il caso magnetico va tolto dal quadro lineare (P4). Nessun punto è FATAL per il risultato principale.
