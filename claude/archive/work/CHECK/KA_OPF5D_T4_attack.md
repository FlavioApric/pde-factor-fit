# KA OPF5D-T4 — memo d'attacco (subagente fresco, 26/10/2026; input KA_OPF5D_T4_input.md)

**Esito: dopo un tentativo onesto NON riesco a rompere L10–L12/T4. Obiezione residua più forte: MINOR (enunciato falso in L10, non usato in modo essenziale).**

Ho verificato in modo indipendente i punti nevralgici. (1) Segno a n = 0: B_1 = iq, quindi T̃_0 = −iq = −T_0; Ṽ_0 = −(i/2)σ_3 e V_d|_{q=0} = −(i/2)Σd̃_n(2ζ)^nσ_3 = −(i/2)Ω̃_dσ_3, corretto. Il difetto di V_d ha componente (1,2) pari a −Σd̃_n2^nB_{n+1} = Σd_nT_n: l'equivalenza iniziale regge. Il controllo sul 1-solitone (q = 2η sech 2ηx, ζ_1 = iη) dà q″ + 2q³ = 4η²q, coerente con Ω̃ ∝ ζ² + η² (con il vecchio Ω_d le radici sarebbero reali: R1 è necessario). (2) Poli: con det m = 1 si ha mσ_3m^{−1} = m_1⊗m_2^⊥ + m_2⊗m_1^⊥, **lineare in m_1**. Quindi l'ordine del polo è ≤ m_j (serve al (⇐)), e il coefficiente d'ordine −m_j è 2λw⊗w^⊥ ≠ 0, perché ψ_−^{(1)}(ζ_j) ≠ 0 è parallelo a ψ_+^{(2)}(ζ_j); questo vale anche per m_j ≥ 2. (3) L12 con M = 0 è corretta (parte diagonale di V_{0,x} − [Q,V_0]), e l'induzione si chiude. (4) Il (⇐) regge: V è intera, è O(|ζ|^M) perché m → I uniformemente, Liouville la rende polinomiale, e il limite x → +∞ con W_m → 0 (m ≥ 1, q ∈ 𝒮) fissa β_n = −i2^{n−1}d̃_n. Anche s = 0 torna (si ricava già dalla traccia nulla).

**Obiezione (MINOR).** L10 afferma che «ρ è continuo su ℝ», ma questo è falso. Controesempio: q = ½ sech x (reale, di Schwartz). Per ζ = 0 il sistema è una rotazione di angolo ∫q = π/2, quindi a(0) = cos(π/2) = 0 e b(0) = −1: ρ = b/a non è limitato vicino a 0 (singolarità spettrale reale, ammessa da |a|² + |b|² = 1). Di conseguenza anche la definizione di Λ_m ({ρ ≠ 0}) e il passo «ρ continuo ⇒ Ω̃ nullo su un aperto» del (⇒) sono formulati male. La riparazione è immediata: si usa b, che è continuo, e b(ξ)Ω̃_d(ξ) = 0. Inoltre una radice reale di a forza |b| = 1, quindi «ρ ≡ 0» ⟺ «b ≡ 0», e L11 (che suppone b ≡ 0) si applica. Questa equivalenza però non è scritta da nessuna parte. Infine, il passaggio a «INT-T2 con molteplicità» poggia su L9 per ZS e su (UC), che qui non sono dimostrati.

## Punti atomici
1. L10, enunciato, «b, ρ continui su ℝ»: falso per ρ quando a ha zeri reali (q = ½ sech x, a(0) = 0); va sostituito con b. MINOR.
2. T4, (⇒) caso ρ ≢ 0, «ρ continuo (L10) ⇒ Ω̃_d nullo su un aperto»: va giustificato con la continuità di b. MINOR.
3. Ipotesi comune, definizione di Λ_m, «{ξ : ρ(ξ) ≠ 0}»: non è definita dove a(ξ) = 0; va scritta come {b ≠ 0}. MINOR.
4. T4 caso ρ ≡ 0 contro L11 (ipotesi b ≡ 0): manca la frase «ρ ≡ 0 ⇒ b ≡ 0 (uno zero reale di a forza |b| = 1)». MINOR.
5. T4, ultima frase dell'enunciato: «INT-T2» dipende da L9 per ZS e da (UC), che non sono provati nell'input. MINOR (fuori bersaglio).
6. L10, prova «Dimensione 1»: l'argomento è solo abbozzato (manca il Wronskiano costante ≠ 0 contro il decadimento di due soluzioni). MINOR.
