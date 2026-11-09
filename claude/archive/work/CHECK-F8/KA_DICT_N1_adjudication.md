# KA DICT-N1 — aggiudicazione (S-CHECK-F8-DICT, 27/10/2026)

Attacco: `KA_DICT_N1_attack.md`, scritto da un subagente indipendente che ha ricevuto solo `KA_DICT_N1_input.md` (estratto verbatim di PROOF_PACKAGE §0, §2.1–§2.6, MF3, Teorema A). L'attacco contiene 11 punti; l'esito che propone è **SURVIVES-WITH-FIXES**. Script dell'attaccante: `sympy/dict_ka_checks.py`. Controllo indipendente dell'aggiudicatore: `sympy/dict_check.py` → `.out`, **18/18 PASS**.

Il KA interno dell'autrice (`work/S8-DICT/KILL_ARGUMENT_N1.md`, PASS-WITH-NOTES, senza revisore fresco) non è stato usato come base: l'attacco è stato rifatto da zero. Nessuno dei punti P1–P6 sotto compare nel KA interno.

**Due scale di gravità.** Nella colonna "KA" uso la scala del kill-argument (impatto sull'accettazione del risultato principale N1: critical/major/minor). Nella colonna "proof-checker" uso la tassonomia a due assi (FATAL/CRITICAL/MAJOR/MINOR): un enunciato falso così come è scritto, ma locale, è CRITICAL anche quando la riparazione è di una riga.

## Verifica dell'aggiudicatore
Ho rifatto a mano tutte le prove bersaglio prima di leggere l'attacco (i miei appunti indipendenti hanno trovato P3, P4, P5, P6, P7 e P10; l'attacco ha trovato in più P1, P2, P8, P9, P11). Su P4 l'attaccante ha ragione e io avevo torto: nel calcolo delle differenze di leggi magnetiche avevo dimenticato il termine i·div B; la condizione giusta è div(|u|²B) = 0 (verificata a mano qui sotto).

## Punti per punto

| punto | bersaglio | verdetto sul testo attuale | gravità KA | gravità proof-checker | fix |
|---|---|---|---|---|---|
| P1 | RANGO (IV), (a′), caso SYS: "mai identificabile" | still_unresolved | major | CRITICAL (INVALID, LOCAL) | DICT-2 |
| P2 | (b′), trasporto: "identificabile ⟺ int Z(u) = ∅", "⟺ {u_x ≠ 0} denso" | still_unresolved | major | CRITICAL (stessa causa di P1) | DICT-2 |
| P3 | (b′) V reale: "legge ⟺ Im(…) ≡ 0 su {u ≠ 0}" | still_unresolved | major | CRITICAL (INVALID, LOCAL) | DICT-3 |
| P4 | caso magnetico dentro RANGO | still_unresolved | major | MAJOR | DICT-5 |
| P5 | N1(iii) senza "L ∈ Ann(u)" | still_unresolved | major | CRITICAL formale (riparazione di una parola) | DICT-6 |
| P6 | Teorema A(iii), palle B_k e ipotesi U_0 | still_unresolved | major | MAJOR (UNJUSTIFIED, LOCAL) | DICT-1 |
| P7 | Teorema A(i), "topologie deboli" | partially_answered | minor | MINOR | DICT-13 |
| P8 | N1(i), continuità della parametrizzazione | partially_answered | minor | MINOR | DICT-14 |
| P9 | N1(iv)(c), "Σ⁰₂ ∖ Π⁰₂" | partially_answered | minor | MINOR | DICT-15 |
| P10 | (a′), "K ≥ 2" | still_unresolved | minor | MINOR | DICT-2 |
| P11 | "rare" per le u differenzialmente algebriche | still_unresolved | minor | MINOR | DICT-16 |

**P1 — accolto.** La definizione di §2.6 è "identificabile se esiste al più una legge". (II) caratterizza ker Φ_u = 0, cioè l'unicità *condizionata all'esistenza*. Se u falsifica la classe, la classe è identificabile per vacuità, quindi "(IV): se K·dim𝔽 > dim(valori) la classe non è mai identificabile" e "(a′): mai identificabile" sono falsi così come sono scritti. Controesempio dell'attaccante verificato a mano: u = t, classe ∂_t + θ_0 + θ_1∂_x; in t = 0 l'equazione θ_0u + θ_1u_x = −u_t diventa 0 = −1. Va notato che (a′) dice anche "se u non ha zeri … ogni u ha una legge": la frase "mai identificabile" è quindi vera nel regime che (a′) ha in mente (u senza zeri), ma è enunciata senza quella restrizione. Riparazione (DICT-2): chiamare "identificabile" la proprietà ker Φ_u = 0 (unicità condizionata), oppure scrivere "se esiste una legge, non è unica".

