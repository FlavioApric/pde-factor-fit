# REPORT — PR-C2c (Asse 1, T10–T12: non lineari e integrabili, modelli fisici applicati, stocastici)
Agente PR-C2c · 2026-10-22 · piano: `research/PR-C2c/PLAN.md`.
*(Salvato dal coordinatore dalla risposta finale di PR-C2c: la scrittura diretta era bloccata dall'ambiente.)*

## 0. Skill caricate (Regola 2)
- `academic-research-skills\deep-research\SKILL.md` (Read; workflow domanda → fonti → sintesi → verifica). `anthropic-skills:deep-research` non invocata via Skill (genera sub-agenti); workflow seguito a mano.
- `scientific-agent-skills\skills\paper-lookup\SKILL.md`, `Auto-claude-code-research-in-sleep\skills\arxiv\SKILL.md` (Read; nessuno script _vendor eseguito). WebSearch per 3 voci (Clarkson–Fokas–Ablowitz 1989, Bertini–Giacomin 1997, Han–Benaroya–Wei 1999).
- `math-skill\SKILL.md` (solver) + `scientific-agent-skills\skills\sympy\SKILL.md`: 5 script in `sympy/`, `.venv\Scripts\python.exe -I`, output in `sympy/*.out.txt` (residui 0 o < 1e−40; alcuni controlli numerici come verifica, non come metodo).
- `scientific-agent-skills\skills\citation-management\SKILL.md`: `sources.bib` (59 voci; solo 3 DOI verificati, segnati in testa).

## 1. Prodotti
- `cards/` 16 schede: 3 dettagliate (C2.15 Burgers/Cole–Hopf; C2.45 KdV/IST con C2.16; C2.33 trave Euler–Bernoulli) + 13 brevi (C2.16, C2.24, C2.44, C2.47, C2.26, C2.27, C2.28, C2.29, C2.32, C2.40, C2.43, C2.57, C2.41). Ogni scheda: operatore, classe nucleo/soluzioni, tag, ≥2 fonti, linearizzazione esatta (sì/no/quale), forma dell'interazione.
- `sympy/`: `burgers_colehopf.py` [B1–B6], `kdv_solitons.py` [K1–K7], `euler_bernoulli.py` [E1–E6], `misc_nonlinear.py` [M1–M10], `kdv_identifiability.py`.
- Messaggi: R7 (tabella linearizzazioni esatte: Cole–Hopf, IST, Miura, Hirota, odografo, Carrier–Greenspan, Cole–Hopf stocastico), R3 (trave EB), PR-C2e (risposta: termini, classi, termini mancanti, attributi), central (PLAN-READY, NEW-ROUTE, DONE).

## 2. Tabella riassuntiva (item → linearizzazione esatta → interazione)
| item | tag | trasformazione esatta | classe a valle | interazione |
|---|---|---|---|---|
| C2.15 Burgers | ▲ | Cole–Hopf u=−2ν∂_x log φ | calore ★ | lineare in φ; in u somma logaritmica, fronti si fondono |
| C2.45 KdV/mKdV/NLS/sG | ▲ | IST (Lax), Miura, Hirota | dati di scattering (evoluzione lineare diagonale) | sfasamenti chiusi; coeff. A_ij per coppia |
| C2.16 asintotiche | ▲◆ | (a) IST; (b) nessuna esatta — WKB/raccordo | serie asintotiche | termine di raccordo = E_int; condizioni di solvibilità |
| C2.24 conservazione | ▲■ | caratteristiche; odografo (2×2); Hopf–Lax | trasporto; EPD lineare | urti si fondono; funzionale di Glimm (bilineare) |
| C2.44 onde viaggianti | ▲ | riduzione PDE→ODE (esatta) | ODE (eteroclinica/omoclinica) | interazione esponenzialmente debole / sfasamenti |
| C2.47 blow-up | ▲ | solo casi speciali (caratteristiche, pseudo-conforme) | autosimili | bilanciamento diffusione/reazione, scaling critico |
| C2.26 comprimibile | ◇■ | Riemann + odografo | EPD; acustica d'Alembert | onde semplici interagenti |
| C2.27 incomprimibile | ◇■ | nessuna (flussi di taglio esatti = calore) | calore, Gaussiane | triadi di Fourier |
| C2.28 shallow water | ◇■ | Riemann/odografo; Carrier–Greenspan | EPD; Bessel | triadi di Rossby; KdV asintotico |
| C2.29 EM | ◇■ | lineare; Helmholtz, TE/TM, onde ± | onda, telegrafo, Helmholtz | assente nel vuoto |
| C2.32 elasticità | ◇■ | Helmholtz P/S | due equazioni d'onda | conversione di modo al bordo |
| C2.33 travi/piastre | ★◇ | fattorizzazione T=S_+S_− (Schrödinger coniugati) | Schrödinger ⊕ Schrödinger | E_int=0 modulo span{1,x} |
| C2.40 cinetiche | ◇ | lineari (FP, OU, Kramers); Vlasov no | Gaussiane/Hermite (Mehler, Kolmogorov) | commutatore trasporto–collisione (ipocoercività) |
| C2.43 frontiera libera | ▲◇ | Landau/Baiocchi; Hele-Shaw: conforme+momenti | calore/armoniche nel dominio | legge d'interfaccia (bordo) |
| C2.57 grafi | ◇ | separazione arco-per-arco | trig. 1D + matrice di vertice | finita-dimensionale ai vertici (scattering) |
| C2.41 SPDE | ● | Cole–Hopf stocastico; Feynman–Kac | SHE lineare; calore | correzione Itô/rinormalizzazione |

## 3. Enunciati chiave
**[PRC2c-P1] Cole–Hopf (identità).** φ>0 liscia, u=−2νφ_x/φ ⇒ u_t+uu_x−νu_xx = −2ν∂_x((φ_t−νφ_xx)/φ). Quindi φ_t=νφ_xx ⇒ u risolve Burgers; viceversa ogni soluzione liscia di Burgers su ℝ si scrive così con φ unica a meno di costante positiva. Fonte: Hopf 1950 §2; Cole 1951. [B1]=0. DIMOSTRATO-CON-FONTE.

**[PRC2c-P2] Sovrapposizione in Burgers.** φ_1, φ_2 soluzioni positive del calore ⇒ u=−2ν∂_x log(φ_1+φ_2) risolve Burgers; E_int(u) := u − u(φ_1) − u(φ_2) ≠ 0 in generale (forma chiusa [B4]); E_int(φ)=0. ν→0: −2ν log(e^{−S_1/2ν}+e^{−S_2/2ν}) → min(S_1,S_2) (Hopf–Lax). DIMOSTRATO ([B2],[B4],[B5]); Hopf–Lax DIMOSTRATO-CON-FONTE (Evans 2010 §3.3–3.4).

**[PRC2c-P3] KdV, 2-solitone e sfasamento.** u=2∂_x² log(1+e^{η1}+e^{η2}+A_12e^{η1+η2}), η_i=k_ix−k_i³t, risolve u_t+6uu_x+u_xxx=0 ⟺ A_12=((k_1−k_2)/(k_1+k_2))². Per k_1>k_2 il veloce avanza di (2/k_1)ln((k_1+k_2)/(k_1−k_2)), il lento arretra di (2/k_2)ln(...). Fonte: Hirota 1971; Drazin–Johnson 1989 cap. 5. [K2a–c], [K3] (1.09861228867 = ln 3 per k=(2,1)), [K4]. DIMOSTRATO-CON-FONTE.

**[PRC2c-P4] E_int solitonico.** Con i solitoni sfasati ‖u − u_1(shift) − u_2‖_{L¹} → 0 per t→+∞ (5e−13 a t=10, 5e−26 a t=20); senza sfasamento resta ≈4. Per P1: nel caso integrabile E_int = parte localizzata nel tempo + riparametrizzazione finita (fasi). VERIFICATO NUMERICAMENTE (controllo); con radiazione NOTO asintoticamente (Deift–Zhou); formulazione P1 APERTA (Q2).

**[PRC2c-P5] Lax e Miura.** L=−∂²−u, B=−4∂³−6u∂−3u_x: ([B,L]−L_t)ψ = KdV[u]ψ [K6]; KdV[−(v²+v_x)] = −(2v+∂_x)mKdV[v] [K5]. Fonte: Lax 1968; Miura 1968. DIMOSTRATO (identità simboliche).

**[PRC2c-T1] Trave EB: scomposizione esatta.** ∂_t²+c²∂_x⁴ = (∂_t−ic∂_x²)(∂_t+ic∂_x²), fattori commutanti; V(S_+)∩V(S_−)={(0,0)} con ideale (τ,ξ²). Per u ∈ C^∞(ℝ²): ker T = ker S_+ + ker S_−, ker S_+ ∩ ker S_− = span{1,x}. Dim.: ⊇ ovvia; ⊆ dalla successione esatta di G2 + Malgrange–Ehrenpreis; intersezione: u_t=0 e u_xx=0 ⇒ u=a_0+a_1x. [E1a–e]. Intersezione DIMOSTRATA; uguaglianza DIMOSTRATA-CON-FONTE (confermata da R2-T2); formula costruttiva per u_± richiede l'inversione di ∂_x² (da scrivere in S-C2/C4).

**[PRC2c-P6] Nucleo della trave.** t>0: G=(8πct)^{−1/2}[cos(x²/4ct)+sin(x²/4ct)] risolve EB, ∫G=1, G=½(K_++K_−) con K_+ propagatore di e^{ict∂²}. Fonte: Graff 1975 §3.4. [E4a–d]. DIMOSTRATO-CON-FONTE.

**[PRC2c-P7] Identificabilità non lineare (esempio).** Dizionario {u_t, uu_x, u_xxx, u_x, u_xx, u}: 1-solitone KdV ha nucleo di dimensione 2 (KdV e trasporto ∂_t+k_1²∂_x) ⇒ non identificabile; 2-solitone dimensione 1; Burgers a 2 fronti dimensione 1 ([B6]). VERIFICATO NUMERICAMENTE; enunciato generale APERTO (Q3). Conferma G7; l'interazione rompe la degenerazione del caso a una componente (coerente con R7-L4).

**[PRC2c-P8] Verifiche brevi:** sine-Gordon kink, NLS sech, Fisher–KPP Ablowitz–Zeppetella, Burgers inviscido implicito + blow-up, blow-up ODE, OU/Fokker–Planck, Feynman–Kac V=bx, trasporto cinetico, acustica 1D, Stefan/Neumann: residuo 0 [M1–M10]. DIMOSTRATO (sostituzione).

## 4. Risultati mappati sugli item
- C2 / A6: V·V_x non ha una classe di nucleo propria (ker(u u_x) = funzioni di t); la classe nasce dal bilanciamento con ∂_t e ∂_x² e, via Cole–Hopf, è il log-gradiente della classe del calore. Nei casi integrabili: τ-funzioni (Hirota) / dati di scattering.
- G2: la trave EB è l'esempio ★ 1D più pulito di fattorizzazione con intersezione non banale (span{1,x}); per operatori del 2° ordine in t le componenti sono i fattori (Q4).
- G7: confermata su Burgers e KdV (identificazione lineare nei coefficienti; decomposizione solo dopo linearizzazione esatta; E_int chiuso nei casi integrabili). Nuovo: Burgers non lascia sfasamenti (i fronti si fondono), KdV sì; per ν→0 la sovrapposizione diventa min-plus.
- P1/P3: modelli di E_int: bilineare in coordinate trasformate (Hirota A_ij, Glimm, triadi); al bordo (elasticità, Stefan, grafi); da commutatore (Kramers, Feynman–Kac).
- C3/G4 non lineare: le onde viaggianti danno non identificabilità strutturale (P7).
- C1: lo spazio delle soluzioni non lineari è una varietà; la IST dà un frame misto discreto+continuo (A7/G6); proposta: pull-back del Gram via Cole–Hopf (Q1).
- Fase 4: rotta (iv) praticabile per V·V_x (Cole–Hopf) e KdV (IST); slot (v): odografo/Riemann (2×2), Miura, Carrier–Greenspan, tropicalizzazione (NEW-ROUTE, fusa in RT-R7b).
- Problema 1 (rinviato): Cole–Hopf stocastico (KPZ) e Feynman–Kac solo annotati.

## 5. Stato
- NOTO: P1, P3, P5, P6, P8; scomposizione EB (T1).
- APERTO: Q1 (RKHS via Cole–Hopf), Q2 (E_int solitonico con radiazione in linguaggio P1), Q3 (identificabilità non lineare generale), Q5 (tropicale), Q6 (E_int di Kramers in forma chiusa).
- PROBABILMENTE FALSO: "ogni termine dell'operatore ha la sua classe di nucleo" (falso per termini non lineari e per operatori del 2° ordine in t); "E_int → 0 asintoticamente" per KdV senza correggere le fasi (resta ≈4 in L¹).
