# SYNTHESIS — Fase 1 (coordinatore) · 22/10/2026

Fonti: i 15 `research/*/REPORT.md`, `ROUTES.md`, `inbox/`. Ogni affermazione rimanda all'ID dell'agente che l'ha dimostrata o trovata. Stato: **N** = noto in letteratura (con fonte), **D** = dimostrato in Fase 1 (con verifica SymPy salvo dove indicato), **A** = aperto, **F** = falso / probabilmente falso. Le citazioni sono in corso di verifica (CIT-AUDIT): fino al suo esito i numeri di teorema "da verificare" restano provvisori.

---

## 1. Messaggio in una pagina

1. **"Identificare L da u" è un problema di rango e di ideali, ed è in larga parte già noto.** ker 𝔾(u) = Ann(u) ∩ span(dizionario) [R4-T6]. Unicità ⟺ dim ker 𝔾 = 1 è Scholl et al. 2022 Cor. 1; per le equazioni di evoluzione He–Zhao–Zhong 2024 Thm 3.2 dà solo una **condizione sufficiente** (toro, due istanti vicini, soglia combinatoria su |supp û₀| più una condizione algebrica): il "⟺ |supp û₀| ≥ n+1" è dimostrato in Fase 1 da R4-T4, non è in letteratura [R8, corretto da CIT-AUDIT]. Il contributo nuovo possibile è un **teorema unificante** (Ann(u) letto sulla varietà V(P), soglia di Bézout [R4-T5]) e il suo uso per la scomposizione.
2. **A8 come scritto ("â = Σaₙ ⟺ f̂ = ΣΣe_{n,i}", somma di termini) è falso**: la parte di ker L che si scompone additivamente per termini ha **dimensione finita** [R2-T3, R3-P1, R5-P4, PR-C2a T1-10].
3. **A8 è vero se "componente" significa "fattore" dell'operatore** (decomposizione primaria di P / LCLM a coefficienti variabili), su ℝ o domini convessi [R2-T2, R2-T4]; sul toro 𝕋 fallisce in presenza di risonanze [R2-C1].
4. **Per somme di termini la struttura giusta è moltiplicativa**: u = S₁(t)⋯S_N(t)u₀, additiva nel log-simbolo. E_int ha forma chiusa (bilineare per N=2: è la h(e₁,e₂) di P1) e si calcola in O(N): **il "O(eⁿ)" di B2 è falso** nel caso commutante [R5-T2]. Vale **solo** per evoluzioni scalari del 1° ordine in t [PR-C2b P4, P5; R6-T8].
5. **Quando i termini non commutano**, il discrimine è l'algebra di Lie che generano: finita e risolubile ⇒ E_int esatto con d funzioni (Wei–Norman); finita non risolubile ⇒ solo locale; infinita ⇒ solo serie [R5, R7-P5].
6. **Nessuna regolarizzazione elimina la parte di E_int che sta fuori dallo span del dizionario**: B8 è falso; ℓ¹ agisce solo sull'ambiguità dentro lo span [R1-T6, P8].
7. **Lo spazio di Hilbert C1 si costruisce dal catalogo C2** (Aronszajn, Green = nucleo riproducente) [R1, PR-C2d]; numerabile su 𝕋, frame continuo su ℝ, con una base numerabile esplicita per il calore (polinomi del calore, spazio di Fock pesato) [R1-P11, R3, PR-C2b P6].
8. **Idea II**: la via (b) — compagna / matrice sull'anello degli operatori — conserva invarianti completi; il tensore della via (a) solo il simbolo principale [R6-T1, P1]. F1 vale con proiettori obliqui (duali biortogonali), non v⊗v [R6-T3].
9. **Non linearità**: l'identificazione resta lineare nei parametri; Burgers (Cole–Hopf) e KdV (Hirota/IST) hanno E_int in forma chiusa; per ν→0 la sovrapposizione diventa "tropicale" (min-plus) [R7, PR-C2c].

---

## 2. Mappa degli item (C1–C4, P1–P4, II)

