# ATTACK-6 — DEVIL-6 · pacchetto proposto per il Gate 6 · 26/10/2026

**Oggetto.** I sei VERDETTI di Fase 6 (F6-DICT, F6-CONV, F6-ENC, F6-SYS, F6-HOR, F6-VAR) e le prove nelle rispettive `NOTE.md`, come base di SYNTHESIS-2 / GATE6 (G★″, scala L6–L10). F6-VAR è stato **revisionato** (VERDETTO e NOTE completi al momento della revisione, AVVISO del coordinatore).
Fonti lette: `FASE6_SCOUTING.md`, `PIANO_FASI_6-11.md` (§ Gate 6), `PROTOCOLLO.md` (Regola 3), `skills-local/claim-lifecycle/SKILL.md`, `research/DEVIL/ATTACK-4.md` (formato e severità), i sei `VERDETTO.md` e `NOTE.md`, `inbox/central-F6.md`, e per confronto `work/P1/CHECK_REQUEST.md` §C (enunciato esatto di P1-T5).

**Skill caricate** (lettura integrale del SKILL.md; nessuno script `_vendor` eseguito):
- `kill-argument`: solo thread di ATTACCO (memo unico ≤ 250 parole + obiezioni atomiche con severità). Niente Codex: il revisore fresco sono io; la difesa spetta al coordinatore. Mappatura del verdetto come nella tabella della skill.
- `scientific-critical-thinking`: separo dati e interpretazione, "prova scritta" da "V-ex", segnalo repliche non indipendenti, ogni obiezione ha un rimedio.
- `claim-lifecycle`: gli stati proposti non possono salire; dove trovo un controesempio propongo FALSO o una riformulazione.

**Verifiche SymPy.** `research/DEVIL/sympy6/devil6_checks.py` → `devil6_checks.out`, **16/16 OK**, eseguito con `.venv -I`. Sono controesempi e controlli, non prove:
- A1: ipotesi (H) di P1-T5 per Dirac 1+1;
- B1–B2: propagatore dell'oscillatore come prodotto chirp·libero·chirp oltre cos t = 0. B1 è controllato numericamente: la semplificazione simbolica di SymPy non chiudeva;
- C1–C3: tricotomia di N1(vi);
- D1: il ritardo come sistema locale di trasporto;
- E1: HOR-P1 con l'atomo costante;
- F1: stati stazionari;
- G1–G3: q costante senza intertwiner differenziale;
- H: passo (ii) di CONV-T2.

---

## 1. Memo d'attacco (≤ 250 parole)

> Il pacchetto risponde all'utente con un teorema negativo che, nella forma in cui è scritto, è falso proprio sul caso che l'utente ha nominato.
>
> F6-DICT presenta N1(vi) e la "tricotomia" come il confine del dizionario universale: "classe troppo grande ⇒ ogni u ha una legge e **nessun operatore è identificato**", e su questo nega (H1) di I-LIM "sempre" con coefficienti in (t,x).
>
> Ma per Schrödinger con V(t,x) arbitrario, la domanda 2 dell'utente, ogni u senza zeri ha una legge e **V è identificato in modo unico** (V = (iu_t+u_xx)/u, C1). Allo stesso modo u_t = a(t,x)u_x identifica a, e (H1) vale (C2). Lo dicono F6-VAR (VAR-T1), F6-ENC (ENC-N2(b)) e F6-HOR (O-H1), e lo usa la stessa regola R6 di F6-DICT. Il confine vero non è la "taglia" della classe. È il conteggio fra funzioni incognite e rango della mappa residuo, e va separato fra identificabilità e falsificabilità.
>
> Il secondo enunciato da registrare, "E per sistemi: P1-T5 no" (F6-SYS), è falso: per Dirac X = iσ_zξ, Y = −imσ_x soddisfano l'ipotesi (H) di P1-T5 (A1), quindi P1-T5 si applica alla lettera. Il prodotto di Euler usa tempi dipendenti da ξ, cioè moltiplicatori non locali e non flussi dei termini.
>
> Anche la colonna (E) di F6-VAR/F6-ENC ("forma chiusa solo per V quadratico", "rottura a cos t = 0") cade: Pöschl–Teller ha un propagatore esplicito, e chirp·libero·chirp attraversa cos t = 0 (B2).
>
> Infine lo stesso fatto (il potenziale dipendente da u) è contato quattro volte come convergenza indipendente, con conclusioni opposte. Sugli stati stazionari ENC-N2(a) contraddice VAR-P4.
>
> Così com'è, il pacchetto va respinto. Le correzioni però sono di riscrittura e non richiedono nuova ricerca.

---

## 2. Obiezioni

### O1 — CRITICA · N1(vi) e la "tricotomia" di F6-DICT confondono identificabilità e falsificabilità; "(H1) fallisce sempre" è falso
**Punto attaccato.** F6-DICT VERDETTO "Risposta in una frase" e N1(vi); NOTE §2 N1(vi)(b), "Tricotomia" punto 1; NOTE §6 "Contro-esempio di (H1)… con coefficienti in (t,x) (H1) fallisce sempre".

