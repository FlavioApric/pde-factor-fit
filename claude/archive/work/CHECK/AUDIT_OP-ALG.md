# AUDIT OP-ALG — decidibilità nel modello olonomo analitico, minimalità del maggiorante, coefficienti variabili, INT-18
Revisore: S-CHECK-12 (12ª tornata), 26/10/2026. Revisore indipendente: non ho scritto nessuna delle prove.
**Fonte esaminata:** `work/OP-ALG/CHECK_REQUEST.md` (autosufficiente per enunciati, ipotesi, fatti importati e punti delicati). Le prove stanno in `work/OP-ALG/PROOF_PACKAGE.md` §§1–5, come dichiara la CHECK_REQUEST; ho letto quelle sezioni e §7–§8 come riferimento puntuale. Per controllare come P4-T4(i) usa gli oracoli ho letto anche `work/P4/PROOF_PACKAGE.md` righe 132–153 (modello M2⁺, P4-T4, P4-T5).
**Fatti usati come dati** (claims/LEDGER.md, DIMOSTRATO): C3-T1 (u ∈ D′(Ω), Ω connesso), C3-T3(ii), C3-T6, C3-L3, C3-C2, P4-T2, P4-T4, P4-T5 (Passi 2–3), P4-L4 (modulo (AC)), P4-L7. Sono usati anche i fatti di Ore, rango e torsione (Goodearl–Warfield cap. 6), che hanno lo stato CON-FONTE generico.
**Skill caricate** (ho letto i SKILL.md e non ho eseguito nessuno script _vendor):
- skills-local/session-protocol, caricata per prima;
- skills-local/claim-lifecycle;
- proof-checker: enunciati canonici, micro-claim, checklist, red team, severità a due assi, acceptance gate. Il revisore sono io.
- kill-argument: i revisori sono subagenti Claude freschi;
- sympy.

**SymPy:** `work/CHECK/sympy/audit_opalg.py` → `audit_opalg.out`, eseguito con `.venv -I` e `timeout 600`: **64/64 OK**. Non ho toccato processi python altrui.

**Kill-argument:** quattro subagenti Claude freschi, uno per l'attacco e uno per l'arbitrato su ciascun bersaglio. Gli input sono `KA_OPALG_T1_input.md` e `KA_OPALG_T3_input.md`, estratti verbatim; i memo sono `KA_OPALG_T{1,3}_attack.md`, gli arbitrati `KA_OPALG_T{1,3}_adjudication.md`. Ho trovato da solo il rilievo OA-1 prima di leggere il memo d'attacco su T1, che lo ha poi trovato in modo indipendente con un altro esempio.

## 0. Verdetti
| claim | verdetto | stato proposto |
|---|---|---|
| OP-ALG-L1, L2, L3, L4, P2 | PASS | DIMOSTRATO (L2, L4 modulo (AC)) |
| OP-ALG-P1 | PASS, ma solo per L_* ∈ A_2(K); va esteso → OA-1 | DIMOSTRATO |
| **OP-ALG-T1** | **PASS-con-fix(OA-1 MAJOR, OA-2 MINOR)**. (i)–(iii) PASS senza riserve. (iv) e la parte "generatori" di (v) non sono giustificate come scritte; la riparazione è mia (L1′, P1′, §2.3) | **DIMOSTRATO** modulo (AC), con il fix OA-1 recepito. Uscite di (iv) e (v) su 𝕂 |
| **OP-ALG-T3** | **PASS-con-fix(OB-1 MAJOR di portata, OB-2, OB-3 MINOR)**. Nessun enunciato (a)–(f) è falso o non dimostrato. La Lettura e le sintesi dicono più di (f) | **DIMOSTRATO**, (f) con "per qualche (Ω, p₀)" |
| OP-ALG-L5, T4, P5 | PASS | DIMOSTRATO |
| OP-ALG-C1 + Lemma NT | PASS-con-fix(OC-1 MINOR, solo la sintesi §0) | DIMOSTRATO (controesempio) |
| OP-ALG-Q1 | — | APERTO |
| INT-18 (§5) | PASS-con-fix(OI-1 MINOR) | verifica corretta; testo da approvare con le precisazioni OI-1 |
| C3-Q1 / P4-Q1 / P4-Q-min / C3-Q2 | vedi §6 | CHIUSO nei termini precisati |

