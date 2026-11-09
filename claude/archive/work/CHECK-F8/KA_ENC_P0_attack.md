# KA ENC-P0: kill-argument avversariale

Revisore indipendente, 27/10/2026. Unica fonte letta: `work/CHECK-F8/KA_ENC_P0_input.md`. Script di controllo: `work/CHECK-F8/sympy/enc_ka_p0_checks.py`, output in `enc_ka_p0_checks.out`. Convenzioni del pacchetto: H_0 = −∂², i u_t = −u_xx + V u. Fa eccezione la lente, che usa H_0 = −½∂² come nel testo.

## Verdetto complessivo: WOUNDED

Le prove scritte di P0(a), P0(b) e POLE-N non contengono passi falsi sostanziali. Ci sono imprecisioni minori, e P0(b) regge anche fuori dal quadro hilbertiano: la riparazione è facile (P4). La tesi complessiva però è più larga di ciò che è dimostrato, e in un punto è falsa.

1. La seconda metà della tesi ("le eccezioni cambiano il tempo") è **falsa** per la classe lineare V = β(t)x. Questa comprende Avron–Herbst con β costante. Lì l'encoder puntuale più gauge ha θ = id. In generale la riparametrizzazione del tempo non è un invariante: si può sempre assorbire con un propagatore libero (P1, P2).
2. Tutti gli esempi che danno contenuto a P0′ e a POLE-N violano (H-P0) o la classe 𝔈, o entrambe. Sono la lente, Avron–Herbst, la classe quadratica di Bluman–Shtelen e gli intertwiner di Darboux su potenziali razionali di Adler–Moser. In (H-P0) su ℝ la classe puntuale più gauge si riduce al caso banale V = γ(t) (P3, P7).
3. P0(b) non copre gli encoder di tipo ENC-1, cioè C²(J) senza condizioni al bordo. Nel quadro hilbertiano con H_0 autoaggiunto su L²(J) compatto, la classe 𝔈 è quasi vuota già nel caso **autonomo**, per ragioni spettrali. Il teorema quindi non isola l'effetto della dipendenza dal tempo (P4).
4. "Commuta con ∂_t" non equivale a "indipendente da t e agisce solo in x" (P5). La conclusione "nessun encoder" dipende inoltre in modo essenziale dalla scelta di imporre (E1) su tutto 𝒴 anziché sulle soluzioni. Se (E1) si legge sulle soluzioni, compare un candidato controesempio strutturato (P6).

Nessun punto è FATAL per gli enunciati come scritti. Due punti sono CRITICAL, per la portata della tesi.

---

## P1. "Le eccezioni cambiano il tempo" è falso per la classe lineare V = β(t)x (Avron–Herbst incluso)

**Accusa.** In ENC-P0′ si afferma che le eccezioni "quadratiche" di F6-ENC "sono elementi di P0′ con θ ≠ id". Nel compito si chiede anche se Avron–Herbst cambi davvero il tempo. Non lo cambia.

**Argomento.** Lo script (parte 1) prende l'ansatz puntuale più gauge più generale compatibile con Schrödinger:

u(t,x) = r(t) e^{i(a x² + b x + d)} v(T(t), (x − ξ(t))/ρ(t)),

con i v_τ = −v_yy e V = α x² + β x + γ. Ne seguono le condizioni:
- T′ = 1/ρ² (coefficiente di v_yy);
- ρ′ = 4aρ e ξ′ = 2b + ξρ′/ρ (coefficienti di v_y);
- a′ + 4a² = −α e b′ + 4ab = −β, più l'equazione per d e r (coefficienti di v).

Con θ = T = id si ottiene ρ² = 1. Da qui a = 0, e quindi **α = 0 è forzato**, mentre β(t) e γ(t) restano arbitrari: b′ = −β, ξ′ = 2b.

Per V = β(t)x la mappa esplicita è

u(t,x) = e^{−iB(t)x − iΦ(t)} v(t, x − Ξ(t)), con B′ = β, Ξ′ = −2B, Φ′ = B².

Lo script (parte 2) verifica che il residuo si riduce esattamente all'operatore libero applicato a v. La mappa è puntuale più gauge, ha **θ = id** e vale per β(t) davvero dipendente dal tempo. Avron–Herbst (β = F costante) ne è il caso autonomo, anche lì con θ = id. La dicotomia corretta è dunque:
- per α ≢ 0 serve θ ≠ id, attraverso la condizione T′ = 1/ρ², ρ′ = 4aρ, che è la condizione di Schwarziana di Bluman–Shtelen;
- per α ≡ 0 basta θ = id.

