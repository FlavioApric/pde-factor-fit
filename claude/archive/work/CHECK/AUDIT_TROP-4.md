# AUDIT TROP-4 — nessuna stima uniforme sulle facce conservative
Revisore: S-CHECK · 25/10/2026 · richiesta: central per S-TROP (inbox/S-CHECK.md).
Fonte esaminata: SOLO enunciato, ipotesi e prova in `work/SCOUT-TROP/VERDETTO.md` §Risultati, TROP-4.
Skill: session-protocol, claim-lifecycle, proof-checker, scientific-critical-thinking, sympy. SymPy: `work/CHECK/sympy/audit_trop.py` (controlli 3–4) → `audit_trop.out`, **OK**.

## 1. Enunciato canonico
Notazione di AUDIT_TROP-3 §1. **(TROP-4)** Se Re τ = Re τ_F = 0 su B e δ ≠ 0 q.o. su B (quindi δ = iφ, φ reale, φ ≠ 0 q.o.), allora (1/T)∫_0^T ‖E_B(t)‖² dt → 2‖1_Bû₀‖² per T → ∞.
**Affermazioni collegate:** (a) si applica a entrambe le bande di KG; (b) nella banda di trasporto di AD, A = {|κ| < κ*}, ‖E_A(t)‖ → ‖1_{A∖0}û₀‖ mentre ‖u(t)‖ → 0, quindi l'errore relativo → ∞.

## 2. Micro-claim
| MC | Passo | Esito |
|---|---|---|
| MC-1 | |e^{tτ} − e^{tτ_F}|² = |e^{itφ} − 1|² = 2 − 2cos(tφ) | corretto (|e^{tτ_F}| = 1) |
| MC-2 | (1/T)∫_0^T (2 − 2cos tφ) dt = 2 − 2 sin(Tφ)/(Tφ) | corretto (controllo 3a) |
| MC-3 | scambio ∫_0^T e ∫_B (Tonelli, integrando ≥ 0) e limite T → ∞ sotto ∫_B | corretto: integrando ≤ 4|û₀|² ∈ L¹, convergenza q.o. perché φ ≠ 0 q.o. (convergenza dominata) — **non scritto nella prova**, va aggiunto (MINOR) |
| MC-4 | conclusione "nessuna stima uniforme" | corretto: se ‖E_B(t)‖ ≤ ε‖1_Bû₀‖ per ogni t, la media sarebbe ≤ ε², quindi ε ≥ √2 (controllo 4) |

## 3. Problemi
- **I-1 · ILLEGAL_INTERCHANGE (non giustificato) · UNJUSTIFIED/LOCAL · MINOR.** Mancano Tonelli e la convergenza dominata in MC-3. *Fix:* ADD_DERIVATION (una riga, sopra).
- **I-2 · HIDDEN_ASSUMPTION per KG · UNCLEAR/LOCAL · MINOR.** KG è del 2° ordine in t: u = e^{itω}a₊ + e^{−itω}a₋. TROP-4 si applica **ramo per ramo** (o nella norma d'energia che li separa); per la norma L² della soluzione intera compaiono termini incrociati. *Fix:* enunciare per ciascun ramo ±ω, con τ = ±iω, τ_F = ±i|κ| (banda d'onda) o ±im (banda d'oscillatore); δ ≠ 0 per ogni κ se m ≠ 0, quindi l'ipotesi vale.
- **I-3 · affermazione (b) fuori dalle ipotesi di TROP-4 · UNCLEAR/LOCAL · MINOR.** Nella banda di trasporto di AD Re τ = −Dκ² ≠ 0, quindi (b) non è un caso di TROP-4 ma un fatto a parte. È corretto: |e^{−Dκ²t} − 1| → 1 per κ ≠ 0 e |e^{tτ}| → 0, convergenza dominata (controllo 4c di S-TROP; ricontrollato a mano). Notare che 1_{A∖0} e 1_A danno la stessa norma ({0} ha misura nulla). *Fix:* separare (b) come TROP-4b.
Nessun FATAL/CRITICAL.

## 4. Red team
Tentato: φ con zeri su un insieme di misura positiva (es. bande dove τ = τ_F): allora il limite è 2‖1_{B∖{φ=0}}û₀‖², cioè l'ipotesi "δ ≠ 0 q.o." è necessaria e la forma generale è 2‖1_{B∩{φ≠0}}û₀‖². Nessun controesempio alla forma enunciata.

## 5. Stato proposto
**TROP-4: DIMOSTRATO** (dopo I-1, prova completata qui). **TROP-4 per KG: DIMOSTRATO ramo per ramo** (I-2). **TROP-4b (banda di trasporto di AD): DIMOSTRATO** come enunciato separato. Kill-argument: non richiesto.