| Item | Domanda degli appunti | Esito Fase 1 | Stato | Fonte |
|---|---|---|---|---|
| **C1** spazio | A1–A3, A7, C1.0–C1.4 | Funtore C1.0 ben posto: K_𝒟 = ΣK_n, norma inf-convoluzione (Aronszajn), split ℓ² uₙ = KₙK⁻¹u; unione di classi di Riesz ⟺ angolo di Friedrichs < 1; Green = nucleo riproducente | D / N | R1-P4, PR-C2d §3 |
| C1 / A7 | "basi numerabili?" | Su 𝕋: base numerabile indicizzata da V(P)∩(ℂ×iℤ). Su ℝ: frame continuo su V(P) (misura non unica). Esponenziali reali mai base in L². Polinomi del calore: base ortogonale di uno spazio di Fock pesato, duale di Rosenbloom–Widder | D / N | R2-T6/T7, R1, R3, PR-C2b P6, R7-T1 |
| C1 / H1 | spazio di u | "u ∈ L²(ℝ)" inadeguata per classi esponenziali: usare H^m(Ω) limitato, PW_A o L²(V(P),μ) | D | PR-C2d §3.7 |
| **C2** catalogo | A5, A6 | ~60 schede verificate (R3 K1–K14, PR-C2a 5+11, PR-C2b 23, PR-C2c 16, PR-C2d 13) ; 120/120 item tassonomici collocati | D / N | R3, PR-C2a–e |
| C2 / A6 | "funzioni legate a ogni operatore?" | **Un monomio isolato ha nucleo solo polinomiale**: la classe esiste per la sotto-equazione ∂_t − aₙ(∂_x), non per il termine; i termini non lineari (u u_x) non hanno classe propria; con coeff. variabili la classe dipende da una sottoalgebra di simmetrie (Miller) | D | R3, PR-C2e, PR-C2c, R7 |
| **C3** identificazione | C3, P4, G4 | ODE: identificabile ⟺ ordine = deg p_u; 2d valori del jet in un punto (Prony). Evoluzione su 𝕋: |supp û₀| ≥ n+1. P ridotto: Ann(u)=(P) ⟺ Z(u) infinito su ogni componente, soglia di Bézout. Si recupera il generatore di Ann(u), non L | D / N | R4-T1…T5, PR-C2b P8 |
| C3 / G4 | versione con la misura di Ehrenpreis | **Falsa** (u ≡ 1) | F | R4-C2, R2 |
| C3 | coeff. variabili | Coeff. continui arbitrari, ordine ≥ 2: mai identificabili (Scholl Prop. 10); ordine 1: unico ⟺ u ha solo zeri isolati (Scholl Prop. 8); da una sola soluzione si determinano gli autovalori ma non i coefficienti (Pierce 1979 — correzione a R4-P2); serve una classe a dimensione finita; l'annullatore minimo dipende dall'anello | N | R8, R4-T7, CIT-AUDIT |
| C3 | simmetrie | u invariante per una simmetria del dizionario ⇒ dim ker 𝔾 ≥ 2 | D | R7-L4, PR-C2c P7 |
| C3.3 | "l'approccio a componenti è giusto?" | **Verdetto**: le componenti per termine sono una carta di coordinate di Ann(u); l'oggetto canonico è Ann(u)/V(P); componenti naturali = pezzi di V(P); termini = coefficienti lineari nel log-simbolo. Confermato da R2, R6, PR-C2a | D | R4 §3, RT-R4a |
| **C4** A8 | A8 | Falso per somma di termini (dim finita); vero per fattori su ℝ; falso su 𝕋 con risonanze | D | R2-T2/T3/C1, R3-P1, PR-C2a T1-9/10 |
| C4.4 | numerabilità | vedi C1/A7 | — | — |
| **P1** E_int | B1–B4 | Definizioni per quadro (additivo, moltiplicativo, log, nucleo) [R5-D1]; commutante: E_int = Σ_{|S|≥2}Π(Sₙ−I)u₀, O(N); matrice E di rango 1; non commutante: classificazione per algebra di Lie | D | R5, R3-P2, PR-C2b P3 |
| P1 / B2 | "algoritmo ≠ O(eⁿ)" | Falso il O(eⁿ) nel caso commutante; KdV: interazione a coppie O(N²) | D | R5-T2, R7-T11 |
| P1 / B4 | "esatto, non modello" | Esatto se l'algebra di Lie è finita e risolubile; altrimenti il troncamento è il "modello locale" di B3 | D (congettura strutturata per l'impossibilità) | R5, R7 |
| **P2** regolarizzazione | B5–B8, C1 | B8 falso per E_int^⊥; ℓ¹ ≻ ℓ² sull'ambiguità interna (NSP/ERC); coerenze → 1 su dizionari continui; positività (calore) e cluster coherence come vie d'uscita; per λ basta rango + grado minimo | D / N | R1-T6/T7/P8/P9, R4 |
| **P3** duali/perturbazioni | C2 (appunti) | Dyson converge per c(x)∂ + diffusione (c ∈ L^∞, Miyadera–Voigt); regole di selezione ⇒ Dyson finito; elemento di matrice al 1° ordine con (e^{λₙt}−e^{λₘt})/(λₙ−λₘ); duali = autovettori sinistri / righe di Vandermonde⁻¹ | D / N | R5-T9/P10, PR-C2d §4, R6-T3 |
| **P4** Â⁻¹ | C3 (appunti) | Sintesi spettrale su Z(u) sempre univoca; identificabile ⟺ restrizione 𝓛 → End Z(u) iniettiva; risolvente = Padé/Laplace | D | R4-T3/T8, R6-T4 |
| **II** matrice/tensore | D2–G6 | E4: via (b) completa, via (a) solo simbolo principale; G5 vera a meno di similitudine su ℂ(x)[∂]; F1 con proiettori obliqui; "Σ D V" = SVD del Gram/catalecticante; F6 = Waring, "ruotare" = caso odeco; log-simbolo additivo solo per ordine 1 in t | D / N | R6, R7 |
| II.4 geometria | rotazioni, simmetrie | simmetrie affini ⟺ stabilizzatore di P; Heisenberg universale X = x + t a′(∂) e base di Appell; separazione = sottoalgebra commutativa | D / N | R7-P2/T1/T3 |
| **Fase 4** non lineare | A6, G3–G4 | Cole–Hopf: sovrapposizione softmax con E_int esplicito; KdV: τ di Hirota, sfasamenti; Koopman/Carleman come immersioni | D / N | R7 §5, PR-C2c |