**Argomento.**
1. L'identità L_{u,i} = u∂_i − (∂_iu) annulla u: è corretta, ed è banale.
2. N1(vi)(a), "ogni u ha una legge", vale solo perché ammette operatori **degeneri**: il coefficiente principale u si annulla sugli zeri di u. Nella classe normalizzata che il progetto usa davvero (livelli affini 𝓐_n con D_0 = ∂_t a coefficiente 1, 𝒦_R di I-LIM) è falsa. Controesempio (C3): u = t − x², in un intorno di 0 non esiste una legge ∂_t + a∂_x + b con a, b lisci (in 0 si ottiene 1 = 0).
3. N1(vi)(b), "nessun operatore è identificato", è falsa per le classi strutturate grandi:
   - Schrödinger con V(t,x) ∈ C^∞ arbitrario: V = (iu_t + u_xx)/u è unico su {u ≠ 0} (C1);
   - u_t = a(t,x)u_x: a = u_t/u_x è unico dove u_x ≠ 0, quindi (H1) di I-LIM **vale** con coefficienti in (t,x) (C2). Il corollario di Hölder di F6-DICT, scritto per a(x), vale identico per a(t,x).
4. (H1) fallisce quando A contiene due atomi i cui residui sono linearmente dipendenti su C^∞, per esempio ∂_x e 1: L + φ(u∂_x − u_x). È il criterio di VAR-T1, cioè l'iniettività della mappa residuo, e il criterio di conteggio di SYS-N3. Non dipende dalla "taglia" della classe.
5. Incoerenza interna. La regola R6 (D4-ENC) di F6-DICT usa proprio "q identificabile puntualmente (V = u″/u)", che la tricotomia punto 1 nega.
6. Incoerenza fra scout sullo stesso fatto:

| fonte | conclusione |
|---|---|
| VAR-T1 / VAR-N1 | V identificato in forma fissata; nessuna identificazione **intrinseca** in 𝒦[∂] |
| ENC-N2(b) | "l'identificazione è banale", cioè possibile |
| HOR-O1 / O-H1 | V identificato, L₀ no |
| F6-DICT | "nessun operatore è identificato" |

**Conseguenza.** Il teorema negativo che dovrebbe "marcare il confine" (regola N1 del piano) dà all'utente, sulla domanda 2 (non autonomo, Schrödinger), una risposta sbagliata. Il fatto giusto ha due facce:
- la legge esiste sempre (non è falsificabile), quindi l'esistenza non spiega nulla;
- i coefficienti sono identificati esattamente se e solo se la mappa residuo è iniettiva.

**Azione (fix F1).** Riscrivere N1(vi) come due enunciati.
- **(a′)** = VAR-N1: in 𝒦[∂] con 𝒦 ∂-chiusa, per u senza zeri con log-derivate in 𝒦 si ha Ann(u) = u·Ann(1)·u^{−1}. L'identificazione intrinseca è vuota.
- **(b′)**: nella classe strutturata L_0 + Σθ_kT_k con θ_k ∈ C^∞(t,x), ogni u senza zeri ammette una legge quando ρ_u(T_k) ≠ 0 per qualche k (non falsificabilità), e θ è identificato ⟺ la mappa residuo è iniettiva (VAR-T1).

Cancellare "nessun operatore è identificato" e "(H1) fallisce sempre". La tricotomia va riscritta lungo l'asse (identificabile / falsificabile), non lungo l'asse della "taglia" della classe.

### O2 — CRITICA · "P1-T5 non si trasporta ai sistemi" (F6-SYS) è falso: Dirac soddisfa (H) e P1-T5 si applica
**Punto attaccato.** F6-SYS VERDETTO (E) e la proposta per G★″ "E per sistemi = P1-T4 sì, P1-T5 no"; NOTE §6 "P1-T5 NON si trasporta (teorema di confine)… richiede 𝔤 di dimensione infinita; per sistemi a coeff. costanti 𝔤 è finito".

**Argomento.**
1. P1-T5 (DIMOSTRATO, `work/P1/CHECK_REQUEST.md` §C) è un enunciato in un'algebra 𝒜 con tempi **scalari** g_i(t,ε). L'algebra pertinente è quella degli operatori, Mat_2(ℂ[∂_x]), cioè 𝒜 = Mat_2(ℂ[ξ]) su ℂ. Non è Mat_2(ℂ) a ξ fissato.
2. Lì, con X = iσ_zξ e Y = −imσ_x:
   - ad_X^{2k}Y ∝ ξ^{2k}σ_x;
   - ad_X^{2k+1}Y ∝ ξ^{2k+1}σ_y;
   - X, Y_0, …, Y_7 hanno rango 9/9 (A1).

   Quindi (H) vale: 𝔤 ha dimensione **infinita su ℂ** ed è finita solo sul modulo ℂ[ξ], cioè puntualmente in ξ.
