# AUDIT S10-INT — argomenti a PROVA SCRITTA di ESEMPI.md (EX10-b-ND, EX10-e-K, EX10-e-H)

Auditor: S-CHECK-EX10, 27/10/2026. Oggetto: `work/S10-INT/ESEMPI.md` (§2 b-coh passo 3c′; §5 passo 3b e argomento EX10-e-K; §5 passo 6) e le righe corrispondenti di `work/S10-INT/LEDGER_ROWS.md`. Riferimenti controllati: `claims/LEDGER.md` riga VAR-C3Q2 (stato (a)–(g) DIMOSTRATO, S-CHECK-F8-VAR OK) e `work/S8-VAR/PROOF_PACKAGE.md` §5.

Script dell'audit, scritti da zero e senza riusare codice di S10-INT, in `work/CHECK-F10/sympy/`: `ex10_b_nd.py`, `ex10_e_k.py`, `ex10_e_h.py`. Sono stati eseguiti con `D:\ProblemaBase\.venv\Scripts\python.exe -I`. Non è stato eseguito nessuno script di `_vendor`. Non ho salvato file `.out`: le uscite rilevanti sono riportate qui sotto.

## Verdetti

| riga | verdetto | stato dopo l'audit | fix |
|---|---|---|---|
| EX10-b-ND | **PASS** | DIMOSTRATO | nessuno (due precisazioni di stesura, facoltative) |
| EX10-e-K | **PASS-con-fix** | DIMOSTRATO con i fix K-1…K-4 | K-1 (unione → span), K-2 (X costante: argomento corretto), K-3 (dal «per ogni k» ai dati finiti), K-4 (ambito della terza clausola nella riga del LEDGER) |
| EX10-e-H | **PASS** | DIMOSTRATO | nessuno |
| V-ex a campione (EX10-a, b, e) | coerenti | — | nota editoriale su SYS-MAXWELL |

---

## 1. EX10-b-ND

### 1.1 Enunciato di riferimento
VAR-C3Q2(c) (PROOF_PACKAGE §5): se L = ∂_t − M con M ∈ B = ℂ[t,x]⟨∂_x⟩, u è analitica su Ω connesso e Lu = 0, allora Ann_{A_2}(u) = A_2L se e solo se u non è D-finita su ℂ(t,x). Nella prova la direzione che serve qui, «non D-finita ⇒ Ann = A_2L», passa per (b). Basta mostrare che nessun R ∈ B non nullo annulla u. Questo segue già dall'indipendenza su ℂ(t,x) delle sole derivate ∂_x^bu. Il LEDGER registra VAR-C3Q2 (a)–(g) come DIMOSTRATO, quindi è utilizzabile.

### 1.2 Verifica riga per riga
1. *Ipotesi di forma.* L = i∂_t + ∂_x² − x² non è monico, ma −iL = ∂_t − M con M = i∂_x² − ix² ∈ B. Poiché −i è un'unità, A_2L = A_2(−iL). Le ipotesi di VAR-C3Q2(c) valgono con m = 1. La riga ESEMPI dice «monico a meno del fattore i»: è corretto (controllo (2)).
2. *u_c risolve l'equazione* ed è intera in (t,x): u_c è analitica su ogni Ω connesso (controllo (1)).
3. *∂_x^bu_c/u_c = p_b(x, α) con grado esatto b in α.* La ricorrenza p_{b+1} = ∂_xp_b + p_b(−x + √2α) è corretta, perché ∂_x non agisce su α = α(t). Il coefficiente di testa si moltiplica per √2 a ogni passo, quindi vale (√2)^b: è una costante non nulla, il che serve. ESEMPI dice «grado esatto b per induzione» senza nominare il coefficiente di testa. L'induzione funziona proprio perché quel coefficiente è costante e non nullo (controlli (3) per b ≤ 8 e (3′) per il passo induttivo simbolico).
4. *Trascendenza.* α = α_0e^{−2it} con α_0 ≠ 0 è trascendente su ℂ(t,x) come funzione su Ω aperto: una relazione polinomiale Σ_jc_j(t,x)e^{−2ijt} = 0 a coefficienti razionali non tutti nulli è impossibile, perché esponenziali di frequenze distinte sono indipendenti su ℂ(t,x), per il principio d'identità su Ω connesso.
5. *Conclusione.* Supponiamo Σ_{b≤d}r_b(t,x)∂_x^bu = 0 con r_b ∈ ℂ(t,x) e r_d ≠ 0. Dividendo per u si ottiene Σ_br_bp_b(x,α) = 0: è un polinomio in α a coefficienti in ℂ(t,x) con coefficiente di testa (√2)^dr_d ≠ 0, il che contraddice il punto 4. Quindi lo span dei ∂_x^bu ha dimensione infinita, u_c non è D-finita e VAR-C3Q2(c) dà Ann_{A_2}(u_c) = A_2L. La riga regge.

