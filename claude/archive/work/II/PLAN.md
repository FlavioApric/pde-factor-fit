# PLAN — S-II (Fase 3, prima ondata) · matrice/compagna/modulo e calcolo funzionale
Data: 2026-10-25 · Cartella: work/II/ · Inbox: inbox/S-II.md · Notazione: NOTAZIONE.md v2 (H0 = ℝ, Ω limitato, componente = fattore).
Appunti: D2–D5, E1–E5, F1–F6, G1–G6 (Idea II); item del piano II.1–II.4, E4, E5, F1/F2, F6, G6; G★′ punti 2–3 (PROBLEM.md).
Input letti: research/R6/REPORT.md (base), R7 §2–3, R5 §4, PR-C2b P4, RIPRESA §4.

## 1. Enunciati da affrontare (ID provvisori [II-…])
Setting comune: R = ℂ[τ,ξ] (τ ↔ ∂_t, ξ ↔ ∂_x), P ∈ R, M_P := R/(P); se P è monico in τ di grado k, C(ξ) ∈ Mat_k(ℂ[ξ]) compagna (ultima riga = −coeff.).
- **[II-L1] Riduzione al 1° ordine come equivalenza di moduli.** Per ogni R-modulo F (C^∞(Ω), 𝒟′(Ω), H^m(Ω)∩ker): u ↦ (u,∂_tu,…,∂_t^{k−1}u) è una biiezione ker_F P → ker_F(∂_t − C(∂_x)); coker(τI − C(ξ)) ≅ M_P. (D5, E1)
- **[II-T1] Completezza della via (b) e sua esistenza.** (i) M_P è ℂ[ξ]-modulo finito ⟺ il coeff. di testa in τ è una costante ≠ 0 (allora libero di rango deg_τP, base 1,…,τ^{k−1}, τ agisce con C(ξ)); (ii) due compagne sono simili su ℂ[ξ] (o su ℂ(ξ)) ⟺ stesso P; (iii) relazione con la via (a): σ_m(1,0) ≠ 0 ⇒ (i) con k = m; il viceversa è falso (calore). (E4, II.1)
- **[II-P2] Via (a) = forma iniziale = punti all'infinito di V(P).** σ_m(P) = P^h|_{ζ=0}; P e P+Q (deg Q < m) hanno lo stesso tensore; GL₂-covarianza. (D4, E3, E4)
- **[II-T2] Proiettori spettrali della compagna = componenti per fattore (con denominatore).** P = Q_1⋯Q_s monico in τ, Q_j coprimi a coppie. Il proiettore di Riesz Π_j(ξ) di C(ξ) sull'autospazio generalizzato di Q_j è razionale in ξ, Π_j = N_j(ξ,C(ξ))/r_j(ξ) con r_j = Res_τ(Q_j, P/Q_j); sul jet di ogni modo esponenziale agisce come indicatrice del fattore; lato soluzioni: se u = Σ u_j, u_j ∈ ker Q_j, allora N_j(∂)u = r_j(∂_x)u_j. (F1 corretta, G★′-2; contatto S-C1C2)
- **[II-T3] Proiettori polinomiali ⟺ varietà disgiunte.** Per P = P_1P_2 coprimi: esistono operatori polinomiali E_1,E_2 con E_ju = u_j su ker P ⟺ V(P_1) ∩ V(P_2) = ∅ in ℂ² ⟺ R/(P) ≅ R/(P_1) × R/(P_2) (mappa naturale). Altrimenti ambiguità Sol(P_1,P_2) (R2-T2). Esempi: calore traslato (sì), onda (no: costanti), trave (no: span{1,x}).
- **[II-T4] Solo i fattori danno proiettori a un valore.** Un proiettore spettrale Π_S di C(ξ) (S = insieme di rami) è razionale in ξ ⟺ ∏_{a∈S}(τ−τ_a)^{μ_a} è un fattore di P in ℂ[ξ][τ] coprimo col cofattore. I singoli rami τ_a(ξ) hanno proiettori solo localmente olomorfi fuori dal discriminante (monodromia = Galois). ⇒ "componente = fattore" DERIVATO dall'Idea II. (F1, F2, II.3)
- **[II-P5] F1 come scritta (v_a ⊗ v_a).** f(C) = Σ_aΣ_k f^{(k)}(λ_a)/k! (C−λ_a)^kΠ_a, Π_a = v_a w_aᵀ (duali = Lagrange/Vandermonde⁻¹). La forma ortogonale Σ f(λ_a) v_a v_a^* vale ⟺ C normale ⟺ λ_a λ̄_b è radice m-esima non banale dell'unità ∀a≠b ⟺ (m ≥ 3: p = s^m − c, |c|=1; m = 2: |a_0| = 1 e ā_0 a_1 = −ā_1). **Sospetta correzione di R6-T3/R7-T5** (che dichiarano s^m − c per ogni m): da verificare in SymPy e, se confermata, CONFLITTO.
- **[II-P6] Termini = perturbazioni di rango 1 della compagna; log-simbolo.** C(ξ) = S − Σ_k λ_k e_m r_k(ξ)ᵀ è affine nei coefficienti dei termini; i rami τ_a non sono affini per m ≥ 2 (controesempio); tr C = −p_{m−1} (Liouville) è l'unica parte additiva del log-det del propagatore. (II.3 ↔ C4.3, G★′-3)
- **[II-T7] Wei–Norman modo per modo su gl_m (2° ordine in t).** Per ogni ξ fissato, la fattorizzazione di Gauss/Wei–Norman e^{tC(ξ)} = (unipotente inf.)(diagonale)(unipotente sup.) esiste su [0,T] ⟺ i Wronskiani principali W(φ_1,…,φ_j)(t) del sistema fondamentale canonico sono ≠ 0 su [0,T], j = 1,…,m−1; per m = 2 condizione esplicita sulle radici (globale su [0,∞) ⟺ radici reali non entrambe positive); onda di Fourier (ξ = iκ): solo locale, t < π/(2|κ|). Lie{termini} = gl_2 per il telegrafo. (PR-C2b P4, G★′-3)
- **[II-P8] Spazio ridotto = sottospazio ciclico (E5, G6).** rank 𝔾_M(u) = min(M+1, deg p_u), ker = multipli di p_u; D agisce come compagna di p_u. (rifacimento compatto di R6-T4; contatto S-C3)
- **[II-T9] Vettore ciclico = jet (coeff. variabili).** Su D = ℂ(x)[∂]: Ann_D(u) = D·L_u; (M_u, u) determina L_u, M_u da solo solo a meno di similitudine di Ore (esempio 1 vs x). (II.2, G5; contatto S-C3)
- **[II-P10] RT-R6a (⋆-prodotto).** σ_KN: A_1 → (ℂ[x,ξ], ⋆), f⋆g = Σ_j (1/j!) ∂_ξ^j f ∂_x^j g è un isomorfismo di algebre; gr(⋆) = prodotto commutativo = via (a). ⇒ nessun invariante oltre D/DL ⇒ MERGE in RT-6 (calcolo, non struttura).
- **[II-D] Tabella degli invarianti (II.1)** con riferimento a ciascun enunciato; **decisione di struttura per il Gate 3**.

