# VERDETTO — F6-HOR (revisione delle strade parcheggiate + non-seme) · 26/10/2026
Criteri fissati prima della ricerca: PLAN.md §2. Dettaglio, motivazioni e prove: NOTE.md. SymPy (solo verifica): sympy/hor1–hor4 (.py/.out), esiti al §4. Stati: candidato / prova scritta / V-ex / CON-FONTE (da verificare). **Nulla è DIMOSTRATO.**
Skill caricate (lettura di SKILL.md): session-protocol, route-scout, claim-lifecycle, novelty-check (fasi A–B; fase C = REVIEW_UNAVAILABLE, niente Codex), math-skill (modo proof), scientific-critical-thinking. Ricerca con WebSearch diretto; nessuno script _vendor eseguito; niente ML.
Canale: inbox/central-F6.md (per AVVISO del coordinatore; nessuna scrittura in central.md).

## 1. Tre fatti trasversali (NOTE §1)
- **O-H1 (→ F6-VAR, F6-DICT):** con V(t,x) libero ogni u ≠ 0 risolve L₀u + Vu = i u_t per ogni L₀ (prova scritta, una riga): **nessuna identificazione di L₀ senza vincoli di classe su V** (ostruzione di tipo N1). Con V = V(x) la condizione u(i u_tt − L₀u_t) − u_t(i u_t − L₀u) = 0 è **lineare in L₀** ⇒ test di tipo Gram (candidato HOR-P1, V-ex su Pöschl–Teller con 2 modi: soluzione unica L₀ = −∂²). **HOR-O1 (prova scritta + V-ex):** gli stati stazionari non identificano mai L₀ con V(x) libero.
- **O-H2 (→ F6-ENC):** "rimuovere V" ha tre livelli di encoder con criteri di esistenza: **puntuale** ⟺ V quadratico in x (Niederer, Boyer, Bluman; CON-FONTE da verificare), **differenziale** (Darboux/Crum) ⟺ V razionale con monodromia banale (Adler–Moser, Duistermaat–Grünbaum 1986; test di Galois/Kovacic), **integrale** (GLM, seme) per V decrescente generico.
- **O-H3 (→ F6-DICT):** sine-Gordon e e^u diventano polinomiali con w = e^{iu} (2(w w_xt − w_x w_t) = w³ − w, V-ex): i dizionari non polinomiali con F(u) soluzione di un'ODE algebrica entrano nel quadro di F4-ALG; lo strumento per il grado di trascendenza è Ax (1971).

