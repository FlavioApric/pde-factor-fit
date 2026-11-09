# KA input — VAR-T1 (preparato da S-CHECK-F8-VAR, 27/10/2026)

Testo estratto VERBATIM da work/S8-VAR/PROOF_PACKAGE.md (convenzioni, §1.2, §1.3, §1.4, §1.5 e la stima di Cauchy di §7.1 attacco 9). Solo enunciati, ipotesi, prove e lemmi usati. Compito del revisore: kill-argument (trovare un controesempio o un passo falso), con attenzione a VAR-T1(c): la riduzione int Z(u) ≠ ∅ ⇒ fascia di silenzio e la serie di Tychonoff (convergenza, regolarità C^∞ in t = 0, soluzione dell'equazione).

## Convenzioni (PROOF_PACKAGE, preambolo)
**Modelli di dato** (NOTAZIONE v5): DM1 formula/EP, DM2 jet in un punto, DM3 u noto esattamente su Ω, DM-φ dato noto a meno della fase temporale globale (u ~ e^{iθ(t)}u, θ reale), DM-inv dati invarianti di gauge. Ogni enunciato dichiara il suo.

**Convenzioni.** Ω = I × J con I, J intervalli aperti (salvo avviso). L_0 := i∂_t + ∂_x². L'equazione di Schrödinger è iψ_t = −ψ_xx + Vψ, cioè L_0ψ = Vψ. "u ∈ C^{1,2}(Ω)" significa u, u_t, u_x, u_xx continue su Ω. Per V ∈ L^∞_loc l'equazione L_0u = Vu è intesa quasi ovunque (il membro sinistro è continuo). Gli operatori differenziali sono scritti con i coefficienti a sinistra; ∂∘f = f∂ + f′.

### 1.2 [VAR-T1(a)] Famiglie affini: identificazione = iniettività di Φ_u — prova scritta
**Enunciato.** Siano L_0, T_1, …, T_K operatori differenziali su Ω e Θ uno spazio vettoriale di parametri θ = (θ_1, …, θ_K) (θ_k funzioni su Ω, per esempio della sola x). Poniamo L_θ := L_0 + Σ_k θ_kT_k e Φ_u(θ) := Σ_k θ_k(T_ku). Allora l'insieme {θ ∈ Θ : L_θu = 0} è vuoto oppure è θ_0 + ker Φ_u per un qualunque suo elemento θ_0. In particolare θ è identificato da u (nell'insieme delle θ ammissibili per u) se e solo se ker Φ_u = {0}. Su {u ≠ 0} si ha Φ_u(θ) = u·Σθ_kρ_u(T_k), e si ritrova la mappa residuo di NOTAZIONE v5.
**Prova.** L_θu − L_{θ_0}u = Φ_u(θ − θ_0), con Φ_u lineare. ∎
**Modello di dato:** DM3. È la faccia (b′) di N1(vi) (fix F1): la legge esiste sempre se ρ_u(T_k) ≠ 0 per qualche k (non falsificabilità), e θ è identificato ⟺ Φ_u è iniettiva.

### 1.3 Continuazione unica laterale per Schrödinger 1D con potenziale limitato
**[VAR-L1] Lemma (continuazione unica attraverso un grafico) — prova scritta.** Siano Ω ⊂ ℝ² aperto, V ∈ L^∞_loc(Ω) a valori complessi (può dipendere da t), u ∈ C^{1,2}(Ω) con L_0u = Vu q.o. Siano g ∈ C^∞(ℝ) e p_0 = (t_0, g(t_0)) ∈ Ω. Se u = 0 su {(t,x) ∈ N : x < g(t)} per un intorno N di p_0, allora u = 0 in un intorno di p_0.

