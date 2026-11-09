# AUDIT R2-T3 — G1 come uguaglianza (somma di termini)
Revisore: S-CHECK (secondo revisore di claim-lifecycle, niente Codex) · 25/10/2026
Fonte esaminata: SOLO enunciato, ipotesi e prova di `research/R2/REPORT.md` §4 (e, perché la prova li invoca, gli enunciati di R2-T1 e R2-T2 in §2–§3).
Skill caricate: session-protocol, claim-lifecycle, proof-checker (workflow Phase 0.5 → 1 → 1.5 → 3.5; io sono il reviewer), scientific-critical-thinking, sympy.
SymPy: `work/CHECK/sympy/audit_r2t3.py` → `audit_r2t3.out`, **ESITO GLOBALE: OK** (30 coppie, di cui 25 casuali coprime, più i controlli 2–5 sotto).

## 1. Enunciato canonico (Phase 0.5, quantificatori espliciti)
R = ℂ[∂_1,…,∂_n] (coefficienti costanti, commutativo). 𝒜 un R-modulo.
- (a) ∀𝒜, ∀L₁,L₂ ∈ R, L := L₁+L₂: `ker L ∩ (ker L₁ + ker L₂) ⊆ Sol_𝒜(R/(L, L₁L₂))`, e `(L, L₁L₂) = (L, L₁²)`.
- (b) Se 𝒜 ∈ {C^∞(Ω), D'(Ω)}, Ω ⊂ ℝⁿ aperto convesso (ipotesi di R2-T1), e gcd(L₁,L₂)=1: uguaglianza.
- (c) n = 2, L₁, L₂ coprimi, **𝒜 ∈ {C^∞(Ω), D'(Ω)} con Ω convesso (quindi connesso)**: `dim_ℂ Sol_𝒜(R/(L,L₁²)) = Σ_p I_p(L,L₁²) = 2·Σ_p I_p(L₁,L₂) < ∞`, base di esponenziali-polinomi a frequenze in V(L₁)∩V(L₂).
- (d) In generale (𝒜 come in (b)): `ker L ∩ (ker L₁+ker L₂) = ker L ∩ ker lcm(L₁,L₂)`; se h = gcd non costante e n ≥ 2, `ker h ⊆ ker L₁ ∩ ker L₂ ∩ ker L` ha dimensione infinita.
- (e) N termini, 𝒜 come in (b): `Σ_n ker L_n = ker lcm(L₁,…,L_N)`, `ker L ∩ Σ_n ker L_n = Sol(R/(L, lcm))`.

## 2. Registro delle ipotesi e dipendenze (DAG)
R2-T3(a) ← commutatività di R (elementare).
R2-T3(b) ← R2-T2.2 ← R2-T1(a) [iniettività di C^∞/D' su convessi: Malgrange–Ehrenpreis–Palamodov; Hörmander ICASV 3a ed. Thm 7.6.13, numerazione VERIFICATA solo su fonte secondaria (CIT-AUDIT: Lomadze 2013)] — CON-FONTE.
R2-T3(c) ← Fulton, *Algebraic Curves*, cap. 3 (proprietà degli indici di intersezione: I_p(F,GH)=I_p(F,G)+I_p(F,H); I_p(F,G)=I_p(F,G+AF); Σ_p I_p = dim R/(F,G) per F,G coprimi) — CON-FONTE; ← "Hom_R(R/I,𝒜) ≅ (R/I)^* per I 0-dimensionale" (R2-T2.5; Sturmfels 2002 cap. 10 / Oberst 1990) — CON-FONTE.
R2-T3(d),(e) ← R2-T2.1, induzione su N (lcm(L₁…L_N) = lcm(lcm(L₁…L_{N−1}),L_N)).
Nessun ciclo.

## 3. Micro-claim e verifica (Phase 1, checklist A–H)
| MC | Passo | Esito |
|---|---|---|
| MC-1 | u=u₁+u₂ ⇒ L₁L₂u = L₂L₁u₁ + L₁L₂u₂ = 0 | corretto (commutatività) |
| MC-2 | (L₁+L₂, L₁L₂) = (L₁+L₂, L₁²) perché L₂ ≡ −L₁ mod L | corretto |
| MC-3 | coprimi ⇒ lcm = L₁L₂ ⇒ ker L₁L₂ = ker L₁+ker L₂ (T2.2) ⇒ "⊇" | corretto dato T1(a) |
| MC-4 | V(L, L₁²) = V(L₁)∩V(L₂) | corretto (su V(L₁): L=0 ⟺ L₂=0) |
| MC-5 | I_p(L, L₁²) = 2 I_p(L, L₁) = 2 I_p(L₂, L₁) | corretto (Fulton; L e L₁ senza componenti comuni perché gcd(L₁,L₂)=1) |
| MC-6 | dim Sol_𝒜(R/J) = dim R/J per J 0-dimensionale | **corretto solo se 𝒜 contiene tutti gli esponenziali-polinomi e Ω è connesso**: vedi I-1 |
| MC-7 | (e) per induzione | corretto (non scritta, ma immediata) |

## 4. Problemi trovati (tassonomia e severità proof-checker)
- **I-1 · HIDDEN_ASSUMPTION · UNCLEAR/LOCAL · MINOR.** (c) è enunciato per "𝒜 iniettivo" ma il conteggio di dimensione richiede 𝒜 = C^∞(Ω) o D'(Ω) con Ω **connesso** (per Ω con k componenti la dimensione è k volte; per 𝒜 = polinomi si vedono solo le frequenze 0). Con Ω convesso (ipotesi di T1) è automatico. *Fix:* STRENGTHEN_ASSUMPTION testuale: "𝒜 come in R2-T1".
- **I-2 · UNPROVEN_SUBCLAIM · UNJUSTIFIED/LOCAL · MINOR.** La prova di (c) non richiama esplicitamente MC-6 (è in T2.5); (e) è dichiarata "idem" senza induzione. *Fix:* ADD_DERIVATION di una riga (fatta sopra, MC-6, MC-7).
- **I-3 · SCOPE (trasferimento a H1 della Fase 3) · UNCLEAR/GLOBAL · MAJOR→ chiuso qui.** H1 = H^m(Ω) non è un R-modulo (le derivate abbassano la regolarità), quindi T3 non si applica letteralmente a u ∈ H^m(Ω). Si legge in D'(Ω) (Ω = I×(a,b) è convesso). Resta da vedere che le componenti u₁, u₂ stiano ancora in H^m(Ω). **Lemma aggiunto da S-CHECK (ADD_DERIVATION):** se u ∈ ker L ∩ ker L₁² in D'(Ω) e u = u₁+u₂ con u_i ∈ ker L_i, allora u₁ ∈ Sol(R/(L₁, L₂²)) (0-dimensionale), quindi u₁, u₂ sono esponenziali-polinomi e stanno in H^m(Ω) per ogni m (Ω limitato).
  *Prova.* Sia J = (L, L₁²) ⊆ Ann(u). L₂u₁ = L₂u − L₂u₂ = L₂u. Per q ∈ J: q·L₂u₁ = L₂·(qu) = 0, quindi u₁ è annullato da (L₁) + L₂J ∋ L₂L = L₂L₁ + L₂², cioè da (L₁, L₂²). V(L₁,L₂²) = V(L₁)∩V(L₂) è finito (n=2, coprimi), quindi Sol(R/(L₁,L₂²)) è di dimensione finita e fatto di esponenziali-polinomi (MC-6). ∎ Verificato in SymPy sull'esempio con collisione in (0,0) e (1,−1) (controllo 2: le quattro scomposizioni esplicite hanno u₁ ∈ ker L₁ ∩ ker L₂²).
- **I-4 · REFERENCE_MISMATCH · UNCLEAR/LOCAL · MINOR.** La numerazione Hörmander 7.6.13 è verificata solo su fonte secondaria (CIT-AUDIT). Non tocca la verità (il principio fondamentale sui convessi è classico: Malgrange 1956, Ehrenpreis 1970, Palamodov 1970), ma va citata con la 3a ed. e con una fonte primaria.
Nessun FATAL, nessun CRITICAL.

## 5. Red team (Phase 1.5)
| Tentativo | Esito |
|---|---|
| 25 coppie casuali coprime di grado ≤ 2 + 5 coppie del catalogo: dim R/(L,L₁²) vs 2·dim R/(L₁,L₂) | sempre uguali (controllo 1) |
| Collisione a frequenza non nulla (L₁ = ∂_t−∂_x², L₂ = ∂_t+∂_x, V = {(0,0),(1,−1)}): base di Sol(R/(L,L₁²)) e scomposizione di ogni elemento | dim 4, base {1, t−2x, e^{t−x}, (t−2x/3)e^{t−x}}, tutte scomposte (controllo 2) — la "⊇" di (b) regge |
| Togliere l'iniettività: I×𝕋, L₁ = ∂_t+∂_x, L₂ = −∂_t+∂_x², u = t | Lu = 0, L₁²u = 0, su ℝ t = (t−x)+x, su 𝕋 il modo 0 dà ker = costanti ∌ t: **(b) falso senza iniettività** — l'ipotesi è necessaria, coerente con R2-C1 (controllo 3) |
| Togliere la coprimalità: L₁ = ∂_t∂_x, L₂ = ∂_x² | R/(L,L₁²) non 0-dimensionale (controllo 4): (c) cade, (d) lo prevede |
| Termini monomiali nella stessa variabile (∂_x², ∂_x) | gcd ≠ 1 sempre: (b)–(c) non si applicano; serve (d) con lcm — già detto nel report |

## 6. Riconciliazione con R5 (obiezione O6 di DEVIL-A, "G1 '=' non riconciliato tra R2 e R5")
R5-P4 è esattamente R2-T3(a) (inclusione, ogni modulo). R5 lascia "=" APERTO (Q3); R2-T3(b) lo chiude sotto le ipotesi coprimi + 𝒜 iniettivo. L'esempio di R5 (L₂ = −∂_x, ideale (ξ², τ−ξ), nucleo span{1, x+t}) e quello di R2 (L₂ = +∂_x, ideale (ξ², τ+ξ)) sono due scissioni diverse e danno entrambe dim 2 = 2·I_0 (controllo 1). La "dim 4" citata in RIPRESA §4A per l'avvezione–diffusione è un'altra scissione ancora (trasporto ∂_t+c∂_x contro diffusione −D∂_x², I_0 = 2), anch'essa verificata. **Nessun conflitto**; la dimensione dipende dalla scissione L = L₁+L₂ scelta, e questo va scritto quando si cita "dim 4" o "dim 2".

## 7. Acceptance gate e stato proposto
Gate: 0 FATAL/CRITICAL ✔; ipotesi esplicite dopo I-1 ✔; applicazioni di T1/T2 con ipotesi scaricate ✔ (Ω convesso); nessun O(·) ✔; controesempi tentati ✔.
**Stato proposto: DIMOSTRATO** per (a) (elementare) e per (b)–(e) con le ipotesi "𝒜 = C^∞(Ω) o D'(Ω), Ω ⊂ ℝ² convesso" (dipendenza CON-FONTE: R2-T1(a), Fulton, dualità di Macaulay). Il lemma I-3 lo rende utilizzabile in Fase 3 per u ∈ H^m(Ω), Ω = I×(a,b). Nessun declassamento a V-ex: la prova è generale, gli esempi SymPy sono solo controllo.
Kill-argument: non richiesto (non sul cammino critico identificazione/fattori/E_int; è il risultato di impossibilità di A8 per somma di termini).
