# AUDIT C12-T1′ (+ C12-L1′, C12-L2′, C12-P10): scomposizione per fattori su Ω semplicemente connesso e sua necessità
Revisore: S-CHECK-3B (3ª tornata, parte B) · 25/10/2026
Fonte esaminata: SOLO `work/C1C2/CHECK_REQUEST_2.md` (§0–§5). `work/C1C2/PROOF_PACKAGE.md` **non è stato letto**, né per intero né per riferimenti puntuali. Lemmi usati come dati: C12-L1, L2, L3, T1 (DIMOSTRATO, AUDIT_C12-T1.md).
Skill caricate (lettura dei SKILL.md, nessuno script _vendor eseguito): skills-local/session-protocol (per prima), skills-local/claim-lifecycle, proof-checker (il reviewer sono io: Phase 0.5 enunciati canonici e micro-claim, checklist A–H, Phase 1.5 red team, severità a due assi, acceptance gate; niente Codex/LaTeX), scientific-critical-thinking (mostrato vs affermato; stato proporzionato), sympy.
SymPy/mpmath: `work/CHECK/sympy/audit_c12_t1prime.py` → `audit_c12_t1prime.out`, **ESITO: 29/29 OK** (.venv -I). Avvertenza: i controlli c1, c2 sono solo di coerenza (banali); i controlli L1p-4..6 verificano l'algebra dell'incollamento con funzioni simboliche generiche, non l'analisi distribuzionale.
Ricerca bibliografica: una ricerca web per verificare Rudin RCA Thm 13.11 **non ha dato conferma** (nessuna fonte che riporti il testo del teorema col numero). Il numero resta non verificato (fix P10-1).

## 0. Verdetti
| claim | verdetto | stato proposto |
|---|---|---|
| C12-L1′ (c′), (d′) | **PASS-con-fix(L1p-1, L1p-2)** | DIMOSTRATO (ipotesi H¹_dR(Ω)=0; con "semplicemente connesso" via il teorema classico s.c. ⇒ H¹_dR=0) |
| C12-L2′ (1)–(3) | **PASS-con-fix(L1p-1)** | DIMOSTRATO |
| C12-T1′ (i)–(iv) | **PASS** (fix testuale T1p-1 facoltativo) | DIMOSTRATO (Ω ⊂ ℝ² aperto connesso con H¹_dR(Ω)=0, in particolare semplicemente connesso) |
| C12-P10 (a)–(c) | **PASS-con-fix(P10-1, P10-2, P10-3)** | DIMOSTRATO nella forma "∃ γ ⊂ Ω chiuso C¹ a tratti, α ∉ Ω con Ind_γ(α) ≠ 0 ⇒ (a),(b)"; il passaggio "Ω non semplicemente connesso ⇒ tali γ, α esistono" è **CON-FONTE (Rudin RCA 13.11, numero da verificare)** |
| "Conseguenza dichiarata" | PASS-con-fix(P10-1) | CON-FONTE (stessa dipendenza da Rudin); quantificatore su P corretto (∀P dentro la parentesi) |

Nessun rilievo FATAL, CRITICAL o MAJOR. Tutti i rilievi sono MINOR (riferimenti e dettagli di scrittura).

