# Kill-argument su ENC-N1 (F6) ed ENC-N1′ (i)–(v)

Revisore avversariale indipendente, 27/10/2026. Unica fonte letta: `work/CHECK-F8/KA_ENC_N1_input.md`. Script di controllo: `work/CHECK-F8/sympy/enc_ka_n1_checks.py`, eseguito con `.venv\Scripts\python.exe -I`. Verifica cinque cose: (a) e^{iθ(t)}u risolve l'equazione con potenziale q − θ′(t), non con q; (b) e^{−ict} manda le soluzioni con potenziale q nelle soluzioni con potenziale q + c; (c) con DM-φ, (iw_t + w_xx)/w = q(x) − θ′(t); (d) la famiglia stretta di Volterra viola (C) sulla classe {c}; (e) l'identità di intrecciamento di (iv).

## Verdetto complessivo: WOUNDED

Non ho trovato un errore fatale. Il verdetto "ENC-N1 (F6) FALSO" regge, e anzi regge in forma più forte di quella dichiarata, ma per la ragione sbagliata. Il controesempio scritto è banale (v = 0) e non confuta la versione caritatevole dell'enunciato. Quella versione è però confutata dal punto (iv) dello stesso pacchetto.

ENC-N1′ è corretto come logica, ma ha più problemi:
- (i)–(iii) sono tautologie. In particolare (iii) ottiene la "forma richiesta dal roster" per ipotesi.
- Il quadro è mal posto sotto DM-φ: un insieme delle soluzioni "chiuso per ~" non è uno spazio lineare, e "modulo costanti" è ridondante o indefinito.
- "Esiste un encoder cieco" dipende dalla famiglia {W_V} scelta, non solo da (𝒱, modello di dato).
- Due delle tre istanze in (v) dicono più di quanto le premesse permettono.

## P1. Con DM-φ il quadro è mal posto: "𝒮_V chiuso per ~" e "W_V lineare su 𝒮_V" non stanno insieme

**Accusa.** Il quadro chiede che 𝒮_V sia l'insieme delle soluzioni, chiuso per ~ e contenente 0, e che W_V: 𝒮_V → 𝒮_0^{(c_V)} sia lineare. Sotto DM-φ le due richieste sono incompatibili, se prese alla lettera.

**Argomento.**
- Sia u soluzione di iu_t = −u_xx + V(x)u. Allora e^{iθ(t)}u risolve l'equazione con potenziale V − θ′(t) (script, punto (a)). Quindi l'insieme letterale delle soluzioni è chiuso per ~ solo rispetto alle fasi costanti. Per V indipendente dal tempo non è mai chiuso rispetto all'intera DM-φ.
- Per rendere vera l'ipotesi bisogna prendere la saturazione sat(𝒮_V) = {e^{iθ(t)}u : u soluzione}. Questa non è uno spazio vettoriale: e^{iθ_1}u_1 + e^{iθ_2}u_2 in generale non è della forma e^{iθ}·(soluzione). Quindi "W_V lineare su 𝒮_V" non ha senso come scritto.
- Allo stesso modo, sotto DM-φ il codominio "𝒮_0^{(c_V)}" va saturato. Ma le saturazioni di 𝒮_0^{(c)} coincidono per ogni c, perché e^{−ict} è una fase ammessa.
- Il punto conta per la sostanza: il controesempio (iv) (vedi P5) funziona **solo** con la lettura saturata. Con gli insiemi letterali, u ∈ 𝒮_{q_0} ∩ 𝒮_{q_0+c} dà c·u = 0, quindi u = 0. L'intersezione si riduce a {0}, l'identificabilità congiunta vale e (iv) non è più un controesempio.

**Severità proposta.** MAJOR. Il problema si ripara senza toccare i risultati, ma oggi la buona posizione del quadro, da cui dipende (iv), non è scritta.

**Riparazione.**
- W_V va definito come operatore lineare sullo spazio ambiente 𝒴 delle funzioni di (t, x), con azione solo in x, così da commutare con la moltiplicazione per e^{iθ(t)}.
- Va posto 𝒮_V^~ := sat(𝒮_V^{lett}), richiedendo W_V(𝒮_V^~) ⊆ sat(𝒮_0) e la compatibilità W_V(e^{iθ}u) = e^{iθ}W_V u.
- Va dichiarato esplicitamente che sotto DM-φ "𝒮_V" indica la saturazione.

