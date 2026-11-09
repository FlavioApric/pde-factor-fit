# AUDIT S4-ID — identificazione non lineare relativa a un dizionario (Fase 4, G★′-NL punto 2)
Revisore: S-CHECK-10 (10ª tornata), 26/10/2026. Revisore indipendente: non ho scritto nessuna delle prove; non ho letto gli script di S4-ID (s4id_checks*.py, explore2.py, reduction_checks.py): il red team SymPy è scritto da zero.
**Fonte esaminata:** `work/S4-ID/CHECK_REQUEST.md` (quadro, fatti importati, tabella dei claim, punti delicati) e, come dichiarato dalla stessa CHECK_REQUEST ("le prove sono complete in quel file"), le prove in `work/S4-ID/PROOF_PACKAGE.md` §1–§6 (riferimenti puntuali: §2 T1, C1; §3 L2, C2, P1; §4 L5, T2, T3, L4, P5, P6, P7; §5 D2, T4; §6 P8). §7 (novità) e §8 (kill-argument) letti solo per sapere che cosa è già stato attaccato; il mio giudizio non ne dipende.
**Fatti usati come dati:** ALG-L1 (S4-INTEG; PASS in AUDIT_S4-INTEG.md, S-CHECK-9 — in più ne ho ricontrollato io i passi usati da T1, §1.1), ALG-T1(a)(b)(c) (PASS-con-fix MINOR, S-CHECK-9), MODREL-T1 + Cor., INT-T1(B) (S-CHECK-9), C3-L3(b) (DIMOSTRATO). CON-FONTE non auditate: Hölder (Γ), Bona–Smith/Kato, Umemura–Watanabe, Deift–Zhou/Grunert–Teschl, Scholl et al. (C1(i)).
**Skill caricate** (lettura dei SKILL.md, nessuno script _vendor eseguito): skills-local/session-protocol (per prima), skills-local/claim-lifecycle, _vendor/Auto-claude-code-research-in-sleep/skills/proof-checker (enunciati canonici + micro-claim, checklist A–H, red team, severità a due assi, acceptance gate; revisore = io, niente Codex), _vendor/scientific-agent-skills/skills/sympy.
**SymPy:** `work/CHECK/sympy/audit_s4id.py` → `audit_s4id_part1.out` (= `audit_s4id.out`) e `audit_s4id_part2.out`; `audit_s4id_fix.py` → `audit_s4id_fix.out` (.venv, -I): **61/61 OK** dopo la correzione di tre errori miei nello script (§9).

## 0. Verdetto
| claim | verdetto | stato proposto |
|---|---|---|
| **S4ID-T1** (a)–(e) | **PASS** | **DIMOSTRATO** (lemma di riduzione; dipende da ALG-L1, DIMOSTRATO) |
| **S4ID-C1** (i)(ii) | PASS | (i) **CON-FONTE (anticipato, Scholl et al.)** + prova propria corretta; (ii) DIMOSTRATO |
| **S4ID-L2**, **S4ID-C2** | PASS | DIMOSTRATO |
| **S4ID-P1** (a)(b)(c) + Conseguenza | **PASS-con-fix(ID-4)**, MINOR (portata della precisazione in PROBLEM.md, non della prova) | **DIMOSTRATO** (per N = σy_n + N′, σ ≠ 0, deg N = 2) |
| **S4ID-L5** | PASS | DIMOSTRATO |
| **S4ID-T2** (a)(b)(c)(d), (e) grado ≤ 1 | **PASS** | **DIMOSTRATO**; K1 (grado ≤ N a ogni ordine) resta CONGETTURA |
| **S4ID-T3** (a)(b) | PASS | DIMOSTRATO; (c) V-ex (confermato da me per k = (1,2)); (d) eredita INT-T1(B) |
| **S4ID-L4** | PASS | DIMOSTRATO |
| **S4ID-P5** (i)(ii)(iii) | PASS | DIMOSTRATO ((iii) via MODREL-T1 Cor.) |
| **S4ID-P6** | PASS (riduzione) | DIMOSTRATO come riduzione; il contenuto resta INT-T1 |
| **S4ID-P7** (i)–(iv) | **PASS-con-fix(ID-2)**, MINOR | DIMOSTRATO |
| **S4ID-T4** (i)(ii); (iii) Burgers; (iv); D2 | **PASS-con-fix(ID-1, ID-5)**, MINOR | (i), (ii) DIMOSTRATO; (iii) DIMOSTRATO mod Hölder (CON-FONTE) per Burgers, mod Bona–Smith/Kato per KdV; (iv) riduzione DIMOSTRATA, "∉ 𝔉" CON-FONTE non verificata |
| **S4ID-P8** | **PASS (logica) — CONDIZIONALE a (H-as)**, con fix ID-3 (MINOR) | **CONDIZIONALE** (non DIMOSTRATO): vale se e solo se (H-as) è un teorema nella forma enunciata (uniformità e convenzione di fase da verificare su Grunert–Teschl) |

Nessun rilievo FATAL, CRITICAL o MAJOR. Acceptance gate: zero FATAL/CRITICAL aperti; ipotesi esplicite in ogni enunciato; ogni applicazione di un lemma scarica le ipotesi (controllato per ALG-L1 in T1, C3-L3(b) in T2(I)/T3, L5 in T3(a), C1 in T2(d)/P7(iv), MODREL-T1 in P5(iii), INT-T1(B) in T3(d)); red team eseguito su tutti i lemmi chiave (§9), controesempi cercati attivamente per P1 (§3.4).

## 1. S4ID-T1 — successione esatta (priorità 1)
### 1.1 Enunciato canonico
∀Ω ⊂ ℝ² aperto non vuoto, ∀N ∈ A d'ordine n ≥ 1, ∀u ∈ C^∞(Ω;ℂ) con u_t = N(u) su Ω, ∀V ⊂ ℂ{y} sottospazio ℂ-lineare (dimensione qualsiasi):
(a) I(u) ∩ V = (ψ|_V)^{−1}(J_u); (b) 0 → [F]∩V →^{incl} I(u)∩V →^{ψ} J_u∩ψ(V) → 0 esatta; (c) I(u)∩V = [F]∩V ⟺ J_u∩ψ(V) = 0; (d) F ∈ V ⇒ (I(u)∩V = ℂF ⟺ [F]∩V = ℂF ∧ J_u∩ψ(V) = 0); (e) Gram.
Nessuna ipotesi su Ω oltre "aperto non vuoto" (limitato o no, connesso o no); nessuna analiticità; ℂ{y} a coefficienti costanti.

