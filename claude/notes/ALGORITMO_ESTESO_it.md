# ALGORITMO_ESTESO — specifica della pipeline estesa (Fase 9)

Sessione S9-ALG. Revisione 2 del 27/10/2026, che recepisce ATTACK-9 (DEVIL-9); la mappa dei fix è in `work/S9-ALG/RECEPIMENTO.md`.

**Fonti.** claims/LEDGER.md, con la tabella «Decisioni di stato del coordinatore» del Gate 8, che prevale sulle celle delle righe di sessione; GATE8; **NOTAZIONE v6**; ATTACK-8; ATTACK-9; research/CIT-AUDIT/AUDIT-9; i PROOF_PACKAGE di S8-CONV, S8-DICT, S8-VAR, S8-SYS, S8-ENC e C3.

Questa specifica **non introduce claim nuovi**. Compone righe già presenti nel LEDGER. Gli esempi del §9 sono verifiche V-ex (SymPy/mpmath) e non sono teoremi.

---

## §0 Convenzioni

### 0.1 Stati e regola di fondamento (ATTACK-9 O6)
- Un passo si **fonda** solo su righe DIMOSTRATO, oppure CON-FONTE con la fonte **verificata** (CIT-AUDIT o una nota del LEDGER che riporta la verifica).
- Un CON-FONTE con la dicitura «da verificare», o senza verifica registrata, non è un fondamento. Il passo che lo usa è marcato **«condizionato a verifica»**, e il §10 elenca le citazioni da chiudere.
- PROVA SCRITTA, CANDIDATO, APERTO, CONDIZIONALE e V-ex sono citati sempre con la marca accanto. Non sono mai garanzie.
- FALSO è citato solo come modo di fallimento, cioè come ciò che l'algoritmo **non** deve promettere.
- Stati aggiornati alla data di questa revisione:
  - **DICT-R6**: (a)–(f) tutti DIMOSTRATO; (f) dopo R6f-1 e R6f-2, recepiti nel PP §3.6 (tabella del Gate 8).
  - **VAR-L2-cor**: CON-FONTE, ereditato da VAR-P11(e), Pazy cap. 5, senza verifica registrata. Nessun passo lo usa (O17); compare solo nel §10.
  - **C3-A1** (algoritmo e costo in M1/M2): PROVA SCRITTA non auditata, senza riga nel LEDGER. Ogni uscita che ne dipende è «(A) condizionato a C3-A1» (O7).

### 0.2 Sensi di «identifica» (NOTAZIONE v6; ATTACK-8 O5)
Ogni passo dichiara quale senso usa. «Identifica» senza etichetta non compare.

| etichetta | significato | quando vale l'unicità |
|---|---|---|
| **ID-ann** | Ann(u) = (P): l'ideale annullatore è principale e generato dalla legge | sempre, se l'uguaglianza è provata. **Mai per u EP** (P4-T2: σ_p ≠ ∅; ATTACK-9 O2) |
| **ID-ker** | ker Φ_u = 0 nella classe parametrica fissata | **solo sotto (H-ex)**: una legge della classe esiste (DICT-RANGO; controesempio u = t + sin x, §9.5(d)) |
| **ID-res** | i coefficienti sono determinati dalla mappa dei residui ρ_u in forma fissata, p. es. V = (iu_t + u_xx)/u | su {u ≠ 0}, nelle classi di VAR-T1 |
| **ID-fam** | identificazione modulo una famiglia: V + c in DM-φ; [A] modulo gauge; encoder (E2) modulo c(t) | — |
| **ID-lim** | identificazione nel limite (I-LIM, CONV-T1, CONV-T2/T2′), mai certificata a tempo finito | sotto (H-ID) |

- **(H-ex)**: nella classe considerata esiste almeno una legge soddisfatta da u.
- **(H-ID)**: Ann(u) ∩ span 𝓓_n = ⟨L⟩_n per n ≥ n_0 (DICT-GR). L'etichetta «(ID)» è un sinonimo deprecato (NOTAZIONE v6).

### 0.3 Modelli di dato (NOTAZIONE v4 e v6; ATTACK-9 O2, O3, O4, O13, O30)

| modello | dato | sensi ammessi | contratto |
|---|---|---|---|
| **DM1** (= M1) | formula EP: combinazione finita di esponenziali-polinomi | **solo ID-ker in una classe finita**, cioè l'identificazione relativa (C3-T4, C3-T2(c,d), soglia di Bézout). **Mai ID-ann**: per u EP la varietà di Ann(u) è finita, σ_p ≠ ∅ (P4-T2) | (A) nella classe dichiarata |
| **M3-hol** | forma chiusa olonoma non EP (Bessel, Airy, sech, gaussiane), data come espressione esatta | ID-ann, ID-res, ID-ker (H-ex), con prova simbolica | (A); decidibilità modulo (AC) (OP-ALG-T1 = C3-Q1 nel modello M3-hol) |
| **DM2** (= M2) | getto in un punto | **solo ID-lim** (CONV-T1); nessun certificato a tempo finito (CONV-T1: «nessun certificato corretto»; C3-P1[M2]) | (Lim); il certificato è (C) |
| **M2⁺** | getto più test di zero (P4 §6) o ideale olonomo dichiarato | decidibilità esatta modulo (AC) nella classe di P4-T6 (P monico in τ, u analitica, dati di Cauchy D-finiti) | (A) modulo (AC) |
| **DM3** (= M3) | u nota esattamente in H^m(Ω), o in C^∞(Ω) | ID-ann, ID-res, ID-ker (H-ex), ID-fam; con calcolo numerico solo misfit e fit (§4) | (A) con prova simbolica; (A)/(B) numerico (§4) |
| **DM-φ** | dato noto a meno di una fase globale e^{iφ(t)} | ID-fam (V modulo funzioni di t) | come il modello sottostante |
| **DM-inv** | solo grandezze invarianti di gauge | ID-fam ([A], G-T2) | come il modello sottostante |
| **DM-δ(Y)** | ũ con ‖ũ − u‖_Y ≤ δ, **norma Y dichiarata** | nessuna identificazione. Valgono: moduli di VAR-P3 (Y ⊇ C^{1,2} con minorante κ di \|u\| su K, che VAR-P3 chiama «δ»), stabilità condizionata di CONV-T4/T5 (Y = H^n o H^{n+s}), negativa DICT-N1(ii) | (B) condizionato a una soglia non certificabile (CONV-T5); altrimenti (C) |

Note:
1. **DM-δ è un'estensione** di PROBLEM v3.1: G★″ non contiene un modello di rumore (O30). È un modificatore ortogonale ai modelli di sopra, per esempio DM3^δ(H^n).
2. **Senza Y il modello non è definito** (O13). In Y = C¹ non c'è controllo su V: con u = 1 e u_δ = 1 + δ² sin(x/δ) si ha ‖u_δ − u‖_{C¹} ≤ δ + δ², ma |V_δ| arriva a 1/(1 − δ²) (ATTACK-9 §3(F)). Le norme ammesse sono almeno C^{1,2}, oppure H^m con m ≥ ordine + 1, come in VAR-P3 e CONV-T4.
3. GATE8 §5, ATTACK-8 O8 e VAR-Q19 dicono «DM2» per il rumore: va letto come DM-δ (NOTAZIONE v6). Anche la riga CONV-T5, etichettata «DM3» nel LEDGER, tratta di fatto DM3^δ.
4. **Gli esempi §9.1–9.3 sono M3-hol/DM3, non DM1.** I loro dati sono forme chiuse non EP.

