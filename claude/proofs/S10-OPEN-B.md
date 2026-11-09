# PROOF_PACKAGE — S10-OPEN-B · residui della Fase 5 · 27/10/2026

> **rev2 (27/10/2026, dopo l'audit S-CHECK-F10-B, `work/CHECK-F10/AUDIT_S10-OPEN-B.md`).** I fix dell'audit sono recepiti nella sezione finale «Recepimento dell'audit (rev2)», che **prevale** sul testo dei §§1–11 dove questi sono in conflitto. In particolare §7, §8, §10 e §11 sono sostituiti da R7, R8, R10 e R11.

Nessun enunciato è dichiarato DIMOSTRATO: gli stati sono **proposti** e attendono l'audit (claim-lifecycle). I calcoli SymPy/mpmath sono **verifiche** (computer-assisted solo dove dichiarato), eseguiti con `.venv\Scripts\python.exe -I`; script e uscite in `sympy/`. Nessuno script `_vendor` eseguito; niente machine learning.

## 0. Sintesi degli esiti

| # | problema | esito | stato proposto | dove |
|---|---|---|---|---|
| 1 | INT-T1(B) / [F4⁻] (N-solitoni di Hirota senza riflessione) | (a) prova per N generale | PROVA SCRITTA, da auditare | §1 |
| 2 | OPF5C-T5 (numero Ritt/Kolchin) | (a) prova autonoma, nessuna fonte necessaria | PROVA SCRITTA, da auditare | §2 |
| 3 | OPA-Q2, densità di (SB) | (a) prova | PROVA SCRITTA, da auditare | §3 |
| 4 | OPA-Q1 con più nascite, lemma L-loc | (a) prova per localizzazione | PROVA SCRITTA, da auditare (punto delicato: §4.4) | §4 |
| 5 | densità di OPF5B-T1 su domini non convessi | (b) controesempio verificato | PROVA SCRITTA + V-ex `s10b_annulus` 3/3 | §5 |
| 6 | [Hm] (parte di S4ID-P8 / OPR2-P7) | (a) prova per soluzioni globali in 𝒮 | PROVA SCRITTA + SymPy `s10b_hm` 4/4 | §6 |
| 7 | [GT-u] (S4ID-P8 / OPR2-P7) | (c) | APERTO — ridotto a uniformità in k_0 delle costanti di GT Thm 5.4 | §7 |
| 8 | INT-Q1 (dati analitici) | (c) | APERTO — ridotto a relazioni con forma iniziale in I_PW singolari nell'origine, mod [GT-u] | §8 |
| 9 | OPF5C-Q1 (δ_N(K)) | valori nuovi + (c) | δ_N(2N) = N+1 per N ≤ 5 (computer-assisted, mod L8′); δ_5(8) = 9; APERTO — ridotto a limiti inferiori graduati a k = 0 | §9 |
| 10 | OPR2-Q3 (rimuovere (I) e (II)) | (c) caratterizzazione esatta | PROVA SCRITTA (caratterizzazione); APERTO — ridotto a realizzabilità degli atomi | §10 |
| 11 | OPR2-Q2′ (localizzazione al poligono) | (c) | APERTO — ridotto al lemma di localizzazione (L) | §11 |

---

## 1. [F4⁻]: gli N-solitoni di Hirota sono potenziali senza riflessione — chiude INT-T1(B)

**Convenzione** (OP-F5D): L_u = −∂² − u, KdV u_t + u_xxx + 6uu_x = 0; funzioni di Jost ψ_±, coefficienti a(k), b(k); per OPF5D-L4 gli zeri di a nel semipiano superiore sono iκ_j e gli autovalori sono −κ_j².

**Enunciato [OPF5D-F4⁻ → S10B-T1].** Siano 0 < κ_1 < … < κ_N, c_j > 0, ε_j := (−1)^{j−1}, k_j := 2κ_j. Sia f l'N-solitone di Hirota

  f(x) = Σ_{S⊆{1..N}} Π_{j∈S} e^{η_j} Π_{i<j; i,j∈S} A_ij,  A_ij = ((k_i − k_j)/(k_i + k_j))²,  e^{η_j} = c_j d_j e^{k_j x},

con d_j := Π_{l≠j} (κ_j + κ_l)/|κ_j − κ_l| > 0, e u := 2(log f)″. Allora u ∈ 𝒮(ℝ), b ≡ 0, a(k) = Π_j (k − iκ_j)/(k + iκ_j), e lo spettro discreto di L_u è {−κ_1², …, −κ_N²}. Con c_j = c_j(0)e^{−8κ_j³t} (cioè η_j = k_jx − k_j³t + η_j⁰) lo stesso vale per ogni t: u(t) è l'N-solitone di KdV, senza riflessione per ogni t.

Poiché ogni scelta di fasi η_j⁰ ∈ ℝ corrisponde a c_j > 0, l'enunciato copre tutti gli N-solitoni di Hirota con k_j distinti positivi.

**Prova.**

*Passo 1 (Wronskiano dei semi).* Siano φ_j := e^{−κ_jx} + ε_jc_je^{κ_jx}, quindi −φ_j″ = −κ_j²φ_j. Sia W := W(φ_1, …, φ_N). Per multilinearità nelle colonne, scegliendo in ogni colonna j l'addendo e^{s_jκ_jx} con s_j = +1 se j ∈ S e s_j = −1 altrimenti, si ottiene

  W = Σ_S Π_{j∈S}(ε_jc_j) · V(s_1κ_1, …, s_Nκ_N) · e^{Σ_j s_jκ_jx},

dove V(z_1..z_N) = Π_{i<j}(z_j − z_i) è il Vandermonde (det[z_b^{a−1}]). Posto V_0 := V(−κ_1, …, −κ_N) ≠ 0 e ρ(S) := V(s·κ)/V_0:

  W = V_0 e^{−Σκ_jx} Σ_S Π_{j∈S}(ε_jc_j) ρ(S) e^{2Σ_{j∈S}κ_jx}.

*Passo 2 (regola dei segni e modulo).* Fattore per fattore, per i < j:
- i, j ∉ S: (−κ_j + κ_i)/(−κ_j + κ_i) = 1;
- i, j ∈ S: (κ_j − κ_i)/(κ_i − κ_j) = −1;
- i ∈ S, j ∉ S: (−κ_j − κ_i)/(κ_i − κ_j) = (κ_i + κ_j)/(κ_j − κ_i) > 0;
- i ∉ S, j ∈ S: (κ_j + κ_i)/(κ_i − κ_j) < 0.

Modulo: |ρ(S)| = Π_{i∈S, l∉S}(κ_i + κ_l)/|κ_i − κ_l|. Poiché Π_{j∈S}d_j = |ρ(S)| · Π_{i<j∈S}((κ_i + κ_j)/(κ_i − κ_j))², si ha |ρ(S)| = Π_{j∈S}d_j Π_{i<j∈S}((κ_i − κ_j)/(κ_i + κ_j))².

Segno: il numero di fattori negativi è C(|S|,2) + #{(i,j): i < j, i ∉ S, j ∈ S} = C(|S|,2) + Σ_{j∈S}[(j − 1) − #{i < j: i ∈ S}] = Σ_{j∈S}(j − 1). Quindi sign ρ(S) = Π_{j∈S}(−1)^{j−1} = Π_{j∈S}ε_j, e Π_{j∈S}ε_j · ρ(S) = |ρ(S)| > 0.

Poiché (κ_i − κ_j)/(κ_i + κ_j) = (k_i − k_j)/(k_i + k_j), risulta

  W = V_0 e^{−Σκ_jx} f(x),  f > 0 (somma di esponenziali a coefficienti positivi, termine S = ∅ uguale a 1).

In particolare W non si annulla mai e 2(log W)″ = 2(log f)″ = u.

*Passo 3 (intreccio, senza citare Crum).* Sia A g := W(φ_1, …, φ_N, g)/W. A è un operatore differenziale monico di ordine N a coefficienti C^∞, A = ∂^N + a_{N−1}∂^{N−1} + …, con a_{N−1} = −W′/W (sviluppo dell'ultima colonna: il cofattore di g^{(N−1)} è −W′), e ker A = span{φ_j}.

Divisione a destra per A: A(−∂²) = QA + R, con ord R < N e Q di ordine 2. Per ogni j, A(−∂²)φ_j = −κ_j²Aφ_j = 0 e QAφ_j = 0, quindi Rφ_j = 0. Se fosse R ≠ 0, con coefficiente di testa r_m ≢ 0 (m < N), su un intervallo dove r_m ≠ 0 le soluzioni di Rg = 0 formerebbero uno spazio di dimensione ≤ m < N, mentre le φ_j sono linearmente indipendenti su ogni intervallo (W ≠ 0). Quindi R = 0.

Confronto dei coefficienti in A(−∂²) = QA, con Q = q_2∂² + q_1∂ + q_0:
- ∂^{N+2}: q_2 = −1;
- ∂^{N+1}: −a_{N−1} = −a_{N−1} + q_1, quindi q_1 = 0;
- ∂^N: −a_{N−2} = −a_{N−2} − 2a_{N−1}′ + q_0, quindi q_0 = 2a_{N−1}′ = −2(log W)″.

Dunque Q = −∂² − u = L_u e **L_u A = A(−∂²)**.

*Passo 4 (asintotica e coefficienti di scattering).* Per k ∈ ℝ∖{0}, ψ := Ae^{ikx} soddisfa L_uψ = k²ψ. W(φ, e^{ikx}) e W(φ) sono somme finite di esponenziali.
- Per x → +∞ dominano i termini S = {1..N} (φ_j ≈ ε_jc_je^{κ_jx}), con errore relativo O(e^{−2κ_1x}) insieme alle derivate. Dunque A → Π_j(∂ − κ_j), operatore a coefficienti costanti con nucleo span{e^{κ_jx}}, e ψe^{−ikx} → Π_j(ik − κ_j).
- Per x → −∞ dominano i termini S = ∅ (φ_j ≈ e^{−κ_jx}), e ψe^{−ikx} → Π_j(ik + κ_j).

Allora ψ_+(x,k) = ψ/Π_j(ik − κ_j) è la soluzione di Jost a +∞, e per x → −∞ vale ψ_+ = [Π_j(ik + κ_j)/(ik − κ_j)]e^{ikx}(1 + o(1)), **senza componente e^{−ikx}**. Nella convenzione di OPF5D-L3 il coefficiente di e^{−ikx} è b, quindi b(k) ≡ 0. Il coefficiente di e^{ikx} è a(k) = Π_j(ik + κ_j)/(ik − κ_j) = Π_j(k − iκ_j)/(k + iκ_j), che ha zeri esattamente in iκ_j. Per OPF5D-L4 lo spettro discreto è {−κ_j²} = {−k_j²/4}.

*Passo 5 (u ∈ 𝒮).* log f = log(termine dominante) + log(1 + somma esponenzialmente piccola) ai due estremi, e il termine dominante è esponenziale lineare in x. Quindi u = 2(log f)″ e tutte le sue derivate decadono come O(e^{−2κ_1|x|}).

*Passo 6 (tempo).* Per t fissato, c_j(t) = c_j(0)e^{−8κ_j³t} > 0: si applicano i Passi 1–5. Che u(t) risolva KdV è il fatto classico di Hirota, già usato da OP-F5D, e non è riprovato qui. ∎

**Conseguenza per INT-T1(B).** [F4⁻] era l'unica ipotesi residua di INT-T1(B) via OPF5D-T3. Con S10B-T1, INT-T1(B) diventa **PROVA SCRITTA mod audit di S10B-T1**, senza fonte esterna.

**Verifica `sympy/s10b_f4.py`** (uscita in `s10b_f4.out`):
- F1: minori principali di Cauchy, N ≤ 4 (forma alternativa f = det(I + C)), simbolica;
- F2/F3: regola dei segni e modulo di ρ, N ≤ 6, esatta;
- F4: Wronskiano = V_0e^{−Σκx}f, N = 2, 3, numerica a 40 cifre in 7 punti;
- F5: (−∂² − u)ψ = k²ψ, numerica;
- F6: asintotica a x = ±40.

Il primo run (F1 fino a N = 5 e F4 simbolica) ha superato il timeout senza uscita. Il run ridotto dà 21/22 OK. L'unico FAIL (F5, N = 3, residuo 2.3e-14) è un artefatto di `lambdify`: con `evalf` esatto il residuo relativo è 8.5e-198 (`s10b_f4_f5check.out`). Dettagli in CHECK_REQUEST.

---

## 2. OPF5C-T5 senza numero di fonte: ideali differenziali primi in una indeterminata

**Enunciato [S10B-T2].** Sia F un campo differenziale di caratteristica 0 con una derivazione, F{y} l'anello dei polinomi differenziali in una indeterminata e J ⊊ F{y} un ideale differenziale primo non nullo. Sia A ∈ J di rango minimo (prima l'ordine n, poi il grado d nella derivata di testa y_n), con iniziale I_A, separante S_A = ∂A/∂y_n e H_A := I_AS_A. Allora **J = [A] : H_A^∞**.

**Prova.**
- *A è irriducibile.* Se A = BC con B, C ∉ F, ciascun fattore ha rango strettamente minore: o ordine < n, o ordine n e grado < d. Per primalità uno dei due sta in J, contro la minimalità. Nessun fattore sta in F∖0, perché J è proprio.
- *H_A ∉ J.* I_A ≠ 0 ha ordine < n o è in F∖0. S_A ≠ 0 perché d ≥ 1 e car F = 0, e ha grado d − 1 in y_n. Entrambi hanno rango minore di A, quindi non stanno in J (un elemento non nullo di rango minore in J contraddirebbe la minimalità; uno in F∖0 contraddirebbe J ≠ F{y}). Per primalità H_A^k ∉ J per ogni k.
- *⊇.* Se H_A^kf ∈ [A] ⊆ J, allora f ∈ J perché J è primo e H_A^k ∉ J.
- *⊆.* Sia f ∈ J. Per la riduzione di Ritt (pseudo-divisione differenziale: prima rispetto alle derivate A^{(i)}, i ≥ 1, il cui iniziale è S_A, poi la pseudo-divisione algebrica per A con iniziale I_A) esistono a, b ≥ 0 e R ridotto rispetto ad A (ordine ≤ n e grado in y_n < d, quindi rango minore di A) tali che S_A^aI_A^bf ≡ R mod [A]. Allora R ∈ J, perché f ∈ J e [A] ⊆ J. Se R ≠ 0, avrebbe rango minore di A (oppure R ∈ F∖0): impossibile. Quindi R = 0 e S_A^aI_A^bf ∈ [A], da cui H_A^{max(a,b)}f ∈ [A]. ∎

Questa è la prova classica in una indeterminata. Non serve il numero del teorema in Ritt o Kolchin: la dipendenza di OPF5C-T5 da quella citazione si elimina.

**Applicazione (ideale J_u di OP-F5C).** Sia u analitica reale su un intervallo connesso e J_u := {P : P[u] ≡ 0}.
- J_u è primo, perché l'anello delle funzioni analitiche su un connesso è integro (teorema d'identità). È differenziale, perché ∂(P[u]) = (∂P)[u].
- Se u(t,·) risolve u_t = F[u] e P[u(t)] ≡ 0 per ogni t, allora (D_FP)[u] = ∂_t(P[u]) ≡ 0: J_u è D_F-stabile.

