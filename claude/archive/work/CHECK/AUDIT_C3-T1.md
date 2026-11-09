# AUDIT C3-T1 (+ C3-L2, C3-L3, Fatto (F), C3-T6): identificabilità su Ω ⊂ ℝ² connesso
Revisore: S-CHECK-2A (2ª tornata, parte A) · 25/10/2026
Fonte esaminata: SOLO enunciati, ipotesi e prove inviati da S-C3 in `inbox/S-CHECK.md` (richiesta + addendum C3-T6). `work/C3/PROOF_PACKAGE.md` **non è stato letto**, né per intero né per riferimenti puntuali.
Skill caricate (lettura dei SKILL.md, nessuno script _vendor eseguito): skills-local/session-protocol (per prima), skills-local/claim-lifecycle, proof-checker (il reviewer sono io: Phase 0.5 enunciati canonici e micro-claim, Phase 1 checklist A–H, Phase 1.5 red team, severità a due assi, acceptance gate; niente Codex/LaTeX), scientific-critical-thinking (separare ciò che è dimostrato da ciò che viene affermato sull'uso), sympy.
SymPy: `work/CHECK/sympy/audit_c3_2a.py` → `audit_c3_2a.out`, **ESITO GLOBALE: OK** (26 controlli; 3 marcati [STRUTTURALE] perché "w ∉ EP" richiede infiniti modi e non si verifica su somme troncate). Controlli della 1ª parte già eseguiti: `audit_round2.py/.out` §C3-T1 (6/6 OK).

## 0. Verdetti
| claim | verdetto | stato proposto |
|---|---|---|
| C3-L2 | **PASS-con-fix(L2-1)** | DIMOSTRATO |
| C3-L3 (a)–(e) | **PASS-con-fix(L3-1, L3-2, L3-3)** | DIMOSTRATO |
| Fatto (F) | **PASS-con-fix(F-1)** | DIMOSTRATO (fa parte della prova di C3-T1) |
| C3-T1 (a)–(e) | **PASS-con-fix(F-1, T1-1)** | DIMOSTRATO |
| C3-T6 (i)–(ii) | **PASS-con-fix(T6-1)** | DIMOSTRATO |

Nessun FATAL, nessun CRITICAL, nessun MAJOR. Tutti i rilievi sono MINOR e sono chiusi qui (testo dei fix in §4). Avvertenza di portata, che non è un difetto di prova: §6.

## 1. Enunciati canonici (Phase 0.5)
R = ℂ[τ,ξ] (UFD, noetheriano), y = (t,x), Q(∂) = Q(∂_t,∂_x). Ω ⊂ ℝ² aperto, **connesso**, non vuoto. Ann(w) := {Q ∈ R : Q(∂)w = 0 in D'(Ω)}, ideale. EP(Ω) := restrizioni a Ω delle somme finite Σ q_k(y)e^{⟨z_k,y⟩} (q_k ∈ ℂ[t,x], z_k ∈ ℂ²); "w ∈ EP" per w ∈ D'(Ω) significa che w coincide come distribuzione con un tale elemento. gcd di un ideale: definito a meno di unità (costante non nulla).
- **L2.** ∀ I ⊆ R ideale, I ≠ 0, posto G := gcd(I): ∃! ideale J con I = G·J; gcd(J) = 1; |V(J)| < ∞; ∃N ≥ 1 con I(V(J))^N ⊆ J; V(J) = ∅ ⟺ J = R.
- **L3.** ∀ w ∈ D'(Ω): (a) ∀Q, q, z: Q(∂)(q e^{⟨z,·⟩}) = (Q(z+∂)q)e^{⟨z,·⟩}; (b) ∀ U ⊆ ℝ² aperto non vuoto, ∀ z_k distinti: Σq_ke^{⟨z_k,·⟩}|_U = 0 ⇒ ∀k q_k = 0; (c) w = Σq_ke^{⟨z_k,·⟩} con q_k ≠ 0, z_k distinti ⇒ dim_ℂ R·w < ∞ e V(Ann w) = {z_k}; (d) dim R·w < ∞ ⇒ w ∈ EP(Ω); (e) w ∈ EP ⟺ dim R·w < ∞ ⟺ |V(Ann w)| < ∞.
- **(F).** ∀ P_i ∈ R irriducibile: |V(P_i)| = ∞; quindi ∀w con |V(Ann w)| < ∞ ∃h ∈ Ann(w) con P_i ∤ h.
- **T1.** ∀ Ω connesso, ∀ u ∈ D'(Ω), ∀ P ∈ R non costante con P(∂)u = 0, P = c∏_{i=1}^r P_i^{e_i}: (a)–(e) come nella richiesta (w_i = (P/P_i)(∂)u, w_i' = (P/P_i^{e_i})(∂)u).
- **T6.** ∀ Ω connesso, ∀ u con Ann(u) ≠ 0, ∀ P ∈ Ann(u) **non nullo** (vedi T6-1), P = c∏P_i^{e_i}: G_u ∼ ∏P_i^{f_i}, f_i = e_i − max S_i, S_i := {k ∈ {0,…,e_i} : (P/P_i^k)(∂)u ∈ EP}; Ann(u) principale ⟺ G_u(∂)u = 0.

## 2. Dipendenze (DAG, nessun ciclo)
L2 ← Nullstellensatz (ℂ alg. chiuso), noetherianità, finitezza di V(f,g) per f,g coprimi [Fulton]. L3(b) ← analiticità + induzione 1D. L3(c) ← (a),(b). L3(d) ← Hörmander ALPDO I Thm 3.1.4′ (o la derivazione di L3-1), ODE 1D distribuzionali, (b). L3(e) ← (c),(d), Nullstellensatz, teorema cinese. (F) ← nessuno. T1 ← L2, L3(e), (F), Fulton. T6 ← L2, L3(e), (F). Nessun riferimento in avanti.

## 3. Micro-claim ed esiti per passo
### C3-L2
| MC | passo | esito |
|---|---|---|
| L2.1 | (i) J = {f/G : f ∈ I} è ideale; gcd(J) = 1 (un primo comune π darebbe Gπ | I) | OK |
| L2.2 | (ii) f ∈ J∖{0} non costante (se costante J = R); g_a ∈ J con π_a ∤ g_a esiste perché gcd(J) = 1 | OK |
| L2.3 | H_a = {c : π_a | Σc_bg_b} è sottospazio proprio (e_a ∉ H_a); ℂ^s ≠ ∪H_a (unione finita di sottospazi propri su campo infinito) ⇒ g coprimo con f | OK (controllo: g = (ξ+1)+(τ+1) coprimo con τξ) |
| L2.4 | V(J) ⊆ V(f,g) finito [Fulton, cap. 1 §6 Prop. 2] | OK nel contenuto; riferimento da verificare → **L2-1** |
| L2.5 | (iii) I(V(J)) = √J (Nullstellensatz su ℂ), √J f.g. ⇒ (√J)^N ⊆ J; V(J) = ∅ ⇒ √J = R ⇒ J = R | OK (controllo: J = (τ²,ξ) richiede N = 2) |
| L2.6 | caso I = R (u = 0 in T1): G = 1, J = R | OK, coperto |

### C3-L3
| MC | passo | esito |
|---|---|---|
| L3.a | Leibniz / traslazione | OK (controllo simbolico di grado 3) |
| L3.b1 | F analitica su ℝ², nulla su aperto ⇒ F ≡ 0 (ℝ² connesso) | OK |
| L3.b2 | esiste v ∈ ℝ² con ⟨z_k − z_l, v⟩ ≠ 0: per w ∈ ℂ²∖0, {v ∈ ℝ² : ⟨w,v⟩ = 0} è un sottospazio reale proprio (Re w, Im w non entrambi nulli) | OK (il dettaglio "Re/Im" va scritto, banale) |
| L3.b3 | y_0 con ∏q_k(y_0) ≠ 0 (prodotto di polinomi non nulli non si annulla su tutto ℝ²); μ_k distinti, r_k(0) ≠ 0 | OK |
| L3.b4 | induzione: ·e^{−μ_1s}, D^{deg r_1+1}; (D+c)^N con c ≠ 0 conserva il grado (coeff. direttore ·c^N); passo base r_1e^{μ_1s} ≡ 0 ⇒ r_1 = 0 | OK |
| L3.c1 | R·(qe^z) ⊆ ℂ[t,x]_{≤deg q}e^z ⇒ dim < ∞ | OK |
| L3.c2 | ∏𝔪_{z_k}^{deg q_k+1} ⊆ Ann(w) (Q ∈ 𝔪_z^{d+1} ⇒ Q(z+∂) ha ordine di annullamento ≥ d+1 in 0 e uccide i polinomi di grado ≤ d; i fattori commutano) ⇒ V(Ann w) ⊆ {z_k} | OK (controllo: (τ−1)²τ², (τ+ξ)²ξ² ∈ Ann((1+t)e^{t−x}+x); τ+ξ ∉ Ann: Ann non è radicale) |
| L3.c3 | Q ∈ Ann ⇒ (b) ⇒ Q(z_k+∂)q_k = 0 ⇒ (parte omogenea di grado deg q_k) Q(z_k)·top(q_k) = 0 ⇒ Q(z_k) = 0 | OK |
| L3.d0 | W = R·w stabile, finito-dimensionale; p, q polinomi minimi di ∂_t|_W, ∂_x|_W; p(∂_t)w = q(∂_x)w = 0 (w ∈ W) | OK (caso w = 0: p = q = 1, banale) |
| L3.d1 | **Passo 1.** Q_0 = I'×J' rettangolo aperto ⊂ Ω. Induzione su deg p: ṽ := (∂_t−λ)v risolve p̃(∂_t)ṽ = 0 ⇒ ṽ = Σc̃⊗t^le^{μt}; soluzioni particolari tensoriali corrette ((D+μ−λ)r = t^l ha soluzione unica di grado l per μ ≠ λ; t^{l+1}e^{λt}/(l+1) per μ = λ); ∂_t(c⊗g) = c⊗g'; ∂_t(e^{−λt}(v−v_p)) = 0 ⇒ e^{−λt}(v−v_p) = c⊗1 per Hörmander 3.1.4′ (Q_0 è prodotto con fattore-intervallo nella variabile t: ipotesi scaricata). Le molteplicità tornano: l'esponente di λ cresce di 1 esattamente quando la molteplicità di λ in p è quella in p̃ più 1 | OK; riferimento → **L3-1** (MINOR) |
| L3.d2 | **Passo 2.** q(∂_x)v = Σ(q(∂_x)c_{jl})⊗t^le^{λ_jt} = 0; esistenza di ψ_{jl} ∈ C_c^∞(I') biortogonali; testare su φ⊗ψ_{jl} dà (q(∂_x)c_{jl})(φ) = 0 ∀φ ∈ C_c^∞(J') | OK; esistenza di ψ non scritta → **L3-3** (MINOR). Il "pairing parziale" non serve: basta testare sui prodotti φ⊗ψ, che è legittimo |
| L3.d3 | caso 1D: c ∈ D'(J'), q(∂_x)c = 0 ⇒ c ∈ EP(J') (stessa induzione con Hörmander Thm 3.1.4 in una variabile) | OK |
| L3.d4 | **Passo 3.** A = {y : w = E_{Q_0} vicino a y} aperto, ∋ Q_0; chiuso in Ω: per y ∈ Ω ∩ Ā, rettangolo Q_y ∋ y con w = E_{Q_y}; Q_y ∩ A aperto non vuoto ⇒ E_{Q_y} = E_{Q_0} su un aperto ⇒ (b) ⇒ E_{Q_y} ≡ E_{Q_0} su ℝ² ⇒ y ∈ A; Ω connesso ⇒ A = Ω; uguaglianza locale ovunque ⇒ uguaglianza in D'(Ω) | OK; "quindi reale-analitica" superfluo e manca la citazione della proprietà di fascio → **L3-2** (MINOR) |
| L3.e | EP ⇒ dim < ∞ (c); dim < ∞ ⇒ EP (d); V finito ⇒ Ann ⊇ I(F)^N, R/I(F)^N ≅ ⊕R/𝔪_z^N (teorema cinese: le 𝔪_z^N sono a due a due comassimali) di dim finita, R·w ≅ R/Ann(w) quoziente; EP ⇒ V(Ann) = {z_k} finito (c). Caso F = ∅: Ann = R, w = 0 | OK |

### Fatto (F)
| MC | passo | esito |
|---|---|---|
| F.1 | deg_τ P_i ≥ 1: per ξ_0 fuori dagli zeri del coefficiente direttore in τ, P_i(·,ξ_0) ha una radice ⇒ V infinito | OK |
| F.2 | **deg_τ P_i = 0** (P_i ∈ ℂ[ξ], irriducibile ⇒ P_i = α(ξ − ξ_0)): non trattato | **LACUNA** → **F-1** (MINOR, chiusa qui: V(P_i) = ℂ×{ξ_0}) |
| F.3 | "quindi": se Ann(w) ⊆ (P_i), allora V(P_i) ⊆ V(Ann w), che è finito: assurdo. Caso Ann(w) = R: h = 1 | OK (passaggio da scrivere in una riga, incluso in F-1) |

### C3-T1
| MC | passo | esito |
|---|---|---|
| T1.0 | I = Ann(u) ∋ P ≠ 0 ⇒ L2: I = GJ, G | P ⇒ G = c'∏P_i^{f_i}, 0 ≤ f_i ≤ e_i | OK |
| T1.e | G ∼ P ⇒ I = PJ ⊆ (P) ⊆ I. Il viceversa (I = (P) ⇒ gcd(I) ∼ P) non è scritto | OK; **T1-1** (MINOR, banale) |
| T1.a⇐ | I ≠ (P) ⇒ (e) G ≁ P ⇒ ∃i: f_i < e_i ⇒ G | P/P_i = GH; h ∈ 𝔫^N ⊆ J ⇒ Hh ∈ J ⇒ h·P/P_i ∈ I ⇒ 𝔫^N ⊆ Ann(w_i) ⇒ V(Ann w_i) ⊆ V(J) finito ⇒ w_i ∈ EP (L3(e)). Caso J = R: P/P_i ∈ I, w_i = 0 | OK (usa Ann(w_i) = {h : hP/P_i ∈ I}, corretto perché gli operatori commutano) |
| T1.a⇒ | w_i ∈ EP ⇒ V(Ann w_i) finito ⇒ (F) h con P_i ∤ h ⇒ Q = hP/P_i ∈ I; Q = PA ⇒ h = P_iA (cancellazione in un dominio) ⇒ assurdo | OK; usa (F) anche per P_i con deg_τ = 0 (controllo: P = ξ(τ−ξ²), u = e^t + calore, w_ξ = e^t, testimone (τ−1)(τ−ξ²)) |
| T1.b1 | V(I) = V(G) ∪ V(J) ⊆ V(P) | OK |
| T1.b2 | f_i ≥ 1 ⇒ V(P_i) ⊆ V(G) ⊆ V(I) | OK |
| T1.b3 | **f_i = 0** ⇒ V(P_i) ∩ V(I) ⊆ ∪_{j≠i, f_j≥1}(V(P_i)∩V(P_j)) ∪ V(J), finito (P_i, P_j irriducibili non associati ⇒ coprimi ⇒ Fulton; V(J) finito per L2) ⇒ poiché V(P_i) è infinito (F, **inclusa la parte F-1**) V(P_i) ⊄ V(I). Anche il caso G costante (V(I) = V(J) finito) e il caso J = R sono coperti | OK (controllo: I = (τ−ξ²)(τ,ξ²+1), P = τ(τ−ξ²): |V(τ)∩V(I)| = 3) |
| T1.b4 | V(I) = V(P) ⟺ ∀i f_i ≥ 1 (⇐: V(P) = ∪V(P_i) ⊆ V(G) ⊆ V(I) ⊆ V(P)) | OK |
| T1.b5 | f_i = 0 ⇒ G | P/P_i^{e_i} ⇒ (come a⇐) w_i' ∈ EP | OK |
| T1.b6 | w_i' ∈ EP ⇒ h, P_i ∤ h, hP/P_i^{e_i} ∈ I ⇒ G | hP/P_i^{e_i}; f_i ≥ 1 ⇒ P_i | h oppure P_i | P/P_i^{e_i} (P_i primo), entrambi falsi ⇒ f_i = 0 | OK |
| T1.c | e_i = 1 ⇒ w_i = w_i' | OK (riproduce R4-T5[alg]) |
| T1.d | P monico in τ di grado m: divisione unica Q = AP + Σ_{j<m}b_j(ξ)τ^j; Q ∈ I ⟺ resto ∈ I; Q ∈ (P) ⟺ resto = 0; ogni B = Σ_{j<m}b_jτ^j è il resto di sé stesso | OK (controllo: onda, u = g(x+t), b = (−ξ,1); concorda con (a)). Coincide con II-C1 di S-II: due prove indipendenti concordanti |

### C3-T6
| MC | passo | esito |
|---|---|---|
| T6.0 | P ∈ Ann(u) deve essere ≠ 0 per avere P = c∏P_i^{e_i}; G_u definito a meno di costante | **T6-1** (MINOR, HIDDEN_ASSUMPTION/UNCLEAR) |
| T6.1 | k = 0 ∈ S_i sempre (P(∂)u = 0 ∈ EP), quindi max S_i esiste | OK (non scritto; banale) |
| T6.2 | 1 ≤ k ≤ e_i, (⇒): f_i ≤ e_i−k e f_j ≤ e_j ⇒ G_u | P/P_i^k = G_uH ⇒ 𝔫^N ⊆ Ann((P/P_i^k)u) ⇒ EP | OK |
| T6.3 | (⇐): EP ⇒ (F) h con P_i ∤ h ⇒ hP/P_i^k ∈ Ann ⇒ G_u | hP/P_i^k ⇒ f_i = v_{P_i}(G_u) ≤ v_{P_i}(h) + e_i − k = e_i − k | OK |
| T6.4 | **Monotonia in k / formula.** Dall'equivalenza T6.2–T6.3 (valida anche per k = 0): S_i = {k ∈ {0..e_i} : k ≤ e_i − f_i} = {0,…,e_i − f_i}, un segmento iniziale ⇒ max S_i = e_i − f_i. La monotonia è dunque una **conseguenza** dell'equivalenza, non un'ipotesi aggiuntiva; vale anche direttamente: (P/P_i^{k−1})u = P_i(∂)[(P/P_i^k)u] ed EP è stabile per derivazione (L3(a)) | OK (controllo: (∂_t−∂_x²) di un EP resta nello span degli stessi esponenziali) |
| T6.5 | (ii) G_u ∈ Ann ⇒ (G_u) ⊆ G_uJ ⊆ (G_u); Ann = (Q) ⇒ Q ∼ gcd(Ann) = G_u ⇒ G_u(∂)u = 0 | OK (controllo: u = calore + cos x, G_u = τ−ξ², G_u(∂)u = cos x ≠ 0 ⇒ non principale) |
| T6.6 | coerenza con T1(a): G_u ∼ P ⟺ ∀i f_i = e_i ⟺ ∀i max S_i = 0 ⟺ ∀i w_i ∉ EP | OK |

## 4. Rilievi e fix (Phase 2, proposti; non applicati ai file di S-C3)
- **L2-1 · REFERENCE_MISMATCH (possibile) · UNCLEAR/COSMETIC · MINOR · ADD_REFERENCE + ADD_DERIVATION.** "Fulton, cap. 1 §6 Prop. 2": nella numerazione che conosco il fatto "F, G senza fattori comuni ⇒ V(F,G) finito" è la **Proposizione 1** di §1.6; da verificare sull'edizione citata. Il passo non dipende dal riferimento, perché vale questa derivazione autosufficiente. f, g coprimi in ℂ[ξ][τ]. Per il lemma di Gauss sono coprimi anche in ℂ(ξ)[τ] (oppure uno dei due sta in ℂ[ξ]∖{0}). Quindi esistono a, b con af + bg = r(ξ) ≠ 0, e le ascisse ξ dei punti comuni sono radici di r. Scambiando i ruoli di τ e ξ, anche le τ sono in numero finito. Dunque V(f,g) è contenuto in una griglia finita (controllo: Res_τ, Res_ξ ≠ 0).
- **L3-1 · REFERENCE_MISMATCH (verifica puntuale) · UNCLEAR/COSMETIC · MINOR · ADD_REFERENCE + ADD_DERIVATION.** L'uso di Hörmander ALPDO I Thm 3.1.4′ è corretto nella sostanza: v ∈ D'(X'×I) con I intervallo aperto e ∂_tv = 0 implica v = v_0⊗1. L'ipotesi "intervallo nella variabile derivata" è scaricata dal rettangolo Q_0. Conviene comunque riportare l'enunciato esatto con la pagina. Derivazione autosufficiente: si fissa χ ∈ C_c^∞(I') con ∫χ = 1. Per φ ∈ C_c^∞(J'×I') si pone Φ(x) := ∫φ(x,t)dt e ψ(x,t) := ∫_{−∞}^t(φ(x,s) − χ(s)Φ(x))ds. ψ ha supporto compatto in J'×I' perché I' è un intervallo, e vale φ = χ⊗Φ + ∂_tψ. Quindi v(φ) = v(χ⊗Φ) =: v_0(Φ). **Red team (necessità del rettangolo):** su un Ω a "U" (barra (0,3)_t×(0,1)_x più bracci (0,1)×(0,3) e (2,3)×(0,3)), v := φ(x)·1_{t>2} con φ liscia, φ = 0 per x < 1 e φ = 1 per x > 2, è liscia su Ω, con ∂_tv = 0, e non è della forma c(x)⊗1. Per questo il passo 1 va fatto su rettangoli e serve il passo 3: la prova lo fa. Nessun controesempio a L3(d), perché un tale v ha dim R·v = ∞.
- **L3-2 · UNPROVEN_SUBCLAIM · UNCLEAR/COSMETIC · MINOR · ADD_DERIVATION.** Nel passo 3 "w è localmente EP, quindi reale-analitica" non serve. Ciò che si usa davvero sono (i) L3(b) applicato a E_{Q_y} − E_{Q_0}, dopo aver raccolto i termini con lo stesso esponente, e (ii) la proprietà di fascio di D' (Hörmander Thm 2.2.1: distribuzioni che coincidono vicino a ogni punto coincidono). Va anche scritto che il passo 1–2 vale per **ogni** rettangolo in Ω con gli stessi p, q (globali): da qui viene l'esistenza di Q_y attorno a ogni y.
- **L3-3 · UNPROVEN_SUBCLAIM · UNCLEAR/COSMETIC · MINOR · ADD_DERIVATION.** Esistenza delle ψ_{jl} biortogonali. Le g_a = t^le^{λ_jt} sono linearmente indipendenti su I' (L3(b) in una variabile). Se T : C_c^∞(I') → ℂ^n, ψ ↦ (∫g_aψ)_a non fosse suriettiva, esisterebbe c ≠ 0 con ∫(Σc_ag_a)ψ = 0 per ogni ψ. Allora Σc_ag_a = 0 su I' (funzione continua nulla come distribuzione): assurdo. Le ψ_{jl} sono le preimmagini dei vettori della base canonica (controllo: Gram pesata non singolare).
- **F-1 · CASE_INCOMPLETE · UNJUSTIFIED · MINOR (chiusa qui) · ADD_DERIVATION.** Caso mancante: se deg_τP_i = 0, P_i è irriducibile in ℂ[ξ], quindi P_i = α(ξ−ξ_0) e V(P_i) = ℂ×{ξ_0}, che è infinito. Il caso non è vacuo, perché fattori in ξ soli compaiono in T1(a),(b),(e) e in T6 (controllo: P = ξ(τ−ξ²)). In T1(d) invece non si pone, perché P è monico in τ. Va scritto anche il "quindi" di (F): se Ann(w) ⊆ (P_i), allora V(P_i) ⊆ V(Ann w), che è finito: assurdo. La classifico MINOR, non CRITICAL, anche se (F) è sul cammino di T1: l'enunciato di (F) è vero come scritto, manca solo la giustificazione di un caso banale.
- **T1-1 · IMPLICATION_REVERSAL (mancata) · UNCLEAR/COSMETIC · MINOR · ADD_DERIVATION.** (e) afferma "G ∼ P ⟺ Ann(u) = (P)" ma la prova dà solo ⇒. Il viceversa: gcd((P)) ∼ P.
- **T6-1 · HIDDEN_ASSUMPTION · UNCLEAR/COSMETIC · MINOR · STRENGTHEN_ASSUMPTION testuale.** "P ∈ Ann(u) qualsiasi" va scritto "P ∈ Ann(u)∖{0}". "G_u = ∏P_i^{f_i}" va scritto "G_u ∼ ∏P_i^{f_i}" (a meno di costante). Conviene anche dire esplicitamente che k = 0 ∈ S_i.

