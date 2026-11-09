# AUDIT_S10-OPEN-C — S-CHECK-F10-C (27/10/2026)

Revisore: S-CHECK-F10-C, indipendente da S10-OPEN-C. Ho letto per intero `work/S10-OPEN-C/` (PROOF_PACKAGE §1–17, CHECK_REQUEST D1–D39, LEDGER_ROWS, open_questions OC-1…OC-11, `sympy/s10openc_checks.py`) e, come contesto, NOTAZIONE.md v6, claims/LEDGER.md sezione «Fase 8» (righe 197–336), le domande originali in `work/S8-VAR/open_questions.md`, `work/S8-SYS/open_questions.md`, `work/S8-ENC/open_questions.md`, `work/S8-DICT/open_questions.md`, e le sedi citate: S8-VAR PP §1.3 (riga 72, uso di P11(e) in L2-cor), §1.6 (VAR-P3), §4.4 (VAR-P12), riga 300 (stima di Cauchy con θ = 1/10); S8-ENC PP §5 (definizioni di (C), (S), ENC-N1′); S8-DICT PP righe 317–327 (I-LIM). Non ho eseguito nessuno script di `_vendor`.

**Verifiche SymPy indipendenti.** Gli script sono miei, stanno in `work/CHECK-F10/sympy/c_*.py` (output nei `.out` omonimi) e sono stati eseguiti con `.venv\Scripts\python.exe -I`:

| script | esito | contenuto |
|---|---|---|
| `c_semigroup.py` | 9/9 | Lemma C in dimensione finita; equazione mite di §2 componente per componente; antiaggiunzione e norma di B su un modello finito; x ∉ D(d/dθ) su L²(𝕋); gauge di §4; formula delle medie con il termine di bordo |
| `c_q10.py` | 14/14 | i due sup di §3 in forma chiusa; Re(1+ζ)^{−2} ≥ 1/2 per \|ζ\| ≤ 1/10; stima di Cauchy di g_0^{(k)} per k ≤ 8; e^{−ℓ^{−4}/2} ≤ ℓ; Leibniz; (k+j)! ≤ 2^{k+j}k!j!; residuo di Tychonoff all'ordine 9; piattezza dei g_j |
| `c_p12.py` | 10/10 | commutatori di Heisenberg; M = diag(−1/5, −5) con ordine dei fattori controllato; 300 Ξ casuali in sl₂; M² = e^Ξ; due regolarizzazioni lisce di ω (tr = −4.81 e −5.13) |
| `c_c3q2_dirac.py` | 13/13 | f^{(k)}/f = polinomio di Touchard monico in e^y (prova elementare della non D-finitezza); divisione per L monico; serie g_1, g_2 con un metodo diverso; ZXZ con residuo ~10^{−31}; asintotica ξ\|G(ξ)\| → m²t/2; Lemma E numerico |
| `c_sys_enc.py` | 20/20 | §8 con basi saturate (metodo diverso da B(A)/B(ξ)) e controesempio rafforzato (stessa matrice A(ξ_0)); §9 nucleo sinistro, criterio di Buchsbaum–Eisenbud; §10 identità P(∂_t, L_q)(e^{αt}f); §11 composizione di Volterra simmetrici e stima ‖𝒱^n‖ discretizzata, passo 2 |
| `c_darboux.py` | 9/9 | §12 in generale (u, φ libere qualsiasi): segno, formula di κ via Wronskiano, residuo di 1/u; esempio **reale** dipendente da t (boost di Galileo) |
| `c_dict.py` | 16/16 | esponenti di §13 e nitidezza per scaling; resto di Taylor; rapporto di interpolazione costante (0.35) su bump che si restringono; §14 polinomio nodale, costanti, e la stima (ii) su un nucleo diverso (t^{−1/2}); §15; §16 |
| `c_dmdelta.py` | 10/10 | §17: scala del bump, salto di V in x_0, margine D39, famiglia sinusoidale |

Totale 101/101. Ho anche rieseguito lo script del pacchetto: 34/34 OK. Nessuna prova del verdetto si appoggia sul solo calcolo.

