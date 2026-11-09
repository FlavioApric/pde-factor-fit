# S10-OPEN-C — stato parziale (27/10/2026, sessione interrotta per limite d'uso)

Il lavoro si è fermato prima delle verifiche SymPy. Il primo tentativo di scrivere lo script è fallito per un errore di quoting della shell, quindi `sympy/` è vuoto. Non sono stati scritti né `PROOF_PACKAGE.md` né `CHECK_REQUEST.md`, `LEDGER_ROWS.md` e `open_questions.md`, e non esiste ancora una riga DONE.

Qui sotto ci sono, per ogni problema, l'esito previsto e lo schema di prova da sviluppare. Sono schemi, non prove auditate, e non vanno trattati come claim.

1. **VAR-P11(e), (a).** Sia y = A_0x + B(s)x. La derivata v risolve v(t) = T(t−s)y + ∫T(t−r)[B′u + Bv]dr. Poi si pone w = x + ∫v. Lemma: per f ∈ C¹, F = ∫T(t−r)f(r)dr è C¹, sta in D(A_0) e soddisfa A_0F = F′ − f. Gronwall dà u = w, che è classica. Ne segue che VAR-L2-cor passa a DIMOSTRATO, se l'audit conferma.
2. **VAR-Q18, (b).** X = ℋ ⊕ ℂ, B(t)(y,c) = (c·T(t)x, −⟨T(t)x, y⟩) con x ∉ D(A). B è antiaggiunto e continuo in norma, ma non C¹. Con dato (0,1) la soluzione ha y(t) = (sin(‖x‖t)/‖x‖)·T(t)x ∉ D(A). Risponde anche a ENC Q13: (H-P0) non è automatica.
3. **VAR-Q10, (a): esistenza con V = 0.** g = Σ_j e^{−ℓ_j^{−4}}B((t−α_j)/ℓ_j) sui gap di un Cantor grasso K, con B(s) = exp(−s^{−2} − (1−s)^{−2}). g è Gevrey 7/4 < 2, quindi la serie di Tychonoff converge ed è intera in x. Z(u) ⊃ K × ℝ ha misura positiva e interno vuoto. V = 0 e V′ = 1_Z sono entrambe leggi.
4. **VAR-Q17.** (a) per V(x) e per V_0(x) + v(t): si mollifica nel tempo, ψ_φ = e^{−itH}φ̂(H)ψ_0 ∈ D(H), poi si applica L2-cor. (c) per V(t,x): il commutatore crea una sorgente fuori da ω, e la continuazione unica fallisce in presenza di sorgenti.
5. **VAR-P12(d).** (b) nella classe quadratica: ω costante a tratti con θ_1 = π/2, θ_2 = 5π/2, ω_2 = 5ω_1, dà tr M = −5,2 < −2, quindi M non è un esponenziale in sl₂(ℝ). (c) per il log differenziale generale.
6. **VAR-C3Q2.** (a): per L monico, Ann(u) = A_2L ⟺ rank_B(A_2u) = m. (b) per VAR-Q12: u = f(x+t) con f = e^{e^y}.
7. **Q-S8SYS-1, dicotomia.** In forma formale g_1, g_2 ∈ ℂ[ξ][[t]], con 2a = arctan(ξ tan(ωt)/ω). A t fisso non esiste una parola finita con tempi polinomiali in ξ: si prende la parte scalare G = O(1/ξ), si applica il lemma sui polinomi esponenziali e si confronta con |G| ≥ |t|m²/(4ξ_n).
8. **II-T2(b′).** (a) criterio dei reticoli saturati. (b) la coppia A_1 = [[ξ,0,0],[0,−ξ,1],[0,0,−2ξ]] (senza polo) e A_2 = [[ξ,1,0],[0,−ξ,0],[0,0,−2ξ]] (polo 1/(2ξ)) ha la stessa forma di Jordan e gli stessi fattori Q e B.
9. **Maxwell Q6, (a).** Le sizigie (ξ,0,−τ,0) e (0,ξ,0,−τ) sono libere, quindi pd M ≤ 2 < 4 = n. Da questo zoccolo = 0, e SYS-EX dà un campo identificante.
10. **ENC-T2(c′), classe principale, (a) in forma forte.** u′ = u + e^{αt}f con (τ − α) ∤ P_*. Allora Ann(u′) = (P_*(τ − α)).
11. **ENC-Q4.** (a) per {q_0 + c} con DM-φ: Z = I + Volterra è quasinilpotente, quindi δ = 0. (c) per la lettura DM3 letterale.
12. **ENC-Q10.** (a) parziale con Darboux V_1 = −2∂²log u, u = x² + 2it, L = ∂_x − u_x/u. Encoder inverso ψ = u[∫χ/u + c(t)] con c′ = iκ. Il segno di V_1 nell'intertwining va verificato. (c) perché c dipende dalla storia.
13. **DICT-ILIM-Hs, (a).** Si usano la condizione del cono, il resto di Taylor, l'equivalenza delle norme sui polinomi per scaling e r = (‖f‖₂/M)^{2/(2s+2+N)}, da cui θ = 2/(2s+2+N).
14. **DICT-U3d-v, (a).** Interpolazione di Čebyšëv in λ su [0,Λ], con Λ_J = 4J/(e²T):
    ‖k − k_J‖_{L¹(0,T)} ≤ 2T(ΛT/4)^J/J!·μ([0,Λ]) + τ_k(Λ), dove τ_k(Λ) = ∫_{λ>Λ}dμ/λ e μ([0,Λ]) ≤ ‖k‖_{L¹}max(1/T,Λ)/(1−1/e).
    Su [δ,T] in norma sup l'errore è ≤ 2ε·k(δ/2) con J = O((T/δ)log(1/ε)), per ogni k c.m. I pesi hanno segno qualsiasi. L'ottimalità della dipendenza da τ_k resta aperta.
15. **DICT-Q3.** (c): ridotto a una divisione C^∞. (b): u = e^{−1/x²}1_{x>0} supera i test puntuale e formale, ma u″/u non è limitato, quindi non esiste V continuo. Per u analitica la divisione è decisa dal test formale (Malgrange, CON-FONTE).
16. **DICT-Q4.** (a): A(iii) vale ⟺ nessuna combinazione non banale degli atomi ha rango finito. La direzione (⇒) segue dal controesempio; la (⇐) usa il lemma di Amitsur sulla dipendenza lineare locale (CON-FONTE, non letto). (b): gli atomi di media D_if = ψ_i∫f certificano il fit con un solo dato esatto.
17. **Robustezza DM-δ / VAR-Q19, (a).** Il minimax vale Θ(ε^{1/3}) nella classe con |u| ≥ δ e derivate fino al terzo ordine limitate. Il limite inferiore usa due punti con h = εφ((x−x_0)/ε^{1/3}). Il limite superiore usa un interpolante consistente nella classe e P3(c) a 2ε.

Da fare:
- lo script SymPy, scritto con lo strumento Write e non con un heredoc;
- i quattro consegnabili;
- la riga DONE.

> **Superato (27/10/2026):** la sessione è ripresa e le consegne sono complete (PROOF_PACKAGE, CHECK_REQUEST, LEDGER_ROWS, open_questions, sympy 34/34). Questo file resta solo come traccia.
