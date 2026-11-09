# AUDIT OP-ANA — ordine di E_int^A9 oltre lo shock, E_int dal bordo, no-go di continuità, P1-Q5 a ε = 1
Revisore: S-CHECK-15 (15ª tornata) · 26/10/2026
Fonte esaminata: `work/OP-ANA/CHECK_REQUEST.md` (per intero) e, perché la CHECK_REQUEST rinvia lì per le prove, `work/OP-ANA/PROOF_PACKAGE.md` §2–§5 (righe 23–200) per i claim auditati; §1 e §6 solo per confrontare le righe proposte. Non letti: PLAN di OP-ANA, script `work/OP-ANA/sympy/*` (il red team è indipendente).
Fatti importati usati come dati (LEDGER): S4T-T3(vi), S4T-L2 (DIMOSTRATO mod [F1]), S4T-T2 Passo 6, [F2] Hopf–Cole (DIMOSTRATO, fix F2-1 di S-CHECK-11), P3-L2, P3-P1, P3-T1(b), P3-T3, P1-T2, P1-L1(d), P1-L2, P1-P1(e), P1-P6. CON-FONTE: [F1] (Lax–Oleinik = Kružkov), [Naz] (Nazarov 1994): solo controllo d'uso.
Skill caricate (lettura dei SKILL.md, nessuno script _vendor eseguito): skills-local/session-protocol (per prima), skills-local/claim-lifecycle, proof-checker (enunciati canonici, micro-claim, checklist A–H, red team, severità a due assi, acceptance gate; revisore = io, niente Codex), kill-argument (Thread 1 e Thread 2 = due subagenti Claude freschi senza contesto; verdetto calcolato da me con la tabella della skill), sympy.
SymPy/mpmath/scipy: `work/CHECK/sympy/audit_opana.py` → `audit_opana.out` (esito in §6).

## 0. Verdetti
| claim | verdetto | stato proposto |
|---|---|---|
| **OPA-T1** (Lemmi 1–3, Passi A–D) | **PASS-con-fix (T1-1 MAJOR di portata, dal kill-argument; T1-2, T1-3 MINOR)**. Matematica locale verificata passo per passo: ρ = ½log(J⁻/J⁺) (segno e fattore ½), logistica, valore 4log(2cosh(ρ/2)) (= 4 ln 2 per ρ = 0), resti di Laplace, separazione \|A+B\|, convergenza dominata | **DIMOSTRATO mod [F1]** (CON-FONTE), **a t fissato** sotto (H_t); non uniforme in t (T1-1) |
| **OPA-C1** | **PASS-con-fix (C1-1, C1-2 MINOR)**; la divergenza Λ(t) = 2log(1/(t−1)) + o(1) per t↓1 è dimostrabile dalla forma chiusa (aggiungere) | DIMOSTRATO mod [F1] |
| OPA-R1 | osservazione; parte "Λ(t) ~ 2log(1/(t−t*))" ora DIMOSTRATA per ε sin x (C1-1); tasso ν\|log ν\| a t = t* e ai tempi degeneri successivi | APERTO (nuovo OPA-Q1) |
| Kill-argument su OPA-T1 | **WARN** (reason_code unresolved_major_or_minor): 1 answered / 3 partially / 1 still_unresolved (P2 major: "senza fattore logaritmico" senza "a t fissato") | → fix T1-1 obbligatorio |
| **OPA-L2** (a),(b) | **PASS** | DIMOSTRATO |
| **OPA-L2** (c) | **PASS-con-fix (L2-1)**: nucleo corretto; **la formula ∫₀ᴸk_s dy = erfc(x/2√Ds) + erfc((L−x)/2√Ds) è FALSA come uguaglianza** (vale ≤, con uguaglianza a meno di termini esponenzialmente piccoli; a s = 0.5: 0.996 contro 1.281). Usata a valle solo come ≤: nessun teorema cambia | DIMOSTRATO con "≤" |
| **OPA-T2** (i)–(iii) | **PASS-con-fix (T2-1 cosmetico)**; costanti N₀ = √(J/π), N₁, il caso k = 3 (t^{9/4}) e la stima uniforme verificati in modo indipendente (serie modale) | DIMOSTRATO |
| OPA-L3, L4, L5 | **PASS** | DIMOSTRATO |
| **OPA-T3** (a)–(d) | **PASS** | DIMOSTRATO |
| **OPA-P3** (i),(ii) | **PASS** (entrambe le direzioni di (TC) ricontrollate caso per caso) | DIMOSTRATO |
| OPA-T3(e) | riduzione a [Naz] **corretta** (logica PASS, fix T3e-1 MINOR di scrittura) | CONDIZIONALE[Naz] |
| **OPA-P4** | **PASS** (Dyson j ≥ 2, induzione Beta, inflow; verifica modale a ε = 1) | DIMOSTRATO (dipende da P3-T1(b)); dati compatibili APERTO |

Rilievi: nessun FATAL. Un rilievo di tipo CRITICAL **locale** per tassonomia (L2-1: formula falsa come scritta) con impatto a valle nullo. Un MAJOR di portata (T1-1, confermato dal kill-argument). Il resto MINOR/cosmetico. **Nessun enunciato numerato risulta falso**; tutte le costanti dichiarate sono state riprodotte indipendentemente.

