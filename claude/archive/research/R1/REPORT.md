# R1 — REPORT (Fase 1): spazi di Hilbert ↔ ML in forma analitica; L¹ vs L²

Agente R1 · 22/10/2026 · item C1 (C1.0–C1.4), P2 (P2.1–P2.3), domanda B8 (+ Pg.C-C1, Pg.D-D1).
Notazione: `NOTAZIONE.md`. ID: `[R1-T#]` teorema, `[R1-P#]` proposizione, `[R1-C#]` controesempio, `[R1-Q#]` aperto (in `open_questions.md`).
Stato ∈ {NOTO (con fonte), DIMOSTRATO (qui, prova completa), APERTO, PROBABILMENTE FALSO / FALSO}.

**Skill caricate (Regola 2).** `anthropic-skills:deep-research` (strumento Skill): ne ho seguito il workflow (scomposizione in sotto-temi → note → sintesi con citazioni) eseguendolo direttamente, senza generare subagenti (R1 è già un subagente). Letti e seguiti i `SKILL.md` (nessuno script `_vendor` eseguito): `math-skill` (modo `proof`: esplorazione separata dalla prova, ricerca di controesempi prima), `scientific-agent-skills/sympy`, `scientific-agent-skills/paper-lookup` e `ARIS/research-lit` (verifica bibliografica via WebSearch/WebFetch su arXiv), `scientific-critical-thinking` (§8).
**Controlli simbolici:** `research/R1/sympy/r1_checks.py` (+`.out`), `r1_airy_check.py` (+`.out`), eseguiti con `.venv\Scripts\python.exe -I`.

---

## 0. Sintesi
1. **C1.0 è ben posto**: il funtore catalogo → RKHS è il teorema di Aronszajn sulle somme di nuclei: `K = Σ_n K_n`, `H_K = Σ_n H_{K_n}` con la norma della *decomposizione di energia minima*. Lo split L² di `u` è `u_n = K_n K⁻¹ u` (filtro di Wiener / media a posteriori dei GP additivi). [R1-T1, R1-T3]
2. **Bound di Riesz in funzione della coerenza inter-classe**: l'unione di classi di Riesz è di Riesz ⟺ il coseno dell'angolo di Friedrichs `c = ‖G₁^{-1/2} C G₂^{-1/2}‖ < 1`; bound `(1−c)·min A_n`, `(1+c)·max B_n`. [R1-P4, DIMOSTRATO]
3. **Esempi del funtore**: il dizionario continuo delle gaussiane del calore al tempo s dà il nucleo RBF gaussiano `G_{2s}`, con `H_K = e^{s∂²}L²` (= dati evoluti dal calore per un tempo s). Gli esponenziali decrescenti danno nuclei completamente monotoni `φ(x+y)`. Airy e trasporto (gruppi unitari) danno il nucleo δ: a tempo fisso non c'è RKHS, e la classe va definita nello spazio-tempo (Ehrenpreis, G6). [R1-P2]
4. **A7 (le basi devono essere numerabili?)**: no, in generale. Gli esponenziali reali in L²(0,∞) sono completi XOR minimali (Müntz–Szász / Blaschke), quindi non sono mai una base. Sono di Riesz nella loro chiusura ⟺ vale la condizione di Carleson. [R1-T5]
5. **B8, risposta principale**: si scompone `E_int = E_int^⊥ + E_int^∥`. La parte `E_int^⊥ = P^⊥u`, cioè quella fuori da `closure(span ⋃D_n)`, è **indipendente da QUALSIASI regolarizzatore** nel limite α→0 [R1-T6, DIMOSTRATO]. È ≠ 0 se `Qu ≠ 0` per qualche `Q ∈ ⋂_n 𝒟L_n`; per le ODE vale ⟺ `LCLM(L_n)u ≠ 0` [R1-T7, DIMOSTRATO]. Quindi "ℒ_ALT elimina E_int" è **FALSO** in generale, e la risposta a Pg.C-C1 ("ci sono regolarizzazioni che lo eliminano?") è **NO**.
6. Il regolarizzatore agisce SOLO su `E_int^∥`, l'ambiguità nello span (`ker S`, ovvero `H_{K₁}∩H_{K₂}`). Lì ℓ¹ restituisce lo split sparso vero sotto NSP, ERC, coerenza o cluster-coherence; ℓ² restituisce lo split vero ⟺ `c ⊥ ker S` [R1-P8]. Con fattorizzazione coprima l'ambiguità è finito-dimensionale (una "gauge"); per le ODE coprime è nulla, e lo split è unico per OGNI metodo.
7. **D1 (encoding+grouping ⇒ E_int→0)**: nessun encoder lineare, limitato e con inverso limitato riduce `E_int^⊥` [R1-P9]. Serve un encoder NON lineare (log-simbolo, G3/RT-2; oppure K_0 di RT-S1d).
8. **P2.2: coerenze in forma chiusa** (SymPy). Gaussiane: `√(2σ₁σ₂/(σ₁²+σ₂²))·e^{−(a−b)²/2(σ₁²+σ₂²)}`. Esponenziali: `sech(½|log λ/μ|)` (distanza iperbolica). Gaussiana vs gaussiana evoluta da Airy: `2√π σ(3t)^{−1/3}e^{2b³/3}Ai(b²)` ~ `t^{−1/3}`. Per i dizionari continui μ→1, quindi i teoremi di coerenza e di RIP sono **vacui**. Valgono solo la super-risoluzione con separazione oppure, per il calore, la **positività** (T-sistemi, Schiebinger–Robeva–Recht, senza separazione).
9. Nel caso esatto l'identificabilità è algebrica (Prony/annullatore, rango); CS e ℓ¹ aggiungono stabilità, non identificabilità (confermato da R8: Scholl–Bacho–Boche–Kutyniok (arXiv:2210.08342) Cor. 1; He–Zhao–Zhong 2024 Thm 3.2). Cercare λ sparso in `ker 𝔾(u)` è il problema del vettore più sparso in un sottospazio, NP-hard in generale (Coleman–Pothen). → R4.
10. **GP**: la media a posteriori coincide con la soluzione RKHS regolarizzata (Kimeldorf–Wahba); EPGP realizza G6 come prior in `ker P`. **Koopman/DMD** per `u_t=a(∂_x)u`: autovalori `e^{a(iκ)Δt}` su `supp û₀` (DMD = Prony nel tempo), con ambiguità di ramo `2πi/Δt` per i simboli dispersivi.

---

## 1. C1 — Spazio di rappresentazione