## 1. Enunciati canonici (Phase 0.5)
R = ℂ[τ,ξ]; 𝒜(Ω) ∈ {𝒟′(Ω), C^∞(Ω)}; forme a coefficienti complessi.
- **L1′.** ∀Ω ⊂ ℝ² aperto, ∀(p,q) ∈ ℂ²: (c′) [H¹_dR(Ω)=0 ∧ φ,ψ ∈ 𝒜 ∧ D_xφ = D_tψ] ⇒ ∃w ∈ 𝒜: D_tw=φ, D_xw=ψ. (d′) Ω connesso **non vuoto** ⇒ ker D_t ∩ ker D_x = ℂe.
- **L2′.** ∀Ω aperto connesso non vuoto con H¹_dR(Ω)=0, ∀M R-modulo con dim_ℂ M = n < ∞: Ext¹_R(M,𝒜)=0; dim Sol_𝒜(M) = n; ϱ: Sol_{C^∞(ℝ²)}(M) → Sol_𝒜(M) (restrizione) è biiettiva.
- **T1′.** Stesse ipotesi su Ω; P = c∏Q_j non costante: (i) ker P = Σ ker Q_j; (ii) dim ker Σ = δ(P), componenti EP; (iii) unicità ⟺ δ=0 ⟺ V(Q_i)∩V(Q_j)=∅ ∀i≠j; (iv) u ∈ C^∞ ⇒ ogni scomposizione in 𝒟′ è liscia.
- **P10 (forma auditata).** ∀Ω aperto connesso, [∃γ ⊂ Ω cammino chiuso C¹ a tratti, ∃α ∈ ℂ∖Ω con Ind_γ(α) ≠ 0] ⇒ (a) per P = τ²+ξ² (e per ogni twist (τ−p)²+(ξ−q)²) ∃u ∈ ker_{C^∞(Ω)}P con u ∉ ker_{𝒟′}Q_1 + ker_{𝒟′}Q_2; (b) per P = τξ ∃u ∈ ker_{𝒟′(Ω)}P con u ∉ ker_{𝒟′}∂_t + ker_{𝒟′}∂_x. (c) Per Ω = D* (disco bucato) e P = τξ, T1(i) vale in C^∞. La premessa tra parentesi quadre equivale a "Ω non semplicemente connesso" per Rudin RCA 13.11 ((b)⟺(c) della lista).
- **Quantificatore su P (domanda C12-Q6).** P10 è **esistenziale in P**: per ogni Ω non s.c. esiste un P (il Laplaciano) per cui T1(i) fallisce, in C^∞ e in 𝒟′. Non dice che T1 fallisce per ogni P: (c) mostra che per τξ in C^∞ sul disco bucato T1(i) vale. La "Conseguenza dichiarata" ha "per ogni P" dentro la parentesi ed è quindi coerente. Così scritta, P10 è corretta e non contraddice C12-Q6, che resta un problema APERTO legittimo (dipendenza da P e da 𝒜 per Ω fissato: τξ in C^∞ fallisce sulla corona (O-1) e vale sul disco bucato (c)).

## 2. Dipendenze (DAG, nessun ciclo)
L1′ ← L1(c),(d) [rettangoli], partizione dell'unità, proprietà di fascio di 𝒟′; per "s.c." in luogo di H¹_dR=0: teorema classico s.c. ⇒ H¹_dR=0.
L2′ ← L1′, Koszul, successione lunga dell'Ext (Weibel 2.7.6), L2 su ℝ² (= rettangolo illimitato), analiticità degli EP.
T1′ ← L2′(1)–(3), L3 (puramente algebrico).
P10 ← (M) mollificazione, calcolo esplicito, H¹_dR(ℝ²∖B̄) = ℂ[dθ_α] (classico), Rudin 13.11 solo per tradurre "non s.c." nella premessa con l'indice.
Nessun riferimento in avanti; P10 non usa T1′ e viceversa.