3. P1-T5 dà allora: nessun prodotto finito di flussi dei termini (trasporto e massa), con tempi olomorfi in (t, m) e flusso di massa spento a m = 0, rappresenta e^{t(X+mY)}.
4. La costruzione di Euler ZXZ usa tempi g_i(t,ξ): gli operatori e^{g_i(t,∂_x)A(∂_x)} non sono flussi dei termini, e F6-SYS stesso lo ammette ("moltiplicatori di Fourier non differenziali"). Non è un controesempio a P1-T5. È un enunciato in un altro dizionario, i moltiplicatori di U3.

**Conseguenza.** La riga proposta per G★″ registrerebbe come "teorema di confine" un enunciato falso.

**Azione (fix F2).** Sostituire con:
- "SYS-E: P1-T5 si applica ai sistemi a coefficienti costanti quando l'orbita aggiunta è infinita su ℂ (Dirac 1+1: sì, A1);
- puntualmente in ξ esiste un prodotto finito (Euler) con tempi dipendenti da ξ, cioè un moltiplicatore non locale (dizionario U3)."

Togliere "P1-T5 no" e "teorema di confine". La stessa cautela vale per "Wei–Norman locale per sl_2 (Dirac)": l'algebra rilevante non è sl_2 su ℂ, ma sl_2 ⊗ ℂ[ξ].

### O3 — MAGGIORE · L'affermazione positiva di F6-DICT è sovradimensionata rispetto a ciò che l'utente ha chiesto
**Punto attaccato.** "Sì, si può costruire un dizionario … che 'tiene conto di tutto'"; Teorema-ombrello §1.6.

**Argomento.**
- Il teorema-ombrello è un'**unione di enunciati di densità classe per classe**, con topologie incompatibili: τ₁, C^m → L^p, getti sopra compatti vicino a ogni f, bilineare debole, H^s → H^{s−m′}, uniforme sui compatti di dati. Non esiste una topologia, né un enunciato unico, in cui 𝓓_∞ "tiene conto di tutto".
- U5, cioè la versione "per tutto", è esattamente la completezza di tipo Hilbert che l'utente ha detto non bastare. F6-DICT lo ammette, ma la frase-risposta la usa comunque come "sì".
- Il solo contenuto di identificazione (I-LIM) vive in classi compatte 𝒦_R **con (H1) come ipotesi**, e (H1) esclude per costruzione quasi tutte le classi del teorema-ombrello.
- Dopo O1, la parte "nel senso della chiusura ogni u ha banalmente una legge" va rivista.
- La "forma più forte vera" richiesta dal piano è dunque: densità per classe con velocità quando esistono (U1-b, U3-c, U3-d), certificato di misfit livello per livello (M2/M3, Teorema A), identificazione solo relativa a un livello o a una classe compatta identificante.

**Azione (fix F3).** Riscrivere la frase-risposta all'utente in questi termini, senza "tiene conto di tutto". Elencare il teorema-ombrello come tabella di enunciati separati, non come teorema. Assegnare a ogni riga la topologia e il modello di dato.

### O4 — MAGGIORE · N3 (ritardo) e la classificazione del ritardo in CONV-T6 sono sbagliati: il ritardo è un sistema locale aumentato
**Punto attaccato.** DICT-N3 "ritardo NON nella chiusura in norma dei sistemi locali ⇒ atomo T_τ"; F6-CONV §3, dove il ritardo dà "nessuna legge differenziale", e la tricotomia L/L⁺/N.

**Argomento.**
1. Con w(t,θ) := u(t−θ) si ha w_t + w_θ = 0, w(t,0) = u(t) e u(t−τ) = w(t,τ) (D1). Il ritardo è un **sistema locale (PDE di trasporto) con una variabile ausiliaria e accoppiamento al bordo**: classe L⁺, come Caffarelli–Silvestre per il frazionario. È il modello standard nei sistemi con ritardo.
2. N3 dimostra soltanto che il ritardo non è nella chiusura delle **funzioni di trasferimento razionali**, cioè dei sistemi ODE aumentati a dimensione finita.
3. N3 è provato su ℝ (Fourier, sup su ω ∈ ℝ), mentre il modello di dato è su Ω limitato.

**Azione (fix F4).**
- Rienunciare N3 come "non nella chiusura in norma dei sistemi ODE lineari aumentati a dimensione finita (su ℝ)".
- Mettere il ritardo in L⁺ con aumento infinito-dimensionale (trasporto), in modo coerente in F6-DICT e F6-CONV.
- La classe N di CONV-T6(4) resta valida per i dati con spettro bidimensionale.

### O5 — MAGGIORE · La colonna (E) di F6-VAR / F6-ENC / NS-EQUIV per V(x) e V(t,x): due affermazioni false
**Punto attaccato.**
- VAR-P8: "E_int in forma chiusa solo per potenziali al più quadratici".
- VAR-T10(3): "sl_2 ⇒ locale, rottura a cos t = 0".
- F6-ENC §11 (E): "V quadratico: solo locale nel tempo (caustica del lens transform)".
- F6-HOR NS-EQUIV.

