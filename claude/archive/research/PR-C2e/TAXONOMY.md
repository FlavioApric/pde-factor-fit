# TAXONOMY — PR-C2.1 (120 item) + Asse 4 S1–S15 come colonne delle schede

Agente: PR-C2e · 2026-10-22 · Fonte: piano §1.3-C2-EXT (testo verbatim degli item), §1.3-C2-TAX (collocazione), card schema (campo (6) = attributi S1–S15).
Notazione: `NOTAZIONE.md` (simbolo `P(τ,ξ)`, `∂_t↔τ`, `∂_x↔ξ`; `V(P)`; `Ann(u)`; `E_int`).
Tag di rilevanza: ★ core lineare scalare 1D · ◆ framework C1/C3 · ▲ Fase 4 non lineare · ■ sistemi · ● stocastico · ◇ multi-D/geometrico/applicato · ○ numerico (solo riferimento, vincolo k3).

---

## 0. Conteggio (verificato)

Controllo eseguito con uno script di conteggio sul blocco §1.3-C2-TAX del piano (righe 332–496; controllo, non metodo): **120 menzioni, 120 ID distinti, 0 doppioni, 0 ID estranei** (insieme atteso = {C2.1…C2.60} ∪ {C2.17′…C2.76′}).

| Asse | Blocchi | Item | di cui serie 1 | di cui serie 2 (′) |
|---|---|---|---|---|
| 1 Famiglie | T1–T12 | 44 | 44 | 0 |
| 2 Metodi esatti | — | 8 | 8 | 0 |
| 3 Quadro funzionale | — | 5 | 5 | 0 |
| 4 Attributi strutturali | S1–S15 | 63 | 3 (C2.17, C2.58, C2.59) | 60 |
| **Totale** | | **120** | **60** | **60** |

(Correzione rispetto al mio PLAN.md, che stimava 41/8/5/66: l'Asse 4 contiene anche tre item della serie 1 — C2.17 in S1, C2.58 e C2.59 in S14 — e l'Asse 1 ne contiene 44.)
Dettaglio Asse 1: T1 5 · T2 3 · T3 3 · T4 3 · T5 4 · T6 3 · T7 2 · T8 3 · T9 2 · T10 6 · T11 9 · T12 1 = 44.
Dettaglio Asse 4: S1 8 · S2 4 · S3 2 · S4 3 · S5 4 · S6 8 · S7 4 · S8 5 · S9 2 · S10 3 · S11 4 · S12 6 · S13 3 · S14 6 · S15 1 = 63.

---

## 1. Asse 1 — Famiglie di equazioni (cosa è l'operatore) · 44 item · schede: PR-C2a/b/c

Formato: ID · tag · operatore canonico 1D (simbolo `P(τ,ξ)`) · classe di nucleo tipica · proprietario.

**T1 ODE lineari (PR-C2a)**
- C2.1 ★ coefficienti costanti · `p(∂_x)`, `p(ξ)` · `x^k e^{λx}` (quasi-polinomi) · a
- C2.2 ★■ ODE forzate e sistemi · `y′=Ay+f` · `e^{xA}`, Jordan, Green causale · a
- C2.3 ★▲ primo ordine · `y′+a(x)y` (lineare ★); Bernoulli/Riccati/Clairaut ▲ · `e^{-∫a}` · a
- C2.4 ★ coefficienti variabili · Euler–Cauchy `x²y″+axy′+by`, Frobenius · `x^r Σ c_n x^n`, `x^r log x` · a
- C2.5 ★◇ ODE di funzioni speciali · Bessel, Legendre, Hermite, Laguerre, Airy, ipergeometrica · funzioni olonome (D-finite) · a

**T2 PDE del primo ordine (PR-C2b)**
- C2.6 ★▲ trasporto · `∂_t+c∂_x`, `τ+cξ` · `g(x−ct)` · b
- C2.18 ▲ primo ordine generale (Lagrange lineare ★) · `a∂_t+b∂_x+c` · integrali primi lungo caratteristiche · b
- C2.25 ▲ Hamilton–Jacobi/iconale · `u_t+H(u_x)` · soluzioni di viscosità, Hopf–Lax · b

