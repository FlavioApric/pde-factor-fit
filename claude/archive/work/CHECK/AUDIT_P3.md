# AUDIT P3 — duali e perturbazioni (claim di S-P3)
Revisore: S-CHECK-5 (5ª tornata) · 25/10/2026
Fonte esaminata: `work/P3/CHECK_REQUEST.md` (per intero). **Riferimenti puntuali dichiarati:** `work/P3/PROOF_PACKAGE.md` §7 (righe 230–281, solo per il kill-argument su RT-S2a, eccezione del coordinatore: testo identico a quello della CHECK_REQUEST) e `research/SCOUT-2/REPORT.md` righe 19–21 e 29 (testo originale del criterio S2-A, per verificare che §7.0 lo riporti "alla lettera nella sostanza"). Nessun'altra parte di work/P3 è stata letta (non §8 "passaggio avversariale inline", non i commenti dell'autore).
Fatti importati usati come dati (LEDGER): P1-L1, P1-L2, P1-L3, P1-L5, P1-T2 (DIMOSTRATO, AUDIT_P1); II-P5(b) (DIMOSTRATO). C12-T6 (base di Appell) è "prova scritta" non auditata: P3-T4(f) e P3-T5 non ne dipendono davvero (le identità usate sono riverificate qui dalla funzione generatrice) → nessuna dipendenza critica.
Skill caricate (lettura integrale dei SKILL.md, nessuno script _vendor eseguito): skills-local/session-protocol (per prima), skills-local/claim-lifecycle, proof-checker (il reviewer sono io: Phase 0.5 enunciati canonici e micro-claim, checklist A–H, Phase 1.5 red team, severità a due assi, acceptance gate; niente Codex/LaTeX), kill-argument (revisori = subagenti Claude freschi senza contesto, al posto di Codex; verdetto calcolato con la tabella della skill, non dall'arbitro), scientific-critical-thinking (separare enunciati dimostrati da "Letture"; stato proporzionato), sympy.
SymPy/numpy: `work/CHECK/sympy/audit_p3.py` → `audit_p3.out` (esito in §5).

## 0. Verdetti
| claim | verdetto | stato proposto |
|---|---|---|
| P3-L1 (Dyson formale) | **PASS** | DIMOSTRATO |
| P3-L2 (a),(b),(c),(e) | **PASS-con-fix(L2-1)** | DIMOSTRATO |
| P3-L2 (d) (identificazione con il semigruppo) | **PASS-con-fix(L2-2)** — argomento di unicità corretto; Miyadera–Voigt da verificare | CON-FONTE (Engel–Nagel, numerazione → CIT-AUDIT, ADD_REFERENCE) |
| P3-T1 (a1),(a2),(b),(c) | **PASS** | DIMOSTRATO (generazione: via P3-L2(d), CON-FONTE) |
| P3-C1 | **PASS-con-fix(C1-1)** | DIMOSTRATO |
| P3-P2 | **PASS** | DIMOSTRATO |
| P3-T2 | **PASS-con-fix(T2-1, T2-2)** | DIMOSTRATO (la fonte Hermite–Genocchi diventa superflua con T2-1) |
| P3-P1 | **PASS-con-fix(P1-1)** | DIMOSTRATO |
| **P3-T3** (i)–(vi) | **PASS-con-fix(T3-1 MAJOR, T3-2, T3-3, T3-4)** — esponente 5/4 verificato analiticamente con costante asintotica esatta | DIMOSTRATO (enunciati come scritti, dati modali finiti); "Lettura (2)" **FALSA fuori dai dati modali finiti** (kill-argument) → nuovo APERTO P3-Q-bordo |
| P3-T4 | **PASS** | DIMOSTRATO |
| P3-T5 | **PASS** | DIMOSTRATO |
| P3-T6 (i)–(v) | **PASS-con-fix(T6-1)** | DIMOSTRATO |
| **P3-T6 (vi)** | **FAIL(T6-vi)** — CRITICAL (INVALID + LOCAL): "L₀ = ∂_t unica scelta equivariante non degenere" è falso (famiglia L₀^θ) | FALSO come scritta; vera la versione ristretta alla famiglia {L₀^Σ} (fix) |
| **Verdetto §7.1 "RT-S2a MERGE-INTO RT-2"** | **non sostenuto come registrato** (kill-argument **FAIL**, reason_code unresolved_critical) | proposta: RT-S2a **PARCHEGGIATA** (criterio di SCOUT-2 silente); P3-T6(i),(iv),(v) entrano comunque in RT-2 come quadro (f) — decisione del coordinatore, §4 |

Rilievi: 1 CRITICAL (T6-vi, locale a P3-T6 ma portante per il verdetto RT-S2a), 2 MAJOR (T3-1 portata della Lettura di P3-T3; V-1 "l'unica scomposizione … continua in H^m" nel verdetto §7.1), il resto MINOR. Nessun FATAL. Tutti i calcoli di P3-T3 (costanti t₁,t₂,t₃, ρ_nm, |g−h|, conteggio di parità) sono corretti.

## 1. Enunciati canonici (Phase 0.5)
- **P3-L2.** ∀X Banach, ∀A₀ generatore con ‖S₀(t)‖ ≤ Me^{ωt}, ∀V lineare con D(A₀) ⊆ D(V), ∀T > 0, (H_β) su (0,T] con β ∈ [0,1) ⇒ ∀n, ∀t ∈ [0,T]: ‖S^{(n)}(t)‖ ≤ Me^{ωt}(KΓ(γ))^n t^{nγ}/Γ(1+nγ); Σ_n ε^nS^{(n)}(t) intera in ε ∈ ℂ, uniformemente in t ∈ [0,T]; se V ∈ 𝓛(X₁,X), coincide su [0,T] con il semigruppo generato da (A₀+εV, D(A₀)).
- **P3-T1(a1).** ∀a ∈ ℂ[ξ] di grado q ≥ 1: [∃δ>0, ω: Re a(iκ) ≤ ω − δ|κ|^q ∀κ ∈ ℝ] ⟺ [q pari ∧ Re(α_q i^q) < 0].
- **P3-T3(iii).** ∀L, D > 0, c ≠ 0, ∀N, ∀(c_n)_{n≤N} ∈ ℂ^N, u₀ = Σc_ne_n: (a) ∃C = C(N, Σn|c_n|, c, L, κ): ‖E^{mult,(1)}(t)u₀‖ ≤ Ct^{5/4} ∀t ∈ (0,1]; (b) (u₀′(0),u₀′(L)) ≠ 0 ⇒ ∃c′ = |c||S|κ^{1/4}/(32L), t_* = min(|S|/(48Aκ N²), 1/(4κN²), 1/(16κ)) con ‖E‖ ≥ c′t^{5/4} ∀t ∈ (0,t_*]; (c) u₀′(0) = u₀′(L) = 0 ⇒ ‖E‖ ≤ Ct². **Le costanti dipendono da N** (non uniformi nei dati: T3-4).
- **P3-T6(vi)** (come scritta). ∀N ≥ 2: tra i riferimenti L₀ che danno una scomposizione esatta, equivariante per permutazioni e non degenere, l'unico è L₀ = ∂_t. **La prova quantifica solo su L₀^Σ, Σ ⊆ [N]** → T6-vi.

## 2. Micro-claim ed esiti per passo

### 2.1 P3-T3 (priorità 1, cammino critico)
| MC | passo | esito |
|---|---|---|
| T3.1 | (i) V_mn = −(2cmn/L)(1−(−1)^{m+n})/(m²−n²), diagonale nulla | OK (SymPy, m,n ≤ 8, simbolico in L, c) |
| T3.2 | (ii) Re_n = (−1)^{n+1}e_n, RV = −VR, R unitaria e reale ⇒ V_mn = −(−1)^{m+n}V_mn | OK |
| T3.3 | (1) \|T_nm\| ≤ min(t, κ\|m²−n²\|t²/2) (ψ ∈ (0,1], \|ψ′\| ≤ \|λ_n−λ_m\|) | OK |
| T3.4 | (2) T_nm = g(κn²t, κm²t)/(κ(m²−n²)), g = ∫_a^b e^{−y}(y−a)dy ∈ [0,1] | OK (SymPy) |
| T3.5 | equivalenza (S_disp, S_pari) = 0 ⟺ u₀′(0) = u₀′(L) = 0 | OK (Σnc_n = S_p + S_d, Σ(−1)^n nc_n = S_p − S_d) |
| T3.6 | (a) modi bassi: \|V_mn\|κ\|m²−n²\|t²/2 = 2\|c\|κmnt²/L, C₁ = 4\|c\|κNΣn\|c_n\|/L | OK |
| T3.7 | (a) modi alti: m²−n² ≥ ¾m², \|V_mn\| ≤ 16\|c\|n/(3Lm); somma spezzata a M = ⌊t^{−1/2}⌋: t⁴M³κ²/4 + t²/M ≤ (κ²/4 + 2)t^{5/2} | OK (M³ ≤ t^{−3/2}, 1/M ≤ 2t^{1/2}); costanti verificate numericamente su 3 dati (anche complessi) |
| T3.8 | (b) E_m = −(4c/(Lκ))m^{−3}(hS + R_m) per m ≡ p, m ≥ 2N | OK |
| T3.9 | ρ_nm − 1 = (2x−x²)/(1−x)² ≤ (32/9)x ≤ 4x ≤ 4N²/m² per x ≤ ¼ | OK (domanda 4) |
| T3.10 | g_nm − h = e^{−a} − 1 + ae^{−y}, \|·\| ≤ 2a ≤ 2κN²t | OK (domanda 4) |
| T3.11 | su [m₋, m₊]: y ∈ [1,4], h ≥ 1 − 2/e > ¼; N²/m² ≤ κN²t ⇒ \|R_m\| ≤ 6AκN²t ≤ \|S\|/8 per t ≤ t₁ | OK |
| T3.12 | m ≥ 2N per t ≤ t₂ = 1/(4κN²); #{m ≡ p in [m₋,2m₋]} ≥ m₋/2 − 1 ≥ m₋/4 per t ≤ t₃ = 1/(16κ) | OK (un intervallo chiuso di lunghezza ℓ contiene ≥ ⌊ℓ⌋ ≥ ℓ−1 interi, di cui ≥ (ℓ−1)/2 − ½ della parità data) |
| T3.13 | costante finale ‖E‖ ≥ \|c\|\|S\|κ^{1/4}t^{5/4}/(32L) | OK (anche numericamente per e₁, t ∈ {t_*, t_*/10, t_*/1000}) |
| T3.14 | segno di c, c_n complessi (domanda 4) | OK: compaiono solo \|c\|, \|S\|, \|c_n\|; h reale |
| T3.15 | (iii)(c) via (iv): A₀u₀ ∈ H¹₀ e Vu₀ ∈ H²∩H¹₀ per somme finite | OK. **Osservazione:** per somme finite A₀u₀ ∈ H¹₀ è automatica; per u₀ ∈ D(A₀) generale è una seconda condizione di compatibilità indipendente → T3-1 |
| T3.16 | (iv) scambio di V (chiuso, D(V) = H¹) con Bochner (Hille): serve r ↦ VS₀(r)f continua e integrabile — data da ‖∂S₀(r)f‖ ≤ ‖∂f‖ per f ∈ H¹₀ (coefficienti in coseni μ_nf_n) | OK (domanda 5) |
| T3.17 | (v) su 𝕋 V diagonale, E^mult ≡ 0; e₁: Ve₁ ∉ D(A₀) | OK; ma la frase "BCH darebbe t²/2[A₀,V]u₀ … il coefficiente di t² non è in L²" è impropria: come espressione differenziale [D∂², −c∂] = 0; per e₁ il commutatore di operatori non è definito (Ve₁ ∉ D(A₀)) → **T3-2** (MINOR) |
| T3.18 | (vi) flusso di inflow, derivata destra in L² | OK (domanda 6): su (h,L) convergenza uniforme, su (0,h) norma ≤ 2\|c\|t‖u₀′‖_∞√h. **MINOR T3-3:** E^{mult,(1)} è definita in P3-P1 per u₀ ∈ D(A₀), mentre (vi) prende u₀ ∈ C¹, u₀(0) = 0 (non necessariamente in D(A₀)): la definizione si estende a u₀ ∈ D(V) = H¹ (S^{(1)}(t) limitato, Vu₀ ∈ L²) — dirlo; per c < 0 l'inflow è in x = L (condizione u₀(L) = 0) |

**Verifica analitica dell'esponente 5/4 (richiesta del coordinatore; indipendente dalla prova di S-P3).** Per u₀ = e₁ solo i modi m pari contribuiscono e, per m → ∞ con y := κm²t fisso, (2) e (i) danno E_m = −(4c/(Lκ))m^{−3}h(y)(1 + O(m^{−2}) + O(κt)), h(y) = 1 − e^{−y}(1+y) = ∫₀^y ze^{−z}dz. La somma su m pari è una somma di Riemann con passo 2 nella variabile m = (y/(κt))^{1/2}:
‖E‖² ≈ (16c²/(L²κ²)) · ½∫₀^∞ m^{−6}h(κm²t)²dm = (16c²/(L²κ²)) · ¼(κt)^{5/2} J,  J := ∫₀^∞ y^{−7/2}h(y)²dy,
convergente in 0 (h² ~ y⁴/4, integrando ~ y^{1/2}/4) e all'infinito (y^{−7/2}); i modi con m limitato (\|E_m\| ≲ mt²) contribuiscono O(t⁴), trascurabile, e la regione y ≪ 1 con m grande è già dentro l'integrale (convergente in 0). Quindi
**‖E^{mult,(1)}(t)e₁‖ = 2\|c\|√J κ^{1/4} t^{5/4}/L · (1 + o(1)),  J = 0.17202777 (mpmath).**
L'esponente 5/4 nasce da: ampiezza per modo m^{−3} (V_m1 ~ 1/m per il bordo, T_1m ~ 1/m² per la dinamica) × numero di modi attivi (κt)^{−1/2} (strato limite di spessore √t): (κt)^{3}·(κt)^{−1/2} = (κt)^{5/2} per il quadrato. Controllo numerico (serie modale esatta, 40000 modi, L=c=D=1): rapporto ‖E‖/previsione = 0.99582, 0.99958, 0.99996, 1.00000 per t = 10⁻³…10⁻⁶ (le pendenze 1.24984, 1.24998 riproducono quelle di S-P3). Coerenza con le costanti di (iii): c′ = κ^{1/4}/32 ≈ 0.055κ^{1/4} ≤ 2√J κ^{1/4} ≈ 0.83κ^{1/4} ≤ costante di (a). Con questo P3-T3(iii)(a)–(b) è confermato da due argomenti indipendenti.

### 2.2 P3-L2, P3-T1, P3-C1, P3-L1
| MC | passo | esito |
|---|---|---|
| L2.1 | (a) fattore e^{ω(t−s)}e^{ωs} = e^{ωt} vale per ogni ω ∈ ℝ (anche ω < 0); M compare una sola volta (la stima di VS₀ non contiene M) | OK (domanda 1) |
| L2.2 | Bochner: s ↦ S^{(n−1)}(t−s)VS₀(s)x è continua su (0,t) (famiglia fortemente continua e uniformemente limitata × funzione continua) ⇒ fortemente misurabile; dominata da Cs^{−β} | OK; **L2-1** (MINOR): esplicitare il lemma "U(·) fortemente continua, uniformemente limitata, f continua ⇒ U(·)f(·) continua" (ε/3) |
| L2.3 | integrale di Beta | OK (SymPy, γ = 2/3, n = 3) |
| L2.4 | (b),(c) raggio infinito (Γ(1+nγ)^{1/n} → ∞), intera in ε, uniforme su [0,T] | OK |
| L2.5 | (d) W := S_ε verifica la formula di variazione delle costanti (somma della ricorrenza, convergenza totale dominata da s^{−β}); Δ = S − W fortemente continua e limitata; identità su D(A₀) estesa a X per densità (il secondo membro è continuo in x grazie a (H_β)); iterazione n volte → 0 | OK (domanda 2): l'identificazione su [0,T] è corretta, dato il teorema di Miyadera–Voigt |
| L2.6 | ipotesi di Miyadera–Voigt: εV ∈ 𝓛(X₁,X), ∫₀^{t₀}‖εVS₀(s)x‖ds ≤ q‖x‖ con q < 1 | OK; **L2-2** (ADD_REFERENCE): Engel–Nagel 2000, Cap. III §3.c (Thm III.3.14 / Cor. III.3.16) — **numerazione non verificabile da me** (nessun accesso al testo): in coda a CIT-AUDIT. Il contenuto (Miyadera–Voigt con formula di variazione delle costanti su D(A)) è standard |
| L2.7 | (e) ‖VS₀(s)‖ ≤ KMT₀^{−β}e^{ωs} ≤ KM(T/T₀)^β s^{−β}e^{ωs} | OK |
| T1.1 | (a1) casi limite: Re(α_qi^q) = 0 ⇒ deg p < q, p + δ\|κ\|^q → +∞; q dispari ⇒ termine direttore → +∞ da un lato | OK (domanda 3) |
| T1.2 | (a2) sup_{y≥0} y^ke^{−sδy^q} = (k/(qδes))^{k/q}; s^{−k/q} ≤ T^{(r−k)/q}s^{−r/q}; V ∈ 𝓛(H^q, L²); X₁ = H^q (norme equivalenti) | OK (SymPy) |
| T1.3 | (b) sup_μ μ²e^{−2Dμ²s} = 1/(2eDs); {√(2/L)cos(μ_nx)}_{n≥1} ortonormale; K dichiarato | OK (SymPy) |
| T1.4 | (c) 𝔅: (H₀), commutazione, riduzione a e^{tA₀}e^{tV} | OK |
| C1.1 | (a) sup(2ty)^ne^{−ty}/n! = (2n)^ne^{−n}/n! ~ 2^n/√(2πn) | OK (numerico n = 12) |
| C1.2 | (a),(b) "A₀+V non genera": l'argomento "‖e^{t(A₀+V)}‖ ≥ sup e^{−tκ} = ∞" presuppone che il semigruppo, se esiste, sia il moltiplicatore | **C1-1** (MINOR): dire che lo spettro di un operatore di moltiplicazione di Fourier contiene la chiusura dell'immagine del simbolo, che non è contenuta in alcun semipiano {Re z ≤ ω}: per Hille–Yosida non è un generatore |
| C1.3 | (c) S^{(n)} = (t∂)^nS₀(t)/n! illimitato | OK |
| L1.1 | P3-L1 (a)–(c): P1-L5, induzione d'ordine, unicità, commutazione con ∂_t | OK |

### 2.3 P3-T2, P3-P1
| MC | passo | esito |
|---|---|---|
| T2.1 | Lemma D a punti distinti (fratti semplici) | OK |
| T2.2 | continuità di F_j in (z₀,…,z_j): via Hermite–Genocchi (CON-FONTE) | OK; **T2-1** (MINOR, ADD_DERIVATION che rende superflua la fonte): F_j(t;z) = (2πi)^{−1}∮_Γ e^{tζ}∏(ζ−z_i)^{−1}dζ con Γ che circonda i punti, continua (anzi olomorfa) nei z_i per z_i dentro Γ, e vale anche a punti ripetuti. Verificato numericamente (Lemma D a punti ripetuti e F_j = t^je^{tz}/j!) |
| T2.3 | (a) S₀(s)e_n = e^{λ_ns}e_n, ⟨e_m^†,S₀(r)y⟩ = e^{λ_mr}⟨e_m^†,y⟩ (densità di D(A₀)), funzionale sotto Bochner | OK |
| T2.4 | (b) induzione rafforzata (uguaglianza in X) | OK (domanda 7). L'ipotesi di espansioni finite è usata per portare la somma fuori dall'integrale e restare in D(A₀); con espansioni infinite servirebbe la convergenza in X della somma sui cammini (ad es. Σ\|V_kn\|‖e_k‖ < ∞ uniformemente) — l'enunciato come scritto è corretto |
| T2.5 | (e) commutante: la prova passa per (b), che richiede espansioni finite; l'ipotesi "A₀V = VA₀ su span{e_n}" non dà da sola Ve_n ∈ span | **T2-2** (MINOR): aggiungere a (e) l'ipotesi di (b) (o V-invarianza di span{e_n}); in alternativa prova diretta: Ve_n è autovettore di A₀ con λ_n, quindi S^{(1)}(t)e_n = te^{λ_nt}Ve_n, e si itera se V^je_n ∈ D(A₀) con A₀V^je_n = λ_nV^je_n |
| T2.6 | (c),(d) | OK |
| T2.7 | Dyson 1° e 2° ordine = formula dei cammini (esponenziale a blocchi di Van Loan, λ = (0,−1,−3), V piena) | OK (SymPy/scipy) |
| P1.1 | (a),(b) forma con φ | OK |
| P1.2 | (c) Hadamard: "per w → −∞ reale h ~ −w, Qe^{cw} decresce o cresce esponenzialmente se c ≠ 0" | **P1-1** (MINOR, LOGICAL_GAP): c è complesso; se c è immaginario puro, \|Q(w)e^{cw}\| = \|Q(w)\| cresce polinomialmente sull'asse reale e non c'è contraddizione a −∞. Fix: per w → +∞, \|h(w)\| ~ e^w forza Re c = 1 (e Q ≠ 0); allora a −∞ \|Qe^{cw}\| = \|Q\|e^w → 0 mentre \|h\| ~ \|w\| → ∞: assurdo. Domanda 8: con il fix l'argomento è completo. Zero esplicito w₀ ≈ 2.0888 + 7.4615i verificato; elemento moltiplicativo nullo a t = 1 verificato |
| P1.3 | (d) | OK |

### 2.4 P3-T4, P3-T5, P3-P2
| MC | passo | esito |
|---|---|---|
| T4.1 | (a) soluzione, derivazione sotto il segno (supporto compatto) | OK (SymPy, deg a = 2, 3 generici) |
| T4.2 | (b) getto in t = 0 determinato da u₀ su J ((a(∂)+εx)^ku₀), analiticità in t; ben posizione di U_ε su 𝒰 (funzioni, non misure): due misure con la stessa u₀ su J danno getti uguali e u intere in t | OK (domanda 9) |
| T4.3 | (c) **B_t(ζ) = Σ_{k=0}^q ε^kt^{k+1}a^{(k)}(ζ)/(k+1)!** e forma nell'altro ordine con (−ε)^k e a^{(k)}(ζ+εt) | OK (SymPy, deg 2 e 3, simbolico: richiesta del coordinatore) |
| T4.4 | grado esatto q in ε: coefficiente t^{q+1}q!α_q/(q+1)! ≠ 0 | OK |
| T4.5 | (e) [a(∂),x] = a′(∂), ad² = 0 | OK |
| T4.6 | (f) (x−x₀)v_n = v_{n+1} − tΣ_j C(n,j)a^{(j+1)}(0)v_{n−j} | OK (a cubico, n ≤ 4); non dipende da C12-T6 (solo funzione generatrice) |
| T5.1 | (i) inversione di e^{±ta(∂)} sui polinomi, continuità su B_ρ, conservazione via P1-T2(i) | OK |
| T5.2 | (ii) (α)⟺(β)⟺(γ): **deg Re a(iκ) = 2r ≥ 2 pari e sℓ < 0** | OK (domanda 10); i casi p costante, deg p dispari, sℓ > 0 sono tutti coperti |
| T5.3 | (iii) M_j = (i d/dκ)^jK̂(0) = (−1)^jh^{(j)}(0) con K̂(κ) = ∫Ke^{−iκx}dx = h(iκ); integrazione per parti; biortogonalità | OK (SymPy: momenti del nucleo del calore j ≤ 4, biortogonalità n,m ≤ 3) |
| T5.4 | (iv) casi (KdV–Burgers p = −Dκ², Airy, Schrödinger, AD, trasporto) | OK |
| P2.1 | (a) Rouché (r_a ∈ (0,∞]), formula integrale, proiettore di Riesz olomorfo | OK |
| P2.2 | (b) w^TC = λ_aw^T, (w)_k = 1/P′(λ_a), proiettore di Riesz | OK (SymPy k = 3) |
| P2.3 | (c) Kato = −T(λ_a)/P′(λ_a) = w^TC_Tv | OK (SymPy, anche differenza finita su radice perturbata) |
| P2.4 | esempi telegrafo/KG; raggio esatto 2\|ξ\|/\|γ\| | OK |

### 2.5 P3-T6 e verdetto §7.1
| MC | passo | esito |
|---|---|---|
| T6.1 | (i) 𝒱 limitato su H^k (ogni ∂^α𝒱f è 𝒱∂_x^jf o ∂_t^{i−1}∂_x^jf), traccia per m ≥ 1, identità q.o., unicità | OK (domanda 11) |
| T6.2 | (ii-a) variazione delle costanti con generatore limitato; (ii-b) ‖𝕂^n‖ ≤ (κ₀\|I\|)^n/n! (norma del massimo, N−1 termini fuori diagonale) | OK |
| T6.3 | (iii) risonanza secolare: ‖G_ca_cf_κ(t)‖ = \|c\|t‖∂ψ_κ‖ → ∞ a ‖f_κ‖ fisso | OK (SymPy) |
| T6.4 | (iv) pesi a_i/a; E^add = ΣE^{(i)}; coeff. di s²: a_i(a−a_i)/2 | OK. **T6-1** (MINOR): scrivere esplicitamente E^{(i)} = G_ia_iΣ_{j≠i}u^{(j)} (da (ii-a)): è esattamente l'E_int^{(i)} = −G_iV_iΣ_{j≠i}u^{(j)} di SCOUT-2 (V_i = −a_i); verificato simbolicamente. Senza questa riga la condizione (a) del criterio ("formula che lega E_int^Faddeev a E^add") non è visibilmente soddisfatta |
| T6.5 | (v) indipendenza lineare degli esponenziali; q_k ≠ 0 | OK |
| T6.6 | **(vi)** equivarianza ⇒ Σ ∈ {∅,[N]} ⇒ "L₀ = ∂_t è l'unica scelta equivariante non degenere" | **ERRORE — T6-vi (CRITICAL: INVALID + LOCAL, portante per il verdetto).** La prova quantifica solo sui riferimenti L₀^Σ. La famiglia L₀^θ := ∂_t − θΣ_ia_i(∂_x), θ ∈ [0,1), dà scomposizioni esatte u = S_θ(s)u₀ + Σ_iu_θ^{(i)}, u_θ^{(i)} := G_θ(1−θ)a_i(∂)u, simmetriche nei termini (equivarianti), non degeneri, con pesi a_i(e^{sa} − e^{θsa})/a dipendenti da θ; inoltre u_θ^{(i)}(t) = ∫_{t₀+θs}^{t}a_i(∂_x)u(ρ)dρ è anch'essa una quadratura di u (SymPy, KA-T6). L'enunciato è falso come scritto. **Fix (WEAKEN_CLAIM + ADD_DERIVATION):** (vi′) "tra i riferimenti L₀^Σ, Σ ⊆ [N], gli unici equivarianti sono Σ ∈ {∅,[N]}"; e come principio di selezione esplicito il **bilancio per termine**: (u^{(i)}) è l'unica N-upla con ∂_tu^{(i)} = a_i(∂_x)u e u^{(i)}(t₀) = 0 (è l'unicità già dimostrata in (i)); la famiglia θ lo viola per θ ∈ (0,1) (∂_su_θ^{(i)} = a_iu(t) − θa_iu(t₀+θs), verificato). Resta la dipendenza dal tempo base t₀ (scelta dell'inversa destra di ∂_t), da dichiarare |
| T6.7 | §7.1, contributo netto 1: "l'**unica** scomposizione additiva per termini esatta, lineare e continua in H^m" | **V-1 (MAJOR: OVERSTATED).** (i) dimostra l'unicità solo sotto le condizioni ∂_tu^{(i)} = a_iu, u^{(i)}(t₀) = 0; le u_θ^{(i)} sono per termini, esatte, lineari e continue H^m → H^{m−d_i} per θ ∈ (0,1). Fix: "l'unica N-upla con ∂_tu^{(i)} = a_i(∂_x)u e u^{(i)}(t₀) = 0; è continua in H^m, a differenza di E^add" |
| T6.8 | §7.0: criterio di SCOUT-2 riportato "nella sostanza" | OK (confrontato con research/SCOUT-2/REPORT.md r. 29). La clausola MERGE è aggiunta dall'autore; il criterio originale, se né PROMUOVI né ELIMINA scattano, è **silente** (la strada resta in SCOUTING) |
| T6.9 | (b) del criterio: caso L4 richiesto = trasporto + diffusione **a coefficiente variabile** | non testato: (ii-c) usa OU su ℂ[x]_{≤n} (dimensione finita, banale); (iii) è a coefficienti costanti. La dichiarazione "(b) non soddisfatta come scritta" è onesta |

**Domanda 12 (il verdetto segue dal criterio?).** No, non come registrato: la riga E1 di §7.1 si appoggia su (vi), che è falsa; la clausola MERGE è dell'autore e la sua precondizione ("interamente esprimibile con oggetti esistenti") è dimostrata ((v)) solo a coefficienti costanti, mentre il caso che il criterio chiedeva per (b) è a coefficiente variabile, dove il log-simbolo non esiste. Si veda §4 e la sezione kill-argument.

## 3. Rilievi e fix (proof-checker, Phase 2: proposti, non applicati)
| id | claim | categoria | stato/impatto | severità | strategia | fix |
|---|---|---|---|---|---|---|
| **T6-vi** | P3-T6(vi) | SCOPE_OVERCLAIM / INVALID | INVALID + LOCAL (portante per RT-S2a) | **CRITICAL** | WEAKEN_CLAIM + ADD_DERIVATION | come in T6.6: restringere a {L₀^Σ}; principio di bilancio per termine come selezione; dichiarare la dipendenza da t₀ |
| **T3-1** | P3-T3 "Lettura" (2) e portata di (iii) | SCOPE_OVERCLAIM | OVERSTATED + LOCAL (risposta a P1-Q5) | **MAJOR** | WEAKEN_CLAIM | "Lettura (2)" vale per dati modali finiti; per u₀ ∈ D(A₀) generale conta anche la seconda condizione di compatibilità A₀u₀ ∈ H¹₀ (u₀″ = 0 ai bordi): u₀ = x²(L−x)² ha Vu₀ ∈ H²∩H¹₀ e ‖E‖ ~ t^{7/4} (V-ex, pendenze 1.63 → 1.71 → 7/4). Aggiungere dopo (iii): "nulla si afferma per dati con infiniti modi; le costanti dipendono da N". Nuovo APERTO **P3-Q-bordo**: (α) ‖E^{mult,(1)}(t)u₀‖ = O(t^{5/4}) per ogni u₀ ∈ D(A₀)? (β) O(t^{7/4}) se Vu₀ ∈ H¹₀? (γ) l'ordine per dati compatibili (somme finite con S = 0: osservato > 2, pendenze 2.14, 2.24; (iii)(c) è solo un bound superiore) |
| **V-1** | §7.1 contributo netto 1 | SCOPE_OVERCLAIM | OVERSTATED + LOCAL | **MAJOR** | WEAKEN_CLAIM | come in T6.7 |
| T3-2 | P3-T3(v) | UNCLEAR | UNCLEAR + COSMETIC | MINOR | riformulare | "[D∂², −c∂] = 0 come espressione differenziale: tutto E^{mult,(1)} è di bordo; per e₁ il commutatore di operatori non è definito perché Ve₁ ∉ D(A₀)" |
| T3-3 | P3-T3(vi) | HIDDEN_ASSUMPTION | UNCLEAR + LOCAL | MINOR | precisare | E^{mult,(1)} esteso a u₀ ∈ D(V) = H¹; caso c < 0 con inflow in L |
| T3-4 | P3-T3(iii) | CONSTANT_DEPENDENCE_HIDDEN | — | MINOR | dichiarare | C, c′, t_* dipendono da N, A = Σn\|c_n\|, \|S\|, c, L, κ (non uniformi in N) |
| L2-1 | P3-L2(a) | LOGICAL_GAP (lieve) | — | MINOR | ADD_DERIVATION | lemma di continuità del prodotto |
| L2-2 | P3-L2(d) | REFERENCE_MISMATCH (numerazione) | — | MINOR | ADD_REFERENCE | Engel–Nagel III.3.14/3.16 → CIT-AUDIT |
| C1-1 | P3-C1(a),(b) | LOGICAL_GAP (lieve) | — | MINOR | ADD_DERIVATION | spettro dei moltiplicatori + Hille–Yosida |
| T2-1 | P3-T2 Lemma D | REFERENCE | — | MINOR | ADD_DERIVATION | formula di Cauchy per F_j (elimina la fonte de Boor) |
| T2-2 | P3-T2(e) | HIDDEN_ASSUMPTION | — | MINOR | STRENGTHEN_ASSUMPTION | espansioni finite o V-invarianza |
| P1-1 | P3-P1(c) | LOGICAL_GAP | — | MINOR | ADD_DERIVATION | caso c complesso: usare w → +∞ |
| T6-1 | P3-T6(iv) | MISSING_DERIVATION (lieve) | — | MINOR | ADD_DERIVATION | E^{(i)} = G_ia_iΣ_{j≠i}u^{(j)} = E_int^{(i)} di SCOUT-2 |

## 4. Conseguenze per LEDGER e ROUTES (proposte al coordinatore)
1. **P3-T3** DIMOSTRATO per gli enunciati (i)–(vi) come scritti (dati modali finiti), con l'esponente 5/4 confermato analiticamente (costante asintotica 2\|c\|√J κ^{1/4}/L, J ≈ 0.172028). La risposta a P1-Q5 va limitata: "al 1° ordine e per dati modali finiti, il bordo abbassa l'ordine da 2 a 5/4 esattamente quando (u₀′(0),u₀′(L)) ≠ 0"; per dati generali la gerarchia di compatibilità (5/4, 7/4 numerico, ≥ 2) è APERTA (P3-Q-bordo).
2. **P3-T6(vi)** FALSO come scritta; (vi′) ristretta alla famiglia {L₀^Σ} DIMOSTRATO.
3. **RT-S2a:** il verdetto "MERGE-INTO RT-2" **non è sostenuto come registrato** (kill-argument FAIL). Proposta: RT-S2a → **PARCHEGGIATA** (il criterio originale di SCOUT-2 è silente quando né PROMUOVI né ELIMINA scattano: E1 non scatta solo se si accetta il principio di bilancio per termine, che va dichiarato; (b) non è stata testata nel caso L4 richiesto). Indipendentemente dallo stato della strada, i lemmi **P3-T6(i), (iv), (v)** sono DIMOSTRATI e possono entrare in RT-2 come quadro (f) di P1-D3 a coefficienti costanti, con il contributo netto 1 riformulato (V-1). Criterio di riapertura: quello originale (b) di SCOUT-2, senza prescrivere il metodo (P3-Q4 riformulato: "convergenza del sistema N×N con ipotesi verificabili per trasporto + diffusione a coefficiente variabile, in qualunque spazio"). La scelta tra "PARCHEGGIATA" e "MERGE ristretto ai coefficienti costanti con il principio di bilancio dichiarato" è del coordinatore.
4. CIT-AUDIT: Engel–Nagel 2000 Thm III.3.14 / Cor. III.3.16 (Miyadera–Voigt). De Boor 2005 diventa superfluo con T2-1. Durán 1989 non usato (non serve verificarlo).

## 5. Red team SymPy (Phase 1.5) — `work/CHECK/sympy/audit_p3.py` → `audit_p3.out`
Esito: **30/30 OK** (riga TOTALE di audit_p3.out). Nota: gli esiti positivi KA-T3 e KA-T6 confermano i controesempi del kill-argument, cioè sono rilievi contro i claim, non conferme dei claim. Controlli: V_mn simbolico (m,n ≤ 8) e parità; T_nm e g; serie modale esatta di ‖E^{mult,(1)}(t)e₁‖ contro la previsione analitica 2\|c\|√Jκ^{1/4}t^{5/4}/L (rapporto → 1.00000); bound inferiore e superiore di (iii) con le costanti dichiarate (anche c_n complessi); dati compatibili e₁ − e₃/3 (ordine osservato > 2); controesempio del kill-argument u₀ = x²(1−x)² (coefficienti in forma chiusa verificati per quadratura; pendenze 1.63, 1.71 → 7/4); integrale di Beta; sup y^ke^{−sδy^q}; sup μ²e^{−2Dμ²s}; C1(a); Lemma D a punti ripetuti via formula di Cauchy; Dyson 1°–2° ordine via Van Loan; zero non reale di e^w−1−w; P3-T4 (forma chiusa dell'esponente per deg a = 2, 3, soluzione, altro ordine, grado esatto, Appell (f), commutatore); P3-T5 (momenti, biortogonalità, casi); P3-P2 (duale di Lagrange, Kato); P3-T6 (E^{(i)} = G_ia_iΣu^{(j)}, coefficiente s², famiglia θ, principio di bilancio, risonanza).
Candidati controesempio registrati: (1) famiglia L₀^θ contro P3-T6(vi) — **controesempio verificato** (simbolico/numerico); (2) u₀ = x²(L−x)² contro "Lettura (2)" di P3-T3 — **verificato numericamente** (V-ex: l'esponente 7/4 non è dimostrato); (3) nessun controesempio agli enunciati numerati di P3-T3, T1, L2, T2, T4, T5, P1, P2.

## 6. Kill-argument (cammino critico) — skill kill-argument, revisori = subagenti Claude freschi
Procedura: per ciascun bersaglio, Thread 1 (attacco, ~200 parole) e Thread 2 (arbitrato per punti) sono due subagenti Claude **distinti, lanciati senza il mio contesto** (al posto di Codex, decisione dell'utente); ciascuno ha letto solo un estratto autosufficiente copiato alla lettera dalla CHECK_REQUEST (work/CHECK/KA_P3_T3_input.md, work/CHECK/KA_RTS2a_input.md; il secondo include il testo originale del criterio di SCOUT-2) e, l'arbitro, il memo d'attacco (KA_*_attack.md). Il verdetto è calcolato da me con la tabella della skill, non dall'arbitro. Entrambi gli arbitri hanno verificato numericamente le affermazioni dell'attacco (riprodotte anche in audit_p3.py).

### 6.1 Bersaglio A — P3-T3 · **Verdetto: WARN** (reason_code: unresolved_major_or_minor)
**Memo d'attacco (verbatim):**
> **Rejection memo, P3-T3**
> 
> The computations in (i)–(iv) hold up. What fails is the theorem's main claim. The *Lettura* (2) says the dividing line is "exact and readable on the datum", namely $Vu_0\in H^1_0$, and that the alternative to $t^{5/4}$ is $t^2$. This is false outside the finite sine sums of (iii), and (iii) proves nothing beyond them.
> 
> A finite sine sum $u_0=\sum_{n\le N}c_ne_n$ automatically has $u_0''=0$ at both ends. So (iii)(c), through (iv), never has to face the extra condition $A_0u_0\in H^1_0$ that (iv) actually requires. That condition is a second compatibility condition, independent of $u_0'(0)=u_0'(L)=0$.
> 
> Counterexample: $u_0=x^2(L-x)^2$, with $L=c=D=1$. It lies in $D(A_0)$ and $Vu_0\in H^1_0$, but $u_0''(0)=2\neq0$. I evaluated the exact modal series of P3-P1(b), $E_m=\sum_nc_nV_{mn}T_{nm}$, keeping 6000 modes. The closed-form sine coefficients were checked by quadrature. The successive log–log slopes of $\lVert E^{mult,(1)}\rVert$ are 1.59, 1.67, 1.70, 1.72 for $t$ from $10^{-2}$ to $10^{-4}$, heading towards $7/4$ and not towards 2. The mechanism is the one in (iv): $\lVert\partial S_0(r)A_0u_0\rVert\sim r^{-1/4}$ in a boundary layer of width $\sqrt r$.
> 
> So the boundary does not produce a two-way split ($t^{5/4}$ or $t^2$). It produces a ladder of exponents, $5/4,\,7/4,\dots$, one step for each compatibility condition that fails. This exposes the "Θ versus $O(t^2)$" statement in (iii) as an accident of the finite-mode class. The constants also degrade without control: $C_1$ grows like $N\sum n|c_n|$ and $t_*\le|S|/(48A\kappa N^2)$ shrinks to 0 as $N$ grows. So nothing passes to the limit of general data.
> 
> The theorem as stated is correct but trivial, and the claim drawn from it is false.
> 

**Arbitrato (sintesi fedele, per punti):**
| punto | accusa | classificazione | severità |
|---|---|---|---|
| P1 | il controesempio x²(L−x)² (Vu₀ ∈ H²∩H¹₀, A₀u₀ ∉ H¹₀, ‖E‖ ~ t^{7/4}) confuta la "Lettura (2)" (discrimine esatto Vu₀ ∈ H¹₀, alternativa t²) | **still_unresolved** (arbitro: slopes 1.593…1.736, stabili al raddoppio dei modi; ‖E‖/t^{7/4} → 0.44–0.45) | major |
| P2 | (iii) "banale", nulla per dati generali | partially_answered ("dati modali finiti" è dichiarato; (iii)(b) è un vero bound bilatero; manca un'osservazione di portata) | major |
| P3 | (iii)(c) nasconde la seconda condizione A₀u₀ ∈ H¹₀ | answered_by_current_text (la condizione è un'ipotesi esplicita di (iv) ed è verificata per le somme finite) | minor |
| P4 | costanti degradano con N | partially_answered | minor |
| P5 | "scala" 5/4, 7/4, … | partially_answered (sopra 7/4 la scala si ferma a 2 per (iv); 7/4 è solo numerico) | minor |
Conteggi: answered 1, partially 3, still_unresolved 1 (major), nessun critical → **WARN**. Valutazione netta dell'arbitro: enunciati (i)–(vi) corretti come scritti (stime di (iii) ricontrollate a mano, e₁ riprodotto); la "Lettura (2)" è falsa fuori dai dati modali finiti; l'attacco esagera chiamando la Lettura "il claim principale" e il teorema "banale". Azioni: (1) riscrivere la Lettura (2) — fix T3-1; (2) osservazione di portata dopo (iii) — T3-1/T3-4; (3) dimostrare O(t^{5/4}) su D(A₀) e O(t^{7/4}) se Vu₀ ∈ H²∩H¹₀, oppure dichiararli aperti — P3-Q-bordo.
**Esito per lo stato:** il kill-argument non colpisce gli enunciati numerati → P3-T3 resta DIMOSTRATO con il fix T3-1 obbligatorio (portata).

### 6.2 Bersaglio B — verdetto "RT-S2a MERGE-INTO RT-2" e P3-T6 · **Verdetto: FAIL** (reason_code: unresolved_critical)
**Memo d'attacco (verbatim):**
> **Rejection memo: "RT-S2a MERGE-INTO RT-2" and P3-T6**
> 
> The verdict rests on P3-T6(vi), and (vi) is false. The proof only compares the reference operators $L_0^\Sigma$ indexed by subsets $\Sigma\subseteq[N]$. That family was chosen by the session, not forced by the problem. The family $L_0^\theta=\partial_t-\theta\sum_i a_i(\partial_x)$, $\theta\in[0,1)$, also gives exact decompositions. Every member is permutation-equivariant and non-degenerate. Its weights are $a_i(e^{sa}-e^{\theta sa})/a$, so the components change with $\theta$. So $L_0=\partial_t$ is not "l'unica scelta equivariante non degenere", and equivariance selects nothing. E1 therefore fires, and by the scout's own criterion the outcome is ELIMINA, not a merge.
> 
> The MERGE clause cannot repair this. The session wrote it itself, for exactly the case where (b) fails. Its precondition is that the content is "interamente" expressible through the log-symbol, and (v) proves that only for finite exponential sums at constant coefficients. Item (b) asked for the variable-coefficient L4 case, where no log-symbol exists. There the exact Volterra balance and the $N\times N$ system are the scout route's only distinctive content, and (ii-c) tests only OU on polynomials, a trivial finite-dimensional subspace. The merge discards that regime and then sets a harder bar for reopening (P3-Q4) than PROMUOVI required.
> 
> Contributo netto item 1 is also false. The uniqueness in (i) holds only among tuples that already satisfy $\partial_t u^{(i)}=a_i(\partial_x)u$ and $u^{(i)}(t_0)=0$. The split $u^{(i)}=u/N$ is exact, linear and continuous in $H^m$, so "l'unica" is an overclaim. The decision should be rejected.
> 

**Arbitrato (sintesi fedele, per punti):**
| punto | accusa | classificazione | severità |
|---|---|---|---|
| P1 | (vi) falsa: famiglia L₀^θ esatta, equivariante, non degenere, componenti dipendenti da θ ⇒ la riga E1 crolla | **still_unresolved** (verificato con mpmath, 3 termini, θ ∈ {0, 0.3, 0.6}, errore ~1e-16; anche le componenti θ sono quadrature di u) | **critical** |
| P2 | allora E1 scatta ⇒ ELIMINA | partially_answered: un principio che seleziona ∂_t esiste implicitamente in (i) (bilancio per termine ∂_tu^{(i)} = a_iu, tempo base fisso), ma non è mai invocato né argomentato; resta la dipendenza da t₀ | critical |
| P3 | clausola MERGE autoprodotta; "interamente log-simbolo" provato solo a coefficienti costanti | partially_answered (aggiunta dichiarata prima della valutazione, ma il criterio originale, se silente, lascia la strada in scouting; destinazione RT-2 sbagliata per la parte a coefficienti variabili) | major |
| P4 | (b) non testata nel caso L4 richiesto (coefficiente variabile); (ii-c) banale | partially_answered (concessione onesta, caso non tentato) | major |
| P5 | "l'unica scomposizione … continua in H^m" è un overclaim | **still_unresolved** (anche le u_θ^{(i)} sono per termini, esatte, lineari, continue) | major |
| P6 | E^{(i)} = E_int^{(i)} di SCOUT-2? | answered_by_current_text (segue da (ii-a)/(ii-b); verificato; manca la riga esplicita) | minor |
Conteggi: answered 1, partially 3, still_unresolved 2 (di cui 1 critical) → **FAIL**. Valutazione netta dell'arbitro: la decisione non regge sui motivi registrati; riscritta (principio di selezione esplicito, unicità corretta, merge limitato ai coefficienti costanti) è difendibile, ma la sopravvivenza dipende dall'accettare il principio di bilancio come principio e non come definizione scelta per ottenere la risposta. Azioni: (1) ritirare (vi) e sostituirla con un principio di selezione esplicito che escluda θ-famiglia e riferimenti simmetrici generali, poi rifare la riga E1; (2) correggere il contributo netto 1; (3) registrare "criterio silente → resta in scouting" oppure limitare il MERGE ai coefficienti costanti, allineando P3-Q4 a (b) originale.
**Esito per lo stato:** T6-vi CRITICAL confermato in modo indipendente (§2.5, audit_p3.py KA-T6); proposta al coordinatore in §4.3.

### 6.3 Concordanza con l'audit
Il kill-argument ha prodotto due rilievi che l'audit per passi da solo non aveva rilevato con questa forza: il controesempio di portata x²(L−x)² (T3-1) e la famiglia θ (T6-vi). Entrambi sono stati verificati da me in audit_p3.py prima di registrarli. Nessun rilievo del kill-argument contraddice un passo che l'audit aveva dato per OK negli enunciati numerati di P3-T3.
