# AUDIT II-T4 — proiettori spettrali razionali ⟺ fattori
Revisore: S-CHECK-2B · 25/10/2026
Fonte esaminata: SOLO `work/II/CHECK_REQUEST.md` §II-T4 (con F1′ e II-T2 dello stesso file).
Skill: session-protocol, claim-lifecycle, proof-checker, scientific-critical-thinking, sympy.
SymPy: `work/CHECK/sympy/audit_ii.py` → `audit_ii.out` sezione "II-T4" (OK, 6 controlli); `audit_round2.out` (OK).

**Verdetto: PASS** (solo rilievi MINOR di esposizione; la risposta alla domanda di S-II è "sì").

## 1. Enunciato canonico
P ∈ ℂ[ξ][τ] monico di grado k; K = ℂ(ξ); radici distinte τ_a ∈ K̄ con molteplicità μ_a; S ⊆ {radici}; Π_S = proiettore spettrale di C su ⊕_{a∈S} ker(C−τ_a)^{μ_a} lungo ⊕_{a∉S}; Q_S = Π_{a∈S}(τ−τ_a)^{μ_a}. Tesi: (1) Π_S ∈ Mat_k(K) ⟺ (2) Q_S ∈ K[τ] ⟺ (3) Q_S ∈ ℂ[ξ][τ] ed è un fattore di P coprimo col cofattore.

## 2. Micro-claim
| MC | Passo | Esito |
|---|---|---|
| MC-1 | Π_S = g(C), g ∈ K̄[τ], deg g < k, g ≡ 1 mod (τ−τ_a)^{μ_a} (a∈S), ≡ 0 (a∉S) | OK (CRT in K̄[τ] + decomposizione primaria; C non derogatoria con polinomio minimo P, F1′). MINOR: ADD_REFERENCE (calcolo funzionale olomorfo/di Hermite, es. Higham, *Functions of Matrices*, Def. 1.4 e Thm 1.12, numerazione da verificare) |
| MC-2 | (1)⇒ g ∈ K[τ] | OK: I,…,C^{k−1} indipendenti su K̄ (F1′); il sistema Σg_iC^i = Π_S ha coefficienti e termine noto in K, rango k, soluzione unica in K̄ ⇒ in K (Cramer su k equazioni indipendenti) |
| MC-3 | gcd_{K̄[τ]}(P, g−1) = Q_S, **con le molteplicità** | OK. Risposta alla domanda: ord_{τ_a} gcd = min(ord_{τ_a}P, ord_{τ_a}(g−1)) = min(μ_a, ≥ μ_a) = μ_a per a ∈ S; per b ∉ S, (g−1)(τ_b) = −1 ⇒ ordine 0; le radici di (g−1) che non sono radici di P non contano. Quindi il gcd monico è esattamente Q_S. Verificato su (τ−ξ)²(τ+ξ), S = {ξ}: ord_{τ=ξ}(g−1) = 2, gcd = (τ−ξ)² |
| MC-4 | gcd invariante per estensione del campo ⇒ Q_S ∈ K[τ] | OK (Euclide in K[τ]) |
| MC-5 | (2)⇒(3): Gauss | OK: ℂ[ξ] UFD (basta integralmente chiuso); Q_S e P/Q_S senza radici comuni ⇒ coprimi |
| MC-6 | (3)⇒(1) via II-T2(b) con s = 2 | OK: la parte generica (su K) di II-T2(b) non è toccata dall'errore II-T2-F1 (che riguarda solo la specializzazione in ξ₀). Π_S(Hermite) = N/r di II-T2 verificato su (τ−ξ)²(τ+ξ) |
| MC-7 | (2)⇒(1) | OK (stessa via di MC-6) |

## 3. Problemi trovati
- **II-T4-F1 · esposizione · MINOR.** Nella prova il blocco "⇐" mescola (2)⇒(1) (via II-T2) e (2)⇒(3) (Gauss). La catena logica completa è (1)⇒(2) [MC-2..4], (2)⇒(3) [MC-5], (3)⇒(2) [banale], (2)⇒(1) [MC-6]. *Fix:* riordinare (ADD_DERIVATION testuale).
- **II-T4-F2 · completamento · MINOR.** Conviene enunciare la conseguenza: S dà un proiettore razionale ⟺ S è unione delle radici di alcuni fattori irriducibili di P su K (con molteplicità piena); quindi i proiettori razionali sono esattamente 2^r, r = numero di fattori irriducibili distinti. Controlli: τ² − ξ e (τ² − ξ)² con S = {√ξ} danno Π_S non razionale (contiene √ξ).
- **Dipendenza da II-T2:** usa solo la parte generica, quindi il verdetto non dipende dal fix II-T2-F1. Se però si usa II-T4 per affermare che Π_S(ξ₀) è "il proiettore lungo il complemento spettrale" in un ξ₀ speciale, vale la versione corretta di II-T2 (nucleo = ker B(ξ₀,C₀)).

## 4. Red team
| Tentativo | Esito |
|---|---|
| fattore irriducibile, S non chiuso per Galois (τ² − ξ, S = {√ξ}) | Π_S irrazionale: coerente |
| fattore non ridotto ((τ²−ξ)², S = {√ξ}, μ = 2) | irrazionale: coerente |
| molteplicità piena (τ−ξ)² nel non ridotto (τ−ξ)²(τ+ξ) | razionale, gcd con molteplicità corretta |
| possibile "molteplicità parziale" | esclusa dalla definizione di Π_S e Q_S (μ_a pieno) |

## 5. Stato proposto
**DIMOSTRATO** (risultato di algebra lineare su K; novità bassa, ma è il raccordo esatto tra "componente = fattore" (G★′) e i proiettori della compagna: utile e corretto).
