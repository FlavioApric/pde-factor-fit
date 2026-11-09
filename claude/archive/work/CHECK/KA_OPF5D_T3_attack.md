# KA OPF5D-T3+L6 — memo d'attacco (subagente fresco, 26/10/2026; input KA_OPF5D_T3_input.md)

**Esito: non sono riuscito a rompere la catena L3–L8 ⇒ T3. Nessuna obiezione FATALE né MAJOR. La più forte obiezione residua è MINOR.**

Ho attaccato tutti i punti indicati. (a) Continuità in k = 0: L3(ii) regge, perché |∂_kD_k(s)| ≤ s² e v ∈ 𝒮 rendono sommabile la serie di Volterra derivata (un fattore (|y|+|x|)² per ogni termine, con decadimento fattoriale). In L5(i), con w(0) = 0, la regolarità C¹ sul semipiano chiuso dà w(k) = w′(0)k + o(|k|) con w′(0) complesso (∂_{k̄}w = 0 si estende per continuità al bordo). Quindi |w′(0)| ≥ 2 e |w| ≥ |k| valgono sul semidisco chiuso, e T(0) = 2i/w′(0). Le due definizioni di Ψ coincidono su ℝ∖0 e sono entrambe continue fino a 0, quindi Ψ è continua anche in 0. (b) Ho ricontrollato la semplicità degli zeri (L4): (W(ψ_−, ψ̇_+))′ = −2kψ_−ψ_+, ψ_± sono reali in iκ e γ ∈ ℝ∖0. (c) Ho verificato 𝔅(−k) = Π(k + iκ_j)/(k − iκ_j), da cui |Ψ| ≤ C_xΠ(|k| + κ_j) nel semipiano inferiore. (d) Il coefficiente direttore è (−i)^N·(−1)^N(−i)^N = 1. La trasposta senza coniugio è corretta perché LA = AL_0 è un'identità algebrica e L, L_0 sono simmetrici. (e) I K_n[v] sono reali e α_N = 1, quindi d* ∈ ℝ^{N+1} con d*_N ≠ 0. Ho controllato a mano la segnatura sul solitone v = 2κ²sech²(κx): −v″ − 3v² + 4κ²v = 0. Anche L7 (ordine m+1 ≥ 1 ⇒ x_m′ = 0) e L8 (Σd_na_n costante → 0) reggono.

**Obiezione residua (MINOR).** In T3 il passaggio «R ≡ 0, cioè b ≡ 0» ricava b ≡ 0 solo su (0,∞), perché Λ e R sono definiti per k > 0. L6, invece, richiede b ≡ 0 su ℝ∖0 e usa proprio b(−k) = 0 per k > 0 nell'identità ψ_−(−k) = a(−k)ψ_+(k). Manca la simmetria b(−k) = b̄(k), che vale per v reale perché ψ_±(−k) = ψ̄_±(k) per k reale. Si ripara in una riga, ma senza di essa l'aggancio T3 → L6 è incompleto così come è scritto. Altri difetti minori: la stima di L3(i) come è enunciata cresce in |x| e quindi non dà da sola l'uniformità in x ≥ x_0 invocata in L4 (serve la variante con (y − x) ≤ y per x ≥ 0). L'enunciato di T3 normalizza q_{d*} = Π(λ − 4κ_j²), mentre la prova ottiene 4^{−N}Π (basta riscalare). In L6 il simbolo κ := −k collide con κ_j.

## Punti atomici
- T3, prova, riga 49: «R ≡ 0, cioè b ≡ 0» copre solo k > 0; manca b(−k) = b̄(k) (v reale) per il caso k < 0 usato in L6 (MINOR).
- L6, prova, riga 37: «ψ_−(−k) = a(−k)ψ_+(k) (b = 0)» usa b(−k) = 0, che dipende dal punto precedente (MINOR).
- L4, prova, riga 29: «stime di Cauchy … uniformi in x ≥ x_0» non segue dalla stima di L3(i) come è enunciata, che cresce con |x|; serve (y − x) ≤ y per x ≥ 0 (MINOR).
- T3, enunciato riga 48 contro prova riga 49: q_{d*} = Π(λ − 4κ_j²) contro 4^{−N}Π; si risolve riscalando (MINOR, cosmetico).
- L3(ii), riga 25: la convergenza uniforme della serie derivata è solo abbozzata (manca il conteggio n·C^{n−1}/(n−1)!); è corretta (MINOR, di presentazione).
- L6, riga 37: la notazione κ := −k collide con κ_j (cosmetico).
