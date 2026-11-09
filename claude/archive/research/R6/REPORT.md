# R6 — REPORT (Fase 1) · Idea II: formulazione matrice/tensore
Agente R6 · 2026-10-22 · Item: II (II.1, II.2, II.3; per II.4 vedi R7), domande E4, E5, F1/F2, F3–F6, G6, congettura G5, strade RT-5 / RT-6 (+ merge RT-S1h, RT-S1d).
Notazione: NOTAZIONE.md v1. Verifiche: research/R6/sympy/r6_checks.py → r6_checks.out (CHECK 1–11, tutte superate; .venv\Scripts\python.exe -I).
*(Salvato dal coordinatore dalla risposta finale di R6: la scrittura diretta era bloccata dall'ambiente.)*

**Skill caricate (Regola 2)**, lette con Read e seguite: academic-research-skills\deep-research\SKILL.md (lit-review, agente singolo); research-lit e arxiv (solo istruzioni, ricerca via WebSearch, nessuno script _vendor); math-skill (proof: esplorazione separata dalla prova, controesempi presto — uno trovato su un esempio proprio); sympy; formula-derivation (§4: COHERENT AFTER REFRAMING); scientific-critical-thinking (§7). anthropic-skills:deep-research non invocata (coordina sotto-agenti).

## 0. Sintesi
1. **Via (b) contro via (a).** La via (b) (compagna) conserva l'invariante completo: coker(sI−C) ≅ R[s]/(P), Smith diag(1,…,1,P) [R6-T1]. La via (a) (tensore omogeneo J^n_φ) conserva solo σ_m(P); per le ODE è un solo numero [R6-P1]. Risposta a E4: via (b); prezzo: rompe la covarianza GL₂ e richiede t non caratteristica.
2. **G5 corretta [R6-T5, T6].** Su ℂ(x) la "non-matrice" è una connessione e il gauge non conserva il polinomio caratteristico (CHECK 5). Invariante completo [D/DL] a meno di similitudine di Ore, Jacobson diag(1,…,1,L). L si recupera solo fissando il vettore ciclico = jet di u.
3. **F1 corretta [R6-T3].** f(C) = Σ_a Σ_k f^{(k)}(λ_a)/k! N_a^k P_a, proiettori obliqui v_a⊗w_a (duali = righe di V⁻¹); v_a⊗v_a solo se C normale ⟺ p = s^m−c, |c|=1. Componenti u_a = e₁ᵀe^{xC}P_aY₀ con E_int = 0.
4. **E5/G6 [R6-T4].** SVD del Gram/Hankel del jet di rango r (ordine dell'annullatore minimo); sullo spazio ridotto D agisce come C(p_u). Il "Σ D V" degli appunti è la SVD della catalecticante (apolarità).
5. **F6/G6 [R6-T7, L1].** Il simbolo principale si separa in potenze ortogonali ⟺ è odeco; m=2 sempre. Cubiche binarie: c₀c₂+c₁c₃−c₁²−c₂² = αβ(k₁−k₂)²(1+k₁k₂) = 0. Con GL₂: rango di Waring 2 per la cubica generica (Sylvester), ≥3 per m≥4.
6. **F2.** E-autovettori di una forma binaria f = radici di (X∂_Y−Y∂_X)f (generatore delle rotazioni); numero generico m (Cartwright–Sturmfels, n=2); non danno una decomposizione salvo il caso odeco.
7. **II.3 [R6-T8].** I rami τ_a(ξ) di V(P) sono gli autovalori di C(ξ); proiettori olomorfi fuori da Disc_τP; sul discriminante blocchi di Jordan (termini t·e^{τt}).
8. **Verdetto R4 su C3.3: confermato.** Le componenti sono i proiettori spettrali della compagna (pezzi di V(P)), non i termini T_k.
9. **R5.** La matrice E di B2 ha rango 1 (z⊗z), ordine k = z^{⊗k}: la via tensoriale non aggiunge invarianti.
10. **Raccomandazione Gate 3.** Struttura = via (b) + modulo (R[s]/(P) o D/DL) come oggetto canonico; via (a) come invariante geometrico del simbolo principale (tipo, direzioni, rango di Waring), con R7.

## 1. Setting
- ODE: p(D) = D^m+…+a₀, compagna C(p) con ultima riga (−a₀,…,−a_{m−1}).
- PDE: P monico in τ ha compagna C(ξ) ∈ Mat_m(ℂ[ξ]).
- Via (a): le derivate commutano ⇒ J^n_φ = ∂⊗…⊗∂ agisce solo tramite la parte simmetrica in Sym^n(ℂ²) (le antisimmetriche sono nulle); con i coefficienti J_{ω,λ} = λ⊗J_φ diventa σ_n(P) = Σ a_{jk}τ^jξ^k.

## 2. Tabella degli invarianti (II.1, E4)
| Oggetto | Via (a): tensore simbolo | Via (b): compagna / matrice su anello |
|---|---|---|
| ODE, coeff. costanti, ordine m | Sym^m(ℂ¹) ha dim 1: vede solo il coefficiente di testa [P1] | Fattori invarianti (1,…,1,p): completo; Jordan non derogatoria ⇒ classi x^k e^{λx} [T1, T2] |
| PDE (t,x), coeff. costanti | Forma binaria σ_m; invarianti SL₂/GL₂ (discriminante; tipo per m=2); O(2): m E-autovettori; ranghi delle catalecticanti e rango di Waring [T7]; non completo (perde l'ordine < m) | coker(τI−C(ξ)) ≅ ℂ[τ,ξ]/(P): completo se P monico in τ; Jordan su Disc_τP; rompe GL₂; simmetrie affini = automorfismi di ℂ[ξ] + shift, non gauge (R7) |
| Coeff. variabili | σ_m(x,ξ) invariante su T*ℝ (Hörmander III §18.1); simboli inferiori non invarianti; perde la non commutatività (gr A₁ = ℂ[x,ξ]) | Gauge A ↦ G⁻¹AG−G⁻¹G′: charpoly non invariante (CHECK 5); invariante completo [D/DL] (Ore), Jacobson; eigenring End_D(D/DL) rileva la decomponibilità (RT-S1d); L recuperato col vettore ciclico = jet di u [T6] |
| Spazio ridotto (E5) | HOSVD banale in 2 variabili (rango ≤ 2); utile la SVD delle catalecticanti | SVD di 𝔾/Hankel del jet: rango r, D agisce come C(p_u) [T4] |
| Calcolo funzionale (F1) | Solo per tensori odeco, con autovettori in più (Robeva 2016) | f(C) via Jordan/Hermite (Higham), proiettori obliqui; C normale solo per s^m−c, \|c\|=1 [T3] |

**Risposta a E4.** Via (b) completa sotto similitudine/gauge; via (a) solo la forma iniziale. Non vanno confrontate sotto lo stesso gruppo ((a) GL₂-covariante, (b) no): il comparatore corretto è il modulo M = R/(P) (o D/DL); (b) è una presentazione di M come R[τ]-modulo libero di rango m, (a) è la parte di testa di gr M.

**Merge di RT-S1h.** Le catalecticanti di σ_m sono Hankel nei coefficienti normalizzati; Waring σ_m = Σα_i(X+k_iY)^m ⟺ Prony c_j = Σα_ik_i^j (CHECK 8): stesso algoritmo di R4-T2 sul jet di u. Invarianti nuovi solo per la colonna (a) (rango di Waring, ranghi delle catalecticanti). Verdetto: MERGE come lemma-ponte.

## 3. Teoremi
**[R6-T1] DIMOSTRATO-CON-FONTE.** R commutativo, p ∈ R[s] monico. (1) sI−C ~ diag(1,…,1,p) su R[s], coker ≅ R[s]/(p). (2) Su un campo A ~ C(p) ⟺ A non derogatoria; due compagne simili ⟺ stesso p. Fonti: Gantmacher vol. I cap. VI; GLR 2009 cap. 1. Prova: il minore (m−1)×(m−1) senza prima colonna e ultima riga ha −1 in diagonale ⇒ Fitting₁ = R[s]. CHECK 1.

**[R6-P1] DIMOSTRATO.** Sym^m(ℂ¹) ≅ ℂ; σ_m(P+Q) = σ_m(P) se deg Q < m. Controesempio: ∂_t−∂_x² e ∂_t−∂_x²+c hanno lo stesso σ₂ ma nuclei diversi.

**[R6-T2] DIMOSTRATO-CON-FONTE** (Higham cap. 1, 10; GLR cap. 2). La prima riga di e^{xC} è una base di ker p(D); Jordan ha un blocco per radice ⇒ ker p(D) = ⊕ span{x^k e^{λ_a x}}. CHECK 2 (p = (s−1)(s−2)²).

**[R6-T3] DIMOSTRATO-CON-FONTE** (Higham Def. 1.2/1.4, Thm 1.12, numerazione da verificare; Kato I §5). f(C) = ΣΣ f^{(k)}(λ_a)/k! N_a^kP_a, P_a = q_a(C) (interpolazione di Hermite). Radici semplici: P_a = v_aw_aᵀ, v_a Vandermonde, w_a riga a-esima di V⁻¹ (Lagrange) = "duale e†" di C1.4. C normale ⟺ p = s^m−c, |c|=1 (CHECK 9; R7 S3g). Componenti u_a = e₁ᵀe^{xC}P_aY₀ ∈ ker(D−λ_a)^{m_a}, E_int = 0. CHECK 3.

**[R6-T4] DIMOSTRATO.** Coeff. costanti, annullatore minimo p_u di grado r. (i) M ≥ r: rank 𝔾_M = r, ker 𝔾_M = multipli di p_u di grado ≤ M. (ii) V_u = span{u,…,u^{(r−1)}} è D-invariante con matrice C(p_u)ᵀ. (iii) La SVD separa range (spazio ridotto) e kernel (annullatori). Prova: 𝔾 = BᵀG_bB, G_b ≻ 0. CHECK 4 (rango 3, dim ker 3 per M=5; Hankel 3×3 ≠ 0, 4×4 = 0). V_u = Z(u) di R4-T8.

**[R6-T5] DIMOSTRATO-CON-FONTE.** Su D = ℂ(x)[∂]: (i) forma di Jacobson diag(1,…,1,L) per matrici non singolari; (ii) vettore ciclico: ogni modulo differenziale di dim n è ≅ D/DL; (iii) D/DL₁ ≅ D/DL₂ ⟺ L₁, L₂ simili (Ore). Fonti: Jacobson 1943 cap. 3; Cohn 1985 cap. 8; Katz 1987; Ore 1933; van der Put–Singer §2.1; arXiv:1312.7096. CHECK 6: y₁′=y₂, y₂′=ay₁+by₂ ⇒ diag(1, ∂²−b∂−a); CHECK 5: gauge [[1,0],[x,1]] cambia il charpoly (+1), diag(1,eˣ) cambia la traccia di −1; (∂−1/x)∘x = x∘∂. Correzione di G5: vera a meno di similitudine e su ℂ(x)[∂]; su A₁ niente forma di Jacobson (A₁ non PID, Stafford 1978). La parte su (a) (solo simbolo principale) è vera.

**[R6-T6] DIMOSTRATO.** u olonoma ⇒ M_u = D·u ≅ D/DL_min e la compagna di L_min è la matrice di ∂ nella base del jet di u; un'altra base G dà vettore ciclico G⁻¹e₁ e un operatore simile, non uguale. Identificare L = scegliere il vettore ciclico (coerente con R4-T7a).

**[R6-T7] DIMOSTRATO (n=2) / CON FONTE.** (i) m=2 sempre odeco (teorema spettrale) ⇒ forma canonica per rotazione (Courant–Hilbert II cap. III). (ii) Odeco come in Robeva 2016; per n=2 l'ideale è generato dalle equazioni di Robeva. (iii) [R6-L1] c_j = αk₁^j+βk₂^j ⇒ c₀c₂+c₁c₃−c₁²−c₂² = αβ(k₁−k₂)²(1+k₁k₂) (CHECK 11); X³+3X²Y+Y³ è odeco (quadrica 0, 1+k₁k₂ = 0); (X+Y)³+(X+2Y)³ non è odeco (quadrica 3): si separa in direzioni oblique ma non per rotazione. Una prima stesura che dichiarava non odeco il primo esempio era errata ed è stata corretta. (iv) Sylvester (Iarrobino–Kanev §1.3): rango di Waring generico ⌈(m+1)/2⌉; cubica generica in 2 direzioni oblique, m≥4 servono ≥3 (CHECK 8). (v) E-autovettori = zeri di (X∂_Y−Y∂_X)f, in numero m (CHECK 7: 3, 4, 5 con 3, 4, 2 reali); H-autovalori 2(m−1) (Qi 2005). Interpretazione: F6 = decomposizione di Waring; G6 "ruotare" = caso odeco; i termini di ordine inferiore richiedono la via (b).

**[R6-T8] DIMOSTRATO-CON-FONTE** (Kato II §1–2; R5-T10). P monico in τ: gli autovalori di C(ξ) sono i rami algebroidi di V(P); proiettori P_a(ξ) olomorfi fuori da Z (discriminante e coincidenze), su Z blocchi di Jordan (CHECK 10: τ²+2ξτ+ξ⁴, Disc = −4ξ²(ξ²−1), Jordan non diagonale per ξ ∈ {0, ±1}). Fuori da Z: û = Σe^{tτ_a(ξ)}P_aÛ₀. Log-simbolo additivo nei termini solo per m=1 (C4.3); per m≥2 solo Σ_aτ_a = −p_{m−1} è lineare nei coefficienti (conferma R4 e PR-C2b P4). Per P=P₁P₂ coprimi i rami si raggruppano per fattore = decomposizione primaria (RT-1, R2).

## 4. formula-derivation per â = f(J·Φ): COHERENT AFTER REFRAMING
- Φ = jet di u su V_u, J = C(p_u)ᵀ.
- f è una funzione di matrice: exp(x·) dà la soluzione, (z−·)⁻¹ il risolvente (= Padé, R4-T3), log il log-simbolo.
- â = charpoly(J) (Cayley–Hamilton), non f(J); le componenti sono f(J)P_a.
- F4 ("lavoro su f e Φ indipendentemente") vero: Φ fissa la base ciclica, f la funzione spettrale.
- Non coerente come scritta: la versione tensoriale Σf(λ_a)v_a⊗v_a con J ∈ 𝒯ⁿ (vale solo per tensori odeco, non canonica).

## 5. Raccordi
- R4: C3.3 confermato; R4-T3 = risolvente della compagna; R4-T8 = R6-T4(ii).
- R5: E^{(2)} di rango 1 (z⊗z), ordine k = z^{⊗k}, nessun invariante tensoriale nuovo; Kato = R6-T8; con coeff. variabili l'algebra di Lie dei termini agisce per gauge sulla connessione.
- R7: simmetrie affini sulla compagna = automorfismi di ℂ[ξ] + shift, non gauge; simmetrie affini ⟺ P∘g = κP; calcolo funzionale normale/non normale concorde (compagna normale ⟺ s^m−c, |c|=1); per operatori quadratici in (x,∂) la rotazione giusta è la metaplettica Sp(2) (versione a coeff. variabili di R6-T7(i)).
- SCOUT-1: RT-S1h → MERGE (§2); RT-S1d: idempotenti dell'eigenring = versione a coeff. variabili dei P_a.
- R8 / Problema 2: coeff. Mat 4×4 costanti ⇒ matrice polinomiale; linearizzazione GLR / Mackey–Mackey–Mehl–Mehrmann 2006 conserva i divisori elementari (solo puntatore, fuori scopo).
- NEW-ROUTE RT-R6a: simbolo totale con ⋆-prodotto (Weyl/Kohn–Nirenberg) come via (a′) completa per coeff. variabili; atteso merge in RT-6.

## 6. Stato per item
| Item | Esito | Stato |
|---|---|---|
| E4 | via (b) completa | DIMOSTRATO (+fonte) |
| E5/G6 | spazio ridotto = sottospazio ciclico | DIMOSTRATO |
| F1/F2 | corrette con duali biortogonali; versione tensoriale solo odeco | DIMOSTRATO / FALSO come scritto |
| F6 | Waring / odeco | DIMOSTRATO (n=2) |
| II.1 | tabella §2 | fatto |
| II.2 | Jacobson / Ore | DIMOSTRATO-CON-FONTE |
| II.3 | calcolo funzionale per rami; additività solo per m=1 | DIMOSTRATO-CON-FONTE |
| G5 | vera a meno di similitudine su ℂ(x)[∂] | CORRETTA |
| RT-6 | struttura per la Fase 3 | promuovere |
| RT-5 | strumento geometrico | parcheggiare |

## 7. Limiti
- Numerazioni di Higham, Jacobson, Gantmacher ed equazione odeco di Robeva da verificare sui testi (OQ5).
- R6-L1 derivato qui, non confrontato riga per riga con Robeva.
- R6-T8: struttura dei poli nei punti eccezionali non analizzata.
- SymPy verifica esempi più due casi generici (CHECK 1 e 11); le prove sono nel testo o rimandate alle fonti.