**Kill-argument:**
- **T1: WARN.** L'arbitro conclude che il titolo sopravvive e che il gap OA-1 è reale, locale e riparabile a basso costo.
- **T3: WARN.** L'arbitro trova che nessun enunciato è falso; resta una sovra-dichiarazione nella Lettura (OB-1).

**Acceptance gate:** dopo i fix, nessun rilievo FATAL o CRITICAL resta aperto, e il red team è stato eseguito su tutti i lemmi chiave.

## 1. OP-ALG-T1 e la sua catena: micro-claim
| MC | passo | esito |
|---|---|---|
| L1(a) | conteggio | OK. La filtrazione di Bernstein è moltiplicativa (F_kA_2·F_dA_2 ⊆ F_{k+d}A_2) e F_kN = F_kA_2·1̄ è una buona filtrazione. Per l'olonomia dim F_jN ≤ Cj², mentre dim S_k = binom(k+3,3). Il caso N = 0 (I = A_2) è banale. |
| L1(b) | ricerca | OK. Il sistema LM = ΣC_lH_l è lineare omogeneo su K in forma normale. Termina perché esiste una rappresentazione di grado finito ed è corretta perché LM ∈ I. È una ricerca illimitata ma terminante: basta per la decidibilità, senza stima di complessità (dichiarato). |
| L1(c) | — | OK: L(Mu) = (LM)u = 0, perché I ⊆ Ann_{A_2}(u) e l'azione è un'azione di modulo. |
| L2(i) | ι ≠ 0, Z finito | OK. I fattoriali decrescenti con j distinti hanno gradi distinti. δ ≥ −r. Le radici intere ≥ 0 del gcd dei coefficienti in x si calcolano con (AC). Servono β_ij ∈ K[x], quindi t₀ ∈ K, che vale. |
| L2(ii) | punto singolare | OK. Il coefficiente di (t−t₀)^{n₀+δ} riceve contributi solo da n = n₀ e i − j = δ: i termini con n > n₀ hanno esponente ≥ n+δ, quelli con n < n₀ hanno c_n = 0. Nessuna ipotesi di regolarità di t₀. Da c_{n₀} ≢ 0 analitica segue che ι(n₀;·) si annulla su un insieme infinito, quindi ≡ 0. **SymPy:** ricorrenza verificata simbolicamente con c_n(x) funzioni generiche su 6 operatori casuali; t∂_t − x dà Z = ∅; x t²∂_t − 2xt dà δ = 1, K₀ = 2; esempi del package. |
| L3 | restrizione | OK. Se Λ ha ordine 0, P4-L4 dà K₀ = −1 e c_n ≡ 0, il che è coerente. |
| P1 | catena | OK per L_* ∈ A_2(K): getti di v per Leibniz in 𝕂; Λ_n ∈ K[x]⟨∂_x⟩; P4-L4 vale anche nei punti singolari; v ≡ 0 vicino a p₀ ⟹ v ≡ 0 su Ω (analitica, Ω connesso). **Limite:** solo operatori a coefficienti in K → OA-1. |
| L4(i) esponente | t^{D+ν} | OK. La coniugazione e^{−⟨z,y⟩}Le^{⟨z,y⟩} = L_τ è corretta perché i coefficienti non contengono ∂_x. C3-L3(b) separa gli esponenti distinti z_k. Il grado i+a−l ≤ D+ν ha l'uguaglianza solo per (i,a,l) = (D,ν,0), con coefficiente M_D(x;τ)r_ν(x). T_t è finito e contenuto in K. |
| L4(i) grado | δ_τ | OK. L_τ ≠ 0 (automorfismo di coniugazione). L'uguaglianza a+i−l = ν+δ_τ forza a = ν e i−l = δ_τ, dando ι_τ(ν;·) ≡ 0 e ν ≤ N_t(τ). Per gli esponenti presenti N_t(τ) ≥ 0. **SymPy:** eliminanti "sporche" L = A·L_min, con A casuale a coefficienti in x, per w = (t²+x)e^{2t+x} + 3te^{−t}: T_t ⊇ {2, −1}, N_t(2) ≥ 2, N_t(−1) ≥ 1, a*(∂_t)w = 0 (4/4). |
| L4(ii), P2 | — | OK. (⇐): a*(τ), b*(ξ) ∈ Ann(w), quindi V(Ann w) è finito e w è EP (C3-L3(e)). Il prodotto vuoto dà w = 0. |
| P4-C4(b) | — | OK (SymPy): L_w annulla w = (2t−1)e^{t²}, M_D ≡ −4, T_t = ∅, a* = 1, w ≠ 0, dunque w ∉ EP. Calore: T_t = {0}, N_t(0) = −1, a* = 1. Per e^{tx}: T_t = ∅. |
| T1(i)–(ii) | — | OK. Tutti gli operatori testati, Q(∂), a*(∂_t)Q(∂) e b*(∂_x)Q(∂), stanno in A_2(K) (T_t, T_x ⊂ K). |
| T1(iii) | — | OK. Applica C3-T1(a),(b) e C3-T6 con al più Σe_i test, tutti su operatori in K[τ,ξ]. In C3-T6 il caso k = 0 è sempre "EP" (P(∂)u = 0), quindi il massimo esiste. I fattori sono irriducibili su ℂ per D1(v). |
| T1(iv) | P4-T4(i) | **LACUNA → OA-1.** |
| T1(v) | B, generatori | B := dim E(w₀) è corretto, perché G_u ∈ K[τ,ξ] e w₀ ha eliminanti su K. C3-T3(ii) non dipende dal campo. Il passo "Ann(w₀) ∩ R_{≤B} con (iv)" eredita OA-1. Manca l'ipotesi P(∂)u = 0 → OA-2. |

