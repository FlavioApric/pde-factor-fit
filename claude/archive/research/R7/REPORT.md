# R7 — REPORT (Fase 1) · Geometria, simmetria, spettro, non linearità
Agente R7 · 2026-10-22 · Item: II.3, II.4, F6, G6, G5; Fase 4 (L5, G3–G4, A6 "V·d/dx V"); congettura G7. Verifiche: `research/R7/sympy/*.py`, eseguite con `.venv\Scripts\python.exe -I` (citate come [S…]).
*(Salvato dal coordinatore dalla risposta finale di R7: la scrittura diretta era bloccata dall'ambiente.)*

## 0. Skill caricate (Regola 2)
- `anthropic-skills:deep-research`: invocata con Skill; decomposizione (simmetrie/funzioni speciali · spettro · non lineare) seguita in modalità agente singolo, senza subagenti.
- `math-skill` (proof), `sympy`, `scientific-critical-thinking`: SKILL.md letti e seguiti.
- `research-lit`, `arxiv`, `paper-lookup`, `scientific-brainstorming`: dichiarati nel PLAN. Nessuna ricerca web: fonti classiche; collocazioni "(da verificare)" elencate in Q-R7-9. Nessuno script `_vendor` eseguito.

## 1. Sintesi
1. Le classi e_{n,i} (A5/A6) sono legate a (L, 𝔞), con 𝔞 sottoalgebra commutativa massimale delle simmetrie di L (Miller), non al singolo termine T_k — salvo quando T_k è una simmetria (coeff. costanti).
2. Heisenberg universale R7-T1 e base di Appell (§2.3).
3. Simmetrie affini ⇔ stabilizzatore di P (R7-P2).
4. F6 = diagonalizzazione simultanea: vale a coeff. costanti, impossibile per x e ∂ (R7-L3).
5. G7 vera con le correzioni R7-L4 (simmetria ⇒ non identificabilità) e R7-P6/T11 (E_int chiuso: miscela softmax per Burgers, interazione a coppie per KdV).
6. Tre NEW-ROUTE: RT-R7a/b/c.

## 2. Geometria e simmetrie (II.4, G5, G6)
### 2.1 Fatti noti (DIMOSTRATO-CON-FONTE)
**[R7-T0a] Criterio infinitesimale** (Olver GTM 107, Thm 2.31, 2.36): per Δ di rango massimo e localmente risolubile (Def. 2.70), G è gruppo di simmetria ⟺ pr^{(n)}v[Δ]=0 su {Δ=0} per ogni generatore v.

**[R7-T0b] Algebre di simmetria** (Olver Ex. 2.41; Ovsiannikov 1982; Ibragimov CRC vol. 1), modulo superposizione:

| PDE | algebra di simmetria | classi / funzioni speciali |
|---|---|---|
| trasporto | infinito-dimensionale | qualunque f(x−ct) |
| calore | dim 6: ∂_x, ∂_t, u∂_u, x∂_x+2t∂_t, 2t∂_x−xu∂_u, 4tx∂_x+4t²∂_t−(x²+2t)u∂_u; sch(1)=sl(2)⋉h₁ | esponenziali, polinomi del calore/Hermite, Airy, cilindro parabolico (Miller 1977 Cap. 2, da verificare) |
| Airy | dim 4: ∂_x, ∂_t, u∂_u, x∂_x+3t∂_t | esponenziali; t^{-1/3}Ai(x/(3t)^{1/3}) |
| onda | infinito-dimensionale (f(x+t), g(x−t)); parte finita so(2,2) | d'Alembert; Bessel/Legendre per riduzione |

CONGETTURA: algebra grande quando il simbolo è degenere o di grado 2; per ordine ≥3 omogeneo resta solo lo scaling (Q-R7-3).

### 2.2 [R7-P2] (DIMOSTRATO)
P∈ℂ[τ,ξ], z=(t,x), g(ζ)=Mζ+b, T_g u(z)=e^{b·z}u(Mᵀz). (i) P(∂)T_g=T_g(P∘g)(∂); (ii) T_g e^{ζ·z}=e^{g(ζ)·z}, T_g agisce su V(P) come g; (iii) T_g ker P=ker P ⟺ P∘g=κP.
Prova: (i) ∂ ↦ M∂+b sotto T_g; (iii ⟹) T_g ker P = ker(P∘g) e, per il principio fondamentale (Ehrenpreis–Malgrange–Palamodov; Hörmander II §7.6; Björk Cap. 8), Ann(ker Q(∂))=(Q), quindi (P∘g)=(P). ∎
Verifiche: calore Galilei (τ,ξ)↦(τ+2sξ+s², ξ+s), P∘g=P [S3a]; T_g e^{ξ₀x+ξ₀²t}=e^{(ξ₀+s)x+(ξ₀+s)²t} [S3a″]; Airy: stabilizzatore affine solo {(d³τ,dξ)} [S3b].
Non cattura la simmetria proiettiva del calore né le riparametrizzazioni di trasporto e onda: queste agiscono su L²(V(P),μ) solo tramite trasformate integrali (G6/RT-7).

### 2.3 [R7-T1] (DIMOSTRATO)
L=∂_t−a(∂_x), X=x+t a′(∂_x): [L,X]=0 e [∂_x,X]=1 (perché [∂_t,X]=a′(∂), [a(∂),x]=a′(∂)); p_n=Xⁿ1=∂_sⁿe^{sx+ta(s)}|₀. Verificato per calore, Airy, a generico [S3c]: calore p₃=x³+6tx (Rosenbloom–Widder 1959); Airy p₃=x³−6t.
Lettura: la base di Appell (numerabile) e il frame esponenziale su V(P) (continuo) sono due coordinate della stessa rappresentazione di h₁ — ponte A7↔G6; base di Schauder aperta (Q-R7-2).

### 2.4 [R7-T2] Rappresentazioni → funzioni speciali (Vilenkin 1968; Vilenkin–Klimyk; Miller 1968)
| gruppo | funzioni speciali | dove |
|---|---|---|
| SO(2) | Fourier | — |
| E(2) | Bessel J_n(Rr) (Graf, Jacobi–Anger) | Vilenkin Cap. IV |
| SO(3)/SU(2) | Legendre, armoniche sferiche, Wigner d (Jacobi) | Cap. III |
| SL(2,ℝ)/SU(1,1) | Laguerre, Gegenbauer, ipergeometriche | Cap. VI–VII |
| Heisenberg/oscillatore | Hermite | — |
| sch(1) | polinomi del calore, Hermite, Airy, cilindro parabolico | — |

Mehler (R3-K8) = forma chiusa di sl(2) = disentangling di Wei–Norman.

**[R7-T3] Separazione delle variabili = sottoalgebra commutativa** (Miller 1977 Cap. 1–2; Kalnins–Miller): sistemi separabili ↔ insiemi commutativi di simmetrie del 2° ordine; soluzioni separate = autofunzioni comuni. DIMOSTRATO-CON-FONTE per Helmholtz, calore, Schrödinger, onda in dimensione bassa; APERTO in generale (Q-R7-1).

### 2.5 Rotazioni (G6)
1. SO(2) sul simbolo (via (a), R6): per m=2 il simbolo principale si diagonalizza per rotazione; per m≥3 serve l'odeco (Robeva 2016).
2. Metaplettica Sp(2,ℝ) (Folland 1989 Cap. 4): la Fourier frazionaria ruota (x,ξ) e scambia termini x con termini ∂ — la "rotazione" esatta per coefficienti di grado ≤2.
3. Lax: L(t)=U(t)L(0)U(t)⁻¹, flusso non lineare = rotazione unitaria isospettrale [S2e].

### 2.6 Raccordo con R6
Simmetrie affini: sulla via (a) stabilizzatore GL₂ della forma binaria (b=0); sulla via (b) automorfismi dell'anello ℂ[ξ], C(ξ)↦α⁻¹[C(dξ+e)−(βξ+γ)I], non gauge GL_m(ℂ[ξ]). Proposta per S-II: invariante = (V(P) come schema, stabilizzatore affine di P).

## 3. Spettro (II.3, F1/F2, F6)
- **[R7-T4]** Teorema spettrale e calcolo funzionale boreliano (Reed–Simon I Thm VIII.4–VIII.6; Rudin FA 12.21, 13.24, 13.33): A autoaggiunto/normale, anche illimitato, A=∫λdE, f(A)=∫f dE. F1 = caso a spettro discreto; per −i∂_x autofunzioni generalizzate (terne di Gel'fand) = frame continuo di G6.
- **[R7-T5]** Riesz–Dunford (Dunford–Schwartz §VII.3; Higham Def. 1.2, Thm 1.12): f(C)=Σ_aΣ_k f^{(k)}(λ_a)/k! N_a^kP_a. C(p) normale ⟺ p=z^m−c con |c|=1 [S3g] ⇒ in F1 servono duali biortogonali (Vandermonde, R6); i blocchi di Jordan danno x^k e^{λx}.
- **[R7-T6]** Diagonalizzazione simultanea in dim. finita (Horn–Johnson Thm 1.3.21, 2.5.5): diagonalizzabili insieme ⟺ commutano; normali con un'unica unitaria ⟺ commutano.
- **[R7-T7]** Spettro congiunto illimitato (Schmüdgen GTM 265 Thm 5.21, 5.23): autoaggiunti fortemente commutanti ⇒ misura spettrale congiunta; controesempio di Nelson (Reed–Simon I §VIII.5; Schmüdgen Ex. 5.5): commutazione su un core comune non basta.
- **[R7-L3] (DIMOSTRATO)** [A,B]=cI, c≠0 ⇒ nessun autovettore comune (∂v=av, xv=bv ⇒ v=[∂,x]v=0). Radice dell'E_int di commutatore (L4).
- **F6:** vale a coeff. costanti (spettro congiunto ξ↦(p₁(ξ),…,p_N(ξ)) = V(P) parametrizzata); falso per coefficienti variabili; nel mezzo Wei–Norman.

## 4. Algebre di Lie per E_int (in accordo con R5)
- **[R7-T8] Wei–Norman** (JMP 4 (1963) 575; PAMS 15 (1964) 327): 𝔤 finito-dimensionale ⇒ U=Πexp(g_j(t)X_j) localmente; risolubile ⇒ globale. Copre RT-S1i e R5-T8.
- Verifiche: e^{t(∂²+x)}=e^{t³/3}e^{tx}e^{t²∂}e^{t∂²} [S3e] ({∂²,∂,x,1} nilpotente di passo 3); {∂²,x²,x∂+½} = sl(2), [∂²,x²]=4x∂+2, Wei–Norman solo locale; {∂³,∂²,∂,x,1} chiusa, dim 5; ⟨∂³,x²⟩: [∂³,[∂³,x²]]=18∂⁴, [∂³,[x²,∂⁴]]=−24∂⁵, [∂³,[x²,∂⁵]]=−30∂⁶ [S3d, s3b_extra].
- **[R7-P5] (DIMOSTRATO, schizzo)** ⟨∂^m,x^k⟩ con m≥3, k≥2 è infinito-dimensionale: simbolo principale del commutatore = parentesi di Poisson; {p^m,q²}=−2mqp^{m−1}, {p^m,qp^j}=−mp^{m+j−1} ⇒ gradi in p illimitati. Complementare a R5-P7. Congettura comune: finito-dimensionale ⟺ m+k≤3 o min(m,k)≤1 (Q-R7-4).
- Corollario: algebra finita risolubile ⇒ prodotto esatto; finita non risolubile ⇒ forma chiusa locale; infinita ⇒ solo serie (B3).

## 5. Non linearità (Fase 4, L5, G7)
### 5.1 Identificazione
- Lineare nei parametri: λ∈ker𝔾(u) anche con monomi del jet (Rudy et al. 2017; Brunton et al. 2016).
- **[R7-L4] (DIMOSTRATO)** u invariante per una simmetria con caratteristica Q_v nello span del dizionario, Q_v non ∝ L ⇒ dim ker𝔾(u) ≥ 2. Verifica esatta [S4], KdV u_t+6uu_x+u_xxx=0, dizionario {u_t,u_x,u,u²,uu_x,u_xx,u_xxx}: 1-solitone dim ker = 3 (relazioni u_t+u_x, −u+3u²+u_xx, KdV); 2-solitone dim ker = 1. L'interazione rompe la simmetria e rende u identificante (RT-R7c).

### 5.2 Linearizzazioni esatte
- **[R7-T9] Cole–Hopf** (Hopf 1950; Cole 1951): u=−2νφ_x/φ ⇒ Burgers[u]=−2ν∂_x(heat[φ]/φ) [S1a] (il V·V_x di A6).
- **[R7-P6] (DIMOSTRATO [S1b–f])** φ=φ₁+φ₂ ⇒ u=w₁u₁+w₂u₂, w_i=φ_i/(φ₁+φ₂), E_int=−(w₂u₁+w₁u₂). Onde piane: u=Σc_i·softmax(θ)_i, θ_i=−(c_ix−c_i²t/2)/2ν. ν→0 (Maslov, Hopf–Lax: −2ν log Σe^{θ_i}→max): pesi → argmax, u costante a tratti, E_int sugli shock. Forma esatta di D1 e della "graduated mixture" di B3 (RT-R7b; Kolokoltsov–Maslov 1997).
- **[R7-T10] Lax/IST** (Lax 1968; GGKM 1967; AKNS 1974; Ablowitz–Segur 1981 Cap. 1): L=−∂²+u, P=−4∂³+6u∂+3u_x, L_t=[P,L] ⟺ u_t=6uu_x−u_xxx [S2e]. Dati di scattering lineari: b(k,t)=b(k,0)e^{8ik³t}, κ_n costanti, c_n(t)=c_n(0)e^{4κ_n³t} (segni da verificare); esponente = dispersione linearizzata in 2k ⇒ log b è il log-simbolo additivo di G3 nel caso integrabile (RT-R7a).
- **[R7-T11] Hirota** (Hirota 1971; 2004): u=2(log f)_xx, f=Σ_μ exp(Σμ_iη_i+Σ_{i<j}μ_iμ_j log A_ij), A_ij=((k_i−k_j)/(k_i+k_j))²; verificato N=1,2,3 [S2a,b]. Interazione solo a coppie: N(N−1)/2 parametri, O(N²) e non O(2^N) (B2). Sfasamenti: il veloce avanza di −log A₁₂/k₁, il lento arretra di log A₁₂/k₂ [S2c]; ∫E_int dx=0 [S2d]. Cole–Hopf e Hirota hanno la stessa forma c∂^m log(·): φ risolve una PDE lineare (E_int=0 in φ), f una bilineare (un coefficiente per coppia).
- **[R7-T12] Miura e Bäcklund** (Miura 1968; Wahlquist–Estabrook 1973; Rogers–Schief 2002): KdV[−(v²+v_x)]=−(2v+∂)mKdV[v] [S2f]; Bianchi w₁₂=w₀+c(λ₁−λ₂)/(w₁−w₂) (convenzione da verificare, Drazin–Johnson §5.4): E_int algebrico.

### 5.3 Immersioni
- **[R7-T13] Koopman** (Koopman 1931; Mezić 2005; Budišić–Mohr–Mezić 2012; Lan–Mezić 2013; Mauroy–Mezić–Susuki 2020): lineare, unitario con misura invariante; spettro a reticolo (λ_i+λ_j): le frequenze somma sono l'impronta spettrale di E_int; Burgers ha autofunzionali espliciti via Cole–Hopf (Page–Kerswell 2018).
- **[R7-T14] Carleman** (Carleman 1932; Kowalski–Steeb 1991; Forets–Pouly 2017; Liu et al. 2021 Thm 1, costanti da verificare): Re spec F₁<0 e R<1 ⇒ errore di troncamento O(R^N) uniforme in t. Esempio esatto [S3f]: x′=−x+x², troncamento N = Σ_{n≤N}x₀ⁿe^{−t}(1−e^{−t})^{n−1}, converge uniformemente ⟺ |x₀|<1. Carleman = serie di Volterra nel dato iniziale; il termine n=2 è la h(e₁,e₂) di P1.

### 5.4 Stato di G7
| parte di G7 | stato |
|---|---|
| identificazione lineare nei parametri | VERO, con l'ostruzione R7-L4 |
| servono linearizzazione esatta o immersione | VERO in parte: Burgers E_int esatto; non integrabile ⇒ immersione troncata, senza decomposizione esatta finita |
| E_int chiuso nel caso integrabile | VERO e più forte (interazione a coppie, massa nulla, asintoticamente solo sfasamento) |
| componente non lineare = solitone / modo di scattering / autofunzione di Koopman | CONGETTURA |

Rischio: le soluzioni analitiche note sono ridotte per simmetria, quindi non identificanti; il test corretto è un 2-solitone o un multi-shock.

## 6. Mappa sugli item
| item | sezioni |
|---|---|
| II.4 | §2 |
| II.3, F1–F2 | T4, T5 |
| F6 | T6, T7, L3 |
| G5 | T3 |
| G6 | §2.5, P2 |
| A7 | §2.3 |
| B3/D1 | P6 |
| P1/B2 | T8, P5, T11 |
| C3/G4 | L4 |
| L5 / Fase 4 | §5 |
| A6 | T9, P6 |

## 7. Verifiche SymPy
| script | esito |
|---|---|
| s1 | S1a–f OK |
| s2 | N=1,2, S2c, S2d (massa 6=2k₁+2k₂), Miura OK; "N=3 False" è un artefatto superato da s2b |
| s2b | N=3 OK, Lax OK |
| s3 / s3b | S3a–g OK |
| s4 | dim ker 3 (1-solitone) / 1 (2-solitone) |

## 8. Messaggi
- Ricevuti: TABELLA e domande di R6; AVVISI di SCOUT-1, R5, central; messaggio sui linearizzabili.
- Inviati: RISPOSTA a R6; TABELLA ed errata a R5; PLAN-READY, 3 NEW-ROUTE (RT-R7a/b/c) e DONE a central.
- Da verificare sulle fonti (Q-R7-9): numeri di teorema/pagine in Miller 1977 e Schmüdgen, costanti di Liu et al. 2021, segni dei dati di scattering, formula di Bianchi.
