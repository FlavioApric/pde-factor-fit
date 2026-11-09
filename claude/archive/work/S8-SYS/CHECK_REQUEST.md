# CHECK_REQUEST — S8-SYS → S-CHECK-F8 (e DEVIL-8 per i claim del cammino critico)
27/10/2026. Pacchetto: `work/S8-SYS/PROOF_PACKAGE.md`. SymPy: `work/S8-SYS/sympy/s8sys_checks.py` → `s8sys_checks.out` (32/32 OK). Righe proposte: `LEDGER_ROWS.md`. Il revisore riceva solo enunciati, ipotesi e prove (§ indicati), senza il resto del contesto.

## Ordine di priorità
1. **SYS-EX** (§2): criterio d'esistenza di una soluzione identificante, su ogni Ω aperto connesso. Cammino critico (identificazione L6). Chiedo anche il kill-argument a DEVIL-8.
2. **H-DIRAC-1/2** (§7): risposta alla domanda dell'utente su "λ ∈ Mat 4×4". Kill-argument richiesto.
3. **SYS-S1(i⇒), (i⇐), SYS-S1-C** (§3): scomposizione L6 e controesempio su Ω a U.
4. **SYS-E1–E3** (§5): versione corretta F2 di P1-T5 per i sistemi.
5. **SYS-C1, SYS-T0, LAME-3** (§§2, 4); **SYS-N3, G-T2** (§6).
6. SYS-T1 e G-T0 sono declassati: basta confermare il declassamento.

## Fatti esterni usati (da controllare come citazioni)
- Iniettività di C^∞(ℝ^n) e di 𝒟′(ℝ^n) come ℂ[∂]-moduli (Ehrenpreis–Malgrange–Palamodov; Malgrange, Sém. Bourbaki exp. 246; Oberst 1990). È usata **solo su ℝ^n**.
- Normalizzazione di Noether; una mappa finita è un rivestimento non ramificato fuori da un chiuso di Zariski proprio; il luogo liscio di una varietà irriducibile è connesso e Zariski-denso; Nullstellensatz.
- Stone–Weierstrass; principio d'identità per le funzioni olomorfe (una palla reale di dimensione d è un insieme d'unicità in ℂ^d).
- Koszul: Ext^i(R/m, R) = 0 per i < n; Auslander–Buchsbaum; teorema di de Rham per le correnti.
- Schwartz: le distribuzioni a supporto in {0} sono combinazioni finite di derivate di δ.
- P1-T5 (DIMOSTRATO nel progetto, `work/P1/CHECK_REQUEST.md` §C); C3-L3 e C3-T1 (progetto).

## Domande mirate
**SYS-EX.**
- Passo 2: la riduzione a un primo q con una relazione in cui compaiono solo i p ⊇ q è corretta anche quando la famiglia contiene più copie dello stesso primo non massimale, con palle disgiunte sulla stessa sezione s?
- È corretto usare h_0 ∈ ∏_{p ⊋ q} p con h_0 ∉ q per eliminare ν′ (che comprende i punti e^{λ·x} e i pezzi di sezioni di primi p ⊋ q)?
- Stone–Weierstrass: l'algebra {g(ℓ ∘ s)} ristretta a ∪_j B_{q,j} coincide con i polinomi complessi nelle variabili reali y. È chiusa per coniugio e separa i punti: va bene?
- EX-L2(b): da "r ∘ s ≡ 0 su una palla reale" si ottiene r ∈ q. Controllare il passaggio "aperto euclideo del luogo liscio ⇒ Zariski-denso in V(q)".
- Passo 3: l'estensione passa per C^∞(ℝ^n) e poi si restringe a Ω, senza mai usare l'iniettività di C^∞(Ω). Va bene per Ω arbitrario, anche non P-convesso?
- (i) ⇒ (ii) in 𝒟′: ker(∇ − λ) su 𝒟′(Ω) connesso è ℂe^{λ·x}: è corretto?
- Domanda di novità (per CIT-AUDIT-8): il caso Ω = ℝ^n è in Oberst 1990 o 1995?

**H-DIRAC-1.** L'argomento sul grado (la componente omogenea di grado massimo di W per (τI + α_0·ξ) è non nulla) è corretto in Mat_4(R)? Serve "τI + α_0·ξ non è un divisore di zero", che segue da det = τ^4 + … ≠ 0: va bene anche con W non quadrata? (W è 4×4.)

**H-DIRAC-2.** L'eliminazione e_top = (1/m) X e_bot in M_D dà M_D ≅ (R/q)² senza perdere relazioni? (SymPy C4 verifica YX − m² = (KG − m²)I.) Nel caso 1+1: "un ideale che contiene strettamente un primo di altezza 1 in ℂ[τ, ξ] ha colunghezza finita" e poi C3-L3: è corretto?

**SYS-S1.**
- (i⇐)(b): l'identificazione del complesso di Koszul di (∂_j − λ_j) su 𝒜 con il complesso di de Rham (coniugio per e^{λ·x}) e la dévissage su N di lunghezza finita sono corrette? Per 𝒟′ basta il teorema di de Rham per le correnti?
- SYS-S1-C: controllare che f ∈ C^∞(Ω), che i punti (1, 1/2) e (1, 5/2) stiano in Ω, che i segmenti {t} × [1/2, 5/2] stiano in Ω per t < 1, e che Ω sia semplicemente connesso.
- Il controesempio ha P = 0 (nessuna equazione). È accettabile come "sistema"? Se si preferisce un P non nullo, si può aggiungere una terza componente libera; non l'ho fatto.

**SYS-E.**
- SYS-E1: P1-T5 richiede 𝒜 = ℂ-algebra e tempi scalari g_i(t, m). Mat_2(ℂ[ξ]) con ε = m soddisfa le ipotesi?
- SYS-E3(c): "operatore invariante per traslazioni locale ⟺ simbolo polinomiale": basta Schwartz, o serve Peetre?
- SYS-E3(a): verificare che a = ½ arg z abbia un ramo continuo per ogni t quando ξ ≠ 0.

**SYS-N3.** La parte (c) per n ≥ 3 (k = rot Φ, con campo magnetico diverso) è scritta in modo sintetico: è sufficiente?

**LAME-3.** Controllare che la Smith su R_{(q_S)} abbia esponenti (0, 1, 1), cioè rango mod q_S = 1 e valutazione di det = 2, e il passaggio "r̄ᵀ[ξ]_× ∈ κξ ⟺ r̄ ∈ κξ" (usa ξ·ξ ≠ 0 in κ(q_S)).

## Punti che so deboli
- SYS-EX: i fatti di geometria algebrica di EX-L2 sono citati, non dimostrati. La novità su ℝ^n è dubbia.
- SYS-S1-C: vale solo per C^∞; il caso 𝒟′ è aperto (Q-S8SYS-2).
- II-T2(b′) derogatoria: non svolta (solo il controesempio alla versione ingenua).
