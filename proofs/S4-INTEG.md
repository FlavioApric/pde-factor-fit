# PROOF_PACKAGE — S4-INTEG (Fase 4) · lemmi di trasporto · 26/10/2026

Autore: S4-INTEG. Skill caricate (lettura integrale dei SKILL.md, nessuno script `_vendor` eseguito): `skills-local/session-protocol` (per prima), `skills-local/claim-lifecycle`, `_vendor/Auto-claude-code-research-in-sleep/skills/proof-writer` (struttura Claim/Status/Assumptions/Strategy/Dependency/Proof/Risks), `_vendor/math-skill` (modo proof: mappa, controesempi presto), `_vendor/scientific-agent-skills/skills/sympy` (solo verifica).
SymPy/mpmath: `sympy/integ_checks.py` → `sympy/integ_checks.out`, **35/35 OK** (aritmetica esatta in punti razionali dove possibile; il resto sono controlli numerici a 20–40 cifre, marcati).

**Stati usati.**
- **DIMOSTRATO-pronto**: prova completa qui, che usa solo fatti elementari o fatti classici elencati in §0 con il loro stato. In attesa dell'audit S-CHECK, quindi **non** ancora DIMOSTRATO.
- **CONDIZIONALE[F…]**: la riduzione è dimostrata, ma la conclusione dipende da fatti classici la cui fonte non è stata letta.
- **CON-FONTE**: enunciato identico a un teorema pubblicato e verificato.
- **FALSO**: c'è un controesempio verificato.

Per ogni lemma dichiaro la **riduzione classica** (DEVIL-4 O3) e il **modello di dato e il dominio** (O4). Modelli M1/M2/M3 = formula chiusa / getto in un punto / u nota esattamente su Ω.

**Avvertenza O1.** Nessuno degli "E_int" di questo pacchetto (E^trop in F4LIN-T2, E^NL in F4L-P3, u − Σ 1-solitoni in Hirota) è l'E_int^add di A9 (NOTAZIONE v3). Sono strumenti, non risposte al punto 1 di G★′-NL.

---
## §0. Fatti importati (con stato)
| ID | enunciato | fonte | stato della fonte |
|---|---|---|---|
| F-H | Per u₀ ∈ L¹(ℝ) (o misura finita) e ν > 0, u = −2νφ_x/φ con φ = G_ν(t)∗e^{−U₀/2ν} è la soluzione (unica nella classe di Hopf) di u_t + uu_x = νu_xx con dato u₀ | Hopf, CPAM 3 (1950) 201–230; Cole, QAM 9 (1951) 225–236 | metadati verificati (AUDIT-4 r. 23a–b); enunciato **non letto** |
| F-N | Sull'intervallo (0,L), il nucleo di Neumann del calore G_N(t,x,y) è ≥ 0 e ∫₀^L G_N dy = 1; il problema di Dirichlet omogeneo per Burgers viscoso con dato L¹ ha soluzione unica, classica per t > 0 | principio del massimo, teoria parabolica standard | classico, nessuna fonte letta |
| F-SS | (Saut–Scheurer 1987, Thm 1.1, via Kenig–Ponce–Vega arXiv:math/0009065 §1) Sia w soluzione di ∂_t w + ∂_x³w + Σ_{j≤2} r_j(x,t)∂_x^j w = 0 in (a,b)×(t₁,t₂), con r_j ∈ L^∞_t L²_loc. Se w = 0 su un aperto ω, allora w = 0 nelle componenti orizzontali di ω | JDE 66 (1987) 118–139 | **secondaria** (AUDIT-4 r. 7) |
| F-C | I flussi K_n della gerarchia KdV commutano: K_m′[u]K_n[u] = K_n′[u]K_m[u] per ogni u | Lax 1968; Olver cap. 5 | classico, non letto |
| F-MS | Per k_j > 0 distinti, il multi-solitone u = 2∂_x² log f (f di §1.3) soddisfa, come identità in (x, c), K_n[u] = −Σ_j k_j^{2n+1} ∂u/∂c_j per ogni n ≥ 0 (N-solitone simultaneo di tutta la gerarchia) | Hirota; Sato / Date–Jimbo–Kashiwara–Miwa | non letto; **V-ex** qui per N ≤ 2, n ≤ 2 (integ_checks) |
| F1 | Se u(s) è una soluzione di u_s = K_d[u] nella classe di Faddeev, allora κ_j sono costanti, r(k,s) = r(k,0)e^{−2ik q_d(−4k²)s}, c_j(s) = c_j(0)e^{−2κ_j q_d(4κ_j²)s} (a meno della convenzione di segno, che non conta) | Lax 1968; AKNS 1974; Ablowitz–Segur 1981 | non letto |
| F2 | La mappa diretta di scattering v ↦ (r, {κ_j, c_j}) è iniettiva sulla classe di Faddeev; r è continuo su (0,∞); gli autovalori sono finiti e semplici; c_j ≠ 0 | Deift–Trubowitz 1979; Marchenko 1986 | metadati verificati, testo non letto |
| F3 | Esistenza e unicità locale per u_s = K_d[u] nella classe di Faddeev (via IST) | Deift–Trubowitz; letteratura IST | non letto |
| F4 | r ≡ 0 ⟺ v è un multi-solitone | Kay–Moses 1956 | abstract verificato (costruzione) |

---
## §1. Integrabili (F4-INT)

### §1.1 [INT-T1] KdV nella classe 𝓗_M
**Notazione.** Uso KdV u_t + 6uu_x + u_xxx = 0. K_0 = −u_x e K_{n+1} = 𝓡K_n, con 𝓡 = ∂_x² + 4u + 2u_x∂_x^{−1}. Questo dà K_1 = −(u_xxx + 6uu_x) e K_2 = −(u_5x + 10uu_xxx + 20u_xu_xx + 30u²u_x); la parte lineare di K_n è −∂_x^{2n+1}. Per d ∈ ℝ^{M+1} pongo K_d := Σ_n d_nK_n e q_d(λ) := Σ_n d_nλ^n. La classe è 𝓗_M := {u_t = K_c[u] : c ∈ ℝ^{M+1}}. L'insieme spettrale è Λ(v) := {4κ_j²} ∪ {−4k² : k > 0, r(k) ≠ 0} ⊂ ℝ.

