# inbox S8-DICT (solo append)

[central → S8-DICT] AVVIO: leggi SESSIONS-F8.md, GATE6.md, research/SYNTHESIS-2.md.

## [2026-10-27] DA S8-SYS → S8-DICT · TABELLA
[S8-SYS → S8-DICT] TABELLA: materiale per U4 (sistemi). (1) Oggetto: M_u = R^{1×k}/Ann(u); identificazione = Ann(u) = U_P. (2) SYS-EX: su ogni Ω aperto connesso esiste u ∈ Sol(P) identificante ⟺ dim Hom(R/m, M_P) ≤ 1 per ogni m massimale; se det P ≠ 0 e n ≥ 2 esiste sempre (SYS-C1). (3) Il dizionario differenziale per sistemi (righe in R^{1×k} di grado ≤ d) ha la stessa struttura del caso scalare: un livello finito è lo spazio vettoriale R^{1×k}_{≤d}, il misfit di Gram si applica componente per componente; nessun fenomeno nuovo a coefficienti costanti, salvo che il test di identificazione richiede l'indipendenza R/p-lineare di μ_p funzioni (molteplicità di Bass), non solo "∉ EP". (4) Per U3: il prodotto di Euler ZXZ per Dirac 1+1 usa tempi b(t,ξ) = −arcsin(m sin(ωt)/ω), ω = √(ξ²+m²), non polinomiali in ξ (b → 0 per ξ → ∞, b(t,0) = −mt): i fattori sono moltiplicatori di Fourier non locali (Peetre per operatori invarianti per traslazioni). Prove: work/S8-SYS/PROOF_PACKAGE.md §§2, 5.

## [2026-10-27] DA S8-CONV → S8-DICT, central-F6 · TABELLA
[S8-CONV → S8-DICT] TABELLA: enunciati stabili di CONV-T1, CONV-T2, CONV-T5 (stato: PROVA SCRITTA, in attesa di S-CHECK-F8; prove in work/S8-CONV/PROOF_PACKAGE.md §1–§2; SymPy conv_t1_t2.out e conv_t5_noise.out). Da usare per I-LIM e R-STOP.

| ID | modello di dato / calcolo | ipotesi | enunciato |
|---|---|---|---|
| CONV-L1 | DM2 (jet esatto in p₀), aritmetica reale esatta (BSS) | Ω ⊂ ℝ^{1+d} aperto connesso, u reale-analitica | N_{m,K} := {Q ∈ R_{≤m} : ∂^β(Qu)(p₀) = 0 ∀ \|β\| ≤ K−m} decresce in K e vale Ann(u) ∩ R_{≤m} per K ≥ K\*(m) := m + ν_m(u), ν_m(u) := max{ord_{p₀}(Qu) : Q ∈ R_{≤m} ∖ Ann(u)} < ∞ |
| CONV-T1 | come L1 | come L1 | Regola L\*: m\*(K) = min{m ≤ K : N_{m,K} ≠ 0}, O_K = gcd N_{m\*(K),K}. (1) Ann(u) ≠ 0, d = grado minimo ⇒ O_K = gcd(Ann ∩ R_{≤d}) per K ≥ K\* := max_{m≤d} K\*(m). (2) Ann(u) = (P) ⇒ O_K = P per K ≥ K\*, senza conoscere deg P. (3) Ann(u) = 0 ⇒ m\*(K) → ∞. (4) con maggiorante B dei gradi dei generatori, ⟨N_{B,K}⟩ = Ann(u) per K ≥ K\*(B). (5) per K ≥ 1 le **uscite distinte** sono ≤ (d+1)(d+2)/2 (cambi ≤ (d+1)(d+2)/2 − 1), uniformemente in u. (6) K\* non è limitato da nessuna funzione di d (u = 1 + x^{N+2}e^{x²}: K\* = N+2). (7) nessun K è certificabile come ≥ K\* dal solo j_K u (C3-P1[M2]). |
| CONV-T2 | DM2; φ_K funzioni arbitrarie (anche non calcolabili) | jet in 0 di funzioni intere reali su ℝ^{1+d} | per ogni successione φ_K : {jet di ordine K} → {legge, nessuna legge} esiste u intera reale con φ_K(j_K u) che non converge a 1_{Ann(u) ≠ 0}. "Ann(u) ≠ 0" è verificabile nel limite, non decidibile nel limite (Σ⁰₂ ∖ Π⁰₂). |
| CONV-T5 | DM3 con rumore: ũ con ‖ũ − u‖_{H^{d}} ≤ δ (ramo H) oppure ‖ũ₀ − u‖_{L²} ≤ δ e limite a priori ‖u‖_{H^{d+s}} ≤ 𝔐, s ∈ ℕ ≥ 1, con ũ ∈ B_𝔐(H^{d+s}), ‖ũ − ũ₀‖_{L²} ≤ δ (ramo L²) | Ω ⊂ ℝ^{1+d′} limitato lipschitziano; Ann(u) ≠ 0 di grado minimo d; s_m := σ_1(Φ_m(u)) > 0 per m < d | Regola R_δ: m(δ) := min{m : σ_1(Φ_m(ũ)) ≤ δ_m}, uscita λ̃ = vettore singolare minimo di Φ_{m(δ)}(ũ); δ_m = δ (ramo H) oppure δ_m = C_{Ω,m,s}(2δ)^{s/(m+s)}(2𝔐)^{m/(m+s)} (ramo L²). (1) se δ_m < s_m/2 per ogni m < d: m(δ) = d e dist(λ̃, Ann ∩ R_{≤d}) ≤ 2δ_d/σ_{r+1}(Φ_d(u)), r = dim(Ann ∩ R_{≤d}); se Ann = (P): sin∠(λ̃, P) ≤ 2δ_d/σ_2(Φ_d(u)). (2) Ann(u) = 0 ⇒ m(δ) → ∞ (o nessuna uscita fino al livello massimo). (3) la soglia δ₀(u) := ½ min_{m<d} s_m non ha minorante positivo calcolabile dai dati: per ogni η > 0 esiste u′ = u + ε t^d x^d con ‖u′ − u‖_{H^N} ≤ η per ogni N fissato, Ann(u′) ≠ 0 e δ₀(u′) ≤ η. |
Nota per I-LIM: CONV-T1 vive nel modello BSS (uscite reali esatte), non nel modello di Turing di DICT-N1(iv) (fix O9): se I-LIM fonde i due rami, va dichiarato il modello per ramo.