---

## 3. Congetture guida (NOTAZIONE.md) — sopravvissute, cambiate, cadute

| Congettura | Esito | Correzione |
|---|---|---|
| G1 (A8 additivo falso) | **sopravvive, rafforzata** | uguaglianza ker(L₁+L₂)∩(ker L₁+ker L₂) = Sol(L₁+L₂, L₁²), dim 2·Σ I_p, per termini coprimi su spazi iniettivi [R2-T3]; va esplicitata l'ipotesi "coprimi" [PR-C2b P2] |
| G2 (A8 vero per fattorizzazione) | **sopravvive su ℝ, cade su 𝕋** | ker lcm = ker f + ker g su convessi; su 𝕋 serve l'assenza di risonanze; coeff. variabili: LCLM [R2] |
| G3 (somma ⇒ prodotto, log-simbolo O(N)) | **sopravvive con restrizione** | solo u_t = Σ aₙ(∂_x)u scalare del 1° ordine in t; falsa per 2° ordine in t, Caputo, sistemi, intervalli con BC [PR-C2b, PR-C2d, R6] |
| G4 (identificabilità) | **cambiata** | ODE vera (classica); evoluzione: "⟺ |supp û₀| ≥ n+1" dimostrata qui (R4-T4), in letteratura solo condizioni sufficienti più forti (He–Zhao–Zhong); versione con la misura falsa; versione intrinseca V(Ann u) = V(P) vera per P ridotto; ostruzione da simmetria [R4, R7] |
| G5 (non-matrice = matrice su anello, invariante D/DL) | **sopravvive corretta** | vera a meno di similitudine di Ore e su ℂ(x)[∂], non su A₁ [R6-T5] |
| G6 (spazio di Ehrenpreis) | **sopravvive come quoziente** | isometria ⟺ sintesi iniettiva [R1]; numerabile su 𝕋, continuo su ℝ [R2] |
| G7 (non lineare) | **sopravvive, più forte** | E_int chiuso nei casi integrabili; ostruzione da simmetria all'identificazione [R7, PR-C2c] |
| §1.2-3 "â = Σf(λ_a)v_a⊗v_a" | **cambiata** | proiettori obliqui v_a⊗w_a + parte di Jordan; versione tensoriale solo per tensori odeco [R6, R7] |
| B2 "O(eⁿ)" | **cade** (caso commutante) | O(N) / O(N²) [R5] |
| B8 "ℒ_ALT elimina E_int" | **cade** | nessun regolarizzatore elimina E_int^⊥ [R1] |
| H1 "u ∈ L²(ℝ)" | **cade** per classi esponenziali | H^m(Ω) limitato / PW_A / L²(V(P),μ) [PR-C2d] |

