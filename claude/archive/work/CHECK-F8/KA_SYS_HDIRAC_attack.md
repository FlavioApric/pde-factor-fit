# Kill-argument su H-DIRAC-1 / H-DIRAC-2 (con SYS-L0, SYS-C1)

Revisore ostile indipendente. Fonte letta: solo `KA_SYS_HDIRAC_input.md`. Verifiche: `work/CHECK-F8/sympy/sys_ka_hd_check.py`.

## 1. Attacco principale: H-DIRAC-2(d) è falso su Ω non connesso, e il pacchetto non dichiara la connessione

La notazione fissa Ω ⊂ ℝ^n come aperto qualsiasi. Né l'enunciato di H-DIRAC-2 né la sua prova chiedono che Ω sia connesso. La prova di (d), però, usa C3-L3, che vale solo «su Ω connesso». Anche (b) passa da SYS-C1, che è enunciato «su ogni Ω aperto connesso».

Ecco il controesempio a (d). Prendiamo Ω = B_1 ⊔ B_2, unione di due palle disgiunte in ℝ², e m ≠ 0. Scegliamo λ = (λ_0, λ_1) ∈ ℂ² sulla quadrica {KG(λ) = m²}. Esiste, perché la quadrica non è vuota. Poniamo ψ_2 = e^{λ·x} su B_1 e ψ_2 = 0 su B_2, poi ψ_1 = (p_0 − p_1)ψ_2/m. Allora ψ = (ψ_1, ψ_2) ∈ Sol(D_2), perché ogni componente risolve il sistema localmente.

- ψ_2 non appartiene a EP. Un esponenziale-polinomio è analitico reale su tutto ℝ². Se coincidesse con ψ_2, si annullerebbe sull'aperto B_2, quindi sarebbe identicamente nullo, e invece su B_1 vale e^{λ·x} ≠ 0. Dunque, secondo (d), ψ dovrebbe identificare D_2.
- ψ non identifica D_2. Ann(ψ_2) ⊇ m_λ, perché (ζ_j − λ_j)ψ_2 = 0 su entrambe le componenti. Inoltre m_λ ⊄ q, dato che m_λ ha colunghezza 1. Quindi Ann(ψ_2) ⊋ q, cioè ker φ_ψ ≠ 0.

La direzione «ψ_2 ∉ EP ⟹ ψ identifica» è quindi falsa. Il guasto è nel passo «ψ_2 è annullata da un ideale di colunghezza finita ⟺ ψ_2 ∈ EP», che su un Ω sconnesso diventa «EP a pezzi». Il difetto è reale ma si ripara in una riga: basta aggiungere «Ω aperto connesso» come ipotesi globale di H-DIRAC-2, oppure sostituire EP con «EP su ogni componente connessa». Oltre questo non sono riuscito a rompere nulla. La parte algebrica (eliminazione, primalità, colunghezza, identificazione dei coefficienti) regge a tutti i controlli che ho tentato. Per questo l'attacco ferisce, ma non uccide.

## 2. Punti secondari