### 1.3 Controllo SymPy indipendente (`ex10_b_nd.py`, 9/9 PASS)
- (1) L u_c = 0. (2) −iL = ∂_t − M con M ∈ B.
- (3) Gradi in α pari a 0, 1, …, 8, con testa (√2)^b. (3′) Passo induttivo con parte bassa generica.
- (4) Ricerca diretta di un annullatore in B: ordine ≤ 4, coefficienti polinomiali in (t,x) di grado ≤ 3, 50 incognite, e^{−2it} trattato come indeterminata. Solo la soluzione nulla.
- (4′) Lo stesso controllo **senza** usare la trascendenza: matrice dei valori di t^ix^j∂_x^bu in 70 punti casuali, a 40 cifre. Rango numerico pieno, σ_min/σ_max ≈ 1,1e-7/1,1e3, lontano dal rumore.
- (5)–(7) Kill-argument, vedi sotto.

### 1.4 Kill-argument
- *α_0 = 0.* u = e^{−x²/2 − it} è D-finita, con (∂_x + x)u = 0 e ∂_x + x ∈ B. L'ipotesi α_0 ≠ 0 è necessaria ed è dichiarata (controllo (5)).
- *Annullatori d'ordine 1 con coefficienti non polinomiali.* (∂_x + x − √2α(t))u = 0 esiste, ma il suo coefficiente sta in ℂ(x, e^{2it}) e non in ℂ[t,x]: non è in B, quindi non contraddice la tesi. È esattamente la dipendenza dall'anello segnalata in 1′ (controllo (6)).
- *Operatori misti con ∂_t.* Per VAR-C3Q2(a) ogni Q ∈ A_2 si riduce modulo A_2L a un resto in B. Controllo su Q = ∂_t∂_x: il resto è ∂_x∘M e non annulla u (controllo (7)). Nessun canale sfugge.
- *Dominio.* La tesi chiede Ω connesso (ipotesi della riga), che serve per il principio d'identità. Su Ω non connesso «D-finita» va letta componente per componente; la riga dichiara Ω connesso, quindi va bene.

Il kill-argument non trova nulla. **Verdetto: PASS (DIMOSTRATO).** Precisazioni facoltative per la stesura: (a) nominare il coefficiente di testa (√2)^b nell'induzione; (b) dire che per (b)–(c) di VAR-C3Q2 basta l'indipendenza dei soli ∂_x^bu.

---

## 2. EX10-e-K

### 2.1 Verifica riga per riga
Classe: ∂_tψ = Σ_jA_j∂_jψ + Bψ, con 144 incognite. Il nucleo di Φ_u è {(A, B) : Σ_jA_j∂_jψ + Bψ = 0}.

