# AUDIT OP-F5C — S-CHECK-19 · 26/10/2026

**Oggetto:** `work/OP-F5C/PROOF_PACKAGE.md` (priorità da `CHECK_REQUEST.md`), fonti `sources.bib`, script `work/OP-F5C/sympy/`.
**Skill caricate (lettura SKILL.md):** skills-local/session-protocol, skills-local/claim-lifecycle (passi 3–4: audit con revisore indipendente, kill-argument). Nessuno script `_vendor` eseguito. Nessun processo altrui toccato.
**Prodotti:** questo file; `KA_OPF5C_T2_{input,attack,adjudication}.md`; `KA_OPF5C_T6_{input,attack,adjudication}.md`; `sympy/s19_delta.py` + `sympy/s19_delta_*.out`; script dell'attaccante `sympy/s19ka_*.py`.

---
## 0. Tabella dei verdetti

| Claim | Verdetto | Finding | Stato LEDGER proposto |
|---|---|---|---|
| (Nov′) | OK con fix MINOR | F5C-2 | DIMOSTRATO mod fonte verificata ((Nov), CIT-AUDIT-F5) dopo F5C-2 |
| OPF5C-L1 | OK | — | DIMOSTRATO |
| OPF5C-L2 | OK (CON-FONTE verificata) | F5C-10 | CON-FONTE (Blum-Smith 2.4.17–2.4.19, verificata) |
| OPF5C-L3 | OK | — | DIMOSTRATO |
| OPF5C-T1 (a,b,c) | OK | — | DIMOSTRATO mod fonte verificata (L2; (c) anche (Nov′)) |
| OPF5C-L4 | OK | — | DIMOSTRATO |
| OPF5C-L5 | OK | — | DIMOSTRATO mod fonte verificata ((Nov′)) |
| **OPF5C-T2 (OP-K15)** | **OK con fix MINOR**; KA: SOPRAVVIVE | F5C-1, F5C-2 | **DIMOSTRATO mod fonte verificata** (OP-K15: CONGETTURA → chiusa) |
| OPF5C-L6 | OK | — | DIMOSTRATO (mod (Nov′)) |
| OPF5C-P7 (a,b) | OK con fix MINOR | F5C-3 | DIMOSTRATO mod fonte verificata ((Nov′)) |
| OPF5C-L8 | OK con fix MINOR | F5C-4 | DIMOSTRATO (dopo F5C-4: prova autonoma, fonte KR non necessaria) |
| OPF5C-P9 | OK con fix MINOR (direzione mod p corretta) | F5C-5 | righe k = 0 (L8) e K = N: DIMOSTRATO (assistito da calcolo mod p, riprodotto); righe K = 2N e N=1,K=2: lower bound solo per i k testati → **V-ex** per "∀k" |
| OPF5C-T5 | OK, fonte NON verificata | F5C-11 | CONDIZIONALE (Ritt/Kolchin, numero non verificato) |
| OPF5C-O6 | OK | F5C-12 | DIMOSTRATO (enunciato sul metodo) |
| OPF5C-L9 | **MAJOR (enunciato falso con g ∈ C¹)** → OK dopo fix | F5C-6 | DIMOSTRATO dopo fix (g ∈ C²); com'è: FALSO (i) |
| **OPF5C-T6** | (a),(c), Cor.(i),(ii): OK con fix MINOR; (b), Cor.(iii): **MAJOR (lacuna)**; KA: SOPRAVVIVE | F5C-7, F5C-8, F5C-9 | (a),(c),Cor.(i),(ii): DIMOSTRATO (dopo F5C-8/9); (b),Cor.(iii): PROVA SCRITTA (lacuna F5C-7) |
| OPF5C-O7 | OK | — | DIMOSTRATO (enunciato sul metodo; dipende da OP-P4 DIMOSTRATO) |
| INT-Q1 (analitici) | resta APERTO | — | APERTO (progresso parziale T6) |

---
## 1. Controllo linea per linea