**Argomento.**
1. **Oltre il quadratico.** Per V = −2sech²x (Pöschl–Teller), il propagatore è esplicito via Darboux: U_q(t)A† = A†U_0(t) sul continuo, più lo stato legato. Anche e^{−itV} è esplicito, quindi E_int^add = U_V − U_0 − e^{−itV} + I ha forma chiusa. VAR-P8 dimostra soltanto che ⟨∂², V⟩ ha dimensione infinita per V polinomiale di grado ≥ 3. Questo esclude Wei–Norman con un numero finito di funzioni, non la forma chiusa. P1-T5 stesso avverte che "non significa che l'equazione non si possa risolvere", e la sua ipotesi (H) **non** vale per ⟨∂², x^k⟩ (R5-P7, P1-Q3 APERTO). La "consequenza" di VAR-P8 non segue.
2. **Caustica.** Per H = (−∂² + x²)/2, la rotazione simplettica è R(t) = L(−tan(t/2))·U(sin t)·L(−tan(t/2)) per |t| < π (B1). Nella rappresentazione d'onda, chirp·libero·chirp coincide con il propagatore esatto, a meno di una fase in t, anche a **t = π/2 = caustica del lens** e a t = 2.5 (B2, scarto ≤ 6·10⁻¹⁶). Ripetendo il prodotto (6 fattori) si arriva a |t| < 2π.

   La rottura a cos t = 0 è quindi un **artefatto della fattorizzazione lens** (chirp·dilatazione·libero, dove la dilatazione non è un flusso di un termine). Non è un fatto di sl_2. P1-P5 ("non risolubile ⇒ solo locale per una parola fissa di dim 𝔤 fattori") resta compatibile: la parola chirp·libero·chirp si rompe a t = π.
3. **Doppioni.** ENC-L1 e VAR-P8 sono lo stesso enunciato. La dimensione infinita di ⟨∂², x^k⟩, k ≥ 3, era già nota al progetto (R5-P7, citata in P1-T5 "Portata"). Non vanno contati come due candidati nuovi.

**Azione (fix F5).**
- Riscrivere VAR-P8: "Wei–Norman con dim 𝔤 < ∞ ⟺ V al più quadratico (V polinomiale)". Togliere "E_int in forma chiusa solo per V quadratico" e aggiungere Darboux/Pöschl–Teller come classe con E_int esplicito.
- Riscrivere VAR-T10(3) ed ENC (E): "una parola fissa di 3 flussi copre |t| < π; la caustica del lens a π/2 non è un'ostruzione".
- Fondere ENC-L1 in VAR-P8 e citare R5-P7.

### O6 — MAGGIORE · F6-ENC: ENC-T2 è corretto ma circolare per B1; ENC-P0 è inquadrato male; la colonna (E) ripete l'equivoco su E_int di ATTACK-4 O1
**Punto attaccato.** ENC-T2, D4-ENC/R6 (H3)–(H4), ENC-P0 e la frase "salvo la classe quadratica", NOTE §11 (E).

**Argomento.**
1. **Validità.** Ho ricontrollato ENC-T2(a)–(b): Ann_q(u) = φ^{−1}Ann(Wu); per (Q) ∩ ℂ[τ,ξ²] il generatore è lcm(Q,Q̃) se pari, ξ·lcm se dispari. È corretto. Corretto anche ENC-T2(c): W conserva i getti nel punto base x_0, quindi C3-P1[M2] si trasporta in x_0.
2. **Circolarità.**
   - Per costruire W serve q. In D4-ENC, q si ottiene con una "formula di residuo nota per la classe" (H4), cioè supponendo già nota la forma P (Schrödinger, calore, onda).
   - Poi ENC-T2 "identifica" Ann_q(u), cioè P.
   - Come procedura di identificazione per B1, ENC-T2 non aggiunge nulla se P non è già fissato (ENC-N2(d) lo ammette: "aperta").
   - Il caso non circolare è l'eliminazione di V alla HOR-P1: L₀ in un dizionario, V(x) libero. Lì però resta l'ambiguità L₀ → L₀ + c (E1).
3. **ENC-P0.**
   - Il calcolo è corretto: iM′ = 0.
   - Ma P0 classifica solo gli intertwiner **a tempo fissato** W(t). Gli encoder della classe quadratica (lente di Niederer: t ↦ tan t, x ↦ x/cos t) **riparametrizzano il tempo** e stanno fuori dalle ipotesi di P0.
   - Nessuno di loro commuta con ∂_t. La frase del VERDETTO "non esiste un encoder che commuti con ∂_t … salvo la classe quadratica" è quindi falsa nell'eccezione.
   - L'enunciato giusto ("V davvero dipendente da t ⇒ nessun W ≠ 0 indipendente dal tempo con W(i∂_t − H(t)) = (i∂_t − H_0)W", perché W(V(t) − V(s)) = 0) è elementare e non ha bisogno di P0.
4. **(E).** E^mult := W^{−1}S_0W − S_0S_V ("difetto di coniugazione") non è l'E_int di A9 (U − U_1U_2 o U − e_1 − e_2 + I). È lo stesso schema che ATTACK-4 O1 aveva segnalato. F6-VAR invece usa A9 correttamente (VAR-P9).