**Definizione di ψ (controllata).** ℂ{y} è l'anello di polinomi libero sulle indeterminate θy (θ = ∂_t^a∂_x^b), quindi ψ è ben definito come l'unico omomorfismo di ℂ-algebre con θy ↦ D_N^aD^by_0. Che sia un omomorfismo **differenziale** (∂_x ↦ D, ∂_t ↦ D_N) richiede [D, D_N] = 0 su A: [D, D_N] è una derivazione di A e sui generatori D D_Ny_j = D^{j+1}N = D_N y_{j+1} = D_N D y_j, quindi è nulla. Su un generatore: ψ(∂_xθy) = D_N^aD^{b+1}y_0 = Dψ(θy) (commutazione), ψ(∂_tθy) = D_Nψ(θy). Le due derivazioni ∂_t, ∂_x di ℂ{y} e le loro immagini sono derivazioni, e un omomorfismo che intreccia due derivazioni sui generatori le intreccia ovunque (regola di Leibniz). ψ|_A = id (a = 0). ψ(V) := immagine lineare di V, sottospazio di A. **OK.**
**ALG-L1 nei punti usati (ricontrollato, oltre al PASS di S-CHECK-9).** (α) Per p ∈ A, ∂_tp − D_Np = Σ_j(∂p/∂y_j)(∂_x^jy_t − D^jN) = Σ_j(∂p/∂y_j)∂_x^jF ∈ [F] (in ℂ{y}, ∂_x^jN = D^jN perché ∂_x|_A = D). (β) Per induzione su a: θy − ψ(θy) ∈ [F]; il passo è ∂_t^{a+1}∂_x^by − D_Nψ = ∂_t(∂_t^a∂_x^by − ψ(∂_t^a∂_x^by)) + (∂_t − D_N)ψ(∂_t^a∂_x^by), somma di un elemento di [F] (ideale differenziale) e di un elemento di [F] per (α). (γ) G − ψ(G) ∈ [F] per ogni G: si sostituisce θy = ψ(θy) + (θy − ψ(θy)) nei monomi e si sviluppa (ogni termine con almeno un fattore θy − ψ(θy) sta in [F]). (δ) ker ψ = [F]: ψ(F) = N − N = 0 e ψ differenziale ⇒ [F] ⊆ ker ψ; G ∈ ker ψ ⇒ G = G − ψ(G) ∈ [F]. **OK.**

### 1.2 Micro-claim
| MC | passo | esito |
|---|---|---|
| T1.1 | [F] ⊆ I(u) | OK. ev_u: ℂ{y} → C^∞(Ω), θy ↦ θu, è un omomorfismo di anelli che intreccia ∂_t, ∂_x perché u ∈ C^∞ (le derivate miste commutano: Schwarz). ev_u(gθF) = g(u)·θ(F(u)) = 0. Solo C^∞ (anzi basta C^r con r ≥ ordine degli elementi coinvolti, per V di dimensione finita). |
| T1.2 | (a): G(u) = ψ(G)(u) per G ∈ V | OK. G − ψ(G) ∈ [F] ⊆ I(u) (ALG-L1(γ) + T1.1). Nessuna analiticità, nessuna ipotesi su Ω: è un'identità puntuale. **Punto delicato 1 della CHECK_REQUEST: superato.** |
| T1.3 | esattezza a sinistra | OK (inclusione). |
| T1.4 | esattezza al centro: ker(ψ|_{I(u)∩V}) = [F]∩V | OK. ker ψ ∩ I(u) ∩ V = [F] ∩ I(u) ∩ V = [F] ∩ V (perché [F] ⊆ I(u)). |
| T1.5 | ψ(I(u)∩V) ⊆ J_u ∩ ψ(V) | OK: ψ(G) ∈ A ∩ I(u) = J_u per (a); ψ(G) ∈ ψ(V). |
| T1.6 | suriettività su J_u ∩ ψ(V) | OK: p = ψ(G), G ∈ V; p ∈ J_u ⇒ G ∈ I(u) per (a). Nota: è qui che serve ψ(V) e non V ∩ A (in generale ψ(V) ⊋ V ∩ A): la successione è esatta con il termine giusto. |
| T1.7 | formula delle dimensioni | OK (rango + nullità, dim V < ∞). |
| T1.8 | (c), (d) | OK. In (d) la catena ℂF ⊆ [F]∩V ⊆ I(u)∩V e "uguaglianza tra estremi ⟺ entrambe le uguaglianze". "[F]∩V dipende solo da (F, V)": vero; ψ(V) dipende da (F, V), J_u solo da u (frase già corretta da KA-1). |
| T1.9 | (e) Gram | OK. λ^*𝔾λ = ∫|Σλ_kb_k(u)|² con 𝔾 = ∫Φ̄Φ^T hermitiana semidefinita; 𝔾λ = 0 ⟺ λ^*𝔾λ = 0 (semidefinita); Σλ_kb_k(u) = 0 q.o. ⇒ ovunque (continuità) ⟺ Σλ_kb_k ∈ I(u) ∩ V. Poi (b). Ipotesi b_k(u) ∈ L²(Ω) esplicita. |

**Verdetto T1: PASS. Stato: DIMOSTRATO.** Osservazione (non un rilievo): T1 è un corollario di poche righe di ALG-L1 (lo dice S4-ID stesso, §7); il suo valore è di quadro. Red team: §9 blocco C (successione verificata in modo **indipendente da ALG-L1**, con serie formali di soluzioni generiche) e blocco D (N-shock esatti).

## 2. S4ID-C1, S4ID-L2, S4ID-C2
- **C1(i)**: ψ(ay_t + m) = aN + m; nullo ⟺ m = −aN ⟺ ay_t + m = aF; ψ(V) = ℂN + M = M (N ∈ M). Poi T1(d). OK. **C1(ii)**: y_t − m ∈ I(u) ⟺ N − m ∈ J_u (T1(a)) ⟺ m ∈ N + J_u. OK. Stato: (i) CON-FONTE anticipato (Scholl et al. Prop. 1, come registrato) con prova propria corretta; (ii) DIMOSTRATO.
- **L2**: induzione su a con m = na + b: D_N(σ^ay_m) = σ^a(σy_{m+n} + D^mN′), ord D^mN′ ≤ n−1+m; D_Nq = Σ_{j<m}(∂q/∂y_j)D^jN con ordine ≤ n+m−1. Grado: D_Np = Σ(∂p/∂y_j)D^jN ha grado ≤ deg p − 1 + deg N ≤ deg p + δ − 1. Inoltre (usato in P1) y_{na+b} compare in ψ(θy) **solo linearmente** (q_{a,b} non contiene y_{na+b}). OK; SymPy §9 blocco A (4 banchi, a, b ≤ 2).
- **C2**: monomio di V_{d,k} con e ≤ d fattori, |θ_i| ≤ k: grado ≤ Σ(1 + a_i(δ−1)) ≤ d(1 + k(δ−1)) (δ ≥ 1), ordine ≤ max(na_i + b_i) ≤ nk (n ≥ 1). OK.
**Verdetto: PASS.**