### (Nov′)
Derivazione dal pacchetto: 2GG″ − G′² + 4(u+λ)G² ha derivata 2G(G‴ + 4(u+λ)G′ + 2u′G) = 0 ✓; per x → +∞ (k reali positivi) i getti → 0, g_i(0) = 0 (i ≥ 1), G → Σa_jλ^{N−j} ✓; con G = U, G′ = 2V: 4V² + 4f = 2UU″ + 4(u+λ)U² ≡ 0 mod U ✓. Estensione a (k, X) complessi: identità razionale in (k, X), regolare su U_0 (denominatori k_i + k_j) e vera su un aperto reale ⇒ ovunque ✓.
**F5C-2 (MINOR).** Il pacchetto presuppone che le costanti della relazione stazionaria siano esattamente a_j = e_j(κ). CIT-AUDIT-F5 registra (Nov) come CON-FONTE (secondaria) per "N-solitone ⇒ equazione stazionaria d'ordine 2N+1 con costanti dipendenti dai soli autovalori", ma **PARZIALE** per la forma delle costanti. *Riparazione (prova di 3 righe da inserire):* se u risolve ∂Ĝ_{N+1} = 0 con costanti c_j (c_0 = 1), si linearizza in X = 0: u = Σ2k_i²X_i + O(X²), X_i ∝ e^{k_ix} indipendenti; la parte lineare di g_j è −½(−¼∂²)^{j−1}u, quindi la parte lineare dell'equazione è −½∂·G_c(−∂²/4)u con G_c(μ) = Σc_jμ^{N−j}; annullandosi su ogni e^{k_ix} dà G_c(−κ_i) = 0, i = 1..N, κ_i distinti ⇒ G_c = Π(λ+κ_i), c_j = e_j(κ) ✓. Il V-ex esatto (pacchetto N ≤ 5; attaccante N ≤ 4 con k di segno misto, incluso k = (1,2,3,−5)) è coerente.

### L1 — OK
c′_j = −½(−¼)^{j−1}: g_1 = −y_0/2 ✓, g_2 = y_2/8 + … ✓. s_{2j−1} = u_j contiene y_{2j−2} = y_{i−1}, s_{2j} = v_j contiene y_{2j−1} ✓; pesi wt s_i = i+1 = wt y_{i−1} ✓; triangolare con diagonale costante ⇒ automorfismo ✓.

### L2 — OK, CON-FONTE verificata
V(F, p) = {0} ⇒ R/(F,p) artiniano ⇒ (F, p) h.s.o.p. di R. Blum-Smith (verificato, v2 HTML): Notation 2.4.13 (R f.g., connesso, ℕ-graduato su k), Def. 2.4.14 (h.s.o.p.), Cor. 2.4.17 (anello di polinomi CM), Prop. 2.4.18 (h.s.o.p. regolare ⟺ R libero su k[θ]), Cor. 2.4.19 (Hironaka). Catena: R CM ⇒ R libero su ℂ[F,p] ⇒ (F,p) regolare (2.4.18) ⇒ p regolare su R/(F), R/(F) finito su ℂ[p] ⇒ p h.s.o.p. di R/(F) ⇒ R/(F) libero su ℂ[p] (2.4.18). Rango dalla serie di Hilbert ✓; fibre di lunghezza = rango ✓.
**F5C-10 (MINOR, fonti):** citare Blum-Smith 2.4.17, 2.4.18, 2.4.19 (non solo 2.4.19); i numeri Bruns–Herzog ed Eisenbud restano NON verificati e non sono necessari: toglierli o marcarli "non usati".

### L3 — OK
deg λE² ≤ 2N−2a−1 ≤ N−1 (2a ≥ N), deg V² ≤ 2N−2b−2 ≤ N−1 (2b ≥ N−1) ✓; argomento di parità ✓.

