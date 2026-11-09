# REPORT — R2 · Nuclei di operatori differenziali e classi di funzioni (Fase 1)
Data: 22/10/2026 · Item: C2, C4, P1 · Notazione `NOTAZIONE.md` v1 · `R = ℂ[∂_t,∂_x]` (più in generale `ℂ[∂_1,…,∂_n]`), simbolo `P(τ,ξ)`, `V(P) ⊂ ℂ²`.

## 0. Skill caricate (Regola 2) e metodo
- `anthropic-skills:deep-research` — **invocata con Skill**. La skill prescrive un coordinatore che lancia subagenti; per vincolo di sessione (niente spawn non richiesti) ne ho seguito la struttura (decomposizione in sottotemi Q1–Q7 del PLAN, note → sintesi) **conducendo la ricerca inline**.
- `research-lit`, `arxiv`, `paper-lookup`, `math-skill` (modalità *proof*), `scientific-critical-thinking` — `SKILL.md` lette da `_vendor` (nessuno script vendor eseguito). Riferimenti verificati via web: arXiv 2212.14319, 2101.03643, 2104.10146; Oberst 1990 (Acta Appl. Math. 20:1–175); Malgrange 1956 (AIF 6:271–355); numerazione Hörmander 7.6.13/7.6.14 (attestata da fonti secondarie, vedi §9).
- `sympy`: tre script in `research/R2/sympy/` eseguiti con `.venv\Scripts\python.exe -I -X utf8`; output salvati in `*.out` e citati sotto.

## 1. Sintesi dei risultati (stato)
| # | Enunciato | Stato |
|---|---|---|
| R2-T1 | `C^∞(Ω)`, `D'(Ω)` (Ω ⊂ ℝⁿ aperto convesso) sono R-moduli **iniettivi** (principio fondamentale) e **cogeneratori** | DIMOSTRATO-CON-FONTE |
| R2-T2 | **G2 corretta**: `ker lcm(f,g) = ker f + ker g`, `ker f ∩ ker g = Sol(R/(f,g))`; per f,g coprimi `ker(fg) = ker f + ker g`; somma diretta ⟺ `V(f)∩V(g)=∅`; in n=2 intersezione di dim. `Σ_p I_p(f,g) ≤ deg f·deg g` | DIMOSTRATO (da T1) + SymPy |
| R2-C1 | **G2 FALSA nel caso periodico** `x ∈ 𝕋`: `f=∂_t−∂_x², g=∂_t+∂_x`, `u=t ∈ ker(fg)` ma `u ∉ ker f + ker g` su `ℝ_t×𝕋_x` | DIMOSTRATO + SymPy |
| R2-P2 | Criterio esatto su `I×𝕋`: vale ⟺ ∀k∈ℤ `f(·,ik)`, `g(·,ik)` coprimi in ℂ[τ] (o uno ≡0) | DIMOSTRATO (schizzo completo) |
| R2-T3 | **G1 corretta e rafforzata**: `ker(L₁+L₂) ∩ (ker L₁+ker L₂) = Sol(R/(L₁+L₂, L₁²))` (coprimi, 𝒜 iniettivo); varietà `V(L₁)∩V(L₂)`; in n=2 dim `= 2·Σ_p I_p(L₁,L₂)`. "⊆" vale in ogni R-modulo | DIMOSTRATO + SymPy |
| R2-T4 | Coeff. variabili (Ore `K[∂]`): `ker LCLM(L₁,L₂) = ker L₁ + ker L₂`, `ker GCRD = ker L₁ ∩ ker L₂` | DIMOSTRATO-CON-FONTE + SymPy |
| R2-C2 | Il prodotto non basta: `ker((x∂−1)∂) ≠ ker(x∂−1)+ker ∂` | DIMOSTRATO + SymPy |
| R2-T5 | D-finite: chiusura per somma (ord ≤ r+s, via LCLM) e prodotto (ord ≤ rs) | DIMOSTRATO-CON-FONTE + SymPy |
| R2-T6/T7 | C4.4: Ehrenpreis–Palamodov = frame continuo su V(P), misura NON unica; densità esponenziali (Malgrange); su 𝕋 base numerabile indicizzata da `V(P)∩(ℂ×iℤ)` | DIMOSTRATO-CON-FONTE; base di Schauder su ℝ: APERTO |
| R2-P1 | Galois: componenti canoniche di ker L = sottospazi G-invarianti (fattori destri), non i "termini" | DIMOSTRATO-CON-FONTE |
| A8 (C4.1) | "â = Σaₙ ⟺ f̂ = ΣΣe_{n,i}" | **FALSO come scritto** (vero solo su un sottospazio di dim. finita, T3); **VERO in forma fattorizzata** (T2) con `lcm`/`LCLM` al posto della somma, su ℝ |

