# AUDIT di VAR-L2-cor e campione del recepimento post-Gate 8 (S-CHECK-F8-VAR, 27/10/2026)

**Oggetto.** VAR-L2-cor, come appare in `work/S8-VAR/PROOF_PACKAGE.md` §1.3 (dopo VAR-L2) e in `LEDGER_ROWS.md` (riga 13, stato DA AUDITARE).

**Campione del recepimento post-Gate 8.** ATTACK-8 O3, O8 e O17, più la citazione per VAR-L2 (CIT-AUDIT-8 §5, punto 2).

**Fonti lette.**
- `PROOF_PACKAGE.md`: Convenzioni, §1.3, §1.5, §1.6, §4.2, §4.3, §9 (righe VAR-16 e VAR-L1), §10, §11.
- `LEDGER_ROWS.md` e `RECEPIMENTO.md` (sezione «post-Gate 8»).
- `open_questions.md` (VAR-Q17, VAR-Q18).
- `research/DEVIL/ATTACK-8.md` (O3, O8, O17, O20).
- `research/CIT-AUDIT/AUDIT-8.md` (A8, A9, B4, §5).

**Script del revisore.** `sympy/var2_l2cor.py`, con uscita `var2_l2cor.out`: TUTTO OK, 12 controlli. Il metodo è indipendente da quello dell'autore, che per VAR-L2-cor non ha script.

## 0. Verdetto

| claim | verdetto | stato proposto |
|---|---|---|
| VAR-L2-cor (V ∈ C¹([0,T]; L^∞), dati in D(H_0)) | **PASS-con-fix.** L'argomento proprio è corretto riga per riga. L'unico anello non dimostrato è VAR-P11(e), oggi CON-FONTE. | **Oggi: CON-FONTE**, perché eredita P11(e); non citabile da righe DIMOSTRATO (resta il vincolo O20). **Dopo il fix VAR-L2c-1: DIMOSTRATO.** |
| VAR-P11(e) | La prova autosufficiente esiste ed è breve: §2 qui sotto (fix VAR-L2c-1). | CON-FONTE → DIMOSTRATO quando l'autore la inserisce nel PP e un revisore diverso dall'estensore la riscontra (vedi §2, nota finale) |
| (nuovo, proposta) VAR-L2-cor(b): V = V(x) ∈ L^∞(J; ℝ), dati in L² | La prova del revisore è nel §3. Chiude VAR-Q17 **nel caso autonomo** e non usa P11(e). | proposta: «prova scritta (revisore)», da inserire dall'autore; VAR-Q17 resta APERTO per V dipendente da t |
| Recepimento O3 / O8 / O17 | **conforme** (§4) | — |
| Citazione per VAR-L2 (Isakov 1993, non Saut–Scheurer) | **conforme** nell'osservazione di §1.3 e nel LEDGER. Resta un residuo MINOR nella tabella dei fix, §9 (VAR-L2c-7). | — |

Non ci sono errori analitici. Ci sono un rilievo MAGGIORE e alcuni MINORI.
- **MAGGIORE.** Il CON-FONTE di P11(e) è chiudibile con la prova del §2.
- **MINORE.** Vale solo per la clausola «mai a tempo fisso», che è vera solo se ω non è denso in J.

## 1. VAR-L2-cor: ipotesi e prova riga per riga

**Enunciato (PP §1.3).** Siano dati:
- J ⊂ ℝ un intervallo aperto e I = (0, T);
- V ∈ C¹([0, T]; L^∞(J; ℝ));
- ω ⊂ J aperto non vuoto;
- H_0 = −∂² autoaggiunto su L²(J), con D(H_0) ⊂ H²(J);
- ψ, ψ̃ soluzioni con dati in D(H_0).

Allora ψ = ψ̃ q.o. su I × ω implica ψ_0 = ψ̃_0.

### 1.1 Ipotesi

