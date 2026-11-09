# KA input ENC-P0 — preparato da S-CHECK-F8-ENC (27/10/2026). Testo estratto VERBATIM da work/S8-ENC/PROOF_PACKAGE.md (righe 15, 33–42, 192–250) e da NOTAZIONE.md v5 (riga 111). Il kill-argument interno dell'autore (§10) è stato tolto. Compito del revisore: kill-argument su ENC-P0 — in particolare P0(b) "nessun encoder strutturato per V(t,x) davvero non autonomo che commuti con ∂_t" e P0′ "le eccezioni cambiano il tempo" (lente, Avron–Herbst, classe quadratica di Bluman–Shtelen), più P0(a) e POLE-N: controesempi, passi falsi, ipotesi vuote o incoerenti con gli esempi, sovrastime di portata.

Fatti esterni usati dall'autore e NON riportati qui: VAR-P11 (propagatore per H_0 = −∂² e V(t) moltiplicazione limitata continua in norma; continuità nella norma del grafo CON-FONTE Pazy cap. 5); Bluman–Shtelen 1996 §2 (le trasformazioni puntuali + gauge che mandano i u_t = −u_xx + V(t,x)u nel libero esistono solo per V = α(t)x² + β(t)x + γ(t) reale); ENC-1 (encoder di Volterra W_q indipendente dal tempo con W_q L_q = L_0 W_q su C²(J), J = [x_0 − a, x_0 + a] compatto, senza condizioni al bordo).

## Da NOTAZIONE.md v5
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

## 4. ENC-P0: intertwiner non autonomi, eccezioni che cambiano il tempo

**Ipotesi (H-P0).**
- ℋ è uno spazio di Hilbert e H_0 è autoaggiunto con dominio D := D(H_0).
- V ∈ C(ℝ; B(ℋ)) è continuo in norma, con valori autoaggiunti, e H(t) := H_0 + V(t).
- Esiste un propagatore unitario U_V(t, s), fortemente continuo, con U_V(t, s)D ⊂ D, continuo in t nella norma del grafo su D, e con i∂_tU_V(t, s)ψ = H(t)U_V(t, s)ψ e i∂_sU_V(t, s)ψ = −U_V(t, s)H(s)ψ per ψ ∈ D. Questo è CON-FONTE (Dyson–Phillips: Pazy cap. 5, Reed–Simon II §X.12, numeri da verificare). Per H_0 = −∂² e V(t) moltiplicazione limitata e continua in norma, l'esistenza è VAR-P11 di S8-VAR (prova scritta).
- U_V(t) := U_V(t, 0) e U_0(t) := e^{−itH_0}.

*Classe 𝔈 degli encoder ammessi:* W: ℝ → B(ℋ) fortemente continua, con W(t)D ⊂ D, e t ↦ W(t)ψ di classe C¹ per ψ ∈ D.

*Intrecciamento:*

   (INT) iW′(t)ψ = (H_0 + c(t))W(t)ψ − W(t)H(t)ψ per ogni ψ ∈ D,

con c ≡ 0 per (E2) stretta e c costante per (E2′) (NOTAZIONE v5). Il caso di una c(t) funzione è trattato in (b).

**[ENC-P0(a)] Classificazione a tempo fissato (prova scritta, regolarità del propagatore CON-FONTE).** Per W ∈ 𝔈 e c ≡ 0:

   W soddisfa (INT) ⟺ W manda soluzioni forti in soluzioni forti libere ⟺ W(t) = U_0(t)W(0)U_V(t)^{−1} per ogni t.

*Prova.*

(⇒) Sia u_0 ∈ D, u(t) := U_V(t)u_0 e g(t) := W(t)u(t). Si scrive

   [W(t + h)u(t + h) − W(t)u(t)]/h = W(t + h)(u(t + h) − u(t))/h + (W(t + h) − W(t))u(t)/h.

Il primo termine tende a W(t)u′(t): W è localmente limitata per Banach–Steinhaus ed è fortemente continua. Il secondo tende a W′(t)u(t) perché u(t) ∈ D. Quindi ig′ = iW′u + W(iu′) = (H_0W − WH)u + WHu = H_0g, con g(t) ∈ D.

Unicità per l'equazione libera: per lo stesso argomento, d/dt[U_0(−t)g(t)] = U_0(−t)(g′ + iH_0g) = 0. Quindi g(t) = U_0(t)g(0), cioè W(t)U_V(t)u_0 = U_0(t)W(0)u_0 su D denso, e per limitatezza su tutto ℋ.

(⇐) Sia M := W(0) ∈ 𝔈. Allora MD ⊂ D, e M è limitato nella norma del grafo per il teorema del grafo chiuso (H_0M|_D è chiuso). Per ψ ∈ D, φ(t) := U_V(0, t)ψ è C¹ in ℋ e continua nella norma del grafo. Quindi U_0(t)Mφ(t) è derivabile, e il calcolo diretto, usando φ′ = iU_V(0, t)H(t)ψ, dà (INT).