**T3 Parabolica (PR-C2b)**
- C2.7 ★▲ diffusione · `∂_t−D∂_x²`, `τ−Dξ²` · nucleo del calore (gaussiana), Hermite · b
- C2.21 ★ PDE paraboliche · `∂_t−∂_x(a(x)∂_x)` · nucleo del calore generalizzato, Aronson · b
- C2.39 ▲ diffusione non lineare/mezzi porosi · `u_t=(u^m)_xx` · Barenblatt · b (▲ anche c)

**T4 Iperbolica (PR-C2b)**
- C2.8 ★◇ onde · `∂_t²−c²∂_x²`, `τ²−c²ξ²` · d'Alembert `f(x−ct)+g(x+ct)` · b
- C2.22 ★■ iperboliche e sistemi · `∂_t U+A∂_x U` · onde semplici lungo autovettori · b
- C2.31 ■◇ relativistiche · Klein–Gordon `∂_t²−∂_x²+m²` ★ · Bessel `J_0(m√(t²−x²))` · b

**T5 Ellittica (PR-C2b)**
- C2.9 ★◇ ellittiche · Laplace `∂_x²+∂_y²` (in 1D+t: `∂_t²+∂_x²`) · armoniche, `log r` · b
- C2.20 ★◇ problemi al contorno ellittici · idem + BC · Green di dominio · b
- C2.34 ◇ flusso potenziale/analisi armonica · `∂_z̄` · funzioni olomorfe, Poisson · b
- C2.35 ★◇ Helmholtz/autovalori · `∂_x²+k²` · `e^{±ikx}`, Hankel in 2D · b

**T6 Dispersiva (PR-C2b)**
- C2.10 ★ dispersiva (Airy) · `∂_t+∂_x³`, `τ+ξ³` · nucleo di Airy · b
- C2.30 ★●▲ quantistica · `i∂_t+∂_x²` ★; `V(x)` = Problema 1; NLS ▲ · nucleo di Fresnel · b
- C2.46 ▲ dispersive non lineari · KdV, BO, NLS, KP · solitoni · b/c

**T7 Reazione/crescita (PR-C2b)**
- C2.11 ★▲ reazione · `∂_t−a` ★; logistica/Fisher–KPP ▲ · `e^{at}` · b
- C2.42 ▲■ pattern formation/biologia · reazione–diffusione, Keller–Segel · fronti, Turing · b/c

**T8 Operatori misti/composti — banco di prova di E_int (PR-C2b)**
- C2.12 ★ avvezione–diffusione, telegrafo, onde smorzate · `∂_t+c∂_x−D∂_x²`; `∂_t²+2a∂_t−c²∂_x²` · gaussiana traslata; Bessel `I_0` · b
- C2.19 ★ lineari di ordine alto · `P(∂)` fattorizzabile, biarmonica, `∂_t+∂_x⁴` · somma diretta dei nuclei dei fattori · b
- C2.23 ◇ tipo misto · Tricomi `y u_xx+u_yy` · Airy/ipergeometriche · b

**T9 Nonlocale/frazionaria (PR-C2b)**
- C2.37 ◆★ integrali e nonlocali · `(−∂_x²)^{α/2}`, `J*u−u` · leggi α-stabili · b
- C2.38 ◆★ frazionarie · Caputo `∂_t^β`, Riesz `|ξ|^α` · Mittag-Leffler, Wright, Fox H · b

**T10 Non lineari e integrabili (PR-C2c)**
- C2.15 ▲ PDE non lineari · Burgers `u_t+uu_x=νu_xx` · Cole–Hopf → calore · c
- C2.16 ▲◆ strutture integrabili e asintotiche · IST, WKB, scale multiple · c
- C2.24 ▲■ leggi di conservazione · `u_t+f(u)_x=0` · shock, rarefazioni · c
- C2.44 ▲ onde viaggianti · `u(x−ct)` · orbite eterocline/omocline · c
- C2.45 ▲ integrabili (Lax, IST) · KdV, mKdV, NLS, sine-Gordon · solitoni `sech²` · c
- C2.47 ▲ blow-up · `u_t=u_xx+u^p` · autosimilari · c

**T11 Modelli fisici applicati (PR-C2c)**
- C2.26 ◇■ fluidi comprimibili · C2.27 ◇■ incomprimibili · C2.28 ◇■ acque basse · C2.29 ◇■ elettromagnetismo · C2.32 ◇■ elasticità
- C2.33 ★◇ piastre e travi · Euler–Bernoulli `∂_t²+∂_x⁴` (caso test ★ 1D) · modi `cos(k²t)sin(kx)` · c
- C2.40 ◇ cinetiche · C2.43 ▲◇ frontiera libera · C2.57 ◇ grafi e reti