| ipotesi | serve a | giudizio |
|---|---|---|
| V ∈ C¹([0,T]; L^∞(J)) | B(t) = −iV(t) ∈ C¹([0,T]; 𝓛(L²)) in norma, perché ‖V(t)‖_{𝓛(L²)} = ‖V(t)‖_∞; serve per P11(e) | corretta e sufficiente |
| V reale | autoaggiunzione e unitarietà dell'evoluzione | **non usata dalla prova**: P11(e) vale per B limitato qualunque e VAR-L0–L2 assorbono \|Vw\| ≤ ‖V‖_∞\|w\| senza usare la realtà di V. Si può togliere, oppure lasciarla dichiarando che è solo per il contesto unitario (VAR-L2c-5, facoltativo). |
| D(H_0) ⊂ H²(J) | regolarità spaziale | **automatica**: ogni estensione autoaggiunta di −∂² su C_c^∞(J) è una restrizione dell'operatore massimale, il cui dominio è {f ∈ L²: f″ ∈ L²} = H²(J), su qualunque intervallo. La frase «per J ≠ ℝ con condizioni al bordo che diano D(H_0) ⊂ H²(J)» si può sostituire con «H_0 estensione autoaggiunta di −∂²\|C_c^∞(J)» (VAR-L2c-4). |
| ω aperto non vuoto, non necessariamente un intervallo | VAR-L2 su una componente | corretta: basta una componente connessa (α, β) ⊂ ω |
| dati in D(H_0) | ψ ∈ (SF) | necessaria per questa prova; il caso L² è VAR-Q17, chiuso qui solo per V autonomo (§3) |

### 1.2 Prova, passo per passo

1. **u := ψ − ψ̃; A_0 = −iH_0, B(t) = −iV(t).** È lineare: u risolve lo stesso problema con dato u_0 = ψ_0 − ψ̃_0 ∈ D(H_0). Corretto.

2. **P11(e) ⇒ u ∈ C¹([0,T]; ℋ), con u(t) ∈ D(H_0).** Le ipotesi di P11(e) sono soddisfatte (B ∈ C¹ in norma, x ∈ D(A_0)). È l'unico anello CON-FONTE, e il §2 lo chiude.

3. **H_0u = iu′ − Vu è continua ⇒ u ∈ C([0,T]; H²(J)).**
   - Serve l'equivalenza fra la norma del grafo di H_0 e la norma H²(J) su D(H_0).
   - Questa equivalenza vale per l'interpolazione ‖f′‖ ≤ C(‖f‖ + ‖f″‖) su un intervallo, cioè la versione L² del passo di Taylor di VAR-P3(c), oppure per il teorema del grafo chiuso.
   - Per Dirichlet, Neumann e condizioni periodiche c'è anche la via diretta: ‖f′‖² = −⟨f, f″⟩ ≤ ‖f‖‖f″‖, perché il termine di bordo f f′ si annulla (`var2_l2cor` (0), con SymPy).
   - Il package non scrive questa riga. Va aggiunta (VAR-L2c-4).

4. **H²(J) ⊂ C¹(J̄) ⇒ u, u_x continue.**
   - L'immersione H²(J) ⊂ C_b¹(J̄) è limitata anche per J illimitato.
   - Quindi t ↦ u(t) è continua a valori in C_b¹, e (t, x) ↦ u(t, x) e u_x(t, x) sono **congiuntamente** continue su [0,T] × J̄.
   - Corretto. Conviene dire «congiuntamente» in modo esplicito.

5. **u_t, u_xx ∈ C([0,T]; L²) ⊂ L²_loc; equazione q.o.**
   - La derivata distribuzionale ∂_t u su I × J coincide con u′. Per φ ∈ C_c^∞(I × J) si ha ∬uφ_t = ∫⟨u(t), φ_t(t)⟩dt = −∫⟨u′(t), φ(t)⟩dt: è la regola del prodotto per funzioni C¹ a valori in L².
   - ∂_x²u(t) = −H_0u(t) per ogni t.
   - L'equazione iu′ = H_0u + Vu vale in L²(J) per ogni t, e quindi q.o. su I × J (Fubini).
   - Corretto.

6. **V come funzione su I × J.**
   - VAR-L2 chiede V ∈ L^∞_loc(Ω) come funzione di (t, x). Un elemento di C([0,T]; L^∞(J)) ha un rappresentante congiuntamente misurabile, con |V(t, x)| ≤ sup_t‖V(t)‖_∞ q.o.
   - La ragione: è continuo a valori in L¹_loc(J), quindi Bochner-misurabile, e L¹(I; L¹(K)) ≅ L¹(I × K).
   - Il package non lo dice. È una riga (VAR-L2c-3, MINOR).