**P2 — accolto, stessa causa di P1.** I "⟺" di (b′) e del trasporto sono corretti se "identificabile" significa ker Φ_u = 0 (è esattamente (II)), falsi in (⇒) con la definizione "al più una legge" per i dati che falsificano la classe e hanno un aperto di zeri. Il controesempio u = t + ψ(x) con ψ′ = 0 su un intervallo è corretto (non c'è legge perché u_t = 1, u_x = 0 lì). Lo script K5 dell'attaccante non calcola la conclusione, ma il controesempio è elementare e l'ho verificato a mano. Si ripara con DICT-2. Conseguenza per I-LIM: la frase "(H-ID) vale … quando {u_x ≠ 0} è denso" resta corretta, perché (H-ID) presuppone già l'esistenza di una legge.

**P3 — accolto.** Lo avevo trovato in modo indipendente con u = x³ (`dict_check` G1: il quoziente è 6/x², reale, ma non si estende in x = 0). Il controesempio dell'attaccante u = e^{−it}(x + x²) è più forte, perché qui −L_0u(t,0) = −2e^{−it} ≠ 0 mentre A_u(t,0) = 0, quindi u falsifica la classe per (III). Riparazione (DICT-3): "⟺" solo per u senza zeri; in generale (⇒) soltanto, con la condizione aggiuntiva iu_t + u_xx = 0 su Z(u) e il problema di divisione (Q3).

**P4 — accolto.** (∇ − iA)²u = Δu − 2iA·∇u − i(div A)u − |A|²u: il termine div A contiene derivate dell'incognita e |A|² è quadratico, quindi il quadro L_0 + Σθ_kT_k non si applica. Ho rifatto il calcolo delle differenze di leggi: con (A, V) e (A + B, V + δV) leggi reali per lo stesso u, δV = −2iB·∇u/u − i div B − 2A·B − |B|², e δV reale ⟺ 2B·Re(∇u/u) + div B = 0 ⟺ div(|u|²B) = 0 (perché Re(∇u/u) = ∇|u|²/(2|u|²)). La descrizione "spazio affine sui campi a divergenza nulla" è falsa (controesempio K6 dell'attaccante: u = (2 + cos x)e^{iy}, B = (sin y, 0)). La conclusione qualitativa "le leggi, se esistono, non sono uniche per n ≥ 2" è plausibile (div(ρ²B) = 0 ha soluzioni non nulle a supporto compatto, per esempio B = ρ^{−2}∇^⊥χ in n = 2 dove ρ ≠ 0), ma non è un corollario di RANGO. Riparazione (DICT-5): togliere il caso dai corollari di RANGO e rinviare a SYS-N3 (S8-SYS, già auditato) con la condizione div(|u|²B) = 0.

