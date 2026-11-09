# KA CONV-T2′ — input verbatim (S-CHECK-F8-CONV, 27/10/2026)

Estratto verbatim da `work/S8-CONV/PROOF_PACKAGE.md`: lemma di evitamento di §1.3 (righe 84–88, contesto necessario) e §1.3′ completa (righe 102–124). Segue la riga del ledger proposta (`LEDGER_ROWS.md`, riga 10).

## Contesto: §1.3, passo 1 (lemma di evitamento)
*Passo 1 (lemma di evitamento).* Siano m ≥ 0, L ≥ 0 e g₀(z) := e^{|z|²} su ℝ^n. Allora:
(i) Ann(g₀) = 0, e più in generale Q(∂)(h g₀) ≠ 0 per ogni polinomio h ≠ 0 e ogni Q ≠ 0. Infatti, per un polinomio h, ∂_j(h e^{|z|²}) = (∂_j h + 2z_j h)e^{|z|²}. Per induzione, se Q ≠ 0 ha grado q e parte omogenea di grado massimo Q_top, allora Q(∂)(h e^{|z|²}) = e^{|z|²}(Q_top(2z)h_top + termini di grado < q + deg h), dove h_top è la parte di grado massimo di h. Il prodotto Q_top(2z)h_top di due polinomi non nulli è non nullo.
(ii) Sia N^{>L}_{m,K}(g₀) := {Q ∈ R_{≤m} : ∂^β(Qg₀)(0) = 0 per L < |β| ≤ K − m}, definito per K ≥ m + L + 1 (altrimenti non ci sono righe con |β| > L). La catena è decrescente in K. La sua intersezione è formata dai Q per cui la serie di Taylor di Qg₀ (funzione intera) non ha termini di grado > L, cioè Qg₀ è un polinomio di grado ≤ L. Allora ∂_t^{L+1}(Qg₀) = 0, cioè τ^{L+1}Q ∈ Ann(g₀) = 0, quindi Q = 0. Per finitezza della dimensione esiste K̄ = K̄(m, L) ≥ m + L + 1 con N^{>L}_{m,K̄}(g₀) = 0. Cioè la sottomatrice M^{>L}_{m,K̄}(g₀) di M_{m,K̄}(g₀), formata dalle righe |β| > L, ha rango pieno di colonna r := dim R_{≤m}. Fissiamo r righe che formano un minore Δ(j) non nullo in j = jet(g₀).
(iii) Le righe |β| > L di M_{m,K̄}(j) contengono solo coordinate j_γ con L < |γ| ≤ K̄. Dunque Δ è un polinomio a coefficienti reali nelle sole variabili y := (j_γ)_{L<|γ|≤K̄}, ed è non identicamente nullo perché Δ(jet di g₀) ≠ 0. Il suo insieme degli zeri Z è chiuso e senza punti interni. Il box B := {y : |j_γ| ≤ γ!/|γ|!} ha interno non vuoto, quindi esiste y\* ∈ B ∖ Z.
(iv) Conclusione del lemma. Sia j′ un jet i cui coefficienti di ordine in (L, K̄] sono y\*, qualunque siano gli altri. Allora N^{>L}_{m,K̄}(j′) = 0, quindi N_{m,K̄}(j′) = 0. Se inoltre j′ è il jet di una funzione analitica u′, allora Ann(u′) ∩ R_{≤m} ⊆ N_{m,K̄}(j′) = 0.