### 0.4 Contratto: completezza e correttezza (ATTACK-9 O1)
Il contratto di CONV-T7 (proposizione DIMOSTRATO; nel contratto, «Magnus (B)» è condizionato) ha quattro classi:
- **(A)** finito/esatto;
- **(B)** convergente con stima esplicita ε_i;
- **(C)** nessuna garanzia;
- **(Lim)** nel limite, senza certificato.

La pipeline ha **due strati**:

1. **Condizionamento (passi 1–3).** Fissano modello, livello n, classe K e senso ID-*. Le loro uscite sono **discrete** (un modello, un livello, un ideale, una classe). Ann(·) è discontinuo in ogni punto (CONV-T3), quindi non esiste una costante di Lipschitz e il bound di CONV-T7 **non si applica** a questi passi.
   - La **completezza** («la legge giusta è nel livello scelto») è sempre **(C)**: il livello è scelto con la regola euristica R4, e CONV-T1 e CONV-T2′ escludono un criterio a priori.
   - Se il budget si esaurisce, l'uscita è `NON-DECISO`.
2. **Correttezza condizionata (passi 4–6).** **Al livello n e nella classe K dichiarati**, i passi 4 → 5 → 6 hanno uscite metriche (residui, coefficienti, componenti). Su questa sottocatena CONV-T7 si applica: d(x̃_k, x_k) ≤ Σ_i (∏_{j>i} L_j) ε_i, purché ogni passo sia (A) o (B) e lipschitziano sugli ingressi calcolati. Un passo (C) o (Lim) rende (C) o (Lim) la sottocatena a valle.

Ogni uscita porta perciò **due etichette**: completezza (sempre (C), oppure (A) solo nei casi decidibili DM1-relativo, M3-hol e M2⁺ modulo (AC)), e correttezza condizionata ((A), (B), (C) o (Lim)).

### 0.5 Etichette d'uscita (ATTACK-9 O25, O26, O27)
La pipeline **non emette mai** «legge identificata» a partire da dati numerici finiti (DICT-N1(ii), DICT-A-iii, C3-P1[M2]). Le uscite ammesse sono:
- `MISFIT(certificato)` al livello n;
- `FIT-COMPATIBILE(n, r_n, bound)`;
- `IDENTIFICATA[senso, modello]`, solo con prova simbolica esatta in DM3, M3-hol o M2⁺ (modulo (AC)), oppure relativa a una classe finita in DM1 (senso ID-ker). Il senso è uno tra ID-ann, ID-res, ID-ker (con (H-ex)) e **ID-fam** (DM-φ, DM-inv, encoder);
- `ID-LIM(n)`: candidato corrente di una regola nel limite (DM2), senza certificato;
- `NON-DECISO`: budget esaurito, oppure nessun livello entro il budget dà misfit o fit.

---

## §1 Passo 1 — Modello di dato (condizionamento)