## P2. 𝒪 "modulo ~ e modulo le costanti" è ridondante sotto DM-φ e indefinito sotto DM3

**Accusa.** La definizione di 𝒪 non è coerente nei due modelli di dato.

**Argomento.**
- Sotto DM-φ la costante c_V si traduce nella fase e^{−ic_V t}, che è già assorbita da ~. Quindi "modulo costanti" non aggiunge nulla.
- Sotto DM3 le uscite di potenziali diversi vivono in spazi diversi, 𝒮_0^{(c_V)} ≠ 𝒮_0^{(c_{V′})}. Per confrontarle bisogna identificare v ∈ 𝒮_0^{(c)} con e^{ict}v ∈ 𝒮_0. Questo equivale a introdurre di nascosto una DM-φ ristretta alle fasi affini, cioè una perdita d'informazione che DM3 non prevede.
- Anche Φ(V, v) := W_V^{−1}v "su 𝒱 × 𝒮" ha un problema di tipo quando c_V varia: 𝒮 dipende da V.
- Il problema non tocca le istanze in cui c ≡ 0 (Volterra stretto, DM3).

**Severità proposta.** MINOR.

**Riparazione.** Definire 𝒪 := sat(𝒮_0)/~ e la normalizzazione N_V(v) := e^{ic_V t}v. Porre poi E(u) = [N_V W_V u]. Sotto DM3, dichiarare che (E2′) con c ≠ 0 introduce esattamente l'equivalenza per fasi affini, oppure limitarsi a c = 0.

## P3. Il controesempio a ENC-N1 (F6) è banale; la versione caritatevole è vera in quell'istanza, ma resta falsa in generale per (iv)

**Accusa.** "Φ(V, 0) = 0 = Φ(V′, 0)" sfrutta solo lo zero, una degenerazione ovvia. Non dice nulla sul contenuto dell'enunciato.

**Argomento.**
- **Versione caritatevole F6\*:** "encoder cieco ⟺ Φ è iniettiva su 𝒱 × (𝒮 ∖ {0})", oppure modulo ~ su v ≁ 0.
- **Nell'istanza del controesempio dichiarato** (V ∈ C¹(J), DM3, Volterra) F6\* è **vera**. Se Φ(V, v) = Φ(V′, v′) = u con v, v′ ≠ 0, allora u ≢ 0 è soluzione comune. Per VAR-T1(b), V = V′, quindi v = W_V u = v′. Il controesempio scritto dunque non confuta F6\*.
- **In generale**, Φ iniettiva su v ≠ 0 equivale a identificabilità congiunta più iniettività di W_V. Quindi F6\* equivale a "cieco ⟺ identificabile".
  - Il verso ⇐ di F6\* è vero, per (ii).
  - Il verso ⇒ è falso, per (iv). Lì Φ(q_0, v) = W_{q̂}^{−1}v = Φ(q_0 + c, v) con v ≠ 0 (sotto saturazione, script punto (b)), eppure l'encoder cieco esiste.
- Quindi F6 resta falso anche nella lettura caritatevole, ma il testimone corretto è (iv), non il controesempio con v = 0.
- Errore di citazione: "l'encoder cieco esiste, per il punto (iii)". In realtà si usa (ii), cioè identificabilità ⇒ (C). (iii) ⇐ è proprio (ii).

**Severità proposta.** MAJOR, come presentazione e portata. Il verdetto FALSO è giusto, la giustificazione è debole.

**Riparazione.** Scrivere: "FALSO come scritto (banalmente, v = 0); falso anche nella forma caritatevole F6\* (v ≠ 0), che equivale a 'cieco ⟺ identificabile': il verso ⇐ vale per (ii), il verso ⇒ fallisce per (iv)". Correggere il rimando a (ii).

## P4. (i)–(iii) sono tautologiche; (iii) dà la "forma richiesta dal roster" solo per ipotesi