**T12 Stocastiche (PR-C2c)**
- C2.41 ● probabilità e SPDE (Feynman–Kac ◆ come rappresentazione analitica) · c

## 2. Asse 2 — Metodi esatti (come si calcolano i nuclei) · 8 item · schede: PR-C2d
- C2.13 ★◆ separazione di variabili / Sturm–Liouville
- C2.14 ★◆ trasformate integrali
- C2.36 ★◆ funzioni di Green e soluzioni fondamentali
- C2.48 ◆ perturbazioni e asintotica (→ P3)
- C2.49 ◆ similarità e scaling
- C2.50 ◆◇ metodi di Lie (→ II.4)
- C2.51 ◆ formulazioni variazionali/deboli
- C2.60 ★◆ problemi inversi e identificazione (= C3/P4)

## 3. Asse 3 — Quadro funzionale (su cosa si costruisce C1) · 5 item · schede: PR-C2d
- C2.52 ◆ Sobolev/distribuzioni · C2.53 ◆ semigruppi/equazioni di evoluzione · C2.54 ◆ buona posizione · C2.55 ◆ condizioni al bordo/iniziali · C2.56 ◇◆ coordinate/PDE geometriche

---

## 4. Asse 4 — Attributi strutturali S1–S15 (63 item) · PR-C2e

Ogni attributo Sj diventa **una colonna** del campo (6) della scheda. Per ciascuno: (a) item contenuti; (b) definizione breve; (c) **valori della colonna** (vocabolario chiuso + slot "altro" per la regola §1.6); (d) **rilevanza per G★**. Gli item della serie 2 sono "sotto-colonne": il loro testo nel piano elenca i valori ammessi.

