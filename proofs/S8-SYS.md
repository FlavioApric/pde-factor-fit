# PROOF_PACKAGE — S8-SYS (Fase 8, L6: sistemi a coefficienti costanti, gauge, E_int per sistemi)
27/10/2026. Riprende `research/F6-SYS/NOTE.md` e `VERDETTO.md`, con i fix F2, F8 e F9 di DEVIL-6 (`research/DEVIL/ATTACK-6.md`, O2, O8, O9) e le correzioni di `research/CIT-AUDIT/AUDIT-6.md`.

**Skill caricate.** session-protocol e claim-lifecycle (lette per intero). Catena seguita: proof-writer (struttura del pacchetto e triage onesto), math-skill in modo prova e controesempio (il controesempio a SYS-S1 del §3.3 e la ricerca di casi limite), SymPy solo come verifica. Gli audit (proof-checker) e il kill-argument sui claim del cammino critico (SYS-EX, SYS-S1, H-DIRAC) sono delegati a S-CHECK-F8 e DEVIL-8 tramite `CHECK_REQUEST.md`; non ho lanciato subagenti. Nessuno script `_vendor` eseguito.

**Verifiche.** `sympy/s8sys_checks.py` → `sympy/s8sys_checks.out`: **32/32 OK**. Alla prima esecuzione il controllo D6 era FAIL per un errore mio nel controllo (confrontavo un'espressione espansa con una non espansa); corretto il controllo, l'enunciato non è cambiato.

**Stati.** Nessun enunciato è DIMOSTRATO: manca S-CHECK. "Prova scritta" indica una prova completa non ancora auditata. "CON-FONTE in sostanza" indica un enunciato di cui ho scritto una prova completa ma che con buona probabilità è già in letteratura, con la fonte da verificare. FALSO indica un enunciato confutato con controesempio esplicito.

**Notazione.** R = ℂ[ζ_1, …, ζ_n], con ζ_j ↔ ∂_j (per i sistemi di evoluzione ζ = (τ, ξ) ↔ (∂_t, ∂_x)). **Ipotesi globale (fix SYS-13):** salvo avviso contrario Ω ⊂ ℝ^n è un aperto **connesso non vuoto**. Basta un aperto non vuoto qualsiasi per SYS-EX (ii) ⇒ (i), SYS-S1(i⇒) e SYS-S1(i⇐); la connessione serve per SYS-N1, SYS-EX (i) ⇒ (ii), SYS-T0, SYS-C1, SYS-S1(ii) e H-DIRAC. 𝒜 ∈ {C^∞(Ω), 𝒟′(Ω)}. Le righe agiscono a sinistra: P ∈ R^{l×k} agisce su u ∈ 𝒜^k. U_P := R^{1×l}P ⊆ R^{1×k} è il modulo delle righe e M_P := R^{1×k}/U_P. Sol_𝒜(P) ≅ Hom_R(M_P, 𝒜). Per u ∈ 𝒜^k: Ann(u) := {r ∈ R^{1×k} : r(∂)u = 0}, M_u := R^{1×k}/Ann(u), e φ_u : M_P → 𝒜, [r] ↦ r(∂)u, che è ben definita se u ∈ Sol(P). Ann(u)/U_P = ker φ_u. "u identifica P" significa Ann(u) = U_P, cioè φ_u iniettiva. Per un ideale massimale m: soc_m(M) := Hom_R(R/m, M) = {x ∈ M : m x = 0}; m_λ := (ζ_1 − λ_1, …, ζ_n − λ_n). EP indica gli esponenziali-polinomi. Modello di dato: DM3 (u noto esattamente) in tutto il pacchetto, salvo G-T2, che usa DM-inv.

---
## 1. SYS-T1: declassamento e confronto con Oberst 1990 e con Schindelar–Levandovskyy–Zerz 2011

### [SYS-L0] Test d'iniettività su un sottomodulo essenziale — standard
Sia φ : M → F un omomorfismo di R-moduli e sia E ⊆ M essenziale (ogni sottomodulo non nullo di M interseca E in modo non banale). Allora φ è iniettiva se e solo se φ|_E è iniettiva.
*Prova.* ker φ ∩ E = ker(φ|_E). Se questo è 0, ker φ è un sottomodulo che interseca E banalmente, quindi è nullo per essenzialità. ∎

### [SYS-L1] Famiglia essenziale — standard (prova in `research/F6-SYS/NOTE.md` §1)
Sia M finitamente generato. Esiste una famiglia finita x_{p,j} ∈ M, con p ∈ Ass(M) e j = 1, …, μ_p, tale che R x_{p,j} ≅ R/p, la somma E := Σ R x_{p,j} è diretta ed E è essenziale in M. Per p = m massimale, μ_m ≤ dim_ℂ soc_m(M): le copie di R/m nella somma diretta generano un sottospazio di soc_m(M) di dimensione μ_m. Si ha anzi μ_p = μ_0(p, M), il numero di Bass (Matsumura, *Commutative Ring Theory*, §18; numerazione da verificare), ma nel seguito serve solo la disuguaglianza.

### [SYS-T1] Criterio d'identificazione su una famiglia essenziale — prova scritta; declassato a strumento
*Enunciato.* Sia u ∈ Sol_𝒜(P), sia {x_{p,j}} una famiglia come in SYS-L1 per M_P, e sia w_{p,j} := φ_u(x_{p,j}). Allora u identifica P se e solo se, per ogni q ∈ Ass(M_P), non esiste alcuna relazione Σ_{p ∈ Ass, p ⊇ q} Σ_j r_{p,j}(∂) w_{p,j} = 0 in cui qualche r_{q,j} ∉ q.
*Prova.* È SYS-L0 applicato a E = ⊕ R x_{p,j}, con la riduzione al primo q che si trova in `NOTE.md` §1: un elemento non nullo di ker φ_u ∩ E può essere scelto con annullatore primo q ∈ Ass(E) = Ass(M_P); nella sua scrittura compaiono solo addendi con p ⊇ q, e almeno un coefficiente r_{q,j} ∉ q. Il passaggio "∩_{c_{p,j} ≠ 0} p = q con ogni p ⊇ q ⇒ q compare tra i p" vale perché un'intersezione finita di primi uguale a un primo q contiene il prodotto dei primi, quindi q contiene uno di essi. ∎
*Riduzione al caso scalare.* Per k = 1 il criterio è esattamente C3-T1 (`NOTE.md` §1). In n ≥ 3 variabili il test "w_i ∉ EP" va sostituito con "Ann(w_i) = (P_i)".

**Declassamento (O8 accolta).** SYS-T1 non è un teorema strutturale. È la riformulazione di SYS-L0 su una famiglia essenziale, e su una u non EP non è più decidibile del calcolo diretto di Ann(u). Lo stato proposto è "prova scritta, CON-FONTE in sostanza (algebra standard dei moduli essenziali, Matlis, Pacific J. Math. 8(3) (1958) 511–528)". Lo strumento resta utile per due ragioni: riduce il test a μ_p funzioni scalari per ogni primo associato (Dirac 3+1 nel §7, Lamé nel §4) e dà esattamente C3-T1 per k = 1. Il contenuto strutturale passa a SYS-EX (§2).

**Confronto con Schindelar–Levandovskyy–Zerz, J. Symbolic Comput. 46 (2011) 1189–1204.** Fonte: abstract di arXiv:1004.2924, letto il 27/10/2026; il testo completo non è stato letto. Il lavoro calcola l'MPUM (coefficienti costanti) e il VMPUM (coefficienti variabili) di traiettorie **polinomiali e polinomiali-esponenziali**, con basi di Gröbner su algebre di Ore. Il delta si dichiara con un fatto elementare:
- **[SYS-R1] (prova scritta, una riga).** Se u ∈ EP^k, allora M_u ha lunghezza finita. *Prova.* Ogni componente sta in uno spazio di EP di dimensione finita invariante per le derivate, quindi M_u ≅ Σ R u_i ⊆ 𝒜 ha dimensione finita su ℂ. ∎
- Quindi da dati EP si identificano **solo** sistemi con Sol di dimensione finita. SYS-T1 e SYS-EX trattano invece il caso in cui M_P non ha lunghezza finita (ogni EDP vera). Lì il dato identificante non è mai EP e il problema esce dalla classe di SLZ. In quella classe, cioè per M_P di lunghezza finita, SYS-EX dice che un dato EP identificante esiste se e solo se gli zoccoli hanno dimensione ≤ 1, cioè se il duale di Matlis di M_P è ciclico. Questo è coerente con la teoria dell'MPUM e probabilmente noto.

**Confronto con Oberst, Acta Appl. Math. 20 (1990) 1–175, DOI 10.1007/BF00046908.** Il testo è a pagamento e non l'ho letto, come già CIT-AUDIT-6; CIT-AUDIT-8 (A2) non ha letto le pp. 24–36 né i §2–4, che quindi **non** vanno citati come verificati. Secondo la fonte secondaria (Gluesing-Luerssen–Rosenthal–Weiner, math/9905046, §3) Oberst usa che C^∞(ℝ^n) e 𝒟′(ℝ^n) sono cogeneratori iniettivi "grandi" (Ass = Spec R). SYS-EX (§2) equivale a "C^∞(Ω) contiene ogni E(R/p) con molteplicità ∞ per p non massimale e 1 per p massimale", insieme al criterio di Matlis. È molto probabile che il caso Ω = ℝ^n sia in Oberst 1990, o in Oberst 1995 (*Variations on the fundamental principle for linear systems of partial differential and difference equations with constant coefficients*, AAECC 6(4–5) (1995) 211–243, DOI 10.1007/BF01235717; abstract), o in Shankar/Pillai–Shankar. Due cose non le ho trovate nelle fonti secondarie: la versione **su ogni aperto connesso Ω** (senza iniettività di C^∞(Ω)) e la lettura come criterio d'esistenza di una traiettoria identificante.

**Prior art segnalato dall'audit (fix SYS-2).** U. Oberst, "On the minimal number of trajectories determining a multidimensional system", *Math. Control Signals Systems* 6(3) (1993) 264–288, DOI 10.1007/BF01211623. Letto **solo nell'abstract indicizzato**; il testo non è stato letto. Secondo l'abstract il lavoro determina in modo costruttivo il numero minimo μ(S) di traiettorie che generano un sistema lineare a coefficienti costanti (EDP o equazioni alle differenze), estende Heij e Zampieri, e collega i sistemi con μ(S) ≤ 1 ai sistemi principali di Macaulay. Su ℝ^n, dove C^∞ è un cogeneratore iniettivo, "u identifica P" equivale a "Sol(P) è generato da u". Quindi SYS-EX su Ω = ℝ^n è con alta probabilità il caso μ(S) ≤ 1 di Oberst 1993, presumibilmente con μ(S) = max_m dim soc_m(M_P) (almeno 1). Questo non è verificato sul testo. **Non rivendico alcuna novità su ℝ^n** (né per SYS-N1 e SYS-T0, il cui caso n = 1 è classico: Heij, Oberst).
**Riclassificazione post-Gate 8 (CIT-AUDIT-8 §3, §5; rischio di novità altissimo).** Oltre a Oberst 1993, CIT-AUDIT-8 segnala:
- J.-F. Pommaret, *Macaulay inverse systems revisited*, arXiv:0902.2314v2 (2010), Thm 5.2.5, letto in testo pieno da CIT-AUDIT-8 (non da me): dà la formula max_m dim soc_m;
- F. S. Macaulay §82: per moduli di lunghezza finita "zoccoli ≤ 1" è la condizione classica di tipo 1 (Gorenstein, sistemi principali).
Di conseguenza **SYS-EX, SYS-N1 e SYS-T0 su Ω = ℝ^n sono NOTI** e non sono un contributo di questo pacchetto. SYS-T0 è interamente noto: in n = 1 ogni aperto connesso è un intervallo, su cui C^∞ è già iniettivo.
**Delta dichiarato (unico):** SYS-EX (con SYS-N1) su un aperto connesso non vuoto Ω **arbitrario**, anche non P-convesso, dove C^∞(Ω) non è iniettivo (§3.3), sicché il caso ℝ^n non si trasferisce per restrizione in modo ovvio. La costruzione con funzioni intere e la lettura come criterio d'identificazione sono il mezzo della prova e il modo d'uso nel progetto, non rivendicazioni di novità; anche la riduzione SYS-T1 ↦ C3-T1 è standard. Nessuno stato del pacchetto dipende dal testo di Oberst 1990, 1993 o 1995. Resta da fare (RT-SYS, prima di ogni rivendicazione): leggere l'enunciato principale di Oberst 1993 e Oberst 1990 §2–4, per verificare che il caso Ω arbitrario non vi sia già.

---
## 2. Criterio d'esistenza di una soluzione identificante (zoccoli ≤ 1)

### [SYS-N1] Ostruzione di zoccolo — prova scritta
*Enunciato.* Sia Ω connesso e sia M un R-modulo. Se dim_ℂ soc_m(M) ≥ 2 per qualche ideale massimale m = m_λ, nessun omomorfismo M → 𝒜 è iniettivo. In particolare, se ciò vale per M = M_P, nessuna u ∈ Sol_𝒜(P) identifica P.
*Prova.* Un omomorfismo φ manda soc_{m_λ}(M) in {f ∈ 𝒜 : (∂_j − λ_j) f = 0 ∀ j}. Su Ω connesso questo spazio è ℂ e^{λ·x}: si scrive f = e^{λ·x} g, si ha ∇g = 0 in 𝒟′(Ω), e quindi g è costante (anche per le distribuzioni, su un aperto connesso). Un'applicazione lineare da uno spazio di dimensione ≥ 2 a uno di dimensione 1 non è iniettiva. ∎

### [EX-L1] Unicità di Fourier–Laplace sui momenti — prova scritta
*Enunciato.* Sia ν una misura boreliana complessa a supporto compatto in ℂ^n, e sia Λν(x) := ∫ e^{ζ·x} dν(ζ). Se Λν = 0 su un aperto non vuoto Ω ⊆ ℝ^n, allora ∫ h dν = 0 per ogni polinomio h ∈ ℂ[ζ].
*Prova.* Λν si estende a una funzione intera di x ∈ ℂ^n (si deriva sotto il segno d'integrale: il supporto è compatto). Una funzione intera nulla su un aperto non vuoto di ℝ^n è nulla: per il principio d'identità tutte le sue derivate si annullano in un punto di Ω. Allora ∂_x^α Λν(0) = ∫ ζ^α dν = 0 per ogni α. ∎

### [EX-L2] Sezioni reali di una varietà irriducibile — prova scritta (con fatti standard di geometria algebrica)
*Enunciato.* Sia q ⊂ R un primo con d := dim V(q) ≥ 1. Esistono forme lineari ℓ = (ℓ_1, …, ℓ_d), un aperto connesso U ⊆ ℂ^d con U ∩ ℝ^d ≠ ∅ e un'applicazione olomorfa s : U → V(q) con ℓ ∘ s = id_U, tali che:
(a) s(U) è un aperto (euclideo) di V(q);
(b) se r ∈ R si annulla su s(B) per una palla reale B ⊂ U ∩ ℝ^d, allora r ∈ q.
*Prova.* Normalizzazione di Noether: esistono forme lineari ℓ_1, …, ℓ_d con ℂ[ℓ] ↪ R/q finita, quindi π := ℓ|_{V(q)} : V(q) → ℂ^d è finita e suriettiva. Esiste un chiuso di Zariski proprio Δ ⊊ ℂ^d (luogo di diramazione più immagine del luogo singolare) fuori dal quale π è un rivestimento finito non ramificato di punti lisci (fatto standard: Shafarevich, *Basic Algebraic Geometry* 1, cap. II; numerazione da verificare). Δ non contiene alcun aperto non vuoto di ℝ^d, perché ℝ^d è Zariski-denso in ℂ^d. Si sceglie allora un punto reale y_0 ∉ Δ, una palla complessa U ∋ y_0 disgiunta da Δ e un foglio s del rivestimento sopra U: s(U) è aperto in V(q), quindi vale (a). Per (b): r ∘ s è olomorfa su U connesso e nulla su una palla reale di dimensione d, che è un insieme d'unicità per le funzioni olomorfe di d variabili; quindi r ∘ s ≡ 0 su U e r si annulla sull'aperto s(U) del luogo liscio di V(q). Se fosse r ∉ q, V(q) ∩ V(r) sarebbe un insieme algebrico di dimensione d − 1 (V(q) è irriducibile di dimensione d e r non vi si annulla identicamente). Non potrebbe quindi contenere l'aperto s(U), che è una varietà complessa di dimensione d (argomento dimensionale, fix SYS-1(d)). Dunque r ∈ q. Equivalentemente: r si annulla su V(q), quindi r ∈ I(V(q)) = q per il Nullstellensatz (q è primo, dunque radicale). ∎
*Forma contrapposta, usata nel Passo 2 di SYS-EX:* se h ∉ q, allora h ∘ s non è identicamente nulla su alcuna palla reale B ⊂ U ∩ ℝ^d.
Per q = 0 (V = ℂ^n) si prende ℓ = id, U = ℂ^n e s = id.

### [SYS-EX] Criterio d'esistenza — prova scritta (bersaglio di F8)
*Enunciato.* Sia Ω ⊆ ℝ^n un aperto connesso **non vuoto qualsiasi** (non serve la convessità; con Ω = ∅ si avrebbe 𝒜 = 0 e M = R soddisferebbe (ii) ma non (i), fix SYS-1(b)), sia 𝒜 ∈ {C^∞(Ω), 𝒟′(Ω)} e sia M un R-modulo finitamente generato. La connessione serve solo per (i) ⇒ (ii); (ii) ⇒ (i) vale su ogni aperto non vuoto. Sono equivalenti:
(i) esiste un omomorfismo iniettivo M ↪ 𝒜;
(ii) dim_ℂ soc_m(M) ≤ 1 per ogni ideale massimale m di R.
In particolare, per P ∈ R^{l×k}: **esiste u ∈ Sol_𝒜(P) che identifica P ⟺ dim_ℂ Hom_R(R/m, M_P) ≤ 1 per ogni m massimale.** In tal caso u si può prendere in C^∞(Ω).

*Prova.* (i) ⇒ (ii) è SYS-N1.

(ii) ⇒ (i). Si fissa una famiglia essenziale {x_{p,j}} di M (SYS-L1) e si pone E = ⊕ R x_{p,j} ≅ ⊕_p (R/p)^{μ_p}. Per (ii) e SYS-L1 si ha μ_m ≤ 1 per ogni primo massimale m. La prova ha tre passi.

*Passo 1 (funzioni per i primi non massimali).* Per ogni primo q ∈ Ass(M) non massimale si fissano ℓ, U, s come in EX-L2 e μ_q palle reali chiuse B_{q,1}, …, B_{q,μ_q} ⊂ U ∩ ℝ^d, a due a due disgiunte. Si pone
  f_{q,j}(x) := ∫_{B_{q,j}} e^{s(y)·x} dy  (x ∈ ℝ^n).
f_{q,j} è la restrizione di una funzione intera e r(∂) f_{q,j} = ∫_{B_{q,j}} r(s(y)) e^{s(y)·x} dy. Se r ∈ q, allora r(s(y)) = 0, perché s(y) ∈ V(q); dunque q f_{q,j} = 0. Per i primi massimali m_λ ∈ Ass(M), che hanno μ = 1, si pone f_λ(x) := e^{λ·x}. Esempio (SymPy G3): per q = (τ − ξ²) (calore) con ℓ = ξ e s(y) = (y², y), f(t, x) = ∫_0^1 e^{y² t + y x} dy risolve f_t = f_xx.

*Passo 2 (ψ : E → C^∞(ℝ^n), x_{p,j} ↦ f_{p,j}, è ben definita e iniettiva anche ristretta a Ω).* La buona definizione segue dal Passo 1. Per l'iniettività di E → C^∞(Ω) si ragiona così (riduzione autosufficiente, fix SYS-1(a)). Se ker(ρ_Ω ∘ ψ) ≠ 0, esso ha un primo associato q ∈ Ass(E) = Ass(M) e contiene un elemento z ≠ 0 con Ann(z) = q. Scritto z = Σ c_{p,j} x_{p,j} con c_{p,j} ∈ R/p, si ha Ann(z) = ∩_{c_{p,j} ≠ 0} p, perché ogni R/p è un dominio. Quindi ogni p presente contiene q, e q stesso è presente: un'intersezione finita di primi uguale al primo q contiene il prodotto dei primi, quindi q contiene uno di essi, che allora è uguale a q. I primi incomparabili con q non compaiono mai. Applicando ρ_Ω ∘ ψ a z si ottengono q ∈ Ass(M) e una relazione su Ω
  Σ_j r_{q,j}(∂) f_{q,j} + Σ_{p ⊋ q} Σ_j r_{p,j}(∂) f_{p,j} = 0  con qualche r_{q,j} ∉ q.
- Se q è massimale, la relazione contiene solo il termine r(∂)e^{λ·x} = r(λ)e^{λ·x} (non ci sono primi ⊋ q), quindi r(λ) = 0 e r ∈ m_λ: contraddizione.
- Se q non è massimale, il primo membro è Λν per la misura a supporto compatto ν = ν_q + ν′, dove ν_q := Σ_j s_*((r_{q,j} ∘ s) 1_{B_{q,j}} dy) e ν′ è supportata in ∪_{p ⊋ q} V(p) (pezzi s_p(B) e punti λ). Per EX-L1, ∫ h dν = 0 per ogni polinomio h.
  - Si sceglie h_0 ∈ ∏_{p ⊋ q} p con h_0 ∉ q. È possibile: ogni p ⊋ q non è contenuto in q e q è primo. h_0 si annulla su ∪_{p ⊋ q} V(p), quindi h_0 ν′ = 0.
  - Con h = h_0 · g(ℓ), dove g è un polinomio qualsiasi in d variabili, si ottiene Σ_j ∫_{B_{q,j}} g(y) F_j(y) dy = 0, con F_j := (h_0 ∘ s)(r_{q,j} ∘ s), continua sull'unione disgiunta dei compatti B_{q,j}.
  - Per Stone–Weierstrass i polinomi complessi g sono densi in C(∪_j B_{q,j}): l'algebra è chiusa per coniugio sulle variabili reali y e separa i punti. Quindi ogni F_j ≡ 0 su B_{q,j}.
  - h_0 ∘ s non è identicamente nulla su B_{q,j}, per EX-L2(b) in forma contrapposta (h_0 ∉ q); è reale-analitica su B_{q,j}, quindi il suo luogo di zeri in B_{q,j} ha misura nulla (fix SYS-1(c)), r_{q,j} ∘ s = 0 su un sottoinsieme denso di B_{q,j}, e per continuità ovunque su B_{q,j}. Per EX-L2(b) r_{q,j} ∈ q per ogni j: contraddizione.

*Passo 3 (estensione da E a M).* C^∞(ℝ^n) è un R-modulo iniettivo (principio fondamentale di Ehrenpreis–Malgrange–Palamodov; Malgrange, Sém. Bourbaki exp. 246, 1962–63, vol. 8, pp. 79–89; Oberst 1990, citato senza aver letto le pagine pertinenti; CON-FONTE). Quindi ψ : E → C^∞(ℝ^n) si estende a Ψ : M → C^∞(ℝ^n). Sia ρ_Ω la restrizione a Ω. ker(ρ_Ω ∘ Ψ) ∩ E = ker(ρ_Ω ∘ ψ) = 0 per il Passo 2, quindi ρ_Ω ∘ Ψ è iniettiva per SYS-L0. Poiché C^∞(Ω) ⊂ 𝒟′(Ω), lo stesso omomorfismo è un'immersione anche in 𝒟′(Ω).

*Ultima frase.* Con M = M_P e φ l'immersione, si pone u := (φ(e_1), …, φ(e_k)) ∈ C^∞(Ω)^k, dove e_i sono le classi dei vettori unitari. Allora r(∂)u = φ([r]), quindi u ∈ Sol(P) e Ann(u) = {r : [r] ∈ ker φ} = U_P. ∎

*Osservazioni.*
1. La prova non usa l'iniettività di C^∞(Ω), che è falsa per Ω non P-convesso (§3.3). Usa solo quella di C^∞(ℝ^n) e la rigidità delle funzioni intere costruite.
2. **[SYS-EX-C] Corollario (Bass di C^∞).** Per p non massimale, (R/p)^N ↪ C^∞(Ω) per ogni N (Passo 2 con M = (R/p)^N); per m massimale si ha dim soc_m(C^∞(Ω)) = 1. Su Ω convesso, dove I := C^∞(Ω) è iniettivo: da (R/p)^N ↪ I segue E(R/p)^N ↪ I (l'inviluppo iniettivo di un sottomodulo di un iniettivo vi si immerge), e l'immagine è un addendo diretto perché E(R/p)^N è iniettivo; quindi μ_p(I) ≥ N per ogni N (fix SYS-12). Dunque μ_p(C^∞(Ω)) = ∞ per p non massimale e μ_m = 1. È la verifica chiesta da O8 ("molteplicità di E(R/p) in C^∞").
3. La u identificante non è mai EP se M_P non ha lunghezza finita (SYS-R1).
4. Decidibilità: la condizione (ii) è calcolabile, perché soc_m(M) ≠ 0 solo per m ∈ Ass(M), i primi associati massimali si ottengono per decomposizione primaria di moduli (Eisenbud–Huneke–Vasconcelos, Invent. Math. 110 (1992) 207–235), e dim soc_m = dim_ℂ Hom(R/m, M) è algebra lineare su un quoziente di lunghezza finita (Hom(R/m, M) = Hom(R/m, H^0_m(M))). Il test su una u **data** resta invece non certificabile da dati finiti (C3-P1).
5. *Prior art (fix SYS-2, riclassificato post-Gate 8).* Per Ω = ℝ^n SYS-EX è **NOTO**: caso μ(S) ≤ 1 di U. Oberst, *Math. Control Signals Systems* 6(3) (1993) 264–288 (letto solo nell'abstract); formula max_m dim soc_m in Pommaret 2010, Thm 5.2.5; tipo 1 in Macaulay §82 (dettagli in §1). L'unico delta dichiarato è Ω arbitrario; lo stato di SYS-EX su Ω arbitrario poggia sulla prova scritta qui, non sul testo di Oberst.

### [SYS-T0] Sistemi di EDO — prova scritta (corollario di SYS-EX); risultato NOTO (post-Gate 8: in n = 1 nessun delta)
*Enunciato.* n = 1, R = ℂ[s], I intervallo aperto, P ∈ R^{l×k} di rango r con fattori invarianti e_1 | … | e_r. Esiste u ∈ Sol_{C^∞(I)}(P) che identifica P ⟺ e_1 = … = e_{r−1} = 1 ⟺ il gcd dei minori (r−1)×(r−1) di P è 1 (per r ≤ 1 la condizione è vuota).
*Prova.* Per la forma di Smith, M_P ≅ ⊕_{i ≤ r} ℂ[s]/(e_i) ⊕ ℂ[s]^{k−r}. Si ha dim soc_{(s−λ)}(M_P) = #{i : e_i(λ) = 0}, perché ogni addendo ciclico di torsione con λ come radice ha zoccolo di dimensione 1 in λ e quelli liberi hanno zoccolo 0. Siccome e_i | e_r, la condizione "≤ 1 per ogni λ" equivale a: e_{r−1} non ha radici, cioè e_1 = … = e_{r−1} = 1. Il gcd dei minori di ordine r − 1 è e_1 ⋯ e_{r−1}. Si conclude con SYS-EX. ∎ Esempi (SymPy G1–G2): diag(s−1, s−1) non è mai identificabile; [[s−1, 1], [0, s−2]] è identificata da u = (a e^x − b e^{2x}, b e^{2x}) con ab ≠ 0.

### [SYS-C1] Sistemi quadrati non singolari in n ≥ 2 variabili — prova scritta
*Enunciato.* Siano n ≥ 2 e P ∈ R^{k×k} con det P ≠ 0. Allora soc_m(M_P) = 0 per ogni m massimale, quindi su ogni Ω aperto connesso esiste u ∈ Sol(P) che identifica P. Inoltre Ass(M_P) è costituito dai primi di altezza 1 che dividono det P.
*Prova.* La successione 0 → R^{1×k} → R^{1×k} → M_P → 0 (moltiplicazione a destra per P) è esatta, perché det P ≠ 0 rende P iniettiva. Applicando Hom_R(R/m, −) si ottiene la successione esatta Hom(R/m, R^k) → Hom(R/m, M_P) → Ext¹_R(R/m, R)^k. Il primo termine è nullo (R è un dominio). Il terzo è nullo perché grade(m, R) = n ≥ 2 (m è generato dalla successione regolare ζ_j − λ_j), e quindi Ext^i(R/m, R) = 0 per i < n (caratterizzazione della profondità tramite Ext; complesso di Koszul). Dunque soc_m(M_P) = 0 e si applica SYS-EX.
Per Ass(M_P) servono due inclusioni.
- ⊆: pd M_P ≤ 1, quindi per Auslander–Buchsbaum depth M_p ≥ ht p − 1 per ogni primo p. Se p ∈ Ass(M_P), allora depth M_p = 0, quindi ht p ≤ 1; p ≠ 0 perché M_P è di torsione, e p ⊇ Ann(M_P) ⊇ (det P), quindi p è un fattore primo di det P.
- ⊇ (fix SYS-3): Supp M_P = V(Fitt_0(M_P)) = V(det P). Se f è un fattore primo di det P, (f) contiene det P, quindi sta nel supporto; ha altezza 1 ed è minimale nel supporto, perché l'unico primo più piccolo è 0 e 0 ∉ Supp M_P (M_P è di torsione). I primi minimali del supporto sono associati, quindi (f) ∈ Ass(M_P). ∎
*Conseguenze.* Dirac 3+1, Klein–Gordon matriciale e Lamé (§4) hanno sempre un dato identificante, anche con molteplicità di Bass ≥ 2: la molteplicità sui primi non massimali non ostruisce mai l'esistenza, ma solo la scelta di u (il test SYS-T1 diventa un'indipendenza R/p-lineare).

---
## 3. SYS-S1: somma di nuclei e minimo comune multiplo sinistro, anche su Ω non convesso

Siano Q_1 ∈ R^{a×k} e Q_2 ∈ R^{b×k} con U_P ⊆ U_{Q_i}. Si pongono U_i := U_{Q_i} e N := R^{1×k}/(U_1 + U_2).

### [SYS-S1(i⇒)] Su ogni aperto Ω — prova scritta
*Enunciato.* Se Sol_𝒜(Q_1) + Sol_𝒜(Q_2) = Sol_𝒜(P), allora U_1 ∩ U_2 = U_P. Vale per ogni aperto non vuoto Ω e per 𝒜 ∈ {C^∞, 𝒟′}.
*Prova.* Sia r ∈ (U_1 ∩ U_2) ∖ U_P. r(∂) annulla Sol(Q_1) + Sol(Q_2). Si ha 0 ≠ [r] ∈ M_P e R[r] ≅ R/Ann([r]). Si sceglie m_λ ⊇ Ann([r]) massimale e il morfismo R[r] → R/m_λ → C^∞(ℝ^n) che manda [r] in e^{λ·x}. Lo si estende a M_P → C^∞(ℝ^n) (iniettività, come nel Passo 3 di SYS-EX) e lo si restringe a Ω. Si ottiene v ∈ Sol_Ω(P) con r(∂)v = e^{λ·x} ≠ 0, quindi v ∉ Sol(Q_1) + Sol(Q_2). ∎

### [SYS-S1(i⇐)] Sotto Ext¹(N, 𝒜) = 0; caso N di lunghezza finita con H¹_dR(Ω) = 0 — prova scritta
*Successione.* Se U_1 ∩ U_2 = U_P, la successione 0 → M_P → M_{Q_1} ⊕ M_{Q_2} → N → 0, con [r] ↦ ([r], [r]) e ([a], [b]) ↦ [a − b], è esatta.
- Al centro: se a − b ∈ U_1 + U_2, a − b = c_1 + c_2, allora con r := a − c_1 = b + c_2 si ha ([a], [b]) = ([r], [r]).
- A sinistra: il nucleo è (U_1 ∩ U_2)/U_P = 0.
Applicando Hom_R(−, 𝒜) si ottiene
  0 → Sol(N) → Sol(Q_1) ⊕ Sol(Q_2) → Sol(P) → Ext¹_R(N, 𝒜),
dove la terza freccia è (v_1, v_2) ↦ v_1 + v_2.
*Enunciato.* (a) Se Ext¹_R(N, 𝒜) = 0, allora U_1 ∩ U_2 = U_P ⇒ Sol(Q_1) + Sol(Q_2) = Sol(P). È il caso di Ω convesso, dove 𝒜 è iniettivo: ritrova F6-SYS.
(b) Se N ha lunghezza finita e H¹_dR(Ω) = 0 (per esempio Ω semplicemente connesso), allora Ext¹_R(N, 𝒜) = 0 per 𝒜 ∈ {C^∞(Ω), 𝒟′(Ω)}, quindi vale (a).
*Prova di (b).* La risoluzione di Koszul di R/m_λ (la successione ζ_j − λ_j è regolare) dà Ext^p_R(R/m_λ, 𝒜) = H^p del complesso di Koszul degli operatori (∂_j − λ_j) su 𝒜. Il coniugio f ↦ e^{−λ·x} f lo trasforma nel complesso di Koszul di (∂_1, …, ∂_n), cioè nel complesso di de Rham di Ω, con coefficienti C^∞ (forme) o 𝒟′ (correnti di grado 0 nei coefficienti). Quindi Ext¹(R/m_λ, 𝒜) ≅ H¹_dR(Ω; ℂ), che è 0 per ipotesi; per le correnti si usa il teorema di de Rham (la coomologia delle correnti coincide con quella liscia). N ha una serie di composizione con fattori R/m_λ. Per una successione esatta 0 → N′ → N → R/m → 0, la successione lunga di Ext(−, 𝒜) contiene il tratto Ext¹(R/m, 𝒜) → Ext¹(N, 𝒜) → Ext¹(N′, 𝒜) (fix SYS-6(b): il verso è questo, perché Ext(−, 𝒜) è controvariante). Se il primo e il terzo termine sono nulli lo è anche il secondo, quindi Ext¹(N, 𝒜) = 0 per induzione sulla lunghezza. ∎
*Riduzione scalare.* Per k = 1, **n = 2** e Q_1, Q_2 coprimi, N = R/(Q_1, Q_2) ha lunghezza finita δ(P) e (b) ritrova C12-T1′ su Ω semplicemente connesso, che è DIMOSTRATO con un'altra tecnica. Per n ≥ 3 la coprimalità non basta: Q_1 = ζ_1 e Q_2 = ζ_2 danno N = ℂ[ζ_3], di lunghezza infinita (fix SYS-6(a)).

### [SYS-S1-C] FALSO in generale su Ω semplicemente connesso non convesso (N di lunghezza infinita) — controesempio, SymPy E1–E3
*Enunciato.* Esistono Ω ⊂ ℝ² aperto, connesso e semplicemente connesso, e Q_1, Q_2 ∈ R^{1×2} tali che U_1 ∩ U_2 = U_P ma Sol_{C^∞(Ω)}(Q_1) + Sol_{C^∞(Ω)}(Q_2) ⊊ Sol_{C^∞(Ω)}(P).
*Costruzione.* Coordinate (t, x).
- Ω := (0,3)_t × (0,3)_x ∖ ([1,3)_t × [1,2]_x), un dominio "a U". È connesso e semplicemente connesso: è omeomorfo a un disco, retraendo i due bracci sulla base (0,1) × (0,3).
- k = 2, Q_1 = (1, 0), Q_2 = (1, ∂_x), cioè U_1 = R(1, 0) e U_2 = R(1, ξ).
- U_1 ∩ U_2 = 0: da a(1, 0) = b(1, ξ) segue bξ = 0, quindi b = 0 e a = 0. Dunque P = 0 (nessuna equazione), U_P = 0 = U_1 ∩ U_2 e Sol(P) = 𝒜².
- U_1 + U_2 = R(1,0) + R(0,ξ), quindi N ≅ R/(ξ), di lunghezza infinita.
- Sol(Q_1) = {(0, g)} e Sol(Q_2) = {(−∂_x h, h)}, quindi Sol(Q_1) + Sol(Q_2) = {(v_1, v_2) : v_1 ∈ ∂_x C^∞(Ω)}.
*∂_x non è suriettivo su C^∞(Ω).*
- Si fissano ρ ∈ C_c^∞((1,2)) con ∫ρ = 1 e β ∈ C^∞(ℝ) con β = 0 su (−∞, 1/2] e β = 1 su [3/4, ∞). In particolare **β(1) ≠ 0** e supp ρ ⊂ (1, 2): sono le ipotesi usate anche nella parte 𝒟′ qui sotto (DEVIL-8, O21).
- Si pone f(t, x) := β(t) ρ(x)/(1 − t) per t < 1 e f := 0 altrove in Ω. f ∈ C^∞(Ω): i punti di Ω con t ≥ 1 hanno x ∈ (0,1) ∪ (2,3), a distanza positiva da supp ρ, quindi f ≡ 0 in un loro intorno; per t < 1 la formula è liscia.
- Se h ∈ C^∞(Ω) risolvesse ∂_x h = f, per t ∈ (3/4, 1) il segmento {t} × [1/2, 5/2] starebbe in Ω e h(t, 5/2) − h(t, 1/2) = ∫_{1/2}^{5/2} f(t, x) dx = 1/(1 − t) → +∞ per t → 1⁻.
- Ma (1, 1/2) e (1, 5/2) stanno in Ω e h è continua in entrambi, quindi la differenza resta limitata vicino a t = 1: contraddizione.
Dunque (−f, 0) ∈ Sol(P) ∖ (Sol(Q_1) + Sol(Q_2)). ∎
*Lettura.* L'ostruzione è la mappa di connessione Sol(P) → Ext¹(N, 𝒜) = C^∞(Ω)/∂_x C^∞(Ω) ≠ 0: è la mancanza di P-convessità di Ω per ∂_x, non la topologia. L'ipotesi "semplicemente connesso" basta solo quando N ha lunghezza finita (S1(i⇐)(b)).
*Portata.* Per 𝒟′(Ω) il controesempio richiede che ∂_x non sia suriettivo su 𝒟′(Ω) dello stesso Ω. Questo punto era aperto (Q-S8SYS-2) ed è chiuso dal fix SYS-5 qui sotto.

*Variante con P ≠ 0 (fix SYS-4, verificata dal revisore).* Il caso P = 0 è formalmente accettabile (U_P = 0). Una variante con un'equazione vera: k = 3, Q_1 = [(1, 0, 0); (0, 0, τ)], Q_2 = [(1, ξ, 0); (0, 0, τ)], P = (0, 0, τ). Allora U_1 ∩ U_2 = R(0, 0, τ) = U_P, e N ≅ R/(ξ) ⊕ R/(τ) ha lunghezza infinita. Si ha Sol(P) = {(w_1, w_2, w_3) : ∂_t w_3 = 0} e Sol(Q_1) + Sol(Q_2) = {(v_1, ·, w_3) : v_1 ∈ ∂_x C^∞(Ω), ∂_t w_3 = 0}. Con la stessa f, (−f, 0, 0) ∈ Sol(P) sta fuori dalla somma.

*Estensione a 𝒟′(Ω) (fix SYS-5; prova del revisore S-CHECK-F8-SYS, integrata qui; da far rivedere a DEVIL-8).*
- *L'f di sopra non basta in 𝒟′.* Con f = β(t)ρ(x)/(1 − t), l'equazione ∂_x h = f è risolubile in 𝒟′(Ω). Si pone h = F := ∫_{1/2}^x f nella parte t < 1, h = 0 sul braccio x < 1 e h = T(t) sul braccio x > 2, con T := d/dt[−β log|1 − t|] + β′ log|1 − t| ∈ 𝒟′((0,3)). Per t < 1, T vale β/(1 − t); i tre pezzi si incollano.
- *Con un'altra f il controesempio vale in 𝒟′.* Ipotesi: β(1) ≠ 0 e supp ρ ⊂ (1, 2) (O21; valgono per la scelta di sopra, dove β = 1 vicino a t = 1). Si pone f(t, x) := β(t) ρ(x) e^{1/(1−t)} per t < 1 e f := 0 altrove in Ω. f ∈ C^∞(Ω) per lo stesso motivo di prima. Sia h ∈ 𝒟′(Ω) con ∂_x h = f.
- Sui rettangoli A = (0,1) × (0,3), B = (0,3) × (0,1) e C = (0,3) × (2,3), le soluzioni distribuzionali di ∂_x(·) = 0 sono della forma k(t) ⊗ 1. Quindi h = F + k_A(t) su A, h = k_B(t) su B e h = k_C(t) su C, con F := ∫_{1/2}^x f.
- Su A ∩ B si ha F = 0, quindi k_A = k_B su (0,1). Su A ∩ C si ha F = β(t)e^{1/(1−t)}, quindi k_C − k_B = β e^{1/(1−t)} su (0,1).
- Ma k_C − k_B ∈ 𝒟′((0,3)), mentre e^{1/(1−t)} non si estende a una distribuzione vicino a t = 1. Si prende φ_ε ≥ 0 supportata in [1 − 2ε, 1 − ε], con |φ_ε^{(j)}| ≤ C_j ε^{−j} e ∫φ_ε ≥ cε. Allora ⟨e^{1/(1−t)}, φ_ε⟩ ≥ c ε e^{1/(2ε)}, mentre un'estensione di ordine N darebbe una stima O(ε^{−N}). Contraddizione.
Dunque SYS-S1(⇐) senza ipotesi su N è FALSO anche in 𝒟′(Ω), e Q-S8SYS-2 è chiusa.

### [SYS-S1(ii)] Intersezione e ambiguità — prova scritta
Sol(Q_1) ∩ Sol(Q_2) = Sol(N) su ogni Ω: u è annullata da U_1 e da U_2 se e solo se è annullata da U_1 + U_2. Su Ω connesso dim_ℂ Sol(N) < ∞ ⟺ N ha lunghezza finita, e in tal caso Sol(N) ⊂ EP.
- (⇐) Per induzione sulla lunghezza, con dim Hom(R/m, 𝒜) = 1 (SYS-N1) e l'esattezza a sinistra di Hom: dim Sol(N) ≤ ℓ(N). Inoltre Ann(N) ⊇ ∏ m_i^e ha colunghezza finita, quindi Sol(N) ⊆ Sol(∏ m_i^e) ⊂ EP (C3-L3 per ideali di colunghezza finita).
- (⇒) Se N non ha lunghezza finita, Ass(N) contiene un primo non massimale p e R/p ↪ N. Le funzioni f_g := ∫_B e^{s(y)·x} g(y) dy, con g polinomio, sono in Sol(p), sono intere e sono linearmente indipendenti su Ω (EX-L1 più Stone–Weierstrass). Il morfismo R/p → C^∞(ℝ^n), 1 ↦ f_g, si estende a N (iniettività di C^∞(ℝ^n)) e si restringe a Ω. Si ottengono così infinite soluzioni linearmente indipendenti, distinte già sull'immagine del generatore di R/p.
- *Uguaglianza dim Sol(N) = ℓ(N) (fix SYS-7).* Su Ω connesso, il sottomodulo di m_λ-torsione di 𝒜 è e^{λ·x}ℂ[x] (si coniuga con e^{λ·x} e si usa che le soluzioni di ∂^α g = 0 per |α| grande sono polinomi), ed è isomorfo all'inviluppo iniettivo E_R(R/m_λ) (sistemi inversi di Macaulay, caratteristica 0). Per N di lunghezza finita, N = ⊕_λ N_λ (componenti primarie) e Hom(N, 𝒜) = ⊕_λ Hom(N_λ, E(R/m_λ)). Per la dualità di Matlis dim_ℂ Hom(N_λ, E(R/m_λ)) = ℓ(N_λ), quindi dim Sol(N) = Σ_λ ℓ(N_λ) = ℓ(N).
δ_sys := ℓ(N) = dim Sol(N) nel caso finito. Per k = 1 coincide con δ(P) di C12-T1′.

---
## 4. Lamé, n = 3 (facoltativo, chiude Q-SYS-5) — prova scritta, SymPy D1–D7
P(τ, ξ) = ρτ² I_3 − μ|ξ|² I_3 − (λ+μ) ξξᵀ, che è l'operatore di ρ u_tt − μΔu − (λ+μ)∇ div u. Ipotesi: ρ, μ ≠ 0, λ + μ ≠ 0 e **λ + 2μ ≠ 0** (fix SYS-8; fisicamente λ + 2μ > 0). Senza l'ultima ipotesi l'enunciato è falso: con λ = −2μ si ha q_P = ρτ², che non è primo, det P = ρτ² q_S² e Ass(M_P) = {(τ), (q_S)}. Anche ρ ≠ 0 serve: dà (q_P, q_S) = (τ², |ξ|²), di altezza 2 (punto 3). Si pongono q_P := ρτ² − (λ+2μ)|ξ|² e q_S := ρτ² − μ|ξ|².
1. **Struttura.** det P = q_P q_S² (D1); q_P e q_S sono quadriche di rango 4 in 4 variabili, irriducibili e distinte (D6). Per SYS-C1, Ass(M_P) = {(q_P), (q_S)}. P mod q_S ha rango 1 e P mod q_P ha rango 2 (D5). Su R_{(q_S)}, che è un DVR, la forma di Smith ha due esponenti non nulli con somma 2, quindi M_{(q_S)} ≅ κ(q_S)²; analogamente M_{(q_P)} ≅ κ(q_P). Dunque **μ_{q_P} = 1 e μ_{q_S} = 2**, la previsione di F6-SYS.
2. **Esistenza.** Per SYS-C1 esiste sempre un campo di spostamento che identifica Lamé.
3. **Sottomodulo essenziale.** Sia E ⊆ M_P generato dalla riga d := ξᵀ (div) e dalle righe c_1, c_2, c_3 di [ξ]_× (rot).
   - ξᵀP = q_P ξᵀ (D2) e [ξ]_× P = q_S [ξ]_× (D3), quindi q_P d = 0 e q_S c_i = 0 in M_P.
   - Helmholtz (D4): |ξ|² I = ξξᵀ − [ξ]_×², quindi |ξ|² M_P ⊆ E.
   - |ξ|² ∉ (q_P) ∪ (q_S) (D7) non è divisore di zero su M_P, perché non sta in alcun primo associato. Dunque E è essenziale: se x ≠ 0, allora 0 ≠ |ξ|² x ∈ E.
   - R d ∩ Σ R c_i = 0: un elemento comune è annullato da (q_P, q_S), che ha altezza 2, mentre Ass(M_P) contiene solo primi di altezza 1.
4. **Test (SYS-L0 su E).** u ∈ Sol(Lamé) identifica Lamé se e solo se valgono (a) e (b):
   (a) Ann(div u) = (q_P): div u non soddisfa alcuna equazione oltre a quella delle onde P (test scalare C3-T1, versione n ≥ 3);
   (b) se Σ_i r_i(∂)(rot u)_i = 0 con r ∈ R^3, allora esiste b ∉ (q_S) con b r ∈ q_S R^3 + R ξ.
   Inoltre nessuna relazione mista tra div u e rot u può violare il test, perché i due pezzi hanno primi incomparabili (SYS-T1).
   *Prova di (b).* Σ r_i c_i = 0 in M_P ⟺ è 0 in M_{(q_S)} (è già 0 in M_{(q_P)}, dove q_S è un'unità). M_{(q_S)} = κ^{1×3}/κ ξᵀ con κ = κ(q_S), perché la riga di P̄ = −(λ+μ)ξξᵀ genera κξᵀ. Le classi c̄_i generano ξ^⊥ mod κξ, che ha dimensione 2, dato che ξ·ξ ≠ 0 in κ. Infine r̄ᵀ[ξ]_× ∈ κξ ⟺ r̄ × ξ = 0 ⟺ r̄ ∈ κξ ⟺ ∃ b ∉ q_S con b r ∈ q_S R^3 + Rξ. ∎
*Lettura fisica.* Un singolo campo identifica Lamé se e solo se la parte P (div) e la parte S (le due polarizzazioni trasverse di rot u, legate solo da div rot = 0) non soddisfano equazioni in più. Un campo di sole onde P (rot u = 0) non identifica mai: il test (b) fallisce con r = e_i.

---
## 5. SYS-E: P1-T5 per sistemi (versione corretta F2) e Wei–Norman su sl_2 ⊗ ℂ[ξ]
Dirac 1+1 come evoluzione: ψ_t = A(∂_x)ψ con A(ξ) = X + mY, X := iξσ_z (trasporto), Y := −iσ_x (massa per unità di massa). L'algebra pertinente è 𝒜 = Mat_2(ℂ[ξ]) sulla base ℂ: gli operatori differenziali matriciali a coefficienti costanti (DEVIL-6, O2).

### [SYS-E1] (H) vale per Dirac 1+1, quindi P1-T5 si applica — prova scritta, SymPy A1–A2
*Enunciato.* X, Y_0 := Y, Y_k := ad_X^k Y sono linearmente indipendenti su ℂ. Di conseguenza, per P1-T5 (`work/P1/CHECK_REQUEST.md` §C, DIMOSTRATO), non esistono una parola finita (Z_1, …, Z_d) ∈ {X, Y}^d e funzioni g_i(t, m) olomorfe vicino a (0, 0), con g_i(0, m) = 0 e g_i(t, 0) ≡ 0 quando Z_i = Y, tali che e^{t(X+mY)} = ∏_i e^{g_i(t,m) Z_i} in 𝒜[[t]] per ogni m vicino a 0.
*Prova.* Si usano [σ_z, σ_x] = 2iσ_y e [σ_z, σ_y] = −2iσ_x. Allora ad_X(σ_x) = iξ[σ_z, σ_x] = −2ξσ_y e ad_X(σ_y) = 2ξσ_x. Per induzione Y_k = c_k ξ^k σ_x per k pari e Y_k = c_k ξ^k σ_y per k dispari, con c_k ∈ ℂ ∖ {0}. Questi elementi hanno gradi in ξ distinti, quindi sono indipendenti; X = iξσ_z ha una componente su σ_z, assente in tutti gli Y_k, quindi resta indipendente da essi. (SymPy A1: rango 10/10 per X, Y_0, …, Y_8.) ∎
*Lettura.* Nessuna formula chiusa che sia prodotto finito di flussi di trasporto e di massa, con tempi indipendenti da ξ e analitici in (t, m), rappresenta il propagatore di Dirac in modo uniforme nella massa. "P1-T5 non si applica ai sistemi" è FALSO (F2).

### [SYS-E2] L'algebra generata è la current algebra torcita — prova scritta, SymPy A3–A4
*Enunciato.* Lie_ℂ⟨X, Y⟩ = 𝔏^θ := {Z ∈ sl_2 ⊗ ℂ[ξ] : θ(Z) = Z}, dove θ(Z)(ξ) := σ_x Z(−ξ) σ_x. Esplicitamente 𝔏^θ = span_ℂ{ξ^{2k+1}σ_z, ξ^{2k}σ_x, ξ^{2k+1}σ_y : k ≥ 0}, di dimensione infinita su ℂ.
*Prova.* Scrivendo Z = aσ_z + bσ_x + cσ_y con a, b, c ∈ ℂ[ξ], si ha θ(Z) = −a(−ξ)σ_z + b(−ξ)σ_x − c(−ξ)σ_y. Quindi θ(Z) = Z ⟺ a e c sono dispari e b è pari. θ è un automorfismo di algebre di Lie, quindi 𝔏^θ è una sottoalgebra; contiene X e Y, quindi contiene Lie⟨X, Y⟩. Viceversa Lie⟨X, Y⟩ contiene Y_{2k} ∝ ξ^{2k}σ_x e Y_{2k+1} ∝ ξ^{2k+1}σ_y (SYS-E1), e [σ_x, ξ^{2k+1}σ_y] = 2iξ^{2k+1}σ_z, quindi contiene una base di 𝔏^θ. ∎
*Conseguenze.* (a) P1-T4 (Wei–Norman globale con d = dim 𝔤 funzioni) non si applica su ℂ: 𝔤 ha dimensione infinita, e la frase "Wei–Norman locale per sl_2" di F6-SYS è sbagliata come enunciato su ℂ. (b) Su ℂ(ξ), o puntualmente in ξ, 𝔤 ⊗ ℂ(ξ) = sl_2(ℂ(ξ)) ha dimensione 3. Le coordinate di seconda specie esistono, ma con tempi funzioni di ξ (SYS-E3).

### [SYS-E3] Euler ZXZ esplicito, tempi non polinomiali, moltiplicatori non locali — prova scritta, SymPy B1–B4
*Enunciato.* Sia m ∈ ℝ ∖ {0} e ω := √(ξ² + m²). Per ξ ∈ ℝ si pongono
  b(t, ξ) := −arcsin(m sin(ωt)/ω),  a(t, ξ) := ½ arg(cos ωt + iξ sin(ωt)/ω)  (ramo continuo, a(0, ξ) = 0).
Allora:
(a) e^{tA(ξ)} = e^{iaσ_z} e^{ibσ_x} e^{iaσ_z}, cioè e^{tA} = e^{g_1X} e^{g_2(mY)} e^{g_1X} con g_1 = a/ξ e g_2 = −b/m. La decomposizione vale per ogni t ∈ ℝ se ξ ≠ 0, e per |t| < π/(2|m|) anche in ξ = 0.
(b) Per |t| < π/(2|m|) i tempi g_1 e g_2 sono funzioni analitiche reali di ξ ∈ ℝ, ma g_2 non è un polinomio in ξ, e g_1 non lo è perché g_1 → t/2 per |ξ| → ∞ (a ≈ ωt/2 sul ramo continuo) senza essere costante (g_1 → tan(mt)/(2m) per ξ → 0). A t = π/(2|m|), g_1 diverge per ξ → 0 (blocco cardanico).
(c) Il moltiplicatore di Fourier e^{g_2(t, ∂_x) mY}, di simbolo e^{ib(t,ξ)σ_x}, non è un operatore locale.
*Prova.* (a) Con A² = −ω² I si ha e^{tA} = cos ωt I + (sin ωt/ω) A (SYS-NOTE F2–F3). Il prodotto ZXZ ha elementi (11) = cos b e^{2ia}, (12) = (21) = i sin b, (22) = cos b e^{−2ia}. Confrontando con e^{tA}: (12) = −im sin(ωt)/ω dà sin b = −m sin(ωt)/ω. Inoltre |cos ωt + iξ sin(ωt)/ω|² = 1 − m² sin²(ωt)/ω² = cos² b, con cos b > 0 quando |m sin(ωt)/ω| < 1, e questo dà a. L'argomento di arcsin ha modulo 1 solo se ξ = 0 e |sin mt| = 1; il numero cos ωt + iξ sin(ωt)/ω si annulla solo se ξ = 0 e cos mt = 0. Fuori da questi casi tutto è analitico. (SymPy B1: errore 3.8e−16.)
(b) Per |ξ| → ∞, |b| ≤ arcsin(|m|/|ξ|) → 0, mentre b(t, 0) = −arcsin(sin mt) = −mt ≠ 0 per 0 < |t| < π/(2|m|). Un polinomio limitato su ℝ è costante, quindi b non è polinomiale (B2). a è dispari in ξ e analitica, quindi a/ξ è analitica in ξ = 0 con limite tan(mt)/(2m) (B3). A t = π/(2|m|) e per ξ → 0^±, l'argomento tende a ±π/2, quindi a → ±π/4 e g_1 → ±∞ (B4).
(c) Il simbolo è liscio e limitato, quindi il nucleo di convoluzione è una distribuzione temperata. Un operatore di convoluzione è locale se e solo se il suo nucleo ha supporto in {0}, cioè (Schwartz) è una combinazione finita di derivate di δ, cioè se e solo se il simbolo è un polinomio. Basta Schwartz: il teorema di Peetre serve solo per operatori non invarianti per traslazioni (fix SYS-11(c)). Il simbolo cos b I + i sin b σ_x è liscio e limitato su ℝ, tende a I all'infinito e non è costante, quindi non è un polinomio. ∎
*Controlli del revisore (fix SYS-11(b)).* Per ξ ≠ 0 il numero cos ωt + iξ sin(ωt)/ω non si annulla mai, quindi il ramo continuo di a esiste per ogni t. Il revisore lo ha verificato numericamente, sollevando il ramo fino a t = 20 (errore 8.7·10^{−14}), e ha confermato il limite g_1 → t/2. Le ipotesi di P1-T5 in SYS-E1 (ℂ-algebra Mat_2(ℂ[ξ]), parametro ε = m) sono verificate (fix SYS-11(a)).
*Collocazione.* Il prodotto finito esiste nel dizionario dei moltiplicatori (U3 di S8-DICT), non in quello differenziale né nella classe di P1-T5. **APERTO** (Q-S8SYS-1): esistono prodotti finiti di flussi dei termini con tempi g_i ∈ ℂ[ξ][[t]] (polinomiali in ξ)? SYS-E1 esclude solo i tempi indipendenti da ξ.

---
## 6. Gauge

### [G-L0] Covarianza — prova scritta, SymPy H1
e^{−iχ}(∂_μ − i(A_μ + ∂_μχ))e^{iχ} = ∂_μ − iA_μ: si ha infatti (∂ − iA − i∂χ)(e^{iχ}f) = e^{iχ}(∂f − iAf). Quindi, per ogni operatore L_A polinomiale nelle ∇_μ = ∂_μ − iA_μ con coefficienti matriciali costanti e potenziali scalari moltiplicativi, L_{A+dχ}(e^{iχ}u) = e^{iχ} L_A u. A coefficienti costanti con χ = c·x si ha Ann(e^{ic·x}u) = σ_c Ann(u), dove σ_c(r)(ζ) = r(ζ − ic): SYS-T1, SYS-EX e C3-T1 sono covarianti.

### [G-T2] Dati invarianti ⇒ solo l'orbita; quoziente = (F, olonomie) — prova scritta, CON-FONTE in sostanza
*Enunciato.* Ω ⊆ ℝ^n aperto connesso, A, A′ ∈ C^∞(Ω; ℝ^n) (1-forme), gauge = applicazioni lisce g : Ω → U(1), che agiscono come A ↦ A + (1/i) g^{−1} dg.
(a) A′ ~ A ⟺ d(A′ − A) = 0 e ∮_γ (A′ − A) ∈ 2πℤ per ogni ciclo γ ⟺ dA′ = dA e e^{i∮_γ A′} = e^{i∮_γ A} per ogni γ. Su Ω semplicemente connesso: A′ ~ A ⟺ dA′ = dA.
(b) (DM-inv) Se un'osservazione O soddisfa O(g u) = O(u) (|ψ|², correnti bilineari, u a meno di fase), ogni procedura che ricostruisce A da O(u), con u soluzione di L_A u = 0, ricostruisce al più la classe [A].
*Prova.* (a) (⇒) Localmente g = e^{iχ} e A′ − A = dχ è chiusa; lungo γ, (1/i)∮ g^{−1}dg = 2π · (grado di g ∘ γ) ∈ 2πℤ. (⇐) B := A′ − A è chiusa con periodi in 2πℤ. g(x) := exp(i∫_{x_0}^x B) è indipendente dal cammino (due cammini differiscono per un ciclo e i periodi stanno in 2πℤ), è liscia, e (1/i) g^{−1}dg = B. La seconda equivalenza è immediata. Il caso semplicemente connesso segue dal lemma di Poincaré.
(b) Se L_A u = 0 e A′ = A + (1/i)g^{−1}dg, allora L_{A′}(g u) = g L_A u = 0 (G-L0, anche per g non della forma e^{iχ} globale) e O(g u) = O(u). Quindi i dati non distinguono A da A′. ∎
*Fonti.* Aharonov–Bohm, Phys. Rev. 115(3) (1959) 485–491, DOI 10.1103/PhysRev.115.485; Wu–Yang, Phys. Rev. D 12(12) (1975) 3845–3857, DOI 10.1103/PhysRevD.12.3845 (fattore di fase non integrabile; dati confermati da CIT-AUDIT-8). Lo stato proposto è "CON-FONTE in sostanza".
*Collegamento.* Su Ω non semplicemente connesso le olonomie sono il dato in più (effetto Aharonov–Bohm). È la stessa ipotesi topologica di C12-T1′. SYS-S1-C (§3.3) mostra però che per i sistemi la topologia non basta: serve la P-convessità.

### [SYS-N3] Schrödinger magnetico: una sola u non identifica (A, V) nemmeno a meno di gauge, anche nel caso non stazionario — prova scritta, SymPy F1–F3
*Enunciato.* Siano n ≥ 2, Ω ⊆ ℝ^n aperto, J un intervallo, e u ∈ C^∞(J × Ω) con u ≠ 0 ovunque, soluzione di i u_t = −(∇ − iA)²u + Vu con A, V reali e lisci. Si pongono ρ := |u| > 0, ∇S := Im(∇u/u), S_t := Im(u_t/u) (definiti senza scegliere un ramo di S), w := ∇S − A e j := ρ² w. Allora:
(a) la coppia (A′, V′), reale e liscia, soddisfa la stessa equazione con la stessa u se e solo se
  A′ = ∇S − j′/ρ²,  V′ = −S_t + Δρ/ρ − |j′|²/ρ⁴,  div_x j′ = −½ ∂_t(ρ²);
(b) quindi l'insieme di tali coppie è lo spazio affine (A, V) + {(−k/ρ², (|j|² − |j + k|²)/ρ⁴) : div_x k = 0}, di dimensione infinita per n ≥ 2. *Riassunto (O15):* le variazioni ammesse del potenziale sono B := A′ − A = −k/ρ² con **div(ρ²B) = 0** (non div B = 0);
(c) esistono k con d(k/ρ²) ≠ 0: le coppie corrispondenti hanno campi magnetici diversi e non sono equivalenti di gauge. Una trasformazione di gauge che fissa u è anzi g ≡ costante, perché g u = u con u ≠ 0 forza g = 1.
Il caso stazionario (u indipendente da t) è il caso ∂_tρ = 0, S_t = −E: la condizione diventa div j′ = 0 e V′ = E + Δρ/ρ − |j′|²/ρ⁴, cioè F6-SYS.
*Prova.* (a) Si scrive u = ρe^{iS} localmente; le formule usano solo ∇S e S_t, che sono globali. (∇ − iA)·(∇ − iA)(ρe^{iS}) = e^{iS}[Δρ − ρ|w|² + (i/ρ) div(ρ²w)], e i u_t = e^{iS}(iρ_t − ρS_t). Separando parte reale e immaginaria (SymPy F1):
  V = −S_t + Δρ/ρ − |w|²  e  ∂_t ρ² + 2 div(ρ² w) = 0.
Queste equazioni sono necessarie e sufficienti, e A′ entra solo tramite w′ = ∇S − A′, cioè j′ = ρ²(∇S − A′).
(b) Due soluzioni j, j′ differiscono per k con div_x k = 0; viceversa ogni tale k dà, con la formula per V′, una coppia ammissibile.
(c) Per n = 2 si prende k = ∇^⊥ψ con ψ ∈ C_c^∞(Ω) non nulla, che dà div k = 0. Allora rot(k/ρ²) = div(ρ^{−2}∇ψ), che non è identicamente nullo: se lo fosse, ψ sarebbe una soluzione a supporto compatto di un'equazione ellittica in forma di divergenza, quindi ψ ≡ 0 per il principio del massimo. Per n ≥ 3 (fix SYS-10) si prende Φ = ψ e_3 con ψ ∈ C_c^∞(Ω) non nulla, e k := rot Φ, che ha div k = 0. La componente (1,2) di d(k/ρ²) è −div_{12}(ρ^{−2}∇_{12}ψ), dove div_{12} e ∇_{12} agiscono solo su (x_1, x_2). Se fosse identicamente nulla, per ogni x_3 fissato la restrizione di ψ alla fetta sarebbe una soluzione a supporto compatto di un'equazione ellittica in forma di divergenza in (x_1, x_2). Per il principio del massimo, applicato su ogni componente connessa della fetta, ψ ≡ 0 su ogni fetta: contraddizione. Esempio esplicito in SymPy F3. ∎
*Prior art per i dati al bordo:* Sun 1993 (Trans. AMS 338, 953–969) e Nakamura–Sun–Uhlmann 1995: la mappa DN determina (dA, V) per n ≥ 3. *Contrasto:* Dirac 1+1 determina A puntualmente dove ψ_1ψ_2 ≠ 0 (Radford 1996; Booth–Legg–Jarvis 2001, J. Phys. A 34, 5667–5677): è prior art, non è un claim di S8-SYS.
*Lettura.* Il gauge crea ambiguità solo con dati invarianti (G-T2). Con il dato complesso completo l'ostacolo è il conteggio: un'equazione complessa scalare contro n + 1 incognite reali.

### [G-T0] Osservazione (declassata per F8)
Un potenziale di Maxwell che soddisfa una condizione di gauge g(∂)A = 0 ha g ∈ Ann(A) ∖ U_A, quindi non identifica mai Maxwell da solo. Se Ann(A) = U_A + Rg con g·∂ ≠ 0, allora U_A = {r ∈ Ann(A) : r·∂ = 0} (prova in `NOTE.md` §5.5). È un'osservazione, senza contenuto nuovo.

---
## 7. Risposta a "λ ∈ Mat 4×4" in forma hamiltoniana — H-DIRAC, prova scritta, SymPy C1–C7
*Classe.* 𝒞 := {L = I_4 ∂_t + Σ_{k=1}^3 α^k ∂_k + B : α^k, B ∈ Mat_4(ℂ) arbitrarie}. È la forma hamiltoniana ψ_t = −α·∇ψ − iβmψ, con B = iβm. Non si assumono le relazioni di Clifford. Dato: DM3, ψ ∈ C^∞(Ω)^4 in una base fissata.

### [H-DIRAC-1] Identificazione esatta dei coefficienti
*Enunciato.* Sia L_0 ∈ 𝒞, e sia ψ ∈ Sol(L_0) che identifica L_0 (Ann(ψ) = U_{L_0}). Se L ∈ 𝒞 e Lψ = 0, allora L = L_0: le matrici α^k e B sono determinate da ψ, senza ambiguità GL a sinistra e senza coniugio.
*Prova.* Le righe di L stanno in Ann(ψ) = R^{1×4}L_0, quindi L = V L_0 con V ∈ R^{4×4}. Sia W := V − I, così che L − L_0 = W L_0. L − L_0 = Σ(α^k − α_0^k)ξ_k + (B − B_0) non contiene τ e ha grado ≤ 1. Supponiamo W ≠ 0 e sia W_d ≠ 0 la sua componente omogenea di grado massimo d. La componente di grado d + 1 di W L_0 è W_d (τI + Σα_0^k ξ_k). È non nulla, perché det(τI + α_0·ξ) = τ^4 + … ≠ 0, quindi τI + α_0·ξ non è un divisore di zero in Mat_4(R): posto H := τI + α_0·ξ, da W_d H = 0 seguirebbe W_d (det H) = W_d H adj H = 0, quindi W_d = 0.
- Se d ≥ 1, il grado d + 1 ≥ 2 contraddice "grado ≤ 1".
- Se d = 0, W è costante e W L_0 ha coefficiente di τ uguale a W ≠ 0, mentre L − L_0 non contiene τ: contraddizione.
Dunque W = 0 e L = L_0. ∎
*Lettura.* L'ambiguità D ~ VD della forma covariante γ^μ ∂_μ è solo un artefatto della forma: γ^0 D è la forma hamiltoniana (C6) e la normalizzazione "coefficiente di ∂_t = I" la elimina. Il coniugio α ↦ SαS^{−1} di Pauli (F6-HOR) compare solo con il modello di dato "ψ a meno di un cambio di base costante" (ψ ↦ Sψ), che non è DM3.

*Esistenza per ogni L_0 ∈ 𝒞 (fix SYS-9(d)).* det L_0 è monico di grado 4 in τ, quindi non nullo, e SYS-C1 (n = 4) dà sempre una ψ ∈ Sol(L_0) che identifica L_0. H-DIRAC-1 vale dunque per ogni operatore in forma hamiltoniana, non solo per Dirac.

### [H-DIRAC-2] Esistenza e criterio
*Ipotesi (fix SYS-9(a)).* Ω ⊂ ℝ^{1+3} (o ℝ^{1+1} in (d)) è un aperto **connesso non vuoto**. Senza la connessione (d) è falso: su Ω = B_1 ⊔ B_2 si prende ψ_2 = e^{λ·x} su B_1 e 0 su B_2. *Convenzione (fix SYS-9(b)).* p_μ := i∂_μ. D è nella forma covariante; −iγ^0 D ∈ 𝒞, e il fattore −i è un'unità costante, quindi non cambia il modulo né l'annullatore.
*Enunciato.* Per Dirac massivo (m ≠ 0) in 3+1, in rappresentazione chirale D = [[−m, X], [Y, −m]] con X = p_0 − σ·p, Y = p_0 + σ·p, XY = YX = KG · I_2, KG := p_0² − |p|² (C1).
(a) M_D ≅ (R/q)^{1×2} con q := (KG − m²), primo (C5), generato dalle classi di e_3 ed e_4. Quindi μ_q = 2 e Ass(M_D) = {q}.
(b) Esiste sempre ψ ∈ Sol(D) che identifica D (SYS-C1, n = 4).
(c) ψ identifica D ⟺ (ψ_3, ψ_4) sono R/q-indipendenti: r_3(∂)ψ_3 + r_4(∂)ψ_4 = 0 ⇒ r_3, r_4 ∈ q.
(d) In 1+1, D_2 = [[−m, p_0 − p_1], [p_0 + p_1, −m]], M_{D_2} ≅ R/q è ciclico, generato da e_2, e ψ identifica D_2 ⟺ ψ_2 ∉ EP.
*Prova.* (a) In M_D le righe di D sono nulle. (L'eliminazione non perde relazioni: E D F è diagonale con E, F unimodulari; verifica del revisore HD1, HD2.) Le prime due danno e_top = (1/m) X e_bot (m è invertibile). Sostituendo nelle ultime due si ha (1/m)(YX − m²) e_bot = ((KG − m²)/m) e_bot = 0 (C4). Quindi M_D ≅ R^{1×2}/R^{1×2}(KG − m²)I_2 = (R/q)². (c) E = M_D stesso è libero su R/q con base e_3, e_4: si applica SYS-L0, e φ_ψ(r_3 e_3 + r_4 e_4) = r_3(∂)ψ_3 + r_4(∂)ψ_4. (d) Analogamente M_{D_2} ≅ R/q, generato da e_2 (C7). In ℂ[τ, ξ] ogni ideale che contiene strettamente il primo q di altezza 1 ha colunghezza finita. Quindi Ann(ψ_2) ⊋ q ⟺ ψ_2 è annullata da un ideale di colunghezza finita ⟺ ψ_2 ∈ EP (C3-L3). Infine ψ_1 = (p_0 − p_1)ψ_2/m. ∎
**Risposta alla domanda dell'utente.** Un operatore con coefficienti λ ∈ Mat_4(ℂ) costanti è un elemento di Mat_4(R): l'oggetto è il modulo M_D, non un'algebra non commutativa nuova. In forma hamiltoniana, da una ψ nota in una base fissata, le matrici α^k e βm si leggono **esattamente** non appena ψ identifica il sistema. Una tale ψ esiste sempre (SYS-C1), per ogni operatore in forma hamiltoniana. Il criterio d'identificazione è un'indipendenza di molteplicità 2 sulle componenti chirali basse (3+1), oppure "ψ_2 non è EP" (1+1), su Ω connesso. È un criterio, non un test: per una ψ data non è certificabile da un numero finito di dati (C3-P1) (fix SYS-9(c)).

---
## 8. II-T2(b′) per A derogatoria — APERTO (facoltativo, non svolto)
Non ho scritto una prova del candidato SYS-II-T2 ("polo in ξ_0 ⟺ A(ξ_0) ha un blocco di Jordan che mescola autovalori di fattori diversi"). La sola parte certa è l'esempio di F6-SYS: A(ξ) = diag(ξ, −ξ) ha proiettori costanti e nessun polo in ξ = 0, pur avendo un incrocio di autovalori. Quindi la versione "incrocio ⇒ polo" di II-T2(b′) è **FALSA** per A derogatoria (controesempio di una riga, già in NOTE §3). Il resto è in open_questions Q-S8SYS-4.

---
## 9. Triage (aggiornato dopo S-CHECK-F8-SYS del 27/10/2026, esito PASS-con-fix, e dopo il Gate 8: vedi RECEPIMENTO.md)
Gli stati sono quelli proposti dall'audit `work/CHECK-F8/AUDIT_S8-SYS.md` §0, validi dopo i fix SYS-1…SYS-13 recepiti qui (§10). La registrazione nel LEDGER spetta al coordinatore.
| ID | enunciato | stato proposto | dipendenze esterne |
|---|---|---|---|
| SYS-L0, SYS-L1 | iniettività su un essenziale; famiglia essenziale | DIMOSTRATO (standard) | Matsumura §18 (n. da verificare) |
| SYS-T1 | criterio su una famiglia essenziale | DIMOSTRATO come strumento, **declassato**, CON-FONTE in sostanza | — |
| SYS-R1 | dato EP ⇒ M_u di lunghezza finita (delta vs SLZ 2011) | DIMOSTRATO | — |
| SYS-N1 | zoccolo ≥ 2 ⇒ nessuna u identificante | caso ℝ^n **NOTO** (Oberst 1993; Pommaret 2010 Thm 5.2.5); su Ω arbitrario DIMOSTRATO (elementare, parte del delta di SYS-EX) | — |
| EX-L1, EX-L2 | unicità sui momenti; sezioni reali | DIMOSTRATO (dopo SYS-1(d)) | Noether, Nullstellensatz |
| **SYS-EX** | ∃ u identificante ⟺ zoccoli ≤ 1, su ogni Ω connesso non vuoto | caso Ω = ℝ^n **NOTO** (Oberst, MCSS 6(3) 1993, solo abstract; Pommaret 2010 Thm 5.2.5; Macaulay §82); delta unico: Ω arbitrario, DIMOSTRATO (dopo SYS-1); KA: SURVIVES | iniettività di C^∞(ℝ^n) (CON-FONTE) |
| SYS-EX-C | μ_p(C^∞) = ∞ per p non massimale | DIMOSTRATO (dopo SYS-12) | come sopra |
| SYS-T0 | EDO: e_1 = … = e_{r−1} = 1 | **NOTO** (in n = 1 non c'è delta: ogni aperto connesso è un intervallo); prova scritta come corollario | Smith |
| SYS-C1 | det P ≠ 0, n ≥ 2 ⇒ esiste u; Ass = fattori primi di det P | DIMOSTRATO (dopo SYS-3) | Koszul, Auslander–Buchsbaum |
| SYS-S1(i⇒) | su ogni Ω | DIMOSTRATO | iniettività di C^∞(ℝ^n) |
| SYS-S1(i⇐) | Ext¹(N, 𝒜) = 0; N di lunghezza finita e H¹_dR = 0 | DIMOSTRATO (dopo SYS-6) | de Rham per le correnti |
| **SYS-S1-C** | (⇐) falso su Ω a U semplicemente connesso | **FALSO** in C^∞(Ω) e in 𝒟′(Ω) (f modificata, ipotesi β(1) ≠ 0; parte 𝒟′ rivista da DEVIL-8: corretta, O21) | — |
| SYS-S1(ii) | intersezione; δ_sys = ℓ(N) | DIMOSTRATO (dopo SYS-7) | C3-L3, Matlis |
| LAME-3 | Ass = {q_P, q_S}, μ = (1, 2), criterio div/rot | DIMOSTRATO con l'ipotesi λ + 2μ ≠ 0 (SYS-8) | — |
| SYS-E1 | (H) per Dirac 1+1 ⇒ P1-T5 | DIMOSTRATO | P1-T5 (DIMOSTRATO) |
| SYS-E2 | Lie⟨X, Y⟩ = (sl_2 ⊗ ℂ[ξ])^θ | DIMOSTRATO | — |
| SYS-E3 | ZXZ esplicito, tempi non polinomiali, non locale | DIMOSTRATO | Schwartz (supporto puntuale) |
| G-L0 | covarianza | DIMOSTRATO | — |
| G-T2 | orbita ↔ (F, olonomie) | DIMOSTRATO, CON-FONTE in sostanza | Aharonov–Bohm 1959, Wu–Yang 1975 (dati confermati da CIT-AUDIT-8) |
| SYS-N3 | (A, V) non identificati da una u, anche non stazionario; variazioni B con div(ρ²B) = 0 | DIMOSTRATO (dopo SYS-10); DICT-MAG-NU ne è corollario (O15) | — |
| G-T0 | gauge fissato non identifica Maxwell | osservazione | — |
| H-DIRAC-1/2 | α, B esatti in forma hamiltoniana; criterio μ = 2 / ψ_2 ∉ EP | DIMOSTRATO (dopo SYS-9); KA: SURVIVES | SYS-C1, C3-L3 |
| II-T2(b′) derog. | "incrocio ⇒ polo" | FALSO (diag(ξ, −ξ)); versione corretta APERTA | — |
| Q-S8SYS-1 | prodotti finiti con tempi polinomiali in ξ | APERTO | — |

---
## 10. Recepimento audit F8
Fonte: `work/CHECK-F8/AUDIT_S8-SYS.md` (S-CHECK-F8-SYS, esito PASS-con-fix), `KA_SYS_EX_adjudication.md` e `KA_SYS_HDIRAC_adjudication.md` (entrambi SURVIVES), risposta del coordinatore in `inbox/S8-SYS.md`. Recepiti il 27/10/2026. **Tutti i fix sono accettati; nessuno è rifiutato.** Oberst 1993 resta "letto solo nell'abstract": nessuno stato dipende dal suo testo.
| fix | gravità | contenuto | dove applicato |
|---|---|---|---|
| SYS-1(a) | MINOR | riduzione autosufficiente al primo associato q del nucleo | §2, SYS-EX Passo 2 (primo capoverso) |
| SYS-1(b) | MINOR | Ω non vuoto; la connessione serve solo per (i) ⇒ (ii) | §2, enunciato di SYS-EX; Notazione |
| SYS-1(c) | MINOR | h_0 ∘ s non nulla su B_{q,j} (EX-L2(b) contrapposto), reale-analitica ⇒ zeri di misura nulla | §2, SYS-EX Passo 2 |
| SYS-1(d) | MINOR | argomento dimensionale in EX-L2(b) e forma contrapposta | §2, EX-L2(b) |
| SYS-2 | MAJOR (attribuzione) | prior art Oberst 1993 (solo abstract); nessuna novità su ℝ^n; delta (i)–(iii) | §1 (confronto con Oberst), §2 Oss. 5, §9 |
| SYS-3 | MINOR | inclusione ⊇ di Ass(M_P) via Fitt_0 e primi minimali; grade(m, R) = n al posto di "Weibel 4.5" | §2, SYS-C1 |
| SYS-4 | MINOR | variante di SYS-S1-C con P = (0, 0, τ) ≠ 0 | §3.3, "Variante con P ≠ 0" |
| SYS-5 | MINOR (chiude Q-S8SYS-2) | l'f originale è risolubile in 𝒟′; f = βρe^{1/(1−t)} dà il controesempio in 𝒟′ | §3.3, "Estensione a 𝒟′(Ω)"; open_questions.md |
| SYS-6 | MINOR | riduzione scalare solo per n = 2 (controesempio n = 3); verso della successione Ext | §3, SYS-S1(i⇐) |
| SYS-7 | MINOR | dim Sol(N) = ℓ(N) via e^{λ·x}ℂ[x] ≅ E(R/m_λ) e Matlis | §3, SYS-S1(ii) |
| SYS-8 | **CRITICAL** (formale) | ipotesi λ + 2μ ≠ 0 (con λ = −2μ: Ass = {(τ), (q_S)}); ruolo di ρ ≠ 0 | §4, riga delle ipotesi |
| SYS-9(a) | MINOR | Ω connesso non vuoto in H-DIRAC-2 (controesempio su Ω sconnesso) | §7, H-DIRAC-2 "Ipotesi" |
| SYS-9(b) | MINOR | convenzione p_μ = i∂_μ; −iγ^0 D ∈ 𝒞 | §7, H-DIRAC-2 "Convenzione" |
| SYS-9(c) | MINOR | "criterio" invece di "test"; non certificabile da dati finiti | §7, "Risposta alla domanda dell'utente"; titolo di H-DIRAC-2 |
| SYS-9(d) | MINOR | det L_0 monico in τ ⇒ ψ identificante per ogni L_0 ∈ 𝒞 | §7, dopo H-DIRAC-1 |
| SYS-9 (risposte) | — | W_d H = 0 ⇒ W_d det H = 0 via adj H; eliminazione senza perdita di relazioni | §7, prove di H-DIRAC-1 e H-DIRAC-2(a) |
| SYS-10 | MINOR | Φ = ψe_3, componente (1,2) di d(k/ρ²), principio del massimo per fette | §6, SYS-N3(c) |
| SYS-11 | risposte | ipotesi di P1-T5 verificate; ramo continuo di a e limite t/2 confermati; basta Schwartz | §5, SYS-E3(c) e "Controlli del revisore" |
| SYS-12 | MINOR | E(R/p)^N addendo diretto di I ⇒ μ_p(I) ≥ N | §2, Oss. 2 (SYS-EX-C) |
| SYS-13 | MINOR | ipotesi globale "Ω aperto connesso non vuoto"; dove basta un aperto qualsiasi | Notazione (inizio del file) |
*Note.* (1) La parte 𝒟′ di SYS-S1-C è una prova del revisore, integrata qui; l'audit chiede che DEVIL-8 la riveda. (2) I riferimenti a "sys_check_f8" (S1–S4, L2–L3, N1, HD1–HD2, E1–E2) sono controlli SymPy del revisore in `work/CHECK-F8/`: non li ho rieseguiti e non sono script di S8-SYS. (3) Lo script `sympy/s8sys_checks.py` (32/32 OK) non cambia: i fix sono di testo e d'ipotesi.