## 3. S4ID-P1 (con L2) — teorema negativo (priorità 1, controllato con cura)
### 3.1 Enunciato canonico
Sia N = σy_n + N′, σ ∈ ℂ∖{0}, n ≥ 1, N′ ∈ ℂ[y_0..y_{n−1}], deg N = 2 (cioè N′ ha componente quadratica N_2 ≠ 0; N è lineare in y_n con coefficiente costante). Allora: (a) F ∈ V_{d,k} ⟺ d ≥ 2 ∧ k ≥ n; (b) d ≥ 2, k ≥ n, (d,k) ≠ (2,n) ⇒ dim([F]∩V_{d,k}) ≥ 2; (c) [F]∩V_{2,n} = ℂF. Conseguenza (con T1(d)): per ogni soluzione u e ogni (d,k) ≠ (2,n) con F ∈ V_{d,k}, I(u)∩V_{d,k} ⊋ ℂF.
### 3.2 Micro-claim
| MC | passo | esito |
|---|---|---|
| P1.1 | (a) | OK: V_{d,k} è lo span dei monomi; F ∈ V_{d,k} ⟺ ogni monomio di F è in 𝓓_{d,k}; i monomi sono y_t (ordine 1), y_n, quelli di N′ (con uno quadratico): k ≥ max(1,n) = n, d ≥ 2. |
| P1.2 | (b), k ≥ n+1 | OK: ∂_xF = y_{tx} − σy_{n+1} − DN′ ∈ V_{2,max(2,n+1)} ⊆ V_{d,k} (D conserva il grado); contiene y_{n+1}, F no. Anche n = 1 (k ≥ 2, y_{tx} ha ordine 2). |
| P1.3 | (b), d ≥ 3 | OK: yF ∈ V_{3,n}, contiene y·y_t. (d,k) ≠ (2,n) con d ≥ 2, k ≥ n ⟺ k ≥ n+1 ∨ d ≥ 3: casi esaustivi. |
| P1.4 | (c) generatori, λ = na + b ≥ n+1 e iniettiva su Θ_+ | OK. a = 1 ⇒ 1 ≤ b ≤ n−1, λ = n + b ∈ [n+1, 2n−1]; a ≥ 2 ⇒ λ ≥ 2n ≥ n+1; per a ≥ 1, b ≤ n − a ≤ n − 1 < n, quindi (a, b) = divisione euclidea di λ per n. Per n = 1, Θ_+ = ∅ (caso banale, coperto). **Punto delicato 2: superato.** |
| P1.5 | Passo 1: y_{λ*} compare in ψ(G) solo tramite ψ(θ*y), e solo linearmente in ψ(θ*y) | OK: θ ∈ Θ_+ con λ(θ) > λ* non compaiono in G (massimalità); quelli con λ < λ* e y_t, y_b hanno immagini d'ordine < λ* (ord ψ(y_t) = ord N = n < n+1 ≤ λ*); in ψ(θ*y) = σ^{a*}y_{λ*} + q, q non contiene y_{λ*} (L2). |
| P1.6 | coefficiente di y_{λ*}² (c = 0) e di y_{λ*} (ψ(L) = 0) | OK: G ha grado ≤ 2 nei generatori, quindi G = c(θ*y)² + (θ*y)L + G₀ con L di grado ≤ 1 è la forma generale. |
| P1.7 | indipendenza di {1} ∪ {ψ(g) : g ≠ θ*y} ⇒ L = 0 | OK: ∂/∂y_{λ(θ)} della combinazione, per il θ ∈ Θ_+ di λ massimo con coefficiente ≠ 0, vale σ^a·coeff ≠ 0; restano 1, y_0..y_n, N: indipendenti perché N_2 ≠ 0. |
| P1.8 | Passo 2 per gradi | OK: componente di grado 4 c_{tt}N_2² = 0 ⇒ c_{tt} = 0 (ℂ[y] dominio, N_2 ≠ 0); grado 3: (Σc_{tb}y_b)N_2 = 0 ⇒ c_{tb} = 0 (G₀ e c_tN hanno grado ≤ 2); resta G₀ = −c_tN. **Il Passo 2 usa davvero N_2 ≠ 0** (punto delicato 2). |
| P1.9 | Conseguenza | OK: per u soluzione [F] ⊆ I(u) (T1.1), quindi I(u)∩V ⊇ [F]∩V ⊋ ℂF. |