### T1 — OK
(a) ipotesi di L2 da L1 + L3 ✓; Π_{m<N}2(2N+1−m)/Π_{i=N+2}^{2N+1}i = 2^N ✓; specializzazione di k lecita ✓. (b) libero su anello regolare ⇒ CM; ogni primo associato contrae a 0 in B ⇒ niente immersi, tutte le componenti di dim N ✓. Strati (i)–(iii) ricontrollati (in (iii) m = 2: v_1 libero, m ≥ 3: v_1² = −c, v_2..v_{m−2} determinati, v_{m−1} libero) ✓; dim strato ≤ numero di cluster ✓; S° = immagine di Ω (surgettività: scelta del segno di σ_j, casi h = 0 o μ = 0 banali) ✓; liscezza generica via Vandermonde, jacobiano diag(2ν_j), ν_j² = −f(μ_j) ≠ 0 ✓; CM + R_0 ⇒ ridotto ✓. (c) ✓ (Nullstellensatz; immagine dei getti irriducibile di dim N).

### L4 — OK
Conti rifatti: a′ + b′ = N+1; N dispari: deg V² ≤ N−3, deg E²(λ+c) ≤ N−2; N pari: N−2, N−3 ✓. Troncamento T_N²(1+x) = 1 − 2R(1+x)^{1/2} + O(x^{2N+2}) ⇒ e_j = −2Σ_{i=N+1}^{j}t_is_{j−i} ✓. Q = −e_{N+1}c^{N+1}U; coefficiente di λ^{N−1}: −e_{N+2}c^{N+2} = −e_{N+1}c^{N+1}·(−c/2) ✓; e_{N+2}+e_{N+1}/2 = −2(t_{N+2}+t_{N+1}) = −t_{N+1}/(N+2) ≠ 0 ✓. Script E1/E2 OK; attaccante Gröbner GB = {1} N ≤ 6.

### L5 — OK
k^ε ∈ U_0, M e Ψ dipendono solo da κ ✓; parte lineare (2k_i²(k_i^ε)^j) invertibile ✓; ℓ_ε dalla ricorrenza con polinomio Π(z − k_i^ε) ✓; multinsiemi distinti perché i 2N numeri ±k_i sono distinti ✓; 2^N punti distinti in una fibra di lunghezza 2^N ⇒ fibra ridotta, discriminante ≢ 0 ✓.

### T2 — OK con fix MINOR (vedi KA)
Teoria dei campi: A_k ⊗_B K = L (dominio finito su campo) ✓; m ∈ B[z] (B normale) ✓; χ_k = m^{[L:K(y_N)]} ✓; nucleo = (m) ✓; = P_k per T1(c) ✓. Pesi: base omogenea del modulo libero graduato ⇒ c_i omogenei di peso i(N+2) ✓; monomi di grado W/2 solo y_0^{W/2}, privo di k, nel termine noto c_{2^N} ✓; coefficiente = det della moltiplicazione per y_N sulla fibra di Z_0 sopra (1,0,…,0) ≠ 0 per L4 (c = 1) ✓.
**F5C-1 (MINOR).** "Π_N(k) = ±χ_k": Π_N(k) è definito a meno di scalare; normalizzare Π_N(k) := generatore monico in y_N, allora Π_N(k) = χ_k. "Omogeneo pesato in (k, y)" vale per il χ universale ∈ ℂ[k, y_0..y_N] (Π_N(k) a k fisso non è omogeneo); riformulare.
*Kill-argument:* SOPRAVVIVE (KA_OPF5C_T2_adjudication.md). *Controllo indipendente:* s19_delta.py `gen 2 2 1,3 8` (getti dei 2-solitoni da f direttamente, senza Mumford/GD/(Nov′)): grado minimo 8 ✓.

### L6 — OK (eredita T1(c)).

### P7 — OK con fix MINOR
(a) r_{N−1} di peso 2N+4 ⇒ grado ≤ N+2 ✓; non nullo ✓. (b) r_m = R_m + 2v_{N−m}v_N per m ≥ 1 (2v_N(V − v_N) ha grado ≤ N−1, v_N² costante) ✓; D indipendente da v_N, quindi da y_{2N−1} ✓; peso 3 + (2N+6) = 5 + (2N+4) = 2N+9 ⇒ grado ≤ N+4 ✓; v_2²v_{N−1} con coefficiente −2 (N ≥ 4), −v_2³ (N = 3) ✓.
**F5C-3 (MINOR).** Nella prova di non nullità "il resto di V² + λ^{2N+1}" vale solo a k = 0: per k ≠ 0, a U = λ^N, r_m = Σ_{i+j=2N−m}v_iv_j + f_m (f_m coefficienti di f_k in grado < N). I termini aggiuntivi in D sono lineari in v (v_1f_{N−2} − v_2f_{N−1}) e non cancellano v_2²v_{N−1}: conclusione invariata; correggere la frase.