7. **u = 0 su I × ω ⇒ VAR-L2 ⇒ u ≡ 0.**
   - L'ipotesi è «q.o. su I × ω». Per la continuità del passo 4 si ha u = 0 ovunque su I × ω.
   - VAR-L2 si applica su una componente (α, β) di ω, con Ω = I × J e u ∈ (SF).
   - Corretto. Conviene scrivere esplicitamente il passaggio da «q.o.» a «ovunque» (VAR-L2c-3).

8. **Continuità in t = 0 ⇒ ψ_0 = ψ̃_0.**
   - Da u ≡ 0 su I × J segue u(t) = 0 in L² per t ∈ (0, T).
   - La continuità in ℋ dà u(0) = 0.
   - Corretto.

### 1.3 Portata

- **(1) Iniettività solo sulle traiettorie; «mai a tempo fisso».** È vera **se e solo se ω non è denso in J**, cioè se J ⊄ ω̄. Le due direzioni:
  - *Se J ∖ ω̄ contiene un intervallo:* una bump C_c^∞ in esso sta in D(H_0), qualunque siano le condizioni al bordo. Quindi la restrizione a tempo fisso non è iniettiva su D(H_0). A t > 0 vale lo stesso, perché U(t, 0) è biiettivo su D(H_0) per P11(c), (e).
  - *Se invece ω è un aperto denso,* anche di misura piccola: f ∈ D(H_0) ⊂ C(J̄) nulla su ω è nulla. Quindi la restrizione a tempo fisso **è** iniettiva su D(H_0).
  - Va corretta la clausola (VAR-L2c-2, MINOR).
  - Illustrazione numerica, `var2_l2cor` (2): dato a supporto in (3.5, 5.5), ω = (0.5, 1.5). Si ottiene max|u(0)| su ω ≈ 1.5·10⁻⁷ (coda di Fourier), mentre max_t max|u(t)| su ω ≈ 0.14.
- **(2) Dati in D(H_0) e V ∈ C¹; dati L² aperti (VAR-Q17).** Corretto. Per V autonomo, il §3 qui sotto chiude il caso L².
- **(3) Lo stato CON-FONTE di P11(e) si trasmette.** Corretto, finché non si applica il fix VAR-L2c-1.

### 1.4 Citazione

- Per VAR-L2-cor in quanto tale non serve una fonte: è un corollario di VAR-L2 e P11(e).
- Per VAR-L2 il PP (§1.3, osservazione «Holmgren», paragrafo «Letteratura») e il LEDGER (riga VAR-L2) citano ora Isakov, JDE 105 (1993) 217–238, e dichiarano Saut–Scheurer parabolico e da non citare. È conforme a CIT-AUDIT-8 (A8, A9, §5 punto 2).
- Osservazione: secondo CIT-AUDIT-8, Isakov tratta soluzioni H^{2m}_loc attraverso x = costante. La classe (SF) chiede u_t ∈ L² ma non u_tt: può essere un poco più larga. «PROBABILMENTE NOTO» resta la formula giusta.

## 2. Fix VAR-L2c-1 (MAGGIORE): prova autosufficiente di VAR-P11(e)

**Enunciato (P11(e)).** A_0 genera un semigruppo C_0 S(t) con ‖S(t)‖ ≤ Me^{ωt}; B ∈ C¹([0,T]; 𝓛(X)) in norma, con b := sup‖B‖; x ∈ D(A_0). Allora u(t) := U(t, 0)x è in C¹([0,T]; X), con u(t) ∈ D(A_0) e u′ = (A_0 + B(t))u.

**Prova.** Si usano solo P11(a), cioè l'equazione mite, e P11(c), cioè la proprietà di evoluzione. Sia f(s) := B(s)u(s), che è continua.

(i) *Due forme dell'equazione mite.*
- Dall'equazione mite e dal semigruppo: u(t + h) = S(t)u(h) + ∫_0^t S(t − s)f(s + h)ds. Basta spezzare ∫_0^{t+h} in ∫_0^h + ∫_h^{t+h} e porre r = s + h.
- Da P11(c) e dall'equazione mite partita da t: u(t + h) = S(h)u(t) + ∫_t^{t+h} S(t + h − r)f(r)dr.