Fuori piano (non faccio): identificabilità su ℝ (S-C3), teorema di scomposizione per fattori in H^m(Ω) (S-C1C2: lo cito e lo uso come input), E_int per quadri (S-P1).

## 2. Skill (ordine d'uso)
1. `skills-local/session-protocol` (caricata, letta per intero).
2. `skills-local/claim-lifecycle` (letta): ciclo per ogni enunciato. Al suo interno `proof-writer` (letto: triage PROVABLE AS STATED / AFTER WEAKENING / NOT JUSTIFIED, mappa di dipendenze).
3. `_vendor/math-skill` modo `proof` (letto: esplorazione separata dalla prova, controesempi presto) — prima di ogni prova cerco controesempi in SymPy.
4. `_vendor/.../formula-derivation` (letto): per la catena "â = f(J·Φ)" (oggetto invariante = modulo M_P; classificazione identità/proposizione/interpretazione).
5. `_vendor/scientific-agent-skills/skills/sympy` (letto): script in work/II/sympy/, eseguiti con `.venv\Scripts\python.exe -I`, output salvati in .out.
6. Secondo revisore (proof-checker): S-CHECK via inbox/S-CHECK.md (DOMANDA con solo enunciato + ipotesi + prova). kill-argument: passaggio avversariale inline per i claim sul cammino critico (II-T2, II-T3, II-T4), dichiarato nel PROOF_PACKAGE (niente subagenti).
Nessuno script dei repository _vendor viene eseguito.