### L8 — OK con fix MINOR
Il lemma "forme iniziali di una successione regolare generano l'ideale iniziale" è corretto per filtrazioni per peso positivo.
**F5C-4 (MINOR, fonte):** il numero in Kreuzer–Robbiano (§4.3) NON è verificato (ricerca senza esito). Riparazione: inserire la prova standard (5 righe): data p = Σh_mF_m con μ := max(wt h_m + d_m) minimo; se μ > wt p, le componenti di peso massimo danno una sizigia Σh_m⁺F_m⁺ = 0; per F⁺ regolare (H_1 di Koszul nullo) è combinazione di sizigie di Koszul, che si sollevano a F e abbassano μ (interi positivi: termina); a μ = wt p, p⁺ = Σh_m⁺F_m⁺ ∈ (F⁺). Con questo L8 è autonomo.

### P9 — direzione dei limiti inferiori: **CONFERMATA**, con fix MINOR
*Direzione.* Una relazione q ∈ ℚ[y] primitiva in ℤ[y] nulla su Z_k soddisfa q∘Φ = 0 in ℚ(σ), dove Φ: σ ↦ y è la parametrizzazione di S° (Lagrange + Ψ^{−1}) con coefficienti in ℤ_(p)[σ, 1/Δ], Δ = Π(μ_i − μ_j)·(costanti GD, potenze di 2); riducendo mod p, q̄ ≠ 0 si annulla sui punti mod p con Δ ≠ 0: la riga di kernel esisterebbe. Quindi **rango pieno mod p ⇒ nessuna relazione su ℚ (dunque su ℂ, per k razionale) di quel grado** ✓; la nullità mod p non prova esistenza (e il pacchetto non la usa) ✓. Per le righe k = 0 si applica a q omogenei pesati, blocco per blocco di peso: corretto per L8 (p⁺ omogeneo) ✓. Nello script il caso Δ ≡ 0 mod p non ha assert esplicito ma è intercettato dall'assert `U non divide V^2+f` (un V errato fallisce la divisibilità) ✓.
*Riproduzione indipendente* (`sympy/s19_delta.py`: GD da identità del risolvente, non da Lenard; righe "gen" con getti dei solitoni calcolati direttamente da f, senza (Nov′)/Mumford):

| N | K | pacchetto | S-CHECK-19 | esito |
|---|---|---|---|---|
| 1 | 2 | ≥ 2 (k=3) | ≥ 2, nullità a 2 | ✓ |
| 2 | 3 | ≥ 4 (k=(1,2), k=0) | gen ≥ 4; k=0 graduato ≥ 4 (peso 8) | ✓ |
| 2 | 4 | ≥ 3 (k=(1,2)) | ≥ 3 | ✓ |
| 3 | 4 | ≥ 7 (k=(1,2,4), k=0) | gen ≥ 7; k=0 ≥ 7 (peso 15) | ✓ |
| 3 | 5 | ≥ 5 | gen ≥ 5; k=0 ≥ 5 (peso 10) | ✓ |
| 3 | 6 | ≥ 4 (k=(1,2,4)) | ≥ 4 | ✓ |
| 4 | 6 | ≥ 8 (k=0) | k=0 ≥ 8 (peso 17) | ✓ |
| 4 | 7 | ≥ 6 (k=0) | k=0 ≥ 6 (peso 12) | ✓ |
| 4 | 8 | ≥ 5 (k=(1,2,4,7)) | ≥ 5 (rango pieno fino a d = 4, nullità a 5) | ✓ |
| 5 | 9 | ≥ 7 (k=0) | k=0 ≥ 7 (peso 14) | ✓ |

