# Plan — Analytic identification of linear differential operators from their kernel ("Problema base")

## Context
The user has 8 pages of handwritten notes (Italian, photographed upside down) about an algorithm they want to treat as a **proof**. Given a function that solves a 1D linear PDE (no noise, not a system), the goal is to recover the differential operator analytically. The operator is reached from its kernel. The solution splits into components, one per term of the operator, and each term has its own natural function class. The approach must be analytic, not machine learning: no learned weights, and the result must be exact, not a model.
This plan covers the preparatory work. That means installing skills (including doc2math and Mathpix), then Phase 1 research, Phase 2 skill-building and session design, Phase 3 the linear problems, Phase 4 nonlinearity, and Phase 5 integration and Lean formalisation.
**Out of scope until Phase 5 is done:** Problema 1 (variable potential V as noise, Schrödinger and Dirac), Problema 2 (matrix coefficients, Dirac 4×4), and Idea I (t-SNE, autoencoder, GMM preprocessing). Phase 1 may read about them but nothing gets built for them.

## Decisions (from the user)
- **Project folder:** the user picks it with `request_directory` as the very first action. The session moves there before anything else is written.
- **Cross-model review:** Claude-only, no Codex. proof-checker's second reviewer is an independent Claude subagent, plus `kill-argument`. Install ARIS without the Codex bridge.
- **Framing confirmed:** u ∈ ker L, L = ΣLᵢ → recover L and split u into per-term classes, with E_int as the part that does not split.
- **Feedback on plan v1:** the transcription missed notation and points, and the problem, goals, sub-goals, mathematical structure and relations were not defined. v2 **adds** sections 0A–0D and Section 1, and enriches every phase. Nothing from v1 is removed.
- **Feedback on plan v2 (rule from now on: only add, never remove a word):**
  - (1) **C1 and C2 are strictly connected: C1 is built from C2.** The Hilbert space and dictionary are made out of the kernel catalogue.
  - (2) C2's sub-goals were far too incomplete. Diffusion was only an example. The user supplied the full list C2.1–C2.60 plus a second series C2.17′–C2.76′ (structural categories). It is kept word for word in §1.3-C2-EXT and **reorganised by PDE type** in §1.3-C2-TAX.
  - (3) New point **PR-C2**: pre-research covering **all** categories.
  - (4) Extra sources: MIT OCW 18.03 (Spring 2010) and 18.303 (Fall 2006), with topic lists in §1.3-C2-SRC.

---

## 0A. Page order and reading notes
- The photos are rotated 180°. The pages form **one continuous argument**, and the order is fixed by the sentences that run on from one page to the next:
  **Pg.A** (④, the basis) → **Pg.B** (P1, P2) → **Pg.C** (P3, P4, Idea I) → **Pg.D** (marked ③; Idea II) → **Pg.E** (the two paths) → **Pg.F** (spectral form) → **Pg.G** (proposed process) → **Pg.H** (index / numbering scheme).
- Legend: `[?]` uncertain reading; `[barrato: …]` crossed-out text (kept, because it shows intent); `[≈ …]` my normalisation.
- In the photos, only component **④** is explicitly circled at the start of a component. ①–③ come from the index (Pg.H) and the user's message. The mapping in Section 1.3 is **to be confirmed at Gate 0**.

## 0B. Verbatim transcription (original Italian, every symbol kept, every point numbered)
**Pg.A**
- A1 ④ Voglio eliminare il rumore su f̂ — utilizzo [termine del?] machine learning: REGOLARIZZATO
- A2 f̂ := Σ ω_n e_n
- A3 non posso usare base qualsiasi sennò includo il rumore
- A4 • NO POLINOMI LEGENDRE • NO POL. FOURIER
- A5 {e_n} appropriata: {e_n} = Σ CLASSI DI FUNZIONI CHE RISOLVONO EQ. DIFF. [DELLE] LORO COMP[ONENTI]
- A6 (P) ∃ funzioni legate [alla] comp[onente] diffusiva? [riquadro: ∂/∂t] ∃ f[unzioni] legate ind[ividualmente] a ogni operatore? ANCHE NON LINEARE: V·d/dx V ⟺ {e^n_i}_{i∈ℕ}
- A7 Devono essere basi numerabili?
- A8 Vale che se â = Σ a_n ⟺ f̂ = Σ_n Σ_i e_{n,i}. Così da analizzare [le] componenti individualmente.
- A9 [barrato: Problemi] Potenziali soluzioni. Hp: trovo le {e_{n,i}}, f[unzioni] legate a un partic[olare] operatore. Immagino â = â₁ + â₂ ⇒ **f̂ := e_{n1} + e_{n2} + E_int** (E_int sottolineato due volte)