1. **H-DIRAC-2 (b), (d); MAJOR.** È l'attacco del punto 1: l'ipotesi di connessione è nascosta. In (b) l'esistenza su Ω sconnesso resta vera (basta scegliere una ψ identificante su una componente e 0 sulle altre, perché l'annullatore può solo restringersi), ma la prova citata non la copre.
2. **H-DIRAC-1, «ambiguità di L in 𝒞 con lo stesso ψ»; attacco fallito.** Ho controllato la prova riga per riga. La componente di grado d+1 di W L_0 è solo W_d(τI + α_0·ξ). Questa matrice non è un divisore di zero a destra: da W_d A = 0 segue W_d · det A = 0 moltiplicando per adj A, e R è un dominio. Il caso d = 0 usa correttamente il coefficiente di τ. Il risultato non richiede ipotesi su m, su B singolare, su α hermitiane o sulla relazione di Clifford. Con SymPy, per α_0 e B_0 casuali e W di grado ≤ 1, l'unica soluzione è W = 0. Il teorema regge.
3. **H-DIRAC-2(a), «eliminazione e_top = (1/m) X e_bot con perdita di relazioni»; attacco fallito.** È un complemento di Schur. Con U = [[I, 0], [Y/m, I]] e C = [[I, X/m], [0, I]], entrambe unimodulari (det = 1), si ha U D C = diag(−m I, (YX − m²)/m) (verificato con SymPy). Poiché m ∈ ℂ^×, M_D ≅ (R/q)² esattamente, e non si perde nessuna relazione. Il caso m = 0 è escluso dall'enunciato, quindi non è un controesempio.
4. **Primalità di KG − m²; attacco fallito.** Una forma quadratica non degenere meno una costante non nulla è irriducibile per n ≥ 2. Per n ≥ 3, Q stessa è irriducibile, quindi non può scriversi come l_1 l_2 con forme lineari. Per n = 2, (l_1 + a)(l_2 + b) = l_1 l_2 − c forza a = b = 0 e quindi c = 0. SymPy conferma in 3+1 e in 1+1. Con m = 0 in 1+1 si avrebbe (p_0 − p_1)(p_0 + p_1), che è riducibile, ma il caso è escluso.
5. **(d), «ideale che contiene strettamente un primo di altezza 1 ha colunghezza finita»; attacco fallito.** R/q è un dominio noetheriano di dimensione 1, quindi ogni suo ideale non nullo ha quoziente artiniano. La direzione inversa (ψ_2 ∈ EP ⟹ Ann ⊋ q) è corretta anch'essa: un ideale J di colunghezza finita non è contenuto in q, perché R/q ha dimensione infinita su ℂ. Il caso ψ_2 = 0 è coerente con l'enunciato.
6. **SYS-C1, parte su Ass; MINOR.** La prova dimostra solo l'inclusione «Ass ⊆ fattori primi di det P». L'inclusione opposta segue perché Supp M_P = V(det P) e i primi minimali del supporto sono associati, ma il testo non lo scrive. In H-DIRAC-2(a) Ass è calcolato direttamente, quindi l'omissione non danneggia H-DIRAC.
7. **SYS-C1, riferimento; MINOR.** «Weibel 4.5, numerazione da verificare» è un riferimento aperto. Il fatto è comunque standard: grade(m, R) = n, quindi Ext^i(R/m, R) = 0 per i < n.
8. **«Lettura» e «Risposta», convenzioni; MINOR.** Con p_μ = i∂_μ, γ^0 D ha coefficiente iI su ∂_t, non I. Per entrare in 𝒞 serve un fattore −i. È innocuo, perché un'unità costante non cambia U_D, ma il testo non lo dice. La convenzione p ↔ ζ non è fissata (SymPy: con p = iζ, det D = (−τ² + |ξ|² − m²)²).
9. **(c), natura del «test»; MINOR.** «(ψ_3, ψ_4) R/q-indipendenti» riformula l'iniettività. Non è un criterio verificabile in un numero finito di passi, mentre la «Risposta» lo presenta come un test. In 3+1 non esiste un analogo di «non EP»: due componenti non EP ma dipendenti, per esempio ψ_4 = P(∂)ψ_3 con P ∉ q, non identificano. Il testo è coerente su questo, ma la parola «test» esagera.
10. **Rappresentazione chirale contro hamiltoniana, divisori di zero in Mat_4(R), ψ_2 ∈ EP; nessun difetto.** U_{γ^0 D} = U_D perché γ^0 è invertibile e costante. L'ambiguità per coniugio S, come dichiarato, compare solo fuori dal modello di dato DM3.

## 3. Verdetto

**WOUNDED (lieve).** H-DIRAC-1 sopravvive integralmente. In H-DIRAC-2, (a) e (c) sono corrette. (d), e formalmente anche la prova di (b), dipendono da un'ipotesi non dichiarata, Ω connesso. Senza di essa (d) è falso, come mostra il controesempio esplicito del punto 1. La correzione è banale e non tocca il contenuto matematico.