### 2.1 OA-1 (MAJOR · UNJUSTIFIED + LOCAL · HIDDEN_ASSUMPTION / REFERENCE_MISMATCH): campo di definizione di Ann(u)
In M3-hol i getti stanno in 𝕂 ⊋ K, ma OP-ALG-P1 decide "L_*u = 0" solo per L_* ∈ A_2(K). P4-T4(i), citata in T1(iv), presuppone invece due cose: getti in K e un oracolo di zero su K[τ,ξ]. In quelle condizioni i sottospazi A_k hanno base in K. Con getti in 𝕂, A_k e Ann(u) ∩ 𝓛 hanno in generale **solo** una base in 𝕂, e l'algoritmo deve interrogare lo zero su operatori a coefficienti in 𝕂. T1(i) non lo fornisce.

**Controesempio.** L'ho trovato prima del KA; l'attacco del KA ne ha trovato uno equivalente.
- u = e^x(t + πx), p₀ = 0, 𝕂 = ℚ̄(π) (computabile, uguaglianza decidibile).
- I = (∂_t², ∂_t(∂_x−1), (∂_x−1)²) ⊂ A_2(ℚ), olonomo.
- (π∂_t − ∂_x + 1)u = 0, e Ann(u) = (πτ − ξ + 1, (ξ−1)²), che **non è definito su ℚ̄**.
- Ann(u) ∩ ℚ̄[τ,ξ] genera solo (τ, ξ−1)², di colunghezza 3 invece di 2.
- SymPy, 5 controlli A1:
  - I annulla u;
  - πτ − (ξ−1) ∈ Ann(u);
  - dim Ann(u) ∩ R_{≤2} = 4;
  - il sottospazio dipende da π.

**Portata.**
- (i)–(iii), cioè il titolo C3-Q1, G_u e V(Ann u), non sono toccati: lì tutti gli operatori stanno in A_2(K).
- B in (v) non è toccato.
- È toccato solo il calcolo di Ann(u) ∩ 𝓛 e dei generatori di Ann(u).

