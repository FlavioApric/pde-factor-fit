# AUDIT S8-DICT, controllo leggero di R6-T(f) — S-CHECK-F8-DICT · 27/10/2026

Richiesta: controllo leggero, chiesto dal coordinatore dopo il Gate 8 (`GATE8.md`). Nel LEDGER DICT-R6 è DIMOSTRATO per (a)–(e), mentre (f) è PROVA SCRITTA.

Oggetto:
- la nuova prova di R6-T(f) (`work/S8-DICT/PROOF_PACKAGE.md` §3.6: enunciato (f), prova di (f), (H-dato));
- un campione del recepimento di MAG-1…MAG-4 (`AUDIT_S8-DICT_rev2.md`) e di O5, O13, O15 (ATTACK-8).

Letti:
- `work/S8-DICT/RECEPIMENTO.md`, sezioni "AUDIT_S8-DICT_rev2" e "ATTACK-8";
- PROOF_PACKAGE §2.2 (N1(ii)), §2.6 ("Significato e ipotesi", "Sistemi", corollario DICT-MAG-NU), §3.3 (Teorema A), §3.5 (Teorema G-R), §3.6 e §7.

Script: `sympy/dict3_r6f.py` → `.out`: **8/8 PASS**.
- T1: triangolarità stretta dei getti di W = I + V nel punto base, ordini 1–6.
- T2: non località in x_1 ≠ x_0.
- T3: ∂_t commuta con W.

## Esito: **PASS-con-fix** (due fix MINOR di redazione). Stato proposto per R6(f): **DIMOSTRATO** dopo R6f-1 e R6f-2.

## 1. Prova di R6-T(f)

**Dipendenze.** La prova di (f) usa solo:
- (H-W): W = I + V, con V operatore di Volterra simmetrico di ENC-1(3), DIMOSTRATO;
- DICT-N1(ii), DIMOSTRATO;
- Teorema A(iii), DIMOSTRATO dopo DICT-1.

ENC-T2(c′) è nominato solo per dire che non è più usato. VAR-L2-cor non compare nella §3.6. (H-dato) cita ora N1(ii) e il Teorema A. Nessuna dipendenza da claim non auditati.

