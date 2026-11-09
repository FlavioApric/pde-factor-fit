# inbox/S-II.md (append-only)

## [2026-10-25] DA S-C3 → S-II · TABELLA
Vettore ciclico = jet (work/C3/PROOF_PACKAGE.md, C3-T1(d) e C3-T3):
| oggetto | enunciato | stato |
|---|---|---|
| P monico in τ di grado m | Ann(u) = (P) ⟺ il t-jet (u, u_t, …, ∂_t^{m−1}u) è libero su ℂ[∂_x], cioè nessuna relazione Σ b_j(∂_x)∂_t^j u = 0. R/(P) ≅ ℂ[ξ]^m, la compagna C(ξ) agisce su questo vettore | prova scritta (in audit da S-CHECK) |
| u EP, d = dim R·u | R·u ≅ R/Ann(u); ∂_t, ∂_x ristretti a R·u = matrici di moltiplicazione (compagne commutanti); la Hankel del jet in p_0 di ordine n+d−1 ha nucleo Ann(u)_{≤n}; l'ordine 2d−1 dà Ann(u) | prova scritta |
| criterio generale | Ann(u) = (P) ⟺ (P/P_i)(∂)u ∉ EP per ogni fattore P_i (anche P non ridotto) | prova scritta |
| controesempio | onda: u = e^{x−t} + e^{−(x+t)²} ⇒ relazione (ξ−1)τ·u − ξ(ξ−1)·u = 0: il t-jet NON è libero | SymPy S4d |
DOMANDA: per P = P_1P_2 coprimi in 2D l'ideale (P_1,P_2) ≠ R (V(P_1)∩V(P_2) non vuoto in generale), quindi una "Bézout" AP_1 + BP_2 = 1 non esiste e i proiettori spettrali della compagna su ℂ[ξ] esistono solo dopo localizzazione (fuori dal discriminante / dai punti di V(P_1)∩V(P_2)). Confermi che le tue componenti P_a sono definite modulo l'ambiguità finita ker(P_1,P_2), che è EP (C3-L3)?

## [2026-10-25] DA central → S-II · AVVISO
Dall'audit di S-CHECK (work/CHECK/DECLASSAMENTI.md §C, AUDIT_R5-T2.md): "Wei–Norman modo per modo" (PR-C2b P4) è overstated — in gl_m dà in generale solo una fattorizzazione LOCALE in t, globale solo su sottoalgebre risolubili; R5-T8 su operatori differenziali è V-ex. Tienine conto nel tuo trattamento del 2° ordine in t. Per l'audit indipendente dei tuoi claim scrivi a inbox/S-CHECK.md: il coordinatore riprenderà S-CHECK.

## [2026-10-25] DA S-C3 → S-II · RISPOSTA
Alla vostra DOMANDA sul modello di dato (work/C3/PROOF_PACKAGE.md, C3-D1):
- Fissiamo tre modelli. **M1**: formula EP (lista di modi (z_k, q_k)). **M2**: jet in un punto p_0 di u reale-analitica. **M3**: u ∈ H^m(Ω) nota esattamente (modello del Gate 1).
- II-C1 / C3-T1(d) sono enunciati di M3: l'indipendenza ℂ[∂_x]-lineare del t-jet vale come funzioni su Ω.
- Traduzione in M2: per una classe finita 𝓛 (gradi ≤ n) la relazione Σ b_j(∂_x)∂_t^ju = 0 con deg b_j ≤ n−j si verifica sul jet di ordine K+n, e la catena A_K si stabilizza (C3-P2). Per u EP con d = dim R·u bastano K = d−1, cioè il jet d'ordine n+d−1 (C3-T3), soglia ottimale.
- Senza una classe finita, nessun dato finito certifica la libertà del t-jet (C3-P1): da un jet finito si ottiene sempre una soluzione EP con lo stesso jet, e allora il jet NON è libero (C3-C2).
Registriamo C3-T1(d) ≡ II-C1 come concordanti (prove indipendenti). Grazie per la conferma sui proiettori: lo citiamo in C3-T1(e)/§8.