### S1 Forma e classificazione — C2.17 ◆, C2.17′, C2.18′, C2.19′, C2.20′, C2.21′, C2.22′, C2.23′
- **Definizione.** Dati sintattici dell'operatore `L = Σ_k λ_k T_k`: ordine e multi-indici `α_k` (C2.17′), struttura di linearità (C2.18′), simbolo principale e tipo (C2.17, C2.19′), operatori differenziali elementari che compaiono (C2.20′), struttura dei coefficienti (C2.21′), scalare/sistema (C2.22′), variabili (C2.23′).
- **Colonne.** `ordine (m_t, m_x)`; `multi-indici {α_k}` (lista ↔ righe della matrice componenti); `lineare | semilineare | quasilineare | pienamente NL | affine`; `simbolo P(τ,ξ)` e `σ_m(P)`; `tipo ∈ {ellittico, iperbolico, parabolico, dispersivo, misto, degenere, nessuno (ordine 1)}`; `coeff ∈ {costanti, polinomiali, analitici, lisci, periodici, rugosi, singolari}`; `scalare | sistema n×n`; `variabili (t,x) | (x) | (x,y)`.
- **Rilevanza G★ (massima, ★).** È il dizionario stesso: H2 fissa `T_k = ∂^{α_k}` (coeff. costanti) o `f_k(x)∂^{α_k}`. Il campo `coeff` decide il quadro algebrico di `Ann(u)` (ideale di `ℂ[τ,ξ]` vs ideale sinistro dell'algebra di Weyl) e quindi se §1.2-2b (commutativo, E_int moltiplicativo ma additivo nel log-simbolo) o §1.2-2c (commutatori/BCH) si applica. Il tipo/simbolo principale è il punto di contatto con la via (a) di II (tensore simbolo).

### S2 Dominio e dati — C2.24′, C2.25′, C2.26′, C2.27′
- **Definizione.** Geometria/topologia di Ω, formulazione ai valori iniziali, condizioni al bordo, classe del problema al contorno.
- **Colonne.** `Ω ∈ {ℝ, 𝕋, [0,ℓ], semiretta, I×ℝ, I×𝕋, grafo}`; `dati ∈ {Cauchy, IBVP, BVP, sovradeterminato}`; `BC ∈ {D, N, R, misto, periodico, trasmissione, radiazione, assorbente}`.
- **Rilevanza G★ (★/◆).** H0 sceglie `I×ℝ` o `I×𝕋`. Su 𝕋 lo spettro di `∂_x` è discreto (`ξ ∈ iℤ`) ⇒ base numerabile `{e^{inx}}`; su ℝ è continuo ⇒ frame continuo (risposta ad A7, congettura G6). Le BC fanno parte dell'operatore: due problemi con lo stesso `P` e BC diverse hanno nuclei diversi (es. calore su `[0,ℓ]` Dirichlet ↔ serie di seni; Neumann ↔ coseni) — per l'identificazione da una `u` le BC sono **non osservabili dall'interno** e vanno trattate come incognite o fissate da H0.

### S3 Geometria caratteristica e causale — C2.28′, C2.29′
- **Definizione.** Varietà caratteristica `V(P)`, direzioni/curve caratteristiche (`σ_m(P)(dt,dx)=0`), coni di dipendenza, velocità di propagazione, propagazione delle singolarità.
- **Colonne.** `V(P)` (equazione); `caratteristiche reali: nessuna | 1 famiglia | 2 famiglie`; `velocità: finita c | infinita`; `supporto: preservato compatto | non compatto`.
- **Rilevanza G★ (◆).** `V(P)` è l'oggetto centrale di C3.2 (identificabilità: chiusura di Zariski del supporto della misura di Ehrenpreis di `u` = `V(P)`, congettura G4). Distinguere velocità finita/infinita è un test diagnostico qualitativo su `u` (supporto compatto preservato ⇒ niente termine parabolico/dispersivo).

### S4 Invarianti — C2.30′, C2.31′, C2.32′
- **Definizione.** Leggi di conservazione/bilancio (C2.30′), simmetrie (traslazioni, riflessioni, Galileo, Lorentz, gauge; C2.31′), scaling e dimensioni (C2.32′).
- **Colonne.** `invarianza per traslazione in x / in t (sì/no)`; `gruppo di Lie dei punti` (generatori); `peso di scaling` `[∂_t] = [∂_x]^s` (omogeneità del simbolo: calore s=2, Airy s=3, trasporto s=1); `quantità conservate` (massa `∫u`, energia `∫|u|²`, …).
- **Rilevanza G★ (★).** **Invarianza per traslazione ⟺ coefficienti costanti ⟺ diagonalizzazione simultanea con Fourier** (§1.2-3, F6): è l'attributo che decide se il "log-simbolo" rende additivo lo split (G3). Lo **scaling** separa i termini: termini con pesi diversi dominano a scale diverse (base dell'asintotica di P3) e un dizionario di monomi è una somma di pezzi quasi-omogenei. Le leggi di conservazione danno vincoli lineari su `λ` (es. `∫u` conservata ⇔ nessun termine di reazione puro).

### S5 Rappresentazione, nucleo e spettro — C2.33′, C2.34′, C2.35′, C2.36′ (nucleo di C1–C4/P4)
- **Definizione.** Trasformata che diagonalizza (C2.33′), nuclei (fondamentali, Green, calore, Poisson, propagatori, risolventi, **riproducenti**; C2.34′), struttura spettrale (C2.35′), ortogonalità/completezza e sistemi **biortogonali** (C2.36′).
- **Colonne.** `trasformata ∈ {Fourier, serie di Fourier, Laplace, Mellin, Hankel, Sturm–Liouville, IST}`; `nucleo K(t,x)` (forma chiusa + classe: gaussiana, Airy, Fresnel, Bessel, Mittag-Leffler, …); `spettro ∈ {discreto, continuo, misto}` con `λ(κ) = P(·,iκ)`; `base {e_{n,i}}` numerabile/continua; `duale`: ortonormale | biortogonale | frame.
- **Rilevanza G★ (★◆, la colonna più importante).** È letteralmente il campo (2)–(3)–(5) della scheda e il materiale grezzo di C1.0 (dizionario 𝒟, Gram G, nucleo riproducente K, sistema duale). I nuclei di questa colonna sono le "classi di funzioni" di A5/C2; l'indice incrociato (`cross_index.md`) è costruito su questa colonna.

