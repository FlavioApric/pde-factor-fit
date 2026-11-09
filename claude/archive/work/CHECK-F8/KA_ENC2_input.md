# KA ENC2 — input per l'attaccante (S-CHECK-F8-ENC-rev2, 27/10/2026)

Estratto verbatim da `work/S8-ENC/PROOF_PACKAGE.md` rev. 2 (righe indicate). Bersagli: **ENC-P0(b)^cl** (con la variante ENC-P0(b)^loc) ed **ENC-T2(c′)**. Notazione: L_q := −∂_x² + q(x), L_0 := −∂_x²; S = ℂ[τ, σ] con σ ↔ L_q; Ann_q(u) := {P ∈ S : P(∂_t, L_q)u = 0}; φ(P)(τ, ξ) = P(τ, −ξ²); W è l'operatore di trasformazione di Volterra (encoder) di q, con W L_q = L_0 W; DM3 = il dato è u stesso (nessuna equivalenza). Fatti esterni dati per buoni: ENC-1 (W e T = W^{−1} di Volterra, biiettivi su C^k(J), iniettivi su C⁰, J intervallo simmetrico attorno a x_0).

## Righe 156–158 (ENC-C1, ipotesi richiamate da ENC-T2)
**[ENC-C1] Corollario (prova scritta).** Ipotesi di ENC-1 con q ∈ C^∞(J°), Ω = I × J° (I intervallo aperto) e u ∈ C^∞(Ω). Per ogni P ∈ S:

   P(∂_t, L_q)u = 0 ⟺ P(∂_t, L_0)(Wu) = φ(P)(∂_t, ∂_x)(Wu) = 0.

## Righe 170–174 (ENC-T2, enunciato)
**[ENC-T2] Lemma (prova scritta; SymPy `enc_algebra` (b) 6/6, `enc_s8b` (c) 2/2).** Ipotesi di ENC-C1. **q è noto**: il lemma non identifica q. Se q non è dato, l'uso del lemma per l'identificazione B1 è circolare (DEVIL-6 O6). Modello di dato: DM3 su Ω = I × J°, rettangolo simmetrico attorno a x_0.
- (a) Ann_q(u) = φ^{−1}(Ann(Wu)) = φ^{−1}(Ann(Wu) ∩ ℂ[τ, ξ²]).
- (b) Se Ann(Wu) = (Q) con Q ≠ 0, allora Ann_q(u) = (P_*) è principale, con φ(P_*) = lcm(Q, Q̃) se questo è pari in ξ, e φ(P_*) = ξ·lcm(Q, Q̃) se è dispari. Si ha sempre lcm(Q, Q̃)~ = ±lcm(Q, Q̃).
- (c) (*Getti.*) Per ogni N la mappa j^N_{(t_0, x_0)}u ↦ j^N_{(t_0, x_0)}(Wu) è ben definita, lineare e triangolare unipotente. Dipende solo dal getto di q in x_0 di ordine N − 2. In particolare (Wf)(x_0) = f(x_0), (Wf)′(x_0) = f′(x_0) e (Tf)″(x_0) = f″(x_0) + q(x_0)f(x_0). **W non conserva i getti, li trasforma in modo triangolare.** L'induzione vale per ogni ordine (risposta a D5 del revisore).
- (c′) (*Osservazione elementare, non usa W; fix ENC-6(a); DA AUDITARE.*) Sia P_* ≠ 0. Per **ogni** punto (t_1, x_1) ∈ Ω e ogni N, nessun getto finito j^N u in (t_1, x_1) certifica Ann_q(u) = (P_*).

