# AUDIT R5-T2 — E_int nel caso commutante e complessità
Revisore: S-CHECK · 25/10/2026
Fonte esaminata: SOLO enunciato, ipotesi e prova di `research/R5/REPORT.md` §2, [R5-T2] (con la definizione R5-D1(a) e l'enunciato di R5-T1 che la prova usa).
Skill caricate: session-protocol, claim-lifecycle, proof-checker (io sono il reviewer), scientific-critical-thinking, sympy.
SymPy: `work/CHECK/sympy/audit_r5t2.py` → `audit_r5t2.out`, **ESITO GLOBALE: OK** (13 controlli).

## 1. Enunciato canonico (Phase 0.5)
Spazio di Banach X; A_1,…,A_N generatori di C0-semigruppi S_n(t) = e^{tA_n} **a due a due commutanti come semigruppi** (S_m(s)S_n(t) = S_n(t)S_m(s)); A := chiusura di ΣA_n su ∩D(A_n) (genera S(t) = S_1(t)⋯S_N(t) per R5-T1); u(t) := S(t)u₀.
- (i) ∀t ≥ 0: u(t) = Σ_{S⊆[N]} Π_{n∈S}(S_n(t)−I)u₀; quindi E_int^add(t) = Σ_{|S|≥2} Π_{n∈S}(S_n(t)−I)u₀.
- (ii) Coeff. costanti su ℝ o 𝕋 (moltiplicatori di Fourier): Ê_int(t,κ) = [Π(1+z_n)−1−Σz_n]û₀ = Σ_{k≥2}e_k(z)û₀, z_n = e^{t a_n(iκ)}−1.
- (iii) Complessità, per ogni κ fissato e dati z_1…z_N, in operazioni aritmetiche su ℂ: il valore Ê_int(t,κ) costa O(N); tutti gli aggregati per ordine e_k(z)û₀, k = 2…N, costano O(N²).
- (iv) "B2 'O(eⁿ)' è FALSO nel caso commutante".

## 2. Dipendenze
(i) ← R5-T1 (CON-FONTE: Engel–Nagel 2000, numerazione §II.2.7 da verificare) + espansione di un prodotto di operatori commutanti. (ii) ← (i) + diagonalizzazione di Fourier. (iii) ← (ii) + algoritmo standard dei coefficienti di Π(1+λz_n). (iv) ← (iii) + lettura di B2.

## 3. Micro-claim e verifica
| MC | Passo | Esito |
|---|---|---|
| MC-1 | S = Π S_n | corretto **se** vale R5-T1 e se la soluzione u è quella del semigruppo (I-2) |
| MC-2 | Π(I + (S_n−I)) = Σ_S Π_{n∈S}(S_n−I) | corretto: gli S_n−I commutano, espansione di un prodotto finito; verificato con matrici commutanti N = 3 e fallisce con matrici non commutanti (controlli 2–3) |
| MC-3 | i termini |S| = 0, 1 sono u₀ e (u_n − u₀) | corretto, coerente con R5-D1(a) |
| MC-4 | forma di Fourier e Σ_{k≥2} e_k | corretto; numero di monomi 2^N−N−1 per N = 2…6 (controllo 1) |
| MC-5 | O(N) per il valore, O(N²) per gli e_k | corretto nel modello aritmetico (N moltiplicazioni; N aggiornamenti da O(N)); confronto con forza bruta per N = 7 (controllo 4) |

## 4. Problemi trovati
- **I-1 · HIDDEN_ASSUMPTION · UNDERSTATED/LOCAL · MAJOR.** "Termini a due a due commutanti" va letto come **commutazione dei semigruppi (o dei risolventi)**, non come commutazione formale A_mA_n = A_nA_m su un dominio comune: per generatori illimitati la seconda non implica la prima (esempio di Nelson 1959, operatori essenzialmente autoaggiunti che commutano su un dominio denso invariante ma non hanno proiettori spettrali commutanti). Nel caso del progetto (coeff. costanti, moltiplicatori di Fourier su ℝ o 𝕋) le due nozioni coincidono. *Fix:* STRENGTHEN_ASSUMPTION testuale.
- **I-2 · HIDDEN_ASSUMPTION · INVALID senza l'ipotesi/LOCAL · MAJOR.** Servono due ipotesi non scritte:
  (a) **ogni A_n genera un semigruppo** (o almeno S_n(t)u₀ è definito): u_t = −u_xxxx − u_xx è ben posto (simbolo −κ⁴+κ² ≤ 1/4), ma il termine A_2 = −∂_x² ha moltiplicatore e^{tκ²}; con û₀ = e^{−|κ|} il dato S_2(t)u₀ ∉ L² per t > 0, quindi u_2 ed E_int^add non sono definiti mentre u lo è (controllo 5). L'identità (ii) resta vera **frequenza per frequenza**, non come identità in X.
  (b) **u è la soluzione del semigruppo** (classe di unicità): su ℝ, senza restrizioni di crescita, il problema di Cauchy per il calore non ha unicità (Tychonoff 1935; F. John, *PDE*, cap. 7). Componendo la soluzione di Tychonoff w (dato nullo, w ≢ 0) con la traslazione galileiana si ottiene una soluzione di u_t = u_xx + cu_x con u₀ = 0 e u ≢ 0, per la quale (i) dà u = 0: falso. *Controesempio da letteratura (CON-FONTE), non verificato in SymPy (serie infinita).*
  *Fix:* STRENGTHEN_ASSUMPTION: "u ∈ C([0,T];X) soluzione mild; ogni A_n genera un C0-semigruppo su X" (oppure: u₀ in una classe analitica su cui tutti gli S_n(t) sono definiti).
- **I-3 · SCOPE rispetto a H0/H1 della Fase 3 · UNDERSTATED/GLOBAL · MAJOR.** Con H0 = ℝ e H1 = H^m(Ω), Ω = I×(a,b) **limitato e senza condizioni al bordo**, u₀ = u(0,·) non determina u e non c'è un semigruppo S_n su (a,b); con condizioni al bordo i termini smettono in generale di commutare (PR-C2d). T2 vale quindi su ℝ intero (classe di unicità) o su 𝕋, non direttamente nel quadro H1. **Riformulazione proposta (ADD_DERIVATION, da affidare a S-P1):** per u in una classe di esponenziali (somme finite Σ_j c_j e^{τ_j t + ξ_j x} con P(τ_j,ξ_j) = 0, o integrali di Ehrenpreis convergenti) si definisce S_n(t) come moltiplicatore e^{t a_n(ξ)} sull'esponenziale e^{ξx}, senza condizioni al bordo; per ogni esponenziale vale (ii) con z_n = e^{t a_n(ξ_j)}−1, quindi (i) vale per linearità. È una riscrittura algebrica, ma va enunciata e dimostrata nel quadro scelto.
- **I-4 · SCOPE_OVERCLAIM · OVERSTATED/GLOBAL · MAJOR.** (iv) "B2 'O(eⁿ)' è FALSO" è più largo di (iii). B2 (piano) chiede se la "matrice di funzioni E" si costruisce con un algoritmo ≠ O(eⁿ). Ciò che (iii) dimostra: il **valore** di E_int e gli **aggregati per ordine** e_k costano O(N) e O(N²) per frequenza; la matrice d'ordine 2 (R5-P3) ha N² voci di rango 1. Ciò che **non** si può avere: la famiglia completa dei coefficienti di Möbius {c_S}_{|S|≥2} (che lo stesso T2 identifica con RT-S1c) ha 2^N−N−1 voci, quindi costa Ω(2^N) solo per essere scritta (controllo 6). *Fix:* WEAKEN_CLAIM: "Nel caso commutante il valore di E_int e le sue componenti per ordine d'interazione si calcolano in O(N) e O(N²) operazioni per frequenza; solo la tabella completa delle interazioni per sottoinsiemi è esponenziale (ed è esponenziale per dimensione dell'output, non per l'algoritmo)".
- **I-5 · CONSTANT_DEPENDENCE_HIDDEN · MINOR.** "O(N) per frequenza" nasconde: il costo di valutare z_n (grado di a_n, esponenziale complesso, aritmetica esatta o in virgola mobile) e il numero di frequenze M (su ℝ un continuo; per u esponenziale-polinomio, M = numero di esponenziali: costo O(NM) e O(N²M)). *Fix:* dichiarare il modello di costo (dipende dal modello di dato O7, da fissare da S-C3).
Nessun FATAL; nessun CRITICAL: la parte algebrica (MC-2, MC-4, MC-5) è corretta.

## 5. Red team (Phase 1.5)
| Tentativo | Esito |
|---|---|
| Matrici commutanti (polinomi in una stessa matrice di Jordan), N = 3 | identità (i) verificata esattamente |
| Matrici non commutanti (E₁₂, E₂₁) | identità falsa: commutatività necessaria |
| Termine che non genera (−∂_x² dentro −∂⁴−∂²) | u_2 non definito: ipotesi I-2(a) necessaria |
| Non unicità (Tychonoff) | (i) falsa senza classe di unicità: ipotesi I-2(b) necessaria (fonte) |
| Conteggio dei c_S | 2^N−N−1: limite inferiore Ω(2^N) per l'output completo |

## 6. Acceptance gate e stato proposto
Gate: 0 FATAL/CRITICAL ✔ (parte algebrica); ipotesi esplicite: **no** finché I-1, I-2 non entrano nell'enunciato; O(·) con dipendenze dichiarate: **no** (I-5); scope (I-3, I-4): da restringere.
**Stato proposto:**
- **R5-T2(i)–(iii)** con le ipotesi di I-1 e I-2 (X Banach, semigruppi commutanti, ogni A_n generatore, u soluzione mild), su ℝ intero o 𝕋: **DIMOSTRATO** (dipende da R5-T1 CON-FONTE).
- **R5-T2(iv)** "B2 falso": declassare a **DIMOSTRATO nella forma ristretta di I-4**; nella forma attuale è OVERSTATED.
- **R5-T2 nel quadro H1 = H^m(Ω) limitato:** **APERTO** fino alla riformulazione di I-3 (a S-P1, che ha già il compito "rifare R5-T2 con claim-lifecycle").
Kill-argument: **sì**, quando S-P1 consegna la riformulazione (cammino critico: E_int).