---

## 4. Strade scoperte (dettagli in ROUTES.md)
- **Candidate alla promozione**: RT-R4a (restrizione al sottospazio ciclico; verdetto C3.3), RT-R2b (behaviours di Oberst: componente = fattore), RT-R3a (base di Rosenbloom–Widder; R1 raccomanda), RT-S1a+S2b [TROP-L2] (poligono di Newton / dominant balance), RT-R7b (Cole–Hopf tropicale, trovata indipendentemente anche da PR-C2c), RT-S2a (componenti di Faddeev).
- **Da fondere**: RT-S1h → RT-4/RT-5 (lemma-ponte Prony ⟺ Waring, R6); RT-S1i → RT-3; RT-S2b → RT-S1a; RT-D1 → C1.0; RT-D2, RT-S2c → RT-4; RT-R6a → RT-6 (atteso); RT-S2d → RT-3.
- **Parcheggiate**: RT-S1e (rigidità di Katz, utile a coeff. variabili), RT-R7a (IST, Fase 4), RT-R1b (positività), RT-S1g (microlocale, solo iperbolico).
- **Decisione di dominio**: RT-R2a (ℝ vs 𝕋).

---

## 5. Proposta di ri-formulazione di G★ (da approvare al Gate 1)
> **G★′.** Per un operatore lineare scalare 1D a coefficienti costanti (e poi in una classe a dimensione finita di coefficienti variabili), data una soluzione esatta u:
> (i) **identificazione**: ricostruire il generatore dell'ideale Ann(u) tramite la sua varietà V(Ann u), con criterio verificabile di quando coincide con L (teorema unificante, versione intrinseca di G4);
> (ii) **scomposizione**: scrivere u come somma di componenti indicizzate dai **fattori** di P (decomposizione primaria / Loewy), con ambiguità esattamente ker dell'ideale dei fattori;
> (iii) **termini**: dentro ogni fattore, leggere i termini come coefficienti lineari nel log-simbolo (evoluzioni del 1° ordine), con E_int in forma chiusa nei quadri additivo e moltiplicativo e classificazione per algebra di Lie quando i termini non commutano;
> (iv) complessità polinomiale e dichiarazione esplicita di ciò che è impossibile (B8, A8 per somma di termini, coefficienti arbitrari).

Secondo R8 la parte (i) generalizza lavori noti, le parti (ii)–(iii) sono nuove come teoria della scomposizione per termine.

---

## 6. Sottoproblemi aperti principali (per la Fase 3)
1. Base di Schauder/Riesz del nucleo su ℝ (es. calore su ℝ²) [R2-Q1, R7-Q2].
2. G4 per P non ridotto (molteplicità, operatori di Noether) [R4-Q2].
3. Impossibilità di forma chiusa di E_int quando l'algebra di Lie è infinita [R5-Q5]; caratterizzazione esatta "algebra finita ⟺ gradi bassi" [R5-Q6, R7-Q4].
4. H_{K₁} ∩ H_{K₂} come misura esatta dell'ambiguità di E_int [PR-C2d-Q1].
5. Analoghi di Rosenbloom–Widder per Airy e Schrödinger [PR-C2b-Q2].
6. Teorema [TROP-L2] (limiti di scala verso le forme iniziali estreme, stima di E_int nelle bande).
7. Identificabilità non lineare generale (oltre 1- e 2-solitone) [PR-C2c-Q3].

---