(ii) *Candidato per la derivata.*
- Sia w ∈ C([0,T]; X) l'unica soluzione dell'equazione di Volterra w(t) = S(t)y_0 + ∫_0^t S(t − s)[B′(s)u(s) + B(s)w(s)]ds, con y_0 := A_0x + B(0)x.
- Esiste ed è unica: nucleo limitato, iterazione di Picard, come in P11(a).

(iii) *Convergenza dei rapporti incrementali.* Sia Δ_h(t) := (u(t + h) − u(t))/h, per 0 < h e t ∈ [0, T − h].
- Dalla prima forma di (i): Δ_h(t) = S(t)(u(h) − x)/h + ∫_0^t S(t − s)[(B(s + h) − B(s))/h · u(s + h) + B(s)Δ_h(s)]ds.
- Sottraendo (ii) si ottiene ‖Δ_h(t) − w(t)‖ ≤ Me^{|ω|T}[ε_1(h) + Tε_2(h)] + Me^{|ω|T}b∫_0^t‖Δ_h − w‖, dove:
  - ε_1(h) := ‖(u(h) − x)/h − y_0‖;
  - ε_2(h) := sup_s‖(B(s + h) − B(s))/h · u(s + h) − B′(s)u(s)‖.
- ε_2(h) → 0 perché B è C¹ in norma e u è uniformemente continua.
- ε_1(h) → 0 perché (u(h) − x)/h = (S(h)x − x)/h + h⁻¹∫_0^h S(h − r)f(r)dr → A_0x + f(0) = y_0.
- Per Gronwall, Δ_h → w uniformemente su [0, T − h].

(iv) *u ∈ C¹.*
- u ha derivata destra continua w su [0, T).
- Per ogni funzionale φ ∈ X*, la funzione scalare φ(u(t)) − ∫_0^t φ(w) è continua, con derivata destra nulla, quindi costante (lemma classico di analisi reale).
- Per Hahn–Banach si ha u(t) = x + ∫_0^t w, quindi u ∈ C¹([0,T]; X) con u′ = w.

(v) *u(t) ∈ D(A_0).*
- Dalla seconda forma di (i): (S(h) − I)u(t)/h = Δ_h(t) − h⁻¹∫_t^{t+h}S(t + h − r)f(r)dr → u′(t) − f(t).
- Quindi u(t) ∈ D(A_0) e A_0u(t) = u′(t) − B(t)u(t). ∎

**Osservazioni.**
- Lo spazio X è un Banach qualunque.
- B serve C¹ **in norma** solo in ε_2. Con B fortemente C¹ il passo richiederebbe un argomento di equicontinuità, che non ho verificato. VAR-Q18 (B solo continuo) resta aperto e non è toccato.
- I numeri dei teoremi di Pazy restano non verificati (CIT-AUDIT-8, B4). Con questa prova la citazione diventa solo un'attribuzione. Da memoria, il caso semilineare con f di classe C¹ è in Pazy, cap. 6, §6.1, ma il numero va lasciato fuori (CIT-AUDIT-8: «lasciare "cap. 5" senza numero»).
- Illustrazione numerica, `var2_l2cor` (1). Modello di Galerkin sul toro, V = (1 + ½ sin 3t)cos x, Magnus del 4° ordine con dt = 10⁻³. Il rapporto incrementale centrato tende a −i(H_0 + V(t))u(t) con ordine 2: errori relativi 8.0·10⁻², 2.1·10⁻², 5.4·10⁻³, 8.6·10⁻⁴ per h = 0.02, 0.01, 0.005, 0.002. Inoltre t ↦ ‖u(t)‖_{H²} è continua.

**Nota sullo stato.** La prova del §2 è scritta dal revisore. Per non certificare un proprio testo, propongo che:
- l'autore (S8-VAR) la inserisca in §4.2 come prova di (e);
- il cambio di stato P11(e): CON-FONTE → DIMOSTRATO, e con esso VAR-L2-cor: → DIMOSTRATO, sia confermato da un riscontro di un'altra sessione di CHECK o dal coordinatore.

## 3. Proposta: VAR-L2-cor(b), caso autonomo con dati in L² (chiude VAR-Q17 per V = V(x))