**Fix (prova del revisore, da recepire in §2):**
- **[OP-ALG-L1′] Eliminante simultanea.**
  - *Ipotesi:* come in L1, con M_1, …, M_r ∈ A_2(K).
  - *Tesi:* esiste L ∈ S∖{0}, calcolabile, con LM_k ∈ I per ogni k.
  - *Prova:* con d := max deg M_k, la mappa S_k → (F_{k+d}N)^r, L ↦ (L·M_k·1̄)_k, ha bersaglio di dimensione ≤ rC(k+d+1)² < binom(k+3,3) per k grande. La ricerca è quella di L1(b), con incognite C_{kl}: LM_k = Σ_lC_{kl}H_l.
- **[OP-ALG-P1′] Test di zero per operatori a coefficienti in 𝕂.** Per L_* = Σ_kc_kM_k, con c_k ∈ 𝕂 e M_k ∈ A_2(K), "L_*u = 0" è decidibile. Si procede come in P1:
  - Passo 1: L1′ su (M_k)_k dà L ∈ S_t(K) con Lv = 0.
  - Passo 2: L1′ su (∂_t^nM_k)_k dà L′_n ∈ S_x(K).
  - L2, L3, P4-L4 e (AC) restano su K.
  - I getti di v sono Σ_kc_k(getti di M_ku), in 𝕂. Serve solo l'uguaglianza in 𝕂, che D1(iv) già assume.
  - Non servono radici in 𝕂.
- **T1(iv)** si riscrive così: P4-T4(i) con aritmetica in 𝕂 al posto di K e con l'oracolo P1′. L'uscita è una base di Ann(u) ∩ 𝓛 su 𝕂, in generale non razionale su K (esempio sopra).
- **T1(v), generatori:** Ann(w₀) ∩ R_{≤B} si calcola su 𝕂 come sopra, e i generatori di Ann(u) = G_u·Ann(w₀) stanno in 𝕂[τ,ξ].
- **Nota da aggiungere a §2:** "Ann(u) non è in generale definito su K: u = e^x(t+πx). Lo sono G_u (C3-T6, perché P ∈ K[τ,ξ]) e gli esponenti della parte EP (T_t, T_x ⊂ K, OP-ALG-L4). Non lo sono i coefficienti dei polinomi della parte EP."

### 2.2 OA-2 (MINOR · HIDDEN_ASSUMPTION · LOCAL)
T1(v) usa G_u, ma non richiede P(∂)u = 0. Senza P, Ann(u) può essere 0: per u = e^{tx}, per esempio.

**Fix:** "(v) Se P(∂)u = 0 (verificato con (i)), …".

### 2.3 Rilievi minori e informativi su T1
- **INFO-1.** Il "Commento" su Lindemann–Weierstrass è corretto per esponenti algebrici ℚ-linearmente indipendenti: ℚ̄(e^{α_1}, …) ≅ ℚ̄(X_1, …).
- **INFO-2.** Le ricerche di L1 non hanno un limite di grado, quindi non c'è complessità. È dichiarato (Rischi R1–R3).

