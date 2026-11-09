# ATTACK-4 — DEVIL-4 · Gate 4a · 26/10/2026

**Oggetto.** `GATE4A.md` §1–§2: quattro sessioni S4-IST, S4-CH, S4-MOD, S4-LIFT; parcheggi (Koopman, PAINLEVÉ, MON, NLSPEC, HAANTJES, F4-ALG come strada autonoma); eliminazione di SPLIT-f. Fonti lette: `FASE4_SCOUTING.md`, `GATE3.md`, `PROBLEM.md`, i cinque `research/F4-*/VERDETTO.md`, le `NOTE.md` per le prove INT-T1, F4LIN-T2, MODREL-T1, F4L-P3, ALG-T1, SPLIT-L1, e `open_questions.md` di F4-LIN e F4-ALG.

**Skill caricate** (lettura del SKILL.md; nessuno script `_vendor` eseguito):
- `session-protocol`: PLAN-4, PLAN-READY, DONE.
- `kill-argument`: ho eseguito solo il thread di ATTACCO. Il memo è singolo e sotto le 250 parole, seguito dalle obiezioni atomiche con severità. Niente Codex: il revisore fresco sono io, e la difesa spetta al coordinatore.
- `scientific-critical-thinking`: separo i dati dall'interpretazione e "prova scritta" da "V-ex"; tengo conto della non indipendenza delle repliche; ogni obiezione ha un rimedio.
- `novelty-check`: ho applicato i limiti di verdetto. Niente ABANDON senza un articolo nominato; la vicinanza ad altri lavori è informazione, non condanna.

**Verifiche SymPy/mpmath.** Script in `research/DEVIL/sympy4/`, eseguiti con `.venv -I`; output nei file `.out` accanto agli script.
- `e_int_a9.py`: confronta l'E_int per termine di A9 con gli oggetti di Fase 4, su Burgers.
- `radius_checks.py`: calcola il raggio in ε del flusso del solo termine non lineare e controlla il lemma della striscia dei cumulanti.

---

## 1. Memo d'attacco (≤ 250 parole)

> Il Gate 4a promuove quattro strade che rispondono a una domanda diversa da quella dell'utente.
>
> L'utente chiede tre cose: identificazione, scomposizione **per termine** ed E_int, nel senso di A9: f̂ = e_{n1} + e_{n2} + E_int, dove e_n è il flusso del termine n da solo. I quattro verdetti dichiarano invece, ciascuno con una prova, che i termini non passano: INT-O1, F4LIN-O1, ALG-O1, e F4-LIFT, dove (S) è una filtrazione e non una somma. La colonna "E_int sì" della tabella §1 mette sotto lo stesso nome cinque oggetti diversi: E^trop = u^ν − u⁰, E^NL = u − e^{tA}u₀, u − Σ 1-solitoni, l'interazione fra modi di NF-1 ed E^mix. Nessuno di questi è l'E_int di A9. Per Burgers l'E_int di A9 vale ε²(3νt²/2) sin 2x + …, mentre E^NL al primo ordine è t·B(u₀), cioè il solo termine non lineare (calcolo esatto, `e_int_a9.out`).
>
> Anche l'identificazione "nell'anello intero" è vuota su ogni dato calcolabile. Per ALG-T1(c) identifica solo una u con trdeg ℂ⟨u⟩ = ∞, mentre ogni formula elementare o D-algebrica ha trdeg finito. Restano quindi solo identificazioni relative a una classe (𝓗_M, dizionari di Hammerstein), cioè RT-4.
>
> I teoremi chiave sono corollari brevi di fatti classici: INT-T1 viene da Novikov/Lax più Vandermonde, F4L-P3 dal lemma della striscia per i cumulanti, F4LIN-T2 da log-sum-exp, MODREL-T1 dal gcd in un dominio fattoriale. Sono enunciati su ℝ, mentre G★′ è posto su Ω limitato.
>
> Quanto agli scarti, l'unico quadro in cui e_n esiste dopo lo shock (MON: Kružkov, Brezis–Pazy) è parcheggiato, e la domanda per termine sopravvive solo come criterio di kill di S4-CH (LIN-Q3). Così com'è, il set va respinto.

---

## 2. Obiezioni

