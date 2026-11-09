# TRIAGE dei problemi APERTI di CHIUSURA_F10 §3 (valutatore indipendente, 27–28/10/2026)

**Fonti consultate.**
- `CHIUSURA_F10.md` §3.
- `claims/LEDGER.md`: sezione Fase 10 (righe 385–543) e righe precedenti con lo stesso ID.
- `work/S10-OPEN-{A,B,C}/PROOF_PACKAGE.md` e i relativi `open_questions.md`.
- `work/CHECK-F10/AUDIT_*.md`.
- `research/CIT-AUDIT/{AUDIT-F5,AUDIT-GTU}.md`, `BIBLIOGRAFIA.md`, `research/CIT-AUDIT/sources_verified.bib`.

**Script nuovi.** Stanno in `work/CHECK-F10/triage_scripts/`: `tri_delta.py`, `tri_p1q7.py` e le uscite `*.out`. Non ho modificato nessun altro file.

**Classi.**
- **(A) CHIUDIBILE ORA**: un'azione concreta e limitata.
- **(B) PROBLEMA DI RICERCA APERTO**: nessuna strada nota.
- **(C) RICHIEDE FONTI** non disponibili offline.

**Fonti offline: verifica.** I soli PDF del progetto, fuori da `_vendor`, sono gli elaborati del progetto stesso:
- `PAPER/*.pdf`, `PAPER_EXPLAINED/*.pdf`, `FASI05/*.pdf`, `VOLUMES/Punto_di_partenza.pdf`, `NOTE_ML/*.pdf`.

Non c'è nessun testo di letteratura: niente PDF, djvu o txt di articoli. `BIBLIOGRAFIA.md` e `sources_verified.bib` contengono solo metadati (DOI, stato della citazione). In `_vendor` ci sono solo PDF estranei (skill e tutorial), che non ho aperto né eseguito.

Quindi ogni fonte indicata sotto come «non letta» **non è disponibile localmente**. Per alcune chiavi la ricerca nei metadati non trova nulla:
- Amitsur, Matveev–Salle, Bagrov–Samsonov, Braess e Tataru non compaiono né in BIBLIOGRAFIA né nel .bib.
- Oberst 1993 e Björk 1979 compaiono solo come metadati, con stato «VERIFICATO (abstract)» e «VERIFICATO-K».

---

## 1. Voci «con riduzione o condizione provata»

### P1-Q7: algebre con (H) senza (Dil)
**Classe: A per il candidato dichiarato, B per l'enunciato generale.**

Il pacchetto indica come caso test del residuo X = (x³+x)∂, Y = ∂ in A₁, con «(H) da verificare». Ho verificato tre fatti:

1. **(H) vale.** Y_k = ad_X^kY = p_k(x)∂ ha grado 2k e lo stesso coefficiente direttore del caso x³∂, cioè Π_{j<k}(2j−3) ≠ 0. Quindi X, Y_0, Y_1, … sono indipendenti (`tri_p1q7.out`, TUTTO OK).
2. **Il candidato si chiude con una variante di S10A-T2, la «dilatazione filtrata».**
   - L'automorfismo σ_μ: x ↦ μx, ∂ ↦ ∂/μ dà σ_μX = μ²(x³∂ + μ⁻²x∂) e σ_μY = μ⁻¹∂.
   - Con t = ν²s, ν = 1/μ, si ottiene e^{s(x³∂ + ν²x∂ + ε₀ν³∂)} = Π e^{h_i Z_i(ν)}.
   - I fattori X portano solo potenze **pari** di ν, sia nei coefficienti g_{i,k}ν^{2k−2} sia nel termine ν²x∂. I fattori Y portano potenze dispari ν^{2k+1} ≥ ν³.
   - Il Passo 1 di S10A-T2 (identità polinomiale in ν, μ infiniti) vale invariato, in un sottospazio di dimensione finita di A₁.
   - Il Passo 2 vale modulo ν³. I fattori X condividono X_ν, quindi commutano, e si ottiene H ≡ s.
   - All'ordine ν³ non c'è contaminazione da x∂, perché un termine ν³ non si può ottenere dai pari. L'equazione è esattamente quella del Passo 3 di S10A-T2 per la coppia omogenea (x³∂, ∂).
   - Per questa coppia (H) vale (P1-T5, esempio L4, a = 3). Il Passo 4 (Hankel/Hilbert) dà la contraddizione.
3. **Conseguenza.** Per (x³+x)∂, ∂ non esiste nessuna parola finita a nessun ε₀ ≠ 0. Le condizioni sufficienti generalizzano (Dil):
   - σ_μX = μ^α(X₀ + Σ_j μ^{−c_j}X_j), σ_μY = μ^βY₀;
   - 𝔞 = α−β fuori dal semigruppo generato da {c_j, α};
   - (H) per la coppia graduata (X₀, Y₀).

   È un'**abbozzo di prova del valutatore, non auditato**: va scritto e sottoposto ad audit, il che richiede qualche ora.