## 2. Quadro algebrico (Oberst / Malgrange–Ehrenpreis–Palamodov)
**[R2-D1] Comportamento (behaviour).** Per un R-modulo 𝒜 (spazio di funzioni su cui R agisce per derivazione) e un R-modulo f.g. `M = R^{1×q}/R^{1×p}A`: `Sol_𝒜(M) := Hom_R(M,𝒜) ≅ {w ∈ 𝒜^q : A w = 0}`. In particolare `ker_𝒜 P = Hom_R(R/(P), 𝒜)` e `ker f ∩ ker g = Hom_R(R/(f,g),𝒜)`.

**[R2-T1] (Principio fondamentale; iniettività e cogeneratore).** *Ipotesi:* Ω ⊂ ℝⁿ aperto **convesso**, 𝒜 ∈ {C^∞(Ω), D'(Ω)}. *Tesi:* (a) 𝒜 è un R-modulo iniettivo, cioè `Hom_R(·,𝒜)` è esatto; equivalentemente, per ogni matrice A e ogni f ∈ 𝒜^p che soddisfa tutte le condizioni di compatibilità (B f = 0 per ogni B con BA = 0), A u = f è risolubile in 𝒜. (b) 𝒜 è cogeneratore: `Hom_R(M,𝒜)=0 ⟹ M=0`.
*Fonti:* Ehrenpreis 1970; Palamodov 1970; Malgrange 1956 (AIF 6) e 1963/64; Hörmander, *An Introduction to Complex Analysis in Several Variables*, Thm 7.6.13 (principio fondamentale, convessi) e Thm 7.6.14 (densità esponenziali-polinomi) [numerazione attestata da Lomadze, da ricontrollare]; forma modulo/comportamento ("injective cogenerator") per ℝⁿ: Oberst 1990. Per n=1 su ogni intervallo: elementare (ℂ[∂] PID e C^∞ divisibile).
*(b) per Ω convesso — argomento:* se M ≠ 0 f.g. esiste una soluzione esponenziale-polinomiale non nulla su ℝⁿ (Oberst 1990), analitica, la cui restrizione a Ω è ≠ 0.
*Attenzione:* senza convessità (o P-convessità, Hörmander ALPDO II §10.6) (a) può fallire; per `S'(ℝⁿ)` l'iniettività è plausibile ma **da verificare**, il cogeneratore è falso (S' non contiene e^{x}) — open_questions Q-R2-3.

## 3. C4.2 / G2 — teorema esatto
**[R2-T2].** *Ipotesi:* 𝒜 come in T1; f, g ∈ R∖{0}. *Tesi:*
1. `ker_𝒜 lcm(f,g) = ker f + ker g` e `ker f ∩ ker g = Sol_𝒜(R/(f,g))`.
2. Se f, g sono **coprimi** (R UFD): `ker(fg) = ker f + ker g`.
3. Somma **diretta** ⟺ `(f,g) = R` ⟺ `V(f)∩V(g) = ∅` (Nullstellensatz + cogeneratore).
4. n = 1 (ODE): coprimi ⟹ `(f,g)=R` (Bézout) ⟹ somma diretta (classico).
5. n = 2 (caso (t,x)): coprimi ⟹ `V(f)∩V(g)` finito; `dim_ℂ (ker f ∩ ker g) = dim_ℂ R/(f,g) = Σ_{p} I_p(f,g) ≤ deg f · deg g`; base: esponenziali-polinomi `t^a x^b e^{τ_p t + ξ_p x}` ai punti comuni (duale di Macaulay di R/(f,g); Sturmfels 2002 cap. 10).
6. n ≥ 3: tipicamente `V(f)∩V(g)` ha dim n−2 ≥ 1 ⟹ intersezione infinito-dimensionale.
7. I fattori ripetuti contano: `ker(f²) ⊋ ker f` (operatori di Noether, §5).