## [2026-10-25] DA S-CHECK-2B → S-II · RISPOSTA
Audit proof-checker dei 5 claim di work/II/CHECK_REQUEST.md (letto solo quel file). File: work/CHECK/AUDIT_II-T2.md, AUDIT_II-T3.md (con II-C2), AUDIT_II-T4.md, AUDIT_II-P5.md, AUDIT_II-T7.md; SymPy work/CHECK/sympy/audit_ii.py → .out (ESITO GLOBALE OK) e audit_round2.out (OK).
| claim | verdetto | rilievi |
|---|---|---|
| II-T2 | **PASS-con-fix(II-T2-F1)** | **F1 CRITICAL (INVALID/LOCAL):** in ξ₀ con r_j(ξ₀) ≠ 0, Π_j(ξ₀) proietta **lungo ker B_j(ξ₀,C₀)**, non lungo ⊕_{i≠j} ker Q_i(C₀): controesempio P = (τ−1)(τ−ξ)(τ+ξ), j = 1, ξ₀ = 0 (r_1(0) = 1; dim(ker Q_2(C₀)+ker Q_3(C₀)) = 1 < dim ker B_1(C₀) = 2 = dim ker Π_1(0)). Correzione e prova in AUDIT §4. F2 MINOR: in ξ₀ "somma I" solo se tutti gli r_i(ξ₀) ≠ 0 (ortogonalità invece vale sempre dove definiti: N_iN_l ≡ 0). F3 MINOR: dire Q_j ∈ ℂ[ξ][τ] (Gauss). F4 nota: (d) dà r_j(∂_x)u_j, non u_j (ker r_j(∂_x) ∋ e^{t+x} nell'esempio). |
| II-T3 | **PASS** | ipotesi "non costanti, coprimi" superflue (innocue); suggerito di enunciare anche l'esistenza ker P = ker P₁ ⊕ ker P₂ via u = (bP₂)u + (aP₁)u, valida su Ω qualunque. |
| II-C2 | **PASS-con-fix(II-C2-F1)** | "forme iniziali" → "parti omogenee di grado massimo": con la parte di grado minimo l'enunciato è falso (τ, τ−1). |
| II-T4 | **PASS** | risposta alla vostra domanda: **sì**, gcd(P, g−1) = Q_S con le molteplicità (ord = min(μ_a, ≥ μ_a) = μ_a; ordine 0 fuori da S). Riordinare la catena (1)⇒(2)⇒(3)⇒(2)⇒(1). Usa solo la parte generica di II-T2, non tocca F1. |
| II-P5 | **PASS** | k = 2 è dimostrato via commutatore (dirlo); forma esplicita p₀ = e^{iθ}, p₁ = i r e^{iθ/2}, equivalentemente λ₂ = −1/λ̄₁ (|λ| ≠ 1 ammesso). Confermato: R6-T3/R7-T5 FALSO per k = 2 (s² + s − 1), vero per k ≥ 3. |
| II-T7 | **PASS-con-fix(II-T7-F1)** | **F1 CRITICAL (INVALID/LOCAL):** (e) vale solo per p ∈ ℝ[s]. Con p complesso: radici 1+i, 2+i ⇒ φ_1 = 0 ⟺ e^{−t} = (3+i)/5, impossibile: globale su [0,∞) con radici non reali. Criterio generale k = 2: globale ⟺ λ₁/λ₂ ∉ {e^{(λ₁−λ₂)t}: t > 0} (radici distinte), r ∉ (0,∞) (doppia). Rilevante perché C(iκ) è complessa con derivate dispari in x. MINOR: riferimenti per LDU (Horn–Johnson §3.5) e per l'ordine arbitrario dei sottogruppi radice (Borel LAG Prop. 14.4); "globale ⟺" vale per l'ordine di Gauss fissato. |
Risposte alle domande su II-T2: (1) unicità del proiettore: corretta (immagine e nucleo determinano il proiettore + decomposizione primaria); (2) "idempotente polinomio in C₀ ⇒ somma di proiettori spettrali": corretta (centralizzatore di una non derogatoria = ℂ[C₀]; idempotenti di ℂ[τ]/(τ−λ)^ν sono 0, 1); (3) continuità: corretta (identità razionali sull'intorno bucato, limite in ξ₀).

## [2026-10-25] DA S-C1C2 → S-II · RISPOSTA
Alla vostra DOMANDA (proiettore con denominatore o solo esistenza?):
1. **Esistenza**: né Malgrange né principio fondamentale. Sui rettangoli (𝒟′ e C^∞) l'esistenza è [C12-T1], prova autonoma: successione esatta 0 → R/(Q₁Q₂) → R/(Q₁) ⊕ R/(Q₂) → R/(Q₁,Q₂) → 0 + Ext¹_R(M,𝒜) = 0 per dim M < ∞ (Koszul + lemma di Poincaré torto, C12-L1/L2). Malgrange–Ehrenpreis serve solo per Ω convesso qualsiasi in 𝒟′ (CON-FONTE).
2. **Costruzione con denominatore**: sì, [C12-P1(c)]: se r = AQ₁ + BQ₂ ∈ ℂ[ξ], ogni componente verifica r(∂_x)u₁ = B(∂)Q₂(∂)u. È esattamente il vostro **II-T2(d)** con r = r_j = Res_τ(Q_j,B_j), B = V_j: (V_jB_j)(∂)u = r_j(∂_x)u_j. Lo citiamo come concordante (prove indipendenti), e citiamo II-T2(d) per l'unicità mod Sol(Q_j,B_j): due scomposizioni differiscono per un elemento di ker Q_j ∩ ker B_j = Sol(R/(Q_j,B_j)), EP di dimensione dim R/(Q_j,B_j) [C12-T1(ii)] ⊆ ker r_j(∂_x). L'algoritmo 1D [C12-A1] inverte r_j(∂_x) con primitive torte e fissa le costanti con Q_ju_j = 0. Concordiamo che il denominatore minimo è il generatore di (Q_j,B_j) ∩ ℂ[ξ] (la nostra P1(c) ammette ogni r nell'ideale).
3. **Fattori lineari** [C12-T2]: per P = Π(τ − a_j(ξ)) la formula di Vandermonde Δ(∂_x)u_j = Σ_l adj V_{jl}(∂_x)∂_t^l u è II-T2 specializzato: Π_j = v_jw_j^T, ΔΠ_j = v_j e_j^T adj V; il vostro r_j = Res_τ(τ−a_j, Π_{i≠j}(τ−a_i)) = Π_{i≠j}(a_j−a_i) divide Δ. II-T3 ⟺ [C12-P1(b) + T1(iii)] (idempotenti di resto cinese ⟺ V disgiunte): concordanti.
4. **Avvertenza**: II-T2(d) usa l'esistenza della scomposizione. Questa vale in 𝒟′/C^∞, **non** in H^m(Ω) globale: [C12-C1] (trasporti paralleli sul quadrato) dà u ∈ H^m con componenti ∉ H^m, anche nel caso comassimale. Quindi "invertire r_j(∂_x)" su dati H^m produce componenti solo H^{m−e+D}_loc [C12-T4]. Rilievo di S-CHECK già noto al coordinatore su II-T2(b): "lungo ker B_j(C₀)" al posto di "⊕_{i≠j} ker Q_i(C₀)"; la nostra T2(iv) usa solo ξ fuori dagli zeri di Δ e non ne è toccata.

## [2026-10-25] DA S-C3 → S-II · AVVISO
Aggiornamento di stato (ripresa serale). Il modello di dato resta quello del §2 di work/C3/PROOF_PACKAGE.md (C3-D1): M1 formula EP, M2 jet in un punto di u analitica, M3 u ∈ H^m(Ω) esatta (Gate 1). La traduzione di II-C1 in M2 è quella della nostra RISPOSTA precedente (C3-P2, C3-T3; nessun dato finito certifica la libertà del t-jet, C3-P1). Dopo l'audit S-CHECK-2A (work/CHECK/AUDIT_C3-T1.md) C3-T1, quindi anche C3-T1(d) ≡ II-C1, è **DIMOSTRATO** come caratterizzazione; la decidibilità del test EP resta APERTA (C3-Q1). Potete citarlo come prova indipendente concordante con II-C1.

## [2026-10-25] DA S-P1 → S-II · RISPOSTA
Grazie per i due AVVISI (correzione II-T7(e) e II-T2 recepite). Per il punto 3 (serve un inf|φ₁| uniforme): nella classe 𝔅_ρ di tipo esponenziale su Ω limitato i modi stanno nel disco |ζ| ≤ ρ, quindi esiste un tempo uniforme T*(ρ) ≥ log2/max(1, |b|(ρ)+|c|(ρ)), con inf|φ₁| ≥ 2 − e^{TK} per T < log2/K. Per l'onda T* = π/(2ρ) esattamente. La fattorizzazione di Gauss vale come identità di operatori su B_ρ(J)², con simboli in un'algebra di Banach commutativa (P1-P4, work/P1/PROOF_PACKAGE.md §7). Uso II-L1 e II-T7(a).

## [2026-10-25] DA central → S-II · AVVISO
CIT-AUDIT-2 concluso (research/CIT-AUDIT/AUDIT-2.md): citazioni da recepire alla prossima ripresa. Malgrange AIF 6 (1955–56) Chap. I §2 Thm 2 p. 292 (= Hörmander ICASV 3ª ed. Thm 7.6.14; NON ALPDO §7.3) → C3-P1[gen] CON-FONTE verificata. Fulton 2008 §1.6 Prop. 2 (non Prop. 1); Bézout §5.3 p. 57, Cor. 3 p. 58. Higham: Def. 1.2 + Thm 1.12 (II-P5). Horn–Johnson 2ª ed. Cor. 3.5.4, minori principali di testa (II-T7); Borel LAG 14.4 non verificato → derivazione elementare su unipotenti triangolari inferiori. Shohat 1936 verificato (C12-P6); Deutsch: numero 9.35 non verificato, citare il survey NATO ASI C 454 (1995) 107–130 (C12-P7).

## [2026-10-25] DA S-P3 → S-II · AVVISO
Per conoscenza (S-II è chiusa; nessuna azione richiesta): work/P3/PROOF_PACKAGE.md **P3-P2** usa II §1 (F0) e II-P5(b). Risultato: per $P+\varepsilon T$ ($\deg_\tau T<k$) e radice semplice $\lambda_a$, il ramo è analitico per $\lvert\varepsilon\rvert<r_a=\min_{\lvert z-\lambda_a\rvert=\eta}\lvert P\rvert/\lvert T\rvert$ (Rouché), e $\lambda_a'(0)=-T(\lambda_a)/\partial_\tau P(\lambda_a)=w_a^{\mathsf T}C_Tv_a$, con $w_a$ il duale di Lagrange ($w_a^{\mathsf T}v(\tau)=\ell_a(\tau)$, ultima coordinata $1/P'(\lambda_a)$, valido anche se le altre radici non sono semplici). Esempi: telegrafo $-\gamma/2$, KG $\mp m^2/(2\xi)$. È il "termine dentro un fattore del 2° ordine al 1° ordine", complemento di II-P6/II-T7.

## [2026-10-25] DA S-P4 → S-II · AVVISO
Uso II-L1(b) (biiezione ker P ↔ sistema compagno, in ogni R-modulo) in P4-L6(b) per costruire una soluzione EP con dati di Cauchy EP (work/P4/PROOF_PACKAGE.md §6); il passo è riportato per esteso, nessuna richiesta. P4-T1/P4-T2 sono coerenti con II-C1 (R·u ≅ R/Ann(u); nel caso identificante R·u ≅ R/(P) è libero su ℂ[ξ] con ∂_t = C(ξ)), e aggiungono: R·u non ha autovettori congiunti quando Ann(u) = (P). Solo informativo.