**Criterio di stato.** Propongo DIMOSTRATO solo se il verdetto è PASS o i fix sono redazionali (dicitura, refusi, una riga standard, un'ipotesi di non degenerazione). Se un fix ripara un passo intermedio falso, oppure aggiunge un passo che il pacchetto aveva delegato al calcolo, propongo PROVA SCRITTA; la promozione a DIMOSTRATO va fatta dopo il recepimento, rileggendo il testo. «APERTO — ridotto a X» lo accetto solo se l'implicazione «X ⇒ claim» è provata.

## 1. Tabella claim → verdetto → stato → fix

| claim | § | verdetto | stato proposto | fix |
|---|---|---|---|---|
| VAR-P11(e) | 1 | PASS | **DIMOSTRATO** | C-1 (redazionale) |
| VAR-L2-cor | 1 | PASS (catena verificata: S8-VAR PP riga 72 usa solo B ∈ C¹(𝓛(L²))) | **DIMOSTRATO** | — |
| VAR-Q18-CE (P11(e) con B solo continuo) | 2 | PASS | controesempio **DIMOSTRATO**; l'enunciato «P11(e) vale per B continuo in norma» è **FALSO** | C-2 (redazionale) |
| VAR-Q18-mult | 2 | «ridotto a» non è una riduzione | **APERTO** (sottocaso residuo, nessuna riduzione) | C-3 |
| VAR-Q10-EX | 3 | PASS | **DIMOSTRATO**; chiude la riga VAR-T1(c)-Q10 | — |
| VAR-Q17(a) | 4 | PASS-con-fix | **DIMOSTRATO** per v continua a tratti (quadro di P11); per v ∈ L^∞ dopo C-4 (redazionale) | C-4, C-5 |
| VAR-Q17(b) | 4(c) | «ridotto a» è una riformulazione della domanda | **APERTO** (nessuna riduzione; ostruzione solo euristica) | C-6 |
| VAR-P12(d) nella classe quadratica | 5 | PASS-con-fix | **DIMOSTRATO** come nuovo ID VAR-P12(d)-quad | C-7 |
| VAR-P12(d) (caso generale) | 5 | — | **APERTO** (la «riduzione» è una sottodomanda, non una riduzione) | C-7(c) |
| VAR-C3Q2-R (a) criterio di rango | 6 | PASS | **DIMOSTRATO** | — |
| VAR-C3Q2-R (b) f(x+t) non identifica □ | 6 | PASS-con-fix | **DIMOSTRATO** con la prova elementare di C-8 (senza Wiman–Valiron); senza C-8 resta CON-FONTE | C-8 |
| VAR-C3Q2-R (a′) olonomo ⇒ mai identificato | 6 | PASS | **CON-FONTE** (disuguaglianza di Bernstein, Björk cap. 1, classica, non riletta) | — |
| VAR-Q13 (non monico) | 6 | «ridotto a» non provato | **APERTO** (nessuna riduzione) | C-9 |
| SYS-DIRAC-POL (a) formale | 7 | PASS | **DIMOSTRATO** | — |
| SYS-DIRAC-POL (b) t fisso, tempi reali | 7 | PASS (kill-argument: sopravvive) | **DIMOSTRATO** | C-10 (redazionale) |
| II-T2(b′)-CRIT (a) | 8 | PASS-con-fix | **DIMOSTRATO** | C-11 (redazionale) |
| Q-S8SYS-4 | 8 | PASS, con precisazione di lettura | **FALSO** nella lettura «il polo dipende solo da A(ξ_0) e dalla fattorizzazione», anche con la stessa matrice A(ξ_0) (C-12) | C-12 |
| SYS-MAXWELL | 9 | PASS | **DIMOSTRATO** (stesso statuto di SYS-C1: dipende da SYS-EX come registrato) | C-13 (osservazione) |
| ENC-T2(c′)-P (classe principale) | 10 | PASS-con-fix | **DIMOSTRATO** | C-14 (redazionale) |
| ENC-Q4-S (a) | 11 | PASS-con-fix: il passo «u(t,·) ≢ 0 per ogni t» può essere falso | **PROVA SCRITTA**; DIMOSTRATO dopo il recepimento di C-15 | C-15, C-16 |
| ENC-Q4 (lettura DM3) | 11(c) | «ridotto a» non è una riduzione | **APERTO** | C-16 |
| ENC-Q10-D (i), (ii) | 12 | PASS-con-fix: la formula di κ era delegata a SymPy | **PROVA SCRITTA**; DIMOSTRATO dopo l'inserimento della derivazione C-17 (testo fornito qui sotto) | C-17 |
| ENC-Q10 residuo «V reale» | 12(c) | la frase «non ho un esempio» è superata | **APERTO**, da riformulare: esiste un esempio reale banale (C-18) | C-18 |
| DICT-ILIM-Hs | 13 | PASS-con-fix | **CON-FONTE** (condizione di cono); **DIMOSTRATO** dopo C-19 (lemma elementare, testo fornito) | C-19 |
| DICT-U3d-v (velocità) | 14 | PASS-con-fix | **DIMOSTRATO** (la formula di Čebyšëv è elementare, non serve la fonte) | C-20 (redazionale) |
| DICT-U3d-v (ottimalità) | 14 | «ridotto a» non provato | **APERTO** | C-21 |
| DICT-Q3-R (b) controesempio | 15 | PASS | **DIMOSTRATO** | — |
| DICT-Q3-R (c) | 15 | è la definizione, non una riduzione | **APERTO** (riformulato come problema di divisione C^∞) | C-22 |
| DICT-Q3-R (a) caso analitico | 15 | non verificabile qui | **CON-FONTE** (Malgrange 1966, non letto) | — |
| DICT-Q4-C (1) ⟺ (2) e «rango finito ⇒ falso» | 16 | PASS-con-fix | **DIMOSTRATO** | C-23 (redazionale) |
| DICT-Q4-C «rango infinito ⇒ A(iii)» | 16 | logica corretta, lemma non letto | **CON-FONTE** (Amitsur 1965 / Brešar–Šemrl 1999) | — |
| DM-δ-MINIMAX | 17 | PASS-con-fix (kill-argument: sopravvive) | **DIMOSTRATO** con l'ipotesi di non degenerazione M > δ_0 (C-24) | C-24 |

## 2. Audit dei claim

### §1 VAR-P11(e) — PASS
- **Lemma C.** La scrittura F(t) = ∫_0^{t−s}T(σ)f(t − σ)dσ e lo spezzamento del rapporto incrementale sono corretti. Per il primo termine: ‖T(σ)f(t + h − σ) − T(t − s)f(s)‖ ≤ M_0‖f(t + h − σ) − f(s)‖ + ‖(T(σ) − T(t − s))f(s)‖, uniformemente per σ ∈ [t − s, t − s + h] (D1). Il secondo termine converge per convergenza dominata, perché f′ è uniformemente continua. Il passo sul dominio è esatto: (T(h) − I)F(t) = F(t + h) − F(t) − ∫_t^{t+h}T(t + h − r)f(r)dr. Il limite destro basta per il generatore. Verificato in dimensione finita (`c_semigroup`).
- **Passi 1–3.** v esiste per Picard. f = Bw è C¹ con f′ = B′w + Bv perché w′ = v è continua. z′ = T(t − s)(A_0x + B(s)x) + ∫T(t − r)f′ usa f(s) = B(s)w(s) = B(s)x. Quindi v − z′ = ∫T(t − r)B′(u − w). Corretto.
- **Passo 4 (D2).** u − z = ∫T(t − r)B(r)e(r)dr. (w − z)(s) = 0 e (w − z)′ = ∫T B′e, quindi ‖w − z‖ ≤ (t − s)M_0β_1∫_s^t‖e‖. Dato che e = (u − z) − (w − z), Gronwall dà e ≡ 0. Il «doppio integrale» è maggiorato correttamente.
- **Passo 5.** Con f = Bu = Bw si ha z = u, e la formula A_0u = z′ − Bu = u′ − Bu è corretta. u ∈ C([s, T]; D(A_0)) nella norma del grafico.
- **D3.** In S8-VAR PP riga 72, P11(e) è usato solo con A_0 = −iH_0 e B(t) = −iV(t) ∈ C¹([0, T]; 𝓛(ℋ)), e ‖V(t)·‖_{𝓛(L²)} = ‖V(t)‖_{L^∞}. La catena L2-cor ← P11(e) usa esattamente l'uscita di §1: u ∈ C¹, u(t) ∈ D(H_0). Il resto di L2-cor era già auditato (AUDIT_S8-VAR_L2cor). La riga di Gate 8 («DIMOSTRATO quando la prova autonoma di P11(e) sarà scritta e controllata») è soddisfatta.

### §2 VAR-Q18-CE — PASS
- Antiaggiunzione: il segno è giusto, con il prodotto lineare a sinistra (D4). Verificato sul modello ℂ³ ⊕ ℂ.
- Continuità in norma: ‖B(t) − B(t′)‖ ≤ √2‖f(t) − f(t′)‖ ≤ 2‖f(t) − f(t′)‖ (D5).
- B non è C¹: corretto.
- La soluzione esplicita è mite. Prima componente: ∫T(t − r)cos(nr)T(r)x dr = (sin(nt)/n)T(t)x. Seconda: 1 − ∫n²C = cos nt (`c_semigroup`). Per unicità della soluzione mite (P11(a)–(d)) è U(t, 0)x_*. La conclusione vale per ogni t con sin(nt) ≠ 0, non solo per t < π/n.
- La domanda VAR-Q18 è formulata in astratto (A_0 generatore, B ∈ C([0, T]; 𝓛(X))), quindi il controesempio la chiude in negativo. Chiude anche ENC Q13, che chiede V ∈ C(ℝ; B(ℋ)).
- **Osservazione (non bloccante).** Il controesempio si realizza dentro L²(J) con H_0 = −∂² di Neumann: si prende e = costante normalizzata (H_0e = 0), x ⊥ e con x ∉ D(H_0), e B(t)y := ⟨y, e⟩f(t) − ⟨y, f(t)⟩e. Resta fuori solo il caso di una **moltiplicazione** (OC-1).

### §3 VAR-Q10-EX — PASS
- D6: la stima |g_0^{(k)}(s)| ≤ k!(θs)^{−k}e^{−1/(2s²)} è quella di S8-VAR riga 300. Ho ricontrollato che Re(1 + ζ)^{−2} ≥ 0.826 > 1/2 per |ζ| ≤ 1/10, e la stima numericamente per k ≤ 8. sup_s s^{−k}e^{−1/(2s²)} = k^{k/2}e^{−k/2} ≤ (k!)^{1/2} (verificato per k ≤ 200, C = 1).
- La somma di Leibniz è ≤ 2^k(k!)^{3/2}. Il sup in ℓ vale (k/(2e))^{k/4}, anche quando il punto critico cade fuori da (0, 1], perché allora il sup su (0, 1] è minore.
- D7: log ℓ + ℓ^{−4}/2 è decrescente su (0, 1] (punto critico 2^{1/4}) e vale 1/2 in ℓ = 1.
- D8: (k + j)! ≤ 2^{k+j}k!j! e (2k)! ≥ (k!)², quindi la maggiorante è (2^{7/4}A)^k|x|^{2k}/(k!)^{1/4}. Le derivate in x danno solo fattori polinomiali.
- Sui gap ogni punto appartiene al più a un g_j, e su K tutte le derivate sono nulle: g^{(k)} = 0 su K è corretto.
- D9: con I = (0, 1) l'argomento su int Z è corretto. W aperto incontra un tempo di gap, perché K è mai denso; lì u(t, ·) è intera, non nulla (u(t, 0) = g(t) > 0) e non può annullarsi su un intervallo. |Z| ≥ |K| · ∞ > 0.
- La risposta a VAR-Q10 («esiste u … con |Z| > 0 e int Z = ∅?») è sì, con V = 0 e u ∈ C^∞. Con V′ = 1_Z si hanno due leggi L^∞ distinte.

### §4 VAR-Q17 — (a) PASS-con-fix; (b) APERTO senza riduzione
- Gauge: verificato simbolicamente. **C-4.** Il quadro di P11 chiede B fortemente continuo a tratti, mentre v ∈ L^∞(0, T). Basta dire che per B misurabile e limitato la soluzione mite è ancora unica (lo stesso Gronwall), e che e^{−i∫v}e^{−itH}ψ_0 soddisfa l'equazione di Duhamel (integrale di Bochner). Oppure si restringe v a continua a tratti. È una precisazione del quadro.
- D11: H = H_0 + V_0 è autoaggiunto su D(H_0) (perturbazione limitata). φ̌ è di Schwartz, quindi φ̌(H)ψ_0 ∈ D(H^∞) ⊂ D(H_0).
- D10: V_0 non dipende da t. L2-cor si applica sull'intervallo (η, T − η) alla soluzione con dato e^{−iηH}φ̌(H)ψ_0 ∈ D(H_0) (e^{−iηH} conserva D(H)). Il dato è nullo, quindi φ̌(H)ψ_0 = 0. Serve η < T/2.
- Il limite con l'approssimazione dell'identità è corretto.
- **C-5 (lemma delle medie).** «Lo stesso calcolo in s» nasconde un termine di bordo. Dopo Fubini il nucleo interno è ∫_0^{T−r}h(r + σ)T(σ)dσ con k(0) = h(r) ≠ 0, e A_0 applicato dà −h(r)B(r)ψ(r) − ∫h′(r + σ)T(σ)B(r)ψ(r)dσ. Il termine è limitato e integrabile in r, quindi il lemma resta vero per chiusura di A_0, ma il termine va scritto (formula verificata in `c_semigroup`).
- **(c) C-6.** «Continuazione laterale per i∂_tψ + ∂_x²ψ = Vψ con V ∈ C([0, T]; L^∞) in una classe ψ ∈ C([0, T]; L²)» **è** VAR-Q17(b), riscritta. Non è una riduzione. Anche la frase «ogni soluzione del problema con sorgente si può modificare lontano da ω» è un'euristica, non un'ostruzione provata. Stato: APERTO. La formula per R_φ e il fatto che R_φ = 0 su ω sono corretti.

### §5 VAR-P12(d) nella classe quadratica — PASS-con-fix
- Heisenberg (ẋ = 2p, ṗ = −2ω²x) e il fattore di tratto sono verificati. M = M_2M_1 = diag(−1/5, −5): tr = −26/5, det = 1.
- exp(sl₂(ℝ)) ⊂ {tr > −2} ∪ {−I} è classico (verificato su 300 campioni). Il caso di bordo tr = −2 forza e^Ξ = −I.
- **D12.** Stone–von Neumann non serve. Se e^{−iTK′} = cU(T, 0), le fasi si cancellano nella coniugazione. Per K′ quadratico affine, e^{iTK′}(x, p)e^{−iTK′} = e^{TΞ}(x, p) + v su 𝒮(ℝ). L'uguaglianza tra le due mappe affini, con x, p, 1 linearmente indipendenti come operatori, dà v = 0 ed e^{TΞ} = M.
- **C-7.**
  - (a) τ_2 := π/(4ω_1) è scritto uguale a τ_1. Il valore è giusto (θ_2 = 2ω_2τ_2 = 5π/2), ma va detto esplicitamente.
  - (b) «Continua in ω ∈ L¹» va precisato: serve ω_n² → ω² in L¹, che vale per regolarizzazioni uniformemente limitate. Ho controllato due regolarizzazioni tanh: tr = −4.81 e −5.13.
  - (c) Il risultato riguarda solo i logaritmi quadratici, con potenziale non limitato (D13). VAR-P12(d) chiede di V(t, x) generico e di logaritmi differenziali qualsiasi, e resta APERTO. La «riduzione» di §5(c) è una sottodomanda nuova (OC-3), senza implicazione verso (d).
  - (d) Nel LEDGER va registrato un ID separato, VAR-P12(d)-quad (DIMOSTRATO), e non «(d) FALSO nella classe quadratica».

### §6 VAR-C3Q2-R — (a) PASS; (b) PASS-con-fix; (a′) CON-FONTE
- (a) La divisione per L monico a destra con resto in ⊕B∂_t^j è S8-VAR §5(a), già DIMOSTRATO; ne ho controllato un esempio. ker π = 0 ⟺ Ann = A_2L è corretto in entrambe le direzioni. D14: la localizzazione di Ore D_B è piatta come B-modulo destro, quindi il rango è additivo e un sottomodulo non nullo di B^m ha rango ≥ 1. È algebra standard (Goodearl–Warfield), accettabile senza fonte.
- **(b) C-8.** Wiman–Valiron (D15) si può eliminare. Si ha f^{(k)} = f·T_k(e^y), con T_k polinomio di Touchard monico di grado k (verificato per k ≤ 8; in generale per induzione: T_{k+1}(z) = z(T_k + T_k′)). Una relazione Σ_{k≤K}a_k(t, x)∂_x^ku = 0 con a_K ≢ 0 diventa Σa_k(t, x)T_k(e^{x+t}) = 0. Le funzioni t, x, e^{x+t} sono algebricamente indipendenti su ℂ, e il coefficiente di (e^{x+t})^K è a_K: quindi a_K = 0, assurdo. Lo stesso argomento vale con ∂_t al posto di ∂_x. Con questo testo (b) è DIMOSTRATO. Anche il passaggio per «restrizione di un olonomo» diventa superfluo. Il resto di (b) è corretto: ∂_t − ∂_x ∈ Ann(u) ha ordine 1 in ∂_t, quindi non sta in A_2□, e □u = 0.
- (a′) D16: GKdim(A_n/A_nP) = 2n − 1 e la disuguaglianza di Bernstein sono classiche. Stato CON-FONTE (non rilette).
- **C-9.** La frase «Ann(u) ⊂ A_2 ∩ D_BL ⟺ ker π = 0» per L non monico non è provata (senza monicità non c'è la decomposizione del passo 1), e «ridotto a: calcolare rank_B e la saturazione» è il problema stesso. VAR-Q13 resta APERTO, senza riduzione.

### §7 SYS-DIRAC-POL — PASS
- (a) Ho ricalcolato g_1 e g_2 con le serie di SymPy in t, poi ω² → ξ² + m²: coefficienti in ℚ[ξ, m] fino a t^9. Il passaggio «identità analitica ⇒ identità formale» è corretto: i coefficienti di Taylor sono polinomi uguali su un aperto reale. ZXZ ha residuo ~10^{−31} in tre punti nuovi, anche con ξ < 0.
- (b) Lemma E (D17): l'argomento è corretto. La maggiorazione scritta «2/|Q′(X)| + |[1/Q′]|» va corretta (C-10) in 1/|Q′(X)| + 1/|Q′(2X)| + |1/Q′(2X) − 1/Q′(X)|, usando la monotonia di 1/Q′. Resta O(1), quindi la conclusione non cambia.
- D18: il raggruppamento a meno di costanti è corretto. I coefficienti c_j sono costanti (±1/2, ±i/2 e prodotti), non dipendono da ξ.
- D19: i tempi reali servono per |e^{iR}| = 1 nello sviluppo di |S|².
- L'asintotica è verificata in forma esatta: (e^{tA})_11 = e^{iωt} + i(ξ/ω − 1)sin ωt, con ω − ξ = m²/(2ξ) + O(ξ^{−3}). Numericamente ξ|G(ξ)| → m²t/2.
- La domanda Q-S8SYS-1 ammette anche tempi in ℂ[ξ][[t]]. (a) risponde sì in forma formale; (b) risponde no a t fisso con polinomi reali. Il caso complesso (OC-5) è dichiarato fuori portata. La riga di Fase 8 «Q-S8SYS-1 APERTO» va divisa di conseguenza.

### §8 II-T2(b′)-CRIT e Q-S8SYS-4 — PASS-con-fix
- (a) **C-11 (D20).** «Dividere le colonne per potenze di (ξ − ξ_0)» non basta in generale: possono servire operazioni di colonna. L'enunciato corretto è che E(ξ) ∩ 𝒪^n, con 𝒪 l'anello locale (DVR) in ξ_0, è un addendo diretto libero di rango k (𝒪^n/(E ∩ 𝒪^n) è privo di torsione su un PID); se ne prende una base. Il testo cita la forma di Smith, quindi il fix è di dicitura. Il resto è corretto: P = [e 0][e f]^{−1}; P è razionale, quindi «polo» ⟺ «illimitato»; dim E_0 + dim F_0 = n dà det = 0 ⟺ E_0 ∩ F_0 ≠ 0. Ho ricalcolato il proiettore con le basi saturate (metodo indipendente da B(A)/B(ξ)): A_1 dà det[e f](0) = 1 e nessun polo; A_2 dà det = 0 e un polo 1/(2ξ).
- **C-12 (D21).** Nella congettura di S8-SYS il lato destro («un blocco di Jordan non banale che mescola autovalori di Q e di B») non è una funzione di A(ξ_0), perché in ξ_0 gli autovalori di Q e di B coincidono. La lettura del pacchetto («dipende solo da A(ξ_0) e dalla fattorizzazione») è l'unica in cui la congettura ha senso, ed è falsa. Il controesempio si può rafforzare. Con la permutazione S: e_1 → e_2, e_2 → e_3, e_3 → e_1, la matrice A_2′ := SA_2S^{−1} ha A_2′(0) = A_1(0) **come matrice**, lo stesso polinomio caratteristico e ancora il polo (`c_sys_enc`). Consiglio di riportarlo: elimina la riserva «stessa forma di Jordan ≠ stessa matrice». Q-S8SYS-4: FALSO in questa lettura; la versione corretta è il criterio (a).

### §9 SYS-MAXWELL — PASS
- Ho verificato le sizigie, det(τ²I + C²) = τ²(τ² − |ξ|²)², il rango 6 e che il nucleo sinistro su Frac(R) ha dimensione 2 ed è generato da S_1 ed S_2.
- D22: l'argomento con il gcd è corretto. I supporti sono disgiunti e gcd(ξ_1, ξ_2, ξ_3, τ) = 1. Controllo indipendente dell'esattezza di 0 → R² → R^8 → R^6 (Buchsbaum–Eisenbud): i ranghi danno 2 + 6 = 8; I_2(S) contiene τ² e ξ_i², quindi ha profondità 4 ≥ 2; I_6(P) ≠ 0.
- Lo zoccolo: Ext^i_R(k, R) = 0 per i < 4 vale localizzando in 𝔪 (profondità 4). Le due successioni lunghe sono usate correttamente.
- D23: soc = 0 ≤ 1, quindi SYS-EX si applica.
- **C-13 (osservazione).** Per Auslander–Buchsbaum basta pd M_P ≤ n − 1 (allora depth ≥ 1, cioè Hom(k, M) = 0). La frase «vale per ogni sistema con pd M_P ≤ n − 2» è vera ma non nitida.
- Stato: DIMOSTRATO con lo stesso statuto di SYS-C1, cioè dipendente da SYS-EX come registrato (con la sua CON-FONTE sull'iniettività di C^∞).

### §10 ENC-T2(c′) nella classe principale — PASS-con-fix
- L'identità P(∂_t, L_q)(e^{αt}f) = e^{αt}P(α, L_q)f è verificata per un P generico.
- D24: p(L_q) ha coefficiente di testa costante (−1)^{deg p}lc(p) e ordine 2deg p, e f si annulla vicino agli estremi di J°. L'unicità di Cauchy dà f ≡ 0 (se deg p = 0, è immediato).
- D25: il passo 5 è corretto. Più semplice: da P_* | R segue Ru = 0, quindi Rh = 0 e (τ − α) | R.
- **C-14.** Va richiesto che J° ∖ [x_1 − η, x_1 + η] abbia interno non vuoto («per ogni η tale che …»). Altrimenti non c'è spazio per f.
- Stato: DIMOSTRATO. La riga di Gate 8 «ENC-T2(c′) nella classe principale APERTO» passa a DIMOSTRATO.

### §11 ENC-Q4-S — PASS-con-fix (C-15 non è redazionale)
- Il quadro coincide con S8-ENC PP §5: (S) con N_V = I per c_V = 0, e uscite modulo ≈ con θ arbitraria.
- Passo 2 verificato simbolicamente: il residuo è (−θ_1′ − δ)u′. Passo 6 (D26): la composizione resta di Volterra simmetrica. Verificato discretizzando due nuclei: il nucleo composto è nullo per |r| > |x|, ‖𝒱^n‖ ≤ (2‖k‖a)^n/n! per n ≤ 15, e il raggio spettrale numerico è piccolo. Passo 7 corretto.
- **C-15 (D27, lacuna reale).** Il pacchetto usa «u(t, ·) ≢ 0 per ogni t» (passi 2, 4, 7). Per soluzioni classiche su I × J° senza condizioni al bordo è **falso** in generale: la serie di Tychonoff di §3 (V = 0) si annulla identicamente per t ∈ K. La prova si ripara localizzando. G := {t : u(t, ·) ≢ 0} è aperto e non vuoto (u ≠ 0 continua). Su una componente G_0 di G si ha θ_1 = κ − δt (passo 2), θ ≡ θ_0 (passo 4; θ è automaticamente liscia su G_0, perché e^{iθ} = w′/w in un punto con w ≠ 0) e μ(t) = 1 (passo 7). Quindi δt + costante ∈ 2πℤ su un intervallo, e δ = 0. L'enunciato resta invariato. Propongo PROVA SCRITTA fino al recepimento.
- D28: coerente con ENC-N1′(iii) e (v). (S) è vera, (C) è falsa e l'identificabilità è falsa, come deve essere. Nota di portata: il risultato risponde a ENC Q4 nella lettura DM-φ (intersezioni modulo ~). L'esempio (v) di S8-ENC ne era già un caso particolare.
- **C-16.** «APERTO — ridotto a ENC-P0 con W(t)» non è una riduzione: S8-ENC già registra «aperta per W(t) strutturati». Stato: APERTO.

### §12 ENC-Q10-D — PASS-con-fix
- (i) Verificato **in generale** (u, φ libere qualsiasi, non solo sull'esempio): L_0(Λφ) = V_1Λφ, e il segno opposto è falso. Λu = 0.
- **C-17 (D29), derivazione a mano da inserire al posto di «delegato a SymPy».** Sia φ libera con Λφ = χ, e W := uφ_x − u_xφ, così χ = W/u. Dato che φ_t = iφ_xx e u_t = iu_xx,
  ∂_t(φ/u) = i(uφ_xx − φu_xx)/u² = iW_x/u² = i(u_xχ + uχ_x)/u² = i(χ_x + (u_x/u)χ)/u.
  In x_0 questo è iκ(t). Ogni ψ con Λψ = χ si scrive ψ = φ + a(t)u, e L_0(au) = ia′u. Quindi ψ è libera ⟺ a′ = 0 ⟺ c(t) = (φ/u)(t, x_0) + costante ⟺ c′ = iκ. Verificato simbolicamente in generale (`c_darboux`).
- D30: u = x² + 2it non si annulla per x > 0, e V_1 = −2(u_xx/u − u_x²/u²) non richiede un ramo del logaritmo. Il residuo di 1/u, 2u_xx/u², è verificato in generale.
- **C-18 ((c) e OC-7).** Esiste un esempio **reale**, regolare sul dominio e dipendente da t: il boost di Galileo u_G = (x − 2kt + a)e^{i(kx − k²t)} è libera e dà V_1 = 2/(x − 2kt + a)², regolare su I × J se J ⊂ (2k sup I − a, ∞). Λ_G produce soluzioni del modello reale (`c_darboux`). È banale, perché è un boost di Galileo di un caso stazionario, ma rende falsa la frase «per V_1 reale, regolare e dipendente da t non ho un esempio». OC-7 va riformulato: esempi reali non riconducibili per simmetria (Galileo, lente) a potenziali stazionari. La «riduzione» a Matveev–Salle è un puntatore, non una riduzione.
- Stato di (i)–(ii): PROVA SCRITTA, DIMOSTRATO dopo l'inserimento di C-17. Il testo è fornito qui.

### §13 DICT-ILIM-Hs — PASS-con-fix
- Passo 2: il resto integrale è corretto (verificato con s = 2). Il cono è convesso, quindi il segmento sta in C_x.
- Passo 3 (D32): per rotazione, le norme |D^βP(0)| cambiano per un fattore limitato (azione lineare limitata sulle parti omogenee). Lo scaling dà r^{−|β|−N/2}.
- Passi 4–7: l'algebra degli esponenti è verificata: θ(s + N/2) = 1 − θ e θ_j = θ(s + 1 − j). La nitidezza vale per scaling, e su bump che si restringono il rapporto è costante (0.35).
- Casi limite: M = 0 o ‖f‖_2 = 0 implicano f = 0.
- **C-19 (D31).** La condizione di cono uniforme si dimostra in poche righe e la CON-FONTE (Adams–Fournier §4.11, numero non verificato) diventa superflua.
  - In una carta, Ω ∩ U = {y_N > φ(y′)} ∩ U con Lip φ ≤ L.
  - Per x ∈ Ω ∩ U′, con U′ ⋐ U, il cono {x + z : z_N > L|z′|, |z| < h} sta in Ω, perché x_N + z_N > φ(x′) + L|z′| ≥ φ(x′ + z′).
  - I punti lontani dal bordo hanno una palla.
  - Un numero finito di carte e un numero di Lebesgue danno h uniforme; i coni sono congruenti a meno di rotazioni.
  - Per x ∈ Ω̄ si usa sup_Ω = sup_Ω̄.

  Con questo testo: DIMOSTRATO; senza, CON-FONTE.

### §14 DICT-U3d-v — PASS-con-fix
- Passo 1 (D33): la costante 2(ΛT/4)^J/J! è giusta (verificato max|ω_J| = 2(Λ/4)^J per J = 3, 6, 9). **C-20:** non è CON-FONTE. È il resto di Lagrange (Rolle) più |T_J| ≤ 1, cioè due righe elementari.
- (ii), (iii): corrette. C_k ≤ ‖k‖_1/(1 − e^{−1}) per concavità; m_k ≤ C_k max(1/T, Λ); (J/e²)^J/J! ≤ e^{−J} (J < 60).
- (iv): con J ≥ log(1/ε) l'errore è ≤ 2εm_k + εk(δ/2), quindi c'è un fattore 2 da scrivere (redazionale).
- Controllo indipendente su un nucleo diverso da quello di S10, k = t^{−1/2}: errori L¹ 0.754, 0.542, 0.443 contro le stime 0.779, 0.542, 0.443 (J = 4, 8, 12). La stima è soddisfatta e quasi esatta, dominata dalla coda. La formula per τ_k con t^{−β} è verificata.
- D34: i pesi reali di segno qualsiasi danno ancora un sistema locale aumentato. Si perde la positività e la dissipatività, che però non sono affermate.
- **C-21.** «Ottimalità APERTA — ridotto a un limite inferiore per somme lacunari» non contiene un'implicazione provata. Stato: APERTO.

### §15 DICT-Q3-R — (b) PASS
- (b): u″/u = 4/x^6 − 6/x^4 → +∞ e u è piatta in 0 (verificato fino a k = 6).
- Il caso è davvero intermedio: A_u è iniettiva solo su {x > 0}, che non è denso, e non è suriettiva su {x ≤ 0}.
- D35: u e V sono reali, e la classe è quella di Schrödinger con V reale. Nessuna V continua (né L^∞_loc) esiste.
- **C-22.** (c) è la definizione di legge riletta come divisione. È una riformulazione, non una riduzione che sposti il problema. Stato: APERTO (riformulato).
- (a): CON-FONTE. L'argomento elementare per K = q = 1 è corretto in una variabile. In più variabili «meromorfa e formalmente olomorfa ⇒ olomorfa» richiede la fedele piattezza del completamento formale (standard); va detto.

### §16 DICT-Q4-C — PASS-con-fix
- (1) ⇒ (2) con u = 0 ∈ F_n: corretto.
- (2) ⇒ (1): il polinomio in s ha coefficiente direttore det(ℓ′_j(D_iw)) ≠ 0. **C-23:** va detto perché esistono ℓ′_j (funzioni test φ_0, …, φ_N) con quel determinante non nullo: N + 1 distribuzioni linearmente indipendenti ammettono funzioni test duali.
- «Rango finito ⇒ (1) falso» (D37): le coordinate λ_k(f) = ⟨Df, φ_k⟩ sono continue, perché D è continuo verso 𝒟′ debole, quindi ker D = ∩ker λ_k. Corretto.
- «Rango infinito ⇒ (2)»: con il lemma di Amitsur (n = N + 1 operatori localmente dipendenti ⇒ una combinazione non banale di rango ≤ N) la logica è corretta, e rank(Σc_iD_i) ≤ N + codim Z. CON-FONTE (D36).
- Esempio (b) e corollari: corretti. Per i corollari conta il rango delle **combinazioni** Σc_iD_i, non dei singoli D_i: per differenziali e convoluzioni la combinazione è dello stesso tipo e non nulla, quindi va bene.

### §17 DM-δ-MINIMAX — PASS-con-fix
- Limite superiore (D38): VAR-P3(c) (S8-VAR PP §1.6) vale per ogni coppia con |u_1| ≥ δ al denominatore. Qui al denominatore c'è la u vera, in 𝒰, quindi |u| ≥ δ_0. ‖V_{u*}‖ ≤ (|u*_t| + |u*_xx|)/δ_0 ≤ 2M/δ_0. Le costanti dipendono da ℓ_t, ℓ_x. u* esiste perché u stessa va bene.
- Limite inferiore: verificati ∂_x^kh = ε^{1−k/3}φ^{(k)} e il salto ε^{1/3}φ″(0)/u_1 in x_0. ũ = u_1 + h/2 è ε/2-vicino a entrambe. L^∞ ≥ valore puntuale vale perché V_{u_2} − V_{u_1} è continua.
- **C-24 (D39).** «u_1 con |u_1| ≥ 2δ_0 e derivate ≤ M/2, per esempio una costante» richiede M ≥ 4δ_0, che non è scritto. Se M < δ_0 la classe è vuota e il limite inferiore è falso. Fix:
  - aggiungere l'ipotesi M > δ_0;
  - prendere u_1 ≡ (M + δ_0)/2;
  - riscalare φ con il margine (M − δ_0)/2;
  - porre ε_0 := min((M − δ_0)/4, ε_1), con ε_1 tale che supp h ⊂ K′.

  È un'ipotesi di non degenerazione e non cambia la sostanza. Stato: DIMOSTRATO con l'ipotesi.

## 3. Kill-argument

**KA-1: SYS-DIRAC-POL (b)** (a t fisso nessuna parola finita a tempi polinomiali reali).
- *Attacco 1.* Scegliere tempi che rendano W_11 = e^{iξt} + (termine che decade come 1/ξ). Una somma finita Σc_je^{iP_j} con P_j reali che tende a 0 è identicamente nulla (Lemma E), quindi nessuna somma del genere decade come 1/ξ senza essere zero. Il termine i(m²t/(2ξ))e^{iξt} è quindi irraggiungibile. Respinto.
- *Attacco 2.* I coefficienti potrebbero dipendere da ξ tramite cos(q(ξ)m). No: sono riscritti come esponenziali di fasi polinomiali, con coefficienti costanti. Respinto.
- *Attacco 3.* La prova usa solo ξ → +∞. Questo rafforza l'enunciato: basta l'uguaglianza su una semiretta.
- *Attacco 4.* Tempi complessi. Fuori dall'enunciato, che li esclude (OC-5).
- **Esito: SURVIVES.**

**KA-2: DM-δ-MINIMAX** (Θ(ε^{1/3})).
- *Attacco 1.* L'osservazione in t può aiutare? No: h non dipende da t e ∂_tu_1 = ∂_tu_2. Respinto.
- *Attacco 2.* Uno stimatore più furbo, che non passi per u*? Il limite inferiore è a due punti e vale per ogni mappa ũ ↦ V̂. Respinto.
- *Attacco 3.* Il limite superiore usa P3(c) con il denominatore giusto? Sì (vedi D38). Respinto.
- *Attacco 4.* La classe potrebbe essere vuota o senza margine. **Accolto**: porta al fix C-24.
- *Attacco 5.* Una famiglia diversa, sinusoidale con derivate ≤ M, dà la stessa scala ε^{1/3} (rapporto → 1): coerente.
- **Esito: SURVIVES-WITH-FIX (C-24).**

**KA-3: ENC-Q4-S** (eseguito in più, perché il claim dichiara «il primo esempio con (S) non vacua»).
- *Attacco.* Il passo «u(t, ·) ≢ 0 per ogni t» fallisce sulle soluzioni di Tychonoff. **Accolto**: la prova come scritta ha una lacuna.
- *Riparazione.* Localizzazione su una componente di {t : u(t, ·) ≢ 0} (C-15). La conclusione regge.
- **Esito: SURVIVES-WITH-FIX.**

**KA-4: VAR-Q10-EX.**
- *Attacco 1.* Z contiene gli zeri ai tempi di gap? Per ogni tempo di gap u(t, ·) è intera e non nulla, quindi ha zeri discreti in x: è un insieme di misura nulla che non crea interno.
- *Attacco 2.* Il bordo t ∈ {0, 1}? Escluso da I = (0, 1).
- **Esito: SURVIVES.**

## 4. Le «riduzioni» (punto 6 della richiesta)

| sede | «APERTO — ridotto a …» del pacchetto | giudizio |
|---|---|---|
| §2 Portata, VAR-Q18-mult | P11(e) per moltiplicazioni continue non C¹ | è il sottocaso residuo, non una riduzione → «APERTO» |
| §4(c), VAR-Q17(b) | continuazione laterale per soluzioni miti con V(t, x) | è la domanda stessa → «APERTO» |
| §5(c), VAR-P12(d) | log non quadratici di metaplettici con tr < −2 | sottodomanda senza implicazione verso (d) → «APERTO» (OC-3 resta come domanda) |
| §6, VAR-Q13 | rank_B e saturazione A_2 ∩ D_BL | l'equivalenza enunciata non è provata → «APERTO» |
| §11(c), ENC-Q4 DM3 | ENC-P0 con W(t) | già registrato come aperto in S8-ENC → «APERTO» |
| §12(c), ENC-Q10 V reale | Darboux reale (Matveev–Salle) | puntatore; c'è anche un esempio reale banale (C-18) → «APERTO», da riformulare |
| §14, ottimalità di U3d-v | limite inferiore per somme lacunari | nessuna implicazione → «APERTO» |
| §15(c), DICT-Q3 | divisione C^∞ | equivalenza per definizione, vera ma vuota → «APERTO (riformulato)» |

Nessuna delle otto è una riduzione dimostrata nel senso del protocollo. Le dichiarazioni di stato «APERTO» sono oneste, ma l'etichetta «ridotto a» va tolta o sostituita con «riformulato come» o «sottodomanda».

## 5. LEDGER_ROWS e open_questions

**Correzioni a LEDGER_ROWS:**
- **VAR-P12:** sostituire «(d) FALSO nella classe quadratica» con due righe: VAR-P12(d)-quad DIMOSTRATO; VAR-P12(d) APERTO.
- **VAR-Q18-mult:** «APERTO» senza «ridotto a».
- **VAR-C3Q2-R:** separare (a) DIMOSTRATO, (b) DIMOSTRATO con C-8 e (a′) CON-FONTE (Bernstein). Wiman–Valiron esce dalle dipendenze.
- **SYS-DIRAC-POL:** la riga di Fase 8 «II-T2(b′) derog., Q-S8SYS-1 — APERTO» va sostituita da: II-T2(b′)-CRIT DIMOSTRATO, Q-S8SYS-4 FALSO (lettura C-12), Q-S8SYS-1 (a) e (b) DIMOSTRATO, tempi complessi APERTO.
- **ENC-Q4-S:** PROVA SCRITTA fino a C-15.
- **ENC-Q10-D:** PROVA SCRITTA fino a C-17.
- **DICT-ILIM-Hs:** CON-FONTE, oppure DIMOSTRATO con C-19.
- **DICT-U3d-v:** DIMOSTRATO (C-20). La dipendenza CON-FONTE da Čebyšëv cade.
- **VAR-T1(c)-Q10** (riga di Fase 8): chiusa da VAR-Q10-EX.
- **ENC-T2(c′)** (riga di Gate 8): «nella classe principale APERTO» passa a DIMOSTRATO.
- **DM-δ-MINIMAX:** aggiungere l'ipotesi M > δ_0.
- Le colonne «proof-checker: da fare» vanno aggiornate con questo audit.

**open_questions:**
- OC-1: corretta; con l'osservazione di §2 il caso non moltiplicativo è chiuso anche dentro L²(J).
- OC-2, OC-3, OC-4, OC-5, OC-6, OC-8, OC-9, OC-10, OC-11: corrette.
- OC-7: la prima metà va riformulata (C-18).
- Nella lista «CIT da verificare» si tolgono Wiman–Valiron (C-8), la formula di Čebyšëv (C-20) e, se si recepisce C-19, Adams–Fournier. Restano Björk (Bernstein), Malgrange 1966 e Amitsur 1965 / Brešar–Šemrl 1999.

## 6. Elenco dei fix

- **C-1** (§1, redazionale): limite sinistro nel Lemma C per h < 0; una riga per «ogni soluzione classica è mite» (si deriva r ↦ T(t − r)u(r)).
- **C-2** (§2, redazionale): nell'enunciato usare n = ‖x‖ della costruzione; la conclusione vale per ogni t con sin(nt) ≠ 0. Facoltativo: la realizzazione con H_0 di Neumann su L²(J).
- **C-3** (§2): VAR-Q18-mult «APERTO», non «ridotto a».
- **C-4** (§4, redazionale): soluzione mite per v ∈ L^∞ (unicità per Gronwall con B misurabile limitato), oppure v continua a tratti.
- **C-5** (§4): termine di bordo −h(r)B(r)ψ(r) nel lemma delle medie.
- **C-6** (§4(c)): «APERTO»; l'ostruzione è euristica.
- **C-7** (§5): τ_2 esplicito; continuità in L¹ di ω² con limite uniforme; ID separato VAR-P12(d)-quad; (d) APERTO.
- **C-8** (§6): prova elementare della non D-finitezza con i polinomi di Touchard (testo in §2 di questo audit).
- **C-9** (§6): VAR-Q13 «APERTO», togliere l'equivalenza non provata.
- **C-10** (§7, redazionale): maggiorazione corretta nel Lemma E.
- **C-11** (§8, redazionale): basi saturate come addendo diretto libero (non solo divisione delle colonne).
- **C-12** (§8): lettura di Q-S8SYS-4 e controesempio con la stessa matrice A(ξ_0) (permutazione S).
- **C-13** (§9, osservazione): basta pd ≤ n − 1.
- **C-14** (§10, redazionale): η tale che J° ∖ [x_1 − η, x_1 + η] abbia interno non vuoto.
- **C-15** (§11, sostanziale): localizzazione su una componente di {t : u(t, ·) ≢ 0}.
- **C-16** (§11(c)): «APERTO», non «ridotto a».
- **C-17** (§12, sostanziale ma con testo fornito): derivazione a mano di κ via Wronskiano.
- **C-18** (§12(c), OC-7): esempio reale per boost di Galileo; riformulare il residuo.
- **C-19** (§13): lemma elementare del cono (testo fornito).
- **C-20** (§14, redazionale): errore di Čebyšëv elementare; fattore 2 in (iv).
- **C-21** (§14): ottimalità «APERTO».
- **C-22** (§15): (c) «riformulato», non «ridotto»; in (a), fedele piattezza per più variabili.
- **C-23** (§16, redazionale): esistenza delle funzioni test duali.
- **C-24** (§17): ipotesi M > δ_0, u_1 ≡ (M + δ_0)/2, φ riscalata, ε_0 esplicito.