### O1 — CRITICA · Nessuna sessione ha per obiettivo la domanda per termine; "E_int sì" è un'equivocazione
**Punto attaccato.** GATE4A §1, colonna (E). Sessioni del §2. PROBLEM.md G★′ punto 3, che il Gate 3 ha approvato a tre livelli.

**Argomento.** I verdetti dichiarano un'ostruzione sui termini, ciascuno con una prova:
- INT-O1: l'IST separa i flussi, non i monomi.
- F4LIN-O1: in φ i flussi di uu_x e di νu_xx diventano non lineari, e il calore ha un solo termine.
- ALG-O1: nessuna somma.
- F4-LIFT: (S) è una filtrazione, non una somma.
- MODREL: (S) = no, (E) = no.

Gli "E_int sì" della tabella sono invece cinque oggetti distinti:

| strada | oggetto chiamato E_int | che cosa misura |
|---|---|---|
| RT-R7b (F4LIN-T2) | E^trop = u^ν − u⁰ | effetto della viscosità (pieno meno limite non viscoso) |
| F4-LIFT (F4L-P2/P3) | E^NL = u − e^{tA}u₀ | intera parte non lineare |
| RT-R7a (Hirota) | u − Σ_i u_i^{(1)} | interazione fra **solitoni** (componenti spettrali) |
| H-v2 (NF-1) | termine di 2° ordine fra modi l, m | interazione fra **modi di Fourier** |
| Cole–Hopf | E^mix ≡ 0 | — |

L'E_int di A9 per i due termini A = ν∂² e B(u) = −uu_x è u − e_A − e_B + u₀. Il calcolo esatto all'ordine ε² con u₀ = ε sin x (`e_int_a9.out`) dà:
- E_int^{A9} = ε²[2νt e^{4νt} − e^{2νt} + 1]e^{−4νt}/(4ν) · sin 2x = ε²(3νt²/2 − 7ν²t³/3 + …) sin 2x. Il termine principale è (t²/2)(DA[B] + DB[A])u₀: l'anticommutatore, cioè la versione non lineare di P1-T2.
- E^NL = ε²(−t/2 + …) sin 2x, con primo ordine **= t·B(u₀)**: è il termine non lineare da solo, senza alcuna interazione.

Quindi l'E_int "uniforme in t" di F4L-P3 è un oggetto diverso da quello di A9.

