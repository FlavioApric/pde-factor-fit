# KA input SYS-EX — preparato da S-CHECK-F8-SYS (27/10/2026). Testo estratto VERBATIM da work/S8-SYS/PROOF_PACKAGE.md (righe 10, 15–20, 38–84): notazione, lemmi usati, enunciato, ipotesi e prova. Compito del revisore: kill-argument (trovare un controesempio o un passo falso nell'enunciato SYS-EX o nei lemmi da cui dipende).

Fatti esterni citati dall'autore (non dimostrati nel testo): iniettività di C^∞(ℝ^n) e 𝒟′(ℝ^n) come ℂ[∂]-moduli (Ehrenpreis–Malgrange–Palamodov); normalizzazione di Noether; mappa finita = rivestimento non ramificato fuori da un chiuso di Zariski proprio; luogo liscio di una varietà irriducibile connesso e Zariski-denso; Nullstellensatz; Stone–Weierstrass; principio d'identità.

**Notazione.** R = ℂ[ζ_1, …, ζ_n], con ζ_j ↔ ∂_j (per i sistemi di evoluzione ζ = (τ, ξ) ↔ (∂_t, ∂_x)). Ω ⊂ ℝ^n è un aperto, 𝒜 ∈ {C^∞(Ω), 𝒟′(Ω)}. Le righe agiscono a sinistra: P ∈ R^{l×k} agisce su u ∈ 𝒜^k. U_P := R^{1×l}P ⊆ R^{1×k} è il modulo delle righe e M_P := R^{1×k}/U_P. Sol_𝒜(P) ≅ Hom_R(M_P, 𝒜). Per u ∈ 𝒜^k: Ann(u) := {r ∈ R^{1×k} : r(∂)u = 0}, M_u := R^{1×k}/Ann(u), e φ_u : M_P → 𝒜, [r] ↦ r(∂)u, che è ben definita se u ∈ Sol(P). Ann(u)/U_P = ker φ_u. "u identifica P" significa Ann(u) = U_P, cioè φ_u iniettiva. Per un ideale massimale m: soc_m(M) := Hom_R(R/m, M) = {x ∈ M : m x = 0}; m_λ := (ζ_1 − λ_1, …, ζ_n − λ_n). EP indica gli esponenziali-polinomi. Modello di dato: DM3 (u noto esattamente) in tutto il pacchetto, salvo G-T2, che usa DM-inv.

### [SYS-L0] Test d'iniettività su un sottomodulo essenziale — standard
Sia φ : M → F un omomorfismo di R-moduli e sia E ⊆ M essenziale (ogni sottomodulo non nullo di M interseca E in modo non banale). Allora φ è iniettiva se e solo se φ|_E è iniettiva.
*Prova.* ker φ ∩ E = ker(φ|_E). Se questo è 0, ker φ è un sottomodulo che interseca E banalmente, quindi è nullo per essenzialità. ∎

### [SYS-L1] Famiglia essenziale — standard (prova in `research/F6-SYS/NOTE.md` §1)
Sia M finitamente generato. Esiste una famiglia finita x_{p,j} ∈ M, con p ∈ Ass(M) e j = 1, …, μ_p, tale che R x_{p,j} ≅ R/p, la somma E := Σ R x_{p,j} è diretta ed E è essenziale in M. Per p = m massimale, μ_m ≤ dim_ℂ soc_m(M): le copie di R/m nella somma diretta generano un sottospazio di soc_m(M) di dimensione μ_m. Si ha anzi μ_p = μ_0(p, M), il numero di Bass (Matsumura, *Commutative Ring Theory*, §18; numerazione da verificare), ma nel seguito serve solo la disuguaglianza.

### [SYS-N1] Ostruzione di zoccolo — prova scritta
*Enunciato.* Sia Ω connesso e sia M un R-modulo. Se dim_ℂ soc_m(M) ≥ 2 per qualche ideale massimale m = m_λ, nessun omomorfismo M → 𝒜 è iniettivo. In particolare, se ciò vale per M = M_P, nessuna u ∈ Sol_𝒜(P) identifica P.
*Prova.* Un omomorfismo φ manda soc_{m_λ}(M) in {f ∈ 𝒜 : (∂_j − λ_j) f = 0 ∀ j}. Su Ω connesso questo spazio è ℂ e^{λ·x}: si scrive f = e^{λ·x} g, si ha ∇g = 0 in 𝒟′(Ω), e quindi g è costante (anche per le distribuzioni, su un aperto connesso). Un'applicazione lineare da uno spazio di dimensione ≥ 2 a uno di dimensione 1 non è iniettiva. ∎