**Pg.B**
- B1 [barrato: Sotto ipotesi] questo è vero di certo. Se poi E_int ≈ 0 bene, sennò vediamo.
- B2 (P1) posso trovare E_int ≈ h(e₁, e₂)?? Se posso, come costruisco la Matrice di funzioni E con algoritmo risolvibile ≠ O(eⁿ)?
- B3 Se trovo [che l']algoritmo [è] NON risolvibile (come prob[abilmente] è) tento soluzione locale ↳ COME SI FA CON "GRADUATION MIXTURE MODE[L]" [? ≈ Gaussian / graduated mixture model]
- B4 Solo per dare [l']idea di possibile soluzione locale: **L'ALGORITMO NON DEVE ESSERE UN MODELLO MA ESATTO.**
- B5 (P2) Regolarizzare vuol dire fare Hp su [la] serie [di] Fourier [≈ prior sui coefficienti]. ℒ_G = ℒ + ‖ω‖² ⇒ f_i ≈ e^{−(λ−λ₀)²/σ²}·N, gaussiana.
- B6 ℒ_ALT = ℒ + Σ|ω| ⇒ f_i ≈ Σ ω_n e_n, n piccolo [≈ sparso]
- B7 Ci sono altre regolarizzazioni possibili; forse è meglio ℒ_ALT.
- B8 ↳ Si può dimostrare che ℒ_ALT elimina E_int?? Se non lo elimina va ben[e lo stesso?]

**Pg.C**
- C1 Ci sono regolarizzazioni che lo eliminano?
- C2 (P3) Se non posso eliminarlo posso identificarlo. Idee: lavorare [con] un sistema [di] perturbazioni tempo-dipendenti, come si fa per [l']interazione radiazione–materia tempo-dipendente ⇒ lavorare con i duali: e^†_{n,i}·E_int, ⟨e_{n,i}|E_int⟩ = ? magari scopro qualcosa.
- C3 (P4) posso costruire Â [o Â⁻¹?] t.c. Â⁻¹ [è] identificato ∧ [?] Â⁻¹{e_{n,i}}_{n,i∈ℕ} è identificato?
- C4 ALTRE IDEE (I): l'algoritmo può essere migliorato preparando i dati. Es. T-SNE ∨ AUTOENCODER o simili per ottenere una separazione naturale. Si può poi usare un algoritmo di grouping come GMM.
- C5 NOTA!! Questo non vuol dire che devo [arrivare?] a raggruppare i dati e conoscere le componenti; vorrei che l'algoritmo funzionasse a prescindere da questo passo.

**Pg.D (③)**
- D1 Se proprio non si riesce, si può dimostrare che ENCODING + GROUPING ⇒ E_int → 0
- D2 (II) Trattare tutte [le] E.D.P. come MATRICI, CON J_φ op[eratore] diff[erenziale]: ∂/∂x_i ⊗ ∂/∂x_j =: J_φ; "J_φ·Φ = 0" [scritto ≈ Φ̂_φ·Φ = 0], idea di base.
- D3 2 opzioni: • Usare tensori di II ordine o superiori: J_{ω,λ} = λ ⊗ J_φ, dove λ sono i coefficienti degli operatori, assumendo che siano moltiplicazioni. Da qua si aprono 2 strade:
- D4 • (a) Aumentare [l']ordine [del] tensore per eq. diff. [di] ordine superiore: J_φ = ∂/∂x_i ⊗ ∂/∂x_j ⊗ … ⊗ ∂/∂x_k; J^n_φ : n = #⊗. [barrato: oppure] PRO: tensore quadrato, cubico…
- D5 • (b) Aumentare [il] numero di righe e fare come si fa per [le] ODE: Ẋ = AX [con ∂/∂t], A = [[0 1 …],[0 0 1 …],[riga eq. diff.]] ↳ riga eq. diff.

**Pg.E**
- E1 Da questa scende [l']opzione [a] 2 strade (P): • usare [l']ultima riga come riga che descrive [l']eq. diff. ↳ **NON È UNA MATRICE**: [[0 1 …],[… 1],[f₁(x) f₂(x) …]]
- E2 oppure fare una base di generatori [?]: â = f(J_φ·Φ), dove nelle info di Φ sono contenute le info [della] soluzione [dell']eq. diff. [che] si linearizza [?]
- E3 VALE SIA PER • â = f(J_φ·Φ) ↳ con J_φ ∈ Mat M×N con [la] costruzione appena su; • â = f(J_ω·Φ) con **J_ω ∈ 𝒴ⁿ [? ≈ 𝒯ⁿ], TENSORE ORDINE N**
- E4 Domanda: **quale costruzione fornisce più invarianti per [l']ordine del sistema?** ⇒ J costruzione migliore.
- E5 Nota: se â = f(J_ω·Φ) ⇒ J_ω = Σ D V [? ≈ U·D·V, decomposizione SVD/HOSVD] in un opportuno spazio ridotto su cui ci si può spostare per lavorare.

**Pg.F**
- F1 **â = Σ_a f(λ_a) v_a ⊗ v_a**
- F2 dove V_a = {v | J_ω·Φ v = a v}, o [il] concetto [di] autovettore generalizzato per tensori [di] ordine superiore.
- F3 Dici che la soluzione [è] â = f(J_ω·Φ)? [barrato: …] Forse è meglio: sia J_ω ∈ 𝒴_n o J_ω ∈ Mat m×n con la struttura [[0 1 …],[0 0 …],[… 1]].
- F4 Così: • evidenzio [la] struttura geometrica; • posso lavorare su f e Φ indipendentemente.
- F5 IDEA • Se riesco a risolvere il problema fondamentale di Â SOLO per eq. lineari, poi posso lavorare su f in una fase successiva (è qualcosa).
- F6 • Se rompo il sistema posso lavorare su ogni direzione scalarmente, studiando f(λ), e poi unire dopo i pezzi.

**Pg.G**
- G1 DIREI CHE UN BUON PROCESSO PUÒ ESSERE:
- G2 – Risolvo tutto per coeff[icienti] scalari lineari.
- G3 – Vedo se riesco a includere anche coeff. non lineari, e risolvo così il problema delle basi prendendo in considerazione operatori non lineari
- G4 ↳ Se non riesco, studio le f(S·x) [? S ≈ J] con f non lineare ↳ ancora scalari o vettoriali.
- G5 Cercando di capire come f ⟺ {e_{n,i}}, come e_{n,i} diventa ↳ base [per] classe [di] eq. lineare.
- G6 – # Per risolvere il sistema [barrato: mi basta ruotare il] mi basta studiare [lo] spazio ridotto e studiare autovettori e autovalori, prendendo la scelta: J ∈ 𝒴_n ∨ J ∈ Mat m×n. ("ruotare" = rotation; the crossed-out word links to the user's geometry and rotation intuition.)

**Pg.H (index)**
- H1 Problema 1: ∃ equazioni come Dirac e Schrödinger che hanno V̂ che varia ↳ lo tratto come **rumore**. Devo trovare un **encoder** che lo **elimini!!!** OSS: questo va oltre l'algoritmo core, VA STUDIATO SEPARATAMENTE.
- H2 Problema 2: fino ad ora [i coefficienti sono] scalari: J_λ·Φ ↳ matrice di scalari. Dirac → **λ sono Mat 4×4**. Come risolvo?? Problema molto avanzato.
- H3 IDENTIFICA OGNI PROBLEMA E IDEA E FAI IL PUNTO [DELLA] SITUAZIONE. OGNI PUNTO HA UN NUMERO. SEPARA: ①②③④ COMPONENTI · (P1)(P2)(P3)(P4) NODI DA RISOLVERE ↳ P_i · (I)(II) IDEE E SOLUZIONI · Problema 1, Problema 2: problemi avanzati, dopo.
- *(Correction from v1: in H2 the symbol is **λ** (the coefficients), not "A". This matches D3, J_{ω,λ} = λ ⊗ J_φ.)*

## 0C. English gloss (kept from v1 for readability)
- **Pg.A / ④:** remove "noise" from f̂ by a regularized expansion f̂ = Σω_n e_n. A generic basis (Legendre, Fourier) would absorb the noise, so {e_n} must be the union of the function classes that solve the equation of each component. The open questions are whether there are classes tied to the diffusive part, to each operator individually, and to nonlinear terms like V·V_x, and whether the bases must be countable. The claim is â = Σa_n ⟺ f̂ = ΣΣe_{n,i}. With â = â₁ + â₂, f̂ = e_{n1} + e_{n2} + E_int.
- **Pg.B:** P1 asks whether E_int ≈ h(e₁,e₂), and for an algorithm that is not O(eⁿ). If none exists, a local solution, but the algorithm must be exact. P2 compares L² regularization (Gaussian) with L¹ (sparse) and asks whether L¹ removes E_int.
- **Pg.C:** P3 says that if E_int can't be removed, it should be identified with time-dependent perturbation theory and duals ⟨e_{n,i}|E_int⟩. P4 asks for an inverse Â⁻¹ that identifies Â from {e_{n,i}}. Idea I is preprocessing; the algorithm must not depend on it.
- **Pg.D–G:** Idea II writes PDEs as matrices or tensors built from derivative tensors and coefficients. Path (a) uses higher-order tensors; path (b) uses companion rows, where the last row holds f_k(x) so it is "not a matrix". The spectral form is â = Σ f(λ_a) v_a⊗v_a, and the question is which construction keeps more invariants. Then a reduced space, solving the linear case first, splitting into scalar directions, and the process: scalar linear → nonlinear coefficients → f(S·x).
- **Pg.H:** the numbering scheme, plus Problema 1 and 2 postponed.

## 0D. doc2math Mathematical Problem Specification (draft, produced now; regenerated with the installed skill in Step 0)
This applies the doc2math rules. Every element cites a point ID, unknowns are `null`, inferences carry `inferred:true` and their basis, and no equation is added that is not in the source; derived equations live only in Section 1, marked as inferred.
```json
{"mps_version":"1.0","source_title":"Appunti – algoritmo/processo identificazione operatori","problem_class":"proof",
 "variables":[
  {"id":"v1","name":"dato/soluzione","symbol":"f̂","type":"function","domain":null,"role":"input","evidence":"A1,A2","inferred":false,"status":"PARTIAL (dominio e spazio non dati)"},
  {"id":"v2","name":"coefficienti di espansione","symbol":"ω_n","type":"real/complex sequence","domain":null,"role":"decision","evidence":"A2,B5,B6","inferred":false},
  {"id":"v3","name":"base/funzioni per componente","symbol":"e_n, e_{n,i}","type":"functions","domain":"n,i∈ℕ (A6,C3)","role":"decision/latent","evidence":"A5,A8,A9","inferred":false},
  {"id":"v4","name":"termine di interazione","symbol":"E_int","type":"function","role":"residual/target","evidence":"A9,B1,B2,C2","inferred":false},
  {"id":"v5","name":"coefficienti dell'operatore","symbol":"λ (scalari; Mat 4×4 in Dirac)","type":"scalars→matrices","role":"unknown","evidence":"D3,H2","inferred":false},
  {"id":"v6","name":"vettore/oggetto soluzione","symbol":"Φ","type":"ambiguous","role":"input","evidence":"D2,E2","inferred":true,"inference_basis":"E2: 'nelle info di Φ sono contenute le info della soluzione' ⇒ Φ = jet/vettore di derivate di f"},
  {"id":"v7","name":"autovalori/autovettori","symbol":"λ_a, v_a, V_a","type":"spectral data","evidence":"F1,F2","inferred":false}],
 "operators":[
  {"id":"o1","name":"operatore incognito","symbol":"â / Â","arity":1,"acts_on":"funzioni","produces":"funzioni","evidence":"A8,A9,C3,F5"},
  {"id":"o2","name":"componenti","symbol":"â = Σ a_n, â = â₁+â₂","evidence":"A8,A9"},
  {"id":"o3","name":"tensore di derivate","symbol":"J_φ = ∂/∂x_i⊗∂/∂x_j(⊗…), J^n_φ","evidence":"D2,D4"},
  {"id":"o4","name":"tensore coefficienti⊗derivate","symbol":"J_{ω,λ} = λ⊗J_φ; J_ω ∈ 𝒴ⁿ","evidence":"D3,E3"},
  {"id":"o5","name":"matrice compagna / righe aggiunte","symbol":"A (Ẋ=AX), ultima riga f_k(x)","evidence":"D5,E1,F3"},
  {"id":"o6","name":"calcolo funzionale","symbol":"â = f(J·Φ) = Σ_a f(λ_a) v_a⊗v_a","evidence":"E2,E3,F1"},
  {"id":"o7","name":"inverso identificante","symbol":"Â⁻¹","evidence":"C3"},
  {"id":"o8","name":"duale","symbol":"e^†_{n,i}, ⟨e_{n,i}|·⟩","evidence":"C2"}],
 "constraints":[
  {"id":"k1","type":"equality","expression":"J_φ·Φ = 0","evidence":"D2","hardness":"hard"},
  {"id":"k2","type":"structural","expression":"base ≠ Legendre, ≠ Fourier; base = classi che risolvono le eq. delle componenti","evidence":"A4,A5","hardness":"hard"},
  {"id":"k3","type":"method","expression":"algoritmo esatto, non modello; nessun ML/pesi","evidence":"B4 + messaggio utente","hardness":"hard"},
  {"id":"k4","type":"complexity","expression":"≠ O(eⁿ)","evidence":"B2","hardness":"soft"},
  {"id":"k5","type":"scope","expression":"lineare, scalare, 1D, senza rumore, non-sistema (prima)","evidence":"G2,F5 + messaggio utente","hardness":"hard"},
  {"id":"k6","type":"independence","expression":"funzionare senza preprocessing (I)","evidence":"C5","hardness":"hard"}],
 "objectives":[
  {"id":"g1","direction":"find","expression":"{e_{n,i}} legate a ogni operatore","evidence":"A6,A9"},
  {"id":"g2","direction":"prove","expression":"â = Σ a_n ⟺ f̂ = Σ_n Σ_i e_{n,i}","evidence":"A8"},
  {"id":"g3","direction":"find","expression":"E_int ≈ h(e₁,e₂)","evidence":"B2"},
  {"id":"g4","direction":"prove","expression":"ℒ_ALT elimina E_int?","evidence":"B8"},
  {"id":"g5","direction":"find","expression":"identificare E_int via ⟨e_{n,i}|E_int⟩","evidence":"C2"},
  {"id":"g6","direction":"find","expression":"Â⁻¹ identificante","evidence":"C3"},
  {"id":"g7","direction":"find","expression":"costruzione J con più invarianti","evidence":"E4"},
  {"id":"g8","direction":"prove","expression":"ENCODING+GROUPING ⇒ E_int→0 (fallback)","evidence":"D1"}],
 "uncertainty":[{"id":"u1","type":"none_stated","affects":"v1","characterization":"'rumore' = E_int / parti non spiegate (A1,H1), non rumore stocastico","evidence":"A1,H1, utente 'without noise'"}],
 "missing_information":[
  {"element":"dominio Ω, variabili (t,x)?, condizioni al bordo/iniziali","needed_for":"spazio di Hilbert, unicità","missing_reason":"non scritto"},
  {"element":"spazio funzionale di f̂","needed_for":"C1,P2","missing_reason":"non scritto"},
  {"element":"definizione di E_int","needed_for":"P1–P3","missing_reason":"solo per uso (A9)"},
  {"element":"significato di 'componente' (termine singolo vs sotto-equazione)","needed_for":"C2,C4","missing_reason":"A6 ambiguo"},
  {"element":"definizione di 𝒴ⁿ, 'Σ D V', S in f(S·x)","needed_for":"II","missing_reason":"grafia"},
  {"element":"quanti dati: una soluzione o una famiglia","needed_for":"P4 identificabilità","missing_reason":"non scritto"}],
 "validation_flags":{"has_complete_objectives":"partial","has_bounded_variables":false,"has_evidence_for_all_elements":true,"inference_count":1,"missing_count":6,"overall_formalizability":"MEDIUM"}}
```

---

## 1. Precise problem definition (my mathematical reconstruction; every item is a **claim to verify**, not a result)

### 1.1 Setting (fills the MISSING items as working hypotheses H0–H4, revisable at Gate 0/1)
- **H0 (domain):** u = u(t,x) on Ω = I×ℝ or I×𝕋 (1 space dimension plus time). The ODE case u = u(x) is the warm-up.
- **H1 (space):** u ∈ 𝓗, a Hilbert space (L², Sobolev H^k, or a weighted/analytic space to be chosen by C1). Distributions are allowed for kernels.
- **H2 (operator):** L = Σ_{k=1}^{N} λ_k ∂^{α_k} with α_k multi-indices in (∂_t, ∂_x). The λ_k are scalars in the base case (G2) and functions f_k(x) in the variable case (E1).
- **H3 (data):** one exact solution f̂ = u with Lu = 0 (k5). There is no stochastic noise. The "noise" of A1/H1 means the part E_int that the chosen basis does not explain.
- **H4 (jet):** Φ(u) := (∂^{α_1}u, …, ∂^{α_M}u)ᵀ is the jet vector over a candidate dictionary of M derivatives. Then **J_φ·Φ = 0** (D2) reads λ·Φ(u)(t,x) = 0 for every (t,x).

### 1.2 The main goal (G★)
> **G★ (Teorema base).** In the linear, scalar, 1D, noise-free case, find an **exact and analytic** procedure 𝓘 : u ↦ (L, {u_n}) that from one solution u
> (i) recovers L, i.e. its coefficients λ, up to the stated non-uniqueness, and
> (ii) splits u into per-component parts u_n, written in the natural function classes {e_{n,i}} of each component, plus an explicitly characterised remainder E_int.
> The proof must state when (i) is unique (identifiability), when E_int = 0, and how E_int is computed otherwise, with complexity below O(eⁿ).

Three analytic facts shape how G★ is stated (all to be verified in Phase 1/3):
1. **"An operator that goes from a kernel"** (the user's unusual functional-analysis object). The coefficient vector satisfies λ ∈ ker 𝔾(u), where 𝔾(u) := ∫_Ω Φ(u) Φ(u)ᵀ is the Gram matrix of the jet. Identification is a **kernel problem for 𝔾**, and uniqueness ⟺ dim ker 𝔾 = 1. Algebraically, the set of all annihilators Ann(u) = {P : P(∂)u = 0} is an ideal (or a left ideal of the Weyl algebra if coefficients vary). 𝓘 must return its generator(s).
2. **Sums vs products (the core of E_int).**
   - (a) If P = P₁·P₂ with coprime factors, then ker P = ker P₁ ⊕ ker P₂. This is an **additive** split with no E_int (Bezout for ODEs; Ehrenpreis–Palamodov/Malgrange injectivity for PDEs).
   - (b) If L = L₁ + L₂ (a **sum of terms**, as in A8/A9) and the evolution is u_t = (L₁+L₂)u, then u = e^{t(L₁+L₂)}u₀. This equals e^{tL₁}e^{tL₂}u₀ iff the terms commute. The split is **multiplicative** (convolution of kernels), and in the additive picture E_int = (K₁−δ)∗(K₂−δ)∗u₀ ≠ 0, which is bilinear, so an h(e₁,e₂) as in P1 exists. With N terms the additive expansion has 2ᴺ terms: this is the O(eⁿ) of B2. In the Fourier/symbol (log) domain the split is **additive and linear**: log û(t,ξ) = log û₀ + t Σ p_n(ξ).
   - (c) If the terms do **not** commute (variable coefficients), E_int is built from commutators [L_i, L_j] through BCH/Zassenhaus/Dyson. This is exactly the interaction picture of P3.
3. **Idea II is the symbol / functional calculus.** â = Σ_a f(λ_a) v_a⊗v_a (F1) is the spectral theorem: v_a are Fourier modes for constant coefficients and λ_a = p(iξ) is the symbol. The order-n tensor J^n_φ (path a) corresponds to the **principal symbol as a symmetric n-tensor**. The companion matrix (path b) is the first-order reduction. Its similarity invariants equal the characteristic polynomial, i.e. the operator itself, and its Jordan blocks give the xᵏe^{λx} kernel classes. "Rompo il sistema, lavoro per direzione" (F6) means joint diagonalisation, which is possible iff the parts commute or are normal. "ENCODING + GROUPING ⇒ E_int → 0" (D1) has an analytic candidate: the encoder is the spectral transform (Fourier/Laplace/log-symbol), with no weights.

### 1.3 Item dictionary — precise statement, goal, sub-goals, deliverable, done-criterion
(The C-item mapping uses Pg.H plus the user's message. It is confirmed at Gate 0.)

**C1 — Representation space (Hilbert space ↔ analytic ML).** *Source: A1–A3, B5–B6; user: "component 1 = Hilbert spaces + ML, analytically".*
- **Statement:** choose 𝓗 and a regularised representation f̂ = Σω_n e_n as the exact minimiser of ‖f − Σω_n e_n‖² + αR(ω) (with α→0 in the noise-free case), using a representer theorem/RKHS view.
- **Goal:** a space in which the dictionary ⋃_n{e_{n,i}} is a frame or Riesz basis of the solution set, so that the coefficients are unique and computable in closed form.
- **Sub-goals:**
  - C1.1 Candidate spaces: L², H^k, RKHS with kernel K(x,y) = Σ e_{n,i}(x)e_{n,i}(y), analytic/Bargmann.
  - C1.2 Representer theorem → closed-form ω (Gram inverse).
  - C1.3 Conditions for completeness, minimality and Riesz property (answers A7, countability).
  - C1.4 Dual/biorthogonal system e^†_{n,i}, which feeds P3.
- **Deliverable:** `work/C1/PROOF_PACKAGE.md`, defining the space and proving existence, uniqueness and a closed form.
- **Done when:** proof-checker passes and SymPy verifies the closed form on the heat and Airy examples.
- **C1 ⇐ C2 (strict coupling, user v3).** C1 is not chosen independently: it is **built from C2**.
  - The dictionary is 𝒟 := ⋃_n {e_{n,i}} taken from the C2 catalogue.
  - The space is 𝓗_𝒟 := closure of span 𝒟 under the norm induced by the Gram operator G_{(n,i),(m,j)} = ⟨e_{n,i}, e_{m,j}⟩. Equivalently, it is the RKHS with kernel K(x,y) = Σ e_{n,i}(x) e_{n,i}(y), or the continuous-frame version ∫_{V(P)} e^{⟨z,·⟩}… dμ(z) when a class is not countable (A7).
  - Each C2 entry must therefore deliver, besides its kernel class, the data C1 needs: inner products and Gram blocks between classes, a dual/biorthogonal system, and a countable-vs-continuous index set.
  - New sub-goal **C1.0**: define the construction functor C2-catalogue → (𝓗_𝒟, G, K, dual system), and prove it is well defined: positivity, completeness and Riesz bounds as functions of the inter-class coherence.
  - **Sessions S-C1 and S-C2/C4 run as one coupled pair** in Phase 3, sharing a Gram-matrix file `work/C1C2/gram.md`.

**C2 — Kernel classes of each operator term.** *Source: A5, A6, A9; user: "component 2: operator kernels, each PDE term → function class (diffusion, divergence, third derivative, Bessel)".*
- **Statement:** for each elementary term or sub-equation T_n, characterise K_n = ker T_n (or its solution class) and give a basis {e_{n,i}}.
- **Goal:** a verified **catalogue** mapping operator term → kernel class → closure properties → spectral data.
- **Sub-goals:**
  - C2.1 ODE constant coefficients: xᵏe^{λx}.
  - C2.2 Transport ∂_t + c∂_x: g(x−ct).
  - C2.3 Diffusion ∂_t − D∂_xx: heat kernel, Gaussians, Hermite functions (links to B5's Gaussian).
  - C2.4 Dispersion ∂_t + ∂_xxx: Airy.
  - C2.5 Reaction: exponentials.
  - C2.6 Polynomial coefficients: holonomic classes (Bessel, Legendre, hypergeometric) and why they come from symmetry and separation of variables.
  - C2.7 Nonlinear term V·V_x, *brief*: Cole–Hopf → heat.
- **Deliverable:** `work/C2/CATALOG.md`, one `kernel-catalog-entry` per term.
- **Done when:** every entry has a SymPy check that T_n e = 0 and a textbook citation.
- *(The v2 sub-goals C2.1–C2.7 above are kept as the "core-ladder" subset. The user's full list below supersedes their numbering. Where labels collide, the v2 draft labels are read as C2.1ᵈ–C2.7ᵈ.)*

#### §1.3-C2-EXT — C2 extended sub-goals (user v3, verbatim; second series marked ′ because its numbers repeat)
**Series 1 (families and methods)**
C2.1 Constant-coefficient ODEs: characteristic polynomials, distinct roots, repeated roots, complex roots, exponential-polynomial solutions x^k e^(lambda x), fundamental solution sets.
C2.2 Forced ODEs and linear systems: undetermined coefficients, resonance, variation of parameters, Green's functions, matrix exponentials, Jordan canonical forms, fundamental matrices.
C2.3 First-order ODEs: separable, linear, exact, integrating factors, homogeneous, Bernoulli, Riccati, Clairaut, Lagrange, autonomous equations, phase lines, equilibria, stability.
C2.4 Variable-coefficient ODEs: Euler-Cauchy, Frobenius method, regular and irregular singular points, reduction of order, power series, asymptotic solutions.
C2.5 Special-function ODEs: Bessel, Legendre, associated Legendre, Hermite, Laguerre, hypergeometric, confluent hypergeometric, Airy, Chebyshev, Gegenbauer, Jacobi, spheroidal equations.
C2.6 Transport equations: linear advection, characteristics, characteristic curves, g(x-ct), variable-speed transport, nonlinear transport, transport with sources.
C2.7 Diffusion equations: heat equation, heat kernel, Gaussian fundamental solutions, Fourier modes, Hermite functions, anisotropic diffusion, variable diffusivity, nonlinear diffusion.
C2.8 Wave equations: d'Alembert solutions, wave propagation, standing waves, eigenmodes, vibrating strings and membranes, forced waves, wave equations in higher dimensions.
C2.9 Elliptic equations: Laplace, Poisson, harmonic functions, mean-value property, maximum principles, Green's functions, Dirichlet and Neumann problems.
C2.10 Dispersive equations: Airy equation and Airy profiles, Fourier integrals, dispersion relations, group velocity, stationary phase, Schrödinger propagators, dispersive estimates.
C2.11 Reaction and growth equations: exponential modes, logistic growth, Fisher-KPP equation, equilibria, linear stability, reaction-diffusion systems, Turing instability.
C2.12 Advection-diffusion and damped waves: convection-diffusion, drift-diffusion, telegraph equation, damped wave equation, viscous transport, competing transport and diffusion.
C2.13 Separation of variables and spectral theory: Sturm-Liouville problems, eigenvalues, eigenfunctions, boundary conditions, orthogonal expansions, completeness, spectral decompositions.
C2.14 Integral transforms: Fourier transform, Fourier series, Laplace transform, inverse transforms, convolution, Green's-function methods, transform methods for initial and boundary data.
C2.15 Nonlinear PDEs: nonlinear characteristics, quasilinear equations, shocks, rarefaction waves, traveling waves, entropy solutions, Burgers equation, Cole-Hopf transformation.
C2.16 Integrable and asymptotic structures: solitons, inverse scattering transform, perturbation theory, boundary layers, multiple scales, WKB, similarity solutions, matched asymptotic expansions.
C2.17 PDE classification and canonical forms: order, linearity, semilinear, quasilinear and fully nonlinear equations, principal symbol, elliptic, hyperbolic, parabolic, ultrahyperbolic, mixed-type and degenerate equations.
C2.18 General first-order PDEs: Hamilton-Jacobi equations, Lagrange's linear PDE, Charpit's method, complete integrals, envelopes, characteristic initial-value problems, eikonal equations.
C2.19 Higher-order linear PDEs: biharmonic equations, polyharmonic equations, higher-order evolution equations, constant-coefficient operators, factorization, fundamental solutions.
C2.20 Elliptic boundary-value problems: Dirichlet, Neumann, Robin and mixed boundary conditions, exterior-domain problems, uniqueness, maximum principles, elliptic regularity.
C2.21 Parabolic PDEs: classical heat flow, anisotropic heat equations, variable-coefficient diffusion, degenerate parabolic equations, fundamental solutions, smoothing and maximum principles.
C2.22 Hyperbolic PDEs and systems: wave propagation, characteristic cones, domains of dependence, domains of influence, finite propagation speed, hyperbolic systems, energy estimates.
C2.23 Mixed-type PDEs: Tricomi equation, Keldysh equation, transonic flow, changes of type, elliptic-hyperbolic interfaces, mixed-type boundary-value problems.
C2.24 Conservation laws: scalar conservation laws, systems of conservation laws, flux functions, Rankine-Hugoniot conditions, entropy conditions, weak solutions, shock formation.
C2.25 Hamilton-Jacobi and eikonal equations: value functions, optimal-control PDEs, viscosity solutions, action functions, geometric optics, caustics, front propagation.
C2.26 Compressible fluid equations: Euler equations, compressible Navier-Stokes equations, continuity equation, momentum conservation, energy conservation, acoustic waves, gas dynamics.
C2.27 Incompressible fluid equations: incompressible Euler equations, incompressible Navier-Stokes equations, pressure Poisson equation, vorticity equations, stream functions, boundary layers.
C2.28 Shallow-water and geophysical flow: shallow-water equations, Saint-Venant equations, rotating fluids, Coriolis effects, Rossby waves, potential vorticity, atmospheric and oceanic transport.
C2.29 Electromagnetic PDEs: Maxwell equations, electromagnetic wave equation, electrostatics, magnetostatics, Helmholtz equation, electromagnetic potentials, gauge conditions, boundary conditions.
C2.30 Quantum PDEs: time-dependent Schrödinger equation, stationary Schrödinger equation, free-particle propagator, quantum scattering, nonlinear Schrödinger equation, semiclassical limits.
C2.31 Relativistic wave equations: d'Alembertian, Klein-Gordon equation, Dirac equation, wave equations on curved spacetime, characteristic cones, hyperbolic initial-value problems.
C2.32 Elasticity and solid mechanics: linear elasticity, Navier-Cauchy equations, elastodynamics, stress-strain relations, elastic waves, plate equations, beam equations, shell equations.
C2.33 Plate, beam and structural PDEs: Euler-Bernoulli beam, Timoshenko beam, Kirchhoff-Love plate, von Karman plate equations, bending waves, vibration modes, structural stability.
C2.34 Potential flow and harmonic analysis: Laplace equation, harmonic conjugates, complex potentials, Poisson integral formula, boundary integral methods, multipole expansions.
C2.35 Helmholtz and eigenvalue equations: Helmholtz equation, modified Helmholtz equation, Helmholtz decomposition, resonances, scattering, eigenfrequency problems, radiation conditions.
C2.36 Green's functions and fundamental solutions: causal Green's functions, retarded and advanced solutions, fundamental solutions, resolvent kernels, layer potentials, boundary integral equations.
C2.37 Integral and nonlocal PDEs: fractional Laplacian, fractional diffusion, fractional wave equations, nonlocal diffusion, integro-differential equations, convolution operators, memory kernels.
C2.38 Fractional differential equations: Caputo derivatives, Riemann-Liouville derivatives, time-fractional diffusion, space-fractional diffusion, anomalous transport, fractional evolution equations.
C2.39 Nonlinear diffusion and porous media: porous medium equation, fast diffusion equation, p-Laplacian evolution, nonlinear heat flow, finite-speed propagation, free boundaries.
C2.40 Kinetic equations: Boltzmann equation, BGK models, Vlasov equation, Fokker-Planck equation, Liouville equation, phase-space transport, collision operators.
C2.41 Probability and stochastic PDEs: stochastic heat equation, stochastic wave equation, stochastic reaction-diffusion, space-time white noise, Itô and Stratonovich formulations, Feynman-Kac representations.
C2.42 Pattern formation and biological PDEs: reaction-diffusion systems, Turing patterns, Fisher-KPP fronts, Gray-Scott models, chemotaxis, Keller-Segel equations, population dispersal.
C2.43 Free-boundary and moving-interface problems: Stefan problem, melting and solidification, moving boundary conditions, phase-change fronts, Hele-Shaw flow, interface tracking.
C2.44 Traveling waves and coherent structures: traveling-wave reduction, heteroclinic and homoclinic orbits, solitary waves, pulses, fronts, wave trains, stability of traveling waves.
C2.45 Integrable nonlinear PDEs: Korteweg-de Vries equation, modified KdV, nonlinear Schrödinger equation, sine-Gordon equation, Toda-type systems, Lax pairs, inverse scattering.
C2.46 Nonlinear dispersive wave equations: KdV, generalized KdV, Benjamin-Ono, nonlinear Schrödinger, Davey-Stewartson, Kadomtsev-Petviashvili, water-wave models.
C2.47 Blow-up, singularity formation and regularity: finite-time blow-up, self-similar singularities, critical exponents, continuation criteria, regularity, weak-strong uniqueness.
C2.48 Perturbation and asymptotic analysis: regular perturbations, singular perturbations, matched asymptotics, boundary layers, multiple-scale analysis, WKB, averaging, homogenization.
C2.49 Similarity and scaling methods: dimensional analysis, scaling symmetries, self-similar variables, first and second-kind similarity solutions, invariant reductions, dimensional reduction.
C2.50 Symmetry and Lie-group methods: Lie point symmetries, infinitesimal generators, symmetry reductions, invariants, conservation laws from symmetries, Noether-type methods.
C2.51 Variational and weak formulations: Euler-Lagrange equations, energy functionals, weak solutions, test functions, distributional derivatives, variational principles, direct methods in the calculus of variations.
C2.52 Sobolev spaces and distribution theory: distributions, weak derivatives, Sobolev spaces, trace theorems, embedding theorems, compactness, dual spaces, regularity.
C2.53 Functional analysis and evolution equations: semigroups, generators, resolvents, abstract Cauchy problems, dissipative operators, spectral theory, maximal regularity.
C2.54 Well-posedness and energy methods: existence, uniqueness, continuous dependence, energy estimates, a priori bounds, Gronwall inequalities, stability, continuation of solutions.
C2.55 Boundary and initial-boundary conditions: Dirichlet, Neumann, Robin, periodic, absorbing, reflecting, radiation, impedance, inflow-outflow, initial compatibility conditions.
C2.56 Coordinate systems and geometric PDEs: Cartesian, polar, cylindrical and spherical coordinates, Laplace-Beltrami operator, manifolds, covariant derivatives, curvature-dependent equations.
C2.57 PDEs on graphs and networks: diffusion on metric graphs, network wave equations, vertex coupling conditions, transport on networks, graph Laplacians, discrete-continuum models.
C2.58 Numerical PDE methods: finite differences, finite elements, finite volumes, spectral methods, discontinuous Galerkin, method of lines, adaptive meshes, stability and convergence.
C2.59 Computational fluid dynamics and numerical conservation laws: upwind schemes, Godunov methods, Riemann solvers, shock-capturing methods, flux limiters, CFL conditions, entropy-stable schemes.
C2.60 Inverse problems and parameter identification: inverse elliptic problems, inverse heat conduction, inverse scattering, coefficient recovery, data assimilation, parameter estimation, PDE-constrained optimization, adjoint equations.

**Series 2 (structural categories; original numbers C2.17–C2.76, written here with ′)**
C2.17′ PDE order and derivative structure: first-order, second-order, higher-order, mixed derivatives, multi-index notation, principal and lower-order terms.
C2.18′ Linearity and nonlinear structure: linear, semilinear, quasilinear, fully nonlinear, homogeneous, inhomogeneous, affine, coupled nonlinearities.
C2.19′ Principal symbols and operator classification: principal symbol, characteristic polynomial, ellipticity, hyperbolicity, parabolicity, degeneracy, mixed type.
C2.20′ Differential operators: gradient, divergence, curl, Laplacian, Hessian, directional derivatives, higher-order differential operators, operator composition.
C2.21′ Coefficient structures: constant coefficients, variable coefficients, smooth coefficients, rough coefficients, anisotropic coefficients, singular coefficients, periodic coefficients.
C2.22′ Scalar and system formulations: scalar PDEs, vector-valued PDEs, coupled systems, first-order systems, second-order systems, diagonalization, symmetrization.
C2.23′ Independent and dependent variables: spatial variables, time variables, multiple time scales, vector-valued unknowns, tensor-valued unknowns, parameter-dependent solutions.
C2.24′ Domain geometry and topology: bounded domains, unbounded domains, exterior domains, disconnected domains, periodic domains, manifolds, corners, edges, geometric singularities.
C2.25′ Initial-value formulations: initial data, initial surfaces, initial velocity, compatibility conditions, Cauchy data, propagation of initial information.
C2.26′ Boundary-condition structures: Dirichlet, Neumann, Robin, mixed, periodic, transmission, impedance, absorbing, inflow, outflow, radiation conditions.
C2.27′ Boundary-value problem classifications: elliptic boundary-value problems, evolution boundary-value problems, initial-boundary-value problems, exterior problems, overdetermined problems, underdetermined problems.
C2.28′ Characteristic geometry: characteristic curves, characteristic surfaces, bicharacteristics, characteristic cones, characteristic directions, characteristic roots, characteristic boundaries.
C2.29′ Causality and propagation: domains of dependence, domains of influence, finite propagation speed, propagation of singularities, causal cones, retardation, support propagation.
C2.30′ Conservation and balance structures: conserved quantities, local conservation laws, fluxes, source terms, balance laws, divergence identities, global invariants.
C2.31′ Symmetry and invariance: translation invariance, rotational invariance, scaling invariance, Galilean invariance, Lorentz invariance, gauge invariance, reflection symmetry.
C2.32′ Dimensional and scaling structures: dimensional analysis, nondimensionalization, characteristic scales, dimensionless parameters, scaling exponents, critical scaling, similarity variables.
C2.33′ Transform and representation structures: Fourier representations, Laplace representations, integral transforms, convolution representations, spectral representations, integral equations.
C2.34′ Kernel structures: fundamental solutions, Green's kernels, heat kernels, Poisson kernels, propagator kernels, resolvent kernels, reproducing kernels.
C2.35′ Spectral structures: eigenvalues, eigenfunctions, continuous spectrum, discrete spectrum, essential spectrum, spectral measures, resolvents, spectral projections.
C2.36′ Orthogonality and completeness: orthogonal eigenfunctions, biorthogonal systems, completeness relations, generalized eigenfunctions, Fourier expansions, basis decompositions.
C2.37′ Functional spaces: Lp spaces, Sobolev spaces, Hölder spaces, Besov spaces, Triebel-Lizorkin spaces, weighted spaces, anisotropic spaces, spaces of distributions.
C2.38′ Solution regularity: classical regularity, weak regularity, interior regularity, boundary regularity, elliptic regularity, parabolic regularity, hypoellipticity.
C2.39′ Generalized solution concepts: classical solutions, strong solutions, weak solutions, distributional solutions, mild solutions, viscosity solutions, entropy solutions.
C2.40′ Existence and uniqueness structures: local existence, global existence, uniqueness, nonuniqueness, continuation criteria, a priori estimates, compactness arguments.
C2.41′ Well-posedness and stability: Hadamard well-posedness, continuous dependence, stability estimates, conditional stability, ill-posedness, backward evolution, sensitivity to data.
C2.42′ Energy and integral estimates: energy identities, energy inequalities, coercivity, dissipation estimates, multiplier methods, Gronwall inequalities, a priori bounds.
C2.43′ Maximum and comparison principles: weak maximum principle, strong maximum principle, comparison principles, positivity preservation, order-preserving evolution, Harnack inequalities.
C2.44′ Monotonicity and coercivity: monotone operators, maximal monotonicity, coercive operators, accretive operators, pseudomonotonicity, compactness and monotonicity methods.
C2.45′ Variational structures: action functionals, energy minimization, Euler-Lagrange structures, weak variational formulations, stationary points, constrained variations, saddle-point formulations.
C2.46′ Hamiltonian and symplectic structures: Hamiltonian PDEs, canonical variables, Poisson brackets, symplectic evolution, conserved Hamiltonians, canonical transformations.
C2.47′ Gradient-flow structures: gradient flows, energy dissipation, metric gradient flows, Wasserstein gradient flows, entropy methods, free-energy functionals.
C2.48′ Dissipative and irreversible structures: dissipative operators, entropy production, Lyapunov functionals, contraction properties, irreversible evolution, long-time decay.
C2.49′ Nonlocal and integral operators: convolution operators, singular integral operators, pseudodifferential operators, fractional operators, integral kernels, memory operators.
C2.50′ Microlocal structures: wavefront sets, singular supports, pseudodifferential calculus, Fourier integral operators, propagation of singularities, microlocal ellipticity.
C2.51′ Geometric differential structures: differential forms, exterior derivatives, pullbacks, covariant derivatives, tensor operators, Laplace-Beltrami operators, curvature-dependent structures.
C2.52′ Coordinate and geometric representations: Cartesian coordinates, polar coordinates, cylindrical coordinates, spherical coordinates, curvilinear coordinates, coordinate transformations, moving frames.
C2.53′ Singularities and degeneracies: singular coefficients, degenerate ellipticity, degenerate parabolicity, characteristic degeneracy, caustics, blow-up singularities, removable singularities.
C2.54′ Free boundaries and interfaces: moving interfaces, free-boundary conditions, interface motion laws, jump conditions, contact lines, phase boundaries, interface regularity.
C2.55′ Transmission and coupling structures: continuity conditions, flux matching, jump relations, interface sources, domain decomposition, coupled subdomains, multiphysics coupling.
C2.56′ Stochastic structures: random coefficients, stochastic forcing, space-time noise, stochastic integrals, random fields, statistical solution concepts, moment estimates.
C2.57′ Multiscale structures: microscopic and macroscopic scales, homogenization, two-scale convergence, effective coefficients, averaging, scale separation, multiscale asymptotics.
C2.58′ Perturbative structures: regular perturbations, singular perturbations, asymptotic expansions, multiple scales, boundary-layer expansions, WKB expansions, resummation.
C2.59′ Bifurcation and stability structures: linearized operators, spectral stability, nonlinear stability, bifurcation parameters, symmetry-breaking bifurcations, instability modes, center manifolds.
C2.60′ Long-time dynamical structures: invariant sets, attractors, global attractors, invariant measures, ergodicity, asymptotic compactness, decay rates, convergence to equilibrium.
C2.61′ Traveling and coherent structures: traveling-wave coordinates, wave profiles, fronts, pulses, coherent structures, modulated waves, orbital stability, wave interactions.
C2.62′ Weak discontinuities and singular waves: shocks, contact discontinuities, rarefaction structures, jump conditions, entropy admissibility, delta-type singularities, measure-valued solutions.
C2.63′ Free-energy and entropy structures: entropy functionals, entropy fluxes, entropy inequalities, relative entropy, entropy dissipation, convex entropy pairs, entropy solutions.
C2.64′ Nonlinear interaction structures: mode coupling, nonlinear resonances, wave-wave interactions, triad interactions, energy transfer, nonlinear cascades, amplitude equations.
C2.65′ Integrability and exact-solution structures: Lax pairs, compatibility conditions, Bäcklund transformations, Darboux transformations, inverse scattering, conservation-law hierarchies.
C2.66′ Reduction and equivalence structures: symmetry reduction, similarity reduction, dimensional reduction, traveling-wave reduction, hodograph transformations, dependent-variable transformations.
C2.67′ Boundary asymptotics and singular limits: boundary layers, initial layers, corner layers, matched expansions, thin-domain limits, high-frequency limits, zero-diffusion limits.
C2.68′ Averaging and effective dynamics: temporal averaging, spatial averaging, homogenized equations, effective evolution laws, modulation equations, closure relations.
C2.69′ Inverse and identification structures: inverse operators, coefficient recovery, source identification, parameter estimation, uniqueness of recovery, observability, identifiability.
C2.70′ Control and observation structures: distributed control, boundary control, controllability, observability inequalities, stabilization, feedback operators, optimal control.
C2.71′ Data assimilation and uncertainty: observation operators, state estimation, parameter uncertainty, ensemble methods, Bayesian inversion, uncertainty propagation, model calibration.
C2.72′ Discretization structures: spatial discretization, temporal discretization, mesh structures, discrete differential operators, variational discretization, conservation-preserving discretization.
C2.73′ Numerical stability and consistency: consistency, convergence, stability, truncation error, dispersion error, numerical dissipation, stiffness, CFL constraints.
C2.74′ Numerical approximation spaces: finite-element spaces, finite-volume reconstructions, spectral bases, wavelet bases, discontinuous polynomial spaces, adaptive approximation, reduced-order spaces.
C2.75′ Computational solution structures: nonlinear solvers, iterative linear solvers, preconditioning, operator splitting, domain decomposition, multigrid, parallel algorithms, error estimation.
C2.76′ PDE model structure and closure: constitutive relations, source closures, flux closures, effective models, reduced models, coupling assumptions, admissibility constraints, mathematical model validation.

#### §1.3-C2-TAX — Reorganisation by PDE type (every item above appears exactly once; nothing dropped)
**Relevance tags for G★:**
- ★ core: linear, scalar, 1D, Phase 3.
- ◆ framework for C1/C3 (spaces, spectra, kernels).
- ▲ Phase 4 (nonlinear).
- ■ systems or matrix coefficients (Problema 2 / II generalisation).
- ● noise or stochastic (Problema 1 / out of the core).
- ◇ multi-dimensional, geometric or applied model (later generalisation via II/R7).
- ○ numerical (reference only; never the method, constraint k3).

**Axis 1 — Families of equations (what the operator is)**
- **T1 Linear ODEs:**
  - C2.1 ★ constant-coefficient
  - C2.2 ★■ forced ODEs and linear systems; feeds II path (b)
  - C2.3 ★▲ first-order (linear ★; Bernoulli/Riccati/Clairaut ▲)
  - C2.4 ★ variable-coefficient (Frobenius)
  - C2.5 ★◇ special-function ODEs
- **T2 First-order PDEs:**
  - C2.6 ★▲ transport (linear ★, nonlinear ▲)
  - C2.18 ▲ general first-order (Lagrange's linear PDE ★)
  - C2.25 ▲ Hamilton–Jacobi/eikonal
- **T3 Parabolic (diffusive):**
  - C2.7 ★▲ diffusion
  - C2.21 ★ parabolic PDEs
  - C2.39 ▲ nonlinear diffusion / porous media
- **T4 Hyperbolic (wave):**
  - C2.8 ★◇ wave
  - C2.22 ★■ hyperbolic PDEs and systems
  - C2.31 ■◇ relativistic (Klein–Gordon ★; Dirac = Problema 2)
- **T5 Elliptic:**
  - C2.9 ★◇ elliptic
  - C2.20 ★◇ elliptic BVPs
  - C2.34 ◇ potential flow / harmonic analysis
  - C2.35 ★◇ Helmholtz / eigenvalue equations
- **T6 Dispersive:**
  - C2.10 ★ dispersive (Airy)
  - C2.30 ★●▲ quantum (free Schrödinger ★; varying V = Problema 1; NLS ▲)
  - C2.46 ▲ nonlinear dispersive
- **T7 Reaction / growth:**
  - C2.11 ★▲ (linear reaction ★; logistic/Fisher–KPP ▲)
  - C2.42 ▲■ pattern formation / biological
- **T8 Mixed / composite operators (the E_int test-bed: sums of terms):**
  - C2.12 ★ advection–diffusion, telegraph, damped wave
  - C2.19 ★ higher-order linear PDEs (factorisation, so the additive split of §1.2-2a)
  - C2.23 ◇ mixed type (Tricomi, Keldysh)
- **T9 Nonlocal / fractional:**
  - C2.37 ◆★ integral and nonlocal (convolution operators ↔ symbols)
  - C2.38 ◆★ fractional (the symbol |ξ|^α extends the catalogue)
- **T10 Nonlinear and integrable:**
  - C2.15 ▲ nonlinear PDEs (Burgers / Cole–Hopf = the V·V_x of A6)
  - C2.16 ▲◆ integrable and asymptotic structures
  - C2.24 ▲■ conservation laws
  - C2.44 ▲ traveling waves
  - C2.45 ▲ integrable nonlinear (Lax pairs, IST)
  - C2.47 ▲ blow-up
- **T11 Applied physical models (multi-D, systems):**
  - C2.26 ◇■ compressible fluids
  - C2.27 ◇■ incompressible fluids
  - C2.28 ◇■ shallow water
  - C2.29 ◇■ electromagnetism
  - C2.32 ◇■ elasticity
  - C2.33 ★◇ plates and beams (the Euler–Bernoulli beam ∂_t² + ∂_x⁴ is a ★ 1D test case)
  - C2.40 ◇ kinetic
  - C2.43 ▲◇ free-boundary problems
  - C2.57 ◇ PDEs on graphs and networks
- **T12 Stochastic:**
  - C2.41 ● probability and stochastic PDEs (Feynman–Kac ◆ as an analytic representation)

**Axis 2 — Exact analytic solution methods (how kernels are computed: the C2 toolset)**
- C2.13 ★◆ separation of variables / Sturm–Liouville
- C2.14 ★◆ integral transforms
- C2.36 ★◆ Green's functions and fundamental solutions
- C2.48 ◆ perturbation and asymptotics (feeds P3)
- C2.49 ◆ similarity and scaling
- C2.50 ◆◇ Lie-group methods (feeds II.4)
- C2.51 ◆ variational / weak formulations
- C2.60 ★◆ inverse problems and parameter identification (= C3/P4)

**Axis 3 — Functional-analytic framework (what C1 is built on)**
- C2.52 ◆ Sobolev spaces / distributions
- C2.53 ◆ functional analysis / evolution equations (semigroups, the sum rule of §1.2-2b)
- C2.54 ◆ well-posedness
- C2.55 ◆ boundary and initial-boundary conditions
- C2.56 ◇◆ coordinates / geometric PDEs

**Axis 4 — Structural attributes (classify every catalogue entry along these)**
- **S1 Form and classification:**
  - C2.17 ◆ classification and canonical forms
  - C2.17′ order and derivative structure
  - C2.18′ linearity
  - C2.19′ principal symbols (= II path (a))
  - C2.20′ differential operators
  - C2.21′ coefficient structures
  - C2.22′ scalar vs system ■
  - C2.23′ independent and dependent variables
- **S2 Domain and data:**
  - C2.24′ domain geometry
  - C2.25′ initial-value formulations
  - C2.26′ boundary-condition structures
  - C2.27′ BVP classifications
- **S3 Characteristic and causal geometry:**
  - C2.28′ characteristic geometry
  - C2.29′ causality and propagation
- **S4 Invariants:**
  - C2.30′ conservation
  - C2.31′ symmetry and invariance (rotations → II.4)
  - C2.32′ scaling
- **S5 Representation, kernel and spectrum — the core of C1–C4/P4:**
  - C2.33′ transforms
  - C2.34′ kernel structures (incl. **reproducing kernels** → C1.0)
  - C2.35′ spectral structures
  - C2.36′ orthogonality and completeness (**biorthogonal systems** → P3 duals)
- **S6 Spaces and solution theory:**
  - C2.37′ functional spaces
  - C2.38′ regularity
  - C2.39′ generalised solutions
  - C2.40′ existence and uniqueness
  - C2.41′ well-posedness and stability
  - C2.42′ energy estimates
  - C2.43′ maximum principles
  - C2.44′ monotonicity
- **S7 Variational and dynamical geometry:**
  - C2.45′ variational
  - C2.46′ Hamiltonian / symplectic
  - C2.47′ gradient flows
  - C2.48′ dissipative
- **S8 Operator-theoretic extensions:**
  - C2.49′ nonlocal / ΨDO (symbol calculus ↔ â = f(J·Φ))
  - C2.50′ microlocal
  - C2.51′ geometric differential
  - C2.52′ coordinate representations
  - C2.53′ singularities
- **S9 Interfaces:**
  - C2.54′ free boundaries
  - C2.55′ transmission / coupling
- **S10 Stochastic, multiscale and perturbative:**
  - C2.56′ ● stochastic
  - C2.57′ multiscale
  - C2.58′ perturbative (→ P3)
- **S11 Stability and long-time behaviour:**
  - C2.59′ bifurcation
  - C2.60′ long-time
  - C2.61′ coherent structures
  - C2.62′ singular waves
- **S12 Nonlinear structure ▲:**
  - C2.63′ entropy
  - C2.64′ **nonlinear interaction / mode coupling** (the nonlinear analogue of E_int)
  - C2.65′ integrability
  - C2.66′ reduction and equivalence (dependent-variable transformations = the analytic "encoder" of D1)
  - C2.67′ boundary asymptotics
  - C2.68′ averaging
- **S13 Inverse, control and data:**
  - C2.69′ ★◆ **inverse and identification structures** (= G★ itself)
  - C2.70′ control / observability (observability ↔ identifiability C3.2)
  - C2.71′ ● data assimilation
- **S14 Numerical ○ (reference only):**
  - C2.58 numerical methods
  - C2.59 CFD
  - C2.72′ discretisation (discrete differential operators are useful as **finite-dimensional analogues** of J_φ in II)
  - C2.73′ stability and consistency
  - C2.74′ approximation spaces (spectral and wavelet bases are what A4 forbids as generic bases, so they are useful as contrast)
  - C2.75′ solvers (operator splitting ↔ Trotter/§1.2-2b)
- **S15 Modelling:**
  - C2.76′ model structure and closure

**Card schema (filled for every item in Axis 1 and Axis 2, and used as columns for Axis 4).** Each catalogue entry answers:
- (1) the canonical operator(s) T and its symbol p(τ,ξ);
- (2) the kernel / solution class ker T and basis {e_{n,i}}, countable or continuous;
- (3) its special functions and transforms;
- (4) its decomposition into components (factorisation ⇒ additive; sum of commuting terms ⇒ multiplicative; non-commuting ⇒ commutators);
- (5) the data C1 needs: Gram blocks with other classes and the dual system;
- (6) its Axis-4 attributes S1–S15;
- (7) the relevance tag;
- (8) sources;
- (9) a SymPy check that T e = 0.

#### §1.3-C2-SRC — Sources added by the user (MIT OCW), mapped to C2
- **MIT 18.03 Differential Equations, Spring 2010, lecture notes:** https://ocw.mit.edu/courses/18-03-differential-equations-spring-2010/pages/lecture-notes/
  - I. First order (L1–L9): direction fields/existence-uniqueness, numerics ○, linear equations, integrating factors, complex numbers, complex exponentials, sinusoidal response (gain, phase lag), autonomous equations / phase line / stability, linear vs nonlinear → C2.3, C2.1.
  - II. Second-order linear (L11–L18): modes and the characteristic polynomial; damping; **exponential response formula**; complex gain; **operators, undetermined coefficients, resonance**; frequency response; LTI systems and superposition → C2.1, C2.2.
    - The ERF p(D)e^{rt} = p(r)e^{rt} is exactly the **symbol action** behind F1 and §1.2-3, so it is a key reading for II and P1.
  - III. Fourier series (L20–L30): Fourier series and operations, periodic solutions, resonance, step and delta functions, step and impulse response, **convolution**, Laplace transform, the pole diagram, **transfer function** → C2.14, C2.36.
    - Transfer function = symbol; convolution = the multiplicative composition of §1.2-2b.
  - IV. First-order systems (L32–L39): matrices, eigenvalues and eigenvectors, complex or repeated eigenvalues, phase plane, **normal modes and the matrix exponential**, nonlinear systems, linearisation, limit cycles and chaos → C2.2, II path (b) (companion matrix / Jordan), Phase 4.
- **MIT 18.303 Linear PDEs, Fall 2006 (M. Hancock):** https://ocw.mit.edu/courses/18-303-linear-partial-differential-equations-fall-2006/ (lecture notes at `/pages/lecture-notes/`, syllabus at `/pages/syllabus/`)
  - L1–9: 1D heat equation (separation of variables, Fourier series, **Sturm–Liouville**) → C2.7, C2.13.
  - L10–15: 1D wave equation (characteristics) → C2.8, C2.28′.
  - L16–18: quasilinear PDEs (characteristics) → C2.15.
  - L19–28: heat and wave equations in 2D/3D (**Bessel functions**, Laplace's equation) → C2.5, C2.9, C2.56.
  - L29–33: infinite domains and the Fourier transform → C2.14.
  - L34–35: Green's functions for ODEs and PDEs → C2.36.
  - Textbooks: Guenther & Lee, *PDEs of Mathematical Physics and Integral Equations* (Dover 1996); Myint-U & Debnath, *Linear PDEs for Scientists and Engineers*, 4th ed. (Birkhäuser 2006). Both added to R3's source list.

**PR-C2 — Pre-research over ALL categories (new point, user v3)**
- **Statement:** before C2 is solved, build a complete, classified **map** of every category in §1.3-C2-EXT, organised by §1.3-C2-TAX, with one card per item using the card schema above.
- **Goal:** no category is missed. Every category is tagged with its relevance to G★, and the ★ and ◆ cards are detailed enough to start S-C2/C4 and C1.0.
- **Sub-goals:**
  - PR-C2.1 Taxonomy file with all 120 items (60 in C2.1–C2.60 and 60 in C2.17′–C2.76′), each placed once.
  - PR-C2.2 Full cards for every ★ and ◆ item.
  - PR-C2.3 Short cards (operator, kernel class, tag, 2 sources) for ▲ ■ ● ◇ ○ items.
  - PR-C2.4 Cross-index: which items share kernel classes (e.g. heat kernel in C2.7, C2.21, C2.41 Feynman–Kac, C2.53 semigroups).
  - PR-C2.5 A "components" matrix: which elementary terms (∂_t, ∂_x, ∂_x², ∂_x³, ∂_x⁴, multiplication by x or f(x), nonlocal |ξ|^α, …) occur in which family. This is the actual list of components that A6 asks for.
- **Deliverable:** `research/PR-C2/TAXONOMY.md` + `research/PR-C2/cards/*.md` + `components_matrix.md`.
- **Done when:** all 120 items are placed; ★/◆ cards pass `kernel-catalog-entry` with SymPy checks; R2/R3 sign off on the cross-index.

**C3 — The operator from its kernel (identification map 𝓘).** *Source: C3/P4, D2, F5; user: "component 3: find who studied such operators and all approaches; maybe the component approach is not the right one".*
- **Statement:** study 𝓘 : u ↦ Ann(u), the minimal annihilating operator. This is the map from a kernel element back to the operator.
- **Goal:** know every existing formalism for it and pick the best one. Candidates: Prony/Hankel, the Wronskian/Gram kernel, D-finite guessing, differential elimination, Ehrenpreis–Palamodov (characteristic variety from μ), and inverse spectral theory (Gel'fand–Levitan).
- **Sub-goals:**
  - C3.1 Literature map of who studies "operators from kernels".
  - C3.2 Identifiability theorem: when one solution determines L, e.g. when supp μ is Zariski-dense in V(P).
  - C3.3 A verdict on whether the component approach is optimal compared with the annihilator-ideal and symbol approaches.
- **Deliverable:** `work/C3/PROOF_PACKAGE.md` plus a comparison memo.
- **Done when:** the identifiability theorem is proved in the ODE and constant-coefficient PDE cases, and the verdict is documented.

**C4 — The basis {e_n} = union of component classes (A4/A5 constraint).** *Source: A4–A8; user: "component 4 like 2: basis from kernels".*
- **Statement:** build {e_n} = ⋃_n {e_{n,i}} under constraint k2 (not Legendre, not Fourier), and decide whether A8 (â = Σa_n ⟺ f̂ = ΣΣe_{n,i}) is true, false, or true only in a transformed domain.
- **Goal:** the correct form of A8, with hypothesis that it holds when the operator **factorises** (additive split), the **multiplicative/convolutive** form for **sums of commuting terms**, and **commutator corrections** otherwise.
- **Sub-goals:**
  - C4.1 Prove or disprove A8 as written.
  - C4.2 Factorisation theorem: ker(P₁P₂) = ker P₁ ⊕ ker P₂.
  - C4.3 Sum theorem: semigroup product form, and the log-symbol additivity.
  - C4.4 Countability: Schauder vs Riesz vs continuous frames (integrals over V(P)).
- **Deliverable:** `work/C4/PROOF_PACKAGE.md`.
- **Done when:** the status of A8 is in the claims LEDGER with a proof or counterexample checked by SymPy.

**P1 — Structure of E_int: E_int ≈ h(e₁,e₂), complexity ≠ O(eⁿ).** *Source: B2–B4.*
- **Statement:** define E_int := u − Σ_n P_n u, where P_n projects onto K_n, or the analogous expression in the chosen picture. Find h explicitly and its algebraic type (bilinear, convolution, commutator series).
- **Goal:** an exact formula for h, and a polynomial-time algorithm (e.g. linear in N in the symbol domain).
- **Sub-goals:**
  - P1.1 Commuting case: h = convolution product, 2ᴺ inclusion–exclusion vs O(N) in log-symbol.
  - P1.2 Non-commuting case: BCH/Zassenhaus truncation and error bounds.
  - P1.3 The "matrix of functions E" from B2, as the Gram/interaction matrix.
  - P1.4 Proof that no local or approximate model is needed (B4), or a proof of why one is.
- **Done when:** theorem plus complexity proof; local solutions only as a documented fallback.

**P2 — Regularisation: does ℒ_ALT (L¹) remove E_int? Compare with ℒ_G (L²).** *Source: B5–B8, C1.*
- **Statement:** regularisation = a prior on the coefficients (L² ↔ Gaussian, L¹ ↔ Laplace/sparse).
- **Goal:** theorems giving conditions on the dictionary (null-space property, coherence, RIP) under which basis pursuit returns exactly the true components and puts E_int into the residual, or "lo elimina". Also a proof that L² cannot do this (it spreads weight).
- **Sub-goals:**
  - P2.1 Exact recovery theorems specialised to kernel dictionaries.
  - P2.2 Coherence between classes, e.g. Gaussians vs Airy.
  - P2.3 Other regularisers from B7: total variation, group-L¹ per component (natural "grouping" for D1), reweighted L¹.
- **Done when:** a theorem with explicit hypotheses and SymPy/numerical counterexamples at the boundary. Numerics are for checking only, never for the method.

**P3 — Identify E_int when it can't be removed (perturbation / duals).** *Source: C1–C2.*
- **Statement:** treat L₂ as a perturbation of L₁ and use the interaction picture U_I(t) = e^{−tL₁}e^{t(L₁+L₂)}, the Dyson series, and matrix elements ⟨e^†_m|L₂|e_n⟩ e^{(λ_m−λ_n)t} (as for radiation–matter interaction).
- **Goal:** a closed or convergent series formula for ⟨e^†_{n,i}|E_int⟩.
- **Sub-goals:**
  - P3.1 Dual basis from C1.4.
  - P3.2 First- and second-order terms.
  - P3.3 Convergence (Kato).
  - P3.4 What the duals reveal: selection rules, when the coefficients vanish.
- **Done when:** proved formula plus symbolic verification on transport + diffusion with a variable coefficient.

**P4 — Construct Â⁻¹ / the identification map.** *Source: C3.*
- **Statement:** from the spectral data ({e_{n,i}}, λ) rebuild Â = Σ λ e⊗e^† (spectral synthesis). Read C3 as "Â⁻¹ acting on {e_{n,i}} identifies Â".
- **Goal:** existence and uniqueness of the reconstruction, and its relation to 𝓘 from C3. The resolvent (Â − z)⁻¹ is the natural "Â⁻¹".
- **Sub-goals:**
  - P4.1 Spectral synthesis.
  - P4.2 Resolvent/Green's-function route.
  - P4.3 Identifiability: the link to C3.2.
- **Done when:** theorem in the ODE and constant-coefficient PDE cases.

**II — Matrix/tensor formulation and geometry.** *Source: D2–G6.*
- **Statement:** compare path (a), the symmetric tensor J^n_φ (principal symbol) with J_{ω,λ} = λ⊗J_φ, and path (b), the companion/first-order system (with the operator-valued "non-matrix" last row of E1).
- **Goal:**
  - answer E4 (which construction carries more invariants for the system order, under coordinate changes and similarity);
  - make â = f(J·Φ) precise as functional calculus (F1/F2, including tensor eigenvalues);
  - make the reduced space precise (E5, G6: SVD/HOSVD/Tucker core);
  - decide when one can "rompere il sistema" per direction (F6, joint diagonalisation, rotations: crossed-out word in G6).
- **Sub-goals:**
  - II.1 Invariant table: companion (characteristic polynomial, Jordan) vs symbol tensor (GL/O-invariants, discriminants).
  - II.2 Variable coefficients: matrices over the Weyl algebra / D-modules.
  - II.3 Functional calculus and its link to C4.3 (log-symbol additivity).
  - II.4 Geometry: characteristic variety, Lie symmetries, rotation groups → special functions.
- **Done when:** the structure decision is recorded at Gate 3.

**I — Preprocessing (t-SNE/AE/GMM). Postponed.** The only part kept now is D1 as an analytic theorem (encoder = spectral transform, grouping = group-L¹).
**Problema 1 / Problema 2 — Postponed** until after Phase 5. Pointers for Phase 1 reading only: inverse Sturm–Liouville / Gel'fand–Levitan (V varies); Clifford algebras / matrix-valued symbols (Dirac λ ∈ Mat 4×4).

### 1.4 How the items relate (dependency graph)
```
            ┌──────────── C3 (u ↦ Ann(u), identifiability) ────────────┐
            │                         ▲                                  │
  C2 catalogue ──► C4 basis & A8 status ──► P1 E_int structure ──► P3 E_int via duals/Dyson
     ▲   │             ▲        │                ▲      │                  ▲
     │   └─► C1 space/frames ───┴──► P2 L¹ vs L² ┘      └──► P4 Â⁻¹ / spectral synthesis
     │                                                     ▲
     └──────────── II symbol/tensor/companion, functional calculus, geometry ──┘
   (II supplies the "encoder" that makes E_int additive; it feeds C4.3, P1.1, P4)
```
- **Critical path:** C2 → C4 → P1 → (P2 ∥ P3) → P4 → G★. C1 and II run alongside from the start, because both change how E_int is defined.
- **v3 addition:** **PR-C2 → C2 ⇒ C1.** C1 is *built from* C2 (C1.0), so the arrow C2 → C1 is a construction, not a weak dependency. The critical path becomes PR-C2 → C2 ⇔ C1 → C4 → P1 → (P2 ∥ P3) → P4 → G★.
```
 PR-C2 (all 120 categories, classified) ──► C2 catalogue ══build══► C1 space (𝓗_𝒟, Gram G, kernel K, duals)
                                             │                         │
                                             └──► C4 / A8 status ◄─────┘──► P1 … (as above)
```

### 1.5 Ladder of cases (the order in which G★ is proved; G2 and F5 say "linear first")
| Level | Case | Expected tool | Expected E_int |
|---|---|---|---|
| L0 | linear ODE, constant coefficients | Prony/Hankel, companion + Jordan | 0 (spectral projectors) |
| L1 | linear ODE, polynomial coefficients | holonomic guessing, Weyl algebra | commutator terms |
| L2 | u_t = Σ a_k ∂_x^k u, constant coefficients | Fourier symbol, semigroups | 0 in log-symbol; bilinear additively |
| L3 | general P(∂_t,∂_x)u = 0, constant coefficients | Ehrenpreis–Palamodov, primary decomposition | 0 for factorisable P |
| L4 | variable coefficients f_k(x) (E1) | interaction picture, BCH, Kato | commutator series |
| L5 (Phase 4) | nonlinear (V·V_x, f(S·x)) | Cole–Hopf, Carleman/Koopman, Lax pairs/IST | — |

---

## 1.6 Adaptive research protocol (v4: the plan is dynamic; every list of options in this file is a **starting set, not a closed menu**)
**Principle.**
- Every decision point in this plan carries an explicit **open slot "(ω) route not yet known"**. Each option list (paths a/b, routes (i)–(iv), candidate spaces, tools in the ladder table, agents R1–R8, sessions S-*) is a **seed**.
- Research may add options, merge them, split them or kill them. The central session may not close a decision while an open-slot candidate with evidence is still unevaluated.
- Section 1 (G★, H0–H4, §1.2 facts, the ladder) is itself a set of **working hypotheses**. Each can be revised, refuted or replaced. If §1.2 turns out wrong (e.g. A8 is true in a sense I did not foresee), the plan follows the evidence, not the reconstruction.

**Route registry: `ROUTES.md` (new blackboard file, owned by the central session; any agent may propose).** One entry per route:
- id, decision point it belongs to, and its origin (seed / discovered by R# / S#);
- one-paragraph idea, with the notes it relates to (point IDs A1…H3);
- status: `seed | proposed | scouting | active | parked | merged-into:X | killed`;
- evidence for and against, with links into `research/` or `claims/`;
- cost estimate, and what result would **promote** or **kill** it (kill criteria fixed in advance);
- owner session/agent, and review date (next gate).

**How a new route enters (discovery loop).**
1. Any agent that finds an approach not already in the plan writes `inbox/central.md` with tag `NEW-ROUTE`. Example sources: a different formalism for "operators from kernels", a geometric picture, a known theorem that makes a P_i trivial or impossible, a better space than C1's.
2. The central session registers it as `proposed` within the same work cycle.
3. Triage uses three questions: does it serve G★ or a C/P/II item? Is it analytic, so not violating k3? Is it cheaper or stronger than the active route?
4. If it passes, it gets a **scouting budget**: one short agent, a `PLAN.md`, the right research or proof skill, and a 1-page verdict.
5. At the next gate it is promoted, parked or killed, and the outcome is recorded in `ROUTES.md` and on the BOARD.

**Re-planning triggers (any of these forces a re-plan at the next gate, or immediately if blocking):**
- A **counterexample** to a claim on the critical path, e.g. A8 or C4.2.
- An **impossibility result**, e.g. non-identifiability in C3.2 or NP-hardness of P1.
- A **literature hit** showing an item is already solved, or solved better, elsewhere. G★ is then re-scoped toward what is new (R8).
- A route needing a **new skill or tool**. Phase 2 can be re-entered at any time; skills are added mid-project via `skill-creator`.
- **New sub-problems** found inside an item. That item is split into sub-items (P1.a, P1.b …) with new sessions, as Phase 3 already allows.
- **User input** (new notes or pages, a change of priority).

**Breadth safeguards (so choices are never only "what I decided").**
- **Horizon scouts:** in every phase, 1–2 agents have the *only* job of looking **outside** the seeded options. They search adjacent fields (algebraic geometry, representation theory, operator algebras, harmonic analysis, control theory, signal processing, mathematical physics, category-theoretic views) for formulations of "operator from kernel / component splitting / E_int". They report via `NEW-ROUTE`.
- **Devil's-advocate pass:** at each gate a `kill-argument` / `scientific-critical-thinking` run attacks the *chosen* route and argues for the best alternative.
- **Exploration quota:** at each gate at least one non-seed route must be either scouting or explicitly killed with reasons. "We didn't look" is not an allowed outcome.
- **Parallel routes allowed:** when two routes are both credible, both stay `active` with separate sessions until evidence separates them. Parked routes are re-checked at every later gate, because results from other phases can revive them.

**Where the open slot applies (non-exhaustive; it applies to every decision in the plan):**
- **§1.1 H0–H4:** the domain, space, operator class and data model may change. Examples: several solutions instead of one; distributions or hyperfunctions; operators over other rings.
- **§1.2 analytic facts 1–3:** these are guesses about the mathematical structure. Alternatives are welcomed: e.g. a geometric/sheaf picture of kernels, Galois-theoretic splitting, a categorical sum/product duality.
- **§1.3 every item:** sub-goals can be added, and an item can be re-defined, merged or found ill-posed. C3's question "is the component approach right?" is the explicit example, and its answer may replace the C/P structure itself.
- **§1.5 ladder:** levels may be reordered, inserted (e.g. L0.5 periodic coefficients / Floquet–Hill) or skipped. The "expected tool" and "expected E_int" columns are predictions to be tested, not choices.
- **II (path a vs b vs symbol):** the open slot (ω) covers, for example, Clifford/geometric-algebra encodings, operator-valued matrices over D-modules, Lie-algebraic or quiver representations, Hopf/jet-bundle formalisms, or a construction found in research.
- **P2 regularisers:** beyond L² and L¹, anything found (B7 already says "other regularisations are possible").
- **Phase 4 (i)–(iv):** the open slot (v) covers anything Phase 3, R7 or the scouts surface. Examples to *check, not to assume*: Painlevé analysis, Darboux/Bäcklund dressing, hodograph or Miura maps, tropical or asymptotic linearisation, normal forms, monotone-operator theory, a new space suggested by the Phase-3 structure.
- **Phase 5 formalisation order:** bottom-up is the default. If a route turns out to depend on missing Mathlib pieces, the order and even the proof assistant (Lean vs Isabelle/Coq) are re-decided.

## Step 0 — Install every requested skill (first action on execution, after the folder is chosen)
All downloads go into a new, empty folder: `<project>/_vendor/<repo>/`, cloned with `git clone --depth 1`. Each skill folder is read before it is copied to `~/.claude/skills/`. Python dependencies go into a project venv run with `python -I`.

| Requested | Source found | Install |
|---|---|---|
| proof-checker, proof-writer, lean-formalize (+ proof-orchestrator, kill-argument, research-lit, idea-discovery, openalex, research-wiki, citation-audit) | `wanshuiyin/Auto-claude-code-research-in-sleep` (ARIS) | `claude plugin marketplace add wanshuiyin/Auto-claude-code-research-in-sleep` → `claude plugin install aris@aris` → `/aris:setup` **without** the Codex bridge (decision: Claude-only review) |
| math-skill (12 modes, SymPy helpers) | `googlarz/math-skill` | clone, then copy to `~/.claude/skills/math-skill`; `pip install sympy numpy mpmath` |
| scientific-agent-skills (all ~177) | `K-Dense-AI/scientific-agent-skills` | `npx skills add K-Dense-AI/scientific-agent-skills` (all skills, as requested). Key ones: sympy, paper-lookup (arXiv/S2/OpenAlex), literature-review, scientific-writing, scientific-critical-thinking, hypothesis-generation, scientific-brainstorming, peer-review, citation-management |
| academic-research-skills (all 5) | `Imbad0202/academic-research-skills` | `/plugin marketplace add Imbad0202/academic-research-skills` → `/plugin install academic-research-skills` (deep-research, academic-paper, academic-paper-reviewer, academic-pipeline, sr-screener) |
| **doc2math** | `sickn33/agentic-awesome-skills` (`skills/doc2math`) | `npx skills add sickn33/agentic-awesome-skills --skill doc2math`. Run it **without** its external hosted BYOK tool (that would send the notes to a third party) |
| **Mathpix** (handwriting → LaTeX) | `Mathpix/mpxpy` (official Python client) + `Mathpix/mpx-cli` | `pip install mpxpy`. Needs a Mathpix account: **the user sets `MATHPIX_APP_ID` / `MATHPIX_APP_KEY` themselves**, because I must not enter API keys. Uploading the 8 photos to Mathpix is the user's request |
| Lean toolchain (for lean-formalize) | elan (official) | Windows elan installer, then `lake new` a project with **Mathlib**; verify with `lake build` |
| Extra (recommended) | SageMath `ore_algebra` | guessing and closure of D-finite functions, which is exact. Optional, via WSL or conda |

**Step 0.5 — Re-OCR and formal spec, using the new skills**
1. Rotate the 8 photos 180° (Pillow) into `notes/img/`.
2. Run Mathpix (`mpxpy`) on each page and save `notes/mathpix/pgX.mmd`.
3. Diff Mathpix output against Section 0B and list every disagreement for the user (`notes/OCR_diff.md`).
4. The user resolves the `[?]` items.
5. Run `doc2math` on the reconciled text and save `notes/MPS.json`, replacing draft 0D.
6. Update Section 1 wherever the MPS changes a definition.

**Gate 0:** the user confirms the transcription, the C1–C4 mapping, and H0–H4.

Verification: `ls ~/.claude/skills`, `claude plugin list`, run `/ars-plan` (smoke test), run math-skill's SymPy helper on one test, `lake build` a trivial Mathlib theorem, and get a Mathpix test response on one page.

---

## Shared workspace (the "blackboard" every agent and session uses)
```
<project>/
  notes/OCR_appunti.md            ← sections 0A–0C verbatim; notes/mathpix/, notes/MPS.json, notes/OCR_diff.md
  PROBLEM.md                      ← Section 1 (G★, H0–H4, item dictionary, graph, ladder); versioned
  BOARD.md                        ← central status: every C/P/I item, owner, status, links ("punto situazione")
  glossary.md                     ← one notation for e_{n,i}, E_int, J_φ, J_ω, Φ, Â (fixed in Phase 1)
  research/R1..R8/{PLAN.md, REPORT.md, sources.bib, open_questions.md}
  ROUTES.md                       ← v4 route registry (seed / proposed / scouting / active / parked / merged / killed), see §1.6
  research/SCOUT-*/               ← v4 horizon-scout verdicts (1 page each)
  inbox/<agent>.md                ← async messages between agents (append-only, dated)
  claims/LEDGER.md                ← every claim: statement · status (provable / needs assumption / unjustified / false) · proof link · checker report
  work/<C*|P*|II>/PROOF_PACKAGE.md, sympy/, lean/
  skills-local/                   ← project skills created in Phase 2
```
Protocol for every agent and session: (1) write `PLAN.md` before any tool use, (2) name the skill being invoked explicitly, (3) write results only to its own folder plus `inbox/` messages, (4) the central session alone edits `BOARD.md`, `PROBLEM.md` and `glossary.md`. Live messages use `SendMessage`. The files are the durable record.

---

## Phase 1 — Research (8 parallel research agents + central coordinator)
**Phase goal:** for every item in 1.3, find the known theorems, the open parts, and the claims that are likely false. Decide whether the component approach survives.
Each agent first writes `PLAN.md` (questions, sources, search strings). Then it runs `academic-research-skills:deep-research` (or `anthropic-skills:deep-research`) with `paper-lookup` / `research-lit` / `openalex`. It ends with `REPORT.md` (findings mapped to C/P/II items, key theorems stated precisely, references in BibTeX) and `open_questions.md`.

| Agent | Topic | Maps to | Questions it must answer | Core sources to pull |
|---|---|---|---|---|
| **R1** Hilbert spaces ↔ ML, analytically | RKHS, representer theorem, Tikhonov/regularization theory, L¹ vs L² (compressed sensing, exact recovery theorems: RIP, coherence), Gaussian processes as analytic objects, Koopman/DMD spectral theory | C1, P2 | C1.1–C1.4, P2.1–P2.3 | Aronszajn, Schölkopf–Smola, Engl–Hanke–Neubauer, Candès–Romberg–Tao, Donoho, Mezić |
| **R2** Kernels of differential operators and function classes | Ehrenpreis–Palamodov, Malgrange, D-modules/algebraic analysis, holonomic/D-finite functions, Picard–Vessiot/differential Galois, closure properties (sum/product of D-finite) | C2, C4, P1 | C4.2 (ker of product = ⊕), C4.4, C2.6 | Hörmander (Analysis of Linear PDO II), Björk, Kauers–Paule, van der Put–Singer, Härkönen–Lange-Hegermann–Raiță (EPGP, 2023) |
| **R3** Term-by-term catalogue of linear PDE pieces | for ∂_t, ∂_x (transport), ∂_xx (diffusion), ∂_xxx (dispersion/Airy), reaction, x-dependent coefficients, polar/cylindrical Laplacian: fundamental solutions, Green's functions, eigenfunctions, special functions (Bessel, Airy, Hermite, Legendre), Sturm–Liouville | C2, C4 | C2.1–C2.7 entries | Evans, Courant–Hilbert, Polyanin *Handbook of Linear PDEs*, DLMF, Zettl (Sturm–Liouville) |
| **R4** Operator identification / inverse problems | recovering L from u ∈ ker L: Prony, annihilating filters/finite rate of innovation, differential elimination (Ritt, Rosenfeld–Gröbner), D-finite guessing, identifiability of PDEs from one solution, inverse Sturm–Liouville (Borg, Gel'fand–Levitan, Marchenko) | C3, P4 | C3.1–C3.3, P4.1–P4.3 | Vetterli et al., Boulier, Kauers "guessing", Freiling–Yurko, PDE-identifiability papers |
| **R5** Interaction term E_int | non-commuting operators, BCH and Zassenhaus, Trotter–Kato, perturbation theory (Kato), interaction picture and Dyson series, Duhamel, when ker(L₁+L₂) splits (commuting operators, joint spectra, separation of variables) | P1, P3 | P1.1–P1.3, P3.1–P3.4 | Kato, Reed–Simon, Sakurai, Miller *Symmetry and Separation of Variables* |
| **R6** Matrix/tensor formulation (Idea II) | companion matrices and first-order reduction, Jordan/Frobenius forms, matrix functions f(A) (Higham), operator symbols and pseudo-differential calculus, polynomial eigenproblems, tensor eigenvalues (Qi, Lim), jet spaces. Compare paths (a) and (b) by the invariants they preserve | II | II.1–II.3, E4, E5 | Higham, Gohberg–Lancaster–Rodman, Qi–Luo, Lim 2005, Olver (jets) |
| **R7** Geometry, symmetry, spectral | Lie symmetry groups of PDEs, rotation groups and representations → special functions (Vilenkin), spectral theorem, functional calculus, joint spectra. Plus a **brief** survey of nonlinear spectral and Koopman methods for Phase 4 | II, Phase 4 | II.4, F6, L5 options | Olver *Applications of Lie Groups to DEs*, Vilenkin, Reed–Simon, Koopman literature |
| **R8** Prior art and tooling | closest existing work (SINDy, PDE-FIND, weak SINDy, operator inference, symbolic regression), to position the analytic approach and state what is new. Also Mathlib coverage (Hilbert spaces, spectral theorem, ODE, polynomials) and SymPy/ore_algebra capabilities. One short section on Problema 1/2 and Idea I literature, research only | novelty, Phase 5 | novelty statement for G★ | Brunton–Proctor–Kutz, Rudy et al., Messenger–Bortz, Mathlib docs |

**PR-C2 agent group (v3; runs first, in parallel with R1–R8, and feeds R2/R3 and C1).** Five research agents, one per taxonomy block. Each writes `PLAN.md`, then calls `academic-research-skills:deep-research` + `paper-lookup`, then fills cards with `kernel-catalog-entry` (after Phase 2; before that, the card schema by hand + `math-skill`/`sympy` checks):
- **PR-C2a:** Axis 1 T1 (ODEs C2.1–C2.5) + MIT 18.03 notes.
- **PR-C2b:** Axis 1 T2–T9 (linear PDE families) + MIT 18.303 notes, Guenther–Lee, Myint-U–Debnath, Polyanin.
- **PR-C2c:** Axis 1 T10–T12 (nonlinear, applied, stochastic; short cards).
- **PR-C2d:** Axis 2 + Axis 3 (methods and framework).
- **PR-C2e:** Axis 4 S1–S15 (attribute columns + the components matrix PR-C2.5).

They communicate a→b (ODE kernels are the building blocks of separated PDE kernels), b↔e (attributes), d→R1 (spaces), and all of them → R3. Output gate: the PR-C2 "Done when" in §1.3.

**Communication graph.** R2↔R3↔R4 form the kernel cluster and exchange their operator→function-class tables. R1↔R4 (sparsity ⇔ identifiability). R5↔R2 (when E_int=0). R6↔R7 (matrix, symbol, geometry). R8 reads all and flags overlaps. The central session merges everything into `research/SYNTHESIS.md`: a dependency map of C1–C4, P1–P4 and II, each with "known theorem / open / likely false". It also fixes `glossary.md` and updates `PROBLEM.md`.
**v4 dynamic additions to Phase 1.**
- The R1–R8 topics and the PR-C2 blocks are **seeds**. An agent may widen its own scope in its `PLAN.md`, and may request a new agent (R9, R10, …) via `NEW-ROUTE` when a topic outgrows it.
- Two **horizon scouts** (SCOUT-1: algebra/geometry/representation theory; SCOUT-2: analysis/physics/signal processing/control) run in parallel with no assigned answer.
- SYNTHESIS includes a "routes discovered" section, and a table of which seeded assumptions in §1 survived, changed or fell.

**Gate 1:** I present SYNTHESIS plus an updated BOARD to the user, including whether the component approach survives or a better formulation exists (the user's question for C3). User approval before Phase 2.

## Phase 2 — Skill-building and session design (no mathematics done here)
**Phase goal:** every Phase-3 session has one job, one skill chain, defined inputs and outputs, and defined contacts.
Use `anthropic-skills:skill-creator` to build project skills in `skills-local/` that chain the installed ones:
- **`kernel-catalog-entry`**: the template for "operator term → kernel/function class → closure properties → SymPy check that L e = 0". Calls `math-skill`, then `sympy`.
- **`claim-lifecycle`**: draft (`proof-writer` → PROOF_PACKAGE.md), verify symbolically (`math-skill` counterexample/limit mode), audit (`proof-checker`), adversarial pass (`kill-argument`), and write to `claims/LEDGER.md`.
- **`session-protocol`**: the mandatory PLAN, explicit skill call, artifact and inbox steps, plus how a session reports to the central session.
- **`formalize-claim`** (for Phase 5): statement → `lean-formalize` → `lake build` → axiom check.
- **`spec-sync`**: after any definition changes, re-run `doc2math` on `PROBLEM.md` to keep the MPS consistent.

*(v4) The four project skills above are seeds. Phase 2 also designs skills for any route promoted at Gate 1, and stays **re-enterable**: a new skill can be created at any later gate when a route needs it. The roster in SESSIONS.md is versioned, so sessions can be added, split, merged or retired as routes change.* Add a fifth skill seed **`route-scout`**: NEW-ROUTE note → scouting PLAN → research/proof skill → 1-page verdict → ROUTES.md entry.
Then write `SESSIONS.md` with the roster, each session's skill sequence, its inputs and outputs, and who talks to whom. Profiles: analytic/geometric sessions use proof-heavy chains (proof-writer, proof-checker, kill-argument); Hilbert-space/basis sessions use math-heavy chains plus symbolic simulation (math-skill, sympy). **Gate 2:** user approves the roster.

## Phase 3 — The linear problems (separate sessions, coordinated by the central session)
**Phase goal:** prove G★ along ladder L0→L4, with every claim in the LEDGER.
Draft roster, finalized in Phase 2 and split further if the research shows sub-problems. The goals and done-criteria come from Section 1.3:
- **S-C1** Hilbert space and basis {e_{n,i}}: completeness, countability, the right space (L², Sobolev, distributions, RKHS).
- **S-C2/C4** Kernel classes per operator term, and the sum rule â=Σa_n ⟺ f̂=ΣΣe_{n,i} (status of A8).
- **S-C3** The operator from its kernel: does u determine L (identifiability), and up to what?
- **S-P1** Structure of E_int, h(e₁,e₂), and complexity (is it really O(eⁿ)?).
- **S-P2** Theorems on whether L¹ (ℒ_ALT) eliminates or isolates E_int, compared with L².
- **S-P3** Identifying E_int through duals and perturbation series.
- **S-P4** Constructing Â⁻¹ and the identification map.
- **S-II** Matrix vs tensor construction, comparing invariants; the spectral form â=Σf(λ_a)v_a⊗v_a; geometry.

**v3: S-C1 and S-C2/C4 are one coupled pair.** C1 is built from C2's catalogue (C1.0), and they share `work/C1C2/gram.md`. S-C2/C4 works through the ★ cards of PR-C2 in ladder order L0→L4.
The analytic cluster (C1–C4, P1–P4) works closely together; S-II is linked to all of them. Every claim passes through `claim-lifecycle`. The central session decides the matrix structure (path a vs b vs symbol) from S-II's invariant comparison.
*(v4) The structure decision includes (ω): any construction registered in ROUTES.md, and "combine several" is allowed. The roster above is a seed. Items found ill-posed are re-defined, new sub-problems get new sessions, and one horizon scout stays active during Phase 3. If C3 concludes that the component approach is not the best one, Gate 3 may re-shape the C/P structure itself, with the user's approval.* **Gate 3:** a linear-case theorem package plus the decision on structure.

## Phase 4 — Nonlinearity
**Phase goal:** decide and test the route from G3/G4.
From Phase 3 results and R7, choose between (i) nonlinear spectral and Koopman/Carleman lifting (linearize in a larger Hilbert space), (ii) f(S·x) with componentwise analysis as in the notes, (iii) a Hilbert space built to absorb the nonlinearity, or (iv) exact linearisations (Cole–Hopf, Lax pairs/IST). Run the same session and skill machinery, scalar first (e.g. V·∂_x V, which is Burgers → Cole–Hopf).
*(v4) Routes (i)–(iv) are **seeds**, and the choice is broader than them:*
- **(v) open slot:** any route surfaced by Phase 3, R7, the scouts or the ROUTES registry. Examples to *investigate, not assume*: Painlevé analysis, Darboux/Bäcklund/Miura maps, normal forms, monotone-operator and nonlinear-semigroup theory, nonlinear spectral theory (eigenproblems of nonlinear operators), a new space suggested by the Phase-3 structure.
- **Phase 4 opens with a route-scouting sprint:** horizon scouts plus the `route-scout` skill.
- The choice is made at a dedicated **Gate 4a** with the user. Several routes may run in parallel. Kill criteria are fixed before work starts.
- A **Gate 4b** reviews whether the Phase-3 linear structure itself should be revised in light of the nonlinear findings (feedback loop to Phase 3).

## Phase 5 — Integration and formalization
Integration: a session checks that every result composes and that the notation and assumptions in the LEDGER are consistent. Integration checks also run at the end of each Phase-3 gate. Then `formalize-claim`/`lean-formalize` goes bottom-up from definitions to the main theorem, with `proof-checker` audit reports. Problema 1, Problema 2 and Idea I are reopened only after this.
*(v4) Integration may itself reveal incompatibilities between routes that each worked alone. When it does, the affected routes go back to `active`, and the loop returns to the relevant phase instead of forcing a fit. Formalisation order and tooling follow §1.6. Parked routes from all phases are reviewed one final time before Problema 1/2 reopen, because some may fit the advanced problems better.*

---

## Verification
- **Phase 0:** skills listed, plugin smoke tests, a Mathpix test page, and `lake build` all pass. Gate 0 signed off by the user.
- **Every claim:** a SymPy check (L e = 0, counterexample search) plus a proof-checker report in the LEDGER. Nothing is marked "provable" without both.
- **Gates 1–3:** the user reviews BOARD and SYNTHESIS.
- **(v4) At every gate:** ROUTES.md is up to date; at least one non-seed route was scouted or killed with reasons; the devil's-advocate report is attached; and every re-planning trigger that fired is logged with its consequence.
- **Phase 5:** Lean files compile with no `sorry` and no extra axioms. Known textbook examples are checked against the theory: heat equation, Airy, Bessel, and transport + diffusion as a case with E_int.
