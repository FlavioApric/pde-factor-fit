# Notazione comune e quadro di lavoro (versione 1, 22/10/2026)

Fonte: `D:\piano di ricerca.md` (il piano). Questo file fissa UNA notazione per tutti i pacchetti di lavoro (WP).
Le "congetture guida" in fondo sono IPOTESI DA VERIFICARE, non risultati: ogni WP deve dimostrarle, correggerle o confutarle.

## Oggetti
- Variabili: `(t,x)` con `x ∈ ℝ` o `x ∈ 𝕋 = ℝ/2πℤ`, `t ∈ I = [0,T]`. Caso ODE: solo `x`.
- Operatore incognito (â/Â negli appunti): `L = Σ_{k=1}^N λ_k T_k`, con `T_k = ∂^{α_k}` (monomi di derivata) oppure `T_k = f_k(x)∂^{α_k}`.
  I `T_k` sono i "termini" / "componenti dell'operatore" (A8, A9).
- Simbolo: per coefficienti costanti `P(τ,ξ)` con `∂_t ↔ τ`, `∂_x ↔ ξ` (convenzione Laplace/Ehrenpreis: `e^{τt+ξx}`; per Fourier `ξ = iκ`).
- Varietà caratteristica: `V(P) = {(τ,ξ) ∈ ℂ² : P(τ,ξ) = 0}`.
- Dato: una soluzione esatta `u` (= f̂ negli appunti), `Lu = 0`, senza rumore stocastico.
- Jet / feature vector (Φ di D2, E2): `Φ(u) = (T_1 u, …, T_M u)ᵀ` su un dizionario di M termini candidati.
- Gram del jet: `𝔾(u) = ∫_Ω Φ(u) Φ(u)^* dμ` (matrice M×M, semidefinita positiva). `Lu=0 ⟺ λ ∈ ker 𝔾(u)` (con λ esteso a M componenti).
- Annullatore: `Ann(u) = {Q : Q u = 0}` — ideale di `ℂ[∂_t,∂_x]` (coeff. costanti) o ideale sinistro dell'algebra di Weyl / anello di operatori `D` (coeff. variabili).
- Classe di funzioni di un termine (C2): `K_n = ker T_n` o, per equazioni a più termini, `ker` della sotto-equazione; base/frame `{e_{n,i}}`.
- Termine di interazione: `E_int := u − Σ_n u_n` dove `u_n` è la parte di `u` attribuita alla componente n (definizione precisa da fissare nel WP2; la si deve dare per ciascun "quadro": additivo, moltiplicativo, log-simbolo).
- Semigruppi: per `u_t = A u`, `A = Σ A_n`, `S(t) = e^{tA}`, `S_n(t) = e^{tA_n}`; nucleo (kernel di convoluzione) `K_n(t,·)`.
- Matrice compagna (via b): `C(p)` per `p(D) = D^m + a_{m-1}D^{m-1}+…+a_0`.
- Tensore simbolo (via a): simbolo principale come forma simmetrica `σ_m(P) ∈ Sym^m(ℂ²)`.