## 3. OP-ALG-T3
| MC | esito |
|---|---|
| D2 | OK come definizione. ≤ è computabilità uniforme a oracoli **senza limiti di risorse**: va detto (OB-2). |
| (a) χ ≤ 𝔇 | OK. Con N = max(D, deg P), un testimone di grado ≤ D rende stretta l'inclusione (P) ∩ R_{≤N} ⊆ Ann ∩ R_{≤N}. Si calcola con P4-T4(i), con getti in K: qui non c'è il problema OA-1. |
| (a) 𝔇 ≤ χ | OK. La semi-decisione P4-T4(ii) termina esattamente quando Ann ≠ (P). Un salto di dimensione al livello n dà un testimone di grado ≤ n. |
| (b) | OK ma **tautologico** ("sufficiente" è definito come χ ≤ 𝒜). Il contenuto reale sta in (a), (d) e (f) → OB-2. |
| (c) 𝔊 ≤ 𝔅 | OK: P4-T4(iii). |
| (c) 𝔅 ≤ 𝔊 | OK. Gli oracoli di w₀ = G(∂)u si ricavano da quelli di u; la ricerca di a(τ) e b(ξ) termina (C3-L3(c) + Nullstellensatz: V finito dà un elemento univariato in Ann); R·w₀ è quoziente di R/(a, b); B = deg a·deg b; w₀ = 0 dà a = 1. |
| (d), (e) | OK. In (e), χ = 0 con r = 1, e_1 = 1 dà cu ∈ EP, quindi w₀ = u. (e) vale per ogni (Ω, p₀). |
| (f) istanza | OK. z₀ esiste: V(P_1) ∩ V(P_j) è finito, i punti singolari sono finiti, V(P_1) ∩ K² è infinito. P(∂)e = 0. κ ≠ 0, anche se e_1 = 1 (κ = P̃(z₀) ≠ 0). χ(u) = 0. Ann(u) ⊆ (P̃) per P4-T2(v)(a). |
| (f) avversario | OK. F è scelto dopo B, k₀ e 𝒬. I getti coincidono. Le risposte su 𝒬 ∩ (P̃) coincidono perché Q(∂) annulla ker P̃. Su 𝒬′ restano finiti sottospazi affini propri, più gli iperpiani c_z = 0 di S_F, che non ricoprono lo spazio su K infinito. L'adattività si tratta per induzione. χ(u′) = 0 per C3-C2. Il conteggio dà dim R·u′ ≥ \|V(Ann u′)\| ≥ \|supp S_F\| ≥ \|F\| − N₀ > B, usando il CRT e il fatto che F evita gli altri esponenti. |
| (f) quantificatori | La Tesi è esistenziale in (Ω, p₀), con Ω = (−ε,ε)² da P4-L7 e p₀ = 0, e la prova dà esattamente questo. **La Lettura, §0 e la riga LEDGER proposta la rendono universale** → OB-1. |

**SymPy (istanza allineata a (f), p₀ = 0).** Prendo P = (τ−ξ)(τ+ξ), P_1 = τ−ξ, ũ = e^{(x−t)²} (Ann = (τ+ξ)), e = e^{t+x}, k₀ = 2 e un B simulato = 5. Costruisco v₁ = e^{s} + e^{−s} − 1 con s = x − t, e_Q a getto nullo, e F con 12 punti di V(τ+ξ). Risultati:
- u′ ha lo stesso 2-getto di u;
- u′ dà le stesse risposte di zero su 6 operatori;
- P(∂)u′ = 0;
- u′ ha più di B modi nuovi.

Controlli T3f: 10/10. Qui ũ è intera, quindi l'avversario funziona anche su Ω = ℝ² per questo P. Non è una prova del caso universale.

### OB-1 (MAJOR · OVERSTATED + GLOBAL, solo per la portata · SCOPE_OVERCLAIM)
Ci sono quattro formulazioni universali, senza quantificatore su (Ω, p₀):
- PROOF_PACKAGE §0.2: "per ogni P con Σe_i ≥ 2 … B è strettamente più forte di χ";
- la Lettura: "B è strettamente più forte se P ha almeno due fattori…";
- la riga LEDGER proposta: "χ < 𝔅 ⟺ Σe_i ≥ 2";
- CHECK_REQUEST: "B strettamente più forte di χ se Σe_i ≥ 2".

(f) però dà solo "esistono Ω ∋ 0 e p₀ = 0". Non c'è un argomento di trasporto ad altri (Ω, p₀): servirebbe un analogo globale di P4-L7.

**Fix:** sostituire con "per ogni P con Σe_i ≥ 2 esistono (Ω, p₀) (un quadrato (−ε,ε)² attorno a p₀ = 0) su cui 𝔅 ≰ χ, quindi χ < 𝔅". Nella riga LEDGER: "χ < 𝔅 su qualche (Ω,p₀) se Σe_i ≥ 2; 𝔅 ≡ χ per ogni (Ω,p₀) se P è irriducibile ridotto".

Il caso universale va registrato come **nuovo APERTO OP-ALG-Q2**: per Ω, p₀ arbitrari (p. es. Ω = ℝ²) e Σe_i ≥ 2, vale 𝔅 ≰ χ? Basterebbe un'u globale con Ann(u) = (P̃) e getti in K, cioè P4-L7 globale.