S10B-T2 si applica a J_u ≠ 0 e dà J_u = [A] : H_A^∞.

---

## 3. OPA-Q2: densità di (SB) dentro Morse

**Quadro** (OP-F5A §3): u_0 ∈ C^r(𝕋), r ≥ 3, U_0 una primitiva sul rivestimento, Φ_x(a) = U_0(a) + (x − a)²/2t, M_t(x) l'insieme dei minimizzanti, J_t(a) = 1 + tu_0′(a). Per OPF5A-L4 e Morse, un minimizzante degenere sta in un minimo locale a_b di u_0′ con u_0′(a_b) = −1/t_b < 0, ed è una cuspide A_3 (i massimi locali di u_0′ non sono mai minimizzanti degeneri). (SB): per ogni t_b ∈ T_1 c'è al più un minimizzante degenere (x_b, a_b), e M_{t_b}(x_b) = {a_b}.

**Enunciato [S10B-P3].** Morse+(SB) è densa in C^r(𝕋), r ≥ 3. Insieme all'apertura (audit F5A-12) e alla densità di Morse (F5A-11, DIMOSTRATA), la classe Morse+(SB) è **aperta e densa**: "generico" in OPA-Q2 cessa di essere CONDIZIONALE, mod audit.

**Prova.** Sia u_0 ∈ C^r con u_0′ di Morse (densità F5A-11) e sia ε_0 > 0 fissato. Siano m_1, …, m_p i minimi locali di u_0′ con u_0′(m_i) < 0, e t_i := −1/u_0′(m_i) i tempi candidati: per L4 sono gli unici tempi con possibili minimizzanti degeneri. Sia x_i := m_i + t_iu_0(m_i).

*Passo 1 (valori critici distinti).* Sia χ ∈ C_c^∞(−2ρ, 2ρ) pari, con χ = 1 su [−ρ, ρ], e ψ_i(x) := (x − m_i)χ(x − m_i). Allora ψ_i′ = 1 vicino a m_i, e ψ_i″ è supportato in ρ ≤ |x − m_i| ≤ 2ρ. Si sceglie ρ così piccolo che la corona non contenga punti critici di u_0′ e che vi valga |u_0″| ≥ c > 0. Per |ε| < c/‖ψ_i″‖_∞ la funzione u_0 + εψ_i:
- ha gli stessi punti critici di u_0′, con le stesse hessiane;
- ha u_0′(m_i) spostato di ε e gli altri valori critici invariati.

Con una scelta successiva di ε_i piccoli e generici, i valori u_0′(m_i) diventano a due a due distinti: ai tempi t_i c'è al più un candidato, quindi al più un minimizzante degenere. La condizione è aperta (finitezza e continuità dei valori critici).

*Passo 2 (unicità del minimizzante a t_i).* Si procede per i = 1..p. Se a t_i il punto m_i non è minimizzante di Φ_{x_i}, oppure M_{t_i}(x_i) = {m_i}, non si fa nulla. Altrimenti M_{t_i}(x_i) ∋ a′ ≠ m_i.
- m_i è un minimo locale stretto isolato di Φ_{x_i}: Φ_{x_i}′(a) = (X_{t_i}(a) − x_i)/t_i con X′ = J_{t_i} ≥ 0 vicino a m_i, nullo solo in m_i.
- Si sceglie r_i > 0 tale che (m_i − 2r_i, m_i + 2r_i) non contenga punti critici di u_0′ diversi da m_i né punti di M_{t_i}(x_i)∖{m_i}. Sulla corona compatta C_i := {r_i ≤ |a − m_i| ≤ 2r_i} vale Φ_{x_i} ≥ Φ_{x_i}(m_i) + η_i con η_i > 0.
- Sia Θ_i ∈ C^∞(𝕋), 0 ≤ Θ_i ≤ 1, Θ_i = 0 su |a − m_i| ≤ r_i e Θ_i = 1 fuori da |a − m_i| < 2r_i. Si pone θ_i := Θ_i′: periodica, a media nulla, supportata in C_i.
- Con u_0 ↦ u_0 + εθ_i si ha U_0 ↦ U_0 + εΘ_i. Il getto di u_0 in m_i non cambia, quindi t_i e x_i non cambiano. Φ_{x_i} aumenta esattamente di ε fuori dalla finestra, di εΘ_i ∈ [0, ε] su C_i, e non cambia su |a − m_i| ≤ r_i. Per 0 < ε < η_i: M_{t_i}(x_i) = {m_i}.
- Per ε piccolo restano invariati: Morse (su C_i |u_0″| ≥ c e θ_i″ è limitata), i punti critici di u_0′ e i loro valori (θ_i′ è nulla fuori da C_i, dove non ci sono punti critici). Quindi i tempi candidati t_j e i punti m_j, x_j sono invariati.