## 5. Red team (Phase 1.5) — esito
Tentativi registrati (script `audit_c3_2a.py`):
1. **L2:** ideale con J ≠ R non radicale (J = (τ²,ξ), N = 2). Il lemma regge e N > 1 è davvero necessario.
2. **L3(c):** w = (1+t)e^{t−x}+x. dim R·w = 4, V(Ann) = {(1,−1),(0,0)}, Ann non radicale (τ+ξ ∉ Ann). Coerente con il lemma.
3. **L3(d), Ω sconnesso:** w = 1_{Ω₁} ha dim R·w = 1 ma non è in EP(Ω). È un controesempio **all'ipotesi tolta**, non al lemma: "Ω connesso" è necessario, ed è presente.
4. **L3(d), passo 1 su dominio non t-convesso** (U, vedi L3-1): ∂_tv = 0 non dà v = c⊗1 globalmente. La prova lo evita lavorando su rettangoli. Nessun controesempio al lemma.
5. **(F) e T1 con fattore ξ** (deg_τ = 0): P = ξ(τ−ξ²), u = e^t + calore. w_ξ = e^t ∈ EP; il testimone (τ−1)(τ−ξ²) ∈ Ann∖(P) è verificato. Il teorema regge una volta chiusa F-1.
6. **T1(b), f_i = 0:** I = (τ−ξ²)(τ,ξ²+1), P = τ(τ−ξ²), con |V(τ)∩V(I)| = 3. È realizzato da u = calore + cos x, e w_τ' = cos x ∈ EP. Regge.
7. **T1(a) vs (b) per P non ridotto:** già nella 1ª parte (audit_round2: P = (τ−ξ²)², calore) le due condizioni differiscono come previsto.
8. **T1(d):** onda. È coerente con (a) e con II-C1.
9. **T6:** P = (τ−ξ²)² con u = t·v + ∂_xv (f = 2, Ann = (P)) e con u = v (f = 1, principale); u = calore + cos x (G_u(∂)u = cos x ≠ 0, non principale). La monotonia è verificata.
Nessun controesempio agli enunciati come scritti (più i fix MINOR). Tre controlli sono [STRUTTURALE]: "∉ EP" per infiniti modi non si verifica simbolicamente, e lo dichiaro.

