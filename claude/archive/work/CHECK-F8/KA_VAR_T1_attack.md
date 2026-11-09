# KA VAR-T1 — attacco (subagente indipendente, 27/10/2026)

Fonte letta: soltanto `work/CHECK-F8/KA_VAR_T1_input.md`. I controlli numerici e simbolici sono nello script `C:\Users\<user>\AppData\Local\Temp\claude\D--ProblemaBase\ad2c3e6b-182c-4434-a232-3d147636ed10\scratchpad\ka_attack\chk.py`, che si trova fuori dal progetto.

## Memo d'attacco

L'argomento più dannoso che sono riuscito a costruire non trova un errore nelle prove. Colpisce invece la portata dell'enunciato. VAR-T1(b) e (c) dichiarano come classe "V ∈ L^∞_loc" e presentano questa scelta come una generalità reale. Però l'ipotesi u ∈ C^{1,2} insieme a L_0u = Vu q.o. costringe V ad avere un rappresentante continuo ovunque u ≠ 0.

Ecco perché. Su un aperto U ⊂ {u ≠ 0} la funzione F := (iu_t + u_xx)/u è continua e coincide con V q.o. Nel caso V = V(x) di §1.4, F(t,x) − F(t′,x) si annulla q.o. in (t,t′,x) e quindi ovunque, per continuità. Allora V coincide q.o. con una funzione continua su J ∖ X_0, e X_0 è discreto per (i). In (c) lo stesso ragionamento dà V = F q.o. su {u ≠ 0}.

Ne segue che la parte "L^∞" del teorema è in gran parte solo nominale. Per un V genuinamente ruvido, per esempio V = 1_C con C un Cantor grasso, non esiste nessuna soluzione u ≢ 0 di classe C^{1,2}, e (b) vale per vacuità. La classe effettiva è "V continuo fuori da un insieme discreto X_0, sui cui punti u(·,x) ≡ 0".

C'è un secondo punto debole, in (c). Il criterio L^∞ "identificato ⟺ |Z(u)| = 0" di (c)(i) non è ricondotto alle fasce di silenzio. (c)(ii) copre solo il caso int Z(u) ≠ ∅ e lascia aperto il caso di uno Z(u) di misura positiva con interno vuoto.

Ho rifatto a mano e verificato numericamente i passi tecnici: il commutatore (§1.3, VAR-L0 (i)), l'assorbimento del termine incrociato, la lente e il cut-off di VAR-L1, la compattezza di VAR-L2, l'estensione per zero di (b)(i), la stima di Cauchy su g^{(k)} e la serie di Tychonoff. Nessuno di questi cede. Non ho trovato nessun controesempio all'enunciato.

## Punti d'attacco atomici

**A1. Identità del commutatore (VAR-L0 (i)).**
- Accusa: c'è un segno sbagliato nel termine incrociato 4λφ_xt Im(z_x z̄), oppure nella decomposizione P_λ = S + A.
- Conto tentato:
  - Ho rifatto a mano tutti i commutatori: [∂_x², −2λφ_x∂_x − λφ_xx], [∂_x², −iλφ_t], [λ²φ_x², −2λφ_x∂_x], [i∂_t, ·]. Coincidono riga per riga con quelli del testo.
  - Ho verificato l'integrazione per parti: −4λ∫φ_xx z_xx z̄ dà 4λ∫φ_xx|z_x|² + 4λ∫φ_xxx z_x z̄, che cancella il termine −4λφ_xxx∂_x. La parte reale di −4iλφ_xt z_x z̄ cancella −2iλφ_xxt.
  - Ho controllato che S è simmetrico e che A è antisimmetrico.
  - SymPy conferma P_λ − S − A = 0. Per una φ generica con φ_xt, φ_xxxx ≠ 0 e una z complessa a decadimento gaussiano, ho ottenuto ‖Pz‖² = 35.031033 e ‖Sz‖² + ‖Az‖² + q(z) = 35.031033. Col segno opposto del termine incrociato il valore è 30.63.
- Esito: fallito.
- Severità: nessuna.