**Azione (fix F6).**
- Dichiarare ENC-T2 come lemma di trasporto "a q noto" e non come identificazione.
- Riformulare l'eccezione di ENC-P0 come "trasformazioni che cambiano il tempo (NS-EQUIV)".
- Rietichettare (E) di F6-ENC con l'oggetto effettivo e fissare in NOTAZIONE l'E_int di A9 per V.

### O7 — MAGGIORE · Le classificazioni "solo se" degli encoder sono incoerenti fra loro e la decidibilità è sovrastimata
**Punto attaccato.** ENC-K1 (congettura); F6-HOR O-H2 / NS-GALDAR ("⟺ V razionale con monodromia banale", "criterio decidibile", Kovacic); NS-EQUIV ("⟺ V quadratico"); definizione (E2) di encoder.

**Argomento.**
1. ENC-K1 include i solitoni senza riflessione (sech², non razionali). NS-GALDAR dice "⟺ V **razionale** con monodromia banale" e copre sech² con il pull-back x ↦ tanh x. Ma il pull-back cambia l'operatore: −∂_x² non diventa −∂_y². La classe "W a coefficienti razionali" esclude dunque Pöschl–Teller, che entrambi gli scout usano come esempio guida. Le due caratterizzazioni non coincidono.
2. Kovacic decide l'esistenza di soluzioni liouvilliane **per un λ fissato**. "Monodromia banale per ogni λ" è un problema parametrico, e Kovacic da solo non lo decide. Il criterio decidibile giusto per V razionale è sui coefficienti di Laurent ai poli (condizioni di Duistermaat–Grünbaum / Gesztesy–Weikard, da verificare con CIT-AUDIT).
3. q ≡ c ≠ 0 (rimovibile con il gauge e^{ict} o con lo spostamento σ ↦ σ − c) **non** ha alcun intertwiner differenziale W L_c = L_0 W: per ordine ≤ 3 e coefficienti polinomiali è verificato (G1–G3), e la ricorsione dall'alto lo mostra per ogni ordine. La definizione (E2) è troppo rigida. Andrebbe ammesso W L_q = (L_0 + c)W, o un'affinità di σ, e la congettura ENC-K1 va enunciata "modulo costanti".
4. NS-EQUIV "⟺ quadratico" vale per le trasformazioni **puntuali** su ℝ. Su Ω limitato il dominio si deforma e il tempo di vita è finito, come HOR stesso osserva. L'enunciato "I/S/E sì/sì/sì (trasporto esatto)" non è compatibile con questa ostruzione.

**Azione (fix F7).**
- Un'unica tabella "livello di encoder ⟷ classe di V ⟷ stato" in SYNTHESIS-2:
  - puntuale: CON-FONTE da verificare, su ℝ;
  - differenziale: congettura unica, che includa i solitoni e sia enunciata modulo costanti;
  - integrale: GLM.
- Togliere "decidibile via Kovacic" finché non c'è un criterio parametrico verificato.
- Per NS-EQUIV su Ω limitato: I/S/E parziale.

### O8 — MAGGIORE · SYS-T1: probabile corollario di Oberst 1990, e non è il teorema più forte disponibile
**Punto attaccato.** SYS-T1, SYS-N1, SYS-T0 e il delta dichiarato da F6-SYS.

**Argomento.**
- La prova di SYS-T1 è corretta, ma l'enunciato è una riformulazione dell'iniettività di φ_u su un sottomodulo essenziale. Il "test" chiede di escludere relazioni Σr_{p,j}w_{p,j} = 0, cioè di calcolare di nuovo un annullatore (di un vettore di funzioni). Su una u non EP non è un test più decidibile di Ann(u) = U_P.
- L'enunciato strutturale più forte che il materiale suggerisce è un criterio di **esistenza**: "esiste u ∈ Sol(P) che identifica P ⟺ dim soc_m(M_P) ≤ 1 per ogni ideale massimale m". La parte "solo se" è SYS-N1; la parte "se" è provata solo per le EDO (SYS-T0). In nD seguirebbe dalla decomposizione di Matlis di 𝒜, perché E(R/m) compare con molteplicità 1 (lo zoccolo in λ è ℂe^{λ·x}). Che E(R/p) compaia con molteplicità infinita per p non massimale è plausibile ma da verificare.
- Questa è precisamente la struttura dei "large injective cogenerators" di Oberst 1990. Il rischio di novità, che F6-SYS stesso segnala, è alto.
- G-T0 è banale (la condizione di gauge sta in Ann(A) perché la si è imposta). G-T2 e G-T3 sono prior art dichiarato.

**Azione (fix F8).**
- Tenere SYS-T1 come "candidato, novità da verificare su Oberst 1990 §2–4 prima di ogni promozione".
- Aggiungere come obiettivo di S8-SYS il criterio di esistenza (zoccoli ≤ 1) in nD, con la verifica della molteplicità di E(R/p) in C^∞.
- Declassare G-T0 a osservazione.