*Passo 3 (le condizioni già ottenute sono aperte).* Per ogni j, la condizione SB_j ("m_j non minimizzante di Φ_{x_j} a t_j" oppure "M_{t_j}(x_j) = {m_j}") è aperta in C^3:
- il primo caso è una disuguaglianza stretta tra quantità continue nel dato (m_j, t_j, x_j dipendono con continuità da u_0 sotto Morse);
- nel secondo caso il margine η_j fuori da un intorno di m_j è stabile, e dentro l'intorno Φ_{x_j}′ è strettamente crescente tranne in un punto (J_{t_j} ≥ 0 con zero isolato, struttura che persiste perché m_j resta un minimo locale non degenere di u_0′ con valore −1/t_j). Quindi c'è un solo minimizzante locale nell'intorno.

Si sceglie allora ε_i nel Passo 2 minore della metà dei margini delle condizioni SB_j, j < i, e della condizione di distinzione del Passo 1.

Dopo p passi, ũ_0 := u_0 + Σε_iψ_i + Σε'_iθ_i è Morse+(SB) e ‖ũ_0 − u_0‖_{C^r} < ε_0. ∎

Rispetto allo schizzo F5A-12, la verifica mancante ("la perturbazione non crea nuove coincidenze agli altri tempi") è il Passo 3: i tempi candidati sono finiti e invariati dalle perturbazioni, e le condizioni ai tempi già trattati hanno margini aperti.

---

## 4. OPA-Q1 con più nascite: lemma L-loc