### S6 Spazi e teoria delle soluzioni — C2.37′ … C2.44′
- **Definizione.** Spazi funzionali, regolarità, nozioni di soluzione generalizzata, esistenza/unicità, buona posizione, stime d'energia, principi del massimo, monotonia.
- **Colonne.** `spazio naturale` (`L²`, `H^s`, pesato, analitico); `effetto regolarizzante` (analitico/Gevrey/nessuno); `nozione` (classica/debole/mild/viscosità/entropica); `ben posto avanti/indietro`; `principio del massimo (sì/no)`.
- **Rilevanza G★ (◆).** Fissa H1. L'effetto regolarizzante dice **quanto della `u` osservata è informativo**: per il calore `u(t,·)` è intera per `t>0` (tutte le derivate disponibili ⇒ il jet `Φ(u)` è ben definito ovunque), per trasporto/onde `u` è regolare quanto i dati (jet limitato da H1). Buona posizione all'indietro (falsa per il calore) ⇒ instabilità dell'identificazione su intervalli lunghi (C3, P2). Principio del massimo = vincolo di segno sui coefficienti (`D>0`).

### S7 Geometria variazionale e dinamica — C2.45′, C2.46′, C2.47′, C2.48′
- **Definizione.** Struttura di Eulero–Lagrange, hamiltoniana/simplettica, flusso gradiente, dissipativa.
- **Colonne.** `L autoaggiunto | antiautoaggiunto | normale | non normale` (per il generatore spaziale `A` in `u_t = Au`); `dissipativo (Re σ(A) ≤ 0)`; `hamiltoniano (A = J ∇H)`; `funzionale` (energia/entropia).
- **Rilevanza G★ (◆).** Ogni generatore lineare a coeff. costanti si spezza in parte **simmetrica** (simbolo reale pari: `∂_x²`, `∂_x⁴`, reazione → dissipazione) e **antisimmetrica** (simbolo immaginario: `∂_x`, `∂_x³`, `i∂_x²` → trasporto/dispersione, conservativi). È la prima "decomposizione per componenti" naturale: `u_t = (A_s + A_a)u` con `[A_s, A_a] = 0` a coeff. costanti; `|û|` vede solo `A_s`, la fase solo `A_a` (lettura diretta del log-simbolo, G3). La normalità decide la diagonalizzazione congiunta di F6.

### S8 Estensioni operatoriali — C2.49′, C2.50′, C2.51′, C2.52′, C2.53′
- **Definizione.** Operatori nonlocali/ΨDO/frazionari, struttura microlocale, strutture differenziali geometriche, rappresentazioni in coordinate, singolarità e degenerazioni.
- **Colonne.** `locale | nonlocale`; `simbolo` (polinomiale | `|ξ|^α` | razionale | `sgn ξ`) e `ordine reale`; `coordinate` (cartesiane | polari/radiali `∂_r + (d−1)/r`); `punti singolari` (regolari/irregolari: Fuchs).
- **Rilevanza G★ (◆★).** Il calcolo dei simboli è il linguaggio di `â = f(J·Φ)` (F1): allargare il dizionario da `ξ^k` a `|ξ|^α` (C2.37–38) è un'estensione "gratuita" nel dominio log-simbolo ma rompe la località (Ann(u) non è più un ideale polinomiale). Le coordinate radiali generano coefficienti `1/r` ⇒ Bessel: è il meccanismo per cui coefficienti polinomiali/razionali producono funzioni speciali (C2.6ᵈ).

### S9 Interfacce — C2.54′, C2.55′
- **Definizione.** Frontiere libere, interfacce, condizioni di trasmissione/accoppiamento.
- **Colonne.** `interfaccia: nessuna | fissa | mobile`; `condizioni di salto`.
- **Rilevanza G★ (◇, bassa).** Fuori dal core (Ω senza interfacce). Utile solo come avvertenza: coefficienti costanti a tratti (trasmissione) ⇒ `u` non è nel nucleo di un unico `P` globale; il dizionario deve essere localizzato.

### S10 Stocastica, multiscala, perturbativa — C2.56′ ●, C2.57′, C2.58′
- **Definizione.** Coefficienti/forzanti aleatorie, struttura multiscala (omogeneizzazione), struttura perturbativa (espansioni regolari/singolari, WKB).
- **Colonne.** `rumore: nessuno | additivo | moltiplicativo`; `piccolo parametro ε e termine che moltiplica`; `perturbazione regolare | singolare (ε moltiplica l'ordine massimo)`.
- **Rilevanza G★ (◆ per C2.58′, ● per C2.56′).** H3 esclude rumore. C2.58′ → P3: l'E_int nel quadro di interazione (Dyson/Duhamel) è esattamente una serie perturbativa in un termine rispetto all'altro; la colonna "singolare" segnala dove l'espansione additiva non converge uniformemente (strati limite: es. `ε∂_x² + ∂_x`).