L'equivalenza con "soluzioni in soluzioni" è il contenuto di (⇒), letto all'indietro. ∎

**[ENC-P0(b)] Nessun encoder indipendente dal tempo se V dipende davvero dal tempo (prova scritta).** Ipotesi (H-P0) con ℋ = L²(J), V(t) = moltiplicazione per V(t, ·) ∈ L^∞(J), e una funzione scalare c(t) ammessa in (INT). Se W ∈ 𝔈 non dipende da t e ha dim ker W < ∞ (E1), allora V(t, ·) − V(s, ·) = c(t) − c(s) q.o. per ogni t, s. Quindi V(t, x) = V_0(x) + c(t), la cui dipendenza dal tempo si toglie con il gauge e^{−i∫c}. In particolare, per V che dipende davvero da t, non esiste alcun encoder strutturato indipendente dal tempo, nemmeno modulo costanti.

*Prova.* Con W′ = 0, (INT) dà (H_0 + c(t))Wψ = WH(t)ψ per ogni t. Sottraendo le uguaglianze in t e in s: W[V(t) − V(s) − (c(t) − c(s))] = 0, cioè Ran(m) ⊂ ker W con m := V(t) − V(s) − (c(t) − c(s)).

L'operatore di moltiplicazione per m ∈ L^∞ ha rango finito solo se m = 0 q.o. Se |{m ≠ 0}| > 0, esistono infiniti insiemi disgiunti E_k ⊂ {|m| > ε} di misura positiva, per un opportuno ε > 0, e le funzioni m·1_{E_k} ∈ Ran sono linearmente indipendenti. ∎

*Lettura.* Questa è la forma "elementare" chiesta da DEVIL-6 O6.3, rafforzata da "iniettivo" a "nucleo finito" e da c = 0 a c(t) qualsiasi.

**[ENC-P0′] Eccezioni che cambiano il tempo (prova scritta; SymPy `enc_algebra` P0′ 3/3).** Ipotesi (H-P0). Siano θ ∈ C¹(I) con θ′ > 0 e θ(0) = 0 (I ∋ 0 intervallo) e W ∈ 𝔈|_I. Supponiamo che W mandi soluzioni in soluzioni libere **riparametrizzate**: per ogni u_0 ∈ D, v(θ(t)) := W(t)U_V(t)u_0 è una soluzione forte di iv_τ = H_0v su θ(I). Allora

   W(t) = U_0(θ(t)) W(0) U_V(t)^{−1}, t ∈ I.

*Prova.* v(τ) = U_0(τ)v(0) per l'unicità della soluzione libera (come in (a)) e v(0) = W(0)u_0. ∎

*Esempio: la lente di Niederer.* Si prendono H = −½∂² + ½x², H_0 = −½∂², θ = tan, W(0) = I e I = (−π/2, π/2). La formula puntuale

   u(t, x) = (cos t)^{−1/2}e^{−ix² tan t/2}v(tan t, x/cos t)

coincide quindi con W(t)^{−1} = U_osc(t)U_0(tan t)^{−1}. È un quadro d'interazione con cambio di tempo che *risulta* locale. Le eccezioni "quadratiche" di F6-ENC non sono eccezioni a P0(a): sono elementi di P0′ con θ ≠ id. Quali W di P0′ siano puntuali più gauge è la classificazione di Bluman–Shtelen 1996 §2 per V reale: V = α(t)x² + β(t)x + γ(t), CON-FONTE verificata in CIT-AUDIT-6 voce 16. Con trasformazioni **non locali** esistono anche V non quadratici, quindi "solo quadratico" vale solo per gli encoder puntuali.

**[POLE-N] Strada POLE: esito negativo per Schrödinger (prova scritta).** Sia V(t, ·) una famiglia (per esempio razionale di Adler–Moser, con poli che si muovono per KdV/Calogero–Moser: AMM 1977, CON-FONTE) con intertwiner istantanei W(t), cioè W(t)L_{V(t)} = (L_0 + c)W(t) per ogni t, con W ∈ 𝔈 e nucleo finito. Allora W è un encoder per i u_t = L_{V(t)}u solo se V non dipende da t.

*Prova.* (INT) con W(t)H(t) = (H_0 + c)W(t) dà iW′ = 0. Quindi W è costante e si conclude con P0(b). ∎

*Lettura.* Gli intertwiner di Darboux dipendenti dal tempo funzionano per il **flusso di Lax** (ψ_t = B_3ψ nella gerarchia KdV), non per Schrödinger nel suo tempo. La strada POLE è utile solo per quell'equazione, che è di terzo ordine in x. Per B2 si richiude.