### OB-2 (MINOR · UNCLEAR)
- (b) va declassato a osservazione: "per D2, χ è banalmente il minimo dei dati sufficienti".
- In D2 e nella Lettura va scritto che ≤ è computabilità uniforme a oracoli senza limiti di risorse. 𝔇 ≡ χ non dice nulla sulla complessità: D si calcola dal bit con una ricerca non limitata.
- "Minimo assoluto" va sostituito con "minimo nell'ordine D2".

### OB-3 (MINOR · COSMETIC)
I controlli QMIN usano il nucleo del calore in p₀ = (1,0): illustrano il meccanismo su un'istanza diversa da (f).

**Fix:** etichettarli come "illustrazione" e citare l'istanza di S-CHECK-12 con p₀ = 0.

## 4. OP-ALG-L5, T4, P5, C1, Lemma NT
| MC | esito |
|---|---|
| L5(a) | OK. In A_2 la forma normale Σq_k∂_t^k ha q_k ∈ 𝒜 a sinistra. ∂_t^{n−m}P = ∂_t^n + (grado < n). Il coefficiente direttore di AP è quello di A. 𝔇/𝔇P ≅ 𝔄^m come 𝔄-moduli sinistri. |
| L5(b) | OK. Un dominio noetheriano è di Ore da entrambi i lati, quindi la torsione è un sottomodulo: per af si usa da = d′b. Per ∂_t si usa b(∂_tf) = −b_tf, poi b′b. Va menzionato il caso b_t = 0 (banale). |
| T4 | OK. (a)⟺(b) per divisione. (b)⟺(c): N è senza torsione e il rango è additivo. (b)⟺(d): b ≠ 0 e Q₀ ≠ 0 danno bQ₀ ≠ 0 di grado < m. |
| P5 | OK. L'eliminante L ∈ 𝒜 sta in I ⊆ Ann, quindi u ∈ 𝒯_𝒜 e Q = 1 viola (d). **SymPy:** (2t∂_x + x)G = 0, quindi in A_2 neanche il nucleo del calore identifica. |
| C1(i)–(ii) | OK. Identità verificate su una funzione generica f(t,x): P_1P_2 = P_2P_1, P_1∂_x = ∂_xP_2, (1+λ∂_x)P = P_1Q_λ. Sulle soluzioni: P_2u_2 = 0, Pu^{(λ)} = 0, P_1u^{(λ)} = −u_2, P_2u^{(λ)} = λ∂_xu_2, Q_λu^{(λ)} = 0, Q_λu^{(μ)} = (μ−λ)∂_xu_2. Q_λ ha grado 1 in ∂_t e coefficiente 1 + λ∂_x ≠ 0, quindi Q_λ ∉ 𝔇P. |
| Lemma NT | OK. Primo passo: Φ(t,x,e^t) ≡ 0 implica φ_k ≡ 0 per C3-L3(b), fetta per fetta. Secondo passo: f_w = Ã(·,w)e^{w²x²} con w > 0 distinti sono soluzioni dell'EDO b_{t₁}. Su J il coefficiente direttore non si annulla, quindi lo spazio delle soluzioni ha dimensione ≤ ordine. L'indipendenza segue dalla dominanza per x → ∞, dopo l'estensione analitica a ℝ. Ã(·,w) ≢ 0 salvo un numero finito di w. **V-ex:** nessun b di ordine ≤ 2 con coefficienti di grado ≤ 2 annulla u_2. |
| C1(iii) | OK. L_λ è un ideale sinistro saturato. rank N_λ = 1, perché 1 ∉ L_λ per il Lemma NT. Q_λ ∉ L_μ. N_λ ∩ N_μ è saturato e di rango ≤ 1, quindi è 0. |
| C1(iv) | OK. Per T ∉ 𝔇P, {λ : T ∈ L_λ} ha al più un elemento. → OC-1 (portata della sintesi). |
| C1(v) | OK. La corrispondenza (b_0,b_1) ↔ (c,d) è biiettiva. Gli esponenti ±e^t sono distinti. L'argomento degli e^{kt} dà γ_j = δ_j = 0. **V-ex:** su 25 punti, nessuna relazione di grado basso. |