### S11 Stabilità e comportamento a lungo termine — C2.59′, C2.60′, C2.61′, C2.62′
- **Definizione.** Biforcazioni/linearizzazione, attrattori e decadimento, strutture coerenti (fronti, impulsi), onde singolari (shock, delta).
- **Colonne.** `tasso di decadimento` (`t^{-1/2}`, `t^{-1/3}`, esponenziale); `strutture coerenti` (sì/tipo); `discontinuità` (sì/no).
- **Rilevanza G★ (◆ debole).** I tassi asintotici sono **firme dei termini**: `‖u‖_∞ ~ t^{-1/2}` (diffusione), `t^{-1/3}` (Airy), `t^{-1/2}` con oscillazione (Schrödinger), `t^{-1/4}` (`∂_x⁴`). Forniscono un test diagnostico indipendente per l'identificazione (controllo, non metodo).

### S12 Struttura non lineare ▲ — C2.63′, C2.64′, C2.65′, C2.66′, C2.67′, C2.68′
- **Definizione.** Entropia, interazione non lineare/accoppiamento di modi (C2.64′ = analogo non lineare di E_int), integrabilità, riduzioni ed equivalenze (trasformazioni di variabile dipendente = "encoder" analitico di D1), asintotica al bordo, mediazione.
- **Colonne.** `nonlinearità` (monomi del jet: `uu_x`, `u²`, `|u|²u`, `sin u`, `(u^m)_xx`); `linearizzabile esattamente` (Cole–Hopf, Miura, IST, hodografo, no); `integrabile (Lax)`.
- **Rilevanza G★ (▲, Fase 4).** G7: con monomi del jet nel dizionario l'identificazione resta **lineare in λ**; la decomposizione richiede una linearizzazione esatta (colonna "linearizzabile"). C2.66′ è la colonna che dice se esiste l'encoder di D1.
- **Nota critica.** C2.67′ (asintotica al bordo) e C2.68′ (mediazione) non sono intrinsecamente non lineari: semanticamente appartengono a S10. Li lascio in S12 (collocazione del piano, conteggio invariato) e lo segnalo in `open_questions.md`.

### S13 Inverso, controllo, dati — C2.69′ ★◆, C2.70′, C2.71′ ●
- **Definizione.** Strutture di identificazione (operatori inversi, recupero dei coefficienti, identificabilità), controllo/osservabilità, assimilazione dati/incertezza.
- **Colonne.** `identificabile da una soluzione (sì/no/condizione)`; `dati minimi` (es. `#supp û_0 ≥ deg a + 1`, G4); `osservabilità`.
- **Rilevanza G★ (★ massima).** C2.69′ **è** G★(i). Ogni scheda deve dichiarare la condizione di identificabilità della sua famiglia (C3.2). Osservabilità (C2.70′) ↔ identificabilità: entrambe sono iniettività di una mappa lineare dati→parametri.

### S14 Numerico ○ (solo riferimento) — C2.58, C2.59, C2.72′, C2.73′, C2.74′, C2.75′
- **Definizione.** Metodi numerici, CFD, discretizzazione, stabilità/consistenza, spazi di approssimazione, solutori.
- **Colonne.** Nessuna colonna obbligatoria nelle schede (k3). Facoltativa: `analogo discreto` (es. differenze finite di `∂_x^k` = matrice di Toeplitz → analogo finito-dimensionale di `J_φ`, II); `splitting` (Lie/Strang ↔ Trotter, §1.2-2b).
- **Rilevanza G★ (○).** Contrasto e controllo. C2.75′ operator splitting è il gemello numerico della fattorizzazione `e^{t(A+B)} ≈ e^{tA}e^{tB}`: il suo errore di ordine `t²[A,B]/2` è l'E_int del quadro moltiplicativo.

