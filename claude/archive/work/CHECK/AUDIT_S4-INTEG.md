# AUDIT S4-INTEG — lemmi di trasporto della Fase 4
Revisore: S-CHECK-9 (9ª tornata), 26/10/2026. Revisore indipendente: non ho scritto nessuna delle prove.
**Fonte esaminata:** solo `work/S4-INTEG/CHECK_REQUEST.md` (§A domande Q1–Q8, §B testo integrale, §0 fatti importati). `PROOF_PACKAGE.md` **non letto** (la CHECK_REQUEST è risultata autosufficiente; nessun riferimento puntuale necessario). Contesto: research/CIT-AUDIT/AUDIT-4.md (r. 7, r. 17, §2.1–2.4), research/DEVIL/ATTACK-4.md (O3, O4, O7, O10).
**Fatti usati come dati:** C3-T1(a) (DIMOSTRATO, S-CHECK-2A; già applicato al calore in AUDIT_P4-L7 L7.19) per ALG-P4(c). F-H, F-N, F-SS, F-C, F-MS, F1–F4 con lo stato dichiarato in §0 della CHECK_REQUEST (non riauditati: sono fonti).
**Skill caricate** (lettura dei SKILL.md, nessuno script _vendor eseguito): skills-local/session-protocol, skills-local/claim-lifecycle, proof-checker (enunciati canonici, micro-claim, checklist, red team, severità a due assi, acceptance gate; revisore = io, niente Codex), scientific-critical-thinking (mostrato vs affermato; stato proporzionato), sympy.
**SymPy/mpmath:** `work/CHECK/sympy/audit_s4integ.py` → `audit_s4integ.out` (.venv, -I). Esito in §11.
**Kieffer et al. (PDF):** tentata la lettura di arXiv:2512.12019 con WebFetch (sola lettura): **bloccata dalla policy di rete** (arxiv.org e export.arxiv.org). Non ho aggirato il blocco. La discrepanza e^{δRe} / e^{δRe/2} resta quindi **da verificare sul PDF** (R7 aperto); §1.5 dà ciò che si può decidere senza il testo.

## 0. Verdetti
| claim | verdetto | stato proposto |
|---|---|---|
| **L-S** | PASS | DIMOSTRATO |
| **F4L-P3** (i)–(iii) | PASS-con-fix(P3-1, P3-2, P3-3), MINOR | DIMOSTRATO (identificazione "u_ε = soluzione di Burgers con dato εu₀" CONDIZIONALE[F-H] per dato misura) |
| **F4L-P3** (iv) (0,L), Neumann | PASS-con-fix(P3-4), MINOR | DIMOSTRATO modulo F-N → CONDIZIONALE[F-N] (F-N è teoria parabolica classica: CON-FONTE da fissare) |
| **KIEFFER-C** (§4.3) | PASS-con-fix(K-1, K-2) | "tesi 'raggio infinito per q.o. x' falsa per v = 0": **sostenuto** (indipendente dalla discrepanza); "incoerenza interna (30)": **NON verificato** (PDF non letto) |
| **ALG-L1** | PASS | DIMOSTRATO (noto) |
| **ALG-T1** (a)(b)(c) | PASS-con-fix(T1-1), MINOR | DIMOSTRATO; (b) CON-FONTE parziale (Scholl et al.) |
| **ALG-P3** | PASS-con-fix(P3a-1, P3a-2), MINOR | DIMOSTRATO (dicotomia: vedi §2.3) |
| **ALG-P4** | PASS-con-fix(P4-1), MINOR | DIMOSTRATO (dip. C3-T1(a) solo per il controesempio di (c)) |
| **ALG-P6** | PASS | DIMOSTRATO |
| **MODREL-T1** + Cor. + Burgers | PASS-con-fix(M-1), MINOR | DIMOSTRATO |
| **INT-T1(A)**, **(UC-ω)**, **Lemma B1** | PASS | DIMOSTRATO |
| **INT-T1(UC-1)** | PASS-con-fix(UC-1a, UC-1b), MINOR | CONDIZIONALE[F-C, F-SS] (riduzione DIMOSTRATA; tesi "Saut–Scheurer limita l'ordine del flusso vero, non 𝓗_M" **confermata**) |
| **INT-T1(B)** | PASS | CONDIZIONALE[F-MS] (riduzione DIMOSTRATA; F-MS V-ex qui per N = 2, n ≤ 3) |
| **INT-T1(C)** | riduzione PASS-con-fix(C-1), MINOR | CONDIZIONALE[F1–F4] (invariato) |
| **INT-T2** | riduzione PASS | CONDIZIONALE[ZS, UC] (invariato) |
| **INT-P5** (Hirota (a),(b),(c),(e)) | PASS | DIMOSTRATO |
| **INT-P6** (Hirota (d)) | PASS | DIMOSTRATO |
| **F4LIN-T2** (0),(i),(ii) | PASS-con-fix(L-1), MINOR | DIMOSTRATO (identificazione entropica CON-FONTE Evans, numero da verificare) |
| **F4LIN-T2** (iii) | PASS-con-fix(L-2, L-3), MINOR | DIMOSTRATO; la stima si migliora a O(e^{−δ/2ν}) (L-3) |

Nessun rilievo FATAL, CRITICAL o MAJOR. Nessun FALSO. Acceptance gate: zero FATAL/CRITICAL aperti; ipotesi esplicite (con le aggiunte MINOR sotto); red team eseguito (§11).

Nota sullo stato "DIMOSTRATO modulo F…": secondo claim-lifecycle, uno stato DIMOSTRATO pieno richiede che ogni fatto usato sia DIMOSTRATO o CON-FONTE con riferimento verificato. Dove la fonte non è stata letta (F-C, F-SS solo da secondaria, F-MS, F-N, F-H per misure) propongo **CONDIZIONALE[F…]**, con la riduzione dichiarata DIMOSTRATA. CIT-AUDIT-5 può promuoverle a CON-FONTE leggendo le fonti.

---
## 1. L-S e F4L-P3 (priorità 1)
### 1.1 L-S — enunciato canonico
∀X v.a. reale con X ∈ [a,b] q.c., w = b−a > 0: M(s) = 𝔼e^{sX} è intera; ∀s con |Im s| < π/w, M(s) ≠ 0; log M (ramo con log M(0) = 0) è olomorfa sulla striscia e la sua serie di Taylor in 0 ha raggio ≥ π/w; esiste X (Bernoulli simmetrica su {a,b}) con raggio = π/w.
| MC | passo | esito |
|---|---|---|
| LS.1 | M intera | OK (|e^{sX}| ≤ e^{|Re s|max(|a|,|b|)}, convergenza dominata localmente uniforme; Morera o derivazione sotto il segno). |
| LS.2 | Re(e^{−iτm}M(s)) = 𝔼[e^{σX}cos(τ(X−m))] ≥ cos(|τ|w/2)𝔼e^{σX} > 0 | OK: |X−m| ≤ w/2 e |τ|w/2 < π/2, cos è decrescente su [0,π/2]. Red team: 200 leggi × 20 punti della striscia. |
| LS.3 | log M olomorfa sulla striscia, raggio ≥ π/w | OK: striscia semplicemente connessa, M ≠ 0; il disco |s| < π/w è contenuto nella striscia. |
| LS.4 | ottimalità | OK: M = e^{sm}cosh(sw/2), zeri in iπ(2k+1)/w. Il raggio è **esattamente** π/w perché log M non si prolunga olomorficamente in un intorno di uno zero di M (exp(log M) = M ≠ 0). La frase "il raggio vale esattamente π/w" è corretta. |
**Verdetto L-S: PASS → DIMOSTRATO.** (Folklore; nessuna fonte: lo stato DIMOSTRATO poggia sulla prova, che è completa.)