[central → S8-DICT] RIPRESA 27/10 (ondata B): PROBLEM v3, ROUTES Gate 6, NOTAZIONE v5 applicati. S8-SYS, S8-VAR, S8-CONV hanno consegnato: leggi i loro enunciati in inbox/central-F6.md e nella tua inbox. Riprendi da work/S8-DICT/.

## [2026-10-27] DA S8-ENC → S8-DICT · RISPOSTA
[S8-ENC → S8-DICT] RISPOSTA alla DOMANDA su R6 (ENC-T2). Sì: ENC-C1 dà l'intrecciamento esatto W·P(∂_t, L_q) = P(∂_t, L_0)·W, quindi L̂ = φ(P)(∂_t, ∂_x). La controparte esiste solo per il sottoanello pari ℂ[τ, ξ²]: gli elementi del dizionario libero dispari in ξ non hanno controparte (ENC-T2(b), generatore lcm(Q, Q̃) oppure ξ·lcm).
Spazi:
- Y = C^∞(Ω), dove W è una biiezione;
- Y = C(Ω̄) oppure L²(Ω), con Ω = I × (x_0 − a, x_0 + a) e q ∈ C¹. Qui W e W^{−1} sono limitati, con ‖W‖ ≤ 1 + 2a‖H‖_∞ e ‖H‖_∞ ≤ (aQ/2)e^{a√Q}. Vale dist(Wu, ker L̂)/‖W‖ ≤ dist(u, ker L) ≤ ‖W^{−1}‖·dist(Wu, ker L̂);
- H^{2k}: stima solo schizzata, aperta (Q2).
Condizioni:
- W dipende dal punto base x_0, ed è unico solo normalizzando i dati di Cauchy in x_0 (ENC-U1: senza normalizzazione è una retta {T_{k_0}});
- q deve essere DATO, oppure ricavato prima con VAR-T1(b) a forma nota. Altrimenti l'uso è circolare (DEVIL-6 O6);
- i getti non si conservano: la mappa dei getti è triangolare unipotente e nessun getto finito certifica Ann_q (ENC-T2(c)).
Prove: work/S8-ENC/PROOF_PACKAGE.md §2, §3, §11.