### 1.1 Teoremi di base
**[R1-T1] (Moore–Aronszajn; somma di nuclei) — NOTO.** *Fonte:* Aronszajn 1950, Part I §2 (esistenza e unicità dell'RKHS per ogni nucleo definito positivo) e Part I §6, Thm I (somma). *Enunciato:* se `K₁, K₂` sono nuclei definiti positivi su X, allora `K = K₁+K₂` ha RKHS `H_K = {f₁+f₂ : f_i ∈ H_{K_i}}`, con `‖f‖²_K = min{‖f₁‖²_{K₁}+‖f₂‖²_{K₂} : f=f₁+f₂}`. Se `H_{K₁}∩H_{K₂}={0}` la somma è diretta e `‖f‖²=‖f₁‖²+‖f₂‖²`.
*Specializzazione:* se `K_n` è il nucleo della classe n del catalogo C2, allora `H_𝒟 := H_{ΣK_n}` è esattamente lo spazio di C1.0. La sua norma è l'energia della decomposizione più economica di `u` in componenti, cioè ℒ_G (L²) applicato per classi.

**[R1-T2] (spazio delle feature / sintesi) — NOTO.** *Fonti:* Steinwart–Christmann 2008, Thm 4.21; Paulsen–Raghupathi 2016, capp. 2–3. Teorema di Papadakis: `{f_s}` è un frame di Parseval di `H_K` ⟺ `K(x,y)=Σ_s f_s(x)conj(f_s(y))` puntualmente. La numerazione "Thm 2.10" viene da una fonte secondaria ed è da verificare sul libro. *Enunciato:* se `K(x,y)=⟨Φ(y),Φ(x)⟩_F` con `Φ: X→F` (F di Hilbert), allora `H_K = {x↦⟨w,Φ(x)⟩ : w∈F}` con `‖f‖ = min‖w‖_F`. La sintesi `S: F→H_K` è una coisometria, ed è un'isometria ⟺ è iniettiva.
*Specializzazione (G6 / RT-7):* per `P(∂)` a coefficienti costanti e una misura μ su `V(P)`, si pone `K_P(x,y)=∫_{V(P)}e^{⟨x,z⟩}conj(e^{⟨y,z⟩})dμ(z)` (con operatori noetheriani se P non è radicale). Allora `H_{K_P} ≅ L²(V(P),μ)/ker S`. **G6 è vero come quoziente, ed è un'isometria ⟺ la sintesi di Fourier–Laplace–Ehrenpreis è iniettiva su L²(μ).** Esempio, il calore: μ su `ξ∈iℝ` dà la trasformata di Fourier, che è iniettiva. Questo è il costrutto EPGP (§4).

**[R1-P1] (l'RKHS di una classe contiene solo soluzioni) — DIMOSTRATO.** Sia `K` continuo su `Ω×Ω` con `K(·,y) ∈ ker P` (in 𝒟′(Ω)) per ogni y, e P operatore differenziale a coefficienti lisci. Allora ogni `f∈H_K` soddisfa `Pf=0` in 𝒟′(Ω).
*Prova.* Le combinazioni finite `f_m=Σc_iK(·,y_i)` sono dense in `H_K` e soddisfano `Pf_m=0`. Se `f_m→f` in `H_K`, allora `|f_m(x)−f(x)| ≤ ‖f_m−f‖_K·K(x,x)^{1/2}`. Poiché `K(x,x)` è limitato sui compatti, la convergenza è uniforme sui compatti, quindi vale in 𝒟′. P è continuo su 𝒟′, dunque `Pf_m→Pf` e `Pf=0`. ∎ *Conseguenza:* `H_{K_n} ⊆ ker T_n` e `H_𝒟 ⊆ Σ_n ker T_n` (si veda §3 per B8).

### 1.2 C1.1 — Spazi candidati: verdetto
| Spazio | Pro | Contro | Verdetto |
|---|---|---|---|
| L²(Ω), H^k(Ω) | i nuclei `ker T_n` sono **chiusi**; proiezioni e residui sono ben definiti | la sintesi da atomi di calore è compatta, con valori singolari `e^{−sκ²}` (severamente mal posta, Hohage 2000) | spazio ambiente per i residui (§3) |
| RKHS `H_{ΣK_n}` [R1-T1] | split di energia minima in forma chiusa; rappresentante; GP | la norma dipende dalla misura e dai pesi scelti nella classe | **scelta raccomandata per C1.0** |
| Bargmann/Fock | gaussiane = stati coerenti = nuclei riproducenti; Segal–Bargmann = semigruppo del calore + continuazione analitica (Bargmann 1961; Hall 1994) | specifico della classe del calore | encoder analitico per la componente diffusiva |
| Ehrenpreis `L²(V(P),μ)` [R1-T2] | contiene esattamente soluzioni; frame continuo; numerabile su 𝕋 | V(P) dipende dall'incognita P | VERO come quoziente (G6) |
| Misure con norma TV | ℓ¹ su dizionari continui = norma atomica; super-risoluzione | non è hilbertiano | necessario per P2 con parametri continui |

**[R1-P2] (esempi del funtore C2 → RKHS) — DIMOSTRATO.**
(a) *Calore.* Prendiamo gli atomi `G_s(x−a)=(4πs)^{−1/2}e^{−(x−a)²/4s}`, `a∈ℝ`, con misura di Lebesgue. Allora `K(x,y)=∫G_s(x−a)G_s(y−a)da=G_{2s}(x−y)` (proprietà di semigruppo), che è il **nucleo gaussiano RBF** del ML. Per [R1-T2], `H_K=e^{s∂²}L²(ℝ)={f:∫|f̂|²e^{2sκ²}dκ<∞}` con `‖f‖=‖e^{−s∂²}f‖_{L²}` (il semigruppo è iniettivo). Quindi la regolarizzazione gaussiana di B5 e la classe del calore coincidono: l'RKHS gaussiano è l'insieme dei dati evoluti dal calore per un tempo s.
(b) *Reazione/rilassamento.* Atomi `e^{−λx}` su (0,∞), con `λ~ν`: `K=∫e^{−λ(x+y)}dν(λ)=φ(x+y)`, con φ completamente monotona (Bernstein). Per ν di Lebesgue si ottiene `1/(x+y)` (nucleo di Carleman).
(c) *Airy e trasporto (gruppi unitari).* Per `Â_t(κ)=e^{iκ³t}` si ha `∫A_t(x−a)conj(A_t(y−a))da=δ(x−y)`: non c'è RKHS a tempo fisso (si ottiene L² stesso). Il dizionario va quindi definito nello spazio-tempo (Ehrenpreis), non a tempo fisso.

### 1.3 C1.2 — Rappresentante e forma chiusa
**[R1-T3] (rappresentante) — NOTO.** *Fonti:* Kimeldorf–Wahba 1971; Schölkopf–Herbrich–Smola 2001, Thm 1. Ogni minimizzatore di `c((x_i,y_i,f(x_i))_i)+g(‖f‖_K)`, con g strettamente crescente, è della forma `f=Σα_iK(·,x_i)`. Nel caso L² si ha `α=(𝐊+αI)^{−1}y`; nel caso esatto (α→0), `𝐊^{+}y`, l'interpolante di norma minima.
*Dato completo (non campionato):* `min‖ω‖₂ s.t. Sω=u` dà `ω=S*(SS*)^{+}u`, cioè i coefficienti del frame duale canonico `ω_j=⟨u,(SS*)^{−1}e_j⟩`. Le componenti sono `u_n=S_nS_n*(SS*)^{−1}u=K_nK^{−1}u`, che coincidono con la media a posteriori della componente n in un GP additivo `f=Σf_n`, `f_n~GP(0,K_n)`.
**[R1-T4] (Tikhonov, α→0) — NOTO.** *Fonte:* Engl–Hanke–Neubauer 1996, cap. 2 (Moore–Penrose; criterio di Picard `y∈D(T^†) ⟺ Σ|⟨y,u_n⟩|²/σ_n²<∞`) e cap. 5 (`(T*T+αI)^{−1}T*y → T^†y` ⟺ `y∈D(T^†)=R(T)⊕R(T)^⊥`); i numeri dei teoremi sono da verificare sul testo. Per ℓ¹: Scherzer et al. 2009, cap. 3 (i minimizzatori convergono a soluzioni di ℓ¹-norma minima); Grasmair–Haltmeier–Scherzer 2011 CPAM: convergenza lineare ⟺ condizione sorgente `∃w: S*w∈∂‖c‖₁` più iniettività ristretta al supporto. In dimensione finita è il certificato duale di Fuchs 2004. *Specializzazione:* con gli atomi di calore il problema è esponenzialmente mal posto; nel caso esatto il limite esiste se vale Picard, ma senza condizioni sorgente non ci sono tassi (al più logaritmici, Hohage 2000).

### 1.4 C1.3 — Completezza, minimalità, Riesz (A7)
Fatto standard (Christensen 2016, capp. 3, 5–7): `{e_j}` è di Riesz con bound (A,B) ⟺ la Gram soddisfa `AI ≤ G ≤ BI` su ℓ²; base di Riesz ⟺ Riesz e completa ⟺ frame esatto; il duale canonico è `(SS*)^{−1}e_j`.
**[R1-P4] (bound di Riesz dell'unione vs coerenza inter-classe) — DIMOSTRATO.** Siano `D₁,D₂` di Riesz con bound `(A_n,B_n)`, chiusure `H_n` e Gram incrociata `C=(⟨e_{2,j},e_{1,i}⟩)`. Sia `c:=‖P_{H₁}P_{H₂}‖=‖G₁^{−1/2}CG₂^{−1/2}‖` (coseno dell'angolo di Friedrichs/Dixmier). Allora `D₁∪D₂` è di Riesz ⟺ `c<1`, e in tal caso `A≥(1−c)min(A₁,A₂)` e `B≤(1+c)max(B₁,B₂)`.
*Prova.* Per `f_n∈H_n`: `‖f₁+f₂‖² ≥ ‖f₁‖²+‖f₂‖²−2c‖f₁‖‖f₂‖ ≥ (1−c)(‖f₁‖²+‖f₂‖²)`; il bound superiore `≤(1+c)(…)` è analogo; si conclude con `‖f_n‖²∈[A_n,B_n]‖ω_n‖²`. Se c=1 esistono `f₁^k,f₂^k` unitari con `‖f₁^k−f₂^k‖→0`, quindi manca il bound inferiore. ∎
Tramite la coerenza (test di Schur): `c ≤ (A₁A₂)^{−1/2}(max_iΣ_j|C_ij|·max_jΣ_i|C_ij|)^{1/2}`. Con N classi basta `Σ_{m≠n}c_{nm}<1` (Gershgorin a blocchi).
**[R1-T5] (esponenziali reali: completi XOR minimali) — NOTO.** *Fonti:* Müntz–Szász (Szász 1916); Shapiro–Shields 1961 (Amer. J. Math. 83(3):513–532); Nikolski 1986; Avdonin–Ivanov 1995. Il ponte è l'isometria di Laplace/Paley–Wiener `L²(0,∞)→H²(ℂ₊)`, che manda `e^{−λt}` in `1/(s+λ)`, un multiplo del nucleo riproducente di H²(ℂ₊). Per `Re λ_n>0`: completo in L²(0,∞) ⟺ `ΣReλ_n/(1+|λ_n|²)=∞` (non-Blaschke); minimale ⟺ la somma è finita (Blaschke). Quindi **non è mai una base**. È di Riesz nella sua chiusura ⟺ `{λ_n}` è interpolante di Carleson: `inf_nΠ_{k≠n}|λ_n−λ_k|/|λ_n+conj(λ_k)|>0` (es. `λ_n=q^n`, q>1).
Altri casi: per esponenziali immaginari su un intervallo, base di Riesz sotto `|λ_n−n|≤L<1/4` (Kadec 1/4; Young 2001, cap. 1). Le traslate di una gaussiana su αℤ sono di Riesz per ogni α>0, ma non complete in L²(ℝ) (Christensen capp. 9–10). **Risposta ad A7:** in generale servono frame continui (Ali–Antoine–Gazeau 1993); famiglie numerabili si ottengono solo discretizzando V(P) sotto condizioni di densità; su 𝕋 ci sono basi numerabili (Fourier).

### 1.5 C1.4 — Sistema duale
- Frame: duale canonico `(SS*)^{−1}e_j`; Riesz: biortogonale unico. Gaussiane su reticolo: generatore duale `ĝ/Σ_k|ĝ(·+2πk/α)|²`. Esponenziali minimali: biortogonale costruito dal prodotto di Blaschke con zeri `{λ_n}` (Nikolski; Avdonin–Ivanov cap. II). Airy/trasporto: `S(t)` è unitario, quindi il duale di `S(t)e_j` è `S(t)ẽ_j`.
- Per P3: `⟨ẽ_{n,i},E_int⟩` è canonico solo se l'unione delle classi è di Riesz (c<1, R1-P4). Con un frame ridondante esistono infiniti duali e la quantità dipende dalla scelta.

### 1.6 Valutazione di RT-R3a (R3: sistema biortogonale di Rosenbloom–Widder) — richiesta di central
**Oggetti.** Polinomi del calore `v_n(x,t)=n!Σ_k x^{n−2k}t^k/(k!(n−2k)!)` (soluzioni di `u_t=u_xx`) e funzioni associate `w_n` (trasformata di Appell di `v_n`), con `⟨v_n,w_m⟩=2^n n! δ_nm`. Fonte: Rosenbloom–Widder 1959, Trans. AMS 92, 220–266. Teorema di sviluppo: `u=Σa_nv_n` converge nella striscia `|t|<σ` ⟺ u si estende a una funzione intera in x di ordine ≤ 2 e tipo legato a σ (enunciato esatto nella fonte, da riportare da R3).
**[R1-P11] (in quale spazio è una base di Riesz) — DIMOSTRATO (SymPy `r1_heatpoly.out`).** Si fissi s>0 e si definisca
`𝓗_s := {u soluzione di u_t=u_xx definita per t>−s′ con s′>s e u(·,−s) ∈ L²(ℝ, G_s dx)}`, con `‖u‖_s := ‖u(·,−s)‖_{L²(G_s dx)}`, dove `G_s=(4πs)^{−1/2}e^{−x²/4s}`.
Allora `{v_n}` è una **base ortogonale** di `𝓗_s` (quindi, normalizzata, una base di Riesz con A=B=1), con `‖v_n‖²_s=(2s)^n n!`.
*Prova.* `v_n(x,−s)=s^{n/2}He_n(x/√(2s))·2^{n/2}` è il polinomio di Hermite (probabilisti) riscalato; SymPy verifica che `∫v_n(x,−s)v_m(x,−s)G_s dx=(2s)^n n! δ_nm` (n,m<6), che `v_n(x,−1/2)=He_n(x)` e che `2^n v_n(x,−1/4)=H_n(x)`. I polinomi di Hermite sono completi in `L²(G_s dx)`. La mappa `u ↦ u(·,−s)` è iniettiva (unicità all'indietro nella classe di crescita in cui `e^{s∂²}` è definito) e manda `v_n` nella base ortogonale di Hermite. ∎
*Lettura funzionale.* `𝓗_s` è un RKHS di soluzioni del calore. Il suo nucleo è la serie di Mehler `K((x,t),(y,τ))=Σ_n v_n(x,t)v_n(y,τ)/((2s)^n n!)`, che converge per |t|,|τ|<s. Tramite `u ↔ U(z)=Σa_nz^n` è isometricamente uno **spazio di Fock pesato** (`‖z^n‖²=(2s)^n n!`, Bargmann 1961). Il duale di `v_n` in `𝓗_s` è `v_n/‖v_n‖²_s`; la `w_n` di Rosenbloom–Widder ne è la realizzazione come funzionale integrale a tempo +s: `⟨u,w_n⟩=∫u(x,−s)w_n(x,s)dx`, con `w_n(x,s)=G_s(x)v_n(x,−s)/s^n`. Questo è coerente con `⟨v_n,w_m⟩=2^n n! δ_nm` (verificato: `(2s)^n n!/s^n=2^n n!`).
*In L²(ℝ) a t≥0 non è una base* (i `v_n` non stanno in L²). Nello spazio di Rosenbloom–Widder (funzioni intere di ordine 2) c'è convergenza ma non una struttura di Hilbert.
**Verdetto RT-R3a.** Promuovere come risposta costruttiva ad A7 e come C1.4 per la classe del calore: `{v_n}` è numerabile, con duale esplicito, ed è base ortogonale nello spazio di Hilbert `𝓗_s` = Fock/Bargmann pesato = RKHS di Mehler. **Limiti:** (i) 𝓗_s contiene solo soluzioni "analitiche all'indietro" fino a −s (dati iniziali intere di ordine ≤2): esclude il nucleo del calore `G_t(x)` stesso, che è singolare in t=0, e quindi non contiene gli atomi di R1-P2a (che sono e^{s∂²}L²). Le due rappresentazioni sono complementari (polinomi = sviluppo di Taylor nel punto t=−s; gaussiane = sintesi in avanti). (ii) Coerenza con le altre classi: `v_n` sono polinomi, quindi altamente coerenti con le classi polinomiali (es. `ker ∂_x²`): per [R1-P4] l'unione con classi polinomiali NON è di Riesz (intersezione non banale). È la gauge `ker(L₁,L₂)` di R1-P8.

---

## 2. P2 — L¹ vs L²
### 2.1 P2.1 — Teoremi di recupero esatto
Setting: `S` = sintesi del dizionario `D=⋃D_n`, colonne normalizzate; BP: `min‖ω‖₁ s.t. Sω=u`.
| # | Teorema | Ipotesi esatte | Conclusione | Fonte |
|---|---|---|---|---|
| T-a | Spark | `spark(A)>2s` | x s-sparso è l'unica soluzione s-sparsa | Donoho–Elad 2003 PNAS |
| T-b | NSP | `‖v_S‖₁<‖v_{S^c}‖₁ ∀v∈ker A∖0, |S|≤s` | BP recupera ogni s-sparso **⟺** NSP | Donoho–Huo 2001; Gribonval–Nielsen 2003; Foucart–Rauhut 2013 Thm 4.5 |
| T-c | Coerenza | `μ=max_{i≠j}|⟨a_i,a_j⟩|`, `s<(1+1/μ)/2` | unicità ℓ⁰; BP e OMP esatti | Donoho–Elad 2003; Gribonval–Nielsen 2003; Tropp 2004 Cor. 3.6 |
| T-c′ | Due basi ON | `s<(√2−1/2)/μ` | BP esatto; `‖α‖₀+‖β‖₀≥2/μ` | Elad–Bruckstein 2002 |
| T-d | ERC (per supporto) | `max_{j∉Λ}‖A_Λ⁺a_j‖₁<1` | BP e OMP esatti per ogni x con supp ⊆ Λ; implicato da Babel `μ₁(s−1)+μ₁(s)<1` | Tropp 2004 Thm 3.1, 3.3, 3.5 |
| T-e | Lasso con residuo | ERC(Λ) e `‖A*(u−Ac_Λ)‖_∞ ≤ γ(1−max_{j∉Λ}‖A_Λ⁺a_j‖₁)` | il minimizzatore di `½‖u−Aω‖²+γ‖ω‖₁` ha supp ⊆ Λ, è unico, `‖ω*−c_Λ‖_∞≤γ‖(A_Λ*A_Λ)^{−1}‖_{∞,∞}` | Tropp 2006 Thm 8 |
| T-f | RIP | `δ_{2s}<√2−1` (ottimale `<1/√2`) | BP esatto e stabile | Candès–Tao 2005; Candès 2008; Cai–Zhang 2014 |
| T-g | Cluster coherence (separazione) | `Φ₁,Φ₂` frame di Parseval; `‖1_{Λ₁^c}Φ₁*u₁‖₁+‖1_{Λ₂^c}Φ₂*u₂‖₁≤δ` | la soluzione di `min‖Φ₁*v₁‖₁+‖Φ₂*v₂‖₁ s.t. v₁+v₂=u` soddisfa `‖v₁−u₁‖+‖v₂−u₂‖≤2δ/(1−2κ)`, con `κ≤max{μ_c(Λ₁,Φ₁;Φ₂),μ_c(Λ₂,Φ₂;Φ₁)}` e `μ_c(Λ,Φ;Ψ)=max_jΣ_{i∈Λ}|⟨φ_i,ψ_j⟩|` | Donoho–Kutyniok 2013 CPAM, Prop. 2.1 + Lemma 2.1 (verificato su arXiv:1004.3006) |
| T-h | Super-risoluzione | spike su 𝕋, frequenze `|k|≤f_c`, separazione `≥2/f_c` | la norma TV/atomica recupera esattamente | Candès–Fernandez-Granda 2014 CPAM Thm 1.2 |
| T-i | Positività | sorgenti ≥0, PSF gaussiana (T-sistema), >2s misure | unica misura ≥0 consistente, **senza separazione** | Schiebinger–Robeva–Recht 2018 |
| T-j | Block sparsity | block-coerenza μ_B, sub-coerenza ν, blocchi di taglia d: `kd<½(μ_B^{−1}+d−(d−1)ν/μ_B)` | group-ℓ¹ recupera i blocchi attivi | Eldar–Kuppinger–Bölcskei 2010 |
| T-k | BLASSO | certificato non degenere | supporto esatto e stabile | Duval–Peyré 2015 FoCM |

### 2.2 P2.2 — Coerenze tra classi
**[R1-P5] — DIMOSTRATO (SymPy: `r1_checks.out` [1]–[3], `r1_airy_check.out`).**
- Gaussiane `e^{−(x−a)²/2σ₁²}`, `e^{−(x−b)²/2σ₂²}` in L²(ℝ) (calore: σ²=2s): `μ=√(2σ₁σ₂/(σ₁²+σ₂²))·e^{−(a−b)²/(2(σ₁²+σ₂²))}`; a centro comune `μ²=sech(log(σ₂/σ₁))`.
- Esponenziali `e^{−λx}, e^{−μx}` in L²(0,∞): `μ=2√(λμ)/(λ+μ)=sech(½|log(λ/μ)|)`, funzione della distanza iperbolica (coerente con R1-T5).
- Gaussiana g (larghezza σ) vs `S_Airy(t)g` (`u_t+u_xxx=0`): `μ(t)=2√πσ(3t)^{−1/3}e^{2b³/3}Ai(b²)` con `b=σ²(3t)^{−2/3}`. Si ha μ→1 per t→0 e `μ~2√πσAi(0)(3t)^{−1/3}` per t→∞. La verifica ad alta precisione coincide a 15 cifre per (σ,t) ∈ {(1,1), (1,10), (0.5,3)}. *Derivazione:* `∫e^{ik³/3−bk²}dk=2πe^{2b³/3}Ai(b²)`, con la traslazione `k→k−ib` che elimina il termine quadratico.

**Lettura (P2.1 specializzato).** I dizionari di nuclei sono parametrizzati con continuità (centro, scala, esponente λ, tempo t), e ogni discretizzazione fine ha μ→1 (atomi vicini quasi paralleli). Quindi T-a…T-f garantiscono solo s<1: sono **vacui**. Restano tre tipi di garanzie non banali: (i) separazione minima nel parametro (T-h/T-k; per gli esponenziali è separazione iperbolica, R1-T5); (ii) positività per il calore (T-i: soluzioni con dato iniziale ≥0 sono misure positive di gaussiane, recuperabili senza separazione); (iii) cluster coherence tra classi diverse (T-g; gaussiane e Airy sono incoerenti come `t^{−1/3}`). La RIP richiede campionamenti casuali di (t,x) e non è verificabile in modo deterministico (NP-hard, Tillmann–Pfetsch 2014): **non pertinente** al problema esatto.
**[R1-P6] (esatto ⇒ identificabilità algebrica) — NOTO.** Senza rumore, `u=Σ_{j≤s}c_je^{λ_jx}` è determinato (λ_j inclusi) da 2s valori equispaziati via Prony/Hankel, *senza ipotesi di separazione o coerenza*; un polinomio s-sparso da 2s valutazioni in progressione geometrica (Ben-Or–Tiwari 1988). Conferma da R8 (inbox R1): Scholl–Bacho–Boche–Kutyniok 2026 (Machine Learning; arXiv:2210.08342), Cor. 1 (unicità ⟺ indipendenza lineare delle feature del jet); He–Zhao–Zhong 2024 (FoCM), Thm 3.2 (condizione sul supporto di Fourier, nessuna coerenza). **ℓ¹/CS non serve per l'identificabilità; serve per la stabilità o la selezione.**
**[R1-P7] (sparsità di λ) — NOTO + riduzione.** Trovare λ sparso e normalizzato con `𝔾(u)λ=0` significa trovare il vettore più sparso nel sottospazio `ker𝔾(u)=Ann(u)∩span(dizionario)`: NP-hard in generale (Coleman–Pothen 1986, "null space problem"). Se dim ker 𝔾 = 1 la sparsità è superflua. Per le ODE il criterio canonico non è la sparsità ma l'ordine minimo (Ann(u) è principale); per le PDE, la base di Gröbner ridotta dell'ideale (→ R2/R4).
**Risposta di R4 (integrata).** Si veda `research/R4/REPORT.md` §2.
- [R4-T1]: per le ODE `dim ker 𝔾_n(u)=n+1−d`, quindi u è identificabile ⟺ n=d.
- [R4-T4]: su 𝕋 vale ⟺ `|supp û₀| ≥ n+1`; con coefficienti reali la condizione diventa `|S∪(−S)| ≥ n+1`.
- [R4-T5]: per le PDE si usa un criterio di Bézout sulle componenti di V(P).
- **[R4-C1], controesempio cruciale:** per `u=e^x`, `D^k−1` annulla u per ogni k. Ci sono quindi infiniti annullatori 2-sparsi non proporzionali, e spark/NSP su 𝔾(u) falliscono *strutturalmente* quando il dizionario contiene più ordini del necessario.
- Il criterio canonico è la **filtrazione per grado**: si prende il primo n con `ker 𝔾_n≠0`. È algebra lineare graduata, polinomiale, che sostituisce il "vettore più sparso" (NP-hard).
- Con campioni generici (t_i,x_i) l'identificabilità è generica (q.c.), non RIP.
**Conclusione per P2: per l'identificazione di λ, ℓ¹ è sia superfluo (rango + grado minimo) sia inaffidabile (R4-C1); ℓ¹ resta pertinente solo per la decomposizione di u (E_int^∥, §3).**

### 2.3 P2.3 — Altri regolarizzatori (B7)
- **Group-ℓ¹** `Σ_n‖ω_n‖₂`, con i gruppi = classi C2: seleziona *quali termini/componenti sono attivi*, cioè identifica i termini di L, con le garanzie T-j; dentro un gruppo distribuisce come ℓ² (R1-P8). Varianti: sparse-group lasso (Simon–Friedman–Hastie–Tibshirani 2013); quadro generale: structured sparsity (Bach–Jenatton–Mairal–Obozinski 2012). È la versione analitica del "GROUPING" di D1.
- **Separazione morfologica (MCA)** `min Σ_n‖Φ_n*u_n‖₁ s.t. Σu_n=u` (Starck–Elad–Donoho 2005; Donoho–Kutyniok 2013, T-g): è **esattamente A8 in forma ℓ¹ di analisi** (NEW-ROUTE; SCOUT-2 copre lo stesso tema, si veda §7).
- **Norma atomica / TV di misure** (Chandrasekaran–Recht–Parrilo–Willsky 2012; Candès–Fernandez-Granda 2014): è l'ℓ¹ corretto per dizionari a parametro continuo.
- **TV** (Rudin–Osher–Fatemi 1992): pertinente solo per classi con salti (trasporto di discontinuità).
- **Reweighted ℓ¹** (Candès–Wakin–Boyd 2008): approssima ℓ⁰ e migliora le soglie; non cambia R1-T6.
- **Lettura bayesiana di B5/B6:** ℓ² è il MAP con prior gaussiana su ω, e il posterior di u è il GP con covarianza `SS*=K` (§4). ℓ¹ è il MAP con prior di Laplace, ma la **media** a posteriori laplaciana non è sparsa (Gribonval 2011). La frase di B5 "f_i ≈ gaussiana" va letta come prior gaussiana sui coefficienti; per la classe del calore anche la covarianza è gaussiana (R1-P2a).

---

## 3. B8 (con Pg.C-C1 e Pg.D-D1): ℒ_ALT elimina E_int?
**Definizioni.** `D=⋃_nD_n`, `M:=closure(span D)⊆H` (H = L²(Ω) o H^k), P la proiezione ortogonale su M. Per un regolarizzatore `R ≥ 0`, finito sulle successioni finite, sia `ω_α` un minimizzatore (o un ε_α-minimizzatore, con `ε_α/α→0`) di `½‖u−Sω‖²+αR(ω)`, e `r_α=u−Sω_α`. Si pone `E_int^⊥:=P^⊥u`; `E_int^∥` è l'ambiguità della scomposizione di `Pu` in componenti (data da `ker S`).

**[R1-T6] (il residuo limite non dipende dal regolarizzatore) — DIMOSTRATO.** Per OGNI R come sopra, `r_α→P^⊥u` in norma per α→0.
*Prova.* Poiché `Sω_α∈M`, `‖r_α‖²=‖P^⊥u‖²+‖Pu−Sω_α‖²`. Dato ε>0, si sceglie ω_ε finita con `‖Pu−Sω_ε‖²<ε` (le combinazioni finite sono dense in M). Per minimalità `½‖r_α‖² ≤ ½‖r_α‖²+αR(ω_α) ≤ ½‖P^⊥u‖²+ε/2+αR(ω_ε)+ε_α`. Quindi `limsup‖Pu−Sω_α‖²≤ε` per ogni ε, cioè `r_α−P^⊥u=Pu−Sω_α→0`. ∎
*Conseguenza:* la parte `E_int^⊥` **non è eliminata da nessun regolarizzatore** (L², L¹, group, TV, reweighted, …). Risposta a Pg.C-C1: **NO** per questa parte. `E_int^⊥=0 ⟺ u∈M` è una proprietà del **dizionario**, non del regolarizzatore.

**[R1-T7] (criterio per E_int^⊥ ≠ 0) — DIMOSTRATO.** Siano `L_1,…,L_N` operatori differenziali a coefficienti lisci su Ω aperto, `D_n⊆ker L_n` (in 𝒟′), e `Q∈⋂_n𝒟·L_n` (intersezione di ideali sinistri: `Q=A_nL_n` per ogni n). Se `u∈closure(Σ_n ker L_n)` (chiusura in L²_loc o in una topologia più fine di 𝒟′), allora `Qu=0` in 𝒟′. Quindi `Qu≠0 ⇒ E_int^⊥≠0`.
*Prova.* Per `v=Σv_n` con `v_n∈ker L_n`: `Qv=ΣA_nL_nv_n=0`. Q è continuo su 𝒟′ e la convergenza in L²_loc implica quella in 𝒟′, quindi `Qu=lim Qv^{(k)}=0`. ∎
*Casi.* (i) Coefficienti costanti: `Q=L₁⋯L_N`. (ii) **ODE:** `Σker L_n=ker LCLM(L_1,…,L_N)` (minimo comune multiplo sinistro; Ore 1933; van der Put–Singer 2003, cap. 2) ha dimensione finita, quindi è chiuso, e vale **`E_int^⊥=0 ⟺ LCLM(L_n)u=0`** (⟺, non solo ⇒).
*Esempi (A8 "un termine = una classe").* Scriviamo l'ODE `u″−u=0` come somma dei termini `T₁=D²` e `T₂=−1`. Le classi sono `ker D²=span{1,x}` e `ker(−1)={0}`; `LCLM=D²` e `D²e^x≠0`, quindi c'è un residuo non eliminabile: `‖P^⊥e^x‖²_{L²(0,1)}=20e−7e²/2−57/2≈3.94·10⁻³` (SymPy [4]). Con la fattorizzazione `(D−1)(D+1)` invece le classi `{e^x},{e^{−x}}` danno residuo 0 e Gram invertibile (det≈0.381), quindi lo split è unico. PDE: `u_t+cu_x=u_xx` con le classi calore e trasporto: `Q=(∂_t−∂²_x)(∂_t+c∂_x)` e `Qu=−c·u_xxx≠0` salvo che u sia un polinomio di grado ≤2 in x, quindi `E_int^⊥≠0` (coerente con G1: `ker L∩(ker L₁+ker L₂)` è finito-dimensionale).
*Il viceversa per le PDE* (`Qu=0 ⇒ u∈closure(Σker L_n)`) richiede Ehrenpreis–Palamodov su Ω convesso: è plausibile per fattori coprimi (G2), ma **APERTO** qui ([R1-Q2] → R2/R5).

**[R1-P8] (il regolarizzatore agisce solo su E_int^∥) — DIMOSTRATO.** Supponiamo `u=Sc` esattamente, così che le rappresentazioni esatte siano `c+ker S`.
(a) ℓ² restituisce c ⟺ `c∈(ker S)^⊥=closure(R(S*))` (la soluzione di norma minima è l'unico elemento di `c+ker S` ortogonale a ker S).
(b) ℓ¹ restituisce c ⟺ c è l'unico minimo ℓ¹ su `c+ker S` (NSP ristretta al supporto di c, T-b/T-d).
(c) Le componenti funzionali `u_n=S_nω_n` sono uniche per OGNI metodo ⟺ `H_m∩Σ_{n≠m}H_n={0}` per ogni m (somma diretta). In particolare per le **ODE con fattorizzazione coprima** (`ker L₁∩ker L₂=ker GCRD={0}`) lo split è unico e L¹ = L² = qualsiasi metodo. Per le PDE con fattori coprimi l'ambiguità è `ker L₁∩ker L₂=ker(L₁,L₂)` (tipicamente finito-dimensionale): una **libertà di gauge** finita.
**[R1-C1] (L² distribuisce il peso; SymPy [5]).** In ℝ², `D={e₁,e₂,(e₁+e₂)/√2}` e `u=(e₁+e₂)/√2`. Lo split sparso vero è `(0,0,1)` (ℓ¹-norma 1, unico minimo ℓ¹); ℓ² dà `(√2/4,√2/4,1/2)`, tutti non nulli, con ℓ¹-norma `1/2+√2/2>1`. Conferma B6/B7 per la parte nello span: "forse è meglio ℒ_ALT" è VERO per `E_int^∥` quando lo split vero è sparso e vale NSP/ERC.
**[R1-C2] (avvertenza).** Se `E_int` stesso è sparso nel dizionario unione (per esempio contiene atomi di una classe), ℓ¹ lo **assorbe nelle componenti**, cioè lo attribuisce erroneamente, invece di eliminarlo.

**[R1-P9] (D1: un encoder lineare non basta) — DIMOSTRATO.** Se `E:H→H′` è unitario, `dist(Eu,EM)=dist(u,M)`. Se E è limitato con inverso limitato, `‖E^{−1}‖^{−1}dist(u,M) ≤ dist(Eu,EM) ≤ ‖E‖dist(u,M)`. (E manda M sul sottospazio chiuso EM, e `‖Eu−Ev‖` è compreso tra i due multipli di `‖u−v‖`.) Quindi "ENCODING + GROUPING ⇒ E_int→0" (D1) è impossibile con encoder lineari (Fourier, wavelet, Bargmann inclusi) applicati al dizionario delle classi additive. Serve un encoder **non lineare** che trasformi prodotti di semigruppi in somme: il log-simbolo `∂_t log û=Σa_n(iκ)` (G3, RT-2), dove l'identificazione diventa una regressione lineare di Vandermonde su `supp û₀`, senza E_int e senza bisogno di ℓ¹ se `|supp û₀|≥#termini`; se il dizionario dei monomi è più grande, è interpolazione sparsa (Ben-Or–Tiwari/Prony). È coerente con RT-S1d di SCOUT-1: il passaggio a K_0 "dimentica" esattamente Ext¹ ed è additivo.

**Verdetto B8.** "ℒ_ALT elimina E_int" è **FALSO per la parte E_int^⊥** (qualunque regolarizzatore; R1-T6, R1-T7, controesempio ODE esplicito), quindi **PROBABILMENTE FALSO in generale**. È **VERO in senso ristretto**: ℓ¹ elimina l'ambiguità `E_int^∥` sotto NSP/ERC/cluster coherence (T-b, T-d, T-g) e, con group-ℓ¹, seleziona correttamente le classi attive (T-j). Sulla domanda "se non lo elimina va bene lo stesso?" (B8): sì. `E_int^⊥=P^⊥u` è un oggetto canonico, si calcola per proiezione, e il suo annullarsi è caratterizzato algebricamente (LCLM per le ODE).

---

## 4. Processi gaussiani come oggetti analitici
- **[R1-T8] (Kimeldorf–Wahba) — NOTO.** *Fonti:* Kimeldorf–Wahba 1970 (Ann. Math. Stat. 41); Rasmussen–Williams 2006 §6.2. Sia `f~GP(0,K)` con `y_i=f(x_i)+ε_i`, `ε~N(0,σ²)`. La media a posteriori è il minimizzatore di `Σ(y_i−f(x_i))²+σ²‖f‖²_K`, cioè la Tikhonov [R1-T3] con α=σ². Nel caso esatto (σ→0) è l'interpolante di norma minima.
- Le traiettorie di un GP **non** stanno in `H_K` (q.c.) quando dim H_K=∞ (Driscoll 1973; Lukić–Beder 2001): l'RKHS è lo spazio di Cameron–Martin, non il supporto della misura.
- **EPGP** (Härkönen–Lange-Hegermann–Raiță 2023, ICML; arXiv:2212.14319): per ogni sistema lineare a coefficienti costanti costruisce, via Ehrenpreis–Palamodov, una covarianza tale che ogni realizzazione è soluzione esatta. Realizza G6/RT-7. B-EPGP (Huang et al., arXiv:2411.16663) estende il costrutto ai problemi al bordo; Lange-Hegermann 2018 (NeurIPS) tratta i casi precedenti. Secondo R8, il lato algebrico di EPGP è di R2; qui resta il lato posterior.
- **GP additivi:** con `f=Σf_n`, `f_n~GP(0,K_n)` indipendenti, la media a posteriori di ciascuna componente è `K_nK^{−1}u`: è lo split L² di R1-T1/T3. La teoria degli additive GP (Duvenaud–Nickisch–Rasmussen 2011) è quindi lo strumento probabilistico per A8, ma eredita R1-T6: non tocca `E_int^⊥`.

## 5. Koopman / DMD (lato R1; R7 copre il lato nonlineare/Fase 4)
- **Fonti:** Koopman 1931; Mezić 2005 (Nonlinear Dyn. 41); Rowley et al. 2009 (JFM 641); Schmid 2010 (JFM 656); Tu et al. 2014 (J. Comput. Dyn. 1): **DMD esatta** — se le coppie di snapshot sono linearmente consistenti, autovalori e modi DMD sono autovalori e autovettori dell'operatore lineare che le collega. Convergenza EDMD→Koopman: Korda–Mezić 2018. Monografia: Mauroy–Mezić–Susuki 2020.
- **[R1-P10] (specializzazione) — DIMOSTRATO (algebra lineare elementare).** Sia `u_t=a(∂_x)u` su 𝕋, con `u₀` polinomio trigonometrico di supporto F. Allora `u(t_k)=Σ_{κ∈F}û₀(κ)e^{a(iκ)kΔt}e^{iκx}`: gli snapshot generano `span{e^{iκx}}_{κ∈F}` e l'operatore di avanzamento è diagonale con autovalori `e^{a(iκ)Δt}`. La DMD esatta (con ≥|F|+1 snapshot) restituisce quindi `{e^{a(iκ)Δt}, e^{iκx}}_{κ∈F}`: è Prony nel tempo, modo per modo. Conseguenze: (i) a è determinato solo su F (coerente con G4: serve `|F|≥deg a+1`); (ii) **ambiguità di ramo**: `a(iκ)` è noto solo modulo `2πi/Δt`, e per i simboli dispersivi (immaginari, es. `iκ³`) c'è aliasing se `Δt|κ|³≥π`; con dati continui nel tempo (∂_t esatto) l'ambiguità sparisce. Lo spettro di Koopman sulle osservabili polinomiali contiene il reticolo `{Σ_κ m_κ a(iκ)}`.
- Rilevanza: nel caso commutativo Koopman fornisce lo "split per direzione" di F6 (i modi di Fourier sono autofunzioni congiunte). Per termini non commutanti la DMD restituisce gli autovalori della somma, non quelli dei termini, quindi nessuna scomposizione per termine (→ R5/R7).

---

## 6. Tabella di stato
| Claim | Stato | Rif. |
|---|---|---|
| C1.0 funtore catalogo→RKHS ben definito (positività, completezza) | NOTO (Aronszajn) + DIMOSTRATO | R1-T1, R1-P1 |
| C1.0 bound di Riesz in funzione della coerenza inter-classe | DIMOSTRATO | R1-P4 |
| C1.1 G6: Ehrenpreis L²(V,μ) come RKHS di soluzioni | VERO come quoziente; isometria ⟺ sintesi iniettiva | R1-T2 |
| C1.2 forma chiusa ω = duale canonico; split `K_nK⁻¹u` | NOTO / DIMOSTRATO | R1-T3 |
| C1.3 / A7: servono basi numerabili | FALSO in generale (frame continui); gli esponenziali reali non sono mai basi | R1-T5 |
| C1.4 duali | NOTO; canonici solo se c<1 | §1.5 |
| P2.1 teoremi di recupero su dizionari di nuclei | NOTI; coerenza/RIP VACUI sui dizionari continui; validi separazione/positività/cluster coherence | §2 |
| P2.2 coerenze gaussiane/esponenziali/Airy | DIMOSTRATO (SymPy) | R1-P5 |
| B8: ℓ¹ elimina E_int | FALSO per E_int^⊥ (ogni regolarizzatore); VERO per E_int^∥ sotto NSP/ERC | R1-T6, T7, P8 |
| L² non può dare lo split sparso | VERO salvo `c⊥ker S` | R1-P8, R1-C1 |
| D1: encoding lineare ⇒ E_int→0 | FALSO (serve un encoder non lineare) | R1-P9 |
| Viceversa di R1-T7 per le PDE (Qu=0 ⇒ u nella chiusura) | APERTO (→ R2) | R1-Q2 |
| Identificazione di λ sparso in ker 𝔾 | NP-hard in generale; la sparsità fallisce strutturalmente (R4-C1); criterio canonico = grado minimo / Gröbner | R1-P7 + R4 |
| RT-R3a: polinomi del calore come base di Riesz | VERO in 𝓗_s (Fock pesato / RKHS di Mehler), base ortogonale; FALSO in L² | R1-P11 |

## 7. Messaggi scambiati
- → central: `PLAN-READY R1`; `NEW-ROUTE` (separazione morfologica / cluster coherence per A8; positività/T-sistemi per il calore); `AVVISO` (evidenza per RT-7, RT-2, RT-S1d); `DONE R1`.
- → R4: `TABELLA` dei teoremi di recupero + `DOMANDA` (identificabilità di rango vs sparsità; ideale Ann(u) e criterio canonico; campionamento casuale/RIP). ← R4 `RISPOSTA`: rango puro, grado minimo come criterio canonico, controesempio R4-C1, identificabilità campionata generica (integrata in §2.2).
- ← SCOUT-2 `AVVISO`: RT-S2b (Donoho–Kutyniok come forma di D1/B8 al limite di scala; la parte ℓ¹/coerenza resta a R1); gamblets parcheggiati (ortogonali per scala, non per termine). ← central `AVVISO`: valutare RT-R3a, fatto in §1.6.
- ← R8 (`AVVISO`): conferma che l'identificabilità esatta è di rango (Scholl et al.; He–Zhao–Zhong); segnala le sovrapposizioni con SCOUT-2 (MCA) e R7 (Koopman/DMD); EPGP lato algebrico assegnato a R2. → R8 `RISPOSTA`; → R7 e SCOUT-2 `AVVISO` (confini); → R5 `AVVISO` (E_int^⊥ / E_int^∥).
- ← PR-C2d: nessun messaggio ricevuto alle tre letture dell'inbox.

## 8. Valutazione critica (scientific-critical-thinking)
- I risultati DIMOSTRATO sono elementari ma completi, e le prove dipendono da ipotesi esplicite (Ω aperto, convergenza più fine di 𝒟′, ε-minimizzatori). R1-T6 è robusto: vale per ogni R≥0 finito sulle successioni finite.
- Rischio principale: la **definizione** di E_int del progetto non è ancora fissata (WP2/R5). R1-T6/T7 usano la definizione "residuo additivo rispetto alle classi". Nel quadro moltiplicativo/log-simbolo (G3) B8 cambia natura (non c'è un residuo additivo), e le conclusioni vanno riformulate quando R5 fisserà E_int.
- Numeri di teorema da verificare sul testo: Engl–Hanke–Neubauer capp. 2/5; Paulsen–Raghupathi Thm 2.10; Scherzer et al. cap. 3; Tropp 2004 Cor. 3.6; Foucart–Rauhut Thm 4.5. Verificati online: Donoho–Kutyniok Prop. 2.1/Lemma 2.1; Schiebinger–Robeva–Recht (Inf. Inference 7(1):1–30); EPGP (ICML 2023); Shapiro–Shields (Amer. J. Math. 83(3):513–532).
- Bias da evitare: la cornice "ML" (B5/B6) suggerisce che la regolarizzazione sia lo strumento centrale. I risultati mostrano invece che nel caso esatto è l'**algebra** (annullatori, LCLM, Prony) a decidere identificabilità ed `E_int^⊥`; la regolarizzazione fissa solo una libertà di gauge.