### O9 — MAGGIORE · Coerenza del pacchetto: simboli sovrapposti, modelli di dato non dichiarati, conflitti sugli stati stazionari e sull'ambiguità di "λ ∈ Mat 4×4"
**Punto attaccato.** Il pacchetto nel suo insieme, punto (5) del compito, e le risposte alle 4 domande dell'utente.

**Argomento.**
1. **Stati stazionari, quattro enunciati con modelli di dato diversi:**

| enunciato | modello di dato | conclusione |
|---|---|---|
| HOR-O1 | L₀ incognito, V(x) libero | nessuna identificazione di L₀ (corretto) |
| VAR-P4 | profilo φ soltanto | solo V − E |
| VAR-P4 / VAR-T1 | u(t,x) completo | V esatto |
| VAR-T2 | anello ℂ(x)[∂] | gli autostati iperesponenziali non identificano intrinsecamente |
| ENC-N2(a) | u = e^{−iλt}φ | "(q+c, λ+c) indistinguibili" |

   ENC-N2(a) è **falso se si osserva la fase globale nel tempo**: q = λ + φ″/φ si legge esattamente da u(t,x) (F1). La coppia (q+c, λ+c) produce il dato e^{−ict}u, diverso. È vero solo per dati "a meno della fase temporale globale". Questo modello di dato è fisicamente naturale (come in G-T2 di F6-SYS), ma va dichiarato.
2. **"λ ∈ Mat 4×4": due gruppi d'ambiguità diversi sotto lo stesso nome.**
   - F6-SYS: da ψ si identifica il modulo delle righe U_D, cioè D a meno di V ∈ GL_l(R) **a sinistra**. Per esempio γ^0D (forma hamiltoniana) è equivalente a D.
   - F6-HOR: "i γ^μ sono identificabili al più modulo coniugio GL₄" (Pauli). Ma il coniugio richiede il cambio di base del dato ψ ↦ Sψ: con ψ dato in una base fissata non c'è ambiguità di coniugio.

   Risposta corretta alla domanda 1, che nessuno scout scrive: fissata la forma normale hamiltoniana (coefficiente di ∂_t = I), V è costante con V·I = I, quindi V = I. Le matrici α^k, β sono identificate **esattamente**, sotto SYS-T1 e il test di molteplicità μ = 2.
3. **Simboli sovrapposti:**
   - "M1/M2/M3" sono i teoremi di misfit in F6-DICT §3 e i modelli di dato in CONV/C3;
   - "N1" ha quattro significati (DICT-N1, ENC-N1, SYS-N1, VAR-N1);
   - "(H1)" è l'unicità in I-LIM e il rettangolo simmetrico in D4-ENC;
   - σ indica il simbolo di L in ENC, i valori singolari in CONV e il simbolo principale in DICT;
   - CONV cita "F6-DICT §7" per il ramo approssimato di I-LIM, che sta in §6;
   - Peetre è "CON-FONTE verificata" in DICT e "CON-FONTE da verificare" in CONV.
4. **Modelli di dato non dichiarati per enunciato** (stesso difetto di ATTACK-4 O4):

| enunciato | modello / dominio |
|---|---|
| CONV-T1/T2 | M2, getti esatti di u analitica, aritmetica reale esatta |
| CONV-T6 | u intera in x, spettro compatto |
| ENC-1/T2 | rettangolo **simmetrico** attorno a x_0; W dipende da x_0 |
| ENC-5 | globale, t → ∞ |
| DICT-N3 | ℝ |
| I-LIM | H^m(Ω) |

   DICT-N1(iv) ragiona con uscite finite (macchina di Turing), CONV-T1 con uscite reali esatte (modello BSS). La fusione "I-LIM = CONV-T1 + DICT §6" mescola due modelli di calcolo.
5. **Repliche non indipendenti.** Il potenziale dipendente da u (DICT-N1(vi), VAR-N1, ENC-N2(b), HOR-O1/O-H1) e la classificazione degli encoder (ENC-3/K1, HOR O-H2/NS-EQUIV/NS-GALDAR) sono lo stesso fatto ricomunicato attraverso l'inbox (grafo hub di F6-DICT). Non vanno presentati come convergenza indipendente.
6. **Copertura delle 4 domande dell'utente:**

| domanda | stato | che cosa manca |
|---|---|---|
| (1) Dirac a coefficienti matriciali | coperta da F6-SYS | la risposta esplicita "identificazione esatta in forma normale" (punto 2); E corretto come in O2 |
| (2) coefficienti variabili / non autonomo (Schrödinger) | coperta, ma con risposte contraddittorie | serve O1 e i fix F5–F6 |
| (3) convergenza a un'equazione differenziale | coperta da CONV | la risposta va detta in chiaro: "nel limite, mai certificata; con rumore solo al livello minimo con margine e soglia δ₀ non calcolabile" |
| (4) operatori fuori catalogo | coperta da F6-DICT | con le correzioni O3–O4 |