## 1. Enunciati canonici (Phase 0.5)
- **OPA-T1.** ∀u₀ ∈ C⁴(𝕋) reale, ∀t > 0 fissato con (H_t): lim_{ν→0} ν^{-1}‖S(t)u₀ − S_B(t)u₀‖_{L¹(𝕋)} = Λ_uv(t) e lim_{ν→0} ν^{-1}‖E^add(t)‖_{L¹} = Λ_add(t), con Λ_• = ∫₀^{2π}t|κ_•(x)|dx + 4Σ_i log(2cosh(ρ_i/2)). Dipendenze: [F1] (CON-FONTE), [F2] (DIMOSTRATO), S4T-T3(vi), S4T-L2, S4T-T2 Passo 6. **Quantificatori:** t fissato, poi ν → 0; ν₀ e il resto o(ν) dipendono da t (tramite δ, j₀, η, r₀ del Lemma 1, non quantitativi). **Nessuna uniformità in t affermata né vera** (§2.4).
- **OPA-C1.** ∀ε > 0, ∀t > 1/ε: (H_t) vale per ε sin x con Σ_t = {π}, ρ = 0, Λ_uv = 2log((1+τ)/(1−τcos b)) + 4 ln 2, τ = εt, b = τ sin b, b ∈ (0,π).
- **OPA-L2.** (a) ∀f ∈ H¹₀(0,L), s > 0: ∂S^D(s)f = S^N(s)f′; (b) ∀u₀ ∈ H¹₀: E^{mult,(1)}(t)u₀ = −c∫₀ᵗS^D(t−s)(S^N(s)−S^D(s))u₀′ds; (c) K^N − K^D = 2Σ_jG_{Ds}(x+y−2jL) > 0 e [fix L2-1] ∫₀ᴸk_s(x,y)dy = 1 − S^D(s)1(x) ≤ erfc(x/2√Ds) + erfc((L−x)/2√Ds).
- **OPA-T2.** (i) ∀u₀ ∈ H¹₀ ∩ W^{1,∞}, ∀t > 0: ‖E(t)‖ ≤ C_*|c|D^{1/4}‖u₀′‖_∞t^{5/4}, C_* = (8/5)(2(2−√2)/√π)^{1/2} = 1.3008; (ii) asintotica t → 0⁺ a L, D, c fissati con errore O(t^{5/4+(α+β)/2}); (iii) Θ(t^{k/2+3/4}) con costante esplicita.
- **OPA-T3/P3.** Ω = (0,T) × J rettangolo limitato; per ogni m ≥ 0 e t₀ ∈ Ī, illimitatezza (sup_ζ R(ζ) = ∞) di E^add: (𝔅 ∩ ker Q, ‖·‖_{H^m}) → L², sotto (ND)+(S); per termini proporzionali: limitata da H¹ ⟺ (TC).
- **OPA-P4.** ∀u₀ ∈ H¹₀ ∩ W^{2,∞}, 0 < t ≤ min(1, L/c): ‖E^mult(t)u₀ − E^{mult,(1)}(t)u₀‖ ≤ C(c,D,L,‖u₀′‖_∞,‖u₀″‖_∞)t^{3/2}.