## 3. Micro-claim ed esiti per passo
### C12-L1′
| MC | passo | esito |
|---|---|---|
| L1′.0 | twist con e: moltiplicazione per e = e^{pt+qx} biiettiva su 𝒜 (e liscia, mai nulla); D_t(ev) = e∂_tv | OK |
| L1′.C∞ | caso C^∞: η = φ̃dt + ψ̃dx chiusa ⇒ esatta per definizione di H¹_dR=0 | OK (forme complesse: parte reale e immaginaria separatamente) |
| L1′.1 | ricoprimento con quadrati a lati paralleli, chiusura in Ω; partizione dell'unità numerabile localmente finita subordinata | OK nel contenuto; numero "Hörmander ALPDO I Thm 1.4.5" non verificato → **L1p-2** (non portante: risultato standard) |
| L1′.2 | w_j ∈ 𝒟′(U_j) da L1(c) con p=q=0; U_j∩U_k è un rettangolo aperto (quindi connesso), ∇(w_j−w_k)=0 ⇒ w_j−w_k = c_jk per L1(d) | OK. La scelta di quadrati assi-paralleli serve proprio a rendere le intersezioni rettangoli, cioè domini di L1 |
| L1′.3 | χ_jw_j ∈ ℰ′(U_j) esteso per zero; somma localmente finita | OK |
| L1′.4 | **buona definizione e liscezza di h_k (punto da verificare (a))**. Su U_k: w_k = Σ_jχ_jw_k (Σχ_j = 1, somma localmente finita), quindi w−w_k = Σ_jχ_j(w_j−w_k), dove ogni addendo è in 𝒟′(U_k). I due aperti U_j∩U_k e U_k∖suppχ_j ricoprono U_k perché suppχ_j ⊂ U_j; sul primo l'addendo vale χ_jc_jk, sul secondo 0; sull'intersezione (U_j∩U_k)∖suppχ_j entrambe sono 0. Per la proprietà di fascio l'addendo è la funzione liscia h_jk; la somma è localmente finita ⇒ h_k ∈ C^∞(U_k) | **OK** (verifica algebrica in L1p-4: h_1 = Σ_jχ_j(c_j−c_1)) |
| L1′.5 | a = −∂_th_k, b = −∂_xh_k su ogni U_k ⇒ a, b ∈ C^∞(Ω) (fascio); ∂_xa−∂_tb = 0 (le derivate distribuzionali commutano); a dt + b dx = dg, g ∈ C^∞(Ω) | OK (L1p-5, L1p-6) |
| L1′.6 | w̃ = w+g: ∂_tw̃ = φ̃, ∂_xw̃ = ψ̃ | OK |
| L1′.d | (d′): costanti locali c_U ben definite, localmente costanti, Ω connesso ⇒ costante; fascio ⇒ w̃ = c | OK; serve Ω **non vuoto** per avere dimensione 1 → **L1p-1** |