**Cosa resta aperto (B).** Le algebre con (H) prive di qualunque dilatazione, anche filtrata. Non c'è nessun esempio e nessuna strada: il meccanismo di S10A-T2 usa la simmetria in modo essenziale per spegnere i flussi di Y. Servirebbe un'idea nuova, per esempio la rigidità della Hankel ordine per ordine in ε₀, che il pacchetto propone ma non tenta.

### C12-Q2 = OPF-Q2
**Classe: B.**

L'enunciato astratto è falso in Hilbert (C12-P7(d)), quindi una prova deve usare la struttura differenziale. S10A-C2 restringe la ricerca alle terne con almeno due coppie a interazione non compatta, ma nessuna famiglia candidata è stata analizzata.

Il passo successivo indicato nel pacchetto è finito: compattezza di Π_iΠ_j per coppie ellittiche ∂_z̄−λ, ∂_z−μ e per coppie con la stessa caratteristica reale. Non decide però la domanda, perché la compattezza di tutte le coppie tranne una esclude il controesempio solo in quella famiglia. Non c'è nessuna strada verso un teorema generale.

### OPF5C-Q1: caso graduato (limiti inferiori graduati per N generale)
**Classe: B per N generale.**

È una congettura di algebra commutativa graduata: assenza di relazioni omogenee di grado ≤ N, N+1, N+3 sulle varietà Z₀ per tutti gli N. Non c'è nessuna struttura nota, per esempio una successione regolare o una risoluzione esplicita, che dia il limite per ogni N.

Per N fissato il problema è finito; per i casi nuovi vedi S10B-V9 (§2). Il mio generatore di punti Adler–Moser (AM) rende il caso N = 6 eseguibile in pochi minuti, invece di più di 3,5 ore.

### OPR2-Q3: realizzabilità degli atomi
**Classe: B.**

S10B-P10 è una caratterizzazione esatta: insieme colpitore finito o ¬(I). La realizzabilità degli atomi è solo sufficiente. La domanda aperta è se 𝓛 possa avere un insieme colpitore finito pur con infiniti atomi, con zoccolo ripetuto e M non spezzato su 𝔇.

Non c'è nessun esempio e nessuna strada. Servirebbe una teoria dei sollevamenti di endomorfismi di M_P a 𝔇, che nel progetto non c'è.

### OPR2-Q2′: condizione sufficiente (L-v) a ogni vertice
**Classe: A per (L-int), B per (L-v). Nel complesso B.**

- **(L-int).** È la compattezza di P_iχ₀²P_j lontano dai vertici. È di fatto un calcolo finito: con d_j = 0 i nuclei sono funzioni di n_j^⊥·x, e P_iχ₀²P_j ha nucleo integrale esplicito con norma di Hilbert–Schmidt ∫χ₀⁴/(|sin θ|ℓ_iℓ_j). È finita perché le corde corte del poligono convesso stanno vicino ai vertici, dove χ₀ = 0.

  L'audit ha già il controllo numerico (`b2_p11_lint` 7/7, triangolo entro il 2.5%). Basta scrivere la stima, inclusi d_j ≠ 0 (fattore e^{−d_j τ} limitato) e le direzioni parallele a un lato. Lo stimo in poche ore.

  Dopo questo passo OPR2-Q2′ diventa una **vera riduzione** alla sola (L-v).
- **(L-v).** È il trasferimento del modello del cono (OPF5B-P8) al poligono. L'errore (n_j·∇χ_v)f_j non è compatto in modo ovvio, perché i nuclei sono infinito-dimensionali anche localmente. Serve un'analisi microlocale o di scaling al vertice, che non esiste nel progetto: B.

### INT-Q1: equivalente a (R), mod S4ID-P8, [GT-u_m], (WP)
**Classe: B, con una dipendenza C a monte.**

Per escludere (R) servono i termini **sottodominanti** dell'asintotica radiativa di KdV (correzioni t^{−1/2}log t, fase di Deift–Zhou). Il caso test, la relazione cubica di Airy (OP-O5), ha in(G) ∈ I_PW, quindi l'ordine dominante non basta per costruzione.

Anche con le fonti (Deift–Zhou 1994, CMP 165) servirebbe un lavoro nuovo di asintotica d'ordine superiore con controllo delle derivate. Non c'è nessuna strada breve.

### [GT-u₀]: costanti di Hölder (5.20)–(5.21) e ε del disaccoppiamento
**Classe: C, che diventa A dopo la lettura.**