Ne segue che la classe lineare, che è puntuale, è un elemento di P0(a), non di P0′ con θ ≠ id. Questo smentisce anche la lettura implicita secondo cui gli elementi di P0(a), i "quadri d'interazione", non sono mai strutturati: per V = β(t)x il quadro d'interazione U_0(t)W(0)U_V(t)^{−1} con W(0) = I **è** puntuale più gauge.

La prima metà della tesi resta in piedi: questi W(t) dipendono da t e non commutano con ∂_t.

**Severità: CRITICAL** (per la tesi e per la frase su F6-ENC; gli enunciati di P0′ e P0(a) restano intatti).

**Riparazione.** Riscrivere la Lettura così: "gli encoder puntuali più gauge per V non autonomo esistono esattamente nella classe di Bluman–Shtelen. Richiedono θ ≠ id se e solo se α ≢ 0 (condizione di Schwarziana). Per α ≡ 0 (Avron–Herbst e Kramers–Henneberger) sono elementi di P0(a) con θ = id, locali e dipendenti da t." Togliere "le eccezioni cambiano il tempo" dalla tesi, oppure restringerlo ad α ≢ 0.

## P2. La riparametrizzazione θ non è un invariante: P0′ e P0(a) sono in biiezione

**Accusa.** Presentare P0′ come una classe di "eccezioni" distinta da P0(a) suggerisce che il cambio di tempo sia una proprietà intrinseca dell'encoder. Non lo è.