**Enunciato.** Siano I un intervallo aperto e Ω ⊂ I×ℝ un aperto con π_t(Ω) = I (ogni fetta {t}×ℝ incontra Ω). Sia u ∈ C^∞(I×ℝ) reale, soluzione di u_t = K_c[u] su I×ℝ per un c ∈ ℝ^{M+1}, con u(t,·) nella classe di Faddeev (∫(1+|x|)|u| < ∞, insieme a sufficienti derivate). Il dato è u|_Ω (modello M3, oppure M1 se u è in forma chiusa), con la conoscenza a priori "u è restrizione di una soluzione di 𝓗_M di questa classe". Definisco 𝒜(u) := {c′ ∈ ℝ^{M+1} : u_t = K_{c′}[u] su Ω} e 𝒩 := {d : q_d|_{Λ(u(t,·))} = 0}.
- **(A) Riduzione (DIMOSTRATO-pronto).** Se vale (UC) "K_d[u] = 0 su Ω ⇒ K_d[u] = 0 su I×ℝ", allora 𝒜(u) = c + {d : K_d[u(t,·)] ≡ 0 per ogni t ∈ I}.
- **(UC) Continuazione unica.**
  - (UC-1) **DIMOSTRATO-pronto modulo F-C e F-SS**: vale se il flusso **vero** ha ordine **esattamente** 3 (c_1 ≠ 0, c_n = 0 per n ≥ 2; c_1 ≠ 0 è necessario, [fix UC-1b, S5-FIX2]), per **qualunque** M della classe d'ipotesi.
  - (UC-ω) **DIMOSTRATO-pronto**: vale se u è reale-analitica su I×ℝ (p.es. multi-solitoni).
  - Negli altri casi (flusso vero d'ordine ≥ 5, u non analitica) è **APERTA**: nessuna fonte trovata (AUDIT-4 r. 7).
- **(B) Multi-solitoni, DIMOSTRATO-pronto modulo F-MS.** Sia u l'N-solitone con k_j > 0 distinti (soluzione di K_1, analitica). Allora 𝒩 = {d : q_d(k_j²) = 0, j = 1..N}, quindi dim 𝒩 = max(0, M+1−N). In particolare u identifica il flusso in 𝓗_M ⟺ M ≤ N−1; in 𝓗_N vale l'equazione stazionaria di Novikov K_d[u] = 0 con q_d = Π_j(λ − k_j²).
- **(C) Caso generale, CONDIZIONALE[F1, F2, F3, F4].** K_d[v] = 0 ⟺ q_d|_{Λ(v)} = 0. Quindi:
  - (a) dim 𝒩 = max(0, M+1−|Λ|), e u identifica in 𝓗_M ⟺ |Λ(u)| ≥ M+1;
  - (b) u identifica in 𝓗_∞ ⟺ Λ è infinito ⟺ r ≢ 0 ⟺ u(t,·) non è un multi-solitone. [fix C-1, S5-FIX2] Qui 𝓗_∞ := ∪_M 𝓗_M (polinomi q_d di grado arbitrario ma finito).

**Riduzione classica (O3).** (B) e (C) sono il fatto che i flussi della gerarchia agiscono sui dati di scattering come moltiplicatori diagonali (Lax/AKNS; stazionarie di Novikov), più il conteggio di Vandermonde per i polinomi di grado ≤ M che si annullano su un insieme finito. Il contributo è solo la formulazione come teorema di identificazione (trasposizione di C3-T4) e la precisazione (UC-1).

**Prova.**
*(A).* Se c′ ∈ 𝒜(u), allora su Ω vale K_{c′}[u] = u_t = K_c[u], quindi K_d[u] = 0 su Ω con d := c′ − c (K_d è lineare in d). Per (UC), K_d[u] = 0 su I×ℝ, cioè K_d[u(t,·)] = 0 per ogni t. Viceversa, se K_d[u(t,·)] ≡ 0 per ogni t, allora u_t = K_c[u] = K_{c+d}[u] su Ω. ∎

*(UC-ω).* Se u è analitica su I×ℝ, anche K_d[u] lo è: è un polinomio differenziale a coefficienti costanti in u. I×ℝ è connesso e Ω è un aperto non vuoto, quindi per il principio d'identità K_d[u] = 0 su Ω implica K_d[u] = 0 su I×ℝ. ∎

*(UC-1).* Pongo w := K_d[u]. Su I×ℝ vale ∂_t w = K_d′[u]u_t = K_d′[u]K_c[u] = K_c′[u]K_d[u] = K_c′[u]w per F-C (bilinearità in c, d). Con c = (c_0, c_1, 0, …) si ha
K_c′[u]w = −c_0w_x − c_1(w_xxx + 6uw_x + 6u_xw),
quindi w_t + c_1w_xxx + (c_0 + 6c_1u)w_x + 6c_1u_xw = 0.
Riduco alla forma di F-SS:
- se c_1 > 0, cambio il tempo con s = c_1t;
- se c_1 < 0, pongo prima x̃ = −x (il segno di ∂_x³ cambia, ∂_x³ → −∂_x̃³) e poi s = |c_1|t.

Si ottiene ∂_s w + ∂_x̃³w + r_1w_x̃ + r_0w = 0 con r_1, r_0 lisci, quindi in L^∞_t L²_loc su ogni rettangolo limitato. Fisso un rettangolo (a,b)×(t₁,t₂) ⊂ I×ℝ che contiene un aperto ω ⊂ Ω non vuoto. F-SS dà w = 0 nelle componenti orizzontali di ω. Facendo crescere (a,b) e ricoprendo I con le proiezioni (π_t(Ω) = I), si ottiene w = 0 su I×ℝ. ∎ (Rischio R1: interpretazione di "componente orizzontale".)
**[fix UC-1a, S5-FIX2] Esaustione con palle e rettangoli (chiude R1 senza la forma "componenti orizzontali di ω non connesso").** Per ogni palla B ⊂ Ω (connessa) e ogni rettangolo (a,b)×(t₁,t₂) ⊃ B contenuto in I×ℝ, F-SS dà w = 0 su (a,b)×π_t(B). Si fa a → −∞, b → +∞; poiché π_t(Ω) = I, le proiezioni π_t(B) di palle B centrate in punti di Ω ricoprono I (fetta per fetta). Quindi w = 0 su I×ℝ; la conclusione è identica. Regolarità richiesta da F-SS: w = K_d[u] ∈ C^∞, quindi qualunque classe (p.es. L²_tH³_loc) è soddisfatta.
**[fix UC-1b, S5-FIX2] Necessità di c_1 ≠ 0 (flusso vero d'ordine esattamente 3).** Se il flusso vero è la sola traslazione (c_1 = 0), w_t + c_0w_x = 0 è di trasporto e la UC fallisce. Controesempio: u = u₀(x − c_0t) con u₀ liscia nella classe di Faddeev e u₀ ≡ 0 su (−1,1), Ω = {|x − c_0t| < ½} (π_t(Ω) = I): u ≡ 0 su Ω, quindi K_d[u] = 0 su Ω per ogni d, mentre K_0[u] ≢ 0 su I×ℝ (S-CHECK-9 red team).

*(B).* Per F-MS, K_d[u] = Σ_n d_nK_n[u] = −Σ_j k_j q_d(k_j²) ∂u/∂c_j. Resta da vedere che ∂u/∂c_1, …, ∂u/∂c_N sono linearmente indipendenti come funzioni di x, a t fissato. Allora K_d[u] = 0 ⟺ k_jq_d(k_j²) = 0 per ogni j ⟺ q_d(k_j²) = 0 (k_j > 0). Il conteggio è Vandermonde: i k_j² sono distinti e i polinomi di grado ≤ M che si annullano su N punti distinti formano uno spazio di dimensione max(0, M+1−N).

*Lemma B1 (indipendenza).* Supponiamo Σ_j a_j∂u/∂c_j ≡ 0 in x. Poiché u = 2∂_x² log f, si ha Σ_j a_j∂_{c_j} log f = αx + β per costanti α, β. Scrivo f = Σ_{S⊆[N]} a_S E^S con E^S := Π_{i∈S}E_i e a_S := Π_{i<j∈S}A_ij > 0. Allora ∂_{c_j}f = Σ_{S∋j} a_S E^S.
- Per x → −∞ tutti gli E_i → 0 esponenzialmente (k_i > 0), quindi f → 1 e ∂_{c_j} log f = E_j(1 + O(max_i E_i)).
- Il membro sinistro tende a 0, quindi αx + β → 0, cioè α = β = 0.
- Se non tutti gli a_j sono nulli, sia j₀ l'indice con k_{j₀} minimo fra quelli con a_j ≠ 0. Divido per E_{j₀}: a_{j₀} + Σ_{j≠j₀, a_j≠0} a_j E_j/E_{j₀} + O(max_i E_i) = 0. Ogni E_j/E_{j₀} = e^{(k_j − k_{j₀})x + cost} → 0, quindi a_{j₀} = 0: contraddizione. ∎

L'equazione di Novikov segue scegliendo q_d = Π_j(λ − k_j²), di grado N. (V-ex: K_0, K_1, K_2 contro −Σ k_j^{2n+1}∂_{c_j}u per N = 1, 2; Novikov 4K_0 − 5K_1 + K_2 = 0 per k = (1,2); Wronskiano di ∂_{c_1}u, ∂_{c_2}u ≠ 0.) ∎

*(C).* Sia v = u(t,·) e d fissato.
- (⇒) Se K_d[v] = 0, la funzione costante u(s) ≡ v risolve u_s = K_d[u]. Per F1 i suoi dati di scattering soddisfano r(k) = r(k)e^{−2ikq_d(−4k²)s} e c_j = c_je^{−2κ_jq_d(4κ_j²)s} per ogni s. Poiché c_j ≠ 0 (F2), si ha q_d(4κ_j²) = 0; e dove r(k) ≠ 0 (k > 0) si ha q_d(−4k²) = 0. Cioè q_d|_Λ = 0.
- (⇐) Se q_d|_Λ = 0, sia u(s) la soluzione di u_s = K_d[u] con u(0) = v (F3). Per F1 i suoi dati di scattering sono costanti in s, perché ogni moltiplicatore vale 1 dove il dato è non nullo. Per l'iniettività (F2), u(s) = v per ogni s, quindi K_d[v] = ∂_su|_{s=0} = 0.

Conteggio (a): Λ ⊂ ℝ è finito oppure no; i punti 4κ_j² > 0 e −4k² < 0 sono distinti fra loro. Se |Λ| = L ≤ M+1, Vandermonde dà dim 𝒩 = M+1−L; se L > M+1, dà 0. Poi si applica (A). Λ non dipende da t (|r| e κ_j sono invarianti per F1).
(b): r è continuo (F2); se r(k₀) ≠ 0, allora r ≠ 0 su un intervallo, quindi Λ è infinito. Se r ≡ 0, Λ è finito (numero finito di autovalori, F2) e v è un multi-solitone (F4). u identifica in 𝓗_∞ ⟺ identifica in ogni 𝓗_M ⟺ |Λ| ≥ M+1 per ogni M ⟺ Λ è infinito. ∎

**Stato.**
- (A), (UC-ω), Lemma B1: DIMOSTRATO-pronto.
- (UC-1): DIMOSTRATO-pronto modulo F-C e F-SS (fonte secondaria).
- (B): DIMOSTRATO-pronto modulo F-MS (V-ex).
- (C): CONDIZIONALE[F1–F4].
- Nessun FALSO.

**Correzione rispetto a CIT-AUDIT-4.** Saut–Scheurer non limita la **classe d'ipotesi** M. Limita l'ordine del **flusso vero**: w = K_d[u] risolve la linearizzazione del flusso vero, per commutazione. Quindi INT-T1 su Ω limitato vale per ogni dato KdV (flusso vero K_1, più eventuale traslazione), in qualunque 𝓗_M. Resta aperto solo per dati che risolvono flussi superiori e non sono analitici.

**Limite O4.** Λ(u) è definito dalla continuazione di u su I×ℝ. Anche quando la UC vale, la mappa u|_Ω ↦ Λ(u) non è stabile: la continuazione unica di Saut–Scheurer non dà stime. INT-T1 è quindi un teorema d'identificabilità con dato esatto (M1/M3), non un criterio certificabile con dati finiti.

### §1.2 [INT-T2] NLS in 𝓗_M^{NLS} — CONDIZIONALE
**Enunciato.** Focusing iq_t + q_xx + 2|q|²q = 0. I flussi a coefficienti reali sono T_0 = iq, T_1 = q_x, T_2 = i(q_xx + 2|q|²q), T_3 = −(q_xxx + 6|q|²q_x), … . Λ(q) := {k ∈ ℝ : ρ(k) ≠ 0} ∪ {ζ_j, ζ̄_j}. Sotto i fatti di scattering di Zakharov–Shabat analoghi a F1–F3 (iniettività solo nella classe generica: Beals–Coifman 1984, Zhou 1989, non letti) e con (UC) su Ω: l'ambiguità in 𝓗_M è max(0, M+1−|Λ|). I ζ_j non reali contano doppio, perché un polinomio reale nullo in ζ_j lo è anche in ζ̄_j.

**Prova.** Identica a INT-T1 (A)+(C): reduction e conteggio con polinomi **reali** di grado ≤ M nulli su Λ ⊂ ℂ chiuso per coniugio.

**Stato.** CONDIZIONALE[F1–F3 per ZS, UC]. Non porto a DIMOSTRATO-pronto neppure la parte multi-solitonica: servirebbero l'analogo di F-MS per NLS e l'indipendenza reale delle 2N direzioni (Re c_j, Im c_j), non scritte in questa sessione corta. V-ex di F4-INT (int_nls 9/9) invariato.

**UC.** Per multi-solitoni e breather vale (UC-ω), perché q è analitica. Per dati generali su Ω limitato non ho una fonte: la UC per la linearizzazione di NLS non è verificata.

### §1.3 [Hirota: INT-P5, INT-P6] E_int a coppie e ∫E_int = 0
**Enunciato.** Siano N ≥ 1, k_1, …, k_N > 0 distinti, c_i ∈ ℝ, E_i := e^{η_i} con η_i = k_ix − k_i³t + c_i, A_ij := ((k_i − k_j)/(k_i + k_j))² ∈ (0,1) e
f := Σ_{S⊆[N]} a_S E^S, con a_S := Π_{i<j∈S}A_ij.
Pongo u := 2∂_x² log f, u_i^{(1)} := 2∂_x² log(1+E_i), E_int := u − Σ_iu_i^{(1)}, p_i := E_i/(1+E_i).
Allora, a t fissato:
- (a) f = det(I + C), con C_ij = √(E_iE_j)·2√(k_ik_j)/(k_i+k_j). La matrice I + C è definita positiva.
- (b) E_int = 2∂_x² log Z, con Z := f/Π_i(1+E_i) = Σ_μ a_μ Π_ip_i^{μ_i}(1−p_i)^{1−μ_i} = 𝔼_μ[Π_{i<j}A_ij^{μ_iμ_j}] (μ_i ~ Bernoulli(p_i) indipendenti). Interazione **a coppie**: i cumulanti d'interazione b_S := Σ_{T⊆S}(−1)^{|S∖T|} log a_T valgono 0 per |S| ≠ 2 e b_{ij} = log A_ij.
- (c) Per N ≥ 2, E_int(t,·) ≢ 0.
- (d) [INT-P6] E_int ∈ L¹(ℝ) e ∫_ℝ E_int dx = 0; inoltre ∫_ℝ u dx = 2Σ_ik_i.
- (e) Il valore di E_int in un punto costa O(N³) operazioni: una fattorizzazione di I + C più le formule di Jacobi.

Il fatto che u risolva KdV è il teorema di Hirota 1971 (PRL 27, 1192; metadati verificati) e **non** è usato in (a)–(e): sono identità sulla funzione f.

**Modello e dominio.** M1 (formula chiusa), x ∈ ℝ a t fissato. (d) è intrinsecamente su ℝ: su un intervallo limitato ∫_a^b E_int = 2[(log Z)_x]_a^b ≠ 0 in generale, ma è O(e^{−k_min·min(|a|,|b|)}) se le fasi stanno dentro (a,b).

**Riduzione classica.**
- (a) è il determinante di Cauchy.
- (b) è la lettura "gas reticolare / Ising" del τ di Hirota (Loutsenko–Spiridonov, SIGMA 3 (2007) 059; attribuzione corretta da AUDIT-4, testo non letto).
- (c) e (d) sono limiti elementari.

Nessuna novità rivendicata.

**Prova.**
*(a).* det(I + C) = Σ_S det C_S (sviluppo nei minori principali). Ho C_S = D_S K_S D_S con D = diag(√E_i) e K_ij = 2√(k_ik_j)/(k_i+k_j). Quindi det C_S = E^S·Π_{i∈S}2k_i·det[1/(k_i+k_j)]_S. Per Cauchy, det[1/(k_i+k_j)]_S = Π_{i<j∈S}(k_i−k_j)² / Π_{i,j∈S}(k_i+k_j). Il denominatore è Π_{i∈S}2k_i·Π_{i<j∈S}(k_i+k_j)², quindi det C_S = E^S·Π_{i<j∈S}A_ij = a_SE^S.
Positività: K_ij = ∫_0^∞ 2√(k_ik_j)e^{−(k_i+k_j)s}ds è una matrice di Gram, quindi semidefinita positiva. Allora C = DKD ⪰ 0 e I + C ≻ 0. (V-ex N = 3, simbolico.)

*(b).* Π_iE_i^{μ_i}/Π_i(1+E_i) = Π_ip_i^{μ_i}(1−p_i)^{1−μ_i}, da cui la formula di Z. Inoltre u − Σu_i^{(1)} = 2∂_x²[log f − Σ log(1+E_i)] = 2∂_x² log Z.
Cumulanti: log a_T = Σ_{\{i,j\}⊆T} log A_ij = Σ_{P∈\binom{[N]}{2}} 1[P⊆T]·log A_P. L'inversione di Möbius di T ↦ 1[P⊆T] è l'indicatrice di S = P, quindi b_S = log A_S se |S| = 2 e 0 altrimenti. (V-ex N = 3.)

*(c), (d).* Z è combinazione convessa dei numeri a_μ ∈ [Π_{i<j}A_ij, 1], quindi 0 < Π_{i<j}A_ij ≤ Z ≤ 1.
- Per x → −∞, p_i → 0 e Z → a_∅ = 1. Per x → +∞, p_i → 1 e Z → a_{[N]} = Π_{i<j}A_ij.
- ∂_xp_i = k_ip_i(1−p_i) e ogni ∂_x^m p_i è O(min(p_i, 1−p_i)), che decade esponenzialmente a ±∞. Quindi Z_x, Z_xx → 0 esponenzialmente.
- Con Z ≥ ΠA > 0: (log Z)_x → 0 a ±∞ e (log Z)_xx decade esponenzialmente, quindi E_int ∈ L¹. Allora ∫_ℝ E_int = 2[(log Z)_x]_{−∞}^{+∞} = 0.
- Per ∫u: (log f)_x → 0 per x → −∞; per x → +∞, f = a_{[N]}E^{[N]}(1 + O(e^{−k_min x})) e così pure f_x/(Σk_i), quindi (log f)_x → Σk_i.
- (c): se E_int ≡ 0, allora (log Z)_x è costante; poiché tende a 0, è nulla. Ma allora log Z è costante, mentre i suoi limiti a ±∞ sono 0 e Σ_{i<j} log A_ij < 0 (k distinti, N ≥ 2). Contraddizione. (V-ex N = 3: ∫E_int ≈ 0 con errore < 10⁻¹², E_int(0) ≠ 0, Z(+∞) = ΠA.)

*(e).* M := I + C(x) è definita positiva (Cholesky in O(N³)). M′ e M″ si ottengono moltiplicando C_ij per (k_i+k_j)/2 e ((k_i+k_j)/2)². Si ha (log f)″ = tr(M^{−1}M″) − tr((M^{−1}M′)²), O(N³). La somma Σ log(1+E_i) costa O(N). ∎

**Stato.** (a)–(e): DIMOSTRATO-pronto. Nota d'oggetto: questo E_int è un'interazione fra **solitoni**, non fra termini (O1).

---
## §2. [F4LIN-T2] Stima di E^trop in ν (F4-LIN)
**Notazione.** Burgers_ν[u] := u_t + uu_x − νu_xx. Per N ≥ 1, pendenze c_1 > … > c_N e costanti β_i ∈ ℝ pongo
- S_i(t,x) := c_ix − c_i²t/2 − β_i;
- ψ^ν := −2ν log Σ_ie^{−S_i/2ν}, ψ⁰ := min_iS_i;
- u^ν := ∂_xψ^ν, u⁰ := ∂_xψ⁰ (q.o.), E^trop := u^ν − u⁰.

**Enunciato.**
- (0) u^ν risolve Burgers_ν. ψ⁰ è la soluzione di Hopf–Lax di ψ_t + ψ_x²/2 = 0 con dato concavo lineare a tratti ψ⁰(0,x) = min_i(c_ix − β_i).
- (i) −2ν log N ≤ ψ^ν − ψ⁰ ≤ 0 su ℝ²_{t≥0}, quindi ‖E^trop(t)‖_{W^{−1,∞}(ℝ)} ≤ 2ν log N uniformemente in t, β, N.
- (ii) Caso N = 2, Δ := c_1 − c_2 > 0, y := x − x_s, x_s := (c_1+c_2)t/2 + (β_1−β_2)/Δ. Allora:
  - u^ν = (c_1+c_2)/2 − (Δ/2)tanh(Δy/4ν) e E^trop = (Δ/2)F(Δy/4ν), con F := sgn − tanh;
  - ‖E^trop‖_{L¹(ℝ)} = 4ν ln 2, indipendente da Δ e da t;
  - ‖E^trop‖²_{L²} = 4νΔ(ln 2 − ½) e ‖E^trop‖_{L^p} = C_pΔ^{1−1/p}ν^{1/p};
  - ‖E^trop‖_{Ḣ^s} = C_sΔ^{s+1/2}ν^{1/2−s} per −3/2 < s < 1/2, mentre E^trop ∉ Ḣ^s per s ≥ ½;
  - |u^ν|²_{Ḣ¹} = Δ³/12ν;
  - versione su intervallo: ∫_{|y|>η}|E^trop| ≤ 4νe^{−Δη/2ν}.
- (iii) Sia N ≥ 3 e t fissato. Suppongo che l'inviluppo inferiore x ↦ min_iS_i(t,x) non abbia punti tripli (nessun x in cui tre rette realizzano il minimo; "nessuna collisione a t"). Sia K(t) il numero dei suoi punti di rottura (shock). Allora
|‖E^trop(t)‖_{L¹(ℝ)} − 4ν ln 2·K(t)| ≤ 4νK(t)e^{−δ/2ν} + C·e^{−δ/4ν},
con δ := inf_x(S_{(3)} − S_{(1)}) > 0 (statistiche d'ordine a t fissato) e C che dipende da (c, β, t, N) e non da ν ∈ (0,1].
**[fix L-3, S5-FIX2] Versione rafforzata (S-CHECK-9 §5.2 L.7):** |‖E^trop(t)‖_{L¹(ℝ)} − 4ν ln 2·K(t)| ≤ (4ν(K−1) + C′)e^{−δ/2ν}, con C′ dipendente da (c, β, t, N) e non da ν ∈ (0,1]. L'enunciato sopra resta vero (è più debole).

**Modello e dominio.** M1 (miscela finita di onde, in forma chiusa), x ∈ ℝ a t fissato. Su Ω limitato: (ii) e (iii) restano valide su ogni intervallo che contiene gli shock a distanza η dai bordi, con un errore esponenzialmente piccolo (ultima voce di (ii)).

**Riduzione classica.**
- (i) è la disuguaglianza log-sum-exp, cioè la dequantizzazione di Maslov.
- (ii) è il profilo dello shock viscoso (tanh, classico), con ∫_0^∞(1 − tanh) = ln 2. Wang 1998 (SIAM J. Math. Anal. 30, 38–52) studia lo stesso errore L¹ via Hopf–Cole; la costante potrebbe comparirvi (testo non letto).
- (iii) è un'analisi di Laplace del log-sum-exp.

La costante 4ν ln 2 è **elementare, non un contributo**.

**Prova.**
*(0).* φ := Σ_ie^{−S_i/2ν} risolve φ_t = νφ_xx, perché ogni addendo lo fa: (e^{−S_i/2ν})_t = (c_i²/4ν)e^{−S_i/2ν} = ν(e^{−S_i/2ν})_xx. Poi u^ν = −2νφ_x/φ e l'identità di Cole–Hopf (ALG-P4, §3.4) danno Burgers_ν[u^ν] = −2ν∂_x((φ_t − νφ_xx)/φ) = 0.
Hopf–Lax: min_y{min_i(c_iy − β_i) + (x−y)²/2t} = min_i min_y(…) = min_i(c_ix − c_i²t/2 − β_i), con il minimo in y = x − c_it. L'identificazione di u⁰ con la soluzione entropica di Kružkov è Lax–Oleinik (Evans §3.4, **numero non verificato**) e non serve per (i)–(iii).

*(i).* Sia m := min_iS_i. Allora e^{−m/2ν} ≤ Σ_ie^{−S_i/2ν} ≤ Ne^{−m/2ν}; si applica −2ν log. Poiché E^trop = ∂_x(ψ^ν − ψ⁰) con ψ^ν − ψ⁰ ∈ L^∞, la norma quoziente in W^{−1,∞} (inf ‖g‖_∞ su g con g′ = E) è ≤ ‖ψ^ν − ψ⁰‖_∞ ≤ 2ν log N.

*(ii).* S_1 − S_2 = Δ(x − x_s), e i pesi sono w_1 = (1 + e^{Δy/2ν})^{−1}, w_2 = 1 − w_1. Quindi u^ν = c_2 + Δw_1 = (c_1+c_2)/2 − (Δ/2)tanh(Δy/4ν). Inoltre u⁰ = c_1 per y < 0 e c_2 per y > 0, cioè (c_1+c_2)/2 − (Δ/2)sgn y. Da qui E^trop = (Δ/2)F(Δy/4ν).
- L¹: con z = Δy/4ν, ‖E‖_{L¹} = (Δ/2)(4ν/Δ)·2∫_0^∞(1 − tanh z)dz = 4ν·lim_{Z→∞}(Z − ln cosh Z) = 4ν ln 2.
- L²: (1 − tanh)² = 2 − 2tanh − sech², con integrale su (0,∞) pari a 2ln 2 − 1. Quindi ‖E‖²_{L²} = (Δ²/4)(4ν/Δ)·2(2ln2 − 1) = 4νΔ(ln 2 − ½).
- L^p: per scala, ‖E‖_p^p = (Δ/2)^p(4ν/Δ)‖F‖_p^p.
- Ḣ^s: Ê(κ) = 2νF̂(4νκ/Δ), quindi ‖E‖²_{Ḣ^s} = 4ν²(Δ/4ν)^{2s+1}∫|η|^{2s}|F̂(η)|²dη. F è dispari, in L¹ con decadimento esponenziale, e ha un salto in 0. Ne segue F̂(η) = O(η) in 0 e F̂(η) ~ (const)/η all'infinito (la trasformata di tanh, in valore principale, cancella 2/(iη) a meno di un termine che decade esponenzialmente). L'integrale converge ⟺ 2s + 2 > −1 e 2s − 2 < −1 ⟺ −3/2 < s < ½. Per s ≥ ½ diverge.
  **[fix L-1, S5-FIX2] Forma chiusa (chiude R5):** F̂(η) = i(π csch(πη/2) − 2/η) (trasformate in valore principale di sgn e tanh; S-CHECK-9: verificata in 3 punti a 15 cifre). Quindi F̂(η) = −iπ²η/12 + O(η³) in 0 e F̂(η) = −2i/η + O(e^{−πη/2}) all'infinito: l'intervallo −3/2 < s < ½ è dimostrato, non solo motivato.
- Ḣ¹: ∫(u^ν_x)² = (Δ²/4)(Δ/4ν)²∫sech⁴(Δy/4ν)dy = (Δ⁴/64ν²)(4ν/Δ)(4/3) = Δ³/12ν.
- Coda: 1 − tanh z = 2/(e^{2z}+1) ≤ 2e^{−2z}, quindi |E| ≤ Δe^{−Δ|y|/2ν} e ∫_{|y|>η}|E| ≤ 4νe^{−Δη/2ν}.

(V-ex: profilo, Burgers, L¹, L², Ḣ¹ esatti in SymPy.)

*(iii).* A t fissato pongo D := ψ^ν − ψ⁰ = −2ν log Φ, con Φ := Σ_ie^{−(S_i−m)/2ν} ≥ 1. D è lipschitziana con D′ = E^trop q.o., quindi ‖E^trop‖_{L¹} = TV(D). Siano g := S_{(2)} − S_{(1)} e h := S_{(3)} − S_{(1)}; scrivo Φ = 1 + e^{−g/2ν} + R, con 0 ≤ R ≤ (N−2)e^{−h/2ν}.

(1) δ > 0. h è continua e positiva ovunque: h(x) = 0 vorrebbe dire tre rette al minimo in x, cioè un punto triplo, escluso. Inoltre h(x) ≥ a|x| − b con a > 0, perché le pendenze sono distinte e per |x| grande le tre rette più basse si separano linearmente. Quindi δ = inf h > 0 è raggiunto, e h ≥ max(δ, a|x| − b).

(2) Struttura di g. Fra due rotture consecutive dell'inviluppo, S_{(1)} = S_a è una sola retta e S_{(2)} = min_{i≠a}S_i è concava e lineare a tratti. Quindi g è concava, lineare a tratti, con pendenze mai nulle (pendenze distinte), nulla agli estremi finiti dell'intervallo (rotture) e tendente a +∞ sugli intervalli illimitati. Su ogni intervallo interno g ha un solo massimo, in un punto angoloso dove S_{(2)} cambia retta, cioè dove S_{(2)} = S_{(3)}: lì g = h ≥ δ. Sui due intervalli illimitati g è monotona.

(3) D_2 := −2ν log(1 + e^{−g/2ν}) è funzione **crescente** di g [fix L-2, S5-FIX2: il testo diceva "decrescente"; dD_2/dg = e^{−g/2ν}/(1 + e^{−g/2ν}) > 0; conta solo la monotonia stretta, l'argomento non cambia], quindi ha gli stessi tratti di monotonia di g. Vale D_2 = −2ν ln 2 nelle rotture, D_2 → 0 a ±∞, e nei K−1 massimi interni |D_2| = 2ν log(1 + e^{−g_max/2ν}) ≤ 2νe^{−δ/2ν}. Sommando le variazioni sui 2K tratti monotoni:
TV(D_2) = 4νK ln 2 − 4ν·Σ_{max interni} log(1 + e^{−g_max/2ν}) ∈ [4νK ln 2 − 4ν(K−1)e^{−δ/2ν}, 4νK ln 2].

(4) D − D_2 = −2ν log(1 + R/(1 + e^{−g/2ν})). Questa funzione è continua (R, g, Φ sono continue anche dove le etichette (2), (3) si scambiano) e C¹ a tratti. Ha derivata |(D − D_2)′| ≤ 2ν(|R′| + R|g′|/2ν) ≤ C_c·Σ_{i∉\{(1),(2)\}}e^{−(S_i−m)/2ν} ≤ C_c(N−2)e^{−h/2ν}, con C_c := 2 max_{i,j}|c_i − c_j|. Allora TV(D − D_2) ≤ C_c(N−2)∫e^{−h/2ν} ≤ C_c(N−2)e^{−δ/4ν}∫e^{−h/4ν} ≤ C e^{−δ/4ν}, perché ∫e^{−max(δ, a|x|−b)/4ν}dx ≤ 2b/a + 8/a per ν ≤ 1.
**[fix L-3, S5-FIX2]** Stima migliore: spezzando in |x| ≤ (b+δ)/a (dove h ≥ δ) e il resto (dove h ≥ a|x| − b > δ), ∫e^{−h/2ν} ≤ (2(b+δ)/a + 4ν/a)e^{−δ/2ν}; quindi TV(D − D_2) ≤ C′e^{−δ/2ν} e, con (3), |‖E^trop‖_{L¹} − 4νK ln 2| ≤ (4ν(K−1) + C′)e^{−δ/2ν}.

(5) |TV(D) − TV(D_2)| ≤ TV(D − D_2). Si conclude. ∎
(Controllo numerico: N = 3, K = 2, δ = 2, t = 1: per ν = 0.05 l'errore è 1.8·10⁻⁵ ≤ e^{−δ/4ν} = 4.5·10⁻⁵; per ν = 0.02 è 2.2·10⁻¹² ≤ 1.4·10⁻¹¹.)
**[fix L-3, S5-FIX2] Correzione del controllo numerico (cifra segnalata da S-CHECK-9 come incompatibile).** Ricontrollato con mpmath (work/S5-FIX2/l3_check.py → l3_check.out; 40 cifre, quadratura spezzata in ±1, ±½, ±¼, 0): la cifra **1.8·10⁻⁵ è corretta** (1.816·10⁻⁵ per ν = 0.05; 2.22·10⁻¹² per ν = 0.02) e non è un errore di quadratura. L'errore è nel **δ dichiarato**: nella configurazione usata (c = (2, 0, −2), β = (0, 3, 0), t = 1, rotture in x = ±½) si ha **δ = 1**, non 2 (inf in x = 0, dove S_{(3)} − S_{(1)} = 2|x| + 1). I maggioranti stampati 4.5·10⁻⁵ e 1.4·10⁻¹¹ sono e^{−2/4ν} = e^{−δ/2ν} con δ = 1, cioè la stima rafforzata di L-3; rapporti errore/e^{−δ/2ν} = 0.40 (ν = 0.05), 0.16 (ν = 0.02), 0.79 (ν = 0.1), coerenti con il red team di S-CHECK-9 (§11). Lettura corretta: "N = 3, K = 2, δ = 1, t = 1: errore 1.8·10⁻⁵ ≤ e^{−δ/2ν} = 4.5·10⁻⁵ (ν = 0.05); 2.2·10⁻¹² ≤ 1.4·10⁻¹¹ (ν = 0.02)".

**Stato.** (0) (tranne l'identificazione entropica), (i), (ii), (iii): DIMOSTRATO-pronto. (iii) migliora il "+ o(ν)" della NOTE in un errore esponenzialmente piccolo. La costante **non** è uniforme vicino ai tempi di collisione (δ → 0). Nota d'oggetto (O1, domanda di S4-TERM): E^trop non è E_int^add di A9.

---
## §3. Algebra differenziale (F4-ALG) e sizigie (F4-HOR)
**Quadro.** ℂ{y} := ℂ[θy : θ = ∂_t^a∂_x^b] con derivazioni commutanti ∂_t, ∂_x e coefficienti costanti. Ω ⊂ ℝ² aperto connesso. Per u ∈ C^∞(Ω): ev_u(G) := G(u), I(u) := ker ev_u (ideale differenziale; radicale perché G^n(u) = 0 implica G(u) = 0). Equazione di evoluzione F := y_t − N con N ∈ A := ℂ[y_0, y_1, …] (y_k ≡ ∂_x^ky). Su A: D y_k := y_{k+1} e D_N y_k := D^kN. J_u := {p ∈ A : p(u, u_x, …) ≡ 0}.
**Modello e dominio (per tutto §3).** u nota esattamente su un aperto connesso Ω qualsiasi, limitato incluso (M3, o M1 se in forma chiusa). Gli enunciati sono locali: **nessun problema di dominio** (O4 soddisfatta nativamente). Limite: i criteri (trdeg = ∞, Ann = 0) non sono certificabili con dati finiti (analogo di C3-P1).

### §3.1 [ALG-L1] ℂ{y}/[F] ≅ A, [F] è primo
**Enunciato.** (i) [D, D_N] = 0 su A. (ii) ψ: ℂ{y} → A, ∂_t^a∂_x^b y ↦ D_N^aD^by_0, è un omomorfismo di anelli differenziali (∂_x ↦ D, ∂_t ↦ D_N), con ψ|_A = id e ker ψ = [F]. (iii) Quindi ℂ{y}/[F] ≅ A, che è un dominio, e [F] è primo.
**Riduzione classica.** È la forma normale dell'algebra dei polinomi differenziali di un'equazione di evoluzione (calcolo variazionale formale: Olver cap. 5; Sanders–Wang). Nota, non nuova.
**Prova.**
(i) [D, D_N] è una derivazione di A, quindi basta verificarla sui generatori: D_N(Dy_k) = D_Ny_{k+1} = D^{k+1}N = D(D^kN) = D(D_Ny_k).
(ii) ℂ{y} è l'anello dei polinomi nelle variabili libere θy, quindi ψ è ben definita assegnando le immagini dei generatori; D_N^aD^b non dipende dall'ordine, per (i). ψ∘∂_x e D∘ψ sono entrambe ψ-derivazioni ℂ{y} → A e coincidono sui generatori (ψ(∂_x∂_t^a∂_x^by) = D_N^aD^{b+1}y_0 = D ψ(∂_t^a∂_x^by)), quindi coincidono ovunque; lo stesso per ∂_t e D_N. ψ|_A = id perché ψ(∂_x^by) = y_b.
ker ψ ⊇ [F]: ψ(F) = D_Ny_0 − N = 0 e ker ψ è un ideale differenziale.
ker ψ ⊆ [F]: mostro G − ψ(G) ∈ [F] per ogni G.
- Sui generatori, per induzione su a. Per a = 0 è 0. Se θy − ψ(θy) ∈ [F], allora ∂_tθy ≡ ∂_tψ(θy) mod [F], perché [F] è differenziale. Inoltre, per p ∈ A, ∂_tp = Σ_k(∂p/∂y_k)∂_x^k(y_t) ≡ Σ_k(∂p/∂y_k)D^kN = D_Np mod [F], perché ∂_x^k(y_t − N) ∈ [F] e ∂_x^kN = D^kN. Con p = ψ(θy): ∂_tθy ≡ D_Nψ(θy) = ψ(∂_tθy). Le derivate in x sono analoghe (∂_x p = Dp per p ∈ A).
- La proprietà passa a somme e prodotti: G_1G_2 − ψG_1ψG_2 = (G_1 − ψG_1)G_2 + ψG_1(G_2 − ψG_2).
- Quindi ψ(G) = 0 implica G ∈ [F].

(iii) ψ è suriettiva (ψ|_A = id) e A è un anello di polinomi. ∎ (V-ex: [D, D_N] = 0 per Burgers e KdV su un polinomio di prova.)
**Stato.** DIMOSTRATO-pronto. Novità: nessuna.

### §3.2 [ALG-T1] Identificazione per evoluzioni (con u analitica in (c))
**Enunciato.** Sia u ∈ C^∞(Ω), Ω connesso, con u_t = N(u, u_x, …) su Ω.
- (a) I(u) = ψ^{−1}(J_u) ⊇ [F], e J_u è stabile per D e D_N.
- (b) I(u) = [F] ⟺ J_u = 0 ⟺ u, u_x, u_xx, … sono algebricamente indipendenti su ℂ.
- (c) Se u è **reale-analitica** su Ω: J_u è primo, e J_u ≠ 0 ⟺ trdeg_ℂ ℂ(u, u_x, …) < ∞. In tal caso esiste k tale che ∂_x^ju ∈ ℂ(u, …, ∂_x^ku) per ogni j, e ℂ⟨u⟩ = ℂ(u, …, ∂_x^ku).

Il campo è quello delle frazioni del dominio C^ω(Ω). [fix T1-1, S5-FIX2] Precisamente C^ω(Ω;ℂ) (funzioni analitiche reali a valori complessi), perché i polinomi hanno coefficienti in ℂ; è ancora un dominio per Ω connesso.
**Riduzione classica.** Zero generico di un ideale primo (Kolchin 1973) più l'argomento del separante (riduzione di Ritt).
**Anticipazione (AUDIT-4 §2.4).** Scholl–Bacho–Boche–Kutyniok, Mach. Learn. 115 (2026) 139, Prop. 1 + Tab. 1: per g = (u, …, ∂^nu) fissato, u_t = F(g) è unica fra le PDE polinomiali ⟺ le componenti di g sono algebricamente indipendenti. (b) equivale a quell'enunciato per ogni n: una G ∈ I(u)∖[F] dà ψ(G) ∈ J_u∖0, cioè una seconda equazione u_t = N + ψ(G). È quindi **CON-FONTE in forma parziale** (ordine finito). Il delta residuo è la formulazione per ideali e la dicotomia (c).
**Prova.**
(a) ev_u è un omomorfismo differenziale, e F(u) = 0, quindi [F] ⊆ I(u). Per ALG-L1, G − ψ(G) ∈ [F] ⊆ I(u), quindi G(u) = ψ(G)(u) e G ∈ I(u) ⟺ ψ(G) ∈ J_u. J_u è il nucleo di p ↦ p(u, u_x, …), e D, D_N agiscono come ∂_x, ∂_t sulle soluzioni.
(b) Se J_u = 0, allora I(u) = ψ^{−1}(0) = [F]. Se 0 ≠ p ∈ J_u ⊂ A, allora p ∈ I(u) e ψ(p) = p ≠ 0, quindi p ∉ [F]. L'ultima equivalenza è la definizione.
(c) Primalità: C^ω(Ω) [C^ω(Ω;ℂ), fix T1-1, S5-FIX2] è un dominio (Ω connesso, principio d'identità).
- (⇐) Se d := trdeg < ∞, allora u, …, ∂_x^du sono d+1 elementi algebricamente dipendenti: un polinomio non nullo li annulla, ed è in J_u.
- (⇒) Sia p ∈ J_u∖0 d'ordine minimo k e, fra questi, di grado minimo in y_k.
  - Se k = 0, u prende valori nell'insieme finito degli zeri di p, quindi è costante (Ω connesso) e trdeg = 0.
  - Se k ≥ 1, il separante S := ∂p/∂y_k è non nullo. Inoltre S ∉ J_u: ha ordine < k, oppure ordine k e grado minore in y_k, contro la minimalità. Quindi S(u) è un elemento non nullo del dominio, invertibile nel campo dei quozienti. Per induzione, D^jp = S·y_{k+j} + (termini d'ordine < k+j) (il passo: D(Sy_{k+j} + R_j) = Sy_{k+j+1} + (DS)y_{k+j} + DR_j, con DS e DR_j d'ordine ≤ k+j). Da D^jp ∈ J_u segue ∂_x^{k+j}u ∈ ℂ(u, …, ∂_x^{k+j−1}u) ⊆ … ⊆ ℂ(u, …, ∂_x^ku).
  - Allora trdeg ≤ k (p è una relazione fra k+1 generatori). Le derivate in t stanno in ℂ[x-getto], perché ∂_t^a∂_x^bu = ψ(∂_t^a∂_x^by)(u) per (a). Quindi ℂ⟨u⟩ = ℂ(u, …, ∂_x^ku). ∎

**Stato.** DIMOSTRATO-pronto. (b) è CON-FONTE parziale (Scholl et al.). La correzione O10 (analiticità nell'enunciato di (c)) è recepita: (a) e (b) valgono per u ∈ C^∞, mentre (c) e la primalità richiedono u analitica.

### §3.3 [ALG-P3] Forma chiusa ⇒ non identifica
**Enunciato.** Sia u reale-analitica su Ω connesso, soluzione di u_t = N. Supponiamo che esistano g_1, …, g_m ∈ C^ω(Ω) tali che il campo K := ℂ(g_1, …, g_m) (dentro Frac C^ω(Ω); precisamente Frac C^ω(Ω;ℂ), g_i ∈ C^ω(Ω;ℂ) [fix P3a-2, S5-FIX2]) sia chiuso per ∂_x e contenga u. Allora trdeg ℂ(u, u_x, …) ≤ m e I(u) ⊋ [F].
Casi:
- EP e razionali in (t,x): g = (t, x, e^{z_l·(t,x)});
- shock di Cole–Hopf di EP;
- N-solitoni di KdV: g = (E_1, …, E_N), perché ∂_xE_i = k_iE_i e u = 2∂_x² log f ∈ ℂ(E);
- 1-solitone e 2-solitone: relazioni esplicite in F4-ALG (V-ex C4–C7).

**Riduzione classica.** Corollario immediato di ALG-T1(c). È la versione non lineare di C3-C2 (EP non identifica).
**Prova.** ℂ(u, u_x, …) ⊆ K, perché K è un campo chiuso per ∂_x che contiene u. Quindi trdeg ≤ trdeg K ≤ m < ∞. Per ALG-T1(c) J_u ≠ 0, e per (b) I(u) ≠ [F]. ∎
**Limite (O7).** "Forma chiusa" qui significa **immersione in un campo di trdeg finito chiuso per ∂_x**. Una rappresentazione integrale (Cole–Hopf con U₀ generico) non è coperta: per U₀ differenzialmente trascendente la dicotomia non si applica. Con questa definizione la dicotomia "forma chiusa ⇒ non identifica" è un teorema (questo) e non è tautologica.
**[fix P3a-1, S5-FIX2]** La frase precedente è sovraenunciata e va letta così: con questa definizione, la dicotomia è ALG-T1(c): u analitica identifica ⟺ trdeg ℂ⟨u⟩ = ∞; ALG-P3 ne è la **direzione facile** (forma chiusa ⇒ non identifica), un corollario di una riga dato ALG-T1(b). La parte non banale è la direzione opposta (ALG-T1(b), che usa ALG-L1, e il viceversa di ALG-T1(c), che usa il separante e l'analiticità). La dicotomia non è un'evidenza indipendente (O7): è un teorema dentro un solo linguaggio.
**Stato.** DIMOSTRATO-pronto.

### §3.4 [ALG-P4] Trasporto attraverso Cole–Hopf
**Enunciato.** Siano Ω ⊂ ℝ² aperto connesso con H¹_dR(Ω) = 0 (semplicemente connesso), ν > 0 noto, e u reale-analitica su Ω con F_B(u) := u_t + uu_x − νu_xx = 0.
- (a) Esiste φ > 0 reale-analitica, unica a meno di una costante moltiplicativa, con u = −2νφ_x/φ e φ_t = νφ_xx.
- (b) I(u) = [F_B] ⟺ I(φ) = [y_t − νy_xx] ⟺ trdeg ℂ⟨φ⟩ = ∞.
- (c) Se vale (b), allora Ann(φ) = (τ − νξ²). Il viceversa è falso.

**Riduzione classica.** Cole–Hopf (Hopf 1950, Cole 1951) più ALG-T1, più un confronto di gradi di trascendenza.
**Prova.**
(a) La 1-forma ω_u := u dx + (νu_x − u²/2)dt ha dω_u = (u_t − ∂_x(νu_x − u²/2))dt∧dx = F_B(u)dt∧dx = 0. Per Poincaré (H¹_dR = 0) esiste ψ analitica con dψ = ω_u, unica a meno di costante. Pongo φ := e^{−ψ/2ν} > 0. Allora φ_x/φ = −u/2ν e φ_t/φ = −(νu_x − u²/2)/2ν, quindi
(φ_t − νφ_xx)/φ = −(νu_x − u²/2)/2ν − ν[(−u/2ν)_x + u²/4ν²] = 0.
Identità (V-ex esatto): F_B(−2νφ_x/φ) = −2ν∂_x((φ_t − νφ_xx)/φ).
**[fix P4-1, S5-FIX2] Unicità di φ (riga mancante).** Se φ̃ > 0 con u = −2νφ̃_x/φ̃ e φ̃_t = νφ̃_xx, allora ψ̃ := −2ν log φ̃ ha ψ̃_x = u e ψ̃_t = −2νφ̃_t/φ̃ = −2ν²φ̃_xx/φ̃ = νu_x − u²/2 (perché φ̃_xx/φ̃ = (φ̃_x/φ̃)_x + (φ̃_x/φ̃)² = −u_x/2ν + u²/4ν²); quindi dψ̃ = ω_u, ψ̃ = ψ + cost. e φ̃ = cost.·φ.
(b) Pongo r_j := ∂_x^jφ/φ. Si ha ∂_xr_j = r_{j+1} − r_1r_j e u = −2νr_1. Per induzione ∂_x^ku = −2νr_{k+1} + P_k(r_1, …, r_k), con P_k polinomio, quindi ℂ(u, …, ∂_x^ku) = ℂ(r_1, …, r_{k+1}) (triangolarità). Inoltre ℂ(φ, …, ∂_x^{k+1}φ) = ℂ(φ, r_1, …, r_{k+1}). I due x-getti generano campi i cui gradi di trascendenza differiscono di al più 1, quindi sono entrambi finiti o entrambi infiniti. u e φ sono analitiche e risolvono equazioni di evoluzione (Burgers, calore): si applica ALG-T1(b,c) a entrambe.
(c) La parte lineare di un ideale: I(φ) ∩ L = Ann(φ)·y, dove L è lo spazio delle forme lineari θy. Inoltre [Py] ∩ L = R·Py: [Py] è l'ideale dell'anello di polinomi ℂ[θy] generato dal sottospazio W = R·Py di forme lineari, e la sua componente di grado 1 è W. Quindi I(φ) = [heat] implica Ann(φ)y = R(τ − νξ²)y.
Il viceversa è falso: con φ = G_ν = t^{−1/2}e^{−x²/4νt}, u = x/t ha u_xx = 0, quindi y_2 ∈ J_u e I(u) ≠ [F_B]. Invece Ann(G_ν) = (τ − νξ²), perché G_ν ∉ EP (C3-T1/C3-T4 di Fase 3, importati; l'esempio è ALG-C1). ∎
**Stato.** DIMOSTRATO-pronto. Il controesempio in (c) usa C3-T4 (Fase 3, importato con il suo stato).

### §3.5 [ALG-P6] Trasporto attraverso Miura
**Enunciato.** KdV: u_t + 6uu_x + u_xxx = 0; mKdV: v_t − 6v²v_x + v_xxx = 0. Sia v reale-analitica su Ω connesso, soluzione di mKdV, e u := −(v² + v_x). Allora u risolve KdV e I(u) = [KdV] ⟺ I(v) = [mKdV].
**Riduzione classica.** Miura 1968 (JMP 9, 1202) più ALG-T1. L'argomento di Galois SL₂ non serve.
**Prova.** L'identità KdV[−(v² + v_x)] = −(2v + ∂_x)mKdV[v] (V-ex esatto) dà KdV(u) = 0. Da v_x = −u − v², per induzione v_k ∈ ℂ(x-getto di u)[v]. Quindi ℂ(x-getto di u) ⊆ ℂ(x-getto di v) = ℂ(x-getto di u)(v), e i gradi di trascendenza differiscono di al più 1. u è analitica. Si conclude con ALG-T1(b,c), applicato a KdV e a mKdV (entrambe di evoluzione). ∎
**Stato.** DIMOSTRATO-pronto.

### §3.6 [MODREL-T1] Rango 1 + relazione primitiva ⇒ Syz_f(u) = R·v
**Enunciato.** Siano R = ℂ[τ,ξ], 𝒜 ∈ {D′(Ω), C^∞(Ω), C^ω(Ω)} con Ω aperto, f = (f_1, …, f_d) funzioni polinomiali, **u tale che f_j(u) ∈ 𝒜 per ogni j** [fix M-1, S5-FIX2: in D′(Ω) il prodotto non è definito per u distribuzione qualsiasi; basta p.es. u ∈ L^p_loc(Ω) con p ≥ max deg f_j, oppure u ∈ C^∞; per 𝒜 = C^∞, C^ω nulla da aggiungere] e Syz_f(u) := {(Q_j) ∈ R^d : Σ_jQ_j(∂)f_j(u) = 0 in 𝒜}.
- (T1) Se v ∈ Syz_f(u) è primitivo (gcd_j v_j = 1) e rank_R Syz_f(u) = 1, allora Syz_f(u) = R·v.
- (Cor., d = 2) Se esiste v ∈ Syz primitivo, allora: Syz_f(u) = R·v ⟺ Ann(f_1(u)) = 0 oppure Ann(f_2(u)) = 0.
- (Burgers) Con f = (u, u²) e v = (τ − νξ², ½ξ), che è primitivo: u identifica Burgers nella classe di Hammerstein {Q_1(∂)u + Q_2(∂)u² = 0} ⟺ Ann(u) = 0 oppure Ann(u²) = 0.

**Riduzione classica.** Un vettore primitivo in R^d, con R fattoriale, genera un sottomodulo **saturato**: K·v ∩ R^d = R·v (lemma di Gauss / gcd). Il corollario è l'additività del rango in 0 → Syz → R² → M_f(u) → 0. Elementare.
**Anticipazione.** La versione ℂ-lineare (dizionario fissato, Gram) è in Scholl et al. (Tab. 1) e in He–Zhao–Zhong (FoCM 24 (2024) 1595–1641). La struttura di R-modulo non è stata trovata (AUDIT-4 §2.3).
**Prova.**
(T1) Sia K = Frac R. Syz è un sottomodulo di R^d di rango 1 che contiene v ≠ 0, quindi Syz ⊗ K = K·v. Per w ∈ Syz, w = (a/b)v con a, b ∈ R coprimi. Da bw = av segue b | av_j per ogni j, quindi b | gcd_j(av_j) = a·gcd_j(v_j) = a (R fattoriale, a meno di unità). Con gcd(a,b) = 1, b è un'unità e w ∈ R·v.
(Cor.) K è piatto, quindi 0 → Syz⊗K → K² → M_f(u)⊗K → 0 è esatta e rank Syz = 2 − rank M_f(u). Con v ≠ 0 in Syz, rank M ≤ 1. Inoltre rank M = 0 ⟺ M è di torsione ⟺ entrambi i generatori f_1(u), f_2(u) sono di torsione (la torsione è un sottomodulo, R è un dominio) ⟺ Ann(f_1(u)) ≠ 0 e Ann(f_2(u)) ≠ 0. Quindi Syz = R·v ⟺ rank Syz = 1 (⇐ per T1; ⇒ perché R·v ha rango 1) ⟺ rank M = 1 ⟺ Ann(f_1(u)) = 0 oppure Ann(f_2(u)) = 0.
(Burgers) (∂_t − ν∂_x²)u + ½∂_x(u²) = F_B(u) = 0, quindi v ∈ Syz. gcd(τ − νξ², ξ) = 1, perché ξ non divide τ − νξ² (V-ex). ∎
**Stato.** DIMOSTRATO-pronto.

---
## §4. [F4L-P3] Raggio in ampiezza per Burgers: un caso del lemma della striscia dei cumulanti
### §4.1 [L-S] Lemma della striscia (elementare)
**Enunciato.** Sia X una variabile aleatoria reale con valori q.c. in [a,b], w := b − a > 0, M(s) := 𝔼e^{sX}. Allora:
- M è intera;
- M(s) ≠ 0 per |Im s| < π/w;
- s ↦ log M(s) (ramo con log M(0) = 0) è olomorfa nella striscia, e la sua serie di Taylor in 0 (la serie dei cumulanti) ha raggio ≥ π/w;
- la costante è ottimale: per la legge a due punti simmetrica su {a,b}, il raggio vale esattamente π/w.

**Prova.** M è intera perché X è limitata (convergenza dominata). Siano s = σ + iτ con |τ| < π/w e m := (a+b)/2. Allora
Re(e^{−iτm}M(s)) = 𝔼[e^{σX}cos(τ(X−m))] ≥ cos(|τ|w/2)·𝔼e^{σX} > 0,
perché |τ(X−m)| ≤ |τ|w/2 < π/2. La striscia è semplicemente connessa e M non vi si annulla, quindi log M è olomorfa e il disco |s| < π/w ⊂ striscia dà il raggio. Per la legge simmetrica a due punti, M(s) = e^{sm}cosh(sw/2) ha zeri in s = iπ(2k+1)/w, a distanza π/w. ∎ (V-ex: 400 leggi casuali a 4 atomi su [0,1], min|Im s| sugli zeri = 3.1714 ≥ π. DEVIL-4: 300 leggi a 3 atomi.) Folklore della teoria delle funzioni caratteristiche: ho la prova, non una fonte con numero.

### §4.2 [F4L-P3] Enunciato e prova
**Notazione.** ν > 0. u₀ è una misura reale finita su ℝ (in particolare u₀ ∈ L¹). Pongo U₀(x) := u₀((−∞,x]), che è limitata, e w := osc U₀ = sup U₀ − inf U₀ ≤ ‖u₀‖. Siano G_ν(t,z) = (4πνt)^{−1/2}e^{−z²/4νt} e, per ε ∈ ℂ,
φ_ε(t,x) := ∫G_ν(t,x−y)e^{−εU₀(y)/2ν}dy,  u_ε := −2ν∂_xφ_ε/φ_ε.
Per ε reale, u_ε è la soluzione di Burgers con dato εu₀ (F-H). La **serie di Volterra in ampiezza** è per definizione la serie di Taylor in ε di u_ε: u_ε = Σ_nε^nu^{(n)}.
**[fix P3-2, S5-FIX2]** (i)–(iii) sono enunciati sulla **formula** di Cole–Hopf e non dipendono da F-H. L'identificazione "u_ε è la soluzione di Burgers con dato εu₀" è il teorema di Hopf per u₀ ∈ L¹; per u₀ **misura** (in particolare δ) la formula definisce una soluzione classica per t > 0 che assume il dato in senso debole-*, ma l'unicità nella classe delle misure non è coperta da F-H come enunciato in §0: per dato misura l'identificazione è **CONDIZIONALE[F-H]**.
**Enunciato.**
- (i) Per ogni t > 0 e x ∈ ℝ, φ_ε(t,x) ≠ 0 per |Im ε| < 2πν/w. Quindi ε ↦ u_ε(t,x) è olomorfa nella striscia, e la serie di Volterra in (t,x) converge per |ε| < 2πν/w. Il raggio non dipende da t né da x, e non serve alcun gap spettrale.
- (ii) Stime uniformi. Per 0 < r < 2πν/w:
  - sup_{|ε|≤r, x∈ℝ}|u_ε(t,x)| ≤ 2ν e^{rw/2ν}/(cos(rw/4ν)√(πνt));
  - se u₀ ∈ L¹ ∩ L^∞, sup_{|ε|≤r, t>0, x}|u_ε| ≤ r‖u₀‖_∞ e^{rw/2ν}/cos(rw/4ν).
  Quindi |u^{(n)}(t,x)| ≤ C r^{−n}, uniformemente su t ≥ t₀ > 0 (rispettivamente su t > 0).
- (iii) Ottimalità. Per u₀ = Aδ_0 (A > 0, w = A) si ha u_ε(t,0) = 4νG_ν(t,0)tanh(εA/4ν), con poli in ε = ±2πiν/A·(2k+1). Il raggio in (t,0) è esattamente 2πν/A per ogni t > 0. In (t,x), con Φ := ∫_0^∞G_ν(t,x−y)dy ∈ (0,1), il raggio vale R(t,x) = (2ν/A)√(log²((1−Φ)/Φ) + π²) ≥ 2πν/A.
- (iv) Versione su intervallo limitato. Sia Burgers su (0,L) con u(t,0) = u(t,L) = 0 e dato εu₀, u₀ ∈ L¹(0,L). Sostituendo G_ν con il nucleo di Neumann G_N(t,x,y) e U₀(y) := ∫_0^yu₀, (i) e la prima stima di (ii) valgono con lo stesso w = osc_{[0,L]}U₀ (modulo F-N).

**Modello e dominio.** Problema di Cauchy su ℝ (dato u₀ su tutta la retta), oppure (iv) problema di Dirichlet su (0,L), cioè una versione su Ω = (0,T)×(0,L) limitato. Le conclusioni sono puntuali, quindi valgono uniformemente su ogni Ω ⊂ (0,∞)×ℝ. Oggetto: E^NL, non E_int A9 (O1).
**Riduzione classica (O3).** **F4L-P3 è un caso di L-S.** Sia Y ~ G_ν(t,x−·) (densità di probabilità), X := U₀(Y) ∈ [inf U₀, sup U₀] e s := −ε/2ν. Allora φ_ε(t,x) = 𝔼e^{sX} = M(s), e |Im s| < π/w ⟺ |Im ε| < 2πν/w. L'uniformità in t è automatica, perché w non dipende da t. Il caso estremale tanh è la legge di Bernoulli simmetrica: per u₀ = Aδ e x = 0, X ∈ {0, A} con probabilità ½ ciascuno.
**Prova.**
(i) Per L-S applicato a X, φ_ε(t,x) = M(−ε/2ν) ≠ 0 nella striscia. ∂_xφ_ε(t,x) = ∫∂_xG_ν(t,x−y)e^{−εU₀(y)/2ν}dy è intera in ε: ∂_xG_ν(t,·) ∈ L¹ per t > 0, l'integrando è limitato da |∂_xG_ν|e^{|Re ε|w'/2ν} [fix P3-1, S5-FIX2: w′ non definito; leggere e^{|Re ε|·sup|U₀|/2ν}] e la convergenza è dominata localmente uniforme. Quindi u_ε è olomorfa dove φ_ε ≠ 0, e il disco |ε| < 2πν/w sta nella striscia.
(ii) Siano |ε| ≤ r, σ := Re s e τ := Im s, con |s| ≤ r/2ν. Da L-S: |φ_ε| ≥ cos(|τ|w/2)𝔼e^{σX} ≥ cos(rw/4ν)e^{σm − |σ|w/2}. Inoltre |∂_xφ_ε| ≤ e^{σm + |σ|w/2}‖∂_xG_ν(t)‖_{L¹} = e^{σm + |σ|w/2}/√(πνt). Ne segue |u_ε| ≤ 2νe^{|σ|w}/(cos(rw/4ν)√(πνt)) con |σ| ≤ r/2ν.
Se u₀ ∈ L^∞, U₀ è assolutamente continua e, integrando per parti, ∂_xφ_ε = ∫G_ν(t,x−y)·(−ε/2ν)u₀(y)e^{−εU₀(y)/2ν}dy. Quindi |∂_xφ_ε| ≤ (r/2ν)‖u₀‖_∞e^{σm + |σ|w/2}, uniformemente in t > 0. Le disuguaglianze di Cauchy sul cerchio |ε| = r danno |u^{(n)}| ≤ sup|u_ε|·r^{−n}.
(iii) U₀ = A·1_{[0,∞)}, quindi φ_ε = (1−Φ) + Φe^{−σ'} con σ' := εA/2ν, e ∂_xφ_ε = G_ν(t,x)(e^{−σ'} − 1), perché ∂_xΦ = G_ν(t,x).
- In x = 0, Φ = ½ e u_ε = −2νG(e^{−σ'} − 1)/((1 + e^{−σ'})/2) = 4νG·tanh(σ'/2).
- Zeri del denominatore: e^{−σ'} = −(1−Φ)/Φ, cioè σ' = −log((1−Φ)/Φ) + iπ(2k+1). Lì il numeratore vale G(−(1−Φ)/Φ − 1) = −G/Φ ≠ 0, quindi sono poli.
- Il modulo minimo è |ε| = (2ν/A)√(log²((1−Φ)/Φ) + π²), che in x = 0 vale 2πν/A. Questo è anche il raggio della serie di Taylor: il primo polo è sul cerchio.

(V-ex: formula tanh; la radice n-esima dei coefficienti di Taylor, n = 25, vale 1.927 contro 2πν/A = 1.933.)
(iv) Per ε reale, φ_ε(t,x) := ∫_0^LG_N(t,x,y)e^{−εU₀(y)/2ν}dy è positiva, risolve il calore con φ_x = 0 in 0 e L, e u_ε = −2νφ_x/φ risolve Burgers (identità di ALG-P4) con u = 0 al bordo. Per F-N è la soluzione. Con G_N ≥ 0 e ∫G_N dy = 1 (F-N), Y ha legge G_N(t,x,·)dy su [0,L], e L-S si applica come in (i). La stima di ∂_xφ si fa allo stesso modo, con ‖∂_xG_N(t,x,·)‖_{L¹} finito per t > 0. **[fix P3-4, S5-FIX2] Costante (lacuna chiusa da S-CHECK-9):** con la formula per immagini G_N = Σ_k[G(x−y+2kL) + G(x+y+2kL)] > 0 si ha ∫₀^L|∂_xG_N(t,x,y)|dy ≤ Σ_k∫₀^L(|G′(x−y+2kL)| + |G′(x+y+2kL)|)dy = ∫_ℝ|G′| = (πνt)^{−1/2}, perché gli intervalli {x−y+2kL : y ∈ (0,L)} e {x+y+2kL : y ∈ (0,L)} tassellano ℝ. Quindi la prima stima di (ii) vale **con la stessa costante**. L'identificazione con la soluzione di Dirichlet resta CONDIZIONALE[F-N]. (V-ex: nucleo di Neumann ≥ 0 di massa 1 nei nodi; |φ_ε| > 0 su un campione della striscia, dato U₀ = sin 2πy.) ∎

### §4.3 Confronto esplicito con Kieffer et al. (arXiv:2512.12019)
- **Loro equazione** (§II, letta dall'HTML v1 con uno strumento di estrazione, citazioni parziali): ∂_tu + (1−δ)v∂_xu + δu∂_xu − Re^{−1}∂_x²u = f, u(0,x) = g(x). Con v = 0 e f = 0, w := δu risolve Burgers con ν = 1/Re e dato δg. Quindi la loro serie in δ è la serie di Volterra in ampiezza divisa per δ, con lo **stesso raggio**: F4L-P3 si applica con ε = δ, ν = 1/Re, u₀ = g.
- **Loro tesi:** raggio in δ infinito "per ogni t > 0 e quasi ogni x". **È falsa.** Il loro argomento mostra che, per δ fissato, il denominatore si annulla su un insieme di x di misura nulla. Non mostra che, a x fissato, il denominatore non si annulli per alcun δ ∈ ℂ, ed è questo che determina il raggio. Gli autori dichiarano di non essere riusciti a provarlo.
- **Controesempio dai loro stessi dati.** Dato di Dirac. La loro forma integrale contiene e^{−(δRe/2)1_{(0,∞)}(y)}, cioè g = δ_0 di massa 1 (U₀ = 1_{(0,∞)}, w = 1). Per F4L-P3(iii), in ogni (t,x) il raggio è finito, R(t,x) = (2/Re)√(log²((1−Φ)/Φ) + π²). In x = 0 vale esattamente 2π/Re: è finito per **ogni** x, non solo per quasi ogni x.
- **Incoerenza interna.** La loro formula esplicita (30), come stampata, contiene e^{δRe}. La loro forma integrale (massa 1) dà invece e^{δRe/2}: controllo numerico in integ_checks, dove la forma integrale coincide con (30) **solo** con e^{δRe/2}. Il polo a δ = iπ/Re segnalato da CIT-AUDIT-4 viene dalla (30) stampata. Corrisponde a F4L-P3(iii) con massa A = 2: 2πν/A = π/Re. Con la forma integrale (massa 1) il polo è a δ = 2πi/Re (verificato: zero del denominatore in x = 0 in 2πi/Re, con numeratore ≠ 0). In entrambe le letture il raggio è finito e coincide con la previsione di F4L-P3, nella normalizzazione corrispondente.
- **[fix K-1, S5-FIX2] Portata della correzione.** La correzione è formulata **per il dato di Dirac** (che gli autori stessi usano come esempio): per quel dato il raggio è finito in **ogni** x. Per una tesi su dati generici (lisci) serve un controesempio a parte: la finitezza del raggio per un dato liscio vicino ad Aδ **non** segue da F4L-P3, che dà solo un minorante (APERTO, non verificato). Le due condizioni chieste da S-CHECK-9 — che la tesi copra v = 0 e il dato di Dirac — sono verificate sul testo (work/KIEFFER/LETTURA.md: l'abstract dice "for arbitrary integrable initial data"; §II intro "for every t>0 and almost every x"; l'equazione (II.1) con v = 0 si riduce a Burgers; la formula (30) è proprio il caso Dirac).
- **[fix K-2, S5-FIX2] Discrepanza e^{δRe} / e^{δRe/2} e numerazione.** Al momento dell'audit S-CHECK-9 il PDF non era leggibile (rete bloccata) e la discrepanza era registrata come "da verificare". Ora è **verificata sul testo** dal coordinatore (work/KIEFFER/LETTURA.md, versione HTML v1 letta col browser integrato): la forma integrale ha esponente −(δRe/2)𝟏_(0,∞)(y) (fattore ½ confermato), la formula stampata è la **(30)** e contiene e^{δRe}: (30) è incoerente con la loro forma integrale (segno e fattore 2). Numerazione uniformata: **(30)** (la "(23)" di AUDIT-4 è da leggere come (30)). Il raggio è finito in ogni x con entrambe le forme; gli autori ammettono nel §II.1 di non aver dimostrato la stretta disuguaglianza per ogni x. Stato KIEFFER-C: **DIMOSTRATO** (LEDGER), correzione pubblicabile come commento citando la loro ammissione.
- **Distinzione di oggetto.** Per v ≠ 0 la loro deformazione aggiunge una traslazione galileiana dipendente da δ. Lì F4L-P3 non si applica tale e quale (rischio R4, non trattato).

**Stato F4L-P3.** DIMOSTRATO-pronto (i)–(iii), su ℝ. (iv) è DIMOSTRATO-pronto modulo F-N. **Novità:** nessuna nella tecnica (è L-S). Il contenuto è il raggio esplicito, uniforme in t e ottimale, e la correzione della tesi di Kieffer et al. Non è CON-FONTE: nessun enunciato identico trovato (AUDIT-4 §2.1). Resta da leggere Bender–Boettcher–Milton, JMP 32 (1991) 3031, e la letteratura sugli zeri dei calori complessi (Polacik e coll.).

---
## §5. Tabella riassuntiva (stato onesto)
| ID | enunciato (1 riga) | modello · dominio | riduzione classica | stato |
|---|---|---|---|---|
| INT-T1(A), UC-ω, B1 | 𝒜(u) = c + {d : K_d[u(t,·)] = 0}; UC per u analitica; indipendenza delle ∂_{c_j}u | M1/M3 · Ω con π_t(Ω) = I | principio d'identità; asintotica | **DIMOSTRATO** (S-CHECK-9 PASS) |
| INT-T1(UC-1) | UC da Ω a I×ℝ se il flusso vero ha ordine **esattamente** 3 (c_1 ≠ 0 necessario, UC-1b), per ogni M | M3 · Ω limitato | Saut–Scheurer + commutazione dei flussi | **CONDIZIONALE[F-C, F-SS]** (riduzione DIMOSTRATA; PASS-con-fix(UC-1a, UC-1b)) |
| INT-T1(B) | N-solitone: 𝒩 = {q_d(k_j²) = 0}, identifica in 𝓗_M ⟺ M ≤ N−1 | M1 · Ω qualsiasi | Novikov + Vandermonde | **CONDIZIONALE[F-MS]** (riduzione DIMOSTRATA) |
| INT-T1(C) | identifica in 𝓗_M ⟺ \|Λ\| ≥ M+1; in 𝓗_∞ = ∪_M𝓗_M (C-1) ⟺ r ≢ 0 | M3 esatto · I×ℝ (Ω via UC) | Lax/AKNS + Vandermonde | **CONDIZIONALE[F1–F4]** (riduzione PASS-con-fix(C-1)) |
| INT-T2 | NLS: ambiguità max(0, M+1−\|Λ\|) | M3 · I×ℝ | Zakharov–Shabat + Vandermonde reale | **CONDIZIONALE[ZS, UC]** |
| INT-P5 | f = det(I+C); E_int = 2∂² log Z; cumulanti solo a coppie; E_int ≢ 0; costo O(N³) | M1 · ℝ | Cauchy; gas di Ising | **DIMOSTRATO** |
| INT-P6 | ∫E_int dx = 0, ∫u = 2Σk_i | M1 · ℝ (solo ℝ) | limiti | **DIMOSTRATO** |
| F4LIN-T2 | −2ν log N ≤ ψ^ν − ψ⁰ ≤ 0; 4ν ln 2 per shock; L^p/Ḣ^s (F̂ in forma chiusa, L-1); K shock + O(e^{−δ/2ν}) (L-3) | M1 · ℝ (intervalli con errore esp.) | log-sum-exp; profilo tanh | **DIMOSTRATO** (PASS-con-fix(L-1..L-3); costante elementare, cfr. Wang 1998; identificazione entropica CON-FONTE Evans, non usata) |
| L-S | 𝔼e^{sX} ≠ 0 per \|Im s\| < π/w, ottimale | — | folklore | **DIMOSTRATO** |
| F4L-P3 | raggio ≥ 2πν/osc U₀, uniforme in t, ottimale **come costante uniforme, raggiunta in x = 0** (P3-3: in x ≠ 0 il raggio è più grande); versione Dirichlet su (0,L); controesempio a Kieffer et al. | Cauchy su ℝ; Dirichlet su (0,L) | **caso di L-S** | (i)–(iii) **DIMOSTRATO** come enunciati sulla formula di Cole–Hopf; "è la soluzione per dati misura" **CONDIZIONALE[F-H]** (P3-2); (iv) **DIMOSTRATO** per la formula, identificazione con la soluzione di Dirichlet **CONDIZIONALE[F-N]** |
| KIEFFER-C | contro arXiv:2512.12019: raggio finito per il dato di Dirac in ogni x | v = 0 | F4L-P3(iii) | **DIMOSTRATO** (testo letto, work/KIEFFER/LETTURA.md; K-1, K-2) |
| ALG-L1 | ℂ{y}/[F] ≅ A, [F] primo | · Ω connesso | Olver cap. 5 | **DIMOSTRATO** (noto) |
| ALG-T1 | I(u) = [F] ⟺ J_u = 0; (u analitica, C^ω(Ω;ℂ)) ⟺ trdeg = ∞ | M3 · Ω connesso | zero generico + separante | **DIMOSTRATO**; (b) CON-FONTE parziale (Scholl et al. 2026) |
| ALG-P3 | u in un campo ∂_x-chiuso di trdeg finito ⇒ I(u) ⊋ [F] (direzione facile di ALG-T1(c), P3a-1) | M1 · Ω | corollario di ALG-T1 | **DIMOSTRATO** |
| ALG-P4 | Cole–Hopf: I(u) = [F_B] ⟺ I(φ) = [calore]; ⇒ Ann φ = (τ−νξ²), non viceversa | M3 · Ω semplicemente connesso | Hopf–Cole + trdeg | **DIMOSTRATO** (fix P4-1) |
| ALG-P6 | Miura: I(u) = [KdV] ⟺ I(v) = [mKdV] | M3 · Ω connesso | Miura + trdeg | **DIMOSTRATO** |
| MODREL-T1 (+Cor., Burgers) | rank Syz = 1 + v primitivo ⇒ Syz = R·v; d = 2 ⟺ Ann f_1(u) = 0 o Ann f_2(u) = 0 (f_j(u) ∈ 𝒜, M-1) | M3 · Ω qualsiasi | saturazione di Gauss | **DIMOSTRATO** |
**[fix stati, S5-FIX2]** Colonna "stato" allineata a claims/LEDGER.md (righe "Fase 4 — lemmi di trasporto", audit S-CHECK-9, work/CHECK/AUDIT_S4-INTEG.md, 69/69); il testo originale diceva "DIMOSTRATO-pronto" per tutte le righe tranne INT-T1(C), INT-T2, e i fatti F-C, F-SS, F-MS, F-H (misure), F-N non letti rendono CONDIZIONALI le righe corrispondenti. Le marche nella tabella recepiscono [fix P3-3, UC-1b, C-1, L-1, L-3, T1-1, P3a-1, P4-1, M-1, K-1, K-2, S5-FIX2].
Nessun lemma FALSO. Una tesi della letteratura risulta falsa: Kieffer et al., "raggio infinito" (§4.3).

## §6. Rischi aperti (per S-CHECK)
- R1. [chiuso da fix UC-1a, S5-FIX2: esaustione con palle e rettangoli, §1.1] In (UC-1) uso "componenti orizzontali" di Saut–Scheurer da fonte secondaria. Se il teorema richiede ω connesso, oppure un dominio (a,b) fisso con coefficienti più regolari, la conclusione su I×ℝ va riformulata per esaustione.
- R2. F-MS (N-solitone simultaneo della gerarchia) è V-ex solo per N ≤ 2, n ≤ 2. Serve una fonte letta per n qualsiasi.
- R3. In INT-T1(C) i segni e i fattori 2 della convenzione di F1 sono irrilevanti per il conteggio, ma non sono verificati.
- R4. F4L-P3 con v ≠ 0 (Kieffer) non è trattato.
- R5. [chiuso da fix L-1, S5-FIX2: F̂ in forma chiusa, §2] F4LIN-T2(ii), Ḣ^s: l'asintotica F̂(η) ~ const/η è motivata, non calcolata in forma chiusa.
- R6. In ALG-P4(c) e ALG-C1 il controesempio usa C3-T4 di Fase 3: si eredita il suo stato.
- R7. [chiuso da fix K-2, S5-FIX2: testo letto dal coordinatore, work/KIEFFER/LETTURA.md; (30) confermata incoerente] La lettura di Kieffer et al. viene da un'estrazione automatica dell'HTML (citazioni parziali). Prima di pubblicare la correzione, va riletta l'equazione (30) sul PDF.
