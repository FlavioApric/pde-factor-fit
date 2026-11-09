# REPORT — R4 · Identificazione dell'operatore dal nucleo (C3, P4)
Data 22/10/2026. Notazione: NOTAZIONE.md. Verifiche in research/R4/sympy/ (r4_checks.out, r4_zariski.out, r4_measure.out): tutte [OK].
*(Salvato dal coordinatore dalla risposta finale di R4: la scrittura diretta era bloccata dall'ambiente.)*
Skill caricate con Read del SKILL.md: academic-research-skills/deep-research, research-lit, novelty-check (fasi A e B), math-skill (modalità proof), sympy, scientific-critical-thinking. anthropic-skills:deep-research non invocata (lancia sotto-agenti). Nessuno script _vendor eseguito. Revisione cross-model di novelty-check non disponibile.
Stati: DIMOSTRATO, DIMOSTRATO-CON-FONTE, CONGETTURA, FALSO, APERTO.

## 0. Sintesi
1. Identificare L da u è un problema di rango e di ideali: ker 𝔾(u) = Ann(u) ∩ span(dizionario) [T6].
2. G4: parte ODE vera [T1–T3]; parte evolutiva vera con correzione [T4].
3. G4 generale: falsa nella versione con la misura [C2]; vera nella versione intrinseca per P ridotto, con soglia di Bézout [T5].
4. L'identificabilità dipende dalla classe ammessa 𝓛 [C3, C4]; la sparsità non la ripristina [C1].
5. P4: la sintesi spettrale dà A|_{Z(u)} in modo univoco; identificabilità ⟺ la restrizione 𝓛 → End Z(u) è iniettiva [T8]. Risolvente = Padé/Laplace [T3].

## 1. C3.1 Mappa della letteratura
- **Prony/Hankel** (de Prony 1795; Kronecker; Hua–Sarkar 1990): 2d campioni; rango Hankel = d; nucleo = annullatore minimo (L0).
- **FRI** (Vetterli–Marziliano–Blu 2002; Dragotti–Vetterli–Blu 2007): filtro annullatore = Prony sui coefficienti di Fourier; 2K campioni per K impulsi.
- **Prony operatoriale** (Peter–Plonka 2013, Inverse Problems 29:025001; Stampfer–Plonka arXiv:1901.08778): somme sparse di autofunzioni di un A noto = P4.1.
- **Prony multivariato** (Kunis–Peter–Römer–von der Ohe 2016; Mourrain FoCM 2018): ideale annullatore = ideale dei punti con molteplicità; output base di Gröbner/bordo (L3 con modi finiti).
- **Guessing D-finito** (Kauers 2009; Kauers–Jaroschek–Johansson 2015, ore_algebra; Salvy–Zimmermann 1994; Beckermann–Labahn 1994; Chen–Kauers–Singer 2016): sistema lineare (r+1)(d+1), trade-off ordine/grado (L1).
- **Eliminazione differenziale** (Ritt 1950; Kolchin 1973; Boulier–Lazard–Ollivier–Petitot 1995/2009; Ljung–Glad 1994; Byrne–Harrington–Ovchinnikov–Pogudin–Rahkooy–Soto 2024): identificabilità ⟺ iniettività dei coefficienti nei parametri (L4–L5).
- **Identificabilità da una soluzione:** Scholl–Bacho–Boche–Kutyniok (arXiv:2210.08342; Cor. 1: F lineare unica ⟺ feature linearmente indipendenti; Prop. 6/7 ODE ordine 2/3; Prop. 10 coeff. variabili mai identificabili); He–Zhao–Zhong (FoCM 24, 2024; Thm 3.2 soglia sui modi; Thm 3.4/3.5 coeff. variabili); Stanhope–Rubin–Swigon (SIADS 13, 2014: identificabile ⟺ x₀ ciclico); Qiu et al. (AMC 430, 2022).
- **Ehrenpreis–Palamodov** (Ehrenpreis 1970; Palamodov 1970; Hörmander II cap. 7; Björk 1979; Cid-Ruiz–Homs–Sturmfels 2021; Ait El Manssour–Härkönen–Sturmfels 2021): solo la direzione diretta; l'inversa è C3.2.
- **Inverso Sturm–Liouville** (Borg 1946; Gel'fand–Levitan 1951; Marchenko 1950/77; Hochstadt–Lieberman 1978; Freiling–Yurko 2001): serve una famiglia di soluzioni; da una sola soluzione parabolica: Pierce 1979.
- **Apolarità** (Iarrobino–Kanev; SCOUT-1 RT-S1h): la Hankel di Prony è un catalecticante.

Novità: l'enunciato unificato T5+T6 (schema spettrale per modo, criterio V(Ann u) = V(P), Bézout, Gram = Vandermonde pesata) non trovato come teorema esplicito; probabilmente nuovo ma elementare (da confermare con R8).

## 2. C3.2 Teoremi
**[R4-T1] ODE coeff. costanti — DIMOSTRATO.** I aperto, u ∈ C^∞(I), u ≢ 0, 𝓛_n = {Σ_{k≤n} λ_k D^k}.
(a) Ann(u) ideale di ℂ[z]; ≠ 0 ⟺ dim span{u^{(k)}} < ∞ ⟺ u = Σ q_j e^{λ_j x}.
(b) Ann(u) = (p_u), p_u = ∏(z−λ_j)^{m_j}, m_j = deg q_j + 1, d = deg p_u = dim V_u.
(c) {L ∈ 𝓛_n : Lu = 0} = p_u·ℂ[z]_{≤ n−d}; identificabile ⟺ n = d, allora L = c·p_u.
Prova: ℂ[z] PID; V_u ⊆ ker p(D) con base x^i e^{λx}; minimalità: (D−λ)(q e^{λx}) = q' e^{λx}, (D−μ) con μ≠λ preserva il grado; V_u ≅ ℂ[z]/(p_u). ∎
Gram: rank 𝔾_n = min(n+1, d), ker 𝔾_n = coordinate di Ann(u)_{≤n}. SymPy C1, C2 (d=3, n=4 ⇒ dim ker = 2).

**[R4-T2] Prony nel jet in un punto — DIMOSTRATO.** s_k = u^{(k)}(x₀): rank (s_{i+j}) = min(N, d); nucleo della d×(d+1) dà p_u; bastano 2d valori del jet in un punto.
Prova: p_u(E)s = 0; se q(E)s = 0 allora q(D)u ha tutte le derivate nulle in x₀, analitica ⇒ nulla ⇒ p_u | q; Kronecker. ∎ SymPy C1: (z−2)²(z+1).

**[R4-T3] Risolvente/Laplace = Padé — DIMOSTRATO.** ℒu(z) = Σ s_k z^{−k−1} = r/p_u ridotta = e_1^T (z−C)^{−1} X(0) (compagna). Prova: ℒ(x^i e^{λx}) = i!/(z−λ)^{i+1}. ∎ SymPy C3.

**[R4-T4] Evoluzione su 𝕋, u_t = a(∂_x)u, deg a ≤ n — DIMOSTRATO.** S = supp û₀.
(a) û(t,κ) = û₀(κ)e^{a(iκ)t}, quindi a(iκ) = ∂_t log û(t,κ) per κ ∈ S.
(b) Coeff. complessi: identificabile ⟺ |S| ≥ n+1; altrimenti a + ∏_{κ∈S}(ξ−iκ)·ℂ[ξ]_{≤ n−|S|}.
(c) Coeff. reali: ⟺ |S ∪ −S| ≥ n+1.
(d) Grado ignoto: ⟺ S infinito.
Prova: interpolazione di Lagrange. ∎ SymPy C5. Coerente con HZZ Thm 3.2 in d=1.

**[R4-T5] P(∂_t,∂_x) su 𝕋×I, P monico in τ di grado m — DIMOSTRATO per P ridotto.** v_κ = û(·,κ), p_κ annullatore minimo di v_κ, Z(u) = {(τ, iκ) : p_κ(τ) = 0}.
(a) Ann(u) = {Q : p_κ | Q(·, iκ) ∀κ}.
(b) P ridotto = P_1⋯P_r: Ann(u) = (P) ⟺ V(Ann u) = V(P) ⟺ Z ∩ V(P_i) infinito per ogni i.
(c) Se |Z ∩ V(P_i)| > n·deg P_i ∀i, ogni Q con deg Q ≤ n e Qu = 0 è multiplo di P.
Prova: (c) Bézout per P_i ∤ Q coprimi; (b ⇒) se Z ∩ V(P_i) finito, (P/P_i)·∏ ℓ_z ∈ Ann(u) \ (P); κ con radici multiple in numero finito; V(I) = V(P) con P ridotto ⇒ I = (P). ∎
SymPy r4_zariski.out (calore): soglie = Bézout (n=2: |Z| = 6 > 4; n=3: |Z| = 8 > 6, dim = 3 = multipli di P).
Verdetto G4: vera in forma intrinseca; falsa con la misura [C2]; aperta per P non ridotto (Q2); su ℝ² le soluzioni temperate del calore sono polinomi ⇒ Ann 0-dimensionale.

**[R4-T6] Gram = Vandermonde pesata — DIMOSTRATO (radici semplici).** 𝔾 = 2π Σ_κ Φ_κ^* M_κ Φ_κ, (Φ_κ)_{jk} = z_{κj}^{α_k}, M_κ ≻ 0 ⇒ ker 𝔾 = {λ : Σ λ_k z^{α_k} = 0 su Z(u)}. Prova: Parseval in x, ker Σ A^*A = ∩ ker A. ∎ I pesi influenzano solo il condizionamento.

**[R4-T7] Algebra di Weyl — DIMOSTRATO-CON-FONTE (Ore 1933; Chen–Kauers–Singer 2016).** (a) Ann_{ℂ(x)⟨D⟩}(u) = K·L_min. (b) Annullatori di ordine r in A_1 = p(x)·L̃, L̃ primitivo ⇒ identificabile in 𝓛_{r,δ} ⟺ δ = deg L̃. (c) Trade-off ordine/grado: e^{2x} + x e^{−x} ha ordine 2 in A_1 contro 3 (osservazione di R8). SymPy C7.

**[R4-T8] P4.3: restrizione al sottospazio ciclico — DIMOSTRATO (caso commutativo).** Z = span{e^{tA}u₀}. (i) u determina A|_Z = Σ_{κ∈S} a(iκ) e_κ⊗e_κ^†. (ii) A identificato in 𝓐 ⟺ 𝓐 → End Z iniettiva. 𝓐 = polinomi di grado ≤ n ⇒ T4; 𝓐 = End ℂ^d ⇒ Stanhope–Rubin–Swigon. Nota F1: esatta solo su Z e nel caso diagonalizzabile; con molteplicità serve la parte nilpotente di Jordan.

**[R4-P2] Inverso Sturm–Liouville.** Borg, Gel'fand–Levitan, Marchenko, Hochstadt–Lieberman richiedono una famiglia di soluzioni; una soluzione stazionaria dà solo q − λ = y''/y; una soluzione parabolica con dati al bordo determina i coefficienti se tutti i coefficienti di Fourier iniziali sono ≠ 0 (Pierce 1979, da verificare sul testo).

**Controesempi.**
- [C1] D^k − 1 annulla e^x per ogni k: la sparsità non dà unicità.
- [C2] u ≡ 1 = ∫_{|ξ|=1} e^{ξx}dθ/2π ha supporto Zariski-denso in V(τ), ma Ann(u) = (τ, ξ).
- [C3] uD − u' annulla qualsiasi u: con coefficienti liberi mai identificabilità.
- [C4] e^{−t}cos x + e^{−4t}cos 2x risolve il calore e u_tt + 5u_t + 4u = 0; il modo complesso risolve anche u_t = 3iu_x + 2u; nella classe evoluzione reale di grado ≤ 2 identifica il calore.

## 3. C3.3 Verdetto
- **Identificazione:** il dizionario a componenti è una carta di coordinate di Ann(u), dipendente dalle coordinate e non unica se sovradimensionato. L'ideale annullatore è canonico; il simbolo/varietà dà il criterio verificabile (T5). È strettamente migliore; il dizionario resta come filtrazione graduata (si sale di grado finché ker 𝔾 ≠ 0).
- **Scomposizione di u:** componenti naturali indicizzate dalle componenti di V(P) (decomposizione primaria), non dai termini; i termini entrano linearmente solo nel log-simbolo (Vandermonde di T4).
- **Architettura raccomandata:** u → Z(u) → λ per interpolazione, costo polinomiale.
- **Quando le componenti sono ottimali:** dizionario graduato e minimale con Ann(u) principale ⇒ ker 𝔾 = ℂP, le due formulazioni coincidono.
- Strada nuova: RT-R4a.

## 4. P4
- P4.1: T8(i). P4.2: T3 (per le PDE modo per modo). P4.3: T8(ii), T4, T5; coeff. variabili: P2.

## 5. Messaggi
- Inviati: R1 (RISPOSTA: condizioni puramente di rango; criterio canonico = grado minimo/base di Gröbner, non vettore più sparso; con campioni generici identificabilità q.c., RIP non necessaria); R2 e R3 (TABELLA); R3 (RISPOSTA riga per riga: trave e onde identificabili solo se Z(u) infinito su entrambi i fattori); central (NEW-ROUTE e DONE).
- Ricevuti: R1, R8, SCOUT-1, SCOUT-2, R3, central.