## 2. Tabella delle strade parcheggiate / sospese / eliminate
| strada (stato prima) | trigger scattato? | decisione | destinatario | I / S / E (regola 3) |
|---|---|---|---|---|
| RT-5 tensore simbolo (parcheggiata) | sì (P-A, gauge) | **RIAPRI**: simbolo principale = strato invariante di gauge; varietà caratteristica V(Fitt₀) non distingue Dirac da KG⊗I | F6-SYS | parziale / parziale / no |
| RT-S1e RIGID (parcheggiata fino a L1/L4) | sì (P-B, potenziali singolari fuchsiani) | **RIAPRI**: V identificato dagli esponenti locali per operatori rigidi | F6-VAR | sì (rigidi) / settoriale / no |
| RT-S1f STOKES (parcheggiata fino a L1) | sì (V illimitati: x², Coulomb) | **RIAPRI fusa con RIGID**, priorità bassa | F6-VAR | parziale / settoriale / Stokes |
| RT-R1b positività (parcheggiata) | no | **RESTA PARCHEGGIATA** | — | — |
| RT-S2d Mori–Zwanzig (parcheggiata) | sì (C2 località; V come rumore) | **RIAPRI**: componente di un sistema locale ⇒ memoria; criterio C2 candidato | F6-CONV (+nota F6-ENC) | no / sì / sì (memoria) |
| RT-S2a Faddeev (parcheggiata, criterio (b) a coeff. variabili) | sì (P-B apre il caso) | **RIAPRI** dentro "serie di Born", con il criterio (b) originale | F6-ENC | no / sì / sì (fuori diagonale N×N) |
| Koopman (parcheggiata) | no (Floquet già seme; DMD = regressione ⇒ vincolo no-ML) | **RESTA PARCHEGGIATA** | — | — |
| PAINLEVÉ + POLE (parcheggiata) | sì (sine-Gordon, e^u; V razionali non autonomi) | **RIAPRI come strumento** (test di Painlevé dopo w = e^{iu}; POLE = Adler–Moser che evolvono per KdV) | F6-DICT (Painlevé), F6-ENC (POLE) | parziale / parziale / dinamica dei poli |
| NLSPEC (parcheggiata) | formalmente sì (Problema 1), ma scompone il dato | **RESTA PARCHEGGIATA** (nota: TV come regolarizzazione analitica per dati rumorosi) | nota F6-CONV | — |
| HAANTJES (parcheggiata) | sì ma vuoto nel lineare | **RESTA PARCHEGGIATA** (trigger ristretto ai sistemi quasi lineari idrodinamici) | nota F6-SYS | — |
| MON per identificazione (parcheggiata) | no | **RESTA PARCHEGGIATA** | — | — |
| F4-ALG autonoma (parcheggiata) | sì (U2 = polinomi nei getti; N1 non lineare) | **RIAPRI come strumento**: ALG-T1/P3 = parte non lineare di N1 | F6-DICT | sì / no / no |
| RT-S1b NAT (scouting breve) | parziale (gauge = equivarianza) | **RESTA PARCHEGGIATA** (nota) | nota F6-SYS | — |
| RT-S1c MOB | no | **RESTA** strato di definizione | — | — |
| RT-S1d EXT (scouting a L1/L4) | sì | **FONDI** nel seme Loewy/eigenring | F6-VAR | parziale / sì / Ext¹ |
| RT-R2a ℝ vs 𝕋 (decisione H0) | sì (bordo, R15) | **RIAPRI** come caso "bordo periodico", senza toccare H0 | F6-CONV | parziale / sì con criterio di risonanza / no |
| RT-S1g MICRO (eliminata per il core) | sì (Dirac, Maxwell, elasticità iperbolici) | **RIAPRI** come Foldy–Wouthuysen (esatta per Dirac libero; asintotica con V) | F6-SYS (+F6-ENC) | no / sì (fogli ±E) / termini dispari |
| RT-S2c MPUM Willems (fusa in RT-4) | sì (traiettorie vettoriali; lemma fondamentale per C1) | **RIAPRI** | F6-SYS (+F6-CONV) | sì in classe EP vettoriale / no / no |
| gamblets / omogeneizzazione (parcheggiata da SCOUT-2) | sì (V oscillante/ruvido) | **RIAPRI come strumento** (costruzione variazionale deterministica; lettura bayesiana esclusa) | F6-ENC | no / sì per scala / no |
| Clifford (parcheggiata fino a Fase 5) | sì | **coperta dal seme** di F6-SYS; lemma di Pauli consegnato (ambiguità per coniugio GL₄) | nota F6-SYS | — |
| Galois parametrizzato | parziale | open question (OQ3) collegata a NS-GALDAR | — | — |
| Riemann–Hilbert come encoder; Magnus/Floquet–Hill; RT-R7a fuori da 𝓗 | sì | **coperte dai semi** (F6-ENC GLM; F6-VAR; F6-DICT via NS-EXPALG) | — | — |
| rinormalizzazione / scale multiple | sì (V rapidamente oscillante) | strumento di media, nessuna strada | nota F6-ENC | — |
| SPLIT-f, S4-LIFT, RT-D2, RT-R4a, RT-R1a, RT-S1h, RT-R7c, WIENER, deconvoluzione cieca, Prony multivariato | no | **RESTANO** eliminate/fuse | — | — |
| probabilità libera, ICA | — (statistiche) | **RESTANO ELIMINATE** (vincolo no-ML) | — | — |
Conteggio: 33 voci riviste; 12 riaperte (di cui 4 come strumento), 1 fusa in un seme, 4 coperte da semi, 8 restano parcheggiate/strato, 10 restano eliminate o fuse.