**[VAR-L0] Lemma di Carleman — prova scritta.** Fissati g ∈ C^∞(ℝ), t_0 ∈ ℝ, a, b > 0, siano s := x − g(t), B := {|t − t_0| ≤ a, |s| ≤ b}, μ := 1/(4b), κ := 1 e
φ(t,x) := −s + μs² − κ(t − t_0)².
Sia C_1 := sup_B (|φ_tt| + φ_xt²/(2μ)). Per λ ≥ λ_0 := (C_1/μ)^{1/2} e per ogni w ∈ C_c(int B) con w_t, w_x, w_xx continue vale
μλ³ ∫ e^{2λφ}|w|² ≤ ∫ e^{2λφ}|L_0w|².
*Prova.* (i) *Identità.* Per z ∈ C_c^∞(int B) poniamo P_λ := e^{λφ}L_0e^{−λφ}. Si calcola P_λ = S + A con
S := ∂_x² + λ²φ_x² + i∂_t (simmetrico in L²(dt dx)), A := −2λφ_x∂_x − λφ_xx − iλφ_t (antisimmetrico).
Allora ‖P_λz‖² = ‖Sz‖² + ‖Az‖² + ([S,A]z, z) e, calcolando il commutatore e integrando per parti (z ha supporto compatto),
([S,A]z, z) = ∫ [4λφ_xx|z_x|² + 4λφ_xt Im(z_x z̄) + (4λ³φ_x²φ_xx − λφ_xxxx + λφ_tt)|z|²] =: q(z).
Dettaglio del commutatore: [∂_x², −2λφ_x∂_x − λφ_xx] = −4λφ_xx∂_x² − 4λφ_xxx∂_x − λφ_xxxx; [∂_x², −iλφ_t] = −iλφ_txx − 2iλφ_tx∂_x; [λ²φ_x², −2λφ_x∂_x] = 4λ³φ_x²φ_xx; [i∂_t, −2λφ_x∂_x] = −2iλφ_xt∂_x; [i∂_t, −λφ_xx] = −iλφ_xxt; [i∂_t, −iλφ_t] = λφ_tt; gli altri commutatori sono nulli. Nella forma quadratica i termini −4λφ_xx∂_x² − 4λφ_xxx∂_x danno 4λ∫φ_xx|z_x|²; i termini −4iλφ_xt∂_x − 2iλφ_xxt danno, separando Re(z_xz̄) = ½(|z|²)_x e integrando per parti, esattamente 4λ∫φ_xt Im(z_xz̄) (le parti immaginarie si cancellano). SymPy `s8_carleman` (a): l'identità è verificata numericamente (scarto relativo < 10⁻¹²) per una φ generica con φ_xt ≠ 0 e φ_xxxx ≠ 0; col segno opposto del termine incrociato fallisce; P_λ = S + A verificato simbolicamente.
(ii) *Stima.* Su B: φ_x = −1 + 2μs ∈ [−3/2, −1/2], quindi φ_x² ≥ 1/4; φ_xx = 2μ; φ_xxxx = 0. Per la disuguaglianza 4λ|φ_xt||z_x||z| ≤ 8λμ|z_x|² + λφ_xt²/(2μ)|z|² il termine incrociato è assorbito da 4λφ_xx|z_x|² = 8λμ|z_x|². Quindi q(z) ≥ ∫(2μλ³ − λC_1)|z|² ≥ μλ³∫|z|² per λ ≥ λ_0. Poiché ‖Sz‖², ‖Az‖² ≥ 0 e z = e^{λφ}w, si ottiene la stima per w ∈ C_c^∞(int B).
(iii) *Densità.* Per w come nell'enunciato, w_ε := w ∗ ρ_ε (mollificatore) ha supporto in int B per ε piccolo, e L_0w_ε = (L_0w) ∗ ρ_ε (le derivate classiche continue coincidono con quelle distribuzionali); w_ε → w e L_0w_ε → L_0w uniformemente con supporti in un compatto fisso; il peso è continuo e limitato su B. Si passa al limite. ∎
SymPy `s8_carleman` (b): per un grafico curvo g = 0.3 sin t e una bolla w, il rapporto ∫e^{2λφ}|L_0w|² / (λ³∫e^{2λφ}|w|²) vale 75–497 ≥ μ = 1/4 per λ = 5…80 (λ_0 = 3.16).

