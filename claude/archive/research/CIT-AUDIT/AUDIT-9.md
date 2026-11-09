# AUDIT-9 — CIT-AUDIT-9 (prima del Gate 9)

Data: 2026-10-27 · Agente: CIT-AUDIT-9 · Piano: `PLAN-9.md` · Modello: `AUDIT-8.md`.
Mandato: `GATE8.md` §5 («Prima del Gate 9: CIT su Oberst 1990/1993, Isakov 1993 al posto di Saut–Scheurer per VAR-L2, Andrianov–Sokolov 2003 / Sokolov 2008») e `research/DEVIL/ATTACK-8.md` O6.
Ambito: le fonti da cui dipendono le rivendicazioni di novità di Fase 8 (SYS-EX, SYS-N1, SYS-T0, SYS-EX-C, VAR-L0–L2, ENC-K1′, ENC-K1) e le voci PARZIALE di AUDIT-8 che sorreggono righe DIMOSTRATO o CON-FONTE citate in `ALGORITMO_ESTESO.md` (mappa in `PLAN-9.md` §3).

## 0. Metodo

- **Esiti e gradi di lettura** come in AUDIT-8 §0: VERIFICATO / DATI CORRETTI / CONTENUTO DIVERSO / NON TROVATO / PARZIALE; (primaria), (abstract), (secondaria), (memoria). La memoria non conta come verifica.
- **Metadati.** Crossref (`api.crossref.org/works/<DOI>`), OpenAlex, Semantic Scholar, API arXiv, indici dei capitoli dei libri ricavati dai DOI dei capitoli su Crossref.
- **Testi primari letti.**
  - Oberst 1990: scansione depositata dall'autore sul sito dell'Università di Innsbruck (`uibk.ac.at/mathematik/personal/oberst/oberst-actaapplmath-1990.pdf`), oggi rimossa dal sito e recuperata dall'istantanea Wayback del 2024-08-31 (175 pagine, immagini; letta pagina per pagina). Numerazione: la pagina stampata «− n −» è la pagina n + 1 del PDF. Le citazioni sotto usano la numerazione dell'autore «(§, n)» e la pagina stampata.
  - Oberst 1996 (Adv. Appl. Math. 17): scansione dell'autore, stessa provenienza, pp. 337–338.
  - Pommaret, arXiv:0902.2314v2; Andrianov–Sokolov, arXiv:hep-th/0301062v4; Sokolov, arXiv:0903.2835v1; Moan–Niesen, arXiv:math/0609198v2; Trefethen–Weideman, PDF dell'autore (`people.maths.ox.ac.uk/trefethen/sirev56-3_385.pdf`); Huang, arXiv:1707.08548v5; Bakalov–Horozov–Yakimov, arXiv:q-alg/9602011; Rapisarda–Antoulas 2016, eprint Southampton.
- **Non accessibili.** Oberst 1993 (Springer, accesso con login; OpenAlex e Unpaywall: `closed`, nessuna copia in archivi; non presente nell'archivio dell'autore). Isakov 1993 e Saut–Scheurer 1987 (Elsevier, open archive «bronze», ma ScienceDirect risponde 403 agli script e chiede un CAPTCHA nel browser: **non aggirato**). van der Put–Singer: trovata solo una copia su un mirror non autorizzato, **non usata**.
- **Regole.** Nessuno script `_vendor` eseguito. PDF e immagini solo nello scratchpad della sessione. Paywall, 403, CAPTCHA e login non valgono come conferma.

## 1. Tabella, priorità A (fonti delle rivendicazioni di novità)