## 6. Portata (scientific-critical-thinking): cosa è dimostrato e cosa no
- **Dimostrato:** per Ω ⊂ ℝ² connesso (non serve limitato né convesso; H^m non serve) e u ∈ D'(Ω), l'identificabilità Ann(u) = (P) equivale al test "w_i ∉ EP(Ω) per ogni fattore", e la forma geometrica V(Ann u) = V(P) equivale al test su w_i'. Questo risolve in forma algebrico-analitica la parte di G9 lasciata APERTA in AUDIT_R4-T5 (R4-T5[ℝ]): la caratterizzazione non passa per la misura di Ehrenpreis ma per l'appartenenza a EP, che è intrinseca.
- **Non dimostrato (e non affermato dalla prova):** che il test "w ∉ EP" sia decidibile o certificabile da dati finiti. Un jet finito in un punto è sempre il jet di un polinomio (audit_round2, M2), quindi la non appartenenza a EP non si legge su un jet finito. È C3-Q1, già aperto presso S-C3. In LEDGER va scritto "identificabilità ⟺ test EP" e non "identificabilità decidibile".
- Il kill-argument su C3-T1 è già stato fatto da S-C3 (WARN, framing corretto). Questo audit non ha trovato nulla che lo contraddica.

## 7. Acceptance gate
0 FATAL/CRITICAL ✔. Ipotesi esplicite dopo T6-1 ✔. Ogni applicazione (Nullstellensatz su ℂ, noetherianità, Fulton/risultante, Hörmander 3.1.4′ su rettangolo, proprietà di fascio, teorema cinese, cancellazione in dominio) ha le ipotesi scaricate ✔. Controesempi tentati su tutti i lemmi chiave ✔. Nessuna O(·) ✔.
**Stati proposti:** C3-L2, C3-L3, C3-T1, C3-T6: **DIMOSTRATO**, con i fix MINOR da recepire nel testo di S-C3 (L2-1, L3-1, L3-2, L3-3, F-1, T1-1, T6-1).