1. *Le 12 direzioni di vincolo stanno nel nucleo per ogni soluzione di Maxwell.* Σ_j(we_{E_j}^T)∂_jψ = w·div E, e lo stesso per B. L'applicazione (w_1, w_2) ↦ (w_1e_{E_j}^T + w_2e_{B_j}^T)_j è iniettiva, quindi la dimensione è 12. **Corretto** per ogni dato con div E = div B = 0, non solo EP (controllo (2)).
2. *Riduzione alle onde piane.* Su v e^{i(k·x − ωt)} la condizione è T(k)v = 0 con T(k) = iΣk_jA_j + B, indipendente da ω. Con i due rami e le due polarizzazioni i vettori v generano K(k) = {k·E = k·B = 0}, di dimensione 4. **Corretto.**
3. *«Il termine costante B si annulla su ∪_kK(k) = ℂ⁶».* Due difetti di stesura. Primo: per separare B dalla parte lineare bisogna usare K(λk) = K(k), cioè scalare k ↦ λk. Questo è lecito nell'enunciato «per ogni k» ed è implicito nel testo. Secondo, e qui serve il fix **K-1**: l'unione dei K(k) con k reale **non** è ℂ⁶. Per esempio ((1, i, 0), (0, 0, 1)) non sta in nessun K(k) con k reale non nullo (controllo (8)). Ciò che serve, e che è vero, è che lo **span** dei K(k) sia ℂ⁶. Basta perché B è lineare. Conclusione B = 0 corretta.
4. *«X è costante perché k·E e k·B sono lineari e coprimi».* Così com'è scritto è uno schizzo: a priori X(k) è solo razionale, omogenea di grado 0. Fix **K-2**, argomento corretto e breve: ogni riga di A(k) := Σk_jA_j è una forma bilineare β(k, (E, B)) = k^TcE + k^TdB che si annulla quando k·E = k·B = 0. Ponendo B = 0 si ottiene k^TcE = 0 per ogni E ⊥ k, quindi c = λI. Analogamente d = μI. Dunque la riga è λ(k·E) + μ(k·B) con λ, μ costanti, cioè X è costante. Conclusione corretta.
5. *Nucleo esattamente di dimensione 12, A_j = −i(w_1e_{E_j}^T + w_2e_{B_j}^T).* Corretto per la condizione **su tutti i k** (controlli (3), (3′): identità polinomiale T(k)Π(k) = 0 con Π(k) = |k|²I − diag(kk^T, kk^T), rango 132, B = 0, 12 parametri liberi nella forma dichiarata).
6. *«Il rango per insiemi sufficientemente generici di k è 132».* Il testo non spiega il passaggio dal «per ogni k» a un insieme finito di dati. Fix **K-3**. Per S finito, ker_S ⊇ ker_tutti, di dimensione 12. Le equazioni per un k dato sono polinomiali in k, perché K(k) è generato da prodotti vettoriali con k e non serve |k|. Quindi {S ∈ (ℂ³)^n : rango_S = 132} è un aperto di Zariski. È non vuoto per n ≥ 6: lo prova il calcolo esatto (controllo (4): ranghi 24, 48, 72, 96, 120, 132, 132 per n = 1…7). Ne segue «esattamente 12 per S generico con n ≥ 6». Per i 12 k specifici di S10-INT, e per i 12 k nuovi dell'audit, l'uguaglianza è un calcolo esatto (V-ex), e va detto così.
7. *Classe simmetrica: nucleo 0.* ESEMPI considera solo «we_{E_j}^T simmetrica». L'elemento del nucleo è w_1e_{E_j}^T + w_2e_{B_j}^T. Perché sia simmetrico per ogni j, w_1 e w_2 devono essere supportati su {E_j, B_j} per ogni j, quindi w = 0. Il completamento è immediato e la conclusione è corretta, per tutti i k (controllo (7′): rango 99 su 99) e per dati generici (controllo (6)). Maxwell sta nella classe simmetrica e risolve il sistema affine (controllo (6′)), quindi la soluzione è unica ed è Maxwell.

### 2.2 Controllo SymPy indipendente (`ex10_e_k.py`, 13/13 PASS)
Uso 12 quaterne pitagoriche **diverse** da quelle di S10-INT: (2,6,9), (6,6,7), (3,4,12), (2,10,11), (1,12,12), (8,9,12), (12,4,3), (9,2,6), (6,9,2), (7,4,4), (−3,4,12), (2,−10,11). Le polarizzazioni sono costruite con prodotti vettoriali. I ranghi sono calcolati con DomainMatrix su QQ, dopo la riparametrizzazione A′_j = iA_j, che non cambia il rango.

| controllo | esito |
|---|---|
| 48 onde piane, vincoli inclusi | PASS |
| classe generale: 288 equazioni, rango 132 | PASS |
| 12 direzioni nel nucleo per ogni soluzione (simbolico) | PASS |
| 12 direzioni = nucleo dei dati | PASS |
| tutti i k (identità polinomiale): rango 132, forma esplicita del nucleo | PASS |
| rango con n = 1…7 vettori k: 24, 48, 72, 96, 120, 132, 132 | PASS |
| un solo ramo: rango 132 con 12 k, 72 con 6 k | PASS (vedi kill) |
| classe simmetrica: 99/99; per tutti i k: 99/99 | PASS |
| legge vera simmetrica e soluzione del sistema affine | PASS |
| classe simmetrica con un solo k: rango 24/99 | PASS (vedi kill) |
| unione dei K(k) ≠ ℂ⁶ | PASS (vedi K-1) |