*Prova di VAR-L1.* Scegliamo a, b > 0 con B (come in VAR-L0, centrato in t_0) contenuto in N ∩ Ω. Per s ∈ [0, b] vale μs² ≤ s/4, quindi φ ≤ −(3/4)s − (t − t_0)² su B ∩ {s ≥ 0}. Scegliamo ε > 0 con 8ε/3 < b e (2ε)^{1/2} < a; allora la lente Λ_{2ε} := B ∩ {s ≥ 0, φ ≥ −2ε} è contenuta in {0 ≤ s ≤ 8ε/3, |t − t_0| ≤ (2ε)^{1/2}} ⊂ int B. Sia χ ∈ C^∞(ℝ) con χ = 1 su [−ε, ∞) e χ = 0 su (−∞, −2ε]. Definiamo w := χ(φ)u su B e w := 0 fuori da B. Poiché u = 0 su B ∩ {s < 0}, il supporto di w sta in Λ_{2ε} ⊂ int B; w ha w_t, w_x, w_xx continue. Si ha L_0w = χ(φ)Vu + R con
R := iχ′(φ)φ_tu + χ″(φ)φ_x²u + 2χ′(φ)φ_xu_x + χ′(φ)φ_xxu,
supportato in {−2ε ≤ φ ≤ −ε}. Quindi |L_0w| ≤ ‖V‖_{L^∞(B)}|w| + |R| q.o. Da VAR-L0, per λ ≥ λ_0 con (μλ³)^{1/2} ≥ 2‖V‖_{L^∞(B)}:
½(μλ³)^{1/2}‖e^{λφ}w‖ ≤ ‖e^{λφ}R‖ ≤ e^{−λε}‖R‖_{L²}.
Sia Λ := B ∩ {φ ≥ −ε/2}, che contiene un intorno di p_0 (φ(p_0) = 0). Su Λ ∩ {s ≥ 0} vale w = u, e su Λ ∩ {s < 0} vale u = 0; quindi ‖e^{λφ}w‖ ≥ e^{−λε/2}‖u‖_{L²(Λ)}. Ne segue ‖u‖_{L²(Λ)} ≤ 2(μλ³)^{−1/2}e^{−λε/2}‖R‖_{L²} → 0 per λ → ∞. Dunque u = 0 su Λ. ∎