AUDIT-GTU dice che la clausola d'uniformità di GT Thm 5.1 («uniform with respect to this parameter», via Krüger–Teschl) copre quasi tutto. Restano due cose:
- la limitatezza in k₀ ∈ compatto delle costanti L di (5.20)–(5.21);
- la ε di Thm 5.2.

È plausibilmente un argomento di continuità: R è C⁵ e |R(k₀)| ≤ ρ < 1 sui compatti. Si scrive però solo con il testo di GT §5 (arXiv:0807.5041v2, pp. 18–24) e di Krüger–Teschl (il riferimento [25] di GT) davanti. Nessuno dei due è nel progetto: AUDIT-GTU li ha letti online e non li ha salvati.

Con le fonti a disposizione stimo qualche ora di riscrittura con costanti esplicite.

### [GT-u_m]: derivate in x (GT Remark 5.5, «formally»)
**Classe: C, poi probabilmente B.**

La giustificazione è rimandata a Deift–Zhou, CMP 165 (1994) 175–191, e c'è un candidato alternativo in Buslaev–Sukhanov 1986. Nessuno dei due è disponibile: in BIBLIOGRAFIA c'è solo DeiftZhou1993 [VN]. Senza fonte la derivazione termine a termine di un'asintotica di steepest descent non è un lavoro breve.

---

## 2. Voci «senza riduzione»

### P2-Q1-NL: domini non lipschitziani
**Classe: A per il caso modello, B in generale.**

**Caso modello chiudibile ora.** P = Δ (Q₁ = ∂_z̄, Q₂ = ∂_z), m ≥ 1, Ω limitato semplicemente connesso con disuguaglianza di Poincaré. Questo include il **disco con fessura**, cioè l'esempio esplicito del residuo. In questo caso ker_{H^m}Δ = 𝓗₁ + 𝓗₂ come insiemi, cosa più forte della densità.

*Prova.*
1. Sia h ∈ ker_{H^m}Δ. Allora h_z è olomorfa.
2. Ω è semplicemente connesso, quindi h_z ha una primitiva f, e h − f è antiolomorfa.
3. f′ = h_z ∈ H^{m−1}, e per Poincaré ‖f − f_Ω‖_{L²} ≤ C‖∇f‖_{L²}. Quindi f ∈ H^m, e anche h − f ∈ H^m.
4. Per il disco con fessura D ∖ [0,1) la disuguaglianza di Poincaré è elementare. Si ricopre con tre convessi: il semidisco superiore, quello inferiore e D ∩ {Re z < 0}, a due a due sovrapposti in insiemi di misura positiva. Poi si concatenano le medie.

Va scritto e auditato: meno di un'ora.

**Cosa resta (B).**
- P generale, per esempio fattori ellittici con λ ≠ 0, oppure iperbolici o di trasporto, dove le traslazioni del Passo 2′ falliscono.
- m = 0.
- Domini senza Poincaré, per esempio «stanze e corridoi».

Per P generale non c'è nessuna strada.

### P2-Q1-COD: codimensione esatta per P generale
**Classe: B.**

Servono funzionali «di periodo» continui in H^m che separino ker ι (OPF-T4) dalla chiusura. Per Δ c'è il flusso, ma per P generale non c'è nessuna costruzione: bisognerebbe rappresentare H¹ di de Rham a coefficienti nel complesso di P con classi in H^m, e qui manca una teoria.

### C12-Q1: chiusura della somma per (τ−ξ²)(τ+cξ)
**Classe: B, con una strada indicata.**

La densità è DIMOSTRATA (OPR2-T1). Per la chiusura la via naturale è OPR2-L1: compattezza di Π_caloreΠ_trasporto in H^m sul rettangolo.

Euristica del valutatore:
- le soluzioni di trasporto oscillanti e^{in(x−ct)} hanno correlazione normalizzata O(1/n) con gli strati iniziali del calore;
- con gli strati laterali (larghezza ω^{−1/2}) la correlazione è O(ω^{−3/4}).

Questo suggerisce che il prodotto sia compatto e la somma chiusa. Servono però stime rigorose degli strati di bordo del calore sul rettangolo: un lavoro di più giorni, non un calcolo finito. Lo considero ricerca, con una strada plausibile.

### VAR-Q18: moltiplicazioni
**Classe: B.**

- Per W(x) liscio (multiplicatore limitato su D(H₀)), U(t,0) preserva D(H₀) qualunque sia la regolarità di v(t): punto fisso in D(H₀).
- Per V indipendente dal tempo, D(H₀+V) = D(H₀) per Kato–Rellich.

