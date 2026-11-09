# REPORT — SCOUT-2 (horizon scout: analisi, fisica matematica, segnali, controllo) — Fase 1
Data 2026-10-22. Mandato: §1.6 del piano ("Breadth safeguards", slot aperto RT-ω). Solo strade FUORI da RT-1…RT-7.

**Skill caricate (Regola 2), tutte come lettura del SKILL.md, nessuno script `_vendor` eseguito:**
`academic-research-skills/deep-research` (workflow domanda→fonti→sintesi→verifica; preferito a `anthropic-skills:deep-research` perché quest'ultimo orchestra sotto-agenti e duplicherebbe R1–R8) · `idea-discovery` + `scientific-brainstorming` (prima generazione indipendente delle strade, poi letteratura, poi riapertura; etichette idea/assunzione/evidenza) · `research-lit`/`arxiv`/`semantic-scholar` → eseguiti come WebSearch/WebFetch · `novelty-check` (fasi A–B: confronto con RT-1…7 e con i PLAN di R1, R4, R5, SCOUT-1; la fase C "cross-model" è sostituita dal confronto con i PLAN, niente Codex) · `scientific-critical-thinking` (verdetti: ipotesi, punti deboli, kill).
Controllo SymPy (solo controllo, k3): `sympy/faddeev_cc.py` (output citato in S2-A).
Etichette: [idea] proposta; [ev] evidenza in letteratura; [calc] verificato da script; [ass] assunzione.

## Sintesi
| id proposto | strada | punti appunti | item | verdetto |
|---|---|---|---|---|
| S2-A | Scomposizione di Faddeev / Lippmann–Schwinger ("bilancio per termine") | A8, A9, B2, C2, P3 | C4, P1, P3 | **PROMUOVERE a scouting** (la più promettente) |
| S2-B | Separazione in spazio delle fasi: dominant balance / poligonale di Newton analitica + Wigner–Cohen + separazione geometrica | A5, A8, D1, B2, B6, F6 | C4, P1, P2, D1 | **scouting** (forte su D1, medio su A8) |
| S2-C | Teoria dei sistemi: MPUM di Willems, lemma fondamentale, realizzazione 2D (Roesser/Ho–Kalman) | C3, D5, E1, A7 | C3, P4, II | **scouting breve, probabile merge in RT-4/R4** |
| S2-D | Proiezione di Mori–Zwanzig (E_int = memoria + "rumore") | A1, H1, C2, P3 | P3, Problema 1 | **parcheggiare** (probabile merge in RT-3/R5) |

---
## S2-A — Faddeev / Lippmann–Schwinger: componenti come "contributo di ogni termine"
**Idea.** Scelto un termine di riferimento $L_0$ (con inversa destra $G_0$) e scritto $L = L_0 + \sum_{i=1}^N V_i$ ($V_i=\lambda_i T_i$), ogni $u\in\ker L$ soddisfa l'identità di Lippmann–Schwinger $u = u^{(0)} - G_0\sum_i V_i u$, $u^{(0)}\in\ker L_0$. Le **componenti di Faddeev** $u^{(i)} := -G_0 V_i u$ danno una scomposizione additiva **esatta** $u = u^{(0)} + \sum_i u^{(i)}$ (A9 con E_int ≡ 0 per costruzione) e soddisfano il sistema accoppiato N×N
$$u^{(i)} = -G_i V_i\Big(u^{(0)} + \sum_{j\ne i} u^{(j)}\Big),\qquad G_i := (L_0+V_i)^{-1}$$
($G_i$ = Green del "canale" a due termini $L_0+V_i$, fornita dal catalogo C2), cioè una **matrice di operatori** $\mathbb K_{ij} = -(1-\delta_{ij})G_iV_i$: realizzazione concreta della "Matrice di funzioni E" di B2, con costo lineare (sistema N×N, serie di Neumann se $\|\mathbb K\|<1$), **non 2^N**. L'interazione è il termine fuori diagonale $E_{int}^{(i)} := -G_iV_i\sum_{j\ne i}u^{(j)}$ (candidata h(e_i,e_j) di P1). [ev] Faddeev (1961) e Watson (1953) introducono esattamente questa scomposizione (componenti $\psi^{(i)} = G_0V_i\psi$ con equazioni accoppiate) per lo scattering a tre corpi / multiplo; la formula a due potenziali di Gell-Mann–Goldberger (1953) è la versione al livello del risolvente.

**Caso coefficienti costanti (fatto nuovo, [calc]).** Su $u=\sum_m c_m e^{\tau_m t+\xi_m x}$ con $P(\tau_m,\xi_m)=0$: $u^{(i)} = w_i(\partial)u$ con **pesi** $w_i = -\lambda_i p_i/p_0$ su $V(P)$ e $\sum_i w_i = 1$ su $V(P)$ (partizione dell'unità sulla varietà caratteristica). Trasporto+diffusione ($L_0=\partial_t$): $w_{tr} = c/(c-D\xi)$, $w_{diff} = D\xi/(D\xi-c)$; sui modi di Fourier $\xi=i\kappa$: $|w_{tr}|^2 = c^2/(c^2+D^2\kappa^2)$ — **crossover lorentziano alla scala di Péclet $\kappa^*=c/D$**. Output di `sympy/faddeev_cc.py`: `L u = 0`, `u1+u2-u = 0`, `Faddeev eq 1: 0`, `Faddeev eq 2: 0`, `w1 = c/(-D*xi1 + c)`, `w2 = D*xi1/(D*xi1 - c)`. Con $L_0=\partial_t$ e $G_0=\int_0^t$ (Volterra, sempre invertibile) la scomposizione diventa $u(t)=u(0)+\sum_i\int_0^t A_iu(s)\,ds$: il "bilancio per termine" esatto, lineare, O(N).

**Cosa cambia nel problema.** L'esistenza di E_int dipende dalla DEFINIZIONE di componente: se $u_n$ = "contributo del termine n" (bilancio) allora E_int = 0 sempre; se $u_n$ deve stare nella classe del termine (ker/semigruppo, A5, G3) allora E_int ≠ 0. Il ponte quantitativo è $u^{(i)}(t) - (S_i(t)u_0-u_0)$ = interazione del termine i ([idea], da calcolare e confrontare con G3).
**Relazione con le RT.** Non è RT-2 (moltiplicativo/log-simbolo) né RT-3 (BCH/Dyson nel tempo): è una formulazione stazionaria al livello di risolvente/Green con struttura matriciale N×N. Tocca R5 (P3) e R3/PR-C2 (servono le $G_i$ dei sotto-sistemi a due termini).
**Rischi [scientific-critical-thinking].** (1) Dipendenza dalla scelta di $L_0$ (libertà di "gauge"): serve un principio di selezione ($L_0=\partial_t$ per l'evoluzione; termine d'ordine massimo per le ODE) o un teorema di covarianza. (2) Con $V_i$ differenziali non limitati, la convergenza di Neumann richiede limitatezza relativa (Kato): da verificare. (3) Rischio di banalità: il bilancio $u(t)-u(0)=\sum\int A_iu$ è ovvio; il valore sta nel sistema accoppiato e nei pesi $w_i$.
**Costo.** Basso–medio: 1 agente, ~1 giorno; ingredienti classici.
**Criterio (fissato ora).** PROMUOVI se (a) teorema in L2 ($u_t=\sum a_k(\partial_x)u$) con pesi $w_i$ in forma chiusa e formula esplicita che lega $E_{int}^{Faddeev}$ all'E_int additivo di G3, E (b) convergenza del sistema N×N con ipotesi verificabili in un caso L4 (trasporto+diffusione a coefficiente variabile). ELIMINA se le componenti dipendono da $L_0$ senza alcun principio di selezione, o se non si legano a nessuna classe C2 (resta solo il bilancio banale).

---
## S2-B — Separazione in spazio delle fasi (dominant balance analitico, Wigner/Cohen, separazione geometrica)
**Idea.** Ogni termine $T_k$ "domina" in una regione dello spazio $(\tau,\xi)$ (o $(x,\kappa)$): la poligonale di Newton del simbolo $P=\sum\lambda_kp_k$ individua i regimi di bilanciamento dominante (es. trasporto per $|\kappa|\ll c/D$, diffusione per $|\kappa|\gg c/D$ — lo stesso $\kappa^*$ di S2-A). Definire $u_n$ := restrizione microlocale di $u$ (Fourier/FBI/Wigner) al regime n; E_int := parte localizzata nelle zone di crossover + termini d'interferenza. Due strumenti già noti: (i) [ev] la distribuzione di Wigner di una somma contiene i termini incrociati $W_{u_1,u_2}$ — un h(e_1,e_2) **bilineare canonico** (P1/B2), localizzato "a metà strada" tra le componenti (geometria delle interferenze, Hlawatsch–Flandrin) e sopprimibile con kernel della classe di Cohen; (ii) [ev] la **separazione geometrica** di Donoho–Kutyniok (CPAM 2013): ℓ¹ su due frame (wavelet/curvelet) separa le componenti con errore relativo → 0 alle scale fini grazie a *cluster coherence* e wavefront set separati (Kutyniok 2012: anche con thresholding a passo singolo). È la forma analitica di **D1 "ENCODING + GROUPING ⇒ E_int → 0"**: encoder = trasformata di fase (senza pesi), grouping = ℓ¹ a gruppi per frame/regime, teorema = limite di scala.
**Teorema-bersaglio [idea].** Per L2 a due termini con scale separate: $\|E_{int}\|/\|u\|\to0$ nel limite di scala ($\kappa^*\to0$ o $\infty$), con tasso dato dalla larghezza della zona di crossover (trasporto+diffusione: la lorentziana di S2-A); componenti identificate regime per regime dalle pendenze (esponenti di Puiseux) di V(P).
**Relazione.** Non seminata. Sovrapposizione con SCOUT-1 (Newton polygon / Levelt–Turrittin / tropicale, lato algebrico) e con R1 (coerenza, ℓ¹, P2): qui il lato è analitico/asintotico. Collega P2 (B6, ℒ_ALT) a un teorema esistente di separazione con ℓ¹.
**Rischi.** Separazione solo asintotica (non esatta a scala finita: tensione con B4 "esatto"); per dati con spettro concentrato nel crossover E_int non è piccolo. Wigner è quadratica: la scomposizione va mantenuta lineare in u (FBI/filtri di Fourier; Wigner solo come diagnostica).
**Costo.** Medio: 1 agente, 1–2 giorni.
**Criterio.** PROMUOVI se si dimostra (o si trova) $\|E_{int}\|/\|u\| = O(\varepsilon^\gamma)$ per un caso L2 a due termini nel limite di separazione di scala ε, con ε leggibile dal simbolo. ELIMINA se E_int non decresce in alcuna scala naturale o se per dati generici la quota nel crossover è O(1) senza parametro di controllo (D1 resterebbe euristico).

---
## S2-C — Teoria dei sistemi: MPUM di Willems, lemma fondamentale, realizzazione 2D
**Idea.** Riformulare "operatore dal nucleo" come **modellazione esatta**: il *most powerful unfalsified model* (MPUM, Willems 1986) è il behaviour più piccolo (lineare, invariante per traslazioni, chiuso) che contiene i dati; per dati esponenziale-polinomiali esiste ed è unico, e in una variabile è il nucleo dell'annullatore minimo (= Ann(u), RT-4). [ev] Rapisarda–Antoulas (SIAM J. Control Optim. 2016) calcolano la rappresentazione di stato dell'MPUM per traiettorie vettoriali-esponenziali in **due variabili indipendenti** (PDE a coeff. costanti) e un modello di Roesser, fattorizzando matrici costanti costruite dai dati. Il "lemma fondamentale" (Willems–Rapisarda–Markovsky–De Moor 2005) dà la **persistenza di eccitazione** ⇔ le traiettorie osservate generano tutto il behaviour (criterio di rango di Hankel). La dualità di Oberst (1990) modulo ↔ behaviour dà il quadro (lato algebrico: SCOUT-1).
**Cosa aggiunge a RT-4.** (1) La realizzazione (Ho–Kalman, Roesser) è una forma canonica della **via (b) di Idea II** (compagna, D5/E1) ottenuta dai dati, con unicità fino a similitudine (teorema di isomorfismo di stato): collega C3 e II. (2) Persistenza di eccitazione = versione "rango" della congettura G4.
**Rischi.** Molto vicino a RT-4 (R4 cita Kalman/osservabilità, SCOUT-1 cita Oberst/Willems). Risultati 2D solo per esponenziali-polinomiali (dimensione finita): non coprono misure di Ehrenpreis continue (RT-7).
**Costo.** Basso: 3 articoli, mezza giornata.
**Criterio.** PROMUOVI se l'MPUM 2D o il lemma fondamentale danno un teorema di identificabilità per L3 **più forte o con ipotesi più verificabili** della G4, o una forma canonica della via (b) con invarianti nuovi per E4. ELIMINA (merge-into RT-4) se si riduce a "Ann(u) + rango di Hankel" senza nuovi teoremi.

---
## S2-D — Mori–Zwanzig: E_int come memoria e "rumore"
**Idea.** Con il proiettore 𝒫 sulla classe di una componente, l'identità di Mori–Zwanzig (Dyson + proiettori) dà un'equazione esatta per 𝒫u: termine markoviano + **memoria** (convoluzione nel tempo) + termine "rumore" ortogonale. È una formula chiusa ed esatta dell'interazione; il termine-rumore è letteralmente il "rumore" di A1/H1 (H1: V(x) variabile trattato "come rumore" da eliminare con un encoder).
**Relazione.** Matematicamente è Duhamel + proiettori: già nel perimetro di R5 (Dyson, Duhamel) e RT-3. Novità solo nel vocabolario e nel legame con Problema 1 (fuori scopo fino a Fase 5).
**Criterio.** PROMUOVI solo se il kernel di memoria per due termini commutanti coincide in forma chiusa con $(K_1-\delta)*(K_2-\delta)$ di G3 o dà un criterio nuovo E_int=0 ⇔ [𝒫,L]=0. Altrimenti merge-into RT-3. **Verdetto: parcheggiare**; fonte segnalata a R5.

---
## Fusi / parcheggiati (con motivo)
| campo | esito | motivo |
|---|---|---|
| Prony multivariato, decomposizione polinomio-esponenziale da momenti (Mourrain 2018; Kunis–Peter–Römer–von der Ohe 2016), Kronecker multivariato | merge → RT-4, AVVISO R4 | ker della matrice dei momenti = ideale dei polinomi annullanti = Ann(u); decomposizione per punti = primaria (RT-1). |
| Koopman / DMD esatta / vettori ciclici (molteplicità di Hellinger–Hahn) | merge → RT-7 / R1-d | $u_0$ ciclico ⇔ identificabilità; modello di moltiplicazione su $L^2(\mu_{u_0})$ = G6. |
| ANOVA / Hoeffding / Sobol (u come funzione di λ) | merge → RT-2 (vocabolario) | E_int = interazioni di ordine ≥2 dell'inclusione-esclusione 2^N; in scala log l'ANOVA è additiva ⇔ termini commutanti. |
| Matrici di trasferimento, Magnus, Floquet–Hill | merge → RT-3 / R5, R4 | Magnus = BCH continuo; Hill inverso = R4; livello L0.5 già previsto in §1.6. |
| Wavelet adattate all'operatore / gamblets (Owhadi–Scovel 2019), omogeneizzazione | parcheggiato, AVVISO R1 | scompone per SCALA (ortogonale nell'energia), non per TERMINE; candidabile come spazio C1 con scomposizione ortogonale. |
| Deconvoluzione cieca (cross-relation, Xu–Liu–Tong–Kailath 1995) | merge → RT-2/G4 | $\hat u(t_2)/\hat u(t_1)=e^{(t_2-t_1)a(\kappa)}$: già nella G4. |
| Rinormalizzazione (Chen–Goldenfeld–Oono), multiple scales | merge → S2-B (scale) e R5 (termini secolari) | stesso contenuto del dominant balance; utile per la convergenza in P3. |
| Separazione cieca statistica (ICA) | eliminato | non analitico (k3), richiede indipendenza statistica e più miscele. |

## Giudizio complessivo
Le due strade genuinamente nuove sono **S2-A** (scomposizione additiva ESATTA e lineare in N che sposta E_int in una matrice N×N di operatori: risposta strutturale a B2) e **S2-B** (versione analitica e dimostrabile di D1 via separazione in spazio delle fasi). Convergono sullo stesso oggetto: i **pesi per termine sulla varietà caratteristica** $w_i(\tau,\xi)$ e la scala di crossover dove due termini si bilanciano. S2-C e S2-D sono quasi certamente assorbite da RT-4 e RT-3.