**[VAR-L2] Globalizzazione — prova scritta.** Ω = I × J, V ∈ L^∞_loc(Ω), u ∈ C^{1,2}(Ω) con L_0u = Vu q.o. Se u = 0 su I × (α, β) per un sottointervallo non vuoto (α, β) ⊂ J, allora u ≡ 0 su Ω.
*Prova.* Trattiamo la propagazione verso destra; quella verso sinistra è simmetrica (x ↦ −x conserva la forma dell'equazione). Sia W := {p ∈ Ω : u = 0 in un intorno di p} (aperto).
Passo 0. Per ogni t_* ∈ I, VAR-L1 con g ≡ β dà (t_*, β) ∈ W. Quindi W ⊃ I × (α, β].
Passo 1. Fissiamo t_1 < t_2 e δ > 0 con [t_1 − δ, t_2 + δ] ⊂ I, e b″ ∈ (β, sup J). Sia T := (t_1 − δ, t_2 + δ) e ψ ∈ C^∞(ℝ) con 0 < ψ ≤ 1 su T, ψ = 1 su [t_1, t_2], ψ(t_1 − δ) = ψ(t_2 + δ) = 0. Per s ∈ [β, b″] poniamo φ_s(t) := β + (s − β)ψ(t) e R_s := {(t,x) : t ∈ T, α < x < φ_s(t)} ⊂ Ω. Gli R_s crescono con s e ∪_{s<s′}R_s = R_{s′}. Sia s* := sup{s ∈ [β, b″] : u = 0 su R_s}; R_β = T × (α, β) ⊂ W, e u = 0 su R_{s*}. Supponiamo s* < b″. Ogni punto (t, φ_{s*}(t)) con t ∈ T sta in W per VAR-L1 (grafico g = φ_{s*} ∈ C^∞, u = 0 dal lato x < g(t) in un intorno, perché quell'intorno interseca {x < g} dentro R_{s*}). I due estremi (t_1 − δ, β), (t_2 + δ, β) stanno in W per il passo 0. La chiusura del grafico è un compatto contenuto nell'aperto W; esiste quindi η > 0 tale che il suo η-intorno sta in W. Per s* < s < s* + η si ha R_s ⊂ R_{s*} ∪ (η-intorno del grafico) (perché φ_s − φ_{s*} = (s − s*)ψ ≤ s − s*), quindi u = 0 su R_s, contro la definizione di s*. Dunque s* = b″ e u = 0 su (t_1, t_2) × (α, b″) (lì φ_{b″} = b″). Facendo tendere t_1 → inf I, t_2 → sup I, b″ → sup J si ottiene u = 0 su I × (α, sup J). ∎


### 1.4 [VAR-T1(b)] Schrödinger con V = V(x): ogni soluzione non nulla identifica V — prova scritta
**Enunciato.** Ω = I × J, V ∈ L^∞_loc(J) (complesso), u ∈ C^{1,2}(Ω) con L_0u = V(x)u q.o., u ≢ 0. Sia X_0 := {x ∈ J : u(t,x) = 0 per ogni t ∈ I}. Allora:
(i) X_0 non ha punti d'accumulazione in J (è discreto e chiuso in J); in particolare int X_0 = ∅ e |X_0| = 0;
(ii) se W ∈ L^∞_loc(J) e L_0u = W(x)u q.o., allora W = V q.o.; se V e W sono continui, W = V ovunque;
(iii) ricostruzione: per ogni x ∈ J ∖ X_0 e ogni t con u(t,x) ≠ 0, V(x) = (iu_t + u_xx)/u (t,x) (per V continuo; per V ∈ L^∞ q.o. in x).
**Modello di dato:** DM3. **Classe:** V(x) ∈ L^∞_loc(J). Il dato può essere non stazionario.
**Prova.** (i) Sia x_0 ∈ J punto d'accumulazione di X_0, x_n → x_0, x_n ∈ X_0 ∖ {x_0}. X_0 è chiuso in J (u continua), quindi x_0 ∈ X_0: u(·, x_0) ≡ 0 e u_t(·, x_0) ≡ 0. Inoltre u_x(t,x_0) = lim (u(t,x_n) − u(t,x_0))/(x_n − x_0) = 0. Infine u_xx(t,x_0) = 0: u_xx è continua e, q.o., u_xx = Vu − iu_t; su un compatto K intorno a (t, x_0) vale |Vu| ≤ ‖V‖_{L^∞(K)}|u| q.o., quindi lungo una successione di punti di validità che converge a (t, x_0) si ha u_xx → 0. Definiamo ũ := u per x ≥ x_0 e ũ := 0 per x < x_0 su I × J. Allora ũ ∈ C^{1,2}(Ω) (i dati di Cauchy e u_xx, u_t si annullano su x = x_0) e L_0ũ = Ṽũ q.o. con Ṽ := V·1_{x ≥ x_0} ∈ L^∞_loc. Poiché ũ = 0 su I × (inf J, x_0), VAR-L2 dà ũ ≡ 0, cioè u = 0 per x ≥ x_0; lo stesso argomento riflesso dà u = 0 per x ≤ x_0. Quindi u ≡ 0, contro l'ipotesi.
(ii) Per VAR-T1(a) con Θ = L^∞_loc(J) e T = 1: (V − W)(x)u(t,x) = 0 q.o. in Ω. Per x ∉ X_0 esiste t con u(t,x) ≠ 0 e, per continuità, u ≠ 0 in un intorno di (t,x); quindi V − W = 0 q.o. su J ∖ X_0, insieme di misura piena per (i). Se V, W sono continui, coincidono su J ∖ X_0, denso, quindi ovunque.
(iii) Dalla formula L_0u = Vu nei punti dove u ≠ 0 (per V continuo l'equazione vale ovunque per continuità). ∎

### 1.5 [VAR-T1(c)] V = V(t,x): fasce di silenzio — prova scritta; "ogni u ≢ 0 identifica V(t,x)" è FALSO
**Enunciato.** Ω = I × J, u ∈ C^{1,2}(Ω), Z(u) := {u = 0}.
(i) Nella classe V(t,x) ∈ C(Ω) (risp. L^∞_loc(Ω)) i potenziali compatibili con u formano V + {W : W = 0 su Ω ∖ Z(u)}; quindi V è identificato ⟺ int Z(u) = ∅ (risp. |Z(u)| = 0).
(ii) Se L_0u = Vu con V ∈ L^∞_loc(Ω) e int Z(u) ≠ ∅, allora esiste un intervallo aperto T′ ⊂ I con u = 0 su T′ × J (una "fascia di silenzio").
(iii) Esistono u ≢ 0 con fasce di silenzio: su Ω = (−1,1)² la serie di Tychonoff u(t,x) := Σ_{k≥0}(−i)^k g^{(k)}(t)x^{2k}/(2k)!, con g(t) = exp(−t^{−2}) per t > 0 e g = 0 per t ≤ 0, è una soluzione C^∞ di L_0u = 0, nulla per t ≤ 0 e con u(t,0) = g(t) ≠ 0 per t > 0. Per essa ogni V(t,x) = W(t,x)·1_{t<0} è compatibile: V(t,x) non è identificato.
**Prova.** (i) VAR-T1(a) con T = 1: W·u = 0 ⟺ W = 0 su Ω ∖ Z(u) (q.o. per L^∞). Se int Z(u) ≠ ∅ esiste W ∈ C_c(int Z(u)) non nullo; se |Z(u)| > 0, W = 1_{Z(u)} ∈ L^∞. Viceversa, se int Z(u) = ∅ un W continuo nullo su Ω ∖ Z(u) (denso) è nullo; se |Z(u)| = 0 un W ∈ L^∞ nullo q.o. fuori da Z(u) è nullo q.o.
(ii) Sia la palla B((t_0,x_0), r) ⊂ Z(u). Con T′ := (t_0 − r/2, t_0 + r/2) si ha u = 0 su T′ × (x_0 − r/2, x_0 + r/2); VAR-L2 su T′ × J dà u = 0 su T′ × J.
(iii) Termine a termine: ∂_x² del termine k è il termine k − 1 con g^{(k)} al posto di g^{(k−1)}, quindi u_xx = Σ_k(−i)^{k+1}g^{(k+1)}x^{2k}/(2k)! = −iu_t e L_0u = 0. La convergenza e la derivabilità termine a termine seguono dalla stima |g^{(k)}(t)| ≤ k!(θt)^{−k}e^{−1/(2t²)} (t > 0, θ > 0 fisso), che dà |termine k| ≤ (x²/(θt))^k e^{−1/(2t²)}/k! (perché k!/(2k)! ≤ 1/k!), una serie maggiorante convergente localmente uniformemente con somma exp(x²/(θt) − 1/(2t²)) → 0 per t → 0⁺; idem per le serie derivate. È l'esempio di Tychonoff per il calore (F. John, *Partial Differential Equations*, cap. 7, solo per l'attribuzione; la stima su g^{(k)} è dimostrata in §7.1, attacco 9, con le stime di Cauchy, θ = 1/10); i fattori (−i)^k non cambiano i moduli. SymPy `s8_carleman` (c): residuo della serie troncata = solo il termine di coda; u(1/2,1/2) ≈ 0.0107 − 0.0365i ≠ 0. ∎

## Stima di Cauchy per la serie di Tychonoff (PROOF_PACKAGE §7.1, attacco 9, verbatim)
*Attacco 9 (contro T1(c)): la serie di Tychonoff non converge o non è C^∞ in t = 0.* Stima di Cauchy autosufficiente (sostituisce la CON-FONTE di §1.5): per t > 0 e |z − t| ≤ θt con θ = 1/10, scrivendo z = t(1 + ζ), |ζ| ≤ θ, si ha Re(z^{−2}) = t^{−2}Re((1 + ζ)^{−2}) ≥ t^{−2}/2 (perché |(1+ζ)^{−2} − 1| ≤ ((1−θ)^{−2} − 1) < 1/2), quindi |e^{−1/z²}| ≤ e^{−1/(2t²)} e |g^{(k)}(t)| ≤ k!(θt)^{−k}e^{−1/(2t²)}. Con (2k)! ≥ (k!)² i termini sono ≤ (x²/(θt))^k e^{−1/(2t²)}/k!, la somma ≤ exp(x²/(θt) − 1/(2t²)), che tende a 0 per t → 0⁺ uniformemente per |x| ≤ 1; le serie derivate (in t: g^{(k+j)} con (k + j)! ≤ 2^{k+j}k!j!; in x: spostamento d'indice) ammettono maggioranti dello stesso tipo. Quindi u ∈ C^∞ e tutte le derivate tendono a 0 per t → 0⁺.