### [EX-L1] Unicità di Fourier–Laplace sui momenti — prova scritta
*Enunciato.* Sia ν una misura boreliana complessa a supporto compatto in ℂ^n, e sia Λν(x) := ∫ e^{ζ·x} dν(ζ). Se Λν = 0 su un aperto non vuoto Ω ⊆ ℝ^n, allora ∫ h dν = 0 per ogni polinomio h ∈ ℂ[ζ].
*Prova.* Λν si estende a una funzione intera di x ∈ ℂ^n (si deriva sotto il segno d'integrale: il supporto è compatto). Una funzione intera nulla su un aperto non vuoto di ℝ^n è nulla: per il principio d'identità tutte le sue derivate si annullano in un punto di Ω. Allora ∂_x^α Λν(0) = ∫ ζ^α dν = 0 per ogni α. ∎

### [EX-L2] Sezioni reali di una varietà irriducibile — prova scritta (con fatti standard di geometria algebrica)
*Enunciato.* Sia q ⊂ R un primo con d := dim V(q) ≥ 1. Esistono forme lineari ℓ = (ℓ_1, …, ℓ_d), un aperto connesso U ⊆ ℂ^d con U ∩ ℝ^d ≠ ∅ e un'applicazione olomorfa s : U → V(q) con ℓ ∘ s = id_U, tali che:
(a) s(U) è un aperto (euclideo) di V(q);
(b) se r ∈ R si annulla su s(B) per una palla reale B ⊂ U ∩ ℝ^d, allora r ∈ q.
*Prova.* Normalizzazione di Noether: esistono forme lineari ℓ_1, …, ℓ_d con ℂ[ℓ] ↪ R/q finita, quindi π := ℓ|_{V(q)} : V(q) → ℂ^d è finita e suriettiva. Esiste un chiuso di Zariski proprio Δ ⊊ ℂ^d (luogo di diramazione più immagine del luogo singolare) fuori dal quale π è un rivestimento finito non ramificato di punti lisci (fatto standard: Shafarevich, *Basic Algebraic Geometry* 1, cap. II; numerazione da verificare). Δ non contiene alcun aperto non vuoto di ℝ^d, perché ℝ^d è Zariski-denso in ℂ^d. Si sceglie allora un punto reale y_0 ∉ Δ, una palla complessa U ∋ y_0 disgiunta da Δ e un foglio s del rivestimento sopra U: s(U) è aperto in V(q), quindi vale (a). Per (b): r ∘ s è olomorfa su U connesso e nulla su una palla reale di dimensione d, che è un insieme d'unicità per le funzioni olomorfe di d variabili; quindi r ∘ s ≡ 0 su U e r si annulla sull'aperto s(U) del luogo liscio di V(q). Il luogo liscio di una varietà irriducibile è connesso e Zariski-denso, quindi r si annulla su V(q) e r ∈ I(V(q)) = q per il Nullstellensatz (q è primo, dunque radicale). ∎
Per q = 0 (V = ℂ^n) si prende ℓ = id, U = ℂ^n e s = id.

### [SYS-EX] Criterio d'esistenza — prova scritta (bersaglio di F8)
*Enunciato.* Sia Ω ⊆ ℝ^n un aperto connesso **qualsiasi** (non serve la convessità), sia 𝒜 ∈ {C^∞(Ω), 𝒟′(Ω)} e sia M un R-modulo finitamente generato. Sono equivalenti:
(i) esiste un omomorfismo iniettivo M ↪ 𝒜;
(ii) dim_ℂ soc_m(M) ≤ 1 per ogni ideale massimale m di R.
In particolare, per P ∈ R^{l×k}: **esiste u ∈ Sol_𝒜(P) che identifica P ⟺ dim_ℂ Hom_R(R/m, M_P) ≤ 1 per ogni m massimale.** In tal caso u si può prendere in C^∞(Ω).

*Prova.* (i) ⇒ (ii) è SYS-N1.

(ii) ⇒ (i). Si fissa una famiglia essenziale {x_{p,j}} di M (SYS-L1) e si pone E = ⊕ R x_{p,j} ≅ ⊕_p (R/p)^{μ_p}. Per (ii) e SYS-L1 si ha μ_m ≤ 1 per ogni primo massimale m. La prova ha tre passi.

*Passo 1 (funzioni per i primi non massimali).* Per ogni primo q ∈ Ass(M) non massimale si fissano ℓ, U, s come in EX-L2 e μ_q palle reali chiuse B_{q,1}, …, B_{q,μ_q} ⊂ U ∩ ℝ^d, a due a due disgiunte. Si pone
  f_{q,j}(x) := ∫_{B_{q,j}} e^{s(y)·x} dy  (x ∈ ℝ^n).
f_{q,j} è la restrizione di una funzione intera e r(∂) f_{q,j} = ∫_{B_{q,j}} r(s(y)) e^{s(y)·x} dy. Se r ∈ q, allora r(s(y)) = 0, perché s(y) ∈ V(q); dunque q f_{q,j} = 0. Per i primi massimali m_λ ∈ Ass(M), che hanno μ = 1, si pone f_λ(x) := e^{λ·x}. Esempio (SymPy G3): per q = (τ − ξ²) (calore) con ℓ = ξ e s(y) = (y², y), f(t, x) = ∫_0^1 e^{y² t + y x} dy risolve f_t = f_xx.

*Passo 2 (ψ : E → C^∞(ℝ^n), x_{p,j} ↦ f_{p,j}, è ben definita e iniettiva anche ristretta a Ω).* La buona definizione segue dal Passo 1. Per l'iniettività di E → C^∞(Ω) si procede come nella prova di SYS-T1: altrimenti esistono q ∈ Ass(M) e una relazione su Ω
  Σ_j r_{q,j}(∂) f_{q,j} + Σ_{p ⊋ q} Σ_j r_{p,j}(∂) f_{p,j} = 0  con qualche r_{q,j} ∉ q.
- Se q è massimale, la relazione contiene solo il termine r(∂)e^{λ·x} = r(λ)e^{λ·x} (non ci sono primi ⊋ q), quindi r(λ) = 0 e r ∈ m_λ: contraddizione.
- Se q non è massimale, il primo membro è Λν per la misura a supporto compatto ν = ν_q + ν′, dove ν_q := Σ_j s_*((r_{q,j} ∘ s) 1_{B_{q,j}} dy) e ν′ è supportata in ∪_{p ⊋ q} V(p) (pezzi s_p(B) e punti λ). Per EX-L1, ∫ h dν = 0 per ogni polinomio h.
  - Si sceglie h_0 ∈ ∏_{p ⊋ q} p con h_0 ∉ q. È possibile: ogni p ⊋ q non è contenuto in q e q è primo. h_0 si annulla su ∪_{p ⊋ q} V(p), quindi h_0 ν′ = 0.
  - Con h = h_0 · g(ℓ), dove g è un polinomio qualsiasi in d variabili, si ottiene Σ_j ∫_{B_{q,j}} g(y) F_j(y) dy = 0, con F_j := (h_0 ∘ s)(r_{q,j} ∘ s), continua sull'unione disgiunta dei compatti B_{q,j}.
  - Per Stone–Weierstrass i polinomi complessi g sono densi in C(∪_j B_{q,j}): l'algebra è chiusa per coniugio sulle variabili reali y e separa i punti. Quindi ogni F_j ≡ 0 su B_{q,j}.
  - h_0 ∘ s è olomorfa e non identicamente nulla su U, per EX-L2(b) applicato a h_0 ∉ q. Quindi il suo luogo di zeri in B_{q,j} ha misura nulla, r_{q,j} ∘ s = 0 su un sottoinsieme denso di B_{q,j}, e per continuità ovunque su B_{q,j}. Per EX-L2(b) r_{q,j} ∈ q per ogni j: contraddizione.

*Passo 3 (estensione da E a M).* C^∞(ℝ^n) è un R-modulo iniettivo (principio fondamentale di Ehrenpreis–Malgrange–Palamodov; Malgrange, Sém. Bourbaki exp. 246, 1962–63, vol. 8, pp. 79–89; Oberst 1990; CON-FONTE). Quindi ψ : E → C^∞(ℝ^n) si estende a Ψ : M → C^∞(ℝ^n). Sia ρ_Ω la restrizione a Ω. ker(ρ_Ω ∘ Ψ) ∩ E = ker(ρ_Ω ∘ ψ) = 0 per il Passo 2, quindi ρ_Ω ∘ Ψ è iniettiva per SYS-L0. Poiché C^∞(Ω) ⊂ 𝒟′(Ω), lo stesso omomorfismo è un'immersione anche in 𝒟′(Ω).

*Ultima frase.* Con M = M_P e φ l'immersione, si pone u := (φ(e_1), …, φ(e_k)) ∈ C^∞(Ω)^k, dove e_i sono le classi dei vettori unitari. Allora r(∂)u = φ([r]), quindi u ∈ Sol(P) e Ann(u) = {r : [r] ∈ ker φ} = U_P. ∎

*Osservazioni.*
1. La prova non usa l'iniettività di C^∞(Ω), che è falsa per Ω non P-convesso (§3.3). Usa solo quella di C^∞(ℝ^n) e la rigidità delle funzioni intere costruite.
2. **[SYS-EX-C] Corollario (Bass di C^∞).** Per p non massimale, (R/p)^N ↪ C^∞(Ω) per ogni N (Passo 2 con M = (R/p)^N); per m massimale si ha dim soc_m(C^∞(Ω)) = 1. Su Ω convesso, dove C^∞(Ω) è iniettivo: μ_p(C^∞(Ω)) = ∞ per p non massimale e μ_m = 1. È la verifica chiesta da O8 ("molteplicità di E(R/p) in C^∞").
3. La u identificante non è mai EP se M_P non ha lunghezza finita (SYS-R1).
4. Decidibilità: la condizione (ii) è calcolabile, perché soc_m(M) ≠ 0 solo per m ∈ Ass(M), i primi associati massimali si ottengono per decomposizione primaria di moduli (Eisenbud–Huneke–Vasconcelos 1992), e dim soc_m = dim_ℂ Hom(R/m, M) è algebra lineare su un quoziente di lunghezza finita (Hom(R/m, M) = Hom(R/m, H^0_m(M))). Il test su una u **data** resta invece non certificabile da dati finiti (C3-P1).
