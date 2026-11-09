# AUDIT S8-SYS — S-CHECK-F8-SYS · 27/10/2026

Revisore: S-CHECK-F8-SYS (proof-checker indipendente). Oggetto: `work/S8-SYS/PROOF_PACKAGE.md` (§1–§8), priorità e domande di `CHECK_REQUEST.md`, righe di `LEDGER_ROWS.md`, script `work/S8-SYS/sympy/s8sys_checks.py` (32/32 OK, letto l'output).
Skill caricate (lettura dei SKILL.md): skills-local/claim-lifecycle; proof-checker (Phase 0.5, tassonomia A–D, severità a due assi, Phase 1.5 red team, acceptance gate); kill-argument (attacco e aggiudicazione separati); scientific-critical-thinking per il giudizio finale sugli stati. Nessuno script `_vendor` eseguito. Contesto della sessione autrice non usato: ho letto solo enunciati, ipotesi e prove, più l'enunciato di P1-T5 (`work/P1/CHECK_REQUEST.md` §C) perché SYS-E1 lo applica.
Kill-argument: due subagenti nuovi, ciascuno con il solo file `KA_SYS_<claim>_input.md` (estratto verbatim): SYS-EX e H-DIRAC. File `_input/_attack/_adjudication` in `work/CHECK-F8/`. Entrambi gli attacchi: WOUNDED lieve; aggiudicazione: **SURVIVES** dopo fix MINOR.
Numerica indipendente: `work/CHECK-F8/sympy/sys_check_f8.py` → `sys_check_f8.out` (**13/13 OK**). Gli attaccanti hanno scritto `sympy/sys_ka_ex_check.py` e `sympy/sys_ka_hd_check.py`.

## 0. Verdetti

| ID | verdetto | fix | stato proposto |
|---|---|---|---|
| SYS-L0, SYS-L1 | OK (algebra standard) | — | **DIMOSTRATO** |
| SYS-T1 | OK; declassamento a strumento **confermato** | — | **DIMOSTRATO** come strumento (contenuto standard: Matlis 1958) |
| SYS-R1 | OK | — | **DIMOSTRATO** |
| SYS-N1 | OK | SYS-1(b), SYS-13 | **DIMOSTRATO** (su ℝ^n prior art probabile: Oberst 1993, SYS-2) |
| EX-L1 | OK | — | **DIMOSTRATO** |
| EX-L2 | OK con fix MINOR | SYS-1(d) | **DIMOSTRATO** (fatti standard di geometria algebrica citati) |
| **SYS-EX** | **OK con fix MINOR** (KA: SURVIVES); **novità: MAJOR di attribuzione** | SYS-1, SYS-2 | **DIMOSTRATO** su ogni Ω aperto connesso non vuoto. Su Ω = ℝ^n il contenuto è con alta probabilità in Oberst 1993 (da verificare sul testo: CIT-AUDIT-8); il delta è Ω arbitrario e la prova costruttiva |
| SYS-EX-C | OK con fix MINOR | SYS-12 | **DIMOSTRATO** |
| SYS-T0 | OK | — | **DIMOSTRATO** (caso n = 1: classico, Heij/Oberst; vedi SYS-2) |
| SYS-C1 | OK con fix MINOR | SYS-3 | **DIMOSTRATO** dopo SYS-3 |
| SYS-S1(i⇒) | OK | — | **DIMOSTRATO** |
| SYS-S1(i⇐) | OK con fix MINOR | SYS-6 | **DIMOSTRATO** |
| SYS-S1-C | **FALSO confermato** (C^∞); estensione a 𝒟′ trovata dal revisore | SYS-4, SYS-5 | **FALSO** per C^∞(Ω); per 𝒟′(Ω) FALSO con l'f modificata di SYS-5 (prova scritta dal revisore, da integrare: chiude Q-S8SYS-2) |
| SYS-S1(ii) | caratterizzazione OK; uguaglianza δ_sys = ℓ(N) non provata | SYS-7 | **DIMOSTRATO** dopo SYS-7 (senza SYS-7: solo dim Sol(N) ≤ ℓ(N)) |
| LAME-3 | **enunciato falso nel caso degenere λ + 2μ = 0** (ipotesi mancante) | SYS-8 | **DIMOSTRATO** con l'ipotesi aggiunta λ + 2μ ≠ 0 |
| SYS-E1 | OK (ipotesi di P1-T5 verificate) | — | **DIMOSTRATO** |
| SYS-E2 | OK | — | **DIMOSTRATO** |
| SYS-E3 | OK | SYS-11 (risposte) | **DIMOSTRATO** |
| G-L0 | OK | — | **DIMOSTRATO** |
| G-T2 | OK | — | **DIMOSTRATO**, CON-FONTE in sostanza (Aharonov–Bohm, Wu–Yang: fonti da CIT-AUDIT-8) |
| SYS-N3 | OK con fix MINOR | SYS-10 | **DIMOSTRATO** dopo SYS-10 |
| G-T0 | declassamento **confermato** | — | osservazione (nessuna riga di teorema) |
| **H-DIRAC-1** | **OK** (KA: SURVIVES integralmente) | SYS-9(b) | **DIMOSTRATO** |
| **H-DIRAC-2** | **OK con fix** (KA: SURVIVES dopo ipotesi Ω connesso) | SYS-9 | **DIMOSTRATO** dopo SYS-9 |
| SYS-II-T2-C | FALSO confermato (A(ξ) = diag(ξ, −ξ): autovalori che si incrociano in 0, proiettori costanti) | — | **FALSO** |
| II-T2(b′) derogatoria, Q-S8SYS-1 | non svolti | — | **APERTO** |

Nessun FATAL. Un CRITICAL formale e banale da riparare (SYS-8, LAME-3: enunciato falso per λ = −2μ). Un MAJOR di attribuzione (SYS-2: prior art Oberst 1993 per SYS-EX su ℝ^n). Tutto il resto è MINOR.

## 1. Fix numerati

**SYS-1 (MINOR, SYS-EX).** Prova autosufficiente e ipotesi esplicite.
(a) Nel Passo 2 va riscritta la riduzione invece del rimando a SYS-T1. Testo proposto: "Se ker(ρ_Ω ∘ ψ) ≠ 0, esso ha un primo associato q ∈ Ass(E) = Ass(M) e contiene z ≠ 0 con Ann(z) = q. Scritto z = Σ c_{p,j} x_{p,j} con c_{p,j} ∈ R/p, si ha Ann(z) = ∩_{c_{p,j} ≠ 0} p, perché ogni R/p è un dominio. Quindi ogni p presente contiene q, e q stesso è presente, perché contiene il prodotto dei p presenti." Il kill-argument ha mostrato che senza questa frase il lettore ricostruisce una riduzione che sembra trascurare i primi incomparabili (KA P1).
(b) Ipotesi "Ω non vuoto" (con Ω = ∅ si ha 𝒜 = 0 e M = R soddisfa (ii) ma non (i)). Osservazione utile: la connessione serve solo per (i) ⇒ (ii); (ii) ⇒ (i) vale su ogni aperto non vuoto.
(c) Ultimo punto del Passo 2: scrivere "h_0 ∘ s non è identicamente nulla su B_{q,j}, per EX-L2(b) in forma contrapposta; è reale-analitica, quindi il suo zero set in B_{q,j} ha misura nulla".
(d) EX-L2(b): sostituire "luogo liscio connesso e Zariski-denso" con l'argomento dimensionale: se r ∉ q, V(q) ∩ V(r) ha dimensione d − 1 e non contiene l'aperto s(U), varietà complessa di dimensione d. Risposta alla domanda del CHECK_REQUEST: il passaggio "aperto euclideo del luogo liscio ⇒ Zariski-denso in V(q)" è corretto; l'argomento dimensionale lo rende immediato.

**SYS-2 (MAJOR di attribuzione, SYS-EX su ℝ^n; anche SYS-N1, SYS-T0).** Prior art non citato: **U. Oberst, "On the minimal number of trajectories determining a multidimensional system", Math. Control Signals Systems 6 (1993) 264–288**. Fonte: abstract indicizzato (trovato con ricerca web il 27/10/2026); **testo completo non letto**, il server della scheda ha restituito 403. Secondo l'abstract, il lavoro determina in modo costruttivo il numero minimo μ(S) di generatori (traiettorie) di un sistema lineare a coefficienti costanti di EDP o di equazioni alle differenze, estende Heij e Zampieri (casi discreti 1D e 2D) e collega i sistemi con μ(S) ≤ 1 ai sistemi **principali** di Macaulay. Su ℝ^n, dove C^∞ è un cogeneratore iniettivo, "u identifica P" (Ann(u) = U_P) equivale a "Sol(P) è il più piccolo sistema che contiene u", cioè a "Sol(P) è generato da u". Quindi SYS-EX su ℝ^n è con alta probabilità un caso (μ(S) ≤ 1) del risultato di Oberst 1993, e la formula attesa è μ(S) = max_m dim soc_m(M_P) (almeno 1). *Riparazione:* citare Oberst 1993 in §1 e §2; togliere ogni pretesa di novità su ℝ^n; dichiarare il delta solo come (i) Ω aperto connesso arbitrario, senza iniettività di C^∞(Ω), (ii) costruzione esplicita della u con funzioni intere, (iii) la lettura come criterio d'identificazione. CIT-AUDIT-8 deve leggere Oberst 1993 (enunciato principale e definizione di μ(S)) oltre a Oberst 1990.
*Schindelar–Levandovskyy–Zerz 2011:* ho riletto solo l'abstract (arXiv:1004.2924). Tratta segnali polinomiali e polinomiali-esponenziali (MPUM, VMPUM) e non enuncia criteri sul numero di traiettorie. Il delta dichiarato nel pacchetto (SYS-R1: da dati EP si identificano solo sistemi con M_P di lunghezza finita) è corretto: nessuna sovrapposizione con SYS-EX per sistemi con M_P di lunghezza infinita. Rischio di novità rispetto a SLZ: basso.
*Oberst 1990:* non leggibile (a pagamento, come per CIT-AUDIT-6). La fonte secondaria conferma solo che "large" significa Ass(F) = Spec R; i numeri di Bass di C^∞(ℝ^n) non sono confermati sul testo.

**SYS-3 (MINOR, SYS-C1).** La prova dimostra solo "Ass(M_P) ⊆ {fattori primi di det P}". Inclusione opposta da aggiungere: Supp M_P = V(Fitt_0) = V(det P); se f è un fattore primo di det P, (f) è un primo minimale del supporto (altezza 1, e M_P è di torsione), quindi è associato. Inoltre la numerazione "Weibel 4.5" va verificata; basta citare grade(m, R) = n.

**SYS-4 (MINOR, SYS-S1-C).** Risposta alla domanda "P = 0 è accettabile?": sì formalmente (U_P = 0, l = 0), ma conviene una variante con P ≠ 0, che il revisore ha verificato. k = 3, Q_1 = [(1,0,0); (0,0,τ)], Q_2 = [(1,ξ,0); (0,0,τ)], P = (0,0,τ). Allora U_1 ∩ U_2 = R(0,0,τ) = U_P (sys_check_f8 S1), N ≅ R/(ξ) ⊕ R/(τ) ha lunghezza infinita, Sol(P) = {(w_1, w_2, w_3) : ∂_t w_3 = 0} e Sol(Q_1) + Sol(Q_2) = {(v_1, ·, w_3) : v_1 ∈ ∂_x C^∞(Ω), ∂_t w_3 = 0}. Con la stessa f si ha (−f, 0, 0) ∈ Sol(P) fuori dalla somma. Ho controllato anche gli altri punti chiesti: f ∈ C^∞(Ω); i punti (1, 1/2) e (1, 5/2) stanno in Ω; i segmenti {t} × [1/2, 5/2] stanno in Ω per t < 1; Ω è aperto (il rettangolo tolto è relativamente chiuso in (0,3)²) e semplicemente connesso.

**SYS-5 (MINOR come fix; chiude Q-S8SYS-2).** *L'f del pacchetto non basta in 𝒟′.* Sul dominio a U, ∂_x h = f con f = β(t)ρ(x)/(1 − t) **è** risolubile in 𝒟′(Ω). Si pone h = F := ∫_{1/2}^x f nella parte t < 1, h = 0 sul braccio inferiore x < 1, e h = T(t) sul braccio superiore x > 2, con T := d/dt[−β log|1 − t|] + β′ log|1 − t| ∈ 𝒟′((0,3)), che per t < 1 vale β/(1 − t) (sys_check_f8 S2). I tre pezzi si incollano. *Con un'altra f il controesempio vale anche in 𝒟′.* Si pone f(t, x) := β(t) ρ(x) e^{1/(1−t)} per t < 1 e 0 altrove; f ∈ C^∞(Ω) per lo stesso motivo del pacchetto. Sia h ∈ 𝒟′(Ω) con ∂_x h = f. Sui rettangoli A = (0,1) × (0,3), B = (0,3) × (0,1) e C = (0,3) × (2,3) le soluzioni distribuzionali di ∂_x(·) = 0 sono della forma k(t) ⊗ 1. Quindi h = F + k_A(t) su A, h = k_B(t) su B e h = k_C(t) su C. Su A ∩ B si ha F = 0, quindi k_A = k_B su (0,1). Su A ∩ C si ha F = β(t)e^{1/(1−t)}, quindi k_C − k_B = β e^{1/(1−t)} su (0,1). Ma k_C − k_B ∈ 𝒟′((0,3)), mentre e^{1/(1−t)} non si estende a una distribuzione vicino a t = 1. Infatti, con φ_ε ≥ 0 supportata in [1 − 2ε, 1 − ε] e |φ_ε^{(j)}| ≤ C_j ε^{−j}, si ha ⟨e^{1/(1−t)}, φ_ε⟩ ≥ c ε e^{1/(2ε)}, mentre un'estensione di ordine N darebbe una stima O(ε^{−N}) (sys_check_f8 S3). Contraddizione. Dunque SYS-S1(⇐) è FALSO anche in 𝒟′(Ω) e Q-S8SYS-2 si chiude. Stato proposto per questa estensione: prova scritta dal revisore, da integrare dall'autore e da far rivedere a DEVIL-8.

**SYS-6 (MINOR, SYS-S1(i⇐)).** (a) "Per k = 1 e Q_1, Q_2 coprimi, N ha lunghezza finita" vale solo per n = 2: con n = 3, Q_1 = ζ_1, Q_2 = ζ_2 si ha N = ℂ[ζ_3] (sys_check_f8 S4). Va scritto "n = 2". (b) Nella dévissage va fissato il verso: da 0 → N′ → N → R/m → 0 si ha Ext¹(R/m, 𝒜) → Ext¹(N, 𝒜) → Ext¹(N′, 𝒜). (c) Risposte alle domande: l'identificazione di Koszul con de Rham tramite il coniugio per e^{λ·x} è corretta, e per 𝒟′ basta il teorema di de Rham per le correnti.

**SYS-7 (MINOR, SYS-S1(ii)).** La prova dà solo dim Sol(N) ≤ ℓ(N), ma il pacchetto scrive "δ_sys := ℓ(N) = dim Sol(N)". L'uguaglianza vale e si prova così: su Ω connesso, il sottomodulo m_λ-di torsione di 𝒜 è e^{λ·x}ℂ[x], che è isomorfo a E_R(R/m_λ) (sistemi inversi di Macaulay, caratteristica 0). Per N di lunghezza finita si ha Hom(N, 𝒜) = ⊕_λ Hom(N_λ, E(R/m_λ)), e per la dualità di Matlis la dimensione è Σ_λ ℓ(N_λ) = ℓ(N). Senza questa riga, scrivere "≤".

**SYS-8 (CRITICAL formale, riparazione banale, LAME-3).** Le ipotesi "ρ, μ ≠ 0, λ + μ ≠ 0" ammettono λ = −2μ. In quel caso q_P = ρτ² non è primo, det P = ρτ² q_S² e Ass(M_P) = {(τ), (q_S)} (sys_check_f8 L2–L3). L'enunciato "Ass = {(q_P), (q_S)}, μ = (1, 2)" è quindi falso così com'è scritto. *Riparazione:* aggiungere λ + 2μ ≠ 0 (fisicamente λ + 2μ > 0). Con questa ipotesi tutto il §4 è corretto. Ho rifatto la Smith su R_{(q_S)} (esponenti (0, 1, 1), perché rango mod q_S = 1 e v(det) = 2), il passaggio r̄ᵀ[ξ]_× ∈ κξ ⟺ r̄ ∈ κξ (usa ξ·ξ ≠ 0 in κ(q_S)), l'essenzialità di E e l'assenza di relazioni miste. Serve anche ρ ≠ 0 per (q_P, q_S) = (τ², |ξ|²), di altezza 2.

**SYS-9 (MINOR, H-DIRAC; dal kill-argument).** (a) Aggiungere "Ω aperto connesso non vuoto" a H-DIRAC-2: senza, (d) è falso (Ω = B_1 ⊔ B_2, ψ_2 = e^{λ·x} su B_1 e 0 su B_2). (b) Fissare la convenzione p_μ = i∂_μ e dire che −iγ^0 D ∈ 𝒞: il fattore −i serve ed è innocuo, perché è un'unità costante. (c) Nella "Risposta" scrivere "criterio" invece di "test" e aggiungere che non è certificabile da dati finiti. (d) Aggiunta utile: per ogni L_0 ∈ 𝒞, det L_0 è monico di grado 4 in τ, quindi SYS-C1 dà sempre una ψ identificante. H-DIRAC-1 vale dunque per ogni operatore in forma hamiltoniana, non solo per Dirac.
Risposte alle domande: in H-DIRAC-1, "τI + α_0·ξ non è un divisore di zero" basta anche per W qualsiasi, perché da W_d H = 0 segue W_d det H = 0 moltiplicando per adj H. In H-DIRAC-2 l'eliminazione non perde relazioni (E D F diagonale con E, F unimodulari: HD1, HD2). In 1+1, "ideale che contiene strettamente q ⇒ colunghezza finita" è corretto, perché R/q è un dominio di dimensione 1.

**SYS-10 (MINOR, SYS-N3(c) per n ≥ 3).** Va resa esplicita la scelta Φ = ψ e_3, con ψ ∈ C_c^∞(Ω). Allora k = rot Φ ha div k = 0, e la componente (1,2) di d(k/ρ²) è −div_{12}(ρ^{−2}∇_{12}ψ) (sys_check_f8 N1). Fetta per fetta in x_3, il principio del massimo su ogni componente connessa della fetta dà ψ ≡ 0. Con questa riga la parte (c) è sufficiente.

**SYS-11 (risposte, SYS-E).** (a) SYS-E1: P1-T5 chiede una ℂ-algebra 𝒜 e tempi scalari g_i(t, ε) olomorfi con g_i(t, 0) ≡ 0 per Z_i = Y. Mat_2(ℂ[ξ]) con ε = m soddisfa le ipotesi; il calcolo ad_X(σ_x) = −2ξσ_y, ad_X(σ_y) = 2ξσ_x è corretto. (b) SYS-E3(a): per ξ ≠ 0 il numero cos ωt + iξ sin(ωt)/ω non si annulla mai, quindi il ramo continuo di a esiste per ogni t (controllo numerico indipendente con sollevamento del ramo fino a t = 20: errore 8.7·10^{−14}, E1). Il limite g_1 → t/2 è confermato (E2). (c) SYS-E3(c): basta Schwartz, non serve Peetre. Il moltiplicatore ha simbolo liscio e limitato, quindi il nucleo è una distribuzione temperata; l'operatore di convoluzione è locale ⟺ il nucleo ha supporto in {0}. Peetre serve solo per operatori non invarianti per traslazioni.

**SYS-12 (MINOR, SYS-EX-C).** Da (R/p)^N ↪ I con I iniettivo segue E(R/p)^N ↪ I, che è un addendo diretto, quindi μ_p(I) ≥ N. Una riga.

**SYS-13 (MINOR, globale).** Mettere "Ω aperto connesso non vuoto" come ipotesi globale nella notazione per SYS-N1, SYS-EX, SYS-T0, SYS-C1, SYS-S1(ii) e H-DIRAC, e segnalare dove basta un aperto qualsiasi: SYS-EX (ii)⇒(i), SYS-S1(i⇒), SYS-S1(i⇐).

## 2. Verifica di SYS-EX (Phase 0.5 e red team, sintesi)
*Obblighi di prova.* (O1) Famiglia essenziale finita E ≅ ⊕(R/p)^{μ_p} con μ_m ≤ dim soc_m: OK. (O2) q f_{q,j} = 0: OK, perché s(y) ∈ V(q). (O3) La relazione nel nucleo coinvolge solo p ⊇ q, con qualche r_{q,j} ∉ q: OK tramite il primo associato del nucleo (SYS-1(a)). (O4) Il primo membro è Λν con ν complessa a supporto compatto: OK (s è continua sui compatti B, e i punti λ danno r(λ)δ_λ). (O5) EX-L1: OK; la funzione è intera, il principio d'identità vale su un aperto reale e i momenti si annullano. (O6) h_0 ∈ ∏_{p⊋q} p ∖ q esiste e annulla ν′: OK. (O7) Stone–Weierstrass su K = ⊔_j B_{q,j}: i polinomi complessi nelle variabili reali y formano un'algebra con l'unità, chiusa per coniugio, che separa i punti; F è continua su K perché le palle sono disgiunte; ∫_K gF = 0 per ogni g ∈ C(K) implica F = 0. OK. (O8) EX-L2(b) dà r_{q,j} ∈ q: OK (SYS-1(c), (d)). (O9) Passo 3: l'estensione a M → C^∞(ℝ^n) usa solo l'iniettività su ℝ^n (CON-FONTE: Malgrange 1962–63, Palamodov, Ehrenpreis); poi la restrizione e SYS-L0 danno l'iniettività. OK per Ω arbitrario, anche non P-convesso. (O10) (i) ⇒ (ii) in 𝒟′: ker(∇ − λ) su 𝒟′(Ω), con Ω connesso, è ℂe^{λ·x}. OK.
*Red team.* Più copie dello stesso primo non massimale, sulla stessa sezione s con palle disgiunte: OK, perché Stone–Weierstrass separa le F_j. Primi annidati (M = R ⊕ R/(ζ), n = 1): OK (attaccante, SymPy). Primi massimali dentro V(q): uccisi da h_0. q = 0: s = id. Ω illimitato o non convesso: OK. Nessun controesempio.
*Domande del CHECK_REQUEST su SYS-EX.* La riduzione con più copie dello stesso primo è corretta. L'uso di h_0 è corretto. Stone–Weierstrass va bene. EX-L2(b) va bene (SYS-1(d)). Il Passo 3 va bene per Ω arbitrario. (i) ⇒ (ii) in 𝒟′ è corretto. Sulla novità, vedi SYS-2.

## 3. Altri controlli fatti a mano (OK, senza fix)
SYS-N1; SYS-R1 (M_u ≅ Σ R u_i ⊂ 𝒜, di dimensione finita); SYS-T0 (Smith, divisori determinantali; l'esempio G1 risolve il sistema); SYS-S1(i⇒) (r ∈ U_1 ∩ U_2 annulla la somma; v costruita per estensione); successione esatta di SYS-S1(i⇐) (esattezza al centro e a sinistra); SYS-S1(ii)(⇒) (indipendenza lineare delle f_g per EX-L1 e Stone–Weierstrass); SYS-E2 (θ automorfismo, a e c dispari, b pari, generazione della base); G-L0 (calcolo del coniugio, σ_c); G-T2(a) (grado di g ∘ γ, costruzione di g); SYS-N3(a), (b) (calcolo di (∇ − iA)²(ρe^{iS}), parti reale e immaginaria, j′ = j + k). In SYS-L1 l'uguaglianza μ_p = numero di Bass è corretta, perché E(M) = E(E).

## 4. Acceptance gate
1. Nessun FATAL. Un solo CRITICAL (SYS-8), con riparazione banale (un'ipotesi): i claim restano DIMOSTRATO solo **dopo** il fix.
2. Ipotesi esplicite: richiedono SYS-1(b), SYS-8, SYS-9(a) e SYS-13.
3. Nessuna stima asintotica con costanti nascoste nel pacchetto (solo SYS-E3(b), dove i limiti sono espliciti).
4. Red team eseguito su SYS-EX, EX-L2, SYS-C1, SYS-S1-C, LAME-3 e H-DIRAC. Controesempi trovati: LAME-3 con λ = −2μ (enunciato) e H-DIRAC-2(d) su Ω sconnesso (ipotesi). Entrambi si riparano con un'ipotesi.
**Esito:** PASS-con-fix (SYS-1 … SYS-13). Le promozioni a DIMOSTRATO della tabella §0 valgono dopo l'applicazione dei fix indicati; SYS-2 è condizione per il testo di novità, non per lo stato.