### 3.3 Il ruolo delle ipotesi (dove si romperebbe)
- **σ costante non nullo** serve a L2 (termine dominante σ^ay_λ) e quindi al Passo 1. Con coefficiente non costante di y_n (es. N = −y_0y_1, Burgers inviscido, n = 1) l'enunciato non è coperto. Il calcolo (§9 B3, informativo) mostra che per Burgers inviscido [F]∩V_{2,1} = ℂF comunque, ma non è un caso del teorema.
- **deg N = 2.** Per deg N ≥ 3 (es. mKdV, N = −y_3 − 6y_0²y_1) F ∉ V_{2,n} e il dizionario minimo diventa V_{deg N, n}; S4-ID lo dichiara aperto (S4ID-Q3). Già il fatto F ∉ V_{2,n} mostra che l'eccezione "(2,n)" **non** si trasferisce letteralmente (il calcolo di [F]∩V_{3,3} per mKdV è stato omesso per memoria). Questo non tocca P1 (che ha l'ipotesi), ma tocca la **precisazione in PROBLEM.md** → ID-4.
### 3.4 Ricerca di controesempi (eseguita)
(1) Valori dichiarati di dim([F]∩V_{d,k}) ricalcolati con un'implementazione indipendente di ψ (Burgers ν = 1/3, Fisher, KdV, KdV–Burgers; 11 casi). (2) N casuali di grado 2 nella forma dell'ipotesi, n = 1, 2, 3, 4 (due per n): =1 in (2,n), ≥ 2 in (2,n+1), (3,n), (3,n+1). (3) Controllo indipendente da ALG-L1: per una soluzione a dato di Cauchy generico (serie formale esatta mod p) dim I(u)∩V_{d,k} coincide con dim ker ψ|_V (cioè J_u ∩ ψ(V) = 0, come atteso per un dato generico), in 7 casi. Nessun controesempio. Esiti in §9.
**Verdetto P1: PASS-con-fix(ID-4). Stato: DIMOSTRATO** (con l'ipotesi deg N = 2, N = σy_n + N′).

## 4. S4ID-L5, S4ID-T2 (N-shock di Burgers)
### 4.1 L5
| MC | esito |
|---|---|
| X ↦ sX commuta con D | OK: D preserva il grado omogeneo in X (DX^m = ⟨m,k⟩X^m), quindi agisce coefficiente per coefficiente sulla serie in s; la localizzazione ai denominatori non nulli in 0 rende ben definita l'immersione in ℂ[X][[s]]. |
| ordine s⁰ ⇒ G_0 = 0; ordine s^{e₀} ⇒ G_{e₀}(ℓ, Dℓ, …) = 0 | OK (le componenti di grado > e₀ contribuiscono da s^{e₀+1}). |
| W = ℂ^{K+1} se K+1 ≤ N | OK: matrice (α_ik_i^j), j = 0..K, rango K+1 (Vandermonde a k_i distinti, colonne scalate da α_i ≠ 0; k_i = 0 ammesso). |
**PASS → DIMOSTRATO.**
### 4.2 T2
| MC | passo | esito |
|---|---|---|
| T2.0 | u = −2νφ_x/φ risolve Burgers; φ_t = νφ_xx | OK (Cole–Hopf; SymPy §9 J per N = 1). |
| T2.I | (NR) ⇒ E^m (m ∈ ℕ^N) linearmente indipendenti su ogni aperto (C3-L3(b) con q_k costanti) ⇒ ℂ[X] → C^ω(Ω) iniettiva ⇒ ℂ(X) ↪ 𝓜(Ω) (Ω connesso) che intreccia D e ∂_x; p ∈ J_u ⟺ p(u-getto) = 0 in ℂ(X) | OK. Ipotesi di C3-L3(b) scaricate: esponenti distinti per (NR) (differenze in ℤ^N∖0), aperto non vuoto. (NR) per N = 2 ⟺ k_1 ≠ k_2: verificato (k_i ≠ 0). **Punto delicato 3a: superato.** |
| T2.II | p_i = X_i/φ algebricamente indipendenti; r_j = Σk_i^jp_i; Dr_j = r_{j+1} − wr_j; r_j = Y_j (Bell completi), (Y-a), (Y-b) | OK. 1 − Σp_l = 1/φ, X_i = p_i/(1 − Σp_l). Ricorrenza Y_{j+1} = 𝔇Y_j + w_0Y_j con r_0 = 1, r_1 = w. |
| T2.a | ℂ[w..D^{N−1}w] = ℂ[r_1..r_N] (triangolare), r = Vp con det V = Πk_i·Π(k_l − k_i) ≠ 0 | OK. **Punto delicato 3b (Vandermonde): superato.** |
| T2.b | Σe_mr_m = Σ_ip_ik_iΠ_l(k_i − k_l) = 0; R_N = −y_N/2ν + β; deg N+1, top (−2ν)^{−N−1}y_0^{N+1}; divisione per R_N (grado 1 in y_N, coefficiente costante) | OK. Irriducibilità: un fattore libero da y_N divide il coefficiente direttore costante. Dimensione binom(d, N+1) = numero di monomi in N+1 variabili di grado ≤ d−N−1. **Punto delicato 3c: superato.** |
| T2.c | D^jR_N = −y_{N+j}/2ν + (ordine < N+j); divisioni successive | OK. |
| T2.d | criterio in V^{ev}_{d,K} (C1) e in V_{d,k} (C2 con n = δ = 2) | OK. Nota: "K = N" richiede N ≥ 2 (K ≥ 2 perché N_B ∈ A_{≤d,≤K}). |
| T2.e | grado ≤ 1: specializzazione X_2 = … = X_N = 0 (ideale D-stabile, φ ↦ 1 + X_1), poli d'ordine j+1 in X_1 = −1 | OK: l'omomorfismo ℂ[X][1/φ] → ℂ[X_1][1/(1+X_1)] commuta con D. Numeratore non nullo in −1 verificato in SymPy (j ≤ 6) e per induzione: D(f/(1+X)^{j+1}) = kX(f′(1+X) − (j+1)f)/(1+X)^{j+2}, che in X = −1 vale k(j+1)f(−1) ≠ 0. |
**Verdetto T2: PASS. Stato: (a)–(d) DIMOSTRATO; (e) grado ≤ 1 DIMOSTRATO; K1 CONGETTURA (V-ex).** SymPy §9 blocchi D, E, F (inclusi R_N per N = 1, 2, 3 e k = (2,−1,5), dimensioni 0/1/binom, (c) a ordine N+1, conteggio 21/4/1 dei 1-, 2-, 3-shock in V_{2,2}).

## 5. S4ID-T3 (N-solitoni di KdV), parti dimostrate
| MC | passo | esito |
|---|---|---|
| T3.0 | riduzione al formale con esponenti (−k_i³, k_i) e (NR) | OK (come T2.I; f > 0 per k_i > 0 reali, A_{ij} > 0). Nota: per N ≥ 3 (NR) non è automatica: è ipotesi esplicita. |
| T3.a | L5(ii) con u(sX) = 2sΣk_i²X_i + O(s²) | OK: f(sX) = 1 + sΣX_i + O(s²) (i prodotti hanno grado ≥ 2), f(0) = 1; α_i = 2k_i² ≠ 0, k_i distinti. |
| T3.b | P := J_u ∩ ℂ[y_0..y_N] primo, ≠ 0, ℂ[y_0..y_N]/P di trdeg N | OK: nucleo di un omomorfismo verso un campo; N+1 elementi in ℂ(X) (trdeg N) sono dipendenti; trdeg ≥ N per (a). |
| T3.b′ | ht P = 1 ⇒ P principale | OK: per un'algebra affine dominio, ht P + dim(ℂ[y]/P) = N+1, quindi ht P = 1; in un UFD ogni primo di altezza 1 è principale (contiene un fattore primo π di un suo elemento non nullo, (π) è primo non nullo ⊆ P, altezza 1 ⇒ uguaglianza). **Punto delicato 4: superato.** |
| T3.Π1 | u = 2k²p(1−p), u_x = 2k³p(1−p)(1−2p), (1−2p)² = 1 − 2u/k² ⇒ Π_1 ∈ J_u; irriducibile (y_0²(k² − 2y_0) non quadrato) ⇒ Π_1 genera P | OK (SymPy §9 G). |
| T3.crit | K = N ⇒ identifica ⟺ d < deg Π_N; 1-solitone non identifica mai (Novikov a ordine 2, grado 2) | OK. |
**Verdetto T3(a)(b): PASS. Stato: DIMOSTRATO.** (c) V-ex: ho ricalcolato deg Π_2 = 8 per k = (1,2) (§9 G) e, a titolo informativo, per k = (1,3) (anche lì deg Π_2 = 8: due valori di k concordi, l'indipendenza da k resta comunque non dimostrata). (d) eredita lo stato di INT-T1(B).

## 6. S4ID-L4 e S4ID-P5
**L4** — enunciato canonico: ∀ν ∈ ℂ, ∀Q_1, Q_2 ∈ ℂ[τ,ξ]: Q_1(∂)y + Q_2(∂)y² ∈ [F_B] ⇒ ∃A ∈ ℂ[τ,ξ]: Q_1 = A(τ − νξ²), Q_2 = Aξ/2.
| MC | esito |
|---|---|
| divisione per τ − νξ² (monico in τ), G′ = b(∂_x)y + Q(∂)y² ∈ [F_B] | OK. |
| ψ(Q(∂)y²) = Q(D_N, D)(y_0²); D_N = D_ν + D_B, D_ν conserva il grado, D_B lo alza di 1 | OK. **Non serve che D_ν e D_B commutino**: nello sviluppo di (D_ν + D_B)^m in parole non commutative l'unica parola che raggiunge grado m+2 è D_B^m (parole con j lettere D_B danno grado 2 + j). Questo va detto (INFO-1), il testo lo lascia implicito. |
| D_B(y_0^j) = −(j/(j+1))D(y_0^{j+1}) e induzione: D_B^m(y_0²) = (−1)^m(2/(m+2))D^m(y_0^{m+2}) | OK (usa [D, D_B] = 0; SymPy m ≤ 4). **Punto delicato 5: superato.** |
| q(D)(y_0^E) ≠ 0 per q ≠ 0 (peso) | OK: D^j(y_0^E) omogeneo di peso j, contiene Ey_0^{E−1}y_j. |
| m = 0: separazione dei gradi 1 e 2 | OK. |
Brute force indipendente (§9 H): ker ψ su {Q_1(∂)y + Q_2(∂)y², deg Q_i ≤ 3} ha la dimensione di {A·F_B : deg A ≤ 1} (ν ≠ 0) e di {A·F_B : deg A ≤ 2} (ν = 0). **PASS → DIMOSTRATO.**
**P5** (i) iniettività di ι: per j fissato il monomio y^{j−1}·θy compare in θ′(y^j) solo per θ′ = θ (Leibniz: ogni altro termine ha ≥ 2 fattori non banali o è y^j); coefficiente j (θ ≠ 1) o 1 (θ = 1). OK. (ii) T1(b). (iii) L4 + MODREL-T1 Cor. (v_B primitivo: gcd(τ − νξ², ξ/2) = 1). **PASS → DIMOSTRATO.**
**P6**: riduzione corretta (C1(ii) con M₀ = span{K_n}); il contenuto è INT-T1 (S-CHECK-9). **PASS** come riduzione.

## 7. S4ID-P7 (MON-1 corretto) e S4ID-P8 (condizionale)
**P7.** (i) sottrazione: OK (serve u ∈ C², f ∈ C¹). (ii) se λ ≠ 0, h = G(u)/λ su U; in un punto con dh∧du ≠ 0 la mappa (u, h) è un diffeomorfismo locale (h ∈ C¹ perché u ∈ C⁴ … basta C³), quindi l'immagine di un intorno è aperta e contiene due punti con la stessa u e h diversa: contraddizione con "h funzione di u". G continua soltanto: l'argomento è insiemistico, OK. Poi G(u)u_x = 0 ⇒ G = 0 su u(U) e, per continuità, sulla chiusura. (iii) verifica diretta, OK (con l'estensione costante [fix KA-7]). (iv) → **ID-2**. La "Correzione rispetto a F4-HOR §7" è corretta: dh∧du ≡ 0 su U dà h = H(u) solo localmente (su componenti dove u è monotona in x), e né (ii) né (iii) coprono quel caso intermedio: la condizione di (ii) è sufficiente, non necessaria, ed è enunciata così. SymPy §9 J: 1-shock con H affine. **PASS-con-fix(ID-2) → DIMOSTRATO.**
**P8 (solo logica; CONDIZIONALE).** (1) e₀ ≥ 1: u(t,·) di Schwartz ⇒ getto → 0 per x → +∞, p(0) = 0. OK. (2) lungo (t_m, x_m) il getto è t_m^{−1/2}(v + o(1)): richiede che (H-as) valga uniformemente per k_m := √(−x_m/12t_m) in un compatto di J, con α continua: è **dentro** l'ipotesi (H-as) come scritta ("o(·) uniforme lungo le successioni sotto", "α continua"). OK come implicazione. (3) p polinomio: Σ_et_m^{−e/2}p_e(v + o(1)), moltiplicando per t_m^{e₀/2}: p_{e₀}(v) = 0. OK. (4) omogeneità (α > 0) e polinomialità in (A, κ) per θ fisso: nullo su (0,∞) × 2J aperto ⇒ identicamente nullo. OK. (5) parte lineare: → **ID-3** (la scrittura "Re(e^{iθ}…)" vale per c_j reali; con c_j complessi si usa l'indipendenza di e^{±iθ}; conclusione invariata, SymPy §9 J). (6) "p non ha parte lineare non nulla": se e₀ ≥ 2 è vacuo, se e₀ = 1 segue da (5). OK. Esempi y_0y_3 − y_1y_2, y_0y_4 − y_2² ∈ I_PW: OK (SymPy). **Verdetto: PASS della logica; stato CONDIZIONALE a (H-as)** — non può salire a DIMOSTRATO finché (H-as), con l'uniformità lungo successioni e la differenziabilità termine a termine fino all'ordine K, non è verificata sulla fonte (Grunert–Teschl 2009; Deift–Venakides–Zhou). INT-Q1 resta APERTO.

## 8. S4ID-T4 (dicotomia, "forma chiusa", soglia D*)
**D2 (forma chiusa a torre).** Definizione ben posta: ogni passo (alg)/(int)/(exp)/(lin) produce un campo chiuso per ∂_t, ∂_x (per (alg) perché la derivata di un algebrico separabile sta nel campo generato; per (lin) per l'equazione). L'appartenenza è certificabile esibendo la torre; la non appartenenza no (lo dichiara). L'elenco "Contiene: …" è un elenco di esempi non dimostrati uno per uno: corretti EP, razionali, elementari, N-shock, N-solitoni, funzioni speciali via (lin); **"Cole–Hopf di dati EP" è ambiguo** → **ID-1**.
**(i)** trdeg K_s ≤ 2 + Σm_i (alg: +0; int, exp: ≤ +1; lin: ≤ +m); u, …, ∂_x^ru in K_s (chiuso per ∂_x) ⇒ dipendenti; un p con p(u-getto) = 0 in 𝓜(Ω) si annulla fuori da un chiuso a interno vuoto, quindi ovunque [fix KA-5]; poi T1(c). OK. È la direzione facile di ALG-T1(c) estesa alle torri (in linea con P3a-1 di S-CHECK-9) → **ID-5** (portata del termine "dicotomia", MINOR).
**(ii)** micro-claim: P_{j+1} = ∂(P_j)Q − (j+1)P_j∂Q dà ∂_x^ju = ev(P_j)/ev(Q)^{j+1} (OK); ∂ non alza il grado (X ↦ 1, T ↦ 0, E_i ↦ ξ_iE_i), deg P_j ≤ a + jb (OK); esponente D(n+1) − Σ(j_i + 1) ≥ 0 perché e ≤ D, j_i ≤ n (OK); deg Λ(m) ≤ e(a−b) + bD(n+1) ≤ cD (OK, e ≤ D, c = b(n+1) + max(a−b, 0)); ev(Λ(G)) = G(u)·ev(Q)^{D(n+1)} con esponente **uniforme** su tutti i monomi (è ciò che rende Λ lineare: OK); Λ(G) = 0 in S basta (non serve l'iniettività di ev); conteggio binom(D+n+1, n+1) > binom(cD+n, n) per D = D*: binom(cD+n,n) = Π(cD+i)/i ≤ c^n binom(D+n,n) (c ≥ 1), basta (D+n+1)/(n+1) > c^n ⟺ D > (n+1)c^n − n − 1. OK. **Punto delicato 6: superato.** Nota: n indica sia il numero di variabili di S sia l'ordine del getto; la scelta è coerente (n+1 funzioni del getto in un campo di trdeg ≤ n) ma va detta (INFO-2). Caso n = 0 (u costante): D* = 1, corretto. SymPy §9 I: disuguaglianza per n ≤ 5, c ≤ 8; 1-shock (n = 1, c = 2, D* = 3) ha davvero una relazione in A_{≤3,≤1}.
**(iii)** p ∈ J_u ⇒ p(u(t,·)) = 0 su (a,b) per t ∈ (0,T); continuità di ∂_x^ju fino a t = 0 ⇒ p(g, g′, …) = 0 su (a,b) ⇒ p = 0. OK. Burgers: G = ∫_0^xg limitata con derivate limitate; φ_0 = e^{−G/2ν} limitata, uniformemente continua con tutte le derivate (φ_0′ = −gφ_0/2ν a supporto compatto), ≥ e^{−‖G‖_∞/2ν}; ∂_x^jφ = e^{νt∂²}φ_0^{(j)} → φ_0^{(j)} uniformemente (nucleo del calore su funzioni limitate uniformemente continue); ∂_t^i∂_x^jφ = ν^i∂_x^{j+2i}φ ⇒ φ ∈ C^∞([0,∞)×ℝ) nel senso delle derivate unilaterali in t = 0; φ ≥ inf φ_0 > 0; u(0,·) = −2νφ_0′/φ_0 = g. OK. **Punto delicato 7: superato.** Γ: Hölder dà più del necessario (nessuna equazione algebrica differenziale nemmeno con coefficienti polinomiali in x); principio d'identità su (0,∞). OK mod CON-FONTE. KdV: mod Bona–Smith/Kato (CON-FONTE), la regolarità fino a t = 0 segue da u ∈ C([0,T]; H^s) ∀s e dall'equazione (∂_t = −6uu_x − u_xxx).
**(iv)** riduzione autosimile verificata in SymPy (§9 I); trdeg ≤ 5 (generatori (3t)^{1/3}, x, W, W′, W″). "∉ 𝔉" CON-FONTE non verificata (Umemura–Watanabe): lo stato di (iv) come "il viceversa è falso" è CON-FONTE.
**Verdetto T4: PASS-con-fix(ID-1, ID-5), MINOR.** Stato: (i), (ii) DIMOSTRATO; (iii) DIMOSTRATO mod CON-FONTE (Hölder per l'esempio Γ; Bona–Smith/Kato per KdV); (iv) riduzione DIMOSTRATA, stretta inclusione CON-FONTE non verificata.

## 9. Red team SymPy (`audit_s4id.py`, `audit_s4id_fix.py`)
**Esecuzioni.** (1) `audit_s4id.py` → `audit_s4id_part1.out` (= `audit_s4id.out`): blocchi A, B, B2 (n = 1, 2, 3), **25/25 OK**, poi MemoryError su B2 n = 4 (dizionario (3,4) troppo grande: limite della macchina, non del claim). (2) `audit_s4id.py part2` (salta A, B, B2 già eseguiti; n = 4 solo (2,4); M = 18) → `audit_s4id_part2.out`: **33/36 OK**; i 3 FAIL sono **errori miei nello script**, ricontrollati in (3) `audit_s4id_fix.py` → `audit_s4id_fix.out`: **3/3 OK**. Totale **61/61 OK** dopo la correzione, nessun FAIL attribuibile ai claim.
**I tre FAIL corretti (dichiarazione).** (a)(b) T2(c), N = 1, 2: avevo atteso dim J_u ∩ A_{≤N+1,≤N+1} = 2 (solo R_N, DR_N), dimenticando le combinazioni g·R_N + h·DR_N con g, h di grado ≥ 1 in cui le parti di grado > N+1 si cancellano (per N = 1: y_1R_1 − (y_0/2)DR_1 ha grado ≤ 2). Il valore misurato (3, 4) coincide con la dimensione calcolata **direttamente dall'ideale** (R_N, DR_N) troncato (moltiplicatori di grado ≤ 3): conferma di T2(c), non smentita. (c) P7(iii): `simplify` non riduceva un'espressione con tanh; riscritta in E = e^{kx+νk²t}: u_xx/u_x = k + u/ν esattamente (H affine globale), come dichiarato.
| blocco | contenuto | esito |
|---|---|---|
| A | [D, D_N] = 0 su polinomi casuali; L2 (termine σ^ay_{na+b}, ordine, grado ≤ 1 + a(δ−1)) per Burgers (ν = 1/3), Fisher, KdV, KdV–Burgers | 8/8 |
| B | dim([F]∩V_{d,k}) con ψ implementato da zero: Burgers (2,2) 1, (2,3) 3, (3,2) 7, (3,3) 34; Fisher (2,2) 1, (2,3) 6, (3,2) 7; KdV (2,3) 1, (2,4) 3, (3,3) 11; KdV–Burgers (2,3) 1 — **tutti uguali ai valori di S4-ID** | 11/11 |
| B2 | N casuali di grado 2 nella forma σy_n + N′, n = 1, 2, 3, 4: dim = 1 in (2,n) e ≥ 2 in (2,n+1), (3,n), (3,n+1) (per n = 4 solo (2,4)) | 8/8 |
| B3 (info) | mKdV (deg N = 3): F ∉ V_{2,3} (eccezione "(2,n)" non applicabile, ID-4); Burgers inviscido (σ = 0, fuori ipotesi): [F]∩V_{2,1} = ℂF | — |
| C | **controllo di T1(b) indipendente da ALG-L1**: soluzione a dato di Cauchy generico (serie formale esatta mod p = 1000003), dim I(u)∩V calcolata dalla definizione = dim [F]∩V in 7 casi (Burgers V_{2,2}, V_{2,3}, V_{3,2}; Fisher V_{2,2}, V_{2,3}; KdV, KdV–Burgers V_{2,3}) | 7/7 |
| D | N-shock esatti (Taylor esatta), dim I(u)∩V_{2,2} = 21, 4, 1 per N = 1, 2, 3: coincide con S4-ID (il 3-shock identifica Burgers in senso stretto in V_{2,2}) | 3/3 |
| E | T2(b): R_N da Bell, R_N(u) = 0 in ℂ(X), lineare in y_N con coefficiente −1/2ν, grado N+1, parte di testa (−2ν)^{−N−1}y_0^{N+1} (N = 1, 2, 3, k = (2), (1,3), (2,−1,5)); dim J∩A_{≤N,≤N} = 0, J∩A_{≤N+1,≤N} = 1, J∩A_{≤6 (4),≤N−1} = 0; dim J∩A_{≤N+2,≤N} = binom(N+2,N+1); T2(c) a ordine N+1 (con fix) | 10/10 |
| F | T2(e): polo d'ordine j+1 in X = −1, j ≤ 6 | 1/1 |
| G | T3: 1-solitone risolve KdV e Π_1 ∈ J_u; 2-solitone k = (1,2): J∩A_{≤10,≤1} = 0 (L5), deg Π_2 = 8 (J∩A_{≤7,≤2} = 0, J∩A_{≤8,≤2} = 1); **informativo:** anche per k = (1,3) deg Π_2 = 8 (due valori di k: più evidenza per Q2, non una prova) | 3/3 |
| H | L4: identità D_B^m(y_0²), m ≤ 4; ker ψ su R_{≤3}y ⊕ R_{≤3}y² = {A·F_B : deg A ≤ 1} (dim 3) e, con ν = 0, deg A ≤ 2 (dim 6) | 3/3 |
| I | T4(ii): disuguaglianza per n ≤ 5, c ≤ 8; 1-shock: relazione in A_{≤D* = 3,≤1}; T4(iv): riduzione autosimile esatta | 3/3 |
| J | P7(iii) 1-shock (con fix); P8: y_0y_3 − y_1y_2, y_0y_4 − y_2² ∈ I_PW; forma lineare a coefficienti complessi nulla sulle onde piane ⇒ c = 0 (ID-3); y_1² − k²y_0² ∉ I_PW | 4/4 |

## 10. Rilievi e fix (nessuno FATAL/CRITICAL/MAJOR)
### ID-1 (MINOR · UNCLEAR · LOCAL) — T4/D2: "Cole–Hopf di dati EP"
Vero se "dato EP" significa φ_0 EP (allora φ = e^{νt∂²}φ_0 è EP e u = −2νφ_x/φ è razionale in EP: torre (exp) + (alg)). Se significa u_0 EP, φ_0 = e^{−∫u_0/2ν} è l'esponenziale di un EP e il suo flusso del calore (es. u_0 = sin x: serie di Fourier con coefficienti di Bessel I_n) non è dimostrato appartenere a una torre. **Fix:** "Cole–Hopf con φ_0 esponenziale-polinomiale (cioè u_0 = −2νφ_0′/φ_0, φ_0 EP)". Nessun teorema dipende dall'elenco.
### ID-2 (MINOR · HIDDEN_ASSUMPTION · LOCAL) — P7(iv)
C1(ii) richiede N ∈ A: la riga (iv) vale se **f′ è polinomiale di grado < D** (allora N = νy_2 − f′(y_0)y_1 ∈ N + M₀ con M₀ = span{y_0^jy_1 (j < D), y_2}). **Fix:** aggiungere "e f′ polinomiale di grado < D" all'enunciato (iv).
### ID-3 (MINOR · UNCLEAR · COSMETIC) — P8, parte lineare
"Σc_jκ^j cos(θ + jπ/2) = Re(e^{iθ}Σc_j(iκ)^j)" vale per c_j reali; p ∈ A ha coefficienti complessi. **Fix:** Σc_jκ^j cos(θ + jπ/2) = ½[e^{iθ}Σc_j(iκ)^j + e^{−iθ}Σc_j(−iκ)^j] ≡ 0 per ogni θ ⇒ (indipendenza di e^{±iθ}) Σc_j(iκ)^j ≡ 0 ⇒ c = 0. Conclusione invariata (SymPy §9 J).
### ID-4 (MINOR · OVERSTATED · LOCAL) — portata della precisazione su G★′-NL punto 2 in PROBLEM.md (non della prova di P1)
La precisazione scrive: la forma letterale "è falsa per ogni u con 𝓓 = monomi di grado ≤ d, ordine ≤ k, salvo (d,k) = (2,n)". P1 lo prova **solo** per N = σy_n + N′ (σ costante ≠ 0, N′ d'ordine < n, deg N = 2) — cioè per i banchi di G★′-NL (Burgers, KdV–Burgers, Fisher–KPP, KdV) — e solo per i dizionari **completi** 𝓓_{d,k} (che contengono derivate in t). Due precisazioni servono: (1) per deg N ≥ 3 (es. mKdV) F ∉ V_{2,n} e l'eccezione non è "(2,n)" (S4ID-Q3); (2) nei dizionari **evolutivi** ℂy_t ⊕ A_{≤d,≤k} (quelli della regressione sparsa) [F] ∩ V = ℂF sempre (C1(i)): lì la forma letterale e la forma "modulo [F] ∩ V" coincidono e la forma letterale **non** è falsa. **Fix (testo per il coordinatore):** "… è falsa per ogni soluzione u nei dizionari completi 𝓓_{d,k} (monomi del getto in (t,x) di grado ≤ d e ordine ≤ k) con F ∈ span 𝓓_{d,k}, salvo (d,k) = (2,n), per N = σy_n + N′ con deg N = 2 (tutti i banchi) [S4ID-P1]; nei dizionari evolutivi ℂy_t ⊕ A_{≤d,≤k} le due forme coincidono [S4ID-C1]. La forma corretta in generale è modulo [F] ∩ V: I(u) ∩ V = [F] ∩ V ⟺ J_u ∩ ψ(V) = 0 [S4ID-T1]."
### ID-5 (MINOR · OVERSTATED · LOCAL) — T4, nome "dicotomia"
T4(i) è la direzione facile di ALG-T1(c) estesa alle torri (stesso rilievo P3a-1 di S-CHECK-9 su ALG-P3); il contenuto proprio è in (ii) (soglia esplicita) e (iii) (esistenza). Il §0 del package lo dice già ("implicazione di chiusura + soglia + esistenza, non una caratterizzazione"), ma il titolo del claim resta "Dicotomia, forma non tautologica". **Fix:** titolo "Chiusura, soglia esplicita ed esistenza (non una dicotomia in senso stretto)"; in LEDGER, enunciato su una riga: "forma chiusa a torre ⇒ J_u ≠ 0 (ordine ≤ trdeg); soglia D* su M1; esistono soluzioni identificanti".
### INFO (facoltativi)
- INFO-1 (L4): dire esplicitamente che la componente di grado m+2 di D_N^m(y_0²) è D_B^m(y_0²) senza bisogno che D_ν e D_B commutino (parole non commutative).
- INFO-2 (T4(ii)): n indica sia il numero di variabili presenti sia l'ordine del getto; scriverlo.
- INFO-3 (T2(d)): il ramo "K = N" ha senso per N ≥ 2 (K ≥ 2); per N = 1 il dizionario evolutivo ha K ≥ 2 > N e si applica "K ≥ N+1".
- INFO-4 (T2(e)): la prova del polo d'ordine j+1 si chiude in una riga: D(f/(1+X)^{j+1}) = kX[f′(1+X) − (j+1)f]/(1+X)^{j+2}, che in X = −1 vale k(j+1)f(−1) ≠ 0 (induzione).

## 11. Risposte ai 7 punti delicati della CHECK_REQUEST
1. **T1(a), u solo C^∞:** corretto. G − ψ(G) ∈ [F] è un'identità in ℂ{y} (ALG-L1); [F] ⊆ I(u) usa solo che ev_u intrecci ∂_t, ∂_x (Schwarz, u ∈ C^∞). Nessuna analiticità, nessuna ipotesi su Ω (né limitatezza né connessione).
2. **P1(c):** λ = na + b ≥ n+1 e iniettiva su Θ_+ (divisione euclidea perché b ≤ n − a < n); indipendenza di {1, y_0..y_n, N, ψ(θy)} corretta (N_2 ≠ 0 per N; termine dominante lineare σ^ay_λ per i ψ(θy)); il Passo 2 usa davvero N_2 ≠ 0 (gradi 4 e 3). Corretto.
3. **T2:** (I) corretto ((NR) ⇒ esponenti distinti ⇒ C3-L3(b)); (a) Vandermonde con det = Πk_i·Π(k_l − k_i) e triangolarità di Bell corretti; (b) divisione per un polinomio di grado 1 in y_N con coefficiente costante: corretta e dà anche l'irriducibilità.
4. **T3(b):** "primo di altezza 1 in un UFD ⇒ principale" corretto; altezza = (N+1) − trdeg(ℂ[y]/P) = 1 con trdeg = N da (a) e da ℂ(X).
5. **L4:** identità D_B^m(y_0²) corretta (SymPy m ≤ 4) e q(D)(y_0^E) ≠ 0 per peso corretto; vedi INFO-1.
6. **T4(ii):** deg P_j ≤ a + jb e conteggio binomiale corretti (SymPy n ≤ 5, c ≤ 8); vedi INFO-2.
7. **T4(iii):** passaggio t → 0⁺ corretto: φ ∈ C^∞([0,∞) × ℝ) per il nucleo del calore su dati limitati uniformemente continui con tutte le derivate, φ ≥ inf φ_0 > 0.

## 12. Confronto con il kill-argument di S4-ID (§8 del package, letto dopo)
Concordo con l'elenco "verificato senza errori" del revisore avversariale (L2, P1(c), L5, T2(a)–(c), T3(a)–(b), L4, P5(i), T4(ii)) e aggiungo come verificati da me: T1 (con ALG-L1 nei punti usati), C1, C2, T2(d)(e-grado 1), P5(ii)(iii), P6 (riduzione), P7, T4(i)(iii)(iv-riduzione), logica di P8. Il WARN del kill-argument riguarda la portata (K1, deg Π_N, INT-Q1) e non la validità: lo confermo. I miei rilievi nuovi rispetto al kill-argument: ID-1, ID-2, ID-3, ID-4 (portata della precisazione in PROBLEM.md: dizionari evolutivi e deg N ≥ 3), ID-5 (coerenza con P3a-1 di S-CHECK-9).

## 13. Riga LEDGER proposta (sintesi; tabella completa in inbox/central.md)
T1 DIMOSTRATO · C1(i) CON-FONTE (anticipato) / (ii) DIMOSTRATO · L2, C2 DIMOSTRATO · P1 DIMOSTRATO (fix ID-4 sulla precisazione in PROBLEM.md) · L5 DIMOSTRATO · T2(a)–(d), (e) grado ≤ 1 DIMOSTRATO; K1 CONGETTURA · T3(a)(b) DIMOSTRATO, (c) V-ex, (d) come INT-T1(B) · L4, P5 DIMOSTRATO · P6 riduzione DIMOSTRATA · P7 DIMOSTRATO (fix ID-2) · T4(i)(ii) DIMOSTRATO, (iii) DIMOSTRATO mod CON-FONTE, (iv) riduzione DIMOSTRATA + CON-FONTE (fix ID-1, ID-5) · P8 CONDIZIONALE a (H-as) (fix ID-3) · INT-Q1 APERTO.
