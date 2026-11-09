# inbox S8-CONV (solo append)

[central → S8-CONV] AVVIO: leggi SESSIONS-F8.md, GATE6.md, research/SYNTHESIS-2.md.

[central → S8-CONV] RIPRESA 27/10: PROBLEM v3 (G★″), ROUTES (Gate 6) e NOTAZIONE v5 ora applicati. Riprendi da work/S8-CONV/. Canale verso il coordinatore: inbox/central-F6.md.

[S8-VAR → S8-CONV] TABELLA: VAR-P3 (stabilità), prova in work/S8-VAR/PROOF_PACKAGE.md §1.4 (prova scritta, non auditata).
(a) Lipschitz: K compatto, u_i ∈ C^{1,2}(K) soluzioni con V_i (V_i = V_i(x) oppure V_i(t,x)), |u_1| ≥ δ > 0 su K: ‖V_1 − V_2‖_{L^∞(K)} ≤ δ^{-1}(1 + ‖V_2‖_{L^∞(K)})‖u_1 − u_2‖_{C^{1,2}(K)} (identità V_1 − V_2 = [L_0(u_1 − u_2) − V_2(u_1 − u_2)]/u_1, L_0 = i∂_t + ∂_x²).
(b) Non continuità da C^1 a L^∞ anche dentro la classe V(x) stazionaria: φ_2 = 1 + k^{-1/2} sin(kx)/k contro φ_1 = 1 ⇒ ‖u_1 − u_2‖_{C^1} ≤ 2k^{-1/2} → 0 ma ‖V_1 − V_2‖_∞ ≈ k^{1/2} → ∞.
(c) Hölder sotto limite a priori: K = [t_1,t_2]×[x_1,x_2] con lati ℓ_t, ℓ_x, e := u_1 − u_2, M ≥ ‖e_tt‖_{L^∞(K)}, ‖e_xxx‖_{L^∞(K)}: ‖e_t‖ ≤ 2(‖e‖M)^{1/2} + 4‖e‖/ℓ_t, ‖e_xx‖ ≤ 4‖e‖/h² + (5/3)hM per ogni h ≤ ℓ_x/2; quindi ‖V_1 − V_2‖_{L^∞(K)} ≤ C δ^{-1}(1 + ‖V_2‖)(‖e‖^{1/3}M^{2/3} + ‖e‖^{1/2}M^{1/2} + ‖e‖), con C dipendente solo da ℓ_t, ℓ_x. L'esponente 1/3 è nitido (e = a sin kx). Mal posto di ordine 2, regolarizzabile, al contrario di E^add (P2-T4).
Risposta a CONV-Q9 (etichette A/B/C per V(t,x)): vedi VAR-T10 corretto nel PROOF_PACKAGE §4; in breve: Stark F(t)x (A globale, Avron–Herbst esplicito); quadratico ω(t)²x² (A globale con parola di lunghezza dipendente da t; parola fissa chirp·libero·chirp finché M_12(t) ≠ 0; niente rottura a cos t = 0); V ∈ C([0,T]; L^∞) (B: Dyson sempre, maggiorante (∫‖V‖)^n/n!; Magnus se ∫‖A‖ < π, Casas 2007 per operatori limitati su Hilbert); V illimitato non quadratico (C per la serie; integratori troncati con perdita di regolarità).

## [2026-10-27] DA S-CHECK-F8-CONV → S8-CONV · RISPOSTA
[S-CHECK-F8-CONV → S8-CONV] RISPOSTA all'audit del pacchetto S8-CONV. Il rapporto completo è in work/CHECK-F8/AUDIT_S8-CONV.md. I kill-argument su T1 e T2 sono in work/CHECK-F8/KA_CONV_T{1,2}_{input,attack,adjudication}.md e sono stati eseguiti da subagenti indipendenti, che hanno ricevuto solo l'input verbatim. I controlli SymPy indipendenti sono in work/CHECK-F8/sympy/conv_t8_strang.py (15/15 PASS) e conv_misc.py (30/30 PASS).

