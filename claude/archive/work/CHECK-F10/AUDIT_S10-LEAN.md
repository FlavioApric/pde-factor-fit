# AUDIT S10-LEAN — revisione indipendente della formalizzazione Lean (Fase 10)

Revisore: S-CHECK-LEAN, 27/10/2026. Materiale esaminato: progetto `C:\Users\<user>\PBLean` (moduli `PBLean/F10/*.lean`), copia `D:\ProblemaBase\PBLean_src\F10\`, `work/S10-LEAN/FORMAL_MAP.md`, `work/S10-LEAN/BUILD_LOG.md`, `claims/LEDGER.md` (Fase 8 e Fase 10), `work/S8-SYS/PROOF_PACKAGE.md` (§§2, 3, 5, 6, 7) e `work/S8-DICT/PROOF_PACKAGE.md` (§§0, 2.1, 2.3, 3.5). Nessun sorgente è stato modificato e nessuno script di `_vendor` è stato eseguito.

**Esito complessivo.** Build pulita, nessun `sorry`, nessun assioma estraneo, sorgenti identici alla copia. Delle 37 voci della mappa: 27 FEDELE, 7 PIÙ DEBOLE, 3 PIÙ FORTE/DIVERSO, 0 VACUO. Non ho trovato ipotesi contraddittorie né definizioni che rendano tautologico un enunciato in modo nascosto. I problemi riguardano la mappa più che il codice: tre voci sono etichettate «piena» o associate a un claim che non formalizzano (§4).

## 1. Build e assiomi

`lake build` in `C:\Users\<user>\PBLean`: **Build completed successfully (9064 jobs)**, codice d'uscita 0. I moduli F10 risultavano già compilati e `lake` li ha ripresi dalla cache («Replayed»). Per non fidarmi della cache ho rielaborato ogni file da sorgente con `lake env lean PBLean/F10/<file>.lean`, nell'ordine Comax, Morita, Dirac, Gauge, Filtration, SmithT0, BaireN1, Axioms. Tutti e otto i file terminano con codice 0, senza errori. La rielaborazione di `Axioms.lean` ristampa le stesse 85 righe di assiomi.

Gli avvisi sono solo di stile: righe oltre 100 caratteri, argomenti `simp` inutilizzati, variabili di sezione incluse ma inutilizzate (`Fintype`, `DecidableEq`), e l'avviso sull'import di `Mathlib` intero. Non ci sono errori né avvisi «declaration uses 'sorry'».

Ricerca nei sorgenti (tutto `PBLean/`, non solo F10) delle parole `sorry`, `admit` e `axiom`, e in F10 anche di `opaque`, `unsafe`, `implemented_by`, `extern`, `native_decide` e `set_option`: nessuna occorrenza, a parte i comandi `#print axioms`. Non ci sono istanze dichiarate a mano.

`#print axioms`: l'output della build contiene 85 righe per dichiarazioni `PBLean.F10.*`. Ognuna dà `[propext, Classical.choice, Quot.sound]` oppure `[propext, Quot.sound]`; nessuna dipende da `sorryAx` o da altri assiomi. Il controllo copre tutte le dichiarazioni dei sette moduli tranne `Comax.mem_Sol`, che è `Iff.rfl` e quindi irrilevante. Le righe coincidono con quelle trascritte in `BUILD_LOG.md`.

## 2. Corrispondenza dei sorgenti