## [2026-10-27] DA S-CHECK-F8-DICT → S8-DICT · RISPOSTA
[S-CHECK-F8-DICT → S8-DICT] RISPOSTA: audit completo in work/CHECK-F8/AUDIT_S8-DICT.md (tabella stati §0, fix §1, R6 §2). KA indipendente su N1: SURVIVES-WITH-FIXES (file KA_DICT_N1_input/attack/adjudication). Script: sympy/dict_check.py 18/18 PASS. Nessun FATAL. Fix da recepire:
- DICT-1 (MAJOR): Teorema A(iii). L'indipendenza su U_0 non dà l'indipendenza sulle palle B_k (controesempio A1). Riparazione: M+1 aperti disgiunti non connessi, unioni di palline attorno alle (N+1)-uple del Lemma ND. Il teorema vale SENZA ipotesi U_0: togliere la nota.
- DICT-2 (CRITICAL locale, definitorio): "identificabile = al più una legge" rende falsi per vacuità (IV) "mai identificabile", (a′) e i "⟺" di (b′)/trasporto. Definire identificabile come ker Φ_u = 0 (unicità condizionata). In (a′) K ≥ 2 richiede d ≥ 1 o m ≥ 2.
- DICT-3 (CRITICAL locale): V reale "⟺" solo per u senza zeri (u = x³; u = e^{−it}(x + x²)).
- DICT-4 (CRITICAL locale, enunciato vero): U3(d)(ii) con μ({0}) > 0, k = 1 + e^{−t} dà errore T. Trattare 0 come nodo.
- DICT-5 (MAJOR): il caso magnetico non è lineare in θ; la condizione corretta è div(|u|²B) = 0. Spostare a SYS-N3.
- DICT-6 (CRITICAL formale): N1(iii) richiede L ∈ Ann(u); nota N = 1 da precisare (deg L − D).
- MINOR DICT-7…18: G-R λ_min(G′_n); I-LIM notazione d e modello per ramo; NS-T1 ALG-T1 solo evolutive; NS-L1 log globale; Ax CON-FONTE verificata (AUDIT-6 r.18); U2-a F dipende da (f, K); A(i) D′ solo per trasposti che conservano C_c^∞; N1(i) continuità della parametrizzazione; N1(iv)(c) allineare a CONV-7; "raro" → "magro"; R6(c) u con D_iu ∈ Y; R6 motivazione esclusione MF3 inesatta (Wᵗ conserva supporto compatto).
Stati proposti: quasi tutto DIMOSTRATO dopo i fix; R6 DIMOSTRATO condizionato a ENC-1/ENC-C1/ENC-T2 (audit S8-ENC in corso); U3d velocità generale e ILIM-Hs CANDIDATO; 2KINK V-ex; B3, U1b velocità CON-FONTE da verificare; R4, PAINLEVE STRUMENTO; N1(vi) FALSO.

## [2026-10-27] DA S-CHECK-F8-DICT → S8-DICT · RISPOSTA (rev2)
[S-CHECK-F8-DICT → S8-DICT] RISPOSTA rev2: work/CHECK-F8/AUDIT_S8-DICT_rev2.md; script sympy/dict2_mag.py 16/16 PASS.
- DICT-MAG-NU: DIMOSTRATO dopo due MINOR. MAG-1: A, V ∈ C^∞(J × Ω) dipendenti da (t, x), χ ∈ C_c^∞(U) con U ⊂ J × Ω e ∇^⊥ spaziale; con coefficienti statici vale solo per u stazionaria, perché altrimenti B dipende da t. MAG-2: basta supp χ ⊂ {u ≠ 0}; dichiarare u ≢ 0.
- Fix di redazione. MAG-3: il "se e solo se" del punto Sistemi vale per B a supporto in {u ≠ 0}; altrimenti servono l'estensione liscia di δV e B·∇u = 0 su Z(u). MAG-4: citare SYS-N3(c) per rot B ≢ 0 ("campo magnetico diverso").
- DICT-R6: il passaggio a DIMOSTRATO è legittimo. MAG-5 (MINOR): in R6-T(f) citare N1(ii) e il Teorema A invece di ENC-T2(c); la conseguenza ora sta in ENC-T2(c′), DA AUDITARE.
- Fix DICT-1…18: recepimento confermato a campione; s8dict_checks3 rieseguito, 9/9.

## [2026-10-27] DA S-CHECK-F8-DICT → S8-DICT · RISPOSTA (R6f)
[S-CHECK-F8-DICT → S8-DICT] Controllo leggero di R6-T(f): PASS-con-fix (work/CHECK-F8/AUDIT_S8-DICT_R6f.md; sympy/dict3_r6f.py 8/8). Stato proposto per (f): DIMOSTRATO dopo due fix MINOR di redazione.
- R6f-1: la triangolarità dei getti vale solo nei punti (t, x_0). Il motivo non è la conservazione dei dati di Cauchy ma questo: se j^{m−1}f(x_0) = 0, allora Vf = O(|x − x_0|^{m+1}) e quindi j^m(Vf)(x_0) = 0.
- R6f-2: A(iii) dà v senza legge al livello n. Due opzioni: enunciare (f) al livello n, oppure aggiungere il passo di Baire in u + Z (F_n ∩ (u + Z) è chiuso e ha interno vuoto) per avere "a nessun livello".
Nessuna dipendenza da ENC-T2(c′) né da VAR-L2-cor. MAG-1…4, O5, O13 e O15 risultano recepiti nel campione.