**Argomento.** Siano W ∈ P0′ con funzione θ e W_id(t) := U_0(t − θ(t)) W(t). Allora W_id(t) = U_0(t) W(0) U_V(t)^{−1}, cioè W_id è un elemento di P0(a) con lo stesso W(0) (lo script, parte 5, controlla l'identità di fase U_0(t − θ)U_0(θ) = U_0(t)). Il passaggio vale anche al contrario per ogni θ. Ogni "eccezione che cambia il tempo" ha quindi un rappresentante con θ = id, ed è sempre un quadro d'interazione. Ciò che distingue la lente non è l'esistenza: è che il rappresentante **locale** (E3) ha θ = tan. Il cambio di tempo è dunque una proprietà della coppia (W, località), e la tesi è sensata solo se "eccezione" significa "encoder puntuale".

C'è anche una conseguenza per la regolarità. W_id contiene U_0(t − tan t), che va all'infinito per t → ±π/2. L'intervallo I resta quindi lo stesso, ma la proprietà di essere in 𝔈 non è garantita in modo uniforme.

**Severità: MAJOR.**

**Riparazione.** Enunciare P0′ come "forma normale": ogni W che manda soluzioni in soluzioni libere riparametrizzate si scrive U_0(θ(t))W(0)U_V(t)^{−1}, e P0′ ≅ P0(a) tramite W ↦ U_0(t − θ)W. Spostare il contenuto non banale nella classificazione dei rappresentanti locali (Bluman–Shtelen più P1).

## P3. Gli esempi di P0′ (lente, Avron–Herbst, classe quadratica) violano (H-P0) e 𝔈

**Accusa.** P0′ è enunciato sotto (H-P0) con W ∈ 𝔈|_I, ma nessun esempio citato soddisfa le ipotesi.

**Argomento.**
- **Potenziale illimitato.** Nella lente V = ½x², in Avron–Herbst V = Fx e in generale V = αx² + βx con (α, β) ≠ 0, V non è limitato su ℝ. Quindi V ∉ C(ℝ; B(ℋ)). In (H-P0) su L²(ℝ) l'unico elemento limitato della classe di Bluman–Shtelen è V = γ(t), cioè il caso banale di gauge. Su L²(J) con J compatto, βx è limitato, ma la traslazione di Avron–Herbst non conserva J né alcuna condizione al bordo.
- **La lente non è in 𝔈.** W(t)^{−1} contiene il chirp e^{−ix² tan t/2}, che non conserva D = H²(ℝ). Lo script (parte 4) lo mostra con f = (1+x²)^{−1/2} ∈ H²: per f vale ∫|f″|² = 27π/128, mentre |(e^{iax²}f)″| ~ 4a²|x| ∉ L². Dunque W(t)D ⊄ D per t ≠ 0, e W ∉ 𝔈. Lo stesso vale per U_osc(t), che non conserva H²: a t = π/2 è una trasformata di Fourier a meno di fase.
- **Avron–Herbst non è in 𝔈.** Il fattore e^{−iB(t)x} con B′ = β ≠ 0 non è C¹ in t su D: la derivata è −iβ x e^{−iBx}ψ, e per ψ ∈ H² non si ha in generale xψ ∈ L².

Quindi le frasi "la formula puntuale … coincide quindi con W(t)^{−1}" e "le eccezioni quadratiche sono elementi di P0′" non seguono dall'enunciato dimostrato: sono applicazioni euristiche fuori ipotesi. La formula della lente è vera (lo script, parte 3, dà residuo nullo su onde piane e su gaussiane), ma la deduzione da P0′ non è valida.

**Severità: MAJOR.**

**Riparazione.** Dimostrare l'identità della lente in modo diretto. Lo spazio di Schwartz 𝒮 è conservato sia dalla mappa puntuale sia da U_0 e da U_osc. Si verifica che la mappa manda soluzioni libere con dato in 𝒮 in soluzioni dell'oscillatore, e si conclude per unicità del gruppo unitario e^{−itH_osc} (H_osc è essenzialmente autoaggiunto su 𝒮) e per densità. Si fa lo stesso per Avron–Herbst. In alternativa si formula una versione P0′-bis con V illimitato e un core comune invariante. In ogni caso va scritto esplicitamente che gli esempi sono fuori (H-P0).

## P4. P0(b) non copre gli encoder di tipo ENC-1, e in L²(J) la classe 𝔈 è quasi vuota già nel caso autonomo

**Accusa.** La tesi "nessun encoder strutturato" riguarda gli encoder di tipo ENC-1 (Volterra su C²(J) senza condizioni al bordo), mentre P0(b) è dimostrato solo per W ∈ B(L²(J)) con WD ⊂ D e H_0 autoaggiunto.

**Argomento.**
- **ENC-1 è fuori da 𝔈.** H_0 autoaggiunto su L²(J) compatto richiede condizioni al bordo, per esempio di Dirichlet. Un W_q di Volterra con base in x_0 − a lascia invariato il valore in x_0 − a, ma non conserva la condizione nell'altro estremo. Quindi W_q D ⊄ D e W_q ∉ 𝔈.
- **Argomento spettrale.** Ogni W limitato con nucleo finito e H_0W = W(H_V − c) su D manda autovettori φ_n di H_V in autovettori di H_0 con autovalore λ_n − c, oppure in 0. Fuori da un numero finito di indici, quindi, σ(H_V) − c ⊂ σ(H_0). Per q generico questo è falso: la classe 𝔈 contiene encoder a nucleo finito solo per coppie (quasi) isospettrali (tipo Pöschel–Trubowitz).
- **Conseguenza.** In L²(J) P0(b) esclude per V non autonomi una classe che è vuota già per quasi tutti i V autonomi. Il teorema non isola l'effetto della dipendenza dal tempo, che invece è ciò che la tesi vuole affermare.

L'argomento di P0(b) però è puramente algebrico, e la riparazione funziona.

**Severità: MAJOR** (sovrastima di portata; la sostanza regge).

**Riparazione: P0(b) algebrico.** Siano 𝒴 = C²(J), W: C⁰(J) → C⁰(J) lineare (una Volterra di seconda specie agisce su C⁰) e V(t,·) ∈ C⁰(J). Supponiamo W(L_0 + V(t))f = (L_0 + c(t))Wf per ogni f ∈ C²(J) e ogni t. Per sottrazione W(m f) = 0 per ogni f ∈ C², con m := V(t) − V(s) − (c(t) − c(s)).
- Se W è di Volterra, è iniettivo su C⁰, quindi m f ≡ 0 per ogni f, quindi m ≡ 0.
- Se W ha nucleo finito: se m(x*) ≠ 0, m non si annulla su un intervallo, e le funzioni bump f_k a supporti disgiunti danno infinite m f_k indipendenti nel nucleo. Contraddizione.

Non servono né la struttura hilbertiana né il propagatore. Conviene sostituire o affiancare l'enunciato hilbertiano con questo. Si noti che P0(b), anche nella versione attuale, non usa mai il propagatore U_V: lo si dica, così che P0(b) non erediti la dipendenza da CON-FONTE (vedi P8).

## P5. "Commuta con ∂_t" non equivale a "indipendente da t e agisce solo in x"

**Accusa.** ENC-D dice "W commuta con ∂_t quando agisce solo in x", che è un'implicazione in una sola direzione. La tesi usa invece l'equivalenza: P0(b) tratta solo W indipendenti da t e agenti solo in x, ma la tesi dice "nessun encoder … che commuti con ∂_t".

**Argomento.** Su funzioni di (t,x), commutano con ∂_t anche operatori non locali in t:
- le traslazioni temporali T_h u(t) = u(t + h);
- ∂_t stesso;
- le convoluzioni in t, k(∂_t) ⊗ A.

Nessuno di questi è "indipendente da t e agente solo in x". Il buco però si chiude per c costante, con lo stesso trucco. Se W commuta con le traslazioni temporali e

W(i∂_t − H_0 − V(t)) = (i∂_t − H_0 − c)W

come operatori su funzioni spazio-tempo, si coniuga con T_h e si sottrae. Si ottiene W·(V(·+h) − V(·)) = 0 come moltiplicazione spazio-temporale. Con nucleo finito su 𝒴 ne segue V(t+h, x) = V(t, x), cioè V autonomo. Con c(t) non costante la relazione diventa W Δ_hV = (Δ_h c)·W, e un W non locale in t non commuta in generale con la moltiplicazione per Δ_h c. Questo sotto-caso resta scoperto, anche se non sembra produrre controesempi.

**Severità: MINOR** (riparabile; vale come lacuna di enunciato).

**Riparazione.** Aggiungere un lemma: "se W è definito su uno spazio di funzioni spazio-tempo invariante per traslazioni, commuta con T_h per ogni h, ha nucleo finito e c è costante, allora V è autonomo". Oppure restringere la tesi alla lettera a "W indipendente da t e agente solo in x".

## P6. (E1) su tutto 𝒴 contro (E1) sulle soluzioni: candidato controesempio strutturato con V davvero non autonomo

**Accusa.** La conclusione "nessun encoder strutturato" dipende dal leggere (E1) come "nucleo finito su tutto 𝒴". La nozione naturale di encoder, cioè iniettivo sullo spazio delle soluzioni e quindi senza perdita di informazione sul dato, è più debole. Con essa esiste un candidato strutturato.

**Argomento.** Siano ω ⊂ J un sottointervallo aperto e V(t,x) = V_0(x) + χ(x) cos t, con χ ∈ C_c^∞(J ∖ ω̄) non nulla. V è davvero non autonomo, ma su ω coincide con V_0. Sia W_{V_0,ω} l'encoder di Volterra ENC-1 su C²(ω), senza condizioni al bordo, e

W := W_{V_0,ω} ∘ (restrizione a ω).

La restrizione commuta con L perché L è locale. Quindi W L_{V(t)} f = W_{V_0,ω}(L_{V_0} f|_ω) = L_0 W f per ogni f ∈ C²(J) e ogni t. Ne segue:
- W è indipendente da t, agisce solo in x e commuta con ∂_t;
- W è esplicito (E3) e soddisfa (E2) con c = 0;
- W manda soluzioni su ℝ×J in soluzioni libere su ℝ×ω senza condizioni al bordo, esattamente nel modello ENC-1.

ker W contiene tutte le f nulle su ω, quindi (E1) su 𝒴 fallisce. Tuttavia W è iniettivo sulle soluzioni se vale la continuazione unica: una soluzione nulla su ℝ×ω dev'essere nulla. La superficie x = cost è non caratteristica per Schrödinger, e i coefficienti sono analitici in t. Questo è il quadro del teorema di Tataru (Robbiano–Zuily–Hörmander) sulla continuazione unica per coefficienti parzialmente analitici: plausibile ma **da verificare**, CON-FONTE.

Se la continuazione unica vale, la tesi "nessun encoder strutturato per V davvero non autonomo che commuti con ∂_t" è falsa per la nozione "iniettivo sulle soluzioni", e vera solo per la nozione "nucleo finito su 𝒴". Il caso è lo stesso di P0(b) con un'osservazione in più: basta che V sia autonomo su una regione aperta. In modo analogo, (H-P0) mette sorgente e bersaglio nello stesso ℋ, ed esclude così anche encoder tra spazi diversi (L²(J) → L²(ω)).

**Severità: CRITICAL** se (E1) si legge sulle soluzioni; MAJOR come minimo, come ambiguità di definizione che regge la tesi.

**Riparazione.** Dire esplicitamente che (E1) è "nucleo finito su 𝒴", e che con (E1) sulle soluzioni la tesi richiede che V(t,·) − V(s,·) non sia costante su nessun aperto. Più precisamente, P0(b) andrebbe riformulato così: "gli encoder strutturati indipendenti da t vedono solo la regione {x : V(·, x) − c(·) è autonomo}". Verificare o citare la continuazione unica laterale per Schrödinger 1D con coefficienti analitici in t.

## P7. POLE-N: ipotesi vuote per gli esempi motivanti, e conclusione di "Lettura" sovrastimata

**Accusa.** POLE-N è enunciato per W ∈ 𝔈 (limitati) e V limitati, ma è motivato con i potenziali razionali di Adler–Moser e con gli intertwiner di Darboux differenziali.

**Argomento.**
- **Fuori ipotesi.** I potenziali razionali di Adler–Moser hanno poli doppi (reali, oppure complessi in movimento): V ∉ L^∞, e per poli complessi V non è nemmeno autoaggiunto. Gli intertwiner di Darboux W(t) = ∂_x − (log ψ(t,·))′ sono differenziali e illimitati, e non stanno in B(ℋ). Gli esempi citati violano quindi sia (H-P0) sia 𝔈, e l'enunciato dimostrato non li tocca.
- **La classe 𝔈 non è vuota.** Per potenziali limitati riflessionless, per esempio i multisolitoni KdV V(t,x) = −2∂_x² log τ, la parte unitaria della decomposizione polare della catena di Crum, oppure W = Ω_±^* (operatori d'onda), è limitata, ha nucleo finito (gli stati legati) e intreccia istantaneamente H(t) con H_0. Su questi POLE-N si applica davvero, e la conclusione regge.
- **La prova.** (INT) più l'intrecciamento istantaneo danno W′ = 0 su D denso, quindi W è costante, e si conclude con P0(b) con c costante. È corretta.
- **Sovrastima.** La "Lettura" ("la strada POLE … per B2 si richiude") esclude solo che gli intertwiner **istantanei** siano encoder. Per P0(a), W̃(t) = U_0(t)W(0)U_V(t)^{−1}, con W(0) l'intertwiner istantaneo a t = 0, è sempre un encoder. Non è strutturato, ma la strada POLE potrebbe passare per un rappresentante locale diverso: P1 mostra che succede per V lineare.

**Severità: MAJOR** (portata ed esempi); la prova formale è OK.

**Riparazione.** Riformulare POLE-N con esempi dentro le ipotesi (multisolitoni riflessionless più parte polare, oppure operatori d'onda), oppure enunciarlo algebricamente per W differenziale su C^∞(J) con l'argomento algebrico di P4. Limitare la "Lettura" agli intertwiner istantanei.

## P8. (H-P0): esistenza di soluzioni forti con V solo continuo in norma (VAR-P11) sospetta

**Accusa.** (H-P0) assume l'esistenza di un propagatore che conserva D e dà soluzioni forti, e attribuisce questo fatto, per V(t) di moltiplicazione limitata e continua in norma, a VAR-P11 e a "Dyson–Phillips, Pazy cap. 5".

**Argomento.** Per una perturbazione limitata B(t) solo continua, i teoremi standard danno un sistema di evoluzione **mild**. Per avere U(t,s)D ⊂ D e soluzioni classiche servono di solito B ∈ C¹ forte, oppure B(t)D ⊂ D, oppure condizioni di tipo Hölder (Pazy cap. 5, teoremi sulle perturbazioni limitate; Kato nel caso iperbolico). È lo stesso fenomeno del problema non omogeneo u′ = Au + f con f solo continua (Pazy cap. 4), dove la soluzione mild può non essere classica. Non ho un controesempio esplicito con V di moltiplicazione, e VAR-P11 non è nel materiale fornito: lo segnalo come sospetto, non come falsità. L'ipotesi è comunque enunciata come ipotesi, e P0(a) e P0′ restano corretti in forma condizionale. Per P0(b) e POLE-N l'ipotesi non serve.

**Severità: MAJOR** se VAR-P11 usa solo la continuità in norma; MINOR per gli enunciati di P0, che la assumono.

**Riparazione.** Verificare VAR-P11. Se serve, chiedere V ∈ C¹(ℝ; B(ℋ)) in senso forte, che è il caso coperto da Pazy e Kato. Annotare che P0(b) e POLE-N non dipendono dal propagatore.

## P9. P0(a): imprecisioni minori nella prova

- **Errore di categoria.** In (⇐) si scrive "M := W(0) ∈ 𝔈", ma M è un operatore e 𝔈 è una classe di funzioni t ↦ W(t). Si intende MD ⊂ D.
- **Continuità nel secondo argomento.** (H-P0) chiede la continuità in t nella norma del grafo di U_V(t,s). La prova usa φ(t) = U_V(0,t)ψ, cioè la continuità e la derivata nel **secondo** argomento. Va detto esplicitamente.
- **Struttura del (⇐).** Il grafo chiuso serve solo a dimostrare che W(t) := U_0(t)MU_V(t)^{−1} è C¹ (continuità di U_0(t)H_0Mφ(t)) per ogni M con MD ⊂ D. Nell'enunciato, invece, W ∈ 𝔈 è già un'ipotesi, quindi per (⇐) basta la derivabilità. Il passo dimostra di più di quanto serve (il che va bene), ma andrebbe enunciato: "per ogni M ∈ B(ℋ) con MD ⊂ D, la famiglia U_0 M U_V^{−1} è in 𝔈 e soddisfa (INT)". La chiusura di H_0M|_D come operatore da (D, ‖·‖_G) a ℋ è corretta: M è limitato e H_0 è chiuso.
- **Il resto della prova.** (⇒), con Banach–Steinhaus e la regola del prodotto su u(t) ∈ D, e l'unicità libera sono corretti. L'estensione da D a ℋ è corretta per limitatezza.
- **Lemma del rango in P0(b).** È corretto per la misura di Lebesgue (non atomica). Gli E_k vanno presi di misura finita, così che 1_{E_k} ∈ L². Il passaggio da "W m ψ = 0 per ψ ∈ D" a "Ran(m) ⊂ ker W" usa la densità di D, la limitatezza di m e la chiusura di ker W: va scritto.

**Severità: MINOR.**

**Riparazione.** Correggere le diciture come indicato.

## P10. Sovrastime residue

- **"Nessun encoder … nemmeno modulo costanti".** È vero solo nel senso di P4 e P6: indipendente da t, nucleo finito su 𝒴, stesso spazio.
- **"Con trasformazioni non locali esistono anche V non quadratici".** È banalmente vero, perché ogni V ha il quadro d'interazione (P0(a)), quindi l'affermazione non ha contenuto. Va riformulata come "per E3 non locale, cioè di Volterra o integrale esplicito, la classificazione è aperta".
- **NOTAZIONE: "q costante non ha intertwiner differenziale con c = 0".** È plausibile ma non dimostrato qui. Con c = q esiste invece l'intertwiner banale W = I.

**Severità: MINOR.**

---

### Tabella riassuntiva

| Punto | Oggetto | Severità |
|---|---|---|
| P1 | "le eccezioni cambiano il tempo" falso per V = β(t)x (Avron–Herbst: θ = id) | CRITICAL |
| P2 | θ non invariante, P0′ ≅ P0(a) | MAJOR |
| P3 | esempi di P0′ fuori da (H-P0) e 𝔈 (V illimitato, chirp non conserva H²) | MAJOR |
| P4 | P0(b) non copre ENC-1; 𝔈 quasi vuota in L²(J) già nel caso autonomo; riparazione algebrica | MAJOR |
| P5 | "commuta con ∂_t" ≠ "indipendente da t" | MINOR |
| P6 | (E1) su 𝒴 contro (E1) sulle soluzioni: restrizione a ω più Volterra | CRITICAL (con riserva di continuazione unica) |
| P7 | POLE-N: Adler–Moser e Darboux fuori ipotesi; "Lettura" sovrastimata | MAJOR |
| P8 | soluzioni forti con V solo C⁰ in norma (VAR-P11) sospette | MAJOR / MINOR |
| P9 | imprecisioni in P0(a) e nel lemma del rango | MINOR |
| P10 | sovrastime verbali | MINOR |
