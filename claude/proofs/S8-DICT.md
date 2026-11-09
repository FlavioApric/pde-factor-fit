# PROOF_PACKAGE — S8-DICT (Fase 8, prove) · L9–L10: dizionario universale filtrato 𝓓_∞
27/10/2026. Sessione S8-DICT, ripresa da `work/S8-DICT/` (PLAN.md del 26/10 con predizione scritta; PLAN-READY già inviato).

**Audit (aggiornamento del 27/10/2026).** Il pacchetto è stato auditato da S-CHECK-F8-DICT: `work/CHECK-F8/AUDIT_S8-DICT.md`. Il kill-argument indipendente su N1 (`work/CHECK-F8/KA_DICT_N1_*.md`) ha esito SURVIVES-WITH-FIXES. Gli script `work/CHECK-F8/sympy/dict_check.py` danno 18/18 PASS. I fix DICT-1 … DICT-18 sono recepiti nel testo e ciascuno è marcato "[fix DICT-k]" nel punto in cui interviene; l'elenco "fix → modifica → sezione" è in `RECEPIMENTO.md`. Gli stati proposti dall'audit (DIMOSTRATO dopo i fix, salvo le eccezioni) sono riportati in §7 e in `LEDGER_ROWS.md`; la registrazione nel LEDGER spetta al coordinatore. Gli enunciati nuovi nati dal recepimento, e non già scritti dall'audit, sono marcati **DA AUDITARE**.

**Post-Gate 8 (27/10/2026).** Recepiti `work/CHECK-F8/AUDIT_S8-DICT_rev2.md` (MAG-1…MAG-5), `research/DEVIL/ATTACK-8.md` (O5, O13, O15, O19) e `research/CIT-AUDIT/AUDIT-8.md` §5. Elenco in `RECEPIMENTO.md`, sezione "post-Gate 8". Gli stati in questa versione sono cambiati solo verso il basso: DICT-AX scende a "CON-FONTE da leggere"; DICT-RANGO e DICT-RANGO-cor valgono come ID-ker sotto (H-ex); DICT-MAG-NU non è più un claim autonomo, è un corollario di SYS-N3(c).

