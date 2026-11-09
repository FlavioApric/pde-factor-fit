# AUDIT P4 — modulo ciclico, Padé 2D, decidibilità di C3-Q1 (claim di S-P4)
Revisore: S-CHECK-6 (6ª tornata) · iniziato 25/10/2026, ripreso e chiuso 26/10/2026 (ripresa dopo l'arresto delle 18:32: red team e memo d'attacco NON rifatti, riusati da disco).
Fonte esaminata: `work/P4/CHECK_REQUEST.md` (per intero: §A, §B, §C). **Riferimenti puntuali dichiarati:** `work/II/PROOF_PACKAGE.md` §[II-L1] (righe 56–61, per auditare II-L1(b), usato in P4-L6(b) → P4-T6); `work/P4/sympy/p4_checks.py` riga 141 (solo per la normalizzazione di G nel controllo C8); `claims/LEDGER.md` riga 61 e la TABELLA di S-P4 in `inbox/central.md` (solo per confrontare la formulazione proposta con gli enunciati). Nessun'altra parte di work/P4 letta (non §9 "passaggio avversariale in linea").
Fatti importati usati come dati (LEDGER, DIMOSTRATO): Fatto (V), C3-L2, C3-L3, Fatto (F), C3-T1, C3-T3, C3-T6, C3-P1[M2], C12-T1′. Prove scritte non auditate usate da P4 e auditate qui: **C3-T2(a)** (in P4-T2(v)(b)) e **II-L1(b)** (in P4-L6(b)); C3-C2 (in P4-T2(v)(c), P4-T5 Passo 4) riverificata nella sua prova di due righe. Restano come dati non auditati: C3-L1 (solo in P4-T1(iv)), C3-P5(a) (solo in P4-C4(a)), l'assunzione (AC).
Skill caricate (lettura integrale dei SKILL.md, nessuno script _vendor eseguito): skills-local/session-protocol (per prima), skills-local/claim-lifecycle, proof-checker (reviewer = io: Phase 0.5 enunciati canonici e micro-claim, checklist, Phase 1.5 red team, severità a due assi, acceptance gate; niente Codex/LaTeX), kill-argument (Thread 1 e Thread 2 = subagenti Claude freschi senza contesto, al posto di Codex; verdetto calcolato da me con la tabella della skill), scientific-critical-thinking (enunciati dimostrati separati dalle "Letture" e dalle righe LEDGER; stato proporzionato), sympy.
SymPy: `work/CHECK/sympy/audit_p4.py` → `audit_p4.out` **34/34 OK** (eseguito il 25/10 con `.venv -I`; esiti in §5). Kill-argument: `KA_P4_T2_{input,attack,adjudication}.md`, `KA_P4_T5_{input,attack,adjudication}.md` (§6).