**Enunciato (L-loc, testo dell'audit F5A-13).** Sotto Morse+(SB), u_0 ∈ C^5, per ogni t_b ∈ T_1′ esistono τ_b, r_b > 0 tali che per |t − t_b| ≤ τ_b:

  ∫_{|x−x_b|<r_b}|u − v|dx = 2ν log(1/max(|t − t_b|, √ν)) + O(ν),  ∫_{|x−x_b|≥r_b}|u − v|dx = O(ν),

con O(ν) uniforme in t. Con C1 (già DIMOSTRATO mod [F1] su (0, t* + τ_0] e lontano da T_1′) si ottiene C1 su (0, T] per tutta la classe Morse+(SB), mod [F1].

Notazione locale: a_b minimo locale non degenere di u_0′, u_0′(a_b) = −1/t_b, κ_3 := u_0‴(a_b) > 0, α := a − a_b, η := 1 − t/t_b.

**4.1 Margine (sostituisce l'unicità globale di (G\*)).** Per (SB) M_{t_b}(x_b) = {a_b}. Per la semicontinuità superiore di (t, x) ↦ M_t(x) (compattezza di 𝕋 e continuità di Φ) esistono z_0, r_b, τ_b, η_0 > 0 tali che, per |t − t_b| ≤ τ_b e |x − x_b| < 2r_b:
- ogni minimizzante sta in |α| < z_0/2;
- Φ_x(a) ≥ min Φ_x + η_0 per |α| ≥ z_0.

Il contributo all'integrale di Hopf della regione |α| ≥ z_0 è O(e^{−η_0/2ν}), quindi trascurabile in tutte le medie ⟨·⟩_x.

**4.2 Geometria locale (L2 localizzato).** Su |α| ≤ 2z_0, con z_0 piccolo:
- J_t(a_b + α) = (t/t_b)J_{t_b}(a_b + α) + η, con J_{t_b}(a_b + α) = (t_bκ_3/2)α²(1 + O(α)). Quindi c(η + α²) ≤ J_t ≤ C(η + α²) per η ≥ 0, e |u_0″(a)| ≤ C|α|.
- Nella finestra |α| < 2z_0, Φ_x″ = J_t/t ≥ 0 per t ≤ t_b: Φ_x è convessa **nella finestra**.

Le stime (a)–(c) di OPF5A-L2 valgono con ψ(z) := Φ_x(a + z) − m(x), per |z| ≤ z_0 e a nella finestra. La prova è quella di L2: usa solo ψ(z) = (1/t)∫_0^z(z − s)J_t(a + s)ds e la forma di J_t vicino ad a_b. Per |z| ≥ z_0 la convessità globale, usata in L2 solo per la coda, è sostituita dal margine η_0 di 4.1 (come in F5A-6).

**4.3 Fase pre-shock t ∈ [t_b − τ_b, t_b] (T1 localizzato).**
- *Dentro |x − x_b| < r_b.* I Passi 1–4 di OPF5A-T1 si ripetono parola per parola. Il Passo 1 usa integrazioni per parti per la misura e^{−ψ/2ν}: con la coda O(e^{−η_0/2ν}) si ottengono le stesse identità a meno di errori esponenzialmente piccoli. Il Passo 2 (integrale esterno) diventa ν∫t|u_0″|/J_t da sulla finestra di a, dove J_t è monotona su ciascun lato di a_b (tu_0″ = ∂_aJ_t). Ciò dà 2 log(1/max(√ν, η)) + O(1), con O(1) uniforme perché ai bordi della finestra J_t ≍ 1. Il Passo 3 (regione interna) è invariato.
- *Fuori, |x − x_b| ≥ r_b.* A t = t_b ogni minimizzante (t_b, x, a) con |x − x_b| ≥ r_b ha J > 0, perché l'unico degenere è (x_b, a_b) per (SB). L'insieme 𝒦_b := {(t, x, a): |t − t_b| ≤ τ_b, |x − x_b| ≥ r_b, a ∈ M_t(x)} è compatto, e per τ_b piccolo J ≥ 2j_0 > 0 su 𝒦_b (semicontinuità). L'argomento delle scatole di OPF5A-L3 si applica: ricoprimento finito, costanti uniformi, L3 su ogni scatola. Dà ∫_{|x−x_b|≥r_b}|u − v| ≤ Cν, inclusi i punti tripli e gli urti preesistenti.

**4.4 Fase post-shock t ∈ [t_b, t_b + τ_b] (T2 e Lemma U localizzati).** Questo è il punto da auditare con più cura.
- Con τ := t − t_b, a = a_b + √τA, x = X_t(a_b) − tτ^{3/2}ξ, la forma normale Ψ_τ(ξ, A) := τ^{−2}[Φ_x(a_b + √τA) − Φ_x(a_b)] converge in C^4 sui compatti a Ψ_0 = ξA + (κ_3/24)A⁴ − A²/(2t_b²). La derivazione del Lemma U usa solo lo sviluppo di Taylor di u_0 in a_b fino all'ordine 5, quindi è locale.
- Le code |A| grandi entro la finestra |α| < z_0 sono controllate dalla crescita A⁴ (Lemma 3 di OP-ANA). Oltre la finestra vale il margine η_0 di 4.1.
- L3′ si applica alla famiglia compatta {Ψ_τ(ξ, ·)}_{τ≤τ_0, |ξ|≤Ξ}. Le sue ipotesi (1)–(3) sono proprietà di Ψ_0 e della C^4-vicinanza, indipendenti dal resto di 𝕋.
- La regione intermedia (|ξ| > Ξ ma |x − x_b| < r_b) è trattata come in T2(a): un solo minimizzante non degenere, con le stime L2 locali.
- Fuori da |x − x_b| < r_b: come in 4.3, con lo stesso compatto 𝒦_b.

Ordine delle costanti (come nel KA su Lemma U): K'_{(b)} → Ξ → ν̂_0 → K_1 → K'_{(a)}, poi τ_b ≤ min(τ_0, margine di 4.1). Non è circolare, perché z_0, r_b, η_0 sono fissati prima da (SB).

**4.5 Conclusione.** T_1′ ∩ (0, T] = {t_1 < … < t_B} è finito (T4(iv)). Su [t_b − τ_b, t_b + τ_b] valgono 4.3–4.4; sui compatti complementari vale L3. Per ogni t ∈ (0, T] c'è al più una finestra attiva (τ_b < metà delle distanze tra nascite). Quindi uniformemente su (0, T]:

  ‖u − v‖_{L^1} = 2ν log(1/max(d(t), √ν)) + O(ν),  d(t) = min_b|t − t_b|,

mod [F1], e sup = ν|log ν| + O(ν) con coefficiente 1. ∎

**Stato proposto:** PROVA SCRITTA (localizzazione), da auditare. Non sono stati fatti nuovi controlli numerici. Il punto di rischio è 4.4, l'uniformità del Lemma U con il margine al posto della convessità globale.

---

## 5. Densità di OPF5B-T1 fuori dai convessi: controesempio

**Enunciato [S10B-C1].** Siano Ω := (0,3)² ∖ [1,2]² (aperto limitato connesso, lipschitziano, non convesso), P = ∂_x∂_y, Q_1 = ∂_x, Q_2 = ∂_y (coprimi, P = Q_1Q_2). Per ogni m ≥ 0, ker_{H^m(Ω)}Q_1 + ker_{H^m(Ω)}Q_2 **non è denso** in ker_{H^m(Ω)}P, nemmeno nella norma L². Quindi la convessità in OPF5B-T1 non si può togliere: la condizione corretta va cercata tra "convesso" e "stellato rispetto a una palla" (OPF5B-C1(d), che resta un'osservazione).

**Prova.**
- *Il dato.* Sia φ ∈ C^∞(ℝ), φ = 0 su (−∞, 1], φ = 1 su [2, ∞), e u(x, y) := φ(x)φ(y). Allora u_xy = φ′(x)φ′(y) è supportato in [1,2]², disgiunto da Ω. Quindi Pu = 0 su Ω e u ∈ H^m(Ω) per ogni m (liscia e limitata con le derivate su Ω limitato).
- *Il funzionale.* Siano I_1 := (0.4, 0.6), I_2 := (2.4, 2.6) e, per F ∈ L²(Ω),

  Λ(F) := 25² [∫_{I_2×I_2}F − ∫_{I_1×I_2}F − ∫_{I_2×I_1}F + ∫_{I_1×I_1}F]

  (25² = 1/|I_i × I_j|). I quattro quadratini stanno in Ω, e Λ è continuo su L²(Ω).
- *Λ si annulla su ker Q_1.* Le strisce (0,3) × I_j sono connesse e contenute in Ω. Se ∂_xF = 0 in 𝒟′(Ω), allora F(x, y) = g_j(y) q.o. su ciascuna striscia. Quindi ∫_{I_2×I_j}F = ∫_{I_1×I_j}F e Λ(F) = 0.
- *Λ si annulla su ker Q_2.* Simmetricamente, con le strisce I_j × (0,3).
- *Conclusione.* Λ si annulla sulla chiusura L² di ker Q_1 + ker Q_2. Ma Λ(u) = 1 − 0 − 0 + 0 = 1, perché u = 1 su I_2 × I_2 e u = 0 sugli altri tre quadratini. ∎

**V-ex `sympy/s10b_annulus.py` (3/3 OK):**
- A1: u_xy = 0 su griglia 59×59 di Ω;
- A2: Λ(A(y) + B(x)) = 0, simbolico;
- A3: Λ_avg(u) = 1.0, quadratura.

**Lettura.** L'ostruzione è topologica: il funzionale "rettangolo attorno al buco" è la monodromia della 1-forma u_x dx + u_y dy ristretta ai nuclei. Ogni Ω in cui esiste un rettangolo coordinato con lati in Ω che circonda un punto di ℝ² ∖ Ω dà lo stesso controesempio per P = ∂_x∂_y. La domanda "per quali Ω non convessi vale la densità" resta aperta (open_questions).

---

## 6. [Hm]: limiti H^m uniformi nel tempo dalle leggi di Gardner

**Enunciato [S10B-T3].** Sia u ∈ C(ℝ; 𝒮(ℝ)) una soluzione liscia di u_t + u_xxx + 6uu_x = 0 (classe (Cl) di OP-F5D). Per ogni n ≥ 1, sup_{t∈ℝ}‖u(t)‖_{H^{n−1}} ≤ C_n(‖u(0)‖_{H^{n−1}}) < ∞.

L'esistenza globale in 𝒮 per dati di Schwartz resta un'ipotesi. È CON-FONTE secondaria (KVZ 2018 §1) e non è riprovata. Con S10B-T3, in S4ID-P8 e OPR2-P7 il fatto [Hm] cessa di essere una citazione: resta solo [GT-u].

**Prova.**

*Passo 1 (Gardner).* Identità algebrica sui getti (SymPy H1): se u = w + εw_x − ε²w², allora

  u_t + 6uu_x + u_xxx = (1 + ε∂ − 2ε²w)(w_t + 6(w − ε²w²)w_x + w_xxx).

La serie formale w = Σε^nw_n[u] che inverte la trasformazione è determinata da w_0 = u, w_n = −∂w_{n−1} + Σ_{i+j=n−2}w_iw_j. Se u risolve KdV, w risolve formalmente l'equazione di Gardner, perché l'operatore (1 + ε∂ − 2ε²w) è invertibile come serie formale (comincia con 1). L'equazione di Gardner è in forma di conservazione: w_t = −∂(3w² − 2ε²w³ + w_xx). Quindi, ordine per ordine in ε, D_Fw_n è una derivata totale e H_n := ∫w_n[u]dx è conservata per u ∈ C(ℝ; 𝒮). SymPy H2 lo controlla per n ≤ 8 (Euler(D_Fw_n) = 0).

*Passo 2 (omogeneità).* Con pesi wt(∂) = 1, wt(u) = 2, wt(ε) = −1, la trasformazione è omogenea di peso 2, quindi w_n è omogeneo di peso n + 2. Un monomio Π_{i=1}^dy_{j_i} (y_j = ∂^ju) ha peso Σ(j_i + 2) = n + 2. SymPy H4 lo controlla per w_{2n}, n ≤ 5.

*Passo 3 (parte quadratica, n generale).* La parte lineare di w_n è L_n = (−∂)^nu, una derivata totale per n ≥ 1. La parte quadratica Q_n soddisfa Q_n = −∂Q_{n−1} + Σ_{i+j=n−2}L_iL_j. Modulo derivate totali, con k = 2n − 2:

  ∫Q_{2n} = Σ_{i=0}^{k}∫∂^iu ∂^{k−i}u = Σ_{i=0}^{k}(−1)^{n−1−i}∫(∂^{n−1}u)² = (−1)^{n+1}∫(∂^{n−1}u)²,

usando (−1)^{i+j} = 1 e Σ_{m=−(n−1)}^{n−1}(−1)^m = (−1)^{n−1}. SymPy H3 lo controlla per n ≤ 5.

*Passo 4 (riduzione dell'ordine dei termini di grado ≥ 3).* In w_{2n} un monomio di grado d ≥ 3 ha D := Σj_i = 2n + 2 − 2d ≤ 2n − 4 derivate. Siano j_1 ≥ j_2 ≥ … . Se j_1 > j_2 + 1, una integrazione per parti sposta una derivata dal primo fattore: ∫y_{j_1}R = −∫y_{j_1−1}∂R. I monomi prodotti hanno un fattore con ordine j_k + 1 ≤ j_2 + 1 < j_1, e il potenziale Σj_i² decresce strettamente (j_1 > j_k + 1). Il processo termina con j_1 ≤ j_2 + 1 in ogni monomio, quindi j_1 ≤ (D + 1)/2 ≤ n − 3/2, cioè **j_1 ≤ n − 2**.

*Passo 5 (Gagliardo–Nirenberg).* Siano m := n − 1, X := ‖∂^mu‖_{L²} e M_0 := ‖u‖_{L²} (conservata: H_2 ∝ ∫u²). Per j ≤ m − 1:
- ‖∂^ju‖_{L²} ≤ CM_0^{1−j/m}X^{j/m};
- ‖∂^ju‖_∞ ≤ CM_0^{1−θ_j}X^{θ_j}, θ_j = (j + 1/2)/m < 1.

Per un monomio ridotto:

  |∫Πy_{j_i}| ≤ ‖y_{j_1}‖_2‖y_{j_2}‖_2Π_{i≥3}‖y_{j_i}‖_∞ ≤ C(M_0)X^γ,  γ = [D + (d − 2)/2]/m = (2n + 1 − 3d/2)/(n − 1).

Per d ≥ 3, γ ≤ (2n − 7/2)/(n − 1) < 2.

*Passo 6 (conclusione).* Per i Passi 3–5, X(t)² = ±H_{2n} + O(1 + X(t)^γ) con γ < 2 e costanti che dipendono solo da M_0. Poiché H_{2n} è costante, sup_tX(t) < ∞. Insieme a M_0 si ottiene sup_t‖u(t)‖_{H^{n−1}} < ∞. Non serve induzione. ∎

**SymPy `sympy/s10b_hm.py` (4/4 OK):**
- H1: identità di Miura–Gardner;
- H2: Euler(D_Fw_n) = 0, n ≤ 8;
- H3: parte quadratica di w_{2n} = (−1)^{n+1}y_{n−1}² mod derivate totali, n ≤ 5;
- H4: omogeneità di peso, n ≤ 5.

La prima versione dello script usava il segno di Gardner di u_t − 6uu_x + u_xxx (H1, H2 FAIL). Il segno è stato corretto per la convenzione del progetto: la correzione riguarda lo script, la prova sopra usa il segno corretto.

---

## 7. [GT-u]: esito (c)

**Fatto mancante.** Per S4ID-P8 e OPR2-P7 serve che l'errore di Grunert–Teschl (arXiv:0807.5041v2) Thm 5.4 (regione solitonica/oscillatoria x/t ≤ −C, errore O(t^{−α}), 1/2 < α < 1) sia **uniforme per x/t in compatti**.

**Lettura (pp. 20–24 del PDF).** Il problema di Riemann–Hilbert dipende da (x, t) solo tramite il punto stazionario k_0 = √(−x/12t) e tramite t. Le stime (5.20)–(5.21) usano una costante di Hölder L del dato riflessione deformato, che dipende da k_0. L'uniformità in k_0 non è enunciata. Coincide con F5D-11: "non trovata come enunciato".

**Riduzione.** [GT-u] ⟸ (U): *le costanti di (5.20)–(5.21) e la costante della soluzione del modello parabolico cilindrico sono limitate per k_0 in compatti di (0, ∞)*. Ogni passo di GT §5 è continuo in k_0: le deformazioni dipendono in modo C^1 da k_0, e la norma di Hölder del dato riflessione su un intorno di ±k_0 è continua. Quindi (U) è plausibile, ma la sua verifica richiede di riscrivere §5 con costanti esplicite, cosa non fatta qui. Pista alternativa: Deift–Zhou 1993/1994 (mKdV, uniformità in x/t sui compatti). È **non letta**, e nessuna sua formulazione è riportata qui.

**Esito.** Dopo §6 ([Hm] PROVA SCRITTA), **S4ID-P8 e OPR2-P7 sono CONDIZIONALI solo su [GT-u]**. Stato proposto: APERTO — ridotto a (U).

---

## 8. INT-Q1 (dati analitici): esito (c)

**Domanda.** Sia u(0) analitica con r ≢ 0. Esiste un'ODE autonoma in x soddisfatta da u(t) per ogni t?

**Pezzi già disponibili.**
- OPF5C-T6: le relazioni con origine non singolare danno code esponenziali; ordine ≤ 3 dà 0 o 1-solitone.
- S4ID-P8: asintotica radiativa con derivate, ora mod solo [GT-u] (§7). Il getto di u nella regione radiativa tende, dopo riscalamento, al getto della funzione di Airy/parabolica, e l'ideale limite è I_PW (OP-L2: ideale dei getti di v″ = cv).

**Combinazione.** Sia G una relazione autonoma soddisfatta da u(t, ·) per ogni t.
- Se l'origine non è singolare per G, si applica T6.
- Altrimenti si sviluppa G nella regione radiativa con S4ID-P8 (mod [GT-u]). La forma iniziale in(G) (parte di peso minimo nello scaling radiativo) deve annullarsi sul getto limite, cioè in(G) ∈ I_PW. Se in(G) ∉ I_PW si ottiene una contraddizione e r ≡ 0.

**Residuo esatto.** INT-Q1 ⟸ **(R)**: *nessuna relazione G con origine singolare e in(G) ∈ I_PW è soddisfatta da u(t) per ogni t, se r ≢ 0*. Per escludere (R) servono i termini **sottodominanti** dell'asintotica radiativa (correzioni t^{−1/2}·log, fase di Deift–Zhou), che S4ID-P8 non fornisce. La relazione cubica di Airy (OP-O5) è esattamente di questo tipo: in(G) ∈ I_PW e origine singolare.

Stato proposto: APERTO — ridotto a (R) mod [GT-u]. Non è un risultato nuovo oltre la combinazione; la combinazione è scritta qui per la prima volta.

---

## 9. OPF5C-Q1 (δ_N(K)): valori nuovi e riduzione

**L8′ (estensione di OPF5C-L8 a K = 2N).** L'argomento di L8 usa che i generatori del problema di eliminazione hanno forme iniziali che formano una successione regolare, così che il limite inferiore graduato a k = 0 si trasferisce a ogni k ∈ U_0. Per K = 2N il generatore aggiunto è y_{2N} − Φ(y_0, …, y_{2N−1}), con forma iniziale y_{2N}: è monico in una variabile nuova, quindi la successione resta regolare e L8 vale per K = 2N. È PROVA SCRITTA in forma breve: l'audit deve confermare che L8 non usa K ≤ 2N − 1 altrove.

**Calcolo graduato a k = 0 (computer-assisted)**, `sympy/s10b_delta.py` (copia di `OP-F5C/sympy/opf5c_delta.py`, invariata salvo intestazione), uscite `s10b_delta_K2N_graded.out` e `s10b_delta_big_graded.out`:

| N | K | grado minimo di una relazione omogenea | tempo |
|---|---|---|---|
| 1 | 2 | 2 | 0.0 s |
| 2 | 4 | 3 | 0.1 s |
| 3 | 6 | 4 | 0.7 s |
| 4 | 8 | 5 | 21.5 s |
| 5 | 10 | 6 | 3231 s |

Con L8′ ogni riga dà δ_N(2N)(k) ≥ N + 1 per ogni k. Insieme a OPR2-P4 (δ_N(K) ≤ N + 1 per K ≥ 2N): **δ_N(2N) = N + 1 per ogni k ∈ U_0, N ≤ 5** (computer-assisted, mod L8′). La congettura δ_N(2N) = N + 1 è confermata fino a N = 5.

**δ_5(8).** Il run concluso di OP-F5C (`OP-F5C/sympy/opf5c_delta0_5.out`) dà δ_5(8) ≥ 9 a k = 0 graduato, e con L8 il limite vale per ogni k. Con OPF5C-P7(b) (δ_N(2N − 2) ≤ N + 4 = 9): **δ_5(8) = 9**, in accordo con la congettura δ_N(2N − 2) = N + 4. δ_4(5) non è disponibile (uscita vuota, run non concluso).

**Run ancora in corso** al momento della consegna: (N, K) = (6, 12) e (6, 11). Non sono riportati valori per questi casi.

**Riduzione per N generale.** Le tre congetture equivalgono, via L8/L8′ e i maggioranti P4 e P7(b), a limiti **inferiori** graduati a k = 0: assenza di relazioni omogenee di grado ≤ N (per K = 2N), ≤ N + 1 (per K = 2N − 1) e ≤ N + 3 (per K = 2N − 2) tra le funzioni graduate di OP-F5C. È un problema di algebra commutativa graduata, senza parametro k. Stato: APERTO — ridotto al caso graduato.

---

## 10. OPR2-Q3: caratterizzazione esatta, ruolo di (I) e (II)

Quadro di OP-R2 §3.1 e OP-F5B §3. Un **criterio a test finiti** è un insieme finito {T_1, …, T_s} ⊂ 𝔇 tale che, per ogni u ∈ ℱ con Pu = 0: Ann_𝔇(u) = 𝔇P ⟺ T_iu ∉ 𝒯 per ogni i. Sia 𝓛 := {L_u : Pu = 0, Ann(u) ≠ 𝔇P}. Per OP-ALG-T4, L_u ⊋ 𝔇P esattamente quando u non è identificante.

**Proposizione [S10B-P10].** Esiste un criterio a test finiti ⟺ **¬(I)** (nessuna soluzione identificante) **oppure** 𝓛 ha un **insieme colpitore finito** in 𝔇 ∖ 𝔇P (T_1..T_s ∉ 𝔇P con ogni L ∈ 𝓛 contenente qualche T_i).

*Prova.*
- (⇐, primo caso) Se vale ¬(I), il test T_1 ∈ 𝔇P dà T_1u = 0 ∈ 𝒯 per ogni u, quindi il criterio dichiara ogni u non identificante, e ciò è corretto.
- (⇐, secondo caso) Se u non è identificante, qualche T_i ∈ L_u, cioè T_iu ∈ 𝒯. Se u è identificante, L_u = 𝔇P e T_i ∉ 𝔇P dà T_iu ∉ 𝒯.
- (⇒) Sia {T_i} un criterio corretto e valga (I). Se qualche T_i ∈ 𝔇P, il criterio fallisce sulla soluzione identificante u*. Quindi tutti i T_i ∉ 𝔇P. Per ogni u non identificante qualche T_iu ∈ 𝒯, cioè T_i ∈ L_u: l'insieme è colpitore. ∎

**Conseguenze.**
1. **(I) è necessaria** per il teorema "nessun test finito": senza (I) il criterio banale è corretto. (I) non si può rimuovere.
2. **(II) si sostituisce con (II′)**: *esistono infinite soluzioni u_λ con gli L_{u_λ} a due a due intersecanti in 𝔇P*. Infatti un T ∉ 𝔇P sta in al più uno di essi, quindi nessun insieme finito colpisce tutti. (I)+(II) implicano (II′) via OPF5B-T6 (u_λ = R_λu*). (II′) non richiede che gli endomorfismi di M si sollevino a 𝔇: basta realizzare infiniti atomi, o ideali che li contengono, con soluzioni qualsiasi.
3. **Teorema negativo esatto:** "nessun test finito" ⟺ (I) ∧ 𝓛 senza insieme colpitore finito. Con zoccolo ripetuto gli atomi sono infiniti (OPR2-P3′). Se ogni atomo è realizzato (∃u con L_u = atomo), allora vale (II′).

Stato proposto: P10 PROVA SCRITTA (elementare). OPR2-Q3: APERTO — ridotto a **realizzabilità degli atomi** (o di infiniti L_u a intersezione 𝔇P) per zoccolo ripetuto con M non spezzato, più (I) per P generale. Né un controesempio né una prova generale.

---

## 11. OPR2-Q2′: esito (c)

Il modello tangente è chiuso e la somma è diretta (OPF5B-P8). Per un poligono convesso limitato con tre trasporti a due a due non paralleli, la chiusura seguirebbe da:

**(L) Lemma di localizzazione.** Sia S = Σ_j ker Q_j su Ω poligono. Se ogni vertice ha un modello tangente con somma chiusa e diretta (P8) e i lati e l'interno non danno interazioni non compatte (OPR2-L1), allora la somma su Ω è chiusa. Formulazione: "Fredholm modulo vertici" per l'operatore di Gram dei proiettori, con partizione dell'unità e commutatori compatti, inclusi i termini d'ordine zero d_j.

Nessuna prova di (L) è stata scritta in questa sessione: i commutatori dei proiettori sui nuclei con i tagli non sono controllati. Stato: APERTO — ridotto a (L).

---

# Recepimento dell'audit (rev2) — S-CHECK-F10-B, 27/10/2026

Fonte: `work/CHECK-F10/AUDIT_S10-OPEN-B.md`. Nessun FAIL. Qui sotto ogni fix è applicato con il testo sostitutivo. Dove il testo dei §§1–11 è in conflitto con questa sezione, prevale questa sezione. Gli stati restano **proposti**: li registra il coordinatore.

## R1. S10B-T1 — fix T1-a, T1-b, T1-c

**T1-a (sostituisce, nel Passo 4, la frase «Nella convenzione di OPF5D-L3 il coefficiente di e^{−ikx} è b»).** Nella convenzione di OPF5D, ψ_−(k) = a(k)ψ_+(−k) + b(k)ψ_+(k). Dalle relazioni tra Wronskiani segue, per x → −∞,

  ψ_+(x,k) = a(k)ψ_−(x,−k) − b(−k)ψ_−(x,k).

Il coefficiente di e^{−ikx} nell'asintotica di ψ_+ a −∞ è quindi **−b(−k)**, e il coefficiente di e^{ikx} è a(k). Il Passo 4 mostra che il coefficiente di e^{−ikx} è nullo per ogni k ∈ ℝ∖0, quindi b(−k) = 0 per ogni k ∈ ℝ∖0, cioè **b ≡ 0**. Il coefficiente di e^{ikx} dà a(k) = Π_j(k − iκ_j)/(k + iκ_j) per k ∈ ℝ∖0.

**T1-b (aggiunta al Passo 4, prima dell'uso di OPF5D-L4).** Sia R(k) := Π_j(k − iκ_j)/(k + iκ_j). R è razionale con poli solo in −iκ_j, quindi è analitica in Im k > 0 e continua fino a ℝ. Per OPF5D-L3, a è analitica in Im k > 0 e continua fino a ℝ∖0. La differenza h := a − R è analitica in Im k > 0, continua fino a ℝ∖0 e nulla su ℝ∖0. Per il principio di riflessione di Schwarz h si estende analiticamente attraverso ℝ∖0, ponendo h(k̄)‾ nel semipiano inferiore, e si annulla su un intervallo reale. Per il teorema d'identità h ≡ 0 in Im k > 0. È lo stesso argomento di OPF5D-L9. Quindi gli zeri di a nel semipiano superiore sono esattamente iκ_1, …, iκ_N, e OPF5D-L4 dà lo spettro discreto {−κ_j²}.

**T1-c (sostituisce l'ultima frase dell'enunciato e il Passo 6).** S10B-T1 prova, **per ogni t fissato**, che il potenziale u(t) = 2(log f(·,t))″, con c_j(t) = c_j(0)e^{−8κ_j³t} > 0, ha u(t) ∈ 𝒮, b ≡ 0, a = R e spettro {−κ_j²}. Che t ↦ u(t) risolva KdV è il teorema di Hirota (1971), che **non** è provato qui. Nel progetto vale la convenzione già usata da INT-P5/P6 e OPF5D-C2: la classe dei multi-solitoni è *definita* dalla formula di Hirota, e il fatto che sia soluzione di KdV fa parte della definizione. Il V-ex dell'audit (`audit_hirota.py`: residuo ≤ 4·10⁻⁴¹ per N = 2, 3 in sei punti) lo conferma numericamente.

**Verifica rigenerata (punto 2 del mandato).** `sympy/s10b_f4.py noF1` (rev2: F5 con sostituzione esatta ed evalf a 60 cifre) → `sympy/s10b_f4_rev2.out`: **18/18 OK**.
- F2/F3 (segni e modulo di ρ, N ≤ 6, esatti): 12/12.
- F4 (Wronskiano, N = 2, 3): errore relativo ≤ 1.8·10⁻⁴¹.
- F5 (−∂² − u)ψ = k²ψ: residuo relativo 4.8·10⁻¹⁹⁷ (N = 2) e 4.4·10⁻¹⁹⁶ (N = 3).
- F6 (asintotica a x = ±40): ≤ 9·10⁻¹⁷, cioè di ordine e^{−40}, come atteso.

F1 (minori di Cauchy, N ≤ 4) è in `s10b_f4.out` (4/4 OK). Il FAIL di F5 nel run precedente era un artefatto di `lambdify`: vedi `s10b_f4_f5check.out`.

## R3. S10B-P3 — fix P3-a, P3-b

**P3-a (aggiunta al Passo 1).** L'insieme dei candidati {m_1, …, m_p}, cioè i minimi locali di u_0′ con valore critico < 0, è fissato **prima** delle perturbazioni ed è **invariato** da tutte le perturbazioni dei Passi 1–2:
- ψ_i sposta solo il valore critico u_0′(m_i) e lascia invariati i punti critici;
- θ_i ha supporto in una corona senza punti critici e non tocca né i punti né i valori critici.

Un minimo locale con valore critico 0 corrisponderebbe a un tempo infinito. Nel Passo 1 si sceglie inoltre ε **generico**, in modo che *nessun* valore critico di u_0′ sia nullo e che quelli dei minimi siano a due a due distinti (insieme di misura nulla da evitare, finitezza dei valori critici). Così ũ_0 resta in Morse+(SB) per perturbazioni C^3 piccole su (0, T] con T arbitrario, e l'apertura di F5A-12 si applica senza eccezioni.

**P3-b (aggiunta finale).** Tutte le perturbazioni ψ_i, θ_i hanno supporto in finestre di lunghezza < 2π attorno a punti di 𝕋, cioè sono funzioni periodiche ben definite. Il Passo 2 non crea problemi con i traslati m_i + 2πn: un minimizzante soddisfa X_{t_i}(a′) = x_i, mentre X(m_i + 2πn) = x_i + 2πn. La densità si misura nella norma C^r(𝕋):

  ‖ũ_0 − u_0‖_{C^r} ≤ Σ_i|ε_i|‖ψ_i‖_{C^r} + Σ_i|ε′_i|‖θ_i‖_{C^r} < ε_0,

con ‖ψ_i‖_{C^r}, ‖θ_i‖_{C^r} < ∞ perché sono C^∞. Osservazione dell'audit, recepita: nel Passo 2 la condizione 0 < ε < η_i è superflua (basta ε > 0, perché su C_i vale Φ + εΘ_i ≥ Φ ≥ Φ(m_i) + η_i). Resta invece necessaria la piccolezza rispetto ai margini del Passo 3.

## R4. S10B-L4 (L-loc) — fix L4-a … L4-e

**L4-a (ordine dei quantificatori, sostituisce l'inizio di 4.1).**
1. Si fissa z_0 > 0 minore di (i) il raggio in cui valgono le stime di Taylor di 4.2 e (ii) la distanza di a_b dagli altri punti critici di u_0′ (L4-b).
2. Dato z_0, per (SB) (M_{t_b}(x_b) = {a_b}), per la semicontinuità superiore di (t, x) ↦ M_t(x) e per la continuità di Φ_x(a) − min Φ_x, si scelgono r_b, τ_b, η_0 > 0 come in 4.1. Ciò è possibile per **ogni** z_0. Le code |a| → ∞ sul rivestimento sono controllate da (x − a)²/2t.
3. Si sceglie τ_b < dist(t_b, T_1 ∖ {t_b}) (L4-d) e τ_b < metà della minima distanza tra nascite.
4. Infine si sceglie ν_0 = ν_0(η_0, z_0) tale che il peso della regione |α| ≥ z_0, che è O(ν^{−1/4}e^{−η_0/2ν}) rispetto alla massa principale, sia ≤ ν² per ν ≤ ν_0.

**L4-b (sostituisce, in 4.3, «Il Passo 2 (integrale esterno) diventa …»).** Il Passo 2 di T1 usa globalmente «dx = J_t da, X_t crescente e biiettiva». Dopo la prima nascita questo è falso, perché J_t < 0 vicino ai minimi già passati. Lo si sostituisce con la **biiezione locale**: per |t − t_b| ≤ τ_b e t ≤ t_b, X_t è strettamente crescente sulla finestra W_b := {|α| < z_0}, perché J_t = (t/t_b)J_{t_b} + η > 0 su W_b∖{a_b} (u_0′ è monotona su ciascun lato di a_b, dato che z_0 è minore della distanza dagli altri punti critici). Per 4.1 il minimizzante a(x) di ogni x con |x − x_b| < r_b sta in W_b, quindi la mappa x ↦ a(x) è l'inversa di X_t|_{W_b} su X_t^{−1}(|x − x_b| < r_b) ∩ W_b. Lì dx = J_t da, e il Passo 2 si fa su quell'intervallo di a. Per la stessa scelta di z_0, J_t è monotona su ciascun lato di a_b (tu_0″ = ∂_aJ_t ha segno costante su ciascun lato), da cui ∫|∂_aJ_t|/J_t da = 2 log(1/max(√ν, η)) + O(1).

**L4-c (sostituisce, in 4.4, «La regione intermedia … è trattata come in T2(a) … con le stime L2 locali»).** Per t > t_b la finestra non è convessa, e le stime di 4.2 (valide solo per t ≤ t_b) **non** si applicano. Nella regione intermedia (|ξ| > Ξ, |x − x_b| < r_b) si usano le stime di OPF5A-T2, «Struttura», che sono locali in |z| ≤ z_0 e valgono qui senza modifiche:

  ψ(z) ≥ max(0, c_1(z⁴ + α²z²) − Cτz²),  ψ(z) ≤ C(z⁴ + α²z² + τz²),  per |z| ≤ z_0,

insieme al margine η_0 di 4.1 per |z| ≥ z_0. Su questa regione il minimizzante è unico e non degenere, come in T2(a), e la stima O(ν) di T2(a) si ripete con queste stime.

**L4-d (aggiunta a 4.3, parte esterna).** Con τ_b < dist(t_b, T_1 ∖ {t_b}) (L4-a, punto 3), nell'intervallo |t − t_b| ≤ τ_b non ci sono altri tempi di T_1. Quindi ogni minimizzante (t, x, a) con |x − x_b| ≥ r_b è non degenere: J > 0 su 𝒦_b, e per compattezza J ≥ 2j_0 > 0.

**L4-e (elenco dei punti in cui le prove originali usano convessità o unicità globale, con il sostituto locale).**

| punto della prova originale | uso globale | sostituto in L-loc |
|---|---|---|
| OPF5A-L2(b), coda \|z\| ≥ z_0 | convessità globale di Φ_x | margine η_0 di 4.1 (L4-a) |
| OPF5A-T1, Passo 2 | X_t biiettiva su 𝕋, dx = J_t da | biiezione locale di X_t su W_b (L4-b) |
| OPF5A-T2, «Struttura» e regione intermedia | stime su tutta la finestra | stime «Struttura» locali in \|z\| ≤ z_0 + margine (L4-c) |

Le identità del Passo 1 di T1 (⟨ψ′⟩ = 0, ⟨zψ′⟩ = 2ν) e lo sviluppo ψ′ = pz + qz²/2 + ρ_3 sono globali e valgono senza localizzare: servono solo le stime dei momenti, che vengono da 4.1–4.2. Il Lemma U e L3′ sono già locali, e il margine al posto della convessità era già in T2 dopo F5A-6. L'audit conferma che l'elenco è completo per quanto verificato.

**V-ex dell'audit (`audit_lloc.py`)**, con u_0 = sin x + 0.45 sin(2x + 1), seconda nascita t_2 = 1.8370: (I − pred)/ν è stabile a t_2 (−1.086, −1.085, −1.087 per ν = 10⁻³, 3·10⁻⁴, 10⁻⁴) e limitato a |t − t_2| = 0.02. È coerente con L-loc dentro la finestra. Chiude la domanda 7 di open_questions per la parte interna.

## R5. S10B-C1 — fix C1-a (sostituisce la nota «Lettura» del §5)

**Lettura (corretta).** L'ostruzione è il funzionale «rettangolo attorno al buco» Λ. Il controesempio vale per **ogni m ≥ 0** non appena esiste un rettangolo coordinato R = [x_1, x_2] × [y_1, y_2] tale che:
- le quattro strisce che contengono i lati di R stanno in Ω;
- ℝ² ∖ Ω contiene, dentro R, un **rettangolo coordinato chiuso con interno non vuoto** [p_1, q_1] × [p_2, q_2].

In questo caso si prende u = φ_1(x)φ_2(y), con φ_i ∈ C^∞, φ_i = 0 prima di p_i e = 1 dopo q_i: u_xy = φ_1′φ_2′ ha supporto nel rettangolo chiuso, fuori da Ω, e Λ(u) = 1.

Per un **foro puntiforme** l'affermazione precedente era falsa per m ≥ 1. Sia Ω = (0,3)² ∖ {p}. Per u ∈ H^1(Ω), u_xy ∈ H^{−1} ha supporto in {p}, quindi è una combinazione finita di derivate di δ_p. Poiché δ_p ∉ H^{−1}(ℝ²) (∫(1 + |ξ|²)^{−1}dξ = ∞), si ha u_xy = 0 sul quadrato, e la densità vale per OPF5B-T1 sul quadrato convesso. Per m = 0 invece il controesempio vale anche con un foro puntiforme: u = H(x − p_1)H(y − p_2) ∈ L², u_xy = δ_p è nullo su Ω e Λ(u) = 1.

**Condizione generale (per m fissato):** esiste u ∈ H^m(Ω) con P u = 0 su Ω (cioè supp u_xy ⊂ ℝ² ∖ Ω nel senso delle estensioni) e Λ(u) ≠ 0 per un rettangolo con lati in Ω. La domanda 6 di open_questions è precisata nello stesso senso.

## R6. S10B-T3 — fix R-1

S10B-T3 vale per soluzioni u ∈ C(ℝ; 𝒮(ℝ)). L'esistenza globale in 𝒮 per dati di Schwartz è l'ipotesi **(WP)**: CON-FONTE secondaria, la stessa di OP-C3′, non riprovata. Quindi **S4ID-P8 e OPR2-P7 sono CONDIZIONALI su [GT-u] e (WP)**, non «solo su [GT-u]» come nel §6 e nel §7. In LEDGER la colonna di [Hm] passa da «CON-FONTE secondaria KVZ» a «S10B-T3 mod (WP)».

## R7. [GT-u] — sostituisce il §7

La «riduzione» [GT-u] ⟸ (U) del §7 è **ritirata**: (U), cioè «costanti di GT (5.20)–(5.21) limitate per k_0 in compatti», è [GT-u] riscritto nelle costanti della prova di GT e non è un enunciato più semplice. Non ho né una prova di [GT-u] né un controesempio. La continuità in k_0 dei passi di GT §5 è plausibile ma non verificata, e Deift–Zhou non è letto.

**Stato: APERTO** (senza riduzione). Fatto mancante, come in F5D-11: l'errore O(t^{−α}) di GT Thm 5.4 è uniforme per x/t in compatti della regione x/t ≤ −C. S4ID-P8 e OPR2-P7 sono CONDIZIONALI su [GT-u] e (WP) (R6).

## R8. INT-Q1 (dati analitici) — sostituisce il §8

**Correzione.** Il ramo «origine non singolare ⇒ OPF5C-T6» del §8 è **tolto**. Per ordine ≥ 4, T6 dà solo code esponenziali, che non contraddicono r ≢ 0, quindi da solo non chiude quel ramo. Lo chiude S4ID-P8 stesso. «Origine non singolare» significa che G ha parte lineare non nulla, e P8 (mod [GT-u] e (WP)) esclude ogni relazione con parte lineare non nulla se r ≢ 0. Inoltre, per P8, la forma iniziale di ogni relazione soddisfatta sta in I_PW.

**Enunciato (R).** Per ogni soluzione u ∈ C(ℝ;𝒮) di KdV con u(0) analitico e r ≢ 0, nessun G ∈ ℂ[y_0, …, y_n] ∖ 0 con parte lineare nulla e forma iniziale in(G) ∈ I_PW soddisfa G[u(t)] ≡ 0 per ogni t.

**Proposizione [S10B-E8] (equivalenza, mod S4ID-P8, [GT-u], (WP)).** INT-Q1 ha risposta «no» (nessuna ODE autonoma in x) ⟺ (R).

*Prova.* (⇒) Se nessuna relazione esiste, in particolare nessuna della classe di (R). (⇐) Sia G ≠ 0 con G[u(t)] ≡ 0 per ogni t. Per S4ID-P8, se r ≢ 0 la parte lineare di G è nulla e in(G) ∈ I_PW. Dunque G sta nella classe di (R), il che contraddice (R). ∎

Questa è un'**equivalenza**, non una riduzione: (R) è INT-Q1 ristretto alla classe in cui P8 confina già ogni relazione. Per decidere (R) servono i termini sottodominanti dell'asintotica radiativa, e la relazione cubica di Airy (OP-O5) sta in questa classe. **Stato: APERTO.**

## R9. S10B-L8′ e δ_N — fix L8-a, L8-b; run N = 6

**L8-a (sostituisce, in §9, «con forma iniziale y_{2N}»).** Per OPF5C-L1 la mappa Ψ è un automorfismo polinomiale omogeneo pesato, e il flusso in x di Mumford (V′ = (V² + f)/U − (y_0 + λ)U, divisione esatta) è polinomiale e pesato. Quindi su Z_k vale y_{2N} = Φ(k; y_0, …, y_{2N−1}), con Φ polinomio omogeneo di peso 2N + 2 in (k, y). La **forma iniziale** del generatore aggiunto, cioè la componente di peso massimo in y, è

  y_{2N} − Φ(0; y_0, …, y_{2N−1}).

È monica in y_{2N}, una variabile nuova rispetto ai generatori (F⁺) di L8. Quindi non è divisore di zero modulo (F⁺), e la successione delle forme iniziali resta regolare.

**L8-b (enunciato e giustificazione di P_k^{(2N)}).** Sia I_k := P_k^{(2N−1)} = (F) ∩ ℂ[y_0..y_{2N−1}], l'ideale della varietà Z_k. È ridotto per OPF5C-T1(b) e coincide con l'ideale delle relazioni d'ordine 2N − 1 degli N-solitoni per T1(c). Allora

  P_k^{(2N)} = I_k·ℂ[y_0..y_{2N}] + (y_{2N} − Φ(k; ·)).

*Prova.*
- (⊇) Ogni generatore si annulla sui getti d'ordine 2N degli N-solitoni: I_k per T1(c), y_{2N} − Φ per il flusso di Mumford.
- (⊆) L'insieme 𝒥 dei getti d'ordine 2N degli N-solitoni è il grafico di Φ sopra l'insieme 𝒥′ dei getti d'ordine 2N − 1, che è denso in Z_k (T1(c)). Poiché Φ è continua (polinomiale), la chiusura di Zariski di 𝒥 è il grafico Γ di Φ|_{Z_k}. Γ è chiuso e la proiezione Γ → Z_k è un isomorfismo con inversa z ↦ (z, Φ(z)). Perciò ℂ[y_0..y_{2N}]/(I_k, y_{2N} − Φ) ≅ ℂ[y_0..y_{2N−1}]/I_k = ℂ[Z_k], che è ridotto. Quindi (I_k, y_{2N} − Φ) è radicale con luogo di zeri Γ, ed è l'ideale di Γ, cioè P_k^{(2N)}. ∎

Con L8-a e L8-b il resto di L8 si applica parola per parola. Lo script `s10b_delta.py` calcola y_{2N} dal flusso a k = 0, quindi valuta esattamente su V(F⁺, y_{2N} − Φ(0; ·)).

**Stati (dall'audit, recepiti).**
- δ_N(2N) = N + 1 per ogni k ∈ U_0: N ≤ 4 riprodotto dall'audit; N = 5 calcolato una sola volta (3231 s) e **non riprodotto**.
- δ_5(8) = 9: usa L8 (DIMOSTRATO), non L8′; **non riprodotto**.
- La riduzione di OPF5C-Q1 «a limiti inferiori graduati a k = 0» è una vera riduzione, perché elimina il parametro k (audit §9.3).

**Run N = 6 (punto 4 del mandato).** (N, K) = (6, 12) è stato avviato alle 17:27. Alle 20:55 era ancora in esecuzione senza uscita, dopo circa 3 h 28 min (il timeout 7000 s non ha avuto effetto sul processo Windows), ed è stato **fermato**. (6, 11) non è mai partito. Entrambi sono **NON ESEGUITI**, come annotato in `sympy/s10b_delta_big_graded.out`. Nessun valore per N = 6.

## R10. OPR2-Q3 — precisazione (sostituisce le Conseguenze 2–3 e lo stato del §10)

S10B-P10 è la **caratterizzazione**: esiste un criterio a test finiti ⟺ ¬(I) oppure 𝓛 ha un insieme colpitore finito in 𝔇 ∖ 𝔇P. Ne segue (Conseguenza 1, dimostrata con P10) che **(I) è necessaria** per il teorema «nessun test finito».

La realizzabilità degli atomi, o più in generale (II′), è solo una condizione **sufficiente** per l'assenza di un insieme colpitore finito, **non** una riduzione equivalente. L'implicazione (I)+(II) ⇒ (II′) via OPF5B-T6 è un'osservazione non auditata e non entra nell'enunciato.

**Stato: OPR2-Q3 APERTO**, nella forma esatta data da P10: con zoccolo ripetuto, (I) vale e 𝓛 non ha insieme colpitore finito?

## R11. OPR2-Q2′ — formulazione precisa di (L) e implicazione dimostrata (sostituisce il §11)

**Quadro.** Ω ⊂ ℝ² è un poligono convesso limitato con vertici v_1, …, v_V. Per j = 1, …, N (N ≥ 2), Q_j = n_j·∇ + d_j, con n_j ∈ ℝ² ∖ 0 a due a due non paralleli e d_j ∈ ℝ. K_j := {f ∈ L²(Ω) : Q_jf = 0 in 𝒟′(Ω)} è un sottospazio chiuso, con proiettore ortogonale P_j.

Sia ℋ := K_1 × … × K_N con ‖f‖²_ℋ = Σ_j‖f_j‖², S: ℋ → L²(Ω) definito da Sf := Σ_j f_j, e 𝒢 := S*S (S*g = (P_1g, …, P_Ng)). La somma K_1 + … + K_N è chiusa ⟺ ran S è chiuso. OPR2-Q2′ (congettura, caso m = 0) afferma che questa somma è chiusa.

**Partizione.** Siano χ_0, χ_1, …, χ_V ∈ C^∞(ℝ²) reali con Σ_{α=0}^V χ_α² = 1 su Ω̄, dove:
- χ_v ≡ 1 vicino al vertice v_v, con supporto in un disco B_v che non contiene altri vertici;
- χ_0 ≡ 0 vicino a tutti i vertici.

**Ipotesi (L).**
- **(L-int)** Per i ≠ j l'operatore P_i χ_0² P_j è compatto su L²(Ω). In parole: lontano dai vertici l'interazione tra classi di direzione diverse è compatta. È l'analogo, su tutto il complementare dei vertici, del meccanismo di OPR2-L1.
- **(L-v)** Per ogni vertice v esistono c_v > 0 e un operatore autoaggiunto compatto 𝒦_v su ℋ tali che

  ‖Σ_j χ_v f_j‖²_{L²} ≥ c_v Σ_j‖χ_v f_j‖²_{L²} − ⟨𝒦_v f, f⟩_ℋ  per ogni f ∈ ℋ.

  In parole: vicino a ogni vertice, la somma delle componenti localizzate è «diretta e chiusa modulo compatti».

**Proposizione [S10B-P11].** Se valgono (L-int) e (L-v) per ogni vertice, allora K_1 + … + K_N è chiusa in L²(Ω).

*Prova.* Sia f = (f_j) ∈ ℋ. Poiché Σ_α χ_α² = 1 su Ω,

  ‖Sf‖² = Σ_α ‖χ_α Σ_j f_j‖² = Σ_α ‖Σ_j χ_α f_j‖².

- *Termine α = 0.* ‖Σ_j χ_0 f_j‖² = Σ_j‖χ_0f_j‖² + Σ_{i≠j}⟨χ_0f_i, χ_0f_j⟩. Poiché f_i = P_if_i e f_j = P_jf_j, si ha ⟨χ_0f_i, χ_0f_j⟩ = ⟨f_i, P_iχ_0²P_jf_j⟩. Sia 𝒦_0 l'operatore su ℋ definito da (𝒦_0f)_i := −Σ_{j≠i}P_iχ_0²P_jf_j. È compatto per (L-int), ed è autoaggiunto perché (P_iχ_0²P_j)* = P_jχ_0²P_i. Allora Σ_{i≠j}⟨χ_0f_i, χ_0f_j⟩ = −⟨𝒦_0f, f⟩_ℋ, e la somma è reale perché ‖Σ_jχ_0f_j‖² e Σ_j‖χ_0f_j‖² lo sono. Quindi ‖Σ_jχ_0f_j‖² = Σ_j‖χ_0f_j‖² − ⟨𝒦_0f, f⟩.
- *Termini α = v.* Si usa (L-v).
- *Somma.* Con c := min(1, c_1, …, c_V) > 0 e 𝒦 := 𝒦_0 + Σ_v𝒦_v (compatto, autoaggiunto):

  ‖Sf‖² ≥ c Σ_α Σ_j ‖χ_αf_j‖² − ⟨𝒦f, f⟩ = c‖f‖²_ℋ − ⟨𝒦f, f⟩,

  usando di nuovo Σ_αχ_α² = 1. Quindi ⟨(𝒢 + 𝒦)f, f⟩ ≥ c‖f‖², e 𝒢 + 𝒦 è invertibile (autoaggiunto e coercivo).
- *Conclusione.* 𝒢 = (𝒢 + 𝒦) − 𝒦 è Fredholm, quindi ha immagine chiusa e nucleo di dimensione finita. Su (ker 𝒢)^⊥ = (ker S)^⊥, 𝒢 è limitato dal basso da una costante c′ > 0, e ‖Sf‖² = ⟨𝒢f, f⟩ ≥ c′‖f‖². Quindi S è limitato dal basso su (ker S)^⊥ e ran S è chiuso. ∎

**Stato.** S10B-P11 è PROVA SCRITTA (analisi funzionale elementare). **OPR2-Q2′ (m = 0, trasporti reali con d_j ∈ ℝ, poligono convesso) è APERTO — ridotto a (L-int) ∧ (L-v) per ogni vertice**, con l'implicazione dimostrata da P11.

**Rapporto con i risultati esistenti (non dimostrato qui).**
- OPF5B-P8 dà, sul cono tangente infinito con trasporti omogenei (d_j = 0) e nuclei esatti, una somma chiusa e diretta. Per il teorema della mappa aperta ciò equivale a ‖Σ_jg_j‖² ≥ c Σ‖g_j‖² per g_j nei nuclei del cono, cioè a (L-v) per il modello, con 𝒦_v = 0.
- Il passaggio dal modello a (L-v) sul poligono richiede che χ_vf_j sia, modulo errori compatti in f, un elemento del nucleo del modello tangente. Ostacoli: χ_vf_j non è nel nucleo (errore (n_j·∇χ_v)f_j) e i termini d'ordine zero d_j. Questo passaggio **non** è dimostrato.
- (L-int) **non** è dimostrata in questa generalità: OPR2-L1 tratta il criterio «proiettori a prodotti compatti ⇒ somma chiusa», non la compattezza localizzata lontano dai vertici sul poligono.

**Portata.** P11 non tocca i fattori d'ordine ≥ 2 né m ≥ 1, che restano aperti come nella riga di LEDGER di OPR2-Q2′.

## R12. Tabella degli stati dopo la rev2 (proposti)

| ID | stato proposto (audit + rev2) |
|---|---|
| S10B-T1 ([F4⁻]) | DIMOSTRATO (fix redazionali T1-a…c applicati); s10b_f4 F1 4/4, F2–F6 18/18; audit_f4 34/34 |
| INT-T1(B) | DIMOSTRATO, con la convenzione «multi-soliton = soluzione di Hirota» (T1-c) |
| S10B-T2, OPF5C-T5 | DIMOSTRATO (audit PASS) |
| S10B-P3 | PROVA SCRITTA, fix P3-a, P3-b applicati |
| S10B-L4, OPF5A-C1 | PROVA SCRITTA (fix L4-a…e applicati); C1: PROVA SCRITTA mod [F1] |
| S10B-C1 | DIMOSTRATO (nota «Lettura» corretta, C1-a) |
| S10B-T3 ([Hm]) | DIMOSTRATO per u ∈ C(ℝ;𝒮) |
| S4ID-P8, OPR2-P7 | CONDIZIONALE su [GT-u] e (WP) |
| [GT-u] | APERTO (riduzione ritirata) |
| INT-Q1 | APERTO; S10B-E8: equivalente a (R) mod S4ID-P8, [GT-u], (WP) (PROVA SCRITTA) |
| S10B-L8′ | PROVA SCRITTA (fix L8-a, L8-b applicati) |
| S10B-V9 | PROVA SCRITTA assistita da calcolo (N ≤ 4 riprodotto; N = 5 e δ_5(8) non riprodotti); N = 6 NON ESEGUITO |
| OPF5C-Q1 | APERTO — ridotto a limiti inferiori graduati a k = 0 (riduzione confermata dall'audit) |
| S10B-P10 | DIMOSTRATO (audit PASS) |
| OPR2-Q3 | APERTO, caratterizzato da P10 |
| S10B-P11 | PROVA SCRITTA (nuova, da auditare) |
| OPR2-Q2′ | APERTO — ridotto a (L-int) ∧ (L-v) via S10B-P11 (da auditare) |

Per T1, INT-T1(B) e C1 lo stato DIMOSTRATO è quello indicato dall'audit una volta applicati i fix redazionali. La registrazione spetta al coordinatore.