**Stati (testo originale, prima dell'audit).** Nessun enunciato di questo pacchetto è DIMOSTRATO: "prova scritta" significa prova completa non ancora auditata da S-CHECK-F8; "CON-FONTE" significa enunciato pubblicato (con "verificata" solo se letto sulla fonte, altrimenti "da verificare"); "candidato" significa enunciato senza prova completa; "FALSO" significa refutato con controesempio; "strumento" significa procedura o euristica senza contenuto di teorema.

**Skill caricate** (lettura integrale dei SKILL.md, nessuno script `_vendor` eseguito): `skills-local/session-protocol`, `skills-local/claim-lifecycle`; dalla catena di claim-lifecycle: proof-writer (triage di ogni claim: PROVABLE AS STATED / AFTER WEAKENING / NOT JUSTIFIED, mappa delle dipendenze, prova), math-skill in modo controesempio/limite, SymPy, kill-argument su N1 (`KILL_ARGUMENT_N1.md`). Il proof-checker non è eseguito qui: lo esegue S-CHECK-F8 (`CHECK_REQUEST.md`). Niente ML.

**Verifiche** (solo verifiche, non prove): `sympy/s8dict_checks.py` → `.out` **27/27 OK** (il test A4 falliva il 26/10 per una tolleranza numerica: con y = 10⁻¹⁰ e s = 0,8 la correzione (ξy)^{2(1−s)} ≈ 10⁻⁴ superava la soglia; con y = 10⁻⁴⁰ passa, la formula era giusta); `sympy/s8dict_checks2.py` → `.out` **12/12 OK**.

**Modelli di dato** (NOTAZIONE v5): DM1 formula/EP, DM2 jet in un punto, DM3 u noto esattamente in H^m(Ω), DM-φ dato a meno della fase temporale globale, DM-inv dati invarianti di gauge. **Modelli di calcolo**: (T) Turing (uscite = stringhe finite, eventualmente con oracolo per u); (BSS) aritmetica reale esatta (uscite reali). Ogni enunciato dichiara quelli che usa.

**Fix di DEVIL-6 recepiti qui:** F1 (N1(vi) sostituito dal teorema di rango (a′)/(b′), §2.6), F3 (nessun "tiene conto di tutto": tabella di enunciati separati, §1.8 e §6), F4 (ritardo = sistema aumentato di trasporto; N3 ristretto ai sistemi ODE a dimensione finita, §1.5), F9 (modelli di dato e di calcolo per enunciato; MF1–MF3, (H-ID)), F10 (N1(v) non lineare via parti omogenee di grado massimo, §2.5; novità di N1(i)–(iii) e N2 dichiarata bassa). Correzioni di CIT-AUDIT-6: Slovák 1987 (primo Peetre non lineare) e 1988; Prenter solo per spazi di Hilbert (U5, §1.8).

---

## 0. Quadro e definizioni
- Ω ⊂ ℝ^N aperto, N = 1 + d, coordinate y = (t, x). C^∞(Ω) è lo spazio di Fréchet della convergenza uniforme di tutte le derivate sui compatti (spazio polacco). R = ℂ[τ, ξ_1, …, ξ_d] ≅ ℂ[∂_t, ∂_x], R_{≤n} i polinomi di grado ≤ n.
- **Dizionario filtrato**: successione 𝓓_0 ⊂ 𝓓_1 ⊂ … di insiemi finiti di operatori ("atomi") enumerata da un algoritmo esplicito; 𝓓_∞ = ∪_n 𝓓_n. Un atomo può dipendere da un parametro reale preso in un insieme numerabile denso (s ∈ ℚ per |ξ|^s, τ ∈ ℚ_+ per il ritardo, x_0 ∈ ℚ^d per gli atomi singolari). Funzione di altezza h: 𝓓_∞ → ℕ con finiti atomi per altezza, 𝓓_n = {h ≤ n}.
- **Livello omogeneo** n: span_ℂ 𝓓_n = span{D_0, …, D_{N_n}}. **Livello affine** 𝓐_n = {D_0 + Σ_{i≥1} c_iD_i} (atomo D_0 fissato con coefficiente 1, per esempio ∂_t). **Fit** omogeneo di u al livello n: esiste c ≠ 0 con Σc_iD_iu = 0; **misfit**: non esiste.
- **Universalità per una classe 𝒞 in una topologia τ**: ogni T ∈ 𝒞 è limite in τ di una successione in span_{ℚ(i)} 𝓓_∞. Rappresentazione esatta: T ∈ span 𝓓_n per qualche n.
- Per coefficienti costanti, 𝓓_n = {∂^α : |α| ≤ n}, span 𝓓_n = R_{≤n} e il nucleo di Gram al livello n è Ann(u) ∩ R_{≤n} (C3-L1).

---

## 1. Universalità classe per classe

### 1.1 U1 (operatori locali lineari) e N0
**Triage:** PROVABLE AS STATED (U1-a, U1(a), N0); U1-b (velocità) AFTER WEAKENING: velocità solo CON-FONTE da verificare.

**Fonte (CON-FONTE, verificata in KMS §19.1).** Peetre, Math. Scand. 7 (1959) 211–218; Rectification, Math. Scand. 8 (1960) 116–120. Kolář–Michor–Slovák (KMS), *Natural Operations in Differential Geometry*, Springer 1993, Thm 19.1: se D: C^∞(L_1) → C^∞(L_2) è lineare e supp Ds ⊂ supp s, per ogni compatto K esiste r tale che j^r_y s = 0 ⇒ Ds(y) = 0 per y ∈ K. Nessuna ipotesi di continuità.

**Lemma U1-a (prova scritta).** Sia T: C^∞(Ω) → C^∞(Ω) lineare con supp Tu ⊂ supp u. Esistono a_α ∈ C^∞(Ω), localmente finite (su ogni compatto K solo i |α| ≤ r(K) sono non nulli), con Tu = Σ_α a_α∂^αu.
*Prova.* Sia K compatto e U un intorno aperto relativamente compatto di K; per Peetre su Ū esiste r con j^r_yu = 0 ⇒ Tu(y) = 0 (y ∈ Ū). Per y ∈ U la mappa j^r_yu ↦ Tu(y) è quindi ben definita e lineare sullo spazio dei getti (ogni getto è il getto di un polinomio), e si scrive in modo unico Tu(y) = Σ_{|α|≤r} a_α(y)∂^αu(y). Liscezza: sia χ ∈ C_c^∞(Ω) con χ ≡ 1 su un intorno di Ū e m_β(z) := χ(z)z^β/β!. Per y ∈ U il getto di m_β in y è quello di z^β/β!, quindi T(m_β)(y) = Σ_{α≤β} a_α(y)y^{β−α}/(β−α)!. È un sistema triangolare (ordine parziale α ≤ β) con diagonale 1, termini noti T(m_β) ∈ C^∞ e coefficienti polinomiali: per induzione su |β| si ha a_β = T(m_β) − Σ_{α<β}a_α y^{β−α}/(β−α)! ∈ C^∞(U). L'unicità dei coefficienti puntuali permette di incollare le definizioni sui diversi U. ∎ (SymPy A0: il sistema triangolare in 1D, ordine 2.)

**Topologia τ₁.** T_j → T se per ogni compatto K esiste r con ord(T_j|_K), ord(T|_K) ≤ r per ogni j e i coefficienti convergono in C^∞(K). Implica T_ju → Tu in C^∞(Ω) per ogni u, uniformemente sui limitati.

**Teorema U1 (prova scritta).** (a) Sia (χ_j) una partizione dell'unità C^∞ esplicita, localmente finita, subordinata a un'esaustione K_1 ⋐ K_2 ⋐ … di Ω, e 𝓓^{loc}_n := {χ_j(y)y^β∂^α : j, |α|, |β| ≤ n}. Ogni T lineare locale C^∞(Ω) → C^∞(Ω) è limite in τ₁ di elementi di span_{ℚ(i)} 𝓓^{loc}_∞.
(b) **N0.** Con 𝓓^{pol}_n := {y^β∂^α : |α|, |β| ≤ n}: T è limite puntuale (T_nu → Tu in C^∞(Ω) per ogni u) di operatori a coefficienti polinomiali se e solo se T ha ordine globalmente finito su Ω.
*Prova di (a).* Densità dei polinomi in C^ℓ(K): data g ∈ C^∞ definita vicino a K, χg ∈ C_c^∞(ℝ^N) con χ ≡ 1 vicino a K; (χg) ∗ G_ε → χg in C^ℓ(K) (G_ε gaussiana), e (χg) ∗ G_ε è intera, con serie di Taylor convergente con tutte le derivate uniformemente su K; i coefficienti si arrotondano in ℚ(i). Sia r_j l'ordine di T su supp χ_j (finito per U1-a). Scelgo polinomi p_{α,j,n} con ‖a_α − p_{α,j,n}‖_{C^n(supp χ_j)} ≤ 2^{−n}/(1 + ‖χ_j‖_{C^n}) e pongo T_n := Σ_{j≤n}χ_jΣ_{|α|≤r_j}p_{α,j,n}∂^α. Su un compatto K solo finiti supp χ_j intersecano K: l'ordine di T_n|_K è ≤ max r_j, indipendente da n, e per Leibniz Σ_jχ_jp_{α,j,n} → Σ_jχ_ja_α = a_α in C^∞(K). ∎
*Prova di (b).* (⇐) Se ord T ≤ k su Ω, prendo polinomi p_{α,n} con ‖a_α − p_{α,n}‖_{C^n(K_n)} ≤ 1/n (|α| ≤ k); allora ‖(T − T_n)u‖_{C^ℓ(K)} → 0 per ogni u, ℓ, K. (⇒) C^∞(Ω) è di Fréchet, quindi botte: per Banach–Steinhaus la successione puntualmente convergente {T_n} è equicontinua; fissato K compatto con interno non vuoto esistono k, K′, C con sup_K|T_nu| ≤ C‖u‖_{C^k(K′)} per ogni n, u. Se un T_n avesse un coefficiente p_{α,n} ≢ 0 con |α| = ρ > k (ρ l'ordine massimo), sceglierei y_0 ∈ int K e θ ∈ ℝ^N con σ(y_0, θ) := Σ_{|α|=ρ}p_{α,n}(y_0)θ^α ≠ 0 (un polinomio non nullo non si annulla su un aperto). Con u_λ = χ(y)e^{iλ⟨θ,y⟩}, χ ≡ 1 vicino a y_0: |T_nu_λ(y_0)| = λ^ρ|σ(y_0,θ)| + O(λ^{ρ−1}), mentre C‖u_λ‖_{C^k(K′)} = O(λ^k): contraddizione per λ → ∞. Quindi ogni T_n ha ordine ≤ k su int K, cioè i coefficienti polinomiali di ordine > k si annullano su un aperto, dunque ovunque: ord T_n ≤ k su Ω. Allora j^k_yu = 0 ⇒ T_nu(y) = 0 per ogni n ⇒ Tu(y) = 0: ord T ≤ k su Ω. ∎
*Esempio di N0.* Ω = ℝ, T = Σ_kφ_k(x)∂_x^k con φ_k ∈ C_c^∞((k, k+1)) non nulle: locale, lineare, di ordine globalmente infinito; non è limite puntuale di operatori a coefficienti polinomiali, ma lo è in 𝓓^{loc} per (a).

**U1-b (classi di coefficienti; stato per voce).** Su K = [−1,1]^N, T di ordine ≤ m:
1. coefficienti polinomiali: rappresentazione esatta a un livello finito (prova ovvia);
2. coefficienti analitici in un intorno del poliellisse di Bernstein E_ρ: E_n(a)_{C^ℓ} ≤ C_{ℓ,ρ′}ρ′^{−n}, ρ′ < ρ — **CON-FONTE da verificare** (approssimazione di Chebyshev tensoriale);
3. coefficienti C^s: Jackson multivariato e approssimazione simultanea delle derivate (Bagby–Bos–Levenberg 2002) — **CON-FONTE da verificare**;
4. coefficienti singolari (Coulomb 1/|x|, log|x|): T non manda C^∞(Ω) in C^∞(Ω), quindi è fuori dal quadro di Peetre su Ω (Peetre vale su Ω ∖ Σ). **Prova scritta** della densità debole: se a ∈ L^p(K), 1 ≤ p < ∞, e p_n sono polinomi con ‖a − p_n‖_{L^p(K)} → 0 (densi in L^p), allora ‖(a − p_n)∂^αu‖_{L^p(K)} ≤ ‖a − p_n‖_{L^p(K)}‖u‖_{C^m(K)} → 0: convergenza in norma C^m(K) → L^p(K), senza velocità uniforme. La rappresentazione esatta richiede atomi singolari |x − x_0|^{−j}, log|x − x_0| con x_0 parametro continuo (x_0 ∈ ℚ^d: esattezza solo nel limite).

### 1.2 U2 (operatori locali non lineari) — liscezza di F senza KMS 18.16
**Triage:** PROVABLE AS STATED; la predizione del PLAN (liscezza di F dalla regolarità di D su una famiglia liscia esplicita + Boman) è confermata.

**Fonti.** Slovák, *On the finite order of some operators*, Proc. Conf. Diff. Geom. Appl. Brno 1986, Reidel 1987, 283–294 (primo Peetre non lineare, attribuzione di KMS p. 210, CIT-AUDIT-6) e Slovák, Ann. Global Anal. Geom. 6 (1988) 273–283, DOI 10.1007/BF00054575 (generalizzazione). **KMS §19.10 (versione regolare, teorema non numerato; CON-FONTE verificata da CIT-AUDIT-6):** se D: C^∞(Y → X) → C^∞(Z, W) è π-locale e regolare, per ogni f e compatto K ⊂ Z esistono r e un intorno 𝒱 di f nella topologia C^∞ compatto-aperta tali che, per x ∈ π(K) e g_1, g_2 ∈ 𝒱, j^r_xg_1 = j^r_xg_2 ⇒ Dg_1 = Dg_2 su π^{−1}(x) ∩ K. **Boman**, Math. Scand. 20 (1967) 249–268, DOI 10.7146/math.scand.a-10835 (riferimento corretto da CIT-AUDIT-8 §5; enunciato CON-FONTE): una funzione f: ℝ^n ⊃ U → ℝ è C^∞ se f∘c è C^∞ per ogni curva c ∈ C^∞(ℝ, U).

**Quadro.** Y = Ω × ℝ^q, Z = Ω, π = id; D: C^∞(Ω, ℝ^q) → C^∞(Ω, ℝ^p) **locale** (Dg(y) dipende solo dal germe di g in y) e **regolare** (per ogni famiglia g: ℝ × Ω → ℝ^q liscia, (s, y) ↦ D(g_s)(y) è liscia). Notazione: J^r_y ≅ ℝ^{M}, M = q·#{|α| ≤ r}, coordinate (j_α); j^r_yg = (∂^αg(y))_{|α|≤r}.

**Lemma U2-a (prova scritta).** Siano f ∈ C^∞(Ω, ℝ^q) e K ⊂ Ω compatto. Esistono r, ε_0 > 0, un intorno aperto Ω_1 ⊃ K e, posto 𝒲 := {(y, j) ∈ Ω_1 × J^r : |j − j^r_yf| < ε_0}, una funzione F ∈ C^∞(𝒲, ℝ^p) tale che Dg(y) = F(y, j^r_yg) per ogni g ∈ 𝒱 e ogni y ∈ Ω_1 con (y, j^r_yg) ∈ 𝒲 (𝒱 l'intorno di KMS 19.10 relativo a un compatto K_1 ⊃ Ω_1). [fix DICT-12] F dipende dalla coppia (f, K): la prova ne dà la levigatezza per la coppia scelta, ma non prova (e non serve) che F sia indipendente da f. La conclusione del Teorema U2 non richiede questa indipendenza.
*Prova.* (1) *Scelte.* Sia K_1 un compatto con K ⊂ Ω_1 := int K_1 ⊂ K_1 ⊂ Ω e siano r, 𝒱 dati da KMS 19.10 per (f, K_1). 𝒱 contiene un insieme {g : ‖g − f‖_{C^k(K′)} < η} con k ∈ ℕ, K′ compatto, η > 0 (base della topologia C^∞ compatto-aperta). Sia ρ > 0 con B̄_ρ(y) ⊂ Ω per y ∈ K_1 e χ ∈ C_c^∞(B_ρ(0)) con χ ≡ 1 su B_{ρ/2}(0).
(2) *Realizzazione liscia dei getti.* Per (y, j) ∈ Ω_1 × J^r definisco
g_{y,j}(z) := f(z) + χ(z − y)Σ_{|α|≤r}(j_α − ∂^αf(y))(z − y)^α/α!.
Poiché χ ≡ 1 vicino a y, j^r_yg_{y,j} = j (SymPy A1). La perturbazione ha norma C^k(K′) ≤ C_1|j − j^r_yf| con C_1 dipendente solo da χ, k, r, ρ: scelgo ε_0 := η/(2C_1). Allora g_{y,j} ∈ 𝒱 per (y, j) ∈ 𝒲. La mappa (y, j, z) ↦ g_{y,j}(z) è C^∞ in tutte le variabili (composizione di f, delle sue derivate, di χ e di polinomi).
(3) *Buona definizione.* Pongo F(y, j) := D(g_{y,j})(y) per (y, j) ∈ 𝒲. Sia g ∈ 𝒱 e y ∈ Ω_1 con j := j^r_yg tale che (y, j) ∈ 𝒲. Allora g e g_{y,j} stanno entrambi in 𝒱 e hanno lo stesso r-getto in y ∈ K_1; KMS 19.10 dà Dg(y) = D(g_{y,j})(y) = F(y, j^r_yg). La condizione (y, j^r_yg) ∈ 𝒲 va richiesta esplicitamente: g ∈ 𝒱 controlla g − f solo in C^k(K′), che può non controllare il getto d'ordine r (precisazione rispetto alla NOTE di F6, che non la dichiarava).
(4) *Liscezza.* Sia c: ℝ → 𝒲, s ↦ (y(s), j(s)), una curva C^∞. La famiglia G(s, z) := g_{c(s)}(z) è liscia in (s, z) per (2); per la regolarità di D, (s, z) ↦ D(G(s, ·))(z) è liscia; la composizione con s ↦ (s, y(s)) dà s ↦ D(g_{c(s)})(y(s)) = F(c(s)) liscia. Per il teorema di Boman F è C^∞ su 𝒲 (aperto di ℝ^N × ℝ^M). Se la definizione di regolarità ammette famiglie con parametri in varietà di dimensione qualsiasi, la conclusione è immediata (parametro (y, j) ∈ 𝒲) e Boman non serve. ∎
*Commento.* KMS 18.16 non è usato: la sola cosa che serve è che le realizzazioni dei getti formino una famiglia liscia **nel parametro getto**, cosa che la formula (2) dà esplicitamente. U2-a è la **versione locale di KMS 18.16 sull'intorno 𝒱 di 19.10**: 18.16 richiede un ordine finito globale, qui basta quello locale di 19.10 (CIT-AUDIT-8, riga A6 e §5 punto 5).

**Teorema U2 (prova scritta).** Dizionario 𝓓^{NL}_n := {y^β∏_{i=1}^{ℓ}∂^{α_i}u_{c_i} : |β| ≤ n, ℓ ≤ n, |α_i| ≤ n, 1 ≤ c_i ≤ q} (monomi nel getto). Nelle ipotesi del Lemma U2-a, per ogni compatto 𝒞 ⊂ 𝒲, ogni ℓ ∈ ℕ, ogni M > 0 ed ε > 0 esiste P ∈ span_{ℚ(i)}𝓓^{NL}_n (n abbastanza grande) tale che per ogni g ∈ 𝒱 con (y, j^r_yg) ∈ 𝒞 per y ∈ K e ‖g‖_{C^{r+ℓ}(K)} ≤ M:
‖Dg − P[g]‖_{C^ℓ(K)} ≤ ε.
*Prova.* Sia ψ ∈ C_c^∞(𝒲) con ψ ≡ 1 su un intorno di 𝒞; ψF ∈ C_c^∞(ℝ^{N+M}) e, come in 1.1, esiste un polinomio P in (y, j) a coefficienti in ℚ(i) con ‖F − P‖_{C^ℓ(𝒞)} ≤ ε′. Per y ∈ K, Dg(y) − P[g](y) = (F − P)(y, j^r_yg) (Lemma U2-a). Per la regola della catena (Faà di Bruno) ∂^γ_y[(F − P)(y, j^r_yg)], |γ| ≤ ℓ, è somma di derivate di F − P di ordine ≤ |γ|, valutate in (y, j^r_yg) ∈ 𝒞, per prodotti di derivate di g di ordine ≤ r + |γ|, limitate da costanti dipendenti da M. Quindi ‖Dg − P[g]‖_{C^ℓ(K)} ≤ C(ℓ, r, M)ε′. ∎

**Confine (prova scritta).** (a) *Ordine solo localmente finito nel getto.* D(u) := Σ_kψ_k(u)∂_x^ku con ψ_k ∈ C_c^∞((k, k+1)) è locale e regolare; vicino a ogni f (su K compatto, dove |f| è limitato) solo finiti termini sono attivi, ma nessun livello fisso di 𝓓^{NL} approssima D uniformemente su tutti i g limitati in C^r(K) con |g| arbitrario. (b) *sin u non è globale.* Per ogni polinomio P in (y, getto) e costanti g ≡ c: P[c](y_0) = P(y_0, c, 0, …, 0) è un polinomio in c, e sup_{c∈ℝ}|P(y_0, c, 0…) − sin c| ≥ 1 (grado ≥ 1: diverge; grado 0: sup_c|a − sin c| ≥ 1). Sine-Gordon non è nella chiusura uniforme globale; lo diventa con la famiglia di atomi {e^{iku}, e^{λu}} (§5: rappresentazione esatta e polinomializzazione).

### 1.3 U3(c) simboli e N2
**Triage:** N2 PROVABLE AS STATED; U3(c) AFTER WEAKENING: prova completa per i moltiplicatori di Fourier e per i simboli a supporto compatto in x, con la continuità di Op: S^{m′} → L(H^s, H^{s−m′}) presa da Hörmander III (Thm 18.1.13, numero **da verificare**) per il caso dipendente da x.

Notazione: S^m = S^m_{1,0}(ℝ^d × ℝ^d), seminorme |p|_{m,j} = sup_{|α|+|β|≤j}sup⟨ξ⟩^{−m+|α|}|∂_ξ^α∂_x^βp|. Per moltiplicatori p(ξ): ‖p(D)‖_{H^s→H^{s−m}} = sup_ξ|p(ξ)|⟨ξ⟩^{−m} (Plancherel; esatto).

**Teorema N2 (prova scritta; classico, novità ≤ 2/10).** Sia φ ∈ C^∞([0,∞)) non crescente, φ = 1 su [0,1], φ = 0 su [2,∞), ψ(r) := φ(r) − φ(2r) (supporto in [1/2, 2]), ψ_k(ξ) := ψ(2^{−k}|ξ|). Per ε ⊂ ℕ_{≥1} sia m_ε(ξ) := ⟨ξ⟩^mΣ_{k∈ε}ψ_k(ξ). Allora (i) {m_ε} è limitato in S^m uniformemente in ε; (ii) per ε ≠ ε′, ‖m_ε(D) − m_{ε′}(D)‖_{H^s→H^{s−m}} ≥ 1. Quindi nessun insieme numerabile è denso, per la norma H^s → H^{s−m}, in {Op(p) : |p|_{m,j} ≤ C}.
*Prova.* (i) Su supp ψ_k, |ξ| ≍ 2^k; ogni derivata in ξ di ψ_k porta un fattore 2^{−k} ≍ ⟨ξ⟩^{−1}; in ogni ξ al più due ψ_k sono non nulli. (ii) Se k ∈ ε ∖ ε′, nei punti con ψ_k = 1 (|ξ| = 2^k) i ψ_j, j ≠ k, sono nulli (ψ ≥ 0 e Σψ_j ≤ 1; SymPy A2), quindi |m_ε − m_{ε′}|⟨ξ⟩^{−m} = 1 lì (A2b). La famiglia ha la cardinalità del continuo ed è 1-separata. ∎

**Teorema U3(c) (prova scritta, con l'avvertenza del triage).** Sia m < m′. (a) *Moltiplicatori.* Per ogni p ∈ S^m indipendente da x esistono p_n nel dizionario esplicito 𝓢_n := {ξ^γχ(2^{−j}ξ) : |γ|, j ≤ n} (χ := φ(|·|)) con ‖p_n(D) − p(D)‖_{H^s→H^{s−m′}} → 0 per ogni s. (b) *Simboli a supporto compatto in x.* Se p ∈ S^m e p(x, ξ) = 0 per x ∉ K compatto, con θ ∈ C_c^∞ e θ ≡ 1 vicino a K, gli atomi θ(x)x^βξ^γχ(2^{−j}ξ) danno p_n → p nelle seminorme di S^{m′}, quindi Op(p_n) → Op(p) in L(H^s, H^{s−m′}) per la continuità citata.
*Prova.* Coda: (1 − χ(ξ/R))p ha seminorme S^{m′} ≤ C_jR^{m−m′}|p|_{m,j} (sul supporto ⟨ξ⟩ ≳ R, quindi ⟨ξ⟩^{m−m′} ≤ CR^{m−m′}; le derivate cadute su χ(ξ/R) danno R^{−|α|} ≍ ⟨ξ⟩^{−|α|}) (SymPy A3). Testa: p_R := χ(ξ/R)p ha supporto in K × B_{2R}. Scelgo 2^j ≥ 2R, così χ(2^{−j}ξ) ≡ 1 su B_{2R}; approssimo p_R con un polinomio q in (x, ξ) in C^J(supp θ × B̄_{2^{j+1}}) (Weierstrass in C^J). Poiché p_R = θ(x)χ(2^{−j}ξ)p_R, la differenza p_R − θχ(2^{−j}·)q = θχ(2^{−j}·)(p_R − q) è supportata nel compatto fisso supp θ × B̄_{2^{j+1}}, dove le seminorme S^{m′} di ordine ≤ J sono controllate dalla norma C^J (Leibniz, con costanti che dipendono da θ, χ, j); e θχ(2^{−j}·)q è combinazione finita di atomi. Per i moltiplicatori la norma dell'operatore è sup|·|⟨ξ⟩^{−m′}, controllata da |·|_{m′,0}. ∎
**N2 + U3(c) = confine netto:** densità numerabile in norma con perdita di un ε di ordine, impossibile senza perdita.

**Atomi a parametro continuo (prova scritta).** Per 0 < s, s′ < m′: sup_ξ||ξ|^s − |ξ|^{s′}|⟨ξ⟩^{−m′} ≤ C|s − s′| con C = max(1/(e(m′ − max(s,s′))), 1/(e·min(s,s′))). *Prova.* |r^s − r^{s′}| ≤ |s − s′||log r|r^{max} per r ≥ 1 e ≤ |s − s′||log r|r^{min} per r < 1; sup_{r≥1}r^{−a}log r = 1/(ea), sup_{r<1}r^b|log r| = 1/(eb). ∎ L'ordine s è un parametro continuo: con s ∈ ℚ l'esattezza vale solo nel limite. Simboli razionali P(ξ)/Q(ξ), Q senza zeri reali: v = Q(D)^{−1}P(D)u ⟺ Q(D)v = P(D)u (lemma di dilatazione locale, ovvio): un'incognita ausiliaria rende il simbolo razionale un sistema locale (§1.7).

### 1.4 U3(d) memoria completamente monotona
**Triage:** (i) e (ii) PROVABLE AS STATED; (iii) PROVABLE AS STATED per t^{−β}; velocità per nuclei c.m. generali NOT JUSTIFIED (resta candidato, open_questions Q1).

Sia k completamente monotono e localmente integrabile su (0, ∞). Per Bernstein (CON-FONTE classica) k(t) = ∫_{[0,∞)}e^{−λt}dμ(λ) con μ ≥ 0; k ∈ L^1(0,T) ⟺ ∫min(T, 1/λ)dμ(λ) < ∞ (Tonelli: ∫_0^Te^{−λt}dt = (1 − e^{−λT})/λ ≍ min(T, 1/λ)).

**Teorema U3(d) (prova scritta).**
(i) *Rappresentazione diffusiva esatta.* Per f ∈ L^∞(0,T): (k ∗ f)(t) = ∫w(t, λ)dμ(λ), dove w(·, λ) è l'unica soluzione di ∂_tw = −λw + f, w(0, λ) = 0. L'equazione con memoria k ∗ f è quindi **esattamente** un sistema locale in t aumentato con una variabile continua λ (nessuna derivata in λ: è una famiglia di EDO lineari parametrizzata da λ).
(ii) *Convergenza senza velocità per ogni k c.m. in L^1_loc.* Esistono somme finite k_J(t) = Σ_{i≤J}μ_ie^{−λ_it} (μ_i ≥ 0) con ‖k − k_J‖_{L^1(0,T)} → 0; quindi ‖(k − k_J) ∗ f‖_{L^∞(0,T)} ≤ ‖k − k_J‖_{L^1(0,T)}‖f‖_{L^∞} → 0, e k_J ∗ f è un sistema locale aumentato con J incognite (immersione markoviana).
(iii) *Velocità per k = t^{−β}, 0 < β < 1.* Con nodi λ_j = e^{jh}, pesi hλ_j^β/Γ(β) (troncati a s_min ≤ jh ≤ s_max) l'errore relativo della somma infinita è ≤ 2(cos a)^{−β}/(e^{2πa/h} − 1) **uniformemente in t > 0** per ogni a ∈ (0, π/2); il troncamento costa, per t ∈ [δ, T], al più T^βe^{βs_min}h/((1 − e^{−βh})Γ(β)) + C(h, β)T^βexp(−e^{s_max}δ + βs_max)/Γ(β) in errore relativo. Quindi errore relativo ε su [δ, T] con O(log(1/ε)·(β^{−1}log(1/ε) + log(T/δ))) esponenziali.
*Prova.* (i) w(t, λ) = ∫_0^te^{−λ(t−s)}f(s)ds (SymPy A7); |w(t,λ)| ≤ ‖f‖_∞∫_0^te^{−λ(t−s)}ds, integrabile in dμ perché k ∈ L^1(0,T); Fubini dà ∫w dμ = ∫_0^t(∫e^{−λ(t−s)}dμ)f(s)ds = (k ∗ f)(t). (SymPy F5, k = 1/(1+t).)
(ii) [fix DICT-4: la versione precedente trascurava λ < ε_0, e se μ({0}) > 0 quella parte non è piccola: per k = 1 + e^{−t} l'errore era T.] Scrivo μ = μ({0})δ_0 + μ′ con μ′({0}) = 0. L'atomo in 0 dà il termine costante μ({0})·1 = μ({0})e^{−0·t}, che è già un atomo del dizionario e si tiene **esattamente** (nodo λ_0 = 0, peso μ({0})). Per μ′: fissato η > 0, scelgo Λ > 1 con ∫_{λ>Λ}dμ′/λ < η e ε_0 < 1 con Tμ′((0, ε_0)) < η; questo è possibile perché μ′ è finita sui compatti di [0, ∞) (da ∫min(T,1/λ)dμ < ∞) e μ′((0, ε_0)) → μ′(∅) = 0 per ε_0 → 0 (continuità dall'alto, perché μ′({0}) = 0). Partiziono [ε_0, Λ] in celle I_i con λ_i ∈ I_i e diam I_i ≤ η/(T²μ′([ε_0,Λ]) + 1), e pongo k_J := μ({0}) + Σμ′(I_i)e^{−λ_it}. Allora ∫_0^T|k − k_J| ≤ ∫_{(0,ε_0)}∫_0^Te^{−λt}dt dμ′ + ∫_{λ>Λ}∫_0^Te^{−λt}dt dμ′ + Σ_i∫_{I_i}∫_0^T|e^{−λt} − e^{−λ_it}|dt dμ′. Il primo termine è ≤ Tμ′((0, ε_0)) < η, il secondo ≤ ∫_{λ>Λ}dμ′/λ < η. Per il terzo |e^{−λt} − e^{−λ_it}| ≤ t|λ − λ_i| ≤ T diam I_i, quindi è ≤ T²diam I_i·μ′([ε_0,Λ]) ≤ η. Totale < 3η. L'enunciato (ii) resta invariato (la somma finita contiene ora il nodo λ = 0). (SymPy F5b: convergenza osservata per k = 1/(1+t), senza velocità dichiarata.)
(iii) Γ(β)t^{−β} = ∫_0^∞e^{−λt}λ^{β−1}dλ = ∫_ℝexp(−e^st + βs)ds. Con s = σ − log t l'integrando è t^{−β}G(σ), G(σ) := exp(−e^σ + βσ), e la somma h Σ_j exp(−e^{jh}t + βjh) è t^{−β} volte la regola dei trapezi per G sulla griglia traslata hℤ + log t. G si estende analiticamente alla striscia |Im σ| < π/2 con |G(σ + iy)| = exp(−e^σcos y + βσ), e ∫_ℝ|G(x + iy)|dx = Γ(β)(cos y)^{−β}. Il teorema classico sull'errore dei trapezi per funzioni analitiche in una striscia (Trefethen–Weideman, SIAM Rev. 56 (2014), Thm 5.1; CON-FONTE **non letta**: CIT-AUDIT-8 §5 segnala che il Thm 5.1 non è stato letto, quindi numero e costante della stima restano da controllare sulla fonte) dà |h Σ_jG(jh + c) − ∫G| ≤ 2M(a)/(e^{2πa/h} − 1), M(a) = Γ(β)(cos a)^{−β}, uniformemente nella traslazione c: dividendo per Γ(β) si ottiene l'errore relativo uniforme in t. Code: per jh < s_min, exp(−e^{jh}t) ≤ 1 e Σ_{jh<s_min}he^{βjh} ≤ he^{βs_min}/(1 − e^{−βh}); per jh > s_max e t ≥ δ, la somma è dominata da una serie geometrica nel primo termine exp(−e^{s_max}δ + βs_max); dividere per Γ(β)t^{−β} ≥ Γ(β)T^{−β}. Il conteggio segue scegliendo h ≍ 2πa/log(1/ε), s_min ≍ −β^{−1}log(1/ε) − log T, s_max ≍ log(1/δ) + log log(1/ε). (SymPy A8: errore relativo ≤ stima, t da 10⁻⁶ a 10⁶.) ∎
*Caputo.* k = t^{−α}/Γ(1−α), μ = λ^{α−1}dλ/(Γ(α)Γ(1−α)) (SymPy A7b): il frazionario temporale è un caso di (i)–(iii).

### 1.5 Ritardo come sistema aumentato (fix F4) e N3 ristretto
**Triage:** RIT-1 PROVABLE AS STATED; N3 PROVABLE AFTER WEAKENING (fix F4: solo sistemi ODE lineari a dimensione finita; distanza esattamente 1 su ℝ, ≥ 1 su (0, T)).

**Teorema RIT-1 (prova scritta).** Siano τ > 0, T > 0, u ∈ C^1([−τ, T]). La funzione w(t, θ) := u(t − θ) su [0,T] × [0,τ] è l'unica w ∈ C^1([0,T] × [0,τ]) con
w_t + w_θ = 0,  w(t, 0) = u(t) (t ∈ [0,T]),  w(0, θ) = u(−θ) (θ ∈ [0,τ]),
e u(t − τ) = w(t, τ). Quindi ogni equazione con ritardo costante F(u(t), u′(t), u(t − τ)) = 0 è equivalente al sistema locale (u, w) formato da F(u, u′, w(·, τ)) = 0, dall'equazione di trasporto e dall'accoppiamento al bordo θ = 0, con la storia come dato iniziale. Il ritardo sta nella classe L⁺ (legge locale con variabili aggiunte, aumento infinito-dimensionale), come Caffarelli–Silvestre (§1.6).
*Prova.* w(t, θ) = u(t − θ) soddisfa le tre condizioni (SymPy A5). Unicità: se w̃ le soddisfa, z := w − w̃ ha z_t + z_θ = 0 con z(t, 0) = 0 e z(0, θ) = 0; lungo le caratteristiche s ↦ (t_0 + s, θ_0 + s) la derivata di z è z_t + z_θ = 0; ogni caratteristica nel rettangolo, percorsa all'indietro, incontra {t = 0} o {θ = 0}, dove z = 0. ∎

**Teorema N3 (prova scritta).** Sia S_τ l'operatore di ritardo e ℛ l'insieme delle risposte ingresso-uscita dei sistemi lineari a dimensione finita e coefficienti costanti, stabili, a stato iniziale nullo: H = Dδ + h∗, h(t) = Ce^{At}B 1_{t>0}.
(a) Su L²(ℝ): dist(S_τ, ℛ) = 1 in norma operatoriale. (b) Su L²(0, T) con T > τ (S_τf(t) = f(t − τ)1_{t>τ}, h ristretto a (0,T), nessuna ipotesi di stabilità): dist(S_τ, ℛ) ≥ 1.
*Prova.* (a) Il simbolo di H ∈ ℛ è una funzione razionale propria R(iω) senza poli sull'asse immaginario, la norma operatoriale è sup_ω|e^{−iτω} − R(iω)|. R(iω) → c ∈ ℂ per |ω| → ∞; dato η > 0, per ω ≥ ω_0 si ha |R(iω) − c| < η, e su [ω_0, ω_0 + 2π/τ] e^{−iτω} percorre tutto il cerchio unitario, quindi c'è ω con e^{−iτω} = −c/|c| (qualsiasi punto se c = 0) e |e^{−iτω} − c| = 1 + |c|. Dunque sup ≥ 1 + |c| − η ≥ 1 − η, per ogni η. L'uguaglianza vale per H = 0 (|e^{−iτω}| = 1). (SymPy A6: 200 razionali casuali, min 1,0029; Padé [3/3] sup 2, piccolo solo su banda limitata.)
(b) Sia φ ∈ C_c^∞((0, T − τ)) con diam supp φ < τ e f_ω(t) := φ(t)e^{iωt}. Allora S_τf_ω = φ(t − τ)e^{iω(t−τ)}, a supporto disgiunto da quello di φ; Hf_ω = Dφe^{iωt} + h ∗ f_ω e ‖h ∗ f_ω‖_{L²(0,T)} → 0 per ω → ∞ (h è liscia su [0,T]: integrando per parte, |(h ∗ f_ω)(t)| ≤ C/ω uniformemente). Quindi ‖(S_τ − H)f_ω‖² → ‖φ‖² + |D|²‖φ‖² ≥ ‖f_ω‖². (SymPy F4: rapporto ≥ 1,0071 per ω = 200, 400.) ∎
*Lettura.* N3 dice solo che il ritardo non è nella chiusura in norma dei sistemi **ODE a dimensione finita**; non dice che il ritardo non abbia una legge locale: ce l'ha con l'aumento di RIT-1. Padé approssima solo su bande di frequenza limitate.

### 1.6 Frazionari (S8-NLOC confluisce qui)
**Triage:** CS-1 PROVABLE AS STATED (costante esplicita); il frazionario temporale è U3(d).

**Teorema CS-1 (prova scritta; fonte: Caffarelli–Silvestre, Comm. PDE 32 (2007) 1245–1260, CON-FONTE da verificare il numero del teorema; qui prova autosufficiente via Fourier).** Siano 0 < s < 1, f ∈ H^s(ℝ^d), φ_s(r) := (2^{1−s}/Γ(s))r^sK_s(r) (K_s Bessel modificata), e Û(ξ, y) := f̂(ξ)φ_s(|ξ|y) per y > 0. Allora:
(i) div_{x,y}(y^{1−2s}∇_{x,y}U) = 0 in ℝ^d × (0, ∞) (in senso distribuzionale, e classico per y > 0), U(·, y) → f in H^s per y → 0;
(ii) −y^{1−2s}∂_yU(·, y) → c_s(−Δ)^sf in H^{−s} per y → 0, con c_s = 2^{1−2s}Γ(1−s)/Γ(s); se f ∈ H^{2s} la convergenza è in L².
Il laplaciano frazionario è quindi un **sistema locale aumentato** (equazione ellittica degenere in una variabile in più, con accoppiamento di tipo Neumann al bordo y = 0): classe L⁺.
*Prova.* (i) In Fourier in x: div(y^{1−2s}∇U) = y^{1−2s}(ΔU + U_yy + (1−2s)y^{−1}U_y), cioè −|ξ|²Û + Û_yy + (1−2s)y^{−1}Û_y = 0; con r = |ξ|y diventa φ″ + (1−2s)r^{−1}φ′ − φ = 0. Con φ = r^sg si ottiene l'equazione di Bessel modificata d'ordine s per g, quindi le soluzioni sono r^sI_s, r^sK_s; r^sK_s è limitata su (0,∞) e tende a 0 all'infinito. Normalizzazione: K_s(r) = (Γ(s)/2)(r/2)^{−s}(1 + o(1)) per r → 0, quindi φ_s(0+) = 1 (SymPy A4). 0 ≤ φ_s ≤ 1 (φ_s è decrescente: φ_s′ = −(2^{1−s}/Γ(s))r^sK_{1−s} < 0, usando (r^sK_s)′ = −r^sK_{s−1} e K_{−ν} = K_ν); convergenza dominata: ‖U(·,y) − f‖²_{H^s} = ∫⟨ξ⟩^{2s}|f̂|²|φ_s(|ξ|y) − 1|² → 0.
(ii) −y^{1−2s}∂_yÛ = −y^{1−2s}|ξ|φ_s′(|ξ|y)f̂ = (2^{1−s}/Γ(s))|ξ|^{2s}h(|ξ|y)f̂, h(r) := r^{1−s}K_{1−s}(r). h è decrescente con h(0+) = 2^{−s}Γ(1−s) (SymPy F6), quindi (2^{1−s}/Γ(s))h(0+) = c_s e |c_sh(|ξ|y)/h(0+) − c_s| ≤ 2c_s; per convergenza dominata ∫⟨ξ⟩^{−2s}|ξ|^{4s}|f̂|²|…|² → 0 per f ∈ H^s (perché ⟨ξ⟩^{−2s}|ξ|^{4s} ≤ ⟨ξ⟩^{2s}), e analogamente in L² per f ∈ H^{2s}. ∎ (Costante di Neumann verificata in SymPy A4 per s = 0,25; 0,5; 0,8.)
**Tabella dei frazionari.** Spaziale (−Δ)^s: atomo |ξ|^{2s} (U3(c), parametro s ∈ ℚ, esatto nel limite) o sistema aumentato CS-1 (esatto). Temporale (Caputo, Riemann–Liouville): memoria c.m., U3(d) (esatto con variabile continua λ; somme finite con velocità log).

### 1.7 U4 (sistemi)
**Triage:** PROVABLE AS STATED (parte di densità); la struttura algebrica è di S8-SYS.

**Teorema U4 (prova scritta).** Sia 𝓓^{(k)}_n := {E_{ij} ⊗ D : D ∈ 𝓓_n, 1 ≤ i, j ≤ k}. (a) Ogni enunciato di densità U1–U3 vale componente per componente per gli operatori matriciali k × k (le topologie sono prodotti finiti). (b) L'annullatore relativo al livello n di u ∈ C^∞(Ω)^k, {Q ∈ span 𝓓^{(1×k)}_n : Qu = 0}, è il nucleo della Gram a blocchi di (D e_c ⊗ u_c)_{D,c}, cioè C3-L1 per righe. (c) Simboli razionali e memoria a somma di esponenziali sono sistemi locali aumentati: Q(D)v = P(D)u (dilatazione), w_j′ = −λ_jw_j + f (immersione markoviana).
*Prova.* (a) Ovvia: convergenza in un prodotto finito ⟺ convergenza di ogni componente. (b) Qu = Σ_{D,c}q_{D,c}D u_c = 0 ⟺ il vettore q annulla la forma quadratica ‖Σq_{D,c}Du_c‖². (c) §1.3 e §1.4(i). ∎
**Da S8-SYS (inbox, TABELLA 27/10):** a coefficienti costanti l'oggetto è M_u = R^{1×k}/Ann(u); il misfit di Gram si applica per componenti senza fenomeni nuovi, **salvo** che il test d'identificazione richiede l'indipendenza R/𝔭-lineare di μ_𝔭 funzioni (molteplicità di Bass), non solo "∉ EP" (SYS-EX). Il prodotto di Euler ZXZ di Dirac 1+1 ha tempi b(t, ξ) non polinomiali in ξ: i fattori sono moltiplicatori di Fourier non locali (U3), non flussi di termini locali.

### 1.8 Tabella per classe (fix F3: enunciati separati, non un teorema-ombrello)
| classe | dizionario | topologia della densità | modello di dato | esattezza / confine | stato |
|---|---|---|---|---|---|
| locali lineari (Peetre) | 𝓓^{loc} | τ₁ | DM3 | polinomi puri ⟺ ordine globale finito (N0) | prova scritta |
| coefficienti singolari | atomi \|x−x_0\|^{−j}, log | C^m(K) → L^p(K) | DM3 | fuori da Peetre su Ω; x_0 ∈ ℚ^d | prova scritta (densità) |
| locali non lineari regolari | 𝓓^{NL}, {e^{iku}, e^{λu}} | C^ℓ(K) sui g con getti in un compatto 𝒞 ⊂ 𝒲 | DM3 | ordine localmente finito anche nel getto; sin u non globale | prova scritta |
| simboli S^m | 𝓢_n (θ(x)x^βξ^γχ(2^{−j}ξ)) | L(H^s, H^{s−m′}), m′ > m | DM3 | impossibile con m′ = m (N2) | prova scritta (dip. da x: continuità Op da verificare) |
| memoria c.m. | 𝓔_n (e^{−λt}) | L^1 sul nucleo ⇒ L^∞ → L^∞ | DM3 | esatta con λ continua; velocità log per t^{−β} | prova scritta |
| ritardo | trasporto aumentato | esatto (RIT-1) | DM3 | non nella chiusura dei sistemi ODE finiti (N3) | prova scritta |
| frazionari spaziali | \|ξ\|^{2s} o CS-1 | esatto (CS-1) | DM3 | s ∈ ℚ: esatto nel limite | prova scritta |
| sistemi | ⊗ Mat_k | prodotto | DM3 | identificazione: S8-SYS | prova scritta |
| continui qualsiasi (U5) | polinomi di funzionali | uniforme sui compatti di dati | — | nessuna velocità né identificazione | **parcheggiato**; noto: Prenter 1970 **solo per Hilbert**, Fréchet da altra fonte (non verificata) |
Non esiste una topologia unica in cui 𝓓_∞ "tiene conto di tutto" (fix F3): la tabella è il contenuto positivo.


---

## 2. Il teorema negativo N1 (cammino critico; kill-argument in `KILL_ARGUMENT_N1.md`)
**Triage complessivo.** N1(i) PROVABLE AS STATED (classico, novità ≤ 2/10); N1(ii) = Teorema A (§3.3) più C3-P1 e P4-T5 (già DIMOSTRATI nel LEDGER); N1(iii) AFTER WEAKENING (serve N ≥ 2: per N = 1 è falso, vedi sotto); N1(iv) AFTER WEAKENING (due modelli di calcolo separati, fix O9/O10); N1(v) PROVABLE AS STATED in forma rafforzata (magro **e** trascurabile nel senso della prevalenza; anche per polinomi differenziali, fix F10); N1(vi) **ritirato** e sostituito dal teorema di rango §2.6 (fix F1). N1(vi) originale è **FALSO**: enunciato e controesempio in §2.6bis (confermato da AUDIT_S8-DICT §0).

### 2.1 N1(i) — rappresentazione esatta (Baire)
**Enunciato (prova scritta).** Sia X un F-spazio (spazio vettoriale topologico metrizzabile completo) di dimensione infinita, o un suo traslato affine, e sia 𝒜 un insieme numerabile di mappe continue a_k: P_k → X con P_k ⊂ ℝ^{p_k} σ-compatto (atomi con finiti parametri continui; i coefficienti di una combinazione lineare finita sono parametri anch'essi). Allora ∪_k a_k(P_k) è magro in X. In particolare, per ogni dizionario numerabile, anche con finiti parametri continui per atomo, gli operatori rappresentabili esattamente formano un insieme magro in ognuna delle classi: coefficienti a ∈ C^∞(Ω) in ∂_t − a∂_x (traslato affine di C^∞(Ω)); non linearità f ∈ C^∞(J^k); simboli S^m (Fréchet); nuclei di Hilbert–Schmidt L²(Ω × Ω).
*Prova.* a_k(P_k) è unione numerabile di immagini continue di compatti, quindi di compatti. Un compatto C di X ha interno vuoto: se contenesse x + V con V intorno di 0, V ⊂ C − x sarebbe contenuto in un intorno compatto di 0, e uno spazio vettoriale topologico di Hausdorff localmente compatto ha dimensione finita (Riesz). C è chiuso (X di Hausdorff), quindi raro. Baire. ∎ Combinazioni lineari: span(D_1, …, D_n) con coefficienti in ℂ^n è unione numerabile di immagini di compatti di ℂ^n. Novità ≤ 2/10 (O10).
*Applicazione alle classi elencate [fix DICT-14].* L'enunciato richiede mappe a_k **continue** (oppure, in alternativa, un'immagine σ-compatta), e questa ipotesi va verificata per ogni classe citata. Non è automatica: |ξ|^s non è un simbolo liscio in ξ = 0, e s ↦ ⟨ξ⟩^s è continua a valori in S^m solo per s < m. Nel pacchetto i parametri sono razionali e i dizionari numerabili: ogni a_k ha allora dominio numerabile, l'immagine è numerabile, e la conclusione (insieme magro) vale senza alcuna continuità, perché un punto è un compatto. L'esito non cambia.

### 2.2 N1(ii) — nessun dato finito certifica il fit o l'identificazione
Due livelli. (a) *Classe esatta dentro un livello*: C3-P1[M2] (DIMOSTRATO), C3-P1[gen] (CON-FONTE verificata, Malgrange, Ω convesso), P4-T5 (DIMOSTRATO come enunciato). (b) *Livelli del dizionario*: Teorema A (§3.3), parte (ii) con dati approssimati e parte (iii) con dati **esatti** finiti (nuova in questa fase, prova scritta).

### 2.3 N1(iii) — non monotonia per dati in forma chiusa
**Enunciato (prova scritta; corretto: serve N ≥ 2).** Siano N = 1 + d ≥ 2, Ω connesso, u ∈ EP(Ω) con u ≢ 0, D := dim R·u < ∞ (C3-L3). Per ogni n con C(n+N−1, N−1) > D e per ogni L ∈ **Ann(u)** con deg L ≥ 1 [fix DICT-6: senza "L ∈ Ann(u)" l'inclusione è falsa, per esempio u = e^t, L = τ + 5, oppure u = e^{−t}sin x, L = ∂_x]: Ann(u) ∩ R_{≤n} ⊋ (L) ∩ R_{≤n}. A ogni livello alto il nucleo di Gram è strettamente più grande delle conseguenze di qualunque singola legge.
*Prova.* La mappa R_{≤n} → R·u, Q ↦ Qu, ha nucleo Ann(u) ∩ R_{≤n} e immagine di dimensione ≤ D, quindi dim(Ann(u) ∩ R_{≤n}) ≥ C(n+N, N) − D. Inoltre (L) ∩ R_{≤n} = L·R_{≤n−deg L} ha dimensione C(n − deg L + N, N) ≤ C(n − 1 + N, N). Poiché C(n+N, N) − C(n+N−1, N) = C(n+N−1, N−1) > D, la prima dimensione supera la seconda. Infine (L) ∩ R_{≤n} ⊂ Ann(u) ∩ R_{≤n} perché L ∈ Ann(u) e Ann(u) è un ideale; con la disuguaglianza fra le dimensioni l'inclusione è stretta. ∎
*Perché N ≥ 2.* Per N = 1 (EDO a coefficienti costanti) Ann(u) è principale, generato dal polinomio minimo di grado D, e (P_min) ∩ ℂ[τ]_{≤n} = Ann(u) ∩ ℂ[τ]_{≤n} per ogni n: la non monotonia non c'è. [fix DICT-6, nota precisata] Per N = 1 vanno distinte due differenze. La differenza dim R_{≤n} − dim((L) ∩ R_{≤n}) è costante, uguale a deg L per n ≥ deg L; è questa che calcola SymPy B1. La differenza dim(Ann(u) ∩ R_{≤n}) − dim((L) ∩ R_{≤n}) si stabilizza invece a deg L − D (con L ∈ Ann(u), quindi P_min | L), ed è 0 quando L = P_min. Per N ≥ 2 la seconda differenza cresce come n^{N−1} (SymPy F10). Esempio esatto (F6-DICT, dict_checks C1–C3): u = e^{−t}sin x; livello {∂_t, ∂_x²}: nucleo di dimensione 1 (calore); livello {∂_t, ∂_x², 1}: dimensione 2 (anche ∂_t + 1). Conseguenza per R2 (§3.5): il fallimento della coerenza diagnostica dati in forma chiusa.

### 2.4 N1(iv) — uscite finite: due modelli di calcolo
**Enunciato (prova scritta).** (a) *Modello (T).* Sia Φ una procedura qualsiasi (anche non calcolabile, con oracolo per u) le cui uscite sono stringhe finite su un alfabeto finito, interpretate da una mappa fissata stringa ↦ operatore. L'insieme degli operatori che Φ emette, anche come limite stabilizzato di una successione di uscite (alla Gold), è al più numerabile. Poiché ogni membro della famiglia non numerabile {∂_t − c∂_x : c ∈ ℝ} è identificato da sue soluzioni opportune (C3-T4), per tutti i c salvo un insieme numerabile Φ non emette mai ∂_t − c∂_x, su nessun dato. In (T) l'identificazione esatta universale è impossibile, anche nel limite alla Gold; resta possibile la **convergenza topologica** (uscite q_n → c).
(b) *Modello (BSS).* Con uscite reali esatte la stabilizzazione esatta in tempo finito è possibile: CONV-T1 (S8-CONV, DM2) dà O_K = P per K ≥ K* quando Ann(u) = (P), senza conoscere deg P; K* non è certificabile (CONV-T1(7)) né limitato in funzione del grado (CONV-T1(6)).
(c) *In entrambi i modelli* distinguere Ann(u) = 0 da Ann(u) ≠ 0 non è possibile nemmeno nel limite, con nessuna successione di regole (CONV-T2, S8-CONV, DM2, jet di funzioni intere): la proprietà "Ann(u) ≠ 0" è verificabile nel limite ma non decidibile nel limite, con qualunque successione di regole. [fix DICT-15, allineato a CONV-7: la lettura come classe Σ⁰₂ ∖ Π⁰₂ è solo un commento, non parte dell'enunciato.]
*Prova di (a).* Le stringhe finite sono numerabili; una successione stabilizzata ha per limite una stringa; l'immagine di un insieme numerabile è numerabile. ∎ (b) e (c) sono enunciati di S8-CONV, importati con il loro modello. Il corollario di CONV-T2 sulla "classe principale nel limite" è stato ritirato da S8-CONV (CONV-Q10) e qui non è usato.

### 2.5 N1(v) — la u generica non ha legge nel dizionario (anche non lineare)
**Lemma ND (non degenerazione; prova scritta).** Siano D_1, …, D_M operatori differenziali lineari di ordine finito a coefficienti C^∞(Ω) e U ⊂ Ω aperto non vuoto. Esiste w ∈ C_c^∞(U) con D_1w, …, D_Mw linearmente indipendenti **se e solo se** D_1|_U, …, D_M|_U sono linearmente indipendenti su ℂ come operatori.
*Prova.* (⇒) Ovvia. (⇐) Sia r l'ordine massimo e, per y ∈ U, L_i(y): J^r_y → ℂ la forma lineare j ↦ (D_i applicato a un qualsiasi rappresentante di j)(y). Sia S := {(L_1(y)(j), …, L_M(y)(j)) : y ∈ U, j ∈ J^r} ⊂ ℂ^M. Se span S ≠ ℂ^M, esiste c ≠ 0 con Σc_iL_i(y)(j) = 0 per ogni y ∈ U e ogni j, cioè Σc_iD_i = 0 su U: escluso. Quindi esistono y_1, …, y_M ∈ U e getti j_1, …, j_M con det[L_i(y_k)(j_k)] ≠ 0; perturbando, i y_k si prendono distinti (il determinante è continuo in y_k a getti polinomiali fissati). Sia w := Σ_kχ(· − y_k)p_k con p_k polinomio di getto j_k in y_k e χ cutoff ≡ 1 vicino a 0, a supporti disgiunti contenuti in U. Allora D_iw(y_k) = L_i(y_k)(j_k) e la matrice di valutazione è invertibile: le funzioni D_iw sono indipendenti. ∎ (SymPy F1: D_1 = ∂_x, D_2 = x∂_x sono dipendenti in ogni punto come forme sul getto, ma w = x dà 1, x indipendenti.)

**Lemma ND-NL (prova scritta).** Siano Q_1, …, Q_M polinomi differenziali (polinomi nel getto j^r u con coefficienti C^∞(Ω)), linearmente indipendenti su ℂ come funzioni su U × J^r. Esiste w ∈ C_c^∞(U) con Q_1[w], …, Q_M[w] linearmente indipendenti. *Prova.* Identica: S := {(Q_i(y, j))_i : y ∈ U, j ∈ J^r} genera ℂ^M, altrimenti un c ≠ 0 darebbe Σc_iQ_i ≡ 0 su U × J^r; si realizzano i getti in punti distinti con cutoff disgiunti. ∎ (SymPy F2: u², uu_x, u_x².)

**Teorema N1(v) (prova scritta).** Sia V_0 ⊂ V_1 ⊂ … una filtrazione di spazi di dimensione finita di polinomi differenziali in u a coefficienti C^∞(Ω) (in particolare: operatori lineari del dizionario; oppure polinomi differenziali di ordine ≤ n, grado ≤ n, coefficienti polinomiali in y di grado ≤ n). Sia B_n := {u ∈ C^∞(Ω) : ∃P ∈ V_n ∖ {0}, P[u] = 0}. Allora:
(a) B_n è chiuso e raro, quindi ∪_nB_n è **magro** in C^∞(Ω);
(b) B_n è **trascurabile nel senso della prevalenza** (shy: Christensen, Israel J. Math. 13(3–4) (1972) 255–260, riferimento da CIT-AUDIT-8 §5; Hunt–Sauer–Yorke, Bull. AMS 27 (1992) 217–238, CON-FONTE da verificare la numerazione), quindi ∪_nB_n è shy: la u generica non soddisfa alcuna equazione del dizionario sia in senso topologico sia in senso di misura.
Le stesse conclusioni valgono in H^m(Ω) per i livelli lineari di ordine ≤ m (D_i continui H^m → L²).
*Prova.* Sia P_1, …, P_M una base di V_n **adattata al grado**, cioè con parti omogenee di grado massimo P_i^{top} linearmente indipendenti. Esiste: sia V_n^{≤e} il sottospazio degli elementi di grado ≤ e; per ogni e si sceglie un complemento di V_n^{≤e−1} in V_n^{≤e}; gli elementi del complemento hanno grado esattamente e e parti top indipendenti (una combinazione con parte top nulla avrebbe grado < e, quindi starebbe in V_n^{≤e−1}, quindi sarebbe nulla); parti top di gradi diversi sono indipendenti perché omogenee di gradi diversi. Sia e_i := deg P_i.
*Chiuso:* se u_k ∈ B_n, u_k → u, con c^{(k)} nella sfera unitaria di ℂ^M e Σc^{(k)}_iP_i[u_k] = 0, per compattezza c^{(k)} → c (sottosuccessione), e u ↦ P_i[u] è continua C^∞ → C^∞: Σc_iP_i[u] = 0, u ∈ B_n.
*Direzione di fuga:* per il Lemma ND-NL esiste w con P_1^{top}[w], …, P_M^{top}[w] indipendenti, e (Lemma di indipendenza, MF3(a), §3.2) funzionali ℓ_1, …, ℓ_M (integrali contro funzioni test) con det(ℓ_j(P_i^{top}[w])) ≠ 0. Per ogni u, P_i[u + sw] = s^{e_i}P_i^{top}[w] + (termini di grado < e_i in s), quindi p_u(s) := det(ℓ_j(P_i[u + sw])) è un polinomio in s il cui coefficiente di s^{Σe_i} è det(ℓ_j(P_i^{top}[w])) ≠ 0 (multilinearità per righe; SymPy B5). Se u + sw ∈ B_n, le funzioni P_i[u + sw] sono dipendenti e p_u(s) = 0. Quindi {s ∈ ℝ : u + sw ∈ B_n} ha al più Σe_i elementi.
(a) Raro: B_n è chiuso e, per ogni u, u + sw ∉ B_n per s ≠ 0 piccolo, quindi il complementare è denso. Baire.
(b) Prevalenza: C^∞(Ω) è un gruppo abeliano polacco; la misura di probabilità μ := legge di sw con s uniforme in [0,1] ha supporto compatto e, per ogni u, μ(B_n − u) = |{s ∈ [0,1] : u + sw ∈ B_n}| = 0; B_n è boreliano (chiuso). Per definizione B_n è shy, e un'unione numerabile di insiemi shy è shy (Christensen). In H^m: stessa prova con D_i: H^m → L² continui. ∎
*Caso lineare.* e_i = 1 e P_i^{top} = P_i: serve solo il Lemma ND, cioè l'indipendenza degli atomi su ℂ. **La correzione F10 è chiusa**: per atomi non lineari si usa il termine di grado massimo in s con una base adattata al grado, e l'ipotesi di non degenerazione delle parti omogenee è automatica dopo la scelta della base.
**Corollario N1(v)-ALG (prova scritta).** Prendendo per V_n tutti i polinomi differenziali di ordine ≤ n, grado ≤ n, coefficienti polinomiali in y di grado ≤ n: l'insieme delle u ∈ C^∞(Ω) **differenzialmente algebriche su ℂ(y)** (che soddisfano una equazione differenziale algebrica non banale a coefficienti polinomiali) è magro e shy. La u generica è differenzialmente trascendente. (Fatto probabilmente noto per le funzioni intere generiche; fonte non trovata: da cercare in CIT-AUDIT-8.)
**Legame con F4-ALG** (ALG-T1, DIMOSTRATO nel LEDGER: I(u) = [F] ⟺ trdeg ℂ⟨u⟩ = ∞ per evolutive, u analitica). N1(v)-ALG dice che, fra tutte le u, quelle con I(u) ≠ 0 formano un insieme magro e shy (non raro: è denso, perché contiene i polinomi; fix DICT-16); ALG-T1 dice che, fra le soluzioni di un'evolutiva F, identificano F esattamente quelle di grado di trascendenza infinito. Insieme danno la versione non lineare della tricotomia (§2.7): una legge non lineare esiste solo per u eccezionali, e per quelle u l'identificazione esatta richiede trdeg = ∞.

### 2.6 Teorema di rango: (a′) e (b′) (fix F1, sostituisce N1(vi))
**Quadro.** Classe strutturata L_θ := L_0 + Σ_{k=1}^Kθ_kT_k, con L_0, T_k operatori lineari fissati C^∞(Ω, ℂ^p) → C^∞(Ω, ℂ^q) (q equazioni; caso scalare p = q = 1) e coefficienti incogniti θ = (θ_1, …, θ_K) ∈ Θ := C^∞(Ω, 𝔽^K), 𝔽 ∈ {ℝ, ℂ}. Dato u, la **mappa residuo puntuale** è A_u(y): 𝔽^K → ℂ^q ≅ ℝ^{2q}, A_u(y)ϑ := Σϑ_kT_ku(y) (ℝ-lineare). Φ_u(θ) := Σθ_kT_ku. Una **legge** per u è un θ ∈ Θ con L_θu = 0. La classe è **identificabile** da u se ker Φ_u = 0, cioè se **una legge, quando esiste, è unica** (unicità condizionata all'esistenza); u **falsifica** la classe se non esiste alcuna legge. [fix DICT-2: la definizione precedente, "esiste al più una legge", rendeva identificabile per vacuità ogni classe falsificata da u, e quindi falsi (IV), (a′) e i "⟺" di (b′) e del trasporto; per esempio u = t con la classe ∂_t + θ_0 + θ_1∂_x non ha leggi, perché in t = 0 l'equazione diventa 0 = −1. Con la definizione nuova (II) caratterizza esattamente l'identificabilità.] (Per dati e coefficienti reali si sostituisce ℝ^{2q} con ℝ^q.)

**Significato e ipotesi (post-Gate 8, O5 di ATTACK-8).**
- In questo paragrafo e nei corollari "identificabile" ha il significato **ID-ker** (etichette di NOTAZIONE v6): ker Φ_u = 0.
- ID-ker dà l'unicità della legge **solo sotto (H-ex)**, cioè l'ipotesi che una legge della classe esista per u. Senza (H-ex) ID-ker non è un'identificazione.
- Controesempio (ATTACK-8 O5, SymPy F): classe u_t = a u_xx + b u con a, b costanti, u = t + sin x. Si ha Φ_u(a, b) = −a sin x + b(t + sin x), quindi ker Φ_u = 0. Ma bt + (b − a) sin x ≡ 1 non ha soluzione, quindi nessuna legge della classe esiste.
- Ogni "identificabile" di RANGO (II)–(IV), (a′), (b′) e del trasporto va letto come "ID-ker; unicità sotto (H-ex)". Gli enunciati (II) e (IV) non cambiano.

**Teorema RANGO (prova scritta).**
(I) *Struttura (= VAR-T1(a)).* L'insieme delle leggi è vuoto oppure θ⁰ + ker Φ_u.
(II) *Identificabilità.* ker Φ_u = 0 (in Θ = C^∞ o C^0) ⟺ A_u(y) è iniettiva per y in un sottoinsieme denso di Ω.
(III) *Non falsificabilità.* Se A_u(y) è suriettiva per **ogni** y ∈ Ω, allora per ogni L_0 esiste una legge θ ∈ C^∞. Se invece esiste y_0 con −L_0u(y_0) ∉ im A_u(y_0), u falsifica la classe (nessuna legge, nemmeno continua).
(IV) *Conteggio.* Se in un punto y la mappa A_u(y) è iniettiva e suriettiva, allora K·dim_ℝ𝔽 = dim_ℝ(valori). Quindi: se K·dim_ℝ𝔽 > dim_ℝ(valori) la classe non è mai identificabile (A_u(y) non è iniettiva in nessun punto e ker Φ_u ≠ 0 per (II): se una legge esiste, non è unica); se K·dim_ℝ𝔽 < dim_ℝ(valori) la condizione di (III) non vale in nessun punto e l'esistenza di una legge è un vincolo puntuale non banale (−L_0u(y) in un sottospazio proprio per ogni y).
*Prova.* (I) Se θ⁰, θ¹ sono leggi, Φ_u(θ¹ − θ⁰) = L_{θ¹}u − L_{θ⁰}u = 0; viceversa ogni θ⁰ + ker Φ_u è una legge. (II) (⇐) Φ_u(θ) = 0 ⇒ θ(y) ∈ ker A_u(y) = 0 per y in un denso ⇒ θ ≡ 0 per continuità. (⇒) Se l'insieme di iniettività non è denso, esiste un aperto U dove A_u(y) non ha rango pieno per nessun y (il rango è semicontinuo inferiormente, quindi {rango pieno} è aperto e il suo complementare chiuso). Il rango massimo r su U è raggiunto su un aperto U′ ⊂ U (ancora per semicontinuità), dove il rango è costante = r: ker A_u è un fibrato vettoriale liscio di rango K·dim_ℝ𝔽 − r ≥ 1 su U′ (A_u(y) è liscia in y perché u è liscia), e ha una sezione locale liscia non nulla; moltiplicata per un cutoff a supporto in U′ dà θ ≠ 0 in ker Φ_u. (III) Se A_u(y) è suriettiva ovunque, A_u(y)A_u(y)^T (aggiunta reale) è invertibile e θ(y) := −A_u(y)^T(A_u(y)A_u(y)^T)^{−1}L_0u(y) è liscia e risolve L_θu = 0. Se −L_0u(y_0) ∉ im A_u(y_0), nessun valore θ(y_0) risolve l'equazione in y_0. (IV) Algebra lineare. ∎ (SymPy B3, F11.)

**Corollari (prova scritta; ciascuno è (I)–(IV) applicato).**
- **(a′) = VAR-N1 (identificazione intrinseca vuota).** Classe "tutti gli operatori" d'ordine ≤ m: L_0 = ∂_t, T_k = tutti i ∂^α con |α| ≤ m, α ≠ (1, 0, …, 0) (incluso α = 0, moltiplicazione), 𝔽 = ℂ, q = 1, con d ≥ 1 variabili spaziali oppure m ≥ 2 [fix DICT-2, punto P10 del KA: serve per avere K ≥ 2]: K ≥ 2 e K·2 > 2, quindi **mai identificabile** (ker Φ_u ≠ 0) (θ = φ(T_2u, −T_1u, 0, …) ∈ ker Φ_u); se u non ha zeri, la componente α = 0 è u(y) ≠ 0, A_u(y) è suriettiva ovunque e **ogni u ha una legge**: né identificabile né falsificabile. Nella forma algebrica di S8-VAR: Ann_{𝒦[∂]}(u) = 𝒦[∂](∂_t − u_t/u) + 𝒦[∂](∂_x − u_x/u) (stesso fatto, contato una volta: fix F9).
- **(b′) Schrödinger, V complesso.** L_0 = i∂_t + ∂_x², T_1 = −1, 𝔽 = ℂ, K = q = 1: A_u(y)ϑ = −ϑu(y) è iniettiva ⟺ u(y) ≠ 0. Identificabile ⟺ int Z(u) = ∅ (= VAR-T1(c)); se u non ha zeri, non falsificabile.
- **(b′) Schrödinger, V reale.** 𝔽 = ℝ, K = 1, valori in ℂ ≅ ℝ²: identificabile ⟺ int Z(u) = ∅, ma **falsificabile**. [fix DICT-3] **Se u non ha zeri**: una legge con V reale esiste ⟺ Im((iu_t + u_xx)/u) ≡ 0, e allora V = (iu_t + u_xx)/u. **In generale** vale solo (⇒): se una legge con V reale esiste, allora Im((iu_t + u_xx)/u) ≡ 0 su {u ≠ 0} e inoltre iu_t + u_xx = 0 su Z(u); il viceversa è un problema di divisione (open_questions Q3). Il "⟺" scritto prima per ogni u è falso: con u = x³ il quoziente 6/x² è reale ma non si estende a x = 0 (dict_check G1); con u = e^{−it}(x + x²) si ha A_u(t, 0) = 0 ma −L_0u(t, 0) = −2e^{−it} ≠ 0, quindi u falsifica la classe per (III). Esempio senza zeri: u = e^{−it}(2 + cos x) + itx/5 falsifica la classe (SymPy B3b: V(0,3; 0,7) ha parte immaginaria −0,0249), mentre gli stati stazionari danno V reale (B3c). **Identificabile e falsificabile**: l'asse giusto non è la "taglia" della classe ma il conteggio K·dim_ℝ𝔽 contro dim_ℝ(valori) (predizione del PLAN confermata).
- **Trasporto a(t, x).** u_t = a(t,x)u_x, tutto reale, K = q = 1: identificabile ⟺ {u_x ≠ 0} denso; a = u_t/u_x (B3d). Quindi (H-ID) di I-LIM **vale** con coefficienti dipendenti da (t, x) quando {u_x ≠ 0} è denso (correzione di "(H1) fallisce sempre", O1).
- **Classe normalizzata e u = t − x² (DEVIL-6 C3).** L_0 = ∂_t, T = (∂_x, 1): A_u(0,0) = (u_x, u)(0,0) = (0, 0) e L_0u(0,0) = 1: u falsifica la classe vicino a 0 (B4). Nelle classi normalizzate "ogni u ha una legge" è falso.
- **Sistemi: caso magnetico fuori da RANGO [fix DICT-5; post-Gate 8: MAG-1…MAG-4 di AUDIT_S8-DICT_rev2, O15 di ATTACK-8].** Lo Schrödinger magnetico (∇ − iA)²u = Δu − 2iA·∇u − i(div A)u − |A|²u **non** è lineare in θ = A: il termine div A contiene derivate dell'incognita e |A|² è quadratico. Il quadro L_0 + Σθ_kT_k quindi non si applica, e la frase originale ("spazio affine sui campi a divergenza nulla") è falsa. Controesempio: u = (2 + cos x)e^{iy}, B = (sin y, 0), che ha div B = 0 ma div(|u|²B) ≠ 0.
  - **La riga canonica è SYS-N3 (S8-SYS, DIMOSTRATO)** [O15]. In SYS-N3 la divergenza è quella di ρ²B: div_x(ρ²B) = 0, ρ = |u|. Non è div B = 0.
  - *Convenzione:* i u_t = −(∇ − iA)²u + Vu.
  - *Classe [MAG-1]:* A, V ∈ C^∞(J × Ω; ℝ) dipendono da (t, x); J è un intervallo, Ω ⊂ ℝ^n aperto, n ≥ 2, e ∇, ∇^⊥ agiscono nelle sole variabili spaziali.
  - *Identità delle differenze.* Sia (A, V) una legge reale per u. Sia B ∈ C^∞(J × Ω; ℝ^n) con **supp B ⊂ {u ≠ 0}** [MAG-3]. Poniamo δV := −2iB·∇u/u − i div B − 2A·B − |B|² su {u ≠ 0} e δV := 0 fuori da supp B. Allora (A + B, V + δV) è una legge reale per u se e solo se div_x(|u|²B) = 0; infatti Im(δV)·|u|² = −div_x(|u|²B).
  - *Se supp B incontra Z(u)* servono in più due cose: un'estensione liscia di δV attraverso Z(u), e B·∇u = 0 su Z(u). Questo caso non è trattato qui, come in DICT-3.

  **Corollario DICT-MAG-NU (di SYS-N3(c), localizzato; non è un claim autonomo [O15]).**
  - *Ipotesi:* le ipotesi della classe [MAG-1]; u ∈ C^∞(J × Ω) soluzione con una legge reale (A, V); u ≢ 0 [MAG-2] (se u ≡ 0 ogni coppia è una legge e la non unicità è banale); U ⊂ {u ≠ 0} aperto di J × Ω; χ ∈ C_c^∞(U) reale non nulla.
  - *Costruzione:* B := |u|^{−2}(∂_{x_2}χ, −∂_{x_1}χ, 0, …, 0).
  - *Tesi:* (A + B, V + δV) è una seconda legge reale e liscia per u, con **campo magnetico diverso** [MAG-4]: dB ≢ 0, quindi non è un cambio di gauge.
  - *Prova.*
    - Su U, dove u ≠ 0, è SYS-N3(a)(b) con k := −|u|²B = −∇^⊥χ, che ha div_x k = 0: la coppia A′ = A − k/ρ² = A + B, V′ = V + δV è ammissibile.
    - Fuori da supp χ si ha B = 0 e δV = 0, quindi la coppia è liscia su tutto J × Ω anche se u ha zeri fuori da U.
    - dB ≢ 0: a un t fissato con χ(t, ·) ≢ 0, la componente (1,2) di dB vale −div_{12}(|u|^{−2}∇_{12}χ). Questa non è identicamente nulla per il principio del massimo, come in SYS-N3(c) (fix SYS-10 per n ≥ 3, sulle fette).
  - *Contributo rispetto a SYS-N3:* SYS-N3 chiede u ≠ 0 ovunque; qui u può avere zeri fuori da supp χ.
  - *Caso statico:* se la classe richiede A, V indipendenti da t, la costruzione dà una legge della classe solo per u stazionaria (|u| indipendente da t) e χ = χ(x). Con u non stazionaria la non unicità statica non è dimostrata [MAG-1].
  - *Verifiche:* `sympy/s8dict_checks3.py` R3; `work/CHECK-F8/sympy/dict2_mag.py` 16/16 (anche con zeri di u, dipendenza dal tempo e n = 3).
  - *Stato* (AUDIT_S8-DICT_rev2): DIMOSTRATO dopo MAG-1 e MAG-2, come corollario di SYS-N3(c). L'audit dichiara di non essere del tutto indipendente, perché la costruzione viene dall'aggiudicazione del KA.
*Caso intermedio non coperto (open_questions Q3).* Se A_u(y) perde rango su un insieme Z e −L_0u ∈ im A_u su Z, l'esistenza di una legge liscia è un problema di divisione (Malgrange–Łojasiewicz) e non è caratterizzata qui.

### 2.6bis N1(vi) originale: FALSO (registrazione con controesempio)
**Enunciato originale** (F6-DICT, NOTE.md e VERDETTO.md): "L_{u,i} = u∂_i − ∂_iu annulla ogni u; quindi, con coefficienti C^∞(t, x), ogni u ha una legge e **nessun operatore è identificato**; in particolare (H1) di I-LIM **fallisce sempre** con coefficienti dipendenti da (t, x)."
**Stato: FALSO.** È vera solo la prima frase: L_{u,i}u = u∂_iu − (∂_iu)u = 0, cioè nella classe non normalizzata di tutti gli operatori del primo ordine ogni u ha una legge. Sono false le due conclusioni.
- *Controesempio a "nessun operatore è identificato" e a "(H1) fallisce sempre".* Classe u_t = a(t, x)u_x, cioè L_0 = ∂_t, T_1 = −∂_x, θ = a ∈ C^∞(Ω) reale. Per u = t + x si ha u_x = 1 ovunque: A_u(y) = −u_x(y) è iniettiva in ogni punto, quindi per RANGO (II) ker Φ_u = 0. La legge esiste (a ≡ 1) ed è unica: l'operatore ∂_t − ∂_x è identificato, con coefficiente ammesso dipendente da (t, x). Più in generale, con {u_x ≠ 0} denso la legge a = u_t/u_x, se esiste, è unica (corollario "Trasporto" di §2.6; SymPy B3d; DEVIL-6 O1).
- *Controesempio a "ogni u ha una legge" nelle classi normalizzate.* Con L_0 = ∂_t, T = (∂_x, 1) e u = t − x² si ha A_u(0, 0) = (0, 0) e L_0u(0, 0) = 1: u falsifica la classe (§2.6, SymPy B4).
L'osservazione corretta che sopravvive è il corollario (a′): nella classe di **tutti** gli operatori di ordine ≤ m (non normalizzata, con d ≥ 1 oppure m ≥ 2) la legge, se esiste, non è mai unica, ed esiste sempre per le u senza zeri. Ritiro confermato da AUDIT_S8-DICT §0 ("N1(vi) originale: ritiro corretto, FALSO").

### 2.7 Tricotomia riscritta (asse identificabile / falsificabile)
1. **Classi né identificabili né falsificabili** (conteggio in eccesso e u senza zeri, per esempio "tutti gli operatori", (a′)): ogni u ha una legge e la legge non è unica; l'esistenza non spiega nulla.
2. **Classi identificabili** (conteggio ≤ dim dei valori e A_u iniettiva su un denso): la legge, se esiste, è unica; con conteggio in difetto la classe è anche falsificabile (Schrödinger con V reale). Le classi di dimensione numerabile (span 𝓓_∞: Weyl, polinomi differenziali) sono il caso estremo: la u generica non ha legge (N1(v), magro e shy); per le u speciali l'identificazione è esatta livello per livello (G-R, §3.5), certificabile solo nel limite (N1(ii), (iv)).
3. **Classi compatte intermedie** 𝒦_R (livello più limiti sulle norme): identificazione nel limite con modulo di stabilità sotto (H-ID) (I-LIM, §4), che vale per esempio con un solo coefficiente e residuo non degenere.
Il contenuto di un dizionario universale sta nella filtrazione e nei certificati relativi al livello, non nella chiusura (osservazione dell'utente sullo spazio di Hilbert).

### 2.8 Kill-argument su N1 (sintesi; testo completo in `KILL_ARGUMENT_N1.md`)
Thread d'attacco e d'aggiudicazione eseguiti in questa sessione, separati (revisore fresco non disponibile: stessa prassi di DEVIL-6; il passaggio indipendente spetta a DEVIL-8). Esito: **PASS-WITH-NOTES**. Effetti sul testo: N1(iii) ristretto a N ≥ 2; N1(v) rafforzato con la prevalenza (risponde all'obiezione "magro è la categoria sbagliata"); Teorema A(iii) ristretto ad atomi locali (gli atomi non locali restano aperti, Q4); modelli (T) e (BSS) separati in N1(iv).
**Kill-argument indipendente (S-CHECK-F8-DICT, 27/10).** `work/CHECK-F8/KA_DICT_N1_{input,attack,adjudication}.md`, con un subagente nuovo: 11 punti, esito **SURVIVES-WITH-FIXES**. Il KA interno PASS-WITH-NOTES non aveva trovato nessuno dei punti P1–P6. Fix recepiti:
- P1, P2, P10 → DICT-2 (definizione di "identificabile", K ≥ 2);
- P3 → DICT-3 (V reale e zeri di u);
- P4 → DICT-5 (caso magnetico fuori da RANGO);
- P5 → DICT-6 (L ∈ Ann(u) in N1(iii));
- P6 → DICT-1 (Teorema A(iii) senza U_0);
- P7 → DICT-13;
- P8 → DICT-14;
- P9 → DICT-15;
- P11 → DICT-16.


---

## 3. Certificati di misfit MF1–MF3, Teorema A, B2, regole R0–R6, R-STOP, G-R
Livello affine 𝓐_n = {D_0 + Σ_{i=1}^Nc_iD_i}; livello omogeneo span{D_0, …, D_N}. Y è lo spazio normato dove vivono i D_iu (L²(Ω), H^{−k}(Ω), L^1(Ω)); W := span{D_1u, …, D_Nu}. Modello di dato: DM3 (u in H^m, o in L^1_loc per la forma debole); i certificati sono enunciati analitici, la loro calcolabilità è dichiarata in MF3(d).

### 3.1 MF1 — distanza di Hahn–Banach (prova scritta; classica)
**Enunciato.** Y normato (reale o complesso), W ⊂ Y di dimensione finita, v ∈ Y. Allora dist(v, W) = max{|φ(v)| : φ ∈ Y*, ‖φ‖ ≤ 1, φ|_W = 0}, e il massimo è raggiunto. Ogni φ ammissibile dà il limite inferiore dist(v, W) ≥ |φ(v)|/‖φ‖. Quindi: nessun L ∈ 𝓐_n annulla u ⟺ dist(D_0u, W) > 0 ⟺ esiste φ con φ(D_iu) = 0 (i ≥ 1) e φ(D_0u) ≠ 0.
*Prova.* (≥) Per w ∈ W, |φ(v)| = |φ(v − w)| ≤ ‖v − w‖. (≤) Sia δ := dist(v, W) > 0 (W è chiuso perché di dimensione finita; se δ = 0 ogni φ va bene). Su span(W, v) pongo φ_0(w + λv) := λδ; |φ_0(w + λv)| = |λ|δ ≤ ‖λv + w‖ (perché ‖λv + w‖ = |λ|‖v + w/λ‖ ≥ |λ|δ per λ ≠ 0). Hahn–Banach estende φ_0 con norma ≤ 1; φ(v) = δ. ∎

### 3.2 MF2 — Gram (prova scritta; classica) e MF3 — forma debole (prova scritta)
**MF2.** Y di Hilbert, D_1u, …, D_Nu indipendenti: r_n² := min_{L∈𝓐_n}‖Lu‖² = det G(D_0u, D_1u, …, D_Nu)/det G(D_1u, …, D_Nu); il certificato ottimo è φ = ⟨·, res⟩/‖res‖ con res := D_0u − P_WD_0u: φ(D_iu) = 0, φ(D_0u) = r_n. Livello omogeneo: nessun L ≠ 0 nel livello annulla u ⟺ λ_min(G_n(u)) > 0, con λ_min = min_{|c|=1}‖Σc_iD_iu‖² (C3-L1).
*Prova.* Sostituire la prima riga e la prima colonna di G(D_0u, …) con quelle di res = D_0u − Σβ_iD_iu (operazioni elementari che non cambiano il determinante) dà una matrice a blocchi diag(‖res‖², G(D_1u, …)), perché res ⊥ W. φ(D_iu) = ⟨D_iu, res⟩/‖res‖ = 0 e φ(D_0u) = ⟨res + P_WD_0u, res⟩/‖res‖ = ‖res‖. ∎ (dict_checks A1, A2 di F6.)

**MF3 (forma debole; prova scritta).** (a) *Lemma di indipendenza.* f_0, …, f_N ∈ D′(Ω) sono linearmente indipendenti ⟺ esistono ψ_0, …, ψ_N ∈ C_c^∞(Ω), presi da un insieme numerabile Ψ denso in C_c^∞(Ω) fissato, con det(⟨f_i, ψ_j⟩) ≠ 0. (b) Se i D_i sono differenziali a coefficienti lisci, ⟨D_iu, ψ⟩ = ⟨u, D_i^tψ⟩: il certificato usa solo integrali di u, nessuna derivata di u (vale per u ∈ L^1_loc o distribuzione). (c) *Robustezza.* Sia A(u) := (⟨u, D_i^tψ_j⟩)_{ij} (con M ≥ N + 1 funzioni test, matrice M × (N+1)). Se i dati ũ soddisfano |⟨ũ − u, D_i^tψ_j⟩| ≤ δ_{ij}, allora σ_{N+1}(A(u)) ≥ σ_{N+1}(A(ũ)) − ‖(δ_{ij})‖_F (Weyl): il misfit omogeneo è certificato da dati rumorosi se σ_{N+1}(A(ũ)) > ‖δ‖_F. (d) *Semi-decisione (modello (T) con oracolo che restituisce gli integrali ⟨u, D_i^tψ_j⟩ con precisione arbitraria).* Enumerando le (N+1)-uple di Ψ e raffinando la precisione, la ricerca termina se e solo se c'è misfit omogeneo al livello n.
*Prova.* (a) (⇐) Se Σc_if_i = 0 con c ≠ 0, la matrice ha le colonne dipendenti. (⇒) Altrimenti l'immagine della mappa lineare ψ ↦ (⟨f_i, ψ⟩)_i ⊂ ℂ^{N+1} è un sottospazio proprio, ortogonale a qualche c ≠ 0: allora ⟨Σc̄_if_i, ψ⟩ = 0 per ogni ψ, cioè Σc̄_if_i = 0. Esistono quindi ψ_j ∈ C_c^∞ con det ≠ 0, e per continuità del determinante in ψ (topologia di C_c^∞) si possono prendere in Ψ. (b) Definizione di derivata distribuzionale. (c) Weyl per i valori singolari: |σ_k(A) − σ_k(B)| ≤ ‖A − B‖_2 ≤ ‖A − B‖_F (SymPy C3). (d) Se c'è misfit, per (a) esiste una (N+1)-upla in Ψ con det ≠ 0, e con precisione sufficiente l'approssimazione intervallare del determinante esclude lo 0; se non c'è misfit tutti i determinanti sono nulli e nessun intervallo esclude lo 0. ∎
*Prior art:* la forma debole come metodo di stima è in Weak SINDy (Messenger–Bortz, J. Comput. Phys. 443 (2021) 110525); la lettura come certificato di non appartenenza (determinante, robustezza, semi-decisione) non risulta pubblicata (ricerca non estesa).

**MF-C (complemento: coefficienti vincolati; prova scritta).** (a) B ⊂ ℂ^N convesso compatto: min_{c∈B}‖D_0u + Σc_iD_iu‖ = max_{‖φ‖≤1}min_{c∈B}Re φ(D_0u + Σc_iD_iu) (Sion: la funzione è affine reale in c e in φ, B è compatto convesso, la palla duale è convessa e debole* compatta, e il massimo è raggiunto per semicontinuità superiore debole* di φ ↦ min_c). Un φ con min_{c∈B}Re φ(…) > 0 certifica il misfit per tutti i coefficienti in B. (b) Vincoli di cono (per esempio diffusività ≥ 0) sulle coppie di test discretizzate Ac = b: per il lemma di Farkas o esiste c ≥ 0 con Ac = b, o esiste z con A^Tz ≥ 0 e b^Tz < 0, e z è il certificato.

### 3.3 Teorema A (asimmetria fit/misfit; prova scritta)
**Enunciato.** Sia span{D_0, …, D_N} un livello di operatori lineari continui C^∞(Ω) → D′(Ω), linearmente indipendenti su ℂ. Sia U_n := {u : D_0u, …, D_Nu indipendenti} (misfit omogeneo) e F_n := C^∞(Ω) ∖ U_n (fit).
(i) U_n è aperto, e ogni u ∈ U_n ha un certificato finito (N+1 funzioni test di Ψ) valido in un intorno di u. Se i D_i sono operatori differenziali (più in generale, se i trasposti D_i^t conservano C_c^∞), l'intorno si può prendere anche nella topologia indotta da D′ [fix DICT-13: per operatori continui C^∞ → D′ qualsiasi u ↦ ⟨D_iu, ψ⟩ non è continua per la convergenza debole].
(ii) F_n è chiuso. Se i D_i sono differenziali (o soddisfano la conclusione del Lemma ND), F_n ha interno vuoto: **nessun insieme finito di dati approssimati certifica il fit** (ogni insieme {v : |ℓ_j(v) − ℓ_j(u)| ≤ δ}, ℓ_j continui, contiene punti di U_n).
(iii) **Dati esatti finiti.** Se i D_i sono differenziali lineari a coefficienti lisci (atomi **locali**) e ℓ_1, …, ℓ_M sono funzionali lineari continui qualsiasi su C^∞(Ω), allora per ogni u ∈ F_n esiste v ∈ U_n con ℓ_j(v) = ℓ_j(u) per ogni j; v si può prendere vicino quanto si vuole a u. Il fit non è certificabile nemmeno con dati finiti esatti. Lo stesso vale per il fit affine (D_0u ∈ W), che implica il fit omogeneo.
*Prova.* (i) MF3(a) dà ψ con det A(u) ≠ 0. u ↦ A(u) è continua su C^∞, e anche nella topologia di D′ quando D_i^tψ_j ∈ C_c^∞ (operatori differenziali); quindi det A(v) ≠ 0 vicino a u. (ii) F_n chiuso: complemento di (i). Interno vuoto: N1(v)(a) (lineare, con il Lemma ND). Un insieme di dati approssimati contiene un intorno di u, quindi punti di U_n. (iii) Sia Z := ∩_j ker ℓ_j, chiuso di codimensione ≤ M. [fix DICT-1: la versione precedente usava M+1 palle disgiunte B_k dentro un aperto U_0 d'indipendenza, ma l'indipendenza su U_0 non dà quella su ciascuna palla (controesempio dict_check A1: su Ω = (0,1), moltiplicazione per φ_1 con supporto in (0; 0,3) e per φ_3 con supporto in (0,7; 1)); l'ipotesi U_0 era inoltre vuota.] *Aperti d'indipendenza disgiunti.* La prova del Lemma ND (§2.5, con N+1 operatori D_0, …, D_N indipendenti su Ω) dà punti distinti y_0, …, y_N ∈ Ω e polinomi p_0, …, p_N con det[L_i(y_k)(j^r_{y_k}p_k)]_{i,k} ≠ 0. A polinomi p_k fissati il determinante è continuo nei punti, quindi resta ≠ 0 per spostamenti piccoli dei punti. Scelgo così M+1 (N+1)-uple (y^m_0, …, y^m_N), m = 0, …, M, con tutti gli (M+1)(N+1) punti distinti e matrice invertibile per ogni m. Fissato ρ > 0 minore di metà della distanza minima fra questi punti (e della distanza da ∂Ω), pongo O_m := ∪_kB_ρ(y^m_k) e w_m := Σ_kχ_ρ(· − y^m_k)p_k, con χ_ρ cutoff ≡ 1 vicino a 0 e supporto in B_ρ(0). Gli O_m sono aperti a due a due disgiunti (non connessi), w_m ∈ C_c^∞(O_m), e D_iw_m(y^m_k) = L_i(y^m_k)(j^r p_k): la matrice di valutazione è invertibile, quindi D_0w_m, …, D_Nw_m sono indipendenti (già ristrette a O_m). *Sistema.* Σ_mγ_mℓ_j(w_m) = 0 (j = 1, …, M) ha M equazioni e M + 1 incognite: esiste γ ≠ 0, e w := Σγ_mw_m ∈ Z. Sia m_0 con γ_{m_0} ≠ 0. Per località (supp D_iw_m ⊂ supp w_m), su O_{m_0} si ha D_iw = γ_{m_0}D_iw_{m_0}, quindi le D_iw sono indipendenti. Il polinomio s ↦ det(ℓ′_j(D_i(u + sw))), con funzionali ℓ′ scelti per w come in N1(v), ha coefficiente direttore ≠ 0: per s ≠ 0 piccolo v := u + sw ∈ U_n e ℓ_j(v) = ℓ_j(u). ∎
*Nota [fix DICT-1].* L'ipotesi "aperto d'indipendenza U_0" è **tolta**: (iii) vale per ogni livello di operatori differenziali lineari a coefficienti lisci, indipendenti su Ω, senza ipotesi aggiuntive. Gli aperti O_m non sono connessi; la località è l'unica proprietà usata. (Verifica dell'audit, dict_check A2: stessi dati esatti a 10⁻¹⁶, λ_min relativo di v pari a 0,383. SymPy F3 di questa sessione: u = e^{−t}sin x con fit nel livello {∂_t, ∂_x²}, tre funzionali, v con gli stessi dati esatti e λ_min relativo 4,5·10⁻².)
*Atomi non locali* (memoria, simboli): (iii) resta aperta (open_questions Q4): la prova usa la località (D_iw_k supportato in B_k).

### 3.4 B1–B2 — migliore approssimazione con stima (prova scritta)
**B1.** L_n := argmin_{L′∈𝓐_n}‖L′u‖ = D_0 + Σc_iD_i con G′c = −b (G′ Gram di D_1u, …, D_Nu, b_i = ⟨D_iu, D_0u⟩). Per ogni L̃ ∈ 𝓐_n e ogni L con Lu = 0: r_n ≤ ‖L̃u‖ = ‖(L̃ − L)u‖. r_n non cresce con n (livelli annidati).
**B2.** Siano D_1u, …, D_Nu indipendenti, λ_min := λ_min(G′_n) > 0. Per ogni L̃_n = D_0 + Σc̃_iD_i ∈ 𝓐_n, posto η := ‖L̃_nu‖: |c_n − c̃_n| ≤ 2η/√λ_min.
*Prova.* Σ(c_n − c̃_n)_iD_iu = L_nu − L̃_nu ha norma ≤ r_n + η ≤ 2η, e ‖Σδc_iD_iu‖² ≥ λ_min|δc|². ∎ (SymPy C1, 300 prove.) Se L ha coefficienti a_α e L̃_n i loro approssimanti p_α: η ≤ Σ_α‖a_α − p_α‖_{L^∞}‖∂^αu‖_{L²}. **B3** (ottimalità d'ordine dei polinomi via n-larghezze di Kolmogorov, Pinkus 1985) resta **CON-FONTE da verificare** (fonte non letta): non è usato altrove. **B4**: la convergenza dei coefficienti non segue da B2 da sola (λ_min può tendere a 0): serve la compattezza (I-LIM) o il bilanciamento di Lepskii.

### 3.5 Regole R0–R6 (definizioni) e teorema G-R
Le regole sono **definizioni di procedura** (strumenti); il contenuto di teorema sta in R3, nel lemma di trasporto di R6 e in G-R.
- **R0 (filtrazione).** Altezza esplicita, finiti atomi per altezza; si procede per altezza crescente; dentro un'altezza per famiglie (locale lineare → non lineare polinomiale → famiglie non polinomiali (§5) → simboli → memoria → ritardo/frazionari aumentati → singolari).
- **R1 (test al livello n).** Si calcola G_n(u) (o A(u) in forma debole). Dati esatti (BSS): λ_min(G_n) = 0 ⇒ candidato al livello minimo. Dati rumorosi: soglia di R-STOP. Altrimenti certificato di misfit (MF2/MF3) e si passa a n + 1.
- **R2 (coerenza).** Accettato L al livello n_0, per n > n_0 il nucleo deve coincidere con le conseguenze ⟨L⟩_n := {QL : Q} ∩ span 𝓓_n (S4-ID P-a; coefficienti costanti: (L) ∩ R_{≤n}). Nucleo più grande ⇒ dati in forma chiusa o non identificanti (N1(iii), P4-T2).
- **R3 (guadagno esatto di un atomo; prova scritta).** Dato il residuo ottimo res_n (res_n ⊥ W) e un atomo D con P^⊥_WDu ≠ 0: r_{n+1}² = r_n² − |⟨res_n, Du⟩|²/‖P^⊥_WDu‖², con W′ = W ⊕ span(P^⊥_WDu). *Prova.* P_{W′} = P_W + proiezione sulla direzione e := P^⊥_WDu/‖P^⊥_WDu‖; il nuovo residuo è res_n − ⟨res_n, e⟩e, e ⟨res_n, P^⊥_WDu⟩ = ⟨res_n, Du⟩ perché res_n ⊥ W. ∎ (SymPy C2.) Si sceglie l'atomo di guadagno massimo fra i candidati dell'altezza successiva (criterio OLS, Chen–Billings–Luo 1989: prior art). Un atomo con φ_n(Du) = 0 non migliora: il certificato indica la direzione d'arricchimento.
- **R4 (cambio di famiglia; strumento euristico, nessun teorema).** Segnature del residuo: legge di potenza in |reŝ(ξ)| ⇒ |D|^s; correlazione esponenziale nel ritardo temporale ⇒ memoria; fase e^{−iτω} ⇒ ritardo; concentrazione vicino a x_0 ⇒ atomi singolari; dipendenza dall'ampiezza ⇒ grado non lineare; poli mobili e test di Painlevé ⇒ famiglia esponenziale (§5.4). Predizione del PLAN confermata: R4 resta euristica.
- **R5 = R-STOP = CONV-T5 (S8-CONV, importato senza modifiche).** Regola R_δ: m(δ) := min{m : σ_1(Φ_m(ũ)) ≤ δ_m}, uscita λ̃ = vettore singolare minimo di Φ_{m(δ)}(ũ); ramo H (rumore in H^d, δ_m = δ) o ramo L² (limite a priori ‖u‖_{H^{d+s}} ≤ 𝔐, δ_m hölderiano). Garanzia sotto la soglia δ₀(u) = ½min_{m<d}s_m, **non calcolabile dai dati** (CONV-T5(3)). Nel regime senza legge (Ann = 0 relativo al livello) m(δ) → ∞ e l'uscita onesta è il certificato di misfit ai livelli < m(δ). Regime di sola approssimazione: principio di discrepanza o Lepskii su B2 (Mathé–Pereverzev 2003, prior art; nessun teorema nuovo qui).
- **R6 = D4-ENC (cambio di quadro).** Sostituito da §3.6 (R6 recepita, 27/10): lemma R6-T con intrecciamento esatto ENC-C1, ristretto al sottoanello pari ℂ[∂_t, L_q], q dato, Y = C(Ω̄) o L²(Ω) su rettangolo simmetrico attorno a x_0.

**Teorema G-R (prova scritta; DM3 esatto, modello BSS).** Sia n_0 il minimo livello con fit affine e L ∈ 𝓐_{n_0} con Lu = 0. Ipotesi (H-ID): Ann(u) ∩ span 𝓓_n = ⟨L⟩_n per ogni n ≥ n_0 [O13 di ATTACK-8: etichetta unificata con (H-ID) di NOTAZIONE, ipotesi d'unicità dell'identificazione nel limite; qui nella forma esatta, a livello n ≥ n_0]. Allora: (a) R1 si ferma esattamente a n_0 [fix DICT-7: il test di arresto è allineato alla definizione di n_0 tramite il fit affine. R1 calcola r_n = dist(D_0u, W_n), W_n := span{D_iu : i ≥ 1}, con MF2 applicato a una base massimale indipendente di W_n, cioè la Gram del sistema affine aumentato. La versione precedente diceva "λ_min(G′_n) > 0", che non segue dalla minimalità, perché i D_iu con i ≥ 1 possono essere dipendenti anche senza fit affine. Per n < n_0 si ha r_n > 0 per minimalità di n_0, e r_{n_0} = 0] e restituisce il nucleo ⟨L⟩_{n_0} (identificazione modulo conseguenze; se ⟨L⟩_{n_0} ∩ 𝓐_{n_0} = {L}, restituisce L); (b) se (H-ID) fallisce, esiste n_1 ≥ n_0 con nucleo ⊋ ⟨L⟩_{n_1} (si ha sempre ⟨L⟩_n ⊂ nucleo), e R2 lo segnala al livello n_1 (per dimensione); (c) n_0 e n_1 non sono maggiorabili a priori (P4-T5, CONV-T1(6)–(7), N1(ii)); (d) se nessun livello ha fit, R1 produce un certificato di misfit a ogni livello (MF2/MF3) e, sotto le ipotesi di I-LIM, i minimizzatori convergono (§4). ∎ (La prova è la verifica delle definizioni; il contenuto non banale è nei riferimenti di (c).)

---

## 4. I-LIM con (H-ID)
**Triage:** ramo esatto = CONV-T1 (importato); ramo approssimato PROVABLE AS STATED; corollario hölderiano PROVABLE per s = 0 (costante esplicita), AFTER WEAKENING per s ≥ 1 (interpolazione da fonte, da verificare).

**Ramo esatto (S8-CONV, CONV-T1; modello BSS, dato DM2).** Regola L*: m*(K) = min{m ≤ K : N_{m,K} ≠ 0}, O_K = gcd N_{m*(K),K}. Ann(u) = (P) ⇒ O_K = P per K ≥ K*, senza conoscere deg P; uscite distinte ≤ (d+1)(d+2)/2, dove d è il **grado minimo** di una legge, come in CONV-T1(5) [fix DICT-8: la versione precedente usava d anche per la dimensione spaziale; qui le variabili sono (t, x) ∈ ℝ^{1+d′} con d′ = 1, come in CONV]; K* non limitato da funzioni del grado e non certificabile. **Modello per ramo [fix DICT-8, nota O9]:** il ramo esatto vive nel modello BSS (uscite reali esatte), non nel modello (T); il ramo approssimato qui sotto è un enunciato analitico di convergenza, valido in qualunque modello che calcoli i minimizzatori a meno di ε_opt (punto (d)).

**Ramo approssimato (prova scritta; DM3, enunciato analitico, nessun modello di calcolo richiesto).**
*Ipotesi.* Ω ⊂ ℝ^N limitato lipschitziano; u ∈ H^m(Ω); A insieme finito di multi-indici di ordine ≤ m; D_0 atomo fisso di ordine ≤ m; s ∈ ℕ.
(H0) 𝒦_R := {L = D_0 + Σ_{α∈A}c_α(y)∂^α : ‖c_α‖_{C^{s,1}(Ω̄)} ≤ R}; è compatto per la convergenza C^s(Ω̄) (Arzelà–Ascoli sulle derivate d'ordine ≤ s, equi-lipschitziane; la palla C^{s,1} è chiusa per convergenza C^s).
(H-ID) **unicità**: esiste L ∈ 𝒦_R con Lu = 0, e per un R′ ≥ R ogni L′ ∈ 𝒦_{R′} con L′u = 0 coincide con L.
(H2) **approssimazione limitata**: esistono L̃_n ∈ span 𝓓_n ∩ 𝒦_{R′} con ‖L̃_n − L‖_{C^s} ≤ ε_n → 0 (norma sui coefficienti).
**Teorema I-LIM (prova scritta).** (a) Il modulo ω(η) := sup{‖L′ − L‖_{C^s} : L′ ∈ 𝒦_{R′}, ‖L′u‖_{L²} ≤ η} tende a 0 per η → 0. (b) Ogni minimizzatore L_n di ‖L′u‖_{L²} su span 𝓓_n ∩ 𝒦_{R′} (esiste: insieme compatto non vuoto in dimensione finita) soddisfa ‖L_n − L‖_{C^s} ≤ ω(C_uε_n), C_u := Σ_α‖∂^αu‖_{L²}. (c) Con dati ũ, ‖ũ − u‖_{H^m} ≤ δ, ogni minimizzatore L^δ_n di ‖L′ũ‖ soddisfa ‖L^δ_n − L‖ ≤ ω(C_uε_n + 2C_{R′}δ), C_{R′} := ‖D_0‖_{H^m→L²} + |A|R′; scegliendo n(δ) con C_uε_{n(δ)} ≤ δ, L^δ_{n(δ)} → L per δ → 0. (d) Con un errore di ottimizzazione ε_opt (minimizzatore approssimato), si aggiunge ε_opt nell'argomento di ω.
*Prova.* (a) Altrimenti esistono ε_0 > 0 e L′_j ∈ 𝒦_{R′} con ‖L′_ju‖ → 0, ‖L′_j − L‖ ≥ ε_0; per compattezza L′_j → L* in C^s (sottosuccessione), e L* ∈ 𝒦_{R′}. La mappa (coefficienti) ↦ L′u è continua da C^0 a L² (‖(L′ − L″)u‖ ≤ Σ_α‖c′_α − c″_α‖_∞‖∂^αu‖_{L²}), quindi L*u = 0 e ‖L* − L‖ ≥ ε_0, contro (H-ID). (b) ‖L_nu‖ ≤ ‖L̃_nu‖ = ‖(L̃_n − L)u‖ ≤ C_uε_n; poi (a). (c) Per L′ ∈ 𝒦_{R′}: ‖L′ũ − L′u‖ ≤ C_{R′}δ; quindi ‖L^δ_nu‖ ≤ ‖L^δ_nũ‖ + C_{R′}δ ≤ ‖L̃_nũ‖ + C_{R′}δ ≤ ‖L̃_nu‖ + 2C_{R′}δ ≤ C_uε_n + 2C_{R′}δ; poi (a). (d) Identica. ∎
**Quando vale (H2) (prova scritta modulo estensione).** Per il dizionario a coefficienti polinomiali e Ω lipschitziano, (H2) vale con R′ = C_ER + 1, dove C_E è la norma di un operatore d'estensione C^{s,1}(Ω̄) → C^{s,1}(ℝ^N) (estensione di Whitney–Stein, CON-FONTE da verificare; esplicita per Ω scatola con riflessioni di Hestenes): si estende c_α, si regolarizza (‖c_ε‖_{C^{s,1}} ≤ C_ER, c_ε → c_α in C^s), e si approssima c_ε con polinomi in C^{s+1}(Ω̄) (Weierstrass), che controlla anche la norma C^{s,1}.
**Quando vale (H-ID) (dal Teorema RANGO, §2.6).** Un solo coefficiente (|A| = 1, A = {α_1}) e {∂^{α_1}u ≠ 0} denso: (H-ID) vale per ogni R′. Esempio O1: u_t = a(t,x)u_x con {u_x ≠ 0} denso — anche con coefficiente dipendente da (t, x). Con due atomi a residui dipendenti su C^∞ (per esempio ∂_x e 1 nella classe non normalizzata) (H-ID) fallisce.
**Corollario hölderiano (prova scritta per s = 0).** Siano |A| = 1, D_0 = ∂_t, c ∈ C^{0,1}, |∂^{α_1}u| ≥ γ > 0 su Ω̄, e Ω soddisfi la condizione del cono: |B_r(y) ∩ Ω| ≥ κr^N per y ∈ Ω̄, r ≤ r_0. Allora
ω(η) ≤ max{2(2R′)^{N/(N+2)}(η/(γ√κ′))^{2/(N+2)}, 2(η/γ)(κr_0^N)^{−1/2}}, κ′ := κ/2^N,
quindi ‖L^δ_{n(δ)} − L‖_{C^0} = O((ε_n + δ)^{2/(N+2)}).
*Prova.* Se L′u, Lu hanno coefficienti c′, c, allora L′u = (c′ − c)∂^{α_1}u e ‖c′ − c‖_{L²} ≤ ‖L′u‖/γ ≤ η/γ. Sia f := c′ − c, Lip(f) ≤ 2R′, M := ‖f‖_∞ = |f(y_0)|. Su B_ρ(y_0) ∩ Ω con ρ := min(M/(2·2R′), r_0) si ha |f| ≥ M/2, quindi (η/γ)² ≥ (M/2)²κρ^N. Se ρ = M/(4R′): M^{N+2} ≤ 4(4R′)^N(η/γ)²/κ, che dà la prima espressione (a meno della costante scritta, che la maggiora); se ρ = r_0: M ≤ 2(η/γ)(κr_0^N)^{−1/2}. ∎ (SymPy F8: N = 1 su [0,1], costante esplicita, 300 prove.) Per s ≥ 1 l'interpolazione ‖f‖_{C^s} ≤ C‖f‖_{L²}^θ‖f‖_{C^{s,1}}^{1−θ}, θ = 2/(2s+2+N) (esponente verificato per scaling, SymPy E1) è CON-FONTE da verificare (Gagliardo–Nirenberg su domini lipschitziani): il corollario per s ≥ 1 resta **candidato**.

---

## 5. NS-EXPALG: famiglie esponenziali, polinomializzazione, Ax, Painlevé
**Triage:** NS-L1 PROVABLE AS STATED; NS-T1 (trasporto di trdeg) PROVABLE AS STATED senza Ax; Ax: osservazione CON-FONTE **da leggere** (teorema differenziale non letto; riferimento corretto da CIT-AUDIT-8 §5; prima: "verificata", fix DICT-11); kink nucleo 3 PROVABLE AS STATED; 2-kink nucleo 1 solo V-ex; PAINLEVÉ: strumento.

### 5.1 Polinomializzazione esatta
**Lemma NS-L1 (prova scritta).** Sia E[u] un polinomio (a coefficienti in ℂ[y]) nelle derivate ∂^αu con |α| ≥ 1 e negli esponenziali e^{λ_1u}, …, e^{λ_qu} con λ_j = n_jλ, n_j ∈ ℤ (esponenti commensurabili), senza u non derivata. Posto w := e^{λu} (w non si annulla), esistono k ∈ ℕ e un polinomio differenziale Ẽ[w] esplicito con E[u] = w^{−k}Ẽ[w]. Quindi u risolve E[u] = 0 ⟺ w risolve Ẽ[w] = 0, e la corrispondenza fra soluzioni è u ↦ e^{λu}, w ↦ λ^{−1}log w (a meno di 2πi/λ). [fix DICT-10] La direzione w ↦ u richiede un logaritmo globale di w: si assume Ω semplicemente connesso, oppure si legge u come definita modulo (2πi/λ)ℤ. La direzione u ↦ w e le identità di polinomializzazione non richiedono ipotesi su Ω. In particolare:
- sine-Gordon u_xt = sin u (λ = i): 2(ww_xt − w_xw_t) − (w³ − w) = 2iw²(u_xt − sin u) (SymPy D1);
- Liouville u_xt = e^u (λ = 1): vv_xt − v_xv_t − v³ = v²(u_xt − e^u) (D2);
- u_xt = e^u − e^{2u}: ww_xt − w_xw_t − (w³ − w⁴) = w²(u_xt − e^u + e^{2u}) (F9).
*Prova.* ∂_iu = λ^{−1}∂_iw/w; per induzione ∂^αu = λ^{−1}P_α[w]/w^{|α|} con P_α polinomio differenziale (∂_i(P/w^k) = (w∂_iP − kP∂_iw)/w^{k+1}); e^{λ_ju} = w^{n_j}. Sostituendo in E e moltiplicando per una potenza w^k che cancella tutti i denominatori (e le potenze negative di w) si ottiene Ẽ. Le equivalenze seguono da w ≠ 0. ∎ (D4: getti di u razionali in quelli di w.)
*Esponenti non commensurabili* (e^u, e^{√2u}): due variabili w_1 = e^u, w_2 = e^{√2u} con il vincolo differenziale polinomiale √2 w_2∂_iw_1 = w_1∂_iw_2 (i = 0, …, d): sistema polinomiale aumentato (prova identica).
*Restrizione necessaria:* se u compare non derivata, E non si polinomializza (u = λ^{−1}log w).

### 5.2 Trasporto del grado di trascendenza (senza Ax)
**NS-T1 (prova scritta).** Sia u analitica su Ω connesso, w = e^{λu}, ℂ⟨u⟩ e ℂ⟨w⟩ i campi differenziali generati su ℂ. Allora trdeg_ℂ ℂ⟨w⟩ = ∞ ⟺ trdeg_ℂ ℂ⟨u⟩ = ∞.
*Prova.* Sia F_1 := ℂ(∂^αu : |α| ≥ 1). Per NS-L1, ℂ⟨w⟩ = F_1(w) (le derivate di w sono w per polinomi nelle derivate di u, e viceversa le derivate di u sono razionali nel getto di w) e ℂ⟨u⟩ = F_1(u). Aggiungere un elemento cambia il grado di trascendenza al più di 1, quindi trdeg ℂ⟨w⟩, trdeg ℂ⟨u⟩ e trdeg F_1 sono tutti infiniti o tutti finiti. ∎ **Conseguenza [ristretta, fix DICT-9]:** il criterio di F4-ALG (ALG-T1: I(u) = [F] ⟺ trdeg = ∞) vale per equazioni **evolutive**. Si trasporta dalla forma polinomializzata Ẽ alla forma esponenziale E, senza Ax, solo quando E è in una forma evolutiva coperta da ALG-T1, per esempio sine-Gordon in coordinate di laboratorio u_tt = u_xx + sin u. Non si applica alla forma nel cono di luce u_xt = sin u, che non è evolutiva: per quella forma il riferimento ad ALG-T1 è tolto. NS-T1 in sé (equivalenza dei gradi di trascendenza) non dipende dalla forma dell'equazione.
**Dove serve Ax (osservazione, CON-FONTE da leggere [post-Gate 8, CIT-AUDIT-8 §5 punto 2]: Ax, *On Schanuel's conjectures*, Ann. of Math. (2) 93(2) (1971) 252–268, DOI 10.2307/1970774. Il riferimento è confermato; il teorema differenziale non è stato letto sulla fonte. L'etichetta precedente, "verificata per l'enunciato standard" (CIT-AUDIT-6 riga 18, fix DICT-11), scende a "da leggere").** Solo se si vuole trattare e^{u} come **variabile indipendente** accanto al getto di u (dizionario in (getto di u, e^u) senza eliminare u): Ax–Schanuel differenziale dà trdeg_ℂ ℂ(u_1, …, u_n, e^{u_1}, …, e^{u_n}) ≥ n + rango jacobiano, per u_i ℚ-linearmente indipendenti modulo costanti, cioè esclude relazioni algebriche nascoste fra u-getto ed esponenziali. Nel quadro di NS-L1 non serve.

### 5.3 Kink e 2-kink: identificazione nel dizionario esponenziale
Dizionario a 5 atomi {u_xt, sin u, u_xx, u_tt, u} (sine-Gordon nel cono di luce, u_xt = sin u).
**Kink (prova scritta).** u = U(θ), θ = ax + t/a, U = 4 arctan e^θ, a ≠ 0. Allora le cinque funzioni atomo valgono U″, sin U = U″, a²U″, a^{−2}U″, U; U″ e U sono linearmente indipendenti (se aU″ + bU = 0, per θ → +∞ si ha U″ → 0 e U → 2π, quindi b = 0, e poi a = 0 perché U″ ≢ 0), quindi lo span ha dimensione 2 e il nucleo ha **dimensione 3**: u_xt − sin u, u_xx − a²u_xt, u_tt − a^{−2}u_xt. Nel livello affine con D_0 = u_xt il nucleo affine ha dimensione 2: **il kink non identifica sine-Gordon** in questo dizionario (le relazioni del boost di parametro a). (SymPy D3: valori singolari 59, 23, poi ≤ 4·10⁻¹⁵.)
*Precisazione sul calcolo:* U″(θ) = sin U(θ) è l'equazione del pendolo soddisfatta da 4 arctan e^θ (verificata simbolicamente in D3 nei punti di prova); U″ = −2 sech θ tanh θ ≠ 0 per θ ≠ 0.
**2-kink (V-ex, non prova).** Con a_1 = 1/2, a_2 = 2 (SymPy F7, residuo 2,7·10⁻¹⁵) le cinque funzioni hanno rango numerico 4: nucleo 1, sine-Gordon identificato nel dizionario. Una prova richiederebbe l'indipendenza esatta di u_xt, u_xx, u_tt, u per il 2-kink (open_questions Q6).

### 5.4 PAINLEVÉ come strumento (nessun teorema)
Dopo la polinomializzazione NS-L1 l'equazione è polinomiale e il test di Painlevé (Weiss–Tabor–Carnevale, J. Math. Phys. 24 (1983) 522–526; per sine-Gordon in forma polinomiale Weiss, J. Math. Phys. 25 (1984) 13–24, entrambe CON-FONTE da verificare) si applica: è un **criterio diagnostico** per R4 (presenza di poli mobili senza ramificazione suggerisce la famiglia esponenziale e la forma polinomiale) e un controllo di coerenza sul candidato. Non ha contenuto di identificazione e non entra in nessuna garanzia. POLE (Adler–Moser) è di S8-ENC.

---

## 6. Il dizionario 𝓓_∞ esplicito e la sezione per ALGORITMO_ESTESO
**Atomi per famiglia e altezza h** (h = massimo degli indici; finiti atomi per altezza):
| famiglia | atomi di altezza ≤ n | parametri | rappresentazione | topologia / modello | teoremi |
|---|---|---|---|---|---|
| LIN | y^β∂^α | \|α\|, \|β\| ≤ n | esatta per coeff. polinomiali | τ₁ / DM3 | U1, N0 |
| LOC | χ_jy^β∂^α | j ≤ n | densa (ordine localmente finito) | τ₁ / DM3 | U1(a) |
| NL | y^β∏∂^{α_i}u_{c_i} | grado, ordine ≤ n | densa sui compatti di getti | C^ℓ(K) / DM3 | U2, N1(v) |
| EXP | e^{iku}, e^{λu}, λ ∈ ℚ | \|k\| ≤ n | esatta per sine-Gordon, Liouville (via NS-L1) | polinomiale dopo w | NS-L1, NS-T1 |
| SYM | θx^βξ^γχ(2^{−j}ξ), \|ξ\|^s, s ∈ ℚ | j, \|β\|, \|γ\| ≤ n | densa con perdita ε | L(H^s, H^{s−m′}) / DM3 | U3(c), N2 |
| MEM | e^{−λt}, λ = e^{jh}, h = 2^{−n} | \|jh\| ≤ n | esatta con λ continua; somme finite | L^1 sul nucleo / DM3 | U3(d) |
| DEL | trasporto w_t + w_θ = 0, τ ∈ ℚ_+ | τ con denominatore ≤ n | esatta (sistema aumentato) | — / DM3 | RIT-1, N3 |
| FRAC | estensione CS, s ∈ ℚ ∩ (0,1) | denominatore ≤ n | esatta (sistema aumentato) | H^s → H^{−s} / DM3 | CS-1 |
| SING | \|x − x_0\|^{−j}, log\|x − x_0\|, x_0 ∈ ℚ^d | j, altezza di x_0 ≤ n | esatta nel limite | C^m(K) → L^p(K) | U1-b(4) |
| SYS | E_{ij} ⊗ (sopra) | i, j ≤ k | per componenti | prodotto | U4; S8-SYS |
I parametri continui (s, τ, x_0, λ) presi in insiemi numerabili danno esattezza solo nel limite (N1(i), N1(iv)).

**Passi per ALGORITMO_ESTESO (contratto: ogni uscita porta un'etichetta).**
1. *Livello n* (R0): si costruisce span 𝓓_n per altezza e famiglia.
2. *Test* (R1): Gram MF2 su u in DM3, o forma debole MF3 (solo integrali di u). Uscite: "misfit certificato al livello n" (certificato φ o ψ-upla, Σ₁, robusto al rumore se σ_{N+1}(A(ũ)) > ‖δ‖_F) oppure "candidato".
3. *Coerenza* (R2): confronto del nucleo con ⟨L⟩_n ai livelli successivi; incoerenza ⇒ "dati in forma chiusa / non identificanti".
4. *Arricchimento* (R3, R4): guadagno esatto dal certificato; cambio di famiglia euristico (etichetta "euristica").
5. *Arresto* (R5 = R-STOP = CONV-T5): con rumore, garanzia solo sotto una soglia non calcolabile (etichetta "asintotica, non certificata").
6. *Cambio di quadro* (R6, §3.6): solo con q dato, sul sottoanello pari ℂ[∂_t, L_q], dato DM3 su rettangolo simmetrico; certificati trasportati con ψ ↦ ψ∘W.
7. *Uscita finale*, con modello dichiarato: "legge esatta nel limite (BSS, CONV-T1)", "legge approssimata con modulo ω (I-LIM, sotto (H-ID))", "nessuna legge fino al livello n (misfit certificato)". Mai "legge identificata" da dati finiti (N1(ii), Teorema A).

---

## 7. Mappa delle dipendenze e stati dopo l'audit
Gli stati sono quelli proposti da AUDIT_S8-DICT §0, dopo il recepimento dei fix indicati. La registrazione nel LEDGER spetta al coordinatore. "DA AUDITARE" marca il testo nuovo che l'audit non ha scritto.
| ID | stato proposto (dopo audit) | fix recepiti | dipende da |
|---|---|---|---|
| DICT-U1 (U1-a, U1(a), N0) | DIMOSTRATO | — | Peetre (CON-FONTE verificata via KMS 19.1); Banach–Steinhaus |
| DICT-U1b | singolari e densità L^p DIMOSTRATO; velocità 2–3 CON-FONTE da verificare | — | Bernstein/Chebyshev, Jackson, Bagby–Bos–Levenberg |
| DICT-U2 (con U2-a) | DIMOSTRATO | DICT-12; CIT-AUDIT-8 §5 (1, 5) | KMS 19.10 (verificata), Slovák 1987/1988, Boman, Math. Scand. 20 (1967) 249–268, DOI 10.7146/math.scand.a-10835 (enunciato CON-FONTE; la prova non dipende dal numero); U2-a = versione locale di KMS 18.16 sull'intorno di 19.10 |
| DICT-N2 | DIMOSTRATO | — | — |
| DICT-U3c | DIMOSTRATO (moltiplicatori); caso dipendente da x CON-FONTE | — | Hörmander III 18.1.13 (da verificare) |
| DICT-U3d (i), (iii) | DIMOSTRATO | CIT-AUDIT-8 §5 (4) | Bernstein; trapezi in striscia (bordo verificato, dict_check D1); Trefethen–Weideman 2014 Thm 5.1 CON-FONTE non letta |
| DICT-U3d (ii) | DIMOSTRATO dopo DICT-4 | DICT-4 | Bernstein |
| DICT-U3d velocità generale | CANDIDATO (Q1) | — | — |
| DICT-RIT1 | DIMOSTRATO | — | — |
| DICT-N3 (a), (b) | DIMOSTRATO | — | — |
| DICT-CS1 | DIMOSTRATO | — | Caffarelli–Silvestre 2007 (prova autosufficiente) |
| DICT-U4 | DIMOSTRATO | — | S8-SYS |
| DICT-N1 (i), (ii), (iv)(a) | DIMOSTRATO | DICT-14 | C3-P1, P4-T5, C3-T4, Teorema A |
| DICT-N1 (iii) | DIMOSTRATO dopo DICT-6 (N ≥ 2, L ∈ Ann(u)) | DICT-6 | C3-L3 |
| DICT-N1 (iv)(b)(c) | DIMOSTRATO come in AUDIT_S8-CONV | DICT-15 | CONV-T1, CONV-T2 |
| DICT-N1v (ND, ND-NL, (v)-ALG) | DIMOSTRATO | DICT-16; CIT-AUDIT-8 §5 (3) | MF3(a); Christensen, Israel J. Math. 13(3–4) (1972) 255–260; HSY (numerazione da verificare) |
| DICT-RANGO (I)–(III) | DIMOSTRATO come **ID-ker**; unicità della legge solo sotto (H-ex) | O5 | VAR-T1(a) |
| DICT-RANGO (IV), (a′), (b′), trasporto | DIMOSTRATO dopo DICT-2, DICT-3, come **ID-ker**; unicità solo sotto (H-ex) | DICT-2, DICT-3, O5 | VAR-N1, VAR-T1(c) |
| DICT-RANGO caso magnetico | tolto da RANGO; riga canonica SYS-N3 (div_x(ρ²B) = 0) | DICT-5, O15 | SYS-N3 (S8-SYS) |
| DICT-MAG-NU (§2.6) | **corollario di SYS-N3(c)**, non claim autonomo (O15). Contenuto proprio: u con zeri fuori da supp χ. AUDIT_S8-DICT_rev2 propone DIMOSTRATO dopo MAG-1, MAG-2 (recepiti); qui lo stato non viene alzato | DICT-5, MAG-1…MAG-4, O15 | SYS-N3(a)(b)(c) |
| N1(vi) originale | **FALSO** (§2.6bis; controesempio u = t + x nella classe u_t = a(t,x)u_x) | — | — |
| DICT-MF (MF1, MF2, MF3 (a)–(d), MF-C) | DIMOSTRATO | — | Hahn–Banach, Weyl, Sion, Farkas |
| DICT-A (i), (ii) | DIMOSTRATO | DICT-13 | N1(v), Lemma ND |
| DICT-A (iii) | DIMOSTRATO dopo DICT-1 (senza ipotesi U_0; atomi differenziali) | DICT-1 | Lemma ND, MF3(a) |
| DICT-B2, DICT-R3 | DIMOSTRATO (folklore, prior art OLS) | — | — |
| DICT-B3 | CON-FONTE da verificare (Pinkus) | — | — |
| DICT-R4, DICT-PAINLEVE | STRUMENTO | — | — |
| DICT-GR | DIMOSTRATO; ipotesi (H-ID) (prima "(ID)") | DICT-7, O13 | P4-T5, CONV-T1 |
| DICT-R6 (Lemma R6-T, §3.6) | (a)–(e) DIMOSTRATO (AUDIT_S8-ENC; rev2). (f): DIMOSTRATO proposto da AUDIT_S8-DICT_R6f dopo R6f-1, R6f-2 (recepiti) | DICT-17, DICT-18, MAG-5, O19, R6f-1, R6f-2 | ENC-1, ENC-C1, ENC-T2(a)(b); (f) da DICT-N1(ii) e Teorema A |
| DICT-ILIM (a)–(d) | DIMOSTRATO | DICT-8 | (H0), (H-ID), (H2); CONV-T1 per il ramo esatto |
| DICT-ILIM-H0 (s = 0) | DIMOSTRATO | — | condizione del cono |
| DICT-ILIM-Hs (s ≥ 1) | CANDIDATO | — | Gagliardo–Nirenberg (da verificare) |
| DICT-NS (NS-L1, NS-T1, KINK) | DIMOSTRATO | DICT-9, DICT-10 | ALG-T1 (solo per forme evolutive) |
| DICT-2KINK | V-ex | — | — |
| DICT-AX | CON-FONTE **da leggere** (teorema differenziale non letto; prima "verificata") | DICT-11, CIT-AUDIT-8 §5 (2) | Ax, On Schanuel's conjectures, Ann. of Math. (2) 93(2) (1971) 252–268, DOI 10.2307/1970774 |
**Confronto con la predizione del PLAN (aggiornato).** Confermato:
- U1, U2 senza KMS 18.16 (Boman), U3(c)+N2, U3(d) uniforme in t per t^{−β} con rappresentazione diffusiva esatta;
- ritardo come trasporto aumentato, N3 con distanza esattamente 1, CS-1 con costante esplicita, U4;
- N1(v) per polinomi differenziali;
- teorema di rango con "Schrödinger con V reale identificabile e falsificabile", dopo la definizione corretta di identificabile (DICT-2);
- Teorema A(iii) con dati esatti, ora senza ipotesi aggiuntive (DICT-1);
- NS-EXPALG senza Ax; I-LIM completo.

Declassamenti previsti e avvenuti: velocità per nuclei c.m. generali (candidato), B3 (fonte), Hölder per s ≥ 1 (candidato), R4 (euristica).

Non previsti:
- N1(iii) richiede N ≥ 2 e L ∈ Ann(u);
- N1(v) vale anche in senso di prevalenza; N3 vale anche su (0, T);
- il caso magnetico non sta in RANGO;
- (b′) con V reale è un "⟺" solo per u senza zeri;
- U3(d)(ii) richiede il nodo λ = 0.



---

## 3.6 R6 recepita: cambio di quadro tramite l'encoder di Volterra (aggiunta del 27/10/2026, sostituisce il punto R6 di §3.5)
Questa sezione recepisce la risposta di S8-ENC (inbox/S8-DICT.md, 27/10) e work/S8-ENC/PROOF_PACKAGE.md §2–§3: ENC-1, ENC-U1, ENC-C1, ENC-T2. Sostituisce la versione di §3.5, che era condizionata a una conferma su ENC-T2. Quella conferma è arrivata: l'intrecciamento è esatto. La regola però vale **solo sul sottoanello pari**. Le altre sezioni del pacchetto non cambiano.

**Ipotesi (R6-H), tutte dichiarate.**
- (H-dom) Punto base x_0 ∈ ℝ e raggio a > 0, J := [x_0 − a, x_0 + a], I intervallo aperto limitato, Ω := I × J° (rettangolo simmetrico attorno a x_0 nella variabile x).
- (H-q) q ∈ C^∞(J; ℂ) è **dato**: è parte del dato oppure è ricavato prima con VAR-T1(b) quando la forma di Schrödinger è nota. Senza (H-q) la regola è circolare (DEVIL-6 O6) e **non si applica**. Le stime di norma richiedono solo q ∈ C¹(J). Poniamo Q := ‖q‖_∞.
- (H-W) W := T^{−1} è l'operatore di ENC-1(3) relativo a (x_0, a, q), normalizzato in modo da conservare i dati di Cauchy in x_0. Nella classe di Volterra simmetrica è l'unico con questa proprietà (ENC-U1). W agisce nella sola variabile x e commuta con ∂_t.
- (H-Y) Y = C(Ω̄) oppure Y = L²(Ω), e u è tale che i D_iu considerati stanno in Y. In C^∞(Ω) valgono le identità senza norme. Il caso Y = H^{2k} **non è coperto** (stima di S8-ENC solo schizzata, open_questions Q2 di S8-ENC).
- (H-dato) Modello di dato DM3 (u su Ω). Il modello DM2 (getti in un punto) è escluso: per (f) nessun getto finito certifica un fit (DICT-N1(ii), Teorema A; post-Gate 8, MAG-5).

**Livelli.** Indico con L_q l'operatore spaziale di ENC-1, con L_0 il caso q = 0, e con φ l'omomorfismo di ENC-T2, P(τ, σ) ↦ P(τ, L_0) scritto come polinomio in (τ, ξ), la cui immagine è ℂ[τ, ξ²]. Pongo:
- livello q, omogeneo: 𝓓^q_n := span{∂_t^jL_q^k : j + 2k ≤ n}; livello q, affine: 𝓐^q_n := ∂_t + span{∂_t^jL_q^k : j + 2k ≤ n, (j, k) ≠ (1, 0)};
- livello libero pari: 𝓓^{pari}_n := span{∂_t^jL_0^k : j + 2k ≤ n}, e 𝓐^{pari}_n definito allo stesso modo.
φ manda 𝓓^q_n su 𝓓^{pari}_n in modo lineare e biiettivo, e manda 𝓐^q_n su 𝓐^{pari}_n (fissa ∂_t). L'operatore corrispondente a L = P(∂_t, L_q) è L̂ := φ(P)(∂_t, ∂_x) = P(∂_t, L_0).

**Lemma R6-T (prova scritta; usa ENC-1, ENC-C1 ed ENC-T2 come importati).** Sotto (R6-H):
- (a) *Intrecciamento esatto.* Per ogni L ∈ 𝓓^q_n e u ∈ C^∞(Ω) vale W(Lu) = L̂(Wu). Quindi Lu = 0 ⟺ L̂(Wu) = 0, e Ann_q(u) ∩ 𝓓^q_n = φ^{−1}(Ann(Wu) ∩ 𝓓^{pari}_n). In particolare: fit al livello q n ⟺ fit di Wu al livello libero **pari** n.
- (b) *Norme.* Sia C_W := 1 + a²Q·e^{a√Q}. Su Y vale ‖W‖_{Y→Y} ≤ C_W e ‖W^{−1}‖_{Y→Y} ≤ C_W.
- (c) *Distanze.* [fix DICT-17] Sia u ∈ C^∞(Ω) tale che D_iu ∈ Y per tutti gli atomi D_i del livello q usato (per gli atomi del livello pari, D̂_i(Wu) = W(D_iu) ∈ Y segue da (a) e (b)); senza questa condizione ‖Lu‖_Y non è definita. Poniamo r^q_n(u) := inf_{L∈𝓐^q_n}‖Lu‖_Y e r^{pari}_n(v) := inf_{L̂∈𝓐^{pari}_n}‖L̂v‖_Y. Allora r^{pari}_n(Wu)/‖W‖ ≤ r^q_n(u) ≤ ‖W^{−1}‖·r^{pari}_n(Wu). Per Y = L², nel livello omogeneo i valori λ_min delle matrici di Gram soddisfano λ_min(G^{pari}_n(Wu))/‖W‖² ≤ λ_min(G^q_n(u)) ≤ ‖W^{−1}‖²λ_min(G^{pari}_n(Wu)).
- (d) *Trasporto dei certificati (MF1).* Sia ψ ∈ Y* un certificato di misfit affine per Wu al livello pari: ψ(L̂_iWu) = 0 per gli atomi L̂_i ≠ ∂_t e ψ(∂_tWu) ≠ 0. Allora ψ∘W ∈ Y* è un certificato di misfit affine per u al livello q, con ‖ψ∘W‖ ≤ ‖W‖‖ψ‖ e lo stesso valore (ψ∘W)(∂_tu) = ψ(∂_tWu). Vale anche il viceversa, con W^{−1}.
- (e) *Perdita degli atomi dispari.* Un elemento del livello libero che non sta in ℂ[τ, ξ²] (dispari in ξ, o misto) **non ha controparte** nel livello q. Se Ann(Wu) = (Q), il generatore trasportato è P_* con φ(P_*) = lcm(Q, Q̃) se lcm è pari, oppure ξ·lcm(Q, Q̃) se è dispari (ENC-T2(b)). Una legge libera dispari, per esempio ξ − ik per Wu = e^{ikx − ik²t}, si riporta solo attraverso il suo multiplo pari minimo.
- (f) *Getti.* [fix R6f-1, R6f-2 di AUDIT_S8-DICT_R6f]
  - (f1) **Nei punti (t, x_0)** la mappa dei getti j^N u(t, x_0) ↦ j^N(Wu)(t, x_0) è triangolare unipotente. In x_1 ≠ x_0 non lo è, perché W non è locale.
  - (f2) *Al livello n.* Per ogni n e ogni dato finito (getti finiti in un numero finito di punti) esiste v con gli stessi dati e senza legge al livello n.
  - (f2′) *A nessun livello.* Esiste v con gli stessi dati e senza legge a nessun livello. Quindi nessun getto finito certifica Ann_q(u) ≠ 0.
  - Riferimenti: DICT-N1(ii) e Teorema A, più un passo di Baire per (f2′). R6 è una regola DM3 e non dà certificati di fit da dati finiti. [post-Gate 8, MAG-5 di AUDIT_S8-DICT_rev2 e O19 di ATTACK-8: la citazione precedente era ENC-T2(c). Dopo ENC-6(a) quella conseguenza sta in ENC-T2(c′), che è DA AUDITARE in S8-ENC, e qui non è più usata. (a)–(e) non dipendono da (f).]

*Prova.*
- (a) È ENC-C1 applicato a ogni P con φ(P) nel livello, più ENC-T2(a). La biiezione dei livelli viene dall'iniettività di φ: φ manda il monomio τ^jσ^k in τ^jξ^{2k} a meno di segni e costanti fissati dalla convenzione su L_0, e il peso j + 2k si conserva.
- (b) H è il nucleo di W. Per ENC-1(3) e (5) vale ‖H‖_∞ ≤ (aQ/2)e^{a√Q}; lo stesso vale per il nucleo K di T = W^{−1}, con la stessa stima. Su C(J): |∫_{−x}^{x}H(x, s)f(s)ds| ≤ 2a‖H‖_∞‖f‖_∞. Su L²(J): con Cauchy–Schwarz il valore puntuale è ≤ ‖H‖_∞√(2a)‖f‖_{L²(J)}, e integrando in x su J (lunghezza 2a) la norma L² è ≤ 2a‖H‖_∞‖f‖_{L²(J)}. Quindi ‖W‖ ≤ 1 + 2a‖H‖_∞ ≤ C_W. W agisce a t fissato. Su C(Ω̄) si prende il sup in t; su L²(Ω) si integra in t (Fubini). Lo stesso argomento vale per W^{−1}.
- (c) Per L ∈ 𝓐^q_n, da (a): ‖L̂Wu‖ = ‖WLu‖ ≤ ‖W‖‖Lu‖ e ‖Lu‖ = ‖W^{−1}L̂Wu‖ ≤ ‖W^{−1}‖‖L̂Wu‖. Si prende l'inf su L, e L ↦ L̂ è biiettiva fra i due livelli affini. Per il Gram: ‖Σc_iL_iu‖ e ‖Σc_iL̂_iWu‖ = ‖W Σc_iL_iu‖ si confrontano con le stesse costanti; si prende il min su |c| = 1.
- (d) Da (a): (ψ∘W)(L_iu) = ψ(WL_iu) = ψ(L̂_iWu).
- (e) È ENC-T2(b).
- (f1) [fix R6f-1] Si ha W = I + V, con Vf(x) = ∫_{2x_0−x}^{x}H(x, s)f(s)ds, l'operatore di Volterra simmetrico di ENC-1(3) (H-W).
  - Se j^{m−1}f(x_0) = 0, allora f = O(|x − x_0|^m) vicino a x_0. L'intervallo d'integrazione ha lunghezza 2|x − x_0| e H è limitato, quindi Vf(x) = O(|x − x_0|^{m+1}) e j^m(Vf)(x_0) = 0.
  - Per linearità, j^m(Wf)(x_0) = j^m f(x_0) + (una funzione lineare di j^{m−1}f(x_0)): la mappa è triangolare unipotente.
  - W agisce solo in x e commuta con ∂_t, quindi lo stesso vale per i getti in (t, x_0).
  - La sola conservazione dei dati di Cauchy riguarda solo gli ordini 0 e 1 e non basta. In x_1 ≠ x_0, (Vf)(x_1) dipende da f lontano da x_1.
  - Verifica: `work/CHECK-F8/sympy/dict3_r6f.py` T1–T3.
- (f2) Gli atomi ∂_t^jL_q^k sono operatori differenziali lineari a coefficienti lisci e sono linearmente indipendenti (simboli principali ∂_t^j∂_x^{2k} distinti). I funzionali "getto in un punto" sono lineari e continui su C^∞(Ω). Il Teorema A(iii), che vale per atomi differenziali senza ipotesi aggiuntive (fix DICT-1), dà allora per ogni dato finito una v con gli stessi dati e senza legge al livello n. Questo è N1(ii)(b). Il punto non usa W e vale in ogni punto, non solo in x_0.
- (f2′) [fix R6f-2, passo di Baire]
  - Sia Z l'intersezione dei nuclei dei funzionali di dato. È un sottospazio chiuso di C^∞(Ω), quindi u + Z è uno spazio affine di Fréchet e soddisfa il teorema di Baire.
  - Sia F_n l'insieme di fit omogeneo del livello n (Teorema A). È chiuso per A(ii), e contiene le funzioni con una legge affine al livello n.
  - F_n ∩ (u + Z) ha interno vuoto in u + Z. Infatti A(iii), applicato in ogni suo punto w, dà v ∈ U_n vicina quanto si vuole a w e con gli stessi dati, quindi v ∈ u + Z.
  - Quindi ∪_n F_n ∩ (u + Z) è magro in u + Z, ed esiste v ∈ u + Z senza legge a nessun livello. ∎

**Regola R6 (definizione di procedura).**
- *Quando si applica.* Valgono (R6-H), e il residuo nel livello libero pari è piccolo su Wu mentre nel quadro originale c'è misfit con atomi a coefficienti costanti.
- *Cosa fa.* Si calcola Wu (nucleo H da (G) con −q, ENC-1(3)) e si applicano R1–R5 al livello libero **pari** su Wu. Il risultato si riporta nel quadro q con φ^{−1}: i certificati con ψ ↦ ψ∘W, i livelli e le distanze con le costanti di (b)–(c).
- *Etichetta d'uscita.* "Legge nel sottoanello ℂ[∂_t, L_q], q dato, base x_0".
- *Cosa non fa.* Non identifica q. Non allarga la classe identificabile (ricodifica in modo esatto). Non trasporta gli atomi dispari. Non trasporta la forma debole MF3 con funzioni test a supporto compatto: questo caso è dichiarato **non coperto**. [fix DICT-18: la ragione data prima, "W* non conserva il supporto compatto", è inesatta. Il trasposto Wᵗ porta C_c^∞(J°) in funzioni con supporto nell'involucro simmetrico [x_0 − b, x_0 + b] ⊂ J°, e per q costante Wᵗψ è liscia anche in x_0 (dict_check J2). La ragione corretta è che la liscezza di Wᵗψ in x_0 per q generale non è verificata. L'esclusione resta come scelta prudente di ambito.]
- *Punto base.* Un altro (x_0, a) dà un altro W. Le conclusioni di fit e misfit non cambiano, perché Ann_q(u) è intrinseco; cambiano solo le costanti C_W.

**Stato (aggiornato dopo gli audit).**
- **AUDIT_S8-DICT §2:** R6-T è corretto con i fix MINOR DICT-17 e DICT-18. Lo stato proposto è DIMOSTRATO condizionato a ENC-1, ENC-C1 ed ENC-T2.
- **AUDIT_S8-ENC (`work/CHECK-F8/AUDIT_S8-ENC.md` §0 e §2.1):**
  - ENC-1 (1)–(5): DIMOSTRATO, con il fix MINOR ENC-8.
  - ENC-C1: DIMOSTRATO.
  - ENC-T2 (a)(b): DIMOSTRATO come lemma a q noto, solo nel sottoanello pari. ENC-T2(c): DIMOSTRATO dopo ENC-6.
  - Conclusione dell'audit: "il cammino critico ENC-1 → ENC-C1 → ENC-T2 → R6 di S8-DICT regge".
- **AUDIT_S8-DICT_R6f (controllo leggero di (f)):** PASS-con-fix. R6f-1: la triangolarità vale solo in (t, x_0), con l'argomento O(|x − x_0|^{m+1}). R6f-2: (f) è enunciato al livello n, (f2), e con il passo di Baire, (f2′). Entrambi recepiti; stato proposto per (f): DIMOSTRATO. Script `work/CHECK-F8/sympy/dict3_r6f.py` 8/8.
- **AUDIT_S8-DICT_rev2 (Gate 8):** il passaggio a DIMOSTRATO è legittimo. Il solo rilievo è MAG-5 (MINOR, citazione in (f)), recepito sopra: (f) cita DICT-N1(ii) e il Teorema A, non ENC-T2(c) o (c′).
  - La convenzione φ(P)(τ, ξ) = P(τ, −ξ²), con L_0 = −∂², è coerente con quella usata qui.
- **Condizione soddisfatta:** il Lemma R6-T si mantiene come proposto, **DIMOSTRATO** (la registrazione nel LEDGER spetta al coordinatore).
- **Riserva:** S8-ENC sta recependo i suoi fix. Se un fix tocca ENC-T2, il lemma si riallinea alla segnalazione in inbox/S8-DICT.md. ENC-6(b) dice che ENC-T2 non va contato fra gli strumenti di B1 senza q: è coerente con (H-q).
- La regola R6 resta una definizione di procedura.
