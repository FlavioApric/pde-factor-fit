# AUDIT TROP-3 — stima uniforme in t di E_B sulle facce dissipative
Revisore: S-CHECK · 25/10/2026 · richiesta: central per S-TROP (inbox/S-CHECK.md).
Fonte esaminata: SOLO enunciato, ipotesi e prova in `work/SCOUT-TROP/VERDETTO.md` §Risultati, TROP-3 (con la notazione d'intestazione: B, τ_F, δ, E_B).
Skill: session-protocol, claim-lifecycle, proof-checker (io sono il reviewer), scientific-critical-thinking, sympy. SymPy: `work/CHECK/sympy/audit_trop.py` → `audit_trop.out`, **ESITO GLOBALE: OK**.

## 1. Enunciato canonico
u_t = a(∂_x)u su ℝ, simbolo τ(κ) = a(iκ); B ⊆ ℝ misurabile (banda); τ_F forma iniziale (monomio dominante) su B; δ := τ − τ_F; u₀ ∈ L²(ℝ); E_B(t) := F⁻¹[1_B(e^{tτ} − e^{tτ_F})û₀].
**(TROP-3, come scritto)** Se ∃α > 0 con Re τ_F ≤ −α su B e Re δ ≤ 0 su B, allora ∀t ≥ 0: ‖E_B(t)‖_{L²} ≤ (sup_B|δ|)/(eα) · ‖1_Bû₀‖.
**Corollario dichiarato:** per la banda diffusiva di AD (τ = −icκ − Dκ², τ_F = −Dκ², κ* = c/D) "il fattore vale κ*/(e|κ|)", γ = 1, ε = 1/Pe_κ, costante 1/e asintoticamente ottimale.

## 2. Micro-claim
| MC | Passo | Esito |
|---|---|---|
| MC-1 | e^{tτ} − e^{tτ_F} = e^{tτ_F}(e^{tδ} − 1) | corretto |
| MC-2 | |e^z − 1| ≤ |z| per Re z ≤ 0 | corretto: e^z − 1 = ∫_0^1 z e^{sz} ds, |e^{sz}| ≤ 1 |
| MC-3 | |e^{tτ_F}| ≤ e^{−αt}, sup_t t e^{−αt} = 1/(eα) | corretto |
| MC-4 | Plancherel: ‖E_B(t)‖ ≤ ‖sup_t|…| · 1_Bû₀‖ | corretto (stessa normalizzazione di Fourier per u e E_B) |

## 3. Problemi
- **I-1 · REFERENCE/APPLICATION MISMATCH (enunciato ≠ uso) · OVERSTATED/LOCAL · MAJOR.** Sulla banda diffusiva di AD, B = {|κ| > κ*}, si ha sup_B|δ| = sup c|κ| = +∞: la stima **come è scritta** è vacua (controllo 1). Il "fattore κ*/(e|κ|)" viene dalla versione **puntuale**, che la stessa prova dimostra ma che non è l'enunciato:
  **TROP-3′ (proposta, stessa prova).** Se Re τ_F(κ) < 0 e Re δ(κ) ≤ 0 per q.o. κ ∈ B, allora ∀t ≥ 0: |e^{tτ} − e^{tτ_F}| ≤ ρ(κ) := |δ(κ)|/(e·|Re τ_F(κ)|), e quindi sup_{t≥0}‖E_B(t)‖ ≤ ‖ρ 1_Bû₀‖ ≤ (sup_B ρ)·‖1_Bû₀‖.
  Per AD ρ(κ) = κ*/(e|κ|) (controllo 2a); il bound puntuale è rispettato e il rapporto sup_t/ρ → 1 per |κ| → ∞ (1/e asintoticamente ottimale: controllo 2b, rapporti 0.962 → 1.000 per κ/κ* = 1…50).
- **I-2 · SCOPE · UNCLEAR/LOCAL · MINOR.** "ε = 1/Pe_κ" è un fattore **per frequenza**. Una stima uniforme sulla banda B = {|κ| > K} ha costante κ*/(eK); sulla banda che parte da κ* vale 1/e, cioè non è piccola (controllo 2c). Va detto che ε piccolo richiede K ≫ κ* (o dati con 1_Bû₀ concentrato ad alte frequenze).
- **I-3 · SCOPE rispetto a H0/H1 · MINOR.** La stima è su ℝ con u₀ ∈ L²(ℝ) (Plancherel); su Ω limitato non vale nella stessa forma (lo dice TROP-7). Da scrivere nell'enunciato.
- **I-4 · ipotesi Re δ ≤ 0 · osservazione.** Si può indebolire a Re δ ≤ (1−η)|Re τ_F| (η ∈ (0,1]) con ρ = |δ|/(eη|Re τ_F|) (stessa prova con |e^z − 1| ≤ |z|e^{max(Re z,0)}). Non necessario per AD.
Nessun FATAL/CRITICAL.

## 4. Red team
Controesempio all'uso letterale: banda illimitata con δ illimitato (AD) — trovato (I-1). Controesempi alla versione puntuale: nessuno (griglia κ/κ* ∈ [1,50]; la prova è comunque generale). Ipotesi Re τ_F < 0 necessaria: senza dissipazione si cade in TROP-4 (nessuna stima con ε < √2).

## 5. Stato proposto
**TROP-3 (come scritto): DIMOSTRATO** (corretto ma vacuo sulle bande illimitate). **TROP-3′ (versione puntuale) + corollario AD: DIMOSTRATO** dopo la riscrittura di I-1 e la precisazione di I-2. Su Ω limitato: non applicabile. Kill-argument: non richiesto (S-TROP propone il merge in RT-2; non è sul cammino critico).