**Enunciato proposto.** Siano V ∈ L^∞(J; ℝ) e H := H_0 + V, autoaggiunto su D(H_0) per Kato–Rellich, perché la perturbazione è limitata. Siano ψ_0, ψ̃_0 ∈ L²(J), ψ(t) = e^{−itH}ψ_0 e ψ̃(t) = e^{−itH}ψ̃_0. Se ψ = ψ̃ q.o. su I × ω, intendendo ψ ∈ C([0,T]; L²) ⊂ L²(I × J), allora ψ_0 = ψ̃_0.

**Prova.** Sia u_0 := ψ_0 − ψ̃_0 e u(t) := e^{−itH}u_0.
1. *Da q.o. a ogni tempo.* Per Fubini, u(τ)|_ω = 0 per q.o. τ ∈ I. Per la continuità di τ ↦ u(τ) in L², vale per ogni τ ∈ I.
2. *Mollificazione nel tempo.* Fissato 0 < ε < T/2, sia ρ_ε ∈ C_c^∞(−ε, ε) con ∫ρ_ε = 1, e sia g_ε := ∫ρ_ε(s)e^{−isH}u_0 ds.
   - Per il calcolo spettrale (Stone): g_ε ∈ D(H) = D(H_0), con Hg_ε = −i∫ρ_ε′(s)e^{−isH}u_0 ds e ‖Hg_ε‖ ≤ ‖ρ_ε′‖_1‖u_0‖. Verifica: `var2_l2cor` (3), con dato a gradino in L² ∖ H¹. ‖Hg‖ resta 2.1864 per 64, 128 e 256 modi, mentre ‖Hψ_0‖ cresce: 93, 268, 771.
   - Per t ∈ (ε, T − ε) si ha e^{−itH}g_ε = ∫ρ_ε(s)u(t + s)ds, che è nullo su ω per il passo 1.
3. *Applicazione del corollario.* v(t) := e^{−i(t+ε)H}g_ε è una soluzione con dato v(0) = e^{−iεH}g_ε ∈ D(H_0), nulla su (0, T − 2ε) × ω.
   - Per VAR-L2-cor (caso autonomo) si ha v(0) = 0, quindi g_ε = 0.
   - In questo caso non serve P11(e): per Stone, e^{−itH}y ∈ C¹([0,T]; L²) ∩ C([0,T]; D(H)) per y ∈ D(H), e i passi 3–8 del §1.2 sono identici.
4. *Limite.* g_ε → u_0 in L² per ε → 0 (continuità forte). Quindi u_0 = 0. ∎

**Portata.** Per V dipendente da t la mollificazione non commuta con l'evoluzione: e^{−itH} va sostituito con U(t, s), e ∫ρ(s)U(t + s, s)… non è una soluzione. VAR-Q17 resta quindi APERTO nel caso non autonomo, ma va ristretto a quel caso (VAR-L2c-6).

## 4. Campione del recepimento post-Gate 8