### 2.3 Kill-argument
- *Terza clausola della riga del LEDGER.* La riga EX10-e-K dichiara come ipotesi «dati di Maxwell con div E = div B = 0» e poi afferma «nella classe A_j = A_j^T il nucleo è 0». Per un dato di Maxwell qualsiasi questo è **falso**: con un solo k, su entrambi i rami, il rango nella classe simmetrica è 24 su 99 (controllo (7)), e per ψ = 0 il nucleo è tutto. Fix **K-4**: nella riga va scritto che la prima clausola vale per ogni dato di Maxwell, mentre la seconda e la terza valgono per onde piane su entrambi i rami con un insieme generico di n ≥ 6 vettori k (oppure per la condizione su tutti i k). Il testo di ESEMPI §5 rispetta già questa distinzione; la riga del LEDGER no.
- *«Su entrambi i rami».* Ho tentato di far cadere l'esattezza con un solo ramo. L'esattezza **non** cade: con 12 k e ω > 0 soltanto il rango è ancora 132. L'ipotesi dei due rami serve all'argomento, perché dà K(k) di dimensione 4 per ogni singolo k, ma non è necessaria al risultato: con un solo ramo servono più k (con 6 k il rango è 72). Non è un difetto. Lo segnalo perché l'enunciato con i due rami è più forte del necessario.
- *Dati non generici.* k tutti paralleli oppure n < 6 danno un nucleo più grande di 12. È coperto da «generici», a condizione di applicare K-3.

**Verdetto: PASS-con-fix.** Con K-1…K-4 l'argomento è completo e la riga passa a DIMOSTRATO.

---

## 3. EX10-e-H

### 3.1 Verifica riga per riga
1. *Cambio di base.* F = E + iB, G = E − iB, ψ = T(F, G) con T costante invertibile. Combinando le righe (E ± iB, div E ± i div B) con V costante invertibile si ottiene VPT = diag(P_F, P_G), a meno dell'ordine delle righe, con P_F = [τI + iC(ξ); ξ^T] e P_G = [τI − iC(ξ); ξ^T]. Verificato anche al livello degli operatori veri: F_t + i rot F = M_1 + iM_2 e G_t − i rot G = M_1 − iM_2, dove M_1, M_2 sono le equazioni di Maxwell. **Corretto.**
2. *N = 0.* Q_1 = P più le righe costanti di G, Q_2 = P più le righe costanti di F. Le due terne di righe costanti hanno insieme rango 6 su ℂ, quindi U_1 + U_2 = R^{1×6} e N = 0. **Corretto.**
3. *U_1 ∩ U_2 = U_P.* Nelle coordinate (F, G) i generatori di U_P sono a blocchi, quindi U_PT = U_{P_F} ⊕ U_{P_G}. Inoltre U_1T = U_{P_F} ⊕ R^{1×3} e U_2T = R^{1×3} ⊕ U_{P_G}, e l'intersezione è U_{P_F} ⊕ U_{P_G}. **Corretto.**
4. *Sol(P) = Sol(Q_1) ⊕ Sol(Q_2) su ogni Ω, con proiettori costanti.* π_1 = T diag(I, 0)T^{−1} e π_2 = T diag(0, I)T^{−1} soddisfano Pπ_i = W_iP con W_i costanti. Quindi mandano Sol(P) in sé, in 𝒞^∞ e in 𝒟′, su qualunque Ω. Valgono inoltre π_1 + π_2 = I, π_1π_2 = 0, G(π_1ψ) = 0 e F(π_2ψ) = 0. La somma è diretta perché Sol(Q_1) ∩ Sol(Q_2) ⊂ {F = G = 0}. **Corretto**, e non serve alcuna ipotesi topologica su Ω. Il richiamo a SYS-S1(i⇐) è coerente (caso N = 0, Ext¹(0, 𝒜) = 0 banalmente), ma non necessario: la scomposizione si ottiene direttamente dal cambio di base costante.
5. *Stessa varietà.* det(τI ± iC) = τ(τ² − |ξ|²). **Corretto.** È coerente con CONV-D1 («salvo fattori comassimali»): U_1 + U_2 = R^{1×6} vuol dire proprio comassimali.