### 1.2 F4L-P3 (i)–(ii) — enunciato canonico
∀ν > 0, ∀u₀ misura reale finita su ℝ, w := osc U₀ > 0, ∀t > 0, ∀x ∈ ℝ: ε ↦ φ_ε(t,x) è intera e non nulla su {|Im ε| < 2πν/w}; ε ↦ u_ε(t,x) è olomorfa lì e la sua serie di Taylor in 0 ha raggio ≥ 2πν/w (costante indipendente da (t,x)). ∀r ∈ (0, 2πν/w): sup_{|ε|≤r, x}|u_ε(t,x)| ≤ 2νe^{rw/2ν}/(cos(rw/4ν)√(πνt)); se in più u₀ ∈ L¹∩L^∞, sup_{|ε|≤r, t>0, x}|u_ε| ≤ r‖u₀‖_∞e^{rw/2ν}/cos(rw/4ν).
| MC | passo | esito |
|---|---|---|
| P3.1 | φ_ε(t,x) = M(−ε/2ν) con X = U₀(Y), Y ~ G_ν(t,x−·)dy | OK (G_ν(t,x−·) è una densità; X ∈ [inf U₀, sup U₀]). |
| P3.2 | ∂_xφ_ε intera in ε | OK nella sostanza; **typo**: "e^{|Re ε|w′/2ν}" con w′ non definito: va e^{|Re ε|·sup|U₀|/2ν} → **P3-1** (COSMETIC). |
| P3.3 | |φ_ε| ≥ cos(rw/4ν)e^{σm−|σ|w/2} | OK: |φ| ≥ Re(e^{−iτm}φ), poi LS.2; |τ| ≤ |s| ≤ r/2ν; σX ≥ σm − |σ|w/2. (Q5: sì.) |
| P3.4 | |∂_xφ_ε| ≤ e^{σm+|σ|w/2}/√(πνt) | OK: ‖∂_xG_ν(t)‖_{L¹} = 2G_ν(t,0) = (πνt)^{−1/2}. |
| P3.5 | rapporto: e^{|σ|w} ≤ e^{rw/2ν} | OK. |
| P3.6 | caso L^∞: integrazione per parti | OK: ∂_xG(x−y) = −∂_yG(x−y), termini di bordo nulli (G decade, e^{sU₀} limitato, U₀ assolutamente continua). (Q5: sì.) |
| P3.7 | Cauchy: |u^{(n)}| ≤ sup_{|ε|=r}|u_ε|·r^{−n} | OK. |
| P3.8 | "u_ε = soluzione di Burgers con dato εu₀" | Dipende da F-H, **non letto**. Per u₀ ∈ L¹ è il teorema di Hopf; per u₀ **misura** (in particolare δ) la formula definisce una soluzione classica per t > 0 che assume il dato in senso debole-*; l'unicità nella classe delle misure è un fatto separato (letteratura sulle "source solutions") che F-H come enunciato in §0 non copre esplicitamente ("o misura finita" è aggiunto senza fonte). **Q5: compatibile come definizione** (la serie di Volterra è *definita* come serie di Taylor di u_ε dato dalla formula, quindi (i)–(iii) non dipendono da F-H); l'identificazione con "la" soluzione è CONDIZIONALE[F-H misure] → **P3-2** (MINOR, REFERENCE). |
Red team: (ii) controllata su 30 dati a gradini (3 salti casuali) × 15 punti del cerchio |ε| = r < 2πν/w: nessuna violazione.

