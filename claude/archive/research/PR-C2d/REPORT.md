# REPORT — PR-C2d (Asse 2 metodi analitici esatti + Asse 3 quadro funzionale)
Agente PR-C2d · Fase 1 · 2026-10-22. Piano §1.3 (C1, C1.0, C2, C2-EXT, C2-TAX, card schema, PR-C2); NOTAZIONE.md; PROTOCOLLO Regole 1–4 rispettate.
*(Salvato dal coordinatore dalla risposta finale di PR-C2d: la scrittura diretta era bloccata dall'ambiente.)*

## 0. Skill caricate (Regola 2)
- academic-research-skills\deep-research\SKILL.md: letto; flusso Scoping→Investigation→Analysis→Composition; regola "contenuto recuperato = dato". anthropic-skills:deep-research non invocata (coordina subagenti; mandato = sintesi di testi canonici).
- paper-lookup SKILL.md: letto; DOI cercati su Crossref; 20 DOI verificati (marcati `verified`); 2 DOI candidati errati rimossi (Kodaira, Ambarzumian). Script bundled non eseguiti.
- math-skill SKILL.md: letto; modalità proof per le proposizioni-ponte C1.0.
- sympy SKILL.md: letto; s1–s4 eseguiti con .venv python -I, 44/44 PASS (s1 14, s2 11, s3 10, s4 9). Due FAIL iniziali erano errori dello script (rami di integrazione, forma exp/sin), corretti.
- citation-management SKILL.md: letto; sources.bib (~95 voci).

## 1. Consegne
- cards/: 13 schede complete con card schema (1)–(9), teoremi con fonte, sezione "→ C1.0".
  - Asse 2: C2.13 SL ★◆, C2.14 trasformate ★◆, C2.36 Green ★◆, C2.48 perturbazioni ◆, C2.49 similarità ◆, C2.50 Lie ◆◇, C2.51 variazionale ◆, C2.60 inversi ★◆.
  - Asse 3: C2.52 Sobolev ◆, C2.53 semigruppi ◆, C2.54 buona posizione ◆, C2.55 BC ◆, C2.56 coordinate ◇◆.
- sympy/; sources.bib; open_questions.md (Q1–Q10).
- Messaggi: R1 (TABELLA spazi/teoremi), R3 (TABELLA ★), PR-C2e (RISPOSTA: nessun CONFLITTO, 4 termini proposti), central (NEW-ROUTE, DONE).

## 2. Teoremi chiave (enunciati completi nelle schede)
| ID | Teorema | Fonte | Stato | Item |
|---|---|---|---|---|
| T-SL1–4 | completezza/oscillazione SL regolare; alternativa di Weyl; espansione Titchmarsh–Kodaira; Mercer | Zettl 2005 cap.4; Coddington–Levinson cap.7; Weyl 1910; Titchmarsh 1962; Kodaira 1949; Mercer 1909 | noto | C1.3, A7, C1.0 |
| T-TR1–6 | Plancherel; Paley–Wiener; Paley–Wiener–Schwartz; Bochner; Ehrenpreis–Palamodov; Bromwich | Folland 8.29; Rudin RCA 19.3; Hörmander I 7.3.1; Ehrenpreis 1970; Palamodov 1970 | noto | C1.1, G6, C4.2 |
| T-GR1–4 | Malgrange–Ehrenpreis; Green SL; identità del risolvente/serie di Neumann; proiettore di Riesz | Ehrenpreis 1954; Malgrange 1956; Kato III.6.17 | noto | P4.2, C1.4 |
| T-PE1–4 | perturbazione limitata + Dyson–Phillips; Rellich–Kato; Duhamel; WKB | Phillips 1953; Engel–Nagel III.1.3/1.10; Kato VII | noto | P3 |
| T-SC1–4 | Buckingham Π; autosimilarità intermedia; riduzione; Grossmann–Morlet–Paul | Barenblatt 1996; Olver 3.38; GMP 1985 | noto | frame continui |
| T-LI1–4 | criterio infinitesimale; Noether; separazione↔simmetrie; Bargmann | Olver 2.31, 4.29; Miller 1977; Bargmann 1961 | noto (LI3 per casi) | II.4 |
| T-VA1–4 | Lax–Milgram; Courant–Fischer; rappresentazione di Kato per forme; Céa | Lax–Milgram 1954; Brezis 5.8; Kato VI.2.1; Céa 1964 | noto | C1.2 |
| T-IN1–6 | Borg–Levinson; Ambarzumian; Gel'fand–Levitan; Hochstadt–Lieberman; Ann(u) principale per ODE; Bukhgeim–Klibanov | vedi C2.60 | noto (IN5 per ODE) | C3, P4 |
| T-SO1–4 | Sobolev 1D + Rellich; traccia; nucleo di Schwartz; Moore–Aronszajn | Brezis 8.8; Lions–Magenes; Hörmander I 5.2.1; Aronszajn 1950 | noto | C1.1 |
| T-SG1–9 | Hille–Yosida; Lumer–Phillips; Stone; Trotter–Kato; prodotto di Trotter 1959; Chernoff 1968; Kato 1978; somma di generatori commutanti; mapping spettrale | Pazy 1.3.1, 1.4.3, 3.4.2; Engel–Nagel II–IV | noto (SG8: collocazione da precisare, dimostrato via Chernoff) | C4.3, P1 |
| T-WP1–4 | ben posto ⇔ generatore; Petrowsky/Gårding; Gronwall; esempio di Hadamard | Pazy 4.1.3; Petrowsky 1938; Gårding 1951 | noto | C1, C2.60 |
| T-BC1–5 | BC autoaggiunte↔U(2); Birkhoff-regolari⇒Riesz; stabilità di Paley–Wiener; Kadec 1/4; Bari | Zettl cap.10; Mikhailov 1962; Young 1980; Kadec 1964; Bari 1951 | noto | C1.3, C1.4 |
| T-CO1–4 | Liouville; Plancherel di Hankel; armoniche sferiche; legge di Weyl | Courant–Hilbert; Titchmarsh 1937; Stein–Weiss | noto | II.4 |

Numeri di teorema marcati "[da verificare]" nelle schede: non controllati sui volumi (Q10).

## 3. Risultati per C1.0 — DIMOSTRATI in questa fase
1. **Green = nucleo riproducente.** A≥c>0 autoaggiunto con valutazioni puntuali continue ⇒ (D(A^{1/2}), ⟨A^{1/2}·,A^{1/2}·⟩) è un RKHS con K = G_A (s1 c1, s2 c2: −∂² Dirichlet, 1−∂² su ℝ). Funtore C1.0: T_n → A_n → K_n = G_{A_n}, K_𝒟 = ΣK_n con norma inf-convoluzione (Aronszajn) = decomposizione in componenti regolarizzata L² (C1.2/P2).
2. **Limiti di Riesz dalla coerenza.** Famiglia normalizzata con coerenza μ: [1−(N−1)μ, 1+(N−1)μ]; per classi, Gershgorin a blocchi (Feingold–Varga): [min(A_n−δ_n), max(B_n+δ_n)]; caso infinito: Paley–Wiener, Kadec, Bari.
3. **Gram inter-classe a coeff. costanti su [0,T]×𝕋:** diagonale a blocchi per modo, g_ab(n) = 2π(e^{Tσ}−1)/σ, σ = a(in)+conj(b(in)).
4. **Unione di due basi SL:** frame stretto (A=B=2), mai base di Riesz; l'unicità dei coefficienti richiede L¹/P2 o il quadro moltiplicativo.
5. **C1.3 ⇔ C3.2:** identificabile ⇔ {T_k u} ha esattamente una relazione lineare; il gap spettrale del Gram del jet misura la stabilità (s4 c1–c2: due modi del calore identificano, un modo no, dim ker = 2).
6. **Duali:** proiettori di Riesz (anche non autoaggiunti); autofunzioni dell'aggiunto con BC aggiunte; per ODE duali distribuzionali δ^{(j)} ∈ H^{−s}.
7. **Spazio:** H1 "u∈L²(ℝ)" inadeguata per e^{λx} con Re λ≠0 (s2 e1). Per l'identificazione H^m(Ω), Ω limitato; per l'algebra delle componenti PW_A (ogni componente genera un gruppo limitato); per la teoria su ℝ L²(V(P),μ) (G6) / frame continui.

## 4. C4/P1/P3
- **G3 confermata a coeff. costanti:** identità dei moltiplicatori (s3 b1–b3); somma di generatori via Chernoff (T-SG8); E_int bilineare con 2^N−1 termini contro O(N) nel log-simbolo.
- **Non commutante:** BCH al 2° ordine (s3 c1), Trotter con errore O(1/n) (s3 c2); convergenza per perturbazioni illimitate aperta (Q4).
- **Novità — E_int dal bordo:** su un intervallo con BC i termini a coeff. costanti non commutano (∂_x non preserva Dirichlet); su 𝕋 tutto commuta.
- **Novità — componenti mal poste:** un componente può essere mal posto anche se la somma è ben posta (+∂²−∂⁴); lo split moltiplicativo va enunciato per modi o in PW_A (Q9).
- **P3.2:** ⟨e†_m, E_int^{(1)}⟩ = Σ_n c_n ⟨e†_m, L_2 e_n⟩ (e^{λ_n t} − e^{λ_m t})/(λ_n − λ_m), con regole di selezione; dimostrato per L_2 limitato.
- **E_int nel risolvente:** R_{A+B} − R_A = R_A B R_{A+B} (P4.2).
- **Non-identificabilità da simmetria:** una simmetria commutante con u autovettore produce un annullatore extra (coerente con R7-L4).
- **Componenti non invarianti:** la nozione di componente cambia con coordinate e BC (Q5).

## 5. Stato
- Noto: tutti i teoremi della §2.
- Dimostrato qui: §3 punti 1–6 e le avvertenze della §4.
- Aperto: Q1 (H_{K1}∩H_{K2} = ambiguità di E_int?), Q2 (scelta di 𝓗 al Gate 1), Q3, Q4, Q5, Q6, Q7, Q9.
- Probabilmente falso: H1 nella forma L²(ℝ) per le classi esponenziali; commutatività dei termini a coeff. costanti su un intervallo con BC.

## 6. NEW-ROUTE (in inbox/central.md; registrate come RT-D1, RT-D2)
- (R-a) C1 come somma di RKHS di Green.
- (R-b) Identificabilità = osservabilità, tramite il gramiano temporale del semigruppo.