Un controesempio, se esiste, deve combinare W ruvido in x e v(t) solo continuo, per esempio V = v(t)W(x). Il primo ordine di Dyson, Σ_n(∫v(r)e^{irλ_n}dr)g_n, suggerisce che con v Hölder lacunare e W ruvido si esca da D(H₀). Bisogna però controllare l'intera serie, ed è possibile una cancellazione con gli ordini superiori.

È una strada plausibile ma non breve, e nessuna fonte del progetto la copre.

### VAR-Q17(b), riformulato
**Classe: C, poi probabilmente A o B.**

Si tratta della continuazione unica laterale per i∂_t + ∂_x² − V(t,x) con V ∈ L^∞, per soluzioni miti. La letteratura delle stime di Carleman per Schrödinger con potenziali dipendenti dal tempo è quella pertinente:
- Baudouin–Puel 2002 (Inverse Problems);
- Lasiecka–Triggiani–Zhang 2004;
- Mercado–Osses–Rosier 2008;
- Tataru (coefficienti parzialmente analitici, che qui però non bastano perché V non è analitico in t).

Tutti questi lavori richiedono di regola soluzioni H¹ in t; poi serve un argomento di dualità o in H^{−1}_t. Nessuna di queste fonti è nel progetto: Isakov compare nel .bib solo come metadato.

Non so se il risultato sia già in letteratura per soluzioni miti. Finché non si leggono le fonti, C.

### VAR-P12(d), caso generale
**Classe: B.**

Il risultato quadratico (tr M = −26/5) esclude solo i logaritmi quadratici. Osservazione del valutatore: per un metaplettico con monodromia −e^{Ξ} (Ξ iperbolico) si ha U = Π·e^{−iTQ}, con Π la parità che commuta con Q.
- Il logaritmo **non locale** K′ = Q + (π/T)·P_dispari esiste.
- Ogni operatore differenziale che commuta con le dilatazioni è un polinomio in x∂, e non distingue la parità.

Quindi nella classe che commuta con Q non c'è un log differenziale. Il caso che non commuta resta aperto e non c'è un'ostruzione per ordini ≥ 3.

### VAR-C3Q2-open (caso non monico) e VAR-Q13
**Classe: B.**

Senza monicità manca la decomposizione A₂ = A₂L ⊕ ⊕B∂_t^j, e l'equivalenza della prima versione è stata ritirata. Bisognerebbe calcolare la saturazione A₂ ∩ D_BL e un rango effettivo. Non c'è nessuna strada nota, ma è un problema algebrico ben posto.

### SYS-DIRAC-POL a tempi complessi
**Classe: A (abbozzo di prova completo del valutatore, da auditare).**

**Lemma E′ («ordinamento per crescita»).** Siano R_j ∈ ℂ[ξ] con R_i − R_j non costante per i ≠ j, e siano d_j non tutti nulli. Sia S(ξ) = Σd_je^{iR_j(ξ)}, con ξ → +∞ reale.

1. Le differenze Im R_j − Im R_k sono polinomi reali, quindi costanti oppure tendenti a ±∞. Si ordinano le classi e si prende la classe dominante J₀, cioè quella con −Im R massimo, tra gli indici con d_j ≠ 0.
2. In J₀ le parti immaginarie differiscono per costanti, quindi le Re R_j hanno differenze non costanti.
3. Per il Lemma E (reale) applicato a S·e^{Im R_{j₀}}, che è uguale alla somma su J₀ più o(1), la media quadratica di S·e^{Im R_{j₀}} su [X,2X] tende a Σ_{J₀}|d′_j|² > 0.
4. Di conseguenza |S|, in media quadratica, è comparabile con e^{−Im R_{j₀}}. Ci sono tre casi:
   - (i) Im R_{j₀} costante: allora S non tende a 0;
   - (ii) Im R_{j₀} → −∞: allora S esplode;
   - (iii) Im R_{j₀} → +∞, polinomialmente con grado ≥ 1: allora |S| ≤ Ce^{−cξ}, cioè S decade esponenzialmente.

**Prova della tesi.** Si applica il lemma a G = W₁₁ − e^{iξt}, che ha questa forma perché e^{pX} ed e^{qmY} sono combinazioni di e^{±iξp(ξ)} ed e^{±iq(ξ)m}.
- Dall'asintotica del pacchetto, G ~ i(m²t/2ξ)e^{iξt}: G → 0 in modo **solo algebrico** e G ≢ 0.
- Questo esclude i tre casi (i)–(iii) e anche il caso G ≡ 0, che contraddirebbe l'asintotica.

Quindi non esistono tempi polinomiali complessi. Resta da scrivere e auditare: meno di 2 ore.

### ENC-Q4: lettura DM3
**Classe: B.**