Tutti i 15 limiti inferiori della tabella P9 sono riprodotti indipendentemente (inclusi quelli i cui .out mancavano nel pacchetto).

**F5C-5 (MINOR).** (i) I certificati k = 0 per N = 2, 3, 4 non sono salvati su disco (solo N = 5, K = 9 in `opf5c_delta0_5.out`; `opf5c_delta_4_7.out` è il controllo a k generico): salvare gli .out (riprodotti qui). (ii) Le righe K = 2N (e N = 1, K = 2) hanno limite inferiore solo per i k testati: in §0 ("δ_N(2N) = N+1 per N ≤ 4") e in grassetto nella tabella vanno qualificate "per k = (…) testato" (per ogni k ∈ U_0: solo ≤ N+1 dimostrato, = N+1 V-ex). Le righe K = 2N−1, 2N−2 (limite inferiore da L8, ∀k) e K = N (T2) valgono per ogni k ∈ U_0 ✓. (iii) I tre run ancora attivi (`opf5c_delta0_4_5`, `opf5c_delta0_5` = "5 8 9 graded", `opf5c_delta_4_7`) non sono finiti al momento dell'audit (delta0_4_5.out vuoto; delta_4_7.out fermo a d = 5; l'attuale delta0_5.out contiene solo la riga K = 9 di un run precedente); nessun enunciato ne dipende ✓.