## 2. OPA-T1 e OPA-C1 (priorità 1)
### 2.1 Micro-claim ed esiti
| MC | passo | esito |
|---|---|---|
| T1.1 | Periodicità: Φ_{x+2π}(y+2π) = Φ_x(y) + 2πū₀ ⇒ M(x+2π) = M(x)+2π, ⟨y⟩_{x+2π} = ⟨y⟩_x + 2π | OK (U₀(y+2π) = U₀(y) + 2πū₀) |
| T1.2 | [F2] nella forma ⟨y⟩ rispetto a e^{−Φ_x/2ν}: nucleo del calore con diffusività ν = e^{−(x−y)²/4νt} = e^{−[(x−y)²/2t]/2ν} | OK |
| T1.3 | Lemma 1(i): 𝒦 = {(x,a): a ∈ M(x)} compatto (limitato per S4T-L2(a), chiuso per continuità congiunta di Φ) ⇒ J ≥ 2j₀ su 𝒦; uniforme continuità di u₀′ ⇒ δ₁; scelta di δ ≤ min_i(a_i⁺−a_i⁻)/8 | OK |
| T1.4 | Lemma 1(ii): IFT con ∂_aF = J > 0 (u₀ ∈ C⁴ ⇒ rami C³); a_i⁺(x) − a_i⁻(x) ≥ 8δ − δ; inviluppo d/dx Φ_x(a(x)) = (x−a)/t ⇒ Δ_i′ = −(a⁺−a⁻)/t | OK (anche ricontrollato: la derivata parziale in x è (x−y)/t valutata sul ramo) |
| T1.5 | Lemma 1(iii): g(x̄) > 0 (minimo su compatto grazie alla crescita quadratica, Lemma 3); |Φ_x − Φ_{x̄}| ≤ |x−x̄|(|x−x̄|+2|x̄−y|)/2t; stima g − g/4 − g/4 = g/2 del margine; M(x) negli intorni δ/2; unicità per stretta convessità (Φ″ = J/t ≥ j₀/t su [ā−2δ, ā+2δ] grazie a (1a)); ricoprimento finito del compatto [0,2π]∖Σ^{r₀}; η = min/2 | OK. Uso di (H_t): (i) in (1a) per j₀ > 0; (ii) per la finitezza di Σ_t e i due rami. Il Lemma 3 è citato prima d'essere enunciato ma è indipendente (nessuna circolarità) |
| T1.6 | Lemma 2: λz²/2 ≤ ψ ≤ Λz²/2; I₀ ≥ ½√(2πε/Λ) per ε ≤ Λδ²/4 (δ ≥ 2σ); (iii) con m_k esplicito; integrazione per parti con bordo ≤ 2ε‖φ‖e^{−λδ²/2ε}; ⟨z²⟩ = ε/p + O(ε^{3/2}); p⟨z⟩ + (q/2)⟨z²⟩ = O(ε^{3/2}) ⇒ (ii); (i) via |e^{−A} − e^{−B}| ≤ |A−B|e^{−min} | OK; costanti dipendenti solo da (λ, Λ, M₃, M₄, δ), uniformi in x perché λ = j₀/t, Λ = (1+t‖u₀′‖)/t, M₃ = ‖u₀″‖, M₄ = ‖u₀‴‖. Red team: ⟨z⟩ + εq/2p² = O(ε^{3/2}) su tre ψ di prova (§6) |
| T1.7 | Lemma 3: crescita (y−x)²/4t per |y−x| ≥ R₁; fattorizzazione e^{−η/4ν}e^{−(Φ−m)/4ν} | OK |
| T1.8 | Passo A: ⟨z⟩ = −ε u₀″(a)/(2(J/t)²) con ε = 2ν ⇒ ⟨y⟩ − a = −νt²u₀″/J², u − v = (a − ⟨y⟩)/t = νκ(a) + O(ν^{3/2}) uniformemente | OK |
| T1.9 | Passo B, pesi: W_± = e^{−(Φ(a±)−m)/2ν}Z_±, Z_± = √(4πνt/J(a±))(1+O(ν^{1/2})) ⇒ log(W₊/W₋) = −Δ/2ν + ½log(J⁻/J⁺) + O(ν^{1/2}) | OK — **ρ = ½log(J⁻/J⁺) esatto** (segno e fattore ½): il pozzo più piatto (J minore) pesa di più. Red team: log(Z₊/Z₋) = ½log(J⁻/J⁺) su pozzi gaussiani esatti; Cole–Hopf completa sul dato asimmetrico (§6) |
| T1.10 | identità (1−σ)κ(a⁻) + σκ(a⁺) − κ(a(x)) = (H−σ)(κ(a⁻)−κ(a⁺)), H = 1_{x>x_i} (Lemma 1(1c): ramo vincente decide il segno di Δ) | OK |
| T1.11 | decadimento: ℓ ≥ 2δ(x−x_i)/(tν) − C per x > x_i (da Δ ≤ −4δ(x−x_i)/t) ⇒ |H−σ| ≤ Ce^{−2δ|x−x_i|/tν}, ∫|H−σ| ≤ Cν | OK |
| T1.12 | separazione: ||A+B| − |A| − |B|| ≤ 2min(|A|,|B|); ∫min(Ce^{−c|x−x_i|/ν}, ν) = O(ν²|log ν|) | OK |
| T1.13 | profilo: x = x_i + νw, Δ_i(x_i+νw)/ν → −D_iw, ℓ → D_iw/2 + ρ_i; dominazione Ce^{−2δ|w|/t} (uniforme in ν ≤ ν₀); DCT | OK (ipotesi della DCT verificate: convergenza puntuale, dominante integrabile indipendente da ν) |
| T1.14 | valore: cambio z = Dw/2 ⇒ 2ν[log(1+e^ρ) + log(1+e^{−ρ})] = 4νlog(2cosh(ρ/2)); indipendente da D_i; ρ = 0 ⇒ 4ν ln 2 | OK (identità (1+e^ρ)(1+e^{−ρ}) = 4cosh²(ρ/2); quadratura per ρ ∈ {0, −0.3035, 0.7, 2}, errore < 10⁻⁸) |
| T1.15 | Passo C: ricomposizione di ν∫|κ(a(x))| su [0,2π] (Σ_t di misura nulla) | OK |
| T1.16 | Passo D: E^add = (u−v) − (h−u₀), ‖h−u₀−νtu₀″‖_∞ ≤ (νt)²‖u₀⁗‖/2; κ → κ − tu₀″(x) limitata; Λ_add ≥ 4 ln 2 > 0 se K ≥ 1 | OK (u₀ ∈ C⁴ serve qui) |
| T1.17 | "Se t > t*, K ≥ 1" (S4T-L2(d)); "t < t* ⇒ (H_t) con K = 0" | OK |
| T1.18 | Stato "CONDIZIONALE[F1, F2]" | **T1-3**: [F2] è DIMOSTRATO (S-CHECK-11, fix F2-1): lo stato corretto è DIMOSTRATO mod [F1] |
| C1.1 | {J ≥ 0} = ∪[2πk ± a_c]; F(a) = a + t sin a crescente su ciascun intervallo; g(t) = a_c + √(t²−1), g(1) = π, g′ = √(t²−1)/t > 0 ⇒ F(a_c) > π | OK (derivata ricontrollata: d/dt arccos(−1/t) = −1/(t√(t²−1))) |
| C1.2 | al più due candidati per x ∈ (−π, π]; Δ(π) = 0 per simmetria; Δ decrescente | OK. **C1-2 (MINOR):** la monotonia di Δ su tutta la sovrapposizione (2π−F(a_c), F(a_c)) non segue dal Lemma 1 (locale) ma dalla stessa formula d'inviluppo Δ′ = −(a₁−a₀)/t < 0, valida ovunque esistano i due rami con J > 0: scriverlo |
| C1.3 | non degenerazione: J = 0 solo in ±a_c, che non è mai minimizzante; J(π∓b) = 1 − t cos b > 0 | OK. **C1-2 (segue):** "t cos b = 1 ⇒ tan b = b impossibile" esclude l'annullarsi; la positività segue per continuità da t ↓ 1 (1 − t cos b ≈ 2(t−1) > 0): una riga |
| C1.4 | ∫t|u₀″(a)|/J(a)²dx = ∫_{−(π−b)}^{π−b} t|sin a|/(1+t cos a)da = 2log((1+t)/(1−t cos b)) (dx = J da) | OK (quadratura indipendente per t = 1.2, 2, 3.7; errore < 10⁻⁹) |
| C1.5 | **(aggiunta, C1-1)** b² = 6(t−1) + O((t−1)²), 1 − t cos b = 2(t−1) + O((t−1)²) ⇒ Λ_smooth(t) = 2log(1/(t−1)) + o(1) | verificato (t = 1.1 … 1.0001: differenza 0.155, 0.016, 0.0016, 0.00016). Quindi la prima metà di OPA-R1 è **dimostrata** per ε sin x |