**Azione (fix F9).**
- Una tabella di raccordo in SYNTHESIS-2: per ogni enunciato, modello di dato, dominio, modello di calcolo, stato, e oggetto E_int secondo A9.
- Rinominare i simboli sovrapposti, con prefissi per scout e "DATA-M1..M3" per i modelli.
- Riscrivere ENC-N2(a) dichiarando il modello "a meno di fase temporale".
- Scrivere la risposta alla domanda 1 con la forma normale hamiltoniana.

### O10 — MINORE · Punti formali e di novità
- **CONV-T2: la prova regge.** Ho ricontrollato il passo (ii) parola per parola:
  - Ann(g) = 0 per g = (t²+x²)^{L+1}e^{t²+x²} via il termine di grado massimo Q_top(2t,2x)(t²+x²)^{L+1};
  - le righe |β| > L coinvolgono solo i coefficienti di ordine > L ≥ deg p;
  - il rango pieno segue da "Qg polinomio di grado ≤ L ⇒ ∂_t^{L+1}Q ∈ Ann(g)";
  - verifica di rango 3/3 e 6/6 (H).

  Restano tre note:
  - è un'istanza della separazione classica Σ⁰₂ ∖ Π⁰₂ (novità bassa, come dichiarato);
  - vale nel modello M2 (getti esatti in un punto);
  - CONV-T1(5) conta le **uscite** distinte (≤ (d+1)(d+2)/2): i cambi sono al più quel numero meno uno.
- **CONV-T5:** il rumore va misurato in norma H^d (derivate dei dati). In L² serve il ramo hölderiano con limite a priori. La soglia δ₀(u) non è calcolabile: la "garanzia" è asintotica e non certificata. Va detto all'utente in questi termini.
- **DICT:**
  - N1(i) (Baire), N1(iii) (EP ⇒ Ann non principale, riformulazione di C3-L3) e N2 (non separabilità di S^m, alla ℓ^∞) sono fatti classici: novità ≤ 2/10, non "confine nuovo".
  - La prova di N1(v) per i **polinomi differenziali** non funziona così com'è: per atomi non lineari il coefficiente direttore di det(M_{u+sw}) non è det M_w. Va usato il termine omogeneo di grado massimo, con un'ipotesi di non degenerazione sulle parti omogenee.
  - N1(iv) confonde la stabilizzazione alla Gold con la convergenza topologica ("nel limite").
- **HOR-P1:** con l'atomo costante nel dizionario il nucleo affine ha sempre dimensione ≥ 1 (L₀ → L₀ + c, E1). L'"unicità" del V-ex su Pöschl–Teller dipende dal dizionario scelto senza 1. Va dichiarata la normalizzazione (ripete VAR-P4).
- **VAR-C7:** Landau mostra la non unicità del **numero** di fattori irriducibili di un LPDO (classico: Landau 1902, Tsarev). Non falsifica C12-T1′, che è un enunciato di decomposizione dei nuclei. Etichetta corretta: "unicità di Jordan–Hölder per elementi falsa per LPDO". Novità nulla.
- **F6-SYS:**
  - "E^mult ≠ 0 è nuovo" è la sola non commutatività delle matrici;
  - "forma chiusa sempre" vale nel dizionario dei moltiplicatori (ω = √(ξ²+m²)), cioè non locale;
  - II-T2(b′) da rifare: d'accordo.
- **F6-ENC ENC-1:** l'esistenza su rettangolo simmetrico e la dipendenza da x_0 vanno messe nell'enunciato e non solo nei rischi. ENC-5 sta fuori dal modello G★′: il parcheggio è corretto.
- **F6-VAR:** VAR-N1, VAR-T2 (ciclicità di Galois), VAR-P5 e VAR-P9 sono corretti, ma classici o corollari immediati, come dichiarato. VAR-P11 è CON-FONTE da verificare.

---

## 3. Risposta ai punti del compito
1. **N1 e il dizionario universale.**
   - L'affermazione positiva non è vuota, ma è sovradimensionata e senza topologia unica (O3).
   - N1(vi) è un'identità corretta inquadrata male: confonde identificabilità e falsificabilità e usa operatori degeneri (O1, CRITICA).
   - N1(i)–(iii) sono classici (O10). N3 è sovradimensionato (O4).
2. **CONV.**
   - T2 regge, passo (ii) compreso (O10, H).
   - T1 è corretto nel modello M2 (getti esatti, aritmetica reale).
   - T4/T5 sono corretti; la garanzia è solo asintotica con soglia non calcolabile.
   - Il raccordo con DICT-N1(iv) mescola i modelli di calcolo (O9).
3. **ENC.**
   - ENC-T2 è corretto ma circolare come identificazione (O6).
   - ENC-P0 è corretto come calcolo, ma la sua "eccezione quadratica" è fuori ipotesi (O6).
   - I "solo se" (ENC-K1, NS-GALDAR, NS-EQUIV) sono incoerenti fra loro, la decidibilità è sovrastimata e q = c resta escluso (O7).
4. **SYS.**
   - SYS-T1 è corretto, a rischio Oberst e non massimale (O8).
   - SYS-N1 è corretto. G-T0 è banale.
   - "P1-T5 non vale per Dirac" è **falso** (O2, CRITICA).