*Dimostrazione.* In un UFD `(f)∩(g) = (lcm(f,g))`. La successione
`0 → R/(lcm) --(1↦(1,1))--> R/(f) ⊕ R/(g) --((a,b)↦a−b)--> R/(f,g) → 0`
è esatta (iniettività: `a ∈ (f)∩(g)`; al centro: `a−b = αf+βg ⟹ (a,b) ≡ (c,c)` con `c = a−αf = b+βg`). Applicando il funtore controvariante esatto `Hom_R(·,𝒜)` (T1a):
`0 → Sol(R/(f,g)) --(w↦(w,−w))--> ker f ⊕ ker g --((u,v)↦u+v)--> ker lcm → Ext¹_R(R/(f,g),𝒜) = 0.`
Surgettività = punto 1; coprimi ⟹ `lcm = fg` (2). (3): il nucleo della somma è `Sol(R/(f,g))`, nullo ⟺ `R/(f,g)=0` (T1b). (5): per moduli di lunghezza finita `Hom_R(R/I,𝒜) ≅ (R/I)^*` (tutte le soluzioni sono esponenziali-polinomi) e `dim R/(f,g) = Σ I_p` (Fulton, *Algebraic Curves*, cap. 3 e 5). ∎
*Nota:* "⊇" è puramente algebrica e vale in ogni spazio; "⊆" (esistenza della scomposizione) è esattamente `Ext¹(R/(f,g),𝒜)=0`.

**Esempio verificato** (`sympy/g2_factorization.py` → `.out`): `f = ∂_t−∂_x²`, `g = ∂_t+∂_x`. Gröbner `(f,g) = (τ+ξ, ξ²+ξ)`; `V(f)∩V(g) = {(0,0),(1,−1)}`, molteplicità 1 ⟹ `ker f ∩ ker g = span{1, e^{t−x}}` (verificato). Quindi `ker(fg) = ker(calore) + ker(trasporto)` con ambiguità di dimensione 2. `u = t ∈ ker(fg)`: su ℝ² `t = x + (t−x)`; scomposizione generale `u₂ = −(x−t) + C e^{t−x} + D` (2 parametri = dim intersezione ✔).