**Dove serve davvero la semplice connessione.** Solo nel passo (5), e solo nella forma H¹_dR(Ω)=0 per forme **lisce**. I passi (1)–(4) e la verifica di chiusura in (5) valgono su ogni aperto (l'Osservazione "non usata" del testo è corretta): ogni 1-forma distribuzionale chiusa è coomologa a una forma liscia chiusa. Con un'osservazione in più (una h ∈ 𝒟′ con dh liscia è liscia: localmente h = primitiva liscia + costante per L1(d)) si ottiene anche l'iniettività, quindi Ext¹_R(R/𝔪,𝒟′(Ω)) ≅ Ext¹_R(R/𝔪,C^∞(Ω)) ≅ H¹_dR(Ω) su **ogni** aperto piano. Questo chiude in modo elementare il punto lasciato come schizzo in O-2 (AUDIT_C12-T1 §6), senza de Rham per le correnti. La connessione serve solo in (d′), quindi per il conteggio delle dimensioni in L2′(2) e T1′(ii). Controllo: L1p-7, L1p-8 (dθ chiusa con periodo 2π: è esattamente il passo (5) a fallire sulla corona).

**Punto da verificare (b), equivalenze topologiche.**
- s.c. ⇒ H¹_dR(Ω)=0: classico (invarianza omotopica degli integrali di linea delle forme chiuse; un primitivo si definisce integrando lungo cammini). Riferimento: J. M. Lee, *Introduction to Smooth Manifolds*, 2ª ed., cap. 11 (forme chiuse ed esatte; il numero esatto del teorema non è verificato qui) → **L1p-2**. È l'unica direzione usata da T1′.
- Viceversa per aperti piani connessi: H¹_dR(Ω)=0 ⇒ (per ogni γ chiuso in Ω e α ∉ Ω, dθ_α = Im(dz/(z−α)) è chiusa su Ω, quindi esatta, quindi ∮_γdθ_α = 2π·Ind_γ(α) = 0) ⇒ condizione (c) di Rudin ⇒ s.c. (Rudin, (c) ⇒ (b)). La prima implicazione è elementare; la seconda dipende da Rudin 13.11 → **P10-1**.

### C12-L2′
| MC | passo | esito |
|---|---|---|
| L2′.i | M = R/𝔪: Hom = ker β* = ℂe (L1′(d′)); Ext¹ = ker α*/im β* = 0 (L1′(c′); ker α* = {D_xφ = D_tψ}) | OK |
| L2′.ii | induzione su n: autovettore comune v di τ, ξ (operatori commutanti su M ≠ 0 di dimensione finita); S ≅ R/𝔪_{(p,q)}; successione lunga; dim Hom(M) = (n−1)+1 | OK (caso n=0 banale, n=1 = caso (i)) |
| L2′.iii | ℝ² = I×J con I=J=ℝ (L1, L2 valgono "anche illimitato", audit 2C); ϱ R-lineare; iniettiva: per ogni m, φ_0(m) è EP nullo sull'aperto non vuoto Ω ⇒ nullo (analiticità reale su ℝ² connesso); dim n = n ⇒ biiettiva; unicità di φ_0 = iniettività | OK; Ω ≠ ∅ necessario → **L1p-1** (controllo L2p-1) |

Osservazione: (1) e (2) non usano ℝ²; solo (3) usa L2 su ℝ².

### C12-T1′
| MC | passo | esito |
|---|---|---|
| T1′.1 | successione esatta 0 → R/(fg) → R/(f)⊕R/(g) → R/(f,g) → 0, Hom(R/(h),𝒜) = ker_𝒜 h(∂): algebra, indipendente da Ω | OK |
| T1′.2 | Ext¹(R/(f,g),𝒜) = 0 (L3 + L2′(1)) ⇒ Σ suriettiva; ker Σ ≅ Sol(R/(f,g)), dimensione da L2′(2) | OK |
| T1′.3 | induzione su s: s=2 applicato a f=Q_1, g=P′ (serve solo la coprimalità); dim ker(Σ_2∘B) = dim ker B + dim ker Σ_2 con B suriettiva; additività L3(b) | OK |
| T1′.4 | componenti di 𝒩: w_j ∈ Sol(R/(Q_j,∏_{i≠j}Q_i)), modulo di dimensione finita ⇒ EP (L2′(3)) | OK |
| T1′.5 | (iii) da L3(c) (con il fix L3-1 già recepito); (iv) scomposizione liscia da (i) in C^∞ + 𝒩_{𝒟′} fatto di EP (lisci) | OK |
| T1′.6 | **punto da verificare: la prova non usa altro su Ω oltre L2′(1)–(3)** | **OK**: ho controllato riga per riga; gli altri ingredienti (UFD, L3, successioni esatte, aritmetica delle dimensioni) sono puramente algebrici |

Red team sulle ipotesi: (a) "connesso" non serve per (i) (vale componente per componente) ma serve per (ii): su Ω con k componenti s.c. la dimensione di 𝒩 è k·δ(P), e infinita se le componenti sono infinite. L'enunciato ha "connesso": corretto. (b) H¹_dR=0 è necessaria per "ogni P" (P10) ma non per ogni P fissato (C12-Q6). Fix testuale facoltativo **T1p-1**.

### C12-P10
| MC | passo | esito |
|---|---|---|
| P10.0 | premessa: γ chiuso C¹ a tratti, α ∈ ℂ∖Ω, Ind_γ(α) ≠ 0, da Rudin 13.11 (negazione di (c), con α ≠ ∞ perché Ind_γ(∞) = 0 per convenzione) | contenuto OK secondo la mia conoscenza del teorema (lista di condizioni equivalenti per regioni piane: omeomorfa al disco, s.c., Ind_γ(α)=0 ∀α ∈ S²∖Ω, S²∖Ω connesso, …); **numero non verificato** → **P10-1** |
| P10.M | (M): η = dh, h ∈ 𝒟′(Ω); per ε < ½dist(γ,∁Ω) (∁Ω ≠ ∅ perché α ∉ Ω), η_ε = η∗ρ_ε = d(h∗ρ_ε) è liscia su Ω_ε ⊃ intorno di γ; ∮_γ di una forma esatta liscia = 0 | OK. Con il mollificatore prodotto di (b) il supporto ha semidiagonale √2ε < dist(γ,∁Ω), anche questo garantito da ε < ½dist: OK |
| P10.a1 | u = log|z−α|² ∈ C^∞(Ω), Δu = 0; Q_1 = 2∂_z, Q_2 = 2∂_{z̄}; Q_2u = 2/w con w = z̄−ᾱ | OK (a1–a3) |
| P10.a2 | u = h+k ⇒ Q_2h = F, ∂_th = F/2 = 1/w, ∂_xh = F/(2i) = −i/w, dh = dw/w (liscia, chiusa) | OK (a4–a6) |
| P10.a3 | η_ε → η uniformemente su γ (η continua) ⇒ ∮_γ dw/w = 0; ma ∮_γ dw/w = conj(∮_γ dz/(z−α)) = −2πi·n ≠ 0. **Segno e orientazione corretti** | OK (a7: −2πi sul cerchio antiorario in z = t+ix) |
| P10.a4 | versione torta: [(τ−p)∓i(ξ−q)](∂)(ev) = eQ_{1,2}(∂)v; prodotto = (τ−p)²+(ξ−q)²; la scomposizione di eu dà, dividendo per e, quella di u | OK (a8–a10); dim R/(Q_1,Q_2) = 1 (a11) |
| P10.b1 | u = H(x−x₀)H(t−t₀) ∈ L¹_loc; ∂_t∂_xu = δ_α in 𝒟′(ℝ²), quindi = 0 in 𝒟′(Ω) | OK (b6) |
| P10.b2 | u = A+B ⇒ dB = φ dt, φ = ∂_tu = H(x−x₀)δ(t−t₀)|_Ω; vicino a γ, η_ε coincide con ω_ε = H_ε(x−x₀)ρ_ε(t−t₀)dt (mollificazione del dato globale ristretta, perché il supporto del mollificatore attorno ai punti vicini a γ sta in Ω) | OK; l'identificazione "mollificato del ristretto = ristretto del mollificato su Ω_ε" non è scritta → **P10-2** |
| P10.b3 | dω_ε = ρ_ε(x−x₀)ρ_ε(t−t₀) dx∧dt, supportata in α+[−ε,ε]² ⇒ ω_ε chiusa su E = ℝ²∖B̄(α,r) per √2ε < r < dist(α,γ) | OK (b5) |
| P10.b4 | ∮_{C_{r′}}ω_ε = −1 sul cerchio antiorario (solo l'arco alto contribuisce, H_ε = 1 e t decresce; in basso H_ε = 0) | **OK, segno verificato** (b1 = −1.0 con bump C^∞ e mpmath; b4 cerchio decentrato −1; b3 non circondante 0) |
| P10.b5 | H¹_dR(E) = ℂ[dθ_α] ⇒ ∮_γω_ε = (−1)·Ind_γ(α) = −n ≠ 0, contro (M) | OK (b2: Ind 2 dà −2); fatto classico non citato → **P10-3** |
| P10.c | D*: ∂_x(∂_tu) = 0; fette {t = t₁} connesse per t₁ ≠ 0; in t = 0 il valore è il limite, indipendente da x₁; g liscia (localmente g(t) = φ(t,x₁) con x₁ ≠ 0, t*²+x₁² < 1); B = ∫₀ᵗg, A = u−B lisce | OK (c1 controllo banale della costruzione) |
| P10.coh | (c) e (a) riguardano operatori diversi; (c) e O-1 (corona) riguardano domini diversi: sul disco bucato il quadrato [−½,½]²∖{0} sta in D*, quindi il controesempio di O-1 non è nel nucleo su D* (c2). Nessuna contraddizione | OK |

## 4. Rilievi e fix (proposti, non applicati ai file di S-C1C2)
- **L1p-1 · CASE_INCOMPLETE · UNCLEAR/COSMETIC · MINOR · STRENGTHEN_ASSUMPTION testuale.** In L1′(d′), L2′ e T1′ scrivere "Ω connesso **non vuoto**". Con Ω = ∅ (connesso per alcune convenzioni), ℂe|_∅ = 0 e dim Sol = 0 ≠ n.
- **L1p-2 · REFERENCE_MISMATCH (possibile) · COSMETIC · MINOR · ADD_REFERENCE.** Hörmander ALPDO I Thm 1.4.5 (partizione dell'unità) e J. M. Lee ISM 2ª ed. (s.c. ⇒ ogni 1-forma chiusa è esatta; precisare che per forme complesse si applica a parte reale e immaginaria): numeri da far verificare a un CIT-AUDIT. Non portanti: entrambi i fatti sono standard e il primo ha prove brevi in ogni testo.
- **P10-1 · REFERENCE_MISMATCH (non verificato) · UNJUSTIFIED/LOCAL→ridotto a COSMETIC con la riformulazione · MINOR · ADD_REFERENCE + WEAKEN/RESTATE.**
  - *Problema.* Il numero "Rudin RCA 3ª ed. Thm 13.11" non è verificabile qui (ricerca web senza conferma). Il contenuto che il testo usa ((b) ⟺ (c) della lista di equivalenze per regioni piane) è quello che ricordo per quel teorema, ma non è un controllo.
  - *Fix.* (1) Enunciare P10 con la premessa autosufficiente "esistono γ ⊂ Ω chiuso C¹ a tratti e α ∉ Ω con Ind_γ(α) ≠ 0": così (a), (b) sono DIMOSTRATO senza fonti. (2) Aggiungere: "per Ω piano aperto connesso questa premessa equivale a 'Ω non semplicemente connesso' [Rudin RCA 3ª ed., Thm 13.11, (b)⟺(c); CIT-AUDIT]" → questa parte è CON-FONTE. (3) Nella "Conseguenza" distinguere le direzioni: T1′ usa solo s.c. ⇒ H¹_dR=0 (classico); H¹_dR=0 ⇒ (Ind ≡ 0) è elementare (dθ_α esatta); (Ind ≡ 0) ⇒ s.c. è Rudin. (4) Mettere Rudin 13.11 in coda al prossimo CIT-AUDIT (già proposto dal coordinatore).
  - *Alternativa senza Rudin (facoltativa).* Formulare tutta la teoria con la condizione topologica "Ind_γ(α) = 0 ∀γ ⊂ Ω, ∀α ∉ Ω" al posto di "s.c.": allora P10 è autosufficiente, ma T1′ richiede la direzione (Ind ≡ 0) ⇒ H¹_dR = 0, che è di nuovo Rudin (o Runge/∂̄ su aperti arbitrari). Non c'è quindi una via del tutto elementare per l'equivalenza completa; le due metà autosufficienti sono T1′ con "H¹_dR=0" e P10 con "∃γ,α".
- **P10-2 · UNPROVEN_SUBCLAIM · COSMETIC · MINOR · ADD_DERIVATION.** In (b) scrivere: per y con dist(y,∁Ω) > √2ε, (φ∗ρ_ε)(y) dipende solo da φ su y+[−ε,ε]² ⊂ Ω, dove φ = (∂_t u_glob)|_Ω; quindi η_ε = ω_ε su un intorno di γ. In (a) dire esplicitamente che η_ε → η uniformemente su γ perché η è continua su Ω e γ è compatto.
- **P10-3 · UNPROVEN_SUBCLAIM · COSMETIC · MINOR · ADD_REFERENCE.** "H¹_dR(E) = ℂ[dθ_α]" per E = ℝ²∖B̄(α,r): classico (E è omotopicamente equivalente a S¹; Lee ISM, coomologia di de Rham di ℝ²∖{0}). Va citato o ridotto: ω_ε + (1/2π)dθ_α è chiusa su E con periodo nullo sul cerchio, quindi esatta. Il valore −n è confermato numericamente (b1–b4).
- **T1p-1 · SCOPE · COSMETIC · MINOR (facoltativo).** Aggiungere a T1′: "(i) non richiede la connessione (vale componente per componente); (ii) sì. La condizione H¹_dR(Ω)=0 è necessaria per 'ogni P' (P10) ma non per un P fissato (C12-Q6; es. τξ in C^∞ sul disco bucato, P10(c))".

## 5. Red team (Phase 1.5) — esito
Script `audit_c12_t1prime.py`, 29/29 OK.
1. **P10(a):** Q_2u = 2/w, gradiente di h = dw/w, chiusura, periodo −2πi sul cerchio antiorario, twist, dim R/(Q_1,Q_2) = 1. Tentativo di rottura: un buco puntiforme (α isolato) va bene, perché u è liscia su Ω = ℝ²∖{α} e γ = cerchio. Nessun controesempio.
2. **P10(b):** periodo di ω_ε calcolato con un bump C^∞ (mpmath, 30 cifre) su quattro cerchi: −1 (antiorario attorno ad α), −2 (due giri), 0 (non circonda α), −1 (decentrato). Il segno "−1" e la formula −n sono corretti. Distribuzionalmente ∂_t∂_x(H⊗H) = δ_α (test con una gaussiana).
3. **L1′ passo (4)–(5):** l'incollamento con primitive locali che differiscono per costanti dà h_1 = Σχ_j(c_j−c_1), a = −∂_th_1, b = −∂_xh_1, forma chiusa (algebra simbolica con χ_j generiche). Contro-test topologico: dθ chiusa con periodo 2π, quindi senza H¹_dR = 0 il passo (5) fallisce, e solo quello.
4. **T1′:** δ calcolate con Gröbner (Laplaciano 1, τξ 1, calore×trasporto 2, tre rette 3), coerenti con l'audit 2C.
5. **L2′(3):** un EP non nullo ha jet non nullo (controllo di non banalità).
6. **Coerenza.** Con O-1 (corona, τξ in C^∞): coerente con (c), perché il disco bucato contiene il supporto di α′β′ meno l'origine. Con C3-L3(e) (ambiguità EP su ogni connesso): coerente. Con II-T3 (caso comassimale su ogni Ω): coerente (M = 0). Con C12-Q6: P10 è esistenziale in P, quindi Q6 resta aperto in modo legittimo.

Nessun controesempio agli enunciati come scritti.

## 6. Portata (scientific-critical-thinking)
- **Dimostrato.** Su ogni Ω ⊂ ℝ² aperto, connesso, non vuoto, con H¹_dR(Ω) = 0 (in particolare s.c.), in 𝒟′ e in C^∞: la scomposizione per fattori, l'ambiguità δ(P) fatta di EP che sono restrizioni di soluzioni globali, l'unicità ⟺ comassimalità a coppie, e la regolarità. Questo sostituisce il CON-FONTE di Malgrange–Ehrenpreis sui convessi con una prova autosufficiente.
- **Dimostrato (necessità).** Se esiste un cammino chiuso in Ω con indice non nullo attorno a un punto fuori da Ω, T1(i) fallisce per il Laplaciano (C^∞ → 𝒟′) e per τξ (𝒟′).
- **CON-FONTE (da verificare).** L'equivalenza di questa premessa con "non semplicemente connesso" (Rudin 13.11), quindi anche la frase "T1 per ogni P ⟺ s.c.".
- **Non affermato e corretto non affermarlo.** Che T1 fallisca per ogni P su Ω non s.c.: falso (P10(c)). La caratterizzazione per P fissato è C12-Q6 (APERTO).
- **Per G★′ punto 2.** La riformulazione proposta da S-C1C2 ("Ω limitato e semplicemente connesso; componenti in 𝒟′; componenti H^m per ogni u ⟺ c_F<1, falso in generale") è coerente con quanto auditato qui e in 2C. La scelta spetta al coordinatore e all'utente.

## 7. Acceptance gate
| condizione | esito |
|---|---|
| 0 FATAL/CRITICAL | ✔ |
| Ipotesi esplicite (H¹_dR=0, connesso non vuoto; premessa con l'indice per P10) | ✔ con L1p-1, P10-1 |
| Ipotesi scaricate a ogni applicazione (L1 su quadrati e intersezioni rettangolari; L2 su ℝ²; L2′ in T1′) | ✔ |
| Controesempi tentati sui lemmi chiave e sui segni | ✔ |
| Nessuna O(·) | ✔ |

**Stati proposti:** C12-L1′, C12-L2′, C12-T1′ **DIMOSTRATO**; C12-P10 **DIMOSTRATO** nella forma con la premessa sull'indice, **CON-FONTE (Rudin 13.11, numero da verificare)** per la traduzione in "non semplicemente connesso" e per la "Conseguenza". Fix MINOR da recepire: L1p-1, L1p-2, P10-1, P10-2, P10-3; T1p-1 facoltativo.