### S15 Modellazione — C2.76′
- **Definizione.** Relazioni costitutive, chiusure, modelli ridotti, validazione.
- **Colonne.** `origine fisica dei termini` (flusso di Fick → `∂_x²`, Fourier → calore, ecc.).
- **Rilevanza G★ (◇, bassa).** Utile solo per dare un nome fisico a ogni componente identificata (interpretazione dell'output di 𝓘).

---

## 5. Vettore attributi della scheda (campo (6)) — template

Ogni scheda PR-C2a/b/c/d riporta la riga:
```
S1[ord=(m_t,m_x); α={…}; lin=…; P(τ,ξ)=…; tipo=…; coeff=…; scal/sys=…]
S2[Ω=…; dati=…; BC=…]  S3[V(P)=…; vel=finita/inf]  S4[transl=sì/no; scaling s=…; cons=…]
S5[trasf=…; K=…; spettro=…; base=num/cont; duale=…]  S6[spazio=…; regolarizz=…; backward=sì/no]
S7[A_s/A_a; dissip=…; hamilt=…]  S8[locale/nonlocale; simbolo=…]  S10[ε=…]  S11[decad=…]
S12[NL=…; linearizz=…]  S13[identificabile=…; dati minimi=…]
```
S9, S14, S15 sono facoltativi (tag ◇/○).

## 6. Coppie gemelle serie 1 ↔ serie 2 (NON sono doppioni)

La regola "ogni item una sola volta" è rispettata; ma 22 coppie trattano lo stesso tema da due lati: **famiglia/metodo (scheda)** vs **attributo (colonna)**. Chi compila una scheda della serie 1 riempie la colonna gemella.

| Serie 1 (Asse 1–3, scheda) | Serie 2 (Asse 4, colonna) | Tema |
|---|---|---|
| C2.17 | C2.19′ | simbolo principale, tipo |
| C2.13 | C2.35′, C2.36′ | Sturm–Liouville ↔ spettro, completezza |
| C2.14 | C2.33′ | trasformate |
| C2.36 | C2.34′ | Green/fondamentali ↔ strutture di nucleo |
| C2.48 | C2.58′, C2.67′ | perturbazioni |
| C2.49 | C2.32′ | scaling |
| C2.50 | C2.31′, C2.66′ | simmetrie/riduzioni |
| C2.51 | C2.45′ | variazionale |
| C2.52 | C2.37′, C2.38′ | spazi, regolarità |
| C2.53 | C2.48′, C2.35′ | semigruppi, dissipatività |
| C2.54 | C2.40′, C2.41′, C2.42′ | buona posizione, energia |
| C2.55 | C2.26′, C2.25′ | condizioni al bordo/iniziali |
| C2.56 | C2.51′, C2.52′ | coordinate/geometria |
| C2.60 | C2.69′ | identificazione |
| C2.24 | C2.30′, C2.62′, C2.63′ | conservazione, shock, entropia |
| C2.44 | C2.61′ | onde viaggianti |
| C2.45, C2.16 | C2.65′ | integrabilità |
| C2.43 | C2.54′ | frontiere libere |
| C2.41 | C2.56′ | stocastico |
| C2.37, C2.38 | C2.49′ | nonlocale/frazionario |
| C2.58, C2.59 | C2.72′–C2.75′ | numerico (tutti in S14) |
| C2.22 | C2.22′, C2.29′ | sistemi iperbolici, causalità |

## 7. Controllo critico (scientific-critical-thinking)
1. **Ortogonalità.** Gli attributi non sono indipendenti: `coeff=costanti` (S1) ⇔ `transl=sì` (S4) ⇔ `trasf=Fourier` diagonalizza (S5). Nelle schede basta dichiararne uno e derivare gli altri; segnalato come vincolo di coerenza.
2. **Item-metodo in un asse di attributi.** C2.58, C2.59 (serie 1) sono famiglie di metodi numerici, non attributi: la loro presenza in S14 è coerente con il tag ○ ma non producono colonne.
3. **Collocazioni discutibili** (non spostate, conteggio invariato): C2.67′, C2.68′ (→ S10); C2.53′ singolarità (in parte S3: caustiche; in parte S1: coefficienti singolari); C2.23 tipo misto (in T8 ma è anche un attributo S1 `tipo=misto`).
4. **Rischio principale per G★.** La tassonomia classifica *equazioni*, mentre A6 chiede *componenti* (termini). Il ponte è la matrice `components_matrix.md`: le famiglie sono **combinazioni** di poche righe.
