# AUDIT R4-T5 — identificabilità per P ridotto (Ann(u) = (P) ⟺ V(Ann u) = V(P), soglia di Bézout)
Revisore: S-CHECK · 25/10/2026
Fonte esaminata: SOLO enunciato, ipotesi e prova di `research/R4/REPORT.md` §2, [R4-T5] (più la definizione di Z(u) data lì).
Skill caricate: session-protocol, claim-lifecycle, proof-checker (io sono il reviewer), scientific-critical-thinking, sympy.
SymPy: `work/CHECK/sympy/audit_r4t5.py` → `audit_r4t5.out`, **ESITO GLOBALE: OK** (9 controlli).

## 1. Enunciato canonico (Phase 0.5)
R = ℂ[τ,ξ] (τ ↔ ∂_t, ξ ↔ ∂_x). I ⊂ ℝ intervallo, 𝕋 = ℝ/2πℤ.
**Ipotesi (da rendere esplicite):** (H1) u ∈ D'(I×𝕋) (o C^∞); (H2) **Pu = 0** (nel report è implicita); (H3) P monico in τ di grado m ≥ 1; (H4, solo per (b)–(c)) P ridotto, P = P₁⋯P_r con P_i irriducibili distinti.
Definizioni: v_κ := û(·,κ) ∈ D'(I); per (H2)–(H3) v_κ risolve l'ODE P(∂_t,iκ)v_κ = 0 di ordine m, quindi è un esponenziale-polinomio; p_κ := annullatore minimo di v_κ (p_κ | P(·,iκ)); Z(u) := {(τ,iκ) : κ ∈ ℤ, p_κ(τ) = 0} ⊆ V(P).
- (a) Ann(u) = {Q ∈ R : p_κ | Q(·,iκ) ∀κ ∈ ℤ}.
- (b) Ann(u) = (P) ⟺ V(Ann u) = V(P) ⟺ ∀i: |Z(u) ∩ V(P_i)| = ∞.
- (c) ∀n ∈ ℕ: se ∀i |Z(u) ∩ V(P_i)| > n·deg P_i, allora ∀Q con deg Q ≤ n e Qu = 0: P | Q.

## 2. Dipendenze
(a) ← serie di Fourier in x su D'(I×𝕋) (∂_x agisce come iκ sul modo κ). (b) ← (a) + Nullstellensatz + irriducibilità delle curve V(P_i). (c) ← (a) + Bézout affine (|V(F)∩V(G)| ≤ deg F·deg G per F, G coprimi). Nessun ciclo. Nessuna fonte esterna oltre ai classici (Hilbert, Fulton).

## 3. Micro-claim e verifica
| MC | Passo | Esito |
|---|---|---|
| MC-1 | Qu = 0 ⟺ ∀κ Q(∂_t,iκ)v_κ = 0 ⟺ p_κ | Q(·,iκ) | corretto (H1) |
| MC-2 | (P) ⊆ Ann(u) | corretto, **usa (H2)** |
| MC-3 | Z ⊆ V(Ann u) | corretto: p_κ | Q(·,iκ) ⇒ Q(z) = 0 per z ∈ Z |
| MC-4 | V(Ann u) = Z̄ (chiusura di Zariski) | **non scritto nel report.** Vero: per Q ∈ I(Z), Q^m(·,iκ) è divisibile per p_κ (le molteplicità delle radici di p_κ sono ≤ m), quindi Q^m ∈ Ann(u) e √Ann(u) = I(Z). (ADD_DERIVATION) |
| MC-5 | V(Ann u) = V(P), P ridotto ⇒ Ann(u) = (P) | corretto: (P) ⊆ Ann(u) ⊆ √Ann(u) = I(V(P)) = (P) |
| MC-6 | Z̄ = V(P) ⟺ ogni Z∩V(P_i) è infinito | corretto: V(P_i) curva irriducibile, i suoi chiusi propri sono finiti; per (H3) ogni P_i ha grado positivo in τ, quindi V(P_i) è infinito e V(P_i) ⊄ V(P_j) per i≠j |
| MC-7 | (b ⇒) testimone "(P/P_i)·∏ℓ_z ∈ Ann(u)∖(P)" | **lacuna**, vedi I-2 |
| MC-8 | (c) Bézout | corretto: se P_i ∤ Q, Q e P_i coprimi, |V(Q)∩V(P_i)| ≤ n·deg P_i, contraddizione; P_i distinti primi ⇒ P | Q |

