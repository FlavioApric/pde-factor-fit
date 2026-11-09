# AUDIT OP-F5B · S-CHECK-18 · 26/10/2026
Bersaglio: work/OP-F5B/PROOF_PACKAGE.md (priorità da CHECK_REQUEST.md).
Skill caricate (lettura dei SKILL.md): skills-local/session-protocol, skills-local/claim-lifecycle (passi 3–4: proof-checker con revisore = subagente indipendente; kill-argument). Nessuno script _vendor eseguito.
Controlli propri: work/CHECK/sympy/s18_opf5b.py → s18_opf5b.out, **12/12 OK** (Leibniz per P generico di grado 3; temperanza di P̃ per la trave; azione destra su 𝒟/x𝒟 con prodotto di Weyl indipendente; P_r u_G = 0, (2t∂_x+x)u_G = 0, modi J_0; u_G non di A_1-torsione per ordine/grado ≤ 4; intrecciatore P_1∂_x = ∂_xP_2, R_λu* = (1+λ∂_x)u*_2, P R_λu* = 0; Gram del cuneo λ_min = 0.0054 > 0 su |σ| ≤ 40). Controlli, non prove.
Controlli dell'agente: opf5b_checks.out 21/21 OK (letto).
Kill-argument: T1 → KA_OPF5B_T1_{input,attack,adjudication}.md (**SOPRAVVIVE**); T2/P3/C4 → KA_OPF5B_T2C4_{input,attack,adjudication}.md (**SOPRAVVIVONO**). Subagenti lanciati con il solo file di input.

## Verdetti
| claim | verdetto | finding |
|---|---|---|
| OPF5B-L1 | **OK** | — |
| F1 (Hörmander 10.2.1) | **CON-FONTE (verificata, fonte secondaria)** con fix MINOR di enunciato | F5B-1 |
| F2 (Stein) | **CON-FONTE (verificata, fonti secondarie concordi)**; precisare Thm 5 | F5B-3 |
| OPF5B-T1 | **OK con fix MINOR** (KA sopravvissuto) | F5B-1, 2, 3, 4 |
| OPF5B-C1 | **OK con fix MINOR** | F5B-5, F5B-6 |
| OPF5B-T2 | **OK** per 𝒟; per A_2 **OK modulo CON-FONTE** (Ore, numero non verificato) | F5B-9 |
| OPF5B-P3 | **OK con fix MINOR** | F5B-7, F5B-8 |
| OPF5B-C4 | **OK** (KA sopravvissuto) | — |
| OPF5B-L5 | **OK** | — |
| OPF5B-T6 | **OK** | F5B-10 (nota) |
| OPF5B-P7 | **OK con fix MINOR** | F5B-11 |
| OPF5B-P8 | **OK** | F5B-12 (nota) |
| OPR2-Q3, OPR2-Q2′ residui | APERTO (PARZIALE) — corretto | — |
Nessun MAJOR, nessun FALSO.