**A2. Stima di Carleman e soglia λ_0 (VAR-L0 (ii)–(iii)).**
- Accusa: l'assorbimento non basta, oppure la densità, cioè il passaggio da C_c^∞ a w ∈ C_c con w_t, w_x, w_xx continue, non è lecita.
- Conto tentato:
  - Su |s| ≤ b si ha φ_x = −1 + 2μs ∈ [−3/2, −1/2] e φ_xx = 2μ.
  - Per AM-GM vale 4ab ≤ 8μa² + b²/(2μ), perché 2·√(8μ/(2μ)) = 4. Il termine incrociato consuma tutto 8λμ|z_x|², che resta comunque ≥ 0.
  - Risulta q ≥ (2μλ³ − λC_1)‖z‖² ≥ μλ³‖z‖² per λ² ≥ C_1/μ.
  - La mollificazione è corretta: L_0w è continua a supporto compatto, quindi L_0w_ε → L_0w uniformemente.
- Esito: fallito.
- Severità: nessuna.

**A3. Lente, cut-off ed estensione per zero (VAR-L1).**
- Accusa: w = χ(φ)u non è C^{1,2} attraverso s = 0, oppure il supporto non è compatto in int B, oppure R non è separato dal peso.
- Conto tentato:
  - Su s ∈ [0,b] si ha μs² ≤ s/4, quindi sulla lente φ ≥ −2ε forza s ≤ 8ε/3 e |t − t_0| ≤ √(2ε). La lente sta in int B.
  - u è C^{1,2} ed è nulla per s < 0, quindi u, u_x, u_xx, u_t si annullano per continuità su s = 0.
  - Ho ricalcolato L_0(χ(φ)u) = χL_0u + R: la formula di R è esatta.
  - Su supp R si ha φ ≤ −ε, mentre su Λ = {φ ≥ −ε/2} vale w = u oppure u = 0.
  - Il confronto ½(μλ³)^{1/2}e^{−λε/2}‖u‖_{L²(Λ)} ≤ e^{−λε}‖R‖ forza u = 0 su Λ.
- Esito: fallito.
- Severità: nessuna.

**A4. Globalizzazione e compattezza (VAR-L2).**
- Accusa: il sup s* non è raggiunto, oppure il grafico tocca il bordo di Ω, oppure gli estremi del grafico non stanno in W.
- Conto tentato:
  - ∪_{s<s′}R_s = R_{s′} perché ψ > 0 su T, quindi u = 0 su R_{s*}.
  - I punti interni del grafico stanno in W per VAR-L1: un piccolo intorno ∩ {x < g} sta in R_{s*}, dato che φ_{s*} ≥ β > α.
  - Gli estremi (t_1 − δ, β) e (t_2 + δ, β) stanno in W per il passo 0, perché [t_1 − δ, t_2 + δ] ⊂ I. La chiusura del grafico è quindi un compatto dentro W, ed esiste un η-intorno.
  - Per s − s* < η si ha 0 ≤ φ_s − φ_{s*} < η, dunque R_s ⊂ R_{s*} ∪ (η-intorno).
  - Il grafico sta in Ω perché b″ < sup J.
  - La riflessione x ↦ −x conserva L_0.
- Esito: fallito.
- Severità: nessuna.

**A5. Scope overclaim della classe L^∞_loc (VAR-T1(b), (c)(i)).**
- Accusa: la classe dichiarata promette più di quanto la coppia di ipotesi permetta.
- Conto tentato:
  - Su {u ≠ 0} la funzione F = (iu_t + u_xx)/u è continua e coincide con V q.o.
  - In (b), F risulta indipendente da t, perché una funzione continua che è q.o. uguale a una funzione indipendente da t lo è ovunque. Quindi V ha un rappresentante continuo su J ∖ X_0, con X_0 discreto.
  - Conseguenza verificata logicamente: per V = 1_C con C un Cantor grasso, su ogni componente di J ∖ X_0 la funzione 1_C dovrebbe essere q.o. costante. Il valore 1 è escluso, perché C non è denso da nessuna parte. Allora |C ∩ componente| = 0 per ogni componente, quindi |C| = 0: contraddizione. Dunque l'unica soluzione è u ≡ 0, e il teorema è vacuo per V di questo tipo.
  - Le discontinuità di V sono ammesse solo nei punti di X_0. Ne ho verificato un esempio: con V a gradino in x_1 e h″ = (V − E)h, h(x_1) = 0, si ottiene h ∈ C², perché il salto di h″ è [V]·h(x_1) = 0.
- Esito: riuscito come rilievo di portata. Non è un controesempio, perché l'enunciato resta vero.
- Severità: maggiore (presentazione e portata). La classe va riscritta come "V ∈ L^∞_loc; necessariamente V è continuo fuori da X_0".