**Accusa.** ENC-N1′ è etichettato "Teorema", ma (i)–(iii) sono riformulazioni delle definizioni.

**Argomento.**
- **(i).** "E esiste ⟺ (C)" è la definizione stessa di funzione ben definita. A E non si chiede alcuna struttura: niente (E3), niente continuità, niente misurabilità.
- **(iii).** (S) dice: "su ogni sovrapposizione non banale con V ≠ V′ le uscite differiscono". (C) dice: "su ogni sovrapposizione le uscite coincidono". Quindi (S) ∧ (C) equivale esattamente all'assenza di sovrapposizioni non banali, cioè all'identificabilità. Inoltre l'identificabilità implica (S) a vuoto. Dunque (iii) si riduce all'equivalenza "identificabilità ⟺ (S) ∧ (C)", che si ottiene semplicemente aprendo le definizioni.
- (S) non si può verificare indipendentemente dall'encoder, ed è "la negazione di (C) sulle sovrapposizioni".
- In tutte le istanze citate in (v), (S) vale **solo a vuoto**, cioè solo perché l'identificabilità vale già. Il pacchetto non mostra nessuna istanza in cui (S) sia non vacua e quindi faccia lavoro.
- (P5 suggerisce un candidato: la famiglia stretta su {q_0 + c} sotto DM-φ.)
- Presentare (iii) come "la forma richiesta dal roster" è quindi una sovrastima. Il roster ottiene l'equivalenza solo perché la si è inserita nell'ipotesi.
- La sezione "Lettura" lo ammette in parte ("il contenuto non banale non è l'equivalenza logica"), ma l'etichetta "Teorema" e la frase sul roster restano.

**Severità proposta.** MAJOR, per portata ed etichettatura.

**Riparazione.**
- Rietichettare (i)–(iii) come "Osservazione (logica)".
- Dire esplicitamente che (S) ∧ (C) ⟺ identificabilità per definizione.
- Dare un esempio con (S) non vacua, oppure dichiarare che non se ne conoscono.
- Togliere "è la forma richiesta dal roster", oppure scrivere "il roster è soddisfatto solo nella forma condizionale, con ipotesi equivalente alla tesi".

## P5. "Esiste un encoder cieco" dipende dalla famiglia {W_V} scelta: (iv) funziona con W_{q̂}, fallisce con la famiglia stretta

**Accusa.** Il quadro fissa "per ogni V un encoder W_V", ma l'encoder non è unico. Né (C) né (S) sono proprietà di (𝒱, modello di dato).

**Argomento.**
- Classe {c : c ∈ ℝ} (cioè q_0 = 0) sotto DM-φ, con la famiglia **stretta** di ENC-1: W_c di Volterra per il potenziale costante c, con W_c L_c = L_0 W_c, che esiste per Volterra anche se non esiste per via differenziale.
- Si prenda u = e^{−iλt} cos(√λ (x − x_0)). È soluzione per V = 0, ed e^{−ict}u è soluzione per V = c, quindi u sta nell'intersezione saturata.
- Con la normalizzazione di Cauchy in x_0, si ha W_0 u = u e W_c u = e^{−iλt} cos(√(λ+c)(x − x_0)). Il rapporto dipende da x (script, punto (d)), quindi le due uscite non sono equivalenti per ~. Dunque (C) **fallisce** e con questa famiglia non c'è encoder cieco.
- Con la famiglia normalizzata W_{q̂} di (iv), invece, (C) vale.
- Quindi l'affermazione "l'encoder cieco esiste" in (iv), e la lettura (b) "con DM-φ ed (E2′) l'encoder cieco esiste lo stesso", vanno relativizzate alla famiglia.
- Il fatto ha anche un lato positivo: la famiglia stretta è un candidato naturale per un'istanza in cui (S) non è vacua, cosa che manca in P4. Va però verificato su tutte le u comuni, non solo sugli autostati.
- Riserva: il conto di (d) assume che "normalizzato dai dati di Cauchy in x_0" voglia dire che W manda la soluzione con dati di Cauchy (α, β) in x_0 nella soluzione libera con gli stessi dati. È la lettura naturale di ENC-1, ma ENC-1 non è riportato nel testo.