**P5 — accolto.** Senza "L ∈ Ann(u)" l'inclusione stretta è falsa (u = e^t, L = τ + 5; il mio `dict_check` F1 usa L = ∂_x con u = e^{−t}sin x). La prova dà solo la disuguaglianza fra dimensioni; con L ∈ Ann(u), (L) ⊂ Ann(u) perché Ann(u) è un ideale, e l'inclusione è stretta. La frase sul caso N = 1 ("la differenza delle dimensioni è costante (= deg L)") si riferisce a dim R_{≤n} − dim (L) ∩ R_{≤n} (lo script B1 dell'autrice calcola questa), non a dim Ann − dim (L): va detto quale differenza (MINOR, dentro DICT-6).

**P6 — accolto; trovato anche dall'aggiudicatore.** La prova applica il Lemma ND su M+1 palle disgiunte B_k ⊂ U_0, ma l'indipendenza su U_0 non dà l'indipendenza su ciascuna palla. Il mio controesempio connesso (`dict_check` A1): Ω = (0,1), D_0 = moltiplicazione per φ_1 con supporto in (0; 0,3), D_1 = moltiplicazione per φ_3 con supporto in (0,7; 1). I due operatori sono indipendenti su Ω = U_0, ma un intervallo su cui sono indipendenti deve contenere [0,3; 0,7], quindi due intervalli disgiunti non possono esserlo entrambi. Come osserva l'attaccante, l'"ipotesi dichiarata" è anche vuota (U_0 = Ω la soddisfa sempre). **Il teorema è vero senza ipotesi aggiuntive**: la prova del Lemma ND dà N+1 punti y_k e getti polinomiali con matrice di valutazione invertibile, e l'invertibilità resta per piccoli spostamenti dei punti; si scelgono M+1 (N+1)-uple di punti tutti distinti e, per ciascuna, l'aperto O_m := unione di N+1 palline minuscole. Gli O_m sono a due a due disgiunti (non connessi) e su ciascuno i D_i sono indipendenti; il resto della prova (sistema M × (M+1), località, coefficiente direttore) non cambia. Verifica numerica della costruzione: `dict_check` A2 (stessi dati esatti a 10⁻¹⁶, λ_min relativo di v = 0,38). Riparazione: DICT-1.

**P7 — parzialmente risposto.** U_n è aperto nella topologia indotta da D′ se u ↦ ⟨D_iu, ψ⟩ è continua per la convergenza debole, il che vale per operatori differenziali (D_i^tψ ∈ C_c^∞) ma non per operatori continui C^∞ → D′ qualsiasi. Il testo dice "anche in topologie deboli" nel quadro generale. MINOR.

**P8 — parzialmente risposto.** L'enunciato N1(i) richiede già mappe continue a_k: P_k → X; l'accusa riguarda le applicazioni elencate nel testo (|ξ|^s non è un simbolo liscio in ξ = 0 e s ↦ ⟨ξ⟩^s è continua in S^m solo per s < m). Nel pacchetto i parametri sono razionali e i dizionari numerabili, quindi l'esito non cambia. MINOR: dichiarare che la continuità (o la σ-compattezza dell'immagine) va verificata per ogni classe citata.

**P9 — parzialmente risposto.** È un enunciato importato da CONV-T2. L'audit di S8-CONV (fix CONV-7, recepito da S8-CONV) ha già ridotto la "Lettura" Σ⁰₂/Π⁰₂ a commento. DICT §2.4(c) deve allinearsi: "verificabile nel limite, non decidibile nel limite, con qualunque successione di regole". MINOR.

**P10 — accolto.** K ≥ 2 richiede d ≥ 1 oppure m ≥ 2. MINOR.

**P11 — accolto.** L'insieme delle u differenzialmente algebriche è denso (contiene i polinomi), quindi è magro e shy ma non raro. MINOR.

**Punti che reggono (concordo con l'attaccante e con la mia verifica).** N1(i) (Riesz + Baire); Lemma ND e ND-NL; base adattata al grado; chiusura di B_n; coefficiente direttore per multilinearità; rarità di ciascun B_n e magrezza dell'unione; prevalenza con la sonda unidimensionale s ↦ sw, che non dipende da u (B_n chiuso, quindi boreliano; nessuna misurabilità universale serve); passaggio a H^m con D_i continui H^m → L²; MF3(a)–(d); RANGO (I)–(III) incluso il passo del fibrato a rango costante (basta un aperto U′ a rango costante, non serve che sia denso); Teorema A(i)–(ii); sistema M × (M+1) e coefficiente direttore in A(iii).

## Conteggio e verdetto
Punti: 11. answered_by_current_text: 0. partially_answered: 3 (P7, P8, P9; tutti minor). still_unresolved: 8 (P1–P6 major, P10–P11 minor). Nessun punto è critical sulla scala del KA: il nucleo di N1 (i), (ii), (iv), (v) e il Teorema A sopravvivono, e tutti i difetti hanno una riparazione esplicita che non indebolisce le conclusioni principali (A(iii) anzi si rafforza: l'ipotesi U_0 sparisce).

Mappa della skill: still_unresolved a gravità major, nessuno critical ⇒ **WARN (`unresolved_major_or_minor`)**, cioè, nella terminologia degli audit F8, **SURVIVES-WITH-FIXES**. Dopo il recepimento di DICT-1, DICT-2, DICT-3, DICT-5, DICT-6 lo stato proposto di DICT-N1, DICT-N1v e DICT-A è DIMOSTRATO; per DICT-RANGO i punti (I)–(III) sono DIMOSTRATO, (IV) e i corollari lo diventano con la riformulazione di DICT-2/DICT-3.
