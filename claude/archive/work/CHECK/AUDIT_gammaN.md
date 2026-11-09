# AUDIT γ_N — P2-C2, P2-T4(1),(2) + applicazione (i), C12-P7(a),(c),(d) (+ gram.md §2bis)
Revisore: S-CHECK-7 (7ª tornata) · 26/10/2026
**Fonti esaminate.** (1) `work/P2/CHECK_REQUEST_2.md` (autosufficiente: notazione, fatti esterni, enunciati e prove di P2-C2 e P2-T4, 9 domande). (2) `work/C1C2/PROOF_PACKAGE.md` §6 [C12-P7] (ipotesi, ipotesi per N ≥ 2 fattori, tesi (a)–(d), prova, *Portata*, *Stato*) e `work/C1C2/gram.md` §0 (riga di convenzioni) e §2bis. Ho lavorato dagli enunciati e dalle prove; stati, commenti e righe LEDGER proposte non sono stati presi come evidenza. Non ho letto `work/P2/PROOF_PACKAGE.md` (la CHECK_REQUEST_2 dichiara di copiarne alla lettera §7).
**Fatti esterni usati come dati.** P2-T1 (DIMOSTRATO, AUDIT_P2), P2-T3(b) (DIMOSTRATO, AUDIT_P2), P2-C1(a) (DIMOSTRATO, AUDIT_P2: densità per m = 0 nei trasporti paralleli su convessi limitati), C12-C1 (DIMOSTRATO). Teorema spettrale per autoaggiunti limitati, mappa aperta, compattezza debole delle palle, continuità debole degli operatori limitati, σ(AB)∖{0} = σ(BA)∖{0} (fatti standard).
**Skill caricate** (lettura dei SKILL.md, nessuno script _vendor eseguito): skills-local/session-protocol (per prima), skills-local/claim-lifecycle, proof-checker (Phase 0.5 enunciati canonici e micro-claim, checklist A–H, Phase 1.5 red team, severità a due assi, acceptance gate; il reviewer sono io, niente Codex), scientific-critical-thinking (mostrato vs affermato; stato proporzionato all'evidenza), sympy.
**SymPy/numpy:** `work/CHECK/sympy/audit_gammaN.py` → `audit_gammaN.out`, **ESITO 78/78 OK** (.venv -I). Controlli di coerenza su esempi finiti e su troncamenti delle costruzioni infinito-dimensionali: non sostituiscono le prove, che ho controllato a mano passo per passo.
**Perimetro.** II-L1(b) e i claim di S-P4 sono di S-CHECK-6 e non sono auditati qui. C12-P7(b) (DIMOSTRATO per N = 2) e C12-T5 (norma di Aronszajn, citata in gram.md §0) non sono rieseguiti.

## 0. Verdetti
| claim | verdetto | stato proposto |
|---|---|---|
| **P2-C2** (a)–(f) | **PASS-con-fix(C2-1, C2-2)** (entrambi MINOR) | **DIMOSTRATO** (spazio di Hilbert reale o complesso, N ≥ 2 sottospazi chiusi non tutti nulli) |
| **P2-T4** (1) | **PASS** | DIMOSTRATO (era già DIMOSTRATO, AUDIT_P2) |
| **P2-T4** (2) (selezioni esatte, fix T4-1) | **PASS** | **DIMOSTRATO** |
| P2-T4 applicazione (i) | **PASS** (nota T4-a) | DIMOSTRATO come implicazione: vale per ogni procedura che soddisfa le ipotesi (R_α lipschitziane, convergenza puntuale a una selezione esatta); per ℓ¹/MCA le ipotesi non sono verificate qui |
| **C12-P7(a)** | **PASS-con-fix(P7-1, P7-2)** | **DIMOSTRATO** l'equivalenza; la densità resta APERTA in generale (P2-Q1); "indipendenti" va ristretto (P7-1) |
| **C12-P7(c)** | **PASS-con-fix(P7-3)** | **DIMOSTRATO** (= P2-C2(b) nello spazio di Hilbert H^m(Ω)) |
| **C12-P7(d)** | **PASS-con-fix(P7-4)** | **DIMOSTRATO** come enunciato in uno **spazio di Hilbert astratto**; nessuna affermazione per nuclei di operatori differenziali (aperto, C12-Q2) |
| gram.md §2bis | coerente con P2-C2 e C12-P7 | — (da aggiornare la dicitura "audit in attesa") |

Nessun rilievo FATAL, CRITICAL o MAJOR. Acceptance gate: soddisfatto per tutti i claim (nessun FATAL/CRITICAL aperto; ipotesi esplicite; ogni applicazione scarica le ipotesi; nessun O(·) non dichiarato; red team eseguito su tutti i lemmi chiave).

## 1. Enunciati canonici (Phase 0.5)
- **P2-C2.** ∀H Hilbert (ℝ o ℂ), ∀N ≥ 2, ∀ℋ_1,…,ℋ_N ⊂ H chiusi non tutti nulli; W = ⊕ℋ_j, S(ω) = Σω_j, T = S*S, γ_N := inf σ(T|_{(ker S)^⊥}):
  (a) S*h = (P_jh)_j, ker T = ker S, σ(T) ⊆ {0} ∪ [γ_N, ‖S‖²], γ_N ∈ σ(T), ‖S‖² ≤ N;
  (b) Σℋ_j chiuso ⟺ γ_N > 0; se γ_N > 0, ‖S^†‖ = γ_N^{−1/2} (ottimale); se γ_N = 0, sup_{u ∈ im S∖0}‖S^†u‖/‖u‖ = ∞;
  (c) ∀α > 0: ‖R_α‖² = sup_{σ(T)} λ/(λ+α)²; sup_α‖R_α‖ = γ_N^{−1/2} (non raggiunto) se γ_N > 0, = ∞ se γ_N = 0;
  (d) γ_N > 0, u ∈ im S ⇒ ∀α > 0: ‖ω_α(u) − S^†u‖ ≤ α/(γ_N+α)·‖S^†u‖ (uguaglianza se S^†u autovettore di γ_N); γ_N = 0 ⇒ ∃u ∈ M∖im S e ∀ tale u: Sω_α(u) → u, ‖ω_α(u)‖ → ∞ (α → 0);
  (e) ∀ω ∈ W: (1−‖C‖)‖ω‖² ≤ ‖Sω‖² ≤ (1+‖C‖)‖ω‖², C = (‖P_iP_j‖)_{i≠j}; ‖C‖ < 1 ⇒ ker S = 0, γ_N ≥ 1−‖C‖ ≥ 1 − max_i Σ_{j≠i} c_ij, somma chiusa; N = 2, ℐ = 0: uguaglianza;
  (f) ∃ (in un Hilbert separabile) tre chiusi con intersezioni a coppie nulle, c_F ≤ 1/2 a coppie, somma tripla densa e non chiusa; ∃ tre chiusi con ℋ_1+ℋ_2 non chiuso e somma tripla chiusa; ∃ due terne di rette con tutti i c_F a coppie = 1/2 e γ_3 = 1/2, rispettivamente 3/2.
- **P2-T4.** (1) ∀X, Y normati, ∀V ⊆ X, ∀Φ: V → Y, ∀(R_α) lipschitziane di costanti L_α con R_αv → Φv ∀v ∈ V: Lip(Φ) ≤ liminf_{α→0} L_α. (2) ∀ℋ_1,…,ℋ_N come in P2-C2, ∀σ: Σℋ_j → W con Sσ = id: Lip(σ) ≥ γ_N^{−1/2} (= ∞ se γ_N = 0).
- **C12-P7.** Ω ⊂ ℝ² limitato lipschitziano connesso, m ≥ 0, P = c∏_{j=1}^N Q_j con Q_j = P_j^{m_j} a due a due coprimi, ℋ_j = ker_{H^m(Ω)}Q_j, W, S, γ_N come sopra nello spazio di Hilbert H^m(Ω) (γ_N := +∞ se (ker S)^⊥ = 0): (a) ker_{H^m}P = Σℋ_j ⟺ Σℋ_j chiuso e denso in ker_{H^m}P; (c) Σℋ_j chiuso ⟺ γ_N > 0, e allora Σ‖u_j‖² ≤ γ_N^{−1}‖u‖² per lo split S^†u, costante ottimale; (d) ∃ (in un Hilbert astratto) tre chiusi a intersezioni nulle, somme a coppie chiuse (c_F ≤ 1/2), somma tripla non chiusa; ∃ terna con una coppia a somma non chiusa e somma tripla chiusa.

## 2. Dipendenze (DAG, nessun ciclo)
P2-C2(a) ← teorema spettrale. (b) ← (a), mappa aperta. (c) ← (a), calcolo funzionale, "punto isolato ⇒ autovalore". (d) ← (a), (b), P2-T1, compattezza debole. (e) ← Cauchy–Schwarz, Gershgorin; confronto N = 2 ← **P2-T3(b)**. (f) ← (b), (e) o **P2-T3(b)** (chiusura/non chiusura delle somme a coppie). P2-T4(2) ← P2-C2(b). App. (i) ← P2-T4(1),(2), P2-C2(c),(d). C12-P7(a) ← continuità di P(∂); (c) ← teorema spettrale, mappa aperta (= P2-C2(b)); (d) ← (b) di C12-P7 / P2-T3(b), (c). Nessun riferimento in avanti; P2-T3 non usa P2-C2. **Rilievo C2-1:** la riga "Dipendenze … Nessuna dipendenza da P2-T3: la prova è autonoma" è inesatta per (e) (ultima frase) e (f).

## 3. Micro-claim ed esiti — P2-C2
| MC | passo | esito |
|---|---|---|
| C2.1 | (a) ⟨Sω,h⟩ = Σ⟨ω_j,P_jh⟩ ⇒ S*h = (P_jh)_j; ‖Sω‖ ≤ Σ‖ω_j‖ ≤ √N‖ω‖ (Cauchy–Schwarz in ℝ^N) | OK |
| C2.2 | ⟨Tω,ω⟩ = ‖Sω‖² ⇒ ker T = ker S; T autoaggiunto riduce ker T e (ker T)^⊥ | OK |
| C2.3 | σ(T) = σ(0|_{ker S}) ∪ σ(T|_{(ker S)^⊥}) (somma diretta ortogonale di parti ridotte) ⊆ {0} ∪ [γ_N, ‖T‖], ‖T‖ = ‖S‖² | OK. **Domanda (a)/(b):** sì, vale senza ipotesi su dim ker S (anche infinita): serve solo che (ker S)^⊥ sia chiuso e invariante. Se ker S = 0 il termine {0} può mancare: l'inclusione resta vera |
| C2.4 | γ_N = min σ(T|_{(ker S)^⊥}) = inf del rango numerico di T|_{(ker S)^⊥} = inf{‖Sω‖² : ω ⊥ ker S, ‖ω‖ = 1}; (ker S)^⊥ ≠ 0 perché S ≠ 0 (un ℋ_j ≠ 0) | OK (audit_gammaN C2(a,b), 7 famiglie reali e complesse, dim ker S = 0…3) |
| C2.5 | (b) im S = S((ker S)^⊥) (ω = P_{(ker S)^⊥}ω + k) | OK |
| C2.6 | limitata dal basso ⇒ immagine chiusa (immagine di un completo, Cauchy ↦ Cauchy); immagine chiusa ⇒ inversa limitata (mappa aperta tra Banach (ker S)^⊥ e im S) | OK |
| C2.7 | ‖S^†u‖²/‖u‖² = ‖ω‖²/‖Sω‖², sup = 1/γ_N; ogni ω ≠ 0 in (ker S)^⊥ ha Sω ≠ 0, quindi per γ_N = 0 il rapporto è illimitato; minimalità: ‖ω+k‖² = ‖ω‖²+‖k‖² | OK (audit ‖S^+‖ = γ^{−1/2}) |
| C2.8 | (c) R_αR_α* = (T+α)^{−1}T(T+α)^{−1} = T(T+α)^{−2} (funzioni di T commutano); ‖R_α‖² = ‖R_αR_α*‖ = max_{σ(T)} λ/(λ+α)² | OK (audit C2(c): formula esatta su tutte le famiglie) |
| C2.9 | γ_N > 0: λ/(λ+α)² < 1/λ ≤ 1/γ_N per λ ≥ γ_N; il max su un compatto è < 1/γ_N (non raggiunto); γ_N ∈ σ(T) dà il limite 1/γ_N. Inoltre ‖R_α‖ è crescente per α ↓ 0 (ogni λ/(λ+α)² lo è) | OK (audit: monotonia verificata) |
| C2.10 | γ_N = 0: 0 ∈ σ(T|_{(ker S)^⊥}) (C2.4) e T|_{(ker S)^⊥} iniettivo; punto isolato dello spettro di un autoaggiunto ⇒ autovalore (E({λ₀}) ≠ 0, Ran E({λ₀}) = ker(T−λ₀)); quindi λ_k ↓ 0 in σ(T), ‖R_{λ_k}‖² ≥ 1/(4λ_k) | OK. **Domanda (c):** l'uso è corretto e identico a P2-T3(c) (T3.13 di AUDIT_P2). Audit: troncate dell'esempio (f), ‖R_{λ_K}‖ ≥ 1/(2√λ_K) |
| C2.11 | (d) ω_α = (T+α)^{−1}S*u unico minimizzatore (strettamente convesso, gradiente S*(Sω−u)+αω) | OK |
| C2.12 | S*u = Tω^†, ω_α − ω^† = −α(T+α)^{−1}ω^†; norma di α(T+α)^{−1} su (ker S)^⊥ = α/(γ_N+α), raggiunta sull'autovettore | OK (audit C2(d): stima e uguaglianza) |
| C2.13 | γ_N = 0 ⇒ im S ⊊ M (per (b)); P2-T1 con R = ½‖·‖², ε_α = 0 | OK. **Domanda (d):** le ipotesi di P2-T1 sono soddisfatte: {R < ∞} = W, S(W) = im S è denso in M = \overline{im S} per definizione; il minimizzatore esatto ha ε_α = 0; J_α = ½‖u−Sω‖² + α·½‖ω‖² è la forma di P2-T1. Conclusione Sω_α → P_Mu = u |
| C2.14 | se ‖ω_{α_k}‖ ≤ C lungo α_k → 0: sottosuccessione debolmente convergente a ω, Sω_{α_k} ⇀ Sω e Sω_{α_k} → u ⇒ Sω = u ∈ im S, assurdo. Quindi ogni successione α_k → 0 ha ‖ω_{α_k}‖ → ∞ | OK |
| C2.15 | (e) ‖Sω‖² = Σ‖ω_j‖² + Σ_{i≠j}⟨ω_i,ω_j⟩; \|⟨ω_i,ω_j⟩\| = \|⟨ω_i,P_iP_jω_j⟩\| ≤ c_ij‖ω_i‖‖ω_j‖ | OK (c_ij = c_ji perché (P_iP_j)* = P_jP_i) |
| C2.16 | \|Σ_{i≠j}⟨ω_i,ω_j⟩\| ≤ nᵀCn ≤ ‖C‖\|n\|², \|n\| = ‖ω‖ | OK. **Domanda (e):** corretta (C simmetrica a entrate ≥ 0, n ≥ 0 componente per componente) |
| C2.17 | ‖C‖ < 1 ⇒ S iniettiva, γ_N ≥ 1−‖C‖, somma chiusa per (b); ‖C‖ = ρ(C) ≤ max riga (Gershgorin, o norma ∞ indotta) | OK (audit C2(e): bound su tutte le famiglie, caso ‖C‖ = 0.994 < 1 con γ = 0.30) |
| C2.18 | ℐ_{ij} = 0 ⇒ c_F = sup_b ‖P_ib‖ = ‖P_iP_j‖ | OK (audit: = s_max(B_i*B_j)). **Domanda (e), intersezione non nulla:** z ∈ ℋ_i∩ℋ_j unitario dà ‖P_iP_j‖ = 1, quindi ‖C‖ ≥ 1 e la stima (1−‖C‖)‖ω‖² ≤ ‖Sω‖² è vera banalmente; la conclusione "se ‖C‖ < 1" non si applica. La (e) resta vera come scritta (audit: casi 1, 4) |
| C2.19 | N = 2, ℐ = 0, ℋ_1 ≠ 0 ≠ ℋ_2: ‖C‖ = c_F, γ_2 = 1−c_F per P2-T3(b) | OK, ma usa P2-T3(b) → **C2-1** |
| C2.20 | (f) non sufficienza: ⟨v_i,v_j⟩ = −½cos²ε + sin²ε = −½ + (3/2)sin²ε ∈ (−½, 0) per 0 < sin²ε < 1/3 (sin²(½) = 0.2298) | OK (SymPy simbolico) |
| C2.21 | VVᵀ = diag((3/2)cos²ε, (3/2)cos²ε, 3sin²ε); VᵀV e VVᵀ isospettrali (quadrate); γ_3 = 3sin²ε perché tan²ε ≤ tan²(½) = 0.298 < ½ | OK (SymPy simbolico; numerico ε = 2^{−k}, k ≤ 11). **Domanda (f):** il conto è corretto |
| C2.22 | blocchi: ℋ_j chiusi (immagini isometriche di ℓ²); ℋ_i∩ℋ_j = 0 blocco per blocco; c_F = sup_k\|c(ε_k)\| (per a = (s_kv_i), b = (t_kv_j) unitari, \|⟨a,b⟩\| ≤ sup\|c_k\|·Σ\|s_kt_k\| ≤ sup\|c_k\|, e i vettori di un solo blocco danno \|c_k\|) ≤ ½ | OK (audit troncate K = 3, 6, 10: c_F = 0.4767, 0.4996, 0.499999 ≤ ½; il sup ½ non è raggiunto) |
| C2.23 | ker S = ⊕ker V_k = 0; ‖Sω‖² = Σ⟨V_kᵀV_kt_k,t_k⟩ ≥ inf_kλ_min‖ω‖²; i vettori concentrati sul blocco k danno 3sin²ε_k; γ_3 = 0 ⇒ somma non chiusa (b) | OK |
| C2.24 | densità: ogni successione a supporto finito ha preimmagine a supporto finito (V_k invertibile), e queste sono dense in ⊕ℝ³ | OK (audit: rank S = dim H sulle troncate). **Controesempio "densa ma non chiusa": verificato** |
| C2.25 | la riduzione a blocchi è completa: S, T, P_iP_j commutano con la scomposizione ortogonale in blocchi; ker S, γ_3, c_F, densità sono stati controllati uno per uno (C2.22–C2.24) | OK. **Domanda (f), riduzione a blocchi:** completa |
| C2.26 | non necessità: c_F(ℋ_1,ℋ_2) = sup_kcos θ_k = 1 (non raggiunto), ℋ_1∩ℋ_2 = 0 ⇒ ℋ_1+ℋ_2 non chiuso (P2-T3(b)); ℋ_1+ℋ_2+ℋ_3 = H chiuso | OK. **Domanda (f), non necessità:** controesempio valido all'enunciato "chiusura della tripla ⇒ chiusura delle somme a coppie"; le intersezioni non nulle con ℋ_3 = H non sono escluse dall'enunciato |
| C2.27 | "VVᵀ = aaᵀ+bbᵀ+I ≥ I, quindi γ_3 ≥ 1" | **LACUNA (MINOR)**: VVᵀ blocco per blocco è SS* (su H), γ_3 è definito da S*S su (ker S)^⊥ e qui ker S ≠ 0. Il passo da SS* ≥ I a γ_3 ≥ 1 richiede σ(S*S)∖{0} = σ(SS*)∖{0} e γ_3 ≠ 0, non dichiarati → **C2-2**. Non tocca la validità del controesempio (la chiusura di H è banale). Audit: σ(S*S)∖{0} = σ(SS*)∖{0} e γ_3 ≥ 1 sulle troncate |
| C2.28 | nessuna formula: tre rette a 120° in ℝ²: Gram con fuori diagonale −½, autovalori 0, 3/2, 3/2, ker S = span(1,1,1), γ_3 = 3/2; Gram con +½ definita positiva (Cholesky), autovalori 2, ½, ½, γ_3 = ½; rette distinte, intersezioni nulle, c_F = ½ in entrambi i casi | OK (SymPy esatto: autovalori, realizzazione a 120° e Cholesky, coseni). **Domanda (f), Gram:** sì. **Caso γ_3 = 1/2 vs 3/2 del coordinatore: confermato.** In entrambi ‖C‖ = 1, quindi il bound (e) dà 0: coerente |
| C2.29 | (f) è costruita in spazi reali; l'enunciato ammette H complesso | OK: le stesse rette in ℂ³ (ℂv_k) danno le stesse Gram e gli stessi coseni (vettori reali); nota facoltativa |

## 4. Micro-claim ed esiti — P2-T4
| MC | passo | esito |
|---|---|---|
| T4.1 | (1) ‖Φv−Φw‖ = lim_α‖R_αv−R_αw‖ ≤ liminf_αL_α‖v−w‖ (continuità della norma, limite lungo α → 0⁺) | OK |
| T4.2 | Φ lineare su un sottospazio: Lip(Φ) = ‖Φ‖; Φ illimitata ⇒ liminf L_α = ∞ ⇒ L_α → ∞ | OK |
| T4.3 | (2) Sσ(0) = 0, quindi S(σ(u)−σ(0)) = u − 0 = u: usa **solo** la linearità di S (e Sσ = id), non quella di σ | OK. **Domanda P2-T4(2):** corretto |
| T4.4 | ‖σ(u)−σ(0)‖ ≥ ‖S^†u‖ (preimmagine di norma minima, P2-C2(b)); Lip(σ) ≥ sup_u‖S^†u‖/‖u‖ = γ_N^{−1/2}, = ∞ se γ_N = 0 | OK (audit T4(2): selezione σ(u) = S^†u + (sin Σu + u₁²)k, k ∈ ker S; rapporto sull'autovettore di γ_N = 31.10 ≥ γ^{−1/2} = 31.06) |
| T4.5 | app. (i): (1) con V = Σℋ_j, Φ = σ dà Lip(σ) ≤ liminf L_α; (2) dà Lip(σ) ≥ γ_N^{−1/2}; con γ_N > 0 Tikhonov ha L_α = ‖R_α‖ ↑ γ_N^{−1/2} (P2-C2(c), monotonia C2.9) e R_αu → S^†u (P2-C2(d)) | OK. **Domanda (i):** la versione con selezioni esatte copre limiti non lineari (ℓ¹/MCA) **purché** la procedura soddisfi le ipotesi (R_α: H → W lipschitziana, R_αu → σ(u) ∀u ∈ Σℋ_j, σ selezione esatta). Che ℓ¹/MCA le soddisfino non è provato qui (nota **T4-a**, informativa: è già scritto come ipotesi) |

## 5. Micro-claim ed esiti — C12-P7(a),(c),(d) e gram.md §2bis
| MC | passo | esito |
|---|---|---|
| P7.1 | ℋ_j ⊆ ker_{H^m}P (Q_j \| P); ker_{H^m}P chiuso in H^m perché "P(∂): H^m → H^{m−deg P} continua" | OK nella sostanza; per m < deg P l'indice è negativo e H^{m−deg P}(Ω) va definito. Basta P(∂): H^m(Ω) → 𝒟′(Ω) continua (H^m ↪ L² ↪ 𝒟′, ∂ continua su 𝒟′) e il nucleo di una mappa continua in uno spazio di Hausdorff è chiuso → **P7-2** (MINOR) |
| P7.2 | (a) "⇐": somma chiusa e densa in ker_{H^m}P ⇒ uguale; "⇒": ovvia | OK. La riformulazione "ogni u ∈ ker_{H^m}P ha componenti u_j ∈ H^m" = "u ∈ Σℋ_j" (esiste **una** scomposizione in H^m) è corretta |
| P7.3 | "Le due condizioni sono indipendenti: in C12-C1 (m = 0) la somma è densa (P2-C1(a)) ma non chiusa" | **OVERSTATED (MINOR)**: è mostrata solo "densa ⇏ chiusa" (C12-C1 con m = 0: u ∈ L², componenti fuori da L², scomposizione unica, quindi ker ≠ Σ; densa per P2-C1(a) ⇒ non chiusa: corretto). "Chiusa ⇏ densa" non ha esempio (è il problema P2-Q1) → **P7-1** |
| P7.4 | (c) (ker S)^⊥ = \overline{im S*} invariante; inf della forma sulla sfera di (ker S)^⊥ = inf σ(S*S\|_{(ker S)^⊥}) = γ_N | OK |
| P7.5 | γ_N > 0 ⇒ immagine chiusa; immagine chiusa ⇒ mappa aperta ⇒ ‖Sω‖ ≥ c‖ω‖ su (ker S)^⊥ ⇒ γ_N ≥ c² | OK (= P2-C2(b), C2.5–C2.7) |
| P7.6 | ‖S^†u‖² ≤ γ_N^{−1}‖u‖², ottimale per definizione di inf | OK |
| P7.7 | convenzione γ_N := +∞ se (ker S)^⊥ = 0 (tutti gli ℋ_j nulli: somma {0} chiusa) | OK, coerente con P2-C2 (che esclude il caso "tutti nulli") |
| P7.8 | il valore di γ_N (e la costante γ_N^{−1}) dipende dal prodotto scalare scelto su H^m(Ω); la positività no (la chiusura è topologica) | **precisazione (MINOR)** → **P7-3**: fissare il prodotto scalare (quello di gram.md §1, Σ_{\|α\|≤m}⟨∂^αu,∂^αv⟩) |
| P7.9 | (d) G_ε di v_1 = (1,0,ε)/√(1+ε²), v_2, v_3 a ±120°: det G_ε = 3ε²/(4(1+ε²)) > 0, coseni 1/(2√(1+ε²)), 1/(2√(1+ε²)), ½; λ_min(G_ε) ~ ε²/3; ε = 0: {0, 3/2, 3/2} | OK (SymPy esatto per det e coseni; λ_min = 3.3076·10⁻³, 3.3331·10⁻⁵, 3.3333·10⁻⁷ per ε = 10⁻¹, 10⁻², 10⁻³: coincidono con gram.md §2bis) |
| P7.10 | blocchi ⊕_kℂ³ con ε_k → 0: intersezioni nulle; "il coseno di Friedrichs è il sup dei coseni dei blocchi"; S*S = ⊕G_{ε_k}, ker S = 0, γ_3 = inf_kλ_min = 0 | OK nella sostanza; il passo "c_F della somma = sup dei blocchi" è affermato senza la riga di prova (che è quella di C2.22) e serve ε_k > 0 per ogni k (ker G_{ε_k} = 0) → **P7-4** (MINOR) |
| P7.11 | "viceversa: ℋ_1, ℋ_2 con somma non chiusa e ℋ_3 = H" | OK; l'esistenza di ℋ_1, ℋ_2 con somma non chiusa va citata (C12-T3, corollario, o P2-C2(f) non necessità) → in **P7-4** |
| P7.12 | **Portata di (d)**: dichiarata esplicitamente "controesempio in uno spazio di Hilbert astratto, non un esempio di nuclei di operatori differenziali"; il caso differenziale è aperto (C12-Q2) | OK — **(d) è un esempio in Hilbert astratto e non va dichiarato per operatori differenziali**: il testo lo rispetta, anche in gram.md §2bis ("Esempio astratto … aperto (C12-Q2)") |
| P7.13 | coerenza con P2-C2: (c) = P2-C2(b) (stessa S, W, γ_N, stessa prova); (d) è una variante di P2-C2(f) | **coerente**. Le parametrizzazioni differiscono: in C12-P7(d) (S-CHECK-4) si inclina **una** retta, γ_3 ~ ε²/3; in P2-C2(f) si inclinano **tutte e tre**, γ_3 = 3sin²ε ~ 3ε². Entrambe verificate (audit §5 e §2 dello script): nessun conflitto; consiglio solo di non mescolare le due formule nei richiami |
| P7.14 | gram.md §2bis: "se le intersezioni a coppie sono nulle, γ_N ≥ 1−‖C‖ con C la matrice dei c_F a coppie" | coerente: è il caso particolare di P2-C2(e) (con intersezioni nulle c_ij = c_F). P2-C2(e) vale anche senza l'ipotesi (con c_ij = ‖P_iP_j‖), ma la frase di gram.md non è falsa |
| P7.15 | gram.md §0: "Norma di Aronszajn ‖·‖_K equivalente … ⟺ somma chiusa ⟺ γ_N > 0" | **non auditato** (C12-T5, fuori perimetro); la seconda equivalenza è P2-C2(b) |

## 6. Red team (Phase 1.5) — esiti
1. **γ_N = min forma su (ker S)^⊥ e σ(T) ⊆ {0} ∪ [γ_N, N]** su 7 famiglie (reali/complesse, N = 3…5, dim ker S = 0…3, con e senza ℋ_1∩ℋ_2 ≠ 0): OK. Nessun controesempio.
2. **Bound γ_N ≥ 1−‖C‖** (richiesto dal coordinatore): vale su tutte le famiglie (sopra e sotto 1, con intersezioni non nulle ‖C‖ ≥ 1 e bound banale); con ‖C‖ = 0.994 < 1: ker S = 0 e γ = 0.30 ≥ 0.006; per N = 2, ℐ = 0, uguaglianza γ_2 = 1−c_F. Il bound non è stretto per N ≥ 3 (nelle due terne di (f) ‖C‖ = 1 e γ_3 = ½, 3/2).
3. **γ_3 = 1/2 vs 3/2 con tutti i coseni 1/2** (richiesto dal coordinatore): confermato in aritmetica esatta, con realizzazioni esplicite (120° in ℝ²; Cholesky in ℝ³).
4. **"Densa ma non chiusa"** (richiesto dal coordinatore): troncate K = 3, 6, 10 dell'esempio (f): c_F a coppie ≤ ½, ker S = 0, γ_3 = 3sin²(2^{−K}) → 0, rank S = dim H (ogni blocco suriettivo). Nella versione infinita: densità per supporti finiti, non chiusura per (b). Confermato.
5. **Non necessità**: γ_2 = 1−cos 2^{−K} → 0, SS* ≥ I, γ_3 ≥ 1 sulle troncate.
6. **(c), γ = 0**: ‖R_{λ_K}‖ ≥ 1/(2√λ_K) (4.6, 73.9, 1182 per K = 4, 8, 12).
7. **P2-T4(2) con selezione non lineare**: tentativo di violare Lip(σ) ≥ ‖S^†‖ con σ = S^† + φ(u)k, φ non lineare: nessuna violazione (2000 campioni + autovettore di γ_N).
8. Tentativo "(e) falsa con intersezioni non nulle": impossibile, c_ij = 1 ⇒ bound ≤ 0.

## 7. Fix
### C2-1 — dipendenze dichiarate (MINOR; UNCLEAR + COSMETIC; strategia ADD_REFERENCE)
**Prima:** "Nessuna dipendenza da P2-T3: la prova è autonoma." **Problema:** (e) (uguaglianza per N = 2) e (f) (chiusura delle somme a coppie, non chiusura di ℋ_1+ℋ_2) citano P2-T3(b). **Dopo:** "Dipendenze: … P2-T3(b) (DIMOSTRATO) solo per l'uguaglianza N = 2 in (e) e per le somme a coppie in (f); (a)–(d) e la stima di (e) sono autonome." In alternativa, (f) diventa autonoma così: chiusura a coppie da (e) con N = 2 (‖C‖ = c_F ≤ ½ < 1); non chiusura di ℋ_1+ℋ_2 da (b): ker S = 0 (ℋ_1∩ℋ_2 = 0) e ω_k = (e₁^{(k)}, −(cos θ_k, sin θ_k)^{(k)}) ha ‖Sω_k‖²/‖ω_k‖² = 1 − cos θ_k → 0, quindi γ_2 = 0.
### C2-2 — "γ_3 ≥ 1" nella non necessità (MINOR; UNJUSTIFIED + COSMETIC; ADD_DERIVATION)
**Prima:** "blocco per blocco VVᵀ = aaᵀ+bbᵀ+I ≥ I, quindi γ_3 ≥ 1". **Problema:** VVᵀ = SS* agisce su H, γ_3 è definito da S*S su (ker S)^⊥ (qui ker S ≠ 0). **Dopo:** "ℋ_1+ℋ_2+ℋ_3 = H è chiuso, quindi γ_3 > 0 per (b). Inoltre SS* = P_{ℋ_1}+P_{ℋ_2}+I ≥ I (in ogni blocco aaᵀ+bbᵀ+I), e σ(S*S)∖{0} = σ(SS*)∖{0} (fatto standard σ(AB)∪{0} = σ(BA)∪{0}); poiché γ_3 ∈ σ(S*S) e γ_3 ≠ 0, γ_3 ∈ σ(SS*) ⊆ [1, ∞), cioè γ_3 ≥ 1." Oppure eliminare la frase: la chiusura della tripla è banale.
### P7-1 — "indipendenti" in C12-P7(a) (MINOR; OVERSTATED + LOCAL; WEAKEN_CLAIM)
**Dopo:** "La densità non implica la chiusura: in C12-C1 (m = 0) la somma è densa (P2-C1(a)) ma non chiusa. Se la chiusura possa valere senza densità (somma chiusa propria in ker_{H^m}P) è aperto (P2-Q1)."
### P7-2 — chiusura di ker_{H^m}P (MINOR; UNCLEAR + COSMETIC; ADD_DERIVATION)
**Dopo:** "ker_{H^m}P è chiuso in H^m: P(∂): H^m(Ω) → 𝒟′(Ω) è continua (H^m ↪ L²_loc ↪ 𝒟′ e ∂ è continua su 𝒟′)." (Oppure definire H^{m−deg P}(Ω) per indice negativo come in §1, se lì è definito.)
### P7-3 — dipendenza di γ_N dal prodotto scalare (MINOR; UNCLEAR + COSMETIC; precisazione)
**Dopo (in (c) o nelle ipotesi):** "H^m(Ω) con il prodotto scalare ⟨u,v⟩_{H^m} = Σ_{|α|≤m}⟨∂^αu,∂^αv⟩_{L²}; il valore di γ_N e la costante γ_N^{−1} dipendono da questa scelta, la condizione γ_N > 0 no (è equivalente alla chiusura, proprietà topologica)."
### P7-4 — dettagli di (d) (MINOR; UNJUSTIFIED + COSMETIC; ADD_DERIVATION)
**Dopo:** "ε_k > 0, ε_k → 0. Per a = (s_kv_i^{(k)})_k, b = (t_kv_j^{(k)})_k unitari, |⟨a,b⟩| = |Σ_ks_k\bar t_k⟨v_i^{(k)},v_j^{(k)}⟩| ≤ sup_k|⟨v_i^{(k)},v_j^{(k)}⟩| (Cauchy–Schwarz in ℓ²), con uguaglianza approssimata su un solo blocco: c_F = sup_k dei coseni ≤ ½ < 1." E per il "viceversa": "ℋ_1, ℋ_2 con somma non chiusa esistono (C12-T3, corollario; o P2-C2(f), non necessità)."
### T4-a — (informativa, nessun fix richiesto)
L'applicazione (i) è un'implicazione: per ℓ¹/MCA restano da verificare lipschitzianità di R_α e convergenza puntuale a una selezione esatta.

## 8. Risposte alle 9 domande della CHECK_REQUEST_2 (sintesi)
1. (a)/(b): sì, γ_N = min σ(T|_{(ker S)^⊥}) = inf della forma; σ(T) ⊆ {0} ∪ [γ_N, ‖S‖²] senza ipotesi su dim ker S (C2.3–C2.4).
2. (c): sì, uso corretto, come P2-T3(c) (C2.10).
3. (d): sì, ipotesi di P2-T1 soddisfatte (C2.13).
4. (e): stima e identificazione corrette; con intersezione non nulla la (e) resta vera (banale) (C2.15–C2.18).
5. (f) non sufficienza: riduzione a blocchi completa; conti corretti (C2.20–C2.25).
6. (f) non necessità: controesempio valido (C2.26); fix C2-2 sul passo "γ_3 ≥ 1".
7. (f) Gram ±½: sì, realizzate, γ_3 = ½ e 3/2 (C2.28).
8. P2-T4(2): solo linearità di S; (i) copre limiti non lineari sotto le ipotesi dichiarate (T4.3–T4.5).
9. (Esito atteso) verdetti in §0.

## 8bis. Kill-argument
Non eseguito (lasciato al giudizio del revisore da S-P2, inbox/S-CHECK.md 26/10). Motivo: P2-C2 è analisi funzionale elementare (teorema spettrale + mappa aperta) controllata passo per passo, senza passi asintotici né fonti esterne non verificate; i controesempi di (f) e C12-P7(d) sono verificati in aritmetica esatta. Il punto di G★′ su cui un attacco avrebbe presa — se γ_N > 0 valga per nuclei di P concreti con N ≥ 3 — non è affermato da nessun claim auditato (P2-Q2, C12-Q2 APERTI). Se il coordinatore lo ritiene necessario per il Gate 3, il bersaglio naturale è la *formulazione* di G★′ punto 2 con γ_N, non P2-C2.

## 9. Giudizio (scientific-critical-thinking)
Mostrato: il criterio γ_N > 0 per la chiusura di Σℋ_j, con costanti ottimali e Tikhonov, per N qualsiasi in un Hilbert qualsiasi; la condizione sufficiente 1−‖C‖; tre controesempi astratti verificati in aritmetica esatta. Non mostrato (e correttamente non affermato): un caso di nuclei di operatori differenziali con N ≥ 3 in cui le somme a coppie sono chiuse e la tripla no (C12-Q2); la densità in ker_{H^m}P in generale (P2-Q1); il calcolo di γ_N per un P concreto a ≥ 3 fattori (P2-Q2). Lo stato DIMOSTRATO è proporzionato per gli enunciati come scritti, con i fix MINOR.