**Severità proposta.** MAJOR.

**Riparazione.** Definire "encoder cieco per la famiglia 𝒲 = {W_V}" e quantificare: "esiste una famiglia 𝒲 ammissibile per cui...". In (iv), dire che la famiglia stretta viola (C) e che è la normalizzazione q̂ a renderla vera.

## P6. (iv) è corretto nella lettura saturata, ma il controesempio è "di gauge" ed è appoggiato a citazioni improprie

**Accusa.** Ho verificato l'identità e la compatibilità con ~. Il contenuto del controesempio però è più debole di quanto suggerisce il testo.

**Argomento.**
- **Identità.** L_{q_0+c} = L_{q̂} + q_0(x_0) + c, perché q̂ = q_0 − q_0(x_0) è lo stesso per tutta la classe. Usando W_{q̂}L_{q̂} = L_0 W_{q̂} e il fatto che una costante commuta con W, si ottiene W_{q̂}L_{q_0+c} = (L_0 + q_0(x_0) + c)W_{q̂}. **Corretta.**
- **Compatibilità con ~.** W_{q̂} agisce solo in x, quindi W(e^{iθ(t)}u) = e^{iθ(t)}Wu. **Corretta.**
- **Evoluzione.** Se iu_t = L_q u e v = Wu, allora iv_t = (L_0 + c_V)v ed e^{ic_V t}v è libera, coerentemente con (E2′).
- **Natura del controesempio.** La non identificabilità è proprio il gauge del modello di dato: sat(𝒮_{q_0}) = sat(𝒮_{q_0+c}) via e^{−ict} (script, punto (b)). (iv) mostra quindi soltanto che la nozione giusta è l'identificabilità **modulo il gruppo di gauge del dato**.
- Con quella nozione, (iv) non è più un controesempio. Sotto DM-φ, (iw_t + w_xx)/w = q(x) − θ′(t) (script, punto (c)), quindi q è identificato modulo costanti da qualunque dato non nullo regolare.
- **Citazioni.** "V identificato solo modulo costanti (VAR-P4(a))" cita un fatto sugli stati **stazionari**, mentre la non identificabilità che serve è immediata dalla saturazione. Il fatto positivo "identificato modulo costanti" per dati generali segue dalla formula (c), non da VAR-P4.
- **Regolarità.** Con θ arbitraria, e^{iθ}u non è C^{1,2}. Per applicare VAR-T1(b) a dati saturati serve θ ∈ C¹.

**Severità proposta.** MINOR. Il punto è corretto, va solo ridimensionata la portata e sistemate le citazioni.

**Riparazione.** Aggiungere: "(iv) è un controesempio di gauge; modulo il gauge del dato (V ~ V + cost) l'identificabilità vale per la formula q − θ′". Sostituire la citazione VAR-P4(a) con la saturazione e la formula (c). Richiedere θ ∈ C¹.

## P7. Istanza magnetica di (v): un non sequitur che contraddice (iv)

**Accusa.** "L'identificabilità di (A, V) fallisce (SYS-N3). Coerentemente, un encoder cieco che tolga A non è disponibile."

**Argomento.**
- Per (iv) dello stesso teorema, la non identificabilità **non** implica la non esistenza dell'encoder cieco. Questa implicazione vale solo con (S), e (S) non è verificata per il caso magnetico.
- Anzi, la non identificabilità magnetica è tipicamente di gauge, (A, V) → (A + ∇χ, V), proprio come in (iv). Proprio in quella situazione un encoder gauge-invariante potrebbe soddisfare (C).
- Il quadro inoltre è unidimensionale (J intervallo, L_q = −∂_x² + q), mentre il caso magnetico vive in n ≥ 2: è fuori dal quadro. "Coerentemente" non è giustificato.

**Severità proposta.** MAJOR, per sovrastima di portata dentro il teorema.

**Riparazione.** Togliere la frase, oppure scrivere: "fuori dal quadro (n ≥ 2); l'identificabilità di (A, V) fallisce (SYS-N3); se esista un encoder cieco gauge-invariante è aperto. Per (iv), la non identificabilità da sola non lo esclude."