**A6. Riduzione alle fasce di silenzio nel caso L^∞ (VAR-T1(c)(i)–(ii)).**
- Accusa: nella classe L^∞ la non-identificabilità equivale a |Z(u)| > 0, ma (ii) tratta solo int Z(u) ≠ ∅. Resta scoperto il caso di uno Z(u) chiuso, di misura positiva e con interno vuoto. In quel caso V non è identificato e non c'è, almeno a priori, nessuna fascia di silenzio.
- Conto tentato: nei punti di densità di Z valgono u = u_x = u_t = 0 e, per l'equazione, u_xx = 0. Da questo non ho ottenuto né una contraddizione né un esempio. Servirebbe una continuazione unica da insiemi di misura positiva per Schrödinger con V ∈ L^∞, e l'input non la fornisce.
- La prova di (ii) è corretta: il quadrato di semilato r/2 sta nella palla di raggio r, e T′ ⊂ I.
- Esito: candidato da verificare. L'enunciato non afferma il falso, ma il titolo "fasce di silenzio" suggerisce un'equivalenza che vale solo nella classe C(Ω).
- Severità: maggiore come lacuna di portata, minore come correttezza.

**A7. Serie di Tychonoff: convergenza, C^∞ in t = 0, equazione (VAR-T1(c)(iii) e §7.1).**
- Accusa: la stima su g^{(k)} è falsa, oppure le derivate non tendono a 0, oppure la serie non risolve L_0u = 0.
- Conto tentato:
  - Stima di Cauchy. Il disco |z − t| ≤ t/10 evita lo 0. |(1+ζ)^{−2} − 1| ≤ Σ(n+1)θ^n = (1−θ)^{−2} − 1 ≈ 0.235 < 1/2, quindi Re(z^{−2}) ≥ t^{−2}/2. Il controllo numerico con mpmath per t ∈ {0.2, 0.5} e k ∈ {1, 3, 6, 10} rispetta sempre la stima, con margini ampi.
  - Maggiorante della serie: exp(x²/(θt) − 1/(2t²)) → 0.
  - Derivate in t: con (k+j)! ≤ 2^{k+j}k!j! il maggiorante è j!(2/(θt))^j exp(2x²/(θt) − 1/(2t²)), che tende a 0.
  - Derivate in x: ∂_x^{2n}u = (−i∂_t)^n u; per le derivate dispari compare un fattore 2k, assorbibile.
  - Equazione: u_xx = Σ(−i)^{k+1}g^{(k+1)}x^{2k}/(2k)! = −iu_t, quindi iu_t + u_xx = 0.
  - Il valore u(1/2,1/2) ≈ 0.01066 − 0.03653i, riprodotto, è ≠ 0.
  - Rilievi minori:
    - l'incollamento C^∞ in t = 0, cioè che tutte le derivate tendano a 0 uniformemente in x e che quindi l'estensione per zero sia C^∞, è dato per noto senza il lemma del valore medio;
    - il caso delle derivate x dispari e quello delle derivate miste sono solo accennati.
- Esito: fallito.
- Severità: minore (dettaglio di scrittura).

**A8. Dettagli formali di (a) e (b)(iii).**
- Accusa: le convenzioni sono incoerenti.
- Rilievi:
  - In (b)(ii) si applica (a) con L_θ = L_0 + θ·1. Allora L_θu = 0 significa L_0u = −θu: il segno di V è invertito rispetto a θ. Questo non ha effetto su V − W.
  - ρ_u non è definito nell'estratto.
  - In (a), ker Φ_u = {0} va inteso modulo q.o. per Θ = L^∞.
  - In (b)(iii) la formula "per ogni t con u(t,x) ≠ 0" vale per il rappresentante continuo di V di cui parla A5. Scritta "q.o. in x" è ambigua.
- Esito: riuscito come rilievo formale.
- Severità: minore.

## Esito finale

**SURVIVES**, con un rilievo di portata maggiore (A5) e una lacuna di portata da segnalare nell'enunciato (A6).

Non ho trovato nessun passo falso, nessun errore di segno e nessun controesempio contro VAR-L0, VAR-L1, VAR-L2, VAR-T1(a), (b) e (c). Raccomando di dichiarare esplicitamente due cose:
- che la classe "V ∈ L^∞_loc con u ∈ C^{1,2}" forza V a essere continuo fuori da X_0 (in (b)) e su {u ≠ 0} (in (c));
- che nel caso L^∞ di (c) l'equivalenza tra non-identificabilità e fasce di silenzio è dimostrata solo sotto int Z(u) ≠ ∅.