**Non certificabilità: corretta.** Le ipotesi del Teorema A(iii) sono soddisfatte:
- gli atomi ∂_t^jL_q^k sono operatori differenziali lineari a coefficienti lisci, perché q ∈ C^∞ per (H-q);
- sono linearmente indipendenti, perché hanno simboli principali distinti ∂_t^j∂_x^{2k};
- i funzionali "getto in un punto" (derivate fino all'ordine N in punti di Ω) sono lineari e continui su C^∞(Ω).

A(iii) dà quindi, per ogni u con fit al livello n e ogni dato finito, una v con gli stessi dati e senza legge al livello n. L'uso di N1(ii) è corretto: N1(ii)(b) è appunto il Teorema A. Questa parte non usa W e vale in ogni punto, non solo in x_0.

**R6f-1 (MINOR: giustificazione e luogo della triangolarità).** La prova dice: "W = I + Volterra e conserva i dati di Cauchy in x_0, quindi la parte d'ordine N di j^N(Wu) è quella di u più termini d'ordine minore". Il "quindi" non segue dalla conservazione dei dati di Cauchy, che riguarda solo gli ordini 0 e 1. La ragione corretta è un'altra.
- Se j^{m−1}f(x_0) = 0, allora f = O(|x − x_0|^m) e Vf(x) = ∫_{2x_0−x}^{x}H(x, s)f(s)ds = O(|x − x_0|^{m+1}). Quindi j^m(Vf)(x_0) = 0.
- Dunque j^m(Wf)(x_0) = j^m f(x_0) + (funzione lineare di j^{m−1}f(x_0)): triangolare unipotente. Verifica: `dict3_r6f` T1, ordini 1–6.
- W agisce nella sola x e commuta con ∂_t (T3), quindi lo stesso vale per i getti in (t, x_0).
- La triangolarità vale **solo nei punti (t, x_0)**. In x_1 ≠ x_0 il valore di Vf dipende da f lontano da x_1 (T2: f nulla vicino a x_1 = 1/2 e (Vf)(x_1) = 0,0191).

Riparazione: scrivere "nei punti (t, x_0)" nell'enunciato di (f) e sostituire il "quindi" con l'argomento O(|x − x_0|^{m+1}).

**R6f-2 (MINOR: "a nessun livello" contro "al livello n").** L'enunciato dice "nessun getto finito certifica Ann_q(u) ≠ 0", cioè l'esistenza di una legge a qualche livello. La prova, con A(iii), dà invece una v senza legge al livello n fissato. Ci sono due modi di sistemare.
- (i) Enunciare (f) al livello n, che è l'uso che ne fa la regola R6.
- (ii) Aggiungere il passo di Baire. Sia Z l'intersezione dei nuclei dei funzionali di dato. u + Z è un sottospazio affine chiuso di C^∞(Ω), quindi di Fréchet e di Baire. Ogni F_n ∩ (u + Z) è chiuso, e ha interno vuoto in u + Z perché A(iii) si applica in ogni suo punto. Allora ∪_n F_n ∩ (u + Z) è magro, ed esiste v ∈ u + Z senza legge a nessun livello.

Con (ii) l'enunciato attuale è dimostrato.

**(a)–(e)** non dipendono da (f): confermato, nessuna parte di (a)–(e) cita (f).

## 2. Campione del recepimento

- **MAG-1:** recepito. "Classe": A, V ∈ C^∞(J × Ω; ℝ) dipendono da (t, x); ∇ e ∇^⊥ sono spaziali. "Caso statico": coperto solo per u stazionaria e χ = χ(x).
- **MAG-2:** recepito. U ⊂ {u ≠ 0}; u ≢ 0 dichiarato, con la nota sul caso banale.
- **MAG-3:** recepito. Il "se e solo se" vale per supp B ⊂ {u ≠ 0}. Il caso in cui supp B incontra Z(u) è dichiarato non trattato.
- **MAG-4:** recepito. La tesi è "campo magnetico diverso", dB ≢ 0. Ho ricontrollato la formula della componente (1,2): ∂_1B_2 − ∂_2B_1 = −div_{12}(|u|^{−2}∇_{12}χ). Il principio del massimo si applica su un intorno di supp χ(t, ·) con chiusura in {u ≠ 0}, dove |u|^{−2} è liscia e positiva.
  - Nota non bloccante: SYS-N3 è enunciato su un prodotto J × Ω con u ≠ 0 ovunque, mentre U è un aperto qualsiasi dello spazio-tempo. La prova funziona perché l'identità delle differenze è puntuale (`dict2_mag` M1, M2).
- **O15:** recepito. DICT-MAG-NU è un corollario di SYS-N3(c) senza stato autonomo; la riga canonica è SYS-N3, con div_x(ρ²B) = 0.
- **O5:** recepito. Paragrafo "Significato e ipotesi": ID-ker, unicità solo sotto (H-ex). Controesempio u = t + sin x nella classe u_t = a u_xx + b u. Ricontrollato a mano:
  - Φ_u(a, b) = −a sin x + b(t + sin x) = 0 forza b = 0 e poi a = 0, quindi ker Φ_u = 0;
  - una legge richiederebbe bt + (b − a) sin x ≡ 1, che è impossibile.
- **O13:** recepito. In G-R l'ipotesi è "(H-ID)". "(ID)" resta solo nella nota storica della tabella §7 ("prima (ID)").

## 3. Sintesi
- R6-T(f): **PASS-con-fix**. Stato proposto: **DIMOSTRATO** dopo R6f-1 e R6f-2.
  - R6f-1: triangolarità solo in (t, x_0), con l'argomento O(|x − x_0|^{m+1}).
  - R6f-2: enunciato al livello n, oppure passo di Baire.
  - Nessuna dipendenza da ENC-T2(c′) o da VAR-L2-cor.
- Recepimento di MAG-1…4, O5, O13, O15: confermato nel campione.