| voce | contenuto |
|---|---|
| **Input** | il dato u e la sua dichiarazione di modello (tabella §0.3); per DM-δ, la norma Y e δ; budget (livello massimo n_max, precisione di lavoro) |
| **Output** | modello fissato; anello dei coefficienti dichiarato (Gate 8b, NOTAZIONE v6: ℂ[∂], ℂ(x)[∂] o A_n, oppure una classe parametrica); dominio Ω; classe di regolarità; insieme dei sensi ID-* raggiungibili |
| **Claim → stato** | C3-P1[M2] DIMOSTRATO (nessun getto finito in un punto certifica Ann(u) = (P)); P4-T5 DIMOSTRATO (impossibilità a scatola nera senza dato aggiuntivo, M2⁺); CONV-T1 DIMOSTRATO (in DM2 nessun certificato corretto; K* non è maggiorato da d); C3-T3 DIMOSTRATO (**solo per u EP**: il getto d'ordine 2d−1 determina Ann(u)); C3-T2(c,d) DIMOSTRATO (soglia di Bézout per dati EP); P4-T2 DIMOSTRATO (u EP ⇒ σ_p ≠ ∅ ⇒ niente ID-ann); P4-T6 DIMOSTRATO modulo (AC) (M2⁺); OP-ALG-T1 DIMOSTRATO modulo (AC) (M3-hol); VAR-P4 DIMOSTRATO (DM-φ: compatibili = {V + c}); G-T2 DIMOSTRATO, CON-FONTE nella sostanza (DM-inv: al più [A]); VAR-P3 DIMOSTRATO come stima di modulo, **non** come certificato (DM-δ) |
| **Ipotesi** | Ω aperto connesso; (AC) per P4-T6 e OP-ALG-T1; norma Y dichiarata in DM-δ |
| **Costo** | DM1: lineare nella lunghezza della formula; getto di un dato EP: ordine 2d−1, O(d²) coefficienti in 1+1 (C3-T3) |
| **Fallimenti** | DM1: mai ID-ann (P4-T2; ATTACK-9 §3(B): u = e^{−t}cos x risolve il calore, ma ∂_t + 1 e ∂_x² + 1 stanno in Ann(u)); DM2: nessun certificato (CONV-T1; ATTACK-9 §3(C): i getti d'ordine 2, 4, 6 di una soluzione non EP coincidono con quelli di polinomi del calore); DM-φ: V solo modulo funzioni di t; DM-inv: A solo modulo gauge; DM-δ in C¹: nessun controllo su V (§0.3, nota 2) |
| **Senso** | fissa i sensi raggiungibili secondo la tabella §0.3 |
| **Contratto** | condizionamento: uscita discreta, fuori da CONV-T7. Completezza (A) per la dichiarazione del modello (è un ingresso) |

---

## §2 Passo 2 — Scelta del livello di 𝓓_∞ (L0–L10) (condizionamento)

La filtrazione del dizionario (S8-DICT §6, regola R0) ha famiglie LIN, LOC, NL, EXP, SYM, MEM, DEL, FRAC, SING, SYS, ciascuna con altezza h. I livelli operativi sono:

| livello | classe | passo 3 relativo |
|---|---|---|
| L0–L2 | scalare a coefficienti costanti, P monico in τ, grado crescente | C3, P4 |
| L3 | non monico / grado ≥ 2 in τ | OPF, P1 |
| L4 | non lineare polinomiale (G★′-NL) | S4ID |
| L5 | memoria/ritardo (MEM, DEL), via sistema aumentato | DICT-RIT1, CONV-MZ |
| L6 | sistemi a coefficienti costanti (Dirac, Lamé, Maxwell) | SYS |
| L7 | coefficienti variabili in x (Schrödinger stazionario, Airy) | VAR, ENC |
| L8 | coefficienti dipendenti da (t, x) (Stark, oscillatore H = −∂² + x², Floquet) | VAR-T1(c), VAR-T10 |
| L9 | non locali (FRAC, moltiplicatori di Fourier) | CONV-T6 |
| L10 | dizionario generale con test di misfit e arresto | DICT |

| voce | contenuto |
|---|---|
| **Input** | modello (passo 1), budget n_max, eventuale conoscenza a priori (q noto, simmetrie) |
| **Output** | livello n e insieme finito di atomi 𝓓_n; sequenza di livelli da provare in ordine di altezza; `NON-DECISO` a n = n_max senza esito |
| **Claim → stato** | DICT-N2 DIMOSTRATO (S^m non è separabile: non esiste un dizionario numerabile esaustivo); DICT-N3 DIMOSTRATO (il ritardo dista ≥ 1 dal dizionario locale); DICT-RIT1 DIMOSTRATO (ritardo = trasporto aumentato); DICT-N1iii DIMOSTRATO (non monotonia); DICT-N1v DIMOSTRATO (le u con legge nel dizionario sono un insieme magro e shy); CONV-T2′ DIMOSTRATO (nessun learner identifica Ann su {Ann principale} ∪ {Ann = 0}) |
| **Ipotesi** | dizionario finito a ogni livello; atomi linearmente indipendenti su Ω |
| **Costo** | per LIN in 1+1, (n+1)(n+2)/2 monomi di grado ≤ n. Per le altre famiglie il conteggio dipende dall'altezza h e dalla parametrizzazione (NL: monomi nelle derivate fino al grado dichiarato; SYS: r² per ogni monomio): nessuna stima generale dimostrata (O29) |
| **Fallimenti** | la scelta del livello è **euristica** (R4: completezza (C)); un atomo non locale non è mai raggiunto dal dizionario locale (DICT-N3, CONV-T6); un u generico non ha legge (DICT-N1v) |
| **Senso** | nessuno: il passo sceglie soltanto lo spazio di ricerca |
| **Contratto** | condizionamento: completezza (C); arresto a n_max con `NON-DECISO` |

---

## §3 Passo 3 — Identificazione (condizionamento della classe)

### 3a. Scalare a coefficienti costanti (L0–L5)
| voce | contenuto |
|---|---|
| **Input** | u in DM1, M3-hol, M2⁺ o DM3; livello n |
| **Output** | Ann(u) ∩ R_{≤n}, il gcd G_u, lo spettro puntuale σ_p, la decisione ID-ann (non in DM1) o ID-ker relativa (DM1) |
| **Claim → stato** | II-C1 = C3-T1(d) DIMOSTRATO (Ann(u) = (P) ⟺ u, ∂_tu, …, ∂_t^{k−1}u sono ℂ[∂_x]-indipendenti, P monico in τ); R4-T5[ℝ] = C3-T1 DIMOSTRATO (test w_i ∉ EP); C3-T6 DIMOSTRATO (G_u ricostruito da qualsiasi annullatore con un test EP); P4-T2 DIMOSTRATO (Ann(u) = (P) ⟺ σ_p = ∅ e G_u ∼ P); C3-T4 DIMOSTRATO (u_t = a(∂_x)u: **ID-ker relativa** nella classe deg a ≤ n, O24); C3-T2(c,d) DIMOSTRATO; S4ID-T1, S4ID-P1 DIMOSTRATO (non lineare); CONV-MZ1, CONV-MZ2 DIMOSTRATO (eliminazione: (det D)U_i = 0) |
| **Ipotesi** | Ω connesso; P monico in τ per II-C1; coefficienti costanti |
| **Costo** | C3-A1: eliminazione a costo polinomiale — **PROVA SCRITTA**, non auditata, senza riga nel LEDGER |
| **Fallimenti** | u EP: Ann(u) contiene sempre operatori estranei (σ_p ≠ ∅), quindi mai ID-ann; CONV-T3 DIMOSTRATO (Ann(·) discontinua ovunque, i due insiemi densi) |
| **Senso** | **ID-ann** in M3-hol, M2⁺ (modulo (AC)) e DM3 con prova simbolica; **ID-ker relativa** in DM1; ID-lim in DM2 |
| **Contratto** | condizionamento: decisione discreta. Correttezza (A) con prova simbolica; «(A) condizionato a C3-A1» se si usa l'algoritmo di eliminazione |

### 3b. Sistemi (L6)
| voce | contenuto |
|---|---|
| **Input** | u ∈ 𝒜^r (𝒜 = C^∞(Ω) o 𝒟′(Ω)), classe di sistemi P ∈ R^{s×r} |
| **Output** | test di esistenza di una u identificante; per u data, decisione ID-ann oppure ID-ker nella classe hamiltoniana; criterio dei componenti |
| **Claim → stato** | SYS-EX: su Ω arbitrario DIMOSTRATO con prova propria (EX-L1, EX-L2, Passi 1–3), che non dipende da Oberst per il valore di verità; caso ℝ^n NOTO (Oberst 1993, letto solo nell'abstract); Ω convesso PROBABILMENTE NOTO (Oberst 1990 (4.32), VERIFICATO in CIT-AUDIT-9 C1). SYS-N1: NOTO/folklore, DIMOSTRATO su Ω arbitrario. SYS-T0: NOTO (Heij 1992). SYS-C1 DIMOSTRATO (det P ≠ 0, n ≥ 2 ⇒ ∃ u identificante). SYS-S1(i⇒), (i⇐) [con Ext¹(N, 𝒜) = 0], (ii) DIMOSTRATO. LAME-3 DIMOSTRATO con ρ ≠ 0, μ ≠ 0, λ + μ ≠ 0, λ + 2μ ≠ 0 (O19). **H-DIRAC** DIMOSTRATO sotto H-DIRAC-1 e H-DIRAC-2, con m ≠ 0 e la base delle matrici fissata (α = σ_x, β = σ_z in 1+1) (O20). SYS-N3 DIMOSTRATO (magnetico: famiglia affine, div(ρ²B) = 0). DICT-MAG-NU DIMOSTRATO |
| **H-DIRAC, due sensi (O5)** | **H-DIRAC-ann**: la premessa «ψ identifica L_0» è ID-ann; criterio d'indipendenza in 1+1 ψ_2 ∉ EP. **H-DIRAC-ker**: nella classe hamiltoniana iψ_t = Aψ_x + Bψ (8 incognite in 1+1) il sistema lineare puntuale ha rango 8. Questo vale per ψ non EP (§9.1) e anche per un dato EP con ≥ 4 modi generici (ATTACK-9 §3(A): 4 onde piane, rango esatto 8, soluzione unica). Fallisce con 1 sola onda piana (rango 2). ID-ker richiede (H-ex) |
| **Ipotesi** | Ω aperto connesso; Ext¹(N, 𝒜) = 0 per SYS-S1(i⇐); le ipotesi di Lamé e Dirac sopra |
| **Costo** | rango del sistema lineare puntuale nella classe hamiltoniana: 2r² incognite (8 per Dirac 1+1) |
| **Fallimenti** | SYS-N1 (zoccolo ≥ 2: nessun dato identifica); SYS-S1-C **FALSO** (senza ipotesi su N la somma dei nuclei non basta); LAME-3 falso per λ = −2μ; ID-ker con troppo pochi modi (una sola onda piana: rango 2 su 8); magnetico: mai unicità di (A, V), solo ID-fam |
| **Senso** | ID-ann (SYS-EX, SYS-C1, H-DIRAC-ann); ID-ker con (H-ex) (H-DIRAC-ker); ID-fam (magnetico) |
| **Contratto** | condizionamento. Correttezza (A) con prova simbolica. **Novità condizionata a CIT** (O14): CIT-AUDIT-9 ha verificato Oberst 1990; Oberst 1993 è PARZIALE (testo pieno non accessibile). Il delta (Ω connesso con C^∞(Ω) non iniettivo) ha rischio residuo basso–medio e resta fuori dalle promesse di novità del §8 |

### 3c. Coefficienti variabili (L7–L8)
| voce | contenuto |
|---|---|
| **Input** | u in DM3, M3-hol o DM-φ; anello dei coefficienti dichiarato; classe di regolarità (SF) |
| **Output** | coefficiente V tramite la mappa dei residui ρ_u, oppure l'insieme affine dei compatibili θ_0 + ker Φ_u; oggetto canonico ((D·u, u), ρ_u) (NOTAZIONE v6) |
| **Claim → stato** | VAR-N1 DIMOSTRATO (vacuità in un campo ∂-chiuso: il campo dei coefficienti va fissato); VAR-T1(a) DIMOSTRATO; VAR-T1(b) DIMOSTRATO (V(x): ogni u ≢ 0 in (SF) identifica V q.o.); VAR-T1(c)(i)–(iii) DIMOSTRATO (V(t,x), fuori dalle fasce di silenzio: identifica ⟺ int Z(u) = ∅ per V continuo, oppure \|Z(u)\| = 0 per V ∈ L^∞); VAR-P5(a)(b) DIMOSTRATO (Dirac); VAR-T2a DIMOSTRATO (K = ℂ(x), u D-finita); VAR-E1 DIMOSTRATO (Airy); VAR-C3Q2(a)–(g) DIMOSTRATO; DICT-RANGO, DICT-RANGO-cor DIMOSTRATO come ID-ker sotto (H-ex); VAR-L2 DIMOSTRATO (continuazione unica; Isakov 1993 VERIFICATO su fonte secondaria, CIT-AUDIT-9 C4). **Condizionato a verifica**: VAR-T6, CON-FONTE (vdPS Prop. 1.34/Thm 1.27 «da verificare»), usato solo per la struttura socle/Loewy |
| **Ipotesi** | u ∈ (SF); DM3 o M3-hol; V ∈ L^∞_loc o continuo |
| **Costo** | ρ_u: due derivate e una divisione per punto; ker Φ_u: un sistema lineare nella classe |
| **Fallimenti** | VAR-T1(c)-F **FALSO** (serie di Tychonoff); fasce di silenzio int Z(u) ≠ ∅; DICT-N1vi **FALSO**; VAR-T1(c)-Q10 APERTO; x∂_t non è mai identificato (VAR-C3Q2) |
| **Senso** | **ID-res** (VAR-T1(b)(c), VAR-P5); ID-ker sotto (H-ex) (RANGO); ID-fam (DM-φ: V + c(t); magnetico) |
| **Contratto** | condizionamento. Correttezza: (A) con prova simbolica; ρ_u numerico è (B) solo con il modulo di VAR-P3 su K, con \|u\| ≥ κ |

---

## §4 Passo 4 — Certificato di misfit o migliore approssimazione (correttezza)

| voce | contenuto |
|---|---|
| **Input** | u in DM3 (o DM3^δ(Y)); livello n e classe dal condizionamento; atomo guida D_0; W_n = span(D_1u, …, D_Nu) in Y = L²(Ω) o H^s; precisione di lavoro p |
| **Output** | `MISFIT(certificato)` se r_n > 0 è certificato; altrimenti `FIT-COMPATIBILE(n, r_n, coefficienti con bound)` |
| **Claim → stato** | DICT-MF (MF1, MF2, MF3 (a)–(d), MF-C) DIMOSTRATO — MF1: distanza come duale di Hahn–Banach; MF2: r_n² = det G(D_0u, D_1u, …)/det G(D_1u, …); MF3: forma debole, robusta se σ_{N+1}(A(ũ)) > ‖δ‖_F (semi-decisione). DICT-A DIMOSTRATO (misfit aperto con certificato finito; fit chiuso con interno vuoto). DICT-A-iii DIMOSTRATO (fit non certificabile da dati finiti esatti, atomi differenziali). DICT-B2 DIMOSTRATO (\|c − c̃\| ≤ 2η/√λ_min). DICT-R3 DIMOSTRATO. DICT-GR DIMOSTRATO (R1 si ferma a n_0 sotto (H-ID)). CONV-T4 DIMOSTRATO (Lipschitz 2δ/ρ, Hölder; Stein 1970 verificato da CIT-AUDIT-8). CONV-T5 DIMOSTRATO (la regola di discrepanza seleziona m = d; **soglia δ₀ non minorabile dai dati**). DICT-ILIM-H0 DIMOSTRATO. **Condizionati a verifica**: DICT-ILIM (ramo (H2) via Whitney–Stein «da verificare»); DICT-B3 (CON-FONTE da verificare). **CANDIDATO**: DICT-ILIM-Hs |
| **Calcolo (O10)** | r_n si calcola come **residuo di minimi quadrati** (QR, oppure equazioni normali seguite dal residuo diretto ‖D_0u + Σc_iD_iu‖), non come rapporto di determinanti di Gram. Il rapporto MF2 serve alla prova, ma è numericamente singolare quando D_0u sta nello span (ATTACK-9 §3(G)) |
| **Ipotesi** | atomi indipendenti su Ω; Ω limitato lipschitziano (CONV-T4); margine σ_2 ≥ ρ; λ_min > 0 (DICT-B2) |
| **Costo** | Gram (N+1)×(N+1): O(N²) prodotti scalari, ciascuno una quadratura su Ω; QR O(N³). **Precisione di lavoro** p ≳ log₁₀(1/λ_min) cifre: l'esempio §9.5 ne usa 25. MF3 richiede un SVD della matrice dei test |
| **Fallimenti** | il fit non è mai certificabile (DICT-A, A-iii, N1(ii)); in DM-δ il misfit è certificato solo se r_n supera il rumore propagato, e la soglia di CONV-T5 non si stima dai dati; λ_min → 0 rende B2 vuoto; atomi non locali: A(iii) non provato (§11) |
| **Senso** | il misfit non identifica: esclude. Il fit dà al più **ID-ker** al livello n, con (H-ex), e **ID-lim** al crescere di n (DICT-GR, I-LIM) |
| **Contratto** | misfit: **(A) solo con un'inclusione rigorosa** di r_n (aritmetica intervallare o bound d'errore della quadratura); con la quadratura in virgola mobile senza bound è (B). Fit: (B) con bound B2/CONV-T4 al livello fissato. Arresto R5: (Lim) |

---

## §5 Passo 5 — Encoder analitico per V (correttezza)

L'encoder è una **traduzione** a q noto, **non una sorgente d'informazione** (ATTACK-8 O7). Trasporta un problema a coefficienti variabili in uno a coefficienti costanti, dove si applicano 3a e 4, e riporta indietro i certificati. Nella forma non autonoma soddisfa (E2) con c(t): W(t)(i∂_t − H(t)) = (i∂_t − H_0 − c(t))W(t). Il caso con c costante è (E2₀) (NOTAZIONE v6).

Due tipi di traduzione, da non confondere (O12):

| tipo | operatore | contratto |
|---|---|---|
| **limitata** | W_q Volterra simmetrico (ENC-1): ‖W‖, ‖W^{−1}‖ ≤ C_W | (A) per l'intrecciamento esatto; (B) per i certificati trasportati, con fattore C_W², **solo se q è dato esattamente** |
| **Darboux** | A differenziale (ENC-K1′): non limitato, con nucleo non banale | (C): C_W non si applica, i modi del nucleo si perdono e un dato identificante può diventare EP (§9.2) |

| voce | contenuto |
|---|---|
| **Input** | q (o V) **dato**; u in DM3 o M3-hol; J = [x_0 − a, x_0 + a]; sottoanello di operatori ammesso |
| **Output** | Wu (dato tradotto), operatore tradotto L̂, certificati trasportati ψ ↦ ψ∘W, costante C_W |
| **Claim → stato** | ENC-1 DIMOSTRATO (Volterra simmetrico, L_qT = TL_0, conserva i dati di Cauchy, stabilità Lipschitz); ENC-U1 DIMOSTRATO; ENC-C1 DIMOSTRATO (P(∂_t, L_q)u = 0 ⟺ P(∂_t, L_0)(Wu) = 0); **ENC-T2 DIMOSTRATO** (lemma, O18); ENC-T2(c′): osservazione in C^∞ senza vincoli DIMOSTRATO, FALSO con vincolo di grado, APERTO nella classe principale (R6 non lo usa); ENC-K0 DIMOSTRATO; ENC-K1′ DIMOSTRATO (i W differenziali sono catene di Darboux; prior art Andrianov–Sokolov VERIFICATO, CIT-AUDIT-9 C6); ENC-P0(b)^cl DIMOSTRATO e ENC-P0(b)^loc in versione corretta DIMOSTRATO (nessun encoder indipendente da t per V(t,x) generico); ENC-P0′ astratto e nucleo denso DIMOSTRATO; ENC-P0′-DIC: FALSO per un rappresentante arbitrario, forma esistenziale DIMOSTRATO; POLE-N^cl DIMOSTRATO; ENC-N1 **FALSO**; ENC-N1′ DIMOSTRATO solo come lemma di riduzione; FAD-1 DIMOSTRATO; FW-1 DIMOSTRATO per il libero (con V: CON-FONTE, condizionato a verifica); NS-EQ-Ω DIMOSTRATO; **DICT-R6 (a)–(f) DIMOSTRATO** (O16) |
| **Ipotesi** | q ∈ C¹(J) (C^∞ per ENC-C1), noto esattamente; sottoanello pari ℂ[∂_t, L_q]; rettangolo simmetrico; DM3 |
| **Costo** | C_W = 1 + a²Q·e^{a√Q}, con Q = ‖q‖_∞ (DICT-R6). Le distanze e λ_min si confrontano a meno di C_W². Il nucleo K si ottiene da un problema di Goursat sul triangolo caratteristico: con M nodi per lato, O(M²) valutazioni di q con uno schema di quadratura iterata (stima indicativa, non dimostrata; O29) |
| **Perdita del bound (O32)** | C_W è l'unico bound dimostrato e cresce come e^{a√Q}. A a√Q = 5, C_W² ≈ 1,4·10⁷, mentre cosh²(a√Q) ≈ 5,5·10³ (ATTACK-9 §3(H), V-ex): i certificati trasportati possono perdere circa quattro ordini di grandezza. Un bound più stretto (cosh(a√Q) o Gronwall esatto) è una domanda aperta (§11) |
| **Fallimenti** | q ignoto: l'encoder non fornisce informazione (O7); **q ricavato dal passo 3c** anziché dato: la costante di Lipschitz di q ↦ W_q (ENC-1, C(a, Q, Q′)) non è esplicita, quindi il trasporto è (C); V(t,x) generico: nessun encoder indipendente da t (ENC-P0(b)); Darboux: perdita dei modi legati e dell'identificabilità ID-ann (§9.2) |
| **Senso** | nessun senso nuovo: il passo conserva il senso del passo 3/4 che traduce (ENC-C1); ID-fam modulo c(t) nella forma (E2) |
| **Contratto** | traduzione limitata a q dato: (A) intrecciamento, (B) certificati con C_W². Traduzione limitata con q stimato: (C). Darboux: (C) |

---

## §6 Passo 6 — Scomposizione in fattori e termini; E_int nel senso A9 (correttezza)

| voce | contenuto |
|---|---|
| **Input** | legge P (o la sua candidata) con la fattorizzazione P = ∏Q_j; dato u |
| **Output** | componenti u_j ∈ ker Q_j; ambiguità δ(P); termini d'interazione E^add, E^mult (definizione A9) con stime |
| **Claim → stato** | C12-T1 DIMOSTRATO (Ω rettangolo) e **C12-T1′** DIMOSTRATO (Ω semplicemente connesso, H¹_dR(Ω) = 0): ker P = Σ ker Q_j, δ(P) = Σ_{i<j} dim R/(Q_i, Q_j), unicità ⟺ varietà disgiunte. C12-P7(a–d) DIMOSTRATO (componenti in H^m ⟺ somma dei nuclei chiusa e densa; γ_N > 0). OPF5B-T1 DIMOSTRATO mod F1, F2 CON-FONTE verificate. II-T2 DIMOSTRATO. P1-T2 = R5-T2[𝔅] DIMOSTRATO (E^mult = 0 in 𝔅). OPF-L1, OPF-T1, OPF-L2, OPF-T2, OPF-P3, OPF-P4, OPF-C1 DIMOSTRATO. P1-T3 DIMOSTRATO (complessità, O23). P1-T5 DIMOSTRATO. SYS-E1, SYS-E2, SYS-E3 DIMOSTRATO. ENC-A9(b): (b1), (b2), (b4) DIMOSTRATO, (b3) CON-FONTE + V-ex. VAR-P9 DIMOSTRATO. Burgers: Lemma J, S4T-T1, S4T-L0, S4T-L1, S4T-T2, S4T-P3 DIMOSTRATO; S4T-L2, S4T-T3 (i, ii, v, vi, vii) DIMOSTRATO mod [F1] (Lax–Oleinik = Kružkov, CON-FONTE da verificare: condizionato a verifica) (O21). P2-T4 DIMOSTRATO (ogni selezione esatta ha Lip ≥ γ_N^{−1/2}) |
| **Ipotesi** | Q_j a due a due coprimi; per i sistemi «componente = fattore» richiede Ext¹(N, 𝒜) = 0 (Gate 8b, NOTAZIONE v6); Ω limitato lipschitziano per C12-P7 |
| **Costo** | P1-T3: Θ(M2^N(L+1)²) DIMOSTRATO nel modello di costo unitario |
| **Fallimenti (O11)** | **C12-C1 FALSO** (la scomposizione non conserva H^m: perdita esatta di 1 derivata). **C12-P10** DIMOSTRATO e **OPF-T4** DIMOSTRATO: su Ω non semplicemente connesso la scomposizione fallisce sul nucleo di ι (difetto ≤ δ(P)·b₁(Ω)) → `NON-DECISO` per le componenti. **CONV-D1** DIMOSTRATO: in 1+d, d ≥ 2, l'ambiguità è infinita salvo fattori comassimali (Lamé, Maxwell in L6) → (C). **OPA-T3(a–d)** DIMOSTRATO e **P1-P1(e)** FALSO come estensione continua: E^add è illimitata H^m → L², quindi E_int da un dato approssimato è (C). **CONV-B1** DIMOSTRATO: le condizioni al bordo sono invisibili ad Ann(u) → la scomposizione non le restituisce. Somma dei nuclei non chiusa (γ_N = 0): componenti instabili (P2-T4). Varietà non disgiunte: δ(P) > 0. Sistemi senza Ext¹ = 0: SYS-S1-C |
| **Senso** | il passo non identifica la legge: la presuppone. Le componenti sono uniche solo per varietà disgiunte |
| **Contratto** | (A) in 𝔅 e nel caso commutativo; (B) con γ_N^{−1/2} (C12-P7) o con il resto di Faddeev (FAD-1); (C) se γ_N non è stimato, per E_int da dato approssimato, e nei casi CONV-D1 |

---

## §7 Passo 7 — Garanzie di convergenza

| voce | contenuto |
|---|---|
| **Input** | etichette di completezza dei passi 1–3; la sottocatena 4 → 5 → 6 con costanti L_i ed errori ε_i |
| **Output** | per ogni uscita, l'etichetta di completezza e quella di correttezza condizionata (§0.4), con il bound della sottocatena |
| **Claim → stato** | CONV-T7 proposizione DIMOSTRATO (contratto con Magnus (B) condizionato); CONV-T1 DIMOSTRATO; CONV-T2, CONV-T2′ DIMOSTRATO; CONV-T3, CONV-T4, CONV-T5, CONV-T6 DIMOSTRATO; CONV-T8 DIMOSTRATO in L² (Lie ordine 1; Strang Θ(h^{5/4}) con Dirichlet; ordine 1 in L^∞ solo V-ex); II-T7 DIMOSTRATO; P1-T4 DIMOSTRATO, con Lie CON-FONTE (Humphreys §4.1 Cor. B, verifica non registrata: condizionato a verifica); VAR-P8(a) DIMOSTRATO, VAR-P8(b) «⟹» DIMOSTRATO e «⟸» CON-FONTE (Wei–Norman 1964: CIT-AUDIT-3 ha verificato i metadati, la globalità solo da fonti secondarie; condizionato a verifica); VAR-P11 (a)–(d) DIMOSTRATO, (e) CON-FONTE (Pazy cap. 5, condizionato a verifica); **VAR-T10**: (1) e (3)(i)–(ii) DIMOSTRATO (Stark globale; oscillatore H = −∂² + x², rottura a cos t = 0, lente); (3)(iii) CON-FONTE + V-ex; (2), (5) CON-FONTE; **(4) Magnus ∫‖A‖ < π: CON-FONTE (Casas Thm 3.4)** (O9); VAR-P12 (a)–(c) DIMOSTRATO, (d) APERTO; DICT-N1iv-bc DIMOSTRATO |
| **Ipotesi** | passi 4–6 lipschitziani sugli ingressi calcolati |
| **Costo** | il bound Σ_i (∏_{j>i} L_j) ε_i si calcola in O(k) operazioni, accumulando da destra il prodotto (O29) |
| **Fallimenti** | CONV-T2/T2′: nessuna procedura nel limite decide l'esistenza di una legge; CONV-T3: discontinuità ovunque (per questo i passi 1–3 stanno fuori dalla catena); CONV-T5: soglia non certificabile; Magnus fuori dalle ipotesi → (C); CONV-R1-F, CONV-MZ3-F **FALSO** |
| **Senso** | **ID-lim** (CONV-T1) è l'unico senso che la convergenza garantisce senza maggiorante |

Tabella del contratto (CONV-T7, Gate 8 §5, ATTACK-9 O7–O9):

| classe | strumenti |
|---|---|
| **(A)** | eliminazione C3-A1: **(A) condizionato a C3-A1** (PROVA SCRITTA); esattezza da C3-T6 e P4-T2. II-T7; P1-T4; P1-T2 in 𝔅; splitting commutativo; CONV-MZ1; Bézout su 𝕋 = **R4-T5[𝕋]** DIMOSTRATO (O22) |
| **(B)** | Dyson–Phillips (VAR-P11; (e) condizionato a verifica). **Magnus**: solo per generatori limitati in dimensione finita, oppure per troncamenti con ‖H_N‖·τ < π (VAR-T10(4), CON-FONTE Casas Thm 3.4; Moan–Niesen); in dimensione infinita sotto l'ipotesi di normalità di Casas in rappresentazione d'interazione A_I = e^{iH_0t}V e^{−iH_0t}; altrimenti Dyson. Per una PDE il Magnus (B) è quasi vuoto: nel troncamento ‖H_N‖ cresce con N. **Trotter–Kato/splitting**: (B) solo per V limitato (o relativamente limitato, con ipotesi dichiarate). Non ha una riga nel LEDGER e quindi non è un fondamento: richiesta al coordinatore (O8). CONV-T8 (Lie 1, Strang Θ(h^{5/4})); DICT-B2; CONV-T4; FAD-1 |
| **(C)** | completezza (scelta del livello R4); Magnus fuori dalle ipotesi, **in particolare Stark L8**, dove ∫‖A_I‖ = ∞; splitting/Trotter–Kato per V non limitato (VAR-T10(5)); γ_N non stimato; DM-δ sotto una soglia non nota; encoder con q stimato o di Darboux; E_int da dato approssimato |
| **(Lim)** | CONV-T1 senza maggiorante; R5/R-STOP; DICT-GR al crescere di n; I-LIM |

---

## §8 La pipeline: condizionamento e sottocatena certificata

```
CONDIZIONAMENTO (uscite discrete, fuori da CONV-T7, completezza (C))
  passo 1: modello ──► passo 2: livello n (budget, NON-DECISO) ──► passo 3: classe K, senso ID-*
                                         │
CORRETTEZZA CONDIZIONATA «al livello n, nella classe K» (CONV-T7 si applica)
  passo 4: misfit (A con inclusione, altrimenti B) / fit (B) / arresto (Lim)
        ──► passo 5: encoder (limitato a q dato: A/B con C_W²; altrimenti C)
        ──► passo 6: fattori, termini, E_int (A/B/C)
                                         │
  passo 7: etichetta doppia (completezza, correttezza) + bound Σ_i(∏_{j>i}L_j)ε_i
```

Che cosa promette all'utente. Ogni promessa è **condizionata al livello n e alla classe K dichiarati**; la completezza è (C) salvo dove indicato.

1. **M3-hol, DM3 con prova simbolica, M2⁺ modulo (AC):** `IDENTIFICATA[ID-ann | ID-res | ID-ker con (H-ex) | ID-fam]` nella classe dichiarata, con correttezza (A). Nei casi decidibili (P4-T6, OP-ALG-T1) anche la completezza è (A) modulo (AC).
2. **DM1 (EP):** solo `IDENTIFICATA[ID-ker, DM1]`, relativa a una classe finita (C3-T4, C3-T2(c,d)), correttezza (A). Mai ID-ann.
3. **DM3 con calcolo numerico:** misfit (A) con un'inclusione rigorosa, altrimenti (B); fit compatibile con bound (B) al livello fissato; mai «legge identificata» (DICT-A-iii).
4. **DM2:** `ID-LIM(n)`, contratto (Lim), nessun certificato (CONV-T1).
5. **DM-δ(Y):** moduli di continuità (VAR-P3, CONV-T4) e una soglia non certificabile (CONV-T5). La robustezza resta aperta.
6. **Bound della sottocatena 4 → 6:** d(x̃_k, x_k) ≤ Σ_i (∏_{j>i} L_j) ε_i, valido solo se ogni passo è (A) o (B).

Novità (ATTACK-8 O6): non i singoli passi, in buona parte noti, ma la composizione dei livelli L6–L10 sotto un unico contratto a due strati, insieme alle negative nuove (DICT-N1, DICT-A-iii, CONV-T2′, VAR-T1(c)-F, ENC-P0(b)). Il delta di SYS-EX su Ω non iniettivo **non** è dichiarato come novità finché Oberst 1993 non è letto per intero (O14).

---

## §9 Esempi da manuale (V-ex)

Gli script sono in `work/S9-ALG/sympy/`, eseguiti con `.venv\Scripts\python.exe -I`; l'uscita è salvata nei file `.out`. Sono verifiche, non prove. **Modelli: gli esempi 9.1–9.3 sono M3-hol/DM3 (forme chiuse non EP), non DM1** (O2).

### 9.1 L6 — Dirac 1+1 libero (`ex_L6_dirac.py`, 7/7 PASS)
Convenzione: iψ_t = Hψ, con H = −iσ_x∂_x + mσ_z, m = 1 ≠ 0 e base σ_x, σ_z fissata (H-DIRAC-1, H-DIRAC-2).
- (a) (i∂_t − H)(i∂_t + H) = −(τ² − ξ² + m²)I: ogni componente risolve Klein–Gordon.
- (b) ψ = (i∂_t + H)(f e_1), con f = J_0(m√(t² − x²)) soluzione KG non EP. ψ risolve Dirac; residuo numerico < 1e-20 a 40 cifre. Dato M3-hol; ψ_2 ∉ EP, quindi vale la premessa di **H-DIRAC-ann**.
- (c) **H-DIRAC-ker** nella classe hamiltoniana iψ_t = Aψ_x + Bψ, con 8 incognite. Con ψ di (b) il sistema puntuale ha rango 8 (σ_min ≈ 4,3e-2) e la legge vera (−iσ_x, mσ_z) lo risolve, quindi vale (H-ex). **Correzione (O5):** una sola onda piana dà rango 2, ma un dato EP con ≥ 4 modi generici dà già rango 8 e soluzione unica (ATTACK-9 §3(A)). Il fallimento di ID-ker dipende dal numero di modi, non dall'essere EP; il criterio ψ_2 ∉ EP riguarda ID-ann.

### 9.2 L7 — Pöschl–Teller (`ex_L7_poschl_teller.py`, 11/11 PASS)
q = −2 sech²x, u = e^{it} sech x + e^{−ik²t}(ik − tanh x)e^{ikx} con k = 3/2. Dato M3-hol.
- (a) Il residuo restituisce V = q: **ID-res** in DM3 (VAR-T1(b)). **Non ID-ann (O12):** il dato ha annullatore (L_q + 1)(L_q − k²), già nel sottoanello ℂ[∂_t, L_q], e (i∂_t + 1)(i∂_t − k²) (ATTACK-9 §3(D)). Nell'anello degli operatori il dato non identifica i∂_t − L_q in senso ID-ann; vale solo ID-res.
- (b) DM-φ: il residuo di e^{iφ}u_b è q − φ′(t), quindi solo **ID-fam** (VAR-P4).
- (c) Traduzione **di Darboux** A = ∂ + tanh x, con A L_q = L_0 A e ker A = ℂ sech x. Au risolve Schrödinger libero; A u_b = 0 (il modo legato si perde); A u_s è un'onda piana, cioè un dato EP. A non è limitato e C_W non si applica: è il caso (C) del passo 5 (ENC-K1′, O7), non un esempio della traduzione limitata.
- (d) A⁺A = L_q + 1 e AA⁺ = L_0 + 1.

### 9.3 L8 — Stark dipendente dal tempo, Avron–Herbst (`ex_L8_stark.py`, 5/5 PASS)
V = β(t)x con β = t. Si pone u = e^{i(−Bx + g)}w(t, x − s), con B = t²/2, s = −t³/3, g = −t⁵/20 e w gaussiana libera. Dato M3-hol.
- u risolve l'equazione con V = tx: residuo esatto via la derivata logaritmica, controllo diretto < 1e-30.
- u non ha zeri, quindi int Z(u) = ∅ e **ID-res** di V(t,x) (VAR-T1(c)).
- DM-φ: il residuo diventa tx − φ′(t), quindi V solo modulo funzioni di t (ID-fam, (E2) con c(t)).
- Contratto: (A) per la trasformazione di Avron–Herbst (VAR-T10(1), Stark globale). **Magnus qui è (C)**, perché ∫‖A_I‖ = ∞ (O9).

### 9.4 L9 — non locale indistinguibile (`ex_L9_L10_dict.py`, parte L9)
u = e^{−t}e^{ix} + e^{−2t}e^{2ix} soddisfa sia u_t = −|D|u sia la legge locale u_t = iu_x. **L'esempio è banale (O28):** ogni dato con un numero finito di modi soddisfa una legge locale per interpolazione dei simboli (ATTACK-9 §3(E)), quindi l'indistinguibilità non dipende da CONV-T6. CONV-T6 dà il fenomeno non banale (dato a spettro continuo con a algebrica). Un esempio L9 a infiniti modi che identifichi un atomo non locale manca (§11).

### 9.5 L10 — dizionario sul calore (`ex_L9_L10_dict.py`, 12/12 PASS insieme a L9)
u = (t+1)^{−1/2}e^{−x²/(4(t+1))} su Ω = (0,1) × (−1,1), Y = L²(Ω), D_0 = ∂_t, quadrature mpmath a 25 cifre (precisione di lavoro, O10).
- (a) Livello affine 1 (atomi 1, ∂_x): r_1 = 0,0778 > 0. Il valore è calcolato sia come rapporto di Gram (MF2) sia come residuo diretto di minimi quadrati, e i due coincidono (a′). È un **misfit (B)**: quadratura senza inclusione rigorosa. (A) richiederebbe un'inclusione (O10).
- (b) Livello 2 (atomi 1, ∂_x, ∂_x², ∂_t∂_x, ∂_t²): r_2 ≈ 4e-33 come residuo diretto, minimizzatore ∂_t − ∂_x². La Gram omogenea ha un solo autovalore nullo (1,25e-28; il successivo è 1,71e-4). Uscita: `FIT-COMPATIBILE(2, r_2, bound B2)`, **non** «identificata» (DICT-A-iii).
- (c) CONV-T4(a) con la perturbazione ε cos 3x:
  - ε = 1e-3: ρ = 0,01309, δ = 0,00936, 2δ/ρ = 1,43 > 1. **Caso vacuo** (O15), perché sin ≤ 1 sempre.
  - (c′) ε = 1e-4: δ = 9,36e-4, sin = 4,93e-3 ≤ 2δ/ρ = 0,143 < 1. Il bound è non banale e vale.
- (d) (H-ex): u = t + sin x nella classe u_t = a u_xx + b u dà ker Φ_u = 0, ma **nessuna legge** esiste. ID-ker senza (H-ex) non identifica (DICT-RANGO).

---

## §10 Tabella «claim usati → stato»

| claim | stato (Gate 8 prevalente) | passo |
|---|---|---|
| C3-P1[M2], P4-T5, CONV-T1, C3-T3 (solo EP), C3-T2(c,d), P4-T2 | DIMOSTRATO | 1 |
| P4-T6, OP-ALG-T1 | DIMOSTRATO modulo (AC) | 1 (M2⁺, M3-hol) |
| VAR-P4 | DIMOSTRATO | 1 |
| G-T2 | DIMOSTRATO, CON-FONTE in sostanza | 1 |
| VAR-P3 | DIMOSTRATO come stima di modulo, non certificato di robustezza | 1, 3c (DM-δ) |
| DICT-N2, DICT-N3, DICT-RIT1, DICT-N1iii, DICT-N1v, CONV-T2′ | DIMOSTRATO | 2 |
| II-C1 = C3-T1(d), R4-T5[ℝ], C3-T6, C3-T4 (ID-ker relativa), S4ID-T1, S4ID-P1, CONV-MZ1, CONV-MZ2 | DIMOSTRATO | 3a |
| C3-A1 | PROVA SCRITTA, non auditata, senza riga LEDGER → «(A) condizionato» | 3a, 7 |
| SYS-EX | Ω arbitrario DIMOSTRATO; ℝ^n NOTO (Oberst 1993, abstract); convesso PROBABILMENTE NOTO; novità condizionata a CIT Oberst 1993 | 3b |
| SYS-N1, SYS-T0 | NOTO (SYS-N1 DIMOSTRATO su Ω arbitrario) | 3b |
| SYS-C1, SYS-S1(i⇒)(i⇐)(ii), H-DIRAC (ann e ker, sotto H-DIRAC-1/2, m ≠ 0), SYS-N3, DICT-MAG-NU | DIMOSTRATO | 3b |
| LAME-3 | DIMOSTRATO con ρ, μ ≠ 0, λ + μ ≠ 0, λ + 2μ ≠ 0 | 3b |
| SYS-S1-C | FALSO | 3b (fallimento) |
| VAR-N1, VAR-T1(a)(b)(c)(i)–(iii), VAR-P5, VAR-T2a, VAR-E1, VAR-C3Q2(a)–(g), VAR-L2, DICT-RANGO, DICT-RANGO-cor (ID-ker, (H-ex)) | DIMOSTRATO | 3c, 4 |
| VAR-T6 | CON-FONTE da verificare → condizionato | 3c |
| VAR-T1(c)-F, DICT-N1vi | FALSO | 3c (fallimento) |
| VAR-T1(c)-Q10 | APERTO | 3c |
| VAR-L2-cor | CON-FONTE (eredita VAR-P11(e)); **non usato** (O17) | — |
| DICT-MF, DICT-A, DICT-A-iii, DICT-B2, DICT-R3, DICT-GR, DICT-ILIM-H0, DICT-N1 (i)(ii)(iv)(a), DICT-N1iv-bc | DIMOSTRATO | 4, 7 |
| DICT-ILIM | DIMOSTRATO; ramo (H2) con Whitney–Stein da verificare → condizionato | 4 |
| DICT-B3 | CON-FONTE da verificare → condizionato | 4 |
| DICT-ILIM-Hs | CANDIDATO | 4 |
| CONV-T2, T3, T4, T5, T6 | DIMOSTRATO | 4, 7 |
| CONV-T8 | DIMOSTRATO in L² (L^∞: V-ex) | 7 |
| CONV-T7 | proposizione DIMOSTRATO; Magnus (B) condizionato; applicato solo alla sottocatena 4 → 6 | 7 |
| CONV-R1-F, CONV-MZ3-F | FALSO | 7 (fallimento) |
| ENC-1, ENC-U1, ENC-C1, ENC-T2, ENC-K0, ENC-K1′, FAD-1, NS-EQ-Ω | DIMOSTRATO | 5 |
| ENC-P0(b)^cl; ENC-P0(b)^loc (versione corretta) | DIMOSTRATO (^loc FALSO come scritto) | 5 |
| ENC-P0′ (astratto, nucleo denso); ENC-P0′-DIC (esistenziale); POLE-N^cl | DIMOSTRATO (P0′-DIC FALSO per un rappresentante arbitrario) | 5 |
| ENC-T2(c′) | osservazione in C^∞ DIMOSTRATO; FALSO con vincolo di grado; APERTO nella classe principale | 5 |
| ENC-N1 / ENC-N1′ | FALSO / DIMOSTRATO solo come lemma di riduzione | 5 |
| FW-1 | DIMOSTRATO per il libero; con V CON-FONTE → condizionato | 5 |
| DICT-R6 (a)–(f) | DIMOSTRATO | 5 |
| C12-T1, C12-T1′, C12-P7, C12-P10, OPF-T4, II-T2, P1-T2, OPF-L1/T1/L2/T2/P3/P4/C1, P1-T3, P1-T5, SYS-E1–E3, VAR-P9, Lemma J, S4T-T1, S4T-L0, S4T-L1, S4T-T2, S4T-P3, P2-T4, CONV-D1, CONV-B1, OPA-T3(a–d) | DIMOSTRATO | 6 |
| S4T-L2, S4T-T3 (i, ii, v, vi, vii) | DIMOSTRATO mod [F1] (CON-FONTE da verificare) → condizionato | 6 |
| OPF5B-T1 | DIMOSTRATO mod F1, F2 CON-FONTE verificate | 6 |
| ENC-A9(b) | (b1), (b2), (b4) DIMOSTRATO; (b3) CON-FONTE + V-ex | 6 |
| C12-C1; P1-P1(e) = R5-T2[H^m] | FALSO | 6 (fallimento) |
| II-T7, R4-T5[𝕋] | DIMOSTRATO | 7 |
| P1-T4 | DIMOSTRATO; Lie CON-FONTE (Humphreys), verifica non registrata → condizionato | 7 |
| VAR-P8(a); VAR-P8(b) | DIMOSTRATO; «⟹» DIMOSTRATO, «⟸» CON-FONTE (Wei–Norman: metadati verificati, contenuto da fonti secondarie) → condizionato | 7 |
| VAR-P11 | (a)–(d) DIMOSTRATO; (e) CON-FONTE (Pazy) → condizionato | 7 |
| VAR-T10 | (1), (3)(i)–(ii) DIMOSTRATO; (3)(iii) CON-FONTE + V-ex; (2), (4), (5) CON-FONTE | 7, 9.3 |
| VAR-P12 | (a)–(c) DIMOSTRATO; (d) APERTO | 7 |
| Trotter–Kato | **nessuna riga LEDGER**: non è un fondamento; richiesta al coordinatore | 7 |
| esempi §9.1–9.5 | V-ex | 9 |

**Citazioni da chiudere** perché i passi «condizionati a verifica» diventino fondati (O6): vdPS Prop. 1.34/Thm 1.27 (VAR-T6); DICT-B3; Whitney–Stein (DICT-ILIM, (H2)); Pazy cap. 5 (VAR-P11(e), VAR-L2-cor); Thaller cap. 5 (FW-1 con V); Lax–Oleinik = Kružkov [F1] (S4T-T3); Humphreys §4.1 Cor. B (P1-T4); Wei–Norman 1964, contenuto (VAR-P8(b) «⟸»); Casas 2007 Thm 3.4 (VAR-T10(4)); Oberst 1993, testo pieno (novità di SYS-EX).

---

## §11 Domande aperte

Elenco completo, con motivazione e rinvii, in `work/S9-ALG/open_questions.md`. In sintesi:
1. Robustezza in DM-δ(Y) (VAR-Q19, ATTACK-8 O8).
2. Un esempio L9 a infiniti modi con un atomo non locale identificato; DICT-A(iii) per atomi non locali (DICT Q4).
3. DICT-ILIM-Hs, CANDIDATO.
4. CONV-Q1: G_u nel limite senza maggiorante.
5. VAR-T1(c)-Q10.
6. C3-Q2 in generale.
7. CONV-Q9: V illimitato.
8. Costo di R1 per livello; audit di C3-A1; inclusione rigorosa per il misfit (A).
9. R6 in H^{2k} e con la forma debole MF3; un bound di ‖W_q‖ più stretto di C_W.
10. Costante di Lipschitz esplicita di q ↦ W_q (ENC-1), per il passo 5 con q stimato.
11. ENC-T2(c′) nella classe principale; VAR-P12(d); II-T2(b′) e Maxwell (Q6).
12. Riga LEDGER per Trotter–Kato; chiusura delle citazioni elencate nel §10.

---
## Errata di Fase 10 (coordinatore, 27/10/2026; da S10-INT, ESEMPI.md §7; NOTAZIONE v7)
- §0.3 e §9.2: il dato di Pöschl–Teller è **DM3**, non M3-hol (sech x non è D-finita su ℂ(x)). Nessun valore di verità cambia.
- §0.5: nuova uscita **`COMPATIBILI(θ_0 + ker Φ_u)`** (o `COMPATIBILI(𝒞_u)` per classi non lineari) per un dato esatto con più leggi compatibili; `NON-DECISO` resta per il budget n_max esaurito o per l'indecidibilità.
- ID-ker solo per classi lineari nei parametri; per FRAC e simili si usa l'unicità del compatibile (NOTAZIONE v7 punto 1).
- §3b e §6, Maxwell: va dichiarata la classe (simmetrica, oppure modulo i vincoli). Nella classe hamiltoniana generale ID-ker è impossibile (EX10-e-K).
- §9.3, oscillatore: il passaggio di cos t = 0 tramite la parità è V-ex, non un fondamento.
- Esempi da manuale della Fase 10 (Dirac libero, oscillatore armonico, Pöschl–Teller, calore frazionario, Maxwell nel vuoto): `work/S10-INT/ESEMPI.md`, script 80/80 PASS.