| # | voce | usata in | esito | metadati verificati (fonte) | contenuto rispetto all'uso | correzione |
|---|---|---|---|---|---|---|
| C1 | Oberst, *Multidimensional constant linear systems* | SYS-EX Passo 3, SYS-EX-C, SYS-T1; CONV-Q17 | **VERIFICATO** (primaria, scansione d'autore) | Acta Appl. Math. 20(1–2) (1990) 1–175, DOI 10.1007/BF00046908 (Crossref) | (a) **(§2, 52) Lemma e definizione** (p. 31): A iniettivo è un *cogeneratore iniettivo grande* se ogni D-modulo f.g. si immerge in un prodotto finito A^k; basta verificarlo per i D/p, p primo. (b) **(§2, 54) Main Theorem** (p. 32): i moduli degli esempi (1.7), (1.13), (1.18), (1.22), (1.24) e le loro forme reali sono cogeneratori iniettivi grandi; «the proof of the large cogenerator property is new». (c) **(1.22)** (pp. 15–16): fra gli esempi ci sono 𝒟′(Ω) e 𝒟′^F(Ω) **per Ω aperto convesso** di ℝ^r. (d) **(§4, 32) Teorema** (p. 69): C^∞(ℝ^r) e 𝒟′(ℝ^r) sono iniettivi; «more generally the same is true for the spaces C^∞(Ω), 𝒟′(Ω) and 𝒟′^F(Ω) where Ω ⊂ ℝ^r is an open convex subset». Prova: Palamodov 1970, th. 1 p. 300, th. 2 p. 304, th. 3 p. 305; per Ω = ℝ^r, Ehrenpreis 1970 th. 5.11 p. 145, th. 5.14 p. 150, th. 5.20 p. 156. (e) **(§4, 36)** (p. 70): monomorfismi ℂ⟨t⟩ ≅ 𝒪(ℂ^r; exp) ⊂ 𝒪(ℂ^r) → C^∞(ℝ^r) ⊂ 𝒟′(ℝ^r); se ℂ⟨t⟩ è grande lo sono tutti i moduli di (35). (f) **(§4, 51) Lemma** (p. 73): μ(g) := ∫_{ℝ^r} φ(s) g(s) ds, φ funzione test reale, è un funzionale analitico 𝒪(ℂ^r)-linearmente indipendente; prova con Stone–Weierstrass e principio d'identità. (g) **(§4, 54) Teorema** (p. 73, «the main new result of this paragraph»): per ogni primo p di ℂ[s] esiste un'immersione ℂ[s]-lineare **ℂ[s]/p ↪ 𝒪(ℂ^r)′** (una sola copia). Prova (pp. 74–76): Nullstellensatz, X = V(p), normalizzazione di Noether (61), funzionale (51) trasportato da ℂ^d a X. | SYS: Oberst 1990 non è più «non letto»; citare (2.52), (2.54), (4.32), (4.54). La costruzione di SYS-EX Passi 1–2 (EX-L1, EX-L2) **segue lo stesso schema** di (4.51)–(4.66): va detto. CONV-Q17: la fonte cercata esiste (vedi D1). |
| C2 | Oberst, *On the minimal number of trajectories determining a multidimensional system* | SYS-EX, SYS-N1, SYS-T0 (prior art) | **PARZIALE** (abstract e bibliografia; testo pieno non accessibile) | MCSS 6(3) (1993) 264–288, DOI 10.1007/BF01211623 (Crossref, OpenAlex) | Il contenuto noto resta quello dell'abstract (AUDIT-8 A1): μ(S) determinato costruttivamente per sistemi EDP e alle differenze a coefficienti costanti; estende Heij (1D) e Zampieri (2D); μ(S) ≤ 1 ⟺ sistema principale di Macaulay. **Nuovo (Crossref, 28 riferimenti):** la bibliografia cita Oberst 1990, Heij 1992 (*Exact modelling and identifiability of linear systems*), Macaulay, Matlis, Malgrange, Palamodov, Ehrenpreis, Grauert–Remmert, EHV 1992; **nessun lavoro su aperti non convessi o su spazi di segnali non iniettivi.** Rapisarda–Antoulas (SIAM J. Control Optim. 2016, §6) lo citano «on identifiability of nD systems». | La lettura «criterio di identificazione» **non** è un delta: è già il quadro di Heij 1992 e di Oberst 1993. Testo pieno da leggere appena accessibile (biblioteca). |
| C3 | Pommaret, *Macaulay inverse systems revisited* | sostegno di SYS-EX, SYS-N1 | **VERIFICATO** (primaria) — **portata precisata** | arXiv:0902.2314v2 (2010) | **Thm 5.2.5** (p. 15): «When M is n-pure, the minimum number of generators of R is equal to the maximum number of isotypical components … that is max_{m∈max∩ass(M)} dim_{D/m} soc_m(M)». R è il sistema duale (sistema inverso di Macaulay); n-puro con n = numero di variabili significa lunghezza finita. Pommaret lo dice «straight consequence» di Kunz, IV §2, pp. 104–109, e Macaulay §82 (fine di p. 91). Il §5.3 avverte che, fuori dal caso n-puro, nel sistema *localizzato* possono servire due generatori anche senza primi associati massimali: è un'altra nozione di generatore, non quella in C^∞. | AUDIT-8 A1 e §3: «la formula max dim soc_m» vale **solo per M di lunghezza finita**. Non copre SYS-EX per M di dimensione positiva. |
| C4 | Isakov, *Carleman type estimates in an anisotropic case and applications* | VAR-L0, VAR-L1, VAR-L2 | **VERIFICATO** (secondaria; primaria non accessibile, CAPTCHA) | J. Differential Equations 105(2) (1993) 217–238, DOI 10.1006/jdeq.1993.1088 (Crossref, OpenAlex) | Secondaria: Huang, CPDE 46(7) (2021) 1372–1388 (arXiv:1707.08548v5), §1. **In dimensione spaziale n = 1** Isakov prova la continuazione unica locale attraverso un segmento parallelo all'asse dei tempi, per soluzioni H^{2m}_loc di operatori parabolici ∂_t + (−∂_x²)^m **e di tipo Schrödinger** i^{−1}∂_t + (−∂_x²)^m, con termini di ordine inferiore fino a 2m − 1 a coefficienti A(t, x) localmente limitati. Per m = 1 questo copre i∂_t u + ∂_x²u + b u_x + c u = 0 con b, c ∈ L^∞_loc(t, x). In n > 1, per Schrödinger, solo un risultato più debole. | VAR-L1: con y = x − g(t) l'operatore acquista il termine −i g′(t)∂_y, del primo ordine a coefficiente limitato, ammesso da Isakov; quindi **anche VAR-L1 su un grafico x = g(t) rientra nel caso n = 1 di Isakov**. VAR-L2 segue iterando. Stato: VAR-L0–L2 **NOTI** (fonte secondaria), prove del progetto autosufficienti. |
| C5 | Saut, Scheurer, *Unique continuation for some evolution equations* | VAR l.75 (storico); ATTACK-8 O6 | **VERIFICATO** (secondaria) — **non serve** | J. Differential Equations 66(1) (1987) 118–139, DOI 10.1016/0022-0396(87)90043-X (Crossref) | Huang, §1 e §5: Saut–Scheurer trattano il caso **parabolico** del 2° ordine (componente orizzontale), migliorato da Isakov; lo affermano anche per ordine superiore, ma secondo Huang i dettagli non sono completi. **Nessun claim del progetto dipende da Saut–Scheurer.** | VAR: già tolto per VAR-L2 (post-Gate 8). ATTACK-8 O6: «VAR-L1 e L2: Saut–Scheurer 1987» → «Isakov 1993 (n = 1)». Può restare solo come contesto storico. |
| C6 | Andrianov, Sokolov, *Nonlinear supersymmetry in quantum mechanics: algebraic properties and differential representation* | ENC-K1′ (prior art) | **VERIFICATO** (primaria) | Nucl. Phys. B 660(1–2) (2003) 25–50, DOI 10.1016/S0550-3213(03)00232-3 (Crossref); arXiv:hep-th/0301062v4 | §1, eq. (2), (6): operatori di intrecciamento h⁺q⁺ = q⁺h⁻ con h^± = −∂² + V^±, q^±_N = Σ w_k^± ∂^k, **coefficienti complessi e sufficientemente lisci**, w_N costante. §2, **Lemma** (pp. 6–8): esistono operatori del primo ordine r_l = ∂ + χ_l(x), «where the functions χ_l(x) may be complex and/or singular at some points», con q_N = r_1 ⋯ r_N, Hamiltoniani intermedi di Schrödinger (potenziali complessi e/o singolari) e intrecci h_{l−1} r_l = r_l h_l. Prova: forma di Jordan della matrice di h sullo spazio dei modi nulli e ricorsione sull'ordine, cioè lo schema di ENC-K1′(iii). Il §2 è enunciato con la simmetria per trasposizione q⁻ = (q⁺)^t; per operatori di Schrödinger è automatica: trasponendo W L_q = (L_0 + c)W si ottiene L_q W^t = W^t(L_0 + c). | ENC-K1′: «probabilmente noto» → **NOTO** (Andrianov–Sokolov 2003, §2, Lemma). Vedi §3. |
| C7 | Sokolov, *Factorization of nonlinear supersymmetry in one-dimensional quantum mechanics. II: proofs of theorems on reducibility* | ENC-K1′ (contesto) | **VERIFICATO** (primaria) | J. Math. Sci. 151(2) (2008) 2924–2936, DOI 10.1007/s10958-008-9009-3 (Crossref); arXiv:0903.2835v1 | Classe K di potenziali **reali** con condizioni all'infinito. Teoremi 2 e 3: fattorizzazione dell'intertwiner, eventualmente moltiplicato per un polinomio in H, in blocchi **reali non singolari** del primo ordine o in blocchi irriducibili del secondo ordine. Ipotesi più forti e conclusione più forte del caso locale complesso di ENC-K1′. La parte I è Andrianov–Sokolov, J. Math. Sci. 143(1) (2007) 2707. | ENC: citare come «versione reale non singolare». |
| C8 | Wilson, *Bispectral commutative ordinary differential operators* | ENC-K1 | **VERIFICATO** (metadati; contenuto da secondaria) | J. reine angew. Math. 442 (1993) 177–204, DOI 10.1515/crll.1993.442.177 (Crossref) | Bakalov–Horozov–Yakimov (arXiv:q-alg/9602011, introduzione): Wilson trova tutte le algebre bispettrali massimali di rango 1 tramite piani della Grassmanniana di Sato (adelica). La lista di Duistermaat–Grünbaum contiene, in rango 1, i potenziali ottenuti da u = 0 con un numero finito di trasformazioni di Darboux razionali (0.5) (soluzioni razionali di KdV, Adler–Moser). | ENC-K1 resta **CON-FONTE (secondaria)**. Va dichiarato che l'enunciato «∃ W differenziale con W L_V = L_0 W ⟺ V Darboux iterato di 0» è la **composizione** di ENC-K1′ con la lista (0.5) di D–G e con Wilson 1993, non un enunciato letterale di una delle due fonti. |

## 2. Voci PARZIALE di AUDIT-8 che sorreggono righe di `ALGORITMO_ESTESO.md` (priorità B)

| # | voce AUDIT-8 | riga sorretta (stato in ALGORITMO_ESTESO) | esito F9 | fonte | nota e correzione |
|---|---|---|---|---|---|
| D1 | B2: iniettività di 𝒟′(Ω), Ω convesso | CONV-Q17 (caso escluso) | **VERIFICATO** (primaria, Oberst 1990) | Oberst 1990 (§4, 32), p. 69, che rinvia a Palamodov 1970 th. 1–3, pp. 300–305 (Palamodov non letto) | AUDIT-8 B2 diceva «nessuna fonte trovata»: **superato**. C^∞(Ω), 𝒟′(Ω) e 𝒟′^F(Ω) sono iniettivi per Ω aperto convesso. CONV-Q17 può reintegrare il caso come CON-FONTE. |
| D2 | B26: Moan–Niesen, Thm 3 | CONV-T7, contratto (B); VAR-T10(4) (DIMOSTRATO) | **VERIFICATO** (primaria) | Found. Comput. Math. 8(3) (2008) 291–301, DOI 10.1007/s10208-007-9010-0 (Crossref); arXiv:math/0609198v2 | «Let A(t) be a real integrable matrix … If ∫_0^t ‖A(τ)‖_2 dτ < π, then the Magnus series converges and its sum Ω(t) satisfies e^{Ω(t)} = Y(t).» Il testo di CONV l.297 («per matrici reali») è corretto. ALGORITMO_ESTESO l.214 dice «Moan–Niesen» senza «reali»: aggiungerlo. |
| D3 | B17: Trefethen–Weideman, Thm 5.1 | DICT-U3d(iii) (DIMOSTRATO) | **VERIFICATO** (primaria) | SIAM Rev. 56(3) (2014) 385–458, DOI 10.1137/130932132; PDF dell'autore | Thm 5.1: w analitica in |Im x| < a, w → 0 uniformemente per |x| → ∞ nella striscia, ∫|w(x + ib)|dx ≤ M per ogni b ∈ (−a, a) ⇒ |I_h − I| ≤ 2M/(e^{2πa/h} − 1). L'uso in DICT l.100 è corretto: con G(σ) = exp(−e^σ + βσ), β > 0 e 0 < a < π/2, si ha sup_{|b|<a} ∫|G(x + ib)|dx = Γ(β)(cos a)^{−β} e il decadimento uniforme vale; la griglia traslata si ottiene applicando il teorema a G(· + c). Togliere «CON-FONTE non letta». |
| D4 | B29: Engel–Nagel III.1 | CONV-T7, contratto (B) (Dyson–Phillips) | **PARZIALE** (secondaria, frammento) | Engel, Nagel, GTM 194 (2000), DOI 10.1007/b97696 | Una fonte terza (Results Math., DOI 10.1007/s00025-021-01353-1, frammento indicizzato) cita «III.1.3» per il teorema di perturbazione limitata e «III.1.10» per la formula di Dyson–Phillips. Da confermare sul testo. CONV l.297: «Engel–Nagel III.1.3 e III.1.10 (secondaria)». |
| D5 | B4: Pazy cap. 5 | VAR-P11(e), VAR-L2-cor (CON-FONTE) | **PARZIALE** (metadati del capitolo) | Pazy 1983, cap. 5 «Evolution Equations», pp. 126–182, DOI 10.1007/978-1-4612-5561-1_5 (Crossref) | Il capitolo esiste ed è quello giusto per sistemi di evoluzione; il numero del teorema (A_0 + B(t), B ∈ C¹ in norma ⇒ soluzione classica) non è stato letto. Lasciare «Pazy, cap. 5» **senza** «Thm 5.2.?». Lo stato CON-FONTE di VAR-P11(e) e VAR-L2-cor resta. |
| D6 | B6: van der Put–Singer 1.27 / 1.34 | VAR-T6 (CON-FONTE) | **PARZIALE** (memoria) | — | Nessuna copia autorizzata letta. VAR-T6: citare «van der Put–Singer 2003, cap. 1 (corrispondenza di Galois di Picard–Vessiot)» **senza numeri**. |
| D7 | B5: Folland, cap. 4 | VAR-T10(3) (DIMOSTRATO, parte metaplettica) | **DATI CORRETTI** (indice dei capitoli) | Folland, *Harmonic Analysis in Phase Space*, Ann. of Math. Stud. 122 (1989), DOI 10.1515/9781400882427; capitoli da Crossref | Cap. 1 «The Heisenberg group and its representations» (pp. 9–77); cap. 4 «The metaplectic representation» (pp. 170–222). Stone–von Neumann è nel cap. 1 (numero di paragrafo da memoria), la rappresentazione metaplettica nel cap. 4. VAR l.225–226: «Folland 1989, cap. 1 (Stone–von Neumann), cap. 4 (metaplettica)». |
| D8 | B24: Thaller, cap. 5 | FW-1 con V (CON-FONTE) | **DATI CORRETTI** (indice dei capitoli; paragrafo non letto) | Thaller, *The Dirac Equation*, Springer 1992, DOI 10.1007/978-3-662-02753-0; cap. 5 «Supersymmetry», pp. 138–175; cap. 6 «The Nonrelativistic Limit», pp. 176–192 (Crossref) | Il cap. 5 è quello sulla supersimmetria, dove si trova la trasformazione di Foldy–Wouthuysen esatta in forma astratta; il paragrafo non è stato letto. Fonte originale della trasformazione esatta Λ = sign(H): Eriksen, Phys. Rev. 111(3) (1958) 1011–1016, DOI 10.1103/PhysRev.111.1011 (metadati). FW-1 con V resta CON-FONTE: citare «Thaller 1992, cap. 5 (Supersymmetry); Eriksen 1958». |
| D9 | B12: Niederer 1973 | ENC-P0′-DIC (lente; forma esistenziale DIMOSTRATO) | **DATI CORRETTI** (secondaria) | *The maximal kinematical invariance group of the harmonic oscillator*, Helv. Phys. Acta 46 (1973) 191–200; nessun DOI | Due secondarie (arXiv:1111.5569; arXiv:1706.04555). La seconda scrive «47 (1973)», ma il vol. 47 è del 1974 (Boyer, Helv. Phys. Acta 47 (1974)): vale 46. Aggiungere titolo e pagine. La forma esistenziale è sorretta da Bluman–Shtelen 1996 (AUDIT-8 A16), non da Niederer. |
| D10 | A15: Marchenko cap. 1 | ENC-1 (DIMOSTRATO, prova propria) | **PARZIALE** (invariato) | — | Citazione di solo confronto; nessuna azione. |
| D11 | B8: Matsumura §18 | SYS-L1 (μ_p = numero di Bass, osservazione non usata) | **PARZIALE** (invariato) | — | Nessuna riga dipende dal numero. |
| D12 | A2: Oberst 1990 | SYS-EX Passo 3 | **VERIFICATO** (vedi C1) | — | Chiuso da C1. |
| D13 | A8: Saut–Scheurer | VAR-L2 | **VERIFICATO** (secondaria; non serve) | — | Chiuso da C5. |

Fuori ambito, perché nessuna riga DIMOSTRATO o CON-FONTE di ALGORITMO_ESTESO ne dipende: A21 (Dang–Einkemmer–Ostermann, CONV-Q6′ aperto), A22 (Ax, DICT-AX non in ALGORITMO_ESTESO), B30 (Nečas/Grisvard, uso generico), B31 (Hörmander III 18.1.13, solo in AUDIT_S8-DICT), B32 (Kato, osservazione in ENC l.216).

**Fonti nuove usate in F9** (in coda al bib, `% F9`): Oberst 1996 (Adv. Appl. Math. 17(3) 337–356, DOI 10.1006/aama.1996.0014; primaria pp. 337–338: per un sistema con M di dimensione finita, Sol è somma diretta di esponenziali-polinomi; è il contesto di SYS-R1); Heij 1992 (Automatica 28(2) 325–344, DOI 10.1016/0005-1098(92)90119-Z; metadati); Huang 2021; Eriksen 1958; Thaller 1992; Niederer 1973; Rapisarda–Antoulas 2016 (DOI 10.1137/15M1031837).

## 3. Verdetto di novità

### 3.1 SYS-EX, SYS-N1, SYS-T0 (con SYS-EX-C)

**Che cosa è già in letteratura (letto o confermato).**
1. *Quadro.* Oberst 1990 (C1): C^∞(Ω) e 𝒟′(Ω), per Ω = ℝ^n **e per Ω aperto convesso**, sono iniettivi (4.32) e cogeneratori iniettivi grandi (2.54), (1.22), (4.36). Ogni modulo f.g. si immerge in un prodotto finito A^k.
2. *Una copia per ogni primo.* Oberst 1990 (4.54): ℂ[s]/p ↪ 𝒪(ℂ^n)′ ≅ ℂ⟨t⟩ ⊂ C^∞(ℝ^n). La costruzione usa la normalizzazione di Noether, un funzionale integrato sul dominio reale, Stone–Weierstrass e il principio d'identità: **sono gli ingredienti di EX-L1, EX-L2 e dei Passi 1–2 di SYS-EX.**
3. *Numero minimo di traiettorie.* Oberst 1993 (abstract): μ(S) determinato costruttivamente; μ(S) ≤ 1 ⟺ sistema principale di Macaulay; esteso da Heij (n = 1, «identifiability») e Zampieri (2D). Il lavoro è letto in letteratura come risultato sull'identificabilità (Rapisarda–Antoulas 2016).
4. *Lunghezza finita.* Pommaret 2010, Thm 5.2.5 (con Macaulay §82 e Kunz IV §2): per M n-puro il numero minimo di generatori del sistema duale è max_m dim soc_m(M).

**Che cosa non risulta in nessuna fonte letta.** Il criterio su un aperto connesso Ω **su cui C^∞(Ω) (risp. 𝒟′(Ω)) non è iniettivo**, per esempio un Ω non P-convesso (§3.3 di S8-SYS). Lì il quadro di Oberst, che presuppone un modulo di segnali iniettivo, non si applica. La bibliografia di Oberst 1993 non contiene lavori su aperti non convessi. Il meccanismo della prova di S8-SYS è: immersione in C^∞(ℝ^n), un sottomodulo essenziale mandato in funzioni intere (restrizione a Ω iniettiva per analiticità), SYS-L0. È elementare una volta noti (2) e il caso ℝ^n.

**Verdetti.**

| claim | caso | verdetto | motivo |
|---|---|---|---|
| SYS-EX | Ω = ℝ^n | **NOTO** | Oberst 1993 (abstract), con 1990 (2.54), (4.54) |
| SYS-EX | Ω convesso | **PROBABILMENTE NOTO** | Oberst 1990 dà i cogeneratori grandi su Ω convesso. Se Oberst 1993 enuncia μ(S) per un cogeneratore grande qualsiasi (probabile, non verificato), il caso convesso è incluso. |
| SYS-EX | Ω connesso con C^∞(Ω) non iniettivo | **DELTA (estensione)**, rischio residuo basso–medio | Non trovato. Il rischio dipende solo dal testo pieno di Oberst 1993, non letto. |
| SYS-EX-C | Ω convesso: μ_p(C^∞(Ω)) = ∞ per p non massimale, μ_m = 1 | **PROBABILMENTE NOTO** | È ciò che serve per «zoccoli ≤ 1 ⇒ μ(S) ≤ 1» su un cogeneratore grande; Oberst 1990 dà solo una copia per primo (4.54); l'abstract di Oberst 1993 («molti sistemi grandi sono principali») lo suggerisce. |
| SYS-N1 | ogni Ω connesso | **NOTO / folklore** | Su ℝ^n è la direzione facile di Oberst 1993. Su Ω connesso qualsiasi è un argomento di una riga (soc_m ↦ ℂe^{λ·x}). È parte del delta solo come metà dell'equivalenza su Ω non iniettivo. |
| SYS-T0 | n = 1 | **NOTO** | Heij 1992; Oberst 1993 lo estende. Nessun delta (in n = 1 ogni aperto connesso è un intervallo, su cui C^∞ è iniettivo). |
| costruzione con funzioni intere | — | **NON è un delta** | Oberst 1990 (4.51)–(4.66). AUDIT-8 §3 punto (ii) va ritirato. |
| lettura come criterio di identificazione | — | **NON è un delta** | Heij 1992; Oberst 1993 letto come identificabilità. AUDIT-8 §3 punto (iii) va ritirato. |

**Formulazione esatta da dichiarare nel paper** (italiano; da tradurre senza cambiare la portata):

> «Per Ω = ℝ^n il criterio "esiste una traiettoria u con Ann(u) = U_P se e solo se dim_ℂ soc_m(M_P) ≤ 1 per ogni ideale massimale m" è dovuto a Oberst [Ob93], nel quadro dei cogeneratori iniettivi grandi di [Ob90], che comprende anche gli aperti convessi [Ob90, (4.32)]. Per M_P di lunghezza finita è il criterio classico di Macaulay sui sistemi principali [Mac16, §82; Pom10, Thm 5.2.5]; in una variabile è dovuto a Heij [He92]. Osserviamo che il criterio resta valido su ogni aperto connesso non vuoto Ω ⊂ ℝ^n, anche quando C^∞(Ω) e 𝒟′(Ω) non sono moduli iniettivi e il quadro di [Ob90] non si applica. La prova combina le immersioni R/p ↪ {funzioni intere} di [Ob90, (4.54)] con un argomento di sottomodulo essenziale (Prop. …).»

Nel paper la frase va presentata come **osservazione o proposizione di estensione**, non come teorema nuovo. Va aggiunta la riserva «[Ob93] non è stato consultato in testo integrale» finché non lo è.

### 3.2 ENC-K1′

**Già in letteratura (letto in primaria).** Andrianov–Sokolov 2003, §2, Lemma (C6): un intertwiner differenziale di ordine N fra due operatori di Schrödinger, con coefficienti complessi lisci e coefficiente di testa costante, si fattorizza in N operatori del primo ordine ∂ + χ_l, con χ_l eventualmente complessi e singolari in alcuni punti, con Hamiltoniani intermedi di Schrödinger e intrecci a catena. La prova è la stessa di ENC-K1′(iii): autovettore di h sul nucleo, divisione per il fattore del primo ordine, induzione. La versione con blocchi reali non singolari è Sokolov 2008 (C7). Il viceversa è Crum 1955.

**Confronto punto per punto.**

| parte di ENC-K1′ | in AS03? |
|---|---|
| (i) w_n costante | **assunto** in AS03, eq. (6). In ENC-K1′ è dedotto, ma è il calcolo standard del coefficiente di ∂^{n+1}: non è un delta. |
| (ii) ker W di dimensione n, invariante per L_q | sì: AS03 eq. (16), matrice di h sui modi nulli |
| (iii) W = w_n A_n ⋯ A_1, catena di Darboux | sì: AS03 §2, Lemma, con h⁺ = −∂² + c come caso particolare |
| descrizione di Z (chiuso, numerabile; discretezza aperta, Q7) | AS03 dice solo «singular at some points». È una precisazione tecnica, non un risultato. |
| viceversa (Crum) | Crum 1955 |

**Verdetto: NOTO.** Nessun delta da rivendicare. Lo stato in LEDGER deve passare da «DIMOSTRATO, probabilmente noto» a «DIMOSTRATO; NOTO (Andrianov–Sokolov 2003, §2, Lemma)». ALGORITMO_ESTESO dice già «nessuna novità»: va aggiunta solo la citazione.

**Formulazione da dichiarare nel paper:**

> «La fattorizzazione di un operatore di intrecciamento differenziale fra due operatori di Schrödinger in una catena di trasformazioni di Darboux del primo ordine, con coefficienti eventualmente complessi e singolari, è dovuta ad Andrianov e Sokolov [AS03, §2, Lemma]; la versione con blocchi reali non singolari è in [Sok08]; il viceversa è il teorema di Crum [Cr55]. Ne usiamo il caso h₊ = −∂² + c. La nostra sola precisazione è che l'insieme eccezionale Z su cui la catena non è definita è chiuso e numerabile.»

### 3.3 Effetto su O6 (DEVIL-8) e su G★″

- O6 chiede di dichiarare in G★″ la **composizione** L6–L10 e le negative nuove. AUDIT-9 conferma la richiesta. Fra i lemmi positivi di F8 esaminati qui, l'unico candidato delta resta **SYS-EX su Ω non iniettivo**, come estensione.
- VAR-L0–L2: NOTI (Isakov 1993, n = 1, fonte secondaria). Non lo è nemmeno VAR-L1 su grafico (C4).
- ENC-K1′: NOTO. ENC-K1: CON-FONTE (composizione dichiarata, C8).

## 4. Esiti riassuntivi

Voci contate: 21 (C1–C8, D1–D13).

| esito | n. |
|---|---|
| VERIFICATO | 12 (C1, C3, C4, C5, C6, C7, C8, D1, D2, D3, D12, D13) |
| DATI CORRETTI | 3 (D7, D8, D9) |
| CONTENUTO DIVERSO | 0 |
| NON TROVATO | 0 |
| PARZIALE | 6 (C2, D4, D5, D6, D10, D11) |

- **Passano da PARZIALE (AUDIT-8) a VERIFICATO:** A2 Oberst 1990, B2 (𝒟′(Ω) convesso), B17 Trefethen–Weideman Thm 5.1, B26 Moan–Niesen Thm 3, A8 Saut–Scheurer (come «non serve»).
- **Passano da PARZIALE a DATI CORRETTI:** B5 Folland, B12 Niederer, B24 Thaller.
- **Portata ridotta:** Pommaret Thm 5.2.5 vale solo per lunghezza finita (C3).
- **Nessun CONTENUTO DIVERSO.** Il punto più vicino: AUDIT-8 §3 elencava come delta di SYS-EX la «costruzione esplicita» e la «lettura come criterio di identificazione», che sono in Oberst 1990 e in Heij 1992 / Oberst 1993.

## 5. Correzioni per file e claim

**`work/S8-SYS/PROOF_PACKAGE.md`**
1. §1, paragrafo «Confronto con Oberst, Acta Appl. Math. 20 (1990)»: «Il testo è a pagamento e non l'ho letto» → «letto da CIT-AUDIT-9 (scansione dell'autore): (2.52) definizione di cogeneratore iniettivo grande; (2.54) teorema principale; (4.32) iniettività di C^∞(Ω), 𝒟′(Ω), 𝒟′^F(Ω) per Ω aperto convesso (Palamodov 1970, th. 1–3, pp. 300–305); (4.54) ℂ[s]/p ↪ 𝒪(ℂ^n)′».
2. §1, «Riclassificazione post-Gate 8», punto Pommaret: aggiungere «per M di lunghezza finita (n-puro)»; il §5.3 di Pommaret usa un'altra nozione di generatore.
3. §1, «Delta dichiarato (unico)»: «Ω arbitrario, anche non P-convesso» → «Ω connesso su cui C^∞(Ω) (risp. 𝒟′(Ω)) non è iniettivo. Per Ω convesso il caso è probabilmente coperto da Oberst 1990 (4.32) + Oberst 1993». Usare la frase di §3.1.
4. §2, Passo 1 / EX-L2: aggiungere «lo schema (normalizzazione di Noether, funzionale integrato sul dominio reale, Stone–Weierstrass, principio d'identità) è quello di Oberst 1990, (4.51)–(4.66)».
5. §2, Passo 3: «Oberst 1990, citato senza aver letto le pagine pertinenti» → «Oberst 1990 (4.32), p. 69; Ehrenpreis 1970 th. 5.20 p. 156 (via Oberst)».
6. Oss. 2 (SYS-EX-C): aggiungere «su Ω convesso probabilmente in Oberst 1993 (non letto)».
7. SYS-T0: aggiungere Heij, Automatica 28(2) (1992) 325–344, DOI 10.1016/0005-1098(92)90119-Z.

**`work/S8-SYS/LEDGER_ROWS.md`**
- SYS-EX: stato «delta unico: Ω arbitrario» → «delta: Ω connesso con C^∞(Ω) non iniettivo (estensione); Ω convesso probabilmente noto (Oberst 1990 (4.32) + 1993)». Dipendenza «iniettività di C^∞(ℝ^n) (CON-FONTE: Malgrange 1962–63; Oberst 1990 non letto)» → «(Oberst 1990 (4.32), letto CIT-AUDIT-9; Malgrange 1962–63)».
- SYS-N1: «DIMOSTRATO (elementare, parte del delta di SYS-EX)» → aggiungere «NOTO/folklore come enunciato a sé».
- SYS-T0: aggiungere Heij 1992.
- SYS-EX-C: aggiungere «su Ω convesso probabilmente noto (Oberst 1993)».

**`work/S8-VAR/PROOF_PACKAGE.md` e `LEDGER_ROWS.md`**
1. l.75 «Letteratura»: «con ogni probabilità contiene VAR-L2» → «Isakov 1993, n = 1: continuazione unica attraverso x = cost. per Schrödinger con termini di ordine ≤ 1 localmente limitati (secondaria: Huang, CPDE 46 (2021) 1372–1388, §1); con y = x − g(t) copre anche VAR-L1». Stato di priorità: PROBABILMENTE NOTO → **NOTO (secondaria)**.
2. LEDGER VAR-L1 «quasi certamente noto» e VAR-L2 «PROBABILMENTE NOTO» → «NOTO (Isakov 1993, n = 1; secondaria)». Lo stato DIMOSTRATO della prova propria non cambia.
3. l.147 e LEDGER VAR-T6: «Prop. 1.34 / Thm 1.27 — numero da verificare» → «van der Put–Singer 2003, cap. 1» senza numeri.
4. l.215 VAR-P11(e): «Thm 5.2.?» → togliere; «Pazy 1983, cap. 5 (Evolution Equations)».
5. l.225–226 (VAR-T10(3)): Folland → «cap. 1 (Stone–von Neumann), cap. 4 (rappresentazione metaplettica)».
6. l.324, lista dei numeri non verificati: togliere Folland (capitolo corretto) e Moan–Niesen Thm 3 (verificato); restano vdPS e Pazy cap. 5.

**`work/S8-CONV/PROOF_PACKAGE.md`**
1. l.217 (CONV-Q17): l'iniettività di 𝒟′(Ω) per Ω convesso è Oberst 1990 (4.32) (Palamodov th. 2 p. 304). Il caso escluso può rientrare come CON-FONTE.
2. l.297: «Engel–Nagel III.1, numero da verificare» → «Engel–Nagel III.1.3 (perturbazione limitata), III.1.10 (Dyson–Phillips), secondaria». Moan–Niesen: aggiungere FoCM 8(3) 291–301, DOI 10.1007/s10208-007-9010-0.

**`work/S8-ENC/PROOF_PACKAGE.rev2.md` e `LEDGER_ROWS.rev2.md`**
1. l.382, «Nota sulla priorità»: «l'enunciato non è stato letto. ENC-K1′ è quasi certamente noto» → «letto da CIT-AUDIT-9: Andrianov–Sokolov 2003, §2, Lemma (coefficienti complessi, singolarità puntuali ammesse); versione reale non singolare in Sokolov 2008, J. Math. Sci. 151(2) 2924–2936. ENC-K1′ è NOTO; la sola precisazione propria è la descrizione di Z».
2. LEDGER ENC-K1′ (rev2 l.34): «probabilmente noto (Andrianov–Sokolov 2003)» → «NOTO (Andrianov–Sokolov 2003, §2, Lemma)».
3. l.384 ENC-K1: «Wilson 1998 per la grassmanniana adelica» → «Wilson 1993 (J. reine angew. Math. 442, 177–204) per le algebre bispettrali di rango 1; l'enunciato con l'intertwiner è la composizione di ENC-K1′ con la lista di Duistermaat–Grünbaum». Già chiesto da AUDIT-8 A14 e non ancora applicato nel rev2.
4. l.525 FW-1: «Thaller 1992 cap. 5, da verificare» → «Thaller 1992, cap. 5 (Supersymmetry, pp. 138–175; paragrafo non letto); Eriksen, Phys. Rev. 111 (1958) 1011–1016».
5. l.290 (lente): Niederer → «Helv. Phys. Acta 46 (1973) 191–200».

**`work/S8-DICT/PROOF_PACKAGE.md` e `LEDGER_ROWS.md`**
- l.100 e LEDGER DICT-U3d: «CON-FONTE non letta» → «Trefethen–Weideman 2014, Thm 5.1, verificato (CIT-AUDIT-9): ipotesi soddisfatte con 0 < a < π/2, M(a) = Γ(β)(cos a)^{−β}».

**`ALGORITMO_ESTESO.md`** (proposte per chi ne ha la scrittura)
- l.131: «noto su ℝ^n, Oberst 1993; delta dichiarato solo per Ω arbitrario» → «noto su ℝ^n (Oberst 1993) e probabilmente su Ω convesso (Oberst 1990 (4.32)); delta solo per Ω connesso con C^∞(Ω) non iniettivo».
- l.142: «VAR-L2 DIMOSTRATO (continuazione unica)» → aggiungere «(NOTO: Isakov 1993)».
- l.173: «ENC-K1′ DIMOSTRATO (… nessuna novità)» → aggiungere «(Andrianov–Sokolov 2003, §2)».
- l.214: «Moan–Niesen» → «Moan–Niesen, Thm 3 (matrici reali)».

**`research/CIT-AUDIT/AUDIT-8.md`** (errata, non modificato)
- A1 e §3: la formula max dim soc_m di Pommaret vale solo per lunghezza finita.
- A2: superato (VERIFICATO, primaria). B2: superato (D1). B5, B12, B24: DATI CORRETTI. B17, B26: VERIFICATO.
- §3, riga SYS-EX: ritirare (ii) «costruzione esplicita» e (iii) «lettura come criterio di identificazione» dal delta.
- §3, riga VAR-L0–L2: VAR-L1 su grafico rientra in Isakov n = 1 dopo il cambio di variabile.

**`research/DEVIL/ATTACK-8.md` O6** (per il coordinatore)
- «VAR-L1 e L2: Saut–Scheurer 1987» → «Isakov 1993 (n = 1)». «ENC-K1′: probabilmente Andrianov–Sokolov 2003» → «Andrianov–Sokolov 2003, §2, Lemma (letto)».

**`GATE8.md` §5** (per il coordinatore): la voce «Prima del Gate 9: CIT su Oberst 1990/1993, Isakov 1993, Andrianov–Sokolov» è eseguita. Oberst 1990, Andrianov–Sokolov e Sokolov sono letti in primaria; Oberst 1993 solo nell'abstract (testo non accessibile); Isakov solo in secondaria (CAPTCHA non aggirato).

## 6. Provenienza (accesso 2026-10-27)

- Crossref `api.crossref.org/works/<DOI>`: 10.1007/BF00046908, 10.1007/BF01211623 (con lista dei riferimenti), 10.1006/jdeq.1993.1088, 10.1016/0022-0396(87)90043-X, 10.1016/S0550-3213(03)00232-3, 10.1007/s10958-008-9009-3, 10.1515/crll.1993.442.177, 10.1007/s10208-007-9010-0, 10.1103/PhysRev.111.1011, 10.1080/03605302.2021.1881110, 10.1006/aama.1996.0014, 10.1016/0005-1098(92)90119-Z; capitoli 10.1007/978-3-662-02753-0_1…_10 (Thaller), 10.1007/978-1-4612-5561-1_1…_8 (Pazy), 10.1515/9781400882427-001…-009 (Folland).
- OpenAlex e Semantic Scholar: stato di accesso di Oberst 1993 (closed, abstract eliso dall'editore) e lavori che lo citano.
- Wayback Machine: `web.archive.org/web/20240831180331id_/https://www.uibk.ac.at/mathematik/personal/oberst/oberst-actaapplmath-1990.pdf` (scansione d'autore, 12,7 MB); `…/oberst_1996.pdf`.
- arXiv: 0902.2314v2, hep-th/0301062v4, 0903.2835v1, math/0609198v2, 1707.08548v5, q-alg/9602011, 1111.5569, 1706.04555. Eprint Southampton 399367 (Rapisarda–Antoulas).
- PDF dell'autore: `people.maths.ox.ac.uk/trefethen/sirev56-3_385.pdf`.
- Non usati: ScienceDirect (403 e CAPTCHA), API Elsevier (accesso negato), mirror non autorizzato di van der Put–Singer.
- Tutti i file scaricati sono solo nello scratchpad della sessione.