## Verifica riga per riga — punti essenziali
### L1
(a) Taylor di p^{(α)} (somma finita, grado ≤ d) e simmetria ζ ↔ ζ+η: corretto; 1/P̃ temperato; P̃ ≥ c_P > 0 (la derivata d'ordine d del monomio direttore z^α è α!·coeff, le altre si annullano) corretto. (b) per definizione. (c) Young con φ̂ ∈ 𝒮: corretto (è Hörmander ALPDO II Thm 10.1.15 in forma elementare). (d) prodotto delle trasformate, corretto (Hörmander 10.1.8).
### T1
- **Passo 1.** K_0 compatto in Ω perché ∂Ω ⊂ ∪B(p_i,ρ/8); ricoprimento {Ω_0, B(p_i,ρ/4)} di Ω̄; partizione con Σθ_i = 1 su un intorno V di Ω̄: standard. Scelte indipendenti da ε: sì.
- **Passo 2.** Identità y₀+τ_i+q = (1−ε)y₀ + ε(z+q/ε), z = o+y₀−p_i, |z−o| ≤ ρ/2, |q/ε| < ρ/2 ⇒ z+q/ε ∈ B(o,ρ) ⊂ Ω; il lemma "(1−ε)y₀+εw ∈ Ω per y₀ ∈ Ω̄, w ∈ Ω" è corretto per convessi aperti. Conseguenza: |y₀−p_i| < ρ/4+ερ/4 ≤ ρ/2 e |y−y₀| < ερ/4 < ερ/2. Corretto; nessuna regolarità del bordo usata.
- **Passo 3–4.** Corretto (continuità delle traslazioni in H^m(ℝ²), |τ_i| ≤ ε·diam(Ω̄∪{o})).
- **Passo 5.** Leibniz P(∂)(θf) = Σ_α(∂^αθ/α!)P^{(α)}(∂)f: corretto (ricontrollato s18-1 per P generico). Il simbolo di P^{(α)}(∂) ha modulo |p^{(α)}| ≤ P̃; k = k_m/P̃ temperato; costante dipende solo dai θ_i fissati. Corretto.
- **Passo 6.** z = (φE)*g su un intorno di Ω̄ con φ = 1 vicino a Ω̄ − K (K fisso): corretto; ‖(φE)*g‖_{2,k_m} ≤ ‖φE‖_{∞,P̃}‖g‖_{2,k}, kP̃ = k_m. È esattamente il guadagno di Hörmander: nessuna ipotesi (ipoellitticità, simmetrie) su P.
- **Passo 7.** Per ψ ∈ C_c^∞(V_ε): ⟨θ_iPũ_i,ψ⟩ = ⟨Pũ_i,θ_iψ⟩ = 0 perché supp(θ_iψ) ⊂ V_ε ∩ supp θ_i ⊂ O_i (aperto, Pũ_i = 0 lì). [P,Σθ_i]ũ = 0 su V perché Σθ_i ≡ 1 su V (anche se Pũ ≠ 0 fuori da Ω). v − u = Σθ_iw_i − z su Ω. Corretto.
- **Passo 8.** Intorno metrico di un convesso è convesso; v ∈ H^m(W); (Pv)*ρ_η = 0 su W′ per η < η_1/2; v_η → v in H^m(Ω) (Ω + B_η ⊂ W); C12-T1′ (DIMOSTRATO, ipotesi H¹_dR = 0: W′ convesso la soddisfa) in C^∞; v_{η,j} ∈ C^∞(W′) ⊃ Ω̄ compatto ⇒ v_{η,j}|_Ω ∈ H^m(Ω). Ordine dei limiti (prima ε, poi η) corretto.
- **Tesi aggiuntiva** "⟺ chiusa ⟺ γ_N > 0 (⟺ c_F < 1)": segue da C12-P7(a),(b),(c) (DIMOSTRATO, Ω lipschitziano connesso: soddisfatto). Corretto.
- **Coerenza col LEDGER.** Nessuna somma "chiusa e non densa" registrata; il LEDGER (C12-P7) lascia "chiusa ma non densa" aperto: T1 lo esclude sui convessi. OPF-T5/OPF-P5 sono coerenti. Nessun CONFLITTO.
### T2, P3, C4
Ricontrollati a mano tutti i passi (vedi KA_OPF5B_T2C4_adjudication.md). In particolare: in (b)⇒(a′) cbQ₀ = cbQ − A″P ∈ 𝔇 ha grado < m e appartiene a N; P3(iii) 𝒟_πP ∩ 𝒟 = π-saturazione di 𝒟P; P3(vi) corretto; C4(a) f·P_r = Tf′ − ηf − η²f′, coefficiente di η^{d+1} = −(d+1)c_d ≠ 0; C4(b) coefficiente di s^r di H = β_r(−x/2)^r; passaggio Ω∩{x≠0} → Ω corretto (Ann su Ω ⊆ Ann su Ω′ = 𝒟P_r ⊆ Ann su Ω).
### L5, T6, P7
L5: E(1̄) = R̄, PR ∈ 𝔇P; L_{u*} = 𝔇P da T4; T ∈ L_{u_R} ⟺ TR ∈ 𝔇P ⟺ E_R(T̄) = 0. Corretto. T6: corretto; la forma dei test ("Tu ∉ 𝒯") coincide con OP-ALG-C1(iv) (LEDGER r. 113). P7(b): teorema cinese del resto, inversa c^{−1}(AP_2 − BP_1) verificata; iniettività di J via rango 1 e assenza di torsione corretta; R_λ = −c^{−1}(1+λJ)P_1 corretto; (c) ricontrollato (s18-8..11).
### P8
Unitarietà della Mellin con peso r dr (h(ρ) = e^ρf(e^ρω)) corretta; trasformata di F(n_j·y) = a_j^{−1+iσ}F^♯ corretta; Passo 4: radici s_j distinte (altrimenti la retta passa per 0), monodromia e^{2πiα} = e^{−2πσ} ≠ 1 per σ ≠ 0, residuo c_j/B_j per σ = 0: corretto; Passo 5: ψ′_{jk} = tan(φ−α_k) − tan(φ−α_j) ≠ 0, integrazione per parti O(1/|σ|): corretto.

## Findings
**F5B-1 (MINOR, T1/F1, §1 "[Fonte F1]").** Hörmander ALPDO II Thm 10.2.1 è enunciato in forma globale pesata: per ogni ε > 0 esiste una soluzione fondamentale E con E/cosh(ε|x|) ∈ B_{∞,P̃}; l'appartenenza a B^{loc}_{∞,P̃} ne segue (ed è la forma in cui il teorema è citato in letteratura). *Riparazione:* riscrivere F1 così e aggiungere "φE = (φ cosh(ε|·|))·(E/cosh(ε|·|)) ∈ B_{∞,P̃} per φ ∈ C_c^∞ (Thm 10.1.15)". Convenzione: Hörmander usa P(D), D = −i∂; il suo P(ξ) è il p(ζ) = P(iζ) del pacchetto, quindi P̃ coincide. Basta per l'uso fatto (solo φE).
**F5B-2 (MINOR, T1 ipotesi).** P ≠ 0 (c ≠ 0) è implicito; dichiararlo.
**F5B-3 (MINOR, F2).** Citazione precisa: Stein, *Singular Integrals and Differentiability Properties of Functions*, cap. VI §3.1, Teorema 5 (p. 181): domini a bordo "minimally smooth" (in particolare lipschitziani limitati) hanno un operatore d'estensione **unico per ogni k**, limitato W^{k,p}(Ω) → W^{k,p}(ℝⁿ). "Convesso limitato ⇒ lipschitziano": Grisvard, *Elliptic Problems in Nonsmooth Domains*, Cor. 1.2.2.3 (numero non verificato in questa sessione; fatto elementare).
**F5B-4 (MINOR, T1 Passo 4).** |τ_i| ≤ ε·|o − p_i| ≤ ε·diam Ω̄ (o ∈ Ω): la scrittura "ε diam Ω" va bene; aggiungere che w_0 = 0 e che la convergenza è uniforme sugli n+1 indici (finiti). Puramente redazionale.
**F5B-5 (MINOR, C1(c)).** "OPF-T5, OPF-P5(i) … casi particolari" vale solo per la parte di quei teoremi sui domini **convessi** (OPF-T5 copre anche domini non convessi con simmetria); scrivere "sui domini convessi limitati".
**F5B-6 (MINOR, C1(d)).** L'estensione a domini stellati rispetto a una palla è solo osservazione; va anche verificato che gli intorni W′ usati nel Passo 8 abbiano H¹_dR = 0 **e** contengano un intorno metrico in cui P(∂)v = 0 — lasciare come osservazione esplicitamente non auditata.
**F5B-7 (MINOR, P3 sintesi §0 e (iv)–(v)).** "T4 vale alla lettera ⟺ 𝒟/𝒟P senza π-torsione": la direzione "torsione ⇒ T4 falso" richiede che esista una soluzione con getto libero (b); altrimenti T4 è vacuamente vero. *Riparazione:* enunciare come (iv) + (v): senza π-torsione T4 vale; con π-torsione Ann_𝒟(u) ⊋ 𝒟P per ogni u ∈ ker P (quindi T4 fallisce esattamente quando qualche soluzione ha getto libero).
**F5B-8 (MINOR, P3(iv) prova).** "OP-ALG-T4 vale per P̂ su 𝒟_π (la prova di T4 e di L5 usa solo questo)" non è verificabile dal pacchetto. *Riparazione* (suggerita dal KA): applicare T2 con 𝔄 := 𝔄_π (i {π^N} sono un insieme di Ore in A_1, ad_π localmente nilpotente; P̂ monico ⇒ 𝒟_πP̂ saturato, T2(e)).
**F5B-9 (MINOR, T2 per A_2).** Ore di 𝔄∖0 in A_2 = 𝔄[∂_t;δ]: CON-FONTE McConnell–Robson §2.1 con numero non verificato. Resta CON-FONTE (non verificata); C4 non la usa.
**F5B-10 (nota, T6).** La formulazione coincide con OP-ALG-C1(iv) (test "Tu ∉ 𝒯_𝔄"). Non copre criteri di altra forma (es. test di nullità Tu = 0 o test non lineari): dirlo.
**F5B-11 (MINOR, P7(a)).** "ker E_λ saturato (nucleo di una mappa verso M senza torsione)" richiede M senza 𝔄-torsione, cioè M = 𝔇/𝔇P con P monico: aggiungere l'ipotesi a P7(a) (è nel quadro di T6 ma (a) è enunciato per M astratto).
**F5B-12 (nota, P8).** Nessun problema; il controllo numerico s18 conferma λ_min > 0 (0.0054) per la configurazione di B1. L'ostruzione residua (localizzazione) è dichiarata correttamente.

## Letteratura su OPF5B-T1
Ricerca svolta (web, 26/10/2026): non ho trovato l'enunciato di T1 (approssimazione **in H^m(Ω) fino al bordo** di ker_{H^m(Ω)}P con soluzioni su un intorno di Ω̄, ogni P a coefficienti costanti, Ω convesso) in letteratura in questa forma. Risultati vicini, tutti in topologie **locali** (convergenza sui compatti di Ω, non in H^m(Ω)): teoremi di approssimazione di tipo Runge di Malgrange (1955–56) e Hörmander (ALPDO II cap. X, sezione sull'approssimazione delle soluzioni delle equazioni omogenee; numero non verificato), e la loro estensione a coppie di aperti (Kalmes, arXiv:1804.08099, condizioni sufficienti per l'approssimazione di soluzioni su un aperto con soluzioni su un aperto più grande, anche per calore e Schrödinger). La tecnica di T1 (localizzazione + guadagno P̃ della soluzione fondamentale) è classica nella teoria B_{p,k} di Hörmander; l'enunciato fino al bordo è, per quanto verificato, nuovo nel progetto e va tenuto come risultato proprio (DIMOSTRATO) modulo F1, F2 CON-FONTE.

## Bibliografia verificata
1. **[F1] L. Hörmander**, *The Analysis of Linear Partial Differential Operators II: Differential Operators with Constant Coefficients*, Grundlehren 257, Springer 1983 (rist. Classics in Mathematics 2005), **Teorema 10.2.1**: ogni operatore P(D) ≠ 0 a coefficienti costanti ha una soluzione fondamentale in B^{loc}_{∞,P̃}; più precisamente, per ogni ε > 0 esiste E con E/cosh(ε|x|) ∈ B_{∞,P̃}. *Verifica:* numero e contenuto confermati dalla fonte secondaria C. O. Kiselman, "Analytic continuation of fundamental solutions to differential equations with constant coefficients", Ann. Fac. Sci. Toulouse Math. (6) 20 (2011), n. spécial, 153–182, §2 ("Hörmander 1983: Theorem 10.2.1"; ottimalità pp. 17–18). Testo primario non consultato. Stato: **CON-FONTE (verificata su fonte secondaria)**.
2. **[F2] E. M. Stein**, *Singular Integrals and Differentiability Properties of Functions*, Princeton University Press 1970, **cap. VI §3.1, Teorema 5, p. 181**: per un dominio a bordo minimally smooth (in particolare lipschitziano limitato) esiste un operatore d'estensione 𝔈, indipendente da k, limitato W^{k,p}(Ω) → W^{k,p}(ℝⁿ) per ogni k ∈ ℕ, 1 ≤ p ≤ ∞. *Verifica:* numero, pagina e contenuto concordi in più citazioni secondarie (es. arXiv:1812.02267 "On Stein's extension operator preserving Sobolev–Morrey spaces"; appendice di arXiv:2110.00395, Thm B.2 "[Ste70], Theorem 5, p. 181"). Testo primario non consultato. Stato: **CON-FONTE (verificata su fonti secondarie)**.
3. (di supporto, non verificata qui) P. Grisvard, *Elliptic Problems in Nonsmooth Domains*, Pitman 1985, Cor. 1.2.2.3 (aperto convesso limitato ⇒ bordo lipschitziano).
4. (di supporto, non verificata qui) J. C. McConnell, J. C. Robson, *Noncommutative Noetherian Rings*, AMS GSM 30, §2.1 (localizzazione di Ore in estensioni di Ore) — per T2 su A_2.
5. (contesto letteratura) T. Kalmes, arXiv:1804.08099 (approssimazione di tipo Runge per P(D), topologie locali).

## Righe LEDGER proposte
| ID | stato proposto |
|---|---|
| OPF5B-L1 | **DIMOSTRATO** |
| OPF5B-T1 | **DIMOSTRATO** modulo F1 (Hörmander ALPDO II Thm 10.2.1) e F2 (Stein cap. VI Thm 5) **CON-FONTE (verificate)**; proof-checker S-CHECK-18 26/10 OK-con-fix(F5B-1..4); kill-argument sì, SOPRAVVISSUTO |
| OPF5B-C1 | **DIMOSTRATO** (fix F5B-5; (d) osservazione non auditata) |
| OPF5B-T2 | **DIMOSTRATO** per 𝒟 = A_1[∂_t]; per A_2 modulo Ore CON-FONTE (numero non verificato) |
| OPF5B-P3 | **DIMOSTRATO** (fix F5B-7, F5B-8) |
| OPF5B-C4 | **DIMOSTRATO**; kill-argument sì, SOPRAVVISSUTO |
| OPF5B-L5, OPF5B-T6 | **DIMOSTRATO** |
| OPF5B-P7 | **DIMOSTRATO** (fix F5B-11) |
| OPF5B-P8 | **DIMOSTRATO** (no kill-argument) |
| OPR2-Q3, OPR2-Q2′ | **APERTO** (PARZIALE) |
Aggiornamenti: OPF-Q3 → CHIUSO; P2-Q1 → CHIUSO su ogni convesso limitato per ogni P; EX-Q1 → CHIUSO; EX-BES (u_G identifica) V-ex → DIMOSTRATO.