Il caso naturale successivo è ENC-P0 con encoder W(t) dipendenti dal tempo, per le classi con fasce di silenzio. Prima va **definita** la classe degli encoder ammessi, che è una scelta di modello del coordinatore. Poi è un problema nuovo. Nessuna strada.

### ENC-Q10: residuo con V reale, riformulato
**Classe: C, più una decisione di modello.**

Darboux dipendente dal tempo con V₁ reale e regolare richiede le trasformazioni con coppie di soluzioni, del tipo V₁ = V₀ − 2∂²log W(u,ū). Le fonti pertinenti sono:
- Matveev–Salle, *Darboux Transformations and Solitons* (1991);
- Bagrov–Samsonov, Phys. Lett. A (1996/97), Darboux dipendente dal tempo per Schrödinger.

Nessuna delle due è nel progetto: nessun risultato in BIBLIOGRAFIA o nel .bib. Va anche deciso se la dipendenza dalla storia è ammessa in 𝔈.

### DICT-U3d-v: ottimalità
**Classe: C, con parte B.**

Per approssimanti con J esponenziali **arbitrari** la letteratura dell'approssimazione con somme di esponenziali dovrebbe mostrare che, per k = t^{−β}, l'errore decade come exp(−c√J) o meglio, quindi molto più veloce di τ_k(Λ_J) ~ J^{β−1}:
- Braess, *Nonlinear Approximation Theory* (1986);
- Braess–Hackbusch (IMA J. Numer. Anal. 2005).

Se è così, la dipendenza da τ_k **non** è necessaria nella forma attuale per i nuclei a potenza. Lo ricordo a memoria e va verificato sulla fonte, che non è nel progetto. Un limite inferiore uniforme su tutta la classe dei nuclei completamente monotoni normalizzati resta comunque una domanda di ricerca (B).

### DICT-Q3(c), riformulato come divisione C^∞
**Classe: B.**

È la definizione riletta, e il controesempio (b) mostra che il test formale più quello puntuale non bastano. Per u solo C^∞ con rango variabile non esiste un criterio generale. Servirebbero ipotesi di tipo Łojasiewicz o quasi-analitiche, un tema di ricerca aperto. Il caso analitico (a) è C (Malgrange, vedi §3).

### S10B-V9: N = 5 non riprodotto, N = 6 non eseguito
**Classe: A, tentata. Risultato: riprodotto in modo indipendente e N = 6 calcolato.**

**Script.** `triage_scripts/tri_delta.py` non usa `opf5c_gd.pkl` né `s10b_delta.py`, e lavora con il primo p = 2³¹−1, diverso da quello del pacchetto. Rango pieno mod p della matrice di valutazione, che è la riduzione di una matrice razionale, implica rango pieno su ℚ, quindi nessuna relazione. Ha due generatori di punti indipendenti:
- **(H) Hirota.** Getti y_j = ∂^ju(0) con u = 2∂²log f, f = Σ_S a_S e^{(Σ_S k_i)x}, k interi fissati, a casuali mod p. È rigoroso per **quel** k e non usa né L8 né L8′.
- **(AM) Adler–Moser.** Getti di 2∂²log θ_N al livello k = 0, famiglia omogenea pesata, controllo peso per peso. Vale come limite su Z₀ sotto l'ipotesi, plausibile ma **non dimostrata qui**, che i getti AM generici stiano nella chiusura dello strato principale S°₀ di M₀. La validazione indiretta è la coincidenza esatta con tutti i valori noti.

**Validazione** (`tri_delta_small.out`):
- (H), N = 1..4: rango pieno al grado ≤ N e nullità N+1 al grado N+1, con k = (1), (1,2), (1,2,4), (1,2,3,5).
- (AM): grado minimo N+1 per N = 1..4.
- I valori coincidono con il pacchetto.

**Risultati.**

| caso | metodo | esito | tempo |
|---|---|---|---|
| N=5, K=10 | AM graduato, d ≤ 6 | grado minimo di una relazione = **6** (peso 12) ⇒ δ₅(10) ≥ 6; con OPR2-P4 **δ₅(10) = 6** | 26 s (contro 3231 s del pacchetto) |
| N=5, K=9 | AM, d ≤ 7 | grado minimo **7** (peso 14): riproduce δ₅(9) = 7 | 88 s |
| N=5, K=8 | AM, d ≤ 8 | **nessuna relazione di grado ≤ 8** ⇒ δ₅(8) ≥ 9; con OPF5C-P7(b) **δ₅(8) = 9** | 161 s |
| N=6, K=12 | AM, d ≤ 6 | **nessuna relazione di grado ≤ 6** ⇒ δ₆(12) ≥ 7; con OPR2-P4 **δ₆(12) = 7** (congettura N+1 confermata per N = 6) | 195 s |
| N=5, K=10 | Hirota, k=(1,2,3,5,7), d ≤ 5 (4368 monomi) | **non concluso**: run interrotto (stima circa 17 min, oltre il budget residuo) | — |
| N=6, K=11 | AM, d ≤ 7 | **non concluso** (interrotto) | — |