## 3. Fonti
Gantmacher vol. I cap. VI; Gohberg–Lancaster–Rodman 2009; Higham 2008 cap. 1; Kato cap. II; Lang, Algebra (risultante nell'ideale, CRT); Hörmander II §7.6 / Björk cap. 8 (principio fondamentale); Wei–Norman 1963/64; Coppel 1971 (Disconjugacy, Wronskiani); Jacobson 1943, Ore 1933, van der Put–Singer §2.1; Folland 1989 (calcolo di Weyl). Tutte già nel corpus di Fase 1 o classiche; i numeri di teorema non verificati saranno marcati.

## 4. Contatti
- S-C1C2: DOMANDA/TABELLA su II-T2/II-T3 (proiettori = componenti, denominatore = risultante, polinomiali ⟺ disgiunte).
- S-C3: II-T9/II-P8 (vettore ciclico = jet; spazio ridotto); chiedo il modello di dato fissato.
- S-CHECK: prove di II-T2, II-T3, II-T4, II-P5, II-T7.
- S-P1 (più avanti): II-P6/II-T7 come input per E_int modo per modo.
- central: PLAN-READY, eventuale CONFLITTO su R6-T3/R7-T5 (normalità della compagna), righe LEDGER, DONE.

## 5. Criterio di "fatto"
Tabella degli invarianti con ogni casella rimandata a un enunciato dimostrato (o CON-FONTE / V-ex dichiarato); prove complete di II-L1, T1, P2, T2, T3, T4, P5, P6, T7, P10 con script SymPy di controllo; prove inviate a S-CHECK; decisione di struttura motivata (via (b)+modulo; via (a) come invariante geometrico; RT-R6a merge sì/no); righe LEDGER proposte; DONE S-II.

## Ripresa 25/10 sera — recepimento audit
Input: RISPOSTA di S-CHECK-2B (inbox/S-II.md), work/CHECK/AUDIT_II-T2/T3/T4/P5/T7.md, RIPRESA.md (ultimo AGGIORNAMENTO). Skill: session-protocol (riletta per prima), claim-lifecycle (stato = ultimo controllo superato).
Azioni (in ordine):
1. PROOF_PACKAGE: applicare con l'id del fix — II-T2-F1 (Π_j(ξ₀) lungo ker B_j(ξ₀,C₀), prova AUDIT §4), F2 (ΣΠ_i = I solo dove tutti gli r_i ≠ 0; N_iN_l ≡ 0), F3 (Q_j ∈ ℂ[ξ][τ] per Gauss), F4 (nota su r_j(∂_x)u_j); II-T3-F2 (esistenza ker P = ker P₁ ⊕ ker P₂ via u = (bP₂)u + (aP₁)u) e F1 (ipotesi superflue); II-C2-F1 ("parti omogenee di grado massimo"); II-T4-F1/F2 (catena (1)⇒(2)⇒(3)⇒(2)⇒(1), conteggio 2^r); II-P5-F1/F2 (k = 2 via commutatore, forma esplicita); II-T7-F1/F2/F3 ((e) solo p ∈ ℝ[s]; criterio complesso k = 2; riferimenti Horn–Johnson §3.5, Borel LAG Prop. 14.4; ordine fissato).
2. Verificare le conseguenze di T7(e) corretta su onda, KG, telegrafo, termini con derivate dispari in x (ξ = iκ ⇒ p complesso), incluse le frasi inviate a S-P1. Script: work/II/sympy/s3_ripresa.py → .out.
3. Tabella degli stati nel PROOF_PACKAGE (DIMOSTRATO dove l'audit è passato); §10 se toccata.
4. AVVISO in inbox/S-P1.md (correzione II-T7(e) e II-T2), TABELLA aggiornata in inbox/central.md, "DONE S-II (ripresa audit)".
Fatto quando: tutti i fix marcati nel testo, script OK, messaggi inviati.