### 2.2 Rilievi su OPA-T1/C1
- **T1-1 (MAJOR; OVERSTATED + GLOBAL rispetto all'uso "S4T-Q1 risolto"; SCOPE_OVERCLAIM / QUANTIFIER_ERROR).** Il teorema è un limite ν → 0 **a t fissato**; il testo (§1 tabella, r. 12 e r. 41: "l'ordine è esattamente ν, quindi S4T-Q1 è risolto … senza fattore logaritmico") non dice "a t fissato" né "non uniforme in t". Da OPA-T1 + OPA-C1 (C1-1) segue invece, rigorosamente, per u₀ = sin x: limsup_{ν→0} sup_{t∈(1,T]} ν^{-1}‖S(t)u₀ − S_B(t)u₀‖_{L¹} = ∞. Il fattore log non è eliminato: è spostato nella costante Λ(t) ~ 2log(1/(t−t*)). Questo è coerente con Tang–Teng (ν|log ν| uniforme), non in contrasto. La domanda S4T-Q1 come formulata (S4-TERM r. 210) è a t fissato, quindi la risposta resta valida **con la precisazione**. *Fix:* in §1 (riga OPA-T1), nell'enunciato e alla r. 41 sostituire con: "Per ogni t > t* fissato con (H_t): ‖·‖_{L¹} = νΛ(t) + o(ν), cioè Θ(ν) senza fattore logaritmico **a t fissato**; il resto o(ν) e ν₀ dipendono da t; la stima **non è uniforme in t**: Λ(t) → ∞ per t ↓ t* (per ε sin x: Λ(t) = 2log(1/(εt−1)) + 4 ln 2 + o(1)), e limsup_ν sup_{t∈(t*,T]}‖·‖/ν = ∞, in accordo con il tasso uniforme ν|log ν| di Tang–Teng". Stesso testo nelle righe LEDGER di OPA-T1 e S4T-Q1.
- **T1-2 (MINOR; HIDDEN_ASSUMPTION/scope).** (a) "(H_t) è quella minima che usa la prova" (r. 26): non giustificato; sostituire con "un'ipotesi sufficiente". (b) (H_t) è verificata solo per ε sin x (OPA-C1); per il dato asimmetrico è verificata solo numericamente (un solo shock con due minimizzanti, §6). La genericità ("per u₀ generico (H_t) fallisce solo in un insieme discreto di tempi: nascite di shock e collisioni") non è dimostrata: registrarla come APERTA (nuovo **OPA-Q2**). (c) Rischio residuo (3) ("con tre minimizzanti … l'ordine resta ν con la stessa prova"): non scritto ⇒ **congettura**.
- **T1-3 (MINOR; stato).** CONDIZIONALE[F1, F2] → DIMOSTRATO mod [F1], perché [F2] è DIMOSTRATO (S-CHECK-11, F2-1).
- **C1-1 (MINOR; aggiunta).** Aggiungere a OPA-C1 la divergenza dimostrata Λ_smooth(t) = 2log(1/(t−1)) + o(1) (con lo sviluppo di b e di 1 − t cos b) e spostarla da OPA-R1. OPA-R1 resta osservazione solo per il tasso a t = t* (scala di Pearcey) e per i dati generali: nuovo **OPA-Q1** (tasso ai tempi degeneri: t*, nascite e collisioni successive).
- **C1-2 (MINOR).** Vedi C1.2, C1.3.
- Nota (nessun rilievo): le costanti δ, j₀, η, r₀ non sono quantitative; per un enunciato Θ(ν) a t fissato ciò non è un difetto (KA P3: answered). Il resto O(ν^{3/2}) nel profilo (con Δ_i ∈ C²) non è scritto: l'enunciato dice correttamente o(ν).

### 2.3 Acceptance gate (OPA-T1)
(1) Nessun FATAL/CRITICAL aperto. (2) Ipotesi esplicite ((H_t), C⁴, [F1]); scambi giustificati (DCT con dominante, Fubini non usato in modo non banale); applicazioni dei lemmi con ipotesi scaricate (δ, ε₀ = Λδ²/4, ν ≤ ν₀). (3) Dipendenze dei resti: **dichiarate solo dopo T1-1** (dipendenza da t). (4) Controesempi cercati: dato asimmetrico (ρ ≠ 0), ρ estremi, pozzi non simmetrici, t ↓ t*: nessun controesempio all'enunciato a t fissato; controesempio (vero) all'uniformità in t. Gate superato **con T1-1**.

### 2.4 Kill-argument su OPA-T1
Input: `work/CHECK/KA_OPANA_T1_input.md` (CHECK_REQUEST contesto + PROOF_PACKAGE §2 verbatim; per l'arbitrato, appendice con la formulazione verbatim di S4T-Q1). Attacco (Thread 1, subagente fresco): `KA_OPANA_T1_attack.md` — riconosce corretti ρ, la costante di strato, i resti di Laplace e l'integrale di OPA-C1; attacca la conclusione "S4T-Q1 risolto … senza fattore logaritmico": il risultato è puntuale in t, Λ(t) diverge come 2log(1/(t−t*)), il log è spostato nella costante; (H_t) verificata solo per sin x. Arbitrato (Thread 2, subagente fresco): `KA_OPANA_T1_adjudication.md` — P1 (domanda uniforme?) partially (la lettura a t fissato è quella di S4T-Q1, sostenibile se dichiarata), **P2 (overclaim "senza log") still_unresolved, major**, P3 (costanti non quantitative) answered, P4 ((H_t) solo per sin x) partially major, P5 (tempi degeneri) partially minor. **Verdetto calcolato: WARN** (unresolved_major_or_minor). Il mio audit concorda: i punti P1, P2, P4, P5 sono assorbiti dai fix T1-1, T1-2, C1-1; nessun punto tocca la correttezza dell'enunciato a t fissato.

## 3. OPA-L2 e OPA-T2 (priorità 2)
| MC | passo | esito |
|---|---|---|
| L2.1 | (a) ⟨f′,c_n⟩ = [fc_n]₀ᴸ + μ_n⟨f,e_n⟩ = μ_nf_n; ⟨f′,c₀⟩ = (f(L)−f(0))/√L = 0 per f ∈ H¹₀; derivazione termine a termine (convergenza in H¹ per s > 0) | OK (controllo numerico su f = x(1−x)(2−x), 400 modi, errore 4·10⁻¹⁰) |
| L2.2 | (b) su D(A₀): VS₀(s)u₀ = −cS^N(s)u₀′, S₀(s)Vu₀ = −cS^D(s)u₀′; estensione per densità di D(A₀) in H¹₀ (secondo membro lipschitziano in H¹; primo membro continuo in L² per P3-L2(a)) | OK |
| L2.3 | (c) K^N − K^D = (1/L)Σ_{n∈ℤ}e^{−Dμ_n²s}e^{iμ_n(x+y)} = 2Σ_jG_{Ds}(x+y−2jL) (Poisson, periodo 2L) | OK (confronto numerico s = 10⁻³, 0.05, 0.5: errore < 10⁻⁹) |
| L2.4 | (c) "per j ≤ 0 gli intervalli {x+y−2jL} ricoprono (x,∞) senza sovrapposizioni … ∫₀ᴸk_s dy = erfc(x/2√Ds) + erfc((L−x)/2√Ds)" | **ERRORE (L2-1)**: per j ≤ 0 gli intervalli sono (x+2mL, x+(2m+1)L), m ≥ 0: coprono **metà** di (x,∞), con lacune (x+(2m+1)L, x+(2m+2)L); idem per j ≥ 1. Il valore esatto è ∫₀ᴸk_s dy = (S^N−S^D)(s)1 = 1 − S^D(s)1(x) ≤ erfc(x/2√Ds) + erfc((L−x)/2√Ds), con uguaglianza a meno di O(erfc(L/2√Ds)) (termini j = 0,1 completati a semirette). Controprova: x = 0.13, L = D = 1, s = 0.5: 0.99636 contro 1.28087; per s → ∞ il primo → 1, il secondo → 2 |
| T2.1 | (i) |(S^N−S^D)g| ≤ ‖g‖_∞∫k_s dy ≤ ‖g‖_∞[erfc + erfc] (con L2-1 corretto la prova resta identica: usa solo ≤); ∫₀^∞erfc² = (2−√2)/√π; triangolare sui due bordi, ∫s^{1/4} = (4/5)t^{5/4} ⇒ C_* = (8/5)(2(2−√2)/√π)^{1/2} = 1.30082 | OK. **T2-1 (cosmetico):** la tabella §1 e la riga LEDGER dicono 1.31 (maggiorante valido), l'enunciato ≈1.30: uniformare (1.301) |
| T2.2 | (ii) Passo 1: immagini lontane, 0 ≤ r_s ≤ 4Σ_{m≥1}G_σ(2mL) | OK |
| T2.3 | Passo 2: spezzamento di g, b^{(σ)}_γ(x) = σ^{γ/2}β_γ(x/√σ), β_γ ≤ C_γe^{−w²/4} ((w+v)² ≥ w²+v²) ⇒ ‖·‖ ≤ Cσ^{(α+β)/2+1/4} | OK |
| T2.4 | Passo 3: |K^D_{(0,L)} − K_+| ≤ Ce^{−L²/32Dτ} per y ≤ L/2; b^{(σ)}_α(y) ≤ Ce^{−L²/16Dt} per y > L/2 | OK |
| T2.5 | Passo 4: Z^{(D)}(t) = D^{-1}Z^{(1)}(Dt); Z^{(1)}(T)(x) = T^{1+α/2}Z_α(x/√T) (scala parabolica) ⇒ ‖Z^{(D)}(t)‖ = D^{α/2+1/4}t^{5/4+α/2}N_α; 0 ≤ Z_α ≤ Ce^{−x²/4} | OK (esponenti ricalcolati) |
| T2.6 | Passo 5–6: riflessione R commuta con S^D; ⟨Z, RZ⟩ esponenzialmente piccolo ⇒ norma √(γ₀²+γ_L²) | OK |
| T2.7 | positività N_α > 0 (β_α > 0, nucleo di Dirichlet sul semiasse > 0) | OK |
| T2.8 | N₀: trasformata seno di erfc(x/2√s) = √(2/π)(1−e^{−k²s})/k; Ẑ₀; Plancherel e y = k² ⇒ N₀² = (1/π)∫y^{−7/2}(1−e^{−y}(1+y))²dy | OK (ricalcolato a mano; numerica: J = 0.172028, N₀ = 0.234005; N₀ ricalcolato anche per quadratura doppia indipendente nella forma trasformata, §6) |
| T2.9 | (iii) Taylor: α = k−1, β = 1 (u₀ ∈ C^{k+1}), γ_L = (−1)^{k−1}u₀^{(k)}(L)/(k−1)!; potenza D^{k/2−1/4}; errore relativo O(t^{1/2}); dato piatto: O(t^p) ∀p | OK |
| T2.10 | Conseguenze: (1) e₁: 2|c|√J κ^{1/4}/L = costante di S-CHECK-5; (2) x²(L−x)²: k = 2, costante |c|N₁D^{3/4}2√2L²; (3) somme di seni con u₀′(0) = u₀′(L) = 0 ⇒ k ≥ 3 dispari, ordine ≥ 9/4 | OK (e₁ con L = 1: 2πN₀ = 1.47030; (3): derivate pari dei seni nulle ai bordi) |

Rilievi: **L2-1 (CRITICAL locale per tassonomia: INVALID + LOCAL; impatto a valle nullo).** Formula falsa come uguaglianza e frase "ricoprono (x,∞) senza sovrapposizioni" falsa. *Fix:* "(c) … e ∫₀ᴸk_s(x,y)dy = 1 − S^D(s)1(x) ≤ erfc(x/2√Ds) + erfc((L−x)/2√Ds) (per j ≤ 0 gli intervalli {x+y−2jL : y ∈ (0,L)} sono disgiunti e contenuti in (x,∞); per j ≥ 1 in (−∞, x−L))". OPA-T2(i) usa solo "≤": invariato. Nessun altro uso dell'uguaglianza nei Passi 1–6 (ho controllato: Passo 1 usa la serie, non l'integrale). **T2-1** cosmetico.

## 4. OPA-L3..L5, OPA-T3, OPA-P3 (priorità 3)
| MC | passo | esito |
|---|---|---|
| L3 | E^add(u_ζ) = e^{at₀}G_ζ(t−t₀)e^{ζx} (P1-T2(iii)); ‖u_ζ‖²_{H^m} ≤ C(1+|ζ|)^{2mK}∫_Ie^{2Re a t}·∫_Je^{2Re ζx} | OK |
| L4.1 | eccezioni: Re(γe^{ieθ}) = 0 in 2e angoli; e_{qq′} ≥ 1 per (ND) ⇒ g(r) ≥ c′r | OK |
| L4.2 | (i): |G(s)| ≥ ½e^{sρ_*} per s ≥ s_r; finestra [(T+t₀)/2, T] ammessa se s_r ≤ (T−t₀)/2; ∫ ≥ e^{2(T−t₀)ρ_*}/(4ρ_*) ⇒ costante 1/16; denominatore ≤ C(1+r)^{2mK}Te^{2ρ_aT}; esponente 2(T−t₀)(ρ_*−ρ_a) ≥ 2(T−t₀)c′r | OK |
| L4.3 | (ii) simmetrico per s < 0 (domina il fondo); esponente 2t₀(|ρ_•|−|ρ_a|), |ρ_•|−|ρ_a| = ρ_a − ρ_• ≥ c′r | OK |
| L5 | caso d ∤ e: ∫_Pe^{ieθ} = (2/e)sin(eπ/2d)e^{−ie arg α/d}Σ_ke^{2πiek/d} = 0 ⇒ f ≥ 0 su P impossibile; e = jd, j ≥ 2: immagine di un arco aperto di lunghezza π tramite w^j ha lunghezza ≥ 2π; e = d: semicirconferenze né uguali né opposte se β ∉ ℝα | OK (formula dell'integrale ricalcolata; red team: 300 coppie casuali (d,e,α,β), incluse le eccezioni, nessuna discordanza) |
| T3(a) | θ ∈ Θ₊ ⇒ Re a → +∞ e Re(a_n − a) = −Re b_n → +∞ ⇒ q^{top} ≠ a (t₀ < T); Θ₋ per t₀ > 0; Θ_± aperti ⇒ si evita l'insieme finito di L4 | OK |
| T3(b) | (ND) per monomi distinti di grado ≥ 1; b_N di grado l_{N−1} ∈ [1, d) ⇒ e_N ≠ d ⇒ (S) | OK |
| T3(c) | caratterizzazione di ¬(S): entrambe le direzioni; Σθ_n = 1 e almeno due termini di grado d | OK (direzione ⇐ ricontrollata: deg a_n < d ⇒ β_n = α; deg a_n = d, θ_n < 1 ⇒ β_n = (1−θ_n)α) |
| T3(e) | rami ζ_k(iy) (2d direzioni a passo π/d); Re a = 0 ⇒ Re a_n = Re c_n; esistenza di un ramo con Re c_n → ±∞ (altrimenti e^{ieπ/d} reale ⇒ d | e, impossibile per 1 ≤ e < d); grappolo in cima con Re-differenze limitate e Im-differenze divergenti ((ND)); sup_{I′}|b| ≥ c (termini incrociati O(1/|Im(q−q′)|)); [Naz] con E = {|b| < ε} di misura ≥ metà finestra ⇒ ε ≥ c/poly(ρ_*); denominatore = T | **riduzione corretta**. **T3e-1 (MINOR, scrittura):** dire esplicitamente (1) che le Re-differenze tra elementi di 𝒬° lungo il ramo hanno sviluppo in potenze di |y|^{1/d}, quindi sono o limitate (grappolo) o ≥ c|y|^{1/d} (gap): è ciò che rende ben definito il grappolo; (2) che il numero di esponenti n in [Naz] è ≤ |𝒬°| (fisso) e che max|Re λ_k| sul grappolo è limitato, così il fattore e^{|I′|max|Re λ|} è una costante. Stato: CONDIZIONALE[Naz] (enunciato e costante da CIT-AUDIT) |
| P3(i) | e^{sa_n(∂)} = e^{sκ_n}e^{sθ_na(∂)} (P1-L2(a)); P1-T2(i) con τ = θ_n(t−t₀); formula di E^add; ∫_I‖u(t₀+θ(t−t₀))‖² ≤ |θ|^{-1}‖u‖²; traccia u(t₀) via P1-L1(d) | OK |
| P3(TC) | equivalenza: θ ∈ (0,1] sempre; θ > 1 mai; θ = −μ < 0 ⟺ μT/(1+μ) ≤ t₀ ≤ T/(1+μ) (estremi t = 0 e t = T) | OK (ricontrollata) |
| P3(ii) | gruppo estremo con fattore fisso b(s) analitico non nullo (zero d'ordine finito), gruppi a distanza ≥ c|λ|; quattro casi di esponente: 2λ(θ_max−1)(T−t₀), 2T|λ|(θ_max−1) (t₀ = T), 2|λ|(|θ_min|(T−t₀)−t₀), 2λ(t₀(1+|θ_min|)−T) | OK (ciascun caso ricalcolato; red team numerico sui casi di op_q3 con peso H¹, §6) |

Nessun rilievo oltre T3e-1. Nota di portata (non un rilievo): l'Osservazione sui termini costanti (r. 181) è dichiarata "non scritta": resta fuori dagli enunciati.

## 5. OPA-P4 (priorità 4)
| MC | passo | esito |
|---|---|---|
| P4.1 | decomposizione E^mult − E^{(1)} = [S − S₀ − S^{(1)}]u₀ − S₀[S₂u₀ − u₀ − tVu₀] | OK (algebra ricontrollata con S₀S₂ = S₀ + S₀(S₂ − 1)) |
| P4.2 | ‖∂S^D(r)‖ ≤ sup_μ μe^{−Dμ²r} = (2eDr)^{−1/2} | OK |
| P4.3 | induzione: ‖S^{(j)}(τ)‖ ≤ (a√π)^jτ^{j/2}/Γ(j/2+1) via B((j+1)/2, 1/2) | OK |
| P4.4 | primo fattore su u₀: ‖VS₀(r)u₀‖ = |c|‖S^N(r)u₀′‖ ≤ |c|‖u₀′‖ (OPA-L2(a)) ⇒ ‖S^{(j)}(t)u₀‖ ≤ C_j t^{(j+1)/2}; somma j ≥ 2 = O(t^{3/2}) (serie di tipo Mittag-Leffler) | OK (dipende da P3-T1(b): serie di Dyson a ε = 1, DIMOSTRATO) |
| P4.5 | inflow: x > ct Taylor (ct)²‖u₀″‖/2; x < ct: |u₀(x)| ≤ ct‖u₀′‖ (u₀(0) = 0) ⇒ 2(ct)^{3/2}‖u₀′‖ in L² | OK |
| P4.6 | corollario: errore relativo O(t^{1/2}) + O(t^{1/4}) | OK |
| P4.7 | ostruzione residua (dati compatibili): inflow O(t^{5/2}) con u₀′(0) = 0; cancellazione solo all'ordine dominante; congettura Θ(t^{k/2+3/4}) | coerente; correttamente APERTO/congettura |
Nessun rilievo. Red team: serie modale completa a ε = 1 (expm della matrice troncata) per u₀ = x(1−x), §6.

## 6. Red team (audit_opana.py → audit_opana.out)
**Esito: 53/53 OK** (run per sezioni con timeout: `audit_opana_{A,BCDE,F,G,H}.out`, concatenati in `audit_opana.out`; un primo run unico fu interrotto, exit 120, prima di finire: rieseguito per parti; nessun processo altrui toccato). Due controlli iniziali falliti per errori **miei** nello script (formula sbagliata dei coefficienti seno di x²(1−x)²; estrapolazione con resto ν^{1/2} invece di ν) sono stati corretti (coefficienti da SymPy: 2(24−2π²n²)/(πn)⁵, n dispari) e rieseguiti.
- **A. Cole–Hopf indipendente** (quadratura di Laplace esatta per ogni x, griglia in x raffinata sullo shock; S_B via Newton sul ramo). sin x, t = 2: ‖u−v‖₁/ν = 3.98839, 3.98561, 3.98431 (ν = 2, 1, 0.5·10⁻³), Richardson **3.98301** vs predetto **3.98281**; ‖E^add‖₁/ν = 9.88773, 9.89592, 9.90011 → **9.90430** vs **9.90409**. Dato asimmetrico sin x + 0.3cos 2x, t = 1.5: un solo shock per periodo (x_s = 3.16755, J⁻ = 1.02977, J⁺ = 1.88947, ρ = −0.30348, D = 1.93187); ‖u−v‖₁/ν → **4.66687** vs **4.66669**; ‖E^add‖₁/ν → **11.74559** vs **11.74738** (costante Λ_add del dato asimmetrico non riportata da OP-ANA: verificata qui per la prima volta). Il resto osservato è O(ν²) nella norma (differenze successive dimezzate), meglio dell'o(ν) dichiarato. Quindi il termine log cosh con ρ ≠ 0 e il segno di ρ sono confermati.
- **B. Strato:** 2∫|H − L(z+ρ)| = 4log(2cosh(ρ/2)) per ρ ∈ {0, −0.3035, 0.7, 2} (errore < 10⁻¹⁰); indipendenza da D; log(Z₊/Z₋) = ½log(J⁻/J⁺) su pozzi gaussiani.
- **C. Lemma 2(ii):** |⟨z⟩ + εq/2p²|/ε^{3/2} limitato (decrescente) su tre ψ di prova.
- **D. OPA-C1:** forma chiusa = quadratura (t = 1.2, 2, 3.7); Λ_smooth(t) − 2log(1/(t−1)) = 0.155, 0.016, 0.0016, 0.00016 per t − 1 = 10⁻¹…10⁻⁴ (C1-1); F(a_c) > π.
- **E. OPA-L2:** ⟨f′,c_n⟩ = μ_nf_n; nucleo = immagini (s = 10⁻³, 0.05, 0.5); ∫k_s dy = 1 − S^D1 ≤ erfc + erfc sempre, **uguaglianza falsa** a s = 0.5 (0.99636 contro 1.28087; L2-1).
- **F. OPA-T2:** J = 0.172028, N₀ = 0.234005 = √(J/π); N₁ = 0.162622 (quadratura doppia indipendente, forma trasformata seno con Dawson); **N₂ = 0.203448** (nuovo); C_* = 1.30082; serie modale indipendente (3000 modi, matrice V_mn = −4cmn/(m²−n²)): e₁ → 1.47023 vs 2πN₀ = 1.47030; x²(1−x)² → 0.45996 vs N₁√8 = 0.45996; **k = 3** (sin πx − sin 3πx/3, t^{9/4}): 35.6525 (estr. 35.6820) vs N₂·√2·8π³/2 = 35.6844 — l'esponente 9/4 e la costante di (iii) con (k−1)! sono confermati; stima uniforme (i) verificata.
- **G. OPA-L5/T3/P3:** 300 casi casuali del lemma di Fourier, nessuna discordanza; crescita di log R² (peso H¹, m = 1, K = d) lungo il raggio migliore per AD (ξ, ξ²) e (iξ³, ξ², −2ξ) per t₀ ∈ {0, 0.5, 1}; proporzionali: limitati esattamente quando (TC) vale (θ = (½,½); (−0.3, 0.6, 0.7) a t₀ = 0.5), illimitati altrimenti ((2,−1); (−0.3, 1.3); (−0.3, 0.6, 0.7) a t₀ = 0.1, 0.9). (L'etichetta "L2/L2" nello script è impropria: il rapporto usa il peso H¹.)
- **H. OPA-P4** (ε = 1, expm della matrice troncata a 700 modi, trasporto con inflow proiettato): ‖E^mult − E^{(1)}‖/t^{3/2} = 0.063, 0.058, 0.048, 0.038 (limitato); ‖E^mult‖/t^{5/4} = 0.247, 0.286, 0.306, 0.317 → N₀√2 = 0.331 con correzione O(t^{1/4}) visibile; sup_μ μe^{−Dμ²r} ≤ (2eDr)^{−1/2}.

## 7. Fix richiesti (riepilogo)
| ID | severità | dove | testo |
|---|---|---|---|
| **T1-1** | MAJOR (portata; KA WARN) | PROOF_PACKAGE §1 r. 12, §2 r. 41, §6 righe OPA-T1 e S4T-Q1 | "a t fissato; non uniforme in t; Λ(t) → ∞ per t ↓ t* (ε sin x: 2log(1/(εt−1)) + 4 ln 2 + o(1)); limsup_ν sup_{t∈(t*,T]}‖·‖/ν = ∞, coerente con Tang–Teng" |
| T1-2 | MINOR | §2.0 r. 26, Rischi r. 89 | "(H_t) sufficiente" (non "minima"); genericità di (H_t) APERTA (OPA-Q2); punti tripli = congettura |
| T1-3 | MINOR | §1, §6 | stato: DIMOSTRATO mod [F1] ([F2] è DIMOSTRATO) |
| C1-1 | MINOR | OPA-C1, OPA-R1 | aggiungere la divergenza dimostrata; OPA-R1 ridotta al tasso a t = t* e ai dati generali (OPA-Q1) |
| C1-2 | MINOR | prova di OPA-C1 | monotonia di Δ su tutta la sovrapposizione via inviluppo; positività di 1 − t cos b per continuità |
| **L2-1** | CRITICAL locale (impatto a valle nullo) | OPA-L2(c) e sua prova | "∫₀ᴸk_s dy = 1 − S^D(s)1 ≤ erfc + erfc"; correggere la frase sulle immagini |
| T2-1 | cosmetico | §1, §6 | C_* = 1.301 ovunque |
| T3e-1 | MINOR | prova di OPA-T3(e) | dicotomia limitato/gap delle Re-differenze; n e max|Re λ| fissi in [Naz] |

## 8. Esito sui problemi aperti
- **S4T-Q1** → **CHIUSO a t fissato** sotto (H_t): ‖E_int^{A9}(t)‖_{L¹} = Θ(ν), costante Λ_add(t) esplicita (DIMOSTRATO mod [F1]); **non uniforme in t** (T1-1). Restano APERTI: OPA-Q1 (tasso ai tempi degeneri, t* incluso), OPA-Q2 (genericità di (H_t)).
- **P3-Q-bordo** → **CHIUSO** (OPA-T2, dati lisci e con asintotica a potenza; t^{7/4} di x²(L−x)² DIMOSTRATO; P3-T3(iii)(c) migliorato a O(t^{9/4})).
- **P1-Q6** → **CHIUSO** per monomi distinti (OPA-T3(b)) e sotto (S); eccezione proporzionale caratterizzata (OPA-P3); classe (F) non proporzionale CONDIZIONALE[Naz].
- **P1-Q5** → **CHIUSO** per dati con pendenza al bordo non nulla (OPA-P4); dati compatibili APERTO.