## 4. Problemi trovati
- **I-1 · HIDDEN_ASSUMPTION · UNCLEAR/LOCAL · MINOR.** Pu = 0 e u ∈ D'(I×𝕋) non compaiono nell'enunciato. *Fix:* STRENGTHEN_ASSUMPTION testuale (H1, H2).
- **I-2 · UNPROVEN_SUBCLAIM · UNJUSTIFIED/LOCAL · MAJOR (chiuso qui).** Il testimone di (b ⇒) non è specificato: se ℓ_z è una forma lineare in τ (τ−τ_z) può coincidere con P_i (quando P_i = τ − c) e dare Q = P ∈ (P) (controllo 2); con forme lineari generiche resta il problema delle molteplicità nei punti V(P_i)∩V(P_j). **Testimone corretto (ADD_DERIVATION):** sia K_i := {κ : Z ∩ V(P_i) ha un punto sopra ξ = iκ}, finito per ipotesi; Q := (P/P_i)·∏_{κ∈K_i}(ξ − iκ). Per κ ∈ K_i, Q(·,iκ) ≡ 0; per κ ∉ K_i, p_κ non ha radici in comune con P_i(·,iκ), e da p_κ | (P/P_i)(·,iκ)·P_i(·,iκ) segue p_κ | (P/P_i)(·,iκ). Quindi Q ∈ Ann(u). Q ∉ (P): P_i è primo, P_i ∤ P/P_i (P ridotto) e P_i ∤ (ξ−iκ) (P_i ha grado positivo in τ). ∎ Verificato su P = τ(τ−ξ²), u = calore (7 modi) + cos x + 3cos 2x: Q = (τ−ξ²)ξ(ξ²+1)(ξ²+4) annulla u e non è multiplo di P (controllo 1).
- **I-3 · UNPROVEN_SUBCLAIM · MINOR.** MC-4 (V(Ann u) = Z̄) è usato implicitamente in "V(Ann u) = V(P) ⟺ Z∩V(P_i) infinito". Per la direzione ⇐ basta MC-3; per ⇒ serve MC-4 oppure il testimone di I-2 (che lo rende superfluo). Il commento "κ con radici multiple in numero finito" non è necessario.
- **I-4 · SCOPE_OVERCLAIM rispetto a H0 = ℝ · OVERSTATED/GLOBAL · MAJOR.** T5 è dimostrato su I×𝕋 (modi di Fourier discreti). La decisione del Gate 1 è H0 = ℝ, Ω limitato. Su Ω ⊂ ℝ² limitato:
  - **si trasferisce senza cambiamenti** la parte algebrica MC-5: per u ∈ D'(Ω) con Pu = 0 e P ridotto, Ann(u) = (P) ⟺ V(Ann u) = V(P) (solo Nullstellensatz), e la parte (c) se si sostituisce Z(u) con un qualunque insieme di punti su cui Ann(u) si annulla;
  - **non si trasferisce** la caratterizzazione con Z(u): manca una decomposizione in modi discreti; la versione "supporto della misura di Ehrenpreis" è falsa (R4-C2: u ≡ 1 come integrale su |ξ|=1 ha supporto Zariski-denso in V(τ) ma Ann(u) = (τ,ξ)); e per u esponenziale-polinomio finito Ann(u) è sempre 0-dimensionale, quindi mai = (P).
  Questo è esattamente il compito G9 di S-C3; qui va solo registrato che la versione su ℝ è APERTA.
- **I-5 · Necessità delle ipotesi (non errori, da scrivere nell'enunciato).** (H3) monico: per P = ξτ il modo κ = 0 è arbitrario in t (u = t³+1 risolve Pu = 0), Z non è definito (controllo 4); basta "coefficiente direttore in τ senza zeri su iℤ". (H4) ridotto: con P₂² l'ideale (P₂², ξP₂) ha V = V(P₂) ma P₂ ∉ I (controllo 5) — coerente con "aperto per P non ridotto (Q2)". (c) disuguaglianza **stretta**: calore, n = 2, modi κ = ±1, ±2 (|Z| = 4 = n·deg P) ⇒ Q = τ²+5τ+4 = (τ+1)(τ+4) di grado 2 annulla u e non è multiplo di P; con un modo in più (|Z| = 6) restano solo i multipli di P (controllo 3). La soglia di Bézout è quindi raggiunta: non è migliorabile in generale.
Nessun FATAL; nessun CRITICAL dopo il fix di I-2.

## 5. Red team (Phase 1.5)
Controesempi cercati a (a), (b), (c) nella forma corretta: nessuno trovato (controlli 1, 3). Controesempi alle ipotesi tolte: trovati e verificati per (H3), (H4) e per la stretta disuguaglianza in (c) (controlli 3–5). Controesempio "candidato" al testimone di R4: verificato (controllo 2).

## 6. Acceptance gate e stato proposto
Gate su 𝕋: 0 FATAL/CRITICAL dopo I-2 ✔; ipotesi esplicite dopo I-1 ✔; ogni applicazione (Nullstellensatz, Bézout) con ipotesi scaricate ✔; controesempi tentati ✔.
**Stato proposto:**
- **R4-T5[𝕋]** (enunciato del §1 con H1–H4 e il testimone di I-2): **DIMOSTRATO**.
- **R4-T5[alg]** (Ω qualunque, Pu = 0, P ridotto: Ann(u) = (P) ⟺ V(Ann u) = V(P)): **DIMOSTRATO** (Nullstellensatz).
- **R4-T5[ℝ]** (caratterizzazione di V(Ann u) da u su Ω limitato ⊂ ℝ², G9): **APERTO** — a S-C3. Non usare R4-T5 come "dimostrato su ℝ" in Fase 3.
Kill-argument: **sì, richiesto** quando S-C3 consegna la versione su ℝ (cammino critico: identificazione).