## 3. Strade NON-seme
| id | idea | caso di prova | I / S / E | novità | decisione (PLAN §2b) |
|---|---|---|---|---|---|
| **NS-EQUIV** | gruppoide di equivalenza / trasformazioni ammissibili come **encoder puntuale** di V; esistenza ⟺ V = a(t)x² + b(t)x + c(t) (CON-FONTE da verificare) | lente di Niederer: libero → oscillatore, V-ex (residuo ~3e-15) | sì / sì / sì (trasporto esatto; i termini non si conservano: V viene soppresso, non scomposto) | 4/10 PROCEED WITH CAUTION (classico; nuovo il criterio come encoder e il trasporto I/S/E) | **PROMUOVI → F6-ENC** (+F6-VAR non autonomo). Ostruzione: Ω e tempo di vita deformati |
| **NS-GALDAR** | Picard–Vessiot/Kovacic + monodromia banale ⇒ criterio decidibile di esistenza dell'**encoder differenziale** (Darboux) | W = ∂ − tanh x (Pöschl–Teller), W = ∂ − 1/x (2/x²), anche per i u_t: V-ex | sì (con O-H1) / parziale (modulo ker W) / parziale | 4/10 PROCEED WITH CAUTION | **PROMUOVI → F6-ENC** (+F6-VAR: Kovacic come test di decidibilità) |
| **NS-EXPALG** | regola di arricchimento D4: aggiungere E = F(u) (exp, sin) come variabile differenziale; Ax–Schanuel per il trdeg; test di Painlevé | sine-Gordon kink e 2-kink, forma polinomiale, Liouville: V-ex; dizionario: kink nucleo 3 (non identifica, boost), 2-kink nucleo 1 (identifica) | sì / no (ALG-O1) / parziale (Hirota) | 4/10 PROCEED WITH CAUTION | **PROMUOVI → F6-DICT** |
| quiver | Morita: Mat_k(R)-mod ≃ R-mod, nulla oltre Malgrange; uso residuo dentro RIGID | — | — | — | **ELIMINA** come strada (resta in RIGID) |
| fasci/microlocale (Kashiwara–Schapira) | utile solo varietà caratteristica + disaccoppiamento iperbolico | Dirac 1+1: det simbolo = KG, V-ex | — | — | **ELIMINA come strada, MERGE** in RT-5 e MICRO riaperte |
| Lie/Olver "a meno di simmetria" | lato encoder = NS-EQUIV; lato ostruzione = RT-R7c/ALG-P5 | — | — | — | **FUSA** |
| Clifford | è seme di F6-SYS | — | — | — | non qualificabile come non-seme |
Quota: 3 non-seme promosse, 3 eliminate/fuse con motivi.

## 4. Esiti SymPy (verifica, non metodo)
- hor1_lens: OK (residui 2.3e-15, 3.4e-15; controllo di non banalità 1.19).
- hor2_darboux: OK. Intertwining Pöschl–Teller 0; centrifugo 0 (dopo correzione di segno φ = 1/x, prima esecuzione con φ = −1/x FAIL, registrata); Schrödinger dipendente dal tempo 0; HOR-P1: valori singolari (70.8, 7.06, 3.57), soluzione (−1, 0, 0); stato stazionario: matrice nulla (HOR-O1).
- hor3_sg: OK. Kink e 2-kink (Hirota, tan(u/4) = (e^{θ1}+e^{θ2})/(1 − A12 e^{θ1+θ2}), A12 = ((a1−a2)/(a1+a2))²; il segno + fallisce, la prima esecuzione con + era FAIL) residui ≤ 7e-14, forma polinomiale verificata su entrambi; Liouville 0; nucleo del dizionario: kink 3, 2-kink 1.
- hor4_dirac: Clifford, det = m² − τ² + ξ², (D₊)(D₋) = −(□+m²)I nel simbolo, covarianza di gauge 0, Λ± idempotenti con entrate non razionali: OK.

## 5. Raccomandazione d'insieme
La revisione conferma l'osservazione del piano: diverse strade parcheggiate "si adattano meglio ai problemi avanzati". Le più utili sono **MICRO→Foldy–Wouthuysen e RT-5** per P-A (S e strato invariante di gauge), **RIGID/STOKES** e **RT-S1d** per P-B1 con potenziali singolari, **Faddeev, gamblets e Mori–Zwanzig** per P-B2/P-C. Fra i non-seme, NS-EQUIV e NS-GALDAR danno a F6-ENC ciò che mancava: **criteri esatti di esistenza dell'encoder** ai livelli puntuale e differenziale. O-H1 dà a F6-VAR/F6-DICT un'ostruzione netta (V libero ⇒ niente identificazione) e un test lineare (V(x) ⇒ Gram). Teorema negativo da registrare come candidato: **HOR-O1**. Costo: ogni riapertura è al più una sottosezione della sessione di Fase 8 del destinatario; nessuna nuova sessione proposta.