## Convenzioni di scrittura per i PROOF_PACKAGE
- Lingua: italiano; matematica in LaTeX inline `$…$` / blocchi `$$…$$`.
- Ogni enunciato ha un ID: `[WPx-T#]` teorema, `[WPx-L#]` lemma, `[WPx-P#]` proposizione, `[WPx-C#]` controesempio, `[WPx-D#]` definizione, `[WPx-A#]` algoritmo, `[WPx-Q#]` problema aperto.
- Ogni enunciato riporta: ipotesi esplicite, dimostrazione completa (o "Fonte: …" con riferimento preciso se è un teorema noto della letteratura, con l'enunciato esatto), stato ∈ {DIMOSTRATO, DIMOSTRATO-CON-FONTE, CONGETTURA, FALSO (con controesempio), APERTO}.
- Ogni claim verificabile simbolicamente ha uno script SymPy in `work/WPx/sympy/` eseguito con `D:\ProblemaBase\.venv\Scripts\python.exe -I script.py`; l'output va citato.
- Collegare ogni risultato ai punti degli appunti (A1…H3) e agli item del piano (C1…C4, P1…P4, II).
- Niente numerica come METODO (vincolo k3). La numerica è ammessa solo come CONTROLLO di un enunciato.

## Congetture guida (da verificare/confutare — NON assumere)
- G1 (A8 additivo è falso in generale): se `L = L_1 + L_2` (somma di termini a coeff. costanti) allora `ker L ∩ (ker L_1 + ker L_2) ⊆ ker(L, L_1 L_2)` che ha varietà `V(P_1)∩V(P_2)`, tipicamente finita ⇒ sottospazio di dimensione finita.
- G2 (A8 vero per fattorizzazione): `P = P_1 P_2` coprimi ⇒ `ker P = ker P_1 + ker P_2` con intersezione `ker(P_1,P_2)` (dim. finita) — via la successione esatta `0→R/(P_1P_2)→R/(P_1)⊕R/(P_2)→R/(P_1,P_2)→0` e iniettività di `C^∞` (Malgrange–Ehrenpreis).
- G3 (somma di termini ⇒ prodotto): `u_t = (A_1+A_2)u` a coeff. costanti ⇒ `u = S_1(t)S_2(t)u_0` e nel dominio log-simbolo `∂_t log û(t,κ) = a_1(κ)+a_2(κ)` (additivo, lineare, O(N)). L'E_int additivo è `(K_1−δ)*(K_2−δ)*u_0` (bilineare: è la h(e_1,e_2) di P1), e per N termini l'espansione additiva ha 2^N termini (l'O(eⁿ) di B2).
- G4 (identificabilità): ODE a coeff. costanti: `u` identifica `L` (a meno di scala) ⟺ l'annullatore minimo di `u` ha grado = ordine di L. PDE di evoluzione `u_t = a(∂_x)u`: `u` identifica `a` ⟺ `supp û_0` ha almeno `deg a + 1` punti (infinito se il grado non è noto). Caso generale: chiusura di Zariski del supporto della misura di Ehrenpreis di u = V(P).
- G5 (Idea II): la "non-matrice" di E1 è una matrice sull'anello `ℂ[∂_x]` (o algebra di Weyl); i suoi invarianti completi sono il modulo `D/DL` (forma normale di Smith/Jacobson); il tensore simbolo (via a) conserva solo gli invarianti del simbolo principale.
- G6 (spazio di Hilbert da C2): lo spazio naturale è `L²(V(P), μ)` immerso tramite la trasformata di Fourier–Laplace/Ehrenpreis (l'"encoder" analitico di D1); numerabile su 𝕋, frame continuo su ℝ (risposta ad A7).
- G7 (non linearità): l'identificazione resta lineare nei coefficienti se il dizionario contiene monomi del jet (es. `u u_x`); la decomposizione in componenti richiede una linearizzazione esatta (Cole–Hopf, IST) o un'immersione (Carleman/Koopman); nel caso integrabile l'E_int ha forma chiusa (sfasamenti dei solitoni, Hirota).

---
# Versione 2 (25/10/2026, dopo il Gate 1) — aggiunte; nulla della v1 è rimosso
## Decisioni fissate
- **H0:** x ∈ ℝ (non 𝕋), t ∈ I = [0,T]. **H1:** u ∈ H^m(Ω), Ω = I × (a,b) limitato (oppure Ω ⊂ ℝ² convesso limitato); per l'identificazione non serve u ∈ L²(ℝ).
- **Componente (A8):** una componente è un **fattore** dell'operatore: per coeff. costanti i fattori della decomposizione primaria P = Π P_j^{m_j}; per coeff. variabili i fattori di Loewy / LCLM. Le classi di funzioni {e_{n,i}} di A5 sono i nuclei dei fattori.
- **Termine:** un monomio λ_k T_k di L. Dentro un fattore che è un'evoluzione del 1° ordine, ∂_t − Σ_n a_n(∂_x), i termini si leggono come coefficienti lineari del log-simbolo.
- **Classe dei coeff. variabili (default di lavoro):** polinomiali / olonomi (dimensione finita).
## Definizioni nuove
- `Z(u)`: insieme dei punti spettrali di u su V(P) [R4]. `V_u = Z(u)`-sottospazio ciclico span{T^k u} [R4-T8, R6-T4].
- `E_int` per quadro [R5-D1]: E_int^add := u − u_0 − Σ_n (S_n(t)u_0 − u_0); E_int^mult := S_1⋯S_N^{-1}S (o errore di splitting S − S_1⋯S_N); E_int^log := ∂_t log û − Σ a_n; E_int^ker := classe di u in ker L / (ker L ∩ Σ ker L_n). Per scomposizione regolarizzata: E_int^⊥ = P^⊥u (fuori dallo span del dizionario), E_int^∥ = ambiguità dentro lo span [R1].
- Stato **V-ex** = verificato solo su esempi (SymPy), non dimostrato in generale. Da usare al posto di "D" dove applicabile (obiezione O6 di DEVIL-A).
## Congetture guida — stato aggiornato (vedi research/SYNTHESIS.md §3)
- G1: vera e rafforzata per termini coprimi (R2-T3). G2: vera su ℝ / convessi (R2-T2). G3: vera **solo** per evoluzioni scalari del 1° ordine in t, coeff. costanti, senza bordo (PR-C2b P4/P5, PR-C2d). G4: forma intrinseca V(Ann u) = V(P) per P ridotto (R4-T5, da riportare su ℝ). G5: vera a meno di similitudine di Ore su ℂ(x)[∂] (R6-T5). G6: vera come quoziente (R1). G7: vera, più forte nel caso integrabile (R7).
## Nuove congetture guida (da verificare in Fase 3)
- G8 (O1): per u_t = a(∂_x)u lo strato "fattori" è banale; il contenuto per termine è interamente nel log-simbolo e nella lettura per regimi di scala [TROP-L2].
- G9 (O3): R4-T4/T5 valgono su Ω limitato ⊂ ℝ con u ∈ H^m(Ω), sostituendo i modi di Fourier con la rappresentazione di Ehrenpreis e Z(u) con il supporto spettrale analitico.

## Versione 3 (Gate 4a, 26/10/2026) — E_int non lineare
- **A9 non lineare (approvato dall'utente):** per u_t = Σ_n T_n(u), S_n(t) := flusso del solo termine T_n (semigruppo non lineare; per termini iperbolici la soluzione entropica di Kružkov, oltre lo shock). E_int^add := u − u₀ − Σ_n (S_n(t)u₀ − u₀); E^mult := S(t) − S_1(t)⋯S_N(t) (errore di splitting, dipende dall'ordine dei fattori). Al 2° ordine in t: E_int^add = (t²/2)·Σ_{m≠n} T_m′(u₀)T_n(u₀) + O(t³) (per due termini: l'anticommutatore). Esempio di riferimento (DEVIL-4, verificato): Burgers, u₀ = ε sin x ⇒ E_int^add = (3/2)νt²ε² sin 2x + O(t³, ε³).
- **Da non confondere** con E^NL (somma dei termini di Volterra di ordine ≥ 2 in ampiezza), E^trop, u − Σ (1-solitoni), E^mix: oggetti diversi, usati in Fase 4 come strumenti.
- I(u) := ideale differenziale di u; identificazione relativa: I(u) ∩ span(𝓓).

<!-- Proposta S5-FIX (26/10/2026): testo di work/S5-INT/INTEGRAZIONE_LINEARE.md §2.3, pronto da appendere in fondo a NOTAZIONE.md dal coordinatore. Modifiche rispetto alla fonte: tolto il blocco di codice; aggiunta la riga di intestazione alla tabella E_int perché sia una tabella Markdown valida. Contenuto invariato. -->

## Versione 4 (proposta S5-INT, 26/10/2026) — integrazione del pacchetto lineare; nulla di v1–v3 è rimosso
### Domini (sostituisce, per i risultati di Fase 3, la frase di v2 H1 "Ω = I×(a,b) oppure convesso")
- Ω_c: aperto connesso non vuoto di ℝ² — identificazione (C3-T1, C3-T6, P4-T2, P4-T4..T6).
- Ω_sc: Ω_c con H¹_dR(Ω) = 0 (⟺ semplicemente connesso, Rudin RCA cap. 13 per "⇐") — scomposizione per fattori (C12-T1′, C12-P10, P4-P1, R2-T3 esteso).
- Ω_R: rettangolo limitato I×J — classe 𝔅 e strato "termini" (P1, P2-T2 "⇐", P2-P5(a)).
- Ω_conv: convesso limitato — C12-T3, P2-C1, C3-P1[gen] (qui la convessità è necessaria).
- "limitato" serve solo per EP ⊂ H^m(Ω) e per gli enunciati in H^m (C12-P7: limitato, lipschitziano, connesso).
### Oggetti
- EP(Ω) := restrizioni a Ω delle somme finite Σ_k q_k(y)e^{⟨z_k,y⟩}, q_k ∈ ℂ[t,x], z_k = (τ_k,ξ_k) ∈ ℂ², ⟨z,y⟩ = τt + ξx. Esponenti sempre come z_k (non σ_k, ρ_k, ζ_k).
- P = c∏_{j=1}^s P_j^{e_j} (P_j irriducibili su ℂ, non associati); componente Q_j := P_j^{e_j}; s = numero di fattori; N = numero di termini; k = deg_τP.
- Ann(u) = G_u·J_u (G_u = gcd, V(J_u) finito); M_u := R·u ≅ R/Ann(u).
- "u identifica P" ⟺ Ann(u) = (P). "u identifica in 𝓛" ⟺ dim(Ann(u) ∩ 𝓛) = 1.
- 𝔅_ρ(Ω_R), B_ρ(J): P1-D1.
- Mappa somma Σ: ⊕_jℋ_j → H, γ(ℋ_1,…,ℋ_s) := inf σ(Σ*Σ|_{(ker Σ)^⊥}) (+∞ se (ker Σ)^⊥ = 0); per i nuclei in H^m il prodotto scalare è ⟨u,v⟩ = Σ_{|α|≤m}⟨∂^αu,∂^αv⟩_{L²}; il valore di γ dipende da esso e dal raggruppamento dei fattori, la condizione γ > 0 no.
- c_F(ℋ_1,ℋ_2) := coseno di Friedrichs (sup |⟨a,b⟩| su a ∈ ℋ_1⊖𝓘, b ∈ ℋ_2⊖𝓘 unitari, 𝓘 = ℋ_1∩ℋ_2); c₀ := ‖Π_{ℋ_1}Π_{ℋ_2}‖ (Dixmier; = c_F se 𝓘 = 0). Per s = 2: γ = 1 − c_F (P2-T3).
- Proiettori ortogonali: Π_ℋ (mai P_i, riservato ai fattori).
- Modelli di dato: M1 (formula EP), M2 (jet in un punto), M2⁺ (jet + test di zero, P4 §6), M3 (u ∈ H^m(Ω) esatta); "dati modali finiti": u₀ ∈ span{e_n : n ≤ N} (P3-T3).
### E_int: tabella unica (quadro → definizione → dove)
| simbolo | definizione | quadro | dove |
|---|---|---|---|
| E^add | u − u₀ − Σ_n(S_n(t)u₀ − u₀) | 𝔅 (lineare), A9 (non lineare) | P1-D3(b), v3 |
| E^{add,form} | stessa, in getti formali in t | ogni u liscia | P1-D3(a) |
| E^mult | S(t) − S_1(t)⋯S_N(t) (dipende dall'ordine) | 𝔅, A9 | P1-D3(c), v3 |
| 𝔈^mult | (S_1⋯S_N)^{-1}S | 𝔅 | P1-D3(c) (sostituisce la scrittura di v2) |
| E^{add,(1)}, E^{mult,(1)} | coefficienti di ε¹ (ordine: prima S₀, poi il flusso di V; con Dirichlet, flusso di inflow) | semigruppi perturbati | P3-P1, P3-T3 |
| E^log | ∂_t log(densità spettrale) − Σ a_n ≡ 0 | misure a supporto compatto | P1-D3(d) |
| E^fatt_X | ker_X P / im Σ_X (fattori, non termini) | X ∈ {D′, C^∞, H^m, 𝔅} | P1-D2 |
| E^ker | ker L/(ker L ∩ Σ ker L_n) (termini) | D′, C^∞ | v2, R2-T3 |
| E^⊥, E^∥ | fuori dallo span / ambiguità nello span | regolarizzazione | v2, P2 |
| E_B, E^trop, E^NL, E^mix | strumenti di regime / Fase 4 | ℝ / non lineare | TROP, v3 |
### Stati
Aggiungere PROVA SCRITTA (prova completa, non auditata), che sostituisce "APERTO-con-prova", "PC-attesa", "DIMOSTRATO (bozza)"; "PARZIALE" solo per problemi aperti con risultati parziali (es. C3-Q1), non come stato di un claim.

## Versione 5 (Gate 6, applicata il 27/10/2026) — aggiunte per le Fasi 8–11; nulla di v1–v4 è rimosso
*Nota: GATE6.md la chiama "NOTAZIONE v4"; il nome v4 era già usato dalla proposta S5-INT, quindi qui diventa v5.* Fonte: `research/SYNTHESIS-2.md` §1, §3.
### Modelli di dato (da dichiarare in ogni enunciato di Fase 8)
- **DM1** formula chiusa / esponenziale-polinomiale; **DM2** jet in un punto; **DM3** u noto esattamente in H^m(Ω) (= M1, M2, M3 di Fase 3).
- **DM-φ**: dato noto a meno della fase temporale globale (u ~ e^{iφ(t)}u). Con DM-φ gli stati stazionari identificano solo V − E (VAR-P4 = ENC-N2(a)); con la fase osservata il dato identifica q.
- **DM-inv**: solo dati invarianti di gauge (|ψ|², correnti); identifica al più l'orbita (F, olonomie su H¹_dR(Ω)).
### Dizionari e misfit
- **MF1–MF3**: i tre teoremi di certificato di misfit di F6-DICT §3 (rinominati per non confondersi con i modelli M1–M3).
- **(H-ID)**: ipotesi d'unicità dell'identificazione nel limite I-LIM (non (H1), che resta l'ipotesi di dominio di v2).
- 𝓓_∞ = ∪_n 𝓓_n: dizionario filtrato numerabile; "identificazione relativa al livello n".
### Sistemi e coefficienti variabili
- Sistemi: R = ℂ[∂_t, ∂_x], dato ψ ∈ (H^m(Ω))^k, oggetto canonico M_u = R^{1×k}/Ann(u) (non più ciclico). Equivalenza **a sinistra** D ~ VD, V ∈ GL_l(R); in forma hamiltoniana (iψ_t = (α·p + βm)ψ) α, β identificati esattamente.
- Mappa residuo: ρ_u(Q) = Qu/u su {u ≠ 0}; identificazione strutturata ⟺ ρ_u iniettiva sulla classe (VAR-T1).
### E_int e encoder
- E_int è sempre quello di A9 (v3). **E^conj**: difetto di coniugazione di un encoder (ex "E" di F6-ENC), da non confondere con E_int.
- **Encoder (E2) modulo costanti** (F6-ENC (E1)–(E3); allentamento di DEVIL-6 O7): W L_q = (L_0 + c) W per qualche costante c (stazionario, W commuta con ∂_t), oppure W(t)(i∂_t − H(t)) = (i∂_t − H_0 − c)W(t) nel caso non autonomo; q costante non ha intertwiner differenziale con c = 0.
### Stati
Invariati (DIMOSTRATO, CON-FONTE, PROVA SCRITTA, V-ex, APERTO, FALSO). "Candidato" = enunciato senza prova completa (uso di Fase 6).

## Versione 6 (Gate 8 §5, applicata il 27/10/2026; nulla di v1–v5 è rimosso, le voci sotto prevalgono dove c'è conflitto)
- **Modelli di dato.** DM2 resta il **getto in un punto** (v5). Il dato rumoroso si chiama **DM-δ**: u nota a meno di un errore ‖u − ũ‖ ≤ δ in una norma dichiarata (introdotto da ALGORITMO_ESTESO §0.3). In GATE8 §5 e in ATTACK-8 O8 «DM2» va letto come DM-δ. L'identificazione è dichiarata in DM3; in DM-δ valgono solo i moduli di VAR-P3 e la negativa DICT-N1(ii).
- **Sensi di «identifica»** (ATTACK-8 O5). Ogni enunciato dichiara quale usa:
  - **ID-ann**: Ann(u) = (P) (v1);
  - **ID-ker**: ker Φ_u = 0 nella classe (DICT-RANGO). Ha senso solo sotto **(H-ex)**: una legge della classe esiste per u;
  - **ID-res**: coefficienti determinati dalla mappa residuo ρ_u in forma fissata (VAR-T1);
  - **ID-fam**: identificazione di una famiglia modulo costanti (encoder, (E2));
  - **ID-lim**: identificazione nel limite (I-LIM, CONV-T2/T2′), sotto (H-ID).
- **(E2) con c(t).** W(t)(i∂_t − H(t)) = (i∂_t − H_0 − c(t))W(t), con c ∈ C(I). Il caso con c costante si chiama **(E2₀)** (ATTACK-8 O12; ENC-P0(b), (b)^cl).
- **(H-ID)** è l'unico nome dell'ipotesi d'unicità nel limite; l'etichetta «(ID)» di DICT-GR è sinonimo deprecato (O13).
- **H-DIRAC**: «α, β identificati esattamente» vale sotto H-DIRAC-1 e H-DIRAC-2 (O11).
- **Oscillatore.** La normalizzazione unica è H = −∂² + x². La fattorizzazione chirp·libero·chirp si rompe a cos t = 0 e si attraversa con la lente (O3; VAR-T10).
- **Anello dei coefficienti** (Gate 8b). Ogni enunciato di tipo Gate 3 specifica l'anello: ℂ[∂] (coefficienti costanti), ℂ(x)[∂] o A_n (polinomiali), oppure una classe parametrica fissata. In un campo chiuso per derivazione (D·u, u) è vacuo (VAR-N1). Per L7–L9 l'oggetto canonico è la coppia ((D·u, u), ρ_u).
- **Sistemi** (Gate 8b). «Componente = fattore» richiede Ext¹(N, 𝒜) = 0 (SYS-S1-C è FALSO senza).

---
## Versione 7 (Fase 10, coordinatore, 27/10/2026; da S10-INT, ESEMPI.md §7)
1. **ID-ker per famiglie non lineari.** ID-ker (nucleo di Φ_u nullo, (H-ex)) è definito per classi **lineari** nei parametri θ. Per classi in cui un parametro entra in modo non lineare (per esempio FRAC: ∂_t + c(−∂_x²)^σ, con σ non lineare) l'identificazione si dichiara come **unicità del compatibile** (ID-fam con insieme dei compatibili ridotto a un punto). La dicitura "ID-ker" è riservata al caso lineare.
2. **Uscita COMPATIBILI.** Per un dato esatto con più leggi compatibili nella classe dichiarata, l'uscita è `COMPATIBILI(θ_0 + ker Φ_u)` (caso lineare) oppure `COMPATIBILI(𝒞_u)` (caso non lineare), distinta da `NON-DECISO`, che resta riservato al budget esaurito o all'indecidibilità.
3. **Classe di Maxwell.** Per Maxwell e per i sistemi con vincoli (div E = div B = 0) la classe va dichiarata: classe simmetrica (A_j = A_j^T), oppure classe generale **modulo i vincoli**. Nella classe hamiltoniana generale ker Φ_u ha dimensione ≥ 12 per ogni dato di Maxwell (EX10-e-K).
4. **Etichetta di Pöschl–Teller.** sech x non è D-finita su ℂ(x): il dato di Pöschl–Teller è **DM3**, non M3-hol.
5. **Passaggio di cos t = 0 nell'oscillatore.** U(π/2) = −i·parità è soltanto **V-ex**; non è un fondamento.