### T5 — OK, fonte non verificata
J_u ideale differenziale primo (dal quadro OPR2 §6); Ritt: P = [A] : H_A^∞ per un insieme caratteristico (uno solo, in una indeterminata). D_F A ∈ J_u ✓.
**F5C-11 (MINOR, fonte):** Ritt 1950 cap. II / Kolchin 1973 cap. IV: numeri NON verificati (ricerche web: la definizione di ideale "caratterizzabile" e Kolchin p. 82 Def./Lemma 8 trovati in Kondratieva–Ovchinnikov arXiv:math/0606124, ma non l'enunciato "ogni primo è [A] : H_A^∞" con numero). Stato: CONDIZIONALE fino a verifica (la proposizione è standard). Nota: T5 è dichiarata "riformulazione".

### O6 — OK
**F5C-12 (MINOR):** O6 richiede u reale-analitica in (t, x) congiuntamente (il quadro dà analiticità solo in x): l'enunciato lo dice ("soluzione reale-analitica vicino a (t₀,x₀)") — va solo ricordato nella "Conseguenza" che, senza analiticità congiunta, φ è C^∞ (la conclusione metodologica non cambia).

### L9 — MAJOR sull'enunciato, OK dopo fix
**F5C-6 (MAJOR → fix immediato).** Con g solo C¹, L9(i) è FALSO: dim 1, A = 0, g(z) = −z/(2 log(1/z)), z = e^{−√x} (verificato: g ∈ C¹, Dg(0) = 0, z′ = g(z), decadimento super-polinomiale, z ≢ 0 con s = 0). La prova usa |g(w) − g(w′)| ≤ Cρ|w − w′| e |g(w)| ≤ C|w|² (C^{1,1}). Riparazione: ipotesi g ∈ C² (o C^{1,1}). Le stime dell'integrale (∫(1+σ−x)^m(1+σ−x₁)^{−2n} ≤ (1+x−x₁)^{−n}∫(1+τ)^{m−n}; parte stabile) sono corrette con la stima quadratica; punto fisso in Y ↪ X_n e unicità nella palla ✓; (ii) ✓ (‖z‖_β ≤ C(2β−β′)^{−1}e^{−βx₁}‖z‖_β²). T6 usa g analitica: non toccato. Il riferimento Chicone (numero non verificato) non è necessario: la costruzione in Y è la stessa contrazione.

### T6 — vedi KA
Forma normale ✓; (a) ✓ (s = 0 ⇒ z ≡ 0 su semiretta ⇒ u(t,·) ≡ 0 ⇒ u ≡ 0 per conservazione L²); (c) ✓ dopo F5C-8.
**F5C-7 (MAJOR, lacuna).** (b) e Cor.(iii): l'ipotesi controlla solo u, L9(ii) richiede tutto il getto z. Riparazione: (α) ipotesi sul getto (vale per i dati esempio e^{−x²}·polinomio), oppure (β) bootstrap su W^{ss}_loc scritto per esteso (KA_OPF5C_T6_adjudication.md).
**F5C-8 (MINOR).** Scelta di q_±: definirli nelle code effettive e usare che due code su B_+ sono archi della stessa orbita monotona; chiusura di T_± senza continuità L² (bastano la convergenza puntuale e T_+ ∩ T_− = ∅).
**F5C-9 (MINOR).** p complesso: ℓ, s, n_u riferiti a Re p o Im p (quella con α ≠ 0); Cor.(ii) per relazioni reali.
Coerenza: N-solitoni (s = n_u = N ≥ 2) e Airy (q_a ∈ 𝔪³) non contraddicono T6 ✓.

### O7 — OK
(a) la prova di T6 usa di KdV solo conservazione L², regolarità e classificazione delle onde viaggianti di Schwartz (per Airy H‴ = cH′ non ha soluzioni di Schwartz ≠ 0) ✓ — con i fix F5C-7/8 vale identico. (b) da OP-P4(iv) ✓.

---
## 2. Bibliografia verificata (S-CHECK-19)

| Fonte | Uso | Esito |
|---|---|---|
| B. Blum-Smith, *Two inquiries about finite groups and well-behaved quotients*, arXiv:1803.08417 (v2, 23/03/2018), §2.4: Notation 2.4.13, Def. 2.4.14, Cor. 2.4.17, Prop. 2.4.18, **Cor. 2.4.19** (criterio di Hironaka: R f.g. connesso ℕ-graduato su k è CM ⟺ libero su k[θ] per un qualsiasi h.s.o.p.) | L2, T1(a) | **VERIFICATA** (testo HTML letto; enunciati coincidono con l'uso) |
| S. P. Novikov, «The periodic problem for the Korteweg–de Vries equation», Funkts. Anal. Prilozh. 8:3 (1974) 54–66; Funct. Anal. Appl. 8 (1974) 236–246, DOI 10.1007/BF01075697 | (Nov) → (Nov′) | **CON-FONTE (secondaria)** come da CIT-AUDIT-F5 (via arXiv:1309.1816 §2); forma delle costanti: non in fonte → dimostrata da F5C-2 |
| W. Bruns, J. Herzog, *Cohen–Macaulay Rings*, CUP 1993 | L2 (alternativa) | NON verificata (numeri); non necessaria |
| D. Eisenbud, GTM 150 | L2 (alternativa) | NON verificata; non necessaria |
| F. Gesztesy, H. Holden, *Soliton Equations and Their Algebro-Geometric Solutions I*, CUP 2003, cap. 1 | identità 2FF″ − F′² + 4(u+z)F² = R | NON verificata (numero equazione); non necessaria (identità dimostrata nel pacchetto) |
| J. F. Ritt, *Differential Algebra*, AMS Coll. Publ. 33 (1950), cap. II; E. R. Kolchin, *Differential Algebra and Algebraic Groups* (1973), cap. IV | T5 | NON verificata (numero); T5 CONDIZIONALE |
| C. Chicone, *ODE with Applications*, 2ª ed. 2006, cap. 4 | L9 | NON verificata; non necessaria (contrazione nel testo) |
| M. Kreuzer, L. Robbiano, *Computational Commutative Algebra 2*, Springer 2005, §4.3 | L8 | NON verificata; non necessaria dopo F5C-4 |
| I. Kay, H. E. Moses, J. Appl. Phys. 27 (1956) 1503–1508 | Cor. T6 (1-solitone ha r ≡ 0) | CON-FONTE (S4-INTEG F4) |
| M. Kondratieva, A. Ovchinnikov, arXiv:math/0606124 §2 (letto) | contesto T5 | conferma definizioni (Kolchin p. 82), non il teorema citato |

---
## 3. Esito dei run indipendenti
Vedi `sympy/s19_delta_*.out` (tutti con seed fissi, p = 2147483587).