**[R2-C1] Controesempio periodico.** Su `D'(I×𝕋)` (o C^∞), stessa coppia: `u = t` è periodica in x, `fg·t = 0`, ma il modo k=0 dà `f₀ = g₀ = τ` ⟹ `ker f₀ + ker g₀ = {costanti} ∌ t`. **G2 è falsa su 𝕋.** Motivo: `C^∞(𝕋)` non è divisibile per ∂_x (∂_x u = 1 non ha soluzioni periodiche) ⟹ non è R-modulo iniettivo.
**[R2-P2] Criterio su `I×𝕋`.** Per f, g coprimi, `ker(fg) = ker f + ker g` su `D'(I×𝕋)` ⟺ ∀k ∈ ℤ: `f_k := f(·,ik) ≡ 0` oppure `g_k ≡ 0` oppure `gcd(f_k,g_k) = 1` in ℂ[τ]; nel caso non degenere ⟺ `V(f)∩V(g)∩(ℂ×iℤ) = ∅`.
*Dimostrazione.* Fourier in x: `fg u = 0 ⟺ f_k g_k u_k = 0 ∀k`. Per n=1, `ker(f_kg_k) = ker f_k + ker g_k ⟺ gcd = 1` (dimensioni `deg f_k + deg g_k` contro `deg f_k + deg g_k − deg gcd`). Globalizzazione: identità di Bézout–risultante `a f + b g = r(ξ)`, `a,b ∈ R`, `r = Res_τ(f,g) ≢ 0`; per |k| grande `|r(ik)| ≥ c > 0`; `u₁ := r(∂_x)^{-1} b g u`, `u₂ := r(∂_x)^{-1} a f u` (moltiplicatori a crescita polinomiale ⟹ continui su D') danno la scomposizione sui modi con r(ik)≠0; i modi restanti sono finiti e si trattano col caso n=1. ∎ Nell'esempio `Res_τ = ξ²+ξ`, unico modo cattivo k=0 (script).
→ **Per H0:** la scelta ℝ vs 𝕋 cambia la verità di A8-fattorizzato; su 𝕋 le **risonanze** `V(f)∩V(g)∩(ℂ×iℤ)` sono un'ostruzione, assente su ℝ dove la scomposizione usa funzioni non periodiche (es. x).

## 4. C4.1 / G1 — somma di termini (A8 come scritto)
**[R2-T3].** *Ipotesi:* L = L₁ + L₂ ∈ R. *Tesi:*
(a) (ogni R-modulo 𝒜) `ker L ∩ (ker L₁ + ker L₂) ⊆ Sol(R/(L, L₁L₂)) = Sol(R/(L₁+L₂, L₁²))`.
(b) (𝒜 iniettivo, L₁, L₂ coprimi) uguaglianza.
(c) `V(L₁+L₂, L₁²) = V(L₁)∩V(L₂)`; in n = 2 con L₁, L₂ coprimi lo spazio ha dimensione finita `Σ_p I_p(L₁+L₂, L₁²) = 2·Σ_p I_p(L₁,L₂)`, generato da esponenziali-polinomi con frequenze nei punti comuni.
(d) Fattore comune h: `ker h ⊆ ker L₁ ∩ ker L₂ ∩ ker L` infinito-dimensionale (n ≥ 2); in generale `ker L ∩ (ker L₁+ker L₂) = ker L ∩ ker lcm(L₁,L₂)`.
(e) N termini, `L = Σ_n L_n`, 𝒜 iniettivo: `Σ_n ker L_n = ker lcm(L₁,…,L_N)` e `ker L ∩ Σ_n ker L_n = Sol(R/(L, lcm))`, varietà `⋃_n V(L_n) ∩ V(Σ_{m≠n} L_m)`.
*Dimostrazione.* (a) u = u₁+u₂, L₁u₁ = L₂u₂ = 0 ⟹ `L₁L₂u = L₂(L₁u₁) + L₁(L₂u₂) = 0` (commutatività); modulo `(L₁+L₂)`: `L₁L₂ ≡ −L₁²`. (b) T2.2. (c) su V(L₁): `L₁+L₂ = 0 ⟺ L₂ = 0`; molteplicità: `I_p(F,GH) = I_p(F,G)+I_p(F,H)`, `I_p(L₁+L₂,L₁) = I_p(L₂,L₁)` (Fulton cap. 3). (d),(e) idem con T2.1. ∎
**Risposta alla questione lasciata APERTA da R5** (R5 dimostra solo "⊆"): **sì, la successione esatta + iniettività di Malgrange–Ehrenpreis decide l'uguaglianza** `ker(L₁+L₂) ∩ (ker L₁+ker L₂) = ker(L₁+L₂, L₁L₂)` — è vera per L₁, L₂ coprimi su C^∞/D' di un convesso (la "⊇" è esattamente T2.2, cioè `Ext¹(R/(L₁,L₂),𝒜) = 0`); è falsa in generale se L₁, L₂ hanno un fattore comune (sostituire L₁L₂ con lcm) e può fallire su 𝕋 per risonanza (R2-C1).
**Esempi verificati** (`sympy/g1_sum_split.py` → `.out`):
- Calore come somma `L₁ = ∂_x²`, `L₂ = −∂_t`: Gröbner `(τ², ξ²−τ)`, dim **4** `= 2·I_0(ξ²,τ) = 2·2`; soluzioni con E_int = 0: `1, x, x²+2t, x³+6tx`. La soluzione generica `e^{s²t+sx}` (s≠0) ha `L₁L₂u = −s⁴e^{…} ≠ 0` ⟹ **non** sta in `ker L₁ + ker L₂`.
- Avvezione-diffusione `L₁ = ∂_t−∂_x²`, `L₂ = ∂_x`: Gröbner `(ξ², τ+ξ)`, dim 2.
- Termini non coprimi `∂_t∂_x`, `∂_x²` (fattore ξ): ogni `a(t)` sta in tutti i nuclei.
- Tre termini `∂_t, −∂_x², −∂_x`: `gcd(∂_x², ∂_x) = ∂_x` ⟹ per termini **monomiali** nella stessa variabile la coprimalità fallisce sempre.
**Verdetto A8:** falso come equivalenza; la parte di ker L che si scompone additivamente per termini è un sottospazio **di dimensione finita** (n=2, termini coprimi) di esponenziali-polinomi concentrati sul luogo di collisione `V(L₁)∩V(L₂)`; per termini monomiali è fatta di polinomi (frequenza 0). E_int ≠ 0 per la soluzione generica: conferma P1 e il quadro moltiplicativo di R5. (Coerente con, e più forte di, RT-S1b di SCOUT-1, che dà solo `ker L₁ ∩ ker L₂ ⊆ ker L`.)

## 5. Ehrenpreis–Palamodov, operatori di Noether, C4.4 (numerabilità)
**[R2-T6] (Rappresentazione integrale).** *Ipotesi:* Ω convesso, P ∈ R (o modulo f.g.). *Tesi:* esistono le componenti irriducibili V₁,…,V_s (dei primi associati) e operatori di Noether polinomiali `B_{ij}(x,z)` tali che ogni `u ∈ ker_{C^∞(Ω)} P` si scrive `u(x) = Σ_{i,j} ∫_{V_i} B_{ij}(x,z) e^{⟨x,z⟩} dμ_{ij}(z)` con misure complesse opportune; P ridotto ⟹ basta B = 1. *Fonti:* Ehrenpreis 1970; Palamodov 1970; Hörmander ICASV §7.6; Björk 1979; Ait El Manssour–Härkönen–Sturmfels, Glasgow Math. J. 65 (2023) S2–S27 (arXiv 2104.10146) — algoritmi; Cid-Ruiz–Sturmfels (IMRN, arXiv 2101.03643): decomposizione primaria differenziale, numero minimo di operatori di Noether = molteplicità aritmetica. Per `P = Q^m` gli operatori di Noether danno `x^l e^{⟨x,z⟩}` (analogo PDE di `x^k e^{λx}`, C2.1).
**[R2-T7] (Densità, Malgrange 1956).** Ω convesso: gli esponenziali-polinomi in ker P sono densi in `ker_{C^∞(Ω)} P` (Malgrange AIF 6; Hörmander ICASV Thm 7.6.14). Per P irriducibile basta `span{e^{⟨x,z⟩} : z ∈ S}`, S ⊂ V(P) insieme di unicità per funzioni intere di tipo esponenziale ristrette a V(P) (es. S con punto di accumulazione nel luogo regolare) — per dualità: `T ∈ E'(Ω)` annulla ker P ⟺ `T̂` si annulla su V(P) (con molteplicità). *Stato:* schizzo; dettaglio per V(P) singolare APERTO.
**Risposta a C4.4 / A7.**
- **ODE:** dimensione finita `= deg P`; base `x^k e^{λx}`.
- **PDE su ℝ (Ω convesso):** Fréchet separabile infinito-dimensionale; la rappresentazione naturale è un **frame continuo** su V(P), con **misura non unica** (non una base). Famiglie numerabili totali esistono (T7); esistenza di una **base di Schauder/Riesz** di esponenziali-polinomi (es. calore su ℝ²): APERTO (Q-R2-1). Conferma G6.
- **PDE su I×𝕋:** ker P = ⊕̂_k (modo k: ODE `P(∂_t, ik)w = 0`) ⟹ sistema **numerabile** `t^j e^{τ t + ikx}`, `(τ,ik) ∈ V(P)∩(ℂ×iℤ)` con molteplicità, sviluppo incondizionato in D' — base di Schauder di ker P. Per `u_t = a(∂_x)u`: base `e^{a(ik)t+ikx}`. Conferma G6.
- **EPGP / C1 / RT-7** (divisione concordata con R8: R2 = parte algebrica, R1 = GP/RKHS): Härkönen–Lange-Hegermann–Raiță (ICML 2023, PMLR 202:12587–12615) usano nuclei `k(x,y) = ∫_V e^{⟨x,z⟩} conj(e^{⟨y,z⟩}) dν(z)` le cui realizzazioni sono soluzioni esatte: è l'RKHS di C1.0 costruito da C2 (encoder analitico di D1 = trasformata di Fourier–Laplace/Ehrenpreis). La scelta della misura spettrale ν su V(P) **è** la regolarizzazione di P2. Ait El Manssour–H–S è solo direzione diretta (da P a ker P), non inversa.

## 6. Coefficienti variabili, D-moduli, Galois (C4.2 non commutativo, C2.6ᵈ)
**[R2-T4] (Ore).** *Ipotesi:* K campo differenziale (es. ℂ(x)) con costanti algebricamente chiuse, `D = K[∂]`, U estensione di Picard–Vessiot (o germi analitici in un punto ordinario) contenente spazi completi di soluzioni; L₁, L₂ ≠ 0. *Tesi:* `ker_U LCLM(L₁,L₂) = ker L₁ + ker L₂`, `ker_U GCRD(L₁,L₂) = ker L₁ ∩ ker L₂`, `ord LCLM + ord GCRD = ord L₁ + ord L₂`; successione esatta `0 → D/D·LCLM → D/DL₁ ⊕ D/DL₂ → D/D·GCRD → 0` (**analogo esatto di G2**, lcm → LCLM). Somma diretta ⟺ GCRD = 1. *Fonti:* Ore 1933 (Ann. Math. 34); Bronstein–Petkovšek 1996 (TCS 157); van der Put–Singer 2003 cap. 2.
**[R2-C2] Il prodotto non basta.** `L₁ = x∂−1` (ker span{x}), `L₂ = ∂` (ker span{1}): `L₁L₂ = x∂²−∂`, `ker = span{1, x²}` ∌ x; `LCLM = ∂²`, ker = span{1,x} = ker L₁ + ker L₂; `L₂L₁ = x∂²` ha il nucleo giusto perché multiplo sinistro di entrambi (`sympy/ore_lclm.py`). In generale `ker(L₁L₂) ⊇ ker L₂`, e `⊇ ker L₁` ⟺ `L₁L₂ ∈ D·L₁`. La fattorizzazione non è unica (`∂² = (∂ + 1/(x+c))(∂ − 1/(x+c))` ∀c); unica solo la decomposizione di Loewy.
**[R2-P1] (Galois).** G = gruppo di Galois differenziale di L. Sottospazi G-invarianti di ker L ↔ fattori destri monici di L (vdP–S cap. 2). L completamente riducibile (LCLM di irriducibili) ⟺ ker L G-modulo semisemplice; vale se G riduttivo. Decomposizioni `D/DL ≅ ⊕` ↔ idempotenti dell'eigenring (Singer 1996; van Hoeij) — coincide con RT-S1d di SCOUT-1 (**proposta di fusione**: RT-S1d ⊃ R2-Q5). ⟹ **Le "componenti" canoniche nel caso a coeff. variabili sono gli addendi G-invarianti / indecomponibili di ker L, non i termini additivi di L.**
**[R2-T5] (D-finite / olonome; C2.6ᵈ).** f D-finita su K(x) ⟺ ∃ L ≠ 0 con Lf = 0 ⟺ `dim_{K(x)} span{f^{(i)}} < ∞`. ord(f) ≤ r, ord(g) ≤ s ⟹ `f+g` annullata da `LCLM(L_f,L_g)`, ord ≤ r+s; `fg` dal prodotto simmetrico, ord ≤ rs; chiusura per derivata, integrale, composizione con algebriche; multivariato: olonomia (Bernstein), Lipshitz 1989, Zeilberger 1990. *Fonti:* Stanley 1980 (Eur. J. Comb. 1, Thm 2.3); Kauers–Paule 2011 cap. 7; bound per LCLM: Bostan–Chyzak–Li–Salvy ISSAC 2012. Esempio verificato: `LCLM(∂−2x, ∂²+1)` annulla `e^{x²}+sin x`, ordine 3, con singolarità **apparenti** in `4x²+3=0` — la somma di due classi "belle" porta singolarità spurie nel catalogo.
*Osservazioni:* (i) le funzioni speciali sono soluzioni D-finite di ordine 2 con singolarità prescritte: la classe è fissata dal D-modulo `D/DL` (a meno di gauge), non da L; (ii) una singola PDE non è olonoma per n ≥ 2 (`D/DP` ha dimensione 2n−1), ma singole soluzioni possono esserlo (nucleo del calore: `Ann ⊇ (∂_t−∂_x², 2t∂_x+x)`) — per R4: `L ∈ Ann_D(u) ∩ ℂ[∂]` per eliminazione; (iii) (nota R8) l'annullatore minimo dipende dall'anello: `e^{2x}+x e^{−x}` ha ordine 3 su ℂ[∂] ma ordine 2 su ℂ[x][∂] — per G4 bisogna fissare l'anello dei coefficienti ammessi.
**C2.6 (serie 1, trasporto) lato Ehrenpreis:** `V(τ+cξ)` retta ⟹ `u = ∫ e^{ξ(x−ct)} dμ(ξ) = g(x−ct)`: V(P) lineare ⟺ soluzioni = funzioni arbitrarie di una forma lineare.

## 7. P1 — contributo su E_int (e risposta a R5)
- Quadro additivo per termini: `{u ∈ ker L : E_int = 0}` = `Sol(L₁+L₂, L₁²)` (T3), dim finita; E_int vive canonicamente nel **quoziente** `ker L / (ker L ∩ Σ ker L_n)`; un rappresentante canonico richiede struttura in più (proiezione di C1 o quadro moltiplicativo). Anche dove E_int = 0 la scomposizione è unica solo modulo `ker L₁ ∩ ker L₂`.
- Quadro fattorizzato (T2): E_int = 0 sempre su ℝ (ambiguità `Sol(f,g)`); su 𝕋 E_int vive in `⊕_{k risonanti} ker(f_kg_k)/(ker f_k + ker g_k)`, dim `Σ deg gcd(f_k,g_k)`.
- Coeff. variabili: E_int = 0 usando LCLM; componenti canoniche G-invarianti; per estensioni non spezzate E_int ∈ Ext¹ (RT-S1d).

## 8. Mappa sugli item del piano
| Item | Contributo R2 | Stato |
|---|---|---|
| C4.1 (A8) | T3: falso salvo sottospazio finito; vero in forma lcm (T2) | dimostrato |
| C4.2 | T2 (ℝ, convesso); R2-C1/P2 (𝕋); T4 (Ore) | dimostrato; S' e non convessi aperti |
| C4.3 | lato R2: nessuna somma additiva di nuclei per somme di termini ⇒ quadro moltiplicativo (R5) | rinvio R5 |
| C4.4 | T6/T7: frame continuo su ℝ, base numerabile su 𝕋 | noto; Schauder su ℝ aperto |
| C2.6ᵈ | T5, R2-P1 | noto |
| C2.6 (trasporto) | §6 | noto |
| P1 | §7 | dimostrato (parte algebrica) |
| G1 | corretta e rafforzata | dimostrato |
| G2 | vera su ℝ/convessi; **falsa su 𝕋** senza non-risonanza | dimostrato + controesempio |
| G4 (per R4) | "supporto della misura" mal posto (misura non unica); invariante corretto `V(Ann(u))`, anello fissato | osservazione |
| G6 | confermata | noto |

## 9. Critica (scientific-critical-thinking)
- Solidi: T2 su ℝⁿ/convessi (teoria classica + dimostrazione breve da T1); T3 (algebra elementare + T2); controesempi verificati simbolicamente.
- Da ricontrollare: numerazione Hörmander 7.6.13/7.6.14 (attestata indirettamente); iniettività di S'; lemma "insieme di unicità" in T7 per V(P) singolare/riducibile; in P2 la globalizzazione è in D'/C^∞ (crescita polinomiale), non automaticamente in L².
- Rischio interpretativo principale: se "termine" = monomio `λ_k∂^{α_k}` (NOTAZIONE), A8 è quasi vuoto (T3); se "componente" = fattore / sotto-equazione, A8 è un teorema (T2). **Raccomandazione R2 per il Gate 1: definire le componenti come fattori (coeff. costanti: decomposizione primaria di (P); coeff. variabili: fattori di Loewy / addendi G-invarianti), e trattare le somme di termini nel quadro moltiplicativo/log-simbolo (R5).**

## 9bis. Verdetto R4 (RT-R4a / C3.3) e coerenza con R3
- **Confermo** il verdetto di R4: le componenti naturali di u sono indicizzate dai pezzi di V(P) (decomposizione primaria di (P) / fattori coprimi), non dai termini. È esattamente T2 (+ T6 per i fattori ripetuti); la versione a coeff. variabili è T4/R2-P1 (fattori di Loewy, addendi G-invarianti). Unica correzione: su 𝕋 la scomposizione per fattori richiede l'assenza di risonanze (R2-C1/P2).
- Concordo con R4-C2 (G4 con "supp μ Zariski-denso" falsa: misura non unica) — stesso rilievo in §8.
- R3 (Lemma R3-L1, avvezione–diffusione `L₁=∂_t+c∂_x`, `L₂=−D∂_x²`: dim 4) è coerente con T3(c): `2·I_0(τ+cξ, ξ²) = 2·2 = 4`.

## 10. Messaggi scambiati
- Ricevuti: R5 (DOMANDA a,b,c — risposta inviata), R8 (AVVISO EPGP — accettata divisione), SCOUT-1 (AVVISO RT-S1b/d/e/f — risposta con proposta di fusione RT-S1d ⊃ Q5).
- Inviati: TABELLA a R3 e R4; RISPOSTA a R5; RISPOSTA a SCOUT-1; NEW-ROUTE a central (ostruzione periodica/risonanze; quadro Oberst dei comportamenti); PLAN-READY e DONE a central.