**Conseguenza.** Nessuna delle quattro sessioni ha come obiettivo il punto 3 di G★′ nel non lineare. Compare solo LIN-Q3, usato da S4-CH come *criterio di kill* e non come obiettivo. È lo stesso schema che DEVIL-A aveva segnalato al Gate 1 (O2: la domanda per termine sostituita da un'altra).

**Azione.**
- Fissare in NOTAZIONE, prima di partire, la definizione A9 di E_int non lineare (e_n = flusso del termine n da solo).
- Rietichettare la colonna (E) della tabella con l'oggetto effettivo di ogni strada.
- Assegnare la domanda per termine a una sessione come **obiettivo** (S4-TERM, §4).

### O2 — CRITICA · L'identificazione "nell'anello intero" è vuota sui dati calcolabili: tutte le (I) promosse sono relative a una classe
**Punto attaccato.** GATE4A §1, colonna (I) e "Dicotomia". ALG-T1, ALG-P3, INT-T1(b), INT-Q1. Obiettivo di S4-MOD ("decidibilità di Ann(u) = 0").

**Argomento.**
- ALG-T1(c): u identifica in ℂ{y} ⟺ trdeg ℂ⟨u⟩ = ∞.
- Ogni u espressa da una formula costruita con funzioni D-algebriche ha ℂ⟨u⟩ ⊂ ℂ(x,t)⟨u⟩, che ha trdeg finito. Le funzioni D-algebriche comprendono le elementari, le Liouvilliane, erf, le funzioni di Airy e tutta la classe EP-razionale di M1 fissata al Gate 3.
- Quindi **nel modello di dato M1 nessun dato identifica nell'anello intero**. Il nucleo del calore (ALG-C1) è il primo esempio, non un caso patologico.
- Identificano solo i dati differenzialmente trascendenti. F4-ALG lo sa (ALG-Q3, Γ di Hölder), ma GATE4A non ne trae la conseguenza.
- In M3 (u ∈ H^m noto) il criterio non è certificabile con dati finiti: è l'analogo di C3-P1, come ammette MODREL stesso.
- Le (I) con contenuto sono quindi tutte relative a una classe: INT-T1 in 𝓗_M, MODREL in un dizionario di Hammerstein fisso, F4L-P6 in 𝔏_N. È esattamente RT-4 (identificazione relativa a una classe), cioè l'esito che GATE4A indica come *kill* di S4-IST e S4-MOD ("→ lemma di RT-4").
- Inoltre tutti i banchi di prova con risultati sono integrabili o linearizzabili: Burgers, KdV, NLS. L'unico risultato fuori dall'integrabilità è negativo: F4L-O1, u_t = u_xx + u², raggio ρ(T) → 0.

**Conseguenza.**
- Le esclusioni di S4-IST e S4-MOD sono già scattate per costruzione.
- L'obiettivo "decidibilità di Ann(u) = 0" di S4-MOD è già deciso: in M1-EP è banale (u ∉ EP), in M3 è impossibile.
- La risposta onesta all'utente è "identificazione relativa a un dizionario, con soglie di grado (MODREL-P2) e di ordine (INT-T1)". Il set non la rivendica come tale.

**Azione.**
- Riscrivere (I) come identificazione relativa: un teorema unico "dizionario D ⟹ criterio di rango e soglie".
- Chiedere a ogni sessione almeno un risultato, positivo o negativo, su un'equazione **non integrabile** (KdV–Burgers, Fisher–KPP, u_t = u_xx + u²).
- Scrivere G★′-NL (O8) prima di avviare le sessioni.

### O3 — MAGGIORE · Le prove chiave sono corollari brevi di fatti classici; il programma rischia di produrre un "dizionario"
**Punto attaccato.** Novità 4/10 o PROCEED WITH CAUTION in tutte e quattro le strade; GATE4A dichiara F4L-P3 "candidato più nuovo".

**Controllo delle prove.** Non ho trovato controesempi alle prove scritte così come sono enunciate (dettagli nel §5). Ho trovato invece la loro radice classica:

| prova | riduzione | stato del delta |
|---|---|---|
| **F4L-P3** | **Lemma della striscia dei cumulanti**: se X ha valori in un intervallo di ampiezza w, s ↦ log E e^{sX} è olomorfa per \|Im s\| < π/w; il raggio è ≥ π/w, con uguaglianza per la legge simmetrica a due punti (log cosh). Con X = U₀(Y), Y ~ G(x−·), s = −ε/2ν si ottiene \|ε\| < 2πν/osc(U₀). L'uniformità in t è automatica perché l'ampiezza del range di U₀ non dipende da t, e il caso estremale tanh è il Bernoulli simmetrico. Controllo numerico: su 300 leggi casuali a 3 atomi il minimo \|zero\| è 3.1575 ≥ π (`radius_checks.out`). | La prova di F4-LIFT è proprio questo argomento di settore. Il delta "raggio in ampiezza" è una riformulazione di un fatto probabilistico noto (CIT: letteratura sui cumulanti e su Lee–Yang, da verificare). Il criterio di kill di S4-LIFT ("se F4L-P3 è classico") è molto probabilmente già scattato. |
| **INT-T1** | Le soluzioni stazionarie dei flussi superiori sono quelle con q_d nullo sullo spettro (Novikov 1974, Lax 1975), più Vandermonde. | Il delta è solo formulazione e trasporto, come ammette F4-INT. |
| **F4LIN-T2** | (i) è la disuguaglianza log-sum-exp (dequantizzazione di Maslov). (ii) è il profilo tanh dello shock viscoso, con ∫(1 − tanh) = ln 2. Ḣ^s per s < ½ perché u⁰ ha un salto. | Classico, come ammette F4-LIN. |
| **MODREL-T1** | Cinque righe: gcd in un dominio fattoriale. | Elementare. Il delta possibile è MODREL-P2 (soglia di grado N+1). |
| **ALG-T1** | Argomento del separante, cioè zeri generici di Kolchin. | Noto in sostanza (F4-ALG). |

**Conseguenza.** Secondo i limiti del novelty-check non c'è ABANDON: nessun articolo nominato contiene i pacchetti di enunciati. Il verdetto è però PROCEED WITH CAUTION, e la cosa specifica che rende sottile il delta è questa: il contenuto è la tabella di trasporto Fase 3 → Fase 4, non un teorema. Se le quattro sessioni portano questi enunciati a DIMOSTRATO, la Fase 4 produce una rassegna ben fatta. Il delta reggerebbe con:
- un risultato fuori dall'integrabilità (convergenza NF per KdV–Burgers, E_int di A9);
- oppure INT-Q1 nell'anello intero;
- oppure la soglia di grado di MODREL-P2/C3 come teorema generale.

**Azione.**
- Fare novelty-check di MODREL: in GATE4A risulta "n.d.", mentre il verdetto F4-HOR dice PROCEED. È un'incoerenza.
- Chiedere a CIT-AUDIT-4 una ricerca mirata sul lemma della striscia dei cumulanti prima di aprire S4-LIFT.
- Trattare INT-T1/T2, F4LIN-T2, F4L-P3, ALG-T1 e MODREL-T1 come **lemmi da auditare**, non come obiettivi di sessione.

### O4 — MAGGIORE · Il modello di dato non corrisponde, e gli scarti usano due pesi e due misure
**Punto attaccato.** INT-T1: Faddeev su ℝ, più continuazione unica (UC) da Ω a I×ℝ. F4L-P3: su ℝ. F4-LIN: "canonica su ℝ (Widder), non intrinseca su Ω limitato". Parcheggio di PAINLEVÉ.

**Argomento.**
- G★′ è posto su Ω limitato con u ∈ H^m(Ω) (M3).
- In INT-T1, Λ(u) è definito dallo scattering della continuazione di u su tutta la retta; da u|_Ω si ottiene solo tramite UC, che è instabile.
- PAINLEVÉ è stato parcheggiato proprio perché "M3 incompatibile: continuazione analitica mal posta" (F4-HOR). La UC di Saut–Scheurer da Ω a I×ℝ è lo stesso tipo di continuazione mal posta.
- Due pesi e due misure: INT-T1 è promosso, il residuo WTC è parcheggiato.

**Azione.**
- Ogni enunciato promosso dichiari il suo modello di dato (M1, M2 o M3) e il dominio (ℝ, 𝕋 o Ω).
- Per S4-IST: o la versione M3 è un obiettivo esplicito (stabilità di Λ(u) rispetto a u|_Ω), oppure i risultati sono dichiarati M1.
- Riallineare il criterio usato per PAINLEVÉ: o si riammette WTC come strumento di (I) in M1, o si applica lo stesso metro a INT-T1.

### O5 — MAGGIORE · Errore di scarto: MON (accretivi / splitting) è l'unico quadro in cui esiste il flusso del termine da solo
**Punto attaccato.** F4-HOR H-v3 MON: PARCHEGGIA, motivato con "L¹ non risponde alla domanda 3 del Gate 3". F4-HOR H-ii-c SPLIT-f: ELIMINA.

**Argomento.**
- L'E_int di A9 richiede e_B, il flusso del solo termine uu_x, cioè Burgers non viscosa. Questo flusso perde regolarità a t* = 1/(ε max|u₀′|).
- Calcolo: con u₀ = ε sin x il raggio in ε di e_B(t, x=1) vale circa 0.81/t (root test a n = 40: 1.60, 0.81, 0.41, 0.21 per t = ½, 1, 2, 4; `radius_checks.out`). **Tende a 0 come 1/t.** Per il flusso pieno, invece, F4L-P3 dà raggio ≥ 2πν/osc(U₀) = πν uniforme in t.
- Oltre t*, e_B esiste solo come soluzione entropica, cioè come semigruppo di contrazioni L¹ (Kružkov; Crandall–Liggett), e la formula prodotto è quella di Brezis–Pazy. È esattamente il quadro MON. La teoria dello splitting per leggi di conservazione viscose esiste ed è classica (Holden–Karlsen–Lie–Risebro, *Splitting methods for PDEs with rough solutions*, EMS 2010, da verificare).
- Il rigetto di F4-HOR riguarda la **continuità** (domanda 3 del Gate 3), non l'**oggetto** per termine.
- SPLIT-L1 è corretto, ma dice proprio che L è diagonale in Fourier e f è diagonale in x. Due cornici diverse in cui ciascun termine è diagonale: è l'impianto dello splitting. Eliminare SPLIT-f come strada va bene. Parcheggiare il suo naturale successore (lo splitting a due cornici, MON) è l'errore.

**Azione.** Riammettere MON e lo splitting dentro la sessione per termine (S4-TERM, §4), con:
- e_n entropico;
- E_int di A9 all'ordine t² (anticommutatore, come sopra);
- comportamento oltre t*;
- dipendenza da ν.

### O6 — MAGGIORE · I criteri d'uscita non sono né severi né verificabili
| sessione | criterio proposto | difetto | riscrittura proposta |
|---|---|---|---|
| S4-IST | "INT-Q1 falsa **e** nessuna classe intermedia con criterio" | Se INT-Q1 resta aperta (l'esito più probabile) non scatta. La "classe intermedia con criterio" è sempre disponibile (un dizionario finito con il rango di MODREL). Non è falsificabile. | Time-box: entro la data X, o INT-Q1 dimostrata, o un controesempio, o almeno la riduzione a un enunciato classico nominato. Altrimenti MERGE in RT-4 come lemma. |
| S4-CH | "LIN-Q3 non dà né forma chiusa né stima" | Una stima banale esiste sempre: l'errore di splitting è 2-Lipschitz in L¹ (F4-HOR NOTE §MON). Il criterio non scatta mai. | "Stima" deve voler dire ordine t² con costante esplicita, oppure un teorema negativo che la escluda. Ostruzione F4LIN-O1 già nota. |
| S4-MOD | "se il criterio di rango non si estende oltre Burgers (KdV)" | È già V-ex per il 2-solitone di KdV (tabella MODREL): è soddisfatto in partenza. "Decidibilità di Ann(u) = 0" è già decisa (O2). | Estensione a un dizionario non di Hammerstein (u_x², u u_xx) **e** a un'equazione non integrabile; soglia di grado come teorema (MODREL-C3). |
| S4-LIFT | "se F4L-P3 è classico (CIT) o non si estende a Ω limitato" | CIT non può certificare la novità. Il lemma dei cumulanti (O3) rende probabile che il criterio sia già scattato. Per la serie NF di KdV–Burgers non c'è alcun kill. | Kill duplice e datato: (a) convergenza NF per KdV–Burgers in una classe esplicita, oppure controesempio; (b) versione su Ω limitato con stima. |

Mancano anche, per tutte le sessioni:
- un limite di tempo e di budget;
- predizioni registrate prima di partire;
- un "minimo consegnabile" se la sessione fallisce.

### O7 — MAGGIORE · La "dicotomia" non è un'evidenza indipendente: o è tautologica o è falsa
**Punto attaccato.** GATE4A §1, "Due fatti trasversali (convergenza indipendente di più scout)", punto 1.

**Argomento.** La tesi è "forma chiusa per (S) ed (E) ⟹ non identifica".
- Se "forma chiusa" vuol dire trdeg finito, segue dalla definizione tramite ALG-T1(c): forma chiusa ⟹ relazioni extra ⟹ ambiguità.
- Se "forma chiusa" comprende le rappresentazioni integrali, è **falsa**. Cole–Hopf dà per *ogni* dato di Burgers u = −2ν∂_x log ∫G(x−y)e^{−U₀(y)/2ν}dy. In φ vale E^mix = 0, e la sovrapposizione è una miscela softmax su un continuo (Widder). Per U₀ differenzialmente trascendente si ha trdeg = ∞, quindi u identifica (ALG-Q3).
- Le repliche non sono indipendenti. Il grafo di comunicazione di FASE4_SCOUTING fa di F4-ALG il "hub" che traduce ogni strada nello stesso linguaggio, e la convergenza è indotta dal dizionario comune.

**Azione.** Enunciare la dicotomia come teorema, con una definizione precisa di forma chiusa: immersione ℂ⟨u⟩ ⊂ ℂ(E₁,…,E_N) di trdeg finito. Poi assegnarla (S4-ID, §4), oppure togliere "convergenza indipendente".

### O8 — MAGGIORE · Al Gate 4a manca un enunciato bersaglio non lineare
**Punto attaccato.** PROBLEM.md: G★′ è lineare, e la scala arriva a L5 = "Fase 4 non lineare" senza un enunciato.

**Argomento.** I criteri d'uscita del §2 rimandano a domande degli scout (INT-Q1, LIN-Q3), non a punti di un G★′-NL. Senza un bersaglio non si può giudicare se una strada "risponde alla domanda dell'utente" (è il punto 1 del compito). Al Gate 1 G★′ era stato approvato *prima* delle strade.

**Azione.** Scrivere G★′-NL in 3 righe (I relativa a un dizionario, S/E per termine nel senso di A9, banchi non integrabili) e farlo approvare insieme al set di strade.

### O9 — MINORE · Koopman parcheggiato mentre Carleman e NF sono promossi: è lo stesso oggetto
F4L-P5 mostra che gli **autovalori** di Koopman vedono solo la parte lineare. Le **autofunzioni** portano invece il termine non lineare:
- Cole–Hopf è un'autofunzione di Koopman per Burgers (Page–Kerswell 2018, verificato da F4-LIFT);
- la linearizzazione di Poincaré è un insieme di autofunzioni;
- F4-LIFT stesso scrive "componente = autospazio di Koopman del sollevato".

Lo scarto è motivato con un argomento che riguarda gli autovalori e non le autofunzioni. Non si perde nulla se la cosa è dichiarata.

**Azione.** Rinominare la strada in "Carleman/Koopman (autofunzioni) + NF".

### O10 — MINORE · Ipotesi e incoerenze formali
- **ALG-T1** è enunciato per u ∈ C^∞ su Ω connesso, ma la primalità di J_u e il campo ℂ⟨u⟩ richiedono u analitica: il verdetto stesso dice "primo per u analitica". Per le evoluzioni la UC attraverso t = cost non è garantita (soluzioni di tipo Tychonoff). **Azione:** mettere l'analiticità nell'enunciato.
- **INT-T1** dipende da F1–F4 e dalla UC. Il criterio d'uscita di S4-IST copre solo INT-Q1, non il rischio sulle fonti.
- **GATE4A**:
  - "Due fatti trasversali" ne elenca tre;
  - la novità di MODREL è "n.d." nella tabella e PROCEED nel verdetto;
  - S4-IST assorbe cinque cose (R7a, R7c, Hirota, Miura, Darboux) più INT-Q1;
  - quattro sessioni in parallelo più S-CHECK su circa 20 claim superano verosimilmente la capacità di audit.
- **F4-ALG** come strada autonoma: il parcheggio è corretto secondo il suo PLAN (P2 non soddisfatto). ALG-T1-gen (equazioni non evolutive, Kolchin) è però l'unica (I) generale, e finisce dentro S4-MOD senza obiettivo. Va bene, ma va scritto.
- **NLSPEC, HAANTJES**: scarti corretti, con trigger chiari (P2, sistemi). **SPLIT-f**: eliminazione corretta come strada (SPLIT-L1 regge, §5), con la riserva di O5.

---

## 3. Risposta ai sei punti del compito
1. **Rispondono alla domanda dell'utente?** No per la scomposizione per termine ed E_int (O1). Per l'identificazione sì, ma solo in forma relativa a un dizionario e su banchi integrabili (O2). Manca il bersaglio (O8).
2. **Novità.** Il rischio di riformulazione è concreto: ogni prova chiave si riduce a un fatto classico nominabile, e F4L-P3 al lemma dei cumulanti (O3). Niente ABANDON. CAUTION, con il delta specificato.
3. **Scarti.** Un errore: MON e lo splitting (O5). Un doppio standard: PAINLEVÉ contro INT-T1 sul modello di dato (O4). Una questione di etichetta: Koopman (O9). Gli altri scarti sono corretti.
4. **Criteri d'uscita.** Non severi: due non scattano mai (S4-IST, S4-CH), uno è soddisfatto in partenza (S4-MOD), uno è probabilmente già scattato (S4-LIFT) (O6).
5. **Prove scritte.** Nessun controesempio alla validità (§5). I punti deboli sono di portata (dominio ℝ, UC, classe 𝓗), di oggetto (E^NL non è E_int, O1) e di ipotesi (analiticità in ALG-T1).
6. **Alternativa:** §4.

## 4. Il set che proporrei
**Prima di partire:** G★′-NL (O8) e la definizione A9 di E_int non lineare in NOTAZIONE (O1).

| sessione | contenuto | obiettivo | kill (binario, datato) |
|---|---|---|---|
| **S4-TERM** (nuova, prioritaria) | E_int di A9 per termini non lineari. Assorbe MON/Brezis–Pazy/Kružkov, H-v2 NF (rapporto dei simboli come strumento di calcolo), LIN-Q3, F4L-P2. | (a) Forma chiusa all'ordine t² e struttura della serie in (ε, t) (anticommutatore e rapporto dei simboli). (b) Comportamento oltre t* con e_n entropico. (c) Dipendenza da ν. (d) KdV–Burgers e Fisher–KPP come banchi non integrabili. (e) Versione su Ω limitato. | Entro la data X, nessuna stima di ordine t² per Burgers oltre t* migliore della disuguaglianza triangolare ⇒ teorema negativo registrato in RT-2. |
| **S4-ID** | Identificazione relativa: MODREL e linguaggio F4-ALG, con INT-T1 come caso 𝓗_M di un dizionario. Dicotomia come teorema (O7). INT-Q1 come sotto-domanda con time-box. | Teorema unico "dizionario D: criterio di rango e soglie di grado e di ordine" (MODREL-C3, INT-T1(c)), verificato su almeno un'equazione non integrabile. | Nessun criterio su KdV–Burgers o Fisher entro la data X ⇒ RT-4 come lemma. |
| **S4-INTEG** (corta, solo audit) | INT-T1/T2, F4LIN-T2, F4L-P3, Hirota (INT-P5/P6), ALG-T1/P4/P6: lemmi di trasporto. | DIMOSTRATO dopo CIT, con la riduzione classica dichiarata (O3) e il modello di dato dichiarato (O4). Nessun obiettivo di ricerca nuovo. | — (audit) |

S4-LIFT, come sessione autonoma, scompare:
- F4L-P3 diventa un lemma in S4-INTEG;
- NF e la versione su Ω limitato passano in S4-TERM;
- Koopman (autofunzioni) entra in S4-TERM come linguaggio.

**Sequenza:** S4-INTEG in parallelo (costa poco). S4-TERM e S4-ID in parallelo. S-CHECK solo sul cammino critico.

## 5. Che cosa regge (onestà)
- **Validità.** Le prove di INT-T1 (modulo F1–F4 e UC), MODREL-T1, F4L-P3, F4LIN-T2(i)–(ii), ALG-T1(a)–(c) per u analitica, SPLIT-L1 e ALG-C1 sono corrette per quanto ho potuto controllare. Ho verificato a mano:
  - il caso tanh di F4L-P3;
  - la riduzione F4L-P3 → striscia dei cumulanti;
  - il conteggio di MODREL per x/t: Ann(u) ∋ ξ², Ann(u²) ∋ ξ³ ⇒ rango 2 ⇒ non identifica, coerente con F4LIN-C1;
  - la relazione K₁ − k²K₀ = 0 per il 1-solitone, con k = 2κ.

  Non ho trovato controesempi.
- **Contenuto vero e utile.**
  - Le ostruzioni negative (INT-O1, F4LIN-O1, ALG-O1, SPLIT-L1, F4L-O1) sono il contenuto più solido e più vicino alla domanda dell'utente, perché dicono **dove** la scomposizione per termine non può esistere.
  - MODREL-P2 (soglia di grado N+1) è il candidato con il delta più netto per (I).
- **Gli scarti di NLSPEC e HAANTJES** sono corretti.

## 6. Verdetto (mappatura kill-argument)
Obiezioni non risolte dal testo attuale:
- 2 CRITICHE (O1, O2);
- 6 MAGGIORI (O3–O8);
- 2 MINORI (O9–O10).

Esito: **FAIL** (`unresolved_critical`) per il set *come proposto*.

**Raccomandazione:** non approvare le quattro sessioni così come sono. Approvare invece il set ristrutturato del §4, oppure, come minimo:
1. G★′-NL e la definizione A9 prima di partire;
2. la domanda per termine come obiettivo di una sessione, con MON riammesso;
3. criteri d'uscita riscritti come nella tabella di O6;
4. F4L-P3 e INT-T1 trattati come lemmi da auditare, non come obiettivi.