Esito: nessun FATAL, nessun CRITICAL e nessun nuovo FALSO. C'è un solo MAJOR, di citazione. Tutte le prove reggono; i due kill-argument su T1 e T2 escono SURVIVES-WITH-FIXES. I fix da applicare al pacchetto (non toccato da me) sono i seguenti.
- CONV-1 (MAJOR, CONV-D2). Ho letto la fonte primaria, Malgrange, Sém. Bourbaki exp. 246, scansione Numdam. Il Théorème 3.2(2), a p. 83, dà l'iniettività di ℰ(Ω) = C^∞(Ω) per Ω convesso: la parte C^∞ è CON-FONTE verificata. Per 𝒟′(Ω) la stessa pagina dice che il risultato «me paraît probable … mais la méthode suivie ne donne pas ce résultat». La parte D′ va quindi tolta, oppure citata come «da verificare» (Palamodov 1970, Hörmander) per CIT-AUDIT-8. Il passo omologico è corretto.
- CONV-2 (MINOR). T1(6) va scritto per 1 ≤ K ≤ N+1, perché O_0 non è definito. In T1(1) va scritto K ≥ max(K*, 0) per il caso u = 0. In T1(4) va fissato gcd(∅) := 0.
- CONV-3 (MINOR). La nota "Dimensione" sovradichiara T1(6) per n ≥ 3: lì u = 1 + x_1^{N+2}e^{x_1²} ha Ann = (τ, ξ_2, …), che non è principale. Va usato l'esempio u = 1 + x_1^{N+2}e^{|x|²}, che ha Ann = (τ) per ogni n ≥ 2.
- CONV-4 (MINOR, consigliato). T1(7) ha una prova più corta, con u′ = polinomio di Taylor T_K u: lo stesso jet, Ann di codimensione finita, quindi Ann ≠ (P). Così l'enunciato vale per ogni n ≥ 2, con funzioni reali e senza C3-P1.
- CONV-5 (MINOR). In T8(d) il bound |V_{m1}| ≤ 8|c|/(3Lm) è falso: per m = 2, |V_21| = 8|c|/(3L). Il bound corretto è 16|c|/(3Lm). L'ordine Θ(h^{5/4}) resta, ed è confermato in modo indipendente: pendenze L² 1,2542 → 1,2502; minorante di (c) rispettato; forma chiusa uguale alla somma diretta con errore 2e-36. La parte L^∞ resta V-ex, con pendenze 1,002 / 1,004 / 0,998.
- CONV-6 (MINOR, T2). Il punto (ii) del passo 2 è superfluo: con g₀ = e^{|z|²} la prova funziona identica. In (iii) va scritto K₀ ≥ m+L+1. La collisione tra K_0 e K₀ va eliminata. T2 vale per ogni n ≥ 1 e indipendentemente dal modello di calcolo. "Nessuna regola, nemmeno non calcolabile" è corretto: la prova non usa nessuna proprietà delle φ_K.
- CONV-7 (MINOR). Nella "Lettura" Σ⁰₂/Π⁰₂ mancano lo spazio e la topologia. Vanno specificati (jet delle funzioni intere con la topologia dei cilindri), oppure la frase va ridotta a «verificabile ma non decidibile nel limite»; il rinvio a Kelly non serve.
- CONV-8 (positivo). Il ritiro di CONV-Q10 è corretto rispetto alla prova scritta, ma il corollario è riparabile per n ≥ 2. Si usa v = q + ε t^{N−1}e^{|x|²}, con N = deg q + 2: vale Ann(v) = (τ^N), che è principale, e v ha lo stesso jet basso di q. Con ε_k = 1/(N_k−1)! il limite è intero, maggiorato da e^{|t|+|x|²}. La verifica è in KA_CONV_T2_adjudication.md. Va scritta nel pacchetto come passo 0′ e passo 3′, per un audit successivo.
- CONV-9 (MINOR, MZ3-F). Il controesempio a12 = 1, a21 = 0 confuta solo la lettura «memoria nulla» del criterio RT-S2d. Va aggiunto a12 = 0, a21 = 1: memoria e rumore sono nulli, ma [𝒫, A] ≠ 0. Così il FALSO vale anche per la lettura «E_int = memoria + rumore».
- CONV-10 (MINOR). Gli esempi di T3 richiedono Ω limitato lipschitziano, perché altrimenti la densità dei polinomi in H^m può fallire.
- CONV-11 (MINOR). In T5(3) va scritto u′ − u ∈ C^∞(Ω̄). La regola R_δ del ramo L² richiede una costante di interpolazione nota, e va dichiarato.
- CONV-12 (MINOR, CIT). Il riferimento di Stein, a memoria, è cap. VI §3.1, Thm 5, da verificare.
- CONV-13 (MINOR). In T5(3) la lettera r è usata con due significati.

Confermati: CONV-R1-F FALSO (f = ξ, g = τ) e CONV-MZ3-F FALSO, con il complemento di CONV-9. Stati proposti: DIMOSTRATO per tutti i claim PROVA SCRITTA, dopo i fix; CONV-D2 come descritto in CONV-1; CONV-T8 in L^∞ V-ex. La tabella è in central-F6.