### OC-1 (MINOR · OVERSTATED · LOCAL)
PROOF_PACKAGE §0.3 dice: "La struttura I = G·J fallisce, e con essa ogni criterio a numero finito di test". (iv) però esclude solo i criteri della forma "Tu ∉ 𝒯_𝔄 per T in una lista finita dipendente solo da P". K6 di §7 lo riconosce.

**Fix:** in §0 e nella riga C3-Q2, scrivere "ogni criterio a numero finito di test del tipo 'Tu ∉ 𝒯_𝔄'".

## 5. INT-18
Verifica (§5 (1)–(3)): **OK**.
- Con P(∂)u = 0, G_u ∼ P implica P = G_u·j, con j ∈ J_u costante non nulla, quindi J_u = R. σ_p = ∅ è dunque ridondante.
- V(Ann u) = V(P) se e solo se ogni P_i divide G_u. Lo garantiscono il Fatto (F) e la finitezza di V(J_u).
- Esempi verificati con SymPy:
  - (τ−ξ²)(tG) = G;
  - u₃ = G + (t−1)e^{(t−1)+x}: P(∂)u₃ = 0, (τ−ξ²)u₃ = e^{(t−1)+x}, e (1,1) ∈ V(τ−ξ²).

**OI-1 (MINOR · OVERSTATED · LOCAL), testo proposto.** Tre correzioni:
1. "decidibile quando u è analitica e olonoma (data come formula: OP-ALG-T1)" → "decidibile quando u è reale-analitica su Ω connesso ed è dato un ideale olonomo a coefficienti in ℚ̄ che la annulla, con i getti in un punto algebrico calcolabili in un campo computabile (modello M3-hol, assunzione (AC): OP-ALG-T1)".
2. "non decidibile a scatola nera … (P4-T5)" → "(P4-T5 + P4-L7)".
3. "il dato aggiuntivo minimo per decidere è la risposta stessa, equivalente a un limite sul grado di un testimone, mentre ricostruire G_u richiede esattamente un maggiorante di dim(R·u ∩ EP)" → "nell'ordine dei dati per computabilità a oracoli (senza limiti di risorse), il dato minimo per decidere è la risposta stessa, equivalente a un limite sul grado di un testimone; un maggiorante di dim(R·u ∩ EP) equivale a conoscere G_u ed è strettamente più forte del minimo su qualche dominio quando Σe_i ≥ 2 (OP-ALG-T3)".

Il resto del testo è corretto. Resta la decisione dell'utente.

## 6. Problemi
- **C3-Q1:** CHIUSO nel modello M3-hol (OP-ALG-T1(i)–(iii), DIMOSTRATO modulo (AC)). Fuori modello restano le ostruzioni P4-T5 + P4-L7 e P4-C4(a).
- **P4-Q1:** CHIUSO. Il maggiorante B di T1(v) non dipende da OA-1.
- **P4-Q-min:** CHIUSO, con OB-1 e OB-2: χ ≡ 𝔇; 𝔅 ≡ 𝔊; 𝔅 ≡ χ se P è irriducibile ridotto; χ < 𝔅 su qualche (Ω, p₀) se Σe_i ≥ 2. Il caso universale è il nuovo **OP-ALG-Q2 APERTO**.
- **C3-Q2:** CHIUSO come criterio (T4) più teorema negativo (C1 per criteri a test finiti del tipo Tu ∉ 𝒯; P5). Il residuo è OP-ALG-Q1 APERTO.

## 7. Confronto con il passaggio avversariale interno (§7 del package)
- Il passaggio interno non aveva visto il campo di definizione (OA-1). K4 tratta solo gli esponenti, che stanno davvero in K.
- Non aveva visto il quantificatore su (Ω, p₀) (OB-1).
- K6 coincide con OC-1, ma §0 non ne tiene conto.
