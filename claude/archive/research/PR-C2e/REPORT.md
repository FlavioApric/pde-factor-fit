# REPORT — PR-C2e (Fase 1, pre-ricerca PR-C2: Asse 4 S1–S15 + PR-C2.1, PR-C2.4, PR-C2.5)

Data: 2026-10-22 · Item del piano: PR-C2.1, PR-C2.4, PR-C2.5; Asse 4 (C2.17, C2.17′–C2.76′, C2.58, C2.59); collegamenti C1.0, C2, C3.2, P1/P3, II, A5/A6.
*(Salvato dal coordinatore dalla risposta finale di PR-C2e: la scrittura diretta era bloccata dall'ambiente.)*

## Skill caricate (Regola 2)
- `academic-research-skills\deep-research\SKILL.md` (Read; workflow seguito a mano, nessun subagente). `anthropic-skills:deep-research` non invocata (coordina subagenti, non necessari per un blocco tassonomico).
- `scientific-agent-skills\skills\paper-lookup\SKILL.md` (Read) — nessuna chiamata API eseguita: fonti = testi standard, metadati da validare (open_questions Q9).
- `scientific-agent-skills\skills\scientific-critical-thinking\SKILL.md` (Read) — controllo della classificazione (TAXONOMY §7).
- `scientific-agent-skills\skills\citation-management\SKILL.md` (Read) — formato `sources.bib`.
- SymPy (venv del progetto, `python -I`): `sympy/check_components.py`. Nessuno script `_vendor` eseguito.

## Deliverable
| file | contenuto |
|---|---|
| `TAXONOMY.md` | 120 item collocati una volta; S1–S15 con definizione, colonne della scheda, rilevanza G★; template campo (6); 22 coppie gemelle serie1↔serie2; controllo critico |
| `components_matrix.md` | ~45 termini elementari (costanti, variabili, nonlocali, non lineari, affini) con simbolo e classe; matrice termine × T1–T12; 17 combinazioni canoniche con regime di E_int |
| `cross_index.md` | 18 classi di nuclei × item; snodi con ≥4 classi; frecce di trasformazione tra classi |
| `sympy/check_components.py` (+ `.out.txt`) | 19 residui = 0 + 5 fattorizzazioni |

## Risultati (NOTO = letteratura; VERIFICATO = SymPy; PROPOSTA = da verificare)
1. [PR-C2.1] Conteggio — VERIFICATO (script sul blocco §1.3-C2-TAX): 120 ID distinti, 0 doppioni, 0 estranei. Asse 1/2/3/4 = 44/8/5/63 (l'Asse 4 contiene anche C2.17, C2.58, C2.59).
2. Attributi S1–S15 come colonne — PROPOSTA. Colonne decisive per G★: S1 (dizionario; coefficienti ⇒ anello commutativo o algebra di Weyl), S4 (invarianza per traslazione ⇔ Fourier diagonalizza ⇔ log-simbolo additivo), S5 (nucleo/spettro/base/duale = materia prima di C1.0), S13 (C2.69′ = G★(i)), S3 (V(P) per C3.2). S7 dà una prima decomposizione naturale: generatore = parte simmetrica (dissipativa) + antisimmetrica (conservativa), che commutano a coeff. costanti (|û| vede solo la prima, la fase solo la seconda).
3. Unità di componente (A6) — NOTO nei singoli casi, PROPOSTA come principio: il nucleo di un monomio ∂^α isolato è polinomiale; le classi di A5 (gaussiane, Airy, Fresnel, …) nascono dalle sotto-equazioni a un termine ∂_t − a_n(∂_x). Proposta: la componente di G★(ii) è il generatore a_n(∂_x) con nucleo di semigruppo K_n.
4. Tre regimi di E_int — PROPOSTA (fatti singoli VERIFICATI):
   (i) fattorizzazione coprima ⇒ split additivo esatto (onde (τ−cξ)(τ+cξ); trave E–B τ²+ξ⁴=(τ−iξ²)(τ+iξ²) ⇒ il nucleo di Fresnel risolve la trave, VERIFICATO; Laplace; Helmholtz; C2.19) — coerente con G2 (Ehrenpreis–Malgrange, Hörmander ALPDO II);
   (ii) generatori commutanti (avvezione–diffusione, reazione–diffusione, KdV–Burgers lineare) ⇒ split moltiplicativo K = K_1*K_2, additivo nel log-simbolo (G3; NOTO per semigruppi commutanti, Pazy);
   (iii) non commutanti con algebra di Lie finita: {∂_x², x², x∂_x+½} ≅ sl(2) (VERIFICATO [A,B]=4C, [C,A]=−2A, [C,B]=2B) ⇒ nucleo di Mehler, E_int in forma chiusa via Wei–Norman 1963; potenziale lineare (Avron–Herbst). Il caso f(x) generico (algebra infinita) = Problema 1.
   Telegrafo e Klein–Gordon hanno simbolo irriducibile (VERIFICATO) ⇒ fuori da (i); telegrafo → KG con u=e^{-at}v (VERIFICATO).
5. [PR-C2.4] Indice dei nuclei — classe-hub: nucleo del calore K1 (≥20 item, incl. C2.7, C2.21, C2.41 Feynman–Kac, C2.53 semigruppi, C2.15 via Cole–Hopf VERIFICATO). Snodi multi-classe: C2.5, C2.30, C2.41, C2.53, C2.36, C2.13, C2.37/38 — sono le schede che devono contenere per prime i blocchi di Gram tra classi (C1.0). Classi collegate da parametri continui: K1 = K10|α=2 = K11|β=1; K8 = K10|α=1; K4 = K1|D→i.
6. Firme asintotiche dei termini — NOTO: ‖K(t)‖_∞ ~ t^{-1/n} per ∂_x^n (n=2 calore, 3 Airy, 4 iperdiffusione): test diagnostico qualitativo (controllo, non metodo k3).

## Comunicazioni
- DOMANDA a PR-C2a, PR-C2b, PR-C2c, PR-C2d: nessuna risposta e nessuna scheda cards/*.md alla consegna; integrazione rimandata (open_questions Q7).
- TABELLA a R3 (matrice + indice, 19 residui); AVVISO a R5 (tre regimi di E_int).
- inbox/PR-C2e.md letta a inizio, metà e consegna.

## Limiti
Matrice e indice costruiti dal piano e da fonti standard, non ancora riconciliati con le schede degli altri agenti; bibliografia non validata via API; i segni ●/○ della matrice di incidenza sono giudizi da rivedere con PR-C2b/c. **Coordinatore:** PR-C2e va ripreso per la v2 (integrazione schede) quando PR-C2a–d avranno consegnato.