| punto | richiesta | dove | esito |
|---|---|---|---|
| O3 | normalizzazione unica H = −∂² + x²; rottura a cos t = 0; F5 ritirata; VAR-T10-F FALSO solo nella forma «al tempo della lente/Fourier» | PP Convenzioni («Normalizzazione unica dell'oscillatore»); §4.3, «Correzione rispetto a F6» e (3)(ii)–(iv); LEDGER VAR-T10-F | **conforme**. γ = −(tan t)/2, rottura a t ∈ π/2 + πℤ (−i·parità), parola banale a t ∈ πℤ, attraversamento della lente t = π/4: coincide con le mie verifiche `var_misc` (6) e `var_num` (B). La riga 23 del PP (tabella delle predizioni) conserva «\|t\| < π (normalizzazione H/2)» solo come testo della predizione, e l'esito accanto la corregge: accettabile. |
| O8 | VAR-P3 è una stima di modulo, non un certificato di robustezza | PP §1.6, «Natura del risultato»; LEDGER VAR-P3 («DIMOSTRATO come stima di modulo; non è un certificato di robustezza in DM2»); VAR-Q19 aperta per la Fase 9 | **conforme** |
| O17 | «fuori dalle fasce di silenzio, in (SF)» | PP §1.5(i), «Lettura»; LEDGER VAR-T1(c) | **conforme**. VAR-T1(c)-Q10 resta APERTO, come deve. |
| O20 | VAR-L2-cor non va citato da righe DIMOSTRATO | LEDGER_ROWS: l'unica occorrenza è la propria riga e la nota in testa | **conforme** |
| CIT-AUDIT-8 §5 p. 2 | Isakov 1993 per VAR-L2; Saut–Scheurer parabolico | PP §1.3 «Letteratura»; §9 riga VAR-L1; LEDGER VAR-L2 | **conforme**. Residuo: la tabella dei fix in §9 (riga VAR-16, l. 347) dice ancora «Saut–Scheurer 1987 e Isakov 1993 citati come probabile fonte» (VAR-L2c-7). |

## 5. Fix

| fix | severità | dove | testo proposto |
|---|---|---|---|
| VAR-L2c-1 | MAGGIORE | PP §4.2 (e); LEDGER VAR-P11(e), VAR-L2-cor | inserire la prova del §2 qui sopra. Stato di P11(e) → DIMOSTRATO, e di VAR-L2-cor → DIMOSTRATO, dopo un riscontro di terzi. Finché non c'è, VAR-L2-cor è CON-FONTE e non citabile da righe DIMOSTRATO. |
| VAR-L2c-2 | MINORE | PP §1.3 VAR-L2-cor, Portata (1); LEDGER (enunciato) | «mai a tempo fisso **se ω non è denso in J**; se ω è un aperto denso la restrizione a tempo fisso è già iniettiva su D(H_0) ⊂ C(J̄)» |
| VAR-L2c-3 | MINORE | prova di VAR-L2-cor | una riga sul rappresentante congiuntamente misurabile di V, con \|V\| ≤ sup_t‖V(t)‖_∞, e una sul passaggio «q.o. su I × ω ⇒ ovunque» per continuità |
| VAR-L2c-4 | MINORE | enunciato e prova | «H_0 estensione autoaggiunta di −∂²\|C_c^∞(J)»: D(H_0) ⊂ H²(J) è automatico; aggiungere l'equivalenza della norma del grafo con H² (interpolazione) e la continuità **congiunta** di u e u_x |
| VAR-L2c-5 | facoltativo | enunciato | la realtà di V non è usata dalla prova; si può togliere, o dichiarare che serve solo per l'unitarietà |
| VAR-L2c-6 | proposta | PP §1.3, nuovo punto (b); open_questions VAR-Q17 | inserire VAR-L2-cor(b), cioè il §3 (V autonomo, dati in L²); restringere VAR-Q17 al caso V dipendente da t |
| VAR-L2c-7 | MINORE | PP §9, riga VAR-16 | aggiungere «(corretto post-Gate 8: solo Isakov 1993; Saut–Scheurer è parabolico)» |

## 6. Script

`work/CHECK-F8/sympy/var2_l2cor.py`, con uscita `var2_l2cor.out`: **TUTTO OK**, 12 controlli.

Comando:
```
D:\ProblemaBase\.venv\Scripts\python.exe -I work/CHECK-F8/sympy/var2_l2cor.py
```

**(0) SymPy.** Su polinomi di grado 6 che soddisfano le condizioni al bordo (Dirichlet, Neumann, periodiche), il termine di bordo f f′ è nullo e ‖f′‖² = −⟨f, f″⟩.

**(1) P11(e).** Su un modello di Galerkin con V dipendente dal tempo:
- il rapporto incrementale tende a −i(H_0 + V)u, con ordine 2;
- ‖u(t)‖_{H²} è continua;
- ‖u(t)‖_{L²} è costante.

Nella prima esecuzione questo controllo è fallito per un artefatto: il dato era troppo ruvido, con k²h ≫ 1 sui modi alti, e quindi il regime asintotico non era raggiunto. L'ho corretto con un dato a coefficienti gaussiani e h fino a 0.002. Non è un problema della tesi.

**(2) Portata.** Restrizione a ω nulla a t = 0 (1.5·10⁻⁷, coda di Fourier del bump), traiettoria non nulla su I × ω (0.14). Nella prima esecuzione la soglia 10⁻⁸ era più stretta della coda di Fourier; ora la soglia è relativa.

**(3) Caso autonomo con dato in L².** g_ε ∈ D(H), con Hg_ε = −i∫ρ′U u_0, e la stima è uniforme nel troncamento.

Gli script dell'autore non sono stati rieseguiti per questo audit: VAR-L2-cor non ne ha.
