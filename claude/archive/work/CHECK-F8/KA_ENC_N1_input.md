# KA input ENC-N1 — preparato da S-CHECK-F8-ENC (27/10/2026). Testo estratto VERBATIM da work/S8-ENC/PROOF_PACKAGE.md (righe 15, 33–42, 254–283) e da NOTAZIONE.md v5 (righe 100, 110–111). Il kill-argument interno dell'autore (§10) è stato tolto. Compito del revisore: kill-argument su ENC-N1 (F6) dichiarato FALSO e su ENC-N1′ (encoder cieco ⟺ identificabilità congiunta, sotto (S)): trovare un controesempio, un passo falso, una definizione mal posta o una sovrastima di portata.

Fatti esterni usati dall'autore e NON riportati qui (trattarli come ipotesi): VAR-T1(b) (con u ∈ C^{1,2}, u ≢ 0, Schrödinger con V(x) noto in forma: q = (iu_t + u_xx)/u q.o.; V identificato q.o.), VAR-P4(a) (con DM-φ gli stati stazionari identificano solo V − E), VAR-T1(c) (fasce di silenzio per V(t,x)), ENC-P0(b) (nessun encoder strutturato indipendente dal tempo per V(t,x) davvero non autonomo), SYS-N3 (non identificabilità di (A,V) magnetico in n ≥ 2), ENC-1 (encoder di Volterra simmetrico W_q con W_q L_q = L_0 W_q su J = [x_0 − a, x_0 + a], q ∈ C¹, normalizzato dai dati di Cauchy in x_0).

## Da NOTAZIONE.md v5
- **DM-φ**: dato noto a meno della fase temporale globale (u ~ e^{iφ(t)}u). Con DM-φ gli stati stazionari identificano solo V − E (VAR-P4 = ENC-N2(a)); con la fase osservata il dato identifica q.
- E_int è sempre quello di A9 (v3). **E^conj**: difetto di coniugazione di un encoder (ex "E" di F6-ENC), da non confondere con E_int.
- **Encoder (E2) modulo costanti** (F6-ENC (E1)–(E3); allentamento di DEVIL-6 O7): W L_q = (L_0 + c) W per qualche costante c (stazionario, W commuta con ∂_t), oppure W(t)(i∂_t − H(t)) = (i∂_t − H_0 − c)W(t) nel caso non autonomo; q costante non ha intertwiner differenziale con c = 0.

## Notazione (PROOF_PACKAGE riga 15)
**Notazione.** L_q := −∂_x² + q(x), L_0 := −∂_x², H_0 := L_0 su L²(ℝ). R := ℂ[τ, ξ] (τ ↔ ∂_t, ξ ↔ ∂_x). S := ℂ[τ, σ] (σ ↔ L). φ: S → R, φ(P)(τ, ξ) := P(τ, −ξ²). Per Q ∈ R, Q̃(τ, ξ) := Q(τ, −ξ). Ann_q(u) := {P ∈ S : P(∂_t, L_q)u = 0}. Ann(v) ⊆ R è l'annullatore di C3-T1. I modelli di dato sono quelli di NOTAZIONE v5 (DM1–DM3, DM-φ, DM-inv). E_int è sempre quello di A9; E^conj è il difetto di coniugazione di un encoder.

## 1. Che cosa è un encoder; definizione (E2) modulo costanti

**[ENC-D] Definizione (prova scritta della buona posizione, non è un teorema).** Sia J un intervallo e sia q dato. Un *encoder strutturato* per L_q è un operatore lineare W, definito su uno spazio di funzioni 𝒴 (precisato caso per caso: C²(J), C^∞(J), L²(J)), con le tre proprietà seguenti:
- (E1) W è iniettivo, oppure ha nucleo di dimensione finita noto;
- (E2′) *modulo costanti*: W L_q = (L_0 + c)W per qualche c ∈ ℂ; quindi W commuta con ∂_t quando agisce solo in x. Nel caso non autonomo la condizione diventa W(t)(i∂_t − H(t)) = (i∂_t − H_0 − c)W(t). La versione stretta (E2) è c = 0;
- (E3) W è esplicito: differenziale, puntuale più gauge, oppure di Volterra con nucleo dato da un problema ben posto.

Con c ≠ 0 la soluzione libera è definita a meno del fattore e^{−ict}, cioè della fase globale di DM-φ. (E2′) è la scelta registrata in NOTAZIONE v5.

**[ENC-O1] Osservazione (banale).** Senza (E1)–(E3) la richiesta è vuota. W = 0 va bene, e su ℝ va bene anche il quadro d'interazione W(t) = U_0(t)U_V(t)^{−1} (F6-ENC NOTE §1).

## 5. ENC-N1: encoder cieco e identificabilità