Gli otto file di `D:\ProblemaBase\PBLean_src\F10\` (Axioms, BaireN1, Comax, Dirac, Filtration, Gauge, Morita, SmithT0) sono identici byte per byte (`cmp`) a quelli di `C:\Users\<user>\PBLean\PBLean\F10\`, cioè ai file compilati. `PBLean.lean` importa tutti e otto i moduli F10, quindi la build li comprende.

## 3. Tabella voce → verdetto

Legenda: **FEDELE** = l'enunciato Lean dice quanto il claim, nella parte che la mappa dichiara (anche quando è più generale); **PIÙ DEBOLE** = manca una parte di ciò che la mappa associa alla voce; **PIÙ FORTE/DIVERSO** = enunciato senza riga corrispondente nel LEDGER, oppure con ipotesi diverse; **VACUO** = ipotesi contraddittorie o enunciato tautologico.

| # | voce Lean | ID LEDGER (dalla mappa) | verdetto | motivazione |
|---|---|---|---|---|
| 1 | `Morita.matEnd` | quadro SYS | FEDELE | omomorfismo di anelli `Mat_k(R) → End_R(M^k)`, verificato su 1, prodotto, 0 e somma |
| 2 | `Morita.rowSpan_le_ker_iff` | quadro SYS | FEDELE | `U_P ≤ ker φ_u ⟺ Pu = 0`; `rowSpan` è lo span delle righe, cioè `R^{1×ℓ}P` |
| 3 | `Morita.malgrange` | quadro SYS (Sol ≅ Hom(M_P, 𝒜)) | FEDELE | isomorfismo `R`-lineare `ker(matOp P) ≃ Hom_R(R^k/U_P, M)` per ogni `R`-modulo `M`, che è esattamente il quadro astratto usato dal progetto |
| 4 | `Morita.det_smul_eq_zero_of_mem_Sol` | SYS-C1 (passo det), CONV-MZ1 | FEDELE | CONV-MZ1 senza l'ipotesi `det D ≠ 0`, che non serve: più generale. Per SYS-C1 copre solo il passo `(det P) ⊆ Ann`; Koszul, Auslander–Buchsbaum e Fitting restano fuori, come dichiarato |
| 5 | `Morita.end_kernel_decomposition` | «II-T3 per sistemi» | PIÙ FORTE/DIVERSO | non esiste una riga LEDGER «II-T3 per sistemi». Le ipotesi `bT₁ = T₁b` e `aT₂ = T₂a` sono aggiunte: soddisfacibili (per esempio con endomorfismi scalari, dove si ritrova II-T3 [Lean] della r. 103), ma restrittive. Risultato corretto e non vacuo |
| 6 | `Morita.matrix_kernel_decomposition` | idem | PIÙ FORTE/DIVERSO | come la voce 5. Il proiettore (identità su `Sol P₁`, nullo su `Sol P₂`) è nella voce 5 ma non è riesportato qui |
| 7 | `Morita.sol_split_of_det` | nessuna riga («bersaglio 5») | PIÙ FORTE/DIVERSO | enunciato nuovo, corretto e senza ipotesi di non singolarità. La mappa lo dichiara correttamente come nuovo |
| 8 | `Dirac.clifford_sq` | H-DIRAC (premessa), SYS-E1 | FEDELE (H-DIRAC) | Clifford in forma diagonale ⇒ `(Σ p_μγ_μ)² = (Σ η_μ p_μ²)·1`. **SYS-E1 non c'entra**: SYS-E1 riguarda l'indipendenza lineare di `X, ad_X^k Y` per Dirac 1+1, e nessun teorema Lean la tocca (§4.1) |
| 9 | `Dirac.massive_factor` | H-DIRAC | FEDELE | identità d'anello banale |
| 10 | `Dirac.scalar_sub_mul_add` | H-DIRAC | FEDELE | identità d'anello banale |
| 11 | `Dirac.pauli_sq`, `pauli_anticomm` | H-DIRAC | FEDELE | le matrici `σ₁, σ₂, σ₃` sono definite correttamente |
| 12 | `Dirac.XY_eq_KG` | H-DIRAC (C1) | FEDELE | `XY = YX = KG·I₂` in `Mat₂(ℂ[p₀,…,p₃])`, con `X = p₀ − σ·p`, `Y = p₀ + σ·p` come in PROOF_PACKAGE §7 |
| 13 | `Dirac.diracChiral_sq` | Dirac² = KG | FEDELE | `diracChiral` è **definito** come `[[0, X], [Y, 0]]`, non ricavato da matrici γ esplicite. La forma coincide con `γ^μ p_μ` chirale, con `p_μ` a indice basso (controllato a mano), ed è la stessa del PROOF_PACKAGE (`D = diracChiral − m`) |
| 14 | `Dirac.dirac_massive` | H-DIRAC(a) (premessa) | FEDELE | è la premessa; H-DIRAC(a) vero e proprio (`M_D ≅ (R/q)²`, `q` primo) non è formalizzato, e la nota della mappa lo dice |
| 15 | `Dirac.antidiag_sq` | H-DIRAC(d) (lemma) | FEDELE | lemma di calcolo |
| 16 | `Dirac.dirac2_sq` | H-DIRAC(d) (1+1), portata «piena» | PIÙ DEBOLE | H-DIRAC(d) afferma `M_{D₂} ≅ R/q` e «ψ identifica ⟺ ψ₂ ∉ EP». Lean prova solo `[[0, p₀−p₁], [p₀+p₁, 0]]² = (p₀² − p₁²)·I₂`, nel caso senza massa. «Piena» è un'etichetta sbagliata |
| 17 | `Gauge.nabla_covariant` | G-L0 | FEDELE | `∇^{a′}(gu) = g∇^a u` con `a′ = a + g⁻¹∂g`. La convenzione `a = iA` è coerente con `A′ = A + (1/i)g⁻¹dg` |
| 18 | `Gauge.op_covariant` | G-L0 | FEDELE (più generale) | vale per ogni polinomio non commutativo nelle `∇_μ` e in operatori `K`-lineari `V_i` qualsiasi, che comprendono potenziali e matrici costanti, con `g ∈ Kˣ` qualsiasi |
| 19 | `Gauge.sol_gauge` | G-L0, G-T2(b) | FEDELE | `L_A u = 0 ⟺ L_{A′}(gu) = 0` |
| 20 | `Gauge.invariant_data_gauge` | G-T2(b) | FEDELE | traduce alla lettera la prova (b) del PROOF_PACKAGE §6. Contenuto minimo: la tesi è la congiunzione di `sol_gauge` e dell'ipotesi `hO` riscritta. La «procedura di ricostruzione» non è modellata, ma segue in una riga. Non vacuo |
| 21 | `Gauge.gauge_fixing_u_trivial` | SYS-N3(c), ultima frase | FEDELE | `gu = u` con `u_j` non divisore di zero ⇒ `g = 1`. Una `u` senza zeri in `C^∞` soddisfa l'ipotesi, quindi l'enunciato è più generale. Il resto di SYS-N3 è fuori portata, come dichiarato |
| 22 | `Filtration.kernelAt_mono` | DICT §0 | FEDELE | banale |
| 23 | `Filtration.kernelAt_compat` | DICT §0 | FEDELE | banale |
| 24 | `Filtration.iSup_kernelAt` | DICT §0 | FEDELE | usa la direzionalità dei `V_n` |
| 25 | `Filtration.not_fit_iff` | DICT §0 (misfit) | FEDELE (nota) | `Fit` è definito su **operatori** (`c ∈ V_n`, `c ≠ 0`), mentre DICT §0 lo definisce su **vettori di coefficienti** (`c ∈ ℂ^{N_n}`, `Σ c_iD_iu = 0`). Le due nozioni coincidono se gli atomi di `𝓓_n` sono linearmente indipendenti, come nel caso a coefficienti costanti (`∂^α`). Con atomi dipendenti la definizione del LEDGER dà fit banali; quella Lean è la più sensata (§4.3) |
| 26 | `Filtration.fit_mono` | DICT-GR (livelli) | FEDELE | banale |
| 27 | `Filtration.finrank_le_kernelAt_add` | DICT-N1iii (passo di rango) | PIÙ DEBOLE | è solo rango più nullità. DICT-N1iii (inclusione stretta `Ann(u) ∩ R_{≤n} ⊋ (L) ∩ R_{≤n}` per `N ≥ 2`) richiede anche i conteggi binomiali e `dim((L) ∩ R_{≤n})`, che mancano. Dichiarato «parte» |
| 28 | `Filtration.Rle_mono`, `iSup_Rle`, `mul_mem_Rle` | DICT §0 | FEDELE | `Rle` è `restrictTotalDegree` di Mathlib |
| 29 | `Filtration.iSup_kernelAt_Rle` | DICT §0 / C3-L1 | FEDELE | `ker(evAt u)`, visto come `𝕜`-sottospazio, è `Ann(u)` |
| 30 | `Filtration.consequences_le_kernelAt` | DICT-GR (b), R2 | FEDELE | `Lu = 0 ⇒ (L) ∩ R_{≤n} ⊆ Ann(u) ∩ R_{≤n}`, cioè «si ha sempre ⟨L⟩_n ⊂ nucleo» a coefficienti costanti. Il resto del teorema G-R non è coperto |
| 31 | `Filtration.finrank_Rle_le` | DICT-N1iii (passo di rango) | PIÙ DEBOLE | come la voce 27. L'istanza `[FiniteDimensional 𝕜 (Rle n)]` è un'ipotesi esplicita, soddisfacibile e derivabile per `σ` finito: non svuota l'enunciato |
| 32 | `Comax.Sol_sup` | SYS-S1(ii), prima parte | FEDELE | `Sol(U₁ + U₂) = Sol(U₁) ∩ Sol(U₂)`, cioè `Sol(Q₁) ∩ Sol(Q₂) = Sol(N)`. La parte su dimensione e lunghezza di SYS-S1(ii) non è coperta, come dichiarato |
| 33 | `Comax.Sol_inf_of_sup_eq_top` | SYS-S1(i⇐) con `N = 0` | PIÙ DEBOLE | è solo il caso `N = 0`, dove `Ext¹(N, 𝒜) = 0` è banale. Il caso di contenuto (`N` di lunghezza finita, `H¹_dR = 0`) manca. Dichiarato «caso»; enunciato corretto e non vacuo |
| 34 | `Comax.scalar_case` | II-T3 (ponte), portata «piena» | PIÙ DEBOLE | prova solo i fatti sugli ideali (`(P₁) + (P₂) = R`, `(P₁) ∩ (P₂) = (P₁P₂)`). Il ponte annunciato («il caso `k = 1` di `Sol_inf_of_sup_eq_top` è II-T3») richiede `Hom_R(R/(P), 𝒜) ≅ ker P` su `𝒜`, che non è enunciato da nessuna parte. «Piena» è eccessivo |
| 35 | `SmithT0.socle_le_one_iff` | SYS-T0 (passo finale) | PIÙ DEBOLE | è solo il passo polinomiale finale (corretto, «unità» invece di «= 1», cioè a meno di associati). Mancano Smith, gli zoccoli (`rootCount` è solo un conteggio di radici) e i minori. Dichiarato «parte» |
| 36 | `BaireN1.isMeagre_iUnion_compact` | DICT-N1(i) | PIÙ DEBOLE | solo il caso normato. Gli spazi del claim (`C^∞(Ω)`, `S^m`, F-spazi non normati) sono esclusi; mancano anche i traslati affini e le immagini continue di σ-compatti, banali. `E` non è supposto completo: l'enunciato resta vero ma, senza Baire, «magro» può valere per tutto lo spazio |
| 37 | `BaireN1.interior_eq_empty_of_isCompact` | DICT-N1(i) (lemma) | FEDELE | Riesz nel caso normato |

**Conteggio.** FEDELE 27 (voci 1–4, 8–15, 17–26, 28–30, 32, 37); PIÙ DEBOLE 7 (16, 27, 31, 33, 34, 35, 36); PIÙ FORTE/DIVERSO 3 (5, 6, 7); VACUO 0.

## 4. Problemi segnalati

### 4.1 Mappatura sbagliata o etichette di portata eccessive
- **SYS-E1 associato a `clifford_sq` (voce 8).** SYS-E1 dice che `X, Y, ad_X^k Y` sono linearmente indipendenti su `ℂ` (Dirac 1+1, `X = iξσ_z`, `Y = −iσ_x`), e di qui segue P1-T5. Nessun teorema Lean ne parla. SYS-E1 va tolto dalla colonna ID oppure spostato tra i claim non formalizzati.
- **`dirac2_sq` con portata «piena» per H-DIRAC(d) (voce 16).** È soltanto l'identità del quadrato nel caso senza massa; l'isomorfismo `M_{D₂} ≅ R/q` e il criterio `ψ₂ ∉ EP` non sono formalizzati. La portata va corretta in «parte (premessa)».
- **`scalar_case` con portata «piena» per il ponte II-T3 (voce 34).** Manca un teorema che colleghi `Comax.Sol` su `L = R` con `ker P ⊆ 𝒜`; la conclusione «è II-T3» sta solo nel commento. Basterebbe un corollario che componga `Sol_inf_of_sup_eq_top`, `scalar_case` e l'isomorfismo `Hom_R(R, 𝒜) ≅ 𝒜`.

### 4.2 Ipotesi aggiunte
- Voci 5 e 6: le commutazioni `BP₁ = P₁B` e `AP₂ = P₂A` non stanno in II-T3, che è scalare, e non c'è una riga LEDGER per sistemi con cui confrontarle. Non svuotano il risultato: valgono nel caso scalare e, per esempio, per matrici diagonali o polinomi in una matrice fissata. Escludono però le identità di Bézout matriciali generiche. Il risultato va registrato come estensione condizionata, non come «II-T3 per sistemi».
- Voce 31: l'istanza `[FiniteDimensional 𝕜 (Rle n)]` è un'ipotesi, ma è vera per un numero finito di variabili. Non è un problema.
- Nessun'altra voce ha ipotesi contraddittorie. Ho controllato in particolare che le ipotesi di `socle_le_one_iff`, `end_kernel_decomposition`, `sol_split_of_det`, `Sol_inf_of_sup_eq_top` e `gauge_fixing_u_trivial` siano soddisfacibili con istanze non banali.

### 4.3 Definizioni da tenere d'occhio
- `Filtration.Fit` (voce 25): la nozione Lean di fit è sugli operatori, quella del LEDGER (DICT §0) sui vettori di coefficienti. Le due coincidono solo con atomi linearmente indipendenti. Non è un errore del codice; semmai il testo di DICT §0 andrebbe precisato («c ≠ 0 come operatore», oppure «atomi indipendenti»).
- `Dirac.diracChiral` (voce 13): definito direttamente in forma a blocchi. È corretto, ma Lean non verifica che coincida con `Σ γ^μ p_μ` per matrici γ chirali esplicite. Il rischio è basso: la forma è standard e coincide con il PROOF_PACKAGE.
- `Gauge.invariant_data_gauge` (voce 20): non è vacuo, ma il suo contenuto è `sol_gauge` più l'ipotesi riscritta. Non va presentato come una formalizzazione sostanziale di G-T2(b) oltre la parte algebrica.
- `Gauge`: `gaugeTransform` usa `a = iA` e `∇ = ∂ − a`; ho controllato che coincida con `A′ = A + (1/i)g⁻¹dg` e con G-L0 (`g = e^{iχ}`, `a′ = iA + i∂χ`).

### 4.4 Varie
- La sezione «Fase 10» del LEDGER non contiene ancora righe S10-LEAN (contiene solo F10-A). Il confronto è stato fatto con le righe di Fase 8 e con i PROOF_PACKAGE.
- `BUILD_LOG.md` è corretto, ma va precisato che la build del 27/10 ripresa dalla cache non ricompila i moduli. La rielaborazione da sorgente di questo audit conferma l'esito.