**Stato proposto.**
- δ₅(10) = 6 e δ₅(8) = 9 sono **riprodotti** da un'implementazione indipendente, mod L8/L8′ e l'ipotesi AM ⊂ cl(S°₀).
- δ₆(12) = 7 è **nuovo**, con le stesse dipendenze.
- Per arrivare a DIMOSTRATO (computer-assisted) mancano tre cose:
  - (a) una dimostrazione che i getti AM stanno in cl(S°₀). Strada: AM = soluzioni razionali, corrispondenti al livello λ^{2N+1}, con U a radici distinte e non nulle per parametri generici; verificabile anche numericamente calcolando U da un getto;
  - (b) la conclusione del run Hirota N = 5 (circa 20 min), oppure un rerun di `s10b_delta.py` con seme e primo diversi;
  - (c) un audit di `tri_delta.py`.

### S10B-P3: «aperta e densa» dopo il fix P3-c
**Classe: A (redazionale; di fatto già chiusa dall'audit).**

AUDIT_S10-OPEN-B_rev2 §2 dice esplicitamente che «aperta e densa» è DIMOSTRATO una volta applicato P3-c, «redazionale e non richiede un nuovo audit». Il fix consiste nell'aggiungere bump anche nei minimi di u₀′ con valore critico 0.

Con spirito critico va detto anche che, **come scritto**, «Morse+(SB) aperta» è **falso**: u₀′ = −cos x − cos 2x sta nella classe ma non è un punto interno per (SB) a tutti i tempi (`b2_p3_zero_min` 6/6). L'enunciato corretto è uno di questi due:
- «Morse+(SB)+(nessun valore critico nullo di u₀′) è aperto e denso in C^r»;
- «aperto e denso per (SB) su (0,T] con T fissato».

Azione: il coordinatore inserisce il testo P3-c in R3 e aggiorna la riga del LEDGER. Pochi minuti.

---

## 3. Voci condizionali su fonti

| fonte | uso | disponibile offline? | valutazione |
|---|---|---|---|
| **Oberst 1993** (MCSS 6, solo abstract) | SYS-EX, SYS-N1, SYS-T0 | no (solo metadati, «VERIFICATO (abstract)») | **Non è portante dal punto di vista matematico.** Il LEDGER (righe 222–234) dà SYS-EX DIMOSTRATO su Ω **arbitrario**, ℝⁿ compreso, e SYS-T0 come corollario scritto. La fonte serve solo per la **priorità/novità**. Classe C solo per l'attribuzione; lo stato matematico non dipende da Oberst. |
| **[F1] Oleinik ⟺ Kružkov** | S4T-L2, S4T-T3, OPA-T1, S10B-L4 | no (Evans, Kružkov: solo metadati) | **Classe A.** Si evita la fonte con la viscosità evanescente: Cole–Hopf ([F2] DIMOSTRATO) e il metodo di Laplace danno u^ν → formula di Lax–Oleinik q.o. con ‖u^ν‖_∞ ≤ ‖u₀‖_∞. L'entropia passa al limite (η(u^ν)_t + q(u^ν)_x = νη_xx − νη″u_x² ≤ νη_xx), quindi Lax–Oleinik soddisfa le disuguaglianze di Kružkov. Resta l'**unicità** di Kružkov (citazione classica, metadati VC), oppure si **definisce** S_B come limite viscoso, cosa che il progetto di fatto usa, e [F1] diventa superfluo. Qualche ora. |
| **Malgrange 1966** (Ideals of Differentiable Functions, cap. VI) | DICT-Q3-R(a), caso analitico | no (in BIBLIOGRAFIA c'è solo Malgrange 1955/56) | **C.** È il teorema di chiusura dei moduli generati da funzioni analitiche (Malgrange–Tougeron). Non è ricostruibile in poche ore, perché richiede Łojasiewicz e la divisione di Whitney. |
| **Amitsur 1965 / Brešar–Šemrl 1999** | DICT-Q4-C, «rango infinito ⇒ A(iii)» | no (Amitsur assente perfino dai metadati) | **Classe A: la fonte non serve.** Dimostrazione elementare di ciò che serve, data sotto. |
| **Björk** (Rings of Differential Operators) | VAR-C3Q2-R(a′): olonomo ⇒ mai identificato | no (solo metadati) | **Classe A.** La disuguaglianza di Bernstein **non serve**. Se Ann(u) = A₂L, allora A₂u ≅ A₂/A₂L. Rispetto alla filtrazione di Bernstein gr(A₂L) = gr(A₂)·σ(L), perché gr è un dominio, quindi gr(A₂/A₂L) = ℂ[x,ξ]/(σ(L)) ha dimensione 3. Un modulo olonomo ha dimensione 2 per definizione. Serve solo il lemma elementare d'indipendenza della dimensione dalla buona filtrazione, dimostrabile in mezza pagina. |
| **(WP)**: esistenza globale in 𝒮 per KdV | S10B-T3, S4ID-P8, OPR2-P7, S10B-E8 | no (Bona–Smith 1975, Kato 1983, Lax 1975: solo metadati) | **C.** Ricostruirla in modo autonomo richiede più giorni: esistenza locale in H^s per regolarizzazione parabolica, limiti globali (già S10B-T3) e persistenza del decadimento di Schwartz (stime pesate di Kato). Non è un'azione da poche ore. |

**Amitsur, prova elementare.** Siano D₀, …, D_N: Z → V lineari su ℂ, localmente dipendenti, e sia r := max_{u∈Z} dim span{D_iu} ≤ N, con il massimo raggiunto in u₀.
1. Siano D_{i₁}u₀, …, D_{i_r}u₀ indipendenti, sia j un indice fuori da questi (esiste perché r < N+1), e sia S = {i₁..i_r, j}.
2. Si scelgono funzionali φ₁..φ_r con det[φ_k(D_{i_l}u₀)] ≠ 0.
3. Per w ∈ Z sia α(s) il vettore dei minori r×r con segno della matrice [φ_k(D_i(u₀+sw))]_{i∈S}. È polinomiale in s, con α_j(0) ≠ 0.
4. Si pone R(s) := Σ_{i∈S}α_i(s)D_i(u₀+sw). Allora φ_k(R(s)) = 0 per Cramer. Per i valori s, cofiniti, in cui i D_{i_l}(u₀+sw) sono indipendenti, R(s) sta nel loro span, dove φ è iniettiva; dunque R ≡ 0.
5. Derivando in s = 0 si ottiene Σα_i(0)D_iw ∈ span{D_iu₀ : i∈S}, che ha dimensione r.
6. Gli α_i(0) non dipendono da w, quindi D := Σα_i(0)D_i ≠ 0 ha rango ≤ r ≤ N su Z.

È esattamente ciò che usa §16, applicato alle restrizioni D_i|_Z. La prova va trascritta e auditata: meno di un'ora.

---

## 4. Osservazioni trasversali (scetticismo sulle etichette)

1. **Già chiusa nei fatti.** S10B-P3 «aperta e densa» è DIMOSTRATO per decisione dell'audit B2 dopo un fix redazionale. Resta APERTO solo nel LEDGER, e il suo enunciato letterale è falso: va riformulato, non tenuto aperto.
2. **Fonti non portanti.** Tre voci elencate come «condizionali su fonti» non lo sono, o non devono esserlo:
   - Oberst 1993 (solo novità);
   - Amitsur e Björk (prove elementari di quanto serve);
   - [F1] (aggirabile con la viscosità evanescente sul Cole–Hopf già dimostrato).
3. **Chiudibili con prove brevi.** Due voci «senza riduzione» hanno prove brevi:
   - SYS-DIRAC-POL complesso (Lemma E′ per crescita);
   - il caso modello di P2-Q1-NL (Δ, m ≥ 1, disco con fessura: la somma è tutto il nucleo).

   Il candidato di P1-Q7 si chiude con la dilatazione filtrata.
4. **Calcolo.** S10B-V9 non è più «non riprodotto»: δ₅(10), δ₅(9) e δ₅(8) sono riprodotti in modo indipendente in 26–161 s, e δ₆(12) = 7 è calcolato in 195 s. La dipendenza nuova da dichiarare è che i getti AM stiano nella chiusura dello strato principale.
5. **Limiti di questo triage.** Le prove abbozzate (P1-Q7 candidato, SYS-DIRAC-POL, P2-Q1-NL modello, Amitsur, Björk, [F1], (L-int)) **non sono auditate**: le registro come proposte, non come DIMOSTRATO. Le affermazioni sulla letteratura (Braess, Carleman per Schrödinger, Bagrov–Samsonov) vengono dalla memoria e vanno verificate sulle fonti.

---

## 5. Tabella riassuntiva

| ID | classe | motivo in una riga | risultato del tentativo |
|---|---|---|---|
| P1-Q7 | A (candidato) / B (generale) | il candidato (x³+x)∂, ∂ cade con una «dilatazione filtrata» (parità in ν) più (H) per (x³∂, ∂); senza alcuna dilatazione nessuna strada | (H) verificata, σ_μ e parità verificate (`tri_p1q7.out` OK); prova abbozzata, da auditare |
| C12-Q2 = OPF-Q2 | B | falso in Hilbert astratto; serve una famiglia con ≥ 2 interazioni non compatte, nessuna analizzata | — |
| OPF5C-Q1 | B | congettura graduata per ogni N senza struttura nota; per N fissato è un calcolo finito (vedi S10B-V9) | casi N = 5, 6 sotto |
| OPR2-Q3 | B | serve la teoria dei sollevamenti degli atomi; nessun esempio | — |
| OPR2-Q2′ | B (con (L-int) in A) | (L-int) = stima HS esplicita, scrivibile ora; (L-v) richiede l'analisi al vertice del modello del cono | — |
| INT-Q1 | B (a monte C) | servono i termini sottodominanti dell'asintotica radiativa con derivate | — |
| [GT-u₀] | C (poi A) | riscrittura di GT §5 con costanti esplicite; GT e Krüger–Teschl non sono offline | — |
| [GT-u_m] | C (poi B) | Deift–Zhou CMP 165 (1994) e Buslaev–Sukhanov non disponibili | — |
| P2-Q1-NL | A (Δ, m ≥ 1) / B (generale) | su domini semplicemente connessi con Poincaré (disco con fessura) ker Δ = 𝓗₁ + 𝓗₂ con prova di mezza pagina; P generale e m = 0 aperti | prova abbozzata, da auditare |
| P2-Q1-COD | B | mancano funzionali di periodo continui in H^m per P generale | — |
| C12-Q1 | B | strada OPR2-L1 (compattezza calore×trasporto) plausibile ma richiede stime di strato di bordo | — |
| VAR-Q18 | B | un controesempio richiede W ruvido e v solo continuo con controllo di tutta la serie di Dyson | — |
| VAR-Q17(b) | C | letteratura di Carleman per Schrödinger con V(t,x) (Baudouin–Puel, Lasiecka–Triggiani–Zhang, Mercado–Osses–Rosier) non offline | — |
| VAR-P12(d) | B | nessuna ostruzione per log non quadratici; nella classe che commuta con Q non c'è log differenziale | osservazione parziale (parità e dilatazioni) |
| VAR-C3Q2-open / VAR-Q13 | B | senza monicità manca la decomposizione; nessuna strada | — |
| SYS-DIRAC-POL (tempi complessi) | A | Lemma E′ «per crescita»: G è o(1) solo algebricamente, il che è incompatibile con le classi esponenziali | prova abbozzata completa, da auditare |
| ENC-Q4 (DM3) | B | richiede prima la definizione della classe W(t), poi un problema nuovo | — |
| ENC-Q10 (V reale) | C | Darboux a coppie (Matveev–Salle, Bagrov–Samsonov) non offline, più una decisione su 𝔈 | — |
| DICT-U3d-v (ottimalità) | C (parte B) | Braess / Braess–Hackbusch (non offline) indicano che τ_k non è necessario per t^{−β}; il limite uniforme sulla classe resta aperto | — |
| DICT-Q3(c) | B | divisione C^∞ a rango variabile senza criterio generale | — |
| S10B-V9 | A (tentata) | calcolo mod p con generatori indipendenti (Hirota, Adler–Moser) | **δ₅(10)=6 (26 s), δ₅(9)=7, δ₅(8)=9 riprodotti; δ₆(12)=7 nuovo (195 s)**, mod L8/L8′ e AM ⊂ cl(S°₀); Hirota N=5 e (6,11) non conclusi |
| S10B-P3 («aperta e densa») | A | già DIMOSTRATO dall'audit B2 dopo il fix redazionale P3-c; l'enunciato letterale è falso e va riformulato | nessun calcolo necessario |
| Oberst 1993 | C (solo novità) | non portante: SYS-EX è DIMOSTRATO su Ω arbitrario | — |
| [F1] Oleinik ⟺ Kružkov | A | viscosità evanescente sul Cole–Hopf (F2 dimostrato) più Laplace; resta solo l'unicità di Kružkov oppure si definisce S_B come limite viscoso | piano dato |
| Malgrange 1966 | C | teorema di Malgrange–Tougeron non ricostruibile in breve; testo non offline | — |
| Amitsur / Brešar–Šemrl | A | prova elementare (minori, derivata in s) di ciò che serve | prova abbozzata completa, da auditare |
| Björk | A | basta dim gr(A₂/A₂L) = 3 contro olonomo = 2; Bernstein non serve | prova abbozzata |
| (WP) esistenza globale in 𝒮 | C | Bona–Smith, Kato 1983, Lax 1975 non offline; prova autonoma di più giorni | — |