### 3.2 Controllo SymPy indipendente (`ex10_e_h.py`, 10/10 PASS)
Controlli: livello degli operatori (1); V e T costruiti qui, con det V = 16 e det T = −i/8 (2); VPT a blocchi (2′); N = 0 (3); generatori a blocchi (4); proiettori e intrecciamento Pπ_i = W_iP (5, 5′); stessa varietà (6); due kill (7, 8).

### 3.3 Kill-argument
- *Scomposizione banale?* No. L'onda circolare F = (1, i, 0)e^{i(z−t)} sta in Sol(Q_1) ed è non nulla, e (1, −i, 0)e^{i(z−t)} come G sta in Sol(Q_2) (controllo (7)).
- *Elicità e segno della frequenza.* Ho verificato che l'elicità + contiene sia ω = +1 sia ω = −1 (k ↦ −k, controllo (8)). La scomposizione per elicità non coincide con quella per segno della frequenza. Quest'ultima, come dice ESEMPI, non è polinomiale. Nessuna contraddizione.
- *Ω non semplicemente connesso, 𝒟′.* I proiettori sono matrici costanti, quindi la conclusione non dipende né dalla topologia né dallo spazio funzionale. Il controesempio SYS-S1-C non si applica, perché lì N ≠ 0.

**Verdetto: PASS (DIMOSTRATO).**

---

## 4. Controllo a campione degli esempi V-ex

Ho rieseguito tre script di S10-INT (`ex10_a_dirac.py`, `ex10_b_oscillatore.py`, `ex10_e_maxwell.py`) con `python.exe -I` e ho confrontato riga per riga l'uscita con i `.out` salvati: **identiche**, 13/13, 19/19 e 17/17 PASS. Le affermazioni di ESEMPI corrispondono alle uscite:
- EX10-a: ranghi 2, 4, 6, 8; σ_min = 7,72e-2 con 4 modi; sei valori singolari < 1e-30 con 1 modo.
- EX10-b: gradi in α 0…5; γ = −tan t/2; U(π/2) = −i·parità.
- EX10-e: rango 132/144 e 99/99; VPT = diag(P_F, P_G); 48 onde piane.

Gli script `ex10_e_maxwell.py` e `ex10_b_oscillatore.py` sono anche confermati in modo indipendente dai miei, con dati diversi per Maxwell.

**Nota editoriale (non un fix degli argomenti auditati).** ESEMPI §5, passo 3b, cita SYS-MAXWELL come «PROVA SCRITTA (S10-OPEN-C §9)». Nel LEDGER (sezione degli esiti di audit, riga «SYS-MAXWELL (Q6)») risulta già **DIMOSTRATO** (PASS, C-13). L'indicazione di ESEMPI è prudente ma superata; conviene allinearla.

## 5. Testo dei fix

- **K-1** (ESEMPI §5, argomento EX10-e-K, seconda puntata). Sostituire «su ∪_kK(k) = ℂ⁶» con: «scalando k ↦ λk (K(λk) = K(k)) si separano B e la parte lineare; B si annulla su ogni K(k), e lo span dei K(k) è ℂ⁶; dunque B = 0».
- **K-2** (prima puntata). Sostituire l'argomento di coprimalità con: «ogni riga di Σk_jA_j è una forma bilineare k^TcE + k^TdB nulla per k·E = k·B = 0; con B = 0 si ha k^TcE = 0 per E ⊥ k, quindi c = λI; analogamente d = μI; dunque X è costante».
- **K-3** (terza puntata). Aggiungere: «la condizione per un singolo k è polinomiale in k, quindi rango_S = 132 è una condizione aperta di Zariski sugli insiemi S di n vettori; è non vuota per n ≥ 6 (calcolo esatto); per i 12 k dello script l'uguaglianza è V-ex». Completare la frase sulla classe simmetrica: «w_1e_{E_j}^T + w_2e_{B_j}^T simmetrica per ogni j ⇒ w_1 = w_2 = 0».
- **K-4** (LEDGER_ROWS, riga EX10-e-K). Ipotesi: «(i) ogni dato di Maxwell, div E = div B = 0; (ii)–(iii) onde piane su entrambi i rami con un insieme generico di n ≥ 6 vettori k». Non registrare «nucleo 0 nella classe simmetrica» per ogni dato di Maxwell, perché è falso (un solo k: rango 24/99).