## P8. Istanza V(t, x) di (v): "domanda vuota" vale solo per encoder indipendenti dal tempo

**Accusa.** P0(b) esclude soltanto gli encoder strutturati **indipendenti dal tempo**. ENC-D, (E2′), ammette esplicitamente encoder W(t) dipendenti dal tempo nel caso non autonomo.

**Argomento.** La domanda sull'encoder cieco con W(t) strutturato non è vuota: è aperta. Il quadro d'interazione U_0 U_V^{−1} è escluso da (E3), ma questo non esclude altri W(t) espliciti. Inoltre il richiamo alle fasce di silenzio (VAR-T1(c)) riguarda l'identificazione, non l'encoder.

**Severità proposta.** MINOR o MAJOR (portata). La propongo MAJOR solo se la frase viene usata come chiusura della questione nel roster; altrimenti MINOR.

**Riparazione.** Scrivere: "vuota per encoder strutturati indipendenti dal tempo (P0(b)); aperta per W(t) strutturati dipendenti dal tempo".

## P9. Istanza V(x), DM3: corretta sotto le ipotesi, con riserve su "q.o." e "costruttivo"

**Accusa.** L'istanza segue dalle ipotesi dichiarate solo se si precisano alcuni punti.

**Argomento.**
- **Portata di VAR-T1(b).** VAR-T1(b) identifica V "q.o.". Per dedurre 𝒮_V ∩ 𝒮_{V′} = {0} per V ≠ V′ in C¹(J) serve che la proiezione su J dell'insieme {u ≠ 0} sia densa (o di misura piena) in J. Questo richiede una continuazione unica: u ≡ 0 su (0, T) × J′ ⇒ u ≡ 0. Non è detto se sia contenuta in VAR-T1(b). Poi la continuità di V − V′ dà l'uguaglianza ovunque.
- **Formule.** Le tre formule sono verificate: Schrödinger q = (iu_t + u_xx)/u, onda q = (u_xx − u_tt)/u, calore q = (u_xx − u_t)/u.
- **Fuori quadro.** Onda e calore però sono fuori dal quadro (E2′), che è scritto con i∂_t. Serve un rimando a un quadro analogo.
- **"Costruttivo".** Lo è solo in senso algebrico esatto: divisione per u e derivate seconde del dato, quindi nessuna stabilità.

**Severità proposta.** MINOR.

**Riparazione.** Precisare l'ipotesi di continuazione unica o di densità. Scrivere "costruttivo (non stabile)". Segnalare che onda e calore richiedono la versione di (E2′) per i rispettivi operatori.

## P10. Dettagli formali minori

**Argomento.**
- **(i), "Equivalentemente...".** Con dati modulo ~ l'ipotesi naturale è Φ(V, v) ~ Φ(V′, v′), non l'uguaglianza. L'equivalenza con (C) vale grazie alla compatibilità con ~, ma va detto.
- **Dominio di Φ.** Φ è definita su tutto 𝒱 × 𝒮 solo se W_V è suriettivo su 𝒮_0^{(c_V)}. Per Volterra va bene (inverso di Volterra), in generale (E1) dà solo l'iniettività.
- **(ii).** "Se u ~ 0 allora [W_V u] = [0] per linearità" va bene, perché u ~ 0 implica u = 0. Nella lettura saturata (P1) la "linearità" va intesa sull'ambiente 𝒴.
- **Unicità di c_V.** Va bene: (c − c′)W = 0 con W ≠ 0 dà c = c′.

**Severità proposta.** MINOR.

**Riparazione.** Le tre precisazioni indicate sopra.

## Sintesi delle severità

- FATAL: nessuno.
- CRITICAL: nessuno.
- MAJOR: P1, P3, P4, P5, P7, P8 (quest'ultimo condizionato).
- MINOR: P2, P6, P9, P10.

Il verdetto "F6 FALSO" sopravvive e va rafforzato con (iv). ENC-N1′ sopravvive come osservazione logica, a patto di riformulare il quadro sotto DM-φ, quantificare sulle famiglie di encoder e ridimensionare le istanze (v).