### 1.3 F4L-P3 (iii) — ottimalità
| MC | passo | esito |
|---|---|---|
| P3.9 | U₀ = A·1_{[0,∞)}, φ_ε = (1−Φ) + Φe^{−σ′}, ∂_xφ_ε = G_ν(t,x)(e^{−σ′}−1) | OK (∂_xΦ = G_ν(t,x)). |
| P3.10 | x = 0: u_ε = 4νG tanh(εA/4ν) | OK (SymPy esatto). |
| P3.11 | zeri del denominatore = poli (numeratore −G/Φ ≠ 0); R(t,x) = (2ν/A)√(log²((1−Φ)/Φ)+π²) | OK. Red team: 3 terne (ν,A,t,x): zero numerico del denominatore, |zero| = formula a 20 cifre, radice n-esima dei coefficienti di Taylor (n = 40) entro il 10% di R(t,x), R ≥ 2πν/A. |
| P3.12 | "ottimale" | OK nel senso: la costante 2πν/w del minorante uniforme in (t,x) è raggiunta (in x = 0, per ogni t). In x ≠ 0 il raggio è più grande: va detto "ottimale come costante uniforme", non "il raggio vale 2πν/w" → **P3-3** (COSMETIC; l'enunciato (iii) lo dice già correttamente, la tabella §5 no). |

### 1.4 F4L-P3 (iv) — (0,L) con Neumann
Enunciato canonico: Burgers su (0,L), u(t,0) = u(t,L) = 0, dato εu₀ con u₀ ∈ L¹(0,L), U₀(y) = ∫₀^y u₀; allora ∀t > 0, x ∈ [0,L], φ_ε(t,x) = ∫₀^L G_N(t,x,y)e^{−εU₀(y)/2ν}dy ≠ 0 per |Im ε| < 2πν/w, w = osc_{[0,L]}U₀, e vale la prima stima di (ii).
| MC | passo | esito |
|---|---|---|
| P3.13 | φ_x = 0 al bordo ⟺ u = 0 al bordo; identità di Cole–Hopf | OK. |
| P3.14 | G_N ≥ 0, ∫₀^L G_N dy = 1 | OK (classico; anche esplicito per immagini: G_N = Σ_k[G(x−y+2kL) + G(x+y+2kL)] > 0). Red team: positività, massa 1 a 12 cifre, ∂_xG_N = 0 in x = 0, L. |
| P3.15 | L-S con Y ~ G_N(t,x,·)dy su [0,L] | OK. |
| P3.16 | "la prima stima di (ii) vale" | La prova dice solo "‖∂_xG_N(t,x,·)‖_{L¹} finito": così la costante non è quella di (ii). **Lacuna di costante, chiusa qui:** con la formula per immagini, ∫₀^L|∂_xG_N(t,x,y)|dy ≤ Σ_k∫₀^L(|G′(x−y+2kL)| + |G′(x+y+2kL)|)dy = ∫_ℝ|G′| = (πνt)^{−1/2}, perché gli intervalli {x−y+2kL : y ∈ (0,L)} e {x+y+2kL : y ∈ (0,L)} tassellano ℝ. Quindi la prima stima di (ii) vale **con la stessa costante**. Red team: 3 casi, disuguaglianza verificata. → **P3-4** (MINOR, fix: aggiungere questa riga). |
| P3.17 | "Per F-N è la soluzione" | Dipende da F-N (unicità della soluzione di Dirichlet con dato L¹): CONDIZIONALE[F-N]. Come per P3.8, (iv) come affermazione sulla formula non dipende da F-N. |
**Verdetto F4L-P3: PASS-con-fix(P3-1..P3-4)**, tutti MINOR/COSMETIC → (i)–(iii) **DIMOSTRATO** (come enunciati sulla formula di Cole–Hopf; l'identificazione con la soluzione per dato misura è CONDIZIONALE[F-H]); (iv) **DIMOSTRATO** come enunciato sulla formula, CONDIZIONALE[F-N] per l'identificazione con la soluzione di Dirichlet.
**Novità / O3:** confermo che F4L-P3 è un caso di L-S (la riduzione è esatta: s = −ε/2ν, X = U₀(Y)). La valutazione di S4-INTEG ("nessuna novità di tecnica") è corretta.

### 1.5 Kieffer et al. (§4.3, Q8)
Senza il PDF posso verificare solo ciò che non dipende dalla lettura del testo.
1. **Riduzione v = 0** (indipendente dal testo, data la loro equazione come riportata): w := δu risolve w_t + ww_x = Re^{−1}w_xx con dato δg (SymPy: identità esatta). Quindi la serie in δ di u è (serie di Volterra in ampiezza)/δ, con lo **stesso raggio** (u_ε si annulla in ε = 0: la divisione non cambia il raggio). OK.
2. **Tesi "raggio infinito per ogni t > 0 e quasi ogni x" falsa per v = 0:** per il dato di Dirac di massa A > 0, F4L-P3(iii) dà R(t,x) = (2ν/A)√(log²((1−Φ)/Φ)+π²) < ∞ per **ogni** (t,x). Questo vale **qualunque sia la massa** A del loro dato e qualunque sia la normalizzazione (e^{δRe} o e^{δRe/2}): la conclusione non dipende dalla discrepanza. Per un dato g generico in L¹ il raggio è comunque ≥ 2πν/w; la tesi "infinito" è falsificata dal solo controesempio di Dirac, se il loro enunciato include quel dato. **Sostenuto**, con due condizioni da verificare sul PDF: (a) che la tesi sia enunciata per v = 0 o per ogni v (inclusa v = 0); (b) che il dato di Dirac rientri nella classe della loro tesi. Se la tesi fosse solo per g ∈ L¹ liscio, il controesempio va dato con un dato liscio: basta g ≥ 0 a supporto compatto vicino a Aδ? **No**, la finitezza del raggio per dati lisci non segue da F4L-P3 (che dà solo un minorante). **K-1 (MINOR, SCOPE):** formulare la correzione come "per il dato di Dirac (che gli autori stessi usano come esempio) il raggio è finito in ogni x"; per una tesi su dati generici serve un controesempio liscio. Propongo di aggiungere: per g = A·(densità gaussiana stretta) il raggio resta finito — **non verificato da me**; lasciarlo fuori o verificarlo (APERTO).
3. **Argomento "misura nulla in x per δ fisso ≠ assenza di zeri complessi per x fisso"**: la distinzione logica è corretta (quantificatori invertiti: il raggio a x fisso è determinato dagli zeri complessi in δ a quel x).
4. **Discrepanza e^{δRe} vs e^{δRe/2}:** dall'interno della CHECK_REQUEST: con la forma integrale e^{−(δRe/2)1_{(0,∞)}(y)} (massa 1) il denominatore in x = 0 è (1+e^{−δRe/2})/2, nullo in δ = 2πi/Re e non in iπ/Re; con e^{δRe} (massa 2 o diversa normalizzazione) il polo è in iπ/Re (SymPy). La formula classica per dato Mδ ha esponente M/(2ν), quindi e^{δRe} corrisponde a M = 2 con ν = 1/Re. **Non posso decidere quale sia stampato** (PDF non letto; anche la numerazione è incerta: AUDIT-4 cita la (23), S4-INTEG la (30)). **K-2 (MINOR, REFERENCE):** (a) la riga KIEFFER-C deve restare "incoerenza (30) da verificare sul PDF" finché qualcuno non legge il PDF; (b) uniformare il numero dell'equazione ((23) in AUDIT-4, (30) in S4-INTEG: probabilmente versioni HTML/PDF diverse). In entrambe le letture la conclusione 2 regge.
**Stato proposto KIEFFER-C:** la parte "raggio finito per il dato di Dirac in ogni x, contro la tesi 'raggio infinito'" → DIMOSTRATO come conseguenza di F4L-P3(iii) **condizionatamente alla lettura corretta della loro tesi e del loro dato** (R7); la parte "incoerenza interna della (30)" → APERTO (da verificare sul PDF). Non pubblicare la correzione prima della lettura del PDF.

---
## 2. ALG-L1, ALG-T1, ALG-P3 (priorità 2)
### 2.1 ALG-L1
| MC | passo | esito |
|---|---|---|
| L1.1 | [D, D_N] derivazione nulla sui generatori | OK (commutatore di derivazioni; D_N(y_{k+1}) = D^{k+1}N = D(D^kN)). SymPy: KdV su un polinomio di prova. |
| L1.2 | ψ ben definita, ψ∘∂_x = D∘ψ, ψ∘∂_t = D_N∘ψ | OK: ψ-derivazioni che coincidono sui generatori; la commutatività (i) serve per ∂_x (D D_N^aD^b = D_N^aD^{b+1}). |
| L1.3 | ker ψ ⊇ [F] | OK. |
| L1.4 | G − ψ(G) ∈ [F] | OK: induzione su a (per ogni b), ∂_tp ≡ D_Np mod [F] perché ∂_x^k(y_t − N) ∈ [F] e ∂_x^kN = D^kN; passaggio a somme e prodotti. |
| L1.5 | dominio ⇒ [F] primo | OK. |
**PASS → DIMOSTRATO** (noto; Olver cap. 5 come riferimento di contesto).

### 2.2 ALG-T1 (con u analitica in (c)) — Q3
Enunciato canonico: ∀Ω ⊂ ℝ² aperto connesso, ∀N ∈ A, ∀u ∈ C^∞(Ω) con u_t = N(u,u_x,…): (a) I(u) = ψ^{−1}(J_u); (b) I(u) = [F] ⟺ J_u = 0; (c) se u ∈ C^ω(Ω): J_u primo e J_u ≠ 0 ⟺ trdeg_ℂ ℂ(u,u_x,…) < ∞, nel qual caso ∃k: ℂ⟨u⟩ = ℂ(u,…,∂_x^ku).
| MC | passo | esito |
|---|---|---|
| T1.1 | (a): G(u) = ψ(G)(u); J_u stabile per D, D_N | OK (D_N agisce come ∂_t **sulle soluzioni**: usa u_t = N(u) su Ω). |
| T1.2 | (b) | OK (ψ(p) = p per p ∈ A). Vale per u ∈ C^∞: nessuna analiticità usata. |
| T1.3 | (c) primalità | OK: J_u = nucleo di A → C^ω(Ω;ℂ), dominio per Ω connesso. **Precisazione:** i polinomi hanno coefficienti in ℂ, quindi il dominio è C^ω(Ω;**ℂ**) (funzioni a valori complessi analitiche reali), non C^ω(Ω) reale; resta un dominio. → **T1-1** (COSMETIC). |
| T1.4 | (⇐) trdeg d < ∞ ⇒ relazione | OK. |
| T1.5 | k = 0 | OK: p ∈ ℂ[y₀]∖0, u continua a valori nell'insieme finito degli zeri, Ω connesso ⇒ u costante ⇒ ℂ(u,…) = ℂ, trdeg 0. (Q3: trattato correttamente.) |
| T1.6 | separante S = ∂p/∂y_k ≠ 0 e S ∉ J_u | OK: p ha ordine k quindi deg_{y_k}p ≥ 1 e S ≠ 0 (car. 0); S ha ordine < k (contro la minimalità dell'ordine) oppure ordine k e grado in y_k minore (contro la minimalità del grado). L'ordine lessicografico (ordine, poi grado nel leader) è quello giusto. (Q3: sì.) |
| T1.7 | D^jp = S·y_{k+j} + R_j, ord R_j < k+j | OK (j ≥ 1; DS ha ordine ≤ k+1 ≤ k+j). Per j = 0 la relazione è p stessa, non lineare in y_k: non serve. |
| T1.8 | ∂^{k+j}u ∈ ℂ(u,…,∂^ku); trdeg ≤ k; derivate in t nel x-getto (via (a)) | OK; la chiusura di ℂ(u,…,∂^ku) per ∂_t e ∂_x segue perché le derivate dei generatori stanno nel campo. |
| T1.9 | "Serve un'ipotesi in più su N?" | **No.** N è un polinomio qualsiasi in A; (c) non usa altro di N che u_t = N(u) (solo per ℂ⟨u⟩ = ℂ(x-getto)). L'unica ipotesi necessaria in più rispetto a (a),(b) è l'analiticità (O10, recepita). Senza analiticità (c) può fallire: S(u) può annullarsi su un aperto senza essere ≡ 0 (C^∞ non è un dominio). |
**PASS-con-fix(T1-1) → DIMOSTRATO**; (b) CON-FONTE parziale (Scholl et al., ordine finito) come dichiarato.

### 2.3 ALG-P3 — definizione di forma chiusa e dicotomia (O7)
| MC | passo | esito |
|---|---|---|
| P3a.1 | ℂ(u,u_x,…) ⊆ K, trdeg ≤ m | OK (K campo chiuso per ∂_x contenente u). |
| P3a.2 | ⇒ J_u ≠ 0 ⇒ I(u) ⊋ [F] | OK. Usa solo la direzione **facile** (⇐) di ALG-T1(c) (d+1 elementi in un campo di trdeg d sono dipendenti) e ALG-T1(b). |
| P3a.3 | casi: EP/razionali, Cole–Hopf di EP, N-solitoni | OK: ℂ(t,x,e^{z_l·(t,x)}) e ℂ(E_1,…,E_N) sono chiusi per ∂_x; u = −2νφ_x/φ con φ EP e u = 2∂²log f stanno in quei campi. SymPy: relazione d'ordine 1 del 1-solitone (u_x² = u² − 2u³, con separante 2u_x ∉ J_u). |
**Sulla definizione.** "Forma chiusa := ℂ⟨u⟩ immerso in un campo ∂_x-chiuso di trdeg finito dentro Frac C^ω(Ω;ℂ)" è precisa, non dipende da scelte arbitrarie e copre anche le funzioni D-finite in x (ℂ(x,u,…,u^{(r−1)}) è chiuso per ∂_x) e le liouvilliane elementari (erf ecc.). Esclude correttamente la rappresentazione integrale di Cole–Hopf con U₀ generico (O7). OK.
**Sulla frase "la dicotomia è un teorema e non è tautologica".** È **sovraenunciata**: ALG-P3 è corretto ma è un corollario di una riga (P3a.2) — dato ALG-T1(b), "trdeg finito ⇒ non identifica" è quasi la definizione. Il contenuto non banale della dicotomia sta altrove: (1) in ALG-T1(b) (J_u = 0 ⇒ I(u) = [F], che usa ALG-L1) e (2) nel **viceversa** di ALG-T1(c) (identificazione ⟺ trdeg = ∞, che usa il separante e l'analiticità). → **P3a-1 (MINOR, OVERSTATED):** riscrivere il "Limite (O7)" come: "Con questa definizione, la dicotomia è ALG-T1(c): u analitica identifica ⟺ trdeg ℂ⟨u⟩ = ∞; ALG-P3 ne è la direzione facile (forma chiusa ⇒ non identifica). La parte non banale è la direzione opposta. La dicotomia non è un'evidenza indipendente (O7): è un teorema dentro un solo linguaggio."
→ **P3a-2 (COSMETIC):** stesso fix di T1-1 (campo dentro Frac C^ω(Ω;ℂ)).
**PASS-con-fix(P3a-1, P3a-2) → DIMOSTRATO.**

---
## 3. INT-T1 (priorità 3)
### 3.1 (A), (UC-ω)
Canonico (A): se (UC) vale per ogni d, allora 𝒜(u) = c + {d : K_d[u(t,·)] ≡ 0 ∀t ∈ I}. OK (linearità di d ↦ K_d). (UC-ω): K_d[u] analitica su I×ℝ connesso, nulla su Ω aperto non vuoto ⇒ nulla ovunque. OK. **PASS → DIMOSTRATO.**

### 3.2 (UC-1) e la tesi su Saut–Scheurer (Q1)
| MC | passo | esito |
|---|---|---|
| UC.1 | ∂_tK_d[u] = K_d′[u]u_t | OK: K_d[u] è un polinomio differenziale nelle sole x-derivate; u ∈ C^∞(I×ℝ). |
| UC.2 | K_d′[u]K_c[u] = K_c′[u]K_d[u] (F-C, bilinearità) | OK come uso di F-C. Red team: F-C verificata in SymPy come **identità in u** per K_0,…,K_3 (K_n generati dalla ricorrenza 𝓡, K_1, K_2 coincidono con le formule date). |
| UC.3 | K_1′[u]w = −(w_xxx + 6uw_x + 6u_xw) | OK (SymPy). |
| UC.4 | riduzione di segno x̃ = −x se c_1 < 0, s = |c_1|t | OK: ∂_x³ = −∂_x̃³; i coefficienti di ordine inferiore restano lisci; r_2 = 0. |
| UC.5 | esaustione e "componenti orizzontali" (R1) | OK con la lettura standard: per ω = palla B ⊂ Ω (connessa) e rettangolo (a,b)×(t₁,t₂) ⊃ B, F-SS dà w = 0 su (a,b)×π_t(B). Basta questa forma (ω connesso, rettangolo fisso, poi a → −∞, b → +∞ e ricoprimento di I con le proiezioni di palle centrate in punti di Ω su ogni fetta, π_t(Ω) = I). Quindi R1 si chiude **senza** usare la forma più forte "componenti orizzontali di ω non connesso". → **UC-1a (MINOR):** scrivere la prova con palle B ⊂ Ω e rettangoli, come sopra; la conclusione resta identica. |
| UC.6 | Ipotesi di regolarità di F-SS su w | w = K_d[u] ∈ C^∞: qualunque classe di regolarità richiesta da Saut–Scheurer (p.es. L²_tH³_loc) è soddisfatta. OK, da annotare. |
| UC.7 | **Necessità di c_1 ≠ 0** | Corretta e necessaria: se il flusso vero è la sola traslazione (c_1 = 0), w_t + c_0w_x = 0 è di trasporto e la UC fallisce. Controesempio (red team): u = u₀(x − c_0t), u₀ liscia di classe di Faddeev, u₀ ≡ 0 su (−1,1), Ω = {|x − c_0t| < ½}, π_t(Ω) = I: allora K_d[u] = 0 su Ω per **ogni** d (u ≡ 0 su Ω), mentre K_0[u] ≢ 0. L'enunciato ha già c_1 ≠ 0. → **UC-1b (MINOR):** aggiungere questo controesempio come nota di necessità, e scrivere "flusso vero di ordine **esattamente** 3". |
**Tesi di S4-INTEG ("Saut–Scheurer limita l'ordine del flusso vero, non la classe 𝓗_M"): CONFERMATA.** Il punto è UC.1–UC.2: w = K_d[u], per qualunque d ∈ ℝ^{M+1} (ordine 2M+1 qualsiasi), risolve la **linearizzazione del flusso vero** K_c, che ha ordine 3 se c = (c_0, c_1, 0, …) con c_1 ≠ 0. L'ordine di K_d non entra mai nell'equazione per w. Quindi la riga 7 di AUDIT-4 ("non copre i flussi superiori K_c con c ∈ 𝓗_M, M ≥ 2") va letta come: non copre i dati il cui flusso **vero** è d'ordine ≥ 5; copre ogni dato KdV in ogni 𝓗_M. La correzione a CIT-AUDIT-4 è giusta.
Limiti che restano: (i) F-SS è da fonte secondaria (KPV, arXiv:math/0009065): CON-FONTE da completare; (ii) O4: la UC è instabile, INT-T1 resta un teorema d'identificabilità con dato esatto (lo dice §1.1 "Limite O4"); (iii) flusso vero d'ordine ≥ 5 e u non analitica: APERTO.
**PASS-con-fix(UC-1a, UC-1b) → CONDIZIONALE[F-C, F-SS]** (riduzione DIMOSTRATA).

### 3.3 (B) e Lemma B1 (Q2)
| MC | passo | esito |
|---|---|---|
| B.1 | K_d[u] = −Σ_jk_jq_d(k_j²)∂_{c_j}u (da F-MS) | OK come uso di F-MS. Coerenza: per n = 0, K_0 = −u_x = −Σk_j∂_{c_j}u è immediato (η_j = k_jx + …); per n = 1 è la dipendenza da t di η_j. Red team V-ex esteso: N = 2, k = (1,2), n = 0,1,2,**3**, in 3 punti × 3 scelte di (c_1,c_2): residuo < 10⁻²⁰. Novikov 4K_0 − 5K_1 + K_2 = 0 verificata. |
| B.2 | αx + β → 0 per x → −∞ | OK: il membro sinistro Σa_j∂_{c_j}f/f → 0 (tutti gli E_i → 0, f → 1), quindi α = 0 (altrimenti |αx+β| → ∞) e poi β = 0. (Q2: sì, il passo è completo.) |
| B.3 | divisione per E_{j₀}, k_{j₀} minimo fra gli a_j ≠ 0 | OK: ∂_{c_j}f = E_j(1 + O(max_iE_i)); E_j/E_{j₀} → 0 per k_j > k_{j₀} (k distinti); il termine O(max E) → 0. |
| B.4 | Vandermonde: dim = max(0, M+1−N) | OK. |
**Lemma B1: PASS → DIMOSTRATO.** **(B): PASS → CONDIZIONALE[F-MS]** (F-MS classico, Hirota/Sato, non letto; V-ex qui N = 2, n ≤ 3). Nota: con UC-ω (multi-solitoni analitici) (A) si applica senza F-SS.

### 3.4 (C) — solo riduzione
(⇒) e (⇐) corretti dati F1–F3: e^{as} = 1 ∀s ⟺ a = 0; per r: kq_d(−4k²) = 0 ⟺ q_d(−4k²) = 0 (k > 0); per i c_j serve c_j ≠ 0 (F2). Coerenza dei moltiplicatori: con q_d = 1 (K_0, traslazione) e q_d = λ (K_1) si ritrovano e^{−2iks} ed e^{8ik³s} (convenzione standard per r); per i c_j il segno differisce dalla convenzione usuale (c_j(t) = c_j(0)e^{4κ_j³t}), irrilevante per il conteggio (R3: chiuso). Conteggio (a), (b) corretti (un polinomio nullo su un insieme infinito è nullo; r continuo).
→ **C-1 (MINOR):** in (b) "u identifica in 𝓗_∞ ⟺ identifica in ogni 𝓗_M": precisare che 𝓗_∞ = ∪_M𝓗_M (polinomi q_d di grado arbitrario finito). **Riduzione PASS-con-fix(C-1); stato CONDIZIONALE[F1–F4] invariato.**

### 3.5 INT-T2 — solo riduzione
Conteggio dei polinomi reali di grado ≤ M nulli su Λ ⊂ ℂ chiuso per coniugio: un punto non reale e il suo coniugato impongono 2 condizioni reali indipendenti; dim = max(0, M+1−|Λ|). OK. Red team: [T_2, T_3] = 0 (flussi NLS, componente q, q e r = q̄ come variabili indipendenti), coerente con la gerarchia usata. **Riduzione PASS; CONDIZIONALE[ZS, UC] invariato.**

---
## 4. Hirota INT-P5 / INT-P6 (Q7)
| MC | passo | esito |
|---|---|---|
| H.1 | det(I+C) = Σ_S det C_S, Cauchy, det C_S = a_SE^S | OK (SymPy N = 3 simbolico in E). |
| H.2 | K matrice di Gram ⇒ I + C ≻ 0 | OK (minori principali di K positivi in SymPy). |
| H.3 | Z = 𝔼_μ[ΠA^{μ_iμ_j}], cumulanti solo a coppie (Möbius) | OK (SymPy N = 3, tutti gli S). |
| H.4 | ΠA ≤ Z ≤ 1, limiti a ±∞ | OK. |
| H.5 | derivate di p_i: O(min(p_i, 1−p_i)), decadimento esponenziale di Z_x, Z_xx | OK (Z multilineare in p, derivate limitate su [0,1]^N). |
| H.6 | **Q7:** E_int ∈ L¹ e ∫E_int = 0 in senso di Lebesgue | **Sì.** E_int = 2(log Z)_xx è continua e |E_int(x)| ≤ Ce^{−κ|x|} per |x| grande (κ > 0 dipende da k_min e dalle fasi), quindi E_int ∈ L¹(ℝ); per convergenza dominata ∫_ℝ = lim_{R→∞}∫_{−R}^R = lim 2[(log Z)_x]_{−R}^R = 0. Z ≥ ΠA > 0 serve per controllare 1/Z. |
| H.7 | ∫u = 2Σk_i | OK (1-solitone: ∫(k²/2)sech²(kx/2) = 2k). Red team N = 3: ∫E_int con errore < 10⁻¹⁰ per quadratura diretta, 2[(log Z)_x] < 10⁻¹⁵, ∫u = 2Σk. |
| H.8 | (c) E_int ≢ 0 | OK. |
| H.9 | (e) formula di Jacobi, O(N³) | OK (mpmath: (log f)″ = tr(M^{−1}M″) − tr((M^{−1}M′)²) a 20 cifre). Il costo O(N³) è in operazioni aritmetiche reali (più N esponenziali): da dire, COSMETIC. |
**INT-P5, INT-P6: PASS → DIMOSTRATO.** Nessuna novità rivendicata (corretto).

---
## 5. F4LIN-T2 (Q6)
### 5.1 (0), (i), (ii)
Tutti i passi OK: φ risolve il calore; Hopf–Lax (minimo in y = x − c_it); log-sum-exp; profilo tanh, L¹ = 4ν ln 2, L² = 4νΔ(ln2 − ½), L^p per scala, Ḣ¹ = Δ³/12ν, coda 4νe^{−Δη/2ν} (SymPy/mpmath esatti o a 25 cifre). Ḣ^s: **R5 chiuso** — in forma chiusa F̂(η) = i(π csch(πη/2) − 2/η) (trasformate in valore principale di sgn e tanh; verificata numericamente in 3 punti a 15 cifre). Da qui F̂(η) = −iπ²η/12 + O(η³) in 0 e F̂(η) = −2i/η + O(e^{−πη/2}) all'infinito, e l'intervallo −3/2 < s < ½ è dimostrato, non solo motivato. → **L-1 (MINOR):** inserire la forma chiusa di F̂ in (ii). L'identificazione di u⁰ con la soluzione entropica (Lax–Oleinik, Evans §3.4) resta CON-FONTE con numero da verificare (non usata in (i)–(iii)).
### 5.2 (iii)
| MC | passo | esito |
|---|---|---|
| L.1 | ‖E‖_{L¹} = TV(D), D lipschitziana | OK. |
| L.2 | δ = inf h > 0 raggiunto, h ≥ max(δ, a|x| − b) | OK: h continua (statistiche d'ordine), positiva (nessun punto triplo), crescita lineare. (Q6: sì.) |
| L.3 | concavità di g fra due rotture; unico massimo interno in un punto in cui S_(2) = S_(3) | OK: S_(1) = S_a strettamente minima nell'intervallo aperto, S_(2) = min_{i≠a}S_i concava, pendenze di g = c_j − c_a ≠ 0; un massimo di una funzione concava lineare a tratti con pendenze non nulle sta in un angolo, dove due rette si scambiano il secondo posto, quindi S_(2) = S_(3) e g = h ≥ δ. Sugli intervalli illimitati g è concava e → +∞, quindi crescente (o decrescente) strettamente. (Q6: sì.) |
| L.4 | 2K tratti monotoni | OK: K rotture ⇒ K−1 intervalli interni (2 tratti ciascuno) + 2 illimitati (1 tratto ciascuno) = 2K. TV(D_2) = 4νK ln2 − 4νΣ_{max}log(1+e^{−g_max/2ν}). (Q6: sì, conto corretto.) |
| L.5 | "D_2 è funzione **decrescente** di g" | **Errore di segno innocuo:** dD_2/dg = e^{−g/2ν}/(1+e^{−g/2ν}) > 0, quindi D_2 è **crescente** in g. Per l'argomento conta solo la monotonia stretta (stessi tratti di g). → **L-2 (COSMETIC).** |
| L.6 | TV(D − D_2) ≤ C_c(N−2)∫e^{−h/2ν} | OK: |(D−D_2)′| ≤ 2ν(|R′| + R|g′|/2ν) ≤ 2max|c_i−c_j|·R, R ≤ (N−2)e^{−h/2ν}; continuità di R e C¹ a tratti (finiti scambi d'etichetta). |
| L.7 | ∫e^{−h/2ν} ≤ e^{−δ/4ν}∫e^{−h/4ν} ≤ (2b/a + 8/a)e^{−δ/4ν} | OK (corretto, ν ≤ 1). **Ma non ottimale:** spezzando in |x| ≤ (b+δ)/a (dove h ≥ δ) e il resto (dove h ≥ a|x| − b > δ) si ottiene ∫e^{−h/2ν} ≤ (2(b+δ)/a + 4ν/a)e^{−δ/2ν}. Quindi **TV(D − D_2) ≤ C′e^{−δ/2ν}** e l'enunciato migliora a |‖E‖_{L¹} − 4νK ln2| ≤ (4ν(K−1) + C′)e^{−δ/2ν}. → **L-3 (MINOR, UNDERSTATED, facoltativo):** l'enunciato attuale è vero; il fix lo rafforza. |
| L.8 | (5) |TV(D) − TV(D_2)| ≤ TV(D−D_2) | OK. |
**Controllo numerico di S4-INTEG** (N = 3, K = 2, δ = 2, ν = 0.05: errore 1.8·10⁻⁵): con la stima L-3 l'errore dovrebbe essere O(e^{−20}) ≈ 2·10⁻⁹ (a meno della costante), quindi quel valore non è compatibile né con L-3 né con il red team (§11: errore/e^{−δ/2ν} ∈ [0.1, 0.4] su tutti i casi provati). È con ogni probabilità errore di quadratura (E salta nelle rotture) o un δ diverso da 2 nella configurazione usata: da ricontrollare. Non cambia il verdetto (il valore era comunque sotto il maggiorante dichiarato).
**F4LIN-T2: PASS-con-fix(L-1, L-2, L-3) → DIMOSTRATO.** La costante 4ν ln 2 è elementare (Wang 1998 da verificare): nessuna novità rivendicata, corretto.

---
## 6. MODREL-T1 + Cor. + Burgers (Q4)
| MC | passo | esito |
|---|---|---|
| M.1 | (T1) saturazione: w = (a/b)v, b | a·gcd(v_j) = a ⇒ b unità | OK (R fattoriale). Red team: con v non primitivo (v = ξ·(τ,ξ)) R·v non è saturato. |
| M.2 | 0 → Syz → R² → M_f(u) → 0, M_f(u) = Rf_1(u) + Rf_2(u) ⊂ 𝒜 | OK (M finitamente generato anche se 𝒜 non lo è). |
| M.3 | piattezza di K, rank Syz = 2 − rank M | OK (localizzazione). **Q4: sì**, puramente algebrico, valido in 𝒜 = D′(Ω). |
| M.4 | rank M = 0 ⟺ M di torsione ⟺ entrambi i generatori di torsione | OK: per M f.g. su un dominio, M⊗K = 0 ⟺ M di torsione; la torsione è un sottomodulo (R dominio). **Q4: sì.** |
| M.5 | Syz = Rv ⟺ rank Syz = 1 ⟺ Ann f_1(u) = 0 o Ann f_2(u) = 0 | OK. |
| M.6 | Burgers: v ∈ Syz, gcd(τ − νξ², ½ξ) = 1 | OK (SymPy); vale anche per ν = 0. |
| M.7 | **ipotesi mancante:** in 𝒜 = D′(Ω) il prodotto f_j(u) non è definito per u distribuzione qualsiasi | **M-1 (MINOR, HIDDEN_ASSUMPTION):** aggiungere "u tale che f_j(u) ∈ 𝒜" (p.es. u ∈ L^p_loc(Ω) con p ≥ max deg f_j, oppure u ∈ C^∞). Per 𝒜 = C^∞, C^ω nulla da aggiungere. |
**PASS-con-fix(M-1) → DIMOSTRATO.**

## 7. ALG-P4 (Cole–Hopf)
| MC | passo | esito |
|---|---|---|
| CH.1 | dω_u = F_B(u)dt∧dx; primitiva analitica; φ = e^{−ψ/2ν} > 0 risolve il calore | OK (SymPy: dω_u, identità F_B(−2νφ_x/φ) = −2ν∂_x((φ_t−νφ_xx)/φ)). |
| CH.2 | unicità di φ a meno di costante | La prova dà l'unicità di ψ con dψ = ω_u, non direttamente quella di φ fra le φ̃ > 0 con u = −2νφ̃_x/φ̃ e φ̃_t = νφ̃_xx. Chiusura (una riga): ψ̃ := −2ν log φ̃ ha ψ̃_x = u e ψ̃_t = −2ν²φ̃_xx/φ̃ = νu_x − u²/2, quindi dψ̃ = ω_u e ψ̃ = ψ + cost. → **P4-1 (MINOR).** |
| CH.3 | (b) triangolarità r_j, gradi di trascendenza che differiscono di ≤ 1, ALG-T1(b,c) su Burgers e calore | OK (ν ≠ 0 serve per la triangolarità: è nell'ipotesi ν > 0). |
| CH.4 | (c) I(φ) ∩ L = Ann(φ)y; [Py] ∩ L = R·Py (ideale generato da forme lineari omogenee) | OK. |
| CH.5 | viceversa falso: G_ν, u = x/t, y_2 ∈ J_u; Ann(G_ν) = (τ − νξ²) | OK (SymPy); Ann(G_ν) = (τ−νξ²) per C3-T1(a) (P irriducibile, G_ν ∉ EP perché G_ν(t,0) ∝ t^{−1/2}); stesso argomento già controllato in AUDIT_P4-L7 L7.19. Ω ⊂ {t > 0} rettangolo (semplicemente connesso). R6: lo stato ereditato è DIMOSTRATO. |
**PASS-con-fix(P4-1) → DIMOSTRATO.**

## 8. ALG-P6 (Miura)
Identità KdV[−(v²+v_x)] = −(2v+∂_x)mKdV[v] verificata in SymPy (esatta). v_k ∈ ℂ(x-getto di u)[v] per induzione (v_x = −u − v²); ℂ(x-getto di v) = ℂ(x-getto di u)(v); ALG-T1(b,c) su KdV e mKdV (u analitica perché v lo è). **PASS → DIMOSTRATO.**

---
## 9. Rilievi e fix (riepilogo)
| ID | claim | severità · tipo | fix |
|---|---|---|---|
| P3-1 | F4L-P3(i) | COSMETIC · notazione | w′ → sup|U₀| nella dominazione. |
| P3-2 | F4L-P3 | MINOR · REFERENCE | "u_ε è la soluzione di Burgers con dato εu₀" CONDIZIONALE[F-H] per dato misura; (i)–(iii) come enunciati sulla formula non ne dipendono. |
| P3-3 | F4L-P3, tabella §5 | COSMETIC | "ottimale" = costante uniforme raggiunta in x = 0. |
| P3-4 | F4L-P3(iv) | MINOR · costante | ‖∂_xG_N(t,x,·)‖_{L¹(0,L)} ≤ (πνt)^{−1/2} per immagini: stessa costante di (ii). |
| K-1 | KIEFFER-C | MINOR · SCOPE | formulare la correzione per il dato di Dirac; per dati lisci serve un controesempio a parte (APERTO). Verificare sul PDF che la tesi copra v = 0 e il dato di Dirac. |
| K-2 | KIEFFER-C | MINOR · REFERENCE | e^{δRe} vs e^{δRe/2}: NON verificato (PDF non leggibile da questa sessione); uniformare (23)/(30). |
| T1-1 | ALG-T1(c) | COSMETIC | C^ω(Ω;ℂ). |
| P3a-1 | ALG-P3 | MINOR · OVERSTATED | "non tautologica" → "direzione facile di ALG-T1(c); il contenuto non banale è il viceversa". |
| P3a-2 | ALG-P3 | COSMETIC | come T1-1. |
| P4-1 | ALG-P4(a) | MINOR · gap di una riga | unicità di φ (prova in CH.2). |
| M-1 | MODREL-T1 | MINOR · ipotesi | f_j(u) ∈ 𝒜 (rilevante per D′). |
| UC-1a | INT-T1(UC-1) | MINOR · R1 | esaustione con palle e rettangoli; chiude R1 senza la forma "componenti di ω non connesso". |
| UC-1b | INT-T1(UC-1) | MINOR | ordine esattamente 3 (c_1 ≠ 0) necessario: controesempio della traslazione. |
| C-1 | INT-T1(C) | MINOR | 𝓗_∞ = ∪𝓗_M. |
| L-1 | F4LIN-T2(ii) | MINOR · R5 | F̂(η) = i(π csch(πη/2) − 2/η). |
| L-2 | F4LIN-T2(iii) | COSMETIC | D_2 crescente (non decrescente) in g. |
| L-3 | F4LIN-T2(iii) | MINOR · UNDERSTATED (facoltativo) | errore O(e^{−δ/2ν}) invece di O(e^{−δ/4ν}). |

## 10. Risposte alle domande Q1–Q8
- **Q1 (UC-1).** Sì: w = K_d[u] risolve la linearizzazione del flusso **vero** (F-C), d'ordine 3 per ogni M; la riduzione di segno è corretta; l'esaustione è corretta con palle e rettangoli (UC-1a), e chiude R1. Serve c_1 ≠ 0 (UC-1b). La correzione a CIT-AUDIT-4 r. 7 è giusta.
- **Q2 (B1).** Sì, completo, incluso αx + β → 0 (⇒ α = β = 0).
- **Q3 (ALG-T1(c)).** Sì: k = 0 e la minimalità (ordine, poi grado nel leader) sono corretti; nessuna ipotesi in più su N; serve solo l'analiticità (e C^ω(Ω;ℂ), T1-1).
- **Q4 (MODREL Cor.).** Sì, entrambi i punti, in D′(Ω) con l'ipotesi M-1.
- **Q5 (L-S/F4L-P3).** Sì: la minorazione e le stime (ii) sono corrette (red team); il dato δ è compatibile come **definizione** (formula di Cole–Hopf); l'identificazione con la soluzione è CONDIZIONALE[F-H misure] (P3-2).
- **Q6 (F4LIN-T2(iii)).** Sì a concavità, δ > 0, 2K tratti, TV(D−D_2) ≤ Ce^{−δ/4ν}; il segno "decrescente" è sbagliato ma innocuo (L-2); la stima si migliora a e^{−δ/2ν} (L-3).
- **Q7 (Hirota).** Sì: Z ≥ ΠA e il decadimento esponenziale danno E_int ∈ L¹ e ∫ = 0 per convergenza dominata (H.6).
- **Q8 (Kieffer).** Il ragionamento è corretto per v = 0 e dato di Dirac, **qualunque** sia la normalizzazione: il raggio è finito in ogni x. L'inversione dei quantificatori nel loro argomento è individuata correttamente. La discrepanza e^{δRe}/e^{δRe/2} **non** è verificabile senza il PDF (fetch bloccato): R7 resta aperto; non pubblicare prima di leggerlo (K-1, K-2).

## 11. Red team (`audit_s4integ.py` → `.out`)
**69/69 OK** (ultima esecuzione completa). Contenuto:
- **L-S**: settore verificato su 200 leggi casuali a 2–5 atomi × 20 punti della striscia; zeri della legge a due punti.
- **F4L-P3**: formula tanh (esatta); R(t,x) su 3 terne (zero del denominatore a 20 cifre, |zero| = formula, radice n-esima n = 40 entro il 10%, R ≥ 2πν/A); stima (ii) su 30 dati a gradini × 15 punti di |ε| = r; nucleo di Neumann per immagini: positività, massa 1, ∂_xG_N = 0 al bordo, ‖∂_xG_N‖_{L¹(0,L)} ≤ (πνt)^{−1/2} (P3-4).
- **Kieffer**: forma integrale di massa 1 nulla in 2πi/Re e non in iπ/Re; 1 + e^{δRe} nulla in iπ/Re; w = δu risolve Burgers (identità esatta).
- **Hirota**: det(I+C) = f (N = 3, simbolico), K definita positiva, cumulanti solo a coppie, ∫E_int = 0 (residuo 10⁻³²), ∫u = 2Σk, E_int(0) ≠ 0, formula di Jacobi.
- **F4LIN-T2**: integrali di (ii), profilo di Burgers, F̂ in forma chiusa (3 punti, 15 cifre); (iii) a 40 cifre con quadratura spezzata nelle rotture: rette (1, 0, −1), t = 1 (K = 1, δ = ½) per ν = 0.05, 0.1, 0.2, errore/e^{−δ/2ν} = 0.10, 0.20, 0.37; 4 configurazioni casuali N = 4 (K ∈ {1,2}), errore ≤ e^{−δ/2ν}. Coerente con la stima migliorata L-3.
- **INT-T1**: K_0..K_3 dalla ricorrenza 𝓡 (∂^{−1} per ansatz di peso: K_2 è una derivata totale, K_3 locale); K_1, K_2 coincidono con §1.1; **F-C come identità in u per 0 ≤ m < n ≤ 3**; K_1′; **F-MS per N = 2, k = (1,2), n = 0..3** in 3 punti (mpmath 60 cifre, residuo relativo ≤ 3·10⁻⁶¹); Novikov (residuo 10⁻⁶⁰); Wronskiano B1 ≠ 0; controesempio c_1 = 0.
- **INT-T2**: [T_2, T_3] = 0. **ALG**: identità di Cole–Hopf, dω_u, controesempio G_ν, Miura, [D, D_N] = 0, relazione d'ordine 1 del 1-solitone. **MODREL**: gcd, non saturazione per v non primitivo.
Errori **miei** nelle prime versioni dello script, corretti (nessuno del pacchetto): confronto di autovalori con parte immaginaria numerica nulla; ∂^{−1} ingenuo con `integrate` (K_3 non locale, commutatori spuri); troncamento delle code in INT-P6 a |x| ≤ 40–60 (residui 10⁻⁸, 10⁻¹³ dovuti a e^{−k_min|x|}); valutazione in virgola mobile di F-MS (cancellazione, residuo 10⁻⁸ per n = 3) e poi valutazione simbolica esatta troppo lenta: sostituita da derivazione numerica mpmath a 60 cifre; un NameError. **Nota di processo:** in un tentativo di interrompere una mia esecuzione lenta ho usato un `kill` su tutti i processi `.venv/Scripts/python` attivi; può aver interrotto anche un'esecuzione di un'altra sessione in work/CHECK/sympy (audit_s4id.py, rilanciata alle 11:56). Segnalato al coordinatore.

## 12. Dichiarazione sui limiti di questo audit
- Non ho letto nessuna fonte primaria (F-H, F-N, F-SS, F-C, F-MS, F1–F4, Kieffer et al.): gli stati CONDIZIONALE[…] sono proporzionati a questo. Il PDF di Kieffer et al. non era raggiungibile (policy di rete).
- Kill-argument non eseguito (non richiesto; ALG-T1 e MODREL-T1 sono corollari corti, ben dentro la portata del proof-check). Se S4-ID li mette sul cammino critico di G★′-NL, il punto da attaccare è la **definizione di identificazione** (I(u) = [F], Syz = R·v) rispetto al dato M3 finito, non le prove.
