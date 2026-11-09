# REPORT — R5 · Il termine d'interazione E_int (Fase 1)
Agente R5 · 2026-10-22 · Item: P1 (P1.1–P1.4), P3 (P3.1–P3.4); contributi a C4.3, G1, G3, RT-3 (con RT-S1i fusa), RT-S1c.
*(Salvato dal coordinatore dalla risposta finale di R5: la scrittura diretta era bloccata dall'ambiente.)*

**Skill caricate (Regola 2):**
- `anthropic-skills:deep-research`, invocata con Skill; workflow eseguito senza sotto-agenti.
- Lette con Read e seguite: formula-derivation, math-skill (modalità proof), research-lit (solo fonti web; nessuno script _vendor eseguito), scientific-critical-thinking (§8).

**SymPy:** `research/R5/sympy/r5_checks.py` → `r5_checks_output.txt` (tutti [OK]); `g1_example.py` → `g1_example_output.txt`.

Stato ∈ {DIMOSTRATO, DIMOSTRATO-CON-FONTE, CONGETTURA, APERTO, FALSO}.

## 1. Definizioni di E_int [R5-D1]
Sia u_t = Au, A = Σ_n A_n, S = e^{tA}, S_n = e^{tA_n}.
- (a) **additivo:** u_n := S_n(t)u0; E_int^add := u − u0 − Σ_n(u_n − u0). Il −u0 è necessario: senza di esso E_int non sparisce nemmeno per N=1.
- (b) **moltiplicativo / d'interazione:** S(t) = S_1(t)⋯S_N(t)·E_int^mult(t). Per due termini E_int^mult = U_I = e^{−tA1}e^{t(A1+A2)}; in forma non invertibile è l'errore di splitting S − S_1⋯S_N.
- (c) **log-simbolo:** ∂_t log û = Σ a_n(iκ) + E_int^log, con E_int^log ≡ 0 a coefficienti costanti.
- (d) **nucleo:** u ∈ ker L_1 + ker L_2 ?

Stato: DEFINIZIONE, da fissare nel glossario.

## 2. Caso commutante (P1.1, G1, G3)
**[R5-T1]** S1, S2 C0-semigruppi commutanti ⇒ S1(t)S2(t) è un C0-semigruppo generato dalla chiusura di A1+A2 su D(A1)∩D(A2). Fonte: Engel–Nagel 2000 §II.2.7 (numerazione da verificare); anche da Trotter. DIMOSTRATO-CON-FONTE. Esempio: D∂² e −c∂ commutano, u = G_D(t)∗u0(·−ct) (SymPy C1a/b).

**[R5-T2]** Termini a due a due commutanti.
- u = Σ_{S⊆[N]} Π_{n∈S}(S_n−I)u0, quindi E_int^add = Σ_{|S|≥2} Π_{n∈S}(S_n−I)u0. Per N=2 è (K1−δ)∗(K2−δ)∗u0: G3 confermata (C1c).
- Fourier: Ê_int = [Π(1+z_n) − 1 − Σz_n]û0 = Σ_{k≥2} e_k(z)û0, z_n = e^{t a_n(iκ)} − 1.
- Complessità: 2^N−N−1 monomi (C2: 26 per N=5), ma il valore costa O(N) per frequenza e tutti gli ordini O(N²) (coefficienti di Π(1+λz_n)).
- Coincide con l'inversione di Möbius di RT-S1c: c_S = Π(S_k−I)u0.
- DIMOSTRATO. **B2 "O(eⁿ)" è FALSO nel caso commutante.**

**[R5-P3]** Interazione d'ordine 2: E^{(2)}_{mn} = z_m z_n û0 (m≠n), parte fuori diagonale di z zᵀ û0, rango 1; ordine k = tensore z^{⊗k}. DIMOSTRATO. Il log è l'encoder giusto (D1, §1.2-3).

**[R5-P4] (G1)** L1, L2 commutanti ⇒ ker(L1+L2) ∩ (ker L1 + ker L2) ⊆ ker(L1+L2) ∩ ker(L1L2).
Dim.: u = v1+v2, L1v1 = 0, L2v2 = 0 ⇒ L1L2u = L2L1v1 + L1L2v2 = 0. ∎ DIMOSTRATO.
- Coeff. costanti: varietà V(P1+P2) ∩ V(P1P2) = V(P1,P2), finita ⇒ dimensione finita.
- Esempio L1 = ∂t−∂x², L2 = −∂x: Gröbner {ξ², τ−ξ}, quoziente di dim 2, nucleo span{1, x+t}; qui vale l'uguaglianza (x+t = x + t, x ∈ ker L1, t ∈ ker L2).
- A8 nel quadro del nucleo è falso salvo un sottospazio di dimensione finita. Uguaglianza in generale APERTA (Q3).

## 3. Caso non commutante (P1.2)
**[R5-T4] Duhamel.** A, B limitati:
e^{tA}e^{tB} − e^{t(A+B)} = ∫_0^t e^{sA}e^{sB}(e^{−sB}Ae^{sB} − A)e^{(t−s)(A+B)} ds, con e^{−sB}Ae^{sB} − A = −∫_0^s e^{−rB}[B,A]e^{rB} dr.
Bound (t²/2)‖[A,B]‖e^{t(‖A‖+‖B‖)}; E_int^mult ≡ I vicino a 0 ⟺ [A,B] = 0. DIMOSTRATO (SymPy C7).

**[R5-T5] Trotter–Kato–Chernoff.** Stabilità ‖(e^{tA/n}e^{tB/n})^n‖ ≤ Me^{ωt} e chiusura di A+B generatore di T ⇒ T(t)x = lim (e^{tA/n}e^{tB/n})^n x uniformemente sui compatti. Fonti: Trotter 1959; Chernoff 1968; Engel–Nagel Cor. III.5.8; Pazy §3.5; Kato 1978. DIMOSTRATO-CON-FONTE.

**[R5-T6] Jahnke–Lubich 2000 (BIT 40:735).** A genera C0-semigruppo, B limitato, contrattività dopo riscalamento, ‖[A,B]v‖ ≤ c1‖(−A)^α v‖, ‖[A,[A,B]]v‖ ≤ c2‖(−A)^β v‖ ⇒ errore locale Strang C1τ²‖(−A)^α v‖; con la seconda condizione O(τ³) (Thm 2.1); A analitico, α=β=1 ⇒ errore globale ≤ Cτ² log n ‖u0‖ (Thm 2.2); Thm 2.3 per B(−A)^{−1/2} limitato (convezione–diffusione). Esponenti di (b) da ricontrollare. DIMOSTRATO-CON-FONTE.

**[R5-T7] Convergenza delle serie (algebre di Banach).**
- BCH: ‖X‖+‖Y‖ < log 2, esteso a ≈1.0869 (Blanes–Casas 2004).
- Zassenhaus (C2 = −½[X,Y], C3 = ⅓[Y,[X,Y]] + ⅙[X,[X,Y]]; SymPy C3 OK): Suzuki 0.193; Bayen 0.5967; Casas–Murua–Nadinić 2012 dominio con ‖X‖+‖Y‖ < 1.054.
- Magnus: ∫‖A‖₂ < π su Hilbert / C*-algebre (Moan–Niesen 2008, Casas 2007), ottimale; Banach ≥ 2 (Moan–Oteo 2001).
- DIMOSTRATO-CON-FONTE. **Per operatori differenziali queste serie sono solo formali.**

## 4. Fattorizzazione esatta: algebre di Lie finite
**[R5-T8] Wei–Norman (1963 JMP 4:575; 1964 PAMS 15:327).** A(t) in algebra di Lie di dim. finita d ⇒ U = Π e^{g_i(t)X_i} localmente, con d ODE; risolubile ⇒ globale, per quadrature. DIMOSTRATO-CON-FONTE. Non globalità in sl(2): E−F richiede a = tan t; E+F dà a = tanh t globale (SymPy C6).

**[R5-P5] ∂²+x.** [∂²,x] = 2∂, [x,2∂] = −2: nilpotente di passo 3. e^{t(∂²+x)} = e^{t∂²}e^{tx}e^{−t²∂}e^{−2t³/3}; su e^{kx} dà exp((k+t)x + k²t + kt² + t³/3), soluzione di u_t = u_xx + xu (SymPy C4). E_int^mult = traslazione di −t² più fattore scalare. DIMOSTRATO sugli esponenziali.

**[R5-P6] OU ∂²−x∂.** [∂²,x∂] = 2∂² (affine, risolubile). e^{t(∂²−x∂)} = e^{h∂²}e^{−tx∂}, h = (e^{2t}−1)/2, globale (SymPy C5a/b). DIMOSTRATO.

**[R5-P7]** k ≥ 3 ⇒ ⟨∂², x^k⟩ ha dimensione infinita. Dim.: [x^k, ∂²] = −2kx^{k−1}∂ − k(k−1)x^{k−2}, [x^k, x^{k−1}∂] = −kx^{2k−2} (C9); 2k−2 > k, i gradi crescono senza limite. ∎ DIMOSTRATO. Per k ≤ 2 l'algebra sta in {∂², x², x∂+½, ∂, x, 1} (algebra di Schrödinger). Generalizzazione (f di grado ≤ 2 ⟺ dimensione finita): CONGETTURA (Q6).

**Corollario-tesi (P1.4/B4):** algebra finita risolubile ⇒ E_int esatto con d funzioni scalari; finita non risolubile ⇒ forma chiusa solo locale; infinita ⇒ serie, il troncamento è il "modello locale" di B3. CONGETTURA strutturata; impossibilità nel caso infinito APERTA (Q5).

## 5. Quadro d'interazione, Dyson, Kato (P3)
**[R5-D2]** U_I = e^{−tA0}e^{t(A0+V)}, U_I' = V_I U_I, V_I = Σ(−t)^j/j! ad_{A0}^j V. Dyson: U_I = 𝒯exp∫V_I; Magnus su V_I: U_I = exp Ω. Esempio OU: V_I = −x∂ + 2t∂² (polinomio in t).

**[R5-T9] Dyson–Phillips.**
- (a) B limitato: converge in norma uniformemente sui compatti, ‖S‖ ≤ Me^{(ω+M‖B‖)t} (Engel–Nagel III.1.3, III.1.10; Pazy 3.1.1).
- (b) Miyadera–Voigt: ∫_0^{t0}‖BT(s)x‖ds ≤ q‖x‖, q < 1 ⇒ converge (Engel–Nagel III.3.14–3.16).
- (c) **Dimostrato:** X = L², A = ∂², B = c(x)∂, c ∈ L^∞: ‖∂e^{s∂²}‖ = (2es)^{−1/2} ⇒ ∫_0^{t0} ≤ ‖c‖∞√(2t0/e) < 1 per t0 piccolo ⇒ Dyson converge su [0,T].
- (d) Perturbazioni con bound relativo piccolo generano semigruppo analitico (Pazy 3.2.1, Engel–Nagel III.2.10).

**[R5-T10] Kato.** Famiglia olomorfa di tipo (A): autovalore isolato di molteplicità finita ⇒ rami algebroidi, proiettore di Riesz olomorfo; raggio di Rayleigh–Schrödinger r0 ≥ min_Γ‖VR(z)‖^{−1} (Kato II §3, VII §§1–2; Reed–Simon X.12, XII.8). Il duale e^†_n è l'autovettore sinistro.

**[R5-P10] Regole di selezione.** V abbassa strettamente il grado nella base propria di A0 ⇒ Dyson ha al più n−m termini, frequenze λ_m−λ_n.
- OU: A0 = −x∂, e_n = x^n, e^†_n = δ^{(n)}(0)/n!, ⟨x^{n−2}|∂²|x^n⟩ = n(n−1).
- Primo ordine: n(n−1)e^{−(n−2)t}(1−e^{−2t})/2 = esatto (C5c); termina dopo ⌊n/2⌋ ordini (C5d).
- u0 = x⁴: coefficiente in t² di E_int^add = (t²/2)(A1A2+A2A1)u0 = −36t²x² (C5e). La parità dà zeri ulteriori. DIMOSTRATO.

**Faddeev / Lippmann–Schwinger (SCOUT-2).** Con G0 = ∂t^{−1}: u = u0 + Σ∫A_i u, identità esatta in N pezzi ma fuori dalle classi ker T_i. Relazione con G3: E_int^add = Σ_i ∫_0^t A_i(S(s)−S_i(s))u0 ds. Mori–Zwanzig = Duhamel + proiettore, da fondere in RT-3.

## 6. Quando ker(L1+L2) si separa
- Commutanti autoaggiunti: misura spettrale congiunta (Reed–Simon I; Schmüdgen cap. 5); il nucleo è l'unione degli autospazi congiunti su {λ1+λ2 = 0}, non ker L1 + ker L2.
- Miller 1977: separazione R ⟺ sottoalgebre commutative di simmetrie del 2° ordine; per il calore 1D algebra di Schrödinger (dim 6 + identità; numero di classi da verificare). Decomposizione moltiplicativa/spettrale.
- Fattorizzazione (G2): domanda inviata a R2, senza risposta (Q1).

## 7. Tabella di stato
| Claim | Stato |
|---|---|
| G3 | DIMOSTRATO |
| B2 "O(eⁿ)" | FALSO nel caso commutante (O(N) / O(N²)) |
| Matrice E di rango 1 | DIMOSTRATO |
| G1 (⊆) | DIMOSTRATO |
| G1 (=) | APERTO |
| E_int^mult = I ⟺ [A,B] = 0 (limitati) | DIMOSTRATO |
| Wei–Norman: forma esatta per algebra finita risolubile | DIMOSTRATO-CON-FONTE, più due esempi L4 |
| ∂²+x^k, k≥3: algebra infinita | DIMOSTRATO |
| Impossibilità di forma chiusa se l'algebra è infinita | APERTO |
| Dyson per c∈L^∞ + diffusione | DIMOSTRATO |
| BCH/Zassenhaus/Magnus su operatori differenziali | solo formali |
| Regole di selezione ⇒ Dyson finito | DIMOSTRATO |

## 8. Passata critica
- Il quadro additivo richiede u0 = u(0,·).
- I raggi di convergenza valgono solo in algebre di Banach.
- Esponenti di Jahnke–Lubich da ricontrollare; numerazioni di Engel–Nagel II.2.7, Wei–Norman e Miller da verificare.
- Tutti gli esempi chiave hanno un controllo SymPy indipendente.

## 9. Messaggi
- → R2: DOMANDA sui casi E_int=0; in attesa.
- ← R8: integrati i riferimenti (He–Zhao–Zhong 2024, Efendiev–Vabishchevich: dati bibliografici incompleti, da completare).
- ← SCOUT-1: WN fusa in RT-3; MOB = [R5-T2].
- ↔ SCOUT-2: relazione Faddeev↔G3.
- → R6, R7, central: AVVISI.