## 7. Note di processo
- 15/15 agenti hanno pianificato prima di agire (PLAN.md), dichiarato le skill caricate e scambiato messaggi nelle inbox secondo il grafo del piano; R2↔R3↔R4, R1↔R4, R6↔R7, PR-C2a→b, PR-C2b↔e, PR-C2d→R1 hanno effettivamente scambiato tabelle; un CONFLITTO (PR-C2b → PR-C2e su G3) è stato aperto e accolto.
- La scrittura dei file REPORT.md è bloccata ai subagenti: 11 REPORT sono stati salvati dal coordinatore dalle risposte finali. SCOUT-1, R1, R8, R2 hanno aggirato il blocco con `cp` prima dell'avviso (R8, R2 hanno poi rimosso la copia).
- Due interruzioni per limite di spesa API, entrambe recuperate.
- **CIT-AUDIT completato** (`research/CIT-AUDIT/AUDIT.md`, bib unificata `sources_verified.bib`): 625 voci (445 opere), 491 verificate online, 123 classici riconosciuti ma non verificati online, 8 metadati corretti, 0 inventate, 3 contesti non supportati (He–Zhao–Zhong Thm 3.2 solo sufficiente; Pierce 1979 non determina i coefficienti; Scholl Prop. 10 solo ordine ≥ 2), già corretti in questa sintesi. Da citare: Hörmander ICASV 3a ed. 1990; non verificati sul testo: espansione di Rosenbloom–Widder, numeri in Pazy (Trotter–Kato forse Thm 3.4.5), Zettl, Paulsen–Raghupathi Thm 2.10.

---
## Errata (25/10/2026, dopo l'audit di S-CHECK — work/CHECK/, claims/LEDGER.md)
- §1.4 e §2 P1/B2: "il O(eⁿ) di B2 è falso" vale per il **valore** di E_int e per gli aggregati per ordine; la tabella completa {c_S} dell'inversione di Möbius ha costo Ω(2^N) (AUDIT_R5-T2 I-4). G3/R5-T2 sono DIMOSTRATI con ipotesi esplicite (semigruppi commutanti, ogni termine generatore, soluzione mild) su ℝ o 𝕋; nel quadro H1 = H^m(Ω) limitato restano APERTI.
- §2 riga C3 "simmetrie": PR-C2c P7 è V-ex; il DIMOSTRATO vale solo per R7-L4.
- §2 P1/B2 "KdV interazione a coppie O(N²)": vero per il **numero di parametri** (N(N−1)/2, Hirota); come costo di calcolo di f è overstated.
- R4-T5 è DIMOSTRATO su 𝕋 e nella forma algebrica; la versione su ℝ (G9) è APERTA (S-C3).
- Declassati a V-ex gli 11 claim elencati in work/CHECK/DECLASSAMENTI.md §A; R5-P6 e R5-T4 promossi a DIMOSTRATO con prova (§B).
- §2 P1/B4 e PR-C2b P4: "Wei–Norman modo per modo" per il 2° ordine in t è overstated — in gl_m Wei–Norman dà in generale solo una fattorizzazione **locale** in t; globale solo per sottoalgebre risolubili. R5-T8 applicato a operatori differenziali è V-ex (ipotesi di Wei–Norman non verificate per generatori illimitati).
- R2-T3: ipotesi da scrivere esplicite (Ω convesso, quindi connesso; 𝒜 iniettivo); conflitto R2/R5 su G1 chiuso (R5-P4 = parte (a) di R2-T3).
- **CONFLITTO S-II accolto (25/10):** R6-T3 / R7-T5 "compagna normale ⟺ p = s^m − c, |c| = 1" è FALSO per m = 2 (controesempio s² + s − 1: compagna [[0,1],[1,−1]] reale simmetrica). Enunciato corretto [II-P5]: normale ⟺ radici semplici e λ_aλ̄_b ∈ μ_m∖{1} per a ≠ b; per m ≥ 3 si riduce a s^m − c, |c| = 1. La conclusione su F1 (proiettori obliqui nel caso generale) resta valida.
- **Audit S-CHECK 2ª tornata (25/10 sera).** C3-T1 (identificabilità su Ω ⊂ ℝ² connesso ⟺ test "w_i ∉ EP") DIMOSTRATO: chiude R4-T5[ℝ] come **caratterizzazione**; la decidibilità da dati finiti (C3-Q1) resta APERTA. II-T2: nei punti ξ₀ con collisioni tra altri fattori Π_j proietta lungo ker B_j(ξ₀,C₀), non lungo ⊕_{i≠j} ker Q_i. II-T7(e) "globale ⟺ radici reali non entrambe > 0" vale solo per p reale; per p complesso (derivate dispari in x) il criterio è λ₁/λ₂ ∉ {e^{(λ₁−λ₂)t}: t>0}.