## §1.3′
### §1.3′ [CONV-T2′] Il corollario sulla classe principale (ex CONV-Q10) — PROVA SCRITTA (riparazione proposta dall'audit F8, fix CONV-8; da auditare)
**Enunciato.** Sia n ≥ 2 e sia 𝒞 l'insieme delle funzioni intere reali u su ℝ^n con Ann(u) principale non nullo oppure Ann(u) = 0. Per ogni successione (φ_K) come in T2 esiste u ∈ 𝒞 su cui φ_K(j_K u) non converge alla risposta corretta. In particolare nessun learner identifica nel limite Ann(u) su 𝒞: un identificatore darebbe un decisore, con φ_K := "legge" se e solo se l'uscita al passo K è un ideale non nullo. (Per n = 1 ogni ideale di ℂ[τ] è principale, e l'enunciato coincide con T2.)
**Lemma (famiglia test).** Si scrive z = (t, x), con x ∈ ℝ^{n−1}. Siano q un polinomio di grado ≤ M, N := M + 2, ε ≠ 0 e v := q + ε t^{N−1}e^{|x|²}. Allora Ann(v) = (τ^N), quindi v ∈ 𝒞. Inoltre j_M v = j_M q, perché t^{N−1}e^{|x|²} ha ordine N − 1 = M + 1 in 0.
*Prova.* τ^N annulla v, perché il grado in t di q è < N. Sia Q ∈ Ann(v); si divide Q per τ^N, ottenendo Q = τ^N Q′ + Σ_{j<N} τ^j Q_j(ξ). Allora
 0 = Q(∂)v = P₀ + ε e^{|x|²} R(t, x), con P₀ := Σ_{j<N} Q_j(∂_x)∂_t^j q (un polinomio) e R := Σ_{j<N} c_j t^{N−1−j} r_j(x).
Qui c_j := (N−1)!/(N−1−j)! ≠ 0 e Q_j(∂_x)e^{|x|²} =: r_j e^{|x|²}. Per il punto (i) del lemma di §1.3, in n − 1 ≥ 1 variabili, r_j ≠ 0 se Q_j ≠ 0.
Se R ≠ 0, si fissa t₀ con R(t₀, ·) ≠ 0. Allora x ↦ e^{|x|²}R(t₀, x) = −P₀(t₀, x)/ε è un polinomio. Questo è impossibile: lungo una semiretta su cui R(t₀, ·) non è identicamente nullo, e^{|x|²}R(t₀, x) cresce più di ogni polinomio. Dunque R = 0. Poiché le potenze di t in R sono distinte, ogni r_j = 0, quindi ogni Q_j = 0 e Q ∈ (τ^N). ∎
*(Nota.* Confrontare solo il coefficiente di t^{N−1−j₀} chiude il caso j₀ = 0. Per j₀ ≥ 1 serve la separazione tra polinomio ed e^{|x|²}·polinomio, come sopra; osservazione dell'aggiudicatore.)
**Prova di T2′.**
*Passo 0′.* Se φ non converge a "legge" su qualche v = q + εt^{N−1}e^{|x|²} della famiglia test, basta u = v: v ∈ 𝒞 e la risposta corretta è "legge". Supponiamo d'ora in poi che φ_K(j_K v) → "legge" per ogni v della famiglia.
*Passo 2′ (costruzione).* Si parte da p_0 := 0 e H_0 := 0. Al passo k ≥ 0 è dato un polinomio p_k di grado ≤ H_k.
1. Si applica il lemma di evitamento (§1.3, passo 1) con m = k e L = H_k, e si pone L′_k := K̄(k, H_k). Si ottiene il blocco y\*_k sugli ordini (H_k, L′_k], e q_k := p_k + Σ_{H_k<|γ|≤L′_k}(y\*_{k,γ}/γ!)z^γ, di grado ≤ L′_k.
2. Si pone N_k := L′_k + 2, ε_k := 1/(N_k − 1)! e v_k := q_k + ε_k t^{N_k−1}e^{|x|²}. Per il lemma, Ann(v_k) = (τ^{N_k}). ε_k dipende solo da L′_k, noto prima di interrogare φ su v_k: non c'è circolarità.
3. Per il passo 0′ esiste H_{k+1} ≥ N_k − 1 (quindi H_{k+1} > L′_k) con φ_{H_{k+1}}(j_{H_{k+1}} v_k) = "legge".
4. Si pone p_{k+1} := T_{H_{k+1}} v_k, il polinomio di Taylor di v_k in 0 di ordine H_{k+1}.

*Passo 3′ (limite).* La costruzione modifica a ogni passo solo gli ordini > H_k, quindi la serie formale u := lim p_k è ben definita. I suoi termini di ordine in (H_k, L′_k] formano il blocco y\*_k. I suoi termini di ordine in (L′_k, H_{k+1}] sono quelli di ε_k t^{N_k−1}e^{|x|²} di ordine ≤ H_{k+1}, cioè ε_k t^{N_k−1}x^{2β}/β! con N_k − 1 + 2|β| ≤ H_{k+1}.
- *Interezza.* Si ha |u(z)| ≤ Σ_γ |z^γ|/|γ|! + Σ_k ε_k|t|^{N_k−1}e^{|x|²} ≤ Σ_k #{|γ| = k}‖z‖_∞^k/k! + e^{|t|}e^{|x|²}, perché gli N_k sono distinti. La serie converge assolutamente su ℝ^n (anzi su ℂ^n), e u è intera reale.
- *Il learner dice "legge" infinite volte.* Per ogni k, j_{H_{k+1}}u = j_{H_{k+1}}v_k: i passi successivi aggiungono il blocco sugli ordini (H_{k+1}, L′_{k+1}] e una coda di ordine ≥ N_{k+1} − 1 > H_{k+1}. Dunque φ_{H_{k+1}}(j_{H_{k+1}}u) = "legge" per ogni k.
- *Ann(u) = 0.* Per ogni k, i coefficienti di u di ordine in (H_k, L′_k] sono y\*_k, quindi Ann(u) ∩ R_{≤k} = 0 (lemma di evitamento, punto (iv)).

Allora u ∈ 𝒞, la risposta corretta è "nessuna legge", e φ dice "legge" infinite volte. ∎
**Stato.** PROVA SCRITTA. La riparazione è stata proposta dall'attaccante del kill-argument esterno su T2 e verificata dall'aggiudicatore (`work/CHECK-F8/KA_CONV_T2_adjudication.md`). Il testo qui sopra va auditato nel proprio ciclo.

## Riga ledger
| CONV-T2′ | (ex CONV-Q10) Nessuna successione di funzioni dei jet decide nel limite la dicotomia legge/nessuna legge sulla classe 𝒞 = {Ann principale ≠ 0} ∪ {Ann = 0}; quindi nessun learner identifica Ann su 𝒞 | n ≥ 2 | PROVA SCRITTA (riparazione proposta dall'audit, CONV-8; da auditare) | §1.3′ | — | da fare (nuovo testo) | riparazione nata dal KA esterno su T2 | CONV-T2 (lemma di evitamento) |

Notazione: R_n = ℂ[τ, ξ], τ ↔ ∂_t, ξ ↔ ∂_x; Ann(u) = {Q ∈ R_n : Q(∂)u = 0}; R_{≤m} = polinomi di grado ≤ m; N_{m,K}(j) = {Q ∈ R_{≤m} : ∂^β(Q(∂)u)(0) = 0 per |β| ≤ K − m}, scritto come nucleo della matrice M_{m,K}(j) le cui entrate sono coordinate del jet j_γ = ∂^γu(0).