## 0. Verdetti
| claim | verdetto | stato proposto |
|---|---|---|
| P4-T1 (i)–(iv) | **PASS-con-fix(T1-1)** | DIMOSTRATO ((iv) condizionato a C3-L1, prova scritta) |
| P4-L1 (a)–(c) (Weyl) | **PASS-con-fix(L1-1)** | DIMOSTRATO (prova completa inclusa; la fonte Dixmier/Coutinho diventa superflua) |
| P4-C1 (a)–(c) | **PASS** | DIMOSTRATO (l'enunciato confutato, forma "End" di RT-R4a in L4, è FALSO) |
| **P4-T2** (i)–(vi) | **PASS-con-fix(T2-1, T2-2, T2-3, T2-4 MAJOR, T2-5)** — tutti i passi richiesti (Q1–Q5) corretti; "V(J) ⊆ σ_p" non circolare; "radicale ⟺ q_k costanti" corretto con ℓ(z_k+∂) | DIMOSTRATO (enunciato come scritto, a una direzione). **La formulazione nel LEDGER (riga 61: "dicotomia identifica ⟺ nessun autovettore", "Â⁻¹ non esiste quasi ovunque") e nella TABELLA di S-P4 ("sintesi spettrale ⟺ u EP ⟺ non identifica") è FALSA** → T2-4 |
| C3-T2(a) (usato in P4-T2(v)(b)) | **PASS** | DIMOSTRATO (audit qui, §2.1) |
| P4-C2 | **PASS** | DIMOSTRATO |
| P4-T3 (i)–(iv) | **PASS-con-fix(T3-1)** | DIMOSTRATO |
| P4-C3 | **PASS** | DIMOSTRATO |
| P4-L2 | **PASS** | DIMOSTRATO |
| **P4-P1** (cammino critico G★′ p. 2) | **PASS** | DIMOSTRATO |
| P4-T4 (i)–(iii) | **PASS**; la sua *Lettura* ("si riduce **esattamente**", "il maggiorante non si può eliminare") **OVERSTATED** → T5-1 MAJOR | DIMOSTRATO (enunciato); Lettura da riformulare |
| **P4-T5** | **PASS-con-fix(T5-1 MAJOR, T5-2 MAJOR, T5-3)** — Passi 1–5 corretti; manca l'esistenza di un u ammissibile con Ann(u) = (P) per P generico (fornita qui, P4-L7 proposto) | DIMOSTRATO (enunciato condizionale come scritto); "indecidibile a scatola nera **per ogni P**" DIMOSTRATO **solo con P4-L7** (fix T5-2) |
| P4-L3 | **PASS-con-fix(L3-1)** | DIMOSTRATO (calcolabilità di B(L) modulo (AC) estesa, L3-1) |
| P4-L4, P4-L5, P4-P2 | **PASS** | DIMOSTRATO |
| P4-L6 (a)–(c) | **PASS** | DIMOSTRATO (dipende da II-L1(b), auditato qui) |
| II-L1(b) | **PASS** | da APERTO-con-prova a **DIMOSTRATO** (audit qui, §2.6) |
| **P4-T6** | **PASS-con-fix(AC-1)** — dipendenza da II-L1(b) chiusa; (AC) resta un'assunzione dichiarata | DIMOSTRATO **modulo (AC)** (CON-FONTE generico da documentare, AC-1) |
| P4-C4 (a)–(c) | **PASS-con-fix(C4-1, C4-2)** | DIMOSTRATO ((a) condizionato a C3-P5(a), prova scritta; (c) è una Lettura che usa P4-T5 + P4-L7) |
| C3-Q1 (riga proposta da S-P4: APERTO → PARZIALE) | sostenuta **con T5-1 e T5-2** | PARZIALE: decidibile nella classe di P4-T6 (modulo AC); indecidibile nel modello a scatola nera M2⁺ senza dato aggiuntivo, per ogni P non costante (P4-T5 + P4-L7); "B è il dato giusto/minimo" NON dimostrato (B è sufficiente, non necessario) |
| Kill-argument A (P4-T2) | **WARN** (`unresolved_major_or_minor`) | nessun punto critico; recepito in T2-3, T2-4, T2-1, T2-2 |
| Kill-argument B (P4-T5) | **WARN** (`unresolved_major_or_minor`) | nessun passo errato; punti non risolti sulla cornice: T5-1, T5-2 |

Rilievi: nessun FATAL, nessun CRITICAL. 3 MAJOR, tutti di portata/formulazione e non di prova: **T2-4** (la riga LEDGER e la TABELLA di S-P4 enunciano un bicondizionale falso che il teorema non afferma), **T5-1** (Lettura di P4-T4/T5: "esattamente" e "non si può eliminare" non dimostrati; B è sufficiente, non minimo), **T5-2** (esistenza di u ammissibile con Ann(u) = (P) per ogni P: necessaria perché "indecidibile a scatola nera" non sia vuoto; prova fornita in §3.1). Il resto MINOR. Acceptance gate (proof-checker): (1) zero FATAL/CRITICAL ✓; (2) ipotesi esplicite e scaricate a ogni uso ✓ con i fix MINOR; (3) nessun O-grande; (4) red team eseguito su tutti i lemmi chiave ✓ (34/34, inclusi i controesempi del kill-argument e del lapsus ℓ(∂)).

## 1. Enunciati canonici (Phase 0.5)
- **P4-T2(ii).** ∀Ω ⊂ ℝ² aperto connesso, ∀u ∈ D′(Ω) con I = Ann(u) ≠ 0, I = G·J (G = gcd I): {z ∈ ℂ² : ∃w ∈ R·u∖0, ∂_tw = τ_zw, ∂_xw = ξ_zw} = V(J); e ogni tale w è c·e^{⟨z,·⟩}.
- **P4-T2(v)(a).** Nelle stesse ipotesi: I principale ⟺ J = R ⟺ V(J) = ∅ ⟺ R·u ∩ EP = 0. **Corollario (una direzione):** Ann(u) = (P) ⇒ σ_p(u) = ∅. Il viceversa è falso (u = e^{x²}, P = τ²: Ann = (τ), σ_p = ∅; SymPy KA-A). Forma corretta: **Ann(u) = (P) ⟺ σ_p(u) = ∅ e G_u ∼ P** (T2-4).
- **P4-T2(v)(b).** u ∈ EP: ρ_u(L) = Σ_z L(z)Π_z ∀L ⟺ I radicale ⟺ u = Σc_ke^{⟨z_k,·⟩}, c_k ∈ ℂ.
- **P4-T2(vi).** ∀τ₀: ∂_t − τ₀ biiettivo su R·u ⟺ τ₀ ∉ π_τV(I). Per I = (P): risolvente = ℂ∖π_τV(P); **finito solo se ogni fattore irriducibile di P dipende da ξ** (P = τ, u = e^{x²}: risolvente ℂ∖{0}; SymPy T2g).
- **P4-T3(iii).** ∀u reale-analitica su Ω connesso, ∀a ∈ ℂ[z₁]∖0, b ∈ ℂ[z₂]∖0: a(z₁)b(z₂)S_u ∈ ℂ[z₁,z₂] ⟺ a(τ), b(ξ) ∈ Ann(u).
- **P4-P1.** Ω connesso e semplicemente connesso, P = c∏P_j^{m_j}, P(∂)u = 0, u = Σu_j con u_j ∈ ker P_j^{m_j} qualsiasi: Ann(u) = (P) ⟺ ∀j Ann(u_j) = (P_j^{m_j}) ⟺ ∀j P_j^{m_j−1}(∂)u_j ∉ EP.
- **P4-T4(iii).** Nel modello M2⁺, ∀B ≥ dim(R·u ∩ EP): Ann(u) = (P) ⟺ Ann(u) ∩ R_{≤N} = (P) ∩ R_{≤N}, N = B + deg P − 1.
- **P4-T5** (come scritto, condizionale). ∀P ∈ K[τ,ξ] non costante, ∀(Ω, p₀, u) ammissibili con **Ann(u) = (P)**, ∀k₀ ∈ ℕ, ∀𝒬 ⊂ K[τ,ξ] finito, ∃v ∈ E_P^K: jet_{k₀}(v) = jet_{k₀}(u), [Q(∂)v = 0 ⟺ Q(∂)u = 0] ∀Q ∈ 𝒬, Ann(v) ⊋ (P). **Lettura "indecidibile per ogni P" = P4-T5 + esistenza di (Ω,p₀,u) ammissibili (P4-L7, fix T5-2).**
- **P4-T6.** (H1)–(H4) + (AC) ⇒ "Ann(u) = (P)", "V(Ann u) = V(P)" decidibili; G_u, Ann(u) ∩ 𝓛, generatori di Ann(u) calcolabili.

## 2. Micro-claim ed esiti per passo
### 2.1 P4-T2 (priorità 1) e C3-T2(a)
| MC | passo | esito |
|---|---|---|
| T2.1 | (i) caratteri di R/I ↔ z ∈ V(I) (Q ↦ Q(z) passa al quoziente ⟺ I ⊆ 𝔪_z); V(GJ) = V(G) ∪ V(J) | OK |
| T2.2 | (ii) forma: 𝔪_z(∂)w = 0, w ≠ 0 ⇒ V(Ann w) ⊆ {z} ⇒ w ∈ EP (C3-L3(e)) ⇒ w = q e^{⟨z,·⟩} (L3(c)) ⇒ ∂_tq = ∂_xq = 0 (L3(a),(b)); generalizzati idem | OK |
| T2.3 | (Q1) σ_p ⊆ V(J): (LG) corretto (τ−τ_z, ξ−ξ_z primi non associati, R fattoriale; G costante banale); Q = GQ′, cancellazione di G nel dominio (GJ = {Gj}); Q′ ∉ J; 𝔪_z ⊆ (J:Q′) ≠ R ⇒ (J:Q′) = 𝔪_z ⊇ J | OK (SymPy T2f) |
| T2.4 | (Q2) V(J) ⊆ σ_p: ∏𝔪_{z′}^N ⊆ I(V(J))^N ⊆ J (C3-L2); J+𝔪_{z′}^N a due a due comassimali, ∩ = ∏ ⊆ J + ∏𝔪^N = J; teorema cinese; M_z ≠ 0 (J+𝔪_z^N ⊆ 𝔪_z); (LS) corretto; v ∉ J ⇒ (vG)(∂)u ≠ 0 (vG ∈ GJ ⟺ v ∈ J); 𝔪_zv ⊆ J ⇒ autovettore | OK (SymPy LS1–LS3 su J = (τ², ξ(ξ−1))). **Non circolarità:** l'isomorfismo R/J ≅ R·G(∂)u usa solo Ann(G(∂)u) = (I:G) = J (R dominio); la prova di (iii) usa di (ii) solo la "forma degli autovettori" (T2.2), provata prima. La mappa delle dipendenze "(iii) ← (ii)" è imprecisa → T2-5 (MINOR) |
| T2.5 | (Q3) (iii) ⊇: Ann(G(∂)u) = J, V(J) finito ⇒ EP, EP stabile per derivazione. ⊆: w = Q(∂)u ∈ EP ⇒ V(Ann w) finito (w = 0 banale) ⇒ per ogni primo P_i | G, h ∈ Ann(w) con P_i ∤ h (Fatto (F)) ⇒ P_i^{f_i} | hQ ⇒ P_i^{f_i} | Q ⇒ G | Q (R fattoriale) | OK |
| T2.6 | (iii) somma degli autospazi generalizzati: W ∩ EP di dimensione finita, stabile, A_u, B_u commutanti ⇒ decomposizione congiunta; viceversa ogni generalizzato è EP (T2.2) | OK |
| T2.7 | (iv) ·G ben definita, iniettiva, immagine (G)/I; R/(G) senza autovettori (LG); caratteri V(G) | OK (SymPy C2a, C2b per il caso G = τ) |
| T2.8 | (v)(a) J = R ⟺ V(J) = ∅ (C3-L2(iii)) ⟺ σ_p = ∅; J = R ⟺ I principale (I = (Q) ⇒ G ∼ Q ⇒ GJ = (G) ⇒ J = R); W ∩ EP ≅ R/J | OK. La tesi è **a una direzione** per "identifica": controesempio al viceversa u = e^{x²}, P = τ² (SymPy KA-A). L'enunciato non afferma il viceversa; la riga LEDGER 61 e la TABELLA di S-P4 sì → **T2-4** |
| T2.9 | (v)(b) W generato da generalizzati ⇒ u ∈ W ∩ EP; u ∈ EP ⇒ V(I) finito ⇒ G ∼ 1 (Fatto (F)); G ∼ 1 ⇒ V(I) = V(J) finito ⇒ EP | OK |
| T2.10 | (v)(b) idempotenti del teorema cinese, Π_z polinomi in A_u, B_u, W_z = autospazio generalizzato (un elemento di 𝔪_z^N∖𝔪_{z′} è invertibile su W_{z′}); Taylor finita | OK (nota: N_z^α = 0 già per \|α\| ≥ N; "2N" è una sovrastima innocua) |
| T2.11 | (Q4) diagonalità ⟺ N_z = 0 ∀z ⟺ I + 𝔪_z^N = 𝔪_z ∀z ⟺ I = ∩𝔪_z (radicale) | OK |
| T2.12 | C3-T2(a): Q(∂)Σq_ke^{⟨z_k,·⟩} = Σ(Q(z_k+∂)q_k)e^{⟨z_k,·⟩} (L3(a)), nullo ⟺ ogni coefficiente nullo (L3(b), z_k distinti, Ω connesso) | OK → **C3-T2(a) DIMOSTRATO** (SymPy T2b, 8 polinomi). Conviene inlinare le due righe in P4-T2 → T2-2 |
| T2.13 | q_k costanti ⇒ I_k = 𝔪_{z_k} ⇒ I = ∩𝔪_{z_k} radicale | OK (SymPy T2e) |
| T2.14 | q_k non costante ⇒ I non radicale: **la prova scrive ℓ(∂)q_k dove serve ℓ(z_k+∂)q_k** (due occorrenze). Letta alla lettera la scelta di ℓ è sbagliata: per q₁ = x, z₁ = (1,1), ℓ = τ−1 soddisfa ℓ(∂)q₁ = −x ≠ 0 ma ℓ(z₁+∂)q₁ = ∂_tx = 0 e Q = (τ−1)(τ−4) ∈ I (SymPy T2d). Con ℓ(z_k+∂) ∈ {∂_t, ∂_x}: ℓ(z_k+∂)q_k ≠ 0, ∏_{j≠k}ℓ_j(z_k+∂) = c + (abbassa il grado), c ≠ 0, invertibile sui polinomi; Q ∈ ∩𝔪_{z_j} = √I, Q ∉ I | OK con il fix **T2-3** (MINOR: lapsus di notazione, argomento corretto; SymPy T2c con ℓ = ξ−1, ℓ₂ = τ−4) |
| T2.15 | (v)(c) C3-C2: u ∈ EP ⇒ V(Ann u) finito, V(P) infinito (Fatto (F)) ⇒ Ann(u) ≠ (P) | OK (prova di C3-C2 riverificata) |
| T2.16 | (Q5) (vi) biiettività ⟺ τ−τ₀ invertibile in R/I (suriettiva ⇒ 1̄ = (τ−τ₀)ḡ) ⟺ (I, τ−τ₀) = R ⟺ V(I) ∩ {τ = τ₀} = ∅ (Nullstellensatz debole); iniettività su R/(P) ⟺ coprimalità; π_τV(P_i) cofinito se P_i dipende da ξ (coefficiente direttore in ξ); calore ℂ, τξ−1 ℂ∖{0}, ∂_x = ∂_t^{−1} | OK. La qualifica "se ogni fattore dipende da ξ" è nell'enunciato ma **non nella riga LEDGER** ("Â⁻¹ non esiste quasi ovunque per u identificante"): falsa per P = τ, u = e^{x²} (risolvente ℂ∖{0}, SymPy T2g) → parte di **T2-4** |
| T2.17 | Casi limite: "u = 0 è escluso (I = R ≠ 0 è ammesso …)" autocontraddittorio (I = R ⟺ u = 0) | **T2-1** (MINOR): "u = 0 (⟺ I = R) è ammesso ed è banale" |

### 2.2 P4-C2, P4-T1, P4-L1, P4-C1
| MC | passo | esito |
|---|---|---|
| C2.1 | Q = Q₀(ξ) + τQ₁(ξ) + τ²Q₂: Q(∂)u = Q₀(0)t + Q₀(∂_x)f + Q₁(0); Q₀ ≠ 0 ⇒ ξQ₀(ξ) annulla f ⇒ f EP (1D): assurdo; quindi Q ∈ (τ², τξ) | OK (SymPy C2a: dim Ann ∩ R_{≤3} = 5) |
| C2.2 | G = τ, J = 𝔪_0, W ∩ EP = R·∂_tu = ℂ·1, σ_p = {0}; non spezzamento: u = c + w′ ⇒ ∂_tw′ = 1 ∈ W′ ∩ ℂ·1 = 0 | OK (SymPy C2b) |
| T1.1 | (i) ker ρ_u = Ann(u) (commutatività: Q(∂)Q′(∂)u = Q′(∂)Q(∂)u); (ii) rango–nullità; (iii) classi affini; (iv) = C3-L1 | OK. (iv) poggia su C3-L1 (prova scritta, non auditata): dichiararlo nello stato → **T1-1** (MINOR) |
| L1.1 | (a) Q x^{j₀} = Σ_i c_{ij₀}j₀!x^i ≠ 0 (i termini j > j₀ annullano x^{j₀}) | OK |
| L1.2 | (b) [∂, x^i∂^j] = ix^{i−1}∂^j, [x^i∂^j, x] = jx^i∂^{j−1}; j* applicazioni di [·,x] danno j*!Σ_ic_{ij*}x^i; i* applicazioni di [∂,·] danno i*!j*!c_{i*j*} ≠ 0 | OK (SymPy L1a, i,j ≤ 3) |
| L1.3 | (c) A_2: "elemento di grado massimo in (∂_t,∂_x) e poi in (t,x)" non specifica l'ordine sui multi-indici | **L1-1** (MINOR): prendere (a,b) massimo in ordine lessicografico tra i multi-indici di (∂_t,∂_x) presenti, applicare ad_t^a ad_x^b (con [·,t], [·,x]), poi analogamente in (t,x) con ad_{∂_t}, ad_{∂_x}; i termini con multi-indice lessicograficamente minore si annullano o restano di ordine inferiore e vengono eliminati allo stesso modo |
| C1.1 | (a) ker ρ_u ideale bilatero (sinistro: (C′Q)(Cu) = C′(Q(Cu)); destro: (QC′)(Cu) = Q((C′C)u)), 1 ∉ ker (u ≠ 0) ⇒ ker = 0 per L1(b) | OK |
| C1.2 | (b) ℂ[x]eˣ = A_1·eˣ; (c₀ + c₁∂)(xeˣ) = (c₀x + c₁(1+x))eˣ ⇒ c₁ = 0, c₀ + c₁ = 0 | OK (SymPy C1b); (c) diretta |

### 2.3 P4-T3, P4-C3
| MC | passo | esito |
|---|---|---|
| T3.1 | (i) (Q∘S_u)_{ab} = ∂^{(a,b)}(Q(∂)u)(p₀); analiticità + Ω connesso ⇒ Ann(u) = Ann_R(S_u), W ≅ R∘S_u | OK |
| T3.2 | (ii) W ⊆ EP di dimensione finita; serie di Neumann; ev_{p₀} lineare (continuo in dimensione finita); (z₁−A)^{−1} = M(z₁,A)/μ_A(z₁) | OK (SymPy T3a: S_u riprodotta per a,b ≤ 3) |
| T3.3 | (iii)⇐: per i ≤ −1 la somma in k è completa; [T]_{ij} = Σ_lb_l∂_x^{l−j−1}∂_t^{−i−1}(a(∂_t)u)(p₀) = 0; simmetria; restano monomi con i,j ≥ 0, finiti | OK |
| T3.4 | (Q6) (iii)⇒: (1) i,j ≤ −1 ⇒ b(∂_x)a(∂_t)u = 0; (2) i ≤ −1, 0 ≤ j ≤ n−1 ⇒ Σ_{l>j}b_l∂_x^{l−j−1}∂_t^{i′}v(p₀) = 0, induzione discendente da j = n−1 (b_n ≠ 0) ⇒ ∂_x^c∂_t^{i′}v(p₀) = 0, c < n; (3) h_c analitiche su I₀ con tutte le derivate nulle in t₀ ⇒ h_c ≡ 0 su I₀; per ogni t ∈ I₀, v(t,·) risolve b(d/dx)y = 0 con dati nulli in x₀ ⇒ v = 0 su Q₀ ⇒ su Ω | OK (casi n = 0, deg a = 0 coperti) (SymPy T3b, T3c) |
| T3.5 | conseguenze: V(Ann u) ⊆ V(a(τ)) ∩ V(b(ξ)) finito ⇒ EP; μ_t = μ_A via P4-T1(i) | OK |
| T3.6 | (iv) "per u EP basta il jet di ordine 2d−1": generatori di grado ≤ d (C3-T3(ii)) + C3-T3(i) con d′ = d ⇒ derivate di ordine ≤ d + d − 1 | OK, ma richiede di conoscere d (o un maggiorante d′, ordine d + d′ − 1) → **T3-1** (MINOR) |
| C3.1 | (a) s_{ab} = δ_{ab}, S_u = 1/(z₁z₂−1); (b) ∂_t∂_x(tx)^n/(n!)² = (tx)^{n−1}/((n−1)!)²; (c) Σ_ka_ks_{k+i,b} = a_{b−i} ⇒ a = 0; (d) τξ−1 irriducibile, u ∉ EP ⇒ Ann = (τξ−1) (C3-T1(a), r = 1) | OK (SymPy C3a–C3c) |

### 2.4 P4-L2, P4-P1 (cammino critico G★′ punto 2)
| MC | passo | esito |
|---|---|---|
| L2.1 | Ann(v) ⊇ (Q) + B·K (K = Ann(B(∂)v)); V((Q)+BK) ⊆ (V(Q)∩V(B)) ∪ V(K), entrambi finiti (Fatto (V); C3-L3(c)); B(∂)v = 0 ⇒ K = R | OK |
| P1.1 | (a) (P/P_j)(∂)u_k = 0 per k ≠ j (P_k^{m_k} \| P/P_j); w_j = c·B_j(∂)v_j, v_j = P_j^{m_j−1}(∂)u_j, P_j(∂)v_j = 0; P4-L2 con (P_j, B_j) coprimi; C3-T1(a) per u_j e P_j^{m_j} | OK |
| P1.2 | (b) w_j′ = c·B_j(∂)u_j, P4-L2 con (P_j^{m_j}, B_j); (c) le condizioni si riscrivono su u | OK (SymPy S-P4 C5a–C5b; non rifatto) |
| P1.3 | uso di C12-T1′: P = ∏Q_j con Q_j = P_j^{m_j} primari coprimi, Ω semplicemente connesso, solo per l'esistenza della scomposizione | OK; la *Lettura* ("su Ω non semplicemente connesso C3-T1 si applica comunque a u") è corretta |

### 2.5 P4-T4, P4-T5 (priorità 4)
| MC | passo | esito |
|---|---|---|
| T4.1 | (i) A_k nucleo di una matrice in K; catena stabile; A_∞ = Ann ∩ 𝓛 (analiticità); l'algoritmo si ferma solo se A_k ⊆ Ann (zero-test sulla base) e al più a k* | OK |
| T4.2 | (ii) semi-decisione: termina a n = max(deg Q, deg P) | OK |
| T4.3 | (Q7) (iii) w_i ∈ W ∩ EP ⇒ d_i ≤ B; w_i = 0 ⇒ h = 1; altrimenti generatore h con P_i ∤ h, deg h ≤ d_i (C3-T3(ii) + Fatto (F)); Q = hP/P_i ∈ Ann∖(P), deg Q ≤ B + deg P − deg P_i ≤ N | OK |
| T4.4 | test EP con dim R·w ≤ B ⇒ eliminanti di grado ≤ B; viceversa eliminanti ⇒ EP; G_u via C3-T6, V(Ann u) via C3-T1(b) | OK |
| T4.5 | *Lettura* "C3-Q1 si riduce **esattamente** a … un maggiorante di dim R/J_u; il maggiorante non si può eliminare" | **OVERSTATED**: è provata solo la sufficienza di B; un decisore non produce B sulle istanze "no"; basta un dato più debole (un maggiorante D del grado minimo di un testimone in Ann(u)∖(P): Ann ∩ R_{≤max(D,deg P)} vs (P) ∩ R_{≤…}); P4-T5 mostra solo che *senza alcun dato aggiuntivo* il problema non è decidibile → **T5-1** (MAJOR; kill-argument B, P_1–P_3) |
| T5.1 | Passo 1: infiniti punti di V(P_i) in K² (K algebricamente chiuso); punti singolari finiti; jet di e_{i,z} in K (normalizzazione y − p₀, p₀ ∈ K²) | OK |
| T5.2 | (Q8) Passo 2: g_{i,z,j} ∈ ker P (P_i(z+∂) abbassa il grado di 1 in s_z); "⊇" banale; "⊆": z ∈ K² dal Passo 1 evitando insiemi finiti; ∂^βg_{i,z,e_i−1} ∈ span_K{g_{i,z,j}, j < e_i} (per questo servono **tutti** i j < e_i); Q(∂)g ∈ EP con serie di Taylor nulla ⇒ 0; dualità in dimensione finita ⇒ J(u) ∈ V_K, combinazione K-lineare | OK (SymPy T5a, T5b; T5c: con i soli j = e_i−1 il rango cala a 9 < 18 — i j < e_i sono necessari) |
| T5.3 | Passo 3: M > dim R_{≤k₀} punti, nucleo con base in K; Q(∂)e_Q ≠ 0 per C3-L3(b) | OK |
| T5.4 | (Q9) Passo 4: H_Q sottospazi affini propri, unione finita non ricopre K^{𝒬′}; v ∈ EP ∩ ker P ⇒ Ann(v) ⊋ (P) (C3-C2; v = 0 incluso) | OK |
| T5.5 | (Q9) Passo 5: avversario scelto dopo l'esecuzione su u; induzione sulle interrogazioni adattive | OK |
| T5.6 | Notazione: K indica sia il campo ℚ̄ sia l'ordine del jet | **T5-3** (MINOR): ordine del jet → k₀ |
| T5.7 | Esistenza di (Ω, p₀, u) ammissibili con Ann(u) = (P) | **assente** nel testo salvo il calore (C8: u = t^{−1/2}e^{−x²/(4t)} *non normalizzato*, p4_checks.py r. 141; jet razionali, SymPy T5d — l'obiezione dell'arbitro sulla costante 1/√(4π) non si applica). Senza esistenza, per quel P il decisore costante "no" è corretto e la Lettura è vuota. I dati di Cauchy vanno scelti genericamente (SymPy T5e: P = τ², Q = τ, con il solo f₀ i dati di Cauchy di Q(∂)u sono nulli) → **T5-2** (MAJOR), prova fornita in §3.1 |

### 2.6 P4-L3–L6, P4-P2, P4-T6, II-L1(b), P4-C4 (priorità 5)
| MC | passo | esito |
|---|---|---|
| L3.1 | L(qe^{λx}) = e^{λx}L_λq; L3(b) 1D ⇒ L_{λ_k}q_k = 0; (a) coefficiente di x^{D+n} = M_D(λ)q_n | OK |
| L3.2 | (Q10) (b) coefficiente di x^{n+δ_λ} = ι_λ(n)q_n; ι_λ ≢ 0 (fattoriali decrescenti di gradi distinti, coefficienti m_{ij}(λ), i−j = δ_λ, non tutti nulli) | OK (SymPy L3a: x∂ − 5, ι(n) = n − 5, B = 6; L3b indipendenza) |
| L3.3 | conteggio dim ℂ[∂]g ≤ Σ(deg q_k+1) ≤ B(L); M_D costante ⇒ g = 0 | OK |
| L3.4 | calcolabilità: "le radici intere non negative si trovano fra le radici in K (test di uguaglianza)" — (AC) come enunciata (operazioni di campo, uguaglianza, radici in K) non include il test "α ∈ ℤ_{≥0}?" per α ∈ ℚ̄ | **L3-1** (MINOR): estendere (AC) con il test di appartenenza a ℤ_{≥0} (standard con la rappresentazione polinomio minimo + intervallo isolante), oppure: le radici razionali di ι_λ ∈ K[n] sono radici della norma N_{K(λ)/ℚ}(ι_λ) ∈ ℚ[n], che si trovano col teorema delle radici razionali |
| L4.1 | ordine minimo n₀+δ, coefficiente ι_{x₀}(n₀)h_{n₀}; termini con n+i−j < 0 hanno n^{\underline j} = 0; valido anche in punti singolari | OK (SymPy L4a: x⁵ per x∂ − 5 in 0, soglia K₀ = 5 necessaria) |
| L5.1 | 𝒟 su K(x)^N, ε(𝒟v) = (εv)′ fuori da Σ finito; ε K(x)-lineare; N+1 vettori dipendenti; continuità su J₀; casi r_l = 0, N = 0 | OK (Σ deve includere anche gli zeri dei denominatori dei φ_j: dopo la moltiplicazione per il denominatore comune è irrilevante) |
| P2.1 | caso B = 0 (EP non nullo ⇒ B ≥ 1); caso B ≥ 1: N_H = Ann(g) ∩ ℂ[ξ]_{≤B} per C3-T3(i) applicato a G(t,x) = g(x) con d′ = B; ramo N_H = 0; ramo p ∈ N_H∖0 in K con test p(∂)g = 0 (L5 + L4) | OK |
| L6.1 | (c) τ^lQ = AP + Σc_{lj}τ^j, restrizione a t₀ commuta con ∂_x; (a) ricorrenza per j ≥ m, Taylor nulla, analiticità e connessione | OK |
| L6.2 | (Q11) (b)⇐: M_k = C(ξ_k+∂_x) endomorfismo di (ℂ[x]_{≤δ})^m; ∂_tU = C(∂_x)U per C3-L3(a) componente per componente; U ∈ EP(ℝ²)^m, U(t₀) = F; II-L1(b) in F = C^∞(ℝ²) ⇒ E = U₁ ∈ ker P con Cauchy(E) = F; unicità da (a) | OK (SymPy L6a–L6c: onda, dati (xeˣ, e^{2x}), confronto con d'Alembert) |
| IIL1.1 | **II-L1(b)** (work/II/PROOF_PACKAGE.md righe 57–60): u ∈ ker_FP ⇒ U = J(u) soddisfa ∂_tU_i = U_{i+1} (i < k), ∂_tU_k = −Σp_j(∂_x)U_{j+1}; viceversa U_i = ∂_t^{i−1}U₁ e l'ultima riga è P(∂)U₁ = 0; mappe inverse; intreccio J(f(∂)w) = f(∂_x, C(∂_x))J(w) da f = τ, ξ | OK in ogni R-modulo F (nessuna ipotesi su F oltre l'azione di R) → **II-L1(b) DIMOSTRATO**. Convenzione della compagna (1 sulla sopradiagonale, ultima riga −p₀…−p_{k−1}) coerente con P4-L6 (SymPy II-L1(b), m = 3, p_j generici). Letta anche (a): corretta, non richiesta qui |
| T6.1 | (H1) fattori monici in τ (prodotto dei coefficienti direttori = 1 in ℂ[ξ] ⇒ costanti; quindi deg_τP_i ≥ 1) | OK |
| T6.2 | Passo 0: ricorrenza in K (a_{j,r_j}(x₀) ≠ 0); derivate miste da L6(c), Q = 1 (non serve t₀ ∈ K) | OK |
| T6.3 | Passo 1: v = Q(∂)u = 0 ⟺ Cauchy(v) = 0 (L6(a)); componenti g_l = Σc^Q_{lj}(∂_x)f_j; L5 + L4 (anche in punto singolare); analiticità su J₀ | OK |
| T6.4 | Passo 2: L6(b) + P4-P2 per componente | OK (dipende da II-L1(b): chiuso sopra) |
| T6.5 | (Q12) generatori: J_u = Ann(w₀), w₀ = G_u(∂)u ∈ EP (P4-T2(iii)); Cauchy iniettiva su R·w₀ (L6(a)); immagine ⊆ (Σ_jℂ[∂_x]h_j)^m; d₀ ≤ B₀ = m·Σ_jB(L_{h_j}); C3-T3(ii); P4-T4(i). Caso w₀ = 0 (Ann principale): generatori = G_u | OK |
| T6.6 | (AC): usata in Passo 0 (aritmetica), P4-L3 (radici di M_D, ι_λ), P4-P2 (nuclei in K) | assunzione dichiarata, "CON-FONTE generico, non verificato" → **AC-1** (MINOR, ADD_REFERENCE): fonte standard per l'aritmetica effettiva in ℚ̄ (p. es. H. Cohen, *A Course in Computational Algebraic Number Theory*, Springer GTM 138, cap. 4 — numerazione da verificare da CIT-AUDIT); stato di P4-T6: DIMOSTRATO **modulo (AC)** |
| C4.1 | (a) u ∉ EP (C3-P5(a), prova scritta) ⇒ Ann(u) = (τ+ξ): la prova cita **C3-T4(a)**, che non è tra i fatti importati di §A; basta C3-T1(a) con P irriducibile | **C4-1** (MINOR): citare C3-T1(a) (r = 1, e = 1) |
| C4.2 | (a) "nessun dato su una fetta decide": vero per la fetta scelta {1/2}×(−1,1) (stessi dati di e^{x−t}, che non identifica); falso per fette che incontrano il supporto di φ (J₀ = (−5,5)) | **C4-2** (MINOR): "il dato sulla fetta {1/2}×(−1,1) coincide con quello di e^{x−t}: nessun algoritmo che usa solo quella fetta decide" |
| C4.3 | (b) P = ξ(τ−1), u = e^{t²}: Ann(u) = (ξ) (Q(∂)u = Q(∂_t,0)e^{t²}, e^{t²} non EP), (P/ξ)(∂)u = (2t−1)e^{t²}; G_u restituito = 1: sbagliato | OK (SymPy C4b) |
| C4.4 | (c) Lettura: usa P4-T5; per tutti i P solo con P4-L7 (T5-2) | OK con T5-2 |

## 3. Rilievi e fix (proof-checker, Phase 2: proposti, non applicati — S-P4 è chiusa, li smista il coordinatore)
| id | claim | categoria | stato/impatto | severità | strategia | fix |
|---|---|---|---|---|---|---|
| **T2-4** | P4-T2: riga LEDGER 61, TABELLA di S-P4, titolo "Dicotomia" | SCOPE_OVERCLAIM / IMPLICATION_REVERSAL | OVERSTATED (il teorema è corretto; la formulazione registrata è falsa) | **MAJOR** | WEAKEN_CLAIM | Nel LEDGER e nel PROOF_PACKAGE: "Ann(u) principale ⟺ σ_p(u) = ∅ ⟺ R·u ∩ EP = 0; **Ann(u) = (P) ⟺ σ_p(u) = ∅ e G_u ∼ P**; u identifica ⇒ nessun autovettore (non viceversa: u = e^{x²}, P = τ²)". Sostituire "sintesi spettrale ⟺ u EP ⟺ non identifica" con "sintesi spettrale ⟺ u EP ⇒ non identifica (P non costante); il viceversa è falso (u = t + e^{x²}, P4-C2)". Sostituire "Â⁻¹ non esiste quasi ovunque per u identificante" con "risolvente di ∂_t su R·u = ℂ∖π_τV(P), finito se ogni fattore irriducibile di P dipende da ξ (P = τ: ℂ∖{0})". Aggiungere dopo (v)(a) la frase: "la condizione spettrale vede solo J_u, non G_u". |
| **T5-1** | Lettura di P4-T4 (letta con P4-T5) | SCOPE_OVERCLAIM | OVERSTATED + LOCAL (riga C3-Q1) | **MAJOR** | WEAKEN_CLAIM | "Con un test di zero, C3-Q1 **si riduce a** (condizione sufficiente) un maggiorante B ≥ dim(R·u ∩ EP) = dim R/J_u; B dà anche G_u e V(Ann u). Per la sola decisione basta un dato più debole: un maggiorante del grado minimo di un elemento di Ann(u)∖(P). **Senza alcun dato aggiuntivo** il problema non è decidibile nel modello M2⁺ (P4-T5 + P4-L7); non è dimostrato che B sia necessario o minimo." |
| **T5-2** | P4-T5 (portata "per ogni P"), P4-C4(c), riga C3-Q1 | MISSING_DERIVATION | UNJUSTIFIED + LOCAL | **MAJOR** | ADD_DERIVATION | aggiungere **P4-L7** (§3.1, prova completa sotto) e citarlo nella Lettura e nella riga C3-Q1 |
| T2-1 | P4-T2 Casi limite | CASE_INCOMPLETE (formulazione) | UNCLEAR + COSMETIC | MINOR | riformulare | "u = 0 (⟺ I = R) è ammesso ed è banale: G ∼ 1, J = R, W = 0, tutti gli insiemi vuoti" |
| T2-2 | P4-T2(v)(b) | REFERENCE (dipendenza non auditata) | — | MINOR | ADD_DERIVATION | inlinare C3-T2(a): "per C3-L3(a), Q(∂)u = Σ_k(Q(z_k+∂)q_k)e^{⟨z_k,·⟩}, nullo ⟺ ogni coefficiente nullo (C3-L3(b))"; C3-T2(a) è comunque DIMOSTRATO (T2.12) |
| T2-3 | P4-T2(v)(b), radicale | LOGICAL_GAP (lapsus) | UNCLEAR + LOCAL (alla lettera la scelta di ℓ fallisce, SymPy T2d) | MINOR | correggere | sostituire le due occorrenze di ℓ(∂)q_k con ℓ(z_k+∂)q_k (= ∂_tq_k o ∂_xq_k): "scegliamo ℓ ∈ {τ−τ_{z_k}, ξ−ξ_{z_k}} con ℓ(z_k+∂)q_k ≠ 0" e "Q(z_k+∂)q_k = [∏_{j≠k}ℓ_j(z_k+∂)]ℓ(z_k+∂)q_k" |
| T2-5 | P4-T2 mappa delle dipendenze | UNCLEAR | COSMETIC | MINOR | precisare | "(iii) ← forma degli autovettori di (ii)"; "(ii) V(J) ⊆ σ_p ← isomorfismo di (iii) (che non usa questo passo)"; oppure spostare il passo dopo (iii) |
| T5-3 | P4-T5 | NOTATION | COSMETIC | MINOR | rinominare | ordine del jet K → k₀ (K resta ℚ̄) |
| T1-1 | P4-T1(iv) | REFERENCE (prova scritta) | — | MINOR | dichiarare | "(iv) dipende da C3-L1 (prova scritta, non auditata)" |
| L1-1 | P4-L1(c) | LOGICAL_GAP (lieve) | — | MINOR | ADD_DERIVATION | ordine lessicografico sui multi-indici (T2.2, L1.3) |
| T3-1 | P4-T3(iv) | HIDDEN_ASSUMPTION | — | MINOR | precisare | "per u EP basta il jet di ordine d + d′ − 1, con d′ ≥ d un maggiorante noto (2d−1 se d è noto)" |
| L3-1 | P4-L3 calcolabilità | HIDDEN_ASSUMPTION | — | MINOR | precisare | test "α ∈ ℤ_{≥0}" per α ∈ ℚ̄ incluso in (AC), o via norma su ℚ e teorema delle radici razionali |
| AC-1 | (AC), P4-T6 | REFERENCE_MISMATCH (fonte non indicata) | — | MINOR | ADD_REFERENCE | fonte standard per l'aritmetica esatta in ℚ̄ → CIT-AUDIT; stato P4-T6 "DIMOSTRATO modulo (AC)" |
| C4-1 | P4-C4(a) | REFERENCE_MISMATCH | — | MINOR | correggere | C3-T4(a) → C3-T1(a) (r = 1) |
| C4-2 | P4-C4(a) | SCOPE (formulazione) | — | MINOR | riformulare | come in C4.2 |

### 3.1 Fix T5-2 — P4-L7 (esistenza di dati ammissibili identificanti), prova
**Enunciato.** Sia K = ℚ̄ e P ∈ K[τ,ξ] non costante, P = c∏_iP_i^{e_i} con P_i ∈ K[τ,ξ] irriducibili non associati. Esistono un aperto connesso Ω ∋ 0, p₀ = 0 e u reale-analitica su Ω con P(∂)u = 0, ∂^αu(0) ∈ K per ogni α, e **Ann(u) = (P)**. In particolare P4-T5 non è vuoto per nessun P, e "Ann(·) = (P)" non è decidibile nel modello M2⁺ senza dato aggiuntivo, per ogni P non costante.
**Prova.** (1) *Riduzione al caso non caratteristico.* Sia m = deg P e P_m ≠ 0 la parte omogenea di grado m. P_m si annulla su un numero finito di rette per l'origine, quindi esiste (a,b) ∈ ℚ² con P_m(a,b) ≠ 0. Sia A ∈ GL₂(ℚ) con A^{−T}e₁ = (a,b) e y = Ay′. Per u′ := u∘A si ha ∂′ = A^T∂ (gradiente della composizione), quindi (Q(∂)u)∘A = Q^A(∂′)u′ con Q^A(ζ′) := Q(A^{−T}ζ′); Q ↦ Q^A è un automorfismo K-lineare di K[τ,ξ] che conserva grado, irriducibilità e divisibilità, e Ann(u′) = {Q^A : Q ∈ Ann(u)}; i jet di u′ in 0 sono combinazioni K-lineari (anzi ℚ-lineari) di quelli di u e viceversa. Il coefficiente di τ′^m in P^A è P_m(A^{−T}e₁) = P_m(a,b) ≠ 0 (solo la parte di grado m contribuisce a τ′^m). Basta quindi provare il lemma per P^A: d'ora in poi P è **monico in τ di grado m = deg P** (dopo divisione per una costante), cioè t = 0 non caratteristica; anche ogni P_i è allora monico in τ (a meno di costanti) con deg_τP_i = deg P_i ≥ 1.
(2) *Dati di Cauchy.* Per λ = (λ₀,…,λ_{m−1}) ∈ ℚ^m siano f_j(x) := λ_je^{x²} (j < m). Per il teorema di Cauchy–Kovalevskaya (P non caratteristico per {t = 0}, dati analitici) esiste un'unica u reale-analitica in un intorno connesso Ω di 0 (si può prendere Ω = (−ε,ε)×(−ε,ε), J₀ = (−ε,ε)) con P(∂)u = 0 e ∂_t^ju(0,·) = f_j. I jet di u in 0 stanno in ℚ: le derivate ∂_x^bf_j(0) sono razionali, e per j ≥ m la ricorrenza ∂_t^ju = −Σ_{l<m}p_l(∂_x)∂_t^{j−m+l}u (come in P4-L6(a)) ha coefficienti in K.
(3) *Ann(u) = (P).* Per C3-T1(a) basta w_i := Q_i(∂)u ∉ EP(Ω) per ogni i, con Q_i := P/P_i. P è monico in τ e u analitica: per P4-L6(b) (con t₀ = 0, J₀) w_i ∈ EP ⟺ ogni componente di Cauchy(w_i) sta in EP(J₀). Poiché deg_τQ_i = m − deg_τP_i < m, la divisione di Q_i per P dà resto Q_i stesso, e per P4-L6(c) con l = 0: Cauchy(w_i)₀ = w_i(0,·) = Σ_jc^{(i)}_j(∂_x)f_j = r_i^λ(∂_x)e^{x²}, dove c^{(i)}_j(ξ) è il coefficiente di τ^j in Q_i e r_i^λ(ξ) := Σ_jλ_jc^{(i)}_j(ξ). La mappa λ ↦ r_i^λ, ℚ^m → K[ξ], è lineare e non nulla (Q_i ≠ 0 ha qualche c^{(i)}_j ≠ 0), quindi il suo nucleo è un sottospazio proprio; si sceglie λ ∈ ℚ^m fuori dall'unione finita di questi nuclei (i = 1,…,r). Allora r_i^λ ≠ 0 e r_i^λ(∂_x)e^{x²} ∉ EP(J₀): se s(∂_x)r_i^λ(∂_x)e^{x²} = 0 con s ≠ 0, e^{x²} sarebbe EP (in una variabile un annullatore non nullo a coefficienti costanti dà EP), mentre ∂_x^ke^{x²} = p_k(x)e^{x²} con deg p_k = k dà dim ℂ[∂]e^{x²} = ∞. Quindi w_i ∉ EP per ogni i e Ann(u) = (P). ∎
*Note.* (a) La scelta generica di λ è necessaria: per P = τ², Q₁ = τ, con il solo f₀ ≠ 0 si ha Cauchy(Q₁(∂)u) = (f₁, 0) = 0 e Ann(u) ∋ τ (SymPy T5e). (b) Per il calore (caratteristico per t = 0) il passo (1) è indispensabile; resta valido anche l'esempio diretto C8 (u = t^{−1/2}e^{−x²/(4t)} in (1,0), jet razionali, SymPy T5d). (c) Dipendenze: Cauchy–Kovalevskaya (classico, CON-FONTE: p. es. Folland, *Introduction to PDE*, cap. 1 — numerazione → CIT-AUDIT), P4-L6(b),(c) (DIMOSTRATO qui, con II-L1(b)), C3-T1(a).

## 4. Conseguenze per LEDGER e ROUTES (proposte al coordinatore)
- Righe nuove/aggiornate: vedi TABELLA in inbox/central.md (S-CHECK-6). Stati: DIMOSTRATO per P4-T1 ((iv) cond. C3-L1), P4-L1, P4-C1, P4-T2, P4-C2, P4-T3, P4-C3, P4-L2, **P4-P1**, P4-T4, P4-T5 (condizionale; portata "∀P" con P4-L7), P4-L3–L6, P4-P2, P4-T6 (modulo AC), P4-C4; **C3-T2(a) DIMOSTRATO**; **II-L1(b) da APERTO-con-prova a DIMOSTRATO**; P4-L7 proposto (prova in §3.1: "prova scritta, verificata dal revisore", da inserire nel PROOF_PACKAGE di P4 e confermare con un controllo indipendente se il coordinatore lo ritiene necessario, perché è il revisore ad averla scritta).
- **Riga 61 del LEDGER va riscritta (T2-4):** contiene un bicondizionale falso ("dicotomia identifica ⟺ nessun autovettore") e "Â⁻¹ non esiste quasi ovunque" senza la qualifica; la colonna "dipende da" deve dire II-L1(b) DIMOSTRATO (S-CHECK-6).
- **C3-Q1**: APERTO → PARZIALE sostenuto, con la formulazione di T5-1 (B sufficiente, non dimostrato necessario) e con P4-L7.
- **RT-R4a → MERGE-INTO RT-4**: P4-C1 è corretto (kill criterion scattato); nessuna obiezione dell'audit.
- **G★′ punto 2** (cammino critico): P4-P1 DIMOSTRATO (dipende da C12-T1′ DIMOSTRATO, C3-T1, Fatto (V)). Il kill-argument non è stato lanciato su P4-P1 (bersagli scelti dal piano: P4-T2, P4-T5); la prova è di quattro righe e ogni passo è verificato in §2.4. Se il coordinatore vuole il passaggio avversariale formale anche su P4-P1, va lanciato a parte.

## 5. Red team SymPy (Phase 1.5) — `work/CHECK/sympy/audit_p4.py` → `audit_p4.out`: **34/34 OK**
Verifiche su esempi (V-ex), non prove. Copertura: P4-C2 (C2a, C2b); attacco KA-A (u = e^{x²}, P = τ²: Ann = (τ) principale, ≠ (τ²)); P4-T2 su u = xe^{t+x} + e^{4t+2x} (T2a; C3-T2(a) su 8 polinomi T2b; non radicale T2c; **lapsus ℓ(∂) T2d**; caso radicale T2e; autovettore T2f); (LS) + teorema cinese su J = (τ², ξ(ξ−1)) (LS1–LS3); P4-T3 (T3a–T3c); P4-C3 (C3a–C3c); P4-T5 Passo 2 con P = (τ−ξ²)², k₀ = 5 (T5a dim V = 18, T5b, **T5c necessità dei j < e_i**); C8 jet razionali (T5d); P4-L3/L4 (L3a, L4a, L3b); P4-L6(b) + II-L1(b) (L6a–L6c, II-L1(b) simbolico m = 3); P4-L1 (L1a); P4-C1 (C1b); P4-T2(vi) e riga LEDGER (T2g: P = τ, risolvente ℂ∖{0}); P4-C4(b) (C4b); esistenza (T5e: necessità della scelta generica dei dati). Nessun controesempio agli enunciati come scritti; due controesempi alle formulazioni (KA-A → T2-4, T2g → T2-4) e uno alla lettera della prova (T2d → T2-3). Controlli di S-P4 (p4_checks.out 36/36) non rieseguiti.

## 6. Kill-argument (cammino critico) — skill kill-argument, revisori = subagenti Claude freschi senza contesto
Protocollo: Thread 1 (attacco, ~200 parole) e Thread 2 (arbitrato per punti) affidati a due subagenti distinti e freschi per ciascun bersaglio, che hanno ricevuto solo il file di input (estratto letterale della CHECK_REQUEST) e, per l'arbitro, il memo; verdetto calcolato da me con la tabella della skill. File: `KA_P4_T2_input.md`, `KA_P4_T2_attack.md` (agente a3a6b4be4aec9658d), `KA_P4_T2_adjudication.md` (agente acc5928ba08659033); `KA_P4_T5_input.md`, `KA_P4_T5_attack.md` (agente a474f066361fd42a5), `KA_P4_T5_adjudication.md` (agente af6b3674785288ffb).
*Nota di trasparenza:* la riga di titolo di `KA_P4_T2_input.md` ("dicotomia 'u identifica ⟺ nessun autovettore'") è stata scritta da S-CHECK-6 riprendendo la riga 61 del LEDGER, non dal testo di P4-T2; l'attacco l'ha presa come enunciato. Il rilievo resta valido perché la stessa formulazione è nel LEDGER e nella TABELLA di S-P4 (T2-4).

### 6.1 Bersaglio A — P4-T2 · **Verdetto: WARN** (reason_code: unresolved_major_or_minor)
Attacco: "il bicondizionale 'identifica ⟺ nessun autovettore' è falso (u = e^{x²}, P = τ²); la condizione spettrale vede solo J, non G_u; difetti: V(J) ⊆ σ_p dipende da (iii), C3-T2(a) non auditato, ℓ(∂) vs ℓ(z_k+∂), casi limite contraddittori".
| punto | accusa | classificazione | severità |
|---|---|---|---|
| P1 | bicondizionale nel titolo | partially_answered (l'enunciato è a una direzione; l'etichetta no) | major |
| P2 | controesempio e^{x²}, τ² | answered (corretto, ma confuta solo l'etichetta) | — |
| P3 | lo spettro non vede G_u | partially_answered (limite di portata reale) | major |
| P4 | circolarità V(J) ⊆ σ_p | answered (nessuna circolarità) | — |
| P5 | C3-T2(a) non auditato | partially_answered (auditato qui: PASS) | minor |
| P6 | ℓ(∂)q_k | still_unresolved | minor |
| P7 | casi limite u = 0 | still_unresolved | minor |
Conteggi: 2 answered / 3 partial / 2 unresolved (nessun critical) ⇒ **WARN**. Recepito: P1, P3 → T2-4 (MAJOR); P5 → T2-2 e audit di C3-T2(a); P6 → T2-3; P7 → T2-1. Concordanza con l'audit: piena (l'audit aveva già trovato T2-3 e T2-1 in modo indipendente, SymPy T2d).

### 6.2 Bersaglio B — P4-T5 · **Verdetto: WARN** (reason_code: unresolved_major_or_minor)
Attacco: "nessun passo falso, ma P4-T5 è un argomento avversario generico; non prova 'esattamente' né che il maggiorante non si possa eliminare; B non è il dato minimo; l'esistenza di u con Ann(u) = (P) non è provata fuori dal calore".
| punto | accusa | classificazione | severità |
|---|---|---|---|
| P_1 | "esattamente" senza viceversa | partially_answered | major |
| P_2 | B non minimo (basta il grado di un testimone) | still_unresolved | major |
| P_3 | "non si può eliminare" | partially_answered (vero come "senza alcun dato aggiuntivo") | minor |
| P_4 | argomento generico, vale per ogni dato | answered (falso: B rompe l'avversario, perché dim(R·v ∩ EP) ≥ 1 per v ≠ 0 in E_P^K) | — |
| P_5 | esistenza di u ammissibile | still_unresolved | major |
Conteggi: 1 answered / 2 partial / 2 unresolved (nessun critical) ⇒ **WARN**. Recepito: P_1–P_3 → T5-1 (MAJOR); P_5 → T5-2 (MAJOR) con P4-L7 provato in §3.1 (dopo il fix il punto è risolto; l'obiezione sulla costante 1/√(4π) in C8 non si applica: S-P4 usa G non normalizzato); nota dell'arbitro su K → T5-3.

### 6.3 Concordanza con l'audit
I due kill-argument non hanno trovato passi errati negli enunciati; colpiscono le formulazioni (LEDGER, Letture). L'audit li recepisce come tre MAJOR di portata (T2-4, T5-1, T5-2), nessuno dei quali tocca la prova dei teoremi come scritti. Con i fix MINOR applicati e T2-4, T5-1, T5-2 recepiti, tutti i claim di S-P4 superano l'acceptance gate.