## Righe 190–194 (prova di ENC-T2(c′))
(c′) Nella prima versione era provata solo in x_0, perché T non è locale fuori da x_0 (T2c2 dell'audit). Ecco una prova diretta in ogni punto.

Sia d := deg_σ P_*(τ, σ) e sia p_d(τ) il coefficiente di σ^d. Si sceglie α ∈ ℂ con p_d(α) ≠ 0. Si pone h := e^{αt}(x − x_1)^M con M > max(N, 2d). Allora L_q^j(x − x_1)^M = (−1)^jM!/(M − 2j)!·(x − x_1)^{M−2j} + (potenze più alte di x − x_1), perché q aumenta il grado. Quindi P_*(α, L_q)(x − x_1)^M = p_d(α)(−1)^dM!/(M − 2d)!·(x − x_1)^{M−2d} + (ordini superiori) ≢ 0 (`enc_recep` 1/1).

Dunque j^N h = 0 in (t_1, x_1) e P_*(∂_t, L_q)h = e^{αt}P_*(α, L_q)(x − x_1)^M ≠ 0. Ne segue che u′ := u + h ha lo stesso N-getto di u e P_* ∉ Ann_q(u′). ∎

## Righe 242–264 (ENC-P0(b), ENC-P0(b)^cl, ENC-P0(b)^loc)
**[ENC-P0(b)] Nessun encoder indipendente dal tempo in L² (prova scritta; non usa il propagatore).** Siano ℋ = L²(J), H_0 autoaggiunto, V(t) = moltiplicazione per V(t, ·) ∈ L^∞(J), e c(t) scalare ammessa in (INT). Sia W ∈ B(ℋ), con WD ⊂ D, indipendente da t, con **dim ker W < ∞ su ℋ** ((E1) sul dominio dell'encoder, fix ENC-14). Allora V(t, ·) − V(s, ·) = c(t) − c(s) q.o. per ogni t, s.

*Prova.* Con W′ = 0, (INT) dà (H_0 + c(t))Wψ = WH(t)ψ per ψ ∈ D. Sottraendo t e s: W m ψ = 0 per ψ ∈ D, con m := V(t) − V(s) − (c(t) − c(s)). Siccome m è limitato, D è denso e ker W è chiuso, si ottiene W m = 0 su ℋ, cioè Ran(m) ⊂ ker W.

Se |{m ≠ 0}| > 0, esistono ε > 0 e infiniti insiemi disgiunti E_k ⊂ {|m| > ε} di misura **finita** e positiva. Le funzioni m·1_{E_k} ∈ Ran(m) sono linearmente indipendenti, contro dim ker W < ∞. ∎

*Portata (fix ENC-4).* In L²(J) con J limitato, H_0 autoaggiunto impone condizioni al bordo che l'encoder di Volterra di ENC-1 non rispetta, per cui W ∉ 𝔈. Quindi P0(b), letto alla lettera, **non** esclude un encoder di tipo ENC-1 per V(t, x).

C'è anche un argomento spettrale (KA P0, P4). In L²(J) un W ∈ 𝔈 con nucleo finito forza σ(H_V) − c ⊂ σ(H_0), a meno di un numero finito di autovalori: la classe è quasi vuota già per V autonomo. Per questo l'enunciato di riferimento è la versione classica che segue.

**[ENC-P0(b)^cl] Versione classica (prova scritta; testo del revisore, fix ENC-4; DA AUDITARE come claim nuovo).** Siano J un intervallo aperto, V ∈ C(I × J) e c ∈ C(I). Sia W: C^∞(J) → C^∞(J) lineare, con dim ker W < ∞ (su C^∞(J)), tale che

   W(−∂_x² + V(t, ·))f = (−∂_x² + c(t))Wf per ogni t ∈ I e ogni f ∈ C^∞_c(J).

Equivalentemente: W agisce solo in x e intreccia i u_t = L_{V(t)}u con i v_t = (L_0 + c(t))v sulle funzioni C^∞ di (t, x). Allora V(t, x) − V(s, x) = c(t) − c(s) per ogni t, s, x.

*Prova.* Sottraendo le identità in t e in s si ha W(mf) = 0 per ogni f ∈ C^∞_c(J), con m := V(t, ·) − V(s, ·) − (c(t) − c(s)) continua. Se m(x*) ≠ 0, allora m ≠ 0 su un intervallo U ∋ x*. Si scelgono φ_1, φ_2, … ∈ C^∞_c(U) non nulle a supporti disgiunti: le mφ_k sono linearmente indipendenti e stanno in ker W, contro dim ker W < ∞. ∎

Copre l'encoder di Volterra di ENC-1 (iniettivo su C⁰, quindi con nucleo nullo).

**[ENC-P0(b)^loc] Versione localizzata (prova scritta; fix ENC-14; DA AUDITARE).** Sia U ⊂ J aperto. Sia W lineare, definito almeno su C^∞_c(U), con dim ker W|_{C^∞_c(U)} < ∞, tale che l'identità di P0(b)^cl valga per ogni f ∈ C^∞_c(U). Allora V(t, ·) − c(t) è autonomo su U.

*Prova.* Quella di P0(b)^cl, con le funzioni φ_k supportate in U. ∎