**Quadro.**
- 𝒟 è lo spazio dei dati, con un'equivalenza ~ (DM3: uguaglianza; DM-φ: u ~ e^{iθ(t)}u).
- 𝒱 è una classe di potenziali. Per ogni V ∈ 𝒱, 𝒮_V ⊂ 𝒟 è l'insieme delle soluzioni, chiuso per ~ e contenente 0.
- Per ogni V c'è un encoder strutturato W_V: 𝒮_V → 𝒮_0^{(c_V)}, lineare e iniettivo, compatibile con ~, verso le soluzioni libere a meno della costante c_V ((E2′)).
- 𝒪 := classi delle uscite modulo ~ e modulo le costanti, e 𝒰 := ∪_V 𝒮_V.
- Un *encoder cieco* è una mappa E: 𝒰 → 𝒪 con E(u) = [W_V u] per ogni V e ogni u ∈ 𝒮_V.
- *Identificabilità (congiunta)* su 𝒰: per u ∈ 𝒮_V ∩ 𝒮_{V′} con u ≁ 0 si ha V = V′. Allora anche la componente libera v = W_V u è determinata.

**[ENC-N1 (F6)] FALSO come scritto.** "Esiste un encoder cieco ⟺ Φ(V, v) := W_V^{−1}v è iniettiva su 𝒱 × 𝒮." *Controesempio:* 𝒱 = {V(x) ∈ C¹(J)} con DM3 ed encoder di Volterra (ENC-1). Φ(V, 0) = 0 = Φ(V′, 0) per V ≠ V′, quindi Φ non è iniettiva. Eppure l'encoder cieco esiste, per il punto (iii) qui sotto con VAR-T1(b).

**[ENC-N1′] Teorema (prova scritta).** Nel quadro sopra:
- (i) Un encoder cieco esiste ⟺ vale la **coerenza** (C): per ogni V, V′ e ogni u ∈ 𝒮_V ∩ 𝒮_{V′}, [W_V u] = [W_{V′}u]. Equivalentemente: Φ(V, v) = Φ(V′, v′) ⇒ [v] = [v′] (la componente libera è identificabile, il potenziale non necessariamente).
- (ii) L'identificabilità congiunta implica (C), quindi l'encoder cieco esiste. È costruttivo se l'identificazione lo è: E(u) = [W_{V(u)}u].
- (iii) Con l'ipotesi di **separazione** (S) — per V ≠ V′ e u ∈ 𝒮_V ∩ 𝒮_{V′}, u ≁ 0, si ha [W_V u] ≠ [W_{V′}u] — vale: **encoder cieco ⟺ identificabilità congiunta**. È la forma richiesta dal roster.
- (iv) Senza (S) la freccia "cieco ⇒ identificabile" è **falsa**. *Controesempio:* si considerano DM-φ, 𝒱 = {q_0 + c : c ∈ ℝ} con q_0 ∈ C¹(J) reale, e la famiglia (E2′) normalizzata W_{q} := W_{q̂} con q̂ := q − q(x_0) (encoder di Volterra di q̂). Si ha W_{q̂}L_q = (L_0 + q(x_0))W_{q̂}. Tutti i potenziali della classe hanno lo stesso q̂, quindi lo stesso encoder, e (C) vale. Dunque l'encoder cieco esiste: E([u]) = [W_{q̂}u]. Ma V è identificato solo modulo costanti (VAR-P4(a)). Qui (S) fallisce.
- (v) *Istanze.*
  - V(x) ∈ C¹, DM3, Volterra stretto: l'identificabilità vale per VAR-T1(b), anzi 𝒮_V ∩ 𝒮_{V′} = {0} per V ≠ V′, quindi (S) vale a vuoto. L'encoder cieco esiste ed è costruttivo: q = (iu_t + u_xx)/u nei punti u ≠ 0 (per onda e calore, q = (u_xx − u_tt)/u e q = (u_xx − u_t)/u), poi il Goursat (G).
  - V(t, x): per P0(b) non esiste un encoder strutturato indipendente dal tempo, quindi la domanda sull'encoder cieco strutturato è vuota. L'identificazione puntuale stessa può fallire su fasce di silenzio (VAR-T1(c)).
  - Schrödinger magnetico in n ≥ 2: l'identificabilità di (A, V) fallisce (SYS-N3 di S8-SYS). Coerentemente, un encoder cieco che tolga A non è disponibile.

*Prova.*
- (i) Se E esiste, (C) è la sua buona definizione. Viceversa, (C) dice che [W_V u] non dipende dalla scelta di V con u ∈ 𝒮_V.
- (ii) Se u ∈ 𝒮_V ∩ 𝒮_{V′} e u ≁ 0, allora V = V′ e (C) è banale. Se u ~ 0, allora [W_V u] = [0] per linearità.
- (iii) ⇐ è (ii). ⇒: se esistessero V ≠ V′ con u ≁ 0 comune, (S) darebbe [W_V u] ≠ [W_{V′}u], contro (C).
- (iv) Si verifica W_{q̂}L_{q_0 + c} = W_{q̂}(L_{q̂} + q_0(x_0) + c) = (L_0 + q_0(x_0) + c)W_{q̂}. La compatibilità con ~ segue dal fatto che W_{q̂} agisce solo in x.
- (v) Rimandi citati. ∎

*Lettura.* "Encoder cieco = identificazione congiunta" vale solo con (S). Il contenuto non banale non è l'equivalenza logica, ma: (a) quali classi soddisfano l'identificabilità (S8-VAR); (b) che con DM-φ ed (E2′) l'encoder cieco esiste lo stesso; (c) che per V(t, x) la domanda è vuota (P0(b)). ENC-N2(a) di F6-ENC coincide con VAR-P4 (DM-φ) ed è contata una volta sola (fix F9).