5. **Coerenza.** È insufficiente (O9):
   - stati stazionari: ENC-N2(a) contro VAR-P4;
   - ambiguità di λ: sinistra contro coniugio;
   - simboli sovrapposti, modelli di dato non dichiarati, repliche non indipendenti.

   Le 4 domande sono tutte toccate. La (2) riceve risposte contraddittorie e la (1) manca della frase risolutiva.

## 4. Che cosa regge (onestà)
- **Validità controllata senza controesempi:**
  - CONV-L1, CONV-T1, CONV-T2 (passo (ii) compreso), CONV-T3, CONV-T4, CONV-P8;
  - DICT U1/N0, N2, B2, M2/M3(c), I-LIM (dato (H1));
  - ENC-1 (intertwining senza bordo), ENC-T2(a)–(c), ENC-P0 (come calcolo);
  - SYS-T1, SYS-N1, SYS-T0, SYS-S1, la fattorizzazione di Dirac (D′ − D = 2m);
  - VAR-N1, VAR-T1, VAR-T2, VAR-P3, VAR-P5, VAR-P9;
  - HOR-O1 (nel suo modello).
- **Contenuto più utile per l'utente:**
  - il certificato di misfit in forma debole con robustezza (M3) e l'asimmetria Σ₁/Π₁ (Teorema A);
  - CONV-T2 come confine;
  - VAR-T1 + VAR-P3 (identificazione strutturata puntuale, mal posta di ordine 2, regolarizzabile);
  - SYS-S1 per Dirac (ker(□+m²)^4 = ker D ⊕ ker D′ con proiettori polinomiali);
  - VAR-T2 (ciclicità di Galois come analogo di C3-T1 per le ODE).
- **Scarti di F6-HOR:** corretti (NLSPEC, HAANTJES, Koopman/DMD per il vincolo no-ML, quiver per Morita).

## 5. Verdetto (mappatura kill-argument)
Obiezioni non risolte dal testo attuale:
- **2 CRITICHE** (O1, O2);
- **7 MAGGIORI** (O3–O9);
- **1 MINORE** (O10, a più voci).

Esito per il pacchetto **come proposto**: **FAIL** (`unresolved_critical`).

Entrambe le CRITICHE e tutte le MAGGIORI si chiudono con riscritture, declassamenti e una tabella di raccordo, senza nuova ricerca. Con i fix F1–F9 applicati in SYNTHESIS-2/GATE6, il pacchetto diventa **PASS-WITH-FIXES**: nessuna prova scritta centrale cade, cadono solo enunciati di confine sovradimensionati.

## 6. Fix che il coordinatore deve applicare in SYNTHESIS-2 / GATE6
| # | fix | obiezione |
|---|---|---|
| F1 | N1(vi) sdoppiato in (a′) = VAR-N1 (intrinseca vuota) e (b′) (legge sempre esistente ma θ identificato ⟺ mappa residuo iniettiva). Togliere "nessun operatore identificato" e "(H1) fallisce sempre". Tricotomia lungo l'asse identificabile/falsificabile | O1 |
| F2 | "P1-T5 no" per i sistemi → FALSO. P1-T5 si applica a Dirac (orbita infinita su ℂ). Euler = moltiplicatore non locale (U3) | O2 |
| F3 | Frase-risposta di F6-DICT riscritta (densità per classe + misfit per livello + identificazione solo relativa). Teorema-ombrello come tabella di enunciati separati | O3 |
| F4 | N3 limitato ai sistemi ODE a dimensione finita su ℝ. Ritardo in L⁺ (trasporto), coerente fra DICT e CONV | O4 |
| F5 | VAR-P8 riscritto (Wei–Norman finito ⟺ quadratico), con Pöschl–Teller come E_int esplicito. "Rottura a cos t = 0" eliminata (chirp·libero·chirp per \|t\| < π). ENC-L1 fuso in VAR-P8, con R5-P7 citato | O5 |
| F6 | ENC-T2 come lemma "a q noto". Eccezione di ENC-P0 = trasformazioni che cambiano il tempo. E di F6-ENC rietichettato secondo A9 | O6 |
| F7 | Tabella unica degli encoder (puntuale / differenziale modulo costanti, solitoni inclusi / GLM). Niente "decidibile via Kovacic". NS-EQUIV su Ω limitato: parziale | O7 |
| F8 | SYS-T1 candidato con verifica Oberst obbligatoria. Criterio di esistenza (zoccoli ≤ 1) come obiettivo S8-SYS. G-T0 come osservazione | O8 |
| F9 | Tabella di raccordo (modello di dato, dominio, modello di calcolo, oggetto E_int) per ogni enunciato. Simboli rinominati. ENC-N2(a) "a meno di fase temporale". Risposta esplicita alla domanda 1 (forma hamiltoniana ⇒ α, β identificati esattamente). Risposta alla domanda 3 detta in chiaro (nel limite, mai certificata) | O9 |
| F10 | Punti di O10 (N1(v) non lineare, CONV-T1(5), HOR-P1 con costante, VAR-C7 etichetta, novità di N1(i)–(iii)/N2) | O10 |
